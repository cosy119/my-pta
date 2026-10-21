# -*- coding: utf-8 -*-
"""C++ 基础编程题 · 第 5 册：指针与引用（20）+ 字符数组与字符串（20）= 40 题。

对应教材第 06 讲后半（p220~251）。这一册专练「地址」：
`a[i]` 就是 `*(a+i)`、数组名退化成首地址、`new` 与 `delete` 必须配对、
`char` 数组末尾那个 `\\0` 到底占不占长度、`getline` 和 `cin >>` 差在哪。

★ oracle 一律是独立的 Python 实现（直接模拟 / 内建方法），绝不复用 C++ 解的结果。
★ 每题 alt 换一条实现路径（指针算术↔下标、手写↔库函数、循环↔递归）。

重生成：python tools/gen_cpp_basic5.py
"""
from __future__ import annotations

import random
import string
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cpp_basic_kit import cases, cli, stmt          # noqa: E402

SEC_PTR = "C++ 编程 · 指针与引用"
SEC_STR = "C++ 编程 · 字符数组与字符串"

PROBLEMS: list[dict] = []


def A(title, sec, d, st, inf, outf, con, inp, orc, sol, alt, tags):
    PROBLEMS.append(dict(title=title, section=sec, difficulty=d, statement_md=st,
                         input_format=inf, output_format=outf, constraints_md=con,
                         inputs=inp, oracle=orc, solution=sol, alt=alt, tags=tags))


# ------------------------------------------------------------------ #
#  数据助手
# ------------------------------------------------------------------ #
def rints(seed: int, n: int, lo: int = -50, hi: int = 50) -> list[int]:
    rng = random.Random(seed)
    return [rng.randint(lo, hi) for _ in range(n)]


def barr(seed: int, n: int, lo: int = -50, hi: int = 50) -> str:
    v = rints(seed, n, lo, hi)
    return "%d\n%s\n" % (n, " ".join(str(x) for x in v))


def toks(t: str) -> list[int]:
    return [int(x) for x in t.split()]


def line_of(t: str) -> str:
    return t.rstrip("\n")


def _swap_at(t: str) -> str:
    tok = toks(t)
    n, i, j = tok[0], tok[1], tok[2]
    a = tok[3:3 + n]
    a[i], a[j] = a[j], a[i]
    return " ".join(str(x) for x in a) + "\n"


def _select_sort(t: str) -> str:
    """真模拟一遍选择排序，同时数交换次数。"""
    a = toks(t)[1:]
    n = len(a)
    sw = 0
    for i in range(n - 1):
        k = i
        for j in range(i + 1, n):
            if a[j] < a[k]:
                k = j
        if k != i:
            a[i], a[k] = a[k], a[i]
            sw += 1
    return " ".join(str(x) for x in a) + "\n" + "%d\n" % sw


# ===================================================================== #
#  SEC_PTR · 指针与引用（20 题）
# ===================================================================== #

A("【指针】用指针参数交换数组元素", SEC_PTR, 1,
  stmt("写函数 `void swapAt(int *p, int *q)` 交换两个指针指向的元素。"
       "读入 `n i j`，第二行 `n` 个整数，交换下标 `i` 与 `j` 的元素后输出整个数组。",
       ["下标从 0 开始；`swapAt(a + i, a + j)` 传的是地址不是值",
        "`void swapAt(int x, int y)` 交换的是副本，原数组不变",
        "输出一行，空格分隔"]),
  "第一行 `n i j`；第二行 `n` 个整数。",
  "一行：交换后的数组。",
  "- 1 ≤ n ≤ 1000\n- 0 ≤ i, j < n\n- |x| ≤ 10⁶",
  lambda: cases("5 0 4\n1 2 3 4 5", "3 1 1\n7 8 9", "2 0 1\n-1 -2",
                "%d %d %d\n%s" % (10, 2, 7, " ".join(str(x) for x in rints(11, 10))),
                "%d %d %d\n%s" % (6, 5, 0, " ".join(str(x) for x in rints(12, 6, -100, 100))),
                "1 0 0\n42"),
  _swap_at,
  r'''#include <cstdio>
void swapAt(int *p, int *q) {      // 形参是指针，*p 就是原元素
    int t = *p; *p = *q; *q = t;
}
int main() {
    int n, i, j;
    if (scanf("%d %d %d", &n, &i, &j) != 3) return 0;
    int a[1005];
    for (int k = 0; k < n; k++) scanf("%d", &a[k]);
    swapAt(a + i, a + j);          // 传地址
    for (int k = 0; k < n; k++) printf("%d%c", a[k], k + 1 == n ? '\n' : ' ');
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n, i, j;
    if (scanf("%d %d %d", &n, &i, &j) != 3) return 0;
    int *a = new int[n];           // 动态数组
    for (int k = 0; k < n; k++) scanf("%d", &a[k]);
    std::swap(*(a + i), *(a + j)); // 指针解引用直接交换
    for (int k = 0; k < n; k++) printf("%d%c", a[k], k + 1 == n ? '\n' : ' ');
    delete[] a;
    return 0;
}
''',
  ["指针", "交换", "数组"])

