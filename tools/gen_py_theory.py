#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Python 线理论题库生成器（单选 / 多选 / 判断 / 填空 / 简答）。

    python tools/gen_py_theory.py [--check]

为什么要有一个生成器，而不是手写模块
------------------------------------
理论题最容易出的错不是「题不好」，而是**答案键写错**：选项排版时点错一个字母、
`-7 // 2` 记成 -3、`sort()` 以为返回列表。这类错 `verify_bank.py` 抓不到
（理论题没有第二套实现），只能靠人肉再看一遍——而人肉看第二遍同样会错。

所以这里的规矩是：**凡是能在本机跑出事实的题，答案一律由实跑结果反推**。

    code   一段真 Python 源码（**最后一行必须是表达式**）
    expect 该表达式 `repr()` 出来的文本

`mcq()` 会先 `exec` 这段代码，拿到实跑结果，再在选项里找**恰好等于该结果**的那一项，
答案字母由它反推 —— 也就是说：answer 不是手写的，是跑出来的。
`tfq()` 拿实跑结果跟声明的真假比，`fillq()` 拿实跑结果去核答案表。

跑不了的（纯定义题，如「列表与元组的区别」）走 `mc()/tf()/fill()` 原样手写，
但**每一道这样的题都在下面标了「无实跑」**，方便日后人来复核。

答案键的排版约定（由 `app/bank_kit.py` 统一保证）
- 期望值一律 `|答案`，多行 = 多个可接受写法，`oneof` 口径
- 理论题用例 `is_sample` 恒为 0：样例会公开在静态站上，等于把答案印在题面
"""
from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.bank_kit import fill, mc, multi, tf          # noqa: E402

OUT_PATH = ROOT / "app" / "problems_bank_py_theory.py"

HEADER = '''"""Python 线理论题库 —— **自动生成，不要手改**。

本文件由 `tools/gen_py_theory.py` 产出，重新生成：

    python tools/gen_py_theory.py

题源
----
《Python快乐编程基础入门》（ISBN 9787302530145）第 02 ~ 14 讲的知识点，
按讲义章节分节（`source_section`），与同节的编程题并列。
全部是**理论题**（`line = "text"`）：提交答案文本，由 `app/judge/runner_text.py`
归一化后交给 `oneof` checker 比对，不启子进程。

答案可信度
----------
凡能实跑的题，答案键都是 `expect` 表达式**在本机 3.13 上跑出来的结果反推**的，
不是手写的；生成器跑不通过的题根本写不出这个文件。
少数纯定义题（列表与元组的区别、*args 语义之类）无法用一行代码判定，
在生成器里标了「无实跑」，靠教材口径人工核对。
"""
from __future__ import annotations

PY_THEORY_PROBLEMS: list[dict] = '''


# =========================================================================
# 实跑：把一段源码跑出结果，返回 repr 文本
# =========================================================================
def ev(src: str) -> str:
    """执行 `src`（最后一行必须是表达式），返回末行求值结果的 repr。

    ★ 为什么用 exec+eval 而不是 subprocess
      生成器自己就跑在 ref_interpreter 指定的 3.13 上，同一解释器里跑出来的
      结果就是学生那边会看到的结果；subprocess 只会让每次生成慢上二三十倍。
      隔离性够用：这里的代码全部由本文件写死，不接受外部输入。
    """
    tree = ast.parse(src)
    if not tree.body or not isinstance(tree.body[-1], ast.Expr):
        raise ValueError("check 代码的最后一行必须是表达式：%r" % src[:60])
    ns: dict = {"__name__": "_chk"}
    body = ast.Module(body=tree.body[:-1], type_ignores=[])
    # ★ 有些题**故意**写出会触发告警的代码（比如 `{10, 20}[0]` 会报
    #   SyntaxWarning: 'set' object is not subscriptable）——那正是题干要考的点。
    #   这里把告警吞掉，否则生成器输出会被这行噪音糊住。
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        exec(compile(body, "<chk>", "exec"), ns)
        return repr(eval(compile(ast.Expression(tree.body[-1].value), "<chk>", "eval"), ns))


PROBS: list[dict] = []
_SEEN: set[str] = set()


def _push(p: dict) -> dict:
    t = p["title"]
    if t in _SEEN:
        raise SystemExit("★ 标题重复：%s" % t)
    _SEEN.add(t)
    PROBS.append(p)
    return p


def mcq(*, title: str, stmt: str, options: list[str], code: str, section: str,
        expl: str, tags: list[str], diff: int = 1, score: int = 10,
        note: str = "") -> dict:
    """单选题 —— 答案字母由**实跑结果**在选项里的位置反推。

    选项文本允许写 `'cba'`（带引号的 repr 原样）或 `cba`（去掉引号）；
    两种写法都能反查到字母，但**必须恰好命中一个选项**。
    """
    want = ev(code)
    bare = want[1:-1] if len(want) >= 2 and want[0] == want[-1] and want[0] in "'\"" else want
    for cand in ([want] if bare == want else [want, bare]):
        if options.count(cand) == 1:
            letter = "ABCDEFGH"[options.index(cand)]
            return _push(mc(title, stmt, options, letter, subject="python",
                            section=section, explanation=expl, tags=tags,
                            difficulty=diff, total_score=score, answer_note=note))
    raise SystemExit("★ %s：实跑得 %s，在选项里命中 %d 次（要么 0 次要么多次）"
                     % (title, want, options.count(want)))


def tfq(*, title: str, stmt: str, code: str, section: str, expl: str,
        tags: list[str], diff: int = 1) -> dict:
    """判断题 —— `code` 必须返回「题干这句话是否为真」。"""
    got = ev(code)
    if got not in ("True", "False"):
        raise SystemExit("★ %s：check 必须返回布尔，实际 %s" % (title, got))
    return _push(tf(title, stmt, got == "True", subject="python", section=section,
                    explanation=expl, tags=tags, difficulty=diff))


def fillq(*, title: str, stmt: str, answers: list[str], code: str, section: str,
          expl: str, tags: list[str], diff: int = 2, hint: str = "",
          extra: list[str] | None = None) -> dict:
    """填空题 —— 实跑结果必须出现在可接受答案里（通常是第一个）。"""
    got = ev(code)
    bare = got[1:-1] if len(got) >= 2 and got[0] == got[-1] and got[0] in "'\"" else got
    if bare not in answers:
        raise SystemExit("★ %s：实跑得 %s，不在答案表 %s 里" % (title, bare, answers))
    # ★ 为什么允许 extra：`normalize_answer()` 会把 `True`/`False` 归一成 `对`/`错`
    #   （那是给判断题用的便利）。于是答案写 `False` 的填空题，学生答 `False`
    #   会被归成 `错`，永远对不上 `|False` —— 由 `selftest_theory.py` 的全库扫抓出来的。
    #   补上 `错` 这个等价写法即可，语义也一样（False 就是「错」）。
    return _push(fill(title, stmt, answers + list(extra or []), subject="python",
                      section=section, explanation=expl, tags=tags,
                      difficulty=diff, hint=hint))


def shortq(*, title: str, statement_md: str, answers: list[str], section: str,
           explanation: str, tags: list[str], difficulty: int = 3,
           total_score: int = 12, hint: str = "") -> dict:
    """简答题 —— 结构跟填空题一样（`oneof` 比答案文本），只是题型标签不同。

    ★ 这类题**没有实跑**（答案是一句人话，不是可求值的表达式），
      所以答案表里要把常见等价说法都列上，题干里也要给句式提示 —— 否则
      `oneof` 会把「说得对但用词不同」的答案判错。
    """
    p = fill(title, statement_md, answers, subject="python", section=section,
             explanation=explanation, tags=tags, difficulty=difficulty,
             total_score=total_score, hint=hint)
    p["question_type"] = "short_answer"
    p["output_format"] = "一句话作答（不要写解释、不要抄题目）"
    return _push(p)


def multq(*, title: str, stmt: str, options: list[str], answers: list[str],
          checks: list[tuple[str, str]], section: str, expl: str, tags: list[str],
          diff: int = 3) -> dict:
    """多选题 —— 每个选项配一句「该选项是否为真」的实跑代码，全跑一遍再定答案。"""
    letters = "ABCDEFGH"
    if len(checks) != len(options):
        raise SystemExit("★ %s：checks 数量要跟选项一一对应" % title)
    got = set()
    for (letter, code), text in zip(checks, options):
        r = ev(code)
        if r not in ("True", "False"):
            raise SystemExit("★ %s 选项 %s：check 必须返回布尔，实际 %s" % (title, letter, r))
        if r == "True":
            got.add(letter)
    if got != set(a.strip().upper() for a in answers):
        raise SystemExit("★ %s：实跑得正确项 %s，声明的答案是 %s"
                         % (title, "".join(sorted(got)), "".join(sorted(answers))))
    return _push(multi(title, stmt, options, sorted(got), subject="python",
                       section=section, explanation=expl, tags=tags, difficulty=diff))


# =========================================================================
# 第 02 讲 · 编程基础
# =========================================================================
mcq(title="幂运算符是右结合", code="2 ** 3 ** 2",
    stmt="表达式 `2 ** 3 ** 2` 的值是多少？",
    options=["64", "512", "12", "语法错误"],
    section="第 02 讲 · 编程基础",
    expl="`**` 是**右结合**：先算 `3 ** 2 = 9`，再算 `2 ** 9 = 512`。"
         "如果按从左往右算会得 `(2**3)**2 = 64`，那是错的。要左结合必须自己加括号。",
    tags=["运算符", "优先级"])

mcq(title="负数整除是向下取整", code="-7 // 2",
    stmt="表达式 `-7 // 2` 的值是多少？",
    options=["-4", "-3", "-3.5", "3"],
    section="第 02 讲 · 编程基础",
    expl="`//` 是**向下取整**（floor），不是向零截断：`-3.5` 往下取到 `-4`。"
         "这与 C/Java 的整数除法（向零截断得 `-3`）不同，是跨语言最容易踩的一处。",
    tags=["运算符", "整除"])

mcq(title="取模结果的符号跟着除数", code="-7 % 3",
    stmt="表达式 `-7 % 3` 的值是多少？",
    options=["-1", "1", "2", "-2"],
    section="第 02 讲 · 编程基础",
    expl="Python 的 `%` 结果符号**跟除数一致**（这里除数是正数 3，所以结果为正）。"
         "它满足 `a == (a // b) * b + a % b`：`(-4)*3 + 2 = -10`？不对——是 `(-3)*3 + 2 = -7`。"
         "记住这条恒等式就能自己推，不用背。",
    tags=["运算符", "取模"])

mcq(title="浮点数参与整除的结果类型", code="7 // 2.0",
    stmt="表达式 `7 // 2.0` 的值是多少？",
    options=["3", "3.0", "3.5", "4.0"],
    section="第 02 讲 · 编程基础",
    expl="`//` 只是「取整」，**不改变类型**：有 float 参与就还是 float，所以是 `3.0` 而不是 `3`。",
    tags=["运算符", "类型"])

# =========================================================================
# 第 03 讲 · 流程控制语句
# =========================================================================
mcq(title="range 的负步长", code="list(range(5, 0, -2))",
    stmt="`list(range(5, 0, -2))` 的结果是什么？",
    options=["[5, 3, 1]", "[5, 3, 1, -1]", "[4, 2, 0]", "[5, 4, 3, 2, 1]"],
    section="第 03 讲 · 流程控制语句",
    expl="`range(start, stop, step)` 是**左闭右开**：从 5 开始，每次减 2，"
         "取到 `> 0` 为止 → 5、3、1。`stop` 那个 0 本身取不到。",
    tags=["range", "循环"])

mcq(title="循环被 break 时 else 不执行", code="""hit = []
for i in range(3):
    if i == 1:
        break
