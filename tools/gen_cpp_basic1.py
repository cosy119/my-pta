# -*- coding: utf-8 -*-
"""C++ 基础编程题 · 第 1 册：输入输出（12）+ 运算符（12）+ 分支（12）= 36 题。

对应教材第 02 讲「C++ 简单程序设计」（p18~63）的知识点切分：
  格式化输出 / 整数与浮点运算 / 位运算 / 取模语义 / 关系与逻辑 / if 与 switch。

★ 全部为**编程题**，判题为标准输出逐字节比对。
★ 每题 6 个测试点（前 2 个公开样例），两套 C++ 解必须都过。
★ oracle 一律用 Python 笨办法独立算，不看 C++ 解的结果。

重生成：python tools/gen_cpp_basic1.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cpp_basic_kit import cases, cli, stmt          # noqa: E402

SEC_IO = "C++ 编程 · 输入输出与格式化"
SEC_OP = "C++ 编程 · 运算符与表达式"
SEC_BR = "C++ 编程 · 分支结构"

PROBLEMS: list[dict] = []


def A(title, sec, d, st, inf, outf, con, inp, orc, sol, alt, tags):
    PROBLEMS.append(dict(title=title, section=sec, difficulty=d, statement_md=st,
                         input_format=inf, output_format=outf, constraints_md=con,
                         inputs=inp, oracle=orc, solution=sol, alt=alt, tags=tags))


# ===================================================================== #
#  SEC_IO · 输入输出与格式化（12 题）
# ===================================================================== #

A("【输入输出】两数之和与差", SEC_IO, 1,
  stmt("读入两个整数 `a b`，输出它们的和与差。",
       ["先输出和，再输出差，各占一行",
        "`a - b` 可能为负，别取绝对值"]),
  "一行两个整数 `a b`。",
  "两行：第一行 `a+b`，第二行 `a-b`。",
  "- -10⁹ ≤ a, b ≤ 10⁹\n- 差最大 2×10⁹，仍在 `int` 内，但养成用 `long long` 的习惯更稳",
  lambda: cases("3 5", "0 0", "-7 4", "1000000000 -1000000000", "12 12", "-3 -9"),
  lambda t: "%d\n%d\n" % (lambda a, b: (a + b, a - b))(*map(int, t.split())),
  r'''#include <cstdio>
int main() {
    long long a, b;
    if (scanf("%lld %lld", &a, &b) != 2) return 0;
    printf("%lld\n", a + b);
    printf("%lld\n", a - b);
    return 0;
}
''',
  r'''#include <iostream>
using namespace std;
int main() {
    long long a, b;
    cin >> a >> b;
    cout << a + b << "\n" << a - b << "\n";
    return 0;
}
''',
  ["C++基础", "输入输出", "整数运算"])

A("【输入输出】三数平均值保留两位小数", SEC_IO, 1,
  stmt("读入三个整数，输出它们的算术平均值，保留两位小数。",
       ["`(a+b+c)/3` 在整数上做会**截断**，必须先转 `double`",
        "输出用 `printf(\"%.2f\")` 或 `fixed << setprecision(2)`"]),
  "一行三个整数 `a b c`。",
  "一行，平均值，保留两位小数。",
  "- -1000 ≤ a, b, c ≤ 1000",
  lambda: cases("1 2 3", "10 20 30", "0 0 0", "4 5 2", "1 1 5", "100 100 100"),
  lambda t: "%.2f\n" % (sum(map(int, t.split())) / 3.0),
  r'''#include <cstdio>
int main() {
    int a, b, c;
    if (scanf("%d %d %d", &a, &b, &c) != 3) return 0;
    double avg = (a + b + c) / 3.0;      // 3.0 而非 3，否则先做整除
    printf("%.2f\n", avg);
    return 0;
}
''',
  r'''#include <iostream>
#include <iomanip>
using namespace std;
int main() {
    int a, b, c;
    cin >> a >> b >> c;
    cout << fixed << setprecision(2) << (a + b + c) / 3.0 << "\n";
    return 0;
}
''',
  ["C++基础", "输入输出", "浮点", "类型转换"])

A("【输入输出】交换两个整数", SEC_IO, 1,
  stmt("读入两个整数 `a b`，交换它们的值后输出。",
       ["输出顺序是**先原来的 b，再原来的 a**",
        "用临时变量最稳；异或交换虽然不用临时变量，但对同一变量自交换会清零"]),
  "一行两个整数 `a b`。",
  "一行两个整数：交换后的 `a b`。",
  "- -10⁹ ≤ a, b ≤ 10⁹",
  lambda: cases("3 5", "7 7", "0 -1", "-8 12", "100 200", "2147483647 -2147483648"),
  lambda t: "%d %d\n" % (lambda a, b: (b, a))(*map(int, t.split())),
  r'''#include <cstdio>
int main() {
    long long a, b;
    if (scanf("%lld %lld", &a, &b) != 2) return 0;
    long long t = a;                     // 临时变量，交换
    a = b;
    b = t;
    printf("%lld %lld\n", a, b);
    return 0;
}
''',
  r'''#include <iostream>
#include <utility>
using namespace std;
int main() {
    long long a, b;
    cin >> a >> b;
    swap(a, b);                          // 标准库直接换
    cout << a << " " << b << "\n";
    return 0;
}
''',
  ["C++基础", "输入输出", "交换"])

A("【输入输出】按位宽 8 右对齐输出", SEC_IO, 1,
  stmt("读入 `n` 个整数，每个整数占一行、宽度固定为 8、右对齐（左侧补空格）。",
       ["用 `printf(\"%8d\")` 或 `setw(8)`",
        "`setw` 只对**下一个**输出生效，循环里每次都要写",
        "补的是空格不是 0；补 0 是 `%08d`，那是另一道题"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "`n` 行，每行一个宽度为 8 的整数。",
  "- 1 ≤ n ≤ 6\n- -9999999 ≤ x ≤ 9999999（含负号不超 8 位）",
  lambda: cases("3\n1 22 333", "1\n0", "4\n-1 -22 -333 -4444",
                "2\n1234567 7654321", "5\n9 99 999 9999 99999",
                "6\n1000000 -1000000 5 -5 40 -40"),
  lambda t: "".join("%8d\n" % int(x) for x in t.split()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 0; i < n; i++) {
        int x;
        scanf("%d", &x);
        printf("%8d\n", x);              // 宽度 8 右对齐
    }
    return 0;
}
''',
  r'''#include <iostream>
#include <iomanip>
using namespace std;
int main() {
    int n;
    if (!(cin >> n)) return 0;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        cout << setw(8) << x << "\n";    // setw 到空格为止
    }
    return 0;
}
''',
  ["C++基础", "格式化输出", "setw"])

A("【输入输出】摄氏度转华氏度", SEC_IO, 1,
  stmt("每行一个摄氏温度（整数），转成华氏温度输出，保留一位小数。\n\n"
       "换算公式：`F = C × 9 / 5 + 32`。",
       ["`C * 9 / 5` 在整数里会截断，要写成 `C * 9.0 / 5`",
        "输入行数不定，读到文件末尾为止"]),
  "若干行，每行一个整数摄氏温度。",
  "每行一个华氏温度，保留一位小数。",
  "- -100 ≤ C ≤ 200\n- 行数 ≤ 10",
  lambda: cases("0\n100\n37", "-40", "25\n66", "36\n38",
                "-100 -1 0 1", "10 20 -10 -20 50"),
  lambda t: "".join("%.1f\n" % (int(x) * 9.0 / 5 + 32) for x in t.split()),
  r'''#include <cstdio>
int main() {
    int c;
    while (scanf("%d", &c) == 1) {
        printf("%.1f\n", c * 9.0 / 5 + 32);   // 9.0 保证浮点除法
    }
    return 0;
}
''',
  r'''#include <iostream>
#include <iomanip>
using namespace std;
int main() {
    int c;
    cout << fixed << setprecision(1);
    while (cin >> c) {
        cout << c * 9.0 / 5 + 32 << "\n";
    }
    return 0;
}
''',
  ["C++基础", "格式化输出", "浮点", "EOF"])

A("【输入输出】秒数换算成时分秒", SEC_IO, 1,
  stmt("读入一个非负整数表示的总秒数，换算成 `时 分 秒` 输出。",
       ["一小时 3600 秒、一分 60 秒",
        "秒数可达 10⁹，用 `long long`",
        "三个数之间用一个空格分隔，不足的位不补零"]),
  "一行一个整数 `s`（总秒数）。",
  "一行三个整数 `h m sec`，空格分隔。",
  "- 0 ≤ s ≤ 10¹²",
  lambda: cases("0", "3661", "59", "3600", "86399", "1000000000"),
  lambda t: "%d %d %d\n" % (lambda s: (s // 3600, s % 3600 // 60, s % 60))(*map(int, t.split())),
  r'''#include <cstdio>
int main() {
    long long s;
    if (scanf("%lld", &s) != 1) return 0;
    long long h = s / 3600;
    long long m = s % 3600 / 60;
    long long sec = s % 60;
    printf("%lld %lld %lld\n", h, m, sec);
    return 0;
}
''',
  r'''#include <iostream>
using namespace std;
int main() {
    long long s;
    cin >> s;
    cout << s / 3600 << " " << (s / 60) % 60 << " " << s % 60 << "\n";
    return 0;
}
''',
  ["C++基础", "整除取模", "输入输出"])

A("【输入输出】圆的周长与面积", SEC_IO, 2,
  stmt("读入圆的半径（整数），用 `π = 3.14159` 计算周长与面积，各保留两位小数。\n\n"
       "公式：周长 `2πr`，面积 `πr²`。",
       ["`π` 是常量，别写成变量被后续语句改掉",
        "面积是 `3.14159 * r * r`，不要写成 `3.14159 * r ^ 2`（`^` 在 C++ 里是异或）",
        "两行输出：先周长后面积"]),
  "一行一个整数 `r`。",
  "两行：第一行周长，第二行面积，均保留两位小数。",
  "- 1 ≤ r ≤ 1000",
  lambda: cases("1", "2", "3", "5", "10", "7"),
  lambda t: "%.2f\n%.2f\n" % (lambda r: (2 * 3.14159 * r, 3.14159 * r * r))(*map(int, t.split())),
  r'''#include <cstdio>
const double PI = 3.14159;
int main() {
    int r;
    if (scanf("%d", &r) != 1) return 0;
    printf("%.2f\n", 2 * PI * r);
    printf("%.2f\n", PI * r * r);
    return 0;
}
''',
  r'''#include <iostream>
#include <iomanip>
using namespace std;
#define PI 3.14159
int main() {
    int r;
    cin >> r;
    double area = PI * (double)r * (double)r;
    cout << fixed << setprecision(2);
    cout << 2 * PI * r << "\n" << area << "\n";
    return 0;
}
''',
  ["C++基础", "常量", "格式化输出"])

A("【输入输出】字符的 ASCII 码", SEC_IO, 1,
  stmt("读入 `n` 个用空格分隔的可见字符，逐个输出它们的 ASCII 码。",
       ["`char` 参与算术运算时会自动转成整数，所以 `(int)c` 与 `c` 直接输出不同",
        "用 `scanf(\" %c\")` 读字符：格式串前的空格会跳过空白符，否则会把上一行残留的换行读进来"]),
  "第一行 `n`；第二行 `n` 个字符，空格分隔。",
  "`n` 行，每行一个整数。",
  "- 1 ≤ n ≤ 6\n- 字符均在可见 ASCII 范围内（33~126）",
  lambda: cases("3\nA a 0", "1\nZ", "4\n+ _ 9 ~", "2\n! ?", "5\nb c d e f", "3\nX y 5"),
  lambda t: "".join("%d\n" % ord(c) for c in t.split()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 0; i < n; i++) {
        char c;
        scanf(" %c", &c);            // 前导空格跳过空白符
        printf("%d\n", (int)c);
    }
    return 0;
}
''',
  r'''#include <iostream>
using namespace std;
int main() {
    int n;
    cin >> n;
    for (int i = 0; i < n; i++) {
        char c;
        cin >> c;                    // cin >> char 自动跳过空白
        cout << static_cast<int>(c) << "\n";
    }
    return 0;
}
''',
  ["C++基础", "字符", "ASCII", "类型转换"])

A("【输入输出】各数位之和", SEC_IO, 2,
  stmt("读入 `n` 个整数，逐个输出「它各位数字之和」。负数按**绝对值**处理。",
       ["循环里 `x % 10` 取个位、`x /= 10` 砍掉个位，直到 `x == 0`",
        "负数直接取模会得到负数，先取绝对值",
        "0 的各位和是 0（循环一次都不进）"]),
  "第一行 `n`；第二行 `n` 个整数。",
  "`n` 行，每行一个整数。",
  "- 1 ≤ n ≤ 6\n- -10⁹ ≤ x ≤ 10⁹",
  lambda: cases("3\n123 456 0", "1\n-987", "4\n9 10 100 1000",
                "2\n-1 -100", "5\n2147483647 999999999 1000000000 -1000000000 5",
                "3\n11 22 33"),
  lambda t: "".join("%d\n" % sum(int(ch) for ch in str(abs(int(x)))) for x in t.split()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 0; i < n; i++) {
        long long x;
        scanf("%lld", &x);
        if (x < 0) x = -x;
        int s = 0;
        while (x > 0) { s += (int)(x % 10); x /= 10; }
        printf("%d\n", s);
    }
    return 0;
}
''',
  r'''#include <cstdio>
#include <cstdlib>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        char buf[32];
        scanf("%s", buf);                 // 当字符串读，逐字符累加数字值
        int s = 0;
        for (int i = 0; buf[i]; i++)
            if (buf[i] >= '0' && buf[i] <= '9') s += buf[i] - '0';
        printf("%d\n", s);
    }
    return 0;
}
''',
  ["C++基础", "循环", "数位分解"])

A("【输入输出】三种进制各输出一行", SEC_IO, 2,
  stmt("读入 `n` 个非负整数，对每个数输出三行：十进制、八进制、十六进制（**大写**字母）。",
       ["`printf` 的格式符：`%d` 十进制、`%o` 八进制、`%X` 大写十六进制",
        "八进制和十六进制**不加** `0` / `0x` 前缀（加了就多字符，直接判错）"]),
  "第一行 `n`；第二行 `n` 个非负整数。",
  "对每个数输出三行，依次是十进制、八进制、十六进制。",
  "- 1 ≤ n ≤ 6\n- 0 ≤ x ≤ 10⁹",
  lambda: cases("2\n255 8", "1\n0", "3\n16 4095 1", "2\n1000000000 123456789",
                "4\n7 8 15 16", "1\n1048576"),
  lambda t: "".join("%d\n%o\n%X\n" % (int(x), int(x), int(x)) for x in t.split()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 0; i < n; i++) {
        unsigned x;
        scanf("%u", &x);
        printf("%u\n", x);
        printf("%o\n", x);
        printf("%X\n", x);
    }
    return 0;
}
''',
  r'''#include <iostream>
#include <iomanip>
using namespace std;
int main() {
    int n;
    cin >> n;
    while (n--) {
        unsigned x;
        cin >> x;
        cout << dec << x << "\n"
             << oct << x << "\n"
             << hex << uppercase << x << "\n";
    }
    return 0;
}
''',
  ["C++基础", "进制转换", "格式化输出"])

A("【输入输出】补零到 5 位", SEC_IO, 2,
  stmt("读入 `n` 个非负整数，每个占一行、宽度固定 5、左侧**补 0**。",
       ["格式符是 `%05d`：宽度 5 且用 0 填充",
        "`%5d` 补的是空格，不是 0 —— 一字之差结果全错",
        "数本身超过 5 位时原样输出，不截断"]),
  "第一行 `n`；第二行 `n` 个非负整数。",
  "`n` 行，每行一个 5 位（至少）的数。",
  "- 1 ≤ n ≤ 6\n- 0 ≤ x ≤ 999999",
  lambda: cases("3\n1 22 333", "1\n0", "4\n9 99 999 9999",
                "2\n12345 123456", "5\n1 2 3 4 5", "3\n10000 1000 100"),
  lambda t: "".join("%05d\n" % int(x) for x in t.split()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 0; i < n; i++) {
        int x;
        scanf("%d", &x);
        printf("%05d\n", x);          // 宽度 5，补 0
    }
    return 0;
}
''',
  r'''#include <iostream>
#include <iomanip>
using namespace std;
int main() {
    int n;
    cin >> n;
    while (n--) {
        int x;
        cin >> x;
        cout << setfill('0') << setw(5) << x << "\n";
    }
    return 0;
}
''',
  ["C++基础", "格式化输出", "补零"])

A("【输入输出】读到文件末尾求和", SEC_IO, 2,
  stmt("输入若干行，每行两个整数，输出它们的和（每行一个结果）。",
       ["行数未知，用 `while (scanf(...) == 2)` 或 `while (cin >> a >> b)`",
        "注意判断的是**读到了两个数**，不是 `!= EOF`（后者遇到残缺行会算错）"]),
  "若干行，每行两个整数。",
  "每行一个整数，为对应行的和。",
  "- 行数 ≤ 10\n- -10⁹ ≤ a, b ≤ 10⁹",
  lambda: cases("1 2\n3 4", "0 0", "-5 5\n100 -100\n7 8",
                "1000000000 1000000000", "1 1\n2 2\n3 3\n4 4",
                "-1 -2\n-3 -4\n-5 -6"),
  lambda t: "".join("%d\n" % (lambda a, b: a + b)(*map(int, ln.split()))
                    for ln in t.strip().splitlines()),
  r'''#include <cstdio>
int main() {
    long long a, b;
    while (scanf("%lld %lld", &a, &b) == 2) {   // 恰读到两个数才算一条
        printf("%lld\n", a + b);
    }
    return 0;
}
''',
  r'''#include <iostream>
using namespace std;
int main() {
    long long a, b;
    while (cin >> a >> b) {
        cout << a + b << "\n";
    }
    return 0;
}
''',
  ["C++基础", "EOF", "循环读取"])


# ===================================================================== #
#  SEC_OP · 运算符与表达式（12 题）
# ===================================================================== #

def _cdiv(a: int, b: int) -> int:
    """C/C++ 的整数除法：向零截断（Python 的 // 是向负无穷，不能用）。"""
    q = abs(a) // abs(b)
    return -q if (a < 0) != (b < 0) else q