A("【指针】指针遍历数组求最值及下标", SEC_PTR, 1,
  stmt("用指针遍历数组，求最大值和它**第一次出现**的下标（从 1 开始）。"
       "读入 `n` 和 `n` 个整数，输出 `max pos`。",
       ["指针遍历的写法是 `for (int *p = a; p < a + n; ++p)`",
        "`a + n` 是「最后一个元素再往后一格」的地址，可以比较但不能解引用",
        "`pos` 从 1 开始，别写成指针差值"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：`max pos`。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases(barr(21, 5), barr(22, 1), "3\n5 5 1", barr(23, 20),
                barr(24, 50, -1000, -1), barr(25, 8, 0, 0)),
  lambda t: "%d %d\n" % (lambda v: (max(v), v.index(max(v)) + 1))(toks(t)[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int mx = a[0], pos = 1, idx = 1;
    for (int *p = a + 1; p < a + n; ++p) {   // 指针遍历
        idx++;
        if (*p > mx) { mx = *p; pos = idx; }
    }
    printf("%d %d\n", mx, pos);
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int *mx = std::max_element(a, a + n);     // 取第一个最大
    printf("%d %d\n", *mx, (int)(mx - a) + 1);
    return 0;
}
''',
  ["指针", "遍历", "最值"])

A("【指针】用指针求数组元素之和", SEC_PTR, 1,
  stmt("用指针遍历求所有元素之和。读入 `n` 和 `n` 个整数（|x| ≤ 10⁶），输出总和。",
       ["`*(p + i)` 和 `a[i]` 完全等价",
        "10⁵ 个 10⁶ 累加到 10¹¹，必须用 `long long`",
        "输出一个整数"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：总和。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases(barr(31, 5), barr(32, 1), barr(33, 20),
                barr(34, 200, -1000000, 1000000), "3\n-1 -2 -3", barr(35, 333)),
  lambda t: "%d\n" % sum(toks(t)[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    long long s = 0;
    for (int *p = a; p < a + n; ++p) s += *p;
    printf("%lld\n", s);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    long long s = 0;
    for (int i = 0; i < n; i++) s += *(a + i);   // 指针偏移写法
    printf("%lld\n", s);
    return 0;
}
''',
  ["指针", "求和"])

A("【指针】指针偏移访问元素", SEC_PTR, 1,
  stmt("读入 `n k` 和 `n` 个整数，输出两个数：`*(a + k)` 与 `a[k]`（它们必然相同），"
       "再输出 `*(a + k) * 2`。",
       ["`a[k]` 在编译后就是 `*(a + k)`，两者是同一个东西的两种写法",
        "0 ≤ k < n，越界读是未定义行为",
        "输出一行三个整数"]),
  "第一行 `n k`；第二行 `n` 个整数。",
  "一行：`*(a+k)`、`a[k]`、`*(a+k)*2`。",
  "- 1 ≤ n ≤ 1000\n- 0 ≤ k < n\n- |x| ≤ 10⁴",
  lambda: cases("5 0\n1 2 3 4 5", "5 4\n1 2 3 4 5", "1 0\n-7",
                "%d %d\n%s" % (10, 3, " ".join(str(x) for x in rints(41, 10))),
                "%d %d\n%s" % (6, 5, " ".join(str(x) for x in rints(42, 6, -100, 100))),
                "3 2\n0 0 9"),
  lambda t: (lambda tok: (lambda v, k: "%d %d %d\n" % (v[k], v[k], v[k] * 2))(
      tok[2:2 + tok[0]], tok[1]))(toks(t)),
  r'''#include <cstdio>
int main() {
    int n, k;
    if (scanf("%d %d", &n, &k) != 2) return 0;
    int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    printf("%d %d %d\n", *(a + k), a[k], *(a + k) * 2);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n, k;
    if (scanf("%d %d", &n, &k) != 2) return 0;
    int *a = new int[n];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int *p = a + k;               // 先算好指针，再重复解引用
    printf("%d %d %d\n", *p, a[k], *p * 2);
    delete[] a;
    return 0;
}
''',
  ["指针", "偏移", "数组名"])

A("【指针】二级指针让指针指向最大元素", SEC_PTR, 3,
  stmt("用二级指针 `int **pp` 修改一级指针的指向：让它指向数组中的最大元素，再输出 `**pp`。"
       "读入 `n` 和 `n` 个整数，输出最大值。",
       ["`int **pp = &p;` 之后 `*pp` 就是 `p`，给 `*pp` 赋值等于改 `p` 的指向",
        "实参必须是「指针的地址」，直接传 `p` 只能改副本",
        "输出一个整数"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：最大值。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases(barr(51, 5), barr(52, 1), "3\n5 5 1", barr(53, 20),
                barr(54, 30, -1000, -1), barr(55, 9, 7, 7)),
  lambda t: "%d\n" % max(toks(t)[1:]),
  r'''#include <cstdio>
void pointToMax(int a[], int n, int **pp) {
    *pp = &a[0];                       // 通过二级指针改一级指针
    for (int i = 1; i < n; i++)
        if (a[i] > **pp) *pp = &a[i];
}
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int *p = a;
    pointToMax(a, n, &p);              // 传 p 的地址
    printf("%d\n", *p);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int *p = a, **pp = &p;             // 局部二级指针
    for (int i = 1; i < n; i++) if (a[i] > **pp) *pp = &a[i];
    printf("%d\n", **pp);
    return 0;
}
''',
  ["指针", "二级指针"])

A("【指针】new 与 delete 动态数组求和", SEC_PTR, 2,
  stmt("用 `new int[n]` 申请动态数组存放 `n` 个整数，求和后 `delete[]` 释放。"
       "读入 `n` 和 `n` 个整数，输出总和。",
       ["`new[]` 必须配 `delete[]`，写 `delete p` 是未定义行为",
        "数组长度可以运行时才定 —— 这是动态数组相对 `int a[10]` 的唯一优势",
        "释放后指针变成悬空指针，最好立刻置 `nullptr`"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：总和。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases(barr(61, 5), barr(62, 1), barr(63, 20),
                barr(64, 200, -1000000, 1000000), "3\n-1 -2 -3", barr(65, 100)),
  lambda t: "%d\n" % sum(toks(t)[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    int *a = new int[n];               // 运行时才知道长度
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    long long s = 0;
    for (int i = 0; i < n; i++) s += a[i];
    printf("%lld\n", s);
    delete[] a;                        // 必须 delete[]
    a = nullptr;
    return 0;
}
''',
  r'''#include <cstdio>
#include <vector>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    std::vector<int> a(n);             // 现代写法：容器自己管内存
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    long long s = 0;
    for (int x : a) s += x;
    printf("%lld\n", s);
    return 0;
}
''',
  ["指针", "new", "delete"])

A("【指针】指针实现冒泡排序", SEC_PTR, 2,
  stmt("用指针访问元素实现冒泡排序（升序）。读入 `n` 和 `n` 个整数，输出排序结果。",
       ["外层 `n-1` 趟，内层比较相邻两个 `*(p+j)` 和 `*(p+j+1)`",
        "加一个「本趟有没有交换」的标记可以提前结束",
        "输出一行，空格分隔"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：升序排列的数组。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases(barr(71, 5), barr(72, 1), "5\n5 4 3 2 1", barr(73, 20),
                barr(74, 15, -100, 100), "4\n3 3 3 3"),
  lambda t: " ".join(str(x) for x in sorted(toks(t)[1:])) + "\n",
  r'''#include <cstdio>
void bubble(int *a, int n) {
    for (int i = 0; i < n - 1; i++) {
        bool moved = false;
        for (int j = 0; j < n - 1 - i; j++)
            if (*(a + j) > *(a + j + 1)) {
                int t = *(a + j); *(a + j) = *(a + j + 1); *(a + j + 1) = t;
                moved = true;
            }
        if (!moved) break;             // 已经有序，提前收工
    }
}
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    bubble(a, n);
    for (int i = 0; i < n; i++) printf("%d%c", a[i], i + 1 == n ? '\n' : ' ');
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    int *a = new int[n];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    std::sort(a, a + n);               // 指针区间排序
    for (int i = 0; i < n; i++) printf("%d%c", a[i], i + 1 == n ? '\n' : ' ');
    delete[] a;
    return 0;
}
''',
  ["指针", "冒泡排序"])

A("【指针】指针倒序输出数组", SEC_PTR, 1,
  stmt("用指针从后往前遍历，倒序输出数组。读入 `n` 和 `n` 个整数。",
       ["从 `a + n - 1` 开始，往 `a` 方向走",
        "`--p` 是先减再解引用，注意别走到 `a` 之前",
        "输出一行，空格分隔"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：倒序的数组。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases(barr(81, 5), barr(82, 1), barr(83, 10),
                barr(84, 20, -100, 100), "6\n1 2 3 4 5 6", barr(85, 33)),
  lambda t: " ".join(str(x) for x in reversed(toks(t)[1:])) + "\n",
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    for (int *p = a + n - 1; p >= a; --p)   // 从尾部往头走
        printf("%d%c", *p, p == a ? '\n' : ' ');
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    std::reverse(a, a + n);            // 先原地反转再正序输出
    for (int i = 0; i < n; i++) printf("%d%c", a[i], i + 1 == n ? '\n' : ' ');
    return 0;
}
''',
  ["指针", "倒序"])

A("【指针】引用返回值替换最大值", SEC_PTR, 3,
  stmt("写函数 `int &maxRef(int a[], int n)` 返回最大元素的**引用**。"
       "读入 `n x` 和 `n` 个整数，把**第一个**最大值改成 `x` 后输出整个数组。",
       ["返回引用才能当左值用：`maxRef(a, n) = x;` 直接改到原数组",
        "返回局部变量的引用是悬空引用，返回数组元素或静态变量的引用才安全",
        "有多个最大值时只改第一个"]),
  "第一行 `n x`；第二行 `n` 个整数。",
  "一行：修改后的数组。",
  "- 1 ≤ n ≤ 1000\n- |x|, |a[i]| ≤ 10⁶",
  lambda: cases("5 0\n1 2 3 4 5", "3 -1\n7 7 7", "1 9\n-2",
                "%d %d\n%s" % (10, 100, " ".join(str(x) for x in rints(91, 10))),
                "%d %d\n%s" % (6, 0, " ".join(str(x) for x in rints(92, 6, -100, -1))),
                "4 5\n2 5 5 2"),
  lambda t: (lambda tok: (lambda v, x: (lambda i: " ".join(
      str(x if k == i else v[k]) for k in range(len(v))) + "\n")(v.index(max(v))))(
      tok[2:2 + tok[0]], tok[1]))(toks(t)),
  r'''#include <cstdio>
int &maxRef(int a[], int n) {
    int k = 0;
    for (int i = 1; i < n; i++) if (a[i] > a[k]) k = i;   // 严格大于，取第一个
    return a[k];                                          // 返回引用
}
int main() {
    int n, x;
    if (scanf("%d %d", &n, &x) != 2) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    maxRef(a, n) = x;                 // 当左值用
    for (int i = 0; i < n; i++) printf("%d%c", a[i], i + 1 == n ? '\n' : ' ');
    return 0;
}
''',
  r'''#include <cstdio>
int *maxPtr(int a[], int n) {         // 用指针达到同样效果
    int *p = a;
    for (int i = 1; i < n; i++) if (a[i] > *p) p = a + i;
    return p;
}
int main() {
    int n, x;
    if (scanf("%d %d", &n, &x) != 2) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    *maxPtr(a, n) = x;
    for (int i = 0; i < n; i++) printf("%d%c", a[i], i + 1 == n ? '\n' : ' ');
    return 0;
}
''',
  ["指针", "引用", "返回值"])

A("【指针】指针统计小于均值的元素个数", SEC_PTR, 2,
  stmt("读入 `n` 和 `n` 个整数，先算平均值（实数），再统计严格小于平均值的元素个数。"
       "输出平均值（保留 2 位小数）和个数，空格分隔。",
       ["均值要用 `double` 算，不能用整数除法 `s / n`",
        "比较时 `a[i] < avg` 会自动把 `a[i]` 转成 `double`",
        "输出一行：均值与个数"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：`平均值 个数`（均值保留 2 位小数）。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases("5\n1 2 3 4 5", "3\n1 1 1", "1\n-7", barr(101, 20),
                barr(102, 50, -1000, 1000), "4\n2 4 6 8"),
  lambda t: "%.2f %d\n" % (lambda v: (sum(v) / len(v),
                                      sum(1 for x in v if x < sum(v) / len(v))))(toks(t)[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    long long s = 0;
    for (int i = 0; i < n; i++) { scanf("%d", &a[i]); s += a[i]; }
    double avg = (double)s / n;        // 先转 double 再除
    int c = 0;
    for (int *p = a; p < a + n; ++p) if (*p < avg) c++;
    printf("%.2f %d\n", avg, c);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    double s = 0;
    for (int i = 0; i < n; i++) { scanf("%d", &a[i]); s += a[i]; }
    double avg = s / n;
    int c = 0;
    for (int i = 0; i < n; i++) c += (a[i] < avg);
    printf("%.2f %d\n", avg, c);
    return 0;
}
''',
  ["指针", "均值", "统计"])

A("【指针】指针差求数组元素个数", SEC_PTR, 2,
  stmt("读入 `n` 和 `n` 个整数，输出两个数：`n` 本身、以及 `&a[n] - a`（指针相减得到的元素个数）。"
       "两个数应当相等。",
       ["同类型的两个指针相减，结果是它们之间相差的**元素个数**，不是字节数",
        "`&a[n]` 是「最后一个元素再往后一格」的地址，合法可算但不可解引用",
        "输出一行两个整数"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：`n` 与 `&a[n] - a`。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases(barr(111, 5), barr(112, 1), barr(113, 20),
                barr(114, 100), barr(115, 7), barr(116, 333)),
  lambda t: "%d %d\n" % (lambda tok: (tok[0], tok[0]))(toks(t)),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    printf("%d %d\n", n, (int)(&a[n] - a));   // 指针相减得元素个数
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int *begin = a, *end = a;            // 用一个指针走到末尾
    while (end < a + n) ++end;
    printf("%d %d\n", n, (int)(end - begin));
    return 0;
}
''',
  ["指针", "指针差"])

A("【指针】动态二维数组求每行之和", SEC_PTR, 3,
  stmt("用 `new int*[n]` 申请二维动态数组，读入 `n` 行 `m` 列的矩阵，输出每行元素之和（每行一个数）。",
       ["`int **a = new int*[n]` 之后，还要对每一行 `a[i] = new int[m]`",
        "释放顺序反过来：先 `delete[] a[i]`，再 `delete[] a`",
        "一行的和用 `long long`"]),
  "第一行 `n m`；之后 `n` 行，每行 `m` 个整数。",
  "`n` 行，每行一个和。",
  "- 1 ≤ n, m ≤ 100\n- |x| ≤ 10⁴",
  lambda: cases("2 2\n1 2\n3 4", "1 1\n-5", "3 1\n1\n2\n3",
                "2 3\n1 2 3\n-1 -2 -3",
                "%d %d\n%s" % (4, 5, "\n".join(
                    " ".join(str(x) for x in rints(120 + r, 5, -100, 100)) for r in range(4))),
                "%d %d\n%s" % (3, 4, "\n".join(
                    " ".join(str(x) for x in rints(130 + r, 4, 1000, 2000)) for r in range(3)))),
  lambda t: (lambda tok: (lambda n, m: "".join(
      "%d\n" % sum(tok[2 + r * m:2 + (r + 1) * m]) for r in range(n)))(tok[0], tok[1]))(
      toks(t)),
  r'''#include <cstdio>
int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    int **a = new int *[n];            // 行指针数组
    for (int i = 0; i < n; i++) a[i] = new int[m];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++) scanf("%d", &a[i][j]);
    for (int i = 0; i < n; i++) {
        long long s = 0;
        for (int j = 0; j < m; j++) s += a[i][j];
        printf("%lld\n", s);
    }
    for (int i = 0; i < n; i++) delete[] a[i];   // 先放行
    delete[] a;                                   // 再放行指针数组
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    int *flat = new int[n * m];        // 一维连续内存模拟二维
    for (int i = 0; i < n * m; i++) scanf("%d", &flat[i]);
    for (int i = 0; i < n; i++) {
        long long s = 0;
        for (int j = 0; j < m; j++) s += flat[i * m + j];
        printf("%lld\n", s);
    }
    delete[] flat;
    return 0;
}
''',
  ["指针", "二维数组", "new"])

A("【指针】指针求两数组交集大小", SEC_PTR, 3,
  stmt("读入两个数组（含重复元素），求它们的**多重集交集**大小：某个值在两数组里分别出现 "
       "`c1`、`c2` 次，就对答案贡献 `min(c1, c2)`。输出交集大小。",
       ["先把第一个数组排序，再对第二个数组的每个元素做一次二分查找并「消耗」一个",
        "直接对每个元素 `count(a) == count(b)` 相加会把重复算多",
        "输出一个整数"]),
  "第一行 `n m`；第二行 `n` 个整数；第三行 `m` 个整数。",
  "一行：交集大小。",
  "- 1 ≤ n, m ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases("5 4\n1 2 2 3 4\n2 2 5 3", "3 3\n1 1 1\n1 1 1", "1 1\n5\n6",
                "%d %d\n%s\n%s" % (8, 6, " ".join(str(x) for x in rints(141, 8, 1, 5)),
                                   " ".join(str(x) for x in rints(142, 6, 1, 5))),
                "%d %d\n%s\n%s" % (10, 10, " ".join(str(x) for x in rints(143, 10, 0, 3)),
                                   " ".join(str(x) for x in rints(144, 10, 0, 3))),
                "4 4\n1 2 3 4\n4 3 2 1"),
  lambda t: "%d\n" % (lambda tok: (lambda n, m, a, b: sum(
      min(a.count(v), b.count(v)) for v in set(a)))(tok[0], tok[1], tok[2:2 + tok[0]],
                                                    tok[2 + tok[0]:2 + tok[0] + tok[1]]))(toks(t)),
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    static int a[1005], b[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    for (int i = 0; i < m; i++) scanf("%d", &b[i]);
    std::sort(a, a + n);
    int used[1005] = {0}, c = 0;       // used 标记 a 里已被配对的下标
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++)
            if (!used[j] && a[j] == b[i]) { used[j] = 1; c++; break; }
    }
    printf("%d\n", c);
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    static int a[1005], b[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    for (int i = 0; i < m; i++) scanf("%d", &b[i]);
    std::sort(a, a + n);
    std::sort(b, b + m);
    int i = 0, j = 0, c = 0;           // 双指针归并式配对
    while (i < n && j < m) {
        if (a[i] == b[j]) { c++; i++; j++; }
        else if (a[i] < b[j]) i++;
        else j++;
    }
    printf("%d\n", c);
    return 0;
}
''',
  ["指针", "交集", "双指针"])

A("【指针】指针在有序数组中找第一个大于等于 x 的位置", SEC_PTR, 3,
  stmt("数组升序。读入 `n x` 和 `n` 个整数，输出第一个 `≥ x` 的元素位置（从 1 开始）；"
       "若所有元素都小于 `x`，输出 `n + 1`。",
       ["这就是 `lower_bound` 的语义，边界是「答案可以是 n」（表示插在末尾）",
        "手写二分的循环条件是 `lo < hi`，最后返回 `lo`",
        "输出一个整数"]),
  "第一行 `n x`；第二行 `n` 个升序整数。",
  "一行：位置（1 起）或 `n + 1`。",
  "- 1 ≤ n ≤ 10⁵\n- |x|, |a[i]| ≤ 10⁹",
  lambda: cases("5 3\n1 2 3 4 5", "5 6\n1 2 3 4 5", "5 0\n1 2 3 4 5", "1 1\n1",
                "%d %d\n%s" % (10, 8, " ".join(str(2 * i) for i in range(10))),
                "%d %d\n%s" % (20, -100, " ".join(str(3 * i - 20) for i in range(20)))),
  lambda t: (lambda tok: (lambda n, x, a: "%d\n" % next(
      (i + 1 for i, v in enumerate(a) if v >= x), n + 1))(tok[0], tok[1],
                                                          tok[2:2 + tok[0]]))(toks(t)),
  r'''#include <cstdio>
int main() {
    int n, x;
    if (scanf("%d %d", &n, &x) != 2) return 0;
    static int a[100005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int lo = 0, hi = n;                // 答案允许是 n
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] >= x) hi = mid; else lo = mid + 1;
    }
    printf("%d\n", lo + 1);
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n, x;
    if (scanf("%d %d", &n, &x) != 2) return 0;
    static int a[100005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int *p = std::lower_bound(a, a + n, x);   // 指针差就是位置
    printf("%d\n", (int)(p - a) + 1);
    return 0;
}
''',
  ["指针", "二分", "lower_bound"])

A("【指针】指针原地反转数组", SEC_PTR, 2,
  stmt("用首尾两个指针向中间靠拢，原地反转数组。读入 `n` 和 `n` 个整数，输出反转结果。",
       ["`int *l = a, *r = a + n - 1;` 循环条件 `l < r`",
        "每轮交换后 `++l`、`--r`，走到中间就停",
        "输出一行，空格分隔"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：反转后的数组。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases(barr(151, 5), barr(152, 4), barr(153, 1), barr(154, 20),
                "5\n1 2 3 4 5", barr(155, 33)),
  lambda t: " ".join(str(x) for x in reversed(toks(t)[1:])) + "\n",
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int *l = a, *r = a + n - 1;        // 首尾双指针
    while (l < r) { int t = *l; *l++ = *r; *r-- = t; }
    for (int i = 0; i < n; i++) printf("%d%c", a[i], i + 1 == n ? '\n' : ' ');
    return 0;
}
''',
  r'''#include <cstdio>
void rev(int *a, int n) {              // 递归反转
    if (n <= 1) return;
    int t = a[0]; a[0] = a[n - 1]; a[n - 1] = t;
    rev(a + 1, n - 2);
}
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    rev(a, n);
    for (int i = 0; i < n; i++) printf("%d%c", a[i], i + 1 == n ? '\n' : ' ');
    return 0;
}
''',
  ["指针", "反转", "双指针"])

A("【指针】交换两个指针的指向", SEC_PTR, 2,
  stmt("有 `int a`、`int b` 和两个指针 `int *p = &a`、`int *q = &b`。"
       "**交换 p 和 q 本身**（不是交换 a 和 b），读入 `a b`，输出交换后 `*p` 与 `*q`。",
       ["`int *t = p; p = q; q = t;` 换的是指针，`a`、`b` 的值不变",
        "若写 `*p` 和 `*q` 互换，那就是改值不是改指向 —— 两件事完全不同",
        "输出一行两个整数"]),
  "一行两个整数 `a b`。",
  "一行：`*p *q`（交换指向之后）。",
  "- |a|, |b| ≤ 10⁹",
  lambda: cases("3 5", "0 0", "-1 1", "100 -100", "7 7", "123 456"),
  lambda t: "%d %d\n" % tuple(reversed(toks(t))),
  r'''#include <cstdio>
int main() {
    int a, b;
    if (scanf("%d %d", &a, &b) != 2) return 0;
    int *p = &a, *q = &b;
    int *t = p; p = q; q = t;          // 换的是指针本身
    printf("%d %d\n", *p, *q);         // 所以变成 b a
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int a, b;
    if (scanf("%d %d", &a, &b) != 2) return 0;
    int *arr[2] = {&a, &b};            // 用指针数组做一次对调
    int *tmp = arr[0]; arr[0] = arr[1]; arr[1] = tmp;
    printf("%d %d\n", *arr[0], *arr[1]);
    return 0;
}
''',
  ["指针", "指向", "交换"])

A("【指针】指针实现选择排序", SEC_PTR, 2,
  stmt("用指针实现选择排序（升序）。读入 `n` 和 `n` 个整数，输出排序结果，并额外输出"
       "「交换次数」。共两行：第一行排序结果，第二行交换次数。",
       ["选择排序每轮找最小值的下标，只有 `i != k` 时才真交换，交换次数才是准确的",
        "把每次 `std::swap` 都计入，全相等数组的交换次数会变成 0 —— 这是对的",
        "输出两行"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "第一行：升序数组；第二行：交换次数。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases("5\n5 4 3 2 1", "5\n1 2 3 4 5", "4\n3 3 3 3", "2\n2 1",
                barr(161, 10), barr(162, 8, -9, 0)),
  _select_sort,
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int sw = 0;
    for (int i = 0; i < n - 1; i++) {
        int k = i;
        for (int j = i + 1; j < n; j++) if (*(a + j) < *(a + k)) k = j;
        if (k != i) { int t = *(a + i); *(a + i) = *(a + k); *(a + k) = t; sw++; }
    }
    for (int i = 0; i < n; i++) printf("%d%c", a[i], i + 1 == n ? '\n' : ' ');
    printf("%d\n", sw);
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    int *a = new int[n];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int sw = 0;
    for (int *p = a; p < a + n - 1; ++p) {
        int *m = p;
        for (int *q = p + 1; q < a + n; ++q) if (*q < *m) m = q;
        if (m != p) { std::swap(*p, *m); sw++; }
    }
    for (int i = 0; i < n; i++) printf("%d%c", a[i], i + 1 == n ? '\n' : ' ');
    printf("%d\n", sw);
    delete[] a;
    return 0;
}
''',
  ["指针", "选择排序", "交换次数"])

A("【指针】引用出参累计求和与积", SEC_PTR, 2,
  stmt("写函数 `void accum(int x, long long &sum, long long &prod)`，"
       "把 `x` 累加到 `sum`、乘到 `prod` 上。读入 `n` 和 `n` 个整数，输出最终的 `sum` 与 `prod`。",
       ["`sum` 要先初始化为 0、`prod` 初始化为 1，初始化放在 main 里更清楚",
        "10 个 5 相乘就到 9765625，`prod` 用 `long long` 更保险",
        "输出一行两个整数"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：`sum prod`。",
  "- 1 ≤ n ≤ 20\n- 1 ≤ x ≤ 20\n- 保证 `prod` 不超过 10¹⁸",
  lambda: cases("5\n1 2 3 4 5", "1\n1", "1\n2", "10\n5 5 5 5 5 5 5 5 5 5",
                "3\n20 20 20", "6\n1 3 5 7 9 11"),
  lambda t: "%d %d\n" % (lambda v: (sum(v), __import__("math").prod(v)))(toks(t)[1:]),
  r'''#include <cstdio>
void accum(int x, long long &sum, long long &prod) {
    sum += x;
    prod *= x;
}
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    long long s = 0, p = 1;            // 初值：和 0、积 1
    for (int i = 0; i < n; i++) { int x; scanf("%d", &x); accum(x, s, p); }
    printf("%lld %lld\n", s, p);
    return 0;
}
''',
  r'''#include <cstdio>
struct Accum { long long sum = 0, prod = 1; };
void accum(int x, Accum &a) {          // 用结构体打包，同样是引用出参
    a.sum += x; a.prod *= x;
}
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    Accum a;
    for (int i = 0; i < n; i++) { int x; scanf("%d", &x); accum(x, a); }
    printf("%lld %lld\n", a.sum, a.prod);
    return 0;
}
''',
  ["指针", "引用", "出参"])

A("【指针】指针数组排序后输出", SEC_PTR, 3,
  stmt("建立 `int *p[n]` 指针数组，每个元素指向原数组的一项，按指针指向的值排序后，"
       "用指针数组的顺序输出。读入 `n` 和 `n` 个整数，输出升序结果。",
       ["排序的是**指针**，原数组一动没动 —— 这就是「索引排序」",
        "比较器写 `bool cmp(int *a, int *b) { return *a < *b; }`",
        "输出一行，空格分隔"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：升序结果。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases(barr(171, 5), "4\n4 3 2 1", "1\n7", barr(172, 20),
                barr(173, 15, -100, 100), "5\n2 2 1 1 3"),
  lambda t: " ".join(str(x) for x in sorted(toks(t)[1:])) + "\n",
  r'''#include <cstdio>
#include <algorithm>
bool cmp(int *a, int *b) { return *a < *b; }
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    static int *p[1005];
    for (int i = 0; i < n; i++) { scanf("%d", &a[i]); p[i] = &a[i]; }
    std::sort(p, p + n, cmp);          // 只排指针
    for (int i = 0; i < n; i++) printf("%d%c", *p[i], i + 1 == n ? '\n' : ' ');
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    static int *p[1005];
    for (int i = 0; i < n; i++) { scanf("%d", &a[i]); p[i] = &a[i]; }
    for (int i = 0; i < n - 1; i++)    // 手写指针数组冒泡
        for (int j = 0; j < n - 1 - i; j++)
            if (*p[j] > *p[j + 1]) { int *t = p[j]; p[j] = p[j + 1]; p[j + 1] = t; }
    for (int i = 0; i < n; i++) printf("%d%c", *p[i], i + 1 == n ? '\n' : ' ');
    return 0;
}
''',
  ["指针", "指针数组", "排序"])

A("【指针】指针遍历字符串统计数字字符", SEC_PTR, 2,
  stmt("用指针遍历一个字符串（不含空格），统计其中数字字符 `0`~`9` 的个数。",
       ["字符串以 `\\0` 结尾，循环条件写 `*p != '\\0'`",
        "判断用 `*p >= '0' && *p <= '9'`，别写 `isdigit` 之外的自造条件（负字符会出错）",
        "输出一个整数"]),
  "一行一个字符串（长度 ≤ 100，仅含可见 ASCII，不含空格）。",
  "一行：数字字符个数。",
  "- 1 ≤ 字符串长度 ≤ 100",
  lambda: cases("a1b2c3", "abc", "123456", "A1!z9", "x0y0z0", "Hello2024World"),
  lambda t: "%d\n" % sum(1 for ch in t.strip() if ch.isdigit()),
  r'''#include <cstdio>
int main() {
    char s[128];
    if (scanf("%127s", s) != 1) return 0;
    int c = 0;
    for (char *p = s; *p != '\0'; ++p)          // 指针遍历到 '\0'
        if (*p >= '0' && *p <= '9') c++;
    printf("%d\n", c);
    return 0;
}
''',
  r'''#include <cstdio>
#include <cstring>
int main() {
    char s[128];
    if (scanf("%127s", s) != 1) return 0;
    int c = 0;
    for (int i = 0, n = (int)strlen(s); i < n; i++)
        if (s[i] >= '0' && s[i] <= '9') c++;
    printf("%d\n", c);
    return 0;
}
''',
  ["指针", "字符串", "遍历"])

# ===================================================================== #
#  SEC_STR · 字符数组与字符串（20 题）
# ===================================================================== #

def _strlen(t: str) -> str:
    return "%d\n" % len(t.strip())


def _concat(t: str) -> str:
    a, b = t.split("\n")[:2]
    return a + b + "\n"


def _classify(t: str) -> str:
    s = t.rstrip("\n")
    letters = sum(1 for ch in s if ch.isalpha())
    digits = sum(1 for ch in s if ch.isdigit())
    return "%d %d %d\n" % (letters, digits, len(s) - letters - digits)


def _words(t: str) -> str:
    return "%d\n" % len(t.split())


def _atoi(t: str) -> str:
    return "%d\n" % int(t.strip())


def _digit_sum(t: str) -> str:
    s = t.strip()
    total, cur = 0, ""
    for ch in s:
        if ch.isdigit():
            cur += ch
        else:
            if cur:
                total += int(cur)
                cur = ""
    if cur:
        total += int(cur)
    return "%d\n" % total


def _longest_run(t: str) -> str:
    s = t.strip()
    best = run = 1 if s else 0
    for i in range(1, len(s)):
        run = run + 1 if s[i] == s[i - 1] else 1
        best = max(best, run)
    return "%d\n" % best


def _vowels(t: str) -> str:
    return "%d\n" % sum(1 for ch in t.strip().lower() if ch in "aeiou")


def _rotate_left(t: str) -> str:
    ln = t.split("\n")
    s, k = ln[0].strip(), int(ln[1].strip())
    k %= len(s)
    return s[k:] + s[:k] + "\n"


def _anagram(t: str) -> str:
    a, b = t.split("\n")[:2]
    return "YES\n" if sorted(a) == sorted(b) else "NO\n"


def _dedup(t: str) -> str:
    s = t.strip()
    seen, out = set(), []
    for ch in s:
        if ch not in seen:
            seen.add(ch)
            out.append(ch)
    return "".join(out) + "\n"


def _pal_sub(t: str) -> str:
    s = t.strip()
    c = 0
    for i in range(len(s)):
        for j in range(i + 2, len(s) + 1):
            sub = s[i:j]
            if sub == sub[::-1]:
                c += 1
    return "%d\n" % c


def _compress(t: str) -> str:
    s = t.strip()
    out = []
    i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        out.append("%s%d" % (s[i], j - i))
        i = j
    return "".join(out) + "\n"


A("【字符串】自己实现 strlen", SEC_STR, 1,
  stmt("不用 `strlen`，自己数到 `\\0` 为止。读入一个不含空格的字符串（长度 ≤ 100），输出它的长度。",
       ["`char s[105]` 要留出放 `\\0` 的空间 —— 「abc」占 4 个字节",
        "循环条件写 `s[i] != '\\0'`",
        "输出一个整数"]),
  "一行一个不含空格的字符串。",
  "一行：长度。",
  "- 1 ≤ 长度 ≤ 100",
  lambda: cases("abc", "a", "hello", "CPlusPlus", "12345", "abcdefghij"),
  _strlen,
  r'''#include <cstdio>
int main() {
    char s[105];
    if (scanf("%104s", s) != 1) return 0;
    int n = 0;
    while (s[n] != '\0') n++;          // 数到 '\0'
    printf("%d\n", n);
    return 0;
}
''',
  r'''#include <cstdio>
#include <cstring>
int main() {
    char s[105];
    if (scanf("%104s", s) != 1) return 0;
    printf("%d\n", (int)strlen(s));     // 库里也是这么数的
    return 0;
}
''',
  ["字符串", "strlen"])

A("【字符串】自己实现字符串拼接", SEC_STR, 1,
  stmt("不用 `strcat`，把第二个串接到第一个串末尾。读入两行不含空格的字符串，输出拼接结果。",
       ["拼接时从第一个串的 `\\0` 位置开始写，写完再补一个新的 `\\0`",
        "目标数组容量要够放下两串加 `\\0`",
        "输出一行"]),
  "两行，各一个不含空格的字符串。",
  "一行：拼接后的字符串。",
  "- 每行长度 ≤ 50",
  lambda: cases("abc\ndef", "a\nb", "hello\nworld", "C++\n2024", "x\ny", "123\n456"),
  _concat,
  r'''#include <cstdio>
int main() {
    char a[120], b[60];
    if (scanf("%59s", a) != 1) return 0;
    if (scanf("%59s", b) != 1) return 0;
    int i = 0, j = 0;
    while (a[i] != '\0') i++;          // 走到 a 的末尾
    while (b[j] != '\0') a[i++] = b[j++];
    a[i] = '\0';                       // 补结束符
    printf("%s\n", a);
    return 0;
}
''',
  r'''#include <cstdio>
#include <cstring>
int main() {
    char a[120], b[60];
    if (scanf("%59s", a) != 1) return 0;
    if (scanf("%59s", b) != 1) return 0;
    strcat(a, b);                      // 库函数版
    printf("%s\n", a);
    return 0;
}
''',
  ["字符串", "strcat"])

A("【字符串】字符串反转输出", SEC_STR, 1,
  stmt("读入一个不含空格的字符串，倒序输出。",
       ["首尾双指针交换，或直接从末尾往前输出",
        "`for (int i = n - 1; i >= 0; i--)` 的 `i` 必须是有符号类型",
        "输出一行"]),
  "一行一个不含空格的字符串。",
  "一行：倒序字符串。",
  "- 1 ≤ 长度 ≤ 100",
  lambda: cases("abc", "a", "hello", "12345", "CPlusPlus", "xy"),
  lambda t: t.strip()[::-1] + "\n",
  r'''#include <cstdio>
int main() {
    char s[105];
    if (scanf("%104s", s) != 1) return 0;
    int n = 0;
    while (s[n]) n++;
    for (int i = n - 1; i >= 0; i--) putchar(s[i]);   // i 必须是有符号
    printf("\n");
    return 0;
}
''',
  r'''#include <cstdio>
#include <cstring>
#include <algorithm>
int main() {
    char s[105];
    if (scanf("%104s", s) != 1) return 0;
    std::reverse(s, s + strlen(s));    // 原地反转
    printf("%s\n", s);
    return 0;
}
''',
  ["字符串", "反转"])

A("【字符串】回文串判断", SEC_STR, 1,
  stmt("读入一个不含空格的字符串（只含小写字母），判断它是不是回文串。是输出 `YES`，否则输出 `NO`。",
       ["首尾字符逐个比较，走到中间就停",
        "单字符一定是回文",
        "只输出 `YES` 或 `NO`"]),
  "一行一个只含小写字母的字符串。",
  "一行：`YES` 或 `NO`。",
  "- 1 ≤ 长度 ≤ 100",
  lambda: cases("abcba", "abca", "a", "ab", "aaaa", "abccba"),
  lambda t: "YES\n" if t.strip() == t.strip()[::-1] else "NO\n",
  r'''#include <cstdio>
int main() {
    char s[105];
    if (scanf("%104s", s) != 1) return 0;
    int n = 0;
    while (s[n]) n++;
    bool ok = true;
    for (int i = 0, j = n - 1; i < j; i++, j--)
        if (s[i] != s[j]) { ok = false; break; }
    printf("%s\n", ok ? "YES" : "NO");
    return 0;
}
''',
  r'''#include <cstdio>
#include <cstring>
int main() {
    char s[105];
    if (scanf("%104s", s) != 1) return 0;
    int n = (int)strlen(s);
    bool ok = true;
    for (int i = 0; i < n / 2; i++) if (s[i] != s[n - 1 - i]) ok = false;
    printf("%s\n", ok ? "YES" : "NO");
    return 0;
}
''',
  ["字符串", "回文"])

A("【字符串】字符分类统计", SEC_STR, 1,
  stmt("读入一行文本（可含空格），统计其中**字母**、**数字**、**其他字符**（含空格和符号）"
       "各有多少个，输出三个整数。",
       ["整行读入必须用 `getline` 或 `fgets`，`cin >>` 遇到空格就停了",
        "行尾的 `\\n` 不属于文本内容，要排除",
        "空格算「其他」，不是分隔符"]),
  "一行文本（长度 ≤ 100，仅含可见 ASCII 字符与空格）。",
  "一行：字母数、数字数、其他字符数。",
  "- 1 ≤ 长度 ≤ 100",
  lambda: cases("abc123", "a b c", "Hello, World!", "123", "!!!", "abc def 123 !"),
  _classify,
  r'''#include <cstdio>
#include <cstring>
int main() {
    char s[128];
    if (!fgets(s, sizeof(s), stdin)) return 0;
    int n = (int)strlen(s);
    if (n > 0 && s[n - 1] == '\n') s[--n] = '\0';   // 去掉行尾换行
    int le = 0, di = 0, ot = 0;
    for (int i = 0; i < n; i++) {
        char c = s[i];
        if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) le++;
        else if (c >= '0' && c <= '9') di++;
        else ot++;
    }
    printf("%d %d %d\n", le, di, ot);
    return 0;
}
''',
  r'''#include <cstdio>
#include <iostream>
#include <string>
#include <cctype>
int main() {
    std::string s;
    if (!std::getline(std::cin, s)) return 0;
    int le = 0, di = 0, ot = 0;
    for (char c : s) {
        if (isalpha((unsigned char)c)) le++;
        else if (isdigit((unsigned char)c)) di++;
        else ot++;
    }
    printf("%d %d %d\n", le, di, ot);
    return 0;
}
''',
  ["字符串", "getline", "字符分类"])

A("【字符串】统计单词个数", SEC_STR, 2,
  stmt("读入一行英文（单词之间用一个或多个空格分隔，行首行尾可能有空格），输出单词个数。",
       ["`cin >> word` 天然跳过空白，循环读到最后即可 —— 这是最简单的写法",
        "用 `getline` 的话要自己处理连续空格和首尾空格",
        "输出一个整数"]),
  "一行英文文本（长度 ≤ 200）。",
  "一行：单词个数。",
  "- 1 ≤ 长度 ≤ 200\n- 单词只含字母",
  lambda: cases("hello world", "a", "  a   b  c  ", "one two three four",
                "x y", "The quick brown fox jumps"),
  _words,
  r'''#include <cstdio>
#include <iostream>
#include <string>
int main() {
    std::string w;
    int c = 0;
    while (std::cin >> w) c++;         // >> 自动跳过空白
    printf("%d\n", c);
    return 0;
}
''',
  r'''#include <cstdio>
#include <cstring>
int main() {
    char s[256];
    if (!fgets(s, sizeof(s), stdin)) return 0;
    int c = 0;
    bool in = false;
    for (int i = 0; s[i]; i++) {
        if (s[i] == ' ' || s[i] == '\n') in = false;
        else if (!in) { in = true; c++; }   // 从空白进入非空白才算一个新词
    }
    printf("%d\n", c);
    return 0;
}
''',
  ["字符串", "单词计数"])

A("【字符串】大小写互换", SEC_STR, 1,
  stmt("读入一个不含空格的字符串，把大写字母改成小写、小写字母改成大写，其余不变，输出结果。",
       ["`c - 'a' + 'A'` 是小写转大写，反过去就是大写转小写",
        "`toupper` / `tolower` 只对字母生效，其他字符原样返回",
        "输出一行"]),
  "一行一个不含空格的字符串。",
  "一行：大小写互换后的字符串。",
  "- 1 ≤ 长度 ≤ 100",
  lambda: cases("AbC", "abc", "ABC", "a1B2", "Hello", "Zz"),
  lambda t: t.strip().swapcase() + "\n",
  r'''#include <cstdio>
int main() {
    char s[105];
    if (scanf("%104s", s) != 1) return 0;
    for (int i = 0; s[i]; i++) {
        if (s[i] >= 'a' && s[i] <= 'z') s[i] = char(s[i] - 'a' + 'A');
        else if (s[i] >= 'A' && s[i] <= 'Z') s[i] = char(s[i] - 'A' + 'a');
    }
    printf("%s\n", s);
    return 0;
}
''',
  r'''#include <cstdio>
#include <cctype>
int main() {
    char s[105];
    if (scanf("%104s", s) != 1) return 0;
    for (int i = 0; s[i]; i++) {
        if (isupper((unsigned char)s[i])) s[i] = (char)tolower((unsigned char)s[i]);
        else if (islower((unsigned char)s[i])) s[i] = (char)toupper((unsigned char)s[i]);
    }
    printf("%s\n", s);
    return 0;
}
''',
  ["字符串", "大小写"])

A("【字符串】字典序比较两串", SEC_STR, 2,
  stmt("读入两行不含空格的字符串，按字典序比较：第一个串小输出 `-1`，相等输出 `0`，"
       "第一个串大输出 `1`。",
       ["`strcmp` 返回的是「差值」而不是固定的 -1/0/1，要自己归一",
        "字典序是逐字符比 ASCII 码，遇到第一个不同的字符就定胜负",
        "只输出 -1、0 或 1"]),
  "两行，各一个不含空格的字符串。",
  "一行：`-1`、`0` 或 `1`。",
  "- 每行长度 ≤ 50",
  lambda: cases("abc\nabd", "abc\nabc", "abd\nabc", "a\nab", "ab\na", "Z\na"),
  lambda t: (lambda a, b: "%d\n" % (0 if a == b else (1 if a > b else -1)))(
      *t.split("\n")[:2]),
  r'''#include <cstdio>
#include <cstring>
int main() {
    char a[60], b[60];
    if (scanf("%59s", a) != 1) return 0;
    if (scanf("%59s", b) != 1) return 0;
    int c = strcmp(a, b);              // 返回差值，不是 -1/0/1
    printf("%d\n", c < 0 ? -1 : (c > 0 ? 1 : 0));
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    char a[60], b[60];
    if (scanf("%59s", a) != 1) return 0;
    if (scanf("%59s", b) != 1) return 0;
    int i = 0;
    while (a[i] && a[i] == b[i]) i++;  // 手写逐字符比较
    int r = 0;
    if (a[i] != b[i]) r = (unsigned char)a[i] < (unsigned char)b[i] ? -1 : 1;
    printf("%d\n", r);
    return 0;
}
''',
  ["字符串", "strcmp", "字典序"])

A("【字符串】子串首次出现位置", SEC_STR, 2,
  stmt("读入两个不含空格的字符串 `s` 和 `p`，输出 `p` 在 `s` 中**第一次**出现的起始位置"
       "（从 1 开始），找不到输出 `-1`。",
       ["朴素匹配：对每个起点 `i` 逐字符比对，全中就返回",
        "`s.find(p)` 返回 `string::npos` 表示没找到，`npos` 是无符号的大数，用 `==` 判断",
        "起始位置从 1 开始，要 `+1`"]),
  "两行：第一行 `s`，第二行 `p`。",
  "一行：起始位置或 `-1`。",
  "- 1 ≤ |p| ≤ |s| ≤ 100",
  lambda: cases("abcabc\nbc", "abcdef\ndef", "abcdef\nxyz", "aaaa\naa", "a\na", "abab\nba"),
  lambda t: (lambda a, b: "%d\n" % (a.find(b) + 1 if b in a else -1))(*t.split("\n")[:2]),
  r'''#include <cstdio>
#include <cstring>
int main() {
    char s[105], p[105];
    if (scanf("%104s", s) != 1) return 0;
    if (scanf("%104s", p) != 1) return 0;
    int n = (int)strlen(s), m = (int)strlen(p);
    int ans = -1;
    for (int i = 0; i + m <= n; i++) {
        int k = 0;
        while (k < m && s[i + k] == p[k]) k++;
        if (k == m) { ans = i + 1; break; }   // 题面要 1 起
    }
    printf("%d\n", ans);
    return 0;
}
''',
  r'''#include <cstdio>
#include <iostream>
#include <string>
int main() {
    std::string s, p;
    if (!(std::cin >> s)) return 0;
    if (!(std::cin >> p)) return 0;
    size_t k = s.find(p);              // npos 是无符号大数
    printf("%d\n", k == std::string::npos ? -1 : (int)k + 1);
    return 0;
}
''',
  ["字符串", "子串", "find"])

A("【字符串】删除指定字符", SEC_STR, 2,
  stmt("读入一个不含空格的字符串和一个字符，删掉字符串里所有该字符，输出结果。"
       "输出可能为空行。",
       ["用「读指针 + 写指针」原地压缩：不删的字符往前搬",
        "删完要补 `\\0`，否则尾巴上的残留还会被打印",
        "如果全被删光，输出一个空行"]),
  "第一行字符串（不含空格），第二行一个字符。",
  "一行：删除后的字符串。",
  "- 1 ≤ 长度 ≤ 100",
  lambda: cases("abcabc\na", "abc\nd", "aaaa\na", "banana\nn", "xyz\nx", "hello\nl"),
  lambda t: (lambda a, c: a.replace(c, "") + "\n")(*t.strip("\n").split("\n")[:2]),
  r'''#include <cstdio>
int main() {
    char s[105], c;
    if (scanf("%104s", s) != 1) return 0;
    scanf(" %c", &c);                  // 前面的空格跳过换行
    int k = 0;
    for (int i = 0; s[i]; i++) if (s[i] != c) s[k++] = s[i];   // 读写双指针
    s[k] = '\0';
    printf("%s\n", s);
    return 0;
}
''',
  r'''#include <cstdio>
#include <iostream>
#include <string>
#include <algorithm>
int main() {
    std::string s, line;
    char c;
    if (!(std::cin >> s)) return 0;
    if (!(std::cin >> c)) return 0;
    s.erase(std::remove(s.begin(), s.end(), c), s.end());   // erase-remove 惯用法
    printf("%s\n", s.c_str());
    return 0;
}
''',
  ["字符串", "删除", "双指针"])

A("【字符串】按字典序排序若干字符串", SEC_STR, 3,
  stmt("读入 `n` 个不含空格的字符串，按字典序升序输出，每行一个。",
       ["`std::sort` 配 `std::string` 默认就是字典序",
        "用 `char[105]` 数组的话要写 `strcmp` 比较器",
        "每行输出一个字符串"]),
  "第一行 `n`；之后 `n` 行，每行一个不含空格的字符串。",
  "`n` 行：按字典序升序。",
  "- 1 ≤ n ≤ 100\n- 每串长度 ≤ 50",
  lambda: cases("3\nbanana\napple\ncherry", "1\nonly", "3\nb\na\nc",
                "5\nzebra\napple\nmango\nbanana\ncherry", "3\naa\na\naaa",
                "%d\n%s" % (6, "\n".join(sorted(
                    "".join(random.Random(200 + i).choice(string.ascii_lowercase)
                            for _ in range(4)) for i in range(6))))),
  lambda t: "".join(x + "\n" for x in sorted(t.strip().splitlines()[1:])),
  r'''#include <cstdio>
#include <cstring>
#include <algorithm>
char s[105][60];
int idx[105];
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    for (int i = 0; i < n; i++) { scanf("%59s", s[i]); idx[i] = i; }
    std::sort(idx, idx + n, [](int x, int y) {     // 排下标，不排二维数组
        return strcmp(s[x], s[y]) < 0;
    });
    for (int i = 0; i < n; i++) printf("%s\n", s[idx[i]]);
    return 0;
}
''',
  r'''#include <cstdio>
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    std::vector<std::string> v(n);
    for (int i = 0; i < n; i++) std::cin >> v[i];
    std::sort(v.begin(), v.end());     // string 默认字典序
    for (auto &x : v) printf("%s\n", x.c_str());
    return 0;
}
''',
  ["字符串", "排序", "字典序"])

A("【字符串】字符串压缩", SEC_STR, 3,
  stmt("把连续相同的字符压缩成「字符 + 次数」。例如 `aabbb` 压缩成 `a2b3`，`abc` 压缩成 `a1b1c1`。"
       "读入一个不含空格的字符串，输出压缩结果。",
       ["统计每一段连续相同字符的长度，然后「字符 + 次数」拼起来",
        "次数为 1 也要写出来（题面规定），不要自作聪明省略",
        "段数最多等于字符串长度"]),
  "一行一个不含空格的字符串。",
  "一行：压缩结果。",
  "- 1 ≤ 长度 ≤ 100",
  lambda: cases("aabbb", "abc", "aaaa", "a", "aabbcc", "abbbbc"),
  _compress,
  r'''#include <cstdio>
int main() {
    char s[105];
    if (scanf("%104s", s) != 1) return 0;
    int i = 0;
    while (s[i]) {
        int j = i;
        while (s[j] == s[i]) j++;      // 找到这一段结束的位置
        printf("%c%d", s[i], j - i);
        i = j;
    }
    printf("\n");
    return 0;
}
''',
  r'''#include <cstdio>
#include <iostream>
#include <string>
int main() {
    std::string s;
    if (!(std::cin >> s)) return 0;
    std::string out;
    for (size_t i = 0; i < s.size();) {
        size_t j = i;
        while (j < s.size() && s[j] == s[i]) j++;
        out += s[i];
        out += std::to_string(j - i);
        i = j;
    }
    printf("%s\n", out.c_str());
    return 0;
}
''',
  ["字符串", "压缩", "游程"])

A("【字符串】自己实现 atoi", SEC_STR, 2,
  stmt("不用 `atoi`，把数字字符串转成整数。读入一行（可能有前导 `+`/`-`，其余全是数字），"
       "输出转换后的整数。",
       ["跳过符号位后逐位 `r = r * 10 + (c - '0')`",
        "负号要最后再乘上去",
        "保证结果在 `int` 范围内"]),
  "一行：可选的符号 + 若干数字。",
  "一行：转换后的整数。",
  "- 1 ≤ 数字位数 ≤ 9\n- 结果在 `int` 范围内",
  lambda: cases("123", "-456", "+789", "0", "-1", "2147483647"),
  _atoi,
  r'''#include <cstdio>
int main() {
    char s[32];
    if (scanf("%31s", s) != 1) return 0;
    int i = 0, sign = 1;
    if (s[0] == '+' || s[0] == '-') { if (s[0] == '-') sign = -1; i = 1; }
    int r = 0;
    for (; s[i]; i++) r = r * 10 + (s[i] - '0');   // 逐位累加
    printf("%d\n", sign * r);
    return 0;
}
''',
  r'''#include <cstdio>
#include <cstdlib>
int main() {
    char s[32];
    if (scanf("%31s", s) != 1) return 0;
    printf("%d\n", atoi(s));           // 库函数版
    return 0;
}
''',
  ["字符串", "atoi", "进制"])

A("【字符串】字符串中的数字求和", SEC_STR, 3,
  stmt("读入一个不含空格的字符串，把其中每一段连续的数字当作一个整数，求它们的和。"
       "例如 `a12b3c` 里是 12 和 3，和为 15。",
       ["用一个累加器 `cur`，遇到数字就 `cur = cur * 10 + d`",
        "遇到非数字时把 `cur` 结算掉并清零",
        "结尾如果还在数字里，别忘了再结算一次"]),
  "一行一个不含空格的字符串。",
  "一行：所有数字段之和。",
  "- 1 ≤ 长度 ≤ 100\n- 每段数字 ≤ 10⁶",
  lambda: cases("a12b3c", "abc", "123", "a1b2c3", "x100y", "9a9b9"),
  _digit_sum,
  r'''#include <cstdio>
int main() {
    char s[105];
    if (scanf("%104s", s) != 1) return 0;
    long long sum = 0, cur = 0;
    bool in = false;
    for (int i = 0; s[i]; i++) {
        if (s[i] >= '0' && s[i] <= '9') { cur = cur * 10 + (s[i] - '0'); in = true; }
        else if (in) { sum += cur; cur = 0; in = false; }
    }
    if (in) sum += cur;                // 结尾还在数字里
    printf("%lld\n", sum);
    return 0;
}
''',
  r'''#include <cstdio>
#include <cctype>
#include <cstdlib>
int main() {
    char s[105];
    if (scanf("%104s", s) != 1) return 0;
    long long sum = 0;
    char buf[16];
    int k = 0;
    for (int i = 0;; i++) {
        if (isdigit((unsigned char)s[i])) buf[k++] = s[i];
        else {
            if (k) { buf[k] = '\0'; sum += atoll(buf); k = 0; }
            if (!s[i]) break;          // 到串尾才真正结束
        }
    }
    printf("%lld\n", sum);
    return 0;
}
''',
  ["字符串", "数字提取"])

A("【字符串】最长连续相同字符段", SEC_STR, 2,
  stmt("读入一个不含空格的字符串，输出最长的一段连续相同字符的长度。",
       ["一遍扫描，`run` 记录当前段长，不同就重置为 1",
        "`best` 在每步后更新，别只在重置时才更新",
        "输出一个整数"]),
  "一行一个不含空格的字符串。",
  "一行：最长连续段长度。",
  "- 1 ≤ 长度 ≤ 100",
  lambda: cases("aabbbcc", "abc", "aaaa", "a", "abbbbc", "aabbccdd"),
  _longest_run,
  r'''#include <cstdio>
int main() {
    char s[105];
    if (scanf("%104s", s) != 1) return 0;
    int best = 1, run = 1;
    for (int i = 1; s[i]; i++) {
        run = (s[i] == s[i - 1]) ? run + 1 : 1;
        if (run > best) best = run;
    }
    printf("%d\n", best);
    return 0;
}
''',
  r'''#include <cstdio>
#include <cstring>
int main() {
    char s[105];
    if (scanf("%104s", s) != 1) return 0;
    int n = (int)strlen(s), best = 1;
    for (int i = 0; i < n;) {          // 按段跳
        int j = i;
        while (j < n && s[j] == s[i]) j++;
        if (j - i > best) best = j - i;
        i = j;
    }
    printf("%d\n", best);
    return 0;
}
''',
  ["字符串", "扫描"])

A("【字符串】统计元音字母个数", SEC_STR, 1,
  stmt("读入一个不含空格的字符串，统计其中元音字母 `a e i o u`（不区分大小写）的总个数。",
       ["先把字符统一转成小写再判断，或者判断两套字母",
        "`y` 不算元音",
        "输出一个整数"]),
  "一行一个不含空格的字符串。",
  "一行：元音个数。",
  "- 1 ≤ 长度 ≤ 100",
  lambda: cases("aeiou", "AEIOU", "xyz", "hello", "Programming", "aA"),
  _vowels,
  r'''#include <cstdio>
int main() {
    char s[105];
    if (scanf("%104s", s) != 1) return 0;
    int c = 0;
    for (int i = 0; s[i]; i++) {
        char ch = s[i];
        if (ch >= 'A' && ch <= 'Z') ch = char(ch - 'A' + 'a');   // 统一转小写
        if (ch == 'a' || ch == 'e' || ch == 'i' || ch == 'o' || ch == 'u') c++;
    }
    printf("%d\n", c);
    return 0;
}
''',
  r'''#include <cstdio>
#include <cstring>
int main() {
    char s[105];
    if (scanf("%104s", s) != 1) return 0;
    int c = 0;
    for (int i = 0; s[i]; i++) c += (strchr("aeiouAEIOU", s[i]) != nullptr);
    printf("%d\n", c);
    return 0;
}
''',
  ["字符串", "元音", "统计"])

A("【字符串】字符串左循环移位", SEC_STR, 2,
  stmt("读入一个不含空格的字符串和整数 `k`，把字符串循环左移 `k` 位（`k` 可能大于长度）。"
       "输出移位后的结果。",
       ["`k` 要先对长度取模，`k = 8`、长度 5 时等价于移 3 位",
        "左移 k 位的结果是 `s[k..n-1] + s[0..k-1]`",
        "输出一行"]),
  "第一行字符串（不含空格），第二行整数 `k`。",
  "一行：左移 `k` 位后的字符串。",
  "- 1 ≤ 长度 ≤ 100\n- 0 ≤ k ≤ 10⁹",
  lambda: cases("abcde\n2", "abcde\n0", "abcde\n5", "abcde\n7", "a\n1000000000", "abcd\n1"),
  _rotate_left,
  r'''#include <cstdio>
int main() {
    char s[105];
    long long k;
    if (scanf("%104s", s) != 1) return 0;
    if (scanf("%lld", &k) != 1) return 0;
    int n = 0;
    while (s[n]) n++;
    k %= n;                            // k 可能比长度大得多
    for (int i = 0; i < n; i++) putchar(s[(int)((i + k) % n)]);
    printf("\n");
    return 0;
}
''',
  r'''#include <cstdio>
#include <cstring>
#include <algorithm>
int main() {
    char s[105];
    long long k;
    if (scanf("%104s", s) != 1) return 0;
    if (scanf("%lld", &k) != 1) return 0;
    int n = (int)strlen(s);
    k %= n;
    std::rotate(s, s + k, s + n);      // 三次反转的封装
    printf("%s\n", s);
    return 0;
}
''',
  ["字符串", "循环移位", "rotate"])

A("【字符串】判断变位词", SEC_STR, 3,
  stmt("两个字符串由相同字母重排得到（长度相同、每个字母出现次数相同）称为变位词。"
       "读入两行不含空格的字符串，是变位词输出 `YES`，否则输出 `NO`。",
       ["统计 26 个字母的频次数组，逐位比较",
        "也可以两串各自排序后比较",
        "只输出 `YES` 或 `NO`"]),
  "两行，各一个不含空格的小写字符串。",
  "一行：`YES` 或 `NO`。",
  "- 每行长度 ≤ 100\n- 只含小写字母",
  lambda: cases("listen\nsilent", "abc\nabd", "a\na", "abc\ncba", "aab\nabb", "hello\nworld"),
  _anagram,
  r'''#include <cstdio>
int main() {
    char a[105], b[105];
    if (scanf("%104s", a) != 1) return 0;
    if (scanf("%104s", b) != 1) return 0;
    int ca[26] = {0}, cb[26] = {0};
    for (int i = 0; a[i]; i++) ca[a[i] - 'a']++;
    for (int i = 0; b[i]; i++) cb[b[i] - 'a']++;
    bool ok = true;
    for (int i = 0; i < 26; i++) if (ca[i] != cb[i]) ok = false;
    printf("%s\n", ok ? "YES" : "NO");
    return 0;
}
''',
  r'''#include <cstdio>
#include <cstring>
#include <algorithm>
int main() {
    char a[105], b[105];
    if (scanf("%104s", a) != 1) return 0;
    if (scanf("%104s", b) != 1) return 0;
    if (strlen(a) != strlen(b)) { printf("NO\n"); return 0; }
    std::sort(a, a + strlen(a));       // 各自排序后比较
    std::sort(b, b + strlen(b));
    printf("%s\n", strcmp(a, b) == 0 ? "YES" : "NO");
    return 0;
}
''',
  ["字符串", "变位词", "频次"])

A("【字符串】去掉重复字符保序", SEC_STR, 3,
  stmt("读入一个不含空格的字符串，去掉重复出现的字符，只保留**第一次**出现的位置，"
       "输出结果。",
       ["用一个 `bool seen[256]` 记录字符是否出现过",
        "扫描时按原顺序决定是否输出，天然保持顺序",
        "输出一行"]),
  "一行一个不含空格的字符串。",
  "一行：去重后的字符串。",
  "- 1 ≤ 长度 ≤ 100",
  lambda: cases("abacb", "aaaa", "abc", "abcdefga", "aAbB", "hello"),
  _dedup,
  r'''#include <cstdio>
int main() {
    char s[105];
    if (scanf("%104s", s) != 1) return 0;
    bool seen[256] = {false};
    int k = 0;
    for (int i = 0; s[i]; i++) {
        unsigned char c = (unsigned char)s[i];
        if (!seen[c]) { seen[c] = true; s[k++] = s[i]; }   // 第一次出现才留
    }
    s[k] = '\0';
    printf("%s\n", s);
    return 0;
}
''',
  r'''#include <cstdio>
#include <iostream>
#include <string>
#include <set>
int main() {
    std::string s, out;
    if (!(std::cin >> s)) return 0;
    std::set<char> seen;
    for (char c : s) if (seen.insert(c).second) out += c;   // insert 返回是否新插入
    printf("%s\n", out.c_str());
    return 0;
}
''',
  ["字符串", "去重", "set"])

A("【字符串】统计回文子串个数", SEC_STR, 4,
  stmt("读入一个不含空格的字符串（只含小写字母），统计长度 **≥ 2** 的回文子串个数。"
       "不同起止位置算不同子串，内容相同也算多个。",
       ["枚举所有起点和终点，判回文，`n ≤ 100` 时 O(n³) 也能过",
        "更快的做法是中心扩展，但先把暴力写对更重要",
        "长度 1 的子串不算"]),
  "一行一个只含小写字母的字符串。",
  "一行：回文子串个数。",
  "- 1 ≤ 长度 ≤ 100",
  lambda: cases("aaa", "abba", "abc", "a", "aaaa", "abab"),
  _pal_sub,
  r'''#include <cstdio>
int main() {
    char s[105];
    if (scanf("%104s", s) != 1) return 0;
    int n = 0;
    while (s[n]) n++;
    int c = 0;
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++) {          // 长度 >= 2
            int l = i, r = j;
            bool ok = true;
            while (l < r) { if (s[l] != s[r]) { ok = false; break; } l++; r--; }
            if (ok) c++;
        }
    printf("%d\n", c);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    char s[105];
    if (scanf("%104s", s) != 1) return 0;
    int n = 0;
    while (s[n]) n++;
    int c = 0;
    for (int center = 0; center < 2 * n - 1; center++) {   // 中心扩展
        int l = center / 2, r = l + center % 2;
        while (l >= 0 && r < n && s[l] == s[r]) {
            if (r - l + 1 >= 2) c++;
            l--; r++;
        }
    }
    printf("%d\n", c);
    return 0;
}
''',
  ["字符串", "回文子串", "中心扩展"])


if __name__ == "__main__":
    sys.exit(cli(PROBLEMS, "app/problems_bank_cpp_basic5.py",
                 "第 5 册：指针与引用 / 字符数组与字符串", "CPP_BASIC5_PROBLEMS"))
