"""排序改造的回归自检：跑 `/api/problems` 的排序不能慢。

★ 为什么要单独守这一条：
  早期版本里 `_order_key()` 逐题调用 `_section_ranks()`，
  而后者每次调用都要打两次库 —— 1440 道题 = 1440 × 2 次 SQL，
  实测把接口从 **0.4 秒拖到 64 秒**（浏览器直接白屏超时）。
  这种坑从代码上看不出来（逻辑完全正确），只能靠计时守住。

跑法：
    python tools/selftest_sort_order.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import db                                    # noqa: E402
from app.api.problems import _order_key, _section_ranks   # noqa: E402
from app.section_order import build_ranks, ranks_from_db  # noqa: E402

#: 单题排序键允许的上限（秒）。实测正常是 0.001 秒级，
#: 出事是 60 秒级 —— 阈值取 2 秒既能抓住退化，又不会因慢机器误报。
BUDGET_PER_QUESTION = 2.0
#: 整库排一次的上限（秒）。正常 0.4 秒以内。
BUDGET_FULL_SORT = 8.0

fails: list[str] = []


def ok(name: str, cond: bool, extra: str = "") -> None:
    if cond:
        print("  [PASS] " + name + ("  -- " + extra if extra else ""))
    else:
        print("  [FAIL] " + name + ("  -- " + extra if extra else ""))
        fails.append(name)


def main() -> int:
    db.init_db()
    rows = db.query("""
        SELECT id, subject, source_section, difficulty
        FROM problems WHERE status='published'
    """)
    n = len(rows)
    print("已发布题目 %d 道\n" % n)
    if n < 100:
        print("题库太小，跳过性能检查")
        return 0

    # ---- 1. 逐题调用排序键不能打库 ----
    ranks = _section_ranks()
    t0 = time.time()
    for r in rows:
        _order_key(r)              # 不传 ranks：走默认快取
    per_q = time.time() - t0
    ok("逐题调用 _order_key 不打库",
       per_q < BUDGET_PER_QUESTION,
       "%.3fs（阈值 %.1fs）" % (per_q, BUDGET_PER_QUESTION))

    # ---- 2. 整库排一次 ----
    t0 = time.time()
    ordered = sorted(rows, key=lambda r: _order_key(r, ranks))
    full = time.time() - t0
    ok("整库排序在预算内", full < BUDGET_FULL_SORT,
       "%.3fs（阈值 %.1fs）" % (full, BUDGET_FULL_SORT))

    # ---- 3. 排序结果：科目 → 分节路径 → 难度 → id ----
    key = lambda r: _order_key(r, ranks)          # noqa: E731
    ok("排序结果与键完全一致",
       [r["id"] for r in ordered] == [r["id"] for r in sorted(rows, key=key)])

    subjects = [r["id"] for r in ordered]
    sub_seq = [r["subject"] for r in ordered]
    order_map = {"python": 0, "ds": 1, "cpp": 2, "linux": 3}
    sub_nums = [order_map.get(s, 9) for s in sub_seq]
    ok("科目按展示顺序排列",
       all(sub_nums[i] <= sub_nums[i + 1] for i in range(len(sub_nums) - 1)),
       str(sorted(set(sub_seq))))

    # 分节在科目内连续，且序号不倒退
    sec_seq = [(r["subject"], r["source_section"]) for r in ordered]
    contiguous = True
    seen: set = set()
    prev = None
    for s in sec_seq:
        if s != prev:
            if s in seen:
                contiguous = False
                break
            seen.add(s)
            prev = s
    ok("同一分节的题目连续排列", contiguous)

    # 组内难度升序
    bad = []
    cur = None
    seq: list[int] = []
    for r in ordered:
        k = (r["subject"], r["source_section"])
        if k != cur:
            if cur is not None and any(seq[i] > seq[i + 1] for i in range(len(seq) - 1)):
                bad.append(cur)
            cur, seq = k, []
        seq.append(int(r["difficulty"] or 1))
    if cur is not None and any(seq[i] > seq[i + 1] for i in range(len(seq) - 1)):
        bad.append(cur)
    ok("每个分节内难度升序", not bad, str(bad[:3]))

    # ---- 4. 序号表覆盖全部在库分节 ----
    payload = ranks_from_db()
    live = {(r["subject"] or "python", r["source_section"] or "") for r in rows}
    known = {(s, sec) for s, d in payload.items() for sec in d}
    ok("序号表覆盖全部分节", not (live - known),
       str(list(live - known)[:3]))

    # ---- 5. 序号表与 build_ranks 一致 ----
    stats: dict = {}
    for r in rows:
        stats.setdefault((r["subject"] or "python", r["source_section"] or ""), []).append(
            int(r["difficulty"] or 1))
    avg = {k: sum(v) / len(v) for k, v in stats.items()}
    manual = build_ranks(live, avg)
    diff = [k for k in live if manual.get(k) != payload.get(k[0], {}).get(k[1])]
    ok("序号表与 build_ranks 结果一致", not diff, str(diff[:3]))

    print()
    if fails:
        print("❌ 失败 %d 项：%s" % (len(fails), "; ".join(fails)))
        return 1
    print("✅ 排序自检全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
