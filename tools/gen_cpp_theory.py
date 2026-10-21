#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""C++ 基础线理论题库生成器（第 01 ~ 06 讲：单选 / 多选 / 判断 / 填空 / 简答）。

    python tools/gen_cpp_theory.py [--check]

为什么答案要「跑」而不是「写」
------------------------------
C++ 理论题里有一大半是**可实证的事实**：「这段代码输出什么」「sizeof 是多少」
「优先级 / 类型转换之后是什么值」「构造析构的先后顺序」…… 手算三五道还行，
连着写五十道必然出错，而且错得极隐蔽：题面、选项、解析三处会一起错，学生反而被教错。

所以规矩是：**凡是有输出的，一律用 `tools/cpp_eval.py::run_cpp` 真编译真运行取结果**，
再拿结果去选项里找字母（找不到、或找到多个，生成器直接中止）。
纯概念题（「析构函数能不能重载」「友元是否传递」）算不了，走 `mcp/tfn/multn`，
按讲义口径判定，源码里标了「无计算」。

    out = cpp(SRC)                 # g++ 真跑，比如 "3 -3 -1"
    options=[...]                  # 造干扰项
    mcn(..., value=out)            # 答案字母由 out 在 options 里的位置反推

★ 口径提醒（讲义原文，出题不得凭记忆）
- 8 位补码范围 [-128, 127]，负数比正数多一个；
- 整数除法向零取整（-7/2 = -3），`%` 的符号跟**被除数**（-7%2 = -1）；
- 数组形参退化为指针，64 位平台函数内 `sizeof(a)` 是 8；
- 构造顺序看**成员声明顺序**，与初始化列表书写顺序无关；析构严格倒放；
- 复制构造三大时机 = 初始化对象 / 传值传参 / 传值返回，
  验证要加 `-fno-elide-constructors`（否则返回值那次被拷贝消除吃掉）。
"""
from __future__ import annotations

import argparse
import itertools
import json
import re
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

from app.bank_kit import fill, mc, multi, tf          # noqa: E402
from cpp_eval import run_cpp                          # noqa: E402

OUT_PATH = ROOT / "app" / "problems_bank_cpp_theory.py"

HEADER = '''"""C++ 基础线理论题库 —— **自动生成，不要手改**。

本文件由 `tools/gen_cpp_theory.py` 产出，重新生成：

    python tools/gen_cpp_theory.py

题源
----
《C++ 语言程序设计》第 01 ~ 06 讲（绪论 / 简单程序设计 / 函数 / 类与对象 /
数据的共享与保护 / 数组指针与字符串），按讲分节，共 111 道**理论题**
（`line = "text"`，`subject = "cpp"`），提交的答案文本由 `oneof` checker 比对。