else:
    hit.append('else')
hit""",
    stmt="下面这段代码执行后 `hit` 是什么？\n\n"
         "```python\nhit = []\nfor i in range(3):\n    if i == 1:\n        break\nelse:\n"
         "    hit.append('else')\n```",
    options=["[]", "['else']", "[0, 1]", "报错"],
    section="第 03 讲 · 流程控制语句",
    expl="`for ... else` 的 `else` 只在**循环正常走完**（没被 break 打断）时执行。"
         "这里 `i == 1` 就 break 了，所以 `hit` 一直是空列表。"
         "它是「没找到才执行」的天然写法，比设一个 flag 变量干净。",
    tags=["for-else", "break"])

mcq(title="循环变量在循环结束后仍存在", code="""for i in range(3):
    pass
i""",
    stmt="执行 `for i in range(3): pass` 之后，变量 `i` 的值是多少？",
    options=["2", "3", "0", "NameError：i 不存在"],
    section="第 03 讲 · 流程控制语句",
    expl="Python 的循环**不产生新的作用域**，循环变量在循环结束后依然存在，"
         "值是最后一次赋的值（这里依次是 0、1、2，所以停在 2）。"
         "这一点跟 C 的 `for (int i ...)` 完全不同。",
    tags=["作用域", "循环"])

# =========================================================================
# 第 04 讲 · 字符串
# =========================================================================
mcq(title="切片反转字符串", code="'abc'[::-1]",
    stmt="`'abc'[::-1]` 的结果是什么？",
    options=["'abc'", "'cba'", "'c'", "报错"],
    section="第 04 讲 · 字符串",
    expl="切片 `[start:stop:step]` 三段全省略、步长给 `-1`，就是从尾到头取一遍 → `'cba'`。"
         "这是 Python 里反转序列最惯用的写法，列表、元组同样适用。",
    tags=["切片", "字符串"])

mcq(title="split 不合并连续分隔符产生的空串", code="'a,b,,c'.split(',')",
    stmt="`'a,b,,c'.split(',')` 的结果是什么？",
    options=["['a', 'b', 'c']", "['a', 'b', '', 'c']",
             "['a', 'b', ',', 'c']", "报错"],
    section="第 04 讲 · 字符串",
    expl="`split` 按分隔符**机械切开**，中间连续两个逗号之间会留下一个空串，所以是 4 段。"
         "如果要丢掉空段，用 `[x for x in s.split(',') if x]`，或者干脆用 `re.split` 后过滤。",
    tags=["split", "字符串"])

mcq(title="find 找不到时返回 -1", code="'abc'.find('z')",
    stmt="`'abc'.find('z')` 的返回值是多少？",
    options=["-1", "0", "None", "抛出 ValueError"],
    section="第 04 讲 · 字符串",
    expl="`find` 找不到返回 **-1**，不抛异常——所以 `if s.find(x):` 这种写法是坑："
         "找到了但位置是 0 时它是假值。要判存在就用 `x in s`。"
         "对比：`index` 找不到会抛 `ValueError`。",
    tags=["find", "字符串"])

# =========================================================================
# 第 05 讲 · 列表与元组
# =========================================================================
mcq(title="列表乘法的浅拷贝", code="[1, 2] * 2",
    stmt="`[1, 2] * 2` 的结果是什么？",
    options=["[1, 2, 1, 2]", "[2, 4]", "[1, 2, 2]", "报错"],
    section="第 05 讲 · 列表与元组",
    expl="`*` 是**重复**，不是逐元素相乘（逐元素要 numpy）。"
         "注意它做的是**浅拷贝**：`[[0]] * 3` 得到的三行是**同一个列表对象**，"
         "改一行会全变——这是二维数组初始化的经典坑。",
    tags=["列表", "乘法"])

mcq(title="sort 返回 None 而不是新列表", code="""a = [3, 1, 2]
r = a.sort()
r""",
    stmt="```python\na = [3, 1, 2]\nr = a.sort()\n```\n执行后 `r` 是什么？",
    options=["None", "[1, 2, 3]", "[3, 1, 2]", "报错"],
    section="第 05 讲 · 列表与元组",
    expl="`list.sort()` 是**就地**排序，返回值恒为 `None`（故意这样设计，提醒你它改的是原列表）。"
         "要新列表用 `sorted(a)`。`r = a.sort()` 之后 `r` 是 None、`a` 已经变成有序——"
         "再对 `r` 做 `for` 循环就会 TypeError。",
    tags=["sort", "就地"])

mcq(title="单元素元组必须带逗号", code="len((1,))",
    stmt="`len((1,))` 的值是多少？",
    options=["1", "0", "2", "报错"],
    section="第 05 讲 · 列表与元组",
    expl="`(1)` 只是加括号的整数 1，**不是元组**；单元素元组必须写成 `(1,)`，"
         "那个逗号才是元组构造符。空元组例外，写 `()` 就行。",
    tags=["元组", "语法"])

# =========================================================================
# 第 06 讲 · 字典与集合
# =========================================================================
mcq(title="get 取不到时返回 None", code="{'a': 1}.get('b')",
    stmt="`{'a': 1}.get('b')` 的结果是什么？",
    options=["None", "KeyError", "0", "''"],
    section="第 06 讲 · 字典与集合",
    expl="`d.get(k)` 取不到返回 `None`（可以给第二个参数指定默认值），**不抛异常**；"
         "`d[k]` 取不到才抛 `KeyError`。所以「不确定键在不在」时用 `get`。",
    tags=["dict", "get"])

mcq(title="集合自动去重", code="len({1, 1, 2, 2, 3})",
    stmt="`len({1, 1, 2, 2, 3})` 的值是多少？",
    options=["3", "5", "1", "报错"],
    section="第 06 讲 · 字典与集合",
    expl="集合的键唯一，重复的会被**静默丢掉**，所以剩 `{1, 2, 3}`，长度 3。"
         "「一行去重」就靠这个：`list(set(seq))`（注意这会打乱顺序，要保序用 `dict.fromkeys`）。",
    tags=["set", "去重"])

# =========================================================================
# 第 07 / 08 讲 · 函数
# =========================================================================
mcq(title="默认参数只在定义时求值一次", code="""def f(a, acc=[]):
    acc.append(a)
    return acc
