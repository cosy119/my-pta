# -*- coding: utf-8 -*-
"""C/C++ 编程精练题库 —— 自动生成，**不要手改本文件**。

生成器：tools/gen_ds_prog.py
分节：编程精练 · C/C++（10 题）

重生成：python tools/gen_ds_prog.py
"""

DS_PROG_PROBLEMS: list[dict] = [
    {
        "title": "顺序表删除重复元素",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "编程精练",
            "顺序表",
            "双指针"
        ],
        "statement_md": "给定一个**非降序**的顺序表，**就地**删除所有重复元素（每个值只保留一个），输出删除后的长度和序列。\n\n要求空间复杂度 `O(1)`——不许开新数组。\n\n★ 这题的钥匙是「有序」两个字：重复元素一定**挨在一起**。于是维护一个慢指针 `i` 指向「已保留部分的末尾」，快指针 `j` 一路向前扫；只要 `a[j] != a[i]`，就把 `a[j]` 挪到 `i+1` 去。\n\n⚠️ 如果表无序，这个双指针法就**不成立**了，只能 `O(n²)` 对每个元素往回扫，或者开哈希表——那就不是 `O(1)` 空间了。题目条件不是摆设。",
        "input_format": "第一行 `n`；第二行 `n` 个整数（**非降序**）。",
        "output_format": "两行：去重后的长度；去重后的序列（空格分隔）。",
        "constraints_md": "- 1 ≤ n ≤ 10⁵\n- 序列非降序\n- 要求 O(1) 额外空间",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "编程精练 · C/C++",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <vector>\nusing namespace std;\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    vector<int> a(n);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n\n    int i = 0;                        // 慢指针：已保留部分的末尾\n    for (int j = 1; j < n; j++) {\n        if (a[j] != a[i]) {\n            i++;\n            a[i] = a[j];\n        }\n    }\n    int len = i + 1;\n\n    printf(\"%d\\n\", len);\n    for (int k = 0; k < len; k++) {\n        printf(\"%d\", a[k]);\n        putchar(k + 1 == len ? '\\n' : ' ');\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n\n    int n;\n    if (!(cin >> n)) return 0;\n    vector<int> a(n);\n    for (int i = 0; i < n; i++) cin >> a[i];\n\n    // 另一条路：std::unique（它做的就是「相邻去重 + 返回新末尾」，\n    // 正好是本题双指针的库版本），配上 distance 求长度。\n    auto tail = unique(a.begin(), a.end());\n    int len = (int)distance(a.begin(), tail);\n\n    cout << len << '\\n';\n    for (int k = 0; k < len; k++) {\n        if (k) cout << ' ';\n        cout << a[k];\n    }\n    cout << '\\n';\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "6\n1 1 2 2 3 3\n",
                "expected_stdout": "3\n1 2 3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n7\n",
                "expected_stdout": "1\n7\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n1 2 3 4 5\n",
                "expected_stdout": "5\n1 2 3 4 5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "8\n-3 -3 -3 0 0 5 5 5\n",
                "expected_stdout": "3\n-3 0 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n2 2 2 2\n",
                "expected_stdout": "1\n2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "用数组模拟链表就地逆置",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "编程精练",
            "链表",
            "指针",
            "静态链表"
        ],
        "statement_md": "用**静态链表**存 `n` 个整数：`data[i]` 放值，`next[i]` 放下一个节点的下标（下标从 1 起，`0` 表示空）。初始 `head = 1`，节点依次串联。\n\n把这个链表**就地**逆置（不许新建节点、不许开新数组存值，只能改 `next`），输出三行：\n1. 逆置后从头遍历得到的序列\n2. 新的 `head`\n3. 逆置过程中 **`next` 被改写的次数**\n\n★ 逆置三件套：`follow = next[cur]` 先记住后路，`next[cur] = prev` 掉头，`prev = cur; cur = follow` 一起前进。\n\n⚠️ 顺序千万不能乱：**先存 `follow` 再改 `next[cur]`**。反过来写的话，`cur` 的后继信息已经被覆盖，链当场断掉——这是链表题第一大坑。\n\n★ 每个节点恰好被改一次 `next`，所以改写次数就是 `n`。能自己推导出这个数，说明你真的看懂了循环执行了几轮。",
        "input_format": "第一行 `n`；第二行 `n` 个整数（按链表顺序）。",
        "output_format": "三行：逆置后序列；新的 head 下标；next 改写次数。",
        "constraints_md": "- 1 ≤ n ≤ 10⁵\n- |元素| ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "编程精练 · C/C++",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <vector>\nusing namespace std;\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n\n    vector<int> data(n + 1), nxt(n + 1);\n    for (int i = 1; i <= n; i++) {\n        scanf(\"%d\", &data[i]);\n        nxt[i] = (i < n) ? i + 1 : 0;\n    }\n\n    int head = 1;\n    int prev = 0, cur = head, rewrites = 0;\n    while (cur) {\n        int follow = nxt[cur];   // 先记后路\n        nxt[cur] = prev;         // 再掉头\n        prev = cur;\n        cur = follow;\n        rewrites++;\n    }\n    head = prev;\n\n    int p = head;\n    bool first = true;\n    while (p) {\n        if (!first) putchar(' ');\n        printf(\"%d\", data[p]);\n        first = false;\n        p = nxt[p];\n    }\n    putchar('\\n');\n    printf(\"%d\\n%d\\n\", head, rewrites);\n    return 0;\n}\n",
        "alt_solution": "#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n\n    int n;\n    if (!(cin >> n)) return 0;\n    vector<int> data(n + 1), nxt(n + 1);\n    for (int i = 1; i <= n; i++) {\n        cin >> data[i];\n        nxt[i] = (i < n) ? i + 1 : 0;\n    }\n\n    // 另一条路：三指针同时推进，但把「头结点的接管」放在循环外单独做，\n    // 循环里只处理「已经确定 prev 的情况」。\n    int head = 1;\n    if (head != 0) {\n        int prev = head;\n        int cur = nxt[head];\n        nxt[head] = 0;              // 原来的头变成新尾巴\n        while (cur) {\n            int follow = nxt[cur];\n            nxt[cur] = prev;\n            prev = cur;\n            cur = follow;\n        }\n        head = prev;\n    }\n\n    int rewrites = n;               // 每个节点恰好改一次 next\n    int p = head;\n    string out;\n    out.reserve((size_t)n * 4);\n    while (p) {\n        out += to_string(data[p]);\n        p = nxt[p];\n        if (p) out += ' ';\n    }\n    cout << out << '\\n' << head << '\\n' << rewrites << '\\n';\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n1 2 3 4 5\n",
                "expected_stdout": "5 4 3 2 1\n5\n5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n42\n",
                "expected_stdout": "42\n1\n1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n-1 -2\n",
                "expected_stdout": "-2 -1\n2\n2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "6\n10 20 30 40 50 60\n",
                "expected_stdout": "60 50 40 30 20 10\n6\n6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "循环队列的操作序列模拟",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 12,
        "tags": [
            "编程精练",
            "队列",
            "循环队列",
            "判空判满"
        ],
        "statement_md": "用一个**容量 `MAXSIZE = 5`** 的循环队列（数组实现，**牺牲一个存储单元**来区分队空与队满），依次执行 `m` 条操作，对每条操作输出一行结果。\n\n队空 `front == rear`，队满 `(rear + 1) % MAXSIZE == front`，元素个数 `(rear - front + MAXSIZE) % MAXSIZE`。因此**实际最多存 4 个元素**。\n\n| 操作 | 输出 |\n|---|---|\n| `push x` | 队满输出 `FULL`，否则入队并输出 `OK` |\n| `pop` | 队空输出 `EMPTY`，否则弹出队头并输出该值 |\n| `front` | 队空输出 `EMPTY`，否则输出队头（不弹出） |\n| `size` | 输出当前元素个数 |\n\n★ 为什么必须「牺牲一个单元」：只用 `front == rear` 一个条件，**队空和队满的表达式完全一样**，没法区分。留一个空位后，`rear` 永远追不上 `front`，两者就分开了。\n\n★ 另一种做法是额外维护 `count`，那就不必牺牲单元（能存满 5 个）——但本题**明确规定**用牺牲单元法，注意别把容量上限搞错。",
        "input_format": "第一行 `m`；之后 `m` 行，每行一条操作。",
        "output_format": "`m` 行，每行对应一条操作的输出。",
        "constraints_md": "- 1 ≤ m ≤ 10⁵\n- 1 ≤ x ≤ 10⁹\n- MAXSIZE 固定为 5（最多存 4 个）",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "编程精练 · C/C++",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <cstring>\nusing namespace std;\n\nconst int MAXSIZE = 5;\n\nint main() {\n    int m;\n    if (scanf(\"%d\", &m) != 1) return 0;\n\n    static int q[MAXSIZE];\n    int front = 0, rear = 0;\n\n    char op[16];\n    for (int i = 0; i < m; i++) {\n        scanf(\"%s\", op);\n        if (strcmp(op, \"push\") == 0) {\n            int x;\n            scanf(\"%d\", &x);\n            if ((rear + 1) % MAXSIZE == front) {\n                printf(\"FULL\\n\");\n            } else {\n                q[rear] = x;\n                rear = (rear + 1) % MAXSIZE;\n                printf(\"OK\\n\");\n            }\n        } else if (strcmp(op, \"pop\") == 0) {\n            if (front == rear) {\n                printf(\"EMPTY\\n\");\n            } else {\n                printf(\"%d\\n\", q[front]);\n                front = (front + 1) % MAXSIZE;\n            }\n        } else if (strcmp(op, \"front\") == 0) {\n            if (front == rear) printf(\"EMPTY\\n\");\n            else printf(\"%d\\n\", q[front]);\n        } else {\n            printf(\"%d\\n\", (rear - front + MAXSIZE) % MAXSIZE);\n        }\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <bits/stdc++.h>\nusing namespace std;\n\nconst int MAXSIZE = 5;\n\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n\n    int m;\n    if (!(cin >> m)) return 0;\n\n    // 另一条路：不用 front/rear 两个游标，改成「基址 + 头 + 计数器」。\n    // 只要 count 上限写成 MAXSIZE-1，行为就与牺牲单元法完全等价。\n    vector<int> buf(MAXSIZE);\n    int base = 0;       // 队头所在的物理下标\n    int count = 0;\n\n    string op;\n    for (int i = 0; i < m; i++) {\n        cin >> op;\n        if (op == \"push\") {\n            int x;\n            cin >> x;\n            if (count == MAXSIZE - 1) {\n                cout << \"FULL\\n\";\n            } else {\n                buf[(base + count) % MAXSIZE] = x;\n                count++;\n                cout << \"OK\\n\";\n            }\n        } else if (op == \"pop\") {\n            if (count == 0) {\n                cout << \"EMPTY\\n\";\n            } else {\n                cout << buf[base] << '\\n';\n                base = (base + 1) % MAXSIZE;\n                count--;\n            }\n        } else if (op == \"front\") {\n            if (count == 0) cout << \"EMPTY\\n\";\n            else cout << buf[base] << '\\n';\n        } else {\n            cout << count << '\\n';\n        }\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "8\npush 1\npush 2\npush 3\npush 4\npush 5\nfront\npop\nsize\n",
                "expected_stdout": "OK\nOK\nOK\nOK\nFULL\n1\n1\n3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "6\npop\nfront\nsize\npush 9\nfront\nsize\n",
                "expected_stdout": "EMPTY\nEMPTY\n0\nOK\n9\n1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "9\npush 1\npop\npush 2\npop\nsize\nfront\npop\npop\nfront\n",
                "expected_stdout": "OK\n1\nOK\n2\n0\nEMPTY\nEMPTY\nEMPTY\nEMPTY\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\nsize\npush 7\npush 8\nsize\nfront\n",
                "expected_stdout": "0\nOK\nOK\n2\n7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "中缀表达式转后缀",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 12,
        "tags": [
            "编程精练",
            "栈",
            "表达式求值",
            "调度场"
        ],
        "statement_md": "读入一行**中缀表达式**（操作数为单个 `0-9` 数字或小写字母，运算符只有 `+ - * /` 与括号，**不含空格、不含一元负号**），输出两行：\n1. 对应的**后缀表达式**（逆波兰式，不加空格）\n2. 该表达式的值（整数，除法**向零截断**，与 C/C++ 的 `/` 一致）\n\n调度场（shunting-yard）的规则只有三条：\n- 遇操作数：直接进输出\n- 遇 `(`：压栈\n- 遇运算符：把栈顶**优先级 ≥ 自己**的运算符全弹到输出，再压自己（`(` 优先级最低，弹不动）\n- 遇 `)`：弹到遇到 `(` 为止，`(` 丢弃\n\n★ 后缀求值只要一个栈：遇数字压栈，遇运算符就弹两个（**先弹出来的是右操作数**）算完压回。\n\n⚠️ 两个高频错：\n1. 减法/除法弹出顺序写反 → `a-b` 算成 `b-a`；\n2. 用 Python 的 `//` 做整除——它是**向下取整**，`-7//2 = -4`，而 C 的 `-7/2 = -3`（向零截断）。跨语言对照时必须自己实现截断除法。",
        "input_format": "一行中缀表达式（长度 ≤ 200）。",
        "output_format": "两行：后缀表达式；表达式的值。",
        "constraints_md": "- 1 ≤ 表达式长度 ≤ 200\n- 保证合法、除数非 0、中间结果在 32 位整数内",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "编程精练 · C/C++",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <cstring>\n#include <string>\n#include <vector>\nusing namespace std;\n\nstatic int prec(char c) {\n    if (c == '+' || c == '-') return 1;\n    if (c == '*' || c == '/') return 2;\n    return 0;                       // '('\n}\n\nint main() {\n    char buf[512];\n    if (!fgets(buf, sizeof(buf), stdin)) return 0;\n    string s(buf);\n    while (!s.empty() && (s.back() == '\\n' || s.back() == '\\r')) s.pop_back();\n\n    string out;\n    vector<char> st;\n    for (char ch : s) {\n        if ((ch >= '0' && ch <= '9') || (ch >= 'a' && ch <= 'z')) {\n            out += ch;\n        } else if (ch == '(') {\n            st.push_back(ch);\n        } else if (ch == ')') {\n            while (!st.empty() && st.back() != '(') {\n                out += st.back();\n                st.pop_back();\n            }\n            if (!st.empty()) st.pop_back();\n        } else {\n            while (!st.empty() && prec(st.back()) >= prec(ch)) {\n                out += st.back();\n                st.pop_back();\n            }\n            st.push_back(ch);\n        }\n    }\n    while (!st.empty()) {\n        out += st.back();\n        st.pop_back();\n    }\n\n    vector<long long> vs;\n    for (char ch : out) {\n        if (ch >= '0' && ch <= '9') {\n            vs.push_back(ch - '0');\n        } else if (ch >= 'a' && ch <= 'z') {\n            vs.push_back(ch - 'a' + 1);\n        } else {\n            long long b = vs.back(); vs.pop_back();\n            long long a = vs.back(); vs.pop_back();\n            long long r = 0;\n            if (ch == '+') r = a + b;\n            else if (ch == '-') r = a - b;\n            else if (ch == '*') r = a * b;\n            else r = a / b;          // C 的整除天然向零截断\n            vs.push_back(r);\n        }\n    }\n\n    printf(\"%s\\n%lld\\n\", out.c_str(), vs.back());\n    return 0;\n}\n",
        "alt_solution": "#include <bits/stdc++.h>\nusing namespace std;\n\nstatic int prec(char c) {\n    switch (c) {\n        case '+': case '-': return 1;\n        case '*': case '/': return 2;\n        default: return 0;\n    }\n}\n\n// 另一条路：求值不走后缀栈，改用**递归下降**直接按优先级算。\n// 后缀串仍然用调度场单独生成——两条腿互不依赖。\nstruct Parser {\n    const string& s;\n    size_t i = 0;\n    explicit Parser(const string& t) : s(t) {}\n\n    long long expr() {\n        long long v = term();\n        while (i < s.size() && (s[i] == '+' || s[i] == '-')) {\n            char op = s[i++];\n            long long r = term();\n            v = (op == '+') ? v + r : v - r;\n        }\n        return v;\n    }\n    long long term() {\n        long long v = factor();\n        while (i < s.size() && (s[i] == '*' || s[i] == '/')) {\n            char op = s[i++];\n            long long r = factor();\n            v = (op == '*') ? v * r : v / r;\n        }\n        return v;\n    }\n    long long factor() {\n        if (s[i] == '(') {\n            i++;\n            long long v = expr();\n            i++;                     // 跳过 ')'\n            return v;\n        }\n        char c = s[i++];\n        if (c >= '0' && c <= '9') return c - '0';\n        return c - 'a' + 1;\n    }\n};\n\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n\n    string s;\n    getline(cin, s);\n    while (!s.empty() && (s.back() == '\\r' || s.back() == '\\n')) s.pop_back();\n\n    string out;\n    vector<char> st;\n    for (char ch : s) {\n        if (isalnum((unsigned char)ch)) {\n            out += ch;\n        } else if (ch == '(') {\n            st.push_back(ch);\n        } else if (ch == ')') {\n            while (!st.empty() && st.back() != '(') { out += st.back(); st.pop_back(); }\n            if (!st.empty()) st.pop_back();\n        } else {\n            while (!st.empty() && prec(st.back()) >= prec(ch)) { out += st.back(); st.pop_back(); }\n            st.push_back(ch);\n        }\n    }\n    while (!st.empty()) { out += st.back(); st.pop_back(); }\n\n    Parser p(s);\n    long long val = p.expr();\n    cout << out << '\\n' << val << '\\n';\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3+4*2\n",
                "expected_stdout": "342*+\n11\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "(3+4)*2\n",
                "expected_stdout": "34+2*\n14\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "8/3\n",
                "expected_stdout": "83/\n2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "a+b*c-d/e\n",
                "expected_stdout": "abc*+de/-\n7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "((1+2)*(3+4))\n",
                "expected_stdout": "12+34+*\n21\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1+2*3-4/2\n",
                "expected_stdout": "123*+42/-\n5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2*(3+4*5)/7\n",
                "expected_stdout": "2345*+*7/\n6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "由先序中序建树并输出后序",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 12,
        "tags": [
            "编程精练",
            "二叉树",
            "遍历",
            "递归"
        ],
        "statement_md": "给定一棵二叉树的**先序**序列与**中序**序列（结点值互不相同），输出两行：\n1. **后序**遍历序列\n2. 树的**高度**（空树为 0，单结点为 1）\n\n★ 为什么这两组序列能唯一确定一棵树：**先序的第一个一定是根**；拿着这个根去中序里一找，左边那段就是左子树的中序、右边那段是右子树的中序，而它们的元素个数又反过来把先序切成了两段。于是递归成立。\n\n★ 想清楚三件事，这题就不会写错：\n- 根在哪：`pre[pl]`\n- 左子树有几个结点：`k - il`（`k` 是根在中序里的位置）\n- 左子树的先序区间：`[pl+1, pl+left_n]`，右子树是 `[pl+left_n+1, pr]`\n\n⚠️ 只给「先序 + 后序」是**不能**唯一建树的——那时左/右子树分不清，必须配中序（或「同时给出空指针位置的扩展先序」）。",
        "input_format": "第一行 `n`；第二行 `n` 个整数（先序）；第三行 `n` 个整数（中序）。",
        "output_format": "两行：后序序列（空格分隔）；树高。",
        "constraints_md": "- 1 ≤ n ≤ 2000\n- 结点值互不相同",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "编程精练 · C/C++",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <vector>\n#include <unordered_map>\nusing namespace std;\n\nint n;\nvector<int> pre, ino, post;\nunordered_map<int, int> pos;\n\nint walk(int pl, int pr, int il, int ir) {\n    if (pl > pr) return 0;\n    int root = pre[pl];\n    int k = pos[root];\n    int leftN = k - il;\n    int hl = walk(pl + 1, pl + leftN, il, k - 1);\n    int hr = walk(pl + leftN + 1, pr, k + 1, ir);\n    post.push_back(root);\n    return (hl > hr ? hl : hr) + 1;\n}\n\nint main() {\n    if (scanf(\"%d\", &n) != 1) return 0;\n    pre.resize(n);\n    ino.resize(n);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &pre[i]);\n    for (int i = 0; i < n; i++) {\n        scanf(\"%d\", &ino[i]);\n        pos[ino[i]] = i;\n    }\n\n    post.reserve(n);\n    int h = walk(0, n - 1, 0, n - 1);\n\n    for (int i = 0; i < n; i++) {\n        printf(\"%d\", post[i]);\n        putchar(i + 1 == n ? '\\n' : ' ');\n    }\n    printf(\"%d\\n\", h);\n    return 0;\n}\n",
        "alt_solution": "#include <bits/stdc++.h>\nusing namespace std;\n\n// 另一条路：**不建树**，直接用区间递归把后序压进结果里，\n// 高度也在同一趟递归里返回。\nstruct Solver {\n    vector<int> pre, ino;\n    vector<int> post;\n\n    int rec(int pl, int pr, int il, int ir) {\n        if (pl > pr) return 0;\n        int root = pre[pl];\n        int k = il;\n        while (ino[k] != root) k++;      // 线性找根，不用哈希表\n        int leftN = k - il;\n        int hl = rec(pl + 1, pl + leftN, il, k - 1);\n        int hr = rec(pl + leftN + 1, pr, k + 1, ir);\n        post.push_back(root);\n        return max(hl, hr) + 1;\n    }\n};\n\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    int n;\n    if (!(cin >> n)) return 0;\n    Solver s;\n    s.pre.resize(n);\n    s.ino.resize(n);\n    for (int i = 0; i < n; i++) cin >> s.pre[i];\n    for (int i = 0; i < n; i++) cin >> s.ino[i];\n    int h = s.rec(0, n - 1, 0, n - 1);\n    for (int i = 0; i < n; i++) {\n        if (i) cout << ' ';\n        cout << s.post[i];\n    }\n    cout << '\\n' << h << '\\n';\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "6\n1 2 4 5 3 6\n4 2 5 1 6 3\n",
                "expected_stdout": "4 5 2 6 3 1\n3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n1\n1\n",
                "expected_stdout": "1\n1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n1 2 3\n3 2 1\n",
                "expected_stdout": "3 2 1\n3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n3 9 20 15 7\n9 3 15 20 7\n",
                "expected_stdout": "9 15 7 20 3\n3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "400\n4 199 101 107 9 108 42 284 111 269 86 105 15 77 75 97 89 351 279 67 175 1 110 25 125 216 233 384 395 400 237 301 213 76 73 37 18 274 299 78 23 54 228 317 371 220 286 303 106 360 122 391 363 281 82 178 380 321 242 121 289 276 177 315 14 382 365 196 124 293 192 302 350 251 81 397 132 154 44 84 322 176 244 370 379 22 234 343 357 46 205 12 191 222 165 245 367 62 342 201 72 323 260 155 179 268 16 120 34 24 306 126 235 340 258 223 10 270 17 386 39 355 55 280 63 102 325 341 329 200 112 60 152 305 118 80 392 204 241 48 190 292 71 33 53 188 345 116 138 263 113 309 87 291 290 221 338 239 230 254 202 160 59 304 376 217 326 297 358 257 195 394 388 19 99 300 319 65 187 114 70 227 92 214 273 272 183 312 141 368 362 162 232 27 354 167 49 56 320 366 95 103 8 146 115 135 61 43 374 364 314 11 186 104 109 210 198 219 185 45 193 252 331 119 288 236 117 83 211 328 243 335 283 287 346 69 307 266 396 90 96 13 264 169 275 172 157 3 277 148 151 372 240 7 123 147 30 145 311 131 74 94 57 313 170 344 253 212 387 20 180 285 208 347 150 250 166 261 158 262 159 35 137 144 127 140 369 168 218 66 373 194 295 398 133 361 64 334 47 139 324 209 256 282 153 378 229 389 294 327 40 32 93 130 182 85 337 333 375 2 28 248 224 308 29 318 156 31 356 298 339 246 203 58 383 143 231 189 225 399 164 50 149 161 173 330 271 207 381 352 171 226 129 377 310 238 36 79 21 181 348 142 38 134 174 385 5 332 197 184 163 336 52 390 51 316 206 6 100 41 278 98 265 128 349 267 393 136 359 88 259 247 26 249 353 68 296 215 255 91\n284 111 42 108 105 86 269 15 9 97 89 75 77 67 279 351 1 175 25 110 107 395 384 233 237 301 400 216 73 76 213 125 299 274 78 18 37 317 228 371 54 286 220 23 106 303 360 101 82 178 281 380 363 242 289 121 321 315 177 276 391 196 365 124 382 293 302 192 14 81 251 350 132 397 44 154 84 122 370 379 244 234 22 176 357 205 46 343 191 12 322 367 62 245 342 165 323 72 201 260 155 222 120 16 268 179 24 34 199 10 223 270 258 17 340 39 355 386 280 55 235 341 329 325 200 112 102 152 305 118 60 80 392 63 204 241 126 71 292 33 188 53 345 190 263 113 138 116 291 87 290 309 338 239 221 230 48 59 160 304 202 376 254 297 326 358 257 217 394 195 388 19 306 114 187 65 319 92 227 214 70 273 300 141 312 183 362 368 272 354 27 232 167 162 56 49 320 99 8 103 115 146 61 135 95 43 374 366 11 314 186 364 109 198 210 104 219 185 4 236 288 119 211 83 117 331 335 243 287 283 328 307 69 346 252 96 264 13 90 169 396 157 3 172 148 277 275 151 266 240 7 372 145 30 147 123 131 311 193 170 313 57 253 344 94 20 387 180 208 285 347 212 250 261 166 158 150 159 262 35 144 137 74 218 168 369 66 140 295 194 398 373 133 127 334 64 47 361 324 139 45 294 389 327 229 32 40 378 93 130 153 337 85 182 375 333 28 2 282 29 308 224 156 318 248 356 298 31 246 339 203 256 231 143 383 189 58 164 50 399 161 149 225 330 173 271 209 129 377 226 171 310 238 79 36 352 181 21 142 38 348 381 385 174 197 332 5 184 134 163 336 52 207 6 206 316 100 51 278 265 98 41 128 349 390 88 359 136 393 247 259 26 267 68 353 249 255 215 91 296\n",
                "expected_stdout": "111 284 42 105 86 15 269 108 89 97 75 67 279 1 25 110 175 351 77 9 395 384 301 237 400 233 73 76 213 216 299 78 274 18 317 371 228 286 220 54 106 360 303 23 37 125 107 178 82 380 281 289 121 242 315 177 276 321 363 196 124 365 302 192 293 382 81 251 132 44 84 154 397 350 14 391 379 370 234 22 244 205 46 357 191 12 343 176 62 367 342 245 323 72 155 260 201 165 120 16 268 24 34 179 222 322 122 101 10 270 223 17 258 355 39 280 55 386 340 329 341 112 200 325 118 305 152 392 80 60 102 241 204 63 235 71 188 345 53 33 292 113 263 138 291 290 87 239 338 230 221 309 116 190 59 304 160 376 202 297 257 358 326 394 19 388 195 217 254 48 126 114 187 65 92 214 227 273 70 319 141 312 362 368 183 354 27 167 232 56 320 49 162 272 300 8 115 61 135 146 103 374 43 95 11 186 314 198 210 109 185 219 104 364 366 99 306 199 236 288 211 83 117 119 335 287 283 243 307 69 346 328 331 264 13 96 169 90 3 157 148 277 172 151 275 396 7 240 145 30 147 131 311 123 372 266 252 170 313 253 344 57 20 208 347 285 180 387 261 158 166 250 159 144 137 35 262 150 212 94 218 168 66 369 295 398 194 133 373 140 334 47 64 324 139 361 127 74 193 294 327 389 32 40 229 130 93 378 337 85 375 28 2 333 182 153 29 308 156 318 224 298 356 246 203 339 31 248 282 231 143 189 383 50 164 161 149 399 330 271 173 225 58 256 377 129 226 79 36 238 310 171 181 38 142 348 21 352 385 197 332 184 5 174 52 336 163 134 381 6 206 100 316 265 98 278 349 128 41 51 88 359 136 247 26 259 393 68 353 255 91 215 296 249 267 390 207 209 45 4\n11\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "哈夫曼编码的总长度",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 14,
        "tags": [
            "编程精练",
            "哈夫曼树",
            "贪心",
            "堆"
        ],
        "statement_md": "给定 `n` 个字符的权值（出现频次），按哈夫曼算法构造最优二叉树，输出**带权路径长度 WPL**（`Σ 权值 × 编码长度`）。\n\n算法只有一句话：**每次取出权值最小的两个结点合并，新结点权值 = 两者之和，把新结点放回集合**，重复 `n-1` 次。\n\n★ 一个省事的恒等式：**WPL 恰好等于每次合并产生的新权值之和**。所以根本不用真的建树，边合并边累加就行。\n\n★ 为什么贪心是对的：权值最小的两个字符必须放在**最深**的位置（它们的贡献被乘的次数最多、但基数最小，这样换出来最划算）。合并之后，这个「两兄弟」在后续计算里就等价于一个权值为和的新字符——于是子问题结构完全一样。\n\n⚠️ 别把它和「构建哈夫曼编码串」混了：**WPL 唯一，但树的形态和每个字符的码长不唯一**（权值相同的结点谁当左谁当右都行）。这也是本题只验 WPL、不验具体编码的原因。\n\n⚠️ `n` 到 10⁵ 时，`WPL` 可能达到 10¹⁴ 量级，**必须用 64 位整数**。",
        "input_format": "第一行 `n`；第二行 `n` 个权值（保证互不相同）。",
        "output_format": "一行：WPL。",
        "constraints_md": "- 2 ≤ n ≤ 10⁵（n = 1 时 WPL 记为 0）\n- 1 ≤ wᵢ ≤ 10⁹\n- WPL 可能超过 32 位",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "编程精练 · C/C++",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <queue>\n#include <vector>\nusing namespace std;\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n\n    priority_queue<long long, vector<long long>, greater<long long>> pq;\n    for (int i = 0; i < n; i++) {\n        long long w;\n        scanf(\"%lld\", &w);\n        pq.push(w);\n    }\n    if (n == 1) {\n        printf(\"0\\n\");\n        return 0;\n    }\n\n    long long wpl = 0;\n    while (pq.size() > 1) {\n        long long a = pq.top(); pq.pop();\n        long long b = pq.top(); pq.pop();\n        long long s = a + b;\n        wpl += s;\n        pq.push(s);\n    }\n    printf(\"%lld\\n\", wpl);\n    return 0;\n}\n",
        "alt_solution": "#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n\n    int n;\n    if (!(cin >> n)) return 0;\n    vector<long long> a(n);\n    for (int i = 0; i < n; i++) cin >> a[i];\n\n    if (n == 1) {\n        cout << 0 << '\\n';\n        return 0;\n    }\n\n    // 另一条路：不用堆，每轮线性扫出两个最小值并「标记为已用」。\n    // O(n^2)，n 小的用例够用；结果与堆版本必须一致。\n    sort(a.begin(), a.end());\n    vector<long long> cur = a;\n    long long wpl = 0;\n    int m = n;\n    while (m > 1) {\n        // cur 保持有序（插入时用 lower_bound 维护），取前两个即可\n        long long x = cur[0], y = cur[1];\n        long long s = x + y;\n        wpl += s;\n        cur.erase(cur.begin(), cur.begin() + 2);\n        cur.insert(lower_bound(cur.begin(), cur.end(), s), s);\n        m--;\n    }\n    cout << wpl << '\\n';\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n1 2 3 4 5\n",
                "expected_stdout": "33\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n7 3\n",
                "expected_stdout": "10\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n9\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n10 20 30 40\n",
                "expected_stdout": "190\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n5 9 12 13 16 45\n",
                "expected_stdout": "224\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2000\n729875201 378613717 622004327 303820983 916849892 185272899 52093430 884344520 259395560 247440817 251856679 3141513 766289273 886373387 587112586 141379634 63448479 213515562 207664230 331286090 686262215 753822277 890963489 706159390 668953939 114459776 794759523 207699241 812256651 161371482 545567479 124360499 232471162 633765546 484243512 5469740 632343241 123390036 394663622 151324356 627958921 373344813 509998133 61258141 66162508 895201027 159274981 157776515 491153342 70070183 982981103 116213561 604411474 240549725 550868352 987962499 551525095 358429258 101962359 904355687 190789842 468947163 660651612 815858362 447113467 95459373 457682196 490553928 763310090 821736188 838065903 49189789 135512867 916589570 414444428 992053394 566849290 223329075 810254290 62127052 932998015 77524381 398216774 102973665 319470438 541903664 205756076 6189747 108187633 80686949 418404476 236189387 611147430 522383189 514880374 671967119 79912671 793771560 572294865 919075131 814915771 64090074 392598617 44323331 828139138 956287970 636860249 406611585 5727781 782167826 515684314 38912381 255458596 950226218 30614493 810106161 761451717 173487021 326985885 921175335 554642393 539425555 792692006 555175988 714477021 396979541 784946504 45467211 920419866 330872672 502703740 15715437 906699926 128883360 33551683 968654102 314279964 624483519 633693958 54223258 976813584 48150803 783952008 542113083 831900188 14998956 414713401 551826271 301542602 463552674 21477296 494050076 783058943 364393533 715362303 215915561 738649864 339581515 687944568 948337193 646966895 599469967 956931961 740073534 719987564 549301035 778549154 566855649 993904887 520677552 300679421 802591624 712999987 917333737 276724146 338871889 552512654 426424987 899057999 855487472 596025065 877985570 611440394 381460641 769180837 788883484 859217953 898738203 384014838 191262728 162096831 538126847 162907793 500184094 553190020 313435819 484692855 163363284 694711350 8924666 41068094 848699405 687052762 888562497 922800407 493862812 743205105 625976438 286663566 722867361 578078751 814281637 916240694 548928145 247026888 895935058 755412241 132341514 854177721 804796733 909811013 523580739 463736465 737326704 995104091 922071885 602887414 158629574 163513487 516747618 263829459 608495371 786078867 19090550 652589076 463453151 539307667 619788417 398938220 95896074 198438770 434177107 361631532 865964819 60582729 336225710 930053834 941469473 117064820 652098478 737100175 209894546 12573370 786502575 289737328 771994757 385104576 407394723 648120088 570574427 494368568 67289629 670893232 652191613 23177533 164459693 235686648 526654654 811102624 216766160 988476702 433102117 68959305 105673220 218996846 507888076 254901702 997630481 853854276 949000747 158511821 432296547 974652832 455306013 396931160 201163641 960774774 795299736 419018257 356691199 651502875 328173860 871371407 54973041 54103401 103676350 701852142 681616806 487210447 554848004 239419685 509459690 135361191 62600706 306520671 846842054 191806288 797525070 513758599 513129978 459402007 392745905 423972572 348133559 66129288 640494856 240236914 586149064 149672981 588309150 772814089 238455357 418335332 548559308 597666037 493718675 823227259 75055897 430338652 544571507 789824713 613453814 554441054 956163822 93945297 199103862 900792079 97903581 81674804 980468254 720810691 616781181 985327182 495926445 42292477 788527252 822739038 247835040 597417939 708862302 593508344 736032069 335210783 174163476 604856744 362542922 270092849 881879575 191914447 557643040 293731411 693041299 623049791 374988877 809275018 42758155 58881566 592139375 582690951 289798484 259200287 328326805 134866858 305757730 383918826 381442866 705429961 69634975 970695313 142422257 740231273 660863534 166559800 946119832 459403765 606029426 193522817 330768207 484433507 860798676 939523261 750291400 341519394 416688359 215663060 861325264 569718856 939482978 215400410 33783211 215044566 734027589 911699699 131310914 631798216 371102848 405761580 379225222 515876327 374379759 739216220 884561214 139586072 363151816 654766687 210032459 269462026 518461681 100175399 612346807 642195889 827545188 393318021 129425354 726058839 666463749 851937378 678558045 529240928 809324785 530015137 18012165 312983487 847621373 318690064 128969495 983665926 357623975 597545748 301759314 5043027 466513002 980772742 720579317 767929778 408929281 288915592 38077327 320449421 123237656 155590771 563762055 584764996 721236585 644719619 143413062 155443464 100681649 816125005 65484576 371561814 863182575 298456055 110378031 278432588 316923281 802345987 970854748 616693662 601349288 633099771 187936549 599275110 222551813 417754751 844181807 792819006 17231081 393948850 115277215 802183089 912707646 379852581 43688650 602334766 763914561 487785407 321500491 183683104 345665735 380278056 402112579 583999971 57580413 356682169 856997178 388535765 943470061 513587191 53823874 110180949 376116282 158344341 746260444 278335841 712464412 389374550 391881998 264781406 707543667 367759167 767013510 95252981 39639531 245835483 652064705 850003732 298057030 942612780 226241093 92650432 836952254 864729806 332688302 552037519 61353261 235750664 427732683 100222720 66347272 360345666 921840664 767316516 176016625 972556640 961797124 129255378 791569668 8191598 248351910 496946204 949244283 443140154 943011638 803679280 4448051 537329344 712606096 65021937 684108013 681867317 56562430 339242186 997254598 357922454 443512181 378927118 686274552 182007069 297916801 982942893 868353147 629215997 982630512 244085208 307298965 847377999 479738517 656061104 653917268 661720675 552545073 709453064 439756228 581821685 332584468 181280676 406151108 813340151 274873890 516081556 44444369 927091670 796531227 720669436 129916762 135003 834709520 922754798 901262136 169486796 73661516 982806486 780935974 347469402 971423910 925919709 824933242 921783872 242673900 128660534 58053843 959589012 46088760 505803210 25710215 333237208 784920808 309121198 26132256 612281398 757279124 213836085 870172640 398570170 282529170 95645535 913595285 672330528 874320666 743309011 779964808 186988270 632135372 837218614 494487285 153550786 833213977 486453496 191540907 404213517 342022330 774724201 997283232 792355882 146356601 123808496 197588213 980547040 610761845 80994654 165089258 676748997 233025544 843936317 62451335 424244003 41540811 329713396 943798066 179434425 724485222 170434083 180305844 51987687 885037846 93793214 944695948 265943750 391296998 924093815 517225680 98770748 35274612 168557060 229327097 428186625 285198981 653653046 659915426 421927253 202057142 252317196 597541499 998118363 984075594 228579809 604955987 559481608 148563457 200081397 308958111 729985323 10491873 56115183 780480570 948027647 459271801 797731864 833296827 287356917 916421560 148333223 487162993 886702046 216315013 674287678 340635648 302803286 361884711 167948775 549741852 63087285 583162547 972776995 96683810 566567872 413674518 279298068 215663938 567415184 622580994 688789807 536541571 491273221 783286880 135309633 946554905 676241928 676572187 516454814 147412296 324438487 155486721 963045678 523253183 99329694 862962976 757130058 813934566 347594065 515095360 991712745 390839107 789363751 437333683 340825955 370283401 708258534 675532232 249146139 928603289 363358211 96397403 237239543 604449518 590787074 241832991 652664797 204722650 453385161 415819659 562580 46214897 93974519 128560019 748587907 429097238 346659390 545419804 645486678 971189641 558611106 258654356 287474870 90599739 621412280 630114429 946345030 635972374 256076222 120157027 919841108 154461715 329992910 647434739 41930842 609924067 695689972 799782442 716152393 629274090 315048654 297612614 892578191 184401300 263581831 432936938 296775985 418604475 563493829 522647195 171734278 815897897 23191456 781230927 635512755 180753682 138695887 849701261 689117829 286871924 968992310 924297637 697265521 602120020 754307281 945182563 243961322 725205838 292332957 650684596 380906144 434583663 265346026 56774979 259562286 813118187 439649000 527046243 267064004 10984436 180505265 570169068 625366852 956927216 622771041 289621525 423995366 464919882 631557422 112578574 821668929 411131952 239991366 540276265 435944066 420874263 557675000 503306970 456180479 834051872 236997844 772486466 117810607 923692859 478430498 47444656 214716528 917494546 900819310 690238115 82734503 402062236 75975821 536642474 216646255 580793767 963917013 275126399 485383617 41308456 826895087 902019040 579762457 287434098 377384133 299833473 645166462 914931915 984793988 399126403 579106338 899193030 563228433 982733918 225395501 951765231 750759071 275156549 497863200 837523755 608555462 918562417 724715118 899242197 917262612 905202171 714599604 528029318 145068887 735139392 148312210 437954909 812081492 195535788 309377673 690464361 233062956 176936448 617777887 999196312 698143769 185548041 734968188 849962142 653015541 335488518 695235204 151511365 101231976 997581966 931322714 825631623 820647643 297657673 609645113 505547837 927827515 908673156 953533249 401798245 130559434 117712257 660158163 930642592 787339710 893099893 222612342 173286109 415652080 113644760 103287559 874781516 533753288 670112318 157656156 739381166 554638970 323213285 691007792 574023526 850532204 85990695 10790718 691036745 625219543 71179896 385129254 225907386 619381252 909826260 333829351 868139756 259291739 233380821 65197713 219016144 200709073 360321555 815791215 266032615 84719772 757747496 792001131 855679886 610232858 687285374 986788715 870318096 112158497 793809854 83348384 954607310 310919790 316725720 919961420 93145147 616364270 903978999 712193919 212121957 913498354 77481676 619660563 91861705 971719354 415699669 990835828 114991795 284134002 98828979 330368557 877732990 618515957 48449236 922456565 208283455 40651448 991498932 786701180 274641899 767753088 487473253 62882577 46501612 517838194 137361707 805881141 835004111 291436415 748531946 868790760 294927080 632305625 503475475 71154201 243371111 747212455 23025333 483503965 496788095 782453626 475313674 978376090 950390484 405204803 129880901 289160973 840559776 280984382 432791179 23703429 932095720 158164021 251253557 278685773 947672100 848911598 487842194 321905751 87648825 239270965 207808965 373546768 267394433 189316797 88435695 928990980 623026885 867970954 925555557 36560473 376637159 313000611 412571378 890932691 449269316 883539824 885299529 751149042 240722573 857591627 253529503 593025061 773797161 29335718 953479766 45381925 528663890 942996270 511118767 257534976 259513773 873649593 633950193 311155472 835988104 670059973 781237582 782424792 254086730 932034846 207781967 194955004 919087709 205198522 826716083 218169828 670353110 145199196 142870841 184020410 801288209 530057780 904130071 800311665 790232754 522332541 177727347 37494862 620960343 436427076 920393081 145922825 104998995 547665628 422516056 2071350 363161235 254375228 210995880 530609438 271322437 60761655 571680207 696601740 789073523 683700832 494712762 134525948 19067950 94212865 576437250 535629932 781483267 43317194 307574052 688321372 37920747 93261747 203545237 897388383 92490443 623171928 971427320 919004005 291723361 159488839 431474029 824622322 814014740 610284959 63727849 917443200 631156372 667485143 964383381 948465838 604890175 93507759 867115608 78143093 831746517 679990093 882460042 365683379 195148839 932681619 66959277 2490213 856793860 499427500 888315702 67321287 479728929 440965744 168475867 489994335 290639388 36292350 438060936 336810093 185918170 158751122 623297276 631739189 288839896 761520245 246679000 486383906 299978316 181243834 262756513 332474685 512655189 153594080 642574255 892623358 26349455 184987415 388487769 221125094 12526609 927507376 794879756 775083826 186404536 113488926 665656739 68687275 37618321 143101204 946465081 263269964 931166551 402879943 711431900 801934469 842638047 154215798 220325137 479008692 4924133 51507747 894847724 643357017 844126530 665195326 380419263 871490581 531581389 883943622 546211028 742778119 342263374 985078488 92353418 236521243 832147230 292274487 200991924 144574255 614224470 638149511 511076079 988236352 927582155 512723774 310835164 756725010 24023337 152199184 125946784 183755780 655620519 44453196 937005255 70462944 278527615 796449508 13917321 781824108 683335899 887473865 165859666 725662053 758745789 187091760 82436649 282955158 746614677 678844418 915799894 872403120 521424902 81136224 462187505 929026740 245330371 698952188 11434614 609201429 739735456 960418735 885736233 441389985 955027930 706939602 228469229 608066468 160309911 749038232 236036320 727379082 278463743 543272414 515446929 156626273 425433694 749867848 262282816 158963638 180232262 701964521 971333291 817248561 428633505 786864933 24495389 493859317 418550158 770023660 83173686 22692635 556998346 751701972 462328696 276744275 203955064 476497720 337543726 722670434 147171377 965303651 184806368 27383665 109070106 708139673 2902745 409692919 841085892 825275325 986975521 812007512 713302523 556965163 409268918 729642480 533323680 955744711 907703079 987905457 68926036 923950828 384630923 892038167 914852077 955010046 995325875 864455466 566691132 986879801 869559319 365885696 110963343 413791378 544717805 183986520 8202750 588280627 433486936 161856641 103017909 785871227 654538695 662046224 514005443 40488788 731300707 747753564 6663585 695419356 857824899 209280086 561332611 805629788 658711653 58462873 273300060 747599040 637580007 408523685 286307432 634697373 879523786 467054911 951026959 149746541 707545386 515014638 816633518 438849959 380958113 455821807 91965634 103534209 639482726 156813135 364970647 795727190 667633713 624221384 516190225 806238025 486022367 69300420 216352948 404338792 381038338 772421137 272743900 450870805 779288191 848520279 254077642 463933785 633866641 158041623 787527946 513495410 117321468 739684386 639313374 256492181 639334970 525008897 486073735 78573705 665416805 799999504 275337317 521150861 44072370 745381631 467073597 475563230 640481013 582418133 582677860 963207124 958548420 414365129 484108902 260770890 352286185 12170330 199993618 585168231 940248599 830368430 708723183 128400329 66039766 519920609 204891201 478614098 354328362 236552118 992215522 825797804 895135634 506253986 410438895 239779607 278008342 643121146 413650632 889081896 872902129 555675693 866551378 994329919 863405328 149622192 296770810 1493883 832468450 699623269 599454604 636473853 781974624 565832248 876055731 813993173 576035074 683776482 71194491 243539793 658605083 949251694 697151164 701343714 995800336 334165135 29514928 107888361 772991511 859397827 636167633 719327206 703731747 593896995 381839095 378661568 956914669 380483861 707736428 648122901 642025469 418561816 456040587 711010386 715196931 218432013 967159257 433098814 265274998 547776644 427176515 713404851 590437859 879569398 541851855 952205606 756878776 456221206 922806630 81183957 185586595 68544140 91049168 905493737 147952286 469151275 134723426 762532483 542414778 508398522 218102496 736656962 87921184 269735531 297908135 227445943 299222451 643106971 961894216 216421150 789467698 18254626 607487486 696104742 818425198 828414697 338531428 189325239 707853770 936364229 211029188 428410074 913586751 162695466 531156255 837392229 863373392 743775737 685378150 354904504 250058449 463511055 212100768 703739734 850528747 599591065 134608097 509800898 267151439 154795882 569242672 951688498 204955640 81486560 641739646 506463006 901526854 773731639 210901538 789613999 363892259 588951364 494823044 598863255 57396531 550190974 172409158 832430453 112944724 273167323 709338181 436755539 916067 300651878 26684994 776589110 651373502 34939612 985681374 921821557 87442150 943957949 774757750 832985354 103020370 142729328 15499836 707400882 758868741 147172539 619400686 913160015 23719827 153232414 867756419 452021905 528283381 661476981 763951922 530776192 64783358 357234623 987377308 933115990 601257780 570878487 634526768 914560284 569790878 131860634 165278527 975569901 493494450 255251896 108703101 944990731 537543416 722309701 749942664 667265674 22114386 48502217 600007269 719252229 708215808 708983810 194425057 55527140 736496133 153440173 202728333 957358910 813024201 735340881 361299119 256906983 683382515 261711211 56927400 739239464 505368375 44897199 463848643 957394692 479497322 231672823 819023759 761393187 179118009 181543297 901241327 834859296 741547148 60142005 506033762 841300802 185509076 551925091 624696061 285404417 314619371 212378991 247497604 279378810 190526930 232455452 922921993 508028188 801061983 704539489 790330587 583792443 359261113 929364984 749952300 500776088 196203696 58109708 953625856 539473445 43017811 332338401 215728410 374266227 51739649 80984530 356216283 259414054 481089971 207951559 200024431 667383017 3895175 931650825 263702453 965328622 338374319 233488417 904817861 873668834 183414357 881147580 88056938 521492830 161011723 947235083 734020272 661577427 888347150 339937942 875615205 934994342 978252722 748756744 395760059 257849454 144533934 302044060 496168334 812443560 770904032 775376397 559796854 903192652 866575753 445251593 63192580 219833737 937751930 320194356 609944566 725130577 180866208 844485647 805678803 362373598 352442327 211420962 609218691 307715460 646190209 239472329 52897735 355722836 54189852 801080079 276859323 407258927 827052585 667980016 671260108 526262046 545613021 443791645 181901022 576823524 400795397 866510266 448137745 471622230 627160161 270458699 753374592 482021311 518959861 221739038 850865575 804786336 172629359 461457185 180485154 856981420 699271258 34652614 371621848 480229189 321382646 347873091 108936023 920791462 722266597 772827637 692353434 481091261 382887857 117031512 857266815 528478694 764736058 711999654 90808684 761313350 406959204 512642003 892950506 441252206 220999345 814004489 591563847 139104364 393686975 666146573 315860464 59837928 746152850 273094383 991703946 398270163 336069951 407338389 361006705 443776713 162171963 344296547 755965430 677240820 398715243 143727541 798383267 784285482 293995997 217029869 331099612 198628663 909582926 805584622 167432621 221942553 911543927 651893527 333646799 766025031 552985946 212550169 495282377 513916294 59303816 960072502 234841746 572633018 501540045 971880290 512150311 404039800 205282923 459672438 511195211 356337208 424117436 158422890 293199782 835107359 566802579 44135380 91143004 433431847 838798948 82765970 3368553 243809466 461173588 683799886 350335824 643382597 990997217 761430876 513902721 669489474 335013795 232623798 140861488 56997435 797066456 140553052 517275363 25330501 957143790 444825849 678694971 57258095 368346395 134484847 225635711 156229008 28732563 36962998 185420089 201399965 671667249 449088581 685867575 760461484 701085147 549270238 136791358 186042978 161942447 753341267 724869441 380733519 687188309 512384288 65983439 778409835 591684678 225498005 784091347 630572503 423534950 679995246 159321957 243785958 133690820 77785927 526136917 242149304 422884369 348119039 900722611 913903817 460201027 635165781 252334556 196560462 781235942 37949868 257416167 560024133 977580442 569761807 687923408 507429110 977919938 922903726 40819932 96988770 947411136 806882043 307850389 437221524 551920460 794113991 656601478 101770869 403169626 234449962 907173051 81678965 565296223 448299180 139158118 984224585 798552647 217525579 451794963 985546622 97554399 316895087 740814677 948855817 380689799 993812597 118556093 262807384 498499411 546728491 585076097 893712796 307726781 537783860 858560049 384551759 104506976 932206605 121244602 961648984 161287576 584946503 915194714 79634856 257524557\n",
                "expected_stdout": "10583153992785\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "图的广度优先与深度优先遍历",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 12,
        "tags": [
            "编程精练",
            "图",
            "BFS",
            "DFS",
            "邻接表"
        ],
        "statement_md": "给定 `n` 个点、`m` 条**无向**边和起点 `s`，输出两行：\n1. 从 `s` 出发的 **BFS** 序列\n2. 从 `s` 出发的 **DFS** 序列\n\n规定：**访问某个点时，按邻接点编号从小到大处理**。只遍历 `s` 所在的连通分量。\n\n★ BFS 用队列：出队一个就把它所有未访问的邻居**一次性全部入队**并立刻标记访问。「入队时就标记」是关键——不然同一个点可能被相邻的多个点重复塞进队列。\n\n★ DFS 用递归（或显式栈）。**如果用栈做迭代版，要注意压栈顺序要反过来**：想按编号升序访问，就得**降序压栈**（栈是后进先出）。顺序压栈会得到「降序访问」的结果，与递归版对不上。\n\n★ 无向边要**双向加**。只加 `u→v` 是这道题最隐蔽的错——图看起来能跑，但序列会缺一大截。",
        "input_format": "第一行 `n m s`；接着 `m` 行 `u v`（无向边）。",
        "output_format": "两行：BFS 序列；DFS 序列。",
        "constraints_md": "- 1 ≤ n ≤ 10⁵，0 ≤ m ≤ 2×10⁵\n- 1 ≤ s ≤ n",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "编程精练 · C/C++",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <vector>\n#include <queue>\n#include <algorithm>\nusing namespace std;\n\nint n, m, s;\nvector<vector<int>> adj;\nvector<char> vis;\nvector<int> dfsOrder;\n\nvoid dfs(int u) {\n    vis[u] = 1;\n    dfsOrder.push_back(u);\n    for (int v : adj[u]) {\n        if (!vis[v]) dfs(v);\n    }\n}\n\nint main() {\n    if (scanf(\"%d %d %d\", &n, &m, &s) != 3) return 0;\n    adj.assign(n + 1, {});\n    for (int i = 0; i < m; i++) {\n        int u, v;\n        scanf(\"%d %d\", &u, &v);\n        adj[u].push_back(v);\n        adj[v].push_back(u);\n    }\n    for (int i = 1; i <= n; i++) sort(adj[i].begin(), adj[i].end());\n\n    vis.assign(n + 1, 0);\n    vector<int> bfsOrder;\n    queue<int> q;\n    q.push(s);\n    vis[s] = 1;\n    while (!q.empty()) {\n        int u = q.front(); q.pop();\n        bfsOrder.push_back(u);\n        for (int v : adj[u]) {\n            if (!vis[v]) {\n                vis[v] = 1;\n                q.push(v);\n            }\n        }\n    }\n\n    vis.assign(n + 1, 0);\n    dfsOrder.clear();\n    dfs(s);\n\n    for (size_t i = 0; i < bfsOrder.size(); i++) {\n        if (i) putchar(' ');\n        printf(\"%d\", bfsOrder[i]);\n    }\n    putchar('\\n');\n    for (size_t i = 0; i < dfsOrder.size(); i++) {\n        if (i) putchar(' ');\n        printf(\"%d\", dfsOrder[i]);\n    }\n    putchar('\\n');\n    return 0;\n}\n",
        "alt_solution": "#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n\n    int n, m, s;\n    if (!(cin >> n >> m >> s)) return 0;\n\n    // 另一条路：邻接矩阵 + 迭代 DFS（显式栈）。\n    // n 小时矩阵更直观；DFS 想按升序访问就必须**逆序压栈**。\n    vector<vector<char>> g(n + 1, vector<char>(n + 1, 0));\n    for (int i = 0; i < m; i++) {\n        int u, v;\n        cin >> u >> v;\n        g[u][v] = g[v][u] = 1;\n    }\n\n    vector<char> vis(n + 1, 0);\n    vector<int> bfs;\n    queue<int> q;\n    q.push(s);\n    vis[s] = 1;\n    while (!q.empty()) {\n        int u = q.front(); q.pop();\n        bfs.push_back(u);\n        for (int v = 1; v <= n; v++) {\n            if (g[u][v] && !vis[v]) {\n                vis[v] = 1;\n                q.push(v);\n            }\n        }\n    }\n\n    fill(vis.begin(), vis.end(), 0);\n    vector<int> dfs;\n    vector<int> st;\n    st.push_back(s);\n    while (!st.empty()) {\n        int u = st.back();\n        st.pop_back();\n        if (vis[u]) continue;\n        vis[u] = 1;\n        dfs.push_back(u);\n        for (int v = n; v >= 1; v--) {       // 逆序压栈 → 升序出栈\n            if (g[u][v] && !vis[v]) st.push_back(v);\n        }\n    }\n\n    for (size_t i = 0; i < bfs.size(); i++) { if (i) cout << ' '; cout << bfs[i]; }\n    cout << '\\n';\n    for (size_t i = 0; i < dfs.size(); i++) { if (i) cout << ' '; cout << dfs[i]; }\n    cout << '\\n';\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 4 1\n1 2\n1 3\n2 4\n3 5\n",
                "expected_stdout": "1 2 3 4 5\n1 2 4 3 5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 0 1\n",
                "expected_stdout": "1\n1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "6 6 2\n1 2\n2 3\n3 4\n4 5\n5 6\n6 2\n",
                "expected_stdout": "2 1 3 6 4 5\n2 1 3 4 5 6\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4 4 3\n1 2\n2 3\n3 4\n4 1\n",
                "expected_stdout": "3 2 4 1\n3 2 1 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "60 150 1\n1 54\n2 15\n2 19\n2 23\n2 24\n2 26\n2 30\n2 37\n2 50\n3 8\n3 18\n3 22\n3 37\n3 41\n3 42\n3 47\n3 53\n3 59\n4 17\n4 19\n4 38\n4 42\n4 53\n5 8\n5 15\n5 27\n5 30\n5 54\n6 25\n6 38\n6 44\n6 46\n7 50\n7 55\n7 60\n8 12\n8 13\n8 37\n8 39\n9 42\n10 13\n10 25\n10 30\n10 42\n10 45\n10 47\n11 21\n11 23\n11 24\n11 37\n11 41\n11 46\n12 18\n12 36\n12 51\n12 55\n13 15\n13 20\n13 48\n13 49\n13 50\n14 33\n14 48\n14 51\n15 23\n15 24\n15 37\n16 21\n16 37\n16 38\n16 42\n16 52\n17 18\n17 27\n17 29\n17 30\n17 37\n17 43\n17 52\n18 20\n18 21\n18 46\n18 50\n18 53\n19 38\n19 40\n19 48\n19 51\n20 23\n20 24\n20 55\n21 30\n21 42\n21 50\n21 57\n21 59\n22 50\n22 57\n23 35\n23 56\n24 34\n24 38\n24 40\n24 46\n24 54\n25 33\n26 29\n26 32\n26 56\n26 60\n27 31\n27 44\n27 58\n28 34\n29 47\n29 57\n30 31\n31 36\n32 51\n33 37\n33 42\n33 45\n33 52\n34 41\n34 48\n35 54\n36 41\n36 55\n37 55\n37 59\n38 43\n39 46\n39 52\n39 53\n39 54\n39 60\n40 51\n41 45\n42 51\n44 49\n45 53\n46 49\n46 51\n46 55\n46 56\n50 54\n51 53\n53 59\n56 57\n56 60\n",
                "expected_stdout": "1 54 5 24 35 39 50 8 15 27 30 2 11 20 34 38 40 46 23 52 53 60 7 13 18 21 22 3 12 37 17 31 44 58 10 19 26 41 55 28 48 4 6 16 43 51 49 56 33 45 59 42 57 47 36 29 25 32 14 9\n1 54 5 8 3 18 12 36 31 27 17 4 19 2 15 13 10 25 6 38 16 21 11 23 20 24 34 28 41 45 33 14 48 51 32 26 29 47 57 22 50 7 55 37 59 53 39 46 49 44 56 60 52 40 42 9 35 30 43 58\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "拓扑排序的最小字典序",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 12,
        "tags": [
            "编程精练",
            "图",
            "拓扑排序",
            "Kahn",
            "堆"
        ],
        "statement_md": "给定 `n` 个点和 `m` 条**有向**边（可能有重边），输出**字典序最小**的拓扑序；若图中有环，输出 `CYCLE`。\n\n★ 普通 Kahn 用队列就够了，但要**字典序最小**，就得把队列换成**小根堆**：「当前所有入度为 0 的点」里永远优先取编号最小的那个。\n\n★ 为什么这样贪心是对的：入度为 0 的点之间**没有任何先后约束**，谁先走都不影响可行性；既然可以随便选，那当然选最小的。选完它只可能让更多点入度归零，不会把局面弄坏——这是标准的「交换论证」。\n\n⚠️ 重边会让入度算多。如果没去重，删边时减两次、入度归零的时机就错了（本题的数据可能含重边，注意按边的条数老老实实加减，别自作聪明去重）。\n\n⚠️ 判环：如果最后输出的点数 `< n`，说明剩下的点互相卡住了 → 有环。",
        "input_format": "第一行 `n m`；接着 `m` 行 `u v`（有向边 u→v）。",
        "output_format": "一行：字典序最小的拓扑序；有环输出 `CYCLE`。",
        "constraints_md": "- 1 ≤ n ≤ 10⁵，0 ≤ m ≤ 2×10⁵\n- 可能有重边",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "编程精练 · C/C++",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <vector>\n#include <queue>\n#include <functional>\nusing namespace std;\n\nint main() {\n    int n, m;\n    if (scanf(\"%d %d\", &n, &m) != 2) return 0;\n\n    vector<vector<int>> adj(n + 1);\n    vector<int> indeg(n + 1, 0);\n    for (int i = 0; i < m; i++) {\n        int u, v;\n        scanf(\"%d %d\", &u, &v);\n        adj[u].push_back(v);\n        indeg[v]++;\n    }\n\n    priority_queue<int, vector<int>, greater<int>> pq;\n    for (int i = 1; i <= n; i++) {\n        if (indeg[i] == 0) pq.push(i);\n    }\n\n    vector<int> order;\n    order.reserve(n);\n    while (!pq.empty()) {\n        int u = pq.top();\n        pq.pop();\n        order.push_back(u);\n        for (int v : adj[u]) {\n            if (--indeg[v] == 0) pq.push(v);\n        }\n    }\n\n    if ((int)order.size() != n) {\n        printf(\"CYCLE\\n\");\n        return 0;\n    }\n    for (int i = 0; i < n; i++) {\n        printf(\"%d\", order[i]);\n        putchar(i + 1 == n ? '\\n' : ' ');\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n\n    int n, m;\n    if (!(cin >> n >> m)) return 0;\n    vector<vector<int>> adj(n + 1);\n    vector<int> indeg(n + 1, 0);\n    for (int i = 0; i < m; i++) {\n        int u, v;\n        cin >> u >> v;\n        adj[u].push_back(v);\n        indeg[v]++;\n    }\n\n    // 另一条路：不用堆，每轮线性扫一遍找「入度为 0 的最小未用点」。\n    // O(n^2)，n 大的用例会慢，但逻辑与堆版本等价。\n    vector<char> used(n + 1, 0);\n    vector<int> order;\n    order.reserve(n);\n    for (int step = 0; step < n; step++) {\n        int pick = 0;\n        for (int i = 1; i <= n; i++) {\n            if (!used[i] && indeg[i] == 0) { pick = i; break; }\n        }\n        if (pick == 0) break;\n        used[pick] = 1;\n        order.push_back(pick);\n        for (int v : adj[pick]) indeg[v]--;\n    }\n\n    if ((int)order.size() != n) {\n        cout << \"CYCLE\\n\";\n        return 0;\n    }\n    for (int i = 0; i < n; i++) {\n        if (i) cout << ' ';\n        cout << order[i];\n    }\n    cout << '\\n';\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "6 6\n6 3\n6 1\n5 1\n5 2\n3 4\n4 2\n",
                "expected_stdout": "5 6 1 3 4 2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 0\n",
                "expected_stdout": "1 2 3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 3\n1 2\n2 3\n3 1\n",
                "expected_stdout": "CYCLE\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4 4\n1 2\n2 3\n3 4\n1 4\n",
                "expected_stdout": "1 2 3 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2 2\n1 2\n1 2\n",
                "expected_stdout": "1 2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "200 600\n1 40\n1 42\n1 61\n1 83\n1 105\n1 113\n1 151\n2 13\n2 22\n2 41\n2 42\n2 44\n2 56\n2 76\n2 149\n3 61\n3 64\n3 104\n3 140\n3 190\n4 8\n4 70\n4 152\n4 175\n4 177\n5 50\n5 77\n6 23\n6 82\n6 98\n6 111\n7 26\n7 42\n7 43\n7 44\n7 76\n7 118\n7 135\n7 137\n7 154\n7 169\n8 12\n8 151\n8 165\n9 105\n9 111\n9 112\n9 128\n9 141\n10 16\n10 35\n10 64\n10 79\n10 82\n10 113\n10 187\n11 14\n11 28\n11 36\n11 73\n11 179\n12 108\n12 124\n12 169\n13 74\n13 93\n13 115\n13 120\n13 125\n13 138\n13 156\n13 162\n13 168\n13 169\n13 170\n14 21\n14 52\n14 63\n14 84\n14 93\n14 102\n14 106\n14 141\n14 145\n15 105\n15 135\n15 198\n16 36\n16 37\n16 59\n16 79\n16 90\n16 112\n16 113\n16 134\n16 191\n17 40\n17 110\n17 133\n17 150\n17 153\n18 93\n18 108\n18 150\n19 36\n19 63\n19 91\n19 111\n19 198\n20 42\n20 44\n20 74\n20 76\n20 78\n21 24\n21 34\n21 57\n21 112\n21 113\n21 126\n21 128\n21 132\n21 143\n21 167\n21 173\n21 178\n21 179\n22 34\n22 37\n22 62\n22 73\n22 93\n22 169\n22 179\n22 180\n22 183\n22 185\n23 26\n23 39\n23 87\n23 95\n23 111\n24 61\n24 108\n24 119\n24 121\n24 151\n24 185\n24 200\n25 192\n26 37\n26 68\n26 80\n26 99\n26 110\n27 43\n27 173\n28 39\n28 91\n28 94\n28 121\n28 192\n29 75\n29 140\n29 141\n29 151\n29 185\n30 41\n30 74\n30 82\n30 113\n30 122\n30 124\n30 137\n31 34\n31 78\n31 130\n31 160\n31 188\n31 193\n31 196\n32 55\n32 56\n32 120\n32 165\n32 167\n33 45\n33 63\n33 82\n33 114\n33 180\n33 190\n33 198\n34 161\n35 70\n35 73\n35 81\n35 177\n36 40\n36 44\n36 66\n36 82\n36 107\n36 195\n37 63\n37 72\n37 85\n37 110\n37 132\n37 159\n37 182\n37 185\n38 45\n38 95\n38 178\n39 47\n39 62\n39 71\n39 102\n39 110\n39 120\n39 198\n40 131\n40 154\n40 192\n40 199\n41 64\n41 197\n42 132\n43 69\n43 100\n43 157\n43 186\n43 195\n44 52\n44 132\n44 194\n45 49\n45 61\n45 117\n45 125\n45 188\n46 91\n46 101\n46 114\n46 132\n47 51\n47 121\n47 154\n48 60\n48 75\n48 165\n49 66\n49 76\n49 127\n49 138\n49 139\n49 168\n49 193\n50 85\n50 129\n50 153\n50 189\n51 54\n51 69\n51 140\n51 160\n51 165\n51 180\n52 101\n52 124\n52 187\n53 57\n53 88\n53 125\n53 140\n53 163\n53 183\n53 192\n54 83\n55 93\n55 192\n56 60\n56 96\n56 160\n56 192\n57 117\n57 118\n57 136\n57 150\n57 160\n58 119\n58 120\n58 179\n58 190\n58 193\n59 84\n59 86\n59 91\n59 122\n59 126\n59 184\n60 86\n60 116\n60 167\n60 174\n61 128\n61 161\n61 166\n61 192\n62 67\n62 89\n62 91\n62 174\n62 178\n63 90\n63 95\n63 193\n63 194\n64 95\n64 166\n64 175\n65 116\n65 144\n65 162\n65 174\n65 184\n66 75\n67 102\n67 120\n67 185\n67 200\n68 156\n68 188\n69 114\n69 151\n70 178\n70 195\n71 105\n71 192\n71 196\n72 93\n72 114\n72 139\n72 147\n72 180\n72 183\n73 78\n73 102\n73 132\n74 79\n74 171\n74 176\n74 199\n75 80\n75 113\n75 138\n75 175\n76 105\n76 109\n76 117\n76 140\n76 149\n76 198\n77 88\n77 172\n78 115\n79 98\n79 106\n79 125\n79 131\n79 167\n80 86\n80 147\n80 186\n81 108\n81 109\n81 123\n81 177\n81 186\n82 86\n82 118\n82 133\n82 163\n83 106\n84 88\n84 99\n84 124\n84 139\n84 153\n84 175\n85 88\n85 95\n85 111\n85 132\n85 171\n85 196\n87 101\n87 145\n87 167\n87 174\n87 195\n88 102\n89 103\n89 130\n89 135\n89 172\n89 191\n90 101\n90 154\n90 168\n91 116\n91 117\n91 150\n91 169\n91 180\n92 128\n92 156\n92 184\n93 110\n93 128\n93 149\n93 200\n94 119\n94 133\n94 146\n95 96\n96 98\n96 118\n96 136\n96 144\n96 161\n96 175\n96 181\n96 195\n97 119\n98 116\n98 162\n98 190\n99 133\n99 184\n100 111\n100 135\n101 125\n101 192\n102 127\n102 135\n102 152\n102 157\n102 171\n103 111\n103 114\n103 142\n103 167\n103 176\n103 195\n104 106\n104 152\n104 173\n105 145\n105 147\n105 166\n106 110\n106 115\n106 117\n106 121\n106 143\n106 199\n107 166\n107 172\n108 128\n108 146\n108 158\n108 159\n108 165\n108 169\n109 118\n109 127\n109 163\n109 182\n110 138\n110 157\n112 118\n112 185\n113 120\n113 174\n114 135\n115 117\n115 152\n115 155\n115 180\n116 128\n116 172\n117 141\n117 172\n118 151\n118 163\n118 169\n118 192\n118 200\n119 131\n119 153\n120 153\n120 160\n120 179\n120 183\n120 186\n121 150\n122 139\n122 141\n122 193\n123 145\n123 147\n123 176\n124 125\n124 134\n125 138\n125 148\n125 150\n125 196\n126 134\n126 156\n126 162\n126 200\n127 163\n128 153\n128 167\n129 157\n129 196\n130 184\n130 192\n130 198\n131 157\n131 197\n132 140\n132 167\n132 168\n132 186\n133 136\n133 166\n133 197\n135 157\n135 189\n135 194\n135 197\n136 157\n136 163\n136 185\n136 196\n137 190\n138 171\n140 156\n141 171\n142 170\n143 147\n143 175\n144 145\n144 147\n144 174\n144 182\n145 147\n146 172\n148 150\n148 172\n149 158\n149 159\n150 156\n151 167\n151 193\n152 159\n152 174\n152 183\n153 183\n154 158\n157 169\n158 184\n159 181\n160 194\n160 195\n161 181\n161 184\n163 170\n163 173\n164 175\n164 182\n165 166\n165 196\n166 181\n167 197\n170 185\n171 181\n172 194\n173 197\n174 195\n175 188\n176 197\n177 186\n179 185\n179 199\n182 189\n",
                "expected_stdout": "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "快排划分后主元的落点",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 12,
        "tags": [
            "编程精练",
            "排序",
            "快速排序",
            "划分"
        ],
        "statement_md": "对给定序列做**一趟快速排序的划分**：以**第一个元素**为枢轴，按教材的**「挖坑填数」**法划分。输出两行：\n1. 划分后的序列\n2. 枢轴的最终下标（**1-based**）\n\n挖坑法的流程（务必照这个来，不同划分法的结果不同）：\n```\npivot = a[low]\nwhile low < high:\n    while low < high and a[high] >= pivot: high--\n    a[low] = a[high]                      # 右边的坑填到左边\n    while low < high and a[low] <= pivot: low++\n    a[high] = a[low]                      # 左边的坑填到右边\na[low] = pivot\n```\n\n★ 「挖坑」这个名字来自过程本身：`a[low]` 的值已经被 `pivot` 存下来了，所以那个位置**空了**，是个可以随便覆盖的坑。于是就不需要 `swap`，一路「拿右边的填左边的坑、再拿左边的填右边的坑」，最后把 `pivot` 补进最后一个坑。\n\n★ 划分完的性质：`pivot` 左边全 `≤ pivot`、右边全 `≥ pivot`——**枢轴从此就位**，后面递归只需要处理左右两段（这就是快排的分治点）。\n\n⚠️ 内层两个 `while` 的边界条件都带 `low < high`，不能省。省掉的话，`high--` 会一路减到越界。",
        "input_format": "第一行 `n`；第二行 `n` 个整数。",
        "output_format": "两行：划分后的序列；枢轴的 1-based 下标。",
        "constraints_md": "- 1 ≤ n ≤ 10⁵\n- |元素| ≤ 10⁹\n- 枢轴取第一个元素",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "编程精练 · C/C++",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <vector>\nusing namespace std;\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    vector<long long> a(n);\n    for (int i = 0; i < n; i++) scanf(\"%lld\", &a[i]);\n\n    long long pivot = a[0];\n    int low = 0, high = n - 1;\n    while (low < high) {\n        while (low < high && a[high] >= pivot) high--;\n        a[low] = a[high];\n        while (low < high && a[low] <= pivot) low++;\n        a[high] = a[low];\n    }\n    a[low] = pivot;\n\n    for (int i = 0; i < n; i++) {\n        printf(\"%lld\", a[i]);\n        putchar(i + 1 == n ? '\\n' : ' ');\n    }\n    printf(\"%d\\n\", low + 1);\n    return 0;\n}\n",
        "alt_solution": "#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n\n    int n;\n    if (!(cin >> n)) return 0;\n    vector<long long> a(n);\n    for (int i = 0; i < n; i++) cin >> a[i];\n\n    // 另一条路：显式维护「坑位」变量 hole，而不是靠 low/high 兼作坑位。\n    // 逻辑等价，但读起来「谁现在是坑」一目了然。\n    long long pivot = a[0];\n    int lo = 0, hi = n - 1;\n    int hole = 0;                       // 当前空坑的下标\n    while (lo < hi) {\n        while (lo < hi && a[hi] >= pivot) hi--;\n        a[hole] = a[hi];\n        hole = hi;\n        while (lo < hi && a[lo] <= pivot) lo++;\n        if (lo < hi) {\n            a[hole] = a[lo];\n            hole = lo;\n        }\n    }\n    a[hole] = pivot;\n\n    for (int i = 0; i < n; i++) {\n        if (i) cout << ' ';\n        cout << a[i];\n    }\n    cout << '\\n' << hole + 1 << '\\n';\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "6\n5 2 9 1 7 3\n",
                "expected_stdout": "3 2 1 5 7 9\n4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n42\n",
                "expected_stdout": "42\n1\n",
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
                "stdin": "5\n5 4 3 2 1\n",
                "expected_stdout": "1 4 3 2 5\n5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7\n4 4 2 4 9 4 1\n",
                "expected_stdout": "1 4 2 4 4 4 9\n5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "二叉排序树的插入与查找次数",
        "subject": "ds",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 12,
        "tags": [
            "编程精练",
            "二叉排序树",
            "BST",
            "查找"
        ],
        "statement_md": "把 `n` 个整数**依次**插入一棵初始为空的二叉排序树（BST），**插入时遇到已存在的值则忽略**。然后回答 `q` 次查找。\n\n输出：\n1. 第一行：BST 的**中序遍历**（一定是升序，空格分隔；树为空时输出空行）\n2. 之后 `q` 行：每次查找**比较了多少个结点**（找到则输出比较次数，找不到输出 `-1`）\n\n比较次数的定义：从根开始，每拿一个结点与目标比一次就 +1；一路比较到命中。若走到空指针仍未命中，说明不存在。\n\n★ BST 的定义只有一句：**左子树上所有结点 < 根 < 右子树上所有结点**。所以插入/查找都是一条道走到黑——不需要回溯。\n\n★ 中序遍历天然升序，这是 BST 最实用的性质：「判断一棵树是不是 BST」最稳的做法就是中序遍历看是否严格递增。\n\n⚠️ 比较次数就是**结点在树中的深度**。这意味着 BST 的效率完全取决于树高：数据是随机的时候树高约 `O(log n)`，但**如果按升序插入，树会退化成一链**，查找变成 `O(n)`。这就是为什么工程上要用 AVL / 红黑树做平衡。",
        "input_format": "第一行 `n`；第二行 `n` 个整数（依次插入）；第三行 `q`；第四行 `q` 个查询值。",
        "output_format": "第一行中序遍历；之后 `q` 行每行一个比较次数（不存在为 `-1`）。",
        "constraints_md": "- 1 ≤ n ≤ 2000，1 ≤ q ≤ 2000\n- |值| ≤ 10⁹\n- 插入重复值时忽略",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "编程精练 · C/C++",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <vector>\nusing namespace std;\n\nstruct Node {\n    int val;\n    Node* lch;\n    Node* rch;\n    Node(int v) : val(v), lch(nullptr), rch(nullptr) {}\n};\n\nNode* insert(Node* root, int x) {\n    if (!root) return new Node(x);\n    if (x < root->val)      root->lch = insert(root->lch, x);\n    else if (x > root->val) root->rch = insert(root->rch, x);\n    // x == root->val 时忽略\n    return root;\n}\n\nvoid inorder(Node* root, vector<int>& out) {\n    if (!root) return;\n    inorder(root->lch, out);\n    out.push_back(root->val);\n    inorder(root->rch, out);\n}\n\nvoid destroy(Node* root) {\n    if (!root) return;\n    destroy(root->lch);\n    destroy(root->rch);\n    delete root;\n}\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    Node* root = nullptr;\n    for (int i = 0; i < n; i++) {\n        int x;\n        scanf(\"%d\", &x);\n        root = insert(root, x);\n    }\n\n    vector<int> ino;\n    inorder(root, ino);\n    for (size_t i = 0; i < ino.size(); i++) {\n        if (i) putchar(' ');\n        printf(\"%d\", ino[i]);\n    }\n    putchar('\\n');\n\n    int q;\n    scanf(\"%d\", &q);\n    for (int i = 0; i < q; i++) {\n        int x;\n        scanf(\"%d\", &x);\n        Node* cur = root;\n        int steps = 0;\n        bool found = false;\n        while (cur) {\n            steps++;\n            if (x == cur->val) { found = true; break; }\n            cur = (x < cur->val) ? cur->lch : cur->rch;\n        }\n        printf(\"%d\\n\", found ? steps : -1);\n    }\n\n    destroy(root);\n    return 0;\n}\n",
        "alt_solution": "#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n\n    int n;\n    if (!(cin >> n)) return 0;\n\n    // 另一条路：不用 new/指针，用数组下标模拟（lch/rch 存下标，0 表示空）。\n    // 这样既不涉及内存管理，也更容易看出「退化成一链」是怎么回事。\n    vector<int> val(n + 2, 0), lch(n + 2, 0), rch(n + 2, 0);\n    int cnt = 0;\n    for (int i = 0; i < n; i++) {\n        int x;\n        cin >> x;\n        if (cnt == 0) {\n            cnt = 1;\n            val[1] = x;\n            continue;\n        }\n        int cur = 1;\n        while (true) {\n            if (x == val[cur]) break;\n            if (x < val[cur]) {\n                if (lch[cur] == 0) { cnt++; val[cnt] = x; lch[cur] = cnt; break; }\n                cur = lch[cur];\n            } else {\n                if (rch[cur] == 0) { cnt++; val[cnt] = x; rch[cur] = cnt; break; }\n                cur = rch[cur];\n            }\n        }\n    }\n\n    // 中序遍历用显式栈做迭代版\n    vector<int> ino;\n    if (cnt) {\n        vector<int> st;\n        int cur = 1;\n        while (cur || !st.empty()) {\n            while (cur) { st.push_back(cur); cur = lch[cur]; }\n            cur = st.back();\n            st.pop_back();\n            ino.push_back(val[cur]);\n            cur = rch[cur];\n        }\n    }\n    for (size_t i = 0; i < ino.size(); i++) {\n        if (i) cout << ' ';\n        cout << ino[i];\n    }\n    cout << '\\n';\n\n    int q;\n    cin >> q;\n    for (int i = 0; i < q; i++) {\n        int x;\n        cin >> x;\n        int cur = cnt ? 1 : 0;\n        int steps = 0;\n        bool found = false;\n        while (cur) {\n            steps++;\n            if (x == val[cur]) { found = true; break; }\n            cur = (x < val[cur]) ? lch[cur] : rch[cur];\n        }\n        cout << (found ? steps : -1) << '\\n';\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "7\n50 30 70 20 40 60 80\n4\n50 20 80 100\n",
                "expected_stdout": "20 30 40 50 60 70 80\n1\n3\n3\n-1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n5\n2\n5 6\n",
                "expected_stdout": "5\n1\n-1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n10 10 5 15 5\n3\n5 10 15\n",
                "expected_stdout": "5 10 15\n2\n1\n2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "500\n-110483 -204920 636652 -528445 -589281 418315 508713 198151 843570 -69519 -848871 712371 896230 -142228 -237595 974565 -697452 607641 446016 939748 -716727 -892260 -289026 -74574 -183574 310734 589017 -840342 905306 -249082 221933 305794 -826136 456571 15620 217185 950574 736609 -907938 247397 328207 930134 -871160 -789478 -933838 -459335 -123127 -11931 -543002 33628 -915655 -958389 436245 -318688 -521948 -185447 139729 -28939 -427708 231547 -320595 -527456 -719483 -19873 -41943 372843 -893479 -239588 -389940 -519201 304747 412674 -749420 926232 -336090 -654690 376429 -335772 747868 76386 -363986 -161947 -228137 169000 813822 -416817 812976 162027 -166580 -878213 436551 901485 -914511 464423 -746954 -832566 -683639 -204238 286519 -871041 678640 113754 -375670 78933 -260110 -182806 -531275 -616249 385996 -428932 446160 -181668 453907 -832788 -634264 601378 -994475 585027 263349 -569096 518471 701134 -93997 417574 -125575 530688 -229181 770711 -394902 334891 13185 376216 -533620 -996909 584782 283939 940088 -747408 -34250 -233368 -528405 644146 117049 -45468 943845 78418 384749 -574230 -487021 874676 500215 298098 -563670 -282047 -583629 -968253 -525418 74011 -485643 376361 -883490 -659613 -667280 7752 306606 899329 436303 795727 93883 -216335 562049 -565852 -108878 -56915 509959 -80179 -880011 -493335 -80831 885016 -475851 -555482 -584738 -947389 953086 48805 342016 833389 410932 998997 938372 619800 134933 -498257 115001 -696703 58884 522169 247741 793726 -306520 -362703 -612551 -338550 -597711 853728 803333 423856 -487036 221992 516094 51675 754364 -214199 -442970 649083 367161 723284 946628 -334365 404941 904986 -114615 423700 -437153 -188549 -143073 -596953 -337738 -834197 46942 -125718 783540 613893 467230 -96696 -979701 -842088 -583729 190991 408364 -598157 566500 -721554 -432622 738470 664154 158220 476991 -976217 250690 520908 -796313 562882 -750365 -765086 736271 -951229 223526 856568 317408 -911 -201966 -531638 -120030 -878912 -867944 -756723 -22049 -750719 -619625 -406744 -325373 419351 647308 -572858 409812 375734 -227949 -849086 -38673 -758868 117044 127397 -461918 911631 -667017 -984320 -814258 -816022 333274 -994973 -709937 574922 -201706 309305 162778 415238 6746 -622999 102195 401763 -711078 -6500 893706 -174285 826905 811851 435543 138597 -956208 -147903 -891484 601376 -996145 511979 737166 -172367 936169 -920615 881046 -676061 -677842 169630 -106870 -156923 -675526 349140 666542 645838 358656 383329 -259489 -298810 515053 369258 852856 191745 -424859 -434204 -36645 195769 -135450 -111261 923888 629591 -382495 -380923 503847 413992 463683 -467077 -2187 545268 560658 627176 -82041 504243 -678272 931409 -602431 -154015 904279 336194 -363323 664942 123405 -684377 638887 359072 -881459 -863508 -727248 799470 728702 993733 687874 -879721 -749220 734162 266880 -92178 346982 981125 351805 232844 -116479 -310325 751629 247468 -376476 331386 821108 -619658 342128 625978 -435468 -492215 5093 803601 379020 -706925 -366495 405341 372672 673213 430016 870031 461277 832899 289933 -338869 213607 -402909 888906 -776988 -945901 -82800 193169 235491 -764626 845422 966149 -648522 62072 -918693 -949763 42229 -138999 159840 -279668 165298 -412161 636537 -153276 -918519 -708524 449298 781099 -179371 -688771 -909693 -815114 -760076 727409 -64872 761596 270999 -610379 -430627 -6878 -613273 -279166 -789353 242885 -986439 -320712 178214 527961 928275 -885607 -688471 -495882 -255814 -384935 -491689 234336 619950 -332646 -363936 -504853 121428 281855 382476 -309259 424137 -942052 209953 -710023 -206272 -819610 -325204 -56204 531228 -113216 -258521 -404285 786925 484385 -484878 -778888 -986827 428978 924381 424424 -160357 648343 -570880 -920830 66547\n202\n-863508 728702 -778888 998997 74011 467230 117044 209953 -233368 -584738 -228137 666542 -675526 953086 -434204 924381 383329 165298 33628 -871160 938372 607641 -708524 -64872 382476 304747 645838 -711078 -654690 -116479 -986439 -750365 408364 424137 367161 924381 165298 520908 -727248 -82800 950574 -96696 436551 436551 853728 -138999 -320712 -82041 404941 -760076 998997 359072 -363323 -711078 -201966 328207 -434204 911631 893706 123405 -543002 306606 247741 -80831 484385 589017 247741 58884 405341 -826136 464423 289933 74011 -123127 -325373 384749 -619658 484385 625978 939748 589017 -56204 446016 -34250 885016 232844 904279 924381 383329 -708524 -435468 -325204 -892260 -572858 -918693 113754 298098 -597711 -883490 -834197 -289026 306606 -688471 856568 178214 601378 793726 281855 -504853 701134 574922 601378 -320712 -237595 -531638 306606 -986439 -826136 -563670 738470 -832566 -951229 464423 -893479 -789478 134933 -185447 231547 -394902 -814258 734162 -402909 -684377 -201966 430016 358656 901485 42229 -683639 -366495 -528405 -996145 754364 -188549 419351 -437153 -22049 -432622 560658 -461918 -976217 -750365 247741 946628 885016 -111261 -648522 408364 463683 -719483 -716727 -172367 456571 562049 464423 304747 -461918 405341 -598157 -160357 -909693 333274 -172367 -228137 -233368 13185 589017 242885 -531638 -986439 619800 -111261 263349 -622999 530688 423700 518471 -613273 -879721 -166580 901485 221933 -994475 -871041 -528405 678640 -2187 169000 -589281 -765086 1000000000 -1000000000\n",
                "expected_stdout": "-996909 -996145 -994973 -994475 -986827 -986439 -984320 -979701 -976217 -968253 -958389 -956208 -951229 -949763 -947389 -945901 -942052 -933838 -920830 -920615 -918693 -918519 -915655 -914511 -909693 -907938 -893479 -892260 -891484 -885607 -883490 -881459 -880011 -879721 -878912 -878213 -871160 -871041 -867944 -863508 -849086 -848871 -842088 -840342 -834197 -832788 -832566 -826136 -819610 -816022 -815114 -814258 -796313 -789478 -789353 -778888 -776988 -765086 -764626 -760076 -758868 -756723 -750719 -750365 -749420 -749220 -747408 -746954 -727248 -721554 -719483 -716727 -711078 -710023 -709937 -708524 -706925 -697452 -696703 -688771 -688471 -684377 -683639 -678272 -677842 -676061 -675526 -667280 -667017 -659613 -654690 -648522 -634264 -622999 -619658 -619625 -616249 -613273 -612551 -610379 -602431 -598157 -597711 -596953 -589281 -584738 -583729 -583629 -574230 -572858 -570880 -569096 -565852 -563670 -555482 -543002 -533620 -531638 -531275 -528445 -528405 -527456 -525418 -521948 -519201 -504853 -498257 -495882 -493335 -492215 -491689 -487036 -487021 -485643 -484878 -475851 -467077 -461918 -459335 -442970 -437153 -435468 -434204 -432622 -430627 -428932 -427708 -424859 -416817 -412161 -406744 -404285 -402909 -394902 -389940 -384935 -382495 -380923 -376476 -375670 -366495 -363986 -363936 -363323 -362703 -338869 -338550 -337738 -336090 -335772 -334365 -332646 -325373 -325204 -320712 -320595 -318688 -310325 -309259 -306520 -298810 -289026 -282047 -279668 -279166 -260110 -259489 -258521 -255814 -249082 -239588 -237595 -233368 -229181 -228137 -227949 -216335 -214199 -206272 -204920 -204238 -201966 -201706 -188549 -185447 -183574 -182806 -181668 -179371 -174285 -172367 -166580 -161947 -160357 -156923 -154015 -153276 -147903 -143073 -142228 -138999 -135450 -125718 -125575 -123127 -120030 -116479 -114615 -113216 -111261 -110483 -108878 -106870 -96696 -93997 -92178 -82800 -82041 -80831 -80179 -74574 -69519 -64872 -56915 -56204 -45468 -41943 -38673 -36645 -34250 -28939 -22049 -19873 -11931 -6878 -6500 -2187 -911 5093 6746 7752 13185 15620 33628 42229 46942 48805 51675 58884 62072 66547 74011 76386 78418 78933 93883 102195 113754 115001 117044 117049 121428 123405 127397 134933 138597 139729 158220 159840 162027 162778 165298 169000 169630 178214 190991 191745 193169 195769 198151 209953 213607 217185 221933 221992 223526 231547 232844 234336 235491 242885 247397 247468 247741 250690 263349 266880 270999 281855 283939 286519 289933 298098 304747 305794 306606 309305 310734 317408 328207 331386 333274 334891 336194 342016 342128 346982 349140 351805 358656 359072 367161 369258 372672 372843 375734 376216 376361 376429 379020 382476 383329 384749 385996 401763 404941 405341 408364 409812 410932 412674 413992 415238 417574 418315 419351 423700 423856 424137 424424 428978 430016 435543 436245 436303 436551 446016 446160 449298 453907 456571 461277 463683 464423 467230 476991 484385 500215 503847 504243 508713 509959 511979 515053 516094 518471 520908 522169 527961 530688 531228 545268 560658 562049 562882 566500 574922 584782 585027 589017 601376 601378 607641 613893 619800 619950 625978 627176 629591 636537 636652 638887 644146 645838 647308 648343 649083 664154 664942 666542 673213 678640 687874 701134 712371 723284 727409 728702 734162 736271 736609 737166 738470 747868 751629 754364 761596 770711 781099 783540 786925 793726 795727 799470 803333 803601 811851 812976 813822 821108 826905 832899 833389 843570 845422 852856 853728 856568 870031 874676 881046 885016 888906 893706 896230 899329 901485 904279 904986 905306 911631 923888 924381 926232 928275 930134 931409 936169 938372 939748 940088 943845 946628 950574 953086 966149 974565 981125 993733 998997\n11\n8\n17\n6\n10\n9\n13\n9\n7\n9\n5\n9\n12\n8\n13\n12\n12\n12\n7\n7\n9\n5\n10\n12\n14\n9\n9\n9\n7\n7\n14\n13\n13\n10\n10\n12\n12\n11\n15\n12\n7\n9\n7\n7\n6\n8\n15\n10\n12\n18\n6\n13\n14\n9\n8\n6\n13\n10\n7\n14\n5\n8\n12\n9\n11\n6\n12\n12\n14\n9\n7\n12\n10\n4\n14\n11\n12\n11\n9\n6\n6\n12\n5\n10\n6\n10\n10\n12\n12\n10\n14\n16\n6\n8\n11\n10\n11\n10\n9\n12\n5\n8\n12\n7\n12\n7\n11\n15\n12\n6\n13\n7\n15\n4\n8\n8\n14\n9\n7\n7\n10\n11\n7\n8\n10\n12\n5\n9\n12\n12\n9\n14\n10\n8\n9\n12\n8\n13\n8\n14\n9\n13\n10\n7\n9\n11\n10\n12\n13\n12\n13\n13\n12\n10\n6\n6\n10\n13\n8\n11\n7\n10\n6\n11\n7\n9\n12\n14\n11\n9\n11\n9\n10\n5\n7\n8\n6\n12\n8\n14\n6\n6\n11\n11\n9\n8\n8\n10\n12\n6\n8\n6\n10\n8\n9\n5\n12\n9\n4\n14\n-1\n-1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    }
]
