"""数据库备份 / 恢复：把做题记录做成能从任何地方带走的东西。

为什么需要
----------
`data/pta.db` 是**本地状态**，不进 Git（否则每次提交都在二进制 diff，
而且会把你没做完的题一起广播出去）。

但这个库里装着你的**提交历史、得分、错题**，丢了很肉疼。所以：

- `backup`  —— 复制一份带时间戳的库到 `backups/`
- `export`  —— 导出成**纯文本 JSON**（可以进 Git、可以人眼看、可以 diff）
- `import`  —— 从 JSON 或 .db 恢复（幂等：按时间戳 + 题目标题去重）

用法
----
    python tools/backup_db.py backup              # 备份当前库
    python tools/backup_db.py export              # 导出成 JSON（默认 backups/progress.json）
    python tools/backup_db.py export -o x.json    # 指定输出
    python tools/backup_db.py import x.json       # 从 JSON 恢复
    python tools/backup_db.py import x.db         # 从 .db 恢复
    python tools/backup_db.py list                # 看看有哪些备份
"""
from __future__ import annotations

import json
import os
import shutil
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

import _console                                                   # noqa: E402
from app import config  # noqa: E402

TABLES = ("problems", "testcases", "submissions", "submission_cases", "mastery")


def _db_path() -> Path:
    cfg = config.get()
    return Path(getattr(cfg, "db_path", None) or (ROOT / "data" / "pta.db"))


def _backup_dir() -> Path:
    d = ROOT / "backups"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _counts(conn: sqlite3.Connection) -> dict[str, int]:
    out = {}
    for t in TABLES:
        try:
            out[t] = conn.execute("SELECT COUNT(*) FROM %s" % t).fetchone()[0]
        except sqlite3.Error:
            out[t] = -1
    return out


def _show(title: str, c: dict[str, int]) -> None:
    print(title)
    for k in TABLES:
        print("   %-18s %s" % (k, c[k] if c[k] >= 0 else "(表不存在)"))


# --------------------------------------------------------------------- #
def cmd_backup() -> int:
    src = _db_path()
    if not src.exists():
        print("找不到数据库：%s" % src)
        return 1
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = _backup_dir() / ("pta_%s.db" % stamp)
    shutil.copy2(src, dst)
    with sqlite3.connect(str(dst)) as c:
        _show("备份内容：", _counts(c))
    print("\n已备份到 %s  (%d 字节)" % (dst, dst.stat().st_size))
    return 0


def cmd_export(out_arg: str | None) -> int:
    src = _db_path()
    if not src.exists():
        print("找不到数据库：%s" % src)
        return 1
    out = Path(out_arg) if out_arg else (_backup_dir() / "progress.json")
    out.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(str(src)) as c:
        c.row_factory = sqlite3.Row
        pid2title = {r["id"]: r["title"]
                     for r in c.execute("SELECT id, title FROM problems")}

        subs = []
        for r in c.execute("SELECT * FROM submissions ORDER BY id"):
            d = dict(r)
            d["problem_title"] = pid2title.get(d.get("problem_id"), "")
            subs.append(d)

        mastery = []
        for r in c.execute("SELECT * FROM mastery"):
            d = dict(r)
            d["problem_title"] = pid2title.get(d.get("problem_id"), "")
            mastery.append(d)

        cases = [dict(r) for r in c.execute("SELECT * FROM submission_cases ORDER BY id")]

    payload = {
        "_note": "本平台做题记录导出。problem_title 是给人和跨库对应用的主键，导入时优先按它匹配。",
        "_exported_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "submissions": subs,
        "submission_cases": cases,
        "mastery": mastery,
    }
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print("已导出 %d 条提交 / %d 条逐点明细 / %d 条题目进度" %
          (len(subs), len(cases), len(mastery)))
    print("→ %s  (%d 字节)" % (out, out.stat().st_size))
    return 0