f(1), f(2)""",
    stmt="```python\ndef f(a, acc=[]):\n    acc.append(a)\n    return acc\n```\n"
         "连续调用 `f(1)`、`f(2)`，两次的返回值合起来是什么？",
    options=["([1, 2], [1, 2])", "([1], [2])", "([1], [1, 2])", "报错"],
    section="第 07 讲 · 函数",
    expl="默认值在**函数定义时求值一次**并挂在 `f.__defaults__` 上，之后每次调用共用同一个列表，"
         "所以第一次 append 1、第二次 append 2，两次返回的是同一个对象 → `([1, 2], [1, 2])`。"
         "正确写法是 `def f(a, acc=None): acc = [] if acc is None else acc`。",
    tags=["默认参数", "陷阱"], diff=2)

mcq(title="*args 收到的是元组", code="""def g(a, b=2, *args, **kw):
    return args
g(1, 3, 4, 5, x=6)""",
    stmt="```python\ndef g(a, b=2, *args, **kw):\n    return args\n```\n"
         "`g(1, 3, 4, 5, x=6)` 返回什么？",
    options=["(4, 5)", "(1, 3, 4, 5)", "(3, 4, 5)", "报错"],
    section="第 08 讲 · 函数",
    expl="位置参数先喂满普通形参：`a=1`、`b=3`，**剩下的** 4、5 才进 `*args`（元组）；"
         "`x=6` 进 `**kw`（字典）。所以 `args` 是 `(4, 5)`。"
         "注意 `b` 虽然带默认值 2，但有位置实参时照样被覆盖。",
    tags=["*args", "参数"], diff=2)

mcq(title="函数内赋值会让变量变成局部变量", code="""x = 1
def h():
    x += 1
    return x
try:
    h()
except UnboundLocalError:
    r = 'UnboundLocalError'
r""",
    stmt="```python\nx = 1\ndef h():\n    x += 1\n    return x\n```\n调用 `h()` 会发生什么？",
    options=["返回 2", "返回 1", "UnboundLocalError", "NameError"],
    section="第 08 讲 · 函数",
    expl="函数体里只要对 `x` **赋过值**（`x += 1` 就是赋值），`x` 在整个函数内就是局部变量，"
         "于是 `x += 1` 里的那个「读」找不到局部 `x` → `UnboundLocalError`。"
         "要改全局变量得先 `global x`；`NameError` 是另一个异常，别混。",
    tags=["作用域", "UnboundLocalError"], diff=3)

# =========================================================================
# 第 09 讲 · 模块与包
# =========================================================================
mcq(title="import 之后必须用限定名", code="""import math
try:
    sqrt(4)
except NameError:
    r = 'NameError'
r""",
    stmt="只写了 `import math`，然后直接调用 `sqrt(4)`，会怎样？",
    options=["正常返回 4.0", "NameError", "AttributeError", "返回 2"],
    section="第 09 讲 · 模块与包",
    expl="`import math` 只把**模块名** `math` 绑进当前命名空间，里面的 `sqrt` 没有进来，"
         "得写 `math.sqrt(4)`。要直接用名字就 `from math import sqrt`。"
         "`import math.sqrt` 这种写法才是错的（sqrt 不是子模块）。",
    tags=["import", "命名空间"])

mcq(title="math.sqrt 返回浮点数", code="""import math
math.sqrt(16)""",
    stmt="`math.sqrt(16)` 的结果是什么？",
    options=["4", "4.0", "2", "16"],
    section="第 09 讲 · 模块与包",
    expl="`math.sqrt` 一律返回 `float`，完全平方数也是 `4.0` 不是 `4`。"
         "要整数开方可以用 `math.isqrt`（返回 int，且是真·整数运算）。",
    tags=["math", "类型"])

# =========================================================================
# 第 10 / 11 讲 · 面向对象
# =========================================================================
mcq(title="bool 是 int 的子类", code="isinstance(True, int)",
    stmt="`isinstance(True, int)` 的结果是什么？",
    options=["True", "False", "TypeError", "None"],
    section="第 10 讲 · 面向对象（上）",
    expl="`bool` 是 `int` 的**子类**（`issubclass(bool, int)` 为 True），`True == 1`、`False == 0`，"
         "所以 `isinstance(True, int)` 为 True。副作用：`sum([True, True]) == 2`，"
         "以及 `{1: 'a'}[True]` 能取到 `'a'`。",
    tags=["bool", "继承"])

mcq(title="实例属性赋值不会改类属性", code="""class C:
    n = 0
