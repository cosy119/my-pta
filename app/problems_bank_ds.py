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

覆盖范围：数据结构第 02 ~ 05 讲（线性表 / 栈与队列 / 串数组广义表 / 树与二叉树）。
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
    }
]
