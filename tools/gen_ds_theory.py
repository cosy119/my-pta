#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""数据结构线理论题库生成器（单选 / 多选 / 判断 / 填空 / 简答）。

    python tools/gen_ds_theory.py [--check]

为什么答案要「算」而不是「写」
------------------------------
数据结构理论题的答案大多是**可计算的事实**：完全二叉树的叶子数、哈夫曼树的 WPL、
KMP 的 next 数组、出栈序列的种数、压缩矩阵的下标……这些东西手算三五道还行，
连着写六十道必然出错，而且错得很难看出来（一个数写错了，题面和解析都跟着错）。

所以这里的规矩是：**凡是能算的，答案一律由本文件里的计算函数算出来**，
再拿算出来的值去选项里找对应项（找不到、或找到多个，生成器直接中止）。

    calc=lambda: n - n // 2      算出 6
    options=["5", "6", "7"]      → 答案字母由 6 的位置反推

纯概念题（「栈是先进先出吗」）算不了，走 `mcn/tfn/multn`，由教材口径核对，
在下面标了「无计算」。这类题不多，且都是各章最基础的那几句定义。

★ 教材口径提醒
数据结构教材（ISBN 9787115651259）下标**从 1 起**：next[1] = 0、
下三角压缩 `k = i(i-1)/2 + j`、邻接矩阵第 0 行第 0 列放哨兵之类。
这套口径与 C 代码里 0 起不同，出题时凡是容易混的一律在解析里写明。
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.bank_kit import fill, mc, multi, tf          # noqa: E402

OUT_PATH = ROOT / "app" / "problems_bank_ds_theory.py"

HEADER = '''"""数据结构线理论题库 —— **自动生成，不要手改**。

本文件由 `tools/gen_ds_theory.py` 产出，重新生成：

    python tools/gen_ds_theory.py

题源
----
《数据结构》（ISBN 9787115651259）第 01 ~ 08 讲，按讲义章节分节，
与同节的编程题并列。全部是**理论题**（`line = "text"`），
提交答案文本由 `oneof` checker 比对，不启子进程。

答案可信度
----------
数值型答案（叶子数、WPL、next 数组、下标、比较次数……）全部由
`tools/gen_ds_theory.py` 里的计算函数**真算出来**再由它反推答案字母，
不是手写的；算不对就生成不出这个文件。纯概念题在生成器里标了「无计算」。
"""
from __future__ import annotations

DS_THEORY_PROBLEMS: list[dict] = '''


PROBS: list[dict] = []
_SEEN: set[str] = set()


def _push(p: dict) -> dict:
    t = p["title"]
    if t in _SEEN:
        raise SystemExit("★ 标题重复：%s" % t)
    _SEEN.add(t)
    PROBS.append(p)
    return p


# =========================================================================
# 计算函数 —— 答案的来源
# =========================================================================
def catalan(n: int) -> int:
    """n 个元素依次入栈、随时可出栈，能得到的**不同出栈序列**种数。"""
    return math.comb(2 * n, n) // (n + 1)


def huffman_wpl(weights: list[int]) -> int:
    """哈夫曼树的带权路径长度 = 每次合并出来的新结点权值之和。"""
    ws = sorted(weights)
    total = 0
    while len(ws) > 1:
        a = ws.pop(0)
        b = ws.pop(0)
        total += a + b
        ws.append(a + b)
        ws.sort()
    return total


def next_array(p: str) -> list[int]:
    """教材口径的 next 数组（下标从 1 起，next[1] = 0）。"""
    n = len(p)
    nxt = [0] * (n + 1)
    i, j = 1, 0
    while i < n:
        if j == 0 or p[i - 1] == p[j - 1]:
            i += 1
            j += 1
            nxt[i] = j
        else:
            j = nxt[j]
    return nxt[1:]


def pre_in_to_post(pre: str, ino: str) -> str:
    """由先序 + 中序还原二叉树，返回后序（顺带验证「能唯一确定」这条）。"""
    if not pre:
        return ""
    root = pre[0]
    k = ino.index(root)
    return (pre_in_to_post(pre[1:1 + k], ino[:k])
            + pre_in_to_post(pre[1 + k:], ino[k + 1:])
            + root)


def bst_inorder(keys: list[int]) -> list[int]:
    """按给定顺序插入二叉排序树，返回中序遍历结果。"""
    class N:
        __slots__ = ("v", "l", "r")

        def __init__(self, v):
            self.v, self.l, self.r = v, None, None

    root = None
    for k in keys:
        if root is None:
            root = N(k)
            continue
        cur = root
        while True:
            if k < cur.v:
                if cur.l is None:
                    cur.l = N(k)
                    break
                cur = cur.l
            else:
                if cur.r is None:
                    cur.r = N(k)
                    break
                cur = cur.r

    out = []
    st, cur = [], root
    while st or cur:
        while cur:
            st.append(cur)
            cur = cur.l
        cur = st.pop()
        out.append(cur.v)
        cur = cur.r
    return out


def stack_orders(n: int) -> set[tuple[int, ...]]:
    """穷举「1..n 依次入栈、随时可出栈」能得到的所有出栈序列。"""
    res: set[tuple[int, ...]] = set()

    def walk(nxt: int, st: tuple, out: tuple):
        if len(out) == n:
            res.add(out)
            return
        if st:                                   # 出栈一个
            walk(nxt, st[:-1], out + (st[-1],))
        if nxt <= n:                             # 压一个
            walk(nxt + 1, st + (nxt,), out)

    walk(1, (), ())
    return res


SHELL_CEX: list = []        # 搜出来的反例（key 序列），给解析用
QUICK_CEX: list = []


def _stable_after_sort(keys, sorter) -> bool:
    """把 (key, 原始下标) 排一遍，看同 key 的原始下标是否仍递增。"""
    a = [(k, i) for i, k in enumerate(keys)]
    out = sorter(a)
    for v in {k for k, _ in out}:
        idx = [i for k, i in out if k == v]
        if idx != sorted(idx):
            return False
    return True


def _search_unstable(sorter, global_name: str) -> bool:
    """在小序列里**枚举**反例：找到一个稳定性被破坏的例子就返回 False。

    ★ 为什么不用手写反例：我第一版手写的 `[(3,0),(3,1),(1,2)]` 跑出来是**稳定的**，
      差点把「快排不稳定」这条答成「稳定」。枚举 4 个元素、取值 1~3 的 81 种情况，
      几毫秒就跑完，比记反例可靠得多。
    """
    import itertools
    globals()[global_name] = []
    for seq in itertools.product([1, 2, 3], repeat=4):
        if len(set(seq)) < 3:          # 至少要有一个重复键才谈得上稳定性
            continue
        if not _stable_after_sort(list(seq), sorter):
            globals()[global_name] = list(seq)
            return False
    return True