c = C()
c.n = 5
C.n""",
    stmt="```python\nclass C:\n    n = 0\nc = C()\nc.n = 5\n```\n此时 `C.n` 是多少？",
    options=["0", "5", "None", "AttributeError"],
    section="第 11 讲 · 面向对象（下）",
    expl="`c.n = 5` 是给**实例**新建一个属性，遮住（shadow）同名类属性，类本身没被改动，"
         "所以 `C.n` 还是 0。要改类属性必须写 `C.n = 5` 或用 `type(c).n = 5`。"
         "读到 5 的是 `c.n` —— 这是「属性查找先实例后类」的必然结果。",
    tags=["类属性", "实例属性"], diff=2)

# =========================================================================
# 第 12 讲 · 文件
# =========================================================================
mcq(title="w 模式打开就清空", code="""import os, tempfile
p = os.path.join(tempfile.mkdtemp(), 't.txt')
open(p, 'w', encoding='utf-8').write('abc')
open(p, 'w', encoding='utf-8').close()
os.path.getsize(p)""",
    stmt="先往文件写入 `abc`，再用 `open(p, 'w')` 打开并立刻关闭，文件大小是多少字节？",
    options=["0", "3", "6", "报错"],
    section="第 12 讲 · 文件",
    expl="`'w'` 模式打开的那一刻文件就被**截断**（truncate）成 0 字节，"
         "不是「写的时候才清空」。所以只想追加要用 `'a'`，想读写又不想清空要用 `'r+'`。",
    tags=["open", "文件模式"], diff=2)

mcq(title="readlines 返回列表", code="""import os, tempfile
p = os.path.join(tempfile.mkdtemp(), 't.txt')
open(p, 'w', encoding='utf-8').write('a\\nb\\n')
type(open(p, encoding='utf-8').readlines()).__name__""",
    stmt="`f.readlines()` 返回什么类型的对象？",
    options=["'list'", "'str'", "'generator'", "'tuple'"],
    section="第 12 讲 · 文件",
    expl="`readlines()` 一次性把全文切成行，返回**列表**（每行带结尾的 `\\n`）；"
         "`read()` 返回整串，`readline()` 返回一行。文件很大时别用 `readlines`，"
         "直接 `for line in f` 才是流式的。",
    tags=["readlines", "文件"], diff=2)

# =========================================================================
# 多选题（10 道；每个选项都有一句实跑代码来判定对错）
# =========================================================================
multq(title="哪些是不可变类型",
      stmt="下列哪些类型是**不可变**类型？", options=["int", "list", "tuple", "str"],
      answers=["A", "C", "D"],
      checks=[
          # 不可变的实证：`+=` 不会改原对象，而是绑到一个**新对象**上（id 变了）
          ("A", """x = 1
i = id(x)
x += 1
id(x) != i"""),
          ("B", """x = [1]
try:
    x.append(2)
    mutated = True
except Exception:
    mutated = False
not mutated"""),
          ("C", """t = (1, 2)
try:
    t[0] = 9
    mutated = True
except TypeError:
    mutated = False
not mutated"""),
          ("D", """s = 'a'
i = id(s)
s += 'b'
id(s) != i"""),
      ],
      section="第 02 讲 · 编程基础",
      expl="`int`、`str`、`tuple` 都是不可变对象：想「改」只能造新的 —— "
           "`x += 1` 看着像加一，其实是把 `x` 重新绑到一个新整数上（`id` 会变）。"
           "`list` 可以就地增删改，`id` 不变。"
           "★ 注意 `id` 这条只对 CPython 有意义（小整数还有缓存），"
           "但「不可变 → 运算产生新对象」这条语义是语言层面的。",
      tags=["不可变", "类型"])

multq(title="哪些操作会就地修改列表",
      stmt="下列哪些操作会**就地**修改列表本身？", options=["append", "sort", "reverse", "sorted"],
      answers=["A", "B", "C"],
      checks=[
          ("A", """a = [1]
a.append(2)
a == [1, 2]"""),
          ("B", """a = [2, 1]
a.sort()
a == [1, 2]"""),
          ("C", """a = [1, 2]
a.reverse()
a == [2, 1]"""),
          # 内置函数 sorted 不改原列表 —— 断言就是「原列表没变」
          ("D", """a = [2, 1]
sorted(a)
a == [1, 2]"""),
      ],
      section="第 05 讲 · 列表与元组",
      expl="`append` / `sort` / `reverse` 都是**就地**方法，返回 `None`，改的是原对象；"
           "`sorted()` 是内置函数，返回**新列表**、原列表不动。"
           "判别口诀：方法（`a.sort()`）就地，函数（`sorted(a)`）新建。",
      tags=["list", "就地"])

multq(title="关于 break / continue / for-else 的说法",
      stmt="关于 `break` / `continue` / `for-else`，下列哪些说法正确？", options=[
        "break 会结束整个循环",
        "continue 只跳过本轮剩余语句，进入下一轮",
        "for-else 的 else 在被 break 打断时不执行",
        "for-else 的 else 在循环体一次都没执行时也不执行"],
      answers=["A", "B", "C"],
      checks=[
          ("A", """hit = []
for i in range(5):
    if i == 2:
        break
    hit.append(i)
hit == [0, 1]"""),
          ("B", """hit = []
for i in range(5):
    if i % 2:
        continue
    hit.append(i)
hit == [0, 2, 4]"""),
          ("C", """hit = []
for i in range(3):
    if i == 1:
        break
else:
    hit.append(1)
hit == []"""),
          # 这条说法是错的：循环体一次都没跑也算「正常结束」，else 照样执行。
          # 断言就写「else 没执行」这件事 —— 实跑为 False，故 D 不是正确项。
          ("D", """hit = []
for i in range(0):
    pass
else:
    hit.append(1)
hit == []"""),
      ],
      section="第 03 讲 · 流程控制语句",
      expl="`break` 跳出**整个**循环；`continue` 只结束本轮；`for-else` 的 `else` 属于"
           "「循环正常结束」这条路径，被 break 打断就不执行。"
           "★ 最后一条是反直觉的地方：**循环体一次都没跑**（`range(0)`）也算正常结束，"
           "`else` 照样执行 —— 所以它天然适合写「找了一圈没找到」。",
      tags=["break", "for-else"])

multq(title="下列哪些是 Python 内置异常",
      stmt="下列哪些是 Python 的**内置异常**？", options=[
        "ZeroDivisionError", "ValueError", "IndexError", "NullPointerError"],
      answers=["A", "B", "C"],
      checks=[
          ("A", "issubclass(ZeroDivisionError, Exception)"),
          ("B", "issubclass(ValueError, Exception)"),
          ("C", "issubclass(IndexError, Exception)"),
          ("D", "'NullPointerError' in dir(__builtins__) or hasattr(__import__('builtins'), 'NullPointerError')"),
      ],
      section="第 13 讲 · 异常",
      expl="前三个都是内置异常。`NullPointerError` 是**Java** 的，Python 里没有——"
           "Python 对应的是 `AttributeError`（访问不存在的属性）"
           "和 `TypeError`（对 None 做操作，常见于忘了 `return`）。",
      tags=["异常", "内置"])

multq(title="哪些能当字典的键",
      stmt="下列哪些值可以直接作为字典的键？", options=["3", "'a'", "(1, 2)", "[1]"],
      answers=["A", "B", "C"],
      checks=[
          ("A", "hash(3) == 3"),
          ("B", "hash('a') == hash('a')"),
          ("C", "hash((1, 2)) == hash((1, 2))"),
          ("D", """try:
    hash([1])
    ok = True
