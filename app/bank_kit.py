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

import re

# 判断题的两个规范答案（runner_text 会把 正确/√/T 之类收成「对」）
TRUE = "对"
FALSE = "错"

# 理论题默认分值
SCORE_CHOICE = 10      # 单选
SCORE_MULTI = 14       # 多选（要对若干个，比单选难，分值给高一点）
SCORE_JUDGE = 8        # 判断
SCORE_FILL = 12        # 填空
SCORE_PRACTICAL = 25   # 实操类实验（多步任务，一步做错整题就废）
SCORE_COMMAND = 12     # 单条命令题（写一条命令解决一个场景）


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


# 单/双引号包住、且里面**不含空白**的片段。
# 只对这种片段做「去引号 / 换引号」扩展 —— 带空格的引号一去掉语义就变了
# （`echo "a b"` 与 `echo a b` 参数个数都不一样），绝不能碰。
_QUOTED_RE = re.compile(r"""(['"])([^\s'"]+)\1""")


def _quote_forms(ans: str) -> list[str]:
    """同一条命令的引号变体：`find . -name '*.log'` → 也认 `*.log` / `"*.log"`。

    为什么值得宽容
    --------------
    「要不要加引号」是手打命令时最容易两边不一的地方：答案里写了 `'*.log'`，
    学生不打引号照样能跑（当前目录没有匹配文件时），判错纯属刁难。
    `compare._norm_cmd` 只管空白与短选项，管不到引号，所以在这一层补。

    ★ 硬约束：引号内出现空白就**一律不动** —— 那种情况下引号是语义的一部分。
    """
    out = [ans]
    for m in _QUOTED_RE.finditer(ans):
        other = '"' if m.group(1) == "'" else "'"
        out.append(ans.replace(m.group(0), m.group(2)))                 # 去引号
        out.append(ans.replace(m.group(0), other + m.group(2) + other))  # 换引号
    seen: set[str] = set()
    uniq: list[str] = []
    for v in out:
        if v not in seen:
            seen.add(v)
            uniq.append(v)
    return uniq


def practical(title: str, statement_md: str, answers: list[str], *,
              subject: str, section: str, explanation: str, tags: list[str],
              difficulty: int = 3, total_score: int = SCORE_COMMAND,
              hint: str = "", input_format: str = "") -> dict:
    """实操题 / 命令题：**给场景，写出命令本身**。

    形态为什么改过（2026-10-19）
    ----------------------------
    早先的版本是「多步任务 + 附一条验收命令 → 提交那条命令的**输出**」。
    能跑，但考错了东西：学生把实验做完，答案就是屏幕上复制一段文字，
    **到底会不会写命令完全没被考察** —— 写不出命令的人照样拿分，
    背下 `VERSION_ID=44` 的人甚至不用碰机器。

    现在改成：题干给场景与约束，提交**命令本身**。
    - 会写就写得出，不会写就是不会 —— 这才是命令题该考的东西
    - 平台不执行提交内容（云端跑任意 shell 是 RCE），只做**文本等价比对**，
      宽容度全压在 `app/judge/compare.py`：
      空白折叠、`-l -a` ≡ `-la`、`-la` ≡ `-al`（短选项簇内排序去重）、
      `/home/<谁>` ≡ `~`，加上这里再补的**引号变体**。

    ★ `answers` 要列全「语义等价但形式不同」的写法。
      自动归一化兜得住形式抖动，兜不住真正的两套写法 ——
      `chmod 751 f` 与 `chmod u=rwx,g=rx,o=x f` 得手工都列上。
    ★ 一道题仍然只能有**一个测试点**：`runner_text` 把同一份提交
      当作每个测试点的 stdout，两个不同期望值必然只能过一个。
    """
    flat = [" ".join(str(x).split()) for x in answers]
    alts: list[str] = []
    for a in flat:
        alts.extend(_quote_forms(a))
        # ★ 单字母命令（`w`）要额外补一个大写形式：
        #   runner_text.normalize_answer 把「单个 ASCII 字母」当成选项字母转成大写，
        #   于是学生写 `w` 会被判成 `W`。这不是 bug（选择题就靠它），
        #   但命令题里得补上 `W` 这条备选，否则 `w` 永远判不过自己。
        if len(a) == 1 and a.isascii() and a.isalpha():
            alts.append(a.upper())
    return _theory(
        title=title, subject=subject, section=section,
        statement_md=statement_md, answers=alts,
        explanation=explanation, tags=tags, difficulty=difficulty,
        total_score=total_score,
        question_type="practical",
        input_format=input_format or
        "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        output_format="一整条命令",
        tip=hint)
