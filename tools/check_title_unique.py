# -*- coding: utf-8 -*-
"""题库标题全局查重 —— `seed.ensure()` 按 title 判重（跨科目也算），撞名会被**静默跳过**。

用法:
    python tools/check_title_unique.py            # 查题库模块
    python tools/check_title_unique.py --db       # 连本地库一起查
    python tools/check_title_unique.py --new "标题1" "标题2"   # 查待加的新标题

为什么单独做一把工装
--------------------
2026-10-19 踩过：Python 线的「滑动窗口最大值」与 C++ 章节同名，ensure 少进 1 题，
**不报错**，只在题量对不上时才发现。加题时先把新标题过一遍这把尺子最省事。
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

MODULES = [
    ("seed", "CORE_PROBLEMS"),
    ("problems_bank", "BANK_PROBLEMS"),
    ("problems_bank_py_theory", "PY_THEORY_PROBLEMS"),
    ("problems_bank_py_theory2", "PY_THEORY2_PROBLEMS"),
    ("problems_bank_py_prog", "PY_PROG_PROBLEMS"),
    ("problems_bank_py_tricks", "PY_TRICKS_PROBLEMS"),
    ("problems_bank_py_bits", "PY_BITS_PROBLEMS"),
    ("problems_bank_ext2", "EXT2_PROBLEMS"),
    ("problems_bank_ds", "DS_PROBLEMS"),
    ("problems_bank_ds_theory", "DS_THEORY_PROBLEMS"),
    ("problems_bank_ds_prog", "DS_PROG_PROBLEMS"),
    ("problems_bank_ds_tricks", "DS_TRICKS_PROBLEMS"),
    ("problems_bank_linux", "LINUX_PROBLEMS"),
    ("problems_bank_cpp_theory", "CPP_THEORY_PROBLEMS"),
    ("problems_bank_cpp_theory2", "CPP_THEORY2_PROBLEMS"),
    ("problems_bank_cpp_prog", "CPP_PROG_PROBLEMS"),
]


def collect() -> dict[str, list[str]]:
    seen: dict[str, list[str]] = {}
    for mod, attr in MODULES:
        try:
            m = importlib.import_module("app." + mod)
        except Exception as exc:                      # 模块还没写 / 写坏了
            print("[skip] %s: %s" % (mod, exc))
            continue
        for p in getattr(m, attr, []) or []:
            seen.setdefault(str(p.get("title", "")).strip(), []).append(mod)
    return seen


def main() -> int:
    argv = sys.argv[1:]
    seen = collect()

    dup = {t: ms for t, ms in seen.items() if len(ms) > 1}
    print("题库模块标题总数: %d（去重后）" % len(seen))
    if dup:
        print("★ 重复标题 %d 组：" % len(dup))
        for t, ms in sorted(dup.items()):
            print("    %s  <- %s" % (t, ", ".join(sorted(set(ms)))))
    else:
        print("模块内无重复标题 ✅")

    if "--db" in argv:
        import sqlite3
        db = ROOT / "data" / "pta.db"
        if db.exists():
            conn = sqlite3.connect(str(db))
            rows = conn.execute("SELECT title, COUNT(*) c FROM problems GROUP BY title HAVING c > 1").fetchall()
            print("库内重复标题: %d 组%s" % (len(rows), "" if rows else " ✅"))
            for t, c in rows[:20]:
                print("    %s ×%d" % (t, c))
            total = conn.execute("SELECT COUNT(*) FROM problems").fetchone()[0]
            print("库内总题数: %d" % total)
            conn.close()

    if "--new" in argv:
        i = argv.index("--new")
        news = argv[i + 1:]
        hit = [t for t in news if t in seen]
        print("待查新标题 %d 条，撞车 %d 条%s" % (len(news), len(hit), " ✅" if not hit else ""))
        for t in hit:
            print("    ★ 已存在: %s (%s)" % (t, ", ".join(sorted(set(seen[t])))))
    return 1 if dup else 0


if __name__ == "__main__":
    sys.exit(main())
