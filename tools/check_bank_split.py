"""校验静态题库的分片与再分片产物是否「一个测试点都没丢」。

为什么需要这个脚本
------------------
题库导出有两层拆分，任何一层写错都是**静默**的：

1. `bank/index.json`（轻索引）+ `bank/<科目>.json`（整科）
2. 单题测试点超 50 KB 的，再拆成 `bank/cases/<id>.json`

第 2 层是后加的。它的失败方式特别隐蔽 —— 科目包里那道题的 `cases` 变成空数组，
前端照样能打开题面，只有真去判题时才发现「这题没有测试点」。所以必须有一条
把两边拼起来跟数据库逐字节对账的检查。

检查项
------
1. 题数 / 测试点总数守恒（库 vs 产物）
2. 每道题的每个测试点内容逐字段一致（stdin / expected_stdout / is_sample / points / ord）
3. `index.json` 的 `has_cases` 与库里真实情况一致（**拆过的题不能变成 false**）
4. `bank/cases/` 下没有孤儿文件
5. `sw.js` 存在且被 `index.html` 注册（缓存策略的载体，别漏拷）

用法
----
    python tools/check_bank_split.py                # 检查 docs/
    python tools/check_bank_split.py --dir data/tmp/dist
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import _console                                            # noqa: E402,F401
from app import db                                      # noqa: E402

_FAIL = []


def check(name: str, ok: bool, detail: str = "") -> None:
    print("  %s %s%s" % ("✓" if ok else "✗", name, ("  — " + detail) if detail else ""))
    if not ok:
        _FAIL.append(name)


def _norm(cases) -> str:
    """只比产物真正带出去的字段。

    ★ `is_sample` 在库里是 1/0、JSON 里是 true/false —— 直接比会全军覆没，
      统一成 bool 再比。（第一版就是这么误报的，1524 道题全判不一致。）
    ★ 库里有 `kind` / `explanation`，产物不导出，不能拿来比。
    """
    return json.dumps([{
        "ord": c.get("ord"),
        "is_sample": bool(c.get("is_sample")),
        "stdin": c.get("stdin") or "",
        "expected_stdout": c.get("expected_stdout") or "",
        "points": c.get("points"),
    } for c in cases], sort_keys=True, ensure_ascii=False)


def main() -> int:
    ap = argparse.ArgumentParser(description="校验题库分片产物")
    ap.add_argument("--dir", default=str(ROOT / "docs"), help="产物目录（默认 docs/）")
    args = ap.parse_args()
    out = Path(args.dir)

    bank_dir = out / "bank"
    idx_path = bank_dir / "index.json"
    if not idx_path.is_file():
        print("没找到 %s —— 先跑 tools/export_static.py --with-cases" % idx_path)
        return 2

    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    print("产物：%s" % out)
    print("  asset_version=%s / 题 %d / 拆分题 %d\n"
          % (idx.get("asset_version"), len(idx.get("items") or []),
             len(idx.get("cases_split") or [])))

    # ---- 库（空库就跳过数据对账，CI 上没 seed 也不会红）----
    db.init_db()
    rows = db.query("""
        SELECT t.* FROM testcases t
        JOIN problems p ON p.id = t.problem_id
        WHERE p.status='published' ORDER BY t.problem_id, t.ord
    """)
    if not rows:
        print("题库是空的，跳过数据对账")
        want = {}
    else:
        want = {}
        for r in rows:
            want.setdefault(r["problem_id"], []).append(r)

    # ---- 产物侧拼回来 ----
    got: dict[int, list] = {}
    # 主包里还留着多少（拆过的题这里必须是空的，否则等于没省下流量）
    main_cases: dict[int, list] = {}
    for sub in idx.get("subjects") or []:
        part = json.loads((bank_dir / ("%s.json" % sub)).read_text(encoding="utf-8"))
        for p in part["items"]:
            main_cases[p["id"]] = p.get("cases") or []
            got[p["id"]] = p.get("cases") or []
    for pid in idx.get("cases_split") or []:
        f = bank_dir / "cases" / ("%s.json" % pid)
        got[pid] = json.loads(f.read_text(encoding="utf-8"))["cases"] if f.is_file() else []

    if want:
        n_got, n_want = sum(len(v) for v in got.values()), sum(len(v) for v in want.values())
        check("测试点总数守恒", n_got == n_want, "产物 %d / 库 %d" % (n_got, n_want))
        check("题数守恒",
              len([k for k, v in got.items() if v]) == len(want),
              "产物 %d / 库 %d" % (len([k for k, v in got.items() if v]), len(want)))

        miss = sorted(k for k in want if not got.get(k))
        check("没有整题丢测试点", not miss, str(miss[:8]) if miss else "")

        diff = sorted(k for k in want if got.get(k) and _norm(got[k]) != _norm(want[k]))
        check("逐题内容一致", not diff, ("不一致 %d 道：%s" % (len(diff), diff[:5])) if diff else "")

        extra = sorted(k for k in got if got[k] and k not in want)
        check("没有库外的题", not extra, str(extra[:8]) if extra else "")

        bad = [p["id"] for p in (idx.get("items") or [])
               if bool(p.get("has_cases")) != bool(want.get(p["id"]))]
        check("index.has_cases 与库一致", not bad, ("不符 %d 道：%s" % (len(bad), bad[:5])) if bad else "")

    # ---- 结构检查 ----
    known_ids = {p["id"] for p in (idx.get("items") or [])}
    case_dir = bank_dir / "cases"
    orphans = []
    if case_dir.is_dir():
        orphans = sorted({int(f.stem) for f in case_dir.glob("*.json")} - known_ids)
    check("bank/cases/ 无孤儿文件", not orphans, str(orphans[:8]) if orphans else "")

    split_ids = set(idx.get("cases_split") or [])
    leaked = sorted(pid for pid in split_ids if main_cases.get(pid))
    check("拆分的题主包里确实没留测试点", not leaked, str(leaked[:8]) if leaked else "")
    check("cases_split 非空时目录存在",
          not split_ids or case_dir.is_dir(), "%d 道" % len(split_ids))

    # ---- Service Worker ----
    sw = out / "sw.js"
    html = (out / "index.html")
    check("sw.js 已产出", sw.is_file())
    if sw.is_file() and html.is_file():
        check("index.html 注册了 sw.js",
              "serviceWorker" in html.read_text(encoding="utf-8", errors="ignore"))

    print()
    if _FAIL:
        print("失败 %d 项：%s" % (len(_FAIL), "、".join(_FAIL)))
        return 1
    print("全部通过 ✓")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
