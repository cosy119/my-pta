"""把题库模块里的**测试点**同步到库里已有的题（只改不增）。

为什么需要这个工具
------------------
`seed.ensure()` 只做一件事：**按标题判重，没有就插入**。
标题已经存在的题直接 `continue` —— 所以「改了一道老题的答案」之后，
库里躺着的还是旧答案。而 `verify_bank.py` / `export_static.py` 读的是**库**，
不是题库模块，于是你改了模块、跑了全量检查、结论全绿，导出的却还是旧数据。

这个坑已经踩过两次（改题库 → 库里没变 → 导出对不上）。
所以单独做一个同步动作，让它显式、可复查。

用法
----
    python tools/sync_bank_cases.py --subject linux --title "某道题" --title "另一道"
    python tools/sync_bank_cases.py --subject linux --title "某道题" --apply

★ 默认**只打印不写库**；必须显式 `--apply`。
★ 必须用 `--title` **点名**要同步的题 —— 故意不提供「整条线一把梭」。

★★ 为什么不做批量：库里有些题的答案**比题库模块多**，那是
   `seed.backfill_choice_alts()` 干的活（把选择题的选项正文也补成可接受答案）。
   整条线覆盖过去会把这些补充答案冲掉，而且不报错 —— 只是悄悄变回窄口径。
   所以这个工具的定位是「我刚改过这几道，把它们推到库里」，不是同步器。

它同步三样东西：`expected_stdout` / `explanation` / `is_sample`。
分值（`points`）**不动**：那是 `backfill_legacy_scores()` 的活，
在这里改会和它打架。测试点数量对不上时直接报出来、跳过那道题，不硬塞。
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

import _console                                              # noqa: E402
from app import db                                           # noqa: E402
from app.seed import SEED_PROBLEMS                            # noqa: E402


def sync(subject: str, titles: list[str], apply: bool) -> int:
    db.init_db()
    want_titles = set(titles)
    changed_titles: list[str] = []
    skipped: list[str] = []
    hit: set[str] = set()

    for spec in SEED_PROBLEMS:
        if spec["title"] not in want_titles:
            continue
        hit.add(spec["title"])
        if (spec.get("subject") or "python") != subject:
            skipped.append("%s（不是 %s 线的题）" % (spec["title"], subject))
            continue
        row = db.query_one("SELECT id FROM problems WHERE title = ?", (spec["title"],))
        if not row:
            skipped.append("%s（库里没有）" % spec["title"])
            continue

        want = spec.get("cases") or []
        have = db.query(
            "SELECT id, ord, expected_stdout, explanation, is_sample "
            "FROM testcases WHERE problem_id = ? ORDER BY ord, id", (row["id"],))
        if len(want) != len(have):
            skipped.append("%s（测试点数 %d ≠ 库 %d）" % (spec["title"], len(want), len(have)))
            continue

        dirty = False
        for i, (w, h) in enumerate(zip(want, have)):
            exp = w.get("expected_stdout", "") or ""
            dsc = w.get("explanation", "") or ""
            smp = int(w.get("is_sample") or 0)
            if (h["expected_stdout"] or "") == exp and (h["explanation"] or "") == dsc \
                    and int(h["is_sample"] or 0) == smp:
                continue
            dirty = True
            print("  · %s  [测试点 %d]" % (spec["title"], i))
            if (h["expected_stdout"] or "") != exp:
                print("      期望值 旧: %r" % (h["expected_stdout"] or "")[:120])
                print("             新: %r" % exp[:120])
            if apply:
                db.execute("UPDATE testcases SET expected_stdout=?, explanation=?, is_sample=? "
                           "WHERE id=?", (exp, dsc, smp, h["id"]))
        if dirty:
            changed_titles.append(spec["title"])

    miss = want_titles - hit
    print()
    print("%s：%d 道题的测试点有变化%s"
          % (subject, len(changed_titles),
             "" if apply else "（只预览，没写库 —— 加 --apply 才真写）"))
    if miss:
        print("题库里找不到这几道（标题要一模一样）：")
        for m in sorted(miss):
            print("  -", m)
    if skipped:
        print("跳过 %d 道：" % len(skipped))
        for s in skipped[:8]:
            print("  -", s)
    return len(changed_titles)


def main() -> int:
    ap = argparse.ArgumentParser(description="把题库模块的测试点同步进库（只点名，不批量）")
    ap.add_argument("--subject", required=True, choices=("python", "ds", "linux"),
                    help="这条题属于哪条线（填错会跳过并提示）")
    ap.add_argument("--title", action="append", required=True,
                    help="要同步的题标题，可重复写多个（必须与题库逐字一致）")
    ap.add_argument("--apply", action="store_true", help="真写库（默认只预览）")
    args = ap.parse_args()
    n = sync(args.subject, args.title, args.apply)
    if args.apply:
        # ★ 同步会把库里「选项正文也算答案」的补充冲掉（题库模块里只有字母）。
        #   所以写完立刻补回来 —— backfill_choice_alts() 是幂等的，没有该补的就不动。
        from app import seed as _seed
        back = _seed.backfill_choice_alts()
        print("已重新补齐选择题的「选项正文」备选答案：%d 个测试点" % back)
    return 0 if n >= 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
