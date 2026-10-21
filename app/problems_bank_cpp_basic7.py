# -*- coding: utf-8 -*-
"""第 7 册：排序与查找 / 贪心 —— 自动生成，**不要手改本文件**。

生成器：tools/gen_cpp_basic7.py
题数：40 题 / 240 测试点 / 总分 546

重生成：python tools/gen_cpp_basic7.py
"""

CPP_BASIC7_PROBLEMS: list[dict] = [
    {
        "title": "【排序】冒泡排序统计交换次数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "排序",
            "冒泡",
            "逆序对"
        ],
        "statement_md": "用冒泡排序把数组排成升序，输出**发生交换的次数**（不输出数组）。\n\n**关键点**\n\n- 只有 `a[j] > a[j+1]` 时才交换，相等不交换 —— 这决定了交换次数\n- 交换次数正好等于逆序对个数，可以拿来对数\n- 输出一个整数",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：交换次数。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 排序与查找",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    long long sw = 0;\n    for (int i = 0; i < n - 1; i++)\n        for (int j = 0; j < n - 1 - i; j++)\n            if (a[j] > a[j + 1]) {                 // 严格大于才换\n                int t = a[j]; a[j] = a[j + 1]; a[j + 1] = t;\n                sw++;\n            }\n    printf(\"%lld\\n\", sw);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    long long sw = 0;                              // 直接数逆序对，结果一样\n    for (int i = 0; i < n; i++)\n        for (int j = i + 1; j < n; j++)\n            if (a[i] > a[j]) sw++;\n    printf(\"%lld\\n\", sw);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n-33 22 47 -42 -18\n",
                "expected_stdout": "5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n1 2 3 4 5\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n5 4 3 2 1\n",
                "expected_stdout": "10\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n3 3 3 3\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "20\n-43 -39 -40 -4 -29 44 35 -11 -18 27 -23 27 -46 24 37 -30 5 31 0 42\n",
                "expected_stdout": "66\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "50\n-3 8 7 -6 1 9 5 10 8 -8 9 -10 5 -2 7 -3 -4 5 7 7 5 2 10 -6 -3 10 -6 6 2 -10 -8 -5 8 -9 -1 -10 -2 5 9 2 3 2 8 4 -6 1 -7 -9 -6 5\n",
                "expected_stdout": "685\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【排序】选择排序每轮最小值位置",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "排序",
            "选择排序"
        ],
        "statement_md": "用选择排序把数组排成升序，输出**每一轮选出的最小值所在位置**（从 1 开始）。共 `n-1` 轮，输出 `n-1` 个数，一行。\n\n**关键点**\n\n- 第 i 轮是在 `[i, n-1]` 范围内找最小值，位置按原数组下标记\n- 并列最小值取**最先出现**的那个（比较用严格小于）\n- 共 `n-1` 个数（最后剩一个不用选）",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：`n-1` 个位置下标（1 起）。",
        "constraints_md": "- 2 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 排序与查找",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n < 2) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    for (int i = 0; i < n - 1; i++) {\n        int k = i;\n        for (int j = i + 1; j < n; j++) if (a[j] < a[k]) k = j;   // 严格小于\n        printf(\"%d%c\", k + 1, i == n - 2 ? '\\n' : ' ');\n        int t = a[i]; a[i] = a[k]; a[k] = t;\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n < 2) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    for (int i = 0; i < n - 1; i++) {\n        int *p = std::min_element(a + i, a + n);     // 指针版最小元\n        printf(\"%d%c\", (int)(p - a) + 1, i == n - 2 ? '\\n' : ' ');\n        int t = a[i]; a[i] = *p; *p = t;\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n5 4 3 2 1\n",
                "expected_stdout": "5 4 3 4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n1 2 3 4 5\n",
                "expected_stdout": "1 2 3 4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n2 1 4 3\n",
                "expected_stdout": "2 2 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n2 1\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8\n-20 -12 -37 42 0 11 -31 -39\n",
                "expected_stdout": "8 3 7 8 7 7 7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n9 -2 1 10 6 -10 4 -3 10 -9\n",
                "expected_stdout": "6 10 8 10 8 7 8 8 9\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【排序】插入排序统计移动次数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "排序",
            "插入排序"
        ],
        "statement_md": "用插入排序把数组排成升序，统计**元素后移的总次数**（每次 `a[j+1] = a[j]` 记 1 次），输出这个次数。\n\n**关键点**\n\n- 插入时比 `key` 大的元素都要往后挪一格，挪一次记一次\n- 已经有序的数组移动次数是 0；完全逆序是 `n(n-1)/2`\n- 输出一个整数",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：后移次数。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 排序与查找",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    long long moves = 0;\n    for (int i = 1; i < n; i++) {\n        int key = a[i], j = i - 1;\n        while (j >= 0 && a[j] > key) {   // 严格大于才后移\n            a[j + 1] = a[j];\n            j--;\n            moves++;\n        }\n        a[j + 1] = key;\n    }\n    printf(\"%lld\\n\", moves);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    long long moves = 0;                 // 等价于数逆序对\n    for (int i = 1; i < n; i++)\n        for (int j = 0; j < i; j++)\n            if (a[j] > a[i]) moves++;\n    printf(\"%lld\\n\", moves);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n5 4 3 2 1\n",
                "expected_stdout": "10\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n1 2 3 4 5\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n2 1 4 3\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n7\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n23 -40 12 47 -17 -46 -50 -32 34 25\n",
                "expected_stdout": "23\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "30\n0 -6 2 10 -9 -8 7 -7 1 8 -9 6 -4 -9 -8 3 3 -8 -3 -8 7 3 -9 8 -7 -3 10 10 8 -9\n",
                "expected_stdout": "183\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【排序】计数排序输出频次表",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "排序",
            "计数排序",
            "频次"
        ],
        "statement_md": "数组元素都在 `0`~`100` 之间。用计数排序统计每个值出现的次数，按值升序输出`值:次数`，用空格分隔（只输出出现过的值）。\n\n**关键点**\n\n- 计数排序的核心是「值 → 下标」直接映射，不做比较\n- 输出格式是 `值:次数`，注意冒号两边没有空格\n- 输出一行",
        "input_format": "第一行 `n`，第二行 `n` 个整数（0 ≤ x ≤ 100）。",
        "output_format": "一行：`值:次数` 序列。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 0 ≤ x ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 排序与查找",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    int cnt[101] = {0};\n    for (int i = 0; i < n; i++) { int x; scanf(\"%d\", &x); cnt[x]++; }\n    bool first = true;\n    for (int v = 0; v <= 100; v++) {\n        if (!cnt[v]) continue;\n        printf(\"%s%d:%d\", first ? \"\" : \" \", v, cnt[v]);\n        first = false;\n    }\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <map>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    std::map<int, int> cnt;              // map 天然按 key 升序\n    for (int i = 0; i < n; i++) { int x; scanf(\"%d\", &x); cnt[x]++; }\n    bool first = true;\n    for (auto &kv : cnt) {\n        printf(\"%s%d:%d\", first ? \"\" : \" \", kv.first, kv.second);\n        first = false;\n    }\n    printf(\"\\n\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n3 1 3 2 3\n",
                "expected_stdout": "1:1 2:1 3:3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n0\n",
                "expected_stdout": "0:1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n100 100 1\n",
                "expected_stdout": "1:1 100:2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n1 2 3 1 1 5 0 0 1 1\n",
                "expected_stdout": "0:2 1:5 2:1 3:1 5:1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "20\n97 99 95 94 92 92 100 90 95 98 97 99 91 95 98 99 90 96 92 97\n",
                "expected_stdout": "90:2 91:1 92:3 94:1 95:3 96:1 97:3 98:2 99:3 100:1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "15\n0 3 3 0 1 3 3 2 1 0 3 2 0 1 2\n",
                "expected_stdout": "0:4 1:3 2:3 3:5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【排序】归并排序求逆序对",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 16,
        "tags": [
            "排序",
            "归并",
            "逆序对"
        ],
        "statement_md": "用归并排序统计数组的逆序对个数（`i < j` 且 `a[i] > a[j]` 的数对数量）。\n\n**关键点**\n\n- 归并时，右半段某个元素被取走时，左半段剩下的元素都比它大，一次就能贡献一批逆序对\n- n 到 2×10⁵ 时逆序对最多约 2×10¹⁰，答案用 `long long`\n- 输出一个整数",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：逆序对个数。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 排序与查找",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint a[1005], tmp[1005];\nlong long cnt = 0;\nvoid msort(int l, int r) {\n    if (l >= r) return;\n    int m = (l + r) / 2;\n    msort(l, m);\n    msort(m + 1, r);\n    int i = l, j = m + 1, k = l;\n    while (i <= m && j <= r) {\n        if (a[i] <= a[j]) tmp[k++] = a[i++];\n        else { cnt += m - i + 1; tmp[k++] = a[j++]; }   // 左半段剩下的都比它大\n    }\n    while (i <= m) tmp[k++] = a[i++];\n    while (j <= r) tmp[k++] = a[j++];\n    for (int t = l; t <= r; t++) a[t] = tmp[t];\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    msort(0, n - 1);\n    printf(\"%lld\\n\", cnt);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    long long c = 0;                      // 暴力 O(n²)，对拍用\n    for (int i = 0; i < n; i++)\n        for (int j = i + 1; j < n; j++)\n            if (a[i] > a[j]) c++;\n    printf(\"%lld\\n\", c);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n5 4 3 2 1\n",
                "expected_stdout": "10\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n1 2 3 4 5\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n2 1 4 3\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n7\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n7 21 49 9 7 15 25 -26 -27 15\n",
                "expected_stdout": "26\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "15\n2 -1 5 3 5 0 -3 1 -5 0 2 -1 5 2 4\n",
                "expected_stdout": "47\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【查找】二分查找并统计比较次数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "查找",
            "二分",
            "比较次数"
        ],
        "statement_md": "数组升序。读入 `n x` 和 `n` 个整数，用二分查找找 `x`，输出「位置（1 起，找不到 -1）」与「比较次数」，一行，空格分隔。\n\n**关键点**\n\n- 每比较一次 `mid` 记 1 次，不管是否命中\n- `mid = (lo + hi) / 2`，循环条件是 `lo <= hi`\n- 输出一行两个整数",
        "input_format": "第一行 `n x`；第二行 `n` 个升序整数。",
        "output_format": "一行：`位置 比较次数`。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x|, |a[i]| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 排序与查找",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n, x;\n    if (scanf(\"%d %d\", &n, &x) != 2) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int lo = 0, hi = n - 1, cnt = 0;\n    while (lo <= hi) {\n        int mid = (lo + hi) / 2;\n        cnt++;                            // 每次比较都计数\n        if (a[mid] == x) { printf(\"%d %d\\n\", mid + 1, cnt); return 0; }\n        if (a[mid] < x) lo = mid + 1;\n        else hi = mid - 1;\n    }\n    printf(\"-1 %d\\n\", cnt);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint bs(const int a[], int lo, int hi, int x, int &cnt) {   // 递归版\n    if (lo > hi) return -1;\n    int mid = (lo + hi) / 2;\n    cnt++;\n    if (a[mid] == x) return mid + 1;\n    if (a[mid] < x) return bs(a, mid + 1, hi, x, cnt);\n    return bs(a, lo, mid - 1, x, cnt);\n}\nint main() {\n    int n, x;\n    if (scanf(\"%d %d\", &n, &x) != 2) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int cnt = 0;\n    int p = bs(a, 0, n - 1, x, cnt);\n    printf(\"%d %d\\n\", p, cnt);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 3\n1 3 5 7 9\n",
                "expected_stdout": "2 3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5 4\n1 3 5 7 9\n",
                "expected_stdout": "-1 3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 1\n1\n",
                "expected_stdout": "1 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1 2\n1\n",
                "expected_stdout": "-1 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7 9\n1 3 5 7 9 11 13\n",
                "expected_stdout": "5 3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4 1\n1 2 3 4\n",
                "expected_stdout": "1 2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【查找】二分答案求最小最大段和",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 16,
        "tags": [
            "查找",
            "二分答案",
            "单调性"
        ],
        "statement_md": "把长度为 `n` 的正整数数组切成 `m` 段**连续**子数组，让「各段和的最大值」尽量小，输出这个最小值。\n\n**关键点**\n\n- 答案有单调性：给定上限 `L`，段数不超过 `m` 是否可行，随 `L` 增大而变容易 —— 这就是二分答案的前提\n- 判定函数：从左往右贪心累加，超了就切一刀，统计需要几段\n- 下界是 `max(a[i])`，上界是 `sum(a)`",
        "input_format": "第一行 `n m`；第二行 `n` 个正整数。",
        "output_format": "一行：最小的「最大段和」。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 1 ≤ m ≤ n\n- 1 ≤ a[i] ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 排序与查找",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint n, m;\nint a[1005];\nbool ok(long long lim) {                 // 上限 lim 时能否切成不超过 m 段\n    long long cur = 0;\n    int seg = 1;\n    for (int i = 0; i < n; i++) {\n        if (cur + a[i] <= lim) cur += a[i];\n        else { seg++; cur = a[i]; }\n    }\n    return seg <= m;\n}\nint main() {\n    if (scanf(\"%d %d\", &n, &m) != 2) return 0;\n    long long lo = 0, hi = 0;\n    for (int i = 0; i < n; i++) {\n        scanf(\"%d\", &a[i]);\n        if (a[i] > lo) lo = a[i];        // 下界：单个最大值\n        hi += a[i];                      // 上界：总和\n    }\n    while (lo < hi) {\n        long long mid = lo + (hi - lo) / 2;\n        if (ok(mid)) hi = mid; else lo = mid + 1;\n    }\n    printf(\"%lld\\n\", lo);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint n, m, a[1005];\nbool ok(long long lim) {\n    int seg = 1; long long cur = 0;\n    for (int i = 0; i < n; i++) {\n        if (cur + a[i] <= lim) cur += a[i];\n        else { seg++; cur = a[i]; }\n    }\n    return seg <= m;\n}\nint main() {\n    if (scanf(\"%d %d\", &n, &m) != 2) return 0;\n    long long sum = 0, mx = 0;\n    for (int i = 0; i < n; i++) { scanf(\"%d\", &a[i]); sum += a[i]; mx = std::max(mx, (long long)a[i]); }\n    long long lo = mx - 1, hi = sum;     // 开区间写法：lo 恒不可行\n    while (hi - lo > 1) {\n        long long mid = (lo + hi) / 2;\n        if (ok(mid)) hi = mid; else lo = mid;\n    }\n    printf(\"%lld\\n\", hi);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 2\n7 2 5 10 8\n",
                "expected_stdout": "18\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 1\n5\n",
                "expected_stdout": "5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 3\n1 2 3\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4 2\n1 1 1 1\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8 2\n9 10 6 8 5 8 6 5\n",
                "expected_stdout": "32\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10 3\n4 20 23 25 21 17 8 9 24 9\n",
                "expected_stdout": "63\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【排序】求第 k 小的数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "排序",
            "第k小",
            "nth_element"
        ],
        "statement_md": "读入 `n k` 和 `n` 个整数，输出第 `k` 小的数（`k` 从 1 开始，重复值分别计数）。\n\n**关键点**\n\n- 排序后取 `a[k-1]` 最直观，O(n log n)\n- 只要第 k 小的话，`nth_element` 平均 O(n)\n- 输出一个整数",
        "input_format": "第一行 `n k`；第二行 `n` 个整数。",
        "output_format": "一行：第 `k` 小的数。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 1 ≤ k ≤ n\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 排序与查找",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n, k;\n    if (scanf(\"%d %d\", &n, &k) != 2 || k < 1 || k > n) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    std::nth_element(a, a + k - 1, a + n);   // 平均 O(n)\n    printf(\"%d\\n\", a[k - 1]);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n, k;\n    if (scanf(\"%d %d\", &n, &k) != 2 || k < 1 || k > n) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    std::sort(a, a + n);                     // 全排一遍也对\n    printf(\"%d\\n\", a[k - 1]);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 1\n5 3 1 4 2\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5 5\n5 3 1 4 2\n",
                "expected_stdout": "5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5 3\n5 3 1 4 2\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1 1\n7\n",
                "expected_stdout": "7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6 4\n2 2 3 3 1 1\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8 3\n-24 -49 16 44 -46 -30 -20 -48\n",
                "expected_stdout": "-46\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【排序】排序后去重输出",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "排序",
            "去重",
            "unique"
        ],
        "statement_md": "读入 `n` 个整数，升序输出去重后的结果（每个值只出现一次）。\n\n**关键点**\n\n- 先排序，相邻相等就跳过 —— 这样去重是 O(n) 的\n- 也可以用 `unique` 配 `erase`（数组用「逻辑长度」模拟）\n- 输出一行",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：升序去重结果。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 排序与查找",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    std::sort(a, a + n);\n    int k = 0;\n    for (int i = 0; i < n; i++)\n        if (i == 0 || a[i] != a[i - 1]) a[k++] = a[i];   // 相邻相等就跳过\n    for (int i = 0; i < k; i++) printf(\"%d%c\", a[i], i + 1 == k ? '\\n' : ' ');\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    std::sort(a, a + n);\n    int k = (int)(std::unique(a, a + n) - a);   // unique 返回新末尾\n    for (int i = 0; i < k; i++) printf(\"%d%c\", a[i], i + 1 == k ? '\\n' : ' ');\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n3 1 3 2 3\n",
                "expected_stdout": "1 2 3\n",
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
                "stdin": "4\n1 1 1 1\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n5 4 3 2 1\n",
                "expected_stdout": "1 2 3 4 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "12\n3 4 4 3 4 2 4 1 4 3 2 2\n",
                "expected_stdout": "1 2 3 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n1 0 3 -1 -1 -1 -2 3 2 2\n",
                "expected_stdout": "-2 -1 0 1 2 3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【排序】稳定排序保原顺序",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "排序",
            "稳定排序"
        ],
        "statement_md": "读入 `n` 个人（姓名、分数），按分数**降序**输出姓名，**分数相同的保持输入顺序**。\n\n**关键点**\n\n- `std::sort` 不保证稳定，同分时顺序可能被打乱 —— 这题就是要你意识到这点\n- `std::stable_sort` 或「比较函数里加原始下标」都能解决\n- 每行一个姓名",
        "input_format": "第一行 `n`；之后 `n` 行，每行 `姓名 分数`。",
        "output_format": "`n` 行：按分数降序的姓名。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 0 ≤ 分数 ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 排序与查找",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <algorithm>\nstruct Person {\n    char name[32];\n    int score;\n};\nbool cmp(const Person &a, const Person &b) { return a.score > b.score; }\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static Person v[1005];\n    for (int i = 0; i < n; i++) scanf(\"%31s %d\", v[i].name, &v[i].score);\n    std::stable_sort(v, v + n, cmp);       // 稳定排序\n    for (int i = 0; i < n; i++) printf(\"%s\\n\", v[i].name);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nstruct Person { char name[32]; int score, idx; };\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static Person v[1005];\n    for (int i = 0; i < n; i++) { scanf(\"%31s %d\", v[i].name, &v[i].score); v[i].idx = i; }\n    std::sort(v, v + n, [](const Person &a, const Person &b) {\n        if (a.score != b.score) return a.score > b.score;\n        return a.idx < b.idx;              // 用原始下标把稳定性补回来\n    });\n    for (int i = 0; i < n; i++) printf(\"%s\\n\", v[i].name);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\na 90\nb 90\nc 80\n",
                "expected_stdout": "a\nb\nc\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\na 80\nb 90\nc 80\n",
                "expected_stdout": "b\na\nc\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\nsolo 100\n",
                "expected_stdout": "solo\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\nw 70\nx 70\ny 70\nz 70\n",
                "expected_stdout": "w\nx\ny\nz\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\na 60\nb 70\nc 60\nd 80\ne 60\n",
                "expected_stdout": "d\nb\na\nc\ne\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\np 100\nq 100\nr 90\ns 100\n",
                "expected_stdout": "p\nq\ns\nr\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【排序】成绩排名（同分同名次）",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "排序",
            "排名",
            "并列"
        ],
        "statement_md": "读入 `n` 个分数，按**从高到低**输出每个分数对应的名次（同分同名次，名次按「比我高的人数 + 1」计算），保持输入顺序输出。\n\n**关键点**\n\n- 名次 = 严格大于它的元素个数 + 1，所以同分必然同名次\n- 不要用「排序后下标 +1」，那样同分会拿到不同名次\n- 输出一行 `n` 个整数",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：`n` 个名次。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 0 ≤ 分数 ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 排序与查找",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    for (int i = 0; i < n; i++) {\n        int r = 1;\n        for (int j = 0; j < n; j++) if (a[j] > a[i]) r++;   // 比我高的 +1\n        printf(\"%d%c\", r, i + 1 == n ? '\\n' : ' ');\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005], t[1005];\n    for (int i = 0; i < n; i++) { scanf(\"%d\", &a[i]); t[i] = a[i]; }\n    std::sort(t, t + n);                                       // 升序\n    for (int i = 0; i < n; i++) {\n        int le = (int)(std::upper_bound(t, t + n, a[i]) - t);   // <= a[i] 的个数\n        printf(\"%d%c\", n - le + 1, i + 1 == n ? '\\n' : ' ');    // 比我高的 +1\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n90 80 90 70 100\n",
                "expected_stdout": "2 4 2 5 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n50 50 50 50 50\n",
                "expected_stdout": "1 1 1 1 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n60\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n100 90 80\n",
                "expected_stdout": "1 2 3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8\n71 67 88 81 75 72 91 100\n",
                "expected_stdout": "7 8 3 4 5 6 2 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n0 0 1 3 2 2 1 2 0 2\n",
                "expected_stdout": "8 8 6 1 2 2 6 2 8 2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【排序】区间合并计数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "排序",
            "区间合并",
            "扫描线"
        ],
        "statement_md": "读入 `n` 个闭区间 `[l, r]`，把有重叠（含端点相接）的区间合并，输出合并后的区间个数。\n\n**关键点**\n\n- 先按左端点排序，再线性扫描：能接上就扩右端点，接不上就新开一段\n- 「端点相接」算重叠：`l <= cur_r` 就合并\n- 输出一个整数",
        "input_format": "第一行 `n`；之后 `n` 行，每行 `l r`。",
        "output_format": "一行：合并后的区间数。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 0 ≤ l ≤ r ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 排序与查找",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <algorithm>\nstruct Seg { int l, r; };\nbool cmp(const Seg &a, const Seg &b) { return a.l < b.l; }\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static Seg v[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d %d\", &v[i].l, &v[i].r);\n    std::sort(v, v + n, cmp);              // 按左端点排序\n    int cnt = 1, cr = v[0].r;\n    for (int i = 1; i < n; i++) {\n        if (v[i].l <= cr) { if (v[i].r > cr) cr = v[i].r; }   // 能接上\n        else { cnt++; cr = v[i].r; }\n    }\n    printf(\"%d\\n\", cnt);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int L[1005], R[1005];\n    for (int i = 0; i < n; i++) { scanf(\"%d %d\", &L[i], &R[i]); }\n    static int idx[1005];\n    for (int i = 0; i < n; i++) idx[i] = i;\n    std::sort(idx, idx + n, [&](int x, int y) { return L[x] < L[y]; });\n    int cnt = 1, cr = R[idx[0]];\n    for (int k = 1; k < n; k++) {\n        int i = idx[k];\n        if (L[i] <= cr) { if (R[i] > cr) cr = R[i]; }\n        else { cnt++; cr = R[i]; }\n    }\n    printf(\"%d\\n\", cnt);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 3\n2 4\n5 6\n",
                "expected_stdout": "2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n0 0\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n1 2\n3 4\n5 6\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n1 10\n2 3\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n5 6\n1 3\n2 2\n8 9\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n1 1\n1 1\n2 2\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【排序】求中位数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "排序",
            "中位数"
        ],
        "statement_md": "读入 `n` 个整数，输出中位数。`n` 为奇数时就是中间那个；为偶数时是中间两个的平均值，保留 1 位小数。\n\n**关键点**\n\n- 奇数个直接取 `a[n/2]`；偶数个取 `(a[n/2-1] + a[n/2]) / 2.0`\n- 偶数时除以 2.0，写 `/ 2` 会截断\n- 输出一行",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：中位数（偶数个时保留 1 位小数）。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 排序与查找",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    std::sort(a, a + n);\n    if (n % 2) printf(\"%d\\n\", a[n / 2]);\n    else printf(\"%.1f\\n\", (a[n / 2 - 1] + a[n / 2]) / 2.0);   // 除以 2.0\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    std::nth_element(a, a + n / 2, a + n);        // 只保证中间位置对\n    if (n % 2) { printf(\"%d\\n\", a[n / 2]); return 0; }\n    int hi = a[n / 2];\n    std::nth_element(a, a + n / 2 - 1, a + n);    // 再找低一位\n    printf(\"%.1f\\n\", (a[n / 2 - 1] + hi) / 2.0);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n3 1 4 1 5\n",
                "expected_stdout": "3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n1 2 3 4\n",
                "expected_stdout": "2.5\n",
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
                "stdin": "2\n4 4\n",
                "expected_stdout": "4.0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8\n42 37 50 48 -31 -17 36 31\n",
                "expected_stdout": "36.5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "9\n-5 3 3 10 -1 5 -4 5 6\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【排序】两数组共同元素个数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "排序",
            "双指针",
            "交集"
        ],
        "statement_md": "读入两个数组，输出它们的**不同**共同元素个数（同一个值在两数组都出现就算 1 个，不重复计数）。\n\n**关键点**\n\n- 排序 + 双指针：相等就计数并同时前移，谁小谁前移\n- 也可以直接 `set` 求交集\n- 格式：第一行 `n`，第二行 `n` 个数；第三行 `m`，第四行 `m` 个数",
        "input_format": "第一行 `n`；第二行 `n` 个整数；第三行 `m`；第四行 `m` 个整数。",
        "output_format": "一行：共同元素个数。",
        "constraints_md": "- 1 ≤ n, m ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 排序与查找",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n, m;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int a[1005], b[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    if (scanf(\"%d\", &m) != 1) return 0;\n    for (int i = 0; i < m; i++) scanf(\"%d\", &b[i]);\n    std::sort(a, a + n);\n    std::sort(b, b + m);\n    int i = 0, j = 0, c = 0;\n    while (i < n && j < m) {\n        if (a[i] == b[j]) { c++; i++; j++; }\n        else if (a[i] < b[j]) i++;\n        else j++;\n    }\n    printf(\"%d\\n\", c);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <set>\nint main() {\n    int n, m;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    std::set<int> s;\n    for (int i = 0; i < n; i++) { int x; scanf(\"%d\", &x); s.insert(x); }\n    if (scanf(\"%d\", &m) != 1) return 0;\n    std::set<int> t;\n    for (int i = 0; i < m; i++) { int x; scanf(\"%d\", &x); if (s.count(x)) t.insert(x); }\n    printf(\"%d\\n\", (int)t.size());\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 2 3\n3\n2 3 4\n",
                "expected_stdout": "2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n5\n1\n5\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n1 2\n2\n3 4\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n1 1 2 2\n3\n2 3 3\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n9 8 7\n2\n7 6\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n0\n1\n1\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【排序】排序后相邻最大差值",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "排序",
            "相邻差"
        ],
        "statement_md": "读入 `n` 个整数，排序后求**相邻两个不同值**之间的最大差值；只有一个不同值时输出 0。\n\n**关键点**\n\n- 先去重再算相邻差，否则重复值会让差值恒为 0\n- 排序后一趟扫描就够\n- 输出一个整数",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：最大相邻差。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 排序与查找",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    std::sort(a, a + n);\n    int best = 0;\n    for (int i = 1; i < n; i++) {\n        int d = a[i] - a[i - 1];\n        if (d > best) best = d;          // 重复值差为 0，不影响\n    }\n    printf(\"%d\\n\", best);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    std::sort(a, a + n);\n    int k = (int)(std::unique(a, a + n) - a);    // 先去重\n    int best = 0;\n    for (int i = 1; i < k; i++) best = std::max(best, a[i] - a[i - 1]);\n    printf(\"%d\\n\", best);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n1 5 3 9 7\n",
                "expected_stdout": "2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n5 5 5\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n7\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n1 100\n",
                "expected_stdout": "99\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n-33 -19 -47 28 7 -27 39 -35 44 33\n",
                "expected_stdout": "26\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "12\n9 2 0 18 9 13 12 16 11 4 6 8\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【排序】按绝对值排序",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "排序",
            "绝对值",
            "比较器"
        ],
        "statement_md": "读入 `n` 个整数，按**绝对值升序**输出；绝对值相同时负数排前面。\n\n**关键点**\n\n- 比较器写 `abs(x) < abs(y)`，相等时再比大小\n- 绝对值相等时若要求「负数在前」，就是 `x < y`\n- 输出一行",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：按绝对值升序的结果。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 排序与查找",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <cstdlib>\n#include <algorithm>\nbool cmp(int x, int y) {\n    int ax = abs(x), ay = abs(y);\n    if (ax != ay) return ax < ay;     // 绝对值升序\n    return x < y;                     // 绝对值相同负数在前\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    std::sort(a, a + n, cmp);\n    for (int i = 0; i < n; i++) printf(\"%d%c\", a[i], i + 1 == n ? '\\n' : ' ');\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cstdlib>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    std::sort(a, a + n, [](int x, int y) {\n        return std::make_pair(abs(x), x) < std::make_pair(abs(y), y);   // pair 字典序\n    });\n    for (int i = 0; i < n; i++) printf(\"%d%c\", a[i], i + 1 == n ? '\\n' : ' ');\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4\n-3 1 2 -1\n",
                "expected_stdout": "-1 1 2 -3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n5 -5 0\n",
                "expected_stdout": "0 -5 5\n",
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
                "stdin": "4\n4 -4 2 -2\n",
                "expected_stdout": "-2 2 -4 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n4 17 -9 -7 -10 -8 -10 -15 -11 -2\n",
                "expected_stdout": "-2 4 -7 -8 -9 -10 -10 -11 -15 17\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8\n1 -5 -2 -1 5 2 -5 -1\n",
                "expected_stdout": "-1 -1 1 -2 2 -5 -5 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【排序】按个位数字排序",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "排序",
            "个位",
            "比较器"
        ],
        "statement_md": "读入 `n` 个整数，按**个位数字升序**输出；个位相同的按数值升序。负数的个位取其绝对值的最低位。\n\n**关键点**\n\n- `abs(x) % 10` 才是「个位数字」，`x % 10` 对负数会得到负数\n- 比较器里第二个关键字用 `x < y`\n- 输出一行",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：按个位数字升序的结果。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 排序与查找",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <cstdlib>\n#include <algorithm>\nbool cmp(int x, int y) {\n    int dx = abs(x) % 10, dy = abs(y) % 10;   // 负数取绝对值再取个位\n    if (dx != dy) return dx < dy;\n    return x < y;\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    std::sort(a, a + n, cmp);\n    for (int i = 0; i < n; i++) printf(\"%d%c\", a[i], i + 1 == n ? '\\n' : ' ');\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cstdlib>\n#include <vector>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    std::vector<int> bucket[10];            // 桶排序：按个位分 10 个桶\n    for (int i = 0; i < n; i++) {\n        int x; scanf(\"%d\", &x);\n        bucket[abs(x) % 10].push_back(x);\n    }\n    bool first = true;\n    for (int d = 0; d < 10; d++) {\n        std::sort(bucket[d].begin(), bucket[d].end());   // 桶内按数值升序\n        for (int x : bucket[d]) {\n            printf(\"%s%d\", first ? \"\" : \" \", x);\n            first = false;\n        }\n    }\n    printf(\"\\n\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4\n23 11 45 12\n",
                "expected_stdout": "11 12 23 45\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n-23 23 0\n",
                "expected_stdout": "0 -23 23\n",
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
                "stdin": "4\n9 19 29 39\n",
                "expected_stdout": "9 19 29 39\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n17 28 -18 12 -17 -3 8 4 -27 -22\n",
                "expected_stdout": "-22 12 -3 4 -27 -17 17 -18 8 28\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "9\n41 30 44 17 18 12 4 4 16\n",
                "expected_stdout": "30 41 12 4 4 44 16 17 18\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【排序】快速排序递归实现",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "排序",
            "快排",
            "划分"
        ],
        "statement_md": "用快速排序（以第一个元素为基准）把数组排成升序并输出。\n\n**关键点**\n\n- 划分：把小于基准的放左边、大于等于的放右边\n- 边界取 `(l, p-1)` 和 `(p+1, r)`，别写成 `(l, p)` 否则死循环\n- 输出一行",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：升序结果。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 排序与查找",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nvoid qsort2(int a[], int l, int r) {\n    if (l >= r) return;\n    int p = a[l], i = l, j = r;\n    while (i < j) {\n        while (i < j && a[j] >= p) j--;\n        a[i] = a[j];\n        while (i < j && a[i] <= p) i++;\n        a[j] = a[i];\n    }\n    a[i] = p;                              // 基准归位\n    qsort2(a, l, i - 1);\n    qsort2(a, i + 1, r);\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    qsort2(a, 0, n - 1);\n    for (int i = 0; i < n; i++) printf(\"%d%c\", a[i], i + 1 == n ? '\\n' : ' ');\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    std::sort(a, a + n);                   // 库里的 introsort\n    for (int i = 0; i < n; i++) printf(\"%d%c\", a[i], i + 1 == n ? '\\n' : ' ');\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n5 3 1 4 2\n",
                "expected_stdout": "1 2 3 4 5\n",
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
                "stdin": "4\n1 1 1 1\n",
                "expected_stdout": "1 1 1 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n5 4 3 2 1\n",
                "expected_stdout": "1 2 3 4 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n-36 45 -34 19 26 41 -28 -22 -34 31\n",
                "expected_stdout": "-36 -34 -34 -28 -22 19 26 31 41 45\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "12\n7 -8 1 9 9 -1 -8 6 1 2 3 -10\n",
                "expected_stdout": "-10 -8 -8 -1 1 1 2 3 6 7 9 9\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【查找】线性查找与二分查找的比较次数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "查找",
            "线性",
            "二分"
        ],
        "statement_md": "数组升序。读入 `n x` 和 `n` 个整数，分别用线性查找和二分查找找 `x`，输出两种方法各自的比较次数（线性查找找不到时比较了 `n` 次）。\n\n**关键点**\n\n- 线性查找从头比到尾，找到 `x` 时比较次数就是它的位置\n- 二分查找每轮比较一次 `mid`\n- 输出一行两个整数",
        "input_format": "第一行 `n x`；第二行 `n` 个升序整数。",
        "output_format": "一行：`线性比较次数 二分比较次数`。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x|, |a[i]| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 排序与查找",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n, x;\n    if (scanf(\"%d %d\", &n, &x) != 2) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int lin = n, bc = 0;                    // 找不到时线性比较 n 次\n    for (int i = 0; i < n; i++) if (a[i] == x) { lin = i + 1; break; }\n    int lo = 0, hi = n - 1;\n    while (lo <= hi) {\n        int mid = (lo + hi) / 2;\n        bc++;\n        if (a[mid] == x) break;\n        if (a[mid] < x) lo = mid + 1; else hi = mid - 1;\n    }\n    printf(\"%d %d\\n\", lin, bc);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n, x;\n    if (scanf(\"%d %d\", &n, &x) != 2) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int *p = std::lower_bound(a, a + n, x);\n    int lin = (p != a + n && *p == x) ? (int)(p - a) + 1 : n;\n    int bc = 0, lo = 0, hi = n - 1;\n    while (lo <= hi) {\n        int mid = (lo + hi) / 2;\n        bc++;\n        if (a[mid] == x) break;\n        if (a[mid] < x) lo = mid + 1; else hi = mid - 1;\n    }\n    printf(\"%d %d\\n\", lin, bc);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 3\n1 3 5 7 9\n",
                "expected_stdout": "2 3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5 9\n1 3 5 7 9\n",
                "expected_stdout": "5 3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5 100\n1 3 5 7 9\n",
                "expected_stdout": "5 3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1 1\n1\n",
                "expected_stdout": "1 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7 1\n1 3 5 7 9 11 13\n",
                "expected_stdout": "1 3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4 2\n1 2 3 4\n",
                "expected_stdout": "2 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【排序】排序后求众数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "排序",
            "众数",
            "频次"
        ],
        "statement_md": "读入 `n` 个整数，输出出现次数最多的值；并列时输出**最小**的那个。\n\n**关键点**\n\n- 先排序，相同的值会连成一段，扫一遍数每段长度\n- 也可以直接统计频次再取最大（并列取最小）\n- 输出一个整数",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：众数。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 排序与查找",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    std::sort(a, a + n);\n    int bestV = a[0], bestC = 0;\n    for (int i = 0; i < n;) {\n        int j = i;\n        while (j < n && a[j] == a[i]) j++;\n        if (j - i > bestC) { bestC = j - i; bestV = a[i]; }   // 严格大于才换，并列留最小\n        i = j;\n    }\n    printf(\"%d\\n\", bestV);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <map>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    std::map<int, int> cnt;\n    for (int i = 0; i < n; i++) { int x; scanf(\"%d\", &x); cnt[x]++; }\n    int bv = 0, bc = -1;\n    for (auto &kv : cnt)                  // map 按 key 升序，先遇到的就是小的\n        if (kv.second > bc) { bc = kv.second; bv = kv.first; }\n    printf(\"%d\\n\", bv);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n1 2 2 3 3\n",
                "expected_stdout": "2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n5 5 5\n",
                "expected_stdout": "5\n",
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
                "stdin": "6\n4 4 2 2 3 3\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n3 2 3 1 3 3 1 2 1 2\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "12\n-2 1 -2 1 -1 -2 -1 -2 2 -1 -1 -1\n",
                "expected_stdout": "-1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【贪心】活动选择（最多不重叠区间）",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "贪心",
            "活动选择",
            "区间"
        ],
        "statement_md": "读入 `n` 个时间段 `[l, r]`，一个人最多能参加多少个**互不重叠**的活动？（一个活动结束的时刻等于下一个开始的时刻，算不重叠）\n\n**关键点**\n\n- 按**结束时间**升序排，能接上就选 —— 按开始时间排是错的\n- 贪心的正确性靠「交换论证」：任何最优解都能换成以最早结束者打头\n- 输出一个整数",
        "input_format": "第一行 `n`；之后 `n` 行，每行 `l r`。",
        "output_format": "一行：最多能参加的活动数。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 0 ≤ l < r ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 贪心",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <algorithm>\nstruct Seg { int l, r; };\nbool cmp(const Seg &a, const Seg &b) { return a.r < b.r; }   // 按结束时间排\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static Seg v[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d %d\", &v[i].l, &v[i].r);\n    std::sort(v, v + n, cmp);\n    int cnt = 0, last = -1;\n    for (int i = 0; i < n; i++)\n        if (v[i].l >= last) { cnt++; last = v[i].r; }   // 能接上就选\n    printf(\"%d\\n\", cnt);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint n, L[1005], R[1005];\nint dp[1005];\nint main() {\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    for (int i = 0; i < n; i++) scanf(\"%d %d\", &L[i], &R[i]);\n    static int idx[1005];\n    for (int i = 0; i < n; i++) idx[i] = i;\n    std::sort(idx, idx + n, [&](int x, int y) { return R[x] < R[y]; });\n    int best = 1;\n    for (int k = 0; k < n; k++) {\n        int i = idx[k];\n        dp[k] = 1;\n        for (int p = 0; p < k; p++) {\n            int j = idx[p];\n            if (R[j] <= L[i] && dp[p] + 1 > dp[k]) dp[k] = dp[p] + 1;\n        }\n        if (dp[k] > best) best = dp[k];\n    }\n    printf(\"%d\\n\", best);       // DP 版：不依赖贪心假设\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 3\n2 4\n3 5\n",
                "expected_stdout": "2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n1 2\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n1 2\n2 3\n3 4\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n1 10\n2 3\n4 5\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n0 1\n1 2\n2 3\n3 4\n",
                "expected_stdout": "4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n5 9\n1 2\n3 4\n6 7\n8 10\n",
                "expected_stdout": "4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【贪心】区间选点（最少点数覆盖所有区间）",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "贪心",
            "区间选点"
        ],
        "statement_md": "读入 `n` 个闭区间，在数轴上选尽量少的点，使每个区间里**至少有一个**被选中的点。输出最少的点数。\n\n**关键点**\n\n- 按右端点升序排；当前区间还没被覆盖时，就把点放在它的**右端点**\n- 点放在右端点最「贪」—— 能同时盖住后面尽可能多的区间\n- 输出一个整数",
        "input_format": "第一行 `n`；之后 `n` 行，每行 `l r`。",
        "output_format": "一行：最少点数。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 0 ≤ l ≤ r ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 贪心",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <algorithm>\nstruct Seg { int l, r; };\nbool cmp(const Seg &a, const Seg &b) { return a.r < b.r; }\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static Seg v[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d %d\", &v[i].l, &v[i].r);\n    std::sort(v, v + n, cmp);\n    int cnt = 0, last = -1;\n    for (int i = 0; i < n; i++) {\n        if (last >= v[i].l && last <= v[i].r) continue;   // 已被盖住\n        cnt++;\n        last = v[i].r;                                    // 点放右端点\n    }\n    printf(\"%d\\n\", cnt);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nstruct Seg { int l, r; };\nbool cmpL(const Seg &a, const Seg &b) { return a.l > b.l; }   // 按左端点降序\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static Seg v[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d %d\", &v[i].l, &v[i].r);\n    std::sort(v, v + n, cmpL);\n    int cnt = 0, last = -1;      // 从右往左，点放左端点\n    for (int i = 0; i < n; i++) {\n        if (last <= v[i].r && last >= v[i].l) continue;\n        cnt++;\n        last = v[i].l;\n    }\n    printf(\"%d\\n\", cnt);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 3\n2 4\n5 6\n",
                "expected_stdout": "2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n0 0\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n1 1\n1 1\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n1 2\n3 4\n5 6\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n1 10\n2 3\n4 5\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n1 5\n5 9\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【贪心】找零钱最少张数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "贪心",
            "找零",
            "DP"
        ],
        "statement_md": "纸币面值为 100、25、10、5、1，读入金额 `x`，输出凑出 `x` 需要的最少张数。\n\n**关键点**\n\n- 这套面值满足「每个面值都是前一个的约数或更大」，贪心（先用大面值）恰好最优\n- 如果面值是 1、3、4 这类，贪心就**不**最优了 —— 那时必须 DP\n- 输出一个整数",
        "input_format": "一行一个整数 `x`。",
        "output_format": "一行：最少张数。",
        "constraints_md": "- 0 ≤ x ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 贪心",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int x;\n    if (scanf(\"%d\", &x) != 1) return 0;\n    int coin[5] = {100, 25, 10, 5, 1}, cnt = 0;\n    for (int i = 0; i < 5; i++) { cnt += x / coin[i]; x %= coin[i]; }   // 先用大的\n    printf(\"%d\\n\", cnt);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint dp[1000005];\nint main() {\n    int x;\n    if (scanf(\"%d\", &x) != 1) return 0;\n    int coin[5] = {100, 25, 10, 5, 1};\n    dp[0] = 0;\n    for (int a = 1; a <= x; a++) {\n        dp[a] = 1 << 30;\n        for (int k = 0; k < 5; k++)\n            if (coin[k] <= a) dp[a] = std::min(dp[a], dp[a - coin[k]] + 1);\n    }\n    printf(\"%d\\n\", dp[x]);      // DP 版：换面值也不会错\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "0\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "30\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "99\n",
                "expected_stdout": "9\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "12345\n",
                "expected_stdout": "126\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【贪心】分数背包",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 16,
        "tags": [
            "贪心",
            "分数背包",
            "性价比"
        ],
        "statement_md": "有 `n` 件物品，每件有重量和价值，背包容量为 `w`。物品**可以切开**拿走一部分，价值按比例计算。求能装下的最大总价值，保留 2 位小数。\n\n**关键点**\n\n- 按「单位重量价值」降序取，直到装满 —— 分数背包是贪心能保证最优的少数情况之一\n- 比较 `v1/w1` 与 `v2/w2` 时用交叉相乘 `v1*w2 > v2*w1`，避免浮点误差\n- 输出一行，两位小数",
        "input_format": "第一行 `n w`；之后 `n` 行，每行 `重量 价值`。",
        "output_format": "一行：最大总价值（2 位小数）。",
        "constraints_md": "- 1 ≤ n ≤ 5\n- 1 ≤ w ≤ 1000\n- 1 ≤ 重量 ≤ 100\n- 1 ≤ 价值 ≤ 1000",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 贪心",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <algorithm>\nstruct Item { int w, v; };\nbool cmp(const Item &a, const Item &b) {\n    return (long long)a.v * b.w > (long long)b.v * a.w;   // 交叉相乘比性价比\n}\nint main() {\n    int n, cap;\n    if (scanf(\"%d %d\", &n, &cap) != 2) return 0;\n    static Item it[10];\n    for (int i = 0; i < n; i++) scanf(\"%d %d\", &it[i].w, &it[i].v);\n    std::sort(it, it + n, cmp);\n    double ans = 0;\n    int left = cap;\n    for (int i = 0; i < n && left > 0; i++) {\n        int take = it[i].w < left ? it[i].w : left;       // 能拿多少拿多少\n        ans += (double)it[i].v * take / it[i].w;\n        left -= take;\n    }\n    printf(\"%.2f\\n\", ans);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nstruct Item { int w, v; double r; };\nbool cmpRatio(const Item &a, const Item &b) { return a.r > b.r; }\nint main() {\n    int n, cap;\n    if (scanf(\"%d %d\", &n, &cap) != 2) return 0;\n    static Item it[10];\n    for (int i = 0; i < n; i++) {\n        scanf(\"%d %d\", &it[i].w, &it[i].v);\n        it[i].r = (double)it[i].v / it[i].w;              // 直接用浮点比值\n    }\n    std::sort(it, it + n, cmpRatio);\n    double ans = 0; int left = cap;\n    for (int i = 0; i < n && left > 0; i++) {\n        int take = std::min(it[i].w, left);\n        ans += it[i].r * take;\n        left -= take;\n    }\n    printf(\"%.2f\\n\", ans);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "2 50\n10 60\n20 100\n",
                "expected_stdout": "160.00\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 5\n10 100\n",
                "expected_stdout": "50.00\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2 10\n10 10\n10 20\n",
                "expected_stdout": "20.00\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3 30\n10 60\n20 100\n15 90\n",
                "expected_stdout": "175.00\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1 100\n100 1\n",
                "expected_stdout": "1.00\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4 50\n10 10\n20 30\n30 40\n40 50\n",
                "expected_stdout": "70.00\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【贪心】合并果子",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "贪心",
            "哈夫曼",
            "优先队列"
        ],
        "statement_md": "有 `n` 堆果子，每次把两堆合并成一堆，花费的体力等于两堆重量之和。把所有堆合并成一堆的最小总体力是多少？\n\n**关键点**\n\n- 每次都挑**最轻的两堆**合并（哈夫曼思想），用最小堆维护\n- `priority_queue<int, vector<int>, greater<int>>` 才是小顶堆，默认是大顶堆\n- 输出一个整数",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：最小总体力。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 1 ≤ 重量 ≤ 1000",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 贪心",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <queue>\n#include <vector>\n#include <functional>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    std::priority_queue<int, std::vector<int>, std::greater<int>> pq;   // 小顶堆\n    for (int i = 0; i < n; i++) { int x; scanf(\"%d\", &x); pq.push(x); }\n    long long cost = 0;\n    while (pq.size() > 1) {\n        int a = pq.top(); pq.pop();\n        int b = pq.top(); pq.pop();\n        cost += a + b;\n        pq.push(a + b);\n    }\n    printf(\"%lld\\n\", cost);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    std::sort(a, a + n);               // 有序数组，每次取前两个\n    long long cost = 0;\n    int len = n;\n    while (len > 1) {\n        int s = a[0] + a[1];\n        cost += s;\n        for (int i = 2; i < len; i++) a[i - 2] = a[i];   // 前移两位\n        len -= 2;\n        int pos = len;\n        for (int i = 0; i < len; i++) if (a[i] > s) { pos = i; break; }   // 插入\n        for (int i = len; i > pos; i--) a[i] = a[i - 1];\n        a[pos] = s;\n        len++;\n    }\n    printf(\"%lld\\n\", cost);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 2 3\n",
                "expected_stdout": "9\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n5\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n1 1 1 1\n",
                "expected_stdout": "8\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n3 1 4 1 5\n",
                "expected_stdout": "30\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n10 20 30\n",
                "expected_stdout": "90\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n2 3 4 5 6 7\n",
                "expected_stdout": "68\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【贪心】排队接水总等待时间",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "贪心",
            "排队",
            "前缀和"
        ],
        "statement_md": "`n` 个人排队接水，第 `i` 个人需要 `t[i]` 时间。合理安排顺序，使所有人的**等待时间之和**最小，输出这个最小值（第一个人的等待时间为 0）。\n\n**关键点**\n\n- 按接水时间**从短到长**排，短的先来，后面的人少等\n- 总等待时间 = `n-1` 个 `t1` + `n-2` 个 `t2` + …，可以用前缀和累加\n- 输出一个整数",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：最小总等待时间。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 1 ≤ t[i] ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 贪心",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int t[15];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &t[i]);\n    std::sort(t, t + n);              // 短的先接\n    long long wait = 0, pre = 0;\n    for (int i = 0; i < n; i++) { wait += pre; pre += t[i]; }   // 前缀和累加\n    printf(\"%lld\\n\", wait);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int t[15], cnt[105] = {0};\n    for (int i = 0; i < n; i++) { scanf(\"%d\", &t[i]); cnt[t[i]]++; }\n    long long wait = 0, pre = 0, done = 0;\n    for (int v = 1; v <= 100; v++)          // 计数排序代替 std::sort\n        for (int k = 0; k < cnt[v]; k++) {\n            wait += pre;\n            pre += v;\n            done++;\n        }\n    printf(\"%lld\\n\", wait);\n    (void)done;\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n3 1 2\n",
                "expected_stdout": "4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n5\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n4 3 2 1\n",
                "expected_stdout": "10\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n10 1\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n10 10 10\n",
                "expected_stdout": "30\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n5 4 3 2 1\n",
                "expected_stdout": "20\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【贪心】跳跃游戏最少步数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 16,
        "tags": [
            "贪心",
            "跳跃游戏",
            "BFS"
        ],
        "statement_md": "数组 `a`，从下标 0 出发，站在 `i` 时最多能跳到 `i + a[i]`。求跳到最后一个下标的**最少步数**（保证能到达）。\n\n**关键点**\n\n- 按「层」扩展：当前层的可达范围是 `[0, curEnd]`，走一步后范围扩到 `[0, nextEnd]`\n- 每扩一次层，步数加 1；`curEnd` 到 `i` 时才换层\n- 输出一个整数",
        "input_format": "第一行 `n`，第二行 `n` 个非负整数。",
        "output_format": "一行：最少步数。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 0 ≤ a[i] ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 贪心",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int steps = 0, curEnd = 0, far = 0;\n    for (int i = 0; i < n - 1; i++) {\n        if (i + a[i] > far) far = i + a[i];      // 本层能到的最远处\n        if (i == curEnd) { steps++; curEnd = far; }   // 换层\n    }\n    printf(\"%d\\n\", steps);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005], dp[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    for (int i = 1; i < n; i++) dp[i] = 1 << 30;    // DP：从哪跳过来最省\n    for (int i = 0; i < n; i++)\n        for (int j = i + 1; j <= i + a[i] && j < n; j++)\n            if (dp[i] + 1 < dp[j]) dp[j] = dp[i] + 1;\n    printf(\"%d\\n\", dp[n - 1]);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n2 3 1 1 4\n",
                "expected_stdout": "2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n0\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n1 1 1\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n1 2 3 4 5\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n2 0 1 1\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n1 1 2 1 1 1\n",
                "expected_stdout": "4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【贪心】加油站绕行起点",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 16,
        "tags": [
            "贪心",
            "加油站",
            "环"
        ],
        "statement_md": "`n` 个加油站围成一圈，第 `i` 站能加 `gas[i]` 升油，到下一站要消耗 `cost[i]` 升。油箱初始为空。输出能绕行一圈的起点编号（从 1 开始）；无解输出 `-1`。\n\n**关键点**\n\n- 先看总油量：`sum(gas) < sum(cost)` 必然无解\n- 有解时，从某个点开始的累计油量一旦变负，说明之前所有点都不可能是起点，直接跳到下一点\n- 输出一个整数",
        "input_format": "第一行 `n`；之后 `n` 行，每行 `gas cost`。",
        "output_format": "一行：起点编号或 `-1`。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 0 ≤ gas, cost ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 贪心",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static long long gas[1005], cost[1005];\n    long long total = 0, tank = 0;\n    int start = 0;\n    for (int i = 0; i < n; i++) {\n        scanf(\"%lld %lld\", &gas[i], &cost[i]);\n        total += gas[i] - cost[i];\n        tank += gas[i] - cost[i];\n        if (tank < 0) { start = i + 1; tank = 0; }   // 之前都不可能是起点\n    }\n    printf(\"%d\\n\", total < 0 ? -1 : start + 1);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static long long gas[1005], cost[1005];\n    for (int i = 0; i < n; i++) scanf(\"%lld %lld\", &gas[i], &cost[i]);\n    for (int s = 0; s < n; s++) {          // 暴力试每个起点\n        long long tank = 0;\n        bool ok = true;\n        for (int k = 0; k < n; k++) {\n            int i = (s + k) % n;\n            tank += gas[i] - cost[i];\n            if (tank < 0) { ok = false; break; }\n        }\n        if (ok) { printf(\"%d\\n\", s + 1); return 0; }\n    }\n    printf(\"-1\\n\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 2\n2 3\n3 4\n",
                "expected_stdout": "-1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n5 3\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n3 5\n",
                "expected_stdout": "-1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n2 3\n3 4\n",
                "expected_stdout": "-1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n4 5\n5 4\n3 3\n2 4\n",
                "expected_stdout": "-1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n0 1\n0 1\n2 1\n",
                "expected_stdout": "-1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【贪心】最少会议室",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "贪心",
            "扫描线",
            "会议室"
        ],
        "statement_md": "读入 `n` 个会议时间段 `[l, r]`，同一时刻一个会议室只能开一个会，问最少需要几个会议室（输出任意时刻的最大重叠数）。\n\n**关键点**\n\n- 答案是「任意时刻同时进行的会议数的最大值」\n- 区间按**半开**算：`[0,5)` 与 `[5,10)` 不冲突，前一散场房间立刻能给后一场用\n- 把开始和结束分别排序，用双指针扫：开始就 +1，结束就 -1\n- 输出一个整数",
        "input_format": "第一行 `n`；之后 `n` 行，每行 `l r`。",
        "output_format": "一行：最少会议室数。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 0 ≤ l < r ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 贪心",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int L[1005], R[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d %d\", &L[i], &R[i]);\n    std::sort(L, L + n);\n    std::sort(R, R + n);\n    int i = 0, j = 0, cur = 0, best = 0;\n    while (i < n) {\n        if (L[i] < R[j]) { cur++; if (cur > best) best = cur; i++; }   // 开始\n        else { cur--; j++; }                                           // 结束\n    }\n    printf(\"%d\\n\", best);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <map>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    std::map<int, int> ev;                 // 扫描线：+1 开始、-1 结束\n    for (int i = 0; i < n; i++) {\n        int l, r;\n        scanf(\"%d %d\", &l, &r);\n        ev[l] += 1;\n        ev[r] -= 1;\n    }\n    int cur = 0, best = 0;\n    for (auto &kv : ev) { cur += kv.second; if (cur > best) best = cur; }\n    printf(\"%d\\n\", best);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n0 30\n5 10\n15 20\n",
                "expected_stdout": "2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n0 1\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n0 5\n5 10\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n0 10\n1 2\n3 4\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n0 1\n0 1\n0 1\n0 1\n",
                "expected_stdout": "4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n1 5\n2 6\n3 7\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【贪心】拼接最大数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 16,
        "tags": [
            "贪心",
            "拼接",
            "比较器"
        ],
        "statement_md": "读入 `n` 个正整数，把它们按某种顺序拼成一个最长的数字串（位数固定，就是字典序最大），输出这个数。\n\n**关键点**\n\n- 排序规则不是「谁大谁前」，而是 `a+b > b+a` 时 a 排前面\n- 比较要按**字符串拼接**比，不能按数值比：`9` 和 `91`，9 在前得 991 更大\n- 输出一行",
        "input_format": "第一行 `n`，第二行 `n` 个正整数。",
        "output_format": "一行：拼接出的最大数。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 1 ≤ 数值 ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 贪心",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <string>\n#include <algorithm>\nbool cmp(const std::string &a, const std::string &b) {\n    return a + b > b + a;              // 拼起来比较，不是直接比大小\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    std::string v[10];\n    for (int i = 0; i < n; i++) { int x; scanf(\"%d\", &x); v[i] = std::to_string(x); }\n    std::sort(v, v + n, cmp);\n    for (int i = 0; i < n; i++) printf(\"%s\", v[i].c_str());\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cstring>\nchar s[10][32];\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    for (int i = 0; i < n; i++) { int x; scanf(\"%d\", &x); snprintf(s[i], 32, \"%d\", x); }\n    for (int i = 0; i < n - 1; i++)          // 手写冒泡 + 拼接比较\n        for (int j = 0; j < n - 1 - i; j++) {\n            char ab[64], ba[64];\n            snprintf(ab, 64, \"%s%s\", s[j], s[j + 1]);\n            snprintf(ba, 64, \"%s%s\", s[j + 1], s[j]);\n            if (strcmp(ab, ba) < 0) {\n                char t[32];\n                strcpy(t, s[j]); strcpy(s[j], s[j + 1]); strcpy(s[j + 1], t);\n            }\n        }\n    for (int i = 0; i < n; i++) printf(\"%s\", s[i]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n9 91 1\n",
                "expected_stdout": "9911\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n5\n",
                "expected_stdout": "5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n12 121\n",
                "expected_stdout": "12121\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n3 30 34\n",
                "expected_stdout": "34330\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n1 2 3\n",
                "expected_stdout": "321\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n10 2 9 39\n",
                "expected_stdout": "939210\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【贪心】分饼干",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "贪心",
            "双指针",
            "匹配"
        ],
        "statement_md": "有 `n` 个孩子和 `m` 块饼干，孩子的胃口是 `g[i]`，饼干大小是 `s[j]`。一块饼干只能给一个孩子，且饼干大小不小于胃口才算满足。求最多能满足几个孩子。\n\n**关键点**\n\n- 两个数组都升序排，然后双指针：能喂就喂，喂不了就换更大的饼干\n- 小饼干先给胃口小的，避免浪费大饼干\n- 输入格式：第一行 `n`，第二行 `n` 个胃口；第三行 `m`，第四行 `m` 个饼干大小",
        "input_format": "第一行 `n`；第二行 `n` 个整数；第三行 `m`；第四行 `m` 个整数。",
        "output_format": "一行：最多满足的孩子数。",
        "constraints_md": "- 1 ≤ n, m ≤ 6\n- 1 ≤ 胃口, 饼干 ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 贪心",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n, m;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int g[15], s[15];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &g[i]);\n    if (scanf(\"%d\", &m) != 1) return 0;\n    for (int j = 0; j < m; j++) scanf(\"%d\", &s[j]);\n    std::sort(g, g + n);\n    std::sort(s, s + m);\n    int i = 0, j = 0, c = 0;\n    while (i < n && j < m) {\n        if (s[j] >= g[i]) { c++; i++; j++; }   // 喂得饱就配一对\n        else j++;                              // 这块饼干废了\n    }\n    printf(\"%d\\n\", c);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <set>\nint main() {\n    int n, m;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int g[15];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &g[i]);\n    if (scanf(\"%d\", &m) != 1) return 0;\n    std::multiset<int> box;\n    for (int j = 0; j < m; j++) { int x; scanf(\"%d\", &x); box.insert(x); }\n    int c = 0;\n    for (int i = 0; i < n; i++) {\n        auto it = box.lower_bound(g[i]);          // 找第一块够大的\n        if (it != box.end()) { c++; box.erase(it); }\n    }\n    printf(\"%d\\n\", c);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 2 3\n2\n1 1\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n1 2\n3\n1 2 3\n",
                "expected_stdout": "2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n5\n1\n4\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n10 20 30\n3\n10 20 30\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n5 5\n2\n5 5\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n1 2 3\n1\n2\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【贪心】无重叠区间最少删除数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "贪心",
            "区间",
            "删除"
        ],
        "statement_md": "读入 `n` 个区间，最少删掉几个才能让剩下的区间互不重叠？\n\n**关键点**\n\n- 等价于 `n - 最多能保留几个不重叠区间`\n- 按右端点排序，能接上就保留 —— 和「活动选择」是同一个问题换个问法\n- 输出一个整数",
        "input_format": "第一行 `n`；之后 `n` 行，每行 `l r`。",
        "output_format": "一行：最少删除数。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 0 ≤ l < r ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 贪心",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <algorithm>\nstruct Seg { int l, r; };\nbool cmp(const Seg &a, const Seg &b) { return a.r < b.r; }\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static Seg v[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d %d\", &v[i].l, &v[i].r);\n    std::sort(v, v + n, cmp);\n    int keep = 0, last = -1;\n    for (int i = 0; i < n; i++)\n        if (v[i].l >= last) { keep++; last = v[i].r; }\n    printf(\"%d\\n\", n - keep);        // 删掉的就是接不上的\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int L[1005], R[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d %d\", &L[i], &R[i]);\n    int keep = 0;                    // 暴力选：每轮找右端点最小的可选区间\n    static bool used[1005] = {false};\n    int last = -1;\n    while (true) {\n        int pick = -1;\n        for (int i = 0; i < n; i++)\n            if (!used[i] && L[i] >= last && (pick == -1 || R[i] < R[pick])) pick = i;\n        if (pick == -1) break;\n        used[pick] = true;\n        keep++;\n        last = R[pick];\n    }\n    printf(\"%d\\n\", n - keep);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 2\n2 3\n1 3\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n1 2\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n1 2\n2 3\n3 4\n1 3\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n1 2\n3 4\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n1 10\n2 3\n4 5\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n1 2\n1 2\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【贪心】股票买卖一次最大利润",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "贪心",
            "股票",
            "状态机"
        ],
        "statement_md": "给定每天的股价，只允许买卖**一次**（先买后卖），求最大利润；不能盈利时输出 0。\n\n**关键点**\n\n- 遍历时维护「到目前为止的最低买入价」，每天算一次「今天卖能赚多少」\n- 不要求最后一天卖，随时更新答案\n- 输出一个整数",
        "input_format": "第一行 `n`，第二行 `n` 个整数股价。",
        "output_format": "一行：最大利润。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 0 ≤ 股价 ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 贪心",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int p[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &p[i]);\n    int low = p[0], best = 0;\n    for (int i = 1; i < n; i++) {\n        if (p[i] - low > best) best = p[i] - low;   // 今天卖\n        if (p[i] < low) low = p[i];                 // 更新最低买入价\n    }\n    printf(\"%d\\n\", best);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int p[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &p[i]);\n    int cash = 0, hold = -1000000000;      // 状态机：空仓 / 持仓\n    for (int i = 0; i < n; i++) {\n        int nc = std::max(cash, hold + p[i]);   // 卖出\n        int nh = std::max(hold, -p[i]);         // 买入（只允许一次）\n        cash = nc; hold = nh;\n    }\n    printf(\"%d\\n\", cash);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n7 1 5 3 6\n",
                "expected_stdout": "5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n7 6 4 3 1\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n5\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n1 10\n",
                "expected_stdout": "9\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n8 24 17 -46 -19 -14 35 31 35 -24\n",
                "expected_stdout": "81\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n48 42 29 21 49 73\n",
                "expected_stdout": "52\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【贪心】股票买卖多次总利润",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "贪心",
            "股票",
            "峰谷"
        ],
        "statement_md": "给定每天的股价，允许**多次**买卖（同一天可以先卖再买，但手上最多一股），求能获得的最大总利润。\n\n**关键点**\n\n- 把所有「上涨的相邻差」加起来就是答案 —— 涨就持有，跌就空仓\n- `p[i] > p[i-1]` 时累加 `p[i]-p[i-1]`\n- 输出一个整数",
        "input_format": "第一行 `n`，第二行 `n` 个整数股价。",
        "output_format": "一行：最大总利润。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 0 ≤ 股价 ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 贪心",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int p[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &p[i]);\n    long long profit = 0;\n    for (int i = 1; i < n; i++)\n        if (p[i] > p[i - 1]) profit += p[i] - p[i - 1];   // 涨就赚这段\n    printf(\"%lld\\n\", profit);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int p[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &p[i]);\n    long long profit = 0;\n    int i = 0;\n    while (i < n - 1) {                     // 峰谷法：找每一段上升\n        while (i < n - 1 && p[i + 1] <= p[i]) i++;\n        int buy = p[i];\n        while (i < n - 1 && p[i + 1] > p[i]) i++;\n        profit += p[i] - buy;\n    }\n    printf(\"%lld\\n\", profit);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n7 1 5 3 6\n",
                "expected_stdout": "7\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n7 6 4 3 1\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n5\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n1 10\n",
                "expected_stdout": "9\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n31 -36 -47 44 -15 -19 -22 -33 44 -37\n",
                "expected_stdout": "168\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n4 36 89 97 18 59\n",
                "expected_stdout": "134\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【贪心】删 k 位使剩下最小",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 16,
        "tags": [
            "贪心",
            "删数",
            "单调栈"
        ],
        "statement_md": "给定一个数字串和整数 `k`，删掉其中 `k` 个字符，使剩下的数字最小。输出剩下的数（去掉前导零；全删光输出 `0`）。\n\n**关键点**\n\n- 从左往右扫，一旦「当前位比后一位大」就删掉当前位 —— 用栈实现最自然\n- 扫完后如果还没删够，就从末尾继续删（此时串已非递减）\n- 输出一行",
        "input_format": "第一行一个数字串，第二行整数 `k`。",
        "output_format": "一行：剩下最小的数。",
        "constraints_md": "- 1 ≤ 位数 ≤ 12\n- 0 ≤ k ≤ 位数",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 贪心",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <cstring>\nint main() {\n    char s[32], st[32];\n    int k;\n    if (scanf(\"%31s\", s) != 1) return 0;\n    if (scanf(\"%d\", &k) != 1) return 0;\n    int n = (int)strlen(s), top = 0;\n    for (int i = 0; i < n; i++) {\n        while (top > 0 && k > 0 && st[top - 1] > s[i]) { top--; k--; }   // 栈顶更大就弹\n        st[top++] = s[i];\n    }\n    while (k > 0 && top > 0) { top--; k--; }        // 还得多删就从尾部删\n    st[top] = '\\0';\n    int p = 0;\n    while (p < top && st[p] == '0') p++;            // 去前导零\n    if (p == top) printf(\"0\\n\");\n    else printf(\"%s\\n\", st + p);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cstring>\nint main() {\n    char s[32];\n    int k;\n    if (scanf(\"%31s\", s) != 1) return 0;\n    if (scanf(\"%d\", &k) != 1) return 0;\n    int n = (int)strlen(s);\n    for (int t = 0; t < k; t++) {                   // 每轮删一个「峰」\n        int i = 0;\n        while (i + 1 < n && s[i] <= s[i + 1]) i++;\n        for (int j = i; j + 1 < n; j++) s[j] = s[j + 1];   // 直接删掉 s[i]\n        n--;\n        if (n == 0) break;\n    }\n    s[n] = '\\0';\n    int p = 0;\n    while (p < n && s[p] == '0') p++;\n    if (p == n) printf(\"0\\n\");\n    else printf(\"%s\\n\", s + p);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "1432219\n3\n",
                "expected_stdout": "1219\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "10200\n1\n",
                "expected_stdout": "200\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "10\n2\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1234\n0\n",
                "expected_stdout": "1234\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4321\n2\n",
                "expected_stdout": "21\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100200\n1\n",
                "expected_stdout": "200\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【贪心】田忌赛马",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 16,
        "tags": [
            "贪心",
            "双指针",
            "田忌赛马"
        ],
        "statement_md": "田忌和齐王各有 `n` 匹马，速度分别是 `a[i]` 和 `b[i]`。每场各出一匹，快的赢。田忌知道齐王的出场顺序，可以任意安排自己的出场顺序，求最多能赢几场。\n\n**关键点**\n\n- 两边都排序，然后双指针：用自己最慢的马去「消耗」对方最快的马，或直接赢下对方最慢的\n- 能赢就赢（自己最慢 > 对方最慢）；不能赢就用自己最慢去换对方最快\n- 输入格式：第一行 `n`，第二行田忌的 `n` 匹，第三行齐王的 `n` 匹",
        "input_format": "第一行 `n`；第二行 `n` 个整数；第三行 `n` 个整数。",
        "output_format": "一行：最多胜场数。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 1 ≤ 速度 ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 贪心",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[20], b[20];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &b[i]);\n    std::sort(a, a + n);\n    std::sort(b, b + n);\n    int i = 0, j = 0, win = 0;\n    while (i < n && j < n) {\n        if (a[i] > b[j]) { win++; i++; j++; }   // 我能赢对方最弱的，就先赢\n        else i++;                               // 赢不了，这匹马废了\n    }\n    printf(\"%d\\n\", win);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <set>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int b[20];\n    std::multiset<int> mine;\n    for (int i = 0; i < n; i++) { int x; scanf(\"%d\", &x); mine.insert(x); }\n    for (int i = 0; i < n; i++) scanf(\"%d\", &b[i]);\n    int win = 0;\n    for (int i = 0; i < n; i++) {                 // 对每匹敌马，找最小的能赢的马\n        auto it = mine.upper_bound(b[i]);\n        if (it != mine.end()) { win++; mine.erase(it); }\n        else mine.erase(mine.begin());            // 赢不了就丢最小的\n    }\n    printf(\"%d\\n\", win);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 2 3\n1 2 3\n",
                "expected_stdout": "2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n3 2 1\n1 2 3\n",
                "expected_stdout": "2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n5\n4\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n10 10\n10 10\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n1 5 9\n2 6 8\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n1 2 3 4\n4 3 2 1\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【贪心】导弹拦截（最长不上升子序列）",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 16,
        "tags": [
            "贪心",
            "LIS",
            "二分"
        ],
        "statement_md": "读入 `n` 个导弹高度，一套拦截系统每次只能拦截高度**不高于**前一发的导弹。一套系统最多能拦下多少发（即最长不上升子序列长度）？\n\n**关键点**\n\n- 不是「最长下降」，而是「不上升」：相等也算接得上\n- 贪心 + 二分：维护一个「每条系统当前最低拦截高度」的序列，用 `upper_bound` 定位\n- 输出一个整数",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：最长不上升子序列长度。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 1 ≤ 高度 ≤ 30000",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 贪心",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int tails[1005];\n    int len = 0;\n    for (int i = 0; i < n; i++) {\n        int x; scanf(\"%d\", &x);\n        int lo = 0, hi = len;               // 找第一个 tails[p] < x 的位置\n        while (lo < hi) {\n            int mid = (lo + hi) / 2;\n            if (tails[mid] >= x) lo = mid + 1;\n            else hi = mid;\n        }\n        tails[lo] = x;\n        if (lo == len) len++;\n    }\n    printf(\"%d\\n\", len);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005], dp[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int best = 1;\n    for (int i = 0; i < n; i++) {\n        dp[i] = 1;\n        for (int j = 0; j < i; j++)\n            if (a[j] >= a[i] && dp[j] + 1 > dp[i]) dp[i] = dp[j] + 1;   // 不上升\n        if (dp[i] > best) best = dp[i];\n    }\n    printf(\"%d\\n\", best);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "8\n389 207 155 300 299 170 158 65\n",
                "expected_stdout": "6\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n5\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n1 2 3\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n3 2 1\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n5 5 5 5 5\n",
                "expected_stdout": "5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n1 3 2 4 3 5\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【贪心】装箱问题（首次适应）",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "贪心",
            "装箱",
            "模拟"
        ],
        "statement_md": "箱子容量固定为 100，物品按给定顺序到达，每个物品放进**第一个装得下**的箱子（首次适应策略），装不下就开新箱。读入 `n` 和 `n` 个物品大小，输出用了几个箱子。\n\n**关键点**\n\n- 这题考的是「按规则模拟」，不是求最优装箱 —— 顺序会影响结果\n- 维护每个箱子的剩余空间，从左往右找第一个 `剩余 >= 物品` 的\n- 输出一个整数",
        "input_format": "第一行 `n`，第二行 `n` 个整数（1 ≤ 大小 ≤ 100）。",
        "output_format": "一行：箱子数。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 1 ≤ 大小 ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 贪心",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int left[1005];\n    int cnt = 0;\n    for (int i = 0; i < n; i++) {\n        int sz; scanf(\"%d\", &sz);\n        int placed = 0;\n        for (int k = 0; k < cnt; k++)\n            if (left[k] >= sz) { left[k] -= sz; placed = 1; break; }   // 首次适应\n        if (!placed) { left[cnt++] = 100 - sz; }\n    }\n    printf(\"%d\\n\", cnt);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <vector>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    std::vector<int> left;                 // 只存剩余空间\n    for (int i = 0; i < n; i++) {\n        int sz; scanf(\"%d\", &sz);\n        for (size_t k = 0; k < left.size(); k++)\n            if (left[k] >= sz) { left[k] -= sz; goto next; }\n        left.push_back(100 - sz);\n    next:;\n    }\n    printf(\"%d\\n\", (int)left.size());\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4\n60 40 30 30\n",
                "expected_stdout": "2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n100\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n100 100 100\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n10 20 30 40 50\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n50 60 50 60\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n30 30 30 30 30 30\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【贪心】区间翻转后亮灯数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "贪心",
            "差分",
            "区间翻转"
        ],
        "statement_md": "`n` 盏灯初始全灭（编号 1~n）。进行 `m` 次操作，第 `i` 次把区间 `[l, r]` 内的灯状态全部翻转。输出最后亮着的灯数。\n\n**关键点**\n\n- 暴力逐个翻转是 O(nm)，用差分数组把每次操作降到 O(1)\n- 差分：`d[l] ^= 1`、`d[r+1] ^= 1`，最后求前缀「异或」就知道每盏灯的状态\n- 输出一个整数",
        "input_format": "第一行 `n m`；之后 `m` 行，每行 `l r`。",
        "output_format": "一行：亮着的灯数。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 1 ≤ m ≤ 1000\n- 1 ≤ l ≤ r ≤ n",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 贪心",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n, m;\n    if (scanf(\"%d %d\", &n, &m) != 2) return 0;\n    static int d[1005];\n    for (int i = 0; i < m; i++) {\n        int l, r; scanf(\"%d %d\", &l, &r);\n        d[l] ^= 1;                      // 翻转区间的差分\n        d[r + 1] ^= 1;\n    }\n    int cur = 0, lit = 0;\n    for (int i = 1; i <= n; i++) {\n        cur ^= d[i];                    // 前缀异或 = 当前灯的状态\n        if (cur) lit++;\n    }\n    printf(\"%d\\n\", lit);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <map>\nint main() {\n    int n, m;\n    if (scanf(\"%d %d\", &n, &m) != 2) return 0;\n    std::map<int, int> ev;              // 事件点：在这里切换状态\n    for (int i = 0; i < m; i++) {\n        int l, r; scanf(\"%d %d\", &l, &r);\n        ev[l] ^= 1;\n        ev[r + 1] ^= 1;\n    }\n    int cur = 0, lit = 0, prev = 1;\n    for (auto &kv : ev) {\n        if (cur) lit += kv.first - prev;   // 上一段是亮的\n        cur ^= kv.second;\n        prev = kv.first;\n    }\n    if (cur) lit += n + 1 - prev;\n    printf(\"%d\\n\", lit);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 1\n1 3\n",
                "expected_stdout": "3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5 2\n1 3\n2 5\n",
                "expected_stdout": "3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 1\n1 1\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4 3\n1 2\n3 4\n1 4\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6 2\n1 6\n1 6\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5 3\n1 1\n2 2\n3 3\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【贪心】数列极差",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 16,
        "tags": [
            "贪心",
            "极差",
            "排序"
        ],
        "statement_md": "给定 `n` 个正整数。每次操作取两个数 `a`、`b`，把它们删掉，加入 `a*b+1`，直到只剩一个数。不同的操作顺序会得到不同的结果，求「最大值 - 最小值」。\n\n**关键点**\n\n- 想要最大，每次都挑**最小**的两个乘（小数先乘，留大数最后放大）\n- 想要最小，每次都挑**最大**的两个乘\n- 输出一个整数",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：最大值与最小值之差。",
        "constraints_md": "- 2 ≤ n ≤ 5\n- 1 ≤ 数值 ≤ 20",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 贪心",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <algorithm>\n// 真·贪心：每轮重排后取指定的两个数合并（n<=5，直接排序足够）\nlong long greedy(int *src, int n, int wantMax) {\n    long long v[20];\n    for (int i = 0; i < n; i++) v[i] = src[i];\n    int m = n;\n    for (int step = 0; step < n - 1; step++) {\n        std::sort(v, v + m);                     // 升序\n        long long c;\n        if (wantMax) {                           // 最大：取最小两个\n            c = v[0] * v[1] + 1;\n            v[0] = c;\n            for (int t = 1; t < m - 1; t++) v[t] = v[t + 1];\n        } else {                                 // 最小：取最大两个\n            c = v[m - 1] * v[m - 2] + 1;\n            v[m - 2] = c;\n        }\n        m--;\n    }\n    return v[0];\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n < 2) return 0;\n    static int a[20];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    printf(\"%lld\\n\", greedy(a, n, 1) - greedy(a, n, 0));\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nlong long go(long long *v, int n, int wantMax) {   // 暴力枚举所有操作顺序\n    if (n == 1) return v[0];\n    long long best = wantMax ? -1 : -1;\n    bool first = true;\n    long long tmp[20];\n    for (int i = 0; i < n; i++)\n        for (int j = i + 1; j < n; j++) {\n            int k = 0;\n            for (int t = 0; t < n; t++) if (t != i && t != j) tmp[k++] = v[t];\n            tmp[k] = v[i] * v[j] + 1;\n            long long r = go(tmp, k + 1, wantMax);\n            if (first) { best = r; first = false; }\n            else best = wantMax ? (r > best ? r : best) : (r < best ? r : best);\n        }\n    return best;\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n < 2) return 0;\n    long long v[20], w[20];\n    for (int i = 0; i < n; i++) { scanf(\"%lld\", &v[i]); w[i] = v[i]; }\n    printf(\"%lld\\n\", go(v, n, 1) - go(w, n, 0));\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 2 3\n",
                "expected_stdout": "2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n2 3\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n2 2 2\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n1 2 3 4\n",
                "expected_stdout": "13\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n5 1 2\n",
                "expected_stdout": "4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n1 1 1 1 1\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    }
]