def _cmod(a: int, b: int) -> int:
    """C/C++ 的取模：余数符号跟随被除数。"""
    return a - _cdiv(a, b) * b


A("【运算】整数除法的商与余数", SEC_OP, 1,
  stmt("每行两个非零整数 `a b`，输出 `a / b` 的商与余数，各占一行。",
       ["C++ 的整数除法是**向零截断**：`-7 / 2 == -3`，不是 `-4`",
        "余数满足 `a == q * b + r`，符号跟着被除数走：`-7 % 2 == -1`",
        "Python 的 `//` 向负无穷取整，本题不能用它直接算"]),
  "若干行，每行两个非零整数。",
  "对每行输出两行：商、余数。",
  "- |a|, |b| ≤ 10⁹，b ≠ 0\n- 行数 ≤ 6",
  lambda: cases("7 2\n-7 2", "7 -2", "-7 -2\n8 3\n-8 3", "1 1\n-1 1",
                "100 7\n-100 7", "2147483647 2"),
  lambda t: "".join("%d\n%d\n" % (lambda a, b: (_cdiv(a, b), a - _cdiv(a, b) * b))(*map(int, ln.split()))
                    for ln in t.strip().splitlines()),
  r'''#include <cstdio>
int main() {
    long long a, b;
    while (scanf("%lld %lld", &a, &b) == 2) {
        printf("%lld\n", a / b);      // C++ 整数除法：向零截断
        printf("%lld\n", a % b);      // 余数符号同被除数
    }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    long long a, b;
    while (scanf("%lld %lld", &a, &b) == 2) {
        long long q = (a - a % b) / b;   // 先用余数修正，再整除
        printf("%lld\n%lld\n", q, a - q * b);
    }
    return 0;
}
''',
  ["C++基础", "整除", "取模", "负数"])

