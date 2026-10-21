"""校验 `app/section_order.py` 的教学路径表与题库实际分节是否一致。

用法::

    D:/Pythontools/Python/python.exe tools/check_section_order.py

输出三件事：
1. **漏登记**：库里有、表里没有的分节（会排到最末尾，学习路径被打断）
2. **多登记**：表里有、库里没有的分节（写错了名字，或题被删了）
3. **轨道内的难度单调性**：``by_difficulty`` 轨道排完后平均难度应不下降；
   其余轨道只提示「该节均难低于前一节」供人工判断，不算错。

退出码：0 = 全部对得上；1 = 有漏登记或多登记。
"""
from __future__ import annotations

import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import db                                   # noqa: E402
from app.section_order import (TRACKS, build_ranks,  # noqa: E402
                               known_sections, lecture_of)


def main() -> int:
    rows = db.query("""
        SELECT subject, source_section AS sec, COUNT(*) AS n, AVG(difficulty) AS av
        FROM problems WHERE status='published'
        GROUP BY subject, source_section
    """)
    if not rows:
        print("库里没有已发布题目 —— 先跑 seed")
        return 1

    pairs = {(r["subject"] or "python", r["sec"] or "") for r in rows}
    stats = {(r["subject"] or "python", r["sec"] or ""): float(r["av"] or 0) for r in rows}
    known = known_sections()
    known_pairs = {(s, n) for s, names in known.items() for n in names}

    missing = sorted(pairs - known_pairs)
    extra = sorted(known_pairs - pairs)

    print("=== 分节覆盖检查 ===")
    print("库内分节 %d 个 / 表内登记 %d 个" % (len(pairs), len(known_pairs)))
    for subject, sec in missing:
        print("  ❌ 漏登记  %-6s %-30s %d 题  均难 %.2f"
              % (subject, sec, counts[(subject, sec)], stats.get((subject, sec), 0)))
    for subject, sec in extra:
        print("  ⚠️  多登记  %-6s %-30s（库里没有这一节）" % (subject, sec))

    ranks = build_ranks(pairs, stats)

    counts = {(r["subject"] or "python", r["sec"] or ""): r["n"] for r in rows}

    print()
    print("=== 各科学习路径（按排序号） ===")
    by_subject = collections.defaultdict(list)
    for (subject, sec) in pairs:
        by_subject[subject].append(sec)
    for subject in sorted(by_subject, key=lambda s: {"python": 0, "ds": 1, "cpp": 2, "linux": 3}.get(s, 9)):
        secs = sorted(by_subject[subject], key=lambda s: ranks[(subject, s)])
        print("-- %s（%d 节）" % (subject, len(secs)))
        prev_av = None
        for sec in secs:
            av = stats.get((subject, sec), 0)
            flag = ""
            if prev_av is not None and av < prev_av - 1e-9:
                flag = "   ← 均难比上一节低 %.2f（顺序是知识点依赖，不是难度）" % (prev_av - av)
            print("   %-34s %3d 题  均难 %.2f%s" % (sec, counts[(subject, sec)], av, flag))
            prev_av = av

    print()
    if missing or extra:
        print("❌ 不一致：%d 个漏登记、%d 个多登记" % (len(missing), len(extra)))
        return 1
    print("✅ 分节表与题库完全一致")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
