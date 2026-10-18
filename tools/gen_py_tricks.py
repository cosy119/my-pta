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