A("【运算】整除、浮点除与取模", SEC_OP, 1,
  stmt("读入两个整数 `a b`（`b > 0`），分别输出：\n\n"
       "1. `a / b` 的整除结果\n2. `a / b` 的浮点结果（保留三位小数）\n3. `a % b`",
       ["整除与浮点除的差别只在于**有没有一个 double 参与**",
        "`a / b` 两个都是 `int` 时先算整除，再赋给 `double` 已经晚了",
        "`(double)a / b` 与 `a / (double)b` 等价，`(double)(a / b)` 不等价"]),
  "一行两个整数 `a b`。",
  "三行：整除结果、浮点结果（三位小数）、余数。",
  "- -10⁶ ≤ a ≤ 10⁶，1 ≤ b ≤ 10⁶",
  lambda: cases("7 2", "1 3", "-7 2", "10 5", "1000000 7", "0 9"),
  lambda t: "%d\n%.3f\n%d\n" % (lambda a, b: (_cdiv(a, b), a / b, a - _cdiv(a, b) * b))(*map(int, t.split())),
  r'''#include <cstdio>
int main() {
    int a, b;
    if (scanf("%d %d", &a, &b) != 2) return 0;
    printf("%d\n", a / b);
    printf("%.3f\n", (double)a / b);      // 先转 double 再除
    printf("%d\n", a % b);
    return 0;
}
''',
  r'''#include <iostream>
#include <iomanip>
using namespace std;
int main() {
    int a, b;
    cin >> a >> b;
    div_t d = div(a, b);                  // 标准库一次拿到商和余数
    cout << d.quot << "\n"
         << fixed << setprecision(3) << (double)a / b << "\n"
         << d.rem << "\n";
    return 0;
}
''',
  ["C++基础", "整除", "浮点除法"])

A("【运算】自增自减的求值顺序", SEC_OP, 2,
  stmt("读入一个整数 `a`，按顺序执行下面四条语句，每条执行后输出此刻 `a` 的值：\n\n"
       "```cpp\n`a++`、`a`、`++a`、`a`\n```\n\n"
       "也就是输出四个数，用来看清**后缀先用后加、前缀先加后用**。",
       ["`a++` 的值是**加之前**的 a，`++a` 的值是**加之后**的 a",
        "每条语句单独一行，别塞进同一个表达式（`a++ + ++a` 是未定义行为）",
        "四条语句顺序执行，不是四条独立测试"]),
  "一行一个整数 `a`。",
  "四行，依次是四条语句执行后的 `a`。",
  "- 0 ≤ a ≤ 10⁶",
  lambda: cases("5", "0", "1", "-3", "100", "9"),
  lambda t: "".join("%d\n" % v for v in (lambda a: (
      (lambda x: x)(a), a + 1, a + 2, a + 2))(int(t))),
  r'''#include <cstdio>
int main() {
    long long a;
    if (scanf("%lld", &a) != 1) return 0;
    printf("%lld\n", a++);      // 输出旧值，a 变 a+1
    printf("%lld\n", a);        // 此时已是 a+1
    printf("%lld\n", ++a);      // 先加，输出 a+2
    printf("%lld\n", a);        // 仍是 a+2
    return 0;
}
''',
  r'''#include <iostream>
using namespace std;
int main() {
    long long a;
    cin >> a;
    long long v1 = a;           // 后缀：先取值
    a = a + 1;                  // 再加
    cout << v1 << "\n";
    cout << a << "\n";
    a = a + 1;                  // 前缀：先加
    cout << a << "\n";          // 再取值
    cout << a << "\n";
    return 0;
}
''',
  ["C++基础", "自增", "运算符"])

A("【运算】位运算五种基本操作", SEC_OP, 2,
  stmt("读入 `n` 对非负整数，对每对输出四行：`a & b`、`a | b`、`a ^ b`、`a << 1`。",
       ["`&` `|` `^` 是**逐位**运算，不是逻辑运算；`&&` `||` 才返回 0/1",
        "`a << 1` 相当于乘 2，但溢出不报错，本题数据保证不溢出",
        "四行顺序固定：与、或、异或、左移一位"]),
  "第一行 `n`；接下来 `n` 行，每行两个非负整数 `a b`。",
  "对每对输出四行，依次是 `a&b`、`a|b`、`a^b`、`a<<1`。",
  "- 1 ≤ n ≤ 6\n- 0 ≤ a, b ≤ 10⁶",
  lambda: cases("2\n5 3\n12 10", "1\n0 0", "3\n1 2\n7 8\n255 15",
                "2\n1000000 999999\n1 1", "4\n16 32\n63 64\n9 6\n3 5",
                "1\n1073741823 1"),
  lambda t: "".join("%d\n%d\n%d\n%d\n" % (a & b, a | b, a ^ b, a << 1)
                    for a, b in [tuple(map(int, ln.split())) for ln in t.strip().splitlines()[1:]]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 0; i < n; i++) {
        int a, b;
        scanf("%d %d", &a, &b);
        printf("%d\n", a & b);
        printf("%d\n", a | b);
        printf("%d\n", a ^ b);
        printf("%d\n", a << 1);
    }
    return 0;
}
''',
  r'''#include <iostream>
