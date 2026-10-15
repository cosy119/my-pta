# -*- coding: utf-8 -*-
"""题库扩展（第三批）：第 12 讲 文件 / 第 13 讲 异常 / 第 14 讲 综合案例。

与 `problems_bank.py` / `problems_bank_ext.py` 同一套约定：

1. **顺序跟讲义走** —— Python 讲义已 01~14 全部完结，本批复跑 12~14 三讲
2. **期望输出独立算** —— 本文件全部 `expected_stdout` 由 **node 独立实现**
   预先算出（`data/_oracle_py_new.js`，另一语言另一套算法），参考解只负责「撞」它
3. **每题带 `alt_solution`** —— 参考解与第二套实现都要通过全部测试点
4. 覆盖讲次考点：12 讲（逐行处理/分隔解析/wc 三件套/读统一写加回）、
   13 讲（ValueError/ZeroDivisionError 分支、自定义异常、负索引语义、else/finally）、
   14 讲（综合：字典+排序+格式化+格式互换）
"""
from __future__ import annotations

EXT2_PROBLEMS: list[dict] = [
    # ================================================================== #
    # 第 12 讲 · 文件
    # ================================================================== #
    {
        "title": "wc 三件套",
        "line": "python",
        "question_type": "programming",
        "difficulty": 1,
        "total_score": 10,
        "tags": ["第12讲·文件", "逐行处理", "splitlines"],
        "source_section": "第 12 讲 · 文件",
        "statement_md": (
            "从标准输入读入**若干行文本**（直到 EOF），统计并输出三个数：\n\n"
            "1. **行数**（按行算，最后一行末尾没有换行符也算一行）\n"
            "2. **单词数**（以空白分隔的段；只由空白组成的行贡献 0 个单词）\n"
            "3. **字符数**（所有行的字符总数，**不含行尾换行符**，含空格和制表符）\n\n"
            "这正是 Linux `wc -l -w -c` 三件套的 Python 实现 —— "
            "考点是 `splitlines()` 与「剥行尾换行」的区别。"
        ),
        "input_format": "若干行文本（可能为空，即 0 行）。",
        "output_format": "一行：`行数 单词数 字符数`，用空格分隔。",
        "constraints_md": "- 总输入 ≤ 10^4 行，每行 ≤ 200 字符",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "data = sys.stdin.read()\n"
            "lines = data.splitlines()          # 按行切，自动不带走行尾换行\n"
            "print(len(lines), len(data.split()), sum(len(l) for l in lines))\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "n_lines = n_words = n_chars = 0\n"
            "for line in sys.stdin:             # 逐行迭代（文件对象迭代是第 12 讲考点）\n"
            "    l = line.rstrip('\\n')          # ★ 只剥行尾换行，内容里的空白不能动\n"
            "    n_lines += 1\n"
            "    n_words += len(l.split())\n"
            "    n_chars += len(l)\n"
            "print(n_lines, n_words, n_chars)\n"
        ),
        "cases": [
            {"stdin": "hello world\nfoo bar baz\n\nlast\n",
             "expected_stdout": "4 6 26\n", "is_sample": 1, "kind": "sample",
             "explanation": "4 行；单词 hello/world/foo/bar/baz/last 共 6 个；字符 11+11+0+4=26"},
            {"stdin": "single line here\n", "expected_stdout": "1 3 16\n",
             "kind": "manual", "explanation": "最后一行的换行符不算字符"},
            {"stdin": "\n\n\n", "expected_stdout": "3 0 0\n", "kind": "manual",
             "explanation": "三行全空：行数照算，单词与字符都是 0"},
            {"stdin": "", "expected_stdout": "0 0 0\n", "kind": "manual",
             "explanation": "空输入：三个 0"},
            {"stdin": "  spaced\t content  \n", "expected_stdout": "1 2 19\n",
             "kind": "manual", "explanation": "字符数含首尾空格与制表符（19 个），单词只按空白切段"},
        ],
    },
    {
        "title": "CSV 成绩排名",
        "line": "python",
        "question_type": "programming",
        "difficulty": 2,
        "total_score": 15,
        "tags": ["第12讲·文件", "CSV 解析", "稳定排序"],
        "source_section": "第 12 讲 · 文件",
        "statement_md": (
            "读入 `n` 名学生的成绩行（CSV 逗号分隔），按**总分降序**输出成绩单。\n\n"
            "★ **同分必须按输入顺序**（先录入的在前）—— 这是对「稳定排序」的直接考察，"
            "`sorted()` 天然稳定，千万别用 `Counter.most_common()` 之类的另立门户。"
        ),
        "input_format": (
            "第一行整数 `n`；接下来 `n` 行，每行 `姓名,语文,数学,英语`，"
            "三科成绩均为 0~100 的整数（**固定三科**）。"
        ),
        "output_format": "n 行：`姓名 总分 平均分`，平均分保留 1 位小数。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 姓名不含逗号与空格，长度 ≤ 20",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "data = sys.stdin.read().splitlines()\n"
            "n = int(data[0])\n"
            "rows = []\n"
            "for i in range(1, n + 1):\n"
            "    name, cn, ma, en = data[i].split(',')\n"
            "    rows.append((name, int(cn) + int(ma) + int(en)))\n"
            "rows.sort(key=lambda r: -r[1])     # 稳定排序：同分保持输入顺序\n"
            "for name, total in rows:\n"
            "    print(name, total, '%.1f' % (total / 3))\n"
        ),
        "alt_solution": (
            "import sys\n"
            "from operator import itemgetter\n\n"
            "lines = sys.stdin.read().splitlines()\n"
            "n = int(lines[0])\n"
            "recs = []\n"
            "for idx, row in enumerate(lines[1:n + 1]):\n"
            "    name, a, b, c = row.split(',')\n"
            "    recs.append([name, int(a) + int(b) + int(c), idx])\n"
            "recs.sort(key=itemgetter(1), reverse=True)   # 稳定 → idx 决定同分先后\n"
            "sys.stdout.write(''.join('%s %d %.1f\\n' % (r[0], r[1], r[1] / 3) for r in recs))\n"
        ),
        "cases": [
            {"stdin": "3\nTom,90,85,88\nJerry,100,60,90\nAlice,85,92,91\n",
             "expected_stdout": "Alice 268 89.3\nTom 263 87.7\nJerry 250 83.3\n",
             "is_sample": 1, "kind": "sample", "explanation": "按总分降序；268/3=89.333→89.3"},
            {"stdin": "2\nBob,80,80,80\nAmy,80,80,80\n",
             "expected_stdout": "Bob 240 80.0\nAmy 240 80.0\n",
             "kind": "manual", "explanation": "同分 240：Bob 先录入在前（稳定排序）"},
            {"stdin": "1\nZhang,0,0,1\n", "expected_stdout": "Zhang 1 0.3\n",
             "kind": "manual", "explanation": "1/3=0.333→0.3"},
            {"stdin": "2\nA,100,100,100\nB,99,100,100\n",
             "expected_stdout": "A 300 100.0\nB 299 99.7\n",
             "kind": "manual", "explanation": "299/3=99.666→99.7"},
        ],
    },
    {
        "title": "提取错误日志",
        "line": "python",
        "question_type": "programming",
        "difficulty": 1,
        "total_score": 10,
        "tags": ["第12讲·文件", "逐行处理", "enumerate"],
        "source_section": "第 12 讲 · 文件",
        "statement_md": (
            "日志过滤器：读入若干行日志，每行格式固定为\n"
            "`日期 时间 级别 消息`（单空格分隔，级别 ∈ {INFO, WARN, ERROR}）。\n\n"
            "把**所有 ERROR 行**原样输出，并在前面带上行号（从 1 计）：\n"
            "`第<行号>行: <原行>`。一行 ERROR 都没有时输出 `无错误`。"
        ),
        "input_format": "若干行日志（可能为空）。",
        "output_format": "见题面；无 ERROR 时输出 `无错误`。",
        "constraints_md": "- 行数 ≤ 1000，每行 ≤ 200 字符",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "found = False\n"
            "for no, line in enumerate(sys.stdin.read().splitlines(), start=1):\n"
            "    if line.split(' ')[2] == 'ERROR':\n"
            "        print('第%d行: %s' % (no, line))\n"
            "        found = True\n"
            "if not found:\n"
            "    print('无错误')\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "hits = ['第%d行: %s' % (no, line)\n"
            "        for no, line in enumerate(sys.stdin.read().splitlines(), 1)\n"
            "        if line.split(' ')[2] == 'ERROR']\n"
            "sys.stdout.write('\\n'.join(hits) if hits else '无错误')\n"
            "sys.stdout.write('\\n')\n"
        ),
        "cases": [
            {"stdin": "2026-10-15 09:00:00 INFO start\n2026-10-15 09:01:00 ERROR disk full\n"
                      "2026-10-15 09:02:00 WARN slow\n2026-10-15 09:03:00 ERROR retry fail\n",
             "expected_stdout": "第2行: 2026-10-15 09:01:00 ERROR disk full\n"
                                "第4行: 2026-10-15 09:03:00 ERROR retry fail\n",
             "is_sample": 1, "kind": "sample", "explanation": "第 2、4 行是 ERROR，原样带行号输出"},
            {"stdin": "2026-10-15 08:00:00 INFO ok\n", "expected_stdout": "无错误\n",
             "kind": "manual", "explanation": "没有 ERROR 行"},
            {"stdin": "", "expected_stdout": "无错误\n", "kind": "manual",
             "explanation": "空输入也算「无错误」"},
        ],
    },
    {
        "title": "倒序输出文本行",
        "line": "python",
        "question_type": "programming",
        "difficulty": 1,
        "total_score": 10,
        "tags": ["第12讲·文件", "splitlines", "读统一"],
        "source_section": "第 12 讲 · 文件",
        "statement_md": (
            "把输入的文本**按行逆序**输出（行为单位倒过来，每行内容原样保留，"
            "包括空行，不要 strip 行内空白）。\n\n"
            "这就是 `tac` 命令做的事。陷阱在「读入时怎么剥换行」："
            "`readlines()` 的每行自带 `\\n`，`rstrip('\\n')` 与 `rstrip()` 一字之差结果天壤之别。"
        ),
        "input_format": "若干行文本（至少 1 行；最后一行可能没有换行符）。",
        "output_format": "按行逆序输出。",
        "constraints_md": "- 行数 ≤ 10^4，每行 ≤ 200 字符\n- 行内可能有连续空格，必须原样保留",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "lines = sys.stdin.read().splitlines()   # 读统一：换行符已消失\n"
            "sys.stdout.write('\\n'.join(reversed(lines)))\n"
            "if lines:\n"
            "    sys.stdout.write('\\n')\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "lines = sys.stdin.readlines()      # 每行自带 \\n\n"
            "out = [line.rstrip('\\n') for line in reversed(lines)]   # ★ 只剥 \\n\n"
            "sys.stdout.write('\\n'.join(out) + ('\\n' if out else ''))\n"
        ),
        "cases": [
            {"stdin": "a\nb\nc\n", "expected_stdout": "c\nb\na\n",
             "is_sample": 1, "kind": "sample", "explanation": "三行倒过来"},
            {"stdin": "first\n\nlast", "expected_stdout": "last\n\nfirst\n",
             "kind": "manual", "explanation": "中间空行原样保留；末行无换行符也算一行"},
            {"stdin": "\n\n", "expected_stdout": "\n\n",
             "kind": "manual", "explanation": "两个空行，倒序后还是两个空行"},
        ],
    },
    {
        "title": "最长的一行",
        "line": "python",
        "question_type": "programming",
        "difficulty": 1,
        "total_score": 10,
        "tags": ["第12讲·文件", "迭代与max"],
        "source_section": "第 12 讲 · 文件",
        "statement_md": (
            "读入若干行（至少 1 行），输出**最长的一行**：\n\n"
            "第一行输出它的长度（字符数，不含行尾换行符），第二行输出该行内容。\n"
            "若最长的有多行，**输出最先出现的那行**（`max` 并列时恰好取先出现的，"
            "但你要能说清为什么）。"
        ),
        "input_format": "若干行文本（至少 1 行）。",
        "output_format": "两行：长度与内容。",
        "constraints_md": "- 行数 ≤ 10^4，每行 ≤ 1000 字符",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "lines = sys.stdin.read().splitlines()\n"
            "best = max(lines, key=len)     # 并列取先出现：max 遇到等长不替换\n"
            "print(len(best))\n"
            "print(best)\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "lines = sys.stdin.read().splitlines()\n"
            "best = lines[0]\n"
            "for l in lines:                # 手写循环：严格大于才换，并列自然保先\n"
            "    if len(l) > len(best):\n"
            "        best = l\n"
            "sys.stdout.write('%d\\n%s\\n' % (len(best), best))\n"
        ),
        "cases": [
            {"stdin": "hi\nhello world\nhey\n", "expected_stdout": "11\nhello world\n",
             "is_sample": 1, "kind": "sample", "explanation": "hello world 11 字符"},
            {"stdin": "abcd\nxy\nabcd\n", "expected_stdout": "4\nabcd\n",
             "kind": "manual", "explanation": "两行并列 4：取最先出现的"},
            {"stdin": "onlyone\n", "expected_stdout": "7\nonlyone\n",
             "kind": "manual", "explanation": "只有一行"},
        ],
    },
    # ================================================================== #
    # 第 13 讲 · 异常
    # ================================================================== #
    {
        "title": "安全整数求和",
        "line": "python",
        "question_type": "programming",
        "difficulty": 1,
        "total_score": 10,
        "tags": ["第13讲·异常", "ValueError", "容错"],
        "source_section": "第 13 讲 · 异常",
        "statement_md": (
            "读入一行若干个 token（空格分隔），把其中**能当成整数**的加起来。\n"
            "解析失败的 token（如 `abc`、`3.5`、`12x`）**跳过并计数**。\n\n"
            "输出 `总和 跳过数`。考点：`int()` 抛 `ValueError`，"
            "而 `\"-5\"`、`\"+7\"`、`\"007\"` 都是**合法**整数。"
        ),
        "input_format": "一行，若干个 token（可能为空行）。",
        "output_format": "一行：`总和 跳过数`。",
        "constraints_md": "- token 数 ≤ 1000\n- token 只含 ASCII；合法整数绝对值 ≤ 10^9",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "total = skipped = 0\n"
            "for tok in sys.stdin.read().split():\n"
            "    try:\n"
            "        total += int(tok)       # 只有整数能进来\n"
            "    except ValueError:          # abc / 3.5 / 12x 全在这落网\n"
            "        skipped += 1\n"
            "print(total, skipped)\n"
        ),
        "alt_solution": (
            "import sys\n"
            "import re\n\n"
            "INT = re.compile(r'^[+-]?\\d+$')    # 手工版 int 解析器（负号/正号/前导零）\n"
            "total = skipped = 0\n"
            "for tok in sys.stdin.read().split():\n"
            "    if INT.match(tok):\n"
            "        total += int(tok)\n"
            "    else:\n"
            "        skipped += 1\n"
            "print(total, skipped)\n"
        ),
        "cases": [
            {"stdin": "12 abc -5 3.5 +7 007 12x\n", "expected_stdout": "21 3\n",
             "is_sample": 1, "kind": "sample",
             "explanation": "12+(-5)+7+7=21；abc/3.5/12x 跳过 3 个；+7 与 007 是合法整数"},
            {"stdin": "1 2 3\n", "expected_stdout": "6 0\n", "kind": "manual",
             "explanation": "全部合法"},
            {"stdin": "x y z\n", "expected_stdout": "0 3\n", "kind": "manual",
             "explanation": "全军覆没：总和 0，跳过 3"},
            {"stdin": "", "expected_stdout": "0 0\n", "kind": "manual",
             "explanation": "空行：没有 token"},
        ],
    },
    {
        "title": "除法分类器",
        "line": "python",
        "question_type": "programming",
        "difficulty": 2,
        "total_score": 15,
        "tags": ["第13讲·异常", "异常分支顺序", "ZeroDivisionError"],
        "source_section": "第 13 讲 · 异常",
        "statement_md": (
            "处理 `n` 组 `a b`。对每组按顺序判定并输出**一个**结果：\n\n"
            "1. `a` 或 `b` 不是整数 → `INVALID`（如 `x`、`2.5`）\n"
            "2. 否则若 `b == 0` → `DIV0`\n"
            "3. 否则输出 **商向下取整**（Python 的 `//`，`-7 // 2 == -4`，不是向零截断）\n\n"
            "考点：两类异常要**分开两个 except**，且 `INVALID` 的判定必须发生在除法之前。"
        ),
        "input_format": "第一行整数 `n`；接下来 `n` 行，每行两个 token 用空格分隔。",
        "output_format": "n 行，每行一个结果。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 合法整数绝对值 ≤ 10^9",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "data = sys.stdin.read().splitlines()\n"
            "n = int(data[0])\n"
            "out = []\n"
            "for i in range(1, n + 1):\n"
            "    a, b = data[i].split(' ')\n"
            "    try:\n"
            "        x = int(a)\n"
            "        y = int(b)\n"
            "    except ValueError:          # 先判输入合法性\n"
            "        out.append('INVALID')\n"
            "        continue\n"
            "    try:\n"
            "        out.append(str(x // y))\n"
            "    except ZeroDivisionError:   # 再判除零\n"
            "        out.append('DIV0')\n"
            "print('\\n'.join(out))\n"
        ),
        "alt_solution": (
            "import sys\n"
            "import re\n\n"
            "INT = re.compile(r'^[+-]?\\d+$')\n"
            "lines = sys.stdin.read().splitlines()\n"
            "res = []\n"
            "for row in lines[1:int(lines[0]) + 1]:\n"
            "    a, b = row.split(' ')\n"
            "    if INT.match(a) and INT.match(b):    # 先验后算，try 只留给除零\n"
            "        x, y = int(a), int(b)\n"
            "        try:\n"
            "            res.append(str(x // y))\n"
            "        except ZeroDivisionError:\n"
            "            res.append('DIV0')\n"
            "    else:\n"
            "        res.append('INVALID')\n"
            "sys.stdout.write('\\n'.join(res) + '\\n')\n"
        ),
        "cases": [
            {"stdin": "5\n7 2\n-7 2\n7 0\nx 2\n7 2.5\n",
             "expected_stdout": "3\n-4\nDIV0\nINVALID\nINVALID\n",
             "is_sample": 1, "kind": "sample",
             "explanation": "-7//2 = -4（向下取整，不是 -3）；x 与 2.5 都不是整数"},
            {"stdin": "3\n0 5\n+9 3\n-8 -4\n", "expected_stdout": "0\n3\n2\n",
             "kind": "manual", "explanation": "+9 是合法整数；-8//-4=2"},
            {"stdin": "1\n10 007\n", "expected_stdout": "1\n",
             "kind": "manual", "explanation": "007 解析成 7；10//7=1"},
        ],
    },
    {
        "title": "成绩录入校验",
        "line": "python",
        "question_type": "programming",
        "difficulty": 2,
        "total_score": 15,
        "tags": ["第13讲·异常", "自定义异常", "raise"],
        "source_section": "第 13 讲 · 异常",
        "statement_md": (
            "录入 `n` 条 `姓名 分数`。分数必须是 **0~100 的整数**，"
            "否则拒绝该条。\n\n"
            "输出 `n` 行：有效 → `姓名 分数`；无效 → `姓名 拒绝`；"
            "最后一行输出 `有效 m 人`。\n\n"
            "建议定义 `InvalidScoreError`（第 11 讲继承 + 第 13 讲 raise）来组织代码，"
            "但**判题只看输出**，实现方式自由。注意 `59.9`、`-3`、`105`、`abc` 都算无效，"
            "而 `+50`、`007` 是合法整数。"
        ),
        "input_format": "第一行整数 `n`；接下来 `n` 行 `姓名 分数`（姓名不含空格）。",
        "output_format": "见题面。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 姓名长度 ≤ 20，分数 token 长度 ≤ 10",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "class InvalidScoreError(Exception):\n"
            "    \"\"\"分数不是 0~100 的整数时抛出（第 11 讲继承 + 第 13 讲异常）\"\"\"\n\n"
            "def parse_score(text):\n"
            "    try:\n"
            "        v = int(text)\n"
            "    except ValueError:\n"
            "        raise InvalidScoreError('not an int')\n"
            "    if not 0 <= v <= 100:\n"
            "        raise InvalidScoreError('out of range')\n"
            "    return v\n\n"
            "data = sys.stdin.read().splitlines()\n"
            "n = int(data[0])\n"
            "out = []\n"
            "valid = 0\n"
            "for i in range(1, n + 1):\n"
            "    name, score_text = data[i].rsplit(' ', 1)\n"
            "    try:\n"
            "        v = parse_score(score_text)\n"
            "    except InvalidScoreError:\n"
            "        out.append(name + ' 拒绝')\n"
            "    else:\n"
            "        valid += 1\n"
            "        out.append('%s %d' % (name, v))\n"
            "out.append('有效 %d 人' % valid)\n"
            "print('\\n'.join(out))\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "def check(text):\n"
            "    \"\"\"不用异常的独立实现：合法返回 int，非法返回 None\"\"\"\n"
            "    t = text.lstrip('+-')\n"
            "    if not (t.isdigit() and t.isascii()):\n"
            "        return None\n"
            "    v = int(text)\n"
            "    return v if 0 <= v <= 100 else None\n\n"
            "lines = sys.stdin.read().splitlines()\n"
            "out = []\n"
            "valid = 0\n"
            "for row in lines[1:int(lines[0]) + 1]:\n"
            "    name, s = row.rsplit(' ', 1)\n"
            "    v = check(s)\n"
            "    if v is None:\n"
            "        out.append(name + ' 拒绝')\n"
            "    else:\n"
            "        valid += 1\n"
            "        out.append('%s %d' % (name, v))\n"
            "out.append('有效 %d 人' % valid)\n"
            "sys.stdout.write('\\n'.join(out) + '\\n')\n"
        ),
        "cases": [
            {"stdin": "4\nTom 85\nJerry -3\nAmy 105\nBob abc\n",
             "expected_stdout": "Tom 85\nJerry 拒绝\nAmy 拒绝\nBob 拒绝\n有效 1 人\n",
             "is_sample": 1, "kind": "sample", "explanation": "-3 越界、105 越界、abc 非整数"},
            {"stdin": "3\n张三 0\n李四 100\n王五 59.9\n",
             "expected_stdout": "张三 0\n李四 100\n王五 拒绝\n有效 2 人\n",
             "kind": "manual", "explanation": "边界 0 与 100 都合法；59.9 不是整数"},
            {"stdin": "2\nA +50\nB 007\n", "expected_stdout": "A 50\nB 7\n有效 2 人\n",
             "kind": "manual", "explanation": "+50 与 007 都是合法整数（输出规范化后的值）"},
        ],
    },
    {
        "title": "列表操作与异常分类",
        "line": "python",
        "question_type": "programming",
        "difficulty": 3,
        "total_score": 20,
        "tags": ["第13讲·异常", "IndexError", "负索引"],
        "source_section": "第 13 讲 · 异常",
        "statement_md": (
            "初始列表 `lst = [10, 20, 30]`。按序处理 `n` 条指令并**立刻**输出每条的结果：\n\n"
            "- `get i` → 输出 `lst[i]`\n"
            "- `pop i` → 弹出并输出 `lst[i]`\n"
            "- `add x` → 把整数 x 追加到列表尾（**不输出**）\n\n"
            "错误分两类：参数不是整数 → 输出 `E2`（**先判**，add 也不例外）；"
            "索引越界 → 输出 `E1`。\n\n"
            "★ **Python 负索引是合法语义**：`get -1` 取最后一个元素。"
            "但越界的负索引（如长度 3 时 `get -9`）照样是 `E1`。"
            "`add` 成功时什么都不输出 —— 别手滑多打一个 OK。"
        ),
        "input_format": "第一行整数 `n`；接下来 `n` 行指令。",
        "output_format": "每条 get/pop 输出一行（值或 E1/E2）；add 无输出。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 整数参数绝对值 ≤ 10^9（可能越界）",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "data = sys.stdin.read().splitlines()\n"
            "n = int(data[0])\n"
            "lst = [10, 20, 30]\n"
            "out = []\n"
            "for i in range(1, n + 1):\n"
            "    parts = data[i].split(' ')\n"
            "    op = parts[0]\n"
            "    try:\n"
            "        idx = int(parts[1])\n"
            "    except ValueError:          # 参数不是整数：先于一切判\n"
            "        out.append('E2')\n"
            "        continue\n"
            "    try:\n"
            "        if op == 'get':\n"
            "            out.append(str(lst[idx]))      # 负索引是合法 Python 语义\n"
            "        elif op == 'pop':\n"
            "            out.append(str(lst.pop(idx)))\n"
            "        else:                              # add：不输出\n"
            "            lst.append(idx)\n"
            "    except IndexError:\n"
            "        out.append('E1')\n"
            "print('\\n'.join(out))\n"
        ),
        "alt_solution": (
            "import sys\n"
            "import re\n\n"
            "INT = re.compile(r'^[+-]?\\d+$')\n"
            "data = sys.stdin.read().splitlines()\n"
            "lst = [10, 20, 30]\n"
            "res = []\n"
            "for row in data[1:int(data[0]) + 1]:\n"
            "    op, arg = (row.split(' ') + [None])[:2]\n"
            "    if arg is not None and not INT.match(arg):\n"
            "        res.append('E2')\n"
            "        continue\n"
            "    k = int(arg) if arg is not None else 0\n"
            "    if op == 'add':\n"
            "        lst.append(k)\n"
            "        continue\n"
            "    j = k + len(lst) if k < 0 else k         # 手工实现负索引\n"
            "    if 0 <= j < len(lst):\n"
            "        res.append(str(lst[j]))\n"
            "        if op == 'pop':\n"
            "            del lst[j]\n"
            "    else:\n"
            "        res.append('E1')\n"
            "sys.stdout.write('\\n'.join(res) + ('\\n' if res else ''))\n"
        ),
        "cases": [
            {"stdin": "7\nget 0\nget -1\npop 5\nadd 40\nget 3\npop x\nget 1\n",
             "expected_stdout": "10\n30\nE1\n40\nE2\n20\n",
             "is_sample": 1, "kind": "sample",
             "explanation": "get -1 合法取 30；pop 5 越界 E1；pop x 参数非整数 E2"},
            {"stdin": "4\npop 0\npop 0\npop 0\npop 0\n",
             "expected_stdout": "10\n20\n30\nE1\n",
             "kind": "manual", "explanation": "弹空之后才越界"},
            {"stdin": "2\nadd 99\nget -1\n", "expected_stdout": "99\n",
             "kind": "manual", "explanation": "add 不输出；get -1 取到刚加的 99"},
        ],
    },
    {
        "title": "批处理报告",
        "line": "python",
        "question_type": "programming",
        "difficulty": 2,
        "total_score": 15,
        "tags": ["第13讲·异常", "else与finally", "float"],
        "source_section": "第 13 讲 · 异常",
        "statement_md": (
            "处理 `n` 行 `a b`：若 `a`、`b` 都能当成浮点数且 `b != 0`，"
            "输出 `a / b` **保留 1 位小数**；`b == 0` → `ZDIV`；其余 → `ERR`。\n"
            "全部处理完后输出一行统计 `ok=<成功数> fail=<失败数>`。\n\n"
            "建议用 try / except / **else** / **finally** 组织：成功输出放 `else`，"
            "计数兜底放 `finally` —— 判题只看输出，但这题就是为练这套结构设计的。"
        ),
        "input_format": "第一行整数 `n`；接下来 `n` 行，每行两个 token。",
        "output_format": "n 行结果 + 1 行统计。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 合法浮点数形如 3、3.6、-1（不含科学计数法）",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "data = sys.stdin.read().splitlines()\n"
            "n = int(data[0])\n"
            "ok = 0\n"
            "out = []\n"
            "for i in range(1, n + 1):\n"
            "    try:\n"
            "        a, b = data[i].split(' ')\n"
            "        x = float(a)\n"
            "        y = float(b)\n"
            "        q = x / y               # y 为 0 在这炸\n"
            "    except ZeroDivisionError:\n"
            "        out.append('ZDIV')\n"
            "    except ValueError:          # 放后面也行：两类异常不重叠\n"
            "        out.append('ERR')\n"
            "    else:                       # 只有没有异常才走 else\n"
            "        out.append('%.1f' % q)\n"
            "        ok += 1\n"
            "out.append('ok=%d fail=%d' % (ok, n - ok))\n"
            "print('\\n'.join(out))\n"
        ),
        "alt_solution": (
            "import sys\n"
            "import re\n\n"
            "NUM = re.compile(r'^[+-]?(\\d+\\.?\\d*|\\.\\d+)$')\n"
            "lines = sys.stdin.read().splitlines()\n"
            "ok = 0\n"
            "out = []\n"
            "for row in lines[1:int(lines[0]) + 1]:\n"
            "    a, b = row.split(' ')\n"
            "    if not (NUM.match(a) and NUM.match(b)):\n"
            "        out.append('ERR')\n"
            "        continue\n"
            "    y = float(b)\n"
            "    if y == 0:\n"
            "        out.append('ZDIV')\n"
            "    else:\n"
            "        out.append('%.1f' % (float(a) / y))\n"
            "        ok += 1\n"
            "out.append('ok=%d fail=%d' % (ok, int(lines[0]) - ok))\n"
            "sys.stdout.write('\\n'.join(out) + '\\n')\n"
        ),
        "cases": [
            {"stdin": "4\n8 4\n7 0\nx 2\n3.6 2\n",
             "expected_stdout": "2.0\nZDIV\nERR\n1.8\nok=2 fail=2\n",
             "is_sample": 1, "kind": "sample", "explanation": "四条路径各走一遍"},
            {"stdin": "3\n10 3\n-1 3\nabc 1\n",
             "expected_stdout": "3.3\n-0.3\nERR\nok=2 fail=1\n",
             "kind": "manual", "explanation": "-1/3=-0.333→-0.3（向下不向上）"},
            {"stdin": "2\n7 5\n9 3\n", "expected_stdout": "1.4\n3.0\nok=2 fail=0\n",
             "kind": "manual", "explanation": "9/3 输出 3.0 而不是 3"},
        ],
    },
    # ================================================================== #
    # 第 14 讲 · 综合案例
    # ================================================================== #
    {
        "title": "班级成绩统计",
        "line": "python",
        "question_type": "programming",
        "difficulty": 3,
        "total_score": 20,
        "tags": ["第14讲·综合案例", "字典与列表", "格式化"],
        "source_section": "第 14 讲 · 综合案例",
        "statement_md": (
            "全班的成绩单处理（第 14 讲案例的统计层）：\n\n"
            "输入 `n` 名学生、`m` 门课；每人一行 `姓名 分1 .. 分m`。\n\n"
            "输出：\n"
            "1. `n` 行 `姓名 总分 均分`，按总分降序，**同分按输入顺序**（均分保留 1 位小数）\n"
            "2. 一行 `课程均分 c1 .. cm`（每门课全班平均，保留 1 位小数）\n"
            "3. 一行 `最高 姓名`（总分最高的学生，数据保证唯一）"
        ),
        "input_format": "第一行 `n m`；接下来 `n` 行 `姓名 分1 .. 分m`（整数 0~100）。",
        "output_format": "见题面。",
        "constraints_md": "- 1 ≤ n, m ≤ 50\n- 总分最高者唯一",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "data = sys.stdin.read().splitlines()\n"
            "n, m = map(int, data[0].split())\n"
            "students = []\n"
            "col = [0] * m\n"
            "for i in range(1, n + 1):\n"
            "    parts = data[i].split(' ')\n"
            "    scores = [int(v) for v in parts[1:1 + m]]\n"
            "    for j, v in enumerate(scores):\n"
            "        col[j] += v\n"
            "    students.append((parts[0], sum(scores)))\n"
            "order = sorted(range(n), key=lambda k: (-students[k][1], k))\n"
            "for k in order:\n"
            "    name, total = students[k]\n"
            "    print(name, total, '%.1f' % (total / m))\n"
            "print('课程均分 ' + ' '.join('%.1f' % (c / n) for c in col))\n"
            "print('最高 ' + students[order[0]][0])\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "lines = sys.stdin.read().splitlines()\n"
            "n, m = map(int, lines[0].split())\n"
            "recs = []\n"
            "for idx, row in enumerate(lines[1:n + 1]):\n"
            "    p = row.split(' ')\n"
            "    sc = list(map(int, p[1:]))\n"
            "    recs.append([p[0], sum(sc), idx])\n"
            "recs.sort(key=lambda r: (-r[1], r[2]))\n"
            "out = ['%s %d %.1f' % (r[0], r[1], r[1] / m) for r in recs]\n"
            "col = [sum(int(row.split(' ')[j]) for row in lines[1:n + 1]) / n\n"
            "       for j in range(1, m + 1)]            # 列向求均分（转置思路）\n"
            "out.append('课程均分 ' + ' '.join('%.1f' % c for c in col))\n"
            "out.append('最高 ' + recs[0][0])\n"
            "sys.stdout.write('\\n'.join(out) + '\\n')\n"
        ),
        "cases": [
            {"stdin": "3 3\nTom 90 85 88\nJerry 100 60 90\nAlice 85 92 91\n",
             "expected_stdout": "Alice 268 89.3\nTom 263 87.7\nJerry 250 83.3\n"
                               "课程均分 91.7 79.0 89.7\n最高 Alice\n",
             "is_sample": 1, "kind": "sample",
             "explanation": "课程均分按列求：(90+100+85)/3=91.7"},
            {"stdin": "2 3\nA 50 50 50\nB 51 50 50\n",
             "expected_stdout": "B 151 50.3\nA 150 50.0\n课程均分 50.5 50.0 50.0\n最高 B\n",
             "kind": "manual", "explanation": "语文列 (50+51)/2=50.5"},
        ],
    },
    {
        "title": "通讯录操作模拟",
        "line": "python",
        "question_type": "programming",
        "difficulty": 2,
        "total_score": 15,
        "tags": ["第14讲·综合案例", "字典", "KeyError"],
        "source_section": "第 14 讲 · 综合案例",
        "statement_md": (
            "通讯录的命令行版（第 14 讲案例的业务层）：依次处理 `n` 条操作并输出结果：\n\n"
            "- `add 姓名 电话` → 存入（同名覆盖），输出 `OK`\n"
            "- `find 姓名` → 存在输出电话，否则 `NOT FOUND`\n"
            "- `del 姓名` → 存在删除并输出 `DELETED`，否则 `NOT FOUND`（试试 `del d[k]` 配 try/except KeyError）\n"
            "- `list` → 按**姓名升序**输出 `姓名:电话`，逗号分隔；空表输出 `(empty)`"
        ),
        "input_format": "第一行整数 `n`；接下来 `n` 行操作。",
        "output_format": "每条操作输出一行（list 可能很长）。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 姓名/电话均不含空格，姓名 ≤ 20 字符",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "data = sys.stdin.read().splitlines()\n"
            "n = int(data[0])\n"
            "book = {}\n"
            "out = []\n"
            "for i in range(1, n + 1):\n"
            "    parts = data[i].split(' ')\n"
            "    op = parts[0]\n"
            "    if op == 'add':\n"
            "        book[parts[1]] = parts[2]\n"
            "        out.append('OK')\n"
            "    elif op == 'find':\n"
            "        out.append(book.get(parts[1], 'NOT FOUND'))\n"
            "    elif op == 'del':\n"
            "        try:\n"
            "            del book[parts[1]]      # 不存在在这炸 KeyError\n"
            "            out.append('DELETED')\n"
            "        except KeyError:\n"
            "            out.append('NOT FOUND')\n"
            "    else:                           # list\n"
            "        out.append(','.join('%s:%s' % (k, book[k]) for k in sorted(book)) or '(empty)')\n"
            "print('\\n'.join(out))\n"
        ),
        "alt_solution": (
            "import sys\n\n"
            "lines = sys.stdin.read().splitlines()\n"
            "book = {}\n"
            "res = []\n"
            "for row in lines[1:int(lines[0]) + 1]:\n"
            "    p = row.split(' ')\n"
            "    if p[0] == 'add':\n"
            "        book[p[1]] = p[2]\n"
            "        res.append('OK')\n"
            "    elif p[0] == 'find':\n"
            "        res.append(book[p[1]] if p[1] in book else 'NOT FOUND')\n"
            "    elif p[0] == 'del':\n"
            "        res.append(book.pop(p[1], None) is not None and 'DELETED' or 'NOT FOUND')\n"
            "    else:\n"
            "        keys = sorted(book)\n"
            "        res.append(','.join(k + ':' + book[k] for k in keys) if keys else '(empty)')\n"
            "sys.stdout.write('\\n'.join(res) + '\\n')\n"
        ),
        "cases": [
            {"stdin": "7\nadd Tom 110\nadd Jerry 120\nfind Tom\ndel Tom\nfind Tom\nlist\ndel Tom\n",
             "expected_stdout": "OK\nOK\n110\nDELETED\nNOT FOUND\nJerry:120\nNOT FOUND\n",
             "is_sample": 1, "kind": "sample", "explanation": "删两次：第二次 NOT FOUND"},
            {"stdin": "5\nadd B 2\nadd A 1\nlist\ndel C\nfind B\n",
             "expected_stdout": "OK\nOK\nA:1,B:2\nNOT FOUND\n2\n",
             "kind": "manual", "explanation": "list 按姓名升序"},
            {"stdin": "2\nlist\nadd X 9\n", "expected_stdout": "(empty)\nOK\n",
             "kind": "manual", "explanation": "空表输出 (empty)"},
        ],
    },
    {
        "title": "词频报告",
        "line": "python",
        "question_type": "programming",
        "difficulty": 2,
        "total_score": 15,
        "tags": ["第14讲·综合案例", "字典计数", "排序"],
        "source_section": "第 14 讲 · 综合案例",
        "statement_md": (
            "读入一段英文文本（词只由字母数字构成，空白分隔），输出四行报告：\n\n"
            "1. `total=<词数>`\n"
            "2. `unique=<不重复词数>`\n"
            "3. `freq=<出现≥2次的词>`，按**字典序升序**、逗号分隔；一个都没有则 `freq=-`\n"
            "4. `longest=<最长词>`；并列时取**字典序最小**"
        ),
        "input_format": "若干行文本（至少 1 个词）。",
        "output_format": "四行报告。",
        "constraints_md": "- 词数 ≤ 10^4，词长 ≤ 20，只含字母数字",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n\n"
            "words = sys.stdin.read().split()\n"
            "cnt = {}\n"
            "for w in words:\n"
            "    cnt[w] = cnt.get(w, 0) + 1\n"
            "freq = sorted(w for w, c in cnt.items() if c >= 2)\n"
            "longest = words[0]\n"
            "for w in words:\n"
            "    if len(w) > len(longest):\n"
            "        longest = w\n"
            "ties = sorted(w for w in cnt if len(w) == len(longest))\n"
            "print('total=%d' % len(words))\n"
            "print('unique=%d' % len(cnt))\n"
            "print('freq=' + (','.join(freq) if freq else '-'))\n"
            "print('longest=' + ties[0])\n"
        ),
        "alt_solution": (
            "import sys\n"
            "from collections import Counter\n\n"
            "words = sys.stdin.read().split()\n"
            "cnt = Counter(words)                # 换 API：Counter 计数\n"
            "freq = sorted(w for w, c in cnt.items() if c >= 2)\n"
            "top = max(map(len, cnt))\n"
            "ties = sorted(w for w in cnt if len(w) == top)\n"
            "sys.stdout.write('total=%d\\nunique=%d\\n' % (len(words), len(cnt)))\n"
            "sys.stdout.write('freq=%s\\n' % (','.join(freq) if freq else '-'))\n"
            "sys.stdout.write('longest=%s\\n' % ties[0])\n"
        ),
        "cases": [
            {"stdin": "apple banana apple cherry banana apple\n",
             "expected_stdout": "total=6\nunique=3\nfreq=apple,banana\nlongest=banana\n",
             "is_sample": 1, "kind": "sample", "explanation": "apple 3 次、banana 2 次进 freq；最长 banana 6 字母"},
            {"stdin": "dog cat\n", "expected_stdout": "total=2\nunique=2\nfreq=-\nlongest=cat\n",
             "kind": "manual", "explanation": "无重复词 → freq=-；并列 3 字母取字典序小的 cat"},
            {"stdin": "z z z a ab abc\n", "expected_stdout": "total=6\nunique=4\nfreq=z\nlongest=abc\n",
             "kind": "manual", "explanation": "只有 z 出现 ≥2 次"},
        ],
    },
    {
        "title": "CSV 转 JSON",
        "line": "python",
        "question_type": "programming",
        "difficulty": 3,
        "total_score": 20,
        "tags": ["第14讲·综合案例", "JSON", "类型转换"],
        "source_section": "第 14 讲 · 综合案例",
        "statement_md": (
            "把 CSV 表转成 JSON 数组（第 14 讲案例的格式互换层）：\n\n"
            "第一行是**表头**（逗号分隔的列名）；之后每行是一条记录，列数与表头一致。\n"
            "输出一行 JSON 数组：\n\n"
            "- 值若**完全由数字组成**（可带 `+`/`-` 号）→ 转成数字类型\n"
            "- 否则保留字符串\n"
            "- 格式与 `json.dumps(rows, ensure_ascii=False)` 完全一致："
            "键值对用 `, ` 分隔、键后 `: `，字符串用双引号"
        ),
        "input_format": "第一行表头；之后若干行数据（至少 1 行）。",
        "output_format": "一行 JSON 数组文本。",
        "constraints_md": "- 列数 ≤ 10，行数 ≤ 1000\n- 值不含逗号、双引号与反斜杠",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "reference_solution": (
            "import sys\n"
            "import json\n"
            "import re\n\n"
            "INT = re.compile(r'^[+-]?\\d+$')\n"
            "data = sys.stdin.read().splitlines()\n"
            "head = data[0].split(',')\n"
            "rows = []\n"
            "for line in data[1:]:\n"
            "    if not line:\n"
            "        continue\n"
            "    vals = line.split(',')\n"
            "    rec = {}\n"
            "    for h, v in zip(head, vals):\n"
            "        rec[h] = int(v) if INT.match(v) else v   # 数值列转 int\n"
            "    rows.append(rec)\n"
            "print(json.dumps(rows, ensure_ascii=False))\n"
        ),
        "alt_solution": (
            "import sys\n"
            "import re\n\n"
            "INT = re.compile(r'^[+-]?\\d+$')\n"
            "data = sys.stdin.read().splitlines()\n"
            "head = data[0].split(',')\n"
            "items = []\n"
            "for line in data[1:]:\n"
            "    if not line:\n"
            "        continue\n"
            "    vals = line.split(',')\n"
            "    pair = []\n"
            "    for h, v in zip(head, vals):\n"
            "        v = int(v) if INT.match(v) else v          # 不用 json 模块的独立拼装\n"
            "        s = str(v) if isinstance(v, int) else '\"%s\"' % v\n"
            "        pair.append('\"%s\": %s' % (h, s))\n"
            "    items.append('{' + ', '.join(pair) + '}')\n"
            "sys.stdout.write('[' + ', '.join(items) + ']\\n')\n"
        ),
        "cases": [
            {"stdin": "name,age,city\nTom,12,Beijing\nJerry,13,Xiamen\n",
             "expected_stdout": "[{\"name\": \"Tom\", \"age\": 12, \"city\": \"Beijing\"}, "
                                "{\"name\": \"Jerry\", \"age\": 13, \"city\": \"Xiamen\"}]\n",
             "is_sample": 1, "kind": "sample", "explanation": "age 是数字列，其余字符串"},
            {"stdin": "id,score,tag\n-5,3.5,ok\n7,x,hi\n",
             "expected_stdout": "[{\"id\": -5, \"score\": \"3.5\", \"tag\": \"ok\"}, "
                                "{\"id\": 7, \"score\": \"x\", \"tag\": \"hi\"}]\n",
             "kind": "manual", "explanation": "3.5 不是「纯数字」→ 保留字符串；-5、7 是整数"},
            {"stdin": "a\n42\n", "expected_stdout": "[{\"a\": 42}]\n",
             "kind": "manual", "explanation": "单行单列"},
        ],
    },
]
