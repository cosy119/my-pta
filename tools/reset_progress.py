"""清空做题记录（题目与测试点原样保留）。

什么情况下用：
- 打分规则 / 题目分值调整过，老记录的口径和新规则对不上
- 想从干净状态开始刷题

**只删这三张表的数据**：submissions / submission_cases / mastery
**不碰**：problems / testcases / settings / ai_config

默认是「预览模式」，只报数量；确认要清就加 `--yes`。
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

import _console                                                   # noqa: E402
from app import db  # noqa: E402


def main() -> int:
    dry = "--yes" not in sys.argv
    counts = {t: (db.query_one("SELECT COUNT(*) AS n FROM %s" % t) or {}).get("n", 0)
              for t in ("problems", "testcases", "submissions", "submission_cases", "mastery")}

    print("当前数据：")
    for t, n in counts.items():
        print("  %-18s %d" % (t, n))
    print()

    if dry:
        print("预览模式 —— 什么也没删。")
        print("要真的清空做题记录（保留题目），重新跑：")
        print("  python tools/reset_progress.py --yes")
        return 0

    db.execute("DELETE FROM submission_cases")
    db.execute("DELETE FROM submissions")
    db.execute("DELETE FROM mastery")
    # 让自增 id 从 1 重新开始，历史看起来清爽。
    # 注意：sqlite_sequence 只在建表用了 AUTOINCREMENT 时才存在，所以这里要容错。
    try:
        db.execute("DELETE FROM sqlite_sequence WHERE name IN "
                   "('submissions','submission_cases')")
    except Exception:
        pass

    print("已清空做题记录。题目与测试点保留：")
    for t in ("problems", "testcases", "submissions", "submission_cases", "mastery"):
        n = (db.query_one("SELECT COUNT(*) AS n FROM %s" % t) or {}).get("n", 0)
        print("  %-18s %d" % (t, n))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
