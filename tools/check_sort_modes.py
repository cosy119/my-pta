"""排序方式（按章节 / 按难度）的回归自检。

守四件事：
  1. 前端 `web/index.html::SORT_MODES` 的 key 是后端 `SORT_MODES` 的子集
     —— 两边对不上，用户点了前端选项、后端会 400。
  2. 默认排序方式仍是 `chapter`，且结果与改造前的 `_order_key` **逐条一致**
     —— 「按章节」是既有行为，不能被这次改动悄悄改掉。
  3. `difficulty` / `difficulty_desc` 的难度单调性正确。
  4. 同难度内的次序 = 章节序（教学路径 → id），三种模式都**不丢题、不重复**。

跑法：
    python tools/check_sort_modes.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import db                                              # noqa: E402
from app.api.problems import (DEFAULT_SORT, SORT_MODES, _order_key,   # noqa: E402
                              _section_ranks, _sort_key)

WEB = ROOT / "web" / "index.html"

fails: list[str] = []


def ok(name: str, cond: bool, extra: str = "") -> None:
    if cond:
        print("  [PASS] " + name + ("  -- " + extra if extra else ""))
    else:
        print("  [FAIL] " + name + ("  -- " + extra if extra else ""))
        fails.append(name)


def frontend_sort_keys() -> list[str]:
    """从 web/index.html 里抠出 `SORT_MODES` 数组的 key。

    ★ 不要用 `import` 或执行 JS —— 这是个纯静态校验，正则足够且不会误伤。
      抠不到就返回空列表，让断言直接失败（比静默通过好）。
    """
    src = WEB.read_text(encoding="utf-8")
    m = re.search(r"const SORT_MODES = \[(.*?)\];", src, re.S)
    if not m:
        return []
    return re.findall(r"k:\s*'([^']+)'", m.group(1))


def difficulty_seq(rows: list[dict]) -> list[int]:
    return [int(r.get("difficulty") or 1) for r in rows]


def monotone(seq: list[int], desc: bool = False) -> bool:
    if desc:
        return all(seq[i] >= seq[i + 1] for i in range(len(seq) - 1))
    return all(seq[i] <= seq[i + 1] for i in range(len(seq) - 1))


def main() -> int:
    db.init_db()

    # ---- 0. 纯静态部分：前后端排序方式对齐（不需要题库，CI 里一定能跑）----
    fe = frontend_sort_keys()
    print("前端 SORT_MODES: %s" % (fe or "（没抠到！）"))
    print("后端 SORT_MODES: %s\n" % (list(SORT_MODES),))
    ok("前端排序方式非空（正则没失配）", bool(fe))
    ok("前端 key 都在后端白名单里", bool(fe) and set(fe) <= set(SORT_MODES),
       "多出来的：%s" % sorted(set(fe) - set(SORT_MODES)))
    ok("默认排序方式是 chapter", DEFAULT_SORT == "chapter", DEFAULT_SORT)

    rows = db.query("""
        SELECT id, subject, source_section, difficulty
        FROM problems WHERE status='published'
    """)
    print("\n已发布题目 %d 道" % len(rows))
    if not rows:
        # ★ 沿用 selftest_sort_order.py 的约定：库没 seed 就跳过排序语义检查，
        #   不要让 CI 因为「忘了 seed」红掉 —— 静态那几条已经守住了关键约束。
        print("题库是空的（未 seed），跳过排序语义检查")
        print()
        if fails:
            print("❌ 失败 %d 项：%s" % (len(fails), "; ".join(fails)))
            return 1
        print("✅ 排序方式静态检查通过（排序语义未验）")
        return 0
    ranks = _section_ranks()

    # ---- 2. 默认（chapter）必须与改造前逐条一致 ----
    legacy = [r["id"] for r in sorted(rows, key=lambda r: _order_key(r, ranks))]
    now = [r["id"] for r in sorted(rows, key=lambda r: _sort_key(r, ranks))]
    ok("默认排序 == 改造前 _order_key（逐条 id 一致）", legacy == now,
       "差异 %d 条" % sum(1 for a, b in zip(legacy, now) if a != b))
    ok("显式 sort=chapter == 不传 sort",
       now == [r["id"] for r in sorted(rows, key=lambda r: _sort_key(r, ranks, "chapter"))])

    # ---- 3. 各模式的难度单调性（★ 分科目内，跨科目不混排）----
    #   排序键是「科目 → 难度 → …」，所以整表看难度并不是全局单调的
    #   （python 的难度 3 排在 cpp 的难度 1 前面是正常的）。
    print()
    for mode, desc in (("difficulty", False), ("difficulty_desc", True)):
        ordered = sorted(rows, key=lambda r: _sort_key(r, ranks, mode))
        bad_subj = []
        for subj in {r["subject"] for r in ordered}:
            seq = difficulty_seq([r for r in ordered if r["subject"] == subj])
            if not monotone(seq, desc):
                bad_subj.append(subj)
        seq_all = difficulty_seq(ordered)
        ok("%s 各科目内难度%s" % (mode, "不增" if desc else "不减"), not bad_subj,
           "违规科目 %s｜全局区间 %d~%d" % (bad_subj, min(seq_all), max(seq_all)))

        # 科目自身也不能被打散
        sub_seq = [r["subject"] for r in ordered]
        blocks = 1 + sum(1 for i in range(len(sub_seq) - 1) if sub_seq[i] != sub_seq[i + 1])
        ok("%s 科目不被打散（连续块数 = 科目数）" % mode,
           blocks == len(set(sub_seq)), "%d 块" % blocks)

        # 同难度内必须是章节序（教学路径 → id），不是原始录入序
        bad = 0
        prev_d, group = None, []

        def flush(g: list[dict]) -> int:
            keys = [(_order_key(r, ranks)[1], r["id"]) for r in g]
            return 0 if keys == sorted(keys) else 1

        for r in ordered:
            d = int(r.get("difficulty") or 1)
            if d != prev_d:
                if group:
                    bad += flush(group)
                group, prev_d = [], d
            group.append(r)
        if group:
            bad += flush(group)
        ok("%s 同难度内按章节序" % mode, bad == 0, "违规 %d 段" % bad)

    # ---- 4. 三种模式互不丢题 ----
    print()
    base = sorted(r["id"] for r in rows)
    allsame = True
    for mode in SORT_MODES:
        got = sorted(r["id"] for r in sorted(rows, key=lambda r: _sort_key(r, ranks, mode)))
        if got != base:
            allsame = False
            print("    %s 丢题/重复：%d vs %d" % (mode, len(got), len(base)))
    ok("三种排序模式题目集合完全相同（不丢不重）", allsame)

    # ---- 5. 未知模式落到默认（不炸）----
    unknown = sorted(rows, key=lambda r: _sort_key(r, ranks, "no_such_mode"))
    ok("未知模式回落章节序（_sort_key 层兜底）", [r["id"] for r in unknown] == legacy)

    print()
    if fails:
        print("❌ 失败 %d 项：%s" % (len(fails), "; ".join(fails)))
        return 1
    print("✅ 排序方式自检全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