except TypeError:
    ok = False
ok"""),
      ],
      section="第 06 讲 · 字典与集合",
      expl="字典/集合的键必须**可哈希**，而「可哈希」的实质是**不可变**：数字、字符串、元组都可以，"
           "列表/字典/集合不行（当场 `TypeError: unhashable type`）。"
           "元组能当键的前提是它**里面每一个元素也都可哈希**：`([1],)` 就不行。",
      tags=["dict", "哈希"])

multq(title="哪些写法会得到新对象",
      stmt="`a` 是个列表，下列哪些写法会得到一个**新列表**（而不是原地修改）？", options=[
        "a.copy()", "sorted(a)", "a[:]", "a.append(1)"],
      answers=["A", "B", "C"],
      checks=[
          ("A", "a = [1]; b = a.copy(); b is not a"),
          ("B", "a = [1]; b = sorted(a); b is not a"),
          ("C", "a = [1]; b = a[:]; b is not a"),
          ("D", """a = [1]
b = a.append(2)
isinstance(b, list) and b is not a"""),
      ],
      section="第 05 讲 · 列表与元组",
      expl="`copy()`、`sorted()`、`[:]` 都造新列表（**浅**拷贝，内层还是同一批对象）；"
           "`append` 是就地方法、返回 `None`。"
           "★ 浅拷贝的坑：`b = a[:]` 之后 `b[0]` 若是列表，改它还是会串到 `a`。",
      tags=["拷贝", "list"])

multq(title="关于 *args 与 **kwargs 的说法",
      stmt="关于 `*args` 与 `**kwargs`，下列哪些说法正确？", options=[
        "*args 收集多余的位置实参，是元组",
        "**kwargs 收集多余的关键字实参，是字典",
        "形参顺序里 *args 必须写在 **kwargs 前面",
        "调用时 f(*lst) 会把列表拆成若干个位置实参"],
      answers=["A", "B", "C", "D"],
      checks=[
          ("A", """def f(*a): return a
f(1, 2) == (1, 2)"""),
          ("B", """def f(**k): return k
f(x=1) == {'x': 1}"""),
          # 「必须写在前面」的硬证据：反着写是语法错误
          ("C", """try:
    compile('def f(**k, *a): pass', '<t>', 'exec')
    ok = False
except SyntaxError:
    ok = True
ok"""),
          ("D", """def f(a, b): return a + b
f(*[3, 4]) == 7"""),
      ],
      section="第 08 讲 · 函数",
      expl="四条都对：`*args` 收成元组、`**kwargs` 收成字典，形参顺序必须是"
           "「普通参数 → `*args` → 有默认值的关键字参数 → `**kwargs`」；"
           "`f(*lst)` 是**拆包**，和定义处的 `*args` 是同一个符号的两种用法。",
      tags=["*args", "**kwargs"])

multq(title="用 with 打开文件的好处",
      stmt="用 `with open(...) as f:` 打开文件，下列哪些说法正确？", options=[
        "离开代码块时自动关闭文件",
        "块内抛异常时也会关闭",
        "省去手写 try/finally",
        "会把整个文件读进内存"],
      answers=["A", "B", "C"],
      checks=[
          ("A", """import os, tempfile
p = os.path.join(tempfile.mkdtemp(), 't.txt')
with open(p, 'w', encoding='utf-8') as f:
    pass
f.closed"""),
          ("B", """import os, tempfile
p = os.path.join(tempfile.mkdtemp(), 't.txt')
try:
    with open(p, 'w', encoding='utf-8') as f:
        raise RuntimeError('boom')
except RuntimeError:
    pass
f.closed"""),
          ("C", """import os, tempfile
p = os.path.join(tempfile.mkdtemp(), 't.txt')
open(p, 'w', encoding='utf-8').close()
hasattr(type(open(p, encoding='utf-8')), '__enter__')"""),
          ("D", "False"),
      ],
      section="第 12 讲 · 文件",
      expl="`with` 是上下文管理器语法：无论正常退出还是抛异常，`__exit__` 都会被调用，"
           "所以关文件、放锁、回滚事务都不会漏。它**不会**替你读文件内容——"
           "读不读、读多少，还是你自己写在块里的。",
      tags=["with", "文件"])

multq(title="关于文件模式的正确说法",
      stmt="关于 `open()` 的文件模式，下列哪些说法正确？", options=[
        "'r' 只读，文件不存在直接报错",
        "'w' 清空已有内容或新建文件",
        "'a' 在文件末尾追加，不截断",
        "'r+' 打开时会清空文件"],
      answers=["A", "B", "C"],
      checks=[
          ("A", """import os, tempfile
p = os.path.join(tempfile.mkdtemp(), 'nope.txt')
try:
    open(p, 'r', encoding='utf-8')
    ok = False
except FileNotFoundError:
    ok = True
ok"""),
          ("B", """import os, tempfile
p = os.path.join(tempfile.mkdtemp(), 't.txt')
open(p, 'w', encoding='utf-8').write('abc')
open(p, 'w', encoding='utf-8').close()
os.path.getsize(p) == 0"""),
          ("C", """import os, tempfile
p = os.path.join(tempfile.mkdtemp(), 't.txt')
open(p, 'w', encoding='utf-8').write('abc')
f = open(p, 'a', encoding='utf-8')
f.write('d')
f.close()
open(p, encoding='utf-8').read() == 'abcd'"""),
          ("D", """import os, tempfile
p = os.path.join(tempfile.mkdtemp(), 't.txt')
open(p, 'w', encoding='utf-8').write('abc')
open(p, 'r+', encoding='utf-8').close()
os.path.getsize(p) == 0"""),
      ],
      section="第 12 讲 · 文件",
      expl="`'r'` 只读且要求文件存在；`'w'` 一打开就截断；`'a'` 追加不截断、文件不存在就新建。"
           "`'r+'` 是**读写**且**不清空**（指针在开头，写会覆盖前面的字节）——"
           "最后一条说它清空，是错的，这正是与 `'w+'` 的区别。",
      tags=["文件模式", "open"])

multq(title="关于魔术方法的说法",
      stmt="关于 `__str__` / `__repr__` / `super()` / `__init__`，下列哪些说法正确？", options=[
        "__str__ 面向用户，print 时调用",
        "__repr__ 面向开发者，交互环境里显示",
        "super() 用来调用父类的方法",
        "__init__ 必须返回 self"],
      answers=["A", "B", "C"],
      checks=[
          ("A", """class A:
    def __str__(self): return 'hi'
str(A()) == 'hi'"""),
          ("B", """class A:
    def __repr__(self): return 'A()'
repr(A()) == 'A()'"""),
          ("C", """class A:
    def who(self): return 'A'
class B(A):
    def who(self): return 'B+' + super().who()
