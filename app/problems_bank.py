"""题库：按讲义进度循序渐进的练习题。

设计原则
--------
1. **顺序跟讲义走** —— `source_section` 标出对应讲次，题目 id 顺序就是学习顺序
   （02 编程基础 → 03 流程控制 → 04 字符串 → 05 列表 → 06 字典 → 07/08 函数）
2. **期望输出独立写** —— 不是「跑出什么算什么」，而是先算好，再让参考解去撞它
3. **每题真跑过** —— `tools/verify_bank.py` 拿参考解跑一遍，与期望输出逐字节比对；
   比对不过的题不入库（防止我手算错、也防止参考解写错）
4. **分值按难度给** —— 入门 10 分、需要想一下 15 分、综合 20 分
"""
from __future__ import annotations

BANK_PROBLEMS: list[dict] = [
    # ------------------------------------------------------------------ #
    # 第 02 讲 · 编程基础：类型转换 / 格式化输出
    # ------------------------------------------------------------------ #
    {
        "title": "圆的面积",
        "line": "python",
        "difficulty": 1,
        "total_score": 10,
        "tags": ["输入输出", "类型转换", "格式化"],
        "source_section": "第 02 讲 · 编程基础",
        "statement_md": (
            "给定圆的半径 `r`，输出圆的面积，**保留 2 位小数**。\n\n"
            "本题 π 取 **3.14**（不要用 `math.pi`，那会差一点点）。\n\n"
            "这题练的是最基础的一环：`input()` 拿到的是**字符串**，"
            "必须先 `int()` 转成数字才能算。"
        ),
        "input_format": "一行，一个整数 `r`。",
        "output_format": "一行，面积，保留 2 位小数（例如 `3.14`、`314.00`）。",
        "constraints_md": "- 0 ≤ r ≤ 10000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "float",
        "float_eps": 0.000001,
        "reference_solution": (
            "import sys\n\n"
            "r = int(sys.stdin.read().strip())\n"
            "print('%.2f' % (3.14 * r * r))\n"
        ),
        "alt_solution": (
            "import sys\n"
            "\n"
            "r = int(sys.stdin.readline().strip())\n"
            "sys.stdout.write(format(3.14 * (r ** 2), \".2f\") + \"\\n\")\n"
        ),
        "cases": [
            {"stdin": "1\n", "expected_stdout": "3.14\n", "is_sample": 1,
             "kind": "sample", "explanation": "3.14 × 1 × 1 = 3.14"},
            {"stdin": "2\n", "expected_stdout": "12.56\n", "is_sample": 1,
             "kind": "sample", "explanation": "3.14 × 4 = 12.56"},
            {"stdin": "0\n", "expected_stdout": "0.00\n", "kind": "manual",
             "explanation": "半径 0，面积为 0"},
            {"stdin": "10\n", "expected_stdout": "314.00\n", "kind": "manual",
             "explanation": "3.14 × 100 = 314，补两位小数"},
            {"stdin": "7\n", "expected_stdout": "153.86\n", "kind": "manual",
             "explanation": "3.14 × 49 = 153.86"},
        ],
    },
    # ------------------------------------------------------------------ #
    # 第 03 讲 · 流程控制语句：if / 逻辑运算
    # ------------------------------------------------------------------ #
    {
        "title": "判断闰年",
        "line": "python",
        "difficulty": 1,
        "total_score": 10,
        "tags": ["条件判断", "逻辑运算"],
        "source_section": "第 03 讲 · 流程控制语句",
        "statement_md": (
            "判断给定的年份是不是闰年。\n\n"
            "闰年的规则：**能被 4 整除但不能被 100 整除**，或者**能被 400 整除**。\n\n"
            "最容易写错的是世纪年：1900 年能被 4 整除，但它不是闰年 —— "
            "因为「能被 100 整除」这一条把它拦掉了。"
        ),
        "input_format": "一行，一个整数 `y`（年份）。",
        "output_format": "一行，闰年输出 `yes`，否则输出 `no`。",
        "constraints_md": "- 1 ≤ y ≤ 9999",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "y = int(sys.stdin.read().strip())\n"
            "if (y % 4 == 0 and y % 100 != 0) or y % 400 == 0:\n"
            "    print('yes')\n"
            "else:\n"
            "    print('no')\n"
        ),
        "alt_solution": (
            "import sys\n"
            "import calendar\n"
            "\n"
            "y = int(sys.stdin.readline().strip())\n"
            "sys.stdout.write((\"yes\" if calendar.isleap(y) else \"no\") + \"\\n\")\n"
        ),
        "cases": [
            {"stdin": "2024\n", "expected_stdout": "yes\n", "is_sample": 1,
             "kind": "sample", "explanation": "2024 能被 4 整除、不能被 100 整除 → 闰年"},
            {"stdin": "1900\n", "expected_stdout": "no\n", "is_sample": 1,
             "kind": "sample", "explanation": "1900 能被 100 整除但不能被 400 整除 → 不是闰年（★ 最容易错的一个）"},
            {"stdin": "2000\n", "expected_stdout": "yes\n", "kind": "manual",
             "explanation": "2000 能被 400 整除 → 闰年"},
            {"stdin": "2023\n", "expected_stdout": "no\n", "kind": "manual"},
            {"stdin": "2100\n", "expected_stdout": "no\n", "kind": "manual",
             "explanation": "又一个世纪年陷阱"},
        ],
    },
    {
        "title": "数字三角形",
        "line": "python",
        "difficulty": 2,
        "total_score": 10,
        "tags": ["循环", "嵌套循环", "字符串拼接"],
        "source_section": "第 03 讲 · 流程控制语句",
        "statement_md": (
            "输入 `n`，输出 `n` 行数字三角形：第 `i` 行是从 1 到 `i`，数字之间用**一个空格**分隔。\n\n"
            "```text\n"
            "1\n"
            "1 2\n"
            "1 2 3\n"
            "```\n\n"
            "考点是**嵌套循环**，以及行末不要多出一个空格。"
        ),
        "input_format": "一行，一个整数 `n`。",
        "output_format": "`n` 行，第 `i` 行为 `1 2 … i`。",
        "constraints_md": "- 1 ≤ n ≤ 100",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "ignore_trailing",
        "reference_solution": (
            "import sys\n\n"
            "n = int(sys.stdin.read().strip())\n"
            "out = []\n"
            "for i in range(1, n + 1):\n"
            "    out.append(' '.join(str(x) for x in range(1, i + 1)))\n"
            "print('\\n'.join(out))\n"
        ),
        "alt_solution": (
            "import sys\n"
            "\n"
            "n = int(sys.stdin.readline().strip())\n"
            "rows = [str(list(range(1, i + 1)))[1:-1].replace(\",\", \"\") for i in range(1, n + 1)]\n"
            "sys.stdout.write(\"\\n\".join(rows) + \"\\n\")\n"
        ),
        "cases": [
            {"stdin": "3\n", "expected_stdout": "1\n1 2\n1 2 3\n", "is_sample": 1,
             "kind": "sample", "explanation": "3 行"},
            {"stdin": "1\n", "expected_stdout": "1\n", "is_sample": 1,
             "kind": "sample", "explanation": "边界：只有一行"},
            {"stdin": "2\n", "expected_stdout": "1\n1 2\n", "kind": "manual"},
            {"stdin": "5\n",
             "expected_stdout": "1\n1 2\n1 2 3\n1 2 3 4\n1 2 3 4 5\n",
             "kind": "manual"},
            {"stdin": "10\n",
             "expected_stdout": ("1\n1 2\n1 2 3\n1 2 3 4\n1 2 3 4 5\n"
                                 "1 2 3 4 5 6\n1 2 3 4 5 6 7\n1 2 3 4 5 6 7 8\n"
                                 "1 2 3 4 5 6 7 8 9\n1 2 3 4 5 6 7 8 9 10\n"),
             "kind": "manual", "explanation": "两位数开始考验拼接"},
        ],
    },
    {
        "title": "素数判断",
        "line": "python",
        "difficulty": 3,
        "total_score": 15,
        "tags": ["循环", "break", "边界", "性能"],
        "source_section": "第 03 讲 · 流程控制语句",
        "statement_md": (
            "判断给定整数是不是素数（质数）。\n\n"
            "两个坑：\n\n"
            "1. **1 不是素数**，也不是合数\n"
            "2. 直接试除到 `n-1` 会超时 —— 试到 **√n** 就够（如果 n 有因子，必有一个 ≤ √n）"
        ),
        "input_format": "一行，一个整数 `n`。",
        "output_format": "一行，`prime` 或 `not prime`。",
        "constraints_md": "- 1 ≤ n ≤ 10^9\n- 时间限制 1000 ms —— 提示：试除到 √n",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "n = int(sys.stdin.read().strip())\n"
            "if n < 2:\n"
            "    print('not prime')\n"
            "else:\n"
            "    ans = 'prime'\n"
            "    i = 2\n"
            "    while i * i <= n:\n"
            "        if n % i == 0:\n"
            "            ans = 'not prime'\n"
            "            break\n"
            "        i += 1\n"
            "    print(ans)\n"
        ),
        "alt_solution": (
            "import sys\n"
            "\n"
            "n = int(sys.stdin.readline().strip())\n"
            "ok = n >= 2 and all(n % i for i in range(2, int(n ** 0.5) + 1))\n"
            "sys.stdout.write((\"prime\" if ok else \"not prime\") + \"\\n\")\n"
        ),
        "cases": [
            {"stdin": "17\n", "expected_stdout": "prime\n", "is_sample": 1,
             "kind": "sample", "explanation": "17 只有 1 和它本身两个因子"},
            {"stdin": "1\n", "expected_stdout": "not prime\n", "is_sample": 1,
             "kind": "sample", "explanation": "1 不是素数（★ 最常错）"},
            {"stdin": "2\n", "expected_stdout": "prime\n", "kind": "manual",
             "explanation": "2 是最小的素数"},
            {"stdin": "4\n", "expected_stdout": "not prime\n", "kind": "manual",
             "explanation": "最小的合数，2 就把它整除了"},
            {"stdin": "1000000007\n", "expected_stdout": "prime\n", "kind": "manual",
             "explanation": "10^9 附近的素数；试除到 √n ≈ 31623 就够，全试会超时"},
            {"stdin": "1000000\n", "expected_stdout": "not prime\n", "kind": "manual"},
        ],
    },
    # ------------------------------------------------------------------ #
    # 第 04 讲 · 字符串
    # ------------------------------------------------------------------ #
    {
        "title": "字符串反转与回文",
        "line": "python",
        "difficulty": 1,
        "total_score": 10,
        "tags": ["字符串", "切片"],
        "source_section": "第 04 讲 · 字符串",
        "statement_md": (
            "读入一行字符串，输出两行：\n\n"
            "1. 它的**反转**\n"
            "2. 它是不是**回文**（正着读反着读一样），是输出 `yes`，不是输出 `no`\n\n"
            "Python 里反转一个字符串只要 `s[::-1]` —— 切片第三个参数是步长，"
            "写成 `-1` 就是从后往前一个个取。"
        ),
        "input_format": "一行字符串 `s`（可能为空，可能含空格）。",
        "output_format": "第一行是反转后的字符串；第二行是 `yes` 或 `no`。",
        "constraints_md": "- 0 ≤ len(s) ≤ 1000\n- 只含可见 ASCII 字符与空格",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "s = sys.stdin.readline().rstrip('\\n').rstrip('\\r')\n"
            "print(s[::-1])\n"
            "print('yes' if s == s[::-1] else 'no')\n"
        ),
        "alt_solution": (
            "import sys\n"
            "\n"
            "s = sys.stdin.readline().rstrip(\"\\n\").rstrip(\"\\r\")\n"
            "rev = \"\".join(reversed(s))\n"
            "sys.stdout.write(rev + \"\\n\")\n"
            "sys.stdout.write((\"yes\" if s == rev else \"no\") + \"\\n\")\n"
        ),
        "cases": [
            {"stdin": "abc\n", "expected_stdout": "cba\nno\n", "is_sample": 1,
             "kind": "sample"},
            {"stdin": "aba\n", "expected_stdout": "aba\nyes\n", "is_sample": 1,
             "kind": "sample"},
            {"stdin": "a\n", "expected_stdout": "a\nyes\n", "kind": "manual",
             "explanation": "长度 1 的串永远是回文"},
            {"stdin": "abccba\n", "expected_stdout": "abccba\nyes\n", "kind": "manual",
             "explanation": "偶数长度回文"},
            {"stdin": "Hello\n", "expected_stdout": "olleH\nno\n", "kind": "manual"},
            {"stdin": "\n", "expected_stdout": "\nyes\n", "kind": "manual",
             "explanation": "空串：反转还是空，回文成立"},
        ],
    },
    {
        "title": "单词计数",
        "line": "python",
        "difficulty": 2,
        "total_score": 10,
        "tags": ["字符串", "split", "空白处理"],
        "source_section": "第 04 讲 · 字符串",
        "statement_md": (
            "统计输入里一共有多少个单词（**按空白字符分割**，连续多个空格算一个分隔）。\n\n"
            "关键点：`s.split()` **不带参数**时会自动把连续空白压缩掉；"
            "而 `s.split(' ')` 会老老实实按每一个空格切，连出空串 —— 两者行为完全不同。\n\n"
            "输入可能是多行，也可能全是空白。"
        ),
        "input_format": "若干行文本。",
        "output_format": "一行，一个整数：单词总数。",
        "constraints_md": "- 输入总长度 ≤ 100000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "data = sys.stdin.read().split()\n"
            "print(len(data))\n"
        ),
        "alt_solution": (
            "import sys\n"
            "import re\n"
            "\n"
            "sys.stdout.write(str(len(re.findall(r\"\\S+\", sys.stdin.read()))) + \"\\n\")\n"
        ),
        "cases": [
            {"stdin": "hello world\n", "expected_stdout": "2\n", "is_sample": 1,
             "kind": "sample"},
            {"stdin": "  a   b  c  \n", "expected_stdout": "3\n", "is_sample": 1,
             "kind": "sample", "explanation": "连续空格和首尾空格都不算新单词"},
            {"stdin": "one\n", "expected_stdout": "1\n", "kind": "manual"},
            {"stdin": "\n", "expected_stdout": "0\n", "kind": "manual",
             "explanation": "空行 → 0 个单词"},
            {"stdin": "a b\nc d e\nf\n", "expected_stdout": "6\n", "kind": "manual",
             "explanation": "跨行统计"},
            {"stdin": "   \n\t\n  \n", "expected_stdout": "0\n", "kind": "manual",
             "explanation": "全是空白 → 0（用 split(' ') 就会数错）"},
        ],
    },
    # ------------------------------------------------------------------ #
    # 第 05 讲 · 列表与元组
    # ------------------------------------------------------------------ #
    {
        "title": "去重保序",
        "line": "python",
        "difficulty": 2,
        "total_score": 15,
        "tags": ["列表", "集合", "顺序"],
        "source_section": "第 05 讲 · 列表与元组",
        "statement_md": (
            "给 `n` 个整数，去掉重复的，**保持第一次出现的顺序**输出。\n\n"
            "直接用 `set()` 会丢顺序（集合是无序的），所以要么手动记录「见过没」，"
            "要么用 `dict.fromkeys()`（3.7 起字典保序）。"
        ),
        "input_format": "第一行一个整数 `n`；第二行 `n` 个整数，空格分隔。",
        "output_format": "一行，去重后的整数，空格分隔。",
        "constraints_md": "- 1 ≤ n ≤ 100000\n- 每个数的绝对值 ≤ 10^9",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "token",
        "reference_solution": (
            "import sys\n\n"
            "data = sys.stdin.read().split()\n"
            "n = int(data[0])\n"
            "nums = [int(x) for x in data[1:1 + n]]\n"
            "seen = set()\n"
            "out = []\n"
            "for x in nums:\n"
            "    if x not in seen:\n"
            "        seen.add(x)\n"
            "        out.append(x)\n"
            "print(' '.join(map(str, out)))\n"
        ),
        "alt_solution": (
            "import sys\n"
            "\n"
            "d = sys.stdin.read().split()\n"
            "n = int(d[0])\n"
            "nums = [int(x) for x in d[1:1 + n]]\n"
            "uniq = list(dict.fromkeys(nums))\n"
            "sys.stdout.write(\" \".join(map(str, uniq)) + \"\\n\")\n"
        ),
        "cases": [
            {"stdin": "5\n1 2 2 3 1\n", "expected_stdout": "1 2 3\n", "is_sample": 1,
             "kind": "sample"},
            {"stdin": "3\n5 5 5\n", "expected_stdout": "5\n", "is_sample": 1,
             "kind": "sample", "explanation": "全一样 → 只剩一个"},
            {"stdin": "1\n7\n", "expected_stdout": "7\n", "kind": "manual"},
            {"stdin": "6\n3 1 4 1 5 9\n", "expected_stdout": "3 1 4 5 9\n",
             "kind": "manual", "explanation": "顺序按首次出现"},
            {"stdin": "4\n-1 0 -1 0\n", "expected_stdout": "-1 0\n", "kind": "manual",
             "explanation": "含负数与 0"},
        ],
    },
    {
        "title": "第 k 大的数",
        "line": "python",
        "difficulty": 2,
        "total_score": 15,
        "tags": ["列表", "排序", "索引"],
        "source_section": "第 05 讲 · 列表与元组",
        "statement_md": (
            "给 `n` 个整数，求**第 k 大**的数。\n\n"
            "第 1 大就是最大值。**重复的数各算一个**（例如 `3 1 4 1 5` 第 3 大是 3）。\n\n"
            "最省事的写法是降序排序后取第 `k-1` 个 —— 注意列表下标从 **0** 开始。"
        ),
        "input_format": "第一行两个整数 `n` 和 `k`；第二行 `n` 个整数。",
        "output_format": "一行，第 `k` 大的数。",
        "constraints_md": "- 1 ≤ k ≤ n ≤ 100000\n- 每个数的绝对值 ≤ 10^9",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "data = sys.stdin.read().split()\n"
            "n, k = int(data[0]), int(data[1])\n"
            "nums = [int(x) for x in data[2:2 + n]]\n"
            "nums.sort(reverse=True)\n"
            "print(nums[k - 1])\n"
        ),
        "alt_solution": (
            "import sys\n"
            "import heapq\n"
            "\n"
            "d = sys.stdin.read().split()\n"
            "n, k = int(d[0]), int(d[1])\n"
            "nums = [int(x) for x in d[2:2 + n]]\n"
            "sys.stdout.write(str(heapq.nlargest(k, nums)[-1]) + \"\\n\")\n"
        ),
        "cases": [
            {"stdin": "5 1\n3 1 4 1 5\n", "expected_stdout": "5\n", "is_sample": 1,
             "kind": "sample", "explanation": "第 1 大 = 最大值"},
            {"stdin": "5 5\n3 1 4 1 5\n", "expected_stdout": "1\n", "is_sample": 1,
             "kind": "sample", "explanation": "第 5 大 = 最小值（降序最后一个是 1）"},
            {"stdin": "5 3\n3 1 4 1 5\n", "expected_stdout": "3\n", "kind": "manual",
             "explanation": "降序 5 4 3 1 1，第 3 个是 3"},
            {"stdin": "3 2\n10 20 30\n", "expected_stdout": "20\n", "kind": "manual"},
            {"stdin": "6 4\n7 7 7 8 9 9\n", "expected_stdout": "7\n", "kind": "manual",
             "explanation": "降序 9 9 8 7 7 7，第 4 个是 7"},
        ],
    },
    # ------------------------------------------------------------------ #
    # 第 06 讲 · 字典与集合
    # ------------------------------------------------------------------ #
    {
        "title": "词频统计",
        "line": "python",
        "difficulty": 2,
        "total_score": 20,
        "tags": ["字典", "排序", "多关键字排序"],
        "source_section": "第 06 讲 · 字典与集合",
        "statement_md": (
            "统计每个单词出现的次数，按下面的规则输出：\n\n"
            "- **次数多的在前**\n"
            "- 次数相同，**按字典序（字母序）排**\n"
            "- 每行 `单词 次数`\n\n"
            "这是「多关键字排序」：先比次数、再比单词。"
            "写成 `sorted(d.items(), key=lambda kv: (-kv[1], kv[0]))` 一次搞定。"
        ),
        "input_format": "第一行一个整数 `n`；随后 `n` 行，每行一个单词（不含空格）。",
        "output_format": "每行 `单词 次数`，按上面的规则排序。",
        "constraints_md": "- 1 ≤ n ≤ 100000\n- 单词由小写字母组成，长度 ≤ 20",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "data = sys.stdin.read().split()\n"
            "n = int(data[0])\n"
            "cnt = {}\n"
            "for w in data[1:1 + n]:\n"
            "    cnt[w] = cnt.get(w, 0) + 1\n"
            "for w, c in sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0])):\n"
            "    print(w, c)\n"
        ),
        "alt_solution": (
            "import sys\n"
            "from collections import Counter\n"
            "\n"
            "d = sys.stdin.read().split()\n"
            "n = int(d[0])\n"
            "cnt = Counter(d[1:1 + n])\n"
            "words = sorted(cnt)\n"
            "words.sort(key=lambda w: cnt[w], reverse=True)\n"
            "for w in words:\n"
            "    sys.stdout.write(\"%s %d\\n\" % (w, cnt[w]))\n"
        ),
        "cases": [
            {"stdin": "5\napple\nbanana\napple\ncherry\nbanana\n",
             "expected_stdout": "apple 2\nbanana 2\ncherry 1\n", "is_sample": 1,
             "kind": "sample",
             "explanation": "apple 和 banana 都是 2 次，按字母序 apple 在前"},
            {"stdin": "3\nb\na\nb\n", "expected_stdout": "b 2\na 1\n",
             "is_sample": 1, "kind": "sample"},
            {"stdin": "1\nz\n", "expected_stdout": "z 1\n", "kind": "manual"},
            {"stdin": "6\na\nb\nc\na\nb\na\n",
             "expected_stdout": "a 3\nb 2\nc 1\n", "kind": "manual"},
            {"stdin": "4\nd\nc\nb\na\n",
             "expected_stdout": "a 1\nb 1\nc 1\nd 1\n", "kind": "manual",
             "explanation": "全 1 次时完全按字母序"},
        ],
    },
    # ------------------------------------------------------------------ #
    # 第 07 讲 · 函数（上）
    # ------------------------------------------------------------------ #
    {
        "title": "最大公约数",
        "line": "python",
        "difficulty": 2,
        "total_score": 10,
        "tags": ["函数", "循环", "欧几里得算法", "边界"],
        "source_section": "第 07 讲 · 函数",
        "statement_md": (
            "求两个非负整数的最大公约数。\n\n"
            "用**辗转相除法**：`gcd(a, b) = gcd(b, a % b)`，直到 `b` 为 0，"
            "此时 `a` 就是答案。\n\n"
            "边界要留意：`gcd(0, 5) = 5`、`gcd(0, 0) = 0`。"
        ),
        "input_format": "一行，两个非负整数 `a` 和 `b`，空格分隔。",
        "output_format": "一行，最大公约数。",
        "constraints_md": "- 0 ≤ a, b ≤ 10^9",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "a, b = map(int, sys.stdin.read().split())\n"
            "while b:\n"
            "    a, b = b, a % b\n"
            "print(a)\n"
        ),
        "alt_solution": (
            "import sys\n"
            "import math\n"
            "\n"
            "a, b = map(int, sys.stdin.read().split())\n"
            "sys.stdout.write(str(math.gcd(a, b)) + \"\\n\")\n"
        ),
        "cases": [
            {"stdin": "12 18\n", "expected_stdout": "6\n", "is_sample": 1,
             "kind": "sample"},
            {"stdin": "7 13\n", "expected_stdout": "1\n", "is_sample": 1,
             "kind": "sample", "explanation": "两个素数 → 互质"},
            {"stdin": "0 5\n", "expected_stdout": "5\n", "kind": "manual",
             "explanation": "0 和任何数的公约数就是那个数"},
            {"stdin": "0 0\n", "expected_stdout": "0\n", "kind": "manual",
             "explanation": "数学上 gcd(0,0)=0；写成 while b 的循环天然返回 0"},
            {"stdin": "100 100\n", "expected_stdout": "100\n", "kind": "manual"},
            {"stdin": "998244353 1000000007\n", "expected_stdout": "1\n",
             "kind": "manual", "explanation": "两个大素数，互质"},
        ],
    },
    # ------------------------------------------------------------------ #
    # 第 08 讲 · 函数（下）：递归
    # ------------------------------------------------------------------ #
    {
        "title": "斐波那契数列",
        "line": "python",
        "difficulty": 2,
        "total_score": 15,
        "tags": ["递归", "迭代", "大整数"],
        "source_section": "第 08 讲 · 函数",
        "statement_md": (
            "求斐波那契数列第 `n` 项。定义：`F(0) = 0`，`F(1) = 1`，"
            "`F(n) = F(n-1) + F(n-2)`。\n\n"
            "**注意 `n = 200` 时结果有 42 位** —— Python 的整数没有上限，"
            "直接算就好；但**不要用朴素递归**（`F(200)` 要算 10^41 次，永远跑不完），"
            "要用循环或记忆化。"
        ),
        "input_format": "一行，一个整数 `n`。",
        "output_format": "一行，`F(n)`。",
        "constraints_md": "- 0 ≤ n ≤ 200\n- 时间限制 1000 ms —— 朴素递归必超时",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "n = int(sys.stdin.read().strip())\n"
            "a, b = 0, 1\n"
            "for _ in range(n):\n"
            "    a, b = b, a + b\n"
            "print(a)\n"
        ),
        "alt_solution": (
            "import sys\n"
            "from functools import lru_cache\n"
            "\n"
            "sys.setrecursionlimit(10000)\n"
            "\n"
            "\n"
            "@lru_cache(maxsize=None)\n"
            "def fib(n):\n"
            "    return n if n < 2 else fib(n - 1) + fib(n - 2)\n"
            "\n"
            "\n"
            "n = int(sys.stdin.readline().strip())\n"
            "sys.stdout.write(str(fib(n)) + \"\\n\")\n"
        ),
        "cases": [
            {"stdin": "0\n", "expected_stdout": "0\n", "is_sample": 1,
             "kind": "sample", "explanation": "F(0) = 0"},
            {"stdin": "1\n", "expected_stdout": "1\n", "is_sample": 1,
             "kind": "sample", "explanation": "F(1) = 1"},
            {"stdin": "10\n", "expected_stdout": "55\n", "kind": "manual"},
            {"stdin": "50\n", "expected_stdout": "12586269025\n", "kind": "manual",
             "explanation": "超过 32 位整数范围，C 语言这里就会溢出"},
            {"stdin": "90\n", "expected_stdout": "2880067194370816120\n",
             "kind": "manual", "explanation": "超过 64 位整数范围（2^63 ≈ 9.2×10^18）"},
            {"stdin": "200\n",
             "expected_stdout": "280571172992510140037611932413038677189525\n",
             "kind": "manual",
             "explanation": "42 位数；朴素递归算不出来，必须迭代或记忆化"},
        ],
    },
]


# ---------------------------------------------------------------------- #
# 第二批题库（第 02 ~ 11 讲，每讲至少 3 道，重难点更多）
# 放在 problems_bank_ext.py，这里合并成唯一的题库入口。
# 列表页按 source_section 的讲次排序，所以合并顺序不影响学习顺序。
# ---------------------------------------------------------------------- #
from .problems_bank_ext import EXT_PROBLEMS as _EXT_PROBLEMS  # noqa: E402

BANK_PROBLEMS = BANK_PROBLEMS + _EXT_PROBLEMS

# 第三批：第 12~14 讲（Python 讲义完结收尾）。同上：合并顺序不影响学习顺序。
from .problems_bank_ext2 import EXT2_PROBLEMS as _EXT2_PROBLEMS  # noqa: E402

BANK_PROBLEMS = BANK_PROBLEMS + _EXT2_PROBLEMS