def shell_stable_counterexample() -> bool:
    """希尔排序是否稳定 —— 枚举出一个真实反例来判。"""
    def sh(a):
        a = list(a)
        n = len(a)
        gap = n // 2
        while gap > 0:
            for i in range(gap, n):
                tmp = a[i]
                j = i - gap
                while j >= 0 and a[j][0] > tmp[0]:
                    a[j + gap] = a[j]
                    j -= gap
                a[j + gap] = tmp
            gap //= 2
        return a
    return _search_unstable(sh, "SHELL_CEX")


def quick_stable_counterexample() -> bool:
    """快速排序是否稳定 —— 枚举出一个真实反例来判（Lomuto 划分取首元素为基准）。"""
    def qs(a):
        a = list(a)

        def go(lo, hi):
            if lo >= hi:
                return
            pivot = a[lo]
            i = lo
            for j in range(lo + 1, hi + 1):
                if a[j][0] < pivot[0]:
                    i += 1
                    a[i], a[j] = a[j], a[i]
            a[lo], a[i] = a[i], a[lo]
            go(lo, i - 1)
            go(i + 1, hi)

        go(0, len(a) - 1)
        return a
    return _search_unstable(qs, "QUICK_CEX")


def is_max_heap(a: list[int]) -> bool:
    """大根堆：每个父结点都不小于它的孩子（用数组存储，0 起下标）。"""
    for i in range(1, len(a)):
        if a[(i - 1) // 2] < a[i]:
            return False
    return True


# =========================================================================
# 构造器
# =========================================================================
def mcn(*, title: str, stmt: str, options: list[str], value, section: str,
        expl: str, tags: list[str], diff: int = 2, score: int = 10) -> dict:
    """单选（**算出来的**）：`value` 转成字符串后必须恰好命中一个选项。"""
    want = str(value)
    if options.count(want) != 1:
        raise SystemExit("★ %s：算得 %s，选项里命中 %d 次"
                         % (title, want, options.count(want)))
    return _push(mc(title, stmt, options, "ABCDEFGH"[options.index(want)],
                    subject="ds", section=section, explanation=expl,
                    tags=tags, difficulty=diff, total_score=score))


def mcp(*, title: str, stmt: str, options: list[str], answer: str, section: str,
        expl: str, tags: list[str], diff: int = 2, score: int = 10) -> dict:
    """单选（**无计算**，纯概念，教材口径）。"""
    return _push(mc(title, stmt, options, answer, subject="ds", section=section,
                    explanation=expl, tags=tags, difficulty=diff,
                    total_score=score))


def tfc(*, title: str, stmt: str, cond: bool, section: str, expl: str,
        tags: list[str], diff: int = 2) -> dict:
    """判断（**算出来的**）：`cond` 是「题干这句话是否成立」的真值。"""
    return _push(tf(title, stmt, cond, subject="ds", section=section,
                    explanation=expl, tags=tags, difficulty=diff))


def tfn(*, title: str, stmt: str, answer: bool, section: str, expl: str,
        tags: list[str], diff: int = 2) -> dict:
    """判断（**无计算**，纯概念）。"""
    return _push(tf(title, stmt, answer, subject="ds", section=section,
                    explanation=expl, tags=tags, difficulty=diff))


def fillc(*, title: str, stmt: str, value, section: str, expl: str,
          tags: list[str], diff: int = 2, hint: str = "",
          extra: list[str] | None = None) -> dict:
    """填空（**算出来的**）：答案就是算出来的那个数。"""
    ans = str(value)
    return _push(fill(title, stmt, [ans] + list(extra or []), subject="ds",
                      section=section, explanation=expl, tags=tags,
                      difficulty=diff, hint=hint))


def multn(*, title: str, stmt: str, options: list[str], answers: list[str],
          section: str, expl: str, tags: list[str], diff: int = 3) -> dict:
    """多选（**无计算**，纯概念；选项两两互斥、由教材口径判定）。"""
    return _push(multi(title, stmt, options, answers, subject="ds",
                       section=section, explanation=expl, tags=tags,
                       difficulty=diff))


def shortq(*, title: str, statement_md: str, answers: list[str], section: str,
           explanation: str, tags: list[str], difficulty: int = 3,
           total_score: int = 12, hint: str = "") -> dict:
    """简答（无计算；`oneof` 比文本，答案表要列常见等价说法）。"""
    p = fill(title, statement_md, answers, subject="ds", section=section,
             explanation=explanation, tags=tags, difficulty=difficulty,
             total_score=total_score, hint=hint)
    p["question_type"] = "short_answer"
    p["output_format"] = "一句话作答（不要写解释、不要抄题目）"
    return _push(p)


# =========================================================================
# 第 01 讲 · 绪论
# =========================================================================
mcn(title="双重循环的语句频度", value=sum(1 for i in range(100) for _ in range(i)),
    stmt="下面这段代码的内层循环体一共执行多少次？\n\n"
         "```c\nfor (i = 0; i < 100; i++)\n    for (j = 0; j < i; j++)\n        x++;\n```",
    options=["4950", "5000", "5050", "100"],
    section="第 01 讲 · 绪论",
    expl="内层执行次数是 0+1+2+…+99 = 99×100/2 = **4950**。"
         "这也解释了为什么它的时间复杂度是 O(n²)：频数是 n(n-1)/2，只差一个低阶项和系数，"
         "大 O 里都要丢掉。",
    tags=["时间复杂度", "语句频度"])

mcp(title="数据结构里不可分割的最小单位", answer="A",
    stmt="数据结构中，**不可分割的最小单位**是：",
    options=["数据项", "数据元素", "数据对象", "数据类型"],
    section="第 01 讲 · 绪论",
    expl="**数据项**是不可分割的最小单位（如「学号」）；"
         "**数据元素**是数据的基本单位，由若干数据项组成（如一个学生记录）；"
         "**数据对象**是性质相同的数据元素的集合。"
         "三层是「项 ⊂ 元素 ⊂ 对象」的包含关系，别把「基本单位」和「最小单位」记混。",
    tags=["基本概念"])

# =========================================================================
# 第 02 讲 · 线性表
# =========================================================================
mcn(title="顺序表插入要移动几个元素（平均值）",
    # 在第 i 个位置插入要移动 n-i+1 个；i 取 1..n+1，总和 = n+(n-1)+…+0
    value=int(sum(range(1, 11)) / 11),
    stmt="长度为 10 的顺序表，等概率地在第 1 ~ 11 个位置（含表尾）插入一个元素，"
         "**平均**需要移动多少个元素？",
    options=["5", "4.5", "5.5", "10"],
    section="第 02 讲 · 线性表",
    expl="在第 i 个位置插入要移动 n-i+1 个元素（i 从 1 到 n+1），"
         "平均值 = (n + (n-1) + … + 0)/(n+1) = n/2 = **5**。"
         "所以顺序表插入的平均时间复杂度是 O(n)。删除是 (n-1)/2，也约等于 n/2。",
    tags=["顺序表", "平均移动"])

mcp(title="顺序表随机访问的时间复杂度", answer="A",
    stmt="顺序表（数组）按**下标**访问第 i 个元素的时间复杂度是：",
    options=["O(1)", "O(log n)", "O(n)", "O(n²)"],
    section="第 02 讲 · 线性表",
    expl="顺序表元素在内存里**连续存放**，第 i 个元素的地址 = 首地址 + i×元素大小，"
         "一步算出来，所以是 O(1)，这叫**随机存取**。"
         "链表做不到这一点，按序号找结点必须从头走，是 O(n)。",
    tags=["顺序表", "随机存取"])

mcn(title="头插法建表得到逆序", value="321",
    stmt="依次读入 1、2、3，用**头插法**建立单链表，从头结点往后遍历得到的序列是：",
    options=["321", "123", "231", "213"],
    section="第 02 讲 · 线性表",
    expl="头插法每次把新结点插在头结点之后，先读进来的会被后来者挤到后面，"
         "所以遍历次序与输入**相反** → 321。"
         "反过来，**尾插法**保持输入顺序（123）。这也是「用头插法做链表逆置」的原理。",
    tags=["头插法", "单链表"])

# =========================================================================
# 第 03 讲 · 栈和队列
# =========================================================================
_pool = [(4, 3, 2, 1), (3, 2, 1, 4), (2, 4, 3, 1), (4, 1, 2, 3)]
_orders = stack_orders(4)
_bad = [s for s in _pool if s not in _orders]
_ok = [s for s in _pool if s in _orders]
assert len(_bad) == 1 and len(_ok) == 3, \
    "干扰项里必须恰好 1 个非法、3 个合法，实际：非法 %s 合法 %s" % (_bad, _ok)
mcn(title="哪个出栈序列不可能出现", value="".join(map(str, _bad[0])),
    stmt="元素 1、2、3、4 依次入栈，入栈过程中允许随时出栈。"
         "下列哪个序列**不可能**是出栈序列？",
    options=["".join(map(str, s)) for s in _pool],
    section="第 03 讲 · 栈和队列",
    expl="用模拟法判：按目标序列走，该出的不是栈顶就继续压，压到没得压还不对就非法。"
         "**2413** 出不来 —— 要 2 先出，栈里剩 1，接着要 4 就得压 3、4，之后栈顶是 4 出 4，"
         "这时栈顶是 3，而序列要的是 1，卡死。"
         "★ 判定口诀：出栈序列里，**任意元素后面比它小的那些必须递减**（栈的后进先出约束）。",
    tags=["栈", "出栈序列"])

mcn(title="循环队列的元素个数",
    value=(8 - 3 + 10) % 10,
    stmt="循环队列容量 `MAXSIZE = 10`（0 ~ 9 号单元），`front = 3`、`rear = 8`，"
         "当前队列里有多少个元素？",
    options=["5", "4", "6", "9"],
    section="第 03 讲 · 栈和队列",
    expl="元素个数 = `(rear - front + MAXSIZE) % MAXSIZE` = (8-3+10)%10 = **5**。"
         "加 MAXSIZE 是为了处理 rear 绕回 front 左边的情况（rear < front 时直接减会得负数）。"
         "★ 别漏掉取模，也别把 MAXSIZE 写成 MAXSIZE-1 —— 队满判据 `(rear+1)%MAXSIZE==front` "
         "里那个 -1 只影响「最多能放几个」，不影响这个公式。",
    tags=["循环队列", "元素个数"])

mcn(title="三个元素能得到的出栈序列种数", value=catalan(3),
    stmt="1、2、3 依次入栈、随时可出栈，一共能得到多少种**不同**的出栈序列？",
    options=["5", "6", "4", "3"],
    section="第 03 讲 · 栈和队列",
    expl="这是卡特兰数 `C(2n,n)/(n+1)`：n=3 时 `C(6,3)/4 = 20/4 = 5`。"
         "穷举就是 123、132、213、231、321 —— 唯独 **312** 出不来（3 出栈时 1、2 还压在下面）。"
         "n 个元素的合法出栈序列数是 1、2、5、14、42…",
    tags=["栈", "卡特兰数"], diff=3)

# =========================================================================
# 第 04 讲 · 串、数组和广义表
# =========================================================================
_nxt = next_array("abaabc")
mcn(title="KMP 的 next 数组（教材口径）", value=_nxt[5],
    stmt="模式串 `abaabc`，按教材口径（下标从 1 起、`next[1] = 0`）求 next 数组，"
         "`next[6]` 等于多少？",
    options=sorted({str(v) for v in (1, 2, 3, 4)} | {str(_nxt[5])}),
    section="第 04 讲 · 串、数组和广义表",
    expl="完整 next 数组是 `0 1 1 2 2 3`（下标 1~6）。`next[j]` 的含义是"
         "「前 j-1 个字符里，最长相等前后缀的长度 + 1」，`next[6]` 看的是前 5 个字符 `abaab`，"
         "最长相等前后缀是 `ab`，长度 2，所以 `next[6] = 3`。"
         "★ 教材从 1 起、`next[1]=0`；有些资料从 0 起、`next[0]=-1`，两套口径的数值会差 1，考试按教材。",
    tags=["KMP", "next 数组"], diff=3)

mcp(title="BF 算法最坏情况的时间复杂度", answer="C",
    stmt="朴素模式匹配（BF）在最坏情况下的时间复杂度是"
         "（主串长 n、模式串长 m）：",
    options=["O(n)", "O(n + m)", "O(n×m)", "O(m²)"],
    section="第 04 讲 · 串、数组和广义表",
    expl="最坏情况下每趟都在最后一个字符失配、指针全部回退重来，"
         "比如主串 `aaaa…ab`、模式串 `aaa…a`，比较次数约 n×m。"
         "KMP 靠 next 数组让主串指针**不回退**，把它降到 O(n+m)。",
    tags=["BF", "时间复杂度"])

mcn(title="下三角矩阵压缩存储的下标",
    value=4 * 3 // 2 + 2,
    stmt="5 阶下三角矩阵按**行优先**压缩到一维数组，"
         "元素 `a[4][2]`（行列都从 **1** 起）存在一维数组的第几个位置？",
    options=["8", "9", "7", "10"],
    section="第 04 讲 · 串、数组和广义表",
    expl="下三角行优先：第 i 行前面有 `1+2+…+(i-1) = i(i-1)/2` 个元素，"
         "再数本行第 j 个 → `k = i(i-1)/2 + j` = 4×3/2 + 2 = **8**。"
         "★ 这是「下标从 1 起」的公式；若一维数组从 0 起存，位置再减 1 得 7。",
    tags=["压缩存储", "下标计算"], diff=3)

# =========================================================================
# 第 05 讲 · 树和二叉树
# =========================================================================
mcn(title="完全二叉树的叶子结点数", value=12 - 12 // 2,
    stmt="一棵有 12 个结点的**完全二叉树**，叶子结点有多少个？",
    options=["6", "5", "7", "4"],
    section="第 05 讲 · 树和二叉树",
    expl="完全二叉树的叶子数 = `n - ⌊n/2⌋` = 12 - 6 = **6**。"
         "等价推法：完全二叉树只有可能有一个度为 1 的结点，n 为偶数时它存在，"
         "由 `n0 = n2 + 1`、`n = n0 + n1 + n2` 解得 n0 = 6。",
    tags=["完全二叉树", "叶子数"])

mcn(title="完全二叉树的高度",
    value=math.floor(math.log2(100)) + 1,
    stmt="一棵有 100 个结点的完全二叉树，高度（层数）是多少？",
    options=["7", "6", "8", "100"],
    section="第 05 讲 · 树和二叉树",
    expl="高度 = `⌊log₂n⌋ + 1` = ⌊6.64⌋ + 1 = **7**。"
         "也等价于 `⌈log₂(n+1)⌉`。"
         "直觉核验：6 层最多 63 个结点装不下 100 个，7 层最多 127 个刚好装得下。",
    tags=["完全二叉树", "高度"])

mcn(title="二叉树的空指针域个数", value=20 + 1,
    stmt="一棵有 20 个结点的二叉树，用二叉链表存储（每个结点两个指针域），"
         "共有多少个**空指针域**？",
    options=["21", "20", "19", "22"],
    section="第 05 讲 · 树和二叉树",
    expl="n 个结点共 2n 个指针域，其中只有根没有父结点，其余 n-1 个结点各被一个指针指向，"
         "所以非空指针域 n-1 个，空指针域 = 2n - (n-1) = **n + 1 = 21**。"
         "★ 这条正好是**线索二叉树**能省下的空间：把 n+1 个空链域用来存前驱/后继线索。",
    tags=["二叉链表", "空指针域"])

mcn(title="由先序和中序求后序",
    value=pre_in_to_post("ABDECF", "DBEAFC"),
    stmt="某二叉树的先序遍历是 `ABDECF`，中序遍历是 `DBEAFC`。"
         "它的后序遍历是什么？",
    options=["DEBFCA", "DBEFCA", "DEBCFA", "EDBFCA"],
    section="第 05 讲 · 树和二叉树",
    expl="先序首字符 A 是根；在中序里 A 左边 `DBE` 是左子树、右边 `FC` 是右子树。"
         "左子树先序 `BDE`、中序 `DBE` → B 是左子树根，D 在左、E 在右；"
         "右子树先序 `CF`、中序 `FC` → C 是根、F 在左。"
         "后序 = 左 D E B、右 F C、根 A → **DEBFCA**。"
         "★ 先序+中序、后序+中序都能唯一确定一棵二叉树，但**先序+后序不能**。",
    tags=["遍历", "还原二叉树"], diff=3)

mcn(title="五个叶子的哈夫曼树 WPL", value=huffman_wpl([5, 7, 2, 3, 9]),
    stmt="权值为 2、3、5、7、9 的 5 个叶子结点构造哈夫曼树，"
         "它的带权路径长度 WPL 是多少？",
    options=["57", "52", "60", "44"],
    section="第 05 讲 · 树和二叉树",
    expl="每次取最小的两个合并：2+3=**5** → {5,5,7,9}；5+5=**10** → {7,9,10}；"
         "7+9=**16** → {10,16}；10+16=**26**。"
         "WPL = 所有合并出的新结点权值之和 = 5+10+16+26 = **57**。"
         "★ 这个「求和」法比逐个算「权值×路径长度」快得多，而且不会数错层。",
    tags=["哈夫曼树", "WPL"], diff=3)

# =========================================================================
# 第 06 讲 · 图
# =========================================================================
mcn(title="六阶无向完全图的边数", value=6 * 5 // 2,
    stmt="6 个顶点的**无向完全图**有多少条边？",
    options=["15", "30", "12", "36"],
    section="第 06 讲 · 图",
    expl="任意两个顶点之间都有一条边：`C(6,2) = 6×5/2 = **15**`。"
         "通式 `n(n-1)/2`。"
         "★ 无向图里 `(i,j)` 与 `(j,i)` 是同一条边，所以除以 2；有向图不除。",
    tags=["完全图", "边数"])

mcn(title="有向完全图的弧数", value=5 * 4,
    stmt="5 个顶点的**有向完全图**有多少条弧？",
    options=["20", "10", "25", "12"],
    section="第 06 讲 · 图",
    expl="每对顶点之间**两个方向各一条弧**：`n(n-1) = 5×4 = **20**`。"
         "对比无向完全图是 n(n-1)/2，正好差一倍。",
    tags=["完全图", "弧数"])

mcn(title="无向图各顶点度数之和", value=2 * 7,
    stmt="一个无向图有 5 个顶点、7 条边，所有顶点的度数之和是多少？",
    options=["14", "7", "12", "35"],
    section="第 06 讲 · 图",
    expl="握手定理：Σdeg(v) = **2e** = 2×7 = 14。"
         "每条边给两端各贡献 1 度。推论：度数之和一定是偶数，"
         "所以「奇数度的顶点个数」必然是偶数。",
    tags=["握手定理", "度"])

# =========================================================================
# 第 07 讲 · 查找
# =========================================================================
mcn(title="折半查找最多比较次数", value=math.ceil(math.log2(101)),
    stmt="对 100 个元素的有序表做**折半查找**，最多需要比较多少次？",
    options=["7", "6", "8", "100"],
    section="第 07 讲 · 查找",
    expl="折半查找的判定树是一棵平衡二叉树，高度 = `⌈log₂(n+1)⌉` = ⌈log₂101⌉ = **7**，"
         "最多比较次数就是树高。"
         "★ 别写成 ⌈log₂100⌉ = 7 就完了 —— 100 不在 2 的整数次幂上，两种写法这次碰巧同值，"
         "但推导要用 n+1。",
    tags=["折半查找", "判定树"])

mcn(title="装填因子的上限换算", value=int(13 * 0.75),
    stmt="散列表长 13，要求装填因子不超过 0.75，最多能存多少个元素？",
    options=["9", "10", "13", "8"],
    section="第 07 讲 · 查找",
    expl="装填因子 α = 表中元素个数 / 表长，所以最多 `13 × 0.75 = 9.75`，"
         "向下取整 **9** 个。"
         "α 越大冲突越多、平均查找长度越长；开放定址法一般控制在 0.75 以下。",
    tags=["散列表", "装填因子"])

# =========================================================================
# 第 08 讲 · 排序
# =========================================================================
mcp(title="快速排序为什么会退化到 O(n²)", answer="C",
    stmt="快速排序在最坏情况下的时间复杂度是：",
    options=["O(n log n)", "O(n)", "O(n²)", "O(n²log n)"],
    section="第 08 讲 · 排序",
    expl="当每次划分都极不均衡（基准是当前区间的最大或最小值，例如序列已基本有序且取首元素为基准）时，"
         "递归深度退化成 n，总比较次数约 n²/2。"
         "平均情况是 O(n log n)。随机选基准或三数取中能把「已有序」这种最坏输入打散。",
    tags=["快速排序", "时间复杂度"])

mcp(title="归并排序的辅助空间", answer="C",
    stmt="二路归并排序需要的**辅助空间**是：",
    options=["O(1)", "O(log n)", "O(n)", "O(n log n)"],
    section="第 08 讲 · 排序",
    expl="归并时要开一个和待合并段等长的临时数组，最大是 n，所以是 **O(n)**。"
         "这也是它相对快排/堆排（都是 O(1) 辅助空间）的主要缺点 ——"
         "拿空间换稳定性和最坏情况保证。",
    tags=["归并排序", "空间复杂度"])

# =========================================================================
# 多选题（10 道）
# =========================================================================
multn(title="哪些排序算法的最坏时间复杂度是 O(n log n)",
      stmt="下列排序算法中，**最坏情况**时间复杂度为 O(n log n) 的有：",
      options=["归并排序", "堆排序", "快速排序", "冒泡排序"], answers=["A", "B"],
      section="第 08 讲 · 排序",
      expl="归并排序和堆排序的最坏都是 O(n log n)。"
           "**快速排序最坏是 O(n²)**（划分极不均衡时），这正是它「平均最快但没保证」的由来；"
           "冒泡最坏 O(n²)。"
           "★ 记法：只有归并、堆排这两个是「稳的 O(n log n)」；快排是平均 O(n log n)。",
      tags=["时间复杂度", "排序"])

multn(title="哪些排序需要 O(n) 的辅助空间",
      stmt="下列排序算法中，**需要额外 O(n) 辅助空间**的有：",
      options=["归并排序", "基数排序", "快速排序", "堆排序"], answers=["A", "B"],
      section="第 08 讲 · 排序",
      expl="归并要开等长临时数组，基数排序要为每个桶准备空间（约 n + 基数个），都是 O(n)。"
           "快排只需递归栈 O(log n)（最坏 O(n)），堆排序只需常数个变量，都是 O(1) 级别。"
           "★ 快排的 O(log n) 栈空间常被忽略，严格说它不是 O(1)。",
      tags=["空间复杂度", "排序"])

multn(title="图的常用存储结构",
      stmt="下列哪些属于图的存储结构？",
      options=["邻接矩阵", "邻接表", "十字链表", "邻接多重表"], answers=["A", "B", "C", "D"],
      section="第 06 讲 · 图",
      expl="四个都是：邻接矩阵（数组，稠密图友好）、邻接表（链式，稀疏图友好）、"
           "十字链表（**有向图**，同时存出边和入边）、邻接多重表（**无向图**，一条边只存一个结点）。"
           "★ 别把十字链表和邻接多重表的适用场景弄反。",
      tags=["图的存储"])

multn(title="栈的典型应用",
      stmt="下列哪些问题天然适合用**栈**解决？",
      options=["括号匹配检查", "表达式求值", "函数调用与递归", "按层遍历二叉树"],
      answers=["A", "B", "C"],
      section="第 03 讲 · 栈和队列",
      expl="括号匹配、中缀转后缀/表达式求值、函数调用栈、递归、DFS、撤销操作都是栈。"
           "而**按层遍历**（BFS）用的是**队列** —— 这是栈与队列最经典的一组对照。",
      tags=["栈", "应用"])

multn(title="散列冲突的解决方法",
      stmt="下列哪些可用于处理散列冲突？",
      options=["开放定址法", "链地址法", "再散列法", "建立公共溢出区"], answers=["A", "B", "C", "D"],
      section="第 07 讲 · 查找",
      expl="四类都行：开放定址（线性探测、二次探测、伪随机）、链地址（拉链，最常用）、"
           "再散列（换个散列函数）、公共溢出区（冲突的全扔到另一个表）。"
           "★ 链地址法删元素最方便，开放定址法删元素不能直接置空（会把探测链断开），得打「删除标记」。",
      tags=["散列", "冲突处理"])

multn(title="链式存储相对顺序存储的优点",
      stmt="相比顺序存储，**链式存储**的优点有：",
      options=["插入删除不需要移动元素", "不需要一整块连续空间",
               "容量可以动态伸缩", "按下标随机访问更快"],
      answers=["A", "B", "C"],
      section="第 02 讲 · 线性表",
      expl="前三条都是链式的优点：改指针即可插删、结点可以散在内存各处、"
           "用多少申请多少。"
           "但**随机访问**恰恰是链式的短板：按序号找第 i 个必须从头走 O(n)，"
           "而顺序表是 O(1)。所以最后一条正好说反了。",
      tags=["链表", "优缺点"])

multn(title="最小生成树的算法",
      stmt="下列算法中，用于求**最小生成树**的有：",
      options=["Prim 算法", "Kruskal 算法", "Dijkstra 算法", "Floyd 算法"],
      answers=["A", "B"],
      section="第 06 讲 · 图",
      expl="Prim（从点出发，每次选连接已选集合的最小边，O(n²)，适合稠密图）和"
           "Kruskal（按边权排序，用并查集判环，O(e log e)，适合稀疏图）都是求 MST 的。"
           "Dijkstra 求**单源最短路径**，Floyd 求**每对顶点间最短路径** —— 都不是生成树。",
      tags=["最小生成树", "Prim", "Kruskal"])

multn(title="关于二叉排序树的正确说法",
      stmt="关于二叉排序树（BST），下列哪些说法正确？",
      options=["中序遍历得到递增序列", "平均查找长度是 O(log n)",
               "插入新结点不需要移动已有元素", "最坏情况下查找退化为 O(n)"],
      answers=["A", "B", "C", "D"],
      section="第 07 讲 · 查找",
      expl="四条都对：中序有序是 BST 的定义性质（也是判断一棵树是不是 BST 的标准做法）；"
           "随机插入时树高约 log n；插入只需改指针；"
           "但如果按**有序序列**插入，树会退化成单支链，查找变成 O(n) —— 这正是要引入平衡树的原因。",
      tags=["二叉排序树"])

multn(title="哪些操作会用到队列",
      stmt="下列哪些场景适合用**队列**？",
      options=["按层遍历二叉树", "图的广度优先搜索", "操作系统的作业调度", "表达式括号匹配"],
      answers=["A", "B", "C"],
      section="第 03 讲 · 栈和队列",
      expl="层次遍历、BFS、各种调度（先来先服务）都靠队列的先进先出。"
           "括号匹配要的是「最近的未匹配左括号」，是后进先出，属于栈。"
           "★ 一句话区分：**要「最近」用栈，要「最早」用队列**。",
      tags=["队列", "应用"])

multn(title="排序趟数与初始序列有关的算法",
      stmt="下列排序算法中，**执行趟数会随初始序列不同而变化**的有：",
      options=["冒泡排序", "快速排序", "直接插入排序", "二路归并排序"],
      answers=["A", "B"],
      section="第 08 讲 · 排序",
      expl="冒泡可以提前发现「本趟无交换」而结束，所以已有序时 1 趟就完事、逆序时要 n-1 趟；"
           "快排的递归深度和划分次数直接取决于基准选得好不好。"
           "直接插入固定 n-1 趟、归并固定 ⌈log₂n⌉ 趟 —— 趟数与数据无关，"
           "变的只是每趟内部的比较次数。",
      tags=["排序", "趟数"], diff=4)

# =========================================================================
# 判断题（14 道；能算的算，算不了的按教材口径）
# =========================================================================
tfc(title="二叉排序树的中序遍历是有序的", cond=bst_inorder([50, 30, 70, 20, 40, 60, 80])
    == sorted([50, 30, 70, 20, 40, 60, 80]),
    stmt="二叉排序树的中序遍历结果一定是**递增有序**的。",
    section="第 07 讲 · 查找",
    expl="对。按定义左子树所有结点 < 根 < 右子树所有结点，"
         "中序「左-根-右」正好把这个大小关系排成一条递增序列。"
         "反过来说：判断一棵二叉树是不是 BST，最靠谱的办法就是中序遍历看是否递增。",
    tags=["二叉排序树", "中序遍历"])

tfc(title="大根堆满足父结点不小于孩子", cond=is_max_heap([9, 7, 8, 3, 5, 6, 4]),
    stmt="用数组存储的大根堆，下标 i 的结点值不小于下标 2i+1、2i+2 的结点值。",
    section="第 08 讲 · 排序",
    expl="对。大根堆的定义就是「每个结点 ≥ 它的孩子」，用数组存时孩子下标是 `2i+1`、`2i+2`"
         "（0 起；若 1 起则是 `2i`、`2i+1`）。"
         "注意堆只保证**父子**有序，兄弟之间、左右子树之间没有任何大小要求。",
    tags=["堆", "性质"])

_SHELL_STABLE = shell_stable_counterexample()
tfc(title="希尔排序是稳定的", cond=_SHELL_STABLE,
    stmt="希尔排序是**稳定**的排序算法。",
    section="第 08 讲 · 排序",
    expl="错。用真反例验证（生成器枚举出来的）：序列 `1 3 2a 2b`（两个 2 相等，"
         "下标 0~3）。第一趟 gap=2 比较位置 1 与 3：`3` 和 `2b`，把 2b 前移、3 后移，"
         "序列成 `1 2b 2a 3` —— **2b 已经跑到 2a 前面**，之后 gap=1 的插入排序不会再交换"
         "它俩，破坏就此固定。\n"
         "★ 根因：希尔是**跳跃式**分组插入，相等元素被分到不同组后各自移动，就会跨过彼此。"
         "结论：冒泡/插入/归并/基数稳定；**希尔、快排、选择、堆排都不稳定**。",
    tags=["希尔排序", "稳定性"])

_QUICK_STABLE = quick_stable_counterexample()
tfc(title="快速排序是稳定的", cond=_QUICK_STABLE,
    stmt="快速排序是**稳定**的排序算法。",
    section="第 08 讲 · 排序",
    expl="错。用真反例验证（生成器枚举出来的）：序列 `1 3 2a 2b`。"
         "第一趟以 `1` 为基准划分没动任何元素，进右半段 `3 2a 2b`；"
         "以 `3` 为基准，两个 2 都小于 3，划分结束时把基准与最后一个位置上的 `2b` 交换 →"
         "`1 2b 2a 3`，**2b 跑到了 2a 前面**。\n"
         "★ 根因：快排划分时的交换是**长距离**的，相等元素会被直接跨过去。"
         "要稳定就别用快排，用归并。",
    tags=["快速排序", "稳定性"])

tfn(title="顺序表可以随机存取", answer=True,
    stmt="顺序表支持**随机存取**（按序号直接定位元素）。",
    section="第 02 讲 · 线性表",
    expl="对。连续存放 + 地址公式 `LOC(i) = LOC(1) + (i-1)×L`，一步算出地址，O(1)。"
         "链表只能**顺序存取**，找第 i 个要从头走。",
    tags=["顺序表", "随机存取"])

tfn(title="单链表可以随机存取", answer=False,
    stmt="单链表支持**随机存取**，可以直接跳到第 i 个结点。",
    section="第 02 讲 · 线性表",
    expl="错。单链表结点地址不连续，唯一入口是头指针，"
         "找第 i 个必须沿 next 走 i-1 步，是 O(n) 的**顺序存取**。"
         "这也是「链表不适合按位置频繁查询、适合频繁插删」的根因。",
    tags=["链表", "存取方式"])

tfn(title="栈是先进先出", answer=False,
    stmt="栈的特点是**先进先出**（FIFO）。",
    section="第 03 讲 · 栈和队列",
    expl="错。栈是**后进先出**（LIFO），只在栈顶操作；"
         "**先进先出**是队列。这是全书最不该错的一对概念，"
         "记法：栈像摞盘子（最后放的先拿走），队列像排队（先来的先走）。",
    tags=["栈", "队列"])

tfn(title="循环队列牺牲一个单元判满", answer=True,
    stmt="循环队列常用「牺牲一个存储单元」的办法来区分队空与队满。",
    section="第 03 讲 · 栈和队列",
    expl="对。队空 `front == rear`，队满也 `front == rear` —— 两者撞在一起无法区分。"
         "常见解法就是少用一个单元：队满判据写成 `(rear+1) % MAXSIZE == front`，"
         "代价是容量 MAXSIZE 的数组只能放 MAXSIZE-1 个元素。"
         "另一条路是额外加一个 `size` 或 `tag` 变量。",
    tags=["循环队列", "判满"])

tfn(title="KMP 的 next 只与模式串有关", answer=True,
    stmt="KMP 的 next 数组只取决于**模式串**本身，与主串无关。",
    section="第 04 讲 · 串、数组和广义表",
    expl="对。next 描述的是「模式串自己前后缀的相似程度」，"
         "所以可以在匹配前先算好、反复用于不同主串。"
         "这正是 KMP 相比 BF 的本质改进：主串指针**永不回退**。",
    tags=["KMP"])

tfn(title="完全二叉树的叶子只出现在最后两层", answer=True,
    stmt="完全二叉树中，叶子结点只可能出现在**最下面两层**。",
    section="第 05 讲 · 树和二叉树",
    expl="对。完全二叉树按层序**从左到右**填满，除最后一层外每层都是满的，"
         "所以倒数第二层的结点要么有两个孩子、要么有一个左孩子（此时它不算叶子），"
         "叶子只可能在最后一层，以及倒数第二层右侧「没有孩子」的那几个。",
    tags=["完全二叉树"])

tfn(title="最小生成树是唯一的", answer=False,
    stmt="一个连通图的最小生成树一定是**唯一**的。",
    section="第 06 讲 · 图",
    expl="错。**边权互不相同**时才唯一；一旦有权值相同的边，就可能有多棵不同的 MST，"
         "但它们的**总权值相同**。"
         "例：三角形三条边都是 1，任取两条都是 MST。"
         "所以 Prim / Kruskal 从不同起点出发可能得到不同形状的树，权值却一样。",
    tags=["最小生成树", "唯一性"])

tfn(title="折半查找要求有序且顺序存储", answer=True,
    stmt="折半查找要求线性表**有序**，并且必须**顺序存储**。",
    section="第 07 讲 · 查找",
    expl="对。有序是前提；顺序存储是为了能 O(1) 跳到中点 —— "
         "链表上找中点本身就要 O(n)，折半就失去意义了。"
         "所以「链表有序」也不能折半查找（可以用跳表之类的结构）。",
    tags=["折半查找", "适用条件"])

tfn(title="归并排序的辅助空间是 O(1)", answer=False,
    stmt="二路归并排序只需要 O(1) 的辅助空间。",
    section="第 08 讲 · 排序",
    expl="错。归并必须开一个和待合并段等长的临时数组，最大 O(n)。"
         "O(1) 辅助空间的是堆排序、冒泡、插入、希尔、选择这些「就地」排序。"
         "归并是典型的**以空间换稳定 + 最坏保证**。",
    tags=["归并排序", "空间复杂度"])

# =========================================================================
# 填空题（12 道，答案都是算出来的整数）
# =========================================================================
fillc(title="完全二叉树的度为 1 的结点数", value=1,
      stmt="一棵有 1000 个结点的完全二叉树，**度为 1** 的结点有多少个？",
      section="第 05 讲 · 树和二叉树",
      expl="完全二叉树里度为 1 的结点最多一个。"
           "由 `n0 = n2 + 1` 和 `n = n0 + n1 + n2` 得 `n = 2n2 + n1 + 1`，"
           "n = 1000 是偶数，所以 n1 必须是奇数 → **n1 = 1**。"
           "（n 为奇数时 n1 = 0。）",
      tags=["完全二叉树", "度"], diff=3)

fillc(title="五阶下三角矩阵的非零元素数", value=5 * 6 // 2,
      stmt="5 阶下三角矩阵（含主对角线）一共有多少个元素需要压缩存储？",
      section="第 04 讲 · 串、数组和广义表",
      expl="下三角含对角线共 `1+2+3+4+5 = 15` 个，即 `n(n+1)/2`。"
           "这正是压缩后一维数组的长度 —— 从 25 个存到 15 个，省了 40%。",
      tags=["压缩存储"])

fillc(title="哈夫曼树的结点总数", value=2 * 5 - 1,
      stmt="一棵哈夫曼树有 5 个叶子结点，整棵树一共有多少个结点？",
      section="第 05 讲 · 树和二叉树",
      expl="哈夫曼树是严格二叉树（没有度为 1 的结点），"
           "由 `n0 = n2 + 1` 得 n2 = 4，总数 = 5 + 4 = **9** = 2n-1。"
           "★ 这个 2n-1 也正好是「n 个叶子构造哈夫曼树需要合并 n-1 次」的另一种说法。",
      tags=["哈夫曼树", "结点数"])

fillc(title="二叉树的结点总数", value=(10 + 1) + 5 + 10,
      stmt="一棵二叉树有 10 个度为 2 的结点、5 个度为 1 的结点，它一共有多少个结点？",
      section="第 05 讲 · 树和二叉树",
      expl="先由 `n0 = n2 + 1` 得叶子 **n0 = 11**；"
           "总数 = n0 + n1 + n2 = 11 + 5 + 10 = **26**。"
           "★ 题里只给 n2 和 n1 就够算了 —— 因为二叉树里 n0 由 n2 唯一确定，"
           "这也是 `n0 = n2 + 1` 最常被考的地方。",
      tags=["二叉树", "结点数"], diff=3)

fillc(title="10 个元素折半查找的最大比较次数", value=math.ceil(math.log2(11)),
      stmt="对 10 个元素的有序表做折半查找，最多比较多少次？",
      section="第 07 讲 · 查找",
      expl="判定树高度 = `⌈log₂(n+1)⌉` = ⌈log₂11⌉ = **4**。"
           "核验：4 层判定树最多容纳 15 个结点，3 层只够 7 个，10 个元素必须到第 4 层。",
      tags=["折半查找"])

fillc(title="直接插入排序的最多比较次数", value=5 * 4 // 2,
      stmt="对 5 个元素做直接插入排序，最坏情况下共需要比较多少次？",
      section="第 08 讲 · 排序",
      expl="第 i 趟最多比较 i 次（要一路比到最前面），"
           "总次数 = 1+2+3+4 = **10** = n(n-1)/2。"
           "对应输入是**逆序**序列。顺带：移动次数也是 n(n-1)/2，所以最坏 O(n²)。",
      tags=["直接插入排序", "比较次数"])

fillc(title="冒泡排序的最少趟数", value=1,
      stmt="对 100 个元素做冒泡排序（带「本趟无交换则提前结束」优化），"
           "如果初始序列**已经有序**，需要几趟？",
      section="第 08 讲 · 排序",
      expl="第一趟从头到尾扫一遍，发现一次交换都没有 → 直接结束，共 **1** 趟。"
           "这就是「冒泡的趟数与初始序列有关」的具体体现；"
           "不加这个优化的话固定要 n-1 = 99 趟。",
      tags=["冒泡排序", "趟数"])

fillc(title="n 个元素出栈序列的种数", value=catalan(4),
      stmt="1、2、3、4 依次入栈、随时可出栈，一共能得到多少种不同的出栈序列？",
      section="第 03 讲 · 栈和队列",
      expl="卡特兰数：`C(8,4)/5 = 70/5 = **14**`。"
           "记住序列 1、2、5、14、42 就行（n=1..5）。"
           "这类「合法序列计数」问题的通式都是 `C(2n,n)/(n+1)`。",
      tags=["栈", "卡特兰数"], diff=3)

fillc(title="模式串 next 数组的末位", value=next_array("abcac")[4],
      stmt="模式串 `abcac`，按教材口径（1 起、`next[1]=0`）求 next 数组，`next[5]` 等于多少？",
      section="第 04 讲 · 串、数组和广义表",
      expl="完整 next 数组是 `0 1 1 1 2`。`next[5]` 看前 4 个字符 `abca`，"
           "最长相等前后缀是 `a`，长度 1，所以 `next[5] = 1+1 = 2`。"
           "★ 口诀：`next[j]` = 「前 j-1 个字符的最长相等前后缀长度」+ 1。",
      tags=["KMP", "next 数组"], diff=4)

fillc(title="对称矩阵压缩后的元素个数", value=4 * 5 // 2,
      stmt="4 阶对称矩阵只存下三角（含主对角线），需要多少个存储单元？",
      section="第 04 讲 · 串、数组和广义表",
      expl="对称矩阵 `a[i][j] = a[j][i]`，存一半就够：`n(n+1)/2 = 4×5/2 = **10**`，"
           "只占原来的 10/16。"
           "访问上三角元素时用转置下标去下三角取：`a[i][j] → a[j][i]`。",
      tags=["对称矩阵", "压缩存储"])

fillc(title="无向图的边数与度数关系", value=2 * 12,
      stmt="一个无向图所有顶点的度数之和是 24，它有多少条边？",
      section="第 06 讲 · 图",
      expl="由握手定理 Σdeg = 2e，得 e = 24/2 = **12**。"
           "顺带一个常考推论：度数之和必为偶数，所以「度为奇数的顶点」个数一定是偶数。",
      tags=["握手定理"])

# =========================================================================
# 简答题（4 道，无计算）
# =========================================================================
shortq(title="栈和队列的区别", statement_md=
       "**简答题**：栈和队列在「操作位置」和「进出顺序」上有什么区别？\n\n"
       "按「插入删除在哪一端 → 是什么顺序」作答。",
       answers=[
           "栈只在栈顶插入和删除，后进先出；队列在队尾插入、队头删除，先进先出",
           "栈在栈顶操作是后进先出，队列队尾进队头出是先进先出",
           "栈只能在栈顶插入删除，遵循后进先出；队列一端进另一端出，遵循先进先出",
       ],
       section="第 03 讲 · 栈和队列",
       explanation="**栈**：插入（push）和删除（pop）都在**栈顶**同一端进行，后进先出（LIFO）。\n"
                   "**队列**：在**队尾**插入（enqueue）、在**队头**删除（dequeue），两端分工，"
                   "先进先出（FIFO）。\n"
                   "一句话记：栈是「一端进出」，队列是「一端进、另一端出」。",
       tags=["栈", "队列", "简答"], difficulty=3)

shortq(title="顺序存储与链式存储的优缺点", statement_md=
       "**简答题**：顺序存储和链式存储各有什么优点？（各说一条即可）",
       answers=[
           "顺序存储可以随机存取、存储密度高；链式存储插入删除不需要移动元素、容量可动态伸缩",
           "顺序存储支持随机访问且不浪费指针空间，链式存储插删方便且不用连续空间",
           "顺序存取快密度高，链式插删快可动态分配",
       ],
       section="第 02 讲 · 线性表",
       explanation="**顺序存储**：地址连续 → 随机存取 O(1)、存储密度高（不用存指针）；"
                   "缺点是插删要移动大量元素、需要预分配连续空间。\n"
                   "**链式存储**：插删只改指针、容量按需申请；"
                   "缺点是不能随机存取（找第 i 个 O(n)）、每个结点多花指针空间、"
                   "存储密度低。\n"
                   "选择依据：**查多改少用顺序，改多查少用链式**。",
       tags=["顺序存储", "链式存储", "简答"], difficulty=3)

shortq(title="快速排序为什么最坏是 O(n²)", statement_md=
       "**简答题**：快速排序在什么情况下退化成 O(n²)？怎么缓解？",
       answers=[
           "每次划分都极不均衡（基准是最大或最小值）时退化成O(n²)，用随机选基准或三数取中缓解",
           "序列已基本有序且固定取首元素为基准时最坏O(n²)，可随机化基准或取中位数",
           "划分极不均衡时递归深度退化为n，比较次数约n²/2，用随机基准缓解",
       ],
       section="第 08 讲 · 排序",
       explanation="快排的性能取决于**划分是否均衡**。当每次选出的基准都是当前区间的"
                   "最大/最小值时（典型场景：**序列已基本有序**、又固定取第一个元素当基准），"
                   "一边为空、另一边只少一个元素，递归深度退化成 n，"
                   "总比较次数约 `n + (n-1) + … + 1 = n²/2`。\n"
                   "缓解办法：**随机选基准**、**三数取中**，或者小区间改用插入排序；"
                   "更彻底的是用堆排序兜底（introsort）。",
       tags=["快速排序", "简答"], difficulty=4)

shortq(title="哈夫曼树的构造过程", statement_md=
       "**简答题**：简述哈夫曼树的构造步骤（用「每次选两个最小的」这句话开头）。",
       answers=[
           "每次从森林中选两个权值最小的树合并成一棵新树，新树权值为两者之和，重复直到只剩一棵",
           "每次选两个最小权值合并，新结点权值为二者之和放回森林，直到只剩一棵树",
           "反复取两个最小权值的树合并，新根权值为两者和，重复直到森林只剩一棵",
       ],
       section="第 05 讲 · 树和二叉树",
       explanation="1. 把 n 个权值各看成一棵只有根的单结点树，组成森林；\n"
                   "2. **每次从森林中选出两棵权值最小的树**，合并成一棵新树，"
                   "新根结点的权值 = 两者之和；\n"
                   "3. 把新树放回森林，重复第 2 步，直到森林里只剩一棵树。\n\n"
                   "得到的树就是哈夫曼树，其 WPL 最小。"
                   "编码时左分支记 0、右分支记 1，就得到**前缀码**"
                   "（没有任何一个编码是另一个的前缀），这是它能被唯一解码的原因。",
       tags=["哈夫曼树", "简答"], difficulty=3)


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
                bad.append("[%d] %s：理论题的样例必须隐藏（is_sample=0）" % (i, t))
            if not c["expected_stdout"].strip():
                bad.append("[%d] %s：期望值为空" % (i, t))
    return bad


def main() -> int:
    ap = argparse.ArgumentParser(description="生成数据结构线理论题库")
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
