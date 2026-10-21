# -*- coding: utf-8 -*-
"""C++ 编程题第二册：循环结构 / 嵌套循环与图形（28 题） —— 自动生成，**不要手改本文件**。

生成器：tools/gen_cpp_basic2.py
题数：28 题 / 168 测试点 / 总分 346

重生成：python tools/gen_cpp_basic2.py
"""

CPP_BASIC2_PROBLEMS: list[dict] = [
    {
        "title": "【循环】1 到 n 求和",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "C++基础",
            "循环",
            "累加",
            "long long"
        ],
        "statement_md": "读入 `n` 个正整数，对每个输出 `1 + 2 + ... + n` 的和。\n\n**关键点**\n\n- `n` 最大 10⁹，`n(n+1)/2` 达 5×10¹⁷，必须用 `long long`\n- 循环累加和公式都能过，但公式更快；注意 `n * (n + 1)` 要在 long long 里做\n- 输出一行一个",
        "input_format": "第一行 `n`；第二行 `n` 个正整数。",
        "output_format": "`n` 行，每行一个整数。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 1 ≤ 值 ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 循环结构",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        long long x;\n        scanf(\"%lld\", &x);\n        long long s = 0;\n        for (long long i = 1; i <= x; i++) s += i;   // 老实累加\n        printf(\"%lld\\n\", s);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        long long x;\n        scanf(\"%lld\", &x);\n        printf(\"%lld\\n\", x * (x + 1) / 2);          // 等差数列公式\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 10 100\n",
                "expected_stdout": "1\n55\n5050\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n1000000000\n",
                "expected_stdout": "500000000500000000\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n999999999 500000000\n",
                "expected_stdout": "499999999500000000\n125000000250000000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n2 3 4 5\n",
                "expected_stdout": "3\n6\n10\n15\n",
                "is_sample": 0,
                "kind": "manual",
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
                "stdin": "3\n1000000 2000000 3000000\n",
                "expected_stdout": "500000500000\n2000001000000\n4500001500000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【循环】n 的阶乘",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "C++基础",
            "循环",
            "阶乘",
            "溢出"
        ],
        "statement_md": "读入 `n` 个整数（0 ≤ x ≤ 20），输出每个数的阶乘。\n\n**关键点**\n\n- `20! = 2432902008176640000`，`long long` 刚好装得下；`21!` 就溢出了\n- `0! = 1`，循环一次都不进，初值必须是 1 不是 0\n- 别用 `int`：13! 就已经超了",
        "input_format": "第一行 `n`；第二行 `n` 个整数。",
        "output_format": "`n` 行，每行一个整数。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 0 ≤ x ≤ 20",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 循环结构",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        int x;\n        scanf(\"%d\", &x);\n        long long f = 1;                 // 0! = 1\n        for (int i = 2; i <= x; i++) f *= i;\n        printf(\"%lld\\n\", f);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    long long f[21];\n    f[0] = 1;\n    for (int i = 1; i <= 20; i++) f[i] = f[i - 1] * i;   // 先打表\n    while (n--) {\n        int x;\n        scanf(\"%d\", &x);\n        printf(\"%lld\\n\", f[x]);\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n0 5 10\n",
                "expected_stdout": "1\n120\n3628800\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n20\n",
                "expected_stdout": "2432902008176640000\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n13 14\n",
                "expected_stdout": "6227020800\n87178291200\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n1 2 3 4\n",
                "expected_stdout": "1\n2\n6\n24\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n19\n",
                "expected_stdout": "121645100408832000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n15 16 17\n",
                "expected_stdout": "1307674368000\n20922789888000\n355687428096000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【循环】最大公约数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "循环",
            "辗转相除"
        ],
        "statement_md": "读入 `n` 对正整数，输出每对的最大公约数。\n\n**关键点**\n\n- 辗转相除：`while (b) { t = a % b; a = b; b = t; }`，最后 `a` 就是答案\n- 别用「从 1 试到较小数」的写法，虽然对但慢\n- 两数相等、其中一个为 1 都是边界",
        "input_format": "第一行 `n`；接下来 `n` 行，每行两个正整数。",
        "output_format": "`n` 行，每行一个整数。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 1 ≤ a, b ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 循环结构",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        long long a, b;\n        scanf(\"%lld %lld\", &a, &b);\n        while (b) {                     // 辗转相除\n            long long t = a % b;\n            a = b;\n            b = t;\n        }\n        printf(\"%lld\\n\", a);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nlong long gcd(long long a, long long b) {\n    return b == 0 ? a : gcd(b, a % b);   // 递归写法\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        long long a, b;\n        scanf(\"%lld %lld\", &a, &b);\n        printf(\"%lld\\n\", gcd(a, b));\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n12 18\n100 75\n7 13\n",
                "expected_stdout": "6\n25\n1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n1 1\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n1000000000 999999999\n1 1000000000\n",
                "expected_stdout": "1\n1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n48 18\n17 5\n36 60\n",
                "expected_stdout": "6\n1\n12\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n2147483647 3\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n6 6\n2 4\n",
                "expected_stdout": "6\n2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【循环】最小公倍数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "循环",
            "最小公倍数",
            "溢出"
        ],
        "statement_md": "读入 `n` 对正整数，输出每对的最小公倍数。\n\n**关键点**\n\n- `lcm = a / gcd(a, b) * b` —— 先除后乘，避免 `a*b` 溢出\n- 写成 `a * b / gcd` 在 `a, b` 接近 10⁹ 时会溢出 `long long`\n- 结果可能很大，用 `long long`",
        "input_format": "第一行 `n`；接下来 `n` 行，每行两个正整数。",
        "output_format": "`n` 行，每行一个整数。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 1 ≤ a, b ≤ 10⁹，保证 lcm ≤ 10¹⁸",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 循环结构",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        long long a, b;\n        scanf(\"%lld %lld\", &a, &b);\n        long long x = a, y = b;\n        while (y) { long long t = x % y; x = y; y = t; }   // x = gcd\n        printf(\"%lld\\n\", a / x * b);                        // 先除后乘\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <numeric>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        long long a, b;\n        scanf(\"%lld %lld\", &a, &b);\n        long long g = std::gcd(a, b);      // C++17 标准库直接给 gcd\n        printf(\"%lld\\n\", a / g * b);\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n12 18\n4 6\n7 13\n",
                "expected_stdout": "36\n12\n91\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n1 1\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n999999999 1000000000\n6 8\n",
                "expected_stdout": "999999999000000000\n24\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n21 6\n9 12\n",
                "expected_stdout": "42\n36\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n1000000000 999999999\n",
                "expected_stdout": "999999999000000000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n2 3\n5 7\n11 13\n",
                "expected_stdout": "6\n35\n143\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【循环】素数判定",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "循环",
            "素数",
            "平方根"
        ],
        "statement_md": "读入 `n` 个整数（≥ 2），判断是否素数，是输出 `YES`，否输出 `NO`。\n\n**关键点**\n\n- 试除到 `i * i > x` 就够了，不要除到 `x`\n- 1 和负数都不是素数，但本题数据 ≥ 2\n- `i * i` 可能溢出 `int`，用 `(long long)i * i`",
        "input_format": "第一行 `n`；第二行 `n` 个整数。",
        "output_format": "`n` 行，每行 `YES` 或 `NO`。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 2 ≤ x ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 循环结构",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        long long x;\n        scanf(\"%lld\", &x);\n        bool ok = true;\n        if (x < 2) ok = false;\n        for (long long i = 2; i * i <= x; i++) {     // 只试到平方根\n            if (x % i == 0) { ok = false; break; }\n        }\n        printf(\"%s\\n\", ok ? \"YES\" : \"NO\");\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cmath>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        long long x;\n        scanf(\"%lld\", &x);\n        bool ok = (x >= 2);\n        long long lim = (long long)std::sqrt((double)x) + 1;\n        for (long long i = 2; ok && i <= lim && i < x; i++) {\n            if (x % i == 0) ok = false;\n        }\n        printf(\"%s\\n\", ok ? \"YES\" : \"NO\");\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n2 3 4 9 17\n",
                "expected_stdout": "YES\nYES\nNO\nNO\nYES\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n1000000007\n",
                "expected_stdout": "YES\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n25 49 97 121\n",
                "expected_stdout": "NO\nNO\nYES\nNO\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n1000000000 999999937 1000003\n",
                "expected_stdout": "NO\nYES\nYES\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n5 6\n",
                "expected_stdout": "YES\nNO\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n7919 7920 7921\n",
                "expected_stdout": "YES\nNO\nNO\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【循环】分解质因数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "C++基础",
            "循环",
            "质因数"
        ],
        "statement_md": "读入 `n` 个整数（≥ 2），把每个数分解成质因数连乘的形式输出。\n\n格式要求：质因数按**从小到大**排列，用 `*` 连接，不合并相同的因子。\n\n例如 `12 = 2*2*3`，`97 = 97`。\n\n**关键点**\n\n- 从 2 开始试除，能除尽就一直除（`while (x % i == 0)`）\n- 除到 `i * i > x` 就停；此时若 `x > 1`，剩下的 `x` 本身就是一个质因数\n- 输出不能有行末的 `*`",
        "input_format": "第一行 `n`；第二行 `n` 个整数。",
        "output_format": "`n` 行，每行一个分解式。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 2 ≤ x ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 循环结构",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        long long x;\n        scanf(\"%lld\", &x);\n        bool first = true;\n        for (long long i = 2; i * i <= x; i++) {\n            while (x % i == 0) {\n                if (!first) printf(\"*\");\n                printf(\"%lld\", i);\n                first = false;\n                x /= i;\n            }\n        }\n        if (x > 1) {                      // 剩下的大质因子\n            if (!first) printf(\"*\");\n            printf(\"%lld\", x);\n        }\n        printf(\"\\n\");\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        long long x;\n        scanf(\"%lld\", &x);\n        long long f[64], cnt = 0;\n        for (long long d = 2; d * d <= x; d++)\n            while (x % d == 0) { f[cnt++] = d; x /= d; }\n        if (x > 1) f[cnt++] = x;\n        for (long long i = 0; i < cnt; i++) {      // 先存后打，省掉 first 标志\n            if (i) printf(\"*\");\n            printf(\"%lld\", f[i]);\n        }\n        printf(\"\\n\");\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n12 97 360\n",
                "expected_stdout": "2*2*3\n97\n2*2*2*3*3*5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n2\n",
                "expected_stdout": "2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n1000000007 1024\n",
                "expected_stdout": "1000000007\n2*2*2*2*2*2*2*2*2*2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n100 101 999999937\n",
                "expected_stdout": "2*2*5*5\n101\n999999937\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n999999999\n",
                "expected_stdout": "3*3*3*3*37*333667\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n30 210\n",
                "expected_stdout": "2*3*5\n2*3*5*7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【循环】n 以内的完全数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "C++基础",
            "循环",
            "完全数"
        ],
        "statement_md": "读入 `n` 个上界 `m`，输出不超过 `m` 的**全部完全数**（真因子之和等于自身）。\n\n输出按从小到大，空格分隔；若一个都没有，输出 `none`。\n\n**关键点**\n\n- 真因子是「除自己以外的因子」，判到 `i < x` 即可\n- 试除只到 `sqrt` 再配对能快一倍，但 `m ≤ 10000` 时朴素写法也够\n- 6、28、496、8128 是四位以内的全部完全数",
        "input_format": "第一行 `n`；第二行 `n` 个正整数。",
        "output_format": "`n` 行，每行若干个整数（空格分隔）或 `none`。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 1 ≤ m ≤ 10000",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 循环结构",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        int m;\n        scanf(\"%d\", &m);\n        bool any = false;\n        for (int x = 2; x <= m; x++) {\n            int s = 1;                        // 1 一定是真因子\n            for (int i = 2; i * i <= x; i++) {\n                if (x % i == 0) {\n                    s += i;\n                    if (i != x / i) s += x / i;\n                }\n            }\n            if (s == x) {\n                printf(any ? \" \" : \"\");\n                printf(\"%d\", x);\n                any = true;\n            }\n        }\n        if (!any) printf(\"none\");\n        printf(\"\\n\");\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static const int P[] = {6, 28, 496, 8128};     // 10000 以内就这四个\n    while (n--) {\n        int m;\n        scanf(\"%d\", &m);\n        bool any = false;\n        for (int i = 0; i < 4; i++) {\n            if (P[i] <= m) {\n                printf(any ? \" \" : \"\");\n                printf(\"%d\", P[i]);\n                any = true;\n            }\n        }\n        if (!any) printf(\"none\");\n        printf(\"\\n\");\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n10 30 10000\n",
                "expected_stdout": "6\n6 28\n6 28 496 8128\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n5\n",
                "expected_stdout": "none\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n6 28\n",
                "expected_stdout": "6\n6 28\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n496 8128\n",
                "expected_stdout": "6 28 496\n6 28 496 8128\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n1\n",
                "expected_stdout": "none\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n100 500 1000\n",
                "expected_stdout": "6 28\n6 28 496\n6 28 496\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【循环】斐波那契数列前 n 项",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "C++基础",
            "循环",
            "斐波那契"
        ],
        "statement_md": "读入 `n` 个整数 `k`，输出斐波那契数列的前 `k` 项（`F₁ = 1, F₂ = 1`），空格分隔。\n\n**关键点**\n\n- `F(n) = F(n-1) + F(n-2)`，用两个变量滚动即可，不必开数组\n- `k = 1` 时只输出 `1`；`k = 0` 时输出空行\n- 第 90 项已达 2.88×10¹⁸，`long long` 到第 92 项，本题 `k ≤ 90`",
        "input_format": "第一行 `n`；第二行 `n` 个整数。",
        "output_format": "`n` 行，每行 `k` 个整数，空格分隔。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 0 ≤ k ≤ 90",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 循环结构",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        int k;\n        scanf(\"%d\", &k);\n        long long a = 1, b = 1;\n        for (int i = 1; i <= k; i++) {\n            if (i > 1) printf(\" \");\n            printf(\"%lld\", a);\n            long long t = a + b;\n            a = b;\n            b = t;\n        }\n        printf(\"\\n\");\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    long long f[91];\n    f[0] = 0; f[1] = 1;\n    for (int i = 2; i <= 90; i++) f[i] = f[i - 1] + f[i - 2];   // 先打表\n    while (n--) {\n        int k;\n        scanf(\"%d\", &k);\n        for (int i = 1; i <= k; i++) {\n            if (i > 1) printf(\" \");\n            printf(\"%lld\", f[i]);\n        }\n        printf(\"\\n\");\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 5 10\n",
                "expected_stdout": "1\n1 1 2 3 5\n1 1 2 3 5 8 13 21 34 55\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n0\n",
                "expected_stdout": "\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n20 30\n",
                "expected_stdout": "1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597 2584 4181 6765\n1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597 2584 4181 6765 10946 17711 28657 46368 75025 121393 196418 317811 514229 832040\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n90\n",
                "expected_stdout": "1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597 2584 4181 6765 10946 17711 28657 46368 75025 121393 196418 317811 514229 832040 1346269 2178309 3524578 5702887 9227465 14930352 24157817 39088169 63245986 102334155 165580141 267914296 433494437 701408733 1134903170 1836311903 2971215073 4807526976 7778742049 12586269025 20365011074 32951280099 53316291173 86267571272 139583862445 225851433717 365435296162 591286729879 956722026041 1548008755920 2504730781961 4052739537881 6557470319842 10610209857723 17167680177565 27777890035288 44945570212853 72723460248141 117669030460994 190392490709135 308061521170129 498454011879264 806515533049393 1304969544928657 2111485077978050 3416454622906707 5527939700884757 8944394323791464 14472334024676221 23416728348467685 37889062373143906 61305790721611591 99194853094755497 160500643816367088 259695496911122585 420196140727489673 679891637638612258 1100087778366101931 1779979416004714189 2880067194370816120\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n2 3 4 6\n",
                "expected_stdout": "1 1\n1 1 2\n1 1 2 3\n1 1 2 3 5 8\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n45 50\n",
                "expected_stdout": "1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597 2584 4181 6765 10946 17711 28657 46368 75025 121393 196418 317811 514229 832040 1346269 2178309 3524578 5702887 9227465 14930352 24157817 39088169 63245986 102334155 165580141 267914296 433494437 701408733 1134903170\n1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597 2584 4181 6765 10946 17711 28657 46368 75025 121393 196418 317811 514229 832040 1346269 2178309 3524578 5702887 9227465 14930352 24157817 39088169 63245986 102334155 165580141 267914296 433494437 701408733 1134903170 1836311903 2971215073 4807526976 7778742049 12586269025\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【循环】整数反转",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "循环",
            "数字反转"
        ],
        "statement_md": "读入 `n` 个整数，输出它们**数字顺序反转**后的结果。\n\n负数保留负号；反转后前导的 0 不输出（`1200` 反转成 `21`）。\n\n**关键点**\n\n- `rev = rev * 10 + x % 10; x /= 10;` 是标准写法\n- 先取绝对值再反转，最后补负号，避免负数取模的符号问题\n- `x = 0` 输出 0；反转后可能溢出 `int`（如 2147483647 反转成 7463847412），用 `long long`",
        "input_format": "第一行 `n`；第二行 `n` 个整数。",
        "output_format": "`n` 行，每行一个整数。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- -10⁹ ≤ x ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 循环结构",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        long long x;\n        scanf(\"%lld\", &x);\n        bool neg = x < 0;\n        if (neg) x = -x;\n        long long r = 0;\n        while (x) { r = r * 10 + x % 10; x /= 10; }\n        printf(\"%lld\\n\", neg ? -r : r);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cstring>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        char buf[32];\n        scanf(\"%s\", buf);                 // 当字符串处理，天然去掉前导 0\n        int len = (int)strlen(buf), i = 0;\n        bool neg = (buf[0] == '-');\n        if (neg) i = 1;\n        printf(neg ? \"-\" : \"\");\n        while (len > i && buf[len - 1] == '0') len--;   // 掐掉尾部的 0\n        for (int k = len - 1; k >= i; k--) printf(\"%c\", buf[k]);\n        if (len == i) printf(\"0\");\n        printf(\"\\n\");\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4\n123 1200 -456 0\n",
                "expected_stdout": "321\n21\n-654\n0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n-1\n",
                "expected_stdout": "-1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n2147483647 -2147483647 1000000000\n",
                "expected_stdout": "7463847412\n-7463847412\n1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n10 100\n",
                "expected_stdout": "1\n1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n9\n",
                "expected_stdout": "9\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n1000000000 -1200 123456789\n",
                "expected_stdout": "1\n-21\n987654321\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【循环】位数统计与数位之和",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "循环",
            "数位"
        ],
        "statement_md": "读入 `n` 个非负整数，输出两个数：它的**位数**和**各位数字之和**，空格分隔。\n\n**关键点**\n\n- `x = 0` 是 1 位数，和为 0 —— 这是最容易漏的边界\n- `x /= 10` 直到 0，循环次数就是位数\n- 先转成字符串数长度也可以",
        "input_format": "第一行 `n`；第二行 `n` 个非负整数。",
        "output_format": "`n` 行，每行 `位数 各位和`。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 0 ≤ x ≤ 10¹²",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 循环结构",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        long long x;\n        scanf(\"%lld\", &x);\n        int cnt = 0, sum = 0;\n        if (x == 0) { cnt = 1; }          // 0 是 1 位数\n        while (x > 0) { cnt++; sum += (int)(x % 10); x /= 10; }\n        printf(\"%d %d\\n\", cnt, sum);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        char buf[32];\n        scanf(\"%s\", buf);\n        int cnt = 0, sum = 0;\n        for (int i = 0; buf[i]; i++) {\n            cnt++;\n            sum += buf[i] - '0';\n        }\n        printf(\"%d %d\\n\", cnt, sum);\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4\n0 7 12345 1000000000000\n",
                "expected_stdout": "1 0\n1 7\n5 15\n13 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n10\n",
                "expected_stdout": "2 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n9 99 999\n",
                "expected_stdout": "1 9\n2 18\n3 27\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n100 1000\n",
                "expected_stdout": "3 1\n4 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n987654321\n",
                "expected_stdout": "9 45\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n1 12 123\n",
                "expected_stdout": "1 1\n2 3\n3 6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【循环】十进制转二进制",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "循环",
            "进制转换"
        ],
        "statement_md": "读入 `n` 个非负整数，输出它们的二进制表示（不带 `0b` 前缀，无前导 0）。\n\n**关键点**\n\n- 除 2 取余、逆序排列；也可以从高位到低位用 `>>` 和 `&`\n- `0` 的答案是 `0`，不要输出空行\n- 位数最多 40 位，用 `long long` 或 `unsigned long long`",
        "input_format": "第一行 `n`；第二行 `n` 个非负整数。",
        "output_format": "`n` 行，每行一个 01 串。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 0 ≤ x ≤ 10¹²",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 循环结构",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        long long x;\n        scanf(\"%lld\", &x);\n        char b[64];\n        int len = 0;\n        if (x == 0) b[len++] = '0';\n        while (x) { b[len++] = (char)('0' + x % 2); x /= 2; }\n        for (int i = len - 1; i >= 0; i--) printf(\"%c\", b[i]);   // 逆序输出\n        printf(\"\\n\");\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        unsigned long long x;\n        scanf(\"%llu\", &x);\n        if (x == 0) { printf(\"0\\n\"); continue; }\n        int top = 63;\n        while (top > 0 && ((x >> top) & 1ULL) == 0) top--;   // 找最高位\n        for (int i = top; i >= 0; i--) printf(\"%d\", (int)((x >> i) & 1ULL));\n        printf(\"\\n\");\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n0 5 10\n",
                "expected_stdout": "0\n101\n1010\n",
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
                "stdin": "4\n255 1024 1000000000000 7\n",
                "expected_stdout": "11111111\n10000000000\n1110100011010100101001010001000000000000\n111\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n2147483647 4294967295\n",
                "expected_stdout": "1111111111111111111111111111111\n11111111111111111111111111111111\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n2\n",
                "expected_stdout": "10\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n3 4 8\n",
                "expected_stdout": "11\n100\n1000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【循环】自然常数 e 的近似值",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "C++基础",
            "循环",
            "级数",
            "浮点"
        ],
        "statement_md": "读入 `n` 个项数 `k`，用下面的级数算 `e` 的近似值（保留 4 位小数）：\n\n```\ne = 1/0! + 1/1! + 1/2! + ... + 1/k!\n```\n\n也就是累加**前 k+1 项**（k = 0 时只有 1）。\n\n**关键点**\n\n- 用 `t = t / i` 递推每一项，别每项都重算阶乘（会爆）\n- 累加变量用 `double`，从 `1.0` 起\n- `k` 大到 15 以后，再加的项小于 1e-13，对 4 位小数已无影响",
        "input_format": "第一行 `n`；第二行 `n` 个非负整数。",
        "output_format": "`n` 行，每行一个四位小数。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 0 ≤ k ≤ 15",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 循环结构",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        int k;\n        scanf(\"%d\", &k);\n        double sum = 1.0, term = 1.0;\n        for (int i = 1; i <= k; i++) {\n            term /= i;                 // 逐项递推 1/i!\n            sum += term;\n        }\n        printf(\"%.4f\\n\", sum);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        int k;\n        scanf(\"%d\", &k);\n        double fact = 1.0, sum = 1.0;\n        for (int i = 1; i <= k; i++) {\n            fact *= i;                 // 老老实实算阶乘\n            sum += 1.0 / fact;\n        }\n        printf(\"%.4f\\n\", sum);\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n0 1 5\n",
                "expected_stdout": "1.0000\n2.0000\n2.7167\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n10\n",
                "expected_stdout": "2.7183\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n15 3\n",
                "expected_stdout": "2.7183\n2.6667\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n2\n",
                "expected_stdout": "2.5000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n8 12\n",
                "expected_stdout": "2.7183\n2.7183\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n4\n",
                "expected_stdout": "2.7083\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【循环】莱布尼茨级数求 π",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "C++基础",
            "循环",
            "级数",
            "π"
        ],
        "statement_md": "用莱布尼茨级数计算 `π` 的近似值：\n\n```\nπ/4 = 1 - 1/3 + 1/5 - 1/7 + ...\n```\n\n读入 `n` 个项数 `k`，取级数**前 k 项**，输出 `π` 的近似值（保留 4 位小数）。\n\n**关键点**\n\n- 符号在每项后翻一次：`sign = -sign`\n- 分母是 `2*i + 1`（i 从 0 开始），别写成 `2*i - 1` 而漏掉第一项 1\n- k 越大收敛越慢：k = 1000 才到 3.1406，别以为是精度问题",
        "input_format": "第一行 `n`；第二行 `n` 个正整数。",
        "output_format": "`n` 行，每行一个四位小数。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 1 ≤ k ≤ 100000",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 循环结构",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        int k;\n        scanf(\"%d\", &k);\n        double s = 0.0;\n        int sign = 1;\n        for (int i = 0; i < k; i++) {\n            s += sign / (2.0 * i + 1.0);\n            sign = -sign;\n        }\n        printf(\"%.4f\\n\", s * 4.0);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        int k;\n        scanf(\"%d\", &k);\n        double s = 0.0;\n        for (int i = 0; i < k; i++) {\n            double t = 1.0 / (2.0 * i + 1.0);\n            if (i % 2 == 1) t = -t;      // 偶数项为正、奇数项为负\n            s += t;\n        }\n        printf(\"%.4f\\n\", s * 4.0);\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 2 10\n",
                "expected_stdout": "4.0000\n2.6667\n3.0418\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n1000\n",
                "expected_stdout": "3.1406\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n10000 100000\n",
                "expected_stdout": "3.1415\n3.1416\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n5 50\n",
                "expected_stdout": "3.3397\n3.1216\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n3\n",
                "expected_stdout": "3.4667\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n500 5000\n",
                "expected_stdout": "3.1396\n3.1414\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【循环】整数平方根",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "循环",
            "二分",
            "平方根"
        ],
        "statement_md": "读入 `n` 个非负整数，输出 `floor(sqrt(x))` —— 也就是**不超过真实平方根的最大整数**。\n\n**不许调用 `sqrt()`**，请用循环或二分自己求。\n\n**关键点**\n\n- `while ((r+1)*(r+1) <= x) r++;` 是最直观的写法，但对 10¹² 太慢\n- 改成二分：`lo = 0, hi = 10⁶+1`，找最后一个 `mid*mid <= x`\n- `mid * mid` 要用 `long long`，`int` 在 46341² 就溢出",
        "input_format": "第一行 `n`；第二行 `n` 个非负整数。",
        "output_format": "`n` 行，每行一个整数。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 0 ≤ x ≤ 10¹²",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 循环结构",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        long long x;\n        scanf(\"%lld\", &x);\n        long long lo = 0, hi = 1000001;\n        while (lo + 1 < hi) {                  // 二分找上界\n            long long mid = (lo + hi) / 2;\n            if (mid * mid <= x) lo = mid;\n            else hi = mid;\n        }\n        printf(\"%lld\\n\", lo);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        long long x;\n        scanf(\"%lld\", &x);\n        long long r = 0;\n        while ((r + 1) * (r + 1) <= x) r++;    // 逐步加一\n        printf(\"%lld\\n\", r);\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4\n0 1 15 16\n",
                "expected_stdout": "0\n1\n3\n4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n1000000000000\n",
                "expected_stdout": "1000000\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n2 3 4\n",
                "expected_stdout": "1\n1\n2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n999999999999 1000000\n",
                "expected_stdout": "999999\n1000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n26\n",
                "expected_stdout": "5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n99 100\n",
                "expected_stdout": "9\n10\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【循环】角谷猜想的步数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "循环",
            "角谷猜想"
        ],
        "statement_md": "对正整数 `x` 反复做：偶数除以 2，奇数乘 3 加 1，直到变成 1。输出所需的**步数**。\n\n读入 `n` 个正整数，每行输出一个步数。\n\n**关键点**\n\n- 用 `while (x != 1)`，每次改 `x` 并让计数加一\n- 奇数的 `3x+1` 可能超 `int`（如 10⁹ 级），用 `long long`\n- `x = 1` 时步数是 0，循环一次都不进",
        "input_format": "第一行 `n`；第二行 `n` 个正整数。",
        "output_format": "`n` 行，每行一个整数。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 1 ≤ x ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 循环结构",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        long long x;\n        scanf(\"%lld\", &x);\n        int step = 0;\n        while (x != 1) {\n            x = (x % 2 == 0) ? x / 2 : x * 3 + 1;\n            step++;\n        }\n        printf(\"%d\\n\", step);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        long long x;\n        scanf(\"%lld\", &x);\n        int step = 0;\n        while (x > 1) {\n            if (x & 1) x = 3 * x + 1;      // 用位与判奇偶\n            else       x >>= 1;            // 右移等价于除 2\n            step++;\n        }\n        printf(\"%d\\n\", step);\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4\n1 2 3 6\n",
                "expected_stdout": "0\n1\n7\n8\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n27\n",
                "expected_stdout": "111\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n97 871 77031\n",
                "expected_stdout": "118\n178\n350\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n1000000 999999\n",
                "expected_stdout": "152\n258\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n7\n",
                "expected_stdout": "16\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n10 20\n",
                "expected_stdout": "6\n7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【循环】1! 到 n! 的和",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "C++基础",
            "循环",
            "阶乘求和"
        ],
        "statement_md": "读入 `n` 个整数 `k`（0 ≤ k ≤ 20），输出 `1! + 2! + ... + k!`。\n\n`k = 0` 时和为 0。\n\n**关键点**\n\n- 边算阶乘边累加，复用上一次的阶乘结果，不要每项重算\n- `20! ≈ 2.43×10¹⁸`，累加和约 `2.56×10¹⁸`，`long long` 装得下\n- 用 `int` 会在 13! 处就错",
        "input_format": "第一行 `n`；第二行 `n` 个整数。",
        "output_format": "`n` 行，每行一个整数。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 0 ≤ k ≤ 20",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 循环结构",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        int k;\n        scanf(\"%d\", &k);\n        long long f = 1, s = 0;\n        for (int i = 1; i <= k; i++) {\n            f *= i;             // 复用上一次的阶乘\n            s += f;\n        }\n        printf(\"%lld\\n\", s);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    long long pref[21];\n    pref[0] = 0;\n    long long f = 1;\n    for (int i = 1; i <= 20; i++) { f *= i; pref[i] = pref[i - 1] + f; }  // 打表\n    while (n--) {\n        int k;\n        scanf(\"%d\", &k);\n        printf(\"%lld\\n\", pref[k]);\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n0 1 5\n",
                "expected_stdout": "0\n1\n153\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n20\n",
                "expected_stdout": "2561327494111820313\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n10 13\n",
                "expected_stdout": "4037913\n6749977113\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n2 3 4\n",
                "expected_stdout": "3\n9\n33\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n19\n",
                "expected_stdout": "128425485935180313\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n15 16\n",
                "expected_stdout": "1401602636313\n22324392524313\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【图形】九九乘法表",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "C++基础",
            "嵌套循环",
            "乘法表"
        ],
        "statement_md": "输出标准的下三角九九乘法表：第 `i` 行有 `i` 个式子，形如 `1*3=3 2*3=6 3*3=9`。\n\n**式子之间一个空格，行末不能有多余空格**，共 9 行。\n\n**关键点**\n\n- 外层 `i` 从 1 到 9，内层 `j` 从 1 到 `i`\n- 行末多打一个空格是本题最常见失分点：用 `if (j > 1) printf(\" \")` 控制\n- 乘号是小写字母 `*`，等号两边没有空格",
        "input_format": "无输入。",
        "output_format": "9 行，第 `i` 行 `i` 个式子。",
        "constraints_md": "- 固定输出，无输入\n- 式子格式 `j*i=积`",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 嵌套循环与图形",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    for (int i = 1; i <= 9; i++) {\n        for (int j = 1; j <= i; j++) {\n            if (j > 1) printf(\" \");          // 空格打在前面，行末就干净\n            printf(\"%d*%d=%d\", j, i, i * j);\n        }\n        printf(\"\\n\");\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\nusing namespace std;\nint main() {\n    for (int i = 1; i <= 9; i++) {\n        for (int j = 1; j <= i; j++) {\n            cout << j << \"*\" << i << \"=\" << i * j;\n            if (j != i) cout << \" \";\n        }\n        cout << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "\n",
                "expected_stdout": "1*1=1\n1*2=2 2*2=4\n1*3=3 2*3=6 3*3=9\n1*4=4 2*4=8 3*4=12 4*4=16\n1*5=5 2*5=10 3*5=15 4*5=20 5*5=25\n1*6=6 2*6=12 3*6=18 4*6=24 5*6=30 6*6=36\n1*7=7 2*7=14 3*7=21 4*7=28 5*7=35 6*7=42 7*7=49\n1*8=8 2*8=16 3*8=24 4*8=32 5*8=40 6*8=48 7*8=56 8*8=64\n1*9=9 2*9=18 3*9=27 4*9=36 5*9=45 6*9=54 7*9=63 8*9=72 9*9=81\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "\n",
                "expected_stdout": "1*1=1\n1*2=2 2*2=4\n1*3=3 2*3=6 3*3=9\n1*4=4 2*4=8 3*4=12 4*4=16\n1*5=5 2*5=10 3*5=15 4*5=20 5*5=25\n1*6=6 2*6=12 3*6=18 4*6=24 5*6=30 6*6=36\n1*7=7 2*7=14 3*7=21 4*7=28 5*7=35 6*7=42 7*7=49\n1*8=8 2*8=16 3*8=24 4*8=32 5*8=40 6*8=48 7*8=56 8*8=64\n1*9=9 2*9=18 3*9=27 4*9=36 5*9=45 6*9=54 7*9=63 8*9=72 9*9=81\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "\n",
                "expected_stdout": "1*1=1\n1*2=2 2*2=4\n1*3=3 2*3=6 3*3=9\n1*4=4 2*4=8 3*4=12 4*4=16\n1*5=5 2*5=10 3*5=15 4*5=20 5*5=25\n1*6=6 2*6=12 3*6=18 4*6=24 5*6=30 6*6=36\n1*7=7 2*7=14 3*7=21 4*7=28 5*7=35 6*7=42 7*7=49\n1*8=8 2*8=16 3*8=24 4*8=32 5*8=40 6*8=48 7*8=56 8*8=64\n1*9=9 2*9=18 3*9=27 4*9=36 5*9=45 6*9=54 7*9=63 8*9=72 9*9=81\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "\n",
                "expected_stdout": "1*1=1\n1*2=2 2*2=4\n1*3=3 2*3=6 3*3=9\n1*4=4 2*4=8 3*4=12 4*4=16\n1*5=5 2*5=10 3*5=15 4*5=20 5*5=25\n1*6=6 2*6=12 3*6=18 4*6=24 5*6=30 6*6=36\n1*7=7 2*7=14 3*7=21 4*7=28 5*7=35 6*7=42 7*7=49\n1*8=8 2*8=16 3*8=24 4*8=32 5*8=40 6*8=48 7*8=56 8*8=64\n1*9=9 2*9=18 3*9=27 4*9=36 5*9=45 6*9=54 7*9=63 8*9=72 9*9=81\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "\n",
                "expected_stdout": "1*1=1\n1*2=2 2*2=4\n1*3=3 2*3=6 3*3=9\n1*4=4 2*4=8 3*4=12 4*4=16\n1*5=5 2*5=10 3*5=15 4*5=20 5*5=25\n1*6=6 2*6=12 3*6=18 4*6=24 5*6=30 6*6=36\n1*7=7 2*7=14 3*7=21 4*7=28 5*7=35 6*7=42 7*7=49\n1*8=8 2*8=16 3*8=24 4*8=32 5*8=40 6*8=48 7*8=56 8*8=64\n1*9=9 2*9=18 3*9=27 4*9=36 5*9=45 6*9=54 7*9=63 8*9=72 9*9=81\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "\n",
                "expected_stdout": "1*1=1\n1*2=2 2*2=4\n1*3=3 2*3=6 3*3=9\n1*4=4 2*4=8 3*4=12 4*4=16\n1*5=5 2*5=10 3*5=15 4*5=20 5*5=25\n1*6=6 2*6=12 3*6=18 4*6=24 5*6=30 6*6=36\n1*7=7 2*7=14 3*7=21 4*7=28 5*7=35 6*7=42 7*7=49\n1*8=8 2*8=16 3*8=24 4*8=32 5*8=40 6*8=48 7*8=56 8*8=64\n1*9=9 2*9=18 3*9=27 4*9=36 5*9=45 6*9=54 7*9=63 8*9=72 9*9=81\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【图形】直角三角形星号",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "C++基础",
            "嵌套循环",
            "直角三角形"
        ],
        "statement_md": "读入 `n` 个整数 `h`，输出高为 `h` 的直角三角形，第 `i` 行有 `i` 个 `*`。\n\n每行末尾**不能有空格**，行之间不能有空行。\n\n**关键点**\n\n- 外层控制行，内层控制这一行打几个星号\n- 本题不需要打前导空格 —— 加了对不齐\n- `h = 0` 时什么都不输出（连空行也没有）",
        "input_format": "第一行 `n`；第二行 `n` 个整数。",
        "output_format": "对每个 `h`，输出 `h` 行。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 1 ≤ h ≤ 30",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 嵌套循环与图形",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        int h;\n        scanf(\"%d\", &h);\n        for (int i = 1; i <= h; i++) {\n            for (int j = 0; j < i; j++) printf(\"*\");\n            printf(\"\\n\");\n        }\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <string>\nusing namespace std;\nint main() {\n    int n;\n    cin >> n;\n    while (n--) {\n        int h;\n        cin >> h;\n        for (int i = 1; i <= h; i++) cout << string(i, '*') << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 3 5\n",
                "expected_stdout": "*\n*\n**\n***\n*\n**\n***\n****\n*****\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n1\n",
                "expected_stdout": "*\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n2 4\n",
                "expected_stdout": "*\n**\n*\n**\n***\n****\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n10\n",
                "expected_stdout": "*\n**\n***\n****\n*****\n******\n*******\n********\n*********\n**********\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n6 7\n",
                "expected_stdout": "*\n**\n***\n****\n*****\n******\n*\n**\n***\n****\n*****\n******\n*******\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n30\n",
                "expected_stdout": "*\n**\n***\n****\n*****\n******\n*******\n********\n*********\n**********\n***********\n************\n*************\n**************\n***************\n****************\n*****************\n******************\n*******************\n********************\n*********************\n**********************\n***********************\n************************\n*************************\n**************************\n***************************\n****************************\n*****************************\n******************************\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【图形】等腰三角形星号",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "嵌套循环",
            "等腰三角形"
        ],
        "statement_md": "读入 `n` 个整数 `h`，输出高为 `h` 的等腰三角形：第 `i` 行先打 `h-i` 个空格，再打 `2i-1` 个 `*`。\n\n**每行末尾不能有多余空格**。\n\n**关键点**\n\n- 空格数 = `h - i`，星号数 = `2*i - 1`\n- 两个内层循环：一个打空格，一个打星号\n- 行末的星号后面不要再补空格",
        "input_format": "第一行 `n`；第二行 `n` 个整数。",
        "output_format": "对每个 `h`，输出 `h` 行。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 1 ≤ h ≤ 30",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 嵌套循环与图形",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        int h;\n        scanf(\"%d\", &h);\n        for (int i = 1; i <= h; i++) {\n            for (int j = 0; j < h - i; j++) printf(\" \");\n            for (int j = 0; j < 2 * i - 1; j++) printf(\"*\");\n            printf(\"\\n\");\n        }\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <string>\nusing namespace std;\nint main() {\n    int n;\n    cin >> n;\n    while (n--) {\n        int h;\n        cin >> h;\n        for (int i = 1; i <= h; i++)\n            cout << string(h - i, ' ') << string(2 * i - 1, '*') << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 3 5\n",
                "expected_stdout": "*\n  *\n ***\n*****\n    *\n   ***\n  *****\n *******\n*********\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n2\n",
                "expected_stdout": " *\n***\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n4 6\n",
                "expected_stdout": "   *\n  ***\n *****\n*******\n     *\n    ***\n   *****\n  *******\n *********\n***********\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n10\n",
                "expected_stdout": "         *\n        ***\n       *****\n      *******\n     *********\n    ***********\n   *************\n  ***************\n *****************\n*******************\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n8 9\n",
                "expected_stdout": "       *\n      ***\n     *****\n    *******\n   *********\n  ***********\n *************\n***************\n        *\n       ***\n      *****\n     *******\n    *********\n   ***********\n  *************\n ***************\n*****************\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n15\n",
                "expected_stdout": "              *\n             ***\n            *****\n           *******\n          *********\n         ***********\n        *************\n       ***************\n      *****************\n     *******************\n    *********************\n   ***********************\n  *************************\n ***************************\n*****************************\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【图形】实心菱形",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "C++基础",
            "嵌套循环",
            "菱形"
        ],
        "statement_md": "读入 `n` 个**奇数** `h`，输出高为 `h` 的实心菱形。\n\n上半（含中间行）第 `i` 行：`h/2+1-i` 个空格 + `2i-1` 个 `*`；\n下半第 `i` 行：`i` 个空格 + `h-2i` 个 `*`。\n\n**关键点**\n\n- 菱形 = 上半 `(h+1)/2` 行 + 下半 `h/2` 行，两段分开写最清楚\n- 下半的空格从 1 开始递增，星号从 `h-2` 开始递减\n- `h = 1` 时只有一行一个星号",
        "input_format": "第一行 `n`；第二行 `n` 个奇数。",
        "output_format": "对每个 `h`，输出 `h` 行。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 1 ≤ h ≤ 31，h 为奇数",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 嵌套循环与图形",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        int h;\n        scanf(\"%d\", &h);\n        int up = (h + 1) / 2;\n        for (int i = 1; i <= up; i++) {              // 上半 + 中间行\n            for (int j = 0; j < up - i; j++) printf(\" \");\n            for (int j = 0; j < 2 * i - 1; j++) printf(\"*\");\n            printf(\"\\n\");\n        }\n        for (int i = 1; i <= h / 2; i++) {           // 下半\n            for (int j = 0; j < i; j++) printf(\" \");\n            for (int j = 0; j < h - 2 * i; j++) printf(\"*\");\n            printf(\"\\n\");\n        }\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <string>\nusing namespace std;\nint main() {\n    int n;\n    cin >> n;\n    while (n--) {\n        int h;\n        cin >> h;\n        int up = (h + 1) / 2;\n        for (int i = 1; i <= up; i++)\n            cout << string(up - i, ' ') << string(2 * i - 1, '*') << \"\\n\";\n        for (int i = 1; i <= h / 2; i++)\n            cout << string(i, ' ') << string(h - 2 * i, '*') << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 3 5\n",
                "expected_stdout": "*\n *\n***\n *\n  *\n ***\n*****\n ***\n  *\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n7\n",
                "expected_stdout": "   *\n  ***\n *****\n*******\n *****\n  ***\n   *\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n9 11\n",
                "expected_stdout": "    *\n   ***\n  *****\n *******\n*********\n *******\n  *****\n   ***\n    *\n     *\n    ***\n   *****\n  *******\n *********\n***********\n *********\n  *******\n   *****\n    ***\n     *\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n21\n",
                "expected_stdout": "          *\n         ***\n        *****\n       *******\n      *********\n     ***********\n    *************\n   ***************\n  *****************\n *******************\n*********************\n *******************\n  *****************\n   ***************\n    *************\n     ***********\n      *********\n       *******\n        *****\n         ***\n          *\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n13 15\n",
                "expected_stdout": "      *\n     ***\n    *****\n   *******\n  *********\n ***********\n*************\n ***********\n  *********\n   *******\n    *****\n     ***\n      *\n       *\n      ***\n     *****\n    *******\n   *********\n  ***********\n *************\n***************\n *************\n  ***********\n   *********\n    *******\n     *****\n      ***\n       *\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n31\n",
                "expected_stdout": "               *\n              ***\n             *****\n            *******\n           *********\n          ***********\n         *************\n        ***************\n       *****************\n      *******************\n     *********************\n    ***********************\n   *************************\n  ***************************\n *****************************\n*******************************\n *****************************\n  ***************************\n   *************************\n    ***********************\n     *********************\n      *******************\n       *****************\n        ***************\n         *************\n          ***********\n           *********\n            *******\n             *****\n              ***\n               *\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【图形】空心正方形",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "嵌套循环",
            "空心正方形"
        ],
        "statement_md": "读入 `n` 个整数 `s`，输出边长为 `s` 的空心正方形：第一行和最后一行是 `s` 个 `*`，中间各行是 `*` + `s-2` 个空格 + `*`。\n\n**关键点**\n\n- `s = 1` 时只有一行一个 `*`；`s = 2` 时两行都是 `**`（没有中间行）\n- 中间行不能打成 `*` + 空格 + `*` 而忘了宽度\n- 每行末尾无多余空格",
        "input_format": "第一行 `n`；第二行 `n` 个整数。",
        "output_format": "对每个 `s`，输出 `s` 行。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 1 ≤ s ≤ 20",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 嵌套循环与图形",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        int s;\n        scanf(\"%d\", &s);\n        for (int i = 0; i < s; i++) {\n            if (i == 0 || i == s - 1) {              // 上下两行整条\n                for (int j = 0; j < s; j++) printf(\"*\");\n            } else {\n                printf(\"*\");\n                for (int j = 0; j < s - 2; j++) printf(\" \");\n                printf(\"*\");\n            }\n            printf(\"\\n\");\n        }\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <string>\nusing namespace std;\nint main() {\n    int n;\n    cin >> n;\n    while (n--) {\n        int s;\n        cin >> s;\n        string full(s, '*');\n        string mid = \"*\" + string(s > 2 ? s - 2 : 0, ' ') + (s > 1 ? \"*\" : \"\");\n        cout << full << \"\\n\";\n        for (int i = 1; i < s - 1; i++) cout << mid << \"\\n\";\n        if (s > 1) cout << full << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 2 4\n",
                "expected_stdout": "*\n**\n**\n****\n*  *\n*  *\n****\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n3\n",
                "expected_stdout": "***\n* *\n***\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n5 6\n",
                "expected_stdout": "*****\n*   *\n*   *\n*   *\n*****\n******\n*    *\n*    *\n*    *\n*    *\n******\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n10\n",
                "expected_stdout": "**********\n*        *\n*        *\n*        *\n*        *\n*        *\n*        *\n*        *\n*        *\n**********\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n7 8\n",
                "expected_stdout": "*******\n*     *\n*     *\n*     *\n*     *\n*     *\n*******\n********\n*      *\n*      *\n*      *\n*      *\n*      *\n*      *\n********\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n20\n",
                "expected_stdout": "********************\n*                  *\n*                  *\n*                  *\n*                  *\n*                  *\n*                  *\n*                  *\n*                  *\n*                  *\n*                  *\n*                  *\n*                  *\n*                  *\n*                  *\n*                  *\n*                  *\n*                  *\n*                  *\n********************\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【图形】数字直角三角形",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "嵌套循环",
            "数字三角形"
        ],
        "statement_md": "读入 `n` 个整数 `h`，输出高为 `h` 的数字三角形：\n\n第 `i` 行先打 `h-i` 个空格，再依次打 `1` 到 `i`（不加分隔符）。\n\n**关键点**\n\n- 先空格后数字，两个内层循环\n- 数字之间没有空格，是连续的 `123...i`\n- `h = 3` 时输出 `  1` / ` 12` / `123`",
        "input_format": "第一行 `n`；第二行 `n` 个整数。",
        "output_format": "对每个 `h`，输出 `h` 行。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 1 ≤ h ≤ 9",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 嵌套循环与图形",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        int h;\n        scanf(\"%d\", &h);\n        for (int i = 1; i <= h; i++) {\n            for (int j = 0; j < h - i; j++) printf(\" \");\n            for (int j = 1; j <= i; j++) printf(\"%d\", j);\n            printf(\"\\n\");\n        }\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <string>\nusing namespace std;\nint main() {\n    int n;\n    cin >> n;\n    while (n--) {\n        int h;\n        cin >> h;\n        string digits = \"123456789\";\n        for (int i = 1; i <= h; i++)\n            cout << string(h - i, ' ') << digits.substr(0, i) << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 3 5\n",
                "expected_stdout": "1\n  1\n 12\n123\n    1\n   12\n  123\n 1234\n12345\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n9\n",
                "expected_stdout": "        1\n       12\n      123\n     1234\n    12345\n   123456\n  1234567\n 12345678\n123456789\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n2 4\n",
                "expected_stdout": " 1\n12\n   1\n  12\n 123\n1234\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n6\n",
                "expected_stdout": "     1\n    12\n   123\n  1234\n 12345\n123456\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n7 8\n",
                "expected_stdout": "      1\n     12\n    123\n   1234\n  12345\n 123456\n1234567\n       1\n      12\n     123\n    1234\n   12345\n  123456\n 1234567\n12345678\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n5\n",
                "expected_stdout": "    1\n   12\n  123\n 1234\n12345\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【图形】杨辉三角前 n 行",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "C++基础",
            "嵌套循环",
            "杨辉三角",
            "二维数组"
        ],
        "statement_md": "读入 `n` 个整数 `k`，输出杨辉三角的前 `k` 行。每行数字之间**一个空格**，行首无空格。\n\n例如 `k = 5`：\n\n```\n1\n1 1\n1 2 1\n1 3 3 1\n1 4 6 4 1\n```\n\n**关键点**\n\n- `a[i][j] = a[i-1][j-1] + a[i-1][j]`，边界 `a[i][0] = a[i][i] = 1`\n- 用一维数组从后往前推也行：`a[j] += a[j-1]`\n- 第 30 行中间的数约 1.4×10⁸，`int` 够；第 34 行才会超",
        "input_format": "第一行 `n`；第二行 `n` 个整数。",
        "output_format": "对每个 `k`，输出 `k` 行。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 1 ≤ k ≤ 30",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 嵌套循环与图形",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        int k;\n        scanf(\"%d\", &k);\n        long long a[32][32] = {0};\n        for (int i = 0; i < k; i++) {\n            a[i][0] = a[i][i] = 1;                    // 两边是 1\n            for (int j = 1; j < i; j++)\n                a[i][j] = a[i - 1][j - 1] + a[i - 1][j];\n            for (int j = 0; j <= i; j++) {\n                if (j) printf(\" \");\n                printf(\"%lld\", a[i][j]);\n            }\n            printf(\"\\n\");\n        }\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        int k;\n        scanf(\"%d\", &k);\n        long long a[32] = {0};\n        a[0] = 1;\n        for (int i = 0; i < k; i++) {\n            for (int j = i; j >= 1; j--) a[j] += a[j - 1];   // 一维从后往前推\n            for (int j = 0; j <= i; j++) {\n                if (j) printf(\" \");\n                printf(\"%lld\", a[j]);\n            }\n            printf(\"\\n\");\n        }\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 2 5\n",
                "expected_stdout": "1\n1\n1 1\n1\n1 1\n1 2 1\n1 3 3 1\n1 4 6 4 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n10\n",
                "expected_stdout": "1\n1 1\n1 2 1\n1 3 3 1\n1 4 6 4 1\n1 5 10 10 5 1\n1 6 15 20 15 6 1\n1 7 21 35 35 21 7 1\n1 8 28 56 70 56 28 8 1\n1 9 36 84 126 126 84 36 9 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n6 7\n",
                "expected_stdout": "1\n1 1\n1 2 1\n1 3 3 1\n1 4 6 4 1\n1 5 10 10 5 1\n1\n1 1\n1 2 1\n1 3 3 1\n1 4 6 4 1\n1 5 10 10 5 1\n1 6 15 20 15 6 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n20\n",
                "expected_stdout": "1\n1 1\n1 2 1\n1 3 3 1\n1 4 6 4 1\n1 5 10 10 5 1\n1 6 15 20 15 6 1\n1 7 21 35 35 21 7 1\n1 8 28 56 70 56 28 8 1\n1 9 36 84 126 126 84 36 9 1\n1 10 45 120 210 252 210 120 45 10 1\n1 11 55 165 330 462 462 330 165 55 11 1\n1 12 66 220 495 792 924 792 495 220 66 12 1\n1 13 78 286 715 1287 1716 1716 1287 715 286 78 13 1\n1 14 91 364 1001 2002 3003 3432 3003 2002 1001 364 91 14 1\n1 15 105 455 1365 3003 5005 6435 6435 5005 3003 1365 455 105 15 1\n1 16 120 560 1820 4368 8008 11440 12870 11440 8008 4368 1820 560 120 16 1\n1 17 136 680 2380 6188 12376 19448 24310 24310 19448 12376 6188 2380 680 136 17 1\n1 18 153 816 3060 8568 18564 31824 43758 48620 43758 31824 18564 8568 3060 816 153 18 1\n1 19 171 969 3876 11628 27132 50388 75582 92378 92378 75582 50388 27132 11628 3876 969 171 19 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n3 4\n",
                "expected_stdout": "1\n1 1\n1 2 1\n1\n1 1\n1 2 1\n1 3 3 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n30\n",
                "expected_stdout": "1\n1 1\n1 2 1\n1 3 3 1\n1 4 6 4 1\n1 5 10 10 5 1\n1 6 15 20 15 6 1\n1 7 21 35 35 21 7 1\n1 8 28 56 70 56 28 8 1\n1 9 36 84 126 126 84 36 9 1\n1 10 45 120 210 252 210 120 45 10 1\n1 11 55 165 330 462 462 330 165 55 11 1\n1 12 66 220 495 792 924 792 495 220 66 12 1\n1 13 78 286 715 1287 1716 1716 1287 715 286 78 13 1\n1 14 91 364 1001 2002 3003 3432 3003 2002 1001 364 91 14 1\n1 15 105 455 1365 3003 5005 6435 6435 5005 3003 1365 455 105 15 1\n1 16 120 560 1820 4368 8008 11440 12870 11440 8008 4368 1820 560 120 16 1\n1 17 136 680 2380 6188 12376 19448 24310 24310 19448 12376 6188 2380 680 136 17 1\n1 18 153 816 3060 8568 18564 31824 43758 48620 43758 31824 18564 8568 3060 816 153 18 1\n1 19 171 969 3876 11628 27132 50388 75582 92378 92378 75582 50388 27132 11628 3876 969 171 19 1\n1 20 190 1140 4845 15504 38760 77520 125970 167960 184756 167960 125970 77520 38760 15504 4845 1140 190 20 1\n1 21 210 1330 5985 20349 54264 116280 203490 293930 352716 352716 293930 203490 116280 54264 20349 5985 1330 210 21 1\n1 22 231 1540 7315 26334 74613 170544 319770 497420 646646 705432 646646 497420 319770 170544 74613 26334 7315 1540 231 22 1\n1 23 253 1771 8855 33649 100947 245157 490314 817190 1144066 1352078 1352078 1144066 817190 490314 245157 100947 33649 8855 1771 253 23 1\n1 24 276 2024 10626 42504 134596 346104 735471 1307504 1961256 2496144 2704156 2496144 1961256 1307504 735471 346104 134596 42504 10626 2024 276 24 1\n1 25 300 2300 12650 53130 177100 480700 1081575 2042975 3268760 4457400 5200300 5200300 4457400 3268760 2042975 1081575 480700 177100 53130 12650 2300 300 25 1\n1 26 325 2600 14950 65780 230230 657800 1562275 3124550 5311735 7726160 9657700 10400600 9657700 7726160 5311735 3124550 1562275 657800 230230 65780 14950 2600 325 26 1\n1 27 351 2925 17550 80730 296010 888030 2220075 4686825 8436285 13037895 17383860 20058300 20058300 17383860 13037895 8436285 4686825 2220075 888030 296010 80730 17550 2925 351 27 1\n1 28 378 3276 20475 98280 376740 1184040 3108105 6906900 13123110 21474180 30421755 37442160 40116600 37442160 30421755 21474180 13123110 6906900 3108105 1184040 376740 98280 20475 3276 378 28 1\n1 29 406 3654 23751 118755 475020 1560780 4292145 10015005 20030010 34597290 51895935 67863915 77558760 77558760 67863915 51895935 34597290 20030010 10015005 4292145 1560780 475020 118755 23751 3654 406 29 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【图形】100 以内素数（每行 5 个）",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "嵌套循环",
            "素数",
            "排版"
        ],
        "statement_md": "输出 100 以内的全部素数，**每行 5 个**，数字之间一个空格，最后一行不足 5 个就照常结束。\n\n**关键点**\n\n- 先判素数，再控制换行：`if (cnt % 5 == 0) printf(\"\\n\")`\n- 计数器从 0 开始，每输出一个加一\n- 行末不要多打空格",
        "input_format": "无输入。",
        "output_format": "若干行，每行至多 5 个整数。",
        "constraints_md": "- 固定输出，无输入\n- 2 ~ 100 之间的素数",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 嵌套循环与图形",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int cnt = 0;\n    for (int x = 2; x <= 100; x++) {\n        bool ok = true;\n        for (int i = 2; i * i <= x; i++)\n            if (x % i == 0) { ok = false; break; }\n        if (!ok) continue;\n        if (cnt % 5 == 0) { if (cnt) printf(\"\\n\"); }\n        else printf(\" \");\n        printf(\"%d\", x);\n        cnt++;\n    }\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int p[30], m = 0;\n    for (int x = 2; x <= 100; x++) {              // 先收集\n        bool ok = true;\n        for (int i = 2; i * i <= x; i++) if (x % i == 0) { ok = false; break; }\n        if (ok) p[m++] = x;\n    }\n    for (int i = 0; i < m; i++) {                 // 再排版\n        if (i % 5 == 0) { if (i) printf(\"\\n\"); }\n        else printf(\" \");\n        printf(\"%d\", p[i]);\n    }\n    printf(\"\\n\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "\n",
                "expected_stdout": "2 3 5 7 11\n13 17 19 23 29\n31 37 41 43 47\n53 59 61 67 71\n73 79 83 89 97\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "\n",
                "expected_stdout": "2 3 5 7 11\n13 17 19 23 29\n31 37 41 43 47\n53 59 61 67 71\n73 79 83 89 97\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "\n",
                "expected_stdout": "2 3 5 7 11\n13 17 19 23 29\n31 37 41 43 47\n53 59 61 67 71\n73 79 83 89 97\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "\n",
                "expected_stdout": "2 3 5 7 11\n13 17 19 23 29\n31 37 41 43 47\n53 59 61 67 71\n73 79 83 89 97\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "\n",
                "expected_stdout": "2 3 5 7 11\n13 17 19 23 29\n31 37 41 43 47\n53 59 61 67 71\n73 79 83 89 97\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "\n",
                "expected_stdout": "2 3 5 7 11\n13 17 19 23 29\n31 37 41 43 47\n53 59 61 67 71\n73 79 83 89 97\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【图形】三位水仙花数（全部）",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "嵌套循环",
            "水仙花数"
        ],
        "statement_md": "输出所有三位水仙花数（各位数字立方和等于自身），一行内空格分隔。\n\n**关键点**\n\n- 枚举 100~999，拆出百十个位再验算\n- 结果只有 4 个，别漏 407\n- 行末无空格",
        "input_format": "无输入。",
        "output_format": "一行，若干个整数（空格分隔）。",
        "constraints_md": "- 固定输出，无输入\n- 三位数范围",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 嵌套循环与图形",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    bool first = true;\n    for (int x = 100; x <= 999; x++) {\n        int a = x / 100, b = x / 10 % 10, c = x % 10;\n        if (a * a * a + b * b * b + c * c * c != x) continue;\n        if (!first) printf(\" \");\n        printf(\"%d\", x);\n        first = false;\n    }\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int res[16], m = 0;\n    for (int a = 1; a <= 9; a++)          // 直接枚举三个数字，不用拆位\n        for (int b = 0; b <= 9; b++)\n            for (int c = 0; c <= 9; c++) {\n                int x = a * 100 + b * 10 + c;\n                if (a * a * a + b * b * b + c * c * c == x) res[m++] = x;\n            }\n    for (int i = 0; i < m; i++) {\n        if (i) printf(\" \");               // 空格打在前头，行末才干净\n        printf(\"%d\", res[i]);\n    }\n    printf(\"\\n\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "\n",
                "expected_stdout": "153 370 371 407\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "\n",
                "expected_stdout": "153 370 371 407\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "\n",
                "expected_stdout": "153 370 371 407\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "\n",
                "expected_stdout": "153 370 371 407\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "\n",
                "expected_stdout": "153 370 371 407\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "\n",
                "expected_stdout": "153 370 371 407\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【图形】字母倒三角",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "嵌套循环",
            "字符"
        ],
        "statement_md": "读入 `n` 个整数 `h`，每行从 `A` 开始连续输出字母：第一行 `h` 个，第二行 `h-1` 个，…，最后一行 1 个。\n\n例如 `h = 3`：`ABC` / `AB` / `A`。\n\n**关键点**\n\n- 第 `i` 行输出前 `h-i+1` 个字母\n- 字符用 `printf(\"%c\", 'A' + k)` 生成，不要手写 26 个 case\n- `h ≤ 26`，超过 26 个字母本题不涉及",
        "input_format": "第一行 `n`；第二行 `n` 个整数。",
        "output_format": "对每个 `h`，输出 `h` 行。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 1 ≤ h ≤ 26",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 嵌套循环与图形",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        int h;\n        scanf(\"%d\", &h);\n        for (int i = 1; i <= h; i++) {\n            for (int k = 0; k <= h - i; k++) printf(\"%c\", 'A' + k);\n            printf(\"\\n\");\n        }\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <string>\nusing namespace std;\nint main() {\n    int n;\n    cin >> n;\n    string letters = \"ABCDEFGHIJKLMNOPQRSTUVWXYZ\";\n    while (n--) {\n        int h;\n        cin >> h;\n        for (int i = h; i >= 1; i--) cout << letters.substr(0, i) << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 3 5\n",
                "expected_stdout": "A\nABC\nAB\nA\nABCDE\nABCD\nABC\nAB\nA\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n26\n",
                "expected_stdout": "ABCDEFGHIJKLMNOPQRSTUVWXYZ\nABCDEFGHIJKLMNOPQRSTUVWXY\nABCDEFGHIJKLMNOPQRSTUVWX\nABCDEFGHIJKLMNOPQRSTUVW\nABCDEFGHIJKLMNOPQRSTUV\nABCDEFGHIJKLMNOPQRSTU\nABCDEFGHIJKLMNOPQRST\nABCDEFGHIJKLMNOPQRS\nABCDEFGHIJKLMNOPQR\nABCDEFGHIJKLMNOPQ\nABCDEFGHIJKLMNOP\nABCDEFGHIJKLMNO\nABCDEFGHIJKLMN\nABCDEFGHIJKLM\nABCDEFGHIJKL\nABCDEFGHIJK\nABCDEFGHIJ\nABCDEFGHI\nABCDEFGH\nABCDEFG\nABCDEF\nABCDE\nABCD\nABC\nAB\nA\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n2 4\n",
                "expected_stdout": "AB\nA\nABCD\nABC\nAB\nA\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n13\n",
                "expected_stdout": "ABCDEFGHIJKLM\nABCDEFGHIJKL\nABCDEFGHIJK\nABCDEFGHIJ\nABCDEFGHI\nABCDEFGH\nABCDEFG\nABCDEF\nABCDE\nABCD\nABC\nAB\nA\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n6 7\n",
                "expected_stdout": "ABCDEF\nABCDE\nABCD\nABC\nAB\nA\nABCDEFG\nABCDEF\nABCDE\nABCD\nABC\nAB\nA\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n20\n",
                "expected_stdout": "ABCDEFGHIJKLMNOPQRST\nABCDEFGHIJKLMNOPQRS\nABCDEFGHIJKLMNOPQR\nABCDEFGHIJKLMNOPQ\nABCDEFGHIJKLMNOP\nABCDEFGHIJKLMNO\nABCDEFGHIJKLMN\nABCDEFGHIJKLM\nABCDEFGHIJKL\nABCDEFGHIJK\nABCDEFGHIJ\nABCDEFGHI\nABCDEFGH\nABCDEFG\nABCDEF\nABCDE\nABCD\nABC\nAB\nA\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【图形】蛇形数字方阵",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "C++基础",
            "嵌套循环",
            "二维数组",
            "模拟"
        ],
        "statement_md": "读入 `n` 个整数 `s`，输出 `s×s` 的方阵：从 1 开始按**蛇形**填数 ——\n\n第 1 行从左到右，第 2 行从右到左，第 3 行从左到右，以此类推。\n\n数字之间一个空格，行末无空格。\n\n**关键点**\n\n- 偶数行（下标 1、3、5…）反向填：`a[i][j] = s*s - i*s + (s-j)`？不如直接反向循环\n- 用一个递增计数器 `v`，按行方向决定内层从 0 到 s-1 还是从 s-1 到 0\n- `s = 1` 时只有 `1`",
        "input_format": "第一行 `n`；第二行 `n` 个整数。",
        "output_format": "对每个 `s`，输出 `s` 行。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 1 ≤ s ≤ 15",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 嵌套循环与图形",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        int s;\n        scanf(\"%d\", &s);\n        int v = 1;\n        for (int i = 0; i < s; i++) {\n            if (i % 2 == 0) {                       // 偶数行正着来\n                for (int j = 0; j < s; j++) {\n                    if (j) printf(\" \");\n                    printf(\"%d\", v++);\n                }\n            } else {                                // 奇数行反着来\n                int start = v + s - 1;\n                for (int j = 0; j < s; j++) {\n                    if (j) printf(\" \");\n                    printf(\"%d\", start - j);\n                }\n                v += s;\n            }\n            printf(\"\\n\");\n        }\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        int s;\n        scanf(\"%d\", &s);\n        int a[16][16], v = 1;\n        for (int i = 0; i < s; i++) {\n            int dir = (i % 2 == 0) ? 1 : -1;\n            int j = (dir == 1) ? 0 : s - 1;\n            for (int t = 0; t < s; t++) {           // 先填进数组\n                a[i][j] = v++;\n                j += dir;\n            }\n        }\n        for (int i = 0; i < s; i++) {               // 再统一打印\n            for (int j = 0; j < s; j++) {\n                if (j) printf(\" \");\n                printf(\"%d\", a[i][j]);\n            }\n            printf(\"\\n\");\n        }\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 2 3\n",
                "expected_stdout": "1\n1 2\n4 3\n1 2 3\n6 5 4\n7 8 9\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n4\n",
                "expected_stdout": "1 2 3 4\n8 7 6 5\n9 10 11 12\n16 15 14 13\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n5 6\n",
                "expected_stdout": "1 2 3 4 5\n10 9 8 7 6\n11 12 13 14 15\n20 19 18 17 16\n21 22 23 24 25\n1 2 3 4 5 6\n12 11 10 9 8 7\n13 14 15 16 17 18\n24 23 22 21 20 19\n25 26 27 28 29 30\n36 35 34 33 32 31\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n10\n",
                "expected_stdout": "1 2 3 4 5 6 7 8 9 10\n20 19 18 17 16 15 14 13 12 11\n21 22 23 24 25 26 27 28 29 30\n40 39 38 37 36 35 34 33 32 31\n41 42 43 44 45 46 47 48 49 50\n60 59 58 57 56 55 54 53 52 51\n61 62 63 64 65 66 67 68 69 70\n80 79 78 77 76 75 74 73 72 71\n81 82 83 84 85 86 87 88 89 90\n100 99 98 97 96 95 94 93 92 91\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n7 8\n",
                "expected_stdout": "1 2 3 4 5 6 7\n14 13 12 11 10 9 8\n15 16 17 18 19 20 21\n28 27 26 25 24 23 22\n29 30 31 32 33 34 35\n42 41 40 39 38 37 36\n43 44 45 46 47 48 49\n1 2 3 4 5 6 7 8\n16 15 14 13 12 11 10 9\n17 18 19 20 21 22 23 24\n32 31 30 29 28 27 26 25\n33 34 35 36 37 38 39 40\n48 47 46 45 44 43 42 41\n49 50 51 52 53 54 55 56\n64 63 62 61 60 59 58 57\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n15\n",
                "expected_stdout": "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15\n30 29 28 27 26 25 24 23 22 21 20 19 18 17 16\n31 32 33 34 35 36 37 38 39 40 41 42 43 44 45\n60 59 58 57 56 55 54 53 52 51 50 49 48 47 46\n61 62 63 64 65 66 67 68 69 70 71 72 73 74 75\n90 89 88 87 86 85 84 83 82 81 80 79 78 77 76\n91 92 93 94 95 96 97 98 99 100 101 102 103 104 105\n120 119 118 117 116 115 114 113 112 111 110 109 108 107 106\n121 122 123 124 125 126 127 128 129 130 131 132 133 134 135\n150 149 148 147 146 145 144 143 142 141 140 139 138 137 136\n151 152 153 154 155 156 157 158 159 160 161 162 163 164 165\n180 179 178 177 176 175 174 173 172 171 170 169 168 167 166\n181 182 183 184 185 186 187 188 189 190 191 192 193 194 195\n210 209 208 207 206 205 204 203 202 201 200 199 198 197 196\n211 212 213 214 215 216 217 218 219 220 221 222 223 224 225\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【图形】空心菱形",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 16,
        "tags": [
            "C++基础",
            "嵌套循环",
            "空心菱形"
        ],
        "statement_md": "读入 `n` 个**奇数** `h`，输出高为 `h` 的空心菱形：只有轮廓是 `*`，内部是空格。\n\n第 `i` 行（从上到下）只有在**最左**和**最右**的星号位置打 `*`，中间全空格；顶端和底端各只有一个 `*`。\n\n**行末的星号之后不能补空格**。\n\n**关键点**\n\n- 先算出每行宽度 `w`，再决定第一个和最后一个 `*` 的列号\n- 上半第 `i` 行：左星号在 `up-i`，右星号在 `up+i-2`（均从 0 计）\n- 下半与上半镜像：左星号在 `i`，右星号在 `h-i-1`\n- 首尾行左右星号重合，只打一个",
        "input_format": "第一行 `n`；第二行 `n` 个奇数。",
        "output_format": "对每个 `h`，输出 `h` 行。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 1 ≤ h ≤ 31，h 为奇数",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 嵌套循环与图形",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        int h;\n        scanf(\"%d\", &h);\n        int up = (h + 1) / 2;\n        for (int i = 1; i <= h; i++) {\n            int width = (i <= up) ? (2 * i - 1) : (2 * (h - i) + 1);  // 该行星号跨度\n            int pad = (h - width) / 2;                                // 左侧空格\n            for (int j = 0; j < pad; j++) printf(\" \");\n            printf(\"*\");\n            if (width > 1) {\n                for (int j = 0; j < width - 2; j++) printf(\" \");\n                printf(\"*\");\n            }\n            printf(\"\\n\");\n        }\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cstring>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        int h;\n        scanf(\"%d\", &h);\n        char line[64];\n        int up = (h + 1) / 2;\n        for (int i = 0; i < h; i++) {                // 先造一整行空格，再点两个星\n            int width = (i < up) ? (2 * (i + 1) - 1) : (2 * (h - i) - 1);\n            int pad = (h - width) / 2;\n            for (int j = 0; j < pad + width; j++) line[j] = ' ';\n            line[pad] = '*';\n            line[pad + width - 1] = '*';\n            line[pad + width] = '\\0';\n            printf(\"%s\\n\", line);\n        }\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 3 5\n",
                "expected_stdout": "*\n *\n* *\n *\n  *\n * *\n*   *\n * *\n  *\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n7\n",
                "expected_stdout": "   *\n  * *\n *   *\n*     *\n *   *\n  * *\n   *\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n9 11\n",
                "expected_stdout": "    *\n   * *\n  *   *\n *     *\n*       *\n *     *\n  *   *\n   * *\n    *\n     *\n    * *\n   *   *\n  *     *\n *       *\n*         *\n *       *\n  *     *\n   *   *\n    * *\n     *\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n21\n",
                "expected_stdout": "          *\n         * *\n        *   *\n       *     *\n      *       *\n     *         *\n    *           *\n   *             *\n  *               *\n *                 *\n*                   *\n *                 *\n  *               *\n   *             *\n    *           *\n     *         *\n      *       *\n       *     *\n        *   *\n         * *\n          *\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n13 15\n",
                "expected_stdout": "      *\n     * *\n    *   *\n   *     *\n  *       *\n *         *\n*           *\n *         *\n  *       *\n   *     *\n    *   *\n     * *\n      *\n       *\n      * *\n     *   *\n    *     *\n   *       *\n  *         *\n *           *\n*             *\n *           *\n  *         *\n   *       *\n    *     *\n     *   *\n      * *\n       *\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n31\n",
                "expected_stdout": "               *\n              * *\n             *   *\n            *     *\n           *       *\n          *         *\n         *           *\n        *             *\n       *               *\n      *                 *\n     *                   *\n    *                     *\n   *                       *\n  *                         *\n *                           *\n*                             *\n *                           *\n  *                         *\n   *                       *\n    *                     *\n     *                   *\n      *                 *\n       *               *\n        *             *\n         *           *\n          *         *\n           *       *\n            *     *\n             *   *\n              * *\n               *\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    }
]
