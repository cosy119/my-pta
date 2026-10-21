"""校验「题型顺序」前后端一致。

题型顺序 = **作答难度顺序**（由易到难）：判断 → 单选 → 多选 → 填空 → 简答 → 实操 → 编程。

单一数据源是 `app/question_types.py::LABELS`（dict 的插入顺序）。
前端 `web/index.html` 里有一份 `QUESTION_TYPES` 常量 —— 静态站没有后端，
前端那份是它唯一能拿到的顺序，所以两边必须逐字一致。

跑法：
    python tools/check_question_type_order.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.question_types import LABELS                       # noqa: E402

FRONTEND = ROOT / "web" / "index.html"

# 前端常量里的顺序
_FRONT_RE = re.compile(
    r"const\s+QUESTION_TYPES\s*=\s*\[(.*?)\];", re.S)
_ITEM_RE = re.compile(r"\{\s*k:\s*'([^']+)'\s*,\s*label:\s*'([^']+)'\s*\}")


def frontend_order() -> list[tuple[str, str]]:
    text = FRONTEND.read_text(encoding="utf-8")
    m = _FRONT_RE.search(text)
    if not m:
        raise SystemExit("✗ 前端里找不到 QUESTION_TYPES 常量")
    return _ITEM_RE.findall(m.group(1))


def main() -> int:
    back = list(LABELS.items())
    front = frontend_order()

    print("后端 app/question_types.py::LABELS")
    for i, (k, v) in enumerate(back, 1):
        print("   %d. %-16s %s" % (i, k, v))
    print()
    print("前端 web/index.html::QUESTION_TYPES")
    for i, (k, v) in enumerate(front, 1):
        print("   %d. %-16s %s" % (i, k, v))
    print()

    bad = []
    if [k for k, _ in back] != [k for k, _ in front]:
        bad.append("键顺序不一致：后端 %s / 前端 %s"
                   % ([k for k, _ in back], [k for k, _ in front]))
    for (kb, vb), (kf, vf) in zip(back, front):
        if kb != kf or vb != vf:
            bad.append("%s→%s 与 %s→%s 不一致" % (kb, vb, kf, vf))

    # 顺序必须是「由易到难」的固定梯度
    EXPECT = ["true_false", "single_choice", "multiple_choice",
              "fill_blank", "short_answer", "practical", "programming"]
    if [k for k, _ in back] != EXPECT:
        bad.append("后端顺序不是约定的难度梯度：%s（应为 %s）"
                   % ([k for k, _ in back], EXPECT))

    if bad:
        print("❌ 题型顺序不一致：")
        for b in bad:
            print("   -", b)
        return 1
    print("✅ 前后端题型顺序一致（7 种，由易到难）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
