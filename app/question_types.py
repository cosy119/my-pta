"""题型是题目的显式元数据，不等同于提交语言 ``line``。

老题没有 question_type 时按已有选项和提交方式补齐；新题可以显式指定。
推断只用于兼容旧数据，不能凭答案长短猜测「简答」或「实操」。
"""
from __future__ import annotations

import json
import re
from typing import Any, Mapping


#: 题型标签。**dict 的插入顺序 = 前端展示顺序 = 作答难度顺序**（由易到难）：
#: 判断 → 单选 → 多选 → 填空 → 简答 → 实操 → 编程。
#: 前端 `web/index.html` 的 `QUESTION_TYPES` 必须与本处保持一致
#: （`tools/check_question_type_order.py` 会校验）。
LABELS = {
    "true_false": "判断题",
    "single_choice": "单选题",
    "multiple_choice": "多选题",
    "fill_blank": "填空题",
    "short_answer": "简答题",
    "practical": "实操题",
    "programming": "编程题",
}


def _choices(value: Any) -> list:
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            return parsed if isinstance(parsed, list) else []
        except ValueError:
            return []
    return []


def infer(problem: Mapping[str, Any]) -> str:
    """只根据可靠的已有字段归类；已有显式题型优先。"""
    explicit = str(problem.get("question_type") or "").strip()
    if explicit:
        if explicit not in LABELS:
            raise ValueError("未知题型：%s" % explicit)
        return explicit
    if str(problem.get("line") or "python") != "text":
        return "programming"
    choices = _choices(problem.get("choices"))
    if len(choices) == 2 and set(choices) == {"对", "错"}:
        return "true_false"
    if choices:
        # 旧题只写字母答案；多选如 AC/BD 才明确识别为多选。
        answer = str(problem.get("reference_solution") or "").strip().upper()
        if re.fullmatch(r"[A-H]{2,}", answer):
            return "multiple_choice"
        return "single_choice"
    # 现有 Linux 命令题只是输入文本并比对，未真正执行命令，归填空。
    return "fill_blank"
