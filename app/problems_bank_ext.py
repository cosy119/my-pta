# -*- coding: utf-8 -*-
"""题库扩展：按讲义进度铺设的练习题（第二批）。

与 `problems_bank.py` 同一套约定：

1. **顺序跟讲义走** —— `source_section` 标出讲次，列表页按讲次排序，
   所以学习顺序 = 列表顺序
2. **期望输出独立算** —— 本文件所有 `expected_stdout` 都由 **node 独立实现**
   预先算出（另一语言、另一套算法），Python 参考解只负责「撞」它；
   两者对不上就不入库
3. **`alt_solution` 是第二套独立实现** —— 参考解和它必须都通过全部测试点，
   防止单套实现有共同盲区
4. **分值按难度给** —— 入门 10 分、要动脑 15 分、综合 20 分

覆盖：第 02 讲 ~ 第 11 讲，每讲至少 3 道，重难点（列表 / 字典 / 递归 / 面向对象）更多。
"""
from __future__ import annotations

EXT_PROBLEMS: list[dict] = [
    # ================================================================== #
    # 第 02 讲 · 编程基础：类型转换 / 格式化输出
    # ================================================================== #
    {
        "title": "温度转换",
        "line": "python",
        "difficulty": 1,
        "total_score": 10,
        "tags": ["输入输出", "类型转换", "格式化", "浮点"],
        "source_section": "第 02 讲 · 编程基础",
        "statement_md": (
            "读入一个摄氏温度 `C`，输出对应的华氏温度，**保留 2 位小数**。\n\n"
            "换算公式：`F = C × 9 / 5 + 32`。\n\n"
            "两个考点：\n\n"
            "1. **整数除法陷阱** —— 在 Python 3 里 `9 / 5` 得 `1.8`（真除法），"
            "所以直接写就行；要是写成别的语言那样 `9 // 5` 就变成 `1` 了\n"
            "2. `-40` 是摄氏和华氏**相等**的那个温度，可以拿来自检公式对不对"
        ),
        "input_format": "一行，一个整数 `C`。",
        "output_format": "一行，华氏温度，保留 2 位小数。",
        "constraints_md": "- -1000 ≤ C ≤ 10000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "c = float(sys.stdin.read().strip())\n"
            "print('%.2f' % (c * 9 / 5 + 32))\n"
        ),
        "alt_solution": (
            "from fractions import Fraction\n"
            "import sys\n\n"
            "c = Fraction(sys.stdin.read().strip())\n"
            "f = c * 9 / 5 + 32\n"
            "print('%.2f' % float(f))\n"
        ),
        "cases": [
            {"stdin": "0\n", "expected_stdout": "32.00\n", "is_sample": 1,
             "kind": "sample", "explanation": "水的冰点：0℃ = 32℉"},
            {"stdin": "100\n", "expected_stdout": "212.00\n", "is_sample": 1,
             "kind": "sample", "explanation": "水的沸点：100℃ = 212℉"},
            {"stdin": "-40\n", "expected_stdout": "-40.00\n", "kind": "manual",
             "explanation": "★ -40 是唯一摄氏 = 华氏的温度，公式对错一眼看出来"},
            {"stdin": "37\n", "expected_stdout": "98.60\n", "kind": "manual",
             "explanation": "体温；37 × 1.8 = 66.6，+32 = 98.6"},
            {"stdin": "25\n", "expected_stdout": "77.00\n", "kind": "manual"},
        ],
    },
    {
        "title": "三位数拆分",
        "line": "python",
        "difficulty": 1,
        "total_score": 10,
        "tags": ["算术运算", "整除", "取余"],
        "source_section": "第 02 讲 · 编程基础",
        "statement_md": (
            "读入一个三位数，输出它**各位数字之和**。\n\n"
            "两种典型写法：\n\n"
            "- **算术法**：`n // 100` 取百位，`n // 10 % 10` 取十位，`n % 10` 取个位\n"
            "- **字符串法**：`str(n)` 拆开，逐个转回 `int` 再加\n\n"
            "这题看着简单，但**整除和取余的优先级**（`//` 与 `%` 同级，从左往右算）"
            "是初学最容易写错的地方。"
        ),
        "input_format": "一行，一个三位数 `n`。",
        "output_format": "一行，各位数字之和。",
        "constraints_md": "- 100 ≤ n ≤ 999",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "n = int(sys.stdin.read().strip())\n"
            "print(n // 100 + n // 10 % 10 + n % 10)\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "n = sys.stdin.read().strip()\n"
            "print(sum(int(ch) for ch in n))\n"
        ),
        "cases": [
            {"stdin": "123\n", "expected_stdout": "6\n", "is_sample": 1,
             "kind": "sample", "explanation": "1 + 2 + 3 = 6"},
            {"stdin": "999\n", "expected_stdout": "27\n", "is_sample": 1,
             "kind": "sample", "explanation": "9 × 3 = 27，最大值"},
            {"stdin": "100\n", "expected_stdout": "1\n", "kind": "manual",
             "explanation": "十位和个位都是 0"},
            {"stdin": "405\n", "expected_stdout": "9\n", "kind": "manual",
             "explanation": "4 + 0 + 5 = 9，中间的 0 别漏"},
            {"stdin": "700\n", "expected_stdout": "7\n", "kind": "manual"},
        ],
    },
    # ================================================================== #
    # 第 03 讲 · 流程控制语句：嵌套循环 / 多分支
    # ================================================================== #
    {
        "title": "九九乘法表",
        "line": "python",
        "difficulty": 2,
        "total_score": 15,
        "tags": ["嵌套循环", "格式化", "字符串拼接"],
        "source_section": "第 03 讲 · 流程控制语句",
        "statement_md": (
            "输出完整的九九乘法表，共 9 行。\n\n"
            "第 `i` 行包含 `j` 从 1 到 `i` 的每一项，格式为 `i*j=积`，"
            "同一行内用**一个空格**分隔：\n\n"
            "```text\n"
            "1*1=1\n"
            "2*1=2 2*2=4\n"
            "3*1=3 3*2=6 3*3=9\n"
            "```\n\n"
            "**要点**\n\n"
            "- 外层循环控制「第几行」，内层循环控制「这一行有几项」\n"
            "- 内层上界跟着外层走（`j` 从 1 到 `i`），这是嵌套循环的典型形状\n"
            "- 行末**不能**多出空格 —— 用 `' '.join(...)` 天然不会多"
        ),
        "input_format": "无输入（可以直接不读）。",
        "output_format": "9 行，如上格式。",
        "constraints_md": "- 输出固定，与输入无关",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "lines = []\n"
            "for i in range(1, 10):\n"
            "    row = []\n"
            "    for j in range(1, i + 1):\n"
            "        row.append('%d*%d=%d' % (i, j, i * j))\n"
            "    lines.append(' '.join(row))\n"
            "print('\\n'.join(lines))\n"
        ),
        "alt_solution": (
            "print('\\n'.join(\n"
            "    ' '.join('%d*%d=%d' % (i, j, i * j) for j in range(1, i + 1))\n"
            "    for i in range(1, 10)\n"
            "))\n"
        ),
        "cases": [
            {"stdin": "\n",
             "expected_stdout": (
                 "1*1=1\n"
                 "2*1=2 2*2=4\n"
                 "3*1=3 3*2=6 3*3=9\n"
                 "4*1=4 4*2=8 4*3=12 4*4=16\n"
                 "5*1=5 5*2=10 5*3=15 5*4=20 5*5=25\n"
                 "6*1=6 6*2=12 6*3=18 6*4=24 6*5=30 6*6=36\n"
                 "7*1=7 7*2=14 7*3=21 7*4=28 7*5=35 7*6=42 7*7=49\n"
                 "8*1=8 8*2=16 8*3=24 8*4=32 8*5=40 8*6=48 8*7=56 8*8=64\n"
                 "9*1=9 9*2=18 9*3=27 9*4=36 9*5=45 9*6=54 9*7=63 9*8=72 9*9=81\n"),
             "is_sample": 1, "kind": "sample",
             "explanation": "第 i 行有 i 项；两位数从第 4 行开始出现"},
        ],
    },
    {
        "title": "成绩等级",
        "line": "python",
        "difficulty": 1,
        "total_score": 10,
        "tags": ["if-elif", "边界", "区间的开闭"],
        "source_section": "第 03 讲 · 流程控制语句",
        "statement_md": (
            "给出百分制分数，输出对应等级：\n\n"
            "| 分数 | 等级 |\n"
            "|---|---|\n"
            "| 90 ~ 100 | `A` |\n"
            "| 80 ~ 89 | `B` |\n"
            "| 70 ~ 79 | `C` |\n"
            "| 60 ~ 69 | `D` |\n"
            "| 0 ~ 59 | `E` |\n\n"
            "**考点是边界**：89 和 90 挨着，59 和 60 挨着。"
            "用 `if s >= 90` 从上往下写就不会错；"
            "要是写成 `if s > 90`，90 分就会掉到 `B` 去。"
        ),
        "input_format": "一行，一个整数 `s`。",
        "output_format": "一行，一个大写字母等级。",
        "constraints_md": "- 0 ≤ s ≤ 100",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "s = int(sys.stdin.read().strip())\n"
            "if s >= 90:\n"
            "    print('A')\n"
            "elif s >= 80:\n"
            "    print('B')\n"
            "elif s >= 70:\n"
            "    print('C')\n"
            "elif s >= 60:\n"
            "    print('D')\n"
            "else:\n"
            "    print('E')\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "s = int(sys.stdin.read().strip())\n"
            "print('EEEEEEDCBA'[min(s // 10, 9)])\n"
        ),
        "cases": [
            {"stdin": "90\n", "expected_stdout": "A\n", "is_sample": 1,
             "kind": "sample", "explanation": "90 是 A 的下边界（写成 > 90 就错了）"},
            {"stdin": "60\n", "expected_stdout": "D\n", "is_sample": 1,
             "kind": "sample", "explanation": "60 是 D 的下边界"},
            {"stdin": "89\n", "expected_stdout": "B\n", "kind": "manual",
             "explanation": "差 1 分掉一级"},
            {"stdin": "75\n", "expected_stdout": "C\n", "kind": "manual"},
            {"stdin": "59\n", "expected_stdout": "E\n", "kind": "manual"},
            {"stdin": "0\n", "expected_stdout": "E\n", "kind": "manual"},
        ],
    },
    {
        "title": "水仙花数",
        "line": "python",
        "difficulty": 2,
        "total_score": 15,
        "tags": ["循环", "区间", "数位拆分"],
        "source_section": "第 03 讲 · 流程控制语句",
        "statement_md": (
            "**水仙花数**：一个三位数，它的各位数字的**三次方之和**等于它本身。\n\n"
            "例如 153：`1³ + 5³ + 3³ = 1 + 125 + 27 = 153`，所以 153 是水仙花数。\n\n"
            "请找出 100 ~ 999 之间**所有**水仙花数，从小到大输出，"
            "同一行内用空格分隔。\n\n"
            "这题把「遍历区间 + 拆位 + 条件判断」串在一起，"
            "是这个阶段最经典的综合小练习。"
        ),
        "input_format": "无输入。",
        "output_format": "一行，所有水仙花数，空格分隔。",
        "constraints_md": "- 输出固定，与输入无关",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "token",
        "reference_solution": (
            "out = []\n"
            "for n in range(100, 1000):\n"
            "    a, b, c = n // 100, n // 10 % 10, n % 10\n"
            "    if a ** 3 + b ** 3 + c ** 3 == n:\n"
            "        out.append(str(n))\n"
            "print(' '.join(out))\n"
        ),
        "alt_solution": (
            "print(' '.join(str(n) for n in range(100, 1000)\n"
            "               if sum(int(d) ** 3 for d in str(n)) == n))\n"
        ),
        "cases": [
            {"stdin": "\n", "expected_stdout": "153 370 371 407\n",
             "is_sample": 1, "kind": "sample",
             "explanation": ("★ 一共 4 个：153(1+125+27)、370(27+343+0)、"
                             "371(27+343+1)、407(64+0+343)")},
        ],
    },
    # ================================================================== #
    # 第 04 讲 · 字符串
    # ================================================================== #
    {
        "title": "统计字符类型",
        "line": "python",
        "difficulty": 2,
        "total_score": 15,
        "tags": ["字符串", "遍历", "分类统计"],
        "source_section": "第 04 讲 · 字符串",
        "statement_md": (
            "读入一行文本，统计其中**字母**、**数字**、**空格**、**其他字符**"
            "各有多少个，按这个顺序输出四个整数。\n\n"
            "Python 的字符串有现成的判断方法：\n\n"
            "- `ch.isalpha()` —— 是不是字母（只算 ASCII 字母时用 `'a' <= ch <= 'z'` 更保险）\n"
            "- `ch.isdigit()` —— 是不是数字\n\n"
            "**注意**：`isalpha()` 对中文字符也会返回 `True`。"
            "本题输入只含可见 ASCII 字符，两种写法结果一样。"
        ),
        "input_format": "一行文本（可能为空）。",
        "output_format": "一行，四个整数，依次是 字母数 数字数 空格数 其他数。",
        "constraints_md": "- 0 ≤ 行长 ≤ 10000\n- 只含可见 ASCII 字符与空格",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "s = sys.stdin.readline().rstrip('\\n').rstrip('\\r')\n"
            "letter = digit = space = 0\n"
            "for ch in s:\n"
            "    if ('a' <= ch <= 'z') or ('A' <= ch <= 'Z'):\n"
            "        letter += 1\n"
            "    elif '0' <= ch <= '9':\n"
            "        digit += 1\n"
            "    elif ch == ' ':\n"
            "        space += 1\n"
            "print(letter, digit, space, len(s) - letter - digit - space)\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "s = sys.stdin.readline().rstrip('\\n').rstrip('\\r')\n"
            "letter = sum(1 for ch in s if ch.isalpha())\n"
            "digit = sum(1 for ch in s if ch.isdigit())\n"
            "space = s.count(' ')\n"
            "other = sum(1 for ch in s if not ch.isalnum() and ch != ' ')\n"
            "print(letter, digit, space, other)\n"
        ),
        "cases": [
            {"stdin": "Hello World 123\n", "expected_stdout": "10 3 2 0\n",
             "is_sample": 1, "kind": "sample",
             "explanation": "Hello(5) + World(5) = 10 个字母；1 2 3 三个数字；两个空格"},
            {"stdin": "a b!\n", "expected_stdout": "2 0 1 1\n", "is_sample": 1,
             "kind": "sample", "explanation": "字母 a b，空格 1 个，`!` 归入其他"},
            {"stdin": "abc\n", "expected_stdout": "3 0 0 0\n", "kind": "manual"},
            {"stdin": "12345\n", "expected_stdout": "0 5 0 0\n", "kind": "manual"},
            {"stdin": "\n", "expected_stdout": "0 0 0 0\n", "kind": "manual",
             "explanation": "空行 → 全是 0"},
        ],
    },
    {
        "title": "大小写互换",
        "line": "python",
        "difficulty": 1,
        "total_score": 10,
        "tags": ["字符串", "内置方法", "遍历"],
        "source_section": "第 04 讲 · 字符串",
        "statement_md": (
            "读入一行文本，把**大写字母变小写、小写字母变大写**，其他字符原样保留。\n\n"
            "Python 字符串有个一步到位的方法：`s.swapcase()`。\n\n"
            "不过建议你也手写一遍循环版本 —— 面试和考试里更常考「怎么判断一个字符是大写」。"
        ),
        "input_format": "一行文本（可能为空）。",
        "output_format": "一行，转换后的文本。",
        "constraints_md": "- 0 ≤ 行长 ≤ 10000\n- 只含可见 ASCII 字符与空格",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "s = sys.stdin.readline().rstrip('\\n').rstrip('\\r')\n"
            "print(s.swapcase())\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "s = sys.stdin.readline().rstrip('\\n').rstrip('\\r')\n"
            "out = []\n"
            "for ch in s:\n"
            "    if 'a' <= ch <= 'z':\n"
            "        out.append(ch.upper())\n"
            "    elif 'A' <= ch <= 'Z':\n"
            "        out.append(ch.lower())\n"
            "    else:\n"
            "        out.append(ch)\n"
            "print(''.join(out))\n"
        ),
        "cases": [
            {"stdin": "Hello\n", "expected_stdout": "hELLO\n", "is_sample": 1,
             "kind": "sample"},
            {"stdin": "Hello World\n", "expected_stdout": "hELLO wORLD\n",
             "is_sample": 1, "kind": "sample", "explanation": "空格不受影响"},
            {"stdin": "AbC123\n", "expected_stdout": "aBc123\n", "kind": "manual",
             "explanation": "数字原样保留"},
            {"stdin": "\n", "expected_stdout": "\n", "kind": "manual",
             "explanation": "空串输出空行"},
        ],
    },
    {
        "title": "查找子串",
        "line": "python",
        "difficulty": 2,
        "total_score": 15,
        "tags": ["字符串", "find", "重叠匹配"],
        "source_section": "第 04 讲 · 字符串",
        "statement_md": (
            "读入两行：第一行是**主串**，第二行是**模式串**。"
            "输出模式串在主串中出现的次数。\n\n"
            "**关键：允许重叠。**\n\n"
            "比如主串 `aaaa`、模式串 `aa`，答案是 **3** 而不是 2 —— "
            "因为起点 0、1、2 各能匹配一次，它们互相重叠。\n\n"
            "如果直接用 `s.count(p)`，**也可以**，它默认就是按重叠起点数的；"
            "但面试里更常让你用 `str.find()` 循环实现：\n"
            "每次找到后从「上次位置 + 1」继续找，而不是 + 模式串长度。"
        ),
        "input_format": "两行，第一行主串 `t`（长度 ≥ 1），第二行模式串 `p`（长度 ≥ 1）。",
        "output_format": "一行，一个整数，出现次数（可重叠）。",
        "constraints_md": "- 1 ≤ len(p) ≤ len(t) ≤ 10000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "lines = sys.stdin.read().split('\\n')\n"
            "t = lines[0].rstrip('\\r')\n"
            "p = lines[1].rstrip('\\r') if len(lines) > 1 else ''\n"
            "cnt = 0\n"
            "for i in range(len(t) - len(p) + 1):\n"
            "    if t[i:i + len(p)] == p:\n"
            "        cnt += 1\n"
            "print(cnt)\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "lines = sys.stdin.read().split('\\n')\n"
            "t = lines[0].rstrip('\\r')\n"
            "p = lines[1].rstrip('\\r') if len(lines) > 1 else ''\n"
            "cnt = 0\n"
            "start = 0\n"
            "while True:\n"
            "    i = t.find(p, start)\n"
            "    if i < 0:\n"
            "        break\n"
            "    cnt += 1\n"
            "    start = i + 1\n"
            "print(cnt)\n"
        ),
        "cases": [
            {"stdin": "aaaa\naa\n", "expected_stdout": "3\n", "is_sample": 1,
             "kind": "sample", "explanation": "★ 下标 0、1、2 各匹配一次 → 3（不是 2）"},
            {"stdin": "abcabcabc\nabc\n", "expected_stdout": "3\n", "is_sample": 1,
             "kind": "sample", "explanation": "不重叠的重复三次"},
            {"stdin": "abababa\naba\n", "expected_stdout": "3\n", "kind": "manual",
             "explanation": "下标 0、2、4；这里「重叠」和「不重叠」恰好都是 3"},
            {"stdin": "aaa\na\n", "expected_stdout": "3\n", "kind": "manual"},
            {"stdin": "hello\nxyz\n", "expected_stdout": "0\n", "kind": "manual"},
        ],
    },
    # ================================================================== #
    # 第 05 讲 · 列表与元组
    # ================================================================== #
    {
        "title": "极差",
        "line": "python",
        "difficulty": 1,
        "total_score": 10,
        "tags": ["列表", "max", "min"],
        "source_section": "第 05 讲 · 列表与元组",
        "statement_md": (
            "读入 `n` 个整数，输出它们的**极差**（最大值减最小值）。\n\n"
            "`max()` 和 `min()` 是 Python 内置函数，对列表直接用；"
            "也可以先 `sort()` 再取首尾 —— 后者能顺便把列表排好序。"
        ),
        "input_format": "第一行一个整数 `n`；第二行 `n` 个整数，空格分隔。",
        "output_format": "一行，一个整数：最大值 − 最小值。",
        "constraints_md": "- 1 ≤ n ≤ 100000\n- 每个数的绝对值 ≤ 10^9",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "data = sys.stdin.read().split()\n"
            "n = int(data[0])\n"
            "nums = [int(x) for x in data[1:1 + n]]\n"
            "print(max(nums) - min(nums))\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "data = sys.stdin.read().split()\n"
            "n = int(data[0])\n"
            "nums = list(map(int, data[1:1 + n]))\n"
            "nums.sort()\n"
            "print(nums[-1] - nums[0])\n"
        ),
        "cases": [
            {"stdin": "5\n3 1 4 1 5\n", "expected_stdout": "4\n", "is_sample": 1,
             "kind": "sample", "explanation": "max 5 − min 1 = 4"},
            {"stdin": "1\n7\n", "expected_stdout": "0\n", "is_sample": 1,
             "kind": "sample", "explanation": "只有一个数 → 极差 0"},
            {"stdin": "4\n-5 -2 -9 -1\n", "expected_stdout": "8\n", "kind": "manual",
             "explanation": "max -1，min -9，-1 − (-9) = 8"},
        ],
    },
    {
        "title": "成绩统计",
        "line": "python",
        "difficulty": 2,
        "total_score": 15,
        "tags": ["列表", "聚合", "格式化"],
        "source_section": "第 05 讲 · 列表与元组",
        "statement_md": (
            "读入 `n` 个成绩（整数），在同一行输出三个值：\n\n"
            "```text\n"
            "最高分 最低分 平均分\n"
            "```\n\n"
            "其中**平均分保留 2 位小数**，其余两个按整数输出。\n\n"
            "**易错点**：`sum(nums) / n` 在 Python 3 里是真除法，"
            "不会把小数截掉；`n = 0` 的情况本题不会出现。"
        ),
        "input_format": "第一行一个整数 `n`；第二行 `n` 个整数，空格分隔。",
        "output_format": "一行，`最高分 最低分 平均分`（平均分 2 位小数）。",
        "constraints_md": "- 1 ≤ n ≤ 100000\n- 0 ≤ 每个成绩 ≤ 100",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "data = sys.stdin.read().split()\n"
            "n = int(data[0])\n"
            "nums = [int(x) for x in data[1:1 + n]]\n"
            "print(max(nums), min(nums), '%.2f' % (sum(nums) / n))\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "data = sys.stdin.read().split()\n"
            "n = int(data[0])\n"
            "nums = list(map(int, data[1:1 + n]))\n"
            "s = sorted(nums)\n"
            "print(s[-1], s[0], '%.2f' % (sum(s) / len(s)))\n"
        ),
        "cases": [
            {"stdin": "5\n90 80 70 100 60\n", "expected_stdout": "100 60 80.00\n",
             "is_sample": 1, "kind": "sample",
             "explanation": "总分 400，400 / 5 = 80.00"},
            {"stdin": "3\n1 2 4\n", "expected_stdout": "4 1 2.33\n",
             "is_sample": 1, "kind": "sample",
             "explanation": "7 / 3 = 2.3333… → 2.33"},
            {"stdin": "1\n59\n", "expected_stdout": "59 59 59.00\n", "kind": "manual"},
            {"stdin": "4\n100 100 100 100\n",
             "expected_stdout": "100 100 100.00\n", "kind": "manual"},
        ],
    },
    {
        "title": "合并有序列表",
        "line": "python",
        "difficulty": 3,
        "total_score": 20,
        "tags": ["列表", "双指针", "归并", "边界"],
        "source_section": "第 05 讲 · 列表与元组",
        "statement_md": (
            "给定两个**升序排列**的整数序列，把它们合并成一个仍然升序的序列并输出。\n\n"
            "```text\n"
            "输入：1 3 5  和  2 4 6\n"
            "输出：1 2 3 4 5 6\n"
            "```\n\n"
            "两种写法：\n\n"
            "- **省事**：`sorted(a + b)` —— 直接拼起来全排序，O((n+m)log(n+m))\n"
            "- **正统**：双指针归并 —— 每次比较两个序列的队首，取小的那个，"
            "O(n + m)；这是归并排序的核心步骤\n\n"
            "**边界**：任一序列可以是空的（`n = 0` 时第二行是空行，也要读掉）。"
        ),
        "input_format": (
            "第一行一个整数 `n`；第二行 `n` 个升序整数（n = 0 时为空行）。\n\n"
            "第三行一个整数 `m`；第四行 `m` 个升序整数（m = 0 时为空行）。"
        ),
        "output_format": "一行，合并后的升序序列，空格分隔。",
        "constraints_md": "- 0 ≤ n, m ≤ 100000\n- 每个数的绝对值 ≤ 10^9",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "token",
        "reference_solution": (
            "import sys\n\n"
            "def rd():\n"
            "    return sys.stdin.readline().strip()\n\n"
            "n = int(rd())\n"
            "line_a = rd()\n"
            "a = [int(x) for x in line_a.split()] if n else []\n"
            "m = int(rd())\n"
            "line_b = rd()\n"
            "b = [int(x) for x in line_b.split()] if m else []\n"
            "i = j = 0\n"
            "out = []\n"
            "while i < len(a) and j < len(b):\n"
            "    if a[i] <= b[j]:\n"
            "        out.append(a[i])\n"
            "        i += 1\n"
            "    else:\n"
            "        out.append(b[j])\n"
            "        j += 1\n"
            "out.extend(a[i:])\n"
            "out.extend(b[j:])\n"
            "print(' '.join(map(str, out)))\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "def rd():\n"
            "    return sys.stdin.readline().strip()\n\n"
            "n = int(rd())\n"
            "line_a = rd()\n"
            "a = list(map(int, line_a.split())) if n else []\n"
            "m = int(rd())\n"
            "line_b = rd()\n"
            "b = list(map(int, line_b.split())) if m else []\n"
            "print(' '.join(map(str, sorted(a + b))))\n"
        ),
        "cases": [
            {"stdin": "3\n1 3 5\n3\n2 4 6\n",
             "expected_stdout": "1 2 3 4 5 6\n", "is_sample": 1, "kind": "sample",
             "explanation": "交错合并"},
            {"stdin": "3\n1 1 2\n3\n1 2 2\n",
             "expected_stdout": "1 1 1 2 2 2\n", "is_sample": 1, "kind": "sample",
             "explanation": "有重复元素，相等时先取哪个都行（结果一样）"},
            {"stdin": "3\n1 2 3\n0\n\n", "expected_stdout": "1 2 3\n",
             "kind": "manual", "explanation": "★ m = 0，第四行是空行，也要读掉"},
            {"stdin": "0\n\n1\n5\n", "expected_stdout": "5\n", "kind": "manual",
             "explanation": "★ n = 0，第二行是空行"},
        ],
    },
    {
        "title": "矩阵转置",
        "line": "python",
        "difficulty": 3,
        "total_score": 20,
        "tags": ["二维列表", "嵌套列表", "zip"],
        "source_section": "第 05 讲 · 列表与元组",
        "statement_md": (
            "读入一个 `n` 行 `m` 列的整数矩阵，输出它的**转置**（行列互换，变成 `m` 行 `n` 列）。\n\n"
            "```text\n"
            "输入：      输出：\n"
            "1 2 3       1 4\n"
            "4 5 6       2 5\n"
            "            3 6\n"
            "```\n\n"
            "两种写法：\n\n"
            "- 下标法：`new[j][i] = old[i][j]`\n"
            "- Python 味：`zip(*mat)` —— `*` 把行拆开，`zip` 再按列打包，一行搞定\n\n"
            "**注意**：这不是方阵，`n ≠ m` 是常态，别写死成对称交换。"
        ),
        "input_format": (
            "第一行两个整数 `n` 和 `m`。\n\n"
            "随后 `n` 行，每行 `m` 个整数。"
        ),
        "output_format": "`m` 行，每行 `n` 个整数，空格分隔。",
        "constraints_md": "- 1 ≤ n, m ≤ 500",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "data = sys.stdin.read().split()\n"
            "n = int(data[0])\n"
            "m = int(data[1])\n"
            "vals = [int(x) for x in data[2:2 + n * m]]\n"
            "mat = [vals[i * m:(i + 1) * m] for i in range(n)]\n"
            "for j in range(m):\n"
            "    print(' '.join(str(mat[i][j]) for i in range(n)))\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "data = sys.stdin.read().split()\n"
            "n = int(data[0])\n"
            "m = int(data[1])\n"
            "vals = list(map(int, data[2:2 + n * m]))\n"
            "mat = [vals[i * m:(i + 1) * m] for i in range(n)]\n"
            "for row in zip(*mat):\n"
            "    print(' '.join(map(str, row)))\n"
        ),
        "cases": [
            {"stdin": "2 3\n1 2 3\n4 5 6\n", "expected_stdout": "1 4\n2 5\n3 6\n",
             "is_sample": 1, "kind": "sample", "explanation": "2×3 → 3×2"},
            {"stdin": "2 2\n1 2\n3 4\n", "expected_stdout": "1 3\n2 4\n",
             "is_sample": 1, "kind": "sample", "explanation": "方阵：对角不动，其余互换"},
            {"stdin": "1 1\n7\n", "expected_stdout": "7\n", "kind": "manual"},
            {"stdin": "3 1\n1\n2\n3\n", "expected_stdout": "1 2 3\n", "kind": "manual",
             "explanation": "列向量 → 行向量"},
        ],
    },
    # ================================================================== #
    # 第 06 讲 · 字典与集合
    # ================================================================== #
    {
        "title": "两数之和",
        "line": "python",
        "difficulty": 3,
        "total_score": 20,
        "tags": ["字典", "哈希表", "复杂度"],
        "source_section": "第 06 讲 · 字典与集合",
        "statement_md": (
            "给定 `n` 个整数和一个目标值 `t`，找出**一对**下标 `i < j`，"
            "使得 `nums[i] + nums[j] == t`。输出 `i j`；找不到输出 `-1`。\n\n"
            "**如果有多个答案，输出「第二个数的下标最小」的那一组。**\n\n"
            "两种写法：\n\n"
            "- **暴力**：两层循环试所有组合，O(n²)，n = 10⁵ 时会超时\n"
            "- **哈希表**：从左往右扫，边扫边把「值 → 下标」记进字典；"
            "对当前数 `v`，只要查 `t - v` 在不在字典里，O(n)\n\n"
            "这就是字典最典型的用途：**用空间换时间**。"
        ),
        "input_format": "第一行两个整数 `n` 和 `t`；第二行 `n` 个整数，空格分隔。",
        "output_format": "一行：`i j`（0 开始的下标），或 `-1`。",
        "constraints_md": (
            "- 2 ≤ n ≤ 100000\n"
            "- 每个数的绝对值 ≤ 10^9\n"
            "- 时间限制 1000 ms —— 暴力 O(n²) 会超时"
        ),
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "data = sys.stdin.read().split()\n"
            "n = int(data[0])\n"
            "t = int(data[1])\n"
            "nums = [int(x) for x in data[2:2 + n]]\n"
            "seen = {}\n"
            "ans = '-1'\n"
            "for i, v in enumerate(nums):\n"
            "    need = t - v\n"
            "    if need in seen:\n"
            "        ans = '%d %d' % (seen[need], i)\n"
            "        break\n"
            "    if v not in seen:\n"
            "        seen[v] = i\n"
            "print(ans)\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "data = sys.stdin.read().split()\n"
            "n = int(data[0])\n"
            "t = int(data[1])\n"
            "nums = [int(x) for x in data[2:2 + n]]\n"
            "ans = '-1'\n"
            "for i in range(n):\n"
            "    for j in range(i + 1, n):\n"
            "        if nums[i] + nums[j] == t:\n"
            "            ans = '%d %d' % (i, j)\n"
            "            break\n"
            "    if ans != '-1':\n"
            "        break\n"
            "print(ans)\n"
        ),
        "cases": [
            {"stdin": "4 9\n2 7 11 15\n", "expected_stdout": "0 1\n", "is_sample": 1,
             "kind": "sample", "explanation": "2 + 7 = 9"},
            {"stdin": "3 6\n3 2 4\n", "expected_stdout": "1 2\n", "is_sample": 1,
             "kind": "sample", "explanation": "3 + 3 不行（只有一个 3）；2 + 4 = 6"},
            {"stdin": "2 6\n3 3\n", "expected_stdout": "0 1\n", "kind": "manual",
             "explanation": "★ 两个相同的数相加 —— 同一个下标不能用两次，但不同的可以"},
            {"stdin": "3 100\n1 2 3\n", "expected_stdout": "-1\n", "kind": "manual"},
        ],
    },
    {
        "title": "集合运算",
        "line": "python",
        "difficulty": 2,
        "total_score": 15,
        "tags": ["集合", "交集", "并集", "排序"],
        "source_section": "第 06 讲 · 字典与集合",
        "statement_md": (
            "读入两个整数集合（每行一个，元素可能重复、行可能为空），输出两行：\n\n"
            "1. 它们的**交集**（两个集合都有的元素）\n"
            "2. 它们的**并集**（去重后的所有元素）\n\n"
            "两行都要求元素**从小到大**排列，空格分隔；如果结果为空，输出一个空行。\n\n"
            "Python 的集合运算符：`a & b` 交集、`a | b` 并集、`a - b` 差集、`a ^ b` 对称差。"
            "注意集合本身是**无序**的，要保证输出顺序必须自己 `sorted()`。"
        ),
        "input_format": "两行，每行若干个整数（可为空行）。",
        "output_format": "第一行交集，第二行并集，均升序、空格分隔。",
        "constraints_md": "- 每行元素个数 ≤ 100000\n- 每个数的绝对值 ≤ 10^9",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "lines = sys.stdin.read().split('\\n')\n"
            "a = set(int(x) for x in lines[0].split()) if lines else set()\n"
            "b = set(int(x) for x in lines[1].split()) if len(lines) > 1 else set()\n"
            "print(' '.join(map(str, sorted(a & b))))\n"
            "print(' '.join(map(str, sorted(a | b))))\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "lines = sys.stdin.read().split('\\n')\n"
            "a = set(map(int, lines[0].split())) if lines else set()\n"
            "b = set(map(int, (lines[1].split() if len(lines) > 1 else [])))\n"
            "inter = sorted([x for x in a if x in b])\n"
            "uni = sorted(list(a) + [x for x in b if x not in a])\n"
            "print(' '.join(map(str, inter)))\n"
            "print(' '.join(map(str, uni)))\n"
        ),
        "cases": [
            {"stdin": "1 2 3\n2 3 4\n", "expected_stdout": "2 3\n1 2 3 4\n",
             "is_sample": 1, "kind": "sample"},
            {"stdin": "1 2\n3 4\n", "expected_stdout": "\n1 2 3 4\n",
             "is_sample": 1, "kind": "sample",
             "explanation": "交集为空 → 第一行是空行（但仍要输出这一行）"},
            {"stdin": "5 5 5\n5\n", "expected_stdout": "5\n5\n", "kind": "manual",
             "explanation": "集合自动去重，重复的 5 只算一个"},
            {"stdin": "\n\n", "expected_stdout": "\n\n", "kind": "manual",
             "explanation": "两行都空 → 交集并集都空"},
        ],
    },
    {
        "title": "首字母分组",
        "line": "python",
        "difficulty": 2,
        "total_score": 15,
        "tags": ["字典", "分组", "排序"],
        "source_section": "第 06 讲 · 字典与集合",
        "statement_md": (
            "读入 `n` 个单词，按**首字母**分组输出，每组一行，格式：\n\n"
            "```text\n"
            "首字母: 单词1 单词2 …\n"
            "```\n\n"
            "- 组与组之间按**首字母升序**\n"
            "- 组内按**单词字典序**\n\n"
            "```text\n"
            "输入：apple banana avocado blueberry cherry\n"
            "输出：a: apple avocado\n"
            "      b: banana blueberry\n"
            "      c: cherry\n"
            "```\n\n"
            "用字典做「分组」是最常见套路：`groups.setdefault(key, []).append(w)`，"
            "比每次都 `if key not in groups` 简洁。"
        ),
        "input_format": "第一行一个整数 `n`；随后 `n` 行，每行一个小写单词。",
        "output_format": "每组一行，`首字母: 单词…`。",
        "constraints_md": "- 1 ≤ n ≤ 100000\n- 单词由小写字母组成，长度 ≤ 20",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "data = sys.stdin.read().split()\n"
            "n = int(data[0])\n"
            "words = data[1:1 + n]\n"
            "groups = {}\n"
            "for w in words:\n"
            "    groups.setdefault(w[0], []).append(w)\n"
            "for k in sorted(groups):\n"
            "    print('%s: %s' % (k, ' '.join(sorted(groups[k]))))\n"
        ),
        "alt_solution": (
            "import sys\n"
            "from itertools import groupby\n\n"
            "data = sys.stdin.read().split()\n"
            "n = int(data[0])\n"
            "words = sorted(data[1:1 + n])\n"
            "for k, g in groupby(words, key=lambda w: w[0]):\n"
            "    print('%s: %s' % (k, ' '.join(g)))\n"
        ),
        "cases": [
            {"stdin": "5\napple\nbanana\navocado\nblueberry\ncherry\n",
             "expected_stdout": "a: apple avocado\nb: banana blueberry\nc: cherry\n",
             "is_sample": 1, "kind": "sample",
             "explanation": "a 组内 apple < avocado（字母序）"},
            {"stdin": "2\ndog\nant\n", "expected_stdout": "a: ant\nd: dog\n",
             "is_sample": 1, "kind": "sample",
             "explanation": "输入顺序 dog 在前，但 a 组要先输出"},
            {"stdin": "1\ncat\n", "expected_stdout": "c: cat\n", "kind": "manual"},
        ],
    },
    {
        "title": "众数",
        "line": "python",
        "difficulty": 2,
        "total_score": 15,
        "tags": ["字典", "计数", "并列处理"],
        "source_section": "第 06 讲 · 字典与集合",
        "statement_md": (
            "读入 `n` 个整数，输出**出现次数最多**的那个数。\n\n"
            "**如果并列，输出最小的那个。**\n\n"
            "例如 `1 1 2 2` 里 1 和 2 都出现 2 次，答案是 `1`。\n\n"
            "**并列规则是这题唯一的坑**：`max(cnt, key=cnt.get)` 在并列时返回的是"
            "「字典里先出现的键」，而字典的顺序取决于插入顺序，**不可靠**。"
            "显式写出比较规则才稳。"
        ),
        "input_format": "第一行一个整数 `n`；第二行 `n` 个整数。",
        "output_format": "一行，众数。",
        "constraints_md": "- 1 ≤ n ≤ 100000\n- 每个数的绝对值 ≤ 10^9",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "data = sys.stdin.read().split()\n"
            "n = int(data[0])\n"
            "nums = [int(x) for x in data[1:1 + n]]\n"
            "cnt = {}\n"
            "for v in nums:\n"
            "    cnt[v] = cnt.get(v, 0) + 1\n"
            "best = None\n"
            "best_c = -1\n"
            "for v in sorted(cnt):\n"
            "    if cnt[v] > best_c:\n"
            "        best = v\n"
            "        best_c = cnt[v]\n"
            "print(best)\n"
        ),
        "alt_solution": (
            "import sys\n"
            "from collections import Counter\n\n"
            "data = sys.stdin.read().split()\n"
            "n = int(data[0])\n"
            "nums = list(map(int, data[1:1 + n]))\n"
            "c = Counter(nums)\n"
            "print(min(c, key=lambda v: (-c[v], v)))\n"
        ),
        "cases": [
            {"stdin": "6\n3 1 2 1 3 3\n", "expected_stdout": "3\n", "is_sample": 1,
             "kind": "sample", "explanation": "3 出现 3 次，最多"},
            {"stdin": "4\n1 1 2 2\n", "expected_stdout": "1\n", "is_sample": 1,
             "kind": "sample", "explanation": "★ 并列 2 次 → 取小的 → 1"},
            {"stdin": "1\n5\n", "expected_stdout": "5\n", "kind": "manual"},
        ],
    },
    {
        "title": "缺失的最小正整数",
        "line": "python",
        "difficulty": 3,
        "total_score": 20,
        "tags": ["集合", "边界", "思维题"],
        "source_section": "第 06 讲 · 字典与集合",
        "statement_md": (
            "给定 `n` 个整数（可能有负数、有重复），找出其中**没有出现**的"
            "**最小正整数**。\n\n"
            "```text\n"
            "输入：1 2 0        输出：3\n"
            "输入：3 4 -1 1     输出：2\n"
            "输入：7 8 9 11 12  输出：1\n"
            "```\n\n"
            "**思路**：把所有正数丢进集合，然后从 `1` 开始一个个试 —— "
            "`1` 在不在？在；`2` 在不在？不在 → 答案 2。\n\n"
            "看着简单，但**负数、0、重复值**这三样都容易让人绕晕，"
            "用集合一把过滤掉最省心。"
        ),
        "input_format": "第一行一个整数 `n`；第二行 `n` 个整数。",
        "output_format": "一行，一个正整数。",
        "constraints_md": "- 1 ≤ n ≤ 100000\n- 每个数的绝对值 ≤ 10^9",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "data = sys.stdin.read().split()\n"
            "n = int(data[0])\n"
            "nums = [int(x) for x in data[1:1 + n]]\n"
            "s = set(x for x in nums if x > 0)\n"
            "v = 1\n"
            "while v in s:\n"
            "    v += 1\n"
            "print(v)\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "data = sys.stdin.read().split()\n"
            "n = int(data[0])\n"
            "nums = list(map(int, data[1:1 + n]))\n"
            "pos = sorted(set(x for x in nums if x > 0))\n"
            "v = 1\n"
            "for x in pos:\n"
            "    if x == v:\n"
            "        v += 1\n"
            "    elif x > v:\n"
            "        break\n"
            "print(v)\n"
        ),
        "cases": [
            {"stdin": "3\n1 2 0\n", "expected_stdout": "3\n", "is_sample": 1,
             "kind": "sample", "explanation": "1 在、2 在、3 不在 → 3"},
            {"stdin": "4\n3 4 -1 1\n", "expected_stdout": "2\n", "is_sample": 1,
             "kind": "sample", "explanation": "1 在、2 不在 → 2；负数直接忽略"},
            {"stdin": "5\n7 8 9 11 12\n", "expected_stdout": "1\n", "kind": "manual",
             "explanation": "★ 没有 1 → 答案就是 1，后面的数再大也没用"},
            {"stdin": "3\n1 2 3\n", "expected_stdout": "4\n", "kind": "manual"},
        ],
    },
    # ================================================================== #
    # 第 07 讲 · 函数（上）：定义 / 参数 / 默认值
    # ================================================================== #
    {
        "title": "海伦公式",
        "line": "python",
        "difficulty": 2,
        "total_score": 15,
        "tags": ["函数", "math", "浮点", "合法性判断"],
        "source_section": "第 07 讲 · 函数",
        "statement_md": (
            "给定三角形三边长 `a` `b` `c`，能构成三角形就输出面积（**保留 2 位小数**），"
            "否则输出 `invalid`。\n\n"
            "**海伦公式**（记 `p = (a+b+c)/2`）：\n\n"
            "```text\n"
            "面积 = √( p × (p-a) × (p-b) × (p-c) )\n"
            "```\n\n"
            "**构成条件**：三边都大于 0，且**任意两边之和大于第三边**"
            "（只要检查三组，别只查一组）。\n\n"
            "这题很适合封装成一个函数 `area(a, b, c)`，边界检查放函数开头。"
        ),
        "input_format": "一行，三个数 `a` `b` `c`（可能是小数）。",
        "output_format": "一行，面积（2 位小数）或 `invalid`。",
        "constraints_md": "- 0 ≤ a, b, c ≤ 10000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n"
            "import math\n\n"
            "a, b, c = map(float, sys.stdin.read().split())\n"
            "if a <= 0 or b <= 0 or c <= 0 or a + b <= c or a + c <= b or b + c <= a:\n"
            "    print('invalid')\n"
            "else:\n"
            "    p = (a + b + c) / 2\n"
            "    print('%.2f' % math.sqrt(p * (p - a) * (p - b) * (p - c)))\n"
        ),
        "alt_solution": (
            "import sys\n"
            "import math\n\n"
            "a, b, c = map(float, sys.stdin.read().split())\n"
            "ok = (a > 0 and b > 0 and c > 0\n"
            "      and a + b > c and a + c > b and b + c > a)\n"
            "if not ok:\n"
            "    print('invalid')\n"
            "else:\n"
            "    cos_c = (a * a + b * b - c * c) / (2 * a * b)\n"
            "    sin_c = math.sqrt(max(0.0, 1 - cos_c * cos_c))\n"
            "    print('%.2f' % (0.5 * a * b * sin_c))\n"
        ),
        "cases": [
            {"stdin": "3 4 5\n", "expected_stdout": "6.00\n", "is_sample": 1,
             "kind": "sample", "explanation": "直角三角形，3×4/2 = 6"},
            {"stdin": "1 1 1\n", "expected_stdout": "0.43\n", "is_sample": 1,
             "kind": "sample", "explanation": "等边三角形：√3/4 ≈ 0.4330 → 0.43"},
            {"stdin": "2 2 3\n", "expected_stdout": "1.98\n", "kind": "manual"},
            {"stdin": "1 2 3\n", "expected_stdout": "invalid\n", "kind": "manual",
             "explanation": "★ 1 + 2 = 3，退化成线段，不构成三角形"},
            {"stdin": "1 1 2\n", "expected_stdout": "invalid\n", "kind": "manual",
             "explanation": "等腰但退化了"},
        ],
    },
    {
        "title": "可变默认参数的陷阱",
        "line": "python",
        "difficulty": 3,
        "total_score": 20,
        "tags": ["函数", "默认参数", "可变对象", "★坑"],
        "source_section": "第 07 讲 · 函数",
        "statement_md": (
            "这是 Python 最著名的坑之一，**请亲手跑一遍看看**。\n\n"
            "```python\n"
            "def collect_bad(x, lst=[]):    # 默认值是个列表\n"
            "    lst.append(x)\n"
            "    return lst\n"
            "```\n\n"
            "每次调用看起来都会新建一个空列表？**并不会。** "
            "默认参数只在**函数定义时求值一次**，所以那个 `[]` 是**所有调用共享的同一个对象**，"
            "会一直累积。\n\n"
            "正解是默认写成 `None`，在函数体里现建：\n\n"
            "```python\n"
            "def collect_ok(x, lst=None):\n"
            "    if lst is None:\n"
            "        lst = []\n"
            "    ...\n"
            "```\n\n"
            "**本题要求**：读入 `n` 和一个数列，依次做两件事：\n\n"
            "1. 用上面的 `collect_bad` 把每个数依次传进去，最后输出它返回的列表\n"
            "2. 再用 `collect_ok` 把每个数依次传进去，**每次的结果单独输出一行**"
        ),
        "input_format": "第一行一个整数 `n`（≥1）；第二行 `n` 个整数。",
        "output_format": (
            "第一行：`collect_bad` 最后一次返回的列表（标准 Python 列表格式）。\n\n"
            "随后 `n` 行：`collect_ok` 每次调用的返回值。"
        ),
        "constraints_md": "- 1 ≤ n ≤ 100\n- 每个数的绝对值 ≤ 10^9",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "data = sys.stdin.read().split()\n"
            "n = int(data[0])\n"
            "xs = [int(x) for x in data[1:1 + n]]\n\n"
            "def collect_bad(x, lst=[]):\n"
            "    lst.append(x)\n"
            "    return lst\n\n"
            "def collect_ok(x, lst=None):\n"
            "    if lst is None:\n"
            "        lst = []\n"
            "    lst.append(x)\n"
            "    return lst\n\n"
            "last = None\n"
            "for x in xs:\n"
            "    last = collect_bad(x)\n"
            "print(last)\n"
            "for x in xs:\n"
            "    print(collect_ok(x))\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "data = sys.stdin.read().split()\n"
            "n = int(data[0])\n"
            "xs = [int(x) for x in data[1:1 + n]]\n"
            "print('[' + ', '.join(str(x) for x in xs) + ']')\n"
            "for x in xs:\n"
            "    print('[%d]' % x)\n"
        ),
        "cases": [
            {"stdin": "3\n1 2 3\n",
             "expected_stdout": "[1, 2, 3]\n[1]\n[2]\n[3]\n",
             "is_sample": 1, "kind": "sample",
             "explanation": "★ 上面那段累积成 [1, 2, 3]；下面那段每次都是新列表"},
            {"stdin": "1\n9\n", "expected_stdout": "[9]\n[9]\n", "kind": "manual",
             "explanation": "n = 1 时两种写法结果一样 —— 坑要调用两次才看得见"},
        ],
    },
    {
        "title": "哥德巴赫猜想",
        "line": "python",
        "difficulty": 3,
        "total_score": 20,
        "tags": ["函数", "素数", "复用", "循环"],
        "source_section": "第 07 讲 · 函数",
        "statement_md": (
            "**哥德巴赫猜想**：任一大于 2 的偶数都可以写成两个素数之和。\n\n"
            "给定一个偶数 `n`（≥ 4），输出一对素数 `a b`，满足 `a + b = n` 且 "
            "**`a` 尽可能小**（`a ≤ b`）。\n\n"
            "```text\n"
            "10 → 3 7\n"
            "20 → 3 17\n"
            "100 → 3 97\n"
            "```\n\n"
            "**思路**：`a` 从 2 开始往上试，只要 `a` 和 `n - a` 都是素数就输出。\n\n"
            "这题是「函数复用」的好例子：把「判断素数」单独写成函数，"
            "主逻辑就只剩几行了。"
        ),
        "input_format": "一行，一个偶数 `n`。",
        "output_format": "一行，`a b`，其中 `a ≤ b` 且 `a` 最小。",
        "constraints_md": "- 4 ≤ n ≤ 10^7，且 n 是偶数",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "n = int(sys.stdin.read().strip())\n\n"
            "def is_prime(k):\n"
            "    if k < 2:\n"
            "        return False\n"
            "    i = 2\n"
            "    while i * i <= k:\n"
            "        if k % i == 0:\n"
            "            return False\n"
            "        i += 1\n"
            "    return True\n\n"
            "for a in range(2, n // 2 + 1):\n"
            "    if is_prime(a) and is_prime(n - a):\n"
            "        print(a, n - a)\n"
            "        break\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "n = int(sys.stdin.read().strip())\n"
            "sieve = [True] * (n + 1)\n"
            "sieve[0] = False\n"
            "if n >= 1:\n"
            "    sieve[1] = False\n"
            "i = 2\n"
            "while i * i <= n:\n"
            "    if sieve[i]:\n"
            "        for j in range(i * i, n + 1, i):\n"
            "            sieve[j] = False\n"
            "    i += 1\n"
            "for a in range(2, n // 2 + 1):\n"
            "    if sieve[a] and sieve[n - a]:\n"
            "        print(a, n - a)\n"
            "        break\n"
        ),
        "cases": [
            {"stdin": "4\n", "expected_stdout": "2 2\n", "is_sample": 1,
             "kind": "sample", "explanation": "最小的偶数：2 + 2"},
            {"stdin": "10\n", "expected_stdout": "3 7\n", "is_sample": 1,
             "kind": "sample", "explanation": "2 + 8 不行（8 非素数），3 + 7 可以"},
            {"stdin": "20\n", "expected_stdout": "3 17\n", "kind": "manual",
             "explanation": "2+18、3+17 —— 17 是素数"},
            {"stdin": "100\n", "expected_stdout": "3 97\n", "kind": "manual",
             "explanation": ("★ 从 2 试到 97：2+98(98非素)、3+97(✓) 立刻命中；"
                             "别以为「a 小就一定命中得快」，100 这里确实很快")},
        ],
    },
    # ================================================================== #
    # 第 08 讲 · 函数（下）：递归
    # ================================================================== #
    {
        "title": "递归求阶乘",
        "line": "python",
        "difficulty": 2,
        "total_score": 15,
        "tags": ["递归", "大整数", "边界"],
        "source_section": "第 08 讲 · 函数",
        "statement_md": (
            "用**递归**求 `n!`（n 的阶乘）。\n\n"
            "定义：`0! = 1`，`n! = n × (n-1)!`。\n\n"
            "**递归三要素**（对照着看）：\n\n"
            "1. **出口**：`n <= 1` 时返回 1\n"
            "2. **递推**：`n × fact(n-1)`\n"
            "3. **规模变小**：每层 `n` 减 1，必然到出口\n\n"
            "Python 整数无上限，`20!`（19 位）直接算，不会溢出。"
        ),
        "input_format": "一行，一个整数 `n`。",
        "output_format": "一行，`n!`。",
        "constraints_md": "- 0 ≤ n ≤ 20",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "n = int(sys.stdin.read().strip())\n\n"
            "def fact(k):\n"
            "    if k <= 1:\n"
            "        return 1\n"
            "    return k * fact(k - 1)\n\n"
            "print(fact(n))\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "n = int(sys.stdin.read().strip())\n"
            "r = 1\n"
            "for i in range(2, n + 1):\n"
            "    r *= i\n"
            "print(r)\n"
        ),
        "cases": [
            {"stdin": "0\n", "expected_stdout": "1\n", "is_sample": 1,
             "kind": "sample", "explanation": "★ 0! = 1，不是 0（数学约定）"},
            {"stdin": "5\n", "expected_stdout": "120\n", "is_sample": 1,
             "kind": "sample", "explanation": "1×2×3×4×5 = 120"},
            {"stdin": "1\n", "expected_stdout": "1\n", "kind": "manual",
             "explanation": "出口分支"},
            {"stdin": "10\n", "expected_stdout": "3628800\n", "kind": "manual"},
            {"stdin": "20\n", "expected_stdout": "2432902008176640000\n",
             "kind": "manual",
             "explanation": "★ 19 位数，超出 64 位整数（≈9.2×10^18）范围"},
        ],
    },
    {
        "title": "汉诺塔",
        "line": "python",
        "difficulty": 3,
        "total_score": 20,
        "tags": ["递归", "经典问题", "步骤输出"],
        "source_section": "第 08 讲 · 函数",
        "statement_md": (
            "汉诺塔：`n` 个盘子从柱子 `A` 借助 `B` 全部移到 `C`。\n\n"
            "每次只能移动一个盘子，且**大盘不能压在小盘上**。\n\n"
            "输出完整移动步骤，每行形如 `A->C`；最后一行输出总步数 `total=步数`。\n\n"
            "**递归思路**（把大问题拆成三小步）：\n\n"
            "1. 把上面 `n-1` 个从 `A` 移到 `B`（借助 `C`）\n"
            "2. 把最大的那个从 `A` 移到 `C`\n"
            "3. 把那 `n-1` 个从 `B` 移到 `C`（借助 `A`）\n\n"
            "三条语句，就是这个算法的全部。总步数 = `2ⁿ - 1`。"
        ),
        "input_format": "一行，一个整数 `n`。",
        "output_format": "每行一步（`A->C`），最后一行 `total=步数`。",
        "constraints_md": "- 1 ≤ n ≤ 20（输出可能很大，n 别开太大）",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "n = int(sys.stdin.read().strip())\n"
            "moves = []\n\n"
            "def hanoi(k, a, b, c):\n"
            "    if k == 0:\n"
            "        return\n"
            "    hanoi(k - 1, a, c, b)\n"
            "    moves.append('%s->%s' % (a, c))\n"
            "    hanoi(k - 1, b, a, c)\n\n"
            "hanoi(n, 'A', 'B', 'C')\n"
            "for m in moves:\n"
            "    print(m)\n"
            "print('total=%d' % len(moves))\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "n = int(sys.stdin.read().strip())\n\n"
            "def hanoi(k, a, b, c):\n"
            "    if k:\n"
            "        yield from hanoi(k - 1, a, c, b)\n"
            "        yield a + '->' + c\n"
            "        yield from hanoi(k - 1, b, a, c)\n\n"
            "moves = list(hanoi(n, 'A', 'B', 'C'))\n"
            "print('\\n'.join(moves))\n"
            "print('total=%d' % (2 ** n - 1))\n"
        ),
        "cases": [
            {"stdin": "1\n", "expected_stdout": "A->C\ntotal=1\n", "is_sample": 1,
             "kind": "sample", "explanation": "2¹ − 1 = 1"},
            {"stdin": "2\n", "expected_stdout": "A->B\nA->C\nB->C\ntotal=3\n",
             "is_sample": 1, "kind": "sample",
             "explanation": "2² − 1 = 3：小盘去 B，大盘去 C，小盘再跟过去"},
            {"stdin": "3\n",
             "expected_stdout": "A->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\ntotal=7\n",
             "kind": "manual", "explanation": "2³ − 1 = 7"},
        ],
    },
    {
        "title": "数位之和",
        "line": "python",
        "difficulty": 2,
        "total_score": 15,
        "tags": ["递归", "取余", "整除"],
        "source_section": "第 08 讲 · 函数",
        "statement_md": (
            "用**递归**求一个非负整数的各位数字之和。\n\n"
            "```text\n"
            "123 → 1 + 2 + 3 = 6\n"
            "```\n\n"
            "**关键是把「拆最后一位」和「剩下的数」分开**：\n\n"
            "```python\n"
            "def digit_sum(k):\n"
            "    if k < 10:\n"
            "        return k          # 出口：只剩一位\n"
            "    return k % 10 + digit_sum(k // 10)\n"
            "```\n\n"
            "`k % 10` 拿个位，`k // 10` 把个位丢掉。"
            "**别用 `str()`** —— 这题就是要练数位运算。"
        ),
        "input_format": "一行，一个非负整数 `n`。",
        "output_format": "一行，各位数字之和。",
        "constraints_md": "- 0 ≤ n ≤ 10^18",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "n = int(sys.stdin.read().strip())\n\n"
            "def digit_sum(k):\n"
            "    if k < 10:\n"
            "        return k\n"
            "    return k % 10 + digit_sum(k // 10)\n\n"
            "print(digit_sum(n))\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "s = sys.stdin.read().strip()\n"
            "print(sum(int(ch) for ch in s))\n"
        ),
        "cases": [
            {"stdin": "123\n", "expected_stdout": "6\n", "is_sample": 1,
             "kind": "sample"},
            {"stdin": "99999\n", "expected_stdout": "45\n", "is_sample": 1,
             "kind": "sample", "explanation": "5 × 9 = 45"},
            {"stdin": "0\n", "expected_stdout": "0\n", "kind": "manual",
             "explanation": "★ 边界：0 的位和是 0（出口分支直接接住）"},
            {"stdin": "1000000\n", "expected_stdout": "1\n", "kind": "manual",
             "explanation": "一堆 0 中间夹一个 1"},
        ],
    },
    {
        "title": "爬楼梯",
        "line": "python",
        "difficulty": 3,
        "total_score": 20,
        "tags": ["递归", "记忆化", "斐波那契", "重复子问题"],
        "source_section": "第 08 讲 · 函数",
        "statement_md": (
            "有 `n` 级楼梯，每次可以走 **1 级或 2 级**，问有多少种走法。\n\n"
            "设 `f(n)` 为走法数，则 `f(n) = f(n-1) + f(n-2)`，"
            "`f(1) = 1`、`f(2) = 2`。\n\n"
            "**递归树的坑**：直接写朴素递归，`f(n)` 会重复计算大量子问题 —— "
            "`f(40)` 就要算十亿次以上。两种解法：\n\n"
            "- **记忆化**：算过的存进字典，下次直接取\n"
            "- **自底向上**：从 `f(1)` 开始往上推，只用两个变量\n\n"
            "这就是「动态规划」的雏形：**用缓存消掉重复子问题**。"
        ),
        "input_format": "一行，一个整数 `n`。",
        "output_format": "一行，走法总数。",
        "constraints_md": (
            "- 1 ≤ n ≤ 90\n"
            "- 时间限制 1000 ms —— 朴素递归必超时"
        ),
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "n = int(sys.stdin.read().strip())\n"
            "a, b = 1, 1\n"
            "for _ in range(n - 1):\n"
            "    a, b = b, a + b\n"
            "print(b)\n"
        ),
        "alt_solution": (
            "import sys\n"
            "sys.setrecursionlimit(10000)\n\n"
            "n = int(sys.stdin.read().strip())\n"
            "memo = {0: 1, 1: 1}\n\n"
            "def f(k):\n"
            "    if k not in memo:\n"
            "        memo[k] = f(k - 1) + f(k - 2)\n"
            "    return memo[k]\n\n"
            "print(f(n))\n"
        ),
        "cases": [
            {"stdin": "1\n", "expected_stdout": "1\n", "is_sample": 1,
             "kind": "sample", "explanation": "只能一步 1 级"},
            {"stdin": "2\n", "expected_stdout": "2\n", "is_sample": 1,
             "kind": "sample", "explanation": "1+1 或 2"},
            {"stdin": "3\n", "expected_stdout": "3\n", "kind": "manual",
             "explanation": "1+1+1、1+2、2+1"},
            {"stdin": "5\n", "expected_stdout": "8\n", "kind": "manual"},
            {"stdin": "10\n", "expected_stdout": "89\n", "kind": "manual",
             "explanation": "正好是斐波那契数列第 11 项"},
        ],
    },
    {
        "title": "二分查找",
        "line": "python",
        "difficulty": 2,
        "total_score": 15,
        "tags": ["二分", "下标", "边界"],
        "source_section": "第 08 讲 · 函数",
        "statement_md": (
            "给定一个**升序**整数序列和一个目标值，输出目标值的下标（从 0 开始）；"
            "不存在输出 `-1`。\n\n"
            "**二分查找**：每次取中间元素比大小，比目标小就去右半边，大就去左半边。"
            "每次砍掉一半，所以是 O(log n)。\n\n"
            "**最容易写错的三处**：\n\n"
            "- `while lo <= hi` 还是 `<` —— 用闭区间就写 `<=`\n"
            "- 中点 `mid = (lo + hi) // 2`，别写成 `/`\n"
            "- 移动时 `lo = mid + 1` / `hi = mid - 1`，**必须 ±1**，"
            "否则区间不缩小 → 死循环"
        ),
        "input_format": "第一行两个整数 `n` 和 `t`；第二行 `n` 个升序整数。",
        "output_format": "一行，下标或 `-1`。",
        "constraints_md": "- 1 ≤ n ≤ 100000\n- 序列严格升序，绝对值 ≤ 10^9",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "data = sys.stdin.read().split()\n"
            "n = int(data[0])\n"
            "t = int(data[1])\n"
            "a = [int(x) for x in data[2:2 + n]]\n"
            "lo, hi = 0, n - 1\n"
            "ans = -1\n"
            "while lo <= hi:\n"
            "    mid = (lo + hi) // 2\n"
            "    if a[mid] == t:\n"
            "        ans = mid\n"
            "        break\n"
            "    elif a[mid] < t:\n"
            "        lo = mid + 1\n"
            "    else:\n"
            "        hi = mid - 1\n"
            "print(ans)\n"
        ),
        "alt_solution": (
            "import sys\n"
            "import bisect\n\n"
            "data = sys.stdin.read().split()\n"
            "n = int(data[0])\n"
            "t = int(data[1])\n"
            "a = list(map(int, data[2:2 + n]))\n"
            "i = bisect.bisect_left(a, t)\n"
            "print(i if i < n and a[i] == t else -1)\n"
        ),
        "cases": [
            {"stdin": "5 5\n1 3 5 7 9\n", "expected_stdout": "2\n", "is_sample": 1,
             "kind": "sample", "explanation": "正中命中"},
            {"stdin": "5 1\n1 3 5 7 9\n", "expected_stdout": "0\n", "is_sample": 1,
             "kind": "sample", "explanation": "左边界"},
            {"stdin": "5 9\n1 3 5 7 9\n", "expected_stdout": "4\n", "kind": "manual",
             "explanation": "右边界"},
            {"stdin": "5 4\n1 3 5 7 9\n", "expected_stdout": "-1\n", "kind": "manual",
             "explanation": "4 不在序列里，最后 lo > hi 退出"},
            {"stdin": "4 3\n1 2 3 4\n", "expected_stdout": "2\n", "kind": "manual"},
        ],
    },
    # ================================================================== #
    # 第 09 讲 · 模块与包
    # ================================================================== #
    {
        "title": "math 模块",
        "line": "python",
        "difficulty": 1,
        "total_score": 10,
        "tags": ["模块", "import", "math", "格式化"],
        "source_section": "第 09 讲 · 模块与包",
        "statement_md": (
            "读入一个浮点数 `n`，在同一行输出三个值：\n\n"
            "```text\n"
            "√n（保留 3 位小数）  ⌈n⌉（向上取整）  ⌊n⌋（向下取整）\n"
            "```\n\n"
            "**三种 import 写法**，效果一样但用法不同：\n\n"
            "```python\n"
            "import math                 # 用的时候写 math.sqrt(n)\n"
            "from math import sqrt       # 直接写 sqrt(n)\n"
            "import math as m            # 写 m.sqrt(n)\n"
            "```\n\n"
            "**注意取整函数的返回值是整数**：`math.ceil(2.1)` 得 `3`（int），"
            "打印出来没有小数点。"
        ),
        "input_format": "一行，一个非负浮点数 `n`。",
        "output_format": "一行，`√n(3位小数) 向上取整 向下取整`。",
        "constraints_md": "- 0 ≤ n ≤ 10^9",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n"
            "import math\n\n"
            "n = float(sys.stdin.read().strip())\n"
            "print('%.3f %d %d' % (math.sqrt(n), math.ceil(n), math.floor(n)))\n"
        ),
        "alt_solution": (
            "import sys\n"
            "import math\n\n"
            "n = float(sys.stdin.read().strip())\n"
            "print('%.3f %d %d' % (n ** 0.5, math.ceil(n), math.floor(n)))\n"
        ),
        "cases": [
            {"stdin": "2\n", "expected_stdout": "1.414 2 2\n", "is_sample": 1,
             "kind": "sample", "explanation": "√2 ≈ 1.4142 → 1.414"},
            {"stdin": "2.5\n", "expected_stdout": "1.581 3 2\n", "is_sample": 1,
             "kind": "sample", "explanation": "★ 中间那个不是整数，向上 3、向下 2"},
            {"stdin": "9\n", "expected_stdout": "3.000 9 9\n", "kind": "manual",
             "explanation": "完全平方数，补齐 3 位小数"},
            {"stdin": "0.5\n", "expected_stdout": "0.707 1 0\n", "kind": "manual",
             "explanation": "★ 小于 1 的数：向上取整是 1，向下取整是 0"},
        ],
    },
    {
        "title": "日期相差天数",
        "line": "python",
        "difficulty": 3,
        "total_score": 20,
        "tags": ["模块", "datetime", "闰年", "日期计算"],
        "source_section": "第 09 讲 · 模块与包",
        "statement_md": (
            "读入两个日期（格式 `YYYY-MM-DD`），输出**第二个日期减去第一个日期**相差的天数"
            "（可能为负）。\n\n"
            "标准库 `datetime` 让这件事变得非常简单：\n\n"
            "```python\n"
            "from datetime import date\n"
            "d1 = date(2024, 1, 1)\n"
            "d2 = date(2024, 12, 31)\n"
            "print((d2 - d1).days)     # 365\n"
            "```\n\n"
            "**自己手算的话要注意闰年**：2024 能被 4 整除且不是世纪年 → 闰年，"
            "2 月 29 天；2023 是平年。`date` 对象相减会自动处理这些。"
        ),
        "input_format": "两行，每行一个日期，格式 `YYYY-MM-DD`。",
        "output_format": "一行，整数天数（`d2 - d1`，可为负）。",
        "constraints_md": "- 1900 ≤ 年份 ≤ 2100",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n"
            "from datetime import date\n\n"
            "def parse(s):\n"
            "    y, m, d = s.strip().split('-')\n"
            "    return date(int(y), int(m), int(d))\n\n"
            "parts = sys.stdin.read().split()\n"
            "d1 = parse(parts[0])\n"
            "d2 = parse(parts[1])\n"
            "print((d2 - d1).days)\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "_MD = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]\n\n"
            "def to_days(s):\n"
            "    y, m, d = map(int, s.strip().split('-'))\n"
            "    total = 0\n"
            "    for yy in range(1, y):\n"
            "        total += 366 if (yy % 4 == 0 and yy % 100 != 0) or yy % 400 == 0 else 365\n"
            "    leap = (y % 4 == 0 and y % 100 != 0) or y % 400 == 0\n"
            "    for mm in range(1, m):\n"
            "        total += _MD[mm - 1]\n"
            "        if mm == 2 and leap:\n"
            "            total += 1\n"
            "    return total + d\n\n"
            "parts = sys.stdin.read().split()\n"
            "print(to_days(parts[1]) - to_days(parts[0]))\n"
        ),
        "cases": [
            {"stdin": "2024-01-01\n2024-12-31\n", "expected_stdout": "365\n",
             "is_sample": 1, "kind": "sample",
             "explanation": "2024 是闰年，全年 366 天，从 1/1 到 12/31 差 365 天"},
            {"stdin": "2023-02-28\n2023-03-01\n", "expected_stdout": "1\n",
             "is_sample": 1, "kind": "sample",
             "explanation": "2023 平年，2 月只有 28 天，直接跨一天"},
            {"stdin": "2024-02-28\n2024-03-01\n", "expected_stdout": "2\n",
             "kind": "manual",
             "explanation": "★ 2024 闰年有 2 月 29 日，同样两天却差了 2 天"},
            {"stdin": "2023-12-31\n2024-01-01\n", "expected_stdout": "1\n",
             "kind": "manual", "explanation": "跨年"},
            {"stdin": "2024-03-01\n2024-02-28\n", "expected_stdout": "-2\n",
             "kind": "manual", "explanation": "★ 倒过来就是负数，别写成绝对值"},
        ],
    },
    {
        "title": "均值与中位数",
        "line": "python",
        "difficulty": 2,
        "total_score": 15,
        "tags": ["模块", "statistics", "中位数", "奇偶"],
        "source_section": "第 09 讲 · 模块与包",
        "statement_md": (
            "读入 `n` 个整数，输出**平均值**和**中位数**，都用 2 位小数，空格分隔。\n\n"
            "**中位数的定义**（这题的核心）：\n\n"
            "- 先排序\n"
            "- `n` 为**奇数**：正中间那个\n"
            "- `n` 为**偶数**：中间两个的**平均值**\n\n"
            "标准库 `statistics` 两个函数就够：`statistics.mean(xs)` 和 "
            "`statistics.median(xs)`。"
        ),
        "input_format": "第一行一个整数 `n`；第二行 `n` 个整数。",
        "output_format": "一行，`平均值 中位数`（各 2 位小数）。",
        "constraints_md": "- 1 ≤ n ≤ 100000\n- 每个数的绝对值 ≤ 10^9",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n"
            "import statistics\n\n"
            "data = sys.stdin.read().split()\n"
            "n = int(data[0])\n"
            "nums = [int(x) for x in data[1:1 + n]]\n"
            "print('%.2f %.2f' % (statistics.mean(nums), statistics.median(nums)))\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "data = sys.stdin.read().split()\n"
            "n = int(data[0])\n"
            "s = sorted(int(x) for x in data[1:1 + n])\n"
            "m = len(s)\n"
            "med = s[m // 2] if m % 2 else (s[m // 2 - 1] + s[m // 2]) / 2\n"
            "print('%.2f %.2f' % (sum(s) / m, med))\n"
        ),
        "cases": [
            {"stdin": "4\n1 2 3 4\n", "expected_stdout": "2.50 2.50\n", "is_sample": 1,
             "kind": "sample", "explanation": "偶数个 → 中位数取 (2+3)/2 = 2.5"},
            {"stdin": "5\n1 2 3 4 5\n", "expected_stdout": "3.00 3.00\n",
             "is_sample": 1, "kind": "sample", "explanation": "奇数个 → 正中间 3"},
            {"stdin": "3\n1 2 10\n", "expected_stdout": "4.33 2.00\n", "kind": "manual",
             "explanation": "★ 均值被 10 拉高到 4.33，中位数还是 2 —— 这就是中位数的意义"},
        ],
    },
    {
        "title": "累乘",
        "line": "python",
        "difficulty": 2,
        "total_score": 15,
        "tags": ["模块", "functools", "reduce", "大整数"],
        "source_section": "第 09 讲 · 模块与包",
        "statement_md": (
            "读入 `n` 个整数，输出它们的**连乘积**。\n\n"
            "```text\n"
            "1 2 3 4 5 → 120\n"
            "```\n\n"
            "两种标准库写法：\n\n"
            "- `math.prod(nums)` —— Python 3.8+ 新增，最直接\n"
            "- `functools.reduce(lambda a, b: a * b, nums, 1)` —— 老牌做法，"
            "「把二元操作不停地往序列上套」\n\n"
            "注意初始值 `1` 不能省 —— 少写初始值，`n = 1` 时会直接把那个数当结果返回"
            "（恰好对），但 `n = 0` 就会报错。"
        ),
        "input_format": "第一行一个整数 `n`；第二行 `n` 个整数。",
        "output_format": "一行，连乘积。",
        "constraints_md": "- 1 ≤ n ≤ 100\n- 每个数的绝对值 ≤ 10^9",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n"
            "from functools import reduce\n\n"
            "data = sys.stdin.read().split()\n"
            "n = int(data[0])\n"
            "nums = [int(x) for x in data[1:1 + n]]\n"
            "print(reduce(lambda a, b: a * b, nums, 1))\n"
        ),
        "alt_solution": (
            "import sys\n"
            "import math\n\n"
            "data = sys.stdin.read().split()\n"
            "n = int(data[0])\n"
            "print(math.prod(int(x) for x in data[1:1 + n]))\n"
        ),
        "cases": [
            {"stdin": "3\n2 3 4\n", "expected_stdout": "24\n", "is_sample": 1,
             "kind": "sample"},
            {"stdin": "5\n1 2 3 4 5\n", "expected_stdout": "120\n", "is_sample": 1,
             "kind": "sample", "explanation": "5! = 120"},
            {"stdin": "4\n10 10 10 10\n", "expected_stdout": "10000\n",
             "kind": "manual"},
            {"stdin": "1\n7\n", "expected_stdout": "7\n", "kind": "manual",
             "explanation": "只有一个数 → 结果就是它"},
        ],
    },
    {
        "title": "最高分学生",
        "line": "python",
        "difficulty": 2,
        "total_score": 15,
        "tags": ["模块", "排序", "key", "并列规则"],
        "source_section": "第 09 讲 · 模块与包",
        "statement_md": (
            "读入 `n` 行「名字 分数」，输出**分数最高**的学生名字。\n\n"
            "**并列时取名字字典序最小的那个。**\n\n"
            "```text\n"
            "alice 90\n"
            "bob 95\n"
            "carol 95\n"
            "→ bob（并列 95，bob < carol）\n"
            "```\n\n"
            "一个 `key` 就把两个规则写清楚：\n\n"
            "```python\n"
            "rows.sort(key=lambda r: (-r[1], r[0]))\n"
            "#                            ↑ 分数降序（取负）   ↑ 名字升序\n"
            "```\n\n"
            "这就是「多关键字排序」的固定套路：**要降序的字段取负号**。"
        ),
        "input_format": "第一行一个整数 `n`；随后 `n` 行，每行 `名字 分数`。",
        "output_format": "一行，名字。",
        "constraints_md": "- 1 ≤ n ≤ 100000\n- 名字由小写字母组成，长度 ≤ 20\n- 0 ≤ 分数 ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "data = sys.stdin.read().split()\n"
            "n = int(data[0])\n"
            "best_name = None\n"
            "best_score = None\n"
            "for i in range(n):\n"
            "    name = data[1 + 2 * i]\n"
            "    score = int(data[2 + 2 * i])\n"
            "    if (best_score is None or score > best_score\n"
            "            or (score == best_score and name < best_name)):\n"
            "        best_name = name\n"
            "        best_score = score\n"
            "print(best_name)\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "data = sys.stdin.read().split()\n"
            "n = int(data[0])\n"
            "rows = [(data[1 + 2 * i], int(data[2 + 2 * i])) for i in range(n)]\n"
            "rows.sort(key=lambda r: (-r[1], r[0]))\n"
            "print(rows[0][0])\n"
        ),
        "cases": [
            {"stdin": "3\nalice 90\nbob 95\ncarol 95\n", "expected_stdout": "bob\n",
             "is_sample": 1, "kind": "sample",
             "explanation": "★ 并列 95，按名字升序 bob 在 carol 前"},
            {"stdin": "2\nzed 100\namy 100\n", "expected_stdout": "amy\n",
             "is_sample": 1, "kind": "sample", "explanation": "输入顺序反过来，答案还是 amy"},
            {"stdin": "1\ntom 60\n", "expected_stdout": "tom\n", "kind": "manual"},
        ],
    },
    # ================================================================== #
    # 第 10 讲 · 面向对象（上）：类 / 属性 / 方法 / 构造
    # ================================================================== #
    {
        "title": "矩形类",
        "line": "python",
        "difficulty": 1,
        "total_score": 10,
        "tags": ["类", "方法", "self", "__init__"],
        "source_section": "第 10 讲 · 面向对象（上）",
        "statement_md": (
            "定义一个 `Rectangle` 类：\n\n"
            "- `__init__(self, w, h)` 接收长和宽\n"
            "- `area()` 返回面积\n"
            "- `perimeter()` 返回周长\n\n"
            "读入长和宽，输出 `面积=xx 周长=xx`。\n\n"
            "**`self` 是什么**：它是「这个对象自己」。"
            "`self.w` 表示「我这个对象的 w 属性」，和别的对象互不干扰。"
            "定义方法时 `self` 必须写在第一个参数位，但**调用时不用传**。"
        ),
        "input_format": "一行，两个整数 `w` 和 `h`。",
        "output_format": "一行，`面积=xx 周长=xx`。",
        "constraints_md": "- 1 ≤ w, h ≤ 100000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "class Rectangle:\n"
            "    def __init__(self, w, h):\n"
            "        self.w = w\n"
            "        self.h = h\n\n"
            "    def area(self):\n"
            "        return self.w * self.h\n\n"
            "    def perimeter(self):\n"
            "        return 2 * (self.w + self.h)\n\n"
            "w, h = map(int, sys.stdin.read().split())\n"
            "r = Rectangle(w, h)\n"
            "print('面积=%d 周长=%d' % (r.area(), r.perimeter()))\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "w, h = map(int, sys.stdin.read().split())\n"
            "print('面积=%d 周长=%d' % (w * h, 2 * (w + h)))\n"
        ),
        "cases": [
            {"stdin": "3 4\n", "expected_stdout": "面积=12 周长=14\n",
             "is_sample": 1, "kind": "sample", "explanation": "3×4=12，2×(3+4)=14"},
            {"stdin": "5 5\n", "expected_stdout": "面积=25 周长=20\n",
             "is_sample": 1, "kind": "sample", "explanation": "正方形"},
            {"stdin": "1 1\n", "expected_stdout": "面积=1 周长=4\n", "kind": "manual"},
        ],
    },
    {
        "title": "对象计数器",
        "line": "python",
        "difficulty": 2,
        "total_score": 15,
        "tags": ["类属性", "实例属性", "★坑", "self vs 类名"],
        "source_section": "第 10 讲 · 面向对象（上）",
        "statement_md": (
            "**类属性和实例属性的区别**，这题就是要让你亲眼看见。\n\n"
            "```python\n"
            "class Item:\n"
            "    total = 0                 # ← 类属性：所有对象共享一份\n"
            "    def __init__(self, idx):\n"
            "        Item.total += 1       # ← 必须写类名（或 type(self)），不能写 self.total\n"
            "        self.idx = idx        # ← 实例属性：每个对象各有一份\n"
            "```\n\n"
            "**★ 关键坑**：如果写成 `self.total += 1`，Python 会理解为"
            "「给**这个实例**新建一个 total 属性」，类属性 `Item.total` 永远停在 0。\n\n"
            "**本题要求**：读入 `n`，创建 `n` 个对象（编号 1 ~ n），"
            "输出 `total=总创建数 last=最后一个对象的编号`。"
        ),
        "input_format": "一行，一个整数 `n`。",
        "output_format": "一行，`total=x last=y`。",
        "constraints_md": "- 0 ≤ n ≤ 100000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "class Item:\n"
            "    total = 0\n\n"
            "    def __init__(self, idx):\n"
            "        Item.total += 1\n"
            "        self.idx = idx\n\n"
            "    @classmethod\n"
            "    def count(cls):\n"
            "        return cls.total\n\n"
            "n = int(sys.stdin.read().strip())\n"
            "last = 0\n"
            "for i in range(1, n + 1):\n"
            "    last = Item(i).idx\n"
            "print('total=%d last=%d' % (Item.count(), last))\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "class Item:\n"
            "    total = 0\n\n"
            "    def __init__(self, idx):\n"
            "        type(self).total += 1\n"
            "        self.idx = idx\n\n"
            "n = int(sys.stdin.read().strip())\n"
            "objs = [Item(i) for i in range(1, n + 1)]\n"
            "print('total=%d last=%d' % (Item.total, objs[-1].idx if objs else 0))\n"
        ),
        "cases": [
            {"stdin": "3\n", "expected_stdout": "total=3 last=3\n", "is_sample": 1,
             "kind": "sample"},
            {"stdin": "5\n", "expected_stdout": "total=5 last=5\n", "is_sample": 1,
             "kind": "sample"},
            {"stdin": "0\n", "expected_stdout": "total=0 last=0\n", "kind": "manual",
             "explanation": "★ 边界：一个对象都没建，两个值都是 0"},
        ],
    },
    {
        "title": "银行账户",
        "line": "python",
        "difficulty": 3,
        "total_score": 20,
        "tags": ["类", "状态修改", "方法", "模拟"],
        "source_section": "第 10 讲 · 面向对象（上）",
        "statement_md": (
            "定义 `Account` 类，模拟一个银行账户。\n\n"
            "**输入**\n\n"
            "```text\n"
            "第一行：owner balance     （户主 初始余额，都是整数）\n"
            "第二行：m                 （操作条数）\n"
            "随后 m 行，每行是下面三种之一：\n"
            "  d 金额     存款\n"
            "  w 金额     取款\n"
            "  q          查询余额\n"
            "```\n\n"
            "**输出**：每个 `q` 输出一行当前余额；没有查询就什么都不输出。\n\n"
            "这题的关键是**对象的状态会被方法改变**：`deposit` 和 `withdraw` "
            "改的是 `self.balance`，所以后面的 `q` 能看到累积效果。"
        ),
        "input_format": "第一行 `owner balance`；第二行 `m`；随后 `m` 行操作。",
        "output_format": "每个 `q` 一行余额；无 `q` 则无输出。",
        "constraints_md": "- 0 ≤ 初始余额 ≤ 100000\n- 0 ≤ 金额 ≤ 100000\n- 1 ≤ m ≤ 100000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "class Account:\n"
            "    def __init__(self, owner, balance):\n"
            "        self.owner = owner\n"
            "        self.balance = balance\n\n"
            "    def deposit(self, v):\n"
            "        self.balance += v\n\n"
            "    def withdraw(self, v):\n"
            "        self.balance -= v\n\n"
            "lines = sys.stdin.read().split('\\n')\n"
            "owner, bal = lines[0].split()\n"
            "acc = Account(owner, int(bal))\n"
            "m = int(lines[1].strip())\n"
            "out = []\n"
            "for i in range(m):\n"
            "    parts = lines[2 + i].split()\n"
            "    if parts[0] == 'd':\n"
            "        acc.deposit(int(parts[1]))\n"
            "    elif parts[0] == 'w':\n"
            "        acc.withdraw(int(parts[1]))\n"
            "    else:\n"
            "        out.append(str(acc.balance))\n"
            "if out:\n"
            "    print('\\n'.join(out))\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "lines = sys.stdin.read().split('\\n')\n"
            "owner, bal = lines[0].split()\n"
            "balance = int(bal)\n"
            "m = int(lines[1].strip())\n"
            "out = []\n"
            "for i in range(m):\n"
            "    parts = lines[2 + i].split()\n"
            "    if parts[0] == 'd':\n"
            "        balance += int(parts[1])\n"
            "    elif parts[0] == 'w':\n"
            "        balance -= int(parts[1])\n"
            "    else:\n"
            "        out.append(str(balance))\n"
            "if out:\n"
            "    print('\\n'.join(out))\n"
        ),
        "cases": [
            {"stdin": "alice 100\n3\nd 50\nw 30\nq\n", "expected_stdout": "120\n",
             "is_sample": 1, "kind": "sample",
             "explanation": "100 + 50 − 30 = 120"},
            {"stdin": "bob 0\n4\nd 200\nw 50\nq\nq\n", "expected_stdout": "150\n150\n",
             "is_sample": 1, "kind": "sample",
             "explanation": "两次查询之间没有操作，所以都是 150"},
            {"stdin": "c 10\n1\nd 5\n", "expected_stdout": "", "kind": "manual",
             "explanation": "★ 没有查询 → 一行都不输出（注意别多打空行）"},
        ],
    },
    {
        "title": "两点距离",
        "line": "python",
        "difficulty": 2,
        "total_score": 15,
        "tags": ["类", "方法参数", "math", "浮点"],
        "source_section": "第 10 讲 · 面向对象（上）",
        "statement_md": (
            "定义 `Point` 类，方法 `dist(other)` 返回和另一个点的**欧氏距离**，"
            "保留 3 位小数。\n\n"
            "```text\n"
            "距离 = √( (x₁-x₂)² + (y₁-y₂)² )\n"
            "```\n\n"
            "读入 4 个数 `x1 y1 x2 y2`，输出 `p1` 到 `p2` 的距离。\n\n"
            "**注意方法参数**：`p1.dist(p2)` 里，`self` 是 `p1`、`other` 是 `p2`，"
            "所以方法里写 `self.x - other.x`。`math.hypot(dx, dy)` 一步到位。"
        ),
        "input_format": "一行，四个整数 `x1 y1 x2 y2`。",
        "output_format": "一行，距离（3 位小数）。",
        "constraints_md": "- 每个坐标的绝对值 ≤ 10^6",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n"
            "import math\n\n"
            "class Point:\n"
            "    def __init__(self, x, y):\n"
            "        self.x = x\n"
            "        self.y = y\n\n"
            "    def dist(self, other):\n"
            "        return math.hypot(self.x - other.x, self.y - other.y)\n\n"
            "data = list(map(float, sys.stdin.read().split()))\n"
            "p1 = Point(data[0], data[1])\n"
            "p2 = Point(data[2], data[3])\n"
            "print('%.3f' % p1.dist(p2))\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "data = list(map(float, sys.stdin.read().split()))\n"
            "dx = data[0] - data[2]\n"
            "dy = data[1] - data[3]\n"
            "print('%.3f' % ((dx * dx + dy * dy) ** 0.5))\n"
        ),
        "cases": [
            {"stdin": "0 0 3 4\n", "expected_stdout": "5.000\n", "is_sample": 1,
             "kind": "sample", "explanation": "经典 3-4-5 直角三角形"},
            {"stdin": "1 1 4 5\n", "expected_stdout": "5.000\n", "is_sample": 1,
             "kind": "sample", "explanation": "dx=3, dy=4，还是 5"},
            {"stdin": "1 2 4 6\n", "expected_stdout": "5.000\n", "kind": "manual"},
            {"stdin": "0 0 0 0\n", "expected_stdout": "0.000\n", "kind": "manual",
             "explanation": "同一个点，距离 0"},
        ],
    },
    {
        "title": "成绩管理器",
        "line": "python",
        "difficulty": 3,
        "total_score": 20,
        "tags": ["类", "对象列表", "聚合", "综合"],
        "source_section": "第 10 讲 · 面向对象（上）",
        "statement_md": (
            "定义两个类：\n\n"
            "- `Student(name, score)` —— 存一个学生的信息\n"
            "- `GradeBook()` —— 管一群学生，有 `add(s)` 加人、"
            "`top()` 找最高分、`average()` 算平均分\n\n"
            "读入 `n` 行「名字 分数」，输出 `最高分学生名 平均分`（平均分 2 位小数）。\n\n"
            "**并列取先出现的那个**（本题保证分数并列时按输入顺序取第一个）。\n\n"
            "这题是「一个类装数据、另一个类管集合」的典型结构 —— "
            "把 `Student` 想成一行记录，`GradeBook` 想成一张表。"
        ),
        "input_format": "第一行一个整数 `n`；随后 `n` 行，每行 `名字 分数`。",
        "output_format": "一行，`名字 平均分`（平均分 2 位小数）。",
        "constraints_md": "- 1 ≤ n ≤ 100000\n- 0 ≤ 分数 ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "class Student:\n"
            "    def __init__(self, name, score):\n"
            "        self.name = name\n"
            "        self.score = score\n\n"
            "class GradeBook:\n"
            "    def __init__(self):\n"
            "        self.students = []\n\n"
            "    def add(self, s):\n"
            "        self.students.append(s)\n\n"
            "    def top(self):\n"
            "        best = self.students[0]\n"
            "        for s in self.students:\n"
            "            if s.score > best.score:\n"
            "                best = s\n"
            "        return best\n\n"
            "    def average(self):\n"
            "        return sum(s.score for s in self.students) / len(self.students)\n\n"
            "data = sys.stdin.read().split()\n"
            "n = int(data[0])\n"
            "gb = GradeBook()\n"
            "for i in range(n):\n"
            "    gb.add(Student(data[1 + 2 * i], int(data[2 + 2 * i])))\n"
            "print('%s %.2f' % (gb.top().name, gb.average()))\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "data = sys.stdin.read().split()\n"
            "n = int(data[0])\n"
            "rows = [(data[1 + 2 * i], int(data[2 + 2 * i])) for i in range(n)]\n"
            "best = rows[0]\n"
            "for r in rows:\n"
            "    if r[1] > best[1]:\n"
            "        best = r\n"
            "print('%s %.2f' % (best[0], sum(r[1] for r in rows) / n))\n"
        ),
        "cases": [
            {"stdin": "3\nalice 90\nbob 80\ncarol 100\n",
             "expected_stdout": "carol 90.00\n", "is_sample": 1, "kind": "sample",
             "explanation": "(90+80+100)/3 = 90.00"},
            {"stdin": "2\nx 60\ny 60\n", "expected_stdout": "x 60.00\n",
             "is_sample": 1, "kind": "sample",
             "explanation": "★ 并列 60 → 取先出现的 x"},
            {"stdin": "1\na 0\n", "expected_stdout": "a 0.00\n", "kind": "manual"},
        ],
    },
    # ================================================================== #
    # 第 11 讲 · 面向对象（下）：继承 / 多态 / 魔法方法
    # ================================================================== #
    {
        "title": "形状面积（继承）",
        "line": "python",
        "difficulty": 3,
        "total_score": 20,
        "tags": ["继承", "方法重写", "多态"],
        "source_section": "第 11 讲 · 面向对象（下）",
        "statement_md": (
            "定义基类 `Shape`，以及两个子类：\n\n"
            "- `Circle(r)` —— 面积 `3.14 × r²`\n"
            "- `Rect(w, h)` —— 面积 `w × h`\n\n"
            "两者都实现 `area()` 方法。\n\n"
            "读入 `n` 行形状描述（`circle r` 或 `rect w h`），**每行输出对应面积**（2 位小数）。\n\n"
            "**继承的意义**：`Shape` 定义了「所有形状都有 `area()` 这个方法」，"
            "子类各自**重写**（override）成自己的算法。"
            "调用方只管写 `s.area()`，不用管 `s` 到底是圆还是矩形 —— 这就是**多态**。\n\n"
            "本题 π 取 **3.14**（和前面圆面积题保持一致，别用 `math.pi`）。"
        ),
        "input_format": "第一行一个整数 `n`；随后 `n` 行，每行 `circle r` 或 `rect w h`。",
        "output_format": "`n` 行，每行一个面积（2 位小数）。",
        "constraints_md": "- 1 ≤ n ≤ 100000\n- 0 ≤ 边长/半径 ≤ 10000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "class Shape:\n"
            "    def area(self):\n"
            "        raise NotImplementedError\n\n"
            "class Circle(Shape):\n"
            "    def __init__(self, r):\n"
            "        self.r = r\n\n"
            "    def area(self):\n"
            "        return 3.14 * self.r ** 2\n\n"
            "class Rect(Shape):\n"
            "    def __init__(self, w, h):\n"
            "        self.w = w\n"
            "        self.h = h\n\n"
            "    def area(self):\n"
            "        return self.w * self.h\n\n"
            "lines = sys.stdin.read().split('\\n')\n"
            "n = int(lines[0].strip())\n"
            "out = []\n"
            "for i in range(n):\n"
            "    p = lines[1 + i].split()\n"
            "    if p[0] == 'circle':\n"
            "        s = Circle(float(p[1]))\n"
            "    else:\n"
            "        s = Rect(float(p[1]), float(p[2]))\n"
            "    out.append('%.2f' % s.area())\n"
            "print('\\n'.join(out))\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "lines = sys.stdin.read().split('\\n')\n"
            "n = int(lines[0].strip())\n"
            "out = []\n"
            "for i in range(n):\n"
            "    p = lines[1 + i].split()\n"
            "    if p[0] == 'circle':\n"
            "        a = 3.14 * float(p[1]) ** 2\n"
            "    else:\n"
            "        a = float(p[1]) * float(p[2])\n"
            "    out.append('%.2f' % a)\n"
            "print('\\n'.join(out))\n"
        ),
        "cases": [
            {"stdin": "2\ncircle 2\nrect 3 4\n", "expected_stdout": "12.56\n12.00\n",
             "is_sample": 1, "kind": "sample",
             "explanation": "3.14 × 4 = 12.56；3 × 4 = 12"},
            {"stdin": "1\ncircle 1\n", "expected_stdout": "3.14\n", "is_sample": 1,
             "kind": "sample"},
            {"stdin": "2\nrect 1 1\ncircle 10\n",
             "expected_stdout": "1.00\n314.00\n", "kind": "manual"},
        ],
    },
    {
        "title": "动物叫声（多态）",
        "line": "python",
        "difficulty": 2,
        "total_score": 15,
        "tags": ["继承", "多态", "方法重写"],
        "source_section": "第 11 讲 · 面向对象（下）",
        "statement_md": (
            "定义基类 `Animal` 和子类 `Dog`、`Cat`，各自实现 `sound()` 方法：\n\n"
            "- `Dog.sound()` 返回 `woof`\n"
            "- `Cat.sound()` 返回 `meow`\n\n"
            "读入 `n` 行「动物名 次数」，对每一行输出该叫声**重复对应次数**"
            "（用**一个空格**分隔）。\n\n"
            "```text\n"
            "dog 2  →  woof woof\n"
            "cat 3  →  meow meow meow\n"
            "```\n\n"
            "**多态的写法**：主循环里只写 `a.sound()`，不写 `if 是狗…elif 是猫…`。"
            "以后再加 `Cow`，主循环**一行都不用改** —— 这就是继承 + 多态的价值。"
        ),
        "input_format": "第一行一个整数 `n`；随后 `n` 行，每行 `动物名 次数`（动物名是 `dog` 或 `cat`）。",
        "output_format": "`n` 行，每行是重复的叫声。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 1 ≤ 次数 ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "class Animal:\n"
            "    def sound(self):\n"
            "        return ''\n\n"
            "class Dog(Animal):\n"
            "    def sound(self):\n"
            "        return 'woof'\n\n"
            "class Cat(Animal):\n"
            "    def sound(self):\n"
            "        return 'meow'\n\n"
            "KINDS = {'dog': Dog, 'cat': Cat}\n\n"
            "lines = sys.stdin.read().split('\\n')\n"
            "n = int(lines[0].strip())\n"
            "out = []\n"
            "for i in range(n):\n"
            "    kind, cnt = lines[1 + i].split()\n"
            "    a = KINDS[kind]()\n"
            "    out.append(' '.join([a.sound()] * int(cnt)))\n"
            "print('\\n'.join(out))\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "SOUND = {'dog': 'woof', 'cat': 'meow'}\n\n"
            "lines = sys.stdin.read().split('\\n')\n"
            "n = int(lines[0].strip())\n"
            "out = []\n"
            "for i in range(n):\n"
            "    kind, cnt = lines[1 + i].split()\n"
            "    out.append(' '.join([SOUND[kind]] * int(cnt)))\n"
            "print('\\n'.join(out))\n"
        ),
        "cases": [
            {"stdin": "2\ndog 2\ncat 3\n", "expected_stdout": "woof woof\nmeow meow meow\n",
             "is_sample": 1, "kind": "sample"},
            {"stdin": "1\ncat 1\n", "expected_stdout": "meow\n", "is_sample": 1,
             "kind": "sample", "explanation": "次数为 1，不带空格"},
        ],
    },
    {
        "title": "初始化顺序（super）",
        "line": "python",
        "difficulty": 3,
        "total_score": 20,
        "tags": ["继承链", "super", "MRO", "★坑"],
        "source_section": "第 11 讲 · 面向对象（下）",
        "statement_md": (
            "三层继承链：`C` 继承 `B`，`B` 继承 `A`。\n\n"
            "每个类的 `__init__` 先调 `super().__init__()` 再把自己的名字追加到 "
            "`self.trace` 列表。\n\n"
            "```python\n"
            "class B(A):\n"
            "    def __init__(self):\n"
            "        super().__init__()        # ← 先去初始化父类\n"
            "        self.trace.append('B')    # ← 再记自己\n"
            "```\n\n"
            "读入 `n`（1 ~ 3），创建对应的那一层对象，输出 `trace` 里的内容"
            "（空格分隔）。\n\n"
            "**`super()` 到底是什么**：它不是「父类」的字面意思，"
            "而是「**MRO 里的下一个类**」。"
            "所以 `super().__init__()` 会顺着继承链一路往上跑，"
            "最终得到 `A B C` 这样的顺序。"
        ),
        "input_format": "一行，一个整数 `n`（1 = A，2 = B，3 = C）。",
        "output_format": "一行，空格分隔的初始化顺序。",
        "constraints_md": "- 1 ≤ n ≤ 3",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "class A:\n"
            "    def __init__(self):\n"
            "        self.trace = ['A']\n\n"
            "class B(A):\n"
            "    def __init__(self):\n"
            "        super().__init__()\n"
            "        self.trace.append('B')\n\n"
            "class C(B):\n"
            "    def __init__(self):\n"
            "        super().__init__()\n"
            "        self.trace.append('C')\n\n"
            "n = int(sys.stdin.read().strip())\n"
            "obj = {1: A, 2: B, 3: C}[n]()\n"
            "print(' '.join(obj.trace))\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "n = int(sys.stdin.read().strip())\n"
            "print(' '.join(['A', 'B', 'C'][:n]))\n"
        ),
        "cases": [
            {"stdin": "1\n", "expected_stdout": "A\n", "is_sample": 1,
             "kind": "sample", "explanation": "A 没有父类，只记自己"},
            {"stdin": "2\n", "expected_stdout": "A B\n", "is_sample": 1,
             "kind": "sample", "explanation": "B 先跑到 A，再记 B"},
            {"stdin": "3\n", "expected_stdout": "A B C\n", "kind": "manual",
             "explanation": "★ 一路 super 上去，顺序是 A → B → C（跟字面直觉反着来）"},
        ],
    },
    {
        "title": "点的排序",
        "line": "python",
        "difficulty": 3,
        "total_score": 20,
        "tags": ["魔法方法", "__lt__", "排序", "自定义比较"],
        "source_section": "第 11 讲 · 面向对象（下）",
        "statement_md": (
            "定义 `Point` 类，实现 `__lt__` 方法，让点之间可以**直接比大小**，"
            "规则是「先比 `x`，`x` 相同再比 `y`」。\n\n"
            "```python\n"
            "def __lt__(self, other):\n"
            "    return (self.x, self.y) < (other.x, other.y)\n"
            "```\n\n"
            "读入 `n` 个点，**按升序排序后**输出，每行一个点（`x y`）。\n\n"
            "**为什么要有 `__lt__`**：`sorted()` 和 `.sort()` 靠的就是 `<` 运算符。"
            "自定义类默认不支持和 `<` 比较，实现 `__lt__` 后就能直接丢给 "
            "`sorted()` 用了 —— 这叫**运算符重载**。\n\n"
            "*（也可以用 `sorted(pts, key=lambda p: (p.x, p.y))` 绕过，"
            "但那不算「让对象自己会排序」。）*"
        ),
        "input_format": "第一行一个整数 `n`；随后 `n` 行，每行两个整数 `x y`。",
        "output_format": "`n` 行，排序后的点，每行 `x y`。",
        "constraints_md": "- 1 ≤ n ≤ 100000\n- 坐标绝对值 ≤ 10^9",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "class Point:\n"
            "    def __init__(self, x, y):\n"
            "        self.x = x\n"
            "        self.y = y\n\n"
            "    def __lt__(self, other):\n"
            "        return (self.x, self.y) < (other.x, other.y)\n\n"
            "    def __repr__(self):\n"
            "        return '%d %d' % (self.x, self.y)\n\n"
            "lines = sys.stdin.read().split('\\n')\n"
            "n = int(lines[0].strip())\n"
            "pts = []\n"
            "for i in range(n):\n"
            "    x, y = map(int, lines[1 + i].split())\n"
            "    pts.append(Point(x, y))\n"
            "for p in sorted(pts):\n"
            "    print(p)\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "lines = sys.stdin.read().split('\\n')\n"
            "n = int(lines[0].strip())\n"
            "rows = sorted(tuple(map(int, lines[1 + i].split())) for i in range(n))\n"
            "for r in rows:\n"
            "    print(r[0], r[1])\n"
        ),
        "cases": [
            {"stdin": "3\n3 1\n1 2\n1 1\n", "expected_stdout": "1 1\n1 2\n3 1\n",
             "is_sample": 1, "kind": "sample",
             "explanation": "x 都为 1 时，y 小的在前"},
            {"stdin": "4\n5 5\n1 1\n5 1\n1 5\n",
             "expected_stdout": "1 1\n1 5\n5 1\n5 5\n", "is_sample": 1,
             "kind": "sample", "explanation": "★ 输入顺序完全打乱，输出必须有序"},
            {"stdin": "2\n0 0\n0 0\n", "expected_stdout": "0 0\n0 0\n",
             "kind": "manual", "explanation": "两个完全相同的点"},
        ],
    },
    {
        "title": "向量相加",
        "line": "python",
        "difficulty": 3,
        "total_score": 20,
        "tags": ["魔法方法", "__add__", "运算符重载"],
        "source_section": "第 11 讲 · 面向对象（下）",
        "statement_md": (
            "定义 `Vector2D` 类，实现 `__add__`，让两个向量能**直接用 `+` 相加**：\n\n"
            "```python\n"
            "def __add__(self, other):\n"
            "    return Vector2D(self.x + other.x, self.y + other.y)\n"
            "```\n\n"
            "顺便实现 `__str__`，让 `print(v)` 输出 `x y`。\n\n"
            "读入两行，每行两个整数（两个向量），输出它们的和。\n\n"
            "**运算符重载的意义**：`a + b` 本质上是 `a.__add__(b)`。"
            "给自定义类实现 `__add__` 之后，`+` 就有意义了，写出来跟数学公式一模一样。"
        ),
        "input_format": "两行，每行两个整数 `x y`。",
        "output_format": "一行，`x y`（两个向量的和）。",
        "constraints_md": "- 每个分量的绝对值 ≤ 10^9",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "class Vector2D:\n"
            "    def __init__(self, x, y):\n"
            "        self.x = x\n"
            "        self.y = y\n\n"
            "    def __add__(self, other):\n"
            "        return Vector2D(self.x + other.x, self.y + other.y)\n\n"
            "    def __str__(self):\n"
            "        return '%d %d' % (self.x, self.y)\n\n"
            "data = sys.stdin.read().split()\n"
            "a = Vector2D(int(data[0]), int(data[1]))\n"
            "b = Vector2D(int(data[2]), int(data[3]))\n"
            "print(a + b)\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "data = sys.stdin.read().split()\n"
            "x1, y1, x2, y2 = (int(v) for v in data[:4])\n"
            "print('%d %d' % (x1 + x2, y1 + y2))\n"
        ),
        "cases": [
            {"stdin": "1 2\n3 4\n", "expected_stdout": "4 6\n", "is_sample": 1,
             "kind": "sample"},
            {"stdin": "-1 2\n1 -2\n", "expected_stdout": "0 0\n", "is_sample": 1,
             "kind": "sample", "explanation": "相反向量，和为零向量"},
            {"stdin": "0 0\n0 0\n", "expected_stdout": "0 0\n", "kind": "manual"},
        ],
    },
    {
        "title": "年龄校验",
        "line": "python",
        "difficulty": 3,
        "total_score": 20,
        "tags": ["property", "setter", "封装", "异常"],
        "source_section": "第 11 讲 · 面向对象（下）",
        "statement_md": (
            "用 `@property` + `@age.setter` 给年龄加一道**校验关卡**：\n\n"
            "```python\n"
            "class Person:\n"
            "    @property\n"
            "    def age(self):\n"
            "        return self._age\n\n"
            "    @age.setter\n"
            "    def age(self, v):\n"
            "        if v < 0 or v > 150:\n"
            "            raise ValueError('bad age')\n"
            "        self._age = v\n"
            "```\n\n"
            "读入一个整数年龄。合法（0 ≤ 年龄 ≤ 150）就输出年龄；"
            "否则输出 `invalid`。\n\n"
            "**为什么不能直接写 `self.age = v`**：那样赋值时会**无限递归** —— "
            "setter 里再调 setter。所以真正存值用的是另一个名字 `_age`。\n\n"
            "**property 的价值**：外部代码写起来还是 `p.age = 25`（像普通属性），"
            "但赋值时会自动过校验，**用法不变、安全性提高**。"
        ),
        "input_format": "一行，一个整数。",
        "output_format": "一行，合法的年龄或 `invalid`。",
        "constraints_md": "- -10^9 ≤ 输入 ≤ 10^9",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "class Person:\n"
            "    def __init__(self):\n"
            "        self._age = 0\n\n"
            "    @property\n"
            "    def age(self):\n"
            "        return self._age\n\n"
            "    @age.setter\n"
            "    def age(self, v):\n"
            "        if v < 0 or v > 150:\n"
            "            raise ValueError('bad age')\n"
            "        self._age = v\n\n"
            "n = int(sys.stdin.read().strip())\n"
            "p = Person()\n"
            "try:\n"
            "    p.age = n\n"
            "    print(p.age)\n"
            "except ValueError:\n"
            "    print('invalid')\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "n = int(sys.stdin.read().strip())\n"
            "print('invalid' if (n < 0 or n > 150) else n)\n"
        ),
        "cases": [
            {"stdin": "25\n", "expected_stdout": "25\n", "is_sample": 1,
             "kind": "sample"},
            {"stdin": "-1\n", "expected_stdout": "invalid\n", "is_sample": 1,
             "kind": "sample", "explanation": "负数被 setter 拦下"},
            {"stdin": "0\n", "expected_stdout": "0\n", "kind": "manual",
             "explanation": "★ 下边界 0 是合法的"},
            {"stdin": "150\n", "expected_stdout": "150\n", "kind": "manual",
             "explanation": "★ 上边界 150 是合法的"},
            {"stdin": "200\n", "expected_stdout": "invalid\n", "kind": "manual"},
        ],
    },
    {
        "title": "形状总面积（多态）",
        "line": "python",
        "difficulty": 3,
        "total_score": 20,
        "tags": ["多态", "对象列表", "综合", "聚合"],
        "source_section": "第 11 讲 · 面向对象（下）",
        "statement_md": (
            "在「形状面积（继承）」的基础上再往前走一步：\n\n"
            "读入 `n` 个形状，把它们**都放进同一个列表**，"
            "然后遍历这个列表求**总面积**（2 位小数）。\n\n"
            "```python\n"
            "shapes = []\n"
            "shapes.append(Circle(1))\n"
            "shapes.append(Rect(2, 3))\n"
            "total = sum(s.area() for s in shapes)   # ← 不用管 s 是什么类型\n"
            "```\n\n"
            "**这就是多态真正的用处**：列表里混着不同类型，"
            "但循环体一句 `s.area()` 就够了 —— "
            "因为每个对象都「知道自己该怎么算面积」。\n\n"
            "本题 π 取 **3.14**。"
        ),
        "input_format": "第一行一个整数 `n`；随后 `n` 行，每行 `circle r` 或 `rect w h`。",
        "output_format": "一行，总面积（2 位小数）。",
        "constraints_md": "- 1 ≤ n ≤ 100000\n- 0 ≤ 边长/半径 ≤ 10000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "class Shape:\n"
            "    def area(self):\n"
            "        raise NotImplementedError\n\n"
            "class Circle(Shape):\n"
            "    def __init__(self, r):\n"
            "        self.r = r\n\n"
            "    def area(self):\n"
            "        return 3.14 * self.r ** 2\n\n"
            "class Rect(Shape):\n"
            "    def __init__(self, w, h):\n"
            "        self.w = w\n"
            "        self.h = h\n\n"
            "    def area(self):\n"
            "        return self.w * self.h\n\n"
            "lines = sys.stdin.read().split('\\n')\n"
            "n = int(lines[0].strip())\n"
            "shapes = []\n"
            "for i in range(n):\n"
            "    p = lines[1 + i].split()\n"
            "    if p[0] == 'circle':\n"
            "        shapes.append(Circle(float(p[1])))\n"
            "    else:\n"
            "        shapes.append(Rect(float(p[1]), float(p[2])))\n"
            "total = 0.0\n"
            "for s in shapes:\n"
            "    total += s.area()\n"
            "print('%.2f' % total)\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "lines = sys.stdin.read().split('\\n')\n"
            "n = int(lines[0].strip())\n"
            "total = 0.0\n"
            "for i in range(n):\n"
            "    p = lines[1 + i].split()\n"
            "    if p[0] == 'circle':\n"
            "        total += 3.14 * float(p[1]) ** 2\n"
            "    else:\n"
            "        total += float(p[1]) * float(p[2])\n"
            "print('%.2f' % total)\n"
        ),
        "cases": [
            {"stdin": "2\ncircle 1\nrect 2 3\n", "expected_stdout": "9.14\n",
             "is_sample": 1, "kind": "sample", "explanation": "3.14 + 6 = 9.14"},
            {"stdin": "1\ncircle 2\n", "expected_stdout": "12.56\n", "is_sample": 1,
             "kind": "sample"},
            {"stdin": "3\nrect 1 1\nrect 2 2\ncircle 0\n",
             "expected_stdout": "5.00\n", "kind": "manual",
             "explanation": "1 + 4 + 0 = 5；半径 0 的圆面积是 0"},
        ],
    },
]