B().who() == 'B+A'"""),
          ("D", """class A:
    def __init__(self):
        return self
try:
    A()
    ok = True
except TypeError:
    ok = False
ok"""),
      ],
      section="第 11 讲 · 面向对象（下）",
      expl="`__str__` 给 `print`/`str()` 用，`__repr__` 给调试和交互环境用"
           "（没定义 `__str__` 时会退回 `__repr__`）；`super()` 沿 MRO 找父类方法。"
           "`__init__` **必须返回 None**，返回别的会 `TypeError` —— 它不是构造器，"
           "只负责初始化已创建好的实例。",
      tags=["魔术方法", "OOP"])

# =========================================================================
# 判断题（16 道，全部由实跑判定）
# =========================================================================
tfq(title="input() 的返回值总是字符串", stmt="`input()` 读进来的内容，类型总是 `str`。",
    code="isinstance(__import__('io').StringIO('3\\n').readline().rstrip('\\n'), str)",
    section="第 02 讲 · 编程基础",
    expl="`input()` 返回的**恒为字符串**，哪怕用户敲的是 `3`。要数字得自己 `int()`/`float()`。"
         "这也是 `input() + 1` 报 TypeError 的原因。", tags=["input"])

tfq(title="int 能直接转换 '3.5'", stmt="`int('3.5')` 能成功把字符串转成整数 3。",
    code="""try:
    int('3.5')
    ok = True
except ValueError:
    ok = False
ok""",
    section="第 02 讲 · 编程基础",
    expl="`int('3.5')` 抛 `ValueError` —— 它只认**整数字面量**。"
         "要转得先 `float('3.5')` 再 `int(...)`（这会截断成 3）。", tags=["类型转换"])

tfq(title="字符串是不可变的", stmt="`s = 'a'` 之后执行 `s[0] = 'b'` 会抛 TypeError。",
    code="""s = 'a'
try:
    s[0] = 'b'
    ok = False
except TypeError:
    ok = True
ok""",
    section="第 04 讲 · 字符串",
    expl="字符串不可变，下标赋值当场 `TypeError`。要「改」只能切片拼新串"
         "（`s[:1] + 'b' + s[2:]`）或转成 `list` 改完再 `join`。", tags=["字符串", "不可变"])

tfq(title="b = a 不是复制列表", stmt="`a = [1]` 之后 `b = a`，再 `b.append(2)`，`a` 也会变成 `[1, 2]`。",
    code="""a = [1]
b = a
b.append(2)
a == [1, 2]""",
    section="第 05 讲 · 列表与元组",
    expl="**对**。`b = a` 只复制了引用，两个名字指向同一列表。要真复制用"
         "`a.copy()`、`a[:]` 或 `list(a)`（都是浅拷贝）。"
         "`a == [1, 2]` 之所以为真，就是因为它们是一个对象。", tags=["引用", "list"])

tfq(title="元组完全不可变", stmt="元组一旦创建，连它内部元素的内容都不会变。",
    code="""t = ([1],)
t[0].append(2)
t == ([1],)""",
    section="第 05 讲 · 列表与元组",
    expl="**错**。元组只保证「自己这一层的**引用**不变」，元素若是可变对象，"
         "元素内容照样能改：`t = ([1],)`，`t[0].append(2)` 之后 `t` 变成 `([1, 2],)`，"
         "而 `t[0] = [9]` 才是不允许的。所谓「元组不可变」是浅层的。", tags=["元组", "陷阱"])

tfq(title="字典的键必须可哈希", stmt="把列表当字典的键会抛 TypeError。",
    code="""try:
    {[1]: 1}
    ok = False
except TypeError:
    ok = True
ok""",
    section="第 06 讲 · 字典与集合",
    expl="对。字典/集合靠哈希值定位，不可哈希的类型（list、dict、set）当键直接"
         "`TypeError: unhashable type: 'list'`。要按列表内容做键，先转成 `tuple`。",
    tags=["dict", "哈希"])

tfq(title="集合支持下标访问", stmt="`{10, 20}[0]` 能取到集合里的第一个元素。",
    code="""try:
    {10, 20}[0]
    ok = True
except TypeError:
    ok = False
ok""",
    section="第 06 讲 · 字典与集合",
    expl="错。集合**无序**，没有下标概念，`{10, 20}[0]` 抛 `TypeError: 'set' object is not subscriptable`。"
         "要取元素只能 `for x in s` / `next(iter(s))` / `list(s)[0]`（顺序不保证）。",
    tags=["set"])

tfq(title="默认参数只求值一次", stmt="函数写成 `def f(acc=[])`，多次调用会共用同一个默认列表。",
    code="""def f(acc=[]):
    acc.append(1)
    return acc
f()
f()
len(f.__defaults__[0]) == 2""",
    section="第 07 讲 · 函数",
    expl="对，这是 Python 最出名的坑之一。默认值在 `def` 执行时求值一次，"
         "之后挂在 `f.__defaults__` 上被所有调用共享。"
         "想每次新列表就写 `acc=None`，进函数再 `acc = [] if acc is None else acc`。",
    tags=["默认参数", "陷阱"])

tfq(title="Python 支持同名函数重载", stmt="Python 里可以定义两个同名但参数个数不同的函数，调用时按参数自动选。",
    code="""def f(x):
    return 1
def f(x, y):
    return 2
try:
    f(1)
    supported = True
except TypeError:
    supported = False
supported""",
    section="第 08 讲 · 函数",
    expl="错。Python **没有重载**：后一个 `def f` 直接覆盖前一个，只剩两个参数那版，"
         "`f(1)` 于是 `TypeError`。要「多态」靠默认参数、`*args` 或 `functools.singledispatch`"
         "（按类型分派）。", tags=["重载", "函数"])

tfq(title="import 之后模块内的名字不自动可见", stmt="只写 `import math` 就能直接调用 `sqrt(4)`。",
    code="""import math
try:
    sqrt(4)
    ok = True
except NameError:
    ok = False
ok""",
    section="第 09 讲 · 模块与包",
    expl="错。`import math` 只绑定了名字 `math`，得写 `math.sqrt(4)`；"
         "要用短名字就 `from math import sqrt`。`import` 不会把模块内容倒进当前命名空间。",
    tags=["import"])

tfq(title="__init__ 可以返回值", stmt="定义 `def __init__(self): return 1` 之后，实例化对象能拿到 1。",
    code="""class A:
    def __init__(self):
        return 1
try:
    A()
    ok = True
except TypeError:
    ok = False
ok""",
    section="第 10 讲 · 面向对象（上）",
    expl="错。`__init__` 只负责初始化已经创建好的实例，返回值必须是 `None`；"
         "返回别的会 `TypeError: __init__() should return None, not 'int'`。"
         "`A()` 拿到的永远是那个实例本身。", tags=["__init__", "OOP"])

tfq(title="with 退出时一定关闭文件", stmt="`with open(p) as f:` 代码块结束后 `f.closed` 为 True。",
    code="""import os, tempfile
p = os.path.join(tempfile.mkdtemp(), 't.txt')
with open(p, 'w', encoding='utf-8') as f:
    pass
f.closed""",
    section="第 12 讲 · 文件",
    expl="对。`with` 靠 `__exit__` 保证关闭，正常结束和抛异常都会走到，"
         "比手写 `try/finally` 更不容易漏。", tags=["with", "文件"])

tfq(title="finally 在 return 时也会执行", stmt="`try` 里 `return` 了，`finally` 块照样会跑。",
    code="""log = []
