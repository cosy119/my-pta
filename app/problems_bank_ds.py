"""数据结构线题库（C / C++）—— **自动生成，不要手改**。

本文件由 `tools/gen_ds_bank.py` 产出，重新生成：

    python tools/gen_ds_bank.py

三条规矩写在这里，改题前先读一遍
--------------------------------
1. **期望输出不是拿参考解跑出来的** —— 由生成脚本里的独立 Python `oracle`
   预先算好（另一门语言、另一套写法）。拿参考解现跑现填等于自己给自己判卷。
2. **每题两套 C++ 实现**（`reference_solution` / `alt_solution`），
   `tools/verify_bank.py` 会把两套都跑一遍逐字节对拍。
   `alt_solution` 只在题库校验时用，`seed.py` 入库时会丢掉它。
3. **语言**：`line = "cpp"`，但**同一道题 C 和 C++ 都能交** ——
   C++ 走 g++ -std=c++17，C 走 gcc -std=gnu11（教材是 C 语言版）。
   判题时按提交里带的语言选编译器，见 `app/judge/runner_cpp.py`。

覆盖范围：数据结构第 01 ~ 08 讲（绪论理论题 / 线性表 / 栈与队列 / 串数组广义表 /
树与二叉树 / 图 / 查找 / 排序）。编程题集中在 02~08 讲；01 讲纯理论（考概念）。
"""
from __future__ import annotations

DS_PROBLEMS: list[dict] = [
    {
        "title": "顺序表按位插入",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "顺序表",
            "插入",
            "位序"
        ],
        "statement_md": "在一个顺序表中，把 `x` 插入到**位序 `i`** 的位置上（原来的第 `i` 个及以后的元素统统后移一位）。\n\n★ 教材里的**位序从 1 开始**，而 C 数组下标从 0 开始 —— 位序 `i` 对应下标 `i-1`。这是本讲最容易出错的地方。\n\n搬移必须**从后往前**做。反过来写（`j` 从小到大）会把后面的元素一路覆盖掉，而且编译器一个警告都不会给。",
        "input_format": "第一行一个整数 `n`（当前表长）。\n\n第二行 `n` 个整数，顺序表的元素。\n\n第三行一个整数 `i`，插入位置（位序，1 ≤ i ≤ n+1）。\n\n第四行一个整数 `x`，要插入的值。",
        "output_format": "一行，插入后的顺序表，元素之间用一个空格分隔。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 1 ≤ i ≤ n+1",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 02 讲 · 线性表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#define MAXN 2005\nint a[MAXN];\nint main(void) {\n    int n, i, x;\n    scanf(\"%d\", &n);\n    for (int k = 0; k < n; k++) scanf(\"%d\", &a[k]);\n    scanf(\"%d %d\", &i, &x);\n    // ★ 从后往前搬：位序 i 对应下标 i-1，把 [i-1, n-1] 整体后移一格\n    for (int j = n - 1; j >= i - 1; j--) a[j + 1] = a[j];\n    a[i - 1] = x;\n    n++;\n    for (int k = 0; k < n; k++) printf(\"%d%c\", a[k], k + 1 == n ? '\\n' : ' ');\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\nusing namespace std;\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    int n; cin >> n;\n    vector<int> a(n);\n    for (int &v : a) cin >> v;\n    int i, x; cin >> i >> x;\n    vector<int> b;                       // 另一套：不原地搬，重新拼一份\n    for (int k = 0; k < n; k++) {\n        if (k == i - 1) b.push_back(x);\n        b.push_back(a[k]);\n    }\n    if (i == n + 1) b.push_back(x);      // 插到末尾（原表后无元素可触发）\n    for (size_t k = 0; k < b.size(); k++)\n        cout << b[k] << (k + 1 == b.size() ? '\\n' : ' ');\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n1 2 3 4 5\n1\n9\n",
                "expected_stdout": "9 1 2 3 4 5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n1 2 3 4 5\n6\n9\n",
                "expected_stdout": "1 2 3 4 5 9\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n1 2 3 4 5\n3\n9\n",
                "expected_stdout": "1 2 9 3 4 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n7\n1\n0\n",
                "expected_stdout": "0 7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n7\n2\n8\n",
                "expected_stdout": "7 8\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "顺序表删除所有值为 x 的元素",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "顺序表",
            "删除",
            "双指针"
        ],
        "statement_md": "删除顺序表中**所有**值为 `x` 的元素，剩下的元素保持原来的相对次序。\n\n要求 O(n) 时间、O(1) 额外空间 —— 也就是用一个写指针 `k` 把「该留下的」往前压，不要每次都搬一整个数组。\n\n若删完表为空，输出 `empty`。",
        "input_format": "第一行一个整数 `n`。\n\n第二行 `n` 个整数。\n\n第三行一个整数 `x`。",
        "output_format": "一行，删除后的顺序表（空格分隔）；若为空则输出 `empty`。",
        "constraints_md": "- 1 ≤ n ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 02 讲 · 线性表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nint a[1005];\nint main(void) {\n    int n, x;\n    scanf(\"%d\", &n);\n    for (int k = 0; k < n; k++) scanf(\"%d\", &a[k]);\n    scanf(\"%d\", &x);\n    int k = 0;                       // k = 写指针：下一个该留下的位置\n    for (int j = 0; j < n; j++)\n        if (a[j] != x) a[k++] = a[j];\n    if (k == 0) { printf(\"empty\\n\"); return 0; }\n    for (int j = 0; j < k; j++) printf(\"%d%c\", a[j], j + 1 == k ? '\\n' : ' ');\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\nusing namespace std;\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    int n; cin >> n;\n    vector<int> a(n);\n    for (int &v : a) cin >> v;\n    int x; cin >> x;\n    vector<int> out;                 // 另一套：直接挑出该留的，不原地压缩\n    for (int v : a) if (v != x) out.push_back(v);\n    if (out.empty()) { cout << \"empty\\n\"; return 0; }\n    for (size_t k = 0; k < out.size(); k++)\n        cout << out[k] << (k + 1 == out.size() ? '\\n' : ' ');\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n1 2 3 2 4\n2\n",
                "expected_stdout": "1 3 4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n2 2 2\n2\n",
                "expected_stdout": "empty\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n1 2 3 4\n5\n",
                "expected_stdout": "1 2 3 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n5\n5\n",
                "expected_stdout": "empty\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n1 1 2 2 3 3\n1\n",
                "expected_stdout": "2 2 3 3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "顺序表删除区间元素",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "顺序表",
            "删除",
            "区间"
        ],
        "statement_md": "删除顺序表中**位序**从 `i` 到 `j`（含两端）的所有元素，后面的元素整体前移。\n\n搬移方向跟插入**正好相反**：这里是**从前往后**搬（把 `j` 后面的元素往前填），写反了同样会静默出错。",
        "input_format": "第一行一个整数 `n`。\n\n第二行 `n` 个整数。\n\n第三行两个整数 `i` `j`（1 ≤ i ≤ j ≤ n）。",
        "output_format": "一行，删除后的顺序表（空格分隔）；若为空则输出 `empty`。",
        "constraints_md": "- 1 ≤ n ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 02 讲 · 线性表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nint a[1005];\nint main(void) {\n    int n, i, j;\n    scanf(\"%d\", &n);\n    for (int k = 0; k < n; k++) scanf(\"%d\", &a[k]);\n    scanf(\"%d %d\", &i, &j);\n    int cnt = j - i + 1;                     // 要删掉几个\n    for (int k = j; k < n; k++) a[k - cnt] = a[k];   // 从前往后搬\n    n -= cnt;\n    if (n == 0) { printf(\"empty\\n\"); return 0; }\n    for (int k = 0; k < n; k++) printf(\"%d%c\", a[k], k + 1 == n ? '\\n' : ' ');\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\nusing namespace std;\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    int n; cin >> n;\n    vector<int> a(n);\n    for (int &v : a) cin >> v;\n    int i, j; cin >> i >> j;\n    vector<int> out;                       // 另一套：按下标挑，不做原地搬移\n    for (int k = 0; k < n; k++)\n        if (k < i - 1 || k > j - 1) out.push_back(a[k]);\n    if (out.empty()) { cout << \"empty\\n\"; return 0; }\n    for (size_t k = 0; k < out.size(); k++)\n        cout << out[k] << (k + 1 == out.size() ? '\\n' : ' ');\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "6\n10 20 30 40 50 60\n2 4\n",
                "expected_stdout": "10 50 60\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n1 2 3 4 5\n1 5\n",
                "expected_stdout": "empty\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n1 2 3 4 5\n1 1\n",
                "expected_stdout": "2 3 4 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n1 2 3 4 5\n5 5\n",
                "expected_stdout": "1 2 3 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n9 8 7 6\n2 3\n",
                "expected_stdout": "9 6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "顺序表原地逆置",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "顺序表",
            "逆置",
            "首尾交换"
        ],
        "statement_md": "把顺序表**原地**逆置（不借第二个数组），用首尾交换向中间收拢的写法。\n\n这是考研高频题：O(n) 时间、O(1) 空间。\n\n注意循环条件是 `i < j` 而不是 `i <= j` —— 写成 `<=` 时中间那个元素会自己跟自己换一次，结果**碰巧还是对的**，于是这个错误永远暴露不出来。",
        "input_format": "第一行一个整数 `n`。\n\n第二行 `n` 个整数。",
        "output_format": "一行，逆置后的顺序表（空格分隔）。",
        "constraints_md": "- 1 ≤ n ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 02 讲 · 线性表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nint a[1005];\nint main(void) {\n    int n;\n    scanf(\"%d\", &n);\n    for (int k = 0; k < n; k++) scanf(\"%d\", &a[k]);\n    for (int i = 0, j = n - 1; i < j; i++, j--) {\n        int t = a[i]; a[i] = a[j]; a[j] = t;\n    }\n    for (int k = 0; k < n; k++) printf(\"%d%c\", a[k], k + 1 == n ? '\\n' : ' ');\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <algorithm>\nusing namespace std;\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    int n; cin >> n;\n    int a[1005];\n    for (int k = 0; k < n; k++) cin >> a[k];\n    reverse(a, a + n);                    // 另一套：直接用标准库的逆置\n    for (int k = 0; k < n; k++) cout << a[k] << (k + 1 == n ? '\\n' : ' ');\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n1 2 3 4 5\n",
                "expected_stdout": "5 4 3 2 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n1 2 3 4\n",
                "expected_stdout": "4 3 2 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n42\n",
                "expected_stdout": "42\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n7 8\n",
                "expected_stdout": "8 7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n-1 -2 -3 -4 -5 -6\n",
                "expected_stdout": "-6 -5 -4 -3 -2 -1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "合并两个有序顺序表",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "顺序表",
            "归并",
            "双指针"
        ],
        "statement_md": "把两个**非递减**顺序表合并成一个非递减顺序表。\n\n标准做法是双指针归并：谁小先输出谁，一个走完就把另一个整段接上。\n\n要求 O(n+m) —— 把两段拼起来再排序虽然结果也对，但那是 O((n+m)log)。",
        "input_format": "第一行一个整数 `n`，第二行 `n` 个非递减整数。\n\n第三行一个整数 `m`，第四行 `m` 个非递减整数。\n\n（`n` 和 `m` 都可能为 0，此时对应的那行为空行。）",
        "output_format": "一行，合并后的非递减序列（空格分隔）；两者都空则输出 `empty`。",
        "constraints_md": "- 0 ≤ n, m ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 02 讲 · 线性表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nint a[1005], b[1005], c[2010];\nint main(void) {\n    int n, m;\n    scanf(\"%d\", &n);\n    for (int k = 0; k < n; k++) scanf(\"%d\", &a[k]);\n    scanf(\"%d\", &m);\n    for (int k = 0; k < m; k++) scanf(\"%d\", &b[k]);\n    int i = 0, j = 0, t = 0;\n    while (i < n && j < m) c[t++] = (a[i] <= b[j]) ? a[i++] : b[j++];\n    while (i < n) c[t++] = a[i++];\n    while (j < m) c[t++] = b[j++];\n    if (t == 0) { printf(\"empty\\n\"); return 0; }\n    for (int k = 0; k < t; k++) printf(\"%d%c\", c[k], k + 1 == t ? '\\n' : ' ');\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <algorithm>\nusing namespace std;\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    int n; cin >> n;\n    vector<int> a(n); for (int &v : a) cin >> v;\n    int m; cin >> m;\n    vector<int> b(m); for (int &v : b) cin >> v;\n    // 另一套：先整体拼接，再用 stable_sort —— 结果同样是全局非递减\n    vector<int> c = a;\n    c.insert(c.end(), b.begin(), b.end());\n    stable_sort(c.begin(), c.end());\n    if (c.empty()) { cout << \"empty\\n\"; return 0; }\n    for (size_t k = 0; k < c.size(); k++)\n        cout << c[k] << (k + 1 == c.size() ? '\\n' : ' ');\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 3 5\n3\n2 4 6\n",
                "expected_stdout": "1 2 3 4 5 6\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n1 2 3 4\n0\n\n",
                "expected_stdout": "1 2 3 4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "0\n\n3\n7 8 9\n",
                "expected_stdout": "7 8 9\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "0\n\n0\n\n",
                "expected_stdout": "empty\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n1 1 2\n3\n1 2 2\n",
                "expected_stdout": "1 1 1 2 2 2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "单链表尾插建表并遍历",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "单链表",
            "尾插法",
            "遍历"
        ],
        "statement_md": "用**尾插法**建立带头结点的单链表，然后从头到尾遍历输出。\n\n尾插法的关键在于**始终维护一个尾指针 `rear`**：\n\n```c\ns->next = NULL;   /* 新结点自己就是尾巴，next 必须先置空 */\nrear->next = s;   /* 挂到尾巴后面 */\nrear = s;         /* 尾巴挪到新结点 */\n```\n\n★ 第一句 `s->next = NULL` **不能省**。少了它，最后一个结点的 `next` 就是 malloc 拿到的随机地址，遍历时不是打印垃圾就是段错误 —— 而且**有时正常、有时崩**，是最难查的一类 bug。\n\n输出格式：每个结点后面跟 ` -> `，最后以 `NULL` 结尾。",
        "input_format": "第一行一个整数 `n`。\n\n第二行 `n` 个整数（`n` 可以为 0）。",
        "output_format": "一行，形如 `1 -> 2 -> 3 -> NULL`；空表输出 `NULL`。",
        "constraints_md": "- 0 ≤ n ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 02 讲 · 线性表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <stdlib.h>\ntypedef struct LNode { int data; struct LNode *next; } LNode, *LinkList;\nint main(void) {\n    int n;\n    scanf(\"%d\", &n);\n    LinkList head = (LinkList)malloc(sizeof(LNode));   /* 头结点 */\n    head->next = NULL;\n    LNode *rear = head;                               /* ★ 尾指针 */\n    for (int k = 0; k < n; k++) {\n        int v; scanf(\"%d\", &v);\n        LNode *s = (LNode *)malloc(sizeof(LNode));\n        s->data = v;\n        s->next = NULL;            /* ★ 不能省，否则尾结点 next 是随机地址 */\n        rear->next = s;\n        rear = s;\n    }\n    for (LNode *p = head->next; p; p = p->next) printf(\"%d -> \", p->data);\n    printf(\"NULL\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\nusing namespace std;\ntypedef struct LNode { int data; struct LNode *next; } LNode, *LinkList;\n// 另一套：先**头插**把元素倒着接进去，再整体逆置——结果与尾插一致\nstatic LinkList insertHead(LinkList head, int v) {\n    LNode *s = new LNode(); s->data = v; s->next = head->next; head->next = s;\n    return head;\n}\nstatic void reverseList(LinkList head) {\n    LNode *p = head->next, *q = NULL;\n    while (p) { LNode *r = p->next; p->next = q; q = p; p = r; }\n    head->next = q;\n}\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    int n; cin >> n;\n    LinkList head = new LNode(); head->next = NULL;\n    for (int k = 0; k < n; k++) { int v; cin >> v; insertHead(head, v); }\n    reverseList(head);\n    for (LNode *p = head->next; p; p = p->next) cout << p->data << \" -> \";\n    cout << \"NULL\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 2 3\n",
                "expected_stdout": "1 -> 2 -> 3 -> NULL\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n10 20 30 40 50\n",
                "expected_stdout": "10 -> 20 -> 30 -> 40 -> 50 -> NULL\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "0\n\n",
                "expected_stdout": "NULL\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n7\n",
                "expected_stdout": "7 -> NULL\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n-1 0 1 2\n",
                "expected_stdout": "-1 -> 0 -> 1 -> 2 -> NULL\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "单链表删除所有值为 x 的结点",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "单链表",
            "删除",
            "双指针"
        ],
        "statement_md": "删除带头结点单链表中**所有**值为 `x` 的结点，保持其余结点次序不变。\n\n★ 关键在 `else`：**只有没删的时候 `p` 才前进**。\n\n```c\nif (p->next->data == x) { q = p->next; p->next = q->next; free(q); }\nelse p = p->next;          /* ← 删了就在原地再查一次 */\n```\n\n写成「每次都 `p = p->next`」，遇到**连续两个 `x`** 时会漏删后面那个。\n\n输出格式与上一题一致。",
        "input_format": "第一行一个整数 `n`。\n\n第二行 `n` 个整数。\n\n第三行一个整数 `x`。",
        "output_format": "一行，形如 `1 -> 3 -> NULL`；删空则输出 `NULL`。",
        "constraints_md": "- 0 ≤ n ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 02 讲 · 线性表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <stdlib.h>\ntypedef struct LNode { int data; struct LNode *next; } LNode, *LinkList;\nint main(void) {\n    int n, x;\n    scanf(\"%d\", &n);\n    LinkList head = (LinkList)malloc(sizeof(LNode));\n    head->next = NULL;\n    LNode *rear = head;\n    for (int k = 0; k < n; k++) {\n        int v; scanf(\"%d\", &v);\n        LNode *s = (LNode *)malloc(sizeof(LNode));\n        s->data = v; s->next = NULL;\n        rear->next = s; rear = s;\n    }\n    scanf(\"%d\", &x);\n    LNode *p = head;\n    while (p->next) {\n        if (p->next->data == x) {\n            LNode *q = p->next;\n            p->next = q->next;      /* 先摘链，再 free */\n            free(q);\n        } else {\n            p = p->next;            /* ★ 删了就不前进，原地再查 */\n        }\n    }\n    for (LNode *t = head->next; t; t = t->next) printf(\"%d -> \", t->data);\n    printf(\"NULL\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\nusing namespace std;\ntypedef struct LNode { int data; struct LNode *next; } LNode, *LinkList;\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    int n; cin >> n;\n    LinkList head = new LNode(); head->next = NULL;\n    LNode *rear = head;\n    for (int k = 0; k < n; k++) {\n        int v; cin >> v;\n        LNode *s = new LNode(); s->data = v; s->next = NULL;\n        rear->next = s; rear = s;\n    }\n    int x; cin >> x;\n    // 另一套：建一条**新链表**，只把不等于 x 的结点尾插过去\n    LinkList h2 = new LNode(); h2->next = NULL;\n    LNode *r2 = h2;\n    for (LNode *p = head->next; p; p = p->next)\n        if (p->data != x) {\n            LNode *s = new LNode(); s->data = p->data; s->next = NULL;\n            r2->next = s; r2 = s;\n        }\n    for (LNode *t = h2->next; t; t = t->next) cout << t->data << \" -> \";\n    cout << \"NULL\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "6\n1 2 3 2 4 2\n2\n",
                "expected_stdout": "1 -> 3 -> 4 -> NULL\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n5 5 5\n5\n",
                "expected_stdout": "NULL\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n1 2 3 4\n9\n",
                "expected_stdout": "1 -> 2 -> 3 -> 4 -> NULL\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n7 7\n7\n",
                "expected_stdout": "NULL\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n1 1 2 1 1\n1\n",
                "expected_stdout": "2 -> NULL\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "单链表就地逆置",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "单链表",
            "逆置",
            "指针"
        ],
        "statement_md": "把带头结点的单链表**就地**逆置（不新建结点、不借数组）。\n\n经典三指针写法：`p` 走原链，`q` 攒新链，`r` 提前记住下一个。\n\n```c\nwhile (p) { r = p->next; p->next = q; q = p; p = r; }\nhead->next = q;\n```\n\n★ 顺序不能乱：**先存 `r = p->next` 再改 `p->next`**。反过来写的话，改完之后 `p->next` 已经指向新链，原来的后续结点就找不回来了。",
        "input_format": "第一行一个整数 `n`。\n\n第二行 `n` 个整数。",
        "output_format": "一行，形如 `3 -> 2 -> 1 -> NULL`；空表输出 `NULL`。",
        "constraints_md": "- 0 ≤ n ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 02 讲 · 线性表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <stdlib.h>\ntypedef struct LNode { int data; struct LNode *next; } LNode, *LinkList;\nint main(void) {\n    int n;\n    scanf(\"%d\", &n);\n    LinkList head = (LinkList)malloc(sizeof(LNode));\n    head->next = NULL;\n    LNode *rear = head;\n    for (int k = 0; k < n; k++) {\n        int v; scanf(\"%d\", &v);\n        LNode *s = (LNode *)malloc(sizeof(LNode));\n        s->data = v; s->next = NULL;\n        rear->next = s; rear = s;\n    }\n    LNode *p = head->next, *q = NULL;\n    while (p) {\n        LNode *r = p->next;     /* ★ 先记下后继，再改 next */\n        p->next = q;\n        q = p; p = r;\n    }\n    head->next = q;\n    for (LNode *t = head->next; t; t = t->next) printf(\"%d -> \", t->data);\n    printf(\"NULL\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\nusing namespace std;\ntypedef struct LNode { int data; struct LNode *next; } LNode, *LinkList;\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    int n; cin >> n;\n    // 另一套：**头插法**建表，读进来就是逆序的，不需要再逆置\n    LinkList head = new LNode(); head->next = NULL;\n    for (int k = 0; k < n; k++) {\n        int v; cin >> v;\n        LNode *s = new LNode(); s->data = v;\n        s->next = head->next; head->next = s;\n    }\n    for (LNode *t = head->next; t; t = t->next) cout << t->data << \" -> \";\n    cout << \"NULL\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n1 2 3 4 5\n",
                "expected_stdout": "5 -> 4 -> 3 -> 2 -> 1 -> NULL\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n9\n",
                "expected_stdout": "9 -> NULL\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "0\n\n",
                "expected_stdout": "NULL\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n10 20 30 40\n",
                "expected_stdout": "40 -> 30 -> 20 -> 10 -> NULL\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n-1 -2 -3 -4 -5 -6\n",
                "expected_stdout": "-6 -> -5 -> -4 -> -3 -> -2 -> -1 -> NULL\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "括号匹配",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "栈",
            "括号匹配",
            "基础应用"
        ],
        "statement_md": "给定一个只由 `()[]{}` 组成的字符串，判断括号是否**正确配对**。\n\n栈的教科书应用。三条判据缺一不可：\n\n1. 遇到**左**括号 → 压栈\n2. 遇到**右**括号 → 栈必须非空，且栈顶是**对应的左**括号\n3. 扫完之后栈必须**空**\n\n★ 最容易漏的是第 3 条：`(()` 在第 2 条上一点问题都没有，只有在收尾检查栈时才会暴露。\n\n配对输出 `yes`，否则 `no`。",
        "input_format": "一行，一个不含空格的字符串，只由 `()[]{}` 组成。",
        "output_format": "一行，`yes` 或 `no`。",
        "constraints_md": "- 字符串长度不超过 10000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 03 讲 · 栈和队列",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <string.h>\nchar s[10005], st[10005];\nint main(void) {\n    scanf(\"%s\", s);\n    int n = (int)strlen(s), top = 0;\n    for (int i = 0; i < n; i++) {\n        char c = s[i];\n        if (c == '(' || c == '[' || c == '{') {\n            st[top++] = c;\n        } else {\n            char want = (c == ')') ? '(' : (c == ']') ? '[' : '{';\n            if (top == 0 || st[top - 1] != want) { printf(\"no\\n\"); return 0; }\n            top--;\n        }\n    }\n    printf(top == 0 ? \"yes\\n\" : \"no\\n\");   /* ★ 收尾必须查栈空 */\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <string>\n#include <stack>\nusing namespace std;\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    string s; cin >> s;\n    stack<char> st;\n    bool ok = true;\n    for (char c : s) {\n        if (c == '(') st.push(')');\n        else if (c == '[') st.push(']');\n        else if (c == '{') st.push('}');\n        else {                                  // 另一套：存「期望的右括号」，比对更直接\n            if (st.empty() || st.top() != c) { ok = false; break; }\n            st.pop();\n        }\n    }\n    if (!st.empty()) ok = false;\n    cout << (ok ? \"yes\" : \"no\") << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "()\n",
                "expected_stdout": "yes\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "(]\n",
                "expected_stdout": "no\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "([{}])\n",
                "expected_stdout": "yes\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "(()\n",
                "expected_stdout": "no\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": ")(\n",
                "expected_stdout": "no\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "{[()]}\n",
                "expected_stdout": "yes\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "用栈实现进制转换",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "栈",
            "进制转换",
            "取余"
        ],
        "statement_md": "把十进制非负整数 `n` 转换成 `r` 进制（2 ≤ r ≤ 16）。\n\n转换过程是**除 r 取余、倒着读**：「倒着读」正好就是栈的后进先出，所以一边算一边压栈，最后依次弹出即可。\n\n10~15 用**大写**字母 `A`~`F` 表示。",
        "input_format": "一行，两个整数 `n` 和 `r`。",
        "output_format": "一行，`n` 的 `r` 进制表示（不含前导零；`n = 0` 输出 `0`）。",
        "constraints_md": "- 0 ≤ n ≤ 2^31-1\n- 2 ≤ r ≤ 16",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 03 讲 · 栈和队列",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nint st[64];\nint main(void) {\n    long long n; int r;\n    scanf(\"%lld %d\", &n, &r);\n    if (n == 0) { printf(\"0\\n\"); return 0; }\n    const char *D = \"0123456789ABCDEF\";\n    int top = 0;\n    while (n > 0) { st[top++] = (int)(n % r); n /= r; }\n    while (top > 0) putchar(D[st[--top]]);\n    putchar('\\n');\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <string>\nusing namespace std;\nstatic void conv(long long n, int r, string &out) {\n    // 另一套：递归。回溯时把当前位接到结果后面，天然就是「倒着读」\n    if (n == 0) return;\n    conv(n / r, r, out);\n    out += \"0123456789ABCDEF\"[n % r];\n}\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    long long n; int r; cin >> n >> r;\n    if (n == 0) { cout << \"0\\n\"; return 0; }\n    string out;\n    conv(n, r, out);\n    cout << out << \"\\n\";\n    return 0;\n}\n",
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
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1000 8\n",
                "expected_stdout": "1750\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "255 2\n",
                "expected_stdout": "11111111\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1 16\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "判断出栈序列是否合法",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "栈",
            "出栈序列",
            "模拟"
        ],
        "statement_md": "入栈序列固定为 `1, 2, 3, …, n`（按此顺序推进去），中途可以随时出栈。判断给定的序列**有没有可能**是出栈序列。\n\n判定方法是「跟着走一遍」：\n\n```c\nint p = 1;                /* 下一个要入栈的数 */\nfor (每个目标值 v) {\n    while (p <= n && (栈空 || 栈顶 != v)) 压入 p++;\n    if (栈顶 == v) 弹出; else 非法;\n}\n```\n\n结论记牢：**`n` 个元素出栈序列的个数是卡特兰数**，`n = 3` 时只有 5 种合法。\n\n合法输出 `yes`，否则 `no`。",
        "input_format": "第一行一个整数 `n`。\n\n第二行 `n` 个整数，是待判断的出栈序列。",
        "output_format": "一行，`yes` 或 `no`。",
        "constraints_md": "- 1 ≤ n ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 03 讲 · 栈和队列",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nint st[1005];\nint main(void) {\n    int n;\n    scanf(\"%d\", &n);\n    int p = 1, top = 0, ok = 1;\n    for (int i = 0; i < n; i++) {\n        int v; scanf(\"%d\", &v);\n        while (p <= n && (top == 0 || st[top - 1] != v)) st[top++] = p++;\n        if (top > 0 && st[top - 1] == v) top--;\n        else ok = 0;\n    }\n    printf(ok ? \"yes\\n\" : \"no\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <stack>\nusing namespace std;\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    int n; cin >> n;\n    vector<int> want(n);\n    for (int &v : want) cin >> v;\n    // 另一套：换一种推进节奏 —— 先按目标值压栈，再统一判断\n    stack<int> st;\n    int p = 1;\n    bool ok = true;\n    for (int i = 0; i < n && ok; i++) {\n        while (p <= n && (st.empty() || st.top() != want[i])) { st.push(p); p++; }\n        if (!st.empty() && st.top() == want[i]) st.pop();\n        else ok = false;\n    }\n    cout << (ok ? \"yes\" : \"no\") << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 2 3\n",
                "expected_stdout": "yes\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n3 2 1\n",
                "expected_stdout": "yes\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n3 1 2\n",
                "expected_stdout": "no\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n1 3 2 4\n",
                "expected_stdout": "yes\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n4 3 2 1\n",
                "expected_stdout": "yes\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n1\n",
                "expected_stdout": "yes\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n1 2 4 5 3\n",
                "expected_stdout": "yes\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "循环队列操作模拟",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "队列",
            "循环队列",
            "队满队空"
        ],
        "statement_md": "循环队列容量为 `m`，按给定顺序处理入队 / 出队操作。\n\n★ 循环队列用「牺牲一个存储单元」区分队空与队满，这是教材的经典设计：\n\n```c\n队空：(rear + 1) % m == front   /* 不对，这里容易记反 */\n队空：front == rear\n队满：(rear + 1) % m == front   /* 尾指针再走一格就顶上头指针 */\n```\n\n因为要用一个空位来区分，所以**容量 `m` 的循环队列最多只能存 `m-1` 个元素**。这点想通了，队满条件就不会记反。\n\n本机模拟时可以直接用「长度计数」，只要**输出与判据一致**即可。\n\n> [!warning] 一个专治流式输入的坑\n> `in x` 里那个 `x`，**不管队满没满都得先读进来**。\n> 只在不满的分支里读，队满时 `x` 就留在输入流里，> 下一次读操作符会把它读走 —— 后面整段输出错位，> 而现象只是「莫名其妙多打了几个 full」，极难 debug。",
        "input_format": "第一行一个整数 `m`（队列容量）。\n\n随后若干行，每行是下面三种之一：\n\n- `in x` —— 把 `x` 入队\n- `out` —— 出队\n- `end` —— 结束\n\n`out` 时若队空，输出 `empty`；`in` 时若队满，输出 `full`。",
        "output_format": "对每个 `out` 输出出队元素、对每个失败的 `in` 输出 `full`（各占一行）；\n\n最后一行输出队列中剩余元素（空格分隔），队空则输出 `empty`。",
        "constraints_md": "- 1 ≤ m ≤ 100\n- 操作数不超过 500",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 03 讲 · 栈和队列",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <string.h>\nint q[105];\nint main(void) {\n    int m;\n    scanf(\"%d\", &m);\n    int cap = m - 1;                 /* ★ 牺牲一个单元 */\n    if (cap < 0) cap = 0;\n    int front = 0, rear = 0, size = 0;   /* 用 size 计数，判据更直白 */\n    char op[16];\n    while (scanf(\"%s\", op) == 1 && strcmp(op, \"end\") != 0) {\n        if (strcmp(op, \"out\") == 0) {\n            if (size == 0) printf(\"empty\\n\");\n            else { printf(\"%d\\n\", q[front]); front = (front + 1) % m; size--; }\n        } else {\n            int x;\n            /* ★ 无论队满不满，都要先把入队元素读掉。\n               漏掉这一句（只在 else 里读），队满时那个数字就会留在输入流里，\n               下一次 scanf(\"%s\") 会把它当成一条新指令 —— 输出开始整段错位，\n               而且看起来只是「多打了几个 full」，极难定位。 */\n            scanf(\"%d\", &x);\n            if (size >= cap) printf(\"full\\n\");\n            else { q[rear] = x; rear = (rear + 1) % m; size++; }\n        }\n    }\n    if (size == 0) printf(\"empty\\n\");\n    else {\n        for (int k = 0; k < size; k++)\n            printf(\"%d%c\", q[(front + k) % m], k + 1 == size ? '\\n' : ' ');\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <string>\n#include <deque>\nusing namespace std;\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    int m; cin >> m;\n    int cap = (m - 1 < 0) ? 0 : m - 1;\n    deque<int> q;                    // 另一套：直接用双端队列，靠 size 模拟\n    string op;\n    while (cin >> op && op != \"end\") {\n        if (op == \"out\") {\n            if (q.empty()) cout << \"empty\\n\";\n            else { cout << q.front() << \"\\n\"; q.pop_front(); }\n        } else {\n            int x; cin >> x;\n            if ((int)q.size() >= cap) cout << \"full\\n\";\n            else q.push_back(x);\n        }\n    }\n    if (q.empty()) cout << \"empty\\n\";\n    else {\n        for (size_t k = 0; k < q.size(); k++)\n            cout << q[k] << (k + 1 == q.size() ? '\\n' : ' ');\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\nin 1\nin 2\nout\nin 3\nin 4\nin 5\nout\nout\nout\nend\n",
                "expected_stdout": "1\nfull\nfull\n2\n3\nempty\nempty\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\nout\nend\n",
                "expected_stdout": "empty\nempty\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\nin 5\nin 6\nin 7\nin 8\nout\nend\n",
                "expected_stdout": "full\nfull\nfull\n5\nempty\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\nin 1\nout\nin 2\nout\nend\n",
                "expected_stdout": "full\nempty\nfull\nempty\nempty\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\nin 1\nin 2\nin 3\nout\nin 9\nout\nend\n",
                "expected_stdout": "1\n2\n3 9\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "后缀表达式求值",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "栈",
            "表达式求值",
            "后缀表达式"
        ],
        "statement_md": "计算一个**后缀表达式**（也叫逆波兰式）的值。\n\n规则很简单：遇到操作数就压栈；遇到运算符就弹出**两个**操作数算一下再压回去。\n\n★ 弹出顺序不能反：**先弹出来的是右操作数**。写成 `a - b`（先弹的在前）做减法／除法时结果就错了，而加法乘法恰好看不出来 —— 这是后缀求值最隐蔽的坑。\n\n除法按 **C 语言整数除法**（向零取整，如 `-7 / 2 = -3`），保证除数非 0。",
        "input_format": "一行，若干 token 用空格分隔。token 是整数或 `+ - * /` 之一。",
        "output_format": "一行，一个整数，表达式的值。",
        "constraints_md": "- token 数不超过 1000\n- 中间结果在 64 位整数范围内",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 03 讲 · 栈和队列",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <string.h>\n#include <stdlib.h>\nlong long st[1005];\nint main(void) {\n    char tk[64];\n    int top = 0;\n    while (scanf(\"%s\", tk) == 1) {\n        if (!strcmp(tk, \"+\") || !strcmp(tk, \"-\") || !strcmp(tk, \"*\") || !strcmp(tk, \"/\")) {\n            long long b = st[--top];     /* ★ 先弹出来的是右操作数 */\n            long long a = st[--top];\n            long long v = 0;\n            if (tk[0] == '+') v = a + b;\n            else if (tk[0] == '-') v = a - b;\n            else if (tk[0] == '*') v = a * b;\n            else v = a / b;              /* C 的整除天然向零取整 */\n            st[top++] = v;\n        } else {\n            st[top++] = atoll(tk);\n        }\n    }\n    printf(\"%lld\\n\", st[top - 1]);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <string>\n#include <vector>\nusing namespace std;\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    vector<long long> st;\n    string tk;\n    while (cin >> tk) {\n        if (tk.size() == 1 && string(\"+-*/\").find(tk[0]) != string::npos) {\n            long long b = st.back(); st.pop_back();\n            long long a = st.back(); st.pop_back();\n            long long v;\n            // 另一套：先算「先弹的那个」的相反数思路 → 用 switch 显式区分左右\n            switch (tk[0]) {\n                case '+': v = a + b; break;\n                case '-': v = a - b; break;\n                case '*': v = a * b; break;\n                default:  v = a / b; break;\n            }\n            st.push_back(v);\n        } else {\n            st.push_back(stoll(tk));\n        }\n    }\n    cout << st.back() << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3 4 +\n",
                "expected_stdout": "7\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5 1 2 + 4 * + 3 -\n",
                "expected_stdout": "14\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "7 2 /\n",
                "expected_stdout": "3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2 3 4 * +\n",
                "expected_stdout": "14\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10 3 - 2 *\n",
                "expected_stdout": "14\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3 5 -\n",
                "expected_stdout": "-2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2 3 + 4 5 + *\n",
                "expected_stdout": "45\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "用栈判断回文串",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "栈",
            "回文",
            "字符串"
        ],
        "statement_md": "判断一个字符串是不是**回文**（正着读和倒着读一样）。\n\n用栈的做法：把整个串压栈，再依次弹出与原串逐字符比较。\n弹出的顺序正好是倒序，所以这就是「倒着读」。\n\n★ **大小写敏感**：`Aba` 不是回文（`A` 与 `a` 是不同的字符）。",
        "input_format": "一行，一个不含空格的字符串。",
        "output_format": "一行，`yes` 或 `no`。",
        "constraints_md": "- 串长不超过 10000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 03 讲 · 栈和队列",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <string.h>\nchar s[10005], st[10005];\nint main(void) {\n    scanf(\"%s\", s);\n    int n = (int)strlen(s), top = 0;\n    for (int i = 0; i < n; i++) st[top++] = s[i];\n    int ok = 1;\n    for (int i = 0; i < n; i++) if (st[--top] != s[i]) { ok = 0; break; }\n    printf(ok ? \"yes\\n\" : \"no\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <string>\nusing namespace std;\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    string s; cin >> s;\n    // 另一套：双指针从两头往中间夹，不用栈\n    int i = 0, j = (int)s.size() - 1;\n    bool ok = true;\n    while (i < j) { if (s[i] != s[j]) { ok = false; break; } i++; j--; }\n    cout << (ok ? \"yes\" : \"no\") << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "abcba\n",
                "expected_stdout": "yes\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "abba\n",
                "expected_stdout": "yes\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "abc\n",
                "expected_stdout": "no\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "a\n",
                "expected_stdout": "yes\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "ab\n",
                "expected_stdout": "no\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "Aba\n",
                "expected_stdout": "no\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "12321\n",
                "expected_stdout": "yes\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "汉诺塔的移动序列",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "递归",
            "汉诺塔",
            "栈"
        ],
        "statement_md": "`n` 个盘子在 `A` 柱上，要全部移到 `C` 柱，`B` 柱当辅助。每次只能移动一个盘，且大盘不能压在小盘上。\n\n递归三步（`n` 个盘从 `from` 经 `via` 到 `to`）：\n\n```c\nHanoi(n-1, from, to, via);   /* 上面 n-1 个先挪到辅助柱 */\nmove(n, from, to);           /* 最大的那个直接到位 */\nHanoi(n-1, via, from, to);   /* 再从那根辅助柱挪到目标 */\n```\n\n最少步数是 `2ⁿ - 1` —— 这是递归式 `T(n) = 2T(n-1) + 1` 的解。\n\n**递归和栈的关系**：整个递归过程完全可以用一个显式栈模拟出来，`n = 64` 时调用的深度也才 64 层，这就是「递归之所以能用栈实现」的直观例子。",
        "input_format": "一行，一个整数 `n`。",
        "output_format": "第一行一个整数，最少移动步数 `2ⁿ - 1`。\n\n随后每行一步，格式为 `X->Y`（`X`、`Y` 为 `A`/`B`/`C`）。",
        "constraints_md": "- 1 ≤ n ≤ 12",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 03 讲 · 栈和队列",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nstatic void hanoi(int n, char from, char via, char to) {\n    if (n == 0) return;\n    hanoi(n - 1, from, to, via);\n    printf(\"%c->%c\\n\", from, to);\n    hanoi(n - 1, via, from, to);\n}\nint main(void) {\n    int n;\n    scanf(\"%d\", &n);\n    printf(\"%d\\n\", (1 << n) - 1);\n    hanoi(n, 'A', 'B', 'C');\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\nusing namespace std;\n// 另一套：**不用递归**，用一个显式栈模拟调用过程\nstruct Frame { int n; char from, via, to; int stage; };\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    int n; cin >> n;\n    cout << ((1 << n) - 1) << \"\\n\";\n    Frame st[64];\n    int top = 0;\n    st[top++] = Frame{n, 'A', 'B', 'C', 0};\n    while (top > 0) {\n        Frame &f = st[top - 1];\n        if (f.n == 0) { top--; continue; }\n        if (f.stage == 0) {\n            f.stage = 1;\n            st[top++] = Frame{f.n - 1, f.from, f.to, f.via, 0};\n        } else if (f.stage == 1) {\n            f.stage = 2;\n            cout << f.from << \"->\" << f.to << \"\\n\";\n            st[top++] = Frame{f.n - 1, f.via, f.from, f.to, 0};\n        } else {\n            top--;\n        }\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "1\n",
                "expected_stdout": "1\nA->C\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n",
                "expected_stdout": "3\nA->B\nA->C\nB->C\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n",
                "expected_stdout": "7\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n",
                "expected_stdout": "15\nA->B\nA->C\nB->C\nA->B\nC->A\nC->B\nA->B\nA->C\nB->C\nB->A\nC->A\nB->C\nA->B\nA->C\nB->C\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n",
                "expected_stdout": "31\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "约瑟夫环的出列顺序",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "队列",
            "约瑟夫环",
            "模拟"
        ],
        "statement_md": "`n` 个人围成一圈，编号 `1` 到 `n`。从 1 号开始报数，报到 `k` 的人出列，然后**从他的下一个人重新从 1 报数**，直到所有人出列。\n\n用队列模拟最直观：\n\n```c\nfor (报数到 k-1 的人) { 出队 → 再从队尾入队; }   /* 报 1..k-1 的跳过 */\n第 k 个：出队 → 直接输出（不再入队）\n```\n\n★ 队列判空有两种写法：`front == rear`（不带头结点、不牺牲单元）和「牺牲一个单元」的循环队列写法。**同一个程序里不能混用**，混了就会出现「少输出一个」或「多输出一个」的静默错误。",
        "input_format": "一行，两个整数 `n` 和 `k`。",
        "output_format": "一行，`n` 个整数，按出列先后排列，空格分隔。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 1 ≤ k ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 03 讲 · 栈和队列",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#define CAP 1005\nint q[CAP];\nint main(void) {\n    int n, k;\n    scanf(\"%d %d\", &n, &k);\n    for (int i = 0; i < n; i++) q[i] = i + 1;\n    int front = 0, rear = n, cnt = n;\n    while (cnt > 0) {\n        for (int c = 1; c < k; c++) {          /* 报 1..k-1 的：出队再从队尾入队 */\n            q[rear] = q[front];\n            rear = (rear + 1) % CAP;\n            front = (front + 1) % CAP;\n        }\n        int v = q[front];                      /* 报 k 的：出队直接输出 */\n        front = (front + 1) % CAP;\n        cnt--;\n        printf(\"%d%c\", v, cnt == 0 ? '\\n' : ' ');\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\nusing namespace std;\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    int n, k; cin >> n >> k;\n    // 另一套：**不模拟报数**，直接算下一个出列者的下标（数学做法）\n    vector<int> alive;\n    for (int i = 1; i <= n; i++) alive.push_back(i);\n    size_t pos = 0;\n    for (int left = n; left > 0; left--) {\n        pos = (pos + (size_t)k - 1) % alive.size();\n        cout << alive[pos] << (left == 1 ? '\\n' : ' ');\n        alive.erase(alive.begin() + (long)pos);\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 2\n",
                "expected_stdout": "2 4 1 5 3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "7 3\n",
                "expected_stdout": "3 6 2 7 5 1 4\n",
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
                "stdin": "6 6\n",
                "expected_stdout": "6 1 3 2 5 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10 4\n",
                "expected_stdout": "4 8 2 7 3 10 9 1 6 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2 3\n",
                "expected_stdout": "1 2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "BF 模式匹配求首次位置",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "串",
            "BF算法",
            "模式匹配"
        ],
        "statement_md": "朴素模式匹配（BF，Brute Force）：在主串 `S` 中找模式串 `T` **第一次**出现的位置。\n\n找不到输出 `0`。**位置从 1 开始数**（教材口径）。\n\n★ BF 的写法里最容易错的是**失配后的回退**：\n\n```c\ni = i - j + 2;   /* 主串回到本轮起点的下一个字符 */\nj = 1;           /* 模式串从头来 */\n```\n\n写成 `i = i - j + 1` 的话，失配时会原地打转 → **死循环**。",
        "input_format": "第一行主串 `S`（不含空格）。\n\n第二行模式串 `T`（不含空格，非空）。",
        "output_format": "一行，`T` 在 `S` 中首次出现的起始位置（1 起）；不存在输出 `0`。",
        "constraints_md": "- 1 ≤ |S|, |T| ≤ 10000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 04 讲 · 串、数组和广义表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <string.h>\nchar s[10005], t[10005];\nint main(void) {\n    scanf(\"%s %s\", s, t);\n    int n = (int)strlen(s), m = (int)strlen(t);\n    int i = 0, j = 0;\n    while (i < n && j < m) {\n        if (s[i] == t[j]) { i++; j++; }\n        else { i = i - j + 1; j = 0; }   /* ★ 回退到本轮起点的下一个 */\n    }\n    printf(\"%d\\n\", j == m ? i - m + 1 : 0);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <string>\nusing namespace std;\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    string s, t;\n    cin >> s >> t;\n    // 另一套：直接用标准库的 find（KMP 实现），结果与 BF 一致\n    size_t p = s.find(t);\n    cout << (p == string::npos ? 0 : (int)p + 1) << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "abcabc\nbc\n",
                "expected_stdout": "2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "aaaa\naa\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "abc\nd\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "a\na\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "ababab\nabab\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "abcde\ncde\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "abcdef\nf\n",
                "expected_stdout": "6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "求模式串的 next 数组",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 25,
        "tags": [
            "串",
            "KMP",
            "next数组"
        ],
        "statement_md": "求模式串的 `next` 数组。这里用的是**教材（严蔚敏）的经典定义**，下标从 1 开始：\n\n- `next[1] = 0`\n- `next[j]` = 「`p[1..j-1]` 的**最长相等前后缀**长度」`+ 1`（长度可以为 0）\n\n拿 `abaabc` 手算一遍就懂了：\n\n| j | p[1..j-1] | 最长相等前后缀 | next[j] |\n|---|---|---|---|\n| 1 | — | — | 0 |\n| 2 | `a` | 无 | 1 |\n| 3 | `ab` | 无 | 1 |\n| 4 | `aba` | `a` | 2 |\n| 5 | `abaa` | `a` | 2 |\n| 6 | `abaab` | `ab` | 3 |\n\n★ 别和 `nextval`（优化后的数组）搞混 —— 那是两道题。本机实测过：`nextval` 并不是万能优化，某些串上反而会多比较几次。",
        "input_format": "一行，模式串（不含空格）。",
        "output_format": "一行，`m` 个整数，用空格分隔，依次是 `next[1]` 到 `next[m]`。",
        "constraints_md": "- 1 ≤ m ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 04 讲 · 串、数组和广义表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <string.h>\nchar p[1005];\nint nxt[1005];\nint main(void) {\n    scanf(\"%s\", p + 1);                 /* 从下标 1 开始存，与教材一致 */\n    int m = (int)strlen(p + 1);\n    nxt[1] = 0;\n    int i = 1, j = 0;\n    while (i < m) {\n        if (j == 0 || p[i] == p[j]) { i++; j++; nxt[i] = j; }\n        else j = nxt[j];\n    }\n    for (int k = 1; k <= m; k++) printf(\"%d%c\", nxt[k], k == m ? '\\n' : ' ');\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <string>\n#include <vector>\nusing namespace std;\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    string p; cin >> p;\n    int m = (int)p.size();\n    // 另一套：对每个 j 直接**暴力枚举**候选长度（O(m^3)，m 小就够用）\n    vector<int> nxt(m + 1, 0);\n    nxt[1] = 0;\n    for (int j = 2; j <= m; j++) {\n        int best = 0;\n        for (int L = 1; L < j - 1; L++) {\n            bool same = true;\n            for (int k = 0; k < L; k++)\n                if (p[k] != p[j - 1 - L + k]) { same = false; break; }\n            if (same) best = L;\n        }\n        nxt[j] = best + 1;\n    }\n    for (int k = 1; k <= m; k++) cout << nxt[k] << (k == m ? '\\n' : ' ');\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "abaabc\n",
                "expected_stdout": "0 1 1 2 2 3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "aaaa\n",
                "expected_stdout": "0 1 2 3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "ababaa\n",
                "expected_stdout": "0 1 1 2 3 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "a\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "abcabx\n",
                "expected_stdout": "0 1 1 1 2 3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "aaab\n",
                "expected_stdout": "0 1 2 3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "abcabcaa\n",
                "expected_stdout": "0 1 1 1 2 3 4 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "KMP 统计不重叠出现次数",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 25,
        "tags": [
            "串",
            "KMP",
            "计数"
        ],
        "statement_md": "统计模式串 `T` 在主串 `S` 中出现了多少次，**两次出现不允许重叠**（匹配成功后从下一个位置继续找）。\n\nKMP 的核心好处是**主串指针 `i` 永不回退**，串越长优势越明显：本机实测同一个任务 BF 比较 91001 次、KMP 只要 1901 次。\n\n★ 但 KMP 也**不是总更快**：本机实测过 `\"ab\"×400` 去匹配 `aaab`，BF 比较 1200 次、KMP 反而 1600 次 —— 因为模式串里根本没有值得跳过的前后缀。别把「KMP 一定更快」当定理记。",
        "input_format": "第一行主串 `S`（不含空格）。\n\n第二行模式串 `T`（不含空格，非空）。",
        "output_format": "一行，一个整数，不重叠出现的次数。",
        "constraints_md": "- 1 ≤ |S|, |T| ≤ 10000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 04 讲 · 串、数组和广义表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <string.h>\nchar s[10005], t[10005];\nint nxt[10005];\nint main(void) {\n    scanf(\"%s %s\", s, t);\n    int n = (int)strlen(s), m = (int)strlen(t);\n    /* ---- 建 next（0-based 存法：nxt[k] = 前 k 个字符的最长相等前后缀长度）---- */\n    nxt[0] = -1;\n    int i = 0, j = -1;\n    while (i < m) {\n        if (j == -1 || t[i] == t[j]) { i++; j++; nxt[i] = j; }\n        else j = nxt[j];\n    }\n    /* ---- 匹配：主串指针 i 永不回退 ---- */\n    int cnt = 0;\n    i = 0; j = 0;\n    while (i < n) {\n        if (j == -1 || s[i] == t[j]) { i++; j++; }\n        else j = nxt[j];\n        if (j == m) {                  /* 命中一次 */\n            cnt++;\n            i = i - m + m;             /* 不重叠：主串指针停在本次匹配之后 */\n            j = 0;                     /* 模式串从头开始 */\n        }\n    }\n    printf(\"%d\\n\", cnt);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <string>\nusing namespace std;\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    string s, t;\n    cin >> s >> t;\n    // 另一套：反复调用标准库 find（内部是 KMP/BM 之类的高效实现）\n    int cnt = 0;\n    size_t pos = 0;\n    while (true) {\n        size_t k = s.find(t, pos);\n        if (k == string::npos) break;\n        cnt++;\n        pos = k + t.size();\n    }\n    cout << cnt << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "aaaaa\naa\n",
                "expected_stdout": "2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "abcabcabc\nabc\n",
                "expected_stdout": "3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "abababa\naba\n",
                "expected_stdout": "2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "abc\nd\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "aaa\naaaa\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "aabaaab\naab\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "abcabxabcd\nabc\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "稀疏矩阵三元组快速转置",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 25,
        "tags": [
            "数组",
            "稀疏矩阵",
            "快速转置"
        ],
        "statement_md": "把稀疏矩阵的三元组顺序表**转置**：把每个元素的「行、列」对调，并且结果仍然是**行优先**排列的三元组表。\n\n朴素做法要扫两遍（对每一列都从头扫一遍全表），复杂度 `O(n·t)`。\n**快速转置**只扫一遍，靠两张辅助表：\n\n- `num[col]` —— 原矩阵第 `col` 列有几个非零元\n- `cpot[col]` —— 该列的第一个非零元在转置结果里应该放的**起始位置**\n\n```c\ncpot[1] = 1;\ncpot[col] = cpot[col-1] + num[col-1];   /* 前缀和 */\n```\n\n★ 最隐蔽的错误是**忘了 `cpot[col]++`** —— 同一列有多个元素时它们会挤在同一个位置，后写的把先写的**静默覆盖**掉，输出少几行、一个报错都没有。",
        "input_format": "第一行三个整数 `r` `c` `t`：原矩阵行数、列数、非零元个数。\n\n随后 `t` 行，每行三个整数 `row col value`（行列下标从 **1** 开始，按**行优先**顺序给出，`value` 非零）。",
        "output_format": "第一行三个整数 `c` `r` `t`：转置后矩阵的列数、行数、非零元个数。\n\n随后 `t` 行，每行 `row col value`，按**行优先**排列。",
        "constraints_md": "- 1 ≤ r, c ≤ 1000\n- 0 ≤ t ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 04 讲 · 串、数组和广义表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nint ar[1005], ac[1005], av[1005];\nint br[1005], bc[1005], bv[1005];\nint num[1005], cpot[1005];\nint main(void) {\n    int r, c, t;\n    scanf(\"%d %d %d\", &r, &c, &t);\n    for (int k = 0; k < t; k++) scanf(\"%d %d %d\", &ar[k], &ac[k], &av[k]);\n    for (int col = 1; col <= c; col++) num[col] = 0;\n    for (int k = 0; k < t; k++) num[ac[k]]++;        /* 统计每列的非零元个数 */\n    cpot[1] = 0;                                     /* 0-based 存法 */\n    for (int col = 2; col <= c; col++) cpot[col] = cpot[col - 1] + num[col - 1];\n    for (int k = 0; k < t; k++) {\n        int col = ac[k];\n        int pos = cpot[col];\n        br[pos] = ac[k]; bc[pos] = ar[k]; bv[pos] = av[k];\n        cpot[col]++;                                 /* ★ 忘了这句就会静默覆盖 */\n    }\n    printf(\"%d %d %d\\n\", c, r, t);\n    for (int k = 0; k < t; k++) printf(\"%d %d %d\\n\", br[k], bc[k], bv[k]);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <algorithm>\nusing namespace std;\nstruct Trip { int r, c, v; };\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    int r, c, t; cin >> r >> c >> t;\n    vector<Trip> a(t);\n    for (auto &e : a) cin >> e.r >> e.c >> e.v;\n    // 另一套：不建 num/cpot，直接对调后整体排序（朴素但结果等价）\n    vector<Trip> b(t);\n    for (int k = 0; k < t; k++) b[k] = Trip{a[k].c, a[k].r, a[k].v};\n    stable_sort(b.begin(), b.end(), [](const Trip &x, const Trip &y) {\n        if (x.r != y.r) return x.r < y.r;\n        return x.c < y.c;\n    });\n    cout << c << \" \" << r << \" \" << t << \"\\n\";\n    for (const auto &e : b) cout << e.r << \" \" << e.c << \" \" << e.v << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3 4 3\n1 1 5\n2 3 7\n3 2 9\n",
                "expected_stdout": "4 3 3\n1 1 5\n2 3 9\n3 2 7\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 3 4\n1 1 1\n1 3 2\n2 2 3\n3 1 4\n",
                "expected_stdout": "3 3 4\n1 1 1\n1 3 4\n2 2 3\n3 1 2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2 2 0\n",
                "expected_stdout": "2 2 0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1 5 2\n1 2 8\n1 4 6\n",
                "expected_stdout": "5 1 2\n2 1 8\n4 1 6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4 1 2\n2 1 3\n4 1 7\n",
                "expected_stdout": "1 4 2\n1 2 3\n1 4 7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3 3 1\n2 2 9\n",
                "expected_stdout": "3 3 1\n2 2 9\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "对称矩阵压缩存储的下标计算",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "数组",
            "对称矩阵",
            "压缩存储",
            "下标计算"
        ],
        "statement_md": "`n` 阶**对称矩阵** `A`，满足 `A[i][j] = A[j][i]`，只需要存**下三角（含对角线）**，共 `n(n+1)/2` 个元素，按**行优先**塞进一维数组 `sa`。\n\n已知 `i`、`j`（都从 1 开始），求对应的一维下标 `k`（也从 1 开始）：\n\n```c\nif (i >= j) k = i * (i - 1) / 2 + j;   /* 在下三角，直接算 */\nelse        k = j * (j - 1) / 2 + i;   /* 在上三角，用对称性换成 A[j][i] */\n```\n\n★ 理解的关键是 `i(i-1)/2` 这一项：它是**前面 `i-1` 行元素的总个数**（第 1 行 1 个、第 2 行 2 个……累加起来就是 `1+2+…+(i-1)`）。\n\n注意 `i` 和 `j` 谁大谁小：写反了不会报错，只会静默算出一个错的 `k`。",
        "input_format": "第一行一个整数 `n`。\n\n第二行一个整数 `q`（查询个数）。\n\n随后 `q` 行，每行两个整数 `i` `j`（1 ≤ i, j ≤ n）。",
        "output_format": "`q` 行，每行一个整数，表示对应的一维下标 `k`。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 1 ≤ q ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 04 讲 · 串、数组和广义表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nint main(void) {\n    int n, q;\n    scanf(\"%d %d\", &n, &q);\n    for (int k = 0; k < q; k++) {\n        int i, j;\n        scanf(\"%d %d\", &i, &j);\n        int idx = (i >= j) ? (i * (i - 1) / 2 + j) : (j * (j - 1) / 2 + i);\n        printf(\"%d\\n\", idx);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\nusing namespace std;\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    int n, q; cin >> n >> q;\n    while (q--) {\n        int i, j; cin >> i >> j;\n        // 另一套：先按对称性把下标换成「大行小列」，再老实累加前面几行的个数\n        int a = (i > j) ? i : j;\n        int b = (i < j) ? i : j;\n        int base = 0;\n        for (int row = 1; row < a; row++) base += row;\n        cout << base + b << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4\n6\n3 2\n2 3\n1 1\n4 4\n1 4\n2 2\n",
                "expected_stdout": "5\n5\n1\n10\n7\n3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n1\n1 1\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n4\n5 5\n5 1\n1 5\n3 4\n",
                "expected_stdout": "15\n11\n11\n9\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n3\n1 2\n2 1\n3 3\n",
                "expected_stdout": "2\n2\n6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "求广义表的深度",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 25,
        "tags": [
            "广义表",
            "深度",
            "递归"
        ],
        "statement_md": "求广义表的**深度**。教材口径：\n\n- **原子**（单个元素）的深度是 `0`\n- **空表** `()` 的深度是 `1`\n- 表的深度 = `1 + 各元素的深度的最大值`\n\n举例：\n\n| 广义表 | 深度 | 理由 |\n|---|---|---|\n| `a` | 0 | 原子 |\n| `()` | 1 | 空表 |\n| `(a)` | 1 | 1 + max(0) |\n| `(a,b)` | 1 | 1 + max(0,0) |\n| `((a))` | 2 | 1 + (1 + 0) |\n| `(a,(b,c))` | 2 | 1 + max(0, 1) |\n\n★ 换算成一个**等价判据**：广义表的深度正好等于**括号的最大嵌套层数**。`(())` 嵌套 2 层、深度 2；`()` 嵌套 1 层、深度 1 —— 因为空表算 1 层。内部用递归解析也行，但两条路都得走通才算真懂。",
        "input_format": "一行，一个合法的广义表（元素为单个字母，表用逗号分隔、用括号括起）。",
        "output_format": "一行，一个整数，广义表的深度。",
        "constraints_md": "- 长度不超过 1000\n- 嵌套层数不超过 100",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 04 讲 · 串、数组和广义表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <string.h>\nchar s[1005];\nint pos;\nstatic int parse(void) {\n    if (s[pos] != '(') { pos++; return 0; }      /* 原子：深度 0 */\n    pos++;                                       /* 跳过 '(' */\n    if (s[pos] == ')') { pos++; return 1; }      /* 空表：深度 1 */\n    int inner = 0;\n    while (1) {\n        int d = parse();\n        if (d > inner) inner = d;\n        if (s[pos] == ',') { pos++; continue; }\n        break;\n    }\n    pos++;                                       /* 跳过 ')' */\n    return 1 + inner;\n}\nint main(void) {\n    scanf(\"%s\", s);\n    pos = 0;\n    printf(\"%d\\n\", parse());\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <string>\nusing namespace std;\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    string s; cin >> s;\n    // 另一套：**完全不解析**，只数括号的最大嵌套层数\n    int d = 0, mx = 0;\n    for (char ch : s) {\n        if (ch == '(') { d++; if (d > mx) mx = d; }\n        else if (ch == ')') d--;\n    }\n    cout << mx << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "a\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "()\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "(a)\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "(a,b)\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "((a))\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "(a,(b,c))\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "((),())\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "((a),(b,((c))))\n",
                "expected_stdout": "4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "反复删除所有指定子串",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "串",
            "删除子串",
            "循环处理"
        ],
        "statement_md": "从主串 `S` 中删除**所有**出现的子串 `T`。\n\n★ 注意是**反复删**：删完之后如果又拼出了新的 `T`，还要接着删，一直删到不再出现为止。\n\n例如 `S = aabbcc`、`T = ab`：\n第一次删掉中间的 `ab` 得到 `abcc`（这里又出现了一个 `ab`）→ 删掉得到 `cc` → 结束。\n\n删空则输出 `empty`。",
        "input_format": "第一行主串 `S`（不含空格）。\n\n第二行子串 `T`（不含空格，非空）。",
        "output_format": "一行，删除后的字符串；若为空输出 `empty`。",
        "constraints_md": "- 1 ≤ |S|, |T| ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 04 讲 · 串、数组和广义表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <string.h>\nchar s[1005], t[1005];\nint main(void) {\n    scanf(\"%s %s\", s, t);\n    int m = (int)strlen(t);\n    int changed = 1;\n    while (changed) {\n        changed = 0;\n        char *p;\n        while ((p = strstr(s, t)) != NULL) {          /* strstr 返回首次出现的指针 */\n            changed = 1;\n            /* 把 p+m 起的部分（含结尾 '\\0'）搬到 p 处 */\n            memmove(p, p + m, strlen(p + m) + 1);\n        }\n    }\n    printf(\"%s\\n\", s[0] ? s : \"empty\");\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <string>\nusing namespace std;\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    string s, t;\n    cin >> s >> t;\n    // 另一套：手写扫描 —— 用一个「结果串 + 待处理位置」的循环\n    string out;\n    size_t i = 0;\n    while (i < s.size()) {\n        if (i + t.size() <= s.size() && s.compare(i, t.size(), t) == 0) { i += t.size(); }\n        else {\n            out += s[i++];\n            // 新加进来的字符可能和 out 的尾巴拼出 t → 回头检查一次\n            while (out.size() >= t.size() &&\n                   out.compare(out.size() - t.size(), t.size(), t) == 0)\n                out.erase(out.size() - t.size());\n        }\n    }\n    cout << (out.empty() ? \"empty\" : out) << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "aaa\naa\n",
                "expected_stdout": "a\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "aabbaabb\naabb\n",
                "expected_stdout": "empty\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "abcabc\nabc\n",
                "expected_stdout": "empty\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "hello\nl\n",
                "expected_stdout": "heo\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "abcabc\nxyz\n",
                "expected_stdout": "abcabc\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "ababab\nab\n",
                "expected_stdout": "empty\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "aabbcc\nab\n",
                "expected_stdout": "cc\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "前序建二叉树并输出中序",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "二叉树",
            "前序建树",
            "中序遍历"
        ],
        "statement_md": "按**带空标记的前序序列**建立二叉树（`#` 表示空子树），然后输出**中序**遍历。\n\n例如 `AB#D##C##`：\n\n```text\n        A\n       / \\\n      B   C\n       \\\n        D\n```\n\n中序（左-根-右）得到 `BDAC`。\n\n★ 建树时最容易踩的坑：递归里**每个 `#` 也要吃掉一个字符位置**（`i` 必须往后走），否则整棵树会错位 —— 而且错得很隐蔽，本机实测过：漏了它重建出来的是一棵**看起来很像、其实完全不同**的树。",
        "input_format": "一行，带空标记的前序序列（结点为大写字母，`#` 表示空）。",
        "output_format": "一行，中序遍历的结点序列（无分隔符）；空树输出 `empty`。",
        "constraints_md": "- 序列长度不超过 2000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 05 讲 · 树和二叉树",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <string.h>\n#include <stdlib.h>\ntypedef struct BTNode { char data; struct BTNode *l, *r; } BTNode;\nchar s[2005];\nint pos;\nstatic BTNode *build(void) {\n    char c = s[pos++];                      /* ★ 空标记也要吃掉一个位置 */\n    if (c == '#' || c == '\\0') return NULL;\n    BTNode *t = (BTNode *)malloc(sizeof(BTNode));\n    t->data = c;\n    t->l = build();\n    t->r = build();\n    return t;\n}\nstatic int any = 0;\nstatic void inorder(BTNode *t) {\n    if (!t) return;\n    inorder(t->l);\n    putchar(t->data); any = 1;\n    inorder(t->r);\n}\nint main(void) {\n    scanf(\"%s\", s);\n    pos = 0;\n    BTNode *root = build();\n    inorder(root);\n    if (!any) printf(\"empty\");\n    putchar('\\n');\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <string>\n#include <vector>\n#include <functional>\nusing namespace std;\nstruct Node { char c; int l, r; };\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    string s; cin >> s;\n    // 另一套：结点存 vector（下标代替指针），中序用**显式栈**迭代做（不写递归）\n    vector<Node> pool;\n    int pos = 0;\n    function<int()> build = [&]() -> int {\n        char c = s[pos++];\n        if (c == '#' || pos > (int)s.size()) return -1;\n        int id = (int)pool.size();\n        pool.push_back(Node{c, -1, -1});\n        int l = build(), r = build();\n        pool[id].l = l; pool[id].r = r;\n        return id;\n    };\n    int root = build();\n    string out;\n    // 迭代中序：一路向左压栈，弹出即访问，再转向右\n    vector<int> st;\n    int cur = root;\n    while (cur != -1 || !st.empty()) {\n        while (cur != -1) { st.push_back(cur); cur = pool[cur].l; }\n        cur = st.back(); st.pop_back();\n        out += pool[cur].c;\n        cur = pool[cur].r;\n    }\n    cout << (out.empty() ? \"empty\" : out) << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "AB#D##C##\n",
                "expected_stdout": "BDAC\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "A##\n",
                "expected_stdout": "A\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "AB##C##\n",
                "expected_stdout": "BAC\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "#\n",
                "expected_stdout": "empty\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "ABC####\n",
                "expected_stdout": "CBA\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "ABD##E##C#F##\n",
                "expected_stdout": "DBEACF\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "求二叉树的深度",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "二叉树",
            "深度",
            "递归"
        ],
        "statement_md": "求二叉树的**深度**（根到最远叶子的结点层数，只有根时深度为 1，空树为 0）。\n\n递归式：`depth(t) = 1 + max(depth(左), depth(右))`，空树返回 0。\n\n★ **空树的深度是 0，不是 1** —— 这一点只在输入就是 `#` 的时候才会暴露。本机实测过：把这个基准情况写成 1，所有非空树的答案照样正确，只有空树悄悄多出 1，非常容易漏测。",
        "input_format": "一行，带空标记的前序序列。",
        "output_format": "一行，一个整数，树的深度。",
        "constraints_md": "- 序列长度不超过 2000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 05 讲 · 树和二叉树",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <string.h>\nchar s[2005];\nint pos, any = 0;\nstatic int depth(void) {\n    char c = s[pos++];\n    if (c == '#' || c == '\\0') return 0;     /* ★ 空树深度 0 */\n    int dl = depth(), dr = depth();\n    any = 1;\n    return 1 + (dl > dr ? dl : dr);\n}\nint main(void) {\n    scanf(\"%s\", s);\n    pos = 0;\n    printf(\"%d\\n\", depth());\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <string>\n#include <vector>\n#include <functional>\nusing namespace std;\nstruct Node { char c; int l, r; };\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    string s; cin >> s;\n    // 另一套：结点存 vector，深度用「反复收敛」算 —— 不写递归求深度\n    vector<Node> pool;\n    int pos = 0;\n    function<int()> build = [&]() -> int {\n        char c = s[pos++];\n        if (c == '#' || pos > (int)s.size()) return -1;\n        int id = (int)pool.size();\n        pool.push_back(Node{c, -1, -1});\n        int l = build(), r = build();\n        pool[id].l = l; pool[id].r = r;\n        return id;\n    };\n    int root = build();\n    if (root < 0) { cout << 0 << \"\\n\"; return 0; }\n    // 父结点的编号恒小于孩子（先创建父），所以**倒着扫一遍**就够了\n    vector<int> h(pool.size(), 0);\n    for (int i = (int)pool.size() - 1; i >= 0; i--) {\n        int a = (pool[i].l < 0) ? 0 : h[pool[i].l];\n        int b = (pool[i].r < 0) ? 0 : h[pool[i].r];\n        h[i] = 1 + (a > b ? a : b);\n    }\n    cout << h[root] << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "AB#D##C##\n",
                "expected_stdout": "3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "A##\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "#\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "ABC####\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "A#B#C#D###\n",
                "expected_stdout": "4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "ABD##E##C#F##\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "统计二叉树的结点数与叶子数",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "二叉树",
            "结点数",
            "叶子"
        ],
        "statement_md": "统计二叉树的**结点总数**和**叶子结点数**。\n\n叶子 = 左、右孩子都为空的结点。\n\n★ 别忘了空树：空树的结点数和叶子数**都是 0**，而且 0 个结点的树也没有叶子 —— 这两句话看着像废话，但写成代码时把「根为空」的基准情况漏掉，空输入就会崩。",
        "input_format": "一行，带空标记的前序序列。",
        "output_format": "一行，两个整数，用空格分隔：结点总数 叶子数。",
        "constraints_md": "- 序列长度不超过 2000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 05 讲 · 树和二叉树",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <string.h>\n#include <stdlib.h>\ntypedef struct BTNode { char data; struct BTNode *l, *r; } BTNode;\nchar s[2005];\nint pos, total = 0, leaves = 0;\nstatic BTNode *build(void) {\n    char c = s[pos++];\n    if (c == '#' || c == '\\0') return NULL;\n    BTNode *t = (BTNode *)malloc(sizeof(BTNode));\n    t->data = c;\n    t->l = build();\n    t->r = build();\n    return t;\n}\nstatic void count(BTNode *t) {\n    if (!t) return;\n    total++;\n    if (!t->l && !t->r) leaves++;      /* 左右都空 → 叶子 */\n    count(t->l);\n    count(t->r);\n}\nint main(void) {\n    scanf(\"%s\", s);\n    pos = 0;\n    BTNode *root = build();\n    count(root);\n    printf(\"%d %d\\n\", total, leaves);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <string>\n#include <vector>\n#include <functional>\nusing namespace std;\nstruct Node { char c; int l, r; };\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    string s; cin >> s;\n    // 另一套：结点存进 vector（下标代替指针），统计用后序回溯一次算完\n    vector<Node> pool;\n    int pos = 0;\n    function<int()> build = [&]() -> int {\n        char c = s[pos++];\n        if (c == '#' || pos > (int)s.size()) return -1;\n        int id = (int)pool.size();\n        pool.push_back(Node{c, -1, -1});\n        int l = build(), r = build();\n        pool[id].l = l; pool[id].r = r;\n        return id;\n    };\n    int root = build();\n    if (root < 0) { cout << \"0 0\\n\"; return 0; }\n    // 倒着扫 pool（父结点一定先于孩子被创建，所以逆序就是后序）\n    vector<int> n(pool.size(), 0), lf(pool.size(), 0);\n    for (int i = (int)pool.size() - 1; i >= 0; i--) {\n        int a = (pool[i].l < 0) ? 0 : n[pool[i].l];\n        int b = (pool[i].r < 0) ? 0 : n[pool[i].r];\n        n[i] = 1 + a + b;\n        if (a + b == 0) lf[i] = 1;\n        else lf[i] = (pool[i].l < 0 ? 0 : lf[pool[i].l]) + (pool[i].r < 0 ? 0 : lf[pool[i].r]);\n    }\n    cout << n[root] << \" \" << lf[root] << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "AB#D##C##\n",
                "expected_stdout": "4 2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "A##\n",
                "expected_stdout": "1 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "#\n",
                "expected_stdout": "0 0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "ABC####\n",
                "expected_stdout": "3 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "AB##C##\n",
                "expected_stdout": "3 2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "ABD##E##C#F##\n",
                "expected_stdout": "6 3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "二叉树的层次遍历",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "二叉树",
            "层次遍历",
            "队列"
        ],
        "statement_md": "输出二叉树的**层次遍历**序列（从上到下、从左到右，逐层输出）。\n\n层次遍历靠的是**队列**：根入队 → 出队一个就把它**非空**的左右孩子入队 → 直到队空。\n\n★ 这里再次体现「队列判空」的重要性：入队时如果**把空结点也塞进去**，队就会一直非空，程序**永远停不下来**。所以要么入队前判空，要么出队后跳过空结点并额外记录「已产出几个」。",
        "input_format": "一行，带空标记的前序序列。",
        "output_format": "一行，层次遍历的结点序列（无分隔符）；空树输出 `empty`。",
        "constraints_md": "- 序列长度不超过 2000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 05 讲 · 树和二叉树",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <string.h>\n#include <stdlib.h>\ntypedef struct BTNode { char data; struct BTNode *l, *r; } BTNode;\nchar s[2005];\nint pos;\nBTNode *build(void) {\n    char c = s[pos++];\n    if (c == '#' || c == '\\0') return NULL;\n    BTNode *t = (BTNode *)malloc(sizeof(BTNode));\n    t->data = c;\n    t->l = build();\n    t->r = build();\n    return t;\n}\nint main(void) {\n    scanf(\"%s\", s);\n    pos = 0;\n    BTNode *root = build();\n    if (!root) { printf(\"empty\\n\"); return 0; }\n    BTNode *q[2005];\n    int front = 0, rear = 0;\n    q[rear++] = root;\n    while (front < rear) {\n        BTNode *t = q[front++];\n        putchar(t->data);\n        if (t->l) q[rear++] = t->l;      /* ★ 只把非空的入队，否则永不终止 */\n        if (t->r) q[rear++] = t->r;\n    }\n    putchar('\\n');\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <string>\n#include <vector>\n#include <functional>\n#include <queue>\nusing namespace std;\nstruct Node { char c; int l, r; };\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    string s; cin >> s;\n    // 另一套：vector 池 + std::queue，并且把**空结点也入队**再跳过\n    vector<Node> pool;\n    int pos = 0;\n    function<int()> build = [&]() -> int {\n        char c = s[pos++];\n        if (c == '#' || pos > (int)s.size()) return -1;\n        int id = (int)pool.size();\n        pool.push_back(Node{c, -1, -1});\n        int l = build(), r = build();\n        pool[id].l = l; pool[id].r = r;\n        return id;\n    };\n    int root = build();\n    if (root < 0) { cout << \"empty\\n\"; return 0; }\n    string out;\n    queue<int> q;\n    q.push(root);\n    while (!q.empty()) {\n        int id = q.front(); q.pop();\n        if (id < 0) continue;                    // ★ 空的直接跳过\n        out += pool[id].c;\n        q.push(pool[id].l);                      // 空孩子也入队 —— 靠上面那句跳过\n        q.push(pool[id].r);\n    }\n    cout << out << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "AB#D##C##\n",
                "expected_stdout": "ABCD\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "AB##C##\n",
                "expected_stdout": "ABC\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "#\n",
                "expected_stdout": "empty\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "A##\n",
                "expected_stdout": "A\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "ABC####\n",
                "expected_stdout": "ABC\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "ABD##E##C#F##\n",
                "expected_stdout": "ABCDEF\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "由先序和中序序列求后序",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 25,
        "tags": [
            "二叉树",
            "重建",
            "遍历序列"
        ],
        "statement_md": "给定二叉树的**先序**和**中序**遍历序列（结点互不相同），求**后序**序列。\n\n核心只有一句话：**先序的第一个元素就是根**，拿着这个根去中序里一劈两半，左边是左子树、右边是右子树，然后递归。\n\n```text\n先序: A B D E C\n中序: D B E A C\n根 A → 中序里 A 左边是 DBE（左子树）、右边是 C（右子树）\n后序: D E B C A\n```\n\n★ 只给「先序 + 后序」是**推不出唯一二叉树**的；必须是「先序 + 中序」或者「后序 + 中序」。",
        "input_format": "第一行先序序列。\n\n第二行中序序列。\n\n（两行都是不含分隔符的字符串，长度相同。）",
        "output_format": "一行，后序遍历的结点序列。",
        "constraints_md": "- 结点数不超过 1000\n- 结点用不重复的大写字母表示",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 05 讲 · 树和二叉树",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <string.h>\nchar pre[1005], ino[1005];\nint idx[256];\nstatic void solve(int pl, int pr, int il, int ir) {\n    if (pl > pr) return;\n    int k = idx[(unsigned char)pre[pl]];      /* 根在中序里的位置 */\n    int ln = k - il;                          /* 左子树结点个数 */\n    solve(pl + 1, pl + ln, il, k - 1);        /* 左 */\n    solve(pl + ln + 1, pr, k + 1, ir);        /* 右 */\n    putchar(pre[pl]);                         /* 根（后序最后输出） */\n}\nint main(void) {\n    scanf(\"%s %s\", pre, ino);\n    int n = (int)strlen(pre);\n    for (int i = 0; i < n; i++) idx[(unsigned char)ino[i]] = i;\n    solve(0, n - 1, 0, n - 1);\n    putchar('\\n');\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <string>\n#include <vector>\nusing namespace std;\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    string pre, ino; cin >> pre >> ino;\n    int n = (int)pre.size();\n    int idx[256] = {0};\n    for (int i = 0; i < n; i++) idx[(unsigned char)ino[i]] = i;\n    // 另一套：**从后往前**把后序填进数组 —— 先放根，再走右子树、再走左子树\n    vector<char> post(n);\n    int pi = n;\n    struct R {\n        string &pre; int *idx; vector<char> &post; int &pi;\n        void go(int pl, int pr, int il, int ir) {\n            if (pl > pr) return;\n            int k = idx[(unsigned char)pre[pl]];\n            int ln = k - il;\n            post[--pi] = pre[pl];                       // 根排在本段末尾\n            go(pl + ln + 1, pr, k + 1, ir);             // ★ 倒填 → 先右后左\n            go(pl + 1, pl + ln, il, k - 1);\n        }\n    } rec{pre, idx, post, pi};\n    rec.go(0, n - 1, 0, n - 1);\n    for (char c : post) cout << c;\n    cout << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "ABDEC\nDBEAC\n",
                "expected_stdout": "DEBCA\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "A\nA\n",
                "expected_stdout": "A\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "ABC\nBAC\n",
                "expected_stdout": "BCA\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "AB\nAB\n",
                "expected_stdout": "BA\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "AB\nBA\n",
                "expected_stdout": "BA\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "ABC\nACB\n",
                "expected_stdout": "CBA\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "ABCDEFG\nCBDAFEG\n",
                "expected_stdout": "CDBFGEA\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "判断一棵二叉树是否为完全二叉树",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 25,
        "tags": [
            "二叉树",
            "完全二叉树",
            "层次遍历"
        ],
        "statement_md": "判断给定的二叉树是不是**完全二叉树**。\n\n完全二叉树的定义：**按层序编号后，编号与满二叉树一一对应，中间不能缺号**。\n\n判定方法是层次遍历的一个小改造：\n\n1. 把结点**连同空孩子一起**按层序排开\n2. 一旦遇到第一个空结点，**后面不允许再出现非空结点**\n\n这个判据一句话就够用：**空结点出现之后，全是空结点**。\n\n举例：`A(∅, B)`（结点 B 只有右孩子，左边是空的）—— 排开后 `A, ∅, B`，空结点后面又冒出 B，所以**不是**完全二叉树。",
        "input_format": "一行，带空标记的前序序列。",
        "output_format": "一行，`yes` 或 `no`（空树视为完全二叉树）。",
        "constraints_md": "- 序列长度不超过 2000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 05 讲 · 树和二叉树",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <string.h>\n#include <stdlib.h>\ntypedef struct BTNode { char data; struct BTNode *l, *r; } BTNode;\nchar s[2005];\nint pos;\nBTNode *build(void) {\n    char c = s[pos++];\n    if (c == '#' || c == '\\0') return NULL;\n    BTNode *t = (BTNode *)malloc(sizeof(BTNode));\n    t->data = c; t->l = build(); t->r = build();\n    return t;\n}\nint main(void) {\n    scanf(\"%s\", s);\n    pos = 0;\n    BTNode *root = build();\n    if (!root) { printf(\"yes\\n\"); return 0; }\n    BTNode *q[4005];                 /* ★ 空结点也要入队，所以容量翻倍 */\n    int front = 0, rear = 0, seenNull = 0;\n    q[rear++] = root;\n    while (front < rear) {\n        BTNode *t = q[front++];\n        if (!t) { seenNull = 1; continue; }\n        if (seenNull) { printf(\"no\\n\"); return 0; }\n        q[rear++] = t->l;            /* 空孩子照样入队 */\n        q[rear++] = t->r;\n    }\n    printf(\"yes\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <string>\n#include <vector>\nusing namespace std;\nstruct Node { char c; int l = -1, r = -1; };\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    string s; cin >> s;\n    vector<Node> pool;\n    int pos = 0;\n    struct R {\n        string &s; vector<Node> &pool; int &pos;\n        int build() {\n            char c = s[pos++];\n            if (c == '#' || pos > (int)s.size()) return -1;\n            int id = (int)pool.size();\n            pool.push_back(Node{c, -1, -1});\n            int l = build(), r = build();\n            pool[id].l = l; pool[id].r = r;\n            return id;\n        }\n    } rec{s, pool, pos};\n    int root = rec.build();\n    if (root < 0) { cout << \"yes\\n\"; return 0; }\n    // 另一套：**不用队列**，按完全二叉树的编号性质检查\n    // 完全二叉树存在 ⇔ 层序编号 1..n 连续且每层填满\n    vector<int> q{root};\n    bool ok = true;\n    for (size_t i = 0; i < q.size() && ok; i++) {\n        int id = q[i];\n        if (id < 0) {                       // 遇到空位：后面必须全空\n            for (size_t j = i + 1; j < q.size(); j++)\n                if (q[j] >= 0) { ok = false; break; }\n            if (i + 1 >= q.size()) break;   // 空位之后还没展开，继续看\n            break;\n        }\n        q.push_back(pool[id].l);\n        q.push_back(pool[id].r);\n    }\n    cout << (ok ? \"yes\" : \"no\") << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "A##\n",
                "expected_stdout": "yes\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "AB##C##\n",
                "expected_stdout": "yes\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "A#B##\n",
                "expected_stdout": "no\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "AB#D##C##\n",
                "expected_stdout": "no\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "AB##\n",
                "expected_stdout": "yes\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "#\n",
                "expected_stdout": "yes\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "ABC####\n",
                "expected_stdout": "no\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "哈夫曼树的带权路径长度",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 25,
        "tags": [
            "哈夫曼树",
            "WPL",
            "贪心"
        ],
        "statement_md": "给定 `n` 个权值，求构造出的**哈夫曼树**的**带权路径长度 WPL**。\n\n构造方法是贪心：**每次取两个最小的合并**，新结点权值为两者之和，再放回去，重复到只剩一个结点。\n\n求 WPL 有个**非常省事的等价算法**：\n\n> WPL = **所有内部结点（新合成的结点）权值之和**\n\n因为每合并一次，那个新结点就代表「这批叶子整体多走一层」，累加起来正好等于 Σ(权值 × 层数)。不用去建树、也不用算每个叶子的深度。\n\n本机实测过：`1 2 3 4 5` → 合并过程 3、6、9、15，WPL = 3+6+9+15 = **33**。",
        "input_format": "第一行一个整数 `n`。\n\n第二行 `n` 个正整数，表示各叶子结点的权值。",
        "output_format": "一行，一个整数，WPL。（`n = 1` 时 WPL 为 `0`。）",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 权值 ≤ 10^9",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 05 讲 · 树和二叉树",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <queue>\n#include <vector>\nusing namespace std;\nint main(void) {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    priority_queue<long long, vector<long long>, greater<long long> > pq;\n    for (int i = 0; i < n; i++) {\n        long long v; scanf(\"%lld\", &v);\n        pq.push(v);\n    }\n    long long wpl = 0;\n    while (pq.size() > 1) {\n        long long a = pq.top(); pq.pop();\n        long long b = pq.top(); pq.pop();\n        wpl += a + b;              /* ★ 内部结点权值累加即可 */\n        pq.push(a + b);\n    }\n    printf(\"%lld\\n\", wpl);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <algorithm>\nusing namespace std;\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    int n; cin >> n;\n    vector<long long> w(n);\n    for (auto &v : w) cin >> v;\n    // 另一套：不用堆，每次**线性扫描**找两个最小的（O(n^2)，n 小够用）\n    long long wpl = 0;\n    while (w.size() > 1) {\n        size_t i1 = 0;\n        for (size_t k = 1; k < w.size(); k++) if (w[k] < w[i1]) i1 = k;\n        long long a = w[i1];\n        w.erase(w.begin() + (long)i1);\n        size_t i2 = 0;\n        for (size_t k = 1; k < w.size(); k++) if (w[k] < w[i2]) i2 = k;\n        long long b = w[i2];\n        w.erase(w.begin() + (long)i2);\n        wpl += a + b;\n        w.push_back(a + b);\n    }\n    cout << wpl << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n1 2 3 4 5\n",
                "expected_stdout": "33\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n7\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n3 5\n",
                "expected_stdout": "8\n",
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
                "stdin": "3\n5 5 5\n",
                "expected_stdout": "25\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n1 2 3 4 5 6\n",
                "expected_stdout": "51\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n1 2 100\n",
                "expected_stdout": "106\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "并查集统计连通块",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "并查集",
            "连通块",
            "路径压缩"
        ],
        "statement_md": "`n` 个点和 `m` 条无向边，求**连通块个数**，并回答若干「两点是否连通」的询问。\n\n并查集的两个优化（本机实测差距很大）：\n\n| 做法 | 找一次根要走几步 |\n|---|---|\n| 朴素合并（总把后一个挂到前一个） | 平均 **91** 步，最深 13 层 |\n| 按大小合并 | **13** 步，深 1 层 |\n| 只做路径压缩 | **25** 步，深 1 层 |\n| 两个都做 | **13** 步，深 1 层 |\n\n★ **路径压缩只在查找时把路径压平**，所以第一次查还是会长；**按大小合并**才是让树一开始就矮的关键。两者都做效果最好。\n\n输出：第一行连通块个数；随后每个询问输出 `yes` / `no`。",
        "input_format": "第一行两个整数 `n` `m`。\n\n随后 `m` 行，每行两个整数 `u` `v`，表示一条无向边（可能有自环或重复边）。\n\n接着一行一个整数 `q`（询问个数）。\n\n随后 `q` 行，每行两个整数 `u` `v`。",
        "output_format": "第一行连通块个数；随后 `q` 行，每行 `yes` 或 `no`。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 0 ≤ m ≤ 2000\n- 1 ≤ q ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 05 讲 · 树和二叉树",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nint parent[1005], sz[1005];\nstatic int find(int x) {\n    while (parent[x] != x) {\n        parent[x] = parent[parent[x]];      /* 路径压缩（隔代压缩） */\n        x = parent[x];\n    }\n    return x;\n}\nint main(void) {\n    int n, m;\n    scanf(\"%d %d\", &n, &m);\n    for (int i = 1; i <= n; i++) { parent[i] = i; sz[i] = 1; }\n    for (int k = 0; k < m; k++) {\n        int u, v;\n        scanf(\"%d %d\", &u, &v);\n        int ru = find(u), rv = find(v);\n        if (ru == rv) continue;\n        if (sz[ru] < sz[rv]) { int t = ru; ru = rv; rv = t; }  /* 按大小合并 */\n        parent[rv] = ru;\n        sz[ru] += sz[rv];\n    }\n    int comps = 0;\n    for (int i = 1; i <= n; i++) if (find(i) == i) comps++;\n    printf(\"%d\\n\", comps);\n    int q;\n    scanf(\"%d\", &q);\n    for (int k = 0; k < q; k++) {\n        int u, v;\n        scanf(\"%d %d\", &u, &v);\n        printf(find(u) == find(v) ? \"yes\\n\" : \"no\\n\");\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <queue>\nusing namespace std;\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    int n, m; cin >> n >> m;\n    // 另一套：**完全不用并查集**，直接建邻接表跑 BFS 求连通块\n    vector<vector<int>> g(n + 1);\n    for (int k = 0; k < m; k++) {\n        int u, v; cin >> u >> v;\n        g[u].push_back(v);\n        g[v].push_back(u);\n    }\n    vector<int> comp(n + 1, 0);\n    int cid = 0;\n    for (int s = 1; s <= n; s++) {\n        if (comp[s]) continue;\n        cid++;\n        queue<int> q; q.push(s); comp[s] = cid;\n        while (!q.empty()) {\n            int x = q.front(); q.pop();\n            for (int y : g[x]) if (!comp[y]) { comp[y] = cid; q.push(y); }\n        }\n    }\n    cout << cid << \"\\n\";\n    int qq; cin >> qq;\n    while (qq--) {\n        int u, v; cin >> u >> v;\n        cout << (comp[u] == comp[v] ? \"yes\" : \"no\") << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 3\n1 2\n2 3\n4 5\n2\n1 3\n1 4\n",
                "expected_stdout": "2\nyes\nno\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 0\n1\n1 1\n",
                "expected_stdout": "1\nyes\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4 0\n3\n1 2\n3 4\n1 1\n",
                "expected_stdout": "4\nno\nno\nyes\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6 5\n1 2\n2 3\n3 1\n4 5\n5 6\n2\n1 3\n1 6\n",
                "expected_stdout": "2\nyes\nno\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3 2\n1 2\n1 2\n2\n2 1\n2 3\n",
                "expected_stdout": "2\nyes\nno\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "无向图的邻接表（头插法）",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "邻接表",
            "头插法",
            "链式存储"
        ],
        "statement_md": "读入一个无向图，用**头插法**建立邻接表，然后按顶点序号 `1` ~ `n` 依次输出每个顶点的邻接点链。\n\n★ 教材的 `firstedge/nextarc` 写法就是**头插法**：后读入的边结点插到链的最前面。所以每个顶点的邻接点顺序与输入顺序**正好相反**——这也是判题的点：你要是按 `vector.push_back` 顺序输出，样例第一个就过不去。\n\n孤立顶点输出 `i:`（冒号后什么都没有，也没有空格）。",
        "input_format": "第一行 `n m`（顶点数、边数）。\n\n接下来 `m` 行，每行 `u v` 表示一条无向边（`1 ≤ u,v ≤ n`，无重边、无自环）。",
        "output_format": "`n` 行，第 `i` 行为顶点 `i` 的邻接链，格式 `i: v1 v2 ...`（邻接点按头插法顺序，即与输入顺序相反；孤立顶点输出 `i:`）。",
        "constraints_md": "- 1 ≤ n ≤ 100\n- 0 ≤ m ≤ n(n-1)/2",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 06 讲 · 图",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#define MAXN 105\n#define MAXE 4005\nint head[MAXN], nxt[MAXE], to[MAXE], ecnt = 0;\n/* 教材式头插法：新边结点插到链的最前面 */\nvoid add_edge(int u, int v) {\n    ++ecnt; to[ecnt] = v; nxt[ecnt] = head[u]; head[u] = ecnt;\n}\nint main(void) {\n    int n, m;\n    scanf(\"%d %d\", &n, &m);\n    for (int k = 0; k < m; k++) {\n        int u, v; scanf(\"%d %d\", &u, &v);\n        add_edge(u, v); add_edge(v, u);\n    }\n    for (int i = 1; i <= n; i++) {\n        printf(\"%d:\", i);\n        for (int e = head[i]; e; e = nxt[e]) printf(\" %d\", to[e]);\n        printf(\"\\n\");\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <algorithm>\nusing namespace std;\n/* 另一套：不用链表，用 vector 顺序收、输出时整体 reverse */\nint main() {\n    int n, m; cin >> n >> m;\n    vector<vector<int>> adj(n + 1);\n    for (int k = 0; k < m; k++) {\n        int u, v; cin >> u >> v;\n        adj[u].push_back(v); adj[v].push_back(u);\n    }\n    for (int i = 1; i <= n; i++) {\n        vector<int> r = adj[i];\n        reverse(r.begin(), r.end());     // 头插法的效果 = 逆输入序\n        cout << i << \":\";\n        for (int v : r) cout << \" \" << v;\n        cout << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4 5\n1 2\n1 3\n1 4\n2 3\n3 4\n",
                "expected_stdout": "1: 4 3 2\n2: 3 1\n3: 4 2 1\n4: 3 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 1\n2 3\n",
                "expected_stdout": "1:\n2: 3\n3: 2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 0\n",
                "expected_stdout": "1:\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5 6\n1 2\n2 3\n3 4\n4 5\n5 1\n2 4\n",
                "expected_stdout": "1: 5 2\n2: 4 3 1\n3: 4 2\n4: 2 5 3\n5: 1 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2 1\n1 2\n",
                "expected_stdout": "1: 2\n2: 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "无权图的最短跳数（BFS）",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "BFS",
            "队列",
            "最短路径"
        ],
        "statement_md": "给一个无权无向图和两个顶点 `s`、`t`，求从 `s` 走到 `t` 最少要经过几条边（跳数）。到不了输出 `-1`。\n\n★ BFS 是「按跳数分层」的：队列里先放跳数 0 的、再放跳数 1 的……所以**第一次摸到 `t` 时记录的跳数就是答案**。这题用的正是讲义里「BFS 副产品：最短跳数」的那套写法——用 `dist[]` 边入队边标距离，别用「出队时才标记」的反面教材。",
        "input_format": "第一行 `n m s t`（顶点数、边数、起点、终点，`s ≠ t`）。\n\n接下来 `m` 行，每行 `u v` 表示一条无向边（无重边、无自环）。",
        "output_format": "一行，一个整数：最少跳数；不可达为 `-1`。",
        "constraints_md": "- 2 ≤ n ≤ 100\n- 0 ≤ m ≤ n(n-1)/2",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 06 讲 · 图",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <iostream>\n#include <vector>\n#include <queue>\nusing namespace std;\nint main() {\n    int n, m, s, t; cin >> n >> m >> s >> t;\n    vector<vector<int>> g(n + 1);\n    for (int k = 0; k < m; k++) {\n        int u, v; cin >> u >> v;\n        g[u].push_back(v); g[v].push_back(u);\n    }\n    vector<int> dist(n + 1, -1);\n    queue<int> q;\n    dist[s] = 0; q.push(s);              // 入队即标记\n    while (!q.empty()) {\n        int x = q.front(); q.pop();\n        for (int y : g[x])\n            if (dist[y] < 0) { dist[y] = dist[x] + 1; q.push(y); }\n    }\n    cout << dist[t] << \"\\n\";\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\nusing namespace std;\n/* 另一套：不用队列，按「层」扩展——cur 是跳数为 k 的全部顶点 */\nint main() {\n    int n, m, s, t; cin >> n >> m >> s >> t;\n    vector<vector<int>> g(n + 1);\n    for (int k = 0; k < m; k++) {\n        int u, v; cin >> u >> v;\n        g[u].push_back(v); g[v].push_back(u);\n    }\n    vector<char> seen(n + 1, 0);\n    vector<int> cur = {s};\n    seen[s] = 1;\n    int hops = 0, ans = -1;\n    while (!cur.empty()) {\n        vector<int> nxt;\n        for (int x : cur) {\n            if (x == t) { ans = hops; cur.clear(); break; }\n            for (int y : g[x]) if (!seen[y]) { seen[y] = 1; nxt.push_back(y); }\n        }\n        if (ans >= 0) break;\n        cur = nxt; hops++;\n    }\n    cout << ans << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "6 7 1 5\n1 2\n1 3\n2 4\n3 4\n4 5\n3 5\n2 6\n",
                "expected_stdout": "2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4 2 1 4\n1 2\n3 4\n",
                "expected_stdout": "-1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2 1 1 2\n1 2\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5 5 1 4\n1 2\n2 3\n3 4\n4 5\n5 1\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3 0 1 3\n",
                "expected_stdout": "-1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "单源最短路径（Dijkstra）",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "Dijkstra",
            "贪心",
            "最短路径"
        ],
        "statement_md": "给一个**边权非负**的有向图和源点 `s`，输出 `s` 到每个顶点的最短距离，到不了的输出 `-1`（`s` 到自己是 `0`）。\n\n★ Dijkstra 的贪心内核：每轮从「未定」的顶点里挑 `dist` 最小的（用不用堆都行，数据规模小，O(n²) 的教材写法就够），把它标成「已定」，再用它松驰出边。\n\n**它不能处理负权边**——讲义里给过反例（Dijkstra 会翻车而 Floyd 正确），所以本题保证所有边权 > 0。",
        "input_format": "第一行 `n m s`（顶点数、边数、源点）。\n\n接下来 `m` 行，每行 `u v w` 表示一条 `u → v`、权 `w`（1 ≤ w ≤ 100）的有向边；可能有重边（取最小即可），无自环。",
        "output_format": "一行 `n` 个整数（空格分隔）：`s` 到各顶点的最短距离；不可达为 `-1`。",
        "constraints_md": "- 1 ≤ n ≤ 50\n- 0 ≤ m ≤ n(n-1)\n- 1 ≤ w ≤ 100",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 06 讲 · 图",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <iostream>\n#include <vector>\nusing namespace std;\nint main() {\n    int n, m, s; cin >> n >> m >> s;\n    const long long INF = (long long)1e18;\n    vector<vector<long long>> w(n + 1, vector<long long>(n + 1, INF));\n    for (int k = 0; k < m; k++) {\n        int u, v; long long c; cin >> u >> v >> c;\n        if (u != v && c < w[u][v]) w[u][v] = c;\n    }\n    vector<long long> dist(n + 1, INF);\n    vector<char> done(n + 1, 0);\n    dist[s] = 0;\n    for (int round = 0; round < n; round++) {\n        int x = -1;\n        for (int i = 1; i <= n; i++)\n            if (!done[i] && dist[i] < INF && (x < 0 || dist[i] < dist[x])) x = i;\n        if (x < 0) break;\n        done[x] = 1;\n        for (int y = 1; y <= n; y++)\n            if (w[x][y] < INF && dist[x] + w[x][y] < dist[y])\n                dist[y] = dist[x] + w[x][y];\n    }\n    for (int i = 1; i <= n; i++) {\n        if (i > 1) cout << \" \";\n        if (dist[i] < INF) cout << dist[i]; else cout << -1;\n    }\n    cout << \"\\n\";\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\nusing namespace std;\n/* 另一套：Floyd 全源最短路，最后只打印 s 那一行（n ≤ 50，三次方也毫无压力） */\nint main() {\n    int n, m, s; cin >> n >> m >> s;\n    const long long INF = (long long)1e18;\n    vector<vector<long long>> d(n + 1, vector<long long>(n + 1, INF));\n    for (int i = 1; i <= n; i++) d[i][i] = 0;\n    for (int k = 0; k < m; k++) {\n        int u, v; long long c; cin >> u >> v >> c;\n        if (c < d[u][v]) d[u][v] = c;\n    }\n    for (int k = 1; k <= n; k++)\n        for (int i = 1; i <= n; i++)\n            for (int j = 1; j <= n; j++)\n                if (d[i][k] < INF && d[k][j] < INF && d[i][k] + d[k][j] < d[i][j])\n                    d[i][j] = d[i][k] + d[k][j];\n    for (int j = 1; j <= n; j++) {\n        if (j > 1) cout << \" \";\n        if (d[s][j] < INF) cout << d[s][j]; else cout << -1;\n    }\n    cout << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4 5 1\n1 2 5\n1 3 1\n3 2 1\n2 4 2\n3 4 6\n",
                "expected_stdout": "0 2 1 4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 1 1\n1 2 7\n",
                "expected_stdout": "0 7 -1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2 0 1\n",
                "expected_stdout": "0 -1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4 6 2\n1 2 3\n2 3 1\n3 4 1\n1 3 5\n2 4 10\n1 4 100\n",
                "expected_stdout": "-1 0 1 2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5 7 1\n1 2 10\n1 4 30\n1 5 100\n2 3 50\n3 5 10\n4 3 20\n4 5 60\n",
                "expected_stdout": "0 10 50 30 60\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "拓扑排序（字典序最小）",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "拓扑排序",
            "AOV 网",
            "贪心"
        ],
        "statement_md": "给一个有向无环图（也可能有环），输出它的一个拓扑序——要求**字典序最小**的那个；如果图里有环（顶点数不足 `n`），输出 `loop`。\n\n★ 教材用**栈**存入度为 0 的顶点，弹出来的顺序是「某种」合法拓扑序；本题要字典序最小，把栈换成**小根堆**就行，算法骨架一模一样。\n\n环检测就是讲义里那句：**出堆个数 < n ⇒ 有环**。",
        "input_format": "第一行 `n m`（顶点数、弧数）。\n\n接下来 `m` 行，每行 `u v` 表示弧 `<u, v>`（无重边、无自环）。",
        "output_format": "一行：字典序最小的拓扑序（`n` 个数，空格分隔）；有环输出 `loop`。",
        "constraints_md": "- 1 ≤ n ≤ 100\n- 0 ≤ m ≤ n(n-1)",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 06 讲 · 图",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <iostream>\n#include <vector>\n#include <queue>\n#include <functional>\nusing namespace std;\nint main() {\n    int n, m; cin >> n >> m;\n    vector<vector<int>> g(n + 1);\n    vector<int> indeg(n + 1, 0);\n    for (int k = 0; k < m; k++) {\n        int u, v; cin >> u >> v;\n        g[u].push_back(v); indeg[v]++;\n    }\n    priority_queue<int, vector<int>, greater<int>> pq;   // 小根堆\n    for (int i = 1; i <= n; i++) if (indeg[i] == 0) pq.push(i);\n    vector<int> order;\n    while (!pq.empty()) {\n        int x = pq.top(); pq.pop();\n        order.push_back(x);\n        for (int y : g[x]) if (--indeg[y] == 0) pq.push(y);\n    }\n    if ((int)order.size() < n) { cout << \"loop\\n\"; return 0; }\n    for (size_t i = 0; i < order.size(); i++)\n        cout << (i ? \" \" : \"\") << order[i];\n    cout << \"\\n\";\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\nusing namespace std;\n/* 另一套：不用堆，每轮线性扫「未用过的入度 0 顶点里编号最小的」（O(n²)） */\nint main() {\n    int n, m; cin >> n >> m;\n    vector<vector<int>> g(n + 1);\n    vector<int> indeg(n + 1, 0);\n    for (int k = 0; k < m; k++) {\n        int u, v; cin >> u >> v;\n        g[u].push_back(v); indeg[v]++;\n    }\n    vector<char> used(n + 1, 0);\n    vector<int> order;\n    for (int round = 0; round < n; round++) {\n        int x = -1;\n        for (int i = 1; i <= n; i++)\n            if (!used[i] && indeg[i] == 0) { x = i; break; }\n        if (x < 0) break;\n        used[x] = 1;\n        order.push_back(x);\n        for (int y : g[x]) indeg[y]--;\n    }\n    if ((int)order.size() < n) { cout << \"loop\\n\"; return 0; }\n    for (size_t i = 0; i < order.size(); i++)\n        cout << (i ? \" \" : \"\") << order[i];\n    cout << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 6\n1 2\n1 3\n3 4\n2 4\n4 5\n2 5\n",
                "expected_stdout": "1 2 3 4 5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5 6\n1 3\n1 2\n2 4\n3 4\n4 5\n3 5\n",
                "expected_stdout": "1 2 3 4 5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5 5\n2 1\n2 3\n1 4\n3 4\n4 5\n",
                "expected_stdout": "2 1 3 4 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3 3\n1 2\n2 3\n3 1\n",
                "expected_stdout": "loop\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6 6\n1 4\n2 4\n2 5\n3 5\n4 6\n5 6\n",
                "expected_stdout": "1 2 3 4 5 6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "折半查找的每次比较",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "折半查找",
            "判定树",
            "有序表"
        ],
        "statement_md": "对一张**严格递增**的有序表做折半查找，输出**依次与之比较的元素**，以及查找结果。\n\n★ 口径钉死（教材写法）：下标 `low=1`、`high=n`，`mid = ⌊(low+high)/2⌋`；`a[mid] == x` 命中，`a[mid] < x` 去 `[mid+1, high]`，否则去 `[low, mid-1]`。\n\n查不到也要把比较过的元素列全——失败 happens 在 `low > high` 那一刻，比较次数和成功一样有讲究（讲义里 n=11 时查 25 也是 4 次）。",
        "input_format": "第一行 `n`（表长）。\n\n第二行 `n` 个严格递增的整数。\n\n第三行 `x`，要找的值。",
        "output_format": "第一行：依次与 `x` 比较过的元素（空格分隔）。\n\n第二行：命中位序（1 基）；查不到为 `-1`。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 表元素严格递增且互不相同",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 07 讲 · 查找",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#define MAXN 1005\nint a[MAXN];\nint main(void) {\n    int n, x;\n    scanf(\"%d\", &n);\n    for (int k = 0; k < n; k++) scanf(\"%d\", &a[k]);\n    scanf(\"%d\", &x);\n    int low = 1, high = n, pos = -1, first = 1;\n    while (low <= high) {\n        int mid = (low + high) / 2;      /* 教材口径：向下取整 */\n        printf(first ? \"%d\" : \" %d\", a[mid - 1]);\n        first = 0;\n        if (a[mid - 1] == x) { pos = mid; break; }\n        else if (a[mid - 1] < x) low = mid + 1;\n        else high = mid - 1;\n    }\n    printf(\"\\n%d\\n\", pos);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\nusing namespace std;\n/* 另一套：递归折半，探到的元素攒在 vector 里最后一起打 */\nvector<int> probes;\nint pos = -1;\nvoid bsearch(const vector<int>& a, int low, int high, int x) {\n    if (low > high) return;\n    int mid = low + (high - low) / 2;    // 与 (low+high)/2 等价，防溢出写法\n    probes.push_back(a[mid - 1]);\n    if (a[mid - 1] == x) { pos = mid; return; }\n    if (a[mid - 1] < x) bsearch(a, mid + 1, high, x);\n    else bsearch(a, low, mid - 1, x);\n}\nint main() {\n    int n, x; cin >> n;\n    vector<int> a(n);\n    for (int &v : a) cin >> v;\n    cin >> x;\n    bsearch(a, 1, n, x);\n    for (size_t i = 0; i < probes.size(); i++)\n        cout << (i ? \" \" : \"\") << probes[i];\n    cout << \"\\n\" << pos << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "11\n7 14 18 21 23 29 31 35 38 42 46\n23\n",
                "expected_stdout": "29 18 21 23\n5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "11\n7 14 18 21 23 29 31 35 38 42 46\n25\n",
                "expected_stdout": "29 18 21 23\n-1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "11\n7 14 18 21 23 29 31 35 38 42 46\n7\n",
                "expected_stdout": "29 18 7\n1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "11\n7 14 18 21 23 29 31 35 38 42 46\n46\n",
                "expected_stdout": "29 38 42 46\n11\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "11\n7 14 18 21 23 29 31 35 38 42 46\n5\n",
                "expected_stdout": "29 18 7\n-1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "二叉排序树：建树、遍历与查找",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "二叉排序树",
            "BST",
            "中序遍历"
        ],
        "statement_md": "按输入顺序把 `n` 个互不相同的数插入一棵**空的二叉排序树**，然后：\n\n1. 输出**中序遍历**序列（BST 的中序 = 升序，这是它的招牌性质）；\n2. 输出树高（**空树为 0，只有根为 1**；树高 = 最长路径上的结点数）；\n3. 在树中查找 `x`，输出**比较次数**（沿根往下走，每碰一个结点记 1 次，走到空指针为止——不存在也是这个口径）。\n\n★ 讲义里 n=11 顺序插入 1..15 那组实测：BST 会退化成链，树高直接飙到 n——插入顺序决定一切。",
        "input_format": "第一行 `n`（插入个数）。\n\n第二行 `n` 个互不相同的整数（按插入顺序给出）。\n\n第三行 `x`，要查找的值。",
        "output_format": "第一行：中序遍历序列（空格分隔）。\n\n第二行：树高。\n\n第三行：查找 `x` 的比较次数。",
        "constraints_md": "- 1 ≤ n ≤ 500\n- 插入值互不相同，|值| ≤ 10⁹",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 07 讲 · 查找",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <stdlib.h>\ntypedef struct Btnode {\n    int v;\n    struct Btnode *l, *r;\n} Btnode;\nBtnode* New(int v) {\n    Btnode* p = (Btnode*)malloc(sizeof(Btnode));\n    p->v = v; p->l = p->r = NULL;\n    return p;\n}\n/* 教材式递归插入 */\nBtnode* Insert(Btnode* t, int v) {\n    if (!t) return New(v);\n    if (v < t->v) t->l = Insert(t->l, v);\n    else if (v > t->v) t->r = Insert(t->r, v);\n    return t;\n}\nvoid Inorder(Btnode* t, int* first) {\n    if (!t) return;\n    Inorder(t->l, first);\n    if (*first) printf(\"%d\", t->v); else printf(\" %d\", t->v);\n    *first = 0;\n    Inorder(t->r, first);\n}\nint Height(Btnode* t) {\n    if (!t) return 0;\n    int a = Height(t->l), b = Height(t->r);\n    return 1 + (a > b ? a : b);\n}\nint main(void) {\n    int n, x;\n    scanf(\"%d\", &n);\n    Btnode* root = NULL;\n    for (int k = 0; k < n; k++) {\n        int v; scanf(\"%d\", &v);\n        root = Insert(root, v);\n    }\n    scanf(\"%d\", &x);\n    int first = 1;\n    Inorder(root, &first);\n    printf(\"\\n%d\\n\", Height(root));\n    int cnt = 0;\n    Btnode* p = root;\n    while (p) {\n        cnt++;\n        if (p->v == x) break;\n        p = (x < p->v) ? p->l : p->r;\n    }\n    printf(\"%d\\n\", cnt);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\nusing namespace std;\n/* 另一套：插入/查找/求高全用迭代写法，结构上不碰递归 */\nstruct N { int v; N *l = nullptr, *r = nullptr; };\nint main() {\n    int n, x; cin >> n;\n    N *root = nullptr;\n    for (int k = 0; k < n; k++) {\n        int v; cin >> v;\n        if (!root) { root = new N{v}; continue; }\n        N *p = root;\n        while (true) {\n            if (v < p->v) { if (!p->l) { p->l = new N{v}; break; } p = p->l; }\n            else          { if (!p->r) { p->r = new N{v}; break; } p = p->r; }\n        }\n    }\n    cin >> x;\n    vector<int> in;\n    vector<N*> st;\n    N *p = root;                          // 迭代中序（模拟栈）\n    while (p || !st.empty()) {\n        while (p) { st.push_back(p); p = p->l; }\n        p = st.back(); st.pop_back();\n        in.push_back(p->v);\n        p = p->r;\n    }\n    for (size_t i = 0; i < in.size(); i++) cout << (i ? \" \" : \"\") << in[i];\n    cout << \"\\n\";\n    vector<vector<N*>> lvl;               // 层序求高\n    if (root) lvl.push_back({root});\n    for (size_t i = 0; i < lvl.size(); i++) {\n        vector<N*> nx;\n        for (N* q : lvl[i]) {\n            if (q->l) nx.push_back(q->l);\n            if (q->r) nx.push_back(q->r);\n        }\n        if (!nx.empty()) lvl.push_back(nx);\n    }\n    cout << lvl.size() << \"\\n\";\n    int cnt = 0; p = root;\n    while (p) { cnt++; if (p->v == x) break; p = (x < p->v) ? p->l : p->r; }\n    cout << cnt << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "6\n45 24 53 12 37 93\n37\n",
                "expected_stdout": "12 24 37 45 53 93\n3\n3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "6\n45 24 53 12 37 93\n40\n",
                "expected_stdout": "12 24 37 45 53 93\n3\n3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n10\n10\n",
                "expected_stdout": "10\n1\n1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n2 1 3\n4\n",
                "expected_stdout": "1 2 3\n2\n2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n5 4 3 2 1\n1\n",
                "expected_stdout": "1 2 3 4 5\n5\n5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "散列表：除留余数 + 线性探测",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "散列表",
            "线性探测",
            "ASL"
        ],
        "statement_md": "表长 `m`，散列函数 `H(key) = key % p`，冲突用**线性探测**（`Hi = (H(key) + i) % m`，i = 0,1,2,…）处理。\n\n输出两行：\n\n1. 槽位 `0` ~ `m-1` 的最终分布（空槽输出 `#`，空格分隔）；\n2. **成功查找的平均查找长度** = 各键探测次数之和 ÷ `n`，保留 2 位小数（`printf(\"%.2f\")` 的口径）。\n\n★ 讲义实测：教材那组 12 个键（m=16, p=13）里，`79` 因为探到 `1%13` 之后的一长串占用，**整整探了 9 次**才落进 `[9]`——「一次冲突不算什么，连锁冲突才是线性探测的命门」。",
        "input_format": "第一行 `m p n`（表长、模数、键个数，保证 n < m 且都能插进去）。\n\n第二行 `n` 个互不相同的非负整数。",
        "output_format": "第一行：`m` 个槽位的分布（空槽 `#`，空格分隔）。\n\n第二行：成功查找 ASL，保留 2 位小数。",
        "constraints_md": "- 2 ≤ p ≤ m ≤ 100\n- 1 ≤ n < m\n- 0 ≤ key ≤ 10⁹",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 07 讲 · 查找",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#define MAXM 105\nlong long slot[MAXM];                    /* -1 = 空 */\nint has[MAXM];\nint main(void) {\n    int m, p, n;\n    scanf(\"%d %d %d\", &m, &p, &n);\n    long long sum = 0;\n    for (int k = 0; k < n; k++) {\n        long long key; scanf(\"%lld\", &key);\n        int h = (int)(key % p), cnt = 0;\n        while (1) {\n            cnt++;\n            if (!has[h]) { has[h] = 1; slot[h] = key; break; }\n            h = (h + 1) % m;\n        }\n        sum += cnt;\n    }\n    for (int i = 0; i < m; i++)\n        printf(i ? has[i] ? \" %lld\" : \" #\" : has[i] ? \"%lld\" : \"#\",\n               slot[i]);\n    printf(\"\\n%.2f\\n\", (double)sum / n);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\nusing namespace std;\n/* 另一套：先算好每键落点与探测次数存进 pair，再统一输出 */\nint main() {\n    int m, p, n; cin >> m >> p >> n;\n    vector<long long> key(n);\n    vector<int> land(n), cost(n);\n    vector<long long> slot(m, -1);\n    long long sum = 0;\n    for (int k = 0; k < n; k++) {\n        cin >> key[k];\n        int h = (int)(key[k] % p), c = 0;\n        while (slot[h] != -1) { h = (h + 1) % m; c++; }\n        c++;                              /* 命中空槽也算一次探测 */\n        slot[h] = key[k];\n        land[k] = h; cost[k] = c;\n        sum += c;\n    }\n    vector<string> cell(m);\n    for (int i = 0; i < m; i++)\n        cell[i] = (slot[i] == -1) ? \"#\" : to_string(slot[i]);\n    for (int i = 0; i < m; i++) cout << (i ? \" \" : \"\") << cell[i];\n    cout << \"\\n\";\n    printf(\"%.2f\\n\", (double)sum / n);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "16 13 12\n19 14 23 1 68 20 84 27 55 11 10 79\n",
                "expected_stdout": "# 14 1 68 27 55 19 20 84 79 23 11 10 # # #\n2.50\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "7 7 5\n10 3 17 24 31\n",
                "expected_stdout": "31 # # 10 3 17 24\n3.00\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5 5 5\n0 5 10 15 20\n",
                "expected_stdout": "0 5 10 15 20\n3.00\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8 5 4\n1 6 11 16\n",
                "expected_stdout": "# 1 6 11 16 # # #\n2.50\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6 3 3\n3 6 9\n",
                "expected_stdout": "3 6 9 # # #\n2.00\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "散列表：链地址法（头插法）",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "散列表",
            "链地址",
            "同义词"
        ],
        "statement_md": "表长 `m`，散列函数 `H(key) = key % p`，冲突用**链地址法**处理：同义词挂一条链，新结点用**头插法**插进链头（教材 `Unsorted` 链的插法）。\n\n输出：\n\n1. `m` 行，桶 `i` 的链：`i: k1 k2 ...`（**链头在前**，即与插入顺序相反；空桶输出 `i:`）；\n2. 最后一行：成功查找 ASL = 每个键在**自己链上**的位置（1 基）之和 ÷ `n`，保留 2 位小数。\n\n★ 同一组教材键，链地址的 ASL（1.75）比线性探测（2.50）好看得多——代价是额外的指针空间。",
        "input_format": "第一行 `m p n`（表长、模数、键个数）。\n\n第二行 `n` 个互不相同的非负整数。",
        "output_format": "前 `m` 行：桶分布，格式 `i: k1 k2 ...`（链头在前，空桶为 `i:`）。\n\n第 `m+1` 行：成功查找 ASL，保留 2 位小数。",
        "constraints_md": "- 2 ≤ p ≤ m ≤ 100\n- 1 ≤ n ≤ 200\n- 0 ≤ key ≤ 10⁹",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 07 讲 · 查找",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <stdlib.h>\n#define MAXM 105\ntypedef struct Node {\n    long long v;\n    struct Node *next;\n} Node;\nNode* bucket[MAXM];\nlong long keys[205];\nint main(void) {\n    int m, p, n;\n    scanf(\"%d %d %d\", &m, &p, &n);\n    for (int k = 0; k < n; k++) {\n        scanf(\"%lld\", &keys[k]);\n        int h = (int)(keys[k] % p);\n        Node* q = (Node*)malloc(sizeof(Node));\n        q->v = keys[k]; q->next = bucket[h];\n        bucket[h] = q;                   /* 头插法 */\n    }\n    for (int i = 0; i < m; i++) {\n        printf(\"%d:\", i);\n        for (Node* q = bucket[i]; q; q = q->next) printf(\" %lld\", q->v);\n        printf(\"\\n\");\n    }\n    long long sum = 0;\n    for (int k = 0; k < n; k++) {\n        int pos = 1;\n        for (Node* q = bucket[keys[k] % p]; q && q->v != keys[k]; q = q->next)\n            pos++;\n        sum += pos;\n    }\n    printf(\"%.2f\\n\", (double)sum / n);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <algorithm>\nusing namespace std;\n/* 另一套：桶用 vector 顺序收，输出时 reverse；ASL 按「值在桶里的下标」算 */\nint main() {\n    int m, p, n; cin >> m >> p >> n;\n    vector<vector<long long>> buck(m);\n    vector<long long> keys(n);\n    for (int k = 0; k < n; k++) {\n        cin >> keys[k];\n        buck[keys[k] % p].push_back(keys[k]);\n    }\n    for (int i = 0; i < m; i++) {\n        vector<long long> r = buck[i];\n        reverse(r.begin(), r.end());     // 头插法效果\n        cout << i << \":\";\n        for (long long v : r) cout << \" \" << v;\n        cout << \"\\n\";\n    }\n    long long sum = 0;\n    for (int k = 0; k < n; k++) {\n        const vector<long long>& b = buck[keys[k] % p];\n        int pos = 0;\n        while (b[pos] != keys[k]) pos++;\n        sum += (int)b.size() - pos;      // reverse 后的位置 = 链上位序\n    }\n    printf(\"%.2f\\n\", (double)sum / n);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "13 13 12\n19 14 23 1 68 20 84 27 55 11 10 79\n",
                "expected_stdout": "0:\n1: 79 27 1 14\n2:\n3: 55 68\n4:\n5:\n6: 84 19\n7: 20\n8:\n9:\n10: 10 23\n11: 11\n12:\n1.75\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5 5 6\n0 5 10 15 20 25\n",
                "expected_stdout": "0: 25 20 15 10 5 0\n1:\n2:\n3:\n4:\n3.50\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 3 3\n1 4 7\n",
                "expected_stdout": "0:\n1: 7 4 1\n2:\n2.00\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7 7 4\n2 9 16 23\n",
                "expected_stdout": "0:\n1:\n2: 23 16 9 2\n3:\n4:\n5:\n6:\n2.50\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6 6 3\n12 18 6\n",
                "expected_stdout": "0: 6 18 12\n1:\n2:\n3:\n4:\n5:\n2.00\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "冒泡排序：逐趟输出",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "冒泡",
            "交换排序",
            "提前终止"
        ],
        "statement_md": "对 `n` 个整数做**冒泡排序**（升序），把**每一趟结束后的序列**都打出来。\n\n★ 口径（教材写法）：第 `i` 趟（`i` 从 1 起）让下标 `j` 从 `0` 扫到 `n-i-1`，`a[j] > a[j+1]` 就交换。**用严格大于**——相等的元素不交换，这正是冒泡「稳定」的原因。\n\n某趟一次交换都没发生就**提前终止**，且这趟本身要输出（它是最后一行）。最后一行输出实际执行的趟数。",
        "input_format": "第一行 `n`（2 ≤ n，元素互异性不保证——相等元素不影响确定性）。\n\n第二行 `n` 个整数。",
        "output_format": "若干行：每趟结束后的序列（空格分隔），最后一趟之后再输出一行趟数。",
        "constraints_md": "- 2 ≤ n ≤ 1000\n- |元素| ≤ 10⁹",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 08 讲 · 排序",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#define MAXN 1005\nint a[MAXN];\nint main(void) {\n    int n;\n    scanf(\"%d\", &n);\n    for (int k = 0; k < n; k++) scanf(\"%d\", &a[k]);\n    int rounds = 0;\n    for (int i = 0; i < n - 1; i++) {\n        int swapped = 0;\n        for (int j = 0; j < n - i - 1; j++)\n            if (a[j] > a[j + 1]) {\n                int t = a[j]; a[j] = a[j + 1]; a[j + 1] = t;\n                swapped = 1;\n            }\n        rounds++;\n        for (int k = 0; k < n; k++)\n            printf(k ? \" %d\" : \"%d\", a[k]);\n        printf(\"\\n\");\n        if (!swapped) break;             /* 提前终止 */\n    }\n    printf(\"%d\\n\", rounds);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\nusing namespace std;\n/* 另一套：「无交换就重来一遍」的写法——效果等价于带提前终止的冒泡 */\nint main() {\n    int n; cin >> n;\n    vector<int> a(n);\n    for (int &v : a) cin >> v;\n    int rounds = 0;\n    while (rounds < n - 1) {\n        bool moved = false;\n        for (int j = 0; j + 1 < n - rounds; j++)\n            if (a[j] > a[j + 1]) { swap(a[j], a[j + 1]); moved = true; }\n        rounds++;\n        for (int k = 0; k < n; k++) cout << (k ? \" \" : \"\") << a[k];\n        cout << \"\\n\";\n        if (!moved) break;\n    }\n    cout << rounds << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n5 4 3 2 1\n",
                "expected_stdout": "4 3 2 1 5\n3 2 1 4 5\n2 1 3 4 5\n1 2 3 4 5\n4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n1 2 3 4 5\n",
                "expected_stdout": "1 2 3 4 5\n1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "6\n3 1 4 1 5 9\n",
                "expected_stdout": "1 3 1 4 5 9\n1 1 3 4 5 9\n1 1 3 4 5 9\n3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n2 3 1 5\n",
                "expected_stdout": "2 1 3 5\n1 2 3 5\n1 2 3 5\n3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7\n49 38 65 97 76 13 27\n",
                "expected_stdout": "38 49 65 76 13 27 97\n38 49 65 13 27 76 97\n38 49 13 27 65 76 97\n38 13 27 49 65 76 97\n13 27 38 49 65 76 97\n13 27 38 49 65 76 97\n6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "快速排序的一趟划分",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "快速排序",
            "Partition",
            "枢轴"
        ],
        "statement_md": "对 `n` 个**互不相同**的整数做快排的**第一趟划分**（教材双向扫描法），输出划分后的序列和枢轴最终落位。\n\n★ 口径（教材写法，一个字都不能变）：\n\n- 枢轴 `pivot = a[0]`（取**第一个**元素），`low=0`、`high=n-1`；\n- `high` 从右往左找第一个 **< pivot** 的元素，填到 `a[low]`；\n- `low` 从左往右找第一个 **> pivot** 的元素，填到 `a[high]`；\n- 反复直到 `low == high`，把枢轴放进去。\n\n位序输出为 **1 基**（`low+1`）。这一趟做完，枢轴左边的全比它小、右边的全比它大——它就位了，以后再也不动。",
        "input_format": "第一行 `n`。\n\n第二行 `n` 个互不相同的整数。",
        "output_format": "第一行：一趟划分后的序列（空格分隔）。\n\n第二行：枢轴最终位序（1 基）。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 元素互不相同，|元素| ≤ 10⁹",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 08 讲 · 排序",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#define MAXN 1005\nint a[MAXN];\nint main(void) {\n    int n;\n    scanf(\"%d\", &n);\n    for (int k = 0; k < n; k++) scanf(\"%d\", &a[k]);\n    int pivot = a[0], low = 0, high = n - 1;\n    while (low < high) {\n        while (low < high && a[high] > pivot) high--;   /* 右找小 */\n        a[low] = a[high];\n        while (low < high && a[low] < pivot) low++;     /* 左找大 */\n        a[high] = a[low];\n    }\n    a[low] = pivot;                      /* 枢轴就位 */\n    for (int k = 0; k < n; k++) printf(k ? \" %d\" : \"%d\", a[k]);\n    printf(\"\\n%d\\n\", low + 1);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\nusing namespace std;\n/* 另一套：把「挖坑」改成「swap 对调」，落位序列与教材法完全一致 */\nint main() {\n    int n; cin >> n;\n    vector<int> a(n);\n    for (int &v : a) cin >> v;\n    int pivot = a[0], low = 0, high = n - 1;\n    while (low < high) {\n        while (low < high && a[high] > pivot) high--;\n        if (low < high) { a[low] = a[high]; }\n        while (low < high && a[low] < pivot) low++;\n        if (low < high) { a[high] = a[low]; }\n    }\n    a[low] = pivot;\n    for (int k = 0; k < n; k++) cout << (k ? \" \" : \"\") << a[k];\n    cout << \"\\n\" << low + 1 << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "8\n49 38 65 97 76 13 27 50\n",
                "expected_stdout": "27 38 13 49 76 97 65 50\n4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n3 1 2 5 4\n",
                "expected_stdout": "2 1 3 5 4\n3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n1\n",
                "expected_stdout": "1\n1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n2 1\n",
                "expected_stdout": "1 2\n2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n50 20 70 10 90 60\n",
                "expected_stdout": "10 20 50 70 90 60\n3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "堆排序：建大顶堆与排序结果",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "堆排序",
            "大顶堆",
            "筛选"
        ],
        "statement_md": "把 `n` 个**互不相同**的整数建成一棵**大顶堆**，再做堆排序。\n\n输出两行：\n\n1. **建成的堆**（1 基数组，即完全二叉树的层序）；\n2. 升序排序结果。\n\n★ 口径（教材写法）：堆用 1 起点的数组存（`i` 的孩子是 `2i`、`2i+1`，这就是全书「下标从 1 起」隐形坑的主场）；建堆从**最后一个非叶结点 `⌊n/2⌋** 倒着到 1 逐个**下沉筛选**；排序阶段每轮「堆顶与末尾交换 → 堆大小减一 → 堆顶重新下沉」。\n\n想看反例的话：升序排序用**大顶**堆——新手十次有九次先想成小顶堆。",
        "input_format": "第一行 `n`。\n\n第二行 `n` 个互不相同的整数。",
        "output_format": "第一行：建成后的大顶堆（层序，空格分隔）。\n\n第二行：升序排序结果（空格分隔）。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 元素互不相同，|元素| ≤ 10⁹",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 08 讲 · 排序",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#define MAXN 1005\nint h[MAXN];\nvoid sift(int i, int size) {             /* 迭代下沉 */\n    while (1) {\n        int c = 2 * i;\n        if (c > size) break;\n        if (c + 1 <= size && h[c + 1] > h[c]) c++;\n        if (h[c] > h[i]) { int t = h[i]; h[i] = h[c]; h[c] = t; i = c; }\n        else break;\n    }\n}\nint main(void) {\n    int n;\n    scanf(\"%d\", &n);\n    for (int k = 1; k <= n; k++) scanf(\"%d\", &h[k]);\n    for (int i = n / 2; i >= 1; i--) sift(i, n);\n    for (int k = 1; k <= n; k++) printf(k > 1 ? \" %d\" : \"%d\", h[k]);\n    printf(\"\\n\");\n    int size = n;                        /* 排序：堆顶换末尾后重沉 */\n    while (size > 1) {\n        int t = h[1]; h[1] = h[size]; h[size] = t;\n        size--;\n        sift(1, size);\n    }\n    for (int k = 1; k <= n; k++) printf(k > 1 ? \" %d\" : \"%d\", h[k]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\nusing namespace std;\n/* 另一套：递归版下沉 + 边排边输出 */\nvector<int> h;\nvoid sift(int i, int size) {\n    int c = 2 * i;\n    if (c > size) return;\n    if (c + 1 <= size && h[c + 1] > h[c]) c++;\n    if (h[c] > h[i]) { swap(h[i], h[c]); sift(c, size); }\n}\nint main() {\n    int n; cin >> n;\n    h.assign(n + 1, 0);\n    for (int k = 1; k <= n; k++) cin >> h[k];\n    for (int i = n / 2; i >= 1; i--) sift(i, n);\n    vector<int> built(h.begin() + 1, h.end());\n    for (size_t k = 0; k < built.size(); k++) cout << (k ? \" \" : \"\") << built[k];\n    cout << \"\\n\";\n    for (int size = n; size > 1; size--) {\n        swap(h[1], h[size]);\n        sift(1, size - 1);\n    }\n    for (int k = 1; k <= n; k++) cout << (k > 1 ? \" \" : \"\") << h[k];\n    cout << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "8\n49 38 65 97 76 13 27 50\n",
                "expected_stdout": "97 76 65 50 49 13 27 38\n13 27 38 49 50 65 76 97\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n1 2 3 4 5\n",
                "expected_stdout": "5 4 3 1 2\n1 2 3 4 5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n7\n",
                "expected_stdout": "7\n7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n12 5 9 20 3 15\n",
                "expected_stdout": "20 12 15 5 3 9\n3 5 9 12 15 20\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n4 3 2 1\n",
                "expected_stdout": "4 3 2 1\n1 2 3 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "二路归并排序：逐趟输出（非递归）",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "归并排序",
            "分治",
            "稳定性"
        ],
        "statement_md": "对 `n` 个整数做**非递归**的二路归并排序（升序），输出**每一趟**结束后的序列。\n\n★ 口径：`width` 从 1 开始，每趟把 `[0..n)` 按 `2*width` 分组，组内 `[i, i+width)` 与 `[i+width, i+2*width)` 两段归并（右段不足整段就原样保留）；`width ≥ n` 时结束。**归并时两边相等取左段**——这就是归并排序稳定的实现根据。\n\n和递归版「先分后合」不同，非递归版**自底向上**：第 1 趟 length-1 有序段两两归并出 length-2，第 2 趟出 length-4……趟数就是 `⌈log₂n⌉`。",
        "input_format": "第一行 `n`（2 ≤ n，元素可重复）。\n\n第二行 `n` 个整数。",
        "output_format": "若干行：第 `k` 趟结束后的完整序列（空格分隔），共 `⌈log₂n⌉` 行。",
        "constraints_md": "- 2 ≤ n ≤ 1000\n- |元素| ≤ 10⁹",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 08 讲 · 排序",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#define MAXN 1005\nint a[MAXN], b[MAXN];\nint main(void) {\n    int n;\n    scanf(\"%d\", &n);\n    for (int k = 0; k < n; k++) scanf(\"%d\", &a[k]);\n    for (int w = 1; w < n; w *= 2) {\n        int len = 0;\n        for (int i = 0; i < n; i += 2 * w) {\n            int p = i, q = i + w, pe = i + w, qe = i + 2 * w;\n            if (pe > n) pe = n;\n            if (qe > n) qe = n;\n            while (p < pe && q < qe)\n                b[len++] = (a[p] <= a[q]) ? a[p++] : a[q++];\n            while (p < pe) b[len++] = a[p++];\n            while (q < qe) b[len++] = a[q++];\n        }\n        for (int k = 0; k < n; k++) a[k] = b[k];\n        for (int k = 0; k < n; k++) printf(k ? \" %d\" : \"%d\", a[k]);\n        printf(\"\\n\");\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\nusing namespace std;\n/* 另一套：in-place merge 用「切开重拼」的思路，先拷左段再按序插右段 */\nint main() {\n    int n; cin >> n;\n    vector<int> a(n);\n    for (int &v : a) cin >> v;\n    for (int w = 1; w < n; w *= 2) {\n        vector<int> nxt;\n        for (int i = 0; i < n; i += 2 * w) {\n            vector<int> L(a.begin() + i, a.begin() + min(i + w, n));\n            vector<int> R(a.begin() + min(i + w, n),\n                          a.begin() + min(i + 2 * w, n));\n            size_t p = 0, q = 0;\n            while (p < L.size() && q < R.size())\n                nxt.push_back(L[p] <= R[q] ? L[p++] : R[q++]);\n            while (p < L.size()) nxt.push_back(L[p++]);\n            while (q < R.size()) nxt.push_back(R[q++]);\n        }\n        a = nxt;\n        for (int k = 0; k < n; k++) cout << (k ? \" \" : \"\") << a[k];\n        cout << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "10\n49 38 65 97 76 13 27 50 5 62\n",
                "expected_stdout": "38 49 65 97 13 76 27 50 5 62\n38 49 65 97 13 27 50 76 5 62\n13 27 38 49 50 65 76 97 5 62\n5 13 27 38 49 50 62 65 76 97\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n2 1\n",
                "expected_stdout": "1 2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n3 1 2 5 4\n",
                "expected_stdout": "1 3 2 5 4\n1 2 3 5 4\n1 2 3 4 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8\n8 7 6 5 4 3 2 1\n",
                "expected_stdout": "7 8 5 6 3 4 1 2\n5 6 7 8 1 2 3 4\n1 2 3 4 5 6 7 8\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n2 2 1 1 3 3\n",
                "expected_stdout": "2 2 1 1 3 3\n1 1 2 2 3 3\n1 1 2 2 3 3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "顺序表的建立及遍历",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "顺序表",
            "建表",
            "遍历"
        ],
        "statement_md": "把 `n` 个整数依次存入顺序表（**尾插法**：读一个存一个，表尾追加），然后按存放顺序遍历输出。\n\n★ 这是所有顺序表题的「地基动作」：`SqList` 建表 → 遍历。后面对照着看：**头插法**建出来正好是反序（见「头插法创建单链表」一题）。",
        "input_format": "第一行 `n`（1 ≤ n）。第二行 `n` 个整数。",
        "output_format": "一行，`n` 个整数（空格分隔）。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |元素| ≤ 10⁹",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 02 讲 · 线性表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#define MAXN 1005\nint a[MAXN];\nint main(void) {\n    int n;\n    scanf(\"%d\", &n);\n    for (int k = 0; k < n; k++) scanf(\"%d\", &a[k]);   /* 尾插 */\n    for (int k = 0; k < n; k++) printf(k ? \" %d\" : \"%d\", a[k]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\nusing namespace std;\nint main() {\n    int n; cin >> n;\n    vector<int> a;\n    for (int k = 0; k < n; k++) { int v; cin >> v; a.push_back(v); }\n    for (size_t k = 0; k < a.size(); k++) cout << (k ? \" \" : \"\") << a[k];\n    cout << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 2 3\n",
                "expected_stdout": "1 2 3\n",
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
                "stdin": "4\n2 2 2 2\n",
                "expected_stdout": "2 2 2 2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n5 4 3 2 1\n",
                "expected_stdout": "5 4 3 2 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "递增有序顺序表的插入（保持有序）",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "顺序表",
            "有序插入",
            "搬移"
        ],
        "statement_md": "在**严格递增**的顺序表里插入 `x`，插完后**仍然递增**。\n\n★ 和「按位插入」的区别：位置不告诉你，得自己找——从前往后扫，找到第一个**大于 x** 的位置就是插入点（等值元素插在它们**后面**）。找位置 O(n)、搬移 O(n)，先找后搬一步都不能少。",
        "input_format": "第一行 `n`。\n\n第二行 `n` 个严格递增的整数。\n\n第三行 `x`。",
        "output_format": "一行，插入后仍递增的表（空格分隔）。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |元素|、|x| ≤ 10⁹",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 02 讲 · 线性表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#define MAXN 1005\nint a[MAXN];\nint main(void) {\n    int n, x;\n    scanf(\"%d\", &n);\n    for (int k = 0; k < n; k++) scanf(\"%d\", &a[k]);\n    scanf(\"%d\", &x);\n    int i = 0;\n    while (i < n && a[i] <= x) i++;      /* 第一个 > x 的位置 */\n    for (int j = n - 1; j >= i; j--) a[j + 1] = a[j];   /* 从后往前搬 */\n    a[i] = x;\n    for (int k = 0; k <= n; k++) printf(k ? \" %d\" : \"%d\", a[k]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\nusing namespace std;\n/* 另一套：新开结果表，边扫边落，x 落一次 */\nint main() {\n    int n, x; cin >> n;\n    vector<int> a(n), b;\n    for (int &v : a) cin >> v;\n    cin >> x;\n    bool placed = false;\n    for (int v : a) {\n        if (!placed && x < v) { b.push_back(x); placed = true; }\n        b.push_back(v);\n    }\n    if (!placed) b.push_back(x);         // 比谁都大 / 表里全相等\n    for (size_t k = 0; k < b.size(); k++) cout << (k ? \" \" : \"\") << b[k];\n    cout << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n1 3 5 7 9\n6\n",
                "expected_stdout": "1 3 5 6 7 9\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n1 3 5 7 9\n0\n",
                "expected_stdout": "0 1 3 5 7 9\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n1 3 5 7 9\n10\n",
                "expected_stdout": "1 3 5 7 9 10\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n2 2 2\n2\n",
                "expected_stdout": "2 2 2 2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n7\n7\n",
                "expected_stdout": "7 7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "合并有序数组",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "归并",
            "双指针",
            "有序表"
        ],
        "statement_md": "两个**非递减**数组 `a`（长 `n`）和 `b`（长 `m`），合并成一个**非递减**数组，不许先拼起来再排序——用**双指针**一次扫完。\n\n★ 相等时取 `a` 的（`<=` 归左边）——这就是归并排序「稳定」的同一套写法，第 08 讲的归并题里还会见到它。",
        "input_format": "第一行 `n m`（n、m 允许为 0）。\n\n第二行 `a` 的 `n` 个非递减整数（可为空行）。\n\n第三行 `b` 的 `m` 个非递减整数（可为空行）。",
        "output_format": "一行，合并后的非递减数组（空表合并结果为空行）。",
        "constraints_md": "- 0 ≤ n, m ≤ 1000\n- |元素| ≤ 10⁹",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 02 讲 · 线性表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#define MAXN 2005\nint a[MAXN], b[MAXN];\nint main(void) {\n    int n, m;\n    scanf(\"%d %d\", &n, &m);\n    for (int k = 0; k < n; k++) scanf(\"%d\", &a[k]);\n    for (int k = 0; k < m; k++) scanf(\"%d\", &b[k]);\n    int i = 0, j = 0, first = 1;\n    while (i < n && j < m) {\n        if (a[i] <= b[j]) printf(first ? \"%d\" : \" %d\", a[i++]);\n        else              printf(first ? \"%d\" : \" %d\", b[j++]);\n        first = 0;\n    }\n    while (i < n) { printf(first ? \"%d\" : \" %d\", a[i++]); first = 0; }\n    while (j < m) { printf(first ? \"%d\" : \" %d\", b[j++]); first = 0; }\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\nusing namespace std;\n/* 另一套：哨兵法——两表各补一个 +∞，循环 n+m 次，每轮挑小的（归并排序原味） */\nint main() {\n    int n, m; cin >> n >> m;\n    vector<int> a(n), b(m);\n    for (int &v : a) cin >> v;\n    for (int &v : b) cin >> v;\n    a.push_back(2000000000); b.push_back(2000000000);\n    vector<int> out;\n    int i = 0, j = 0;\n    for (int k = 0; k < n + m; k++) {\n        if (a[i] <= b[j]) { out.push_back(a[i]); i++; }\n        else { out.push_back(b[j]); j++; }\n    }\n    for (size_t k = 0; k < out.size(); k++) cout << (k ? \" \" : \"\") << out[k];\n    cout << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3 3\n1 3 5\n2 4 6\n",
                "expected_stdout": "1 2 3 4 5 6\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2 2\n1 1\n1 1\n",
                "expected_stdout": "1 1 1 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 1\n9\n1\n",
                "expected_stdout": "1 9\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4 0\n1 2 3 4\n\n",
                "expected_stdout": "1 2 3 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "0 3\n\n5 6 7\n",
                "expected_stdout": "5 6 7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "数组元素循环右移 n 位",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "循环移位",
            "数组",
            "下标变换"
        ],
        "statement_md": "把长度为 `n` 的数组**循环右移 `k` 位**：每个元素后移 `k` 格，移出右端的绕回左端。\n\n★ 两个坑：① `k` 可能比 `n` 大，先 `k %= n`；② `k % n == 0` 时数组**原样不动**——直接按 `a[-k:] + a[:-k]` 切片写，k=0 时会算出整个数组的两倍拼接，记得特判。\n\n三次逆置法（教材延伸）：逆置前 n-k 位 → 逆置后 k 位 → 整体逆置，原地 O(1) 空间完成，值得手玩一遍。",
        "input_format": "第一行 `n k`。第二行 `n` 个整数。",
        "output_format": "一行，右移后的数组（空格分隔）。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 0 ≤ k ≤ 10⁹",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 02 讲 · 线性表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#define MAXN 1005\nint a[MAXN];\nvoid rev(int l, int r) {                 /* 逆置 a[l..r]（闭区间） */\n    while (l < r) { int t = a[l]; a[l] = a[r]; a[r] = t; l++; r--; }\n}\nint main(void) {\n    int n, k;\n    scanf(\"%d %d\", &n, &k);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    k %= n;\n    if (k) {                             /* 三次逆置法：原地完成 */\n        rev(0, n - k - 1);\n        rev(n - k, n - 1);\n        rev(0, n - 1);\n    }\n    for (int i = 0; i < n; i++) printf(i ? \" %d\" : \"%d\", a[i]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\nusing namespace std;\n/* 另一套：直接按下标映射——新位置 (i + k) % n，O(n) 空间换直白 */\nint main() {\n    int n, k; cin >> n >> k;\n    vector<int> a(n), b(n);\n    for (int i = 0; i < n; i++) cin >> a[i];\n    k %= n;\n    for (int i = 0; i < n; i++) b[(i + k) % n] = a[i];\n    for (int i = 0; i < n; i++) cout << (i ? \" \" : \"\") << b[i];\n    cout << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 2\n1 2 3 4 5\n",
                "expected_stdout": "4 5 1 2 3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5 7\n1 2 3 4 5\n",
                "expected_stdout": "4 5 1 2 3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5 5\n1 2 3 4 5\n",
                "expected_stdout": "1 2 3 4 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1 100\n9\n",
                "expected_stdout": "9\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3 1\n7 8 9\n",
                "expected_stdout": "9 7 8\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "最大子列和问题",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "最大子列和",
            "Kadane",
            "动态规划"
        ],
        "statement_md": "在 `n` 个整数（可正可负）里找**连续**子列，使和最大，输出这个最大和。\n\n★ 口径：**允许空子列**——全负数时输出 `0`（一个元素都不选也是合法子列）。\n\nKadane 思想：从头扫，`cur` 记「以当前元素结尾的最大子列和」——前缀和是负数就**果断丢弃重开**（`cur = max(v, cur + v)` 的手写版），`best` 只记历史最高。O(n) 一趟完事，枚举所有起止点的 O(n³)/O(n²) 都能被它秒。",
        "input_format": "第一行 `n`。第二行 `n` 个整数。",
        "output_format": "一行，最大子列和（全负输出 `0`）。",
        "constraints_md": "- 1 ≤ n ≤ 100000\n- |元素| ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 02 讲 · 线性表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#define MAXN 100005\nint a[MAXN];\nint main(void) {\n    int n;\n    scanf(\"%d\", &n);\n    for (int k = 0; k < n; k++) scanf(\"%d\", &a[k]);\n    long long best = 0, cur = 0;\n    for (int k = 0; k < n; k++) {\n        cur = (cur > 0) ? cur + a[k] : a[k];   /* 负前缀果断丢 */\n        if (cur > best) best = cur;\n    }\n    printf(\"%lld\\n\", best);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\nusing namespace std;\n/* 另一套：前缀和视角——最大子列和 = max(前缀和) - min(此前前缀和)，前缀里自带空子列(0) */\nint main() {\n    int n; cin >> n;\n    long long run = 0, mn = 0, best = 0;\n    for (int k = 0; k < n; k++) {\n        long long v; cin >> v;\n        run += v;\n        if (run - mn > best) best = run - mn;\n        if (run < mn) mn = run;\n    }\n    cout << best << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "6\n-2 11 -4 13 -5 -2\n",
                "expected_stdout": "20\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n-1 -2 -3 -4\n",
                "expected_stdout": "0\n",
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
                "stdin": "5\n1 2 3 4 5\n",
                "expected_stdout": "15\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8\n4 -3 5 -2 -1 2 6 -2\n",
                "expected_stdout": "11\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "单词逆置",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "字符串",
            "逆置",
            "分词"
        ],
        "statement_md": "把一行英文里的**单词顺序颠倒**：输入 `hello world`，输出 `world hello`。\n\n★ 口径：单词间可能**有多个空格**、首尾也可能有空格——输出一律以**单个空格**分隔，没有多余空白；整行没有单词就输出空行。\n\n用栈想最自然：单词一个个**进栈**，再逐个**出栈**拼接——后进先出天然就是逆序。",
        "input_format": "一行英文（长度 ≤ 10000，只含空格和大小写字母）。",
        "output_format": "一行，单词顺序颠倒、单空格分隔；无单词则为空行。",
        "constraints_md": "- 1 ≤ 单词数 ≤ 2000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 02 讲 · 线性表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <string.h>\n#include <ctype.h>\nint main(void) {\n    char line[10005];\n    if (!fgets(line, sizeof line, stdin)) { printf(\"\\n\"); return 0; }\n    /* 扫一遍：一个单词 = 一段连续字母，找到就从末尾倒着写 */\n    char *w[2005];\n    int cnt = 0;\n    for (char *p = line; *p; ) {\n        while (*p && isspace((unsigned char)*p)) p++;\n        if (!*p) break;\n        w[cnt++] = p;\n        while (*p && !isspace((unsigned char)*p)) p++;\n        if (*p) *p++ = '\\0';\n    }\n    for (int k = cnt - 1; k >= 0; k--)\n        printf(k == cnt - 1 ? \"%s\" : \" %s\", w[k]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <sstream>\n#include <stack>\n#include <string>\nusing namespace std;\n/* 另一套：正经用栈——单词进栈，出栈拼接（后进先出 = 逆序） */\nint main() {\n    string line;\n    if (!getline(cin, line)) { cout << \"\\n\"; return 0; }\n    istringstream in(line);\n    stack<string> st;\n    string w;\n    while (in >> w) st.push(w);\n    bool first = true;\n    while (!st.empty()) {\n        if (!first) cout << \" \";\n        cout << st.top();\n        st.pop();\n        first = false;\n    }\n    cout << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "hello world\n",
                "expected_stdout": "world hello\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "  the   quick  fox \n",
                "expected_stdout": "fox quick the\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "one\n",
                "expected_stdout": "one\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "  \n",
                "expected_stdout": "\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "a b a\n",
                "expected_stdout": "a b a\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "头插法创建单链表、遍历链表",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "单链表",
            "头插法",
            "遍历"
        ],
        "statement_md": "读 `n` 个整数，按输入顺序用**头插法**建一条带头结点的单链表，再从头到尾遍历输出。\n\n★ 头插法 = 新结点总插在**表头**，建好后结点次序与输入**正好相反**（理论题考过的同款结论）。想输出与输入同序，得用尾插法——或者干脆建完再**就地逆置**（下一题）。",
        "input_format": "第一行 `n`。第二行 `n` 个整数（按插入顺序给出）。",
        "output_format": "一行，遍历链表得到的 `n` 个整数（与输入顺序相反）。",
        "constraints_md": "- 1 ≤ n ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 02 讲 · 线性表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <stdlib.h>\ntypedef struct Lnode {\n    int v;\n    struct Lnode *next;\n} Lnode;\nint main(void) {\n    int n;\n    scanf(\"%d\", &n);\n    Lnode head; head.next = NULL;          /* 带头结点 */\n    for (int k = 0; k < n; k++) {\n        int v; scanf(\"%d\", &v);\n        Lnode *p = (Lnode*)malloc(sizeof(Lnode));\n        p->v = v;\n        p->next = head.next;               /* 头插：插在首元结点前 */\n        head.next = p;\n    }\n    int first = 1;\n    for (Lnode *p = head.next; p; p = p->next) {\n        printf(first ? \"%d\" : \" %d\", p->v);\n        first = 0;\n    }\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <algorithm>\nusing namespace std;\n/* 另一套：不用指针，vector 顺序收 + reverse（头插法的效果） */\nint main() {\n    int n; cin >> n;\n    vector<int> a;\n    for (int k = 0; k < n; k++) { int v; cin >> v; a.push_back(v); }\n    reverse(a.begin(), a.end());\n    for (size_t k = 0; k < a.size(); k++) cout << (k ? \" \" : \"\") << a[k];\n    cout << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4\n1 2 3 4\n",
                "expected_stdout": "4 3 2 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n9\n",
                "expected_stdout": "9\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n5 5 5\n",
                "expected_stdout": "5 5 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n1 2 3 4 5 6\n",
                "expected_stdout": "6 5 4 3 2 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "两个有序链表序列的合并",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "单链表",
            "合并",
            "哨兵结点"
        ],
        "statement_md": "两条**非递减**的单链表 `L1`、`L2`（各以 `-1` 结尾，链表可以有空表），合并成一条**非递减**链表并输出。\n\n★ 教材做法：设一个**哨兵/哑结点**当结果链表的头，两路指针比大小，小的摘下来接到结果尾部——**不许新建结点**，重组现有指针。相等时取 `L1` 的。这题就是 PTA 经典「数据结构」开篇题的口吻。",
        "input_format": "两行：第一行 `L1` 的元素（`-1` 结尾），第二行 `L2` 的元素（`-1` 结尾）。元素非递减；`-1` 只作结束标志。",
        "output_format": "一行，合并后的非递减序列（空格分隔；两表全空则为空行）。",
        "constraints_md": "- 链表长度 0 ≤ len ≤ 1000\n- |元素| ≤ 10⁹",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 02 讲 · 线性表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <stdlib.h>\ntypedef struct Lnode { int v; struct Lnode *next; } Lnode;\nLnode* build(void) {                     /* 尾插建表，返回首元指针（NULL = 空表） */\n    Lnode *h = NULL, *t = NULL;\n    int v;\n    while (scanf(\"%d\", &v) == 1 && v != -1) {\n        Lnode *p = (Lnode*)malloc(sizeof(Lnode));\n        p->v = v; p->next = NULL;\n        if (t) t->next = p; else h = p;\n        t = p;\n    }\n    return h;\n}\nint main(void) {\n    Lnode *a = build(), *b = build();\n    Lnode dummy; Lnode *tail = &dummy;   /* 哑结点收结果 */\n    dummy.next = NULL;\n    while (a && b) {\n        if (a->v <= b->v) { tail->next = a; a = a->next; }\n        else              { tail->next = b; b = b->next; }\n        tail = tail->next;\n    }\n    tail->next = a ? a : b;\n    int first = 1;\n    for (Lnode *p = dummy.next; p; p = p->next) {\n        printf(first ? \"%d\" : \" %d\", p->v);\n        first = 0;\n    }\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\nusing namespace std;\n/* 另一套：读入同款，合并改用「先接 a 剩余再穿插」的朴素双数组写法 */\nint main() {\n    vector<int> a, b;\n    int v;\n    auto read = [&](vector<int>& s) {\n        while (cin >> v && v != -1) s.push_back(v);\n    };\n    read(a); read(b);\n    vector<int> out;\n    size_t i = 0, j = 0;\n    while (i < a.size() && j < b.size())\n        out.push_back(a[i] <= b[j] ? a[i++] : b[j++]);\n    while (i < a.size()) out.push_back(a[i++]);\n    while (j < b.size()) out.push_back(b[j++]);\n    for (size_t k = 0; k < out.size(); k++) cout << (k ? \" \" : \"\") << out[k];\n    cout << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "1 3 5 -1\n2 4 6 -1\n",
                "expected_stdout": "1 2 3 4 5 6\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "-1\n1 2 -1\n",
                "expected_stdout": "1 2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 1 -1\n1 -1\n",
                "expected_stdout": "1 1 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3 1 2 -1\n-1\n",
                "expected_stdout": "3 1 2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "-1\n-1\n",
                "expected_stdout": "\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "约瑟夫环",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "约瑟夫",
            "环形",
            "模拟"
        ],
        "statement_md": "`n` 个人围成一圈，编号 `1..n`。从编号 1 的开始**报数**，报到 `m` 的人出圈，下一个人从 1 重新报数——输出全部出圈顺序。\n\n★ 数据结构味最浓的写法是**循环链表**：删结点 = 前驱 `next` 跨过去。用数组模拟等价：出圈下标 `idx = (idx + m - 1) % 剩余人数`，删掉后**原地接着**从「刚出圈那位的位置」继续数。\n\n几个边界心里过一遍：`m=1` 就是按编号顺序全出；`n=1` 直接出自己；`m` 比人数大会绕圈（取模兜底）。",
        "input_format": "一行 `n m`（1 ≤ n ≤ 1000，1 ≤ m ≤ 10⁹）。",
        "output_format": "一行，`n` 个出圈编号（空格分隔）。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 1 ≤ m ≤ 10⁹",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 02 讲 · 线性表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#define MAXN 1005\nint a[MAXN];                             /* a[i]：0 基，1 = 还在圈内 */\nint main(void) {\n    int n, m;\n    scanf(\"%d %d\", &n, &m);\n    for (int i = 0; i < n; i++) a[i] = 1;\n    int left = n, idx = 0, first = 1;    /* idx：当前报数人的下标（0 基） */\n    while (left) {\n        /* m 可达 1e9，先按剩余人数折算步长：报 m = 绕 alive 圈后的 step */\n        int step = (int)((long long)m % left);\n        if (!step) step = left;\n        int cnt = 0;\n        while (1) {\n            if (a[idx]) cnt++;           /* 在圈内的才计数 */\n            if (cnt == step) break;\n            idx = (idx + 1) % n;\n        }\n        a[idx] = 0;\n        printf(first ? \"%d\" : \" %d\", idx + 1);\n        first = 0;\n        left--;\n        if (!left) break;\n        do { idx = (idx + 1) % n; } while (!a[idx]);   /* 从下一位重新报 1 */\n    }\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <list>\nusing namespace std;\n/* 另一套：list 模拟循环链表——迭代器绕圈，erase 返回下一个位置 */\nint main() {\n    int n, m; cin >> n >> m;\n    list<int> ring;\n    for (int i = 1; i <= n; i++) ring.push_back(i);\n    auto it = ring.begin();\n    bool first = true;\n    while (!ring.empty()) {\n        long long k = (long long)(m - 1) % (long long)ring.size();  /* m 可达 1e9，先折算 */\n        for (long long c = 0; c < k; c++) {\n            if (++it == ring.end()) it = ring.begin();\n        }\n        if (!first) cout << \" \";\n        cout << *it;\n        first = false;\n        it = ring.erase(it);             /* 出圈；erase 给的下一个位置接着报 1 */\n        if (it == ring.end()) it = ring.begin();\n    }\n    cout << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 3\n",
                "expected_stdout": "3 1 5 2 4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "7 2\n",
                "expected_stdout": "2 4 6 1 5 3 7\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5 1\n",
                "expected_stdout": "1 2 3 4 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1 7\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6 5\n",
                "expected_stdout": "5 4 6 2 3 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "单链表建表与就地逆置",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "单链表",
            "就地逆置",
            "指针"
        ],
        "statement_md": "用**尾插法**建一条带头结点的单链表，先遍历输出一次；然后**就地逆置**（一个新结点都不许开，纯指针重排），再遍历输出一次。\n\n★ 就地逆置三指针套路（教材 2.5 的标准动作）：\n\n```c\np = 首元结点; 原表拆空;\nwhile (p) { q = p->next; p->next = 新表头后; 头插 p; p = q; }\n```\n\n本质 = 把结点按原序逐个**头插**进新链——练的就是「头插法反序」的指针手感。",
        "input_format": "第一行 `n`。第二行 `n` 个整数。",
        "output_format": "两行：第一行建表后的正序遍历；第二行就地逆置后的遍历。",
        "constraints_md": "- 1 ≤ n ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 02 讲 · 线性表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <stdlib.h>\ntypedef struct Lnode { int v; struct Lnode *next; } Lnode;\nint main(void) {\n    int n;\n    scanf(\"%d\", &n);\n    Lnode head; head.next = NULL;\n    Lnode *tail = &head;                 /* 尾插建表 */\n    for (int k = 0; k < n; k++) {\n        int v; scanf(\"%d\", &v);\n        Lnode *p = (Lnode*)malloc(sizeof(Lnode));\n        p->v = v; p->next = NULL;\n        tail->next = p; tail = p;\n    }\n    int first = 1;\n    for (Lnode *p = head.next; p; p = p->next) {\n        printf(first ? \"%d\" : \" %d\", p->v); first = 0;\n    }\n    printf(\"\\n\");\n    /* 就地逆置：摘下首元结点起的一串，逐个头插回 head */\n    Lnode *p = head.next, *newhead = NULL;\n    while (p) {\n        Lnode *q = p->next;\n        p->next = newhead;\n        newhead = p;\n        p = q;\n    }\n    head.next = newhead;\n    first = 1;\n    for (Lnode *p2 = head.next; p2; p2 = p2->next) {\n        printf(first ? \"%d\" : \" %d\", p2->v); first = 0;\n    }\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <algorithm>\nusing namespace std;\n/* 另一套：数组建表，双端翻转对照（行为等价；指针版的正确性由对拍保证） */\nint main() {\n    int n; cin >> n;\n    vector<int> a(n);\n    for (int &v : a) cin >> v;\n    for (int k = 0; k < n; k++) cout << (k ? \" \" : \"\") << a[k];\n    cout << \"\\n\";\n    reverse(a.begin(), a.end());\n    for (int k = 0; k < n; k++) cout << (k ? \" \" : \"\") << a[k];\n    cout << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n1 2 3 4 5\n",
                "expected_stdout": "1 2 3 4 5\n5 4 3 2 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n8\n",
                "expected_stdout": "8\n8\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n1 1 2\n",
                "expected_stdout": "1 1 2\n2 1 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n-1 0 -1 3\n",
                "expected_stdout": "-1 0 -1 3\n3 -1 0 -1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "括号匹配检验",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "栈",
            "括号匹配",
            "顺序栈应用"
        ],
        "statement_md": "判断一行括号串（只含 `()[]{}` 六种字符）是否**匹配**：每种左括号都有同类的右括号按正确顺序闭合。匹配输出 `yes`，否则 `no`。\n\n★ 栈的招牌应用（3.3.2 的第一个例子）：左括号**进栈**，碰到右括号就**弹栈对暗号**——弹出来的必须同类；最后栈必须是**空的**（不空 = 左括号多了）。三种失配全在这题里：类型对不上、右括号多了、左括号多了。",
        "input_format": "一行，仅由 `()[]{}` 组成的非空串（长度 ≤ 10000）。",
        "output_format": "一行，`yes` 或 `no`。",
        "constraints_md": "- 1 ≤ 串长 ≤ 10000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 03 讲 · 栈和队列",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#define MAXN 10005\nchar st[MAXN];\nint main(void) {\n    char line[MAXN];\n    if (!fgets(line, sizeof line, stdin)) { printf(\"no\\n\"); return 0; }\n    int top = -1, ok = 1;\n    for (char *p = line; *p && ok; p++) {\n        char c = *p;\n        if (c == '(' || c == '[' || c == '{') st[++top] = c;\n        else if (c == ')' || c == ']' || c == '}') {\n            char want = (c == ')') ? '(' : (c == ']') ? '[' : '{';\n            if (top < 0 || st[top] != want) ok = 0;\n            else top--;\n        }\n        /* 其他字符忽略，防御性 */\n    }\n    printf(ok && top < 0 ? \"yes\\n\" : \"no\\n\");   /* 栈空才叫匹配完 */\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <stack>\n#include <string>\nusing namespace std;\n/* 另一套：map 存配对关系，STL 栈直译 */\nint main() {\n    string line;\n    if (!getline(cin, line)) { cout << \"no\\n\"; return 0; }\n    string open = \"([{\", close = \")]}\";\n    stack<char> st;\n    bool ok = true;\n    for (char c : line) {\n        size_t o = open.find(c), cl = close.find(c);\n        if (o != string::npos) st.push(c);\n        else if (cl != string::npos) {\n            if (st.empty() || st.top() != open[cl]) { ok = false; break; }\n            st.pop();\n        }\n    }\n    cout << (ok && st.empty() ? \"yes\" : \"no\") << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "()[]{}\n",
                "expected_stdout": "yes\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "([)]\n",
                "expected_stdout": "no\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "((\n",
                "expected_stdout": "no\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": ")]\n",
                "expected_stdout": "no\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "{[()]}\n",
                "expected_stdout": "yes\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "进制转换",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "栈",
            "进制转换",
            "数制"
        ],
        "statement_md": "把十进制非负整数 `n` 转成 `b` 进制（`2 ≤ b ≤ 16`），超过 9 的数字用**大写** `A`~`F`。\n\n★ 教材算法 3.1 的直译：反复 `n % b` **进栈**、`n /= b`，最后**出栈**拼串——除基取余倒序读，栈天生干这个。\n\n坑只有两个：`n = 0` 要特判输出 `0`（循环一次都不走）；字母是大写，`A` 不是 `a`。",
        "input_format": "一行 `n b`（0 ≤ n ≤ 10⁹，2 ≤ b ≤ 16）。",
        "output_format": "一行，`n` 的 `b` 进制表示（`n=0` 输出 `0`）。",
        "constraints_md": "- 0 ≤ n ≤ 10⁹\n- 2 ≤ b ≤ 16",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 03 讲 · 栈和队列",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nint main(void) {\n    long long n; int b;\n    scanf(\"%lld %d\", &n, &b);\n    char st[40];\n    int top = -1;\n    if (n == 0) st[++top] = '0';         /* 特判：0 转几进制都是 0 */\n    while (n) {\n        int r = (int)(n % b);\n        st[++top] = (char)(r < 10 ? '0' + r : 'A' + r - 10);\n        n /= b;\n    }\n    while (top >= 0) putchar(st[top--]); /* 出栈 = 倒序读余数 */\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <stack>\n#include <string>\nusing namespace std;\n/* 另一套：递归版——先递归处理高位，再印当前位（系统栈替你倒序） */\nvoid conv(long long n, int b) {\n    if (!n) return;\n    conv(n / b, b);\n    int r = n % b;\n    putchar(r < 10 ? '0' + r : 'A' + r - 10);\n}\nint main() {\n    long long n; int b;\n    cin >> n >> b;\n    if (n == 0) cout << \"0\";\n    else conv(n, b);\n    cout << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "0 2\n",
                "expected_stdout": "0\n",
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
                "stdin": "100 2\n",
                "expected_stdout": "1100100\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "31 8\n",
                "expected_stdout": "37\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1023 16\n",
                "expected_stdout": "3FF\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "16 16\n",
                "expected_stdout": "10\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "出栈序列的合法性",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "栈",
            "出栈序列",
            "模拟"
        ],
        "statement_md": "`1..n` 依次**进栈**（进栈和出栈可以任意交错），给定一个出栈序列，判断它是否合法。合法输出 `yes`，否则 `no`。\n\n★ 判定法：拿目标序列当清单，`1` 到 `n` 顺序进栈，**栈顶一等于目标就弹出**；某一步弹不出还进不进去，就是假序列。理论题里 「`3 1 2` 不可能」的通用版判法就是它。",
        "input_format": "第一行 `n`。\n\n第二行 `n` 个互不相同的整数（是 `1..n` 的一个排列）。",
        "output_format": "一行，`yes` 或 `no`。",
        "constraints_md": "- 1 ≤ n ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 03 讲 · 栈和队列",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#define MAXN 1005\nint st[MAXN], target[MAXN];\nint main(void) {\n    int n, top = -1, nxt = 1;\n    scanf(\"%d\", &n);\n    for (int k = 0; k < n; k++) scanf(\"%d\", &target[k]);\n    int ok = 1;\n    for (int k = 0; k < n && ok; k++) {\n        int want = target[k];\n        while (top < 0 || st[top] != want) {\n            if (nxt > n) { ok = 0; break; }   /* 进完还没有 = 假 */\n            st[++top] = nxt++;\n        }\n        if (ok) top--;                        /* 弹出目标元素 */\n    }\n    printf(ok ? \"yes\\n\" : \"no\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <stack>\n#include <vector>\nusing namespace std;\n/* 另一套：反着走——枚举每次「先弹到弹不动为止」，弹的顺序必须恰好等于目标 */\nint main() {\n    int n; cin >> n;\n    vector<int> t(n);\n    for (int &v : t) cin >> v;\n    stack<int> st;\n    int nxt = 1, j = 0;\n    while (j < n) {\n        if (!st.empty() && st.top() == t[j]) { st.pop(); j++; continue; }\n        if (nxt > n) break;\n        st.push(nxt++);\n    }\n    cout << (j == n ? \"yes\" : \"no\") << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n1 2 3 4 5\n",
                "expected_stdout": "yes\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n3 1 2\n",
                "expected_stdout": "no\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n3 2 1\n",
                "expected_stdout": "yes\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n2 1 4 3\n",
                "expected_stdout": "yes\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n5 4 3 2 1\n",
                "expected_stdout": "yes\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n4 1 2 3\n",
                "expected_stdout": "no\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "判断对称矩阵",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "数组",
            "对称矩阵",
            "二维数组"
        ],
        "statement_md": "给定一个 `n` 阶方阵 `A`，判断它是否为**对称矩阵**（即对任意 `1 ≤ i, j ≤ n` 都满足 `A[i][j] == A[j][i]`）。\n\n★ 只需要检查**上三角**（`j > i`）的元素是否等于对应的下三角元素；主对角线元素 `A[i][i]` 天然等于自己，不用比。这是后面学习「对称矩阵压缩存储」的前置直觉。",
        "input_format": "第一行一个整数 `n`。\n\n随后 `n` 行，每行 `n` 个整数，表示矩阵 `A`。",
        "output_format": "一行，若是对称矩阵输出 `yes`，否则输出 `no`。",
        "constraints_md": "- 1 ≤ n ≤ 100\n- |A[i][j]| ≤ 10^9",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 04 讲 · 串、数组和广义表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nint a[105][105];\nint main(void) {\n    int n;\n    scanf(\"%d\", &n);\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++)\n            scanf(\"%d\", &a[i][j]);\n    for (int i = 0; i < n; i++)\n        for (int j = i + 1; j < n; j++)\n            if (a[i][j] != a[j][i]) { printf(\"no\\n\"); return 0; }\n    printf(\"yes\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\nusing namespace std;\nint main() {\n    int n; cin >> n;\n    vector<long long> a(n * n);\n    for (int i = 0; i < n * n; i++) cin >> a[i];\n    bool ok = true;\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++)\n            if (a[i * n + j] != a[j * n + i]) ok = false;\n    cout << (ok ? \"yes\\n\" : \"no\\n\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 2 3\n2 4 5\n3 5 6\n",
                "expected_stdout": "yes\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n1 2 3\n2 4 5\n9 5 6\n",
                "expected_stdout": "no\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n42\n",
                "expected_stdout": "yes\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n0 -1 2 3\n-1 5 0 4\n2 0 7 -2\n3 4 -2 9\n",
                "expected_stdout": "yes\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n1 2\n1 2\n",
                "expected_stdout": "no\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "统计子串",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "串",
            "子串统计",
            "模式匹配"
        ],
        "statement_md": "给定主串 `S` 和模式串 `T`，统计 `T` 在 `S` 中出现的**总次数**（**允许重叠**），以及首次出现的位置（从 1 开始计，未出现则为 `0`）。\n\n★ 对比「KMP 统计不重叠出现次数」：在 `S = aaaaa` 中找 `T = aa`，不重叠算 `2` 次，而**允许重叠**时起始位置 `1, 2, 3, 4` 全算，共 `4` 次。用 KMP 写允许重叠时，每次匹配成功后模式串指针不是清零，而是跳到 `next[m]`！",
        "input_format": "第一行主串 `S`（不含空格）。\n\n第二行模式串 `T`（不含空格，非空）。",
        "output_format": "一行两个整数，空格分隔：`出现总次数 首次位置`（未出现输出 `0 0`）。",
        "constraints_md": "- 1 ≤ |S|, |T| ≤ 10000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 04 讲 · 串、数组和广义表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <string.h>\nchar s[10005], t[10005];\nint main(void) {\n    scanf(\"%s %s\", s, t);\n    int n = (int)strlen(s), m = (int)strlen(t);\n    int cnt = 0, first = 0;\n    for (int i = 0; i + m <= n; i++) {\n        if (strncmp(s + i, t, m) == 0) {\n            cnt++;\n            if (!first) first = i + 1;\n        }\n    }\n    printf(\"%d %d\\n\", cnt, first);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <string>\nusing namespace std;\nint main() {\n    string s, t; cin >> s >> t;\n    int cnt = 0, first = 0;\n    size_t pos = 0;\n    while (true) {\n        size_t k = s.find(t, pos);\n        if (k == string::npos) break;\n        cnt++;\n        if (!first) first = (int)k + 1;\n        pos = k + 1;    /* ★ 允许重叠：每次只前进 1 格 */\n    }\n    cout << cnt << \" \" << first << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "aaaaa\naa\n",
                "expected_stdout": "4 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "abababa\naba\n",
                "expected_stdout": "3 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "abcde\nxyz\n",
                "expected_stdout": "0 0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "hello\nll\n",
                "expected_stdout": "1 3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "abc\nabcde\n",
                "expected_stdout": "0 0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "aaaa\na\n",
                "expected_stdout": "4 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "字符串模式匹配（KMP）",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "串",
            "KMP",
            "strstr"
        ],
        "statement_md": "给定主串 `S` 和 `q` 个待查模式串 `T`，对每个模式串，在 `S` 中查找它首次出现的位置：\n\n- 若找到，输出从该位置一直到 `S` 末尾的子串（行为与 C 标准库的 `strstr(S, T)` 完全一致）；\n- 若找不到，输出 `Not Found`。\n\n★ 这是 PTA 数据结构题集里的经典原题：主串很长、查询有多次，对每个模式串先预处理 `next` 数组再做 KMP 扫描，每次查询都是线性的 `O(|S| + |T|)`。",
        "input_format": "第一行主串 `S`（不含空格）。\n\n第二行正整数 `q`（查询个数）。\n\n随后 `q` 行，每行一个非空模式串 `T`。",
        "output_format": "`q` 行，每行输出匹配位置起的后缀子串，或 `Not Found`。",
        "constraints_md": "- 1 ≤ |S| ≤ 100000\n- 1 ≤ q ≤ 20\n- 1 ≤ |T| ≤ 10000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 04 讲 · 串、数组和广义表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <string.h>\nchar s[100005], t[10005];\nint nxt[10005];\nint kmp_find(const char *s, int n, const char *t, int m) {\n    nxt[0] = -1;\n    int i = 0, j = -1;\n    while (i < m) {\n        if (j == -1 || t[i] == t[j]) { i++; j++; nxt[i] = j; }\n        else j = nxt[j];\n    }\n    i = 0; j = 0;\n    while (i < n && j < m) {\n        if (j == -1 || s[i] == t[j]) { i++; j++; }\n        else j = nxt[j];\n    }\n    return j == m ? i - m : -1;\n}\nint main(void) {\n    int q;\n    scanf(\"%s %d\", s, &q);\n    int n = (int)strlen(s);\n    while (q--) {\n        scanf(\"%s\", t);\n        int m = (int)strlen(t);\n        int pos = kmp_find(s, n, t, m);\n        if (pos >= 0) printf(\"%s\\n\", s + pos);\n        else printf(\"Not Found\\n\");\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <string>\nusing namespace std;\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    string s; int q;\n    cin >> s >> q;\n    while (q--) {\n        string t; cin >> t;\n        size_t p = s.find(t);\n        if (p == string::npos) cout << \"Not Found\\n\";\n        else cout << s.substr(p) << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "abcabcabcd\n3\nabcabcd\nabcx\ncd\n",
                "expected_stdout": "abcabcd\nNot Found\ncd\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "ababababca\n2\nababca\nxyz\n",
                "expected_stdout": "ababca\nNot Found\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "aaaaaa\n2\naaa\naaaaaaa\n",
                "expected_stdout": "aaaaaa\nNot Found\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "datastructure\n3\nstruct\ndata\nalgo\n",
                "expected_stdout": "structure\ndatastructure\nNot Found\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【模板】KMP字符串匹配",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "串",
            "KMP模板",
            "前缀函数"
        ],
        "statement_md": "KMP 算法的完整模板题：\n\n1. 输出模式串 `T` 在主串 `S` 中**所有出现的位置**（起始下标从 1 开始，允许重叠；若未出现输出 `none`）；\n2. 输出模式串 `T` 每个前缀 `T[1..i]` 的**最长真公共前后缀长度 `pi[i]`**（即现代算法竞赛常用的 Border 数组，满足 `nxt[i] = pi[i-1] + 1`）。\n\n★ 把 `pi[i]` 和严蔚敏教材的 `next[j]` 对照着看：\n`ABABC` 的 `pi` 是 `0 0 1 2 0`，而教材 `next` 是 `0 1 1 2 3` —— 教材的 `next[j]` 正好等于 `pi[j-2] + 1`（`j ≥ 2`）。掌握这层换算，两套口径永远不会混。",
        "input_format": "第一行主串 `S`。\n\n第二行模式串 `T`。",
        "output_format": "第一行：`T` 在 `S` 中所有匹配的起始位置（1 起，空格分隔；无匹配输出 `none`）。\n\n第二行：`|T|` 个整数（空格分隔），依次表示 `T[1..i]` 的最长真公共前后缀长度。",
        "constraints_md": "- 1 ≤ |S|, |T| ≤ 10000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 04 讲 · 串、数组和广义表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <string.h>\nchar s[10005], t[10005];\nint pi[10005];\nint main(void) {\n    scanf(\"%s %s\", s, t);\n    int n = (int)strlen(s), m = (int)strlen(t);\n    pi[0] = 0;\n    for (int i = 1; i < m; i++) {\n        int j = pi[i - 1];\n        while (j > 0 && t[i] != t[j]) j = pi[j - 1];\n        if (t[i] == t[j]) j++;\n        pi[i] = j;\n    }\n    int first = 1, j = 0;\n    for (int i = 0; i < n; i++) {\n        while (j > 0 && s[i] != t[j]) j = pi[j - 1];\n        if (s[i] == t[j]) j++;\n        if (j == m) {\n            printf(first ? \"%d\" : \" %d\", i - m + 2);\n            first = 0;\n            j = pi[j - 1];               /* ★ 继续找重叠匹配 */\n        }\n    }\n    if (first) printf(\"none\");\n    printf(\"\\n\");\n    for (int i = 0; i < m; i++) printf(i ? \" %d\" : \"%d\", pi[i]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <string>\n#include <vector>\nusing namespace std;\nint main() {\n    string s, t; cin >> s >> t;\n    int n = (int)s.size(), m = (int)t.size();\n    vector<int> pos;\n    for (int i = 0; i + m <= n; i++)\n        if (s.compare(i, m, t) == 0) pos.push_back(i + 1);\n    if (pos.empty()) cout << \"none\\n\";\n    else {\n        for (size_t i = 0; i < pos.size(); i++) cout << (i ? \" \" : \"\") << pos[i];\n        cout << \"\\n\";\n    }\n    for (int i = 1; i <= m; i++) {\n        int best = 0;\n        for (int L = 1; L < i; L++)\n            if (t.compare(0, L, t, i - L, L) == 0) best = L;\n        cout << (i > 1 ? \" \" : \"\") << best;\n    }\n    cout << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "ABABABC\nABA\n",
                "expected_stdout": "1 3\n0 0 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "AAAAA\nAA\n",
                "expected_stdout": "1 2 3 4\n0 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "ABCDEFG\nXYZ\n",
                "expected_stdout": "none\n0 0 0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "AABAACAADAABAABA\nAABA\n",
                "expected_stdout": "1 10 13\n0 1 0 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "ABCABC\nABCABC\n",
                "expected_stdout": "1\n0 0 0 1 2 3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "好中缀",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "串",
            "KMP",
            "前后缀",
            "Border"
        ],
        "statement_md": "如果一个非空字符串 `T` 既是主串 `S` 的**前缀**、又是 `S` 的**后缀**，同时还在 `S` 的**内部**（即不作为整串首尾的位置 `2 ≤ i ≤ |S|-|T|`）出现过至少一次，就称 `T` 是 `S` 的一个**好中缀**。\n\n请找出 `S` **最长**的好中缀；若不存在，输出 `none`。\n\n★ KMP 思路：整个串的公共前后缀长度只能沿着 `pi[n-1] → pi[pi[n-1]-1] → …` 这条链取；而「在内部出现过」等价于该长度不超过内部位置的最大前缀函数值 `max(pi[1..n-2])`。",
        "input_format": "一行，一个非空字符串 `S`（不含空格）。",
        "output_format": "一行，最长的好中缀字符串；若不存在则输出 `none`。",
        "constraints_md": "- 1 ≤ |S| ≤ 5000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 04 讲 · 串、数组和广义表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <string.h>\nchar s[5005];\nint pi[5005];\nint main(void) {\n    scanf(\"%s\", s);\n    int n = (int)strlen(s);\n    pi[0] = 0;\n    int max_mid = 0;\n    for (int i = 1; i < n; i++) {\n        int j = pi[i - 1];\n        while (j > 0 && s[i] != s[j]) j = pi[j - 1];\n        if (s[i] == s[j]) j++;\n        pi[i] = j;\n        if (i < n - 1 && pi[i] > max_mid) max_mid = pi[i];\n    }\n    int L = pi[n - 1];\n    while (L > max_mid) L = pi[L - 1];\n    if (L == 0) printf(\"none\\n\");\n    else { s[L] = '\\0'; printf(\"%s\\n\", s); }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <string>\nusing namespace std;\nint main() {\n    string s; cin >> s;\n    int n = (int)s.size();\n    for (int L = n - 2; L >= 1; L--) {\n        if (s.compare(0, L, s, n - L, L) != 0) continue;\n        string cand = s.substr(0, L);\n        size_t p = s.find(cand, 1);\n        if (p != string::npos && (int)p + L < n) {\n            cout << cand << \"\\n\";\n            return 0;\n        }\n    }\n    cout << \"none\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "fixprefixsuffix\n",
                "expected_stdout": "fix\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "abcdabc\n",
                "expected_stdout": "none\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "aaaaa\n",
                "expected_stdout": "aaa\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "ababab\n",
                "expected_stdout": "ab\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "abcde\n",
                "expected_stdout": "none\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "ababa\n",
                "expected_stdout": "a\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "病毒变种",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "串",
            "环状串",
            "模式匹配"
        ],
        "statement_md": "教材案例 4.1「病毒感染检测」：由于病毒的 DNA 序列是**环状**的，长度为 `m` 的病毒序列可以从任意位置断开，形成 `m` 种线性变种（例如 `baa` 的变种有 `baa`、`aab`、`aba`）。\n\n给定若干对 `(病毒序列, 待测人类序列)`，判断每条待测人类序列中是否包含该病毒的**任意一种变种**。\n\n★ 环状串的经典破环成链技巧：把病毒串复制拼接成长度为 `2m` 的 `V + V`，里面所有长度为 `m` 的连续子串就恰好枚举了全部 `m` 种变种！",
        "input_format": "第一行正整数 `q`（检测组数）。\n\n随后 `q` 行，每行两个不含空格的字符串：`病毒DNA 人类DNA`。",
        "output_format": "`q` 行，若感染（含任意变种）输出 `YES`，否则输出 `NO`。",
        "constraints_md": "- 1 ≤ q ≤ 20\n- 1 ≤ |病毒DNA|, |人类DNA| ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 04 讲 · 串、数组和广义表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <string.h>\nchar v[1005], h[1005], vv[2010], pat[1005];\nint main(void) {\n    int q;\n    scanf(\"%d\", &q);\n    while (q--) {\n        scanf(\"%s %s\", v, h);\n        int m = (int)strlen(v);\n        strcpy(vv, v);\n        strcat(vv, v);\n        int hit = 0;\n        for (int i = 0; i < m; i++) {\n            strncpy(pat, vv + i, m);\n            pat[m] = '\\0';\n            if (strstr(h, pat) != NULL) { hit = 1; break; }\n        }\n        printf(hit ? \"YES\\n\" : \"NO\\n\");\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <string>\nusing namespace std;\nint main() {\n    int q; cin >> q;\n    while (q--) {\n        string v, h; cin >> v >> h;\n        int m = (int)v.size();\n        bool hit = false;\n        for (int i = 0; i < m; i++) {\n            string rot = v.substr(i) + v.substr(0, i);\n            if (h.find(rot) != string::npos) { hit = true; break; }\n        }\n        cout << (hit ? \"YES\\n\" : \"NO\\n\");\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4\naab bbaabbba\naab aabbaa\nabc acbxyz\nxyz xy\n",
                "expected_stdout": "YES\nYES\nNO\nNO\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\nabba bababbaa\nabc cab\n",
                "expected_stdout": "YES\nYES\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\na b\na a\nabcd cdab\n",
                "expected_stdout": "NO\nYES\nYES\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "矩阵鞍点查找",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "数组",
            "鞍点",
            "二维数组"
        ],
        "statement_md": "在一个 `n × m` 的矩阵中，若某个元素 `A[i][j]` 既是第 `i` 行的**最大值**（`≥` 同行所有元素），又是第 `j` 列的**最小值**（`≤` 同列所有元素），则称它为该矩阵的一个**鞍点**。\n\n请按行优先顺序找出第一个鞍点，输出它的行号、列号（均从 1 开始）与元素值；若不存在鞍点，输出 `NONE`。",
        "input_format": "第一行两个正整数 `n m`。\n\n随后 `n` 行，每行 `m` 个整数。",
        "output_format": "一行，输出 `row col value`；若无鞍点则输出 `NONE`。",
        "constraints_md": "- 1 ≤ n, m ≤ 100\n- |A[i][j]| ≤ 10^9",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 04 讲 · 串、数组和广义表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nint a[105][105], rmax[105], cmin[105];\nint main(void) {\n    int n, m;\n    scanf(\"%d %d\", &n, &m);\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < m; j++)\n            scanf(\"%d\", &a[i][j]);\n    for (int i = 0; i < n; i++) {\n        rmax[i] = a[i][0];\n        for (int j = 1; j < m; j++) if (a[i][j] > rmax[i]) rmax[i] = a[i][j];\n    }\n    for (int j = 0; j < m; j++) {\n        cmin[j] = a[0][j];\n        for (int i = 1; i < n; i++) if (a[i][j] < cmin[j]) cmin[j] = a[i][j];\n    }\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < m; j++)\n            if (a[i][j] == rmax[i] && a[i][j] == cmin[j]) {\n                printf(\"%d %d %d\\n\", i + 1, j + 1, a[i][j]);\n                return 0;\n            }\n    printf(\"NONE\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\nusing namespace std;\nint main() {\n    int n, m; cin >> n >> m;\n    vector<vector<int>> a(n, vector<int>(m));\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < m; j++) cin >> a[i][j];\n    for (int i = 0; i < n; i++) {\n        for (int j = 0; j < m; j++) {\n            bool ok = true;\n            for (int k = 0; k < m; k++) if (a[i][k] > a[i][j]) ok = false;\n            for (int k = 0; k < n; k++) if (a[k][j] < a[i][j]) ok = false;\n            if (ok) { cout << i + 1 << \" \" << j + 1 << \" \" << a[i][j] << \"\\n\"; return 0; }\n        }\n    }\n    cout << \"NONE\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3 3\n1 7 3\n4 5 6\n7 8 9\n",
                "expected_stdout": "NONE\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2 2\n1 2\n2 1\n",
                "expected_stdout": "NONE\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 4\n9 80 205 40\n90 -60 96 1\n210 -3 101 89\n",
                "expected_stdout": "2 3 96\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1 1\n5\n",
                "expected_stdout": "1 1 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "三元组顺序表表示的稀疏矩阵转置运算I",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "数组",
            "稀疏矩阵",
            "按列序转置"
        ],
        "statement_md": "教材算法 5.1（按列序朴素转置）：给定稀疏矩阵 `M` 的三元组顺序表（行优先），按列号 `col = 1..c` 外层循环、内层从头到尾扫描全部 `t` 个三元组，挑出列号等于 `col` 的元素并交换行列下标，依次填入转置矩阵 `T`。\n\n★ 为什么不能直接「把每个三元组的 row 和 col 对调完事」？因为原表按**行优先**排，直接对调后变成按**列优先**，不再是合法的行优先三元组顺序表！",
        "input_format": "第一行三个整数 `r c t`（行数、列数、非零元个数）。\n\n随后 `t` 行，每行 `row col value`（1 起，按行优先排列）。",
        "output_format": "第一行 `c r t`；随后 `t` 行输出转置后的行优先三元组 `row col value`。",
        "constraints_md": "- 1 ≤ r, c ≤ 500\n- 0 ≤ t ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 04 讲 · 串、数组和广义表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nint ar[1005], ac[1005], av[1005];\nint main(void) {\n    int r, c, t;\n    scanf(\"%d %d %d\", &r, &c, &t);\n    for (int k = 0; k < t; k++) scanf(\"%d %d %d\", &ar[k], &ac[k], &av[k]);\n    printf(\"%d %d %d\\n\", c, r, t);\n    for (int col = 1; col <= c; col++) {\n        for (int k = 0; k < t; k++) {\n            if (ac[k] == col) printf(\"%d %d %d\\n\", ac[k], ar[k], av[k]);\n        }\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <algorithm>\nusing namespace std;\nstruct E { int r, c, v; };\nint main() {\n    int r, c, t; cin >> r >> c >> t;\n    vector<E> a(t);\n    for (auto &x : a) { cin >> x.r >> x.c >> x.v; swap(x.r, x.c); }\n    sort(a.begin(), a.end(), [](const E &x, const E &y) {\n        return x.r != y.r ? x.r < y.r : x.c < y.c;\n    });\n    cout << c << \" \" << r << \" \" << t << \"\\n\";\n    for (auto &x : a) cout << x.r << \" \" << x.c << \" \" << x.v << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3 4 4\n1 2 12\n1 3 9\n3 1 -3\n3 4 14\n",
                "expected_stdout": "4 3 4\n1 3 -3\n2 1 12\n3 1 9\n4 3 14\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2 3 2\n1 3 5\n2 1 8\n",
                "expected_stdout": "3 2 2\n1 2 8\n3 1 5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 3 0\n",
                "expected_stdout": "3 3 0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4 2 3\n1 2 7\n2 1 6\n4 2 9\n",
                "expected_stdout": "2 4 3\n1 2 6\n2 1 7\n2 4 9\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "三元组顺序表表示的稀疏矩阵转置II",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "数组",
            "稀疏矩阵",
            "快速转置",
            "cpot"
        ],
        "statement_md": "教材算法 5.2（快速转置）的核心是先算出两张辅助向量：\n\n- `num[col]`：原矩阵第 `col` 列中非零元的个数；\n- `cpot[col]`：原矩阵第 `col` 列的第一个非零元在转置三元组表中的**位序**（从 **1** 开始）：\n  `cpot[1] = 1`，`cpot[col] = cpot[col-1] + num[col-1]`。\n\n本题要求**先把初始的 `num[1..c]` 和 `cpot[1..c]` 打出来**，再输出快速转置后的三元组表——专门检验你是不是真的算对了辅助数组，而不是拿排序糊弄过去。",
        "input_format": "第一行三个整数 `r c t`（1 ≤ r, c ≤ 500，0 ≤ t ≤ 1000）。\n\n随后 `t` 行，每行 `row col value`（1 起，按行优先排列）。",
        "output_format": "第一行：`num: num[1] num[2] ... num[c]`\n\n第二行：`cpot: cpot[1] cpot[2] ... cpot[c]`\n\n随后 `t` 行：转置后的三元组 `row col value`。",
        "constraints_md": "- 1 ≤ r, c ≤ 500\n- 0 ≤ t ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 04 讲 · 串、数组和广义表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nint ar[1005], ac[1005], av[1005];\nint br[1005], bc[1005], bv[1005];\nint num[505], cpot[505];\nint main(void) {\n    int r, c, t;\n    scanf(\"%d %d %d\", &r, &c, &t);\n    for (int col = 1; col <= c; col++) num[col] = 0;\n    for (int k = 0; k < t; k++) {\n        scanf(\"%d %d %d\", &ar[k], &ac[k], &av[k]);\n        num[ac[k]]++;\n    }\n    cpot[1] = 1;\n    for (int col = 2; col <= c; col++) cpot[col] = cpot[col - 1] + num[col - 1];\n    printf(\"num:\");\n    for (int col = 1; col <= c; col++) printf(\" %d\", num[col]);\n    printf(\"\\ncpot:\");\n    for (int col = 1; col <= c; col++) printf(\" %d\", cpot[col]);\n    printf(\"\\n\");\n    for (int k = 0; k < t; k++) {\n        int pos = cpot[ac[k]]++;\n        br[pos] = ac[k]; bc[pos] = ar[k]; bv[pos] = av[k];\n    }\n    for (int k = 1; k <= t; k++) printf(\"%d %d %d\\n\", br[k], bc[k], bv[k]);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <algorithm>\nusing namespace std;\nstruct E { int r, c, v; };\nint main() {\n    int r, c, t; cin >> r >> c >> t;\n    vector<E> a(t);\n    vector<int> num(c + 1, 0), cpot(c + 1, 0);\n    for (auto &x : a) { cin >> x.r >> x.c >> x.v; num[x.c]++; }\n    cpot[1] = 1;\n    for (int j = 2; j <= c; j++) cpot[j] = cpot[j - 1] + num[j - 1];\n    cout << \"num:\";\n    for (int j = 1; j <= c; j++) cout << \" \" << num[j];\n    cout << \"\\ncpot:\";\n    for (int j = 1; j <= c; j++) cout << \" \" << cpot[j];\n    cout << \"\\n\";\n    for (auto &x : a) swap(x.r, x.c);\n    stable_sort(a.begin(), a.end(), [](const E &x, const E &y) {\n        return x.r != y.r ? x.r < y.r : x.c < y.c;\n    });\n    for (auto &x : a) cout << x.r << \" \" << x.c << \" \" << x.v << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "6 7 8\n1 2 12\n1 3 9\n3 1 -3\n3 6 14\n4 3 24\n5 2 18\n6 1 15\n6 4 -7\n",
                "expected_stdout": "num: 2 2 2 1 0 1 0\ncpot: 1 3 5 7 8 8 9\n1 3 -3\n1 6 15\n2 1 12\n2 5 18\n3 1 9\n3 4 24\n4 6 -7\n6 3 14\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 4 3\n1 1 5\n2 3 7\n3 2 9\n",
                "expected_stdout": "num: 1 1 1 0\ncpot: 1 2 3 4\n1 1 5\n2 3 9\n3 2 7\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2 3 0\n",
                "expected_stdout": "num: 0 0 0\ncpot: 1 1 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3 3 4\n1 3 2\n2 1 4\n2 3 6\n3 2 8\n",
                "expected_stdout": "num: 1 1 2\ncpot: 1 2 3\n1 2 4\n2 3 8\n3 1 2\n3 2 6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "稀疏矩阵加法",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "数组",
            "稀疏矩阵",
            "矩阵加法",
            "双指针"
        ],
        "statement_md": "给定两个同型（`r × c`）稀疏矩阵 `A` 和 `B` 的行优先三元组顺序表，求 `C = A + B` 的行优先三元组顺序表。\n\n★ 两个关键点：\n1. 两个三元组表都已经按 `(row, col)` 字典序排好，用**二路归并双指针**扫一遍就能合并，复杂度 `O(t1 + t2)`；\n2. **正负抵消得 0 的项绝不能写进结果表**（三元组表只存非零元），否则非零元计数 `t3` 和表内容都会错！",
        "input_format": "第一行四个整数 `r c t1 t2`（行数、列数、A 的非零元数、B 的非零元数）。\n\n随后 `t1` 行给出 `A` 的三元组 `row col val`（行优先）。\n\n随后 `t2` 行给出 `B` 的三元组 `row col val`（行优先）。",
        "output_format": "第一行 `r c t3`；随后 `t3` 行按行优先输出 `C` 的非零三元组。",
        "constraints_md": "- 1 ≤ r, c ≤ 1000\n- 0 ≤ t1, t2 ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 04 讲 · 串、数组和广义表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nstruct E { int r, c, v; } a[1005], b[1005], res[2005];\nint cmp_pos(struct E x, struct E y) {\n    if (x.r != y.r) return x.r < y.r ? -1 : 1;\n    if (x.c != y.c) return x.c < y.c ? -1 : 1;\n    return 0;\n}\nint main(void) {\n    int r, c, t1, t2;\n    scanf(\"%d %d %d %d\", &r, &c, &t1, &t2);\n    for (int i = 0; i < t1; i++) scanf(\"%d %d %d\", &a[i].r, &a[i].c, &a[i].v);\n    for (int i = 0; i < t2; i++) scanf(\"%d %d %d\", &b[i].r, &b[i].c, &b[i].v);\n    int i = 0, j = 0, k = 0;\n    while (i < t1 && j < t2) {\n        int s = cmp_pos(a[i], b[j]);\n        if (s < 0) res[k++] = a[i++];\n        else if (s > 0) res[k++] = b[j++];\n        else {\n            int sum = a[i].v + b[j].v;\n            if (sum != 0) res[k++] = (struct E){a[i].r, a[i].c, sum};\n            i++; j++;\n        }\n    }\n    while (i < t1) res[k++] = a[i++];\n    while (j < t2) res[k++] = b[j++];\n    printf(\"%d %d %d\\n\", r, c, k);\n    for (int idx = 0; idx < k; idx++)\n        printf(\"%d %d %d\\n\", res[idx].r, res[idx].c, res[idx].v);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <map>\nusing namespace std;\nint main() {\n    int r, c, t1, t2;\n    cin >> r >> c >> t1 >> t2;\n    map<pair<int, int>, int> mp;\n    for (int i = 0; i < t1 + t2; i++) {\n        int rr, cc, vv; cin >> rr >> cc >> vv;\n        mp[{rr, cc}] += vv;\n    }\n    int cnt = 0;\n    for (auto &kv : mp) if (kv.second != 0) cnt++;\n    cout << r << \" \" << c << \" \" << cnt << \"\\n\";\n    for (auto &kv : mp)\n        if (kv.second != 0)\n            cout << kv.first.first << \" \" << kv.first.second << \" \" << kv.second << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3 3 3 3\n1 1 2\n1 3 5\n2 2 -4\n1 2 7\n1 3 -5\n2 2 9\n",
                "expected_stdout": "3 3 3\n1 1 2\n1 2 7\n2 2 5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2 2 2 2\n1 1 3\n2 2 -3\n1 1 -3\n2 2 3\n",
                "expected_stdout": "2 2 0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 4 2 0\n1 2 6\n3 4 8\n",
                "expected_stdout": "3 4 2\n1 2 6\n3 4 8\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2 3 1 2\n2 1 4\n1 3 9\n2 1 6\n",
                "expected_stdout": "2 3 2\n1 3 9\n2 1 10\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "稀疏矩阵乘法",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "数组",
            "稀疏矩阵",
            "矩阵乘法",
            "行逻辑链接"
        ],
        "statement_md": "给定稀疏矩阵 `A`（`r × k`）和 `B`（`k × c`）的三元组顺序表，求乘积矩阵 `C = A × B`（`r × c`）的行优先三元组顺序表。\n\n★ 教材「行逻辑链接顺序表」乘法思路：逐行处理 `A` 的第 `i` 行，开一个长度为 `c` 的累加器 `ctemp[1..c]`；对 `A` 第 `i` 行的每个非零元 `(i, m, av)`，去 `B` 的第 `m` 行把所有 `(m, j, bv)` 乘积累加进 `ctemp[j]`。第 `i` 行扫完后，`ctemp[1..c]` 中非零的项天然按列递增，直接输出即可！",
        "input_format": "第一行五个整数 `r k c t1 t2`。\n\n随后 `t1` 行给出 `A` 的三元组 `row col val`。\n\n随后 `t2` 行给出 `B` 的三元组 `row col val`。",
        "output_format": "第一行 `r c t3`；随后 `t3` 行按行优先输出 `C` 的非零三元组。",
        "constraints_md": "- 1 ≤ r, k, c ≤ 200\n- 0 ≤ t1, t2 ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 04 讲 · 串、数组和广义表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nstruct E { int r, c; long long v; } A[1005], B[1005], C[40005];\nlong long ctemp[205];\nint main(void) {\n    int r, k, c, t1, t2;\n    scanf(\"%d %d %d %d %d\", &r, &k, &c, &t1, &t2);\n    for (int i = 0; i < t1; i++) scanf(\"%d %d %lld\", &A[i].r, &A[i].c, &A[i].v);\n    for (int i = 0; i < t2; i++) scanf(\"%d %d %lld\", &B[i].r, &B[i].c, &B[i].v);\n    int t3 = 0, p = 0;\n    for (int row = 1; row <= r; row++) {\n        for (int col = 1; col <= c; col++) ctemp[col] = 0;\n        while (p < t1 && A[p].r == row) {\n            int mid = A[p].c;\n            for (int q = 0; q < t2; q++)\n                if (B[q].r == mid) ctemp[B[q].c] += A[p].v * B[q].v;\n            p++;\n        }\n        for (int col = 1; col <= c; col++)\n            if (ctemp[col] != 0) C[t3++] = (struct E){row, col, ctemp[col]};\n    }\n    printf(\"%d %d %d\\n\", r, c, t3);\n    for (int i = 0; i < t3; i++)\n        printf(\"%d %d %lld\\n\", C[i].r, C[i].c, C[i].v);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <map>\nusing namespace std;\nstruct E { int r, c; long long v; };\nint main() {\n    int r, k, c, t1, t2;\n    cin >> r >> k >> c >> t1 >> t2;\n    vector<E> A(t1), B(t2);\n    for (auto &x : A) cin >> x.r >> x.c >> x.v;\n    for (auto &x : B) cin >> x.r >> x.c >> x.v;\n    map<pair<int, int>, long long> mp;\n    for (auto &a : A)\n        for (auto &b : B)\n            if (a.c == b.r) mp[{a.r, b.c}] += a.v * b.v;\n    int cnt = 0;\n    for (auto &kv : mp) if (kv.second != 0) cnt++;\n    cout << r << \" \" << c << \" \" << cnt << \"\\n\";\n    for (auto &kv : mp)\n        if (kv.second != 0)\n            cout << kv.first.first << \" \" << kv.first.second << \" \" << kv.second << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "2 3 2 3 3\n1 1 2\n1 3 1\n2 2 3\n1 1 4\n2 2 5\n3 1 -8\n",
                "expected_stdout": "2 2 1\n2 2 15\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2 2 2 2 2\n1 1 1\n1 2 2\n1 1 2\n2 1 -1\n",
                "expected_stdout": "2 2 0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 3 3 2 2\n1 2 3\n3 1 4\n1 3 5\n2 1 6\n",
                "expected_stdout": "3 3 2\n1 1 18\n3 3 20\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2 3 2 0 2\n1 1 5\n2 2 7\n",
                "expected_stdout": "2 2 0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "最大子矩阵和问题",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "数组",
            "最大子矩阵和",
            "降维",
            "动态规划"
        ],
        "statement_md": "给定一个 `n × m` 的整数矩阵，求其中元素之和最大的**非空连续子矩阵**（至少包含 1 个元素），输出该最大和。\n\n★ 经典「二维压一维」技巧：\n固定子矩阵的上下边界 `r1` 和 `r2`，把 `[r1..r2]` 这一带每一列的元素加起来，就变成了一个长度为 `m` 的一维数组 `col[0..m-1]` —— 随后直接套第 02 讲的**一维最大子段和（Kadane 算法）**！复杂度从 `O(n²m²)` 降到 `O(n²m)`。",
        "input_format": "第一行两个正整数 `n m`。\n\n随后 `n` 行，每行 `m` 个整数。",
        "output_format": "一行一个整数，表示非空连续子矩阵的最大元素和。",
        "constraints_md": "- 1 ≤ n, m ≤ 80\n- -10^5 ≤ A[i][j] ≤ 10^5",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 04 讲 · 串、数组和广义表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nint a[85][85];\nlong long col[85];\nint main(void) {\n    int n, m;\n    scanf(\"%d %d\", &n, &m);\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < m; j++)\n            scanf(\"%d\", &a[i][j]);\n    long long best = a[0][0];\n    for (int r1 = 0; r1 < n; r1++) {\n        for (int j = 0; j < m; j++) col[j] = 0;\n        for (int r2 = r1; r2 < n; r2++) {\n            long long cur = 0;\n            for (int j = 0; j < m; j++) {\n                col[j] += a[r2][j];\n                cur = (cur > 0) ? (cur + col[j]) : col[j];\n                if (cur > best) best = cur;\n            }\n        }\n    }\n    printf(\"%lld\\n\", best);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <algorithm>\nusing namespace std;\nint main() {\n    int n, m; cin >> n >> m;\n    vector<vector<long long>> ps(n + 1, vector<long long>(m + 1, 0));\n    for (int i = 1; i <= n; i++)\n        for (int j = 1; j <= m; j++) {\n            long long v; cin >> v;\n            ps[i][j] = ps[i - 1][j] + ps[i][j - 1] - ps[i - 1][j - 1] + v;\n        }\n    long long best = ps[1][1];\n    for (int r1 = 1; r1 <= n; r1++) {\n        for (int r2 = r1; r2 <= n; r2++) {\n            long long min_pre = 0;\n            for (int c = 1; c <= m; c++) {\n                long long cur = ps[r2][c] - ps[r1 - 1][c];\n                best = max(best, cur - min_pre);\n                min_pre = min(min_pre, cur);\n            }\n        }\n    }\n    cout << best << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3 3\n0 -2 -7\n9 2 -6\n-4 1 -4\n",
                "expected_stdout": "11\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2 2\n-5 -2\n-9 -3\n",
                "expected_stdout": "-2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 4\n1 2 -1 -4\n-8 -3 4 2\n3 8 10 -8\n",
                "expected_stdout": "21\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1 5\n-2 3 -1 4 -5\n",
                "expected_stdout": "6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "广义表的表头与表尾",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "广义表",
            "表头表尾",
            "括号匹配"
        ],
        "statement_md": "给定一个**非空**广义表 `L`（如 `(a,(b,c),d)`），求它的**表头 `GetHead(L)`** 和**表尾 `GetTail(L)`**。\n\n★ 教材铁律（几乎每次考试必考）：\n- **表头**是广义表的第一个顶层元素，它**既可以是原子，也可以是子表**；\n- **表尾**是除去第一个顶层元素后**其余元素组成的广义表**，因此**表尾永远是一个表（外层必带括号 `(...)`）**！\n\n例如 `L = (a)` 的表头是 `a`，表尾是空表 `()`；`L = ((a,b),c)` 的表头是 `(a,b)`，表尾是 `(c)`。",
        "input_format": "一行，一个非空广义表字符串（外层以 `(` 开头、` )` 结尾，且不是 `()`）。",
        "output_format": "第一行输出表头 `GetHead(L)`；第二行输出表尾 `GetTail(L)`。",
        "constraints_md": "- 3 ≤ |L| ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 04 讲 · 串、数组和广义表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <string.h>\nchar s[1005];\nint main(void) {\n    scanf(\"%s\", s);\n    int n = (int)strlen(s);\n    int depth = 0, comma = -1;\n    for (int i = 1; i < n - 1; i++) {\n        if (s[i] == '(') depth++;\n        else if (s[i] == ')') depth--;\n        else if (s[i] == ',' && depth == 0) { comma = i; break; }\n    }\n    if (comma == -1) {\n        for (int i = 1; i < n - 1; i++) putchar(s[i]);\n        printf(\"\\n()\\n\");\n    } else {\n        for (int i = 1; i < comma; i++) putchar(s[i]);\n        printf(\"\\n(\");\n        for (int i = comma + 1; i < n - 1; i++) putchar(s[i]);\n        printf(\")\\n\");\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <string>\n#include <vector>\nusing namespace std;\nint main() {\n    string s; cin >> s;\n    string in = s.substr(1, s.size() - 2);\n    vector<string> items;\n    int d = 0, last = 0;\n    for (int i = 0; i < (int)in.size(); i++) {\n        if (in[i] == '(') d++;\n        else if (in[i] == ')') d--;\n        else if (in[i] == ',' && d == 0) {\n            items.push_back(in.substr(last, i - last));\n            last = i + 1;\n        }\n    }\n    items.push_back(in.substr(last));\n    cout << items[0] << \"\\n(\";\n    for (size_t i = 1; i < items.size(); i++)\n        cout << (i > 1 ? \",\" : \"\") << items[i];\n    cout << \")\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "(a,(b,c),d)\n",
                "expected_stdout": "a\n((b,c),d)\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "(a)\n",
                "expected_stdout": "a\n()\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "((a,b),c)\n",
                "expected_stdout": "(a,b)\n(c)\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "((),a)\n",
                "expected_stdout": "()\n(a)\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "(((a)))\n",
                "expected_stdout": "((a))\n()\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "建立与遍历二叉树",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "二叉树",
            "前序建树",
            "三种遍历"
        ],
        "statement_md": "根据带空指针标记 `#` 的扩展先序序列建立二叉树，依次输出它的**先序遍历**、**中序遍历**和**后序遍历**序列。\n\n★ 三种递归遍历在代码上**走的是完全同一条路线**（每个结点都被经过三次）：\n- 第 1 次经过时打印 → **先序**（根-左-右）\n- 第 2 次（从左子树回来）打印 → **中序**（左-根-右）\n- 第 3 次（从右子树回来）打印 → **后序**（左-右-根）",
        "input_format": "一行，带 `#` 空标记的先序序列（结点为大写字母）。",
        "output_format": "三行，依次为先序、中序、后序序列；若为空树则三行均输出 `empty`。",
        "constraints_md": "- 序列长度 ≤ 2000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 05 讲 · 树和二叉树",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <stdlib.h>\ntypedef struct Node { char c; struct Node *l, *r; } Node;\nchar s[2005];\nint pos;\nNode *build(void) {\n    char c = s[pos++];\n    if (c == '#' || c == '\\0') return NULL;\n    Node *t = (Node *)malloc(sizeof(Node));\n    t->c = c; t->l = build(); t->r = build();\n    return t;\n}\nvoid pre(Node *t)  { if (!t) return; putchar(t->c); pre(t->l); pre(t->r); }\nvoid ino(Node *t)  { if (!t) return; ino(t->l); putchar(t->c); ino(t->r); }\nvoid post(Node *t) { if (!t) return; post(t->l); post(t->r); putchar(t->c); }\nint main(void) {\n    scanf(\"%s\", s);\n    pos = 0;\n    Node *root = build();\n    if (!root) { printf(\"empty\\nempty\\nempty\\n\"); return 0; }\n    pre(root);  putchar('\\n');\n    ino(root);  putchar('\\n');\n    post(root); putchar('\\n');\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <string>\n#include <vector>\n#include <functional>\nusing namespace std;\nstruct N { char c; int l, r; };\nint main() {\n    string s; cin >> s;\n    vector<N> pool;\n    int pos = 0;\n    function<int()> build = [&]() -> int {\n        char c = s[pos++];\n        if (c == '#') return -1;\n        int id = (int)pool.size();\n        pool.push_back({c, -1, -1});\n        int l = build(), r = build();\n        pool[id].l = l; pool[id].r = r;\n        return id;\n    };\n    int root = build();\n    if (root < 0) { cout << \"empty\\nempty\\nempty\\n\"; return 0; }\n    string a, b, c;\n    function<void(int)> go = [&](int u) {\n        if (u < 0) return;\n        a += pool[u].c;\n        go(pool[u].l);\n        b += pool[u].c;\n        go(pool[u].r);\n        c += pool[u].c;\n    };\n    go(root);\n    cout << a << \"\\n\" << b << \"\\n\" << c << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "AB#D##C##\n",
                "expected_stdout": "ABDC\nBDAC\nDBCA\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "AB##C##\n",
                "expected_stdout": "ABC\nBAC\nBCA\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "#\n",
                "expected_stdout": "empty\nempty\nempty\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "A##\n",
                "expected_stdout": "A\nA\nA\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "ABD##E##CF##G##\n",
                "expected_stdout": "ABDECFG\nDBEAFCG\nDEBFGCA\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "交换二叉树中每个结点的左孩子和右孩子",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "二叉树",
            "镜像反转",
            "递归"
        ],
        "statement_md": "读入带 `#` 空标记的先序序列建立二叉树，把树中**每一个结点的左孩子和右孩子互换**（即二叉树的镜像翻转），然后输出翻转后的**中序遍历**和**先序遍历**。\n\n★ 值得想清楚的一个性质：镜像翻转后，新的**中序遍历**（左-根-右）恰好等于原树中序遍历的**整体逆序**（右-根-左）！",
        "input_format": "一行，带 `#` 空标记的先序序列。",
        "output_format": "第一行翻转后的中序序列，第二行翻转后的先序序列；空树输出两行 `empty`。",
        "constraints_md": "- 序列长度 ≤ 2000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 05 讲 · 树和二叉树",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <stdlib.h>\ntypedef struct Node { char c; struct Node *l, *r; } Node;\nchar s[2005];\nint pos;\nNode *build(void) {\n    char c = s[pos++];\n    if (c == '#' || c == '\\0') return NULL;\n    Node *t = (Node *)malloc(sizeof(Node));\n    t->c = c; t->l = build(); t->r = build();\n    return t;\n}\nvoid mirror(Node *t) {\n    if (!t) return;\n    Node *tmp = t->l; t->l = t->r; t->r = tmp;\n    mirror(t->l); mirror(t->r);\n}\nvoid ino(Node *t) { if (!t) return; ino(t->l); putchar(t->c); ino(t->r); }\nvoid pre(Node *t) { if (!t) return; putchar(t->c); pre(t->l); pre(t->r); }\nint main(void) {\n    scanf(\"%s\", s);\n    pos = 0;\n    Node *root = build();\n    if (!root) { printf(\"empty\\nempty\\n\"); return 0; }\n    mirror(root);\n    ino(root); putchar('\\n');\n    pre(root); putchar('\\n');\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <string>\n#include <vector>\n#include <functional>\nusing namespace std;\nstruct N { char c; int l, r; };\nint main() {\n    string s; cin >> s;\n    vector<N> pool;\n    int pos = 0;\n    function<int()> build = [&]() -> int {\n        char c = s[pos++];\n        if (c == '#') return -1;\n        int id = (int)pool.size();\n        pool.push_back({c, -1, -1});\n        int l = build(), r = build();\n        pool[id].l = l; pool[id].r = r;\n        return id;\n    };\n    int root = build();\n    if (root < 0) { cout << \"empty\\nempty\\n\"; return 0; }\n    /* 另一套：不改指针，遍历时直接先走右子树再走左子树 */\n    string ino, pre;\n    function<void(int)> go = [&](int u) {\n        if (u < 0) return;\n        pre += pool[u].c;\n        go(pool[u].r);\n        ino += pool[u].c;\n        go(pool[u].l);\n    };\n    go(root);\n    cout << ino << \"\\n\" << pre << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "AB#D##C##\n",
                "expected_stdout": "CADB\nACBD\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "AB##C##\n",
                "expected_stdout": "CAB\nACB\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "A##\n",
                "expected_stdout": "A\nA\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "#\n",
                "expected_stdout": "empty\nempty\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "ABD##E##C#F##\n",
                "expected_stdout": "FCAEBD\nACFBED\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "列出叶结点",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "二叉树",
            "静态链表",
            "找根",
            "层序遍历"
        ],
        "statement_md": "PTA 经典题 `List Leaves`：给定一棵二叉树的静态数组表示（结点编号 `0` ~ `N-1`），按**从上到下、从左到右**的顺序输出所有叶结点。\n\n★ 这道题最关键的第一步是**自己找根**：题目不会告诉你谁是根，但**根是唯一没有父结点的结点**（即没有出现在任何一行的左右孩子里，入度为 0）！找到根之后跑一遍队列 BFS，遇到左右孩子都为 `-` 的结点就输出。",
        "input_format": "第一行正整数 `N`（1 ≤ N ≤ 20）。\n\n随后 `N` 行，第 `i` 行（对应结点 `i`，从 0 开始）给出左孩子和右孩子编号；无该孩子则用 `-` 表示。",
        "output_format": "一行，按从上到下、从左到右顺序输出所有叶结点编号（空格分隔）。",
        "constraints_md": "- 1 ≤ N ≤ 20",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 05 讲 · 树和二叉树",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <stdlib.h>\nint L[25], R[25], indeg[25], q[25];\nint main(void) {\n    int n;\n    scanf(\"%d\", &n);\n    for (int i = 0; i < n; i++) {\n        char ls[8], rs[8];\n        scanf(\"%s %s\", ls, rs);\n        L[i] = (ls[0] == '-') ? -1 : atoi(ls);\n        R[i] = (rs[0] == '-') ? -1 : atoi(rs);\n        if (L[i] != -1) indeg[L[i]]++;\n        if (R[i] != -1) indeg[R[i]]++;\n    }\n    int root = 0;\n    for (int i = 0; i < n; i++) if (indeg[i] == 0) { root = i; break; }\n    int f = 0, r = 0, first = 1;\n    q[r++] = root;\n    while (f < r) {\n        int u = q[f++];\n        if (L[u] == -1 && R[u] == -1) {\n            printf(first ? \"%d\" : \" %d\", u);\n            first = 0;\n        }\n        if (L[u] != -1) q[r++] = L[u];\n        if (R[u] != -1) q[r++] = R[u];\n    }\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <string>\n#include <algorithm>\n#include <functional>\nusing namespace std;\nint main() {\n    int n; cin >> n;\n    vector<int> L(n, -1), R(n, -1), indeg(n, 0);\n    for (int i = 0; i < n; i++) {\n        string a, b; cin >> a >> b;\n        if (a != \"-\") { L[i] = stoi(a); indeg[L[i]]++; }\n        if (b != \"-\") { R[i] = stoi(b); indeg[R[i]]++; }\n    }\n    int root = 0;\n    for (int i = 0; i < n; i++) if (!indeg[i]) root = i;\n    vector<tuple<int, int, int>> leaves;\n    function<void(int, int, int)> dfs = [&](int u, int dep, int mask) {\n        if (u < 0) return;\n        if (L[u] < 0 && R[u] < 0) leaves.emplace_back(dep, mask, u);\n        dfs(L[u], dep + 1, mask * 2);\n        dfs(R[u], dep + 1, mask * 2 + 1);\n    };\n    dfs(root, 0, 0);\n    sort(leaves.begin(), leaves.end());\n    for (size_t i = 0; i < leaves.size(); i++)\n        cout << (i ? \" \" : \"\") << get<2>(leaves[i]);\n    cout << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "8\n1 -\n- -\n0 -\n2 7\n- -\n- -\n5 -\n4 6\n",
                "expected_stdout": "4 1 5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n- -\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n1 2\n- -\n- -\n",
                "expected_stdout": "1 2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n- 1\n- 2\n- 3\n- 4\n- -\n",
                "expected_stdout": "4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "还原二叉树",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "二叉树",
            "先序中序",
            "树高",
            "分治"
        ],
        "statement_md": "PTA 经典题 `还原二叉树`：给定一棵二叉树的**先序遍历序列**和**中序遍历序列**（结点为互不相同的字符），要求还原该二叉树并输出它的**高度（深度）**。\n\n★ 其实求高度根本不需要把指针树真正 `malloc` 出来：在分治切分 `[pl..pr]` 与 `[il..ir]` 的同时，直接返回 `1 + max(左子树高度, 右子树高度)`，10 行代码就能搞定！",
        "input_format": "第一行正整数 `N`（结点个数）。\n\n第二行长度为 `N` 的先序序列字符串。\n\n第三行长度为 `N` 的中序序列字符串。",
        "output_format": "一行一个整数，表示二叉树的高度。",
        "constraints_md": "- 1 ≤ N ≤ 60\n- 结点字符互不相同",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 05 讲 · 树和二叉树",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nchar pre[105], ino[105];\nint solve(int pl, int pr, int il, int ir) {\n    if (pl > pr) return 0;\n    int k = il;\n    while (ino[k] != pre[pl]) k++;\n    int ln = k - il;\n    int hl = solve(pl + 1, pl + ln, il, k - 1);\n    int hr = solve(pl + ln + 1, pr, k + 1, ir);\n    return 1 + (hl > hr ? hl : hr);\n}\nint main(void) {\n    int n;\n    scanf(\"%d %s %s\", &n, pre, ino);\n    printf(\"%d\\n\", solve(0, n - 1, 0, n - 1));\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <string>\n#include <algorithm>\n#include <functional>\nusing namespace std;\nint main() {\n    int n; string pre, ino;\n    cin >> n >> pre >> ino;\n    function<int(string, string)> h = [&](string p, string i) -> int {\n        if (p.empty()) return 0;\n        size_t k = i.find(p[0]);\n        return 1 + max(h(p.substr(1, k), i.substr(0, k)),\n                       h(p.substr(1 + k), i.substr(k + 1)));\n    };\n    cout << h(pre, ino) << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "9\nABDFGHIEC\nFDHGIBEAC\n",
                "expected_stdout": "5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\nA\nA\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\nABCD\nDCBA\n",
                "expected_stdout": "4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7\nABDECFG\nDBEAFCG\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "根据后序和中序遍历输出前序遍历",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "二叉树",
            "后序中序",
            "前序遍历"
        ],
        "statement_md": "给定一棵二叉树的**后序遍历**和**中序遍历**整数序列（结点值互不相同），输出它的先序遍历序列。\n\n★ 和「先序 + 中序求后序」正好镜像：\n- **后序的最后一个元素** `post[pr]` 就是当前子树的**根**；\n- 拿着根去中序里找到位置 `k`，算出左子树长度 `ln = k - il`；\n- 后序里左子树是 `[pl .. pl+ln-1]`，右子树是 `[pl+ln .. pr-1]`！",
        "input_format": "第一行正整数 `N`。\n\n第二行 `N` 个整数，表示后序遍历序列。\n\n第三行 `N` 个整数，表示中序遍历序列。",
        "output_format": "一行，格式为 `Preorder: v1 v2 ...`（冒号后与数字间均以单个空格分隔）。",
        "constraints_md": "- 1 ≤ N ≤ 30\n- 结点值互不相同",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 05 讲 · 树和二叉树",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nint post[35], ino[35];\nvoid solve(int pl, int pr, int il, int ir) {\n    if (pl > pr) return;\n    int root = post[pr];\n    printf(\" %d\", root);\n    int k = il;\n    while (ino[k] != root) k++;\n    int ln = k - il;\n    solve(pl, pl + ln - 1, il, k - 1);\n    solve(pl + ln, pr - 1, k + 1, ir);\n}\nint main(void) {\n    int n;\n    scanf(\"%d\", &n);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &post[i]);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &ino[i]);\n    printf(\"Preorder:\");\n    solve(0, n - 1, 0, n - 1);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <functional>\nusing namespace std;\nstruct N { int v, l, r; };\nint main() {\n    int n; cin >> n;\n    vector<int> post(n), ino(n);\n    for (int &x : post) cin >> x;\n    for (int &x : ino) cin >> x;\n    vector<N> pool;\n    function<int(int, int, int, int)> build = [&](int pl, int pr, int il, int ir) -> int {\n        if (pl > pr) return -1;\n        int root = post[pr], k = il;\n        while (ino[k] != root) k++;\n        int ln = k - il;\n        int id = (int)pool.size();\n        pool.push_back({root, -1, -1});\n        int l = build(pl, pl + ln - 1, il, k - 1);\n        int r = build(pl + ln, pr - 1, k + 1, ir);\n        pool[id].l = l; pool[id].r = r;\n        return id;\n    };\n    int rt = build(0, n - 1, 0, n - 1);\n    cout << \"Preorder:\";\n    vector<int> st{rt};\n    while (!st.empty()) {\n        int u = st.back(); st.pop_back();\n        if (u < 0) continue;\n        cout << \" \" << pool[u].v;\n        st.push_back(pool[u].r);\n        st.push_back(pool[u].l);\n    }\n    cout << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "7\n2 3 1 5 7 6 4\n1 2 3 4 5 6 7\n",
                "expected_stdout": "Preorder: 4 1 3 2 6 5 7\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n10\n10\n",
                "expected_stdout": "Preorder: 10\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n4 5 2 3 1\n4 2 5 1 3\n",
                "expected_stdout": "Preorder: 1 2 4 5 3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n4 3 2 1\n1 2 3 4\n",
                "expected_stdout": "Preorder: 1 2 3 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "树的遍历",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "二叉树",
            "后序中序",
            "层序遍历",
            "L2-006"
        ],
        "statement_md": "PTA 天梯赛经典题 `L2-006 树的遍历`：给定一棵二叉树的**后序遍历**和**中序遍历**，请你输出它的**层序遍历**序列。\n\n★ 两种写法都值得掌握：\n1. 标准写法：先由后序+中序递归建出二叉树，再用队列做一次 BFS；\n2. 巧算写法：递归切分时多传一个 `depth` 参数，由于左子树总是比右子树先递归，直接 `levels[depth].push_back(root)`，最后按层拼起来就是层序遍历！",
        "input_format": "第一行正整数 `N`。\n\n第二行 `N` 个整数，表示后序序列。\n\n第三行 `N` 个整数，表示中序序列。",
        "output_format": "一行，输出层序遍历序列（`N` 个整数，空格分隔）。",
        "constraints_md": "- 1 ≤ N ≤ 30\n- 结点值互不相同",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 05 讲 · 树和二叉树",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <stdlib.h>\ntypedef struct Node { int v; struct Node *l, *r; } Node;\nint post[35], ino[35];\nNode *build(int pl, int pr, int il, int ir) {\n    if (pl > pr) return NULL;\n    int root = post[pr], k = il;\n    while (ino[k] != root) k++;\n    int ln = k - il;\n    Node *t = (Node *)malloc(sizeof(Node));\n    t->v = root;\n    t->l = build(pl, pl + ln - 1, il, k - 1);\n    t->r = build(pl + ln, pr - 1, k + 1, ir);\n    return t;\n}\nint main(void) {\n    int n;\n    scanf(\"%d\", &n);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &post[i]);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &ino[i]);\n    Node *q[40];\n    int f = 0, r = 0, first = 1;\n    q[r++] = build(0, n - 1, 0, n - 1);\n    while (f < r) {\n        Node *u = q[f++];\n        printf(first ? \"%d\" : \" %d\", u->v);\n        first = 0;\n        if (u->l) q[r++] = u->l;\n        if (u->r) q[r++] = u->r;\n    }\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <functional>\nusing namespace std;\nint main() {\n    int n; cin >> n;\n    vector<int> post(n), ino(n);\n    for (int &x : post) cin >> x;\n    for (int &x : ino) cin >> x;\n    vector<vector<int>> lv(n);\n    function<void(int, int, int, int, int)> go = [&](int pl, int pr, int il, int ir, int d) {\n        if (pl > pr) return;\n        int root = post[pr], k = il;\n        while (ino[k] != root) k++;\n        int ln = k - il;\n        lv[d].push_back(root);\n        go(pl, pl + ln - 1, il, k - 1, d + 1);\n        go(pl + ln, pr - 1, k + 1, ir, d + 1);\n    };\n    go(0, n - 1, 0, n - 1, 0);\n    bool first = true;\n    for (auto &row : lv)\n        for (int v : row) { cout << (first ? \"\" : \" \") << v; first = false; }\n    cout << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "7\n2 3 1 5 7 6 4\n1 2 3 4 5 6 7\n",
                "expected_stdout": "4 1 6 3 5 7 2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n8\n8\n",
                "expected_stdout": "8\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n4 5 2 3 1\n4 2 5 1 3\n",
                "expected_stdout": "1 2 3 4 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n3 2 1 6 5 4\n1 2 3 4 5 6\n",
                "expected_stdout": "4 1 5 2 6 3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "玩转二叉树",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "二叉树",
            "前序中序",
            "镜面反转",
            "L2-011"
        ],
        "statement_md": "PTA 天梯赛经典题 `L2-011 玩转二叉树`：给定一棵二叉树的**中序遍历**和**前序遍历**，请你先将树做个**镜面反转**（交换每个结点的左、右孩子），再输出反转后的**层序遍历**序列。\n\n★ 注意输入顺序是**第一行中序、第二行前序**（别惯性当成先给前序）！而镜面反转后的层序遍历，只需在 BFS 入队时**先把右孩子入队、再把左孩子入队**即可。",
        "input_format": "第一行正整数 `N`。\n\n第二行 `N` 个整数，表示**中序**序列。\n\n第三行 `N` 个整数，表示**前序**序列。",
        "output_format": "一行，镜面反转后的层序遍历序列（空格分隔）。",
        "constraints_md": "- 1 ≤ N ≤ 30\n- 结点值互不相同",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 05 讲 · 树和二叉树",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <stdlib.h>\ntypedef struct Node { int v; struct Node *l, *r; } Node;\nint ino[35], pre[35];\nNode *build(int pl, int pr, int il, int ir) {\n    if (pl > pr) return NULL;\n    int root = pre[pl], k = il;\n    while (ino[k] != root) k++;\n    int ln = k - il;\n    Node *t = (Node *)malloc(sizeof(Node));\n    t->v = root;\n    t->l = build(pl + 1, pl + ln, il, k - 1);\n    t->r = build(pl + ln + 1, pr, k + 1, ir);\n    return t;\n}\nint main(void) {\n    int n;\n    scanf(\"%d\", &n);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &ino[i]);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &pre[i]);\n    Node *q[40];\n    int f = 0, r = 0, first = 1;\n    q[r++] = build(0, n - 1, 0, n - 1);\n    while (f < r) {\n        Node *u = q[f++];\n        printf(first ? \"%d\" : \" %d\", u->v);\n        first = 0;\n        if (u->r) q[r++] = u->r;     /* ★ 先右后左 = 镜面层序 */\n        if (u->l) q[r++] = u->l;\n    }\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <functional>\nusing namespace std;\nint main() {\n    int n; cin >> n;\n    vector<int> ino(n), pre(n);\n    for (int &x : ino) cin >> x;\n    for (int &x : pre) cin >> x;\n    vector<vector<int>> lv(n);\n    function<void(int, int, int, int, int)> go = [&](int pl, int pr, int il, int ir, int d) {\n        if (pl > pr) return;\n        int root = pre[pl], k = il;\n        while (ino[k] != root) k++;\n        int ln = k - il;\n        lv[d].push_back(root);\n        go(pl + ln + 1, pr, k + 1, ir, d + 1);   // ★ 先递归右子树，再递归左子树\n        go(pl + 1, pl + ln, il, k - 1, d + 1);\n    };\n    go(0, n - 1, 0, n - 1, 0);\n    bool first = true;\n    for (auto &row : lv)\n        for (int v : row) { cout << (first ? \"\" : \" \") << v; first = false; }\n    cout << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "7\n1 2 3 4 5 6 7\n4 1 3 2 6 5 7\n",
                "expected_stdout": "4 6 1 7 5 3 2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n5\n5\n",
                "expected_stdout": "5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n4 2 5 1 3\n1 2 4 5 3\n",
                "expected_stdout": "1 3 2 5 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n1 2 3 4\n1 2 3 4\n",
                "expected_stdout": "1 2 3 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "完全二叉树的层序遍历",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "完全二叉树",
            "顺序存储",
            "后序还原",
            "L2-035"
        ],
        "statement_md": "PTA 天梯赛经典题 `L2-035 完全二叉树的层序遍历`：给定一棵 `N` 个结点的**完全二叉树**的**后序遍历**序列，请输出它的**层序遍历**序列。\n\n★ 看似只给了后序（没给中序）怎么可能还原唯一二叉树？因为「**完全二叉树**」四个字已经把树的形状彻底锁死了！\n用一维数组 `tree[1..N]` 按层序编号存完全二叉树（结点 `u` 的左孩子是 `2u`、右孩子是 `2u+1`），对下标 `1..N` 跑一遍后序递归，边走边从输入里读一个数填进 `tree[u]`，最后把 `tree[1..N]` 从头到尾打印出来就是层序遍历！",
        "input_format": "第一行正整数 `N`。\n\n第二行 `N` 个整数，表示完全二叉树的后序遍历序列。",
        "output_format": "一行 `N` 个整数（空格分隔），表示该完全二叉树的层序遍历序列。",
        "constraints_md": "- 1 ≤ N ≤ 30",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 05 讲 · 树和二叉树",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nint n, post[35], tree[35], idx = 0;\nvoid fill_post(int u) {\n    if (u > n) return;\n    fill_post(2 * u);\n    fill_post(2 * u + 1);\n    tree[u] = post[idx++];\n}\nint main(void) {\n    scanf(\"%d\", &n);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &post[i]);\n    fill_post(1);\n    for (int i = 1; i <= n; i++) printf(i > 1 ? \" %d\" : \"%d\", tree[i]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <functional>\nusing namespace std;\nint main() {\n    int n; cin >> n;\n    vector<int> post(n);\n    for (int &x : post) cin >> x;\n    vector<int> order;\n    function<void(int)> dfs = [&](int u) {\n        if (u > n) return;\n        dfs(u * 2);\n        dfs(u * 2 + 1);\n        order.push_back(u);\n    };\n    dfs(1);\n    vector<int> ans(n + 1);\n    for (int i = 0; i < n; i++) ans[order[i]] = post[i];\n    for (int i = 1; i <= n; i++) cout << (i > 1 ? \" \" : \"\") << ans[i];\n    cout << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "8\n91 71 2 34 10 15 55 18\n",
                "expected_stdout": "18 34 55 71 2 10 15 91\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n42\n",
                "expected_stdout": "42\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n4 5 2 3 1\n",
                "expected_stdout": "1 2 3 4 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7\n1 2 3 4 5 6 7\n",
                "expected_stdout": "7 3 6 1 2 4 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "树层次遍历",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "树",
            "双亲表示法",
            "孩子链表",
            "层次遍历"
        ],
        "statement_md": "给定一棵含 `N` 个结点（编号 `1` ~ `N`）的**普通多叉树**（双亲表示法给出每个结点的父结点编号，根结点的父结点为 `0`），请按从上到下、同父结点的孩子按编号从小到大的顺序输出树的**层次遍历**。\n\n★ 普通树的存储转换：输入是**双亲表示法** `parent[i]`（找父亲 O(1)，找孩子慢），先扫一遍把每个 `i` 挂到 `children[parent[i]]` 里转成**孩子表示法**，就能直接跑 BFS 队列了！",
        "input_format": "第一行正整数 `N`。\n\n第二行 `N` 个整数 `p[1] p[2] ... p[N]`，表示结点 `1..N` 的父结点（根为 `0`）。",
        "output_format": "一行 `N` 个整数（空格分隔），表示树的层次遍历序列。",
        "constraints_md": "- 1 ≤ N ≤ 200",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 05 讲 · 树和二叉树",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nint head[205], nxt[205], to[205], ecnt = 0;\nint q[205];\n/* 按编号从大到小头插，遍历时正好从小到大 */\nint par[205];\nint main(void) {\n    int n, root = 1;\n    scanf(\"%d\", &n);\n    for (int i = 1; i <= n; i++) {\n        scanf(\"%d\", &par[i]);\n        if (par[i] == 0) root = i;\n    }\n    for (int i = n; i >= 1; i--) {\n        if (par[i] != 0) {\n            ++ecnt; to[ecnt] = i; nxt[ecnt] = head[par[i]]; head[par[i]] = ecnt;\n        }\n    }\n    int f = 0, r = 0;\n    q[r++] = root;\n    while (f < r) {\n        int u = q[f++];\n        printf(f == 1 ? \"%d\" : \" %d\", u);\n        for (int e = head[u]; e; e = nxt[e]) q[r++] = to[e];\n    }\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\nusing namespace std;\nint main() {\n    int n, root = 1; cin >> n;\n    vector<vector<int>> ch(n + 1);\n    for (int i = 1; i <= n; i++) {\n        int p; cin >> p;\n        if (p == 0) root = i;\n        else ch[p].push_back(i);\n    }\n    vector<int> cur{root}, out;\n    while (!cur.empty()) {\n        vector<int> nxt;\n        for (int u : cur) {\n            out.push_back(u);\n            for (int v : ch[u]) nxt.push_back(v);\n        }\n        cur = nxt;\n    }\n    for (size_t i = 0; i < out.size(); i++) cout << (i ? \" \" : \"\") << out[i];\n    cout << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "7\n0 1 1 2 2 2 3\n",
                "expected_stdout": "1 2 3 4 5 6 7\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n0\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "6\n2 0 2 1 1 3\n",
                "expected_stdout": "2 1 3 4 5 6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n0 1 2 3 4\n",
                "expected_stdout": "1 2 3 4 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "浪漫侧影",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "二叉树",
            "右视图",
            "左视图",
            "层序分层"
        ],
        "statement_md": "PTA 经典题 `浪漫侧影`：给定一棵二叉树的**中序遍历**和**后序遍历**序列，请你分别输出从树的右侧和左侧观察到的「侧影」：\n\n- **右视图（`R:`）**：从上到下每一层的**最右边**那个结点；\n- **左视图（`L:`）**：从上到下每一层的**最左边**那个结点。\n\n★ 按层 BFS（或带深度 `dep` 的先序 DFS）收集每一层的结点列表 `level[dep]`，每层的第一个元素就是左视图、最后一个元素就是右视图！",
        "input_format": "第一行正整数 `N`。\n\n第二行 `N` 个整数，表示**中序**序列。\n\n第三行 `N` 个整数，表示**后序**序列。",
        "output_format": "第一行：`R: r1 r2 ...`（从根层向下的右视图结点，空格分隔）\n\n第二行：`L: l1 l2 ...`（从根层向下的左视图结点，空格分隔）",
        "constraints_md": "- 1 ≤ N ≤ 30\n- 结点值互不相同",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 05 讲 · 树和二叉树",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nint ino[35], post[35], first_v[35], last_v[35], max_d = -1;\nvoid dfs(int pl, int pr, int il, int ir, int d) {\n    if (pl > pr) return;\n    if (d > max_d) { max_d = d; first_v[d] = post[pr]; }\n    last_v[d] = post[pr];\n    int k = il;\n    while (ino[k] != post[pr]) k++;\n    int ln = k - il;\n    dfs(pl, pl + ln - 1, il, k - 1, d + 1);\n    dfs(pl + ln, pr - 1, k + 1, ir, d + 1);\n}\nint main(void) {\n    int n;\n    scanf(\"%d\", &n);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &ino[i]);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &post[i]);\n    dfs(0, n - 1, 0, n - 1, 0);\n    printf(\"R:\");\n    for (int d = 0; d <= max_d; d++) printf(\" %d\", last_v[d]);\n    printf(\"\\nL:\");\n    for (int d = 0; d <= max_d; d++) printf(\" %d\", first_v[d]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <functional>\nusing namespace std;\nstruct N { int v, l, r; };\nint main() {\n    int n; cin >> n;\n    vector<int> ino(n), post(n);\n    for (int &x : ino) cin >> x;\n    for (int &x : post) cin >> x;\n    vector<N> pool;\n    function<int(int, int, int, int)> build = [&](int pl, int pr, int il, int ir) -> int {\n        if (pl > pr) return -1;\n        int root = post[pr], k = il;\n        while (ino[k] != root) k++;\n        int ln = k - il;\n        int id = (int)pool.size();\n        pool.push_back({root, -1, -1});\n        int l = build(pl, pl + ln - 1, il, k - 1);\n        int r = build(pl + ln, pr - 1, k + 1, ir);\n        pool[id].l = l; pool[id].r = r;\n        return id;\n    };\n    vector<int> cur{build(0, n - 1, 0, n - 1)}, R, L;\n    while (!cur.empty()) {\n        L.push_back(pool[cur.front()].v);\n        R.push_back(pool[cur.back()].v);\n        vector<int> nxt;\n        for (int u : cur) {\n            if (pool[u].l >= 0) nxt.push_back(pool[u].l);\n            if (pool[u].r >= 0) nxt.push_back(pool[u].r);\n        }\n        cur = nxt;\n    }\n    cout << \"R:\";\n    for (int v : R) cout << \" \" << v;\n    cout << \"\\nL:\";\n    for (int v : L) cout << \" \" << v;\n    cout << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "8\n6 8 7 4 5 1 3 2\n8 5 4 7 6 3 2 1\n",
                "expected_stdout": "R: 1 2 3 4 5\nL: 1 6 7 8 5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n9\n9\n",
                "expected_stdout": "R: 9\nL: 9\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n4 2 5 1 3\n4 5 2 3 1\n",
                "expected_stdout": "R: 1 3 5\nL: 1 2 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7\n1 2 3 4 5 6 7\n2 3 1 5 7 6 4\n",
                "expected_stdout": "R: 4 6 7 2\nL: 4 1 3 2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "二叉树的最大宽度与层号",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "二叉树",
            "宽度",
            "层序统计"
        ],
        "statement_md": "二叉树的**宽度**定义为各层结点数的最大值（根在第 1 层）。给定带 `#` 空标记的先序序列（保证非空树），求该二叉树的**最大宽度**以及达到最大宽度的**最小层号**。",
        "input_format": "一行，带 `#` 空标记的先序序列（非空树）。",
        "output_format": "一行两个整数，空格分隔：`最大宽度 对应层号`。",
        "constraints_md": "- 序列长度 ≤ 2000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 05 讲 · 树和二叉树",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nchar s[2005];\nint pos = 0, cnt[2005], max_d = 0;\nvoid dfs(int d) {\n    char c = s[pos++];\n    if (c == '#' || c == '\\0') return;\n    cnt[d]++;\n    if (d > max_d) max_d = d;\n    dfs(d + 1);\n    dfs(d + 1);\n}\nint main(void) {\n    scanf(\"%s\", s);\n    dfs(1);\n    int bw = 0, bl = 1;\n    for (int d = 1; d <= max_d; d++)\n        if (cnt[d] > bw) { bw = cnt[d]; bl = d; }\n    printf(\"%d %d\\n\", bw, bl);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <string>\n#include <vector>\n#include <functional>\nusing namespace std;\nstruct N { int l, r; };\nint main() {\n    string s; cin >> s;\n    vector<N> pool;\n    int pos = 0;\n    function<int()> build = [&]() -> int {\n        if (s[pos++] == '#') return -1;\n        int id = (int)pool.size();\n        pool.push_back({-1, -1});\n        int l = build(), r = build();\n        pool[id].l = l; pool[id].r = r;\n        return id;\n    };\n    vector<int> cur{build()};\n    int bw = 0, bl = 1, lv = 1;\n    while (!cur.empty()) {\n        if ((int)cur.size() > bw) { bw = (int)cur.size(); bl = lv; }\n        vector<int> nxt;\n        for (int u : cur) {\n            if (pool[u].l >= 0) nxt.push_back(pool[u].l);\n            if (pool[u].r >= 0) nxt.push_back(pool[u].r);\n        }\n        cur = nxt; lv++;\n    }\n    cout << bw << \" \" << bl << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "ABD##E##CF##G##\n",
                "expected_stdout": "4 3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "AB#D##C##\n",
                "expected_stdout": "2 2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "A##\n",
                "expected_stdout": "1 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "ABC####\n",
                "expected_stdout": "1 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "二叉树的最近公共祖先（LCA）",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "二叉树",
            "LCA",
            "最近公共祖先",
            "递归"
        ],
        "statement_md": "给定一棵 `N` 个结点的二叉树的**先序遍历**和**中序遍历**（结点值互不相同），以及 `Q` 次询问 `(u, v)`，每次输出结点 `u` 和 `v` 的**最近公共祖先（LCA）**。\n\n★ 递归求 LCA 的经典三分支：\n- 若当前根为空，或等于 `u` 或 `v`，直接返回当前根；\n- 递归查左子树和右子树：若两边都返回非空，说明 `u`、`v` 分居左右两侧，当前根就是 LCA；\n- 否则哪边非空就返回哪边！",
        "input_format": "第一行两个正整数 `N Q`。\n\n第二行 `N` 个整数（先序遍历）。\n\n第三行 `N` 个整数（中序遍历）。\n\n随后 `Q` 行，每行两个整数 `u v`（保证在树中）。",
        "output_format": "`Q` 行，每行输出对应询问的最近公共祖先结点值。",
        "constraints_md": "- 1 ≤ N ≤ 200\n- 1 ≤ Q ≤ 200",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 05 讲 · 树和二叉树",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <stdlib.h>\ntypedef struct Node { int v; struct Node *l, *r; } Node;\nint pre[205], ino[205];\nNode *build(int pl, int pr, int il, int ir) {\n    if (pl > pr) return NULL;\n    int root = pre[pl], k = il;\n    while (ino[k] != root) k++;\n    int ln = k - il;\n    Node *t = (Node *)malloc(sizeof(Node));\n    t->v = root;\n    t->l = build(pl + 1, pl + ln, il, k - 1);\n    t->r = build(pl + ln + 1, pr, k + 1, ir);\n    return t;\n}\nNode *lca(Node *t, int u, int v) {\n    if (!t || t->v == u || t->v == v) return t;\n    Node *L = lca(t->l, u, v);\n    Node *R = lca(t->r, u, v);\n    if (L && R) return t;\n    return L ? L : R;\n}\nint main(void) {\n    int n, q;\n    scanf(\"%d %d\", &n, &q);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &pre[i]);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &ino[i]);\n    Node *root = build(0, n - 1, 0, n - 1);\n    while (q--) {\n        int u, v; scanf(\"%d %d\", &u, &v);\n        printf(\"%d\\n\", lca(root, u, v)->v);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <map>\n#include <functional>\nusing namespace std;\nint main() {\n    int n, q; cin >> n >> q;\n    vector<int> pre(n), ino(n);\n    for (int &x : pre) cin >> x;\n    for (int &x : ino) cin >> x;\n    map<int, int> par, dep;\n    function<void(int, int, int, int, int, int)> go = [&](int pl, int pr, int il, int ir, int p, int d) {\n        if (pl > pr) return;\n        int root = pre[pl], k = il;\n        while (ino[k] != root) k++;\n        int ln = k - il;\n        par[root] = p; dep[root] = d;\n        go(pl + 1, pl + ln, il, k - 1, root, d + 1);\n        go(pl + ln + 1, pr, k + 1, ir, root, d + 1);\n    };\n    go(0, n - 1, 0, n - 1, 0, 0);\n    while (q--) {\n        int u, v; cin >> u >> v;\n        while (dep[u] > dep[v]) u = par[u];\n        while (dep[v] > dep[u]) v = par[v];\n        while (u != v) { u = par[u]; v = par[v]; }\n        cout << u << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "8 4\n5 3 2 1 4 8 6 7\n1 2 3 4 5 6 7 8\n1 4\n2 4\n6 7\n1 7\n",
                "expected_stdout": "3\n3\n6\n5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 2\n1 2 3\n2 1 3\n2 3\n2 1\n",
                "expected_stdout": "1\n1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5 3\n1 2 3 4 5\n5 4 3 2 1\n5 3\n4 2\n1 5\n",
                "expected_stdout": "3\n2\n1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "修理牧场",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "哈夫曼树",
            "优先队列",
            "贪心",
            "锯木头"
        ],
        "statement_md": "PTA 经典题 `05-树8 修理牧场`：农夫要把一根长木头锯成给定的 `N` 段。\n每次把一根长度为 `L` 的木头锯成两段，需要花费 `L` 个铜板。\n求把木头锯成这 `N` 段的**最少总花费**。\n\n★ 逆向思维：正向看是「一根长木头不断一分为二」，倒过来看就是「每次挑两根最短的木头粘合起来」—— 花费恰好等于**哈夫曼树的带权路径长度 WPL**！\n注意边界：若 `N = 1`，木头本来就是一整段，一刀都不用锯，花费为 `0`。",
        "input_format": "第一行正整数 `N`。\n\n第二行 `N` 个正整数，表示每段木头的长度。",
        "output_format": "一行一个整数，表示最少总花费。",
        "constraints_md": "- 1 ≤ N ≤ 10000\n- 每段长度 ≤ 10^5",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 05 讲 · 树和二叉树",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <iostream>\n#include <queue>\n#include <vector>\nusing namespace std;\nint main() {\n    int n; cin >> n;\n    priority_queue<long long, vector<long long>, greater<long long>> pq;\n    for (int i = 0; i < n; i++) { long long v; cin >> v; pq.push(v); }\n    long long ans = 0;\n    while (pq.size() > 1) {\n        long long a = pq.top(); pq.pop();\n        long long b = pq.top(); pq.pop();\n        ans += a + b;\n        pq.push(a + b);\n    }\n    cout << ans << \"\\n\";\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <queue>\n#include <algorithm>\nusing namespace std;\n/* 另一套：双队列线性哈夫曼算法（初始排序放 q1，合成结点放 q2，永远单调递增） */\nint main() {\n    int n; cin >> n;\n    vector<long long> a(n);\n    for (auto &v : a) cin >> v;\n    if (n <= 1) { cout << 0 << \"\\n\"; return 0; }\n    sort(a.begin(), a.end());\n    queue<long long> q1, q2;\n    for (auto v : a) q1.push(v);\n    auto pop_min = [&]() -> long long {\n        if (q2.empty() || (!q1.empty() && q1.front() <= q2.front())) {\n            long long v = q1.front(); q1.pop(); return v;\n        }\n        long long v = q2.front(); q2.pop(); return v;\n    };\n    long long ans = 0;\n    for (int k = 1; k < n; k++) {\n        long long s = pop_min() + pop_min();\n        ans += s;\n        q2.push(s);\n    }\n    cout << ans << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "8\n4 5 1 2 1 3 1 1\n",
                "expected_stdout": "49\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n25\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n8 5 8\n",
                "expected_stdout": "34\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n10 20 30 40\n",
                "expected_stdout": "190\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "哈夫曼树",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 25,
        "tags": [
            "哈夫曼树",
            "前缀编码",
            "最优性判定",
            "Trie"
        ],
        "statement_md": "PTA 经典题 `Huffman Codes`：哈夫曼编码的形态**不唯一**（同权结点谁左谁右、谁先合并都可能不同），但任何一套合法的最优哈夫曼编码都必须同时满足两条铁律：\n\n1. **带权路径长度最优**：`Σ(w[i] × |code[i]|)` 恰好等于哈夫曼树的最小 `WPL`；\n2. **前缀码性质**：没有任何一个编码是另一个编码的前缀（即字符全部住在叶子上）。\n\n给定 `N` 个字符的权值与 `M` 套候选编码方案，请先输出最优 `WPL`，再逐套判定是否合法（`YES` / `NO`）。",
        "input_format": "第一行整数 `N`（2 ≤ N ≤ 60）。\n\n第二行 `N` 个正整数 `w[1..N]`。\n\n第三行正整数 `M`（候选方案数）。\n\n随后 `M` 组，每组 `N` 行，第 `i` 行为第 `i` 个字符的 `0/1` 编码串。",
        "output_format": "第一行输出最优 `WPL`；随后 `M` 行每行输出 `YES` 或 `NO`。",
        "constraints_md": "- 2 ≤ N ≤ 60\n- 1 ≤ M ≤ 20\n- 1 ≤ |编码串| ≤ 60",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 05 讲 · 树和二叉树",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <iostream>\n#include <vector>\n#include <string>\n#include <queue>\nusing namespace std;\nstruct Trie { int ch[2] = {0, 0}; bool end = false; };\nint main() {\n    int n; cin >> n;\n    vector<long long> w(n);\n    priority_queue<long long, vector<long long>, greater<long long>> pq;\n    for (int i = 0; i < n; i++) { cin >> w[i]; pq.push(w[i]); }\n    long long wpl = 0;\n    while (pq.size() > 1) {\n        long long a = pq.top(); pq.pop();\n        long long b = pq.top(); pq.pop();\n        wpl += a + b; pq.push(a + b);\n    }\n    cout << wpl << \"\\n\";\n    int m; cin >> m;\n    while (m--) {\n        vector<string> c(n);\n        long long tot = 0;\n        for (int i = 0; i < n; i++) { cin >> c[i]; tot += w[i] * (long long)c[i].size(); }\n        vector<Trie> tr(1);\n        bool ok = (tot == wpl);\n        for (int i = 0; i < n && ok; i++) {\n            int u = 0;\n            for (char b : c[i]) {\n                int d = b - '0';\n                if (!tr[u].ch[d]) { tr[u].ch[d] = (int)tr.size(); tr.push_back(Trie()); }\n                u = tr[u].ch[d];\n                if (tr[u].end) ok = false;\n            }\n            if (tr[u].ch[0] || tr[u].ch[1]) ok = false;\n            tr[u].end = true;\n        }\n        cout << (ok ? \"YES\\n\" : \"NO\\n\");\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <string>\n#include <algorithm>\nusing namespace std;\nint main() {\n    int n; cin >> n;\n    vector<long long> w(n), hp;\n    for (int i = 0; i < n; i++) { cin >> w[i]; hp.push_back(w[i]); }\n    long long wpl = 0;\n    while (hp.size() > 1) {\n        sort(hp.begin(), hp.end());\n        long long s = hp[0] + hp[1];\n        wpl += s;\n        hp.erase(hp.begin(), hp.begin() + 2);\n        hp.push_back(s);\n    }\n    cout << wpl << \"\\n\";\n    int m; cin >> m;\n    while (m--) {\n        vector<string> c(n);\n        long long tot = 0;\n        for (int i = 0; i < n; i++) { cin >> c[i]; tot += w[i] * (long long)c[i].size(); }\n        sort(c.begin(), c.end());\n        bool ok = (tot == wpl);\n        for (int i = 0; i + 1 < n && ok; i++)\n            if (c[i + 1].compare(0, c[i].size(), c[i]) == 0) ok = false;\n        cout << (ok ? \"YES\\n\" : \"NO\\n\");\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4\n1 1 3 3\n3\n000\n001\n01\n1\n01\n01\n0\n1\n00\n01\n10\n11\n",
                "expected_stdout": "15\nYES\nNO\nNO\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n2 3 6\n2\n00\n01\n1\n0\n10\n11\n",
                "expected_stdout": "16\nYES\nNO\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n5 5\n2\n0\n1\n0\n01\n",
                "expected_stdout": "10\nYES\nNO\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "朋友圈",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "并查集",
            "连通块大小",
            "等价类"
        ],
        "statement_md": "PTA 经典题 `朋友圈`：学校里有 `N` 个学生（编号 `1` ~ `N`）和 `M` 个俱乐部。\n每个俱乐部里的学生都是朋友，而且「朋友的朋友也是朋友」（传递性）。请计算**最大的朋友圈**里有多少个学生。\n\n★ 并查集的经典「按大小合并」：维护 `sz[root]` 表示以 `root` 为代表元的集合大小，每次合并两个不同集合 `ru` 和 `rv` 时令 `sz[ru] += sz[rv]`；最后取 `max(sz)` 即可！",
        "input_format": "第一行两个整数 `N M`（学生总数、俱乐部个数）。\n\n随后 `M` 行，每行先给一个正整数 `k`，后跟 `k` 个学生编号。",
        "output_format": "一行一个整数，表示最大朋友圈的人数。",
        "constraints_md": "- 1 ≤ N ≤ 30000\n- 0 ≤ M ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 05 讲 · 树和二叉树",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nint par[30005], sz[30005];\nint find(int x) {\n    while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }\n    return x;\n}\nint main(void) {\n    int n, m;\n    scanf(\"%d %d\", &n, &m);\n    for (int i = 1; i <= n; i++) { par[i] = i; sz[i] = 1; }\n    for (int i = 0; i < m; i++) {\n        int k, first, x;\n        scanf(\"%d %d\", &k, &first);\n        for (int j = 1; j < k; j++) {\n            scanf(\"%d\", &x);\n            int a = find(first), b = find(x);\n            if (a != b) { par[b] = a; sz[a] += sz[b]; }\n        }\n    }\n    int best = 1;\n    for (int i = 1; i <= n; i++) if (find(i) == i && sz[i] > best) best = sz[i];\n    printf(\"%d\\n\", best);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <queue>\nusing namespace std;\n/* 另一套：学生 (1..n) 与俱乐部 (n+1..n+m) 建二分图，跑 BFS 统计连通块里的学生数 */\nint main() {\n    int n, m; cin >> n >> m;\n    vector<vector<int>> g(n + m + 1);\n    for (int i = 1; i <= m; i++) {\n        int k; cin >> k;\n        while (k--) {\n            int u; cin >> u;\n            g[u].push_back(n + i);\n            g[n + i].push_back(u);\n        }\n    }\n    vector<char> vis(n + m + 1, 0);\n    int best = 1;\n    for (int s = 1; s <= n; s++) {\n        if (vis[s]) continue;\n        int cnt = 0;\n        queue<int> q; q.push(s); vis[s] = 1;\n        while (!q.empty()) {\n            int u = q.front(); q.pop();\n            if (u <= n) cnt++;\n            for (int v : g[u]) if (!vis[v]) { vis[v] = 1; q.push(v); }\n        }\n        if (cnt > best) best = cnt;\n    }\n    cout << best << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "7 4\n3 1 2 3\n2 1 4\n3 5 6 7\n1 6\n",
                "expected_stdout": "4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5 0\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "6 3\n2 1 2\n2 3 4\n3 2 3 6\n",
                "expected_stdout": "5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4 2\n2 1 2\n2 1 2\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "部落",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "并查集",
            "连通分量",
            "L2-024"
        ],
        "statement_md": "PTA 天梯赛经典题 `L2-024 部落`：社区里有若干个小圈子，只要两个人出现在同一个小圈子里，他们就属于同一个**部落**（部落关系具有传递性）。\n\n给定 `N` 个小圈子的成员名单，请你：\n1. 统计社区里的**总人数**（出现过的不同人员编号个数）与互不相交的**部落总数**；\n2. 对随后的 `Q` 次询问 `(u, v)`，判断两人是否属于同一个部落（输出 `Y` 或 `N`）。",
        "input_format": "第一行正整数 `N`（小圈子个数）。\n\n随后 `N` 行，每行格式为 `k p1 p2 ... pk`（圈子人数与成员编号，编号为 1~10000 内的正整数）。\n\n接着一行正整数 `Q`，随后 `Q` 行每行两个编号 `u v`。",
        "output_format": "第一行两个整数：`社区总人数 部落数`。\n\n随后 `Q` 行，每行输出 `Y` 或 `N`。",
        "constraints_md": "- 1 ≤ N, Q ≤ 1000\n- 1 ≤ 编号 ≤ 10000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 05 讲 · 树和二叉树",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nint par[10005], seen[10005];\nint find(int x) {\n    while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }\n    return x;\n}\nint main(void) {\n    for (int i = 1; i <= 10000; i++) par[i] = i;\n    int n;\n    scanf(\"%d\", &n);\n    while (n--) {\n        int k, first, x;\n        scanf(\"%d %d\", &k, &first);\n        seen[first] = 1;\n        for (int i = 1; i < k; i++) {\n            scanf(\"%d\", &x);\n            seen[x] = 1;\n            int a = find(first), b = find(x);\n            if (a != b) par[b] = a;\n        }\n    }\n    int tot = 0, tribes = 0;\n    for (int i = 1; i <= 10000; i++) {\n        if (seen[i]) {\n            tot++;\n            if (find(i) == i) tribes++;\n        }\n    }\n    printf(\"%d %d\\n\", tot, tribes);\n    int q;\n    scanf(\"%d\", &q);\n    while (q--) {\n        int u, v;\n        scanf(\"%d %d\", &u, &v);\n        printf(find(u) == find(v) ? \"Y\\n\" : \"N\\n\");\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <queue>\nusing namespace std;\nint main() {\n    int n; cin >> n;\n    vector<vector<int>> g(10005);\n    vector<char> seen(10005, 0);\n    while (n--) {\n        int k, first; cin >> k >> first;\n        seen[first] = 1;\n        for (int i = 1; i < k; i++) {\n            int x; cin >> x; seen[x] = 1;\n            g[first].push_back(x);\n            g[x].push_back(first);\n        }\n    }\n    vector<int> comp(10005, 0);\n    int tot = 0, cid = 0;\n    for (int i = 1; i <= 10000; i++) {\n        if (!seen[i]) continue;\n        tot++;\n        if (comp[i]) continue;\n        cid++;\n        queue<int> q; q.push(i); comp[i] = cid;\n        while (!q.empty()) {\n            int u = q.front(); q.pop();\n            for (int v : g[u]) if (!comp[v]) { comp[v] = cid; q.push(v); }\n        }\n    }\n    cout << tot << \" \" << cid << \"\\n\";\n    int qq; cin >> qq;\n    while (qq--) {\n        int u, v; cin >> u >> v;\n        cout << (comp[u] == comp[v] ? \"Y\\n\" : \"N\\n\");\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4\n3 10 1 2\n2 3 4\n4 1 5 7 8\n3 9 6 4\n2\n10 5\n3 7\n",
                "expected_stdout": "10 2\nY\nN\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n2 1 2\n2 3 4\n2\n1 2\n2 3\n",
                "expected_stdout": "4 2\nY\nN\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n1 1\n1 2\n1 3\n2\n1 2\n1 1\n",
                "expected_stdout": "3 3\nN\nY\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "邻接矩阵表示法创建无向图",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "图",
            "邻接矩阵",
            "顶点度"
        ],
        "statement_md": "用**邻接矩阵**表示一个含 `n` 个顶点（编号 `1` ~ `n`）、`m` 条边的无向图，输出该 `n × n` 的 `0/1` 邻接矩阵，并在最后一行输出每个顶点的**度（degree）**。\n\n★ 无向图邻接矩阵的两条基本性质：\n1. 矩阵一定关于主对角线**对称**（读入边 `(u, v)` 时必须同时置 `G[u][v] = G[v][u] = 1`）；\n2. 第 `i` 行（或第 `i` 列）元素之和就是顶点 `i` 的**度**！",
        "input_format": "第一行两个整数 `n m`。\n\n随后 `m` 行，每行两个整数 `u v` 表示一条无向边（无重边、无自环）。",
        "output_format": "前 `n` 行输出邻接矩阵（每行 `n` 个 `0/1` 整数，空格分隔）；第 `n+1` 行输出 `n` 个顶点的度（空格分隔）。",
        "constraints_md": "- 1 ≤ n ≤ 100\n- 0 ≤ m ≤ n(n-1)/2",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 06 讲 · 图",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nint g[105][105], deg[105];\nint main(void) {\n    int n, m;\n    scanf(\"%d %d\", &n, &m);\n    for (int k = 0; k < m; k++) {\n        int u, v;\n        scanf(\"%d %d\", &u, &v);\n        g[u][v] = g[v][u] = 1;\n    }\n    for (int i = 1; i <= n; i++) {\n        for (int j = 1; j <= n; j++) {\n            printf(j > 1 ? \" %d\" : \"%d\", g[i][j]);\n            deg[i] += g[i][j];\n        }\n        printf(\"\\n\");\n    }\n    for (int i = 1; i <= n; i++) printf(i > 1 ? \" %d\" : \"%d\", deg[i]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <numeric>\nusing namespace std;\nint main() {\n    int n, m; cin >> n >> m;\n    vector<vector<int>> g(n, vector<int>(n, 0));\n    while (m--) {\n        int u, v; cin >> u >> v;\n        --u; --v;\n        g[u][v] = g[v][u] = 1;\n    }\n    for (int i = 0; i < n; i++) {\n        for (int j = 0; j < n; j++) cout << (j ? \" \" : \"\") << g[i][j];\n        cout << \"\\n\";\n    }\n    for (int i = 0; i < n; i++)\n        cout << (i ? \" \" : \"\") << accumulate(g[i].begin(), g[i].end(), 0);\n    cout << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4 5\n1 2\n1 3\n1 4\n2 3\n3 4\n",
                "expected_stdout": "0 1 1 1\n1 0 1 0\n1 1 0 1\n1 0 1 0\n3 2 3 2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 1\n2 3\n",
                "expected_stdout": "0 0 0\n0 0 1\n0 1 0\n0 1 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 0\n",
                "expected_stdout": "0\n0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4 6\n1 2\n1 3\n1 4\n2 3\n2 4\n3 4\n",
                "expected_stdout": "0 1 1 1\n1 0 1 1\n1 1 0 1\n1 1 1 0\n3 3 3 3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "邻接表创建无向图",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "图",
            "邻接表",
            "尾插法"
        ],
        "statement_md": "读入一个无向图，用**尾插法（保持输入顺序）**建立邻接表，然后按顶点编号 `1` ~ `n` 依次输出每个顶点的邻接点链表。\n\n★ 与「无向图的邻接表（头插法）」对照：\n- **头插法**把新边插在链头，邻接点顺序与输入顺序**相反**；\n- **尾插法**（或 C++ `vector::push_back`）把新边挂在链尾，邻接点顺序与输入顺序**一致**。",
        "input_format": "第一行 `n m`（顶点数、边数）。\n\n接下来 `m` 行，每行 `u v` 表示一条无向边。",
        "output_format": "`n` 行，第 `i` 行为 `i: v1 v2 ...`（按输入先后顺序排列；孤立顶点输出 `i:`）。",
        "constraints_md": "- 1 ≤ n ≤ 100\n- 0 ≤ m ≤ n(n-1)/2",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 06 讲 · 图",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nint head[105], tail[105], nxt[4005], to[4005], ecnt = 0;\nvoid add_tail(int u, int v) {\n    ++ecnt; to[ecnt] = v; nxt[ecnt] = 0;\n    if (!head[u]) head[u] = tail[u] = ecnt;\n    else { nxt[tail[u]] = ecnt; tail[u] = ecnt; }\n}\nint main(void) {\n    int n, m;\n    scanf(\"%d %d\", &n, &m);\n    for (int k = 0; k < m; k++) {\n        int u, v; scanf(\"%d %d\", &u, &v);\n        add_tail(u, v); add_tail(v, u);\n    }\n    for (int i = 1; i <= n; i++) {\n        printf(\"%d:\", i);\n        for (int e = head[i]; e; e = nxt[e]) printf(\" %d\", to[e]);\n        printf(\"\\n\");\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\nusing namespace std;\nint main() {\n    int n, m; cin >> n >> m;\n    vector<vector<int>> adj(n + 1);\n    while (m--) {\n        int u, v; cin >> u >> v;\n        adj[u].push_back(v);\n        adj[v].push_back(u);\n    }\n    for (int i = 1; i <= n; i++) {\n        cout << i << \":\";\n        for (int v : adj[i]) cout << \" \" << v;\n        cout << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4 5\n1 2\n1 3\n1 4\n2 3\n3 4\n",
                "expected_stdout": "1: 2 3 4\n2: 1 3\n3: 1 2 4\n4: 1 3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 1\n2 3\n",
                "expected_stdout": "1:\n2: 3\n3: 2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 0\n",
                "expected_stdout": "1:\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5 4\n1 5\n1 3\n2 4\n3 5\n",
                "expected_stdout": "1: 5 3\n2: 4\n3: 1 5\n4: 2\n5: 1 3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "图深度优先遍历",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "图",
            "DFS",
            "深度优先遍历"
        ],
        "statement_md": "给定一个含 `n` 个顶点（编号 `1` ~ `n`）和 `m` 条边的无向图，输出它的**深度优先遍历（DFS）**序列。\n\n★ 为保证遍历序列唯一，约定：\n1. 外层按顶点编号 `1 → n` 依次检查，若未访问则从该顶点发起一次 DFS（处理非连通图）；\n2. 每个顶点扩展邻居时，一律按**邻接点编号从小到大**访问。",
        "input_format": "第一行 `n m`。\n\n随后 `m` 行，每行 `u v` 表示一条无向边。",
        "output_format": "一行 `n` 个整数（空格分隔），表示全图的 DFS 访问序列。",
        "constraints_md": "- 1 ≤ n ≤ 100\n- 0 ≤ m ≤ n(n-1)/2",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 06 讲 · 图",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nint g[105][105], vis[105], n, m, first = 1;\nvoid dfs(int u) {\n    vis[u] = 1;\n    printf(first ? \"%d\" : \" %d\", u);\n    first = 0;\n    for (int v = 1; v <= n; v++)\n        if (g[u][v] && !vis[v]) dfs(v);\n}\nint main(void) {\n    scanf(\"%d %d\", &n, &m);\n    for (int k = 0; k < m; k++) {\n        int u, v; scanf(\"%d %d\", &u, &v);\n        g[u][v] = g[v][u] = 1;\n    }\n    for (int i = 1; i <= n; i++)\n        if (!vis[i]) dfs(i);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <algorithm>\nusing namespace std;\n/* 另一套：邻接表排序 + 显式栈模拟非递归 DFS */\nint main() {\n    int n, m; cin >> n >> m;\n    vector<vector<int>> adj(n + 1);\n    while (m--) {\n        int u, v; cin >> u >> v;\n        adj[u].push_back(v); adj[v].push_back(u);\n    }\n    for (int i = 1; i <= n; i++)\n        sort(adj[i].rbegin(), adj[i].rend()); // 逆序压栈，栈顶就是最小编号\n    vector<char> vis(n + 1, 0);\n    vector<int> out;\n    for (int s = 1; s <= n; s++) {\n        if (vis[s]) continue;\n        vector<int> st{s};\n        while (!st.empty()) {\n            int u = st.back(); st.pop_back();\n            if (vis[u]) continue;\n            vis[u] = 1;\n            out.push_back(u);\n            for (int v : adj[u]) if (!vis[v]) st.push_back(v);\n        }\n    }\n    for (size_t i = 0; i < out.size(); i++) cout << (i ? \" \" : \"\") << out[i];\n    cout << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 5\n1 2\n1 4\n2 3\n2 5\n3 5\n",
                "expected_stdout": "1 2 3 5 4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4 2\n1 3\n2 4\n",
                "expected_stdout": "1 3 2 4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 0\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6 5\n1 6\n1 3\n3 2\n3 5\n2 4\n",
                "expected_stdout": "1 3 2 4 5 6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "列出连通集",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "图",
            "DFS",
            "BFS",
            "连通分量",
            "06-图1"
        ],
        "statement_md": "PTA 经典题 `06-图1 列出连通集`：给定一个有 `N` 个顶点（编号 `0` ~ `N-1`）和 `E` 条边的无向图，请分别用 **DFS** 和 **BFS** 找出图中的所有连通集。\n\n约定：遍历时总是从编号最小的未访问顶点出发，访问邻接点时也按编号**从小到大**的顺序访问。每个连通集输出一行，格式为 `{ v1 v2 ... vk }`。",
        "input_format": "第一行两个整数 `N E`（1 ≤ N ≤ 15）。\n\n随后 `E` 行，每行两个整数 `u v` 表示一条无向边。",
        "output_format": "先按 DFS 顺序输出所有连通集（每行一个 `{ ... }`），再按 BFS 顺序输出所有连通集。",
        "constraints_md": "- 1 ≤ N ≤ 15\n- 0 ≤ E ≤ N(N-1)/2",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 06 讲 · 图",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nint g[20][20], vis[20], q[20], n, e;\nvoid dfs(int u) {\n    vis[u] = 1;\n    printf(\" %d\", u);\n    for (int v = 0; v < n; v++)\n        if (g[u][v] && !vis[v]) dfs(v);\n}\nint main(void) {\n    scanf(\"%d %d\", &n, &e);\n    for (int k = 0; k < e; k++) {\n        int u, v; scanf(\"%d %d\", &u, &v);\n        g[u][v] = g[v][u] = 1;\n    }\n    for (int i = 0; i < n; i++) {\n        if (!vis[i]) {\n            printf(\"{\");\n            dfs(i);\n            printf(\" }\\n\");\n        }\n    }\n    for (int i = 0; i < n; i++) vis[i] = 0;\n    for (int i = 0; i < n; i++) {\n        if (!vis[i]) {\n            printf(\"{\");\n            int f = 0, r = 0;\n            q[r++] = i; vis[i] = 1;\n            while (f < r) {\n                int u = q[f++];\n                printf(\" %d\", u);\n                for (int v = 0; v < n; v++)\n                    if (g[u][v] && !vis[v]) { vis[v] = 1; q[r++] = v; }\n            }\n            printf(\" }\\n\");\n        }\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <queue>\n#include <algorithm>\n#include <functional>\nusing namespace std;\nint main() {\n    int n, e; cin >> n >> e;\n    vector<vector<int>> adj(n);\n    while (e--) {\n        int u, v; cin >> u >> v;\n        adj[u].push_back(v); adj[v].push_back(u);\n    }\n    for (int i = 0; i < n; i++) sort(adj[i].begin(), adj[i].end());\n    vector<char> vis(n, 0);\n    function<void(int)> dfs = [&](int u) {\n        vis[u] = 1;\n        cout << \" \" << u;\n        for (int v : adj[u]) if (!vis[v]) dfs(v);\n    };\n    for (int i = 0; i < n; i++)\n        if (!vis[i]) { cout << \"{\"; dfs(i); cout << \" }\\n\"; }\n    fill(vis.begin(), vis.end(), 0);\n    for (int i = 0; i < n; i++) {\n        if (vis[i]) continue;\n        cout << \"{\";\n        queue<int> q; q.push(i); vis[i] = 1;\n        while (!q.empty()) {\n            int u = q.front(); q.pop();\n            cout << \" \" << u;\n            for (int v : adj[u]) if (!vis[v]) { vis[v] = 1; q.push(v); }\n        }\n        cout << \" }\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "8 6\n0 7\n0 1\n2 0\n4 1\n2 4\n3 5\n",
                "expected_stdout": "{ 0 1 4 2 7 }\n{ 3 5 }\n{ 6 }\n{ 0 1 2 7 4 }\n{ 3 5 }\n{ 6 }\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4 0\n",
                "expected_stdout": "{ 0 }\n{ 1 }\n{ 2 }\n{ 3 }\n{ 0 }\n{ 1 }\n{ 2 }\n{ 3 }\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5 4\n0 1\n1 2\n2 3\n3 4\n",
                "expected_stdout": "{ 0 1 2 3 4 }\n{ 0 1 2 3 4 }\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6 5\n0 2\n0 4\n2 1\n1 4\n3 5\n",
                "expected_stdout": "{ 0 2 1 4 }\n{ 3 5 }\n{ 0 2 4 1 }\n{ 3 5 }\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "哥尼斯堡的“七桥问题”",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "图",
            "欧拉回路",
            "连通性",
            "顶点度"
        ],
        "statement_md": "PTA 经典题 `08-图9 哥尼斯堡的“七桥问题”`：给定一个含 `N` 个顶点（编号 `1` ~ `N`）和 `M` 条边的无向图，判断是否存在一条从某个顶点出发、**每条边恰好走一次**并回到起点的回路（即**欧拉回路**）。\n\n★ 最容易漏掉的坑：**只判「所有顶点度数为偶数」不够，必须同时检查图是否连通！**\n比如两个互不相连的三角形，每个顶点的度都是 2（全偶），但你不可能一笔画走完两个三角形！",
        "input_format": "第一行两个正整数 `N M`。\n\n随后 `M` 行，每行两个整数 `u v` 表示一条无向边。",
        "output_format": "一行，若存在欧拉回路输出 `1`，否则输出 `0`。",
        "constraints_md": "- 1 ≤ N ≤ 1000\n- 0 ≤ M ≤ 5000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 06 讲 · 图",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nint par[1005], deg[1005];\nint find(int x) {\n    while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }\n    return x;\n}\nint main(void) {\n    int n, m;\n    scanf(\"%d %d\", &n, &m);\n    for (int i = 1; i <= n; i++) par[i] = i;\n    for (int k = 0; k < m; k++) {\n        int u, v; scanf(\"%d %d\", &u, &v);\n        deg[u]++; deg[v]++;\n        int a = find(u), b = find(v);\n        if (a != b) par[b] = a;\n    }\n    int comps = 0, ok = 1;\n    for (int i = 1; i <= n; i++) {\n        if (find(i) == i) comps++;\n        if (deg[i] == 0 || deg[i] % 2 != 0) ok = 0;\n    }\n    if (comps != 1) ok = 0;\n    printf(\"%d\\n\", ok);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <queue>\nusing namespace std;\nint main() {\n    int n, m; cin >> n >> m;\n    vector<vector<int>> g(n + 1);\n    while (m--) {\n        int u, v; cin >> u >> v;\n        g[u].push_back(v); g[v].push_back(u);\n    }\n    vector<char> vis(n + 1, 0);\n    queue<int> q; q.push(1); vis[1] = 1;\n    int seen = 0;\n    while (!q.empty()) {\n        int u = q.front(); q.pop();\n        seen++;\n        for (int v : g[u]) if (!vis[v]) { vis[v] = 1; q.push(v); }\n    }\n    bool ok = (seen == n);\n    for (int i = 1; i <= n; i++)\n        if (g[i].empty() || g[i].size() % 2 != 0) ok = false;\n    cout << (ok ? 1 : 0) << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "6 10\n1 2\n2 3\n3 1\n4 5\n5 6\n6 4\n1 4\n1 6\n3 4\n3 6\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "7 12\n1 2\n1 3\n1 4\n2 3\n3 4\n4 7\n2 5\n2 6\n5 6\n5 7\n6 7\n3 6\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "6 6\n1 2\n2 3\n3 1\n4 5\n5 6\n6 4\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4 4\n1 2\n2 3\n3 4\n4 1\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "欧拉通路与欧拉回路判定",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "图",
            "欧拉通路",
            "欧拉回路",
            "奇度顶点"
        ],
        "statement_md": "由「哥尼斯堡七桥问题」举一反三：给定一个含 `N` 个顶点（编号 `1` ~ `N`）和 `M` 条边（`M ≥ 1`）的无向图，判断它的欧拉性质（要求全部 `N` 个顶点连通）：\n\n- 若连通且**奇度顶点个数为 0** → 存在欧拉回路，输出 `Eulerian Circuit`；\n- 若连通且**奇度顶点个数恰为 2** → 存在欧拉通路（半欧拉图，可一笔画但起终点不同），输出 `Eulerian Path`；\n- 若不连通或奇度顶点数为其它值 → 输出 `Non-Eulerian`。",
        "input_format": "第一行两个正整数 `N M`。\n\n随后 `M` 行，每行两个整数 `u v` 表示一条无向边。",
        "output_format": "一行，输出 `Eulerian Circuit`、`Eulerian Path` 或 `Non-Eulerian`。",
        "constraints_md": "- 2 ≤ N ≤ 1000\n- 1 ≤ M ≤ 5000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 06 讲 · 图",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nint par[1005], deg[1005];\nint find(int x) {\n    while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }\n    return x;\n}\nint main(void) {\n    int n, m;\n    scanf(\"%d %d\", &n, &m);\n    for (int i = 1; i <= n; i++) par[i] = i;\n    for (int k = 0; k < m; k++) {\n        int u, v; scanf(\"%d %d\", &u, &v);\n        deg[u]++; deg[v]++;\n        int a = find(u), b = find(v);\n        if (a != b) par[b] = a;\n    }\n    int comps = 0, odd = 0;\n    for (int i = 1; i <= n; i++) {\n        if (find(i) == i) comps++;\n        if (deg[i] % 2 == 1) odd++;\n    }\n    if (comps != 1) printf(\"Non-Eulerian\\n\");\n    else if (odd == 0) printf(\"Eulerian Circuit\\n\");\n    else if (odd == 2) printf(\"Eulerian Path\\n\");\n    else printf(\"Non-Eulerian\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <queue>\nusing namespace std;\nint main() {\n    int n, m; cin >> n >> m;\n    vector<vector<int>> g(n + 1);\n    while (m--) {\n        int u, v; cin >> u >> v;\n        g[u].push_back(v); g[v].push_back(u);\n    }\n    vector<char> vis(n + 1, 0);\n    queue<int> q; q.push(1); vis[1] = 1;\n    int seen = 0, odd = 0;\n    while (!q.empty()) {\n        int u = q.front(); q.pop();\n        seen++;\n        for (int v : g[u]) if (!vis[v]) { vis[v] = 1; q.push(v); }\n    }\n    for (int i = 1; i <= n; i++) if (g[i].size() % 2 == 1) odd++;\n    if (seen != n) cout << \"Non-Eulerian\\n\";\n    else if (odd == 0) cout << \"Eulerian Circuit\\n\";\n    else if (odd == 2) cout << \"Eulerian Path\\n\";\n    else cout << \"Non-Eulerian\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4 4\n1 2\n2 3\n3 4\n4 1\n",
                "expected_stdout": "Eulerian Circuit\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4 5\n1 2\n2 3\n3 4\n4 1\n1 3\n",
                "expected_stdout": "Eulerian Path\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4 6\n1 2\n1 3\n1 4\n2 3\n2 4\n3 4\n",
                "expected_stdout": "Non-Eulerian\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4 2\n1 2\n3 4\n",
                "expected_stdout": "Non-Eulerian\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "公路村村通",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "图",
            "最小生成树",
            "Kruskal",
            "Prim"
        ],
        "statement_md": "PTA 经典题 `08-图7 公路村村通`：现有 `N` 个村庄（编号 `1` ~ `N`）和 `M` 条候选公路及各自的造价，求让所有村庄都连通的**最低总造价**；若候选公路不足以连通所有村庄，输出 `-1`。\n\n★ 最小生成树（MST）的两套经典算法：\n- **Kruskal（加边法）**：边按权值升序排，用并查集判环，选够 `N-1` 条边即成；\n- **Prim（加点法）**：维护生成树到未选顶点的最短距离 `lowcost[]`，每轮拉进距离最小的顶点。",
        "input_format": "第一行两个整数 `N M`。\n\n随后 `M` 行，每行三个整数 `u v cost` 表示连接村庄 `u` 和 `v` 的公路造价。",
        "output_format": "一行一个整数：最小生成树的总造价；不连通输出 `-1`。",
        "constraints_md": "- 1 ≤ N ≤ 1000\n- 0 ≤ M ≤ 3000\n- 1 ≤ cost ≤ 10000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 06 讲 · 图",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <stdlib.h>\nstruct Edge { int u, v, w; } e[3005];\nint par[1005];\nint cmp(const void *a, const void *b) {\n    return ((struct Edge *)a)->w - ((struct Edge *)b)->w;\n}\nint find(int x) {\n    while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }\n    return x;\n}\nint main(void) {\n    int n, m;\n    scanf(\"%d %d\", &n, &m);\n    for (int i = 0; i < m; i++) scanf(\"%d %d %d\", &e[i].u, &e[i].v, &e[i].w);\n    qsort(e, m, sizeof(struct Edge), cmp);\n    for (int i = 1; i <= n; i++) par[i] = i;\n    long long cost = 0;\n    int cnt = 0;\n    for (int i = 0; i < m; i++) {\n        int a = find(e[i].u), b = find(e[i].v);\n        if (a != b) { par[b] = a; cost += e[i].w; cnt++; }\n    }\n    printf(\"%lld\\n\", cnt == n - 1 ? cost : -1LL);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\nusing namespace std;\n/* 另一套：Prim 算法 O(N^2) */\nint main() {\n    int n, m; cin >> n >> m;\n    const long long INF = (long long)1e15;\n    vector<vector<long long>> g(n + 1, vector<long long>(n + 1, INF));\n    while (m--) {\n        int u, v; long long w; cin >> u >> v >> w;\n        if (w < g[u][v]) g[u][v] = g[v][u] = w;\n    }\n    vector<long long> low(n + 1, INF);\n    vector<char> in(n + 1, 0);\n    low[1] = 0;\n    long long cost = 0;\n    for (int r = 0; r < n; r++) {\n        int u = -1;\n        for (int i = 1; i <= n; i++)\n            if (!in[i] && low[i] < INF && (u < 0 || low[i] < low[u])) u = i;\n        if (u < 0) { cout << -1 << \"\\n\"; return 0; }\n        in[u] = 1; cost += low[u];\n        for (int v = 1; v <= n; v++)\n            if (!in[v] && g[u][v] < low[v]) low[v] = g[u][v];\n    }\n    cout << cost << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "6 15\n1 2 5\n1 3 3\n1 4 7\n1 5 4\n1 6 2\n2 3 4\n2 4 6\n2 5 2\n2 6 6\n3 4 6\n3 5 1\n3 6 1\n4 5 10\n4 6 8\n5 6 3\n",
                "expected_stdout": "12\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4 2\n1 2 3\n3 4 5\n",
                "expected_stdout": "-1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 0\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4 5\n1 2 1\n2 3 2\n3 4 3\n4 1 4\n1 3 5\n",
                "expected_stdout": "6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "森森美图",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 25,
        "tags": [
            "图",
            "双权最小生成树",
            "Kruskal",
            "贪心"
        ],
        "statement_md": "在风景区规划 `N` 个景点（编号 `1` ~ `N`）的步道网络，共有 `M` 条候选路线。\n每条路线 `(u, v)` 有两个指标：**破坏度 `bad`**（越小越美观）和**施工造价 `cost`**。\n\n请你选出 `N-1` 条路线使所有景点连通，要求：\n1. 首先让选出路线的**总破坏度最小**；\n2. 在破坏度相同的情况下，优先选择**造价更低**的边，使**总造价最小**。\n\n输出最优方案的 `总破坏度 总造价`；若无法连通全部景点，输出 `-1`。",
        "input_format": "第一行两个正整数 `N M`。\n\n随后 `M` 行，每行四个整数 `u v bad cost`。",
        "output_format": "一行两个整数：`总破坏度 总造价`；不连通输出 `-1`。",
        "constraints_md": "- 1 ≤ N ≤ 1000\n- 0 ≤ M ≤ 5000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 06 讲 · 图",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <stdlib.h>\nstruct E { int u, v, bad, cost; } e[5005];\nint par[1005];\nint cmp(const void *a, const void *b) {\n    const struct E *x = (const struct E *)a, *y = (const struct E *)b;\n    if (x->bad != y->bad) return x->bad - y->bad;\n    return x->cost - y->cost;\n}\nint find(int x) {\n    while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }\n    return x;\n}\nint main(void) {\n    int n, m;\n    scanf(\"%d %d\", &n, &m);\n    for (int i = 0; i < m; i++) scanf(\"%d %d %d %d\", &e[i].u, &e[i].v, &e[i].bad, &e[i].cost);\n    qsort(e, m, sizeof(struct E), cmp);\n    for (int i = 1; i <= n; i++) par[i] = i;\n    long long tb = 0, tc = 0;\n    int cnt = 0;\n    for (int i = 0; i < m; i++) {\n        int a = find(e[i].u), b = find(e[i].v);\n        if (a != b) { par[b] = a; tb += e[i].bad; tc += e[i].cost; cnt++; }\n    }\n    if (cnt < n - 1) printf(\"-1\\n\");\n    else printf(\"%lld %lld\\n\", tb, tc);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <utility>\nusing namespace std;\n/* 另一套：用二元组权值 (bad, cost) 跑 Prim 算法 */\nint main() {\n    int n, m; cin >> n >> m;\n    const long long INF = (long long)1e15;\n    pair<long long, long long> BIG = {INF, INF};\n    vector<vector<pair<long long, long long>>> g(n + 1, vector<pair<long long, long long>>(n + 1, BIG));\n    while (m--) {\n        int u, v; long long b, c; cin >> u >> v >> b >> c;\n        pair<long long, long long> w = {b, c};\n        if (w < g[u][v]) g[u][v] = g[v][u] = w;\n    }\n    vector<pair<long long, long long>> low(n + 1, BIG);\n    vector<char> in(n + 1, 0);\n    low[1] = {0, 0};\n    long long tb = 0, tc = 0;\n    for (int r = 0; r < n; r++) {\n        int u = -1;\n        for (int i = 1; i <= n; i++)\n            if (!in[i] && low[i] < BIG && (u < 0 || low[i] < low[u])) u = i;\n        if (u < 0) { cout << -1 << \"\\n\"; return 0; }\n        in[u] = 1;\n        tb += low[u].first; tc += low[u].second;\n        for (int v = 1; v <= n; v++)\n            if (!in[v] && g[u][v] < low[v]) low[v] = g[u][v];\n    }\n    cout << tb << \" \" << tc << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4 5\n1 2 1 10\n1 2 1 6\n2 3 2 5\n2 3 1 8\n3 4 2 4\n",
                "expected_stdout": "4 18\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5 6\n1 2 2 5\n2 3 2 3\n1 3 2 4\n3 4 1 10\n4 5 3 8\n3 5 3 2\n",
                "expected_stdout": "8 19\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 1\n1 2 1 5\n",
                "expected_stdout": "-1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "单源最短路径",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "图",
            "Dijkstra",
            "最短路径还原",
            "pre数组"
        ],
        "statement_md": "在「单源最短路径（Dijkstra）」的基础上更进一步：给定边权非负的有向图、起点 `s` 和终点 `t`，不仅要求出 `s` 到 `t` 的最短距离，还要**完整还原并打印最短路径经过的顶点序列** `s -> ... -> t`。\n\n★ 路径还原靠的是前驱数组 `pre[]`：每当边 `x → y` 松弛成功（`dist[x] + w < dist[y]`）时，顺手记下 `pre[y] = x`；最后从终点 `t` 顺着 `pre` 一路倒推回 `s`，逆序输出即是完整路径！",
        "input_format": "第一行四个整数 `n m s t`。\n\n随后 `m` 行，每行三个整数 `u v w` 表示有向边 `u → v`（权值 `w > 0`）。",
        "output_format": "若不可达只输出一行 `-1`；若可达，第一行输出最短距离，第二行输出 `v1 -> v2 -> ... -> vk`。",
        "constraints_md": "- 1 ≤ n ≤ 100\n- 0 ≤ m ≤ 2000\n- 测试数据保证最短路径唯一",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 06 讲 · 图",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#define INF 1000000000LL\nlong long w[105][105], dist[105];\nint pre[105], done[105], stk[105];\nint main(void) {\n    int n, m, s, t;\n    scanf(\"%d %d %d %d\", &n, &m, &s, &t);\n    for (int i = 1; i <= n; i++) {\n        dist[i] = INF;\n        for (int j = 1; j <= n; j++) w[i][j] = INF;\n    }\n    for (int k = 0; k < m; k++) {\n        int u, v; long long c;\n        scanf(\"%d %d %lld\", &u, &v, &c);\n        if (c < w[u][v]) w[u][v] = c;\n    }\n    dist[s] = 0;\n    for (int r = 0; r < n; r++) {\n        int x = -1;\n        for (int i = 1; i <= n; i++)\n            if (!done[i] && dist[i] < INF && (x < 0 || dist[i] < dist[x])) x = i;\n        if (x < 0) break;\n        done[x] = 1;\n        for (int y = 1; y <= n; y++)\n            if (w[x][y] < INF && dist[x] + w[x][y] < dist[y]) {\n                dist[y] = dist[x] + w[x][y];\n                pre[y] = x;\n            }\n    }\n    if (dist[t] >= INF) { printf(\"-1\\n\"); return 0; }\n    printf(\"%lld\\n\", dist[t]);\n    int top = 0;\n    for (int cur = t; cur != 0; cur = pre[cur]) stk[top++] = cur;\n    for (int i = top - 1; i >= 0; i--)\n        printf(i == top - 1 ? \"%d\" : \" -> %d\", stk[i]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <queue>\n#include <algorithm>\nusing namespace std;\nint main() {\n    int n, m, s, t; cin >> n >> m >> s >> t;\n    const long long INF = (long long)1e15;\n    vector<vector<pair<int, long long>>> adj(n + 1);\n    while (m--) {\n        int u, v; long long c; cin >> u >> v >> c;\n        adj[u].push_back({v, c});\n    }\n    vector<long long> dist(n + 1, INF);\n    vector<int> pre(n + 1, 0);\n    priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<pair<long long, int>>> pq;\n    dist[s] = 0; pq.push({0, s});\n    while (!pq.empty()) {\n        auto [d, u] = pq.top(); pq.pop();\n        if (d > dist[u]) continue;\n        for (auto [v, c] : adj[u]) {\n            if (dist[u] + c < dist[v]) {\n                dist[v] = dist[u] + c;\n                pre[v] = u;\n                pq.push({dist[v], v});\n            }\n        }\n    }\n    if (dist[t] >= INF) { cout << -1 << \"\\n\"; return 0; }\n    cout << dist[t] << \"\\n\";\n    vector<int> path;\n    for (int cur = t; cur != 0; cur = pre[cur]) path.push_back(cur);\n    reverse(path.begin(), path.end());\n    for (size_t i = 0; i < path.size(); i++)\n        cout << (i ? \" -> \" : \"\") << path[i];\n    cout << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 7 1 5\n1 2 10\n1 4 30\n1 5 100\n2 3 50\n3 5 10\n4 3 20\n4 5 60\n",
                "expected_stdout": "60\n1 -> 4 -> 3 -> 5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4 4 1 4\n1 2 1\n2 3 2\n3 4 3\n1 4 10\n",
                "expected_stdout": "6\n1 -> 2 -> 3 -> 4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 1 1 3\n1 2 5\n",
                "expected_stdout": "-1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3 2 2 2\n1 2 3\n2 3 4\n",
                "expected_stdout": "0\n2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "最短路径",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "图",
            "无向有权图",
            "两点最短路"
        ],
        "statement_md": "给定一个含 `N` 个顶点（编号 `1` ~ `N`）和 `M` 条无向带权边的无向图，回答 `Q` 次两点间的最短路径距离询问 `(s, t)`；若两点不连通，输出 `-1`。",
        "input_format": "第一行三个整数 `N M Q`。\n\n随后 `M` 行，每行三个整数 `u v w`（无向边，1 ≤ w ≤ 10000）。\n\n随后 `Q` 行，每行两个整数 `s t`。",
        "output_format": "`Q` 行，每行输出 `s` 到 `t` 的最短距离（不可达输出 `-1`）。",
        "constraints_md": "- 1 ≤ N ≤ 80\n- 0 ≤ M ≤ 2000\n- 1 ≤ Q ≤ 200",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 06 讲 · 图",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#define INF 1000000000000000LL\nlong long d[85][85];\nint main(void) {\n    int n, m, q;\n    scanf(\"%d %d %d\", &n, &m, &q);\n    for (int i = 1; i <= n; i++)\n        for (int j = 1; j <= n; j++)\n            d[i][j] = (i == j) ? 0 : INF;\n    for (int k = 0; k < m; k++) {\n        int u, v; long long w;\n        scanf(\"%d %d %lld\", &u, &v, &w);\n        if (w < d[u][v]) d[u][v] = d[v][u] = w;\n    }\n    for (int k = 1; k <= n; k++)\n        for (int i = 1; i <= n; i++)\n            for (int j = 1; j <= n; j++)\n                if (d[i][k] + d[k][j] < d[i][j]) d[i][j] = d[i][k] + d[k][j];\n    while (q--) {\n        int s, t; scanf(\"%d %d\", &s, &t);\n        printf(\"%lld\\n\", d[s][t] >= INF ? -1LL : d[s][t]);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <queue>\nusing namespace std;\n/* 另一套：每次询问独立跑一遍堆优化 Dijkstra */\nint main() {\n    int n, m, q; cin >> n >> m >> q;\n    const long long INF = (long long)1e15;\n    vector<vector<pair<int, long long>>> adj(n + 1);\n    while (m--) {\n        int u, v; long long w; cin >> u >> v >> w;\n        adj[u].push_back({v, w});\n        adj[v].push_back({u, w});\n    }\n    while (q--) {\n        int s, t; cin >> s >> t;\n        vector<long long> dist(n + 1, INF);\n        priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<pair<long long, int>>> pq;\n        dist[s] = 0; pq.push({0, s});\n        while (!pq.empty()) {\n            auto [d, u] = pq.top(); pq.pop();\n            if (d > dist[u]) continue;\n            for (auto [v, w] : adj[u])\n                if (dist[u] + w < dist[v]) { dist[v] = dist[u] + w; pq.push({dist[v], v}); }\n        }\n        cout << (dist[t] >= INF ? -1LL : dist[t]) << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 6 3\n1 2 2\n2 3 3\n1 3 10\n3 4 1\n1 4 8\n4 5 4\n1 3\n1 5\n2 4\n",
                "expected_stdout": "5\n10\n4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4 2 2\n1 2 5\n3 4 7\n1 2\n1 4\n",
                "expected_stdout": "5\n-1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 3 2\n1 2 4\n1 2 2\n2 3 3\n1 3\n2 2\n",
                "expected_stdout": "5\n0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "最短路径算法(Floyd-Warshall)",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "图",
            "Floyd-Warshall",
            "多源最短路",
            "动态规划"
        ],
        "statement_md": "给定一个含 `n` 个顶点（编号 `1` ~ `n`）和 `m` 条有向边的有向带权图（允许含负权边，保证无负权回路），使用 **Floyd-Warshall 算法**求出所有顶点对 `(i, j)` 之间的最短路径长度，输出完整的 `n × n` 最短路矩阵。\n\n★ Floyd 三重循环里最致命的错误是**把 `k` 写在内层**：\n状态转移是「允许经过前 `k` 个顶点作为中间跳板」，所以**中转点 `k` 必须在最外层**（`k → i → j`）！",
        "input_format": "第一行两个整数 `n m`。\n\n随后 `m` 行，每行三个整数 `u v w` 表示有向边 `u → v` 的权值。",
        "output_format": "`n` 行，每行 `n` 个项（空格分隔）：若 `i` 可达 `j` 输出最短距离，否则输出 `INF`（对角线 `d[i][i] = 0`）。",
        "constraints_md": "- 1 ≤ n ≤ 60\n- 0 ≤ m ≤ 2000\n- -1000 ≤ w ≤ 1000（无负环）",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 06 讲 · 图",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#define INF 1000000000000000LL\nlong long d[65][65];\nint main(void) {\n    int n, m;\n    scanf(\"%d %d\", &n, &m);\n    for (int i = 1; i <= n; i++)\n        for (int j = 1; j <= n; j++)\n            d[i][j] = (i == j) ? 0 : INF;\n    for (int k = 0; k < m; k++) {\n        int u, v; long long w;\n        scanf(\"%d %d %lld\", &u, &v, &w);\n        if (w < d[u][v]) d[u][v] = w;\n    }\n    for (int k = 1; k <= n; k++)\n        for (int i = 1; i <= n; i++)\n            for (int j = 1; j <= n; j++)\n                if (d[i][k] < INF && d[k][j] < INF && d[i][k] + d[k][j] < d[i][j])\n                    d[i][j] = d[i][k] + d[k][j];\n    for (int i = 1; i <= n; i++) {\n        for (int j = 1; j <= n; j++) {\n            if (j > 1) printf(\" \");\n            if (d[i][j] >= INF) printf(\"INF\");\n            else printf(\"%lld\", d[i][j]);\n        }\n        printf(\"\\n\");\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\nusing namespace std;\n/* 另一套：从每个源点 i 分别跑一次 Bellman-Ford（支持负权边） */\nstruct E { int u, v; long long w; };\nint main() {\n    int n, m; cin >> n >> m;\n    const long long INF = (long long)1e15;\n    vector<E> edges(m);\n    for (auto &e : edges) cin >> e.u >> e.v >> e.w;\n    for (int s = 1; s <= n; s++) {\n        vector<long long> dist(n + 1, INF);\n        dist[s] = 0;\n        for (int r = 1; r < n; r++)\n            for (auto &e : edges)\n                if (dist[e.u] < INF && dist[e.u] + e.w < dist[e.v])\n                    dist[e.v] = dist[e.u] + e.w;\n        for (int j = 1; j <= n; j++) {\n            if (j > 1) cout << \" \";\n            if (dist[j] >= INF) cout << \"INF\";\n            else cout << dist[j];\n        }\n        cout << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4 8\n1 2 2\n1 3 6\n1 4 4\n2 3 3\n3 1 7\n3 4 1\n4 1 5\n4 3 12\n",
                "expected_stdout": "0 2 5 4\n9 0 3 4\n6 8 0 1\n5 7 10 0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 3\n1 2 4\n2 3 -2\n1 3 5\n",
                "expected_stdout": "0 4 2\nINF 0 -2\nINF INF 0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 1\n1 2 10\n",
                "expected_stdout": "0 10 INF\nINF 0 INF\nINF INF 0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "哈利·波特的考试",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "图",
            "Floyd",
            "图的中心点",
            "07-图4"
        ],
        "statement_md": "PTA 经典题 `07-图4 哈利·波特的考试`：有 `N` 种动物（编号 `1` ~ `N`）和 `M` 条双向变形魔咒及各自的咒语长度。\n哈利想带**一只动物**去考场，使得把它变成**最难变的另一种动物**所需的总魔咒长度**最小**（即求图的中心点：`min_i max_j dist(i, j)`）。\n\n- 若有多只动物并列最优，输出**编号最小**的那只动物编号及其最大最短距离；\n- 若带哪只动物都无法变成所有其它动物（图不连通），输出 `0`。",
        "input_format": "第一行两个正整数 `N M`。\n\n随后 `M` 行，每行三个整数 `u v w` 表示动物 `u` 与 `v` 之间魔咒长度为 `w`。",
        "output_format": "一行，输出最优动物编号与对应的最大魔咒长度（空格分隔）；若图不连通输出 `0`。",
        "constraints_md": "- 1 ≤ N ≤ 100\n- 0 ≤ M ≤ 2000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 06 讲 · 图",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#define INF 1000000000LL\nlong long d[105][105];\nint main(void) {\n    int n, m;\n    scanf(\"%d %d\", &n, &m);\n    for (int i = 1; i <= n; i++)\n        for (int j = 1; j <= n; j++)\n            d[i][j] = (i == j) ? 0 : INF;\n    for (int k = 0; k < m; k++) {\n        int u, v; long long w;\n        scanf(\"%d %d %lld\", &u, &v, &w);\n        if (w < d[u][v]) d[u][v] = d[v][u] = w;\n    }\n    for (int k = 1; k <= n; k++)\n        for (int i = 1; i <= n; i++)\n            for (int j = 1; j <= n; j++)\n                if (d[i][k] + d[k][j] < d[i][j]) d[i][j] = d[i][k] + d[k][j];\n    int best_i = 0;\n    long long best_mx = INF;\n    for (int i = 1; i <= n; i++) {\n        long long mx = 0;\n        for (int j = 1; j <= n; j++) if (d[i][j] > mx) mx = d[i][j];\n        if (mx < best_mx) { best_mx = mx; best_i = i; }\n    }\n    if (best_i == 0) printf(\"0\\n\");\n    else printf(\"%d %lld\\n\", best_i, best_mx);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <queue>\n#include <algorithm>\nusing namespace std;\n/* 另一套：对每个动物 i 跑一次 Dijkstra 求它的偏心率 */\nint main() {\n    int n, m; cin >> n >> m;\n    const long long INF = (long long)1e15;\n    vector<vector<pair<int, long long>>> adj(n + 1);\n    while (m--) {\n        int u, v; long long w; cin >> u >> v >> w;\n        adj[u].push_back({v, w}); adj[v].push_back({u, w});\n    }\n    int best_i = 0;\n    long long best_mx = INF;\n    for (int s = 1; s <= n; s++) {\n        vector<long long> dist(n + 1, INF);\n        priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<pair<long long, int>>> pq;\n        dist[s] = 0; pq.push({0, s});\n        while (!pq.empty()) {\n            auto [d, u] = pq.top(); pq.pop();\n            if (d > dist[u]) continue;\n            for (auto [v, w] : adj[u])\n                if (dist[u] + w < dist[v]) { dist[v] = dist[u] + w; pq.push({dist[v], v}); }\n        }\n        long long mx = *max_element(dist.begin() + 1, dist.end());\n        if (mx < best_mx) { best_mx = mx; best_i = s; }\n    }\n    if (best_i == 0) cout << 0 << \"\\n\";\n    else cout << best_i << \" \" << best_mx << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "6 11\n3 4 70\n1 2 1\n5 4 50\n2 6 50\n5 6 60\n1 3 70\n4 6 60\n3 6 80\n5 1 100\n2 4 60\n5 2 80\n",
                "expected_stdout": "4 70\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4 2\n1 2 10\n3 4 20\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 3\n1 2 5\n2 3 5\n1 3 5\n",
                "expected_stdout": "1 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "旅游规划",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "图",
            "Dijkstra",
            "双权最短路",
            "07-图6"
        ],
        "statement_md": "PTA 经典题 `07-图6 旅游规划`：城市编号 `0` ~ `N-1`，有 `M` 条双向高速公路，每条公路既给出了**长度 `len`**，又给出了**过路费 `cost`**。\n\n请找出从出发地 `S` 到目的地 `D` 的**最短路径**；若最短路径不唯一，则选择其中**过路费总和最便宜**的一条，输出 `最短距离 最少过路费`。\n\n★ 双权 Dijkstra 的松弛模板：\n- 当 `dist[u] + len < dist[v]` 时：距离和费用一起更新；\n- 当 `dist[u] + len == dist[v]` 且 `cost[u] + c < cost[v]` 时：只把费用更新得更便宜！",
        "input_format": "第一行四个整数 `N M S D`（城市数、公路数、起点、终点，城市编号 0 ~ N-1）。\n\n随后 `M` 行，每行四个整数 `u v len cost`。",
        "output_format": "一行两个整数，空格分隔：`最短距离 最少过路费`。",
        "constraints_md": "- 2 ≤ N ≤ 500\n- 1 ≤ M ≤ 5000\n- 保证 S 可达 D",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 06 讲 · 图",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#define INF 1000000000LL\nlong long g_len[505][505], g_cost[505][505], d_len[505], d_cost[505];\nint done[505];\nint main(void) {\n    int n, m, s, dst;\n    scanf(\"%d %d %d %d\", &n, &m, &s, &dst);\n    for (int i = 0; i < n; i++) {\n        d_len[i] = d_cost[i] = INF;\n        for (int j = 0; j < n; j++) g_len[i][j] = g_cost[i][j] = INF;\n    }\n    for (int k = 0; k < m; k++) {\n        int u, v; long long L, C;\n        scanf(\"%d %d %lld %lld\", &u, &v, &L, &C);\n        if (L < g_len[u][v] || (L == g_len[u][v] && C < g_cost[u][v])) {\n            g_len[u][v] = g_len[v][u] = L;\n            g_cost[u][v] = g_cost[v][u] = C;\n        }\n    }\n    d_len[s] = 0; d_cost[s] = 0;\n    for (int r = 0; r < n; r++) {\n        int u = -1;\n        for (int i = 0; i < n; i++)\n            if (!done[i] && d_len[i] < INF && (u < 0 || d_len[i] < d_len[u])) u = i;\n        if (u < 0) break;\n        done[u] = 1;\n        for (int v = 0; v < n; v++) {\n            if (g_len[u][v] >= INF) continue;\n            if (d_len[u] + g_len[u][v] < d_len[v]) {\n                d_len[v] = d_len[u] + g_len[u][v];\n                d_cost[v] = d_cost[u] + g_cost[u][v];\n            } else if (d_len[u] + g_len[u][v] == d_len[v] && d_cost[u] + g_cost[u][v] < d_cost[v]) {\n                d_cost[v] = d_cost[u] + g_cost[u][v];\n            }\n        }\n    }\n    printf(\"%lld %lld\\n\", d_len[dst], d_cost[dst]);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <queue>\n#include <tuple>\nusing namespace std;\nint main() {\n    int n, m, s, dst; cin >> n >> m >> s >> dst;\n    const long long INF = (long long)1e15;\n    vector<vector<tuple<int, long long, long long>>> adj(n);\n    while (m--) {\n        int u, v; long long L, C; cin >> u >> v >> L >> C;\n        adj[u].emplace_back(v, L, C);\n        adj[v].emplace_back(u, L, C);\n    }\n    vector<pair<long long, long long>> dist(n, {INF, INF});\n    using T = tuple<long long, long long, int>;\n    priority_queue<T, vector<T>, greater<T>> pq;\n    dist[s] = {0, 0}; pq.push({0, 0, s});\n    while (!pq.empty()) {\n        auto [L, C, u] = pq.top(); pq.pop();\n        if (make_pair(L, C) > dist[u]) continue;\n        for (auto [v, wL, wC] : adj[u]) {\n            pair<long long, long long> cand = {L + wL, C + wC};\n            if (cand < dist[v]) {\n                dist[v] = cand;\n                pq.push({cand.first, cand.second, v});\n            }\n        }\n    }\n    cout << dist[dst].first << \" \" << dist[dst].second << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4 5 0 3\n0 1 1 20\n1 3 2 30\n0 3 4 10\n0 2 2 20\n2 3 1 20\n",
                "expected_stdout": "3 40\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 3 0 2\n0 1 2 10\n1 2 2 10\n0 2 4 25\n",
                "expected_stdout": "4 20\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4 4 0 3\n0 1 5 5\n1 3 5 10\n0 2 3 8\n2 3 7 4\n",
                "expected_stdout": "10 12\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "任务调度的合理性",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "图",
            "拓扑排序",
            "AOV网",
            "判环"
        ],
        "statement_md": "PTA 经典题 `08-图8 任务调度的合理性`：假定一个工程项目由一组子任务构成（编号 `1` ~ `N`），给出每个子任务必须先完成的直接前置子任务列表，判断整个任务调度方案是否合理（即**AOV 网中是否不存在有向环**）。\n\n★ 判环既可以用 **Kahn 入度拓扑排序**（看最终出队的顶点数是否等于 `N`），也可以用 **三色 DFS**（`0=未访问`、`1=当前递归栈中`、`2=已完成`，一旦摸到状态 `1` 的点即是有向环）！",
        "input_format": "第一行正整数 `N`（子任务数）。\n\n随后 `N` 行，第 `i` 行先给一个整数 `K`（前置任务数），随后跟 `K` 个前置任务编号。",
        "output_format": "一行，若调度方案合理（无环）输出 `1`，否则输出 `0`。",
        "constraints_md": "- 1 ≤ N ≤ 100",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 06 讲 · 图",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nint g[105][105], indeg[105], q[105];\nint main(void) {\n    int n;\n    scanf(\"%d\", &n);\n    for (int i = 1; i <= n; i++) {\n        int k; scanf(\"%d\", &k);\n        while (k--) {\n            int pre; scanf(\"%d\", &pre);\n            if (!g[pre][i]) { g[pre][i] = 1; indeg[i]++; }\n        }\n    }\n    int f = 0, r = 0;\n    for (int i = 1; i <= n; i++) if (indeg[i] == 0) q[r++] = i;\n    while (f < r) {\n        int u = q[f++];\n        for (int v = 1; v <= n; v++)\n            if (g[u][v] && --indeg[v] == 0) q[r++] = v;\n    }\n    printf(\"%d\\n\", r == n ? 1 : 0);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <functional>\nusing namespace std;\n/* 另一套：三色 DFS 判有向环 */\nint main() {\n    int n; cin >> n;\n    vector<vector<int>> adj(n + 1);\n    for (int i = 1; i <= n; i++) {\n        int k; cin >> k;\n        while (k--) { int p; cin >> p; adj[p].push_back(i); }\n    }\n    vector<int> col(n + 1, 0);\n    bool cyc = false;\n    function<void(int)> dfs = [&](int u) {\n        col[u] = 1;\n        for (int v : adj[u]) {\n            if (col[v] == 1) cyc = true;\n            else if (col[v] == 0) dfs(v);\n        }\n        col[u] = 2;\n    };\n    for (int i = 1; i <= n; i++) if (!col[i]) dfs(i);\n    cout << (cyc ? 0 : 1) << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "9\n0\n2 1 5\n1 1\n1 1\n2 3 4\n1 4\n2 2 5\n2 5 6\n2 7 8\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n1 2\n1 3\n1 1\n0\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n0\n1 1\n2 1 2\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n1 2\n1 1\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "最短工期",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "图",
            "AOE网",
            "拓扑排序",
            "最早发生时间"
        ],
        "statement_md": "PTA 经典题 `08-图8 最短工期（How Long Does It Take）`：一个项目有 `N` 个里程碑事件（编号 `0` ~ `N-1`）和 `M` 项有向活动 `(u, v, w)`，表示事件 `u` 达成后还需耗时 `w` 才能完成指向事件 `v` 的这项活动。\n\n请计算完成全部里程碑所需的**最短总工期**（即 `max(ve[0..N-1])`）；若计划中存在循环依赖（有向环），输出 `Impossible`。",
        "input_format": "第一行两个整数 `N M`。\n\n随后 `M` 行，每行三个非负整数 `u v w`。",
        "output_format": "一行，输出最短总工期；若有环则输出 `Impossible`。",
        "constraints_md": "- 1 ≤ N ≤ 100\n- 0 ≤ M ≤ 2000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 06 讲 · 图",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nint head[105], nxt[2005], to[2005], wt[2005], ecnt = 0;\nint indeg[105], q[105], ve[105];\nint main(void) {\n    int n, m;\n    scanf(\"%d %d\", &n, &m);\n    for (int k = 0; k < m; k++) {\n        int u, v, w; scanf(\"%d %d %d\", &u, &v, &w);\n        ++ecnt; to[ecnt] = v; wt[ecnt] = w; nxt[ecnt] = head[u]; head[u] = ecnt;\n        indeg[v]++;\n    }\n    int f = 0, r = 0;\n    for (int i = 0; i < n; i++) if (indeg[i] == 0) q[r++] = i;\n    while (f < r) {\n        int u = q[f++];\n        for (int e = head[u]; e; e = nxt[e]) {\n            int v = to[e], w = wt[e];\n            if (ve[u] + w > ve[v]) ve[v] = ve[u] + w;\n            if (--indeg[v] == 0) q[r++] = v;\n        }\n    }\n    if (r < n) { printf(\"Impossible\\n\"); return 0; }\n    int ans = 0;\n    for (int i = 0; i < n; i++) if (ve[i] > ans) ans = ve[i];\n    printf(\"%d\\n\", ans);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <algorithm>\n#include <functional>\nusing namespace std;\nint main() {\n    int n, m; cin >> n >> m;\n    vector<vector<pair<int, int>>> rev(n);\n    while (m--) {\n        int u, v, w; cin >> u >> v >> w;\n        rev[v].push_back({u, w});\n    }\n    vector<int> state(n, 0), dp(n, 0);\n    bool cyc = false;\n    function<int(int)> solve = [&](int v) -> int {\n        if (state[v] == 1) { cyc = true; return 0; }\n        if (state[v] == 2) return dp[v];\n        state[v] = 1;\n        int best = 0;\n        for (auto [u, w] : rev[v]) best = max(best, solve(u) + w);\n        state[v] = 2;\n        return dp[v] = best;\n    };\n    int ans = 0;\n    for (int i = 0; i < n; i++) ans = max(ans, solve(i));\n    if (cyc) cout << \"Impossible\\n\";\n    else cout << ans << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "9 12\n0 1 6\n0 2 4\n0 3 5\n1 4 1\n2 4 1\n3 5 2\n5 4 0\n4 6 9\n4 7 7\n5 7 4\n6 8 2\n7 8 4\n",
                "expected_stdout": "18\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4 4\n0 1 1\n0 2 2\n2 1 3\n1 3 4\n",
                "expected_stdout": "9\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 3\n0 1 5\n1 2 5\n2 0 5\n",
                "expected_stdout": "Impossible\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "关键活动",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 25,
        "tags": [
            "图",
            "AOE网",
            "关键路径",
            "ve与vl",
            "08-图9"
        ],
        "statement_md": "PTA 经典压轴题 `08-图9 关键活动`：给定 AOE 网的 `N` 个事件（编号 `1` ~ `N`）和 `M` 项有向活动 `(u, v, w)`：\n\n1. 若网络中有环（调度不可行），只输出一行 `0`；\n2. 若可行，第一行输出整个工程的**最短完成时间 `T = max(ve)`**，随后输出所有**关键活动**（满足 `ve[u] + w == vl[v]` 的活动 `u->v`）。\n\n★ 两个经典的 PTA 判分细节（踩过的人无数）：\n- 汇点可能不止一个，所以逆拓扑求最迟发生时间时，**全体 `vl[1..N]` 统一初始化为总工期 `T`**；\n- 输出顺序规定：按起点 `u` **从小到大**；起点相同时，按**输入时出现的先后顺序相反**（即邻接表**头插法**的自然遍历顺序）！",
        "input_format": "第一行两个正整数 `N M`。\n\n随后 `M` 行，每行三个正整数 `u v w`。",
        "output_format": "若不可行输出 `0`；否则第一行输出总工期，随后每行输出一条关键活动 `u->v`。",
        "constraints_md": "- 1 ≤ N ≤ 100\n- 1 ≤ M ≤ 1000",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 06 讲 · 图",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\nint head[105], nxt[1005], to[1005], wt[1005], ecnt = 0;\nint indeg[105], q[105], ve[105], vl[105];\n/* 头插法建邻接表：同一个 u 的出边天然按输入逆序排列！ */\nint main(void) {\n    int n, m;\n    scanf(\"%d %d\", &n, &m);\n    for (int k = 0; k < m; k++) {\n        int u, v, w; scanf(\"%d %d %d\", &u, &v, &w);\n        ++ecnt; to[ecnt] = v; wt[ecnt] = w; nxt[ecnt] = head[u]; head[u] = ecnt;\n        indeg[v]++;\n    }\n    int f = 0, r = 0;\n    for (int i = 1; i <= n; i++) if (indeg[i] == 0) q[r++] = i;\n    while (f < r) {\n        int u = q[f++];\n        for (int e = head[u]; e; e = nxt[e]) {\n            int v = to[e], w = wt[e];\n            if (ve[u] + w > ve[v]) ve[v] = ve[u] + w;\n            if (--indeg[v] == 0) q[r++] = v;\n        }\n    }\n    if (r < n) { printf(\"0\\n\"); return 0; }\n    int tot = 0;\n    for (int i = 1; i <= n; i++) if (ve[i] > tot) tot = ve[i];\n    for (int i = 1; i <= n; i++) vl[i] = tot;\n    for (int i = r - 1; i >= 0; i--) {\n        int u = q[i];\n        for (int e = head[u]; e; e = nxt[e]) {\n            int v = to[e], w = wt[e];\n            if (vl[v] - w < vl[u]) vl[u] = vl[v] - w;\n        }\n    }\n    printf(\"%d\\n\", tot);\n    for (int u = 1; u <= n; u++)\n        for (int e = head[u]; e; e = nxt[e])\n            if (ve[u] + wt[e] == vl[to[e]])\n                printf(\"%d->%d\\n\", u, to[e]);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <algorithm>\nusing namespace std;\nstruct E { int u, v, w, idx; };\nint main() {\n    int n, m; cin >> n >> m;\n    vector<E> edges(m);\n    vector<vector<int>> adj(n + 1);\n    vector<int> indeg(n + 1, 0);\n    for (int i = 0; i < m; i++) {\n        cin >> edges[i].u >> edges[i].v >> edges[i].w;\n        edges[i].idx = i;\n        adj[edges[i].u].push_back(i);\n        indeg[edges[i].v]++;\n    }\n    vector<int> q;\n    for (int i = 1; i <= n; i++) if (!indeg[i]) q.push_back(i);\n    vector<int> ve(n + 1, 0);\n    for (size_t f = 0; f < q.size(); f++) {\n        int u = q[f];\n        for (int id : adj[u]) {\n            int v = edges[id].v, w = edges[id].w;\n            ve[v] = max(ve[v], ve[u] + w);\n            if (--indeg[v] == 0) q.push_back(v);\n        }\n    }\n    if ((int)q.size() < n) { cout << 0 << \"\\n\"; return 0; }\n    int tot = *max_element(ve.begin() + 1, ve.end());\n    vector<int> vl(n + 1, tot);\n    for (int i = n - 1; i >= 0; i--) {\n        int u = q[i];\n        for (int id : adj[u]) {\n            int v = edges[id].v, w = edges[id].w;\n            vl[u] = min(vl[u], vl[v] - w);\n        }\n    }\n    vector<E> crit;\n    for (auto &e : edges) if (ve[e.u] + e.w == vl[e.v]) crit.push_back(e);\n    sort(crit.begin(), crit.end(), [](const E &a, const E &b) {\n        return a.u != b.u ? a.u < b.u : a.idx > b.idx;\n    });\n    cout << tot << \"\\n\";\n    for (auto &e : crit) cout << e.u << \"->\" << e.v << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "7 8\n1 2 4\n1 3 3\n2 4 5\n3 4 3\n4 5 1\n4 6 6\n5 7 5\n6 7 2\n",
                "expected_stdout": "17\n1->2\n2->4\n4->6\n6->7\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4 4\n1 2 3\n1 3 3\n2 4 4\n3 4 4\n",
                "expected_stdout": "7\n1->3\n1->2\n2->4\n3->4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 3\n1 2 2\n2 3 2\n3 1 2\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "家庭房产",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 25,
        "tags": [
            "并查集",
            "图连通块",
            "多关键字排序",
            "L2-007"
        ],
        "statement_md": "PTA 天梯赛经典综合题 `L2-007 家庭房产`：给定每个人的家庭成员关系（父母、子女）以及各自名下的房产套数与总面积，凡有亲属关系的人都属于同一个**家庭**。\n\n请统计共有多少个家庭，并对每个家庭输出：\n`家庭最小编号（4位补零） 家庭人口数 人均房产套数 人均房产面积`（两位均值均保留 3 位小数）。\n按**人均面积降序**排列；若人均面积相同，则按**家庭最小编号升序**排列。\n\n★ 巧用并查集：合并两个集合时**永远让编号更小的当根**（`if (ra < rb) par[rb] = ra`），这样每个连通块的根天然就是该家庭的最小编号！",
        "input_format": "第一行正整数 `N`。\n\n随后 `N` 行，每行格式为：`编号 父 母 k 孩子1 ... 孩子k 房产套数 总面积`（编号为 0~9999 的整数，父母未知或去世填 `-1`）。",
        "output_format": "第一行输出家庭个数。\n\n随后每行输出一个家庭的信息：`%04d 人数 人均套数 人均面积`（保留 3 位小数）。",
        "constraints_md": "- 1 ≤ N ≤ 1000\n- 编号范围 0000 ~ 9999",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 06 讲 · 图",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <stdio.h>\n#include <stdlib.h>\nint par[10000], seen[10000], sets_v[10000], area_v[10000];\nstruct Fam { int id, cnt, ts, ta; } fams[10000];\nint find(int x) {\n    while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }\n    return x;\n}\nvoid uni(int a, int b) {\n    int ra = find(a), rb = find(b);\n    if (ra == rb) return;\n    if (ra < rb) par[rb] = ra;\n    else par[ra] = rb;\n}\nint cmp(const void *a, const void *b) {\n    const struct Fam *x = (const struct Fam *)a, *y = (const struct Fam *)b;\n    long long lhs = (long long)x->ta * y->cnt, rhs = (long long)y->ta * x->cnt;\n    if (lhs != rhs) return lhs > rhs ? -1 : 1;\n    return x->id - y->id;\n}\nint main(void) {\n    for (int i = 0; i < 10000; i++) par[i] = i;\n    int n;\n    scanf(\"%d\", &n);\n    while (n--) {\n        int id, fa, mo, k;\n        scanf(\"%d %d %d %d\", &id, &fa, &mo, &k);\n        seen[id] = 1;\n        if (fa != -1) { seen[fa] = 1; uni(id, fa); }\n        if (mo != -1) { seen[mo] = 1; uni(id, mo); }\n        while (k--) { int ch; scanf(\"%d\", &ch); seen[ch] = 1; uni(id, ch); }\n        scanf(\"%d %d\", &sets_v[id], &area_v[id]);\n    }\n    int fcnt = 0;\n    for (int i = 0; i < 10000; i++) {\n        if (seen[i] && find(i) == i) {\n            fams[fcnt++] = (struct Fam){i, 0, 0, 0};\n        }\n    }\n    for (int i = 0; i < 10000; i++) {\n        if (!seen[i]) continue;\n        int r = find(i);\n        for (int j = 0; j < fcnt; j++) {\n            if (fams[j].id == r) {\n                fams[j].cnt++;\n                fams[j].ts += sets_v[i];\n                fams[j].ta += area_v[i];\n                break;\n            }\n        }\n    }\n    qsort(fams, fcnt, sizeof(struct Fam), cmp);\n    printf(\"%d\\n\", fcnt);\n    for (int i = 0; i < fcnt; i++) {\n        printf(\"%04d %d %.3f %.3f\\n\", fams[i].id, fams[i].cnt,\n               (double)fams[i].ts / fams[i].cnt, (double)fams[i].ta / fams[i].cnt);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <vector>\n#include <queue>\n#include <algorithm>\n#include <iomanip>\nusing namespace std;\nstruct Fam { int id, cnt, ts, ta; };\nint main() {\n    int n; cin >> n;\n    vector<vector<int>> adj(10000);\n    vector<char> seen(10000, 0);\n    vector<int> sv(10000, 0), av(10000, 0);\n    while (n--) {\n        int id, fa, mo, k;\n        cin >> id >> fa >> mo >> k;\n        seen[id] = 1;\n        if (fa != -1) { seen[fa] = 1; adj[id].push_back(fa); adj[fa].push_back(id); }\n        if (mo != -1) { seen[mo] = 1; adj[id].push_back(mo); adj[mo].push_back(id); }\n        while (k--) {\n            int ch; cin >> ch;\n            seen[ch] = 1; adj[id].push_back(ch); adj[ch].push_back(id);\n        }\n        cin >> sv[id] >> av[id];\n    }\n    vector<char> vis(10000, 0);\n    vector<Fam> fams;\n    for (int i = 0; i < 10000; i++) {\n        if (!seen[i] || vis[i]) continue;\n        queue<int> q; q.push(i); vis[i] = 1;\n        Fam f{i, 0, 0, 0};\n        while (!q.empty()) {\n            int u = q.front(); q.pop();\n            f.id = min(f.id, u);\n            f.cnt++; f.ts += sv[u]; f.ta += av[u];\n            for (int v : adj[u]) if (!vis[v]) { vis[v] = 1; q.push(v); }\n        }\n        fams.push_back(f);\n    }\n    sort(fams.begin(), fams.end(), [](const Fam &x, const Fam &y) {\n        long long lhs = 1LL * x.ta * y.cnt, rhs = 1LL * y.ta * x.cnt;\n        return lhs != rhs ? lhs > rhs : x.id < y.id;\n    });\n    cout << fams.size() << \"\\n\" << fixed << setprecision(3);\n    for (auto &f : fams)\n        cout << setw(4) << setfill('0') << f.id << \" \" << f.cnt << \" \"\n             << (double)f.ts / f.cnt << \" \" << (double)f.ta / f.cnt << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4\n6666 5551 5552 1 7777 1 100\n1234 5678 9012 1 0002 2 300\n8888 -1 -1 0 1 1000\n2468 0001 0004 1 2222 1 500\n",
                "expected_stdout": "4\n8888 1 1.000 1000.000\n0001 4 0.250 125.000\n0002 4 0.500 75.000\n5551 4 0.250 25.000\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n0005 -1 -1 1 0002 3 150\n0008 -1 -1 0 2 100\n",
                "expected_stdout": "2\n0008 1 2.000 100.000\n0002 2 1.500 75.000\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n0010 0020 -1 0 2 200\n0020 -1 -1 1 0030 2 200\n0030 -1 -1 0 0 0\n",
                "expected_stdout": "1\n0010 3 1.333 133.333\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "「逻辑结构」到底指什么",
        "subject": "ds",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "逻辑结构",
            "基本概念"
        ],
        "choices": [
            "数据在计算机内存里的具体存放方式",
            "数据元素之间的逻辑关系，与怎么存储无关",
            "算法执行时间的度量方法",
            "数据的运算在机器上的实现"
        ],
        "source_section": "第 01 讲 · 绪论",
        "statement_md": "数据结构里说的**逻辑结构**，指的是下面哪一个？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**逻辑结构描述的是「元素之间什么关系」**——集合、线性、树、图四种，只跟数据本身有关。\n\n「放到内存里怎么放」是**存储结构**（顺序/链式/索引/散列）的事，同一张线性表既可以用数组存也可以用链表存，逻辑结构不变。"
            }
        ]
    },
    {
        "title": "同一逻辑结构可以有多种存储结构",
        "subject": "ds",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 1,
        "total_score": 8,
        "tags": [
            "逻辑结构",
            "存储结构"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 01 讲 · 绪论",
        "statement_md": "同一种逻辑结构（比如线性表）可以采用多种不同的存储结构来实现——顺序存储、链式存储都行，两边互不影响逻辑结构本身。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "对",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|对\n|正确\n|√\n|T\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**对**。逻辑结构与存储结构是两个层面：线性表逻辑上就是「一对一」的关系，落地时用顺序表还是链表任选，各有优劣——教材后面「顺序表 vs 链表怎么选」整节都在讲这件事。"
            }
        ]
    },
    {
        "title": "常数次内层循环的时间复杂度",
        "subject": "ds",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "时间复杂度",
            "大 O 记法"
        ],
        "choices": [
            "O(1)",
            "O(log n)",
            "O(n)",
            "O(n²)"
        ],
        "source_section": "第 01 讲 · 绪论",
        "statement_md": "看这段代码：\n\n```c\nfor (int i = 1; i <= n; i++)\n    for (int j = 1; j <= 100; j++)\n        s++;\n```\n\n它的时间复杂度是？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "C",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|C\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "内层循环**固定跑 100 次**，跟 n 无关——它是常数。总执行次数 ≈ 100n，大 O 记法丢掉常数因子，就是 **O(n)**。\n\n★ 常见错误是看到两层循环就条件反射选 O(n²)。判 O(n²) 的标准是**内层次数也随 n 增长**（比如 `j <= i`）。"
            }
        ]
    },
    {
        "title": "无向完全图的边数",
        "subject": "ds",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "基本术语",
            "完全图"
        ],
        "choices": [
            "n(n-1)/2",
            "n(n-1)",
            "n²",
            "n-1"
        ],
        "source_section": "第 06 讲 · 图",
        "statement_md": "`n` 个顶点的**无向完全图**有多少条边？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "A",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|A\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "每个顶点都和其余 `n-1` 个顶点相连，共 `n(n-1)` 个「端点计数」，但每条边被数了两次（无向边两端各记一次）→ **n(n-1)/2**。\n\n有向完全图才是 `n(n-1)`——弧有方向，`<u,v>` 和 `<v,u>` 是两条。"
            }
        ]
    },
    {
        "title": "邻接矩阵第 i 行的非零元个数 = 顶点 i 的出度",
        "subject": "ds",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 1,
        "total_score": 8,
        "tags": [
            "邻接矩阵",
            "出度入度"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 06 讲 · 图",
        "statement_md": "对**有向图**，邻接矩阵 `A[i][j] = 1` 表示弧 `<vi, vj>` 存在，所以第 `i` 行的非零元素个数就是顶点 `vi` 的出度，第 `i` 列的非零元素个数是入度。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "对",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|对\n|正确\n|√\n|T\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**对**。行是「我指向谁」（出度），列是「谁指向我」（入度）。这就是讲义 demo 里「行和出度、列和入度」那句实测结论——求度数连邻接表都不用建。"
            }
        ]
    },
    {
        "title": "单源最短路径该用哪个算法",
        "subject": "ds",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "Dijkstra",
            "最短路径"
        ],
        "choices": [
            "Prim",
            "Kruskal",
            "Floyd",
            "Dijkstra"
        ],
        "source_section": "第 06 讲 · 图",
        "statement_md": "求**边权非负**的带权图上，从一个源点到其余各顶点的最短路径，经典教材算法是？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "D",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|D\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**Dijkstra**：贪心地一轮一轮把「离源点最近的未定顶点」定下来。Prim/Kruskal 是**最小生成树**的算法（树，不是路径）；Floyd 求**全源**最短路，用它求单源是杀鸡用牛刀，而且它靠三重循环动态规划、复杂度 O(n³)。\n\n★ Dijkstra 的命门：**不能有负权边**——讲义给过实测反例。"
            }
        ]
    },
    {
        "title": "折半查找的适用前提",
        "subject": "ds",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "折半查找",
            "有序表"
        ],
        "choices": [
            "链式存储即可，元素有无序都行",
            "顺序存储，且元素按关键字有序",
            "任意存储，只要元素互不相同",
            "必须是用散列函数组织好的表"
        ],
        "source_section": "第 07 讲 · 查找",
        "statement_md": "折半查找（二分查找）要求线性表满足什么条件？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "两个条件**缺一不可**：**有序**（才能判断去左半还是右半）＋**顺序存储**（才能 O(1) 跳到 mid）。\n\n链表虽然也可以有序，但找 mid 只能顺着链走 O(n)，折半的效率优势整个消失——所以教材口径是「顺序存储的有序表」。"
            }
        ]
    },
    {
        "title": "11 个元素折半查找的平均查找长度",
        "subject": "ds",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "折半查找",
            "ASL",
            "判定树"
        ],
        "choices": [
            "3.0",
            "4.0",
            "11/4 ≈ 2.75",
            "log₂11 ≈ 3.46"
        ],
        "source_section": "第 07 讲 · 查找",
        "statement_md": "对含 `n = 11` 个元素的有序表做折半查找，**成功查找**的平均查找长度 ASL 是多少？\n\n（提示：比较次数分布为 1 次 ×1、2 次 ×2、3 次 ×4、4 次 ×4）",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "A",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|A\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "ASL = (1×1 + 2×2 + 3×4 + 4×4) / 11 = 33/11 = **3.0**。\n\n这是讲义 demo 的实测值：判定树逐层数结点，最多比较层数是 `⌊log₂11⌋ + 1 = 4`，失败查找同样 4 次。选 D 的人是把「层数公式」当成了平均长度。"
            }
        ]
    },
    {
        "title": "散列冲突可以完全避免",
        "subject": "ds",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 1,
        "total_score": 8,
        "tags": [
            "散列表",
            "冲突"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 07 讲 · 查找",
        "statement_md": "只要散列函数设计得足够好，散列表的冲突就可以完全避免。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "错",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|错\n|错误\n|×\n|F\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**错**。散列是「任意键 → 有限槽位」的映射，键的取值空间通常远大于槽位数，冲突在数学上**不可避免**（鸽笼原理）。\n\n好的散列函数只能**减少**冲突，真正的功夫在**怎么处理冲突**：线性探测、链地址法……这正是 7.4 节半章篇幅的内容。"
            }
        ]
    },
    {
        "title": "下列排序算法中稳定的是",
        "subject": "ds",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "稳定性",
            "内部排序"
        ],
        "choices": [
            "直接插入排序",
            "简单选择排序",
            "快速排序",
            "堆排序"
        ],
        "source_section": "第 08 讲 · 排序",
        "statement_md": "下面几种内部排序中，**稳定**的是？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "A",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|A\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**直接插入稳定**：相等元素只从后往前找插入点、遇到相等就停，不会越过同类。\n\n另外三个都不稳定（讲义 demo 用 {3a, 3h, 1} 最小反例实测现形）：\n- **简单选择**：first-min 远距离交换会跨越等值元素；\n- **快排**：双向扫描会把等值元素甩到枢轴另一侧；\n- **堆排**：堆顶换末尾的远距离交换同理。\n\n★ 稳定的还有：冒泡、归并、基数——口诀「插冒归基稳」。"
            }
        ]
    },
    {
        "title": "快速排序最坏情况的时间复杂度",
        "subject": "ds",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "快速排序",
            "时间复杂度"
        ],
        "choices": [
            "O(n)",
            "O(n log n)",
            "O(n²)",
            "O(log n)"
        ],
        "source_section": "第 08 讲 · 排序",
        "statement_md": "快速排序在**最坏情况**（比如每次枢轴都选到最值、序列已经有序）下，时间复杂度是？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "C",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|C\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "最坏时每趟划分只分出「1 个 vs n-1 个」，递归深度退到 n 层，总比较次数是等差数列之和 → **O(n²)**。\n\n平均才是 O(n log n)。这就是「快排怕有序」——讲义实测 1..15 顺序插入再快排，划分退化得一模一样。工程上用三者取中/随机枢轴来躲开这个坑。"
            }
        ]
    },
    {
        "title": "基本有序时直接插入排序接近 O(n)",
        "subject": "ds",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 1,
        "total_score": 8,
        "tags": [
            "直接插入",
            "希尔排序",
            "时间复杂度"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 08 讲 · 排序",
        "statement_md": "如果初始序列**基本有序**，直接插入排序的比较和移动次数都会很少，整体时间接近 O(n)。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "对",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|对\n|正确\n|√\n|T\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**对**。每个元素的插入点都几乎在原地，内层 while 基本一两次就停。极端情况：完全有序时每趟只比较 1 次，共 n-1 次——O(n)。\n\n这正是**希尔排序**存在的理由：先用大步长把序列「拍得基本有序」，最后一趟直接插入收尾时就是 O(n) 的舒适区。"
            }
        ]
    },
    {
        "title": "稳定的排序算法有哪些",
        "subject": "ds",
        "line": "text",
        "question_type": "multiple_choice",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "稳定性",
            "内部排序",
            "多选"
        ],
        "choices": [
            "直接插入排序",
            "冒泡排序",
            "堆排序",
            "归并排序"
        ],
        "source_section": "第 08 讲 · 排序",
        "statement_md": "下列内部排序算法中，**稳定**的有哪些？\n\n（提醒：稳定性 = 相等元素排序后相对次序不变）\n\n**多选题**：正确选项不止一个，点选切换，再次点击可取消。",
        "input_format": "",
        "output_format": "若干个选项字母，按字母升序连写（如 `AC`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ABD",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ABD\n|ADB\n|BAD\n|BDA\n|DAB\n|DBA\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "稳定的三个：**直接插入**（相等就停，不越过同类）、**冒泡**（严格大于才交换）、**归并**（两边相等取左段）。\n\n**堆排序不稳定**：堆顶与末尾的远距离交换会把等值元素甩开——讲义 demo 用 {3a, 3h, 1} 实测现形。\n\n口诀：**插冒归基稳，选择快希堆不稳**。"
            }
        ]
    },
    {
        "title": "邻接矩阵与邻接表的说法辨析",
        "subject": "ds",
        "line": "text",
        "question_type": "multiple_choice",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "邻接矩阵",
            "邻接表",
            "存储结构",
            "多选"
        ],
        "choices": [
            "无向图的邻接矩阵一定是对称矩阵",
            "邻接表更适合存稀疏图",
            "邻接矩阵更适合存稀疏图",
            "邻接矩阵判断两个顶点是否邻接是 O(1)"
        ],
        "source_section": "第 06 讲 · 图",
        "statement_md": "关于图的两种存储结构，下列说法**正确**的有哪些？\n\n**多选题**：正确选项不止一个，点选切换，再次点击可取消。",
        "input_format": "",
        "output_format": "若干个选项字母，按字母升序连写（如 `AC`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ABD",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ABD\n|ADB\n|BAD\n|BDA\n|DAB\n|DBA\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "A 对：无向边 (u,v) 在矩阵里两个方向都置 1，必然对称。\n\nB 对、**C 错**：邻接表空间 O(n+e)，稀疏图省得厉害；邻接矩阵固定 O(n²)——边少时全是浪费，它适合**稠密图**。\n\nD 对：矩阵下标直接查 `A[u][v]`，一步到位；邻接表反而要扫链 O(deg)。"
            }
        ]
    },
    {
        "title": "一句话说明什么是稳定排序",
        "subject": "ds",
        "line": "text",
        "question_type": "short_answer",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "稳定性",
            "简答"
        ],
        "choices": [],
        "source_section": "第 08 讲 · 排序",
        "statement_md": "**简答题**：用一句话说明「稳定排序」的含义。\n\n按下面的句式作答：`相等元素……相对次序……`",
        "input_format": "",
        "output_format": "一句话作答（不要写解释、不要抄题目）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "相等元素排序后相对次序保持不变",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|相等元素排序后相对次序保持不变\n|相等元素排序后相对次序不变\n|相等的元素排序后相对次序保持不变\n|值相同的元素排序后相对次序不变\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "参考答案：**相等元素排序后相对次序保持不变**。\n\n展开说：序列里若有多个关键字相同的记录，稳定排序保证排完序后它们的先后顺序与排序前一致（如 49a 一直在 49h 前面）；不稳定排序则可能交换它们的相对位置。\n\n稳定性有什么用？对**多关键字排序**是刚需：先按次要关键字排好，再用稳定的主关键字排序，次要关键字的次序得以保留——基数排序就是靠「每趟都用稳定排序」立住的。"
            }
        ]
    },
    {
        "title": "写出数据结构的三要素",
        "subject": "ds",
        "line": "text",
        "question_type": "short_answer",
        "difficulty": 1,
        "total_score": 12,
        "tags": [
            "三要素",
            "基本概念",
            "简答"
        ],
        "choices": [],
        "source_section": "第 01 讲 · 绪论",
        "statement_md": "**简答题**：写出**数据结构的三要素**，用顿号或空格分隔（按讲义顺序：两个「结构」在前，运算在后）。",
        "input_format": "",
        "output_format": "一句话作答（不要写解释、不要抄题目）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "逻辑结构、存储结构、运算",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|逻辑结构、存储结构、运算\n|逻辑结构 存储结构 运算\n|数据的逻辑结构、数据的存储结构、数据的运算\n|逻辑结构、存储结构、数据的运算\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "参考答案：**逻辑结构、存储结构、运算**。\n\n- **逻辑结构**：元素之间「什么关系」（集合/线性/树/图）；\n- **存储结构**：关系「怎么落进内存」（顺序/链式/索引/散列）；\n- **运算**：在这种结构上「能干什么」（定义在逻辑结构上、实现在存储结构上）。\n\n三者缺一不可：只讲关系不讲落地是数学，只讲落地不讲关系是纯编程。"
            }
        ]
    },
    {
        "title": "顺序表插入的平均移动次数",
        "subject": "ds",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "顺序表",
            "平均移动次数"
        ],
        "choices": [
            "n/2",
            "n",
            "(n-1)/2",
            "n-1"
        ],
        "source_section": "第 02 讲 · 线性表",
        "statement_md": "长度为 `n` 的顺序表，在**等概率**下按位序插入一个元素，平均要移动多少个元素？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "A",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|A\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "插到第 `i` 位要移动 `n-i+1` 个，i 取 1..n+1 等概率平均：Σ(n-i+1)/(n+1) = **n/2**。\n\n对照记忆：删除的平均移动是 **(n-1)/2** —— 插删这两个公式考试最爱配对出现，别背混。"
            }
        ]
    },
    {
        "title": "头插法建单链表的结点次序",
        "subject": "ds",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "单链表",
            "头插法"
        ],
        "choices": [
            "a1 a2 a3",
            "a3 a2 a1",
            "a2 a1 a3",
            "a1 a3 a2"
        ],
        "source_section": "第 02 讲 · 线性表",
        "statement_md": "用**头插法**把 `a1, a2, a3` 依次插入空单链表，建好后的结点次序是？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "头插法 = 新结点总插在**表头**。a1 先进，a2 插到它前面，a3 再插到最前面 → **a3 a2 a1**，与输入顺序**正好相反**。\n\n图、散列桶的邻接链用的也是这个插法（教材惯例）——PTA 里那道「无向图的邻接表（头插法）」考的就是这条。想保持原序就得用**尾插法**。"
            }
        ]
    },
    {
        "title": "循环单链表尾结点的 next 指向头结点",
        "subject": "ds",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 1,
        "total_score": 8,
        "tags": [
            "循环链表",
            "单链表"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 02 讲 · 线性表",
        "statement_md": "在**带头结点**的循环单链表里，尾结点的 `next` 域指向**头结点**。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "对",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|对\n|正确\n|√\n|T\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**对**。这正是「循环」的含义：`尾.next == 头`，整条链成环。\n\n实战价值：判空是 `head->next == head`（而不是普通单链表的 `head->next == NULL`）；从任一结点出发都能扫全表——所以「只设尾指针 R」的循环链表能做到两头 O(1) 操作。"
            }
        ]
    },
    {
        "title": "哪个出栈序列是不可能的",
        "subject": "ds",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "栈",
            "出栈序列",
            "卡特兰数"
        ],
        "choices": [
            "1 2 3",
            "3 2 1",
            "2 1 3",
            "3 1 2"
        ],
        "source_section": "第 03 讲 · 栈和队列",
        "statement_md": "三个元素按 `1, 2, 3` 的顺序依次进栈（进出可以交错），**不可能**得到的出栈序列是？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "D",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|D\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**3 1 2 不可能**：想先弹出 3，必须 1、2、3 都已进栈；3 出来后栈顶是 2，第二个只能弹 2，弹不出 1。\n\n判定法（讲义里的「逐个模拟」）：把出栈序列当目标，元素按 1..n 进栈，栈顶一等于目标就弹——弹不动还不齐，就是假序列。\n\n★ n 个元素合法出栈序列数 = 卡特兰数 C(2n,n)/(n+1)，n=3 时 5 种（总共 6 种排列，恰好只有 `3 1 2` 这一种不合法）。"
            }
        ]
    },
    {
        "title": "循环队列牺牲一格的队满条件",
        "subject": "ds",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 2,
        "total_score": 8,
        "tags": [
            "循环队列",
            "队满条件",
            "假溢出"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 03 讲 · 栈和队列",
        "statement_md": "循环队列用「牺牲一个存储单元」区分队空与队满时，队满条件是`(rear + 1) % m == front`（m 为队列容量）。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "对",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|对\n|正确\n|√\n|T\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**对**。不牺牲一格的话，队空（`front == rear`）和队满（也 `front == rear`）没法区分——这就是讲义里「假溢出」之后必须做的取舍。\n\n代价：实际最多存 `m-1` 个元素。另两种方案：设 size 计数器、设 tag 标记上一次是入队还是出队。"
            }
        ]
    },
    {
        "title": "递归调用背后是什么结构",
        "subject": "ds",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "栈",
            "递归",
            "递归工作栈"
        ],
        "choices": [
            "队列",
            "栈",
            "线性表（顺序）",
            "树"
        ],
        "source_section": "第 03 讲 · 栈和队列",
        "statement_md": "函数递归调用（比如阶乘、汉诺塔）的「保存现场、返回时恢复」，系统背后用的是哪种数据结构？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**栈**——递归工作栈。每次调用压一帧（参数+局部变量+返回地址），返回时弹一帧。后进先出正好匹配「最后调用的最先返回」。\n\n所以任何递归都能**用显式栈改成非递归**（3.4.4 的方法）；递归太深爆的「栈溢出」就是这栈满了。"
            }
        ]
    },
    {
        "title": "教材口径的 next[1] 等于几",
        "subject": "ds",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "KMP",
            "next 数组",
            "下标口径"
        ],
        "choices": [
            "-1",
            "0",
            "1",
            "不存在"
        ],
        "source_section": "第 04 讲 · 串、数组和广义表",
        "statement_md": "KMP 算法里，模式串位序**从 1 开始**（教材口径），`next[1]` 的值是？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "教材（位序从 1 起）规定 **next[1] = 0**——它是个「哨兵」：表示「主串指针 i 前移一位、模式串回到开头重比」。\n\n★ 下标从 1 起是全书的隐形坑：网上不少资料位序从 0 起、next[0] = -1，那套值和教材的整套差一位，抄之前先看清自己的下标口径。"
            }
        ]
    },
    {
        "title": "对称矩阵下三角压缩的下标公式",
        "subject": "ds",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "特殊矩阵",
            "压缩存储",
            "下标口径"
        ],
        "choices": [
            "i(i-1)/2 + j",
            "i(i-1)/2 + j - 1",
            "j(j-1)/2 + i",
            "i(i+1)/2 + j"
        ],
        "source_section": "第 04 讲 · 串、数组和广义表",
        "statement_md": "`n` 阶对称矩阵按**下三角**（含对角线）行优先压缩进一维数组 `sa`，且 `sa` 的**位序也从 1 起**。元素 `a[i][j]`（`i ≥ j`）存在 `sa[k]`，则 `k` = ？\n\n提示：题面已钉死「sa 位序从 1 起」，套公式前先验算 a[1][1]",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "A",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|A\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "第 `i` 行之前有 1..i-1 行，共 `1+2+…+(i-1) = i(i-1)/2` 个元素；行内 `a[i][j]` 前面还有 `j-1` 个 → k = i(i-1)/2 + (j-1) + 1 = **i(i-1)/2 + j**。\n\n验算两头：`a[1][1]` → k=1（sa 第一个），`a[2][1]` → k=2，`a[2][2]` → k=3 —— 全对得上。\n\n★ 本讲最大的坑就是**下标口径**：教材位序从 1 起，网上不少资料从 0 起（那种口径才是 `i(i-1)/2 + j - 1`，即 B 项）。套公式前先核对题面的「从几起」，B/C/D 都是一个符号位错出来的干扰项。"
            }
        ]
    },
    {
        "title": "快速转置需要预先算 num 和 cpot",
        "subject": "ds",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 2,
        "total_score": 8,
        "tags": [
            "稀疏矩阵",
            "快速转置",
            "三元组"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 04 讲 · 串、数组和广义表",
        "statement_md": "稀疏矩阵的**快速转置**之所以快，是因为它先用一遍扫描统计每列非零元个数 `num[]`，再推出每列第一个非零元在目标三元组表中的位置 `cpot[]`，然后一遍放好——不需要按列反复扫描整个表。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "对",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|对\n|正确\n|√\n|T\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**对**。普通转置 O(nu × tu)（对每一列扫全表），快速转置O(nu + tu)（两个线性趟）。\n\n★ 讲义实测大坑：`cpot[col+1] = cpot[col] + num[col]` 这步的累加基准要是写漏，数据会整段错位——demo 里「漏 cpot++ 丢数据」那条陷阱说的就是它。"
            }
        ]
    },
    {
        "title": "二叉树叶子数与度 2 结点数的关系",
        "subject": "ds",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "二叉树性质",
            "叶子结点"
        ],
        "choices": [
            "n0 = n2",
            "n0 = n2 + 1",
            "n2 = n0 + 1",
            "n0 = 2·n2"
        ],
        "source_section": "第 05 讲 · 树和二叉树",
        "statement_md": "任意一棵二叉树，叶子结点数 `n0` 与度数为 2 的结点数 `n2` 满足？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**n0 = n2 + 1**。从边的条数推：n 个结点 n-1 条边，每条边出自一个非叶结点，即 n-1 = n1 + 2·n2；又 n = n0+n1+n2，两式一消就得到 n0 = n2+1。\n\n它跟「度数」无关地恒成立——考题常给几个 n1/n2 让你算叶子数，直接套这个式子比画树快。"
            }
        ]
    },
    {
        "title": "哪种遍历组合能唯一确定一棵二叉树",
        "subject": "ds",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "遍历",
            "唯一确定",
            "先序中序"
        ],
        "choices": [
            "先序 + 后序",
            "先序 + 中序",
            "只有先序",
            "层次 + 后序"
        ],
        "source_section": "第 05 讲 · 树和二叉树",
        "statement_md": "已知两种遍历序列，**能唯一确定**一棵二叉树的组合是？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**先序 + 中序**（以及中序 + 后序、中序 + 层次）可以；**先序 + 后序不行**——两个都缺「左右子树的分界」信息，只有一个结点的子树时分不清它在左还是右（反例：任何一条链都有多棵树对应）。\n\n原理：先序首个是根 → 在中序里切出左右子树 → 递归。教材 5.5.1「由遍历序列确定二叉树」的高频大题就考这个。"
            }
        ]
    },
    {
        "title": "哈夫曼树没有度为 1 的结点",
        "subject": "ds",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 2,
        "total_score": 8,
        "tags": [
            "哈夫曼树",
            "二叉树性质",
            "WPL"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 05 讲 · 树和二叉树",
        "statement_md": "哈夫曼树（最优二叉树）中不存在度数为 1 的结点。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "对",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|对\n|正确\n|√\n|T\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**对**。哈夫曼树每次合并**两个**最小权结点成一个新的度 2 结点，从不产生独苗——所以结点只有叶（n0）和度 2（n2），且 n0 = n2+1，总结点数 = 2·n0 − 1（奇数）。\n\n推论也是考点：n 个权值建哈夫曼树，一共要合并 n−1 次。「WPL = Σ 权值 × 路长」另有一条捷径：WPL 也等于**所有非叶结点权值之和**——讲义 demo 双路复算对过。"
            }
        ]
    }
]
