# -*- coding: utf-8 -*-
"""Python 技巧特训题库生成器 —— 「技巧特训 · Python」分节。

定位：讲义里没专门讲、但做题（蓝桥杯 / 码蹄杯 / ACM 风格）总会遇到的
技巧性简便用法，单独成章，量大、循序渐进（difficulty 1 → 4）。

每道题：
  title / section / difficulty / score / tags
  statement_md / input_format / output_format / constraints_md
  inputs   ← 测试点输入（手写或生成）
  samples  ← 前几个当样例（其余为隐藏测试点）
  oracle   ← 独立 Python 实现，算期望输出（尽量用"笨办法"，与参考解不同路）
  solution / alt ← 两套 Python 实现（verify_bank 双撞）

章节结构：
  基础语法糖   8 题（upper / 负索引切片 / split-join / 推导式 / enumerate-zip /
               sorted 多关键字 / dict.get 词频 / 集合运算）
  竞赛工具箱   6 题（Counter / heapq / 前缀和 / bisect 第一个大于 x / lru_cache / 回文清洗）
  竞赛强度     6 题（01 背包 / LIS n log n / 快速幂 / 区间合并 / 阶乘大数 / 筛法）
  进阶技巧    10 题（ROT13 映射表 / 正则提取整数 / 格式化四连 / zip 转置 /
               第 k 个排列 / gcd-lcm / 位运算三连 / 子集枚举 / 二维前缀和 /
               单调队列滑窗最大值）
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "app" / "problems_bank_py_tricks.py"

PROBLEMS: list[dict] = []


def add(**kw) -> None:
    PROBLEMS.append(kw)


# --------------------------------------------------------------------- #
#  基础语法糖（difficulty 1~2）
# --------------------------------------------------------------------- #

def _oracle_01(text: str) -> str:
    s = text.rstrip("\n")
    letters = sum(1 for c in s if ("a" <= c <= "z") or ("A" <= c <= "Z"))
    digits = sum(1 for c in s if "0" <= c <= "9")
    up = ""
    low = ""
    for c in s:
        if "a" <= c <= "z":
            up += chr(ord(c) - 32)
            low += c
        elif "A" <= c <= "Z":
            up += c
            low += chr(ord(c) + 32)
        else:
            up += c
            low += c
    return "%s\n%s\n%d %d\n" % (up, low, letters, digits)

add(
    title="大小写与字符分类",
    section="技巧特训 · Python",
    difficulty=1, score=10, tags=["技巧特训", "字符串方法", "upper"],
    statement_md=(
        "读入一行字符串，输出三行：\n\n"
        "1. 全大写版本\n"
        "2. 全小写版本\n"
        "3. 字母个数 和 数字个数（空格分隔）\n\n"
        "★ 技巧点：字符串自带 `s.upper()` / `s.lower()` 一行搞定大小写；"
        "`c.isalpha()` / `c.isdigit()` 直接做字符分类——不用手写 ASCII 换算。"
        "非字母字符在 `upper()/lower()` 里保持原样。"
    ),
    input_format="一行字符串（长度 ≤ 1000，可含字母、数字、空格与标点）。",
    output_format="三行，如题面所述。",
    constraints_md="- 1 ≤ 字符串长度 ≤ 1000",
    inputs=[
        "Hello, World 123!\n",
        "abcXYZ\n",
        "12345\n",
        "!!!\n",
        "MiXeD 42abc\n",
    ],
    samples=2,
    oracle=_oracle_01,
    solution=r'''import sys

s = sys.stdin.readline().rstrip("\n")
print(s.upper())
print(s.lower())
letters = digits = 0
for ch in s:
    if ch.isalpha():
        letters += 1
    elif ch.isdigit():
        digits += 1
print(letters, digits)
''',
    alt=r'''import sys

s = sys.stdin.readline().rstrip("\n")
sys.stdout.write(s.upper() + "\n" + s.lower() + "\n")
print(sum(map(str.isalpha, s)), sum(map(str.isdigit, s)))
''',
)


def _oracle_02(text: str) -> str:
    s = text.rstrip("\n")
    n = len(s)
    last = s[n - 1]
    rev = ""
    for i in range(n - 1, -1, -1):
        rev += s[i]
    if n >= 2:
        mid = s[1:n - 1]
    else:
        mid = "EMPTY"
    return "%s\n%s\n%s\n" % (last, rev, mid)

add(
    title="负索引与切片反转",
    section="技巧特训 · Python",
    difficulty=1, score=10, tags=["技巧特训", "切片", "负索引"],
    statement_md=(
        "读入一行**不含空格**的字符串，输出三行：\n\n"
        "1. 最后一个字符\n"
        "2. 反转后的字符串\n"
        "3. 去掉首尾各一个字符后的字符串（长度不足 2 输出 `EMPTY`）\n\n"
        "★ 技巧点：`s[-1]` 直取最后一个字符；`s[::-1]` 一步反转；"
        "`s[1:-1]` 掐头去尾——这三个负索引/切片写法是 Python 的招牌，"
        "C 里要手写下标运算好几行。"
    ),
    input_format="一行字符串（长度 1 ≤ len ≤ 1000，不含空格）。",
    output_format="三行，如题面所述。",
    constraints_md="- 1 ≤ len ≤ 1000",
    inputs=[
        "abcdefg\n",
        "a\n",
        "ab\n",
        "racecar\n",
        "12345\n",
    ],
    samples=2,
    oracle=_oracle_02,
    solution=r'''import sys

s = sys.stdin.readline().rstrip("\n")
print(s[-1])
print(s[::-1])
print(s[1:-1] if len(s) >= 2 else "EMPTY")
''',
    alt=r'''import sys

s = sys.stdin.readline().rstrip("\n")
n = len(s)
print(s[n - 1])
print("".join(reversed(s)))
if n >= 2:
    print(s[1:n - 1])
else:
    print("EMPTY")
''',
)


def _oracle_03(text: str) -> str:
    w = []
    cur = ""
    for c in text.rstrip("\n"):
        if c == " " or c == "\t":
            if cur:
                w.append(cur)
                cur = ""
        else:
            cur += c
    if cur:
        w.append(cur)
    return "%s\n%d\n" % (" ".join(w), len(w))

add(
    title="单词规范化",
    section="技巧特训 · Python",
    difficulty=1, score=10, tags=["技巧特训", "split", "join", "strip"],
    statement_md=(
        "读入一行英文，单词间可能有**多个空格**、首尾也可能有空格。"
        "输出两行：\n\n"
        "1. 规范化后的句子（单词间恰好一个空格，无首尾空格；没有单词则输出空行）\n"
        "2. 单词个数\n\n"
        "★ 技巧点：不带参的 `s.split()` 会按**任意空白**切分并**自动丢弃空串**——"
        "配合 `\" \".join(...)` 一行完成规范化。C 里这题要写状态机。"
    ),
    input_format="一行英文（长度 ≤ 10000，只含空格和可见字符）。",
    output_format="两行，如题面所述。",
    constraints_md="- 1 ≤ 长度 ≤ 10000",
    inputs=[
        "  hello   world  \n",
        "one\n",
        "   \n",
        "a b  c d\n",
        "The Quick BROWN fox\n",
    ],
    samples=2,
    oracle=_oracle_03,
    solution=r'''import sys

words = sys.stdin.readline().split()
print(" ".join(words))
print(len(words))
''',
    alt=r'''import sys, re

line = sys.stdin.readline().rstrip("\n")
words = re.split(r"\s+", line.strip())
words = [w for w in words if w]
print(" ".join(words))
print(len(words))
''',
)


def _oracle_04(text: str) -> str:
    d = text.split()
    n = int(d[0])
    a = [int(v) for v in d[1:1 + n]]
    sq = []
    odd = 0
    total = 0
    for x in a:
        if x % 2 == 0:
            sq.append(str(x * x))
        else:
            odd += 1
        total += x
    return "%s\n%d\n%d\n" % (" ".join(sq), odd, total)

add(
    title="列表推导式三板斧",
    section="技巧特训 · Python",
    difficulty=1, score=12, tags=["技巧特训", "列表推导式", "filter-map"],
    statement_md=(
        "读入 `n` 和 `n` 个整数，输出三行：\n\n"
        "1. 所有**偶数**的平方（按原顺序，空格分隔；没有偶数则为空行）\n"
        "2. 奇数的个数\n"
        "3. 全体元素的和\n\n"
        "★ 技巧点：`[x*x for x in a if x % 2 == 0]` 一行同时完成"
        "**筛选（if）+ 映射（x*x）**，这就是 filter+map 的 Python 写法。"
        "负数奇偶判断注意：Python 里 `-3 % 2 == 1`，所以 `x % 2 == 0` 天然正确。"
    ),
    input_format="第一行 `n`；第二行 `n` 个整数（|元素| ≤ 10⁹）。",
    output_format="三行，如题面所述。",
    constraints_md="- 1 ≤ n ≤ 1000",
    inputs=[
        "6\n1 2 3 4 5 6\n",
        "5\n-2 -3 0 7 8\n",
        "1\n0\n",
        "3\n2 4 6\n",
        "4\n-1 1 -5 5\n",
    ],
    samples=2,
    oracle=_oracle_04,
    solution=r'''import sys

d = sys.stdin.read().split()
n = int(d[0])
a = [int(v) for v in d[1:1 + n]]
print(*[x * x for x in a if x % 2 == 0])
print(len([x for x in a if x % 2 != 0]))
print(sum(a))
''',
    alt=r'''import sys

d = sys.stdin.read().split()
n = int(d[0])
a = list(map(int, d[1:1 + n]))
evens = list(filter(lambda x: x % 2 == 0, a))
print(" ".join(str(e * e) for e in evens))
print(n - len(evens))
print(sum(a))
''',
)


def _oracle_05(text: str) -> str:
    d = text.split()
    n = int(d[0])
    a = [int(v) for v in d[1:1 + n]]
    b = [int(v) for v in d[1 + n:1 + 2 * n]]
    sums = []
    c1 = 0
    c2 = 0
    for i in range(n):
        sums.append(a[i] + b[i])
        if a[i] == i:
            c1 += 1
        if a[i] == b[i]:
            c2 += 1
    return "%s\n%d\n%d\n" % (" ".join(map(str, sums)), c1, c2)

add(
    title="enumerate 与 zip",
    section="技巧特训 · Python",
    difficulty=2, score=12, tags=["技巧特训", "enumerate", "zip"],
    statement_md=(
        "读入 `n` 和两组各 `n` 个整数 `a`、`b`，输出三行：\n\n"
        "1. 对应位置相加的结果（空格分隔）\n"
        "2. `a` 中**值恰好等于下标**的元素个数（下标从 0 起）\n"
        "3. `a` 与 `b` 对应位置相等的个数\n\n"
        "★ 技巧点：`zip(a, b)` 同时走两个序列、`enumerate(a)` 同时给"
        "**下标和值**——都不用亲手写 `range(len(a))`。这两个是 Python "
        "双序列/带下标遍历的标准姿势。"
    ),
    input_format=(
        "第一行 `n`；第二行 `n` 个整数 `a`；第三行 `n` 个整数 `b`。"
    ),
    output_format="三行，如题面所述。",
    constraints_md="- 1 ≤ n ≤ 1000\n- |元素| ≤ 10⁹",
    inputs=[
        "4\n0 5 2 9\n4 3 2 1\n",
        "1\n0\n0\n",
        "3\n1 1 1\n0 0 0\n",
        "5\n4 4 4 4 4\n1 2 3 4 5\n",
        "2\n0 1\n9 9\n",
    ],
    samples=2,
    oracle=_oracle_05,
    solution=r'''import sys

d = sys.stdin.read().split()
n = int(d[0])
a = [int(v) for v in d[1:1 + n]]
b = [int(v) for v in d[1 + n:1 + 2 * n]]
print(*[x + y for x, y in zip(a, b)])
print(sum(1 for i, x in enumerate(a) if x == i))
print(sum(1 for x, y in zip(a, b) if x == y))
''',
    alt=r'''import sys

d = sys.stdin.read().split()
n = int(d[0])
a = [int(v) for v in d[1:1 + n]]
b = [int(v) for v in d[1 + n:1 + 2 * n]]
out1 = []
c1 = c2 = 0
for i in range(n):
    out1.append(a[i] + b[i])
    if a[i] == i:
        c1 += 1
    if a[i] == b[i]:
        c2 += 1
print(*out1)
print(c1)
print(c2)
''',
)


def _oracle_06(text: str) -> str:
    lines = text.split("\n")
    n = int(lines[0])
    rows = []
    for i in range(1, n + 1):
        p = lines[i].split()
        rows.append((p[0], int(p[1])))
    # 两次稳定排序：先按名字升序，再按分数降序（稳定排序保住名字次序）
    rows.sort(key=lambda r: r[0])
    rows.sort(key=lambda r: r[1], reverse=True)
    return "".join("%s %d\n" % (nm, sc) for nm, sc in rows)

add(
    title="多关键字排序成绩单",
    section="技巧特训 · Python",
    difficulty=2, score=15, tags=["技巧特训", "sorted", "lambda", "稳定性"],
    statement_md=(
        "读入 `n` 个学生的「姓名 分数」，输出排名列表：**分数降序**，"
        "同分按**姓名字典序升序**。每行 `姓名 分数`。\n\n"
        "★ 技巧点：`rows.sort(key=lambda r: (-r[1], r[0]))` —— 元组比较"
        "**先比第一项、再比第二项**，负号把降序翻成升序比较，一行写完多关键字。"
        "另一种写法是利用**稳定排序**：先按次关键字排，再按主关键字排。"
    ),
    input_format="第一行 `n`；随后 `n` 行，每行 `姓名 分数`（姓名不含空格）。",
    output_format="`n` 行，排序后的 `姓名 分数`。",
    constraints_md="- 1 ≤ n ≤ 1000\n- 0 ≤ 分数 ≤ 100",
    inputs=[
        "4\nAlice 90\nBob 85\nCindy 90\nDave 70\n",
        "3\nzhou 100\nli 100\nzhao 100\n",
        "2\nab 50\naa 60\n",
        "5\ne 1\nd 2\nc 3\nb 4\na 5\n",
        "3\nTom 88\nJerry 88\nSpike 77\n",
    ],
    samples=2,
    oracle=_oracle_06,
    solution=r'''import sys

data = sys.stdin.read().split("\n")
n = int(data[0])
rows = []
for i in range(1, n + 1):
    name, score = data[i].split()
    rows.append((name, int(score)))
rows.sort(key=lambda r: (-r[1], r[0]))
for name, score in rows:
    print(name, score)
''',
    alt=r'''import sys

data = sys.stdin.read().split("\n")
n = int(data[0])
rows = []
for i in range(1, n + 1):
    name, score = data[i].split()
    rows.append((name, int(score)))
rows.sort(key=lambda r: r[0])                      # 先按次关键字（名字）升序
rows.sort(key=lambda r: r[1], reverse=True)        # 再按主关键字（分数）降序，稳定
for name, score in rows:
    print(name, score)
''',
)


def _oracle_07(text: str) -> str:
    w = text.split()
    order = []
    cnt = {}
    for x in w:
        if x not in cnt:
            order.append(x)
            cnt[x] = 0
        cnt[x] += 1
    out = "".join("%s %d\n" % (k, cnt[k]) for k in order)
    return out + "TOTAL %d\n" % len(w)

add(
    title="词频统计 dict.get",
    section="技巧特训 · Python",
    difficulty=2, score=12, tags=["技巧特训", "dict", "get", "词频"],
    statement_md=(
        "读入一行单词，按**首次出现顺序**输出每个单词及其出现次数"
        "（每行 `单词 次数`），最后一行输出 `TOTAL 总词数`。\n\n"
        "★ 技巧点：`d[k] = d.get(k, 0) + 1` —— `get` 的第二个参数是"
        "**键不存在时的默认值**，计数器从此不用先判 `k in d`。"
        "顺便一提：标准库 `collections.Counter(单词列表)` 一行就能建好计数器，"
        "而且 Python 3.7+ 的字典**保持插入顺序**，天然按首次出现输出。"
    ),
    input_format="一行，若干个单词（1 ≤ 词数 ≤ 2000，单词长度 ≤ 20）。",
    output_format="如题面所述。",
    constraints_md="- 1 ≤ 词数 ≤ 2000",
    inputs=[
        "apple banana apple cherry banana apple\n",
        "one\n",
        "a a a a\n",
        "x y z x y v\n",
        "hello world\n",
    ],
    samples=2,
    oracle=_oracle_07,
    solution=r'''import sys

words = sys.stdin.readline().split()
cnt = {}
for w in words:
    cnt[w] = cnt.get(w, 0) + 1
for k, v in cnt.items():
    print(k, v)
print("TOTAL", len(words))
''',
    alt=r'''import sys
from collections import Counter

words = sys.stdin.readline().split()
cnt = Counter(words)
for k, v in cnt.items():          # Counter 是 dict 子类，保持首次出现顺序
    print(k, v)
print("TOTAL", len(words))
''',
)


def _oracle_08(text: str) -> str:
    lines = text.rstrip("\n").split("\n")
    A = set(int(v) for v in lines[0].split())
    B = set(int(v) for v in lines[1].split())
    inter = sorted(A & B)
    union = sorted(A | B)
    diff = sorted(A - B)
    sym = sorted(A ^ B)
    return "%s\n%s\n%s\n%s\n" % (
        " ".join(map(str, inter)),
        " ".join(map(str, union)),
        " ".join(map(str, diff)),
        " ".join(map(str, sym)),
    )

add(
    title="集合运算四连",
    section="技巧特训 · Python",
    difficulty=2, score=12, tags=["技巧特训", "set", "交并差", "对称差"],
    statement_md=(
        "读入两行整数（各自可重复、乱序），各看作一个集合。"
        "输出四行（元素升序、空格分隔，空集输出空行）：\n\n"
        "1. 交集\n2. 并集\n3. A − B（在 A 不在 B）\n4. 对称差（恰好在其中一个）\n\n"
        "★ 技巧点：`set` 自带运算符 `A & B`、`A | B`、`A - B`、`A ^ B`，"
        "四个运算四个字符，C 里每个都得手写双循环。重复元素会被 `set` "
        "自动吸收，去重白送。"
    ),
    input_format="两行，每行若干个整数（可为空行？不会——每行至少 1 个；|元素| ≤ 10⁹）。",
    output_format="四行，如题面所述。",
    constraints_md="- 每行 1 ≤ 元素个数 ≤ 1000",
    inputs=[
        "1 2 3 4\n3 4 5 6\n",
        "1 2 3\n4 5 6\n",
        "7 7 8 9\n9 9 7\n",
        "5\n5\n",
        "10 20 30\n10 20 30\n",
    ],
    samples=2,
    oracle=_oracle_08,
    solution=r'''import sys

lines = sys.stdin.read().rstrip("\n").split("\n")
A = set(map(int, lines[0].split()))
B = set(map(int, lines[1].split()))
for s in (A & B, A | B, A - B, A ^ B):
    print(*sorted(s))
''',
    alt=r'''import sys

lines = sys.stdin.read().rstrip("\n").split("\n")
A = set(map(int, lines[0].split()))
B = set(map(int, lines[1].split()))
inter = [x for x in A if x in B]
union = list(A) + [x for x in B if x not in A]
diff = [x for x in A if x not in B]
sym = diff + [x for x in B if x not in A]
for s in (inter, union, diff, sym):
    print(*sorted(s))
''',
)


# --------------------------------------------------------------------- #
#  竞赛工具箱（difficulty 2~3）
# --------------------------------------------------------------------- #

def _oracle_09(text: str) -> str:
    d = text.split()
    a = [int(v) for v in d[1:1 + int(d[0])]]
    cnt = {}
    for x in a:
        cnt[x] = cnt.get(x, 0) + 1
    best_x = None
    best_c = 0
    for k in sorted(cnt):
        if cnt[k] > best_c:
            best_x = k
            best_c = cnt[k]
    return "%d %d\n" % (best_x, best_c)

add(
    title="众数与次数 Counter",
    section="技巧特训 · Python",
    difficulty=2, score=12, tags=["技巧特训", "Counter", "most_common"],
    statement_md=(
        "读入 `n` 个整数，输出出现次数最多的数及其次数（一行 `数 次数`）。"
        "若并列，输出**最小**的那个数。\n\n"
        "★ 技巧点：`collections.Counter(a)` 建计数器一行搞定，"
        "`most_common()` 直接按次数降序给结果——并列时想取最小值，"
        "再对候选排一次序即可。这题练的是「计数器 + 一次遍历找最优」。"
    ),
    input_format="第一行 `n`；第二行 `n` 个整数（|元素| ≤ 10⁹）。",
    output_format="一行 `数 次数`。",
    constraints_md="- 1 ≤ n ≤ 10⁵",
    inputs=[
        "6\n1 2 2 3 3 3\n",
        "7\n5 5 1 1 9 9 9\n",
        "4\n-1 -1 2 2\n",
        "1\n42\n",
        "8\n1 2 1 2 1 2 3 3\n",
    ],
    samples=2,
    oracle=_oracle_09,
    solution=r'''import sys
from collections import Counter

d = sys.stdin.read().split()
a = [int(v) for v in d[1:1 + int(d[0])]]
cnt = Counter(a)
top = max(cnt.values())
ans = min(k for k, v in cnt.items() if v == top)
print(ans, top)
''',
    alt=r'''import sys

d = sys.stdin.read().split()
a = [int(v) for v in d[1:1 + int(d[0])]]
cnt = {}
for x in a:
    cnt[x] = cnt.get(x, 0) + 1
best_x, best_c = None, 0
for k in sorted(cnt):
    if cnt[k] > best_c:
        best_x, best_c = k, cnt[k]
print(best_x, best_c)
''',
)


def _oracle_10(text: str) -> str:
    d = text.split()
    n = int(d[0])
    k = int(d[1])
    a = [int(v) for v in d[2:2 + n]]
    a = sorted(a, reverse=True)
    return "%d\n" % a[k - 1]

add(
    title="第 k 大 heapq",
    section="技巧特训 · Python",
    difficulty=2, score=12, tags=["技巧特训", "heapq", "堆", "top-k"],
    statement_md=(
        "读入 `n`、`k` 和 `n` 个整数，输出**第 k 大**的数（重复元素各自算位次）。\n\n"
        "★ 技巧点：`heapq.nlargest(k, a)[-1]` 直接给出第 k 大；"
        "标准库 `heapq` 是**小顶堆**（`heapq.heappush/heappop`），"
        "「维护一个大小为 k 的小顶堆扫一遍」是流式数据的 top-k 标准解法，"
        "n 很大、k 很小时比全排序省得多。"
    ),
    input_format="第一行 `n k`；第二行 `n` 个整数（|元素| ≤ 10⁹）。",
    output_format="一行，第 k 大的数。",
    constraints_md="- 1 ≤ k ≤ n ≤ 2×10⁵",
    inputs=[
        "5 2\n3 1 4 1 5\n",
        "6 3\n9 9 8 8 7 1\n",
        "1 1\n100\n",
        "10 10\n1 2 3 4 5 6 7 8 9 10\n",
        "7 5\n5 5 5 5 5 5 5\n",
    ],
    samples=2,
    oracle=_oracle_10,
    solution=r'''import sys, heapq

d = sys.stdin.read().split()
n, k = int(d[0]), int(d[1])
a = [int(v) for v in d[2:2 + n]]
print(heapq.nlargest(k, a)[-1])
''',
    alt=r'''import sys, heapq

d = sys.stdin.read().split()
n, k = int(d[0]), int(d[1])
a = [int(v) for v in d[2:2 + n]]
heap = a[:k]                      # 大小为 k 的小顶堆
heapq.heapify(heap)
for x in a[k:]:
    if x > heap[0]:
        heapq.heapreplace(heap, x)
print(heap[0])
''',
)


def _oracle_11(text: str) -> str:
    d = text.split()
    i = 0
    n = int(d[i]); i += 1
    q = int(d[i]); i += 1
    a = [int(d[i + k]) for k in range(n)]
    i += n
    out = []
    for _ in range(q):
        l = int(d[i]); r = int(d[i + 1]); i += 2
        s = 0
        for k in range(l - 1, r):
            s += a[k]
        out.append(s)
    return "".join("%d\n" % v for v in out)

add(
    title="前缀和 accumulate",
    section="技巧特训 · Python",
    difficulty=2, score=15, tags=["技巧特训", "前缀和", "accumulate", "itertools"],
    statement_md=(
        "读入 `n`、`q` 和数组 `a`，接着 `q` 个询问 `l r`（1 基闭区间）。"
        "对每个询问输出区间和（一行一个）。\n\n"
        "★ 技巧点：**先建前缀和、再 O(1) 回答**——`pre[i] = a[0..i-1] 之和`，"
        "区间和 = `pre[r] - pre[l-1]`。Python 里 `list(itertools.accumulate(a))` "
        "一行建好前缀和。预处理一次，查询白送，这是竞赛最常用的套路没有之一。"
    ),
    input_format=(
        "第一行 `n q`；第二行 `n` 个整数；随后 `q` 行每行 `l r`。\n"
        "- 1 ≤ n ≤ 10⁵，1 ≤ q ≤ 1000，|aᵢ| ≤ 10⁹，1 ≤ l ≤ r ≤ n"
    ),
    output_format="`q` 行，每行一个区间和。",
    constraints_md="- 1 ≤ n ≤ 10⁵\n- 1 ≤ q ≤ 1000",
    inputs=[
        "5 3\n1 2 3 4 5\n1 5\n2 4\n3 3\n",
        "3 2\n-1 -2 -3\n1 1\n1 3\n",
        "1 1\n1000000000\n1 1\n",
        "6 4\n2 0 -2 4 -4 8\n1 6\n2 2\n3 5\n6 6\n",
        "4 1\n9 9 9 9\n2 3\n",
    ],
    samples=2,
    oracle=_oracle_11,
    solution=r'''import sys
from itertools import accumulate

d = sys.stdin.read().split()
n, q = int(d[0]), int(d[1])
a = [int(v) for v in d[2:2 + n]]
pre = [0] + list(accumulate(a))     # pre[i] = a[0..i-1] 之和
i = 2 + n
out = []
for _ in range(q):
    l, r = int(d[i]), int(d[i + 1])
    i += 2
    out.append(pre[r] - pre[l - 1])
print("\n".join(map(str, out)))
''',
    alt=r'''import sys

d = sys.stdin.read().split()
n, q = int(d[0]), int(d[1])
a = [int(v) for v in d[2:2 + n]]
pre = [0] * (n + 1)
for k in range(n):
    pre[k + 1] = pre[k] + a[k]
i = 2 + n
out = []
for _ in range(q):
    l, r = int(d[i]), int(d[i + 1])
    i += 2
    out.append(pre[r] - pre[l - 1])
print("\n".join(map(str, out)))
''',
)


def _oracle_12(text: str) -> str:
    d = text.split()
    i = 0
    n = int(d[i]); i += 1
    q = int(d[i]); i += 1
    a = [int(d[i + k]) for k in range(n)]
    i += n
    out = []
    for _ in range(q):
        x = int(d[i]); i += 1
        ans = "NONE"
        j = 0
        while j < n:
            if a[j] > x:
                ans = str(a[j])
                break
            j += 1
        out.append(ans)
    return "".join(s + "\n" for s in out)

add(
    title="第一个大于 x 的数 bisect",
    section="技巧特训 · Python",
    difficulty=2, score=15, tags=["技巧特训", "bisect", "二分", "upper_bound"],
    statement_md=(
        "读入**升序**数组（可重复）和 `q` 个询问 `x`。对每个询问，"
        "输出数组中**第一个严格大于 x** 的元素；不存在输出 `NONE`。\n\n"
        "★ 技巧点：`bisect.bisect_right(a, x)` 返回「x 能插入的最右位置」，"
        "**恰好就是第一个大于 x 的下标**——这是 C++ `upper_bound` 的 Python 对应物，"
        "一行替代线性扫描。配套记忆：`bisect_left` 找第一个 ≥ x 的位置。"
        "有序数组的「第一个大于/小于」类问题，全部走二分，别写 for。"
    ),
    input_format=(
        "第一行 `n q`；第二行 `n` 个**升序**整数；随后 `q` 行每行一个 `x`。\n"
        "- 1 ≤ n, q ≤ 2×10⁵，|元素|、|x| ≤ 10⁹"
    ),
    output_format="`q` 行，每行一个数或 `NONE`。",
    constraints_md="- 1 ≤ n, q ≤ 2×10⁵",
    inputs=[
        "8 4\n1 2 4 4 4 7 9 9\n4\n5\n9\n0\n",
        "5 3\n2 2 2 2 2\n1\n2\n3\n",
        "1 2\n10\n10\n11\n",
        "6 2\n-5 -2 0 3 8 8\n-6\n8\n",
        "4 3\n1 3 5 7\n7\n6\n1\n",
    ],
    samples=2,
    oracle=_oracle_12,
    solution=r'''import sys, bisect

d = sys.stdin.read().split()
n, q = int(d[0]), int(d[1])
a = [int(v) for v in d[2:2 + n]]
i = 2 + n
out = []
for _ in range(q):
    x = int(d[i]); i += 1
    p = bisect.bisect_right(a, x)   # 第一个 > x 的下标
    out.append(str(a[p]) if p < n else "NONE")
print("\n".join(out))
''',
    alt=r'''import sys

d = sys.stdin.read().split()
n, q = int(d[0]), int(d[1])
a = [int(v) for v in d[2:2 + n]]
i = 2 + n
out = []
for _ in range(q):
    x = int(d[i]); i += 1
    lo, hi = 0, n                    # 手写二分：找第一个 > x
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] > x:
            hi = mid
        else:
            lo = mid + 1
    out.append(str(a[lo]) if lo < n else "NONE")
print("\n".join(out))
''',
)


def _oracle_13(text: str) -> str:
    d = text.split()
    n = int(d[0])
    x, y = 1, 2
    if n == 1:
        return "1\n"
    for _ in range(n - 2):
        x, y = y, x + y
    return "%d\n" % y

add(
    title="爬楼梯 lru_cache",
    section="技巧特训 · Python",
    difficulty=2, score=12, tags=["技巧特训", "lru_cache", "记忆化", "递归"],
    statement_md=(
        "台阶有 `n` 阶，每次上 1 或 2 阶，问有多少种走法（f(1)=1，f(2)=2）。"
        "n 最大 90——结果会非常大，直接输出精确值。\n\n"
        "★ 技巧点：给递归函数挂上 `@functools.lru_cache(maxsize=None)`，"
        "朴素递归从 O(2ⁿ) 变 O(n)——**记忆化一行加注解就有了**。"
        "Python 的整数没有溢出，大结果直接打出来；这个题同时是"
        "「递归会重复算」的活教材。"
    ),
    input_format="一行一个整数 `n`。",
    output_format="一行，走法总数。",
    constraints_md="- 1 ≤ n ≤ 90",
    inputs=[
        "1\n",
        "2\n",
        "10\n",
        "50\n",
        "90\n",
    ],
    samples=2,
    oracle=_oracle_13,
    solution=r'''import sys
from functools import lru_cache

@lru_cache(maxsize=None)
def f(n):
    if n <= 2:
        return n
    return f(n - 1) + f(n - 2)

print(f(int(sys.stdin.read())))
''',
    alt=r'''import sys

n = int(sys.stdin.read())
x, y = 1, 2                 # f(1), f(2)
if n == 1:
    print(x)
else:
    for _ in range(n - 2):
        x, y = y, x + y
    print(y)
''',
)


def _oracle_14(text: str) -> str:
    s = text.rstrip("\n")
    cl = []
    for c in s:
        c_low = c.lower() if ("A" <= c <= "Z") else c
        if ("a" <= c_low <= "z") or ("0" <= c_low <= "9"):
            cl.append(c_low)
    ok = True
    i, j = 0, len(cl) - 1
    while i < j:
        if cl[i] != cl[j]:
            ok = False
            break
        i += 1
        j -= 1
    return "%s\n%s\n" % ("YES" if ok else "NO", "".join(cl))

add(
    title="回文判定与清洗",
    section="技巧特训 · Python",
    difficulty=2, score=12, tags=["技巧特训", "回文", "isalnum", "切片反转"],
    statement_md=(
        "读入一行（可含标点、空格），只保留**字母和数字**并忽略大小写后，"
        "判断是否回文。第一行输出 `YES`/`NO`，第二行输出清洗后的串。\n\n"
        "★ 技巧点：生成器表达式 + `"".join(...)` 做字符过滤：\n"
        "`t = "".join(c.lower() for c in s if c.isalnum())`，"
        "回文判定就是 `t == t[::-1]`——清洗、比较各一行。"
        "空清洗结果（全是标点）按回文处理。"
    ),
    input_format="一行字符串（长度 ≤ 10000）。",
    output_format="两行：`YES`/`NO` 与清洗后的串。",
    constraints_md="- 1 ≤ 长度 ≤ 10000",
    inputs=[
        "A man, a plan, a canal: Panama\n",
        "race a car\n",
        "!!!\n",
        "0P\n",
        "Was it a car or a cat I saw?\n",
    ],
    samples=2,
    oracle=_oracle_14,
    solution=r'''import sys

s = sys.stdin.readline().rstrip("\n")
t = "".join(c.lower() for c in s if c.isalnum())
print("YES" if t == t[::-1] else "NO")
print(t)
''',
    alt=r'''import sys

s = sys.stdin.readline().rstrip("\n")
t = "".join(c.lower() for c in s if c.isalnum())
i, j = 0, len(t) - 1
ok = True
while i < j:
    if t[i] != t[j]:
        ok = False
        break
    i += 1
    j -= 1
print("YES" if ok else "NO")
print(t)
''',
)


# --------------------------------------------------------------------- #
#  竞赛强度（difficulty 3~4，对标蓝桥杯 / 码蹄杯）
# --------------------------------------------------------------------- #

def _oracle_15(text: str) -> str:
    d = text.split()
    i = 0
    n = int(d[i]); i += 1
    W = int(d[i]); i += 1
    items = []
    for _ in range(n):
        w = int(d[i]); v = int(d[i + 1]); i += 2
        items.append((w, v))
    dp = [0] * (W + 1)
    for w, v in items:
        for j in range(W, w - 1, -1):
            if dp[j - w] + v > dp[j]:
                dp[j] = dp[j - w] + v
    return "%d\n" % dp[W]

add(
    title="01 背包",
    section="技巧特训 · Python",
    difficulty=3, score=25, tags=["技巧特训", "DP", "背包", "动态规划"],
    statement_md=(
        "经典 0-1 背包：`n` 件物品，第 `i` 件重量 `wᵢ`、价值 `vᵢ`，"
        "背包容量的上限 `W`，每件**至多选一次**。求能装下的最大总价值。\n\n"
        "★ 技巧点：一维滚动数组——`dp[j] = max(dp[j], dp[j-w] + v)`，"
        "**内层必须倒着枚举** `j`（正着走同一件物品会被选两次，那就成了完全背包）。"
        "「倒序 = 0-1，正序 = 完全」是背包家族的第一条铁律。"
    ),
    input_format=(
        "第一行 `n W`；随后 `n` 行每行 `w v`。\n"
        "- 1 ≤ n ≤ 100，1 ≤ W ≤ 10000，1 ≤ w ≤ W，0 ≤ v ≤ 10⁴"
    ),
    output_format="一行，最大总价值。",
    constraints_md="- 1 ≤ n ≤ 100\n- 1 ≤ W ≤ 10⁴",
    inputs=[
        "4 5\n1 2\n2 3\n3 4\n4 5\n",
        "3 10\n5 10\n4 8\n6 12\n",
        "1 1\n1 100\n",
        "5 7\n2 3\n3 4\n4 5\n5 6\n1 1\n",
        "6 13\n3 5\n4 7\n2 3\n7 9\n5 6\n1 2\n",
    ],
    samples=2,
    oracle=_oracle_15,
    solution=r'''import sys

d = sys.stdin.read().split()
n, W = int(d[0]), int(d[1])
dp = [0] * (W + 1)
i = 2
for _ in range(n):
    w, v = int(d[i]), int(d[i + 1])
    i += 2
    for j in range(W, w - 1, -1):        # 倒序：保证每件只选一次
        cand = dp[j - w] + v
        if cand > dp[j]:
            dp[j] = cand
print(dp[W])
''',
    alt=r'''import sys
from functools import lru_cache

d = sys.stdin.read().split()
n, W = int(d[0]), int(d[1])
ws = []
vs = []
i = 2
for _ in range(n):
    ws.append(int(d[i])); vs.append(int(d[i + 1]))
    i += 2

@lru_cache(maxsize=None)
def f(k, cap):                # 前 k 件、剩余容量 cap 的最大价值
    if k == 0:
        return 0
    best = f(k - 1, cap)
    if ws[k - 1] <= cap:
        cand = f(k - 1, cap - ws[k - 1]) + vs[k - 1]
        if cand > best:
            best = cand
    return best

print(f(n, W))
''',
)


def _oracle_16(text: str) -> str:
    d = text.split()
    n = int(d[0])
    a = [int(v) for v in d[1:1 + n]]
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if a[j] < a[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
    return "%d\n" % (max(dp) if n else 0)

add(
    title="最长上升子序列 n log n",
    section="技巧特训 · Python",
    difficulty=3, score=25, tags=["技巧特训", "LIS", "二分", "bisect"],
    statement_md=(
        "读入 `n` 个整数，输出**严格上升**子序列的最长长度。\n\n"
        "★ 技巧点：维护「每个长度对应的最小结尾」数组 `tails`，"
        "对每个 x 用 `bisect_left` 找到它该待的位置：替换或追加。"
        "`tails` 始终有序，整个过程 O(n log n)——n=10⁵ 的 LIS 只能这么做，"
        "O(n²) 的 DP 会超时。"
    ),
    input_format="第一行 `n`；第二行 `n` 个整数（|元素| ≤ 10⁹）。",
    output_format="一行，严格上升子序列的最长长度。",
    constraints_md="- 1 ≤ n ≤ 10⁵",
    inputs=[
        "8\n1 3 2 3 1 4 2 5\n",
        "5\n5 4 3 2 1\n",
        "6\n1 2 3 4 5 6\n",
        "1\n7\n",
        "10\n2 2 2 2 3 3 3 1 9 9\n",
    ],
    samples=2,
    oracle=_oracle_16,
    solution=r'''import sys, bisect

d = sys.stdin.read().split()
n = int(d[0])
a = [int(v) for v in d[1:1 + n]]
tails = []                        # tails[k] = 长度 k+1 的 LIS 的最小结尾
for x in a:
    p = bisect.bisect_left(tails, x)   # 严格上升 → bisect_left
    if p == len(tails):
        tails.append(x)
    else:
        tails[p] = x
print(len(tails))
''',
    alt=r'''import sys

d = sys.stdin.read().split()
n = int(d[0])
a = [int(v) for v in d[1:1 + n]]
INF = float("inf")
tails = [INF] * n                 # tails[k] = 长度 k+1 的最小结尾，初始无穷
len_ = 0
for x in a:
    lo, hi = 0, len_
    while lo < hi:                # 手写二分找第一个 >= x 的位置
        mid = (lo + hi) // 2
        if tails[mid] >= x:
            hi = mid
        else:
            lo = mid + 1
    tails[lo] = x
    if lo == len_:
        len_ += 1
print(len_)
''',
)


def _oracle_17(text: str) -> str:
    d = text.split()
    a, b, m = int(d[0]), int(d[1]), int(d[2])
    r = 1 % m
    base = a % m
    e = b
    while e > 0:
        if e & 1:
            r = (r * base) % m
        base = (base * base) % m
        e >>= 1
    return "%d\n" % r

add(
    title="快速幂取模",
    section="技巧特训 · Python",
    difficulty=2, score=15, tags=["技巧特训", "快速幂", "pow", "取模"],
    statement_md=(
        "读入 `a b m`，输出 `a^b mod m`。b 最大 10¹⁸——暴力乘 10¹⁸ 次是天文数字。\n\n"
        "★ 技巧点：Python 内置三参 `pow(a, b, m)` 就是快速幂，**一行，还比手写快**"
        "（C 实现里 m 内建了模乘优化）。要理解原理就自己写：b 按二进制拆位，"
        "平方翻底数——手写版是竞赛通用语言（C++ 没有 powmod），两边都得会。"
    ),
    input_format="一行 `a b m`（1 ≤ a, m ≤ 10⁹；0 ≤ b ≤ 10¹⁸）。",
    output_format="一行，`a^b mod m`。",
    constraints_md="- 1 ≤ a, m ≤ 10⁹\n- 0 ≤ b ≤ 10¹⁸",
    inputs=[
        "2 10 1000\n",
        "3 0 7\n",
        "2 62 1000000007\n",
        "5 100 1000000007\n",
        "123456789 999999999999999998 998244353\n",
    ],
    samples=2,
    oracle=_oracle_17,
    solution=r'''import sys

a, b, m = map(int, sys.stdin.read().split())
print(pow(a, b, m))          # 内置三参 pow = 快速幂取模
''',
    alt=r'''import sys

a, b, m = map(int, sys.stdin.read().split())
r = 1 % m
base = a % m
e = b
while e > 0:                 # 手写快速幂：按指数二进制位逐位平方
    if e & 1:
        r = r * base % m
    base = base * base % m
    e >>= 1
print(r)
''',
)


def _oracle_18(text: str) -> str:
    lines = text.rstrip("\n").split("\n")
    n = int(lines[0])
    ivs = []
    for i in range(1, n + 1):
        l, r = lines[i].split()
        ivs.append((int(l), int(r)))
    ivs.sort()
    merged = []
    for l, r in ivs:
        if merged and l <= merged[-1][1]:
            if r > merged[-1][1]:
                merged[-1] = (merged[-1][0], r)
        else:
            merged.append((l, r))
    out = "%d\n" % len(merged)
    out += "".join("%d %d\n" % m for m in merged)
    return out

add(
    title="区间合并",
    section="技巧特训 · Python",
    difficulty=3, score=20, tags=["技巧特训", "贪心", "排序", "区间"],
    statement_md=(
        "读入 `n` 个闭区间，把所有**有重叠或相接**的区间合并，"
        "输出合并后的个数与各区间（按左端点升序，每行 `l r`）。\n\n"
        "★ 技巧点：**先按左端点排序，再线性扫一遍**——当前区间起点 ≤ "
        "上一合并区间的终点就合并（终点取 max），否则另起一段。"
        "「排序后扫一遍」是所有区间类问题（合并 / 插入 / 去覆盖）的总套路。"
    ),
    input_format="第一行 `n`；随后 `n` 行每行 `l r`（l ≤ r）。",
    output_format="第一行合并后个数；随后每行一个合并区间 `l r`。",
    constraints_md="- 1 ≤ n ≤ 10⁵\n- 0 ≤ l ≤ r ≤ 10⁹",
    inputs=[
        "4\n1 3\n2 6\n8 10\n15 18\n",
        "3\n1 4\n4 5\n2 3\n",
        "2\n1 2\n3 4\n",
        "5\n5 6\n1 2\n3 4\n2 3\n6 7\n",
        "1\n0 1000000000\n",
    ],
    samples=2,
    oracle=_oracle_18,
    solution=r'''import sys

d = sys.stdin.read().split()
n = int(d[0])
ivs = sorted((int(d[1 + 2 * i]), int(d[2 + 2 * i])) for i in range(n))
merged = []
for l, r in ivs:
    if merged and l <= merged[-1][1]:
        merged[-1][1] = max(merged[-1][1], r)
    else:
        merged.append([l, r])
print(len(merged))
for l, r in merged:
    print(l, r)
''',
    alt=r'''import sys

d = sys.stdin.read().split()
n = int(d[0])
ivs = []
for i in range(n):
    ivs.append((int(d[1 + 2 * i]), int(d[2 + 2 * i])))
ivs.sort(key=lambda p: (p[0], p[1]))
cl, cr = ivs[0]
out = []
for l, r in ivs[1:]:
    if l <= cr:
        cr = max(cr, r)
    else:
        out.append((cl, cr))
        cl, cr = l, r
out.append((cl, cr))
print(len(out))
for l, r in out:
    print(l, r)
''',
)


def _oracle_19(text: str) -> str:
    d = text.split()
    n = int(d[0])
    fact = 1
    for k in range(2, n + 1):
        fact *= k
    return "%d\n%d\n" % (len(str(fact)), fact)

add(
    title="阶乘精确值与大数",
    section="技巧特训 · Python",
    difficulty=2, score=15, tags=["技巧特训", "大数", "math", "factorial"],
    statement_md=(
        "读入 `n`，输出两行：`n!` 的**位数**、`n!` 的**精确值**。\n\n"
        "★ 技巧点：Python 的 `int` 是任意精度大数，`math.factorial(n)` "
        "直接给出几百位的精确结果，`len(str(f))` 就是位数——"
        "C 里这是要开数组做高精度乘法的大工程。Python 做大数题"
        "（大数加乘、精确分数、连乘取模前先留底）是降维打击。"
    ),
    input_format="一行一个整数 `n`。",
    output_format="两行：位数、精确值。",
    constraints_md="- 0 ≤ n ≤ 500",
    inputs=[
        "0\n",
        "1\n",
        "10\n",
        "100\n",
        "500\n",
    ],
    samples=2,
    oracle=_oracle_19,
    solution=r'''import sys, math

n = int(sys.stdin.read())
f = math.factorial(n)
print(len(str(f)))
print(f)
''',
    alt=r'''import sys
from functools import reduce
from operator import mul

n = int(sys.stdin.read())
f = reduce(mul, range(1, n + 1), 1)
print(len(str(f)))
print(f)
''',
)


def _oracle_20(text: str) -> str:
    d = text.split()
    n = int(d[0])
    is_comp = [False] * (n + 1)
    cnt = 0
    largest = 0
    for i in range(2, n + 1):
        if not is_comp[i]:
            cnt += 1
            largest = i
            for j in range(i * i, n + 1, i):
                is_comp[j] = True
    return "%d %d\n" % (cnt, largest)

add(
    title="素数筛法",
    section="技巧特训 · Python",
    difficulty=3, score=20, tags=["技巧特训", "筛法", "埃氏筛", "素数"],
    statement_md=(
        "读入 `n`，输出一行两个数：`2..n` 里素数的**个数**与**最大的素数**"
        "（n ≥ 2，必有素数）。\n\n"
        "★ 技巧点：**埃氏筛**——从每个素数 p 开始，把 p², p²+p, ... 全部标记为合数，"
        "整体 O(n log log n)；`i*i` 起步（更小的倍数早被筛过）是关键小优化。"
        "试除判单个数是 O(√n)，要判 1~n 全体就得用筛。Python 版注意"
        "用列表下标而不是集合，否则常数爆炸。"
    ),
    input_format="一行一个整数 `n`。",
    output_format="一行：素数个数 与 最大素数（空格分隔）。",
    constraints_md="- 2 ≤ n ≤ 10⁶",
    time_limit_ms=2000,
    inputs=[
        "2\n",
        "10\n",
        "100\n",
        "10000\n",
        "1000000\n",
    ],
    samples=2,
    oracle=_oracle_20,
    solution=r'''import sys

n = int(sys.stdin.read())
comp = bytearray(n + 1)          # bytearray 当布尔数组，省内存速度快
cnt = 0
largest = 0
for i in range(2, n + 1):
    if not comp[i]:
        cnt += 1
        largest = i
        comp[i * i::i] = b"\x01" * len(comp[i * i::i])
print(cnt, largest)
''',
    alt=r'''import sys

n = int(sys.stdin.read())
comp = [False] * (n + 1)
primes = []
for i in range(2, n + 1):
    if not comp[i]:
        primes.append(i)
    for p in primes:             # 线性（欧拉）筛：每个合数只被最小素因子筛一次
        if i * p > n:
            break
        comp[i * p] = True
        if i % p == 0:
            break
print(len(primes), primes[-1])
''',
)


# --------------------------------------------------------------------- #
#  进阶技巧（difficulty 2~4，第二批量）
# --------------------------------------------------------------------- #

def _oracle_21(text: str) -> str:
    s = text.rstrip("\n")
    enc = []
    for c in s:
        if "a" <= c <= "z":
            enc.append(chr((ord(c) - 97 + 13) % 26 + 97))
        elif "A" <= c <= "Z":
            enc.append(chr((ord(c) - 65 + 13) % 26 + 65))
        else:
            enc.append(c)
    vow = 0
    for c in s:
        if c in "aeiouAEIOU":
            vow += 1
    return "".join(enc) + "\n%d\n" % vow

add(
    title="ROT13 字母替换表",
    section="技巧特训 · Python",
    difficulty=2, score=10, tags=["技巧特训", "str.translate", "maketrans", "字符映射"],
    statement_md=(
        "读入一行字符串，输出两行：\n\n"
        "1. 对每个字母做 ROT13 位移（a→n、z→m，大小写各自循环，非字母原样保留）\n"
        "2. 原串里元音字母（a e i o u，大小写都算）的个数\n\n"
        "★ 技巧点：`str.maketrans(from, to)` 造映射表，`s.translate(table)` 一次性替换——"
        "比 `for c in s: if ... elif ...` 快一个量级，而且天然支持多字符映射。"
        "ROT13 是自逆的（再位移一次就还原），所以它是理解「字符映射表」最好的例子。"
    ),
    input_format="一行字符串（长度 ≤ 10⁵，可含空格与标点）。",
    output_format="两行：加密结果、元音个数。",
    constraints_md="- 1 ≤ 字符串长度 ≤ 10⁵",
    inputs=[
        "Hello, World!\n",
        "abcXYZ\n",
        "123 !?\n",
        "Uryyb\n",
        "AEIOU aeiou\n",
    ],
    samples=2,
    oracle=_oracle_21,
    solution=r'''import sys

s = sys.stdin.readline().rstrip("\n")
lower = "abcdefghijklmnopqrstuvwxyz"
upper = lower.upper()
table = str.maketrans(lower + upper,
                      lower[13:] + lower[:13] + upper[13:] + upper[:13])
print(s.translate(table))
print(sum(c in "aeiouAEIOU" for c in s))
''',
    alt=r'''import sys
import codecs

s = sys.stdin.readline().rstrip("\n")
print(codecs.encode(s, "rot13"))          # 标准库自带 rot13 编解码器
print(sum(1 for c in s if c.lower() in "aeiou"))
''',
)


def _oracle_22(text: str) -> str:
    s = text.rstrip("\n")
    nums = []
    cur = ""
    for c in s:
        if "0" <= c <= "9":
            cur += c
        else:
            if cur:
                nums.append(cur)
                cur = ""
    if cur:
        nums.append(cur)
    if not nums:
        return "0\n0\nEMPTY\n"
    total = 0
    for x in nums:
        total += int(x)
    return "%d\n%d\n%d\n" % (len(nums), total, max(int(x) for x in nums))

add(
    title="正则提取所有整数",
    section="技巧特训 · Python",
    difficulty=2, score=10, tags=["技巧特训", "re", "findall", "正则"],
    statement_md=(
        "读入一行字符串，把里面所有**连续数字**当作整数提取出来，输出三行：\n\n"
        "1. 整数的个数\n"
        "2. 总和\n"
        "3. 最大值（一个数字都没有时输出 `EMPTY`）\n\n"
        "★ 技巧点：`re.findall(r\"\\d+\", s)` 一行拿到所有数字串，比手写扫描短十倍。"
        "注意 `\\d+` 是贪婪的：`\"a12b\"` 抓到的是 `\"12\"` 而不是 `\"1\"、\"2\"`。"
        "不想引入 `re` 时，`\"\".join(c if c.isdigit() else \" \" for c in s).split()` "
        "是同样效果的手写版。"
    ),
    input_format="一行字符串（长度 ≤ 10⁵，可含字母、数字、标点、空格）。",
    output_format="三行，如题面所述。数字按十进制解释，前导零忽略。",
    constraints_md="- 1 ≤ 字符串长度 ≤ 10⁵\n- 每个数字串长度 ≤ 18（能用 int 直接装）",
    inputs=[
        "abc12de345\n",
        "no digits here\n",
        "2026-10-19\n",
        "0 00 000\n",
        "a1b22c333d4444\n",
    ],
    samples=2,
    oracle=_oracle_22,
    solution=r'''import re
import sys

s = sys.stdin.read()
nums = re.findall(r"\d+", s)
if not nums:
    print(0)
    print(0)
    print("EMPTY")
else:
    print(len(nums))
    print(sum(map(int, nums)))
    print(max(map(int, nums)))
''',
    alt=r'''import sys

s = sys.stdin.readline().rstrip("\n")
nums = "".join(c if c.isdigit() else " " for c in s).split()
if not nums:
    sys.stdout.write("0\n0\nEMPTY\n")
else:
    vals = list(map(int, nums))
    sys.stdout.write("%d\n%d\n%d\n" % (len(vals), sum(vals), max(vals)))
''',
)


def _oracle_23(text: str) -> str:
    n = int(text.split()[0])
    return "%s\n%s\n%s\n%.3f\n" % (str(n).zfill(8), format(n, "x"),
                                   format(n, "b"), n / 3.0)

add(
    title="格式化输出四连",
    section="技巧特训 · Python",
    difficulty=2, score=10, tags=["技巧特训", "f-string", "format", "补零"],
    statement_md=(
        "读入一个非负整数 `n`，输出四行：\n\n"
        "1. 八位、左侧补零的十进制写法\n"
        "2. 十六进制（小写，不带 `0x`）\n"
        "3. 二进制（不带 `0b`）\n"
        "4. `n / 3` 保留 3 位小数\n\n"
        "★ 技巧点：`f\"{n:08d}\"` 的格式说明符 `[填充][对齐][宽度][类型]`——"
        "`08d` = 补 0、宽 8、十进制；`x` 十六进制、`b` 二进制、`.3f` 三位小数。"
        "同一套说明符 `format()` 和 `%` 风格都能用，但 f-string 最直观。"
        "输出题里对齐、补零、定点小数几乎必考。"
    ),
    input_format="一行一个整数 `n`。",
    output_format="四行，如题面所述。",
    constraints_md="- 0 ≤ n ≤ 10⁹",
    inputs=[
        "7\n",
        "0\n",
        "123456789\n",
        "1000000000\n",
        "42\n",
    ],
    samples=2,
    oracle=_oracle_23,
    solution=r'''import sys

n = int(sys.stdin.read())
print(f"{n:08d}")
print(f"{n:x}")
print(f"{n:b}")
print(f"{n / 3:.3f}")
''',
    alt=r'''import sys

n = int(sys.stdin.read())
print(format(n, "08d"))
print(format(n, "x"))
print(format(n, "b"))
print(format(n / 3, ".3f"))
''',
)


def _oracle_24(text: str) -> str:
    d = text.split()
    i = 0
    n = int(d[i]); i += 1
    m = int(d[i]); i += 1
    a = []
    for r in range(n):
        a.append([int(d[i + r * m + c]) for c in range(m)])
    out = ["%d %d" % (m, n)]
    for c in range(m):
        out.append(" ".join(str(a[r][c]) for r in range(n)))
    out.append(" ".join(str(max(a[r][c] for r in range(n))) for c in range(m)))
    return "\n".join(out) + "\n"

add(
    title="矩阵转置与列最大值",
    section="技巧特训 · Python",
    difficulty=2, score=10, tags=["技巧特训", "zip", "解包", "矩阵"],
    statement_md=(
        "读入 `n` 行 `m` 列的矩阵，输出：\n\n"
        "1. 一行两个数：转置后的行数 列数（即 `m n`）\n"
        "2. 转置后的矩阵（共 `m` 行，每行 `n` 个数）\n"
        "3. 一行 `m` 个数：原矩阵每一列的最大值\n\n"
        "★ 技巧点：`zip(*a)` 把「行列表」按列拉开——`list(zip(*a))` 就是转置，"
        "一行顶两重循环。`*a` 是解包：`zip(a[0], a[1], ...)`。"
        "配合 `max(col)` 直接拿列最大值，注意 `zip` 返回的是元组。"
    ),
    input_format="第一行 `n m`；随后 `n` 行，每行 `m` 个整数。",
    output_format="如题面所述，矩阵元素之间用单个空格分隔。",
    constraints_md="- 1 ≤ n, m ≤ 500\n- |元素| ≤ 10⁹",
    inputs=[
        "3 4\n1 2 3 4\n5 6 7 8\n9 10 11 12\n",
        "1 1\n5\n",
        "2 3\n-1 0 3\n7 -2 1\n",
        "4 1\n1\n2\n3\n4\n",
        "2 2\n0 0\n0 0\n",
    ],
    samples=2,
    oracle=_oracle_24,
    solution=r'''import sys

d = sys.stdin.read().split()
n, m = int(d[0]), int(d[1])
vals = list(map(int, d[2:2 + n * m]))
a = [vals[r * m:(r + 1) * m] for r in range(n)]
t = list(zip(*a))                 # ★ 转置：一行搞定
print(m, n)
for row in t:
    print(*row)
print(*[max(col) for col in t])
''',
    alt=r'''import sys

d = sys.stdin.read().split()
n, m = int(d[0]), int(d[1])
a = [[0] * m for _ in range(n)]
k = 2
for r in range(n):
    for c in range(m):
        a[r][c] = int(d[k]); k += 1
print(m, n)
for c in range(m):
    print(" ".join(str(a[r][c]) for r in range(n)))
print(" ".join(str(max(a[r][c] for r in range(n))) for c in range(m)))
''',
)


def _oracle_25(text: str) -> str:
    d = text.split()
    n = int(d[0])
    s = d[1]
    k = int(d[2])
    chars = sorted(s[:n])
    res = []

    def dfs(cur, used):
        if len(cur) == n:
            res.append("".join(cur))
            return
        for i in range(n):
            if not used[i]:
                used[i] = True
                cur.append(chars[i])
                dfs(cur, used)
                cur.pop()
                used[i] = False

    dfs([], [False] * n)
    return res[k - 1] + "\n"

add(
    title="字典序第 k 个排列",
    section="技巧特训 · Python",
    difficulty=3, score=20, tags=["技巧特训", "itertools", "permutations", "全排列"],
    statement_md=(
        "读入 `n`、一个长度 `n` 的字符串（字符互不相同）、以及 `k`，"
        "输出把这些字符**按字典序全排列**后的第 `k` 个（`k` 从 1 起）。\n\n"
        "★ 技巧点：`itertools.permutations(seq)` 按输入顺序产出全排列，**不是**字典序——"
        "所以要先 `sorted()` 再传给 `permutations`，这样产出的顺序恰好就是字典序。"
        "取第 k 个直接 `list(permutations(...))[k-1]`；`n ≤ 8` 时 `8! = 40320`，"
        "全部枚举完全够用，不必手写康托展开。"
    ),
    input_format="一行三个部分：`n`、字符串 `s`、`k`（空格分隔）。",
    output_format="一行：第 `k` 个排列的字符序列。",
    constraints_md="- 1 ≤ n ≤ 8\n- 1 ≤ k ≤ n!\n- `s` 由小写或大写字母组成，字符互不相同",
    inputs=[
        "3 abc 5\n",
        "1 z 1\n",
        "4 ABCD 24\n",
        "3 321 1\n",
        "5 abcde 100\n",
    ],
    samples=2,
    oracle=_oracle_25,
    solution=r'''import sys
from itertools import permutations

d = sys.stdin.read().split()
n, s, k = int(d[0]), d[1], int(d[2])
print("".join(list(permutations(sorted(s[:n])))[k - 1]))
''',
    alt=r'''import sys

d = sys.stdin.read().split()
n, s, k = int(d[0]), d[1], int(d[2])
a = sorted(s[:n])
for _ in range(k - 1):                 # 手写 next_permutation：原地推 k-1 次
    i = n - 2
    while i >= 0 and a[i] >= a[i + 1]:
        i -= 1
    j = n - 1
    while a[j] <= a[i]:
        j -= 1
    a[i], a[j] = a[j], a[i]
    a[i + 1:] = reversed(a[i + 1:])
print("".join(a))
''',
)


def _oracle_26(text: str) -> str:
    d = text.split()
    n = int(d[0])
    a = [int(x) for x in d[1:1 + n]]
    g = a[0]
    for x in a[1:]:
        u, v = g, x
        while v:
            u, v = v, u % v
        g = u
    l = a[0]
    for x in a[1:]:
        u, v = l, x
        while v:
            u, v = v, u % v
        l = l // u * x
    return "%d\n%d\n" % (g, l)

add(
    title="一堆数的最大公约数与最小公倍数",
    section="技巧特训 · Python",
    difficulty=2, score=15, tags=["技巧特训", "math.gcd", "math.lcm", "reduce"],
    statement_md=(
        "读入 `n` 个正整数，输出两行：这 `n` 个数的最大公约数、最小公倍数。\n\n"
        "★ 技巧点：`math.gcd` 只吃两个参数，多个数就靠 `functools.reduce` 折叠——"
        "`reduce(gcd, a)` 一行拿全体 gcd。Python 3.9 起还有 `math.lcm`。"
        "求 lcm 切记 `l = l // gcd(l, x) * x`：**先除后乘**，否则中间量可能白涨一大截。"
        "本题 `aᵢ ≤ 100`，lcm 最大只有几十位，Python 大整数直接装得下，不用取模。"
    ),
    input_format="第一行 `n`；第二行 `n` 个正整数（空格分隔）。",
    output_format="两行：gcd、lcm。",
    constraints_md="- 1 ≤ n ≤ 100\n- 1 ≤ aᵢ ≤ 100",
    inputs=[
        "3\n12 18 24\n",
        "1\n7\n",
        "4\n97 89 83 79\n",
        "5\n2 4 8 16 32\n",
        "6\n100 99 98 97 96 95\n",
    ],
    samples=2,
    oracle=_oracle_26,
    solution=r'''import sys
from functools import reduce
from math import gcd, lcm

d = sys.stdin.read().split()
n = int(d[0])
a = list(map(int, d[1:1 + n]))
print(reduce(gcd, a))
print(reduce(lcm, a))
''',
    alt=r'''import sys

d = sys.stdin.read().split()
n = int(d[0])
a = list(map(int, d[1:1 + n]))


def g2(x, y):
    while y:
        x, y = y, x % y
    return x


g = a[0]
l = a[0]
for x in a[1:]:
    g = g2(g, x)
    l = l // g2(l, x) * x          # 先除后乘，避免中间量膨胀
print(g)
print(l)
''',
)


def _oracle_27(text: str) -> str:
    x = int(text.split()[0])
    pc = 0
    t = x
    while t:
        pc += t & 1
        t >>= 1
    low = 1
    while not (x & low):
        low <<= 1
    high = 1
    while high * 2 <= x:
        high <<= 1
    return "%d\n%d\n%d\n" % (pc, low, high)

add(
    title="二进制里的三个位置",
    section="技巧特训 · Python",
    difficulty=3, score=20, tags=["技巧特训", "位运算", "lowbit", "bit_count"],
    statement_md=(
        "读入一个正整数 `x`，输出三行：\n\n"
        "1. 二进制里 1 的个数\n"
        "2. 最低位的 1 所代表的值（lowbit）\n"
        "3. 最高位的 1 所代表的值\n\n"
        "★ 技巧点：三个都是一行——`x.bit_count()`（3.10+）、`x & -x`（lowbit，"
        "树状数组的核心操作）、`1 << (x.bit_length() - 1)`（最高位）。"
        "负数是补码，`x & -x` 等价于 `x & (~x + 1)`。"
        "手写版注意 lowbit 别写成 `x & (x-1)`——那个是**抹掉**最低位的 1。"
    ),
    input_format="一行一个正整数 `x`。",
    output_format="三行，如题面所述。",
    constraints_md="- 1 ≤ x ≤ 10¹⁸",
    inputs=[
        "1\n",
        "6\n",
        "1000000000000000000\n",
        "13\n",
        "1024\n",
    ],
    samples=2,
    oracle=_oracle_27,
    solution=r'''import sys

x = int(sys.stdin.read())
print(x.bit_count())              # 二进制 1 的个数
print(x & -x)                     # lowbit：最低位的 1
print(1 << (x.bit_length() - 1))  # 最高位的 1
''',
    alt=r'''import sys

x = int(sys.stdin.read())
print(len([c for c in bin(x)[2:] if c == "1"]))
print(x & (~x + 1))               # lowbit 的补码写法
print(2 ** (len(bin(x)[2:]) - 1))
''',
)


def _oracle_28(text: str) -> str:
    d = text.split()
    n = int(d[0])
    a = [int(x) for x in d[1:1 + n]]
    best = 0

    def dfs(i, cur):
        nonlocal best
        if i == n:
            if cur > best:
                best = cur
            return
        dfs(i + 1, cur)
        dfs(i + 1, cur ^ a[i])

    dfs(0, 0)
    return "%d\n" % best

add(
    title="子集异或的最大值",
    section="技巧特训 · Python",
    difficulty=4, score=25, tags=["技巧特训", "位掩码", "子集枚举", "线性基"],
    statement_md=(
        "读入 `n` 个非负整数，从中任选若干（可以一个都不选）做异或，"
        "输出能得到的最大的异或值。\n\n"
        "★ 技巧点：`n ≤ 18` 时用**位掩码枚举子集**——`for mask in range(1 << n)`，"
        "第 i 位是 1 就表示选中 `a[i]`，总共 `2^n` 种，"
        "`if mask >> i & 1` 判断取不取。这是所有「选或不选」题目的万能起手式。\n\n"
        "进阶（另一套解）：`n` 到了 10⁵ 就得用**线性基**——把每个数往高位试插，"
        "插不进就异或掉，最终得到一组「基底」，再从高位往下贪心异或，O(n·位数)。"
        "本题两套解都在，可以对照着看。"
    ),
    input_format="第一行 `n`；第二行 `n` 个非负整数。",
    output_format="一行：最大异或值（一个数都不选时为 0）。",
    constraints_md="- 1 ≤ n ≤ 18\n- 0 ≤ aᵢ < 2²⁰",
    time_limit_ms=2000,
    inputs=[
        "3\n1 2 3\n",
        "1\n0\n",
        "4\n5 5 5 5\n",
        "18\n1 2 4 8 16 32 64 128 256 512 1024 2048 4096 8192 16384 32768 65536 131072\n",
        "5\n7 7 7 7 7\n",
    ],
    samples=2,
    oracle=_oracle_28,
    solution=r'''import sys

d = sys.stdin.read().split()
n = int(d[0])
a = list(map(int, d[1:1 + n]))
best = 0
for mask in range(1 << n):          # ★ 子集枚举
    cur = 0
    m = mask
    i = 0
    while m:
        if m & 1:
            cur ^= a[i]
        m >>= 1
        i += 1
    if cur > best:
        best = cur
print(best)
''',
    alt=r'''import sys

d = sys.stdin.read().split()
n = int(d[0])
a = list(map(int, d[1:1 + n]))
BITS = 62
p = [0] * BITS                     # 线性基
for x in a:
    for b in range(BITS - 1, -1, -1):
        if not (x >> b) & 1:
            continue
        if p[b] == 0:
            p[b] = x
            break
        x ^= p[b]
res = 0
for b in range(BITS - 1, -1, -1):
    if (res ^ p[b]) > res:
        res ^= p[b]
print(res)
''',
)


def _rand_big_case_29() -> str:
    """29 号的大用例：500×500 矩阵 + 500 次查询，固定种子可复现。"""
    import random
    rnd = random.Random(20261019)
    n = m = 500
    q = 500
    lines = ["%d %d" % (n, m)]
    for _ in range(n):
        lines.append(" ".join(str(rnd.randint(-1000, 1000)) for _ in range(m)))
    lines.append(str(q))
    for _ in range(q):
        x1 = rnd.randint(1, n)
        x2 = rnd.randint(x1, n)
        y1 = rnd.randint(1, m)
        y2 = rnd.randint(y1, m)
        lines.append("%d %d %d %d" % (x1, y1, x2, y2))
    return "\n".join(lines) + "\n"


def _oracle_29(text: str) -> str:
    d = text.split()
    i = 0
    n = int(d[i]); i += 1
    m = int(d[i]); i += 1
    a = []
    for r in range(n):
        a.append([int(d[i + k]) for k in range(m)])
        i += m
    rp = []
    for r in range(n):
        s = [0] * (m + 1)
        for c in range(m):
            s[c + 1] = s[c] + a[r][c]
        rp.append(s)
    q = int(d[i]); i += 1
    out = []
    for _ in range(q):
        x1 = int(d[i]); y1 = int(d[i + 1])
        x2 = int(d[i + 2]); y2 = int(d[i + 3])
        i += 4
        tot = 0
        for r in range(x1 - 1, x2):
            tot += rp[r][y2] - rp[r][y1 - 1]
        out.append(str(tot))
    return "".join(x + "\n" for x in out)

add(
    title="子矩阵和的 q 次查询",
    section="技巧特训 · Python",
    difficulty=4, score=25, tags=["技巧特训", "二维前缀和", "容斥", "查询"],
    statement_md=(
        "读入一个 `n × m` 的整数矩阵，再回答 `q` 次查询：每次给左上角 "
        "`(x1, y1)` 和右下角 `(x2, y2)`（下标从 1 起），输出这个子矩阵里所有数的和。\n\n"
        "★ 技巧点：**二维前缀和 + 容斥**。令 `S[i][j]` 为左上角 `(1,1)` 到 "
        "`(i,j)` 的子矩阵和，递推式\n\n"
        "```\nS[i][j] = a[i][j] + S[i-1][j] + S[i][j-1] - S[i-1][j-1]\n```\n\n"
        "查询就是四个角加减：`S[x2][y2] - S[x1-1][y2] - S[x2][y1-1] + S[x1-1][y1-1]`。"
        "预处理 `O(nm)`、每次查询 `O(1)`；暴力每次 `O(nm)` 在 `q = 10⁵` 时必超时。"
        "记忆口诀：**加两次、减两次，左上角加回来**。"
    ),
    input_format=(
        "第一行 `n m`；随后 `n` 行每行 `m` 个整数；\n"
        "接着一行 `q`；随后 `q` 行每行 `x1 y1 x2 y2`。"
    ),
    output_format="`q` 行，每行一个查询结果。",
    constraints_md="- 1 ≤ n, m ≤ 500\n- 1 ≤ q ≤ 500\n- |元素| ≤ 10³",
    time_limit_ms=2000,
    inputs=[
        "3 3\n1 2 3\n4 5 6\n7 8 9\n3\n1 1 2 2\n2 2 3 3\n1 2 3 3\n",
        "1 1\n-5\n1\n1 1 1 1\n",
        "2 4\n1 -2 3 -4\n5 6 -7 8\n2\n1 1 2 4\n1 2 1 3\n",
        _rand_big_case_29(),
    ],
    samples=2,
    oracle=_oracle_29,
    solution=r'''import sys

data = sys.stdin.buffer.read().split()
it = iter(data)
n = int(next(it)); m = int(next(it))
S = [[0] * (m + 1) for _ in range(n + 1)]
for r in range(1, n + 1):
    row = S[r]
    prev = S[r - 1]
    acc = 0
    for c in range(1, m + 1):
        acc += int(next(it))
        row[c] = prev[c] + acc        # 二维前缀和
q = int(next(it))
out = []
for _ in range(q):
    x1 = int(next(it)); y1 = int(next(it))
    x2 = int(next(it)); y2 = int(next(it))
    out.append(str(S[x2][y2] - S[x1 - 1][y2] - S[x2][y1 - 1] + S[x1 - 1][y1 - 1]))
sys.stdout.write("\n".join(out) + "\n")
''',
    alt=r'''import sys

data = sys.stdin.buffer.read().split()
it = iter(data)
n = int(next(it)); m = int(next(it))
C = [[0] * (n + 1) for _ in range(m + 1)]   # 按列建一维前缀
for r in range(1, n + 1):
    for c in range(1, m + 1):
        C[c][r] = int(next(it))
for c in range(1, m + 1):
    col = C[c]
    for r in range(1, n + 1):
        col[r] += col[r - 1]
q = int(next(it))
out = []
for _ in range(q):
    x1 = int(next(it)); y1 = int(next(it))
    x2 = int(next(it)); y2 = int(next(it))
    tot = 0
    for c in range(y1, y2 + 1):
        tot += C[c][x2] - C[c][x1 - 1]   # 每列 O(1)，整体 O(列数)
    out.append(str(tot))
sys.stdout.write("\n".join(out) + "\n")
''',
)


def _rand_big_case_30() -> str:
    """30 号的大用例：n = 3000、k = 100，固定种子可复现。"""
    import random
    rnd = random.Random(20261019)
    n, k = 3000, 100
    return ("%d %d\n" % (n, k)
            + " ".join(str(rnd.randint(-1000, 1000)) for _ in range(n)) + "\n")


def _oracle_30(text: str) -> str:
    d = text.split()
    n = int(d[0]); k = int(d[1])
    a = [int(x) for x in d[2:2 + n]]
    out = []
    for i in range(n - k + 1):
        out.append(str(max(a[i:i + k])))
    return " ".join(out) + "\n"

add(
    title="滑窗最大值（deque）",
    section="技巧特训 · Python",
    difficulty=3, score=20, tags=["技巧特训", "deque", "单调队列", "滑动窗口"],
    statement_md=(
        "读入 `n`、窗口长度 `k` 和 `n` 个整数，从左往右滑动大小为 `k` 的窗口，"
        "依次输出每个窗口里的最大值（共 `n-k+1` 个，空格分隔，一行）。\n\n"
        "★ 技巧点：**单调队列**。`collections.deque` 里存**下标**，"
        "保证队首对应的值最大、值从队首到队尾单调递减：\n\n"
        "1. 新元素进来前，把队尾所有 ≤ 它的都弹掉（它们永远不可能再当最大值）\n"
        "2. 入队\n"
        "3. 队首下标如果已经滑出窗口，弹掉\n\n"
        "每个元素最多进出队各一次 → `O(n)`。用 `max(a[i:i+k])` 是 `O(nk)`，"
        "`k = n/2` 时退化到 `O(n²)`。另一套解用 `heapq` + 惰性删除（`O(n log n)`），"
        "思路更直观但常数更大。"
    ),
    input_format="第一行 `n k`；第二行 `n` 个整数。",
    output_format="一行 `n-k+1` 个整数，空格分隔。",
    constraints_md="- 1 ≤ k ≤ n ≤ 3000\n- |元素| ≤ 10⁹",
    time_limit_ms=2000,
    inputs=[
        "8 3\n1 3 -1 -3 5 3 6 7\n",
        "1 1\n5\n",
        "5 5\n9 8 7 6 5\n",
        "6 2\n-1 -2 -3 -4 -5 -6\n",
        _rand_big_case_30(),
    ],
    samples=2,
    oracle=_oracle_30,
    solution=r'''import sys
from collections import deque


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); k = int(data[1])
    a = list(map(int, data[2:2 + n]))
    dq = deque()                  # 存下标，对应值从大到小
    out = []
    for i, v in enumerate(a):
        while dq and a[dq[-1]] <= v:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(str(a[dq[0]]))
    sys.stdout.write(" ".join(out) + "\n")


main()
''',
    alt=r'''import sys
import heapq

data = sys.stdin.buffer.read().split()
n = int(data[0]); k = int(data[1])
a = list(map(int, data[2:2 + n]))
h = []
out = []
for i, v in enumerate(a):
    heapq.heappush(h, (-v, i))          # 大根堆（存负值）+ 惰性删除
    if i >= k - 1:
        while h[0][1] <= i - k:
            heapq.heappop(h)
        out.append(str(-h[0][0]))
sys.stdout.write(" ".join(out) + "\n")
''',
)


# --------------------------------------------------------------------- #

HEADER = '''"""Python 技巧特训题库 —— **自动生成，不要手改**。

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

