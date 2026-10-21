# -*- coding: utf-8 -*-
"""第 6 册：结构体与共用体 / 链表 —— 自动生成，**不要手改本文件**。

生成器：tools/gen_cpp_basic6.py
题数：40 题 / 240 测试点 / 总分 506

重生成：python tools/gen_cpp_basic6.py
"""

CPP_BASIC6_PROBLEMS: list[dict] = [
    {
        "title": "【结构体】学生成绩排序",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "结构体",
            "排序",
            "多关键字"
        ],
        "statement_md": "定义结构体存学号和 3 门课成绩，按**总分降序**排序，总分相同按**学号升序**。每行输出学号与总分。\n\n**关键点**\n\n- 结构体排序的关键是写对比较函数：先比总分（降序），总分相等再比学号（升序）\n- `std::sort` 要求严格弱序，比较函数里不能写 `>=`\n- 总分用 `int` 就够：3 门课各 100 分",
        "input_format": "第一行 `n`；之后 `n` 行，每行 `学号 成绩1 成绩2 成绩3`。",
        "output_format": "`n` 行，每行 `学号 总分`。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 0 ≤ 成绩 ≤ 100\n- 学号唯一",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 结构体与共用体",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <algorithm>\nstruct Student {\n    int id;\n    int s[3];\n    int total() const { return s[0] + s[1] + s[2]; }\n};\nbool cmp(const Student &a, const Student &b) {\n    if (a.total() != b.total()) return a.total() > b.total();   // 总分降序\n    return a.id < b.id;                                         // 同分学号升序\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static Student v[1005];\n    for (int i = 0; i < n; i++)\n        scanf(\"%d %d %d %d\", &v[i].id, &v[i].s[0], &v[i].s[1], &v[i].s[2]);\n    std::sort(v, v + n, cmp);\n    for (int i = 0; i < n; i++) printf(\"%d %d\\n\", v[i].id, v[i].total());\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <vector>\n#include <algorithm>\nstruct Student { int id, total; };\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    std::vector<Student> v;\n    for (int i = 0; i < n; i++) {\n        int id, a, b, c;\n        scanf(\"%d %d %d %d\", &id, &a, &b, &c);\n        v.push_back({id, a + b + c});           // 读的时候就先算好总分\n    }\n    std::sort(v.begin(), v.end(), [](const Student &x, const Student &y) {\n        return x.total != y.total ? x.total > y.total : x.id < y.id;\n    });\n    for (auto &x : v) printf(\"%d %d\\n\", x.id, x.total);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 90 80 70\n2 70 70 70\n3 100 100 100\n",
                "expected_stdout": "3 300\n1 240\n2 210\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n5 60 60 60\n",
                "expected_stdout": "5 180\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n2 80 80 80\n1 80 80 80\n3 79 79 79\n",
                "expected_stdout": "1 240\n2 240\n3 237\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n10 100 0 0\n11 0 100 0\n12 0 0 100\n13 50 50 50\n",
                "expected_stdout": "13 150\n10 100\n11 100\n12 100\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n1 52 63 97\n2 54 95 70\n3 98 74 91\n4 55 52 81\n5 75 55 87\n",
                "expected_stdout": "3 263\n2 219\n5 217\n1 212\n4 188\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n1 100 100 100\n2 100 100 100\n",
                "expected_stdout": "1 300\n2 300\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【结构体】结构体数组求最高分",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "结构体",
            "最值",
            "指针"
        ],
        "statement_md": "读入 `n` 个学生的学号和成绩，输出成绩最高的那个学生的学号与成绩（有并列时输出**最先出现**的）。\n\n**关键点**\n\n- 结构体数组的遍历和普通数组一样，只是取字段时写 `v[i].score`\n- 初值取第一个元素，别写 `max = 0`（成绩可能全 0）\n- 输出一行",
        "input_format": "第一行 `n`；之后 `n` 行，每行 `学号 成绩`。",
        "output_format": "一行：`学号 成绩`。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 0 ≤ 成绩 ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 结构体与共用体",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nstruct Student { int id, score; };\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static Student v[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d %d\", &v[i].id, &v[i].score);\n    int k = 0;\n    for (int i = 1; i < n; i++)\n        if (v[i].score > v[k].score) k = i;   // 严格大于，取最先出现的\n    printf(\"%d %d\\n\", v[k].id, v[k].score);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nstruct Student { int id, score; };\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static Student v[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d %d\", &v[i].id, &v[i].score);\n    Student *p = std::max_element(v, v + n, [](const Student &a, const Student &b) {\n        return a.score < b.score;             // max_element 取第一个最大\n    });\n    printf(\"%d %d\\n\", p->id, p->score);       // 结构体指针用 ->\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 90\n2 95\n3 88\n",
                "expected_stdout": "2 95\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n7 0\n",
                "expected_stdout": "7 0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n1 60\n2 60\n3 60\n",
                "expected_stdout": "1 60\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n10 100\n11 100\n12 99\n13 100\n",
                "expected_stdout": "10 100\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n1 49\n2 0\n3 87\n4 93\n5 51\n",
                "expected_stdout": "4 93\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n5 0\n6 0\n",
                "expected_stdout": "5 0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【结构体】结构体指针遍历求平均分",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "结构体",
            "指针",
            "平均分"
        ],
        "statement_md": "读入 `n` 个学生的成绩，用结构体指针遍历数组求平均分，输出保留 2 位小数。\n\n**关键点**\n\n- `Student *p = v;` 之后 `p->score` 等价于 `(*p).score`\n- 指针遍历写 `for (Student *p = v; p < v + n; ++p)`\n- 平均值用 `double` 算",
        "input_format": "第一行 `n`；之后 `n` 行，每行一个整数成绩。",
        "output_format": "一行：平均分（2 位小数）。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 0 ≤ 成绩 ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 结构体与共用体",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nstruct Student { int score; };\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static Student v[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &v[i].score);\n    long long s = 0;\n    for (Student *p = v; p < v + n; ++p) s += p->score;   // 结构体指针遍历\n    printf(\"%.2f\\n\", (double)s / n);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nstruct Student { int score; };\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static Student v[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &v[i].score);\n    double s = 0;\n    for (int i = 0; i < n; i++) s += (*&v[i]).score;\n    printf(\"%.2f\\n\", s / n);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n90\n80\n70\n",
                "expected_stdout": "80.00\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n100\n",
                "expected_stdout": "100.00\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n100\n100\n0\n0\n",
                "expected_stdout": "50.00\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n60\n61\n62\n63\n64\n",
                "expected_stdout": "62.00\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n95\n97\n29\n92\n31\n58\n",
                "expected_stdout": "67.00\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n59\n61\n",
                "expected_stdout": "60.00\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【结构体】日期结构体比较先后",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "结构体",
            "嵌套",
            "日期"
        ],
        "statement_md": "定义嵌套结构体表示日期（年、月、日），比较两个日期哪个更早，输出较早的那个（格式 `年 月 日`）；两者相同时输出 `same`。\n\n**关键点**\n\n- 年月日按「年优先」比较，不能只看日\n- 把三个字段按字典序比较：先年、再月、再日\n- 相同时只输出 `same`",
        "input_format": "一行六个整数 `y1 m1 d1 y2 m2 d2`。",
        "output_format": "一行：较早的日期，或 `same`。",
        "constraints_md": "- 1 ≤ 年 ≤ 9999\n- 1 ≤ 月 ≤ 12\n- 1 ≤ 日 ≤ 31",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 结构体与共用体",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nstruct Date { int y, m, d; };\nbool earlier(const Date &a, const Date &b) {\n    if (a.y != b.y) return a.y < b.y;\n    if (a.m != b.m) return a.m < b.m;\n    return a.d < b.d;\n}\nbool same(const Date &a, const Date &b) {\n    return a.y == b.y && a.m == b.m && a.d == b.d;\n}\nint main() {\n    Date a, b;\n    if (scanf(\"%d %d %d %d %d %d\", &a.y, &a.m, &a.d, &b.y, &b.m, &b.d) != 6) return 0;\n    if (same(a, b)) { printf(\"same\\n\"); return 0; }\n    Date &e = earlier(a, b) ? a : b;\n    printf(\"%d %d %d\\n\", e.y, e.m, e.d);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nstruct Date { int y, m, d; };\nint key(const Date &x) { return x.y * 10000 + x.m * 100 + x.d; }  // 压成一个整数比较\nint main() {\n    Date a, b;\n    if (scanf(\"%d %d %d %d %d %d\", &a.y, &a.m, &a.d, &b.y, &b.m, &b.d) != 6) return 0;\n    int ka = key(a), kb = key(b);\n    if (ka == kb) printf(\"same\\n\");\n    else {\n        Date &e = ka < kb ? a : b;\n        printf(\"%d %d %d\\n\", e.y, e.m, e.d);\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "2024 1 1 2023 12 31\n",
                "expected_stdout": "2023 12 31\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2024 5 1 2024 5 1\n",
                "expected_stdout": "same\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2024 5 1 2024 5 2\n",
                "expected_stdout": "2024 5 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2000 1 1 1999 12 31\n",
                "expected_stdout": "1999 12 31\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2024 12 31 2025 1 1\n",
                "expected_stdout": "2024 12 31\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2024 2 29 2024 3 1\n",
                "expected_stdout": "2024 2 29\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【结构体】按值传参与按引用传参的差别",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "结构体",
            "值传递",
            "引用"
        ],
        "statement_md": "结构体作参数时，**按值传递**改不动原对象，**按引用传递**才能改。读入 `学号 成绩`，先调用按值的函数给它加 10 分，输出成绩；再调用按引用的函数加 10 分，输出成绩。两行输出。\n\n**关键点**\n\n- 结构体按值传参会把整个对象**复制**一份，函数里改的是副本\n- 按引用传参写 `Student &s`，改的就是原对象\n- 结构体一大，按值传递连性能都亏",
        "input_format": "一行 `学号 成绩`。",
        "output_format": "两行：按值调用后的成绩、按引用调用后的成绩。",
        "constraints_md": "- 0 ≤ 成绩 ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 结构体与共用体",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nstruct Student { int id, score; };\nvoid addByValue(Student s) { s.score += 10; }    // 改的是副本\nvoid addByRef(Student &s)  { s.score += 10; }    // 改的是原对象\nint main() {\n    Student a;\n    if (scanf(\"%d %d\", &a.id, &a.score) != 2) return 0;\n    addByValue(a);\n    printf(\"%d\\n\", a.score);\n    addByRef(a);\n    printf(\"%d\\n\", a.score);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nstruct Student { int id, score; };\nvoid addByPtr(Student *s) { s->score += 10; }    // 指针达到同样效果\nint main() {\n    Student a;\n    if (scanf(\"%d %d\", &a.id, &a.score) != 2) return 0;\n    Student copy = a;\n    addByPtr(&copy);\n    printf(\"%d\\n\", a.score);                     // 原对象没变\n    addByPtr(&a);\n    printf(\"%d\\n\", a.score);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "1 60\n",
                "expected_stdout": "60\n70\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2 0\n",
                "expected_stdout": "0\n10\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 100\n",
                "expected_stdout": "100\n110\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4 45\n",
                "expected_stdout": "45\n55\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5 90\n",
                "expected_stdout": "90\n100\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6 59\n",
                "expected_stdout": "59\n69\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【结构体】时间结构体求秒差",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "结构体",
            "时间",
            "换算"
        ],
        "statement_md": "读入两个时刻（时、分、秒），输出它们相差多少秒（取绝对值）。\n\n**关键点**\n\n- 统一换算成「从 0 点起的秒数」再相减\n- 差可能为负，最后取绝对值\n- 输出一个整数",
        "input_format": "一行六个整数 `h1 m1 s1 h2 m2 s2`。",
        "output_format": "一行：相差的秒数。",
        "constraints_md": "- 0 ≤ 时 ≤ 23\n- 0 ≤ 分, 秒 ≤ 59",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 结构体与共用体",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <cstdlib>\nstruct Time { int h, m, s; };\nint toSec(const Time &t) { return t.h * 3600 + t.m * 60 + t.s; }\nint main() {\n    Time a, b;\n    if (scanf(\"%d %d %d %d %d %d\", &a.h, &a.m, &a.s, &b.h, &b.m, &b.s) != 6) return 0;\n    printf(\"%d\\n\", abs(toSec(a) - toSec(b)));   // 记得取绝对值\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nstruct Time { int h, m, s; };\nint main() {\n    Time a, b;\n    if (scanf(\"%d %d %d %d %d %d\", &a.h, &a.m, &a.s, &b.h, &b.m, &b.s) != 6) return 0;\n    int x = a.h * 3600 + a.m * 60 + a.s;\n    int y = b.h * 3600 + b.m * 60 + b.s;\n    printf(\"%d\\n\", x > y ? x - y : y - x);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "0 0 0 0 0 1\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "12 0 0 12 0 0\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 0 0 0 0 0\n",
                "expected_stdout": "3600\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "23 59 59 0 0 0\n",
                "expected_stdout": "86399\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8 30 15 9 45 50\n",
                "expected_stdout": "4535\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5 0 0 4 59 59\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【结构体】复数结构体加减",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "结构体",
            "复数",
            "函数返回结构体"
        ],
        "statement_md": "用结构体表示复数（实部、虚部都是整数），实现加减法。第一行是运算符 `+` 或 `-`，之后两行各是一个复数 `实部 虚部`。输出运算结果的 `实部 虚部`。\n\n**关键点**\n\n- 复数加减就是实部与实部、虚部与虚部分别运算\n- 输出不带 `i`，就是两个整数\n- 运算符是字符串，用 `%s` 读",
        "input_format": "第一行 `+` 或 `-`；第二行 `a1 b1`；第三行 `a2 b2`。",
        "output_format": "一行：结果的 `实部 虚部`。",
        "constraints_md": "- |实部|, |虚部| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 结构体与共用体",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <cstring>\nstruct Complex { int re, im; };\nComplex add(const Complex &x, const Complex &y) { return {x.re + y.re, x.im + y.im}; }\nComplex sub(const Complex &x, const Complex &y) { return {x.re - y.re, x.im - y.im}; }\nint main() {\n    char op[4];\n    Complex a, b;\n    if (scanf(\"%3s\", op) != 1) return 0;\n    if (scanf(\"%d %d\", &a.re, &a.im) != 2) return 0;\n    if (scanf(\"%d %d\", &b.re, &b.im) != 2) return 0;\n    Complex r = (op[0] == '+') ? add(a, b) : sub(a, b);\n    printf(\"%d %d\\n\", r.re, r.im);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nstruct Complex { int re, im; };\nint main() {\n    char op[4];\n    Complex a, b;\n    if (scanf(\"%3s\", op) != 1) return 0;\n    if (scanf(\"%d %d\", &a.re, &a.im) != 2) return 0;\n    if (scanf(\"%d %d\", &b.re, &b.im) != 2) return 0;\n    int sign = (op[0] == '+') ? 1 : -1;          // 用符号统一处理\n    printf(\"%d %d\\n\", a.re + sign * b.re, a.im + sign * b.im);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "+\n1 2\n3 4\n",
                "expected_stdout": "4 6\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "-\n1 2\n3 4\n",
                "expected_stdout": "-2 -2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "+\n0 0\n0 0\n",
                "expected_stdout": "0 0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "-\n-1 -2\n-3 -4\n",
                "expected_stdout": "2 2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "+\n100 -200\n-50 200\n",
                "expected_stdout": "50 0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "-\n5 5\n5 5\n",
                "expected_stdout": "0 0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【结构体】结构体数组求总分与平均分",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "结构体",
            "统计"
        ],
        "statement_md": "读入 `n` 个学生的成绩，输出总分与平均分（平均分保留 2 位小数），一行，空格分隔。\n\n**关键点**\n\n- 总分用 `long long`，n 到 10⁵ 时总和能到 10⁷\n- 平均分是 `(double)total / n`\n- 输出一行两个数",
        "input_format": "第一行 `n`；之后 `n` 行，每行一个整数成绩。",
        "output_format": "一行：`总分 平均分`。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 0 ≤ 成绩 ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 结构体与共用体",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nstruct Student { int score; };\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static Student v[1005];\n    long long s = 0;\n    for (int i = 0; i < n; i++) { scanf(\"%d\", &v[i].score); s += v[i].score; }\n    printf(\"%lld %.2f\\n\", s, (double)s / n);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nstruct Student { int score; };\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static Student v[1005];\n    double s = 0;\n    for (int i = 0; i < n; i++) { scanf(\"%d\", &v[i].score); s += v[i].score; }\n    printf(\"%.0f %.2f\\n\", s, s / n);      // 总和是整数，用 %.0f 输出\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n90\n80\n70\n",
                "expected_stdout": "240 80.00\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n100\n",
                "expected_stdout": "100 100.00\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n0\n0\n0\n0\n",
                "expected_stdout": "0 0.00\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n59\n61\n",
                "expected_stdout": "120 60.00\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n90\n20\n38\n92\n86\n",
                "expected_stdout": "326 65.20\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7\n61\n68\n84\n80\n96\n74\n73\n",
                "expected_stdout": "536 76.57\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【共用体】用 union 存整数或小数并求和",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "共用体",
            "union",
            "类型标记"
        ],
        "statement_md": "一条记录要么是整数要么是小数，类型由标记位决定。用 `union { int i; double d; }` 存放，读入 `n` 条记录（`i 5` 或 `d 2.5`），输出整数之和与小数之和（小数保留 2 位）。\n\n**关键点**\n\n- 共用体的所有成员**共享同一段内存**，同一时刻只有一种解释是有效的\n- 所以必须另外存一个「类型标记」，否则不知道当前该按哪个成员读\n- 共用体的大小等于最大成员的大小（`double` 是 8 字节）",
        "input_format": "第一行 `n`；之后 `n` 行，每行 `类型标记 值`（`i` 或 `d`）。",
        "output_format": "一行：`整数和 小数和`（小数保留 2 位）。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |整数| ≤ 10⁶\n- |小数| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 结构体与共用体",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nunion Number {\n    int i;\n    double d;\n};\nstruct Record {\n    char kind;              // 类型标记，和 union 一起组成「带标签的联合」\n    Number num;\n};\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    long long si = 0;\n    double sd = 0;\n    for (int k = 0; k < n; k++) {\n        Record r;\n        char buf[8];\n        scanf(\"%7s\", buf);\n        r.kind = buf[0];\n        if (r.kind == 'i') { scanf(\"%d\", &r.num.i); si += r.num.i; }\n        else { scanf(\"%lf\", &r.num.d); sd += r.num.d; }\n    }\n    printf(\"%lld %.2f\\n\", si, sd);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nunion Number { int i; double d; };\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    long long si = 0;\n    double sd = 0;\n    for (int k = 0; k < n; k++) {\n        char kind;\n        Number u;\n        scanf(\" %c\", &kind);\n        if (kind == 'i') { scanf(\"%d\", &u.i); si += u.i; }\n        else { scanf(\"%lf\", &u.d); sd += u.d; }\n    }\n    printf(\"%lld %.2f\\n\", si, sd);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\ni 5\nd 2.5\ni 10\n",
                "expected_stdout": "15 2.50\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\ni 0\n",
                "expected_stdout": "0 0.00\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\nd 0.5\n",
                "expected_stdout": "0 0.50\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\nd 1.25\nd 2.25\nd 3.5\nd 0.0\n",
                "expected_stdout": "0 7.00\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\ni -3\ni 3\n",
                "expected_stdout": "0 0.00\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\nd 1.5\ni 2\nd 2.5\ni -2\nd 0.25\n",
                "expected_stdout": "0 4.25\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【枚举】用 enum 输出星期英文名",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "枚举",
            "enum",
            "switch"
        ],
        "statement_md": "用 `enum Week { MON = 1, TUE, WED, THU, FRI, SAT, SUN };` 读入 `1`~`7`，输出对应的英文名（`Monday`…`Sunday`）；超出范围输出 `Invalid`。\n\n**关键点**\n\n- 枚举的底层就是整数，`MON = 1` 之后 `TUE` 自动是 2\n- 数组下标从 0 开始，枚举从 1 开始，取值时要 `-1`\n- 英文名注意大小写",
        "input_format": "一行一个整数。",
        "output_format": "一行：英文名或 `Invalid`。",
        "constraints_md": "- -10 ≤ 输入 ≤ 20",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 结构体与共用体",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nenum Week { MON = 1, TUE, WED, THU, FRI, SAT, SUN };\nconst char *name[] = {\"\", \"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\",\n                      \"Friday\", \"Saturday\", \"Sunday\"};\nint main() {\n    int k;\n    if (scanf(\"%d\", &k) != 1) return 0;\n    if (k < MON || k > SUN) { printf(\"Invalid\\n\"); return 0; }\n    printf(\"%s\\n\", name[k]);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nenum Week { MON = 1, TUE, WED, THU, FRI, SAT, SUN };\nint main() {\n    int k;\n    if (scanf(\"%d\", &k) != 1) return 0;\n    switch (k) {                    // switch 配枚举更直观\n        case MON: printf(\"Monday\\n\"); break;\n        case TUE: printf(\"Tuesday\\n\"); break;\n        case WED: printf(\"Wednesday\\n\"); break;\n        case THU: printf(\"Thursday\\n\"); break;\n        case FRI: printf(\"Friday\\n\"); break;\n        case SAT: printf(\"Saturday\\n\"); break;\n        case SUN: printf(\"Sunday\\n\"); break;\n        default:  printf(\"Invalid\\n\");\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "1\n",
                "expected_stdout": "Monday\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "7\n",
                "expected_stdout": "Sunday\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "0\n",
                "expected_stdout": "Invalid\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8\n",
                "expected_stdout": "Invalid\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n",
                "expected_stdout": "Wednesday\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "-1\n",
                "expected_stdout": "Invalid\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【结构体】按姓名查找成绩",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "结构体",
            "查找",
            "strcmp"
        ],
        "statement_md": "读入 `n` 个学生的姓名与成绩，再读一个姓名，输出他的成绩；查不到输出 `-1`。\n\n**关键点**\n\n- 姓名用 `char[32]` 存，比较用 `strcmp`（或用 `std::string` 的 `==`）\n- 找到就立刻返回，别继续覆盖\n- 输出一个整数",
        "input_format": "第一行 `n`；之后 `n` 行，每行 `姓名 成绩`；最后一行一个姓名。",
        "output_format": "一行：成绩或 `-1`。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 姓名只含小写字母，长度 ≤ 20",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 结构体与共用体",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <cstring>\nstruct Student {\n    char name[32];\n    int score;\n};\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static Student v[1005];\n    for (int i = 0; i < n; i++) scanf(\"%31s %d\", v[i].name, &v[i].score);\n    char q[32];\n    if (scanf(\"%31s\", q) != 1) return 0;\n    for (int i = 0; i < n; i++)\n        if (strcmp(v[i].name, q) == 0) { printf(\"%d\\n\", v[i].score); return 0; }\n    printf(\"-1\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <iostream>\n#include <string>\n#include <vector>\nstruct Student { std::string name; int score; };\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    std::vector<Student> v(n);\n    for (int i = 0; i < n; i++) std::cin >> v[i].name >> v[i].score;\n    std::string q;\n    if (!(std::cin >> q)) return 0;\n    for (auto &s : v) if (s.name == q) { printf(\"%d\\n\", s.score); return 0; }\n    printf(\"-1\\n\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\nalice 90\nbob 85\ncarol 70\nalice\n",
                "expected_stdout": "90\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\nzoe 100\nzoe\n",
                "expected_stdout": "100\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\naa 1\nbb 2\ncc\n",
                "expected_stdout": "-1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\ntbbk 78\nwryd 7\nkapq 4\nqknb 40\nyzzv 18\nkapq\n",
                "expected_stdout": "4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\nx 60\ny 70\nz 80\nw\n",
                "expected_stdout": "-1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\nonly 0\nonly\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【结构体】点结构体求曼哈顿距离",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "结构体",
            "几何",
            "距离"
        ],
        "statement_md": "用结构体表示平面上的点，读入两个点的坐标，输出它们的曼哈顿距离 `|x1-x2| + |y1-y2|`。\n\n**关键点**\n\n- 曼哈顿距离是「横着走 + 竖着走」的总步数，不是直线距离\n- `abs` 在 `<cstdlib>` 里，注意参数是 `int`\n- 输出一个整数",
        "input_format": "一行四个整数 `x1 y1 x2 y2`。",
        "output_format": "一行：曼哈顿距离。",
        "constraints_md": "- |坐标| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 结构体与共用体",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <cstdlib>\nstruct Point { int x, y; };\nint manhattan(const Point &a, const Point &b) {\n    return abs(a.x - b.x) + abs(a.y - b.y);\n}\nint main() {\n    Point a, b;\n    if (scanf(\"%d %d %d %d\", &a.x, &a.y, &b.x, &b.y) != 4) return 0;\n    printf(\"%d\\n\", manhattan(a, b));\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nstruct Point { int x, y; };\nint main() {\n    Point a, b;\n    if (scanf(\"%d %d %d %d\", &a.x, &a.y, &b.x, &b.y) != 4) return 0;\n    int dx = a.x - b.x, dy = a.y - b.y;\n    if (dx < 0) dx = -dx;              // 手写绝对值\n    if (dy < 0) dy = -dy;\n    printf(\"%d\\n\", dx + dy);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "0 0 3 4\n",
                "expected_stdout": "7\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "0 0 0 0\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "-1 -1 2 2\n",
                "expected_stdout": "6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100 -100 -100 100\n",
                "expected_stdout": "400\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5 5 5 6\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "-3 7 4 -2\n",
                "expected_stdout": "16\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【结构体】矩形结构体求面积与周长",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "结构体",
            "嵌套",
            "矩形"
        ],
        "statement_md": "用两个对角点表示一个矩形，读入两个点的坐标，输出矩形的面积与周长（一行，空格分隔）。\n\n**关键点**\n\n- 边长是两点坐标差的**绝对值**，输入的第二个点不一定在右上方\n- 面积为 0 也要照常输出（退化矩形）\n- 输出一行两个整数",
        "input_format": "一行四个整数 `x1 y1 x2 y2`。",
        "output_format": "一行：`面积 周长`。",
        "constraints_md": "- |坐标| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 结构体与共用体",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <cstdlib>\nstruct Point { int x, y; };\nstruct Rect { Point a, b; };                 // 嵌套结构体\nint width(const Rect &r)  { return abs(r.a.x - r.b.x); }\nint height(const Rect &r) { return abs(r.a.y - r.b.y); }\nint main() {\n    Rect r;\n    if (scanf(\"%d %d %d %d\", &r.a.x, &r.a.y, &r.b.x, &r.b.y) != 4) return 0;\n    int w = width(r), h = height(r);\n    printf(\"%d %d\\n\", w * h, 2 * (w + h));\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nstruct Point { int x, y; };\nstruct Rect { Point a, b; };\nint main() {\n    Rect r;\n    if (scanf(\"%d %d %d %d\", &r.a.x, &r.a.y, &r.b.x, &r.b.y) != 4) return 0;\n    int w = r.a.x > r.b.x ? r.a.x - r.b.x : r.b.x - r.a.x;\n    int h = r.a.y > r.b.y ? r.a.y - r.b.y : r.b.y - r.a.y;\n    printf(\"%d %d\\n\", w * h, 2 * (w + h));\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "0 0 3 4\n",
                "expected_stdout": "12 14\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 4 0 0\n",
                "expected_stdout": "12 14\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "0 0 0 0\n",
                "expected_stdout": "0 0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "-2 -3 2 3\n",
                "expected_stdout": "24 20\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5 5 5 10\n",
                "expected_stdout": "0 10\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1 1 2 2\n",
                "expected_stdout": "1 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【结构体】按成绩分档输出等级",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "结构体",
            "分档",
            "查表"
        ],
        "statement_md": "读入 `n` 个成绩，按 `A(≥90) B(≥80) C(≥70) D(≥60) F(<60)` 转成等级，一行输出，空格分隔。\n\n**关键点**\n\n- 分档判断从高到低写，或用「除以 10」查表\n- 100 分是 A，60 分是 D，59 分是 F\n- 输出 `n` 个字母",
        "input_format": "第一行 `n`；之后 `n` 行，每行一个整数成绩。",
        "output_format": "一行：`n` 个等级字母。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 0 ≤ 成绩 ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 结构体与共用体",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nstruct Student { int score; char grade; };\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static Student v[1005];\n    for (int i = 0; i < n; i++) {\n        scanf(\"%d\", &v[i].score);\n        int s = v[i].score;\n        v[i].grade = s >= 90 ? 'A' : s >= 80 ? 'B' : s >= 70 ? 'C' : s >= 60 ? 'D' : 'F';\n    }\n    for (int i = 0; i < n; i++) printf(\"%c%c\", v[i].grade, i + 1 == n ? '\\n' : ' ');\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    const char *tab = \"FFFFFFDCBAA\";      // 下标 = 分数 / 10（100 落在最后一位 A）\n    for (int i = 0; i < n; i++) {\n        int s; scanf(\"%d\", &s);\n        char g = (s < 60) ? 'F' : tab[s / 10];\n        printf(\"%c%c\", g, i + 1 == n ? '\\n' : ' ');\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n90\n80\n70\n60\n59\n",
                "expected_stdout": "A B C D F\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n100\n",
                "expected_stdout": "A\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n0\n",
                "expected_stdout": "F\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n89\n79\n69\n",
                "expected_stdout": "B C D\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n49\n51\n20\n71\n85\n8\n",
                "expected_stdout": "F F F C B F\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n100\n99\n60\n59\n",
                "expected_stdout": "A A D F\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【结构体】按学号去重保序",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "结构体",
            "去重",
            "保序"
        ],
        "statement_md": "读入 `n` 条学生记录（学号可能重复），只保留每个学号**第一次**出现的那条，按原顺序输出 `学号 成绩`。\n\n**关键点**\n\n- 用一个「已出现」标记数组（学号范围小）或 `set`\n- 去重但**不打乱顺序** —— 所以不能先排序\n- 每行一条记录",
        "input_format": "第一行 `n`；之后 `n` 行，每行 `学号 成绩`。",
        "output_format": "若干行：去重后的记录。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 1 ≤ 学号 ≤ 1000",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 结构体与共用体",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nstruct Student { int id, score; };\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static bool seen[1005];\n    for (int i = 0; i < n; i++) {\n        Student s;\n        scanf(\"%d %d\", &s.id, &s.score);\n        if (seen[s.id]) continue;        // 出现过就丢掉\n        seen[s.id] = true;\n        printf(\"%d %d\\n\", s.id, s.score);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <set>\nstruct Student { int id, score; };\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static Student v[1005];\n    std::set<int> seen;\n    for (int i = 0; i < n; i++) scanf(\"%d %d\", &v[i].id, &v[i].score);\n    for (int i = 0; i < n; i++)\n        if (seen.insert(v[i].id).second)      // insert 返回是否新插入\n            printf(\"%d %d\\n\", v[i].id, v[i].score);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4\n1 90\n2 85\n1 70\n3 60\n",
                "expected_stdout": "1 90\n2 85\n3 60\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n5 50\n",
                "expected_stdout": "5 50\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n1 1\n1 2\n1 3\n",
                "expected_stdout": "1 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n2 10\n1 20\n2 30\n3 40\n1 50\n",
                "expected_stdout": "2 10\n1 20\n3 40\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n2 55\n1 3\n1 22\n2 4\n2 69\n1 88\n",
                "expected_stdout": "2 55\n1 3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n7 80\n7 90\n",
                "expected_stdout": "7 80\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【结构体】排序输出前三名",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "结构体",
            "稳定排序",
            "topK"
        ],
        "statement_md": "读入 `n` 个学生的姓名与成绩，按成绩**降序**输出前 3 名（不足 3 人就有几个输出几个）。成绩相同时保持输入顺序。\n\n**关键点**\n\n- 同分保持原顺序 —— 用 `std::stable_sort` 或比较函数里只比分数\n- `std::sort` 不保证稳定，同分时顺序可能乱\n- 每行 `姓名 成绩`",
        "input_format": "第一行 `n`；之后 `n` 行，每行 `姓名 成绩`。",
        "output_format": "最多 3 行：`姓名 成绩`。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 0 ≤ 成绩 ≤ 100\n- 姓名只含小写字母",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 结构体与共用体",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <algorithm>\nstruct Student {\n    char name[32];\n    int score;\n};\nbool cmp(const Student &a, const Student &b) { return a.score > b.score; }\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static Student v[1005];\n    for (int i = 0; i < n; i++) scanf(\"%31s %d\", v[i].name, &v[i].score);\n    std::stable_sort(v, v + n, cmp);        // 稳定排序，同分保原序\n    int k = n < 3 ? n : 3;\n    for (int i = 0; i < k; i++) printf(\"%s %d\\n\", v[i].name, v[i].score);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nstruct Student { char name[32]; int score; int idx; };\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static Student v[1005];\n    for (int i = 0; i < n; i++) { scanf(\"%31s %d\", v[i].name, &v[i].score); v[i].idx = i; }\n    std::sort(v, v + n, [](const Student &a, const Student &b) {\n        if (a.score != b.score) return a.score > b.score;\n        return a.idx < b.idx;                  // 用原始下标把稳定性「补」回来\n    });\n    int k = n < 3 ? n : 3;\n    for (int i = 0; i < k; i++) printf(\"%s %d\\n\", v[i].name, v[i].score);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4\nalice 90\nbob 85\ncarol 95\ndan 80\n",
                "expected_stdout": "carol 95\nalice 90\nbob 85\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\nx 70\ny 60\n",
                "expected_stdout": "x 70\ny 60\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\nonly 100\n",
                "expected_stdout": "only 100\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\na 80\nb 80\nc 80\n",
                "expected_stdout": "a 80\nb 80\nc 80\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\nflc 71\npul 82\nplc 65\ngvu 98\neol 79\nyds 61\n",
                "expected_stdout": "gvu 98\npul 82\neol 79\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\na 50\nb 90\nc 70\n",
                "expected_stdout": "b 90\nc 70\na 50\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【结构体】分数结构体约分",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "结构体",
            "约分",
            "gcd"
        ],
        "statement_md": "用结构体表示分数（分子、分母），读入一个分数，输出约分后的形式（分母恒为正）。分子为 0 时输出 `0 1`。\n\n**关键点**\n\n- 先求 `gcd(|分子|, |分母|)` 再同除\n- 分母为负时，分子分母同时取反，把负号放到分子上\n- 输出两个整数",
        "input_format": "一行两个整数 `分子 分母`。",
        "output_format": "一行：约分后的 `分子 分母`。",
        "constraints_md": "- |分子| ≤ 10⁶\n- 1 ≤ |分母| ≤ 10⁶\n- 分母不为 0",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 结构体与共用体",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <cstdlib>\nstruct Fraction { int num, den; };\nint gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }\nFraction reduce(Fraction f) {\n    if (f.num == 0) return {0, 1};\n    int g = gcd(abs(f.num), abs(f.den));\n    f.num /= g; f.den /= g;\n    if (f.den < 0) { f.num = -f.num; f.den = -f.den; }   // 分母恒正\n    return f;\n}\nint main() {\n    Fraction f;\n    if (scanf(\"%d %d\", &f.num, &f.den) != 2) return 0;\n    Fraction r = reduce(f);\n    printf(\"%d %d\\n\", r.num, r.den);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <numeric>\n#include <cstdlib>\nstruct Fraction { int num, den; };\nint main() {\n    Fraction f;\n    if (scanf(\"%d %d\", &f.num, &f.den) != 2) return 0;\n    if (f.num == 0) { printf(\"0 1\\n\"); return 0; }\n    int g = std::gcd(abs(f.num), abs(f.den));\n    int a = f.num / g, b = f.den / g;\n    if (b < 0) { a = -a; b = -b; }\n    printf(\"%d %d\\n\", a, b);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "6 8\n",
                "expected_stdout": "3 4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "0 5\n",
                "expected_stdout": "0 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "-6 8\n",
                "expected_stdout": "-3 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6 -8\n",
                "expected_stdout": "-3 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100 1\n",
                "expected_stdout": "100 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "-5 -10\n",
                "expected_stdout": "1 2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【结构体】删除指定学号并输出剩余",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "结构体",
            "删除",
            "压缩"
        ],
        "statement_md": "读入 `n` 条记录和一个学号，删掉该学号的所有记录，输出剩余记录；一条不剩时输出 `empty`。\n\n**关键点**\n\n- 删除就是「不输出」—— 顺序扫描时跳过目标即可\n- 删完可能为空，要单独判断\n- 每行 `学号 成绩`",
        "input_format": "第一行 `n`；之后 `n` 行，每行 `学号 成绩`；最后一行一个学号。",
        "output_format": "若干行剩余记录，或 `empty`。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 1 ≤ 学号 ≤ 1000",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 结构体与共用体",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nstruct Student { int id, score; };\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static Student v[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d %d\", &v[i].id, &v[i].score);\n    int target;\n    if (scanf(\"%d\", &target) != 1) return 0;\n    int c = 0;\n    for (int i = 0; i < n; i++) {\n        if (v[i].id == target) continue;      // 跳过要删的\n        printf(\"%d %d\\n\", v[i].id, v[i].score);\n        c++;\n    }\n    if (c == 0) printf(\"empty\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nstruct Student { int id, score; };\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static Student v[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d %d\", &v[i].id, &v[i].score);\n    int target;\n    if (scanf(\"%d\", &target) != 1) return 0;\n    int k = 0;\n    for (int i = 0; i < n; i++) if (v[i].id != target) v[k++] = v[i];   // 原地压缩\n    if (k == 0) { printf(\"empty\\n\"); return 0; }\n    for (int i = 0; i < k; i++) printf(\"%d %d\\n\", v[i].id, v[i].score);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 90\n2 85\n3 70\n2\n",
                "expected_stdout": "1 90\n3 70\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n1 90\n1\n",
                "expected_stdout": "empty\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n1 90\n2 80\n9\n",
                "expected_stdout": "1 90\n2 80\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n1 10\n2 20\n1 30\n3 40\n1\n",
                "expected_stdout": "2 20\n3 40\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n1 39\n2 57\n3 83\n1 95\n2 10\n1\n",
                "expected_stdout": "2 57\n3 83\n2 10\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n5 50\n6 60\n5\n",
                "expected_stdout": "6 60\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【共用体】union 成员写入互相覆盖",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "共用体",
            "union",
            "内存共享"
        ],
        "statement_md": "共用体的成员共享同一段内存：写 `a` 再写 `b`，`a` 的值就被覆盖了。读入两个整数 `x y`，依次给 `u.a`、`u.b` 赋值，输出此时 `u.a` 与 `u.b` 的值。\n\n**关键点**\n\n- `union { int a; int b; }` 里 `a` 和 `b` 是**同一块 4 字节**\n- 写 `u.b = y` 之后，`u.a` 读出来也是 `y` —— 它们物理上是同一个位置\n- 输出一行两个整数，必然相同",
        "input_format": "一行两个整数 `x y`。",
        "output_format": "一行：`u.a u.b`。",
        "constraints_md": "- |x|, |y| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 结构体与共用体",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nunion Pair {\n    int a;\n    int b;          // 和 a 共用同一段内存\n};\nint main() {\n    int x, y;\n    if (scanf(\"%d %d\", &x, &y) != 2) return 0;\n    Pair u;\n    u.a = x;        // 先写 a\n    u.b = y;        // 再写 b —— a 被覆盖\n    printf(\"%d %d\\n\", u.a, u.b);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nunion Pair { int a; int b; };\nint main() {\n    int x, y;\n    if (scanf(\"%d %d\", &x, &y) != 2) return 0;\n    Pair u;\n    u.a = x;\n    u.b = y;\n    printf(\"%d %d\\n\", u.a, u.b);   // 两者都是 y\n    (void)x;\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "1 2\n",
                "expected_stdout": "2 2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "0 0\n",
                "expected_stdout": "0 0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "-5 5\n",
                "expected_stdout": "5 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100 -100\n",
                "expected_stdout": "-100 -100\n",
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
                "stdin": "123456 -654321\n",
                "expected_stdout": "-654321 -654321\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【结构体】结构体多关键字排序",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "结构体",
            "多关键字",
            "tuple"
        ],
        "statement_md": "读入 `n` 个学生（班级、分数、姓名），先按**班级升序**，同班按**分数降序**，再同分按姓名升序。输出排序结果（每行 `班级 分数 姓名`）。\n\n**关键点**\n\n- 比较函数里三个关键字依次判断，前一个相等才看下一个\n- 班级升序、分数降序、姓名升序，方向不同，别写反\n- 姓名比较用 `strcmp`",
        "input_format": "第一行 `n`；之后 `n` 行，每行 `班级 分数 姓名`。",
        "output_format": "`n` 行：`班级 分数 姓名`。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 1 ≤ 班级 ≤ 10\n- 0 ≤ 分数 ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 结构体与共用体",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <cstring>\n#include <algorithm>\nstruct Student {\n    int cls, score;\n    char name[32];\n};\nbool cmp(const Student &a, const Student &b) {\n    if (a.cls != b.cls) return a.cls < b.cls;          // 班级升序\n    if (a.score != b.score) return a.score > b.score;  // 分数降序\n    return strcmp(a.name, b.name) < 0;                 // 姓名升序\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static Student v[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d %d %31s\", &v[i].cls, &v[i].score, v[i].name);\n    std::sort(v, v + n, cmp);\n    for (int i = 0; i < n; i++) printf(\"%d %d %s\\n\", v[i].cls, v[i].score, v[i].name);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <iostream>\n#include <string>\n#include <vector>\n#include <algorithm>\n#include <tuple>\nstruct Student { int cls, score; std::string name; };\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    std::vector<Student> v(n);\n    for (int i = 0; i < n; i++) std::cin >> v[i].cls >> v[i].score >> v[i].name;\n    std::sort(v.begin(), v.end(), [](const Student &a, const Student &b) {\n        return std::make_tuple(a.cls, -a.score, a.name)\n             < std::make_tuple(b.cls, -b.score, b.name);   // tuple 字典序一次比完\n    });\n    for (auto &s : v) printf(\"%d %d %s\\n\", s.cls, s.score, s.name.c_str());\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n2 90 bob\n1 80 alice\n2 95 carol\n",
                "expected_stdout": "1 80 alice\n2 95 carol\n2 90 bob\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n1 60 solo\n",
                "expected_stdout": "1 60 solo\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n1 80 b\n1 80 a\n1 90 c\n",
                "expected_stdout": "1 90 c\n1 80 a\n1 80 b\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n2 50 x\n1 50 y\n2 50 a\n1 50 b\n",
                "expected_stdout": "1 50 b\n1 50 y\n2 50 a\n2 50 x\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n2 90 rkp\n2 100 vpx\n1 92 yey\n1 65 ppd\n1 84 fbp\n",
                "expected_stdout": "1 92 yey\n1 84 fbp\n1 65 ppd\n2 100 vpx\n2 90 rkp\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n1 100 z\n1 100 a\n",
                "expected_stdout": "1 100 a\n1 100 z\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【链表】尾插法建表并顺序输出",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "链表",
            "尾插",
            "建表"
        ],
        "statement_md": "用**尾插法**建单链表（每次把新结点接到表尾），读入 `n` 和 `n` 个整数，从头到尾输出链表。\n\n**关键点**\n\n- 尾插要维护一个 `tail` 指针，否则每次都要从头找到尾，变成 O(n²)\n- 第一个结点要单独处理：`head = tail = new Node(v)`\n- 输出一行，空格分隔",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：链表的顺序输出。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 链表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nstruct Node {\n    int val;\n    Node *next;\n};\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    Node *head = nullptr, *tail = nullptr;\n    for (int i = 0; i < n; i++) {\n        int x; scanf(\"%d\", &x);\n        Node *p = new Node{x, nullptr};\n        if (!head) head = tail = p;        // 第一个结点\n        else { tail->next = p; tail = p; } // 挂到表尾\n    }\n    for (Node *p = head; p; p = p->next) printf(\"%d%c\", p->val, p->next ? ' ' : '\\n');\n    while (head) { Node *t = head; head = head->next; delete t; }   // 逐个释放\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int val[1005], nxt[1005];       // 数组模拟链表\n    int head = -1, tail = -1;\n    for (int i = 0; i < n; i++) {\n        scanf(\"%d\", &val[i]);\n        nxt[i] = -1;\n        if (head == -1) head = i;\n        else nxt[tail] = i;\n        tail = i;\n    }\n    for (int p = head; p != -1; p = nxt[p]) printf(\"%d%c\", val[p], nxt[p] == -1 ? '\\n' : ' ');\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n1 2 3 4 5\n",
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
                "stdin": "3\n-1 -2 -3\n",
                "expected_stdout": "-1 -2 -3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8\n26 -5 -6 -50 12 -6 17 4\n",
                "expected_stdout": "26 -5 -6 -50 12 -6 17 4\n",
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
                "stdin": "6\n2 60 26 38 17 66\n",
                "expected_stdout": "2 60 26 38 17 66\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【链表】头插法建表（输出逆序）",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "链表",
            "头插",
            "逆序"
        ],
        "statement_md": "用**头插法**建单链表（每次把新结点插在表头），读入 `n` 和 `n` 个整数，输出链表。因为头插，输出顺序与输入相反。\n\n**关键点**\n\n- 头插只有两步：`p->next = head; head = p;`\n- 头插不需要尾指针，但会自然把顺序反过来 —— 这是「逆序建表」的常用技巧\n- 输出一行",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：逆序的链表。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 链表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nstruct Node { int val; Node *next; };\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    Node *head = nullptr;\n    for (int i = 0; i < n; i++) {\n        int x; scanf(\"%d\", &x);\n        head = new Node{x, head};          // 头插：新结点的 next 指向原表头\n    }\n    for (Node *p = head; p; p = p->next) printf(\"%d%c\", p->val, p->next ? ' ' : '\\n');\n    while (head) { Node *t = head; head = head->next; delete t; }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int val[1005], nxt[1005];\n    int head = -1;\n    for (int i = 0; i < n; i++) {\n        scanf(\"%d\", &val[i]);\n        nxt[i] = head;                     // 数组模拟头插\n        head = i;\n    }\n    for (int p = head; p != -1; p = nxt[p]) printf(\"%d%c\", val[p], nxt[p] == -1 ? '\\n' : ' ');\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n1 2 3 4 5\n",
                "expected_stdout": "5 4 3 2 1\n",
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
                "stdin": "3\n7 8 9\n",
                "expected_stdout": "9 8 7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8\n20 -42 -26 34 -17 -30 -14 25\n",
                "expected_stdout": "25 -14 -30 -17 34 -26 -42 20\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n1 1 2 2\n",
                "expected_stdout": "2 2 1 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n-17 -18 42 -41 5\n",
                "expected_stdout": "5 -41 42 -18 -17\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【链表】求链表长度与结点和",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "链表",
            "遍历",
            "统计"
        ],
        "statement_md": "读入 `n` 和 `n` 个整数建成链表，遍历一次同时求出长度和所有结点值之和，输出 `长度 和`（一行）。\n\n**关键点**\n\n- 遍历时计数器与累加器一起走，只扫一遍\n- 和用 `long long`\n- 输出一行两个数",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：`长度 和`。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 链表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nstruct Node { int val; Node *next; };\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    Node *head = nullptr, *tail = nullptr;\n    for (int i = 0; i < n; i++) {\n        int x; scanf(\"%d\", &x);\n        Node *p = new Node{x, nullptr};\n        if (!head) head = tail = p; else { tail->next = p; tail = p; }\n    }\n    int len = 0;\n    long long s = 0;\n    for (Node *p = head; p; p = p->next) { len++; s += p->val; }   // 一趟搞定\n    printf(\"%d %lld\\n\", len, s);\n    while (head) { Node *t = head; head = head->next; delete t; }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nstruct Node { int val; Node *next; };\nint walk(Node *p, int &len, long long &s) {      // 递归遍历\n    if (!p) return 0;\n    len++;\n    s += p->val;\n    return walk(p->next, len, s);\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    Node *head = nullptr, *tail = nullptr;\n    for (int i = 0; i < n; i++) {\n        int x; scanf(\"%d\", &x);\n        Node *p = new Node{x, nullptr};\n        if (!head) head = tail = p; else { tail->next = p; tail = p; }\n    }\n    int len = 0; long long s = 0;\n    walk(head, len, s);\n    printf(\"%d %lld\\n\", len, s);\n    while (head) { Node *t = head; head = head->next; delete t; }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n1 2 3 4 5\n",
                "expected_stdout": "5 15\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n-7\n",
                "expected_stdout": "1 -7\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n0 0 0\n",
                "expected_stdout": "3 0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n7 15 30 -39 6 19 -9 -37 3 -16\n",
                "expected_stdout": "10 -21\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n-436 -200 -743 -234 150 957\n",
                "expected_stdout": "6 -506\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n1000000 1000000\n",
                "expected_stdout": "2 2000000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【链表】查找值首次出现的位置",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "链表",
            "查找"
        ],
        "statement_md": "读入 `n`、`n` 个整数和目标值 `x`，在链表中查找 `x` 第一次出现的位置（从 1 开始），找不到输出 `-1`。\n\n**关键点**\n\n- 遍历时用一个计数器记录位置\n- 找到就立刻返回，不要跑完全程\n- 输出一个整数",
        "input_format": "第一行 `n x`，第二行 `n` 个整数。",
        "output_format": "一行：位置或 `-1`。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 链表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nstruct Node { int val; Node *next; };\nint main() {\n    int n, x;\n    if (scanf(\"%d %d\", &n, &x) != 2) return 0;\n    Node *head = nullptr, *tail = nullptr;\n    for (int i = 0; i < n; i++) {\n        int v; scanf(\"%d\", &v);\n        Node *p = new Node{v, nullptr};\n        if (!head) head = tail = p; else { tail->next = p; tail = p; }\n    }\n    int pos = 0, ans = -1;\n    for (Node *p = head; p; p = p->next) {\n        pos++;\n        if (p->val == x) { ans = pos; break; }   // 第一次就收工\n    }\n    printf(\"%d\\n\", ans);\n    while (head) { Node *t = head; head = head->next; delete t; }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nstruct Node { int val; Node *next; };\nint main() {\n    int n, x;\n    if (scanf(\"%d %d\", &n, &x) != 2) return 0;\n    static int val[1005], nxt[1005];\n    int head = -1, tail = -1;\n    for (int i = 0; i < n; i++) {\n        scanf(\"%d\", &val[i]); nxt[i] = -1;\n        if (head == -1) head = i; else nxt[tail] = i;\n        tail = i;\n    }\n    int pos = 0, ans = -1;\n    for (int p = head; p != -1; p = nxt[p]) {\n        pos++;\n        if (val[p] == x) { ans = pos; break; }\n    }\n    printf(\"%d\\n\", ans);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 3\n1 2 3 4 3\n",
                "expected_stdout": "3\n",
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
                "stdin": "1 1\n1\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3 2\n2 2 2\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8 5\n2 1 7 9 1 6 9 6\n",
                "expected_stdout": "-1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4 -1\n5 2 3 1\n",
                "expected_stdout": "-1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【链表】在第 k 个位置前插入结点",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "链表",
            "插入",
            "哑结点"
        ],
        "statement_md": "读入 `n k x` 和 `n` 个整数建成链表，在**第 k 个结点之前**插入值为 `x` 的新结点，输出插入后的链表。`k = 1` 表示插在表头；`k > n` 表示追加到表尾。\n\n**关键点**\n\n- 插在第 k 个之前，要走到**第 k-1 个**结点，然后 `p->next = newNode`\n- `k = 1` 时没有第 0 个结点，必须单独处理（改 head）\n- 输出一行",
        "input_format": "第一行 `n k x`，第二行 `n` 个整数。",
        "output_format": "一行：插入后的链表。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 1 ≤ k ≤ 10⁶\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 链表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nstruct Node { int val; Node *next; };\nint main() {\n    int n, k, x;\n    if (scanf(\"%d %d %d\", &n, &k, &x) != 3) return 0;\n    Node *head = nullptr, *tail = nullptr;\n    for (int i = 0; i < n; i++) {\n        int v; scanf(\"%d\", &v);\n        Node *p = new Node{v, nullptr};\n        if (!head) head = tail = p; else { tail->next = p; tail = p; }\n    }\n    Node *fresh = new Node{x, nullptr};\n    if (k <= 1) { fresh->next = head; head = fresh; }      // 插表头\n    else {\n        Node *p = head;\n        int pos = 1;\n        while (p->next && pos < k - 1) { p = p->next; pos++; }   // 走到第 k-1 个\n        fresh->next = p->next;\n        p->next = fresh;\n    }\n    for (Node *p = head; p; p = p->next) printf(\"%d%c\", p->val, p->next ? ' ' : '\\n');\n    while (head) { Node *t = head; head = head->next; delete t; }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nstruct Node { int val; Node *next; };\nint main() {\n    int n, k, x;\n    if (scanf(\"%d %d %d\", &n, &k, &x) != 3) return 0;\n    Node dummy{0, nullptr};                 // 哑结点：让「插表头」不用特判\n    Node *tail = &dummy;\n    for (int i = 0; i < n; i++) {\n        int v; scanf(\"%d\", &v);\n        tail->next = new Node{v, nullptr};\n        tail = tail->next;\n    }\n    Node *prev = &dummy;\n    for (int i = 1; i < k && prev->next; i++) prev = prev->next;\n    Node *fresh = new Node{x, prev->next};\n    prev->next = fresh;\n    for (Node *p = dummy.next; p; p = p->next) printf(\"%d%c\", p->val, p->next ? ' ' : '\\n');\n    while (dummy.next) { Node *t = dummy.next; dummy.next = t->next; delete t; }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 1 99\n1 2 3 4 5\n",
                "expected_stdout": "99 1 2 3 4 5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5 3 99\n1 2 3 4 5\n",
                "expected_stdout": "1 2 99 3 4 5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5 6 99\n1 2 3 4 5\n",
                "expected_stdout": "1 2 3 4 5 99\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1 1 0\n5\n",
                "expected_stdout": "0 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3 2 -1\n7 8 9\n",
                "expected_stdout": "7 -1 8 9\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6 2 42\n1 23 -38 17 19 -35\n",
                "expected_stdout": "1 42 23 -38 17 19 -35\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【链表】删除第 k 个结点",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "链表",
            "删除"
        ],
        "statement_md": "读入 `n k` 和 `n` 个整数建成链表，删除第 k 个结点，输出剩余链表；删完为空则输出 `empty`。`k` 超出范围时不做任何删除。\n\n**关键点**\n\n- 删除要拿到**前驱**，所以走到第 k-1 个\n- 删表头要改 head；用哑结点可以一并处理\n- 删完记得 `delete`",
        "input_format": "第一行 `n k`，第二行 `n` 个整数。",
        "output_format": "一行：剩余链表，或 `empty`。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 1 ≤ k ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 链表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nstruct Node { int val; Node *next; };\nint main() {\n    int n, k;\n    if (scanf(\"%d %d\", &n, &k) != 2) return 0;\n    Node dummy{0, nullptr};\n    Node *tail = &dummy;\n    for (int i = 0; i < n; i++) {\n        int v; scanf(\"%d\", &v);\n        tail->next = new Node{v, nullptr};\n        tail = tail->next;\n    }\n    Node *prev = &dummy;\n    for (int i = 1; i < k && prev->next; i++) prev = prev->next;\n    if (prev->next) {                            // k 合法才删\n        Node *victim = prev->next;\n        prev->next = victim->next;\n        delete victim;\n    }\n    if (!dummy.next) { printf(\"empty\\n\"); return 0; }\n    for (Node *p = dummy.next; p; p = p->next) printf(\"%d%c\", p->val, p->next ? ' ' : '\\n');\n    while (dummy.next) { Node *t = dummy.next; dummy.next = t->next; delete t; }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n, k;\n    if (scanf(\"%d %d\", &n, &k) != 2) return 0;\n    static int val[1005], nxt[1005];\n    int head = -1, tail = -1;\n    for (int i = 0; i < n; i++) {\n        scanf(\"%d\", &val[i]); nxt[i] = -1;\n        if (head == -1) head = i; else nxt[tail] = i;\n        tail = i;\n    }\n    if (k == 1) head = nxt[head];                // 删表头\n    else {\n        int prev = head;\n        for (int i = 1; i < k - 1 && nxt[prev] != -1; i++) prev = nxt[prev];\n        if (nxt[prev] != -1) nxt[prev] = nxt[nxt[prev]];   // 跳过被删结点\n    }\n    if (head == -1) { printf(\"empty\\n\"); return 0; }\n    for (int p = head; p != -1; p = nxt[p]) printf(\"%d%c\", val[p], nxt[p] == -1 ? '\\n' : ' ');\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 1\n1 2 3 4 5\n",
                "expected_stdout": "2 3 4 5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5 3\n1 2 3 4 5\n",
                "expected_stdout": "1 2 4 5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 1\n7\n",
                "expected_stdout": "empty\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5 9\n1 2 3 4 5\n",
                "expected_stdout": "1 2 3 4 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3 2\n9 8 7\n",
                "expected_stdout": "9 7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6 4\n-4 -27 1 35 -10 33\n",
                "expected_stdout": "-4 -27 1 -10 33\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【链表】原地逆序链表",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "链表",
            "逆序",
            "三指针"
        ],
        "statement_md": "读入 `n` 和 `n` 个整数建成链表，把链表**原地**逆序后输出。\n\n**关键点**\n\n- 三指针法：`prev`、`cur`、`next`，每步把 `cur->next` 指向 `prev`\n- 顺序不能错：先存 `next`，再改 `cur->next`，最后两个指针一起前移\n- 输出一行",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：逆序后的链表。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 链表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nstruct Node { int val; Node *next; };\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    Node *head = nullptr, *tail = nullptr;\n    for (int i = 0; i < n; i++) {\n        int v; scanf(\"%d\", &v);\n        Node *p = new Node{v, nullptr};\n        if (!head) head = tail = p; else { tail->next = p; tail = p; }\n    }\n    Node *prev = nullptr, *cur = head;\n    while (cur) {\n        Node *nxt = cur->next;    // ① 先存下一站\n        cur->next = prev;         // ② 反转指针\n        prev = cur;               // ③ 整体后移\n        cur = nxt;\n    }\n    head = prev;\n    for (Node *p = head; p; p = p->next) printf(\"%d%c\", p->val, p->next ? ' ' : '\\n');\n    while (head) { Node *t = head; head = head->next; delete t; }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nstruct Node { int val; Node *next; };\nNode *rev(Node *p) {                       // 递归逆序\n    if (!p || !p->next) return p;\n    Node *h = rev(p->next);\n    p->next->next = p;\n    p->next = nullptr;\n    return h;\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    Node *head = nullptr, *tail = nullptr;\n    for (int i = 0; i < n; i++) {\n        int v; scanf(\"%d\", &v);\n        Node *p = new Node{v, nullptr};\n        if (!head) head = tail = p; else { tail->next = p; tail = p; }\n    }\n    head = rev(head);\n    for (Node *p = head; p; p = p->next) printf(\"%d%c\", p->val, p->next ? ' ' : '\\n');\n    while (head) { Node *t = head; head = head->next; delete t; }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n1 2 3 4 5\n",
                "expected_stdout": "5 4 3 2 1\n",
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
                "stdin": "3\n1 2 3\n",
                "expected_stdout": "3 2 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8\n-21 -11 -19 34 -40 -24 36 -32\n",
                "expected_stdout": "-32 36 -24 -40 34 -19 -11 -21\n",
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
                "stdin": "6\n-5 3 3 5 -9 4\n",
                "expected_stdout": "4 -9 5 3 3 -5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【链表】合并两个有序链表",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "链表",
            "归并",
            "双指针"
        ],
        "statement_md": "读入两个**升序**链表，合并成一个仍然升序的链表并输出。格式：第一行 `n`，第二行 `n` 个数；第三行 `m`，第四行 `m` 个数。\n\n**关键点**\n\n- 双指针：每次取两个表头中较小的那个接到结果表尾\n- 一个表走完后，把另一个表的剩余部分整段接上\n- 输出一行",
        "input_format": "第一行 `n`；第二行 `n` 个升序整数；第三行 `m`；第四行 `m` 个升序整数。",
        "output_format": "一行：合并后的升序链表。",
        "constraints_md": "- 1 ≤ n, m ≤ 500\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 链表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nstruct Node { int val; Node *next; };\nNode *build(int n) {\n    Node *head = nullptr, *tail = nullptr;\n    for (int i = 0; i < n; i++) {\n        int v; scanf(\"%d\", &v);\n        Node *p = new Node{v, nullptr};\n        if (!head) head = tail = p; else { tail->next = p; tail = p; }\n    }\n    return head;\n}\nint main() {\n    int n, m;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    Node *a = build(n);\n    if (scanf(\"%d\", &m) != 1) return 0;\n    Node *b = build(m);\n    Node dummy{0, nullptr}, *t = &dummy;\n    while (a && b) {                       // 双指针归并\n        if (a->val <= b->val) { t->next = a; a = a->next; }\n        else { t->next = b; b = b->next; }\n        t = t->next;\n    }\n    t->next = a ? a : b;                   // 剩余部分整段接上\n    for (Node *p = dummy.next; p; p = p->next) printf(\"%d%c\", p->val, p->next ? ' ' : '\\n');\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <vector>\n#include <algorithm>\nint main() {\n    int n, m;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    std::vector<int> v(n);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &v[i]);\n    if (scanf(\"%d\", &m) != 1) return 0;\n    for (int i = 0; i < m; i++) { int x; scanf(\"%d\", &x); v.push_back(x); }\n    std::sort(v.begin(), v.end());         // 偷懒版：全排一遍\n    for (int i = 0; i < (int)v.size(); i++) printf(\"%d%c\", v[i], i + 1 == (int)v.size() ? '\\n' : ' ');\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 4 7\n3\n2 5 8\n",
                "expected_stdout": "1 2 4 5 7 8\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n1\n1\n2\n",
                "expected_stdout": "1 2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n1 2 3\n3\n4 5 6\n",
                "expected_stdout": "1 2 3 4 5 6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n5 6\n2\n1 2\n",
                "expected_stdout": "1 2 5 6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n0\n1\n0\n",
                "expected_stdout": "0 0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n1 3 5 7\n4\n2 4 6 8\n",
                "expected_stdout": "1 2 3 4 5 6 7 8\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【链表】删除重复元素保序",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "链表",
            "去重"
        ],
        "statement_md": "读入 `n` 和 `n` 个整数建成链表，删除重复出现的结点，只保留每个值**第一次**出现的位置，输出结果。\n\n**关键点**\n\n- 用一个 `bool seen[]`（值域小时）或 `set` 记录出现过没有\n- 边遍历边删除，注意保存前驱\n- 输出一行",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：去重后的链表。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 链表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <set>\nstruct Node { int val; Node *next; };\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    Node dummy{0, nullptr}, *tail = &dummy;\n    std::set<int> seen;\n    for (int i = 0; i < n; i++) {\n        int v; scanf(\"%d\", &v);\n        if (!seen.insert(v).second) continue;    // 出现过了，直接丢弃\n        tail->next = new Node{v, nullptr};\n        tail = tail->next;\n    }\n    for (Node *p = dummy.next; p; p = p->next) printf(\"%d%c\", p->val, p->next ? ' ' : '\\n');\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nstruct Node { int val; Node *next; };\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static Node pool[1005];              // 静态结点池，免去 new\n    int cnt = 0;\n    Node dummy{0, nullptr}, *tail = &dummy;\n    for (int i = 0; i < n; i++) {\n        int v; scanf(\"%d\", &v);\n        bool dup = false;\n        for (Node *p = dummy.next; p; p = p->next) if (p->val == v) { dup = true; break; }\n        if (dup) continue;\n        pool[cnt].val = v; pool[cnt].next = nullptr;\n        tail->next = &pool[cnt++];\n        tail = tail->next;\n    }\n    for (Node *p = dummy.next; p; p = p->next) printf(\"%d%c\", p->val, p->next ? ' ' : '\\n');\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n1 2 1 3 2\n",
                "expected_stdout": "1 2 3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n1 1 1\n",
                "expected_stdout": "1\n",
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
                "stdin": "8\n1 3 3 1 3 2 1 4\n",
                "expected_stdout": "1 3 2 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n1 2 3 4\n",
                "expected_stdout": "1 2 3 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n1 2 1 1 2 0\n",
                "expected_stdout": "1 2 0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【链表】求中间结点",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "链表",
            "快慢指针",
            "中间结点"
        ],
        "statement_md": "读入 `n` 和 `n` 个整数建成链表，输出**中间结点**的值。`n` 为偶数时取中间偏前的那个（即第 `n/2` 个）。\n\n**关键点**\n\n- 快慢指针：快指针一次走两步，慢指针一次走一步，快指针到头时慢指针就在中间\n- 偶数个结点时，快指针的判断条件决定取偏前还是偏后一个\n- 输出一个整数",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：中间结点的值。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 链表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nstruct Node { int val; Node *next; };\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    Node *head = nullptr, *tail = nullptr;\n    for (int i = 0; i < n; i++) {\n        int v; scanf(\"%d\", &v);\n        Node *p = new Node{v, nullptr};\n        if (!head) head = tail = p; else { tail->next = p; tail = p; }\n    }\n    Node *slow = head, *fast = head;\n    while (fast->next && fast->next->next) {   // 偶数时停在偏前那个\n        slow = slow->next;\n        fast = fast->next->next;\n    }\n    printf(\"%d\\n\", slow->val);\n    while (head) { Node *t = head; head = head->next; delete t; }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int val[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &val[i]);\n    printf(\"%d\\n\", val[(n - 1) / 2]);          // 直接算下标，结果一致\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n1 2 3 4 5\n",
                "expected_stdout": "3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n1 2 3 4\n",
                "expected_stdout": "2\n",
                "is_sample": 1,
                "kind": "sample",
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
                "stdin": "2\n3 4\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8\n-34 -8 50 22 2 20 6 -22\n",
                "expected_stdout": "22\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7\n71 70 83 13 35 23 46\n",
                "expected_stdout": "13\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【链表】约瑟夫环出列顺序",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 16,
        "tags": [
            "链表",
            "循环链表",
            "约瑟夫环"
        ],
        "statement_md": "`n` 个人围成一圈（编号 1~n），从 1 号开始报数，报到 `m` 的人出列，然后从下一个人重新报数。读入 `n m`，按出列顺序输出所有人的编号。\n\n**关键点**\n\n- 用循环链表：出列就是把前驱的 `next` 指向被删结点的后继\n- 每轮要走 `m-1` 步（不是 `m` 步），因为当前人算第 1 个\n- 只有一个人时 `next` 指向自己，别写成 `nullptr`",
        "input_format": "一行两个整数 `n m`。",
        "output_format": "一行：出列顺序，空格分隔。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 1 ≤ m ≤ 1000",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 链表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nstruct Node { int val; Node *next; };\nint main() {\n    int n, m;\n    if (scanf(\"%d %d\", &n, &m) != 2 || n <= 0) return 0;\n    Node *head = new Node{1, nullptr};\n    Node *tail = head;\n    for (int i = 2; i <= n; i++) { tail->next = new Node{i, nullptr}; tail = tail->next; }\n    tail->next = head;                         // 首尾相接成环\n    Node *prev = tail, *cur = head;\n    for (int left = n; left >= 1; left--) {\n        for (int s = 1; s < m; s++) { prev = cur; cur = cur->next; }   // 走 m-1 步\n        printf(\"%d%c\", cur->val, left == 1 ? '\\n' : ' ');\n        prev->next = cur->next;                // 出列\n        Node *t = cur;\n        cur = cur->next;\n        delete t;\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <vector>\nint main() {\n    int n, m;\n    if (scanf(\"%d %d\", &n, &m) != 2 || n <= 0) return 0;\n    std::vector<int> a;\n    for (int i = 1; i <= n; i++) a.push_back(i);\n    int i = 0;\n    while (!a.empty()) {                       // 用 vector 模拟环\n        i = (i + m - 1) % (int)a.size();\n        printf(\"%d%c\", a[i], a.size() == 1 ? '\\n' : ' ');\n        a.erase(a.begin() + i);\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 3\n",
                "expected_stdout": "3 1 5 2 4\n",
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
                "stdin": "2 1\n",
                "expected_stdout": "1 2\n",
                "is_sample": 0,
                "kind": "manual",
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
                "stdin": "7 4\n",
                "expected_stdout": "4 1 6 5 7 3 2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6 2\n",
                "expected_stdout": "2 4 6 3 1 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【链表】删除所有等于 x 的结点",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "链表",
            "删除",
            "哑结点"
        ],
        "statement_md": "读入 `n x` 和 `n` 个整数建成链表，删除**所有**值等于 `x` 的结点，输出剩余链表；全被删光输出 `empty`。\n\n**关键点**\n\n- 哑结点能省掉「删表头」的特判\n- 删除是循环里最容易写错的：`cur = cur->next` 要在判断之后\n- 输出一行",
        "input_format": "第一行 `n x`，第二行 `n` 个整数。",
        "output_format": "一行：剩余链表，或 `empty`。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 链表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nstruct Node { int val; Node *next; };\nint main() {\n    int n, x;\n    if (scanf(\"%d %d\", &n, &x) != 2) return 0;\n    Node dummy{0, nullptr}, *tail = &dummy;\n    for (int i = 0; i < n; i++) {\n        int v; scanf(\"%d\", &v);\n        tail->next = new Node{v, nullptr};\n        tail = tail->next;\n    }\n    Node *prev = &dummy;\n    while (prev->next) {\n        if (prev->next->val == x) {            // 命中就删，prev 不动\n            Node *t = prev->next;\n            prev->next = t->next;\n            delete t;\n        } else prev = prev->next;\n    }\n    if (!dummy.next) { printf(\"empty\\n\"); return 0; }\n    for (Node *p = dummy.next; p; p = p->next) printf(\"%d%c\", p->val, p->next ? ' ' : '\\n');\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n, x;\n    if (scanf(\"%d %d\", &n, &x) != 2) return 0;\n    static int val[1005], nxt[1005];\n    int head = -1, tail = -1;\n    for (int i = 0; i < n; i++) {\n        scanf(\"%d\", &val[i]); nxt[i] = -1;\n        if (head == -1) head = i; else nxt[tail] = i;\n        tail = i;\n    }\n    while (head != -1 && val[head] == x) head = nxt[head];    // 先清表头\n    for (int p = head; p != -1; p = nxt[p])\n        while (nxt[p] != -1 && val[nxt[p]] == x) nxt[p] = nxt[nxt[p]];\n    if (head == -1) { printf(\"empty\\n\"); return 0; }\n    for (int p = head; p != -1; p = nxt[p]) printf(\"%d%c\", val[p], nxt[p] == -1 ? '\\n' : ' ');\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 2\n1 2 3 2 4\n",
                "expected_stdout": "1 3 4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 1\n1 1 1\n",
                "expected_stdout": "empty\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 5\n5\n",
                "expected_stdout": "empty\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4 9\n1 2 3 4\n",
                "expected_stdout": "1 2 3 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6 1\n3 3 1 3 3 3\n",
                "expected_stdout": "3 3 3 3 3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3 0\n0 1 0\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【链表】求最大值与位置",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "链表",
            "最值"
        ],
        "statement_md": "读入 `n` 和 `n` 个整数建成链表，输出最大值及它第一次出现的结点位置（从 1 开始）。\n\n**关键点**\n\n- 遍历时同时维护「当前最大」和「它的位置」\n- 更新条件用严格大于，才能取到第一次出现的位置\n- 输出一行两个整数",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：`最大值 位置`。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 链表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nstruct Node { int val; Node *next; };\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    Node *head = nullptr, *tail = nullptr;\n    for (int i = 0; i < n; i++) {\n        int v; scanf(\"%d\", &v);\n        Node *p = new Node{v, nullptr};\n        if (!head) head = tail = p; else { tail->next = p; tail = p; }\n    }\n    int mx = head->val, pos = 1, i = 1, best = 1;\n    for (Node *p = head; p; p = p->next, i++) {\n        if (p->val > mx) { mx = p->val; best = i; }   // 严格大于\n    }\n    printf(\"%d %d\\n\", mx, best);\n    (void)pos;\n    while (head) { Node *t = head; head = head->next; delete t; }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int val[1005], nxt[1005];\n    int head = -1, tail = -1;\n    for (int i = 0; i < n; i++) {\n        scanf(\"%d\", &val[i]); nxt[i] = -1;\n        if (head == -1) head = i; else nxt[tail] = i;\n        tail = i;\n    }\n    int mx = val[head], best = 1, i = 1;\n    for (int p = head; p != -1; p = nxt[p], i++)\n        if (val[p] > mx) { mx = val[p]; best = i; }\n    printf(\"%d %d\\n\", mx, best);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n3 1 4 1 5\n",
                "expected_stdout": "5 5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n-9\n",
                "expected_stdout": "-9 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n5 5 1\n",
                "expected_stdout": "5 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n-1 -2 -3 -4\n",
                "expected_stdout": "-1 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7\n-11 21 -18 50 -39 22 12\n",
                "expected_stdout": "50 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n0 0 0\n",
                "expected_stdout": "0 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【链表】判断链表是否严格递增",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "链表",
            "递增",
            "判断"
        ],
        "statement_md": "读入 `n` 和 `n` 个整数建成链表，判断它是否**严格递增**（后一个严格大于前一个）。是输出 `YES`，否则输出 `NO`。\n\n**关键点**\n\n- 只要出现 `cur->val >= cur->next->val` 就不满足\n- 单结点链表算递增\n- 只输出 `YES` 或 `NO`",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：`YES` 或 `NO`。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 链表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nstruct Node { int val; Node *next; };\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    Node *head = nullptr, *tail = nullptr;\n    for (int i = 0; i < n; i++) {\n        int v; scanf(\"%d\", &v);\n        Node *p = new Node{v, nullptr};\n        if (!head) head = tail = p; else { tail->next = p; tail = p; }\n    }\n    bool ok = true;\n    for (Node *p = head; p->next; p = p->next)\n        if (p->val >= p->next->val) { ok = false; break; }   // 必须严格大于\n    printf(\"%s\\n\", ok ? \"YES\" : \"NO\");\n    while (head) { Node *t = head; head = head->next; delete t; }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int val[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &val[i]);\n    bool ok = true;\n    for (int i = 0; i + 1 < n; i++) if (val[i] >= val[i + 1]) ok = false;\n    printf(\"%s\\n\", ok ? \"YES\" : \"NO\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 2 3\n",
                "expected_stdout": "YES\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n1 2 2\n",
                "expected_stdout": "NO\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n5\n",
                "expected_stdout": "YES\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n3 2 1\n",
                "expected_stdout": "NO\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n-32 37 -11 -48 37\n",
                "expected_stdout": "NO\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n-3 -2 -1 0\n",
                "expected_stdout": "YES\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【链表】按值分段（小于 x 的在前）",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 16,
        "tags": [
            "链表",
            "分段",
            "稳定"
        ],
        "statement_md": "读入 `n x` 和 `n` 个整数建成链表，把所有小于 `x` 的结点排到前面，其余排在后面，**两段内部都保持原来的相对顺序**，输出结果。\n\n**关键点**\n\n- 建两个子链表：一个挂小于 x 的，一个挂其余的，最后首尾相接\n- 关键是「保持相对顺序」—— 所以必须用尾插，不能头插\n- 输出一行",
        "input_format": "第一行 `n x`，第二行 `n` 个整数。",
        "output_format": "一行：分段后的链表。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 链表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nstruct Node { int val; Node *next; };\nint main() {\n    int n, x;\n    if (scanf(\"%d %d\", &n, &x) != 2) return 0;\n    Node less{0, nullptr}, *lt = &less;\n    Node rest{0, nullptr}, *rt = &rest;\n    for (int i = 0; i < n; i++) {\n        int v; scanf(\"%d\", &v);\n        if (v < x) { lt->next = new Node{v, nullptr}; lt = lt->next; }   // 尾插保序\n        else       { rt->next = new Node{v, nullptr}; rt = rt->next; }\n    }\n    lt->next = rest.next;                 // 两段接起来\n    for (Node *p = less.next; p; p = p->next) printf(\"%d%c\", p->val, p->next ? ' ' : '\\n');\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <vector>\nint main() {\n    int n, x;\n    if (scanf(\"%d %d\", &n, &x) != 2) return 0;\n    std::vector<int> v(n), a, b;\n    for (int i = 0; i < n; i++) {\n        scanf(\"%d\", &v[i]);\n        if (v[i] < x) a.push_back(v[i]); else b.push_back(v[i]);\n    }\n    for (int i = 0; i < (int)b.size(); i++) a.push_back(b[i]);\n    for (int i = 0; i < (int)a.size(); i++) printf(\"%d%c\", a[i], i + 1 == (int)a.size() ? '\\n' : ' ');\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 3\n1 4 2 5 3\n",
                "expected_stdout": "1 2 4 5 3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5 10\n1 2 3 4 5\n",
                "expected_stdout": "1 2 3 4 5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 0\n1 2 3\n",
                "expected_stdout": "1 2 3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1 5\n9\n",
                "expected_stdout": "9\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7 5\n0 5 4 6 1 1 0\n",
                "expected_stdout": "0 4 1 1 0 5 6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6 100\n1 2 3 4 5 6\n",
                "expected_stdout": "1 2 3 4 5 6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【链表】两个链表的并集",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "链表",
            "并集",
            "去重"
        ],
        "statement_md": "读入两个链表，输出它们的并集（每个值只出现一次，按升序）。格式：第一行 `n`，第二行 `n` 个数；第三行 `m`，第四行 `m` 个数。\n\n**关键点**\n\n- 「并集」意味着去重，重复值只留一个\n- 先把两个链表结在一起，再去重排序\n- 输出一行",
        "input_format": "第一行 `n`；第二行 `n` 个整数；第三行 `m`；第四行 `m` 个整数。",
        "output_format": "一行：升序去重的并集。",
        "constraints_md": "- 1 ≤ n, m ≤ 500\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 链表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <set>\nstruct Node { int val; Node *next; };\nNode *build(int n) {\n    Node *head = nullptr, *tail = nullptr;\n    for (int i = 0; i < n; i++) {\n        int v; scanf(\"%d\", &v);\n        Node *p = new Node{v, nullptr};\n        if (!head) head = tail = p; else { tail->next = p; tail = p; }\n    }\n    return head;\n}\nint main() {\n    int n, m;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    Node *a = build(n);\n    if (scanf(\"%d\", &m) != 1) return 0;\n    Node *b = build(m);\n    std::set<int> s;                        // set 天然去重 + 升序\n    for (Node *p = a; p; p = p->next) s.insert(p->val);\n    for (Node *p = b; p; p = p->next) s.insert(p->val);\n    int i = 0, k = (int)s.size();\n    for (int x : s) printf(\"%d%c\", x, ++i == k ? '\\n' : ' ');\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <vector>\n#include <algorithm>\nint main() {\n    int n, m;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    std::vector<int> v(n);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &v[i]);\n    if (scanf(\"%d\", &m) != 1) return 0;\n    for (int i = 0; i < m; i++) { int x; scanf(\"%d\", &x); v.push_back(x); }\n    std::sort(v.begin(), v.end());\n    v.erase(std::unique(v.begin(), v.end()), v.end());   // 排序后去重\n    for (int i = 0; i < (int)v.size(); i++) printf(\"%d%c\", v[i], i + 1 == (int)v.size() ? '\\n' : ' ');\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 2 3\n3\n2 3 4\n",
                "expected_stdout": "1 2 3 4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n5\n1\n5\n",
                "expected_stdout": "5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n1 2\n2\n3 4\n",
                "expected_stdout": "1 2 3 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n9 8 7\n2\n7 6\n",
                "expected_stdout": "6 7 8 9\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n0\n1\n1\n",
                "expected_stdout": "0 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n1 1 2 2\n3\n2 3 3\n",
                "expected_stdout": "1 2 3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【链表】链表插入排序",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 16,
        "tags": [
            "链表",
            "插入排序"
        ],
        "statement_md": "读入 `n` 和 `n` 个整数建成链表，用**插入排序**把链表排成升序后输出。\n\n**关键点**\n\n- 维护一个「已排好序」的子链表，每取一个新结点就在里面找到插入位置\n- 在链表上做插入排序不需要移动元素，只改指针 —— 这是它相对数组的优势\n- 输出一行",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：升序链表。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 链表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nstruct Node { int val; Node *next; };\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    Node dummy{0, nullptr};                   // dummy.next 是已排序部分的表头\n    for (int i = 0; i < n; i++) {\n        int v; scanf(\"%d\", &v);\n        Node *prev = &dummy;\n        while (prev->next && prev->next->val <= v) prev = prev->next;   // 找插入位置\n        prev->next = new Node{v, prev->next};\n    }\n    for (Node *p = dummy.next; p; p = p->next) printf(\"%d%c\", p->val, p->next ? ' ' : '\\n');\n    while (dummy.next) { Node *t = dummy.next; dummy.next = t->next; delete t; }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <vector>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    std::vector<int> v(n);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &v[i]);\n    std::sort(v.begin(), v.end());            // 等价的库函数版\n    for (int i = 0; i < n; i++) printf(\"%d%c\", v[i], i + 1 == n ? '\\n' : ' ');\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n3 1 4 1 5\n",
                "expected_stdout": "1 1 3 4 5\n",
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
                "stdin": "4\n4 3 2 1\n",
                "expected_stdout": "1 2 3 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n1 1 1\n",
                "expected_stdout": "1 1 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7\n-16 34 -33 -47 -31 -23 8\n",
                "expected_stdout": "-47 -33 -31 -23 -16 8 34\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n-13 49 -47 41 50 -46\n",
                "expected_stdout": "-47 -46 -13 41 49 50\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【链表】奇偶位分离",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "链表",
            "奇偶位",
            "分离"
        ],
        "statement_md": "读入 `n` 和 `n` 个整数建成链表，把**奇数位**（第 1、3、5…个）的结点排在前面，**偶数位**的排在后面，两段内部保持原顺序，输出结果。\n\n**关键点**\n\n- 按「位置」分而不是按「值」分 —— 别写成判断 `val % 2`\n- 和「按值分段」的写法一样：两个子链表尾插，最后相接\n- 输出一行",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：奇偶位分离后的链表。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 链表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nstruct Node { int val; Node *next; };\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    Node odd{0, nullptr}, *ot = &odd;\n    Node even{0, nullptr}, *et = &even;\n    for (int i = 1; i <= n; i++) {\n        int v; scanf(\"%d\", &v);\n        if (i % 2 == 1) { ot->next = new Node{v, nullptr}; ot = ot->next; }   // 按位置分\n        else            { et->next = new Node{v, nullptr}; et = et->next; }\n    }\n    ot->next = even.next;\n    for (Node *p = odd.next; p; p = p->next) printf(\"%d%c\", p->val, p->next ? ' ' : '\\n');\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <vector>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    std::vector<int> v(n);\n    for (int i = 0; i < n; i++) scanf(\"%d\", &v[i]);\n    std::vector<int> out;\n    for (int i = 0; i < n; i += 2) out.push_back(v[i]);\n    for (int i = 1; i < n; i += 2) out.push_back(v[i]);\n    for (int i = 0; i < n; i++) printf(\"%d%c\", out[i], i + 1 == n ? '\\n' : ' ');\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n1 2 3 4 5\n",
                "expected_stdout": "1 3 5 2 4\n",
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
                "stdin": "4\n10 20 30 40\n",
                "expected_stdout": "10 30 20 40\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n1 1 1 1 1 1\n",
                "expected_stdout": "1 1 1 1 1 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7\n-35 46 -40 -12 -13 -21 -24\n",
                "expected_stdout": "-35 -40 -13 -24 46 -12 -21\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n-4 3 -5 6 -3 5\n",
                "expected_stdout": "-4 -5 -3 3 6 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【链表】两个大数链表相加",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 16,
        "tags": [
            "链表",
            "大数",
            "进位"
        ],
        "statement_md": "两个非负整数的每一位按高位到低位存成链表。读入两个整数（十进制，位数 ≤ 30），按链表相加的做法求和后输出。\n\n**关键点**\n\n- 从低位往高位加，所以要先把链表逆序（或者干脆从字符串尾部扫）\n- 每一位 `sum = a + b + carry`，`carry = sum / 10`\n- 两个数可能有 30 位，超过 `long long`（19 位）—— 必须按位做",
        "input_format": "两行，各一个非负整数（位数 ≤ 30）。",
        "output_format": "一行：两数之和。",
        "constraints_md": "- 0 ≤ 数 ≤ 10³⁰\n- 位数 ≤ 30",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 链表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <cstring>\n#include <algorithm>\nstruct Node { int d; Node *next; };\nNode *build(const char *s) {                // 高位在前\n    Node *head = nullptr, *tail = nullptr;\n    for (int i = 0; s[i]; i++) {\n        Node *p = new Node{s[i] - '0', nullptr};\n        if (!head) head = tail = p; else { tail->next = p; tail = p; }\n    }\n    return head;\n}\nNode *reverse(Node *h) {\n    Node *prev = nullptr;\n    while (h) { Node *n = h->next; h->next = prev; prev = h; h = n; }\n    return prev;\n}\nint main() {\n    char sa[64], sb[64];\n    if (scanf(\"%63s\", sa) != 1) return 0;\n    if (scanf(\"%63s\", sb) != 1) return 0;\n    Node *a = reverse(build(sa));            // 逆序后低位在前\n    Node *b = reverse(build(sb));\n    int out[64], k = 0, carry = 0;\n    while (a || b || carry) {\n        int s = carry;\n        if (a) { s += a->d; a = a->next; }\n        if (b) { s += b->d; b = b->next; }\n        out[k++] = s % 10;\n        carry = s / 10;\n    }\n    while (k > 1 && out[k - 1] == 0) k--;    // 去掉前导零\n    for (int i = k - 1; i >= 0; i--) printf(\"%d\", out[i]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cstring>\nint main() {\n    char sa[64], sb[64];\n    if (scanf(\"%63s\", sa) != 1) return 0;\n    if (scanf(\"%63s\", sb) != 1) return 0;\n    int la = (int)strlen(sa), lb = (int)strlen(sb);\n    int n = la > lb ? la : lb;\n    int out[64] = {0}, carry = 0;\n    for (int i = 0; i < n; i++) {            // 直接从字符串尾部扫，不用链表\n        int da = i < la ? sa[la - 1 - i] - '0' : 0;\n        int db = i < lb ? sb[lb - 1 - i] - '0' : 0;\n        int s = da + db + carry;\n        out[i] = s % 10;\n        carry = s / 10;\n    }\n    if (carry) out[n++] = carry;\n    while (n > 1 && out[n - 1] == 0) n--;\n    for (int i = n - 1; i >= 0; i--) printf(\"%d\", out[i]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "123\n456\n",
                "expected_stdout": "579\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "0\n0\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "999\n1\n",
                "expected_stdout": "1000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n999999999999999999999\n",
                "expected_stdout": "1000000000000000000000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "123456789012345678901234567890\n987654321098765432109876543210\n",
                "expected_stdout": "1111111110111111111011111111100\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n5\n",
                "expected_stdout": "10\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【链表】删除倒数第 k 个结点",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 16,
        "tags": [
            "链表",
            "快慢指针",
            "倒数第k"
        ],
        "statement_md": "读入 `n k` 和 `n` 个整数建成链表，删除**倒数第 k 个**结点，输出剩余链表；删完为空输出 `empty`。`k` 超出范围时不删。\n\n**关键点**\n\n- 快慢指针：快指针先走 k 步，然后两个一起走，快指针到头时慢指针就在倒数第 k 个的**前驱**\n- `k == n` 时删的是表头，用哑结点一次处理掉\n- 输出一行",
        "input_format": "第一行 `n k`，第二行 `n` 个整数。",
        "output_format": "一行：剩余链表，或 `empty`。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 1 ≤ k ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 链表",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nstruct Node { int val; Node *next; };\nint main() {\n    int n, k;\n    if (scanf(\"%d %d\", &n, &k) != 2) return 0;\n    Node dummy{0, nullptr}, *tail = &dummy;\n    for (int i = 0; i < n; i++) {\n        int v; scanf(\"%d\", &v);\n        tail->next = new Node{v, nullptr};\n        tail = tail->next;\n    }\n    Node *fast = &dummy, *slow = &dummy;\n    for (int i = 0; i < k && fast; i++) fast = fast->next;   // 快指针先走 k 步\n    if (fast) {\n        while (fast->next) { fast = fast->next; slow = slow->next; }\n        Node *victim = slow->next;\n        slow->next = victim->next;\n        delete victim;\n    }\n    if (!dummy.next) { printf(\"empty\\n\"); return 0; }\n    for (Node *p = dummy.next; p; p = p->next) printf(\"%d%c\", p->val, p->next ? ' ' : '\\n');\n    while (dummy.next) { Node *t = dummy.next; dummy.next = t->next; delete t; }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n, k;\n    if (scanf(\"%d %d\", &n, &k) != 2) return 0;\n    static int val[1005], nxt[1005];\n    int head = -1, tail = -1;\n    for (int i = 0; i < n; i++) {\n        scanf(\"%d\", &val[i]); nxt[i] = -1;\n        if (head == -1) head = i; else nxt[tail] = i;\n        tail = i;\n    }\n    int idx = n - k;                       // 倒数第 k 个就是正数第 n-k+1 个\n    if (idx >= 0 && idx < n) {\n        if (idx == 0) head = nxt[head];\n        else {\n            int prev = head;\n            for (int i = 0; i < idx - 1; i++) prev = nxt[prev];\n            nxt[prev] = nxt[nxt[prev]];\n        }\n    }\n    if (head == -1) { printf(\"empty\\n\"); return 0; }\n    for (int p = head; p != -1; p = nxt[p]) printf(\"%d%c\", val[p], nxt[p] == -1 ? '\\n' : ' ');\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 1\n1 2 3 4 5\n",
                "expected_stdout": "1 2 3 4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5 5\n1 2 3 4 5\n",
                "expected_stdout": "2 3 4 5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 1\n7\n",
                "expected_stdout": "empty\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5 9\n1 2 3 4 5\n",
                "expected_stdout": "1 2 3 4 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3 2\n9 8 7\n",
                "expected_stdout": "9 7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6 3\n-38 13 31 -32 0 -43\n",
                "expected_stdout": "-38 13 31 0 -43\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    }
]
