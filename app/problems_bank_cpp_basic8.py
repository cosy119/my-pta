# -*- coding: utf-8 -*-
"""第 8 册：动态规划 / 综合模拟与数学 —— 自动生成，**不要手改本文件**。

生成器：tools/gen_cpp_basic8.py
题数：40 题 / 240 测试点 / 总分 538

重生成：python tools/gen_cpp_basic8.py
"""

CPP_BASIC8_PROBLEMS: list[dict] = [
    {
        "title": "【DP】01 背包最大价值",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "DP",
            "背包",
            "倒序枚举"
        ],
        "statement_md": "有 `n` 件物品和一个容量为 `V` 的背包。第 `i` 件物品重 `w[i]`、价值 `v[i]`，每件**最多取一次**，求不超过容量能装下的最大总价值。\n\n**关键点**\n\n- `f[j]` = 容量 `j` 时的最大价值；**容量必须倒着枚举** `j = V → w[i]`\n- 倒序是为了保证 `f[j-w[i]]` 还是「没放第 i 件」的旧值 —— 正序就变成完全背包了\n- 输出一个整数",
        "input_format": "第一行 `n V`；之后 `n` 行，每行 `w v`。",
        "output_format": "一行：最大总价值。",
        "constraints_md": "- 1 ≤ n ≤ 10\n- 0 ≤ V ≤ 30\n- 1 ≤ w, v ≤ 50",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 动态规划",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n, V;\n    if (scanf(\"%d %d\", &n, &V) != 2) return 0;\n    int w[20], v[20];\n    for (int i = 0; i < n; i++) scanf(\"%d %d\", &w[i], &v[i]);\n    long long f[205] = {0};\n    for (int i = 0; i < n; i++)\n        for (int j = V; j >= w[i]; j--)          // ★ 倒序：每件只用一次\n            if (f[j - w[i]] + v[i] > f[j]) f[j] = f[j - w[i]] + v[i];\n    printf(\"%lld\\n\", f[V]);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nlong long f[15][205];                            // f[i][j]：前 i 件、容量 j\nint main() {\n    int n, V, w[20], v[20];\n    if (scanf(\"%d %d\", &n, &V) != 2) return 0;\n    for (int i = 0; i < n; i++) scanf(\"%d %d\", &w[i], &v[i]);\n    for (int i = 1; i <= n; i++)\n        for (int j = 0; j <= V; j++) {\n            f[i][j] = f[i - 1][j];\n            if (j >= w[i - 1] && f[i - 1][j - w[i - 1]] + v[i - 1] > f[i][j])\n                f[i][j] = f[i - 1][j - w[i - 1]] + v[i - 1];\n        }\n    printf(\"%lld\\n\", f[n][V]);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "1 5\n3 10\n",
                "expected_stdout": "10\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2 3\n1 5\n2 6\n",
                "expected_stdout": "11\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 5\n2 3\n3 4\n4 5\n",
                "expected_stdout": "7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4 10\n5 10\n4 40\n6 30\n3 50\n",
                "expected_stdout": "90\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3 0\n1 100\n2 200\n3 300\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5 15\n1 2\n2 3\n3 5\n4 7\n5 11\n",
                "expected_stdout": "28\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【DP】完全背包最大价值",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "DP",
            "完全背包",
            "正序枚举"
        ],
        "statement_md": "有 `n` 种物品和一个容量为 `V` 的背包。第 `i` 种物品重 `w[i]`、价值 `v[i]`，每种有**无限多件**，求不超过容量能装下的最大总价值。\n\n**关键点**\n\n- 和 01 背包只差一个字符：容量**正着枚举** `j = w[i] → V`\n- 正序时 `f[j-w[i]]` 已经是「本轮可能放过第 i 种」的新值，正好允许重复取\n- 输出一个整数",
        "input_format": "第一行 `n V`；之后 `n` 行，每行 `w v`。",
        "output_format": "一行：最大总价值。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 0 ≤ V ≤ 20\n- 1 ≤ w, v ≤ 50",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 动态规划",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n, V;\n    if (scanf(\"%d %d\", &n, &V) != 2) return 0;\n    int w[20], v[20];\n    for (int i = 0; i < n; i++) scanf(\"%d %d\", &w[i], &v[i]);\n    long long f[205] = {0};\n    for (int i = 0; i < n; i++)\n        for (int j = w[i]; j <= V; j++)          // ★ 正序：可反复取\n            if (f[j - w[i]] + v[i] > f[j]) f[j] = f[j - w[i]] + v[i];\n    printf(\"%lld\\n\", f[V]);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nlong long memo[10][205];\nint n, V, w[20], v[20];\nlong long best(int i, int cap) {                 // 记忆化递归：自顶向下\n    if (i == n) return 0;\n    if (memo[i][cap] >= 0) return memo[i][cap];\n    long long r = best(i + 1, cap);              // 这一种一件都不拿\n    if (cap >= w[i]) {\n        long long t = best(i, cap - w[i]) + v[i];  // 注意仍是第 i 种\n        if (t > r) r = t;\n    }\n    return memo[i][cap] = r;\n}\nint main() {\n    if (scanf(\"%d %d\", &n, &V) != 2) return 0;\n    for (int i = 0; i < n; i++) scanf(\"%d %d\", &w[i], &v[i]);\n    for (int i = 0; i <= n; i++)\n        for (int j = 0; j <= V; j++) memo[i][j] = -1;\n    printf(\"%lld\\n\", best(0, V));\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "1 10\n2 3\n",
                "expected_stdout": "15\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2 5\n1 5\n2 12\n",
                "expected_stdout": "29\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2 4\n2 3\n3 4\n",
                "expected_stdout": "6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3 7\n1 1\n3 4\n4 6\n",
                "expected_stdout": "10\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1 0\n5 9\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4 12\n2 4\n3 6\n4 9\n5 12\n",
                "expected_stdout": "28\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【DP】最长上升子序列长度",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "DP",
            "LIS",
            "二分"
        ],
        "statement_md": "给定 `n` 个整数，求**最长严格上升子序列**的长度（子序列不要求连续）。\n\n**关键点**\n\n- `d[i]` = 以 `a[i]` 结尾的最长上升子序列长度：`d[i] = 1 + max{d[j] | j<i 且 a[j]<a[i]}`\n- 答案是 `max(d)`，不是 `d[n-1]` —— 这一点最容易写错\n- 输出一个整数",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：最长严格上升子序列长度。",
        "constraints_md": "- 1 ≤ n ≤ 12\n- -100 ≤ a[i] ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 动态规划",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    int a[30], d[30], best = 0;\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    for (int i = 0; i < n; i++) {\n        d[i] = 1;\n        for (int j = 0; j < i; j++)\n            if (a[j] < a[i] && d[j] + 1 > d[i]) d[i] = d[j] + 1;   // 严格上升\n        if (d[i] > best) best = d[i];\n    }\n    printf(\"%d\\n\", best);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint main() {                                     // 贪心 + 二分：O(n log n)\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    int tails[30], len = 0;\n    for (int i = 0; i < n; i++) {\n        int x;\n        scanf(\"%d\", &x);\n        int p = (int)(std::lower_bound(tails, tails + len, x) - tails);\n        tails[p] = x;                            // 严格上升：替换第一个 >= x 的\n        if (p == len) len++;\n    }\n    printf(\"%d\\n\", len);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n1 3 2 4 5\n",
                "expected_stdout": "4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n4 3 2 1\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n1 2 3 4 5\n",
                "expected_stdout": "5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n10 9 2 5 3 7\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n5 5 5\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8\n-3 0 -1 2 -2 4 1 6\n",
                "expected_stdout": "5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【DP】最长公共子序列",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "DP",
            "LCS",
            "记忆化"
        ],
        "statement_md": "给定两个只含小写字母的字符串 `a`、`b`，求它们**最长公共子序列**的长度。\n\n**关键点**\n\n- `f[i][j]` = `a` 前 `i` 个字符与 `b` 前 `j` 个字符的 LCS 长度\n- 字符相等就 `f[i][j] = f[i-1][j-1] + 1`，否则取 `max(f[i-1][j], f[i][j-1])`\n- 输出一个整数",
        "input_format": "两行，各一个字符串。",
        "output_format": "一行：LCS 长度。",
        "constraints_md": "- 1 ≤ 串长 ≤ 10\n- 只含小写字母",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 动态规划",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <cstring>\nint f[20][20];\nint main() {\n    char a[30], b[30];\n    if (scanf(\"%29s %29s\", a, b) != 2) return 0;\n    int n = (int)strlen(a), m = (int)strlen(b);\n    for (int i = 1; i <= n; i++)\n        for (int j = 1; j <= m; j++)\n            f[i][j] = (a[i - 1] == b[j - 1])\n                      ? f[i - 1][j - 1] + 1\n                      : (f[i - 1][j] > f[i][j - 1] ? f[i - 1][j] : f[i][j - 1]);\n    printf(\"%d\\n\", f[n][m]);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cstring>\nchar a[30], b[30];\nint memo[20][20];\nint go(int i, int j) {                           // 记忆化递归\n    if (!i || !j) return 0;\n    if (memo[i][j] >= 0) return memo[i][j];\n    int r = (a[i - 1] == b[j - 1]) ? go(i - 1, j - 1) + 1\n                                   : (go(i - 1, j) > go(i, j - 1) ? go(i - 1, j) : go(i, j - 1));\n    return memo[i][j] = r;\n}\nint main() {\n    if (scanf(\"%29s %29s\", a, b) != 2) return 0;\n    memset(memo, -1, sizeof memo);\n    printf(\"%d\\n\", go((int)strlen(a), (int)strlen(b)));\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "abcde\nace\n",
                "expected_stdout": "3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "abc\nabc\n",
                "expected_stdout": "3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "abc\ndef\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "aab\naab\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "zx\nyy\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "algorithm\nlogarithm\n",
                "expected_stdout": "7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【DP】数字三角形最大路径和",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "DP",
            "数字三角形",
            "自底向上"
        ],
        "statement_md": "给出一个 `n` 行的数字三角形。从顶部出发，每步只能走到**下一行的相邻位置**，一直走到底部，求路径上数字之和的最大值。\n\n**关键点**\n\n- 自底向上：`f[i][j] = a[i][j] + max(f[i+1][j], f[i+1][j+1])`\n- 自顶向下要额外处理边界，倒着推更省事 —— 最后一行的值就是它自己\n- 输出一个整数",
        "input_format": "第一行 `n`；之后 `n` 行，第 `i` 行有 `i` 个整数。",
        "output_format": "一行：最大路径和。",
        "constraints_md": "- 1 ≤ n ≤ 8\n- 0 ≤ 数字 ≤ 99",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 动态规划",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    int a[15][15];\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j <= i; j++) scanf(\"%d\", &a[i][j]);\n    for (int i = n - 2; i >= 0; i--)             // 自底向上\n        for (int j = 0; j <= i; j++)\n            a[i][j] += (a[i + 1][j] > a[i + 1][j + 1] ? a[i + 1][j] : a[i + 1][j + 1]);\n    printf(\"%d\\n\", a[0][0]);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint n, a[15][15];\nint best(int i, int j) {                         // 记忆化：自顶向下\n    if (i == n - 1) return a[i][j];\n    static int memo[15][15];\n    static int done[15][15];\n    if (done[i][j]) return memo[i][j];\n    int x = best(i + 1, j), y = best(i + 1, j + 1);\n    done[i][j] = 1;\n    return memo[i][j] = a[i][j] + (x > y ? x : y);\n}\nint main() {\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j <= i; j++) scanf(\"%d\", &a[i][j]);\n    printf(\"%d\\n\", best(0, 0));\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "1\n5\n",
                "expected_stdout": "5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n1\n2 3\n4 5 6\n",
                "expected_stdout": "10\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n9\n1 2\n3 1 4\n1 2 3 1\n",
                "expected_stdout": "18\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n7\n3 8\n8 1 0\n2 7 4 4\n4 5 2 6 5\n",
                "expected_stdout": "30\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n0\n0 0\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n100\n0 0\n0 0 0\n",
                "expected_stdout": "100\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【DP】最大子段和",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "DP",
            "最大子段和",
            "Kadane"
        ],
        "statement_md": "给定 `n` 个整数（可能为负），求**连续子段**的最大和。子段至少要取一个数。\n\n**关键点**\n\n- `cur = max(a[i], cur + a[i])`，`ans = max(ans, cur)` —— 这就是 Kadane\n- `cur` 一旦变负就直接放弃、从当前数重开，因为负数只会拖累后面的和\n- 输出一个整数",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：最大子段和。",
        "constraints_md": "- 1 ≤ n ≤ 12\n- -100 ≤ a[i] ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 动态规划",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    long long cur = 0, ans = 0;\n    for (int i = 0; i < n; i++) {\n        long long x;\n        scanf(\"%lld\", &x);\n        if (i == 0 || cur < 0) cur = x;          // 前面的和对后面没贡献就丢掉\n        else cur += x;\n        if (i == 0 || cur > ans) ans = cur;\n    }\n    printf(\"%lld\\n\", ans);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {                                     // 前缀和 + 维护最小前缀\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    long long s = 0, mn = 0, ans = 0;\n    for (int i = 0; i < n; i++) {\n        long long x;\n        scanf(\"%lld\", &x);\n        s += x;\n        if (i == 0 || s - mn > ans) ans = s - mn;\n        if (s < mn) mn = s;                      // 更新最小前缀（当前元素之后才用）\n    }\n    printf(\"%lld\\n\", ans);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n1 -2 3 4 -1\n",
                "expected_stdout": "7\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n-1 -2 -3\n",
                "expected_stdout": "-1\n",
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
                "stdin": "4\n2 2 -1 2\n",
                "expected_stdout": "5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n-2 1 -3 4 -1 2\n",
                "expected_stdout": "5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n5 -1 5 -1 5\n",
                "expected_stdout": "13\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【DP】爬楼梯方案数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "DP",
            "斐波那契",
            "滚动变量"
        ],
        "statement_md": "楼梯共 `n` 级，每次可以上 **1 级或 2 级**，问从地面走到第 `n` 级共有多少种走法。\n\n**关键点**\n\n- `f[n] = f[n-1] + f[n-2]`，也就是斐波那契数列（`f[1]=1, f[2]=2`）\n- 也可以直接用组合数算：走了 `k` 次两级，方案数 `C(n-k, k)`，对 `k` 求和\n- 输出一个整数",
        "input_format": "一行，一个整数 `n`。",
        "output_format": "一行：走法总数。",
        "constraints_md": "- 1 ≤ n ≤ 20",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 动态规划",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    long long f[30];\n    f[1] = 1;\n    f[2] = 2;\n    for (int i = 3; i <= n; i++) f[i] = f[i - 1] + f[i - 2];\n    printf(\"%lld\\n\", f[n]);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {                                     // 只用两个滚动变量\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    long long a = 1, b = 2;                      // a = f[1], b = f[2]\n    if (n == 1) { printf(\"1\\n\"); return 0; }\n    for (int i = 3; i <= n; i++) {\n        long long c = a + b;\n        a = b;\n        b = c;\n    }\n    printf(\"%lld\\n\", b);\n    return 0;\n}\n",
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
                "stdin": "10\n",
                "expected_stdout": "89\n",
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
            }
        ]
    },
    {
        "title": "【DP】打家劫舍",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "DP",
            "打家劫舍",
            "相邻约束"
        ],
        "statement_md": "一条街上有 `n` 户人家，第 `i` 户有现金 `a[i]`。若一夜之内偷了两户**相邻**的人家，报警器就会响。求一夜最多能偷到多少钱。\n\n**关键点**\n\n- `f[i]` = 考虑前 `i` 户的最大收益：`f[i] = max(f[i-1], f[i-2] + a[i])`\n- 含义是「第 i 户不偷」或「偷第 i 户、但第 i-1 户不能偷」\n- 输出一个整数",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：最大金额。",
        "constraints_md": "- 1 ≤ n ≤ 12\n- 0 ≤ a[i] ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 动态规划",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    long long p2 = 0, p1 = 0;                    // p2 = f[i-2], p1 = f[i-1]\n    for (int i = 0; i < n; i++) {\n        long long x;\n        scanf(\"%lld\", &x);\n        long long cur = p1 > p2 + x ? p1 : p2 + x;\n        p2 = p1;\n        p1 = cur;\n    }\n    printf(\"%lld\\n\", p1);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nlong long a[30];\nlong long f(int i) {                             // 记忆化递归，从后往前\n    if (i < 0) return 0;\n    if (i == 0) return a[0];\n    static long long memo[30];\n    static int done[30];\n    if (done[i]) return memo[i];\n    long long x = f(i - 1), y = f(i - 2) + a[i];\n    done[i] = 1;\n    return memo[i] = (x > y ? x : y);\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    for (int i = 0; i < n; i++) scanf(\"%lld\", &a[i]);\n    printf(\"%lld\\n\", f(n - 1));\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4\n1 2 3 1\n",
                "expected_stdout": "4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n2 7 9 3 1\n",
                "expected_stdout": "12\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n5\n",
                "expected_stdout": "5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n2 7\n",
                "expected_stdout": "7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n0 0 0 0 0\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n10 1 1 10 1 1\n",
                "expected_stdout": "21\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【DP】编辑距离",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 16,
        "tags": [
            "DP",
            "编辑距离",
            "字符串"
        ],
        "statement_md": "给定两个字符串 `a`、`b`，每次可以**插入 / 删除 / 替换**一个字符，求把 `a` 变成 `b` 所需的最少操作次数。\n\n**关键点**\n\n- `f[i][j]` = `a` 前 `i` 个变成 `b` 前 `j` 个的最少操作数\n- 字符相同：`f[i][j] = f[i-1][j-1]`；不同：`1 + min(删, 增, 换)`\n- 输出一个整数",
        "input_format": "两行，各一个字符串（可含空格以外字符）。",
        "output_format": "一行：最少操作次数。",
        "constraints_md": "- 1 ≤ 串长 ≤ 8",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 动态规划",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <cstring>\nint f[20][20];\nint main() {\n    char a[30] = \"\", b[30] = \"\";\n    if (scanf(\"%29s\", a) != 1) return 0;\n    scanf(\"%29s\", b);\n    int n = (int)strlen(a), m = (int)strlen(b);\n    for (int i = 0; i <= n; i++) f[i][0] = i;    // 全删\n    for (int j = 0; j <= m; j++) f[0][j] = j;    // 全插\n    for (int i = 1; i <= n; i++)\n        for (int j = 1; j <= m; j++) {\n            if (a[i - 1] == b[j - 1]) f[i][j] = f[i - 1][j - 1];\n            else {\n                int t = f[i - 1][j - 1];         // 替换\n                if (f[i - 1][j] < t) t = f[i - 1][j];   // 删除\n                if (f[i][j - 1] < t) t = f[i][j - 1];   // 插入\n                f[i][j] = t + 1;\n            }\n        }\n    printf(\"%d\\n\", f[n][m]);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cstring>\nchar a[30], b[30];\nint memo[20][20];\nint go(int i, int j) {                           // 记忆化递归（后缀版）\n    if (i == 0) return j;\n    if (j == 0) return i;\n    if (memo[i][j] >= 0) return memo[i][j];\n    int r;\n    if (a[i - 1] == b[j - 1]) r = go(i - 1, j - 1);\n    else {\n        int t = go(i - 1, j - 1);\n        int x = go(i - 1, j), y = go(i, j - 1);\n        if (x < t) t = x;\n        if (y < t) t = y;\n        r = t + 1;\n    }\n    return memo[i][j] = r;\n}\nint main() {\n    a[0] = b[0] = 0;\n    if (scanf(\"%29s\", a) != 1) return 0;\n    scanf(\"%29s\", b);\n    memset(memo, -1, sizeof memo);\n    printf(\"%d\\n\", go((int)strlen(a), (int)strlen(b)));\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "abc\nabc\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "abc\nabd\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "abc\nbc\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "kitten\nsitting\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "a\nb\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "abcd\nbadc\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【DP】石子合并最小代价",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 16,
        "tags": [
            "DP",
            "区间DP",
            "石子合并"
        ],
        "statement_md": "有 `n` 堆石子排成一排，第 `i` 堆有 `a[i]` 个。每次只能把**相邻两堆**合并成一堆，代价是这两堆石子数之和。求合并成一堆的**最小总代价**。\n\n**关键点**\n\n- `f[l][r]` = 把 `[l, r]` 合并成一堆的最小代价 = `w(l,r) + min(f[l][k] + f[k+1][r])`\n- `w(l,r)` 是这段石子的总和，先做前缀和，否则每次重算就是 O(n) 拖慢一层\n- 输出一个整数",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：最小总代价。",
        "constraints_md": "- 1 ≤ n ≤ 5\n- 1 ≤ a[i] ≤ 10",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 动态规划",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    long long a[30], s[30] = {0}, f[30][30] = {0};\n    for (int i = 1; i <= n; i++) { scanf(\"%lld\", &a[i]); s[i] = s[i - 1] + a[i]; }\n    for (int len = 2; len <= n; len++)\n        for (int l = 1; l + len - 1 <= n; l++) {\n            int r = l + len - 1;\n            f[l][r] = -1;\n            for (int k = l; k < r; k++) {\n                long long t = f[l][k] + f[k + 1][r];\n                if (f[l][r] < 0 || t < f[l][r]) f[l][r] = t;\n            }\n            f[l][r] += s[r] - s[l - 1];           // 加上本区间的总石子数\n        }\n    printf(\"%lld\\n\", n == 1 ? 0LL : f[1][n]);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cstring>\nlong long a[30], s[30], memo[30][30];\nlong long go(int l, int r) {                     // 记忆化递归（区间版）\n    if (l == r) return 0;\n    if (memo[l][r] >= 0) return memo[l][r];\n    long long best = -1;\n    for (int k = l; k < r; k++) {\n        long long t = go(l, k) + go(k + 1, r);\n        if (best < 0 || t < best) best = t;\n    }\n    return memo[l][r] = best + s[r] - s[l - 1];\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    for (int i = 1; i <= n; i++) { scanf(\"%lld\", &a[i]); s[i] = s[i - 1] + a[i]; }\n    memset(memo, -1, sizeof memo);\n    printf(\"%lld\\n\", go(1, n));\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "2\n1 2\n",
                "expected_stdout": "3\n",
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
                "stdin": "3\n1 2 3\n",
                "expected_stdout": "9\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n4 1 2 3\n",
                "expected_stdout": "19\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n1 1 1 1 1\n",
                "expected_stdout": "12\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n10 1 10\n",
                "expected_stdout": "32\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【DP】带障碍路径计数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "DP",
            "路径计数",
            "障碍"
        ],
        "statement_md": "给一个 `n` 行 `m` 列的网格，`.` 表示空地、`#` 表示障碍。从左上角出发，每步只能**向右或向下**，求走到右下角的路径条数（障碍不能踩）。\n\n**关键点**\n\n- `f[i][j] = f[i-1][j] + f[i][j-1]`，但 `grid[i][j] == '#'` 时 `f[i][j] = 0`\n- 第一行和第一列要单独初始化：碰到第一个障碍之后全是 0\n- 输出一个整数",
        "input_format": "第一行 `n m`；之后 `n` 行，每行 `m` 个字符（`.` 或 `#`）。",
        "output_format": "一行：路径条数。",
        "constraints_md": "- 1 ≤ n, m ≤ 5",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 动态规划",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n, m;\n    if (scanf(\"%d %d\", &n, &m) != 2) return 0;\n    char g[15][15];\n    long long f[15][15] = {0};\n    for (int i = 0; i < n; i++) scanf(\"%14s\", g[i]);\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < m; j++) {\n            if (g[i][j] == '#') { f[i][j] = 0; continue; }\n            if (!i && !j) { f[i][j] = 1; continue; }\n            long long up = i ? f[i - 1][j] : 0;\n            long long lf = j ? f[i][j - 1] : 0;\n            f[i][j] = up + lf;\n        }\n    printf(\"%lld\\n\", f[n - 1][m - 1]);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint n, m;\nchar g[15][15];\nlong long memo[15][15];\nint done[15][15];\nlong long go(int i, int j) {                     // 记忆化递归（从终点往回数）\n    if (i < 0 || j < 0 || g[i][j] == '#') return 0;\n    if (!i && !j) return 1;\n    if (done[i][j]) return memo[i][j];\n    done[i][j] = 1;\n    return memo[i][j] = go(i - 1, j) + go(i, j - 1);\n}\nint main() {\n    if (scanf(\"%d %d\", &n, &m) != 2) return 0;\n    for (int i = 0; i < n; i++) scanf(\"%14s\", g[i]);\n    printf(\"%lld\\n\", go(n - 1, m - 1));\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "2 2\n..\n..\n",
                "expected_stdout": "2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2 2\n.#\n#.\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 3\n...\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3 3\n...\n.#.\n...\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2 3\n...\n...\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3 3\n#..\n...\n...\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【DP】股票买卖一次最大利润",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "DP",
            "股票",
            "一次交易"
        ],
        "statement_md": "给定 `n` 天的股票价格，你最多能**买入一次再卖出一次**（必须先买后卖，也可以不交易），求最大利润。\n\n**关键点**\n\n- 遍历时维护「到目前为止的最低买入价」，当天的最大利润就是 `price - minPrice`\n- 不交易时利润为 0，所以答案至少是 0 —— 别让全跌的情况输出负数\n- 输出一个整数",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：最大利润。",
        "constraints_md": "- 1 ≤ n ≤ 10\n- 0 ≤ 价格 ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 动态规划",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    int mn = 1 << 30, best = 0;\n    for (int i = 0; i < n; i++) {\n        int x;\n        scanf(\"%d\", &x);\n        if (x < mn) mn = x;\n        if (x - mn > best) best = x - mn;\n    }\n    printf(\"%d\\n\", best);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {                                     // 正序求后缀最大值，再扫一遍\n    int n, p[30];\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    for (int i = 0; i < n; i++) scanf(\"%d\", &p[i]);\n    int best = 0;\n    static int mx[30];\n    mx[n - 1] = p[n - 1];\n    for (int i = n - 2; i >= 0; i--) mx[i] = p[i] > mx[i + 1] ? p[i] : mx[i + 1];\n    for (int i = 0; i + 1 < n; i++)\n        if (mx[i + 1] - p[i] > best) best = mx[i + 1] - p[i];\n    printf(\"%d\\n\", best);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "6\n7 1 5 3 6 4\n",
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
                "stdin": "2\n1 5\n",
                "expected_stdout": "4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n2 4 1 7\n",
                "expected_stdout": "6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n1 2 3\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【DP】最少硬币数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "DP",
            "完全背包",
            "最少硬币"
        ],
        "statement_md": "有 `n` 种面额的硬币，每种有**无限多枚**。要凑出金额 `amount`，求**最少**需要几枚；凑不出来输出 `-1`。\n\n**关键点**\n\n- `f[j]` = 凑出 `j` 元的最少枚数，`f[0] = 0`，其余初始化为「无穷大」\n- `f[j] = min(f[j], f[j-coin] + 1)`，最后看 `f[amount]` 是否还是无穷大\n- 输出一个整数",
        "input_format": "第一行 `n amount`；第二行 `n` 个面额。",
        "output_format": "一行：最少硬币数，或 `-1`。",
        "constraints_md": "- 1 ≤ n ≤ 4\n- 0 ≤ amount ≤ 20\n- 1 ≤ 面额 ≤ 20",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 动态规划",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n, amount;\n    if (scanf(\"%d %d\", &n, &amount) != 2) return 0;\n    int c[10];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &c[i]);\n    const int INF = 1000000;\n    int f[105];\n    for (int j = 0; j <= amount; j++) f[j] = INF;\n    f[0] = 0;\n    for (int i = 0; i < n; i++)\n        for (int j = c[i]; j <= amount; j++)       // 正序：每种可用多次\n            if (f[j - c[i]] + 1 < f[j]) f[j] = f[j - c[i]] + 1;\n    printf(\"%d\\n\", f[amount] >= INF ? -1 : f[amount]);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint n, amount, c[10];\nint memo[105];\nint best(int rest) {                             // 记忆化：剩下 rest 元的最少枚数\n    if (rest == 0) return 0;\n    if (memo[rest] >= 0) return memo[rest];\n    const int INF = 1000000;\n    int r = INF;\n    for (int i = 0; i < n; i++)\n        if (c[i] <= rest) {\n            int t = best(rest - c[i]);\n            if (t + 1 < r) r = t + 1;\n        }\n    return memo[rest] = r;\n}\nint main() {\n    if (scanf(\"%d %d\", &n, &amount) != 2) return 0;\n    for (int i = 0; i < n; i++) scanf(\"%d\", &c[i]);\n    for (int j = 0; j <= amount; j++) memo[j] = -1;\n    int r = best(amount);\n    printf(\"%d\\n\", r >= 1000000 ? -1 : r);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3 11\n1 2 5\n",
                "expected_stdout": "3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 3\n2\n",
                "expected_stdout": "-1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2 6\n1 3\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3 0\n1 2 5\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2 7\n2 4\n",
                "expected_stdout": "-1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4 20\n1 5 10 25\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【DP】最大乘积子数组",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 16,
        "tags": [
            "DP",
            "乘积",
            "正负号"
        ],
        "statement_md": "给定 `n` 个整数（可正可负），求**连续子数组**的最大乘积。子数组至少要取一个数。\n\n**关键点**\n\n- 负负得正 —— 所以必须**同时**维护以当前元素结尾的最大值和最小值\n- `mx = max(a, mx*a, mn*a)`、`mn = min(a, mx*a, mn*a)`，注意要用旧值算新值\n- 输出一个整数",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：最大乘积。",
        "constraints_md": "- 1 ≤ n ≤ 8\n- -10 ≤ a[i] ≤ 10",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 动态规划",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    long long a[30];\n    for (int i = 0; i < n; i++) scanf(\"%lld\", &a[i]);\n    long long fmax[30], fmin[30], best = a[0];\n    fmax[0] = fmin[0] = a[0];\n    for (int i = 1; i < n; i++) {\n        long long p1 = fmax[i - 1] * a[i], p2 = fmin[i - 1] * a[i];\n        fmax[i] = a[i];\n        if (p1 > fmax[i]) fmax[i] = p1;\n        if (p2 > fmax[i]) fmax[i] = p2;\n        fmin[i] = a[i];\n        if (p1 < fmin[i]) fmin[i] = p1;\n        if (p2 < fmin[i]) fmin[i] = p2;\n        if (fmax[i] > best) best = fmax[i];\n    }\n    printf(\"%lld\\n\", best);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    long long mx = 0, mn = 0, best = 0;\n    for (int i = 0; i < n; i++) {\n        long long x;\n        scanf(\"%lld\", &x);\n        if (i == 0) { mx = mn = best = x; continue; }\n        long long a = mx * x, b = mn * x;\n        long long hi = x, lo = x;\n        if (a > hi) hi = a;\n        if (b > hi) hi = b;\n        if (a < lo) lo = a;\n        if (b < lo) lo = b;\n        mx = hi;\n        mn = lo;\n        if (mx > best) best = mx;\n    }\n    printf(\"%lld\\n\", best);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n2 3 -2\n",
                "expected_stdout": "6\n",
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
                "stdin": "3\n-2 0 -1\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n-2 3 -4\n",
                "expected_stdout": "24\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n0 2\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n1 -2 -3 4 -5\n",
                "expected_stdout": "60\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【DP】最大子矩阵和",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 16,
        "tags": [
            "DP",
            "最大子矩阵",
            "前缀和"
        ],
        "statement_md": "给定一个 `n` 行 `m` 列的整数矩阵，求它的**子矩阵**（连续的行区间 × 连续的列区间）元素和的最大值。子矩阵至少要含一个元素。\n\n**关键点**\n\n- 先用二维前缀和把「任意子矩阵求和」降到 O(1)，再枚举四条边 —— `n,m ≤ 4` 完全够用\n- 更快的做法是「枚举行的上下界 + 压成一维跑 Kadane」，复杂度 O(n²m)\n- 输出一个整数",
        "input_format": "第一行 `n m`；之后 `n` 行，每行 `m` 个整数。",
        "output_format": "一行：最大子矩阵和。",
        "constraints_md": "- 1 ≤ n, m ≤ 4\n- -50 ≤ 元素 ≤ 50",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 动态规划",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n, m;\n    if (scanf(\"%d %d\", &n, &m) != 2) return 0;\n    long long a[15][15], s[15][15] = {0};\n    for (int i = 1; i <= n; i++)\n        for (int j = 1; j <= m; j++) scanf(\"%lld\", &a[i][j]);\n    for (int i = 1; i <= n; i++)\n        for (int j = 1; j <= m; j++)\n            s[i][j] = a[i][j] + s[i - 1][j] + s[i][j - 1] - s[i - 1][j - 1];\n    long long best = 0;\n    int first = 1;\n    for (int r1 = 1; r1 <= n; r1++)\n        for (int r2 = r1; r2 <= n; r2++)\n            for (int c1 = 1; c1 <= m; c1++)\n                for (int c2 = c1; c2 <= m; c2++) {\n                    long long t = s[r2][c2] - s[r1 - 1][c2] - s[r2][c1 - 1] + s[r1 - 1][c1 - 1];\n                    if (first || t > best) { best = t; first = 0; }\n                }\n    printf(\"%lld\\n\", best);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {                                     // 枚举上下界，压成一维跑 Kadane\n    int n, m;\n    if (scanf(\"%d %d\", &n, &m) != 2) return 0;\n    long long a[15][15];\n    for (int i = 1; i <= n; i++)\n        for (int j = 1; j <= m; j++) scanf(\"%lld\", &a[i][j]);\n    long long best = 0;\n    int first = 1;\n    for (int top = 1; top <= n; top++) {\n        long long col[15] = {0};\n        for (int bot = top; bot <= n; bot++) {\n            for (int j = 1; j <= m; j++) col[j] += a[bot][j];\n            long long cur = 0;\n            for (int j = 1; j <= m; j++) {       // 一维最大子段和\n                cur = (cur > 0 ? cur : 0) + col[j];\n                if (first || cur > best) { best = cur; first = 0; }\n            }\n        }\n    }\n    printf(\"%lld\\n\", best);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "1 1\n-5\n",
                "expected_stdout": "-5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2 2\n1 2\n3 4\n",
                "expected_stdout": "10\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2 2\n-1 -2\n-3 -4\n",
                "expected_stdout": "-1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3 3\n1 -2 3\n-4 5 -6\n7 -8 9\n",
                "expected_stdout": "9\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1 3\n-1 5 -2\n",
                "expected_stdout": "5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3 2\n2 -1\n-1 2\n-1 -1\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【DP】分组背包最大价值",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "DP",
            "分组背包",
            "倒序"
        ],
        "statement_md": "有 `g` 组物品和一个容量为 `V` 的背包。每组内有若干件物品（各有重量与价值），**每组最多只能选一件**，求不超过容量能拿到的最大总价值。\n\n**关键点**\n\n- 外层循环组，内层**倒序**循环容量 —— 这样每组只可能被选一次\n- 组内的每件物品都要试一遍，等价于「这一组选谁」取最大\n- 输出一个整数",
        "input_format": "第一行 `g V`；之后 `g` 组，每组第一行 `k`，随后 `k` 行 `w v`。",
        "output_format": "一行：最大总价值。",
        "constraints_md": "- 1 ≤ g ≤ 3\n- 每组 1 ≤ k ≤ 2\n- 0 ≤ V ≤ 10\n- 1 ≤ w, v ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 动态规划",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int g, V;\n    if (scanf(\"%d %d\", &g, &V) != 2) return 0;\n    long long f[105] = {0};\n    for (int t = 0; t < g; t++) {\n        int k;\n        scanf(\"%d\", &k);\n        int w[10], v[10];\n        for (int i = 0; i < k; i++) scanf(\"%d %d\", &w[i], &v[i]);\n        for (int j = V; j >= 0; j--)               // ★ 倒序：每组只用一次\n            for (int i = 0; i < k; i++)\n                if (j >= w[i] && f[j - w[i]] + v[i] > f[j]) f[j] = f[j - w[i]] + v[i];\n    }\n    printf(\"%lld\\n\", f[V]);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nlong long memo[10][105];\nint g, V, wn[10][10], vn[10][10], kn[10];\nlong long best(int gi, int cap) {                // 记忆化：第 gi 组起、剩 cap 容量\n    if (gi == g) return 0;\n    if (memo[gi][cap] >= 0) return memo[gi][cap];\n    long long r = best(gi + 1, cap);             // 这组不选\n    for (int i = 0; i < kn[gi]; i++)\n        if (wn[gi][i] <= cap) {\n            long long t = best(gi + 1, cap - wn[gi][i]) + vn[gi][i];\n            if (t > r) r = t;\n        }\n    return memo[gi][cap] = r;\n}\nint main() {\n    if (scanf(\"%d %d\", &g, &V) != 2) return 0;\n    for (int t = 0; t < g; t++) {\n        scanf(\"%d\", &kn[t]);\n        for (int i = 0; i < kn[t]; i++) scanf(\"%d %d\", &wn[t][i], &vn[t][i]);\n    }\n    for (int i = 0; i <= g; i++)\n        for (int j = 0; j <= V; j++) memo[i][j] = -1;\n    printf(\"%lld\\n\", best(0, V));\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "1 10\n1\n5 8\n",
                "expected_stdout": "8\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2 10\n2\n3 4\n6 9\n1\n4 5\n",
                "expected_stdout": "14\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 5\n2\n2 3\n3 4\n",
                "expected_stdout": "4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2 3\n1\n5 100\n1\n2 3\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3 8\n1\n2 2\n1\n3 3\n1\n4 4\n",
                "expected_stdout": "7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2 0\n1\n1 5\n1\n1 6\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【DP】最长回文子序列长度",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 16,
        "tags": [
            "DP",
            "回文",
            "区间DP"
        ],
        "statement_md": "给定一个字符串，求它的**最长回文子序列**长度（子序列不要求连续）。\n\n**关键点**\n\n- `f[l][r]`：若 `s[l] == s[r]` 则 `f[l][r] = f[l+1][r-1] + 2`，否则取两端各让一步的最大值\n- 区间 DP 要按**区间长度从小到大**推，`len = 1` 时答案是 1\n- 输出一个整数",
        "input_format": "一行，一个字符串。",
        "output_format": "一行：最长回文子序列长度。",
        "constraints_md": "- 1 ≤ 串长 ≤ 10\n- 只含小写字母",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 动态规划",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <cstring>\nint f[20][20];\nint main() {\n    char s[30];\n    if (scanf(\"%29s\", s) != 1) return 0;\n    int n = (int)strlen(s);\n    for (int i = 0; i < n; i++) f[i][i] = 1;\n    for (int len = 2; len <= n; len++)\n        for (int l = 0; l + len - 1 < n; l++) {\n            int r = l + len - 1;\n            if (s[l] == s[r]) f[l][r] = (len == 2 ? 2 : f[l + 1][r - 1] + 2);\n            else f[l][r] = f[l + 1][r] > f[l][r - 1] ? f[l + 1][r] : f[l][r - 1];\n        }\n    printf(\"%d\\n\", n ? f[0][n - 1] : 0);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cstring>\nchar a[30], b[30];\nint f[20][20];\nint main() {                                     // 转成「原串 与 反转串 的 LCS」\n    if (scanf(\"%29s\", a) != 1) return 0;\n    int n = (int)strlen(a);\n    for (int i = 0; i < n; i++) b[i] = a[n - 1 - i];\n    b[n] = 0;\n    for (int i = 1; i <= n; i++)\n        for (int j = 1; j <= n; j++)\n            f[i][j] = (a[i - 1] == b[j - 1])\n                      ? f[i - 1][j - 1] + 1\n                      : (f[i - 1][j] > f[i][j - 1] ? f[i - 1][j] : f[i][j - 1]);\n    printf(\"%d\\n\", f[n][n]);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "a\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "ab\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "aaa\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "abcba\n",
                "expected_stdout": "5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "abcd\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "aabbaa\n",
                "expected_stdout": "6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【DP】单词拆分",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "DP",
            "字符串",
            "单词拆分"
        ],
        "statement_md": "给定一个目标串和一个词典，问目标串能否由词典里的词**首尾相接**拼出来（每个词可以重复使用）。能则输出 `YES`，否则 `NO`。\n\n**关键点**\n\n- `ok[i]` 表示前 `i` 个字符能否拼出来，`ok[0] = true`\n- `ok[j]` 为真且 `s[j..i)` 在词典里 → `ok[i] = true`\n- 输出 `YES` 或 `NO`",
        "input_format": "第一行目标串；第二行 `n`；之后 `n` 行，每行一个词。",
        "output_format": "一行：`YES` 或 `NO`。",
        "constraints_md": "- 1 ≤ 目标串长度 ≤ 10\n- 1 ≤ n ≤ 3",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 动态规划",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <cstring>\nint main() {\n    char s[40], w[10][40];\n    int n;\n    if (scanf(\"%39s\", s) != 1) return 0;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    for (int i = 0; i < n; i++) scanf(\"%39s\", w[i]);\n    int L = (int)strlen(s);\n    int ok[45] = {1};                             // ok[0] = 1\n    for (int i = 0; i < L; i++) {\n        if (!ok[i]) continue;\n        for (int k = 0; k < n; k++) {\n            int m = (int)strlen(w[k]);\n            if (i + m <= L && strncmp(s + i, w[k], m) == 0) ok[i + m] = 1;\n        }\n    }\n    printf(\"%s\\n\", ok[L] ? \"YES\" : \"NO\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cstring>\nchar s[40], w[10][40];\nint n, L, memo[45];\nint go(int pos) {                                // 记忆化递归：从 pos 往后切\n    if (pos == L) return 1;\n    if (memo[pos] >= 0) return memo[pos];\n    memo[pos] = 0;\n    for (int k = 0; k < n; k++) {\n        int m = (int)strlen(w[k]);\n        if (pos + m <= L && strncmp(s + pos, w[k], m) == 0 && go(pos + m)) {\n            memo[pos] = 1;\n            break;\n        }\n    }\n    return memo[pos];\n}\nint main() {\n    if (scanf(\"%39s\", s) != 1) return 0;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    for (int i = 0; i < n; i++) scanf(\"%39s\", w[i]);\n    L = (int)strlen(s);\n    memset(memo, -1, sizeof memo);\n    printf(\"%s\\n\", go(0) ? \"YES\" : \"NO\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "leetcode\n2\nleet\ncode\n",
                "expected_stdout": "YES\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "applepenapple\n2\napple\npen\n",
                "expected_stdout": "YES\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "catsandog\n3\ncats\ndog\nsand\n",
                "expected_stdout": "NO\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "a\n1\na\n",
                "expected_stdout": "YES\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "ab\n1\na\n",
                "expected_stdout": "NO\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "aaaa\n2\na\naa\n",
                "expected_stdout": "YES\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【DP】矩阵链最小乘法次数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 16,
        "tags": [
            "DP",
            "矩阵链",
            "区间DP"
        ],
        "statement_md": "给定 `n` 个矩阵连乘，第 `i` 个矩阵是 `p[i] × p[i+1]`。矩阵乘法满足结合律，不同的加括号方式标量乘法次数不同，求**最少**次数。\n\n**关键点**\n\n- `f[l][r]` = 第 `l` 到第 `r` 个矩阵相乘的最少次数，枚举断点 `k`\n- `f[l][r] = min(f[l][k] + f[k+1][r] + p[l]*p[k+1]*p[r+1])`\n- 输出一个整数",
        "input_format": "第一行 `n`；第二行 `n+1` 个整数 `p`。",
        "output_format": "一行：最小乘法次数。",
        "constraints_md": "- 1 ≤ n ≤ 5\n- 1 ≤ p[i] ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 动态规划",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    long long p[20], f[20][20] = {0};\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    for (int i = 0; i <= n; i++) scanf(\"%lld\", &p[i]);\n    for (int len = 2; len <= n; len++)\n        for (int l = 1; l + len - 1 <= n; l++) {\n            int r = l + len - 1;\n            f[l][r] = -1;\n            for (int k = l; k < r; k++) {\n                long long t = f[l][k] + f[k + 1][r] + p[l - 1] * p[k] * p[r];\n                if (f[l][r] < 0 || t < f[l][r]) f[l][r] = t;\n            }\n        }\n    printf(\"%lld\\n\", n == 1 ? 0LL : f[1][n]);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cstring>\nlong long p[20], memo[20][20];\nlong long go(int l, int r) {                     // 记忆化递归（矩阵下标从 1 起）\n    if (l == r) return 0;\n    if (memo[l][r] >= 0) return memo[l][r];\n    long long best = -1;\n    for (int k = l; k < r; k++) {\n        long long t = go(l, k) + go(k + 1, r) + p[l - 1] * p[k] * p[r];\n        if (best < 0 || t < best) best = t;\n    }\n    return memo[l][r] = best;\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    for (int i = 0; i <= n; i++) scanf(\"%lld\", &p[i]);\n    memset(memo, -1, sizeof memo);\n    printf(\"%lld\\n\", go(1, n));\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "2\n10 20 30\n",
                "expected_stdout": "6000\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n5 6\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n10 20 30 40\n",
                "expected_stdout": "18000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n40 20 30 10 30\n",
                "expected_stdout": "26000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n1 1 1\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n30 35 15 5 10 20\n",
                "expected_stdout": "11875\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【DP】硬币组合方案数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 16,
        "tags": [
            "DP",
            "组合计数",
            "完全背包"
        ],
        "statement_md": "有 `n` 种面额的硬币，每种有无限多枚。求凑出金额 `amount` 的**方案数**（**组合**计数：`1+2` 与 `2+1` 算同一种）。\n\n**关键点**\n\n- `f[j] += f[j-coin]`，外层枚举硬币、内层**正序**枚举金额 —— 这个顺序才是组合而不是排列\n- `f[0] = 1`（凑 0 元有一种方案：什么都不拿）\n- 输出一个整数",
        "input_format": "第一行 `n amount`；第二行 `n` 个面额。",
        "output_format": "一行：方案数。",
        "constraints_md": "- 1 ≤ n ≤ 3\n- 0 ≤ amount ≤ 20\n- 1 ≤ 面额 ≤ 20",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 动态规划",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n, amount;\n    if (scanf(\"%d %d\", &n, &amount) != 2) return 0;\n    int c[10];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &c[i]);\n    long long f[105] = {0};\n    f[0] = 1;\n    for (int i = 0; i < n; i++)\n        for (int j = c[i]; j <= amount; j++)\n            f[j] += f[j - c[i]];                   // 外层币、内层正序 = 组合\n    printf(\"%lld\\n\", f[amount]);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint n, amount, c[10];\nlong long memo[10][105];\nlong long go(int i, int rest) {                  // 记忆化：从第 i 种起凑 rest 元\n    if (rest == 0) return 1;\n    if (i == n) return 0;\n    if (memo[i][rest] >= 0) return memo[i][rest];\n    long long r = 0;\n    int k = 0;\n    while (k * c[i] <= rest) {\n        r += go(i + 1, rest - k * c[i]);\n        k++;\n    }\n    return memo[i][rest] = r;\n}\nint main() {\n    if (scanf(\"%d %d\", &n, &amount) != 2) return 0;\n    for (int i = 0; i < n; i++) scanf(\"%d\", &c[i]);\n    for (int i = 0; i <= n; i++)\n        for (int j = 0; j <= amount; j++) memo[i][j] = -1;\n    printf(\"%lld\\n\", go(0, amount));\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3 5\n1 2 5\n",
                "expected_stdout": "4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2 0\n1 2\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2 4\n1 2\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1 3\n2\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3 6\n1 3 4\n",
                "expected_stdout": "4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2 10\n2 5\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【模拟】约瑟夫环出列顺序",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "模拟",
            "约瑟夫环",
            "循环链表"
        ],
        "statement_md": "`n` 个人围成一圈，编号 1 到 `n`。从 1 号开始报数，报到 `m` 的人出列，下一个人重新从 1 开始报，求所有人出列的顺序。\n\n**关键点**\n\n- 下标要来回绕：`i = (i + m - 1) % len(v)`，注意 `-1` 是因为报数从自己算起\n- 用数组模拟时，出列后**不要**把后面的人往前挪再回头找下标 —— 很容易差一位\n- 输出一行，出列编号用空格分隔",
        "input_format": "一行两个整数 `n m`。",
        "output_format": "一行：出列顺序，空格分隔。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 1 ≤ m ≤ 5",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 综合模拟与数学",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n, m;\n    if (scanf(\"%d %d\", &n, &m) != 2 || n <= 0) return 0;\n    int gone[30] = {0}, left = n, pos = 0, first = 1;\n    while (left) {\n        int step = 0;\n        while (step < m) {                        // 数 m 个还在圈里的人\n            if (!gone[pos]) step++;\n            if (step < m) pos = (pos + 1) % n;\n        }\n        if (!first) printf(\" \");\n        printf(\"%d\", pos + 1);\n        first = 0;\n        gone[pos] = 1;\n        left--;\n        pos = (pos + 1) % n;\n    }\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint nx[40];\nint main() {                                     // 循环链表模拟\n    int n, m;\n    if (scanf(\"%d %d\", &n, &m) != 2 || n <= 0) return 0;\n    for (int i = 0; i < n; i++) nx[i] = (i + 1) % n;\n    int prev = n - 1, cur = 0, first = 1;\n    for (int left = n; left > 0; left--) {\n        for (int s = 1; s < m; s++) { prev = cur; cur = nx[cur]; }\n        if (!first) printf(\" \");\n        printf(\"%d\", cur + 1);\n        first = 0;\n        nx[prev] = nx[cur];                      // 摘掉 cur\n        cur = nx[cur];\n    }\n    printf(\"\\n\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 2\n",
                "expected_stdout": "2 4 1 5 3\n",
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
                "stdin": "6 3\n",
                "expected_stdout": "3 6 4 2 5 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3 5\n",
                "expected_stdout": "2 3 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4 1\n",
                "expected_stdout": "1 2 3 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2 2\n",
                "expected_stdout": "2 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【模拟】蛇形填数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "模拟",
            "矩阵",
            "蛇形"
        ],
        "statement_md": "输出一个 `n` 行 `n` 列的**蛇形矩阵**：第 1 行从左到右填 1 到 `n`，第 2 行从右到左接着填，第 3 行又从左到右……像蛇一样来回。\n\n**关键点**\n\n- 行号是偶数（0 基）就正着填，奇数就反着填\n- 也可以直接算：第 `i` 行第 `k` 个位置的值是 `i*n + k + 1`，只是列号要翻转\n- 输出 `n` 行，每行 `n` 个整数，空格分隔",
        "input_format": "一行，一个整数 `n`。",
        "output_format": "`n` 行，每行 `n` 个整数。",
        "constraints_md": "- 1 ≤ n ≤ 6",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 综合模拟与数学",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    int g[15][15], cur = 1;\n    for (int i = 0; i < n; i++)\n        for (int k = 0; k < n; k++) {\n            int j = (i % 2 == 0) ? k : (n - 1 - k);\n            g[i][j] = cur;\n            cur++;\n        }\n    for (int i = 0; i < n; i++) {\n        for (int j = 0; j < n; j++) {\n            if (j) printf(\" \");\n            printf(\"%d\", g[i][j]);\n        }\n        printf(\"\\n\");\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {                                     // 不算矩阵，直接按公式输出\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    for (int i = 0; i < n; i++) {\n        for (int k = 0; k < n; k++) {\n            if (k) printf(\" \");\n            int v = (i % 2 == 0) ? (i * n + k + 1)          // 偶数行：正着\n                                 : (i * n + (n - 1 - k) + 1); // 奇数行：反着\n            printf(\"%d\", v);\n        }\n        printf(\"\\n\");\n    }\n    return 0;\n}\n",
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
                "expected_stdout": "1 2 3\n6 5 4\n7 8 9\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n",
                "expected_stdout": "1 2 3 4\n8 7 6 5\n9 10 11 12\n16 15 14 13\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n",
                "expected_stdout": "1 2 3 4 5\n10 9 8 7 6\n11 12 13 14 15\n20 19 18 17 16\n21 22 23 24 25\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n",
                "expected_stdout": "1 2 3 4 5 6\n12 11 10 9 8 7\n13 14 15 16 17 18\n24 23 22 21 20 19\n25 26 27 28 29 30\n36 35 34 33 32 31\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【模拟】螺旋矩阵",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "模拟",
            "螺旋矩阵",
            "边界收缩"
        ],
        "statement_md": "输出一个 `n` 行 `n` 列的**螺旋矩阵**：从左上角开始顺时针由外向内填 1 到 `n²`。\n\n**关键点**\n\n- 维护四条边界 `top / bot / lf / rt`，每走完一条边就收缩对应的那条\n- 收缩后要重新判断 `top <= bot` 和 `lf <= rt`，否则奇数阶会重复写中心\n- 输出 `n` 行，每行 `n` 个整数，空格分隔",
        "input_format": "一行，一个整数 `n`。",
        "output_format": "`n` 行，每行 `n` 个整数。",
        "constraints_md": "- 1 ≤ n ≤ 5",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 综合模拟与数学",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    int g[15][15], cur = 1;\n    int top = 0, bot = n - 1, lf = 0, rt = n - 1;\n    while (top <= bot && lf <= rt) {\n        for (int j = lf; j <= rt; j++) g[top][j] = cur++;\n        top++;\n        for (int i = top; i <= bot; i++) g[i][rt] = cur++;\n        rt--;\n        if (top <= bot) { for (int j = rt; j >= lf; j--) g[bot][j] = cur++; bot--; }\n        if (lf <= rt) { for (int i = bot; i >= top; i--) g[i][lf] = cur++; lf++; }\n    }\n    for (int i = 0; i < n; i++) {\n        for (int j = 0; j < n; j++) { if (j) printf(\" \"); printf(\"%d\", g[i][j]); }\n        printf(\"\\n\");\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {                                     // 方向数组 + 撞墙转向\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int g[15][15];\n    int dr[4] = {0, 1, 0, -1}, dc[4] = {1, 0, -1, 0};\n    int r = 0, c = 0, d = 0;\n    for (int k = 1; k <= n * n; k++) {\n        g[r][c] = k;\n        int nr = r + dr[d], nc = c + dc[d];\n        if (nr < 0 || nr >= n || nc < 0 || nc >= n || g[nr][nc]) {   // 出界或已填\n            d = (d + 1) % 4;\n            nr = r + dr[d];\n            nc = c + dc[d];\n        }\n        r = nr;\n        c = nc;\n    }\n    for (int i = 0; i < n; i++) {\n        for (int j = 0; j < n; j++) { if (j) printf(\" \"); printf(\"%d\", g[i][j]); }\n        printf(\"\\n\");\n    }\n    return 0;\n}\n",
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
        "title": "【数学】两个日期相差天数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "数学",
            "日期",
            "闰年"
        ],
        "statement_md": "给定两个日期（年 月 日），求从第一个日期到第二个日期相差多少天。结果可能为负（第一个日期更晚时）。\n\n**关键点**\n\n- 闰年规则：能被 4 整除且不能被 100 整除，或者能被 400 整除\n- 月天数表里 2 月先按 28 记，是闰年再加 1\n- 输出一个整数",
        "input_format": "两行，每行 `年 月 日`。",
        "output_format": "一行：相差天数（第二行减第一行）。",
        "constraints_md": "- 1900 ≤ 年 ≤ 2100\n- 日期保证合法",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 综合模拟与数学",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint leap(int y) { return (y % 4 == 0 && y % 100 != 0) || y % 400 == 0; }\nlong long days(int y, int m, int d) {            // 距 1 年 1 月 1 日的天数\n    int md[13] = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};\n    long long s = 0;\n    for (int i = 1; i < y; i++) s += leap(i) ? 366 : 365;\n    for (int i = 1; i < m; i++) s += md[i] + (i == 2 && leap(y) ? 1 : 0);\n    return s + d - 1;\n}\nint main() {\n    int y1, m1, d1, y2, m2, d2;\n    if (scanf(\"%d %d %d %d %d %d\", &y1, &m1, &d1, &y2, &m2, &d2) != 6) return 0;\n    printf(\"%lld\\n\", days(y2, m2, d2) - days(y1, m1, d1));\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint leap(int y) { return (y % 4 == 0 && y % 100 != 0) || y % 400 == 0; }\nint main() {                                     // 从早的日期逐天往晚的走\n    int y1, m1, d1, y2, m2, d2;\n    if (scanf(\"%d %d %d %d %d %d\", &y1, &m1, &d1, &y2, &m2, &d2) != 6) return 0;\n    int md[13] = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};\n    int sign = 1;\n    long long a = (long long)y1 * 10000 + m1 * 100 + d1;\n    long long b = (long long)y2 * 10000 + m2 * 100 + d2;\n    if (a > b) { sign = -1; int t; t = y1; y1 = y2; y2 = t; t = m1; m1 = m2; m2 = t; t = d1; d1 = d2; d2 = t; }\n    long long cnt = 0;\n    int y = y1, m = m1, d = d1;\n    while (!(y == y2 && m == m2 && d == d2)) {\n        int lim = md[m] + (m == 2 && leap(y) ? 1 : 0);\n        d++;\n        if (d > lim) { d = 1; m++; if (m > 12) { m = 1; y++; } }\n        cnt++;\n    }\n    printf(\"%lld\\n\", sign * cnt);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "2020 1 1\n2020 1 31\n",
                "expected_stdout": "30\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2020 2 28\n2020 3 1\n",
                "expected_stdout": "2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2000 1 1\n2001 1 1\n",
                "expected_stdout": "366\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2019 12 31\n2020 1 1\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2021 5 5\n2021 5 5\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1900 1 1\n1900 3 1\n",
                "expected_stdout": "59\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【数学】十进制转任意进制",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "数学",
            "进制",
            "取模"
        ],
        "statement_md": "把十进制整数 `n` 转换成 `b` 进制输出（`b` 可能是 2 到 16），10 以上用**大写字母** `A`~`F` 表示。\n\n**关键点**\n\n- 不断 `n % b` 取余数，再把 `n /= b`，最后把余数**倒过来**\n- `n == 0` 要特判输出 `0` —— 否则循环一次都不进，输出空串\n- 输出一行",
        "input_format": "一行两个整数 `n b`。",
        "output_format": "一行：`b` 进制表示。",
        "constraints_md": "- 0 ≤ n ≤ 100000\n- 2 ≤ b ≤ 16",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 综合模拟与数学",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n, b;\n    if (scanf(\"%d %d\", &n, &b) != 2) return 0;\n    const char *D = \"0123456789ABCDEF\";\n    if (n == 0) { printf(\"0\\n\"); return 0; }\n    char s[40];\n    int k = 0;\n    while (n) { s[k++] = D[n % b]; n /= b; }\n    for (int i = k - 1; i >= 0; i--) putchar(s[i]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nconst char *D = \"0123456789ABCDEF\";\nvoid pr(int n, int b) {                          // 递归：先处理高位\n    if (n >= b) pr(n / b, b);\n    putchar(D[n % b]);\n}\nint main() {\n    int n, b;\n    if (scanf(\"%d %d\", &n, &b) != 2) return 0;\n    if (n == 0) { printf(\"0\\n\"); return 0; }\n    pr(n, b);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "10 2\n",
                "expected_stdout": "1010\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "255 16\n",
                "expected_stdout": "FF\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "0 2\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7 8\n",
                "expected_stdout": "7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100 3\n",
                "expected_stdout": "10201\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100000 16\n",
                "expected_stdout": "186A0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【数学】阶乘末尾零的个数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "数学",
            "阶乘",
            "因子5"
        ],
        "statement_md": "给定 `n`，求 `n!` 末尾有多少个连续的 0。\n\n**关键点**\n\n- 末尾的 0 来自因子 10 = 2 × 5，而 2 远比 5 多，所以只数**因子 5 的个数**\n- `n/5 + n/25 + n/125 + ...`，因为 25 贡献两个 5、125 贡献三个\n- `long long` 也不够装 1000! —— 别想着先把阶乘算出来\n- 输出一个整数",
        "input_format": "一行，一个整数 `n`。",
        "output_format": "一行：末尾零的个数。",
        "constraints_md": "- 0 ≤ n ≤ 1000",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 综合模拟与数学",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    long long cnt = 0;\n    for (long long p = 5; p <= n; p *= 5) cnt += n / p;\n    printf(\"%lld\\n\", cnt);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {                                     // 反复除以 5\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    long long cnt = 0;\n    int t = n;\n    while (t >= 5) { t /= 5; cnt += t; }\n    printf(\"%lld\\n\", cnt);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "10\n",
                "expected_stdout": "2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100\n",
                "expected_stdout": "24\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "25\n",
                "expected_stdout": "6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1000\n",
                "expected_stdout": "249\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【数学】最大公约数与最小公倍数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "数学",
            "gcd",
            "lcm"
        ],
        "statement_md": "给定两个正整数 `a`、`b`，输出它们的最大公约数和最小公倍数。\n\n**关键点**\n\n- 辗转相除：`while (b) { t = a % b; a = b; b = t; }`，循环结束 `a` 就是 gcd\n- `lcm = a / gcd * b` —— **先除后乘**，否则 `a*b` 可能溢出\n- 输出两个整数，空格分隔",
        "input_format": "一行两个正整数 `a b`。",
        "output_format": "一行：`gcd lcm`。",
        "constraints_md": "- 1 ≤ a, b ≤ 1000",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 综合模拟与数学",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    long long a, b;\n    if (scanf(\"%lld %lld\", &a, &b) != 2) return 0;\n    long long x = a, y = b;\n    while (y) { long long t = x % y; x = y; y = t; }\n    printf(\"%lld %lld\\n\", x, a / x * b);         // 先除后乘防溢出\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {                                     // 更相减损：大减小，直到相等\n    long long a, b;\n    if (scanf(\"%lld %lld\", &a, &b) != 2) return 0;\n    long long x = a, y = b;\n    while (x != y) {\n        if (x > y) x -= y;\n        else y -= x;\n    }\n    printf(\"%lld %lld\\n\", x, a / x * b);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "12 18\n",
                "expected_stdout": "6 36\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "7 13\n",
                "expected_stdout": "1 91\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 1\n",
                "expected_stdout": "1 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100 75\n",
                "expected_stdout": "25 300\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6 6\n",
                "expected_stdout": "6 6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1 1000\n",
                "expected_stdout": "1 1000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【数学】区间内素数个数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "数学",
            "素数",
            "筛法"
        ],
        "statement_md": "给定 `n`，统计 `1` 到 `n` 之间（含 `n`）有多少个素数。\n\n**关键点**\n\n- 试除法：判 `x` 是否素数只需试到 `sqrt(x)`，注意用 `k*k <= x` 而不是 `k <= sqrt(x)`\n- `1` 不是素数、`2` 是素数 —— 这两条最容易漏\n- 输出一个整数",
        "input_format": "一行，一个整数 `n`。",
        "output_format": "一行：素数个数。",
        "constraints_md": "- 1 ≤ n ≤ 10000",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 综合模拟与数学",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static int comp[10005];\n    int cnt = 0;\n    for (int i = 2; i <= n; i++) {               // 埃氏筛\n        if (comp[i]) continue;\n        cnt++;\n        for (long long j = (long long)i * i; j <= n; j += i) comp[j] = 1;\n    }\n    printf(\"%d\\n\", cnt);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {                                     // 逐个试除\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    int cnt = 0;\n    for (int x = 2; x <= n; x++) {\n        int ok = 1;\n        for (int k = 2; (long long)k * k <= x; k++)\n            if (x % k == 0) { ok = 0; break; }\n        if (ok) cnt++;\n    }\n    printf(\"%d\\n\", cnt);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "1\n",
                "expected_stdout": "0\n",
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
                "stdin": "10\n",
                "expected_stdout": "4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100\n",
                "expected_stdout": "25\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1000\n",
                "expected_stdout": "168\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10000\n",
                "expected_stdout": "1229\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【数学】组合数取模",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 16,
        "tags": [
            "数学",
            "组合数",
            "取模"
        ],
        "statement_md": "给定 `n` 和 `k`，求 `C(n, k) mod 1000000007`。\n\n**关键点**\n\n- 递推式 `C(i, j) = C(i-1, j-1) + C(i-1, j)`（杨辉三角），`n ≤ 30` 直接打表\n- 也可以乘除约分：`res = res * (n-i) / (i+1)`，每一步都能整除，但要保证先乘后除不溢出\n- 输出一个整数",
        "input_format": "一行两个整数 `n k`。",
        "output_format": "一行：`C(n, k) mod 1000000007`。",
        "constraints_md": "- 0 ≤ n ≤ 30\n- 0 ≤ k ≤ n",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 综合模拟与数学",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n, k;\n    if (scanf(\"%d %d\", &n, &k) != 2) return 0;\n    long long c[40][40] = {0};\n    for (int i = 0; i <= n; i++) {\n        c[i][0] = c[i][i] = 1;\n        for (int j = 1; j < i; j++)\n            c[i][j] = (c[i - 1][j - 1] + c[i - 1][j]) % 1000000007;\n    }\n    printf(\"%lld\\n\", c[n][k] % 1000000007);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {                                     // 乘除约分（n 小时结果不超 long long）\n    int n, k;\n    if (scanf(\"%d %d\", &n, &k) != 2) return 0;\n    if (k > n - k) k = n - k;                    // C(n,k) = C(n,n-k)，少算几步\n    long long res = 1;\n    for (int i = 1; i <= k; i++) {\n        res = res * (n - k + i) / i;             // 每步都能整除\n        res %= 1000000007;\n    }\n    printf(\"%lld\\n\", res % 1000000007);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 2\n",
                "expected_stdout": "10\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "10 0\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "30 15\n",
                "expected_stdout": "155117520\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "0 0\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6 3\n",
                "expected_stdout": "20\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "20 10\n",
                "expected_stdout": "184756\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【数学】杨辉三角第 n 行",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "数学",
            "杨辉三角",
            "组合数"
        ],
        "statement_md": "输出杨辉三角第 `n` 行（**从 0 开始编号**，第 0 行就是 `1`）。\n\n**关键点**\n\n- 第 `n` 行第 `k` 个数就是 `C(n, k)`\n- 用一维数组**倒序**更新可以原地算出整行（正序会用到本行已更新的值）\n- 输出一行，数字用空格分隔",
        "input_format": "一行，一个整数 `n`。",
        "output_format": "一行：第 `n` 行的所有数。",
        "constraints_md": "- 0 ≤ n ≤ 12",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 综合模拟与数学",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n < 0) return 0;\n    long long row[40] = {1};\n    for (int i = 1; i <= n; i++)\n        for (int j = i; j >= 1; j--) row[j] += row[j - 1];   // 倒序原地更新\n    for (int j = 0; j <= n; j++) {\n        if (j) printf(\" \");\n        printf(\"%lld\", row[j]);\n    }\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {                                     // 直接用组合数递推\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n < 0) return 0;\n    long long v = 1;\n    for (int k = 0; k <= n; k++) {\n        if (k) printf(\" \");\n        printf(\"%lld\", v);\n        v = v * (n - k) / (k + 1);                // C(n,k+1) = C(n,k)*(n-k)/(k+1)\n    }\n    printf(\"\\n\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "0\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n",
                "expected_stdout": "1 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n",
                "expected_stdout": "1 2 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n",
                "expected_stdout": "1 3 3 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n",
                "expected_stdout": "1 5 10 10 5 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "12\n",
                "expected_stdout": "1 12 66 220 495 792 924 792 495 220 66 12 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【数学】整数拆分方案数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 16,
        "tags": [
            "数学",
            "整数拆分",
            "组合"
        ],
        "statement_md": "把正整数 `n` 写成若干个正整数之和（**不计顺序**，例如 `3 = 1+2` 与 `2+1` 算一种），求方案数。注意 `n` 本身也算一种拆法。\n\n**关键点**\n\n- 拆的时候强制「后一块不大于前一块」，同一种拆法就只会被数一次\n- 或者按完全背包理解：`f[j] += f[j-i]`，`i` 从 1 到 n 外层循环 —— 这才是组合不是排列\n- 输出一个整数",
        "input_format": "一行，一个整数 `n`。",
        "output_format": "一行：拆分方案数。",
        "constraints_md": "- 1 ≤ n ≤ 12",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 综合模拟与数学",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    long long f[30] = {0};\n    f[0] = 1;\n    for (int i = 1; i <= n; i++)                 // 外层是「用到的最大数」\n        for (int j = i; j <= n; j++) f[j] += f[j - i];\n    printf(\"%lld\\n\", f[n]);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nlong long memo[30][30];\nlong long go(int rem, int mx) {                  // 记忆化：剩 rem，下一块不超过 mx\n    if (rem == 0) return 1;\n    if (memo[rem][mx] >= 0) return memo[rem][mx];\n    long long c = 0;\n    for (int k = (rem < mx ? rem : mx); k >= 1; k--) c += go(rem - k, k);\n    return memo[rem][mx] = c;\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    for (int i = 0; i <= n; i++)\n        for (int j = 0; j <= n; j++) memo[i][j] = -1;\n    printf(\"%lld\\n\", go(n, n));\n    return 0;\n}\n",
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
                "expected_stdout": "7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8\n",
                "expected_stdout": "22\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "12\n",
                "expected_stdout": "77\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【模拟】队列操作序列",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "模拟",
            "队列",
            "FIFO"
        ],
        "statement_md": "按顺序执行 `n` 条队列操作：`push x` 入队、`pop` 出队（队列空时输出 `EMPTY`）、`size` 查询元素个数。按执行顺序输出 `pop` 和 `size` 的结果。\n\n**关键点**\n\n- 队列是**先进先出**，别写成栈的 `pop_back`\n- `pop` 和 `size` 都要输出，`push` 不输出 —— 漏一条输出就全错位\n- 输出若干行，每行一个结果",
        "input_format": "第一行 `n`；之后 `n` 行，每行一条操作。",
        "output_format": "若干行：每次 `pop` / `size` 的结果。",
        "constraints_md": "- 1 ≤ n ≤ 10\n- 0 ≤ x ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 综合模拟与数学",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <cstring>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    int q[105], head = 0, tail = 0;\n    char op[20];\n    for (int i = 0; i < n; i++) {\n        scanf(\"%19s\", op);\n        if (!strcmp(op, \"push\")) { int x; scanf(\"%d\", &x); q[tail++] = x; }\n        else if (!strcmp(op, \"pop\")) {\n            if (head == tail) printf(\"EMPTY\\n\");\n            else printf(\"%d\\n\", q[head++]);\n        } else printf(\"%d\\n\", tail - head);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cstring>\n#include <queue>\nint main() {                                     // 直接用 STL 的 queue\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    std::queue<int> q;\n    char op[20];\n    for (int i = 0; i < n; i++) {\n        scanf(\"%19s\", op);\n        if (!strcmp(op, \"push\")) { int x; scanf(\"%d\", &x); q.push(x); }\n        else if (!strcmp(op, \"pop\")) {\n            if (q.empty()) printf(\"EMPTY\\n\");\n            else { printf(\"%d\\n\", q.front()); q.pop(); }\n        } else printf(\"%d\\n\", (int)q.size());\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\npush 1\npush 2\npop\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\npop\nsize\n",
                "expected_stdout": "EMPTY\n0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\npush 5\nsize\npop\nsize\npop\n",
                "expected_stdout": "1\n5\n0\nEMPTY\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\nsize\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\npush 0\npush 0\npop\npop\n",
                "expected_stdout": "0\n0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\npop\npop\npop\n",
                "expected_stdout": "EMPTY\nEMPTY\nEMPTY\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【模拟】扫雷数字统计",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "模拟",
            "扫雷",
            "八方向"
        ],
        "statement_md": "给一个 `n` 行 `m` 列的雷区，`*` 是雷、`.` 是空地。对每个格子输出：雷格输出 `*`，空地输出它**周围 8 个方向**上的雷数。\n\n**关键点**\n\n- 8 个方向就是 `di, dj ∈ {-1,0,1}` 的九宫格去掉 `(0,0)`\n- 越界一定要判，否则读到别的行会算出离谱的数字\n- 输出 `n` 行，每行 `m` 个字符，不要空格",
        "input_format": "第一行 `n m`；之后 `n` 行，每行 `m` 个字符。",
        "output_format": "`n` 行，每行 `m` 个字符。",
        "constraints_md": "- 1 ≤ n, m ≤ 5",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 综合模拟与数学",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n, m;\n    if (scanf(\"%d %d\", &n, &m) != 2) return 0;\n    char g[15][15];\n    for (int i = 0; i < n; i++) scanf(\"%14s\", g[i]);\n    for (int i = 0; i < n; i++) {\n        for (int j = 0; j < m; j++) {\n            if (g[i][j] == '*') { putchar('*'); continue; }\n            int c = 0;\n            for (int di = -1; di <= 1; di++)\n                for (int dj = -1; dj <= 1; dj++) {\n                    if (!di && !dj) continue;\n                    int a = i + di, b = j + dj;\n                    if (a >= 0 && a < n && b >= 0 && b < m && g[a][b] == '*') c++;\n                }\n            putchar('0' + c);\n        }\n        putchar('\\n');\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {                                     // 二维前缀和求 3x3 窗口\n    int n, m;\n    if (scanf(\"%d %d\", &n, &m) != 2) return 0;\n    char g[15][15];\n    int s[20][20] = {0};\n    for (int i = 0; i < n; i++) scanf(\"%14s\", g[i]);\n    for (int i = 1; i <= n; i++)\n        for (int j = 1; j <= m; j++)\n            s[i][j] = (g[i - 1][j - 1] == '*') + s[i - 1][j] + s[i][j - 1] - s[i - 1][j - 1];\n    for (int i = 0; i < n; i++) {\n        for (int j = 0; j < m; j++) {\n            if (g[i][j] == '*') { putchar('*'); continue; }\n            int r1 = i - 1, c1 = j - 1, r2 = i + 2, c2 = j + 2;   // 九宫格 → 前缀区间\n            if (r1 < 0) r1 = 0;\n            if (c1 < 0) c1 = 0;\n            if (r2 > n) r2 = n;\n            if (c2 > m) c2 = m;\n            int c = s[r2][c2] - s[r1][c2] - s[r2][c1] + s[r1][c1];\n            putchar('0' + c);\n        }\n        putchar('\\n');\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "1 1\n.\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 1\n*\n",
                "expected_stdout": "*\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2 2\n**\n**\n",
                "expected_stdout": "**\n**\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3 3\n...\n.*.\n...\n",
                "expected_stdout": "111\n1*1\n111\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2 3\n.*.\n...\n",
                "expected_stdout": "1*1\n111\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3 3\n***\n***\n***\n",
                "expected_stdout": "***\n***\n***\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【数学】分数化简",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "数学",
            "分数",
            "gcd"
        ],
        "statement_md": "给定一个分数 `a/b`（`b ≠ 0`，`a` 可能为负、`b` 也可能为负），把它化成最简形式。若化简后分母为 1，就只输出整数；负号一律放分子。\n\n**关键点**\n\n- 分子分母同除 `gcd(|a|, |b|)`；**负数取模要小心**，先取绝对值算 gcd\n- 分母是负数时把符号翻到分子上，`4/-6` 应输出 `-2/3`\n- `a == 0` 直接输出 `0`（否则会输出 `0/1`）",
        "input_format": "一行两个整数 `a b`。",
        "output_format": "一行：最简分数或整数。",
        "constraints_md": "- -1000 ≤ a ≤ 1000\n- 1 ≤ |b| ≤ 1000",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 综合模拟与数学",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nlong long iabs(long long x) { return x < 0 ? -x : x; }\nint main() {\n    long long a, b;\n    if (scanf(\"%lld %lld\", &a, &b) != 2) return 0;\n    if (a == 0) { printf(\"0\\n\"); return 0; }\n    long long x = iabs(a), y = iabs(b);\n    while (y) { long long t = x % y; x = y; y = t; }\n    a /= x;\n    b /= x;\n    if (b < 0) { a = -a; b = -b; }\n    if (b == 1) printf(\"%lld\\n\", a);\n    else printf(\"%lld/%lld\\n\", a, b);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {                                     // 更相减损求 gcd\n    long long a, b;\n    if (scanf(\"%lld %lld\", &a, &b) != 2) return 0;\n    if (a == 0) { printf(\"0\\n\"); return 0; }\n    long long x = a < 0 ? -a : a, y = b < 0 ? -b : b;\n    long long p = x, q = y;\n    while (p != q) {\n        if (p > q) p -= q;\n        else q -= p;\n    }\n    a /= p;\n    b /= p;\n    if (b < 0) { a = -a; b = -b; }\n    if (b == 1) printf(\"%lld\\n\", a);\n    else printf(\"%lld/%lld\\n\", a, b);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4 6\n",
                "expected_stdout": "2/3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "-4 6\n",
                "expected_stdout": "-2/3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4 -6\n",
                "expected_stdout": "-2/3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6 3\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "0 5\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7 1\n",
                "expected_stdout": "7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【模拟】回文数判断",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "模拟",
            "回文",
            "整数反转"
        ],
        "statement_md": "给定一个整数，判断它是不是回文数（正着读和倒着读一样）。负数不算回文。\n\n**关键点**\n\n- 转成字符串用双指针从前后来比最直观\n- 不想开字符串就用整数反转：`rev = rev*10 + x%10`，最后比 `rev == 原数`\n- 输出 `YES` 或 `NO`",
        "input_format": "一行，一个整数。",
        "output_format": "一行：`YES` 或 `NO`。",
        "constraints_md": "- -2³¹ ≤ n ≤ 2³¹-1",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 综合模拟与数学",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    long long n;\n    if (scanf(\"%lld\", &n) != 1) return 0;\n    if (n < 0) { printf(\"NO\\n\"); return 0; }\n    long long rev = 0, t = n;\n    while (t) { rev = rev * 10 + t % 10; t /= 10; }\n    printf(\"%s\\n\", rev == n ? \"YES\" : \"NO\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cstring>\nint main() {                                     // 字符串双指针\n    char s[40];\n    if (scanf(\"%39s\", s) != 1) return 0;\n    if (s[0] == '-') { printf(\"NO\\n\"); return 0; }\n    int i = 0, j = (int)strlen(s) - 1, ok = 1;\n    while (i < j) {\n        if (s[i] != s[j]) { ok = 0; break; }\n        i++;\n        j--;\n    }\n    printf(\"%s\\n\", ok ? \"YES\" : \"NO\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "121\n",
                "expected_stdout": "YES\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "-121\n",
                "expected_stdout": "NO\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "10\n",
                "expected_stdout": "NO\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "0\n",
                "expected_stdout": "YES\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "12321\n",
                "expected_stdout": "YES\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1000\n",
                "expected_stdout": "NO\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【数学】快速幂取模",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 16,
        "tags": [
            "数学",
            "快速幂",
            "二进制"
        ],
        "statement_md": "给定 `a`、`b`、`m`，求 `a^b mod m`（`b` 可能很大，不能一层循环乘 `b` 次）。\n\n**关键点**\n\n- 把 `b` 按二进制拆开：每右移一位就把底数平方、`b` 的当前位是 1 就把它乘进答案\n- 每次乘完都要 `% m`，否则中途就溢出了\n- `b == 0` 时答案是 `1 % m`（`m == 1` 时是 0）",
        "input_format": "一行三个整数 `a b m`。",
        "output_format": "一行：`a^b mod m`。",
        "constraints_md": "- 0 ≤ a ≤ 1000\n- 0 ≤ b ≤ 10⁹\n- 1 ≤ m ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 综合模拟与数学",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    long long a, b, m;\n    if (scanf(\"%lld %lld %lld\", &a, &b, &m) != 3) return 0;\n    long long res = 1 % m;\n    a %= m;\n    while (b) {\n        if (b & 1) res = res * a % m;            // 当前位是 1，乘进来\n        a = a * a % m;                           // 底数平方\n        b >>= 1;\n    }\n    printf(\"%lld\\n\", res);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nlong long pw(long long a, long long b, long long m) {   // 递归版\n    if (b == 0) return 1 % m;\n    long long t = pw(a, b / 2, m);\n    t = t * t % m;\n    if (b & 1) t = t * (a % m) % m;\n    return t;\n}\nint main() {\n    long long a, b, m;\n    if (scanf(\"%lld %lld %lld\", &a, &b, &m) != 3) return 0;\n    printf(\"%lld\\n\", pw(a, b, m));\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "2 10 1000\n",
                "expected_stdout": "24\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 0 7\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5 3 13\n",
                "expected_stdout": "8\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7 5 1\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2 1000000000 1000000007\n",
                "expected_stdout": "140625001\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "123456 789 99991\n",
                "expected_stdout": "19735\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【数学】正约数个数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "数学",
            "约数",
            "sqrt"
        ],
        "statement_md": "给定正整数 `n`，求它有多少个正约数。\n\n**关键点**\n\n- 只需枚举到 `sqrt(n)`：`k` 是约数，`n/k` 也是，一对算两个\n- `k*k == n` 时只算一个（完全平方数别重复数）\n- 输出一个整数",
        "input_format": "一行，一个整数 `n`。",
        "output_format": "一行：正约数个数。",
        "constraints_md": "- 1 ≤ n ≤ 100000",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 综合模拟与数学",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    int c = 0;\n    for (int k = 1; (long long)k * k <= n; k++)\n        if (n % k == 0) c += (k * k == n) ? 1 : 2;\n    printf(\"%d\\n\", c);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {                                     // 直接枚举 1..n（n 小时也够快）\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    int c = 0;\n    for (int k = 1; k <= n; k++)\n        if (n % k == 0) c++;\n    printf(\"%d\\n\", c);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "1\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "12\n",
                "expected_stdout": "6\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "36\n",
                "expected_stdout": "9\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "97\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100000\n",
                "expected_stdout": "36\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "65536\n",
                "expected_stdout": "17\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【数学】鸡兔同笼",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "数学",
            "方程",
            "枚举"
        ],
        "statement_md": "笼子里有鸡和兔，共有 `h` 个头、`f` 只脚。求鸡和兔各几只；若数据不可能成立，输出 `-1`。\n\n**关键点**\n\n- 设鸡 `c` 只、兔 `r` 只：`c + r = h`、`2c + 4r = f`，联立得 `r = (f - 2h) / 2`\n- `f - 2h` 必须是**非负偶数**，否则无解\n- 输出 `鸡 兔`，空格分隔",
        "input_format": "一行两个整数 `h f`。",
        "output_format": "一行：`鸡 兔`，或 `-1`。",
        "constraints_md": "- 0 ≤ h ≤ 100\n- 0 ≤ f ≤ 400",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 综合模拟与数学",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int h, f;\n    if (scanf(\"%d %d\", &h, &f) != 2) return 0;\n    for (int c = 0; c <= h; c++) {               // 枚举鸡的只数\n        int r = h - c;\n        if (2 * c + 4 * r == f) { printf(\"%d %d\\n\", c, r); return 0; }\n    }\n    printf(\"-1\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {                                     // 直接解方程\n    int h, f;\n    if (scanf(\"%d %d\", &h, &f) != 2) return 0;\n    int t = f - 2 * h;\n    if (t < 0 || t % 2 != 0) { printf(\"-1\\n\"); return 0; }\n    int r = t / 2, c = h - r;\n    if (c < 0 || r < 0) { printf(\"-1\\n\"); return 0; }\n    printf(\"%d %d\\n\", c, r);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "35 94\n",
                "expected_stdout": "23 12\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 2\n",
                "expected_stdout": "1 0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 3\n",
                "expected_stdout": "-1\n",
                "is_sample": 0,
                "kind": "manual",
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
                "stdin": "10 20\n",
                "expected_stdout": "10 0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10 40\n",
                "expected_stdout": "0 10\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【模拟】括号匹配判断",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "模拟",
            "栈",
            "括号匹配"
        ],
        "statement_md": "给定一个只含 `()`、`[]`、`{}` 的字符串，判断括号是否**正确配对**（既不能多、不能少，也不能交叉）。正确输出 `YES`，否则 `NO`。\n\n**关键点**\n\n- 遇到左括号就压栈，遇到右括号就弹栈并检查类型是否对上\n- 右括号来时栈已经空了 = 多了右括号，遍历完栈非空 = 多了左括号，这两种都算 NO\n- `([)]` 这种交叉嵌套必须判 NO —— 只数个数是查不出来的",
        "input_format": "一行，一个括号串（长度 1 到 20）。",
        "output_format": "一行：`YES` 或 `NO`。",
        "constraints_md": "- 1 ≤ 串长 ≤ 20",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 综合模拟与数学",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <cstring>\nint main() {\n    char s[40];\n    if (scanf(\"%39s\", s) != 1) return 0;\n    char st[40];\n    int top = 0;\n    for (int i = 0; s[i]; i++) {\n        char ch = s[i];\n        if (ch == '(' || ch == '[' || ch == '{') st[top++] = ch;\n        else {\n            char want = (ch == ')') ? '(' : (ch == ']' ? '[' : '{');\n            if (top == 0 || st[top - 1] != want) { printf(\"NO\\n\"); return 0; }\n            top--;\n        }\n    }\n    printf(\"%s\\n\", top == 0 ? \"YES\" : \"NO\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cstring>\nchar s[40];\nint main() {                                     // 反复消除成对的括号\n    if (scanf(\"%39s\", s) != 1) return 0;\n    int changed = 1;\n    while (changed) {\n        changed = 0;\n        int n = (int)strlen(s), k = 0;\n        char t[40];\n        for (int i = 0; i < n; i++) {\n            if (i + 1 < n) {\n                char a = s[i], b = s[i + 1];\n                if ((a == '(' && b == ')') || (a == '[' && b == ']') || (a == '{' && b == '}')) {\n                    i++;                             // 整对删掉\n                    changed = 1;\n                    continue;\n                }\n            }\n            t[k++] = s[i];\n        }\n        t[k] = 0;\n        strcpy(s, t);\n    }\n    printf(\"%s\\n\", s[0] == 0 ? \"YES\" : \"NO\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "()\n",
                "expected_stdout": "YES\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "([)]\n",
                "expected_stdout": "NO\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "((\n",
                "expected_stdout": "NO\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "{[()]}\n",
                "expected_stdout": "YES\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "]\n",
                "expected_stdout": "NO\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "()[]{}\n",
                "expected_stdout": "YES\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【数学】多个数的最大公约数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "数学",
            "gcd",
            "结合律"
        ],
        "statement_md": "给定 `n` 个正整数，求它们的最大公约数。\n\n**关键点**\n\n- `gcd` 满足结合律：一路 `d = gcd(d, a[i])` 下来就是全体的 gcd\n- `d` 的初值取 0 是安全的 —— `gcd(0, x) = x`\n- 输出一个整数",
        "input_format": "第一行 `n`；第二行 `n` 个正整数。",
        "output_format": "一行：这 `n` 个数的最大公约数。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 1 ≤ a[i] ≤ 1000",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 综合模拟与数学",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    long long d = 0;\n    for (int i = 0; i < n; i++) {\n        long long x;\n        scanf(\"%lld\", &x);\n        long long a = d, b = x;\n        while (b) { long long t = a % b; a = b; b = t; }\n        d = a;\n    }\n    printf(\"%lld\\n\", d);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {                                     // 更相减损逐个合并\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    long long d = 0;\n    for (int i = 0; i < n; i++) {\n        long long x;\n        scanf(\"%lld\", &x);\n        long long a = d, b = x;\n        if (a == 0) { d = b; continue; }\n        while (a != b) {\n            if (a > b) a -= b;\n            else b -= a;\n        }\n        d = a;\n    }\n    printf(\"%lld\\n\", d);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "2\n12 18\n",
                "expected_stdout": "6\n",
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
                "stdin": "3\n8 12 16\n",
                "expected_stdout": "4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n5 10 15 20\n",
                "expected_stdout": "5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n9 28\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n100 100 100\n",
                "expected_stdout": "100\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    }
]
