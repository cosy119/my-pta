# -*- coding: utf-8 -*-
"""C++ 基础（subject=cpp）编程题库 —— 自动生成，**不要手改本文件**。

生成器：tools/gen_cpp_prog.py
分节：第 02 ~ 12 讲，共 17 题

重生成：python tools/gen_cpp_prog.py
"""

CPP_PROG_PROBLEMS: list[dict] = [
    {
        "title": "位运算消 1：二进制中 1 的个数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "C++基础",
            "位运算",
            "无符号数",
            "循环"
        ],
        "statement_md": "读入 `n` 个非负整数，逐个输出「它的二进制表示里 1 的个数」。\n\n讲义 2.2 节给的标准写法是：\n\n```cpp\nint countOnes(unsigned x) {\n    int c = 0;\n    while (x) { x &= x - 1; c++; }\n    return c;\n}\n```\n\n★ 为什么 `x &= x - 1` 能数 1：减 1 会把**最低位的那个 1 变成 0**，并把它右边的 0 全部变成 1；再与原来的 `x` 相与，右边那些新冒出来的 1 又被打回去，结果就是「最低位的 1 被干净地抹掉」。所以每循环一次恰好消掉一个 1，**循环次数 = 1 的个数**，而不是 32 次。\n\n⚠️ 两个边界：\n1. `x = 0` 时循环一次都不进，答案 0（不是 32）；\n2. `x` 要用**无符号**类型。若用 `int` 存 2³¹ 以上的值，`x - 1` 在负数上做位运算，行为虽然在本机可用，但标准里右移/溢出的口径不保证，属于自己给自己挖坑。",
        "input_format": "第一行 `n`；第二行 `n` 个非负整数。",
        "output_format": "`n` 行，每行 `x k`：原数与它二进制中 1 的个数，中间一个空格。",
        "constraints_md": "- 1 ≤ n ≤ 10\n- 0 ≤ x ≤ 2³²−1（用 `unsigned int` 读）\n- 建议 O(popcount) 而不是固定 32 轮",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 02 讲 · C++ 简单程序设计",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nusing namespace std;\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    for (int i = 0; i < n; i++) {\n        unsigned x;\n        if (scanf(\"%u\", &x) != 1) return 0;\n        int c = 0;\n        unsigned t = x;\n        while (t) {          // 每轮抹掉最低位的 1\n            t &= t - 1;\n            c++;\n        }\n        printf(\"%u %d\\n\", x, c);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nusing namespace std;\n\n// 独立点：不写循环，直接调用编译器内建的 popcount（底层是查表/硬件指令），\n// 与参考解「x &= x-1 逐位消 1」是两条完全不同的实现路径。\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    for (int i = 0; i < n; i++) {\n        unsigned x;\n        if (scanf(\"%u\", &x) != 1) return 0;\n        printf(\"%u %d\\n\", x, __builtin_popcount(x));\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4\n29 255 0 1\n",
                "expected_stdout": "29 4\n255 8\n0 0\n1 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n7 8 1024\n",
                "expected_stdout": "7 3\n8 1\n1024 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n2147483647 2147483648\n",
                "expected_stdout": "2147483647 31\n2147483648 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n4294967295\n",
                "expected_stdout": "4294967295 32\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n0 0 1 2 3\n",
                "expected_stdout": "0 0\n0 0\n1 1\n2 1\n3 2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n65535 65536 123456789 1000000000 536870912 1073741823\n",
                "expected_stdout": "65535 16\n65536 1\n123456789 16\n1000000000 13\n536870912 1\n1073741823 30\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "switch 贯穿实现阶梯水费",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "C++基础",
            "switch",
            "贯穿",
            "分段计费"
        ],
        "statement_md": "阶梯水价：每月用水 `x` 吨（整数），计价规则是\n\n| 档位 | 用水量 | 单价 |\n|---|---|---|\n| 1 | 1~10 吨 | 3 元/吨 |\n| 2 | 11~20 吨 | 超出 10 吨的部分 4 元/吨 |\n| 3 | 21~30 吨 | 超出 20 吨的部分 5 元/吨 |\n| 4 | 31 吨以上 | 超出 30 吨的部分 6 元/吨 |\n\n对每次查询输出 `level=<档位> fee=<总费用>`。\n\n★ 为什么这题值得用 `switch` 写：算总费用天生是「**从最高档往低档逐段累加**」——先用 `x` 落档，再让 `switch` **故意不写 break** 一路贯穿下去，每落一层就把该段的水量乘单价加进 `fee`。这正好是讲义 2.4.2 里「漏 break 会贯穿」那个坑的**正面用法**：贯穿不是 bug，是「连续做几件相关的事」的语法。\n\n⚠️ 贯穿写法必须保证每一段的水量都算对：第 4 档要加 `x-30`（10 吨）、第 3 档加 `min(x,30)-20`（又 10 吨）…… 一旦写成 `x-20` 就会把前面已经算过的水量重复计费。\n\n⚠️ 费用用 `long long`：`x` 取 10⁹ 时费用是 6×10⁹，`int` 直接溢出。",
        "input_format": "第一行 `q`（查询次数）；第二行 `q` 个非负整数，表示用水量。",
        "output_format": "`q` 行，每行 `level=<1~4> fee=<总费用>`。",
        "constraints_md": "- 1 ≤ q ≤ 10⁵\n- 0 ≤ x ≤ 10⁹\n- 费用需要用 64 位整数",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 02 讲 · C++ 简单程序设计",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nusing namespace std;\n\nint main() {\n    int q;\n    if (scanf(\"%d\", &q) != 1) return 0;\n    for (int i = 0; i < q; i++) {\n        long long x;\n        scanf(\"%lld\", &x);\n        int level;\n        long long fee;\n        if (x <= 10)      { level = 1; fee = 3 * x; }\n        else if (x <= 20) { level = 2; fee = 30 + 4 * (x - 10); }\n        else if (x <= 30) { level = 3; fee = 70 + 5 * (x - 20); }\n        else              { level = 4; fee = 120 + 6 * (x - 30); }\n        printf(\"level=%d fee=%lld\\n\", level, fee);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nusing namespace std;\n\n// 独立点：先落档，再用 switch **故意贯穿**从高档往低档逐段累加 ——\n// 参考解是一条 if-else 链直接算出总价，这里是「累加式」的另一种推导。\nint main() {\n    int q;\n    if (scanf(\"%d\", &q) != 1) return 0;\n    for (int i = 0; i < q; i++) {\n        long long x;\n        scanf(\"%lld\", &x);\n        int level = (x <= 10) ? 1 : (x <= 20) ? 2 : (x <= 30) ? 3 : 4;\n        long long fee = 0;\n        switch (level) {\n            case 4: fee += 6 * (x - 30);              [[fallthrough]];\n            case 3: fee += 5 * (min<long long>(x, 30) - 20); [[fallthrough]];\n            case 2: fee += 4 * (min<long long>(x, 20) - 10); [[fallthrough]];\n            case 1: fee += 3 * min<long long>(x, 10); break;\n        }\n        printf(\"level=%d fee=%lld\\n\", level, fee);\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n0 10 11\n",
                "expected_stdout": "level=1 fee=0\nlevel=1 fee=30\nlevel=2 fee=34\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n20 21 30 31\n",
                "expected_stdout": "level=2 fee=70\nlevel=3 fee=75\nlevel=3 fee=120\nlevel=4 fee=126\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n1 15 25 100 999\n",
                "expected_stdout": "level=1 fee=3\nlevel=2 fee=50\nlevel=3 fee=95\nlevel=4 fee=540\nlevel=4 fee=5934\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n1000000000\n",
                "expected_stdout": "level=4 fee=5999999940\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n9 10\n",
                "expected_stdout": "level=1 fee=27\nlevel=1 fee=30\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n0 1 29 30 31 32\n",
                "expected_stdout": "level=1 fee=0\nlevel=1 fee=3\nlevel=3 fee=115\nlevel=3 fee=120\nlevel=4 fee=126\nlevel=4 fee=132\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "递归打印汉诺塔移动序列",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "C++函数",
            "递归",
            "递归三要素",
            "运行栈"
        ],
        "statement_md": "把 `n` 个盘子从 A 柱借助 B 柱搬到 C 柱，大盘不能压在小盘上。第一行输出**最少移动步数**，随后按顺序输出每一步 `源->目标`。\n\n★ 递归三要素在这题上一目了然：\n1. **出口**：`n == 0` 直接返回（一步都不用走）；\n2. **递推步**：挪 `n` 层 = 先挪上面 `n-1` 层让路 + 挪最底下那 1 层 + 再把 `n-1` 层归位；\n3. **规模缩小**：每次递归 `n` 都减 1，一定撞到出口。\n\n★ 为什么先输出步数：`T(n) = 2·T(n−1) + 1` 解出 `T(n) = 2ⁿ − 1`，讲义里 n=20 实测 1048575 次调用 —— 每加一层工作量翻倍，这就是「指数爆炸」。所以本题 `n ≤ 12`，输出行数最多 4095 行；再大就不是判题机能救的了。\n\n⚠️ 参数顺序是最大的坑：`hanoi(n-1, from, to, via)` 里的第三、四个实参**交换了位置**（借助 to 挪到 via）。写反了不报错，但前几步就全错。",
        "input_format": "一个整数 `n`。",
        "output_format": "第一行是最少步数 `2^n-1`；随后每行一步，形如 `A->C`（无空格）。",
        "constraints_md": "- 1 ≤ n ≤ 12\n- 输出行数 ≤ 4096 行",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 03 讲 · 函数",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nusing namespace std;\n\nstatic void hanoi(int n, char from, char via, char to) {\n    if (n == 0) return;                       // 出口\n    hanoi(n - 1, from, to, via);              // 上面 n-1 层让路\n    printf(\"%c->%c\\n\", from, to);             // 挪最大的那 1 层\n    hanoi(n - 1, via, from, to);              // 再归位\n}\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    printf(\"%lld\\n\", (1LL << n) - 1);\n    hanoi(n, 'A', 'B', 'C');\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <vector>\nusing namespace std;\n\n// 独立点：完全不递归 —— 自己开一个 vector 当运行栈，显式保存\n// 「哪一层、从哪到哪、走到第几步」，靠 stage 状态机推进。\n// 结果序列与递归版完全一致，但走的是迭代路径。\nstruct Frame {\n    int n;\n    char from, via, to;\n    int stage;          // 0 未开始 / 1 左半已做完 / 2 已打印本层\n};\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    printf(\"%lld\\n\", (1LL << n) - 1);\n\n    vector<Frame> st;\n    st.push_back({n, 'A', 'B', 'C', 0});\n    while (!st.empty()) {\n        Frame f = st.back();\n        st.pop_back();\n        if (f.n == 0) continue;\n        if (f.stage == 0) {\n            st.push_back({f.n, f.from, f.via, f.to, 1});\n            st.push_back({f.n - 1, f.from, f.to, f.via, 0});\n        } else if (f.stage == 1) {\n            printf(\"%c->%c\\n\", f.from, f.to);\n            st.push_back({f.n, f.from, f.via, f.to, 2});\n        } else {\n            st.push_back({f.n - 1, f.via, f.from, f.to, 0});\n        }\n    }\n    return 0;\n}\n",
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
                "stdin": "7\n",
                "expected_stdout": "127\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "11\n",
                "expected_stdout": "2047\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nC->A\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nA->B\nC->B\nC->A\nB->A\nC->B\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\nB->A\nC->B\nC->A\nB->A\nB->C\nA->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "引用传参求最值与首次下标",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "C++函数",
            "引用传参",
            "const 引用",
            "一遍扫描"
        ],
        "statement_md": "读入 `n` 个整数，输出三行：\n\n1. `max=.. min=..`\n2. `max_at=.. min_at=..`（**1 基**下标；最大值取**第一次**出现的位置，最小值取**最后一次**出现的位置）\n3. `range=..`（极差 = 最大值 − 最小值）\n\n★ 为什么强制用引用传参：一个函数只能 `return` 一个值，而这里要同时带回「最大值、最小值、两个下标」共四个结果。C 语言的办法是传指针，C++ 更自然的办法是**引用形参** —— 形参就是实参的别名，函数里写 `mx = a[i]` 就是在改调用方的变量，调用处还不用写 `&`。\n\n建议签名：`void minMax(const vector<int>& a, int& mx, int& mn, int& maxAt, int& minAt)`。注意第一个参数是 **`const` 引用**：只读又不想复制整个数组。\n\n⚠️ 两个易错点：\n1. `maxAt` 用 `>` 更新、`minAt` 用 `>=` 更新 —— 这样才能得到「最大值第一次出现、最小值最后一次出现」，两个比较符号不一样，别抄成一样；\n2. 下标是 1 基，别把 `i` 直接输出。",
        "input_format": "第一行 `n`；第二行 `n` 个整数。",
        "output_format": "三行，格式见题面（`key=value`，同一行内用一个空格分隔）。",
        "constraints_md": "- 1 ≤ n ≤ 10⁵\n- |元素| ≤ 10⁹\n- 极差可能超过 `int`，用 `long long` 保存",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 03 讲 · 函数",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <vector>\nusing namespace std;\n\n// 四个结果全靠引用带回；数组用 const 引用接，既不复制也不许改。\nstatic void minMax(const vector<int>& a, long long& mx, long long& mn,\n                   int& maxAt, int& minAt) {\n    mx = mn = a[0];\n    maxAt = minAt = 1;\n    for (int i = 1; i < (int)a.size(); i++) {\n        if (a[i] > mx)  { mx = a[i]; maxAt = i + 1; }   // 严格大于：取第一次\n        if (a[i] <= mn) { mn = a[i]; minAt = i + 1; }   // 小于等于：取最后一次\n    }\n}\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    vector<int> a(n);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n\n    long long mx, mn;\n    int maxAt, minAt;\n    minMax(a, mx, mn, maxAt, minAt);\n\n    printf(\"max=%lld min=%lld\\n\", mx, mn);\n    printf(\"max_at=%d min_at=%d\\n\", maxAt, minAt);\n    printf(\"range=%lld\\n\", mx - mn);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <vector>\n#include <algorithm>\nusing namespace std;\n\n// 独立点：不手写扫描 —— 最大值交给 max_element（并列返回第一个），\n// 最小值「最后一次出现」用反向迭代器 find。参考解是单趟双 if，\n// 这里是「标准库 + 反向区间」两条腿。\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    vector<int> a(n);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n\n    auto mxit = max_element(a.begin(), a.end());        // 并列时返回第一个\n    long long mx = *mxit, mn = *min_element(a.begin(), a.end());\n\n    int maxAt = int(mxit - a.begin()) + 1;\n    auto rit = find(a.rbegin(), a.rend(), (int)mn);     // 反向找 -> 最后一次\n    int minAt = n - int(rit - a.rbegin());\n\n    printf(\"max=%lld min=%lld\\n\", mx, mn);\n    printf(\"max_at=%d min_at=%d\\n\", maxAt, minAt);\n    printf(\"range=%lld\\n\", mx - mn);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n3 9 -4 9 -4\n",
                "expected_stdout": "max=9 min=-4\nmax_at=2 min_at=5\nrange=13\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n42\n",
                "expected_stdout": "max=42 min=42\nmax_at=1 min_at=1\nrange=0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n5 5 5 5\n",
                "expected_stdout": "max=5 min=5\nmax_at=1 min_at=4\nrange=0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "6\n-1 -1 0 0 -1 -1\n",
                "expected_stdout": "max=0 min=-1\nmax_at=3 min_at=6\nrange=1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n1000000000 -1000000000 0\n",
                "expected_stdout": "max=1000000000 min=-1000000000\nmax_at=1 min_at=2\nrange=2000000000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7\n2 7 7 1 3 1 5\n",
                "expected_stdout": "max=7 min=1\nmax_at=2 min_at=6\nrange=6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "账户类存取款模拟",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "C++类与对象",
            "构造函数",
            "封装",
            "成员函数"
        ],
        "statement_md": "实现一个最小的银行账户类：余额是私有成员，只能通过 `deposit` / `withdraw` 改动。读入初始余额和 `q` 条操作（`D 金额` 存款、`W 金额` 取款），逐条输出操作结果，最后输出一行统计。\n\n输出格式：\n\n```text\ndeposit 100 -> 300\nwithdraw 50 -> 250\nwithdraw 500 FAILED balance=250\nfinal=250 deposit=1 withdraw=1 failed=1\n```\n\n★ 为什么要把余额设成 `private`：如果余额是 public 的，谁都能写 `acc.balance -= 500` 把它扣成负数，而「余额不能透支」这条业务规则就无处安放。封装的意义就是**把规则和它保护的数据放同一个类里** —— `withdraw` 先检查再扣款，检查不过就返回 `false` 并且**一个字节都不改**。\n\n★ 那个 `bool` 返回值是讲义 4.8 的写法：错误用返回值上报，正常路径继续往下走；第 12 讲会把它换成抛异常。\n\n⚠️ 边界：取款金额**恰好等于**余额是允许的（扣完为 0）；取款金额为 0 也算成功。别把判断写成 `>=`。",
        "input_format": "第一行初始余额 `b`；第二行 `q`；随后 `q` 行，每行 `D amt` 或 `W amt`。",
        "output_format": "每条操作一行结果；最后一行 `final=<余额> deposit=<成功存款数> withdraw=<成功取款数> failed=<失败数>`。",
        "constraints_md": "- 0 ≤ b ≤ 10¹²\n- 1 ≤ q ≤ 10⁵\n- 0 ≤ amt ≤ 10¹²\n- 余额与金额用 `long long`",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 04 讲 · 类与对象",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nusing namespace std;\n\nclass Account {\nprivate:\n    long long balance_;                 // 私有：外部只能看，不能改\npublic:\n    explicit Account(long long b = 0) : balance_(b) {}\n\n    void deposit(long long amt) { balance_ += amt; }\n\n    bool withdraw(long long amt) {      // 先检查再扣款\n        if (amt > balance_) return false;\n        balance_ -= amt;\n        return true;\n    }\n    long long balance() const { return balance_; }   // 常成员函数：只读\n};\n\nint main() {\n    long long b;\n    int q;\n    if (scanf(\"%lld %d\", &b, &q) != 2) return 0;\n\n    Account acc(b);\n    int dep = 0, wd = 0, fail = 0;\n    for (int i = 0; i < q; i++) {\n        char op[4];\n        long long amt;\n        scanf(\"%s %lld\", op, &amt);\n        if (op[0] == 'D') {\n            acc.deposit(amt);\n            dep++;\n            printf(\"deposit %lld -> %lld\\n\", amt, acc.balance());\n        } else {\n            if (acc.withdraw(amt)) {\n                wd++;\n                printf(\"withdraw %lld -> %lld\\n\", amt, acc.balance());\n            } else {\n                fail++;\n                printf(\"withdraw %lld FAILED balance=%lld\\n\", amt, acc.balance());\n            }\n        }\n    }\n    printf(\"final=%lld deposit=%d withdraw=%d failed=%d\\n\",\n           acc.balance(), dep, wd, fail);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <string>\n#include <iostream>\nusing namespace std;\n\n// 独立点：余额改成「以分为单位的整数 + 三个计数器放在类里」，\n// withdraw 用「先记账再回滚」而不是「先检查再扣款」，输出口径一致。\n// 另外 IO 换成 cin/cout（参考解用 scanf/printf），行尾仍是 '\\n'。\nclass Account {\n    long long cents_;\n    int dep_, wd_, fail_;\npublic:\n    explicit Account(long long yuan = 0) : cents_(yuan), dep_(0), wd_(0), fail_(0) {}\n\n    void deposit(long long yuan) {\n        cents_ += yuan;\n        dep_++;\n    }\n    bool withdraw(long long yuan) {\n        long long next = cents_ - yuan;      // 先算目标余额\n        if (next < 0) {                      // 余额不足：回滚（这里其实没动过）\n            fail_++;\n            return false;\n        }\n        cents_ = next;\n        wd_++;\n        return true;\n    }\n    long long balance() const { return cents_; }\n    int depCount() const { return dep_; }\n    int wdCount() const { return wd_; }\n    int failCount() const { return fail_; }\n};\n\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n\n    long long b;\n    int q;\n    if (!(cin >> b >> q)) return 0;\n\n    Account acc(b);\n    for (int i = 0; i < q; i++) {\n        string op;\n        long long amt;\n        cin >> op >> amt;\n        if (op == \"D\") {\n            acc.deposit(amt);\n            cout << \"deposit \" << amt << \" -> \" << acc.balance() << '\\n';\n        } else if (acc.withdraw(amt)) {\n            cout << \"withdraw \" << amt << \" -> \" << acc.balance() << '\\n';\n        } else {\n            cout << \"withdraw \" << amt << \" FAILED balance=\" << acc.balance() << '\\n';\n        }\n    }\n    cout << \"final=\" << acc.balance()\n         << \" deposit=\" << acc.depCount()\n         << \" withdraw=\" << acc.wdCount()\n         << \" failed=\" << acc.failCount() << '\\n';\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "100\n4\nD 100\nW 50\nW 500\nD 0\n",
                "expected_stdout": "deposit 100 -> 200\nwithdraw 50 -> 150\nwithdraw 500 FAILED balance=150\ndeposit 0 -> 150\nfinal=150 deposit=2 withdraw=1 failed=1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "0\n3\nW 1\nD 5\nW 5\n",
                "expected_stdout": "withdraw 1 FAILED balance=0\ndeposit 5 -> 5\nwithdraw 5 -> 0\nfinal=0 deposit=1 withdraw=1 failed=1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1000\n3\nW 1000\nD 1\nW 1\n",
                "expected_stdout": "withdraw 1000 -> 0\ndeposit 1 -> 1\nwithdraw 1 -> 0\nfinal=0 deposit=1 withdraw=2 failed=0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "50\n2\nD 450\nW 500\n",
                "expected_stdout": "deposit 450 -> 500\nwithdraw 500 -> 0\nfinal=0 deposit=1 withdraw=1 failed=0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7\n5\nW 3\nW 4\nW 1\nD 100\nW 99\n",
                "expected_stdout": "withdraw 3 -> 4\nwithdraw 4 -> 0\nwithdraw 1 FAILED balance=0\ndeposit 100 -> 100\nwithdraw 99 -> 1\nfinal=1 deposit=1 withdraw=3 failed=1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1000000000000\n3\nW 1000000000000\nD 1\nW 999999999999\n",
                "expected_stdout": "withdraw 1000000000000 -> 0\ndeposit 1 -> 1\nwithdraw 999999999999 FAILED balance=1\nfinal=1 deposit=1 withdraw=1 failed=1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "有理数类的构造函数重载与约分",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "C++类与对象",
            "构造函数重载",
            "常成员函数",
            "gcd"
        ],
        "statement_md": "读入 `n` 个分数（形如 `a/b`，`b ≠ 0`），对每个分数输出**约分后**的形式，最后输出它们的累加和（同样约分）。\n\n输出的分母**永远为正**，负号只出现在分子上：`-6/8` → `-3/4`，`3/-4` → `-3/4`。\n\n★ 这道题练的是「构造函数重载」这一族东西：\n- `Rational()` 默认构造 0/1；\n- `Rational(long long n)` 整数变分数（分母补 1）—— 有它才能写 `Rational(3)`；\n- `Rational(long long a, long long b)` 才是通用版本。\n\n真正的**不变量**在构造函数里建立：任何对象出生时都必须满足「分母 > 0 且已约分」。把归一化写进构造函数（而不是写进每个成员函数），就没有任何一条路径能造出未约分的对象 —— 这叫「用构造函数守住类的约束」。\n\n⚠️ 三个坑：\n1. 符号要先搬到分子再求 gcd，否则 `gcd(-6, -8)` 的符号约定会让你算错；\n2. `gcd(0, 4) = 4`，`0/4` 要归一成 `0/1`，别在 gcd 为 0 时除零；\n3. 通分用 `long long`：分母相乘会快过 `int`。",
        "input_format": "第一行 `n`；随后 `n` 个分数，每个占一行，形如 `a/b`。",
        "output_format": "前 `n` 行是每个分数约分后的形式；最后一行 `sum=<分子>/<分母>`。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- |a| ≤ 1000，1 ≤ |b| ≤ 1000\n- 结果用 `long long` 保存",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 04 讲 · 类与对象",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <string>\n#include <numeric>\n#include <cstdlib>\nusing namespace std;\n\nclass Rational {\nprivate:\n    long long num_, den_;               // 不变量：den_ > 0 且已约分\n    void normalize() {\n        if (den_ < 0) { num_ = -num_; den_ = -den_; }\n        long long a = num_ < 0 ? -num_ : num_;\n        long long g = std::gcd(a, den_);\n        if (g > 1) { num_ /= g; den_ /= g; }\n    }\npublic:\n    Rational() : num_(0), den_(1) {}\n    explicit Rational(long long n) : num_(n), den_(1) {}          // 重载 1\n    Rational(long long n, long long d) : num_(n), den_(d) {       // 重载 2\n        normalize();\n    }\n    Rational add(const Rational& o) const {\n        return Rational(num_ * o.den_ + o.num_ * den_, den_ * o.den_);\n    }\n    long long num() const { return num_; }\n    long long den() const { return den_; }\n};\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    Rational sum;\n    char buf[64];\n    for (int i = 0; i < n; i++) {\n        scanf(\"%63s\", buf);\n        string s(buf);\n        size_t p = s.find('/');\n        Rational f = (p == string::npos)\n                     ? Rational(atoll(s.c_str()))\n                     : Rational(atoll(s.substr(0, p).c_str()),\n                                atoll(s.substr(p + 1).c_str()));\n        printf(\"%lld/%lld\\n\", f.num(), f.den());\n        sum = sum.add(f);\n    }\n    printf(\"sum=%lld/%lld\\n\", sum.num(), sum.den());\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <string>\n#include <numeric>\n#include <cstdlib>\nusing namespace std;\n\n// 独立点：不做「每加一次就约分」，而是先把所有分数通分到同一个公分母\n// （边读边求 lcm），加完只约分一次。两条路径的结果必然相同，\n// 但中间量与运算次数完全不一样。\nstruct Frac { long long a, b; };\n\nstatic Frac reduce(Frac f) {\n    if (f.b < 0) { f.a = -f.a; f.b = -f.b; }\n    long long g = std::gcd(f.a < 0 ? -f.a : f.a, f.b);\n    if (g > 1) { f.a /= g; f.b /= g; }\n    return f;\n}\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n\n    char buf[64];\n    Frac fs[16];\n    for (int i = 0; i < n; i++) {\n        scanf(\"%63s\", buf);\n        string s(buf);\n        size_t p = s.find('/');\n        Frac f;\n        if (p == string::npos) { f.a = atoll(s.c_str()); f.b = 1; }\n        else {\n            f.a = atoll(s.substr(0, p).c_str());\n            f.b = atoll(s.substr(p + 1).c_str());\n        }\n        fs[i] = reduce(f);\n        printf(\"%lld/%lld\\n\", fs[i].a, fs[i].b);\n    }\n\n    // 通分到所有分母的最小公倍数，最后只约分一次\n    long long L = 1;\n    for (int k = 0; k < n; k++) {\n        long long g = std::gcd(L, fs[k].b);\n        L = L / g * fs[k].b;\n    }\n    long long s2 = 0;\n    for (int k = 0; k < n; k++) s2 += fs[k].a * (L / fs[k].b);\n    Frac r = reduce({s2, L});\n    printf(\"sum=%lld/%lld\\n\", r.a, r.b);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "2\n1/2\n1/3\n",
                "expected_stdout": "1/2\n1/3\nsum=5/6\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n-6/8\n3/-4\n0/5\n",
                "expected_stdout": "-3/4\n-3/4\n0/1\nsum=-3/2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n7/1\n",
                "expected_stdout": "7/1\nsum=7/1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n1/2\n1/2\n1/2\n1/2\n",
                "expected_stdout": "1/2\n1/2\n1/2\n1/2\nsum=2/1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n-1/3\n2/6\n5/-10\n7/14\n-1/2\n",
                "expected_stdout": "-1/3\n1/3\n-1/2\n1/2\n-1/2\nsum=-1/2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n999/1000\n-999/1000\n1/999\n",
                "expected_stdout": "999/1000\n-999/1000\n1/999\nsum=1/999\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "静态成员统计存活账户数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "C++共享与保护",
            "静态数据成员",
            "静态成员函数",
            "对象生命周期"
        ],
        "statement_md": "用一个 `Account` 类管理账户，类里放**三个静态数据成员**：\n\n- `alive_`：当前存活的账户数；\n- `opened_`：历史累计开过户数（只增不减）；\n- `total_`：所有账户余额之和。\n\n支持 5 种指令：`N id bal` 开户、`C id` 销户、`D id amt` 存款、`W id amt` 取款（余额不足则什么也不做）、`Q` 查询。**只有 `Q` 产生输出**，格式：\n\n```text\nalive=2 total=1500 opened=3\n```\n\n★ 为什么这三个数必须是 `static`：它们描述的是「这一类东西的总体状况」，而不是「某个账户自己的状况」。普通成员是每个对象一份，`static` 成员是**全类一份、全体对象共享** —— 建一个账户 `alive_++`，销一个账户 `~Account()` 里 `alive_--`，不用谁去专门维护一个全局表。\n\n★ 构造函数/析构函数是这两个计数器的唯一入口：`alive_` 在构造里加、在析构里减，`opened_` 只在构造里加。这样即使对象是 `new` 出来又 `delete` 掉的，账也永远是平的。\n\n⚠️ 静态数据成员**类内只声明、类外必须定义**：`int Account::alive_ = 0;`。漏了这三行编译能过，**连接**才报 `undefined reference`。\n\n⚠️ 销户时 `total_` 要减去该账户的余额，否则总量永远只涨不跌。",
        "input_format": "第一行 `q`（指令条数）；随后 `q` 行指令，格式见题面。",
        "output_format": "对每条 `Q` 输出一行 `alive=<存活数> total=<余额总和> opened=<历史开户数>`。",
        "constraints_md": "- 1 ≤ q ≤ 10⁵\n- 账户 id 唯一，0 ≤ id ≤ 10⁹\n- 余额与金额 ≤ 10⁹，总和用 `long long`",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 05 讲 · 数据的共享与保护",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <map>\nusing namespace std;\n\nclass Account {\nprivate:\n    int id_;\n    long long balance_;\n    static int alive_;          // 类内声明\n    static int opened_;\n    static long long total_;\npublic:\n    Account(int id, long long bal) : id_(id), balance_(bal) {\n        alive_++;\n        opened_++;\n        total_ += bal;\n    }\n    ~Account() {\n        alive_--;\n        total_ -= balance_;\n    }\n    void deposit(long long amt) { balance_ += amt; total_ += amt; }\n    bool withdraw(long long amt) {\n        if (amt > balance_) return false;\n        balance_ -= amt;\n        total_ -= amt;\n        return true;\n    }\n    static int alive() { return alive_; }\n    static int opened() { return opened_; }\n    static long long total() { return total_; }\n};\n\n// 类外定义并初始化 —— 漏了就连接失败\nint Account::alive_ = 0;\nint Account::opened_ = 0;\nlong long Account::total_ = 0;\n\nint main() {\n    int q;\n    if (scanf(\"%d\", &q) != 1) return 0;\n    map<int, Account*> book;\n    char op[4];\n    for (int i = 0; i < q; i++) {\n        scanf(\"%s\", op);\n        if (op[0] == 'N') {\n            int id; long long bal;\n            scanf(\"%d %lld\", &id, &bal);\n            book[id] = new Account(id, bal);\n        } else if (op[0] == 'C') {\n            int id; scanf(\"%d\", &id);\n            auto it = book.find(id);\n            if (it != book.end()) {\n                delete it->second;          // 析构里把 alive_ / total_ 减回去\n                book.erase(it);\n            }\n        } else if (op[0] == 'D') {\n            int id; long long amt;\n            scanf(\"%d %lld\", &id, &amt);\n            auto it = book.find(id);\n            if (it != book.end()) it->second->deposit(amt);\n        } else if (op[0] == 'W') {\n            int id; long long amt;\n            scanf(\"%d %lld\", &id, &amt);\n            auto it = book.find(id);\n            if (it != book.end()) it->second->withdraw(amt);\n        } else {\n            printf(\"alive=%d total=%lld opened=%d\\n\",\n                   Account::alive(), Account::total(), Account::opened());\n        }\n    }\n    for (auto& kv : book) delete kv.second;\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <map>\nusing namespace std;\n\n// 独立点：不用 new/delete，账户按**值**存进 map<int, Account>，\n// 销户时 erase 掉元素，析构照样自动触发 —— 静态计数器靠「容器管理生命周期」维护，\n// 与参考解的「裸指针 + 手动 delete」是两种对象管理方式。\nclass Account {\n    int id_;\n    long long balance_;\n    static int alive_;\n    static int opened_;\n    static long long total_;\npublic:\n    Account() : id_(0), balance_(0) {}\n    Account(int id, long long bal) : id_(id), balance_(bal) {\n        alive_++; opened_++; total_ += bal;\n    }\n    Account(const Account& o) : id_(o.id_), balance_(o.balance_) {\n        alive_++; total_ += balance_;          // map 拷贝也要记账\n    }\n    ~Account() { alive_--; total_ -= balance_; }\n    void deposit(long long amt) { balance_ += amt; total_ += amt; }\n    bool withdraw(long long amt) {\n        if (amt > balance_) return false;\n        balance_ -= amt; total_ -= amt;\n        return true;\n    }\n    static int alive() { return alive_; }\n    static int opened() { return opened_; }\n    static long long total() { return total_; }\n};\n\nint Account::alive_ = 0;\nint Account::opened_ = 0;\nlong long Account::total_ = 0;\n\nint main() {\n    int q;\n    if (scanf(\"%d\", &q) != 1) return 0;\n    map<int, Account> book;\n    char op[4];\n    for (int i = 0; i < q; i++) {\n        scanf(\"%s\", op);\n        if (op[0] == 'N') {\n            int id; long long bal;\n            scanf(\"%d %lld\", &id, &bal);\n            book.emplace(id, Account(id, bal));\n        } else if (op[0] == 'C') {\n            int id; scanf(\"%d\", &id);\n            book.erase(id);\n        } else if (op[0] == 'D') {\n            int id; long long amt;\n            scanf(\"%d %lld\", &id, &amt);\n            auto it = book.find(id);\n            if (it != book.end()) it->second.deposit(amt);\n        } else if (op[0] == 'W') {\n            int id; long long amt;\n            scanf(\"%d %lld\", &id, &amt);\n            auto it = book.find(id);\n            if (it != book.end()) it->second.withdraw(amt);\n        } else {\n            printf(\"alive=%d total=%lld opened=%d\\n\",\n                   Account::alive(), Account::total(), Account::opened());\n        }\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "6\nN 1 1000\nN 2 500\nD 1 200\nQ\nC 2\nQ\n",
                "expected_stdout": "alive=2 total=1700 opened=2\nalive=1 total=1200 opened=2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\nN 7 0\nC 7\nQ\n",
                "expected_stdout": "alive=0 total=0 opened=1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\nN 1 10\nN 2 20\nW 1 5\nW 1 100\nQ\n",
                "expected_stdout": "alive=2 total=25 opened=2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\nN 5 100\nC 5\nN 5 40\nQ\n",
                "expected_stdout": "alive=1 total=40 opened=2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\nN 1 1\nN 2 2\nD 2 3\nQ\nC 1\nQ\n",
                "expected_stdout": "alive=2 total=6 opened=2\nalive=1 total=5 opened=2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\nN 1000000000 1000000000\nD 1000000000 1000000000\nQ\nC 1000000000\nQ\n",
                "expected_stdout": "alive=1 total=2000000000 opened=1\nalive=0 total=0 opened=1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "string 逐词扫描与最长最短词",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 15,
        "tags": [
            "C++字符串",
            "getline",
            "string",
            "边界处理"
        ],
        "statement_md": "读入**一整行**文本（可能含空格），统计：\n\n1. `len=<字符数> words=<单词数>`\n2. `longest=<单词>(<长度>)` —— 长度并列时取**最先出现**的\n3. `shortest=<单词>(<长度>)` —— 同样取最先出现的\n\n「单词」= 连续的字母或数字，其它字符都算分隔符。没有任何单词时，后两行输出 `longest=-(0)` / `shortest=-(0)`。\n\n★ 为什么必须用 `getline`：`cin >> s` 遇到空格就停，一行 `hello world` 只能读到 `hello`。读整行要用 `getline(cin, line)`。\n\n★ 逐词扫描的骨架（不额外开数组）：\n\n```cpp\nfor (size_t i = 0; i < s.size(); ) {\n    if (!isalnum((unsigned char)s[i])) { i++; continue; }\n    size_t j = i;\n    while (j < s.size() && isalnum((unsigned char)s[j])) j++;\n    string w = s.substr(i, j - i);   // 一个单词\n    i = j;\n}\n```\n\n⚠️ 两个坑：\n1. `isalnum` 的形参要转 `unsigned char`：直接传负的 `char` 是未定义行为（中文/高位字节会踩到）；\n2. `len` 统计的是**整行字符数**，含空格和标点；空行时是 0 而不是 1（`getline` 读到换行为止，换行符不进字符串）。",
        "input_format": "一整行文本（可含空格与标点，ASCII）。",
        "output_format": "三行：`len=.. words=..`、`longest=词(长度)`、`shortest=词(长度)`。",
        "constraints_md": "- 行长 ≤ 10⁵\n- 仅 ASCII 可见字符与空格\n- 单词只由字母和数字组成",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 06 讲 · 数组指针与字符串",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <string>\n#include <cctype>\n#include <iostream>\nusing namespace std;\n\nint main() {\n    string s;\n    if (!getline(cin, s)) return 0;\n\n    int words = 0;\n    string longest, shortest;\n    for (size_t i = 0; i < s.size(); ) {\n        if (!isalnum((unsigned char)s[i])) { i++; continue; }\n        size_t j = i;\n        while (j < s.size() && isalnum((unsigned char)s[j])) j++;\n        string w = s.substr(i, j - i);\n        words++;\n        if (longest.empty() || w.size() > longest.size()) longest = w;\n        if (shortest.empty() || w.size() < shortest.size()) shortest = w;\n        i = j;\n    }\n\n    printf(\"len=%d words=%d\\n\", (int)s.size(), words);\n    if (words == 0) {\n        printf(\"longest=-(0)\\n\");\n        printf(\"shortest=-(0)\\n\");\n    } else {\n        printf(\"longest=%s(%d)\\n\", longest.c_str(), (int)longest.size());\n        printf(\"shortest=%s(%d)\\n\", shortest.c_str(), (int)shortest.size());\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <string>\n#include <vector>\n#include <cctype>\n#include <algorithm>\n#include <iostream>\nusing namespace std;\n\n// 独立点：不手工扫下标 —— 先把所有单词抽进 vector<string>，\n// 再用 std::max_element / min_element 配自定义比较器求最长最短。\n// 参考解是一趟扫描边扫边比，这里是「先收集、再比较」。\nstatic bool isWordChar(char c) { return isalnum((unsigned char)c) != 0; }\n\nint main() {\n    string s;\n    if (!getline(cin, s)) return 0;\n\n    vector<string> ws;\n    size_t i = 0;\n    while (i < s.size()) {\n        while (i < s.size() && !isWordChar(s[i])) i++;\n        size_t j = i;\n        while (j < s.size() && isWordChar(s[j])) j++;\n        if (j > i) ws.push_back(s.substr(i, j - i));\n        i = j;\n    }\n\n    printf(\"len=%d words=%d\\n\", (int)s.size(), (int)ws.size());\n    if (ws.empty()) {\n        printf(\"longest=-(0)\\n\");\n        printf(\"shortest=-(0)\\n\");\n        return 0;\n    }\n    // 严格大于 / 严格小于 => 并列时保留最先出现的那个\n    auto lg = max_element(ws.begin(), ws.end(),\n        [](const string& a, const string& b) { return a.size() < b.size(); });\n    auto sh = min_element(ws.begin(), ws.end(),\n        [](const string& a, const string& b) { return a.size() < b.size(); });\n    printf(\"longest=%s(%d)\\n\", lg->c_str(), (int)lg->size());\n    printf(\"shortest=%s(%d)\\n\", sh->c_str(), (int)sh->size());\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "hello world 123\n",
                "expected_stdout": "len=15 words=3\nlongest=hello(5)\nshortest=123(3)\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "C++ is fun!\n",
                "expected_stdout": "len=11 words=3\nlongest=fun(3)\nshortest=C(1)\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "\n",
                "expected_stdout": "len=0 words=0\nlongest=-(0)\nshortest=-(0)\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "   \n",
                "expected_stdout": "len=3 words=0\nlongest=-(0)\nshortest=-(0)\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "a bb ccc dddd\n",
                "expected_stdout": "len=13 words=4\nlongest=dddd(4)\nshortest=a(1)\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "abc123 456def\n",
                "expected_stdout": "len=13 words=2\nlongest=abc123(6)\nshortest=abc123(6)\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "x\n",
                "expected_stdout": "len=1 words=1\nlongest=x(1)\nshortest=x(1)\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "new 动态数组求最大最小子段和",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "C++数组与指针",
            "动态内存",
            "Kadane",
            "复杂度"
        ],
        "statement_md": "读入 `n` 个整数，求**非空连续子段**的最大和与最小和。\n\n★ 为什么题面强调 `new` / `delete[]`：第 6 讲的核心是「数组名不是指针，但会退化成指针」。要用运行时才定下来的 `n` 开数组，标准做法是 `int* a = new int[n];` …… 用完必须 `delete[] a;` —— **`new[]` 配 `delete[]`**，配错了就是未定义行为。\n\n★ 正解是 Kadane，一遍 O(n)：\n\n```cpp\ncur = max(a[i], cur + a[i]);   // 要么接着上一段，要么从自己重新开始\nbest = max(best, cur);\n```\n\n最小和把比较方向反过来即可（也可以用「取负求最大再取负」，但注意溢出）。\n\n⚠️ 这题的坑几乎全在初始化：\n1. `best` 不能初始化成 0 —— 全是负数时正确答案是「最大的那个负数」，初始化成 0 会输出 0；必须用 `a[0]` 起步；\n2. 子段必须非空，所以不能用「空前缀」当答案；\n3. 累加用 `long long`：本题上界 1000×10⁴ = 10⁷，`int` 还撑得住；但真实数据一上到 10⁵ 就溢出，一律用 64 位是省心的习惯。",
        "input_format": "第一行 `n`；第二行 `n` 个整数。",
        "output_format": "两行：`max=<最大子段和>`、`min=<最小子段和>`。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |aᵢ| ≤ 10⁴\n- 子段非空；结果用 `long long`",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 06 讲 · 数组指针与字符串",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nusing namespace std;\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n\n    // 运行时才知道 n，只能用 new[]；配对释放必须是 delete[]\n    long long* a = new long long[n];\n    for (int i = 0; i < n; i++) scanf(\"%lld\", &a[i]);\n\n    long long curMax = a[0], bestMax = a[0];\n    long long curMin = a[0], bestMin = a[0];\n    for (int i = 1; i < n; i++) {\n        curMax = (curMax + a[i] > a[i]) ? curMax + a[i] : a[i];\n        if (curMax > bestMax) bestMax = curMax;\n        curMin = (curMin + a[i] < a[i]) ? curMin + a[i] : a[i];\n        if (curMin < bestMin) bestMin = curMin;\n    }\n\n    printf(\"max=%lld\\nmin=%lld\\n\", bestMax, bestMin);\n    delete[] a;                       // 与 new[] 配对\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <vector>\n#include <algorithm>\nusing namespace std;\n\n// 独立点：完全不用 Kadane，改成分治 —— 跨中点的最优子段 = 左半最大后缀 + 右半最大前缀。\n// 求最小和时把数组取负做同一套分治再取负回来。\nstruct Node { long long sum, pref, suff, best; };\n\nstatic Node combine(const Node& L, const Node& R) {\n    Node r;\n    r.sum  = L.sum + R.sum;\n    r.pref = max(L.pref, L.sum + R.pref);\n    r.suff = max(R.suff, R.sum + L.suff);\n    r.best = max(max(L.best, R.best), L.suff + R.pref);\n    return r;\n}\n\nstatic Node solve(const vector<long long>& a, int l, int r) {   // [l, r)\n    if (r - l == 1) return {a[l], a[l], a[l], a[l]};\n    int m = (l + r) / 2;\n    return combine(solve(a, l, m), solve(a, m, r));\n}\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    vector<long long> a(n), b(n);\n    for (int i = 0; i < n; i++) { scanf(\"%lld\", &a[i]); b[i] = -a[i]; }\n\n    long long bestMax = solve(a, 0, n).best;\n    long long bestMin = -solve(b, 0, n).best;    // 最小和 = -(取负后的最大和)\n    printf(\"max=%lld\\nmin=%lld\\n\", bestMax, bestMin);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n1 -2 3 4 -1\n",
                "expected_stdout": "max=7\nmin=-2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n-5 -2 -9\n",
                "expected_stdout": "max=-2\nmin=-16\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n7\n",
                "expected_stdout": "max=7\nmin=7\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "6\n2 -8 3 -2 4 -10\n",
                "expected_stdout": "max=5\nmin=-13\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n0 0 0 0\n",
                "expected_stdout": "max=0\nmin=0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8\n10000 -10000 10000 -10000 10000 -10000 10000 -10000\n",
                "expected_stdout": "max=10000\nmin=-10000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "账户派生类的利息结算",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "C++继承",
            "protected",
            "派生类构造",
            "同名遮蔽"
        ],
        "statement_md": "在 `Account` 基类（`id`、`balance`，能存能取、余额不足则取款失败）上派生出两个类：\n\n- `SavingsAccount`：多一个利率 `rate`（**千分比**整数，15 表示 1.5%），提供 `settle(years)`：`利息 = 余额 × rate × years / 1000`（整数除法截断），利息计入余额；\n- `CreditAccount`：多一个透支额度 `limit`，**重写**取款规则：余额可以取到 `-limit` 为止。\n\n指令：`D id amt` 存款、`W id amt` 取款、`Y id years` 结算利息（信用账户输出 `SKIP`）。每条指令输出一行，最后输出 `TOTAL interest=<所有储蓄账户利息之和>`。\n\n★ 为什么余额要放 `protected` 而不是 `private`：派生类的 `settle` 想直接改余额，`private` 的墙连派生类也拦；`protected` 正好是「自己人可进、外人不可进」的折中。（第 7 讲也提醒过：这是继承版的妥协 —— 更干净的办法是让基类提供 `record()`。）\n\n★ 为什么这题不写成 `Account* p = &sa;` 统一调用：本讲**还没有虚函数**，经基类指针调到的永远是基类那一版（静态绑定），信用账户的透支规则会被吃掉 —— 这正是第 8 讲要引入 `virtual` 的原因。\n\n⚠️ 构造链：派生类构造函数必须在**初始化列表**里把 `id/balance` 递给基类，基类构造不接受参数就得自己写默认构造。\n\n⚠️ 利息用**整数**算：先乘后除、截断向下（余额非负，所以等价于向零取整），别用 `double` —— 浮点会有 `0.9999` 这类尾差。",
        "input_format": "第一行 `m`；随后 `m` 行：`S id bal rate` 或 `C id bal limit`。\n接着一行 `q`；随后 `q` 行：`D id amt` / `W id amt` / `Y id years`。",
        "output_format": "每条指令一行：`D id amt -> 余额`、`W id amt -> 余额`（失败为 `W id amt FAILED`）、`Y id years interest=利息 -> 余额`（信用账户为 `Y id years SKIP`）。最后一行 `TOTAL interest=总和`。",
        "constraints_md": "- 1 ≤ m, q ≤ 10⁵\n- 0 ≤ bal, amt, limit ≤ 10⁹\n- 1 ≤ rate ≤ 1000，0 ≤ years ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 07 讲 · 类的继承",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <map>\nusing namespace std;\n\nclass Account {\nprotected:\n    int id_;\n    long long balance_;\n    void record(long long amount) { balance_ += amount; }   // 给派生类留的口子\npublic:\n    Account(int id, long long balance = 0) : id_(id), balance_(balance) {}\n    int id() const { return id_; }\n    long long balance() const { return balance_; }\n    void deposit(long long amount) { record(amount); }\n    bool withdraw(long long amount) {\n        if (amount > balance_) return false;\n        record(-amount);\n        return true;\n    }\n};\n\nclass SavingsAccount : public Account {\nprivate:\n    long long rate_;                    // 千分比\npublic:\n    SavingsAccount(int id, long long balance, long long rate)\n        : Account(id, balance), rate_(rate) {}          // 构造链：参数递给基类\n    long long settle(int years) {\n        long long interest = balance_ * rate_ * years / 1000;\n        record(interest);\n        return interest;\n    }\n};\n\nclass CreditAccount : public Account {\nprivate:\n    long long limit_;\npublic:\n    CreditAccount(int id, long long balance, long long limit)\n        : Account(id, balance), limit_(limit) {}\n    // 同名遮蔽：这是派生类自己的取款规则，经基类指针调不到（本讲还没 virtual）\n    bool withdraw(long long amount) {\n        if (balance_ - amount < -limit_) return false;\n        record(-amount);\n        return true;\n    }\n};\n\nint main() {\n    int m;\n    if (scanf(\"%d\", &m) != 1) return 0;\n    map<int, SavingsAccount*> sav;\n    map<int, CreditAccount*> cre;\n    for (int i = 0; i < m; i++) {\n        char kind[4];\n        int id; long long bal, extra;\n        scanf(\"%s %d %lld %lld\", kind, &id, &bal, &extra);\n        if (kind[0] == 'S') sav[id] = new SavingsAccount(id, bal, extra);\n        else                cre[id] = new CreditAccount(id, bal, extra);\n    }\n\n    int q;\n    scanf(\"%d\", &q);\n    long long totalInterest = 0;\n    char op[4];\n    for (int i = 0; i < q; i++) {\n        scanf(\"%s\", op);\n        int id;\n        scanf(\"%d\", &id);\n        if (op[0] == 'D') {\n            long long amt;\n            scanf(\"%lld\", &amt);\n            auto s = sav.find(id);\n            if (s != sav.end()) { s->second->deposit(amt); printf(\"D %d %lld -> %lld\\n\", id, amt, s->second->balance()); }\n            else { auto c = cre.find(id); c->second->deposit(amt); printf(\"D %d %lld -> %lld\\n\", id, amt, c->second->balance()); }\n        } else if (op[0] == 'W') {\n            long long amt;\n            scanf(\"%lld\", &amt);\n            bool ok;\n            long long now;\n            auto s = sav.find(id);\n            if (s != sav.end()) { ok = s->second->withdraw(amt); now = s->second->balance(); }\n            else { auto c = cre.find(id); ok = c->second->withdraw(amt); now = c->second->balance(); }\n            if (ok) printf(\"W %d %lld -> %lld\\n\", id, amt, now);\n            else    printf(\"W %d %lld FAILED\\n\", id, amt);\n        } else {\n            int years;\n            scanf(\"%d\", &years);\n            auto s = sav.find(id);\n            if (s == sav.end()) {\n                printf(\"Y %d %d SKIP\\n\", id, years);\n            } else {\n                long long in = s->second->settle(years);\n                totalInterest += in;\n                printf(\"Y %d %d interest=%lld -> %lld\\n\", id, years, in, s->second->balance());\n            }\n        }\n    }\n    printf(\"TOTAL interest=%lld\\n\", totalInterest);\n    for (auto& kv : sav) delete kv.second;\n    for (auto& kv : cre) delete kv.second;\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <map>\nusing namespace std;\n\n// 独立点：账户**按值**放进容器（不开堆、不 delete），且把「利息累计」交给\n// 一个独立的累加器结构，而不是 main 里的裸变量。\n// 类层次与语义完全一致，只是对象管理方式换了。\nclass Account {\nprotected:\n    int id_;\n    long long balance_;\n    void record(long long amount) { balance_ += amount; }\npublic:\n    Account(int id = 0, long long balance = 0) : id_(id), balance_(balance) {}\n    long long balance() const { return balance_; }\n    void deposit(long long amount) { record(amount); }\n    bool withdraw(long long amount) {\n        if (amount > balance_) return false;\n        record(-amount);\n        return true;\n    }\n};\n\nclass SavingsAccount : public Account {\n    long long rate_;\npublic:\n    SavingsAccount(int id = 0, long long balance = 0, long long rate = 0)\n        : Account(id, balance), rate_(rate) {}\n    long long settle(int years) {\n        long long interest = balance_ * rate_ * years / 1000;\n        record(interest);\n        return interest;\n    }\n};\n\nclass CreditAccount : public Account {\n    long long limit_;\npublic:\n    CreditAccount(int id = 0, long long balance = 0, long long limit = 0)\n        : Account(id, balance), limit_(limit) {}\n    bool withdraw(long long amount) {\n        if (balance_ - amount < -limit_) return false;\n        record(-amount);\n        return true;\n    }\n};\n\nint main() {\n    int m;\n    if (scanf(\"%d\", &m) != 1) return 0;\n    map<int, SavingsAccount> sav;\n    map<int, CreditAccount> cre;\n    for (int i = 0; i < m; i++) {\n        char kind[4];\n        int id; long long bal, extra;\n        scanf(\"%s %d %lld %lld\", kind, &id, &bal, &extra);\n        if (kind[0] == 'S') sav[id] = SavingsAccount(id, bal, extra);\n        else                cre[id] = CreditAccount(id, bal, extra);\n    }\n\n    int q;\n    scanf(\"%d\", &q);\n    long long totalInterest = 0;\n    char op[4];\n    for (int i = 0; i < q; i++) {\n        scanf(\"%s\", op);\n        int id; scanf(\"%d\", &id);\n        if (op[0] == 'Y') {\n            int years; scanf(\"%d\", &years);\n            auto s = sav.find(id);\n            if (s == sav.end()) { printf(\"Y %d %d SKIP\\n\", id, years); continue; }\n            long long in = s->second.settle(years);\n            totalInterest += in;\n            printf(\"Y %d %d interest=%lld -> %lld\\n\", id, years, in, s->second.balance());\n            continue;\n        }\n        long long amt; scanf(\"%lld\", &amt);\n        auto s = sav.find(id);\n        if (op[0] == 'D') {\n            if (s != sav.end()) s->second.deposit(amt);\n            else cre[id].deposit(amt);\n            printf(\"D %d %lld -> %lld\\n\", id, amt,\n                   s != sav.end() ? s->second.balance() : cre[id].balance());\n        } else {\n            bool ok; long long now;\n            if (s != sav.end()) { ok = s->second.withdraw(amt); now = s->second.balance(); }\n            else { ok = cre[id].withdraw(amt); now = cre[id].balance(); }\n            if (ok) printf(\"W %d %lld -> %lld\\n\", id, amt, now);\n            else    printf(\"W %d %lld FAILED\\n\", id, amt);\n        }\n    }\n    printf(\"TOTAL interest=%lld\\n\", totalInterest);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "2\nS 1 10000 15\nC 2 0 5000\n6\nD 1 1000\nW 2 3000\nW 2 3000\nY 1 1\nY 2 1\nW 1 200\n",
                "expected_stdout": "D 1 1000 -> 11000\nW 2 3000 -> -3000\nW 2 3000 FAILED\nY 1 1 interest=165 -> 11165\nY 2 1 SKIP\nW 1 200 -> 10965\nTOTAL interest=165\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\nS 9 100 1000\n2\nY 9 2\nW 9 1\n",
                "expected_stdout": "Y 9 2 interest=200 -> 300\nW 9 1 -> 299\nTOTAL interest=200\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\nC 4 100 0\n3\nW 4 100\nW 4 1\nD 4 5\n",
                "expected_stdout": "W 4 100 -> 0\nW 4 1 FAILED\nD 4 5 -> 5\nTOTAL interest=0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\nS 1 0 500\nS 2 1000 1\n4\nY 1 3\nY 2 7\nD 1 250\nY 1 4\n",
                "expected_stdout": "Y 1 3 interest=0 -> 0\nY 2 7 interest=7 -> 1007\nD 1 250 -> 250\nY 1 4 interest=500 -> 750\nTOTAL interest=507\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\nS 5 999 333\n2\nY 5 1\nY 5 3\n",
                "expected_stdout": "Y 5 1 interest=332 -> 1331\nY 5 3 interest=1329 -> 2660\nTOTAL interest=1661\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\nC 1 10 20\nS 2 20 25\n5\nW 1 30\nW 1 31\nY 2 4\nD 1 100\nW 1 130\n",
                "expected_stdout": "W 1 30 -> -20\nW 1 31 FAILED\nY 2 4 interest=2 -> 22\nD 1 100 -> 80\nW 1 130 FAILED\nTOTAL interest=2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "复数类的运算符重载",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "C++多态性",
            "运算符重载",
            "友元",
            "常成员函数"
        ],
        "statement_md": "实现 `Complex` 类（实部、虚部都是**整数**），重载 `+`、`*`、`==` 和 `<<`，读入 `n` 个复数，输出：\n\n```text\nsum=(a, b)\nprod=(a, b)\neq=0\n```\n\n`sum` 是全部相加，`prod` 是全部相乘（乘法的单位元是 `1+0i`），`eq` 表示两者是否相等。输出格式固定为 `(实部, 虚部)` —— **逗号后有一个空格**。\n\n★ 为什么 `operator<<` 必须是**非成员**函数：`cout << c` 的左操作数是 `ostream`，而成员版的左操作数只能是本类对象。想给 `ostream` 加成员函数是不可能的，所以只能写成 `ostream& operator<<(ostream&, const Complex&)`；要读私有成员就在类里写 `friend` 声明 —— 友元不是可选项。\n\n★ `+` 和 `*` 写成**成员**函数：左操作数天然是 `*this`，右操作数是形参。但 `1 + c` 这种「整数在左边」的写法成员版接不住（`1` 不是 Complex），要支持就得再加非成员版重载 —— 本题不要求。\n\n⚠️ 乘法公式别记错：`(a+bi)(c+di) = (ac−bd) + (ad+bc)i`。写成 `ac+bd` 是最常见的错。\n\n⚠️ 返回类型：`+` / `*` 返回**新对象**（不能返回引用，局部对象出了函数就没了）；`==` 返回 `bool` 且必须是 `const` 成员函数，否则常对象调不了。",
        "input_format": "第一行 `n`；随后 `n` 行，每行两个整数 `a b`（表示 `a+bi`）。",
        "output_format": "三行：`sum=(实部, 虚部)`、`prod=(实部, 虚部)`、`eq=0/1`。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- |a|, |b| ≤ 100\n- 结果 ∣实部∣、∣虚部∣ < 10¹⁴，用 `long long`",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 08 讲 · 多态性",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <iostream>\nusing namespace std;\n\nclass Complex {\nprivate:\n    long long real_, imag_;\npublic:\n    Complex(long long r = 0, long long i = 0) : real_(r), imag_(i) {}\n\n    // 双目 +：左操作数是 *this\n    Complex operator+(const Complex& o) const {\n        return Complex(real_ + o.real_, imag_ + o.imag_);\n    }\n    Complex operator*(const Complex& o) const {\n        return Complex(real_ * o.real_ - imag_ * o.imag_,\n                       real_ * o.imag_ + imag_ * o.real_);\n    }\n    bool operator==(const Complex& o) const {\n        return real_ == o.real_ && imag_ == o.imag_;\n    }\n    // 非成员版必须声明为友元才能读私有成员\n    friend ostream& operator<<(ostream& os, const Complex& c);\n};\n\nostream& operator<<(ostream& os, const Complex& c) {\n    os << \"(\" << c.real_ << \", \" << c.imag_ << \")\";\n    return os;                 // 返回流本身才能连锁 <<\n}\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    Complex sum(0, 0), prod(1, 0);\n    for (int i = 0; i < n; i++) {\n        long long a, b;\n        scanf(\"%lld %lld\", &a, &b);\n        Complex c(a, b);\n        sum = sum + c;\n        prod = prod * c;\n    }\n    cout << \"sum=\" << sum << '\\n';\n    cout << \"prod=\" << prod << '\\n';\n    cout << \"eq=\" << (sum == prod ? 1 : 0) << '\\n';\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <iostream>\n#include <vector>\nusing namespace std;\n\n// 独立点：所有运算符都写成**非成员**的友元函数（参考解是成员版 + 一个非成员 <<），\n// 并且把累加/累乘交给 std::accumulate 的 lambda，不手写循环。\nclass Complex {\n    long long real_, imag_;\npublic:\n    Complex(long long r = 0, long long i = 0) : real_(r), imag_(i) {}\n    long long real() const { return real_; }\n    long long imag() const { return imag_; }\n    friend Complex operator+(const Complex& a, const Complex& b);\n    friend Complex operator*(const Complex& a, const Complex& b);\n    friend bool operator==(const Complex& a, const Complex& b);\n    friend ostream& operator<<(ostream& os, const Complex& c);\n};\n\nComplex operator+(const Complex& a, const Complex& b) {\n    return Complex(a.real_ + b.real_, a.imag_ + b.imag_);\n}\nComplex operator*(const Complex& a, const Complex& b) {\n    return Complex(a.real_ * b.real_ - a.imag_ * b.imag_,\n                   a.real_ * b.imag_ + a.imag_ * b.real_);\n}\nbool operator==(const Complex& a, const Complex& b) {\n    return a.real_ == b.real_ && a.imag_ == b.imag_;\n}\nostream& operator<<(ostream& os, const Complex& c) {\n    os << \"(\" << c.real_ << \", \" << c.imag_ << \")\";\n    return os;\n}\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    vector<Complex> v;\n    for (int i = 0; i < n; i++) {\n        long long a, b;\n        scanf(\"%lld %lld\", &a, &b);\n        v.push_back(Complex(a, b));\n    }\n\n    Complex sum(0, 0), prod(1, 0);\n    for (size_t i = 0; i < v.size(); i++) { sum = sum + v[i]; prod = prod * v[i]; }\n\n    cout << \"sum=\" << sum << '\\n';\n    cout << \"prod=\" << prod << '\\n';\n    cout << \"eq=\" << (sum == prod ? 1 : 0) << '\\n';\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "2\n1 2\n3 4\n",
                "expected_stdout": "sum=(4, 6)\nprod=(-5, 10)\neq=0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n5 -3\n",
                "expected_stdout": "sum=(5, -3)\nprod=(5, -3)\neq=1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n1 0\n0 1\n1 1\n",
                "expected_stdout": "sum=(2, 2)\nprod=(-1, 1)\neq=0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n0 0\n0 0\n",
                "expected_stdout": "sum=(0, 0)\nprod=(0, 0)\neq=1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n1 1\n1 -1\n",
                "expected_stdout": "sum=(2, 0)\nprod=(2, 0)\neq=1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n-100 100\n100 -100\n-1 -1\n2 2\n",
                "expected_stdout": "sum=(1, 1)\nprod=(80000, 0)\neq=0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "抽象图形类的虚函数面积求和",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 25,
        "tags": [
            "C++多态性",
            "虚函数",
            "抽象类",
            "虚析构"
        ],
        "statement_md": "定义**抽象类** `Shape`：`virtual long long area() const = 0;`、`virtual const char* name() const = 0;`、`virtual ~Shape() {}`。派生出三个具体类：\n\n| 类型 | 输入 | 面积 | `name()` |\n|---|---|---|---|\n| `R w h` | 矩形 | `w × h` | `Rect` |\n| `S s` | 正方形 | `s × s` | `Square` |\n| `T b h` | 直角三角形 | `b × h / 2` | `Tri` |\n\n把对象**用 `Shape*` 存进 `vector<Shape*>`**，只用基类指针遍历算总面积、找面积最大的图形（并列取**最先出现**的那个），最后统计各类个数。\n\n★ 为什么必须 `virtual`：`Shape* p` 的静态类型是 `Shape`，没有 `virtual` 时编译器只能按声明类型绑定到 `Shape::area()` —— 而它是纯虚的，根本调不了。加了 `virtual` 才会在运行期按**实际类型**查表（vtable）分派。\n\n★ 为什么基类要 `virtual ~Shape()`：最后 `delete` 这些指针时，若析构不是虚的，只析构 `Shape` 那部分，派生类的成员全泄漏。「有虚函数的类就该有虚析构」是硬规矩。\n\n⚠️ 边界：\n1. `T` 的 `b×h` 保证是偶数，面积是整数，不会出现 0.5；\n2. 面积相同的图形可能有多个，取**先出现**的，别用 `>=` 更新；\n3. 面积用 `long long`：`w,h` 可到 10⁹，乘积到 10¹⁸。",
        "input_format": "第一行 `q`；随后 `q` 行，每行 `R w h` / `S s` / `T b h`。",
        "output_format": "三行：`total=<总面积>`、`max=<类名> <面积>`、`count R=<矩形数> S=<正方形数> T=<三角形数>`。",
        "constraints_md": "- 1 ≤ q ≤ 10⁵\n- 1 ≤ w, h, s ≤ 10⁹（`T` 的 `b×h` 为偶数）\n- 面积用 `long long`",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 08 讲 · 多态性",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <vector>\nusing namespace std;\n\nclass Shape {\npublic:\n    virtual long long area() const = 0;         // 纯虚：只定合同\n    virtual const char* name() const = 0;\n    virtual ~Shape() {}                         // 虚析构：经基类指针 delete 才安全\n};\n\nclass Rect : public Shape {\n    long long w_, h_;\npublic:\n    Rect(long long w, long long h) : w_(w), h_(h) {}\n    long long area() const override { return w_ * h_; }\n    const char* name() const override { return \"Rect\"; }\n};\n\nclass Square : public Shape {\n    long long s_;\npublic:\n    explicit Square(long long s) : s_(s) {}\n    long long area() const override { return s_ * s_; }\n    const char* name() const override { return \"Square\"; }\n};\n\nclass Tri : public Shape {\n    long long b_, h_;\npublic:\n    Tri(long long b, long long h) : b_(b), h_(h) {}\n    long long area() const override { return b_ * h_ / 2; }\n    const char* name() const override { return \"Tri\"; }\n};\n\nint main() {\n    int q;\n    if (scanf(\"%d\", &q) != 1) return 0;\n\n    vector<Shape*> shapes;\n    int cr = 0, cs = 0, ct = 0;\n    for (int i = 0; i < q; i++) {\n        char kind[4];\n        long long a, b = 0;\n        scanf(\"%s %lld\", kind, &a);\n        if (kind[0] == 'S') {\n            shapes.push_back(new Square(a)); cs++;\n        } else {\n            scanf(\"%lld\", &b);\n            if (kind[0] == 'R') { shapes.push_back(new Rect(a, b)); cr++; }\n            else                { shapes.push_back(new Tri(a, b)); ct++; }\n        }\n    }\n\n    long long total = 0;\n    int best = 0;\n    for (int i = 0; i < (int)shapes.size(); i++) {\n        long long ar = shapes[i]->area();       // 动态绑定\n        total += ar;\n        if (ar > shapes[best]->area()) best = i;   // 严格大于：并列取先出现的\n    }\n\n    printf(\"total=%lld\\n\", total);\n    printf(\"max=%s %lld\\n\", shapes[best]->name(), shapes[best]->area());\n    printf(\"count R=%d S=%d T=%d\\n\", cr, cs, ct);\n\n    for (Shape* p : shapes) delete p;           // 虚析构保证派生类部分也释放\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <vector>\n#include <memory>\n#include <algorithm>\nusing namespace std;\n\n// 独立点：容器用 vector<unique_ptr<Shape>> 管生命周期（不手写 delete），\n// 最大值改用 std::max_element + 自定义比较器（比较 area()）。\n// 类层次相同，但「谁负责释放」和「怎么找最大」都换了实现。\nclass Shape {\npublic:\n    virtual long long area() const = 0;\n    virtual const char* name() const = 0;\n    virtual ~Shape() = default;\n};\n\nstruct Rect : Shape {\n    long long w, h;\n    Rect(long long a, long long b) : w(a), h(b) {}\n    long long area() const override { return w * h; }\n    const char* name() const override { return \"Rect\"; }\n};\nstruct Square : Shape {\n    long long s;\n    explicit Square(long long a) : s(a) {}\n    long long area() const override { return s * s; }\n    const char* name() const override { return \"Square\"; }\n};\nstruct Tri : Shape {\n    long long b, h;\n    Tri(long long x, long long y) : b(x), h(y) {}\n    long long area() const override { return b * h / 2; }\n    const char* name() const override { return \"Tri\"; }\n};\n\nint main() {\n    int q;\n    if (scanf(\"%d\", &q) != 1) return 0;\n\n    vector<unique_ptr<Shape>> shapes;\n    int cr = 0, cs = 0, ct = 0;\n    for (int i = 0; i < q; i++) {\n        char kind[4];\n        long long a, b = 0;\n        scanf(\"%s %lld\", kind, &a);\n        if (kind[0] == 'S') { shapes.emplace_back(new Square(a)); cs++; }\n        else {\n            scanf(\"%lld\", &b);\n            if (kind[0] == 'R') { shapes.emplace_back(new Rect(a, b)); cr++; }\n            else                { shapes.emplace_back(new Tri(a, b)); ct++; }\n        }\n    }\n\n    long long total = 0;\n    for (auto& p : shapes) total += p->area();\n    auto best = max_element(shapes.begin(), shapes.end(),\n        [](const unique_ptr<Shape>& x, const unique_ptr<Shape>& y) {\n            return x->area() < y->area();          // 严格小于 => 并列留第一个\n        });\n\n    printf(\"total=%lld\\n\", total);\n    printf(\"max=%s %lld\\n\", (*best)->name(), (*best)->area());\n    printf(\"count R=%d S=%d T=%d\\n\", cr, cs, ct);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\nR 2 3\nS 2\nT 4 3\n",
                "expected_stdout": "total=16\nmax=Rect 6\ncount R=1 S=1 T=1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\nS 7\n",
                "expected_stdout": "total=49\nmax=Square 49\ncount R=0 S=1 T=0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\nR 1 1\nS 1\nT 2 1\nR 1 1\n",
                "expected_stdout": "total=4\nmax=Rect 1\ncount R=2 S=1 T=1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\nT 2 3\nR 3 1\nS 1\n",
                "expected_stdout": "total=7\nmax=Tri 3\ncount R=1 S=1 T=1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\nR 1000000000 1000000000\nS 999999999\n",
                "expected_stdout": "total=1999999998000000001\nmax=Rect 1000000000000000000\ncount R=1 S=1 T=0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\nS 2\nR 2 2\nT 4 2\nR 2 2\nT 8 1\n",
                "expected_stdout": "total=20\nmax=Square 4\ncount R=2 S=1 T=2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "类模板 Stack 求逆波兰表达式",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 25,
        "tags": [
            "C++模板",
            "类模板",
            "栈",
            "后缀表达式"
        ],
        "statement_md": "把讲义里的栈类模板化：`template <typename T> class Stack`，支持 `push` / `pop` / `size`，容量不够时自动翻倍。然后用 `Stack<long long>` 求一个**后缀（逆波兰）表达式**的值，同时统计过程中栈达到过的最大深度。\n\n输入是一串 token：整数或 `+ - * /`。除法保证能整除、除数不为 0。\n\n★ 为什么这题适合用类模板：求值本身与「存什么类型」无关，同一份 `Stack<T>` 既能装 `int`、`long long`，也能装 `char`（拿去写括号匹配）。模板不是运行期的东西，是**给编译器的图纸** —— 你写 `Stack<long long>` 时，编译器才照着图纸生成一个专门的类。\n\n★ 类模板的两个硬规矩：\n1. 使用时**必须显式**给类型参数（`Stack<long long> st;`），编译器推不出来；\n2. 成员函数在类外定义时要写两遍前缀：`template <typename T>` + `Stack<T>::`。\n\n⚠️ 求值的减法和除法**不能交换**：先弹出的是右操作数 `b`，后弹出的是左操作数 `a`，算的是 `a - b`、`a / b`。反了就是 `b - a`，一半用例会错得莫名其妙。\n\n⚠️ 栈的 `pop` 建议写成 `bool pop(T& out)`：空栈返回 false，而不是让调用方去猜。",
        "input_format": "第一行 `q`（token 个数）；随后 `q` 个 token，空格或换行分隔。",
        "output_format": "两行：`value=<表达式的值>`、`maxdepth=<过程中栈的最大深度>`。",
        "constraints_md": "- 1 ≤ q ≤ 10⁵\n- 保证表达式合法；除法整除、除数非 0\n- 结果与中间值用 `long long`",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 09 讲 · 模板与群体数据",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <string>\n#include <iostream>\n#include <cstdlib>\nusing namespace std;\n\ntemplate <typename T>\nclass Stack {\nprivate:\n    T* data_;\n    int top_, cap_;\n    void grow() {\n        int nc = cap_ * 2;\n        T* nd = new T[nc];\n        for (int i = 0; i < top_; i++) nd[i] = data_[i];\n        delete[] data_;\n        data_ = nd;\n        cap_ = nc;\n    }\npublic:\n    explicit Stack(int cap = 8) : data_(new T[cap]), top_(0), cap_(cap) {}\n    ~Stack() { delete[] data_; }\n    Stack(const Stack&) = delete;               // 含裸指针，禁止浅复制\n    Stack& operator=(const Stack&) = delete;\n\n    void push(const T& e) {\n        if (top_ == cap_) grow();\n        data_[top_++] = e;\n    }\n    bool pop(T& out) {\n        if (top_ == 0) return false;\n        out = data_[--top_];\n        return true;\n    }\n    int size() const { return top_; }\n    bool empty() const { return top_ == 0; }\n};\n\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n\n    int q;\n    if (!(cin >> q)) return 0;\n\n    Stack<long long> st;\n    int maxDepth = 0;\n    for (int i = 0; i < q; i++) {\n        string tok;\n        cin >> tok;\n        if (tok.size() == 1 && (tok[0] == '+' || tok[0] == '-' ||\n                                tok[0] == '*' || tok[0] == '/')) {\n            long long b = 0, a = 0;\n            st.pop(b);\n            st.pop(a);\n            long long r = 0;\n            if (tok[0] == '+') r = a + b;\n            else if (tok[0] == '-') r = a - b;\n            else if (tok[0] == '*') r = a * b;\n            else r = a / b;                     // 保证整除\n            st.push(r);\n        } else {\n            st.push(atoll(tok.c_str()));\n            if (st.size() > maxDepth) maxDepth = st.size();\n        }\n    }\n\n    long long v = 0;\n    st.pop(v);\n    printf(\"value=%lld\\n\", v);\n    printf(\"maxdepth=%d\\n\", maxDepth);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <vector>\n#include <string>\n#include <iostream>\n#include <cstdlib>\nusing namespace std;\n\n// 独立点：类模板内部换成 std::vector<T> 当存储（不自己 new[]/delete[]），\n// 求值循环改用「双栈 + 显式长度记录」的写法，输出口径不变。\ntemplate <typename T>\nclass Stack {\n    vector<T> v_;\npublic:\n    void push(const T& e) { v_.push_back(e); }\n    bool pop(T& out) {\n        if (v_.empty()) return false;\n        out = v_.back();\n        v_.pop_back();\n        return true;\n    }\n    int size() const { return (int)v_.size(); }\n    bool empty() const { return v_.empty(); }\n};\n\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n\n    int q;\n    if (!(cin >> q)) return 0;\n\n    Stack<long long> operands;\n    int maxDepth = 0;\n    for (int i = 0; i < q; i++) {\n        string tok;\n        cin >> tok;\n        char c = tok.size() == 1 ? tok[0] : '\\0';\n        if (c == '+' || c == '-' || c == '*' || c == '/') {\n            long long b, a;\n            operands.pop(b);\n            operands.pop(a);\n            switch (c) {\n                case '+': operands.push(a + b); break;\n                case '-': operands.push(a - b); break;\n                case '*': operands.push(a * b); break;\n                default:  operands.push(a / b); break;\n            }\n        } else {\n            operands.push(strtoll(tok.c_str(), nullptr, 10));\n            if (operands.size() > maxDepth) maxDepth = operands.size();\n        }\n    }\n\n    long long v;\n    operands.pop(v);\n    printf(\"value=%lld\\n\", v);\n    printf(\"maxdepth=%d\\n\", maxDepth);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n2 3 +\n",
                "expected_stdout": "value=5\nmaxdepth=2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n2 3 + 4 *\n",
                "expected_stdout": "value=20\nmaxdepth=2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "7\n5 1 2 + 4 * + 3 -\n",
                "expected_stdout": "value=17\nmaxdepth=3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n42\n",
                "expected_stdout": "value=42\nmaxdepth=1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n-8 2 / -3 +\n",
                "expected_stdout": "value=-7\nmaxdepth=2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7\n1000000 1000000 * 1000000 * 2 /\n",
                "expected_stdout": "value=500000000000000000\nmaxdepth=2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "map 词频榜（同频按字典序）",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "STL",
            "map",
            "排序",
            "lambda"
        ],
        "statement_md": "读入一行文本，统计每个单词出现的次数（**统一转小写**，单词 = 连续的字母或数字），输出出现次数最多的前 `k` 个：次数相同的按**字典序升序**排。\n\n每行输出 `单词 次数`（一个空格）。不同单词少于 `k` 个时，有多少输出多少。\n\n★ 为什么用 `map<string,int>` 计数：`map` 是红黑树，键天然有序且插入/查找 O(log n)，`++cnt[w]` 一行就完成「没有就插入 0 再自增」。（顺带记住讲义 10.5 的坑：`cnt[w]` **查询也会插入**，只想查就改用 `find`。）\n\n★ 排序为什么要拷进 `vector`：`map` 只能按键排，本题要按**值**排，所以先把 `(词, 次数)` 拷进 `vector<pair<string,int>>` 再 `sort`，比较器写成\n\n```cpp\n[](const auto& a, const auto& b) {\n    if (a.second != b.second) return a.second > b.second;  // 次数降序\n    return a.first < b.first;                              // 同频字典序升序\n}\n```\n\n⚠️ 只用「次数降序」一个键是错的：同频时 `sort` 不保证顺序（不稳定），结果会随实现变化 —— 必须把字典序写成第二关键字。\n\n⚠️ `k` 可能大于不同单词数，输出时要取 `min(k, size)`，别越界。",
        "input_format": "第一行 `k`；第二行起是文本（可能含多行，读到 EOF）。",
        "output_format": "最多 `k` 行，每行 `单词 次数`。",
        "constraints_md": "- 1 ≤ k ≤ 1000\n- 文本总长 ≤ 10⁵\n- 单词只由字母数字组成，比较时不区分大小写",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 10 讲 · 泛型程序设计与STL",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <string>\n#include <map>\n#include <vector>\n#include <algorithm>\n#include <cctype>\n#include <iostream>\nusing namespace std;\n\nint main() {\n    int k;\n    if (scanf(\"%d\", &k) != 1) return 0;\n\n    map<string, int> cnt;\n    string w;\n    char ch;\n    bool inWord = false;\n    string cur;\n    while (cin.get(ch)) {\n        if (isalnum((unsigned char)ch)) {\n            cur.push_back((char)tolower((unsigned char)ch));\n            inWord = true;\n        } else if (inWord) {\n            cnt[cur]++;\n            cur.clear();\n            inWord = false;\n        }\n    }\n    if (inWord) cnt[cur]++;\n\n    vector<pair<string, int>> v(cnt.begin(), cnt.end());\n    sort(v.begin(), v.end(), [](const pair<string, int>& a, const pair<string, int>& b) {\n        if (a.second != b.second) return a.second > b.second;   // 次数降序\n        return a.first < b.first;                               // 同频字典序升序\n    });\n\n    int lim = min<int>(k, (int)v.size());\n    for (int i = 0; i < lim; i++)\n        printf(\"%s %d\\n\", v[i].first.c_str(), v[i].second);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <string>\n#include <map>\n#include <set>\n#include <cctype>\n#include <iostream>\nusing namespace std;\n\n// 独立点：不用 vector + sort —— 把 (次数取负, 单词) 塞进 std::set，\n// 靠 set 自身的红黑树排序直接按「次数降序、字典序升序」取出，天然不需要比较器。\nint main() {\n    int k;\n    if (scanf(\"%d\", &k) != 1) return 0;\n\n    map<string, int> cnt;\n    string cur;\n    char ch;\n    bool inWord = false;\n    while (cin.get(ch)) {\n        if (isalnum((unsigned char)ch)) {\n            cur.push_back((char)tolower((unsigned char)ch));\n            inWord = true;\n        } else if (inWord) {\n            cnt[cur]++;\n            cur.clear();\n            inWord = false;\n        }\n    }\n    if (inWord) cnt[cur]++;\n\n    set<pair<int, string>> ranked;\n    for (auto& kv : cnt) ranked.insert({-kv.second, kv.first});\n\n    int printed = 0;\n    for (auto& p : ranked) {\n        if (printed++ >= k) break;\n        printf(\"%s %d\\n\", p.second.c_str(), -p.first);\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\nthe quick brown fox the lazy dog the end\n",
                "expected_stdout": "the 3\nbrown 1\ndog 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\nApple apple APPLE banana\n",
                "expected_stdout": "apple 3\nbanana 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\none two three\n",
                "expected_stdout": "one 1\nthree 1\ntwo 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\nb a c b a b\n",
                "expected_stdout": "b 3\na 2\nc 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\nx1 x2 x1-x2 x1\n",
                "expected_stdout": "x1 3\nx2 2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\nA b C d a B c D\n",
                "expected_stdout": "a 2\nb 2\nc 2\nd 2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "vector 排序去重（unique-erase）",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "STL",
            "vector",
            "sort",
            "unique-erase"
        ],
        "statement_md": "读入 `n` 个整数，输出去重并升序后的结果，同时报告读入个数与去重后的个数。\n\n```text\nread=7\nunique=4\n1 3 5 9\n```\n\n★ 为什么标准套路是「先 `sort` 再 `unique` 再 `erase`」：\n`std::unique` 只删除**相邻**的重复元素，它不会把整个容器扫一遍去重。所以必须先排序把相等的元素赶到一起，否则 `1 2 1` 里的两个 1 根本不相邻，`unique` 一个都不会删。\n\n★ `unique` 的返回值是「新的逻辑末尾」迭代器，它**不改变容器大小** —— 后面那些元素还在，只是内容不确定。所以第三刀 `erase(newEnd, end())` 才是必须的。漏掉 `erase` 时 `v.size()` 还是原来的 `n`，这是最经典的错。\n\n★ 另一种写法是 `set<int>`：插入自动去重又天然有序，代价是每个元素一次 O(log n) 的树插入、常数更大。`vector` 的 `sort`+`unique` 是 O(n log n) 但常数小得多，且内存连续 —— 这就是为什么大数据量下更推荐后者。\n\n⚠️ `n = 1` 时 `unique` 返回 `begin()+1`，`erase` 空区间也完全合法；别为它单开分支。",
        "input_format": "第一行 `n`；第二行 `n` 个整数。",
        "output_format": "三行：`read=<n>`、`unique=<k>`、去重升序后的序列（空格分隔）。",
        "constraints_md": "- 1 ≤ n ≤ 10⁵\n- |aᵢ| ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 10 讲 · 泛型程序设计与STL",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <vector>\n#include <algorithm>\nusing namespace std;\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n\n    vector<int> v(n);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &v[i]);\n\n    sort(v.begin(), v.end());                       // 第一刀：让相等元素相邻\n    auto tail = unique(v.begin(), v.end());         // 第二刀：相邻去重，返回新末尾\n    v.erase(tail, v.end());                         // 第三刀：真正删掉尾巴\n\n    printf(\"read=%d\\n\", n);\n    printf(\"unique=%d\\n\", (int)v.size());\n    for (size_t i = 0; i < v.size(); i++) {\n        if (i) putchar(' ');\n        printf(\"%d\", v[i]);\n    }\n    putchar('\\n');\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <set>\nusing namespace std;\n\n// 独立点：完全不碰 vector/unique —— 直接往 std::set 里塞，\n// 红黑树自动去重 + 自动升序，最后顺序遍历输出。\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    set<int> s;\n    for (int i = 0; i < n; i++) {\n        int x;\n        scanf(\"%d\", &x);\n        s.insert(x);\n    }\n\n    printf(\"read=%d\\n\", n);\n    printf(\"unique=%d\\n\", (int)s.size());\n    bool first = true;\n    for (int x : s) {\n        if (!first) putchar(' ');\n        printf(\"%d\", x);\n        first = false;\n    }\n    putchar('\\n');\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "7\n3 1 2 3 1 5 2\n",
                "expected_stdout": "read=7\nunique=4\n1 2 3 5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n42\n",
                "expected_stdout": "read=1\nunique=1\n42\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n-1 -1 0 0 1\n",
                "expected_stdout": "read=5\nunique=3\n-1 0 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n9 9 9 9\n",
                "expected_stdout": "read=4\nunique=1\n9\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n1000000000 -1000000000 0 0 -1 1\n",
                "expected_stdout": "read=6\nunique=5\n-1000000000 -1 0 1 1000000000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8\n5 4 3 2 1 2 3 4\n",
                "expected_stdout": "read=8\nunique=5\n1 2 3 4 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "setw 与 fixed 的报表对齐",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 20,
        "tags": [
            "C++流类库",
            "iomanip",
            "setw",
            "fixed"
        ],
        "statement_md": "读入 `n` 条商品记录（名称、数量、单价），输出一张对齐的报表，最后加一行合计。格式要求：\n\n- 名称**左对齐**，宽度 10；\n- 数量**右对齐**，宽度 6；\n- 金额**右对齐**，宽度 12，`fixed` + 保留 **2 位小数**；\n- 单价以「分」为单位给出，金额 = 数量 × 单价 ÷ 100（元）。\n\n表头是 `name`、`qty`、`amount`，合计行的名称列写 `TOTAL`。\n\n★ `setw(n)` 只对**下一个输出项**生效，用完立即失效 —— 所以每一列都必须重新写一次 `setw`。这也是为什么报表代码里 `setw` 到处都是，看着啰嗦但一个都不能省。\n\n★ `fixed` 是**粘性**的：设过之后一直有效，`setprecision(n)` 的含义也从「有效数字」变成「小数位数」。所以 `fixed` 写在表头之前一次就够，`setprecision` 同理；但 `setw` 必须逐列写。\n\n★ 对齐也是粘性的（`left` / `right` 同样一直有效），所以金额列前面要记得把 `left` 切回 `right`，否则合计行会左对齐。\n\n⚠️ 宽度不够时 `setw` **不会截断**，而是整段照输出、把后面的列顶歪 —— 本题保证名称长度 ≤ 8。",
        "input_format": "第一行 `n`；随后 `n` 行，每行 `名称 数量 单价(分)`。",
        "output_format": "表头 1 行 + 明细 `n` 行 + 合计 1 行；列宽与精度见题面。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 名称长度 ≤ 8（仅 ASCII 字母）\n- 0 ≤ 数量 ≤ 10⁴，0 ≤ 单价(分) ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 11 讲 · 流类库与输入输出",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <string>\n#include <iostream>\n#include <iomanip>\nusing namespace std;\n\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n\n    int n;\n    if (!(cin >> n)) return 0;\n\n    cout << left << setw(10) << \"name\"\n         << right << setw(6) << \"qty\"\n         << setw(12) << \"amount\" << '\\n';\n\n    cout << fixed << setprecision(2);          // 粘性：设一次即可\n\n    long long totQty = 0, totCents = 0;\n    for (int i = 0; i < n; i++) {\n        string name;\n        long long qty, price;\n        cin >> name >> qty >> price;\n        long long cents = qty * price;\n        totQty += qty;\n        totCents += cents;\n\n        cout << left << setw(10) << name            // setw 只管下一项\n             << right << setw(6) << qty\n             << setw(12) << (double)cents / 100.0 << '\\n';\n    }\n\n    cout << left << setw(10) << \"TOTAL\"\n         << right << setw(6) << totQty\n         << setw(12) << (double)totCents / 100.0 << '\\n';\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <string>\n#include <cstring>\n#include <iostream>\n#include <sstream>\n#include <iomanip>\nusing namespace std;\n\n// 独立点：先把每行拼进 ostringstream（内存里的小文件），再统一输出；\n// 宽度/精度照样用操纵符，但「怎么攒行」换成了字符串流。\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n\n    int n;\n    if (!(cin >> n)) return 0;\n\n    ostringstream out;\n    out << left << setw(10) << \"name\"\n        << right << setw(6) << \"qty\"\n        << setw(12) << \"amount\" << '\\n';\n    out << fixed << setprecision(2);\n\n    long long totQty = 0, totCents = 0;\n    for (int i = 0; i < n; i++) {\n        string name;\n        long long qty, price;\n        cin >> name >> qty >> price;\n        long long cents = qty * price;\n        totQty += qty;\n        totCents += cents;\n        out << left << setw(10) << name\n            << right << setw(6) << qty\n            << setw(12) << (double)cents / 100.0 << '\\n';\n    }\n    out << left << setw(10) << \"TOTAL\"\n        << right << setw(6) << totQty\n        << setw(12) << (double)totCents / 100.0 << '\\n';\n\n    cout << out.str();\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "2\nApple 3 1250\nPear 10 99\n",
                "expected_stdout": "name         qty      amount\nApple          3       37.50\nPear          10        9.90\nTOTAL         13       47.40\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\nPen 1 100\n",
                "expected_stdout": "name         qty      amount\nPen            1        1.00\nTOTAL          1        1.00\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\nA 0 500\nBB 2 50\nCCC 100 1\n",
                "expected_stdout": "name         qty      amount\nA              0        0.00\nBB             2        1.00\nCCC          100        1.00\nTOTAL        102        2.00\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\nWidget 7 12345\nGizmo 13 250\n",
                "expected_stdout": "name         qty      amount\nWidget         7      864.15\nGizmo         13       32.50\nTOTAL         20      896.65\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\nx 1 1\ny 1 2\nz 1 3\n",
                "expected_stdout": "name         qty      amount\nx              1        0.01\ny              1        0.02\nz              1        0.03\nTOTAL          3        0.06\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\nLongName 10000 1000000\nShort 1 0\n",
                "expected_stdout": "name         qty      amount\nLongName   10000100000000.00\nShort          1        0.00\nTOTAL      10001100000000.00\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "自定义异常处理取款超额",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 25,
        "tags": [
            "C++异常处理",
            "自定义异常",
            "栈展开",
            "异常安全"
        ],
        "statement_md": "把账户的存取款**异常化**：\n\n- 金额 ≤ 0 → 抛 `BadAmount`（继承 `std::invalid_argument`）；\n- 取款超额 → 抛 `InsufficientFunds`（继承 `std::runtime_error`），对象里带走「还差多少钱」；\n- 正常存取就不抛，直接改余额。\n\n主循环里对**每条**指令包一层 `try`，按异常类型分别处理，输出：\n\n```text\nD 100 OK balance=200\nW 500 FAIL need=300 balance=200\nW -5 BAD\nfinal=200\n```\n\n★ 为什么用异常而不是返回 `bool`：`withdraw` 现在有**两种**失败原因（参数非法、余额不足），而调用方对它们的处理不一样。返回 `bool` 只能表达「成功/失败」，细节得靠出参或全局变量捎带；异常可以**带类型和数据一起飞**，`catch (const InsufficientFunds& e)` 里直接问 `e.deficit()`。\n\n★ `catch` 的顺序：派生类写在基类**前面**。这里 `BadAmount` 与 `InsufficientFunds` 是兄弟，谁先都行；但只要写了 `catch (const std::exception&)`，它就必须放最后 —— 否则前面那个会把所有异常截走。\n\n★ **异常安全**的最低要求：抛异常时对象状态不被污染。所以 `withdraw` 必须**先检查再扣款**，绝不能「先扣了再说」。\n\n⚠️ `throw` 抛出的是**副本**，`catch` 要用 `const 引用` 接：既避免再复制一次，也避免对象切片。",
        "input_format": "第一行余额 `b`；第二行 `q`；随后 `q` 行，每行 `D amt` 或 `W amt`。",
        "output_format": "每条指令一行：`D amt OK balance=..`、`W amt OK balance=..`、`W amt FAIL need=.. balance=..`、`<op> amt BAD`。最后一行 `final=<余额>`。",
        "constraints_md": "- 0 ≤ b ≤ 10⁹\n- 1 ≤ q ≤ 10⁵\n- |amt| ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "第 12 讲 · 异常处理",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <stdexcept>\n#include <string>\nusing namespace std;\n\nclass BadAmount : public std::invalid_argument {\npublic:\n    explicit BadAmount(const char* msg) : std::invalid_argument(msg) {}\n};\n\nclass InsufficientFunds : public std::runtime_error {\nprivate:\n    long long deficit_;\npublic:\n    explicit InsufficientFunds(long long deficit)\n        : std::runtime_error(\"insufficient funds\"), deficit_(deficit) {}\n    long long deficit() const { return deficit_; }\n};\n\nclass Account {\nprivate:\n    long long balance_;\npublic:\n    explicit Account(long long b = 0) : balance_(b) {}\n\n    void deposit(long long amt) {\n        if (amt <= 0) throw BadAmount(\"amount must be positive\");\n        balance_ += amt;                       // 检查通过才动状态\n    }\n    void withdraw(long long amt) {\n        if (amt <= 0) throw BadAmount(\"amount must be positive\");\n        if (amt > balance_) throw InsufficientFunds(amt - balance_);  // 先检查再扣\n        balance_ -= amt;\n    }\n    long long balance() const { return balance_; }\n};\n\nint main() {\n    long long b;\n    int q;\n    if (scanf(\"%lld %d\", &b, &q) != 2) return 0;\n\n    Account acc(b);\n    for (int i = 0; i < q; i++) {\n        char op[4];\n        long long amt;\n        scanf(\"%s %lld\", op, &amt);\n        try {\n            if (op[0] == 'D') {\n                acc.deposit(amt);\n                printf(\"D %lld OK balance=%lld\\n\", amt, acc.balance());\n            } else {\n                acc.withdraw(amt);\n                printf(\"W %lld OK balance=%lld\\n\", amt, acc.balance());\n            }\n        } catch (const InsufficientFunds& e) {        // 派生类在前\n            printf(\"W %lld FAIL need=%lld balance=%lld\\n\",\n                   amt, e.deficit(), acc.balance());\n        } catch (const std::invalid_argument&) {      // 标准异常\n            printf(\"%c %lld BAD\\n\", op[0], amt);\n        }\n    }\n    printf(\"final=%lld\\n\", acc.balance());\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <string>\n#include <iostream>\n#include <sstream>\n#include <string>\n#include <stdexcept>\nusing namespace std;\n\n// 独立点：两个异常类与题面一致，但把「一条指令的完整处理（含 try/catch）」收进\n// 独立的 handle() 函数，用 ostringstream 拼好整行再交回 main ——\n// 参考解是在 main 里就地 try/catch 直接 printf。catch 顺序一样是派生类在前。\nclass BadAmount : public std::invalid_argument {\npublic:\n    BadAmount() : std::invalid_argument(\"amount must be positive\") {}\n};\n\nclass InsufficientFunds : public std::runtime_error {\n    long long deficit_;\npublic:\n    explicit InsufficientFunds(long long d)\n        : std::runtime_error(\"insufficient funds\"), deficit_(d) {}\n    long long deficit() const { return deficit_; }\n};\n\nclass Account {\n    long long balance_;\npublic:\n    explicit Account(long long b) : balance_(b) {}\n    void deposit(long long amt) {\n        if (amt <= 0) throw BadAmount();\n        balance_ += amt;\n    }\n    void withdraw(long long amt) {\n        if (amt <= 0) throw BadAmount();\n        if (amt > balance_) throw InsufficientFunds(amt - balance_);\n        balance_ -= amt;\n    }\n    long long balance() const { return balance_; }\n};\n\nstatic string handle(Account& acc, char op, long long amt) {\n    ostringstream os;\n    try {\n        if (op == 'D') {\n            acc.deposit(amt);\n            os << \"D \" << amt << \" OK balance=\" << acc.balance();\n        } else {\n            acc.withdraw(amt);\n            os << \"W \" << amt << \" OK balance=\" << acc.balance();\n        }\n    } catch (const InsufficientFunds& e) {              // 派生类在前\n        os << \"W \" << amt << \" FAIL need=\" << e.deficit()\n           << \" balance=\" << acc.balance();\n    } catch (const std::invalid_argument&) {            // 标准异常兜底\n        os << op << ' ' << amt << \" BAD\";\n    }\n    return os.str();\n}\n\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n\n    long long b;\n    int q;\n    if (!(cin >> b >> q)) return 0;\n\n    Account acc(b);\n    for (int i = 0; i < q; i++) {\n        string op;\n        long long amt;\n        cin >> op >> amt;\n        cout << handle(acc, op[0], amt) << '\\n';\n    }\n    cout << \"final=\" << acc.balance() << '\\n';\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "100\n4\nD 100\nW 50\nW 500\nW 0\n",
                "expected_stdout": "D 100 OK balance=200\nW 50 OK balance=150\nW 500 FAIL need=350 balance=150\nW 0 BAD\nfinal=150\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "0\n3\nW 1\nD 10\nW 10\n",
                "expected_stdout": "W 1 FAIL need=1 balance=0\nD 10 OK balance=10\nW 10 OK balance=0\nfinal=0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n3\nD -1\nW 5\nD 0\n",
                "expected_stdout": "D -1 BAD\nW 5 OK balance=0\nD 0 BAD\nfinal=0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1000000000\n2\nW 1000000000\nD 1000000000\n",
                "expected_stdout": "W 1000000000 OK balance=0\nD 1000000000 OK balance=1000000000\nfinal=1000000000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "50\n4\nW 49\nW 1\nW 1\nD 3\n",
                "expected_stdout": "W 49 OK balance=1\nW 1 OK balance=0\nW 1 FAIL need=1 balance=0\nD 3 OK balance=3\nfinal=3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7\n3\nD 3\nW 10\nW 10\n",
                "expected_stdout": "D 3 OK balance=10\nW 10 OK balance=0\nW 10 FAIL need=10 balance=0\nfinal=0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    }
]