答案可信度
----------
凡是「这段代码输出什么」「sizeof 是多少」「构造析构的先后」这类题，
答案都由生成器调用 `tools/cpp_eval.py::run_cpp`（g++ 真编译真运行）取得，
再反推选项字母，不手写；算不出唯一选项时生成器直接中止。
纯概念题在生成器里标了「无计算」，按讲义口径判定。
"""
from __future__ import annotations

CPP_THEORY_PROBLEMS: list[dict] = '''


PROBS: list[dict] = []
_SEEN: set[str] = set()

# ★ 理论题分讲计划。加上各讲的编程题（02/03/04/06 各 2 道、05 有 1 道）后，
#   每讲的**总题数**都是 20；改题量时两边一起核。
SECTION_COUNTS = {
    "第 01 讲 · 绪论": 20,          # + 编程 0 = 20
    "第 02 讲 · C++ 简单程序设计": 18,   # + 编程 2 = 20
    "第 03 讲 · 函数": 18,          # + 编程 2 = 20
    "第 04 讲 · 类与对象": 18,       # + 编程 2 = 20
    "第 05 讲 · 数据的共享与保护": 19,   # + 编程 1 = 20
    "第 06 讲 · 数组指针与字符串": 18,   # + 编程 2 = 20
}


def _push(p: dict) -> dict:
    t = p["title"]
    if t in _SEEN:
        raise SystemExit("★ 标题重复：%s" % t)
    _SEEN.add(t)
    PROBS.append(p)
    return p


def cpp(src: str, flags: str = "-std=c++17") -> str:
    """真编译真运行 —— 所有「输出是什么」的答案都从这里来。"""
    return run_cpp(textwrap.dedent(src).strip() + "\n", std_flags=flags)


def _stmt(intro: str, src: str, tail: str = "") -> str:
    """题面 + cpp 代码围栏。"""
    body = textwrap.dedent(src).strip()
    return intro + "\n\n```cpp\n" + body + "\n```" + tail


# ★ 选项轮转
#   出题时习惯把正确项写在第一个，结果 30 道单选的答案全是 A —— 学生闭眼选 A 就能过。
#   所以统一做一次**固定轮转**：正确项的目标位置按 0,1,2,3 循环，选项整体左移 rot 位，
#   解析里的选项字母引用同步左移（`_shift_letters`），保证「B 是……」永远指向原来那个干扰项。
#   轮转是确定性的：同样的源码永远生成同样的模块（--check 幂等靠这个）。
_LETTER_RE = re.compile(r"(?<![A-Za-z0-9+])[A-H](?![A-Za-z0-9+])")
_SLOT_CYCLE = itertools.cycle([0, 1, 2, 3])


def _shift_letters(text: str, rot: int, n: int) -> str:
    """选项左移 rot 位后，把解析里的 A~H 引用按同一规则重映射。

    只重映射落在本题选项范围内的字母（n 个）；`G`/`F` 这类当函数名的、以及
    `C++` 里的 C 都不会被误改（前者超出范围、后者被 lookahead 挡住）。
    """
    if rot % n == 0:
        return text

    def rep(m: "re.Match[str]") -> str:
        i = ord(m.group(0)) - ord("A")
        if i >= n:
            return m.group(0)
        return chr(ord("A") + (i - rot) % n)

    return _LETTER_RE.sub(rep, text)


def _rotate(options: list[str], rot: int) -> list[str]:
    n = len(options)
    rot %= n
    return options[rot:] + options[:rot] if rot else list(options)


# =========================================================================
# 构造器
# =========================================================================
def mcn(*, title: str, stmt: str, options: list[str], value, section: str,
        expl: str, tags: list[str], diff: int = 2,
        rot: int | None = None) -> dict:
    """单选（**算出来的**）：`value` 必须恰好命中一个选项。

    `rot` 一般留空 —— 由 `_SLOT_CYCLE` 决定正确项的落位，再把选项整体左移；
    极少数解析里含「C++」「C 串」这类会与选项字母撞车的文本，显式传 `rot=0`。
    """
    want = str(value)
    if options.count(want) != 1:
        raise SystemExit("★ %s：算得 %r，选项里命中 %d 次"
                         % (title, want, options.count(want)))
    n = len(options)
    if rot is None:
        rot = (options.index(want) - next(_SLOT_CYCLE)) % n
    if rot % n:
        options = _rotate(options, rot)
        expl = _shift_letters(expl, rot, n)
    return _push(mc(title, stmt, options, "ABCDEFGH"[options.index(want)],
                    subject="cpp", section=section, explanation=expl,
                    tags=tags, difficulty=diff))


def mcp(*, title: str, stmt: str, options: list[str], answer: str,
        section: str, expl: str, tags: list[str], diff: int = 2,
        rot: int = 0) -> dict:
    """单选（**无计算**，纯概念，讲义口径；`rot` 同 `mcn`，默认不轮转）。"""
    n = len(options)
    if rot % n:
        options = _rotate(options, rot)
        expl = _shift_letters(expl, rot, n)
        answer = chr(ord("A") + (ord(answer.upper()) - ord("A") - rot) % n)
    return _push(mc(title, stmt, options, answer, subject="cpp", section=section,
                    explanation=expl, tags=tags, difficulty=diff))


def tfc(*, title: str, stmt: str, cond: bool, section: str, expl: str,
        tags: list[str], diff: int = 2) -> dict:
    """判断（**算出来的**）：`cond` 是「题干这句话是否成立」的真值。"""
    return _push(tf(title, stmt, cond, subject="cpp", section=section,
                    explanation=expl, tags=tags, difficulty=diff))


def tfn(*, title: str, stmt: str, answer: bool, section: str, expl: str,
        tags: list[str], diff: int = 2) -> dict:
    """判断（**无计算**，纯概念）。"""
    return _push(tf(title, stmt, answer, subject="cpp", section=section,
                    explanation=expl, tags=tags, difficulty=diff))


def fillc(*, title: str, stmt: str, value, section: str, expl: str,
          tags: list[str], diff: int = 2, extra: list[str] | None = None) -> dict:
    """填空（**算出来的**）：答案就是跑出来的那个值。"""
    ans = str(value)
    return _push(fill(title, stmt, [ans] + list(extra or []), subject="cpp",
                      section=section, explanation=expl, tags=tags,
                      difficulty=diff))


def multn(*, title: str, stmt: str, options: list[str], answers: list[str],
          section: str, expl: str, tags: list[str], diff: int = 3,
          rot: int = 0) -> dict:
    """多选（**无计算**，纯概念；选项两两互斥、由讲义口径判定）。

    `rot` 与单选同义：选项左移 rot 位，正确答案字母与解析里的字母引用一起左移。
    """
    n = len(options)
    if rot % n:
        options = _rotate(options, rot)
        expl = _shift_letters(expl, rot, n)
        answers = [chr(ord("A") + (ord(a.upper()) - ord("A") - rot) % n)
                   for a in answers]
    return _push(multi(title, stmt, options, answers, subject="cpp",
                       section=section, explanation=expl, tags=tags,
                       difficulty=diff))


def shortq(*, title: str, statement_md: str, answers: list[str], section: str,
           explanation: str, tags: list[str], difficulty: int = 3) -> dict:
    """简答（无计算；`oneof` 比文本，答案列常见等价说法）。"""
    p = fill(title, statement_md, answers, subject="cpp", section=section,
             explanation=explanation, tags=tags, difficulty=difficulty,
             total_score=12)
    p["question_type"] = "short_answer"
    p["output_format"] = "一句话作答（不要写解释、不要抄题目）"
    return _push(p)


# =========================================================================
# 第 01 讲 · 绪论（6 题）
# =========================================================================
_S = "第 01 讲 · 绪论"

mcn(title="8 位补码下 -5 的位模式",
    stmt=_stmt("在 64 位平台上，下面程序输出的 8 位位模式是什么？", '''
        #include <bitset>
        #include <iostream>

        int main() {
            int x = -5;
            std::cout << std::bitset<8>((unsigned char)x) << std::endl;
        }
    '''),
    options=["10000101", "11111010", "11111011", "11110101"],
    value=cpp('''
        #include <bitset>
        #include <iostream>
        int main() {
            int x = -5;
            std::cout << std::bitset<8>((unsigned char)x) << std::endl;
        }
    '''),
    section=_S,
    expl="负数的补码 = **反码 + 1**：-5 的原码 `1000 0101`、反码 `1111 1010`、"
         "补码 `1111 1011`。\n"
         "A 是**原码**（把「符号位 + 绝对值」当成补码，最典型的错法）；"
         "B 停在**反码**上，忘了加 1；D 是随手写错的位型，没有任何编码规则对得上。\n"
         "自检办法：`~5 + 1 == -5`（实测成立）。内存里存的永远是补码。",
    tags=["补码", "位模式"], diff=1)

tfn(title="汇编语言属于高级语言吗",
    stmt="汇编语言用助记符代替了二进制指令，所以它属于**高级语言**。",
    answer=False, section=_S,
    expl="错。语言发展的分水岭是「离机器多远」：机器语言 → 汇编语言 → 高级语言 → "
         "面向对象语言，**前两个都是面向机器的低级语言**。\n"
         "汇编仍然一条指令对应一条机器指令、绑定具体 CPU；高级语言（C/C++/Java）"
         "与机器无关，必须经编译或解释翻译后才能执行。",
    tags=["语言分类", "低级语言"], diff=1)

_TB = cpp('''
    #include <iostream>
    int main() {
        std::cout << (1LL << 40) << std::endl;
    }
''')
mcn(title="1 TB 等于多少字节",
    stmt="按教材口径，存储单位之间**逐级 ×1024**。下面程序算出了 1 TB 的字节数：\n\n"
         "```cpp\n"
         "#include <iostream>\n\n"
         "int main() {\n"
         "    std::cout << (1LL << 40) << std::endl;\n"
         "}\n"
         "```\n\n"
         "它的输出是多少？",
    options=["1000000000000", _TB, "1073741824", "1048576"],
    value=_TB, section=_S,
    expl="1 TB = 1024 GB = 1024² MB = 1024³ KB = 1024⁴ 字节 = 2⁴⁰ 字节 = **1099511627776**。\n"
         "`1000000000000` 是 1000 进制的厂商标称，教材与考试一律按 1024；"
         "`1073741824` 是 2³⁰（1 GB）；`1048576` 是 2²⁰（1 MB）—— 两者都是「少算了一级」。",
    tags=["存储单位", "容量换算"], diff=2)

mcn(title="hex 操纵符输出的十六进制数",
    stmt=_stmt("下面程序的输出是什么？", '''
        #include <iostream>

        int main() {
            std::cout << std::hex << 32 << std::endl;
        }
    '''),
    options=["20", "32", "2", "50"],
    value=cpp('''
        #include <iostream>
        int main() { std::cout << std::hex << 32 << std::endl; }
    '''),
    section=_S,
    expl="32 = 2×16 + 0，十六进制写作 `20`。\n"
         "`hex` 是**持久**的流操纵符：一旦设置，后续所有整数都按十六进制输出"
         "（与 `setw` 只管下一个输出项正好相反）。\n"
         "B 是没看出 hex 生效、仍按十进制读；C 只取了商 2；D 是按八进制算错（32 的八进制是 40）。",
    tags=["流操纵符", "进制输出"], diff=2)

mcp(title="编译方式与解释方式的区别", answer="B",
    stmt="关于**编译方式**与**解释方式**，下列说法正确的是：",
    options=[
        "编译方式逐句翻译、逐句执行，不生成目标程序",
        "编译方式把整个源程序一次性翻译成目标程序，再连接成可执行文件",
        "解释方式先生成目标程序，再由机器直接执行",
        "编译方式和解释方式都必须生成目标程序",
    ],
    section=_S,
    expl="B 正确：编译**一次性整体翻译**并**生成**目标程序（.cpp → .o → 连接 → .exe），"
         "之后运行不再需要源代码 —— C++ 走的就是这条路。\n"
         "A 把编译说成了「逐句执行」，那是解释方式；"
         "C 同样说反（解释逐句翻译逐句执行，**不生成**目标程序）；"
         "D 错在「都生成」：解释方式恰恰不生成目标程序。\n"
         "★ 记两条就够：**翻译时机**（整体 / 逐句）与**是否生成目标程序**（是 / 否）。",
    tags=["编译", "解释"], diff=3, rot=0)

fillc(title="8 位补码能表示的最小整数",
      stmt=_stmt("8 位补码能表示的整数范围并不对称。下面程序把它的**下界**打了出来，"
                 "这个下界是多少？\n\n"
                 "（`(signed char)128` 越过上界后按补码回绕）", '''
        #include <iostream>

        int main() {
            signed char c = (signed char)128;
            std::cout << (int)c << std::endl;
        }
    '''),
      value=cpp('''
        #include <iostream>
        int main() {
            signed char c = (signed char)128;
            std::cout << (int)c << std::endl;
        }
    '''),
      section=_S,
      expl="127 的位型 `0111 1111` 加 1 得 `1000 0000`。这个位型**没有对应的正数**"
           "（按原码解释是 -0），被规定为 **-128** —— 这正是「负数比正数多一个」的来源。\n"
           "填 -127 是把范围错记成对称的 `[-127, 127]`（最常见的错法）；"
           "-129 超出了 8 位能表示的边界；128 是正数侧越界，装不进去。\n"
           "★ 公式记死：n 位补码范围 `[-2^(n-1), 2^(n-1)-1]`，负端多一个。",
      tags=["补码", "表示范围"], diff=4)

# ---- 以下为 2026-10 扩充：01 讲补到 20 题（新增 14 道，难度 2→4）----

mcn(title="十进制 25 的八进制与十六进制输出",
    stmt=_stmt("下面程序先把输出切到八进制、再切到十六进制，打印同一个十进制数 25。"
               "输出是什么？", '''
        #include <iostream>

        int main() {
            std::cout << std::oct << 25 << " " << std::hex << 25 << std::endl;
        }
    '''),
    options=["31 19", "25 25", "31 25", "19 31"],
    value=cpp('''
        #include <iostream>
        int main() {
            std::cout << std::oct << 25 << " " << std::hex << 25 << std::endl;
        }
    '''),
    section=_S,
    expl="25 = 16 + 9 → 十六进制 **19**；25 = 3×8 + 1 → 八进制 **31**。\n"
         "换算的底层依据是分组：25 的二进制是 `11001`，八进制**三位一组**从右往左\n"
         "`011 001` → 3、1 → 31；十六进制**四位一组** `0001 1001` → 1、9 → 19。\n"
         "B 是以为操纵符不生效、两个都按十进制打；C 只认出了八进制（十六进制那半还按十进制）；\n"
         "D 把两种进制对调了 —— 19 是十六进制、31 才是八进制。\n"
         "★ `oct`/`hex` 是**持久**操纵符，一旦设置后续整数全按它输出，切回来要显式写 `dec`。",
    tags=["进制转换", "流操纵符"], diff=2)

mcn(title="8 位补码下 -1 的位模式",
    stmt=_stmt("在 64 位平台上，下面程序打印 -1 的低 8 位。输出是什么？", '''
        #include <bitset>
        #include <iostream>

        int main() {
            std::cout << std::bitset<8>((unsigned char)-1) << std::endl;
        }
    '''),
    options=["11111111", "10000001", "10000000", "11111110"],
    value=cpp('''
        #include <bitset>
        #include <iostream>
        int main() {
            std::cout << std::bitset<8>((unsigned char)-1) << std::endl;
        }
    '''),
    section=_S,
    expl="-1 的补码是 8 位**全 1** `11111111`。按「反码 + 1」验算：原码 `1000 0001` →\n"
         "反码 `1111 1110` → 加 1 得 `1111 1111`。更快的验算：`-1 = 0 - 1`，\n"
         "`0000 0000` 减 1 逐位借位，正好借成 8 个 1。\n"
         "B 是**原码**（符号位加绝对值 1）—— 最经典的错法；C 是 -128 的位模式；\n"
         "D 停在**反码**上忘了加 1（`1111 1110` 实际是 -2 的补码）。",
    tags=["补码", "位模式"], diff=2)

mcn(title="0.1 加 0.2 与 0.3 的判等",
    stmt=_stmt("下面程序先打印判等结果，再打印两数之和。输出是什么？", '''
        #include <iostream>

        int main() {
            std::cout << (0.1 + 0.2 == 0.3) << " " << 0.1 + 0.2 << std::endl;
        }
    '''),
    options=["0 0.3", "1 0.3", "0 0.30000000000000004", "1 0.30000000000000004"],
    value=cpp('''
        #include <iostream>
        int main() {
            std::cout << (0.1 + 0.2 == 0.3) << " " << 0.1 + 0.2 << std::endl;
        }
    '''),
    section=_S,
    expl="输出 `0 0.3`：判等为 **false（0）**，可打印出来却是 0.3。\n"
         "原因是 0.1、0.2、0.3 在二进制里都是**无限循环小数**，存进 double 时已被截断，\n"
         "两份舍入误差加起来不等于第三份 —— 内部位模式不同。而 `cout` 默认只打 6 位有效数字，\n"
         "把 0.30000000000000004 显示成了 0.3。\n"
         "B 是只看打印值就以为相等；C 以为默认会打 17 位（那要 `setprecision(17)`）；\n"
         "D 两处都错。★ 浮点判等必须写 `fabs(a - b) < 1e-6` 这类误差范围。",
    tags=["浮点数", "精度"], diff=2)

fillc(title="float 与 double 各占多少字节",
      stmt=_stmt("在 64 位平台上，下面程序打印 float 与 double 的宽度。输出是什么？", '''
        #include <iostream>

        int main() {
            std::cout << sizeof(float) << " " << sizeof(double) << std::endl;
        }
    '''),
      value=cpp('''
        #include <iostream>
        int main() {
            std::cout << sizeof(float) << " " << sizeof(double) << std::endl;
        }
    '''),
      section=_S,
      expl="IEEE 754 规定：float **32 位 = 4 字节**（约 7 位有效数字），\n"
           "double **64 位 = 8 字节**（约 15~16 位有效数字）→ `4 8`。\n"
           "填 `8 16` 是把「位数」当成了「字节数」；填 `4 4` 是以为两者同宽；\n"
           "填 `2 4` 是把它当成了 16 位/32 位时代的老机器。\n"
           "★ 浮点与定点的分工：定点数小数点位置固定，范围小但精确；浮点数用「阶码 + 尾数」，\n"
           "**范围大而精度有限** —— 上面 0.1+0.2 那道题就是「精度有限」的直接后果。",
      tags=["浮点数", "sizeof 运算"], diff=2)

mcn(title="字符按 ASCII 码值参与算术运算", rot=0,
    stmt=_stmt("下面程序输出什么？", '''
        #include <iostream>

        int main() {
            std::cout << ('D' - 'A') << " " << (char)('A' + 4) << std::endl;
        }
    '''),
    options=["3 69", "68 65", "3 E", "4 E"],
    value=cpp('''
        #include <iostream>
        int main() {
            std::cout << ('D' - 'A') << " " << (char)('A' + 4) << std::endl;
        }
    '''),
    section=_S,
    expl="字符一进算术表达式就**按 ASCII 码值**参与：'A'=65、'D'=68，\n"
         "所以 `'D' - 'A'` = 68 − 65 = **3**；`'A' + 4` = 69，强制转回 char 就是 **'E'**。\n"
         "A 忘了把 69 转回字符，直接把码值打了出来；B 打印的是两个字符本身的码值；\n"
         "D 把差值算成了 4（那是 'E' 与 'A' 的差）。\n"
         "★ 四个锚点记住：'A'=65、'a'=97（差 32）、'0'=48、空格=32；\n"
         "大小写转换公式 `c - 'a' + 'A'` 就是这条性质的应用。",
    tags=["ASCII", "字符运算"], diff=2)

# 无计算：概念题，按讲义口径判定（不跑代码）
mcp(title="程序设计语言四个发展阶段的先后", answer="C",
    stmt="按「离机器由近到远」的顺序，程序设计语言的四个发展阶段依次是：",
    options=[
        "汇编语言 → 机器语言 → 高级语言 → 面向对象语言",
        "机器语言 → 高级语言 → 汇编语言 → 面向对象语言",
        "机器语言 → 汇编语言 → 高级语言 → 面向对象语言",
        "高级语言 → 机器语言 → 汇编语言 → 面向对象语言",
    ],
    section=_S,
    expl="C。分水岭只有一条：**离机器多远**。机器语言是 0/1 指令序列，汇编用助记符但仍一条\n"
         "指令对一条机器指令、绑定具体 CPU —— **前两个都是面向机器的低级语言**；\n"
         "高级语言（C/C++/Java）与机器无关，必须经编译或解释翻译后才能执行；\n"
         "面向对象语言再进一步，直接以「对象」为基本单位组织程序。\n"
         "A 把机器语言与汇编对调；B 把高级语言插到了汇编前面；D 整个倒过来了。\n"
         "★ 常见误区：以为「汇编有助记符、比 0/1 好写」就算高级语言 —— 判据是**是否与机器无关**。",
    tags=["语言分类", "低级语言"], diff=2)

mcn(title="按位取反得到的是反码还是补码",
    stmt=_stmt("下面程序把 5 按位取反后打印低 8 位。输出是什么？", '''
        #include <bitset>
        #include <iostream>

        int main() {
            std::cout << std::bitset<8>((unsigned char)(~5)) << std::endl;
        }
    '''),
    options=["11111010", "11111011", "00000101", "10000101"],
    value=cpp('''
        #include <bitset>
        #include <iostream>
        int main() {
            std::cout << std::bitset<8>((unsigned char)(~5)) << std::endl;
        }
    '''),
    section=_S,
    expl="5 的 8 位形态是 `0000 0101`，`~5` 逐位取反得 **`1111 1010`** —— 这正是 -5 的**反码**。\n"
         "补码还要再加 1 才是 `1111 1011`，所以 `~5` 的值是 **-6** 而不是 -5；\n"
         "`~5 + 1` 才等于 -5（讲义里的自检式）。\n"
         "B 是补码，少了「加 1」这一步 —— 把取反直接当成了求相反数；\n"
         "C 是 5 本身（以为取反没生效）；D 是原码。\n"
         "★ 三套编码的关系一句话：**反码 = 原码除符号位取反，补码 = 反码 + 1**；\n"
         "内存里存的、加法器算的，永远都是补码。",
    tags=["补码", "反码", "位运算"], diff=3)

fillc(title="int 上界加一之后的值",
      stmt=_stmt("32 位 int 的上界是 2147483647。下面程序把它加 1 再打印，输出是什么？", '''
        #include <climits>
        #include <iostream>

        int main() {
            std::cout << INT_MAX + 1 << std::endl;
        }
    '''),
      value=cpp('''
        #include <climits>
        #include <iostream>
        int main() {
            std::cout << INT_MAX + 1 << std::endl;
        }
    '''),
      section=_S,
      expl="`INT_MAX` = 2147483647 = 2³¹ − 1，位模式 `0111...1111`；加 1 进位成 `1000...0000`，\n"
           "按补码解释就是 **-2147483648**（即 -2³¹）。所以 32 位 int 的范围是\n"
           "**[−2147483648, 2147483647]**，负端比正端多一个 —— 与 8 位 char 的 [-128,127] 同一个道理。\n"
           "填 2147483648 是把它当成无符号数（那需要 unsigned 或 long long）；\n"
           "填 0 是只看到「溢出」没算位模式；填 -2147483647 是少减了一位。\n"
           "★ 溢出是**运行期行为**：g++ 只给 `warning: integer overflow [-Woverflow]`，\n"
           "编译照样通过 —— 「能编译」不等于「没溢出」。",
      tags=["表示范围", "整数溢出"], diff=3)

fillc(title="2 TB 硬盘的字节数",
      stmt="按教材口径，存储单位逐级 ×1024。下面程序算出 2 TB 的字节数，输出是什么？\n\n"
           "```cpp\n"
           "#include <iostream>\n\n"
           "int main() {\n"
           "    std::cout << (2LL << 40) << std::endl;\n"
           "}\n"
           "```",
      value=cpp('''
        #include <iostream>
        int main() { std::cout << (2LL << 40) << std::endl; }
    '''),
      section=_S,
      expl="1 TB = 2¹⁰ GB = 2²⁰ MB = 2³⁰ KB = 2⁴⁰ B，所以 2 TB = **2⁴¹ = 2199023255552** 字节。\n"
           "填 2000000000000 是用了 1000 进制（那是厂商标称口径，教材与考试一律 1024）；\n"
           "填 1099511627776 是 1 TB（少乘 2）；填 4294967296 是 2³² = 4 GB。\n"
           "★ 顺带一个边界：这个数已经超过 int 上限（约 2.1×10⁹），必须用 `long long`；\n"
           "`2 << 40` 里左操作数是 int，会先溢出 —— 写成 `2LL` 才安全。",
      tags=["存储单位", "容量换算"], diff=3)

fillc(title="UTF-8 下一个汉字占用的字节数",
      stmt=_stmt("下面程序打印一个汉字的 UTF-8 编码长度（已减去结尾符）。输出是什么？", '''
        #include <iostream>

        int main() {
            std::cout << sizeof(u8"中") - 1 << std::endl;
        }
    '''),
      value=cpp('''
        #include <iostream>
        int main() { std::cout << sizeof(u8"中") - 1 << std::endl; }
    '''),
      section=_S,
      expl="UTF-8 是**变长**编码：ASCII 字符 1 字节，常用汉字 **3 字节**，所以字符本身占 3。\n"
           "`sizeof(u8\"中\")` 是 4 —— 字符串字面量还要带一个结尾 `'\\0'`，减 1 才是字符本身的长度。\n"
           "填 2 是套用了 **GB2312/GBK** 的口径（那里面汉字固定 2 字节）；填 1 是当成 ASCII；\n"
           "填 4 是忘了减结尾符。\n"
           "★ 「一个汉字占几字节」没有唯一答案，取决于**编码**：GBK 2 字节、UTF-8 3 字节、\n"
           "UTF-16 2 字节。答题先看题目说的是哪种编码。",
      tags=["汉字编码", "UTF-8"], diff=3)

# 无计算：概念题，按讲义口径判定（不跑代码）
multn(title="面向对象基本概念的四项辨析",
      stmt="关于面向对象的基本概念，下列说法正确的有：",
      options=[
          "对象是描述客观事物的实体，由一组属性和一组操作组成",
          "类是同类对象的抽象，对象是类的实例",
          "封装把数据和操作捆成一个独立单位，并尽可能隐蔽内部细节",
          "多态是教材 1.2 节与对象、类、封装并列展开的第四个基本概念",
          "继承让派生类自动拥有基类的属性与操作，主要解决可重用性",
      ],
      answers=["A", "B", "C", "E"], section=_S,
      expl="A 对：属性是静态的数据、操作是动态的行为，两者合起来才是一个对象。\n"
           "B 对：**类是模板、对象是产品**，先定义类才能创建对象 —— 顺序不能反。\n"
           "C 对：封装 = 信息隐藏 + 接口暴露，藏起细节的目的恰恰是给出一个更安全的接口，\n"
           "不是「把成员全藏起来就完事」。\n"
           "D 错：教材 1.2 节只展开**对象、类、封装、继承**四个概念，**多态在第 8 章**才正式登场。\n"
           "E 对：派生类自动获得基类的属性与操作，不必重写 —— 这就是可重用性。\n"
           "★ 概念判断题最爱在这里挖坑：把「五大特征」硬套到 1.2 节。",
      tags=["面向对象", "封装与继承", "多选"], diff=3)

# 无计算：概念题，按讲义口径判定（不跑代码）
mcp(title="OOA 与 OOD 在开发过程中的位置", answer="A", rot=3,
    stmt="面向对象的软件开发分 OOA → OOD → OOP → OOT → OOSM 五步。下列关于 OOA 与 OOD 的说法正确的是：",
    options=[
        "OOA 从问题域识别对象和类、建立需求模型，OOD 再为它补充实现细节",
        "OOA 直接编写代码，OOD 负责以类为单元做测试",
        "OOD 排在 OOA 之前：先设计类结构，再回头分析需求",
        "OOA 与 OOD 是同一个阶段的两个名字，只是叫法不同",
    ],
    section=_S,
    expl="A。五步的职责：**OOA 分析**（识别对象和类、建需求模型）→ **OOD 设计**（加实现细节：\n"
         "类结构、交互）→ **OOP 编程**（落地写代码）→ **OOT 测试**（以类为基本单元）→\n"
         "**OOSM 维护**（封装让改动局部化）。口诀：分析找对象，设计搭结构，编程写代码，\n"
         "测试按类测，维护靠封装。\n"
         "B 把 OOP 和 OOT 的活儿安到了前两步上；C 顺序反了（先分析后设计，不能倒）；\n"
         "D 抹掉了两个阶段的边界。\n"
         "★ 考试只考「哪个阶段干什么」和「谁在前」，不必背整段定义。",
    tags=["软件生命周期", "OOA/OOD"], diff=3)

# 无计算：概念题，按讲义口径判定（不跑代码）
mcp(title="源程序到可执行文件的三个环节", answer="A", rot=2,
    stmt="关于从源程序到可执行文件的过程，下列说法正确的是：",
    options=[
        "编译把 .cpp 整体翻译成目标文件，连接再把目标文件与所需库拼成可执行文件",
        "连接把 .cpp 翻译成目标文件，编译再把库拼进去",
        "源程序经编译就直接得到可执行文件，不需要连接这一步",
        "目标程序仍是文本形式，只有可执行文件才是机器码",
    ],
    section=_S,
    expl="A。链条是：**源程序（.cpp，文本）→ 编译 → 目标程序（.o/.obj，机器码碎片）\n"
         "→ 连接（与库函数拼合）→ 可执行文件（.exe）**。\n"
         "B 把编译与连接的职责对调；C 漏掉了连接 —— 自己写的代码一句没错却报\n"
         "`undefined reference`，出事的正是这一步（符号找不到定义）；\n"
         "D 说反了：目标程序已经是机器码，只是还缺库函数、还不能独立运行。\n"
         "★ 两条链一起记：**预处理 → 编译 → 连接 → 运行**；\n"
         "`#` 开头的活在预处理阶段干完，编译器根本看不到被 `#ifdef` 裁掉的行。",
    tags=["编译", "连接"], diff=3)

# 无计算：概念题，按讲义口径判定（不跑代码）
multn(title="C++11/14 对初学者的四个改进",
      stmt="关于 C++11/14 引入的现代写法，下列说法正确的有：",
      options=[
          "constexpr 让常量表达式在编译期求值，结果可以直接当数组长度",
          "auto 按初值推断类型，但 auto s = \"hello\"; 推出的 s 是 const char* 而不是 string",
          "范围 for 让我们不用下标就能遍历数组或容器",
          "C++11 起取消了宏，#define 不再是合法的预处理命令",
          "nullptr 是类型安全的空指针，不会像 NULL 那样被当成整数 0",
      ],
      answers=["A", "B", "C", "E"], section=_S,
      expl="A 对：`constexpr int N = 7*7; int a[N];` 能编译 —— 编译器在编译期就把 49 算完了；\n"
           "`const` 只承诺「运行期不改」，值可能是运行时才知道的，所以不能当数组长度。\n"
           "B 对：字符串字面量的类型是 `const char*`（实测 typeid 名 `PKc`），没有 `.length()`；\n"
           "想要 string 得写 `string s = \"hello\";`。\n"
           "C 对：`for (int v : a)` 逐元素遍历，连长度都不用问；只读时写 `const auto &`。\n"
           "D 错：宏与条件编译**照旧合法**，C++11 只是给了更好的替代品（constexpr 替宏常量、\n"
           "inline 函数替宏函数、using 替 typedef）—— `#ifdef` 至今仍是调试开关的标准做法。\n"
           "E 对：`NULL` 本质是 0，传给重载函数可能选中 int 版；`nullptr` 是专属的空指针类型。\n"
           "★ 现代写法的统一哲学：**让编译器知道你的意图**，而不是让它猜。",
      tags=["C++11/14", "现代 C++", "多选"], diff=4)

# =========================================================================
# 第 02 讲 · C++ 简单程序设计（18 题）
# =========================================================================
_S = "第 02 讲 · C++ 简单程序设计"

mcn(title="整数除法与取余的符号",
    stmt=_stmt("下面程序的输出是什么？", '''
        #include <iostream>

        int main() {
            std::cout << 7 / 2 << " " << -7 / 2 << " " << -7 % 2 << std::endl;
        }
    '''),
    options=["3 -3 -1", "3 -4 -1", "3.5 -3.5 -1", "3 -3 1"],
    value=cpp('''
        #include <iostream>
        int main() {
            std::cout << 7 / 2 << " " << -7 / 2 << " " << -7 % 2 << std::endl;
        }
    '''),
    section=_S,
    expl="两个 int 相除结果还是 int，小数部分**截断**；C++11 起规定**向零取整**，"
         "所以 -7/2 是 -3（不是 -4）。`%` 的结果符号跟**被除数**，-7%2 = -1。\n"
         "B 是「向负无穷取整」的误解（Python 的 `//` 才是那样）；"
         "C 把整数除法当成了浮点除法；D 把余数符号错记成跟除数。",
    tags=["整数除法", "取余"], diff=1)

mcn(title="混合类型表达式的求值结果",
    stmt=_stmt("下面程序的输出是什么？", '''
        #include <iostream>

        int main() {
            int a = 5, b = 2;
            std::cout << a / b << " " << a % b << " " << 1.0 * a / b << std::endl;
        }
    '''),
    options=["2 1 2.5", "2.5 1 2.5", "2 1 2", "2.5 1 2"],
    value=cpp('''
        #include <iostream>
        int main() {
            int a = 5, b = 2;
            std::cout << a / b << " " << a % b << " " << 1.0 * a / b << std::endl;
        }
    '''),
    section=_S,
    expl="`a / b` 两边都是 int → **2**（小数被砍掉）；`a % b` → **1**；"
         "`1.0 * a / b` 先算 `1.0 * 5` 得到 double 临时量 5.0，再除以 2 → **2.5**。\n"
         "配一个 1.0 就能把整条表达式提升成浮点，这是 `1.0*a/b` 这个惯用法的由来。\n"
         "B 以为 `a/b` 也自动提升；C 漏了提升（得到 2）；D 两处都错。",
    tags=["类型转换", "整数除法"], diff=1)

tfc(title="signed 与 unsigned 混算比较",
    stmt=_stmt("**判断**：下面程序输出的 `a < u` 结果为 `true`。", '''
        #include <iostream>

        int main() {
            int a = -1;
            unsigned u = 1;
            std::cout << std::boolalpha << (a < u) << std::endl;
        }
    '''),
    cond=(cpp('''
        #include <iostream>
        int main() {
            int a = -1;
            unsigned u = 1;
            std::cout << std::boolalpha << (a < u) << std::endl;
        }
    ''') == "true"),
    section=_S,
    expl="**错**。int 与 unsigned 一起运算时，int 会先转成 unsigned：-1 变成 "
         "4294967295（2³²-1），于是 `-1 < 1u` 判为 **false**。\n"
         "g++ 会给 `-Wsign-compare` 警告，但照常编译 —— 这类题绝不能靠「负数当然小于正数」的直觉。\n"
         "正确姿势：别让 unsigned 参与带符号运算；见到 -Wsign-compare 就停手。",
    tags=["无符号数", "类型转换"], diff=2)

mcn(title="后置自增与前置自增的取值",
    stmt=_stmt("下面程序的输出是什么？", '''
        #include <iostream>

        int main() {
            int i = 3;
            int v1 = i++;          // 先取值，后自增
            int j = 3;
            int v2 = ++j;          // 先自增，后取值
            std::cout << v1 << " " << i << " " << v2 << " " << j << std::endl;
        }
    '''),
    options=["3 4 4 4", "4 4 4 4", "3 3 4 4", "3 4 3 4"],
    value=cpp('''
        #include <iostream>
        int main() {
            int i = 3;
            int v1 = i++;
            int j = 3;
            int v2 = ++j;
            std::cout << v1 << " " << i << " " << v2 << " " << j << std::endl;
        }
    '''),
    section=_S,
    expl="`i++` 是**后置**：先把 3 赋给 v1，再自增 → v1=3、i=4；"
         "`++j` 是**前置**：先自增到 4，再把 4 赋给 v2 → v2=4、j=4。\n"
         "B 把后置也当成先加；C 以为后置自增不改变 i；D 把前置/后置的效果对调了。\n"
         "★ 单独写 `i++;` 时两者等价，**只有取值时才分家**。",
    tags=["自增", "副作用"], diff=2)

mcn(title="do-while 至少执行一次",
    stmt=_stmt("下面程序输出什么？", '''
        #include <iostream>

        int main() {
            int n = 0;
            int cnt = 0;
            do { cnt++; } while (n > 0);
            std::cout << cnt << std::endl;
        }
    '''),
    options=["1", "0", "2", "死循环"],
    value=cpp('''
        #include <iostream>
        int main() {
            int n = 0, cnt = 0;
            do { cnt++; } while (n > 0);
            std::cout << cnt << std::endl;
        }
    '''),
    section=_S,
    expl="do-while **先执行循环体，再判断条件**：`0 > 0` 一开始就是假，但循环体已经跑过一次，"
         "所以 cnt = **1**。\n"
         "B 是 while 的行为（先判断，一次都不进）；C 是误以为条件为假还要再跑一次；"
         "D 混淆了「尾部漏分号」那类死循环 —— 这里的 n 从未改变，但条件只判一次就退出了。\n"
         "★ 「至少执行一次」正是 do-while 存在的理由（输入校验那类「先做再问」的场景）。",
    tags=["do-while 循环", "循环"], diff=2)

tfn(title="setw 的生效范围",
    stmt="`setw(n)` 设置输出宽度后，对**其后所有**输出项都生效。",
    answer=False, section=_S,
    expl="错。`setw` 是**一次性**操纵符，只管紧随其后的**一个**输出项。"
         "`cout << setw(6) << 42 << \"|\" << 42;` 里只有第一个 42 占 6 位。\n"
         "持久的另一派是 `hex` / `fixed` / `left` / `setfill` —— 一旦设置一直生效。"
         "操纵符分这两派，是本讲格式控制最常考的一句。",
    tags=["setw 宽度", "格式控制"], diff=3)

mcn(title="switch 漏写 break 的输出",
    stmt=_stmt("下面程序的输出是什么？", '''
        #include <iostream>

        int main() {
            int level = 1;
            switch (level) {
            case 1: std::cout << "case1 ";
            case 2: std::cout << "case2 ";
            case 3: std::cout << "case3 ";
            default: std::cout << "default";
            }
            std::cout << std::endl;
        }
    '''),
    options=["case1 case2 case3 default", "case1", "case1 case2", "default"],
    value=cpp('''
        #include <iostream>
        int main() {
            int level = 1;
            switch (level) {
            case 1: std::cout << "case1 ";
            case 2: std::cout << "case2 ";
            case 3: std::cout << "case3 ";
            default: std::cout << "default";
            }
            std::cout << std::endl;
        }
    '''),
    section=_S,
    expl="`case` 标签只是**入口，不是围栏**：匹配 case 1 之后一路往下执行，"
         "直到遇到 `break` 或 switch 结尾，所以四个分支的语句全部跑了一遍。\n"
         "B 以为每个 case 自带隔离；C 以为只贯穿一层；D 以为没匹配上就直接跳 default。\n"
         "g++ 对每一处漏 break 都给 `-Wimplicit-fallthrough` 警告 —— 见到它就查 case。",
    tags=["switch 分支", "贯穿"], diff=3)

fillc(title="setprecision 的有效数字位数",
      stmt=_stmt("下面程序的输出是什么？", '''
        #include <iostream>
        #include <iomanip>

        int main() {
            std::cout << std::setprecision(4) << 3.14159265358979 << std::endl;
        }
    '''),
      value=cpp('''
        #include <iostream>
        #include <iomanip>
        int main() {
            std::cout << std::setprecision(4) << 3.14159265358979 << std::endl;
        }
    '''),
      section=_S,
      expl="不带 `fixed` 时，`setprecision(n)` 是 **n 位有效数字**，不是 n 位小数："
           "3.141592… 取 4 位有效数字 → `3.142`。\n"
           "填 3.1416 是把它当成小数位数（那要写 `fixed << setprecision(4)`）；"
           "填 3.141 是截断而不是四舍五入；填 3.14 是只取 3 位有效数字。\n"
           "★ 两套语义必须分清：裸 precision = 有效位；`fixed` + precision = 小数位。",
      tags=["setprecision 精度", "有效数字"], diff=3)

mcn(title="while (n-- > 0) 的逐步输出",
    stmt=_stmt("下面程序输出什么？", '''
        #include <iostream>

        int main() {
            int n = 3;
            while (n-- > 0) std::cout << n;
            std::cout << std::endl;
        }
    '''),
    options=["210", "321", "123", "3210"],
    value=cpp('''
        #include <iostream>
        int main() {
            int n = 3;
            while (n-- > 0) std::cout << n;
            std::cout << std::endl;
        }
    '''),
    section=_S,
    expl="`n--` 是后置自减：**先拿旧值比较，再减 1**。逐步走：3>0 成立、n 变 2，打印 **2**；"
         "2>0 → 打印 **1**；1>0 → 打印 **0**；0>0 不成立退出（此刻 n 已是 -1）。所以是 `210`。\n"
         "B 打印的是比较前的值（把它当成了 `--n`）；C 是递增方向；D 多打了一位。",
    tags=["while 循环", "后置自减"], diff=3)

multn(title="C++ 表达式陷阱的多项辨析",
      stmt="关于 C++ 中常见的表达式陷阱，下列说法正确的有：",
      options=[
          "两个 int 相除，结果仍是 int，小数部分被直接截断",
          "运算符 % 的两个操作数可以是 double",
          "0.1 + 0.2 == 0.3 的值为 true",
          "if (x = 5) 中赋值表达式的值为 5，条件恒为真",
      ],
      answers=["A", "D"], section=_S,
      expl="A 对：`7/2` 得 3，要小数必须有一方是浮点（`7.0/2`）。\n"
           "B 错：`%` **只接受整型**，浮点取余要用 `fmod`。\n"
           "C 错：二进制表示不了 0.1、0.2 的精确值，`==` 实测为 false —— "
           "虽然打印出来是 0.3（那是四舍五入的表象）；判等必须用误差范围。\n"
           "D 对：赋值表达式的值就是被赋的值，非零即真，且 x 已被污染成 5；"
           "g++ 的 `-Wparentheses` 警告专门盯这个。",
      tags=["表达式陷阱", "多选"], diff=4, rot=1)

mcn(title="逻辑与短路求值的副作用次数",
    stmt=_stmt("下面程序的输出是什么？", '''
        #include <iostream>

        int main() {
            int cnt = 0;
            bool r  = (7 > 4) && (++cnt > 0);   // 左边为真，右边才算
            bool r2 = (7 < 4) && (++cnt > 0);   // 左边为假，右边不算
            std::cout << r << " " << cnt << std::endl;
        }
    '''),
    options=["1 1", "1 2", "0 1", "0 2"],
    value=cpp('''
        #include <iostream>
        int main() {
            int cnt = 0;
            bool r  = (7 > 4) && (++cnt > 0);
            bool r2 = (7 < 4) && (++cnt > 0);
            std::cout << r << " " << cnt << std::endl;
        }
    '''),
    section=_S,
    expl="`&&` 是**短路**求值：左边为真才求右边。第一条 `(7>4)` 为真 → 执行 `++cnt`，cnt=1；"
         "第二条 `(7<4)` 为假 → 右边整个不求值，cnt 保持 1。所以输出 `1 1`。\n"
         "B 以为两侧都会算；C 把 r 的真值算错（r 确实是 1）；D 两处都错。\n"
         "★ 靠短路才敢写 `if (p != nullptr && p->len > 0)` —— 先判空再解引用，写反了就是 UB。",
    tags=["短路求值", "逻辑运算"], diff=4)

# ---- 以下为 2026-10 扩充：02 讲补到 20 题（理论 18 + 编程 2）----

mcn(title="关系运算符左结合造成的连不等式",
    stmt=_stmt("想表达数学上的「3 大于 2 大于 1」，直接写成连不等式。下面程序输出什么？", '''
        #include <iostream>

        int main() {
            std::cout << (3 > 2 > 1) << std::endl;
        }
    '''),
    options=["0", "1", "2", "编译错"],
    value=cpp('''
        #include <iostream>
        int main() { std::cout << (3 > 2 > 1) << std::endl; }
    '''),
    section=_S,
    expl="输出 **0**。关系运算符是**左结合**且结果只有 0/1：先算 `3 > 2` 得 `true`（即 1），\n"
         "再算 `1 > 1` 得 `false`（0）。数学上的连不等式在 C++ 里写不出来。\n"
         "B 是按数学直觉读「3>2 且 2>1」，以为两边都成立；C 是凭空造了个中间值；\n"
         "D 错得最危险 —— 这段代码**语法完全合法**，编译器一句警告都不会给（g++ 也不拦）。\n"
         "★ 正确姿势：`3 > 2 && 2 > 1`。优先级口诀：算术 > 关系 > 逻辑（`!` 最高）> 赋值 > 逗号。",
    tags=["运算符优先级", "关系运算"], diff=2)

mcn(title="逗号表达式的值与赋值优先级",
    stmt=_stmt("下面两行初始化里，`k` 有括号包住、`a` 没有。输出是什么？", '''
        #include <iostream>

        int main() {
            int k = (1, 2, 3);
            int a = 0;
            a = 1, 2;
            std::cout << k << " " << a << std::endl;
        }
    '''),
    options=["3 1", "3 2", "1 1", "1 2"],
    value=cpp('''
        #include <iostream>
        int main() {
            int k = (1, 2, 3);
            int a = 0;
            a = 1, 2;
            std::cout << k << " " << a << std::endl;
        }
    '''),
    section=_S,
    expl="输出 `3 1`。逗号表达式的值是**最后一个**操作数，所以 `(1,2,3)` 得 3，k=3。\n"
         "但第二行 `a = 1, 2;` 里**赋值优先级高于逗号**，实际是 `(a = 1), 2;`：\n"
         "先把 1 赋给 a，那个 2 算完就丢（g++ 给 `-Wunused-value`）。\n"
         "B 以为逗号在任何位置都取最后一个；C 以为括号也救不了、两处都是首值；D 两处都错。\n"
         "★ 「逗号取最后一个」只在**整条表达式被括号包住**时才是你要的效果；\n"
         "实参分隔、声明多个变量用的逗号是**分隔符**，不是逗号运算符，别混。",
    tags=["逗号表达式", "运算符优先级"], diff=2)

mcn(title="按位与或异或取反的一组结果",
    stmt=_stmt("下面程序把 5（101）与 3（011）做四种位运算。输出是什么？", '''
        #include <iostream>

        int main() {
            std::cout << (5 & 3) << " " << (5 | 3) << " "
                      << (5 ^ 3) << " " << (~5) << std::endl;
        }
    '''),
    options=["1 7 6 -6", "1 7 6 6", "1 7 2 -6", "7 1 6 -6"],
    value=cpp('''
        #include <iostream>
        int main() {
            std::cout << (5 & 3) << " " << (5 | 3) << " "
                      << (5 ^ 3) << " " << (~5) << std::endl;
        }
    '''),
    section=_S,
    expl="逐个位算：5=`101`、3=`011`。\n"
         "- `&` 全 1 才 1 → `001` = **1**；\n"
         "- `|` 有 1 就 1 → `111` = **7**；\n"
         "- `^` 同 0 异 1 → `110` = **6**；\n"
         "- `~` 逐位取反（含符号位），`~5` = **-6** —— 与 -5 差 1，因为 -5 要 `~5 + 1`。\n"
         "B 把 `~5` 当成 5，可能把按位取反误认成了「取绝对值」；C 把异或当成普通减法（5−3=2）；\n"
         "D 把 `&` 与 `|` 对调了。\n"
         "★ 位运算与第 1 章补码直接挂钩：`~x + 1 == -x` 是补码的定义式；\n"
         "左移 1 位≈×2、右移 1 位≈÷2，但**负数右移行为依实现**，别拿它做除法。",
    tags=["位运算", "补码"], diff=3)

fillc(title="x 与 x 减 1 相与统计 1 的个数",
      stmt=_stmt("`x &= x - 1` 每轮抹掉最低位的一个 1。下面程序分别统计 29 与 255 的 1 的个数。"
                 "输出是什么？", '''
        #include <iostream>

        int countOnes(unsigned x) {
            int c = 0;
            while (x) { x &= x - 1; c++; }
            return c;
        }

        int main() {
            std::cout << countOnes(29) << " " << countOnes(255) << std::endl;
        }
    '''),
      value=cpp('''
        #include <iostream>
        int countOnes(unsigned x) {
            int c = 0;
            while (x) { x &= x - 1; c++; }
            return c;
        }
        int main() {
            std::cout << countOnes(29) << " " << countOnes(255) << std::endl;
        }
    '''),
      section=_S,
      expl="29 = `11101`，有 **4** 个 1；255 = `11111111`，有 **8** 个 → `4 8`。\n"
           "为什么 `x &= x - 1` 每轮恰好消掉**最低位**的那个 1？拿 29 走一轮：\n"
           "`11101 & 11100 = 11100` —— 最低位的 1 被抹平，高位不动。这就是第 1 章\n"
           "「减 1 时从最低位的 1 借位」的性质。循环次数 = 1 的个数，与总位数无关：\n"
           "255 要走 8 次，而不是 32 次。\n"
           "填 `5 8` 是把 29 当成了 `11111`；填 `4 7` 是数错了 255；填 `3 8` 是漏数最高位。\n"
           "★ 对照写法 `while (n) { c += n & 1; n >>= 1; }` 要固定循环 32 次（或位数次），\n"
           "Kernighan 这一招只循环「1 的个数」次 —— 稀疏数据上快得多。",
      tags=["位运算", "二进制"], diff=3)

mcn(title="bool 参与算术与字符字面量的 sizeof", rot=0,
    stmt=_stmt("下面程序打印三个值。输出是什么？", '''
        #include <iostream>

        int main() {
            std::cout << (true + true) << " " << sizeof('a') << " "
                      << sizeof(bool) << std::endl;
        }
    '''),
    options=["2 4 1", "1 1 1", "2 1 4", "2 1 1"],
    value=cpp('''
        #include <iostream>
        int main() {
            std::cout << (true + true) << " " << sizeof('a') << " "
                      << sizeof(bool) << std::endl;
        }
    '''),
    section=_S,
    expl="输出 `2 1 1`。bool 只有 true/false，一进算术就提升成 int 的 1/0，`true + true` = **2**。\n"
         "关键在第二个数：**C++ 里字符字面量 `'a'` 的类型就是 char**，`sizeof('a')` = **1**。\n"
         "C 语言里它才是 int（4 字节）—— 这是 C/C++ 最著名的分歧之一，从 C 转过来的同学必踩。\n"
         "`sizeof(bool)` 也是 1 字节。\n"
         "A 正是拿 C 的规则来答 C++；B 以为 bool 相加还是 bool（那会得 true=1）；\n"
         "C 把 bool 当成了 4 字节。\n"
         "★ 顺带记：`sizeof` 是**运算符**不是函数，量的是**类型**，编译期就定值。",
    tags=["bool 类型", "sizeof 运算", "类型转换"], diff=3)

mcn(title="continue 与 break 混用后的输出序列",
    stmt=_stmt("下面程序用逗号分隔打印结果。输出是什么？", '''
        #include <iostream>

        int main() {
            for (int k = 1; k <= 10; k++) {
                if (k % 2 == 0) continue;
                if (k > 7) break;
                std::cout << k << ",";
            }
            std::cout << std::endl;
        }
    '''),
    options=["1,3,5,7,", "1,2,3,4,5,6,7,", "1,3,5,7,9,", "1,3,5,"],
    value=cpp('''
        #include <iostream>
        int main() {
            for (int k = 1; k <= 10; k++) {
                if (k % 2 == 0) continue;
                if (k > 7) break;
                std::cout << k << ",";
            }
            std::cout << std::endl;
        }
    '''),
    section=_S,
    expl="输出 `1,3,5,7,`。两类跳转的作用范围完全不同：\n"
         "- **continue** 只跳**本次**，回去执行 `k++` —— 偶数 2、4、6、8、10 被逐个扔掉；\n"
         "- **break** 掐断**整层循环** —— k=9 时 `9 > 7` 成立，直接出循环，9 根本没机会打印。\n"
         "B 是两条跳转都没生效（等价于不加 if）；C 忘了 break（9 会被打出来）；\n"
         "D 以为 break 在 7 之前就触发。\n"
         "★ 手推这类题的方法：把 k 从 1 到 10 逐个写一行，标出「跳过 / 退出 / 打印」，不要跳步。\n"
         "另外注意 `continue` 在 for 里会执行更新表达式，在 while 里则**直接回条件判断** —— \n"
         "循环变量更新写在循环体末尾的 while，配 continue 就是死循环。",
    tags=["break/continue", "循环边界"], diff=3)

fillc(title="unsigned 减出负数后的回绕值",
      stmt=_stmt("下面程序让一个 unsigned 变量减去比自己大的数。输出是什么？", '''
        #include <iostream>

        int main() {
            unsigned u = 2;
            u -= 5;
            std::cout << u << std::endl;
        }
    '''),
      value=cpp('''
        #include <iostream>
        int main() {
            unsigned u = 2;
            u -= 5;
            std::cout << u << std::endl;
        }
    '''),
      section=_S,
      expl="输出 **4294967293**。2 − 5 = −3，但 unsigned 装不下负数，按模 2³² 回绕：\n"
           "2³² − 3 = 4294967296 − 3 = **4294967293**（位模式与 -3 的补码完全相同）。\n"
           "填 -3 是把 unsigned 当成了 int —— 它**不会**输出负数，也不报错；\n"
           "填 3 是取了绝对值；填 4294967295 是把它当成了 0−1。\n"
           "★ 这与「-1 < 1u 为 false」是同一件事的两面：unsigned 的世界里没有负数，\n"
           "减出下界就绕到上界。所以循环里写 `for (unsigned i = n - 1; i >= 0; i--)` 是经典死循环。",
      tags=["无符号数", "回绕"], diff=4)

# =========================================================================
# 第 03 讲 · 函数（18 题）
# =========================================================================
_S = "第 03 讲 · 函数"

mcn(title="值传递与引用传递的实参变化",
    stmt=_stmt("下面程序的输出是什么？", '''
        #include <iostream>

        void ByValue(int x)      { x = 100; }
        void ByReference(int &r) { r = 100; }

        int main() {
            int a = 1;
            ByValue(a);
            std::cout << a << " ";
            ByReference(a);
            std::cout << a << std::endl;
        }
    '''),
    options=["1 100", "100 100", "1 1", "100 1"],
    value=cpp('''
        #include <iostream>
        void ByValue(int x)      { x = 100; }
        void ByReference(int &r) { r = 100; }
        int main() {
            int a = 1;
            ByValue(a);
            std::cout << a << " ";
            ByReference(a);
            std::cout << a << std::endl;
        }
    '''),
    section=_S,
    expl="值传递把 a **复制**一份给 x，函数里改的是复印件，a 仍是 1；"
         "引用是 a 的**别名**，`r = 100` 就是 `a = 100`。所以是 `1 100`。\n"
         "B 是「以为值传递也能改实参」（`Swap(x,y)` 白干就是这个原因）；"
         "C 以为引用只在函数内有效；D 把两种方式的效果对调了。\n"
         "★ 引用与值传递**调用写法一模一样**，改接口时行为会悄悄变化 —— 这是它最迷惑的地方。",
    tags=["值传递", "引用传递"], diff=1)

mcn(title="数组形参的 sizeof 退化",
    stmt=_stmt("在 64 位平台（int 4 字节、指针 8 字节）上，下面程序输出什么？", '''
        #include <iostream>

        void f(int a[10]) { std::cout << sizeof(a) << std::endl; }

        int main() {
            int a[10];
            std::cout << sizeof(a) << " ";
            f(a);
        }
    '''),
    options=["40 8", "40 40", "8 8", "4 8"],
    value=cpp('''
        #include <iostream>
        void f(int a[10]) { std::cout << sizeof(a) << std::endl; }
        int main() {
            int a[10];
            std::cout << sizeof(a) << " ";
            f(a);
        }
    '''),
    section=_S,
    expl="main 里的 a 是真数组，`sizeof(a)` = 10×4 = **40**；作形参时 `int a[10]` 里的 `[10]` "
         "只是给人看的记号，编译器眼里就是 `int *a`，`sizeof` 得到指针大小 **8**。\n"
         "所以数组大小**根本不会随参数传进函数** —— 所有数组版算法都带一个 `n` 参数，原因就在这里。\n"
         "B 忘了形参会退化；C 把 main 里也当指针；D 把 main 里的 sizeof 数成 4。",
    tags=["数组形参", "sizeof 运算"], diff=2)

tfn(title="返回值类型能否作为重载依据",
    stmt="两个同名函数只要**返回值类型不同**（参数个数、类型、顺序完全相同），"
         "就构成合法的函数重载。",
    answer=False, section=_S,
    expl="错。重载**只看参数表**（个数 / 类型 / 顺序），返回值类型不参与。"
         "`int f(int)` 与 `double f(int)` 是非法重复定义 —— 因为调用处写 `f(3);`"
         "不接返回值时，编译器根本无法在两者之间选择。\n"
         "「形参名字不同」也救不了：`int f(int a)` 与 `int f(int b)` 是同一个函数。",
    tags=["函数重载", "返回值"], diff=2)

mcn(title="不带括号的宏展开结果",
    stmt=_stmt("下面程序的输出是什么？", '''
        #include <iostream>

        #define SQ_BAD(x) x * x

        int main() {
            std::cout << SQ_BAD(1 + 2) << std::endl;
        }
    '''),
    options=["9", "5", "6", "7"],
    value=cpp('''
        #include <iostream>
        #define SQ_BAD(x) x * x
        int main() { std::cout << SQ_BAD(1 + 2) << std::endl; }
    '''),
    section=_S,
    expl="宏是**纯文本替换**，`SQ_BAD(1 + 2)` 展开成 `1 + 2 * 1 + 2`，乘法先算 → **5**。\n"
         "A 是内联函数 `Square(1+2)` 的结果（函数有真正的参数边界）；C、D 是随手写的中途值。\n"
         "即使加满括号写成 `((x)*(x))`，宏仍有两个先天缺陷：**不检查类型**、"
         "**带副作用的实参会算多次**（`SQ(x++)` 会让 x 自增两次）。内联函数把这些毛病一次解决。",
    tags=["宏", "内联函数"], diff=2)

mcn(title="默认形参的补值顺序",
    stmt=_stmt("下面程序的输出是什么？", '''
        #include <iostream>

        int Add(int a, int b = 5, int c = 10) { return a + b + c; }

        int main() {
            std::cout << Add(1) << " " << Add(1, 2) << " " << Add(1, 2, 3) << std::endl;
        }
    '''),
    options=["16 13 6", "16 8 6", "11 13 6", "6 13 16"],
    value=cpp('''
        #include <iostream>
        int Add(int a, int b = 5, int c = 10) { return a + b + c; }
        int main() {
            std::cout << Add(1) << " " << Add(1, 2) << " " << Add(1, 2, 3) << std::endl;
        }
    '''),
    section=_S,
    expl="实参**从左往右**依次填，缺的**从右往左**取默认值："
         "Add(1)=1+5+10=16；Add(1,2)=1+2+10=13；Add(1,2,3)=6。\n"
         "B 是以为省略中间参数（那在语法上做不到）；C 以为 b 默认 5 不生效；D 把顺序倒过来了。\n"
         "★ 默认值必须**从右向左连续**给出：`f(int a = 1, int b)` 直接编译错"
         "（`f(2)` 时 b 没值可取）。默认值写在声明处，定义处不重复。",
    tags=["默认形参", "函数调用"], diff=3)

mcn(title="char 实参的重载解析",
    stmt=_stmt("下面程序的输出是什么？", '''
        #include <iostream>

        void Print(int x)    { std::cout << "int " << x; }
        void Print(double x) { std::cout << "double " << x; }

        int main() {
            char c = 'A';
            Print(c);
            std::cout << std::endl;
        }
    '''),
    options=["int 65", "double 65", "int 65.0", "double 65.0"],
    value=cpp('''
        #include <iostream>
        void Print(int x)    { std::cout << "int " << x; }
        void Print(double x) { std::cout << "double " << x; }
        int main() { char c = 'A'; Print(c); std::cout << std::endl; }
    '''),
    section=_S,
    expl="char → int 是**整型提升（promotion）**，char → double 是**标准转换（conversion）**；"
         "提升优先级高于标准转换，所以选中 `Print(int)`，实参按 ASCII 码值 65 传入 → `int 65`。\n"
         "B、D 是只看「double 更宽」；C 是以为 int 版会打印浮点。\n"
         "★ 重载解析优先级：精确匹配 > 整型提升 > 标准转换 > 用户自定义转换；"
         "到第三级还有两个候选打平，就是二义性编译错。",
    tags=["重载解析", "整型提升"], diff=3)

_HANOI = '''
    #include <iostream>

    long long g = 0;

    void HanoiCount(int n) {
        ++g;
        if (n == 1) return;
        HanoiCount(n - 1);
        HanoiCount(n - 1);
    }

    int main() {
        HanoiCount(5);
        std::cout << g << std::endl;
    }
'''
fillc(title="汉诺塔五层的调用次数",
      stmt=_stmt("下面的递归函数只统计调用次数（不打印移动步骤）。"
                 "挪 5 层时，`HanoiCount(5)` 一共被调用多少次（含最外层这次）？", _HANOI),
      value=cpp(_HANOI),
      section=_S,
      expl="T(n) = 2·T(n−1) + 1 且 T(1) = 1，解出 **T(n) = 2ⁿ − 1**；n=5 得 31。\n"
           "填 32 是只算了 2ⁿ、忘了减 1（把「调用次数」当成了满二叉树的结点数再补一层）；"
           "填 15 是少算一层（那是 n=4）；填 63 是 n=6。\n"
           "★ n 每加 1，工作量翻倍：n=20 时是 1048575 次 —— 这就是「指数爆炸」的字面意思。",
      tags=["递归", "汉诺塔"], diff=3)

mcn(title="递归的逆序打印",
    stmt=_stmt("下面程序输出什么？", '''
        #include <iostream>

        void Mystery(int n) {
            if (n == 0) return;
            std::cout << n % 10;
            Mystery(n / 10);
        }

        int main() {
            Mystery(12345);
            std::cout << std::endl;
        }
    '''),
    options=["54321", "12345", "5", "15"],
    value=cpp('''
        #include <iostream>
        void Mystery(int n) {
            if (n == 0) return;
            std::cout << n % 10;
            Mystery(n / 10);
        }
        int main() { Mystery(12345); std::cout << std::endl; }
    '''),
    section=_S,
    expl="每层**先打印个位**（n%10）再递归除 10：依次打出 5、4、3、2、1 → `54321`。\n"
         "B 是把两句调换（先递归后打印）的结果 —— 那才是正序。"
         "「调换递归与处理的先后」是递归输出题最经典的变体。\n"
         "C 只看了第一层；D 把 modulus 当成了累加。",
    tags=["递归", "数位分解"], diff=3)

mcn(title="constexpr 函数的编译期求值",
    stmt=_stmt("下面程序能编译通过，输出是什么？", '''
        #include <iostream>

        constexpr long long Fact(int n) { return n <= 1 ? 1 : n * Fact(n - 1); }

        int main() {
            long long f = Fact(5);
            int arr[Fact(4)];                       // 数组长度必须是常量表达式
            std::cout << f << " " << sizeof(arr) / sizeof(int) << std::endl;
        }
    '''),
    options=["120 24", "120 96", "24 120", "120 4"],
    value=cpp('''
        #include <iostream>
        constexpr long long Fact(int n) { return n <= 1 ? 1 : n * Fact(n - 1); }
        int main() {
            long long f = Fact(5);
            int arr[Fact(4)];
            std::cout << f << " " << sizeof(arr) / sizeof(int) << std::endl;
        }
    '''),
    section=_S,
    expl="Fact(5) = 120。`int arr[Fact(4)]` 能编译通过，说明 Fact(4)=24 是**常量表达式**"
         "（数组长度必须是编译期常量）→ 24 个 int，`sizeof/sizeof` 折回元素个数 24。\n"
         "B 的 96 是字节数（24×4），忘了除 sizeof(int)；C 把两个数对调；"
         "D 是把 Fact(4) 当成 4 的误解。\n"
         "★ constexpr 传常量就在编译期算，传变量则退化为普通函数；"
         "const 只承诺「运行期不改」，不承诺「编译期可算」，所以 `const int n = x*2;` 不能当数组长度。",
    tags=["constexpr 函数", "编译期求值"], diff=4)

mcp(title="重载二义性的成因", answer="C",
    stmt="下列哪种情况会让编译器报「重载调用有二义性（ambiguous）」？",
    options=[
        "两个重载函数的返回值类型不同，参数表完全相同",
        "两个重载函数的形参名字不同，参数表完全相同",
        "实参同时能做两种标准转换，且两种转换谁也不比谁更优",
        "调用重载函数时漏写了语句末尾的分号",
    ],
    section=_S,
    expl="C。典型现场：`void G(long)` 与 `void G(double)` 遇到 `G(10)` —— "
         "int→long 与 int→double 都是标准转换，打平，g++ 报 "
         "`call of overloaded 'G(int)' is ambiguous` 并列出两个候选。\n"
         "A 是**非法重复定义**（返回值不参与重载），不是二义性；B 参数名不影响函数签名，"
         "那是同一个函数的重复定义；D 是纯粹的语法错误。\n"
         "对策：显式写出类型（`G(10L)` / `G(10.0)`），或给重载起不同名字。\n"
         "★ 另两种二义性来源：重载 + 默认形参让两个都能接（`f(int)` 与 `f(int,int=5)`）、"
         "类型顺序重载遇上混合实参（`F(int,double)` 与 `F(double,int)` 遇 `F(1,2)`）。",
    tags=["重载", "二义性"], diff=4)

# ---- 以下为 2026-10 扩充：03 讲补到 20 题（理论 18 + 编程 2）----

# 无计算：概念题，按讲义口径判定（不跑代码）
tfn(title="引用必须在定义时绑定且不能改绑",
    stmt="引用在定义时必须初始化，绑定之后不能再改为引用另一个变量。",
    answer=True, section=_S,
    expl="对。引用是**别名**：`int &r;` 直接编译错（`declaration of reference variable 'r' "
         "requires an initializer`），因为它必须一出生就指出「我是谁的名字」。\n"
         "绑定之后 `r = y;` 是**给被引用的那个变量赋值**（改的是值），**不是改绑** —— \n"
         "引用一旦绑定就死守那个对象。能改指向的只有指针（`p = &y`）。\n"
         "★ 由此还有两条推论：引用没有「空引用」（必须绑到真对象上）；\n"
         "函数返回引用时绝不能返回局部变量（栈帧已拆，别名指向死内存）。",
    tags=["引用", "绑定"], diff=2)

mcn(title="返回引用的函数可以放在赋值号左边",
    stmt=_stmt("`At` 返回数组元素的引用。下面程序输出什么？", '''
        #include <iostream>

        int &At(int a[], int i) { return a[i]; }

        int main() {
            int arr[3] = {10, 20, 30};
            At(arr, 1) = 99;
            std::cout << arr[1] << " " << arr[0] << std::endl;
        }
    '''),
    options=["99 10", "20 10", "99 20", "编译错"],
    value=cpp('''
        #include <iostream>
        int &At(int a[], int i) { return a[i]; }
        int main() {
            int arr[3] = {10, 20, 30};
            At(arr, 1) = 99;
            std::cout << arr[1] << " " << arr[0] << std::endl;
        }
    '''),
    section=_S,
    expl="输出 `99 10`。`At` 的返回类型是 `int&`，所以 `At(arr, 1)` 求值出来就是 `arr[1]` 的\n"
         "**别名**，放在赋值号左边等于直接给 arr[1] 赋值 → 99；arr[0] 没被碰过，仍是 10。\n"
         "B 以为返回引用只能只读；C 以为整个数组会被改；D 错，语法完全合法。\n"
         "★ 「返回引用可作左值」是引用的标志性能力：`operator[]`、`operator=` 返回 `T&`、\n"
         "istream 的 `>>` 返回 `istream&` 以便链式调用，全靠这一条。\n"
         "代价是调用者拿到了内部数据的写权限 —— 不想给就把返回类型写成 `const int&`。",
    tags=["引用", "左值"], diff=2)

mcn(title="指针形参交换两个实参的值",
    stmt=_stmt("下面程序用指针形参交换两个变量。输出什么？", '''
        #include <iostream>

        void SwapPointer(int *a, int *b) { int t = *a; *a = *b; *b = t; }

        int main() {
            int x = 1, y = 2;
            SwapPointer(&x, &y);
            std::cout << x << " " << y << std::endl;
        }
    '''),
    options=["2 1", "1 2", "1 1", "2 2"],
    value=cpp('''
        #include <iostream>
        void SwapPointer(int *a, int *b) { int t = *a; *a = *b; *b = t; }
        int main() {
            int x = 1, y = 2;
            SwapPointer(&x, &y);
            std::cout << x << " " << y << std::endl;
        }
    '''),
    section=_S,
    expl="输出 `2 1`。指针传递复制的是**地址**：`a` 里存着 `&x`，`*a` 顺着地址摸到 x 本体，\n"
         "所以交换真的发生了。\n"
         "B 是**值传递**版 `SwapValue(x, y)` 的结果（改的是两个副本，白干）；\n"
         "C、D 是把某一次解引用漏掉了（只改了副本或只改了一边）。\n"
         "★ 三种传递的分工：要改实参用**引用**（调用处最干净）；需要表达「可能为空」用指针；\n"
         "只读大对象用 `const &`。指针版调用处漏写 `&` 会直接编译错（int 转不成 int*），\n"
         "这反而是好事；引用与值传递**调用写法一模一样**，改接口时会悄悄改变行为。",
    tags=["指针传递", "参数传递"], diff=2)

mcn(title="float 实参在 int 与 double 重载间的选择",
    stmt=_stmt("下面程序用 float 实参调用重载函数。输出什么？", '''
        #include <iostream>

        void F(int x)    { std::cout << "F(int) " << x; }
        void F(double x) { std::cout << "F(double) " << x; }

        int main() {
            F(3.14f);
            std::cout << std::endl;
        }
    '''),
    options=["F(double) 3.14", "F(int) 3", "F(int) 3.14", "F(double) 3.140000"],
    value=cpp('''
        #include <iostream>
        void F(int x)    { std::cout << "F(int) " << x; }
        void F(double x) { std::cout << "F(double) " << x; }
        int main() { F(3.14f); std::cout << std::endl; }
    '''),
    section=_S,
    expl="输出 `F(double) 3.14`。`3.14f` 是 float：**float → double 是浮点提升（promotion）**，\n"
         "**float → int 是标准转换（conversion）**；提升优先级高于标准转换，所以选中 `F(double)`。\n"
         "B、C 以为会截断成 int；D 是以为会打出 6 位小数 —— 这里没设 `fixed`，\n"
         "默认是 6 位**有效数字**，3.14 原样打出。\n"
         "★ 与「char 实参选 F(int) 而不是 F(double)」是同一条规则的两个方向：\n"
         "**精确匹配 > 提升 > 标准转换 > 用户自定义转换**。\n"
         "想强制走 int 版就写 `F(static_cast<int>(3.14f))`，别指望编译器替你猜。",
    tags=["重载解析", "类型提升"], diff=3)

# 无计算：概念题，按讲义口径判定（不跑代码）
tfn(title="默认形参在声明与定义处重复指定",
    stmt="同一个函数可以在原型声明和定义处各写一次默认形参值，编译器会以后写的那个为准。",
    answer=False, section=_S,
    expl="错。同一作用域内一个形参的默认值**只能指定一次**，写两遍是编译错\n"
         "（`redefinition of default argument`）—— 不是「后者覆盖前者」。\n"
         "规矩：默认值写在**声明（头文件）**处，定义处只写参数表。单文件程序把默认值写在\n"
         "定义处也能过，但分文件编译时调用者只看得到头文件，所以放声明处才是工程做法。\n"
         "★ 另两条一起背：默认值必须**从右向左连续**给出（`f(int a = 1, int b)` 编译错）；\n"
         "重载 + 默认形参容易造出「两个都能接」的二义性（`f(int)` 与 `f(int, int = 5)` 遇 `f(1)`）。",
    tags=["默认形参", "声明与定义"], diff=3)

fillc(title="朴素递归求斐波那契的调用次数",
      stmt=_stmt("下面的递归函数只统计自己被调用了多少次（含最外层）。`Fib(5)` 一共调用多少次？", '''
        #include <iostream>

        long long g = 0;

        long long Fib(int n) {
            ++g;
            return n < 2 ? n : Fib(n - 1) + Fib(n - 2);
        }

        int main() {
            Fib(5);
            std::cout << g << std::endl;
        }
    '''),
      value=cpp('''
        #include <iostream>
        long long g = 0;
        long long Fib(int n) {
            ++g;
            return n < 2 ? n : Fib(n - 1) + Fib(n - 2);
        }
        int main() {
            Fib(5);
            std::cout << g << std::endl;
        }
    '''),
      section=_S,
      expl="设 C(n) 为调用次数，则 C(0)=C(1)=1、C(n)=1+C(n−1)+C(n−2)：\n"
           "C(2)=3、C(3)=5、C(4)=9、**C(5)=15**。\n"
           "填 5 是只数了「第几项」；填 9 是少算一层（那是 C(4)）；填 16 是把它当成了满二叉树；\n"
           "填 31 是套了汉诺塔的 2⁵−1 —— 两题结构不同，别混。\n"
           "★ 两种「指数级」病因不同：汉诺塔的 2ⁿ−1 是**问题本身**的工作量（每一步都必须走）；\n"
           "朴素 fib 是指数级**重复计算**（Fib(3) 被算了多遍），加记忆化就能降到 O(n)。\n"
           "考试爱用这对辨析，别一看到「递归很慢」就归成同一类。",
      tags=["递归", "调用次数"], diff=3)

# 无计算：概念题，按讲义口径判定（不跑代码）
tfn(title="递归的空间开销与栈帧层数",
    stmt="递归函数只消耗时间、不额外占用空间，因为各层的局部变量都在同一块栈帧里复用。",
    answer=False, section=_S,
    expl="错。每进入一层函数，系统就在**运行栈**上压一个新的**栈帧**：返回地址、形参、局部变量。\n"
         "各层的局部变量**各有一份**，绝不是复用同一块 —— 否则递归根本无法「回来」。\n"
         "所以递归 n 层的空间开销是 **O(n)**，哪怕函数里一个数组都没开。\n"
         "★ 两条推论：① 递归深度 = 栈帧层数 = 空间开销，深递归爆的是**栈**不是堆；\n"
         "② 没有出口的递归会一路压栈直到栈溢出，进程被异常终止，连最后一句输出都来不及刷出。\n"
         "这也是「能迭代就迭代」的理由之一 —— 但树形/分治问题（汉诺塔、回溯）递归写法直接\n"
         "映射问题结构，该用还得用。",
    tags=["递归", "栈帧"], diff=3)

mcn(title="左值与右值分别落到哪个引用重载",
    stmt=_stmt("两个重载只差参数是 `int&` 还是 `const int&`。下面程序输出什么？", '''
        #include <iostream>

        void H(int &r)       { std::cout << "lvalue"; }
        void H(const int &r) { std::cout << "rvalue"; }

        int main() {
            int x = 5;
            H(x);
            std::cout << " ";
            H(42);
            std::cout << std::endl;
        }
    '''),
    options=["lvalue rvalue", "rvalue lvalue", "lvalue lvalue", "编译错"],
    value=cpp('''
        #include <iostream>
        void H(int &r)       { std::cout << "lvalue"; }
        void H(const int &r) { std::cout << "rvalue"; }
        int main() {
            int x = 5;
            H(x);
            std::cout << " ";
            H(42);
            std::cout << std::endl;
        }
    '''),
    section=_S,
    expl="输出 `lvalue rvalue`。`H(int&)` 只能绑定**左值**（有名字、有地址的 x），精确匹配；\n"
         "字面量 42 是**右值**，没有地址可以当别名，进不了 `H(int&)`，只能进 `H(const int&)`。\n"
         "B 把两者对调；C 以为 42 也能绑到非 const 引用（那会编译错，不是走同一个函数）；\n"
         "D 错，两个重载构成合法的重载集合。\n"
         "★ 注意边界：`void f(int)` 与 `void f(const int)` 是**同一个函数**（值形参的顶层 const\n"
         "对调用者不可见），不能重载；但「引用到 const」与「引用到非 const」是两个不同的类型，\n"
         "可以重载 —— 这一条是 const 参与重载的唯一入口。",
    tags=["引用", "重载解析", "const"], diff=4)

# =========================================================================
# 第 04 讲 · 类与对象（18 题）
# =========================================================================
_S = "第 04 讲 · 类与对象"

mcn(title="struct 与 class 的 sizeof",
    stmt=_stmt("在 64 位平台上，下面程序输出什么？", '''
        #include <iostream>

        struct S { int x; };
        class  C { int x; };

        int main() {
            std::cout << sizeof(S) << " " << sizeof(C) << std::endl;
        }
    '''),
    options=["4 4", "4 0", "0 4", "8 4"],
    value=cpp('''
        #include <iostream>
        struct S { int x; };
        class  C { int x; };
        int main() { std::cout << sizeof(S) << " " << sizeof(C) << std::endl; }
    '''),
    section=_S,
    expl="struct 与 class **唯一的语法差别是默认访问权限**（struct 缺省 public、class 缺省 private），"
         "成员布局完全一样：各有一个 int → `4 4`。\n"
         "B、C 把「默认 private」误解成「不占空间」—— 访问权限只影响能不能访问，不影响大小；"
         "D 多算了 4 字节。\n"
         "★ 顺带记住：**成员函数不占对象内存**（全类共享一份代码，靠 this 认主），"
         "只有数据成员（加对齐）计入 sizeof。",
    tags=["struct 定义", "class 定义", "sizeof 运算"], diff=1)

mcn(title="传统枚举与强类型枚举的取值",
    stmt=_stmt("下面程序输出什么？", '''
        #include <iostream>

        enum OldColor { oRed, oGreen, oBlue };
        enum class Color { Red, Green, Blue };

        int main() {
            OldColor oc = oGreen;
            std::cout << oc << " " << static_cast<int>(Color::Blue) << std::endl;
        }
    '''),
    options=["1 2", "0 2", "1 3", "2 1"],
    value=cpp('''
        #include <iostream>
        enum OldColor { oRed, oGreen, oBlue };
        enum class Color { Red, Green, Blue };
        int main() {
            OldColor oc = oGreen;
            std::cout << oc << " " << static_cast<int>(Color::Blue) << std::endl;
        }
    '''),
    section=_S,
    expl="枚举值从 **0** 起依次递增：oRed=0、oGreen=1、oBlue=2；"
         "Color::Red=0、Green=1、Blue=2 → 输出 `1 2`。\n"
         "传统 enum 能隐式转 int 所以可以直接打印；`enum class` **不能隐式转**，"
         "必须 `static_cast<int>` —— 这正是题里那个转换存在的原因。\n"
         "C 是以为从 1 起编号；D 把两个枚举的编号对调了；"
         "把 oGreen 当成 0 号（0 号是 oRed）也是常见错，那是漏数了第一个枚举值。",
    tags=["枚举", "强类型枚举"], diff=1)

tfn(title="析构函数能否重载",
    stmt="析构函数和构造函数一样可以重载 —— 只要参数表不同，就能定义多个析构函数。",
    answer=False, section=_S,
    expl="错。**构造函数可以重载**（同一个类有多种「生法」，参数不同即可），"
         "但**析构函数不可重载**：它无参、无返回值，一个类只能有一个 `~T()`"
         "（对象只有一种「死法」）。\n"
         "另外构造函数连 `void` 都不能写返回值；析构函数也没有 this 之外的参数。"
         "这两个「不能」是概念题的送分点，也是送命点。",
    tags=["析构函数", "重载"], diff=2)

_ORDER = '''
    #include <iostream>

    struct Part {
        char id;
        Part(char c) : id(c) { std::cout << "+" << id; }
        Part() { id = 'b'; std::cout << "+b"; }
        ~Part() { std::cout << "-" << id; }
    };

    class Whole {
        Part a_, b_, c_;                             // 声明顺序：a_ b_ c_
    public:
        Whole() : c_('c'), a_('a') { std::cout << "+W"; }   // 列表顺序故意写反
        ~Whole() { std::cout << "-W"; }
    };

    int main() {
        { Whole w; }
        std::cout << "|" << std::endl;
    }
'''
mcn(title="组合类构造与析构的执行顺序",
    stmt=_stmt("下面程序输出什么？", _ORDER),
    options=["+a+b+c+W-W-c-b-a|", "+c+a+b+W-W-b-a-c|",
             "+a+b+c+W-c-b-a-W|", "+W+a+b+c-W-c-b-a|"],
    value=cpp(_ORDER), section=_S,
    expl="构造顺序**只看成员声明顺序**：a_ → b_ → c_。初始化列表里写 `c_('c'), a_('a')` "
         "只决定「用什么值初始化」，**不决定顺序**；b_ 没进列表，走默认构造（打 `+b`）。"
         "成员全部就绪后才执行 Whole 的函数体 → `+W`。\n"
         "析构严格倒放：先跑自己的函数体 `-W`，再按 c_ → b_ → a_ 逆序析构。\n"
         "B 是按初始化列表的书写顺序；C 把 `-W` 排到了成员之后；D 把函数体当成了第一步。\n"
         "★ 列表顺序与声明顺序不一致时 g++ 直接给 `-Wreorder` 警告；"
         "更危险的是成员间有依赖（`Array arr_; int len_;`）时，先构造的 arr_ 会读到还没初始化的 len_。",
    tags=["构造顺序", "析构顺序", "组合类"], diff=2)

_COPY_CALLS = '''
    #include <iostream>

    struct Obj {
        static int copies;
        Obj() {}
        Obj(const Obj &) { ++copies; }
    };
    int Obj::copies = 0;

    void TakeByValue(Obj o) { }
    Obj  MakeObj() { Obj o; return o; }

    int main() {
        Obj a;
        Obj b = a;            // ①
        TakeByValue(a);       // ②
        MakeObj();            // ③
        std::cout << Obj::copies << std::endl;
    }
'''
mcn(title="复制构造函数的调用次数",
    stmt=_stmt("下面的程序用计数器统计复制构造函数被调用的次数。"
               "本题的结果按**禁用拷贝消除**（`-fno-elide-constructors`）编译运行 —— "
               "这样三个时机才都能看见。输出是多少？", _COPY_CALLS),
    options=["3", "2", "1", "4"],
    value=cpp(_COPY_CALLS, flags="-fno-elide-constructors"),
    section=_S,
    expl="三大时机各触发一次，共 **3** 次：\n"
         "① `Obj b = a;` 看着像赋值，其实是**初始化**（b 诞生这一刻用 a 复制构造）；\n"
         "② `TakeByValue(a)` 传值传参，形参是实参的副本；\n"
         "③ `MakeObj()` 传值返回，把函数里的局部 o 复制出去交给调用方。\n"
         "B 的 2 是**默认编译**的结果：③ 那次被拷贝消除（copy elision）省掉了，"
         "所以验证时机必须加 `-fno-elide-constructors`；C 只数了初始化；"
         "D 把「赋值」也算进去了 —— 若写 `Obj c; c = a;`，走的是 `operator=`，**不调**复制构造。",
    tags=["复制构造", "拷贝消除"], diff=2)

fillc(title="联合体的字节序读取",
      stmt=_stmt("在 x86（小端序）平台上，下面程序输出什么？", '''
        #include <iostream>

        union U { int i; char c[4]; };

        int main() {
            U u;
            u.i = 0x41424344;
            std::cout << u.c[0] << u.c[1] << u.c[2] << u.c[3] << std::endl;
        }
    '''),
      value=cpp('''
        #include <iostream>
        union U { int i; char c[4]; };
        int main() {
            U u;
            u.i = 0x41424344;
            std::cout << u.c[0] << u.c[1] << u.c[2] << u.c[3] << std::endl;
        }
    '''),
      section=_S,
      expl="union 的所有成员**共享同一块 4 字节**。x86 是**小端序**：低位字节 `0x44`（'D'）"
           "存在低地址 c[0]，所以按 c[0..3] 读出来是 **DCBA**。\n"
           "填 ABCD 是以为按书写顺序从高字节往低字节存；填 0x41424344 是没做「写 A 读 B」；"
           "填 44 是只读了一个字节。\n"
           "★ 写完一个成员读另一个，结果**依赖实现**（小端机器才看到 DCBA）—— "
           "拿它观察内存布局可以，拿它写业务是玩火；sizeof(U) 也等于最大成员 4，不是成员之和 8。",
      tags=["联合体", "字节序"], diff=3)

mcp(title="std::move 到底做了什么", answer="B",
    stmt="对一个左值对象执行 `std::move(a)`，它到底做了什么？",
    options=[
        "把源对象的数据逐个复制到目标对象，再把源对象清空",
        "只是把左值强制转换成右值引用，好让编译器选中移动构造",
        "直接把源对象所在的栈帧搬到目标对象的位置",
        "立刻释放源对象占用的堆内存",
    ],
    section=_S,
    expl="B。`std::move` 本身**不搬任何字节**，它就是一个到右值引用的 `static_cast`"
         "（「我的东西随便拿」的授权书）；真正干活的是移动构造 `X(X&&)`："
         "接管指针后把源对象**置空**，O(1) 完成。\n"
         "A 描述的是深复制（外加清空），那正是移动想避免的开销；C 是完全误解（栈帧不能搬）；"
         "D 更不对 —— 移动构造绝不释放资源，只是换了主人。\n"
         "★ 偷完必须置空，否则两个对象析构时对同一块内存 delete 两次 → 双重释放。"
         "move 之后源对象处于「有效但空」的状态，别再读它的值。",
    tags=["移动构造", "std::move 语义"], diff=3)

mcp(title="enum class 与 enum 的差别", answer="C",
    stmt="C++11 的 `enum class` 相比传统 `enum`，核心区别是什么？",
    options=[
        "enum class 的枚举值从 1 开始编号，传统 enum 从 0 开始",
        "enum class 的枚举值可以隐式转换成 int，传统 enum 不行",
        "enum class 的枚举值必须用枚举名限定，且不能隐式转 int",
        "enum class 不能指定底层类型，传统 enum 可以",
    ],
    section=_S,
    expl="C —— 正是「作用域限定」+「禁止隐式转换」这两条让它类型安全："
         "`Color::Blue` 必须带前缀，也不能跟整数或别的枚举混着比。\n"
         "A 错：两者都从 0 起编号。B 说反了 —— 能隐式转 int 的是传统 enum。"
         "D 也说反了：C++11 起两者都能指定底层类型（`enum X : char`）。\n"
         "教材以传统 enum 为主，但现代代码一律 `enum class`：它防住的正是「把状态值当整数乱比」。",
    tags=["强类型枚举", "类型安全"], diff=3)

multn(title="构造、析构与复制构造的多项辨析",
      stmt="关于构造函数、析构函数与复制构造函数，下列说法正确的有：",
      options=[
          "一旦自定义了任何构造函数，编译器就不再生成默认构造函数",
          "复制构造函数的参数必须是引用，否则会陷入无限递归",
          "构造函数可以写返回值类型，只要写成 void",
          "移动构造偷走资源后必须把源对象的指针置空，否则可能双重释放",
      ],
      answers=["A", "B", "D"], section=_S,
      expl="A 对：你写了 `T(int)`，`T a;` 就编译错 —— 默认构造被「挤掉」了，"
           "要补 `T() {}` 或 `T() = default;`。\n"
           "B 对：值传递参数要先复制实参 → 复制又调复制构造 → 无限套娃，"
           "编译器直接报 `invalid constructor; you probably meant 'X (const X&)'`。\n"
           "C 错：构造函数**连 void 都不写**，语法上就没有返回类型。\n"
           "D 对：不置空则是「一块内存两个主人」，析构时各 delete 一次 → 双重释放。",
      tags=["构造函数", "复制构造", "移动构造"], diff=4, rot=2)

mcp(title="const 成员与引用成员的初始化", answer="B",
    stmt="类里同时有 `const` 数据成员和引用成员时，下面哪条说法正确？",
    options=[
        "const 数据成员可以在构造函数体内赋值，只要保证只赋一次",
        "const 数据成员和引用成员都必须在构造函数的初始化列表里初始化",
        "const 数据成员只能在类外定义时初始化",
        "引用成员可以先默认构造，再在构造函数体里绑定",
    ],
    section=_S,
    expl="B。这两类成员「出生即定终身」：不允许先默认构造再赋值，"
         "构造函数体里写 `id = x;` 或 `r = x;` 直接编译错 —— 只能写进初始化列表。\n"
         "A 错在「赋值 = 修改」：const 成员一次都不许改。C 混淆了**静态数据成员**"
         "（那个才是类外定义初始化）；D 错在引用必须**立即绑定**，不存在「先空着」。\n"
         "★ 顺带的工程习惯：所有对象成员都写初始化列表，既避开这两类限制，"
         "也省掉「先默认构造再赋值覆盖」的双重开销。",
    tags=["const 成员", "初始化列表"], diff=4)

shortq(title="复制构造函数的三大调用时机",
       statement_md="**简答题**：复制构造函数 `X(const X &)` 在什么时刻会被调用？\n\n"
                    "请写出教材总结的**三大时机**，用「……、……、……」的句式一句话作答。",
       answers=[
           "用一个已存在的对象初始化新对象、对象作为实参传值、函数以传值方式返回对象",
           "对象初始化对象、传值传参、传值返回",
           "用同类型对象初始化新对象时，对象按值传参时，函数按值返回对象时",
       ],
       section=_S,
       explanation="三大时机：\n"
                   "① 用**已存在的对象初始化**新对象（`X b = a;` —— 这是初始化，不是赋值）；\n"
                   "② 对象**按值传参**（形参是实参的副本，每调一次复制一次）；\n"
                   "③ 函数**按值返回**对象（局部对象被复制出去交给调用方）。\n"
                   "★ 对照记：`X c; c = a;`（c 已存在）走的是**赋值运算符** `operator=`，"
                   "不调复制构造 —— 「新对象诞生」才叫初始化。\n"
                   "★ 验证时必须加 `-fno-elide-constructors`：默认编译下 ③ 那次常被**拷贝消除**吃掉"
                   "（同一份代码实测 3 次变 2 次），结论就做错了。",
       tags=["复制构造", "简答"], difficulty=4)

# ---- 以下为 2026-10 扩充：04 讲补到 20 题（理论 18 + 编程 2）----

# 无计算：概念题，按讲义口径判定（不跑代码）
tfn(title="自定义构造函数后默认构造是否还在",
    stmt="类里只写了一个带参数的构造函数，`T a;` 仍然合法，编译器会自动补一个默认构造函数。",
    answer=False, section=_S,
    expl="错。**一旦自定义了任何构造函数，编译器就不再生成默认构造函数** —— \n"
         "`T a;` 直接编译错（`no matching function for call to 'T::T()'`）。\n"
         "两个补救办法：自己写 `T() {}`，或 C++11 的 `T() = default;`（意图更明确）。\n"
         "反过来：一个构造函数都没写的类，编译器才白送默认构造 —— 但那个版本对内置类型成员\n"
         "**不做初始化**（`int x;` 里是垃圾值），不是「清零」。\n"
         "★ 同一族考点：`T a;` 与 `T a();` 不是一回事 —— 后者是**函数声明**（最令人头疼的\n"
         "most vexing parse），要造对象就别加那对空括号。",
    tags=["构造函数", "默认构造"], diff=2)

mcn(title="委托构造先执行目标还是先执行本体重",
    stmt=_stmt("默认构造把初始化工作委托给带参版本。下面程序输出什么？", '''
        #include <iostream>

        struct D {
            D(int x) { std::cout << "target "; }
            D() : D(0) { std::cout << "delegate"; }
        };

        int main() {
            D d;
            std::cout << std::endl;
        }
    '''),
    options=["target delegate", "delegate target", "target", "delegate"],
    value=cpp('''
        #include <iostream>
        struct D {
            D(int x) { std::cout << "target "; }
            D() : D(0) { std::cout << "delegate"; }
        };
        int main() { D d; std::cout << std::endl; }
    '''),
    section=_S,
    expl="输出 `target delegate`。委托构造把活儿**转包**出去，执行顺序是铁律：\n"
         "**先跑完被委托的那个构造函数（含它的初始化列表），再执行委托者自己的函数体**。\n"
         "B 把顺序当成了先跑本体；C、D 各漏了一半。\n"
         "★ 这条顺序与「成员先于函数体」同源：所有初始化动作都排在函数体之前。\n"
         "委托构造的价值是消除重复的初始化代码 —— 多个构造函数共用一个「真正的」版本，\n"
         "改一处就够；但别写环形委托（`D() : D(1)` 又 `D(int) : D()`），编译器会报错。",
    tags=["委托构造", "构造顺序"], diff=3)

mcn(title="对象数组的构造与析构编号顺序",
    stmt=_stmt("`P` 在构造/析构时打印自己的编号。下面程序输出什么？", '''
        #include <iostream>

        struct P {
            static int k;
            int id;
            P() : id(k++) { std::cout << "+" << id; }
            ~P() { std::cout << "-" << id; }
        };
        int P::k = 0;

        int main() {
            { P p[3]; }
            std::cout << std::endl;
        }
    '''),
    options=["+0+1+2-2-1-0", "+0+1+2-0-1-2", "+0+1+2+0+1+2", "-0-1-2+0+1+2"],
    value=cpp('''
        #include <iostream>
        struct P {
            static int k;
            int id;
            P() : id(k++) { std::cout << "+" << id; }
            ~P() { std::cout << "-" << id; }
        };
        int P::k = 0;
        int main() {
            { P p[3]; }
            std::cout << std::endl;
        }
    '''),
    section=_S,
    expl="输出 `+0+1+2-2-1-0`。`P p[3]` 按下标 **0→1→2** 依次默认构造；\n"
         "出块时三个对象**严格逆序**析构 **2→1→0**（后构造的先死）。\n"
         "B 以为析构也按正序；C 把析构也打成了 `+`（同号）；D 把构造写在了析构之后。\n"
         "★ 两条附带考点：① 对象数组要求元素类型有**可用的默认构造**（无形参，或全部形参都有\n"
         "默认值），否则编译错；② 局部对象数组的生存期跟着**作用域**走，右花括号一到就整体析构。\n"
         "把 `+`/`-` 换成构造/析构的计数，就是第 6 讲 new[]/delete[] 配对实验的栈版本。",
    tags=["构造顺序", "析构顺序", "对象数组"], diff=3)

mcn(title="已存在对象之间赋值是否触发复制构造",
    stmt=_stmt("`copies` 只统计复制构造函数。`c` 已经构造完成后再赋值，输出是多少？", '''
        #include <iostream>

        struct Obj {
            static int copies;
            int v = 0;
            Obj() {}
            Obj(const Obj &) { ++copies; }
            Obj &operator=(const Obj &o) { v = o.v; return *this; }
        };
        int Obj::copies = 0;

        int main() {
            Obj a;
            Obj c;
            c = a;
            std::cout << Obj::copies << std::endl;
        }
    '''),
    options=["0", "1", "2", "3"],
    value=cpp('''
        #include <iostream>
        struct Obj {
            static int copies;
            int v = 0;
            Obj() {}
            Obj(const Obj &) { ++copies; }
            Obj &operator=(const Obj &o) { v = o.v; return *this; }
        };
        int Obj::copies = 0;
        int main() {
            Obj a; Obj c; c = a;
            std::cout << Obj::copies << std::endl;
        }
    '''),
    section=_S,
    expl="输出 **0**。`Obj c;` 那一句已经把 c **构造完成**了，`c = a;` 走的是**赋值运算符**\n"
         "`operator=`，一次复制构造都不调。\n"
         "B 是把 `c = a` 当成了初始化；C、D 是把构造 a、c 也算进了复制计数。\n"
         "★ 判据只有一句：**新对象诞生 = 初始化（复制构造）；对象已存在 = 赋值（operator=）**。\n"
         "写成 `Obj b = a;` 才是初始化（看着像赋值，实为复制构造）；\n"
         "写成 `Obj b(a);` 也是初始化。三种写法里只有第一种最容易被误读。\n"
         "这也是 Rule of Three 里 `operator=` 不能漏的原因：漏了它，赋值就走默认的浅拷贝。",
    tags=["复制构造", "赋值运算符"], diff=3)

mcn(title="类内默认成员初值与初始化列表的优先级",
    stmt=_stmt("成员在声明处给了默认值，构造函数又用初始化列表覆盖其中一个。输出什么？", '''
        #include <iostream>

        struct S {
            int a = 1;
            int b = 5;
            S() : a(2) {}
        };

        int main() {
            S s;
            std::cout << s.a << " " << s.b << std::endl;
        }
    '''),
    options=["2 5", "1 5", "1 0", "2 0"],
    value=cpp('''
        #include <iostream>
        struct S { int a = 1; int b = 5; S() : a(2) {} };
        int main() { S s; std::cout << s.a << " " << s.b << std::endl; }
    '''),
    section=_S,
    expl="输出 `2 5`。`int a = 1;` 是 **C++11 的默认成员初值**，而初始化列表 `a(2)` 优先级更高，\n"
         "把它覆盖成 2；b 没进列表，用默认成员初值 5。\n"
         "B 以为默认初值赢；C、D 忘了默认成员初值会生效（不是 0，也不是不初始化）。\n"
         "★ 优先级：**初始化列表 > 默认成员初值 > 内置类型不初始化（垃圾值）**。\n"
         "默认成员初值的价值是「让每个构造函数都自动带上兜底值」，省掉在多处重复写同样的初始化；\n"
         "但注意成员**构造顺序仍看声明顺序**，与初始化列表和默认初值的书写位置都无关。",
    tags=["初始化列表", "默认成员初值"], diff=3)

mcn(title="char 与 int 成员的结构体对齐大小", rot=0,
    stmt=_stmt("在 64 位平台上，下面程序输出什么？", '''
        #include <iostream>

        struct A {
            char c;
            int i;
        };

        int main() {
            std::cout << sizeof(A) << " " << sizeof(A::c) << std::endl;
        }
    '''),
    options=["5 1", "8 1", "8 4", "4 1"],
    value=cpp('''
        #include <iostream>
        struct A { char c; int i; };
        int main() { std::cout << sizeof(A) << " " << sizeof(A::c) << std::endl; }
    '''),
    section=_S,
    expl="输出 `8 1`。`char c` 只占 1 字节，但 `int i` 要求地址是 4 的倍数，\n"
         "编译器在 c 后面**填 3 个字节空洞**，i 从偏移 4 开始 → sizeof(A) = **8**。\n"
         "`sizeof(A::c)` 量的是成员**类型**的大小，仍是 1。\n"
         "A 是简单相加 1+4=5（忽略对齐）；C 把 char 也当成 4 字节；D 把结构体算成 4（只看了 int）。\n"
         "★ 成员声明顺序会影响 sizeof：`char c; int i; char d;` 会变成 12（尾部还要补齐）；\n"
         "把大的成员放前面（`int i; char c; char d;`）能压到 8 —— 这就是「按大小降序排成员」的由来。",
    tags=["内存对齐", "sizeof 运算"], diff=3)

mcn(title="移动构造后源对象的指针与长度",
    stmt=_stmt("`Buf` 的移动构造偷走指针并把源对象置空。下面程序输出什么？", '''
        #include <iostream>

        struct Buf {
            int *data;
            int n;
            Buf(int n) : data(new int[n]), n(n) {}
            Buf(Buf &&o) noexcept : data(o.data), n(o.n) { o.data = nullptr; o.n = 0; }
            ~Buf() { delete[] data; }
        };

        int main() {
            Buf a(3);
            Buf c = std::move(a);
            std::cout << (a.data == nullptr) << " " << a.n << " " << c.n << std::endl;
        }
    '''),
    options=["1 0 3", "0 0 3", "1 3 3", "1 3 0"],
    value=cpp('''
        #include <iostream>
        struct Buf {
            int *data;
            int n;
            Buf(int n) : data(new int[n]), n(n) {}
            Buf(Buf &&o) noexcept : data(o.data), n(o.n) { o.data = nullptr; o.n = 0; }
            ~Buf() { delete[] data; }
        };
        int main() {
            Buf a(3);
            Buf c = std::move(a);
            std::cout << (a.data == nullptr) << " " << a.n << " " << c.n << std::endl;
        }
    '''),
    section=_S,
    expl="输出 `1 0 3`。移动构造把指针**偷**过去（c.data 接管），随后必须把源对象**置空**：\n"
         "`o.data = nullptr; o.n = 0;` —— 所以 a.data 是空（判空得 1）、a.n 归 0，资源现在归 c、\n"
         "c.n 仍是 3。\n"
         "B 以为源对象还留着指针（那就成了「一块内存两个主人」）；C、D 把 n 的归属弄反了。\n"
         "★ 不置空的后果：两个对象析构时对同一块 `delete[]` → **双重释放**。\n"
         "置空之后源对象处于「有效但空」的状态，还能安全析构、还能重新赋值，但**别再读它的值**。\n"
         "★ 另记一条：`std::move(a)` 本身不搬任何字节，它只是把 a 转成右值引用，\n"
         "真正干活的是移动构造 —— 授权书和搬家是两件事。",
    tags=["移动构造", "资源所有权"], diff=4)

# =========================================================================
# 第 05 讲 · 数据的共享与保护（19 题）
# =========================================================================
_S = "第 05 讲 · 数据的共享与保护"

mcn(title="静态局部变量的累加输出",
    stmt=_stmt("下面程序输出什么？", '''
        #include <iostream>

        int f() {
            static int n = 0;
            n += 2;
            return n;
        }

        int main() {
            std::cout << f() << " " << f() << " " << f() << std::endl;
        }
    '''),
    options=["2 4 6", "2 2 2", "0 2 4", "6 4 2"],
    value=cpp('''
        #include <iostream>
        int f() {
            static int n = 0;
            n += 2;
            return n;
        }
        int main() {
            std::cout << f() << " " << f() << " " << f() << std::endl;
        }
    '''),
    section=_S,
    expl="`static int n = 0;` 的初始化**只执行一次**，之后跨调用保留上一次的值：2 → 4 → 6。\n"
         "B 是把它当普通局部变量（每次进函数重新置 0）；C 是以为先返回再累加；D 顺序反了。\n"
         "★ 静态局部变量的**生存期**与全局对象一样长（程序结束才析构），"
         "但**作用域**仍是块作用域 —— 出了函数这个名字就不可见，对象却还活着。",
    tags=["static 修饰", "局部变量"], diff=1)

mcn(title="静态数据成员的构造计数",
    stmt=_stmt("下面程序输出什么？", '''
        #include <iostream>

        class Counter {
        public:
            Counter() { ++count; }
            static int count;
        };

        int Counter::count = 0;          // 类外定义并初始化

        int main() {
            Counter a, b, c;
            std::cout << Counter::count << std::endl;
        }
    '''),
    options=["3", "0", "1", "2"],
    value=cpp('''
        #include <iostream>
        class Counter {
        public:
            Counter() { ++count; }
            static int count;
        };
        int Counter::count = 0;
        int main() {
            Counter a, b, c;
            std::cout << Counter::count << std::endl;
        }
    '''),
    section=_S,
    expl="静态数据成员**全类共享一份**，三个对象的构造各 +1 → **3**。\n"
         "B 是以为每次构造都重置（把它当普通成员）；C 是把静态成员误当「只算一次」；"
         "D 是少数了一个对象。\n"
         "★ 类内 `static int count;` 只是**声明**，没有分配存储；必须类外 "
         "`int Counter::count = 0;` 才有着落。漏了这行：**编译通过、连接失败**"
         "（`undefined reference to Counter::count`）—— 最常见的坑。\n"
         "唯一例外：`static const int N = 10;` 可以类内直接初始化。",
    tags=["静态数据成员", "计数器"], diff=2)

tfn(title="静态成员函数没有 this 的后果",
    stmt="静态成员函数没有 this 指针，因此它不能访问本类的**非静态**数据成员。",
    answer=True, section=_S,
    expl="对。非静态数据成员必须靠 this 才能知道「是哪个对象的」，"
         "而静态成员函数压根没被传入这个隐形参数 → 直接写 `balance += amt;` 编译错"
         "（`invalid use of member in static member function`）。\n"
         "但注意：访问**静态**数据成员完全没问题（静态成员也不需要 this），"
         "而且它照样能用 `类名::函数()` 调用 —— 这两条正是它存在的意义。\n"
         "要碰对象数据，就把对象引用当参数传进来。",
    tags=["静态成员函数", "this 指针"], diff=2)

mcn(title="作用域分辨符读取全局变量",
    stmt=_stmt("下面程序输出什么？", '''
        #include <iostream>

        int v = 1;

        int main() {
            {
                int v = 2;
                {
                    int v = 3;
                    std::cout << ::v + v << " ";
                }
                std::cout << v << std::endl;
            }
        }
    '''),
    options=["4 2", "6 3", "4 3", "3 2"],
    value=cpp('''
        #include <iostream>
        int v = 1;
        int main() {
            {
                int v = 2;
                {
                    int v = 3;
                    std::cout << ::v + v << " ";
                }
                std::cout << v << std::endl;
            }
        }
    '''),
    section=_S,
    expl="最内层的 `v` 是 3；`::v` 用**作用域分辨符**穿透到全局的 1 → 4。"
         "出了最内层块，`v` 重新被中层的 2 接管 → 2。所以是 `4 2`。\n"
         "C 是出了块还读内层；D 是漏了 `::v` 的那一半（或把全局当成 1 却没相加）；"
         "把两个块的 v 直接相加得 6，是误以为 `::v` 取的是外层局部。\n"
         "★ 可见性规则：**内层遮住外层，出块自动还回去**；"
         "`::` 只能到全局 / 命名空间，**够不着外层函数的局部变量** —— 那样写直接编译错"
         "（`'::v' has not been declared`）。",
    tags=["作用域", "可见性"], diff=2)

mcn(title="const 指针的管物与管路",
    stmt=_stmt("下面程序输出什么？", '''
        #include <iostream>

        int main() {
            int x = 1, y = 2;

            const int *p = &x;      // 指向常量的指针
            p = &y;                 // 改指向：允许
            std::cout << *p << " ";

            int *const q = &x;      // 常指针
            *q = 10;                // 改内容：允许
            std::cout << x << std::endl;
        }
    '''),
    options=["2 10", "1 10", "2 1", "1 2"],
    value=cpp('''
        #include <iostream>
        int main() {
            int x = 1, y = 2;
            const int *p = &x;
            p = &y;
            std::cout << *p << " ";
            int *const q = &x;
            *q = 10;
            std::cout << x << std::endl;
        }
    '''),
    section=_S,
    expl="`const int *p` 是「指向常量的指针」：`*p` 不能改，但 **p 可以改指向**，"
         "所以改指 y 后 `*p` 是 2。`int *const q` 是「常指针」：q 死守 &x，"
         "但 **`*q` 能改**，于是 x 变成 10。\n"
         "C、D 是把两者记反了（也是最经典的错法）；B 是漏了 `p = &y` 那一步，"
         "`*p` 仍停在 1。\n"
         "★ 口诀：**const 在 `*` 前管「物」，const 在 `*` 后管「路」**；"
         "两个都写（`const int *const p`）就物、路全锁死。",
    tags=["const 指针", "指针"], diff=3)

fillc(title="静态局部变量第三次调用的返回值",
      stmt=_stmt("下面程序输出什么？", '''
        #include <iostream>

        int f() {
            static int n = 0;
            n += 2;
            return n;
        }

        int main() {
            f();
            f();
            std::cout << f() << std::endl;
        }
    '''),
      value=cpp('''
        #include <iostream>
        int f() {
            static int n = 0;
            n += 2;
            return n;
        }
        int main() {
            f();
            f();
            std::cout << f() << std::endl;
        }
    '''),
      section=_S,
      expl="前两次调用把 n 累到 4（先 2、再 4），第三次再加 2 → **6**。\n"
           "填 2 是把它当普通局部变量（每次重新初始化为 0 再加 2）；"
           "填 4 是数错了调用次数（那是第二次的返回值）；填 3 是把它当每次 +1。\n"
           "★ 只初始化一次、跨调用保留 —— 这两条让静态局部变量常被用来做「计数器 / 单次初始化」。",
      tags=["static 修饰", "局部变量"], diff=3)

tfn(title="友元关系能否传递",
    stmt="若 B 是 A 的友元类、C 是 B 的友元类，则 C 也是 A 的友元类。",
    answer=False, section=_S,
    expl="错。友元三性：**单向、不传递、不继承**。\n"
         "- 单向：A 声明 B 是友元，只有 B 能进 A；A 进不了 B。\n"
         "- 不传递：B 的朋友（C）不是 A 的朋友 —— C 想访问 A 的私有成员，必须 A 亲自写 "
         "`friend class C;`。\n"
         "- 不继承：B 的派生类也不是 A 的友元。\n"
         "★ 友元不是成员：写在哪一区（public/private）都不影响它的效力，"
         "它也没有 this、不占对象内存。",
    tags=["友元", "封装"], diff=3)

mcn(title="含静态成员的类对象大小",
    stmt=_stmt("在 64 位平台上，下面程序输出什么？", '''
        #include <iostream>

        class A {
            double d;
            static int n;        // 静态数据成员：全类共享
        };

        int A::n = 0;

        int main() {
            std::cout << sizeof(A) << std::endl;
        }
    '''),
    options=["8", "12", "16", "4"],
    value=cpp('''
        #include <iostream>
        class A {
            double d;
            static int n;
        };
        int A::n = 0;
        int main() { std::cout << sizeof(A) << std::endl; }
    '''),
    section=_S,
    expl="**静态数据成员不属于任何对象**：它存在静态存储区、全类只有一份，"
         "所以对象里只剩一个 double → **8** 字节。\n"
         "B 的 12 是把它当普通成员算进去（8+4）；C 的 16 又加了 8 字节对齐填充；"
         "D 只数了静态成员。\n"
         "★ 同样的道理：**成员函数也不占对象内存**，全类共享一份代码，靠 this 认出调用者。"
         "sizeof(类) 只统计非静态数据成员（加对齐）。",
    tags=["静态数据成员", "sizeof 运算"], diff=3)

multn(title="const 与 static 成员的多项辨析",
      stmt="关于 `const` 与 `static` 修饰的成员，下列说法正确的有：",
      options=[
          "常对象只能调用常成员函数，非常成员函数一律被拒绝",
          "常成员函数只能被常对象调用",
          "静态数据成员必须在类外定义并初始化，漏写会在连接阶段报 undefined reference",
          "常数据成员必须在构造函数的初始化列表里初始化",
      ],
      answers=["A", "C", "D"], section=_S,
      expl="A 对：常对象的 this 是 const 的，非常成员函数可能修改数据 → 编译错 "
           "`passing 'const Account' as 'this' argument discards qualifiers`。\n"
           "B 错，说反了：常成员函数**任何对象都能调**（常的非常的都行）—— "
           "这正是「不会改数据成员的函数一律加 const」的理由：给别人留访问权。\n"
           "C 对：类内只是声明，没有分配存储；漏了类外定义 = 编译过、连接失败。\n"
           "D 对：const 成员不接受赋值，初始化列表是唯一出生通道。\n"
           "★ 补充：`static const int` 是唯一可以类内直接初始化的静态成员例外。",
      tags=["const 修饰", "static 修饰", "多选"], diff=4, rot=1)

mcp(title="条件编译开关的作用", answer="C",
    stmt="关于用 `#define DEBUG` / `#ifdef DEBUG` 控制调试输出的做法，下列说法正确的是：",
    options=[
        "#ifdef 包住的代码块在程序运行时才判断是否执行",
        "注释掉 #define DEBUG 后，#ifdef DEBUG 块里的代码仍然会被编译进可执行文件",
        "未定义 DEBUG 时，#ifdef DEBUG 包住的代码在预处理阶段就被剔除，不产生任何机器码",
        "#ifdef 是 C++ 的运行时分支语句，与 if 等价",
    ],
    section=_S,
    expl="C。`#` 开头的活全在**预处理阶段**做完（文本替换、条件裁剪），"
         "编译器根本看不到被剔除的那些行，所以 release 版里调试输出是**零成本**的 —— "
         "没有判断、也没有体积。\n"
         "A、D 把它当运行时分支：那要用 `if (debug)`，至少还要付出一次判断和代码体积的代价。"
         "B 错：注释掉 `#define` 后那些行根本不参与编译。\n"
         "★ 完整链条：预处理 → 编译（.cpp→.o）→ 连接（.o→exe）→ 运行。",
    tags=["预处理", "条件编译"], diff=4)

# ---- 以下为 2026-10 扩充：05 讲补到 20 题（理论 19 + 编程 1）----

# 无计算：概念题，按讲义口径判定（不跑代码）
tfn(title="static 修饰全局变量后的作用域",
    stmt="在源文件里用 `static` 修饰一个全局变量，它的作用域就被限制在本编译单元（本文件）内。",
    answer=True, section=_S,
    expl="对。文件作用域的 `static` 把**连接属性**改成内部链接：别的 .cpp 看不见这个名字，\n"
         "也就不会在连接阶段撞出 `multiple definition`。这是「同一个名字在不同文件里各用各的」\n"
         "最省事的做法（C++ 里更现代的同款是匿名命名空间）。\n"
         "★ 别和作用域搞混：它改的是**可见范围**（本文件内可见），**生存期**仍是静态生存期 ——\n"
         "程序启动时构造、程序结束时析构。\n"
         "★ 对照记忆：static 修饰**局部变量**改的是**生存期**（活到程序结束）；\n"
         "修饰**全局变量/函数**改的是**链接属性**（本文件私有）；修饰**类成员**改的是**归属**（全类共享）。\n"
         "同一个关键字，三处三种含义 —— 这是第 5 讲最爱出的辨析。",
    tags=["static 修饰", "作用域"], diff=2)

mcn(title="静态常量整型成员的类内初始化", rot=0,
    stmt=_stmt("类里只有一个静态常量成员和若干空成员函数。下面程序输出什么？", '''
        #include <iostream>

        class A {
        public:
            static const int N = 10;
        };

        int main() {
            std::cout << A::N << " " << sizeof(A) << std::endl;
        }
    '''),
    options=["10 4", "0 1", "编译错", "10 1"],
    value=cpp('''
        #include <iostream>
        class A { public: static const int N = 10; };
        int main() { std::cout << A::N << " " << sizeof(A) << std::endl; }
    '''),
    section=_S,
    expl="输出 `10 1`。`static const int` 是**唯一可以类内直接初始化**的静态成员（整型常量），\n"
         "读它得 10。而它属于**类**、不属于对象，所以 sizeof(A) 里没有它的位置 —— \n"
         "空类要占 **1 字节**（标准要求每个对象有唯一地址），所以是 1 而不是 0。\n"
         "A 把 N 当普通成员算进了对象；B 以为没写类外定义就读不到（只有**取它的地址**时\n"
         "才需要类外定义 `const int A::N;`）；C 错，这是合法写法。\n"
         "★ 一般静态数据成员必须「类内声明 + 类外定义」：漏了类外定义是**编译通过、连接失败**\n"
         "（`undefined reference`）。非 const 的静态成员连类内初始化都不允许。",
    tags=["静态数据成员", "常量成员", "sizeof 运算"], diff=2)

# 无计算：概念题，按讲义口径判定（不跑代码）
tfn(title="静态成员函数能否调用非静态成员函数",
    stmt="静态成员函数里可以直接调用本类的非静态成员函数，只要不访问数据成员就行。",
    answer=False, section=_S,
    expl="错。非静态成员函数的调用**必须有一个 this**（它自己也要靠 this 认出「操作哪个对象」），\n"
         "而静态成员函数压根没被传这个隐形参数 → 直接编译错\n"
         "（`cannot call member function without object`）。\n"
         "两条边界一起记：静态成员函数**能**访问静态成员（静态成员也不需要 this）、\n"
         "**不能**访问非静态数据成员、也**不能**调用非静态成员函数。\n"
         "★ 要碰对象数据，就把对象引用当参数传进来：`static void f(A &a) { a.deposit(1); }`。\n"
         "这也是静态成员函数适合做「工具函数 / 工厂函数」的原因 —— 它不依赖任何具体对象。",
    tags=["静态成员函数", "this 指针"], diff=2)

# 无计算：概念题，按讲义口径判定（不跑代码）
tfn(title="友元授权是不是单向的",
    stmt="若类 A 把类 B 声明为友元，则 A 也能访问 B 的私有成员。",
    answer=False, section=_S,
    expl="错。友元是**单向授权**：`friend class B;` 写在 A 里，只让 B 进 A；\n"
         "A 想进 B，必须 B 自己写一句 `friend class A;`。\n"
         "三性一起背：**单向、不传递、不继承** ——\n"
         "B 的朋友 C 不是 A 的友元；B 的派生类也不是 A 的友元。\n"
         "★ 另外两条常考点：友元**不是成员**，写在哪一区（public/private）都同样生效，\n"
         "它没有 this、不占对象内存、不能被继承。\n"
         "友元是对封装的**有节制破坏** —— 报表函数、`operator<<` 这类「天然需要看内部」的\n"
         "角色才用它，别拿它绕开封装做本该是成员函数的事。",
    tags=["友元", "封装"], diff=2)

mcn(title="静态局部对象在何时才构造",
    stmt=_stmt("`f` 里有一个静态局部对象和一个普通输出。`f` 被调用两次，程序输出什么？", '''
        #include <iostream>

        struct L {
            const char *n;
            L(const char *s) : n(s) { std::cout << "ctor-" << n << " "; }
            ~L() { std::cout << "dtor-" << n; }
        };

        void f() {
            static L s("s");
            std::cout << "in ";
        }

        int main() {
            std::cout << "main ";
            f();
            f();
            std::cout << "end ";
        }
    '''),
    options=["main ctor-s in in end dtor-s",
             "ctor-s main in in end dtor-s",
             "main in in end ctor-s dtor-s",
             "main ctor-s in ctor-s in end dtor-s"],
    value=cpp('''
        #include <iostream>
        struct L {
            const char *n;
            L(const char *s) : n(s) { std::cout << "ctor-" << n << " "; }
            ~L() { std::cout << "dtor-" << n; }
        };
        void f() { static L s("s"); std::cout << "in "; }
        int main() {
            std::cout << "main ";
            f();
            f();
            std::cout << "end ";
        }
    '''),
    section=_S,
    expl="输出 `main ctor-s in in end dtor-s`。静态局部对象的三特征是本题的全部考点：\n"
         "① **首次执行到声明处**才构造（不是 main 之前，也不是每次进函数）；\n"
         "② 只构造一次 —— 第二次进 f 不再打印 ctor，所以输出里只有一个 `ctor-s`；\n"
         "③ 析构在 **main 返回之后**（生存期到程序结束），晚于普通局部对象。\n"
         "B 把它当成了全局对象（main 之前构造）；C 以为要先声明后使用、构造拖到最后；\n"
         "D 以为每次调用都重新构造（那是普通局部对象）。\n"
         "★ 记住这条组合：**静态局部变量 = 块作用域（名字出函数就不可见）+ 静态生存期（对象活到程序结束）**。\n"
         "「作用域」和「生存期」是两套独立的体系，别用一个去推另一个。",
    tags=["静态生存期", "局部对象"], diff=3)

mcn(title="全局对象的构造与析构相对 main 的位置",
    stmt=_stmt("`g` 是全局对象，构造和析构都会打印。下面程序输出什么？", '''
        #include <iostream>

        struct G {
            G()  { std::cout << "ctor "; }
            ~G() { std::cout << "dtor"; }
        };

        G g;

        int main() {
            std::cout << "main ";
        }
    '''),
    options=["ctor main dtor", "main ctor dtor", "ctor dtor main", "main dtor ctor"],
    value=cpp('''
        #include <iostream>
        struct G { G() { std::cout << "ctor "; } ~G() { std::cout << "dtor"; } };
        G g;
        int main() { std::cout << "main "; }
    '''),
    section=_S,
    expl="输出 `ctor main dtor`。全局对象在 **main 之前**构造（程序启动时就建好），\n"
         "在 **main 返回之后**析构 —— 它的生存期覆盖整个程序。\n"
         "B 以为进了 main 才构造；C 把析构提前到了 main 之前；D 整个倒过来了。\n"
         "★ 多个全局/静态对象按**构造的逆序**析构（后构造的先死），与局部对象同一个规矩。\n"
         "★ 工程含义：全局对象的构造函数里别依赖别的全局对象 —— 跨编译单元时**谁先构造没有保证**\n"
         "（静态初始化顺序问题）。需要「用时才建」就改用函数内的静态局部对象（第一次调用时构造）。",
    tags=["静态生存期", "全局对象"], diff=3)

# 无计算：概念题，按讲义口径判定（不跑代码）
tfn(title="const 引用形参能否绑定字面量",
    stmt="`void f(const int &r);` 可以用 `f(42)` 调用，而 `void f(int &r);` 不行。",
    answer=True, section=_S,
    expl="对。非 const 引用只能绑定**左值**：字面量 42 是右值，没有地址可以当别名，\n"
         "`f(42)` 直接编译错。而 `const int&` 会为这个临时量开一块只读空间并**延长其寿命**，\n"
         "所以 42 能进来。\n"
         "★ 这就是「只读参数一律写 `const &`」的双重收益：既避免大对象整体复制，\n"
         "又能接临时量/右值 —— 传字面量、传表达式结果、传返回值都不会被挡在门外。\n"
         "第 4 章复制构造参数写 `const X&` 而不是 `X&`，一半原因就在这里（另一半是\n"
         "值传递会引发「复制复制构造的参数」的无限递归）。\n"
         "★ 反过来：如果你写 `void f(X&)`，调用者就**不能**传临时对象 —— 这是有意限制，\n"
         "表示「我要改你，所以你必须是个真实存在、活得够久的对象」。",
    tags=["const 引用", "左值右值"], diff=3)

mcn(title="常对象与非常对象各选中哪个 const 重载", rot=0,
    stmt=_stmt("类里同时提供了 const 版与普通版的 `f`。下面程序输出什么？", '''
        #include <iostream>

        struct Cfg {
            void f()       { std::cout << "nonconst"; }
            void f() const { std::cout << "const"; }
        };

        int main() {
            Cfg a;
            const Cfg &ca = a;
            a.f();
            std::cout << " ";
            ca.f();
            std::cout << std::endl;
        }
    '''),
    options=["const nonconst", "nonconst nonconst", "nonconst const", "const const"],
    value=cpp('''
        #include <iostream>
        struct Cfg {
            void f()       { std::cout << "nonconst"; }
            void f() const { std::cout << "const"; }
        };
        int main() {
            Cfg a; const Cfg &ca = a; a.f(); std::cout << " "; ca.f(); std::cout << std::endl;
        }
    '''),
    section=_S,
    expl="输出 `nonconst const`。`void f()` 与 `void f() const` 是**合法的重载** ——\n"
         "它们真正的差别是隐藏参数 this 的类型（`Cfg*` vs `const Cfg*`）。\n"
         "普通对象 a 精确匹配非 const 版；`const Cfg& ca` 的**静态类型带 const**，\n"
         "只能调 const 版 → `nonconst const`。\n"
         "A 把两者对调；B、D 以为常对象只有一种选择。\n"
         "★ 反过来不成立：**常成员函数任何对象都能调**（常的非常的都行）——\n"
         "所以「不会修改数据成员的函数一律加 const」不是自缚手脚，而是给别人留访问权。\n"
         "★ 注意 ca 绑定的是同一个对象 a，两个版本的函数操作的是同一份数据；\n"
         "编译器只看**引用的静态类型**，不看它实际指向谁。",
    tags=["常成员函数", "const 重载"], diff=4)

# 无计算：概念题，按讲义口径判定（不跑代码）
mcp(title="头文件里直接定义全局变量的连接后果", answer="C",
    stmt="一个头文件里写了 `int g_count = 0;`（不是 `extern` 声明），被两个 .cpp 同时 include。会发生什么？",
    options=[
        "两份 g_count 各自独立存在，程序里就有两个计数器",
        "编译阶段立刻报错，因为头文件里不允许写变量定义",
        "每个 .cpp 都能单独编译通过，连接时报告 multiple definition of 'g_count'",
        "连接器会自动把它们合并成一个 g_count，什么都不会发生",
    ],
    section=_S,
    expl="C。`#include` 是**文本复制**：两个编译单元各自带上了 `int g_count = 0;` 这份**定义**，\n"
         "各自编译都毫无问题，到了**连接**阶段才撞车（`multiple definition of 'g_count'`）。\n"
         "改法：头文件里只放 `extern int g_count;`（**声明**），定义放到某一个 .cpp 里。\n"
         "A 错在把两份定义当成两个独立变量 —— 同名外部链接的全局变量不可能共存；\n"
         "B 错在阶段（编译期看不到另一个编译单元，无从发现）；D 没有这种自动合并。\n"
         "★ 这与「静态数据成员必须类外定义」是同一原理的两副面孔：\n"
         "**声明可以有无数份，定义只能一份**。也正因为如此，头文件里的类定义、函数声明、\n"
         "`constexpr` 变量都能重复出现，唯独「会分配存储的定义」不行。",
    tags=["多文件结构", "连接错误"], diff=4)

# =========================================================================
# 第 06 讲 · 数组、指针与字符串（18 题）
# =========================================================================
_S = "第 06 讲 · 数组指针与字符串"

mcn(title="指针下标与解引用的等价输出",
    stmt=_stmt("下面程序输出什么？", '''
        #include <iostream>

        int main() {
            int a[5] = {10, 20, 30, 40, 50};
            int *p = a;
            std::cout << *(p + 2) << " " << *(a + 4) << " " << p[1] << std::endl;
        }
    '''),
    options=["30 50 20", "30 50 10", "20 40 10", "30 40 20"],
    value=cpp('''
        #include <iostream>
        int main() {
            int a[5] = {10, 20, 30, 40, 50};
            int *p = a;
            std::cout << *(p + 2) << " " << *(a + 4) << " " << p[1] << std::endl;
        }
    '''),
    section=_S,
    expl="`*(p + 2)` = a[2] = 30；`*(a + 4)` = a[4] = 50；`p[1]` 编译器就当 `*(p + 1)` = 20。\n"
         "★ `a[i]` 与 `*(a + i)` **完全等价** —— 下标只是指针运算的语法糖，"
         "所以 `p[1]`、`*(p+1)`、`1[p]` 都能取出同一个元素。\n"
         "B 把 `p[1]` 当成了 a[0]；C、D 是下标算错（把偏移量当成了下标本身）。",
    tags=["指针", "下标"], diff=1)

mcn(title="数组名退化为指针的 sizeof",
    stmt=_stmt("在 64 位平台（int 4 字节、指针 8 字节）上，下面程序输出什么？", '''
        #include <iostream>

        int main() {
            int a[5];
            std::cout << sizeof(a) << " " << sizeof(a + 0) << std::endl;
        }
    '''),
    options=["20 8", "20 20", "8 8", "8 20"],
    value=cpp('''
        #include <iostream>
        int main() {
            int a[5];
            std::cout << sizeof(a) << " " << sizeof(a + 0) << std::endl;
        }
    '''),
    section=_S,
    expl="`sizeof(a)` 量的是数组本身：5×4 = **20**。一旦进表达式 `a + 0`，"
         "数组名**退化**为指向首元素的指针，`sizeof` 变成指针大小 **8**。\n"
         "B 是以为表达式里还保持数组类型；C 是两处都当指针；D 把两者对调了。\n"
         "★ 这正是「数组传参后 sizeof 只剩 8」的同一个机制 —— 长度必须另传一个参数。",
    tags=["sizeof 运算", "数组退化"], diff=2)

mcn(title="二维数组的三层 sizeof",
    stmt=_stmt("在 64 位平台（int 4 字节）上，下面程序输出什么？", '''
        #include <iostream>

        int main() {
            int m[2][3] = {{1, 2, 3}, {4, 5, 6}};
            std::cout << sizeof(m) << " " << sizeof(m[0]) << " " << sizeof(m[0][0]) << std::endl;
        }
    '''),
    options=["24 12 4", "24 4 4", "12 24 4", "24 12 8"],
    value=cpp('''
        #include <iostream>
        int main() {
            int m[2][3] = {{1, 2, 3}, {4, 5, 6}};
            std::cout << sizeof(m) << " " << sizeof(m[0]) << " " << sizeof(m[0][0]) << std::endl;
        }
    '''),
    section=_S,
    expl="二维数组按**行**连续存放，三层 sizeof 正好把结构坐实：\n"
         "整体 `m` = 2 行 × 3 列 × 4 字节 = **24**；`m[0]` 是一维数组（3 个 int）= **12**；"
         "`m[0][0]` 是单个 int = **4**。\n"
         "B 把 `m[0]` 当成一个元素；C 把整体和一行弄反；D 把 int 当成 8 字节（那是 double 或指针）。",
    tags=["二维数组", "sizeof 运算"], diff=2)

tfn(title="strlen 是否包含结尾符",
    stmt="`strlen(s)` 的返回值包含字符串末尾的 `'\\0'`。",
    answer=False, section=_S,
    expl="错。`strlen` 从首字符数到 `'\\0'` **为止**，返回值是「`'\\0'` 之前的字符数」，"
         "**不含**结尾符。\n"
         "但存储时 `'\\0'` 要额外占一字节，所以装 n 个字符至少要 n+1 大小的数组 —— "
         "`char s[5] = \"hello\";` 编译不过就是这个原因（6 个字节塞不进 5 格）。\n"
         "★ 别和 `sizeof` 混：`char s[10] = \"hello\";` 时 `sizeof(s)=10`（容量）、"
         "`strlen(s)=5`（内容长度）。string 用 `length()`，同样不含结尾符。",
    tags=["strlen 长度", "C 串"], diff=2)

_ALIVE = '''
    #include <iostream>

    struct T {
        static int alive;
        T()  { ++alive; }
        ~T() { --alive; }
    };
    int T::alive = 0;

    int main() {
        std::cout << T::alive << " ";
        T *arr = new T[4];
        std::cout << T::alive << " ";
        delete[] arr;
        std::cout << T::alive << std::endl;
    }
'''
mcn(title="new[] 与 delete[] 的计数配对",
    stmt=_stmt("`T::alive` 记录当前活着的对象个数。下面程序输出什么？", _ALIVE),
    options=["0 4 0", "0 1 0", "0 4 3", "4 4 0"],
    value=cpp(_ALIVE), section=_S,
    expl="初始 0；`new T[4]` 构造 4 个对象 → 4；`delete[]` 逐个析构 4 个 → 0（配对正确时有借有还）。\n"
         "B 把 `new T[4]` 当成只构造一个；C 正是**漏写 `[]`** 的后果 —— "
         "普通 `delete` 只析构第一个对象，alive 停在 3，其余 3 个泄漏；"
         "D 忘了初始值。\n"
         "★ 为什么 `delete[]` 知道有几个？`new T[n]` 把 n 记在返回地址前面的「小账本」里，"
         "`delete[]` 先翻账本再逐个析构；普通 `delete` 不翻账本。",
    tags=["new[] 分配", "delete[] 释放"], diff=3)

mcn(title="string 的子串、查找与长度",
    stmt=_stmt("下面程序输出什么？", '''
        #include <iostream>
        #include <string>

        int main() {
            std::string s = "abcd";
            std::cout << s.substr(1, 2) << " " << s.find("c") << " " << s.length() << std::endl;
        }
    '''),
    options=["bc 2 4", "bc 2 5", "cd 2 4", "bcd 3 4"],
    value=cpp('''
        #include <iostream>
        #include <string>
        int main() {
            std::string s = "abcd";
            std::cout << s.substr(1, 2) << " " << s.find("c") << " " << s.length() << std::endl;
        }
    '''),
    section=_S,
    expl="`substr(1, 2)`：第一个参数是**起始下标**、第二个是**长度**，从下标 1 起取 2 个 → `bc`。"
         "`find(\"c\")` 返回首次出现的下标 **2**（找不到返回 `string::npos`）。"
         "`length()` 是 **4**。\n"
         "C 把第二个参数当成结束下标（还取到了 d）；D 既把 substr 当区间又把 find 的结果当成位置 3；"
         "B 多算了结尾符 —— string 的 length 不含结尾符。",
    tags=["string 类", "成员函数"], diff=3)

fillc(title="同数组内指针相减的结果",
      stmt=_stmt("在 64 位平台（int 4 字节）上，下面程序输出什么？", '''
        #include <iostream>

        int main() {
            int a[5];
            int *p = a, *q = a + 4;
            std::cout << q - p << std::endl;
        }
    '''),
      value=cpp('''
        #include <iostream>
        int main() {
            int a[5];
            int *p = a, *q = a + 4;
            std::cout << q - p << std::endl;
        }
    '''),
      section=_S,
      expl="同一数组内两个指针相减，结果是**元素个数**（不是字节数）：`a+4` 与 `a` 差 **4** 个元素。\n"
           "填 16 是拿地址差（4×4 字节）当结果 —— 这是最常见的错法；"
           "填 5 是数了数组长度；填 20 是把地址差又乘了一次。\n"
           "★ 指针运算的单位永远是「元素」：`p+1` 跳 `sizeof(元素类型)` 个字节；"
           "指针**不能相加**，跨数组相减无意义（UB）—— 这些限制都源于「单位是元素」。",
      tags=["指针运算", "指针相减"], diff=3)

_FOLD = '''
    #include <iostream>

    int add(int a, int b) { return a + b; }
    int mul(int a, int b) { return a * b; }
    int sub(int a, int b) { return a - b; }

    int fold(const int *a, int n, int (*op)(int, int), int init) {
        int acc = init;
        for (int i = 0; i < n; i++) acc = op(acc, a[i]);
        return acc;
    }

    int main() {
        int a[5] = {1, 2, 3, 4, 5};
        std::cout << fold(a, 5, add, 0) << " "
                  << fold(a, 5, mul, 1) << " "
                  << fold(a, 5, sub, 0) << std::endl;
    }
'''
mcn(title="函数指针做折叠运算",
    stmt=_stmt("下面的 `fold` 接收一个函数指针作为算子。程序输出什么？", _FOLD),
    options=["15 120 -15", "15 120 15", "15 120 -5", "16 120 -15"],
    value=cpp(_FOLD), section=_S,
    expl="函数名不带括号就是它的**地址**，同一个 `fold` 换个 `op` 就换一种行为：\n"
         "- 求和（init=0）：0+1+2+3+4+5 = **15**；\n"
         "- 连乘（init=1）：1×1×2×3×4×5 = **120**；\n"
         "- 左折叠差（init=0）：(((((0−1)−2)−3)−4)−5) = **−15**。\n"
         "C 的 −5 是没注意 init=0 时先做了 `0−1`；D 的 16 是以为 init 还要再加一次；"
         "B 是把 sub 当成了绝对值差。\n"
         "★ 这就是「把行为当数据传」的回调雏形；后面还有函数对象 / lambda / 虚函数表三种同源手段。",
    tags=["函数指针", "回调"], diff=3)

mcp(title="字符数组初始化容量的陷阱", answer="B",
    stmt="关于字符数组的初始化，下列说法正确的是：",
    options=[
        "char s[5] = \"hello\"; 合法，编译器会自动丢弃结尾的 '\\0'",
        "char s[5] = \"hello\"; 不合法，因为 \"hello\" 占 6 个字节（含 '\\0'），5 格装不下",
        "char s[6] = \"hello\"; 不合法，结尾的 '\\0' 无处存放",
        "char s[] = \"hello\"; 不合法，数组长度必须显式写出来",
    ],
    section=_S,
    expl="B。字符串字面量 `\"hello\"` 是 **6 个字节**（5 个字符 + 结尾 `'\\0'`），"
         "所以容量必须 ≥ 字符数 + 1；5 格装不下，编译错（硬写就越界）。\n"
         "A 是「以为编译器会帮忙丢结尾符」—— 它不会，C 串的所有操作都靠 `'\\0'` 找终点。"
         "C 说反了：6 正好装下。D 也说反了：`char s[] = \"hello\";` 让编译器数出 6，"
         "是合法且常用的写法。",
    tags=["C 串", "字符数组"], diff=4, rot=0)

multn(title="数组、指针与深复制的多项辨析",
      stmt="关于数组、指针与对象复制，下列说法正确的有：",
      options=[
          "数组作为函数形参时退化为指针，函数内 sizeof 得到的是指针大小",
          "new T[n] 必须用 delete[] 释放，用普通 delete 只会析构第一个对象",
          "默认的复制构造函数会为指针成员重新申请一块内存，所以浅复制是安全的",
          "类里有指向堆内存的指针成员时，复制构造、赋值运算符、析构函数应一并自定义",
      ],
      answers=["A", "B", "D"], section=_S,
      expl="A 对：`void f(int a[10])` 的实际类型是 `int *a`，数组大小根本不进函数 —— "
           "所以长度要另传一个参数。\n"
           "B 对：`new T[n]` 把 n 记在返回地址前面的「账本」里，只有 `delete[]` 会翻账本、"
           "逐个析构；普通 delete 只析构第一个。\n"
           "C 错：默认复制构造只**逐成员拷贝**，指针成员拷的是**地址值** —— "
           "两个对象共享同一块内存，改一个另一个跟着变，析构时双重释放。\n"
           "D 对：这就是 Rule of Three（复制构造 + operator= + 析构），"
           "`operator=` 还要 `if (this != &other)` 防自赋值。",
      tags=["数组退化", "深复制", "多选"], diff=4, rot=3)

shortq(title="深层复制与浅层复制的区别",
       statement_md="**简答题**：类里有指针成员指向 `new` 出来的内存时，"
                    "「浅层复制」和「深层复制」的区别是什么？浅复制会导致什么后果？\n\n"
                    "按「拷什么 → 共享还是独立 → 后果」的顺序一句话作答。",
       answers=[
           "浅复制只拷贝指针的值，两个对象共享同一块内存，会双重释放；深复制为新对象重新分配内存并复制内容",
           "浅复制只复制地址导致两个对象共用一块内存，析构时重复释放崩溃；深复制重新申请内存再逐个拷贝数据",
           "浅复制拷贝指针地址，深复制拷贝指针指向的内容，浅复制会造成双重释放",
       ],
       section=_S,
       explanation="**浅复制**：默认复制构造只逐成员赋值，指针成员拷到的是**地址值** → "
                   "两个对象指向同一块堆内存。后果有两层：\n"
                   "① 改一个对象的元素，另一个跟着变（不是脏数据，是同一份数据）；\n"
                   "② 析构时两个对象对同一地址各 `delete[]` 一次 → **双重释放**崩溃"
                   "（实测：两个析构打印的是同一个地址）。\n"
                   "**深复制**：在复制构造里先 `new` 一块自己的内存，再把源对象的元素逐个拷过来；"
                   "两个对象各持一块，互不影响。\n"
                   "★ 含指针成员的类要三件套齐活：复制构造 + `operator=` + 析构；"
                   "`operator=` 开头必须 `if (this != &other)` 防自赋值"
                   "（否则先 delete 再拷的就是自己刚释放的内存）。",
       tags=["深复制", "浅复制", "简答"], difficulty=4)


# ---- 以下为 2026-10 扩充：06 讲补到 20 题（理论 18 + 编程 2）----

# 无计算：概念题，按讲义口径判定（不跑代码）
tfn(title="delete 空指针是否安全",
    stmt="对一个值为 `nullptr` 的指针执行 `delete p;` 是合法的，什么都不会发生。",
    answer=True, section=_S,
    expl="对。标准规定 `delete nullptr` 是**空操作**（内部先判空再动手），不会崩。\n"
         "所以「delete 之后立刻 `p = nullptr;`」是标准姿势：既防**悬空指针**被二次释放，\n"
         "又让析构函数对「本来就没申请过」的成员指针也安全 —— 移动构造偷完资源后置空，\n"
         "靠的正是这一条。\n"
         "★ 但别把它当成万能保险：`delete` 只对 `new` 返回的地址合法。对**野指针**、\n"
         "栈上变量的地址、已经释放却没置空的指针 `delete`，仍然是 UB —— 判空救不了这些。\n"
         "★ 另一条边界：`new[]` 的指针必须 `delete[]`，`delete p`（漏方括号）即使 p 非空也错。",
    tags=["delete", "空指针"], diff=2)

mcn(title="字符数组的 sizeof 与 strlen 对照",
    stmt=_stmt("下面程序分别用 sizeof 与 strlen 量同一个字符数组。输出什么？", '''
        #include <cstring>
        #include <iostream>

        int main() {
            char s[10] = "hello";
            std::cout << sizeof(s) << " " << strlen(s) << std::endl;
        }
    '''),
    options=["10 5", "5 5", "10 6", "6 5"],
    value=cpp('''
        #include <cstring>
        #include <iostream>
        int main() { char s[10] = "hello"; std::cout << sizeof(s) << " " << strlen(s) << std::endl; }
    '''),
    section=_S,
    expl="输出 `10 5`。两个函数量的根本不是一回事：\n"
         "- `sizeof(s)` 是**数组容量**（编译期就定死 10）；\n"
         "- `strlen(s)` 从首字符数到 `'\\0'` **为止**，是**内容长度** 5，**不含**结尾符。\n"
         "B 把 sizeof 当成了内容长；C 把结尾符也算进了 strlen；D 把容量当成了 6。\n"
         "★ 由此推出容量下限：装 n 个字符至少要 **n+1** 格（n 个字符 + 一个 `'\\0'`），\n"
         "所以 `char s[5] = \"hello\";` 是编译错。\n"
         "★ C 串全家桶都靠 `'\\0'` 找终点（cout 打到它停、strlen 数到它停、strcpy 拷到它停）——\n"
         "丢了结尾符，所有操作一起跑飞。这正是 string 更省心的原因。",
    tags=["strlen 长度", "sizeof 运算", "C 串"], diff=2)

mcn(title="double 指针加一跳过的字节数",
    stmt=_stmt("程序把 double 指针的地址差按字节打印出来。输出什么？", '''
        #include <iostream>

        int main() {
            double d[3] = {1.1, 2.2, 3.3};
            std::cout << (char *)(&d[1]) - (char *)&d[0] << std::endl;
        }
    '''),
    options=["8", "4", "1", "3"],
    value=cpp('''
        #include <iostream>
        int main() {
            double d[3] = {1.1, 2.2, 3.3};
            std::cout << (char *)(&d[1]) - (char *)&d[0] << std::endl;
        }
    '''),
    section=_S,
    expl="输出 **8**。指针运算的单位是**元素**：`p + 1` 跳 `sizeof(元素类型)` 个字节，\n"
         "对 double 就是 8 字节。所以 &d[1] 与 &d[0] 的地址差正好 8。\n"
         "本题必须先把两个地址转成 `char*` 再相减，才能看到**字节差**；\n"
         "直接写 `&d[1] - &d[0]` 得到的是**元素个数** 1。\n"
         "B 是 int* 的步长（把 double 记成 4 字节）；C 是 char* 的步长；D 是把下标当成了字节数。\n"
         "★ 三个步长一起背：int* 4、double* 8、char* 1。\n"
         "★ 顺带：指针**不能相加**（`p1 + p2` 编译错），相减只对**同一个数组内**的两个指针有意义，\n"
         "跨数组相减是 UB —— 这些限制都源于「单位是元素」这套语义。",
    tags=["指针运算", "步长"], diff=3)

mcn(title="指针数组与数组指针的 sizeof",
    stmt=_stmt("在 64 位平台上，下面两个声明长得很像。程序输出什么？", '''
        #include <iostream>

        int main() {
            int *a[4];
            int (*b)[4];
            std::cout << sizeof(a) << " " << sizeof(b) << std::endl;
        }
    '''),
    options=["32 8", "8 32", "16 8", "32 32"],
    value=cpp('''
        #include <iostream>
        int main() { int *a[4]; int (*b)[4]; std::cout << sizeof(a) << " " << sizeof(b) << std::endl; }
    '''),
    section=_S,
    expl="输出 `32 8`。两个声明只差一对括号，含义完全不同：\n"
         "- `int *a[4]` 是**指针数组**：`[]` 先与 a 结合，a 是含 4 个元素的数组，\n"
         "元素是 `int*` → 4×8 = **32**；\n"
         "- `int (*b)[4]` 是**数组指针**：括号先结合，b 是**一个指针**，指向「含 4 个 int 的数组」\n"
         "→ 指针大小 **8**。\n"
         "B 把两者对调；C 把指针数组数成 2 个元素；D 把数组指针也当成了数组。\n"
         "★ 读法从名字出发：`a` 是数组（元素是指针）；`b` 是指针（指向数组）。\n"
         "★ 与 const 指针同一个套路 —— 「括号/星号贴着谁，谁先被修饰」：\n"
         "`const int *p` 管物、`int *const p` 管路；`int *a[4]` 是数组、`int (*b)[4]` 是指针。",
    tags=["指针数组", "数组指针", "sizeof 运算"], diff=3)

mcn(title="下标与指针运算的交换律",
    stmt=_stmt("下面用两种写法取同一个元素。输出什么？", '''
        #include <iostream>

        int main() {
            int a[3] = {10, 20, 30};
            std::cout << 1[a] << " " << a[1] << std::endl;
        }
    '''),
    options=["20 20", "10 10", "20 10", "编译错"],
    value=cpp('''
        #include <iostream>
        int main() { int a[3] = {10, 20, 30}; std::cout << 1[a] << " " << a[1] << std::endl; }
    '''),
    section=_S,
    expl="输出 `20 20`。`a[i]` 的定义就是 `*(a + i)`，而加法**可交换**，\n"
         "所以 `*(a + 1) == *(1 + a)`，即 `a[1]` 与 `1[a]` 完全等价，都取 20。\n"
         "B 以为 `1[a]` 会退化成 a[0]；C 以为两种写法不等；D 错，语法合法（g++ 一声不吭）。\n"
         "★ 这条等价关系把一串写法打通了：`p[1]`、`*(p + 1)`、`1[p]` 取的是同一个元素。\n"
         "理解它的价值不在炫技，而在看懂库代码里的 `*(first + n)` 与 `first[n]` 是一回事。\n"
         "★ 但**别在工程里写 `1[a]`** —— 编译器不拦，读代码的人会想打人。",
    tags=["下标", "指针运算"], diff=3)

mcn(title="深复制之后两个对象是否共享缓冲区",
    stmt=_stmt("`Buf` 的复制构造另开了一块内存。下面程序输出什么？", '''
        #include <iostream>

        struct Buf {
            int *data;
            int n;
            Buf(int n) : data(new int[n]), n(n) {
                for (int i = 0; i < n; i++) data[i] = i * 10;
            }
            Buf(const Buf &o) : data(new int[o.n]), n(o.n) {
                for (int i = 0; i < n; i++) data[i] = o.data[i];
            }
            ~Buf() { delete[] data; }
        };

        int main() {
            Buf a(3);
            Buf b = a;
            b.data[0] = 999;
            std::cout << a.data[0] << " " << b.data[0] << " "
                      << (a.data == b.data) << std::endl;
        }
    '''),
    options=["0 999 0", "999 999 1", "0 0 1", "999 0 0"],
    value=cpp('''
        #include <iostream>
        struct Buf {
            int *data;
            int n;
            Buf(int n) : data(new int[n]), n(n) {
                for (int i = 0; i < n; i++) data[i] = i * 10;
            }
            Buf(const Buf &o) : data(new int[o.n]), n(o.n) {
                for (int i = 0; i < n; i++) data[i] = o.data[i];
            }
            ~Buf() { delete[] data; }
        };
        int main() {
            Buf a(3); Buf b = a; b.data[0] = 999;
            std::cout << a.data[0] << " " << b.data[0] << " "
                      << (a.data == b.data) << std::endl;
        }
    '''),
    section=_S,
    expl="输出 `0 999 0`。复制构造里 `new int[o.n]` **另开一块**，再把元素逐个拷过来，\n"
         "所以改 b 的元素完全不影响 a：a 的 data[0] 仍是初始值 0，b 的变成 999，\n"
         "两个地址不相等（判等得 0）。\n"
         "B 正是**浅复制**（默认复制构造）的结果：两个指针存同一个地址，改一个另一个跟着变，\n"
         "而且两个析构会对同一块 `delete[]` → **双重释放**。\n"
         "C、D 把「地址相等」与「值相等」混在了一起。\n"
         "★ 判据很简单：**拷贝指针的值 = 浅复制；拷贝指针指向的内容 = 深复制**。\n"
         "★ 含指针成员的类要三件套齐活：复制构造 + `operator=` + 析构；\n"
         "少写 `operator=`，赋值时灾难会从「构造」转移到「赋值」（g++ 的 deprecated-copy 会提醒你）。",
    tags=["深复制", "浅复制", "复制构造"], diff=3)

mcn(title="函数指针数组按下标选择算子",
    stmt=_stmt("`ops` 是一个存放两个函数指针的数组。下面程序输出什么？", '''
        #include <iostream>

        int add(int a, int b) { return a + b; }
        int mul(int a, int b) { return a * b; }

        int main() {
            int (*ops[2])(int, int) = {add, mul};
            std::cout << ops[0](3, 4) << " " << ops[1](3, 4) << std::endl;
        }
    '''),
    options=["7 12", "12 7", "7 7", "编译错"],
    value=cpp('''
        #include <iostream>
        int add(int a, int b) { return a + b; }
        int mul(int a, int b) { return a * b; }
        int main() {
            int (*ops[2])(int, int) = {add, mul};
            std::cout << ops[0](3, 4) << " " << ops[1](3, 4) << std::endl;
        }
    '''),
    section=_S,
    expl="输出 `7 12`。先读声明：从 `ops` 出发，`ops` 是**数组**（`[2]`），元素是**指针**（`*`），\n"
         "指向 `int(int, int)` 的函数 —— 「存放 2 个函数指针的数组」。\n"
         "函数名不带括号就是函数的**地址**，所以 `{add, mul}` 直接初始化两个元素；\n"
         "`ops[0](3,4)` 调 add 得 7，`ops[1](3,4)` 调 mul 得 12。\n"
         "B 把下标对调；C 以为两个元素指向同一个函数；D 错，`ops[0](...)` 与 `(*ops[0])(...)`\n"
         "完全等价。\n"
         "★ 这就是「把行为当数据」的雏形：同一个调用点，按下标换一个算子就换一种行为。\n"
         "这条线后面还有两种同源手段：函数对象 / lambda（第 10 章）、虚函数表（第 8 章，\n"
         "本质是类里藏着一张函数指针表）。",
    tags=["函数指针", "函数指针数组"], diff=4)


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
        if p.get("subject") != "cpp":
            bad.append("[%d] %s：subject 应为 cpp，实为 %r" % (i, t, p.get("subject")))
        if p.get("line") != "text":
            bad.append("[%d] %s：line 应为 text，实为 %r" % (i, t, p.get("line")))
        if p.get("checker") != "oneof":
            bad.append("[%d] %s：checker 应为 oneof" % (i, t))
        if not (1 <= p["difficulty"] <= 4):
            bad.append("[%d] %s：difficulty 越界 %r" % (i, t, p["difficulty"]))
        if p["total_score"] <= 0:
            bad.append("[%d] %s 满分非法" % (i, t))
        if not p.get("tags"):
            bad.append("[%d] %s：tags 为空" % (i, t))
        qt = p["question_type"]
        choices = p.get("choices") or []
        ans = p["reference_solution"].strip().upper()
        if qt == "single_choice":
            if len(choices) < 2:
                bad.append("[%d] %s：单选缺选项" % (i, t))
            elif ans not in "ABCDEFGH"[:len(choices)]:
                bad.append("[%d] %s：单选答案 %r 不在选项范围" % (i, t, ans))
        if qt == "multiple_choice":
            if len(choices) < 3:
                bad.append("[%d] %s：多选选项少于 3 个" % (i, t))
            if len(ans) < 2:
                bad.append("[%d] %s：多选答案少于 2 个字母" % (i, t))
            if any(a not in "ABCDEFGH"[:len(choices)] for a in ans):
                bad.append("[%d] %s：多选答案超出选项范围" % (i, t))
        if qt == "true_false" and choices != ["对", "错"]:
            bad.append("[%d] %s：判断题选项应为 对/错" % (i, t))
        for c in p["cases"]:
            if c["is_sample"]:
                bad.append("[%d] %s：理论题的样例必须隐藏（is_sample=0）" % (i, t))
            if not c["expected_stdout"].strip():
                bad.append("[%d] %s：期望值为空" % (i, t))
            if not str(c.get("explanation") or "").strip():
                bad.append("[%d] %s：缺解析 explanation" % (i, t))
    return bad


def main() -> int:
    ap = argparse.ArgumentParser(description="生成 C++ 基础线理论题库（第 01~06 讲）")
    ap.add_argument("--check", action="store_true", help="只校验，不写文件")
    args = ap.parse_args()

    probs = PROBS
    from collections import Counter
    by_type = Counter(p["question_type"] for p in probs)
    by_sec = Counter(p["source_section"] for p in probs)
    print("题目数：%d    测试点：%d    总分：%d"
          % (len(probs), sum(len(p["cases"]) for p in probs),
             sum(p["total_score"] for p in probs)))
    print("题型分布：" + "、".join("%s %d" % (k, v) for k, v in sorted(by_type.items())))
    print("分讲题数：")
    for sec, want in SECTION_COUNTS.items():
        got = by_sec.get(sec, 0)
        print("    %-24s %2d（计划 %2d）%s"
              % (sec, got, want, "" if got == want else "  ★ 不符"))
    if any(by_sec.get(s, 0) != n for s, n in SECTION_COUNTS.items()):
        print("★ 分讲题数与计划不符")
        return 1

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
