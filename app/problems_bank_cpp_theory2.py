"""C++ 基础线理论题库（第 07 ~ 12 讲）—— **自动生成，不要手改**。

本文件由 `tools/gen_cpp_theory2.py` 产出，重新生成：

    python tools/gen_cpp_theory2.py

题源
----
《C++语言程序设计》第 07 ~ 12 讲（类的继承 / 多态性 / 模板与群体数据 /
泛型程序设计与 STL / 流类库与输入输出 / 异常处理），按讲分节，
与同节的编程题并列。全部是**理论题**（`line = "text"`），
提交答案文本由 `oneof` checker 比对，不启子进程。

答案可信度
----------
「这段代码输出什么」「构造/析构顺序」「sizeof」「文件字节数」这类答案，
全部由生成器调用 `tools/cpp_eval.py::run_cpp()` **真编译真运行**取得，
再由输出反推选项字母 —— 不是手写的；跑不出预期就生成不出这个文件。
纯概念题在生成器里标了「无计算」，口径以讲义为准。
"""
from __future__ import annotations

CPP_THEORY2_PROBLEMS: list[dict] = [
    {
        "title": "公有继承下 protected 成员的访问属性",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "继承",
            "访问控制"
        ],
        "choices": [
            "类内不可访问，类外不可访问",
            "类内不可访问，类外可访问",
            "类内可访问，类外不可访问",
            "类内可访问，类外也可访问"
        ],
        "source_section": "第 07 讲 · 类的继承",
        "statement_md": "类 `Base` 有一个 protected 成员 `pro`，`class Derived : public Base`。在 `Derived` 的成员函数里访问 `pro`，以及用 `Derived` 对象 `d` 在类外写 `d.pro`，分别是哪种结果？",
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
                "explanation": "public 继承是**原样映射**：基类 public 仍是 public、protected 仍是 protected、private 一律不可见。protected 是「家族专用通道」—— 派生类成员函数能用它，但类外的对象不能。\n选「类外也可访问」是把 protected 当成了 public；选「类内不可访问」是把 protected 当成了 private —— 只有基类的 private 才是派生类成员函数也碰不到。"
            }
        ]
    },
    {
        "title": "派生类能否直接访问基类私有成员",
        "subject": "cpp",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 1,
        "total_score": 8,
        "tags": [
            "继承",
            "private"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 07 讲 · 类的继承",
        "statement_md": "派生类的成员函数可以直接访问基类的 private 成员 —— 因为继承会把基类成员复制一份到派生类对象里。",
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
                "explanation": "错。private 的可见域只有基类自己（和它的友元），**任何继承方式都改变不了这一点**。派生类对象里确实有基类私有成员的那块内存、基类自己的成员函数也确实在对它操作，但派生类的代码不能点名访问它（实测编译错 `is private within this context`）。\n想碰它只有两条路：基类提供的 public/protected 接口，或者友元。"
            }
        ]
    },
    {
        "title": "三级继承加成员对象的构造析构顺序",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "构造顺序",
            "析构顺序",
            "成员对象"
        ],
        "choices": [
            "ABMCcbma",
            "AMBCcbma",
            "AMBCAMBC",
            "MABCcbam"
        ],
        "source_section": "第 07 讲 · 类的继承",
        "statement_md": "下面程序的输出是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nstruct Tracer {\n    const char* n;\n    Tracer(const char* s = \"t\") : n(s) { cout << \"M\"; }\n    ~Tracer() { cout << \"m\"; }\n};\nstruct A { A() { cout << \"A\"; } ~A() { cout << \"a\"; } };\nstruct B : A {\n    Tracer t;\n    B() : t(\"t\") { cout << \"B\"; }\n    ~B() { cout << \"b\"; }\n};\nstruct C : B { C() { cout << \"C\"; } ~C() { cout << \"c\"; } };\n\nint main() { { C c; } cout << \"\\n\"; }\n```\n\n说明：`A` 打 `A`/`a`，成员对象 `Tracer` 打 `M`/`m`，`B`、`C` 分别打 `B`/`b`、`C`/`c`（大写为构造，小写为析构）。",
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
                "explanation": "构造自顶向下：**基类 → 成员对象 → 自身函数体**，所以是 A（基类）→ M（成员 t）→ B → C；析构严格相反：c → b → m → a。\n★ `B() : t(\"t\")` 只是把参数递给成员，不改变顺序 —— 基类永远最先。\n「AMBCAMBC」把析构写成了与构造同序；「MABCcbam」以为成员对象先于基类构造；「ABMCcbma」以为成员对象要等到构造函数体之后才构造。"
            }
        ]
    },
    {
        "title": "基类对象承接派生类对象的现象",
        "subject": "cpp",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "类型兼容",
            "对象切片"
        ],
        "choices": [],
        "source_section": "第 07 讲 · 类的继承",
        "statement_md": "已知 `Derived d;`，写 `Base b = d;` 时只拷贝了 `d` 的基类子对象，派生类特有的成员被丢弃 —— 这个现象的术语叫什么？（四个字的全称或两个字的简称都算）\n\n提示：英文叫 object slicing。",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "对象切片",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|对象切片\n|切片\n|对象切割\n|切割\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "这叫**对象切片**（object slicing）。对象赋值只按 `Base` 的大小拷内存，派生类多出来的那部分装不进去，被「切掉」了。\n★ 这也是「要用多态就只能走指针/引用」的根本原因：指针/引用不拷贝对象，不会切片；而赋值一定切片，切片之后连 vptr 都换成了基类表的，多态彻底没了。"
            }
        ]
    },
    {
        "title": "作用域分辨符穿透同名遮蔽",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "同名遮蔽",
            "作用域分辨符"
        ],
        "choices": [
            "1 1",
            "100 1",
            "1 100",
            "100 100"
        ],
        "source_section": "第 07 讲 · 类的继承",
        "statement_md": "下面程序的输出是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nstruct Base { int v = 1; };\nstruct Derived : Base { int v = 100; };\n\nint main() { Derived d; cout << d.v << \" \" << d.Base::v << \"\\n\"; }\n```",
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
                "explanation": "派生类声明同名成员 `v` 后，基类的 `v` 被**整体遮蔽**，所以 `d.v` 取到 100；`d.Base::v` 用 `::` 作用域分辨符指名走基类那一条，取到 1。\n「1 100」把两者的遮蔽关系弄反了；「100 100」以为 `Base::` 只是换个写法、仍取派生类那份；「1 1」则完全忽略了遮蔽。\n★ 遮蔽是按**名字**生效的，不按签名：基类若有 `f()` 和 `f(int)` 两个重载，派生类只写一个同名的 `f(double)`，基类那两个版本就全都不可见了。"
            }
        ]
    },
    {
        "title": "保护继承下基类 public 成员降为哪一级",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "继承",
            "访问控制",
            "protected继承"
        ],
        "choices": [
            "编译错：pub 在 D 中已降为 protected，类外不可访问",
            "编译通过：public 成员在任何继承方式下都保持 public",
            "编译错：pub 在 D 中已降为 private，D 的成员函数也不能再用",
            "编译通过：protected 继承只改变 protected 成员，不影响 public"
        ],
        "source_section": "第 07 讲 · 类的继承",
        "statement_md": "`class Base { protected: int pro; public: int pub; };`，现在写 `class D : protected Base { };`。在 `D` 的成员函数里访问 `pub` 是合法的；那么在类外用 `D` 的对象 `d` 写 `d.pub` 会怎样？",
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
                "explanation": "三种继承方式是**一张映射表**：\npublic 继承 → 原样（public 仍 public、protected 仍 protected）；\nprotected 继承 → 基类 public 与 protected **都变 protected**；\nprivate 继承 → 两者**都变 private**。\n基类 private 在三列里一律「不可见」，继承方式改不了它。\n所以 `d.pub` 在类外访问：public 继承能过，protected/private 继承全编译错。\n「D 的成员函数也不能再用」是把它当成了 private —— protected 继承下类内照样能用；「只影响 protected 成员」正好把映射表记反了。"
            }
        ]
    },
    {
        "title": "基类无默认构造时派生类不写初始化列表",
        "subject": "cpp",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 2,
        "total_score": 8,
        "tags": [
            "构造函数",
            "初始化列表",
            "继承"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 07 讲 · 类的继承",
        "statement_md": "基类只定义了 `Base(int)`（没有默认构造函数）。派生类 `D` 的构造函数初始化列表里什么都不写，仍能编译通过 —— 因为编译器会替 `D` 自动调用 `Base(int)` 并传 0。",
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
                "explanation": "错，这条是**编译错**（实测 `no matching function for call to 'Base::Base()'`）。\n**基类构造函数不会被继承**：`Base` 定义了 `Base(int)` 之后，编译器就不再为它生成默认构造，而派生类构造对象时必须先构造基类子对象 —— 于是 `D::D()` 找不到可调的基类构造。\n两条修法：① 初始化列表显式递参数 `D() : Base(0) { }`；② C++11 写 `using Base::Base;` 把基类的构造函数「继承」下来。\n★ 编译器不会替你猜参数，更不会自动补 0 —— 这一点和「成员对象没有默认构造」是同一个道理。"
            }
        ]
    },
    {
        "title": "类型兼容规则的反向赋值能不能成立",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "类型兼容",
            "向上转型"
        ],
        "choices": [
            "Derived d2 = b;",
            "Base b2 = d;",
            "Base& r = d;",
            "Base* p = &d;"
        ],
        "source_section": "第 07 讲 · 类的继承",
        "statement_md": "`Derived` 公有继承 `Base`，`Derived d;`、`Base b;` 都已定义。下列四条语句中，**编译不通过**的是：",
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
                "explanation": "类型兼容是**单向**的：公有派生类对象可以出现在任何需要基类对象的地方，三条通道（赋值 / 引用绑定 / 指针指向）都合法；反向一律编译错。\n`Base b2 = d;` 合法但会**切片**（只拷基类子对象）；`Base& r = d;` 与 `Base* p = &d;` 不切片，是第 8 讲多态的两条正道。\n`Derived d2 = b;` 错在「基类对象不一定真的是派生类」—— 基类里根本没有派生类那些成员，拷不过去。真要下行，必须显式 `static_cast<Derived&>(b)`（且要求实际对象确实是 Derived），或多态场景用 `dynamic_cast` 并在失败时拿到空指针。"
            }
        ]
    },
    {
        "title": "类型兼容后经引用调用同名函数",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "类型兼容",
            "静态绑定"
        ],
        "choices": [
            "Derived/Base/Derived",
            "Base/Base/Base",
            "Derived/Derived/Derived",
            "Base/Base/Derived"
        ],
        "source_section": "第 07 讲 · 类的继承",
        "statement_md": "下面程序的输出是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nstruct Base { void show() { cout << \"Base\"; } };\nstruct Derived : Base { void show() { cout << \"Derived\"; } };\n\nint main() {\n    Derived d;\n    Base& r = d;\n    Base b = d;\n    r.show(); cout << \"/\";\n    b.show(); cout << \"/\";\n    d.show(); cout << \"\\n\";\n}\n```",
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
                "explanation": "`show` **不是虚函数**，经引用/指针调用时按**声明类型**静态绑定：`r` 的声明类型是 `Base&`，所以调 `Base::show`；`b` 是切片后的 `Base` 对象，当然也是 `Base::show`；只有直接对象 `d.show()` 才在编译期定到 `Derived::show`。\n「Derived/Base/Derived」以为引用会自动按实际类型绑定 —— 那是加了 `virtual` 之后的事；「Base/Base/Base」以为对象直接调用也按声明类型；「Derived/Derived/Derived」同时错了两处。"
            }
        ]
    },
    {
        "title": "关于继承访问控制与类型兼容的正确说法",
        "subject": "cpp",
        "line": "text",
        "question_type": "multiple_choice",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "继承",
            "类型兼容",
            "多选"
        ],
        "choices": [
            "基类的 private 成员在派生类中变成 protected",
            "公有继承时基类的 protected 成员在派生类中仍是 protected",
            "私有继承时基类的 public 成员在派生类中变成 private",
            "派生类对象可以赋给基类对象，反过来不行"
        ],
        "source_section": "第 07 讲 · 类的继承",
        "statement_md": "关于继承的访问控制与类型兼容规则，下列说法**正确**的有：\n\n**多选题**：正确选项不止一个，点选切换，再次点击可取消。",
        "input_format": "",
        "output_format": "若干个选项字母，按字母升序连写（如 `AC`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "BCD",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|BCD\n|BDC\n|CBD\n|CDB\n|DBC\n|DCB\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "四条里只有「基类的 private 成员在派生类中变成 protected」是错的 —— **任何继承方式都动不了 private 的可见性**，它既不会变成 protected，也不会「消失」，只是派生类代码不能直接点名。\n其余三条都对：public 继承原样映射；private 继承把 public/protected 全降为 private，而且孙辈连这些都看不见（继承链「断代」）；类型兼容只允许派生类 → 基类的赋值/引用/指针三条通道，反向全部编译错。"
            }
        ]
    },
    {
        "title": "非虚继承的菱形里基类构造几次",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "菱形继承",
            "二义性"
        ],
        "choices": [
            "3",
            "0",
            "2",
            "1"
        ],
        "source_section": "第 07 讲 · 类的继承",
        "statement_md": "下面程序输出 `A` 的构造函数被调用的次数：\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nstruct A { static int cnt; A() { cnt++; } };\nint A::cnt = 0;\nstruct B : A {};\nstruct C : A {};\nstruct D : B, C {};\n\nint main() { D d; cout << A::cnt << \"\\n\"; }\n```",
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
                "explanation": "`B`、`C` 都是**非虚**继承 `A`，`D` 里就有**两份** `A` 子对象，构造 `D` 时每段各构造一次 → 2。\n也正因为有两份副本，`D` 里直接写 `x`（假设 A 有成员 x）会报 `is ambiguous`，编译器拒绝替你选路；要修复就把 B、C 改成 `virtual public A`，那样只留一份、只构造一次。\n「1」是以为编译器会自动合并重复基类；「3」「0」无依据。"
            }
        ]
    },
    {
        "title": "成员对象按声明顺序而非列表顺序构造",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "构造顺序",
            "成员对象",
            "初始化列表"
        ],
        "choices": [
            "[y][x]<B>{D}{/D}</B>(x)(y)",
            "<B>[x][y]{D}{/D}(x)(y)</B>",
            "<B>[y][x]{D}{/D}(x)(y)</B>",
            "<B>[x][y]{D}{/D}(y)(x)</B>"
        ],
        "source_section": "第 07 讲 · 类的继承",
        "statement_md": "`D` 里成员对象声明顺序是 `y` 在前、`x` 在后，而初始化列表写的是 `x(\"x\"), y(\"y\")`。下面程序的输出是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nstruct T {\n    const char* n;\n    T(const char* s) : n(s) { cout << \"[\" << n << \"]\"; }\n    ~T() { cout << \"(\" << n << \")\"; }\n};\nstruct B { B() { cout << \"<B>\"; } ~B() { cout << \"</B>\"; } };\n\nstruct D : B {\n    T y;                                  // 声明在前\n    T x;\n    D() : B(), x(\"x\"), y(\"y\") { cout << \"{D}\"; }   // 列表里 x 写在 y 前面\n    ~D() { cout << \"{/D}\"; }\n};\n\nint main() { { D d; } cout << \"\\n\"; }\n```\n\n说明：`T` 构造打 `[名]`、析构打 `(名)`；`B` 前后打 `<B>`/`</B>`；`D` 打 `{D}`/`{/D}`。",
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
                "explanation": "构造顺序由**声明顺序**决定，初始化列表只是参数递送清单：\n基类 `B` → 成员 `y` → 成员 `x` → `D` 的函数体，所以是 `<B>[y][x]{D}`；析构严格相反：`{/D}` → 成员逆序 `(x)(y)` → `</B>`。\n「[x][y]…(y)(x)」正是**把初始化列表当成了顺序说明书** —— 这是本讲最容易踩的一条；「[y][x]<B>」把成员对象排到了基类前面。\n★ 为什么按声明顺序：对象的内存布局是按声明排的，构造也必须按内存布局来；如果允许列表顺序生效，同一个类在不同构造函数里就会有不同的成员构造次序。\n★ 实践建议：初始化列表的书写顺序**与声明顺序保持一致**，纯为了读代码的人不误判。"
            }
        ]
    },
    {
        "title": "私有继承两代之后还能不能看见基类成员",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "继承",
            "private继承",
            "断代"
        ],
        "choices": [
            "编译通过：pub 在 C 中降为 protected",
            "编译错：因为 A 的 private 成员在 C 中不可见",
            "编译错：pub 在 B 中已降为 private，C 看不见",
            "编译通过：C 是 public 继承 B，pub 在 C 中恢复为 public"
        ],
        "source_section": "第 07 讲 · 类的继承",
        "statement_md": "`class B : private A { };`（`A` 有 public 成员 `pub`），再写 `class C : public B { };`。在 `C` 的成员函数里访问 `pub`，结果是什么？",
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
                "explanation": "private 继承把基类的 public/protected **全部降为 private**，而且是**一次性、不可逆**的：`C` 再从 `B` 公有继承，也拿不到 `pub` —— 继承链在这里「断代」。\n三种视角分开看：`B` 自己的成员函数能访问 `pub`（它在 B 里是 private，B 内部可见）；`C` 的成员函数不能；`C`/`B` 的对象在类外也不能。\n「恢复为 public」是无稽之谈 —— 继承只能降级不能升级；「降为 protected」是把 private 与 protected 继承搞混；「因为 A 的 private 成员不可见」这个理由也错（`pub` 是 public，与 A 的 private 成员无关）。\n★ 结论：业务代码一律 public 继承。private 继承语义上接近「组合」，现代写法更推荐直接放成员对象。"
            }
        ]
    },
    {
        "title": "虚基类菱形里两条路径看到的是同一份数据",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "虚基类",
            "菱形继承",
            "共享子对象"
        ],
        "choices": [
            "7 7",
            "7 0",
            "0 7",
            "编译错误：x 是 ambiguous"
        ],
        "source_section": "第 07 讲 · 类的继承",
        "statement_md": "`B`、`C` 都 `virtual` 继承 `A`，`D` 公有继承 `B` 和 `C`。先经 `B` 的路把 `x` 改成 7，再分别经两条路读它。输出是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nstruct A { int x = 0; };\nstruct B : virtual A { void setB(int v) { x = v; } int getB() const { return x; } };\nstruct C : virtual A { int getC() const { return x; } };\nstruct D : B, C {};\n\nint main() { D d; d.setB(7); cout << d.getB() << \" \" << d.getC() << \"\\n\"; }\n```",
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
                "explanation": "`virtual` 继承让 `D` 里只保留**一份** `A` 子对象，`B` 路与 `C` 路访问的是同一块内存，所以经 B 写 7、经 C 也读到 7 → `7 7`。\n「7 0」是**非虚**菱形继承的结果：那时 D 里有两份独立的 A 副本，各改各的；「0 7」把两条路对调；「ambiguous」是**非虚**菱形下直接写 `d.x` 的报错（编译器拒绝替你选路，只能用 `d.B::x` 指名）。\n★ 一句话：非虚菱形 = 两份副本 + 访问二义；虚继承 = 一份共享 + 构造归最远派生类。"
            }
        ]
    },
    {
        "title": "派生类用 using 声明恢复基类重载",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "同名遮蔽",
            "using声明",
            "重载"
        ],
        "choices": [
            "什么也不用写，派生类的 f 会自动与基类的两个重载合并",
            "把 Derived 的 f 改名为 f2，避免同名",
            "在 Derived 里写 using Base::f;",
            "在 Derived 里只写一句声明 void f(int);（不写实现）"
        ],
        "source_section": "第 07 讲 · 类的继承",
        "statement_md": "`Base` 里有 `void f()` 和 `void f(int)` 两个重载；`Derived` 里只写了 `void f(double)`。此时在 `Derived` 的成员函数里写 `f(1)`，想让它调到基类的 `f(int)`，正确做法是：",
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
                "explanation": "遮蔽是**按名字**生效的：派生类一旦声明了任何同名成员，基类的**所有**同名重载就整体不可见。写 `using Base::f;` 把基类的名字引进派生类作用域，此后 `f()`、`f(int)` 与派生自己的 `f(double)` 一起参与重载解析。\n★ 注意不写 using 时 `f(1)` **不是编译错**：int 实参只能匹配派生类的 `f(double)`（int→double 是标准转换），于是「本该走整数版」的调用悄悄跑到浮点版去了 —— 静默错，比报错更危险。\n「只写声明不写实现」能过编译但一调用就链接错（undefined reference）；「自动合并」是把 C++ 的作用域规则当成了 Java 的继承；改名则丢掉了「同名同义」的表达力。"
            }
        ]
    },
    {
        "title": "虚基类的构造实参由哪一层决定",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "虚基类",
            "最远派生类"
        ],
        "choices": [
            "A20",
            "A30",
            "A5A20",
            "A5"
        ],
        "source_section": "第 07 讲 · 类的继承",
        "statement_md": "下面程序的输出是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nstruct A { A(int v) { cout << \"A\" << v; } };\nstruct B : virtual A { B() : A(20) {} };\nstruct C : virtual A { C() : A(30) {} };\nstruct D : B, C { D() : A(5), B(), C() {} };\n\nint main() { D d; cout << \"\\n\"; }\n```",
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
                "explanation": "虚基类 `A` 由**最远派生类 `D`** 负责构造，`B` 里写的 `A(20)`、`C` 里写的 `A(30)` **全部被忽略**（它们只管自己那一层，虚基类不归它们管），所以只输出一次 `A5`。\n「A20」「A30」是以为中间类写的实参生效 —— 这正是最常错的地方；「A5A20」是以为会构造多次，而虚继承的意义恰恰是只留一份、只构造一次。\n★ 顺带记住顺序：**虚基类永远最先构造**，与它写在初始化列表的第几位无关。"
            }
        ]
    },
    {
        "title": "虚基类构造的归属与顺序",
        "subject": "cpp",
        "line": "text",
        "question_type": "short_answer",
        "difficulty": 4,
        "total_score": 12,
        "tags": [
            "虚基类",
            "最远派生类",
            "简答"
        ],
        "choices": [],
        "source_section": "第 07 讲 · 类的继承",
        "statement_md": "**简答题**：菱形继承中 `B`、`C` 都 `virtual` 继承 `A`，`D` 公有继承 `B` 和 `C`。若 `B` 的初始化列表写 `A(20)`、`C` 写 `A(30)`、`D` 写 `A(5)`，最终负责构造 `A` 的是哪个类？`B`、`C` 写的实参是否生效？",
        "input_format": "",
        "output_format": "一句话作答（不要抄题目、不要写代码）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "由最远派生类 D 负责构造 A，B、C 写的实参被忽略，A 只构造一次",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|由最远派生类 D 负责构造 A，B、C 写的实参被忽略，A 只构造一次\n|最远派生类 D 构造虚基类 A，中间类 B、C 的初始化列表对 A 不起作用\n|D 负责构造，B 和 C 写的 A(20)、A(30) 都被忽略，最终用的是 A(5)\n|最远派生类负责，中间类写的被忽略\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "虚基类的构造**归最远派生类管**：`D` 的初始化列表里那句 `A(5)` 才生效，`B::B()` 里写的 `A(20)`、`C::C()` 里写的 `A(30)` 在构造 `D` 对象时被直接忽略（只有单独构造一个 `B` 对象时它们才起作用）。\n所以 `A` 只构造一次、参数是 5；而且它**永远最先构造**，排在其他基类和成员对象之前，与它在初始化列表里写第几位无关。\n为什么这么规定：虚基类只有一份，如果允许两层各传一个参数，编译器没法决定听谁的 ——于是把决定权交给唯一知道完整对象的那一层，也就是最远派生类。"
            }
        ]
    },
    {
        "title": "虚基类排在非虚基类之后的构造顺序",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "虚基类",
            "构造顺序",
            "初始化列表"
        ],
        "choices": [
            "VNBDV",
            "VNBD",
            "NVBD",
            "NBVD"
        ],
        "source_section": "第 07 讲 · 类的继承",
        "statement_md": "`B` 虚继承 `V`；`D` 的基类列表写的是 `D : N, B`，初始化列表又写成 `B(), N()`。下面程序输出四个字母，顺序是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nstruct V { V() { cout << \"V\"; } };\nstruct N { N() { cout << \"N\"; } };\nstruct B : virtual V { B() { cout << \"B\"; } };\nstruct D : N, B { D() : B(), N() { cout << \"D\"; } };\n\nint main() { D d; cout << \"\\n\"; }\n```",
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
                "explanation": "构造顺序的完整规则只有三条：**虚基类 → 非虚基类（按声明序）→ 成员对象（按声明序）→ 自身函数体**。\n所以先构造 V（虚基类永远第一，哪怕它在继承列表里排在 B 后面、在初始化列表里根本没写），再按声明序构造 N、B（B 里的 V 已被跳过），最后进 D → `VNBD`。\n「NVBD」是按继承列表顺序；「NBVD」是按初始化列表顺序 —— 两者都错，初始化列表只递参数、不定顺序；「VNBDV」以为虚基类会被每一层各构造一次。\n★ 这段代码还有一个隐藏考点：`D` 的初始化列表写 `B(), N()`，但实际构造顺序仍是 N→B。编译器对「列表顺序与声明顺序不一致」会给 `-Wreorder` 警告。"
            }
        ]
    },
    {
        "title": "构造析构顺序规则与初始化列表的职责",
        "subject": "cpp",
        "line": "text",
        "question_type": "short_answer",
        "difficulty": 4,
        "total_score": 12,
        "tags": [
            "构造顺序",
            "析构顺序",
            "初始化列表",
            "简答"
        ],
        "choices": [],
        "source_section": "第 07 讲 · 类的继承",
        "statement_md": "**简答题**：派生类对象构造时的完整顺序是什么？析构顺序又是什么？初始化列表里各项的书写顺序会不会改变构造顺序？请一并说明初始化列表真正的作用。",
        "input_format": "",
        "output_format": "一句话作答（不要抄题目、不要写代码）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "构造顺序是虚基类、非虚基类、成员对象、自身函数体，析构严格相反；初始化列表的书写顺序不改变构造顺序，它只负责给基类和成员递构造实参",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|构造顺序是虚基类、非虚基类、成员对象、自身函数体，析构严格相反；初始化列表的书写顺序不改变构造顺序，它只负责给基类和成员递构造实参\n|先虚基类再非虚基类（按声明序），然后成员对象（按声明序），最后自身构造体；析构逆序；初始化列表不影响顺序，只传参\n|构造自顶向下：基类→成员对象→自身，析构自底向上严格相反；顺序由声明决定，初始化列表只是参数清单\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "构造自顶向下，分四段：**虚基类 → 直接非虚基类（按声明顺序）→ 成员对象（按声明顺序）→ 自身函数体**；析构严格逆序，且每一层都是「先自身函数体、再成员、再基类」。\n初始化列表**不是顺序说明书**，它只做两件事：给基类子对象和成员对象**递构造实参**，以及避免「先默认构造再赋值」的那一次多余操作。真正的顺序由**继承列表与成员声明顺序**决定。\n为什么必须这样：对象的内存布局是按声明排好的，构造必须与布局同序；析构逆序则保证「后构造的先拆」，依赖关系不会倒挂（成员用到基类资源时尤其关键）。\n★ 两个直接推论：① 基类没有默认构造时，**只能**靠初始化列表传参（构造函数不被继承）；② 成员对象在函数体开始前就已构造完成，所以在函数体里赋值等于多构造一次。"
            }
        ]
    },
    {
        "title": "不能被重载的运算符",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "运算符重载"
        ],
        "choices": [
            "+=",
            "==",
            "[]",
            "?:"
        ],
        "source_section": "第 08 讲 · 多态性",
        "statement_md": "下列运算符中，**不能**被重载的是：",
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
                "explanation": "C++ 里有五个运算符不能重载：`.`（成员访问）、`.*`（成员指针访问）、`::`（作用域分辨符）、`?:`（三目条件）、`sizeof`。\n另外三条「不能改」：**优先级、结合性、操作数个数**都不能动。\n`+=`、`==`、`[]` 都是最常被重载的三个，`[]` 更是写容器类的必备。"
            }
        ]
    },
    {
        "title": "运算符重载能否改变优先级与结合性",
        "subject": "cpp",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 1,
        "total_score": 8,
        "tags": [
            "运算符重载"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 08 讲 · 多态性",
        "statement_md": "为自定义类型重载运算符时，可以顺便改变该运算符的优先级和结合性。",
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
                "explanation": "错。重载只是给运算符**换一个含义**（本质是名字特殊的函数），它的优先级、结合性、操作数个数都由语言定死，一个都改不了。\n也不能创造新运算符（比如 `**`），不能重载 `.`、`.*`、`::`、`?:`、`sizeof`。"
            }
        ]
    },
    {
        "title": "前置与后置自增的返回值差异",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "运算符重载",
            "自增"
        ],
        "choices": [
            "6 6 7",
            "6 7 7",
            "7 7 7",
            "6 6 6"
        ],
        "source_section": "第 08 讲 · 多态性",
        "statement_md": "下面程序的输出是？（`a` 取自 `++c`，`b` 取自 `c++`）\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nstruct Counter {\n    int v;\n    explicit Counter(int x) : v(x) {}\n    Counter& operator++() { ++v; return *this; }\n    Counter operator++(int) { Counter old(*this); ++v; return old; }\n    int val() const { return v; }\n};\n\nint main() {\n    Counter c(5);\n    int a = (++c).val();\n    int b = (c++).val();\n    cout << a << \" \" << b << \" \" << c.val() << \"\\n\";\n}\n```",
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
                "explanation": "`++c`（前置）先自增再返回**自身引用**，此时 v=6 → a=6；`c++`（后置）先备份旧值（此刻 v 已经是 6）、再自增到 7、返回**旧值副本** → b=6；最后 `c.val()` 是 7。\n「6 7 7」把后置当成「先加后返回」；「7 7 7」以为后置也返回新值；「6 6 6」漏了后置那一次自增确实改了对象本身。\n★ 后置多一个 `int` 占位形参 + 一次对象拷贝，所以能用前置就别用后置。"
            }
        ]
    },
    {
        "title": "经基类指针调用虚函数与非虚函数",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "虚函数",
            "动态绑定"
        ],
        "choices": [
            "BfDg",
            "DfBg",
            "DfDg",
            "BfBg"
        ],
        "source_section": "第 08 讲 · 多态性",
        "statement_md": "下面程序的输出是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nstruct B {\n    virtual void f() { cout << \"Bf\"; }\n    void g() { cout << \"Bg\"; }\n};\nstruct D : B {\n    void f() { cout << \"Df\"; }\n    void g() { cout << \"Dg\"; }\n};\n\nint main() { B* p = new D; p->f(); p->g(); cout << \"\\n\"; }\n```",
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
                "explanation": "`p` 的声明类型是 `B*`、实际指向 `D` 对象。`f` 是虚函数 → 按**实际类型**动态绑定，输出 `Df`；`g` 不是虚函数 → 按**声明类型**静态绑定，输出 `Bg`。\n这一对是整章的核心对照：**同一个指针、同一句调用形式，virtual 与否结果不同**。\n「DfDg」以为非虚函数也会动态绑定；「BfBg」以为虚函数没起作用（或忘了实际对象是 D）；「BfDg」正好把两者对调。"
            }
        ]
    },
    {
        "title": "后置自增的占位形参类型",
        "subject": "cpp",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "运算符重载",
            "自增"
        ],
        "choices": [],
        "source_section": "第 08 讲 · 多态性",
        "statement_md": "为了让前置 `++` 与后置 `++` 能重载成两个不同的函数，后置版本要多写一个形参。这个占位形参的**类型名**是什么？（只写类型，不写形参名）\n\n提示：调用时编译器总是传 0 给它，它不参与任何运算。",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "int",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|int\n|int类型\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "后置版本写作 `Counter operator++(int)`，那个 `int` 纯粹是**区分前后置的暗号**（调用时固定传 0，函数体里用不到它）。\n前置是 `operator++()`：无参、返回**引用**（`Counter&`）；后置是 `operator++(int)`：多一个占位参、返回**旧值副本**（值，不是引用）。\n★ 后置如果也返回引用，返回的就是局部副本的引用 —— 悬垂引用。"
            }
        ]
    },
    {
        "title": "operator<< 为什么只能重载为非成员函数",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "运算符重载",
            "operator<<",
            "成员vs非成员"
        ],
        "choices": [
            "成员函数不能返回流引用，链式输出会断",
            "成员函数访问不到私有成员，所以只能写非成员",
            "C++ 规定所有流运算符都必须是友元函数",
            "成员版的左操作数必须是本类对象，而 `cout << c` 的左操作数是 ostream"
        ],
        "source_section": "第 08 讲 · 多态性",
        "statement_md": "要把自定义类 `C` 用 `cout << c` 直接输出，`operator<<` 通常必须写成**非成员**函数。根本原因是：",
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
                "explanation": "重载为成员函数时，`c << x` 被解释成 `c.operator<<(x)` —— **左操作数就是 this**，必须是本类对象。而 `cout << c` 的左操作数是 `ostream`，你不可能给标准库的 ostream 加一个成员函数，所以只能写非成员 `ostream& operator<<(ostream&, const C&)`。\n要读私有成员就在类里声明它为 `friend`（**只是授权，不改变它是非成员**这一点）。\n「不能返回流引用」正好说反：非成员版返回 `ostream&` 才能支持 `a << b << c` 连锁；「成员函数访问不到私有成员」也反了（成员函数当然能访问）；「必须是友元」不成立 —— 只用 public 接口的 `operator<<` 合法，不写 friend 也行。"
            }
        ]
    },
    {
        "title": "左操作数不是本类对象时的重载方式",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "运算符重载",
            "成员vs非成员"
        ],
        "choices": [
            "把成员版声明为 `static`",
            "在类里再加一个成员版 `C operator+(int) const`",
            "另外定义一个非成员函数 `C operator+(double, const C&)`",
            "把成员版改成 `C operator+(double)`"
        ],
        "source_section": "第 08 讲 · 多态性",
        "statement_md": "类 `C` 已有成员版 `C operator+(const C&) const`，所以 `c + 1` 可用。现在要让 `10 + c` 也成立（结果仍是 `C`），应该：",
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
                "explanation": "`10 + c` 的左操作数是 `double`，而**成员版的左操作数永远是本类对象**，所以无论怎么加成员重载都轮不到它 —— 只能写非成员（需要私有成员时在类里声明 friend）：\n```cpp\nC operator+(double d, const C& c) { return C(d) + c; }\n```\n「改成 `operator+(double)`」只是把右操作数换成 double，左操作数还是 C；「`static`」不行 —— 运算符重载不能是静态成员函数（没有 this 就凑不齐操作数）；「再加一个成员版」与「另外定义一个非成员函数」同理，左操作数依旧必须是 C。\n★ 判断该写成员还是非成员，只看一句话：**左操作数是不是本类对象**。`=、[]、()、->` 必须是成员；`<<、>>`、左操作数为内建类型的算术运算必须是非成员。"
            }
        ]
    },
    {
        "title": "关于虚函数与抽象类的正确说法",
        "subject": "cpp",
        "line": "text",
        "question_type": "multiple_choice",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "虚函数",
            "抽象类",
            "多选"
        ],
        "choices": [
            "派生类只实现一部分纯虚函数后就可以实例化",
            "经基类指针或引用调用虚函数时，按对象的实际类型绑定",
            "构造函数不能声明为虚函数",
            "含纯虚函数的类不能定义对象"
        ],
        "source_section": "第 08 讲 · 多态性",
        "statement_md": "关于虚函数、纯虚函数与抽象类，下列说法**正确**的有：\n\n**多选题**：正确选项不止一个，点选切换，再次点击可取消。",
        "input_format": "",
        "output_format": "若干个选项字母，按字母升序连写（如 `AC`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "BCD",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|BCD\n|BDC\n|CBD\n|CDB\n|DBC\n|DCB\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "四条里只有「派生类只实现一部分纯虚函数后就可以实例化」是错的：剩下的纯虚函数会被继承下来，派生类**仍是抽象类**，一实例化就编译错 —— 纯虚函数要么全实现，要么继续当抽象类。\n其余三条都对：动态绑定三条件之一就是「经基类指针/引用调用」；构造函数不能是虚函数（那时 vptr 还没设好，谈不上查表）；含纯虚函数即抽象类，`Shape s;` 和 `new Shape` 都是编译错。"
            }
        ]
    },
    {
        "title": "基类析构非虚时 delete 基类指针",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "虚析构",
            "资源泄漏"
        ],
        "choices": [
            "~D~B",
            "~B~D",
            "~D",
            "~B"
        ],
        "source_section": "第 08 讲 · 多态性",
        "statement_md": "下面程序的输出是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nstruct B { ~B() { cout << \"~B\"; } };\nstruct D : B { ~D() { cout << \"~D\"; } };\n\nint main() { B* p = new D; delete p; cout << \"\\n\"; }\n```",
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
                "explanation": "`~B` 不是虚函数，`delete p` 只按 `p` 的**声明类型**调 `~B`，然后到此为止 ——`~D` 根本不会执行。如果 `D` 里 `new` 过东西，那块内存就永久泄漏了。\n★ 更可怕的是它**编译时一条警告都没有**：`B` 里一个 virtual 都没有，属于普通非多态类，`-Wdelete-non-virtual-dtor` 也管不到。对策是纪律性的：只要类会被继承，析构就写 virtual。\n「~D~B」是基类析构加了 virtual 之后的正确链条；「~B~D」把析构顺序写反了（析构永远派生类先、基类后）；「~D」漏了基类那一步。"
            }
        ]
    },
    {
        "title": "运行期多态成立的三条件",
        "subject": "cpp",
        "line": "text",
        "question_type": "short_answer",
        "difficulty": 3,
        "total_score": 12,
        "tags": [
            "多态",
            "动态绑定",
            "简答"
        ],
        "choices": [],
        "source_section": "第 08 讲 · 多态性",
        "statement_md": "**简答题**：C++ 的运行期多态（动态绑定）要成立，必须同时满足哪三个条件？请按「函数怎么声明 → 怎么调用 → 对象是什么」的顺序作答。",
        "input_format": "",
        "output_format": "一句话作答（不要抄题目、不要写代码）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "被调用的函数在基类中声明为虚函数，经基类指针或引用调用，实际对象是派生类",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|被调用的函数在基类中声明为虚函数，经基类指针或引用调用，实际对象是派生类\n|虚函数、基类指针或引用调用、公有继承且实际对象为派生类\n|函数是 virtual，通过基类指针或引用调用，实际类型是派生类对象\n|virtual 成员函数 + 基类指针/引用 + 实际对象为派生类\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "三条件缺一不可：\n① 该成员函数在基类里声明为 `virtual`（派生类重写时签名必须完全一致：返回类型、函数名、参数表、const 都要对得上，建议写 `override` 让编译器替你查）；\n② 通过**基类指针或引用**调用（对象直接调用是编译期静态绑定；切片后的基类对象更没戏）；\n③ 实际对象是**公有派生**的派生类对象（类型兼容保证基类指针能指向它）。\n缺①退回静态绑定（第 7 讲 `p->withdraw()` 的痛点）；缺②即使有 virtual 也不会动态绑定；缺③连转换都不成立。"
            }
        ]
    },
    {
        "title": "构造函数里调用虚函数",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "虚函数",
            "构造期",
            "vtable"
        ],
        "choices": [
            "B/D",
            "D/D",
            "B/B",
            "D/B"
        ],
        "source_section": "第 08 讲 · 多态性",
        "statement_md": "下面程序的输出是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nstruct B {\n    B() { init(); }\n    virtual void init() { cout << \"B\"; }\n};\nstruct D : B { void init() { cout << \"D\"; } };\n\nint main() { D d; cout << \"/\"; B* p = &d; p->init(); cout << \"\\n\"; }\n```",
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
                "explanation": "构造 `D` 对象时先构造 `B` 子对象，此刻对象的 vptr 还指着 **B 的虚函数表**、「这个对象还不是 D」，所以 `B::B()` 里那句 `init()` 只能静态绑定到 `B::init` → 输出 `B`；构造完成后经 `B*` 调用才真正查表 → `D::init` 输出 `D`。\n「D/D」以为构造期也会动态绑定；「B/B」以为指针调用也静态绑定；「D/B」对调。\n★ 结论：**不要在构造函数（和析构函数）里调用虚函数** —— 那时虚函数退化为静态绑定，初始化逻辑请放到构造完成后单独调用的普通成员函数里。"
            }
        ]
    },
    {
        "title": "抽象基类指针数组的统一遍历",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "纯虚函数",
            "抽象类",
            "动态绑定"
        ],
        "choices": [
            "编译错误：抽象类不能定义指针数组",
            "Sq4Ci3",
            "Shape4Shape3",
            "Sq3Ci4"
        ],
        "source_section": "第 08 讲 · 多态性",
        "statement_md": "`Shape` 的两个成员函数都是纯虚函数。下面程序依次输出每个图形的名字与面积，结果是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nstruct Shape {\n    virtual double area() const = 0;\n    virtual const char* name() const = 0;\n    virtual ~Shape() = default;\n};\nstruct Sq : Shape {\n    double area() const override { return 4; }\n    const char* name() const override { return \"Sq\"; }\n};\nstruct Ci : Shape {\n    double area() const override { return 3; }\n    const char* name() const override { return \"Ci\"; }\n};\n\nint main() {\n    Shape* a[2] = { new Sq, new Ci };\n    for (auto p : a) cout << p->name() << p->area();\n    cout << \"\\n\";\n    delete a[0]; delete a[1];\n}\n```",
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
                "explanation": "纯虚函数只定合同不干活，派生类**必须全部实现**才能实例化；`Shapes* a[2]` 里存的是基类指针，`p->name()`、`p->area()` 经指针调用虚函数 → 按**实际类型**动态绑定 → `Sq4Ci3`。\n「Shape4Shape3」是忘了 virtual 或按声明类型静态绑定；「Sq3Ci4」把两行对调（面积跟着名字走，不会串）；「抽象类不能定义指针数组」是常见误解 —— 抽象类**不能定义对象**，但指针和引用随便用，这正是多态容器能成立的前提。\n★ 顺带看 `virtual ~Shape() = default;`：接口类的标准三件套是「纯虚接口 + 虚析构 + override」，少一个虚析构，`delete a[0]` 就只析构基类部分。"
            }
        ]
    },
    {
        "title": "签名差一个 const 时 override 的诊断",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "override",
            "虚函数重写",
            "签名"
        ],
        "choices": [
            "编译通过，且正常构成重写",
            "编译错：override 只能用在析构函数上",
            "编译错：它没有重写任何基类虚函数",
            "编译通过，但静默变成一个新函数，多态失效"
        ],
        "source_section": "第 08 讲 · 多态性",
        "statement_md": "基类写 `virtual void show() const;`，派生类写 `void show() override;`（少了尾部 const）。结果是：",
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
                "explanation": "重写要求**签名完全一致**：返回类型、函数名、参数表、**const 限定**，一个都不能差。`show()` 与 `show() const` 是两个不同的函数，所以派生类这个 `show` 谁也没重写。\n写了 `override` 时编译器立刻报错（实测 `marked 'override', but does not override`）——这正是 override 的价值：把「我以为我重写了」从静默 bug 变成编译错。\n「静默变成新函数」是**不写** override 时的后果：编译通过、经基类指针调到的还是基类版，多态悄悄失效，这类 bug 最难查。「override 只能用于析构」完全是编造的。\n★ 现代写法：重写处一律写 `override`（可省略 virtual），让编译器替你核对签名。"
            }
        ]
    },
    {
        "title": "虚析构下 delete 基类指针的计数结果",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "虚析构",
            "析构链"
        ],
        "choices": [
            "11",
            "1",
            "10",
            "0"
        ],
        "source_section": "第 08 讲 · 多态性",
        "statement_md": "`B` 的析构是虚函数（基类计数 +1），`D` 的析构把计数 +10。下面程序经基类指针删除派生类对象，输出的计数是多少？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nstruct B { static int n; virtual ~B() { n += 1; } };\nint B::n = 0;\nstruct D : B { ~D() { B::n += 10; } };\n\nint main() { B* p = new D; delete p; cout << B::n << \"\\n\"; }\n```",
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
                "explanation": "`~B` 是虚函数，`delete p` 会按 `p` 指向的**实际类型**先调 `~D()`（+10），再由编译器自动接着调 `~B()`（+1），合计 **11** —— 完整析构链，一个不漏。\n「1」正是把 `virtual` 去掉的结果：只按声明类型调 `~B()`，派生类析构根本不执行；「10」漏了基类那一步；「0」以为根本没析构。\n★ 所以「会被继承的类，析构必须 virtual」；接口类直接写 `virtual ~Iface() = default;`。反过来，**不需要被继承的类**（如 `final` 类）别乱加 virtual —— 会平白多一个 vptr 和一层间接。"
            }
        ]
    },
    {
        "title": "基类析构为什么必须声明为虚函数",
        "subject": "cpp",
        "line": "text",
        "question_type": "short_answer",
        "difficulty": 4,
        "total_score": 12,
        "tags": [
            "虚析构",
            "资源泄漏",
            "简答"
        ],
        "choices": [],
        "source_section": "第 08 讲 · 多态性",
        "statement_md": "**简答题**：为什么「会被继承的类」的析构函数应当声明为 `virtual`？请说明经基类指针 `delete` 一个派生类对象时，非虚析构会导致什么后果。",
        "input_format": "",
        "output_format": "一句话作答（不要抄题目、不要写代码）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "经基类指针 delete 派生类对象时，非虚析构只调用基类析构，派生类析构不执行，派生类申请的资源泄漏；声明为 virtual 才会按实际类型先析构派生类再析构基类",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|经基类指针 delete 派生类对象时，非虚析构只调用基类析构，派生类析构不执行，派生类申请的资源泄漏；声明为 virtual 才会按实际类型先析构派生类再析构基类\n|不声明 virtual 时 delete 基类指针只析构基类部分，派生类的析构函数不被调用，造成内存泄漏；虚析构保证完整析构链\n|因为 delete 按静态类型调用析构函数，非虚析构漏掉派生类析构，资源泄漏；virtual 让它查表按实际类型析构\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`delete p` 时如果析构函数**不是虚函数**，调用哪一层析构由 `p` 的**声明类型**决定，于是只执行 `~Base()`，`~Derived()` 里的 `delete[]`、关文件、解锁全都不会跑 ——资源泄漏，而且编译期往往**一条警告都没有**（类里没有任何 virtual 时，`-Wdelete-non-virtual-dtor` 也不报警）。\n声明成 `virtual ~Base()` 之后，`delete` 会查虚函数表按**实际类型**先调 `~Derived()`、再由编译器自动接着调 `~Base()`，形成完整析构链。\n★ 所以接口类/抽象类的标准开头是「纯虚函数 + `virtual ~Iface() = default;`」。"
            }
        ]
    },
    {
        "title": "切片对象与作用域分辨符调用虚函数",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "对象切片",
            "虚函数",
            "作用域分辨符"
        ],
        "choices": [
            "DDB",
            "BDD",
            "DDD",
            "BDB"
        ],
        "source_section": "第 08 讲 · 多态性",
        "statement_md": "下面程序的输出是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nstruct B { virtual void f() { cout << \"B\"; } };\nstruct D : B { void f() { cout << \"D\"; } };\n\nint main() {\n    D d;\n    B b = d;\n    B& r = d;\n    b.f(); r.f(); d.B::f(); cout << \"\\n\";\n}\n```",
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
                "explanation": "`B b = d;` 是**切片**：`b` 的实际类型就是 `B`，vptr 指向 `B` 的表，`b.f()` → `B`；`B& r = d;` 是引用绑定、不切片，`r.f()` 走动态绑定 → `D`；`d.B::f()` 用 `::` **显式跳过动态绑定**，指名调基类版本 → `B`。\n「DDB」以为切片对象还保留 `D` 的 vtable（这正是切片最坑的地方：它连多态一起切掉了）；「BDD」以为 `::` 也走动态绑定；「DDD」三处全按实际类型。\n★ 记住三句话：指针/引用不切片、赋值必切片、`::` 显式调用不查表。"
            }
        ]
    },
    {
        "title": "复合赋值运算符返回引用的链式效果",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "运算符重载",
            "复合赋值",
            "返回引用"
        ],
        "choices": [
            "6 3",
            "3 2",
            "编译错误：不能对表达式结果再赋值",
            "6 2"
        ],
        "source_section": "第 08 讲 · 多态性",
        "statement_md": "`operator+=` 返回 `N&`（`*this`）。执行 `(a += b) += c;` 之后，输出是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nstruct N {\n    int v;\n    explicit N(int x) : v(x) {}\n    N& operator+=(const N& o) { v += o.v; return *this; }\n};\n\nint main() {\n    N a(1), b(2), c(3);\n    (a += b) += c;\n    cout << a.v << \" \" << b.v << \"\\n\";\n}\n```",
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
                "explanation": "`a += b` 返回的是 **a 自己的引用**，所以外层 `+= c` 改的仍是 a：1+2+3 = 6；`b`、`c` 全程只被读，仍是 2 和 3 → `6 2`。\n如果 `operator+=` 返回值（`N` 而不是 `N&`），外层改的是**临时副本**，a 停在 3 → 那是「3 2」；「6 3」以为 `+=` 会顺手改动右操作数（不会，右操作数是 const 引用）。\n★ 三条返回类型的惯例：`+= -= *=` 等复合赋值返回 `T&`（支持链式、与内建语义一致）；`+ - *` 返回新值 `T`；`++` 前置返回 `T&`、后置返回 `T`。"
            }
        ]
    },
    {
        "title": "关于 override、final 与虚析构的正确说法",
        "subject": "cpp",
        "line": "text",
        "question_type": "multiple_choice",
        "difficulty": 4,
        "total_score": 14,
        "tags": [
            "override",
            "final",
            "虚析构",
            "多选"
        ],
        "choices": [
            "final 修饰虚函数表示派生类不能再重写它",
            "抽象类的析构函数不需要是虚函数，因为抽象类不能实例化",
            "重写虚函数时写 override，签名写错会直接编译错",
            "final 修饰类表示该类不能再被继承"
        ],
        "source_section": "第 08 讲 · 多态性",
        "statement_md": "关于 C++11 的 `override`/`final` 与虚析构，下列说法**正确**的有：\n\n**多选题**：正确选项不止一个，点选切换，再次点击可取消。",
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
                "explanation": "四条里只有「抽象类的析构函数不需要是虚函数」是错的，而且错得很有代表性：抽象类**不能定义对象，但一定会有派生类对象**，而那些对象常常由基类指针持有 —— 只要可能经基类指针 `delete`，析构就必须是虚的，接口类的标准写法是 `virtual ~Shape() = default;`。\n其余三条都对：`override` 把「签名差一点、静默变新函数」变成编译错；`class X final` 禁止再继承（再继承直接编译错）；`void f() final` 禁止派生类再重写这一个函数。\n★ 三者合起来的现代接口写法：纯虚函数定合同 + `virtual ~Iface() = default;` + 派生类 `override`。"
            }
        ]
    },
    {
        "title": "类模板实例化为什么必须写出类型实参",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "类模板",
            "实例化"
        ],
        "choices": [
            "类模板的构造函数不能带参数",
            "模板的类型参数只能取内置类型",
            "类模板必须先被继承才能使用",
            "类模板使用时必须显式给出类型实参，应写成 Box<double> b(3.14);"
        ],
        "source_section": "第 09 讲 · 模板与群体数据",
        "statement_md": "已有 `template <typename T> class Box { T item; public: Box(T it); };`，此时写 `Box b(3.14);` 编译不通过。原因是：",
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
                "explanation": "函数模板能靠实参推导 `T`，**类模板不行**（C++14 没有类模板实参推导 CTAD，那是 C++17 才有的）：`Box` 本身不是类型，只是图纸，必须先说清按哪个 `T` 生成类。\n构造函数带参数完全合法（`Box(T it)`）；`T` 也可以是 `string`、自定义类，只要支持体内用到的操作；「必须被继承」更是无稽之谈 —— `Box<double>` 与 `Box<int>` 是两个**互不相干的类**，彼此没有继承关系。"
            }
        ]
    },
    {
        "title": "同一模板对不同实参类型的实例化",
        "subject": "cpp",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 1,
        "total_score": 8,
        "tags": [
            "函数模板",
            "实例化"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 09 讲 · 模板与群体数据",
        "statement_md": "`myMax(3, 7)` 与 `myMax(3.5, 2.5)` 调用的是同一个 `template <typename T> T myMax(T, T)` 实例化出来的同一个函数。",
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
                "explanation": "错。前者推 `T = int`、后者推 `T = double`，是**两次独立的实例化**，编译器生成两个不同的函数。\n这也是必须说清的一点：模板**不省运行时间**（跑的还是具体类型的代码），省的是你抄几遍源码的力气；代价是编译变慢、报错信息变难读。"
            }
        ]
    },
    {
        "title": "显式指定类型实参后的实参转换",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "函数模板",
            "显式实例化"
        ],
        "choices": [
            "3",
            "7",
            "7.9",
            "8"
        ],
        "source_section": "第 09 讲 · 模板与群体数据",
        "statement_md": "下面程序的输出是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\ntemplate <typename T>\nT myMax(T a, T b) { return a > b ? a : b; }\n\nint main() { cout << myMax<int>(3, 7.9) << \"\\n\"; }\n```",
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
                "explanation": "写成 `myMax<int>` 之后编译器**不再推导**，`T` 直接钉死为 `int`，实参 `7.9` 按 `double → int` 的常规转换截断成 7，返回值也是 `int`，所以输出 `7`。\n「7.9」以为显式指定不影响实参类型；「8」以为会四舍五入（C++ 的浮点转整型是**截断**，不是四舍五入）；「3」无依据。\n★ 对比：不写 `<int>` 的 `myMax(3, 7.9)` 会**编译失败** —— 从 3 推 `T=int`、从 7.9 推 `T=double`，推导冲突。"
            }
        ]
    },
    {
        "title": "普通函数与函数模板的重载优先",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "函数模板",
            "重载解析"
        ],
        "choices": [
            "73.5",
            "P7P3.5",
            "P7P3",
            "P73.5"
        ],
        "source_section": "第 09 讲 · 模板与群体数据",
        "statement_md": "下面程序的输出是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\ntemplate <typename T>\nT myMax(T a, T b) { return a > b ? a : b; }\n\nint myMax(int a, int b) { cout << \"P\"; return a > b ? a : b; }\n\nint main() { cout << myMax(3, 7) << myMax(3.5, 2.5) << \"\\n\"; }\n```",
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
                "explanation": "`myMax(3, 7)` 两个实参都是 `int`，与普通函数 `myMax(int, int)` **完全匹配**，按重载解析规则普通函数优先于模板实例 → 先打 `P` 再打 7；`myMax(3.5, 2.5)` 是 `double`，普通函数接它要做浮点→整型转换（劣于模板的精确匹配），所以走模板实例化的 `double` 版 → 打 3.5。\n「73.5」漏了普通函数优先；「P7P3.5」以为 `double` 也会被普通函数接走；「P7P3」是把 3.5 也截成了 3。\n★ 想让 `int` 实参强制走模板，写 `myMax<>(3, 7)`。"
            }
        ]
    },
    {
        "title": "循环队列类模板牺牲一格判满",
        "subject": "cpp",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "队列",
            "类模板",
            "判满"
        ],
        "choices": [],
        "source_section": "第 09 讲 · 模板与群体数据",
        "statement_md": "下面程序里连续入队 5 个元素，最终成功入队的次数是多少？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\ntemplate <typename T>\nclass Queue {\n    T* data; int front, rear, cap;\npublic:\n    explicit Queue(int c = 10) : data(new T[c]), front(0), rear(0), cap(c) {}\n    ~Queue() { delete[] data; }\n    bool enqueue(const T& e) {\n        if ((rear + 1) % cap == front) return false;   // 牺牲一格判满\n        data[rear] = e; rear = (rear + 1) % cap; return true;\n    }\n};\n\nint main() {\n    Queue<int> q(5);\n    int ok = 0;\n    for (int i = 1; i <= 5; i++) if (q.enqueue(i)) ok++;\n    cout << ok << \"\\n\";\n}\n```",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "4",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "判满条件是 `(rear + 1) % cap == front` ——「牺牲一格」法：`cap = 5` 的数组实际只能放 4 个元素，第 5 次入队时 `(4+1)%5 == 0 == front` 成立，直接返回 false。\n为什么要牺牲一格：队空和队满都是 `front == rear`，不腾出一格就没法区分；另一条路是额外维护 `size` 或 `tag` 变量。\n★ 这与数据结构线手写队列的约定完全一致，模板只是把元素类型参数化了。"
            }
        ]
    },
    {
        "title": "类模板成员函数类外定义的完整前缀",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "类模板",
            "类外定义"
        ],
        "choices": [
            "T Box::get() const { return item; }",
            "template <typename T> T Box::get() const { return item; }",
            "template <typename T> T Box<T>::get<T>() const { return item; }",
            "template <typename T> T Box<T>::get() const { return item; }"
        ],
        "source_section": "第 09 讲 · 模板与群体数据",
        "statement_md": "有 `template <typename T> class Box { T item; public: T get() const; };`。在类外定义 `get()`，正确写法是：",
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
                "explanation": "类模板的成员在类外定义要凑齐**四要素**：① `template <typename T>` 前缀（重申模板语境）；② 返回类型 `T`；③ 类名必须带参数表 `Box<T>::`；④ 函数名与 const 等修饰照抄。\n少任何一项都是编译错：漏前缀 → `T` 没定义；只写 `Box::` → 模板名在模板语境里必须带 `<T>`；`get<T>()` → 普通成员函数不是模板，不能带自己的模板实参表。\n★ 这也是为什么类模板的声明和实现**必须放同一个头文件**：实例化发生在用到它的编译单元里，编译器那时必须看得见完整定义。"
            }
        ]
    },
    {
        "title": "两个实参推出不同类型时函数模板的推导",
        "subject": "cpp",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 2,
        "total_score": 8,
        "tags": [
            "函数模板",
            "类型推导",
            "编译错"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 09 讲 · 模板与群体数据",
        "statement_md": "`template <typename T> T myMax(T, T);` 之后写 `myMax(3, 7.9)`，编译器会把 `T` 推成 `double`，并自动把 3 转成 3.0。",
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
                "explanation": "错，这是**推导冲突**，直接编译失败：从 `3` 推出 `T = int`，从 `7.9` 推出 `T = double`，同一个 `T` 得到两个答案，编译器不会替你挑一个。\n两条修法：① 显式指定 `myMax<double>(3, 7.9)`（此后不再推导，3 按常规转换变 3.0）；② 用两个类型参数 `template <typename T, typename U>` 各管各的。\n★ 注意这与「显式指定后 7.9 被截成 7」不同：`myMax<int>(3, 7.9)` 是先钉死 T=int，再做转换，合法且结果 7；不写 `<int>` 才叫推导冲突。"
            }
        ]
    },
    {
        "title": "数组类模板深复制的效果",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "深复制",
            "类模板"
        ],
        "choices": [
            "0 9",
            "9 9",
            "0 0",
            "9 0"
        ],
        "source_section": "第 09 讲 · 模板与群体数据",
        "statement_md": "下面程序的输出是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\ntemplate <typename T>\nstruct Arr {\n    T* p; int n;\n    explicit Arr(int k) : p(new T[k]()), n(k) {}\n    Arr(const Arr& a) : p(new T[a.n]), n(a.n) {          // 深复制\n        for (int i = 0; i < n; i++) p[i] = a.p[i];\n    }\n    ~Arr() { delete[] p; }\n    T& operator[](int i) { return p[i]; }\n};\n\nint main() {\n    Arr<int> a(3); a[0] = 0; a[1] = 1; a[2] = 2;\n    Arr<int> b = a;\n    b[0] = 9;\n    cout << a[0] << \" \" << b[0] << \"\\n\";\n}\n```",
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
                "explanation": "复制构造函数自己 `new` 了一块新内存再逐元素拷，所以 `a` 与 `b` 各有一份数据，改 `b[0]` 不影响 `a` → `0 9`。\n「9 9」是**浅复制**（编译器默认版本只拷指针值）的表现：两个对象指向同一块内存，改一个另一个跟着变，而且析构时会对同一块内存 `delete[]` 两次 → 崩溃。\n★ 含指针成员的类，「三件套」缺一不可：复制构造 + 赋值运算符 + 析构。"
            }
        ]
    },
    {
        "title": "插入排序第三趟的结果",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "插入排序",
            "排序过程"
        ],
        "choices": [
            "1 2 3 4 5",
            "1 2 4 5 3",
            "2 4 5 1 3",
            "2 5 4 1 3"
        ],
        "source_section": "第 09 讲 · 模板与群体数据",
        "statement_md": "对 `{5, 2, 4, 1, 3}` 做直接插入排序，每趟结束记录一次序列，下面程序输出**第三趟**结束时的序列：\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nint main() {\n    int a[] = {5, 2, 4, 1, 3}; int n = 5;\n    vector<string> pass;\n    for (int i = 1; i < n; i++) {\n        int t = a[i], j = i - 1;\n        while (j >= 0 && a[j] > t) { a[j + 1] = a[j]; j--; }\n        a[j + 1] = t;\n        string s;\n        for (int k = 0; k < n; k++) { if (k) s += \" \"; s += to_string(a[k]); }\n        pass.push_back(s);\n    }\n    cout << pass[2] << \"\\n\";\n}\n```",
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
                "explanation": "逐趟看：\n第 1 趟把 2 插到 5 前 → `2 5 4 1 3`；\n第 2 趟把 4 插到 5 前 → `2 4 5 1 3`；\n第 3 趟把 1 一路挪到最前 → `1 2 4 5 3`。\n「2 4 5 1 3」是第二趟；「2 5 4 1 3」是第一趟；「1 2 4 5 3」才对；「1 2 3 4 5」是全部四趟跑完的最终结果。\n★ 插入排序第 i 趟结束，前 i+1 个元素一定有序，后面仍保持原样 —— 拿这条就能自查。"
            }
        ]
    },
    {
        "title": "插入排序内层循环的条件顺序",
        "subject": "cpp",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 3,
        "total_score": 8,
        "tags": [
            "插入排序",
            "越界"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 09 讲 · 模板与群体数据",
        "statement_md": "把直接插入排序的内层写成 `while (a[j] > t && j >= 0)`，与写成 `while (j >= 0 && a[j] > t)` 效果一样，都不会出错。",
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
                "explanation": "错。`&&` 严格**从左到右短路求值**：写成 `a[j] > t && j >= 0` 时，`j = -1` 会先算 `a[-1]` —— 数组越界，未定义行为，可能崩、也可能读到垃圾值继续跑。\n正确写法必须把**边界判断放前面**：`while (j >= 0 && a[j] > t)`，这样 `j < 0` 时右边根本不会求值。\n★ 同理适用于所有「先判越界再取元素」的循环。"
            }
        ]
    },
    {
        "title": "函数模板全特化后的调用选择",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "模板特化",
            "全特化",
            "函数模板"
        ],
        "choices": [
            "generic hi",
            "generic generic",
            "hi hi",
            "编译错误：特化必须写在类内"
        ],
        "source_section": "第 09 讲 · 模板与群体数据",
        "statement_md": "有一个通用模板和它的一个全特化版本。下面程序的输出是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\ntemplate <typename T> const char* tag(T) { return \"generic\"; }\ntemplate <> const char* tag<const char*>(const char* s) { return s; }\n\nint main() { cout << tag(1) << \" \" << tag(\"hi\") << \"\\n\"; }\n```",
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
                "explanation": "`template <> const char* tag<const char*>(...)` 是**全特化**：为 `T = const char*` 单独写一份实现。重载/特化的选择规则是「越专门越优先」—— 实参类型精确命中特化版就用它，其余仍走通用模板。\n所以 `tag(1)`（T=int）走通用版打 `generic`，`tag(\"hi\")`（T=const char*）命中特化版，直接把字符串返回 → `generic hi`。\n「generic generic」是以为特化没生效；「hi hi」以为特化会反过来影响 int；「必须写在类内」不对 —— 函数模板特化写在命名空间作用域，且必须在**首次使用之前**声明。\n★ 特化不是重载：它没有自己的模板参数，用 `template <>` 起头，必须精确匹配某个具体类型。偏特化（部分特化）只支持类模板，函数模板只能全特化 —— 想「部分特化」函数模板，改用重载。"
            }
        ]
    },
    {
        "title": "容量 4 的顺序栈压入 5 个元素",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "栈",
            "类模板",
            "判满"
        ],
        "choices": [
            "4321 1",
            "12345 0",
            "4321 0",
            "1234 1"
        ],
        "source_section": "第 09 讲 · 模板与群体数据",
        "statement_md": "顺序栈的 `top` 指向栈顶的**下一个空位**，容量为 4。连续压入 1~5（返回值未检查），再全部弹出并打印。输出是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\ntemplate <typename T>\nclass Stack {\n    T* d; int top, cap;\npublic:\n    explicit Stack(int c) : d(new T[c]), top(0), cap(c) {}\n    ~Stack() { delete[] d; }\n    bool push(const T& e) { if (top >= cap) return false; d[top++] = e; return true; }\n    bool pop(T& e) { if (top == 0) return false; e = d[--top]; return true; }\n    int size() const { return top; }\n};\n\nint main() {\n    Stack<int> s(4);\n    for (int i = 1; i <= 5; i++) s.push(i);      // 返回值没检查\n    int v;\n    while (s.pop(v)) cout << v;\n    cout << \" \" << s.size() << \"\\n\";\n}\n```",
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
                "explanation": "`push` 用 `d[top++] = e`（先存后移），`pop` 用 `e = d[--top]`（先移后取）—— 与教材顺序栈同构。\n容量 4 只能装 4 个：第 5 次 `push` 时 `top >= cap` 成立，返回 false，元素被**丢弃**（返回值没人查，所以静默丢数据）。随后 LIFO 弹出 4 3 2 1，栈空 → `size()` 为 0 → `4321 0`。\n「1234」把栈当成了队列；「4321 1」以为失败的那次也算占了位置；「12345」以为容量 4 能装 5 个。\n★ 这题真正的考点是「**返回值必须检查**」：`if (!st.push(x))` 才是完整写法，否则满栈时数据无声消失。"
            }
        ]
    },
    {
        "title": "带 swapped 标志的冒泡排序趟数与比较次数",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "冒泡排序",
            "提前结束",
            "比较次数"
        ],
        "choices": [
            "1 4",
            "2 7",
            "4 7",
            "2 10"
        ],
        "source_section": "第 09 讲 · 模板与群体数据",
        "statement_md": "对 `{1, 2, 3, 5, 4}` 做带 `swapped` 标志的冒泡排序（一趟无交换就提前结束），下面程序输出「实际趟数 比较次数」，结果是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nint main() {\n    int a[] = {1, 2, 3, 5, 4}, n = 5, pass = 0, cmp = 0;\n    for (int i = 0; i < n - 1; i++) {\n        bool swapped = false;\n        for (int j = 0; j < n - 1 - i; j++) {\n            cmp++;\n            if (a[j] > a[j + 1]) { int t = a[j]; a[j] = a[j + 1]; a[j + 1] = t; swapped = true; }\n        }\n        pass++;\n        if (!swapped) break;\n    }\n    cout << pass << \" \" << cmp << \"\\n\";\n}\n```",
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
                "explanation": "第 1 趟：比较 4 次（1-2、2-3、3-5、5-4），只交换最后那一对 → `1 2 3 4 5`，`swapped = true`；\n第 2 趟：比较 3 次，一次都没换 → 提前 `break`。合计 **2 趟 7 次比较**。\n「4 7」把趟数算成固定的 n-1；「2 10」以为提前结束后仍要把剩余比较算进去（4+3+2+1=10 是不加标志的总次数）；「1 4」以为第一趟之后就结束了（第一趟明明有交换）。\n★ 冒泡的三个卖点：稳定、可提前结束、每趟把当前最大值「冒」到末尾。最坏（逆序）n-1 趟、n(n-1)/2 次比较；最好（已有序）1 趟 n-1 次比较 —— 这也是它比选择排序「聪明」的地方。"
            }
        ]
    },
    {
        "title": "折半查找循环条件漏掉等号的后果",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "折半查找",
            "边界条件",
            "陷阱"
        ],
        "choices": [
            "访问 a[-1]，数组越界",
            "只是多比较一次，结果仍然正确",
            "区间只剩一个元素时循环直接退出，该元素永远查不到",
            "区间不再收缩，陷入死循环"
        ],
        "source_section": "第 09 讲 · 模板与群体数据",
        "statement_md": "折半查找的循环写成 `while (low < high)`（漏了 `=`），其余（`mid` 计算、`low = mid + 1`、`high = mid - 1`）都写对了。会出什么问题？",
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
                "explanation": "`low < high` 意味着**当 `low == high` 时不再进循环**，可此时区间里明明还剩一个元素没比较。后果是：查 `a[0]` 或 `a[n-1]`（最后一步必然收缩到单元素区间）时会直接判失败返回 -1。\n「死循环」是 `low = mid` / `high = mid`（漏 ±1）的后果 —— 区间不收缩，mid 原地踏步；「数组越界」是把内层条件顺序写反（`a[j] > t && j >= 0`）那一类错误；「只是多比较一次」正好说反：是**少**比了一次，导致漏判。\n★ 折半的三个必错点：循环条件 `low <= high`、`low = mid + 1`、`high = mid - 1`，外加「查找前必须有序」这一条前提。"
            }
        ]
    },
    {
        "title": "折半查找在八元素表上的比较次数",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "折半查找",
            "比较次数"
        ],
        "choices": [
            "4",
            "7",
            "3",
            "2"
        ],
        "source_section": "第 09 讲 · 模板与群体数据",
        "statement_md": "在有序表 `1 3 5 7 9 11 13 15` 上折半查找 `13`，下面程序输出的比较次数是多少？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nint main() {\n    int a[] = {1, 3, 5, 7, 9, 11, 13, 15};\n    int n = 8, key = 13, cmp = 0;\n    int low = 0, high = n - 1, pos = -1;\n    while (low <= high) {\n        int mid = (low + high) / 2;\n        cmp++;\n        if (a[mid] == key) { pos = mid; break; }\n        else if (a[mid] < key) low = mid + 1;\n        else high = mid - 1;\n    }\n    cout << cmp << \"\\n\";\n}\n```",
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
                "explanation": "`low=0, high=7`：第 1 次 `mid=3`（值 7）< 13 → 去右半；第 2 次 `mid=5`（值 11）< 13 → 继续右移；第 3 次 `mid=6`（值 13）命中。共 **3** 次。\n「2」以为 8 个元素正好 log₂8=3 但要先命中一次，实际也是 3 —— 总之不是 2；「4」把判定树高度算成 ⌈log₂9⌉ 且多算一层；「7」是**顺序查找**的比较次数（13 在下标 6，从头比 7 次）。\n★ 折半的三处边界一个都不能错：`low <= high`、`low = mid + 1`、`high = mid - 1`。"
            }
        ]
    },
    {
        "title": "选择排序的交换次数",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "选择排序",
            "交换次数"
        ],
        "choices": [
            "4",
            "5",
            "3",
            "2"
        ],
        "source_section": "第 09 讲 · 模板与群体数据",
        "statement_md": "对 `{5, 2, 4, 1, 3}` 做选择排序（每轮先记最小元素下标，`k != i` 时才交换），下面程序输出的交换次数是多少？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nint main() {\n    int a[] = {5, 2, 4, 1, 3}, n = 5, sw = 0;\n    for (int i = 0; i < n - 1; i++) {\n        int k = i;\n        for (int j = i + 1; j < n; j++) if (a[j] < a[k]) k = j;\n        if (k != i) { int t = a[i]; a[i] = a[k]; a[k] = t; sw++; }\n    }\n    cout << sw << \"\\n\";\n}\n```",
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
                "explanation": "第 1 轮最小是 1（下标 3）→ 交换，`1 2 4 5 3`（第 1 次）；\n第 2 轮最小已是 a[1]=2、`k == i` → **不交换**；\n第 3 轮最小是 3（下标 4）→ 交换，`1 2 3 5 4`（第 2 次）；\n第 4 轮最小是 4（下标 4）→ 交换，`1 2 3 4 5`（第 3 次）。\n「2」漏掉了最后一轮；「4」把第 2 轮那次 `k == i` 的空轮也算成交换；「5」按「每轮必换」算（n-1 轮 → 4 次，也不该是 5）。\n★ 选择排序的卖点正是**交换次数最少**（最多 n-1 次），比较次数仍固定 n(n-1)/2。"
            }
        ]
    },
    {
        "title": "类模板的静态成员在各实例化之间是否共享",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "类模板",
            "静态成员",
            "实例化"
        ],
        "choices": [
            "2 1",
            "3 3",
            "1 1",
            "编译错误：类模板不能有静态成员"
        ],
        "source_section": "第 09 讲 · 模板与群体数据",
        "statement_md": "类模板 `Box<T>` 有一个静态成员 `cnt`，构造时自增。先建两个 `Box<int>`、再建一个 `Box<double>`，然后分别打印两个实例化的 `cnt`。输出是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\ntemplate <typename T> struct Box { static int cnt; Box() { cnt++; } };\ntemplate <typename T> int Box<T>::cnt = 0;\n\nint main() {\n    Box<int> a, b;\n    Box<double> c;\n    cout << Box<int>::cnt << \" \" << Box<double>::cnt << \"\\n\";\n}\n```",
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
                "explanation": "`Box<int>` 与 `Box<double>` 是编译器生成的**两个互不相干的类**，各有各的静态成员 —— 所以是 2 和 1，而不是 3 和 3。\n「3 3」正是「以为所有实例化共享一份 static」的典型错；「1 1」以为静态成员没被构造影响；「不能有静态成员」不对，类模板完全可以有 static，只是要写两处 `template <typename T>`（类内声明 + 类外的 `template <typename T> int Box<T>::cnt = 0;` 定义）。\n★ 这条也解释了为什么「用静态成员做全局计数器」在模板里要小心：`Box<int>::cnt` 与 `Box<double>::cnt` 是两个变量，想在所有实例化间共享，得把计数器放到**非模板的基类**里（或独立的全局对象）。"
            }
        ]
    },
    {
        "title": "折半查找不存在的键时的比较次数",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "折半查找",
            "失败情形",
            "比较次数"
        ],
        "choices": [
            "-1 8",
            "-1 3",
            "-1 4",
            "2 3"
        ],
        "source_section": "第 09 讲 · 模板与群体数据",
        "statement_md": "在 `1 3 5 7 9 11 13 15` 上折半查找 `6`（表中没有 6）。下面程序输出「返回位置 比较次数」，结果是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nint main() {\n    int a[] = {1, 3, 5, 7, 9, 11, 13, 15};\n    int n = 8, key = 6, cmp = 0, low = 0, high = n - 1, pos = -1;\n    while (low <= high) {\n        int mid = (low + high) / 2;\n        cmp++;\n        if (a[mid] == key) { pos = mid; break; }\n        else if (a[mid] < key) low = mid + 1;\n        else high = mid - 1;\n    }\n    cout << pos << \" \" << cmp << \"\\n\";\n}\n```",
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
                "explanation": "`mid` 的走位：第 1 次 `mid=3`（值 7）> 6 → `high=2`；第 2 次 `mid=1`（值 3）< 6 → `low=2`；第 3 次 `mid=2`（值 5）< 6 → `low=3`，此时 `low > high` 退出。共 **3** 次比较，`pos` 仍是 **-1**。\n「-1 4」多算一轮（把退出前那次判断也当成比较）；「2 3」以为失败会返回插入点 —— 折半查找只答「在不在」，要插入点得用 `lower_bound`；「-1 8」是顺序查找的比较次数。\n★ 失败时比较次数也是 ⌈log₂(n+1)⌉ 量级：8 个元素的判定树高 4，最多 4 次就够（这题恰好 3 次落空）。这正说明 O(log n) —— 每比一次砍掉一半候选。"
            }
        ]
    },
    {
        "title": "函数模板与类模板的推导差异及实现放置",
        "subject": "cpp",
        "line": "text",
        "question_type": "short_answer",
        "difficulty": 4,
        "total_score": 12,
        "tags": [
            "函数模板",
            "类模板",
            "头文件",
            "简答"
        ],
        "choices": [],
        "source_section": "第 09 讲 · 模板与群体数据",
        "statement_md": "**简答题**：函数模板与类模板在使用时，对「类型参数怎么定」有什么不同要求？为什么类模板的成员函数定义通常必须写在头文件里？",
        "input_format": "",
        "output_format": "一句话作答（不要抄题目、不要写代码）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "函数模板可以由实参推导类型参数，冲突时可显式指定；类模板必须显式给出类型实参。类模板的实例化发生在使用它的编译单元，编译器必须看到完整定义，所以声明和实现要放同一个头文件",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|函数模板可以由实参推导类型参数，冲突时可显式指定；类模板必须显式给出类型实参。类模板的实例化发生在使用它的编译单元，编译器必须看到完整定义，所以声明和实现要放同一个头文件\n|函数模板能靠实参推导 T，推导冲突则编译失败，需写 myMax<double>；类模板必须写 Box<int>。成员定义要放头文件，因为模板只有在实例化时才生成代码，其他编译单元需要看到定义\n|函数模板可推导、类模板必须显式指定类型参数；模板不是普通函数/类，不实例化就不生成代码，所以实现必须随声明一起放在头文件里供各编译单元实例化\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**推导**：函数模板的 `T` 可以由实参类型推出来（`myMax(3.5, 2.5)` → `T = double`），两个实参推出不同 `T` 就编译失败，此时用显式指定 `myMax<double>(...)` 钉死；类模板**不能推导**（C++14 语境），必须写全 `Array<int>`，因为 `Array` 本身只是图纸、不是类型。\n**为什么放头文件**：模板不实例化就不生成任何代码 —— 编译器在**用到**它的那个编译单元里，必须同时看到声明和定义才能按具体类型生成机器码。若把定义放进 .cpp，别的 .cpp 只看到声明，链接时就会 `undefined reference`。\n对比普通函数/类：它们可以「头文件放声明、.cpp 放实现」，因为编译期只需要声明、链接期再去找那唯一一份实现。\n★ 代价也要知道：模板把编译期工作推给使用者，编译变慢、报错信息变长；这也是 C++20 modules 想解决的问题。"
            }
        ]
    },
    {
        "title": "迭代器区间右端点的含义",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "迭代器",
            "区间"
        ],
        "choices": [
            "最后一个元素的下一个位置（不是元素）",
            "最后一个元素本身",
            "第一个元素的前一个位置",
            "容器的首元素"
        ],
        "source_section": "第 10 讲 · 泛型程序设计与STL",
        "statement_md": "STL 算法接受的迭代器区间是左闭右开 `[first, last)`。`last`（即 `c.end()`）指向的是：",
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
                "explanation": "`end()` 是**尾后位置**，不指向任何元素，解引用它是未定义行为。\n左闭右开带来三个好处：`end() - begin()` 直接就是元素个数；空容器 `begin() == end()` 自然成立；`for (it = b; it != e; ++it)` 不用为空区间写特例。\n「最后一个元素本身」是最常见的误记（那要用 `end() - 1` 或 `--end()`）；「第一个元素的前一个位置」把 `--begin()` 这种非法操作当成了 `end()`。"
            }
        ]
    },
    {
        "title": "链表迭代器属于哪一类",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "迭代器",
            "list"
        ],
        "choices": [
            "双向迭代器",
            "随机访问迭代器",
            "前向迭代器",
            "输入迭代器"
        ],
        "source_section": "第 10 讲 · 泛型程序设计与STL",
        "statement_md": "`std::list` 的迭代器属于五类迭代器中的哪一类？",
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
                "explanation": "`list` 是双向链表，迭代器支持 `++` 和 `--`，但**不支持 `it + n`、`it1 - it2`、`<` 比较**，所以是双向迭代器。\n五类能力递增：输入/输出 → 前向（`forward_list`）→ 双向（`list`/`set`/`map`）→ 随机访问（`vector`/`deque`/`array`）。\n「随机访问」是 `vector` 的待遇；正因为 `list` 没有，`std::sort` 用不了它（`std::sort` 要求随机访问），得改用成员函数 `lst.sort()`。"
            }
        ]
    },
    {
        "title": "map 下标访问不存在的键",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "map",
            "operator[]",
            "陷阱"
        ],
        "choices": [
            "1 2",
            "编译错误",
            "0 2",
            "0 1"
        ],
        "source_section": "第 10 讲 · 泛型程序设计与STL",
        "statement_md": "下面程序的输出是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nint main() {\n    map<string, int> m;\n    m[\"a\"] = 1;\n    cout << m[\"b\"] << \" \" << m.size() << \"\\n\";\n}\n```",
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
                "explanation": "`map::operator[]` 的语义是「键不存在就**插入**一个值初始化的元素，再返回它的引用」，所以 `m[\"b\"]` 这一句**只是读**，容器却从 1 个元素变成 2 个 → 输出 `0 2`。\n「0 1」以为读不会改变容器；「1 2」以为默认值是 1；「编译错误」不对 —— `int` 值初始化就是 0，完全合法。\n★ 判存在性一律用 `find(k) != m.end()` 或 `m.count(k)`，它们只查不插。唯一常见例外是词频统计 `freq[w]++` —— 那里「不存在就插 0」正好是想要的。"
            }
        ]
    },
    {
        "title": "值捕获是创建时的快照",
        "subject": "cpp",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 2,
        "total_score": 8,
        "tags": [
            "lambda",
            "捕获"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 10 讲 · 泛型程序设计与STL",
        "statement_md": "lambda 的值捕获 `[x]` 会在**每次调用时**重新复制一份当时的 `x`，所以外部改过 `x` 之后，再调用就能看到新值。",
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
                "explanation": "错。值捕获发生在 **lambda 创建那一刻**，只复制一次，之后无论外部怎么改，lambda 里看到的永远是那份快照。\n实测：`int base = 100; auto f = [base](int x){ return x + base; };` 之后把 `base` 改成 200，`f(1)` 仍然是 101。\n想看最新值要用**引用捕获** `[&base]`；反过来，如果 lambda 活得比原变量久（异步回调、存进容器），引用捕获就成了悬垂引用，那时必须值捕获。"
            }
        ]
    },
    {
        "title": "关于顺序容器与关联容器的正确说法",
        "subject": "cpp",
        "line": "text",
        "question_type": "multiple_choice",
        "difficulty": 2,
        "total_score": 14,
        "tags": [
            "容器",
            "迭代器",
            "多选"
        ],
        "choices": [
            "deque 在两端插入删除都是 O(1)",
            "set 的遍历结果按键升序排列",
            "list 的迭代器支持 it + n",
            "vector 提供随机访问迭代器"
        ],
        "source_section": "第 10 讲 · 泛型程序设计与STL",
        "statement_md": "关于 STL 容器，下列说法**正确**的有：\n\n**多选题**：正确选项不止一个，点选切换，再次点击可取消。",
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
                "explanation": "四条里只有「list 的迭代器支持 it + n」是错的：`list` 是双向迭代器，只有 `++`/`--`，写 `lst.begin() + 1` 直接编译错。\n其余三条都对：`vector` 是连续内存，迭代器支持 `it + n`、`it1 - it2`；`deque` 是分段连续，两头插删 O(1)（所以 `stack`/`queue` 默认拿它当底层）；`set`/`map` 是红黑树，中序遍历天然升序。\n★ 顺带记：`vector` 中间/头部插入是 O(n)，`list` 任意位置插入是 O(1) 但**先要 O(n) 找到位置**。"
            }
        ]
    },
    {
        "title": "无序关联容器提供的迭代器类别",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "迭代器",
            "unordered_map",
            "迭代器类别"
        ],
        "choices": [
            "输入迭代器",
            "前向迭代器",
            "双向迭代器",
            "随机访问迭代器"
        ],
        "source_section": "第 10 讲 · 泛型程序设计与STL",
        "statement_md": "`std::unordered_map` 的迭代器属于五类迭代器中的哪一类？",
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
                "explanation": "`unordered_map`/`unordered_set` 底层是「桶数组 + 单链表」，迭代器只能 `++` 单向前进，**不支持 `--`**（所以不是双向），更不支持 `it + n`、`it1 - it2`（不是随机访问）。\n对照记忆：`forward_list`、`unordered_*` → 前向；`list`、`set`、`map` → 双向；`vector`、`deque`、`array` → 随机访问。\n★ 原则是「容器只提供能兑现全部功能的最弱一档」—— 哈希表本来就没有「前一个」的概念，给双向能力既做不到也没意义。这也是为什么 `unordered_map` 上写 `--it` 会编译错，而 `sort` 对 `list`/`map` 也都用不了。"
            }
        ]
    },
    {
        "title": "左闭右开区间的元素个数与末元素",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "迭代器",
            "左闭右开",
            "vector"
        ],
        "choices": [
            "5 40 10",
            "4 50 10",
            "5 50 10",
            "6 50 10"
        ],
        "source_section": "第 10 讲 · 泛型程序设计与STL",
        "statement_md": "下面程序依次输出「区间长度、末元素、首元素」，结果是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nint main() {\n    vector<int> v = {10, 20, 30, 40, 50};\n    cout << (v.end() - v.begin()) << \" \" << *(v.end() - 1) << \" \" << *v.begin() << \"\\n\";\n}\n```",
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
                "explanation": "`end()` 是**尾后位置**（最后一个元素的下一个位置），所以 `end - begin` = 元素个数 **5**；末元素要 `*(end - 1)` = **50**；`*begin` = **10**。\n「6」是以为 end 也指向一个元素；「5 40 10」把末元素错算成倒数第二个；「4」是以为 `end-begin` 要减一。\n★ 三个好处一次说完：① `end - begin` 直接是 size，不用 ±1；② 空容器 `begin() == end()` 自然成立，空区间不用特判；③ 循环写 `it != end()`，区间为空时一次都不进。**解引用 `end()` 是未定义行为。**"
            }
        ]
    },
    {
        "title": "优先队列默认的出队顺序",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "priority_queue",
            "容器适配器"
        ],
        "choices": [
            "9 1 3 5 7",
            "9 7 5 3 1",
            "1 3 5 7 9",
            "3 9 1 7 5"
        ],
        "source_section": "第 10 讲 · 泛型程序设计与STL",
        "statement_md": "下面程序的输出是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nint main() {\n    priority_queue<int> pq;\n    int a[] = {3, 9, 1, 7, 5};\n    for (int x : a) pq.push(x);\n    while (!pq.empty()) {\n        cout << pq.top();\n        if (pq.size() > 1) cout << \" \";\n        pq.pop();\n    }\n    cout << \"\\n\";\n}\n```",
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
                "explanation": "`priority_queue<int>` 默认用 `less<int>` 比较，构成**大根堆**，`top()` 永远是当前最大值，所以出队顺序是降序 `9 7 5 3 1`。\n「1 3 5 7 9」是小根堆，要写 `priority_queue<int, vector<int>, greater<int>>`；「3 9 1 7 5」是原输入顺序（那是普通队列）；「9 1 3 5 7」既不是堆序也不是插入序。\n★ 三个模板参数依次是：元素类型、底层容器、比较器 —— 第三个决定大根还是小根。"
            }
        ]
    },
    {
        "title": "下界查找返回的插入位置",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "lower_bound",
            "二分"
        ],
        "choices": [
            "4",
            "6",
            "7",
            "5"
        ],
        "source_section": "第 10 讲 · 泛型程序设计与STL",
        "statement_md": "下面程序的输出是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nint main() {\n    vector<int> v = {4, 8, 15, 16, 23, 42, 8};\n    sort(v.begin(), v.end());\n    cout << lower_bound(v.begin(), v.end(), 17) - v.begin() << \"\\n\";\n}\n```",
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
                "explanation": "排序后是 `4 8 8 15 16 23 42`（7 个元素，下标 0~6）。`lower_bound(17)` 返回**第一个 ≥ 17** 的位置，也就是 23 所在的**下标 5**。\n「4」是 16 的下标（那是 `lower_bound(16)`，或者把 17 当成 ≤ 的边界）；「6」是 23 后面一位（误把 lower 当 upper 再加一）；「7」是 `end()`（以为 17 不存在就返回末尾）。\n★ `upper_bound(17)` 与它相同（17 不存在时两者相等）；`lower_bound(16)=4`、`upper_bound(16)=5`，两者相减正好是 16 的出现次数。二分家族的前提是区间**已排序**，忘了 sort 不会报错但结果毫无意义。"
            }
        ]
    },
    {
        "title": "accumulate 初值类型决定结果类型",
        "subject": "cpp",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 3,
        "total_score": 12,
        "tags": [
            "accumulate",
            "类型"
        ],
        "choices": [],
        "source_section": "第 10 讲 · 泛型程序设计与STL",
        "statement_md": "下面程序的输出是多少？（只写数值）\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nint main() {\n    vector<double> v = {1.5, 2.5, 3.5};\n    cout << accumulate(v.begin(), v.end(), 0) << \"\\n\";\n}\n```",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "6",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|6\n|6.0\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`accumulate` 的累加器类型由**第三个参数（初值）**决定：这里写的是 `0`（`int`），于是每一步都按 `int` 累加、每加一项就截断一次：0+1.5→1、1+2.5→3、3+3.5→6，输出 6。\n把初值写成 `0.0` 才是 7.5 —— 这就是讲义反复强调「初值写 0.0」的原因。\n★ 同样的坑也出现在「int 初值求大数和」上：会溢出，得用 `0LL`。"
            }
        ]
    },
    {
        "title": "值捕获与引用捕获的对照输出",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "lambda",
            "捕获"
        ],
        "choices": [
            "100 200",
            "101 201",
            "201 201",
            "101 101"
        ],
        "source_section": "第 10 讲 · 泛型程序设计与STL",
        "statement_md": "下面程序的输出是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nint main() {\n    int base = 100;\n    auto f = [base](int x) { return x + base; };\n    base = 200;\n    cout << f(1) << \" \" << [&base](int x) { return x + base; }(1) << \"\\n\";\n}\n```",
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
                "explanation": "`f` 是**值捕获**：创建时就把 100 复制进去了，之后 `base = 200` 与它无关 → `f(1) = 101`；后面那个 lambda 是**引用捕获** `[&base]`，读的是外面的本体 → `1 + 200 = 201`。\n「201 201」以为值捕获能看到最新值；「101 101」以为引用捕获也是快照；「100 200」是直接打印 `base` 而忘了加实参 1。\n★ 一句话记：**值捕获是快照，引用捕获是本体**。跨生存期（异步回调）只能用值捕获。"
            }
        ]
    },
    {
        "title": "直接对 map 迭代能否按值排序",
        "subject": "cpp",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 3,
        "total_score": 8,
        "tags": [
            "map",
            "排序",
            "迭代器失效"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 10 讲 · 泛型程序设计与STL",
        "statement_md": "`map` 的迭代器按关键字升序遍历。只要在遍历时用 `sort` 按 `second` 排一遍，就能让 `map` 变成按值有序。",
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
                "explanation": "错，而且错两层：\n① `map` 是红黑树，元素位置由**键**决定，迭代器顺序是树的**中序**，外部改不了；想「按值排」本质上是要换一种组织方式，树做不到。\n② `std::sort` 要求**随机访问迭代器**，而 `map` 只给双向迭代器 —— 写 `sort(m.begin(), m.end(), ...)` 直接编译错（不是排序结果不对，是根本编不过）。\n正确姿势：把 `pair` 拷进 `vector`，再对 vector `sort`（要保留同值原序用 `stable_sort`）。\n★ 一句话：**关联容器的顺序是它的定义，不是它的属性**。`map` 有序是「按键」，`set` 有序是「按元素自身」，都不提供「换个维度重排」的接口。"
            }
        ]
    },
    {
        "title": "mutable 初始化捕获的计数器调用结果",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "lambda",
            "捕获",
            "mutable"
        ],
        "choices": [
            "111 3",
            "123 3",
            "编译错误：mutable 不能用于 lambda",
            "123 0"
        ],
        "source_section": "第 10 讲 · 泛型程序设计与STL",
        "statement_md": "`[n = 0]` 是 C++14 的初始化捕获（lambda 自带一个成员 `n`）。连调三次，输出是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nint main() {\n    int calls = 0;\n    auto c = [n = 0]() mutable { return ++n; };\n    int x = c(), y = c(), z = c();\n    cout << x << y << z << \" \" << calls << \"\\n\";\n}\n```",
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
                "explanation": "lambda 本质是一个**匿名函数对象**：`[n = 0]` 相当于给它加了一个成员 `int n = 0;`，`mutable` 则是把 `operator()` 的 const 去掉，允许修改这个成员。于是 `n` 的**状态跨调用保留** → 1、2、3。\n外面那个 `calls` **根本没被捕获**（捕获列表里没有它），所以始终是 0 —— 这是本题的第二个坑。\n「111 3」既以为 `n` 每次都重置、又以为 `calls` 被改了；「123 3」以为 `calls` 被引用捕获；「mutable 不能用于 lambda」不对：不加 `mutable` 反而是**编译错**（`operator()` 默认 const，不能改值捕获的副本）。\n★ 记忆：值捕获 = 对象里的成员副本（快照 + 可跨调用保持）；引用捕获 = 外部变量的别名；`mutable` 只解开「能不能改副本」这一道锁。"
            }
        ]
    },
    {
        "title": "set 构造后的元素个数与顺序",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "set",
            "去重",
            "有序"
        ],
        "choices": [
            "4:1359 1 0",
            "6:535139 1 0",
            "4:1359 2 0",
            "6:1359 1 0"
        ],
        "source_section": "第 10 讲 · 泛型程序设计与STL",
        "statement_md": "用 6 个整数 `5 3 5 1 3 9` 构造 `set<int>`，然后输出「元素个数:所有元素 count(3) count(7)」。结果是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nint main() {\n    int a[] = {5, 3, 5, 1, 3, 9};\n    set<int> s(a, a + 6);\n    cout << s.size() << \":\";\n    for (int x : s) cout << x;\n    cout << \" \" << s.count(3) << \" \" << s.count(7) << \"\\n\";\n}\n```",
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
                "explanation": "`set` 是红黑树：**自动去重 + 自动升序**，6 个输入只剩 4 个元素，遍历即 `1359`。`count` 只查不插，所以 `count(3)=1`（去重后最多一个）、`count(7)=0`。\n「6:535139」是**没去重也没排序**（那是把 set 当成了 vector）；「count(3)=2」以为 count 会数原始输入里的重复次数（那要用 `multiset`）；「6:1359」个数与内容自相矛盾。\n★ `set` 的两个推论：① 插入重复元素是**无操作**（`insert` 返回 `{迭代器, false}`）；② 想保留重复用 `multiset`，想去重但不要顺序用 `unordered_set`。"
            }
        ]
    },
    {
        "title": "erase 返回值的正确用法",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "迭代器失效",
            "erase",
            "vector"
        ],
        "choices": [
            "123",
            "135",
            "12345",
            "1345"
        ],
        "source_section": "第 10 讲 · 泛型程序设计与STL",
        "statement_md": "下面程序删除 `vector` 中所有偶数，输出是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nint main() {\n    vector<int> v = {1, 2, 3, 4, 5};\n    for (auto it = v.begin(); it != v.end();) {\n        if (*it % 2 == 0) it = v.erase(it);\n        else ++it;\n    }\n    for (int x : v) cout << x;\n    cout << \"\\n\";\n}\n```",
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
                "explanation": "`erase(it)` 返回**被删元素之后那个位置的有效迭代器**，循环里用 `it = v.erase(it)` 接住它，不删时才手动 `++it` —— 这是删除遍历的唯一标准姿势，所以干净地删掉了 2 和 4 → `135`。\n「1345」正是「erase 之后还 `++it`」的典型表现：`it` 已失效，`++` 后**跳过**了前移过来的 4，4 逃过删除。这种错常常不崩溃，比崩溃更危险。\n「12345」是完全没删；「123」只删了尾部。\n★ 记住：**erase 之后旧迭代器一个都别用，用返回值**。"
            }
        ]
    },
    {
        "title": "vector 扩容后旧迭代器的有效性",
        "subject": "cpp",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 4,
        "total_score": 8,
        "tags": [
            "迭代器失效",
            "vector",
            "扩容"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 10 讲 · 泛型程序设计与STL",
        "statement_md": "`vector` 在 `push_back` 过程中发生扩容（重新分配更大的连续内存）后，先前保存的迭代器全部失效。",
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
                "explanation": "对。`vector` 元素必须连续存放，容量不够时只能申请一块更大的内存、把元素搬过去、释放旧的 —— 旧迭代器还指着**已经被释放的那块内存**，全部悬空。\n这也是「循环里 `push_back` 之后不要再用之前的迭代器」的原因；要么每次重新取 `begin()`，要么改用下标。\n对照记忆：`list`/`set`/`map` 的插入不会让其他元素的迭代器失效（结点各自独立）；`vector`/`deque` 的插入则可能让插入点之后（甚至全部）失效。"
            }
        ]
    },
    {
        "title": "遍历 map 时删除偶数键的正确写法",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "map",
            "erase",
            "迭代器失效"
        ],
        "choices": [
            "2 135",
            "3 123",
            "3 135",
            "5 12345"
        ],
        "source_section": "第 10 讲 · 泛型程序设计与STL",
        "statement_md": "下面程序删掉所有偶数键，再输出「剩余个数 剩余键」。结果是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nint main() {\n    map<int, int> m = {{1, 10}, {2, 20}, {3, 30}, {4, 40}, {5, 50}};\n    for (auto it = m.begin(); it != m.end();) {\n        if (it->first % 2 == 0) it = m.erase(it);\n        else ++it;\n    }\n    cout << m.size() << \" \";\n    for (auto& p : m) cout << p.first;\n    cout << \"\\n\";\n}\n```",
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
                "explanation": "`erase(it)` 返回**被删元素之后那个位置的有效迭代器**，循环用 `it = m.erase(it)` 接住它，不删时才 `++it` —— 这是关联容器删除遍历的标准姿势，删掉 2 和 4 后剩 `1 3 5`。\n「5 12345」是完全没删（条件写错）；「2 135」个数与内容自相矛盾；「3 123」删错了元素。\n★ 反面写法是 `m.erase(it); ++it;` —— `it` 已失效，`++` 是未定义行为，在 `map` 上常表现为崩溃或跳元素。C++11 起 `erase` 才返回下一个迭代器（老标准返回 void，所以老代码只能用 `it = m.erase(it++)` 这种写法）。\n★ 对照：`list`/`set`/`map` 删除只让**被删元素**的迭代器失效；`vector`/`deque` 删除会让删除点**及之后**的全部失效。"
            }
        ]
    },
    {
        "title": "STL 常用算法的时间复杂度",
        "subject": "cpp",
        "line": "text",
        "question_type": "multiple_choice",
        "difficulty": 4,
        "total_score": 14,
        "tags": [
            "算法",
            "复杂度",
            "多选"
        ],
        "choices": [
            "std::binary_search 是 O(log n)，前提是区间已排序",
            "std::accumulate 是 O(log n)",
            "std::find 是 O(n)",
            "std::sort 平均 O(n log n)"
        ],
        "source_section": "第 10 讲 · 泛型程序设计与STL",
        "statement_md": "在含 n 个元素的区间上，关于下列算法复杂度的说法**正确**的有：\n\n**多选题**：正确选项不止一个，点选切换，再次点击可取消。",
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
                "explanation": "四条里只有「std::accumulate 是 O(log n)」是错的：`accumulate` 是单遍累加，O(n)，`<numeric>` 里的算法基本都是 O(n)。\n其余三条都对：`find`/`count` 是顺序扫描 O(n)；`sort` 是内省排序，平均与最坏都是 O(n log n)；`binary_search`/`lower_bound`/`upper_bound` 是二分，O(log n)，但**必须作用在已排序区间**上，否则不报错、结果毫无意义。\n★ 再补两条常考的：`list::sort()` 是 O(n log n)（链表归并），而 `std::sort` 不能用于 list；`priority_queue` 的 `push`/`pop` 是 O(log n)、`top` 是 O(1)。"
            }
        ]
    },
    {
        "title": "输出流默认打开模式会不会清空文件",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "ofstream",
            "打开模式"
        ],
        "choices": [
            "OLD 与 NEW 各占一行",
            "打开失败，文件内容不变",
            "只有 NEW，原内容在打开那一刻就被清空了",
            "OLD 后面接着 NEW"
        ],
        "source_section": "第 11 讲 · 流类库与输入输出",
        "statement_md": "`a.txt` 里原有内容 `OLD`。执行下面两行之后，`a.txt` 的内容是？\n\n```cpp\nofstream out(\"a.txt\");   // 未写第二个参数\nout << \"NEW\";\n```",
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
                "explanation": "`ofstream out(\"a.txt\")` 等价于 `ofstream out(\"a.txt\", ios::out)`，而 `ios::out` **打开的一瞬间就把文件截断（清空）**，哪怕你一个字都还没写。\n想保留旧内容必须用 `ios::app`（追加，每次写前自动定位到文件尾）。\n「OLD 后面接着 NEW」就是把 out 当成了追加；「各占一行」同上；「打开失败」只在路径/权限有问题时发生，这里不是。\n★ 打开后顺手 `if (!out) { ... }` 判一下成败，是最省事的防御。"
            }
        ]
    },
    {
        "title": "setw 的作用范围",
        "subject": "cpp",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 1,
        "total_score": 8,
        "tags": [
            "操纵符",
            "setw"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 11 讲 · 流类库与输入输出",
        "statement_md": "`setw(8)` 设置之后，会对**其后所有**输出项持续生效，直到再次设置宽度。",
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
                "explanation": "错。`setw` 是**唯一**一次性的常用操纵符：只管紧跟着的那一个输出项，用完立刻恢复默认。\n所以 `cout << '[' << setw(6) << 42 << ']' << '[' << 42 << ']';` 输出 `[    42][42]` ——第二个 42 不再补空格。\n而 `fixed`、`setprecision`、`hex`、`left/right`、`setfill` 都是**粘性**的，改的是流的状态，会一直生效（这也是「后面所有浮点都变成 2 位小数」那个坑的来源）。"
            }
        ]
    },
    {
        "title": "宽度与定点小数操纵符的组合输出",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "操纵符",
            "setw",
            "setprecision"
        ],
        "choices": [
            "[   7]|2.6 3.5",
            "[    7]|2.6 3.5",
            "[7    ]|2.6 3.5",
            "[    7]|2.56 3.456"
        ],
        "source_section": "第 11 讲 · 流类库与输入输出",
        "statement_md": "下面程序的输出是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nint main() {\n    cout << '[' << setw(5) << 7 << \"]|\"\n         << fixed << setprecision(1) << 2.56 << \" \" << 3.456 << \"\\n\";\n}\n```",
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
                "explanation": "`setw(5)` 把 7 右对齐补到 5 列 → `[    7]`（4 个空格 + 7，默认右对齐）；`fixed << setprecision(1)` 之后按**小数位**输出且**粘性**：2.56→2.6、3.456→3.5 都只有一位小数。\n「[7    ]」把默认右对齐当成了左对齐（左对齐要写 `left`）；「2.56 3.456」漏了操纵符的作用；「[   7]」只补了 4 列，数错了宽度。\n★ `setw/setprecision/setfill` 需要 `<iomanip>`；`fixed/hex/left` 在 `<iostream>` 里就有。"
            }
        ]
    },
    {
        "title": "提取运算符后紧跟 getline 的结果",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "getline",
            "输入流",
            "陷阱"
        ],
        "choices": [
            "10|abc|",
            "10| |",
            "10|abc",
            "10||"
        ],
        "source_section": "第 11 讲 · 流类库与输入输出",
        "statement_md": "输入缓冲区的内容是 `10` 换行 `abc` 换行。下面程序的输出是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nint main() {\n    istringstream in(\"10\\nabc\\n\");\n    int n;\n    string s;\n    in >> n;\n    getline(in, s);\n    cout << n << \"|\" << s << \"|\\n\";\n}\n```",
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
                "explanation": "`in >> n` 按「跳过前导空白 → 读到下一个空白」工作，读完 10 后**停在换行符之前、并不消费它**；紧接着 `getline` 的任务恰恰是「读到换行为止」，于是一上来就撞上那个换行，立刻收工 → 得到空串，输出 `10||`。\n「10|abc|」是以为 `>>` 会吃掉换行；「10| |」是以为 getline 会读到一个空格。\n两种修法：① `in >> n; in.ignore();` 先丢掉一个字符；② 全程 `getline` 读整行，再用 `istringstream` 拆字段。"
            }
        ]
    },
    {
        "title": "追加写日志用哪个打开标志",
        "subject": "cpp",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "ofstream",
            "打开模式"
        ],
        "choices": [],
        "source_section": "第 11 讲 · 流类库与输入输出",
        "statement_md": "要在已有日志文件**末尾**追加内容、不破坏旧记录，`ofstream log(\"app.log\", ____);` 第二个参数该写什么？（写出这个打开标志）\n\n提示：app 是 append 的缩写。",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ios::app",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ios::app\n|std::ios::app\n|ios_base::app\n|ios::out|ios::app\n|ios::app|ios::out\n|std::ios::out|std::ios::app\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`ios::app`（append）是追加模式：每次写之前自动把写位置定位到文件尾，旧内容原样保留。\n对比 `ios::out`：打开即**清空**（trunc），写不写都先清。二者可以组合写 `ios::out | ios::app`，语义相同。\n★ `ios::app` 的实现就是「每次写前 seekp 到文件尾」，这也是 `tellp/seekp` 的一个实际用途。"
            }
        ]
    },
    {
        "title": "形参写成 ostream& 能接收哪些流对象",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "流类库",
            "继承体系",
            "ostream"
        ],
        "choices": [
            "cout",
            "ifstream in(\"a.txt\");",
            "ofstream out(\"a.txt\");",
            "ostringstream oss;"
        ],
        "source_section": "第 11 讲 · 流类库与输入输出",
        "statement_md": "函数 `void log(ostream& os, const string& msg)` 里只用了 `os << msg`。下列实参中，**不能**直接传给它的是：",
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
                "explanation": "能不能传，全看**继承体系**：`ostream` 的后代才能绑到 `ostream&` 上。\n`ofstream`、`ostringstream`、`cout` 都是 ostream 的后代（`ifstream` 不是，它是 istream 的后代；`fstream`/`stringstream` 同时继承 iostream，两者都能传）。\n★ 这正是流类库继承体系的实战价值：日志函数形参写 `ostream&`，同一份代码既能往屏幕写、也能往文件写、还能往字符串里写，一个字都不用改 ——第 7~8 章的继承与多态在标准库里就是这么用的。\n反过来，形参写 `istream&` 的函数只能接 `ifstream`/`istringstream`/`cin`。"
            }
        ]
    },
    {
        "title": "进制操纵符的连续切换",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "操纵符",
            "hex",
            "oct"
        ],
        "choices": [
            "ff 377 255",
            "255 255 255",
            "ff 255 377",
            "FF 377 255"
        ],
        "source_section": "第 11 讲 · 流类库与输入输出",
        "statement_md": "下面程序的输出是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nint main() { cout << hex << 255 << \" \" << oct << 255 << \" \" << dec << 255 << \"\\n\"; }\n```",
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
                "explanation": "`hex`、`oct`、`dec` 都是**粘性**操纵符（改的是流的状态），按顺序依次生效：255 的十六进制 `ff`、八进制 `377`、十进制 `255`。\n「255 255 255」以为操纵符只影响一个字面量；「ff 255 377」把后两个顺序弄反；「FF 377 255」以为十六进制默认大写（要 `uppercase` 才是 `FF`）。\n★ 两个后续影响要记住：① 进制状态会一直留着，输出完记得 `<< dec` 复位（否则后面的整数继续按十六进制打印）；② `showbase` 会加上 `0x`/`0` 前缀。`hex/oct/dec` 在 `<iostream>` 里就有，不需要 `<iomanip>`。"
            }
        ]
    },
    {
        "title": "填充字符与左右对齐的组合输出",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "操纵符",
            "setw",
            "setfill",
            "对齐"
        ],
        "choices": [
            "[42***][   7]",
            "[***42][   7]",
            "[**42][7   ]",
            "[***42][7   ]"
        ],
        "source_section": "第 11 讲 · 流类库与输入输出",
        "statement_md": "下面程序的输出是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nint main() {\n    cout << '[' << setw(5) << setfill('*') << 42 << ']'\n         << '[' << left << setw(4) << setfill(' ') << 7 << \"]\\n\";\n}\n```",
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
                "explanation": "`setw(5)` 把 42 补到 5 列，`setfill('*')` 把填充字符换成 `*`，默认右对齐 → `[***42]`；第二段 `left` 改左对齐、`setw(4)` 补到 4 列，但**填充字符仍是粘性的 `*`**，所以必须显式 `setfill(' ')` 才回到空格 → `[7   ]`。\n「[42***]」把右对齐当成左对齐；「[***42][   7]」忘了 `left`（默认右对齐）；「[**42]」把宽度算成 4。\n★ 粘性一览：`setfill`、`left/right`、`fixed`、`hex` 都粘；**只有 `setw` 是一次性的**。这也是「`setfill` 忘了改回来，后面所有输出都带星号」这个经典 bug 的来源。"
            }
        ]
    },
    {
        "title": "ios::ate 与 ios::trunc 的区别",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "打开模式",
            "ofstream",
            "文件定位"
        ],
        "choices": [
            "ios::ate 只能与 ios::in 合用，否则一定打开失败",
            "ios::ate 打开后定位到文件尾，但不截断文件；ios::trunc 会把文件清空",
            "ios::ate 会清空文件，ios::trunc 只是定位到尾部",
            "两者都会清空文件，只是打开后的读写位置不同"
        ],
        "source_section": "第 11 讲 · 流类库与输入输出",
        "statement_md": "关于文件打开模式，下列说法正确的是：",
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
                "explanation": "`ate`（at end）只负责**初始定位**：打开成功后读写指针在文件尾，内容一个字节都不动 ——常配 `ios::binary | ios::ate` 用 `tellg()` 量文件大小。\n`trunc`（truncate）才是**清空**；`ios::out` 在单独使用时隐含 `trunc`，这正是「`ofstream f(\"a.txt\")` 一打开旧内容就没了」的原因。\n`app`（append）与 ate 的区别要说清：`ate` 只在打开时定位一次，之后 `seekp` 到别处就能改写；`app` 则是**每次写之前**都自动定位到尾部，永远只能追加。\n「ate 会清空」正好把两者对调；「ate 只能配 in」不成立（openmode 组合是自由的）。"
            }
        ]
    },
    {
        "title": "读尽数据后流的状态位",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "流状态",
            "eof",
            "fail"
        ],
        "choices": [
            "3 1 1",
            "2 0 1",
            "2 1 1",
            "2 1 0"
        ],
        "source_section": "第 11 讲 · 流类库与输入输出",
        "statement_md": "下面程序依次输出「循环体执行次数、eof()、fail()」，结果是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nint main() {\n    istringstream s(\"11 22\");\n    int x, n = 0;\n    while (s >> x) n++;\n    cout << n << \" \" << s.eof() << \" \" << s.fail() << \"\\n\";\n}\n```",
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
                "explanation": "`\"11 22\"` 只够读两次，循环体执行 2 次；第三次 `s >> x` 提取失败，**eofbit 与 failbit 同时置位**（读到尾还没拿到数据），所以最后是 `2 1 1`。\n「2 1 0」以为 eof 不算失败 —— 只 eof（读完最后一个数据那一刻）时 `fail()` 确实还是 false、流仍可隐式转 true，但**再读一次失败**就会把 fail 也置上；「3 1 1」把失败那次也算进了循环；「2 0 1」以为读完没置 eof。\n★ 这也解释了为什么 `while (cin >> x)` 是最稳的读入循环：读取本身兼判尾，而 `while (!in.eof())` 会多跑一轮（eof 要等再读一次失败才置位）。"
            }
        ]
    },
    {
        "title": "Windows 文本模式与二进制模式的字节数",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "文本模式",
            "二进制模式",
            "换行符"
        ],
        "choices": [
            "4 4",
            "4 6",
            "6 6",
            "6 4"
        ],
        "source_section": "第 11 讲 · 流类库与输入输出",
        "statement_md": "在把 `\\n` 写成 `\\r\\n` 的平台上（如 Windows），把同一个字符串 `\"A\\nB\\n\"` 分别用**文本模式**和**二进制模式**写盘，两个文件各有几个字节？（下面程序输出「文本字节数 二进制字节数」）\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nint main() {\n    const char* ft = \"t.txt\";\n    const char* fb = \"b.txt\";\n    { ofstream t(ft); if (!t) { cout << \"ERRT\"; return 0; } t << \"A\\nB\\n\"; }\n    { ofstream b(fb, ios::binary); if (!b) { cout << \"ERRB\"; return 0; } b << \"A\\nB\\n\"; }\n    long st, sb;\n    { ifstream t(ft, ios::binary | ios::ate); st = (long)t.tellg(); }\n    { ifstream b(fb, ios::binary | ios::ate); sb = (long)b.tellg(); }\n    remove(ft); remove(fb);\n    cout << st << \" \" << sb << \"\\n\";\n}\n```",
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
                "explanation": "文本模式下每个 `\\n` 被**翻译**成 `\\r\\n`（0D 0A）两个字节：A(1) + 2 + B(1) + 2 = **6**；二进制模式原样写入，\\n 还是一个字节：1+1+1+1 = **4**。\n「4 4」是 Linux/Unix 上的结果（两种模式大小相同）—— 所以这道题的答案是**平台相关**的，题干才限定「把 \\n 翻译成 \\r\\n 的平台」；「4 6」把两种模式对调；「6 6」以为二进制也翻译。\n★ 结论：文本数据可用默认文本模式；结构体、图片等二进制数据**必须** `ios::binary`，否则中间出现 0D/0A 字节时会被翻译，数据直接毁掉。"
            }
        ]
    },
    {
        "title": "二进制读写用的强制类型转换",
        "subject": "cpp",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 3,
        "total_score": 12,
        "tags": [
            "二进制I/O",
            "类型转换"
        ],
        "choices": [],
        "source_section": "第 11 讲 · 流类库与输入输出",
        "statement_md": "二进制写入一条定长记录时写 `out.write(_____(char*)(&r), sizeof r);`，让编译器把对象内存**按字节**重新解释。横线上该填哪个强制类型转换运算符？（只写运算符名）\n\n提示：它的语义是「重新解释（re-interpret）这块内存」。",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "reinterpret_cast",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|reinterpret_cast\n|reinterpret_cast<>\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "填 `reinterpret_cast`：`reinterpret_cast<char*>(&r)` 的意思是「把 `r` 这块内存**按字节**重新解释成字符数组」，不做任何数值转换 —— 这正是二进制 I/O 要的。\n对比：`static_cast<char*>` 根本不允许（指针类型之间乱转会编译错），`const_cast` 只管 const，`dynamic_cast` 用于多态类型的向下转型。\n★ 配套要求：被写的结构体成员必须**定长**（`char name[16]` 行，`string` 不行 ——`string` 内部是指针，落盘的是地址，读回来是野指针）。"
            }
        ]
    },
    {
        "title": "带分隔符的 getline 与提取运算符接力",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "getline",
            "istringstream",
            "分隔符"
        ],
        "choices": [
            "[name][42][7]",
            "[name:][42][ 7]",
            "[name][0][ 7]",
            "[name][42][ 7]"
        ],
        "source_section": "第 11 讲 · 流类库与输入输出",
        "statement_md": "输入内容是 `name: 42 7` 加换行。下面程序输出三段带方括号的内容，结果是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nint main() {\n    istringstream in(\"name: 42 7\\n\");\n    string tag, rest;\n    int a;\n    getline(in, tag, ':');\n    in >> a;\n    getline(in, rest);\n    cout << \"[\" << tag << \"][\" << a << \"][\" << rest << \"]\\n\";\n}\n```",
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
                "explanation": "三步走：\n① `getline(in, tag, ':')` 读到 `:` 为止，**吃掉分隔符、但不吃冒号后面的空格** → `tag = \"name\"`；\n② `in >> a` 会**跳过前导空白**再读整数 → `a = 42`，并且停在空格之前不消费它；\n③ `getline(in, rest)` 把剩下的 ` 7`（**带一个前导空格**）整段读走 → `rest = \" 7\"`。\n所以输出 `[name][42][ 7]`。\n「[name][42][7]」以为 `>>` 会把后面的空格也吃掉；「[name:]」忘了带分隔符的 getline 会丢掉分隔符；「[name][0][ 7]」以为 `>>` 读到的是 0。\n★ 关键差异：`>>` 跳过前导空白、`getline` 不跳；`getline(in,s,delim)` 消费 delim、而 `get(buf,n,delim)` **不消费** delim（下一读会立刻撞上它）。"
            }
        ]
    },
    {
        "title": "流进入 fail 态后 clear 再读的结果",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "流状态",
            "fail",
            "clear"
        ],
        "choices": [
            "0 1 42",
            "0 0 abc 42",
            "0 1 abc 42",
            "-1 1 abc 42"
        ],
        "source_section": "第 11 讲 · 流类库与输入输出",
        "statement_md": "输入是 `abc 42`，却按 `int` 去读。下面程序输出「失败后的 v、fail()、清状态后读回的字符串与整数」，结果是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nint main() {\n    istringstream in(\"abc 42\");\n    int v = -1;\n    in >> v;\n    cout << v << \" \" << in.fail() << \" \";\n    in.clear();\n    string s;\n    in >> s;\n    in >> v;\n    cout << s << \" \" << v << \"\\n\";\n}\n```",
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
                "explanation": "① `in >> v` 对 `abc` 做整数解析，一个字符都提取不了 → 置 `failbit`；**C++11 起提取失败会把目标写成 0**（不是保持原值 -1），所以 v 打印 0、`fail()` 是 1。\n② `clear()` 只清**状态位**，不动物理位置 —— `abc` 还在缓冲区里；\n③ 于是 `in >> s` 读到 `abc`，再 `in >> v` 读到 42。\n「-1 1」是 C++98 的老行为（失败时不改目标）；「0 1 42」少了读走 `abc` 那一步；「0 0」以为类型不匹配不算 fail。\n★ 两个结论：① fail 后流是「假死」的，不 `clear()` 后续读取全部直接失败；② `clear()` 之后往往还要 `ignore()` 把坏字符吃掉 —— 交互式程序里 `cin.clear(); cin.ignore(numeric_limits<streamsize>::max(), '\\n');` 是标准组合拳。"
            }
        ]
    },
    {
        "title": "同一个 int 用文本与二进制写盘的字节数",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "文本模式",
            "二进制模式",
            "sizeof"
        ],
        "choices": [
            "3 3",
            "4 3",
            "3 4",
            "4 4"
        ],
        "source_section": "第 11 讲 · 流类库与输入输出",
        "statement_md": "整数 `x = 100`，一份用 `<<` 按文本写，一份用 `write` 按二进制写。程序输出「文本字节数 二进制字节数」，结果是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nint main() {\n    const char* ft = \"t.txt\";\n    const char* fb = \"b.txt\";\n    int x = 100;\n    { ofstream t(ft); if (!t) { cout << \"ERRT\"; return 0; } t << x; }\n    { ofstream b(fb, ios::binary); if (!b) { cout << \"ERRB\"; return 0; } b.write(reinterpret_cast<char*>(&x), sizeof x); }\n    long st, sb;\n    { ifstream t(ft, ios::binary | ios::ate); st = (long)t.tellg(); }\n    { ifstream b(fb, ios::binary | ios::ate); sb = (long)b.tellg(); }\n    remove(ft); remove(fb);\n    cout << st << \" \" << sb << \"\\n\";\n}\n```",
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
                "explanation": "文本模式写的是**字符**：`'1' '0' '0'` 三个字节，长度随数值位数变化（100 是 3，1000 变 4，0 只有 1）；二进制模式 `write(reinterpret_cast<char*>(&x), sizeof x)` 写的是**内存映像**，int 恒为 4 字节。\n「4 4」以为文本也是定长；「3 3」以为二进制会紧凑编码；「4 3」把两者对调。\n★ 这个差别正是「定长记录」能成立的前提：只有二进制写入的每条记录字节数**固定**，才能用 `seekg(k * sizeof(Record))` 像数组一样随机定位第 k 条。\n★ 代价：二进制格式绑定了类型宽度与字节序，跨平台/跨编译器就可能读不了；要可移植就得自己按字节序列化。"
            }
        ]
    },
    {
        "title": "定长记录结构体的大小与文件体积",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "二进制I/O",
            "sizeof",
            "内存对齐"
        ],
        "choices": [
            "40 120",
            "32 96",
            "28 84",
            "32 64"
        ],
        "source_section": "第 11 讲 · 流类库与输入输出",
        "statement_md": "把下面这个结构体用 `write` 原样写进二进制文件，连续写 3 条。程序输出「单条 sizeof、3 条合计字节数」，结果是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nstruct Record { int id; char name[16]; double balance; };\n\nint main() { cout << sizeof(Record) << \" \" << sizeof(Record) * 3 << \"\\n\"; }\n```",
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
                "explanation": "`int` 4 字节 + `char[16]` 16 字节 = 20，接下来 `double` 要求 **8 字节对齐**，编译器在中间补 4 字节填充 → `sizeof` = **32**；3 条就是 96 字节。\n「28 84」是没算填充（4+16+8=28）；「32 64」单条对、合计算错；「40 120」是以为 double 前要补 12 字节。\n★ 正因为有填充，二进制格式**不能跨编译器/跨平台随便搬**；要稳定就得显式按字节序列化（或 `#pragma pack`），这也是「定长记录 + seek 定址」能像数组一样随机访问的前提。"
            }
        ]
    },
    {
        "title": "seekp 定位后覆写与 tellp 的文件尾位置",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "seekp",
            "tellp",
            "随机存取"
        ],
        "choices": [
            "2 abXYef",
            "8 abXYef",
            "6 abXYef",
            "6 abXYefXY"
        ],
        "source_section": "第 11 讲 · 流类库与输入输出",
        "statement_md": "先写入 `abcdef`，再用 `ios::in | ios::out` 打开、`seekp(2)` 后写入 `XY`。程序输出「定位到文件尾时的 tellp 文件内容」，结果是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nint main() {\n    const char* f = \"seek.txt\";\n    { ofstream o(f); o << \"abcdef\"; }\n    { fstream io(f, ios::in | ios::out); io.seekp(2); io << \"XY\"; io.seekp(0, ios::end); cout << io.tellp() << \" \"; }\n    { ifstream in(f); string s; in >> s; cout << s << \"\\n\"; }\n    remove(f);\n}\n```",
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
                "explanation": "`seekp(2)` 把写指针移到第 3 个字节（下标从 0 起），`io << \"XY\"` **原地覆写** `cd` 两个字符 → 文件变成 `abXYef`，长度仍是 6。\n`seekp(0, ios::end)` 再问 `tellp()`，得到 6（文件尾 = 字节数）。\n「abXYefXY」以为 `<<` 是插入而不是覆写；「2」是 `seekp(2)` 之后、还没跳到尾部时的位置；「8」把覆写当成了追加。\n★ 这是「定长记录 + seek 定址」的最小模型：`seekp(k * sizeof(Rec))` 就能改第 k 条记录，无需重写整个文件。前提同样有两条：**记录定长**、**二进制模式**。另外注意 `fstream` 的读指针和写指针是**两个独立位置**，要分别 `seekg`/`seekp`。"
            }
        ]
    },
    {
        "title": "ostringstream 里格式化结果的字符数",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "ostringstream",
            "setw",
            "setprecision",
            "格式化输出"
        ],
        "choices": [
            "0007-1.5 8",
            "0007-1.50 10",
            "0007-1.50 9",
            "7-1.50 6"
        ],
        "source_section": "第 11 讲 · 流类库与输入输出",
        "statement_md": "下面程序把格式化结果拼进字符串，再输出「内容 长度」。结果是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nint main() {\n    ostringstream oss;\n    oss << setw(4) << setfill('0') << 7 << \"-\" << fixed << setprecision(2) << 1.5;\n    string s = oss.str();\n    cout << s << \" \" << s.size() << \"\\n\";\n}\n```",
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
                "explanation": "`setw(4) << setfill('0')` 把 7 补成 4 位 → `0007`（4 字符）；中间一个 `-`（1 字符）；`fixed << setprecision(2)` 把 1.5 输出成 `1.50`（4 字符）。合计 4+1+4 = **9**。\n「7-1.50」漏了 `setw/setfill`；「0007-1.5」忘了 `fixed` 之后 `setprecision` 指的是**小数位**；「10」把连字符数成两个。\n★ `ostringstream` 就是「内存里的小文件」：所有格式化操纵符通用，拼好后 `.str()` 取字符串。要复用同一个对象，必须 `oss.str(\"\")` **和** `oss.clear()` 一起 ——前者清内容、后者清状态位（比如上一轮遗留的 failbit）。"
            }
        ]
    },
    {
        "title": "关于流状态位与操纵符的正确说法",
        "subject": "cpp",
        "line": "text",
        "question_type": "multiple_choice",
        "difficulty": 4,
        "total_score": 14,
        "tags": [
            "流状态",
            "操纵符",
            "多选"
        ],
        "choices": [
            "eof() 为真不代表流不可用，while (in >> x) 是在读取失败时才退出",
            "setw 只对紧随其后的一个输出项生效",
            "fixed 是粘性的，设置后会影响后续所有浮点输出",
            "clear() 会连同缓冲区里导致失败的那些字符一起清掉"
        ],
        "source_section": "第 11 讲 · 流类库与输入输出",
        "statement_md": "关于流的状态位与常用操纵符，下列说法**正确**的有：\n\n**多选题**：正确选项不止一个，点选切换，再次点击可取消。",
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
                "explanation": "四条里只有「clear() 会连同缓冲区里导致失败的那些字符一起清掉」是错的：`clear()` 只清**状态位**，缓冲区里的字符原样还在 —— 想丢掉必须 `ignore()`，这就是为什么 `cin.clear()` 之后往往还要 `cin.ignore(...)`。\n其余三条都对：\n① 读完最后一个数据的那一刻只置 `eofbit`，`fail()` 仍为 false、流还能隐式转 true；要**再读一次**失败才置 `failbit`。所以 `while (!in.eof())` 会多跑一轮，`while (in >> x)` 才是正解。\n② `setw` 是唯一**一次性**的常用操纵符。\n③ `fixed` 改的是流状态，一直有效（`setprecision(n)` 从此按小数位解释）。\n★ 顺带记：`bad()` 比 `fail()` 更严重（流本身坏了，如磁盘错误），`good()` 是「全部状态位都干净」。"
            }
        ]
    },
    {
        "title": "catch 块的匹配顺序",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "catch",
            "异常匹配"
        ],
        "choices": [
            "按书写顺序，第一个类型能匹配的 catch 接住",
            "类型最精确（派生层次最深）的那个 catch 接住",
            "最后一个类型能匹配的 catch 接住",
            "由编译器在编译期随机分配"
        ],
        "source_section": "第 12 讲 · 异常处理",
        "statement_md": "一个 try 后面跟着多个 catch 块，异常被哪一个接住？",
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
                "explanation": "catch 的规则是「**从上到下，第一个能接住的**」，不是「选最匹配的」。\n而基类的 catch 能接住派生类异常（类型兼容），于是「基类写在前面」就会把派生类异常**全部截走**，后面的专用处理块成了死代码 —— 所以派生类必须写在基类前面。\n「类型最精确」是把重载解析的规则套到了 catch 上；「最后一个」与「随机分配」都不成立。"
            }
        ]
    },
    {
        "title": "抛出点与捕获点是否必须同函数",
        "subject": "cpp",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 1,
        "total_score": 8,
        "tags": [
            "throw",
            "catch",
            "调用栈"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 12 讲 · 异常处理",
        "statement_md": "`throw` 与接收它的 `catch` 必须写在同一个函数里，否则异常无法传递。",
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
                "explanation": "错。抛出点与处理点可以隔着任意多层函数：中间层不写 try 也不用写任何转发代码，异常会自动穿过它们，直到遇到匹配的 catch。\n这正是异常机制相对「返回错误码」的价值 —— 错误在深处抛、在上层集中处理，中间层一行都不用改。\n如果一路都没人接，最终由 `std::terminate` 终止程序。"
            }
        ]
    },
    {
        "title": "栈展开时局部对象的析构顺序",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "栈展开",
            "析构",
            "RAII"
        ],
        "choices": [
            "+b+a-b-a|C",
            "+b+a|C-a-b",
            "+a+b-b-a|C",
            "+b+a-a-b|C"
        ],
        "source_section": "第 12 讲 · 异常处理",
        "statement_md": "下面程序的输出是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nstruct T {\n    const char* n;\n    explicit T(const char* s) : n(s) { cout << \"+\" << n; }\n    ~T() { cout << \"-\" << n; }\n};\n\nvoid f() { T a(\"a\"); throw 1; }\n\nint main() {\n    try { T b(\"b\"); f(); }\n    catch (int) { cout << \"|C\"; }\n    cout << \"\\n\";\n}\n```",
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
                "explanation": "构造顺序：先 `main` 的 `b`，再 `f` 里的 `a`（`+b+a`）；`throw` 后开始**栈展开**：`a` 随 `f` 的栈帧销毁（`-a`），异常传出 try 块时 `b` 也销毁（`-b`），**最后**才进 catch 打 `|C` → `+b+a-a-b|C`。\n「+b+a-b-a|C」把两个局部对象的析构顺序弄反（析构永远与构造逆序）；「+b+a|C-a-b」以为先进 catch 再析构 —— 实际上异常离开 try 块时局部对象已经析构完了；「+a+b-b-a|C」把构造顺序弄反。\n★ 这就是 RAII 的根基：栈展开保证局部对象的析构函数一定被调用，所以「构造获取、析构释放」的对象在异常面前也不会漏资源。"
            }
        ]
    },
    {
        "title": "基类 catch 写在前面会怎样",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "catch顺序",
            "类型兼容"
        ],
        "choices": [
            "编译错误",
            "B",
            "D",
            "BD"
        ],
        "source_section": "第 12 讲 · 异常处理",
        "statement_md": "下面程序抛出的异常类型是 `D`。输出是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nstruct B {};\nstruct D : B {};\n\nint main() {\n    try { throw D(); }\n    catch (B) { cout << \"B\"; }\n    catch (D) { cout << \"D\"; }\n    cout << \"\\n\";\n}\n```",
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
                "explanation": "catch 按书写顺序取**第一个能接住的**：`B` 在前，而基类对象/引用能接住派生类异常（类型兼容），于是 `D` 异常被 `B` 的块截走，输出 `B` —— 后面那个 `catch (D)` 永远轮不到，是死代码。\n「D」是以为会选最精确的；「BD」以为两个块都会执行（catch 之间是**互斥**的，只进一个）。\n★ 编译器其实看得出来：g++ 对这段代码给 `-Wexceptions` 警告（exception of type 'D' will be caught by earlier handler）。正确写法是派生类在前。"
            }
        ]
    },
    {
        "title": "捕获一切异常的 catch 子句写法",
        "subject": "cpp",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "catch(...)",
            "兜底"
        ],
        "choices": [],
        "source_section": "第 12 讲 · 异常处理",
        "statement_md": "要兜底捕获**任何类型**的异常，catch 的形参位置该写什么？请写出完整的 catch 头部（从 `catch` 写到右括号）。\n\n提示：三个点，必须放在所有 catch 的最后。",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "catch(...)",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|catch(...)\n|catch (...)\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "写法是 `catch (...)`，三个点表示「匹配任何类型」。\n两条铁律：① 它必须放在**最后**（它什么都接，放前面后面的专用处理块全废）；② 常与 `throw;` 配合 —— 不带操作数的 `throw` 会把当前异常**原样重抛**，典型分工是底层只记日志、真正的处理交给上层。"
            }
        ]
    },
    {
        "title": "throw 之后 try 块内剩余语句是否执行",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "throw",
            "控制流",
            "try块"
        ],
        "choices": [
            "只有 throw 写在循环里时才会跳过后续语句",
            "不会：控制流立刻跳到匹配的 catch，try 块里剩下的语句被跳过",
            "会：catch 处理完再回到 try 块里接着执行",
            "会：throw 只中断它自己所在的那一条语句"
        ],
        "source_section": "第 12 讲 · 异常处理",
        "statement_md": "一个 try 块里第 3 条语句 `throw` 了异常。紧随其后的第 4、5 条语句会执行吗？",
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
                "explanation": "`throw` 是**跳转**，不是 `return`：它立即结束当前执行流，边做栈展开边向上找 catch，try 块里剩下的语句一条都不执行，也不会有「回到原地继续」这回事。\n这正是异常处理最容易埋雷的地方：写在 `throw` **之后**的清理代码（`delete`、`close`、解锁）永远不会执行，从 throw 点到 catch 点之间的所有普通语句也都不会执行。\n★ 唯一可靠的清理钩子是**局部对象的析构函数** —— 栈展开保证它一定被调用。所以资源必须交给「构造获取、析构释放」的对象（RAII），而不是靠「末尾写一句 delete」。"
            }
        ]
    },
    {
        "title": "catch 按值接收基类异常的风险",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "catch",
            "对象切片",
            "异常匹配"
        ],
        "choices": [
            "正常，只是多一次拷贝，功能不受影响",
            "发生对象切片：e 只是基类子对象，虚函数失效、派生类附加信息全丢",
            "编译错：catch 不能用基类类型接收派生类异常",
            "正常：e 会按实际类型完整复制，what() 仍是派生类版本"
        ],
        "source_section": "第 12 讲 · 异常处理",
        "statement_md": "自定义异常 `MyErr` 公有继承 `std::exception` 并重写了 `what()`。如果写成 `catch (std::exception e)`，会怎样？",
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
                "explanation": "catch 的形参本质是**复制初始化**：`catch (std::exception e)` 相当于用异常对象去构造一个 `exception` 类型的副本 —— 派生类那部分装不下，被切掉（第 7 讲的对象切片在这里再次出现）。此后 `e.what()` 调到的是基类版本，派生类加的数据成员也全丢了。\n「编译错」不对：类型兼容允许基类接派生类异常，编译完全通过，**错在静默**。\n★ 标准写法一律 `catch (const std::exception& e)`：不复制、不切片、还能接常量右值。同理，`catch (MyErr& e)` 里改的是**异常副本**本身（不是 throw 出去的那个对象），也能正常工作。"
            }
        ]
    },
    {
        "title": "不带操作数的 throw 重抛",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "重抛",
            "catch(...)"
        ],
        "choices": [
            "A",
            "IB",
            "AB",
            "AI"
        ],
        "source_section": "第 12 讲 · 异常处理",
        "statement_md": "下面程序的输出是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nint main() {\n    try {\n        try { throw 3.5; }\n        catch (...) { cout << \"A\"; throw; }\n    }\n    catch (int) { cout << \"I\"; }\n    catch (...) { cout << \"B\"; }\n    cout << \"\\n\";\n}\n```",
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
                "explanation": "内层抛的是 `double 3.5`，`catch (...)` 接住打 `A`，然后 `throw;`（不带操作数）把**当前这个 double 异常原样再抛出去**。外层第一个 `catch (int)` 接不住 double，落到最后一个 `catch (...)` 打 `B` → `AB`。\n「AI」以为重抛会变成 int（`throw;` 不改类型，这点和 `throw x;` 完全不同）；「A」以为重抛后没人接会终止（其实外层有兜底）；「IB」顺序不对。\n★ `throw;` 只能写在 catch 块里（或从其调用的函数里），它复用的是「正在处理的那个异常对象」。"
            }
        ]
    },
    {
        "title": "at 越界抛出的异常由谁接住",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "标准异常",
            "out_of_range",
            "at"
        ],
        "choices": [
            "L",
            "...",
            "L...",
            "编译错误"
        ],
        "source_section": "第 12 讲 · 异常处理",
        "statement_md": "`vector<int> v(3);` 之后访问 `v.at(10)` 会抛异常。下面程序的输出是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nint main() {\n    vector<int> v(3);\n    try { cout << v.at(10); }\n    catch (const logic_error&) { cout << \"L\"; }\n    catch (...) { cout << \"...\"; }\n    cout << \"\\n\";\n}\n```",
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
                "explanation": "`at()` 带越界检查，越界时抛 `std::out_of_range`；而 `out_of_range` 是 `logic_error` 的派生类，所以被第一个 `catch (const logic_error&)` 接住 → 输出 `L`，`catch (...)` 不会再执行。\n「...」是以为只有 `catch (...)` 接得住（忽略了标准异常的继承体系）；「L...」以为两块都会进（catch 之间互斥，只进第一个匹配的）；「编译错误」不对，`at` 抛异常是标准行为。\n★ 对比：`operator[]` 越界是**未定义行为**，不抛异常 —— 要安全就用 `at()`，要快就用 `[]`。"
            }
        ]
    },
    {
        "title": "noexcept 违约后会不会去找 catch",
        "subject": "cpp",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 3,
        "total_score": 8,
        "tags": [
            "noexcept",
            "terminate"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 12 讲 · 异常处理",
        "statement_md": "声明为 `noexcept` 的函数里抛出了异常，程序会先去寻找最近的匹配 `catch` 块，找不到才终止进程。",
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
                "explanation": "错。`noexcept` 是**运行期强制的承诺**，不是提示：一旦违背，**不进任何 catch**，直接调用 `std::terminate` 终止进程（实测 exit code 134），外面就算包了 `try { ... } catch (int) { ... }` 也拦不住。\ng++ 在编译期就会给 `-Wterminate` 警告（`'throw' will always call 'terminate'`）。\n★ 两个实际推论：① 只给**真的不抛**的函数写 noexcept（析构、swap、move 默认就该不抛）；② **析构函数里绝不能抛异常** —— 栈展开途中再抛，标准直接判 terminate。"
            }
        ]
    },
    {
        "title": "自定义异常经基类引用接住后的 what()",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "自定义异常",
            "标准异常体系",
            "what"
        ],
        "choices": [
            "boom",
            "other",
            "std::exception",
            "编译错误：what() 必须返回 string"
        ],
        "source_section": "第 12 讲 · 异常处理",
        "statement_md": "`MyErr` 继承 `std::exception` 并重写 `what()`。下面程序输出什么？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nstruct MyErr : exception {\n    string m;\n    explicit MyErr(const string& s) : m(s) {}\n    const char* what() const noexcept override { return m.c_str(); }\n};\n\nint main() {\n    try { throw MyErr(\"boom\"); }\n    catch (const exception& e) { cout << e.what(); }\n    catch (...) { cout << \"other\"; }\n    cout << \"\\n\";\n}\n```",
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
                "explanation": "`throw MyErr(\"boom\")` 抛的是派生类对象；`catch (const exception& e)` 用**基类引用**接住它，因为是引用、不切片，`e.what()` 经虚函数分派到 `MyErr::what()` → 输出 `boom`。\n「other」是以为只有 `catch (...)` 接得住（忽略了继承体系）；「std::exception」正是**按值接**（`catch (exception e)`）切片之后的典型结果；「必须返回 string」不对：`what()` 的标准签名就是 `const char*`。\n★ 自定义异常的正确姿势：继承 `std::exception`、`const char* what() const noexcept override`、消息存成员并由 `what()` 返回 `c_str()`（成员生存期与异常对象同寿）。这样别人才能用 `catch (const exception&)` 统一兜住你的异常。"
            }
        ]
    },
    {
        "title": "嵌套 try 中重抛时的栈展开与析构顺序",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "栈展开",
            "重抛",
            "嵌套try"
        ],
        "choices": [
            "+m+f-f|in|out|end",
            "+m+f|in|out|end-f-m",
            "+m+f-f|in|out|end-m",
            "+m+f|in-f|out|end-m"
        ],
        "source_section": "第 12 讲 · 异常处理",
        "statement_md": "`f()` 里抛出 int，内层 catch 打 `|in` 后 `throw;` 重抛，外层 catch 打 `|out`。下面程序的输出是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nstruct G {\n    const char* n;\n    G(const char* s) : n(s) { cout << \"+\" << n; }\n    ~G() { cout << \"-\" << n; }\n};\nvoid f() { G g(\"f\"); throw 1; }\n\nint main() {\n    G m(\"m\");\n    try { try { f(); } catch (int) { cout << \"|in\"; throw; } }\n    catch (int) { cout << \"|out\"; }\n    cout << \"|end\";\n}\n```",
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
                "explanation": "按时间线走：构造 `m`（+m）→ 进 `f` 构造 `g`（+f）→ throw。\n**栈展开先发生，才轮到 catch**：`f` 的栈帧销毁 → `-f`；然后内层 catch 打 `|in`；`throw;` 原样重抛，内层 catch 结束，外层 catch 打 `|out`；打完 `|end`；`main` 结束时 `m` 才析构 → `-m`。\n所以是 `+m+f-f|in|out|end-m`。\n「+m+f|in-f|out…」以为先进 catch 再析构 —— 顺序恰好相反；「…|end」漏了 main 里局部对象的析构；「+m+f|in|out|end-f-m」把 `-f` 挪到最后，等于否定了栈展开。\n★ 记住这条因果：析构是**栈展开的一部分**，它发生在控制权交给 catch **之前**。这也是 RAII 在异常路径上依然可靠的原因。"
            }
        ]
    },
    {
        "title": "throw 局部对象时 catch 按值修改的影响",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "throw副本",
            "catch",
            "值传递"
        ],
        "choices": [
            "0",
            "编译错误：E 没有默认构造函数",
            "1",
            "99"
        ],
        "source_section": "第 12 讲 · 异常处理",
        "statement_md": "抛出的是局部对象 `e`，catch 按值接收并把它改成 99。程序最后输出什么？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nstruct E { int v; };\n\nint main() {\n    E e{1};\n    try { throw e; }\n    catch (E x) { x.v = 99; }\n    cout << e.v << \"\\n\";\n}\n```",
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
                "explanation": "`throw e` 会把 `e` **复制**成一份放在安全地带的异常对象（栈展开后副本仍在），catch 形参 `E x` 再复制一次 —— 整整两份拷贝，改 `x` 与外面的 `e` 毫无关系 → 输出 1。\n「99」是以为 catch 形参引用着抛出的原对象。这里要分清三层：原对象 `e`、**异常副本**、catch 形参。`catch (E& x)` 里改的是第二层（异常副本），仍然改不到 `e`。\n「E 没有默认构造函数」不成立：聚合体 `E{1}` 可以拷贝构造，catch 按值只需拷贝构造。\n★ 所以推荐 `catch (const E& x)`：省掉一次拷贝，又不会误以为自己在改原对象。"
            }
        ]
    },
    {
        "title": "标准异常继承体系里的分类",
        "subject": "cpp",
        "line": "text",
        "question_type": "multiple_choice",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "标准异常",
            "logic_error",
            "多选"
        ],
        "choices": [
            "out_of_range 与 invalid_argument 都是 logic_error 的派生类",
            "runtime_error 与 logic_error 都直接派生自 exception",
            "bad_alloc 是 new 申请内存失败时抛出的异常",
            "what() 返回的是一个 std::string 对象"
        ],
        "source_section": "第 12 讲 · 异常处理",
        "statement_md": "关于 `std::exception` 继承体系，下列说法**正确**的有：\n\n**多选题**：正确选项不止一个，点选切换，再次点击可取消。",
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
                "explanation": "四条里只有「what() 返回的是一个 std::string 对象」是错的：`what()` 返回 `const char*`，且标准要求它不抛异常（现代写法 `const char* what() const noexcept override`）。\n其余三条都对。体系主干是 `exception` → `logic_error` / `runtime_error` / `bad_alloc`。\n`logic_error` 一支：`invalid_argument`、`out_of_range`、`length_error`、`domain_error`；`runtime_error` 一支：`range_error`、`overflow_error`、`underflow_error`。\n`bad_alloc` 是 `new` 要不到内存时抛的（可以 `new (nothrow)` 换成返回空指针）。\n★ 分类的意义：`logic_error` 表示「代码写错了、本可避免」（越界、参数非法），`runtime_error` 表示「运行环境出状况、只能运行期发现」。`vector::at()` 越界抛 `out_of_range`，而 `operator[]` 越界是未定义行为、不抛异常。"
            }
        ]
    },
    {
        "title": "构造函数抛异常时自身析构是否执行",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "构造函数",
            "析构",
            "异常安全"
        ],
        "choices": [
            "对象自身的析构函数会被调用，用来释放构造过程中申请的资源",
            "什么都不会析构，包括已经构造好的成员对象",
            "只有析构函数声明为 virtual 时，对象自身的析构才会执行",
            "对象自身的析构函数不会被调用；已构造完成的基类子对象和成员对象会被析构"
        ],
        "source_section": "第 12 讲 · 异常处理",
        "statement_md": "一个对象的构造函数在执行过程中抛出了异常。此时关于析构函数的说法，正确的是：",
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
                "explanation": "构造函数抛出异常意味着这个对象**没有构造完成**，也就谈不上「死亡」——它自己的析构函数不会被调用。但**已经构造完成的**基类子对象和成员对象会被正常析构（逆序），因为它们各自都构造完了。\n所以「在构造函数里 `new` 一块内存、指望析构函数去 `delete`」是必漏的：构造没走完，析构不会来救场。正确姿势是把资源交给**成员对象**（`vector`、`string`、智能指针、流对象），成员构造成功后由它的析构负责释放 —— 这正是 RAII。\n「会被调用」是这道题最典型的误解；「什么都不会析构」忽略了成员对象的析构；「只有 virtual 才执行」把虚析构的作用（经基类指针 delete）混了进来。"
            }
        ]
    },
    {
        "title": "先检查后修改带来的异常安全",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "异常安全",
            "基本保证",
            "RAII"
        ],
        "choices": [
            "E 70",
            "E 100",
            "E 30",
            "E -400"
        ],
        "source_section": "第 12 讲 · 异常处理",
        "statement_md": "账户初始 100，先取 30 成功，再取 500 触发异常。程序输出「标记 余额」，结果是？\n\n（下面省略 `#include` 与 `using namespace std;`）\n\n```cpp\nstruct Insufficient : exception {\n    const char* what() const noexcept override { return \"no\"; }\n};\nstruct Acc {\n    double bal;\n    explicit Acc(double b) : bal(b) {}\n    void withdraw(double a) { if (a > bal) throw Insufficient(); bal -= a; }\n};\n\nint main() {\n    Acc acc(100);\n    try { acc.withdraw(30); acc.withdraw(500); }\n    catch (const exception&) { cout << \"E\"; }\n    cout << \" \" << acc.bal << \"\\n\";\n}\n```",
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
                "explanation": "第一次取 30 成功（余额 70）；第二次 500 > 70，`withdraw` **在扣款之前**就 throw，余额没有被改动，catch 打 `E`，最后输出 `E 70`。\n「E 100」以为整笔业务回滚了（第一次取款并没有被撤销 —— 那是「强保证 + 事务」才有的效果）；「E 30」算错了；「E -400」正是「先扣款再检查」的后果：状态被污染，违反了最基本的异常安全要求。\n★ 两个层次的异常安全：\n**基本保证** —— 抛出后对象仍处于合法状态、不泄漏资源（本题做到：先检查后修改）；\n**强保证** —— 抛出后状态完全回到调用前（事务式，常用「在副本上改完再 swap」实现）。\n★ 反例长什么样：`bal -= a; if (bal < 0) throw ...;` —— 钱已经扣了才报错。"
            }
        ]
    },
    {
        "title": "noexcept 的使用原则",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "noexcept",
            "terminate",
            "契约"
        ],
        "choices": [
            "只给确实不会抛的函数（析构、swap、move）声明 noexcept",
            "给所有函数都加上 noexcept，编译器会做更强的优化",
            "给可能抛异常的函数也加 noexcept，出错时能被上层 catch 接住",
            "noexcept 只是文档注释，运行期没有任何后果"
        ],
        "source_section": "第 12 讲 · 异常处理",
        "statement_md": "关于 `noexcept` 的使用，下列做法最正确的是：",
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
                "explanation": "`noexcept` 是**运行期强制的契约**：一旦函数里真的抛出，不找任何 catch，直接 `std::terminate`（实测退出码 134），外面写 `try { ... } catch (...)` 也拦不住。\n所以它只能给「确实不抛」的函数：析构函数（默认就是 noexcept）、`swap`、`move` 操作 ——这些声明 noexcept 还能让 `vector` 扩容时放心用 move 而不是拷贝。\n「全部加 noexcept」是灾难：任何一处意外抛出都变成进程直接死；「加了就能被 catch」正好说反；「只是注释」也不对 —— 它有运行期后果，也是类型系统的一部分（`noexcept(f())` 可以参与重载与 `if constexpr` 判断）。\n★ 最要命的一条：**析构函数里绝不抛异常**。栈展开本身就靠析构完成，展开途中再抛就是两个异常同时活跃，标准直接判 terminate。"
            }
        ]
    },
    {
        "title": "达到强异常保证的常用手法",
        "subject": "cpp",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "异常安全",
            "强保证",
            "copy-and-swap"
        ],
        "choices": [
            "在操作前把对象的每个成员备份到全局变量，失败时再拷回",
            "在 catch 块里把对象的所有成员重新赋成默认值",
            "给函数加上 noexcept，这样异常就不会发生",
            "先在副本上完成全部修改，全部成功后再与原对象交换"
        ],
        "source_section": "第 12 讲 · 异常处理",
        "statement_md": "要让一个操作具备**强异常保证**（失败后对象状态完全回到调用前），最常用的手法是：",
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
                "explanation": "这就是 **copy-and-swap**：把改动全做在临时副本上，任何一步抛异常都只毁掉副本、原对象分毫未动；全部成功后再用不抛的 `swap` 一次性换过来 —— 交换本身不会失败，所以「要么全成、要么全不变」。\n「全局变量备份」既线程不安全又容易漏成员，还得处理备份本身的异常；「catch 里赋默认值」把对象清空了，那是**回到初始状态**而不是**回到调用前**；「加 noexcept」是自欺：真抛了就是 terminate，连「失败」的机会都没有。\n★ 三档异常安全等级记一下：\n**不抛保证**（noexcept，最强）→ **强保证**（事务式，copy-and-swap）→ **基本保证**（状态合法、不泄漏）→ 无保证。\n工程上大多数操作做到基本保证即可，关键操作（赋值、容器插入）才追求强保证。"
            }
        ]
    },
    {
        "title": "异常对象的传递方式与析构函数不得抛出",
        "subject": "cpp",
        "line": "text",
        "question_type": "short_answer",
        "difficulty": 4,
        "total_score": 12,
        "tags": [
            "catch引用",
            "对象切片",
            "析构",
            "简答"
        ],
        "choices": [],
        "source_section": "第 12 讲 · 异常处理",
        "statement_md": "**简答题**：为什么 catch 的形参推荐写 `const 异常类型&`？又为什么析构函数里绝不能抛出异常？",
        "input_format": "",
        "output_format": "一句话作答（不要抄题目、不要写代码）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "catch 按值接收会再复制一次并发生对象切片，基类形参接派生类异常时虚函数失效；用 const 引用不复制、不切片。析构函数在栈展开途中被调用，此时再抛异常会出现两个异常同时传播，标准直接调用 terminate",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|catch 按值接收会再复制一次并发生对象切片，基类形参接派生类异常时虚函数失效；用 const 引用不复制、不切片。析构函数在栈展开途中被调用，此时再抛异常会出现两个异常同时传播，标准直接调用 terminate\n|按值 catch 会切片并多一次拷贝，const 引用既避免切片又避免拷贝。栈展开靠析构完成，析构里再抛会导致 terminate，所以析构默认 noexcept，不能抛\n|推荐引用是为了不切片、不复制，保留动态类型；析构不能抛是因为栈展开期间再抛异常会让程序直接终止（terminate）\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**为什么用 `const T&`**：`throw` 时异常对象已经被复制到安全地带，catch 若再按值接就**又复制一次**；更严重的是，当形参是基类类型（如 `catch (std::exception e)`）而抛出的是派生类异常时，会发生**对象切片** —— 派生类部分被切掉，`what()` 退回基类版本，附加信息全丢。写成引用则零拷贝、不切片，`const` 还能接常量右值。\n**为什么析构不能抛**：栈展开本身就是靠调用析构函数完成的。如果某个析构在展开途中又抛出，就有两个异常同时活跃，C++ 无法决定该传哪一个，标准规定直接 `std::terminate`。而且析构函数**默认就是 noexcept** 的，一抛就是 terminate。\n★ 所以清理逻辑要么保证不抛，要么在析构内部自己 `try { ... } catch (...) { /* 记日志 */ }` 吞掉。同理，构造函数抛出时对象自身析构不会被调用 —— 资源要交给成员对象（RAII），别指望析构来救场。"
            }
        ]
    }
]
