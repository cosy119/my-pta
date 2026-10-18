"""Python 技巧特训题库 —— **自动生成，不要手改**。

本文件由 `tools/gen_py_tricks.py` 产出，重新生成：

    python tools/gen_py_tricks.py

规矩与 DS 线一致：
1. 期望输出由生成脚本里的独立 Python `oracle` 预先算好（尽量用"笨办法"实现，
   与参考解不同路），拿参考解现跑现填等于自己给自己判卷。
2. 每题两套 Python 实现（reference_solution / alt_solution），verify_bank 双撞。
3. line = "python"，用 Python 线的判题通道。

分节「技巧特训 · Python」：讲义没专门讲、但做题常用的技巧性用法，
难度 1 → 4 递进，对标蓝桥杯 / 码蹄杯强度。
"""

PY_TRICKS_PROBLEMS: list[dict] = [
    {
        "title": "大小写与字符分类",
        "subject": "python",
        "line": "python",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "技巧特训",
            "字符串方法",
            "upper"
        ],
        "statement_md": "读入一行字符串，输出三行：\n\n1. 全大写版本\n2. 全小写版本\n3. 字母个数 和 数字个数（空格分隔）\n\n★ 技巧点：字符串自带 `s.upper()` / `s.lower()` 一行搞定大小写；`c.isalpha()` / `c.isdigit()` 直接做字符分类——不用手写 ASCII 换算。非字母字符在 `upper()/lower()` 里保持原样。",
        "input_format": "一行字符串（长度 ≤ 1000，可含字母、数字、空格与标点）。",
        "output_format": "三行，如题面所述。",
        "constraints_md": "- 1 ≤ 字符串长度 ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · Python",
        "reference_solution": "import sys\n\ns = sys.stdin.readline().rstrip(\"\\n\")\nprint(s.upper())\nprint(s.lower())\nletters = digits = 0\nfor ch in s:\n    if ch.isalpha():\n        letters += 1\n    elif ch.isdigit():\n        digits += 1\nprint(letters, digits)\n",
        "alt_solution": "import sys\n\ns = sys.stdin.readline().rstrip(\"\\n\")\nsys.stdout.write(s.upper() + \"\\n\" + s.lower() + \"\\n\")\nprint(sum(map(str.isalpha, s)), sum(map(str.isdigit, s)))\n",
        "cases": [
            {
                "stdin": "Hello, World 123!\n",
                "expected_stdout": "HELLO, WORLD 123!\nhello, world 123!\n10 3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "abcXYZ\n",
                "expected_stdout": "ABCXYZ\nabcxyz\n6 0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "12345\n",
                "expected_stdout": "12345\n12345\n0 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "!!!\n",
                "expected_stdout": "!!!\n!!!\n0 0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "MiXeD 42abc\n",
                "expected_stdout": "MIXED 42ABC\nmixed 42abc\n8 2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "负索引与切片反转",
        "subject": "python",
        "line": "python",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "技巧特训",
            "切片",
            "负索引"
        ],
        "statement_md": "读入一行**不含空格**的字符串，输出三行：\n\n1. 最后一个字符\n2. 反转后的字符串\n3. 去掉首尾各一个字符后的字符串（长度不足 2 输出 `EMPTY`）\n\n★ 技巧点：`s[-1]` 直取最后一个字符；`s[::-1]` 一步反转；`s[1:-1]` 掐头去尾——这三个负索引/切片写法是 Python 的招牌，C 里要手写下标运算好几行。",
        "input_format": "一行字符串（长度 1 ≤ len ≤ 1000，不含空格）。",
        "output_format": "三行，如题面所述。",
        "constraints_md": "- 1 ≤ len ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · Python",
        "reference_solution": "import sys\n\ns = sys.stdin.readline().rstrip(\"\\n\")\nprint(s[-1])\nprint(s[::-1])\nprint(s[1:-1] if len(s) >= 2 else \"EMPTY\")\n",
        "alt_solution": "import sys\n\ns = sys.stdin.readline().rstrip(\"\\n\")\nn = len(s)\nprint(s[n - 1])\nprint(\"\".join(reversed(s)))\nif n >= 2:\n    print(s[1:n - 1])\nelse:\n    print(\"EMPTY\")\n",
        "cases": [
            {
                "stdin": "abcdefg\n",
                "expected_stdout": "g\ngfedcba\nbcdef\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "a\n",
                "expected_stdout": "a\na\nEMPTY\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "ab\n",
                "expected_stdout": "b\nba\n\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "racecar\n",
                "expected_stdout": "r\nracecar\naceca\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "12345\n",
                "expected_stdout": "5\n54321\n234\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "单词规范化",
        "subject": "python",
        "line": "python",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "技巧特训",
            "split",
            "join",
            "strip"
        ],
        "statement_md": "读入一行英文，单词间可能有**多个空格**、首尾也可能有空格。输出两行：\n\n1. 规范化后的句子（单词间恰好一个空格，无首尾空格；没有单词则输出空行）\n2. 单词个数\n\n★ 技巧点：不带参的 `s.split()` 会按**任意空白**切分并**自动丢弃空串**——配合 `\" \".join(...)` 一行完成规范化。C 里这题要写状态机。",
        "input_format": "一行英文（长度 ≤ 10000，只含空格和可见字符）。",
        "output_format": "两行，如题面所述。",
        "constraints_md": "- 1 ≤ 长度 ≤ 10000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · Python",
        "reference_solution": "import sys\n\nwords = sys.stdin.readline().split()\nprint(\" \".join(words))\nprint(len(words))\n",
        "alt_solution": "import sys, re\n\nline = sys.stdin.readline().rstrip(\"\\n\")\nwords = re.split(r\"\\s+\", line.strip())\nwords = [w for w in words if w]\nprint(\" \".join(words))\nprint(len(words))\n",
        "cases": [
            {
                "stdin": "  hello   world  \n",
                "expected_stdout": "hello world\n2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "one\n",
                "expected_stdout": "one\n1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "   \n",
                "expected_stdout": "\n0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "a b  c d\n",
                "expected_stdout": "a b c d\n4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "The Quick BROWN fox\n",
                "expected_stdout": "The Quick BROWN fox\n4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "列表推导式三板斧",
        "subject": "python",
        "line": "python",
        "difficulty": 1,
        "total_score": 12,
        "tags": [
            "技巧特训",
            "列表推导式",
            "filter-map"
        ],
        "statement_md": "读入 `n` 和 `n` 个整数，输出三行：\n\n1. 所有**偶数**的平方（按原顺序，空格分隔；没有偶数则为空行）\n2. 奇数的个数\n3. 全体元素的和\n\n★ 技巧点：`[x*x for x in a if x % 2 == 0]` 一行同时完成**筛选（if）+ 映射（x*x）**，这就是 filter+map 的 Python 写法。负数奇偶判断注意：Python 里 `-3 % 2 == 1`，所以 `x % 2 == 0` 天然正确。",
        "input_format": "第一行 `n`；第二行 `n` 个整数（|元素| ≤ 10⁹）。",
        "output_format": "三行，如题面所述。",
        "constraints_md": "- 1 ≤ n ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · Python",
        "reference_solution": "import sys\n\nd = sys.stdin.read().split()\nn = int(d[0])\na = [int(v) for v in d[1:1 + n]]\nprint(*[x * x for x in a if x % 2 == 0])\nprint(len([x for x in a if x % 2 != 0]))\nprint(sum(a))\n",
        "alt_solution": "import sys\n\nd = sys.stdin.read().split()\nn = int(d[0])\na = list(map(int, d[1:1 + n]))\nevens = list(filter(lambda x: x % 2 == 0, a))\nprint(\" \".join(str(e * e) for e in evens))\nprint(n - len(evens))\nprint(sum(a))\n",
        "cases": [
            {
                "stdin": "6\n1 2 3 4 5 6\n",
                "expected_stdout": "4 16 36\n3\n21\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n-2 -3 0 7 8\n",
                "expected_stdout": "4 0 64\n2\n10\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n0\n",
                "expected_stdout": "0\n0\n0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n2 4 6\n",
                "expected_stdout": "4 16 36\n0\n12\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n-1 1 -5 5\n",
                "expected_stdout": "\n4\n0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "enumerate 与 zip",
        "subject": "python",
        "line": "python",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "技巧特训",
            "enumerate",
            "zip"
        ],
        "statement_md": "读入 `n` 和两组各 `n` 个整数 `a`、`b`，输出三行：\n\n1. 对应位置相加的结果（空格分隔）\n2. `a` 中**值恰好等于下标**的元素个数（下标从 0 起）\n3. `a` 与 `b` 对应位置相等的个数\n\n★ 技巧点：`zip(a, b)` 同时走两个序列、`enumerate(a)` 同时给**下标和值**——都不用亲手写 `range(len(a))`。这两个是 Python 双序列/带下标遍历的标准姿势。",
        "input_format": "第一行 `n`；第二行 `n` 个整数 `a`；第三行 `n` 个整数 `b`。",
        "output_format": "三行，如题面所述。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |元素| ≤ 10⁹",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · Python",
        "reference_solution": "import sys\n\nd = sys.stdin.read().split()\nn = int(d[0])\na = [int(v) for v in d[1:1 + n]]\nb = [int(v) for v in d[1 + n:1 + 2 * n]]\nprint(*[x + y for x, y in zip(a, b)])\nprint(sum(1 for i, x in enumerate(a) if x == i))\nprint(sum(1 for x, y in zip(a, b) if x == y))\n",
        "alt_solution": "import sys\n\nd = sys.stdin.read().split()\nn = int(d[0])\na = [int(v) for v in d[1:1 + n]]\nb = [int(v) for v in d[1 + n:1 + 2 * n]]\nout1 = []\nc1 = c2 = 0\nfor i in range(n):\n    out1.append(a[i] + b[i])\n    if a[i] == i:\n        c1 += 1\n    if a[i] == b[i]:\n        c2 += 1\nprint(*out1)\nprint(c1)\nprint(c2)\n",
        "cases": [
            {
                "stdin": "4\n0 5 2 9\n4 3 2 1\n",
                "expected_stdout": "4 8 4 10\n2\n1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n0\n0\n",
                "expected_stdout": "0\n1\n1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n1 1 1\n0 0 0\n",
                "expected_stdout": "1 1 1\n1\n0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n4 4 4 4 4\n1 2 3 4 5\n",
                "expected_stdout": "5 6 7 8 9\n1\n1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n0 1\n9 9\n",
                "expected_stdout": "9 10\n2\n0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "多关键字排序成绩单",
        "subject": "python",
        "line": "python",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "技巧特训",
            "sorted",
            "lambda",
            "稳定性"
        ],
        "statement_md": "读入 `n` 个学生的「姓名 分数」，输出排名列表：**分数降序**，同分按**姓名字典序升序**。每行 `姓名 分数`。\n\n★ 技巧点：`rows.sort(key=lambda r: (-r[1], r[0]))` —— 元组比较**先比第一项、再比第二项**，负号把降序翻成升序比较，一行写完多关键字。另一种写法是利用**稳定排序**：先按次关键字排，再按主关键字排。",
        "input_format": "第一行 `n`；随后 `n` 行，每行 `姓名 分数`（姓名不含空格）。",
        "output_format": "`n` 行，排序后的 `姓名 分数`。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 0 ≤ 分数 ≤ 100",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · Python",
        "reference_solution": "import sys\n\ndata = sys.stdin.read().split(\"\\n\")\nn = int(data[0])\nrows = []\nfor i in range(1, n + 1):\n    name, score = data[i].split()\n    rows.append((name, int(score)))\nrows.sort(key=lambda r: (-r[1], r[0]))\nfor name, score in rows:\n    print(name, score)\n",
        "alt_solution": "import sys\n\ndata = sys.stdin.read().split(\"\\n\")\nn = int(data[0])\nrows = []\nfor i in range(1, n + 1):\n    name, score = data[i].split()\n    rows.append((name, int(score)))\nrows.sort(key=lambda r: r[0])                      # 先按次关键字（名字）升序\nrows.sort(key=lambda r: r[1], reverse=True)        # 再按主关键字（分数）降序，稳定\nfor name, score in rows:\n    print(name, score)\n",
        "cases": [
            {
                "stdin": "4\nAlice 90\nBob 85\nCindy 90\nDave 70\n",
                "expected_stdout": "Alice 90\nCindy 90\nBob 85\nDave 70\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\nzhou 100\nli 100\nzhao 100\n",
                "expected_stdout": "li 100\nzhao 100\nzhou 100\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\nab 50\naa 60\n",
                "expected_stdout": "aa 60\nab 50\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\ne 1\nd 2\nc 3\nb 4\na 5\n",
                "expected_stdout": "a 5\nb 4\nc 3\nd 2\ne 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\nTom 88\nJerry 88\nSpike 77\n",
                "expected_stdout": "Jerry 88\nTom 88\nSpike 77\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "词频统计 dict.get",
        "subject": "python",
        "line": "python",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "技巧特训",
            "dict",
            "get",
            "词频"
        ],
        "statement_md": "读入一行单词，按**首次出现顺序**输出每个单词及其出现次数（每行 `单词 次数`），最后一行输出 `TOTAL 总词数`。\n\n★ 技巧点：`d[k] = d.get(k, 0) + 1` —— `get` 的第二个参数是**键不存在时的默认值**，计数器从此不用先判 `k in d`。顺便一提：标准库 `collections.Counter(单词列表)` 一行就能建好计数器，而且 Python 3.7+ 的字典**保持插入顺序**，天然按首次出现输出。",
        "input_format": "一行，若干个单词（1 ≤ 词数 ≤ 2000，单词长度 ≤ 20）。",
        "output_format": "如题面所述。",
        "constraints_md": "- 1 ≤ 词数 ≤ 2000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · Python",
        "reference_solution": "import sys\n\nwords = sys.stdin.readline().split()\ncnt = {}\nfor w in words:\n    cnt[w] = cnt.get(w, 0) + 1\nfor k, v in cnt.items():\n    print(k, v)\nprint(\"TOTAL\", len(words))\n",
        "alt_solution": "import sys\nfrom collections import Counter\n\nwords = sys.stdin.readline().split()\ncnt = Counter(words)\nfor k, v in cnt.items():          # Counter 是 dict 子类，保持首次出现顺序\n    print(k, v)\nprint(\"TOTAL\", len(words))\n",
        "cases": [
            {
                "stdin": "apple banana apple cherry banana apple\n",
                "expected_stdout": "apple 3\nbanana 2\ncherry 1\nTOTAL 6\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "one\n",
                "expected_stdout": "one 1\nTOTAL 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "a a a a\n",
                "expected_stdout": "a 4\nTOTAL 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "x y z x y v\n",
                "expected_stdout": "x 2\ny 2\nz 1\nv 1\nTOTAL 6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "hello world\n",
                "expected_stdout": "hello 1\nworld 1\nTOTAL 2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "集合运算四连",
        "subject": "python",
        "line": "python",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "技巧特训",
            "set",
            "交并差",
            "对称差"
        ],
        "statement_md": "读入两行整数（各自可重复、乱序），各看作一个集合。输出四行（元素升序、空格分隔，空集输出空行）：\n\n1. 交集\n2. 并集\n3. A − B（在 A 不在 B）\n4. 对称差（恰好在其中一个）\n\n★ 技巧点：`set` 自带运算符 `A & B`、`A | B`、`A - B`、`A ^ B`，四个运算四个字符，C 里每个都得手写双循环。重复元素会被 `set` 自动吸收，去重白送。",
        "input_format": "两行，每行若干个整数（可为空行？不会——每行至少 1 个；|元素| ≤ 10⁹）。",
        "output_format": "四行，如题面所述。",
        "constraints_md": "- 每行 1 ≤ 元素个数 ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · Python",
        "reference_solution": "import sys\n\nlines = sys.stdin.read().rstrip(\"\\n\").split(\"\\n\")\nA = set(map(int, lines[0].split()))\nB = set(map(int, lines[1].split()))\nfor s in (A & B, A | B, A - B, A ^ B):\n    print(*sorted(s))\n",
        "alt_solution": "import sys\n\nlines = sys.stdin.read().rstrip(\"\\n\").split(\"\\n\")\nA = set(map(int, lines[0].split()))\nB = set(map(int, lines[1].split()))\ninter = [x for x in A if x in B]\nunion = list(A) + [x for x in B if x not in A]\ndiff = [x for x in A if x not in B]\nsym = diff + [x for x in B if x not in A]\nfor s in (inter, union, diff, sym):\n    print(*sorted(s))\n",
        "cases": [
            {
                "stdin": "1 2 3 4\n3 4 5 6\n",
                "expected_stdout": "3 4\n1 2 3 4 5 6\n1 2\n1 2 5 6\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 2 3\n4 5 6\n",
                "expected_stdout": "\n1 2 3 4 5 6\n1 2 3\n1 2 3 4 5 6\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "7 7 8 9\n9 9 7\n",
                "expected_stdout": "7 9\n7 8 9\n8\n8\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n5\n",
                "expected_stdout": "5\n5\n\n\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10 20 30\n10 20 30\n",
                "expected_stdout": "10 20 30\n10 20 30\n\n\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "众数与次数 Counter",
        "subject": "python",
        "line": "python",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "技巧特训",
            "Counter",
            "most_common"
        ],
        "statement_md": "读入 `n` 个整数，输出出现次数最多的数及其次数（一行 `数 次数`）。若并列，输出**最小**的那个数。\n\n★ 技巧点：`collections.Counter(a)` 建计数器一行搞定，`most_common()` 直接按次数降序给结果——并列时想取最小值，再对候选排一次序即可。这题练的是「计数器 + 一次遍历找最优」。",
        "input_format": "第一行 `n`；第二行 `n` 个整数（|元素| ≤ 10⁹）。",
        "output_format": "一行 `数 次数`。",
        "constraints_md": "- 1 ≤ n ≤ 10⁵",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · Python",
        "reference_solution": "import sys\nfrom collections import Counter\n\nd = sys.stdin.read().split()\na = [int(v) for v in d[1:1 + int(d[0])]]\ncnt = Counter(a)\ntop = max(cnt.values())\nans = min(k for k, v in cnt.items() if v == top)\nprint(ans, top)\n",
        "alt_solution": "import sys\n\nd = sys.stdin.read().split()\na = [int(v) for v in d[1:1 + int(d[0])]]\ncnt = {}\nfor x in a:\n    cnt[x] = cnt.get(x, 0) + 1\nbest_x, best_c = None, 0\nfor k in sorted(cnt):\n    if cnt[k] > best_c:\n        best_x, best_c = k, cnt[k]\nprint(best_x, best_c)\n",
        "cases": [
            {
                "stdin": "6\n1 2 2 3 3 3\n",
                "expected_stdout": "3 3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "7\n5 5 1 1 9 9 9\n",
                "expected_stdout": "9 3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n-1 -1 2 2\n",
                "expected_stdout": "-1 2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n42\n",
                "expected_stdout": "42 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8\n1 2 1 2 1 2 3 3\n",
                "expected_stdout": "1 3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "第 k 大 heapq",
        "subject": "python",
        "line": "python",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "技巧特训",
            "heapq",
            "堆",
            "top-k"
        ],
        "statement_md": "读入 `n`、`k` 和 `n` 个整数，输出**第 k 大**的数（重复元素各自算位次）。\n\n★ 技巧点：`heapq.nlargest(k, a)[-1]` 直接给出第 k 大；标准库 `heapq` 是**小顶堆**（`heapq.heappush/heappop`），「维护一个大小为 k 的小顶堆扫一遍」是流式数据的 top-k 标准解法，n 很大、k 很小时比全排序省得多。",
        "input_format": "第一行 `n k`；第二行 `n` 个整数（|元素| ≤ 10⁹）。",
        "output_format": "一行，第 k 大的数。",
        "constraints_md": "- 1 ≤ k ≤ n ≤ 2×10⁵",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · Python",
        "reference_solution": "import sys, heapq\n\nd = sys.stdin.read().split()\nn, k = int(d[0]), int(d[1])\na = [int(v) for v in d[2:2 + n]]\nprint(heapq.nlargest(k, a)[-1])\n",
        "alt_solution": "import sys, heapq\n\nd = sys.stdin.read().split()\nn, k = int(d[0]), int(d[1])\na = [int(v) for v in d[2:2 + n]]\nheap = a[:k]                      # 大小为 k 的小顶堆\nheapq.heapify(heap)\nfor x in a[k:]:\n    if x > heap[0]:\n        heapq.heapreplace(heap, x)\nprint(heap[0])\n",
        "cases": [
            {
                "stdin": "5 2\n3 1 4 1 5\n",
                "expected_stdout": "4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "6 3\n9 9 8 8 7 1\n",
                "expected_stdout": "8\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 1\n100\n",
                "expected_stdout": "100\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10 10\n1 2 3 4 5 6 7 8 9 10\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7 5\n5 5 5 5 5 5 5\n",
                "expected_stdout": "5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "前缀和 accumulate",
        "subject": "python",
        "line": "python",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "技巧特训",
            "前缀和",
            "accumulate",
            "itertools"
        ],
        "statement_md": "读入 `n`、`q` 和数组 `a`，接着 `q` 个询问 `l r`（1 基闭区间）。对每个询问输出区间和（一行一个）。\n\n★ 技巧点：**先建前缀和、再 O(1) 回答**——`pre[i] = a[0..i-1] 之和`，区间和 = `pre[r] - pre[l-1]`。Python 里 `list(itertools.accumulate(a))` 一行建好前缀和。预处理一次，查询白送，这是竞赛最常用的套路没有之一。",
        "input_format": "第一行 `n q`；第二行 `n` 个整数；随后 `q` 行每行 `l r`。\n- 1 ≤ n ≤ 10⁵，1 ≤ q ≤ 1000，|aᵢ| ≤ 10⁹，1 ≤ l ≤ r ≤ n",
        "output_format": "`q` 行，每行一个区间和。",
        "constraints_md": "- 1 ≤ n ≤ 10⁵\n- 1 ≤ q ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · Python",
        "reference_solution": "import sys\nfrom itertools import accumulate\n\nd = sys.stdin.read().split()\nn, q = int(d[0]), int(d[1])\na = [int(v) for v in d[2:2 + n]]\npre = [0] + list(accumulate(a))     # pre[i] = a[0..i-1] 之和\ni = 2 + n\nout = []\nfor _ in range(q):\n    l, r = int(d[i]), int(d[i + 1])\n    i += 2\n    out.append(pre[r] - pre[l - 1])\nprint(\"\\n\".join(map(str, out)))\n",
        "alt_solution": "import sys\n\nd = sys.stdin.read().split()\nn, q = int(d[0]), int(d[1])\na = [int(v) for v in d[2:2 + n]]\npre = [0] * (n + 1)\nfor k in range(n):\n    pre[k + 1] = pre[k] + a[k]\ni = 2 + n\nout = []\nfor _ in range(q):\n    l, r = int(d[i]), int(d[i + 1])\n    i += 2\n    out.append(pre[r] - pre[l - 1])\nprint(\"\\n\".join(map(str, out)))\n",
        "cases": [
            {
                "stdin": "5 3\n1 2 3 4 5\n1 5\n2 4\n3 3\n",
                "expected_stdout": "15\n9\n3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 2\n-1 -2 -3\n1 1\n1 3\n",
                "expected_stdout": "-1\n-6\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 1\n1000000000\n1 1\n",
                "expected_stdout": "1000000000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6 4\n2 0 -2 4 -4 8\n1 6\n2 2\n3 5\n6 6\n",
                "expected_stdout": "8\n0\n-2\n8\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4 1\n9 9 9 9\n2 3\n",
                "expected_stdout": "18\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "第一个大于 x 的数 bisect",
        "subject": "python",
        "line": "python",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "技巧特训",
            "bisect",
            "二分",
            "upper_bound"
        ],
        "statement_md": "读入**升序**数组（可重复）和 `q` 个询问 `x`。对每个询问，输出数组中**第一个严格大于 x** 的元素；不存在输出 `NONE`。\n\n★ 技巧点：`bisect.bisect_right(a, x)` 返回「x 能插入的最右位置」，**恰好就是第一个大于 x 的下标**——这是 C++ `upper_bound` 的 Python 对应物，一行替代线性扫描。配套记忆：`bisect_left` 找第一个 ≥ x 的位置。有序数组的「第一个大于/小于」类问题，全部走二分，别写 for。",
        "input_format": "第一行 `n q`；第二行 `n` 个**升序**整数；随后 `q` 行每行一个 `x`。\n- 1 ≤ n, q ≤ 2×10⁵，|元素|、|x| ≤ 10⁹",
        "output_format": "`q` 行，每行一个数或 `NONE`。",
        "constraints_md": "- 1 ≤ n, q ≤ 2×10⁵",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · Python",
        "reference_solution": "import sys, bisect\n\nd = sys.stdin.read().split()\nn, q = int(d[0]), int(d[1])\na = [int(v) for v in d[2:2 + n]]\ni = 2 + n\nout = []\nfor _ in range(q):\n    x = int(d[i]); i += 1\n    p = bisect.bisect_right(a, x)   # 第一个 > x 的下标\n    out.append(str(a[p]) if p < n else \"NONE\")\nprint(\"\\n\".join(out))\n",
        "alt_solution": "import sys\n\nd = sys.stdin.read().split()\nn, q = int(d[0]), int(d[1])\na = [int(v) for v in d[2:2 + n]]\ni = 2 + n\nout = []\nfor _ in range(q):\n    x = int(d[i]); i += 1\n    lo, hi = 0, n                    # 手写二分：找第一个 > x\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if a[mid] > x:\n            hi = mid\n        else:\n            lo = mid + 1\n    out.append(str(a[lo]) if lo < n else \"NONE\")\nprint(\"\\n\".join(out))\n",
        "cases": [
            {
                "stdin": "8 4\n1 2 4 4 4 7 9 9\n4\n5\n9\n0\n",
                "expected_stdout": "7\n7\nNONE\n1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5 3\n2 2 2 2 2\n1\n2\n3\n",
                "expected_stdout": "2\nNONE\nNONE\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 2\n10\n10\n11\n",
                "expected_stdout": "NONE\nNONE\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6 2\n-5 -2 0 3 8 8\n-6\n8\n",
                "expected_stdout": "-5\nNONE\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4 3\n1 3 5 7\n7\n6\n1\n",
                "expected_stdout": "NONE\n7\n3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "爬楼梯 lru_cache",
        "subject": "python",
        "line": "python",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "技巧特训",
            "lru_cache",
            "记忆化",
            "递归"
        ],
        "statement_md": "台阶有 `n` 阶，每次上 1 或 2 阶，问有多少种走法（f(1)=1，f(2)=2）。n 最大 90——结果会非常大，直接输出精确值。\n\n★ 技巧点：给递归函数挂上 `@functools.lru_cache(maxsize=None)`，朴素递归从 O(2ⁿ) 变 O(n)——**记忆化一行加注解就有了**。Python 的整数没有溢出，大结果直接打出来；这个题同时是「递归会重复算」的活教材。",
        "input_format": "一行一个整数 `n`。",
        "output_format": "一行，走法总数。",
        "constraints_md": "- 1 ≤ n ≤ 90",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · Python",
        "reference_solution": "import sys\nfrom functools import lru_cache\n\n@lru_cache(maxsize=None)\ndef f(n):\n    if n <= 2:\n        return n\n    return f(n - 1) + f(n - 2)\n\nprint(f(int(sys.stdin.read())))\n",
        "alt_solution": "import sys\n\nn = int(sys.stdin.read())\nx, y = 1, 2                 # f(1), f(2)\nif n == 1:\n    print(x)\nelse:\n    for _ in range(n - 2):\n        x, y = y, x + y\n    print(y)\n",
        "cases": [
            {
                "stdin": "1\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n",
                "expected_stdout": "2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "10\n",
                "expected_stdout": "89\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "50\n",
                "expected_stdout": "20365011074\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "90\n",
                "expected_stdout": "4660046610375530309\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "回文判定与清洗",
        "subject": "python",
        "line": "python",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "技巧特训",
            "回文",
            "isalnum",
            "切片反转"
        ],
        "statement_md": "读入一行（可含标点、空格），只保留**字母和数字**并忽略大小写后，判断是否回文。第一行输出 `YES`/`NO`，第二行输出清洗后的串。\n\n★ 技巧点：生成器表达式 + `.join(...)` 做字符过滤：\n`t = .join(c.lower() for c in s if c.isalnum())`，回文判定就是 `t == t[::-1]`——清洗、比较各一行。空清洗结果（全是标点）按回文处理。",
        "input_format": "一行字符串（长度 ≤ 10000）。",
        "output_format": "两行：`YES`/`NO` 与清洗后的串。",
        "constraints_md": "- 1 ≤ 长度 ≤ 10000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · Python",
        "reference_solution": "import sys\n\ns = sys.stdin.readline().rstrip(\"\\n\")\nt = \"\".join(c.lower() for c in s if c.isalnum())\nprint(\"YES\" if t == t[::-1] else \"NO\")\nprint(t)\n",
        "alt_solution": "import sys\n\ns = sys.stdin.readline().rstrip(\"\\n\")\nt = \"\".join(c.lower() for c in s if c.isalnum())\ni, j = 0, len(t) - 1\nok = True\nwhile i < j:\n    if t[i] != t[j]:\n        ok = False\n        break\n    i += 1\n    j -= 1\nprint(\"YES\" if ok else \"NO\")\nprint(t)\n",
        "cases": [
            {
                "stdin": "A man, a plan, a canal: Panama\n",
                "expected_stdout": "YES\namanaplanacanalpanama\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "race a car\n",
                "expected_stdout": "NO\nraceacar\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "!!!\n",
                "expected_stdout": "YES\n\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "0P\n",
                "expected_stdout": "NO\n0p\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "Was it a car or a cat I saw?\n",
                "expected_stdout": "YES\nwasitacaroracatisaw\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "01 背包",
        "subject": "python",
        "line": "python",
        "difficulty": 3,
        "total_score": 25,
        "tags": [
            "技巧特训",
            "DP",
            "背包",
            "动态规划"
        ],
        "statement_md": "经典 0-1 背包：`n` 件物品，第 `i` 件重量 `wᵢ`、价值 `vᵢ`，背包容量的上限 `W`，每件**至多选一次**。求能装下的最大总价值。\n\n★ 技巧点：一维滚动数组——`dp[j] = max(dp[j], dp[j-w] + v)`，**内层必须倒着枚举** `j`（正着走同一件物品会被选两次，那就成了完全背包）。「倒序 = 0-1，正序 = 完全」是背包家族的第一条铁律。",
        "input_format": "第一行 `n W`；随后 `n` 行每行 `w v`。\n- 1 ≤ n ≤ 100，1 ≤ W ≤ 10000，1 ≤ w ≤ W，0 ≤ v ≤ 10⁴",
        "output_format": "一行，最大总价值。",
        "constraints_md": "- 1 ≤ n ≤ 100\n- 1 ≤ W ≤ 10⁴",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · Python",
        "reference_solution": "import sys\n\nd = sys.stdin.read().split()\nn, W = int(d[0]), int(d[1])\ndp = [0] * (W + 1)\ni = 2\nfor _ in range(n):\n    w, v = int(d[i]), int(d[i + 1])\n    i += 2\n    for j in range(W, w - 1, -1):        # 倒序：保证每件只选一次\n        cand = dp[j - w] + v\n        if cand > dp[j]:\n            dp[j] = cand\nprint(dp[W])\n",
        "alt_solution": "import sys\nfrom functools import lru_cache\n\nd = sys.stdin.read().split()\nn, W = int(d[0]), int(d[1])\nws = []\nvs = []\ni = 2\nfor _ in range(n):\n    ws.append(int(d[i])); vs.append(int(d[i + 1]))\n    i += 2\n\n@lru_cache(maxsize=None)\ndef f(k, cap):                # 前 k 件、剩余容量 cap 的最大价值\n    if k == 0:\n        return 0\n    best = f(k - 1, cap)\n    if ws[k - 1] <= cap:\n        cand = f(k - 1, cap - ws[k - 1]) + vs[k - 1]\n        if cand > best:\n            best = cand\n    return best\n\nprint(f(n, W))\n",
        "cases": [
            {
                "stdin": "4 5\n1 2\n2 3\n3 4\n4 5\n",
                "expected_stdout": "7\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 10\n5 10\n4 8\n6 12\n",
                "expected_stdout": "20\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 1\n1 100\n",
                "expected_stdout": "100\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5 7\n2 3\n3 4\n4 5\n5 6\n1 1\n",
                "expected_stdout": "9\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6 13\n3 5\n4 7\n2 3\n7 9\n5 6\n1 2\n",
                "expected_stdout": "20\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "最长上升子序列 n log n",
        "subject": "python",
        "line": "python",
        "difficulty": 3,
        "total_score": 25,
        "tags": [
            "技巧特训",
            "LIS",
            "二分",
            "bisect"
        ],
        "statement_md": "读入 `n` 个整数，输出**严格上升**子序列的最长长度。\n\n★ 技巧点：维护「每个长度对应的最小结尾」数组 `tails`，对每个 x 用 `bisect_left` 找到它该待的位置：替换或追加。`tails` 始终有序，整个过程 O(n log n)——n=10⁵ 的 LIS 只能这么做，O(n²) 的 DP 会超时。",
        "input_format": "第一行 `n`；第二行 `n` 个整数（|元素| ≤ 10⁹）。",
        "output_format": "一行，严格上升子序列的最长长度。",
        "constraints_md": "- 1 ≤ n ≤ 10⁵",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · Python",
        "reference_solution": "import sys, bisect\n\nd = sys.stdin.read().split()\nn = int(d[0])\na = [int(v) for v in d[1:1 + n]]\ntails = []                        # tails[k] = 长度 k+1 的 LIS 的最小结尾\nfor x in a:\n    p = bisect.bisect_left(tails, x)   # 严格上升 → bisect_left\n    if p == len(tails):\n        tails.append(x)\n    else:\n        tails[p] = x\nprint(len(tails))\n",
        "alt_solution": "import sys\n\nd = sys.stdin.read().split()\nn = int(d[0])\na = [int(v) for v in d[1:1 + n]]\nINF = float(\"inf\")\ntails = [INF] * n                 # tails[k] = 长度 k+1 的最小结尾，初始无穷\nlen_ = 0\nfor x in a:\n    lo, hi = 0, len_\n    while lo < hi:                # 手写二分找第一个 >= x 的位置\n        mid = (lo + hi) // 2\n        if tails[mid] >= x:\n            hi = mid\n        else:\n            lo = mid + 1\n    tails[lo] = x\n    if lo == len_:\n        len_ += 1\nprint(len_)\n",
        "cases": [
            {
                "stdin": "8\n1 3 2 3 1 4 2 5\n",
                "expected_stdout": "5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n5 4 3 2 1\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "6\n1 2 3 4 5 6\n",
                "expected_stdout": "6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n7\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n2 2 2 2 3 3 3 1 9 9\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "快速幂取模",
        "subject": "python",
        "line": "python",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "技巧特训",
            "快速幂",
            "pow",
            "取模"
        ],
        "statement_md": "读入 `a b m`，输出 `a^b mod m`。b 最大 10¹⁸——暴力乘 10¹⁸ 次是天文数字。\n\n★ 技巧点：Python 内置三参 `pow(a, b, m)` 就是快速幂，**一行，还比手写快**（C 实现里 m 内建了模乘优化）。要理解原理就自己写：b 按二进制拆位，平方翻底数——手写版是竞赛通用语言（C++ 没有 powmod），两边都得会。",
        "input_format": "一行 `a b m`（1 ≤ a, m ≤ 10⁹；0 ≤ b ≤ 10¹⁸）。",
        "output_format": "一行，`a^b mod m`。",
        "constraints_md": "- 1 ≤ a, m ≤ 10⁹\n- 0 ≤ b ≤ 10¹⁸",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · Python",
        "reference_solution": "import sys\n\na, b, m = map(int, sys.stdin.read().split())\nprint(pow(a, b, m))          # 内置三参 pow = 快速幂取模\n",
        "alt_solution": "import sys\n\na, b, m = map(int, sys.stdin.read().split())\nr = 1 % m\nbase = a % m\ne = b\nwhile e > 0:                 # 手写快速幂：按指数二进制位逐位平方\n    if e & 1:\n        r = r * base % m\n    base = base * base % m\n    e >>= 1\nprint(r)\n",
        "cases": [
            {
                "stdin": "2 10 1000\n",
                "expected_stdout": "24\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 0 7\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2 62 1000000007\n",
                "expected_stdout": "145586002\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5 100 1000000007\n",
                "expected_stdout": "146981449\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "123456789 999999999999999998 998244353\n",
                "expected_stdout": "499476836\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "区间合并",
        "subject": "python",
        "line": "python",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "技巧特训",
            "贪心",
            "排序",
            "区间"
        ],
        "statement_md": "读入 `n` 个闭区间，把所有**有重叠或相接**的区间合并，输出合并后的个数与各区间（按左端点升序，每行 `l r`）。\n\n★ 技巧点：**先按左端点排序，再线性扫一遍**——当前区间起点 ≤ 上一合并区间的终点就合并（终点取 max），否则另起一段。「排序后扫一遍」是所有区间类问题（合并 / 插入 / 去覆盖）的总套路。",
        "input_format": "第一行 `n`；随后 `n` 行每行 `l r`（l ≤ r）。",
        "output_format": "第一行合并后个数；随后每行一个合并区间 `l r`。",
        "constraints_md": "- 1 ≤ n ≤ 10⁵\n- 0 ≤ l ≤ r ≤ 10⁹",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · Python",
        "reference_solution": "import sys\n\nd = sys.stdin.read().split()\nn = int(d[0])\nivs = sorted((int(d[1 + 2 * i]), int(d[2 + 2 * i])) for i in range(n))\nmerged = []\nfor l, r in ivs:\n    if merged and l <= merged[-1][1]:\n        merged[-1][1] = max(merged[-1][1], r)\n    else:\n        merged.append([l, r])\nprint(len(merged))\nfor l, r in merged:\n    print(l, r)\n",
        "alt_solution": "import sys\n\nd = sys.stdin.read().split()\nn = int(d[0])\nivs = []\nfor i in range(n):\n    ivs.append((int(d[1 + 2 * i]), int(d[2 + 2 * i])))\nivs.sort(key=lambda p: (p[0], p[1]))\ncl, cr = ivs[0]\nout = []\nfor l, r in ivs[1:]:\n    if l <= cr:\n        cr = max(cr, r)\n    else:\n        out.append((cl, cr))\n        cl, cr = l, r\nout.append((cl, cr))\nprint(len(out))\nfor l, r in out:\n    print(l, r)\n",
        "cases": [
            {
                "stdin": "4\n1 3\n2 6\n8 10\n15 18\n",
                "expected_stdout": "3\n1 6\n8 10\n15 18\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n1 4\n4 5\n2 3\n",
                "expected_stdout": "1\n1 5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n1 2\n3 4\n",
                "expected_stdout": "2\n1 2\n3 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n5 6\n1 2\n3 4\n2 3\n6 7\n",
                "expected_stdout": "2\n1 4\n5 7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n0 1000000000\n",
                "expected_stdout": "1\n0 1000000000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "阶乘精确值与大数",
        "subject": "python",
        "line": "python",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "技巧特训",
            "大数",
            "math",
            "factorial"
        ],
        "statement_md": "读入 `n`，输出两行：`n!` 的**位数**、`n!` 的**精确值**。\n\n★ 技巧点：Python 的 `int` 是任意精度大数，`math.factorial(n)` 直接给出几百位的精确结果，`len(str(f))` 就是位数——C 里这是要开数组做高精度乘法的大工程。Python 做大数题（大数加乘、精确分数、连乘取模前先留底）是降维打击。",
        "input_format": "一行一个整数 `n`。",
        "output_format": "两行：位数、精确值。",
        "constraints_md": "- 0 ≤ n ≤ 500",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · Python",
        "reference_solution": "import sys, math\n\nn = int(sys.stdin.read())\nf = math.factorial(n)\nprint(len(str(f)))\nprint(f)\n",
        "alt_solution": "import sys\nfrom functools import reduce\nfrom operator import mul\n\nn = int(sys.stdin.read())\nf = reduce(mul, range(1, n + 1), 1)\nprint(len(str(f)))\nprint(f)\n",
        "cases": [
            {
                "stdin": "0\n",
                "expected_stdout": "1\n1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n",
                "expected_stdout": "1\n1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "10\n",
                "expected_stdout": "7\n3628800\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100\n",
                "expected_stdout": "158\n93326215443944152681699238856266700490715968264381621468592963895217599993229915608941463976156518286253697920827223758251185210916864000000000000000000000000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "500\n",
                "expected_stdout": "1135\n1220136825991110068701238785423046926253574342803192842192413588385845373153881997605496447502203281863013616477148203584163378722078177200480785205159329285477907571939330603772960859086270429174547882424912726344305670173270769461062802310452644218878789465754777149863494367781037644274033827365397471386477878495438489595537537990423241061271326984327745715546309977202781014561081188373709531016356324432987029563896628911658974769572087926928871281780070265174507768410719624390394322536422605234945850129918571501248706961568141625359056693423813008856249246891564126775654481886506593847951775360894005745238940335798476363944905313062323749066445048824665075946735862074637925184200459369692981022263971952597190945217823331756934581508552332820762820023402626907898342451712006207714640979456116127629145951237229913340169552363850942885592018727433795173014586357570828355780158735432768888680120399882384702151467605445407663535984174430480128938313896881639487469658817504506926365338175055478128640000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "素数筛法",
        "subject": "python",
        "line": "python",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "技巧特训",
            "筛法",
            "埃氏筛",
            "素数"
        ],
        "statement_md": "读入 `n`，输出一行两个数：`2..n` 里素数的**个数**与**最大的素数**（n ≥ 2，必有素数）。\n\n★ 技巧点：**埃氏筛**——从每个素数 p 开始，把 p², p²+p, ... 全部标记为合数，整体 O(n log log n)；`i*i` 起步（更小的倍数早被筛过）是关键小优化。试除判单个数是 O(√n)，要判 1~n 全体就得用筛。Python 版注意用列表下标而不是集合，否则常数爆炸。",
        "input_format": "一行一个整数 `n`。",
        "output_format": "一行：素数个数 与 最大素数（空格分隔）。",
        "constraints_md": "- 2 ≤ n ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · Python",
        "reference_solution": "import sys\n\nn = int(sys.stdin.read())\ncomp = bytearray(n + 1)          # bytearray 当布尔数组，省内存速度快\ncnt = 0\nlargest = 0\nfor i in range(2, n + 1):\n    if not comp[i]:\n        cnt += 1\n        largest = i\n        comp[i * i::i] = b\"\\x01\" * len(comp[i * i::i])\nprint(cnt, largest)\n",
        "alt_solution": "import sys\n\nn = int(sys.stdin.read())\ncomp = [False] * (n + 1)\nprimes = []\nfor i in range(2, n + 1):\n    if not comp[i]:\n        primes.append(i)\n    for p in primes:             # 线性（欧拉）筛：每个合数只被最小素因子筛一次\n        if i * p > n:\n            break\n        comp[i * p] = True\n        if i % p == 0:\n            break\nprint(len(primes), primes[-1])\n",
        "cases": [
            {
                "stdin": "2\n",
                "expected_stdout": "1 2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "10\n",
                "expected_stdout": "4 7\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "100\n",
                "expected_stdout": "25 97\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10000\n",
                "expected_stdout": "1229 9973\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1000000\n",
                "expected_stdout": "78498 999983\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    }
]