using namespace std;
int main() {
    int n;
    cin >> n;
    while (n--) {
        int a, b;
        cin >> a >> b;
        cout << (a & b) << "\n"
             << (a | b) << "\n"
             << (a ^ b) << "\n"
             << a * 2 << "\n";       // 移位等价于乘 2
    }
    return 0;
}
''',
  ["C++基础", "位运算", "移位"])

A("【运算】负数取模的符号", SEC_OP, 2,
  stmt("读入 `n` 对整数 `a b`（`b > 0`），输出 `a % b`。\n\n"
       "本题专门考 C++ 的取模规则：**余数的符号跟着被除数走**。",
       ["`-7 % 3 == -1`，不是 `2`（那是数学上的「最小非负剩余」）",
        "若想要非负余数，得写 `((a % b) + b) % b`",
        "本题按 C++ 原生语义输出，**不要**做非负化"]),
  "第一行 `n`；接下来 `n` 行，每行 `a b`（`b > 0`）。",
  "`n` 行，每行 `a % b` 的结果。",
  "- 1 ≤ n ≤ 6\n- -10⁹ ≤ a ≤ 10⁹，1 ≤ b ≤ 10⁹",
  lambda: cases("3\n-7 3\n7 -3\n-7 -3", "2\n10 4\n-10 4", "1\n0 5",
                "4\n-1 2\n-2 3\n-3 4\n-100 7", "2\n1000000000 7\n-1000000000 7",
                "3\n5 5\n-5 5\n5 1"),
  lambda t: "".join("%d\n" % (lambda a, b: a - _cdiv(a, b) * b)(*map(int, ln.split()))
                    for ln in t.strip().splitlines()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 0; i < n; i++) {
        long long a, b;
        scanf("%lld %lld", &a, &b);
        printf("%lld\n", a % b);       // 余数符号随被除数
    }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        long long a, b;
        scanf("%lld %lld", &a, &b);
        long long q = a / b;           // 先用除法求商
        printf("%lld\n", a - q * b);   // 再由 a - q*b 得余数
    }
    return 0;
}
''',
  ["C++基础", "取模", "负数", "易错"])

A("【运算】三目运算符求最大值", SEC_OP, 1,
  stmt("读入 `n` 组，每组三个整数，用**三目运算符** `? :` 输出最大值。",
       ["`a > b ? a : b` 可以嵌套：`(a > b ? a : b) > c ? ... : ...`",
        "三目运算符有优先级，嵌套时建议加括号",
        "相等的情况任取一个都行，结果一样"]),
  "第一行 `n`；接下来 `n` 行，每行三个整数 `a b c`。",
  "`n` 行，每行一个整数。",
  "- 1 ≤ n ≤ 6\n- |a|, |b|, |c| ≤ 10⁹",
  lambda: cases("3\n1 2 3\n3 2 1\n2 3 1", "1\n-1 -2 -3", "2\n5 5 5\n0 0 1",
                "3\n-100 0 100\n7 7 1\n-9 -9 -9", "1\n2147483647 0 -1",
                "4\n1 0 0\n0 1 0\n0 0 1\n1 1 0"),
  lambda t: "".join("%d\n" % max(int(x) for x in ln.split())
                    for ln in t.strip().splitlines()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        long long a, b, c;
        scanf("%lld %lld %lld", &a, &b, &c);
        long long m = (a > b ? a : b);
        m = (m > c ? m : c);            // 三目嵌套，别忘括号
        printf("%lld\n", m);
    }
    return 0;
}
''',
  r'''#include <iostream>
#include <algorithm>
using namespace std;
int main() {
    int n;
    cin >> n;
    while (n--) {
        long long a[3];
        cin >> a[0] >> a[1] >> a[2];
        cout << max(a[0], max(a[1], a[2])) << "\n";
    }
    return 0;
}
''',
  ["C++基础", "三目运算符", "最大值"])

A("【运算】混合表达式的优先级求值", SEC_OP, 2,
  stmt("读入 `n` 组六个整数 `a b c d e f`，计算并输出下面这个表达式的值：\n\n"
       "```cpp\n`a + b * c - d / e % f`\n```\n\n"
       "其中 `/` 是整除。数据保证 `e != 0`、`f != 0`。",
       ["优先级：`* / %` 同级且高于 `+ -`，同级**从左到右**",
        "所以 `d / e % f` 先算 `d / e`，结果再 `% f`",
        "不要自作主张加括号改变结合顺序"]),
  "第一行 `n`；接下来 `n` 行，每行六个整数。",
  "`n` 行，每行一个整数。",
  "- 1 ≤ n ≤ 6\n- |a|~|f| ≤ 100，e ≠ 0，f ≠ 0",
  lambda: cases("2\n1 2 3 4 2 3\n0 0 0 0 1 1", "1\n5 6 7 8 3 2",
                "3\n1 1 1 1 1 1\n-1 -2 -3 -4 -5 -6\n2 3 4 5 6 7",
                "1\n100 100 100 100 100 100", "2\n0 5 0 9 2 4\n3 0 3 0 1 2",
                "1\n7 3 9 11 4 5"),
  lambda t: "".join("%d\n" % (a + b * c - _cmod(_cdiv(d, e), f))
                    for a, b, c, d, e, f in [tuple(map(int, ln.split()))
                                             for ln in t.strip().splitlines()[1:]]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        int a, b, c, d, e, f;
        scanf("%d %d %d %d %d %d", &a, &b, &c, &d, &e, &f);
        int v = a + b * c - d / e % f;   // 按优先级从左到右
        printf("%d\n", v);
    }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        int a, b, c, d, e, f;
        scanf("%d %d %d %d %d %d", &a, &b, &c, &d, &e, &f);
        int t1 = b * c;                  // 手工拆成三步，等价于优先级
        int t2 = d / e;
        t2 = t2 % f;
        printf("%d\n", a + t1 - t2);
    }
    return 0;
}
''',
  ["C++基础", "运算符优先级", "整除"])

A("【运算】闰年判定", SEC_OP, 1,
  stmt("读入 `n` 个年份，判断是否闰年：是输出 `YES`，否输出 `NO`。\n\n"
       "闰年规则：能被 4 整除但不能被 100 整除，**或者**能被 400 整除。",
       ["`y % 4 == 0 && y % 100 != 0 || y % 400 == 0` —— `&&` 优先级高于 `||`，但加括号更清楚",
        "1900 不是闰年（能被 100 整除且不能被 400 整除），2000 是",
        "输出必须大写"]),
  "第一行 `n`；第二行 `n` 个正整数年份。",
  "`n` 行，每行 `YES` 或 `NO`。",
  "- 1 ≤ n ≤ 6\n- 1 ≤ year ≤ 9999",
  lambda: cases("4\n1900 2000 2024 2023", "2\n1600 1700", "1\n4",
                "3\n100 400 1000", "5\n1996 1999 2004 2100 2400",
                "1\n9999"),
  lambda t: "".join("%s\n" % ("YES" if (int(y) % 4 == 0 and int(y) % 100 != 0)
                              or int(y) % 400 == 0 else "NO") for y in t.split()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 0; i < n; i++) {
        int y;
        scanf("%d", &y);
        bool leap = (y % 4 == 0 && y % 100 != 0) || (y % 400 == 0);
        printf("%s\n", leap ? "YES" : "NO");
    }
    return 0;
}
''',
  r'''#include <iostream>
