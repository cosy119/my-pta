# -*- coding: utf-8 -*-
"""题库扩展（第四批）：二进制统计族（bincount）。

与 `problems_bank_ext2.py` 同一套约定：

1. **顺序跟讲义走** —— 挂在「第 02 讲 · 编程基础」（bin()/位运算 5.5 节），
   是 2026-10-20 用户点名的题型：「读一个数 → 转二进制去前缀 → 统计 1 和 0」
2. **期望输出独立算** —— 全部 `expected_stdout` 由 **node 独立实现**预先算出
   （`data/_oracle_py_bits.js`，手写除 2 取余，不走 toString(2)），
   参考解只负责「撞」它，对不上就不入库
3. **每题带 `alt_solution`** —— 参考解与第二套实现都要通过全部测试点
"""
from __future__ import annotations

PY_BITS_PROBLEMS: list[dict] = [
    {
        "title": "统计二进制里 1 和 0 的个数",
        "line": "python",
        "question_type": "programming",
        "difficulty": 1,
        "total_score": 10,
        "tags": ["进制转换", "二进制", "bin"],
        "source_section": "第 02 讲 · 编程基础",
        "statement_md": (
            "读入一个**非负整数** `x`，把它转成二进制（去掉 `0b` 前缀），"
            "分别统计里面 `1` 和 `0` 的个数。\n\n"
            "考点就一串：`bin(x)` 返回带 `0b` 前缀的**字符串** → 切片 `[2:]` 去前缀 → "
            "`str.count()` 计数。注意 `x = 0` 时二进制就是 `\"0\"`，0 的个数是 1 不是 0。"
        ),
        "input_format": "一行一个非负整数 `x`（0 ≤ x ≤ 10^9）。",
        "output_format": "一行：`1 的个数 0 的个数`，用空格分隔。",
        "constraints_md": "- 0 ≤ x ≤ 10^9",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "x = int(input())\n"
            "# 转换为二进制并去掉前缀 '0b'\n"
            "b_str = bin(x)[2:]\n"
            "# 统计 1 和 0 的个数\n"
            "ones = b_str.count('1')\n"
            "zeros = b_str.count('0')\n"
            "# 输出结果，中间用空格隔开\n"
            "print(f\"{ones} {zeros}\")\n"
        ),
        "alt_solution": (
            "# 第二套：手写除 2 取余，不走 bin()（算术实现，与字符串实现互为独立）\n"
            "x = int(input())\n"
            "ones = zeros = 0\n"
            "if x == 0:\n"
            "    zeros = 1            # 0 的二进制是 \"0\"，含一个 0\n"
            "while x > 0:\n"
            "    if x % 2:\n"
            "        ones += 1\n"
            "    else:\n"
            "        zeros += 1\n"
            "    x //= 2\n"
            "print(ones, zeros)\n"
        ),
        "cases": [
            {"stdin": "5\n", "expected_stdout": "2 1\n", "is_sample": 1,
             "kind": "sample", "explanation": "5 = 0b101：两个 1，一个 0"},
            {"stdin": "0\n", "expected_stdout": "0 1\n", "kind": "manual",
             "explanation": "0 = 0b0：1 的个数 0、0 的个数 1——别把 x=0 当成空串"},
            {"stdin": "255\n", "expected_stdout": "8 0\n", "kind": "manual",
             "explanation": "255 = 0b11111111：8 个 1，0 个 0"},
            {"stdin": "10\n", "expected_stdout": "2 2\n", "kind": "manual",
             "explanation": "10 = 0b1010：各两个"},
            {"stdin": "1000000000\n", "expected_stdout": "13 17\n", "kind": "manual",
             "explanation": "10^9 = 0b111011100110101100101000000000：30 位，13 个 1、17 个 0"},
        ],
    },
    {
        "title": "八位二进制补零输出",
        "line": "python",
        "question_type": "programming",
        "difficulty": 1,
        "total_score": 10,
        "tags": ["进制转换", "二进制", "格式化"],
        "source_section": "第 02 讲 · 编程基础",
        "statement_md": (
            "读入一个非负整数 `x`（0 ≤ x < 256），输出它的 **8 位**二进制表示——"
            "不足 8 位在**左边补零**。\n\n"
            "两条路都行：格式化 `f\"{x:08b}\"`（宽度 8 补零，不带前缀），"
            "或者 `bin(x)[2:]` 之后 `zfill(8)` 补齐。"
            "上一题的 `bin(x)[2:]` 在这题会掉前导零，这正是它俩的差别。"
        ),
        "input_format": "一行一个非负整数 `x`（0 ≤ x < 256）。",
        "output_format": "一行：8 位二进制串（含前导零）。",
        "constraints_md": "- 0 ≤ x < 256",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "x = int(input())\n"
            "print(f\"{x:08b}\")      # 宽度 8、补零、二进制不带前缀\n"
        ),
        "alt_solution": (
            "# 第二套：bin 切片 + zfill 补零（与格式化互为独立）\n"
            "x = int(input())\n"
            "print(bin(x)[2:].zfill(8))\n"
        ),
        "cases": [
            {"stdin": "5\n", "expected_stdout": "00000101\n", "is_sample": 1,
             "kind": "sample", "explanation": "5 = 101，左边补 5 个零到 8 位"},
            {"stdin": "0\n", "expected_stdout": "00000000\n", "kind": "manual",
             "explanation": "0 也要输出满 8 个零"},
            {"stdin": "255\n", "expected_stdout": "11111111\n", "kind": "manual",
             "explanation": "255 刚好 8 位，不用补"},
            {"stdin": "128\n", "expected_stdout": "10000000\n", "kind": "manual",
             "explanation": "128 = 2^7，最高位是 1 后面全是 0"},
            {"stdin": "200\n", "expected_stdout": "11001000\n", "kind": "manual",
             "explanation": "200 = 128+64+8 = 0b11001000"},
        ],
    },
    {
        "title": "谁的二进制 1 最多",
        "line": "python",
        "question_type": "programming",
        "difficulty": 2,
        "total_score": 12,
        "tags": ["进制转换", "二进制", "bit_count"],
        "source_section": "第 02 讲 · 编程基础",
        "statement_md": (
            "第一行读入 `n`，第二行读入 `n` 个非负整数。"
            "输出其中**二进制表示里 1 的个数最多**的那个数。\n\n"
            "若并列（多个数 1 的个数相同），输出**最前面**的那个。\n\n"
            "套路：对每个数 `bin(v)[2:].count('1')`（或 3.10+ 直接 `v.bit_count()`），"
            "边读边比，**严格大于**才更新——并列时保持先来的。"
        ),
        "input_format": (
            "第一行一个整数 `n`（1 ≤ n ≤ 1000）；\n"
            "第二行 `n` 个非负整数（每个 0 ≤ x < 2^31），空格分隔。"
        ),
        "output_format": "一行：1 的个数最多的那个数（并列取最前）。",
        "constraints_md": "- 1 ≤ n ≤ 1000，0 ≤ x < 2^31",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "data = sys.stdin.read().split()\n"
            "n = int(data[0])\n"
            "nums = list(map(int, data[1:1 + n]))\n"
            "best, best_cnt = nums[0], bin(nums[0]).count('1')\n"
            "for v in nums[1:]:\n"
            "    c = bin(v).count('1')\n"
            "    if c > best_cnt:          # 严格大于：并列时保留最前面的\n"
            "        best, best_cnt = v, c\n"
            "print(best)\n"
        ),
        "alt_solution": (
            "# 第二套：max + bit_count（max 对并列键返回最靠前的，语义正好）\n"
            "import sys\n\n"
            "data = sys.stdin.read().split()\n"
            "n = int(data[0])\n"
            "nums = list(map(int, data[1:1 + n]))\n"
            "print(max(nums, key=int.bit_count))\n"
        ),
        "cases": [
            {"stdin": "5\n1 2 3 4 7\n", "expected_stdout": "7\n", "is_sample": 1,
             "kind": "sample", "explanation": "7 = 0b111 有 3 个 1，全场最多"},
            {"stdin": "3\n5 6 3\n", "expected_stdout": "5\n", "kind": "manual",
             "explanation": "5=0b101 与 6=0b110 都是 2 个 1，3 也是 2 个——三并列，取最前的 5"},
            {"stdin": "4\n0 0 8 0\n", "expected_stdout": "8\n", "kind": "manual",
             "explanation": "8 = 0b1000 有 1 个 1，其余全是 0"},
            {"stdin": "1\n0\n", "expected_stdout": "0\n", "kind": "manual",
             "explanation": "只有一个 0：1 的个数都是 0，它自己就是答案"},
            {"stdin": "6\n1023 512 511 256 510 495\n", "expected_stdout": "1023\n",
             "kind": "manual", "explanation": "1023 = 0b1111111111 有 10 个 1，碾压全场"},
        ],
    },
    {
        "title": "汉明距离",
        "line": "python",
        "question_type": "programming",
        "difficulty": 1,
        "total_score": 10,
        "tags": ["进制转换", "位运算", "异或"],
        "source_section": "第 02 讲 · 编程基础",
        "statement_md": (
            "读入两个非负整数 `x` 和 `y`，输出它们的**汉明距离**——"
            "二进制表示里对应位不同的位置个数。\n\n"
            "标准姿势一行完事：`x ^ y` 把「不同的位」全变成 1（相同为 0、不同为 1），"
            "再 `bin(...)[2:].count('1')`（或 3.10+ `(...).bit_count()`）数 1 的个数。"
            "上一题的「数 1」套路直接复用，核心新考点是**异或的语义**。"
        ),
        "input_format": "一行两个非负整数 `x y`（0 ≤ x, y < 2^30），空格分隔。",
        "output_format": "一行：汉明距离。",
        "constraints_md": "- 0 ≤ x, y < 2^30",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "x, y = map(int, input().split())\n"
            "print(bin(x ^ y).count('1'))    # 异或：同 0 异 1，数 1 即距离\n"
        ),
        "alt_solution": (
            "# 第二套：手写按位比较，不用异或运算符\n"
            "x, y = map(int, input().split())\n"
            "cnt = 0\n"
            "while x > 0 or y > 0:\n"
            "    if x % 2 != y % 2:          # 末位不同就计 1\n"
            "        cnt += 1\n"
            "    x //= 2\n"
            "    y //= 2\n"
            "print(cnt)\n"
        ),
        "cases": [
            {"stdin": "1 4\n", "expected_stdout": "2\n", "is_sample": 1,
             "kind": "sample", "explanation": "001 vs 100：第 0、2 位不同，距离 2"},
            {"stdin": "0 0\n", "expected_stdout": "0\n", "kind": "manual",
             "explanation": "全同，距离 0"},
            {"stdin": "5 3\n", "expected_stdout": "2\n", "kind": "manual",
             "explanation": "101 ^ 011 = 110，两个 1 → 距离 2"},
            {"stdin": "255 0\n", "expected_stdout": "8\n", "kind": "manual",
             "explanation": "8 个 1 对 8 个 0，每位都不同"},
            {"stdin": "1073741823 123456789\n", "expected_stdout": "14\n", "kind": "manual",
             "explanation": "2^30-1（30 个 1）与 123456789 的汉明距离：30 − 16 = 14"},
        ],
    },
    {
        "title": "位运算三兄弟",
        "line": "python",
        "question_type": "programming",
        "difficulty": 2,
        "total_score": 12,
        "tags": ["位运算", "异或", "与或"],
        "source_section": "第 02 讲 · 编程基础",
        "statement_md": (
            "读入两个非负整数 `x` 和 `y`，按顺序输出三行：\n\n"
            "1. `x & y`（按位与：两位都是 1 才是 1）\n"
            "2. `x | y`（按位或：至少一位是 1 就是 1）\n"
            "3. `x ^ y`（按位异或：两位不同才是 1）\n\n"
            "对应讲义第 02 讲 5.5 的位运算表，用真实数字把三个运算符的语义过一遍。"
        ),
        "input_format": "一行两个非负整数 `x y`（0 ≤ x, y < 2^30），空格分隔。",
        "output_format": "三行：`x & y`、`x | y`、`x ^ y`（十进制）。",
        "constraints_md": "- 0 ≤ x, y < 2^30",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "x, y = map(int, input().split())\n"
            "print(x & y)\n"
            "print(x | y)\n"
            "print(x ^ y)\n"
        ),
        "alt_solution": (
            "# 第二套：恒等式 x + y = (x^y) + 2*(x&y)，用加法反推三兄弟\n"
            "x, y = map(int, input().split())\n"
            "a = x & y\n"
            "print(a)                    # 与\n"
            "print(x + y - a)            # 或 = x + y - 与\n"
            "print(x + y - 2 * a)        # 异或 = x + y - 2*与\n"
        ),
        "cases": [
            {"stdin": "5 3\n", "expected_stdout": "1\n7\n6\n", "is_sample": 1,
             "kind": "sample", "explanation": "101 与 011：与=001，或=111，异或=110"},
            {"stdin": "0 0\n", "expected_stdout": "0\n0\n0\n", "kind": "manual",
             "explanation": "全零输入三个 0"},
            {"stdin": "255 170\n", "expected_stdout": "170\n255\n85\n", "kind": "manual",
             "explanation": "11111111 掩码：与=170，或=255，异或=85（恰好是差集位）"},
            {"stdin": "12 10\n", "expected_stdout": "8\n14\n6\n", "kind": "manual",
             "explanation": "1100 与 1010：与=1000，或=1110，异或=0110"},
            {"stdin": "1024 1024\n", "expected_stdout": "1024\n1024\n0\n", "kind": "manual",
             "explanation": "自己跟自己：与=或=自己，异或=0（x^x=0 的直接体现）"},
        ],
    },
    {
        "title": "只出现一次的数",
        "line": "python",
        "question_type": "programming",
        "difficulty": 3,
        "total_score": 12,
        "tags": ["位运算", "异或", "技巧"],
        "source_section": "第 02 讲 · 编程基础",
        "statement_md": (
            "第一行读入 `n`，第二行读入 `n` 个非负整数——**其中恰好有一个数只出现一次，"
            "其余每个数都恰好出现两次**。输出那个只出现一次的数。\n\n"
            "★ 异或的杀手锏：`x ^ x = 0`、`x ^ 0 = x`，且异或满足交换律结合律——"
            "把全部数**连异或**一遍，成对的互相抵消成 0，最后剩下的就是落单的那个。"
            "一遍扫描、O(1) 额外空间，不用哈希表也不用排序。"
        ),
        "input_format": (
            "第一行一个整数 `n`（1 ≤ n ≤ 10^5，n 为奇数）；\n"
            "第二行 `n` 个非负整数（每个 0 ≤ x < 2^30），空格分隔。"
        ),
        "output_format": "一行：只出现一次的那个数。",
        "constraints_md": "- n 为奇数，恰有一个数出现一次，其余各出现两次",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "data = sys.stdin.read().split()\n"
            "n = int(data[0])\n"
            "acc = 0\n"
            "for i in range(1, n + 1):\n"
            "    acc ^= int(data[i])         # 成对抵消，落单的留下来\n"
            "print(acc)\n"
        ),
        "alt_solution": (
            "# 第二套：计数表（与异或折叠不同算法，互为对拍）\n"
            "import sys\n"
            "from collections import Counter\n\n"
            "data = sys.stdin.read().split()\n"
            "n = int(data[0])\n"
            "cnt = Counter(map(int, data[1:1 + n]))\n"
            "print(next(v for v, c in cnt.items() if c == 1))\n"
        ),
        "cases": [
            {"stdin": "5\n1 2 3 2 1\n", "expected_stdout": "3\n", "is_sample": 1,
             "kind": "sample", "explanation": "1^1=0、2^2=0，只剩 3"},
            {"stdin": "1\n42\n", "expected_stdout": "42\n", "kind": "manual",
             "explanation": "只有一个数，它就是答案（异或 0 得自身）"},
            {"stdin": "5\n4 4 7 7 9\n", "expected_stdout": "9\n", "kind": "manual",
             "explanation": "4、7 成对抵消，剩 9"},
            {"stdin": "3\n5 5 0\n", "expected_stdout": "0\n", "kind": "manual",
             "explanation": "落单的可以是 0——5^5^0 = 0"},
            {"stdin": "9\n1 1 2 2 3 3 4 4 5\n", "expected_stdout": "5\n", "kind": "manual",
             "explanation": "四对全抵消，剩 5"},
        ],
    },
    {
        "title": "2 的幂判断",
        "line": "python",
        "question_type": "programming",
        "difficulty": 2,
        "total_score": 10,
        "tags": ["位运算", "与", "技巧"],
        "source_section": "第 02 讲 · 编程基础",
        "statement_md": (
            "读入一个非负整数 `x`，判断它是不是 2 的幂（1, 2, 4, 8, …），"
            "是输出 `YES`，不是输出 `NO`。\n\n"
            "★ 位运算的著名技巧：`x & (x - 1) == 0` 当且仅当 x 是 2 的幂——"
            "2 的幂二进制只有一个 1，`x - 1` 会把它借位成「后面全是 1」，两者相与必为 0。\n\n"
            "⚠️ 陷阱：`0 & -1` 也是 0，但 **0 不是 2 的幂**——先判 `x >= 1`。"
        ),
        "input_format": "一行一个非负整数 `x`（0 ≤ x < 2^30）。",
        "output_format": "一行：`YES` 或 `NO`。",
        "constraints_md": "- 0 ≤ x < 2^30",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "x = int(input())\n"
            "print(\"YES\" if x >= 1 and x & (x - 1) == 0 else \"NO\")\n"
        ),
        "alt_solution": (
            "# 第二套：反复除 2（与位技巧不同算法）\n"
            "x = int(input())\n"
            "ok = x >= 1\n"
            "while ok and x % 2 == 0:\n"
            "    x //= 2\n"
            "print(\"YES\" if ok and x == 1 else \"NO\")\n"
        ),
        "cases": [
            {"stdin": "1\n", "expected_stdout": "YES\n", "is_sample": 1,
             "kind": "sample", "explanation": "2^0 = 1，是"},
            {"stdin": "0\n", "expected_stdout": "NO\n", "kind": "manual",
             "explanation": "陷阱：0 & -1 == 0 会误判，必须先排除 0"},
            {"stdin": "1024\n", "expected_stdout": "YES\n", "kind": "manual",
             "explanation": "2^10"},
            {"stdin": "1023\n", "expected_stdout": "NO\n", "kind": "manual",
             "explanation": "0b11111111111111111111111111111 不止一个 1"},
            {"stdin": "1073741824\n", "expected_stdout": "YES\n", "kind": "manual",
             "explanation": "2^30，正好压约束上界"},
        ],
    },
    {
        "title": "十六进制提取器",
        "line": "python",
        "question_type": "programming",
        "difficulty": 2,
        "total_score": 12,
        "tags": ["进制转换", "十六进制", "字符串过滤", "格式化"],
        "source_section": "第 04 讲 · 字符串",
        "statement_md": (
            "读入一行字符串，把里面所有**十六进制字符**（`0-9` `a-f` `A-F`）按原顺序挑出来，"
            "统一**小写**后拼成一个串，按 16 进制解析成整数 `num`，"
            "然后输出一行：`num` 的十六进制、十进制、八进制、二进制（空格分隔，全不带前缀）。\n\n"
            "一个十六进制字符都没有就输出 `0 0 0 0`。\n\n"
            "四件套齐活：遍历筛选 → `append` 收集 → `\"\".join()` 拼串 → `int(s, 16)` 解析 → "
            "`f\"{num:x} {num:d} {num:o} {num:b}\"` 一行输出四种进制。\n\n"
            "⚠️ 注意：`x`、`g`、`z` 这些字母**不是**十六进制字符（只有 a~f）；"
            "`0x1F` 里的 `x` 会被剔除，剩下 `01f`。"
        ),
        "input_format": "一行字符串（长度 ≤ 100，可能为空或全空格）。",
        "output_format": "一行四个数：`十六进制 十进制 八进制 二进制`（空格分隔）。",
        "constraints_md": "- 挑出的十六进制串长度 ≤ 8",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "s = sys.stdin.readline().strip()\n"
            "res = []\n"
            "for ch in s:\n"
            "    if ch in '0123456789abcdefABCDEF':\n"
            "        res.append(ch.lower())\n"
            "if res:\n"
            "    hex_str = \"\".join(res)      # 变量别起名 str——会遮蔽内置类型\n"
            "    num = int(hex_str, 16)\n"
            "    print(f\"{num:x} {num:d} {num:o} {num:b}\")\n"
            "else:\n"
            "    print(\"0 0 0 0\")\n"
        ),
        "alt_solution": (
            "# 第二套：乘基累加解析（不用 int(s,16)），format() 函数代替 f-string\n"
            "import sys\n\n"
            "s = sys.stdin.readline().strip()\n"
            "DIGITS = \"0123456789abcdef\"\n"
            "num = 0\n"
            "for ch in s.lower():\n"
            "    if ch in DIGITS:\n"
            "        num = num * 16 + DIGITS.index(ch)\n"
            "print(f\"{format(num, 'x')} {format(num, 'd')} {format(num, 'o')} {format(num, 'b')}\")\n"
        ),
        "cases": [
            {"stdin": "aB3x!\n", "expected_stdout": "ab3 2739 5263 101010110011\n",
             "is_sample": 1, "kind": "sample",
             "explanation": "挑出 a、B、3 → 小写 ab3 = 2739；x 和 ! 不是十六进制字符"},
            {"stdin": "zzz\n", "expected_stdout": "0 0 0 0\n", "kind": "manual",
             "explanation": "z 不是十六进制字符，一个都挑不出 → 四个 0"},
            {"stdin": "deadbeef\n", "expected_stdout": "deadbeef 3735928559 33653337357 11011110101011011011111011101111\n",
             "kind": "manual", "explanation": "0xdeadbeef = 3735928559，四种进制全展开"},
            {"stdin": "0x1F\n", "expected_stdout": "1f 31 37 11111\n", "kind": "manual",
             "explanation": "陷阱：x 被剔除，剩 01f = 31"},
            {"stdin": "  \n", "expected_stdout": "0 0 0 0\n", "kind": "manual",
             "explanation": "全空格：挑不出任何字符"},
        ],
    },
    {
        "title": "剔除十六进制字符",
        "line": "python",
        "question_type": "programming",
        "difficulty": 2,
        "total_score": 10,
        "tags": ["字符串过滤", "join", "十六进制"],
        "source_section": "第 04 讲 · 字符串",
        "statement_md": (
            "读入一行字符串，把其中所有**十六进制字符**（`0-9` `a-f` `A-F`）**剔除**，"
            "其余字符按原顺序、原样输出一行。\n\n"
            "是上一题的「反着来」：筛选条件取反，且**不做**大小写转换。\n\n"
            "⚠️ 大坑：`a`~`f` 都是十六进制字符——`\"hello, world!\"` 里的 `e` 和 `d` 也要被剔掉！"
        ),
        "input_format": "一行字符串（长度 ≤ 100）。",
        "output_format": "一行：剔除后的字符串（可能为**空行**）。",
        "constraints_md": "- 输入长度 ≤ 100",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "s = sys.stdin.readline().strip()\n"
            "kept = \"\".join(ch for ch in s if ch not in \"0123456789abcdefABCDEF\")\n"
            "print(kept)\n"
        ),
        "alt_solution": (
            "# 第二套：逐字符范围判断 + 列表收集\n"
            "import sys\n\n"
            "s = sys.stdin.readline().strip()\n"
            "res = []\n"
            "for ch in s:\n"
            "    if not ('0' <= ch <= '9' or 'a' <= ch <= 'f' or 'A' <= ch <= 'F'):\n"
            "        res.append(ch)\n"
            "print(\"\".join(res))\n"
        ),
        "cases": [
            {"stdin": "aB3x!\n", "expected_stdout": "x!\n", "is_sample": 1,
             "kind": "sample", "explanation": "a、B、3 是十六进制字符被剔除，x 和 ! 留下"},
            {"stdin": "0123\n", "expected_stdout": "\n", "kind": "manual",
             "explanation": "全是十六进制字符 → 空行"},
            {"stdin": "abcdefg\n", "expected_stdout": "g\n", "kind": "manual",
             "explanation": "a~f 全被剔掉，只剩 g"},
            {"stdin": "hello, world!\n", "expected_stdout": "hllo, worl!\n", "kind": "manual",
             "explanation": "陷阱：e 和 d 也是十六进制字符，一起被剔掉"},
            {"stdin": "###\n", "expected_stdout": "###\n", "kind": "manual",
             "explanation": "没有十六进制字符，原样输出"},
        ],
    },
    {
        "title": "二进制串解析",
        "line": "python",
        "question_type": "programming",
        "difficulty": 2,
        "total_score": 10,
        "tags": ["进制转换", "二进制", "字符串过滤", "int"],
        "source_section": "第 04 讲 · 字符串",
        "statement_md": (
            "读入一行字符串，把里面所有 `0` 和 `1` 字符按原顺序挑出来拼成二进制串，"
            "按 2 进制解析成整数 `num`，输出一行：`num` 的十进制、十六进制（空格分隔，不带前缀）。\n\n"
            "一个 0/1 都没有就输出 `0 0`。\n\n"
            "和十六进制提取器同一套流水线，只是把「筛选表 + 基数」换成了二进制——"
            "体会 `int(s, base)` 里 base 的意思。"
        ),
        "input_format": "一行字符串（长度 ≤ 100）。",
        "output_format": "一行两个数：`十进制 十六进制`（空格分隔）。",
        "constraints_md": "- 挑出的二进制串长度 ≤ 30",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "s = sys.stdin.readline().strip()\n"
            "bits = \"\".join(ch for ch in s if ch in \"01\")\n"
            "num = int(bits, 2) if bits else 0\n"
            "print(f\"{num:d} {num:x}\")\n"
        ),
        "alt_solution": (
            "# 第二套：乘 2 累加（不用 int(s,2)）\n"
            "import sys\n\n"
            "s = sys.stdin.readline().strip()\n"
            "num = 0\n"
            "for ch in s:\n"
            "    if ch in \"01\":\n"
            "        num = num * 2 + (ch == \"1\")\n"
            "print(f\"{num} {format(num, 'x')}\")\n"
        ),
        "cases": [
            {"stdin": "10a1\n", "expected_stdout": "5 5\n", "is_sample": 1,
             "kind": "sample", "explanation": "挑出 101 = 5；十进制 5 的十六进制也是 5"},
            {"stdin": "xyz\n", "expected_stdout": "0 0\n", "kind": "manual",
             "explanation": "没有 0/1 字符"},
            {"stdin": "0011\n", "expected_stdout": "3 3\n", "kind": "manual",
             "explanation": "前导零无所谓：0011 = 3"},
            {"stdin": "1 0 1 0\n", "expected_stdout": "10 a\n", "kind": "manual",
             "explanation": "空格不是 0/1，挑出 1010 = 10 = 0xa"},
            {"stdin": "bin=1101!\n", "expected_stdout": "13 d\n", "kind": "manual",
             "explanation": "从杂质里挑出 1101 = 13 = 0xd"},
        ],
    },
    {
        "title": "自动识别进制",
        "line": "python",
        "question_type": "programming",
        "difficulty": 2,
        "total_score": 12,
        "tags": ["进制转换", "int", "前缀", "格式化"],
        "source_section": "第 08 讲 · 函数（下）",
        "statement_md": (
            "读入一行一个整数字面量——可能是十进制（直接写），"
            "也可能带 `0x` / `0b` / `0o` 前缀。按 `int(s, 0)` 的语义解析成整数 `num`，"
            "输出一行：`num` 的十六进制、十进制、八进制、二进制（空格分隔，全不带前缀）。\n\n"
            "一行 `f\"{num:x} {num:d} {num:o} {num:b}\"` 就是四种进制全家福——"
            "配合 `base=0` 的自动识别，进制的「读」和「写」两边就都通了。"
        ),
        "input_format": "一行一个整数字面量：十进制直接写，或带 `0x`/`0b`/`0o` 前缀（值 < 2^31）。",
        "output_format": "一行四个数：`十六进制 十进制 八进制 二进制`（空格分隔）。",
        "constraints_md": "- 解析结果 0 ≤ num < 2^31",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "s = sys.stdin.readline().strip()\n"
            "num = int(s, 0)                 # base=0：按前缀自动识别\n"
            "print(f\"{num:x} {num:d} {num:o} {num:b}\")\n"
        ),
        "alt_solution": (
            "# 第二套：手写剥前缀 + 显式 base 解析\n"
            "import sys\n\n"
            "s = sys.stdin.readline().strip()\n"
            "table = {\"0x\": 16, \"0b\": 2, \"0o\": 8}\n"
            "low = s.lower()\n"
            "base, body = 10, s\n"
            "for pre, b in table.items():\n"
            "    if low.startswith(pre):\n"
            "        base, body = b, s[2:]\n"
            "        break\n"
            "n = int(body, base)\n"
            "print(f\"{n:x} {n:d} {n:o} {n:b}\")\n"
        ),
        "cases": [
            {"stdin": "255\n", "expected_stdout": "ff 255 377 11111111\n", "is_sample": 1,
             "kind": "sample", "explanation": "十进制直写：ff / 255 / 377 / 11111111"},
            {"stdin": "0xff\n", "expected_stdout": "ff 255 377 11111111\n", "kind": "manual",
             "explanation": "带 0x 前缀，结果同上——base=0 认前缀"},
            {"stdin": "0b1010\n", "expected_stdout": "a 10 12 1010\n", "kind": "manual",
             "explanation": "二进制字面量 1010 = 10"},
            {"stdin": "0o377\n", "expected_stdout": "ff 255 377 11111111\n", "kind": "manual",
             "explanation": "八进制 377 = 255，三行殊途同归"},
            {"stdin": "0\n", "expected_stdout": "0 0 0 0\n", "kind": "manual",
             "explanation": "单个 0：四种进制都是 0"},
        ],
    },
]
