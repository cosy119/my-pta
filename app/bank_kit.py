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
SCORE_MULTI = 14       # 多选（要对若干个，比单选难，分值给高一点）
SCORE_JUDGE = 8        # 判断
SCORE_FILL = 12        # 填空
SCORE_PRACTICAL = 25   # 实操（要真把一套操作做完，才拿得到那段输出）


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
            constraints_md: str = "", tip: str = "",
            question_type: str = "fill_blank") -> dict:
    """理论题的公共骨架。"""
    expected, ref = _oneof(answers)
    stmt = statement_md
    if tip:
        stmt = stmt.rstrip() + "\n\n" + tip
    return {
        "title": title,
        "subject": subject,
        "line": "text",
        "question_type": question_type,
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
        question_type="single_choice",
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
        question_type="true_false",
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


def multi(title: str, statement_md: str, options: list[str], answers: list[str], *,
          subject: str, section: str, explanation: str, tags: list[str],
          difficulty: int = 3, total_score: int = SCORE_MULTI,
          answer_note: str = "") -> dict:
    """多选题。

    `answers` 写**全部正确选项**的字母（例：`["A", "C"]`），至少两个。
    入库时按字母升序收成一个串（`"AC"`）—— 网页端是多选点选，
    取出来的字母天然按选项顺序排好，所以「升序」就是它的标准形式。

    ★ 为什么还要把**排列**也列成可接受答案
      点选界面写不出 `CA` 这种顺序，但 API 直接提交、或者以后做别的客户端时
      写反了就白判一次 WA。字母数 ≤ 3 时全排列最多 6 种，代价很小，就都收进来；
      再多就不列了（4 个字母 24 种，会把「可接受答案」提示刷屏，
      那种情况下题干里会明写「按字母升序」）。
    """
    letters = "ABCDEFGH"
    if len(options) < 3:
        raise ValueError("多选题至少要 3 个选项（2 个选项的多选没有区分度）")
    if len(options) > len(letters):
        raise ValueError("多选题最多 8 个选项")
    picked = {a.strip().upper() for a in answers}
    if len(picked) < 2:
        raise ValueError("多选题至少要 2 个正确答案")
    for a in picked:
        if a not in letters[:len(options)]:
            raise ValueError(f"答案 {a!r} 不在选项范围里")
    key = "".join(sorted(picked))
    alts = [key]
    if len(key) <= 3:
        from itertools import permutations
        alts += ["".join(p) for p in sorted(permutations(key)) if "".join(p) != key]
    return _theory(
        title=title, subject=subject, section=section,
        statement_md=statement_md, answers=alts,
        explanation=explanation, tags=tags, difficulty=difficulty,
        total_score=total_score, choices=options,
        question_type="multiple_choice",
        output_format="若干个选项字母，按字母升序连写（如 `AC`）",
        tip=answer_note or "**多选题**：正确选项不止一个，点选切换，再次点击可取消。")


def practical(title: str, statement_md: str, outputs: list[str], *,
              verify_cmd: str, subject: str, section: str,
              explanation: str, tags: list[str],
              difficulty: int = 4, total_score: int = SCORE_PRACTICAL,
              hint: str = "") -> dict:
    """实操题：多步任务 + **一条验收命令**，提交命令的真实输出。

    为什么做成「提交输出」而不是「提交命令」
    ----------------------------------------
    课程实验（装系统、建用户、改权限、打包解压……）在平台里没法替你执行，
    但**做完之后那台机器的状态是可以自证的**：`stat -c '%a'` 出来的 751、
    `readlink /myshare` 出来的 `/usr/local/sdutshare`、`sort -r` 出来的顺序，
    都不是靠猜能编出来的（或者至少得真算一遍）。

    所以这里的口径是：
    - 题干给完整任务清单（照实验指导书，步骤编号保留）
    - 附一条**验收命令** —— 输出短、且与机器无关（不含时间戳 / 主机名 / 内核版本）
    - 学生把那条命令的**输出**贴回来，不是命令本身

    ★ 期望值仍然走 `oneof`（多行 = 多个可接受写法）。
      把「几种都对的写法」列全，是这类题唯一的宽容口子：
      比如软链目标写绝对路径还是相对路径、tar 用绝对路径打包会不会多一层 `usr/`。

    ★ 一道题只能有**一个测试点**。原因在 `runner_text`：它把**同一份提交**
      当作每个测试点的 stdout —— 两个期望值不同的点，参考答案必然只能过一个。
    """
    tip = ("**验收（先在机器上把任务做完，再把输出贴回来）**\n\n"
           "```bash\n%s\n```\n" % verify_cmd)
    if hint:
        tip += "\n" + hint
    # ★ 多行输出必须压成一行再交给 oneof。
    #   期望值的格式是「**一行一个**可接受答案，行首加 `|`」——
    #   答案自身带换行的话，从第二行起会被当成「另一个答案」，题目必然判不过。
    #   压平不会让判题变宽松：两边最终都要过 compare._squeeze_ws，
    #   换行和空格在那里本来就是一回事。
    flat = [" ".join(str(x).split()) for x in outputs]
    return _theory(
        title=title, subject=subject, section=section,
        statement_md=statement_md, answers=flat,
        explanation=explanation, tags=tags, difficulty=difficulty,
        total_score=total_score,
        question_type="practical",
        input_format="只贴验收命令跑出来的**输出**，不要贴命令本身",
        output_format="验收命令的输出（可以多行，原样贴）",
        tip=tip)
