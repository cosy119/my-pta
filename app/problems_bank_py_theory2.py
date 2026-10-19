# -*- coding: utf-8 -*-
"""Python 线理论题第二批（py_theory2）：把 01~14 讲「每个知识点至少 1 道理论题」补齐。

分工背景
--------
第一批 `problems_bank_py_theory.py`（另一窗口，2026-10-19 提交 b3f1951）覆盖了
02~13 讲，但 01 / 14 两讲为零、07 / 09 / 10 / 11 / 13 各讲偏薄。
本批按各讲小节（知识点）补缺口，全部走 `bank_kit` 工厂生成（mc / multi / tf / fill）。

★ 答案键纪律：所有「求值类」答案（表达式结果、异常类型、排序结果、json 行为……）
  都先用真 Python 跑过（见 data/_facts_pytheory2.py 与当日会话的多选事实核验），
  其中第 14 讲排序题的姓名并列顺序（'张三' 在 '李四' 前，Unicode 码点序）
  就是真跑纠正了直觉错误后才写进来的。概念类答案逐条对照讲义正文。
"""
from __future__ import annotations

from .bank_kit import fill, mc, multi, tf

T = "python"  # subject

PY_THEORY2_PROBLEMS: list[dict] = [

    # ============ 第 01 讲 · Python 开发入门（第一批 0 题，全补） ============
    mc("Python 属于哪一类语言",
       "Python 属于哪一类编程语言？",
       ["编译型语言", "解释型语言", "汇编语言", "标记语言"],
       "B", subject=T, section="第 01 讲 · Python 开发入门", difficulty=1,
       tags=["语言概述"],
       explanation="Python 程序由解释器逐条读取并执行，不需要先整体编译成机器码，"
                   "所以是解释型语言。这也是同一份 .py 能直接在 Windows / Linux 上跑的原因。"),

    tf("Python 3 里 print 必须带括号",
       "在 Python 3 中，`print` 是函数，输出内容必须写在括号里：`print(\"hi\")`。",
       True, subject=T, section="第 01 讲 · Python 开发入门", difficulty=1,
       tags=["语言概述"],
       explanation="Python 2 的 `print \"hi\"` 写法在 Python 3 里是语法错误。"
                   "Python 3 中 print 是内置函数，参数必须加括号。"),

    mc("运行脚本文件的命令",
       "写好了 `hello.py`，在终端里正确的运行方式是哪个？",
       ["python hello.py", "python -m hello", "run hello.py", "execute hello.py"],
       "A", subject=T, section="第 01 讲 · Python 开发入门", difficulty=1,
       tags=["开发环境"],
       explanation="`python 文件名` 是运行脚本的标准方式；`python -m 模块名` 是按模块方式运行"
                   "（不要写 .py 后缀），两者含义不同。"),

    fill("查看 Python 版本的命令",
         "在终端输入什么命令可以查看 Python 解释器的版本号？（写出完整命令）",
         ["python --version", "python -V", "python3 --version", "python3 -V"],
         subject=T, section="第 01 讲 · Python 开发入门", difficulty=1,
         tags=["开发环境"],
         hint="提示：长选项用两个短横线，也有一个字母的大写短写法。",
         explanation="`python --version` 与 `python -V` 等价（V 是大写！小写 -v 是冗余诊断模式）。"
                     "Linux 上解释器名常为 python3。"),

    tf("IDLE 是 Python 自带的",
       "IDLE 是 Python 官方安装包自带的简易交互式开发环境，装好 Python 就能用。",
       True, subject=T, section="第 01 讲 · Python 开发入门", difficulty=1,
       tags=["开发环境", "IDLE"],
       explanation="IDLE 随官方安装包一起安装，支持交互式 >>> 窗口和脚本编辑，"
                   "适合入门；PyCharm / VS Code 则需要另外安装。"),

    # ============ 第 07 讲 · 函数（上）（第一批仅 2 题，补 6） ============
    mc("没有 return 的函数返回什么",
       "定义 `def f(): pass`，调用 `x = f()` 后，`x` 的值是什么？",
       ["0", "None", "空字符串", "报错"],
       "B", subject=T, section="第 07 讲 · 函数（上）", difficulty=1,
       tags=["返回值"],
       explanation="真跑实证：没有 return（或光写 return 不带值）的函数返回 `None`。"
                   "这也是「函数必须有返回值才接得住」的原因。"),

    tf("可变默认参数跨调用共享",
       "函数默认参数的值在 `def` 语句执行时只求值一次；用可变对象（如列表）当默认值，"
       "多次调用会共享同一个对象。",
       True, subject=T, section="第 07 讲 · 函数（上）", difficulty=2,
       tags=["参数", "陷阱"],
       explanation="真跑实证：`def f(x=[]): x.append(1); return x` 连续调用两次分别得到 "
                   "`[1]` 和 `[1, 1]`——两次用的是同一个列表。默认值应该用 `None` 再在函数体内新建。"),

    mc("*args 收集成什么",
       "定义 `def f(*args): ...`，调用 `f(1, 2, 3)` 时 `args` 是什么？",
       ["列表 [1, 2, 3]", "元组 (1, 2, 3)", "字典 {0:1, 1:2, 2:3}", "集合 {1, 2, 3}"],
       "B", subject=T, section="第 07 讲 · 函数（上）", difficulty=2,
       tags=["参数"],
       explanation="真跑实证：`*args` 把多余的位置参数收成**元组**；"
                   "收成字典的是 `**kwargs`（收集关键字参数）。"),

    fill("**kwargs 收集的类型",
         "`def f(**kwargs): ...` 调用 `f(a=1, b=2)` 时，`kwargs` 被收集成哪一种数据类型？（写中文名或英文类名）",
         ["字典", "dict"],
         subject=T, section="第 07 讲 · 函数（上）", difficulty=2,
         tags=["参数"],
         explanation="真跑实证：`**kwargs` 把关键字参数收成字典 `{'a': 1, 'b': 2}`；"
                     "与之相对 `*args` 收成元组。"),

    tf("函数内赋值默认是局部变量",
       "在函数内部给一个全局同名的变量赋值，如果不先 `global` 声明，Python 会在函数内创建一个局部变量，全局变量的值不受影响。",
       True, subject=T, section="第 07 讲 · 函数（上）", difficulty=2,
       tags=["作用域"],
       explanation="真跑实证：全局 `_local = 0`，函数里 `_local = 99` 后调用函数返回 99，"
                   "全局仍是 0。要修改全局变量必须先 `global 变量名`。"),

    fill("默认递归深度限制",
         "CPython 解释器默认的递归深度限制是多大？（超出会抛 RecursionError）",
         ["1000"],
         subject=T, section="第 07 讲 · 函数（上）", difficulty=2,
         tags=["递归"],
         explanation="真跑实证：`sys.getrecursionlimit()` 返回 1000。"
                     "递归太深会抛 `RecursionError`，所以递归必须有终止条件。"),

    multi("f(1, 2) 能调通的函数定义",
          "下列哪些函数定义可以让调用 `f(1, 2)` **成功执行**？（多选）",
          ["def f(a, b): pass", "def f(a, b=1): pass", "def f(*args): pass", "def f(**kw): pass"],
          ["A", "B", "C"], subject=T, section="第 07 讲 · 函数（上）", difficulty=3,
          tags=["参数"],
          explanation="真跑实证：A 直接按位置绑定；B 的 b 收到 2 覆盖默认值；C 的 *args 把 (1, 2) 收成元组。"
                      "D 的 **kw 只收集**关键字**参数，给两个位置参数会抛 `TypeError`。"),

    # ============ 第 08 讲 · 函数（下）（第一批 5 题，补 3） ============
    fill("lambda 表达式的求值",
         "表达式 `(lambda x: x * 2)(5)` 的值是多少？",
         ["10"],
         subject=T, section="第 08 讲 · 函数（下）", difficulty=1,
         tags=["lambda"],
         explanation="真跑实证：lambda 定义一个匿名函数并立即用 5 调用，`5 * 2 = 10`。"),

    mc("@deco 的等价写法",
       "装饰器写法 `@deco` 加在 `def hello(): ...` 上面，等价于下面哪行代码？",
       ["hello = deco(hello)", "hello = hello(deco)", "deco = hello(deco)", "hello = deco()"],
       "A", subject=T, section="第 08 讲 · 函数（下）", difficulty=2,
       tags=["装饰器"],
       explanation="真跑实证：装饰器就是语法糖，`@deco` 等价于把原函数传给装饰器再用返回值替换原名。"
                   "实测装饰后调用得到 `wrapped:hi`，说明调用的是包装函数。"),

    fill("functools.partial 锁定参数",
         "`functools.partial(int, base=2)('101')` 的值是多少？",
         ["5"],
         subject=T, section="第 08 讲 · 函数（下）", difficulty=3,
         tags=["偏函数"],
         explanation="真跑实证：partial 把 `base=2` 固定住，等价于 `int('101', base=2)`，"
                     "即二进制 101 转十进制 5。"),

    # ============ 第 09 讲 · 模块与包（第一批 3 题，补 5） ============
    tf("重复 import 只执行一次",
       "同一个模块被 `import` 多次（哪怕在不同语句里），模块顶层的代码只会在**第一次**导入时执行。",
       True, subject=T, section="第 09 讲 · 模块与包", difficulty=2,
       tags=["模块", "导入"],
       explanation="真跑实证：模块顶层写 `COUNT += 1`，同一程序里 import 两次后 `COUNT` 仍是 1。"
                   "模块对象缓存在 `sys.modules` 里，重复导入只是取缓存。"),

    fill("math.sqrt 的返回值",
         "执行 `import math` 后，表达式 `math.sqrt(16)` 的值是多少？",
         ["4.0"],
         subject=T, section="第 09 讲 · 模块与包", difficulty=1,
         tags=["标准模块"],
         explanation="真跑实证：sqrt 返回**浮点数** 4.0，不是整数 4——注意 `4.0 == 4` 为 True 但类型不同。"),

    mc("__name__ == '__main__' 的含义",
       "模块文件里常写 `if __name__ == '__main__':`，这段代码什么时候才会执行？",
       ["模块被 import 时", "该文件被直接运行时", "程序报错时", "任何时刻都执行"],
       "B", subject=T, section="第 09 讲 · 模块与包", difficulty=2,
       tags=["模块"],
       explanation="真跑实证：直接运行该文件时 `__name__` 是 `'__main__'`；"
                   "被 import 时它等于模块名，所以导入不会触发那段测试代码。"),

    fill("包的标志文件",
         "一个目录要成为 Python 的包，目录下必须有一个名叫什么的文件？（写出完整文件名）",
         ["__init__.py"],
         subject=T, section="第 09 讲 · 模块与包", difficulty=2,
         tags=["包"],
         explanation="`__init__.py`（前后各两条下划线）标记一个目录是包；导入包时它会先被执行。"
                     "没有它，`import 目录.模块` 在传统导入机制下会失败。"),

    mc("sys.path[0] 是什么",
       "用 `python 脚本.py` 方式运行时，`sys.path[0]` 指向哪里？",
       ["Python 安装目录", "当前工作目录", "脚本文件所在的目录", "系统根目录"],
       "C", subject=T, section="第 09 讲 · 模块与包", difficulty=3,
       tags=["模块", "sys.path"],
       explanation="讲义第 09 讲用四种运行方式实测过：脚本方式运行时 `sys.path[0]` 是**脚本所在目录**"
                   "（不是 cwd）；`python -m` 方式或交互式解释器里才是当前工作目录。"),

    # ============ 第 10 讲 · 面向对象（上）（第一批 2 题，补 6） ============
    mc("__init__ 的调用时机",
       "类的 `__init__` 方法在什么时候被调用？",
       ["类定义时", "创建实例时自动调用", "对象销毁时", "手动调用 __init__ 才执行"],
       "B", subject=T, section="第 10 讲 · 面向对象（上）", difficulty=1,
       tags=["构造方法"],
       explanation="真跑实证：`__init__` 里给 `self.v = 7`，一执行 `A()` 立刻就能读到 `a.v == 7`——"
                   "实例创建的瞬间解释器自动调用它（实例方法不用手动调）。"),

    tf("实例方法的 self",
       "实例方法的第一个参数按约定叫 `self`，调用时不需要手动传，它指向调用该方法的实例本身。",
       True, subject=T, section="第 10 讲 · 面向对象（上）", difficulty=1,
       tags=["类"],
       explanation="真跑实证：`a.get()` 等价于 `A.get(a)`——`self` 由 `.` 语法自动传入。"
                   "它只是约定名，但全世界的 Python 代码都这么写。"),

    mc("@classmethod 的第一个参数",
       "用 `@classmethod` 装饰的类方法，它的第一个参数按约定是什么？",
       ["self（实例）", "cls（类本身）", "没有第一个参数", "args（元组）"],
       "B", subject=T, section="第 10 讲 · 面向对象（上）", difficulty=2,
       tags=["类方法", "静态方法"],
       explanation="真跑实证：类方法里 `return cls.__name__` 直接拿到类名——`cls` 指类本身，"
                   "无论用类还是实例调用都一样。"),

    tf("静态方法不带 self/cls",
       "`@staticmethod` 装饰的静态方法定义时不写 `self` 或 `cls` 参数，它其实就是放在类命名空间里的普通函数。",
       True, subject=T, section="第 10 讲 · 面向对象（上）", difficulty=2,
       tags=["静态方法"],
       explanation="真跑实证：`@staticmethod def sm(): return 'static'` 可以直接 `类.sm()` 调用，"
                   "实例与类都不作为第一个参数传入。"),

    fill("__add__ 对应的运算符",
         "在类里定义 `__add__` 方法，重载的是哪个运算符？（写符号）",
         ["+", "加号"],
         subject=T, section="第 10 讲 · 面向对象（上）", difficulty=2,
         tags=["运算符重载"],
         explanation="真跑实证：定义 `def __add__(self, o): return 'add'` 后，`obj + 1` 返回 `'add'`。"
                     "对应关系：`__sub__` 减、`__mul__` 乘、`__eq__` 等于、`__len__` len()。"),

    fill("type(类) 的结果",
         "`class A: pass` 定义后，表达式 `type(A)` 的结果是什么类型？（写英文类名）",
         ["type"],
         subject=T, section="第 10 讲 · 面向对象（上）", difficulty=3,
         tags=["类"],
         explanation="真跑实证：类本身也是对象，它的类型是 `type`（实例 `type(a)` 才是 A）。"
                     "一切皆是对象，类是 type 的实例。"),

    # ============ 第 11 讲 · 面向对象（下）（第一批 3 题，补 4） ============
    fill("私有属性的真实名字",
         "类里写 `self.__secret = 1`（双下划线开头），Python 会把它改名为带前缀的 `_类名__secret`。"
         "若类名是 `P`，在类外访问它的完整属性名是？（写出下划线）",
         ["_P__secret"],
         subject=T, section="第 11 讲 · 面向对象（下）", difficulty=3,
         tags=["封装"],
         explanation="真跑实证：`hasattr(p, '__secret')` 是 False，但 `p._P__secret` 能取到 1。"
                     "这叫名称改写（name mangling），是「伪私有」——防误用，不防恶意。"),

    tf("Python 支持多重继承",
       "Python 的一个类可以同时继承多个父类，如 `class C(A, B):`。",
       True, subject=T, section="第 11 讲 · 面向对象（下）", difficulty=1,
       tags=["继承"],
       explanation="Python 原生支持多重继承，查找顺序由 MRO（方法解析顺序，C3 线性化算法）决定。"
                   "很多语言（如 Java）只允许单继承 + 多接口实现。"),

    mc("多重继承的属性查找顺序",
       "`class M1: pass`、`class M2: pass`、`class M3(M1, M2): pass`，"
       "在 `M3` 实例上找一个 M1 和 M2 都有的属性，先找到谁的？",
       ["M2 的（写在后面优先）", "M1 的（写在前面优先）", "随机", "两个都要执行"],
       "B", subject=T, section="第 11 讲 · 面向对象（下）", difficulty=3,
       tags=["继承", "MRO"],
       explanation="真跑实证：`[c.__name__ for c in M3.__mro__]` 得到 `['M3', 'M1', 'M2', 'object']`——"
                   "按括号里书写的先后顺序查找，M1 在前就先用 M1 的。"),

    tf("多态的含义",
       "多态指：不同类的对象调用**同名**方法，表现出各自不同的行为；调用方不需要关心对象的具体类型。",
       True, subject=T, section="第 11 讲 · 面向对象（下）", difficulty=2,
       tags=["多态"],
       explanation="真跑实证：Duck 和 Cat 两个毫不相干的类都定义 `sound()`，"
                   "循环调用得到 `['ga', 'miao']`——「长得像鸭子就叫」正是 Python 的鸭子类型。"),

    fill("调用父类方法的关键字",
         "在子类方法里调用父类的同名方法，惯用写法是 `super().方法名()`。其中调用父类用的这个函数名叫什么？",
         ["super"],
         subject=T, section="第 11 讲 · 面向对象（下）", difficulty=1,
         tags=["继承"],
         explanation="真跑实证：子类 `def hi(self): return 'mid:' + super().hi()` 输出 `mid:base`。"
                     "零参数 super() 按当前类的 MRO 找下一个类，注意别在嵌套函数里用（第 11 讲讲过的坑）。"),

    # ============ 第 12 讲 · 文件（第一批 5 题，补 4） ============
    tf("open('w') 立即清空",
       "以 `\"w\"` 模式 open 一个已存在的文件，哪怕一行都还没 write，文件内容也已经被清空了。",
       True, subject=T, section="第 12 讲 · 文件", difficulty=2,
       tags=["文件模式", "陷阱"],
       explanation="真跑实证：对一个 28 字节的文件执行 `open(p, 'w')` 后立刻 `getsize`，结果是 0——"
                   "截断发生在打开的瞬间，不是写入时。想保留原内容要追加用 `\"a\"`。"),

    mc("Windows 下 \\n 的落盘与读回",
       "Windows 上以文本模式 `write(\"a\\n\")`，文件里实际存的是什么？用文本模式再读回来得到的又是什么？",
       ["存 \\r\\n，读回 \\n", "存 \\n，读回 \\r\\n", "存 \\r\\n，读回 \\r\\n", "存 \\n，读回 \\n"],
       "A", subject=T, section="第 12 讲 · 文件", difficulty=3,
       tags=["换行", "newline"],
       explanation="真跑实证：rb 方式看文件里确实是 `\\r\\n`；文本模式读回自动统一成 `\\n`。"
                   "这就是「读统一、写加回」会 WA 的根因——加回的 \\r 是多余的。`newline=\"\"` 可双向关闭翻译。"),

    fill("迭代后重读文件的方法",
         "`for line in f:` 遍历完后再 `readline()` 会返回空——因为指针已在文件尾。要重新从头读，应调用 `f.____(0)`。（写方法名）",
         ["seek"],
         subject=T, section="第 12 讲 · 文件", difficulty=2,
         tags=["文件指针"],
         explanation="真跑实证：readline 一行后 `seek(0)`，再 readline 又能读到第一行。"
                     "注意文本模式里 seek 只允许 `seek(0)` 或 `seek(tell())`（字符对不上字节）。"),

    mc("rename 与 replace 的区别",
       "Windows 上想把 a.txt 改名成 b.txt，且 b.txt 已存在。用哪个函数不会报错、直接覆盖？",
       ["os.rename(a, b)", "os.replace(a, b)", "shutil.move(a, b) 的 rename 参数", "两个都不报错"],
       "B", subject=T, section="第 12 讲 · 文件", difficulty=2,
       tags=["os", "陷阱"],
       explanation="真跑实证：`os.rename` 目标存在直接抛 `FileExistsError`（Windows）；"
                   "`os.replace` 语义就是「替换」，目标存在则覆盖。跨平台代码一律用 replace。"),

    multi("哪些模式打开后可读",
          "文件里已有内容 `x`。下列哪些模式打开这个文件后**立刻 read() 是合法的**（不抛异常）？（多选）",
          ["\"r\"", "\"r+\"", "\"a+\"", "\"x\""],
          ["A", "B", "C"], subject=T, section="第 12 讲 · 文件", difficulty=3,
          tags=["文件模式"],
          explanation="真跑实证：r 只读、r+ 读写（指针在头）、a+ 读写（指针在尾，读到空但不报错）都可 read；"
                      "x 是独占创建模式，文件已存在时 open 当场抛 `FileExistsError`，根本打不开。"),

    # ============ 第 13 讲 · 异常（第一批 4 题，补 4） ============
    mc("int('abc') 抛什么异常",
       "表达式 `int('abc')` 会抛出哪种异常？",
       ["ValueError", "TypeError", "KeyError", "IndexError"],
       "A", subject=T, section="第 13 讲 · 异常", difficulty=1,
       tags=["异常类型"],
       explanation="真跑实证：类型正确但**内容**非法 → ValueError；对比：`[1,2][5]` 越界是 IndexError，"
                   "`{}`['k'] 没这个键是 KeyError，`1/0` 是 ZeroDivisionError，`'a'+1` 类型不匹配才是 TypeError。"),

    fill("[1, 2][5] 抛的异常名",
         "表达式 `[1, 2][5]`（索引越界）抛出的异常类名叫什么？（只写类名）",
         ["IndexError"],
         subject=T, section="第 13 讲 · 异常", difficulty=1,
         tags=["异常类型"],
         explanation="真跑实证：列表/元组/字符串的越界访问抛 `IndexError: list index out of range`。"
                     "注意和字典的 KeyError 区分——字典按键找，列表按下标找。"),

    tf("try 里 return，finally 仍执行",
       "`try` 块里写了 `return`，`finally` 块里的代码依然会执行（哪怕函数马上要返回了）。",
       True, subject=T, section="第 13 讲 · 异常", difficulty=2,
       tags=["finally"],
       explanation="真跑实证：try 里 append 'try' 并 return 'try-ret'，finally 里 append 'finally'——"
                   "调用后顺序记录是 ['try', 'finally']，返回值正常。这就是 with 语句能保证关文件的原理。"),

    fill("自定义异常的父类",
         "自定义异常类通常直接继承哪个内置类？（写类名）",
         ["Exception"],
         subject=T, section="第 13 讲 · 异常", difficulty=2,
         tags=["自定义异常"],
         explanation="真跑实证：`class MyErr(Exception): pass` 后 `issubclass(MyErr, Exception)` 为 True。"
                     "继承 Exception 才能被 `except Exception` 兜住；直接继承 BaseException 会绕过常规捕获。"),

    multi("哪些表达式抛 TypeError",
          "下列哪些表达式会抛出 `TypeError`？（多选）",
          ["'a' + 1", "1 + '2'", "[1] + 'a'", "int('a')"],
          ["A", "B", "C"], subject=T, section="第 13 讲 · 异常", difficulty=3,
          tags=["异常类型"],
          explanation="真跑实证：前三例是**类型不匹配**的运算，抛 TypeError；"
                      "D 的 int('a') 类型和签名都合法、只是内容非法，抛的是 ValueError。"),

    # ============ 第 14 讲 · 综合案例（第一批 0 题，全补） ============
    mc("存储层的职责",
       "成绩管理系统采用分层设计（存储 / 校验 / 业务 / 界面）。「存储层」的职责是什么？",
       ["画菜单、接收用户输入", "校验成绩是否在 0~100", "负责数据在文件里的读写与持久化", "计算平均分、排名"],
       "C", subject=T, section="第 14 讲 · 综合案例", difficulty=2,
       tags=["程序设计", "分层"],
       explanation="教材 14.2 的分层思想：每层只干一类事——存储层管 JSON 文件的读写；"
                   "校验层管数据合法性；业务层管统计计算；界面层管交互。改存储格式只动一层，这就是分层的价值。"),

    fill("json 保留中文的参数",
         "`json.dumps({\"名\": \"张三\"})` 默认输出 `\\u540d` 这样的转义。要让中文原样输出，"
         "应给 dumps 传哪个关键字参数？（写 参数名=值 的形式）",
         ["ensure_ascii=False"],
         subject=T, section="第 14 讲 · 综合案例", difficulty=2,
         tags=["json"],
         explanation="真跑实证：默认 ensure_ascii=True 把非 ASCII 全转义成 \\uXXXX；"
                     "传 `ensure_ascii=False` 得到 `{\"名\": \"张三\"}`。注意文件写入时通常还要 `encoding='utf-8'`。"),

    tf("json 往返一致性",
       "`json.loads(json.dumps(数据))` 的结果与原数据等价（列表、字典、字符串、数字都能原样还原）。",
       True, subject=T, section="第 14 讲 · 综合案例", difficulty=2,
       tags=["json"],
       explanation="真跑实证：`json.loads(json.dumps([1, 'a', {'k': 2}]))` 完整还原原结构——"
                   "这就是第 14 讲用 JSON 做持久化的原因。注意元组读回来会变列表、键只能是字符串这类边界。"),

    mc("排序键 -t[1], t[0] 的含义",
       "`sorted(students, key=lambda t: (-t[1], t[0]))`，students 的元素是 (姓名, 分数)。这个排序的规则是？",
       ["分数降序，同分按姓名升序", "分数升序，同分按姓名降序", "按姓名升序", "按分数升序"],
       "A", subject=T, section="第 14 讲 · 综合案例", difficulty=3,
       tags=["排序", "lambda"],
       explanation="真跑实证（键原来写的预期就是被这一跑纠正的）：`('张三',90)` 排在 `('李四',90)` 前面——"
                   "-分数实现降序，元组第二个元素按 Unicode 码点升序。这是「多条件排序」的标准写法。"),

    fill("求平均分的表达式",
         "成绩列表 `scores = [90, 85, 90]`，求平均分的表达式是 `sum(scores) / ____`。（写内置函数调用）",
         ["len(scores)"],
         subject=T, section="第 14 讲 · 综合案例", difficulty=1,
         tags=["统计"],
         explanation="真跑实证：`sum([90, 85, 90]) / len([90, 85, 90])` = 88.33…。"
                     "除数是元素个数 len(scores)，千万别写成列表里最后一个数或常量。"),
]