using namespace std;
int main() {
    int n;
    cin >> n;
    while (n--) {
        int y;
        cin >> y;
        bool leap = false;
        if (y % 400 == 0) leap = true;
        else if (y % 100 == 0) leap = false;
        else if (y % 4 == 0) leap = true;
        cout << (leap ? "YES" : "NO") << "\n";
    }
    return 0;
}
''',
  ["C++基础", "逻辑运算", "闰年"])

A("【运算】绝对值与符号（禁用 abs）", SEC_OP, 1,
  stmt("读入 `n` 个整数，对每个输出两个数：它的绝对值、它的符号（正 1 / 零 0 / 负 -1）。\n\n"
       "**不许调用 `abs()` / `fabs()`**，请用条件表达式自己写。",
       ["`x < 0 ? -x : x` 就是绝对值；注意 `-INT_MIN` 会溢出，本题数据不涉及",
        "符号不要写成 `x > 0`，那样零会落到 -1 分支",
        "两个数在同一行，空格分隔"]),
  "第一行 `n`；第二行 `n` 个整数。",
  "`n` 行，每行两个整数 `|x| sign`。",
  "- 1 ≤ n ≤ 6\n- -10⁹ ≤ x ≤ 10⁹",
  lambda: cases("4\n-5 0 3 -1", "1\n0", "3\n100 -100 1",
                "2\n-2147483647 2147483647", "5\n-2 -1 0 1 2",
                "1\n-999999999"),
  lambda t: "".join("%d %d\n" % (abs(int(x)), (int(x) > 0) - (int(x) < 0))
                    for x in t.split()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 0; i < n; i++) {
        long long x;
        scanf("%lld", &x);
        long long a = (x < 0 ? -x : x);          // 自己写绝对值
        int s = (x > 0) - (x < 0);               // 符号：1 / 0 / -1
        printf("%lld %d\n", a, s);
    }
    return 0;
}
''',
  r'''#include <iostream>
using namespace std;
int main() {
    int n;
    cin >> n;
    while (n--) {
        long long x;
        cin >> x;
        long long a;
        int s;
        if (x > 0)      { a = x;  s = 1; }
        else if (x < 0) { a = -x; s = -1; }
        else            { a = 0;  s = 0; }
        cout << a << " " << s << "\n";
    }
    return 0;
}
''',
  ["C++基础", "条件表达式", "符号"])

A("【运算】复合赋值运算链", SEC_OP, 2,
  stmt("读入 `n` 个整数 `x`，对每个依次执行：\n\n"
       "```cpp\n`x += 3;  x *= 2;  x -= 4;  x /= 2;  x %= 7;`\n```\n\n"
       "输出每一步执行后的 `x`，共五行。",
       ["`x /= 2` 是整除（向零截断），负数会往零靠",
        "`x %= 7` 的结果符号跟 `x` 走",
        "五行顺序固定，别合并"]),
  "第一行 `n`；第二行 `n` 个整数。",
  "对每个 `x` 输出五行，每行一个整数。",
  "- 1 ≤ n ≤ 6\n- -10⁶ ≤ x ≤ 10⁶",
  lambda: cases("2\n0 1", "1\n-10", "3\n100 -100 7", "2\n5 -5",
                "1\n999999", "3\n2 4 6"),
  lambda t: "".join("%d\n" % y for x in t.split()[1:] for y in _chain(int(x))),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        long long x;
        scanf("%lld", &x);
        x += 3; printf("%lld\n", x);
        x *= 2; printf("%lld\n", x);
        x -= 4; printf("%lld\n", x);
        x /= 2; printf("%lld\n", x);
        x %= 7; printf("%lld\n", x);
    }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 0; i < n; i++) {
        long long x;
        scanf("%lld", &x);
        long long r[5];
        r[0] = x + 3;
        r[1] = r[0] * 2;
        r[2] = r[1] - 4;
        r[3] = r[2] / 2;
        r[4] = r[3] % 7;
        for (int k = 0; k < 5; k++) printf("%lld\n", r[k]);
    }
    return 0;
}
''',
  ["C++基础", "复合赋值", "整除"])

A("【运算】类型转换的三条路", SEC_OP, 2,
  stmt("读入 `n` 个整数 `x`（32 ≤ x ≤ 126），对每个输出三行：\n\n"
       "1. `(char)x` 对应的字符\n"
       "2. `(double)x / 4` 的结果，保留两位小数\n"
       "3. `(int)(x / 4.0)` 的结果",
       ["`(char)x` 与 `char c = x` 等价，都是把整数截成 1 字节",
        "第 3 行是**先算浮点再截断**，等于向下取整（正数情况下）",
        "第 2 行别写成 `(double)(x / 4)`，那样先整除再转，结果不一样"]),
  "第一行 `n`；第二行 `n` 个整数。",
  "对每个 `x` 输出三行：字符、两位小数、整数。",
  "- 1 ≤ n ≤ 6\n- 32 ≤ x ≤ 126",
  lambda: cases("3\n65 97 48", "1\n126", "4\n32 33 34 35", "2\n90 122",
                "5\n80 81 82 83 84", "1\n100"),
  lambda t: "".join("%s\n%.2f\n%d\n" % (chr(int(x)), int(x) / 4.0, int(int(x) / 4.0))
                    for x in t.split()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        int x;
        scanf("%d", &x);
        printf("%c\n", (char)x);              // 整数按字节解释成字符
        printf("%.2f\n", (double)x / 4);      // 先转 double 再除
        printf("%d\n", (int)(x / 4.0));       // 浮点结果再截断
    }
    return 0;
}
''',
  r'''#include <iostream>
#include <iomanip>
using namespace std;
int main() {
    int n;
    cin >> n;
    while (n--) {
        int x;
        cin >> x;
        char c = static_cast<char>(x);
        double d = x / 4.0;
        int t = static_cast<int>(d);
        cout << c << "\n" << fixed << setprecision(2) << d << "\n" << t << "\n";
    }
    return 0;
}
''',
  ["C++基础", "类型转换", "字符"])


# ===================================================================== #
#  SEC_BR · 分支结构（12 题）
# ===================================================================== #

A("【分支】分段函数求值", SEC_BR, 1,
  stmt("按下面的分段函数计算 `y`：\n\n"
       "```\n`x < 0`   →  `y = 2x + 1`\n"
       "`x == 0`  →  `y = 0`\n"
       "`x > 0`   →  `y = x * x - 1`\n```",
       ["三段互斥，用 `if / else if / else`，不要写成三个独立 `if`",
        "`x == 0` 必须单独判，别漏",
        "输出是整数，一行一个"]),
  "第一行 `n`；第二行 `n` 个整数 `x`。",
  "`n` 行，每行一个整数 `y`。",
  "- 1 ≤ n ≤ 6\n- -1000 ≤ x ≤ 1000",
  lambda: cases("4\n-2 0 3 1", "1\n0", "3\n-1 -5 -100",
                "2\n10 100", "5\n-3 -2 -1 0 1", "1\n1000"),
  lambda t: "".join("%d\n" % (2 * int(x) + 1 if int(x) < 0 else (0 if int(x) == 0 else int(x) ** 2 - 1))
                    for x in t.split()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        long long x, y;
        scanf("%lld", &x);
        if (x < 0)       y = 2 * x + 1;
        else if (x == 0) y = 0;
        else             y = x * x - 1;
        printf("%lld\n", y);
    }
    return 0;
}
''',
  r'''#include <iostream>
using namespace std;
int main() {
    int n;
    cin >> n;
    while (n--) {
        long long x, y;
        cin >> x;
        if (x == 0)      y = 0;
        else if (x < 0)  y = 2 * x + 1;
        else             y = x * x - 1;
        cout << y << "\n";
    }
    return 0;
}
''',
  ["C++基础", "if-else", "分段函数"])

A("【分支】成绩等级判定", SEC_BR, 1,
  stmt("读入 `n` 个百分制成绩（整数 0~100），按下面规则输出等级：\n\n"
       "```\n90 ~ 100 → A\n80 ~ 89  → B\n70 ~ 79  → C\n60 ~ 69  → D\n 0 ~ 59  → E\n```",
       ["从高到低判，每个分支用 `else if`，不要写成独立 `if`",
        "90 分算 A，60 分算 D（边界要含等号）",
        "输出单个大写字母，一行一个"]),
  "第一行 `n`；第二行 `n` 个整数。",
  "`n` 行，每行一个字母。",
  "- 1 ≤ n ≤ 6\n- 0 ≤ score ≤ 100",
  lambda: cases("5\n95 85 75 65 55", "1\n90", "3\n100 60 59",
                "2\n0 1", "4\n89 79 69 69", "1\n100"),
  lambda t: "".join("%s\n" % ("A" if int(s) >= 90 else "B" if int(s) >= 80 else
                              "C" if int(s) >= 70 else "D" if int(s) >= 60 else "E")
                    for s in t.split()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        int s;
        scanf("%d", &s);
        char g;
        if (s >= 90)      g = 'A';
        else if (s >= 80) g = 'B';
        else if (s >= 70) g = 'C';
        else if (s >= 60) g = 'D';
        else              g = 'E';
        printf("%c\n", g);
    }
    return 0;
}
''',
  r'''#include <iostream>
using namespace std;
int main() {
    int n;
    cin >> n;
    const char *tbl = "EEEEEEDCBAA";     // 下标 = 分数/10，一次查表
    while (n--) {
        int s;
        cin >> s;
        int idx = s / 10;
        if (idx > 10) idx = 10;
        cout << tbl[idx] << "\n";
    }
    return 0;
}
''',
  ["C++基础", "if-else", "成绩等级"])

