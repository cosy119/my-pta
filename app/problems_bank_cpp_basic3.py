# -*- coding: utf-8 -*-
"""C++ 编程题第三册：一维数组 / 二维数组与矩阵（40 题） —— 自动生成，**不要手改本文件**。

生成器：tools/gen_cpp_basic3.py
题数：40 题 / 240 测试点 / 总分 498

重生成：python tools/gen_cpp_basic3.py
"""

CPP_BASIC3_PROBLEMS: list[dict] = [
    {
        "title": "【一维数组】求和与平均值",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "C++基础",
            "数组",
            "累加"
        ],
        "statement_md": "读入 `n` 个整数，输出它们的和与平均值（平均值保留两位小数）。\n\n**关键点**\n\n- 和用 `long long`，100 个 10⁹ 级数会超 `int`\n- 平均值是 `(double)sum / n`，别写成 `sum / n`\n- 两行输出：先和，后平均",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "两行：和、平均值（两位小数）。",
        "constraints_md": "- 1 ≤ n ≤ 100\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 一维数组",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    long long s = 0;\n    for (int i = 0; i < n; i++) { int x; scanf(\"%d\", &x); s += x; }\n    printf(\"%lld\\n\", s);\n    printf(\"%.2f\\n\", (double)s / n);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <vector>\n#include <numeric>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    std::vector<int> a(n);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    long long s = std::accumulate(a.begin(), a.end(), 0LL);   // 初值 0LL\n    printf(\"%lld\\n%.2f\\n\", s, (double)s / n);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n-33 22 47 -42 -18\n",
                "expected_stdout": "-24\n-4.80\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n-43\n",
                "expected_stdout": "-43\n-43.00\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "20\n-20 25 19 -34 -3 27 10 30 24 -42 27 -49 10 -17 20 -21 -26 41 10 19\n",
                "expected_stdout": "50\n2.50\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100\n-517 -379 -789 477 -189 -20 -683 -816 -864 -960 -178 125 879 -408 639 567 -880 -546 65 99 -263 -434 596 -647 693 -783 -464 -561 931 899 -948 697 312 652 -467 639 -444 -604 -663 -366 -407 284 776 498 967 750 737 802 -238 -823 730 240 -309 375 -206 36 -491 -636 -494 -31 -427 -818 934 914 675 772 929 121 721 -386 -986 861 -403 172 443 806 -362 736 567 41 -601 -153 -133 226 -410 -118 -76 -670 -523 -376 -469 664 633 -912 -834 -906 -53 282 -426 62\n",
                "expected_stdout": "-2526\n-25.26\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7\n29 -18 44 -5 38 44 33\n",
                "expected_stdout": "165\n23.57\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "33\n23 -40 12 47 -17 -46 -50 -32 34 25 10 47 44 -3 -10 48 -48 -16 12 -25 43 2 18 19 37 -38 -26 22 20 39 43 -17 34\n",
                "expected_stdout": "211\n6.39\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【一维数组】最大值及其首次下标",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "C++基础",
            "数组",
            "最大值"
        ],
        "statement_md": "读入 `n` 个整数，输出最大值和它**第一次出现**的下标（下标从 0 开始）。\n\n**关键点**\n\n- 初值用 `a[0]`，不要用 0 —— 全负数时 0 会变成答案\n- 比较用严格大于 `>`，这样相等时保留**首次**下标\n- 输出 `最大值 下标`，空格分隔",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行两个整数。",
        "constraints_md": "- 1 ≤ n ≤ 100\n- |x| ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 一维数组",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[105];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int best = 0;                     // 记录下标，靠 a 取值\n    for (int i = 1; i < n; i++)\n        if (a[i] > a[best]) best = i; // 严格大于 → 保留首次\n    printf(\"%d %d\\n\", a[best], best);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[105];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int *p = std::max_element(a, a + n);       // 返回首个最大值的指针\n    printf(\"%d %d\\n\", *p, (int)(p - a));\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n7 21 49 9 7\n",
                "expected_stdout": "49 2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n-2\n",
                "expected_stdout": "-2 0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "10\n-1 -1 5 5 -3 5 -2 5 -3 -2\n",
                "expected_stdout": "5 2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100\n-37 28 39 46 33 17 -19 -16 44 -18 -13 43 -41 34 7 -12 9 37 0 0 49 -35 -17 -22 -10 -5 -17 -4 30 30 16 -31 -30 20 35 34 -15 -29 -49 33 -42 -35 26 -7 -47 -40 -15 -24 -2 1 24 6 27 -38 32 37 -36 24 25 31 31 -4 -27 -38 45 12 15 36 -26 -16 7 29 -23 12 -14 14 -18 -37 -35 -39 -15 -15 -35 -47 -30 44 2 -36 37 17 25 -39 4 11 37 -29 18 -1 8 -11\n",
                "expected_stdout": "49 20\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n1 0 0 1 1 0\n",
                "expected_stdout": "1 0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8\n-4 10 11 -14 3 -21 7 -50\n",
                "expected_stdout": "11 2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【一维数组】最小值及其最后下标",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "数组",
            "最小值",
            "下标"
        ],
        "statement_md": "读入 `n` 个整数，输出最小值和它**最后一次出现**的下标。\n\n**关键点**\n\n- 要「最后」一次，比较必须用 `<=` 而不是 `<`\n- 这题专门和上一题对照：一个用 `>` 取首次，一个用 `<=` 取末次\n- 下标从 0 开始",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行两个整数。",
        "constraints_md": "- 1 ≤ n ≤ 100\n- |x| ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 一维数组",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[105];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int best = 0;\n    for (int i = 1; i < n; i++)\n        if (a[i] <= a[best]) best = i;   // 小于等于 → 保留最后一次\n    printf(\"%d %d\\n\", a[best], best);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[105];\n    int mn = 0;\n    for (int i = 0; i < n; i++) {\n        scanf(\"%d\", &a[i]);\n        if (a[i] <= a[mn]) mn = i;       // 边读边判\n    }\n    printf(\"%d %d\\n\", a[mn], mn);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n-2 0 2 0 2\n",
                "expected_stdout": "-2 0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n-33\n",
                "expected_stdout": "-33 0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "12\n1 0 0 2 1 1 1 2 1 0 2 0\n",
                "expected_stdout": "0 11\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "30\n1 0 1 -1 -1 -1 -1 -1 1 1 -1 1 -1 1 0 1 -1 0 0 1 1 -1 -1 1 -1 0 1 0 1 0\n",
                "expected_stdout": "-1 24\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n5 5 5 5 5 5\n",
                "expected_stdout": "5 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "9\n45 -25 34 -24 5 26 19 -43 -34\n",
                "expected_stdout": "-43 7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【一维数组】逆序输出",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "C++基础",
            "数组",
            "逆序"
        ],
        "statement_md": "读入 `n` 个整数，按**相反顺序**输出，空格分隔。\n\n**关键点**\n\n- 从 `n-1` 倒着遍历到 0\n- 输出之间一个空格，行末不要空格\n- 不需要真的把数组翻转，倒着打印就行",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行 `n` 个整数。",
        "constraints_md": "- 1 ≤ n ≤ 100\n- |x| ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 一维数组",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[105];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    for (int i = n - 1; i >= 0; i--) {\n        if (i != n - 1) printf(\" \");\n        printf(\"%d\", a[i]);\n    }\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[105];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    std::reverse(a, a + n);              // 原地翻转再正着打\n    for (int i = 0; i < n; i++) printf(i ? \" %d\" : \"%d\", a[i]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n-49 10 -36 47 0\n",
                "expected_stdout": "0 47 -36 10 -49\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n-41\n",
                "expected_stdout": "-41\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "10\n23 -29 30 -21 -15 11 33 18 17 -27\n",
                "expected_stdout": "-27 17 18 33 11 -15 -21 30 -29 23\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100\n36 -8 50 -92 -41 -92 0 -6 -83 9 -21 -12 -75 50 31 -60 -75 -29 -11 57 -99 99 -60 93 35 -77 -84 -5 -34 90 42 81 -84 0 -57 51 63 -20 -25 -2 -19 -45 -47 16 38 -54 56 -66 47 84 1 40 9 -39 -36 76 -71 49 72 92 -80 14 -28 7 -70 49 -27 -49 -55 4 99 -12 16 -76 34 90 22 8 19 -7 -66 14 -29 -64 -40 -59 -24 -20 -82 -23 33 -73 50 35 -23 5 -41 5 -20 96\n",
                "expected_stdout": "96 -20 5 -41 5 -23 35 50 -73 33 -23 -82 -20 -24 -59 -40 -64 -29 14 -66 -7 19 8 22 90 34 -76 16 -12 99 4 -55 -49 -27 49 -70 7 -28 14 -80 92 72 49 -71 76 -36 -39 9 40 1 84 47 -66 56 -54 38 16 -47 -45 -19 -2 -25 -20 63 51 -57 0 -84 81 42 90 -34 -5 -84 -77 35 93 -60 99 -99 57 -11 -29 -75 -60 31 50 -75 -12 -21 9 -83 -6 0 -92 -41 -92 50 -8 36\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n20 -8\n",
                "expected_stdout": "-8 20\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "17\n-8 -43 -48 -14 -40 -50 14 30 -28 -19 -16 43 33 5 -4 21 -16\n",
                "expected_stdout": "-16 21 -4 5 33 43 -16 -19 -28 30 14 -50 -40 -14 -48 -43 -8\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【一维数组】大于平均值的个数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "C++基础",
            "数组",
            "平均值"
        ],
        "statement_md": "读入 `n` 个整数，输出**严格大于**平均值（实数平均）的元素个数。\n\n同时输出平均值本身，保留两位小数，先输出平均值再输出个数。\n\n**关键点**\n\n- 平均值用 `double` 算，比较时也用 `double`\n- 严格大于：等于平均值的**不算**\n- 先算完平均值再遍历一遍计数 —— 不能边读边判",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "两行：平均值（两位小数）、个数。",
        "constraints_md": "- 1 ≤ n ≤ 100\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 一维数组",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[105];\n    long long s = 0;\n    for (int i = 0; i < n; i++) { scanf(\"%d\", &a[i]); s += a[i]; }\n    double avg = (double)s / n;\n    int cnt = 0;\n    for (int i = 0; i < n; i++) if (a[i] > avg) cnt++;\n    printf(\"%.2f\\n%d\\n\", avg, cnt);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <vector>\n#include <numeric>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    std::vector<int> a(n);\n    for (int &x : a) scanf(\"%d\", &x);\n    double avg = (double)std::accumulate(a.begin(), a.end(), 0LL) / n;\n    int cnt = 0;\n    for (int x : a) cnt += (x > avg);\n    printf(\"%.2f\\n%d\\n\", avg, cnt);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n7 6 4 3 7\n",
                "expected_stdout": "5.40\n3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n31\n",
                "expected_stdout": "31.00\n0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "10\n-46 -14 39 47 -32 9 -3 35 39 -38\n",
                "expected_stdout": "3.60\n5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "40\n4 33 38 79 -71 -55 -3 -43 -26 -93 -43 -71 45 -98 -75 -60 98 31 76 -23 77 62 -4 51 3 96 76 71 -17 -9 -82 -14 -28 58 -60 -72 30 -83 50 -76\n",
                "expected_stdout": "-3.20\n19\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n4 6 7 4 1 4\n",
                "expected_stdout": "4.33\n2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "33\n-41 1 -45 25 25 -21 31 16 -31 24 18 -46 -47 -42 50 -10 30 -44 -47 -33 20 -13 17 -8 41 47 -39 0 40 11 -4 -31 10\n",
                "expected_stdout": "-2.91\n17\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【一维数组】有序数组去重",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "数组",
            "双指针",
            "去重"
        ],
        "statement_md": "读入一个**已升序**的数组（可能含重复），输出去重后的元素个数与新数组。\n\n**关键点**\n\n- 有序数组的去重是双指针：`i` 扫原数组，`j` 写新数组\n- `a[j] = a[i]` 只在 `a[i] != a[j]` 时发生，`j` 最后就是新长度\n- 先输出个数，再输出数组",
        "input_format": "第一行 `n`，第二行 `n` 个升序整数。",
        "output_format": "两行：个数、去重后的数组（空格分隔）。",
        "constraints_md": "- 1 ≤ n ≤ 100\n- -100 ≤ x ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 一维数组",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[105];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int j = 0;                            // j 是新数组的写指针\n    for (int i = 0; i < n; i++)\n        if (i == 0 || a[i] != a[j - 1]) a[j++] = a[i];\n    printf(\"%d\\n\", j);\n    for (int i = 0; i < j; i++) printf(i ? \" %d\" : \"%d\", a[i]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[105], b[105];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int m = 0;\n    for (int i = 0; i < n; i++)\n        if (m == 0 || b[m - 1] != a[i]) b[m++] = a[i];   // 和上一个写入的比较\n    printf(\"%d\\n\", m);\n    for (int i = 0; i < m; i++) printf(i ? \" %d\" : \"%d\", b[i]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "8\n2 2 2 2 3 5 5 5\n",
                "expected_stdout": "3\n2 3 5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n-16\n",
                "expected_stdout": "1\n-16\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "12\n0 0 0 1 1 1 2 2 2 3 3 3\n",
                "expected_stdout": "4\n0 1 2 3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "20\n-5 -4 -3 -2 -2 -2 -1 0 1 1 2 2 2 2 2 2 3 3 4 4\n",
                "expected_stdout": "10\n-5 -4 -3 -2 -1 0 1 2 3 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n7 7 7 7 7 7\n",
                "expected_stdout": "1\n7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "30\n2 3 7 9 13 18 27 27 30 33 39 44 48 50 54 61 67 70 72 72 74 74 75 80 83 84 88 91 98 99\n",
                "expected_stdout": "27\n2 3 7 9 13 18 27 30 33 39 44 48 50 54 61 67 70 72 74 75 80 83 84 88 91 98 99\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【一维数组】把 0 移到末尾",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "数组",
            "双指针",
            "移动零"
        ],
        "statement_md": "读入 `n` 个整数，把其中所有的 0 移到数组末尾，**非零元素的相对顺序不变**。\n\n输出处理后的数组。\n\n**关键点**\n\n- 双指针：`j` 指向下一个该放非零数的位置，扫一遍先把非零数往前挪\n- 剩下的 `j ~ n-1` 全部填 0\n- 不能排序（排序会打乱非零元素的相对顺序）",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行 `n` 个整数。",
        "constraints_md": "- 1 ≤ n ≤ 100\n- -100 ≤ x ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 一维数组",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[105];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int j = 0;\n    for (int i = 0; i < n; i++)\n        if (a[i] != 0) a[j++] = a[i];     // 非零数依次前移\n    while (j < n) a[j++] = 0;             // 尾部补零\n    for (int i = 0; i < n; i++) printf(i ? \" %d\" : \"%d\", a[i]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[105], b[105];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int m = 0, zeros = 0;\n    for (int i = 0; i < n; i++) {\n        if (a[i] == 0) zeros++;\n        else b[m++] = a[i];               // 先挑非零\n    }\n    for (int i = 0; i < zeros; i++) b[m++] = 0;\n    for (int i = 0; i < n; i++) printf(i ? \" %d\" : \"%d\", b[i]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n0 1 0 3 12\n",
                "expected_stdout": "1 3 12 0 0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "8\n3 1 1 2 2 2 0 3\n",
                "expected_stdout": "3 1 1 2 2 2 3 0\n",
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
                "stdin": "15\n3 3 2 2 3 5 0 3 5 0 0 5 1 2 0\n",
                "expected_stdout": "3 3 2 2 3 5 3 5 5 1 2 0 0 0 0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n0 0 0 0\n",
                "expected_stdout": "0 0 0 0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "20\n0 -3 2 1 0 1 2 -3 -2 -1 2 3 2 3 3 -2 2 3 3 2\n",
                "expected_stdout": "-3 2 1 1 2 -3 -2 -1 2 3 2 3 3 -2 2 3 3 2 0 0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【一维数组】循环右移 k 位",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "数组",
            "循环移位"
        ],
        "statement_md": "读入 `n` 与 `k`，把长度为 `n` 的数组**循环右移** `k` 位后输出。\n\n例如 `1 2 3 4 5` 右移 2 位得到 `4 5 1 2 3`。\n\n**关键点**\n\n- `k` 可能大于 `n`，先 `k %= n`\n- 右移 `k` 位 = 新数组第 `i` 位来自原数组第 `(i - k + n) % n` 位\n- `k = 0` 或 `k` 是 `n` 的倍数时原样输出",
        "input_format": "第一行 `n k`，第二行 `n` 个整数。",
        "output_format": "一行 `n` 个整数。",
        "constraints_md": "- 1 ≤ n ≤ 100\n- 0 ≤ k ≤ 10⁹\n- |x| ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 一维数组",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n, k;\n    if (scanf(\"%d %d\", &n, &k) != 2) return 0;\n    static int a[105], b[105];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    k %= n;                                   // 先取模\n    for (int i = 0; i < n; i++) b[(i + k) % n] = a[i];   // 正着搬到新位置\n    for (int i = 0; i < n; i++) printf(i ? \" %d\" : \"%d\", b[i]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n, k;\n    if (scanf(\"%d %d\", &n, &k) != 2) return 0;\n    static int a[105];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    k %= n;\n    std::rotate(a, a + n - k, a + n);         // 标准库直接旋转\n    for (int i = 0; i < n; i++) printf(i ? \" %d\" : \"%d\", a[i]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 2\n1 2 3 4 5\n",
                "expected_stdout": "4 5 1 2 3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4 0\n1 2 3 4\n",
                "expected_stdout": "1 2 3 4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 3\n7 8 9\n",
                "expected_stdout": "7 8 9\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6 8\n1 2 3 4 5 6\n",
                "expected_stdout": "5 6 1 2 3 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10 3\n-9 15 29 -49 -17 -31 46 -25 -17 -39\n",
                "expected_stdout": "-25 -17 -39 -9 15 29 -49 -17 -31 46\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7 1000000000\n-41 50 26 44 -27 -6 39\n",
                "expected_stdout": "50 26 44 -27 -6 39 -41\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【一维数组】第二大值",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "C++基础",
            "数组",
            "第二大"
        ],
        "statement_md": "读入 `n` 个整数（至少两个**不同**的值），输出**严格第二大**的元素。\n\n**关键点**\n\n- `-1` 或 `0` 当前值初值都是错的，要用最小可能值 `LLONG_MIN`\n- 遇到比最大还大的要先把旧最大降级成第二大；相等则跳过\n- 和最大值相同的元素不算「第二大」",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行一个整数。",
        "constraints_md": "- 2 ≤ n ≤ 100\n- |x| ≤ 10⁹\n- 保证至少有两个不同的值",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 一维数组",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <climits>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    long long m1 = LLONG_MIN, m2 = LLONG_MIN;\n    for (int i = 0; i < n; i++) {\n        long long x;\n        scanf(\"%lld\", &x);\n        if (x > m1)      { m2 = m1; m1 = x; }   // 新最大，旧最大降级\n        else if (x < m1 && x > m2) m2 = x;      // 严格小于最大才可能是第二\n    }\n    printf(\"%lld\\n\", m2);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static long long a[105];\n    for (int i = 0; i < n; i++) scanf(\"%lld\", &a[i]);\n    std::sort(a, a + n);\n    int i = n - 1;\n    while (i > 0 && a[i - 1] == a[i]) i--;      // 跳过与最大相等的\n    printf(\"%lld\\n\", a[i - 1]);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4\n1 2 3 4\n",
                "expected_stdout": "3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n5 5 3\n",
                "expected_stdout": "3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "10\n12 9 1 15 14 4 10 -19 -10 -11\n",
                "expected_stdout": "14\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "30\n-704 575 3 34 -402 984 688 662 -633 618 -659 392 -467 -680 562 870 -932 -113 -35 193 719 -797 -595 -371 147 723 -724 -746 -14 -826\n",
                "expected_stdout": "870\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n-5 -1 -3 -1 -2\n",
                "expected_stdout": "-2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n1 1 0 0 1 0\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【一维数组】查找元素首次位置",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "C++基础",
            "数组",
            "查找"
        ],
        "statement_md": "读入 `n` 个整数和一个目标值 `x`，输出 `x` 第一次出现的下标（从 0 开始）；若不存在输出 `-1`。\n\n**关键点**\n\n- 找到就 `break`，否则会拿到最后一次的位置\n- 用标志变量或直接 `return` 都行\n- 输出单个整数",
        "input_format": "第一行 `n x`，第二行 `n` 个整数。",
        "output_format": "一行一个整数。",
        "constraints_md": "- 1 ≤ n ≤ 100\n- |x| ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 一维数组",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n, x;\n    if (scanf(\"%d %d\", &n, &x) != 2) return 0;\n    static int a[105];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int pos = -1;\n    for (int i = 0; i < n; i++)\n        if (a[i] == x) { pos = i; break; }   // 首次命中就停\n    printf(\"%d\\n\", pos);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n, x;\n    if (scanf(\"%d %d\", &n, &x) != 2) return 0;\n    static int a[105];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int *p = std::find(a, a + n, x);\n    printf(\"%d\\n\", p == a + n ? -1 : (int)(p - a));\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 3\n1 2 3 4 3\n",
                "expected_stdout": "2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5 9\n1 2 3 4 5\n",
                "expected_stdout": "-1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 7\n7\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6 -1\n-1 -1 -1 0 1 2\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "20 5\n-40 25 -28 37 36 -30 1 8 50 45 6 9 8 -18 -19 -26 27 -3 12 -23\n",
                "expected_stdout": "-1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "15 -999\n3 16 22 20 21 25 -16 36 47 -38 22 16 10 -30 -41\n",
                "expected_stdout": "-1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【一维数组】计数排序",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "数组",
            "计数排序"
        ],
        "statement_md": "读入 `n` 个 1~100 之间的整数，用**计数排序**（不比较大小）升序输出。\n\n**关键点**\n\n- 开一个 `cnt[101]` 桶，读一个加一个\n- 再按值从小到大，每个值输出 `cnt[v]` 次\n- 这是 O(n + 值域) 的排序，值域小的时候最快",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行 `n` 个整数，升序。",
        "constraints_md": "- 1 ≤ n ≤ 100\n- 1 ≤ x ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 一维数组",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int cnt[101];\n    for (int i = 0; i < n; i++) { int x; scanf(\"%d\", &x); cnt[x]++; }\n    bool first = true;\n    for (int v = 1; v <= 100; v++)\n        for (int k = 0; k < cnt[v]; k++) {\n            if (!first) printf(\" \");\n            printf(\"%d\", v);\n            first = false;\n        }\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[105];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    std::sort(a, a + n);                  // 直接比较排序\n    for (int i = 0; i < n; i++) printf(i ? \" %d\" : \"%d\", a[i]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "8\n10 4 9 6 8 1 9 4\n",
                "expected_stdout": "1 4 4 6 8 9 9 10\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n19\n",
                "expected_stdout": "19\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "20\n4 2 1 5 1 4 4 3 1 4 1 2 2 5 1 1 2 1 2 5\n",
                "expected_stdout": "1 1 1 1 1 1 1 2 2 2 2 2 3 4 4 4 4 5 5 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "50\n90 93 93 96 95 90 92 90 92 91 92 91 91 100 95 95 100 90 93 99 94 96 95 99 92 100 94 96 90 97 97 98 93 94 92 99 90 91 90 99 91 92 94 98 96 95 91 95 99 98\n",
                "expected_stdout": "90 90 90 90 90 90 90 91 91 91 91 91 91 92 92 92 92 92 92 93 93 93 93 94 94 94 94 95 95 95 95 95 95 96 96 96 96 97 97 98 98 98 99 99 99 99 99 100 100 100\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n50 50 50 50 50 50\n",
                "expected_stdout": "50 50 50 50 50 50\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100\n91 62 3 72 68 61 8 34 9 25 64 47 56 58 95 84 37 89 29 96 60 36 92 62 83 18 24 36 47 63 45 10 37 45 43 23 18 56 11 5 12 95 42 13 93 24 96 48 57 89 71 40 78 33 64 58 55 31 20 19 63 27 20 32 25 42 73 71 28 17 41 35 17 76 99 81 46 71 58 69 50 28 84 54 31 81 68 48 50 97 86 50 85 92 18 21 76 5 94 45\n",
                "expected_stdout": "3 5 5 8 9 10 11 12 13 17 17 18 18 18 19 20 20 21 23 24 24 25 25 27 28 28 29 31 31 32 33 34 35 36 36 37 37 40 41 42 42 43 45 45 45 46 47 47 48 48 50 50 50 54 55 56 56 57 58 58 58 60 61 62 62 63 63 64 64 68 68 69 71 71 71 72 73 76 76 78 81 81 83 84 84 85 86 89 89 91 92 92 93 94 95 95 96 96 97 99\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【一维数组】区间和查询（前缀和）",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "C++基础",
            "数组",
            "前缀和"
        ],
        "statement_md": "读入长度为 `n` 的数组，再读 `q` 个查询 `l r`（下标从 1 开始，闭区间），输出每个区间的元素和。\n\n**关键点**\n\n- `pre[i] = pre[i-1] + a[i]`，查询就是 `pre[r] - pre[l-1]`\n- `pre` 用 `long long`：10⁵ 个 10⁶ 级数累加会超 `int`\n- 别每次查询都循环累加，`q` 大时会超时",
        "input_format": "第一行 `n q`；第二行 `n` 个整数；接下来 `q` 行每行 `l r`。",
        "output_format": "`q` 行，每行一个整数。",
        "constraints_md": "- 1 ≤ n, q ≤ 100\n- 1 ≤ l ≤ r ≤ n\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 一维数组",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n, q;\n    if (scanf(\"%d %d\", &n, &q) != 2) return 0;\n    static long long pre[105];\n    for (int i = 1; i <= n; i++) {\n        long long x;\n        scanf(\"%lld\", &x);\n        pre[i] = pre[i - 1] + x;          // 前缀和\n    }\n    while (q--) {\n        int l, r;\n        scanf(\"%d %d\", &l, &r);\n        printf(\"%lld\\n\", pre[r] - pre[l - 1]);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n, q;\n    if (scanf(\"%d %d\", &n, &q) != 2) return 0;\n    static long long a[105];\n    for (int i = 1; i <= n; i++) scanf(\"%lld\", &a[i]);\n    while (q--) {\n        int l, r;\n        scanf(\"%d %d\", &l, &r);\n        long long s = 0;                  // 老实累加\n        for (int i = l; i <= r; i++) s += a[i];\n        printf(\"%lld\\n\", s);\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 3\n1 2 3 4 5\n1 5\n2 4\n3 3\n",
                "expected_stdout": "15\n9\n3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 1\n7\n1 1\n",
                "expected_stdout": "7\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "6 4\n-1 2 -3 4 -5 6\n1 3\n2 5\n1 6\n4 4\n",
                "expected_stdout": "-2\n-2\n3\n4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "20 10\n-517 -379 -789 477 -189 -20 -683 -816 -864 -960 -178 125 879 -408 639 567 -880 -546 65 99\n12 16\n6 19\n4 12\n7 7\n9 13\n7 9\n10 14\n12 13\n20 20\n13 16\n",
                "expected_stdout": "1802\n-3080\n-3108\n-683\n-998\n-2363\n-542\n1004\n99\n1677\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "50 30\n275 -477 519 -266 628 414 930 723 515 335 888 85 -941 721 -47 589 931 -490 329 -894 845 -679 -769 -239 -40 778 -496 -221 113 -792 175 -490 -974 497 -557 -165 -428 -628 876 776 568 -203 -674 560 632 -853 -716 265 264 -89\n9 17\n1 1\n14 27\n11 21\n19 39\n13 47\n44 49\n14 25\n45 46\n25 34\n2 25\n27 32\n10 26\n5 26\n20 46\n39 48\n1 39\n44 49\n22 24\n20 31\n20 35\n45 47\n12 42\n31 36\n4 20\n2 49\n23 50\n26 26\n36 48\n27 38\n",
                "expected_stdout": "3076\n275\n539\n2016\n-3759\n-2906\n152\n257\n-221\n-1450\n3610\n-1711\n1402\n4612\n-3282\n1231\n1573\n152\n-1687\n-2219\n-3743\n-937\n-1770\n-1514\n4450\n1917\n-2830\n778\n10\n-3966\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100 100\n624 175 683 -835 -7 561 -465 -925 -1000 -702 357 201 -37 977 555 504 -236 -346 577 -956 -442 1 642 -595 494 786 -153 864 102 104 396 -808 -605 153 133 432 648 492 -457 357 645 249 404 -820 729 -131 -313 -810 -259 638 -161 648 -488 -89 432 -808 547 -597 435 300 631 -404 -801 948 -907 205 848 -589 695 342 869 -262 -4 910 705 862 -604 54 179 320 986 429 827 649 31 999 876 -942 297 -260 -499 232 -120 -377 -269 206 -756 -817 24 802\n87 95\n26 40\n78 99\n35 74\n93 96\n49 79\n29 46\n77 83\n90 98\n2 26\n100 100\n3 85\n43 78\n86 95\n80 89\n48 72\n68 92\n38 46\n87 94\n7 30\n55 93\n96 99\n13 69\n32 43\n78 99\n58 86\n49 99\n10 76\n55 85\n39 84\n53 58\n25 59\n58 89\n93 95\n3 5\n69 76\n33 79\n25 57\n65 93\n43 76\n33 85\n54 93\n63 80\n78 93\n85 100\n63 72\n93 99\n64 83\n82 96\n42 65\n85 90\n80 92\n89 98\n35 75\n83 95\n63 73\n38 73\n1 80\n58 61\n24 27\n79 97\n15 62\n47 78\n76 77\n25 44\n35 36\n55 88\n63 67\n61 75\n13 60\n47 56\n88 98\n32 72\n19 23\n81 84\n92 93\n6 88\n62 91\n93 94\n81 81\n90 98\n17 95\n11 31\n80 100\n34 91\n64 65\n82 86\n25 81\n62 90\n58 93\n36 97\n92 93\n38 100\n47 65\n47 49\n11 75\n36 71\n36 96\n56 84\n48 50\n",
                "expected_stdout": "-1062\n2444\n2069\n4637\n-560\n4275\n2023\n2191\n-2660\n-33\n802\n8920\n3155\n-63\n4472\n1363\n7102\n1468\n-793\n307\n7811\n-1343\n4759\n1643\n2069\n8056\n6111\n8037\n7228\n7339\n-1003\n3189\n8287\n-766\n-159\n4117\n5381\n3351\n7128\n3705\n8623\n7722\n3770\n4058\n-573\n1348\n-2109\n6813\n2079\n-627\n1001\n3945\n-2363\n5342\n1444\n1344\n2514\n6797\n769\n532\n2808\n3420\n2973\n258\n3416\n565\n8161\n293\n3186\n4133\n-1210\n-3305\n2471\n-178\n2891\n112\n10012\n6759\n-497\n986\n-2660\n8990\n3795\n2638\n9699\n41\n2935\n8472\n7258\n7640\n8329\n112\n7258\n-1058\n-1382\n7877\n3860\n9085\n6765\n-431\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【一维数组】每个数的出现次数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "数组",
            "计数"
        ],
        "statement_md": "读入 `n` 个整数，按**数值从小到大**输出「值 : 次数」，每个不同的值一行。\n\n**关键点**\n\n- 值域小时用桶 `cnt[值]++` 最省事；值域大就排序后统计连续段\n- 本题值域 -100~100，桶数组开 201 或直接排序\n- 格式是 `值:次数`，冒号两侧没有空格",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "若干行，每行 `值:次数`。",
        "constraints_md": "- 1 ≤ n ≤ 100\n- -100 ≤ x ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 一维数组",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[105];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    std::sort(a, a + n);                       // 排好序，相同的就挨在一起\n    for (int i = 0; i < n; ) {\n        int j = i;\n        while (j < n && a[j] == a[i]) j++;\n        printf(\"%d:%d\\n\", a[i], j - i);\n        i = j;\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int cnt[301];                       // 偏移 150，负值也能当下标\n    for (int i = 0; i < n; i++) { int x; scanf(\"%d\", &x); cnt[x + 150]++; }\n    for (int v = -100; v <= 100; v++)\n        if (cnt[v + 150]) printf(\"%d:%d\\n\", v, cnt[v + 150]);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "8\n-1 0 1 -1 1 1 2 -1\n",
                "expected_stdout": "-1:3\n0:1\n1:3\n2:1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n11\n",
                "expected_stdout": "11:1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "20\n0 2 0 3 2 1 3 0 0 2 1 2 3 2 2 3 2 3 1 3\n",
                "expected_stdout": "0:4\n1:3\n2:7\n3:6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "50\n-2 4 -4 0 5 -2 5 4 -5 -3 3 3 5 3 -1 4 -4 3 0 0 -4 -4 2 1 -4 4 3 -1 0 3 5 1 4 2 -2 2 5 -2 0 4 -1 5 -4 -4 -3 4 5 5 -1 0\n",
                "expected_stdout": "-5:1\n-4:7\n-3:2\n-2:4\n-1:4\n0:6\n1:2\n2:3\n3:6\n4:7\n5:8\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n7 7 7 7 7 7\n",
                "expected_stdout": "7:6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100\n9 7 -1 -10 10 -7 -6 5 5 -3 -2 3 8 3 8 -8 4 -8 0 6 0 5 -9 7 6 -7 2 4 -5 7 1 -6 5 7 -8 6 4 9 -4 8 2 7 -2 1 2 -9 3 10 -10 2 -3 0 8 10 -7 -10 3 0 -1 -3 1 5 3 -5 -1 -9 2 2 -7 -9 -1 -9 -5 0 -2 -9 5 -9 -6 -2 6 4 -10 9 9 -5 5 -3 7 5 3 7 4 2 6 -1 0 2 9 -9\n",
                "expected_stdout": "-10:4\n-9:8\n-8:3\n-7:4\n-6:3\n-5:4\n-4:1\n-3:4\n-2:4\n-1:5\n0:6\n1:3\n2:8\n3:6\n4:5\n5:8\n6:5\n7:7\n8:4\n9:5\n10:3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【一维数组】奇数在前偶数在后",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "数组",
            "稳定划分"
        ],
        "statement_md": "读入 `n` 个整数，重排成「所有奇数在前、所有偶数在后」，**两组内部的相对顺序都要保持**。\n\n输出重排后的数组。\n\n**关键点**\n\n- 这题不能像快排那样两头交换 —— 交换会打乱相对顺序\n- 正确做法是扫两遍：先挑奇数、再挑偶数\n- 0 是偶数",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行 `n` 个整数。",
        "constraints_md": "- 1 ≤ n ≤ 100\n- |x| ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 一维数组",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[105], b[105];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int m = 0;\n    for (int i = 0; i < n; i++) if (a[i] % 2 != 0) b[m++] = a[i];   // 先奇数\n    for (int i = 0; i < n; i++) if (a[i] % 2 == 0) b[m++] = a[i];   // 再偶数\n    for (int i = 0; i < n; i++) printf(i ? \" %d\" : \"%d\", b[i]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <vector>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    std::vector<int> odd, even;\n    for (int i = 0; i < n; i++) {\n        int x; scanf(\"%d\", &x);\n        ((x % 2) ? odd : even).push_back(x);   // 分两堆\n    }\n    odd.insert(odd.end(), even.begin(), even.end());   // 接起来\n    for (int i = 0; i < (int)odd.size(); i++) printf(i ? \" %d\" : \"%d\", odd[i]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n1 2 3 4 5\n",
                "expected_stdout": "1 3 5 2 4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n2 4 6 8\n",
                "expected_stdout": "2 4 6 8\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n1 3 5 7\n",
                "expected_stdout": "1 3 5 7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "20\n-8 -4 8 2 10 -5 9 6 -5 0 -1 -5 10 3 -9 9 3 -6 -10 5\n",
                "expected_stdout": "-5 9 -5 -1 -5 3 -9 9 3 5 -8 -4 8 2 10 6 0 10 -6 -10\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n1 2 0 2 1 3\n",
                "expected_stdout": "1 1 3 2 0 2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "15\n1 5 2 7 5 2 1 7 9 9 6 6 1 3 3\n",
                "expected_stdout": "1 5 7 5 1 7 9 9 1 3 3 2 2 6 6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【一维数组】删除所有指定元素",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "数组",
            "删除元素"
        ],
        "statement_md": "读入 `n` 个整数和目标值 `x`，删除数组中所有等于 `x` 的元素，输出新长度和新数组。\n\n若新数组为空，第二行输出空行（只留换行）。\n\n**关键点**\n\n- 和去重一样用写指针 `j`：`a[i] != x` 才写入\n- 新长度就是 `j`，不要先算「删了几个」再减\n- 全部删光时第二行是空行，不是 `none`",
        "input_format": "第一行 `n x`，第二行 `n` 个整数。",
        "output_format": "两行：新长度、新数组。",
        "constraints_md": "- 1 ≤ n ≤ 100\n- |x|, |aᵢ| ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 一维数组",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n, x;\n    if (scanf(\"%d %d\", &n, &x) != 2) return 0;\n    static int a[105];\n    int j = 0;\n    for (int i = 0; i < n; i++) {\n        int v;\n        scanf(\"%d\", &v);\n        if (v != x) a[j++] = v;          // 不等于目标才留下\n    }\n    printf(\"%d\\n\", j);\n    for (int i = 0; i < j; i++) printf(i ? \" %d\" : \"%d\", a[i]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n, x;\n    if (scanf(\"%d %d\", &n, &x) != 2) return 0;\n    static int a[105], b[105];\n    int m = 0;\n    for (int i = 0; i < n; i++) {\n        scanf(\"%d\", &a[i]);\n        if (a[i] != x) b[m++] = a[i];\n    }\n    printf(\"%d\\n\", m);\n    for (int i = 0; i < m; i++) printf(i ? \" %d\" : \"%d\", b[i]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 3\n1 3 5 3 7\n",
                "expected_stdout": "3\n1 5 7\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4 9\n1 2 3 4\n",
                "expected_stdout": "4\n1 2 3 4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4 1\n1 1 1 1\n",
                "expected_stdout": "0\n\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "20 2\n2 2 4 0 3 2 0 3 0 2 4 4 0 5 1 1 5 5 4 5\n",
                "expected_stdout": "16\n4 0 3 0 3 0 4 4 0 5 1 1 5 5 4 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8 2\n7 3 7 1 3 1 5 2\n",
                "expected_stdout": "7\n7 3 7 1 3 1 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "30 2\n0 -1 0 -1 3 1 3 3 -1 1 2 1 2 2 3 -3 2 -3 3 -1 2 -1 -1 -2 -3 0 1 0 -2 -3\n",
                "expected_stdout": "25\n0 -1 0 -1 3 1 3 3 -1 1 1 3 -3 -3 3 -1 -1 -1 -2 -3 0 1 0 -2 -3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【一维数组】合并两个有序数组",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "C++基础",
            "数组",
            "归并"
        ],
        "statement_md": "读入两个**非降序**数组，合并成一个仍非降序的数组并输出。\n\n**关键点**\n\n- 双指针归并：每次取两边较小的那个，取完就后移\n- 一个数组走完后，把另一个剩下的整体接上\n- 不要用 `sort` 合并后再排 —— 那浪费了「已有序」这个条件",
        "input_format": "第一行 `n m`；第二行 `n` 个整数；第三行 `m` 个整数。",
        "output_format": "一行 `n+m` 个整数。",
        "constraints_md": "- 1 ≤ n, m ≤ 50\n- |x| ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 一维数组",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n, m;\n    if (scanf(\"%d %d\", &n, &m) != 2) return 0;\n    static int a[55], b[55];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    for (int i = 0; i < m; i++) scanf(\"%d\", &b[i]);\n    int i = 0, j = 0;\n    bool first = true;\n    while (i < n || j < m) {\n        int v;\n        if (j >= m || (i < n && a[i] <= b[j])) v = a[i++];   // 取较小者\n        else v = b[j++];\n        printf(first ? \"%d\" : \" %d\", v);\n        first = false;\n    }\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n, m;\n    if (scanf(\"%d %d\", &n, &m) != 2) return 0;\n    static int a[110];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    for (int i = 0; i < m; i++) scanf(\"%d\", &a[n + i]);\n    std::sort(a, a + n + m);                 // 全部丢进去再排\n    for (int i = 0; i < n + m; i++) printf(i ? \" %d\" : \"%d\", a[i]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3 3\n1 3 5\n2 4 6\n",
                "expected_stdout": "1 2 3 4 5 6\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 1\n1\n2\n",
                "expected_stdout": "1 2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2 3\n1 2\n3 4 5\n",
                "expected_stdout": "1 2 3 4 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5 7\n-47 16 24 49 50\n-50 -28 -16 9 10 23 39\n",
                "expected_stdout": "-50 -47 -28 -16 9 10 16 23 24 39 49 50\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10 10\n-29 -14 -6 -5 12 12 24 31 37 38\n-46 -38 -29 -24 -17 -13 18 21 23 27\n",
                "expected_stdout": "-46 -38 -29 -29 -24 -17 -14 -13 -6 -5 12 12 18 21 23 24 27 31 37 38\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1 20\n-27\n-48 -45 -40 -39 -38 -34 -33 -32 -22 -19 -15 -13 2 5 13 23 25 27 43 47\n",
                "expected_stdout": "-48 -45 -40 -39 -38 -34 -33 -32 -27 -22 -19 -15 -13 2 5 13 23 25 27 43 47\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【一维数组】判断严格递增",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "C++基础",
            "数组",
            "递增"
        ],
        "statement_md": "读入 `n` 个整数，判断是否**严格递增**（每个元素都严格大于前一个），是输出 `YES`，否输出 `NO`。\n\n**关键点**\n\n- 从 `i = 1` 开始比 `a[i] <= a[i-1]` 就失败\n- `n = 1` 时算严格递增（没有反例）\n- 相等也不算递增 —— 「严格」二字是关键",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行 `YES` 或 `NO`。",
        "constraints_md": "- 1 ≤ n ≤ 100\n- |x| ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 一维数组",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[105];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    bool ok = true;\n    for (int i = 1; i < n; i++)\n        if (a[i] <= a[i - 1]) { ok = false; break; }\n    printf(\"%s\\n\", ok ? \"YES\" : \"NO\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[105];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    bool ok = std::adjacent_find(a, a + n, [](int x, int y) { return y <= x; }) == a + n;\n    printf(\"%s\\n\", ok ? \"YES\" : \"NO\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n1 2 3 4 5\n",
                "expected_stdout": "YES\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n1 2 2 4 5\n",
                "expected_stdout": "NO\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n7\n",
                "expected_stdout": "YES\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n90 52 91 80 92 26 45 36 47 73\n",
                "expected_stdout": "NO\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n1 1 3 4 4 5 7 13 13 20\n",
                "expected_stdout": "NO\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n4 3 2 1\n",
                "expected_stdout": "NO\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【一维数组】最长连续递增段",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "数组",
            "连续段"
        ],
        "statement_md": "读入 `n` 个整数，输出**最长的严格连续递增子段**的长度。\n\n**关键点**\n\n- 一遍扫描：`a[i] > a[i-1]` 就让当前长度加一，否则重置为 1\n- 每次更新答案，别忘了单独元素长度是 1\n- 注意是「连续」而不是「子序列」",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行一个整数。",
        "constraints_md": "- 1 ≤ n ≤ 100\n- |x| ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 一维数组",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[105];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int best = 1, cur = 1;\n    for (int i = 1; i < n; i++) {\n        if (a[i] > a[i - 1]) cur++;\n        else cur = 1;                     // 断了就从 1 重新数\n        if (cur > best) best = cur;\n    }\n    printf(\"%d\\n\", best);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[105];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int best = 1;\n    for (int i = 0; i < n; i++) {         // 枚举每一段起点\n        int j = i;\n        while (j + 1 < n && a[j + 1] > a[j]) j++;\n        if (j - i + 1 > best) best = j - i + 1;\n        i = j;                            // 跳过这一段\n    }\n    printf(\"%d\\n\", best);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "8\n1 2 3 2 3 4 5 1\n",
                "expected_stdout": "4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n5 4 3 2 1\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n9\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n1 2 2 3 4 5\n",
                "expected_stdout": "4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "20\n8 3 8 2 3 10 9 7 0 7 7 0 7 0 7 9 1 9 7 0\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "15\n-5 5 -2 3 -2 1 2 4 -1 2 2 -5 -3 -4 1\n",
                "expected_stdout": "4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【一维数组】最大子段和",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 16,
        "tags": [
            "C++基础",
            "数组",
            "最大子段和",
            "Kadane"
        ],
        "statement_md": "读入 `n` 个整数（可能全为负），求**非空连续子段**的最大和。\n\n**关键点**\n\n- `Kadane`：`cur = max(a[i], cur + a[i])`，`ans = max(ans, cur)`\n- 初值不能写 0 —— 全负数时答案应该是最大的那个负数\n- O(n²) 暴力也能过本题（n ≤ 100），但要理解 O(n) 的做法",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行一个整数。",
        "constraints_md": "- 1 ≤ n ≤ 100\n- |x| ≤ 1000",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 一维数组",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[105];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    long long cur = a[0], best = a[0];\n    for (int i = 1; i < n; i++) {\n        cur = (cur > 0 ? cur + a[i] : a[i]);   // 前缀为负就丢掉\n        if (cur > best) best = cur;\n    }\n    printf(\"%lld\\n\", best);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[105];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    long long best = a[0];\n    for (int i = 0; i < n; i++) {              // O(n²) 暴力枚举\n        long long s = 0;\n        for (int j = i; j < n; j++) {\n            s += a[j];\n            best = std::max(best, s);\n        }\n    }\n    printf(\"%lld\\n\", best);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "8\n-2 1 -3 4 -1 2 1 -5\n",
                "expected_stdout": "6\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n-5 -2 -9\n",
                "expected_stdout": "-2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n-7\n",
                "expected_stdout": "-7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "20\n7 2 3 -7 8 4 -5 2 -1 0 -5 -5 -5 -6 -3 -6 7 9 -3 -4\n",
                "expected_stdout": "17\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "30\n-10 -51 -46 -24 -10 89 -88 0 18 43 13 -47 46 89 79 -88 12 -24 47 -76 9 -100 35 -66 -43 34 13 -31 -12 -14\n",
                "expected_stdout": "242\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n1 2 3 4 5\n",
                "expected_stdout": "15\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【一维数组】数组升序排序",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "数组",
            "冒泡排序"
        ],
        "statement_md": "读入 `n` 个整数，用**冒泡排序**升序排序后输出。\n\n（要求真的写两层循环交换，不要用 `sort` —— 这道题考的是排序过程本身。）\n\n**关键点**\n\n- 外层跑 `n-1` 轮，内层比较相邻两个、逆序就交换\n- 加一个 `swapped` 标志，某一轮没换过就说明已经有序，可以提前结束\n- 输出一行，空格分隔",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行 `n` 个整数，升序。",
        "constraints_md": "- 1 ≤ n ≤ 100\n- |x| ≤ 1000",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 一维数组",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[105];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    for (int i = 0; i < n - 1; i++) {\n        bool swapped = false;\n        for (int j = 0; j < n - 1 - i; j++)\n            if (a[j] > a[j + 1]) {              // 逆序就换\n                int t = a[j]; a[j] = a[j + 1]; a[j + 1] = t;\n                swapped = true;\n            }\n        if (!swapped) break;                    // 已有序，提前收工\n    }\n    for (int i = 0; i < n; i++) printf(i ? \" %d\" : \"%d\", a[i]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[105];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    for (int i = 0; i < n - 1; i++) {           // 选择排序：每轮找最小放前面\n        int k = i;\n        for (int j = i + 1; j < n; j++) if (a[j] < a[k]) k = j;\n        if (k != i) { int t = a[i]; a[i] = a[k]; a[k] = t; }\n    }\n    for (int i = 0; i < n; i++) printf(i ? \" %d\" : \"%d\", a[i]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "8\n24 39 -37 -43 -8 -7 -26 46\n",
                "expected_stdout": "-43 -37 -26 -8 -7 24 39 46\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n7\n",
                "expected_stdout": "7\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "20\n-37 -39 45 -50 -5 -12 -22 -39 16 -39 -49 32 -46 -41 4 29 25 39 31 -21\n",
                "expected_stdout": "-50 -49 -46 -41 -39 -39 -39 -37 -22 -21 -12 -5 4 16 25 29 31 32 39 45\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n10 9 8 7 6 5 4 3 2 1\n",
                "expected_stdout": "1 2 3 4 5 6 7 8 9 10\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "50\n-30 -99 -39 77 79 -17 -15 -14 85 58 36 -47 15 49 71 -98 -67 30 -29 -15 -56 -9 -41 -83 60 -18 -61 65 100 -74 96 38 -82 28 96 -19 -97 -18 100 7 52 -82 86 -27 37 -93 -8 97 79 -11\n",
                "expected_stdout": "-99 -98 -97 -93 -83 -82 -82 -74 -67 -61 -56 -47 -41 -39 -30 -29 -27 -19 -18 -18 -17 -15 -15 -14 -11 -9 -8 7 15 28 30 36 37 38 49 52 58 60 65 71 77 79 79 85 86 96 96 97 100 100\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n3 3 3 3 3 3\n",
                "expected_stdout": "3 3 3 3 3 3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【一维数组】有序数组插入",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "数组",
            "插入"
        ],
        "statement_md": "读入一个**升序**数组和一个整数 `x`，把 `x` 插入到正确位置后输出新数组。\n\n**关键点**\n\n- 从后往前找位置，一边找一边把元素后移，最后填 `x`\n- `x` 比所有元素都大时插到末尾，比所有都小时插到开头\n- 长度变成 `n + 1`，数组容量要留够",
        "input_format": "第一行 `n x`，第二行 `n` 个升序整数。",
        "output_format": "一行 `n+1` 个整数，升序。",
        "constraints_md": "- 1 ≤ n ≤ 100\n- |x| ≤ 1000",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 一维数组",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n, x;\n    if (scanf(\"%d %d\", &n, &x) != 2) return 0;\n    static int a[110];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int i = n - 1;\n    while (i >= 0 && a[i] > x) { a[i + 1] = a[i]; i--; }  // 比 x 大的后移\n    a[i + 1] = x;                                          // 空位填 x\n    for (int k = 0; k <= n; k++) printf(k ? \" %d\" : \"%d\", a[k]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n, x;\n    if (scanf(\"%d %d\", &n, &x) != 2) return 0;\n    static int a[110], b[110];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int pos = 0;\n    while (pos < n && a[pos] <= x) pos++;      // 找到第一个比 x 大的位置\n    for (int i = 0; i < pos; i++) b[i] = a[i];\n    b[pos] = x;\n    for (int i = pos; i < n; i++) b[i + 1] = a[i];\n    for (int i = 0; i <= n; i++) printf(i ? \" %d\" : \"%d\", b[i]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 3\n1 2 4 5 6\n",
                "expected_stdout": "1 2 3 4 5 6\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 0\n1 2 3\n",
                "expected_stdout": "0 1 2 3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 9\n1 2 3\n",
                "expected_stdout": "1 2 3 9\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1 5\n5\n",
                "expected_stdout": "5 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "20 25\n4 4 8 10 24 26 26 28 31 31 33 33 34 36 40 41 45 49 49 50\n",
                "expected_stdout": "4 4 8 10 24 25 26 26 28 31 31 33 33 34 36 40 41 45 49 49 50\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10 -20\n-8 -3 -2 -1 -1 0 1 3 3 4\n",
                "expected_stdout": "-20 -8 -3 -2 -1 -1 0 1 3 3 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【一维数组】删除首次出现的元素",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "数组",
            "删除"
        ],
        "statement_md": "读入 `n` 个整数和 `x`，删除 `x` **第一次出现**的那个元素（后面的元素前移），输出新长度和新数组。\n\n若 `x` 不存在，输出 `not found`（只一行）。\n\n**关键点**\n\n- 先找位置，找到了再整体前移一位\n- 只删第一个，不要用「删除所有」的写法\n- 找不到时**不要**输出数组，只输出 `not found`",
        "input_format": "第一行 `n x`，第二行 `n` 个整数。",
        "output_format": "找到时两行（新长度、新数组）；否则一行 `not found`。",
        "constraints_md": "- 1 ≤ n ≤ 100\n- |x|, |aᵢ| ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 一维数组",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n, x;\n    if (scanf(\"%d %d\", &n, &x) != 2) return 0;\n    static int a[105];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int pos = -1;\n    for (int i = 0; i < n; i++) if (a[i] == x) { pos = i; break; }\n    if (pos < 0) { printf(\"not found\\n\"); return 0; }\n    for (int i = pos; i < n - 1; i++) a[i] = a[i + 1];   // 后面整体前移\n    printf(\"%d\\n\", n - 1);\n    for (int i = 0; i < n - 1; i++) printf(i ? \" %d\" : \"%d\", a[i]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n, x;\n    if (scanf(\"%d %d\", &n, &x) != 2) return 0;\n    static int a[105], b[105];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int m = 0;\n    bool removed = false;\n    for (int i = 0; i < n; i++) {\n        if (!removed && a[i] == x) { removed = true; continue; }  // 只跳过一个\n        b[m++] = a[i];\n    }\n    if (!removed) { printf(\"not found\\n\"); return 0; }\n    printf(\"%d\\n\", m);\n    for (int i = 0; i < m; i++) printf(i ? \" %d\" : \"%d\", b[i]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 3\n1 3 5 3 7\n",
                "expected_stdout": "4\n1 5 3 7\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4 9\n1 2 3 4\n",
                "expected_stdout": "not found\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 1\n1 1 1\n",
                "expected_stdout": "2\n1 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2 5\n5 6\n",
                "expected_stdout": "1\n6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "20 2\n0 5 2 3 0 2 2 5 5 5 3 4 2 3 3 4 4 3 1 4\n",
                "expected_stdout": "19\n0 5 3 0 2 2 5 5 5 3 4 2 3 3 4 4 3 1 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8 99\n7 8 7 4 4 7 1 7\n",
                "expected_stdout": "not found\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【一维数组】众数（并列取最小值）",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "C++基础",
            "数组",
            "众数"
        ],
        "statement_md": "读入 `n` 个整数，输出出现次数**最多**的数；若并列，输出其中**值最小**的。\n\n**关键点**\n\n- 先排序再扫连续段，或者用桶统计\n- 更新条件写 `cnt > best_cnt`（严格大于），并列时就保留先遇到的（排好序后就是最小的）\n- 并列取最小，用桶从值小到大扫最自然",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行一个整数。",
        "constraints_md": "- 1 ≤ n ≤ 100\n- -100 ≤ x ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 一维数组",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int cnt[301];\n    for (int i = 0; i < n; i++) { int x; scanf(\"%d\", &x); cnt[x + 150]++; }\n    int best = -100, bc = -1;\n    for (int v = -100; v <= 100; v++)        // 从小到大扫\n        if (cnt[v + 150] > bc) { bc = cnt[v + 150]; best = v; }  // 严格大于\n    printf(\"%d\\n\", best);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[105];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    std::sort(a, a + n);\n    int best = a[0], bc = 0;\n    for (int i = 0; i < n; ) {\n        int j = i;\n        while (j < n && a[j] == a[i]) j++;\n        if (j - i > bc) { bc = j - i; best = a[i]; }   // 并列不换 → 保留小值\n        i = j;\n    }\n    printf(\"%d\\n\", best);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "6\n1 2 2 3 3 3\n",
                "expected_stdout": "3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n1 2 2 1 3\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n7\n",
                "expected_stdout": "7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "20\n1 -1 2 -2 -3 -1 2 1 2 3 1 -1 1 3 1 2 2 -2 0 2\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "30\n2 9 -9 8 -9 -1 7 -6 -6 -9 -1 -5 6 0 10 -6 -8 3 -1 2 -8 -1 -9 -5 -9 4 -1 -9 -2 -4\n",
                "expected_stdout": "-9\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n9 9 1 1\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【一维数组】按绝对值排序",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "C++基础",
            "数组",
            "绝对值",
            "比较器"
        ],
        "statement_md": "读入 `n` 个整数，按**绝对值升序**排序；绝对值相同时按**原值升序**。输出排序结果。\n\n**关键点**\n\n- 比较函数写成 `fabs(x) < fabs(y)`，并列时再比 `x < y`\n- `sort` 的比较器必须是**严格弱序**，不能写 `<=`\n- 自己写排序时，比较条件同样要两段",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行 `n` 个整数。",
        "constraints_md": "- 1 ≤ n ≤ 100\n- -1000 ≤ x ≤ 1000",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 一维数组",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <algorithm>\n#include <cstdlib>\nbool cmp(int x, int y) {\n    if (abs(x) != abs(y)) return abs(x) < abs(y);   // 先比绝对值\n    return x < y;                                   // 再比原值\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[105];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    std::sort(a, a + n, cmp);\n    for (int i = 0; i < n; i++) printf(i ? \" %d\" : \"%d\", a[i]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[105];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    for (int i = 0; i < n - 1; i++)             // 手写选择排序\n        for (int j = i + 1; j < n; j++) {\n            int ax = a[i] < 0 ? -a[i] : a[i];\n            int ay = a[j] < 0 ? -a[j] : a[j];\n            if (ay < ax || (ay == ax && a[j] < a[i])) {\n                int t = a[i]; a[i] = a[j]; a[j] = t;\n            }\n        }\n    for (int i = 0; i < n; i++) printf(i ? \" %d\" : \"%d\", a[i]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n-3 1 -2 4 -1\n",
                "expected_stdout": "-1 1 -2 -3 4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n5 -5 3 -3\n",
                "expected_stdout": "-3 3 -5 5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n-7\n",
                "expected_stdout": "-7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "20\n-3 3 -8 5 -2 7 -3 1 7 4 10 9 -8 -9 -2 10 -8 -2 10 -5\n",
                "expected_stdout": "1 -2 -2 -2 -3 -3 3 4 -5 5 7 7 -8 -8 -8 -9 9 10 10 10\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "30\n99 -73 -40 -28 -22 -92 -93 23 -43 13 89 84 12 15 -81 98 -96 -74 7 -82 25 71 31 -48 -7 79 -37 30 -14 12\n",
                "expected_stdout": "-7 7 12 12 13 -14 15 -22 23 25 -28 30 31 -37 -40 -43 -48 71 -73 -74 79 -81 -82 84 89 -92 -93 -96 98 99\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n0 -1 1 -2 2 0\n",
                "expected_stdout": "0 0 -1 1 -2 2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【一维数组】有序数组两数之和",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 16,
        "tags": [
            "C++基础",
            "数组",
            "双指针"
        ],
        "statement_md": "读入一个**升序**数组和目标 `target`，找出两个不同位置的元素使其和等于 `target`，输出它们的下标（**从 1 开始，小的在前**）。\n\n数据保证恰好有一组解。\n\n**关键点**\n\n- 双指针：`l = 0, r = n-1`，和大了 `r--`，和小了 `l++`\n- 不能用两层循环，那样 O(n²) 在 n 大时慢（本题 n ≤ 100 也能过，但要会双指针）\n- 下标是 1-based，输出时记得 +1",
        "input_format": "第一行 `n target`，第二行 `n` 个升序整数。",
        "output_format": "一行两个整数。",
        "constraints_md": "- 2 ≤ n ≤ 100\n- |x|, |target| ≤ 10⁵\n- 保证唯一解",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 一维数组",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n, target;\n    if (scanf(\"%d %d\", &n, &target) != 2) return 0;\n    static int a[105];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int l = 0, r = n - 1;\n    while (l < r) {\n        long long s = (long long)a[l] + a[r];\n        if (s == target) { printf(\"%d %d\\n\", l + 1, r + 1); return 0; }  // 1-based\n        if (s < target) l++;             // 和太小，左指针右移\n        else r--;                        // 和太大，右指针左移\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n, target;\n    if (scanf(\"%d %d\", &n, &target) != 2) return 0;\n    static int a[105];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    for (int i = 0; i < n; i++)                 // 暴力两两枚举\n        for (int j = i + 1; j < n; j++)\n            if ((long long)a[i] + a[j] == target) {\n                printf(\"%d %d\\n\", i + 1, j + 1);\n                return 0;\n            }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4 9\n2 7 11 15\n",
                "expected_stdout": "1 2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 6\n1 2 4\n",
                "expected_stdout": "2 3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2 0\n-1 1\n",
                "expected_stdout": "1 2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5 8\n1 2 3 4 5\n",
                "expected_stdout": "3 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6 13\n1 3 5 7 8 9\n",
                "expected_stdout": "3 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4 -3\n-5 -2 -1 2\n",
                "expected_stdout": "1 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【矩阵】转置",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "C++基础",
            "二维数组",
            "转置"
        ],
        "statement_md": "读入一个 `n×n` 矩阵，输出它的转置（行列互换）。\n\n**关键点**\n\n- 转置就是 `b[j][i] = a[i][j]`\n- 按行输出，每行 `n` 个数，空格分隔\n- 方阵转置可以原地做（交换 `a[i][j]` 与 `a[j][i]`，只遍历上三角）",
        "input_format": "第一行 `n`，接下来 `n` 行每行 `n` 个整数。",
        "output_format": "`n` 行，每行 `n` 个整数。",
        "constraints_md": "- 1 ≤ n ≤ 20\n- |x| ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 二维数组与矩阵",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[25][25];\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) scanf(\"%d\", &a[i][j]);\n    for (int j = 0; j < n; j++) {           // 外层是列\n        for (int i = 0; i < n; i++) printf(i ? \" %d\" : \"%d\", a[i][j]);\n        printf(\"\\n\");\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[25][25];\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) scanf(\"%d\", &a[i][j]);\n    for (int i = 0; i < n; i++)             // 原地交换上三角\n        for (int j = i + 1; j < n; j++) {\n            int t = a[i][j]; a[i][j] = a[j][i]; a[j][i] = t;\n        }\n    for (int i = 0; i < n; i++) {\n        for (int j = 0; j < n; j++) printf(j ? \" %d\" : \"%d\", a[i][j]);\n        printf(\"\\n\");\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n5 20 11\n14 9 -5\n19 -4 -13\n",
                "expected_stdout": "5 14 19\n20 9 -4\n11 -5 -13\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n15\n",
                "expected_stdout": "15\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n-18 -5 -8 -15\n16 19 -4 16\n13 5 -10 6\n10 17 -15 -4\n",
                "expected_stdout": "-18 16 13 10\n-5 19 5 17\n-8 -4 -10 -15\n-15 16 6 -4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n-12 -7 7 12 8\n-17 -6 -1 -5 17\n-6 -17 -17 -2 -4\n-15 -1 4 -12 -9\n4 9 16 3 18\n",
                "expected_stdout": "-12 -17 -6 -15 4\n-7 -6 -17 -1 9\n7 -1 -17 4 16\n12 -5 -2 -12 3\n8 17 -4 -9 18\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n-9 16\n16 5\n",
                "expected_stdout": "-9 16\n16 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n7 13 -8 -3 19 -7\n6 4 15 -18 18 18\n-17 2 -16 16 18 13\n-4 -2 6 -8 6 -17\n14 -4 18 -17 19 15\n-2 1 -3 5 -3 -6\n",
                "expected_stdout": "7 6 -17 -4 14 -2\n13 4 2 -2 -4 1\n-8 15 -16 6 18 -3\n-3 -18 16 -8 -17 5\n19 18 18 6 19 -3\n-7 18 13 -17 15 -6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【矩阵】每行元素之和",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "C++基础",
            "二维数组",
            "行和"
        ],
        "statement_md": "读入 `n×n` 矩阵，输出每一行元素之和，每行一个结果。\n\n**关键点**\n\n- 固定行、遍历列：`for (j) s += a[i][j]`\n- `n` 行，每行一个整数\n- 别把内外层循环写反（那样就是列和）",
        "input_format": "第一行 `n`，接下来 `n` 行。",
        "output_format": "`n` 行，每行一个整数。",
        "constraints_md": "- 1 ≤ n ≤ 20\n- |x| ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 二维数组与矩阵",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[25][25];\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) scanf(\"%d\", &a[i][j]);\n    for (int i = 0; i < n; i++) {\n        long long s = 0;\n        for (int j = 0; j < n; j++) s += a[i][j];\n        printf(\"%lld\\n\", s);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    for (int i = 0; i < n; i++) {           // 不存矩阵，边读边加\n        long long s = 0;\n        for (int j = 0; j < n; j++) { int x; scanf(\"%d\", &x); s += x; }\n        printf(\"%lld\\n\", s);\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n-4 -4 -16\n7 10 -11\n-3 15 -18\n",
                "expected_stdout": "-24\n6\n-6\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n-11\n",
                "expected_stdout": "-11\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n16 -10 7 10\n-19 -8 -12 -17\n2 1 -19 -11\n8 5 10 17\n",
                "expected_stdout": "23\n-56\n-27\n40\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n-8 9 -13 -9 -20\n20 20 -2 -6 5\n-7 5 14 8 -17\n20 20 -9 -12 -14\n-5 -19 -5 16 -4\n",
                "expected_stdout": "-41\n37\n3\n5\n-17\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n6 6\n1 -20\n",
                "expected_stdout": "12\n-19\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n-19 -20 0 -20 -6 -5\n11 -20 9 13 -16 10\n12 20 -6 -6 -18 -11\n0 -8 14 11 12 10\n3 7 -18 -4 -11 16\n4 -20 1 0 13 0\n",
                "expected_stdout": "-70\n7\n-9\n39\n-7\n-2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【矩阵】每列元素之和",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "二维数组",
            "列和"
        ],
        "statement_md": "读入 `n×n` 矩阵，输出每一列元素之和，**一行内**用空格分隔。\n\n**关键点**\n\n- 外层是列、内层是行：`for (j) { s += a[i][j] }`\n- 必须先把矩阵全部读进来，不能边读边算（除非按列重排输入）\n- 输出一行 `n` 个数",
        "input_format": "第一行 `n`，接下来 `n` 行。",
        "output_format": "一行 `n` 个整数。",
        "constraints_md": "- 1 ≤ n ≤ 20\n- |x| ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 二维数组与矩阵",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[25][25];\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) scanf(\"%d\", &a[i][j]);\n    for (int j = 0; j < n; j++) {\n        long long s = 0;\n        for (int i = 0; i < n; i++) s += a[i][j];    // 固定列，累加各行\n        printf(j ? \" %lld\" : \"%lld\", s);\n    }\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static long long col[25] = {0};\n    for (int i = 0; i < n; i++)             // 边读边累加到列上\n        for (int j = 0; j < n; j++) {\n            int x; scanf(\"%d\", &x);\n            col[j] += x;\n        }\n    for (int j = 0; j < n; j++) printf(j ? \" %lld\" : \"%lld\", col[j]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n-3 5 -12\n3 15 8\n1 -5 18\n",
                "expected_stdout": "1 15 14\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n6\n",
                "expected_stdout": "6\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n-13 -12 19 -1\n-17 14 8 0\n0 9 6 2\n-7 11 -18 -4\n",
                "expected_stdout": "-37 22 15 -3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n17 -10 10 -15 14\n7 1 -16 -20 -4\n12 -9 -7 2 2\n-11 20 5 -2 16\n-6 -8 -13 9 -12\n",
                "expected_stdout": "19 -6 -21 -26 16\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n15 -12\n16 -13\n",
                "expected_stdout": "31 -25\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n-14 10 -1 -18 9 5\n-16 -14 -4 0 12 16\n-10 -13 3 -16 2 -13\n-20 -1 -12 -2 15 -18\n10 -17 5 9 8 -19\n4 15 -6 11 -8 15\n",
                "expected_stdout": "-46 -20 -15 -16 38 -14\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【矩阵】主对角线元素之和",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "C++基础",
            "二维数组",
            "对角线"
        ],
        "statement_md": "读入 `n×n` 矩阵，输出**主对角线**（左上到右下）元素之和。\n\n**关键点**\n\n- 主对角线满足 `i == j`\n- `n = 1` 时就是那个唯一元素\n- 只需一次循环 `for (i) s += a[i][i]`",
        "input_format": "第一行 `n`，接下来 `n` 行。",
        "output_format": "一行一个整数。",
        "constraints_md": "- 1 ≤ n ≤ 20\n- |x| ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 二维数组与矩阵",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[25][25];\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) scanf(\"%d\", &a[i][j]);\n    long long s = 0;\n    for (int i = 0; i < n; i++) s += a[i][i];   // i == j\n    printf(\"%lld\\n\", s);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    long long s = 0;\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) {\n            int x; scanf(\"%d\", &x);\n            if (i == j) s += x;                 // 读的时候顺手挑\n        }\n    printf(\"%lld\\n\", s);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n0 -10 -5\n20 -14 10\n9 19 1\n",
                "expected_stdout": "-13\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n-5\n",
                "expected_stdout": "-5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n15 2 2 -7\n5 -15 -2 14\n14 1 6 -4\n-5 1 15 -5\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n-5 15 4 6 -12\n3 2 3 -7 -20\n-4 7 -17 14 -7\n-20 7 -15 -15 -14\n-11 -4 -4 18 17\n",
                "expected_stdout": "-18\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n-11 -20\n8 14\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n-20 14 -8 -11 14 3\n-9 9 -19 11 14 1\n-16 7 -15 11 7 16\n-1 -9 20 2 1 -8\n-3 13 18 20 -16 -5\n-7 5 -17 8 11 11\n",
                "expected_stdout": "-29\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【矩阵】副对角线元素之和",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "二维数组",
            "副对角线"
        ],
        "statement_md": "读入 `n×n` 矩阵，输出**副对角线**（右上到左下）元素之和。\n\n**关键点**\n\n- 副对角线满足 `i + j == n - 1`，即 `j = n-1-i`\n- 别和主对角线搞混 —— 这是最常见的错\n- 奇数阶时中心元素只属于主对角线，副对角线不含它",
        "input_format": "第一行 `n`，接下来 `n` 行。",
        "output_format": "一行一个整数。",
        "constraints_md": "- 1 ≤ n ≤ 20\n- |x| ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 二维数组与矩阵",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[25][25];\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) scanf(\"%d\", &a[i][j]);\n    long long s = 0;\n    for (int i = 0; i < n; i++) s += a[i][n - 1 - i];   // i + j == n-1\n    printf(\"%lld\\n\", s);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[25][25];\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) scanf(\"%d\", &a[i][j]);\n    long long s = 0;\n    for (int i = 0, j = n - 1; i < n; i++, j--) s += a[i][j];   // 双指针式\n    printf(\"%lld\\n\", s);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n17 -1 16\n-11 -17 -18\n15 -4 20\n",
                "expected_stdout": "14\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n-13\n",
                "expected_stdout": "-13\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n-8 11 -10 9\n16 -15 13 0\n6 -19 -4 -1\n-10 -9 -12 -8\n",
                "expected_stdout": "-7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n4 4 -14 -2 13\n18 0 -2 5 7\n20 -4 1 16 7\n6 -6 -10 3 -11\n6 8 -13 -4 -20\n",
                "expected_stdout": "19\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n-2 -20\n-10 6\n",
                "expected_stdout": "-30\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n15 -8 18 13 -13 15\n0 13 14 15 8 10\n-11 16 -14 -15 -11 7\n13 -14 1 -3 -18 -11\n2 5 4 17 12 -3\n8 -1 15 12 -12 9\n",
                "expected_stdout": "22\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【矩阵】最大值及其位置",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "二维数组",
            "最大值"
        ],
        "statement_md": "读入 `n×n` 矩阵，输出最大值以及它第一次出现的行、列号（**从 1 开始**）。\n\n按行优先顺序，取第一个最大值。\n\n**关键点**\n\n- 按行扫描，`>` 严格大于才更新，保证取到第一个\n- 行号列号输出时要 +1（题目要求 1-based）\n- 初值用 `a[0][0]`，不要用 0",
        "input_format": "第一行 `n`，接下来 `n` 行。",
        "output_format": "一行三个整数 `max row col`。",
        "constraints_md": "- 1 ≤ n ≤ 20\n- |x| ≤ 1000",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 二维数组与矩阵",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[25][25];\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) scanf(\"%d\", &a[i][j]);\n    int bi = 0, bj = 0;\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++)\n            if (a[i][j] > a[bi][bj]) { bi = i; bj = j; }   // 严格大于\n    printf(\"%d %d %d\\n\", a[bi][bj], bi + 1, bj + 1);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[25][25];\n    int best = 0, bi = 0, bj = 0, first = 1;\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) {\n            scanf(\"%d\", &a[i][j]);\n            if (first) { best = a[i][j]; first = 0; }\n            else if (a[i][j] > best) { best = a[i][j]; bi = i; bj = j; }\n        }\n    printf(\"%d %d %d\\n\", best, bi + 1, bj + 1);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n19 16 2\n0 -3 0\n-2 19 9\n",
                "expected_stdout": "19 1 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n-2\n",
                "expected_stdout": "-2 1 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n-14 -15 4 -15\n18 11 5 15\n-14 16 10 4\n14 2 17 -7\n",
                "expected_stdout": "18 2 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n-7 -8 -15 -14 20\n-11 -20 -14 -1 -6\n20 18 7 14 -10\n-2 -2 6 10 -10\n-2 17 -6 3 19\n",
                "expected_stdout": "20 1 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n-10 -13\n19 4\n",
                "expected_stdout": "19 2 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n-18 10 -4 6 7 19\n8 13 15 6 -8 15\n1 7 7 20 5 -1\n2 6 5 10 -2 -4\n16 -10 -10 -13 10 -16\n-15 9 -20 1 -10 2\n",
                "expected_stdout": "20 3 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【矩阵】矩阵加法",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "C++基础",
            "二维数组",
            "矩阵加法"
        ],
        "statement_md": "读入两个 `n×n` 矩阵，输出它们的和矩阵（对应位置相加）。\n\n**关键点**\n\n- 先读第一个，再读第二个，边读边加\n- 输出 `n` 行，每行 `n` 个数\n- 输入顺序：`n`、矩阵 A 的 `n` 行、矩阵 B 的 `n` 行",
        "input_format": "第一行 `n`；接下来 `n` 行是 A；再 `n` 行是 B。",
        "output_format": "`n` 行，每行 `n` 个整数。",
        "constraints_md": "- 1 ≤ n ≤ 20\n- |x| ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 二维数组与矩阵",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[25][25], b[25][25];\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) scanf(\"%d\", &a[i][j]);\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) scanf(\"%d\", &b[i][j]);\n    for (int i = 0; i < n; i++) {\n        for (int j = 0; j < n; j++) printf(j ? \" %d\" : \"%d\", a[i][j] + b[i][j]);\n        printf(\"\\n\");\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[25][25];\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) scanf(\"%d\", &a[i][j]);\n    for (int i = 0; i < n; i++)             // 读到 B 就直接加到 A 上\n        for (int j = 0; j < n; j++) {\n            int x; scanf(\"%d\", &x);\n            a[i][j] += x;\n        }\n    for (int i = 0; i < n; i++) {\n        for (int j = 0; j < n; j++) printf(j ? \" %d\" : \"%d\", a[i][j]);\n        printf(\"\\n\");\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n-5 3 3\n5 -9 4\n-5 -4 2\n3 9 0\n4 -9 5\n8 7 -7\n",
                "expected_stdout": "-2 12 3\n9 -18 9\n3 3 -5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n7 7 2 -2\n7 2 7 0\n2 -1 5 2\n9 9 -2 -2\n4 -2 9 -3\n-8 -8 9 9\n-4 8 6 9\n-8 -8 -2 3\n",
                "expected_stdout": "11 5 11 -5\n-1 -6 16 9\n-2 7 11 11\n1 1 -4 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n-4\n-8\n",
                "expected_stdout": "-12\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n-9 -7 6 -9 -9\n-4 1 -2 -5 7\n-3 -4 -8 -1 -5\n-6 -5 -8 -3 3\n5 8 2 5 -4\n-4 -8 0 4 4\n-4 1 -6 -2 7\n4 0 -3 8 -5\n-4 -3 6 -3 -8\n8 -9 0 7 -1\n",
                "expected_stdout": "-13 -15 6 -5 -5\n-8 2 -8 -7 14\n1 -4 -11 7 -10\n-10 -8 -2 -6 -5\n13 -1 2 12 -5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n0 -5\n0 -3\n7 3\n9 3\n",
                "expected_stdout": "7 -2\n9 0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n-7 6 -6 -5 7 3\n3 1 -4 -6 -5 3\n5 -7 -7 -4 -1 -2\n-5 -7 7 -3 -7 -7\n-2 3 6 -9 -2 2\n4 2 2 -6 -7 5\n-9 2 1 9 -3 -6\n-1 -4 8 -2 2 2\n5 8 4 -4 -9 -5\n-7 -7 -5 4 -9 1\n0 4 5 -9 0 9\n7 -6 -2 9 -5 -5\n",
                "expected_stdout": "-16 8 -5 4 4 -3\n2 -3 4 -8 -3 5\n10 1 -3 -8 -10 -7\n-12 -14 2 1 -16 -6\n-2 7 11 -18 -2 11\n11 -4 0 3 -12 0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【矩阵】矩阵乘法",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 16,
        "tags": [
            "C++基础",
            "二维数组",
            "矩阵乘法"
        ],
        "statement_md": "读入两个 `n×n` 矩阵 A、B，输出 `C = A × B`。\n\n`C[i][j] = Σ A[i][k] * B[k][j]`（k 从 0 到 n-1）。\n\n**关键点**\n\n- 三重循环：`i`、`j`、`k`，最内层累加\n- 累加变量用 `long long`：100×100×100 会超 `int`\n- 别把 `B[k][j]` 写成 `B[j][k]` —— 那算的是 `A × Bᵀ`",
        "input_format": "第一行 `n`；接下来 `n` 行是 A；再 `n` 行是 B。",
        "output_format": "`n` 行，每行 `n` 个整数。",
        "constraints_md": "- 1 ≤ n ≤ 20\n- |x| ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 二维数组与矩阵",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[25][25], b[25][25];\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) scanf(\"%d\", &a[i][j]);\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) scanf(\"%d\", &b[i][j]);\n    for (int i = 0; i < n; i++) {\n        for (int j = 0; j < n; j++) {\n            long long s = 0;\n            for (int k = 0; k < n; k++) s += (long long)a[i][k] * b[k][j];\n            printf(j ? \" %lld\" : \"%lld\", s);\n        }\n        printf(\"\\n\");\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[25][25], b[25][25];\n    static long long c[25][25];\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) scanf(\"%d\", &a[i][j]);\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) scanf(\"%d\", &b[i][j]);\n    for (int i = 0; i < n; i++)             // 以 i,k 为外层，写入整行\n        for (int k = 0; k < n; k++) {\n            long long aik = a[i][k];\n            for (int j = 0; j < n; j++) c[i][j] += aik * b[k][j];\n        }\n    for (int i = 0; i < n; i++) {\n        for (int j = 0; j < n; j++) printf(j ? \" %lld\" : \"%lld\", c[i][j]);\n        printf(\"\\n\");\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n0 4 4\n-6 -2 1\n-8 -3 9\n-3 3 9\n-9 -6 -5\n-3 6 -8\n",
                "expected_stdout": "-48 0 -52\n33 0 -52\n24 48 -129\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n-6\n2\n",
                "expected_stdout": "-12\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n-8 -6 -6 -3\n-2 1 3 4\n5 0 5 -7\n2 -9 -1 -6\n-9 -6 -6 -4\n-5 2 2 -7\n2 -2 2 -8\n2 5 5 -1\n",
                "expected_stdout": "84 33 9 125\n27 28 40 -27\n-49 -75 -55 -53\n13 -58 -62 69\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n1 -5 7 -5 -5\n7 8 -2 6 -1\n4 7 2 0 8\n0 6 7 -4 2\n6 3 7 7 -1\n-2 -8 -9 0 9\n-3 -8 -7 -9 -1\n0 -4 2 -4 7\n-7 -2 5 -5 5\n-1 -2 8 -4 7\n",
                "expected_stdout": "53 24 -25 62 3\n-79 -122 -101 -90 64\n-37 -112 -17 -103 99\n8 -72 -32 -70 37\n-69 -112 -34 -86 128\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n-2 2\n-2 4\n-4 -1\n-4 7\n",
                "expected_stdout": "0 16\n-8 30\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n3 6 0 -4 7 -6\n4 3 -4 9 -9 5\n1 -4 0 -8 -2 5\n-7 7 -4 -7 -4 -6\n-9 2 7 5 2 -1\n-4 -3 -8 4 -8 9\n2 7 -7 4 -3 1\n5 0 9 -2 3 -1\n-4 0 4 3 -2 -3\n-9 -9 -1 7 7 5\n-2 0 -6 8 -8 9\n2 -4 2 -7 3 8\n",
                "expected_stdout": "46 81 -17 70 -93 -8\n-14 -73 38 -46 155 17\n68 59 -13 -95 -40 -13\n96 38 115 -93 15 -121\n-87 -104 90 39 35 3\n7 -100 31 -133 138 43\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【矩阵】鞍点查找",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 16,
        "tags": [
            "C++基础",
            "二维数组",
            "鞍点"
        ],
        "statement_md": "读入 `n×n` 矩阵，找一个**鞍点**：它在所在行里最大、同时在所在列里最小。\n\n输出它的行、列（从 1 开始）和值；若有多个取**行优先第一个**；没有则输出 `No`。\n\n**关键点**\n\n- 先扫一行找出最大值所在的列，再验这一列里它是不是最小\n- 一行可能有多个相同的最大值，要逐个当候选验（本题数据保证不重复，简化成取第一个）\n- 判断列最小要用严格小于比较",
        "input_format": "第一行 `n`，接下来 `n` 行。",
        "output_format": "一行 `row col value` 或 `No`。",
        "constraints_md": "- 1 ≤ n ≤ 20\n- |x| ≤ 1000\n- 保证同行最大值不重复",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 二维数组与矩阵",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[25][25];\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) scanf(\"%d\", &a[i][j]);\n    for (int i = 0; i < n; i++) {\n        int bc = 0;\n        for (int j = 1; j < n; j++) if (a[i][j] > a[i][bc]) bc = j;   // 行最大\n        bool ok = true;\n        for (int k = 0; k < n; k++) if (a[k][bc] < a[i][bc]) { ok = false; break; }\n        if (ok) { printf(\"%d %d %d\\n\", i + 1, bc + 1, a[i][bc]); return 0; }\n    }\n    printf(\"No\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[25][25];\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) scanf(\"%d\", &a[i][j]);\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) {\n            bool rowMax = true, colMin = true;\n            for (int k = 0; k < n; k++) {\n                if (a[i][k] > a[i][j]) rowMax = false;\n                if (a[k][j] < a[i][j]) colMin = false;\n            }\n            if (rowMax && colMin) {\n                printf(\"%d %d %d\\n\", i + 1, j + 1, a[i][j]);\n                return 0;\n            }\n        }\n    printf(\"No\\n\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n90 91 92\n1 7 101\n10 7 102\n",
                "expected_stdout": "1 3 92\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n90\n",
                "expected_stdout": "1 1 90\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n9 9 7 3\n4 8 2 6\n5 4 2 4\n5 9 2 1\n",
                "expected_stdout": "No\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n7 1 9 1 6\n4 8 4 2 9\n4 7 5 1 3\n7 8 3 5 7\n7 8 8 7 7\n",
                "expected_stdout": "No\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n90 91\n13 101\n",
                "expected_stdout": "1 2 91\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n5 7 9 8 7 1\n9 1 4 5 5 4\n5 8 6 3 7 3\n9 1 2 3 4 3\n4 8 5 2 8 9\n4 9 2 4 3 7\n",
                "expected_stdout": "No\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【矩阵】上三角判断",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "二维数组",
            "上三角"
        ],
        "statement_md": "读入 `n×n` 矩阵，判断它是否为**上三角矩阵**：主对角线**下方**（`i > j`）的元素全为 0。\n\n是输出 `YES`，否输出 `NO`。\n\n**关键点**\n\n- 只需检查 `i > j` 的位置，对角线和上三角随便是什么\n- 找到第一个非零就可以直接判否\n- `n = 1` 一定是上三角",
        "input_format": "第一行 `n`，接下来 `n` 行。",
        "output_format": "一行 `YES` 或 `NO`。",
        "constraints_md": "- 1 ≤ n ≤ 20\n- |x| ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 二维数组与矩阵",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[25][25];\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) scanf(\"%d\", &a[i][j]);\n    bool ok = true;\n    for (int i = 0; i < n && ok; i++)\n        for (int j = 0; j < i; j++)          // 只看主对角线下方\n            if (a[i][j] != 0) { ok = false; break; }\n    printf(\"%s\\n\", ok ? \"YES\" : \"NO\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    int bad = 0;\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) {\n            int x; scanf(\"%d\", &x);\n            if (i > j && x != 0) bad++;      // 边读边判\n        }\n    printf(\"%s\\n\", bad == 0 ? \"YES\" : \"NO\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n8 3 4\n0 3 3\n0 0 8\n",
                "expected_stdout": "YES\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n8\n",
                "expected_stdout": "YES\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n6 6 3 1\n0 7 8 3\n0 0 1 4\n2 0 0 4\n",
                "expected_stdout": "NO\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n4 4 6 4 8\n0 2 6 6 4\n0 0 3 7 4\n0 0 0 8 7\n0 0 0 0 2\n",
                "expected_stdout": "YES\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n6 6\n3 1\n",
                "expected_stdout": "NO\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n1 5 5 9 3 6\n0 7 2 6 9 5\n0 0 7 2 7 6\n0 0 0 8 3 8\n0 0 0 0 7 6\n0 0 0 0 0 6\n",
                "expected_stdout": "YES\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【矩阵】螺旋矩阵",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 16,
        "tags": [
            "C++基础",
            "二维数组",
            "螺旋矩阵",
            "模拟"
        ],
        "statement_md": "读入 `n`，输出 `n×n` 的螺旋矩阵：从左上角开始填 1，按**顺时针**方向由外向内绕圈。\n\n例如 `n = 3`：\n\n```\n1 2 3\n8 9 4\n7 6 5\n```\n\n**关键点**\n\n- 用四个边界 `top/bottom/left/right`，每走完一条边就收缩\n- 顺序是：上行左→右、右列上→下、下行右→左、左列下→上\n- 收缩后要重新判 `top <= bottom && left <= right`，否则内层会重复填",
        "input_format": "一行一个整数 `n`。",
        "output_format": "`n` 行，每行 `n` 个整数。",
        "constraints_md": "- 1 ≤ n ≤ 20",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 二维数组与矩阵",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[25][25];\n    int v = 1, top = 0, bot = n - 1, left = 0, right = n - 1;\n    while (top <= bot && left <= right) {\n        for (int j = left; j <= right; j++) a[top][j] = v++;      // 上边\n        top++;\n        for (int i = top; i <= bot; i++) a[i][right] = v++;       // 右边\n        right--;\n        if (top <= bot) for (int j = right; j >= left; j--) a[bot][j] = v++;   // 下边\n        bot--;\n        if (left <= right) for (int i = bot; i >= top; i--) a[i][left] = v++;  // 左边\n        left++;\n    }\n    for (int i = 0; i < n; i++) {\n        for (int j = 0; j < n; j++) printf(j ? \" %d\" : \"%d\", a[i][j]);\n        printf(\"\\n\");\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[25][25];\n    int dr[4] = {0, 1, 0, -1}, dc[4] = {1, 0, -1, 0};   // 右下左上\n    int r = 0, c = 0, d = 0;\n    for (int v = 1; v <= n * n; v++) {\n        a[r][c] = v;\n        int nr = r + dr[d], nc = c + dc[d];\n        if (nr < 0 || nr >= n || nc < 0 || nc >= n || a[nr][nc]) {\n            d = (d + 1) % 4;                 // 撞墙就右转\n            nr = r + dr[d]; nc = c + dc[d];\n        }\n        r = nr; c = nc;\n    }\n    for (int i = 0; i < n; i++) {\n        for (int j = 0; j < n; j++) printf(j ? \" %d\" : \"%d\", a[i][j]);\n        printf(\"\\n\");\n    }\n    return 0;\n}\n",
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
                "expected_stdout": "1 2\n4 3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n",
                "expected_stdout": "1 2 3\n8 9 4\n7 6 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n",
                "expected_stdout": "1 2 3 4\n12 13 14 5\n11 16 15 6\n10 9 8 7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n",
                "expected_stdout": "1 2 3 4 5\n16 17 18 19 6\n15 24 25 20 7\n14 23 22 21 8\n13 12 11 10 9\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n",
                "expected_stdout": "1 2 3 4 5 6\n20 21 22 23 24 7\n19 32 33 34 25 8\n18 31 36 35 26 9\n17 30 29 28 27 10\n16 15 14 13 12 11\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【矩阵】边界元素之和",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "二维数组",
            "边界"
        ],
        "statement_md": "读入 `n×n` 矩阵，输出**最外一圈**（四条边）元素之和。\n\n四个角只能算一次。\n\n**关键点**\n\n- 条件：`i == 0 || i == n-1 || j == 0 || j == n-1`\n- `n = 1` 时只有一个元素，算一次\n- `n = 2` 时四个元素都是边界",
        "input_format": "第一行 `n`，接下来 `n` 行。",
        "output_format": "一行一个整数。",
        "constraints_md": "- 1 ≤ n ≤ 20\n- |x| ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 二维数组与矩阵",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[25][25];\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) scanf(\"%d\", &a[i][j]);\n    long long s = 0;\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++)\n            if (i == 0 || i == n - 1 || j == 0 || j == n - 1) s += a[i][j];\n    printf(\"%lld\\n\", s);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[25][25];\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) scanf(\"%d\", &a[i][j]);\n    if (n == 1) { printf(\"%d\\n\", a[0][0]); return 0; }\n    long long s = 0;\n    for (int j = 0; j < n; j++) s += a[0][j] + a[n - 1][j];        // 上下两行\n    for (int i = 1; i < n - 1; i++) s += a[i][0] + a[i][n - 1];    // 左右两列（去角）\n    printf(\"%lld\\n\", s);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n11 -14 7\n-3 16 5\n10 0 -9\n",
                "expected_stdout": "7\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n11\n",
                "expected_stdout": "11\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n-5 19\n1 -18\n",
                "expected_stdout": "-3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n-15 5 -20 13\n-15 18 -14 1\n-12 5 -14 -19\n10 -15 14 -20\n",
                "expected_stdout": "-73\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n-18 -9 9 -14 19\n16 15 -14 5 17\n-1 -6 13 -8 12\n1 -20 5 13 8\n14 2 -2 -2 -10\n",
                "expected_stdout": "42\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n6 6 5 16 -1 20\n-13 -11 -18 -15 -12 -1\n-15 -13 7 -7 19 5\n6 -16 -10 -9 -7 -18\n-15 9 11 12 -2 -5\n-11 -17 10 6 5 9\n",
                "expected_stdout": "-2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【矩阵】每行升序排列",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "C++基础",
            "二维数组",
            "行排序"
        ],
        "statement_md": "读入 `n×n` 矩阵，把**每一行**分别升序排序后输出。\n\n**关键点**\n\n- 外层遍历行，内层对这一行做排序\n- 行与行之间互不影响，不要整体排序\n- 自己写冒泡或直接 `sort(a[i], a[i]+n)`",
        "input_format": "第一行 `n`，接下来 `n` 行。",
        "output_format": "`n` 行，每行 `n` 个整数。",
        "constraints_md": "- 1 ≤ n ≤ 20\n- |x| ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 二维数组与矩阵",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[25][25];\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) scanf(\"%d\", &a[i][j]);\n    for (int i = 0; i < n; i++) {\n        std::sort(a[i], a[i] + n);          // 只排这一行\n        for (int j = 0; j < n; j++) printf(j ? \" %d\" : \"%d\", a[i][j]);\n        printf(\"\\n\");\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[25][25];\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) scanf(\"%d\", &a[i][j]);\n    for (int i = 0; i < n; i++)\n        for (int x = 0; x < n - 1; x++)      // 手写冒泡，只在本行内\n            for (int y = 0; y < n - 1 - x; y++)\n                if (a[i][y] > a[i][y + 1]) {\n                    int t = a[i][y]; a[i][y] = a[i][y + 1]; a[i][y + 1] = t;\n                }\n    for (int i = 0; i < n; i++) {\n        for (int j = 0; j < n; j++) printf(j ? \" %d\" : \"%d\", a[i][j]);\n        printf(\"\\n\");\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n-7 -19 0\n-8 18 -8\n-6 10 5\n",
                "expected_stdout": "-19 -7 0\n-8 -8 18\n-6 5 10\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n-2\n",
                "expected_stdout": "-2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n20 9 -9 -15\n15 -2 -9 15\n-11 -4 8 -3\n-14 14 9 -4\n",
                "expected_stdout": "-15 -9 9 20\n-9 -2 15 15\n-11 -4 -3 8\n-14 -4 9 14\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n7 2 18 -6 19\n-3 -2 -16 -4 14\n-12 2 4 -12 -4\n11 -10 -20 18 -1\n-19 -1 8 -12 20\n",
                "expected_stdout": "-6 2 7 18 19\n-16 -4 -3 -2 14\n-12 -12 -4 2 4\n-20 -10 -1 11 18\n-19 -12 -1 8 20\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n1 -5\n-3 -8\n",
                "expected_stdout": "-5 1\n-8 -3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n-4 -20 12 17 18 17\n-2 12 0 8 19 -18\n15 1 20 -17 -7 11\n12 8 -6 4 18 -20\n-2 11 -16 16 -10 2\n19 -20 0 11 -10 11\n",
                "expected_stdout": "-20 -4 12 17 17 18\n-18 -2 0 8 12 19\n-17 -7 1 11 15 20\n-20 -6 4 8 12 18\n-16 -10 -2 2 11 16\n-20 -10 0 11 11 19\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【矩阵】顺时针旋转 90 度",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 16,
        "tags": [
            "C++基础",
            "二维数组",
            "旋转"
        ],
        "statement_md": "读入 `n×n` 矩阵，输出它**顺时针旋转 90 度**后的结果。\n\n规律：新矩阵第 `i` 行第 `j` 列 = 原矩阵第 `n-1-j` 行第 `i` 列。\n\n**关键点**\n\n- 公式记牢：`b[i][j] = a[n-1-j][i]`\n- 先转置再左右翻转也能得到同样结果，那是另一条思路\n- 不要在原地转置后忘了翻转，那样得到的是逆时针",
        "input_format": "第一行 `n`，接下来 `n` 行。",
        "output_format": "`n` 行，每行 `n` 个整数。",
        "constraints_md": "- 1 ≤ n ≤ 20\n- |x| ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 二维数组与矩阵",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[25][25];\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) scanf(\"%d\", &a[i][j]);\n    for (int i = 0; i < n; i++) {\n        for (int j = 0; j < n; j++) printf(j ? \" %d\" : \"%d\", a[n - 1 - j][i]);\n        printf(\"\\n\");\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[25][25];\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) scanf(\"%d\", &a[i][j]);\n    for (int i = 0; i < n; i++)                  // 先转置\n        for (int j = i + 1; j < n; j++) { int t = a[i][j]; a[i][j] = a[j][i]; a[j][i] = t; }\n    for (int i = 0; i < n; i++) std::reverse(a[i], a[i] + n);   // 再每行翻转\n    for (int i = 0; i < n; i++) {\n        for (int j = 0; j < n; j++) printf(j ? \" %d\" : \"%d\", a[i][j]);\n        printf(\"\\n\");\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n19 19 -4\n11 11 -3\n0 13 8\n",
                "expected_stdout": "0 11 19\n13 11 19\n8 -3 -4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n4\n",
                "expected_stdout": "4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n0 -10\n14 20\n",
                "expected_stdout": "14 0\n20 -10\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n15 9 -12 -17\n6 -16 -6 -10\n-20 -9 4 14\n-8 -7 -8 -14\n",
                "expected_stdout": "-8 -20 6 15\n-7 -9 -16 9\n-8 4 -6 -12\n-14 14 -10 -17\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n6 -15 -10 2 -17\n19 15 15 -6 18\n-6 18 3 6 14\n15 -17 -8 3 13\n10 -14 13 -17 20\n",
                "expected_stdout": "10 15 -6 19 6\n-14 -17 18 15 -15\n13 -8 3 15 -10\n-17 3 6 -6 2\n20 13 14 18 -17\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n-10 1 2 -16 -8 -13\n-1 9 13 15 1 -18\n19 5 -2 -1 1 9\n2 2 -15 -3 -6 -2\n11 2 -19 2 8 -6\n12 13 1 1 -12 0\n",
                "expected_stdout": "12 11 2 19 -1 -10\n13 2 2 5 9 1\n1 -19 -15 -2 13 2\n1 2 -3 -1 15 -16\n-12 8 -6 1 1 -8\n0 -6 -2 9 -18 -13\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【矩阵】矩阵周边元素平均值",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "C++基础",
            "二维数组",
            "边界",
            "平均值"
        ],
        "statement_md": "读入 `n×n` 矩阵，输出**最外一圈**元素的平均值，保留两位小数。\n\n**关键点**\n\n- 和上一册「边界元素之和」同一组位置，只是最后除以元素个数\n- `n = 1` 时个数是 1；`n ≥ 2` 时个数是 `4n - 4`\n- 别把 `4n - 4` 写成 `4n` —— 四个角重复算了",
        "input_format": "第一行 `n`，接下来 `n` 行。",
        "output_format": "一行，保留两位小数。",
        "constraints_md": "- 1 ≤ n ≤ 20\n- |x| ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 二维数组与矩阵",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[25][25];\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) scanf(\"%d\", &a[i][j]);\n    long long s = 0;\n    int cnt = 0;\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++)\n            if (i == 0 || i == n - 1 || j == 0 || j == n - 1) { s += a[i][j]; cnt++; }\n    printf(\"%.2f\\n\", (double)s / cnt);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[25][25];\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) scanf(\"%d\", &a[i][j]);\n    long long s = 0;\n    int cnt = (n == 1) ? 1 : 4 * n - 4;      // 周长元素个数\n    if (n == 1) s = a[0][0];\n    else {\n        for (int j = 0; j < n; j++) s += a[0][j] + a[n - 1][j];\n        for (int i = 1; i < n - 1; i++) s += a[i][0] + a[i][n - 1];\n    }\n    printf(\"%.2f\\n\", (double)s / cnt);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n-2 -19 -18\n-20 7 20\n-10 -7 13\n",
                "expected_stdout": "-5.38\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n17\n",
                "expected_stdout": "17.00\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n-8 11\n-16 -18\n",
                "expected_stdout": "-7.75\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n3 -16 13 -8\n4 12 -2 -19\n-10 9 7 1\n-11 3 15 -18\n",
                "expected_stdout": "-3.58\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n-8 13 11 -1 -17\n16 19 10 0 14\n14 -12 -15 15 -1\n-6 -16 9 -14 5\n-5 14 14 20 4\n",
                "expected_stdout": "5.44\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n4 10 5 -6 -9 3\n-5 15 -14 2 16 -14\n-17 20 8 18 -18 -17\n13 -20 12 8 10 4\n12 17 -8 -2 7 10\n18 3 4 -15 -9 -3\n",
                "expected_stdout": "-0.45\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    }
]
