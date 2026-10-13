"""评分：测试点分值分配与计分。

对齐 PTA 的评分模型：

- 一道题由若干**测试点**（testcase）组成，每个测试点**单独带分值**
- 一次提交的得分 = **通过的测试点分值之和**，不是「通过了几个」
- 满分 = 所有测试点分值之和
- 拿到分但没拿满 = **部分正确**（PTA 里就是这么显示的）

设计上把「分值」和「判定」彻底分开：
判定只看单个测试点对不对（compare），分值只由 scoring 算。
这样以后要换成「一组测试点全过才给分」之类的规则，也只改这里。
"""
from __future__ import annotations

from typing import Iterable, Sequence


def distribute_points(total_score: int, n: int) -> list[int]:
    """把 total_score 尽量平均地分给 n 个测试点，**余数分给前面的**。

    例：
        100 分 5 个点 → [20, 20, 20, 20, 20]
        100 分 6 个点 → [17, 17, 17, 17, 16, 16]
         10 分 3 个点 → [4, 3, 3]
          0 分 3 个点 → [0, 0, 0]
    """
    total_score = int(total_score or 0)
    n = int(n or 0)
    if n <= 0:
        return []
    if total_score <= 0:
        return [0] * n
    base, rem = divmod(total_score, n)
    return [base + (1 if i < rem else 0) for i in range(n)]


def normalize_points(raw_points: Iterable[int], total_score: int) -> list[int]:
    """把库里存的 points 规范化成一份可靠的分值表。

    - 全为 0（老数据、或建题时没写分值）→ 按 total_score 均分兜底
    - 有任何一个是正数 → 原样采用（负数 / None 当 0）
    """
    vals = [max(0, int(p or 0)) for p in raw_points]
    if not vals:
        return []
    if sum(vals) == 0:
        return distribute_points(total_score, len(vals))
    return vals


def grade(raw_points: Sequence[int], verdicts: Sequence[str],
          total_score: int) -> dict:
    """算一次提交的得分。

    参数
    ----
    raw_points  : 每个测试点的分值（库里读出来的，可能全是 0）
    verdicts    : 每个测试点的判定（只有 AC 拿分）
    total_score : 题目满分（points 全为 0 时用来兜底）

    返回
    ----
    dict(points=..., earned=..., score=..., max_score=...)
        points    逐点分值（列表）
        earned    逐点实得（列表）
        score     本次得分
        max_score 满分
    """
    pts = normalize_points(raw_points, total_score)

    # 长度不一致时按短的算 —— 宁可少算，也不要静默错位
    n = min(len(pts), len(verdicts))
    earned = [(pts[i] if verdicts[i] == "AC" else 0) for i in range(n)]
    if len(pts) > n:                       # 多出来的点没判定，不给分
        earned.extend([0] * (len(pts) - n))

    return {
        "points": pts,
        "earned": earned,
        "score": int(sum(earned)),
        "max_score": int(sum(pts)),
    }


def is_partial(score: int, max_score: int) -> bool:
    """部分正确：拿到分，但没拿满。"""
    return 0 < int(score) < int(max_score or 0)


def verdict_label(verdict: str, score: int, max_score: int) -> str:
    """给前端用的一行中文状态（PTA 的显示口径）。"""
    if verdict == "AC":
        return "答案正确"
    if is_partial(score, max_score):
        return "部分正确"
    return {
        "WA": "答案错误", "PE": "格式错误", "TLE": "运行超时",
        "MLE": "内存超限", "RE": "运行时错误", "CE": "编译错误",
        "OLE": "输出超限", "IE": "判题器错误",
        "pending": "排队中", "judging": "判题中",
    }.get(verdict, verdict)