A("【分支】三个数升序输出", SEC_BR, 1,
  stmt("读入 `n` 组三个整数，把它们按**从小到大**输出，空格分隔。",
       ["最省事的写法是三者两两比较、必要时交换",
        "别用 `sort` 的话要保证三次比较覆盖全部分支",
        "相等的情况顺序无所谓，但输出个数不能少"]),
  "第一行 `n`；接下来 `n` 行，每行三个整数。",
  "`n` 行，每行三个整数，升序。",
  "- 1 ≤ n ≤ 6\n- |a|, |b|, |c| ≤ 10⁹",
  lambda: cases("3\n3 1 2\n2 3 1\n1 2 3", "1\n5 5 1", "2\n-1 0 -2\n0 0 0",
                "3\n100 -100 0\n9 8 7\n1 1 2", "1\n2147483647 -2147483648 0",
                "4\n2 1 1\n1 2 1\n1 1 2\n2 2 1"),
  lambda t: "".join("%d %d %d\n" % tuple(sorted(map(int, ln.split())))
                    for ln in t.strip().splitlines()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        long long a, b, c;
        scanf("%lld %lld %lld", &a, &b, &c);
        if (a > b) { long long t = a; a = b; b = t; }   // 两两交换三次
        if (a > c) { long long t = a; a = c; c = t; }
        if (b > c) { long long t = b; b = c; c = t; }
        printf("%lld %lld %lld\n", a, b, c);
    }
    return 0;
}
''',
  r'''#include <iostream>
#include <algorithm>
using namespace std;
int main() {
    int n;
    cin >> n;
    while (n--) {
        long long v[3];
        cin >> v[0] >> v[1] >> v[2];
        sort(v, v + 3);                  // 直接排序
        cout << v[0] << " " << v[1] << " " << v[2] << "\n";
    }
    return 0;
}
''',
  ["C++基础", "if", "排序三数"])

A("【分支】一元二次方程的根", SEC_BR, 3,
  stmt("读入 `n` 组系数 `a b c`，解方程 `ax² + bx + c = 0`，按下面规则输出：\n\n"
       "```\n`a == 0`        →  输出 \"not quadratic\"\n"
       "`Δ > 0`         →  输出两根（大的在前，两位小数，空格分隔）\n"
       "`Δ == 0`        →  输出 \"one root x\"（两位小数）\n"
       "`Δ < 0`         →  输出 \"no real root\"\n```\n\n"
       "其中 `Δ = b² - 4ac`。",
       ["先判 `a == 0`，否则除以 0",
        "`Δ` 可能是完全平方数，本题数据保证根是**整数或 .5**，用 `%.2f` 不会踩精度",
        "两根顺序：`(-b + √Δ) / 2a` 不一定更大，当 `a < 0` 时要比较"]),
  "第一行 `n`；接下来 `n` 行，每行三个整数 `a b c`。",
  "每个方程一行，格式见题面。",
  "- 1 ≤ n ≤ 6\n- |a|, |b|, |c| ≤ 100\n- 保证 Δ 是完全平方数或负数",
  lambda: cases("4\n1 -3 2\n1 2 1\n1 1 1\n0 2 3", "1\n2 -5 2", "2\n1 -5 6\n-1 3 -2",
                "3\n1 0 -4\n1 0 0\n0 0 1", "2\n1 -2 1\n2 -4 2",
                "1\n-1 5 -6"),
  lambda t: "".join(_quad(ln) for ln in t.strip().splitlines()[1:]),
  r'''#include <cstdio>
#include <cmath>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        int a, b, c;
        scanf("%d %d %d", &a, &b, &c);
        if (a == 0) { printf("not quadratic\n"); continue; }
        int d = b * b - 4 * a * c;
        if (d < 0) { printf("no real root\n"); continue; }
        if (d == 0) { printf("one root %.2f\n", -b / (2.0 * a)); continue; }
        double s = sqrt((double)d);
        double x1 = (-b + s) / (2.0 * a);
        double x2 = (-b - s) / (2.0 * a);
        if (x1 < x2) { double t = x1; x1 = x2; x2 = t; }   // 大的在前
        printf("%.2f %.2f\n", x1, x2);
    }
    return 0;
}
''',
  r'''#include <iostream>
#include <iomanip>
#include <cmath>
using namespace std;
int main() {
    int n;
    cin >> n;
    cout << fixed << setprecision(2);
    while (n--) {
        int a, b, c;
        cin >> a >> b >> c;
        if (a == 0) { cout << "not quadratic\n"; continue; }
        long long d = 1LL * b * b - 4LL * a * c;
        if (d < 0) { cout << "no real root\n"; continue; }
        double r = sqrt((double)(d < 0 ? 0 : d));
        double den = 2.0 * a;
        double x1 = (-b + r) / den, x2 = (-b - r) / den;
        if (d == 0) cout << "one root " << x2 << "\n";
        else if (x1 > x2) cout << x1 << " " << x2 << "\n";
        else cout << x2 << " " << x1 << "\n";
    }
    return 0;
}
''',
  ["C++基础", "if-else", "浮点", "数学库"])

A("【分支】三角形类型判定", SEC_BR, 2,
  stmt("读入 `n` 组三个正整数表示的三条边，按下面顺序输出类型：\n\n"
       "```\n任两边之和 <= 第三边   →  not a triangle\n"
       "三边相等               →  equilateral\n"
       "只有两边相等           →  isosceles\n"
       "有 a² + b² == c²       →  right\n"
       "其余                   →  scalene\n```",
       ["先判能否成三角形，后面才有意义",
        "等腰的判断要在等边之后，否则等边永远进不到 `equilateral`",
        "直角判断用平方和，别用开方后比浮点"]),
  "第一行 `n`；接下来 `n` 行，每行三个正整数。",
  "每个三角形一行。",
  "- 1 ≤ n ≤ 6\n- 1 ≤ a, b, c ≤ 1000",
  lambda: cases("5\n3 4 5\n2 2 2\n2 2 3\n3 4 6\n1 2 3", "1\n5 5 8", "2\n6 8 10\n7 7 7",
                "3\n1 1 2\n2 2 1\n8 15 17", "1\n1000 1000 1000",
                "2\n3 3 5\n4 4 4"),
  lambda t: "".join(_tri(ln) for ln in t.strip().splitlines()[1:]),
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        long long v[3];
        scanf("%lld %lld %lld", &v[0], &v[1], &v[2]);
        std::sort(v, v + 3);
        if (v[0] + v[1] <= v[2]) { printf("not a triangle\n"); continue; }
        if (v[0] == v[2])        { printf("equilateral\n");    continue; }
        if (v[0] == v[1] || v[1] == v[2]) { printf("isosceles\n"); continue; }
        if (v[0] * v[0] + v[1] * v[1] == v[2] * v[2]) { printf("right\n"); continue; }
        printf("scalene\n");
    }
    return 0;
}
''',
  r'''#include <iostream>
#include <algorithm>
using namespace std;
int main() {
    int n;
    cin >> n;
    while (n--) {
        long long a, b, c;
        cin >> a >> b >> c;
        if (a > b) swap(a, b);
        if (b > c) swap(b, c);
        if (a > b) swap(a, b);
        bool ok = a + b > c;
        bool eq3 = (a == b && b == c);
        bool eq2 = (a == b || b == c);
        bool rt = (a * a + b * b == c * c);
        if (!ok)       cout << "not a triangle\n";
        else if (eq3)  cout << "equilateral\n";
        else if (eq2)  cout << "isosceles\n";
        else if (rt)   cout << "right\n";
        else           cout << "scalene\n";
    }
    return 0;
}
''',
  ["C++基础", "if-else", "三角形"])