def f():
    try:
        return 1
    finally:
        log.append('x')
f()
log == ['x']""",
    section="第 13 讲 · 异常",
    expl="对。`return` 只是**准备**返回值，真正的返回要等 `finally` 跑完。"
         "所以 `finally` 里写 `return` 会**顶掉** `try` 里的返回值 —— 这是另一个坑，别这么写。",
    tags=["finally", "异常"])

tfq(title="except Exception 能捕获所有异常", stmt="`except Exception:` 能捕获包括 KeyboardInterrupt 在内的所有异常。",
    code="issubclass(SystemExit, Exception)",
    section="第 13 讲 · 异常",
    expl="错。`Exception` 只是绝大多数异常的基类，`KeyboardInterrupt`、`SystemExit`、`GeneratorExit` "
         "派生自 `BaseException`，用 `except Exception` 抓不到。"
         "想全抓得 `except BaseException`（几乎不该这么做，会让 Ctrl-C 失效）。",
    tags=["Exception", "异常层级"])

tfq(title="range 返回列表", stmt="`range(10)` 返回的是一个列表。",
    code="type(range(10)).__name__ == 'list'",
    section="第 03 讲 · 流程控制语句",
    expl="错。`range(10)` 返回 **range 对象**：惰性、占常数内存、可重复迭代。"
         "要列表得显式 `list(range(10))`。这也是 `range(10**9)` 不炸内存的原因。",
    tags=["range"])

tfq(title="字典保持插入顺序", stmt="Python 3.7 起，字典遍历顺序就是键的插入顺序。",
    code="""d = {}
d['b'] = 1
d['a'] = 2
list(d) == ['b', 'a']""",
    section="第 06 讲 · 字典与集合",
    expl="对。3.7 起 CPython 把「保持插入顺序」写进了语言规范（3.6 是实现细节）。"
         "所以要「去重同时保序」可以用 `dict.fromkeys(seq)`。"
         "注意：删掉再插回来算新插入，顺序会跑到最后。",
    tags=["dict", "顺序"])

# =========================================================================
# 填空题（12 道，答案都是单个词，全部由实跑核定）
# =========================================================================
fillq(title="浮点数相等比较的坑", stmt="表达式 `0.1 + 0.2 == 0.3` 的值是什么？",
      answers=["False"], extra=["错"], code="0.1 + 0.2 == 0.3",
      section="第 02 讲 · 编程基础",
      expl="二进制浮点数存不下 0.1、0.2，相加得 `0.30000000000000004`，与 `0.3` 不相等，"
           "所以是 `False`。比较浮点要用 `math.isclose(a, b)`。",
      tags=["浮点数", "陷阱"])

fillq(title="带步长的 range 有几个元素", stmt="`len(range(1, 10, 3))` 的值是多少？",
      answers=["3"], code="len(range(1, 10, 3))",
      section="第 03 讲 · 流程控制语句",
      expl="取的数是 1、4、7（下一个 10 已到 stop，右开区间取不到），共 3 个。",
      tags=["range"])

fillq(title="strip 去掉两端空白", stmt="`'  hi  '.strip()` 的结果是什么？（直接写结果）",
      answers=["hi"], code="'  hi  '.strip()",
      section="第 04 讲 · 字符串",
      expl="`strip()` 去掉**两端**的空白（空格、`\\t`、`\\n`），中间的不管。"
           "`lstrip`/`rstrip` 只管一边。", tags=["strip"])

fillq(title="join 把列表拼成字符串", stmt="`'-'.join(['a', 'b'])` 的结果是什么？",
      answers=["a-b"], code="'-'.join(['a', 'b'])",
      section="第 04 讲 · 字符串",
      expl="`'sep'.join(seq)` 用 sep 把**字符串序列**接起来。"
           "★ 序列里不能有数字，否则 `TypeError` —— 得先 `map(str, seq)`。",
      tags=["join"])

fillq(title="整除的结果", stmt="`10 // 4` 的值是多少？",
      answers=["2"], code="10 // 4",
      section="第 02 讲 · 编程基础",
      expl="`//` 向下取整，`2.5` 取到 `2`；余数用 `10 % 4` 得 2。"
           "两个操作合起来满足 `10 == (10//4)*4 + 10%4`。", tags=["整除"])

fillq(title="空列表的布尔值", stmt="`bool([])` 的值是什么？",
      answers=["False"], extra=["错"], code="bool([])",
      section="第 03 讲 · 流程控制语句",
      expl="空容器（`[]`、`()`、`{}`、`''`、`set()`）、`0`、`None` 都是假值。"
           "所以 `if not lst:` 是「列表为空」的惯用写法。", tags=["布尔", "真值"])

fillq(title="除法结果的类型名", stmt="`type(3 / 2).__name__` 的结果是什么？",
      answers=["float"], code="type(3 / 2).__name__",
      section="第 02 讲 · 编程基础",
      expl="**单个** `/` 永远是真除法，结果一定是 `float`（`3/2` 是 `1.5`，`4/2` 是 `2.0`）。"
           "Python 3 里没有「整数除法得整数」这回事，那是 `//`。", tags=["类型", "除法"])

fillq(title="字典键的数量", stmt="`len({'a': 1, 'b': 2}.keys())` 的值是多少？",
      answers=["2"], code="len({'a': 1, 'b': 2}.keys())",
      section="第 06 讲 · 字典与集合",
      expl="两个键就是两个，`keys()` 返回的是**视图对象**（跟着字典变），"
           "不是快照，`len` 直接能用。", tags=["dict", "keys"])

fillq(title="upper 转大写", stmt="`'abc'.upper()` 的结果是什么？",
      answers=["ABC"], code="'abc'.upper()",
      section="第 04 讲 · 字符串",
      expl="`upper()` 返回**新串**，原串不动（字符串不可变）。"
           "中文和数字不受影响。大小写不敏感的比较常用 `s.lower() == t.lower()` 或 `casefold()`。",
      tags=["upper"])

fillq(title="除零抛什么异常", stmt="`1 / 0` 抛出的异常类名是什么？",
      answers=["ZeroDivisionError"],
      code="""def f():
    try:
        1 / 0
    except ZeroDivisionError as e:
        return type(e).__name__
