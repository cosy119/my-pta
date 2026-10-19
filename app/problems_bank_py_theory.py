"""Python 线理论题库 —— **自动生成，不要手改**。

本文件由 `tools/gen_py_theory.py` 产出，重新生成：

    python tools/gen_py_theory.py

题源
----
《Python快乐编程基础入门》（ISBN 9787302530145）第 02 ~ 14 讲的知识点，
按讲义章节分节（`source_section`），与同节的编程题并列。
全部是**理论题**（`line = "text"`）：提交答案文本，由 `app/judge/runner_text.py`
归一化后交给 `oneof` checker 比对，不启子进程。

答案可信度
----------
凡能实跑的题，答案键都是 `expect` 表达式**在本机 3.13 上跑出来的结果反推**的，
不是手写的；生成器跑不通过的题根本写不出这个文件。
少数纯定义题（列表与元组的区别、*args 语义之类）无法用一行代码判定，
在生成器里标了「无实跑」，靠教材口径人工核对。
"""
from __future__ import annotations

PY_THEORY_PROBLEMS: list[dict] = [
    {
        "title": "幂运算符是右结合",
        "subject": "python",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "运算符",
            "优先级"
        ],
        "choices": [
            "64",
            "512",
            "12",
            "语法错误"
        ],
        "source_section": "第 02 讲 · 编程基础",
        "statement_md": "表达式 `2 ** 3 ** 2` 的值是多少？",
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
                "explanation": "`**` 是**右结合**：先算 `3 ** 2 = 9`，再算 `2 ** 9 = 512`。如果按从左往右算会得 `(2**3)**2 = 64`，那是错的。要左结合必须自己加括号。"
            }
        ]
    },
    {
        "title": "负数整除是向下取整",
        "subject": "python",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "运算符",
            "整除"
        ],
        "choices": [
            "-4",
            "-3",
            "-3.5",
            "3"
        ],
        "source_section": "第 02 讲 · 编程基础",
        "statement_md": "表达式 `-7 // 2` 的值是多少？",
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
                "explanation": "`//` 是**向下取整**（floor），不是向零截断：`-3.5` 往下取到 `-4`。这与 C/Java 的整数除法（向零截断得 `-3`）不同，是跨语言最容易踩的一处。"
            }
        ]
    },
    {
        "title": "取模结果的符号跟着除数",
        "subject": "python",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "运算符",
            "取模"
        ],
        "choices": [
            "-1",
            "1",
            "2",
            "-2"
        ],
        "source_section": "第 02 讲 · 编程基础",
        "statement_md": "表达式 `-7 % 3` 的值是多少？",
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
                "explanation": "Python 的 `%` 结果符号**跟除数一致**（这里除数是正数 3，所以结果为正）。它满足 `a == (a // b) * b + a % b`：`(-4)*3 + 2 = -10`？不对——是 `(-3)*3 + 2 = -7`。记住这条恒等式就能自己推，不用背。"
            }
        ]
    },
    {
        "title": "浮点数参与整除的结果类型",
        "subject": "python",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "运算符",
            "类型"
        ],
        "choices": [
            "3",
            "3.0",
            "3.5",
            "4.0"
        ],
        "source_section": "第 02 讲 · 编程基础",
        "statement_md": "表达式 `7 // 2.0` 的值是多少？",
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
                "explanation": "`//` 只是「取整」，**不改变类型**：有 float 参与就还是 float，所以是 `3.0` 而不是 `3`。"
            }
        ]
    },
    {
        "title": "range 的负步长",
        "subject": "python",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "range",
            "循环"
        ],
        "choices": [
            "[5, 3, 1]",
            "[5, 3, 1, -1]",
            "[4, 2, 0]",
            "[5, 4, 3, 2, 1]"
        ],
        "source_section": "第 03 讲 · 流程控制语句",
        "statement_md": "`list(range(5, 0, -2))` 的结果是什么？",
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
                "explanation": "`range(start, stop, step)` 是**左闭右开**：从 5 开始，每次减 2，取到 `> 0` 为止 → 5、3、1。`stop` 那个 0 本身取不到。"
            }
        ]
    },
    {
        "title": "循环被 break 时 else 不执行",
        "subject": "python",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "for-else",
            "break"
        ],
        "choices": [
            "[]",
            "['else']",
            "[0, 1]",
            "报错"
        ],
        "source_section": "第 03 讲 · 流程控制语句",
        "statement_md": "下面这段代码执行后 `hit` 是什么？\n\n```python\nhit = []\nfor i in range(3):\n    if i == 1:\n        break\nelse:\n    hit.append('else')\n```",
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
                "explanation": "`for ... else` 的 `else` 只在**循环正常走完**（没被 break 打断）时执行。这里 `i == 1` 就 break 了，所以 `hit` 一直是空列表。它是「没找到才执行」的天然写法，比设一个 flag 变量干净。"
            }
        ]
    },
    {
        "title": "循环变量在循环结束后仍存在",
        "subject": "python",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "作用域",
            "循环"
        ],
        "choices": [
            "2",
            "3",
            "0",
            "NameError：i 不存在"
        ],
        "source_section": "第 03 讲 · 流程控制语句",
        "statement_md": "执行 `for i in range(3): pass` 之后，变量 `i` 的值是多少？",
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
                "explanation": "Python 的循环**不产生新的作用域**，循环变量在循环结束后依然存在，值是最后一次赋的值（这里依次是 0、1、2，所以停在 2）。这一点跟 C 的 `for (int i ...)` 完全不同。"
            }
        ]
    },
    {
        "title": "切片反转字符串",
        "subject": "python",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "切片",
            "字符串"
        ],
        "choices": [
            "'abc'",
            "'cba'",
            "'c'",
            "报错"
        ],
        "source_section": "第 04 讲 · 字符串",
        "statement_md": "`'abc'[::-1]` 的结果是什么？",
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
                "explanation": "切片 `[start:stop:step]` 三段全省略、步长给 `-1`，就是从尾到头取一遍 → `'cba'`。这是 Python 里反转序列最惯用的写法，列表、元组同样适用。"
            }
        ]
    },
    {
        "title": "split 不合并连续分隔符产生的空串",
        "subject": "python",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "split",
            "字符串"
        ],
        "choices": [
            "['a', 'b', 'c']",
            "['a', 'b', '', 'c']",
            "['a', 'b', ',', 'c']",
            "报错"
        ],
        "source_section": "第 04 讲 · 字符串",
        "statement_md": "`'a,b,,c'.split(',')` 的结果是什么？",
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
                "explanation": "`split` 按分隔符**机械切开**，中间连续两个逗号之间会留下一个空串，所以是 4 段。如果要丢掉空段，用 `[x for x in s.split(',') if x]`，或者干脆用 `re.split` 后过滤。"
            }
        ]
    },
    {
        "title": "find 找不到时返回 -1",
        "subject": "python",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "find",
            "字符串"
        ],
        "choices": [
            "-1",
            "0",
            "None",
            "抛出 ValueError"
        ],
        "source_section": "第 04 讲 · 字符串",
        "statement_md": "`'abc'.find('z')` 的返回值是多少？",
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
                "explanation": "`find` 找不到返回 **-1**，不抛异常——所以 `if s.find(x):` 这种写法是坑：找到了但位置是 0 时它是假值。要判存在就用 `x in s`。对比：`index` 找不到会抛 `ValueError`。"
            }
        ]
    },
    {
        "title": "列表乘法的浅拷贝",
        "subject": "python",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "列表",
            "乘法"
        ],
        "choices": [
            "[1, 2, 1, 2]",
            "[2, 4]",
            "[1, 2, 2]",
            "报错"
        ],
        "source_section": "第 05 讲 · 列表与元组",
        "statement_md": "`[1, 2] * 2` 的结果是什么？",
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
                "explanation": "`*` 是**重复**，不是逐元素相乘（逐元素要 numpy）。注意它做的是**浅拷贝**：`[[0]] * 3` 得到的三行是**同一个列表对象**，改一行会全变——这是二维数组初始化的经典坑。"
            }
        ]
    },
    {
        "title": "sort 返回 None 而不是新列表",
        "subject": "python",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "sort",
            "就地"
        ],
        "choices": [
            "None",
            "[1, 2, 3]",
            "[3, 1, 2]",
            "报错"
        ],
        "source_section": "第 05 讲 · 列表与元组",
        "statement_md": "```python\na = [3, 1, 2]\nr = a.sort()\n```\n执行后 `r` 是什么？",
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
                "explanation": "`list.sort()` 是**就地**排序，返回值恒为 `None`（故意这样设计，提醒你它改的是原列表）。要新列表用 `sorted(a)`。`r = a.sort()` 之后 `r` 是 None、`a` 已经变成有序——再对 `r` 做 `for` 循环就会 TypeError。"
            }
        ]
    },
    {
        "title": "单元素元组必须带逗号",
        "subject": "python",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "元组",
            "语法"
        ],
        "choices": [
            "1",
            "0",
            "2",
            "报错"
        ],
        "source_section": "第 05 讲 · 列表与元组",
        "statement_md": "`len((1,))` 的值是多少？",
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
                "explanation": "`(1)` 只是加括号的整数 1，**不是元组**；单元素元组必须写成 `(1,)`，那个逗号才是元组构造符。空元组例外，写 `()` 就行。"
            }
        ]
    },
    {
        "title": "get 取不到时返回 None",
        "subject": "python",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "dict",
            "get"
        ],
        "choices": [
            "None",
            "KeyError",
            "0",
            "''"
        ],
        "source_section": "第 06 讲 · 字典与集合",
        "statement_md": "`{'a': 1}.get('b')` 的结果是什么？",
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
                "explanation": "`d.get(k)` 取不到返回 `None`（可以给第二个参数指定默认值），**不抛异常**；`d[k]` 取不到才抛 `KeyError`。所以「不确定键在不在」时用 `get`。"
            }
        ]
    },
    {
        "title": "集合自动去重",
        "subject": "python",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "set",
            "去重"
        ],
        "choices": [
            "3",
            "5",
            "1",
            "报错"
        ],
        "source_section": "第 06 讲 · 字典与集合",
        "statement_md": "`len({1, 1, 2, 2, 3})` 的值是多少？",
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
                "explanation": "集合的键唯一，重复的会被**静默丢掉**，所以剩 `{1, 2, 3}`，长度 3。「一行去重」就靠这个：`list(set(seq))`（注意这会打乱顺序，要保序用 `dict.fromkeys`）。"
            }
        ]
    },
    {
        "title": "默认参数只在定义时求值一次",
        "subject": "python",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "默认参数",
            "陷阱"
        ],
        "choices": [
            "([1, 2], [1, 2])",
            "([1], [2])",
            "([1], [1, 2])",
            "报错"
        ],
        "source_section": "第 07 讲 · 函数",
        "statement_md": "```python\ndef f(a, acc=[]):\n    acc.append(a)\n    return acc\n```\n连续调用 `f(1)`、`f(2)`，两次的返回值合起来是什么？",
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
                "explanation": "默认值在**函数定义时求值一次**并挂在 `f.__defaults__` 上，之后每次调用共用同一个列表，所以第一次 append 1、第二次 append 2，两次返回的是同一个对象 → `([1, 2], [1, 2])`。正确写法是 `def f(a, acc=None): acc = [] if acc is None else acc`。"
            }
        ]
    },
    {
        "title": "*args 收到的是元组",
        "subject": "python",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "*args",
            "参数"
        ],
        "choices": [
            "(4, 5)",
            "(1, 3, 4, 5)",
            "(3, 4, 5)",
            "报错"
        ],
        "source_section": "第 08 讲 · 函数",
        "statement_md": "```python\ndef g(a, b=2, *args, **kw):\n    return args\n```\n`g(1, 3, 4, 5, x=6)` 返回什么？",
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
                "explanation": "位置参数先喂满普通形参：`a=1`、`b=3`，**剩下的** 4、5 才进 `*args`（元组）；`x=6` 进 `**kw`（字典）。所以 `args` 是 `(4, 5)`。注意 `b` 虽然带默认值 2，但有位置实参时照样被覆盖。"
            }
        ]
    },
    {
        "title": "函数内赋值会让变量变成局部变量",
        "subject": "python",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "作用域",
            "UnboundLocalError"
        ],
        "choices": [
            "返回 2",
            "返回 1",
            "UnboundLocalError",
            "NameError"
        ],
        "source_section": "第 08 讲 · 函数",
        "statement_md": "```python\nx = 1\ndef h():\n    x += 1\n    return x\n```\n调用 `h()` 会发生什么？",
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
                "explanation": "函数体里只要对 `x` **赋过值**（`x += 1` 就是赋值），`x` 在整个函数内就是局部变量，于是 `x += 1` 里的那个「读」找不到局部 `x` → `UnboundLocalError`。要改全局变量得先 `global x`；`NameError` 是另一个异常，别混。"
            }
        ]
    },
    {
        "title": "import 之后必须用限定名",
        "subject": "python",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "import",
            "命名空间"
        ],
        "choices": [
            "正常返回 4.0",
            "NameError",
            "AttributeError",
            "返回 2"
        ],
        "source_section": "第 09 讲 · 模块与包",
        "statement_md": "只写了 `import math`，然后直接调用 `sqrt(4)`，会怎样？",
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
                "explanation": "`import math` 只把**模块名** `math` 绑进当前命名空间，里面的 `sqrt` 没有进来，得写 `math.sqrt(4)`。要直接用名字就 `from math import sqrt`。`import math.sqrt` 这种写法才是错的（sqrt 不是子模块）。"
            }
        ]
    },
    {
        "title": "math.sqrt 返回浮点数",
        "subject": "python",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "math",
            "类型"
        ],
        "choices": [
            "4",
            "4.0",
            "2",
            "16"
        ],
        "source_section": "第 09 讲 · 模块与包",
        "statement_md": "`math.sqrt(16)` 的结果是什么？",
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
                "explanation": "`math.sqrt` 一律返回 `float`，完全平方数也是 `4.0` 不是 `4`。要整数开方可以用 `math.isqrt`（返回 int，且是真·整数运算）。"
            }
        ]
    },
    {
        "title": "bool 是 int 的子类",
        "subject": "python",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "bool",
            "继承"
        ],
        "choices": [
            "True",
            "False",
            "TypeError",
            "None"
        ],
        "source_section": "第 10 讲 · 面向对象（上）",
        "statement_md": "`isinstance(True, int)` 的结果是什么？",
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
                "explanation": "`bool` 是 `int` 的**子类**（`issubclass(bool, int)` 为 True），`True == 1`、`False == 0`，所以 `isinstance(True, int)` 为 True。副作用：`sum([True, True]) == 2`，以及 `{1: 'a'}[True]` 能取到 `'a'`。"
            }
        ]
    },
    {
        "title": "实例属性赋值不会改类属性",
        "subject": "python",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "类属性",
            "实例属性"
        ],
        "choices": [
            "0",
            "5",
            "None",
            "AttributeError"
        ],
        "source_section": "第 11 讲 · 面向对象（下）",
        "statement_md": "```python\nclass C:\n    n = 0\nc = C()\nc.n = 5\n```\n此时 `C.n` 是多少？",
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
                "explanation": "`c.n = 5` 是给**实例**新建一个属性，遮住（shadow）同名类属性，类本身没被改动，所以 `C.n` 还是 0。要改类属性必须写 `C.n = 5` 或用 `type(c).n = 5`。读到 5 的是 `c.n` —— 这是「属性查找先实例后类」的必然结果。"
            }
        ]
    },
    {
        "title": "w 模式打开就清空",
        "subject": "python",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "open",
            "文件模式"
        ],
        "choices": [
            "0",
            "3",
            "6",
            "报错"
        ],
        "source_section": "第 12 讲 · 文件",
        "statement_md": "先往文件写入 `abc`，再用 `open(p, 'w')` 打开并立刻关闭，文件大小是多少字节？",
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
                "explanation": "`'w'` 模式打开的那一刻文件就被**截断**（truncate）成 0 字节，不是「写的时候才清空」。所以只想追加要用 `'a'`，想读写又不想清空要用 `'r+'`。"
            }
        ]
    },
    {
        "title": "readlines 返回列表",
        "subject": "python",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "readlines",
            "文件"
        ],
        "choices": [
            "'list'",
            "'str'",
            "'generator'",
            "'tuple'"
        ],
        "source_section": "第 12 讲 · 文件",
        "statement_md": "`f.readlines()` 返回什么类型的对象？",
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
                "explanation": "`readlines()` 一次性把全文切成行，返回**列表**（每行带结尾的 `\\n`）；`read()` 返回整串，`readline()` 返回一行。文件很大时别用 `readlines`，直接 `for line in f` 才是流式的。"
            }
        ]
    },
    {
        "title": "哪些是不可变类型",
        "subject": "python",
        "line": "text",
        "question_type": "multiple_choice",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "不可变",
            "类型"
        ],
        "choices": [
            "int",
            "list",
            "tuple",
            "str"
        ],
        "source_section": "第 02 讲 · 编程基础",
        "statement_md": "下列哪些类型是**不可变**类型？\n\n**多选题**：正确选项不止一个，点选切换，再次点击可取消。",
        "input_format": "",
        "output_format": "若干个选项字母，按字母升序连写（如 `AC`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ACD",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ACD\n|ADC\n|CAD\n|CDA\n|DAC\n|DCA\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`int`、`str`、`tuple` 都是不可变对象：想「改」只能造新的 —— `x += 1` 看着像加一，其实是把 `x` 重新绑到一个新整数上（`id` 会变）。`list` 可以就地增删改，`id` 不变。★ 注意 `id` 这条只对 CPython 有意义（小整数还有缓存），但「不可变 → 运算产生新对象」这条语义是语言层面的。"
            }
        ]
    },
    {
        "title": "哪些操作会就地修改列表",
        "subject": "python",
        "line": "text",
        "question_type": "multiple_choice",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "list",
            "就地"
        ],
        "choices": [
            "append",
            "sort",
            "reverse",
            "sorted"
        ],
        "source_section": "第 05 讲 · 列表与元组",
        "statement_md": "下列哪些操作会**就地**修改列表本身？\n\n**多选题**：正确选项不止一个，点选切换，再次点击可取消。",
        "input_format": "",
        "output_format": "若干个选项字母，按字母升序连写（如 `AC`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ABC",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ABC\n|ACB\n|BAC\n|BCA\n|CAB\n|CBA\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`append` / `sort` / `reverse` 都是**就地**方法，返回 `None`，改的是原对象；`sorted()` 是内置函数，返回**新列表**、原列表不动。判别口诀：方法（`a.sort()`）就地，函数（`sorted(a)`）新建。"
            }
        ]
    },
    {
        "title": "关于 break / continue / for-else 的说法",
        "subject": "python",
        "line": "text",
        "question_type": "multiple_choice",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "break",
            "for-else"
        ],
        "choices": [
            "break 会结束整个循环",
            "continue 只跳过本轮剩余语句，进入下一轮",
            "for-else 的 else 在被 break 打断时不执行",
            "for-else 的 else 在循环体一次都没执行时也不执行"
        ],
        "source_section": "第 03 讲 · 流程控制语句",
        "statement_md": "关于 `break` / `continue` / `for-else`，下列哪些说法正确？\n\n**多选题**：正确选项不止一个，点选切换，再次点击可取消。",
        "input_format": "",
        "output_format": "若干个选项字母，按字母升序连写（如 `AC`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ABC",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ABC\n|ACB\n|BAC\n|BCA\n|CAB\n|CBA\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`break` 跳出**整个**循环；`continue` 只结束本轮；`for-else` 的 `else` 属于「循环正常结束」这条路径，被 break 打断就不执行。★ 最后一条是反直觉的地方：**循环体一次都没跑**（`range(0)`）也算正常结束，`else` 照样执行 —— 所以它天然适合写「找了一圈没找到」。"
            }
        ]
    },
    {
        "title": "下列哪些是 Python 内置异常",
        "subject": "python",
        "line": "text",
        "question_type": "multiple_choice",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "异常",
            "内置"
        ],
        "choices": [
            "ZeroDivisionError",
            "ValueError",
            "IndexError",
            "NullPointerError"
        ],
        "source_section": "第 13 讲 · 异常",
        "statement_md": "下列哪些是 Python 的**内置异常**？\n\n**多选题**：正确选项不止一个，点选切换，再次点击可取消。",
        "input_format": "",
        "output_format": "若干个选项字母，按字母升序连写（如 `AC`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ABC",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ABC\n|ACB\n|BAC\n|BCA\n|CAB\n|CBA\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "前三个都是内置异常。`NullPointerError` 是**Java** 的，Python 里没有——Python 对应的是 `AttributeError`（访问不存在的属性）和 `TypeError`（对 None 做操作，常见于忘了 `return`）。"
            }
        ]
    },
    {
        "title": "哪些能当字典的键",
        "subject": "python",
        "line": "text",
        "question_type": "multiple_choice",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "dict",
            "哈希"
        ],
        "choices": [
            "3",
            "'a'",
            "(1, 2)",
            "[1]"
        ],
        "source_section": "第 06 讲 · 字典与集合",
        "statement_md": "下列哪些值可以直接作为字典的键？\n\n**多选题**：正确选项不止一个，点选切换，再次点击可取消。",
        "input_format": "",
        "output_format": "若干个选项字母，按字母升序连写（如 `AC`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ABC",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ABC\n|ACB\n|BAC\n|BCA\n|CAB\n|CBA\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "字典/集合的键必须**可哈希**，而「可哈希」的实质是**不可变**：数字、字符串、元组都可以，列表/字典/集合不行（当场 `TypeError: unhashable type`）。元组能当键的前提是它**里面每一个元素也都可哈希**：`([1],)` 就不行。"
            }
        ]
    },
    {
        "title": "哪些写法会得到新对象",
        "subject": "python",
        "line": "text",
        "question_type": "multiple_choice",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "拷贝",
            "list"
        ],
        "choices": [
            "a.copy()",
            "sorted(a)",
            "a[:]",
            "a.append(1)"
        ],
        "source_section": "第 05 讲 · 列表与元组",
        "statement_md": "`a` 是个列表，下列哪些写法会得到一个**新列表**（而不是原地修改）？\n\n**多选题**：正确选项不止一个，点选切换，再次点击可取消。",
        "input_format": "",
        "output_format": "若干个选项字母，按字母升序连写（如 `AC`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ABC",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ABC\n|ACB\n|BAC\n|BCA\n|CAB\n|CBA\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`copy()`、`sorted()`、`[:]` 都造新列表（**浅**拷贝，内层还是同一批对象）；`append` 是就地方法、返回 `None`。★ 浅拷贝的坑：`b = a[:]` 之后 `b[0]` 若是列表，改它还是会串到 `a`。"
            }
        ]
    },
    {
        "title": "关于 *args 与 **kwargs 的说法",
        "subject": "python",
        "line": "text",
        "question_type": "multiple_choice",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "*args",
            "**kwargs"
        ],
        "choices": [
            "*args 收集多余的位置实参，是元组",
            "**kwargs 收集多余的关键字实参，是字典",
            "形参顺序里 *args 必须写在 **kwargs 前面",
            "调用时 f(*lst) 会把列表拆成若干个位置实参"
        ],
        "source_section": "第 08 讲 · 函数",
        "statement_md": "关于 `*args` 与 `**kwargs`，下列哪些说法正确？\n\n**多选题**：正确选项不止一个，点选切换，再次点击可取消。",
        "input_format": "",
        "output_format": "若干个选项字母，按字母升序连写（如 `AC`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ABCD",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ABCD\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "四条都对：`*args` 收成元组、`**kwargs` 收成字典，形参顺序必须是「普通参数 → `*args` → 有默认值的关键字参数 → `**kwargs`」；`f(*lst)` 是**拆包**，和定义处的 `*args` 是同一个符号的两种用法。"
            }
        ]
    },
    {
        "title": "用 with 打开文件的好处",
        "subject": "python",
        "line": "text",
        "question_type": "multiple_choice",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "with",
            "文件"
        ],
        "choices": [
            "离开代码块时自动关闭文件",
            "块内抛异常时也会关闭",
            "省去手写 try/finally",
            "会把整个文件读进内存"
        ],
        "source_section": "第 12 讲 · 文件",
        "statement_md": "用 `with open(...) as f:` 打开文件，下列哪些说法正确？\n\n**多选题**：正确选项不止一个，点选切换，再次点击可取消。",
        "input_format": "",
        "output_format": "若干个选项字母，按字母升序连写（如 `AC`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ABC",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ABC\n|ACB\n|BAC\n|BCA\n|CAB\n|CBA\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`with` 是上下文管理器语法：无论正常退出还是抛异常，`__exit__` 都会被调用，所以关文件、放锁、回滚事务都不会漏。它**不会**替你读文件内容——读不读、读多少，还是你自己写在块里的。"
            }
        ]
    },
    {
        "title": "关于文件模式的正确说法",
        "subject": "python",
        "line": "text",
        "question_type": "multiple_choice",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "文件模式",
            "open"
        ],
        "choices": [
            "'r' 只读，文件不存在直接报错",
            "'w' 清空已有内容或新建文件",
            "'a' 在文件末尾追加，不截断",
            "'r+' 打开时会清空文件"
        ],
        "source_section": "第 12 讲 · 文件",
        "statement_md": "关于 `open()` 的文件模式，下列哪些说法正确？\n\n**多选题**：正确选项不止一个，点选切换，再次点击可取消。",
        "input_format": "",
        "output_format": "若干个选项字母，按字母升序连写（如 `AC`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ABC",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ABC\n|ACB\n|BAC\n|BCA\n|CAB\n|CBA\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`'r'` 只读且要求文件存在；`'w'` 一打开就截断；`'a'` 追加不截断、文件不存在就新建。`'r+'` 是**读写**且**不清空**（指针在开头，写会覆盖前面的字节）——最后一条说它清空，是错的，这正是与 `'w+'` 的区别。"
            }
        ]
    },
    {
        "title": "关于魔术方法的说法",
        "subject": "python",
        "line": "text",
        "question_type": "multiple_choice",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "魔术方法",
            "OOP"
        ],
        "choices": [
            "__str__ 面向用户，print 时调用",
            "__repr__ 面向开发者，交互环境里显示",
            "super() 用来调用父类的方法",
            "__init__ 必须返回 self"
        ],
        "source_section": "第 11 讲 · 面向对象（下）",
        "statement_md": "关于 `__str__` / `__repr__` / `super()` / `__init__`，下列哪些说法正确？\n\n**多选题**：正确选项不止一个，点选切换，再次点击可取消。",
        "input_format": "",
        "output_format": "若干个选项字母，按字母升序连写（如 `AC`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ABC",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ABC\n|ACB\n|BAC\n|BCA\n|CAB\n|CBA\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`__str__` 给 `print`/`str()` 用，`__repr__` 给调试和交互环境用（没定义 `__str__` 时会退回 `__repr__`）；`super()` 沿 MRO 找父类方法。`__init__` **必须返回 None**，返回别的会 `TypeError` —— 它不是构造器，只负责初始化已创建好的实例。"
            }
        ]
    },
    {
        "title": "input() 的返回值总是字符串",
        "subject": "python",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 1,
        "total_score": 8,
        "tags": [
            "input"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 02 讲 · 编程基础",
        "statement_md": "`input()` 读进来的内容，类型总是 `str`。",
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
                "explanation": "`input()` 返回的**恒为字符串**，哪怕用户敲的是 `3`。要数字得自己 `int()`/`float()`。这也是 `input() + 1` 报 TypeError 的原因。"
            }
        ]
    },
    {
        "title": "int 能直接转换 '3.5'",
        "subject": "python",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 1,
        "total_score": 8,
        "tags": [
            "类型转换"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 02 讲 · 编程基础",
        "statement_md": "`int('3.5')` 能成功把字符串转成整数 3。",
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
                "explanation": "`int('3.5')` 抛 `ValueError` —— 它只认**整数字面量**。要转得先 `float('3.5')` 再 `int(...)`（这会截断成 3）。"
            }
        ]
    },
    {
        "title": "字符串是不可变的",
        "subject": "python",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 1,
        "total_score": 8,
        "tags": [
            "字符串",
            "不可变"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 04 讲 · 字符串",
        "statement_md": "`s = 'a'` 之后执行 `s[0] = 'b'` 会抛 TypeError。",
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
                "explanation": "字符串不可变，下标赋值当场 `TypeError`。要「改」只能切片拼新串（`s[:1] + 'b' + s[2:]`）或转成 `list` 改完再 `join`。"
            }
        ]
    },
    {
        "title": "b = a 不是复制列表",
        "subject": "python",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 1,
        "total_score": 8,
        "tags": [
            "引用",
            "list"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 05 讲 · 列表与元组",
        "statement_md": "`a = [1]` 之后 `b = a`，再 `b.append(2)`，`a` 也会变成 `[1, 2]`。",
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
                "explanation": "**对**。`b = a` 只复制了引用，两个名字指向同一列表。要真复制用`a.copy()`、`a[:]` 或 `list(a)`（都是浅拷贝）。`a == [1, 2]` 之所以为真，就是因为它们是一个对象。"
            }
        ]
    },
    {
        "title": "元组完全不可变",
        "subject": "python",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 1,
        "total_score": 8,
        "tags": [
            "元组",
            "陷阱"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 05 讲 · 列表与元组",
        "statement_md": "元组一旦创建，连它内部元素的内容都不会变。",
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
                "explanation": "**错**。元组只保证「自己这一层的**引用**不变」，元素若是可变对象，元素内容照样能改：`t = ([1],)`，`t[0].append(2)` 之后 `t` 变成 `([1, 2],)`，而 `t[0] = [9]` 才是不允许的。所谓「元组不可变」是浅层的。"
            }
        ]
    },
    {
        "title": "字典的键必须可哈希",
        "subject": "python",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 1,
        "total_score": 8,
        "tags": [
            "dict",
            "哈希"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 06 讲 · 字典与集合",
        "statement_md": "把列表当字典的键会抛 TypeError。",
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
                "explanation": "对。字典/集合靠哈希值定位，不可哈希的类型（list、dict、set）当键直接`TypeError: unhashable type: 'list'`。要按列表内容做键，先转成 `tuple`。"
            }
        ]
    },
    {
        "title": "集合支持下标访问",
        "subject": "python",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 1,
        "total_score": 8,
        "tags": [
            "set"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 06 讲 · 字典与集合",
        "statement_md": "`{10, 20}[0]` 能取到集合里的第一个元素。",
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
                "explanation": "错。集合**无序**，没有下标概念，`{10, 20}[0]` 抛 `TypeError: 'set' object is not subscriptable`。要取元素只能 `for x in s` / `next(iter(s))` / `list(s)[0]`（顺序不保证）。"
            }
        ]
    },
    {
        "title": "默认参数只求值一次",
        "subject": "python",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 1,
        "total_score": 8,
        "tags": [
            "默认参数",
            "陷阱"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 07 讲 · 函数",
        "statement_md": "函数写成 `def f(acc=[])`，多次调用会共用同一个默认列表。",
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
                "explanation": "对，这是 Python 最出名的坑之一。默认值在 `def` 执行时求值一次，之后挂在 `f.__defaults__` 上被所有调用共享。想每次新列表就写 `acc=None`，进函数再 `acc = [] if acc is None else acc`。"
            }
        ]
    },
    {
        "title": "Python 支持同名函数重载",
        "subject": "python",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 1,
        "total_score": 8,
        "tags": [
            "重载",
            "函数"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 08 讲 · 函数",
        "statement_md": "Python 里可以定义两个同名但参数个数不同的函数，调用时按参数自动选。",
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
                "explanation": "错。Python **没有重载**：后一个 `def f` 直接覆盖前一个，只剩两个参数那版，`f(1)` 于是 `TypeError`。要「多态」靠默认参数、`*args` 或 `functools.singledispatch`（按类型分派）。"
            }
        ]
    },
    {
        "title": "import 之后模块内的名字不自动可见",
        "subject": "python",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 1,
        "total_score": 8,
        "tags": [
            "import"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 09 讲 · 模块与包",
        "statement_md": "只写 `import math` 就能直接调用 `sqrt(4)`。",
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
                "explanation": "错。`import math` 只绑定了名字 `math`，得写 `math.sqrt(4)`；要用短名字就 `from math import sqrt`。`import` 不会把模块内容倒进当前命名空间。"
            }
        ]
    },
    {
        "title": "__init__ 可以返回值",
        "subject": "python",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 1,
        "total_score": 8,
        "tags": [
            "__init__",
            "OOP"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 10 讲 · 面向对象（上）",
        "statement_md": "定义 `def __init__(self): return 1` 之后，实例化对象能拿到 1。",
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
                "explanation": "错。`__init__` 只负责初始化已经创建好的实例，返回值必须是 `None`；返回别的会 `TypeError: __init__() should return None, not 'int'`。`A()` 拿到的永远是那个实例本身。"
            }
        ]
    },
    {
        "title": "with 退出时一定关闭文件",
        "subject": "python",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 1,
        "total_score": 8,
        "tags": [
            "with",
            "文件"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 12 讲 · 文件",
        "statement_md": "`with open(p) as f:` 代码块结束后 `f.closed` 为 True。",
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
                "explanation": "对。`with` 靠 `__exit__` 保证关闭，正常结束和抛异常都会走到，比手写 `try/finally` 更不容易漏。"
            }
        ]
    },
    {
        "title": "finally 在 return 时也会执行",
        "subject": "python",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 1,
        "total_score": 8,
        "tags": [
            "finally",
            "异常"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 13 讲 · 异常",
        "statement_md": "`try` 里 `return` 了，`finally` 块照样会跑。",
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
                "explanation": "对。`return` 只是**准备**返回值，真正的返回要等 `finally` 跑完。所以 `finally` 里写 `return` 会**顶掉** `try` 里的返回值 —— 这是另一个坑，别这么写。"
            }
        ]
    },
    {
        "title": "except Exception 能捕获所有异常",
        "subject": "python",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 1,
        "total_score": 8,
        "tags": [
            "Exception",
            "异常层级"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 13 讲 · 异常",
        "statement_md": "`except Exception:` 能捕获包括 KeyboardInterrupt 在内的所有异常。",
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
                "explanation": "错。`Exception` 只是绝大多数异常的基类，`KeyboardInterrupt`、`SystemExit`、`GeneratorExit` 派生自 `BaseException`，用 `except Exception` 抓不到。想全抓得 `except BaseException`（几乎不该这么做，会让 Ctrl-C 失效）。"
            }
        ]
    },
    {
        "title": "range 返回列表",
        "subject": "python",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 1,
        "total_score": 8,
        "tags": [
            "range"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 03 讲 · 流程控制语句",
        "statement_md": "`range(10)` 返回的是一个列表。",
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
                "explanation": "错。`range(10)` 返回 **range 对象**：惰性、占常数内存、可重复迭代。要列表得显式 `list(range(10))`。这也是 `range(10**9)` 不炸内存的原因。"
            }
        ]
    },
    {
        "title": "字典保持插入顺序",
        "subject": "python",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 1,
        "total_score": 8,
        "tags": [
            "dict",
            "顺序"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 06 讲 · 字典与集合",
        "statement_md": "Python 3.7 起，字典遍历顺序就是键的插入顺序。",
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
                "explanation": "对。3.7 起 CPython 把「保持插入顺序」写进了语言规范（3.6 是实现细节）。所以要「去重同时保序」可以用 `dict.fromkeys(seq)`。注意：删掉再插回来算新插入，顺序会跑到最后。"
            }
        ]
    },
    {
        "title": "浮点数相等比较的坑",
        "subject": "python",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "浮点数",
            "陷阱"
        ],
        "choices": [],
        "source_section": "第 02 讲 · 编程基础",
        "statement_md": "表达式 `0.1 + 0.2 == 0.3` 的值是什么？",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "False",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|False\n|错\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "二进制浮点数存不下 0.1、0.2，相加得 `0.30000000000000004`，与 `0.3` 不相等，所以是 `False`。比较浮点要用 `math.isclose(a, b)`。"
            }
        ]
    },
    {
        "title": "带步长的 range 有几个元素",
        "subject": "python",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "range"
        ],
        "choices": [],
        "source_section": "第 03 讲 · 流程控制语句",
        "statement_md": "`len(range(1, 10, 3))` 的值是多少？",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "3",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "取的数是 1、4、7（下一个 10 已到 stop，右开区间取不到），共 3 个。"
            }
        ]
    },
    {
        "title": "strip 去掉两端空白",
        "subject": "python",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "strip"
        ],
        "choices": [],
        "source_section": "第 04 讲 · 字符串",
        "statement_md": "`'  hi  '.strip()` 的结果是什么？（直接写结果）",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "hi",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|hi\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`strip()` 去掉**两端**的空白（空格、`\\t`、`\\n`），中间的不管。`lstrip`/`rstrip` 只管一边。"
            }
        ]
    },
    {
        "title": "join 把列表拼成字符串",
        "subject": "python",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "join"
        ],
        "choices": [],
        "source_section": "第 04 讲 · 字符串",
        "statement_md": "`'-'.join(['a', 'b'])` 的结果是什么？",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "a-b",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|a-b\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`'sep'.join(seq)` 用 sep 把**字符串序列**接起来。★ 序列里不能有数字，否则 `TypeError` —— 得先 `map(str, seq)`。"
            }
        ]
    },
    {
        "title": "整除的结果",
        "subject": "python",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "整除"
        ],
        "choices": [],
        "source_section": "第 02 讲 · 编程基础",
        "statement_md": "`10 // 4` 的值是多少？",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "2",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`//` 向下取整，`2.5` 取到 `2`；余数用 `10 % 4` 得 2。两个操作合起来满足 `10 == (10//4)*4 + 10%4`。"
            }
        ]
    },
    {
        "title": "空列表的布尔值",
        "subject": "python",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "布尔",
            "真值"
        ],
        "choices": [],
        "source_section": "第 03 讲 · 流程控制语句",
        "statement_md": "`bool([])` 的值是什么？",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "False",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|False\n|错\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "空容器（`[]`、`()`、`{}`、`''`、`set()`）、`0`、`None` 都是假值。所以 `if not lst:` 是「列表为空」的惯用写法。"
            }
        ]
    },
    {
        "title": "除法结果的类型名",
        "subject": "python",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "类型",
            "除法"
        ],
        "choices": [],
        "source_section": "第 02 讲 · 编程基础",
        "statement_md": "`type(3 / 2).__name__` 的结果是什么？",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "float",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|float\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**单个** `/` 永远是真除法，结果一定是 `float`（`3/2` 是 `1.5`，`4/2` 是 `2.0`）。Python 3 里没有「整数除法得整数」这回事，那是 `//`。"
            }
        ]
    },
    {
        "title": "字典键的数量",
        "subject": "python",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "dict",
            "keys"
        ],
        "choices": [],
        "source_section": "第 06 讲 · 字典与集合",
        "statement_md": "`len({'a': 1, 'b': 2}.keys())` 的值是多少？",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "2",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "两个键就是两个，`keys()` 返回的是**视图对象**（跟着字典变），不是快照，`len` 直接能用。"
            }
        ]
    },
    {
        "title": "upper 转大写",
        "subject": "python",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "upper"
        ],
        "choices": [],
        "source_section": "第 04 讲 · 字符串",
        "statement_md": "`'abc'.upper()` 的结果是什么？",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ABC",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ABC\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`upper()` 返回**新串**，原串不动（字符串不可变）。中文和数字不受影响。大小写不敏感的比较常用 `s.lower() == t.lower()` 或 `casefold()`。"
            }
        ]
    },
    {
        "title": "除零抛什么异常",
        "subject": "python",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "异常",
            "除零"
        ],
        "choices": [],
        "source_section": "第 13 讲 · 异常",
        "statement_md": "`1 / 0` 抛出的异常类名是什么？",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ZeroDivisionError",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ZeroDivisionError\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`ZeroDivisionError`，它是 `ArithmeticError` 的子类。整数除零和浮点除零都抛它（不像 C 会得到 inf/nan）。"
            }
        ]
    },
    {
        "title": "reverse 排序后取第一个",
        "subject": "python",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "sorted"
        ],
        "choices": [],
        "source_section": "第 05 讲 · 列表与元组",
        "statement_md": "`sorted([3, 1, 2], reverse=True)[0]` 的值是多少？",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "3",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`reverse=True` 是降序，排序结果 `[3, 2, 1]`，取第一个是 3。等价写法 `sorted(a)[-1]`，但 `reverse=True` 意图更清楚。"
            }
        ]
    },
    {
        "title": "集合去重后的元素个数",
        "subject": "python",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "set",
            "去重"
        ],
        "choices": [],
        "source_section": "第 06 讲 · 字典与集合",
        "statement_md": "`len(set('banana'))` 的值是多少？",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "3",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`'banana'` 里的字符是 b、a、n、a、n、a，去重后只剩 `{b, a, n}` 三个，所以是 **3**。注意 `len` 数的是**不同元素**的个数，不是原串长度 6。"
            }
        ]
    },
    {
        "title": "列表与元组有什么区别",
        "subject": "python",
        "line": "text",
        "question_type": "short_answer",
        "difficulty": 3,
        "total_score": 12,
        "tags": [
            "list",
            "tuple",
            "简答"
        ],
        "choices": [],
        "source_section": "第 05 讲 · 列表与元组",
        "statement_md": "**简答题**：说出列表（`list`）和元组（`tuple`）的三点区别。\n\n按这个顺序答：可变性 → 语法 → 使用场景。\n\n三句话，每句一个区别即可。",
        "input_format": "",
        "output_format": "一句话作答（不要写解释、不要抄题目）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "列表可变，元组不可变；列表用方括号，元组用圆括号；列表适合存会变的数据，元组适合存固定记录",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|列表可变，元组不可变；列表用方括号，元组用圆括号；列表适合存会变的数据，元组适合存固定记录\n|列表可变元组不可变；列表用[]元组用()；列表用于增删改元组用于固定数据\n|list可变tuple不可变；list用方括号tuple用圆括号；list存可变序列tuple存常量集合\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "1. **可变性**：`list` 能就地增删改（`append`/`pop`/`a[0]=1`）；`tuple` 创建后不能改，下标赋值抛 `TypeError`。\n2. **语法**：`[]` 与 `()`；单元素元组必须写 `(1,)`。\n3. **场景**：列表存「同类、数量会变」的序列（一堆学生）；元组存「字段固定、意义各不同」的记录（坐标 `(x, y)`、函数返回多值），而且因为不可变，能当字典的键、能进集合。\n补充：元组的 `tuple` 对象更省内存、创建更快。"
            }
        ]
    },
    {
        "title": "简述 *args 与 **kwargs 的作用",
        "subject": "python",
        "line": "text",
        "question_type": "short_answer",
        "difficulty": 3,
        "total_score": 12,
        "tags": [
            "*args",
            "**kwargs",
            "简答"
        ],
        "choices": [],
        "source_section": "第 08 讲 · 函数",
        "statement_md": "**简答题**：`*args` 和 `**kwargs` 分别收集什么？各自是什么类型？\n\n两句话：一个元组、一个字典。",
        "input_format": "",
        "output_format": "一句话作答（不要写解释、不要抄题目）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "*args收集多余的位置参数，是元组；**kwargs收集多余的关键字参数，是字典",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|*args收集多余的位置参数，是元组；**kwargs收集多余的关键字参数，是字典\n|*args收集位置实参得到元组，**kwargs收集关键字实参得到字典\n|args收集多余位置参数为元组，kwargs收集多余关键字参数为字典\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`*args` 把「多出来的位置实参」收成一个**元组**；`**kwargs` 把「多出来的关键字实参」收成一个**字典**。\n形参顺序固定：普通参数 → `*args` → 有默认值的关键字参数 → `**kwargs`。\n反过来的**拆包**写法：`f(*lst)` 把列表拆成若干位置实参，`f(**d)` 把字典拆成若干关键字实参 —— 同名符号两用。"
            }
        ]
    },
    {
        "title": "__str__ 与 __repr__ 的区别",
        "subject": "python",
        "line": "text",
        "question_type": "short_answer",
        "difficulty": 3,
        "total_score": 12,
        "tags": [
            "魔术方法",
            "简答"
        ],
        "choices": [],
        "source_section": "第 11 讲 · 面向对象（下）",
        "statement_md": "**简答题**：`__str__` 和 `__repr__` 分别给谁看？`print(obj)` 走哪个？\n\n一句话说清「给谁看」，再点出 print 走哪个。",
        "input_format": "",
        "output_format": "一句话作答（不要写解释、不要抄题目）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "__str__面向用户可读，__repr__面向开发者调试，print走__str__",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|__str__面向用户可读，__repr__面向开发者调试，print走__str__\n|str给用户看repr给开发者看，print调用__str__\n|__str__给人看__repr__给开发调试看，print用__str__\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`__str__` 面向**最终用户**，要可读，`print()`、`str()`、`f'{obj}'` 调它；`__repr__` 面向**开发者**，理想形态是「能重建该对象的表达式」（如 `Point(1, 2)`），交互环境直接回车、`repr()`、容器打印时用它。\n没定义 `__str__` 时，`print` 会退回 `__repr__`；反之则不成立。所以两个都写时，`__repr__` 是兜底的那个。"
            }
        ]
    },
    {
        "title": "浅拷贝与深拷贝的区别",
        "subject": "python",
        "line": "text",
        "question_type": "short_answer",
        "difficulty": 3,
        "total_score": 12,
        "tags": [
            "拷贝",
            "简答"
        ],
        "choices": [],
        "source_section": "第 05 讲 · 列表与元组",
        "statement_md": "**简答题**：浅拷贝（`copy.copy` / `list.copy` / `a[:]`）与深拷贝（`copy.deepcopy`）的区别是什么？\n\n重点说「内层对象」是共享还是各一份。",
        "input_format": "",
        "output_format": "一句话作答（不要写解释、不要抄题目）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "浅拷贝只复制最外层，内层对象仍是同一份；深拷贝递归复制所有层，互不影响",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|浅拷贝只复制最外层，内层对象仍是同一份；深拷贝递归复制所有层，互不影响\n|浅拷贝复制外层引用共享内层，深拷贝递归复制全部，改内层不影响原对象\n|浅拷贝只复制第一层，深拷贝把所有嵌套对象都复制一份\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "浅拷贝只造一个新的**外层容器**，里面的元素还是原来那些对象的引用；深拷贝会**递归**复制每一层，得到一棵完全独立的树。\n实证：`a = [[1], [2]]`，`b = a.copy()` 之后 `b[0].append(9)`，`a` 也变成 `[[1, 9], [2]]` —— 因为 `a[0]` 和 `b[0]` 是同一个列表。换成 `b = copy.deepcopy(a)` 就不会串。\n对只含不可变元素（数字、字符串、元组）的列表，两者结果一模一样，深拷贝只是白花时间。"
            }
        ]
    }
]