def cmd_import(src_arg: str) -> int:
    src = Path(src_arg)
    if not src.exists():
        print("找不到文件：%s" % src)
        return 1
    dst = _db_path()
    if not dst.exists():
        print("目标数据库不存在，先启动一次平台让它建库：%s" % dst)
        return 1

    if src.suffix.lower() == ".db":
        return _import_db(src, dst)

    payload = json.loads(src.read_text(encoding="utf-8"))
    subs = payload.get("submissions", [])
    cases = payload.get("submission_cases", [])
    mastery = payload.get("mastery", [])

    with sqlite3.connect(str(dst)) as c:
        c.row_factory = sqlite3.Row
        cols_p = {r[1] for r in c.execute("PRAGMA table_info(problems)")}
        cols_s = {r[1] for r in c.execute("PRAGMA table_info(submissions)")}
        cols_sc = {r[1] for r in c.execute("PRAGMA table_info(submission_cases)")}
        cols_m = {r[1] for r in c.execute("PRAGMA table_info(mastery)")}

        # 老备份按标题对题目；新备份优先按标题（跨库 id 会变）
        title2pid = {r["title"]: r["id"]
                     for r in c.execute("SELECT id, title FROM problems")}

        old2new: dict[int, int] = {}
        added_s = added_sc = added_m = 0

        for s in subs:
            pid = title2pid.get(s.get("problem_title", ""))
            if pid is None:
                pid = s.get("problem_id")
            if pid is None:
                continue
            # 去重键：题目 + 时间 + 判定 + 代码，四样都一样才认作同一条。
            # 只用时间戳不够 —— 连点两次提交会落在同一秒里，会被误判成重复。
            def _sig(pid_, s_):
                return (pid_, s_.get("created_at"), s_.get("verdict"),
                        (s_.get("code") or "").strip())

            seen = {(r["s_pid"], r["s_at"], r["s_v"], r["s_code"])
                    for r in c.execute(
                        "SELECT problem_id AS s_pid, created_at AS s_at,"
                        " verdict AS s_v, TRIM(COALESCE(code,'')) AS s_code"
                        " FROM submissions")}

            for s in subs:
                pid = title2pid.get(s.get("problem_title", ""))
                if pid is None:
                    pid = s.get("problem_id")
                if pid is None:
                    continue
                sig = _sig(pid, s)
                if sig in seen:
                    continue
                seen.add(sig)
                row = {k: v for k, v in s.items()
                       if k in cols_s and k not in ("id", "problem_title")}
                row["problem_id"] = pid
                keys = list(row)
                cur = c.execute(
                    "INSERT INTO submissions (%s) VALUES (%s)" %
                    (",".join(keys), ",".join("?" * len(keys))),
                    tuple(row[k] for k in keys))
                old2new[s["id"]] = cur.lastrowid
                added_s += 1

        for sc in cases:
            new_sid = old2new.get(sc.get("submission_id"))
            if new_sid is None:
                continue
            row = {k: v for k, v in sc.items()
                   if k in cols_sc and k not in ("id", "submission_id")}
            row["submission_id"] = new_sid
            keys = list(row)
            c.execute("INSERT INTO submission_cases (%s) VALUES (%s)" %
                      (",".join(keys), ",".join("?" * len(keys))),
                      tuple(row[k] for k in keys))
            added_sc += 1

        for m in mastery:
            pid = title2pid.get(m.get("problem_title", "")) or m.get("problem_id")
            if pid is None:
                continue
            exist = c.execute("SELECT problem_id FROM mastery WHERE problem_id=?",
                              (pid,)).fetchone()
            row = {k: v for k, v in m.items()
                   if k in cols_m and k not in ("problem_id", "problem_title")}
            if exist:
                # 已有的不覆盖（本地进度更权威），只补空字段
                sets = ", ".join("%s=COALESCE(%s,?)" % (k, k) for k in row)
                c.execute("UPDATE mastery SET %s WHERE problem_id=?" % sets,
                          tuple(row.values()) + (pid,))
            else:
                row["problem_id"] = pid
                keys = list(row)
                c.execute("INSERT INTO mastery (%s) VALUES (%s)" %
                          (",".join(keys), ",".join("?" * len(keys))),
                          tuple(row[k] for k in keys))
                added_m += 1
        c.commit()
        _show("\n导入后：", _counts(c))

    print("\n新增：提交 %d 条 / 逐点明细 %d 条 / 题目进度 %d 条"
          % (added_s, added_sc, added_m))
    print("（已存在的记录自动跳过，可以反复执行）")
    return 0


