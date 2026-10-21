# -*- coding: utf-8 -*-
"""第 5 册：指针与引用 / 字符数组与字符串 —— 自动生成，**不要手改本文件**。

生成器：tools/gen_cpp_basic5.py
题数：40 题 / 240 测试点 / 总分 482

重生成：python tools/gen_cpp_basic5.py
"""

CPP_BASIC5_PROBLEMS: list[dict] = [
    {
        "title": "【指针】用指针参数交换数组元素",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "指针",
            "交换",
            "数组"
        ],
        "statement_md": "写函数 `void swapAt(int *p, int *q)` 交换两个指针指向的元素。读入 `n i j`，第二行 `n` 个整数，交换下标 `i` 与 `j` 的元素后输出整个数组。\n\n**关键点**\n\n- 下标从 0 开始；`swapAt(a + i, a + j)` 传的是地址不是值\n- `void swapAt(int x, int y)` 交换的是副本，原数组不变\n- 输出一行，空格分隔",
        "input_format": "第一行 `n i j`；第二行 `n` 个整数。",
        "output_format": "一行：交换后的数组。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 0 ≤ i, j < n\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 指针与引用",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nvoid swapAt(int *p, int *q) {      // 形参是指针，*p 就是原元素\n    int t = *p; *p = *q; *q = t;\n}\nint main() {\n    int n, i, j;\n    if (scanf(\"%d %d %d\", &n, &i, &j) != 3) return 0;\n    int a[1005];\n    for (int k = 0; k < n; k++) scanf(\"%d\", &a[k]);\n    swapAt(a + i, a + j);          // 传地址\n    for (int k = 0; k < n; k++) printf(\"%d%c\", a[k], k + 1 == n ? '\\n' : ' ');\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n, i, j;\n    if (scanf(\"%d %d %d\", &n, &i, &j) != 3) return 0;\n    int *a = new int[n];           // 动态数组\n    for (int k = 0; k < n; k++) scanf(\"%d\", &a[k]);\n    std::swap(*(a + i), *(a + j)); // 指针解引用直接交换\n    for (int k = 0; k < n; k++) printf(\"%d%c\", a[k], k + 1 == n ? '\\n' : ' ');\n    delete[] a;\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 0 4\n1 2 3 4 5\n",
                "expected_stdout": "5 2 3 4 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 1 1\n7 8 9\n",
                "expected_stdout": "7 8 9\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "2 0 1\n-1 -2\n",
                "expected_stdout": "-2 -1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10 2 7\n7 21 49 9 7 15 25 -26 -27 15\n",
                "expected_stdout": "7 21 -26 9 7 15 25 49 -27 15\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6 5 0\n21 -32 68 35 70 -11\n",
                "expected_stdout": "-11 -32 68 35 70 21\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "1 0 0\n42\n",
                "expected_stdout": "42\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【指针】指针遍历数组求最值及下标",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "指针",
            "遍历",
            "最值"
        ],
        "statement_md": "用指针遍历数组，求最大值和它**第一次出现**的下标（从 1 开始）。读入 `n` 和 `n` 个整数，输出 `max pos`。\n\n**关键点**\n\n- 指针遍历的写法是 `for (int *p = a; p < a + n; ++p)`\n- `a + n` 是「最后一个元素再往后一格」的地址，可以比较但不能解引用\n- `pos` 从 1 开始，别写成指针差值",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：`max pos`。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 指针与引用",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int mx = a[0], pos = 1, idx = 1;\n    for (int *p = a + 1; p < a + n; ++p) {   // 指针遍历\n        idx++;\n        if (*p > mx) { mx = *p; pos = idx; }\n    }\n    printf(\"%d %d\\n\", mx, pos);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int *mx = std::max_element(a, a + n);     // 取第一个最大\n    printf(\"%d %d\\n\", *mx, (int)(mx - a) + 1);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n-29 3 38 3 31\n",
                "expected_stdout": "38 3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n-33\n",
                "expected_stdout": "-33 1\n",
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
                "stdin": "20\n49 -13 -40 -48 25 -11 4 -2 17 -5 -34 42 -26 -16 6 -49 -22 29 8 -47\n",
                "expected_stdout": "49 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "50\n-271 -608 -141 -404 -814 -777 -829 -802 -827 -314 -302 -907 -278 -225 -846 -175 -277 -710 -259 -56 -216 -987 -549 -522 -114 -262 -350 -882 -972 -471 -828 -19 -497 -244 -135 -546 -302 -689 -489 -25 -913 -297 -222 -740 -137 -374 -839 -303 -666 -17\n",
                "expected_stdout": "-17 50\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8\n0 0 0 0 0 0 0 0\n",
                "expected_stdout": "0 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【指针】用指针求数组元素之和",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "指针",
            "求和"
        ],
        "statement_md": "用指针遍历求所有元素之和。读入 `n` 和 `n` 个整数（|x| ≤ 10⁶），输出总和。\n\n**关键点**\n\n- `*(p + i)` 和 `a[i]` 完全等价\n- 10⁵ 个 10⁶ 累加到 10¹¹，必须用 `long long`\n- 输出一个整数",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：总和。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 指针与引用",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    long long s = 0;\n    for (int *p = a; p < a + n; ++p) s += *p;\n    printf(\"%lld\\n\", s);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    long long s = 0;\n    for (int i = 0; i < n; i++) s += *(a + i);   // 指针偏移写法\n    printf(\"%lld\\n\", s);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n-49 10 -36 47 0\n",
                "expected_stdout": "-28\n",
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
                "stdin": "20\n23 -29 30 -21 -15 11 33 18 17 -27 33 28 14 -9 37 17 11 6 -14 36\n",
                "expected_stdout": "199\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "200\n109257 -251166 228400 -941967 768583 -519098 884594 -937277 850079 -184092 -235178 989862 -864590 -110652 -357887 -284591 -801751 224838 73066 724980 -675312 -797639 -424899 -272132 280490 -996922 628181 -675044 578445 98583 -818800 680296 -871585 -225726 -464772 551510 157544 478388 759182 -874735 678697 -188950 958215 -650301 234786 831939 335234 -349869 -387722 -199720 -341805 -553747 -567980 -49747 122560 -624184 273507 -724999 202071 506448 -177955 139734 -111020 -504775 -478973 434572 709573 -765250 218536 407746 570129 -842953 702115 -67839 -411040 -129843 -754572 218881 -406730 915696 902557 -585203 660215 -633578 -149675 637436 628598 900656 -282841 -53889 814880 903031 -810701 91258 553832 736250 -5028 -119045 815016 -31313 -239466 -725525 -68872 -422751 -706088 -509574 -671056 -378877 -347612 -856371 919085 -372058 84361 -781219 226059 100156 -376684 -147712 957341 -522983 -144752 978072 775536 -351051 598100 114612 925383 876286 518043 590342 -257315 560361 278023 733792 826203 -45578 -863476 -849612 539518 -897189 -295138 -141073 -327153 -636378 614027 -609813 555549 -128081 -282983 10731 -237857 388569 -415695 -995628 958741 498165 289165 335640 -454882 74125 116301 650894 -878878 -662152 -434663 -752400 51606 -448808 -821852 799699 396005 148271 -37766 600361 -698884 -471766 352905 455871 876280 626710 -677037 -18185 955867 -623006 363177 -228247 547191 707020 -209704 933678 -690064 -767395 -25233 -316875 245313 -638489 664820 -729133 -442159 557315\n",
                "expected_stdout": "-634545\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n-1 -2 -3\n",
                "expected_stdout": "-6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "333\n20 -8 46 -34 45 -7 -31 -14 5 -18 22 -43 45 17 46 -15 33 -4 41 24 46 -38 -4 -49 15 -49 -38 42 13 -3 43 -47 -7 36 13 -44 -48 -20 -9 -40 -30 -7 -29 22 -41 11 -4 -40 -13 -30 23 -41 36 -34 19 43 6 13 -9 0 29 -1 -46 -17 49 26 48 8 14 21 46 -45 -36 35 -7 20 10 -38 -41 -2 1 -25 6 -1 37 -50 -17 24 42 -22 -19 50 24 -28 -48 35 -40 -38 -36 39 -28 -47 -34 39 12 28 28 -49 35 9 14 46 -29 46 18 -13 19 6 44 0 -44 39 -1 16 44 29 -15 19 14 -29 -7 27 11 -13 13 37 -38 -6 49 19 -40 26 22 -6 43 8 37 -2 -50 7 28 33 8 -37 -21 39 -3 36 18 -30 8 -37 -19 41 -11 -35 -19 4 -43 2 -6 9 21 39 -47 -28 27 38 -37 13 -9 49 15 -38 41 16 -19 50 43 36 19 6 47 -19 -32 -24 1 -24 -17 43 -21 44 19 49 14 0 7 47 -26 -32 6 -38 6 28 18 -24 25 39 -50 26 -5 44 3 23 -17 -22 44 -25 -3 -4 -45 19 -29 -44 8 -9 -14 -35 -40 -1 22 48 43 10 29 -44 -43 -2 4 -48 -6 -17 -49 -33 45 -33 39 9 12 -35 -11 45 -8 8 1 -36 -47 24 21 -39 -31 -6 15 -14 21 47 26 -45 -23 -8 7 40 30 -6 -1 46 4 -41 -43 -35 16 49 22 -4 -42 -45 40 -25 4 -21 -39 -2 -12 34 -41 46 -5 22 -10 43 -31 -17 12 -15 -30 -26 7 6 -3 -41 40 10 48 -28 37 13 -32 -4 3 14 -31 32 4\n",
                "expected_stdout": "287\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【指针】指针偏移访问元素",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "指针",
            "偏移",
            "数组名"
        ],
        "statement_md": "读入 `n k` 和 `n` 个整数，输出两个数：`*(a + k)` 与 `a[k]`（它们必然相同），再输出 `*(a + k) * 2`。\n\n**关键点**\n\n- `a[k]` 在编译后就是 `*(a + k)`，两者是同一个东西的两种写法\n- 0 ≤ k < n，越界读是未定义行为\n- 输出一行三个整数",
        "input_format": "第一行 `n k`；第二行 `n` 个整数。",
        "output_format": "一行：`*(a+k)`、`a[k]`、`*(a+k)*2`。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 0 ≤ k < n\n- |x| ≤ 10⁴",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 指针与引用",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n, k;\n    if (scanf(\"%d %d\", &n, &k) != 2) return 0;\n    int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    printf(\"%d %d %d\\n\", *(a + k), a[k], *(a + k) * 2);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n, k;\n    if (scanf(\"%d %d\", &n, &k) != 2) return 0;\n    int *a = new int[n];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int *p = a + k;               // 先算好指针，再重复解引用\n    printf(\"%d %d %d\\n\", *p, a[k], *p * 2);\n    delete[] a;\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 0\n1 2 3 4 5\n",
                "expected_stdout": "1 1 2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5 4\n1 2 3 4 5\n",
                "expected_stdout": "5 5 10\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 0\n-7\n",
                "expected_stdout": "-7 -7 -14\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10 3\n-2 -8 -21 -29 -1 23 38 -14 20 -15\n",
                "expected_stdout": "-29 -29 -58\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6 5\n63 -72 -94 89 -30 -38\n",
                "expected_stdout": "-38 -38 -76\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3 2\n0 0 9\n",
                "expected_stdout": "9 9 18\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【指针】二级指针让指针指向最大元素",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "指针",
            "二级指针"
        ],
        "statement_md": "用二级指针 `int **pp` 修改一级指针的指向：让它指向数组中的最大元素，再输出 `**pp`。读入 `n` 和 `n` 个整数，输出最大值。\n\n**关键点**\n\n- `int **pp = &p;` 之后 `*pp` 就是 `p`，给 `*pp` 赋值等于改 `p` 的指向\n- 实参必须是「指针的地址」，直接传 `p` 只能改副本\n- 输出一个整数",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：最大值。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 指针与引用",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nvoid pointToMax(int a[], int n, int **pp) {\n    *pp = &a[0];                       // 通过二级指针改一级指针\n    for (int i = 1; i < n; i++)\n        if (a[i] > **pp) *pp = &a[i];\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int *p = a;\n    pointToMax(a, n, &p);              // 传 p 的地址\n    printf(\"%d\\n\", *p);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int *p = a, **pp = &p;             // 局部二级指针\n    for (int i = 1; i < n; i++) if (a[i] > **pp) *pp = &a[i];\n    printf(\"%d\\n\", **pp);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n-19 14 20 -30 -19\n",
                "expected_stdout": "20\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n-16\n",
                "expected_stdout": "-16\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n5 5 1\n",
                "expected_stdout": "5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "20\n28 -23 8 14 41 11 41 16 -4 43 8 43 -47 -46 -29 -6 45 -34 -17 45\n",
                "expected_stdout": "45\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "30\n-65 -860 -551 -431 -695 -506 -89 -19 -501 -611 -776 -543 -663 -409 -252 -609 -103 -67 -101 -787 -259 -796 -943 -493 -182 -438 -537 -388 -907 -445\n",
                "expected_stdout": "-19\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "9\n7 7 7 7 7 7 7 7 7\n",
                "expected_stdout": "7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【指针】new 与 delete 动态数组求和",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "指针",
            "new",
            "delete"
        ],
        "statement_md": "用 `new int[n]` 申请动态数组存放 `n` 个整数，求和后 `delete[]` 释放。读入 `n` 和 `n` 个整数，输出总和。\n\n**关键点**\n\n- `new[]` 必须配 `delete[]`，写 `delete p` 是未定义行为\n- 数组长度可以运行时才定 —— 这是动态数组相对 `int a[10]` 的唯一优势\n- 释放后指针变成悬空指针，最好立刻置 `nullptr`",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：总和。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 指针与引用",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    int *a = new int[n];               // 运行时才知道长度\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    long long s = 0;\n    for (int i = 0; i < n; i++) s += a[i];\n    printf(\"%lld\\n\", s);\n    delete[] a;                        // 必须 delete[]\n    a = nullptr;\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <vector>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    std::vector<int> a(n);             // 现代写法：容器自己管内存\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    long long s = 0;\n    for (int x : a) s += x;\n    printf(\"%lld\\n\", s);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n13 -27 21 -23 -9\n",
                "expected_stdout": "-25\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n23\n",
                "expected_stdout": "23\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "20\n6 6 -13 -18 11 34 -39 -1 45 -40 -41 34 -25 -13 -41 30 -11 45 28 -43\n",
                "expected_stdout": "-46\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "200\n-1424 -738169 321665 285531 -152833 124403 929430 440449 -964660 -573207 -436604 476635 914049 686099 326555 684234 603332 -577703 465190 718442 631986 369375 -690815 -832622 806342 -126046 -77177 -584219 512651 -948389 -824540 -154983 424940 912212 -988795 945416 -866143 -633914 -778934 230391 -904119 992369 234973 -446340 -540200 130847 -587412 -813728 709079 -938043 614135 -38711 -167404 869901 -551719 -379527 556909 -712091 152760 -104761 -247500 67901 -356135 567346 -236215 443596 20720 88785 -624687 -894982 -996559 -515146 -23913 -662483 -552275 -539354 -882600 345143 -411204 -544334 410916 -485453 739460 669083 -938059 514727 691079 969197 -364453 834730 797416 -766482 859978 -671953 -373705 -532805 346146 824639 193747 419043 -502450 906941 831128 375941 -490469 989670 -688516 292498 -459203 -110429 931894 -66596 -369664 486690 -218494 -642443 -425774 -674256 733959 -623615 -374916 -906634 -733372 -888681 -767217 -748107 927749 69814 -882230 754643 -645144 849173 -301443 178093 -473918 747243 -112965 648780 -7926 -907051 412529 33168 -333856 448582 80149 481171 -921650 -887547 566022 442417 122768 -343869 409384 806203 766895 -701317 725966 843773 590230 528568 601206 -770679 51125 -311766 -355402 307203 59064 -731326 827664 -180475 707809 -188358 -216351 -713899 -317401 -124207 -982018 424161 -980784 949937 -348754 382639 335255 287501 611519 -640159 -198513 -610177 607799 109865 451478 -517240 -795 -415167 182412 -61921 -826369 -335788 -377235 -463949\n",
                "expected_stdout": "-5881384\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n-1 -2 -3\n",
                "expected_stdout": "-6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100\n3 -14 -14 15 -22 6 8 17 6 20 -7 31 5 -22 -41 21 9 -17 -25 33 10 29 38 -45 -18 -36 -30 17 44 -33 37 -35 -33 38 -6 -3 23 33 -4 29 -21 31 -21 0 7 10 -44 39 -31 47 -48 49 -8 -18 -10 47 -16 -49 -28 44 5 -41 -17 20 -49 -27 -30 23 18 5 5 -34 16 47 3 44 44 -9 -22 -20 -12 21 -5 -26 -3 23 26 40 32 50 -50 -12 35 -42 -16 -14 8 50 -30 -34\n",
                "expected_stdout": "69\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【指针】指针实现冒泡排序",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "指针",
            "冒泡排序"
        ],
        "statement_md": "用指针访问元素实现冒泡排序（升序）。读入 `n` 和 `n` 个整数，输出排序结果。\n\n**关键点**\n\n- 外层 `n-1` 趟，内层比较相邻两个 `*(p+j)` 和 `*(p+j+1)`\n- 加一个「本趟有没有交换」的标记可以提前结束\n- 输出一行，空格分隔",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：升序排列的数组。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 指针与引用",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nvoid bubble(int *a, int n) {\n    for (int i = 0; i < n - 1; i++) {\n        bool moved = false;\n        for (int j = 0; j < n - 1 - i; j++)\n            if (*(a + j) > *(a + j + 1)) {\n                int t = *(a + j); *(a + j) = *(a + j + 1); *(a + j + 1) = t;\n                moved = true;\n            }\n        if (!moved) break;             // 已经有序，提前收工\n    }\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    bubble(a, n);\n    for (int i = 0; i < n; i++) printf(\"%d%c\", a[i], i + 1 == n ? '\\n' : ' ');\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    int *a = new int[n];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    std::sort(a, a + n);               // 指针区间排序\n    for (int i = 0; i < n; i++) printf(\"%d%c\", a[i], i + 1 == n ? '\\n' : ' ');\n    delete[] a;\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n-9 15 29 -49 -17\n",
                "expected_stdout": "-49 -17 -9 15 29\n",
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
                "stdin": "5\n5 4 3 2 1\n",
                "expected_stdout": "1 2 3 4 5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "20\n-15 -35 14 11 22 -27 9 -12 25 -41 12 1 16 14 -25 7 -36 -48 -18 2\n",
                "expected_stdout": "-48 -41 -36 -35 -27 -25 -18 -15 -12 1 2 7 9 11 12 14 14 16 22 25\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "15\n56 31 -71 -19 -70 -21 -54 -45 -11 -70 13 16 34 -29 14\n",
                "expected_stdout": "-71 -70 -70 -54 -45 -29 -21 -19 -11 13 14 16 31 34 56\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n3 3 3 3\n",
                "expected_stdout": "3 3 3 3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【指针】指针倒序输出数组",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "指针",
            "倒序"
        ],
        "statement_md": "用指针从后往前遍历，倒序输出数组。读入 `n` 和 `n` 个整数。\n\n**关键点**\n\n- 从 `a + n - 1` 开始，往 `a` 方向走\n- `--p` 是先减再解引用，注意别走到 `a` 之前\n- 输出一行，空格分隔",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：倒序的数组。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 指针与引用",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    for (int *p = a + n - 1; p >= a; --p)   // 从尾部往头走\n        printf(\"%d%c\", *p, p == a ? '\\n' : ' ');\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    std::reverse(a, a + n);            // 先原地反转再正序输出\n    for (int i = 0; i < n; i++) printf(\"%d%c\", a[i], i + 1 == n ? '\\n' : ' ');\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n14 8 -7 21 18\n",
                "expected_stdout": "18 21 -7 8 14\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n-32\n",
                "expected_stdout": "-32\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "10\n13 8 -39 -34 -2 -46 -44 33 -23 -26\n",
                "expected_stdout": "-26 -23 33 -44 -46 -2 -34 -39 8 13\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "20\n87 -28 98 -91 25 -99 33 69 -19 -50 17 27 41 93 89 -7 55 -62 39 93\n",
                "expected_stdout": "93 39 -62 55 -7 89 93 41 27 17 -50 -19 69 33 -99 25 -91 98 -28 87\n",
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
            },
            {
                "stdin": "33\n-25 39 28 -37 -9 -26 -22 9 49 48 -6 24 -22 37 -2 18 18 -22 49 37 25 26 23 9 27 5 -35 -50 37 21 -41 5 10\n",
                "expected_stdout": "10 5 -41 21 37 -50 -35 5 27 9 23 26 25 37 49 -22 18 18 -2 37 -22 24 -6 48 49 9 -22 -26 -9 -37 28 39 -25\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【指针】引用返回值替换最大值",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "指针",
            "引用",
            "返回值"
        ],
        "statement_md": "写函数 `int &maxRef(int a[], int n)` 返回最大元素的**引用**。读入 `n x` 和 `n` 个整数，把**第一个**最大值改成 `x` 后输出整个数组。\n\n**关键点**\n\n- 返回引用才能当左值用：`maxRef(a, n) = x;` 直接改到原数组\n- 返回局部变量的引用是悬空引用，返回数组元素或静态变量的引用才安全\n- 有多个最大值时只改第一个",
        "input_format": "第一行 `n x`；第二行 `n` 个整数。",
        "output_format": "一行：修改后的数组。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x|, |a[i]| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 指针与引用",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint &maxRef(int a[], int n) {\n    int k = 0;\n    for (int i = 1; i < n; i++) if (a[i] > a[k]) k = i;   // 严格大于，取第一个\n    return a[k];                                          // 返回引用\n}\nint main() {\n    int n, x;\n    if (scanf(\"%d %d\", &n, &x) != 2) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    maxRef(a, n) = x;                 // 当左值用\n    for (int i = 0; i < n; i++) printf(\"%d%c\", a[i], i + 1 == n ? '\\n' : ' ');\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint *maxPtr(int a[], int n) {         // 用指针达到同样效果\n    int *p = a;\n    for (int i = 1; i < n; i++) if (a[i] > *p) p = a + i;\n    return p;\n}\nint main() {\n    int n, x;\n    if (scanf(\"%d %d\", &n, &x) != 2) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    *maxPtr(a, n) = x;\n    for (int i = 0; i < n; i++) printf(\"%d%c\", a[i], i + 1 == n ? '\\n' : ' ');\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 0\n1 2 3 4 5\n",
                "expected_stdout": "1 2 3 4 0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 -1\n7 7 7\n",
                "expected_stdout": "-1 7 7\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 9\n-2\n",
                "expected_stdout": "9\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10 100\n-40 25 -28 37 36 -30 1 8 50 45\n",
                "expected_stdout": "-40 25 -28 37 36 -30 1 8 100 45\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6 0\n-47 -34 -28 -30 -29 -25\n",
                "expected_stdout": "-47 -34 -28 -30 -29 0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4 5\n2 5 5 2\n",
                "expected_stdout": "2 5 5 2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【指针】指针统计小于均值的元素个数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "指针",
            "均值",
            "统计"
        ],
        "statement_md": "读入 `n` 和 `n` 个整数，先算平均值（实数），再统计严格小于平均值的元素个数。输出平均值（保留 2 位小数）和个数，空格分隔。\n\n**关键点**\n\n- 均值要用 `double` 算，不能用整数除法 `s / n`\n- 比较时 `a[i] < avg` 会自动把 `a[i]` 转成 `double`\n- 输出一行：均值与个数",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：`平均值 个数`（均值保留 2 位小数）。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 指针与引用",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    long long s = 0;\n    for (int i = 0; i < n; i++) { scanf(\"%d\", &a[i]); s += a[i]; }\n    double avg = (double)s / n;        // 先转 double 再除\n    int c = 0;\n    for (int *p = a; p < a + n; ++p) if (*p < avg) c++;\n    printf(\"%.2f %d\\n\", avg, c);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    double s = 0;\n    for (int i = 0; i < n; i++) { scanf(\"%d\", &a[i]); s += a[i]; }\n    double avg = s / n;\n    int c = 0;\n    for (int i = 0; i < n; i++) c += (a[i] < avg);\n    printf(\"%.2f %d\\n\", avg, c);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n1 2 3 4 5\n",
                "expected_stdout": "3.00 2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\n1 1 1\n",
                "expected_stdout": "1.00 0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n-7\n",
                "expected_stdout": "-7.00 0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "20\n24 -26 19 -5 9 -44 34 14 -23 27 -22 -14 12 38 50 -23 -8 6 -41 -18\n",
                "expected_stdout": "0.45 10\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "50\n-697 385 261 -267 -653 135 459 353 244 -627 -213 -401 264 -122 159 190 -912 483 85 112 269 528 64 812 801 -621 505 619 -228 -96 -536 44 -738 -827 659 -892 412 -624 247 178 -96 839 26 715 -546 462 86 76 -703 5\n",
                "expected_stdout": "13.56 20\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4\n2 4 6 8\n",
                "expected_stdout": "5.00 2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【指针】指针差求数组元素个数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "指针",
            "指针差"
        ],
        "statement_md": "读入 `n` 和 `n` 个整数，输出两个数：`n` 本身、以及 `&a[n] - a`（指针相减得到的元素个数）。两个数应当相等。\n\n**关键点**\n\n- 同类型的两个指针相减，结果是它们之间相差的**元素个数**，不是字节数\n- `&a[n]` 是「最后一个元素再往后一格」的地址，合法可算但不可解引用\n- 输出一行两个整数",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：`n` 与 `&a[n] - a`。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 指针与引用",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    printf(\"%d %d\\n\", n, (int)(&a[n] - a));   // 指针相减得元素个数\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int *begin = a, *end = a;            // 用一个指针走到末尾\n    while (end < a + n) ++end;\n    printf(\"%d %d\\n\", n, (int)(end - begin));\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n-23 -10 13 -26 0\n",
                "expected_stdout": "5 5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n11\n",
                "expected_stdout": "1 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "20\n-47 33 42 -15 -48 11 20 -6 -20 5 -47 -42 -12 -34 26 -12 13 -14 -12 5\n",
                "expected_stdout": "20 20\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100\n-20 22 -38 -7 35 -19 30 29 -44 -31 16 17 36 16 -13 24 -42 18 50 -3 -7 40 -37 -39 9 0 -36 26 46 17 -12 -3 17 45 36 5 29 8 -21 11 30 -22 -8 22 -12 37 -38 -40 -33 23 34 32 -18 -6 -29 47 16 50 -26 11 -7 -40 17 -33 -38 -12 -8 -43 -24 5 -40 -16 -7 -39 -23 -20 -24 6 -40 -32 22 10 46 3 -5 -4 -37 -6 4 22 -41 47 -33 -50 -17 14 19 -43 29 12\n",
                "expected_stdout": "100 100\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "7\n-14 -25 49 -36 18 -36 -8\n",
                "expected_stdout": "7 7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "333\n45 26 19 42 -12 -49 46 32 -35 44 -34 11 11 -19 -15 2 24 4 23 -41 7 -42 -10 47 16 -9 13 -43 21 16 -37 1 6 -29 37 19 -4 -32 12 21 -40 15 9 29 -24 22 1 19 -17 40 -3 1 -45 4 30 -50 0 37 47 37 39 -21 -7 45 23 31 -37 -48 38 2 -10 -14 -21 -5 11 2 -28 45 -12 45 -46 37 44 -1 -1 -37 -46 -13 -44 -30 -10 -18 -45 12 -46 -32 -17 14 7 -48 28 26 -30 10 -22 20 13 3 42 21 6 35 -1 15 -13 -7 -1 28 -45 47 44 -37 -24 30 -12 -5 18 -5 -36 -6 48 6 -16 -13 25 -16 49 -23 -28 6 -3 -14 -39 -40 50 23 -43 -43 -33 -5 -45 49 14 32 -23 -17 22 -17 -30 45 -7 32 3 -15 4 18 20 -50 21 -28 14 -45 41 -2 13 -4 6 0 -44 -14 50 -38 -35 39 7 24 -36 -38 -3 11 29 39 14 5 4 8 -47 1 -1 -23 4 -27 32 -35 40 22 -33 -21 -27 19 15 -48 -21 -25 -3 18 46 -13 -37 28 -16 8 -12 -34 11 47 34 17 -14 -22 -50 -41 47 8 0 -49 -38 38 -3 42 34 -38 14 -14 49 -7 41 29 -6 -43 9 11 -27 -28 -23 -18 41 -44 -43 29 -17 -48 22 50 39 16 42 48 41 10 10 30 41 32 9 -41 -16 -40 -32 -31 46 -12 27 -13 -16 -23 -35 14 20 -44 12 -10 -22 34 -25 12 -38 -12 -26 -17 -23 -43 -29 -50 -48 23 2 -17 6 23 22 -14 1 30 15 36 34 26 31 -40 -39 32 18 36 33 47 45 -34 10 50 -42 -47 49\n",
                "expected_stdout": "333 333\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【指针】动态二维数组求每行之和",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "指针",
            "二维数组",
            "new"
        ],
        "statement_md": "用 `new int*[n]` 申请二维动态数组，读入 `n` 行 `m` 列的矩阵，输出每行元素之和（每行一个数）。\n\n**关键点**\n\n- `int **a = new int*[n]` 之后，还要对每一行 `a[i] = new int[m]`\n- 释放顺序反过来：先 `delete[] a[i]`，再 `delete[] a`\n- 一行的和用 `long long`",
        "input_format": "第一行 `n m`；之后 `n` 行，每行 `m` 个整数。",
        "output_format": "`n` 行，每行一个和。",
        "constraints_md": "- 1 ≤ n, m ≤ 100\n- |x| ≤ 10⁴",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 指针与引用",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n, m;\n    if (scanf(\"%d %d\", &n, &m) != 2) return 0;\n    int **a = new int *[n];            // 行指针数组\n    for (int i = 0; i < n; i++) a[i] = new int[m];\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < m; j++) scanf(\"%d\", &a[i][j]);\n    for (int i = 0; i < n; i++) {\n        long long s = 0;\n        for (int j = 0; j < m; j++) s += a[i][j];\n        printf(\"%lld\\n\", s);\n    }\n    for (int i = 0; i < n; i++) delete[] a[i];   // 先放行\n    delete[] a;                                   // 再放行指针数组\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n, m;\n    if (scanf(\"%d %d\", &n, &m) != 2) return 0;\n    int *flat = new int[n * m];        // 一维连续内存模拟二维\n    for (int i = 0; i < n * m; i++) scanf(\"%d\", &flat[i]);\n    for (int i = 0; i < n; i++) {\n        long long s = 0;\n        for (int j = 0; j < m; j++) s += flat[i * m + j];\n        printf(\"%lld\\n\", s);\n    }\n    delete[] flat;\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "2 2\n1 2\n3 4\n",
                "expected_stdout": "3\n7\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 1\n-5\n",
                "expected_stdout": "-5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 1\n1\n2\n3\n",
                "expected_stdout": "1\n2\n3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2 3\n1 2 3\n-1 -2 -3\n",
                "expected_stdout": "6\n-6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4 5\n31 -37 -52 62 87\n-78 -45 49 1 60\n30 -46 52 -23 -82\n-87 -32 -78 96 4\n",
                "expected_stdout": "91\n-13\n-69\n-97\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3 4\n1532 1435 1279 1803\n1323 1381 1788 1520\n1422 1159 1417 1063\n",
                "expected_stdout": "6049\n6012\n5061\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【指针】指针求两数组交集大小",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "指针",
            "交集",
            "双指针"
        ],
        "statement_md": "读入两个数组（含重复元素），求它们的**多重集交集**大小：某个值在两数组里分别出现 `c1`、`c2` 次，就对答案贡献 `min(c1, c2)`。输出交集大小。\n\n**关键点**\n\n- 先把第一个数组排序，再对第二个数组的每个元素做一次二分查找并「消耗」一个\n- 直接对每个元素 `count(a) == count(b)` 相加会把重复算多\n- 输出一个整数",
        "input_format": "第一行 `n m`；第二行 `n` 个整数；第三行 `m` 个整数。",
        "output_format": "一行：交集大小。",
        "constraints_md": "- 1 ≤ n, m ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 指针与引用",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n, m;\n    if (scanf(\"%d %d\", &n, &m) != 2) return 0;\n    static int a[1005], b[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    for (int i = 0; i < m; i++) scanf(\"%d\", &b[i]);\n    std::sort(a, a + n);\n    int used[1005] = {0}, c = 0;       // used 标记 a 里已被配对的下标\n    for (int i = 0; i < m; i++) {\n        for (int j = 0; j < n; j++)\n            if (!used[j] && a[j] == b[i]) { used[j] = 1; c++; break; }\n    }\n    printf(\"%d\\n\", c);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n, m;\n    if (scanf(\"%d %d\", &n, &m) != 2) return 0;\n    static int a[1005], b[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    for (int i = 0; i < m; i++) scanf(\"%d\", &b[i]);\n    std::sort(a, a + n);\n    std::sort(b, b + m);\n    int i = 0, j = 0, c = 0;           // 双指针归并式配对\n    while (i < n && j < m) {\n        if (a[i] == b[j]) { c++; i++; j++; }\n        else if (a[i] < b[j]) i++;\n        else j++;\n    }\n    printf(\"%d\\n\", c);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 4\n1 2 2 3 4\n2 2 5 3\n",
                "expected_stdout": "3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3 3\n1 1 1\n1 1 1\n",
                "expected_stdout": "3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1 1\n5\n6\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8 6\n5 1 5 4 2 5 4 1\n5 4 2 4 3 3\n",
                "expected_stdout": "4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10 10\n1 0 0 1 1 1 0 3 3 1\n3 0 3 0 1 3 0 3 3 1\n",
                "expected_stdout": "7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "4 4\n1 2 3 4\n4 3 2 1\n",
                "expected_stdout": "4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【指针】指针在有序数组中找第一个大于等于 x 的位置",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "指针",
            "二分",
            "lower_bound"
        ],
        "statement_md": "数组升序。读入 `n x` 和 `n` 个整数，输出第一个 `≥ x` 的元素位置（从 1 开始）；若所有元素都小于 `x`，输出 `n + 1`。\n\n**关键点**\n\n- 这就是 `lower_bound` 的语义，边界是「答案可以是 n」（表示插在末尾）\n- 手写二分的循环条件是 `lo < hi`，最后返回 `lo`\n- 输出一个整数",
        "input_format": "第一行 `n x`；第二行 `n` 个升序整数。",
        "output_format": "一行：位置（1 起）或 `n + 1`。",
        "constraints_md": "- 1 ≤ n ≤ 10⁵\n- |x|, |a[i]| ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 指针与引用",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n, x;\n    if (scanf(\"%d %d\", &n, &x) != 2) return 0;\n    static int a[100005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int lo = 0, hi = n;                // 答案允许是 n\n    while (lo < hi) {\n        int mid = lo + (hi - lo) / 2;\n        if (a[mid] >= x) hi = mid; else lo = mid + 1;\n    }\n    printf(\"%d\\n\", lo + 1);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n, x;\n    if (scanf(\"%d %d\", &n, &x) != 2) return 0;\n    static int a[100005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int *p = std::lower_bound(a, a + n, x);   // 指针差就是位置\n    printf(\"%d\\n\", (int)(p - a) + 1);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5 3\n1 2 3 4 5\n",
                "expected_stdout": "3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5 6\n1 2 3 4 5\n",
                "expected_stdout": "6\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5 0\n1 2 3 4 5\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
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
                "stdin": "10 8\n0 2 4 6 8 10 12 14 16 18\n",
                "expected_stdout": "5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "20 -100\n-20 -17 -14 -11 -8 -5 -2 1 4 7 10 13 16 19 22 25 28 31 34 37\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【指针】指针原地反转数组",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "指针",
            "反转",
            "双指针"
        ],
        "statement_md": "用首尾两个指针向中间靠拢，原地反转数组。读入 `n` 和 `n` 个整数，输出反转结果。\n\n**关键点**\n\n- `int *l = a, *r = a + n - 1;` 循环条件 `l < r`\n- 每轮交换后 `++l`、`--r`，走到中间就停\n- 输出一行，空格分隔",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：反转后的数组。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 指针与引用",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int *l = a, *r = a + n - 1;        // 首尾双指针\n    while (l < r) { int t = *l; *l++ = *r; *r-- = t; }\n    for (int i = 0; i < n; i++) printf(\"%d%c\", a[i], i + 1 == n ? '\\n' : ' ');\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nvoid rev(int *a, int n) {              // 递归反转\n    if (n <= 1) return;\n    int t = a[0]; a[0] = a[n - 1]; a[n - 1] = t;\n    rev(a + 1, n - 2);\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    rev(a, n);\n    for (int i = 0; i < n; i++) printf(\"%d%c\", a[i], i + 1 == n ? '\\n' : ' ');\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n40 2 41 30 42\n",
                "expected_stdout": "42 30 41 2 40\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n46 0 30 -32\n",
                "expected_stdout": "-32 30 0 46\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n12\n",
                "expected_stdout": "12\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "20\n-24 -2 12 -24 6 15 -50 7 -17 50 0 4 33 31 24 38 -44 40 47 47\n",
                "expected_stdout": "47 47 40 -44 38 24 31 33 4 0 50 -17 7 -50 15 6 -24 12 -2 -24\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n1 2 3 4 5\n",
                "expected_stdout": "5 4 3 2 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "33\n24 14 19 -14 37 49 3 19 18 3 24 -15 -26 33 -43 23 -47 17 -39 -28 -28 -20 31 -38 48 -42 17 -46 29 25 -21 -7 -40\n",
                "expected_stdout": "-40 -7 -21 25 29 -46 17 -42 48 -38 31 -20 -28 -28 -39 17 -47 23 -43 33 -26 -15 24 3 18 19 3 49 37 -14 19 14 24\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【指针】交换两个指针的指向",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "指针",
            "指向",
            "交换"
        ],
        "statement_md": "有 `int a`、`int b` 和两个指针 `int *p = &a`、`int *q = &b`。**交换 p 和 q 本身**（不是交换 a 和 b），读入 `a b`，输出交换后 `*p` 与 `*q`。\n\n**关键点**\n\n- `int *t = p; p = q; q = t;` 换的是指针，`a`、`b` 的值不变\n- 若写 `*p` 和 `*q` 互换，那就是改值不是改指向 —— 两件事完全不同\n- 输出一行两个整数",
        "input_format": "一行两个整数 `a b`。",
        "output_format": "一行：`*p *q`（交换指向之后）。",
        "constraints_md": "- |a|, |b| ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 指针与引用",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int a, b;\n    if (scanf(\"%d %d\", &a, &b) != 2) return 0;\n    int *p = &a, *q = &b;\n    int *t = p; p = q; q = t;          // 换的是指针本身\n    printf(\"%d %d\\n\", *p, *q);         // 所以变成 b a\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int a, b;\n    if (scanf(\"%d %d\", &a, &b) != 2) return 0;\n    int *arr[2] = {&a, &b};            // 用指针数组做一次对调\n    int *tmp = arr[0]; arr[0] = arr[1]; arr[1] = tmp;\n    printf(\"%d %d\\n\", *arr[0], *arr[1]);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3 5\n",
                "expected_stdout": "5 3\n",
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
                "stdin": "-1 1\n",
                "expected_stdout": "1 -1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "100 -100\n",
                "expected_stdout": "-100 100\n",
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
                "stdin": "123 456\n",
                "expected_stdout": "456 123\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【指针】指针实现选择排序",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "指针",
            "选择排序",
            "交换次数"
        ],
        "statement_md": "用指针实现选择排序（升序）。读入 `n` 和 `n` 个整数，输出排序结果，并额外输出「交换次数」。共两行：第一行排序结果，第二行交换次数。\n\n**关键点**\n\n- 选择排序每轮找最小值的下标，只有 `i != k` 时才真交换，交换次数才是准确的\n- 把每次 `std::swap` 都计入，全相等数组的交换次数会变成 0 —— 这是对的\n- 输出两行",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "第一行：升序数组；第二行：交换次数。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 指针与引用",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int sw = 0;\n    for (int i = 0; i < n - 1; i++) {\n        int k = i;\n        for (int j = i + 1; j < n; j++) if (*(a + j) < *(a + k)) k = j;\n        if (k != i) { int t = *(a + i); *(a + i) = *(a + k); *(a + k) = t; sw++; }\n    }\n    for (int i = 0; i < n; i++) printf(\"%d%c\", a[i], i + 1 == n ? '\\n' : ' ');\n    printf(\"%d\\n\", sw);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    int *a = new int[n];\n    for (int i = 0; i < n; i++) scanf(\"%d\", &a[i]);\n    int sw = 0;\n    for (int *p = a; p < a + n - 1; ++p) {\n        int *m = p;\n        for (int *q = p + 1; q < a + n; ++q) if (*q < *m) m = q;\n        if (m != p) { std::swap(*p, *m); sw++; }\n    }\n    for (int i = 0; i < n; i++) printf(\"%d%c\", a[i], i + 1 == n ? '\\n' : ' ');\n    printf(\"%d\\n\", sw);\n    delete[] a;\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n5 4 3 2 1\n",
                "expected_stdout": "1 2 3 4 5\n2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "5\n1 2 3 4 5\n",
                "expected_stdout": "1 2 3 4 5\n0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n3 3 3 3\n",
                "expected_stdout": "3 3 3 3\n0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2\n2 1\n",
                "expected_stdout": "1 2\n1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n16 -24 20 -29 -21 31 25 11 -46 46\n",
                "expected_stdout": "-46 -29 -24 -21 11 16 20 25 31 46\n7\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "8\n-9 -6 -1 -6 -3 -2 0 -5\n",
                "expected_stdout": "-9 -6 -6 -5 -3 -2 -1 0\n3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【指针】引用出参累计求和与积",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "指针",
            "引用",
            "出参"
        ],
        "statement_md": "写函数 `void accum(int x, long long &sum, long long &prod)`，把 `x` 累加到 `sum`、乘到 `prod` 上。读入 `n` 和 `n` 个整数，输出最终的 `sum` 与 `prod`。\n\n**关键点**\n\n- `sum` 要先初始化为 0、`prod` 初始化为 1，初始化放在 main 里更清楚\n- 10 个 5 相乘就到 9765625，`prod` 用 `long long` 更保险\n- 输出一行两个整数",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：`sum prod`。",
        "constraints_md": "- 1 ≤ n ≤ 20\n- 1 ≤ x ≤ 20\n- 保证 `prod` 不超过 10¹⁸",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 指针与引用",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nvoid accum(int x, long long &sum, long long &prod) {\n    sum += x;\n    prod *= x;\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    long long s = 0, p = 1;            // 初值：和 0、积 1\n    for (int i = 0; i < n; i++) { int x; scanf(\"%d\", &x); accum(x, s, p); }\n    printf(\"%lld %lld\\n\", s, p);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nstruct Accum { long long sum = 0, prod = 1; };\nvoid accum(int x, Accum &a) {          // 用结构体打包，同样是引用出参\n    a.sum += x; a.prod *= x;\n}\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    Accum a;\n    for (int i = 0; i < n; i++) { int x; scanf(\"%d\", &x); accum(x, a); }\n    printf(\"%lld %lld\\n\", a.sum, a.prod);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n1 2 3 4 5\n",
                "expected_stdout": "15 120\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n1\n",
                "expected_stdout": "1 1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\n2\n",
                "expected_stdout": "2 2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "10\n5 5 5 5 5 5 5 5 5 5\n",
                "expected_stdout": "50 9765625\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\n20 20 20\n",
                "expected_stdout": "60 8000\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\n1 3 5 7 9 11\n",
                "expected_stdout": "36 10395\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【指针】指针数组排序后输出",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "指针",
            "指针数组",
            "排序"
        ],
        "statement_md": "建立 `int *p[n]` 指针数组，每个元素指向原数组的一项，按指针指向的值排序后，用指针数组的顺序输出。读入 `n` 和 `n` 个整数，输出升序结果。\n\n**关键点**\n\n- 排序的是**指针**，原数组一动没动 —— 这就是「索引排序」\n- 比较器写 `bool cmp(int *a, int *b) { return *a < *b; }`\n- 输出一行，空格分隔",
        "input_format": "第一行 `n`，第二行 `n` 个整数。",
        "output_format": "一行：升序结果。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 指针与引用",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <algorithm>\nbool cmp(int *a, int *b) { return *a < *b; }\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    static int *p[1005];\n    for (int i = 0; i < n; i++) { scanf(\"%d\", &a[i]); p[i] = &a[i]; }\n    std::sort(p, p + n, cmp);          // 只排指针\n    for (int i = 0; i < n; i++) printf(\"%d%c\", *p[i], i + 1 == n ? '\\n' : ' ');\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    static int a[1005];\n    static int *p[1005];\n    for (int i = 0; i < n; i++) { scanf(\"%d\", &a[i]); p[i] = &a[i]; }\n    for (int i = 0; i < n - 1; i++)    // 手写指针数组冒泡\n        for (int j = 0; j < n - 1 - i; j++)\n            if (*p[j] > *p[j + 1]) { int *t = p[j]; p[j] = p[j + 1]; p[j + 1] = t; }\n    for (int i = 0; i < n; i++) printf(\"%d%c\", *p[i], i + 1 == n ? '\\n' : ' ');\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "5\n50 21 -1 2 -35\n",
                "expected_stdout": "-35 -1 2 21 50\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "4\n4 3 2 1\n",
                "expected_stdout": "1 2 3 4\n",
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
                "stdin": "20\n-5 -26 -23 -12 -5 44 -44 0 9 21 6 -24 23 44 39 -44 6 -12 23 -38\n",
                "expected_stdout": "-44 -44 -38 -26 -24 -23 -12 -12 -5 -5 0 6 6 9 21 23 23 39 44 44\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "15\n-18 24 71 99 84 30 52 -7 -38 4 84 82 -100 -11 78\n",
                "expected_stdout": "-100 -38 -18 -11 -7 4 24 30 52 71 78 82 84 84 99\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\n2 2 1 1 3\n",
                "expected_stdout": "1 1 2 2 3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【指针】指针遍历字符串统计数字字符",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "指针",
            "字符串",
            "遍历"
        ],
        "statement_md": "用指针遍历一个字符串（不含空格），统计其中数字字符 `0`~`9` 的个数。\n\n**关键点**\n\n- 字符串以 `\\0` 结尾，循环条件写 `*p != '\\0'`\n- 判断用 `*p >= '0' && *p <= '9'`，别写 `isdigit` 之外的自造条件（负字符会出错）\n- 输出一个整数",
        "input_format": "一行一个字符串（长度 ≤ 100，仅含可见 ASCII，不含空格）。",
        "output_format": "一行：数字字符个数。",
        "constraints_md": "- 1 ≤ 字符串长度 ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 指针与引用",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    char s[128];\n    if (scanf(\"%127s\", s) != 1) return 0;\n    int c = 0;\n    for (char *p = s; *p != '\\0'; ++p)          // 指针遍历到 '\\0'\n        if (*p >= '0' && *p <= '9') c++;\n    printf(\"%d\\n\", c);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cstring>\nint main() {\n    char s[128];\n    if (scanf(\"%127s\", s) != 1) return 0;\n    int c = 0;\n    for (int i = 0, n = (int)strlen(s); i < n; i++)\n        if (s[i] >= '0' && s[i] <= '9') c++;\n    printf(\"%d\\n\", c);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "a1b2c3\n",
                "expected_stdout": "3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "abc\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "123456\n",
                "expected_stdout": "6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "A1!z9\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "x0y0z0\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "Hello2024World\n",
                "expected_stdout": "4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【字符串】自己实现 strlen",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "字符串",
            "strlen"
        ],
        "statement_md": "不用 `strlen`，自己数到 `\\0` 为止。读入一个不含空格的字符串（长度 ≤ 100），输出它的长度。\n\n**关键点**\n\n- `char s[105]` 要留出放 `\\0` 的空间 —— 「abc」占 4 个字节\n- 循环条件写 `s[i] != '\\0'`\n- 输出一个整数",
        "input_format": "一行一个不含空格的字符串。",
        "output_format": "一行：长度。",
        "constraints_md": "- 1 ≤ 长度 ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 字符数组与字符串",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    char s[105];\n    if (scanf(\"%104s\", s) != 1) return 0;\n    int n = 0;\n    while (s[n] != '\\0') n++;          // 数到 '\\0'\n    printf(\"%d\\n\", n);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cstring>\nint main() {\n    char s[105];\n    if (scanf(\"%104s\", s) != 1) return 0;\n    printf(\"%d\\n\", (int)strlen(s));     // 库里也是这么数的\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "abc\n",
                "expected_stdout": "3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "a\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "hello\n",
                "expected_stdout": "5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "CPlusPlus\n",
                "expected_stdout": "9\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "12345\n",
                "expected_stdout": "5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "abcdefghij\n",
                "expected_stdout": "10\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【字符串】自己实现字符串拼接",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "字符串",
            "strcat"
        ],
        "statement_md": "不用 `strcat`，把第二个串接到第一个串末尾。读入两行不含空格的字符串，输出拼接结果。\n\n**关键点**\n\n- 拼接时从第一个串的 `\\0` 位置开始写，写完再补一个新的 `\\0`\n- 目标数组容量要够放下两串加 `\\0`\n- 输出一行",
        "input_format": "两行，各一个不含空格的字符串。",
        "output_format": "一行：拼接后的字符串。",
        "constraints_md": "- 每行长度 ≤ 50",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 字符数组与字符串",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    char a[120], b[60];\n    if (scanf(\"%59s\", a) != 1) return 0;\n    if (scanf(\"%59s\", b) != 1) return 0;\n    int i = 0, j = 0;\n    while (a[i] != '\\0') i++;          // 走到 a 的末尾\n    while (b[j] != '\\0') a[i++] = b[j++];\n    a[i] = '\\0';                       // 补结束符\n    printf(\"%s\\n\", a);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cstring>\nint main() {\n    char a[120], b[60];\n    if (scanf(\"%59s\", a) != 1) return 0;\n    if (scanf(\"%59s\", b) != 1) return 0;\n    strcat(a, b);                      // 库函数版\n    printf(\"%s\\n\", a);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "abc\ndef\n",
                "expected_stdout": "abcdef\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "a\nb\n",
                "expected_stdout": "ab\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "hello\nworld\n",
                "expected_stdout": "helloworld\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "C++\n2024\n",
                "expected_stdout": "C++2024\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "x\ny\n",
                "expected_stdout": "xy\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "123\n456\n",
                "expected_stdout": "123456\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【字符串】字符串反转输出",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "字符串",
            "反转"
        ],
        "statement_md": "读入一个不含空格的字符串，倒序输出。\n\n**关键点**\n\n- 首尾双指针交换，或直接从末尾往前输出\n- `for (int i = n - 1; i >= 0; i--)` 的 `i` 必须是有符号类型\n- 输出一行",
        "input_format": "一行一个不含空格的字符串。",
        "output_format": "一行：倒序字符串。",
        "constraints_md": "- 1 ≤ 长度 ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 字符数组与字符串",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    char s[105];\n    if (scanf(\"%104s\", s) != 1) return 0;\n    int n = 0;\n    while (s[n]) n++;\n    for (int i = n - 1; i >= 0; i--) putchar(s[i]);   // i 必须是有符号\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cstring>\n#include <algorithm>\nint main() {\n    char s[105];\n    if (scanf(\"%104s\", s) != 1) return 0;\n    std::reverse(s, s + strlen(s));    // 原地反转\n    printf(\"%s\\n\", s);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "abc\n",
                "expected_stdout": "cba\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "a\n",
                "expected_stdout": "a\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "hello\n",
                "expected_stdout": "olleh\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "12345\n",
                "expected_stdout": "54321\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "CPlusPlus\n",
                "expected_stdout": "sulPsulPC\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "xy\n",
                "expected_stdout": "yx\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【字符串】回文串判断",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "字符串",
            "回文"
        ],
        "statement_md": "读入一个不含空格的字符串（只含小写字母），判断它是不是回文串。是输出 `YES`，否则输出 `NO`。\n\n**关键点**\n\n- 首尾字符逐个比较，走到中间就停\n- 单字符一定是回文\n- 只输出 `YES` 或 `NO`",
        "input_format": "一行一个只含小写字母的字符串。",
        "output_format": "一行：`YES` 或 `NO`。",
        "constraints_md": "- 1 ≤ 长度 ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 字符数组与字符串",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    char s[105];\n    if (scanf(\"%104s\", s) != 1) return 0;\n    int n = 0;\n    while (s[n]) n++;\n    bool ok = true;\n    for (int i = 0, j = n - 1; i < j; i++, j--)\n        if (s[i] != s[j]) { ok = false; break; }\n    printf(\"%s\\n\", ok ? \"YES\" : \"NO\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cstring>\nint main() {\n    char s[105];\n    if (scanf(\"%104s\", s) != 1) return 0;\n    int n = (int)strlen(s);\n    bool ok = true;\n    for (int i = 0; i < n / 2; i++) if (s[i] != s[n - 1 - i]) ok = false;\n    printf(\"%s\\n\", ok ? \"YES\" : \"NO\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "abcba\n",
                "expected_stdout": "YES\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "abca\n",
                "expected_stdout": "NO\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "a\n",
                "expected_stdout": "YES\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "ab\n",
                "expected_stdout": "NO\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "aaaa\n",
                "expected_stdout": "YES\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "abccba\n",
                "expected_stdout": "YES\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【字符串】字符分类统计",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "字符串",
            "getline",
            "字符分类"
        ],
        "statement_md": "读入一行文本（可含空格），统计其中**字母**、**数字**、**其他字符**（含空格和符号）各有多少个，输出三个整数。\n\n**关键点**\n\n- 整行读入必须用 `getline` 或 `fgets`，`cin >>` 遇到空格就停了\n- 行尾的 `\\n` 不属于文本内容，要排除\n- 空格算「其他」，不是分隔符",
        "input_format": "一行文本（长度 ≤ 100，仅含可见 ASCII 字符与空格）。",
        "output_format": "一行：字母数、数字数、其他字符数。",
        "constraints_md": "- 1 ≤ 长度 ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 字符数组与字符串",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <cstring>\nint main() {\n    char s[128];\n    if (!fgets(s, sizeof(s), stdin)) return 0;\n    int n = (int)strlen(s);\n    if (n > 0 && s[n - 1] == '\\n') s[--n] = '\\0';   // 去掉行尾换行\n    int le = 0, di = 0, ot = 0;\n    for (int i = 0; i < n; i++) {\n        char c = s[i];\n        if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) le++;\n        else if (c >= '0' && c <= '9') di++;\n        else ot++;\n    }\n    printf(\"%d %d %d\\n\", le, di, ot);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <iostream>\n#include <string>\n#include <cctype>\nint main() {\n    std::string s;\n    if (!std::getline(std::cin, s)) return 0;\n    int le = 0, di = 0, ot = 0;\n    for (char c : s) {\n        if (isalpha((unsigned char)c)) le++;\n        else if (isdigit((unsigned char)c)) di++;\n        else ot++;\n    }\n    printf(\"%d %d %d\\n\", le, di, ot);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "abc123\n",
                "expected_stdout": "3 3 0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "a b c\n",
                "expected_stdout": "3 0 2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "Hello, World!\n",
                "expected_stdout": "10 0 3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "123\n",
                "expected_stdout": "0 3 0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "!!!\n",
                "expected_stdout": "0 0 3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "abc def 123 !\n",
                "expected_stdout": "6 3 4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【字符串】统计单词个数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "字符串",
            "单词计数"
        ],
        "statement_md": "读入一行英文（单词之间用一个或多个空格分隔，行首行尾可能有空格），输出单词个数。\n\n**关键点**\n\n- `cin >> word` 天然跳过空白，循环读到最后即可 —— 这是最简单的写法\n- 用 `getline` 的话要自己处理连续空格和首尾空格\n- 输出一个整数",
        "input_format": "一行英文文本（长度 ≤ 200）。",
        "output_format": "一行：单词个数。",
        "constraints_md": "- 1 ≤ 长度 ≤ 200\n- 单词只含字母",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 字符数组与字符串",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <iostream>\n#include <string>\nint main() {\n    std::string w;\n    int c = 0;\n    while (std::cin >> w) c++;         // >> 自动跳过空白\n    printf(\"%d\\n\", c);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cstring>\nint main() {\n    char s[256];\n    if (!fgets(s, sizeof(s), stdin)) return 0;\n    int c = 0;\n    bool in = false;\n    for (int i = 0; s[i]; i++) {\n        if (s[i] == ' ' || s[i] == '\\n') in = false;\n        else if (!in) { in = true; c++; }   // 从空白进入非空白才算一个新词\n    }\n    printf(\"%d\\n\", c);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "hello world\n",
                "expected_stdout": "2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "a\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "  a   b  c  \n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "one two three four\n",
                "expected_stdout": "4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "x y\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "The quick brown fox jumps\n",
                "expected_stdout": "5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【字符串】大小写互换",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "字符串",
            "大小写"
        ],
        "statement_md": "读入一个不含空格的字符串，把大写字母改成小写、小写字母改成大写，其余不变，输出结果。\n\n**关键点**\n\n- `c - 'a' + 'A'` 是小写转大写，反过去就是大写转小写\n- `toupper` / `tolower` 只对字母生效，其他字符原样返回\n- 输出一行",
        "input_format": "一行一个不含空格的字符串。",
        "output_format": "一行：大小写互换后的字符串。",
        "constraints_md": "- 1 ≤ 长度 ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 字符数组与字符串",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    char s[105];\n    if (scanf(\"%104s\", s) != 1) return 0;\n    for (int i = 0; s[i]; i++) {\n        if (s[i] >= 'a' && s[i] <= 'z') s[i] = char(s[i] - 'a' + 'A');\n        else if (s[i] >= 'A' && s[i] <= 'Z') s[i] = char(s[i] - 'A' + 'a');\n    }\n    printf(\"%s\\n\", s);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cctype>\nint main() {\n    char s[105];\n    if (scanf(\"%104s\", s) != 1) return 0;\n    for (int i = 0; s[i]; i++) {\n        if (isupper((unsigned char)s[i])) s[i] = (char)tolower((unsigned char)s[i]);\n        else if (islower((unsigned char)s[i])) s[i] = (char)toupper((unsigned char)s[i]);\n    }\n    printf(\"%s\\n\", s);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "AbC\n",
                "expected_stdout": "aBc\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "abc\n",
                "expected_stdout": "ABC\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "ABC\n",
                "expected_stdout": "abc\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "a1B2\n",
                "expected_stdout": "A1b2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "Hello\n",
                "expected_stdout": "hELLO\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "Zz\n",
                "expected_stdout": "zZ\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【字符串】字典序比较两串",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "字符串",
            "strcmp",
            "字典序"
        ],
        "statement_md": "读入两行不含空格的字符串，按字典序比较：第一个串小输出 `-1`，相等输出 `0`，第一个串大输出 `1`。\n\n**关键点**\n\n- `strcmp` 返回的是「差值」而不是固定的 -1/0/1，要自己归一\n- 字典序是逐字符比 ASCII 码，遇到第一个不同的字符就定胜负\n- 只输出 -1、0 或 1",
        "input_format": "两行，各一个不含空格的字符串。",
        "output_format": "一行：`-1`、`0` 或 `1`。",
        "constraints_md": "- 每行长度 ≤ 50",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 字符数组与字符串",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <cstring>\nint main() {\n    char a[60], b[60];\n    if (scanf(\"%59s\", a) != 1) return 0;\n    if (scanf(\"%59s\", b) != 1) return 0;\n    int c = strcmp(a, b);              // 返回差值，不是 -1/0/1\n    printf(\"%d\\n\", c < 0 ? -1 : (c > 0 ? 1 : 0));\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    char a[60], b[60];\n    if (scanf(\"%59s\", a) != 1) return 0;\n    if (scanf(\"%59s\", b) != 1) return 0;\n    int i = 0;\n    while (a[i] && a[i] == b[i]) i++;  // 手写逐字符比较\n    int r = 0;\n    if (a[i] != b[i]) r = (unsigned char)a[i] < (unsigned char)b[i] ? -1 : 1;\n    printf(\"%d\\n\", r);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "abc\nabd\n",
                "expected_stdout": "-1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "abc\nabc\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "abd\nabc\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "a\nab\n",
                "expected_stdout": "-1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "ab\na\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "Z\na\n",
                "expected_stdout": "-1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【字符串】子串首次出现位置",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "字符串",
            "子串",
            "find"
        ],
        "statement_md": "读入两个不含空格的字符串 `s` 和 `p`，输出 `p` 在 `s` 中**第一次**出现的起始位置（从 1 开始），找不到输出 `-1`。\n\n**关键点**\n\n- 朴素匹配：对每个起点 `i` 逐字符比对，全中就返回\n- `s.find(p)` 返回 `string::npos` 表示没找到，`npos` 是无符号的大数，用 `==` 判断\n- 起始位置从 1 开始，要 `+1`",
        "input_format": "两行：第一行 `s`，第二行 `p`。",
        "output_format": "一行：起始位置或 `-1`。",
        "constraints_md": "- 1 ≤ |p| ≤ |s| ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 字符数组与字符串",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <cstring>\nint main() {\n    char s[105], p[105];\n    if (scanf(\"%104s\", s) != 1) return 0;\n    if (scanf(\"%104s\", p) != 1) return 0;\n    int n = (int)strlen(s), m = (int)strlen(p);\n    int ans = -1;\n    for (int i = 0; i + m <= n; i++) {\n        int k = 0;\n        while (k < m && s[i + k] == p[k]) k++;\n        if (k == m) { ans = i + 1; break; }   // 题面要 1 起\n    }\n    printf(\"%d\\n\", ans);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <iostream>\n#include <string>\nint main() {\n    std::string s, p;\n    if (!(std::cin >> s)) return 0;\n    if (!(std::cin >> p)) return 0;\n    size_t k = s.find(p);              // npos 是无符号大数\n    printf(\"%d\\n\", k == std::string::npos ? -1 : (int)k + 1);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "abcabc\nbc\n",
                "expected_stdout": "2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "abcdef\ndef\n",
                "expected_stdout": "4\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "abcdef\nxyz\n",
                "expected_stdout": "-1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "aaaa\naa\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
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
                "stdin": "abab\nba\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【字符串】删除指定字符",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "字符串",
            "删除",
            "双指针"
        ],
        "statement_md": "读入一个不含空格的字符串和一个字符，删掉字符串里所有该字符，输出结果。输出可能为空行。\n\n**关键点**\n\n- 用「读指针 + 写指针」原地压缩：不删的字符往前搬\n- 删完要补 `\\0`，否则尾巴上的残留还会被打印\n- 如果全被删光，输出一个空行",
        "input_format": "第一行字符串（不含空格），第二行一个字符。",
        "output_format": "一行：删除后的字符串。",
        "constraints_md": "- 1 ≤ 长度 ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 字符数组与字符串",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    char s[105], c;\n    if (scanf(\"%104s\", s) != 1) return 0;\n    scanf(\" %c\", &c);                  // 前面的空格跳过换行\n    int k = 0;\n    for (int i = 0; s[i]; i++) if (s[i] != c) s[k++] = s[i];   // 读写双指针\n    s[k] = '\\0';\n    printf(\"%s\\n\", s);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <iostream>\n#include <string>\n#include <algorithm>\nint main() {\n    std::string s, line;\n    char c;\n    if (!(std::cin >> s)) return 0;\n    if (!(std::cin >> c)) return 0;\n    s.erase(std::remove(s.begin(), s.end(), c), s.end());   // erase-remove 惯用法\n    printf(\"%s\\n\", s.c_str());\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "abcabc\na\n",
                "expected_stdout": "bcbc\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "abc\nd\n",
                "expected_stdout": "abc\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "aaaa\na\n",
                "expected_stdout": "\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "banana\nn\n",
                "expected_stdout": "baaa\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "xyz\nx\n",
                "expected_stdout": "yz\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "hello\nl\n",
                "expected_stdout": "heo\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【字符串】按字典序排序若干字符串",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "字符串",
            "排序",
            "字典序"
        ],
        "statement_md": "读入 `n` 个不含空格的字符串，按字典序升序输出，每行一个。\n\n**关键点**\n\n- `std::sort` 配 `std::string` 默认就是字典序\n- 用 `char[105]` 数组的话要写 `strcmp` 比较器\n- 每行输出一个字符串",
        "input_format": "第一行 `n`；之后 `n` 行，每行一个不含空格的字符串。",
        "output_format": "`n` 行：按字典序升序。",
        "constraints_md": "- 1 ≤ n ≤ 100\n- 每串长度 ≤ 50",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 字符数组与字符串",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\n#include <cstring>\n#include <algorithm>\nchar s[105][60];\nint idx[105];\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    for (int i = 0; i < n; i++) { scanf(\"%59s\", s[i]); idx[i] = i; }\n    std::sort(idx, idx + n, [](int x, int y) {     // 排下标，不排二维数组\n        return strcmp(s[x], s[y]) < 0;\n    });\n    for (int i = 0; i < n; i++) printf(\"%s\\n\", s[idx[i]]);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <iostream>\n#include <string>\n#include <vector>\n#include <algorithm>\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) != 1 || n <= 0) return 0;\n    std::vector<std::string> v(n);\n    for (int i = 0; i < n; i++) std::cin >> v[i];\n    std::sort(v.begin(), v.end());     // string 默认字典序\n    for (auto &x : v) printf(\"%s\\n\", x.c_str());\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "3\nbanana\napple\ncherry\n",
                "expected_stdout": "apple\nbanana\ncherry\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "1\nonly\n",
                "expected_stdout": "only\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "3\nb\na\nc\n",
                "expected_stdout": "a\nb\nc\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "5\nzebra\napple\nmango\nbanana\ncherry\n",
                "expected_stdout": "apple\nbanana\ncherry\nmango\nzebra\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "3\naa\na\naaa\n",
                "expected_stdout": "a\naa\naaa\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "6\nbbbb\ncccc\ncccc\nmmmm\nnnnn\nyyyy\n",
                "expected_stdout": "bbbb\ncccc\ncccc\nmmmm\nnnnn\nyyyy\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【字符串】字符串压缩",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "字符串",
            "压缩",
            "游程"
        ],
        "statement_md": "把连续相同的字符压缩成「字符 + 次数」。例如 `aabbb` 压缩成 `a2b3`，`abc` 压缩成 `a1b1c1`。读入一个不含空格的字符串，输出压缩结果。\n\n**关键点**\n\n- 统计每一段连续相同字符的长度，然后「字符 + 次数」拼起来\n- 次数为 1 也要写出来（题面规定），不要自作聪明省略\n- 段数最多等于字符串长度",
        "input_format": "一行一个不含空格的字符串。",
        "output_format": "一行：压缩结果。",
        "constraints_md": "- 1 ≤ 长度 ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 字符数组与字符串",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    char s[105];\n    if (scanf(\"%104s\", s) != 1) return 0;\n    int i = 0;\n    while (s[i]) {\n        int j = i;\n        while (s[j] == s[i]) j++;      // 找到这一段结束的位置\n        printf(\"%c%d\", s[i], j - i);\n        i = j;\n    }\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <iostream>\n#include <string>\nint main() {\n    std::string s;\n    if (!(std::cin >> s)) return 0;\n    std::string out;\n    for (size_t i = 0; i < s.size();) {\n        size_t j = i;\n        while (j < s.size() && s[j] == s[i]) j++;\n        out += s[i];\n        out += std::to_string(j - i);\n        i = j;\n    }\n    printf(\"%s\\n\", out.c_str());\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "aabbb\n",
                "expected_stdout": "a2b3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "abc\n",
                "expected_stdout": "a1b1c1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "aaaa\n",
                "expected_stdout": "a4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "a\n",
                "expected_stdout": "a1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "aabbcc\n",
                "expected_stdout": "a2b2c2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "abbbbc\n",
                "expected_stdout": "a1b4c1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【字符串】自己实现 atoi",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "字符串",
            "atoi",
            "进制"
        ],
        "statement_md": "不用 `atoi`，把数字字符串转成整数。读入一行（可能有前导 `+`/`-`，其余全是数字），输出转换后的整数。\n\n**关键点**\n\n- 跳过符号位后逐位 `r = r * 10 + (c - '0')`\n- 负号要最后再乘上去\n- 保证结果在 `int` 范围内",
        "input_format": "一行：可选的符号 + 若干数字。",
        "output_format": "一行：转换后的整数。",
        "constraints_md": "- 1 ≤ 数字位数 ≤ 9\n- 结果在 `int` 范围内",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 字符数组与字符串",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    char s[32];\n    if (scanf(\"%31s\", s) != 1) return 0;\n    int i = 0, sign = 1;\n    if (s[0] == '+' || s[0] == '-') { if (s[0] == '-') sign = -1; i = 1; }\n    int r = 0;\n    for (; s[i]; i++) r = r * 10 + (s[i] - '0');   // 逐位累加\n    printf(\"%d\\n\", sign * r);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cstdlib>\nint main() {\n    char s[32];\n    if (scanf(\"%31s\", s) != 1) return 0;\n    printf(\"%d\\n\", atoi(s));           // 库函数版\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "123\n",
                "expected_stdout": "123\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "-456\n",
                "expected_stdout": "-456\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "+789\n",
                "expected_stdout": "789\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "0\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "-1\n",
                "expected_stdout": "-1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "2147483647\n",
                "expected_stdout": "2147483647\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【字符串】字符串中的数字求和",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "字符串",
            "数字提取"
        ],
        "statement_md": "读入一个不含空格的字符串，把其中每一段连续的数字当作一个整数，求它们的和。例如 `a12b3c` 里是 12 和 3，和为 15。\n\n**关键点**\n\n- 用一个累加器 `cur`，遇到数字就 `cur = cur * 10 + d`\n- 遇到非数字时把 `cur` 结算掉并清零\n- 结尾如果还在数字里，别忘了再结算一次",
        "input_format": "一行一个不含空格的字符串。",
        "output_format": "一行：所有数字段之和。",
        "constraints_md": "- 1 ≤ 长度 ≤ 100\n- 每段数字 ≤ 10⁶",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 字符数组与字符串",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    char s[105];\n    if (scanf(\"%104s\", s) != 1) return 0;\n    long long sum = 0, cur = 0;\n    bool in = false;\n    for (int i = 0; s[i]; i++) {\n        if (s[i] >= '0' && s[i] <= '9') { cur = cur * 10 + (s[i] - '0'); in = true; }\n        else if (in) { sum += cur; cur = 0; in = false; }\n    }\n    if (in) sum += cur;                // 结尾还在数字里\n    printf(\"%lld\\n\", sum);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cctype>\n#include <cstdlib>\nint main() {\n    char s[105];\n    if (scanf(\"%104s\", s) != 1) return 0;\n    long long sum = 0;\n    char buf[16];\n    int k = 0;\n    for (int i = 0;; i++) {\n        if (isdigit((unsigned char)s[i])) buf[k++] = s[i];\n        else {\n            if (k) { buf[k] = '\\0'; sum += atoll(buf); k = 0; }\n            if (!s[i]) break;          // 到串尾才真正结束\n        }\n    }\n    printf(\"%lld\\n\", sum);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "a12b3c\n",
                "expected_stdout": "15\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "abc\n",
                "expected_stdout": "0\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "123\n",
                "expected_stdout": "123\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "a1b2c3\n",
                "expected_stdout": "6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "x100y\n",
                "expected_stdout": "100\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "9a9b9\n",
                "expected_stdout": "27\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【字符串】最长连续相同字符段",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "字符串",
            "扫描"
        ],
        "statement_md": "读入一个不含空格的字符串，输出最长的一段连续相同字符的长度。\n\n**关键点**\n\n- 一遍扫描，`run` 记录当前段长，不同就重置为 1\n- `best` 在每步后更新，别只在重置时才更新\n- 输出一个整数",
        "input_format": "一行一个不含空格的字符串。",
        "output_format": "一行：最长连续段长度。",
        "constraints_md": "- 1 ≤ 长度 ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 字符数组与字符串",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    char s[105];\n    if (scanf(\"%104s\", s) != 1) return 0;\n    int best = 1, run = 1;\n    for (int i = 1; s[i]; i++) {\n        run = (s[i] == s[i - 1]) ? run + 1 : 1;\n        if (run > best) best = run;\n    }\n    printf(\"%d\\n\", best);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cstring>\nint main() {\n    char s[105];\n    if (scanf(\"%104s\", s) != 1) return 0;\n    int n = (int)strlen(s), best = 1;\n    for (int i = 0; i < n;) {          // 按段跳\n        int j = i;\n        while (j < n && s[j] == s[i]) j++;\n        if (j - i > best) best = j - i;\n        i = j;\n    }\n    printf(\"%d\\n\", best);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "aabbbcc\n",
                "expected_stdout": "3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "abc\n",
                "expected_stdout": "1\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "aaaa\n",
                "expected_stdout": "4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "a\n",
                "expected_stdout": "1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "abbbbc\n",
                "expected_stdout": "4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "aabbccdd\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【字符串】统计元音字母个数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "字符串",
            "元音",
            "统计"
        ],
        "statement_md": "读入一个不含空格的字符串，统计其中元音字母 `a e i o u`（不区分大小写）的总个数。\n\n**关键点**\n\n- 先把字符统一转成小写再判断，或者判断两套字母\n- `y` 不算元音\n- 输出一个整数",
        "input_format": "一行一个不含空格的字符串。",
        "output_format": "一行：元音个数。",
        "constraints_md": "- 1 ≤ 长度 ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 字符数组与字符串",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    char s[105];\n    if (scanf(\"%104s\", s) != 1) return 0;\n    int c = 0;\n    for (int i = 0; s[i]; i++) {\n        char ch = s[i];\n        if (ch >= 'A' && ch <= 'Z') ch = char(ch - 'A' + 'a');   // 统一转小写\n        if (ch == 'a' || ch == 'e' || ch == 'i' || ch == 'o' || ch == 'u') c++;\n    }\n    printf(\"%d\\n\", c);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cstring>\nint main() {\n    char s[105];\n    if (scanf(\"%104s\", s) != 1) return 0;\n    int c = 0;\n    for (int i = 0; s[i]; i++) c += (strchr(\"aeiouAEIOU\", s[i]) != nullptr);\n    printf(\"%d\\n\", c);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "aeiou\n",
                "expected_stdout": "5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "AEIOU\n",
                "expected_stdout": "5\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "xyz\n",
                "expected_stdout": "0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "hello\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "Programming\n",
                "expected_stdout": "3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "aA\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【字符串】字符串左循环移位",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "字符串",
            "循环移位",
            "rotate"
        ],
        "statement_md": "读入一个不含空格的字符串和整数 `k`，把字符串循环左移 `k` 位（`k` 可能大于长度）。输出移位后的结果。\n\n**关键点**\n\n- `k` 要先对长度取模，`k = 8`、长度 5 时等价于移 3 位\n- 左移 k 位的结果是 `s[k..n-1] + s[0..k-1]`\n- 输出一行",
        "input_format": "第一行字符串（不含空格），第二行整数 `k`。",
        "output_format": "一行：左移 `k` 位后的字符串。",
        "constraints_md": "- 1 ≤ 长度 ≤ 100\n- 0 ≤ k ≤ 10⁹",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 字符数组与字符串",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    char s[105];\n    long long k;\n    if (scanf(\"%104s\", s) != 1) return 0;\n    if (scanf(\"%lld\", &k) != 1) return 0;\n    int n = 0;\n    while (s[n]) n++;\n    k %= n;                            // k 可能比长度大得多\n    for (int i = 0; i < n; i++) putchar(s[(int)((i + k) % n)]);\n    printf(\"\\n\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cstring>\n#include <algorithm>\nint main() {\n    char s[105];\n    long long k;\n    if (scanf(\"%104s\", s) != 1) return 0;\n    if (scanf(\"%lld\", &k) != 1) return 0;\n    int n = (int)strlen(s);\n    k %= n;\n    std::rotate(s, s + k, s + n);      // 三次反转的封装\n    printf(\"%s\\n\", s);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "abcde\n2\n",
                "expected_stdout": "cdeab\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "abcde\n0\n",
                "expected_stdout": "abcde\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "abcde\n5\n",
                "expected_stdout": "abcde\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "abcde\n7\n",
                "expected_stdout": "cdeab\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "a\n1000000000\n",
                "expected_stdout": "a\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "abcd\n1\n",
                "expected_stdout": "bcda\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【字符串】判断变位词",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "字符串",
            "变位词",
            "频次"
        ],
        "statement_md": "两个字符串由相同字母重排得到（长度相同、每个字母出现次数相同）称为变位词。读入两行不含空格的字符串，是变位词输出 `YES`，否则输出 `NO`。\n\n**关键点**\n\n- 统计 26 个字母的频次数组，逐位比较\n- 也可以两串各自排序后比较\n- 只输出 `YES` 或 `NO`",
        "input_format": "两行，各一个不含空格的小写字符串。",
        "output_format": "一行：`YES` 或 `NO`。",
        "constraints_md": "- 每行长度 ≤ 100\n- 只含小写字母",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 字符数组与字符串",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    char a[105], b[105];\n    if (scanf(\"%104s\", a) != 1) return 0;\n    if (scanf(\"%104s\", b) != 1) return 0;\n    int ca[26] = {0}, cb[26] = {0};\n    for (int i = 0; a[i]; i++) ca[a[i] - 'a']++;\n    for (int i = 0; b[i]; i++) cb[b[i] - 'a']++;\n    bool ok = true;\n    for (int i = 0; i < 26; i++) if (ca[i] != cb[i]) ok = false;\n    printf(\"%s\\n\", ok ? \"YES\" : \"NO\");\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <cstring>\n#include <algorithm>\nint main() {\n    char a[105], b[105];\n    if (scanf(\"%104s\", a) != 1) return 0;\n    if (scanf(\"%104s\", b) != 1) return 0;\n    if (strlen(a) != strlen(b)) { printf(\"NO\\n\"); return 0; }\n    std::sort(a, a + strlen(a));       // 各自排序后比较\n    std::sort(b, b + strlen(b));\n    printf(\"%s\\n\", strcmp(a, b) == 0 ? \"YES\" : \"NO\");\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "listen\nsilent\n",
                "expected_stdout": "YES\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "abc\nabd\n",
                "expected_stdout": "NO\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "a\na\n",
                "expected_stdout": "YES\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "abc\ncba\n",
                "expected_stdout": "YES\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "aab\nabb\n",
                "expected_stdout": "NO\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "hello\nworld\n",
                "expected_stdout": "NO\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【字符串】去掉重复字符保序",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "字符串",
            "去重",
            "set"
        ],
        "statement_md": "读入一个不含空格的字符串，去掉重复出现的字符，只保留**第一次**出现的位置，输出结果。\n\n**关键点**\n\n- 用一个 `bool seen[256]` 记录字符是否出现过\n- 扫描时按原顺序决定是否输出，天然保持顺序\n- 输出一行",
        "input_format": "一行一个不含空格的字符串。",
        "output_format": "一行：去重后的字符串。",
        "constraints_md": "- 1 ≤ 长度 ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 字符数组与字符串",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    char s[105];\n    if (scanf(\"%104s\", s) != 1) return 0;\n    bool seen[256] = {false};\n    int k = 0;\n    for (int i = 0; s[i]; i++) {\n        unsigned char c = (unsigned char)s[i];\n        if (!seen[c]) { seen[c] = true; s[k++] = s[i]; }   // 第一次出现才留\n    }\n    s[k] = '\\0';\n    printf(\"%s\\n\", s);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\n#include <iostream>\n#include <string>\n#include <set>\nint main() {\n    std::string s, out;\n    if (!(std::cin >> s)) return 0;\n    std::set<char> seen;\n    for (char c : s) if (seen.insert(c).second) out += c;   // insert 返回是否新插入\n    printf(\"%s\\n\", out.c_str());\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "abacb\n",
                "expected_stdout": "abc\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "aaaa\n",
                "expected_stdout": "a\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "abc\n",
                "expected_stdout": "abc\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "abcdefga\n",
                "expected_stdout": "abcdefg\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "aAbB\n",
                "expected_stdout": "aAbB\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "hello\n",
                "expected_stdout": "helo\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    },
    {
        "title": "【字符串】统计回文子串个数",
        "subject": "cpp",
        "line": "cpp",
        "difficulty": 4,
        "total_score": 16,
        "tags": [
            "字符串",
            "回文子串",
            "中心扩展"
        ],
        "statement_md": "读入一个不含空格的字符串（只含小写字母），统计长度 **≥ 2** 的回文子串个数。不同起止位置算不同子串，内容相同也算多个。\n\n**关键点**\n\n- 枚举所有起点和终点，判回文，`n ≤ 100` 时 O(n³) 也能过\n- 更快的做法是中心扩展，但先把暴力写对更重要\n- 长度 1 的子串不算",
        "input_format": "一行一个只含小写字母的字符串。",
        "output_format": "一行：回文子串个数。",
        "constraints_md": "- 1 ≤ 长度 ≤ 100",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "float_eps": 1e-06,
        "origin": "manual",
        "status": "published",
        "source_section": "C++ 编程 · 字符数组与字符串",
        "ref_interpreter": "gpp",
        "reference_solution": "#include <cstdio>\nint main() {\n    char s[105];\n    if (scanf(\"%104s\", s) != 1) return 0;\n    int n = 0;\n    while (s[n]) n++;\n    int c = 0;\n    for (int i = 0; i < n; i++)\n        for (int j = i + 1; j < n; j++) {          // 长度 >= 2\n            int l = i, r = j;\n            bool ok = true;\n            while (l < r) { if (s[l] != s[r]) { ok = false; break; } l++; r--; }\n            if (ok) c++;\n        }\n    printf(\"%d\\n\", c);\n    return 0;\n}\n",
        "alt_solution": "#include <cstdio>\nint main() {\n    char s[105];\n    if (scanf(\"%104s\", s) != 1) return 0;\n    int n = 0;\n    while (s[n]) n++;\n    int c = 0;\n    for (int center = 0; center < 2 * n - 1; center++) {   // 中心扩展\n        int l = center / 2, r = l + center % 2;\n        while (l >= 0 && r < n && s[l] == s[r]) {\n            if (r - l + 1 >= 2) c++;\n            l--; r++;\n        }\n    }\n    printf(\"%d\\n\", c);\n    return 0;\n}\n",
        "cases": [
            {
                "stdin": "aaa\n",
                "expected_stdout": "3\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "abba\n",
                "expected_stdout": "2\n",
                "is_sample": 1,
                "kind": "sample",
                "explanation": ""
            },
            {
                "stdin": "abc\n",
                "expected_stdout": "0\n",
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
                "stdin": "aaaa\n",
                "expected_stdout": "6\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            },
            {
                "stdin": "abab\n",
                "expected_stdout": "2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": ""
            }
        ]
    }
]
