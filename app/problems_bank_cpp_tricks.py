# -*- coding: utf-8 -*-
"""C++ 技巧特训题库（subject=cpp，分节「技巧特训 · C++」）—— 自动生成，**不要手改本文件**。

生成器：tools/gen_cpp_tricks.py
共 20 题：难度 1~4 各 5 题，STL 惯用法与竞赛微套路。

重生成：python tools/gen_cpp_tricks.py
校验：  python tools/verify_bank.py --cpp
"""

CPP_TRICKS_PROBLEMS: list[dict] = [
    {
        "title": "count_if 三问：奇数·三的倍数·大于均值",
        "subject": "cpp",
        "line": "cpp",
        "question_type": "programming",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "技巧特训",
            "STL",
            "count_if",
            "lambda",
            "accumulate"
        ],
        "statement_md": "给定 `n` 个**非负**整数，按三个口径各数一次：\n\n1. `odd=` 奇数个数\n2. `mult3=` 3 的倍数个数（**0 也算 3 的倍数**）\n3. `above=` **严格大于平均值**的个数；平均值 = 总和整除 `n`（向下取整）\n\n这一档要练的是「一个 `accumulate` + 三次 `count_if`」这组最常见的组合拳：\n\n```cpp\nlong long total = accumulate(a.begin(), a.end(), 0LL);\nint avg = int(total / n);\nint odd = count_if(a.begin(), a.end(), [](int x) { return x % 2 == 1; });\nint m3  = count_if(a.begin(), a.end(), [](int x) { return x % 3 == 0; });\nint up  = count_if(a.begin(), a.end(), [avg](int x) { return x > avg; });\n```\n\n⚠️ 三个坑：\n1. **`accumulate` 的初值写 `0` 得到的是 `int` 累加**，`n` 大、值大时会溢出；写 `0LL` 才是 `long long`。\n2. `count_if` 的谓词**调用顺序不保证**，别在里面改外部变量。\n3. 平均值要**先累加再除**，别边加边除 —— 整数除法会一路丢精度。",
        "input_format": "第一行 `n`；第二行 `n` 个非负整数。",
        "output_format": "三行：`odd=<奇数个数>` / `mult3=<3 的倍数个数>` / `above=<大于均值的个数>`。",
        "constraints_md": "- 1 ≤ n ≤ 100000\n- 0 ≤ a[i] ≤ 10⁶\n- 总和最大 10¹¹，必须用 64 位累加",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · C++",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <vector>\n#include <numeric>\n#include <algorithm>\nusing namespace std;\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    vector<int> a(n);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n\n    long long total = accumulate(a.begin(), a.end(), 0LL);   // ★ 0LL 才有 64 位\n    int avg = int(total / n);\n\n    int odd = count_if(a.begin(), a.end(), [](int x) { return x % 2 == 1; });\n    int m3  = count_if(a.begin(), a.end(), [](int x) { return x % 3 == 0; });\n    int up  = count_if(a.begin(), a.end(), [avg](int x) { return x > avg; });\n\n    printf(\"odd=%d\\nmult3=%d\\nabove=%d\\n\", odd, m3, up);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nusing namespace std;\n\n// 独立实现：完全不碰 <algorithm>/<numeric>，一个 for 扫一遍，\n// 顺便验证「STL 那三个谓词」与手写判断的结果必须一模一样。\nint a[100005];\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    long long total = 0;\n    for (int i = 0; i < n; i++) {\n        scanf(\"%d\", &a[i]);\n        total += a[i];\n    }\n    int avg = int(total / n);\n    int odd = 0, m3 = 0, up = 0;\n    for (int i = 0; i < n; i++) {\n        if (a[i] % 2 == 1) odd++;\n        if (a[i] % 3 == 0) m3++;\n        if (a[i] > avg) up++;\n    }\n    printf(\"odd=%d\\nmult3=%d\\nabove=%d\\n\", odd, m3, up);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n1 2 3 4 5\n",
                "expected_stdout": "odd=3\nmult3=1\nabove=2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "6\n0 3 6 9 12 15\n",
                "expected_stdout": "odd=3\nmult3=6\nabove=3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n7\n",
                "expected_stdout": "odd=1\nmult3=0\nabove=0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8\n1000000 999999 0 0 3 4 5 6\n",
                "expected_stdout": "odd=3\nmult3=5\nabove=2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n0 0 0 0\n",
                "expected_stdout": "odd=0\nmult3=4\nabove=0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n10 20 30 40 50 60 70 80 90 100\n",
                "expected_stdout": "odd=0\nmult3=3\nabove=5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "lower_bound 与 upper_bound 的差就是区间个数",
        "subject": "cpp",
        "line": "cpp",
        "question_type": "programming",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "技巧特训",
            "STL",
            "lower_bound",
            "upper_bound",
            "二分"
        ],
        "statement_md": "给定 `n` 个整数（可负）和 `q` 次查询，每次查询给出闭区间 `[lo, hi]`，求**有多少个元素落在这个区间里**。\n\n排序一次 `O(n log n)`，之后每次查询 `O(log n)` —— 全部靠这一行：\n\n```cpp\nint L = lower_bound(v.begin(), v.end(), lo) - v.begin();  // 第一个 >= lo\nint R = upper_bound(v.begin(), v.end(), hi) - v.begin();  // 第一个 >  hi\nprintf(\"%d\\n\", R - L);\n```\n\n★ 为什么是「差」：`lower_bound` 落在**区间左端**，`upper_bound` 落在**区间右端的后一个位置**，两者下标相减恰好是夹在中间的个数 —— 空区间时两者相等，差为 0，不需要特判。\n\n⚠️ 常见错法：`upper_bound(hi) - lower_bound(lo) + 1`（多加了个 1）；或者拿 `lower_bound` 当「存在性判断」用 `!= end()` —— 那只说明**有元素 ≥ 它**，不是等于它。",
        "input_format": "第一行 `n`；第二行 `n` 个整数；第三行 `q`；接下来 `q` 行每行 `lo hi`。",
        "output_format": "`q` 行，每行一个整数：落在 `[lo, hi]` 内的元素个数。",
        "constraints_md": "- 1 ≤ n, q ≤ 2000\n- |a[i]|, |lo|, |hi| ≤ 10⁹\n- lo ≤ hi（不必额外判断）",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · C++",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <vector>\n#include <algorithm>\nusing namespace std;\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    vector<int> v(n);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &v[i]);\n    sort(v.begin(), v.end());\n\n    int q;\n    if (scanf(\"%d\", &q) != 1) return 0;\n    while (q--) {\n        int lo, hi;\n        scanf(\"%d %d\", &lo, &hi);\n        int L = int(lower_bound(v.begin(), v.end(), lo) - v.begin());\n        int R = int(upper_bound(v.begin(), v.end(), hi) - v.begin());\n        printf(\"%d\\n\", R - L);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <vector>\nusing namespace std;\n\n// 独立实现：手写两趟二分（lower / upper 的标准写法），不调用 <algorithm>。\n// 边界写错（`<` 与 `<=`）是这里唯一的坑，两趟必须一个用一个不用。\nint lb(const vector<int>& v, int x) {\n    int l = 0, r = int(v.size());\n    while (l < r) {\n        int m = l + (r - l) / 2;\n        if (v[m] < x) l = m + 1; else r = m;\n    }\n    return l;\n}\n\nint ub(const vector<int>& v, int x) {\n    int l = 0, r = int(v.size());\n    while (l < r) {\n        int m = l + (r - l) / 2;\n        if (v[m] <= x) l = m + 1; else r = m;\n    }\n    return l;\n}\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    vector<int> v(n);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &v[i]);\n\n    // 手写插入排序，彻底不用 std::sort\n    for (int i = 1; i < n; i++) {\n        int key = v[i], j = i - 1;\n        while (j >= 0 && v[j] > key) { v[j + 1] = v[j]; j--; }\n        v[j + 1] = key;\n    }\n\n    int q;\n    if (scanf(\"%d\", &q) != 1) return 0;\n    while (q--) {\n        int lo, hi;\n        scanf(\"%d %d\", &lo, &hi);\n        printf(\"%d\\n\", ub(v, hi) - lb(v, lo));\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "6\n1 3 3 5 7 9\n3\n1 3\n3 3\n4 8\n",
                "expected_stdout": "3\n2\n2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n-5 -1 0 2 10\n4\n-10 0\n0 0\n1 9\n-5 10\n",
                "expected_stdout": "3\n1\n1\n5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n42\n3\n42 42\n41 41\n0 100\n",
                "expected_stdout": "1\n0\n1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7\n7 7 7 7 7 7 7\n2\n7 7\n8 9\n",
                "expected_stdout": "7\n0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "9\n-3 -2 -1 0 1 2 3 4 5\n5\n-1 1\n-3 5\n2 4\n-2 -2\n0 0\n",
                "expected_stdout": "3\n9\n3\n1\n1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n1000000000 -1000000000 0 500000000\n3\n-1000000000 0\n1 999999999\n-1000000000 1000000000\n",
                "expected_stdout": "2\n1\n4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "rotate 一次搞定左旋，等价于三次 reverse",
        "subject": "cpp",
        "line": "cpp",
        "question_type": "programming",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "技巧特训",
            "STL",
            "rotate",
            "reverse",
            "迭代器区间"
        ],
        "statement_md": "把长度为 `n` 的序列**左旋** `k` 位（前面的挪到后面），输出旋转后的整个序列和第一个元素。\n\n`std::rotate` 一行就够，且它是**原地**的：\n\n```cpp\nk %= n;                                        // ★ k 可能大于 n\nrotate(v.begin(), v.begin() + k, v.end());     // 中点是「新的开头」\n```\n\n★ `rotate(first, middle, last)` 的语义是「把 `[middle, last)` 转到前面」，所以左旋 `k` 位就是让 `middle = first + k`。\n\n同一个效果还有经典的三次 `reverse` 写法（竞赛里常用来手写，不用记 `rotate` 的参数顺序）：\n\n```cpp\nreverse(v.begin(), v.begin() + k);   // 前段反转\nreverse(v.begin() + k, v.end());     // 后段反转\nreverse(v.begin(), v.end());         // 整体反转\n```\n\n⚠️ 两个坑：\n1. **先 `k %= n`**。`k == n` 时 `middle == last`，`rotate` 合法但白跑；`k > n` 且不取模时 `v.begin() + k` 直接越界（UB，`-O2` 下可能不报错但结果乱）。\n2. 三次 reverse 的**顺序**别乱：先两段各反、再整体反。反过来（先整体）得到的不是左旋。",
        "input_format": "第一行 `n k`；第二行 `n` 个整数。",
        "output_format": "两行：`after=<旋转后序列，空格分隔>` / `first=<旋转后第一个元素>`。",
        "constraints_md": "- 1 ≤ n ≤ 100000\n- 0 ≤ k ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · C++",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <vector>\n#include <algorithm>\nusing namespace std;\n\nint main() {\n    int n, k;\n    if (scanf(\"%d %d\", &n, &k) != 2) return 0;\n    vector<int> v(n);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &v[i]);\n\n    k %= n;                                          // ★ 不取模就可能越界\n    rotate(v.begin(), v.begin() + k, v.end());\n\n    printf(\"after=\");\n    for (int i = 0; i < n; i++) printf(i ? \" %d\" : \"%d\", v[i]);\n    printf(\"\\nfirst=%d\\n\", v[0]);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <vector>\n#include <algorithm>\nusing namespace std;\n\n// 独立实现：三次 reverse，不用 rotate。\nint main() {\n    int n, k;\n    if (scanf(\"%d %d\", &n, &k) != 2) return 0;\n    vector<int> v(n);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &v[i]);\n\n    k %= n;\n    reverse(v.begin(), v.begin() + k);   // 前段\n    reverse(v.begin() + k, v.end());     // 后段\n    reverse(v.begin(), v.end());         // 整体\n\n    printf(\"after=\");\n    for (int i = 0; i < n; i++) printf(i ? \" %d\" : \"%d\", v[i]);\n    printf(\"\\nfirst=%d\\n\", v[0]);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 2\n10 20 30 40 50\n",
                "expected_stdout": "after=30 40 50 10 20\nfirst=30\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5 0\n1 2 3 4 5\n",
                "expected_stdout": "after=1 2 3 4 5\nfirst=1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4 3\n9 8 7 6\n",
                "expected_stdout": "after=6 9 8 7\nfirst=6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3 3\n1 2 3\n",
                "expected_stdout": "after=1 2 3\nfirst=1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1 1000000000\n7\n",
                "expected_stdout": "after=7\nfirst=7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6 4\n-1 -2 -3 -4 -5 -6\n",
                "expected_stdout": "after=-5 -6 -1 -2 -3 -4\nfirst=-5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "accumulate 初值写 0LL，否则大数求和会溢出",
        "subject": "cpp",
        "line": "cpp",
        "question_type": "programming",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "技巧特训",
            "STL",
            "accumulate",
            "溢出",
            "long long"
        ],
        "statement_md": "给定 `n` 个非负整数（每个可达 10⁹），输出它们的总和与平均值（总和整除 `n`）。\n\n这题的正确写法只有一行，但**写错的人很多**：\n\n```cpp\nlong long sum = accumulate(v.begin(), v.end(), 0LL);   // ✅\nint  bad      = accumulate(v.begin(), v.end(), 0);     // ❌ int 累加，溢出\n```\n\n★ 关键在于 `accumulate` 的**返回值类型由初值决定**：它会以初值的类型做累加，中间结果也是那个类型。初值写 `0` 就是 `int` 一路加过去 —— `n = 3`、每个元素都是 10⁹ 时总和 3×10⁹ 已经超出 `int` 上限（2147483647），结果变成负数或乱值，**且编译器不会有任何警告**。\n\n等价写法（同样正确，读起来更直白）：\n\n```cpp\nlong long sum = 0;\nfor (int x : v) sum += x;    // sum 是 long long，每次累加都在 64 位里做\n```\n\n⚠️ 另一个坑：`sum / n` 里 `n` 是 `int`，`long long / int` 结果仍是 `long long`，所以先算再窄化没问题；但如果你写 `int avg = sum / n` 而总和真的超过 2³¹，那**除完再窄化**也会截断 —— 本题保证平均值不超过 10⁹，所以这里安全。",
        "input_format": "第一行 `n`；第二行 `n` 个非负整数。",
        "output_format": "两行：`sum=<总和>` / `avg=<总和整除 n>`。",
        "constraints_md": "- 1 ≤ n ≤ 100000\n- 0 ≤ a[i] ≤ 10⁹\n- 总和可能到 10¹⁴，必须 64 位",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · C++",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <vector>\n#include <numeric>\nusing namespace std;\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    vector<int> v(n);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &v[i]);\n\n    long long sum = accumulate(v.begin(), v.end(), 0LL);   // ★ 初值决定累加类型\n    printf(\"sum=%lld\\navg=%lld\\n\", sum, sum / n);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <vector>\nusing namespace std;\n\n// 独立实现：range-for 手动累加，不用 accumulate —— 用来证明「初值类型」这件事\n// 只要累加变量声明成 long long 就等价。\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    vector<int> v(n);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &v[i]);\n\n    long long sum = 0;\n    for (auto x : v) sum += x;\n    printf(\"sum=%lld\\navg=%lld\\n\", sum, sum / n);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4\n1000000000 1000000000 1000000000 1000000000\n",
                "expected_stdout": "sum=4000000000\navg=1000000000\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n1 2 3\n",
                "expected_stdout": "sum=6\navg=2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n1000000000\n",
                "expected_stdout": "sum=1000000000\navg=1000000000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n2147483647 1 0 0 0\n",
                "expected_stdout": "sum=2147483648\navg=429496729\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n1000000000 999999999\n",
                "expected_stdout": "sum=1999999999\navg=999999999\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8\n1 1 1 1 1 1 1 1000000000\n",
                "expected_stdout": "sum=1000000007\navg=125000000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "string::find 循环切分逗号串再 stoi",
        "subject": "cpp",
        "line": "cpp",
        "question_type": "programming",
        "difficulty": 1,
        "total_score": 12,
        "tags": [
            "技巧特训",
            "STL",
            "string",
            "find",
            "substr",
            "stoi"
        ],
        "statement_md": "读入**一行**逗号分隔的整数（可能带负号），输出段数、总和、最大值、最小值。\n\n`std::string` 上「按单个字符切分」的标准套路是一个 `find` 循环：\n\n```cpp\nsize_t p = 0;\nwhile (true) {\n    size_t q = s.find(',', p);          // 找下一个分隔符\n    if (q == string::npos) q = s.size(); // 没有了就一直到尾\n    v.push_back(stoi(s.substr(p, q - p)));\n    if (q == s.size()) break;           // ★ 先判断再前移，否则会多切一个空段\n    p = q + 1;\n}\n```\n\n★ `find` 返回的是 `size_t`，找不到时是 `string::npos`（一个极大值）。所以**不能**拿它当循环条件写成 `while (s.find(',', p) != npos)`，那样末段永远进不去。\n\n⚠️ 两个坑：\n1. **收尾顺序**。上例里 `if (q == s.size()) break;` 必须放在 `p = q + 1` 之前；顺序反了 `p` 会变成 `size()+1`，`substr` 抛 `out_of_range`。\n2. `stoi` 遇到不认识的字符会抛 `invalid_argument`，遇到超 `int` 范围抛 `out_of_range`，本题保证输入合法；但真实场景里它**不像 `atoi` 那样静默返回 0** —— 这既是好事也是坑。",
        "input_format": "一行：若干个整数，之间用**一个**逗号分隔（无空格、无空段）。",
        "output_format": "四行：`count=<段数>` / `sum=<总和>` / `max=<最大值>` / `min=<最小值>`。",
        "constraints_md": "- 1 ≤ 段数 ≤ 1000\n- |每个整数| ≤ 10⁹\n- 总和可能超 `int` 上限",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · C++",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <iostream>\n#include <string>\n#include <vector>\n#include <climits>\nusing namespace std;\n\nint main() {\n    string s;\n    if (!getline(cin, s)) return 0;\n\n    vector<int> v;\n    size_t p = 0;\n    while (true) {\n        size_t q = s.find(',', p);\n        if (q == string::npos) q = s.size();\n        v.push_back(stoi(s.substr(p, q - p)));\n        if (q == s.size()) break;      // ★ 必须在 p = q + 1 之前\n        p = q + 1;\n    }\n\n    long long sum = 0;\n    int mx = INT_MIN, mn = INT_MAX;\n    for (int x : v) { sum += x; if (x > mx) mx = x; if (x < mn) mn = x; }\n    printf(\"count=%zu\\nsum=%lld\\nmax=%d\\nmin=%d\\n\", v.size(), sum, mx, mn);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <iostream>\n#include <string>\n#include <vector>\n#include <climits>\nusing namespace std;\n\n// 独立实现：不用 find/substr/stoi，逐字符手写解析（顺便处理负号）。\n// 这是竞赛里读「一行非空格分隔」数据最稳的写法 —— 不依赖任何库函数的异常行为。\nint main() {\n    string s;\n    if (!getline(cin, s)) return 0;\n\n    vector<int> v;\n    long long cur = 0;\n    bool neg = false, has = false;\n    for (size_t i = 0; i <= s.size(); i++) {\n        char c = (i < s.size() ? s[i] : ',');\n        if (c == ',') {\n            if (has) v.push_back(int(neg ? -cur : cur));\n            cur = 0; neg = false; has = false;\n        } else if (c == '-') {\n            neg = true;\n        } else {\n            cur = cur * 10 + (c - '0');\n            has = true;\n        }\n    }\n\n    long long sum = 0;\n    int mx = INT_MIN, mn = INT_MAX;\n    for (int x : v) { sum += x; if (x > mx) mx = x; if (x < mn) mn = x; }\n    printf(\"count=%zu\\nsum=%lld\\nmax=%d\\nmin=%d\\n\", v.size(), sum, mx, mn);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "-3,7,12,-5,0\n",
                "expected_stdout": "count=5\nsum=11\nmax=12\nmin=-5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "42\n",
                "expected_stdout": "count=1\nsum=42\nmax=42\nmin=42\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1,1,1\n",
                "expected_stdout": "count=3\nsum=3\nmax=1\nmin=1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "-1000000000,1000000000\n",
                "expected_stdout": "count=2\nsum=0\nmax=1000000000\nmin=-1000000000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5,-5,5,-5,5,-5\n",
                "expected_stdout": "count=6\nsum=0\nmax=5\nmin=-5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "0,0,0,0,0,0,0,0\n",
                "expected_stdout": "count=8\nsum=0\nmax=0\nmin=0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "stable_sort 保住同分者的入场顺序",
        "subject": "cpp",
        "line": "cpp",
        "question_type": "programming",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "技巧特训",
            "STL",
            "stable_sort",
            "排序稳定性"
        ],
        "statement_md": "按分数**从高到低**排序，**同分的人保持输入的先后顺序**（不打乱）。输出排序后的名单（每行 `姓名 分数`），最后再输出 `top=<排在第一的姓名>`。\n\n这一档的核心就一句话：**要稳定就 `stable_sort`，别用 `sort` 再想办法补救**。\n\n```cpp\nstable_sort(v.begin(), v.end(), [](const Rec& a, const Rec& b) {\n    return a.score > b.score;      // ★ 只写 >，绝对不写 >=\n});\n```\n\n★ `sort` 的底层是内省排序（快排 + 堆排 + 插入），**不保证**等价元素的相对次序；`stable_sort` 通常是归并，等价元素保持原次序。两者复杂度都是 `O(n log n)`，`stable_sort` 只是要多一块临时空间 —— 需要稳定时没有理由不用它。\n\n⚠️ 三个坑：\n1. 比较器写 `a.score >= b.score` 会**破坏严格弱序**（等价元素返回了 true），`std::sort` 在 `-O2` 下可能直接越界崩掉 —— 这是最经典的「本地没事、评测 RE」。\n2. 想让 `sort` 也稳定，可以**把输入下标当第二关键字**参与比较，但那要多存一个字段，不如直接 `stable_sort`。\n3. 输出第一名的姓名要用**排序后的 `v[0]`**，别用「扫描时记住的最大值」——同分时两者可能不是同一个人。",
        "input_format": "第一行 `n`；接下来 `n` 行，每行 `姓名 分数`（姓名不含空格）。",
        "output_format": "`n` 行名单（`姓名 分数`），最后一行 `top=<第一名姓名>`。",
        "constraints_md": "- 1 ≤ n ≤ 100000\n- 0 ≤ 分数 ≤ 1000（**大量同分**，所以要考稳定性）\n- 姓名只含字母，长度 ≤ 20",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · C++",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <string>\n#include <vector>\n#include <algorithm>\nusing namespace std;\n\nstruct Rec {\n    string name;\n    int score;\n};\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    vector<Rec> v(n);\n    for (int i = 0; i < n; i++) {\n        char buf[64];\n        if (scanf(\"%63s %d\", buf, &v[i].score) != 2) return 0;\n        v[i].name = buf;\n    }\n\n    stable_sort(v.begin(), v.end(), [](const Rec& a, const Rec& b) {\n        return a.score > b.score;          // ★ 严格大于，同分交给稳定性\n    });\n\n    for (const auto& r : v) printf(\"%s %d\\n\", r.name.c_str(), r.score);\n    printf(\"top=%s\\n\", v[0].name.c_str());\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <string>\n#include <vector>\nusing namespace std;\n\n// 独立实现：手写插入排序（天然稳定：只有严格小于才后移）。\n// 顺便证明「stable_sort 的结果 == 稳定排序的结果」，与 sort 的不确定次序不同。\nstruct Rec {\n    string name;\n    int score;\n};\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    vector<Rec> v(n);\n    for (int i = 0; i < n; i++) {\n        char buf[64];\n        if (scanf(\"%63s %d\", buf, &v[i].score) != 2) return 0;\n        v[i].name = buf;\n    }\n\n    for (int i = 1; i < n; i++) {\n        Rec key = v[i];\n        int j = i - 1;\n        while (j >= 0 && v[j].score < key.score) {   // 只挪严格更小的 → 稳定\n            v[j + 1] = v[j];\n            j--;\n        }\n        v[j + 1] = key;\n    }\n\n    for (const auto& r : v) printf(\"%s %d\\n\", r.name.c_str(), r.score);\n    printf(\"top=%s\\n\", v[0].name.c_str());\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\namy 90\nbob 95\ncid 90\ndan 95\neve 80\n",
                "expected_stdout": "bob 95\ndan 95\namy 90\ncid 90\neve 80\ntop=bob\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\nzoe 100\nmax 100\nli 100\n",
                "expected_stdout": "zoe 100\nmax 100\nli 100\ntop=zoe\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\nsolo 0\n",
                "expected_stdout": "solo 0\ntop=solo\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\na 60\nb 60\nc 70\nd 60\ne 70\nf 50\n",
                "expected_stdout": "c 70\ne 70\na 60\nb 60\nd 60\nf 50\ntop=c\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\np1 1\np2 2\np3 1\np4 2\n",
                "expected_stdout": "p2 2\np4 2\np1 1\np3 1\ntop=p2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8\naa 50\nbb 40\ncc 50\ndd 40\nee 50\nff 40\ngg 50\nhh 40\n",
                "expected_stdout": "aa 50\ncc 50\nee 50\ngg 50\nbb 40\ndd 40\nff 40\nhh 40\ntop=aa\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "比较器必须是严格弱序：绝对值降序再按值升序",
        "subject": "cpp",
        "line": "cpp",
        "question_type": "programming",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "技巧特训",
            "STL",
            "sort",
            "比较器",
            "严格弱序"
        ],
        "statement_md": "给定 `n` 个整数（可负），按下面的规则排序并输出：\n\n1. **绝对值大的在前**；\n2. 绝对值相同时，**数值小的在前**（所以 `-5` 排在 `5` 前面，`3` 排在 `-3` 后面）。\n\n两段式比较器是最干净的写法：\n\n```cpp\nsort(v.begin(), v.end(), [](int a, int b) {\n    int x = abs(a), y = abs(b);\n    if (x != y) return x > y;     // 第一关键字：|x| 降序\n    return a < b;                 // 第二关键字：值升序\n});\n```\n\n★ 「严格弱序」的四条要求里，实践上只要记住一条：**比较器对任意两个元素 `comp(a, a)` 必须返回 `false`，且不能出现 `>=` / `<=`**。写成 `if (x != y) return x > y; return a <= b;` 就违反了 —— 当 `a == b` 时它返回 `true`，排序算法会认为「a 必须排在 a 前面」，`-O2` 下的内省排序可能算出非法下标并越界。\n\n⚠️ 另一个常见错法：只写 `return abs(a) > abs(b);`（漏了第二关键字）。这时绝对值相同的元素次序**不确定**，而本题要求同绝对值按值升序，会稳定错样例。\n\n💡 想不写比较器也行：把键做成 pair，`pair` 自带字典序 —— `sort` 一个 `vector<pair<int,int>>` 存 `{-abs(x), x}`，升序排就是题目要的结果。",
        "input_format": "第一行 `n`；第二行 `n` 个整数（可负）。",
        "output_format": "一行：排序后的 `n` 个整数，空格分隔。",
        "constraints_md": "- 1 ≤ n ≤ 100000\n- |a[i]| ≤ 10⁶（不会碰到 `abs(INT_MIN)` 的 UB）",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · C++",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <vector>\n#include <algorithm>\n#include <cstdlib>\nusing namespace std;\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    vector<int> v(n);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &v[i]);\n\n    sort(v.begin(), v.end(), [](int a, int b) {\n        int x = abs(a), y = abs(b);\n        if (x != y) return x > y;    // 严格：只在不等时比\n        return a < b;                // 严格：相等时返回 false\n    });\n\n    for (int i = 0; i < n; i++) printf(i ? \" %d\" : \"%d\", v[i]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <vector>\n#include <algorithm>\n#include <cstdlib>\nusing namespace std;\n\n// 独立实现：两次 stable_sort 组合，完全不写「两段式 if」比较器。\n//   ① 先按值升序（稳定）\n//   ② 再按 |x| 降序（稳定）→ 同 |x| 的元素保住 ① 的值升序\n// 这是「多关键字排序」的另一个标准套路：从次要关键字往主要关键字，一路稳定排序。\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    vector<int> v(n);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &v[i]);\n\n    stable_sort(v.begin(), v.end());                              // 次要关键字\n    stable_sort(v.begin(), v.end(), [](int a, int b) {            // 主要关键字\n        return abs(a) > abs(b);\n    });\n\n    for (int i = 0; i < n; i++) printf(i ? \" %d\" : \"%d\", v[i]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n3 -5 5 -3 0\n",
                "expected_stdout": "-5 5 -3 3 0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n1 -1 1 -1\n",
                "expected_stdout": "-1 -1 1 1\n",
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
                "stdin": "6\n-10 10 -9 9 0 0\n",
                "expected_stdout": "-10 10 -9 9 0 0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7\n2 -100 100 -2 50 -50 7\n",
                "expected_stdout": "-100 100 -50 50 7 -2 2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n-1000000 1000000 -1 1 0\n",
                "expected_stdout": "-1000000 1000000 -1 1 0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "merge 把两段有序序列一次并起来",
        "subject": "cpp",
        "line": "cpp",
        "question_type": "programming",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "技巧特训",
            "STL",
            "merge",
            "back_inserter",
            "归并"
        ],
        "statement_md": "给定两段**已经升序**的序列（长度 `n`、`m`），把它们合并成一段仍升序的序列。输出合并结果，以及合并后的首元素与末元素。\n\n标准答案是 `std::merge`，注意它**不返回值、写到第三个区间**，所以要配 `back_inserter`：\n\n```cpp\nvector<int> c;\nc.reserve(n + m);                       // ★ 不 reserve 也行，但会多次扩容\nmerge(a.begin(), a.end(), b.begin(), b.end(), back_inserter(c));\n```\n\n★ 为什么不用 `sort(a+b)`：`merge` 是 `O(n+m)`，而重新排序是 `O((n+m)log(n+m))`。数据量大时差一倍以上 —— 「已经有序」这个前提本身就是资源，别浪费。\n\n⚠️ 三个坑：\n1. 忘记 `c.reserve()` 不会错，但会反复扩容；`back_inserter` 每次 `push_back`，配合 `reserve` 才是 `O(n+m)` 的常数。\n2. **输入必须真是有序的**。`merge` 不检查，乱序输入只会得到一段乱序结果，而且在 `-O2` 下不会有任何提示。\n3. `merge` 不会去重。要「并集且去重」得用 `set_union`（同样写两个区间 + 输出迭代器）。",
        "input_format": "第一行 `n m`；第二行 `n` 个升序整数；第三行 `m` 个升序整数。",
        "output_format": "三行：`merged=<合并后序列>` / `first=<首元素>` / `last=<末元素>`。",
        "constraints_md": "- 1 ≤ n, m ≤ 100000\n- 两段各自升序（不保证严格）\n- |元素| ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · C++",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <vector>\n#include <algorithm>\n#include <iterator>\nusing namespace std;\n\nint main() {\n    int n, m;\n    if (scanf(\"%d %d\", &n, &m) != 2) return 0;\n    vector<int> a(n), b(m);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    for (int i = 0; i < m; i++) scanf(\"%d\", &b[i]);\n\n    vector<int> c;\n    c.reserve(n + m);\n    merge(a.begin(), a.end(), b.begin(), b.end(), back_inserter(c));\n\n    printf(\"merged=\");\n    for (size_t i = 0; i < c.size(); i++) printf(i ? \" %d\" : \"%d\", c[i]);\n    printf(\"\\nfirst=%d\\nlast=%d\\n\", c.front(), c.back());\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <vector>\nusing namespace std;\n\n// 独立实现：双指针手工归并，不用 std::merge，也不用 back_inserter。\nint main() {\n    int n, m;\n    if (scanf(\"%d %d\", &n, &m) != 2) return 0;\n    vector<int> a(n), b(m);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    for (int i = 0; i < m; i++) scanf(\"%d\", &b[i]);\n\n    vector<int> c;\n    c.reserve(n + m);\n    int i = 0, j = 0;\n    while (i < n && j < m) {\n        if (a[i] <= b[j]) c.push_back(a[i++]);\n        else c.push_back(b[j++]);\n    }\n    while (i < n) c.push_back(a[i++]);\n    while (j < m) c.push_back(b[j++]);\n\n    printf(\"merged=\");\n    for (size_t k = 0; k < c.size(); k++) printf(k ? \" %d\" : \"%d\", c[k]);\n    printf(\"\\nfirst=%d\\nlast=%d\\n\", c.front(), c.back());\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3 3\n1 4 7\n2 3 9\n",
                "expected_stdout": "merged=1 2 3 4 7 9\nfirst=1\nlast=9\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 1\n5\n1\n",
                "expected_stdout": "merged=1 5\nfirst=1\nlast=5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4 2\n-10 -5 0 5\n-7 6\n",
                "expected_stdout": "merged=-10 -7 -5 0 5 6\nfirst=-10\nlast=6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3 3\n1 1 1\n1 1 1\n",
                "expected_stdout": "merged=1 1 1 1 1 1\nfirst=1\nlast=1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5 1\n1 2 3 4 5\n3\n",
                "expected_stdout": "merged=1 2 3 3 4 5\nfirst=1\nlast=5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2 5\n100 200\n1 2 3 4 5\n",
                "expected_stdout": "merged=1 2 3 4 5 100 200\nfirst=1\nlast=200\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "priority_queue 设 greater 做小顶堆：合并果子",
        "subject": "cpp",
        "line": "cpp",
        "question_type": "programming",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "技巧特训",
            "STL",
            "priority_queue",
            "greater",
            "堆",
            "贪心"
        ],
        "statement_md": "有 `n` 堆果子，每堆 `a[i]` 个。每次可以把**任意两堆**合并成一堆，这次合并的代价是两堆果子数之和。重复直到只剩一堆，求**总代价最小**是多少。\n\n策略很简单：**每次合并当前最小的两堆**（这样大的数被少算几次）。要反复取最小，用小顶堆：\n\n```cpp\npriority_queue<long long, vector<long long>, greater<long long>> pq;\n```\n\n★ `priority_queue` 默认是**大顶堆**，`greater<T>` 把它翻成小顶堆。三个模板参数一个都不能少：`<元素类型, 底层容器, 比较器>` —— 不能只写 `priority_queue<long long, greater<long long>>`。\n\n⚠️ 三个坑：\n1. **`greater<>` 在 C++11 之后才能不写类型**（`greater<long long>` 写成 `greater<>` 也行），老编译器上要写全。\n2. 用 `long long` 存：`n` 大、每堆大时总代价会超 `int`。\n3. `n == 1` 时**一次都不合并**，答案是 0（别把初始那堆算进代价）。\n\n💡 等价容器：`multiset<long long>` 取 `begin()` 也算小顶堆语义，但每轮要 `erase` 两次再 `insert`，常数比 `priority_queue` 大。",
        "input_format": "第一行 `n`；第二行 `n` 个正整数，表示每堆的果子数。",
        "output_format": "一行：`cost=<最小总代价>`。",
        "constraints_md": "- 1 ≤ n ≤ 100000\n- 1 ≤ a[i] ≤ 10⁴\n- 总代价可能到 10⁹ 以上，用 64 位",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · C++",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <queue>\n#include <vector>\n#include <functional>\nusing namespace std;\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n\n    // ★ 小顶堆：<类型, 底层容器, 比较器> 三个参数都要写\n    priority_queue<long long, vector<long long>, greater<long long>> pq;\n    for (int i = 0; i < n; i++) {\n        long long x;\n        scanf(\"%lld\", &x);\n        pq.push(x);\n    }\n\n    long long cost = 0;\n    while (pq.size() > 1) {\n        long long x = pq.top(); pq.pop();\n        long long y = pq.top(); pq.pop();\n        cost += x + y;\n        pq.push(x + y);\n    }\n    printf(\"cost=%lld\\n\", cost);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <set>\nusing namespace std;\n\n// 独立实现：multiset 当有序可重集，每轮取最小的两个（begin()），\n// 不依赖 priority_queue 的模板参数写法。\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n\n    multiset<long long> s;\n    for (int i = 0; i < n; i++) {\n        long long x;\n        scanf(\"%lld\", &x);\n        s.insert(x);\n    }\n\n    long long cost = 0;\n    while (s.size() > 1) {\n        auto it = s.begin();\n        long long x = *it;\n        s.erase(it);\n        it = s.begin();\n        long long y = *it;\n        s.erase(it);\n        cost += x + y;\n        s.insert(x + y);\n    }\n    printf(\"cost=%lld\\n\", cost);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 2 9\n",
                "expected_stdout": "cost=15\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n5\n",
                "expected_stdout": "cost=0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n1 1 1 1\n",
                "expected_stdout": "cost=8\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n10000 10000\n",
                "expected_stdout": "cost=20000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n10 20 30 40 50\n",
                "expected_stdout": "cost=330\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n1 2 3 4 5 6\n",
                "expected_stdout": "cost=51\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "stable_partition 偶数前移且不打乱相对序",
        "subject": "cpp",
        "line": "cpp",
        "question_type": "programming",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "技巧特训",
            "STL",
            "stable_partition",
            "partition",
            "谓词"
        ],
        "statement_md": "把序列里**所有偶数挪到前面、奇数留在后面**，并且**两部分各自保持原来的先后顺序**。输出重排后的序列，再输出偶数的个数。\n\n`stable_partition` 的返回值就是分界点，用它数个数最省事：\n\n```cpp\nauto mid = stable_partition(v.begin(), v.end(), [](int x) { return x % 2 == 0; });\nlong long even = mid - v.begin();     // 满足谓词的元素个数\n```\n\n★ 为什么不能用 `partition`：`partition` 只保证「满足谓词的都在前面」，**不保证**内部次序 —— 它用交换实现，`O(n)` 但会打乱。`stable_partition` 通常要额外空间，复杂度 `O(n log n)`（空间不够时）或 `O(n)`（够时）。\n\n⚠️ 三个坑：\n1. 谓词返回 `true` 的元素**去前面**，别把条件写反（写成 `x % 2 != 0` 就成了奇数在前）。\n2. 负数的取模：`-3 % 2` 在 C++ 里是 `-1`（不是 0），所以「`!= 0` 即奇数」对负数同样成立；但如果写成 `x % 2 == 1` 就**漏掉所有负奇数** —— 这是本题最大的陷阱。\n3. 用返回值减 `begin()` 得到个数，比再跑一遍 `count_if` 更省，也更不容易写错。",
        "input_format": "第一行 `n`；第二行 `n` 个整数（可负）。",
        "output_format": "两行：重排后的序列（空格分隔）/ `even=<偶数个数>`。",
        "constraints_md": "- 1 ≤ n ≤ 100000\n- |a[i]| ≤ 10⁹\n- **含负奇数**，注意 `%` 的符号",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · C++",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <vector>\n#include <algorithm>\nusing namespace std;\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    vector<int> v(n);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &v[i]);\n\n    // ★ 谓词用 != 0，负数也判得对\n    auto mid = stable_partition(v.begin(), v.end(), [](int x) { return x % 2 == 0; });\n    long long even = mid - v.begin();\n\n    for (int i = 0; i < n; i++) printf(i ? \" %d\" : \"%d\", v[i]);\n    printf(\"\\neven=%lld\\n\", even);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <vector>\nusing namespace std;\n\n// 独立实现：两个桶分别收集再拼回去，不用任何 partition。\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    vector<int> ev, od;\n    for (int i = 0; i < n; i++) {\n        int x;\n        scanf(\"%d\", &x);\n        if (x % 2 != 0) od.push_back(x);\n        else ev.push_back(x);\n    }\n\n    vector<int> v;\n    v.reserve(n);\n    for (int x : ev) v.push_back(x);\n    for (int x : od) v.push_back(x);\n\n    for (int i = 0; i < n; i++) printf(i ? \" %d\" : \"%d\", v[i]);\n    printf(\"\\neven=%d\\n\", int(ev.size()));\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "6\n1 2 3 4 5 6\n",
                "expected_stdout": "2 4 6 1 3 5\neven=3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n-3 -2 -1 0 1\n",
                "expected_stdout": "-2 0 -3 -1 1\neven=2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n1 3 5 7\n",
                "expected_stdout": "1 3 5 7\neven=0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n2 4 6\n",
                "expected_stdout": "2 4 6\neven=3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7\n0 -1 2 -3 4 -5 6\n",
                "expected_stdout": "0 2 4 6 -1 -3 -5\neven=4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n-7 -6 -5 -4 -3\n",
                "expected_stdout": "-6 -4 -7 -5 -3\neven=2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "set::insert 的 bool 返回值直接数出重复",
        "subject": "cpp",
        "line": "cpp",
        "question_type": "programming",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "技巧特训",
            "STL",
            "set",
            "insert",
            "去重"
        ],
        "statement_md": "给定 `n` 个整数（可负），输出三行：\n\n- `unique=` 不同值的个数\n- `dup=` **多出来的重复次数**（总个数 − 不同值个数）\n- `second=` 第二小的不同值；不足两个不同值时输出 `none`\n\n`set::insert` 有一个很多人不知道的返回值：`pair<iterator, bool>`，`bool` 表示**这次插入是否真的插进去了**（元素已存在就是 `false`）。于是计数不用 `find` 再 `insert` 两趟：\n\n```cpp\nset<int> s;\nint dup = 0;\nfor (int x : a) {\n    if (!s.insert(x).second) dup++;   // 插不进去 = 之前就有了\n}\n```\n\nC++17 之后还能直接解构：`auto [it, ok] = s.insert(x);`\n\n★ `set` 的迭代器是**中序**的，所以 `s.begin()` 是最小值，`next(s.begin())` 是第二小 —— 不需要排序，本身就维护了有序性。\n\n⚠️ 三个坑：\n1. `s.insert(x).second` 的 `second` **不能省**，光看返回值是 `pair`，`if (s.insert(x))` 编不过。\n2. 取第二小之前必须判 `s.size() >= 2`；`next(s.begin())` 在只有 1 个元素时是 `end()`，解引用它是 UB（`-O2` 下读到垃圾值，不崩但答案错）。\n3. `set` 是 `O(log n)` 插入 + 每个元素一次内存分配，比「`sort` + `unique`」慢且更吃内存；只要能先收完再排序，`vector` 往往更快。",
        "input_format": "第一行 `n`；第二行 `n` 个整数（可负）。",
        "output_format": "三行：`unique=<不同值个数>` / `dup=<重复次数>` / `second=<第二小不同值或 none>`。",
        "constraints_md": "- 1 ≤ n ≤ 100000\n- |a[i]| ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · C++",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <set>\n#include <iterator>\nusing namespace std;\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n\n    set<int> s;\n    int dup = 0;\n    for (int i = 0; i < n; i++) {\n        int x;\n        scanf(\"%d\", &x);\n        if (!s.insert(x).second) dup++;      // ★ 插不进去说明早有\n    }\n\n    if (s.size() >= 2) {\n        auto it = s.begin();\n        ++it;                                // 第二小\n        printf(\"unique=%zu\\ndup=%d\\nsecond=%d\\n\", s.size(), dup, *it);\n    } else {\n        printf(\"unique=%zu\\ndup=%d\\nsecond=none\\n\", s.size(), dup);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <vector>\n#include <algorithm>\nusing namespace std;\n\n// 独立实现：先 sort，再用 unique 的手工版（自己数不同值），完全不用 set。\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    vector<int> a(n);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    sort(a.begin(), a.end());\n\n    int uniq = 0;\n    for (int i = 0; i < n; i++) {\n        if (i == 0 || a[i] != a[i - 1]) uniq++;\n    }\n    int dup = n - uniq;\n\n    // 第二小的不同值：扫描到第二个「与前一个不等」的位置\n    int seen = 0, second = 0;\n    bool has_second = false;\n    for (int i = 0; i < n; i++) {\n        if (i == 0 || a[i] != a[i - 1]) {\n            seen++;\n            if (seen == 2) { second = a[i]; has_second = true; break; }\n        }\n    }\n\n    printf(\"unique=%d\\ndup=%d\\n\", uniq, dup);\n    if (has_second) printf(\"second=%d\\n\", second);\n    else printf(\"second=none\\n\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "6\n5 3 5 7 3 3\n",
                "expected_stdout": "unique=3\ndup=3\nsecond=5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n1 1 1 1\n",
                "expected_stdout": "unique=1\ndup=3\nsecond=none\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n42\n",
                "expected_stdout": "unique=1\ndup=0\nsecond=none\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n-10 -10 0 10 10\n",
                "expected_stdout": "unique=3\ndup=2\nsecond=0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n1000000000 999999999 1000000000\n",
                "expected_stdout": "unique=2\ndup=1\nsecond=1000000000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7\n9 8 7 6 5 4 3\n",
                "expected_stdout": "unique=7\ndup=0\nsecond=4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "map::emplace 不覆盖：同一人的成绩以首次为准",
        "subject": "cpp",
        "line": "cpp",
        "question_type": "programming",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "技巧特训",
            "STL",
            "map",
            "emplace",
            "operator[]"
        ],
        "statement_md": "输入 `n` 条成绩记录（同一个人可能出现多次），**每人只保留第一次出现的成绩**，最后按姓名字典序输出 `姓名 分数`，再输出人数。\n\n`emplace` 和 `operator[]` 的差别就在这一行：\n\n```cpp\nm.emplace(name, score);   // ✅ 已存在就什么都不做（保留首次）\nm[name] = score;          // ❌ 直接覆盖成最后一次\nm.insert({name, score});  // ✅ 同 emplace，但要多构造一次临时 pair\n```\n\n★ `map::emplace` 用的是「**构造即插入、失败即丢弃**」：键已存在时连值都不会构造（C++17 起保证），所以它同时是「不覆盖」和「少一次构造」两个优化。\n\n⚠️ 三个坑：\n1. **`operator[]` 会先默认构造再赋值**。对 `map<string,int>` 只是多写一个 0；对没有默认构造函数的 value 类型直接编译不过。而且它还有一个更隐蔽的副作用 —— **查询也会插入**：`if (m[\"nothere\"] == 0)` 会把键插进去。\n2. 想「保留最大」而不是「保留首次」，得 `m[name] = max(m[name], score)`，但这样 `operator[]` 的插入副作用就变成有用的了 —— 场景不同，选法不同。\n3. `map` 已按 key 有序，输出**不需要再排序**；`unordered_map` 就没有这个便利，必须自己排。",
        "input_format": "第一行 `n`；接下来 `n` 行，每行 `姓名 分数`。",
        "output_format": "若干行 `姓名 分数`（按姓名字典序），最后一行 `count=<人数>`。",
        "constraints_md": "- 1 ≤ n ≤ 100000\n- 姓名只含小写字母，长度 ≤ 10\n- 0 ≤ 分数 ≤ 1000",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · C++",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <string>\n#include <map>\nusing namespace std;\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n\n    map<string, int> m;\n    for (int i = 0; i < n; i++) {\n        char buf[64];\n        int sc;\n        if (scanf(\"%63s %d\", buf, &sc) != 2) return 0;\n        m.emplace(buf, sc);          // ★ 已存在则丢弃，保留首次\n    }\n\n    for (const auto& kv : m) printf(\"%s %d\\n\", kv.first.c_str(), kv.second);\n    printf(\"count=%zu\\n\", m.size());\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <string>\n#include <vector>\n#include <set>\n#include <algorithm>\nusing namespace std;\n\n// 独立实现：vector 记「首次出现的顺序」，set 只用来判重，最后整体排序输出。\n// 完全不用 map，验证 emplace 的语义。\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n\n    vector<pair<string, int>> recs;\n    set<string> seen;\n    for (int i = 0; i < n; i++) {\n        char buf[64];\n        int sc;\n        if (scanf(\"%63s %d\", buf, &sc) != 2) return 0;\n        string name = buf;\n        if (seen.insert(name).second) {        // 第一次见\n            recs.push_back({name, sc});\n        }\n    }\n\n    sort(recs.begin(), recs.end());            // pair 先比 first 再比 second，此处 first 唯一\n    for (const auto& kv : recs) printf(\"%s %d\\n\", kv.first.c_str(), kv.second);\n    printf(\"count=%zu\\n\", recs.size());\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\namy 90\nbob 80\namy 60\ncid 70\nbob 100\n",
                "expected_stdout": "amy 90\nbob 80\ncid 70\ncount=3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\nzoe 1\n",
                "expected_stdout": "zoe 1\ncount=1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\na 1\na 2\na 3\na 4\n",
                "expected_stdout": "a 1\ncount=1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\nb 2\na 1\nc 3\nb 20\nc 30\na 10\n",
                "expected_stdout": "a 1\nb 2\nc 3\ncount=3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\nx 0\ny 1000\nx 1000\n",
                "expected_stdout": "x 0\ny 1000\ncount=2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\nm 5\nk 4\nm 3\nk 2\nm 1\n",
                "expected_stdout": "k 4\nm 5\ncount=2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "nth_element 线性求中位数与四分位",
        "subject": "cpp",
        "line": "cpp",
        "question_type": "programming",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "技巧特训",
            "STL",
            "nth_element",
            "次序统计量",
            "部分排序"
        ],
        "statement_md": "给定 `n` 个**非负**整数，先把它们升序排好（想象一个排好的数组 `b`，下标从 0 开始），然后输出：\n\n- `median=` `n` 为奇数时取 `b[n/2]`；`n` 为偶数时取 `(b[n/2-1] + b[n/2]) / 2`（整除）\n- `q1=` `b[n/4]`\n- `q3=` `b[min(3n/4, n-1)]`\n\n全排序是 `O(n log n)`，但「**只求第 k 小**」其实 `O(n)` 就够 —— `nth_element`：\n\n```cpp\nvector<int> b = v;\nnth_element(b.begin(), b.begin() + n / 2, b.end());   // 让 b[n/2] 就位\nlong long hi = b[n / 2];\nlong long lo = *max_element(b.begin(), b.begin() + n / 2);  // 偶数 n 的下中位数\n```\n\n★ `nth_element(first, nth, last)` 只保证「`nth` 位置上的元素就是排序后该位置的值」，**左右两侧不保证有序**。所以取 `b[n/2]` 安全，取 `b[n/2-1]` 就不安全 —— 但「前 `n/2` 个里最大的那个」一定等于 `b[n/2-1]`，于是用 `max_element` 补上。\n\n⚠️ 三个坑：\n1. 对同一个数组连续 `nth_element` 不同位置是安全的，但**别假设已经就位的位置还保持原值**（每次调用只承诺 `nth` 那一个）。稳妥做法：拷一份原始数组，或每次从副本重新来。\n2. `nth_element` 要求 `nth` 在 `[first, last)` 内；`n == 1` 时 `begin() + 0` 合法，不会崩。\n3. 偶数长度的「中位数」是两数平均，**先加后除**；本题输入非负，所以 C++ 的截断除法与数学向下取整一致。",
        "input_format": "第一行 `n`；第二行 `n` 个非负整数。",
        "output_format": "三行：`median=<中位数>` / `q1=<下四分位>` / `q3=<上四分位>`。",
        "constraints_md": "- 1 ≤ n ≤ 200000\n- 0 ≤ a[i] ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · C++",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <vector>\n#include <algorithm>\nusing namespace std;\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    vector<int> v(n);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &v[i]);\n\n    vector<int> b = v;                       // 拷一份，nth_element 会打乱\n    nth_element(b.begin(), b.begin() + n / 2, b.end());\n    long long hi = b[n / 2];\n    long long med;\n    if (n % 2 == 1) {\n        med = hi;\n    } else {\n        long long lo = *max_element(b.begin(), b.begin() + n / 2);  // 下中位数\n        med = (lo + hi) / 2;\n    }\n\n    // q1 / q3 各自从原始副本重新 nth，避免相互干扰\n    vector<int> c = v;\n    nth_element(c.begin(), c.begin() + n / 4, c.end());\n    long long q1 = c[n / 4];\n\n    vector<int> e = v;\n    int i3 = min(3 * n / 4, n - 1);\n    nth_element(e.begin(), e.begin() + i3, e.end());\n    long long q3 = e[i3];\n\n    printf(\"median=%lld\\nq1=%lld\\nq3=%lld\\n\", med, q1, q3);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <vector>\n#include <algorithm>\nusing namespace std;\n\n// 独立实现：老老实实全排序，直接按下标取 —— 用来验证 nth_element 那套「部分排序」的结果。\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    vector<int> a(n);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    sort(a.begin(), a.end());\n\n    long long med;\n    if (n % 2 == 1) med = a[n / 2];\n    else med = ((long long)a[n / 2 - 1] + a[n / 2]) / 2;\n\n    long long q1 = a[n / 4];\n    long long q3 = a[min(3 * n / 4, n - 1)];\n    printf(\"median=%lld\\nq1=%lld\\nq3=%lld\\n\", med, q1, q3);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n3 1 4 1 5\n",
                "expected_stdout": "median=3\nq1=1\nq3=4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n1 2 3 4\n",
                "expected_stdout": "median=2\nq1=2\nq3=4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n7\n",
                "expected_stdout": "median=7\nq1=7\nq3=7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n10 20 30 40 50 60\n",
                "expected_stdout": "median=35\nq1=20\nq3=50\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8\n0 0 0 0 100 100 100 100\n",
                "expected_stdout": "median=50\nq1=0\nq3=100\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7\n9 8 7 6 5 4 3\n",
                "expected_stdout": "median=6\nq1=4\nq3=8\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "copy_if 配 back_inserter 一次抽子集",
        "subject": "cpp",
        "line": "cpp",
        "question_type": "programming",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "技巧特训",
            "STL",
            "copy_if",
            "back_inserter",
            "谓词"
        ],
        "statement_md": "给定 `n` 个整数和区间 `[lo, hi]`，抽出**同时满足**下面两个条件的元素：\n\n1. `lo <= x <= hi`\n2. `x` **不是** 3 的倍数\n\n抽出来的元素**保持原来的先后顺序**，输出个数与它们本身。\n\n一行流写法（这是「按条件收集」的标准套路）：\n\n```cpp\nvector<int> kept;\ncopy_if(v.begin(), v.end(), back_inserter(kept), [&](int x) {\n    return x >= lo && x <= hi && x % 3 != 0;\n});\n```\n\n★ 为什么必须 `back_inserter`：`copy_if` 的第三个参数是**输出迭代器**，直接传 `kept.begin()` 会在空 `vector` 上写越界（UB，`-O2` 下可能不崩）。`back_inserter` 包成「每写一个就 `push_back`」，容器自己长。\n\n⚠️ 三个坑：\n1. `copy_if` **不 reserve**，元素多时会多次扩容；知道上界就先 `kept.reserve(n)`。\n2. 谓词捕获 `lo/hi` 建议用 `[&]` 或 `[=]`；显式写 `[lo, hi]` 更清楚，但别捕获成引用后又改了它们 —— 谓词调用时机由实现决定。\n3. **负数取模**：`-6 % 3 == 0` ✓，所以「不是 3 的倍数」写 `x % 3 != 0` 对负数也对；写成 `x % 3 > 0` 就会把 `-6`（模为 0）之外的 `-4`（模为 -1）漏掉。\n\n💡 `remove_if` 是「原地删」，`copy_if` 是「抽到别处」。要保留原数组就用 `copy_if`。",
        "input_format": "第一行 `n`；第二行 `n` 个整数；第三行 `lo hi`。",
        "output_format": "两行：`kept=<个数>` / 保留的元素（空格分隔；没有则输出空行）。",
        "constraints_md": "- 1 ≤ n ≤ 100000\n- |a[i]|, |lo|, |hi| ≤ 10⁹\n- lo ≤ hi",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · C++",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <vector>\n#include <algorithm>\n#include <iterator>\nusing namespace std;\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    vector<int> v(n);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &v[i]);\n    long long lo, hi;\n    if (scanf(\"%lld %lld\", &lo, &hi) != 2) return 0;\n\n    vector<int> kept;\n    kept.reserve(n);                      // 知道上界就先要空间\n    copy_if(v.begin(), v.end(), back_inserter(kept), [lo, hi](int x) {\n        return x >= lo && x <= hi && x % 3 != 0;\n    });\n\n    printf(\"kept=%zu\\n\", kept.size());\n    for (size_t i = 0; i < kept.size(); i++) printf(i ? \" %d\" : \"%d\", kept[i]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <vector>\nusing namespace std;\n\n// 独立实现：手写 for + push_back，不用 copy_if / back_inserter。\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    vector<int> v(n);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &v[i]);\n    long long lo, hi;\n    if (scanf(\"%lld %lld\", &lo, &hi) != 2) return 0;\n\n    vector<int> kept;\n    for (int x : v) {\n        if (x >= lo && x <= hi && x % 3 != 0) kept.push_back(x);\n    }\n\n    printf(\"kept=%zu\\n\", kept.size());\n    for (size_t i = 0; i < kept.size(); i++) printf(i ? \" %d\" : \"%d\", kept[i]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "6\n1 2 3 4 5 6\n2 5\n",
                "expected_stdout": "kept=3\n2 4 5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n-6 -4 -3 -1 0\n-10 10\n",
                "expected_stdout": "kept=2\n-4 -1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n1 2 4 5\n10 20\n",
                "expected_stdout": "kept=0\n\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n3 6 9\n0 100\n",
                "expected_stdout": "kept=0\n\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7\n0 3 6 9 12 15 18\n0 18\n",
                "expected_stdout": "kept=0\n\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n-9 -8 -7 -6 -5\n-9 -5\n",
                "expected_stdout": "kept=3\n-8 -7 -5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "tuple 的字典序就是三段排序：科目·分数·学号",
        "subject": "cpp",
        "line": "cpp",
        "question_type": "programming",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "技巧特训",
            "STL",
            "tuple",
            "结构化绑定",
            "字典序"
        ],
        "statement_md": "输入 `n` 条记录 `科目 分数 学号`，按下面的优先级排序后逐行输出：\n\n1. **科目**字典序升\n2. 分数**降序**\n3. 学号**升序**\n\n`tuple` 自带的比较是**逐个元素字典序**，所以把「降序的字段取负」塞进去，排序就变成零成本：\n\n```cpp\nvector<tuple<string, int, int>> v;      // (科目, -分数, 学号)\nv.emplace_back(sub, -score, sid);\nsort(v.begin(), v.end());               // 直接排，不用写比较器\nfor (const auto& [sub, neg, sid] : v)   // C++17 结构化绑定\n    printf(\"%s %d %d\\n\", sub.c_str(), -neg, sid);\n```\n\n★ 为什么用「取负」而不是写比较器：`tuple` 的 `operator<` 已经是「先比第 0 个，相等再比第 1 个……」，把要降序的整数字段取负，升序排出来就是降序。前提是**字段类型是整数**；字符串要降序就没法取负了，得改用 `greater<>` 包住或写自定义比较器。\n\n⚠️ 三个坑：\n1. **别混着用 `vector<pair>`**：pair 只有两个字段，第三个塞不进去。\n2. 结构化绑定是 C++17 的（本平台 `-std=c++17` 支持）；C++14 下要写 `get<0>(t)`。\n3. 输出时**记得把分数取回正号** —— 忘了就是全班负分。",
        "input_format": "第一行 `n`；接下来 `n` 行，每行 `科目 分数 学号`。",
        "output_format": "`n` 行，每行 `科目 分数 学号`（分数为正）。",
        "constraints_md": "- 1 ≤ n ≤ 100000\n- 科目只含小写字母，长度 ≤ 10\n- 0 ≤ 分数 ≤ 100\n- 1 ≤ 学号 ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · C++",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <string>\n#include <vector>\n#include <tuple>\n#include <algorithm>\nusing namespace std;\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n\n    vector<tuple<string, int, int>> v;      // (科目, -分数, 学号)\n    v.reserve(n);\n    for (int i = 0; i < n; i++) {\n        char sub[64];\n        int score, sid;\n        if (scanf(\"%63s %d %d\", sub, &score, &sid) != 3) return 0;\n        v.emplace_back(string(sub), -score, sid);\n    }\n\n    sort(v.begin(), v.end());               // tuple 字典序，无需比较器\n\n    for (const auto& [sub, neg, sid] : v) {\n        printf(\"%s %d %d\\n\", sub.c_str(), -neg, sid);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <string>\n#include <vector>\n#include <algorithm>\nusing namespace std;\n\n// 独立实现：struct + 手写三段比较器（不取负、不用 tuple 字典序）。\nstruct Rec {\n    string sub;\n    int score;\n    long long sid;\n};\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n\n    vector<Rec> v(n);\n    for (int i = 0; i < n; i++) {\n        char sub[64];\n        int score;\n        long long sid;\n        if (scanf(\"%63s %d %lld\", sub, &score, &sid) != 3) return 0;\n        v[i] = {string(sub), score, sid};\n    }\n\n    sort(v.begin(), v.end(), [](const Rec& a, const Rec& b) {\n        if (a.sub != b.sub) return a.sub < b.sub;       // 科目升\n        if (a.score != b.score) return a.score > b.score;  // 分数降\n        return a.sid < b.sid;                           // 学号升\n    });\n\n    for (const auto& r : v) printf(\"%s %d %lld\\n\", r.sub.c_str(), r.score, r.sid);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4\nmath 90 2\nmath 90 1\nphysics 80 3\nmath 95 4\n",
                "expected_stdout": "math 95 4\nmath 90 1\nmath 90 2\nphysics 80 3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\nart 60 7\n",
                "expected_stdout": "art 60 7\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\nb 50 1\na 50 2\nb 70 3\na 70 4\nb 50 0\n",
                "expected_stdout": "a 70 4\na 50 2\nb 70 3\nb 50 0\nb 50 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\nz 100 1\ny 0 2\nx 50 3\n",
                "expected_stdout": "x 50 3\ny 0 2\nz 100 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\ncs 90 10\ncs 90 9\ncs 85 8\nbio 85 7\nbio 85 6\nbio 95 5\n",
                "expected_stdout": "bio 95 5\nbio 85 6\nbio 85 7\ncs 90 9\ncs 90 10\ncs 85 8\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\nsame 1 1000000000\nsame 1 1\n",
                "expected_stdout": "same 1 1\nsame 1 1000000000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "排序后双指针夹逼：和为 0 的三元组",
        "subject": "cpp",
        "line": "cpp",
        "question_type": "programming",
        "difficulty": 4,
        "total_score": 25,
        "tags": [
            "技巧特训",
            "竞赛",
            "双指针",
            "去重",
            "三数之和"
        ],
        "statement_md": "给定 `n` 个整数（可负、可重复），数出**有多少个不同的三元组**（按取值，不看下标）满足 `a + b + c = 0`。\n\n暴力三重循环是 `O(n³)`，`n = 3000` 直接超时。标准做法是**先排序，再固定一个数、双指针夹逼**：\n\n```cpp\nsort(a.begin(), a.end());\nfor (int i = 0; i + 2 < n; i++) {\n    if (i && a[i] == a[i - 1]) continue;        // ① 第一层去重\n    int lo = i + 1, hi = n - 1;\n    while (lo < hi) {\n        long long s = (long long)a[i] + a[lo] + a[hi];\n        if (s == 0) {\n            cnt++;\n            int v = a[lo]; while (lo < hi && a[lo] == v) lo++;   // ② 第二层去重\n            v = a[hi];     while (lo < hi && a[hi] == v) hi--;\n        } else if (s < 0) lo++;\n        else hi--;\n    }\n}\n```\n\n★ 为什么能夹逼：数组有序后，`a[i]` 固定时 `a[lo] + a[hi]` 随 `lo` 增大单调增、随 `hi` 减小单调减，于是「和太小就抬 `lo`、太大就压 `hi`」每一步都在排除一整片不可能的解，总复杂度 `O(n²)`。\n\n⚠️ 四个坑：\n1. **两层去重缺一不可**。漏了 ①，同一组值会被不同 `i` 重复数；漏了 ②，同一组值在 `lo/hi` 上重复数。\n2. `a[i] + a[lo] + a[hi]` 用 `int` 累加会溢出（三个 10⁵ 没问题，但换到 10⁹ 级就炸）；**先转 `long long` 再相加**是习惯动作。\n3. 去重时 `lo`/`hi` 的移动必须**自己带边界检查**（`lo < hi`），否则可能越界。\n4. 三元组要求三个**不同下标**，所以内层从 `i + 1` 起步；若从 0 起步，`[0,0,0]` 这种会被数出来。",
        "input_format": "第一行 `n`；第二行 `n` 个整数（可负）。",
        "output_format": "一行：`triples=<不同取值三元组的个数>`。",
        "constraints_md": "- 1 ≤ n ≤ 3000\n- |a[i]| ≤ 10⁵\n- 要求 O(n²)；O(n³) 会超时",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · C++",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <vector>\n#include <algorithm>\nusing namespace std;\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    vector<int> a(n);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    sort(a.begin(), a.end());\n\n    long long cnt = 0;\n    for (int i = 0; i + 2 < n; i++) {\n        if (i > 0 && a[i] == a[i - 1]) continue;          // ① 第一层去重\n        int lo = i + 1, hi = n - 1;\n        while (lo < hi) {\n            long long s = (long long)a[i] + a[lo] + a[hi]; // ★ 先转 64 位\n            if (s == 0) {\n                cnt++;\n                int v = a[lo];\n                while (lo < hi && a[lo] == v) lo++;        // ② 第二层去重\n                v = a[hi];\n                while (lo < hi && a[hi] == v) hi--;\n            } else if (s < 0) {\n                lo++;\n            } else {\n                hi--;\n            }\n        }\n    }\n    printf(\"triples=%lld\\n\", cnt);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <vector>\n#include <set>\n#include <unordered_set>\n#include <algorithm>\nusing namespace std;\n\n// 独立实现：不用双指针。固定 i 与 j，用哈希表查第三个数是否存在，\n// 命中的三元组丢进 set<vector<int>> 去重。O(n²) 但常数更大、思路完全不同。\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    vector<int> a(n);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    sort(a.begin(), a.end());\n\n    set<vector<int>> found;\n    for (int i = 0; i + 2 < n; i++) {\n        if (i > 0 && a[i] == a[i - 1]) continue;\n        unordered_set<int> seen;                 // j 之前出现过的值\n        for (int j = i + 1; j < n; j++) {\n            long long need = -(long long)a[i] - a[j];\n            if (need >= -2147483648LL && need <= 2147483647LL &&\n                seen.count((int)need)) {\n                vector<int> t = {a[i], (int)need, a[j]};\n                sort(t.begin(), t.end());\n                found.insert(t);\n            }\n            seen.insert(a[j]);\n        }\n    }\n    printf(\"triples=%zu\\n\", found.size());\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "6\n-1 0 1 2 -1 -4\n",
                "expected_stdout": "triples=2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n0 0 0\n",
                "expected_stdout": "triples=1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n1 2 3 4\n",
                "expected_stdout": "triples=0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n0 0 0 0 0\n",
                "expected_stdout": "triples=1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7\n-2 -1 0 1 2 3 -3\n",
                "expected_stdout": "triples=5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8\n-4 -2 -2 0 2 2 4 4\n",
                "expected_stdout": "triples=4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "扫描线求区间并集总长度",
        "subject": "cpp",
        "line": "cpp",
        "question_type": "programming",
        "difficulty": 4,
        "total_score": 25,
        "tags": [
            "技巧特训",
            "竞赛",
            "扫描线",
            "区间合并",
            "差分"
        ],
        "statement_md": "给定 `n` 个闭区间 `[l, r]`，求它们**并集的总长度**。长度按 `r - l` 计算（线段长度，不是整数点个数）。端点相接（`[1,3]` 与 `[3,5]`）视为连通，总长 `4`。\n\n标准扫描：按左端点排序，维护「当前合并段的左右端」：\n\n```cpp\nsort(segs.begin(), segs.end());\nlong long cl = segs[0].first, cr = segs[0].second, total = 0;\nfor (size_t i = 1; i < segs.size(); i++) {\n    if (segs[i].first <= cr) cr = max(cr, segs[i].second);   // ★ 相交或相接 → 合并\n    else { total += cr - cl; cl = segs[i].first; cr = segs[i].second; }\n}\ntotal += cr - cl;      // 最后一段别忘了收尾\n```\n\n★ 另一种完全等价的思路是**差分/事件点**：每个区间记两个事件 `(l, +1)`、`(r, -1)`，按坐标排序后扫一遍，只要「当前覆盖数 > 0」就把相邻两个坐标之间的距离累加。这招能直接推广到「求被覆盖至少 k 层的长度」，比合并段更通用。\n\n⚠️ 四个坑：\n1. **`<=` 还是 `<`**：题面说端点相接算连通，所以合并条件是 `l <= cr`。写成 `<` 会把相邻区间断开，总长不变但段数算多（本题只问总长，所以 `<=` 与 `<` 结果其实相同 —— 但换成「求段数」就会错）。\n2. **收尾**：循环结束后最后一段的 `cr - cl` 要单独加，漏了就是「少算一段」。\n3. 坐标可负、可达 10⁹，长度用 `long long`。\n4. 包在别的区间里的小区间（`[2,3]` 落在 `[1,10]` 内）不能让 `cr` 变小 —— 必须 `cr = max(cr, r)`。",
        "input_format": "第一行 `n`；接下来 `n` 行，每行 `l r`（`l ≤ r`）。",
        "output_format": "一行：`covered=<并集总长度>`。",
        "constraints_md": "- 1 ≤ n ≤ 100000\n- |l|, |r| ≤ 10⁹，l ≤ r\n- 总长度可能到 10⁹ 以上",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · C++",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <vector>\n#include <algorithm>\nusing namespace std;\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    vector<pair<long long, long long>> segs(n);\n    for (int i = 0; i < n; i++) scanf(\"%lld %lld\", &segs[i].first, &segs[i].second);\n    sort(segs.begin(), segs.end());\n\n    long long cl = segs[0].first, cr = segs[0].second, total = 0;\n    for (int i = 1; i < n; i++) {\n        if (segs[i].first <= cr) {\n            if (segs[i].second > cr) cr = segs[i].second;   // ★ 别让 cr 变小\n        } else {\n            total += cr - cl;\n            cl = segs[i].first;\n            cr = segs[i].second;\n        }\n    }\n    total += cr - cl;                                       // 收尾\n    printf(\"covered=%lld\\n\", total);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <vector>\n#include <algorithm>\nusing namespace std;\n\n// 独立实现：差分 / 事件点扫描，不做区间合并。\n// 每个区间贡献 (l, +1) 与 (r, -1) 两个事件；同一坐标上的事件要先全部处理，\n// 再决定「接下来这一段」是否被覆盖 —— 否则端点相接会算错。\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    vector<pair<long long, int>> ev;\n    ev.reserve(2 * n);\n    for (int i = 0; i < n; i++) {\n        long long l, r;\n        scanf(\"%lld %lld\", &l, &r);\n        ev.push_back({l, 1});\n        ev.push_back({r, -1});\n    }\n    sort(ev.begin(), ev.end());\n\n    long long total = 0;\n    int cover = 0;\n    for (size_t i = 0; i < ev.size(); i++) {\n        size_t j = i;\n        long long x = ev[i].first;\n        while (j < ev.size() && ev[j].first == x) {   // 同一坐标的事件一起消化\n            cover += ev[j].second;\n            j++;\n        }\n        if (j < ev.size() && cover > 0) {\n            total += ev[j].first - x;                 // 被覆盖的一段\n        }\n        i = j - 1;\n    }\n    printf(\"covered=%lld\\n\", total);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "2\n1 3\n3 5\n",
                "expected_stdout": "covered=4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n1 4\n2 6\n8 10\n",
                "expected_stdout": "covered=7\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n0 0\n",
                "expected_stdout": "covered=0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n-5 -1\n-2 2\n10 20\n",
                "expected_stdout": "covered=17\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n5 6\n1 2\n6 7\n2 3\n",
                "expected_stdout": "covered=4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n1 10\n2 3\n4 5\n",
                "expected_stdout": "covered=9\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "换一种比较器：把数拼成最小的数字（a+b<b+a）",
        "subject": "cpp",
        "line": "cpp",
        "question_type": "programming",
        "difficulty": 4,
        "total_score": 25,
        "tags": [
            "技巧特训",
            "竞赛",
            "比较器",
            "贪心",
            "字符串拼接"
        ],
        "statement_md": "给定 `n` 个非负整数，把它们**全部用上**、按某种顺序拼成一个数字，要求结果**最小**。输出这个数字（去掉前导零；全是 0 时输出 `0`）。\n\n这题的难点是：**按字典序排是错的**。比如 `9` 与 `30`，字典序 `30 < 9`，拼出来 `309`；但 `930` 更大，所以正确答案是 `309` —— 这个例子字典序碰巧对了。换成 `3` 与 `30`：字典序 `3 < 30` 得到 `330`，而 `303` 更小。所以必须比「拼接后的结果」：\n\n```cpp\nsort(s.begin(), s.end(), [](const string& a, const string& b) {\n    return a + b < b + a;      // ★ 比较的是拼接结果，不是单个数\n});\nstring res;\nfor (auto& t : s) res += t;\nsize_t p = res.find_first_not_of('0');\nres = (p == string::npos) ? \"0\" : res.substr(p);\n```\n\n★ 为什么这个比较器成立：`a+b < b+a` 定义了一个**全序**（可以证明它满足传递性），于是「按它排序后顺序拼接」就是最小解 —— 这是贪心的典型形态：\n把「整体最优」归结为「相邻两元素该谁在前」的局部判断。\n\n⚠️ 四个坑：\n1. **千万别按数值大小排**。`9` 和 `90`：数值 `9 < 90`，但该 `909`？不对，最小是 `909`… 而 `9` 与 `91` 应该拼成 `991` 还是 `919`？`919` 更小 —— 数值序完全失效。\n2. 比较器里 `a + b` 每次都会**新建字符串**，`n` 大时开销明显；本项目 `n ≤ 1000` 无妨，`n = 10⁵` 时要改用「按重复次数补全」的技巧。\n3. 前导零必须处理：输入 `[0, 0]` 拼出来是 `00`，应输出 `0`。\n4. 用**字符串**存每个数，别转成 `int` —— `10⁹` 以上会溢出，且前导零信息也会丢。",
        "input_format": "第一行 `n`；第二行 `n` 个非负整数（无前导零）。",
        "output_format": "一行：拼成的最小数字字符串（无前导零；全零输出 `0`）。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 0 ≤ 每个数 < 10⁹\n- 结果长度 ≤ 9000",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · C++",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <string>\n#include <vector>\n#include <algorithm>\nusing namespace std;\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    vector<string> s(n);\n    for (int i = 0; i < n; i++) {\n        char buf[32];\n        if (scanf(\"%31s\", buf) != 1) return 0;\n        s[i] = buf;\n    }\n\n    sort(s.begin(), s.end(), [](const string& a, const string& b) {\n        return a + b < b + a;          // ★ 比拼接结果，不比单个数\n    });\n\n    string res;\n    for (const auto& t : s) res += t;\n    size_t p = res.find_first_not_of('0');\n    if (p == string::npos) res = \"0\";\n    else res = res.substr(p);\n    printf(\"%s\\n\", res.c_str());\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <string>\n#include <vector>\nusing namespace std;\n\n// 独立实现：手写归并排序，同一个比较规则但完全不用 std::sort。\nstatic bool less_concat(const string& a, const string& b) { return a + b < b + a; }\n\nstatic void msort(vector<string>& v, vector<string>& tmp, int l, int r) {\n    if (r - l <= 1) return;\n    int m = l + (r - l) / 2;\n    msort(v, tmp, l, m);\n    msort(v, tmp, m, r);\n    int i = l, j = m, k = l;\n    while (i < m && j < r) {\n        if (less_concat(v[j], v[i])) tmp[k++] = v[j++];\n        else tmp[k++] = v[i++];              // 相等时取左边 → 稳定\n    }\n    while (i < m) tmp[k++] = v[i++];\n    while (j < r) tmp[k++] = v[j++];\n    for (int t = l; t < r; t++) v[t] = tmp[t];\n}\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    vector<string> s(n);\n    for (int i = 0; i < n; i++) {\n        char buf[32];\n        if (scanf(\"%31s\", buf) != 1) return 0;\n        s[i] = buf;\n    }\n\n    vector<string> tmp(n);\n    msort(s, tmp, 0, n);\n\n    string res;\n    for (const auto& t : s) res += t;\n    size_t p = res.find_first_not_of('0');\n    if (p == string::npos) res = \"0\";\n    else res = res.substr(p);\n    printf(\"%s\\n\", res.c_str());\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n3 30 34\n",
                "expected_stdout": "30334\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n10 2\n",
                "expected_stdout": "102\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n0 0\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n9 91 1 0\n",
                "expected_stdout": "1919\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n121 12 1\n",
                "expected_stdout": "112112\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n999999999 1 0 10 100\n",
                "expected_stdout": "100101999999999\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "partial_sum 建前缀和后每次查询 O(1)",
        "subject": "cpp",
        "line": "cpp",
        "question_type": "programming",
        "difficulty": 4,
        "total_score": 25,
        "tags": [
            "技巧特训",
            "STL",
            "partial_sum",
            "前缀和",
            "long long"
        ],
        "statement_md": "给定 `n` 个整数（可负）和 `q` 次查询，每次查询 `[l, r]`（**1 起、闭区间**），输出该区间的元素之和。\n\n前缀和一遍 `O(n)`，之后每次查询 `O(1)`：`pre[r] - pre[l-1]`。建前缀和可以用 `partial_sum`（注意写到 `pre.begin() + 1`，让 `pre[0] = 0` 当哨兵）：\n\n```cpp\nvector<long long> pre(n + 1, 0);\npartial_sum(a.begin(), a.end(), pre.begin() + 1);   // pre[i] = a[0..i-1] 之和\nprintf(\"%lld\\n\", pre[r] - pre[l - 1]);             // l 是 1 起的，正好\n```\n\n★ `pre` 多开一位并置 0，是为了让 `l == 1` 时 `pre[l-1] = pre[0] = 0` 自然成立 —— **不用特判左边界**。这是前缀和最基本的纪律：**只要下标是 1 起，前缀数组就开 `n+1`**。\n\n⚠️ 四个坑：\n1. **必须 `long long`**。`n = 2×10⁵`、每个 `10⁹` 时总和 2×10¹⁴，`int` 直接溢出。\n2. `partial_sum` 的第二区间**不检查长度**：写到 `pre.begin()` 会让 `pre[0]` 变成 `a[0]`，于是 `l = 1` 的查询全部错 —— 而且不会崩，是个纯逻辑错。\n3. 格式上的小习惯：C 的 `printf` 用 `\\n` 就够快；如果改用 C++ 的 `cout`，**别用 `endl`** —— 它会每次强制刷缓冲，`q = 2×10⁵` 时明显拖慢。\n4. 如果查询**不要求在线**，还能用差分/离线排序，但前缀和已经是最简。",
        "input_format": "第一行 `n q`；第二行 `n` 个整数；接下来 `q` 行每行 `l r`（1 ≤ l ≤ r ≤ n）。",
        "output_format": "`q` 行，每行一个整数：区间和。",
        "constraints_md": "- 1 ≤ n, q ≤ 200000\n- |a[i]| ≤ 10⁹\n- 总和可能到 2×10¹⁴，必须 64 位",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · C++",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <vector>\n#include <numeric>\nusing namespace std;\n\nint main() {\n    int n, q;\n    if (scanf(\"%d %d\", &n, &q) != 2) return 0;\n    vector<long long> a(n);\n    for (int i = 0; i < n; i++) scanf(\"%lld\", &a[i]);\n\n    vector<long long> pre(n + 1, 0);\n    partial_sum(a.begin(), a.end(), pre.begin() + 1);   // ★ 从 +1 开始写\n\n    while (q--) {\n        int l, r;\n        scanf(\"%d %d\", &l, &r);\n        printf(\"%lld\\n\", pre[r] - pre[l - 1]);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <vector>\nusing namespace std;\n\n// 独立实现：手写累加建前缀，不用 partial_sum。\nint main() {\n    int n, q;\n    if (scanf(\"%d %d\", &n, &q) != 2) return 0;\n\n    vector<long long> pre(n + 1, 0);\n    for (int i = 1; i <= n; i++) {\n        long long x;\n        scanf(\"%lld\", &x);\n        pre[i] = pre[i - 1] + x;\n    }\n\n    while (q--) {\n        int l, r;\n        scanf(\"%d %d\", &l, &r);\n        printf(\"%lld\\n\", pre[r] - pre[l - 1]);\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 3\n1 2 3 4 5\n1 5\n2 3\n5 5\n",
                "expected_stdout": "15\n5\n5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 2\n-1 -2 -3\n1 3\n2 2\n",
                "expected_stdout": "-6\n-2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 1\n1000000000\n1 1\n",
                "expected_stdout": "1000000000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4 3\n1000000000 1000000000 1000000000 1000000000\n1 4\n1 1\n2 3\n",
                "expected_stdout": "4000000000\n1000000000\n2000000000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6 2\n0 0 0 0 0 0\n1 6\n3 4\n",
                "expected_stdout": "0\n0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5 2\n-1000000000 1000000000 -5 5 0\n1 5\n2 4\n",
                "expected_stdout": "0\n1000000000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "大顶堆做贪心：单机任务最少迟到几个",
        "subject": "cpp",
        "line": "cpp",
        "question_type": "programming",
        "difficulty": 4,
        "total_score": 25,
        "tags": [
            "技巧特训",
            "竞赛",
            "priority_queue",
            "贪心",
            "调度"
        ],
        "statement_md": "有 `n` 个任务，每个任务有耗时 `t` 和截止期 `d`。单机从时刻 0 开始、中途不停，一个任务只要**完成时刻 > 它的截止期**就算迟到。求**最少有几个任务会迟到**。\n\n经典贪心（Moore-Hodgson）：**按截止期升序处理**，先把任务全部排进去；一旦累计耗时超过当前截止期，就**踢掉已排任务里耗时最大的那个**（记为迟到）：\n\n```cpp\nsort(jobs.begin(), jobs.end());            // 按截止期升序\npriority_queue<long long> pq;              // 默认就是大顶堆\nlong long total = 0, late = 0;\nfor (auto& j : jobs) {\n    total += j.second;                     // 先接进来\n    pq.push(j.second);\n    if (total > j.first) {                 // 超期了\n        total -= pq.top(); pq.pop();       // 踢掉最费时的\n        late++;\n    }\n}\n```\n\n★ 为什么踢「耗时最大」：把最大的那个任务拿掉，既能最大程度地把总时长压回截止期以内，又只损失 1 个任务 —— 换掉任何别的任务，时长降得都没它多。而「按截止期升序」保证每次判定用的都是当前最紧的那条线。\n\n⚠️ 四个坑：\n1. `priority_queue<long long>` **默认就是大顶堆**，这里要的正是最大值，所以千万别顺手加 `greater<>`（那是小顶堆，会踢掉最省时的，答案直接错）。\n2. 累计耗时用 `long long`：`n = 10⁵`、单个 `10⁹` 时总和到 10¹⁴。\n3. 注意「先加后判」的顺序。先判后加会漏掉「这一个任务自己就使它超期」的情形。\n4. 截止期可以重复、可以很大，不需要离散化 —— 排一次序 + 一次堆操作就够，总复杂度 `O(n log n)`。",
        "input_format": "第一行 `n`；接下来 `n` 行，每行 `耗时 截止期`。",
        "output_format": "一行：`late=<最少迟到任务数>`。",
        "constraints_md": "- 1 ≤ n ≤ 100000\n- 1 ≤ 耗时 ≤ 10⁹\n- 0 ≤ 截止期 ≤ 10¹⁴",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "技巧特训 · C++",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <vector>\n#include <queue>\n#include <algorithm>\nusing namespace std;\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    vector<pair<long long, long long>> jobs(n);   // (截止期, 耗时)\n    for (int i = 0; i < n; i++) scanf(\"%lld %lld\", &jobs[i].second, &jobs[i].first);\n    sort(jobs.begin(), jobs.end());               // 按截止期升序\n\n    priority_queue<long long> pq;                 // ★ 默认大顶堆，正好要最大\n    long long total = 0, late = 0;\n    for (const auto& j : jobs) {\n        total += j.second;\n        pq.push(j.second);\n        if (total > j.first) {\n            total -= pq.top();\n            pq.pop();\n            late++;\n        }\n    }\n    printf(\"late=%lld\\n\", late);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <vector>\n#include <set>\n#include <algorithm>\nusing namespace std;\n\n// 独立实现：multiset 维护已排任务，踢人时取最后一个（最大）。\n// 不用 priority_queue，也不用它的模板参数。\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    vector<pair<long long, long long>> jobs(n);\n    for (int i = 0; i < n; i++) scanf(\"%lld %lld\", &jobs[i].second, &jobs[i].first);\n    sort(jobs.begin(), jobs.end());\n\n    multiset<long long> chosen;\n    long long total = 0, late = 0;\n    for (const auto& j : jobs) {\n        total += j.second;\n        chosen.insert(j.second);\n        if (total > j.first) {\n            auto it = prev(chosen.end());        // 最大的那个\n            total -= *it;\n            chosen.erase(it);\n            late++;\n        }\n    }\n    printf(\"late=%lld\\n\", late);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n3 5\n2 3\n1 1\n",
                "expected_stdout": "late=1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n5 5\n",
                "expected_stdout": "late=0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n5 4\n5 4\n",
                "expected_stdout": "late=2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n2 2\n2 2\n2 2\n2 2\n",
                "expected_stdout": "late=3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n10 100\n1 1\n1 2\n1 3\n1 4\n",
                "expected_stdout": "late=0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n100 100\n100 100\n100 100\n",
                "expected_stdout": "late=2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    }
]