def _import_db(src: Path, dst: Path) -> int:
    """从另一个 .db 直接搬记录（用 ATTACH，不覆盖本地题目）。"""
    with sqlite3.connect(str(dst)) as c:
        c.execute("ATTACH DATABASE ? AS src", (str(src),))
        try:
            c.row_factory = sqlite3.Row
            cols_s = {r[1] for r in c.execute("PRAGMA table_info(submissions)")}
            cols_sc = {r[1] for r in c.execute("PRAGMA table_info(submission_cases)")}
            src_cols_s = {r[1] for r in c.execute("PRAGMA src.table_info(submissions)")}
            src_cols_sc = {r[1] for r in c.execute("PRAGMA src.table_info(submission_cases)")}

            title2pid = {r["title"]: r["id"]
                         for r in c.execute("SELECT id, title FROM problems")}
            src_pid2title = {r["id"]: r["title"]
                             for r in c.execute("SELECT id, title FROM src.problems")}

            added_s = added_sc = 0
            old2new: dict[int, int] = {}

            def _sig(pid_, d_):
                return (pid_, d_.get("created_at"), d_.get("verdict"),
                        (d_.get("code") or "").strip())

            seen = {(r["s_pid"], r["s_at"], r["s_v"], r["s_code"])
                    for r in c.execute(
                        "SELECT problem_id AS s_pid, created_at AS s_at,"
                        " verdict AS s_v, TRIM(COALESCE(code,'')) AS s_code"
                        " FROM submissions")}

            for r in c.execute("SELECT * FROM src.submissions ORDER BY id"):
                d = dict(r)
                pid = title2pid.get(src_pid2title.get(d["problem_id"], ""))
                if pid is None:
                    continue
                sig = _sig(pid, d)
                if sig in seen:
                    continue
                seen.add(sig)
                row = {k: v for k, v in d.items()
                       if k in cols_s and k in src_cols_s and k != "id"}
                row["problem_id"] = pid
                keys = list(row)
                cur = c.execute("INSERT INTO submissions (%s) VALUES (%s)" %
                                (",".join(keys), ",".join("?" * len(keys))),
                                tuple(row[k] for k in keys))
                old2new[d["id"]] = cur.lastrowid
                added_s += 1

            for r in c.execute("SELECT * FROM src.submission_cases ORDER BY id"):
                d = dict(r)
                new_sid = old2new.get(d.get("submission_id"))
                if new_sid is None:
                    continue
                row = {k: v for k, v in d.items()
                       if k in cols_sc and k in src_cols_sc and k != "id"}
                row["submission_id"] = new_sid
                keys = list(row)
                c.execute("INSERT INTO submission_cases (%s) VALUES (%s)" %
                          (",".join(keys), ",".join("?" * len(keys))),
                          tuple(row[k] for k in keys))
                added_sc += 1
            c.commit()
            _show("\n导入后：", _counts(c))
        finally:
            c.execute("DETACH DATABASE src")
    print("\n新增：提交 %d 条 / 逐点明细 %d 条" % (added_s, added_sc))
    return 0


def cmd_list() -> int:
    d = _backup_dir()
    files = sorted(list(d.glob("*.db")) + list(d.glob("*.json")))
    if not files:
        print("还没有备份。跑一次：python tools/backup_db.py backup")
        return 0
    print("备份目录 %s" % d)
    for f in files:
        print("   %-32s %9d 字节   %s"
              % (f.name, f.stat().st_size,
                 datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M")))
    return 0


USAGE = """数据库备份 / 恢复

    python tools/backup_db.py backup           备份当前库到 backups/
    python tools/backup_db.py export [-o 文件] 导出成 JSON（可进 Git）
    python tools/backup_db.py import <文件>    从 JSON 或 .db 恢复
    python tools/backup_db.py list             列出已有备份
"""


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(USAGE)
        return 0
    cmd, rest = args[0], args[1:]
    if cmd == "backup":
        return cmd_backup()
    if cmd == "export":
        out = None
        if "-o" in rest:
            out = rest[rest.index("-o") + 1]
        return cmd_export(out)
    if cmd == "import":
        if not rest:
            print("要指定文件：python tools/backup_db.py import <文件>")
            return 1
        return cmd_import(rest[0])
    if cmd == "list":
        return cmd_list()
    print(USAGE)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
