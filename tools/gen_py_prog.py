# -*- coding: utf-8 -*-
"""Python 编程精练题库生成器 —— 「编程精练 · Python」分节。

与「技巧特训 · Python」的分工：
  - 技巧特训 = 讲义没讲、但做题时**能一行省掉十行**的简便用法（Counter / 切片 / heapq）
  - 编程精练 = **老老实实把数据结构和算法自己实现一遍**（栈、队列、归并、Dijkstra、DP）

每道题：
  title / section / difficulty / score / tags
  statement_md / input_format / output_format / constraints_md
  inputs   ← 测试点输入（手写 + 固定种子生成，可复现）
  samples  ← 前几个当样例（其余为隐藏测试点）
  oracle   ← **独立 Python 实现，故意走"笨办法"**，与参考解不同路，
             这样「参考解写错」和「oracle 写错」不会同时错成一样
  solution / alt ← 两套 Python 实现（verify_bank 双撞）

章节结构（difficulty 2 → 4 递进）：
  基本功    4 题（栈判括号 / 约瑟夫环 / Kadane / 任意进制）
  矩阵与串  2 题（矩阵乘法转置 / 词频稳定排序）
  分治与查找 2 题（二分首末位置 / 归并数逆序对）
  图上与 DP  2 题（堆优化 Dijkstra / 编辑距离 + LCS）

★ 全库标题必须唯一（seed.ensure 按 title 判重，撞名会被静默跳过）。
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "app" / "problems_bank_py_prog.py"

SECTION = "编程精练 · Python"

PROBLEMS: list[dict] = []


def add(**kw) -> None:
    PROBLEMS.append(kw)


# --------------------------------------------------------------------- #
#  基本功（difficulty 2）
# --------------------------------------------------------------------- #

def _oracle_01(text: str) -> str:
    """括号匹配：不借 dict，直接一堆 if 判配对（笨办法）。"""
    s = text.rstrip("\n")
    stack: list[str] = []
    bad = 0
    for i, ch in enumerate(s):
        if ch in "([{":
            stack.append(ch)
            continue
        if ch in ")]}":
            if not stack:
                bad = i + 1
                break
            top = stack.pop()
            ok = ((top == "(" and ch == ")")
                  or (top == "[" and ch == "]")
                  or (top == "{" and ch == "}"))
            if not ok:
                bad = i + 1
                break
    if bad == 0 and stack:
        bad = len(s) + 1
    return ("YES" if bad == 0 else "NO") + "\n%d\n" % bad


add(
    title="括号匹配的栈实现",
    section=SECTION,
    difficulty=2, score=10, tags=["编程精练", "栈", "括号匹配"],
    statement_md=(
        "读入一行只由 `()[]{}` 六种字符组成的字符串（可以为空），判断括号是否**正确配对**，"
        "并给出第一个出错的位置。\n\n"
        "输出两行：\n"
        "1. `YES` 或 `NO`\n"
        "2. 第一个出错的位置（**1-based**）；完全匹配输出 `0`\n\n"
        "出错位置的定义（按扫描顺序，先到先算）：\n"
        "- 遇到右括号但栈为空 → 该右括号的位置\n"
        "- 遇到右括号但栈顶不是与之配对的左括号 → 该右括号的位置\n"
        "- 全部扫完后栈非空（左括号多余）→ `len(s) + 1`\n\n"
        "★ 为什么用栈：括号配对是**后进先出**——最近一个还没闭合的左括号，"
        "才是当前右括号该配的对象。这就是栈最经典的应用场景。"
    ),
    input_format="一行字符串（长度 ≤ 10⁵，只含 `()[]{}`）。空行表示空串。",
    output_format="两行：`YES`/`NO`，以及出错位置（整数）。",
    constraints_md="- 0 ≤ len(s) ≤ 10⁵\n- 字符集仅 `()[]{}`",
    inputs=[
        "([]){}\n",
        "([)]\n",
        "(\n",
        ")\n",
        "\n",
        "{[()()]}\n",
        "((((\n",
        "()])\n",
    ],
    samples=3,
    oracle=_oracle_01,
    solution=r'''import sys

PAIR = {")": "(", "]": "[", "}": "{"}

s = sys.stdin.readline().rstrip("\n")
st = []
bad = 0
for i, ch in enumerate(s):
    if ch in "([{":
        st.append(ch)
    elif ch in PAIR:
        if not st or st[-1] != PAIR[ch]:
            bad = i + 1
            break
        st.pop()
if bad == 0 and st:
    bad = len(s) + 1
print("YES" if bad == 0 else "NO")
print(bad)
''',
    alt=r'''import sys

s = sys.stdin.readline().rstrip("\n")

# 另一条路：反复消除成对的 ()[]{}，消不掉就是有问题的。
# 严格说这个写法判不出"第一个出错位置"的精确语义，
# 所以位置单独再扫一遍——但「是否匹配」的结论来自完全不同的机制。
prev = None
cur = s
while prev != cur:
    prev = cur
    for pair in ("()", "[]", "{}"):
        cur = cur.replace(pair, "")

ok = (cur == "")
bad = 0
if not ok:
    stack = []
    pairs = {")": "(", "]": "[", "}": "{"}
    for i, ch in enumerate(s):
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack[-1] != pairs[ch]:
                bad = i + 1
                break
            stack.pop()
    if bad == 0 and stack:
        bad = len(s) + 1
print("YES" if ok else "NO")
print(bad)
''',
)


def _oracle_02(text: str) -> str:
    """约瑟夫环：直接开一个列表，每次数到 k 就 pop（最笨的模拟）。"""
    d = text.split()
    n, k = int(d[0]), int(d[1])
    people = list(range(1, n + 1))
    out: list[int] = []
    idx = 0
    while people:
        idx = (idx + k - 1) % len(people)
        out.append(people.pop(idx))
        if idx == len(people):
            idx = 0
    return " ".join(map(str, out)) + "\n%d\n" % out[-1]


add(
    title="约瑟夫环报数出列",
    section=SECTION,
    difficulty=2, score=10, tags=["编程精练", "队列", "模拟", "约瑟夫环"],
    statement_md=(
        "`n` 个人围成一圈，编号 `1..n`。从 1 号开始报数，每数到第 `k` 个人就出列，"
        "然后从下一个人重新从 1 报数，直到所有人出列。\n\n"
        "输出两行：\n"
        "1. 出列顺序（空格分隔）\n"
        "2. 最后出列（也就是活到最后）的那个人的编号\n\n"
        "★ 两种思路：\n"
        "- **模拟**：用队列一路 `pop` / 位移动，直观但要 O(nk)；\n"
        "- **递推**：只要最后剩下的编号时，`f(1)=0`、`f(i)=(f(i-1)+k) % i`，"
        "答案就是 `f(n)+1`，O(n) 且不用真的排队。"
    ),
    input_format="一行两个整数 `n k`。",
    output_format="两行：出列顺序；最后剩下的人。",
    constraints_md="- 1 ≤ n ≤ 2000\n- 1 ≤ k ≤ 10⁹",
    inputs=[
        "5 3\n",
        "1 1\n",
        "7 2\n",
        "10 1\n",
        "6 10\n",
        "100 7\n",
    ],
    samples=3,
    oracle=_oracle_02,
    solution=r'''import sys
from collections import deque

n, k = map(int, sys.stdin.readline().split())
q = deque(range(1, n + 1))
out = []
while q:
    q.rotate(-((k - 1) % len(q)))
    out.append(q.popleft())
print(" ".join(map(str, out)))
print(out[-1])
''',
    alt=r'''import sys

n, k = map(int, sys.stdin.readline().split())

# 出列顺序用链表模拟（朴素下标推进），最后一个人用递推公式独立算
survivors = list(range(1, n + 1))
out = []
pos = 0
for _ in range(n):
    pos = (pos + k - 1) % len(survivors)
    out.append(survivors.pop(pos))
    if pos == len(survivors) and survivors:
        pos = 0

# 递推（0-based）：f(1)=0, f(i)=(f(i-1)+k)%i
last = 0
for i in range(2, n + 1):
    last = (last + k) % i
print(" ".join(map(str, out)))
print(last + 1)
''',
)


def _oracle_03(text: str) -> str:
    """最大子段和：三重循环枚举所有区间（O(n³) 的笨办法，只在小数据上用）。"""
    d = text.split()
    n = int(d[0])
    a = [int(v) for v in d[1:1 + n]]
    best = None
    bi = bj = 0
    for i in range(n):
        s = 0
        for j in range(i, n):
            s += a[j]
            if best is None or s > best:
                best, bi, bj = s, i, j
    return "%d\n%d %d\n" % (best, bi + 1, bj + 1)


def _rand_subarray_case() -> str:
    import random
    rnd = random.Random(20261019)
    n = 500
    a = [rnd.randint(-100, 100) for _ in range(n)]
    return "%d\n%s\n" % (n, " ".join(map(str, a)))


add(
    title="最大连续子段和",
    section=SECTION,
    difficulty=2, score=10, tags=["编程精练", "动态规划", "Kadane"],
    statement_md=(
        "读入长度 `n` 的整数序列，找出**和最大**的连续子段，输出这个和以及该段的起止下标"
        "（**1-based**）。\n\n"
        "并列的处理：和相同时取**起点更小**的那段；起点也相同取**终点更小**的那段。\n\n"
        "★ Kadane 算法的核心只有一句话：**如果「前面的累计和」是负的，那它对后面只有拖累，"
        "直接从当前元素重新开始**。于是 `cur = max(a[i], cur + a[i])`。\n\n"
        "⚠️ 全负数序列不能把答案初始化成 0——那样会返回「空段」的和 0。"
        "必须用第一个元素或 −∞ 起手。"
    ),
    input_format="第一行 `n`；第二行 `n` 个整数。",
    output_format="两行：最大和；起止下标（空格分隔）。",
    constraints_md="- 1 ≤ n ≤ 10⁵\n- |aᵢ| ≤ 10⁴",
    inputs=[
        "5\n-2 1 -3 4 -1 2 1 -5 4\n",
        "1\n-7\n",
        "4\n-1 -2 -3 -4\n",
        "3\n1 2 3\n",
        "6\n2 -1 2 -1 2 -1\n",
        _rand_subarray_case(),
    ],
    samples=3,
    oracle=_oracle_03,
    solution=r'''import sys

data = sys.stdin.read().split()
n = int(data[0])
a = [int(v) for v in data[1:1 + n]]

best = a[0]
best_l = best_r = 0
cur = a[0]
cur_l = 0
for i in range(1, n):
    if cur < 0:
        cur = a[i]
        cur_l = i
    else:
        cur += a[i]
    if cur > best:
        best = cur
        best_l, best_r = cur_l, i
print(best)
print(best_l + 1, best_r + 1)
''',
    alt=r'''import sys

data = sys.stdin.read().split()
n = int(data[0])
a = [int(v) for v in data[1:1 + n]]

# 换个角度：前缀和。区间 [l, r] 的和 = pre[r+1] - pre[l]，
# 要让差最大 => 在 r 处减去「之前见过的最小前缀」。
pre = 0
min_pre = 0
min_pre_at = 0          # 这个最小前缀出现在第几个元素之前
best = None
best_l = best_r = 0
for r in range(n):
    pre += a[r]
    if best is None or pre - min_pre > best:
        best = pre - min_pre
        best_l, best_r = min_pre_at, r
    if pre < min_pre:
        min_pre = pre
        min_pre_at = r + 1
print(best)
print(best_l + 1, best_r + 1)
''',
)


def _oracle_04(text: str) -> str:
    """任意进制互转：不调 int(s, base)，自己按权值累加。"""
    d = text.split()
    src, b1, b2 = d[0], int(d[1]), int(d[2])
    DIG = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    neg = src.startswith("-")
    body = src[1:] if neg else src
    val = 0
    for ch in body:
        val = val * b1 + DIG.index(ch.upper())
    if val == 0:
        return "0\n"
    out = ""
    while val:
        out = DIG[val % b2] + out
        val //= b2
    return ("-" if neg else "") + out + "\n"


add(
    title="任意进制转换",
    section=SECTION,
    difficulty=2, score=10, tags=["编程精练", "进制", "字符串处理"],
    statement_md=(
        "读入一行 `n b1 b2`：`n` 是一个 `b1` 进制的数（可能是负数），"
        "把它转成 `b2` 进制输出。\n\n"
        "数字用 `0-9` 与 `A-Z` 表示（`A` = 10，`Z` = 35），输出字母**一律大写**。\n"
        "负数保留前导 `-`；值为 0 时输出 `0`（不输出 `-0`）。\n\n"
        "★ 原理只有一个：**权值展开**。`\"12F\"` 在 16 进制下 = `1×16² + 2×16 + 15`；"
        "反向则不断**取余得低位、整除降位**，最后把余数倒过来。\n\n"
        "⚠️ 别依赖 `int(s, base)` / `bin()` / `hex()` 一步到位——"
        "它们最多支持到 36 进制，而且 `hex()` 会带 `0x` 前缀、字母小写。"
    ),
    input_format="一行 `n b1 b2`（`n` 是不含前导零的字符串）。",
    output_format="一行，转换后的 `b2` 进制表示。",
    constraints_md="- 2 ≤ b1, b2 ≤ 36\n- `n` 的绝对值 ≤ 10¹⁸\n- 输入保证合法",
    inputs=[
        "255 10 16\n",
        "-255 10 16\n",
        "FF 16 2\n",
        "0 10 7\n",
        "zz 36 10\n",
        "-1010 2 8\n",
        "777 8 9\n",
    ],
    samples=3,
    oracle=_oracle_04,
    solution=r'''import sys

DIG = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

src, b1, b2 = sys.stdin.readline().split()
b1, b2 = int(b1), int(b2)
neg = src.startswith("-")
if neg:
    src = src[1:]

val = 0
for ch in src:
    val = val * b1 + DIG.index(ch.upper())

if val == 0:
    print(0)
else:
    buf = []
    while val:
        buf.append(DIG[val % b2])
        val //= b2
    print(("-" if neg else "") + "".join(reversed(buf)))
''',
    alt=r'''import sys

DIG = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

src, b1, b2 = sys.stdin.readline().split()
b1, b2 = int(b1), int(b2)
neg = src.startswith("-")
if neg:
    src = src[1:]

# 解析走 Horner 之外的写法：按位权累加（从高位到低位配指数）
val = 0
n = len(src)
for i, ch in enumerate(src):
    val += DIG.index(ch.upper()) * (b1 ** (n - 1 - i))

# 转换用「逐位 divmod」的递归写法
def to_base(v: int, base: int) -> str:
    if v == 0:
        return ""
    q, r = divmod(v, base)
    return to_base(q, base) + DIG[r]

if val == 0:
    print(0)
else:
    print(("-" if neg else "") + to_base(val, b2))
''',
)


# --------------------------------------------------------------------- #
#  矩阵与串（difficulty 3）
# --------------------------------------------------------------------- #

def _oracle_05(text: str) -> str:
    """矩阵乘法：完全朴素三重循环 + 手工转置。"""
    it = iter(text.split())
    n, m, p = int(next(it)), int(next(it)), int(next(it))
    A = [[int(next(it)) for _ in range(m)] for _ in range(n)]
    B = [[int(next(it)) for _ in range(p)] for _ in range(m)]
    lines = []
    for i in range(n):
        row = []
        for j in range(p):
            s = 0
            for k in range(m):
                s += A[i][k] * B[k][j]
            row.append(s)
        lines.append(" ".join(map(str, row)))
    lines.append("")
    for j in range(m):
        lines.append(" ".join(str(A[i][j]) for i in range(n)))
    return "\n".join(lines) + "\n"


add(
    title="矩阵乘法与转置",
    section=SECTION,
    difficulty=3, score=12, tags=["编程精练", "矩阵", "循环顺序"],
    statement_md=(
        "读入 `n m p` 和矩阵 `A`（`n×m`）、矩阵 `B`（`m×p`），按行读入。\n\n"
        "输出：\n"
        "1. 乘积 `C = A × B` 的 `n` 行\n"
        "2. 一个**空行**\n"
        "3. `A` 的转置的 `m` 行\n\n"
        "★ 乘法要三层循环，但**循环顺序不是随便放**：写成 `i-k-j`（把 `A[i][k]` 提到内层外面）"
        "时，内层循环访问 `C[i][j]` 与 `B[k][j]` 都是**顺序**的，缓存命中率高；"
        "写成 `i-j-k` 则每次内层都在跳着访问 `B`。小矩阵看不出差别，几千规模能差好几倍。\n\n"
        "★ 转置用 `zip(*A)` 一行就能做——`zip` 会把每行的同列元素打包成元组。"
    ),
    input_format="第一行 `n m p`；接着 `n` 行是 A，再 `m` 行是 B（同行元素空格分隔）。",
    output_format="`n` 行乘积、一个空行、`m` 行转置。",
    constraints_md="- 1 ≤ n, m, p ≤ 100\n- |元素| ≤ 100",
    inputs=[
        "2 3 2\n1 2 3\n4 5 6\n7 8\n9 10\n11 12\n",
        "1 1 1\n5\n-7\n",
        "2 2 2\n1 0\n0 1\n3 4\n5 6\n",
        "3 1 3\n2\n3\n4\n1 2 3\n",
    ],
    samples=3,
    oracle=_oracle_05,
    solution=r'''import sys

data = list(map(int, sys.stdin.buffer.read().split()))
n, m, p = data[0], data[1], data[2]
pos = 3
A = [[0] * m for _ in range(n)]
for i in range(n):
    for j in range(m):
        A[i][j] = data[pos]
        pos += 1
B = [[0] * p for _ in range(m)]
for i in range(m):
    for j in range(p):
        B[i][j] = data[pos]
        pos += 1

C = [[0] * p for _ in range(n)]
for i in range(n):
    Ai = A[i]
    Ci = C[i]
    for k in range(m):
        a = Ai[k]
        if a == 0:
            continue
        Bk = B[k]
        for j in range(p):
            Ci[j] += a * Bk[j]

out = [" ".join(map(str, row)) for row in C]
out.append("")
for j in range(m):
    out.append(" ".join(str(A[i][j]) for i in range(n)))
sys.stdout.write("\n".join(out) + "\n")
''',
    alt=r'''import sys

data = list(map(int, sys.stdin.buffer.read().split()))
n, m, p = data[0], data[1], data[2]
pos = 3
A = [data[pos + i * m: pos + (i + 1) * m] for i in range(n)]
pos += n * m
B = [data[pos + i * p: pos + (i + 1) * p] for i in range(m)]

# 转置 B，把「列」变成「行」，于是每个 C[i][j] 就是两个列表的点积
Bt = [list(col) for col in zip(*B)]
out = []
for i in range(n):
    row = []
    for j in range(p):
        row.append(sum(x * y for x, y in zip(A[i], Bt[j])))
    out.append(" ".join(map(str, row)))
out.append("")
for col in zip(*A):
    out.append(" ".join(map(str, col)))
sys.stdout.write("\n".join(out) + "\n")
''',
)


def _oracle_06(text: str) -> str:
    """词频：先切词、再手写插入排序（稳定但慢），验证 sorted 的结论。"""
    words: dict[str, int] = {}
    cur = []
    for ch in text:
        if ch.isalpha() or ch == "'":
            cur.append(ch)
        else:
            if cur:
                w = "".join(cur).lower()
                words[w] = words.get(w, 0) + 1
                cur = []
    if cur:
        w = "".join(cur).lower()
        words[w] = words.get(w, 0) + 1
    items = list(words.items())
    # 冒泡排序：频次降序、同频字典序升序
    n = len(items)
    for i in range(n):
        for j in range(n - 1 - i):
            a, b = items[j], items[j + 1]
            if (a[1], b[0]) < (b[1], a[0]):
                items[j], items[j + 1] = b, a
    return "".join("%s %d\n" % (w, c) for w, c in items)


add(
    title="词频统计的稳定排序",
    section=SECTION,
    difficulty=3, score=12, tags=["编程精练", "字典", "排序", "Counter"],
    statement_md=(
        "读入多行英文文本，统计每个单词出现的次数。单词定义为**连续的字母**"
        "（`A-Z`/`a-z`，可含词内的单引号 `'`），**大小写不敏感**，其余字符都是分隔符。\n\n"
        "输出：每行 `单词 次数`，按「**次数降序**，次数相同则**单词字典序升序**」排列。\n"
        "单词一律输出**小写**形式。\n\n"
        "★ 两趟排序的坑：`sorted(words.items(), key=lambda kv: -kv[1])` 只按次数排，"
        "同频词的先后是**字典的插入顺序**，不是字典序。要么把 key 写成 "
        "`(-次数, 单词)` 一次性排对，要么先按单词排一遍再按次数做**稳定**排序。"
    ),
    input_format="若干行英文文本（总长度 ≤ 10⁵）。",
    output_format="每行 `单词 次数`，按题面规则排序。",
    constraints_md="- 文本总长度 ≤ 10⁵\n- 至少含一个单词",
    inputs=[
        "the quick brown fox jumps over the lazy dog\nThe quick dog.\n",
        "a a a b b c\n",
        "Hello, hello! HELLO?\n",
        "don't stop don't\n",
        "one\n",
    ],
    samples=3,
    oracle=_oracle_06,
    solution=r'''import sys
import re
from collections import Counter

text = sys.stdin.read()
words = re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)*", text)
cnt = Counter(w.lower() for w in words)
for w, c in sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0])):
    print(w, c)
''',
    alt=r'''import sys

text = sys.stdin.read()
words = []
cur = []
for ch in text:
    if ch.isalpha() or ch == "'":
        cur.append(ch)
    elif cur:
        words.append("".join(cur).lower())
        cur = []
if cur:
    words.append("".join(cur).lower())

freq = {}
for w in words:
    freq[w] = freq.get(w, 0) + 1

# 两趟稳定排序：先字典序升序，再按次数降序（sorted 是稳定的，同频保持字典序）
items = sorted(freq.items())
items.sort(key=lambda kv: kv[1], reverse=True)
for w, c in items:
    print(w, c)
''',
)


# --------------------------------------------------------------------- #
#  分治与查找（difficulty 3）
# --------------------------------------------------------------------- #

def _oracle_07(text: str) -> str:
    """二分首末位置：不用 bisect，直接线性扫（笨办法）。"""
    it = iter(text.split())
    n = int(next(it))
    q = int(next(it))
    a = [int(next(it)) for _ in range(n)]
    out = []
    for _ in range(q):
        x = int(next(it))
        first = last = -1
        for i in range(n):
            if a[i] == x:
                if first == -1:
                    first = i
                last = i
        out.append("%d %d" % (first + 1 if first >= 0 else -1,
                              last + 1 if last >= 0 else -1))
    return "\n".join(out) + "\n"


def _rand_bisect_case() -> str:
    import random
    rnd = random.Random(4242)
    n = 3000
    a = sorted(rnd.randint(-1000, 1000) for _ in range(n))
    q = 300
    xs = [rnd.randint(-1100, 1100) for _ in range(q)]
    return "%d %d\n%s\n%s\n" % (n, q, " ".join(map(str, a)), " ".join(map(str, xs)))


add(
    title="二分查找的首末位置",
    section=SECTION,
    difficulty=3, score=12, tags=["编程精练", "二分查找", "bisect"],
    statement_md=(
        "给定一个**非降序**数组（可能有重复元素）和 `q` 个查询，"
        "对每个查询 `x` 输出 `x` 第一次和最后一次出现的下标（**1-based**）。不存在输出 `-1 -1`。\n\n"
        "★ 为什么不能「找到一个就停」：普通二分找到的只是**某一个**位置，"
        "它左右可能还有相同的值。要拿边界，得把二分改成**找边界**：\n"
        "- 找第一个 ≥ x 的位置 → 即 `x` 的起点（`bisect_left`）\n"
        "- 找第一个 > x 的位置，减 1 → 即 `x` 的终点（`bisect_right - 1`）\n\n"
        "★ 手写二分最容易死循环的地方是 `lo = mid` 配 `while lo < hi`——"
        "中点取整会下取整，`lo` 可能原地不动。**要么 `lo = mid + 1`，要么中点写成 `(lo+hi+1)//2`。**"
    ),
    input_format="第一行 `n q`；第二行 `n` 个整数（非降序）；第三行 `q` 个查询。",
    output_format="`q` 行，每行 `起点 终点`。",
    constraints_md="- 1 ≤ n ≤ 10⁵，1 ≤ q ≤ 10⁵\n- |元素| ≤ 10⁹",
    inputs=[
        "5 3\n1 2 2 2 5\n2 1 3\n",
        "1 2\n7\n7 8\n",
        "6 4\n-3 -3 -3 0 9 9\n-3 9 0 5\n",
        _rand_bisect_case(),
    ],
    samples=3,
    oracle=_oracle_07,
    solution=r'''import sys
from bisect import bisect_left, bisect_right

data = list(map(int, sys.stdin.buffer.read().split()))
n, q = data[0], data[1]
a = data[2:2 + n]
qs = data[2 + n: 2 + n + q]

out = []
for x in qs:
    lo = bisect_left(a, x)
    hi = bisect_right(a, x)
    if lo == hi:
        out.append("-1 -1")
    else:
        out.append("%d %d" % (lo + 1, hi))
sys.stdout.write("\n".join(out) + "\n")
''',
    alt=r'''import sys

data = list(map(int, sys.stdin.buffer.read().split()))
n, q = data[0], data[1]
a = data[2:2 + n]
qs = data[2 + n: 2 + n + q]


def first_ge(x):
    """第一个 >= x 的下标（不存在返回 n）"""
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo


def last_le(x):
    """最后一个 <= x 的下标（不存在返回 -1）"""
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] <= x:
            lo = mid + 1
        else:
            hi = mid
    return lo - 1


out = []
for x in qs:
    l = first_ge(x)
    r = last_le(x)
    if l > r:
        out.append("-1 -1")
    else:
        out.append("%d %d" % (l + 1, r + 1))
sys.stdout.write("\n".join(out) + "\n")
''',
)


def _oracle_08(text: str) -> str:
    """逆序对：O(n²) 双重循环硬数（笨办法，只在小数据上用）。"""
    d = text.split()
    n = int(d[0])
    a = [int(v) for v in d[1:1 + n]]
    cnt = 0
    for i in range(n):
        for j in range(i + 1, n):
            if a[i] > a[j]:
                cnt += 1
    return "%d\n%s\n" % (cnt, " ".join(map(str, sorted(a))))


def _rand_inv_py_case() -> str:
    import random
    rnd = random.Random(777)
    n = 1500
    a = [rnd.randint(-10 ** 9, 10 ** 9) for _ in range(n)]
    return "%d\n%s\n" % (n, " ".join(map(str, a)))


def _rev_case() -> str:
    n = 800
    return "%d\n%s\n" % (n, " ".join(str(n - i) for i in range(n)))


add(
    title="归并排序数逆序对",
    section=SECTION,
    difficulty=3, score=12, tags=["编程精练", "归并排序", "分治", "逆序对"],
    statement_md=(
        "读入 `n` 个整数，输出两行：\n"
        "1. **逆序对**个数（满足 `i < j` 且 `a[i] > a[j]` 的下标对）\n"
        "2. 升序排序后的序列（空格分隔）\n\n"
        "★ 为什么归并能数：合并两个**各自已有序**的左右半区时，"
        "只要右半区的当前元素比左半区当前元素小，"
        "那左半区**从当前位置到末尾的所有元素**都比它大——一次就能记下一整批逆序对。\n\n"
        "⚠️ 计数必须在「取右边元素」时加，且加的是 `mid - i + 1`（左半区剩余个数），"
        "不是 1。写成 +1 会得到「冒泡交换次数」的顺手估计，但不是逆序对数。\n\n"
        "⚠️ 逆序对最多有 `n(n-1)/2` 个，n = 10⁵ 时约 5×10⁹，**会溢出 int**，要用 64 位。"
    ),
    input_format="第一行 `n`；第二行 `n` 个整数。",
    output_format="两行：逆序对数；升序序列。",
    constraints_md="- 1 ≤ n ≤ 10⁵\n- |aᵢ| ≤ 10⁹",
    inputs=[
        "5\n5 4 3 2 1\n",
        "1\n42\n",
        "4\n1 2 3 4\n",
        "6\n2 2 1 3 1 2\n",
        _rev_case(),
        _rand_inv_py_case(),
    ],
    samples=3,
    oracle=_oracle_08,
    solution=r'''import sys

def main() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:1 + n]

    tmp = [0] * n
    cnt = 0

    def rec(lo: int, hi: int) -> None:
        nonlocal cnt
        if lo >= hi:
            return
        mid = (lo + hi) // 2
        rec(lo, mid)
        rec(mid + 1, hi)
        i, j, k = lo, mid + 1, lo
        while i <= mid and j <= hi:
            if a[i] <= a[j]:
                tmp[k] = a[i]
                i += 1
            else:
                tmp[k] = a[j]
                j += 1
                cnt += mid - i + 1
            k += 1
        while i <= mid:
            tmp[k] = a[i]
            i += 1
            k += 1
        while j <= hi:
            tmp[k] = a[j]
            j += 1
            k += 1
        a[lo:hi + 1] = tmp[lo:hi + 1]

    rec(0, n - 1)
    out = "%d\n%s\n" % (cnt, " ".join(map(str, a)))
    sys.stdout.write(out)

main()
''',
    alt=r'''import sys

def main() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:1 + n]

    # 另一条路：自底向上的迭代归并（不递归），宽度从 1 倍增
    tmp = [0] * n
    cnt = 0
    width = 1
    while width < n:
        lo = 0
        while lo < n:
            mid = min(lo + width - 1, n - 1)
            hi = min(lo + 2 * width - 1, n - 1)
            i, j, k = lo, mid + 1, lo
            while i <= mid and j <= hi:
                if a[i] <= a[j]:
                    tmp[k] = a[i]
                    i += 1
                else:
                    tmp[k] = a[j]
                    j += 1
                    cnt += mid - i + 1
                k += 1
            while i <= mid:
                tmp[k] = a[i]
                i += 1
                k += 1
            while j <= hi:
                tmp[k] = a[j]
                j += 1
                k += 1
            a[lo:hi + 1] = tmp[lo:hi + 1]
            lo += 2 * width
        width *= 2

    out = "%d\n%s\n" % (cnt, " ".join(map(str, a)))
    sys.stdout.write(out)

main()
''',
)


# --------------------------------------------------------------------- #
#  图上与 DP（difficulty 4）
# --------------------------------------------------------------------- #

def _oracle_09(text: str) -> str:
    """最短路：Bellman-Ford 松弛 n-1 轮（笨办法，与 Dijkstra 不同路）。"""
    it = iter(text.split())
    n = int(next(it))
    m = int(next(it))
    s = int(next(it))
    edges = []
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        w = int(next(it))
        edges.append((u, v, w))
    INF = float("inf")
    dist = [INF] * (n + 1)
    dist[s] = 0
    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break
    out = []
    for i in range(1, n + 1):
        out.append("INF" if dist[i] == INF else str(dist[i]))
    return " ".join(out) + "\n"


def _rand_graph_case() -> str:
    import random
    rnd = random.Random(20261020)
    n, m = 300, 1200
    lines = ["%d %d 1" % (n, m)]
    seen = set()
    cnt = 0
    while cnt < m:
        u = rnd.randint(1, n)
        v = rnd.randint(1, n)
        if u == v or (u, v) in seen:
            continue
        seen.add((u, v))
        lines.append("%d %d %d" % (u, v, rnd.randint(1, 1000)))
        cnt += 1
    return "\n".join(lines) + "\n"


add(
    title="单源最短路径的堆优化",
    section=SECTION,
    difficulty=4, score=14, tags=["编程精练", "图", "Dijkstra", "堆"],
    statement_md=(
        "给定 `n` 个点、`m` 条**有向**边（权值全为正）和起点 `s`，"
        "求 `s` 到每个点的最短距离。不可达输出 `INF`。\n\n"
        "输出一行，按点编号 `1..n` 顺序，空格分隔。\n\n"
        "★ 为什么朴素 Dijkstra 是 O(n²)、堆优化是 O(m log n)：朴素版每轮都要**线性扫一遍**"
        "找当前最近的未访问点；堆优化把这个「找最小」交给小根堆，"
        "而每条边带来的松弛最多往堆里塞一次，所以总共 `m` 次入堆、`m` 次出堆。\n\n"
        "★ 两个必须记住的细节：\n"
        "1. **懒删除**：出堆时若 `d > dist[u]` 说明是过期条目，直接 `continue`；\n"
        "2. **正权**是前提。有负权边时 Dijkstra 会错（该轮到被「重新变短」的点已经出堆了），"
        "要用 Bellman-Ford / SPFA。"
    ),
    input_format="第一行 `n m s`；接着 `m` 行 `u v w`（有向边 u→v，权 w）。",
    output_format="一行 `n` 个数：到 1..n 的最短距离，不可达为 `INF`。",
    constraints_md="- 1 ≤ n ≤ 10⁵，0 ≤ m ≤ 2×10⁵\n- 1 ≤ w ≤ 10⁹\n- 1 ≤ s ≤ n",
    inputs=[
        "4 5 1\n1 2 1\n1 3 4\n2 3 2\n2 4 6\n3 4 3\n",
        "3 0 2\n",
        "1 0 1\n",
        "5 4 1\n1 2 10\n2 3 10\n3 4 10\n4 5 10\n",
        _rand_graph_case(),
    ],
    samples=3,
    oracle=_oracle_09,
    solution=r'''import sys
import heapq


def main() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    n, m, s = data[0], data[1], data[2]
    head = [[] for _ in range(n + 1)]
    pos = 3
    for _ in range(m):
        u, v, w = data[pos], data[pos + 1], data[pos + 2]
        pos += 3
        head[u].append((v, w))

    INF = float("inf")
    dist = [INF] * (n + 1)
    dist[s] = 0
    h = [(0, s)]
    while h:
        d, u = heapq.heappop(h)
        if d > dist[u]:
            continue
        for v, w in head[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(h, (nd, v))

    out = []
    for i in range(1, n + 1):
        out.append("INF" if dist[i] == INF else str(dist[i]))
    sys.stdout.write(" ".join(out) + "\n")


main()
''',
    alt=r'''import sys

def main() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    n, m, s = data[0], data[1], data[2]

    # 邻接矩阵 + 朴素 O(n^2) Dijkstra（与堆优化完全不同的实现）
    INF = 10 ** 30
    g = [[INF] * (n + 1) for _ in range(n + 1)]
    pos = 3
    for _ in range(m):
        u, v, w = data[pos], data[pos + 1], data[pos + 2]
        pos += 3
        if w < g[u][v]:
            g[u][v] = w

    dist = [INF] * (n + 1)
    used = [False] * (n + 1)
    dist[s] = 0
    for _ in range(n):
        u = -1
        best = INF
        for i in range(1, n + 1):
            if not used[i] and dist[i] < best:
                best = dist[i]
                u = i
        if u < 0:
            break
        used[u] = True
        gu = g[u]
        for v in range(1, n + 1):
            if not used[v] and gu[v] < INF:
                nd = best + gu[v]
                if nd < dist[v]:
                    dist[v] = nd

    out = []
    for i in range(1, n + 1):
        out.append("INF" if dist[i] >= INF else str(dist[i]))
    sys.stdout.write(" ".join(out) + "\n")


main()
''',
)


def _oracle_10(text: str) -> str:
    """编辑距离 + LCS：纯递归记忆化，与 DP 迭代不同路。"""
    lines = text.split("\n")
    a = lines[0] if lines else ""
    b = lines[1] if len(lines) > 1 else ""

    from functools import lru_cache

    @lru_cache(maxsize=None)
    def ed(i: int, j: int) -> int:
        if i == 0:
            return j
        if j == 0:
            return i
        if a[i - 1] == b[j - 1]:
            return ed(i - 1, j - 1)
        return 1 + min(ed(i - 1, j), ed(i, j - 1), ed(i - 1, j - 1))

    @lru_cache(maxsize=None)
    def lcs(i: int, j: int) -> int:
        if i == 0 or j == 0:
            return 0
        if a[i - 1] == b[j - 1]:
            return lcs(i - 1, j - 1) + 1
        return max(lcs(i - 1, j), lcs(i, j - 1))

    return "%d\n%d\n" % (ed(len(a), len(b)), lcs(len(a), len(b)))


add(
    title="编辑距离的二维 DP",
    section=SECTION,
    difficulty=4, score=14, tags=["编程精练", "动态规划", "编辑距离", "LCS"],
    statement_md=(
        "读入两行字符串 `a`、`b`（可能含空格、可能为空行），输出两行：\n"
        "1. 把 `a` 变成 `b` 的**最少编辑次数**（插入 / 删除 / 替换一个字符，各算 1 次）\n"
        "2. 两串的**最长公共子序列**（LCS）长度\n\n"
        "★ 两个 DP 是同一个骨架：`dp[i][j]` 表示「`a` 的前 i 个」与「`b` 的前 j 个」的关系。\n"
        "- 编辑距离：字符相同则 `dp[i][j] = dp[i-1][j-1]`；不同则 "
        "`1 + min(删 dp[i-1][j], 增 dp[i][j-1], 换 dp[i-1][j-1])`\n"
        "- LCS：相同则 `dp[i-1][j-1] + 1`；不同则 `max(dp[i-1][j], dp[i][j-1])`\n\n"
        "★ 边界是 **`dp[0][j] = j`、`dp[i][0] = i`**——空的 `a` 要变成 `b`，"
        "只能一个个插进去，正好 j 次。忘了初始化边界是最常见的错。\n\n"
        "★ 还有一个漂亮的恒等式：`编辑距离 ≥ max(len(a), len(b)) - LCS`，"
        "只允许插入/删除时取等号；允许替换时，编辑距离就是 "
        "`len(a) + len(b) - 2×LCS - (替换省下来的)`，可以拿来粗查答案是否离谱。"
    ),
    input_format="两行：字符串 `a`、字符串 `b`（每行长度 ≤ 500，可含空格）。",
    output_format="两行：编辑距离；LCS 长度。",
    constraints_md="- 0 ≤ len(a), len(b) ≤ 500",
    inputs=[
        "kitten\nsitting\n",
        "\n\n",
        "abc\nabc\n",
        "abc\n\n",
        "intention\nexecution\n",
        "flaw\nlawn\n",
        "abcde\nace\n",
    ],
    samples=3,
    oracle=_oracle_10,
    solution=r'''import sys

lines = sys.stdin.read().split("\n")
a = lines[0] if lines else ""
b = lines[1] if len(lines) > 1 else ""
n, m = len(a), len(b)

# 编辑距离：滚动数组，只留上一行
prev = list(range(m + 1))
for i in range(1, n + 1):
    cur = [i] + [0] * m
    ai = a[i - 1]
    for j in range(1, m + 1):
        if ai == b[j - 1]:
            cur[j] = prev[j - 1]
        else:
            cur[j] = 1 + min(prev[j], cur[j - 1], prev[j - 1])
    prev = cur
ed = prev[m]

# LCS：同样滚动
prev = [0] * (m + 1)
for i in range(1, n + 1):
    cur = [0] * (m + 1)
    ai = a[i - 1]
    for j in range(1, m + 1):
        if ai == b[j - 1]:
            cur[j] = prev[j - 1] + 1
        else:
            cur[j] = prev[j] if prev[j] > cur[j - 1] else cur[j - 1]
    prev = cur
lcs = prev[m]

sys.stdout.write("%d\n%d\n" % (ed, lcs))
''',
    alt=r'''import sys

lines = sys.stdin.read().split("\n")
a = lines[0] if lines else ""
b = lines[1] if len(lines) > 1 else ""
n, m = len(a), len(b)

# 完整二维表（不滚动），边界在一起初始化
INF = 10 ** 9
dp = [[INF] * (m + 1) for _ in range(n + 1)]
for i in range(n + 1):
    dp[i][0] = i
for j in range(m + 1):
    dp[0][j] = j
for i in range(1, n + 1):
    for j in range(1, m + 1):
        if a[i - 1] == b[j - 1]:
            dp[i][j] = dp[i - 1][j - 1]
        else:
            dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

# LCS 用同一张表再开一张（这里直接复用另一张完整表）
L = [[0] * (m + 1) for _ in range(n + 1)]
for i in range(1, n + 1):
    for j in range(1, m + 1):
        if a[i - 1] == b[j - 1]:
            L[i][j] = L[i - 1][j - 1] + 1
        else:
            L[i][j] = max(L[i - 1][j], L[i][j - 1])

sys.stdout.write("%d\n%d\n" % (dp[n][m], L[n][m]))
''',
)


# --------------------------------------------------------------------- #
#  汇总
# --------------------------------------------------------------------- #

HEADER = '''# -*- coding: utf-8 -*-
"""Python 编程精练题库 —— 自动生成，**不要手改本文件**。

生成器：tools/gen_py_prog.py
分节：编程精练 · Python（10 题）

重生成：python tools/gen_py_prog.py
"""

PY_PROG_PROBLEMS: list[dict] = '''

TAIL = "\n"


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
    return HEADER + body + TAIL


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
    ap = argparse.ArgumentParser(description="生成 Python 编程精练题库")
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

    if args.check:
        return 0

    OUT_PATH.write_text(_dump(probs), encoding="utf-8", newline="\n")
    print("已写入 %s（%d 字节）" % (OUT_PATH, OUT_PATH.stat().st_size))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
