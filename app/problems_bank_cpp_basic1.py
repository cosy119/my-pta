# -*- coding: utf-8 -*-
"""C++ 编程题第一册：输入输出 / 运算符 / 分支（36 题） —— 自动生成，**不要手改本文件**。

生成器：tools/gen_cpp_basic1.py
题数：35 题 / 210 测试点 / 总分 388

重生成：python tools/gen_cpp_basic1.py
"""

CPP_BASIC1_PROBLEMS: list[dict] = [
    {
        "title": "【输入输出】两数之和与差",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "C++基础",
            "输入输出",
            "整数运算"
        ],
        "statement_md": "读入两个整数 `a b`，输出它们的和与差。\n\n**关键点**\n\n- 先输出和，再输出差，各占一行\n- `a - b` 可能为负，别取绝对值",
        "input_format": "一行两个整数 `a b`。",
        "output_format": "两行：第一行 `a+b`，第二行 `a-b`。",
        "constraints_md": "- -10⁹ ≤ a, b ≤ 10⁹\n- 差最大 2×10⁹，仍在 `int` 内，但养成用 `long long` 的习惯更稳",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 输入输出与格式化",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    long long a, b;\n    if (scanf(\"%lld %lld\", &a, &b) != 2) return 0;\n    printf(\"%lld\\n\", a + b);\n    printf(\"%lld\\n\", a - b);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\nusing namespace std;\nint main() {\n    long long a, b;\n    cin >> a >> b;\n    cout << a + b << \"\\n\" << a - b << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3 5\n",
                "expected_stdout": "8\n-2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "0 0\n",
                "expected_stdout": "0\n0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "-7 4\n",
                "expected_stdout": "-3\n-11\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1000000000 -1000000000\n",
                "expected_stdout": "0\n2000000000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "12 12\n",
                "expected_stdout": "24\n0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "-3 -9\n",
                "expected_stdout": "-12\n6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【输入输出】三数平均值保留两位小数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "C++基础",
            "输入输出",
            "浮点",
            "类型转换"
        ],
        "statement_md": "读入三个整数，输出它们的算术平均值，保留两位小数。\n\n**关键点**\n\n- `(a+b+c)/3` 在整数上做会**截断**，必须先转 `double`\n- 输出用 `printf(\"%.2f\")` 或 `fixed << setprecision(2)`",
        "input_format": "一行三个整数 `a b c`。",
        "output_format": "一行，平均值，保留两位小数。",
        "constraints_md": "- -1000 ≤ a, b, c ≤ 1000",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 输入输出与格式化",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int a, b, c;\n    if (scanf(\"%d %d %d\", &a, &b, &c) != 3) return 0;\n    double avg = (a + b + c) / 3.0;      // 3.0 而非 3，否则先做整除\n    printf(\"%.2f\\n\", avg);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <iomanip>\nusing namespace std;\nint main() {\n    int a, b, c;\n    cin >> a >> b >> c;\n    cout << fixed << setprecision(2) << (a + b + c) / 3.0 << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "1 2 3\n",
                "expected_stdout": "2.00\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "10 20 30\n",
                "expected_stdout": "20.00\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "0 0 0\n",
                "expected_stdout": "0.00\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4 5 2\n",
                "expected_stdout": "3.67\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1 1 5\n",
                "expected_stdout": "2.33\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100 100 100\n",
                "expected_stdout": "100.00\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【输入输出】交换两个整数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "C++基础",
            "输入输出",
            "交换"
        ],
        "statement_md": "读入两个整数 `a b`，交换它们的值后输出。\n\n**关键点**\n\n- 输出顺序是**先原来的 b，再原来的 a**\n- 用临时变量最稳；异或交换虽然不用临时变量，但对同一变量自交换会清零",
        "input_format": "一行两个整数 `a b`。",
        "output_format": "一行两个整数：交换后的 `a b`。",
        "constraints_md": "- -10⁹ ≤ a, b ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 输入输出与格式化",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    long long a, b;\n    if (scanf(\"%lld %lld\", &a, &b) != 2) return 0;\n    long long t = a;                     // 临时变量，交换\n    a = b;\n    b = t;\n    printf(\"%lld %lld\\n\", a, b);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <utility>\nusing namespace std;\nint main() {\n    long long a, b;\n    cin >> a >> b;\n    swap(a, b);                          // 标准库直接换\n    cout << a << \" \" << b << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3 5\n",
                "expected_stdout": "5 3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "7 7\n",
                "expected_stdout": "7 7\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "0 -1\n",
                "expected_stdout": "-1 0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "-8 12\n",
                "expected_stdout": "12 -8\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100 200\n",
                "expected_stdout": "200 100\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2147483647 -2147483648\n",
                "expected_stdout": "-2147483648 2147483647\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【输入输出】按位宽 8 右对齐输出",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "C++基础",
            "格式化输出",
            "setw"
        ],
        "statement_md": "读入 `n` 个整数，每个整数占一行、宽度固定为 8、右对齐（左侧补空格）。\n\n**关键点**\n\n- 用 `printf(\"%8d\")` 或 `setw(8)`\n- `setw` 只对**下一个**输出生效，循环里每次都要写\n- 补的是空格不是 0；补 0 是 `%08d`，那是另一道题",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "`n` 行，每行一个宽度为 8 的整数。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- -9999999 ≤ x ≤ 9999999（含负号不超 8 位）",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 输入输出与格式化",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    for (int i = 0; i < n; i++) {\n        int x;\n        scanf(\"%d\", &x);\n        printf(\"%8d\\n\", x);              // 宽度 8 右对齐\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <iomanip>\nusing namespace std;\nint main() {\n    int n;\n    if (!(cin >> n)) return 0;\n    for (int i = 0; i < n; i++) {\n        int x;\n        cin >> x;\n        cout << setw(8) << x << \"\\n\";    // setw 到空格为止\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 22 333\n",
                "expected_stdout": "       1\n      22\n     333\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n0\n",
                "expected_stdout": "       0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n-1 -22 -333 -4444\n",
                "expected_stdout": "      -1\n     -22\n    -333\n   -4444\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n1234567 7654321\n",
                "expected_stdout": " 1234567\n 7654321\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n9 99 999 9999 99999\n",
                "expected_stdout": "       9\n      99\n     999\n    9999\n   99999\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n1000000 -1000000 5 -5 40 -40\n",
                "expected_stdout": " 1000000\n-1000000\n       5\n      -5\n      40\n     -40\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【输入输出】摄氏度转华氏度",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "C++基础",
            "格式化输出",
            "浮点",
            "EOF"
        ],
        "statement_md": "每行一个摄氏温度（整数），转成华氏温度输出，保留一位小数。\n\n换算公式：`F = C × 9 / 5 + 32`。\n\n**关键点**\n\n- `C * 9 / 5` 在整数里会截断，要写成 `C * 9.0 / 5`\n- 输入行数不定，读到文件末尾为止",
        "input_format": "若干行，每行一个整数摄氏温度。",
        "output_format": "每行一个华氏温度，保留一位小数。",
        "constraints_md": "- -100 ≤ C ≤ 200\n- 行数 ≤ 10",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 输入输出与格式化",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int c;\n    while (scanf(\"%d\", &c) == 1) {\n        printf(\"%.1f\\n\", c * 9.0 / 5 + 32);   // 9.0 保证浮点除法\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <iomanip>\nusing namespace std;\nint main() {\n    int c;\n    cout << fixed << setprecision(1);\n    while (cin >> c) {\n        cout << c * 9.0 / 5 + 32 << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "0\n100\n37\n",
                "expected_stdout": "32.0\n212.0\n98.6\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "-40\n",
                "expected_stdout": "-40.0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "25\n66\n",
                "expected_stdout": "77.0\n150.8\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "36\n38\n",
                "expected_stdout": "96.8\n100.4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "-100 -1 0 1\n",
                "expected_stdout": "-148.0\n30.2\n32.0\n33.8\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10 20 -10 -20 50\n",
                "expected_stdout": "50.0\n68.0\n14.0\n-4.0\n122.0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【输入输出】秒数换算成时分秒",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "C++基础",
            "整除取模",
            "输入输出"
        ],
        "statement_md": "读入一个非负整数表示的总秒数，换算成 `时 分 秒` 输出。\n\n**关键点**\n\n- 一小时 3600 秒、一分 60 秒\n- 秒数可达 10⁹，用 `long long`\n- 三个数之间用一个空格分隔，不足的位不补零",
        "input_format": "一行一个整数 `s`（总秒数）。",
        "output_format": "一行三个整数 `h m sec`，空格分隔。",
        "constraints_md": "- 0 ≤ s ≤ 10¹²",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 输入输出与格式化",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    long long s;\n    if (scanf(\"%lld\", &s) != 1) return 0;\n    long long h = s / 3600;\n    long long m = s % 3600 / 60;\n    long long sec = s % 60;\n    printf(\"%lld %lld %lld\\n\", h, m, sec);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\nusing namespace std;\nint main() {\n    long long s;\n    cin >> s;\n    cout << s / 3600 << \" \" << (s / 60) % 60 << \" \" << s % 60 << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "0\n",
                "expected_stdout": "0 0 0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3661\n",
                "expected_stdout": "1 1 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "59\n",
                "expected_stdout": "0 0 59\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3600\n",
                "expected_stdout": "1 0 0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "86399\n",
                "expected_stdout": "23 59 59\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1000000000\n",
                "expected_stdout": "277777 46 40\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【输入输出】圆的周长与面积",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "常量",
            "格式化输出"
        ],
        "statement_md": "读入圆的半径（整数），用 `π = 3.14159` 计算周长与面积，各保留两位小数。\n\n公式：周长 `2πr`，面积 `πr²`。\n\n**关键点**\n\n- `π` 是常量，别写成变量被后续语句改掉\n- 面积是 `3.14159 * r * r`，不要写成 `3.14159 * r ^ 2`（`^` 在 C++ 里是异或）\n- 两行输出：先周长后面积",
        "input_format": "一行一个整数 `r`。",
        "output_format": "两行：第一行周长，第二行面积，均保留两位小数。",
        "constraints_md": "- 1 ≤ r ≤ 1000",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 输入输出与格式化",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nconst double PI = 3.14159;\nint main() {\n    int r;\n    if (scanf(\"%d\", &r) != 1) return 0;\n    printf(\"%.2f\\n\", 2 * PI * r);\n    printf(\"%.2f\\n\", PI * r * r);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <iomanip>\nusing namespace std;\n#define PI 3.14159\nint main() {\n    int r;\n    cin >> r;\n    double area = PI * (double)r * (double)r;\n    cout << fixed << setprecision(2);\n    cout << 2 * PI * r << \"\\n\" << area << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "1\n",
                "expected_stdout": "6.28\n3.14\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n",
                "expected_stdout": "12.57\n12.57\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n",
                "expected_stdout": "18.85\n28.27\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n",
                "expected_stdout": "31.42\n78.54\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n",
                "expected_stdout": "62.83\n314.16\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7\n",
                "expected_stdout": "43.98\n153.94\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【输入输出】字符的 ASCII 码",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "C++基础",
            "字符",
            "ASCII",
            "类型转换"
        ],
        "statement_md": "读入 `n` 个用空格分隔的可见字符，逐个输出它们的 ASCII 码。\n\n**关键点**\n\n- `char` 参与算术运算时会自动转成整数，所以 `(int)c` 与 `c` 直接输出不同\n- 用 `scanf(\" %c\")` 读字符：格式串前的空格会跳过空白符，否则会把上一行残留的换行读进来",
        "input_format": "第一行 `n`；第二行 `n` 个字符，空格分隔。",
        "output_format": "`n` 行，每行一个整数。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 字符均在可见 ASCII 范围内（33~126）",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 输入输出与格式化",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    for (int i = 0; i < n; i++) {\n        char c;\n        scanf(\" %c\", &c);            // 前导空格跳过空白符\n        printf(\"%d\\n\", (int)c);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\nusing namespace std;\nint main() {\n    int n;\n    cin >> n;\n    for (int i = 0; i < n; i++) {\n        char c;\n        cin >> c;                    // cin >> char 自动跳过空白\n        cout << static_cast<int>(c) << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\nA a 0\n",
                "expected_stdout": "65\n97\n48\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\nZ\n",
                "expected_stdout": "90\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n+ _ 9 ~\n",
                "expected_stdout": "43\n95\n57\n126\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n! ?\n",
                "expected_stdout": "33\n63\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\nb c d e f\n",
                "expected_stdout": "98\n99\n100\n101\n102\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\nX y 5\n",
                "expected_stdout": "88\n121\n53\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【输入输出】各数位之和",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "循环",
            "数位分解"
        ],
        "statement_md": "读入 `n` 个整数，逐个输出「它各位数字之和」。负数按**绝对值**处理。\n\n**关键点**\n\n- 循环里 `x % 10` 取个位、`x /= 10` 砍掉个位，直到 `x == 0`\n- 负数直接取模会得到负数，先取绝对值\n- 0 的各位和是 0（循环一次都不进）",
        "input_format": "第一行 `n`；第二行 `n` 个整数。",
        "output_format": "`n` 行，每行一个整数。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- -10⁹ ≤ x ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 输入输出与格式化",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    for (int i = 0; i < n; i++) {\n        long long x;\n        scanf(\"%lld\", &x);\n        if (x < 0) x = -x;\n        int s = 0;\n        while (x > 0) { s += (int)(x % 10); x /= 10; }\n        printf(\"%d\\n\", s);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cstdlib>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        char buf[32];\n        scanf(\"%s\", buf);                 // 当字符串读，逐字符累加数字值\n        int s = 0;\n        for (int i = 0; buf[i]; i++)\n            if (buf[i] >= '0' && buf[i] <= '9') s += buf[i] - '0';\n        printf(\"%d\\n\", s);\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n123 456 0\n",
                "expected_stdout": "6\n15\n0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n-987\n",
                "expected_stdout": "24\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n9 10 100 1000\n",
                "expected_stdout": "9\n1\n1\n1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n-1 -100\n",
                "expected_stdout": "1\n1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n2147483647 999999999 1000000000 -1000000000 5\n",
                "expected_stdout": "46\n81\n1\n1\n5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n11 22 33\n",
                "expected_stdout": "2\n4\n6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【输入输出】三种进制各输出一行",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "进制转换",
            "格式化输出"
        ],
        "statement_md": "读入 `n` 个非负整数，对每个数输出三行：十进制、八进制、十六进制（**大写**字母）。\n\n**关键点**\n\n- `printf` 的格式符：`%d` 十进制、`%o` 八进制、`%X` 大写十六进制\n- 八进制和十六进制**不加** `0` / `0x` 前缀（加了就多字符，直接判错）",
        "input_format": "第一行 `n`；第二行 `n` 个非负整数。",
        "output_format": "对每个数输出三行，依次是十进制、八进制、十六进制。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 0 ≤ x ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 输入输出与格式化",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    for (int i = 0; i < n; i++) {\n        unsigned x;\n        scanf(\"%u\", &x);\n        printf(\"%u\\n\", x);\n        printf(\"%o\\n\", x);\n        printf(\"%X\\n\", x);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <iomanip>\nusing namespace std;\nint main() {\n    int n;\n    cin >> n;\n    while (n--) {\n        unsigned x;\n        cin >> x;\n        cout << dec << x << \"\\n\"\n             << oct << x << \"\\n\"\n             << hex << uppercase << x << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "2\n255 8\n",
                "expected_stdout": "255\n377\nFF\n8\n10\n8\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n0\n",
                "expected_stdout": "0\n0\n0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n16 4095 1\n",
                "expected_stdout": "16\n20\n10\n4095\n7777\nFFF\n1\n1\n1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n1000000000 123456789\n",
                "expected_stdout": "1000000000\n7346545000\n3B9ACA00\n123456789\n726746425\n75BCD15\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n7 8 15 16\n",
                "expected_stdout": "7\n7\n7\n8\n10\n8\n15\n17\nF\n16\n20\n10\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n1048576\n",
                "expected_stdout": "1048576\n4000000\n100000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【输入输出】补零到 5 位",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "格式化输出",
            "补零"
        ],
        "statement_md": "读入 `n` 个非负整数，每个占一行、宽度固定 5、左侧**补 0**。\n\n**关键点**\n\n- 格式符是 `%05d`：宽度 5 且用 0 填充\n- `%5d` 补的是空格，不是 0 —— 一字之差结果全错\n- 数本身超过 5 位时原样输出，不截断",
        "input_format": "第一行 `n`；第二行 `n` 个非负整数。",
        "output_format": "`n` 行，每行一个 5 位（至少）的数。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 0 ≤ x ≤ 999999",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 输入输出与格式化",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    for (int i = 0; i < n; i++) {\n        int x;\n        scanf(\"%d\", &x);\n        printf(\"%05d\\n\", x);          // 宽度 5，补 0\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <iomanip>\nusing namespace std;\nint main() {\n    int n;\n    cin >> n;\n    while (n--) {\n        int x;\n        cin >> x;\n        cout << setfill('0') << setw(5) << x << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 22 333\n",
                "expected_stdout": "00001\n00022\n00333\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n0\n",
                "expected_stdout": "00000\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n9 99 999 9999\n",
                "expected_stdout": "00009\n00099\n00999\n09999\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n12345 123456\n",
                "expected_stdout": "12345\n123456\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n1 2 3 4 5\n",
                "expected_stdout": "00001\n00002\n00003\n00004\n00005\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n10000 1000 100\n",
                "expected_stdout": "10000\n01000\n00100\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【输入输出】读到文件末尾求和",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "EOF",
            "循环读取"
        ],
        "statement_md": "输入若干行，每行两个整数，输出它们的和（每行一个结果）。\n\n**关键点**\n\n- 行数未知，用 `while (scanf(...) == 2)` 或 `while (cin >> a >> b)`\n- 注意判断的是**读到了两个数**，不是 `!= EOF`（后者遇到残缺行会算错）",
        "input_format": "若干行，每行两个整数。",
        "output_format": "每行一个整数，为对应行的和。",
        "constraints_md": "- 行数 ≤ 10\n- -10⁹ ≤ a, b ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 输入输出与格式化",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    long long a, b;\n    while (scanf(\"%lld %lld\", &a, &b) == 2) {   // 恰读到两个数才算一条\n        printf(\"%lld\\n\", a + b);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\nusing namespace std;\nint main() {\n    long long a, b;\n    while (cin >> a >> b) {\n        cout << a + b << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "1 2\n3 4\n",
                "expected_stdout": "3\n7\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "0 0\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "-5 5\n100 -100\n7 8\n",
                "expected_stdout": "0\n0\n15\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1000000000 1000000000\n",
                "expected_stdout": "2000000000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1 1\n2 2\n3 3\n4 4\n",
                "expected_stdout": "2\n4\n6\n8\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "-1 -2\n-3 -4\n-5 -6\n",
                "expected_stdout": "-3\n-7\n-11\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【运算】整数除法的商与余数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "C++基础",
            "整除",
            "取模",
            "负数"
        ],
        "statement_md": "每行两个非零整数 `a b`，输出 `a / b` 的商与余数，各占一行。\n\n**关键点**\n\n- C++ 的整数除法是**向零截断**：`-7 / 2 == -3`，不是 `-4`\n- 余数满足 `a == q * b + r`，符号跟着被除数走：`-7 % 2 == -1`\n- Python 的 `//` 向负无穷取整，本题不能用它直接算",
        "input_format": "若干行，每行两个非零整数。",
        "output_format": "对每行输出两行：商、余数。",
        "constraints_md": "- |a|, |b| ≤ 10⁹，b ≠ 0\n- 行数 ≤ 6",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 运算符与表达式",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    long long a, b;\n    while (scanf(\"%lld %lld\", &a, &b) == 2) {\n        printf(\"%lld\\n\", a / b);      // C++ 整数除法：向零截断\n        printf(\"%lld\\n\", a % b);      // 余数符号同被除数\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    long long a, b;\n    while (scanf(\"%lld %lld\", &a, &b) == 2) {\n        long long q = (a - a % b) / b;   // 先用余数修正，再整除\n        printf(\"%lld\\n%lld\\n\", q, a - q * b);\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "7 2\n-7 2\n",
                "expected_stdout": "3\n1\n-3\n-1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "7 -2\n",
                "expected_stdout": "-3\n1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "-7 -2\n8 3\n-8 3\n",
                "expected_stdout": "3\n-1\n2\n2\n-2\n-2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1 1\n-1 1\n",
                "expected_stdout": "1\n0\n-1\n0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100 7\n-100 7\n",
                "expected_stdout": "14\n2\n-14\n-2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2147483647 2\n",
                "expected_stdout": "1073741823\n1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【运算】整除、浮点除与取模",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "C++基础",
            "整除",
            "浮点除法"
        ],
        "statement_md": "读入两个整数 `a b`（`b > 0`），分别输出：\n\n1. `a / b` 的整除结果\n2. `a / b` 的浮点结果（保留三位小数）\n3. `a % b`\n\n**关键点**\n\n- 整除与浮点除的差别只在于**有没有一个 double 参与**\n- `a / b` 两个都是 `int` 时先算整除，再赋给 `double` 已经晚了\n- `(double)a / b` 与 `a / (double)b` 等价，`(double)(a / b)` 不等价",
        "input_format": "一行两个整数 `a b`。",
        "output_format": "三行：整除结果、浮点结果（三位小数）、余数。",
        "constraints_md": "- -10⁶ ≤ a ≤ 10⁶，1 ≤ b ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 运算符与表达式",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int a, b;\n    if (scanf(\"%d %d\", &a, &b) != 2) return 0;\n    printf(\"%d\\n\", a / b);\n    printf(\"%.3f\\n\", (double)a / b);      // 先转 double 再除\n    printf(\"%d\\n\", a % b);\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <iomanip>\nusing namespace std;\nint main() {\n    int a, b;\n    cin >> a >> b;\n    div_t d = div(a, b);                  // 标准库一次拿到商和余数\n    cout << d.quot << \"\\n\"\n         << fixed << setprecision(3) << (double)a / b << \"\\n\"\n         << d.rem << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "7 2\n",
                "expected_stdout": "3\n3.500\n1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 3\n",
                "expected_stdout": "0\n0.333\n1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "-7 2\n",
                "expected_stdout": "-3\n-3.500\n-1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10 5\n",
                "expected_stdout": "2\n2.000\n0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1000000 7\n",
                "expected_stdout": "142857\n142857.143\n1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "0 9\n",
                "expected_stdout": "0\n0.000\n0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【运算】自增自减的求值顺序",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "自增",
            "运算符"
        ],
        "statement_md": "读入一个整数 `a`，按顺序执行下面四条语句，每条执行后输出此刻 `a` 的值：\n\n```cpp\n`a++`、`a`、`++a`、`a`\n```\n\n也就是输出四个数，用来看清**后缀先用后加、前缀先加后用**。\n\n**关键点**\n\n- `a++` 的值是**加之前**的 a，`++a` 的值是**加之后**的 a\n- 每条语句单独一行，别塞进同一个表达式（`a++ + ++a` 是未定义行为）\n- 四条语句顺序执行，不是四条独立测试",
        "input_format": "一行一个整数 `a`。",
        "output_format": "四行，依次是四条语句执行后的 `a`。",
        "constraints_md": "- 0 ≤ a ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 运算符与表达式",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    long long a;\n    if (scanf(\"%lld\", &a) != 1) return 0;\n    printf(\"%lld\\n\", a++);      // 输出旧值，a 变 a+1\n    printf(\"%lld\\n\", a);        // 此时已是 a+1\n    printf(\"%lld\\n\", ++a);      // 先加，输出 a+2\n    printf(\"%lld\\n\", a);        // 仍是 a+2\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\nusing namespace std;\nint main() {\n    long long a;\n    cin >> a;\n    long long v1 = a;           // 后缀：先取值\n    a = a + 1;                  // 再加\n    cout << v1 << \"\\n\";\n    cout << a << \"\\n\";\n    a = a + 1;                  // 前缀：先加\n    cout << a << \"\\n\";          // 再取值\n    cout << a << \"\\n\";\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n",
                "expected_stdout": "5\n6\n7\n7\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "0\n",
                "expected_stdout": "0\n1\n2\n2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n",
                "expected_stdout": "1\n2\n3\n3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "-3\n",
                "expected_stdout": "-3\n-2\n-1\n-1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100\n",
                "expected_stdout": "100\n101\n102\n102\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "9\n",
                "expected_stdout": "9\n10\n11\n11\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【运算】位运算五种基本操作",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "位运算",
            "移位"
        ],
        "statement_md": "读入 `n` 对非负整数，对每对输出四行：`a & b`、`a | b`、`a ^ b`、`a << 1`。\n\n**关键点**\n\n- `&` `|` `^` 是**逐位**运算，不是逻辑运算；`&&` `||` 才返回 0/1\n- `a << 1` 相当于乘 2，但溢出不报错，本题数据保证不溢出\n- 四行顺序固定：与、或、异或、左移一位",
        "input_format": "第一行 `n`；接下来 `n` 行，每行两个非负整数 `a b`。",
        "output_format": "对每对输出四行，依次是 `a&b`、`a|b`、`a^b`、`a<<1`。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 0 ≤ a, b ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 运算符与表达式",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    for (int i = 0; i < n; i++) {\n        int a, b;\n        scanf(\"%d %d\", &a, &b);\n        printf(\"%d\\n\", a & b);\n        printf(\"%d\\n\", a | b);\n        printf(\"%d\\n\", a ^ b);\n        printf(\"%d\\n\", a << 1);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\nusing namespace std;\nint main() {\n    int n;\n    cin >> n;\n    while (n--) {\n        int a, b;\n        cin >> a >> b;\n        cout << (a & b) << \"\\n\"\n             << (a | b) << \"\\n\"\n             << (a ^ b) << \"\\n\"\n             << a * 2 << \"\\n\";       // 移位等价于乘 2\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "2\n5 3\n12 10\n",
                "expected_stdout": "1\n7\n6\n10\n8\n14\n6\n24\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n0 0\n",
                "expected_stdout": "0\n0\n0\n0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n1 2\n7 8\n255 15\n",
                "expected_stdout": "0\n3\n3\n2\n0\n15\n15\n14\n15\n255\n240\n510\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n1000000 999999\n1 1\n",
                "expected_stdout": "999936\n1000063\n127\n2000000\n1\n1\n0\n2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n16 32\n63 64\n9 6\n3 5\n",
                "expected_stdout": "0\n48\n48\n32\n0\n127\n127\n126\n0\n15\n15\n18\n1\n7\n6\n6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n1073741823 1\n",
                "expected_stdout": "1\n1073741823\n1073741822\n2147483646\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【运算】负数取模的符号",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "取模",
            "负数",
            "易错"
        ],
        "statement_md": "读入 `n` 对整数 `a b`（`b > 0`），输出 `a % b`。\n\n本题专门考 C++ 的取模规则：**余数的符号跟着被除数走**。\n\n**关键点**\n\n- `-7 % 3 == -1`，不是 `2`（那是数学上的「最小非负剩余」）\n- 若想要非负余数，得写 `((a % b) + b) % b`\n- 本题按 C++ 原生语义输出，**不要**做非负化",
        "input_format": "第一行 `n`；接下来 `n` 行，每行 `a b`（`b > 0`）。",
        "output_format": "`n` 行，每行 `a % b` 的结果。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- -10⁹ ≤ a ≤ 10⁹，1 ≤ b ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 运算符与表达式",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    for (int i = 0; i < n; i++) {\n        long long a, b;\n        scanf(\"%lld %lld\", &a, &b);\n        printf(\"%lld\\n\", a % b);       // 余数符号随被除数\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        long long a, b;\n        scanf(\"%lld %lld\", &a, &b);\n        long long q = a / b;           // 先用除法求商\n        printf(\"%lld\\n\", a - q * b);   // 再由 a - q*b 得余数\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n-7 3\n7 -3\n-7 -3\n",
                "expected_stdout": "-1\n1\n-1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n10 4\n-10 4\n",
                "expected_stdout": "2\n-2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n0 5\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n-1 2\n-2 3\n-3 4\n-100 7\n",
                "expected_stdout": "-1\n-2\n-3\n-2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n1000000000 7\n-1000000000 7\n",
                "expected_stdout": "6\n-6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n5 5\n-5 5\n5 1\n",
                "expected_stdout": "0\n0\n0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【运算】三目运算符求最大值",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "C++基础",
            "三目运算符",
            "最大值"
        ],
        "statement_md": "读入 `n` 组，每组三个整数，用**三目运算符** `? :` 输出最大值。\n\n**关键点**\n\n- `a > b ? a : b` 可以嵌套：`(a > b ? a : b) > c ? ... : ...`\n- 三目运算符有优先级，嵌套时建议加括号\n- 相等的情况任取一个都行，结果一样",
        "input_format": "第一行 `n`；接下来 `n` 行，每行三个整数 `a b c`。",
        "output_format": "`n` 行，每行一个整数。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- |a|, |b|, |c| ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 运算符与表达式",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        long long a, b, c;\n        scanf(\"%lld %lld %lld\", &a, &b, &c);\n        long long m = (a > b ? a : b);\n        m = (m > c ? m : c);            // 三目嵌套，别忘括号\n        printf(\"%lld\\n\", m);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <algorithm>\nusing namespace std;\nint main() {\n    int n;\n    cin >> n;\n    while (n--) {\n        long long a[3];\n        cin >> a[0] >> a[1] >> a[2];\n        cout << max(a[0], max(a[1], a[2])) << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n1 2 3\n3 2 1\n2 3 1\n",
                "expected_stdout": "3\n3\n3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n-1 -2 -3\n",
                "expected_stdout": "-1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n5 5 5\n0 0 1\n",
                "expected_stdout": "5\n1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n-100 0 100\n7 7 1\n-9 -9 -9\n",
                "expected_stdout": "100\n7\n-9\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n2147483647 0 -1\n",
                "expected_stdout": "2147483647\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n1 0 0\n0 1 0\n0 0 1\n1 1 0\n",
                "expected_stdout": "1\n1\n1\n1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【运算】混合表达式的优先级求值",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "运算符优先级",
            "整除"
        ],
        "statement_md": "读入 `n` 组六个整数 `a b c d e f`，计算并输出下面这个表达式的值：\n\n```cpp\n`a + b * c - d / e % f`\n```\n\n其中 `/` 是整除。数据保证 `e != 0`、`f != 0`。\n\n**关键点**\n\n- 优先级：`* / %` 同级且高于 `+ -`，同级**从左到右**\n- 所以 `d / e % f` 先算 `d / e`，结果再 `% f`\n- 不要自作主张加括号改变结合顺序",
        "input_format": "第一行 `n`；接下来 `n` 行，每行六个整数。",
        "output_format": "`n` 行，每行一个整数。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- |a|~|f| ≤ 100，e ≠ 0，f ≠ 0",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 运算符与表达式",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        int a, b, c, d, e, f;\n        scanf(\"%d %d %d %d %d %d\", &a, &b, &c, &d, &e, &f);\n        int v = a + b * c - d / e % f;   // 按优先级从左到右\n        printf(\"%d\\n\", v);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        int a, b, c, d, e, f;\n        scanf(\"%d %d %d %d %d %d\", &a, &b, &c, &d, &e, &f);\n        int t1 = b * c;                  // 手工拆成三步，等价于优先级\n        int t2 = d / e;\n        t2 = t2 % f;\n        printf(\"%d\\n\", a + t1 - t2);\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "2\n1 2 3 4 2 3\n0 0 0 0 1 1\n",
                "expected_stdout": "5\n0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n5 6 7 8 3 2\n",
                "expected_stdout": "47\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n1 1 1 1 1 1\n-1 -2 -3 -4 -5 -6\n2 3 4 5 6 7\n",
                "expected_stdout": "2\n5\n14\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n100 100 100 100 100 100\n",
                "expected_stdout": "10099\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n0 5 0 9 2 4\n3 0 3 0 1 2\n",
                "expected_stdout": "0\n3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n7 3 9 11 4 5\n",
                "expected_stdout": "32\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【运算】闰年判定",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "C++基础",
            "逻辑运算",
            "闰年"
        ],
        "statement_md": "读入 `n` 个年份，判断是否闰年：是输出 `YES`，否输出 `NO`。\n\n闰年规则：能被 4 整除但不能被 100 整除，**或者**能被 400 整除。\n\n**关键点**\n\n- `y % 4 == 0 && y % 100 != 0 || y % 400 == 0` —— `&&` 优先级高于 `||`，但加括号更清楚\n- 1900 不是闰年（能被 100 整除且不能被 400 整除），2000 是\n- 输出必须大写",
        "input_format": "第一行 `n`；第二行 `n` 个正整数年份。",
        "output_format": "`n` 行，每行 `YES` 或 `NO`。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 1 ≤ year ≤ 9999",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 运算符与表达式",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    for (int i = 0; i < n; i++) {\n        int y;\n        scanf(\"%d\", &y);\n        bool leap = (y % 4 == 0 && y % 100 != 0) || (y % 400 == 0);\n        printf(\"%s\\n\", leap ? \"YES\" : \"NO\");\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\nusing namespace std;\nint main() {\n    int n;\n    cin >> n;\n    while (n--) {\n        int y;\n        cin >> y;\n        bool leap = false;\n        if (y % 400 == 0) leap = true;\n        else if (y % 100 == 0) leap = false;\n        else if (y % 4 == 0) leap = true;\n        cout << (leap ? \"YES\" : \"NO\") << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4\n1900 2000 2024 2023\n",
                "expected_stdout": "NO\nYES\nYES\nNO\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n1600 1700\n",
                "expected_stdout": "YES\nNO\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n4\n",
                "expected_stdout": "YES\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n100 400 1000\n",
                "expected_stdout": "NO\nYES\nNO\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n1996 1999 2004 2100 2400\n",
                "expected_stdout": "YES\nNO\nYES\nNO\nYES\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n9999\n",
                "expected_stdout": "NO\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【运算】绝对值与符号（禁用 abs）",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "C++基础",
            "条件表达式",
            "符号"
        ],
        "statement_md": "读入 `n` 个整数，对每个输出两个数：它的绝对值、它的符号（正 1 / 零 0 / 负 -1）。\n\n**不许调用 `abs()` / `fabs()`**，请用条件表达式自己写。\n\n**关键点**\n\n- `x < 0 ? -x : x` 就是绝对值；注意 `-INT_MIN` 会溢出，本题数据不涉及\n- 符号不要写成 `x > 0`，那样零会落到 -1 分支\n- 两个数在同一行，空格分隔",
        "input_format": "第一行 `n`；第二行 `n` 个整数。",
        "output_format": "`n` 行，每行两个整数 `|x| sign`。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- -10⁹ ≤ x ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 运算符与表达式",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    for (int i = 0; i < n; i++) {\n        long long x;\n        scanf(\"%lld\", &x);\n        long long a = (x < 0 ? -x : x);          // 自己写绝对值\n        int s = (x > 0) - (x < 0);               // 符号：1 / 0 / -1\n        printf(\"%lld %d\\n\", a, s);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\nusing namespace std;\nint main() {\n    int n;\n    cin >> n;\n    while (n--) {\n        long long x;\n        cin >> x;\n        long long a;\n        int s;\n        if (x > 0)      { a = x;  s = 1; }\n        else if (x < 0) { a = -x; s = -1; }\n        else            { a = 0;  s = 0; }\n        cout << a << \" \" << s << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4\n-5 0 3 -1\n",
                "expected_stdout": "5 -1\n0 0\n3 1\n1 -1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n0\n",
                "expected_stdout": "0 0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n100 -100 1\n",
                "expected_stdout": "100 1\n100 -1\n1 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n-2147483647 2147483647\n",
                "expected_stdout": "2147483647 -1\n2147483647 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n-2 -1 0 1 2\n",
                "expected_stdout": "2 -1\n1 -1\n0 0\n1 1\n2 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n-999999999\n",
                "expected_stdout": "999999999 -1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【运算】复合赋值运算链",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "复合赋值",
            "整除"
        ],
        "statement_md": "读入 `n` 个整数 `x`，对每个依次执行：\n\n```cpp\n`x += 3;  x *= 2;  x -= 4;  x /= 2;  x %= 7;`\n```\n\n输出每一步执行后的 `x`，共五行。\n\n**关键点**\n\n- `x /= 2` 是整除（向零截断），负数会往零靠\n- `x %= 7` 的结果符号跟 `x` 走\n- 五行顺序固定，别合并",
        "input_format": "第一行 `n`；第二行 `n` 个整数。",
        "output_format": "对每个 `x` 输出五行，每行一个整数。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- -10⁶ ≤ x ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 运算符与表达式",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        long long x;\n        scanf(\"%lld\", &x);\n        x += 3; printf(\"%lld\\n\", x);\n        x *= 2; printf(\"%lld\\n\", x);\n        x -= 4; printf(\"%lld\\n\", x);\n        x /= 2; printf(\"%lld\\n\", x);\n        x %= 7; printf(\"%lld\\n\", x);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    for (int i = 0; i < n; i++) {\n        long long x;\n        scanf(\"%lld\", &x);\n        long long r[5];\n        r[0] = x + 3;\n        r[1] = r[0] * 2;\n        r[2] = r[1] - 4;\n        r[3] = r[2] / 2;\n        r[4] = r[3] % 7;\n        for (int k = 0; k < 5; k++) printf(\"%lld\\n\", r[k]);\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "2\n0 1\n",
                "expected_stdout": "3\n6\n2\n1\n1\n4\n8\n4\n2\n2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n-10\n",
                "expected_stdout": "-7\n-14\n-18\n-9\n-2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n100 -100 7\n",
                "expected_stdout": "103\n206\n202\n101\n3\n-97\n-194\n-198\n-99\n-1\n10\n20\n16\n8\n1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n5 -5\n",
                "expected_stdout": "8\n16\n12\n6\n6\n-2\n-4\n-8\n-4\n-4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n999999\n",
                "expected_stdout": "1000002\n2000004\n2000000\n1000000\n1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n2 4 6\n",
                "expected_stdout": "5\n10\n6\n3\n3\n7\n14\n10\n5\n5\n9\n18\n14\n7\n0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【运算】类型转换的三条路",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "类型转换",
            "字符"
        ],
        "statement_md": "读入 `n` 个整数 `x`（32 ≤ x ≤ 126），对每个输出三行：\n\n1. `(char)x` 对应的字符\n2. `(double)x / 4` 的结果，保留两位小数\n3. `(int)(x / 4.0)` 的结果\n\n**关键点**\n\n- `(char)x` 与 `char c = x` 等价，都是把整数截成 1 字节\n- 第 3 行是**先算浮点再截断**，等于向下取整（正数情况下）\n- 第 2 行别写成 `(double)(x / 4)`，那样先整除再转，结果不一样",
        "input_format": "第一行 `n`；第二行 `n` 个整数。",
        "output_format": "对每个 `x` 输出三行：字符、两位小数、整数。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 32 ≤ x ≤ 126",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 运算符与表达式",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        int x;\n        scanf(\"%d\", &x);\n        printf(\"%c\\n\", (char)x);              // 整数按字节解释成字符\n        printf(\"%.2f\\n\", (double)x / 4);      // 先转 double 再除\n        printf(\"%d\\n\", (int)(x / 4.0));       // 浮点结果再截断\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <iomanip>\nusing namespace std;\nint main() {\n    int n;\n    cin >> n;\n    while (n--) {\n        int x;\n        cin >> x;\n        char c = static_cast<char>(x);\n        double d = x / 4.0;\n        int t = static_cast<int>(d);\n        cout << c << \"\\n\" << fixed << setprecision(2) << d << \"\\n\" << t << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n65 97 48\n",
                "expected_stdout": "A\n16.25\n16\na\n24.25\n24\n0\n12.00\n12\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n126\n",
                "expected_stdout": "~\n31.50\n31\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n32 33 34 35\n",
                "expected_stdout": " \n8.00\n8\n!\n8.25\n8\n\"\n8.50\n8\n#\n8.75\n8\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n90 122\n",
                "expected_stdout": "Z\n22.50\n22\nz\n30.50\n30\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n80 81 82 83 84\n",
                "expected_stdout": "P\n20.00\n20\nQ\n20.25\n20\nR\n20.50\n20\nS\n20.75\n20\nT\n21.00\n21\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n100\n",
                "expected_stdout": "d\n25.00\n25\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【分支】分段函数求值",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "C++基础",
            "if-else",
            "分段函数"
        ],
        "statement_md": "按下面的分段函数计算 `y`：\n\n```\n`x < 0`   →  `y = 2x + 1`\n`x == 0`  →  `y = 0`\n`x > 0`   →  `y = x * x - 1`\n```\n\n**关键点**\n\n- 三段互斥，用 `if / else if / else`，不要写成三个独立 `if`\n- `x == 0` 必须单独判，别漏\n- 输出是整数，一行一个",
        "input_format": "第一行 `n`；第二行 `n` 个整数 `x`。",
        "output_format": "`n` 行，每行一个整数 `y`。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- -1000 ≤ x ≤ 1000",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 分支结构",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        long long x, y;\n        scanf(\"%lld\", &x);\n        if (x < 0)       y = 2 * x + 1;\n        else if (x == 0) y = 0;\n        else             y = x * x - 1;\n        printf(\"%lld\\n\", y);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\nusing namespace std;\nint main() {\n    int n;\n    cin >> n;\n    while (n--) {\n        long long x, y;\n        cin >> x;\n        if (x == 0)      y = 0;\n        else if (x < 0)  y = 2 * x + 1;\n        else             y = x * x - 1;\n        cout << y << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4\n-2 0 3 1\n",
                "expected_stdout": "-3\n0\n8\n0\n",
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
                "stdin": "3\n-1 -5 -100\n",
                "expected_stdout": "-1\n-9\n-199\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n10 100\n",
                "expected_stdout": "99\n9999\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n-3 -2 -1 0 1\n",
                "expected_stdout": "-5\n-3\n-1\n0\n0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n1000\n",
                "expected_stdout": "999999\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【分支】成绩等级判定",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "C++基础",
            "if-else",
            "成绩等级"
        ],
        "statement_md": "读入 `n` 个百分制成绩（整数 0~100），按下面规则输出等级：\n\n```\n90 ~ 100 → A\n80 ~ 89  → B\n70 ~ 79  → C\n60 ~ 69  → D\n 0 ~ 59  → E\n```\n\n**关键点**\n\n- 从高到低判，每个分支用 `else if`，不要写成独立 `if`\n- 90 分算 A，60 分算 D（边界要含等号）\n- 输出单个大写字母，一行一个",
        "input_format": "第一行 `n`；第二行 `n` 个整数。",
        "output_format": "`n` 行，每行一个字母。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 0 ≤ score ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 分支结构",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        int s;\n        scanf(\"%d\", &s);\n        char g;\n        if (s >= 90)      g = 'A';\n        else if (s >= 80) g = 'B';\n        else if (s >= 70) g = 'C';\n        else if (s >= 60) g = 'D';\n        else              g = 'E';\n        printf(\"%c\\n\", g);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\nusing namespace std;\nint main() {\n    int n;\n    cin >> n;\n    const char *tbl = \"EEEEEEDCBAA\";     // 下标 = 分数/10，一次查表\n    while (n--) {\n        int s;\n        cin >> s;\n        int idx = s / 10;\n        if (idx > 10) idx = 10;\n        cout << tbl[idx] << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n95 85 75 65 55\n",
                "expected_stdout": "A\nB\nC\nD\nE\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n90\n",
                "expected_stdout": "A\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n100 60 59\n",
                "expected_stdout": "A\nD\nE\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n0 1\n",
                "expected_stdout": "E\nE\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n89 79 69 69\n",
                "expected_stdout": "B\nC\nD\nD\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n100\n",
                "expected_stdout": "A\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【分支】三个数升序输出",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "C++基础",
            "if",
            "排序三数"
        ],
        "statement_md": "读入 `n` 组三个整数，把它们按**从小到大**输出，空格分隔。\n\n**关键点**\n\n- 最省事的写法是三者两两比较、必要时交换\n- 别用 `sort` 的话要保证三次比较覆盖全部分支\n- 相等的情况顺序无所谓，但输出个数不能少",
        "input_format": "第一行 `n`；接下来 `n` 行，每行三个整数。",
        "output_format": "`n` 行，每行三个整数，升序。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- |a|, |b|, |c| ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 分支结构",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        long long a, b, c;\n        scanf(\"%lld %lld %lld\", &a, &b, &c);\n        if (a > b) { long long t = a; a = b; b = t; }   // 两两交换三次\n        if (a > c) { long long t = a; a = c; c = t; }\n        if (b > c) { long long t = b; b = c; c = t; }\n        printf(\"%lld %lld %lld\\n\", a, b, c);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <algorithm>\nusing namespace std;\nint main() {\n    int n;\n    cin >> n;\n    while (n--) {\n        long long v[3];\n        cin >> v[0] >> v[1] >> v[2];\n        sort(v, v + 3);                  // 直接排序\n        cout << v[0] << \" \" << v[1] << \" \" << v[2] << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\n3 1 2\n2 3 1\n1 2 3\n",
                "expected_stdout": "1 2 3\n1 2 3\n1 2 3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n5 5 1\n",
                "expected_stdout": "1 5 5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n-1 0 -2\n0 0 0\n",
                "expected_stdout": "-2 -1 0\n0 0 0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n100 -100 0\n9 8 7\n1 1 2\n",
                "expected_stdout": "-100 0 100\n7 8 9\n1 1 2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n2147483647 -2147483648 0\n",
                "expected_stdout": "-2147483648 0 2147483647\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n2 1 1\n1 2 1\n1 1 2\n2 2 1\n",
                "expected_stdout": "1 1 2\n1 1 2\n1 1 2\n1 2 2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【分支】一元二次方程的根",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "C++基础",
            "if-else",
            "浮点",
            "数学库"
        ],
        "statement_md": "读入 `n` 组系数 `a b c`，解方程 `ax² + bx + c = 0`，按下面规则输出：\n\n```\n`a == 0`        →  输出 \"not quadratic\"\n`Δ > 0`         →  输出两根（大的在前，两位小数，空格分隔）\n`Δ == 0`        →  输出 \"one root x\"（两位小数）\n`Δ < 0`         →  输出 \"no real root\"\n```\n\n其中 `Δ = b² - 4ac`。\n\n**关键点**\n\n- 先判 `a == 0`，否则除以 0\n- `Δ` 可能是完全平方数，本题数据保证根是**整数或 .5**，用 `%.2f` 不会踩精度\n- 两根顺序：`(-b + √Δ) / 2a` 不一定更大，当 `a < 0` 时要比较",
        "input_format": "第一行 `n`；接下来 `n` 行，每行三个整数 `a b c`。",
        "output_format": "每个方程一行，格式见题面。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- |a|, |b|, |c| ≤ 100\n- 保证 Δ 是完全平方数或负数",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 分支结构",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <cmath>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        int a, b, c;\n        scanf(\"%d %d %d\", &a, &b, &c);\n        if (a == 0) { printf(\"not quadratic\\n\"); continue; }\n        int d = b * b - 4 * a * c;\n        if (d < 0) { printf(\"no real root\\n\"); continue; }\n        if (d == 0) { printf(\"one root %.2f\\n\", -b / (2.0 * a)); continue; }\n        double s = sqrt((double)d);\n        double x1 = (-b + s) / (2.0 * a);\n        double x2 = (-b - s) / (2.0 * a);\n        if (x1 < x2) { double t = x1; x1 = x2; x2 = t; }   // 大的在前\n        printf(\"%.2f %.2f\\n\", x1, x2);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <iomanip>\n#include <cmath>\nusing namespace std;\nint main() {\n    int n;\n    cin >> n;\n    cout << fixed << setprecision(2);\n    while (n--) {\n        int a, b, c;\n        cin >> a >> b >> c;\n        if (a == 0) { cout << \"not quadratic\\n\"; continue; }\n        long long d = 1LL * b * b - 4LL * a * c;\n        if (d < 0) { cout << \"no real root\\n\"; continue; }\n        double r = sqrt((double)(d < 0 ? 0 : d));\n        double den = 2.0 * a;\n        double x1 = (-b + r) / den, x2 = (-b - r) / den;\n        if (d == 0) cout << \"one root \" << x2 << \"\\n\";\n        else if (x1 > x2) cout << x1 << \" \" << x2 << \"\\n\";\n        else cout << x2 << \" \" << x1 << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4\n1 -3 2\n1 2 1\n1 1 1\n0 2 3\n",
                "expected_stdout": "2.00 1.00\none root -1.00\nno real root\nnot quadratic\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n2 -5 2\n",
                "expected_stdout": "2.00 0.50\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n1 -5 6\n-1 3 -2\n",
                "expected_stdout": "3.00 2.00\n2.00 1.00\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n1 0 -4\n1 0 0\n0 0 1\n",
                "expected_stdout": "2.00 -2.00\none root 0.00\nnot quadratic\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n1 -2 1\n2 -4 2\n",
                "expected_stdout": "one root 1.00\none root 1.00\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n-1 5 -6\n",
                "expected_stdout": "3.00 2.00\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【分支】三角形类型判定",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "if-else",
            "三角形"
        ],
        "statement_md": "读入 `n` 组三个正整数表示的三条边，按下面顺序输出类型：\n\n```\n任两边之和 <= 第三边   →  not a triangle\n三边相等               →  equilateral\n只有两边相等           →  isosceles\n有 a² + b² == c²       →  right\n其余                   →  scalene\n```\n\n**关键点**\n\n- 先判能否成三角形，后面才有意义\n- 等腰的判断要在等边之后，否则等边永远进不到 `equilateral`\n- 直角判断用平方和，别用开方后比浮点",
        "input_format": "第一行 `n`；接下来 `n` 行，每行三个正整数。",
        "output_format": "每个三角形一行。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 1 ≤ a, b, c ≤ 1000",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 分支结构",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        long long v[3];\n        scanf(\"%lld %lld %lld\", &v[0], &v[1], &v[2]);\n        std::sort(v, v + 3);\n        if (v[0] + v[1] <= v[2]) { printf(\"not a triangle\\n\"); continue; }\n        if (v[0] == v[2])        { printf(\"equilateral\\n\");    continue; }\n        if (v[0] == v[1] || v[1] == v[2]) { printf(\"isosceles\\n\"); continue; }\n        if (v[0] * v[0] + v[1] * v[1] == v[2] * v[2]) { printf(\"right\\n\"); continue; }\n        printf(\"scalene\\n\");\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <algorithm>\nusing namespace std;\nint main() {\n    int n;\n    cin >> n;\n    while (n--) {\n        long long a, b, c;\n        cin >> a >> b >> c;\n        if (a > b) swap(a, b);\n        if (b > c) swap(b, c);\n        if (a > b) swap(a, b);\n        bool ok = a + b > c;\n        bool eq3 = (a == b && b == c);\n        bool eq2 = (a == b || b == c);\n        bool rt = (a * a + b * b == c * c);\n        if (!ok)       cout << \"not a triangle\\n\";\n        else if (eq3)  cout << \"equilateral\\n\";\n        else if (eq2)  cout << \"isosceles\\n\";\n        else if (rt)   cout << \"right\\n\";\n        else           cout << \"scalene\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n3 4 5\n2 2 2\n2 2 3\n3 4 6\n1 2 3\n",
                "expected_stdout": "right\nequilateral\nisosceles\nscalene\nnot a triangle\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n5 5 8\n",
                "expected_stdout": "isosceles\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n6 8 10\n7 7 7\n",
                "expected_stdout": "right\nequilateral\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n1 1 2\n2 2 1\n8 15 17\n",
                "expected_stdout": "not a triangle\nisosceles\nright\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n1000 1000 1000\n",
                "expected_stdout": "equilateral\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n3 3 5\n4 4 4\n",
                "expected_stdout": "isosceles\nequilateral\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【分支】月份天数（switch 贯穿）",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "switch",
            "贯穿着",
            "闰年"
        ],
        "statement_md": "读入 `n` 组「年 月」，输出该月的天数（闰年 2 月为 29 天）。\n\n要求用 `switch` 的**贯穿（fall-through）**写法：把 4、6、9、11 月归到 30 天，2 月单独判闰年，其余 31 天。\n\n**关键点**\n\n- `case 4: case 6: case 9: case 11: d = 30; break;` 是贯穿的标准用法\n- 漏写 `break` 会一路贯到下一个分支，这是最常见的 switch 错误\n- 闰年判断复用 `y%4==0 && y%100!=0 || y%400==0`",
        "input_format": "第一行 `n`；接下来 `n` 行，每行两个整数 `year month`。",
        "output_format": "`n` 行，每行一个整数。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 1 ≤ year ≤ 9999，1 ≤ month ≤ 12",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 分支结构",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        int y, m;\n        scanf(\"%d %d\", &y, &m);\n        int d;\n        switch (m) {\n            case 4: case 6: case 9: case 11: d = 30; break;   // 贯穿\n            case 2:\n                d = ((y % 4 == 0 && y % 100 != 0) || y % 400 == 0) ? 29 : 28;\n                break;\n            default: d = 31;\n        }\n        printf(\"%d\\n\", d);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    static const int TBL[13] = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};\n    while (n--) {\n        int y, m;\n        scanf(\"%d %d\", &y, &m);\n        int d = TBL[m];\n        bool leap = (y % 4 == 0 && y % 100 != 0) || (y % 400 == 0);\n        if (m == 2 && leap) d = 29;\n        printf(\"%d\\n\", d);\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4\n2024 2\n2023 2\n2024 4\n2024 12\n",
                "expected_stdout": "29\n28\n30\n31\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n2000 2\n",
                "expected_stdout": "29\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n1900 2\n2024 1\n2024 7\n",
                "expected_stdout": "28\n31\n31\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n2024 9\n2024 11\n",
                "expected_stdout": "30\n30\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n2024 3\n",
                "expected_stdout": "31\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n2100 2\n2400 2\n",
                "expected_stdout": "28\n29\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【分支】简单计算器",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "switch",
            "计算器",
            "除零"
        ],
        "statement_md": "读入 `n` 行算式，每行形如 `a op b`，其中 `op` 是 `+ - * / %` 之一。\n\n输出运算结果（都是整数运算）。若遇到除数为 0，输出 `error`。\n\n**关键点**\n\n- `op` 是字符，用 `scanf(\"%d %c %d\")` 读；`%c` 前加空格跳空白\n- `switch (op)` 比一串 `if` 清楚\n- 除法和取模都要先判 `b == 0`，否则程序直接崩（不是输出 error）",
        "input_format": "第一行 `n`；接下来 `n` 行，每行 `a op b`。",
        "output_format": "`n` 行结果。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- |a|, |b| ≤ 10⁶\n- `op` ∈ {+,-,*,/,%}",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 分支结构",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        long long a, b;\n        char op;\n        scanf(\"%lld %c %lld\", &a, &op, &b);\n        switch (op) {\n            case '+': printf(\"%lld\\n\", a + b); break;\n            case '-': printf(\"%lld\\n\", a - b); break;\n            case '*': printf(\"%lld\\n\", a * b); break;\n            case '/':\n                if (b == 0) printf(\"error\\n\");\n                else printf(\"%lld\\n\", a / b);\n                break;\n            case '%':\n                if (b == 0) printf(\"error\\n\");\n                else printf(\"%lld\\n\", a % b);\n                break;\n            default: printf(\"error\\n\");\n        }\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\nusing namespace std;\nint main() {\n    int n;\n    cin >> n;\n    while (n--) {\n        long long a, b;\n        char op;\n        cin >> a >> op >> b;\n        if ((op == '/' || op == '%') && b == 0) { cout << \"error\\n\"; continue; }\n        long long r = 0;\n        if (op == '+') r = a + b;\n        else if (op == '-') r = a - b;\n        else if (op == '*') r = a * b;\n        else if (op == '/') r = a / b;\n        else r = a % b;\n        cout << r << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4\n7 + 2\n7 - 2\n7 * 2\n7 / 2\n",
                "expected_stdout": "9\n5\n14\n3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2\n5 % 3\n0 / 5\n",
                "expected_stdout": "2\n0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n1 / 0\n9 % 0\n-7 / 2\n",
                "expected_stdout": "error\nerror\n-3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n-7 % 3\n100 * 100\n",
                "expected_stdout": "-1\n10000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n0 - 0\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n10 + 10\n10 - 10\n10 * 10\n",
                "expected_stdout": "20\n0\n100\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【分支】出租车计费",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "if",
            "分段计费"
        ],
        "statement_md": "出租车计费规则（金额单位：元，结果取整）：\n\n```\n起步价 10 元，含 3 公里\n超过 3 公里的部分，每公里 2 元\n等候时间每分钟加 1 元\n```\n\n读入 `n` 行「公里数 等候分钟数」，输出总费用。公里数可能带小数，向上取整到整公里计费。\n\n**关键点**\n\n- 先算超出里程 `max(0, km - 3)`，不足 1 公里按 1 公里算（向上取整）\n- 向上取整整数的写法：`(x + 0.999999)` 不可靠，用 `ceil` 或整数判断\n- 本题公里数是**整数**，不用处理小数，简化成 `km > 3 ? km - 3 : 0`",
        "input_format": "第一行 `n`；接下来 `n` 行，每行两个整数 `km minutes`。",
        "output_format": "`n` 行，每行一个整数。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 0 ≤ km ≤ 1000，0 ≤ minutes ≤ 600",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 分支结构",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        int km, mins;\n        scanf(\"%d %d\", &km, &mins);\n        int extra = std::max(0, km - 3);      // 超出里程\n        int fee = 10 + extra * 2 + mins;      // 起步价 + 里程费 + 等候费\n        printf(\"%d\\n\", fee);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\nusing namespace std;\nint main() {\n    int n;\n    cin >> n;\n    while (n--) {\n        int km, mins;\n        cin >> km >> mins;\n        int fee = 10 + mins;\n        if (km > 3) fee += (km - 3) * 2;\n        cout << fee << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4\n2 0\n3 0\n10 0\n10 5\n",
                "expected_stdout": "10\n10\n24\n29\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n0 0\n",
                "expected_stdout": "10\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n4 0\n4 30\n100 60\n",
                "expected_stdout": "12\n42\n264\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n1 60\n2 60\n",
                "expected_stdout": "70\n70\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n1000 600\n",
                "expected_stdout": "2604\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n3 10\n5 10\n",
                "expected_stdout": "20\n24\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【分支】阶梯电费",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "if-else",
            "分段累加"
        ],
        "statement_md": "居民阶梯电价（按月用电量 `k` 度）：\n\n```\n0  ~ 100 度      0.50 元/度\n101 ~ 200 度     超出 100 的部分 0.60 元/度\n200 度以上       超出 200 的部分 0.80 元/度\n```\n\n读入 `n` 个整数用电量，输出电费，**保留两位小数**。\n\n**关键点**\n\n- 分段累加：先付前 100 度的 50 元，再付中间段的钱\n- 用「分」做整数运算更稳：50 / 60 / 80 分每度，最后除以 100 输出\n- 别写成「超过 200 就全部按 0.8 算」—— 那是最常见的错解",
        "input_format": "第一行 `n`；第二行 `n` 个非负整数。",
        "output_format": "`n` 行，每行一个两位小数。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 0 ≤ k ≤ 10000",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 分支结构",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        int k;\n        scanf(\"%d\", &k);\n        long long fen = 0;                        // 以「分」为单位\n        fen += std::min(k, 100) * 50LL;\n        if (k > 100)  fen += std::min(k - 100, 100) * 60LL;\n        if (k > 200)  fen += (k - 200) * 80LL;\n        printf(\"%.2f\\n\", fen / 100.0);\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <iomanip>\nusing namespace std;\nint main() {\n    int n;\n    cin >> n;\n    cout << fixed << setprecision(2);\n    while (n--) {\n        int k;\n        cin >> k;\n        double money = 0;\n        int t = k;\n        int a = t < 100 ? t : 100;       t -= a;\n        int b = t < 100 ? t : 100;       t -= b;\n        int c = t;\n        money = a * 0.5 + b * 0.6 + c * 0.8;\n        cout << money << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4\n0 100 150 250\n",
                "expected_stdout": "0.00\n50.00\n80.00\n150.00\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n200\n",
                "expected_stdout": "110.00\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n101 199 201\n",
                "expected_stdout": "50.60\n109.40\n110.80\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n50 300\n",
                "expected_stdout": "25.00\n190.00\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n10000\n",
                "expected_stdout": "7950.00\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n1000 1999\n",
                "expected_stdout": "750.00\n1549.20\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【分支】水仙花数判定",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "C++基础",
            "数位分解",
            "if"
        ],
        "statement_md": "读入 `n` 个三位正整数，判断它是否为**水仙花数**：各位数字的立方和等于它本身。\n\n是输出 `YES`，否输出 `NO`。\n\n**关键点**\n\n- 取各位：`a = x/100`、`b = x/10%10`、`c = x%10`\n- `x/1000` 非零说明不是三位数，但本题数据保证是三位\n- 立方和用 `int` 就够（最大 9³×3 = 2187）",
        "input_format": "第一行 `n`；第二行 `n` 个三位正整数。",
        "output_format": "`n` 行，每行 `YES` 或 `NO`。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 100 ≤ x ≤ 999",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 分支结构",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        int x;\n        scanf(\"%d\", &x);\n        int a = x / 100, b = x / 10 % 10, c = x % 10;\n        bool ok = (a * a * a + b * b * b + c * c * c == x);\n        printf(\"%s\\n\", ok ? \"YES\" : \"NO\");\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\nusing namespace std;\nint main() {\n    int n;\n    cin >> n;\n    while (n--) {\n        int x;\n        cin >> x;\n        int s = 0, t = x;\n        while (t) { int d = t % 10; s += d * d * d; t /= 10; }\n        cout << (s == x ? \"YES\" : \"NO\") << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4\n153 370 371 100\n",
                "expected_stdout": "YES\nYES\nYES\nNO\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n407\n",
                "expected_stdout": "YES\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n999 123 1634\n",
                "expected_stdout": "NO\nNO\nNO\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n100 101\n",
                "expected_stdout": "NO\nNO\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n370 371 372\n",
                "expected_stdout": "YES\nYES\nNO\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n999\n",
                "expected_stdout": "NO\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【分支】三位回文数判定",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "C++基础",
            "回文",
            "if"
        ],
        "statement_md": "读入 `n` 个三位正整数，判断是否为回文数（正读反读相同），是输出 `YES`，否输出 `NO`。\n\n**关键点**\n\n- 三位回文的条件就是「百位 == 个位」，十位随便\n- 别把数字反转再比较，多此一举（虽然也对）\n- 输出大写",
        "input_format": "第一行 `n`；第二行 `n` 个三位正整数。",
        "output_format": "`n` 行，每行 `YES` 或 `NO`。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 100 ≤ x ≤ 999",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 分支结构",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        int x;\n        scanf(\"%d\", &x);\n        printf(\"%s\\n\", (x / 100 == x % 10) ? \"YES\" : \"NO\");\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\nusing namespace std;\nint main() {\n    int n;\n    cin >> n;\n    while (n--) {\n        int x;\n        cin >> x;\n        int rev = 0, t = x;\n        while (t) { rev = rev * 10 + t % 10; t /= 10; }   // 整体反转\n        cout << (rev == x ? \"YES\" : \"NO\") << \"\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4\n121 123 111 100\n",
                "expected_stdout": "YES\nNO\nYES\nNO\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n999\n",
                "expected_stdout": "YES\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n101 202 303\n",
                "expected_stdout": "YES\nYES\nYES\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n120 122\n",
                "expected_stdout": "NO\nNO\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n191 292 393\n",
                "expected_stdout": "YES\nYES\nYES\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1\n505\n",
                "expected_stdout": "YES\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【分支】字符类型判断",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "C++基础",
            "字符分类",
            "cctype"
        ],
        "statement_md": "读入 `n` 个可见字符，逐个判断类型并输出：\n\n```\n0~9  →  digit\nA~Z  →  upper\n a~z  →  lower\n其余  →  other\n```\n\n**关键点**\n\n- 用字符比较 `c >= '0' && c <= '9'`，别写 ASCII 码数字\n- `isupper` / `isdigit` 也行，但要 `#include <cctype>`\n- 顺序：先判数字，再判大小写",
        "input_format": "第一行 `n`；第二行 `n` 个字符，空格分隔。",
        "output_format": "`n` 行，每行一个单词。",
        "constraints_md": "- 1 ≤ n ≤ 6\n- 字符为可见 ASCII",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 分支结构",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1) return 0;\n    while (n--) {\n        char c;\n        scanf(\" %c\", &c);\n        if (c >= '0' && c <= '9')      printf(\"digit\\n\");\n        else if (c >= 'A' && c <= 'Z') printf(\"upper\\n\");\n        else if (c >= 'a' && c <= 'z') printf(\"lower\\n\");\n        else                           printf(\"other\\n\");\n    }\n    return 0;\n}\n",
        "alt_solution": "#include <iostream>\n#include <cctype>\nusing namespace std;\nint main() {\n    int n;\n    cin >> n;\n    while (n--) {\n        char c;\n        cin >> c;\n        if (isdigit((unsigned char)c))      cout << \"digit\\n\";\n        else if (isupper((unsigned char)c)) cout << \"upper\\n\";\n        else if (islower((unsigned char)c)) cout << \"lower\\n\";\n        else                                cout << \"other\\n\";\n    }\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "4\n5 A a +\n",
                "expected_stdout": "digit\nupper\nlower\nother\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\nZ\n",
                "expected_stdout": "upper\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n0 9 ~ _ !\n",
                "expected_stdout": "digit\ndigit\nother\nother\nother\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\nz Z\n",
                "expected_stdout": "lower\nupper\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n@ [ `\n",
                "expected_stdout": "other\nother\nother\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n1 b C 2\n",
                "expected_stdout": "digit\nlower\nupper\ndigit\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    }
]
