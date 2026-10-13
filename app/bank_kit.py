"""题库构造小工具：把理论题（选择 / 判断 / 填空）的样板代码收拢到一处。

为什么需要
----------
课程里有一大批「考概念」的题（Linux 命令、数据结构性质判断……），
它们和编程题共用同一套「测试点 + 分值 + 提交历史 + 进度」模型，
但**出题时的写法**差别很大：编程题要写用例输入/输出，理论题只要一个答案。

如果每道理论题都手写一遍 `line / checker / cases / reference_solution`，
不但啰嗦，还极容易漏字段（漏 `checker` 就会被按 standard 口径比，
一旦答案不是一个干净的字母就永远判不过）。所以统一在这里生成。

约定
----
- 理论题的期望值一律写成 `|答案`（多行 = 多个可接受答案），配合 `oneof` checker
- 理论题的用例 `is_sample` **必须是 0**：样例会在静态站里公开，
  对选择题来说那就是把答案直接印在题面上
- `reference_solution` 就填答案本身 —— 这样 `verify_bank.py` 能像跑编程题
  一样把它跑一遍做自检，不需要为理论题单开一条校验链路
"""
from __future__ import annotations

# 判断题的两个规范答案（runner_text 会把 正确/√/T 之类收成「对」）
TRUE = "对"
FALSE = "错"

# 理论题默认分值
SCORE_CHOICE = 10      # 单选
SCORE_JUDGE = 8        # 判断
SCORE_FILL = 12        # 填空


def _oneof(alts: list[str]) -> tuple[str, str]:
    """把若干可接受答案拼成期望值 + 挑一个当参考解。"""
    clean = [str(a).strip() for a in alts if str(a).strip()]
    if not clean:
        raise ValueError("题目没有可接受答案")
    expected = "\n".join("|" + a for a in clean) + "\n"
    return expected, clean[0]


def _theory(*, title: str, subject: str, section: str, statement_md: str,
            answers: list[str], explanation: str, tags: list[str],
            difficulty: int, total_score: int, choices: list[str] | None = None,
            input_format: str = "", output_format: str = "",
            constraints_md: str = "", tip: str = "") -> dict:
    """理论题的公共骨架。"""
    expected, ref = _oneof(answers)
    stmt = statement_md
    if tip:
        stmt = stmt.rstrip() + "\n\n" + tip
    return {
        "title": title,
        "subject": subject,
        "line": "text",
        "difficulty": difficulty,
        "total_score": total_score,
        "tags": tags,
        "choices": choices or [],
        "source_section": section,
        "statement_md": stmt,
        "input_format": input_format,
        "output_format": output_format,
        "constraints_md": constraints_md,
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": ref,
        # 一个测试点 = 整个答案；is_sample 恒为 0（见模块 docstring）
        "cases": [{
            "stdin": "",
            "expected_stdout": expected,
            "is_sample": 0,
            "kind": "manual",
            "explanation": explanation,
        }],
    }


def mc(title: str, statement_md: str, options: list[str], answer: str, *,
       subject: str, section: str, explanation: str, tags: list[str],
       difficulty: int = 1, total_score: int = SCORE_CHOICE,
       answer_note: str = "") -> dict:
    """单选题。

    `options` 只写选项正文（不写 `A.` 前缀，界面自己编号）；
    `answer` 写选项字母（`"B"`）。
    """
    letters = "ABCDEFGH"
    if len(options) < 2 or len(options) > len(letters):
        raise ValueError("单选题需要 2~8 个选项")
    if answer.strip().upper() not in letters[:len(options)]:
        raise ValueError(f"答案 {answer!r} 不在选项范围里")
    return _theory(
        title=title, subject=subject, section=section,
        statement_md=statement_md, answers=[answer.strip().upper()],
        explanation=explanation, tags=tags, difficulty=difficulty,
        total_score=total_score, choices=options,
        output_format="一个选项字母（`A`~`%s`）" % letters[len(options) - 1],
        tip=answer_note)


def tf(title: str, statement_md: str, answer: bool, *,
       subject: str, section: str, explanation: str, tags: list[str],
       difficulty: int = 1, total_score: int = SCORE_JUDGE) -> dict:
    """判断题。`answer=True` 表示「对」。"""
    return _theory(
        title=title, subject=subject, section=section,
        statement_md=statement_md,
        # 「对/错」的常见等价写法都收进来，免得学生写「正确」被判错
        answers=[TRUE, "正确", "√", "T"] if answer else [FALSE, "错误", "×", "F"],
        explanation=explanation, tags=tags, difficulty=difficulty,
        total_score=total_score, choices=[TRUE, FALSE],
        output_format="`对` 或 `错`（写 `正确`/`√`/`T` 也认）")


def fill(title: str, statement_md: str, answers: list[str], *,
         subject: str, section: str, explanation: str, tags: list[str],
         difficulty: int = 2, total_score: int = SCORE_FILL,
         hint: str = "", input_format: str = "") -> dict:
    """填空题 / 命令题。

    `answers` 列出**全部可接受写法** —— 只收语义等价、形式也固定的那些
    （例如 `ls -a /` 与 `ls -la /`）。比较按 `token` 口径：空格多少无所谓，
    大小写与参数顺序有关系（那就多种写法都列上）。
    """
    return _theory(
        title=title, subject=subject, section=section,
        statement_md=statement_md, answers=answers,
        explanation=explanation, tags=tags, difficulty=difficulty,
        total_score=total_score, input_format=input_format,
        output_format="一行答案（不要写解释、不要写命令提示符）",
        tip=hint)