PY_TRICKS_PROBLEMS: list[dict] = '''


def build() -> list[dict]:
    out: list[dict] = []
    for p in PROBLEMS:
        n_sample = int(p.get("samples", 1))
        cases = []
        for i, inp in enumerate(p["inputs"]):
            exp = p["oracle"](inp)
            if not isinstance(exp, str):
                raise SystemExit("题目《%s》第 %d 个输入的 oracle 返回了 %s（应为 str）"
                                 % (p["title"], i + 1, type(exp).__name__))
            is_s = i < n_sample
            cases.append({
                "stdin": inp,
                "expected_stdout": exp,
                "is_sample": 1 if is_s else 0,
                "kind": "sample" if is_s else "manual",
                "explanation": "",
            })
        out.append({
            "title": p["title"],
            "subject": "python",
            "line": "python",
            "difficulty": int(p.get("difficulty", 2)),
            "total_score": int(p.get("score", 10)),
            "tags": list(p.get("tags", [])),
            "statement_md": p["statement_md"],
            "input_format": p.get("input_format", ""),
            "output_format": p.get("output_format", ""),
            "constraints_md": p.get("constraints_md", ""),
            "time_limit_ms": int(p.get("time_limit_ms", 1000)),
            "memory_limit_mb": int(p.get("memory_limit_mb", 256)),
            "checker": "standard",
            "float_eps": 1e-6,
            "origin": "manual",
            "status": "published",
            "source_section": p["section"],
            "reference_solution": p["solution"],
            "alt_solution": p["alt"],
            "cases": cases,
        })
    return out


def _dump(probs: list[dict]) -> str:
    body = json.dumps(probs, ensure_ascii=False, indent=4)
    body = body.replace(": null", ": None").replace(": true", ": True").replace(": false", ": False")
    return HEADER + body + "\n"


def _sanity(probs: list[dict]) -> list[str]:
    problems: list[str] = []
    seen: set[str] = set()
    for i, p in enumerate(probs, 1):
        t = p["title"]
        if t in seen:
            problems.append("[%d] 标题重复：%s" % (i, t))
        seen.add(t)
        for k in ("statement_md", "input_format", "output_format",
                  "reference_solution", "alt_solution", "source_section"):
            if not str(p.get(k) or "").strip():
                problems.append("[%d] %s 缺字段 %s" % (i, t, k))
        if not p["cases"]:
            problems.append("[%d] %s 没有测试用例" % (i, t))
        if p["total_score"] <= 0:
            problems.append("[%d] %s 满分非法" % (i, t))
        for j, c in enumerate(p["cases"], 1):
            if not c["expected_stdout"]:
                problems.append("[%d] %s 第 %d 个用例期望输出为空" % (i, t, j))
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description="生成 Python 技巧特训题库")
    ap.add_argument("--check", action="store_true", help="只校验，不写文件")
    args = ap.parse_args()

    probs = build()
    total_cases = sum(len(p["cases"]) for p in probs)
    total_score = sum(p["total_score"] for p in probs)
    print("题目数：%d    测试点：%d    总分：%d"
          % (len(probs), total_cases, total_score))

    bad = _sanity(probs)
    if bad:
        print("★ 自检不通过：")
        for b in bad:
            print("   " + b)
        return 1
    print("自检通过 ✅")

    empties = [p["title"] for p in probs
               if any(c["expected_stdout"].strip() == "" and c["expected_stdout"] != "\n"
                      for c in p["cases"])]
    if empties:
        print("★ 期望输出为空的题：%s" % "、".join(empties))
        return 1

    if args.check:
        return 0

    OUT_PATH.write_text(_dump(probs), encoding="utf-8", newline="\n")
    print("已写入 %s（%d 字节）" % (OUT_PATH, OUT_PATH.stat().st_size))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