A("【分支】月份天数（switch 贯穿）", SEC_BR, 2,
  stmt("读入 `n` 组「年 月」，输出该月的天数（闰年 2 月为 29 天）。\n\n"
       "要求用 `switch` 的**贯穿（fall-through）**写法：把 4、6、9、11 月归到 30 天，"
       "2 月单独判闰年，其余 31 天。",
       ["`case 4: case 6: case 9: case 11: d = 30; break;` 是贯穿的标准用法",
        "漏写 `break` 会一路贯到下一个分支，这是最常见的 switch 错误",
        "闰年判断复用 `y%4==0 && y%100!=0 || y%400==0`"]),
  "第一行 `n`；接下来 `n` 行，每行两个整数 `year month`。",
  "`n` 行，每行一个整数。",
  "- 1 ≤ n ≤ 6\n- 1 ≤ year ≤ 9999，1 ≤ month ≤ 12",
  lambda: cases("4\n2024 2\n2023 2\n2024 4\n2024 12", "1\n2000 2", "3\n1900 2\n2024 1\n2024 7",
                "2\n2024 9\n2024 11", "1\n2024 3", "2\n2100 2\n2400 2"),
  lambda t: "".join("%d\n" % _mdays(*map(int, ln.split()))
                    for ln in t.strip().splitlines()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        int y, m;
        scanf("%d %d", &y, &m);
        int d;
        switch (m) {
            case 4: case 6: case 9: case 11: d = 30; break;   // 贯穿
            case 2:
                d = ((y % 4 == 0 && y % 100 != 0) || y % 400 == 0) ? 29 : 28;
                break;
            default: d = 31;
        }
        printf("%d\n", d);
    }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static const int TBL[13] = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    while (n--) {
        int y, m;
        scanf("%d %d", &y, &m);
        int d = TBL[m];
        bool leap = (y % 4 == 0 && y % 100 != 0) || (y % 400 == 0);
        if (m == 2 && leap) d = 29;
        printf("%d\n", d);
    }
    return 0;
}
''',
  ["C++基础", "switch", "贯穿着", "闰年"])

A("【分支】简单计算器", SEC_BR, 2,
  stmt("读入 `n` 行算式，每行形如 `a op b`，其中 `op` 是 `+ - * / %` 之一。\n\n"
       "输出运算结果（都是整数运算）。若遇到除数为 0，输出 `error`。",
       ["`op` 是字符，用 `scanf(\"%d %c %d\")` 读；`%c` 前加空格跳空白",
        "`switch (op)` 比一串 `if` 清楚",
        "除法和取模都要先判 `b == 0`，否则程序直接崩（不是输出 error）"]),
  "第一行 `n`；接下来 `n` 行，每行 `a op b`。",
  "`n` 行结果。",
  "- 1 ≤ n ≤ 6\n- |a|, |b| ≤ 10⁶\n- `op` ∈ {+,-,*,/,%}",
  lambda: cases("4\n7 + 2\n7 - 2\n7 * 2\n7 / 2", "2\n5 % 3\n0 / 5",
                "3\n1 / 0\n9 % 0\n-7 / 2", "2\n-7 % 3\n100 * 100",
                "1\n0 - 0", "3\n10 + 10\n10 - 10\n10 * 10"),
  lambda t: "".join(_calc(ln) for ln in t.strip().splitlines()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        long long a, b;
        char op;
        scanf("%lld %c %lld", &a, &op, &b);
        switch (op) {
            case '+': printf("%lld\n", a + b); break;
            case '-': printf("%lld\n", a - b); break;
            case '*': printf("%lld\n", a * b); break;
            case '/':
                if (b == 0) printf("error\n");
                else printf("%lld\n", a / b);
                break;
            case '%':
                if (b == 0) printf("error\n");
                else printf("%lld\n", a % b);
                break;
            default: printf("error\n");
        }
    }
    return 0;
}
''',
  r'''#include <iostream>
using namespace std;
int main() {
    int n;
    cin >> n;
    while (n--) {
        long long a, b;
        char op;
        cin >> a >> op >> b;
        if ((op == '/' || op == '%') && b == 0) { cout << "error\n"; continue; }
        long long r = 0;
        if (op == '+') r = a + b;
        else if (op == '-') r = a - b;
        else if (op == '*') r = a * b;
        else if (op == '/') r = a / b;
        else r = a % b;
        cout << r << "\n";
    }
    return 0;
}
''',
  ["C++基础", "switch", "计算器", "除零"])

A("【分支】出租车计费", SEC_BR, 2,
  stmt("出租车计费规则（金额单位：元，结果取整）：\n\n"
       "```\n起步价 10 元，含 3 公里\n"
       "超过 3 公里的部分，每公里 2 元\n"
       "等候时间每分钟加 1 元\n```\n\n"
       "读入 `n` 行「公里数 等候分钟数」，输出总费用。公里数可能带小数，向上取整到整公里计费。",
       ["先算超出里程 `max(0, km - 3)`，不足 1 公里按 1 公里算（向上取整）",
        "向上取整整数的写法：`(x + 0.999999)` 不可靠，用 `ceil` 或整数判断",
        "本题公里数是**整数**，不用处理小数，简化成 `km > 3 ? km - 3 : 0`"]),
  "第一行 `n`；接下来 `n` 行，每行两个整数 `km minutes`。",
  "`n` 行，每行一个整数。",
  "- 1 ≤ n ≤ 6\n- 0 ≤ km ≤ 1000，0 ≤ minutes ≤ 600",
  lambda: cases("4\n2 0\n3 0\n10 0\n10 5", "1\n0 0", "3\n4 0\n4 30\n100 60",
                "2\n1 60\n2 60", "1\n1000 600", "2\n3 10\n5 10"),
  lambda t: "".join("%d\n" % (10 + 2 * max(0, int(k) - 3) + int(m))
                    for k, m in [tuple(map(int, ln.split())) for ln in t.strip().splitlines()[1:]]),
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        int km, mins;
        scanf("%d %d", &km, &mins);
        int extra = std::max(0, km - 3);      // 超出里程
        int fee = 10 + extra * 2 + mins;      // 起步价 + 里程费 + 等候费
        printf("%d\n", fee);
    }
    return 0;
}
''',
  r'''#include <iostream>
using namespace std;
int main() {
    int n;
    cin >> n;
    while (n--) {
        int km, mins;
        cin >> km >> mins;
        int fee = 10 + mins;
        if (km > 3) fee += (km - 3) * 2;
        cout << fee << "\n";
    }
    return 0;
}
''',
  ["C++基础", "if", "分段计费"])

A("【分支】阶梯电费", SEC_BR, 2,
  stmt("居民阶梯电价（按月用电量 `k` 度）：\n\n"
       "```\n0  ~ 100 度      0.50 元/度\n"
       "101 ~ 200 度     超出 100 的部分 0.60 元/度\n"
       "200 度以上       超出 200 的部分 0.80 元/度\n```\n\n"
       "读入 `n` 个整数用电量，输出电费，**保留两位小数**。",
       ["分段累加：先付前 100 度的 50 元，再付中间段的钱",
        "用「分」做整数运算更稳：50 / 60 / 80 分每度，最后除以 100 输出",
        "别写成「超过 200 就全部按 0.8 算」—— 那是最常见的错解"]),
  "第一行 `n`；第二行 `n` 个非负整数。",
  "`n` 行，每行一个两位小数。",
  "- 1 ≤ n ≤ 6\n- 0 ≤ k ≤ 10000",
  lambda: cases("4\n0 100 150 250", "1\n200", "3\n101 199 201",
                "2\n50 300", "1\n10000", "2\n1000 1999"),
  lambda t: "".join("%.2f\n" % _elec(int(k)) for k in t.split()[1:]),
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        int k;
        scanf("%d", &k);
        long long fen = 0;                        // 以「分」为单位
        fen += std::min(k, 100) * 50LL;
        if (k > 100)  fen += std::min(k - 100, 100) * 60LL;
        if (k > 200)  fen += (k - 200) * 80LL;
        printf("%.2f\n", fen / 100.0);
    }
    return 0;
}
''',
  r'''#include <iostream>
#include <iomanip>
using namespace std;
int main() {
    int n;
    cin >> n;
    cout << fixed << setprecision(2);
    while (n--) {
        int k;
        cin >> k;
        double money = 0;
        int t = k;
        int a = t < 100 ? t : 100;       t -= a;
        int b = t < 100 ? t : 100;       t -= b;
        int c = t;
        money = a * 0.5 + b * 0.6 + c * 0.8;
        cout << money << "\n";
    }
    return 0;
}
''',
  ["C++基础", "if-else", "分段累加"])