f()""",
      section="第 13 讲 · 异常",
      expl="`ZeroDivisionError`，它是 `ArithmeticError` 的子类。"
           "整数除零和浮点除零都抛它（不像 C 会得到 inf/nan）。", tags=["异常", "除零"])

fillq(title="reverse 排序后取第一个", stmt="`sorted([3, 1, 2], reverse=True)[0]` 的值是多少？",
      answers=["3"], code="sorted([3, 1, 2], reverse=True)[0]",
      section="第 05 讲 · 列表与元组",
      expl="`reverse=True` 是降序，排序结果 `[3, 2, 1]`，取第一个是 3。"
           "等价写法 `sorted(a)[-1]`，但 `reverse=True` 意图更清楚。", tags=["sorted"])

fillq(title="集合去重后的元素个数", stmt="`len(set('banana'))` 的值是多少？",
      answers=["3"], code="len(set('banana'))",
      section="第 06 讲 · 字典与集合",
      expl="`'banana'` 里的字符是 b、a、n、a、n、a，去重后只剩 `{b, a, n}` 三个，所以是 **3**。"
           "注意 `len` 数的是**不同元素**的个数，不是原串长度 6。",
      tags=["set", "去重"])

# =========================================================================
# 简答题（4 道，无实跑 —— 靠教材口径，答案表列出常见等价写法）
# =========================================================================
shortq(title="列表与元组有什么区别",
          section="第 05 讲 · 列表与元组",
          statement_md="**简答题**：说出列表（`list`）和元组（`tuple`）的三点区别。\n\n"
                       "按这个顺序答：可变性 → 语法 → 使用场景。",
          answers=[
              "列表可变，元组不可变；列表用方括号，元组用圆括号；列表适合存会变的数据，元组适合存固定记录",
              "列表可变元组不可变；列表用[]元组用()；列表用于增删改元组用于固定数据",
              "list可变tuple不可变；list用方括号tuple用圆括号；list存可变序列tuple存常量集合",
          ],
          explanation="1. **可变性**：`list` 能就地增删改（`append`/`pop`/`a[0]=1`）；"
                      "`tuple` 创建后不能改，下标赋值抛 `TypeError`。\n"
                      "2. **语法**：`[]` 与 `()`；单元素元组必须写 `(1,)`。\n"
                      "3. **场景**：列表存「同类、数量会变」的序列（一堆学生）；"
                      "元组存「字段固定、意义各不同」的记录（坐标 `(x, y)`、"
                      "函数返回多值），而且因为不可变，能当字典的键、能进集合。\n"
                      "补充：元组的 `tuple` 对象更省内存、创建更快。",
          tags=["list", "tuple", "简答"], difficulty=3, total_score=12,
          hint="三句话，每句一个区别即可。")

shortq(title="简述 *args 与 **kwargs 的作用",
          section="第 08 讲 · 函数",
          statement_md="**简答题**：`*args` 和 `**kwargs` 分别收集什么？各自是什么类型？",
          answers=[
              "*args收集多余的位置参数，是元组；**kwargs收集多余的关键字参数，是字典",
              "*args收集位置实参得到元组，**kwargs收集关键字实参得到字典",
              "args收集多余位置参数为元组，kwargs收集多余关键字参数为字典",
          ],
          explanation="`*args` 把「多出来的位置实参」收成一个**元组**；"
                      "`**kwargs` 把「多出来的关键字实参」收成一个**字典**。\n"
                      "形参顺序固定：普通参数 → `*args` → 有默认值的关键字参数 → `**kwargs`。\n"
                      "反过来的**拆包**写法：`f(*lst)` 把列表拆成若干位置实参，"
                      "`f(**d)` 把字典拆成若干关键字实参 —— 同名符号两用。",
          tags=["*args", "**kwargs", "简答"], difficulty=3, total_score=12,
          hint="两句话：一个元组、一个字典。")

shortq(title="__str__ 与 __repr__ 的区别",
          section="第 11 讲 · 面向对象（下）",
          statement_md="**简答题**：`__str__` 和 `__repr__` 分别给谁看？`print(obj)` 走哪个？",
          answers=[
              "__str__面向用户可读，__repr__面向开发者调试，print走__str__",
              "str给用户看repr给开发者看，print调用__str__",
              "__str__给人看__repr__给开发调试看，print用__str__",
          ],
          explanation="`__str__` 面向**最终用户**，要可读，`print()`、`str()`、`f'{obj}'` 调它；"
                      "`__repr__` 面向**开发者**，理想形态是「能重建该对象的表达式」"
                      "（如 `Point(1, 2)`），交互环境直接回车、`repr()`、容器打印时用它。\n"
                      "没定义 `__str__` 时，`print` 会退回 `__repr__`；反之则不成立。"
                      "所以两个都写时，`__repr__` 是兜底的那个。",
          tags=["魔术方法", "简答"], difficulty=3, total_score=12,
          hint="一句话说清「给谁看」，再点出 print 走哪个。")

shortq(title="浅拷贝与深拷贝的区别",
          section="第 05 讲 · 列表与元组",
          statement_md="**简答题**：浅拷贝（`copy.copy` / `list.copy` / `a[:]`）"
                       "与深拷贝（`copy.deepcopy`）的区别是什么？",
          answers=[
              "浅拷贝只复制最外层，内层对象仍是同一份；深拷贝递归复制所有层，互不影响",
              "浅拷贝复制外层引用共享内层，深拷贝递归复制全部，改内层不影响原对象",
              "浅拷贝只复制第一层，深拷贝把所有嵌套对象都复制一份",
          ],
          explanation="浅拷贝只造一个新的**外层容器**，里面的元素还是原来那些对象的引用；"
                      "深拷贝会**递归**复制每一层，得到一棵完全独立的树。\n"
                      "实证：`a = [[1], [2]]`，`b = a.copy()` 之后 `b[0].append(9)`，"
                      "`a` 也变成 `[[1, 9], [2]]` —— 因为 `a[0]` 和 `b[0]` 是同一个列表。"
                      "换成 `b = copy.deepcopy(a)` 就不会串。\n"
                      "对只含不可变元素（数字、字符串、元组）的列表，两者结果一模一样，"
                      "深拷贝只是白花时间。",
          tags=["拷贝", "简答"], difficulty=3, total_score=12,
          hint="重点说「内层对象」是共享还是各一份。")


# =========================================================================
# 生成
# =========================================================================
def _dump(probs: list[dict]) -> str:
    body = json.dumps(probs, ensure_ascii=False, indent=4)
    body = (body.replace(": null", ": None").replace(": true", ": True")
                .replace(": false", ": False"))
    return HEADER + body + "\n"


def _sanity(probs: list[dict]) -> list[str]:
    bad: list[str] = []
    seen: set[str] = set()
    for i, p in enumerate(probs, 1):
        t = p["title"]
        if t in seen:
            bad.append("[%d] 标题重复：%s" % (i, t))
        seen.add(t)
        for k in ("statement_md", "output_format", "reference_solution",
                  "source_section", "question_type"):
            if not str(p.get(k) or "").strip():
                bad.append("[%d] %s 缺字段 %s" % (i, t, k))
        if p["total_score"] <= 0:
            bad.append("[%d] %s 满分非法" % (i, t))
        for c in p["cases"]:
            if c["is_sample"]:
                bad.append("[%d] %s：理论题的样例必须隐藏（is_sample=0），否则答案印在题面上"
                           % (i, t))
            if not c["expected_stdout"].strip():
                bad.append("[%d] %s：期望值为空" % (i, t))
    return bad


def main() -> int:
    ap = argparse.ArgumentParser(description="生成 Python 线理论题库")
    ap.add_argument("--check", action="store_true", help="只校验，不写文件")
    args = ap.parse_args()

    probs = PROBS
    from collections import Counter
    by_type = Counter(p["question_type"] for p in probs)
    print("题目数：%d    测试点：%d    总分：%d"
          % (len(probs), sum(len(p["cases"]) for p in probs),
             sum(p["total_score"] for p in probs)))
    print("题型分布：" + "、".join("%s %d" % (k, v) for k, v in sorted(by_type.items())))

    bad = _sanity(probs)
    if bad:
        print("★ 自检不通过：")
        for b in bad:
            print("   " + b)
        return 1
    print("自检通过 ✅")

    if args.check:
        return 0

    OUT_PATH.write_text(_dump(probs), encoding="utf-8", newline="\n")
    print("已写入 %s（%d 字节）" % (OUT_PATH, OUT_PATH.stat().st_size))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
