# -*- coding: utf-8 -*-
"""C++ 基础编程题 · 第 4 册：函数与参数传递（20）+ 递归与递推（20）= 40 题。

对应教材第 03 讲「函数」（p64~97）。这一册专练「调用约定」：
值传递为什么不改变实参、引用为什么能、数组参数为什么退化成指针、
递归的边界写在开头还是结尾、递推的方向是「从小到大」还是「从大到小」。

★ oracle 一律是独立的 Python 实现（暴力枚举 / 直接模拟），绝不复用 C++ 解的结果。
★ 每题的 alt 都换一条实现路径（递归↔迭代、手写↔库函数、数组参数↔指针参数）。

重生成：python tools/gen_cpp_basic4.py
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cpp_basic_kit import cases, cli, stmt          # noqa: E402

SEC_FN = "C++ 编程 · 函数与参数传递"
SEC_RC = "C++ 编程 · 递归与递推"

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
    """两行：n，然后 n 个数。"""
    v = rints(seed, n, lo, hi)
    return "%d\n%s\n" % (n, " ".join(str(x) for x in v))


def toks(t: str) -> list[int]:
    return [int(x) for x in t.split()]


# ===================================================================== #
#  SEC_FN · 函数与参数传递（20 题）
# ===================================================================== #

A("【函数】引用传参交换两个数", SEC_FN, 1,
  stmt("写一个交换函数，用**引用参数** `void mySwap(int &a, int &b)` 交换两个整数。"
       "读入两个整数，输出交换后的结果。",
       ["值传递 `void mySwap(int a, int b)` 交换的是副本，实参一点没变 —— 这是本章第一个坑",
        "引用参数在函数体内就是实参本身，`a` 和 `b` 只是它的别名",
        "输出一行，两个整数用空格分隔"]),
  "一行两个整数 `a b`。",
  "一行：交换后的 `a b`。",
  "- |a|, |b| ≤ 10⁹",
  lambda: cases("3 5", "-1 8", "0 0", "100 -100", "7 7", "123456789 987654321"),
  lambda t: "%d %d\n" % tuple(reversed(toks(t))),
  r'''#include <cstdio>
void mySwap(int &a, int &b) {        // 引用参数：a、b 就是实参的别名
    int t = a; a = b; b = t;
}
int main() {
    int x, y;
    if (scanf("%d %d", &x, &y) != 2) return 0;
    mySwap(x, y);
    printf("%d %d\n", x, y);
    return 0;
}
''',
  r'''#include <cstdio>
#include <utility>
int main() {
    int x, y;
    if (scanf("%d %d", &x, &y) != 2) return 0;
    std::swap(x, y);                 // 标准库版本，内部同样是引用
    printf("%d %d\n", x, y);
    return 0;
}
''',
  ["函数", "引用", "参数传递"])

A("【函数】值传递与引用传递的差别", SEC_FN, 1,
  stmt("有两个函数：`void addByValue(int x) { x += 1; }` 与 "
       "`void addByRef(int &x) { x += 1; }`。\n\n"
       "读入一个整数 `a`，先调用 `addByValue(a)` 并输出 `a`，"
       "再调用 `addByRef(a)` 并输出 `a`。",
       ["值传递里函数内加的是副本，回到 main 后 `a` 没变",
        "引用传递改的就是 `a` 本身",
        "两行输出，第一行是值传递之后的值，第二行是引用传递之后的值"]),
  "一行一个整数 `a`。",
  "两行：值传递后的 `a`、引用传递后的 `a`。",
  "- |a| ≤ 10⁹",
  lambda: cases("5", "-1", "0", "1000000000", "-1000000000", "7"),
  lambda t: "%d\n%d\n" % (lambda a: (a, a + 1))(int(t.strip())),
  r'''#include <cstdio>
void addByValue(int x) { x += 1; }
void addByRef(int &x)   { x += 1; }
int main() {
    int a;
    if (scanf("%d", &a) != 1) return 0;
    addByValue(a);
    printf("%d\n", a);
    addByRef(a);
    printf("%d\n", a);
    return 0;
}
''',
  r'''#include <cstdio>
void addByValue(int x) { x += 1; }
void addByPtr(int *x)  { *x += 1; }   // 指针出参，效果等同引用
int main() {
    int a;
    if (scanf("%d", &a) != 1) return 0;
    addByValue(a);
    printf("%d\n", a);
    addByPtr(&a);
    printf("%d\n", a);
    return 0;
}
''',
  ["函数", "值传递", "引用"])

A("【函数】数组传参求最大值与最小值", SEC_FN, 1,
  stmt("写一个函数接收数组和长度，一趟扫描同时求出最大值与最小值。"
       "读入 `n` 和 `n` 个整数，输出最大值与最小值。",
       ["数组作参数会**退化成一个指针**，函数里 `sizeof(a)` 拿不到数组长度，长度必须另传",
        "最大值初值不能写 0 —— 全是负数时 0 就成了「最大值」",
        "输出一行，先最大值后最小值"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：`max min`。",
  "- 1 ≤ n ≤ 100\n- |x| ≤ 10⁶",
  lambda: cases(barr(11, 5), barr(12, 1), barr(13, 20), barr(14, 100, -1000, 1000),
                barr(15, 7), barr(16, 33)),
  lambda t: "%d %d\n" % (lambda v: (max(v), min(v)))(toks(t)[1:]),
  r'''#include <cstdio>
void stat(const int a[], int n, int &mx, int &mn) {   // 数组参数 + 两个引用出参
    mx = mn = a[0];
    for (int i = 1; i < n; i++) {
        if (a[i] > mx) mx = a[i];
        if (a[i] < mn) mn = a[i];
    }
}
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    int a[105];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int mx, mn;
    stat(a, n, mx, mn);
    printf("%d %d\n", mx, mn);
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    int a[105];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int *mx = std::max_element(a, a + n);   // 指针区间：a 已经退化为 int*
    int *mn = std::min_element(a, a + n);
    printf("%d %d\n", *mx, *mn);
    return 0;
}
''',
  ["函数", "数组参数", "引用"])

A("【函数】默认参数求和", SEC_FN, 2,
  stmt("定义 `int addUp(int a, int b = 10, int c = 0)`。读入三个整数 `a b c`，"
       "依次输出 `addUp(a)`、`addUp(a, b)`、`addUp(a, b, c)` 三个调用的结果。",
       ["默认参数必须**从右往左**连续给，写成 `int addUp(int a = 1, int b)` 是编译错误",
        "三行输出，依次是省两个、省一个、一个都不省的结果",
        "`addUp(a)` 展开后是 `a + 10 + 0`"]),
  "一行三个整数 `a b c`。",
  "三行：`addUp(a)`、`addUp(a,b)`、`addUp(a,b,c)`。",
  "- |a|, |b|, |c| ≤ 10⁶",
  lambda: cases("1 2 3", "0 0 0", "-5 5 -5", "100 200 300", "7 -7 7", "12 34 56"),
  lambda t: "%d\n%d\n%d\n" % (lambda a, b, c: (a + 10, a + b, a + b + c))(*toks(t)),
  r'''#include <cstdio>
int addUp(int a, int b = 10, int c = 0) { return a + b + c; }
int main() {
    int a, b, c;
    if (scanf("%d %d %d", &a, &b, &c) != 3) return 0;
    printf("%d\n", addUp(a));
    printf("%d\n", addUp(a, b));
    printf("%d\n", addUp(a, b, c));
    return 0;
}
''',
  r'''#include <cstdio>
int addUp(int a, int b = 10, int c = 0) { return a + b + c; }
int main() {
    int v[3] = {0, 10, 0};             // 缺省的实参保存在数组里，再一次性传齐
    if (scanf("%d %d %d", &v[0], &v[1], &v[2]) != 3) return 0;
    int keep = v[1];
    v[1] = 10;
    printf("%d\n", addUp(v[0], v[1], 0));       // 等价于 addUp(a)
    v[1] = keep;
    printf("%d\n", addUp(v[0], v[1], 0));       // 等价于 addUp(a, b)
    printf("%d\n", addUp(v[0], v[1], v[2]));
    return 0;
}
''',
  ["函数", "默认参数"])

A("【函数】函数重载实现两数相加", SEC_FN, 2,
  stmt("用**函数重载**实现两个数相加：整数版本返回 `int`，小数版本返回 `double`。\n\n"
       "输入第一行是类型标记 `i` 或 `d`，第二行是两个数。整数版输出和本身，"
       "小数版输出和并保留两位小数。",
       ["重载靠**参数类型**区分，不能靠返回值类型区分",
        "`i` 分支用 `scanf(\"%d\")`，`d` 分支必须用 `%lf`，混用会读成 0",
        "小数输出用 `%.2f`"]),
  "第一行 `i` 或 `d`；第二行两个数（`i` 时是整数，`d` 时最多两位小数）。",
  "一行：和（`d` 时保留两位小数）。",
  "- |整数| ≤ 10⁹\n- |小数| ≤ 10⁶，小数位数 ≤ 2",
  lambda: cases("i\n3 5", "d\n1.5 2.25", "i\n-7 7", "d\n0.1 0.2",
                "i\n1000000 2000000", "d\n-3.75 1.25"),
  lambda t: (lambda ln: ("%d\n" % (int(ln[1].split()[0]) + int(ln[1].split()[1]))
                         if ln[0] == "i" else
                         "%.2f\n" % (float(ln[1].split()[0]) + float(ln[1].split()[1]))))(
      [x.strip() for x in t.strip().splitlines()]),
  r'''#include <cstdio>
int    addUp(int a, int b)       { return a + b; }        // 整型重载
double addUp(double a, double b) { return a + b; }        // 浮点重载
int main() {
    char t[4] = {0};
    if (scanf("%3s", t) != 1) return 0;
    if (t[0] == 'i') {
        int a, b;
        scanf("%d %d", &a, &b);
        printf("%d\n", addUp(a, b));
    } else {
        double a, b;
        scanf("%lf %lf", &a, &b);
        printf("%.2f\n", addUp(a, b));
    }
    return 0;
}
''',
  r'''#include <cstdio>
#include <iostream>
#include <iomanip>
template <typename T> T addUp(T a, T b) { return a + b; }  // 模板替代重载
int main() {
    char t;
    if (!(std::cin >> t)) return 0;
    if (t == 'i') {
        int a, b; std::cin >> a >> b;
        std::cout << addUp(a, b) << "\n";
    } else {
        double a, b; std::cin >> a >> b;
        std::cout << std::fixed << std::setprecision(2) << addUp(a, b) << "\n";
    }
    return 0;
}
''',
  ["函数", "重载", "模板"])

A("【函数】判断素数的函数", SEC_FN, 2,
  stmt("写一个 `bool isPrime(int x)`，读入 `n` 和 `n` 个整数，输出其中素数的个数。",
       ["1 不是素数，2 是素数 —— 这两个边界最容易写错",
        "试除只需要到 `i * i <= x`，写成 `i < x` 在大数上会超时",
        "输出一个整数"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：素数个数。",
  "- 1 ≤ n ≤ 1000\n- 0 ≤ x ≤ 10⁶",
  lambda: cases(barr(21, 6, 1, 20), "1\n1", "1\n2", barr(22, 50, 1, 100),
                barr(23, 100, 1, 10000), barr(24, 30, 0, 3)),
  lambda t: "%d\n" % sum(1 for x in toks(t)[1:]
                         if x >= 2 and all(x % d for d in range(2, int(x ** 0.5) + 1))),
  r'''#include <cstdio>
bool isPrime(int x) {
    if (x < 2) return false;
    for (long long i = 2; i * i <= x; i++)      // i*i 防溢出，别写 i < x
        if (x % i == 0) return false;
    return true;
}
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int c = 0;
    for (int i = 0; i < n; i++) { int x; scanf("%d", &x); if (isPrime(x)) c++; }
    printf("%d\n", c);
    return 0;
}
''',
  r'''#include <cstdio>
bool isPrime(int x) {
    if (x < 2) return false;
    if (x % 2 == 0) return x == 2;              // 先摘掉偶数，再 6k±1 试除
    for (long long i = 3; i * i <= x; i += 2)
        if (x % i == 0) return false;
    return true;
}
int main() {
    int n, c = 0, x;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) { scanf("%d", &x); c += isPrime(x) ? 1 : 0; }
    printf("%d\n", c);
    return 0;
}
''',
  ["函数", "素数", "试除"])

A("【函数】long long 阶乘函数", SEC_FN, 1,
  stmt("写函数 `long long fact(int n)` 求 `n!`，读入 `n`（1 ≤ n ≤ 20），输出 `n!`。",
       ["13! = 6227020800 已经超 `int`（上限约 2.1×10⁹），所以返回值必须是 `long long`",
        "`printf` 用 `%lld`，写成 `%d` 会打印出乱数",
        "20! 也在 `long long` 范围内（约 2.4×10¹⁸）"]),
  "一行一个整数 `n`。",
  "一行：`n!`。",
  "- 1 ≤ n ≤ 20",
  lambda: cases("1", "5", "10", "13", "20", "17"),
  lambda t: "%d\n" % (lambda n: __import__("math").factorial(n))(int(t.strip())),
  r'''#include <cstdio>
long long fact(int n) {                // 返回值必须是 long long
    if (n <= 1) return 1;
    return (long long)n * fact(n - 1);
}
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    printf("%lld\n", fact(n));
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    long long r = 1;
    for (int i = 2; i <= n; i++) r *= i;   // 迭代版
    printf("%lld\n", r);
    return 0;
}
''',
  ["函数", "阶乘", "long long"])

A("【函数】static 局部变量记调用次数", SEC_FN, 2,
  stmt("函数 `int nextId() { static int id = 0; return ++id; }` 每次调用返回自增序号。\n\n"
       "读入 `m`，表示连续调用 `m` 次。输出两行：最后一次的返回值、所有返回值之和。",
       ["`static` 局部变量只在第一次调用时初始化，之后跨调用保留",
        "去掉 `static` 的话每次都是 1 —— 正好可以用来验证",
        "第二行用 `long long`（m 到 10⁵ 时和到 5×10⁹）"]),
  "一行一个整数 `m`。",
  "两行：最后一次返回值、所有返回值之和。",
  "- 1 ≤ m ≤ 100000",
  lambda: cases("1", "5", "10", "100", "999", "100000"),
  lambda t: "%d\n%d\n" % (lambda m: (m, m * (m + 1) // 2))(int(t.strip())),
  r'''#include <cstdio>
int nextId() {
    static int id = 0;      // 只初始化一次，之后跨调用保留
    return ++id;
}
int main() {
    int m, last = 0;
    long long s = 0;
    if (scanf("%d", &m) != 1) return 0;
    for (int i = 0; i < m; i++) { last = nextId(); s += last; }
    printf("%d\n%lld\n", last, s);
    return 0;
}
''',
  r'''#include <cstdio>
struct Counter {                       // 用成员变量模拟 static 局部变量
    int id = 0;
    int next() { return ++id; }
};
int main() {
    int m, last = 0;
    long long s = 0;
    Counter c;
    if (scanf("%d", &m) != 1) return 0;
    for (int i = 0; i < m; i++) { last = c.next(); s += last; }
    printf("%d\n%lld\n", last, s);
    return 0;
}
''',
  ["函数", "static", "作用域"])

A("【函数】全局变量被局部变量遮蔽", SEC_FN, 2,
  stmt("程序里有全局变量 `int g = 100;`，函数写成 `int shadow(int g) { g += 1; return g; }`。\n\n"
       "读入 `a`，输出两行：`shadow(a)` 的返回值、函数调用后全局 `g` 的值。",
       ["函数参数名与全局变量同名时，函数内**只有参数可见**，这叫名字遮蔽",
        "函数里改的是参数副本，全局 `g` 纹丝不动",
        "想在函数里用全局变量得写 `::g`"]),
  "一行一个整数 `a`。",
  "两行：函数返回值、全局 `g`。",
  "- |a| ≤ 10⁹",
  lambda: cases("5", "-1", "0", "100", "-100", "999"),
  lambda t: "%d\n100\n" % (int(t.strip()) + 1),
  r'''#include <cstdio>
int g = 100;
int shadow(int g) {         // 形参遮蔽了全局 g
    g += 1;
    return g;
}
int main() {
    int a;
    if (scanf("%d", &a) != 1) return 0;
    printf("%d\n", shadow(a));
    printf("%d\n", g);
    return 0;
}
''',
  r'''#include <cstdio>
int g = 100;
int shadow(int x) {
    g += 0;                 // 只读全局，不遮蔽
    return x + 1;
}
int main() {
    int a;
    if (scanf("%d", &a) != 1) return 0;
    printf("%d\n", shadow(a));
    printf("%d\n", ::g);    // 显式全局作用域
    return 0;
}
''',
  ["函数", "全局变量", "作用域"])

A("【函数】引用出参返回和与最大值", SEC_FN, 2,
  stmt("写函数 `void stat(const int a[], int n, long long &sum, int &mx)`，"
       "一次遍历同时带出总和与最大值。读入 `n` 和 `n` 个整数，输出 `sum` 与 `mx`。",
       ["一个函数想返回两个值，最常用的办法就是引用出参",
        "`const int a[]` 里的 `const` 是承诺「不改数组」，调用方可以传只读数据",
        "和要用 `long long`：100 个 10⁶ 累加就是 10⁸，接近 `int` 的安全边界"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：`sum max`。",
  "- 1 ≤ n ≤ 10⁵\n- |x| ≤ 10⁶",
  lambda: cases(barr(31, 5), barr(32, 1), barr(33, 20), barr(34, 200, -1000, 1000),
                barr(35, 7), barr(36, 333)),
  lambda t: "%d %d\n" % (lambda v: (sum(v), max(v)))(toks(t)[1:]),
  r'''#include <cstdio>
void stat(const int a[], int n, long long &sum, int &mx) {
    sum = 0;
    mx = a[0];
    for (int i = 0; i < n; i++) {
        sum += a[i];
        if (a[i] > mx) mx = a[i];
    }
}
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    int a[100005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    long long sum; int mx;
    stat(a, n, sum, mx);
    printf("%lld %d\n", sum, mx);
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
struct Result { long long sum; int mx; };        // 用结构体打包两个结果
Result stat(const int *a, int n) {
    Result r{0, a[0]};
    for (int i = 0; i < n; i++) { r.sum += a[i]; r.mx = std::max(r.mx, a[i]); }
    return r;
}
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[100005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    Result r = stat(a, n);
    printf("%lld %d\n", r.sum, r.mx);
    return 0;
}
''',
  ["函数", "引用", "出参"])

A("【函数】递归求幂与迭代求幂", SEC_FN, 2,
  stmt("分别用递归和迭代写 `a^n`，输入 `a n`，输出 `a` 的 `n` 次方。",
       ["`n = 0` 时结果恒为 1，包括 `a = 0` 的情况（按幂运算惯例 0⁰ 记作 1）",
        "连乘用 `long long`，`a` 到 10、`n` 到 18 时结果已经到 10¹⁸ 量级",
        "递归版别忘边界 `n == 0`，否则无限递归爆栈"]),
  "一行两个整数 `a n`。",
  "一行：`a` 的 `n` 次方。",
  "- |a| ≤ 10\n- 0 ≤ n ≤ 18",
  lambda: cases("2 10", "0 0", "-2 3", "10 18", "1 18", "-1 17"),
  lambda t: "%d\n" % (lambda a, n: a ** n)(*toks(t)),
  r'''#include <cstdio>
long long power(long long a, int n) {
    if (n == 0) return 1;                 // 边界写在最前
    return a * power(a, n - 1);
}
int main() {
    long long a; int n;
    if (scanf("%lld %d", &a, &n) != 2) return 0;
    printf("%lld\n", power(a, n));
    return 0;
}
''',
  r'''#include <cstdio>
long long power(long long a, int n) {
    long long r = 1;                      // 迭代 + 快速幂
    while (n > 0) {
        if (n & 1) r *= a;
        a *= a;
        n >>= 1;
    }
    return r;
}
int main() {
    long long a; int n;
    if (scanf("%lld %d", &a, &n) != 2) return 0;
    printf("%lld\n", power(a, n));
    return 0;
}
''',
  ["函数", "递归", "快速幂"])

A("【函数】函数封装区间求和", SEC_FN, 2,
  stmt("把「求数组一段区间和」封装成函数（用前缀和，单次询问 O(1)）。\n\n"
       "读入 `n` 和 `q`，第二行 `n` 个整数，之后 `q` 行每行两个整数 `l r`（下标从 1 开始），"
       "对每个询问输出 `a[l] + … + a[r]`。",
       ["前缀和 `pre[i] = pre[i-1] + a[i]`，区间和是 `pre[r] - pre[l-1]`",
        "`pre[0]` 必须是 0，否则 `l = 1` 时会减到数组外",
        "每个询问输出一行"]),
  "第一行 `n q`；第二行 `n` 个整数；之后 `q` 行，每行 `l r`。",
  "`q` 行，每行一个区间和。",
  "- 1 ≤ n ≤ 10⁵\n- 1 ≤ q ≤ 10⁵\n- 1 ≤ l ≤ r ≤ n\n- |a[i]| ≤ 10⁶",
  lambda: cases(
      "5 3\n3 -1 4 -1 5\n1 3\n2 5\n1 5",
      "1 1\n-7\n1 1",
      "6 2\n1 2 3 4 5 6\n1 6\n3 4",
      "%d %d\n%s\n%s" % (10, 4, " ".join(str(x) for x in rints(41, 10)),
                         "\n".join(["1 10", "2 9", "3 3", "5 7"])),
      "%d %d\n%s\n%s" % (20, 3, " ".join(str(x) for x in rints(42, 20, -100, 100)),
                         "\n".join(["1 20", "4 14", "10 11"])),
      "%d %d\n%s\n%s" % (8, 5, " ".join(str(x) for x in rints(43, 8, -1000, 1000)),
                         "\n".join(["1 1", "2 2", "1 8", "3 6", "7 8"]))),
  lambda t: (lambda tok: (lambda n, q, a: (lambda pre: "".join(
      "%d\n" % (pre[int(tok[2 + n + 2 * i + 1])] - pre[int(tok[2 + n + 2 * i]) - 1])
      for i in range(q)))([0] + [sum(a[:k + 1]) for k in range(n)]))(
      int(tok[0]), int(tok[1]), [int(x) for x in tok[2:2 + int(tok[0])]]))(t.split()),
  r'''#include <cstdio>
long long rangeSum(const long long pre[], int l, int r) {
    return pre[r] - pre[l - 1];
}
int main() {
    int n, q;
    if (scanf("%d %d", &n, &q) != 2) return 0;
    static long long pre[100005];
    pre[0] = 0;                            // 哨兵，保证 l=1 时能减
    for (int i = 1; i <= n; i++) {
        long long x; scanf("%lld", &x);
        pre[i] = pre[i - 1] + x;
    }
    while (q--) {
        int l, r; scanf("%d %d", &l, &r);
        printf("%lld\n", rangeSum(pre, l, r));
    }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n, q;
    if (scanf("%d %d", &n, &q) != 2) return 0;
    long long *pre = new long long[n + 1];  // 动态数组版
    pre[0] = 0;
    for (int i = 1; i <= n; i++) {
        long long x; scanf("%lld", &x);
        pre[i] = pre[i - 1] + x;
    }
    for (int k = 0; k < q; k++) {
        int l, r; scanf("%d %d", &l, &r);
        printf("%lld\n", pre[r] - pre[l - 1]);
    }
    delete[] pre;
    return 0;
}
''',
  ["函数", "前缀和", "区间求和"])

A("【函数】多函数协作求最大公约数与最小公倍数", SEC_FN, 2,
  stmt("写两个函数：`gcd` 求最大公约数，`lcm` 在内部调用 `gcd` 求最小公倍数。"
       "读入 `a b`，输出 `gcd(a,b)` 与 `lcm(a,b)`。",
       ["`lcm = a / gcd * b`，先除后乘能少溢出一次",
        "`a`、`b` 到 10⁹ 时 lcm 能到 10¹⁸ 量级，两个量都用 `long long`",
        "输出一行，先 gcd 后 lcm"]),
  "一行两个正整数 `a b`。",
  "一行：`gcd lcm`。",
  "- 1 ≤ a, b ≤ 10⁹",
  lambda: cases("12 18", "1 1", "7 13", "1000000000 999999937",
                "270 192", "36 48"),
  lambda t: "%d %d\n" % (lambda a, b: (__import__("math").gcd(a, b),
                                       a // __import__("math").gcd(a, b) * b))(*toks(t)),
  r'''#include <cstdio>
long long gcd(long long a, long long b) {
    while (b) { long long t = a % b; a = b; b = t; }
    return a;
}
long long lcm(long long a, long long b) {      // 内部复用 gcd
    return a / gcd(a, b) * b;                  // 先除后乘
}
int main() {
    long long a, b;
    if (scanf("%lld %lld", &a, &b) != 2) return 0;
    printf("%lld %lld\n", gcd(a, b), lcm(a, b));
    return 0;
}
''',
  r'''#include <cstdio>
long long gcd(long long a, long long b) {
    return b == 0 ? a : gcd(b, a % b);         // 递归版
}
int main() {
    long long a, b;
    if (scanf("%lld %lld", &a, &b) != 2) return 0;
    long long g = gcd(a, b);
    printf("%lld %lld\n", g, a / g * b);
    return 0;
}
''',
  ["函数", "gcd", "lcm"])

A("【函数】函数内修改数组（传地址）", SEC_FN, 2,
  stmt("写函数把数组里所有负数改成它的绝对值。读入 `n` 和 `n` 个整数，输出修改后的数组。",
       ["数组参数传的是地址，函数内的修改会反映到调用方 —— 这和传 `int` 完全不同",
        "想保护原数组就加 `const`，加了还改会直接编译报错",
        "输出一行，数字之间一个空格"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：修改后的数组。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases(barr(51, 5), "3\n-1 -2 -3", "1\n0", barr(52, 20),
                barr(53, 50, -1000, 1000), barr(54, 8, -9, -1)),
  lambda t: " ".join(str(abs(x)) for x in toks(t)[1:]) + "\n",
  r'''#include <cstdio>
void absAll(int a[], int n) {          // 形参是 int*，改的是原数组
    for (int i = 0; i < n; i++)
        if (a[i] < 0) a[i] = -a[i];
}
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    absAll(a, n);
    for (int i = 0; i < n; i++) printf("%d%c", a[i], i + 1 == n ? '\n' : ' ');
    return 0;
}
''',
  r'''#include <cstdio>
void absAll(int *p, int n) {           // 显式写指针
    for (int *q = p; q < p + n; ++q)
        if (*q < 0) *q = -*q;
}
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    absAll(a, n);
    for (int i = 0; i < n; i++) printf("%d%c", a[i], i + 1 == n ? '\n' : ' ');
    return 0;
}
''',
  ["函数", "数组参数", "指针"])

A("【函数】谓词函数筛选计数（回文数）", SEC_FN, 3,
  stmt("写谓词函数 `bool isPal(int x)` 判断一个数是不是回文数（正读倒读相同），"
       "读入 `n` 和 `n` 个**正整数**，输出其中回文数的个数。",
       ["按十进制位判断，别转成字符串也行：把数反转过来看是否相等",
        "末尾是 0 的数（如 120）一定不是回文数（除非它本身是 0），反转后前导零丢了",
        "输出一个整数"]),
  "第一行 `n`，第二行 `n` 个正整数。",
  "一行：回文数个数。",
  "- 1 ≤ n ≤ 1000\n- 1 ≤ x ≤ 10⁹",
  lambda: cases("5\n121 123 1221 10 7", "1\n1", barr(61, 20, 1, 100),
                barr(62, 50, 1, 1000), "6\n100001 12321 9999 11 100 9",
                barr(63, 30, 900, 1100)),
  lambda t: "%d\n" % sum(1 for x in toks(t)[1:] if str(x) == str(x)[::-1]),
  r'''#include <cstdio>
bool isPal(int x) {
    int y = x, r = 0;                  // 反转这个数
    while (y > 0) { r = r * 10 + y % 10; y /= 10; }
    return r == x;
}
int main() {
    int n, c = 0, x;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) { scanf("%d", &x); if (isPal(x)) c++; }
    printf("%d\n", c);
    return 0;
}
''',
  r'''#include <cstdio>
#include <cstring>
bool isPal(int x) {                    // 转成字符数组两头夹
    char s[16];
    int len = snprintf(s, sizeof(s), "%d", x);
    for (int i = 0, j = len - 1; i < j; i++, j--)
        if (s[i] != s[j]) return false;
    return true;
}
int main() {
    int n, c = 0, x;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) { scanf("%d", &x); c += isPal(x) ? 1 : 0; }
    printf("%d\n", c);
    return 0;
}
''',
  ["函数", "谓词", "回文数"])

A("【函数】复合函数 f(g(x))", SEC_FN, 2,
  stmt("定义 `int f(int x) { return 2 * x + 1; }`、`int g(int x) { return x * x - 3; }`。"
       "读入 `x`，输出 `g(f(g(x)))`。",
       ["从最里面往外算：先 `g(x)`，再 `f(...)`，再 `g(...)`",
        "函数调用可以嵌套，`g(f(g(x)))` 是合法表达式",
        "|x| ≤ 100 时结果仍在 `int` 范围内"]),
  "一行一个整数 `x`。",
  "一行：`g(f(g(x)))`。",
  "- |x| ≤ 100",
  lambda: cases("2", "0", "-3", "10", "-10", "7"),
  lambda t: "%d\n" % (lambda x: ((2 * (x * x - 3) + 1) ** 2 - 3))(int(t.strip())),
  r'''#include <cstdio>
int f(int x) { return 2 * x + 1; }
int g(int x) { return x * x - 3; }
int main() {
    int x;
    if (scanf("%d", &x) != 1) return 0;
    int t = g(x);          // 先算最里层
    t = f(t);
    t = g(t);
    printf("%d\n", t);
    return 0;
}
''',
  r'''#include <cstdio>
int f(int x) { return 2 * x + 1; }
int g(int x) { return x * x - 3; }
int main() {
    int x;
    if (scanf("%d", &x) != 1) return 0;
    printf("%d\n", g(f(g(x))));    // 嵌套调用一次写完
    return 0;
}
''',
  ["函数", "复合函数", "嵌套调用"])

A("【函数】bool 函数统计闰年", SEC_FN, 2,
  stmt("写 `bool isLeap(int y)`：能被 4 整除且不能被 100 整除，或者能被 400 整除的是闰年。"
       "读入 `y1 y2`，输出区间 `[y1, y2]` 内闰年的个数。",
       ["条件顺序：`y % 4 == 0 && y % 100 != 0 || y % 400 == 0`，`&&` 优先于 `||`",
        "1900 不是闰年（被 100 整除但不被 400 整除），2000 是闰年",
        "输出一个整数"]),
  "一行两个整数 `y1 y2`（`y1 ≤ y2`）。",
  "一行：区间内闰年个数。",
  "- 1 ≤ y1 ≤ y2 ≤ 9999",
  lambda: cases("1900 2000", "2000 2000", "1900 1900", "1 4", "1990 2020", "2001 2099"),
  lambda t: "%d\n" % (lambda a, b: sum(1 for y in range(a, b + 1)
                                       if (y % 4 == 0 and y % 100 != 0) or y % 400 == 0))(*toks(t)),
  r'''#include <cstdio>
bool isLeap(int y) {
    return (y % 4 == 0 && y % 100 != 0) || (y % 400 == 0);
}
int main() {
    int a, b, c = 0;
    if (scanf("%d %d", &a, &b) != 2) return 0;
    for (int y = a; y <= b; y++) if (isLeap(y)) c++;
    printf("%d\n", c);
    return 0;
}
''',
  r'''#include <cstdio>
bool isLeap(int y) {
    if (y % 400 == 0) return true;
    if (y % 100 == 0) return false;
    return y % 4 == 0;
}
int main() {
    int a, b;
    if (scanf("%d %d", &a, &b) != 2) return 0;
    int c = 0;
    for (int y = a; y <= b; y++) c += isLeap(y);
    printf("%d\n", c);
    return 0;
}
''',
  ["函数", "bool", "闰年"])

A("【函数】内联函数求平方和", SEC_FN, 1,
  stmt("写 `inline long long sq(long long x) { return x * x; }`，读入 `n`，输出 1² + 2² + … + n²。",
       ["`inline` 只是给编译器的建议，`-O2` 下这种小函数本来就会被内联",
        "`x * x` 里 `x` 必须是 `long long`，`int` 到 46341 就会溢出",
        "n 到 10⁶ 时结果约 3.3×10¹⁷，`long long` 装得下"]),
  "一行一个整数 `n`。",
  "一行：平方和。",
  "- 1 ≤ n ≤ 10⁶",
  lambda: cases("1", "2", "3", "10", "1000", "1000000"),
  lambda t: "%d\n" % (lambda n: n * (n + 1) * (2 * n + 1) // 6)(int(t.strip())),
  r'''#include <cstdio>
inline long long sq(long long x) { return x * x; }
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    long long s = 0;
    for (int i = 1; i <= n; i++) s += sq(i);
    printf("%lld\n", s);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    long long n;
    if (scanf("%lld", &n) != 1) return 0;
    printf("%lld\n", n * (n + 1) * (2 * n + 1) / 6);   // 闭式公式
    return 0;
}
''',
  ["函数", "inline", "平方和"])

A("【函数】函数指针选最大最小", SEC_FN, 3,
  stmt("写一个函数 `int pick(int a[], int n, bool (*better)(int, int))`，"
       "用传入的比较函数决定是挑最大还是挑最小。读入 `n` 和 `n` 个整数，输出最大值与最小值。",
       ["函数指针参数写法：`bool (*better)(int, int)`，括号不能省，否则变成「返回函数指针的函数」",
        "把「怎么比」抽出来，挑最大和挑最小就是同一个函数换一个比较器",
        "输出一行，先最大值后最小值"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：`max min`。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases(barr(71, 5), barr(72, 1), barr(73, 20, -100, 100),
                barr(74, 50), "5\n3 3 3 3 3", barr(75, 9, -1000, -1)),
  lambda t: "%d %d\n" % (lambda v: (max(v), min(v)))(toks(t)[1:]),
  r'''#include <cstdio>
bool greaterThan(int a, int b) { return a > b; }
bool lessThan(int a, int b)    { return a < b; }
int pick(int a[], int n, bool (*better)(int, int)) {
    int r = a[0];
    for (int i = 1; i < n; i++) if (better(a[i], r)) r = a[i];
    return r;
}
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    printf("%d %d\n", pick(a, n, greaterThan), pick(a, n, lessThan));
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
#include <functional>
int pick(int a[], int n, std::function<bool(int, int)> better) {   // 换成 std::function
    int r = a[0];
    for (int i = 1; i < n; i++) if (better(a[i], r)) r = a[i];
    return r;
}
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    auto gt = [](int x, int y) { return x > y; };    // lambda 传进去
    auto lt = [](int x, int y) { return x < y; };
    printf("%d %d\n", pick(a, n, gt), pick(a, n, lt));
    return 0;
}
''',
  ["函数", "函数指针", "lambda"])

A("【函数】函数统计各分数段人数", SEC_FN, 2,
  stmt("写函数按 `[90,100]`、`[80,90)`、`[70,80)`、`[60,70)`、`[0,60)` 五档统计人数。"
       "读入 `n` 和 `n` 个成绩（0~100 的整数），按「优秀、良好、中等、及格、不及格」的顺序"
       "输出五个数字，一行，空格分隔。",
       ["区间是左闭右开，`90` 要落到第一档而不是第二档",
        "五档判断从高到低写 `if/else if` 就不会重叠",
        "输出五个整数"]),
  "第一行 `n`，第二行 `n` 个整数成绩。",
  "一行：五档人数。",
  "- 1 ≤ n ≤ 1000\n- 0 ≤ 成绩 ≤ 100",
  lambda: cases("5\n95 85 75 65 55", "1\n100", "1\n0", "4\n89 90 59 60",
                "10\n100 99 80 79 70 69 60 59 0 90",
                barr(81, 40, 0, 100)),
  lambda t: "%s\n" % " ".join(str(c) for c in (lambda v: (
      sum(1 for x in v if x >= 90),
      sum(1 for x in v if 80 <= x < 90),
      sum(1 for x in v if 70 <= x < 80),
      sum(1 for x in v if 60 <= x < 70),
      sum(1 for x in v if x < 60)))(toks(t)[1:])),
  r'''#include <cstdio>
void countByBand(const int s[], int n, int c[5]) {
    for (int i = 0; i < 5; i++) c[i] = 0;
    for (int i = 0; i < n; i++) {
        if (s[i] >= 90)      c[0]++;      // 从高到低，区间左闭右开不重叠
        else if (s[i] >= 80) c[1]++;
        else if (s[i] >= 70) c[2]++;
        else if (s[i] >= 60) c[3]++;
        else                 c[4]++;
    }
}
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int s[1005];
    for (int i = 0; i < n; i++) scanf("%d", &s[i]);
    int c[5];
    countByBand(s, n, c);
    for (int i = 0; i < 5; i++) printf("%d%c", c[i], i == 4 ? '\n' : ' ');
    return 0;
}
''',
  r'''#include <cstdio>
int band(int x) {                       // 用「档位下标」把判断收敛成一次除法
    if (x >= 90) return 0;
    if (x < 60)  return 4;
    return 4 - (x - 50) / 10;           // 60~69→3, 70~79→2, 80~89→1
}
int main() {
    int n, c[5] = {0, 0, 0, 0, 0};
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    for (int i = 0; i < n; i++) { int x; scanf("%d", &x); c[band(x)]++; }
    printf("%d %d %d %d %d\n", c[0], c[1], c[2], c[3], c[4]);
    return 0;
}
''',
  ["函数", "分段统计"])

# ===================================================================== #
#  SEC_RC · 递归与递推（20 题）
# ===================================================================== #

def _pass_ball(t: str) -> str:
    """n 人围成一圈，从 1 号开始传 m 次，回到 1 号的方案数。"""
    n, m = toks(t)
    dp = [0] * (n + 1)
    dp[1] = 1
    for _ in range(m):
        nx = [0] * (n + 1)
        for i in range(1, n + 1):
            nx[i] = dp[i - 1 if i > 1 else n] + dp[i + 1 if i < n else 1]
        dp = nx
    return "%d\n" % dp[1]


def _partition(t: str) -> str:
    """整数划分：把 n 拆成若干个正整数之和的方案数（无序）。"""
    n = int(t.strip())
    ways = [0] * (n + 1)
    ways[0] = 1
    for part in range(1, n + 1):
        for s in range(part, n + 1):
            ways[s] += ways[s - part]
    return "%d\n" % ways[n]


def _binary_search(t: str) -> str:
    tok = toks(t)
    n, x = tok[0], tok[1]
    a = tok[2:2 + n]
    for i, v in enumerate(a):
        if v == x:
            return "%d\n" % (i + 1)
    return "-1\n"


def _fib(t: str) -> str:
    n = int(t.strip())
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return "%d\n" % a


def _climb(t: str) -> str:
    n = int(t.strip())
    f = [0, 1, 2]
    for i in range(3, n + 1):
        f.append(f[-1] + f[-2])
    return "%d\n" % f[n]


def _trib(t: str) -> str:
    n = int(t.strip())
    f = [0, 1, 2, 4]
    for i in range(4, n + 1):
        f.append(f[-1] + f[-2] + f[-3])
    return "%d\n" % f[n]


def _peaches(t: str) -> str:
    n = int(t.strip())
    x = 1
    for _ in range(n - 1):
        x = (x + 1) * 2
    return "%d\n" % x


def _pascal_row(t: str) -> str:
    n = int(t.strip())
    row = [1]
    for _ in range(1, n):
        row = [1] + [row[k - 1] + row[k] for k in range(1, len(row))] + [1]
    return " ".join(str(v) for v in row) + "\n"


def _fib_sum(t: str) -> str:
    n = int(t.strip())
    a, b = 1, 1
    s = 0
    for _ in range(n):
        s += a
        a, b = b, a + b
    return "%d\n" % s


A("【递归】斐波那契数列第 n 项", SEC_RC, 1,
  stmt("用递归求斐波那契数列：`F(1) = F(2) = 1`，`F(n) = F(n-1) + F(n-2)`。"
       "读入 `n`（1 ≤ n ≤ 30），输出 `F(n)`。",
       ["边界写在函数开头：`n <= 2` 直接返回 1",
        "n 到 30 时朴素递归要算约 130 万次，能跑完；到 45 就明显卡了 —— 这是「递归树重复计算」的经典例子",
        "输出一个整数"]),
  "一行一个整数 `n`。",
  "一行：`F(n)`。",
  "- 1 ≤ n ≤ 30",
  lambda: cases("1", "2", "3", "10", "20", "30"),
  _fib,
  r'''#include <cstdio>
long long fib(int n) {
    if (n <= 2) return 1;             // 边界写最前
    return fib(n - 1) + fib(n - 2);
}
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    printf("%lld\n", fib(n));
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    long long a = 1, b = 1;           // 迭代：只留最近两项
    for (int i = 3; i <= n; i++) { long long c = a + b; a = b; b = c; }
    printf("%lld\n", n <= 2 ? 1LL : b);
    return 0;
}
''',
  ["递归", "斐波那契"])

A("【递归】爬楼梯方案数", SEC_RC, 2,
  stmt("楼梯有 `n` 级，每步只能走 1 级或 2 级。读入 `n`（1 ≤ n ≤ 40），输出走完的方案数。",
       ["最后一步要么是 1 级要么是 2 级，所以 `f(n) = f(n-1) + f(n-2)`",
        "`f(1) = 1`、`f(2) = 2`，注意和斐波那契的初值不同",
        "n = 40 时答案约 1.6×10⁸，`long long` 稳妥"]),
  "一行一个整数 `n`。",
  "一行：方案数。",
  "- 1 ≤ n ≤ 40",
  lambda: cases("1", "2", "3", "5", "20", "40"),
  _climb,
  r'''#include <cstdio>
long long climb(int n) {
    if (n == 1) return 1;
    if (n == 2) return 2;
    return climb(n - 1) + climb(n - 2);
}
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    printf("%lld\n", climb(n));
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    long long f[45] = {0, 1, 2};      // 递推表：从小到大填
    for (int i = 3; i <= n; i++) f[i] = f[i - 1] + f[i - 2];
    printf("%lld\n", f[n]);
    return 0;
}
''',
  ["递归", "递推", "爬楼梯"])

A("【递归】汉诺塔移动次数", SEC_RC, 2,
  stmt("n 个盘子的汉诺塔最少需要移动多少次？读入 `n`（1 ≤ n ≤ 62），输出移动次数。",
       ["递推式 `T(n) = 2T(n-1) + 1`，闭式解是 `2^n - 1`",
        "`1 << n` 在 n ≥ 31 时对 `int` 是未定义行为，必须写 `1LL << n`",
        "n = 62 时结果是 4611686018427387903，还在 `long long` 内"]),
  "一行一个整数 `n`。",
  "一行：最少移动次数。",
  "- 1 ≤ n ≤ 62",
  lambda: cases("1", "2", "3", "10", "31", "62"),
  lambda t: "%d\n" % (2 ** int(t.strip()) - 1),
  r'''#include <cstdio>
long long hanoi(int n) {
    if (n == 1) return 1;
    return 2 * hanoi(n - 1) + 1;
}
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    printf("%lld\n", hanoi(n));
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    printf("%lld\n", (1LL << n) - 1);   // 必须 1LL，写 1<<62 是未定义行为
    return 0;
}
''',
  ["递归", "汉诺塔", "位运算"])

A("【递归】欧几里得求最大公约数", SEC_RC, 1,
  stmt("用递归写辗转相除法：`gcd(a, b) = gcd(b, a % b)`，`gcd(a, 0) = a`。"
       "读入 `a b`，输出最大公约数。",
       ["递归出口是 `b == 0`，此时 `a` 就是答案",
        "`a % b` 在 `b > a` 时会自动交换一轮，不用提前判断大小",
        "输出一个整数"]),
  "一行两个正整数 `a b`。",
  "一行：最大公约数。",
  "- 1 ≤ a, b ≤ 10⁹",
  lambda: cases("12 18", "1 1", "7 13", "1000000000 999999937", "270 192", "36 48"),
  lambda t: "%d\n" % (lambda a, b: __import__("math").gcd(a, b))(*toks(t)),
  r'''#include <cstdio>
int gcd(int a, int b) {
    return b == 0 ? a : gcd(b, a % b);
}
int main() {
    int a, b;
    if (scanf("%d %d", &a, &b) != 2) return 0;
    printf("%d\n", gcd(a, b));
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int a, b;
    if (scanf("%d %d", &a, &b) != 2) return 0;
    while (b) { int t = a % b; a = b; b = t; }   // 迭代版
    printf("%d\n", a);
    return 0;
}
''',
  ["递归", "gcd"])

A("【递推】走方格路径数", SEC_RC, 2,
  stmt("一个 `n` 行 `m` 列的方格，从左下角走到右上角，每步只能向右或向上。"
       "读入 `n m`，输出不同的走法数。",
       ["一共要走 `n + m` 步，其中向上 `n` 步、向右 `m` 步，答案是组合数 `C(n+m, n)`",
        "递推写法：`f[i][j] = f[i-1][j] + f[i][j-1]`，边界上都是 1",
        "n, m ≤ 20 时答案最大约 1.4×10¹¹，用 `long long`"]),
  "一行两个正整数 `n m`。",
  "一行：走法数。",
  "- 1 ≤ n, m ≤ 20",
  lambda: cases("1 1", "2 2", "3 3", "10 10", "20 20", "1 20"),
  lambda t: "%d\n" % (lambda n, m: __import__("math").comb(n + m, n))(*toks(t)),
  r'''#include <cstdio>
long long f[25][25];
int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    for (int i = 0; i <= n; i++)
        for (int j = 0; j <= m; j++) {
            if (i == 0 || j == 0) f[i][j] = 1;              // 边界只有一条路
            else f[i][j] = f[i - 1][j] + f[i][j - 1];
        }
    printf("%lld\n", f[n][m]);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    long long c = 1;                      // 直接算组合数 C(n+m, n)
    int k = n + m;
    for (int i = 1; i <= n; i++) c = c * (k - i + 1) / i;
    printf("%lld\n", c);
    return 0;
}
''',
  ["递推", "组合数", "路径"])

A("【递推】猴子吃桃逆推", SEC_RC, 2,
  stmt("猴子第一天摘了若干个桃子，每天吃掉「现有桃子的一半再加一个」，"
       "到第 `n` 天早上只剩 1 个。读入 `n`（1 ≤ n ≤ 60），输出第一天摘了多少个。",
       ["正向是 `x/2 - 1`，逆推就是 `(x + 1) * 2`",
        "从第 n 天的 1 个往回推 `n-1` 次",
        "n = 60 时答案约 3.5×10¹⁸，`long long` 刚好够"]),
  "一行一个整数 `n`。",
  "一行：第一天桃子数。",
  "- 1 ≤ n ≤ 60",
  lambda: cases("1", "2", "3", "4", "10", "60"),
  _peaches,
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    long long x = 1;                  // 第 n 天早上剩 1 个
    for (int d = n; d > 1; d--) x = (x + 1) * 2;   // 逆推一步
    printf("%lld\n", x);
    return 0;
}
''',
  r'''#include <cstdio>
long long back(long long x, int days) {     // 递归逆推
    if (days <= 1) return x;
    return back((x + 1) * 2, days - 1);
}
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    printf("%lld\n", back(1, n));
    return 0;
}
''',
  ["递推", "逆推"])

A("【递推】杨辉三角第 n 行", SEC_RC, 2,
  stmt("用递推生成杨辉三角，读入 `n`（1 ≤ n ≤ 20），输出第 `n` 行的所有数，一行，空格分隔。",
       ["第 1 行是 `1`，第 2 行是 `1 1`，每行首尾都是 1",
        "`a[i][j] = a[i-1][j-1] + a[i-1][j]`",
        "第 20 行最大项是 C(19,9) = 92378，`int` 够用"]),
  "一行一个整数 `n`。",
  "一行：第 `n` 行的 `n` 个数。",
  "- 1 ≤ n ≤ 20",
  lambda: cases("1", "2", "3", "5", "10", "20"),
  _pascal_row,
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    long long a[25][25] = {{0}};
    for (int i = 0; i < n; i++) {
        a[i][0] = a[i][i] = 1;                       // 首尾为 1
        for (int j = 1; j < i; j++)
            a[i][j] = a[i - 1][j - 1] + a[i - 1][j];
    }
    for (int j = 0; j < n; j++) printf("%lld%c", a[n - 1][j], j + 1 == n ? '\n' : ' ');
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    long long row[25] = {1};             // 一维滚动：从后往前更新
    for (int i = 1; i < n; i++)
        for (int j = i; j >= 1; j--) row[j] += row[j - 1];
    for (int j = 0; j < n; j++) printf("%lld%c", row[j], j + 1 == n ? '\n' : ' ');
    return 0;
}
''',
  ["递推", "杨辉三角"])

A("【递推】调和级数前 n 项和", SEC_RC, 1,
  stmt("读入 `n`（1 ≤ n ≤ 10⁵），输出 `1 + 1/2 + 1/3 + … + 1/n`，保留 6 位小数。",
       ["`1 / i` 是整数除法，结果恒为 0（i = 1 时是 1），必须写 `1.0 / i`",
        "累加用 `double`",
        "输出用 `%.6f`"]),
  "一行一个整数 `n`。",
  "一行：和，保留 6 位小数。",
  "- 1 ≤ n ≤ 100000",
  lambda: cases("1", "2", "3", "10", "1000", "100000"),
  lambda t: "%.6f\n" % sum(1.0 / k for k in range(1, int(t.strip()) + 1)),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    double s = 0;
    for (int i = 1; i <= n; i++) s += 1.0 / i;   // 1.0 不能写成 1
    printf("%.6f\n", s);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    double s = 0;
    for (int i = n; i >= 1; i--) s += 1.0 / i;   // 倒着加，浮点误差略小
    printf("%.6f\n", s);
    return 0;
}
''',
  ["递推", "浮点", "调和级数"])

A("【递推】传球方案数", SEC_RC, 3,
  stmt("`n` 个人围成一圈（编号 1~n），球从 1 号开始，每次可以把球传给左边或右边的人，"
       "共传 `m` 次。读入 `n m`，输出传 `m` 次后球回到 1 号的不同路径数。",
       ["状态是「传了 k 次之后球在谁手里」，`dp[0][1] = 1`",
        "转移：`dp[k][i] = dp[k-1][i-1] + dp[k-1][i+1]`，下标首尾相接绕成环",
        "n = 2 时左右是同一个人，两边的方案都要算，别去重"]),
  "一行两个整数 `n m`。",
  "一行：方案数。",
  "- 2 ≤ n ≤ 20\n- 1 ≤ m ≤ 30",
  lambda: cases("3 3", "2 2", "5 4", "10 10", "20 30", "3 1"),
  _pass_ball,
  r'''#include <cstdio>
long long dp[35][25];
int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    dp[0][1] = 1;
    for (int k = 1; k <= m; k++)
        for (int i = 1; i <= n; i++) {
            int l = (i == 1) ? n : i - 1;        // 左边，绕回 n
            int r = (i == n) ? 1 : i + 1;        // 右边，绕回 1
            dp[k][i] = dp[k - 1][l] + dp[k - 1][r];
        }
    printf("%lld\n", dp[m][1]);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    long long cur[25] = {0}, nxt[25] = {0};
    cur[1] = 1;                                   // 一维滚动
    for (int k = 1; k <= m; k++) {
        for (int i = 1; i <= n; i++)
            nxt[i] = cur[i == 1 ? n : i - 1] + cur[i == n ? 1 : i + 1];
        for (int i = 1; i <= n; i++) cur[i] = nxt[i];
    }
    printf("%lld\n", cur[1]);
    return 0;
}
''',
  ["递推", "环", "路径计数"])

A("【递推】斐波那契前 n 项和", SEC_RC, 2,
  stmt("读入 `n`（1 ≤ n ≤ 60），输出斐波那契数列前 `n` 项之和（`F(1) = F(2) = 1`）。",
       ["边递推边累加最省事，也可以利用 `sum(n) = F(n+2) - 1`",
        "n = 60 时 F(62) ≈ 4×10¹²，和也在 `long long` 内",
        "输出一个整数"]),
  "一行一个整数 `n`。",
  "一行：前 `n` 项和。",
  "- 1 ≤ n ≤ 60",
  lambda: cases("1", "2", "3", "10", "30", "60"),
  _fib_sum,
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    long long a = 1, b = 1, s = 0;
    for (int i = 1; i <= n; i++) { s += a; long long c = a + b; a = b; b = c; }
    printf("%lld\n", s);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    long long f[65] = {0, 1, 1};          // 先填表再求和
    for (int i = 3; i <= n + 2; i++) f[i] = f[i - 1] + f[i - 2];
    printf("%lld\n", f[n + 2] - 1);        // 用闭式：sum = F(n+2) - 1
    return 0;
}
''',
  ["递推", "斐波那契", "前缀和"])

A("【递推】牛顿迭代求平方根", SEC_RC, 3,
  stmt("用牛顿迭代求 `√x`：`t = (t + x / t) / 2`，迭代到前后两次的差小于 `1e-12` 为止。"
       "读入正整数 `x`（1 ≤ x ≤ 10⁹），输出 `√x`，保留 6 位小数。",
       ["初值取 `t = x` 就行，收敛是二阶的，10 次左右就够",
        "循环条件写成 `while (fabs(nx - t) > 1e-12)`",
        "`x / t` 里两个都是 `double`，不要写成整数除法"]),
  "一行一个整数 `x`。",
  "一行：`√x`，保留 6 位小数。",
  "- 1 ≤ x ≤ 10⁹",
  lambda: cases("2", "10", "12345", "999999937", "7", "1000000"),
  lambda t: "%.6f\n" % (int(t.strip()) ** 0.5),
  r'''#include <cstdio>
#include <cmath>
int main() {
    int x;
    if (scanf("%d", &x) != 1) return 0;
    double t = x;
    for (int i = 0; i < 100; i++) {
        double nx = (t + x / t) / 2.0;
        if (fabs(nx - t) < 1e-12) { t = nx; break; }
        t = nx;
    }
    printf("%.6f\n", t);
    return 0;
}
''',
  r'''#include <cstdio>
#include <cmath>
int main() {
    int x;
    if (scanf("%d", &x) != 1) return 0;
    printf("%.6f\n", sqrt((double)x));   // 库函数版
    return 0;
}
''',
  ["递推", "牛顿迭代", "浮点"])

A("【递推】卡特兰数（括号序列计数）", SEC_RC, 3,
  stmt("n 对括号能组成多少种合法的括号序列？读入 `n`（1 ≤ n ≤ 15），输出卡特兰数 `C_n`。",
       ["`C_n = C(2n, n) / (n + 1)`，也满足递推 `C_n = Σ C_i · C_{n-1-i}`",
        "直接算组合数时先乘后除，中途不会出现小数",
        "n = 15 时 C₁₅ = 9694845，`long long` 绰绰有余"]),
  "一行一个整数 `n`。",
  "一行：`C_n`。",
  "- 1 ≤ n ≤ 15",
  lambda: cases("1", "2", "3", "5", "10", "15"),
  lambda t: "%d\n" % (lambda n: __import__("math").comb(2 * n, n) // (n + 1))(int(t.strip())),
  r'''#include <cstdio>
long long cat[20];
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    cat[0] = 1;
    for (int i = 1; i <= n; i++) {             // 用递推式，不碰除法
        long long s = 0;
        for (int j = 0; j < i; j++) s += cat[j] * cat[i - 1 - j];
        cat[i] = s;
    }
    printf("%lld\n", cat[n]);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    long long c = 1;                           // 组合数公式，先乘后除
    for (int i = 1; i <= n; i++) c = c * (n + i) / i;
    printf("%lld\n", c / (n + 1));
    return 0;
}
''',
  ["递推", "卡特兰数", "组合数"])

A("【递归】递归求 1 到 n 的和", SEC_RC, 1,
  stmt("用递归求 `1 + 2 + … + n`。读入 `n`（1 ≤ n ≤ 1000），输出和。",
       ["递归出口 `n == 1` 返回 1",
        "递归深度等于 n，n 到 10⁵ 会爆栈 —— 这正是「能用循环就别用递归」的场景",
        "输出一个整数"]),
  "一行一个整数 `n`。",
  "一行：和。",
  "- 1 ≤ n ≤ 1000",
  lambda: cases("1", "2", "10", "100", "999", "1000"),
  lambda t: "%d\n" % (lambda n: n * (n + 1) // 2)(int(t.strip())),
  r'''#include <cstdio>
long long sumTo(int n) {
    if (n == 1) return 1;              // 出口
    return n + sumTo(n - 1);
}
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    printf("%lld\n", sumTo(n));
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    printf("%lld\n", (long long)n * (n + 1) / 2);   // 公式法，O(1)
    return 0;
}
''',
  ["递归", "求和"])

A("【递归】递归逆序输出数字", SEC_RC, 2,
  stmt("把一个整数的各位数字逆序组成新整数。读入 `a`（|a| ≤ 10⁹），输出逆序后的数，"
       "去掉前导零，负号保留。",
       ["`a = -1200` 的结果是 `-21`：符号与数值分开处理，前导零要去掉",
        "`a = 0` 输出 `0`",
        "用 `long long` 存反转结果，避免中间溢出"]),
  "一行一个整数 `a`。",
  "一行：逆序后的整数。",
  "- |a| ≤ 10⁹",
  lambda: cases("1200", "-1200", "0", "7", "1000000000", "-1000000001"),
  lambda t: "%d\n" % (lambda a: (1 if a >= 0 else -1) * int(str(abs(a))[::-1]))(int(t.strip())),
  r'''#include <cstdio>
int main() {
    long long a;
    if (scanf("%lld", &a) != 1) return 0;
    int sign = a < 0 ? -1 : 1;
    long long v = a < 0 ? -a : a, r = 0;
    while (v > 0) { r = r * 10 + v % 10; v /= 10; }   // 逐位拼新数
    printf("%lld\n", sign * r);
    return 0;
}
''',
  r'''#include <cstdio>
#include <cstring>
#include <cstdlib>
void rev(char *s, int i, int j) {        // 递归反转字符数组
    if (i >= j) return;
    char t = s[i]; s[i] = s[j]; s[j] = t;
    rev(s, i + 1, j - 1);
}
int main() {
    long long a;
    if (scanf("%lld", &a) != 1) return 0;
    char buf[32];
    snprintf(buf, sizeof(buf), "%lld", a < 0 ? -a : a);
    rev(buf, 0, (int)strlen(buf) - 1);
    long long r = atoll(buf);             // atoll 自动跳过前导零
    printf("%lld\n", a < 0 ? -r : r);
    return 0;
}
''',
  ["递归", "逆序", "数字"])

A("【递归】递归求数组元素和", SEC_RC, 1,
  stmt("用递归求数组元素之和。读入 `n` 和 `n` 个整数（|x| ≤ 10⁶），输出总和。",
       ["递归形式：`sum(a, n) = a[n-1] + sum(a, n-1)`，出口是 `n == 0`",
        "和用 `long long`：10⁵ 个 10⁶ 就是 10¹¹",
        "输出一个整数"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：总和。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases(barr(91, 5), barr(92, 1), barr(93, 20), barr(94, 100, -1000, 1000),
                "3\n-1 -2 -3", barr(95, 200, -1000000, 1000000)),
  lambda t: "%d\n" % sum(toks(t)[1:]),
  r'''#include <cstdio>
long long sumOf(const int a[], int n) {
    if (n == 0) return 0;              // 出口：空数组和为 0
    return a[n - 1] + sumOf(a, n - 1);
}
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    printf("%lld\n", sumOf(a, n));
    return 0;
}
''',
  r'''#include <cstdio>
long long sumOf(const int *p, const int *end) {   // 指针区间递归
    if (p == end) return 0;
    return *p + sumOf(p + 1, end);
}
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    printf("%lld\n", sumOf(a, a + n));
    return 0;
}
''',
  ["递归", "数组"])

A("【递归】递归二分查找", SEC_RC, 3,
  stmt("数组**严格递增**。读入 `n` 和 `x`，第二行 `n` 个整数，用递归二分查找 `x`，"
       "找到输出它的下标（从 1 开始），找不到输出 `-1`。",
       ["递归参数是区间 `[lo, hi]`，出口是 `lo > hi`",
        "`mid = lo + (hi - lo) / 2` 比 `(lo + hi) / 2` 更能防溢出",
        "只输出一个整数"]),
  "第一行 `n x`；第二行 `n` 个严格递增整数。",
  "一行：下标（1 起）或 `-1`。",
  "- 1 ≤ n ≤ 10⁵\n- |x|, |a[i]| ≤ 10⁹",
  lambda: cases("5 3\n1 3 5 7 9", "5 4\n1 3 5 7 9", "1 1\n1", "1 2\n1",
                "%d %d\n%s" % (10, 17, " ".join(str(2 * i + 1) for i in range(10))),
                "%d %d\n%s" % (20, 100, " ".join(str(3 * i - 20) for i in range(20)))),
  _binary_search,
  r'''#include <cstdio>
int bs(const int a[], int lo, int hi, int x) {
    if (lo > hi) return -1;                  // 出口：区间空了
    int mid = lo + (hi - lo) / 2;
    if (a[mid] == x) return mid + 1;         // 题目要 1 起
    if (a[mid] < x)  return bs(a, mid + 1, hi, x);
    return bs(a, lo, mid - 1, x);
}
int main() {
    int n, x;
    if (scanf("%d %d", &n, &x) != 2) return 0;
    static int a[100005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    printf("%d\n", bs(a, 0, n - 1, x));
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n, x;
    if (scanf("%d %d", &n, &x) != 2) return 0;
    static int a[100005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int lo = 0, hi = n - 1, ans = -1;         // 迭代版，结果一样
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == x) { ans = mid + 1; break; }
        if (a[mid] < x) lo = mid + 1; else hi = mid - 1;
    }
    printf("%d\n", ans);
    return 0;
}
''',
  ["递归", "二分查找"])

A("【递推】整数划分方案数", SEC_RC, 3,
  stmt("把正整数 `n` 拆成若干个正整数之和（不计顺序），有多少种拆法？"
       "读入 `n`（1 ≤ n ≤ 20），输出方案数。",
       ["`p(1)=1, p(2)=2 (2 / 1+1), p(3)=3, p(4)=5, p(5)=7`",
        "按「允许用的最大加数」从小到大做背包式递推，就不会重复计数",
        "n = 20 时 p(20) = 627，`int` 够"]),
  "一行一个整数 `n`。",
  "一行：方案数。",
  "- 1 ≤ n ≤ 20",
  lambda: cases("1", "2", "3", "4", "5", "20"),
  _partition,
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    long long p[25] = {1};                  // p[0] = 1 是递推的起点
    for (int part = 1; part <= n; part++)
        for (int s = part; s <= n; s++)
            p[s] += p[s - part];            // 完全背包：每个加数可用多次
    printf("%lld\n", p[n]);
    return 0;
}
''',
  r'''#include <cstdio>
long long f[25][25];                        // f[i][j]：用不超过 j 的加数凑 i
long long ways(int i, int j) {
    if (i == 0) return 1;
    if (j == 0) return 0;
    if (f[i][j]) return f[i][j];            // 记忆化
    long long r = ways(i, j - 1);
    if (j <= i) r += ways(i - j, j);
    return f[i][j] = r;
}
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    printf("%lld\n", ways(n, n));
    return 0;
}
''',
  ["递推", "整数划分", "完全背包"])

A("【递推】每次可走 1 到 3 级台阶", SEC_RC, 2,
  stmt("楼梯有 `n` 级，每步可以走 1 级、2 级或 3 级。读入 `n`（1 ≤ n ≤ 40），输出走完的方案数。",
       ["`f(n) = f(n-1) + f(n-2) + f(n-3)`",
        "`f(1)=1, f(2)=2, f(3)=4`，别直接套斐波那契的初值",
        "n = 40 时约 2.4×10⁸，`long long` 稳妥"]),
  "一行一个整数 `n`。",
  "一行：方案数。",
  "- 1 ≤ n ≤ 40",
  lambda: cases("1", "2", "3", "4", "10", "40"),
  _trib,
  r'''#include <cstdio>
long long f[45] = {0, 1, 2, 4};
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 4; i <= n; i++) f[i] = f[i - 1] + f[i - 2] + f[i - 3];
    printf("%lld\n", f[n]);
    return 0;
}
''',
  r'''#include <cstdio>
long long go(int n) {                        // 记忆化递归版（自顶向下）
    if (n == 1) return 1;
    if (n == 2) return 2;
    if (n == 3) return 4;
    static long long memo[50];
    if (memo[n]) return memo[n];
    return memo[n] = go(n - 1) + go(n - 2) + go(n - 3);
}
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    printf("%lld\n", go(n));
    return 0;
}
''',
  ["递推", "台阶"])

A("【递归】递归输出二进制", SEC_RC, 2,
  stmt("用递归把一个正整数打印成二进制（不带前导零）。读入 `n`（1 ≤ n ≤ 10⁹），输出它的二进制表示。",
       ["先递归处理 `n / 2`，再打印 `n % 2`，顺序就正过来了",
        "出口是 `n == 0` 直接返回（什么都不打印），否则最高位会多一个 0",
        "输出一行 01 串"]),
  "一行一个整数 `n`。",
  "一行：二进制表示。",
  "- 1 ≤ n ≤ 10⁹",
  lambda: cases("1", "2", "5", "10", "1000000000", "1023"),
  lambda t: "%s\n" % bin(int(t.strip()))[2:],
  r'''#include <cstdio>
void toBin(int n) {
    if (n == 0) return;          // 出口什么都不打印，避免前导 0
    toBin(n / 2);
    printf("%d", n % 2);         // 回溯时打印，顺序才是高位在前
}
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    toBin(n);
    printf("\n");
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    char s[40]; int k = 0;
    while (n) { s[k++] = char('0' + n % 2); n /= 2; }   // 低位先入栈
    while (k--) putchar(s[k]);                          // 倒着输出
    printf("\n");
    return 0;
}
''',
  ["递归", "二进制", "回溯顺序"])

A("【递推】年龄问题", SEC_RC, 1,
  stmt("第 1 个人 10 岁，后面每个人都比前一个人大 2 岁。读入 `n`（1 ≤ n ≤ 1000），"
       "输出第 `n` 个人的年龄。",
       ["递推式：`age(n) = age(n-1) + 2`，起点 `age(1) = 10`",
        "也可以直接算 `10 + 2 * (n - 1)`",
        "输出一个整数"]),
  "一行一个整数 `n`。",
  "一行：第 `n` 个人的年龄。",
  "- 1 ≤ n ≤ 1000",
  lambda: cases("1", "2", "3", "10", "100", "1000"),
  lambda t: "%d\n" % (10 + 2 * (int(t.strip()) - 1)),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int age = 10;
    for (int i = 2; i <= n; i++) age += 2;   // 递推
    printf("%d\n", age);
    return 0;
}
''',
  r'''#include <cstdio>
int ageOf(int n) {                  // 递归版
    if (n == 1) return 10;
    return ageOf(n - 1) + 2;
}
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    printf("%d\n", ageOf(n));
    return 0;
}
''',
  ["递推", "年龄"])


if __name__ == "__main__":
    sys.exit(cli(PROBLEMS, "app/problems_bank_cpp_basic4.py",
                 "第 4 册：函数与参数传递 / 递归与递推", "CPP_BASIC4_PROBLEMS"))
