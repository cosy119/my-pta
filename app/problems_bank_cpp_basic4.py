# -*- coding: utf-8 -*-
"""第 4 册：函数与参数传递 / 递归与递推 —— 自动生成，**不要手改本文件**。

生成器：tools/gen_cpp_basic4.py
题数：40 题 / 240 测试点 / 总分 472

重生成：python tools/gen_cpp_basic4.py
"""

CPP_BASIC4_PROBLEMS: list[dict] = [
    {
        "title": "【函数】引用传参交换两个数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "函数",
            "引用",
            "参数传递"
        ],
        "statement_md": "写一个交换函数，用**引用参数** `void mySwap(int &a, int &b)` 交换两个整数。读入两个整数，输出交换后的结果。\n\n**关键点**\n\n- 值传递 `void mySwap(int a, int b)` 交换的是副本，实参一点没变 —— 这是本章第一个坑\n- 引用参数在函数体内就是实参本身，`a` 和 `b` 只是它的别名\n- 输出一行，两个整数用空格分隔",
        "input_format": "一行两个整数 `a b`。",
        "output_format": "一行：交换后的 `a b`。",
        "constraints_md": "- |a|, |b| ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 函数与参数传递",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nvoid mySwap(int &a, int &b) {        // 引用参数：a、b 就是实参的别名\n    int t = a; a = b; b = t;\n}\nint main() {\n    int x, y;\n    if (scanf(\"%d %d\", &x, &y) != 2) return 0;\n    mySwap(x, y);\n    printf(\"%d %d\\n\", x, y);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <utility>\nint main() {\n    int x, y;\n    if (scanf(\"%d %d\", &x, &y) != 2) return 0;\n    std::swap(x, y);                 // 标准库版本，内部同样是引用\n    printf(\"%d %d\\n\", x, y);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3 5\n",
                "expected_stdout": "5 3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "-1 8\n",
                "expected_stdout": "8 -1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "0 0\n",
                "expected_stdout": "0 0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100 -100\n",
                "expected_stdout": "-100 100\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7 7\n",
                "expected_stdout": "7 7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "123456789 987654321\n",
                "expected_stdout": "987654321 123456789\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【函数】值传递与引用传递的差别",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "函数",
            "值传递",
            "引用"
        ],
        "statement_md": "有两个函数：`void addByValue(int x) { x += 1; }` 与 `void addByRef(int &x) { x += 1; }`。\n\n读入一个整数 `a`，先调用 `addByValue(a)` 并输出 `a`，再调用 `addByRef(a)` 并输出 `a`。\n\n**关键点**\n\n- 值传递里函数内加的是副本，回到 main 后 `a` 没变\n- 引用传递改的就是 `a` 本身\n- 两行输出，第一行是值传递之后的值，第二行是引用传递之后的值",
        "input_format": "一行一个整数 `a`。",
        "output_format": "两行：值传递后的 `a`、引用传递后的 `a`。",
        "constraints_md": "- |a| ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 函数与参数传递",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nvoid addByValue(int x) { x += 1; }\nvoid addByRef(int &x)   { x += 1; }\nint main() {\n    int a;\n    if (scanf(\"%d\", &a) != 1) return 0;\n    addByValue(a);\n    printf(\"%d\\n\", a);\n    addByRef(a);\n    printf(\"%d\\n\", a);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nvoid addByValue(int x) { x += 1; }\nvoid addByPtr(int *x)  { *x += 1; }   // 指针出参，效果等同引用\nint main() {\n    int a;\n    if (scanf(\"%d\", &a) != 1) return 0;\n    addByValue(a);\n    printf(\"%d\\n\", a);\n    addByPtr(&a);\n    printf(\"%d\\n\", a);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n",
                "expected_stdout": "5\n6\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "-1\n",
                "expected_stdout": "-1\n0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "0\n",
                "expected_stdout": "0\n1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1000000000\n",
                "expected_stdout": "1000000000\n1000000001\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "-1000000000\n",
                "expected_stdout": "-1000000000\n-999999999\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7\n",
                "expected_stdout": "7\n8\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【函数】数组传参求最大值与最小值",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "函数",
            "数组参数",
            "引用"
        ],
        "statement_md": "写一个函数接收数组和长度，一趟扫描同时求出最大值与最小值。读入 `n` 和 `n` 个整数，输出最大值与最小值。\n\n**关键点**\n\n- 数组作参数会**退化成一个指针**，函数里 `sizeof(a)` 拿不到数组长度，长度必须另传\n- 最大值初值不能写 0 —— 全是负数时 0 就成了「最大值」\n- 输出一行，先最大值后最小值",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：`max min`。",
        "constraints_md": "- 1 ≤ n ≤ 100\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 函数与参数传递",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nvoid stat(const int a[], int n, int &mx, int &mn) {   // 数组参数 + 两个引用出参\n    mx = mn = a[0];\n    for (int i = 1; i < n; i++) {\n        if (a[i] > mx) mx = a[i];\n        if (a[i] < mn) mn = a[i];\n    }\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    int a[105];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int mx, mn;\n    stat(a, n, mx, mn);\n    printf(\"%d %d\\n\", mx, mn);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    int a[105];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int *mx = std::max_element(a, a + n);   // 指针区间：a 已经退化为 int*\n    int *mn = std::min_element(a, a + n);\n    printf(\"%d %d\\n\", *mx, *mn);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n7 21 49 9 7\n",
                "expected_stdout": "49 7\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n10\n",
                "expected_stdout": "10 10\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "20\n-17 -13 37 37 -27 33 -21 35 -32 -22 32 43 -27 -34 -41 18 -23 45 -13 -47\n",
                "expected_stdout": "45 -47\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100\n-782 261 438 546 335 79 925 -495 -445 505 -477 -404 503 -852 348 -79 -380 -45 401 787 -188 -194 592 861 -758 -461 -543 783 846 -354 -267 654 -467 -262 647 295 293 57 -694 -671 129 362 359 -437 -663 -979 334 -857 -749 218 -310 -944 -830 -439 -582 749 -218 -174 194 913 -102 835 244 -807 787 312 406 814 -772 185 206 305 297 -255 -629 771 -807 529 791 -4 52 376 -604 -446 -74 278 -554 -8 634 -424 24 -479 -791 -752 675 -817 -430 -426 -758 -943\n",
                "expected_stdout": "925 -979\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7\n-24 -49 16 44 -46 -30 -20\n",
                "expected_stdout": "44 -49\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "33\n-4 10 11 -14 3 -21 7 -50 2 34 41 -17 -20 31 -22 -49 -13 -12 -8 35 -32 45 27 -11 -48 -22 27 -18 -48 -31 27 35 30\n",
                "expected_stdout": "45 -50\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【函数】默认参数求和",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "函数",
            "默认参数"
        ],
        "statement_md": "定义 `int addUp(int a, int b = 10, int c = 0)`。读入三个整数 `a b c`，依次输出 `addUp(a)`、`addUp(a, b)`、`addUp(a, b, c)` 三个调用的结果。\n\n**关键点**\n\n- 默认参数必须**从右往左**连续给，写成 `int addUp(int a = 1, int b)` 是编译错误\n- 三行输出，依次是省两个、省一个、一个都不省的结果\n- `addUp(a)` 展开后是 `a + 10 + 0`",
        "input_format": "一行三个整数 `a b c`。",
        "output_format": "三行：`addUp(a)`、`addUp(a,b)`、`addUp(a,b,c)`。",
        "constraints_md": "- |a|, |b|, |c| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 函数与参数传递",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint addUp(int a, int b = 10, int c = 0) { return a + b + c; }\nint main() {\n    int a, b, c;\n    if (scanf(\"%d %d %d\", &a, &b, &c) != 3) return 0;\n    printf(\"%d\\n\", addUp(a));\n    printf(\"%d\\n\", addUp(a, b));\n    printf(\"%d\\n\", addUp(a, b, c));\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint addUp(int a, int b = 10, int c = 0) { return a + b + c; }\nint main() {\n    int v[3] = {0, 10, 0};             // 缺省的实参保存在数组里，再一次性传齐\n    if (scanf(\"%d %d %d\", &v[0], &v[1], &v[2]) != 3) return 0;\n    int keep = v[1];\n    v[1] = 10;\n    printf(\"%d\\n\", addUp(v[0], v[1], 0));       // 等价于 addUp(a)\n    v[1] = keep;\n    printf(\"%d\\n\", addUp(v[0], v[1], 0));       // 等价于 addUp(a, b)\n    printf(\"%d\\n\", addUp(v[0], v[1], v[2]));\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "1 2 3\n",
                "expected_stdout": "11\n3\n6\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "0 0 0\n",
                "expected_stdout": "10\n0\n0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "-5 5 -5\n",
                "expected_stdout": "5\n0\n-5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100 200 300\n",
                "expected_stdout": "110\n300\n600\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7 -7 7\n",
                "expected_stdout": "17\n0\n7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "12 34 56\n",
                "expected_stdout": "22\n46\n102\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【函数】函数重载实现两数相加",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "函数",
            "重载",
            "模板"
        ],
        "statement_md": "用**函数重载**实现两个数相加：整数版本返回 `int`，小数版本返回 `double`。\n\n输入第一行是类型标记 `i` 或 `d`，第二行是两个数。整数版输出和本身，小数版输出和并保留两位小数。\n\n**关键点**\n\n- 重载靠**参数类型**区分，不能靠返回值类型区分\n- `i` 分支用 `scanf(\"%d\")`，`d` 分支必须用 `%lf`，混用会读成 0\n- 小数输出用 `%.2f`",
        "input_format": "第一行 `i` 或 `d`；第二行两个数（`i` 时是整数，`d` 时最多两位小数）。",
        "output_format": "一行：和（`d` 时保留两位小数）。",
        "constraints_md": "- |整数| ≤ 10⁹\n- |小数| ≤ 10⁶，小数位数 ≤ 2",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 函数与参数传递",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint    addUp(int a, int b)       { return a + b; }        // 整型重载\ndouble addUp(double a, double b) { return a + b; }        // 浮点重载\nint main() {\n    char t[4] = {0};\n    if (scanf(\"%3s\", t) != 1) return 0;\n    if (t[0] == 'i') {\n        int a, b;\n        scanf(\"%d %d\", &a, &b);\n        printf(\"%d\\n\", addUp(a, b));\n    } else {\n        double a, b;\n        scanf(\"%lf %lf\", &a, &b);\n        printf(\"%.2f\\n\", addUp(a, b));\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <iostream>\n#include <iomanip>\ntemplate <typename T> T addUp(T a, T b) { return a + b; }  // 模板替代重载\nint main() {\n    char t;\n    if (!(std::cin >> t)) return 0;\n    if (t == 'i') {\n        int a, b; std::cin >> a >> b;\n        std::cout << addUp(a, b) << \"\\n\";\n    } else {\n        double a, b; std::cin >> a >> b;\n        std::cout << std::fixed << std::setprecision(2) << addUp(a, b) << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "i\n3 5\n",
                "expected_stdout": "8\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "d\n1.5 2.25\n",
                "expected_stdout": "3.75\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "i\n-7 7\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "d\n0.1 0.2\n",
                "expected_stdout": "0.30\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "i\n1000000 2000000\n",
                "expected_stdout": "3000000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "d\n-3.75 1.25\n",
                "expected_stdout": "-2.50\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【函数】判断素数的函数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "函数",
            "素数",
            "试除"
        ],
        "statement_md": "写一个 `bool isPrime(int x)`，读入 `n` 和 `n` 个整数，输出其中素数的个数。\n\n**关键点**\n\n- 1 不是素数，2 是素数 —— 这两个边界最容易写错\n- 试除只需要到 `i * i <= x`，写成 `i < x` 在大数上会超时\n- 输出一个整数",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：素数个数。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 0 ≤ x ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 函数与参数传递",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nbool isPrime(int x) {\n    if (x < 2) return false;\n    for (long long i = 2; i * i <= x; i++)      // i*i 防溢出，别写 i < x\n        if (x % i == 0) return false;\n    return true;\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    int c = 0;\n    for (int i = 0; i < n; i++) { int x; scanf(\"%d\", &x); if (isPrime(x)) c++; }\n    printf(\"%d\\n\", c);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nbool isPrime(int x) {\n    if (x < 2) return false;\n    if (x % 2 == 0) return x == 2;              // 先摘掉偶数，再 6k±1 试除\n    for (long long i = 3; i * i <= x; i += 2)\n        if (x % i == 0) return false;\n    return true;\n}\nint main() {\n    int n, c = 0, x;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) { scanf(\"%d\", &x); c += isPrime(x) ? 1 : 0; }\n    printf(\"%d\\n\", c);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "6\n6 14 14 10 16 7\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n1\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n2\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "50\n18 32 4 79 58 24 90 16 95 84 45 11 30 35 7 41 77 23 71 88 94 56 91 7 74 3 76 34 40 54 25 24 15 75 68 94 100 73 8 90 42 79 43 34 24 51 40 100 84 66\n",
                "expected_stdout": "11\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100\n4750 1369 280 9700 5026 6943 6213 8685 5867 2135 3146 4381 7284 231 3622 7456 406 1736 1406 8164 6902 321 8399 7067 5882 943 3369 579 9653 6048 2817 3540 5944 9266 6041 9373 4609 5151 9388 1405 7768 2911 7915 9677 7332 2681 2983 2926 8743 5299 8521 3205 9541 1873 1349 1616 6982 638 9307 4515 9386 4598 9666 5420 1787 6057 4727 8883 4994 7451 8995 3577 4234 2450 1756 1957 8078 3900 5379 8938 2334 9711 1645 6276 2741 7362 554 917 6820 6446 383 2664 3697 209 3641 932 8825 7293 1521 5672\n",
                "expected_stdout": "9\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "30\n3 1 1 1 1 1 0 1 2 0 3 3 0 0 1 3 3 2 3 0 2 1 2 2 0 2 0 1 2 2\n",
                "expected_stdout": "14\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【函数】long long 阶乘函数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "函数",
            "阶乘",
            "long long"
        ],
        "statement_md": "写函数 `long long fact(int n)` 求 `n!`，读入 `n`（1 ≤ n ≤ 20），输出 `n!`。\n\n**关键点**\n\n- 13! = 6227020800 已经超 `int`（上限约 2.1×10⁹），所以返回值必须是 `long long`\n- `printf` 用 `%lld`，写成 `%d` 会打印出乱数\n- 20! 也在 `long long` 范围内（约 2.4×10¹⁸）",
        "input_format": "一行一个整数 `n`。",
        "output_format": "一行：`n!`。",
        "constraints_md": "- 1 ≤ n ≤ 20",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 函数与参数传递",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nlong long fact(int n) {                // 返回值必须是 long long\n    if (n <= 1) return 1;\n    return (long long)n * fact(n - 1);\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    printf(\"%lld\\n\", fact(n));\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    long long r = 1;\n    for (int i = 2; i <= n; i++) r *= i;   // 迭代版\n    printf(\"%lld\\n\", r);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "1\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n",
                "expected_stdout": "120\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "10\n",
                "expected_stdout": "3628800\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "13\n",
                "expected_stdout": "6227020800\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "20\n",
                "expected_stdout": "2432902008176640000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "17\n",
                "expected_stdout": "355687428096000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【函数】static 局部变量记调用次数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "函数",
            "static",
            "作用域"
        ],
        "statement_md": "函数 `int nextId() { static int id = 0; return ++id; }` 每次调用返回自增序号。\n\n读入 `m`，表示连续调用 `m` 次。输出两行：最后一次的返回值、所有返回值之和。\n\n**关键点**\n\n- `static` 局部变量只在第一次调用时初始化，之后跨调用保留\n- 去掉 `static` 的话每次都是 1 —— 正好可以用来验证\n- 第二行用 `long long`（m 到 10⁵ 时和到 5×10⁹）",
        "input_format": "一行一个整数 `m`。",
        "output_format": "两行：最后一次返回值、所有返回值之和。",
        "constraints_md": "- 1 ≤ m ≤ 100000",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 函数与参数传递",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint nextId() {\n    static int id = 0;      // 只初始化一次，之后跨调用保留\n    return ++id;\n}\nint main() {\n    int m, last = 0;\n    long long s = 0;\n    if (scanf(\"%d\", &m) != 1) return 0;\n    for (int i = 0; i < m; i++) { last = nextId(); s += last; }\n    printf(\"%d\\n%lld\\n\", last, s);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nstruct Counter {                       // 用成员变量模拟 static 局部变量\n    int id = 0;\n    int next() { return ++id; }\n};\nint main() {\n    int m, last = 0;\n    long long s = 0;\n    Counter c;\n    if (scanf(\"%d\", &m) != 1) return 0;\n    for (int i = 0; i < m; i++) { last = c.next(); s += last; }\n    printf(\"%d\\n%lld\\n\", last, s);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "1\n",
                "expected_stdout": "1\n1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n",
                "expected_stdout": "5\n15\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "10\n",
                "expected_stdout": "10\n55\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100\n",
                "expected_stdout": "100\n5050\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "999\n",
                "expected_stdout": "999\n499500\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100000\n",
                "expected_stdout": "100000\n5000050000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【函数】全局变量被局部变量遮蔽",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "函数",
            "全局变量",
            "作用域"
        ],
        "statement_md": "程序里有全局变量 `int g = 100;`，函数写成 `int shadow(int g) { g += 1; return g; }`。\n\n读入 `a`，输出两行：`shadow(a)` 的返回值、函数调用后全局 `g` 的值。\n\n**关键点**\n\n- 函数参数名与全局变量同名时，函数内**只有参数可见**，这叫名字遮蔽\n- 函数里改的是参数副本，全局 `g` 纹丝不动\n- 想在函数里用全局变量得写 `::g`",
        "input_format": "一行一个整数 `a`。",
        "output_format": "两行：函数返回值、全局 `g`。",
        "constraints_md": "- |a| ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 函数与参数传递",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint g = 100;\nint shadow(int g) {         // 形参遮蔽了全局 g\n    g += 1;\n    return g;\n}\nint main() {\n    int a;\n    if (scanf(\"%d\", &a) != 1) return 0;\n    printf(\"%d\\n\", shadow(a));\n    printf(\"%d\\n\", g);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint g = 100;\nint shadow(int x) {\n    g += 0;                 // 只读全局，不遮蔽\n    return x + 1;\n}\nint main() {\n    int a;\n    if (scanf(\"%d\", &a) != 1) return 0;\n    printf(\"%d\\n\", shadow(a));\n    printf(\"%d\\n\", ::g);    // 显式全局作用域\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n",
                "expected_stdout": "6\n100\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "-1\n",
                "expected_stdout": "0\n100\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "0\n",
                "expected_stdout": "1\n100\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100\n",
                "expected_stdout": "101\n100\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "-100\n",
                "expected_stdout": "-99\n100\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "999\n",
                "expected_stdout": "1000\n100\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【函数】引用出参返回和与最大值",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "函数",
            "引用",
            "出参"
        ],
        "statement_md": "写函数 `void stat(const int a[], int n, long long &sum, int &mx)`，一次遍历同时带出总和与最大值。读入 `n` 和 `n` 个整数，输出 `sum` 与 `mx`。\n\n**关键点**\n\n- 一个函数想返回两个值，最常用的办法就是引用出参\n- `const int a[]` 里的 `const` 是承诺「不改数组」，调用方可以传只读数据\n- 和要用 `long long`：100 个 10⁶ 累加就是 10⁸，接近 `int` 的安全边界",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：`sum max`。",
        "constraints_md": "- 1 ≤ n ≤ 10⁵\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 函数与参数传递",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nvoid stat(const int a[], int n, long long &sum, int &mx) {\n    sum = 0;\n    mx = a[0];\n    for (int i = 0; i < n; i++) {\n        sum += a[i];\n        if (a[i] > mx) mx = a[i];\n    }\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    int a[100005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    long long sum; int mx;\n    stat(a, n, sum, mx);\n    printf(\"%lld %d\\n\", sum, mx);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nstruct Result { long long sum; int mx; };        // 用结构体打包两个结果\nResult stat(const int *a, int n) {\n    Result r{0, a[0]};\n    for (int i = 0; i < n; i++) { r.sum += a[i]; r.mx = std::max(r.mx, a[i]); }\n    return r;\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[100005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    Result r = stat(a, n);\n    printf(\"%lld %d\\n\", r.sum, r.mx);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n-49 10 -36 47 0\n",
                "expected_stdout": "-28 47\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n-41\n",
                "expected_stdout": "-41 -41\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "20\n23 -29 30 -21 -15 11 33 18 17 -27 33 28 14 -9 37 17 11 6 -14 36\n",
                "expected_stdout": "199 37\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "200\n83 -269 199 -944 727 -531 840 -939 806 -204 -254 954 943 -868 -132 956 -373 -302 -807 196 47 684 -683 -803 -439 -290 250 -997 590 -683 541 72 -824 640 -875 -244 -478 515 130 443 717 -878 639 -208 912 -659 205 789 303 -366 -403 -219 -358 -565 -579 -73 96 -633 243 -732 173 471 -198 113 -132 -517 -492 400 669 -771 189 374 533 -847 662 -90 -425 -151 -761 190 -421 870 857 -595 621 -643 -170 599 590 856 -300 -77 772 858 -816 65 517 695 -29 -140 772 -55 -258 -732 -91 -437 -713 -522 -679 -394 -363 -860 874 -387 58 -787 197 74 -392 -168 911 -535 -165 931 733 -367 560 88 880 832 482 553 -275 977 523 248 693 783 -68 -867 -854 503 -900 -312 -162 -343 -645 576 -619 519 -149 -300 -13 -256 356 -430 -996 912 463 258 304 -468 48 90 612 -882 -671 -448 -759 26 -462 992 -827 757 363 121 -61 562 -706 -485 321 421 832 588 -685 -42 910 -632 331 -247 510 667 -229 888 -698 -773 -49 -333 216 -647\n",
                "expected_stdout": "-1476 992\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7\n20 -8 46 -34 45 -7 -31\n",
                "expected_stdout": "31 46\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "333\n-8 -43 -48 -14 -40 -50 14 30 -28 -19 -16 43 33 5 -4 21 -16 19 -41 23 2 12 -1 -6 46 0 -19 0 -29 -35 15 13 39 47 -24 17 -13 -27 12 40 25 -9 41 20 -29 -50 26 -1 13 -33 46 -23 3 -3 -24 13 43 46 -18 28 -46 -20 30 14 9 33 14 -13 7 43 -40 -20 -12 -24 22 -29 -28 -42 42 -20 -3 5 41 19 -48 29 -2 -6 12 -29 18 22 43 -18 -40 -38 33 8 -24 -22 38 42 -5 -32 48 -33 -27 19 31 -40 10 -15 -15 -13 -50 19 -12 38 21 -43 -12 -46 13 43 -40 -2 37 -35 -12 2 -2 -27 -16 -9 -25 -33 -14 7 4 -37 30 46 -28 -36 -34 9 37 -11 -12 20 7 -46 23 -29 -1 -40 33 -44 -9 -19 13 -19 -5 -38 4 -4 -32 -4 -5 -11 -36 9 29 3 3 32 3 1 -39 -30 15 17 28 30 24 47 39 -5 -29 35 -47 -41 41 27 45 16 -18 -41 42 32 36 -32 36 40 -36 7 -38 12 18 17 23 -48 -48 15 30 4 -42 4 1 22 33 33 -29 -1 -37 23 13 -20 43 34 3 39 -50 44 -20 -47 42 -28 -28 -2 42 6 0 -15 16 -32 30 -40 45 38 15 2 -3 40 -49 4 23 26 -28 15 -50 35 -10 -9 -33 42 15 38 39 -26 -37 46 13 -40 -2 -21 -40 44 -12 -32 -48 -22 -30 45 -10 -13 -7 0 -16 14 45 -49 -11 0 12 4 49 -31 -1 -40 7 21 21 42 -43 43 26 -9 -47 -28 -29 8 9 42 -23 38 50 29 -7 41 -32 20 -42 -31 18 27 25 -23 3 30 -8 49 0\n",
                "expected_stdout": "67 50\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【函数】递归求幂与迭代求幂",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "函数",
            "递归",
            "快速幂"
        ],
        "statement_md": "分别用递归和迭代写 `a^n`，输入 `a n`，输出 `a` 的 `n` 次方。\n\n**关键点**\n\n- `n = 0` 时结果恒为 1，包括 `a = 0` 的情况（按幂运算惯例 0⁰ 记作 1）\n- 连乘用 `long long`，`a` 到 10、`n` 到 18 时结果已经到 10¹⁸ 量级\n- 递归版别忘边界 `n == 0`，否则无限递归爆栈",
        "input_format": "一行两个整数 `a n`。",
        "output_format": "一行：`a` 的 `n` 次方。",
        "constraints_md": "- |a| ≤ 10\n- 0 ≤ n ≤ 18",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 函数与参数传递",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nlong long power(long long a, int n) {\n    if (n == 0) return 1;                 // 边界写在最前\n    return a * power(a, n - 1);\n}\nint main() {\n    long long a; int n;\n    if (scanf(\"%lld %d\", &a, &n) != 2) return 0;\n    printf(\"%lld\\n\", power(a, n));\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nlong long power(long long a, int n) {\n    long long r = 1;                      // 迭代 + 快速幂\n    while (n > 0) {\n        if (n & 1) r *= a;\n        a *= a;\n        n >>= 1;\n    }\n    return r;\n}\nint main() {\n    long long a; int n;\n    if (scanf(\"%lld %d\", &a, &n) != 2) return 0;\n    printf(\"%lld\\n\", power(a, n));\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "2 10\n",
                "expected_stdout": "1024\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "0 0\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "-2 3\n",
                "expected_stdout": "-8\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10 18\n",
                "expected_stdout": "1000000000000000000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1 18\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "-1 17\n",
                "expected_stdout": "-1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【函数】函数封装区间求和",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "函数",
            "前缀和",
            "区间求和"
        ],
        "statement_md": "把「求数组一段区间和」封装成函数（用前缀和，单次询问 O(1)）。\n\n读入 `n` 和 `q`，第二行 `n` 个整数，之后 `q` 行每行两个整数 `l r`（下标从 1 开始），对每个询问输出 `a[l] + … + a[r]`。\n\n**关键点**\n\n- 前缀和 `pre[i] = pre[i-1] + a[i]`，区间和是 `pre[r] - pre[l-1]`\n- `pre[0]` 必须是 0，否则 `l = 1` 时会减到数组外\n- 每个询问输出一行",
        "input_format": "第一行 `n q`；第二行 `n` 个整数；之后 `q` 行，每行 `l r`。",
        "output_format": "`q` 行，每行一个区间和。",
        "constraints_md": "- 1 ≤ n ≤ 10⁵\n- 1 ≤ q ≤ 10⁵\n- 1 ≤ l ≤ r ≤ n\n- |a[i]| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 函数与参数传递",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nlong long rangeSum(const long long pre[], int l, int r) {\n    return pre[r] - pre[l - 1];\n}\nint main() {\n    int n, q;\n    if (scanf(\"%d %d\", &n, &q) != 2) return 0;\n    static long long pre[100005];\n    pre[0] = 0;                            // 哨兵，保证 l=1 时能减\n    for (int i = 1; i <= n; i++) {\n        long long x; scanf(\"%lld\", &x);\n        pre[i] = pre[i - 1] + x;\n    }\n    while (q--) {\n        int l, r; scanf(\"%d %d\", &l, &r);\n        printf(\"%lld\\n\", rangeSum(pre, l, r));\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n, q;\n    if (scanf(\"%d %d\", &n, &q) != 2) return 0;\n    long long *pre = new long long[n + 1];  // 动态数组版\n    pre[0] = 0;\n    for (int i = 1; i <= n; i++) {\n        long long x; scanf(\"%lld\", &x);\n        pre[i] = pre[i - 1] + x;\n    }\n    for (int k = 0; k < q; k++) {\n        int l, r; scanf(\"%d %d\", &l, &r);\n        printf(\"%lld\\n\", pre[r] - pre[l - 1]);\n    }\n    delete[] pre;\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 3\n3 -1 4 -1 5\n1 3\n2 5\n1 5\n",
                "expected_stdout": "6\n7\n10\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 1\n-7\n1 1\n",
                "expected_stdout": "-7\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "6 2\n1 2 3 4 5 6\n1 6\n3 4\n",
                "expected_stdout": "21\n7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10 4\n-2 -8 -21 -29 -1 23 38 -14 20 -15\n1 10\n2 9\n3 3\n5 7\n",
                "expected_stdout": "-9\n8\n-21\n60\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "20 3\n63 -72 -94 89 -30 -38 -43 -65 88 -74 73 89 39 -78 51 8 -92 -93 -77 -45\n1 20\n4 14\n10 11\n",
                "expected_stdout": "-301\n50\n-1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8 5\n-922 -415 425 561 -706 964 -53 -243\n1 1\n2 2\n1 8\n3 6\n7 8\n",
                "expected_stdout": "-922\n-415\n-389\n1244\n-296\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【函数】多函数协作求最大公约数与最小公倍数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "函数",
            "gcd",
            "lcm"
        ],
        "statement_md": "写两个函数：`gcd` 求最大公约数，`lcm` 在内部调用 `gcd` 求最小公倍数。读入 `a b`，输出 `gcd(a,b)` 与 `lcm(a,b)`。\n\n**关键点**\n\n- `lcm = a / gcd * b`，先除后乘能少溢出一次\n- `a`、`b` 到 10⁹ 时 lcm 能到 10¹⁸ 量级，两个量都用 `long long`\n- 输出一行，先 gcd 后 lcm",
        "input_format": "一行两个正整数 `a b`。",
        "output_format": "一行：`gcd lcm`。",
        "constraints_md": "- 1 ≤ a, b ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 函数与参数传递",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nlong long gcd(long long a, long long b) {\n    while (b) { long long t = a % b; a = b; b = t; }\n    return a;\n}\nlong long lcm(long long a, long long b) {      // 内部复用 gcd\n    return a / gcd(a, b) * b;                  // 先除后乘\n}\nint main() {\n    long long a, b;\n    if (scanf(\"%lld %lld\", &a, &b) != 2) return 0;\n    printf(\"%lld %lld\\n\", gcd(a, b), lcm(a, b));\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nlong long gcd(long long a, long long b) {\n    return b == 0 ? a : gcd(b, a % b);         // 递归版\n}\nint main() {\n    long long a, b;\n    if (scanf(\"%lld %lld\", &a, &b) != 2) return 0;\n    long long g = gcd(a, b);\n    printf(\"%lld %lld\\n\", g, a / g * b);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "12 18\n",
                "expected_stdout": "6 36\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 1\n",
                "expected_stdout": "1 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "7 13\n",
                "expected_stdout": "1 91\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1000000000 999999937\n",
                "expected_stdout": "1 999999937000000000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "270 192\n",
                "expected_stdout": "6 8640\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "36 48\n",
                "expected_stdout": "12 144\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【函数】函数内修改数组（传地址）",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "函数",
            "数组参数",
            "指针"
        ],
        "statement_md": "写函数把数组里所有负数改成它的绝对值。读入 `n` 和 `n` 个整数，输出修改后的数组。\n\n**关键点**\n\n- 数组参数传的是地址，函数内的修改会反映到调用方 —— 这和传 `int` 完全不同\n- 想保护原数组就加 `const`，加了还改会直接编译报错\n- 输出一行，数字之间一个空格",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：修改后的数组。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 函数与参数传递",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nvoid absAll(int a[], int n) {          // 形参是 int*，改的是原数组\n    for (int i = 0; i < n; i++)\n        if (a[i] < 0) a[i] = -a[i];\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    absAll(a, n);\n    for (int i = 0; i < n; i++) printf(\"%d%c\", a[i], i + 1 == n ? '\\n' : ' ');\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nvoid absAll(int *p, int n) {           // 显式写指针\n    for (int *q = p; q < p + n; ++q)\n        if (*q < 0) *q = -*q;\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    absAll(a, n);\n    for (int i = 0; i < n; i++) printf(\"%d%c\", a[i], i + 1 == n ? '\\n' : ' ');\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n-19 14 20 -30 -19\n",
                "expected_stdout": "19 14 20 30 19\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n-1 -2 -3\n",
                "expected_stdout": "1 2 3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n0\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "20\n-16 -44 42 15 11 -3 2 -46 -33 -30 2 -27 -6 6 30 -50 -46 19 -1 6\n",
                "expected_stdout": "16 44 42 15 11 3 2 46 33 30 2 27 6 6 30 50 46 19 1 6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "50\n263 747 823 -558 -66 28 456 -12 918 470 66 -262 502 -69 491 -937 757 902 -925 866 -654 -296 529 -729 -466 804 520 -886 -654 -904 -263 -531 -98 -595 -532 -741 -717 -281 39 567 325 744 -349 47 352 -175 927 -888 -320 -430\n",
                "expected_stdout": "263 747 823 558 66 28 456 12 918 470 66 262 502 69 491 937 757 902 925 866 654 296 529 729 466 804 520 886 654 904 263 531 98 595 532 741 717 281 39 567 325 744 349 47 352 175 927 888 320 430\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8\n-7 -2 -1 -5 -2 -2 -3 -6\n",
                "expected_stdout": "7 2 1 5 2 2 3 6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【函数】谓词函数筛选计数（回文数）",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "函数",
            "谓词",
            "回文数"
        ],
        "statement_md": "写谓词函数 `bool isPal(int x)` 判断一个数是不是回文数（正读倒读相同），读入 `n` 和 `n` 个**正整数**，输出其中回文数的个数。\n\n**关键点**\n\n- 按十进制位判断，别转成字符串也行：把数反转过来看是否相等\n- 末尾是 0 的数（如 120）一定不是回文数（除非它本身是 0），反转后前导零丢了\n- 输出一个整数",
        "input_format": "第一行 `n`，第二行 `n` 个正整数。",
        "output_format": "一行：回文数个数。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 1 ≤ x ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 函数与参数传递",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nbool isPal(int x) {\n    int y = x, r = 0;                  // 反转这个数\n    while (y > 0) { r = r * 10 + y % 10; y /= 10; }\n    return r == x;\n}\nint main() {\n    int n, c = 0, x;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) { scanf(\"%d\", &x); if (isPal(x)) c++; }\n    printf(\"%d\\n\", c);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cstring>\nbool isPal(int x) {                    // 转成字符数组两头夹\n    char s[16];\n    int len = snprintf(s, sizeof(s), \"%d\", x);\n    for (int i = 0, j = len - 1; i < j; i++, j--)\n        if (s[i] != s[j]) return false;\n    return true;\n}\nint main() {\n    int n, c = 0, x;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) { scanf(\"%d\", &x); c += isPal(x) ? 1 : 0; }\n    printf(\"%d\\n\", c);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n121 123 1221 10 7\n",
                "expected_stdout": "3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n1\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "20\n64 24 72 28 42 38 42 89 4 63 46 46 9 52 60 43 22 43 81 1\n",
                "expected_stdout": "4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "50\n951 590 178 67 994 835 244 914 476 318 920 687 365 176 521 192 166 8 985 267 653 176 886 126 31 484 483 532 20 794 890 351 975 605 662 165 709 218 736 81 335 559 459 577 20 632 408 959 962 314\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n100001 12321 9999 11 100 9\n",
                "expected_stdout": "5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "30\n1013 1013 975 964 1023 1068 922 998 1091 920 919 1068 951 974 918 1060 978 1091 1056 915 956 1069 932 984 960 970 1053 1072 907 908\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【函数】复合函数 f(g(x))",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "函数",
            "复合函数",
            "嵌套调用"
        ],
        "statement_md": "定义 `int f(int x) { return 2 * x + 1; }`、`int g(int x) { return x * x - 3; }`。读入 `x`，输出 `g(f(g(x)))`。\n\n**关键点**\n\n- 从最里面往外算：先 `g(x)`，再 `f(...)`，再 `g(...)`\n- 函数调用可以嵌套，`g(f(g(x)))` 是合法表达式\n- |x| ≤ 100 时结果仍在 `int` 范围内",
        "input_format": "一行一个整数 `x`。",
        "output_format": "一行：`g(f(g(x)))`。",
        "constraints_md": "- |x| ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 函数与参数传递",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint f(int x) { return 2 * x + 1; }\nint g(int x) { return x * x - 3; }\nint main() {\n    int x;\n    if (scanf(\"%d\", &x) != 1) return 0;\n    int t = g(x);          // 先算最里层\n    t = f(t);\n    t = g(t);\n    printf(\"%d\\n\", t);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint f(int x) { return 2 * x + 1; }\nint g(int x) { return x * x - 3; }\nint main() {\n    int x;\n    if (scanf(\"%d\", &x) != 1) return 0;\n    printf(\"%d\\n\", g(f(g(x))));    // 嵌套调用一次写完\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "2\n",
                "expected_stdout": "6\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "0\n",
                "expected_stdout": "22\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "-3\n",
                "expected_stdout": "166\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n",
                "expected_stdout": "38022\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "-10\n",
                "expected_stdout": "38022\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7\n",
                "expected_stdout": "8646\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【函数】bool 函数统计闰年",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "函数",
            "bool",
            "闰年"
        ],
        "statement_md": "写 `bool isLeap(int y)`：能被 4 整除且不能被 100 整除，或者能被 400 整除的是闰年。读入 `y1 y2`，输出区间 `[y1, y2]` 内闰年的个数。\n\n**关键点**\n\n- 条件顺序：`y % 4 == 0 && y % 100 != 0 || y % 400 == 0`，`&&` 优先于 `||`\n- 1900 不是闰年（被 100 整除但不被 400 整除），2000 是闰年\n- 输出一个整数",
        "input_format": "一行两个整数 `y1 y2`（`y1 ≤ y2`）。",
        "output_format": "一行：区间内闰年个数。",
        "constraints_md": "- 1 ≤ y1 ≤ y2 ≤ 9999",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 函数与参数传递",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nbool isLeap(int y) {\n    return (y % 4 == 0 && y % 100 != 0) || (y % 400 == 0);\n}\nint main() {\n    int a, b, c = 0;\n    if (scanf(\"%d %d\", &a, &b) != 2) return 0;\n    for (int y = a; y <= b; y++) if (isLeap(y)) c++;\n    printf(\"%d\\n\", c);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nbool isLeap(int y) {\n    if (y % 400 == 0) return true;\n    if (y % 100 == 0) return false;\n    return y % 4 == 0;\n}\nint main() {\n    int a, b;\n    if (scanf(\"%d %d\", &a, &b) != 2) return 0;\n    int c = 0;\n    for (int y = a; y <= b; y++) c += isLeap(y);\n    printf(\"%d\\n\", c);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "1900 2000\n",
                "expected_stdout": "25\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2000 2000\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1900 1900\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1 4\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1990 2020\n",
                "expected_stdout": "8\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2001 2099\n",
                "expected_stdout": "24\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【函数】内联函数求平方和",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "函数",
            "inline",
            "平方和"
        ],
        "statement_md": "写 `inline long long sq(long long x) { return x * x; }`，读入 `n`，输出 1² + 2² + … + n²。\n\n**关键点**\n\n- `inline` 只是给编译器的建议，`-O2` 下这种小函数本来就会被内联\n- `x * x` 里 `x` 必须是 `long long`，`int` 到 46341 就会溢出\n- n 到 10⁶ 时结果约 3.3×10¹⁷，`long long` 装得下",
        "input_format": "一行一个整数 `n`。",
        "output_format": "一行：平方和。",
        "constraints_md": "- 1 ≤ n ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 函数与参数传递",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\ninline long long sq(long long x) { return x * x; }\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    long long s = 0;\n    for (int i = 1; i <= n; i++) s += sq(i);\n    printf(\"%lld\\n\", s);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    long long n;\n    if (scanf(\"%lld\", &n) != 1) return 0;\n    printf(\"%lld\\n\", n * (n + 1) * (2 * n + 1) / 6);   // 闭式公式\n    return 0;\n}\n",
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
                "expected_stdout": "5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n",
                "expected_stdout": "14\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n",
                "expected_stdout": "385\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1000\n",
                "expected_stdout": "333833500\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1000000\n",
                "expected_stdout": "333333833333500000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【函数】函数指针选最大最小",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "函数",
            "函数指针",
            "lambda"
        ],
        "statement_md": "写一个函数 `int pick(int a[], int n, bool (*better)(int, int))`，用传入的比较函数决定是挑最大还是挑最小。读入 `n` 和 `n` 个整数，输出最大值与最小值。\n\n**关键点**\n\n- 函数指针参数写法：`bool (*better)(int, int)`，括号不能省，否则变成「返回函数指针的函数」\n- 把「怎么比」抽出来，挑最大和挑最小就是同一个函数换一个比较器\n- 输出一行，先最大值后最小值",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：`max min`。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 函数与参数传递",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nbool greaterThan(int a, int b) { return a > b; }\nbool lessThan(int a, int b)    { return a < b; }\nint pick(int a[], int n, bool (*better)(int, int)) {\n    int r = a[0];\n    for (int i = 1; i < n; i++) if (better(a[i], r)) r = a[i];\n    return r;\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    printf(\"%d %d\\n\", pick(a, n, greaterThan), pick(a, n, lessThan));\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\n#include <functional>\nint pick(int a[], int n, std::function<bool(int, int)> better) {   // 换成 std::function\n    int r = a[0];\n    for (int i = 1; i < n; i++) if (better(a[i], r)) r = a[i];\n    return r;\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    auto gt = [](int x, int y) { return x > y; };    // lambda 传进去\n    auto lt = [](int x, int y) { return x < y; };\n    printf(\"%d %d\\n\", pick(a, n, gt), pick(a, n, lt));\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n-9 15 29 -49 -17\n",
                "expected_stdout": "29 -49\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n-41\n",
                "expected_stdout": "-41 -41\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "20\n-29 -69 28 22 44 -54 18 -24 50 -82 24 3 32 28 -49 15 -72 -95 -35 5\n",
                "expected_stdout": "50 -95\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "50\n28 15 -36 -10 -35 -11 -27 -23 -6 -35 6 8 17 -15 7 -29 -10 -15 14 29 -50 38 15 -45 -34 -21 6 -31 26 3 -20 -16 -18 34 5 -50 20 -25 34 -30 22 -43 44 -23 41 -8 -45 -48 -48 38\n",
                "expected_stdout": "44 -50\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n3 3 3 3 3\n",
                "expected_stdout": "3 3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "9\n-539 -402 -553 -535 -958 -254 -214 -474 -311\n",
                "expected_stdout": "-214 -958\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【函数】函数统计各分数段人数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "函数",
            "分段统计"
        ],
        "statement_md": "写函数按 `[90,100]`、`[80,90)`、`[70,80)`、`[60,70)`、`[0,60)` 五档统计人数。读入 `n` 和 `n` 个成绩（0~100 的整数），按「优秀、良好、中等、及格、不及格」的顺序输出五个数字，一行，空格分隔。\n\n**关键点**\n\n- 区间是左闭右开，`90` 要落到第一档而不是第二档\n- 五档判断从高到低写 `if/else if` 就不会重叠\n- 输出五个整数",
        "input_format": "第一行 `n`，第二行 `n` 个整数成绩。",
        "output_format": "一行：五档人数。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 0 ≤ 成绩 ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 函数与参数传递",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nvoid countByBand(const int s[], int n, int c[5]) {\n    for (int i = 0; i < 5; i++) c[i] = 0;\n    for (int i = 0; i < n; i++) {\n        if (s[i] >= 90)      c[0]++;      // 从高到低，区间左闭右开不重叠\n        else if (s[i] >= 80) c[1]++;\n        else if (s[i] >= 70) c[2]++;\n        else if (s[i] >= 60) c[3]++;\n        else                 c[4]++;\n    }\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int s[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &s[i]);\n    int c[5];\n    countByBand(s, n, c);\n    for (int i = 0; i < 5; i++) printf(\"%d%c\", c[i], i == 4 ? '\\n' : ' ');\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint band(int x) {                       // 用「档位下标」把判断收敛成一次除法\n    if (x >= 90) return 0;\n    if (x < 60)  return 4;\n    return 4 - (x - 50) / 10;           // 60~69→3, 70~79→2, 80~89→1\n}\nint main() {\n    int n, c[5] = {0, 0, 0, 0, 0};\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    for (int i = 0; i < n; i++) { int x; scanf(\"%d\", &x); c[band(x)]++; }\n    printf(\"%d %d %d %d %d\\n\", c[0], c[1], c[2], c[3], c[4]);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n95 85 75 65 55\n",
                "expected_stdout": "1 1 1 1 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n100\n",
                "expected_stdout": "1 0 0 0 0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n0\n",
                "expected_stdout": "0 0 0 0 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n89 90 59 60\n",
                "expected_stdout": "1 1 0 1 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n100 99 80 79 70 69 60 59 0 90\n",
                "expected_stdout": "3 1 2 2 2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "40\n64 58 43 71 68 49 61 2 20 19 57 86 97 77 0 40 36 92 45 28 39 87 16 77 9 27 65 96 38 74 71 23 99 91 42 23 49 98 29 83\n",
                "expected_stdout": "6 3 5 4 22\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【递归】斐波那契数列第 n 项",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "递归",
            "斐波那契"
        ],
        "statement_md": "用递归求斐波那契数列：`F(1) = F(2) = 1`，`F(n) = F(n-1) + F(n-2)`。读入 `n`（1 ≤ n ≤ 30），输出 `F(n)`。\n\n**关键点**\n\n- 边界写在函数开头：`n <= 2` 直接返回 1\n- n 到 30 时朴素递归要算约 130 万次，能跑完；到 45 就明显卡了 —— 这是「递归树重复计算」的经典例子\n- 输出一个整数",
        "input_format": "一行一个整数 `n`。",
        "output_format": "一行：`F(n)`。",
        "constraints_md": "- 1 ≤ n ≤ 30",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 递归与递推",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nlong long fib(int n) {\n    if (n <= 2) return 1;             // 边界写最前\n    return fib(n - 1) + fib(n - 2);\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    printf(\"%lld\\n\", fib(n));\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    long long a = 1, b = 1;           // 迭代：只留最近两项\n    for (int i = 3; i <= n; i++) { long long c = a + b; a = b; b = c; }\n    printf(\"%lld\\n\", n <= 2 ? 1LL : b);\n    return 0;\n}\n",
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
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n",
                "expected_stdout": "55\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "20\n",
                "expected_stdout": "6765\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "30\n",
                "expected_stdout": "832040\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【递归】爬楼梯方案数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "递归",
            "递推",
            "爬楼梯"
        ],
        "statement_md": "楼梯有 `n` 级，每步只能走 1 级或 2 级。读入 `n`（1 ≤ n ≤ 40），输出走完的方案数。\n\n**关键点**\n\n- 最后一步要么是 1 级要么是 2 级，所以 `f(n) = f(n-1) + f(n-2)`\n- `f(1) = 1`、`f(2) = 2`，注意和斐波那契的初值不同\n- n = 40 时答案约 1.6×10⁸，`long long` 稳妥",
        "input_format": "一行一个整数 `n`。",
        "output_format": "一行：方案数。",
        "constraints_md": "- 1 ≤ n ≤ 40",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 递归与递推",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nlong long climb(int n) {\n    if (n == 1) return 1;\n    if (n == 2) return 2;\n    return climb(n - 1) + climb(n - 2);\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    printf(\"%lld\\n\", climb(n));\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    long long f[45] = {0, 1, 2};      // 递推表：从小到大填\n    for (int i = 3; i <= n; i++) f[i] = f[i - 1] + f[i - 2];\n    printf(\"%lld\\n\", f[n]);\n    return 0;\n}\n",
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
                "stdin": "3\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n",
                "expected_stdout": "8\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "20\n",
                "expected_stdout": "10946\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "40\n",
                "expected_stdout": "165580141\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【递归】汉诺塔移动次数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "递归",
            "汉诺塔",
            "位运算"
        ],
        "statement_md": "n 个盘子的汉诺塔最少需要移动多少次？读入 `n`（1 ≤ n ≤ 62），输出移动次数。\n\n**关键点**\n\n- 递推式 `T(n) = 2T(n-1) + 1`，闭式解是 `2^n - 1`\n- `1 << n` 在 n ≥ 31 时对 `int` 是未定义行为，必须写 `1LL << n`\n- n = 62 时结果是 4611686018427387903，还在 `long long` 内",
        "input_format": "一行一个整数 `n`。",
        "output_format": "一行：最少移动次数。",
        "constraints_md": "- 1 ≤ n ≤ 62",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 递归与递推",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nlong long hanoi(int n) {\n    if (n == 1) return 1;\n    return 2 * hanoi(n - 1) + 1;\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    printf(\"%lld\\n\", hanoi(n));\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    printf(\"%lld\\n\", (1LL << n) - 1);   // 必须 1LL，写 1<<62 是未定义行为\n    return 0;\n}\n",
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
                "expected_stdout": "3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n",
                "expected_stdout": "7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n",
                "expected_stdout": "1023\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "31\n",
                "expected_stdout": "2147483647\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "62\n",
                "expected_stdout": "4611686018427387903\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【递归】欧几里得求最大公约数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "递归",
            "gcd"
        ],
        "statement_md": "用递归写辗转相除法：`gcd(a, b) = gcd(b, a % b)`，`gcd(a, 0) = a`。读入 `a b`，输出最大公约数。\n\n**关键点**\n\n- 递归出口是 `b == 0`，此时 `a` 就是答案\n- `a % b` 在 `b > a` 时会自动交换一轮，不用提前判断大小\n- 输出一个整数",
        "input_format": "一行两个正整数 `a b`。",
        "output_format": "一行：最大公约数。",
        "constraints_md": "- 1 ≤ a, b ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 递归与递推",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint gcd(int a, int b) {\n    return b == 0 ? a : gcd(b, a % b);\n}\nint main() {\n    int a, b;\n    if (scanf(\"%d %d\", &a, &b) != 2) return 0;\n    printf(\"%d\\n\", gcd(a, b));\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int a, b;\n    if (scanf(\"%d %d\", &a, &b) != 2) return 0;\n    while (b) { int t = a % b; a = b; b = t; }   // 迭代版\n    printf(\"%d\\n\", a);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "12 18\n",
                "expected_stdout": "6\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 1\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "7 13\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1000000000 999999937\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "270 192\n",
                "expected_stdout": "6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "36 48\n",
                "expected_stdout": "12\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【递推】走方格路径数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "递推",
            "组合数",
            "路径"
        ],
        "statement_md": "一个 `n` 行 `m` 列的方格，从左下角走到右上角，每步只能向右或向上。读入 `n m`，输出不同的走法数。\n\n**关键点**\n\n- 一共要走 `n + m` 步，其中向上 `n` 步、向右 `m` 步，答案是组合数 `C(n+m, n)`\n- 递推写法：`f[i][j] = f[i-1][j] + f[i][j-1]`，边界上都是 1\n- n, m ≤ 20 时答案最大约 1.4×10¹¹，用 `long long`",
        "input_format": "一行两个正整数 `n m`。",
        "output_format": "一行：走法数。",
        "constraints_md": "- 1 ≤ n, m ≤ 20",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 递归与递推",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nlong long f[25][25];\nint main() {\n    int n, m;\n    if (scanf(\"%d %d\", &n, &m) != 2) return 0;\n    for (int i = 0; i <= n; i++)\n        for (int j = 0; j <= m; j++) {\n            if (i == 0 || j == 0) f[i][j] = 1;              // 边界只有一条路\n            else f[i][j] = f[i - 1][j] + f[i][j - 1];\n        }\n    printf(\"%lld\\n\", f[n][m]);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n, m;\n    if (scanf(\"%d %d\", &n, &m) != 2) return 0;\n    long long c = 1;                      // 直接算组合数 C(n+m, n)\n    int k = n + m;\n    for (int i = 1; i <= n; i++) c = c * (k - i + 1) / i;\n    printf(\"%lld\\n\", c);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "1 1\n",
                "expected_stdout": "2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2 2\n",
                "expected_stdout": "6\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 3\n",
                "expected_stdout": "20\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10 10\n",
                "expected_stdout": "184756\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "20 20\n",
                "expected_stdout": "137846528820\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1 20\n",
                "expected_stdout": "21\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【递推】猴子吃桃逆推",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "递推",
            "逆推"
        ],
        "statement_md": "猴子第一天摘了若干个桃子，每天吃掉「现有桃子的一半再加一个」，到第 `n` 天早上只剩 1 个。读入 `n`（1 ≤ n ≤ 60），输出第一天摘了多少个。\n\n**关键点**\n\n- 正向是 `x/2 - 1`，逆推就是 `(x + 1) * 2`\n- 从第 n 天的 1 个往回推 `n-1` 次\n- n = 60 时答案约 3.5×10¹⁸，`long long` 刚好够",
        "input_format": "一行一个整数 `n`。",
        "output_format": "一行：第一天桃子数。",
        "constraints_md": "- 1 ≤ n ≤ 60",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 递归与递推",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    long long x = 1;                  // 第 n 天早上剩 1 个\n    for (int d = n; d > 1; d--) x = (x + 1) * 2;   // 逆推一步\n    printf(\"%lld\\n\", x);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nlong long back(long long x, int days) {     // 递归逆推\n    if (days <= 1) return x;\n    return back((x + 1) * 2, days - 1);\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    printf(\"%lld\\n\", back(1, n));\n    return 0;\n}\n",
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
                "expected_stdout": "4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n",
                "expected_stdout": "10\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n",
                "expected_stdout": "22\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n",
                "expected_stdout": "1534\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "60\n",
                "expected_stdout": "1729382256910270462\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【递推】杨辉三角第 n 行",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "递推",
            "杨辉三角"
        ],
        "statement_md": "用递推生成杨辉三角，读入 `n`（1 ≤ n ≤ 20），输出第 `n` 行的所有数，一行，空格分隔。\n\n**关键点**\n\n- 第 1 行是 `1`，第 2 行是 `1 1`，每行首尾都是 1\n- `a[i][j] = a[i-1][j-1] + a[i-1][j]`\n- 第 20 行最大项是 C(19,9) = 92378，`int` 够用",
        "input_format": "一行一个整数 `n`。",
        "output_format": "一行：第 `n` 行的 `n` 个数。",
        "constraints_md": "- 1 ≤ n ≤ 20",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 递归与递推",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    long long a[25][25] = {{0}};\n    for (int i = 0; i < n; i++) {\n        a[i][0] = a[i][i] = 1;                       // 首尾为 1\n        for (int j = 1; j < i; j++)\n            a[i][j] = a[i - 1][j - 1] + a[i - 1][j];\n    }\n    for (int j = 0; j < n; j++) printf(\"%lld%c\", a[n - 1][j], j + 1 == n ? '\\n' : ' ');\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    long long row[25] = {1};             // 一维滚动：从后往前更新\n    for (int i = 1; i < n; i++)\n        for (int j = i; j >= 1; j--) row[j] += row[j - 1];\n    for (int j = 0; j < n; j++) printf(\"%lld%c\", row[j], j + 1 == n ? '\\n' : ' ');\n    return 0;\n}\n",
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
                "expected_stdout": "1 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n",
                "expected_stdout": "1 2 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n",
                "expected_stdout": "1 4 6 4 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n",
                "expected_stdout": "1 9 36 84 126 126 84 36 9 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "20\n",
                "expected_stdout": "1 19 171 969 3876 11628 27132 50388 75582 92378 92378 75582 50388 27132 11628 3876 969 171 19 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【递推】调和级数前 n 项和",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "递推",
            "浮点",
            "调和级数"
        ],
        "statement_md": "读入 `n`（1 ≤ n ≤ 10⁵），输出 `1 + 1/2 + 1/3 + … + 1/n`，保留 6 位小数。\n\n**关键点**\n\n- `1 / i` 是整数除法，结果恒为 0（i = 1 时是 1），必须写 `1.0 / i`\n- 累加用 `double`\n- 输出用 `%.6f`",
        "input_format": "一行一个整数 `n`。",
        "output_format": "一行：和，保留 6 位小数。",
        "constraints_md": "- 1 ≤ n ≤ 100000",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 递归与递推",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    double s = 0;\n    for (int i = 1; i <= n; i++) s += 1.0 / i;   // 1.0 不能写成 1\n    printf(\"%.6f\\n\", s);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    double s = 0;\n    for (int i = n; i >= 1; i--) s += 1.0 / i;   // 倒着加，浮点误差略小\n    printf(\"%.6f\\n\", s);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "1\n",
                "expected_stdout": "1.000000\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n",
                "expected_stdout": "1.500000\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n",
                "expected_stdout": "1.833333\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n",
                "expected_stdout": "2.928968\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1000\n",
                "expected_stdout": "7.485471\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100000\n",
                "expected_stdout": "12.090146\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【递推】传球方案数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "递推",
            "环",
            "路径计数"
        ],
        "statement_md": "`n` 个人围成一圈（编号 1~n），球从 1 号开始，每次可以把球传给左边或右边的人，共传 `m` 次。读入 `n m`，输出传 `m` 次后球回到 1 号的不同路径数。\n\n**关键点**\n\n- 状态是「传了 k 次之后球在谁手里」，`dp[0][1] = 1`\n- 转移：`dp[k][i] = dp[k-1][i-1] + dp[k-1][i+1]`，下标首尾相接绕成环\n- n = 2 时左右是同一个人，两边的方案都要算，别去重",
        "input_format": "一行两个整数 `n m`。",
        "output_format": "一行：方案数。",
        "constraints_md": "- 2 ≤ n ≤ 20\n- 1 ≤ m ≤ 30",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 递归与递推",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nlong long dp[35][25];\nint main() {\n    int n, m;\n    if (scanf(\"%d %d\", &n, &m) != 2) return 0;\n    dp[0][1] = 1;\n    for (int k = 1; k <= m; k++)\n        for (int i = 1; i <= n; i++) {\n            int l = (i == 1) ? n : i - 1;        // 左边，绕回 n\n            int r = (i == n) ? 1 : i + 1;        // 右边，绕回 1\n            dp[k][i] = dp[k - 1][l] + dp[k - 1][r];\n        }\n    printf(\"%lld\\n\", dp[m][1]);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n, m;\n    if (scanf(\"%d %d\", &n, &m) != 2) return 0;\n    long long cur[25] = {0}, nxt[25] = {0};\n    cur[1] = 1;                                   // 一维滚动\n    for (int k = 1; k <= m; k++) {\n        for (int i = 1; i <= n; i++)\n            nxt[i] = cur[i == 1 ? n : i - 1] + cur[i == n ? 1 : i + 1];\n        for (int i = 1; i <= n; i++) cur[i] = nxt[i];\n    }\n    printf(\"%lld\\n\", cur[1]);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3 3\n",
                "expected_stdout": "2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2 2\n",
                "expected_stdout": "4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5 4\n",
                "expected_stdout": "6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10 10\n",
                "expected_stdout": "254\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "20 30\n",
                "expected_stdout": "155402532\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3 1\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【递推】斐波那契前 n 项和",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "递推",
            "斐波那契",
            "前缀和"
        ],
        "statement_md": "读入 `n`（1 ≤ n ≤ 60），输出斐波那契数列前 `n` 项之和（`F(1) = F(2) = 1`）。\n\n**关键点**\n\n- 边递推边累加最省事，也可以利用 `sum(n) = F(n+2) - 1`\n- n = 60 时 F(62) ≈ 4×10¹²，和也在 `long long` 内\n- 输出一个整数",
        "input_format": "一行一个整数 `n`。",
        "output_format": "一行：前 `n` 项和。",
        "constraints_md": "- 1 ≤ n ≤ 60",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 递归与递推",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    long long a = 1, b = 1, s = 0;\n    for (int i = 1; i <= n; i++) { s += a; long long c = a + b; a = b; b = c; }\n    printf(\"%lld\\n\", s);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    long long f[65] = {0, 1, 1};          // 先填表再求和\n    for (int i = 3; i <= n + 2; i++) f[i] = f[i - 1] + f[i - 2];\n    printf(\"%lld\\n\", f[n + 2] - 1);        // 用闭式：sum = F(n+2) - 1\n    return 0;\n}\n",
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
                "stdin": "3\n",
                "expected_stdout": "4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n",
                "expected_stdout": "143\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "30\n",
                "expected_stdout": "2178308\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "60\n",
                "expected_stdout": "4052739537880\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【递推】牛顿迭代求平方根",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "递推",
            "牛顿迭代",
            "浮点"
        ],
        "statement_md": "用牛顿迭代求 `√x`：`t = (t + x / t) / 2`，迭代到前后两次的差小于 `1e-12` 为止。读入正整数 `x`（1 ≤ x ≤ 10⁹），输出 `√x`，保留 6 位小数。\n\n**关键点**\n\n- 初值取 `t = x` 就行，收敛是二阶的，10 次左右就够\n- 循环条件写成 `while (fabs(nx - t) > 1e-12)`\n- `x / t` 里两个都是 `double`，不要写成整数除法",
        "input_format": "一行一个整数 `x`。",
        "output_format": "一行：`√x`，保留 6 位小数。",
        "constraints_md": "- 1 ≤ x ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 递归与递推",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <cmath>\nint main() {\n    int x;\n    if (scanf(\"%d\", &x) != 1) return 0;\n    double t = x;\n    for (int i = 0; i < 100; i++) {\n        double nx = (t + x / t) / 2.0;\n        if (fabs(nx - t) < 1e-12) { t = nx; break; }\n        t = nx;\n    }\n    printf(\"%.6f\\n\", t);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cmath>\nint main() {\n    int x;\n    if (scanf(\"%d\", &x) != 1) return 0;\n    printf(\"%.6f\\n\", sqrt((double)x));   // 库函数版\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "2\n",
                "expected_stdout": "1.414214\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "10\n",
                "expected_stdout": "3.162278\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "12345\n",
                "expected_stdout": "111.108056\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "999999937\n",
                "expected_stdout": "31622.775606\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7\n",
                "expected_stdout": "2.645751\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1000000\n",
                "expected_stdout": "1000.000000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【递推】卡特兰数（括号序列计数）",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "递推",
            "卡特兰数",
            "组合数"
        ],
        "statement_md": "n 对括号能组成多少种合法的括号序列？读入 `n`（1 ≤ n ≤ 15），输出卡特兰数 `C_n`。\n\n**关键点**\n\n- `C_n = C(2n, n) / (n + 1)`，也满足递推 `C_n = Σ C_i · C_{n-1-i}`\n- 直接算组合数时先乘后除，中途不会出现小数\n- n = 15 时 C₁₅ = 9694845，`long long` 绰绰有余",
        "input_format": "一行一个整数 `n`。",
        "output_format": "一行：`C_n`。",
        "constraints_md": "- 1 ≤ n ≤ 15",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 递归与递推",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nlong long cat[20];\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    cat[0] = 1;\n    for (int i = 1; i <= n; i++) {             // 用递推式，不碰除法\n        long long s = 0;\n        for (int j = 0; j < i; j++) s += cat[j] * cat[i - 1 - j];\n        cat[i] = s;\n    }\n    printf(\"%lld\\n\", cat[n]);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    long long c = 1;                           // 组合数公式，先乘后除\n    for (int i = 1; i <= n; i++) c = c * (n + i) / i;\n    printf(\"%lld\\n\", c / (n + 1));\n    return 0;\n}\n",
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
                "stdin": "3\n",
                "expected_stdout": "5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n",
                "expected_stdout": "42\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n",
                "expected_stdout": "16796\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "15\n",
                "expected_stdout": "9694845\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【递归】递归求 1 到 n 的和",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "递归",
            "求和"
        ],
        "statement_md": "用递归求 `1 + 2 + … + n`。读入 `n`（1 ≤ n ≤ 1000），输出和。\n\n**关键点**\n\n- 递归出口 `n == 1` 返回 1\n- 递归深度等于 n，n 到 10⁵ 会爆栈 —— 这正是「能用循环就别用递归」的场景\n- 输出一个整数",
        "input_format": "一行一个整数 `n`。",
        "output_format": "一行：和。",
        "constraints_md": "- 1 ≤ n ≤ 1000",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 递归与递推",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nlong long sumTo(int n) {\n    if (n == 1) return 1;              // 出口\n    return n + sumTo(n - 1);\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    printf(\"%lld\\n\", sumTo(n));\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    printf(\"%lld\\n\", (long long)n * (n + 1) / 2);   // 公式法，O(1)\n    return 0;\n}\n",
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
                "expected_stdout": "3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "10\n",
                "expected_stdout": "55\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100\n",
                "expected_stdout": "5050\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "999\n",
                "expected_stdout": "499500\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1000\n",
                "expected_stdout": "500500\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【递归】递归逆序输出数字",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "递归",
            "逆序",
            "数字"
        ],
        "statement_md": "把一个整数的各位数字逆序组成新整数。读入 `a`（|a| ≤ 10⁹），输出逆序后的数，去掉前导零，负号保留。\n\n**关键点**\n\n- `a = -1200` 的结果是 `-21`：符号与数值分开处理，前导零要去掉\n- `a = 0` 输出 `0`\n- 用 `long long` 存反转结果，避免中间溢出",
        "input_format": "一行一个整数 `a`。",
        "output_format": "一行：逆序后的整数。",
        "constraints_md": "- |a| ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 递归与递推",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    long long a;\n    if (scanf(\"%lld\", &a) != 1) return 0;\n    int sign = a < 0 ? -1 : 1;\n    long long v = a < 0 ? -a : a, r = 0;\n    while (v > 0) { r = r * 10 + v % 10; v /= 10; }   // 逐位拼新数\n    printf(\"%lld\\n\", sign * r);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cstring>\n#include <cstdlib>\nvoid rev(char *s, int i, int j) {        // 递归反转字符数组\n    if (i >= j) return;\n    char t = s[i]; s[i] = s[j]; s[j] = t;\n    rev(s, i + 1, j - 1);\n}\nint main() {\n    long long a;\n    if (scanf(\"%lld\", &a) != 1) return 0;\n    char buf[32];\n    snprintf(buf, sizeof(buf), \"%lld\", a < 0 ? -a : a);\n    rev(buf, 0, (int)strlen(buf) - 1);\n    long long r = atoll(buf);             // atoll 自动跳过前导零\n    printf(\"%lld\\n\", a < 0 ? -r : r);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "1200\n",
                "expected_stdout": "21\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "-1200\n",
                "expected_stdout": "-21\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "0\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7\n",
                "expected_stdout": "7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1000000000\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "-1000000001\n",
                "expected_stdout": "-1000000001\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【递归】递归求数组元素和",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "递归",
            "数组"
        ],
        "statement_md": "用递归求数组元素之和。读入 `n` 和 `n` 个整数（|x| ≤ 10⁶），输出总和。\n\n**关键点**\n\n- 递归形式：`sum(a, n) = a[n-1] + sum(a, n-1)`，出口是 `n == 0`\n- 和用 `long long`：10⁵ 个 10⁶ 就是 10¹¹\n- 输出一个整数",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：总和。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 递归与递推",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nlong long sumOf(const int a[], int n) {\n    if (n == 0) return 0;              // 出口：空数组和为 0\n    return a[n - 1] + sumOf(a, n - 1);\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    printf(\"%lld\\n\", sumOf(a, n));\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nlong long sumOf(const int *p, const int *end) {   // 指针区间递归\n    if (p == end) return 0;\n    return *p + sumOf(p + 1, end);\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    printf(\"%lld\\n\", sumOf(a, a + n));\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n-40 25 -28 37 36\n",
                "expected_stdout": "30\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n3\n",
                "expected_stdout": "3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "20\n13 22 42 -5 -36 -39 -5 -32 -28 0 -35 50 -30 24 -46 29 20 -35 36 29\n",
                "expected_stdout": "-26\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100\n119 -627 -746 687 -427 -381 -118 738 -966 407 20 -241 949 -375 -123 218 708 -439 966 100 -959 -109 -974 523 -108 -269 965 886 -70 -283 633 -563 375 480 -908 -158 -46 725 318 702 -673 -464 -730 -812 366 971 -385 -29 414 -433 771 -845 662 -233 -118 612 292 -286 -918 118 970 585 -962 -433 367 775 -538 -917 778 -79 -312 -506 -457 -651 -898 842 667 -660 403 597 525 -36 171 935 -580 813 -32 -967 463 948 -581 144 827 488 24 -785 313 472 381 477\n",
                "expected_stdout": "3480\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n-1 -2 -3\n",
                "expected_stdout": "-6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "200\n594174 115389 77551 544221 130828 643364 962002 812618 -730888 985928 35938 -939840 -707447 690121 -973022 260674 -822144 322937 -419844 693039 -593569 -905971 191203 514408 109746 276395 -591502 319461 360254 -770633 -245018 -412038 559550 668642 -188354 -215728 -677042 -624969 -612846 -178736 -287666 302118 -623647 259837 -168201 248761 -467685 67463 380653 -667266 -767382 541760 -794230 433039 -245221 833860 349469 -14892 -358306 -969913 -949082 -224339 443624 111572 113191 239291 -264134 -372262 945505 -221665 -585267 -97599 278927 891355 -201940 -742319 880847 -722475 639874 959715 -828515 180812 -937560 -970251 881906 -550918 374101 -182884 -513690 82024 -13969 740009 547749 376518 202649 -653832 442745 421705 -174353 469603 351682 313313 767701 -78477 -701055 211936 265263 -765368 -51721 580519 -37328 841421 921945 -606755 205445 -321733 -379083 -191550 997703 877462 63057 -592947 -422309 -704188 -522540 613181 -762556 -632183 161529 264518 -489870 -808236 864430 -987224 -580031 633226 604117 -64819 316391 521716 800928 -956033 -217854 614463 -385869 820863 615538 -651822 530266 734758 -149594 -532804 -481336 126353 -951089 249845 -239408 561723 645131 139113 -679788 -960730 336273 452302 -384665 -104500 -224780 -117204 903864 431934 2402 860799 -886711 68349 930320 635880 -59349 498508 -26893 -41729 -792449 456450 65412 -269835 -595715 -475029 -893891 -296664 -534403 -34798 -704682 -326189 840941 -857739 -711785 638188 -656156 279756 -452680 -535788\n",
                "expected_stdout": "-3944949\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【递归】递归二分查找",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "递归",
            "二分查找"
        ],
        "statement_md": "数组**严格递增**。读入 `n` 和 `x`，第二行 `n` 个整数，用递归二分查找 `x`，找到输出它的下标（从 1 开始），找不到输出 `-1`。\n\n**关键点**\n\n- 递归参数是区间 `[lo, hi]`，出口是 `lo > hi`\n- `mid = lo + (hi - lo) / 2` 比 `(lo + hi) / 2` 更能防溢出\n- 只输出一个整数",
        "input_format": "第一行 `n x`；第二行 `n` 个严格递增整数。",
        "output_format": "一行：下标（1 起）或 `-1`。",
        "constraints_md": "- 1 ≤ n ≤ 10⁵\n- |x|, |a[i]| ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 递归与递推",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint bs(const int a[], int lo, int hi, int x) {\n    if (lo > hi) return -1;                  // 出口：区间空了\n    int mid = lo + (hi - lo) / 2;\n    if (a[mid] == x) return mid + 1;         // 题目要 1 起\n    if (a[mid] < x)  return bs(a, mid + 1, hi, x);\n    return bs(a, lo, mid - 1, x);\n}\nint main() {\n    int n, x;\n    if (scanf(\"%d %d\", &n, &x) != 2) return 0;\n    static int a[100005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    printf(\"%d\\n\", bs(a, 0, n - 1, x));\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n, x;\n    if (scanf(\"%d %d\", &n, &x) != 2) return 0;\n    static int a[100005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int lo = 0, hi = n - 1, ans = -1;         // 迭代版，结果一样\n    while (lo <= hi) {\n        int mid = lo + (hi - lo) / 2;\n        if (a[mid] == x) { ans = mid + 1; break; }\n        if (a[mid] < x) lo = mid + 1; else hi = mid - 1;\n    }\n    printf(\"%d\\n\", ans);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 3\n1 3 5 7 9\n",
                "expected_stdout": "2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5 4\n1 3 5 7 9\n",
                "expected_stdout": "-1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 1\n1\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1 2\n1\n",
                "expected_stdout": "-1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10 17\n1 3 5 7 9 11 13 15 17 19\n",
                "expected_stdout": "9\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "20 100\n-20 -17 -14 -11 -8 -5 -2 1 4 7 10 13 16 19 22 25 28 31 34 37\n",
                "expected_stdout": "-1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【递推】整数划分方案数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "递推",
            "整数划分",
            "完全背包"
        ],
        "statement_md": "把正整数 `n` 拆成若干个正整数之和（不计顺序），有多少种拆法？读入 `n`（1 ≤ n ≤ 20），输出方案数。\n\n**关键点**\n\n- `p(1)=1, p(2)=2 (2 / 1+1), p(3)=3, p(4)=5, p(5)=7`\n- 按「允许用的最大加数」从小到大做背包式递推，就不会重复计数\n- n = 20 时 p(20) = 627，`int` 够",
        "input_format": "一行一个整数 `n`。",
        "output_format": "一行：方案数。",
        "constraints_md": "- 1 ≤ n ≤ 20",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 递归与递推",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    long long p[25] = {1};                  // p[0] = 1 是递推的起点\n    for (int part = 1; part <= n; part++)\n        for (int s = part; s <= n; s++)\n            p[s] += p[s - part];            // 完全背包：每个加数可用多次\n    printf(\"%lld\\n\", p[n]);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nlong long f[25][25];                        // f[i][j]：用不超过 j 的加数凑 i\nlong long ways(int i, int j) {\n    if (i == 0) return 1;\n    if (j == 0) return 0;\n    if (f[i][j]) return f[i][j];            // 记忆化\n    long long r = ways(i, j - 1);\n    if (j <= i) r += ways(i - j, j);\n    return f[i][j] = r;\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    printf(\"%lld\\n\", ways(n, n));\n    return 0;\n}\n",
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
                "stdin": "3\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n",
                "expected_stdout": "5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n",
                "expected_stdout": "7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "20\n",
                "expected_stdout": "627\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【递推】每次可走 1 到 3 级台阶",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "递推",
            "台阶"
        ],
        "statement_md": "楼梯有 `n` 级，每步可以走 1 级、2 级或 3 级。读入 `n`（1 ≤ n ≤ 40），输出走完的方案数。\n\n**关键点**\n\n- `f(n) = f(n-1) + f(n-2) + f(n-3)`\n- `f(1)=1, f(2)=2, f(3)=4`，别直接套斐波那契的初值\n- n = 40 时约 2.4×10⁸，`long long` 稳妥",
        "input_format": "一行一个整数 `n`。",
        "output_format": "一行：方案数。",
        "constraints_md": "- 1 ≤ n ≤ 40",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 递归与递推",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nlong long f[45] = {0, 1, 2, 4};\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    for (int i = 4; i <= n; i++) f[i] = f[i - 1] + f[i - 2] + f[i - 3];\n    printf(\"%lld\\n\", f[n]);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nlong long go(int n) {                        // 记忆化递归版（自顶向下）\n    if (n == 1) return 1;\n    if (n == 2) return 2;\n    if (n == 3) return 4;\n    static long long memo[50];\n    if (memo[n]) return memo[n];\n    return memo[n] = go(n - 1) + go(n - 2) + go(n - 3);\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    printf(\"%lld\\n\", go(n));\n    return 0;\n}\n",
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
                "stdin": "3\n",
                "expected_stdout": "4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n",
                "expected_stdout": "7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n",
                "expected_stdout": "274\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "40\n",
                "expected_stdout": "23837527729\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【递归】递归输出二进制",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "递归",
            "二进制",
            "回溯顺序"
        ],
        "statement_md": "用递归把一个正整数打印成二进制（不带前导零）。读入 `n`（1 ≤ n ≤ 10⁹），输出它的二进制表示。\n\n**关键点**\n\n- 先递归处理 `n / 2`，再打印 `n % 2`，顺序就正过来了\n- 出口是 `n == 0` 直接返回（什么都不打印），否则最高位会多一个 0\n- 输出一行 01 串",
        "input_format": "一行一个整数 `n`。",
        "output_format": "一行：二进制表示。",
        "constraints_md": "- 1 ≤ n ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 递归与递推",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nvoid toBin(int n) {\n    if (n == 0) return;          // 出口什么都不打印，避免前导 0\n    toBin(n / 2);\n    printf(\"%d\", n % 2);         // 回溯时打印，顺序才是高位在前\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    toBin(n);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    char s[40]; int k = 0;\n    while (n) { s[k++] = char('0' + n % 2); n /= 2; }   // 低位先入栈\n    while (k--) putchar(s[k]);                          // 倒着输出\n    printf(\"\\n\");\n    return 0;\n}\n",
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
                "expected_stdout": "10\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n",
                "expected_stdout": "101\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n",
                "expected_stdout": "1010\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1000000000\n",
                "expected_stdout": "111011100110101100101000000000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1023\n",
                "expected_stdout": "1111111111\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【递推】年龄问题",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "递推",
            "年龄"
        ],
        "statement_md": "第 1 个人 10 岁，后面每个人都比前一个人大 2 岁。读入 `n`（1 ≤ n ≤ 1000），输出第 `n` 个人的年龄。\n\n**关键点**\n\n- 递推式：`age(n) = age(n-1) + 2`，起点 `age(1) = 10`\n- 也可以直接算 `10 + 2 * (n - 1)`\n- 输出一个整数",
        "input_format": "一行一个整数 `n`。",
        "output_format": "一行：第 `n` 个人的年龄。",
        "constraints_md": "- 1 ≤ n ≤ 1000",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 递归与递推",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    int age = 10;\n    for (int i = 2; i <= n; i++) age += 2;   // 递推\n    printf(\"%d\\n\", age);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint ageOf(int n) {                  // 递归版\n    if (n == 1) return 10;\n    return ageOf(n - 1) + 2;\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    printf(\"%d\\n\", ageOf(n));\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "1\n",
                "expected_stdout": "10\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n",
                "expected_stdout": "12\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n",
                "expected_stdout": "14\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n",
                "expected_stdout": "28\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100\n",
                "expected_stdout": "208\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1000\n",
                "expected_stdout": "2008\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    }
]