A("【分支】水仙花数判定", SEC_BR, 2,
  stmt("读入 `n` 个三位正整数，判断它是否为**水仙花数**：各位数字的立方和等于它本身。\n\n"
       "是输出 `YES`，否输出 `NO`。",
       ["取各位：`a = x/100`、`b = x/10%10`、`c = x%10`",
        "`x/1000` 非零说明不是三位数，但本题数据保证是三位",
        "立方和用 `int` 就够（最大 9³×3 = 2187）"]),
  "第一行 `n`；第二行 `n` 个三位正整数。",
  "`n` 行，每行 `YES` 或 `NO`。",
  "- 1 ≤ n ≤ 6\n- 100 ≤ x ≤ 999",
  lambda: cases("4\n153 370 371 100", "1\n407", "3\n999 123 1634",
                "2\n100 101", "3\n370 371 372", "1\n999"),
  lambda t: "".join("%s\n" % ("YES" if sum(int(ch) ** 3 for ch in str(x)) == int(x) else "NO")
                    for x in t.split()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        int x;
        scanf("%d", &x);
        int a = x / 100, b = x / 10 % 10, c = x % 10;
        bool ok = (a * a * a + b * b * b + c * c * c == x);
        printf("%s\n", ok ? "YES" : "NO");
    }
    return 0;
}
''',
  r'''#include <iostream>
using namespace std;
int main() {
    int n;
    cin >> n;
    while (n--) {
        int x;
        cin >> x;
        int s = 0, t = x;
        while (t) { int d = t % 10; s += d * d * d; t /= 10; }
        cout << (s == x ? "YES" : "NO") << "\n";
    }
    return 0;
}
''',
  ["C++基础", "数位分解", "if"])

A("【分支】三位回文数判定", SEC_BR, 1,
  stmt("读入 `n` 个三位正整数，判断是否为回文数（正读反读相同），是输出 `YES`，否输出 `NO`。",
       ["三位回文的条件就是「百位 == 个位」，十位随便",
        "别把数字反转再比较，多此一举（虽然也对）",
        "输出大写"]),
  "第一行 `n`；第二行 `n` 个三位正整数。",
  "`n` 行，每行 `YES` 或 `NO`。",
  "- 1 ≤ n ≤ 6\n- 100 ≤ x ≤ 999",
  lambda: cases("4\n121 123 111 100", "1\n999", "3\n101 202 303",
                "2\n120 122", "3\n191 292 393", "1\n505"),
  lambda t: "".join("%s\n" % ("YES" if str(x)[0] == str(x)[-1] else "NO")
                    for x in t.split()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        int x;
        scanf("%d", &x);
        printf("%s\n", (x / 100 == x % 10) ? "YES" : "NO");
    }
    return 0;
}
''',
  r'''#include <iostream>
using namespace std;
int main() {
    int n;
    cin >> n;
    while (n--) {
        int x;
        cin >> x;
        int rev = 0, t = x;
        while (t) { rev = rev * 10 + t % 10; t /= 10; }   // 整体反转
        cout << (rev == x ? "YES" : "NO") << "\n";
    }
    return 0;
}
''',
  ["C++基础", "回文", "if"])

A("【分支】字符类型判断", SEC_BR, 1,
  stmt("读入 `n` 个可见字符，逐个判断类型并输出：\n\n"
       "```\n0~9  →  digit\nA~Z  →  upper\n a~z  →  lower\n其余  →  other\n```",
       ["用字符比较 `c >= '0' && c <= '9'`，别写 ASCII 码数字",
        "`isupper` / `isdigit` 也行，但要 `#include <cctype>`",
        "顺序：先判数字，再判大小写"]),
  "第一行 `n`；第二行 `n` 个字符，空格分隔。",
  "`n` 行，每行一个单词。",
  "- 1 ≤ n ≤ 6\n- 字符为可见 ASCII",
  lambda: cases("4\n5 A a +", "1\nZ", "5\n0 9 ~ _ !", "2\nz Z",
                "3\n@ [ `", "4\n1 b C 2"),
  lambda t: "".join("%s\n" % ("digit" if c.isdigit() else
                              "upper" if c.isupper() else
                              "lower" if c.islower() else "other")
                    for c in t.split()[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        char c;
        scanf(" %c", &c);
        if (c >= '0' && c <= '9')      printf("digit\n");
        else if (c >= 'A' && c <= 'Z') printf("upper\n");
        else if (c >= 'a' && c <= 'z') printf("lower\n");
        else                           printf("other\n");
    }
    return 0;
}
''',
  r'''#include <iostream>
#include <cctype>
using namespace std;
int main() {
    int n;
    cin >> n;
    while (n--) {
        char c;
        cin >> c;
        if (isdigit((unsigned char)c))      cout << "digit\n";
        else if (isupper((unsigned char)c)) cout << "upper\n";
        else if (islower((unsigned char)c)) cout << "lower\n";
        else                                cout << "other\n";
    }
    return 0;
}
''',
  ["C++基础", "字符分类", "cctype"])


# ===================================================================== #
#  本地辅助：题目里的 Python oracle 用到的计算函数
# ===================================================================== #
def _chain(x: int) -> list[int]:
    """复合赋值链 x+=3; x*=2; x-=4; x/=2; x%=7 的逐步结果。"""
    v = [x + 3]
    v.append(v[-1] * 2)
    v.append(v[-1] - 4)
    v.append(_cdiv(v[-1], 2))
    v.append(_cmod(v[-1], 7))
    return v


def _quad(ln: str) -> str:
    a, b, c = map(int, ln.split())
    if a == 0:
        return "not quadratic\n"
    d = b * b - 4 * a * c
    if d < 0:
        return "no real root\n"
    if d == 0:
        return "one root %.2f\n" % (-b / (2.0 * a))
    s = d ** 0.5
    x1 = (-b + s) / (2.0 * a)
    x2 = (-b - s) / (2.0 * a)
    if x1 < x2:
        x1, x2 = x2, x1
    return "%.2f %.2f\n" % (x1, x2)


def _tri(ln: str) -> str:
    v = sorted(map(int, ln.split()))
    a, b, c = v
    if a + b <= c:
        return "not a triangle\n"
    if a == c:
        return "equilateral\n"
    if a == b or b == c:
        return "isosceles\n"
    if a * a + b * b == c * c:
        return "right\n"
    return "scalene\n"


def _mdays(y: int, m: int) -> int:
    if m in (4, 6, 9, 11):
        return 30
    if m == 2:
        return 29 if (y % 4 == 0 and y % 100 != 0) or y % 400 == 0 else 28
    return 31


def _calc(ln: str) -> str:
    a, op, b = ln.split()
    a, b = int(a), int(b)
    if op == "+":
        return "%d\n" % (a + b)
    if op == "-":
        return "%d\n" % (a - b)
    if op == "*":
        return "%d\n" % (a * b)
    if b == 0:
        return "error\n"
    if op == "/":
        return "%d\n" % _cdiv(a, b)
    return "%d\n" % (a - _cdiv(a, b) * b)


def _elec(k: int) -> float:
    a = min(k, 100)
    b = min(max(k - 100, 0), 100)
    c = max(k - 200, 0)
    return (a * 50 + b * 60 + c * 80) / 100.0


if __name__ == "__main__":
    raise SystemExit(cli(PROBLEMS, "app/problems_bank_cpp_basic1.py",
                         "C++ 编程题第一册：输入输出 / 运算符 / 分支（36 题）",
                         "CPP_BASIC1_PROBLEMS"))
