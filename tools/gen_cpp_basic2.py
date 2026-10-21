# -*- coding: utf-8 -*-
"""C++ 基础编程题 · 第 2 册：循环结构（16）+ 嵌套循环与图形（12）= 28 题。

对应教材第 02 讲后半（循环）与第 06 讲（数组前的循环训练）。
图形题一律按「空格 + 星号 + 空格」的精确格式输出，判题为逐字节比对，
所以行末不能多空格 —— 这是初学者最常见的失分点，题干里都点名了。

重生成：python tools/gen_cpp_basic2.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cpp_basic_kit import cases, cli, stmt          # noqa: E402

SEC_LOOP = "C++ 编程 · 循环结构"
SEC_FIG = "C++ 编程 · 嵌套循环与图形"

PROBLEMS: list[dict] = []


def A(title, sec, d, st, inf, outf, con, inp, orc, sol, alt, tags):
    PROBLEMS.append(dict(title=title, section=sec, difficulty=d, statement_md=st,
                         input_format=inf, output_format=outf, constraints_md=con,
                         inputs=inp, oracle=orc, solution=sol, alt=alt, tags=tags))


def _cdiv(a: int, b: int) -> int:
    q = abs(a) // abs(b)
    return -q if (a < 0) != (b < 0) else q


def _cmod(a: int, b: int) -> int:
    return a - _cdiv(a, b) * b


# ===================================================================== #
#  SEC_LOOP · 循环结构（16 题）
# ===================================================================== #

A("【循环】1 到 n 求和", SEC_LOOP, 1,
  stmt("读入 `n` 个正整数，对每个输出 `1 + 2 + ... + n` 的和。",
       ["`n` 最大 10⁹，`n(n+1)/2` 达 5×10¹⁷，必须用 `long long`",
        "循环累加和公式都能过，但公式更快；注意 `n * (n + 1)` 要在 long long 里做",
        "输出一行一个"]),
  "第一行 `n`；第二行 `n` 个正整数。",
  "`n` 行，每行一个整数。",
  "- 1 ≤ n ≤ 6\n- 1 ≤ 值 ≤ 10⁹",
  lambda: cases("3\n1 10 100", "1\n1000000000", "2\n999999999 500000000",
                "4\n2 3 4 5", "1\n0", "3\n1000000 2000000 3000000"),
  lambda t: "".join("%d\n" % (int(x) * (int(x) + 1) // 2) for x in t.split()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        long long x;
        scanf("%lld", &x);
        long long s = 0;
        for (long long i = 1; i <= x; i++) s += i;   // 老实累加
        printf("%lld\n", s);
    }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        long long x;
        scanf("%lld", &x);
        printf("%lld\n", x * (x + 1) / 2);          // 等差数列公式
    }
    return 0;
}
''',
  ["C++基础", "循环", "累加", "long long"])

A("【循环】n 的阶乘", SEC_LOOP, 1,
  stmt("读入 `n` 个整数（0 ≤ x ≤ 20），输出每个数的阶乘。",
       ["`20! = 2432902008176640000`，`long long` 刚好装得下；`21!` 就溢出了",
        "`0! = 1`，循环一次都不进，初值必须是 1 不是 0",
        "别用 `int`：13! 就已经超了"]),
  "第一行 `n`；第二行 `n` 个整数。",
  "`n` 行，每行一个整数。",
  "- 1 ≤ n ≤ 6\n- 0 ≤ x ≤ 20",
  lambda: cases("3\n0 5 10", "1\n20", "2\n13 14", "4\n1 2 3 4",
                "1\n19", "3\n15 16 17"),
  lambda t: "".join("%d\n" % _fact(int(x)) for x in t.split()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        int x;
        scanf("%d", &x);
        long long f = 1;                 // 0! = 1
        for (int i = 2; i <= x; i++) f *= i;
        printf("%lld\n", f);
    }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    long long f[21];
    f[0] = 1;
    for (int i = 1; i <= 20; i++) f[i] = f[i - 1] * i;   // 先打表
    while (n--) {
        int x;
        scanf("%d", &x);
        printf("%lld\n", f[x]);
    }
    return 0;
}
''',
  ["C++基础", "循环", "阶乘", "溢出"])

A("【循环】最大公约数", SEC_LOOP, 2,
  stmt("读入 `n` 对正整数，输出每对的最大公约数。",
       ["辗转相除：`while (b) { t = a % b; a = b; b = t; }`，最后 `a` 就是答案",
        "别用「从 1 试到较小数」的写法，虽然对但慢",
        "两数相等、其中一个为 1 都是边界"]),
  "第一行 `n`；接下来 `n` 行，每行两个正整数。",
  "`n` 行，每行一个整数。",
  "- 1 ≤ n ≤ 6\n- 1 ≤ a, b ≤ 10⁹",
  lambda: cases("3\n12 18\n100 75\n7 13", "1\n1 1", "2\n1000000000 999999999\n1 1000000000",
                "3\n48 18\n17 5\n36 60", "1\n2147483647 3", "2\n6 6\n2 4"),
  lambda t: "".join("%d\n" % _gcd(*map(int, ln.split()))
                    for ln in t.strip().splitlines()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        long long a, b;
        scanf("%lld %lld", &a, &b);
        while (b) {                     // 辗转相除
            long long t = a % b;
            a = b;
            b = t;
        }
        printf("%lld\n", a);
    }
    return 0;
}
''',
  r'''#include <cstdio>
long long gcd(long long a, long long b) {
    return b == 0 ? a : gcd(b, a % b);   // 递归写法
}
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        long long a, b;
        scanf("%lld %lld", &a, &b);
        printf("%lld\n", gcd(a, b));
    }
    return 0;
}
''',
  ["C++基础", "循环", "辗转相除"])

A("【循环】最小公倍数", SEC_LOOP, 2,
  stmt("读入 `n` 对正整数，输出每对的最小公倍数。",
       ["`lcm = a / gcd(a, b) * b` —— 先除后乘，避免 `a*b` 溢出",
        "写成 `a * b / gcd` 在 `a, b` 接近 10⁹ 时会溢出 `long long`",
        "结果可能很大，用 `long long`"]),
  "第一行 `n`；接下来 `n` 行，每行两个正整数。",
  "`n` 行，每行一个整数。",
  "- 1 ≤ n ≤ 6\n- 1 ≤ a, b ≤ 10⁹，保证 lcm ≤ 10¹⁸",
  lambda: cases("3\n12 18\n4 6\n7 13", "1\n1 1", "2\n999999999 1000000000\n6 8",
                "2\n21 6\n9 12", "1\n1000000000 999999999", "3\n2 3\n5 7\n11 13"),
  lambda t: "".join("%d\n" % _lcm(*map(int, ln.split()))
                    for ln in t.strip().splitlines()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        long long a, b;
        scanf("%lld %lld", &a, &b);
        long long x = a, y = b;
        while (y) { long long t = x % y; x = y; y = t; }   // x = gcd
        printf("%lld\n", a / x * b);                        // 先除后乘
    }
    return 0;
}
''',
  r'''#include <cstdio>
#include <numeric>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        long long a, b;
        scanf("%lld %lld", &a, &b);
        long long g = std::gcd(a, b);      // C++17 标准库直接给 gcd
        printf("%lld\n", a / g * b);
    }
    return 0;
}
''',
  ["C++基础", "循环", "最小公倍数", "溢出"])

A("【循环】素数判定", SEC_LOOP, 2,
  stmt("读入 `n` 个整数（≥ 2），判断是否素数，是输出 `YES`，否输出 `NO`。",
       ["试除到 `i * i > x` 就够了，不要除到 `x`",
        "1 和负数都不是素数，但本题数据 ≥ 2",
        "`i * i` 可能溢出 `int`，用 `(long long)i * i`"]),
  "第一行 `n`；第二行 `n` 个整数。",
  "`n` 行，每行 `YES` 或 `NO`。",
  "- 1 ≤ n ≤ 6\n- 2 ≤ x ≤ 10⁹",
  lambda: cases("5\n2 3 4 9 17", "1\n1000000007", "4\n25 49 97 121",
                "3\n1000000000 999999937 1000003", "2\n5 6", "3\n7919 7920 7921"),
  lambda t: "".join("%s\n" % ("YES" if _isprime(int(x)) else "NO") for x in t.split()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        long long x;
        scanf("%lld", &x);
        bool ok = true;
        if (x < 2) ok = false;
        for (long long i = 2; i * i <= x; i++) {     // 只试到平方根
            if (x % i == 0) { ok = false; break; }
        }
        printf("%s\n", ok ? "YES" : "NO");
    }
    return 0;
}
''',
  r'''#include <cstdio>
#include <cmath>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        long long x;
        scanf("%lld", &x);
        bool ok = (x >= 2);
        long long lim = (long long)std::sqrt((double)x) + 1;
        for (long long i = 2; ok && i <= lim && i < x; i++) {
            if (x % i == 0) ok = false;
        }
        printf("%s\n", ok ? "YES" : "NO");
    }
    return 0;
}
''',
  ["C++基础", "循环", "素数", "平方根"])

A("【循环】分解质因数", SEC_LOOP, 3,
  stmt("读入 `n` 个整数（≥ 2），把每个数分解成质因数连乘的形式输出。\n\n"
       "格式要求：质因数按**从小到大**排列，用 `*` 连接，不合并相同的因子。\n\n"
       "例如 `12 = 2*2*3`，`97 = 97`。",
       ["从 2 开始试除，能除尽就一直除（`while (x % i == 0)`）",
        "除到 `i * i > x` 就停；此时若 `x > 1`，剩下的 `x` 本身就是一个质因数",
        "输出不能有行末的 `*`"]),
  "第一行 `n`；第二行 `n` 个整数。",
  "`n` 行，每行一个分解式。",
  "- 1 ≤ n ≤ 6\n- 2 ≤ x ≤ 10⁹",
  lambda: cases("3\n12 97 360", "1\n2", "2\n1000000007 1024",
                "3\n100 101 999999937", "1\n999999999", "2\n30 210"),
  lambda t: "".join(_factor(int(x)) for x in t.split()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        long long x;
        scanf("%lld", &x);
        bool first = true;
        for (long long i = 2; i * i <= x; i++) {
            while (x % i == 0) {
                if (!first) printf("*");
                printf("%lld", i);
                first = false;
                x /= i;
            }
        }
        if (x > 1) {                      // 剩下的大质因子
            if (!first) printf("*");
            printf("%lld", x);
        }
        printf("\n");
    }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        long long x;
        scanf("%lld", &x);
        long long f[64], cnt = 0;
        for (long long d = 2; d * d <= x; d++)
            while (x % d == 0) { f[cnt++] = d; x /= d; }
        if (x > 1) f[cnt++] = x;
        for (long long i = 0; i < cnt; i++) {      // 先存后打，省掉 first 标志
            if (i) printf("*");
            printf("%lld", f[i]);
        }
        printf("\n");
    }
    return 0;
}
''',
  ["C++基础", "循环", "质因数"])

A("【循环】n 以内的完全数", SEC_LOOP, 3,
  stmt("读入 `n` 个上界 `m`，输出不超过 `m` 的**全部完全数**（真因子之和等于自身）。\n\n"
       "输出按从小到大，空格分隔；若一个都没有，输出 `none`。",
       ["真因子是「除自己以外的因子」，判到 `i < x` 即可",
        "试除只到 `sqrt` 再配对能快一倍，但 `m ≤ 10000` 时朴素写法也够",
        "6、28、496、8128 是四位以内的全部完全数"]),
  "第一行 `n`；第二行 `n` 个正整数。",
  "`n` 行，每行若干个整数（空格分隔）或 `none`。",
  "- 1 ≤ n ≤ 6\n- 1 ≤ m ≤ 10000",
  lambda: cases("3\n10 30 10000", "1\n5", "2\n6 28", "2\n496 8128",
                "1\n1", "3\n100 500 1000"),
  lambda t: "".join(
      (" ".join(str(x) for x in _perfect(int(m))) or "none") + "\n"
      for m in t.split()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        int m;
        scanf("%d", &m);
        bool any = false;
        for (int x = 2; x <= m; x++) {
            int s = 1;                        // 1 一定是真因子
            for (int i = 2; i * i <= x; i++) {
                if (x % i == 0) {
                    s += i;
                    if (i != x / i) s += x / i;
                }
            }
            if (s == x) {
                printf(any ? " " : "");
                printf("%d", x);
                any = true;
            }
        }
        if (!any) printf("none");
        printf("\n");
    }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static const int P[] = {6, 28, 496, 8128};     // 10000 以内就这四个
    while (n--) {
        int m;
        scanf("%d", &m);
        bool any = false;
        for (int i = 0; i < 4; i++) {
            if (P[i] <= m) {
                printf(any ? " " : "");
                printf("%d", P[i]);
                any = true;
            }
        }
        if (!any) printf("none");
        printf("\n");
    }
    return 0;
}
''',
  ["C++基础", "循环", "完全数"])

A("【循环】斐波那契数列前 n 项", SEC_LOOP, 1,
  stmt("读入 `n` 个整数 `k`，输出斐波那契数列的前 `k` 项（`F₁ = 1, F₂ = 1`），空格分隔。",
       ["`F(n) = F(n-1) + F(n-2)`，用两个变量滚动即可，不必开数组",
        "`k = 1` 时只输出 `1`；`k = 0` 时输出空行",
        "第 90 项已达 2.88×10¹⁸，`long long` 到第 92 项，本题 `k ≤ 90`"]),
  "第一行 `n`；第二行 `n` 个整数。",
  "`n` 行，每行 `k` 个整数，空格分隔。",
  "- 1 ≤ n ≤ 6\n- 0 ≤ k ≤ 90",
  lambda: cases("3\n1 5 10", "1\n0", "2\n20 30", "1\n90",
                "4\n2 3 4 6", "2\n45 50"),
  lambda t: "".join(" ".join(str(x) for x in _fib(int(k))) + "\n" for k in t.split()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        int k;
        scanf("%d", &k);
        long long a = 1, b = 1;
        for (int i = 1; i <= k; i++) {
            if (i > 1) printf(" ");
            printf("%lld", a);
            long long t = a + b;
            a = b;
            b = t;
        }
        printf("\n");
    }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    long long f[91];
    f[0] = 0; f[1] = 1;
    for (int i = 2; i <= 90; i++) f[i] = f[i - 1] + f[i - 2];   // 先打表
    while (n--) {
        int k;
        scanf("%d", &k);
        for (int i = 1; i <= k; i++) {
            if (i > 1) printf(" ");
            printf("%lld", f[i]);
        }
        printf("\n");
    }
    return 0;
}
''',
  ["C++基础", "循环", "斐波那契"])

A("【循环】整数反转", SEC_LOOP, 2,
  stmt("读入 `n` 个整数，输出它们**数字顺序反转**后的结果。\n\n"
       "负数保留负号；反转后前导的 0 不输出（`1200` 反转成 `21`）。",
       ["`rev = rev * 10 + x % 10; x /= 10;` 是标准写法",
        "先取绝对值再反转，最后补负号，避免负数取模的符号问题",
        "`x = 0` 输出 0；反转后可能溢出 `int`（如 2147483647 反转成 7463847412），用 `long long`"]),
  "第一行 `n`；第二行 `n` 个整数。",
  "`n` 行，每行一个整数。",
  "- 1 ≤ n ≤ 6\n- -10⁹ ≤ x ≤ 10⁹",
  lambda: cases("4\n123 1200 -456 0", "1\n-1", "3\n2147483647 -2147483647 1000000000",
                "2\n10 100", "1\n9", "3\n1000000000 -1200 123456789"),
  lambda t: "".join("%d\n" % _rev(int(x)) for x in t.split()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        long long x;
        scanf("%lld", &x);
        bool neg = x < 0;
        if (neg) x = -x;
        long long r = 0;
        while (x) { r = r * 10 + x % 10; x /= 10; }
        printf("%lld\n", neg ? -r : r);
    }
    return 0;
}
''',
  r'''#include <cstdio>
#include <cstring>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        char buf[32];
        scanf("%s", buf);                 // 当字符串处理，天然去掉前导 0
        int len = (int)strlen(buf), i = 0;
        bool neg = (buf[0] == '-');
        if (neg) i = 1;
        printf(neg ? "-" : "");
        while (len > i && buf[len - 1] == '0') len--;   // 掐掉尾部的 0
        for (int k = len - 1; k >= i; k--) printf("%c", buf[k]);
        if (len == i) printf("0");
        printf("\n");
    }
    return 0;
}
''',
  ["C++基础", "循环", "数字反转"])

A("【循环】位数统计与数位之和", SEC_LOOP, 2,
  stmt("读入 `n` 个非负整数，输出两个数：它的**位数**和**各位数字之和**，空格分隔。",
       ["`x = 0` 是 1 位数，和为 0 —— 这是最容易漏的边界",
        "`x /= 10` 直到 0，循环次数就是位数",
        "先转成字符串数长度也可以"]),
  "第一行 `n`；第二行 `n` 个非负整数。",
  "`n` 行，每行 `位数 各位和`。",
  "- 1 ≤ n ≤ 6\n- 0 ≤ x ≤ 10¹²",
  lambda: cases("4\n0 7 12345 1000000000000", "1\n10", "3\n9 99 999",
                "2\n100 1000", "1\n987654321", "3\n1 12 123"),
  lambda t: "".join("%d %d\n" % (len(str(int(x))), sum(int(ch) for ch in str(int(x))))
                    for x in t.split()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        long long x;
        scanf("%lld", &x);
        int cnt = 0, sum = 0;
        if (x == 0) { cnt = 1; }          // 0 是 1 位数
        while (x > 0) { cnt++; sum += (int)(x % 10); x /= 10; }
        printf("%d %d\n", cnt, sum);
    }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        char buf[32];
        scanf("%s", buf);
        int cnt = 0, sum = 0;
        for (int i = 0; buf[i]; i++) {
            cnt++;
            sum += buf[i] - '0';
        }
        printf("%d %d\n", cnt, sum);
    }
    return 0;
}
''',
  ["C++基础", "循环", "数位"])

A("【循环】十进制转二进制", SEC_LOOP, 2,
  stmt("读入 `n` 个非负整数，输出它们的二进制表示（不带 `0b` 前缀，无前导 0）。",
       ["除 2 取余、逆序排列；也可以从高位到低位用 `>>` 和 `&`",
        "`0` 的答案是 `0`，不要输出空行",
        "位数最多 40 位，用 `long long` 或 `unsigned long long`"]),
  "第一行 `n`；第二行 `n` 个非负整数。",
  "`n` 行，每行一个 01 串。",
  "- 1 ≤ n ≤ 6\n- 0 ≤ x ≤ 10¹²",
  lambda: cases("3\n0 5 10", "1\n1", "4\n255 1024 1000000000000 7",
                "2\n2147483647 4294967295", "1\n2", "3\n3 4 8"),
  lambda t: "".join("%s\n" % bin(int(x))[2:] for x in t.split()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        long long x;
        scanf("%lld", &x);
        char b[64];
        int len = 0;
        if (x == 0) b[len++] = '0';
        while (x) { b[len++] = (char)('0' + x % 2); x /= 2; }
        for (int i = len - 1; i >= 0; i--) printf("%c", b[i]);   // 逆序输出
        printf("\n");
    }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        unsigned long long x;
        scanf("%llu", &x);
        if (x == 0) { printf("0\n"); continue; }
        int top = 63;
        while (top > 0 && ((x >> top) & 1ULL) == 0) top--;   // 找最高位
        for (int i = top; i >= 0; i--) printf("%d", (int)((x >> i) & 1ULL));
        printf("\n");
    }
    return 0;
}
''',
  ["C++基础", "循环", "进制转换"])

A("【循环】自然常数 e 的近似值", SEC_LOOP, 3,
  stmt("读入 `n` 个项数 `k`，用下面的级数算 `e` 的近似值（保留 4 位小数）：\n\n"
       "```\ne = 1/0! + 1/1! + 1/2! + ... + 1/k!\n```\n\n"
       "也就是累加**前 k+1 项**（k = 0 时只有 1）。",
       ["用 `t = t / i` 递推每一项，别每项都重算阶乘（会爆）",
        "累加变量用 `double`，从 `1.0` 起",
        "`k` 大到 15 以后，再加的项小于 1e-13，对 4 位小数已无影响"]),
  "第一行 `n`；第二行 `n` 个非负整数。",
  "`n` 行，每行一个四位小数。",
  "- 1 ≤ n ≤ 6\n- 0 ≤ k ≤ 15",
  lambda: cases("3\n0 1 5", "1\n10", "2\n15 3", "1\n2", "2\n8 12", "1\n4"),
  lambda t: "".join("%.4f\n" % _e_approx(int(k)) for k in t.split()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        int k;
        scanf("%d", &k);
        double sum = 1.0, term = 1.0;
        for (int i = 1; i <= k; i++) {
            term /= i;                 // 逐项递推 1/i!
            sum += term;
        }
        printf("%.4f\n", sum);
    }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        int k;
        scanf("%d", &k);
        double fact = 1.0, sum = 1.0;
        for (int i = 1; i <= k; i++) {
            fact *= i;                 // 老老实实算阶乘
            sum += 1.0 / fact;
        }
        printf("%.4f\n", sum);
    }
    return 0;
}
''',
  ["C++基础", "循环", "级数", "浮点"])

A("【循环】莱布尼茨级数求 π", SEC_LOOP, 3,
  stmt("用莱布尼茨级数计算 `π` 的近似值：\n\n"
       "```\nπ/4 = 1 - 1/3 + 1/5 - 1/7 + ...\n```\n\n"
       "读入 `n` 个项数 `k`，取级数**前 k 项**，输出 `π` 的近似值（保留 4 位小数）。",
       ["符号在每项后翻一次：`sign = -sign`",
        "分母是 `2*i + 1`（i 从 0 开始），别写成 `2*i - 1` 而漏掉第一项 1",
        "k 越大收敛越慢：k = 1000 才到 3.1406，别以为是精度问题"]),
  "第一行 `n`；第二行 `n` 个正整数。",
  "`n` 行，每行一个四位小数。",
  "- 1 ≤ n ≤ 6\n- 1 ≤ k ≤ 100000",
  lambda: cases("3\n1 2 10", "1\n1000", "2\n10000 100000",
                "2\n5 50", "1\n3", "2\n500 5000"),
  lambda t: "".join("%.4f\n" % _pi_approx(int(k)) for k in t.split()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        int k;
        scanf("%d", &k);
        double s = 0.0;
        int sign = 1;
        for (int i = 0; i < k; i++) {
            s += sign / (2.0 * i + 1.0);
            sign = -sign;
        }
        printf("%.4f\n", s * 4.0);
    }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        int k;
        scanf("%d", &k);
        double s = 0.0;
        for (int i = 0; i < k; i++) {
            double t = 1.0 / (2.0 * i + 1.0);
            if (i % 2 == 1) t = -t;      // 偶数项为正、奇数项为负
            s += t;
        }
        printf("%.4f\n", s * 4.0);
    }
    return 0;
}
''',
  ["C++基础", "循环", "级数", "π"])

A("【循环】整数平方根", SEC_LOOP, 2,
  stmt("读入 `n` 个非负整数，输出 `floor(sqrt(x))` —— 也就是**不超过真实平方根的最大整数**。\n\n"
       "**不许调用 `sqrt()`**，请用循环或二分自己求。",
       ["`while ((r+1)*(r+1) <= x) r++;` 是最直观的写法，但对 10¹² 太慢",
        "改成二分：`lo = 0, hi = 10⁶+1`，找最后一个 `mid*mid <= x`",
        "`mid * mid` 要用 `long long`，`int` 在 46341² 就溢出"]),
  "第一行 `n`；第二行 `n` 个非负整数。",
  "`n` 行，每行一个整数。",
  "- 1 ≤ n ≤ 6\n- 0 ≤ x ≤ 10¹²",
  lambda: cases("4\n0 1 15 16", "1\n1000000000000", "3\n2 3 4",
                "2\n999999999999 1000000", "1\n26", "2\n99 100"),
  lambda t: "".join("%d\n" % _isqrt(int(x)) for x in t.split()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        long long x;
        scanf("%lld", &x);
        long long lo = 0, hi = 1000001;
        while (lo + 1 < hi) {                  // 二分找上界
            long long mid = (lo + hi) / 2;
            if (mid * mid <= x) lo = mid;
            else hi = mid;
        }
        printf("%lld\n", lo);
    }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        long long x;
        scanf("%lld", &x);
        long long r = 0;
        while ((r + 1) * (r + 1) <= x) r++;    // 逐步加一
        printf("%lld\n", r);
    }
    return 0;
}
''',
  ["C++基础", "循环", "二分", "平方根"])

A("【循环】角谷猜想的步数", SEC_LOOP, 2,
  stmt("对正整数 `x` 反复做：偶数除以 2，奇数乘 3 加 1，直到变成 1。输出所需的**步数**。\n\n"
       "读入 `n` 个正整数，每行输出一个步数。",
       ["用 `while (x != 1)`，每次改 `x` 并让计数加一",
        "奇数的 `3x+1` 可能超 `int`（如 10⁹ 级），用 `long long`",
        "`x = 1` 时步数是 0，循环一次都不进"]),
  "第一行 `n`；第二行 `n` 个正整数。",
  "`n` 行，每行一个整数。",
  "- 1 ≤ n ≤ 6\n- 1 ≤ x ≤ 10⁶",
  lambda: cases("4\n1 2 3 6", "1\n27", "3\n97 871 77031",
                "2\n1000000 999999", "1\n7", "2\n10 20"),
  lambda t: "".join("%d\n" % _collatz(int(x)) for x in t.split()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        long long x;
        scanf("%lld", &x);
        int step = 0;
        while (x != 1) {
            x = (x % 2 == 0) ? x / 2 : x * 3 + 1;
            step++;
        }
        printf("%d\n", step);
    }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        long long x;
        scanf("%lld", &x);
        int step = 0;
        while (x > 1) {
            if (x & 1) x = 3 * x + 1;      // 用位与判奇偶
            else       x >>= 1;            // 右移等价于除 2
            step++;
        }
        printf("%d\n", step);
    }
    return 0;
}
''',
  ["C++基础", "循环", "角谷猜想"])

A("【循环】1! 到 n! 的和", SEC_LOOP, 3,
  stmt("读入 `n` 个整数 `k`（0 ≤ k ≤ 20），输出 `1! + 2! + ... + k!`。\n\n"
       "`k = 0` 时和为 0。",
       ["边算阶乘边累加，复用上一次的阶乘结果，不要每项重算",
        "`20! ≈ 2.43×10¹⁸`，累加和约 `2.56×10¹⁸`，`long long` 装得下",
        "用 `int` 会在 13! 处就错"]),
  "第一行 `n`；第二行 `n` 个整数。",
  "`n` 行，每行一个整数。",
  "- 1 ≤ n ≤ 6\n- 0 ≤ k ≤ 20",
  lambda: cases("3\n0 1 5", "1\n20", "2\n10 13", "3\n2 3 4", "1\n19", "2\n15 16"),
  lambda t: "".join("%d\n" % _fact_sum(int(k)) for k in t.split()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        int k;
        scanf("%d", &k);
        long long f = 1, s = 0;
        for (int i = 1; i <= k; i++) {
            f *= i;             // 复用上一次的阶乘
            s += f;
        }
        printf("%lld\n", s);
    }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    long long pref[21];
    pref[0] = 0;
    long long f = 1;
    for (int i = 1; i <= 20; i++) { f *= i; pref[i] = pref[i - 1] + f; }  // 打表
    while (n--) {
        int k;
        scanf("%d", &k);
        printf("%lld\n", pref[k]);
    }
    return 0;
}
''',
  ["C++基础", "循环", "阶乘求和"])


# ===================================================================== #
#  SEC_FIG · 嵌套循环与图形（12 题）
# ===================================================================== #

A("【图形】九九乘法表", SEC_FIG, 1,
  stmt("输出标准的下三角九九乘法表：第 `i` 行有 `i` 个式子，形如 `1*3=3 2*3=6 3*3=9`。\n\n"
       "**式子之间一个空格，行末不能有多余空格**，共 9 行。",
       ["外层 `i` 从 1 到 9，内层 `j` 从 1 到 `i`",
        "行末多打一个空格是本题最常见失分点：用 `if (j > 1) printf(\" \")` 控制",
        "乘号是小写字母 `*`，等号两边没有空格"]),
  "无输入。",
  "9 行，第 `i` 行 `i` 个式子。",
  "- 固定输出，无输入\n- 式子格式 `j*i=积`",
  lambda: cases("", "", "", "", "", ""),
  lambda t: "".join(" ".join("%d*%d=%d" % (j, i, i * j) for j in range(1, i + 1)) + "\n"
                    for i in range(1, 10)),
  r'''#include <cstdio>
int main() {
    for (int i = 1; i <= 9; i++) {
        for (int j = 1; j <= i; j++) {
            if (j > 1) printf(" ");          // 空格打在前面，行末就干净
            printf("%d*%d=%d", j, i, i * j);
        }
        printf("\n");
    }
    return 0;
}
''',
  r'''#include <iostream>
using namespace std;
int main() {
    for (int i = 1; i <= 9; i++) {
        for (int j = 1; j <= i; j++) {
            cout << j << "*" << i << "=" << i * j;
            if (j != i) cout << " ";
        }
        cout << "\n";
    }
    return 0;
}
''',
  ["C++基础", "嵌套循环", "乘法表"])

A("【图形】直角三角形星号", SEC_FIG, 1,
  stmt("读入 `n` 个整数 `h`，输出高为 `h` 的直角三角形，第 `i` 行有 `i` 个 `*`。\n\n"
       "每行末尾**不能有空格**，行之间不能有空行。",
       ["外层控制行，内层控制这一行打几个星号",
        "本题不需要打前导空格 —— 加了对不齐",
        "`h = 0` 时什么都不输出（连空行也没有）"]),
  "第一行 `n`；第二行 `n` 个整数。",
  "对每个 `h`，输出 `h` 行。",
  "- 1 ≤ n ≤ 6\n- 1 ≤ h ≤ 30",
  lambda: cases("3\n1 3 5", "1\n1", "2\n2 4", "1\n10", "2\n6 7", "1\n30"),
  lambda t: "".join("*" * i + "\n" for h in t.split()[1:]
                    for i in range(1, int(h) + 1)),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        int h;
        scanf("%d", &h);
        for (int i = 1; i <= h; i++) {
            for (int j = 0; j < i; j++) printf("*");
            printf("\n");
        }
    }
    return 0;
}
''',
  r'''#include <iostream>
#include <string>
using namespace std;
int main() {
    int n;
    cin >> n;
    while (n--) {
        int h;
        cin >> h;
        for (int i = 1; i <= h; i++) cout << string(i, '*') << "\n";
    }
    return 0;
}
''',
  ["C++基础", "嵌套循环", "直角三角形"])

A("【图形】等腰三角形星号", SEC_FIG, 2,
  stmt("读入 `n` 个整数 `h`，输出高为 `h` 的等腰三角形：第 `i` 行先打 `h-i` 个空格，"
       "再打 `2i-1` 个 `*`。\n\n"
       "**每行末尾不能有多余空格**。",
       ["空格数 = `h - i`，星号数 = `2*i - 1`",
        "两个内层循环：一个打空格，一个打星号",
        "行末的星号后面不要再补空格"]),
  "第一行 `n`；第二行 `n` 个整数。",
  "对每个 `h`，输出 `h` 行。",
  "- 1 ≤ n ≤ 6\n- 1 ≤ h ≤ 30",
  lambda: cases("3\n1 3 5", "1\n2", "2\n4 6", "1\n10", "2\n8 9", "1\n15"),
  lambda t: "".join(" " * (int(h) - i) + "*" * (2 * i - 1) + "\n"
                    for h in t.split()[1:] for i in range(1, int(h) + 1)),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        int h;
        scanf("%d", &h);
        for (int i = 1; i <= h; i++) {
            for (int j = 0; j < h - i; j++) printf(" ");
            for (int j = 0; j < 2 * i - 1; j++) printf("*");
            printf("\n");
        }
    }
    return 0;
}
''',
  r'''#include <iostream>
#include <string>
using namespace std;
int main() {
    int n;
    cin >> n;
    while (n--) {
        int h;
        cin >> h;
        for (int i = 1; i <= h; i++)
            cout << string(h - i, ' ') << string(2 * i - 1, '*') << "\n";
    }
    return 0;
}
''',
  ["C++基础", "嵌套循环", "等腰三角形"])

A("【图形】实心菱形", SEC_FIG, 3,
  stmt("读入 `n` 个**奇数** `h`，输出高为 `h` 的实心菱形。\n\n"
       "上半（含中间行）第 `i` 行：`h/2+1-i` 个空格 + `2i-1` 个 `*`；\n"
       "下半第 `i` 行：`i` 个空格 + `h-2i` 个 `*`。",
       ["菱形 = 上半 `(h+1)/2` 行 + 下半 `h/2` 行，两段分开写最清楚",
        "下半的空格从 1 开始递增，星号从 `h-2` 开始递减",
        "`h = 1` 时只有一行一个星号"]),
  "第一行 `n`；第二行 `n` 个奇数。",
  "对每个 `h`，输出 `h` 行。",
  "- 1 ≤ n ≤ 6\n- 1 ≤ h ≤ 31，h 为奇数",
  lambda: cases("3\n1 3 5", "1\n7", "2\n9 11", "1\n21", "2\n13 15", "1\n31"),
  lambda t: "".join(_diamond(int(h)) for h in t.split()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        int h;
        scanf("%d", &h);
        int up = (h + 1) / 2;
        for (int i = 1; i <= up; i++) {              // 上半 + 中间行
            for (int j = 0; j < up - i; j++) printf(" ");
            for (int j = 0; j < 2 * i - 1; j++) printf("*");
            printf("\n");
        }
        for (int i = 1; i <= h / 2; i++) {           // 下半
            for (int j = 0; j < i; j++) printf(" ");
            for (int j = 0; j < h - 2 * i; j++) printf("*");
            printf("\n");
        }
    }
    return 0;
}
''',
  r'''#include <iostream>
#include <string>
using namespace std;
int main() {
    int n;
    cin >> n;
    while (n--) {
        int h;
        cin >> h;
        int up = (h + 1) / 2;
        for (int i = 1; i <= up; i++)
            cout << string(up - i, ' ') << string(2 * i - 1, '*') << "\n";
        for (int i = 1; i <= h / 2; i++)
            cout << string(i, ' ') << string(h - 2 * i, '*') << "\n";
    }
    return 0;
}
''',
  ["C++基础", "嵌套循环", "菱形"])

A("【图形】空心正方形", SEC_FIG, 2,
  stmt("读入 `n` 个整数 `s`，输出边长为 `s` 的空心正方形：第一行和最后一行是 `s` 个 `*`，"
       "中间各行是 `*` + `s-2` 个空格 + `*`。",
       ["`s = 1` 时只有一行一个 `*`；`s = 2` 时两行都是 `**`（没有中间行）",
        "中间行不能打成 `*` + 空格 + `*` 而忘了宽度",
        "每行末尾无多余空格"]),
  "第一行 `n`；第二行 `n` 个整数。",
  "对每个 `s`，输出 `s` 行。",
  "- 1 ≤ n ≤ 6\n- 1 ≤ s ≤ 20",
  lambda: cases("3\n1 2 4", "1\n3", "2\n5 6", "1\n10", "2\n7 8", "1\n20"),
  lambda t: "".join(_hollow_square(int(s)) for s in t.split()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        int s;
        scanf("%d", &s);
        for (int i = 0; i < s; i++) {
            if (i == 0 || i == s - 1) {              // 上下两行整条
                for (int j = 0; j < s; j++) printf("*");
            } else {
                printf("*");
                for (int j = 0; j < s - 2; j++) printf(" ");
                printf("*");
            }
            printf("\n");
        }
    }
    return 0;
}
''',
  r'''#include <iostream>
#include <string>
using namespace std;
int main() {
    int n;
    cin >> n;
    while (n--) {
        int s;
        cin >> s;
        string full(s, '*');
        string mid = "*" + string(s > 2 ? s - 2 : 0, ' ') + (s > 1 ? "*" : "");
        cout << full << "\n";
        for (int i = 1; i < s - 1; i++) cout << mid << "\n";
        if (s > 1) cout << full << "\n";
    }
    return 0;
}
''',
  ["C++基础", "嵌套循环", "空心正方形"])

A("【图形】数字直角三角形", SEC_FIG, 2,
  stmt("读入 `n` 个整数 `h`，输出高为 `h` 的数字三角形：\n\n"
       "第 `i` 行先打 `h-i` 个空格，再依次打 `1` 到 `i`（不加分隔符）。",
       ["先空格后数字，两个内层循环",
        "数字之间没有空格，是连续的 `123...i`",
        "`h = 3` 时输出 `  1` / ` 12` / `123`"]),
  "第一行 `n`；第二行 `n` 个整数。",
  "对每个 `h`，输出 `h` 行。",
  "- 1 ≤ n ≤ 6\n- 1 ≤ h ≤ 9",
  lambda: cases("3\n1 3 5", "1\n9", "2\n2 4", "1\n6", "2\n7 8", "1\n5"),
  lambda t: "".join(" " * (int(h) - i) + "".join(str(d) for d in range(1, i + 1)) + "\n"
                    for h in t.split()[1:] for i in range(1, int(h) + 1)),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        int h;
        scanf("%d", &h);
        for (int i = 1; i <= h; i++) {
            for (int j = 0; j < h - i; j++) printf(" ");
            for (int j = 1; j <= i; j++) printf("%d", j);
            printf("\n");
        }
    }
    return 0;
}
''',
  r'''#include <iostream>
#include <string>
using namespace std;
int main() {
    int n;
    cin >> n;
    while (n--) {
        int h;
        cin >> h;
        string digits = "123456789";
        for (int i = 1; i <= h; i++)
            cout << string(h - i, ' ') << digits.substr(0, i) << "\n";
    }
    return 0;
}
''',
  ["C++基础", "嵌套循环", "数字三角形"])

A("【图形】杨辉三角前 n 行", SEC_FIG, 3,
  stmt("读入 `n` 个整数 `k`，输出杨辉三角的前 `k` 行。每行数字之间**一个空格**，行首无空格。\n\n"
       "例如 `k = 5`：\n\n```\n1\n1 1\n1 2 1\n1 3 3 1\n1 4 6 4 1\n```",
       ["`a[i][j] = a[i-1][j-1] + a[i-1][j]`，边界 `a[i][0] = a[i][i] = 1`",
        "用一维数组从后往前推也行：`a[j] += a[j-1]`",
        "第 30 行中间的数约 1.4×10⁸，`int` 够；第 34 行才会超"]),
  "第一行 `n`；第二行 `n` 个整数。",
  "对每个 `k`，输出 `k` 行。",
  "- 1 ≤ n ≤ 6\n- 1 ≤ k ≤ 30",
  lambda: cases("3\n1 2 5", "1\n10", "2\n6 7", "1\n20", "2\n3 4", "1\n30"),
  lambda t: "".join("".join(" ".join(str(v) for v in row) + "\n" for row in _yang(int(k)))
                    for k in t.split()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        int k;
        scanf("%d", &k);
        long long a[32][32] = {0};
        for (int i = 0; i < k; i++) {
            a[i][0] = a[i][i] = 1;                    // 两边是 1
            for (int j = 1; j < i; j++)
                a[i][j] = a[i - 1][j - 1] + a[i - 1][j];
            for (int j = 0; j <= i; j++) {
                if (j) printf(" ");
                printf("%lld", a[i][j]);
            }
            printf("\n");
        }
    }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        int k;
        scanf("%d", &k);
        long long a[32] = {0};
        a[0] = 1;
        for (int i = 0; i < k; i++) {
            for (int j = i; j >= 1; j--) a[j] += a[j - 1];   // 一维从后往前推
            for (int j = 0; j <= i; j++) {
                if (j) printf(" ");
                printf("%lld", a[j]);
            }
            printf("\n");
        }
    }
    return 0;
}
''',
  ["C++基础", "嵌套循环", "杨辉三角", "二维数组"])

A("【图形】100 以内素数（每行 5 个）", SEC_FIG, 2,
  stmt("输出 100 以内的全部素数，**每行 5 个**，数字之间一个空格，最后一行不足 5 个就照常结束。",
       ["先判素数，再控制换行：`if (cnt % 5 == 0) printf(\"\\n\")`",
        "计数器从 0 开始，每输出一个加一",
        "行末不要多打空格"]),
  "无输入。",
  "若干行，每行至多 5 个整数。",
  "- 固定输出，无输入\n- 2 ~ 100 之间的素数",
  lambda: cases("", "", "", "", "", ""),
  lambda t: _primes_grid(),
  r'''#include <cstdio>
int main() {
    int cnt = 0;
    for (int x = 2; x <= 100; x++) {
        bool ok = true;
        for (int i = 2; i * i <= x; i++)
            if (x % i == 0) { ok = false; break; }
        if (!ok) continue;
        if (cnt % 5 == 0) { if (cnt) printf("\n"); }
        else printf(" ");
        printf("%d", x);
        cnt++;
    }
    printf("\n");
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int p[30], m = 0;
    for (int x = 2; x <= 100; x++) {              // 先收集
        bool ok = true;
        for (int i = 2; i * i <= x; i++) if (x % i == 0) { ok = false; break; }
        if (ok) p[m++] = x;
    }
    for (int i = 0; i < m; i++) {                 // 再排版
        if (i % 5 == 0) { if (i) printf("\n"); }
        else printf(" ");
        printf("%d", p[i]);
    }
    printf("\n");
    return 0;
}
''',
  ["C++基础", "嵌套循环", "素数", "排版"])

A("【图形】三位水仙花数（全部）", SEC_FIG, 2,
  stmt("输出所有三位水仙花数（各位数字立方和等于自身），一行内空格分隔。",
       ["枚举 100~999，拆出百十个位再验算",
        "结果只有 4 个，别漏 407",
        "行末无空格"]),
  "无输入。",
  "一行，若干个整数（空格分隔）。",
  "- 固定输出，无输入\n- 三位数范围",
  lambda: cases("", "", "", "", "", ""),
  lambda t: " ".join(str(x) for x in range(100, 1000)
                     if sum(int(c) ** 3 for c in str(x)) == x) + "\n",
  r'''#include <cstdio>
int main() {
    bool first = true;
    for (int x = 100; x <= 999; x++) {
        int a = x / 100, b = x / 10 % 10, c = x % 10;
        if (a * a * a + b * b * b + c * c * c != x) continue;
        if (!first) printf(" ");
        printf("%d", x);
        first = false;
    }
    printf("\n");
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int res[16], m = 0;
    for (int a = 1; a <= 9; a++)          // 直接枚举三个数字，不用拆位
        for (int b = 0; b <= 9; b++)
            for (int c = 0; c <= 9; c++) {
                int x = a * 100 + b * 10 + c;
                if (a * a * a + b * b * b + c * c * c == x) res[m++] = x;
            }
    for (int i = 0; i < m; i++) {
        if (i) printf(" ");               // 空格打在前头，行末才干净
        printf("%d", res[i]);
    }
    printf("\n");
    return 0;
}
''',
  ["C++基础", "嵌套循环", "水仙花数"])

A("【图形】字母倒三角", SEC_FIG, 2,
  stmt("读入 `n` 个整数 `h`，每行从 `A` 开始连续输出字母：第一行 `h` 个，第二行 `h-1` 个，…，最后一行 1 个。\n\n"
       "例如 `h = 3`：`ABC` / `AB` / `A`。",
       ["第 `i` 行输出前 `h-i+1` 个字母",
        "字符用 `printf(\"%c\", 'A' + k)` 生成，不要手写 26 个 case",
        "`h ≤ 26`，超过 26 个字母本题不涉及"]),
  "第一行 `n`；第二行 `n` 个整数。",
  "对每个 `h`，输出 `h` 行。",
  "- 1 ≤ n ≤ 6\n- 1 ≤ h ≤ 26",
  lambda: cases("3\n1 3 5", "1\n26", "2\n2 4", "1\n13", "2\n6 7", "1\n20"),
  lambda t: "".join("".join(chr(65 + k) for k in range(int(h) - i + 1)) + "\n"
                    for h in t.split()[1:] for i in range(1, int(h) + 1)),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        int h;
        scanf("%d", &h);
        for (int i = 1; i <= h; i++) {
            for (int k = 0; k <= h - i; k++) printf("%c", 'A' + k);
            printf("\n");
        }
    }
    return 0;
}
''',
  r'''#include <iostream>
#include <string>
using namespace std;
int main() {
    int n;
    cin >> n;
    string letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    while (n--) {
        int h;
        cin >> h;
        for (int i = h; i >= 1; i--) cout << letters.substr(0, i) << "\n";
    }
    return 0;
}
''',
  ["C++基础", "嵌套循环", "字符"])

A("【图形】蛇形数字方阵", SEC_FIG, 3,
  stmt("读入 `n` 个整数 `s`，输出 `s×s` 的方阵：从 1 开始按**蛇形**填数 ——\n\n"
       "第 1 行从左到右，第 2 行从右到左，第 3 行从左到右，以此类推。\n\n"
       "数字之间一个空格，行末无空格。",
       ["偶数行（下标 1、3、5…）反向填：`a[i][j] = s*s - i*s + (s-j)`？不如直接反向循环",
        "用一个递增计数器 `v`，按行方向决定内层从 0 到 s-1 还是从 s-1 到 0",
        "`s = 1` 时只有 `1`"]),
  "第一行 `n`；第二行 `n` 个整数。",
  "对每个 `s`，输出 `s` 行。",
  "- 1 ≤ n ≤ 6\n- 1 ≤ s ≤ 15",
  lambda: cases("3\n1 2 3", "1\n4", "2\n5 6", "1\n10", "2\n7 8", "1\n15"),
  lambda t: "".join(_snake(int(s)) for s in t.split()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        int s;
        scanf("%d", &s);
        int v = 1;
        for (int i = 0; i < s; i++) {
            if (i % 2 == 0) {                       // 偶数行正着来
                for (int j = 0; j < s; j++) {
                    if (j) printf(" ");
                    printf("%d", v++);
                }
            } else {                                // 奇数行反着来
                int start = v + s - 1;
                for (int j = 0; j < s; j++) {
                    if (j) printf(" ");
                    printf("%d", start - j);
                }
                v += s;
            }
            printf("\n");
        }
    }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        int s;
        scanf("%d", &s);
        int a[16][16], v = 1;
        for (int i = 0; i < s; i++) {
            int dir = (i % 2 == 0) ? 1 : -1;
            int j = (dir == 1) ? 0 : s - 1;
            for (int t = 0; t < s; t++) {           // 先填进数组
                a[i][j] = v++;
                j += dir;
            }
        }
        for (int i = 0; i < s; i++) {               // 再统一打印
            for (int j = 0; j < s; j++) {
                if (j) printf(" ");
                printf("%d", a[i][j]);
            }
            printf("\n");
        }
    }
    return 0;
}
''',
  ["C++基础", "嵌套循环", "二维数组", "模拟"])

A("【图形】空心菱形", SEC_FIG, 4,
  stmt("读入 `n` 个**奇数** `h`，输出高为 `h` 的空心菱形：只有轮廓是 `*`，内部是空格。\n\n"
       "第 `i` 行（从上到下）只有在**最左**和**最右**的星号位置打 `*`，中间全空格；"
       "顶端和底端各只有一个 `*`。\n\n"
       "**行末的星号之后不能补空格**。",
       ["先算出每行宽度 `w`，再决定第一个和最后一个 `*` 的列号",
        "上半第 `i` 行：左星号在 `up-i`，右星号在 `up+i-2`（均从 0 计）",
        "下半与上半镜像：左星号在 `i`，右星号在 `h-i-1`",
        "首尾行左右星号重合，只打一个"]),
  "第一行 `n`；第二行 `n` 个奇数。",
  "对每个 `h`，输出 `h` 行。",
  "- 1 ≤ n ≤ 6\n- 1 ≤ h ≤ 31，h 为奇数",
  lambda: cases("3\n1 3 5", "1\n7", "2\n9 11", "1\n21", "2\n13 15", "1\n31"),
  lambda t: "".join(_hollow_diamond(int(h)) for h in t.split()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        int h;
        scanf("%d", &h);
        int up = (h + 1) / 2;
        for (int i = 1; i <= h; i++) {
            int width = (i <= up) ? (2 * i - 1) : (2 * (h - i) + 1);  // 该行星号跨度
            int pad = (h - width) / 2;                                // 左侧空格
            for (int j = 0; j < pad; j++) printf(" ");
            printf("*");
            if (width > 1) {
                for (int j = 0; j < width - 2; j++) printf(" ");
                printf("*");
            }
            printf("\n");
        }
    }
    return 0;
}
''',
  r'''#include <cstdio>
#include <cstring>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        int h;
        scanf("%d", &h);
        char line[64];
        int up = (h + 1) / 2;
        for (int i = 0; i < h; i++) {                // 先造一整行空格，再点两个星
            int width = (i < up) ? (2 * (i + 1) - 1) : (2 * (h - i) - 1);
            int pad = (h - width) / 2;
            for (int j = 0; j < pad + width; j++) line[j] = ' ';
            line[pad] = '*';
            line[pad + width - 1] = '*';
            line[pad + width] = '\0';
            printf("%s\n", line);
        }
    }
    return 0;
}
''',
  ["C++基础", "嵌套循环", "空心菱形"])


# ===================================================================== #
#  本地辅助
# ===================================================================== #
def _fact(x: int) -> int:
    r = 1
    for i in range(2, x + 1):
        r *= i
    return r


def _fact_sum(k: int) -> int:
    f, s = 1, 0
    for i in range(1, k + 1):
        f *= i
        s += f
    return s


def _gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def _lcm(a: int, b: int) -> int:
    return a // _gcd(a, b) * b


def _isprime(x: int) -> bool:
    if x < 2:
        return False
    i = 2
    while i * i <= x:
        if x % i == 0:
            return False
        i += 1
    return True


def _factor(x: int) -> str:
    out = []
    d = 2
    while d * d <= x:
        while x % d == 0:
            out.append(d)
            x //= d
        d += 1
    if x > 1:
        out.append(x)
    return "*".join(str(v) for v in out) + "\n"


def _perfect(m: int) -> list[int]:
    res = []
    for x in range(2, m + 1):
        s = 0
        for i in range(1, x):
            if x % i == 0:
                s += i
        if s == x:
            res.append(x)
    return res


def _fib(k: int) -> list[int]:
    a, b = 1, 1
    out = []
    for _ in range(k):
        out.append(a)
        a, b = b, a + b
    return out


def _rev(x: int) -> int:
    neg = x < 0
    x = abs(x)
    r = 0
    while x:
        r = r * 10 + x % 10
        x //= 10
    return -r if neg else r


def _e_approx(k: int) -> float:
    s, term = 1.0, 1.0
    for i in range(1, k + 1):
        term /= i
        s += term
    return s


def _pi_approx(k: int) -> float:
    s = 0.0
    sign = 1
    for i in range(k):
        s += sign / (2.0 * i + 1.0)
        sign = -sign
    return s * 4.0


def _isqrt(x: int) -> int:
    r = 0
    while (r + 1) * (r + 1) <= x:
        r += 1
    return r


def _collatz(x: int) -> int:
    step = 0
    while x != 1:
        x = x // 2 if x % 2 == 0 else x * 3 + 1
        step += 1
    return step


def _diamond(h: int) -> str:
    up = (h + 1) // 2
    out = []
    for i in range(1, up + 1):
        out.append(" " * (up - i) + "*" * (2 * i - 1) + "\n")
    for i in range(1, h // 2 + 1):
        out.append(" " * i + "*" * (h - 2 * i) + "\n")
    return "".join(out)


def _hollow_square(s: int) -> str:
    out = []
    for i in range(s):
        if i == 0 or i == s - 1:
            out.append("*" * s + "\n")
        else:
            out.append("*" + " " * (s - 2) + "*\n")
    return "".join(out)


def _yang(k: int) -> list[list[int]]:
    rows = []
    for i in range(k):
        row = [1] * (i + 1)
        for j in range(1, i):
            row[j] = rows[i - 1][j - 1] + rows[i - 1][j]
        rows.append(row)
    return rows


def _primes_grid() -> str:
    ps = [x for x in range(2, 101) if _isprime(x)]
    out = []
    for i in range(0, len(ps), 5):
        out.append(" ".join(str(v) for v in ps[i:i + 5]) + "\n")
    return "".join(out)


def _snake(s: int) -> str:
    out = []
    v = 1
    for i in range(s):
        if i % 2 == 0:
            row = list(range(v, v + s))
        else:
            row = list(range(v + s - 1, v - 1, -1))
        v += s
        out.append(" ".join(str(x) for x in row) + "\n")
    return "".join(out)


def _hollow_diamond(h: int) -> str:
    out = []
    up = (h + 1) // 2
    for i in range(1, h + 1):
        width = 2 * i - 1 if i <= up else 2 * (h - i) + 1
        pad = (h - width) // 2
        if width == 1:
            out.append(" " * pad + "*\n")
        else:
            out.append(" " * pad + "*" + " " * (width - 2) + "*\n")
    return "".join(out)


if __name__ == "__main__":
    raise SystemExit(cli(PROBLEMS, "app/problems_bank_cpp_basic2.py",
                         "C++ 编程题第二册：循环结构 / 嵌套循环与图形（28 题）",
                         "CPP_BASIC2_PROBLEMS"))
