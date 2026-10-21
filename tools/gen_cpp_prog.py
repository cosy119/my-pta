# -*- coding: utf-8 -*-
"""「C++ 基础」科目线（subject=cpp）编程题生成器 —— 17 题，按讲义 02~12 讲分布。

与另外两条线的分工：
  - Python 线 / DS 线 已经用掉了大量「排序、词频、字符串反转」类标题，
    本题库一律让标题带上 C++ 机制特征（账户类、static 成员、虚函数、类模板……），
    既避免 `seed.ensure()` 按 title 判重时被静默跳过，也让学生一眼看出在考什么。

每题固定字段：
  title / section / difficulty / score / tags
  statement_md / input_format / output_format / constraints_md
  inputs   ← 测试点输入（手写 + 固定形态，可复现）
  samples  ← 前几个当样例（公开）
  oracle   ← **独立 Python 实现**，算 expected_stdout（笨办法，与 C++ 参考解不同路）
  solution / alt ← 两套 C++ 实现（必须逐字节同输出）

★ oracle 绝不拿 C++ 参考解跑出来填：那是自己给自己判卷。
★ 金额一律用「分」做整数运算，避免浮点误差污染期望输出（第 02 讲浮点判等的教训）。
★ 只有第 11 讲那道格式化题用 double，且取值都落在两位小数可精确表示的点上。

重生成：python tools/gen_cpp_prog.py
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "app" / "problems_bank_cpp_prog.py"

SUBJECT = "cpp"
LINE = "cpp"

SEC_02 = "第 02 讲 · C++ 简单程序设计"
SEC_03 = "第 03 讲 · 函数"
SEC_04 = "第 04 讲 · 类与对象"
SEC_05 = "第 05 讲 · 数据的共享与保护"
SEC_06 = "第 06 讲 · 数组指针与字符串"
SEC_07 = "第 07 讲 · 类的继承"
SEC_08 = "第 08 讲 · 多态性"
SEC_09 = "第 09 讲 · 模板与群体数据"
SEC_10 = "第 10 讲 · 泛型程序设计与STL"
SEC_11 = "第 11 讲 · 流类库与输入输出"
SEC_12 = "第 12 讲 · 异常处理"

PROBLEMS: list[dict] = []


def add(**kw) -> None:
    PROBLEMS.append(kw)


# ===================================================================== #
#  第 02 讲 · C++ 简单程序设计
# ===================================================================== #

def _oracle_02a(text: str) -> str:
    """二进制中 1 的个数：把整数转成二进制字符串再数 '1'（与位运算完全无关的笨办法）。"""
    d = text.split()
    n = int(d[0])
    out = []
    for tok in d[1:1 + n]:
        x = int(tok)
        out.append("%d %d" % (x, bin(x).count("1")))
    return "\n".join(out) + "\n"


add(
    title="位运算消 1：二进制中 1 的个数",
    section=SEC_02,
    difficulty=1, score=10,
    tags=["C++基础", "位运算", "无符号数", "循环"],
    statement_md=(
        "读入 `n` 个非负整数，逐个输出「它的二进制表示里 1 的个数」。\n\n"
        "讲义 2.2 节给的标准写法是：\n\n"
        "```cpp\n"
        "int countOnes(unsigned x) {\n"
        "    int c = 0;\n"
        "    while (x) { x &= x - 1; c++; }\n"
        "    return c;\n"
        "}\n"
        "```\n\n"
        "★ 为什么 `x &= x - 1` 能数 1：减 1 会把**最低位的那个 1 变成 0**，"
        "并把它右边的 0 全部变成 1；再与原来的 `x` 相与，右边那些新冒出来的 1 又被打回去，"
        "结果就是「最低位的 1 被干净地抹掉」。所以每循环一次恰好消掉一个 1，"
        "**循环次数 = 1 的个数**，而不是 32 次。\n\n"
        "⚠️ 两个边界：\n"
        "1. `x = 0` 时循环一次都不进，答案 0（不是 32）；\n"
        "2. `x` 要用**无符号**类型。若用 `int` 存 2³¹ 以上的值，`x - 1` 在负数上做位运算，"
        "行为虽然在本机可用，但标准里右移/溢出的口径不保证，属于自己给自己挖坑。"
    ),
    input_format="第一行 `n`；第二行 `n` 个非负整数。",
    output_format="`n` 行，每行 `x k`：原数与它二进制中 1 的个数，中间一个空格。",
    constraints_md="- 1 ≤ n ≤ 10\n- 0 ≤ x ≤ 2³²−1（用 `unsigned int` 读）\n- 建议 O(popcount) 而不是固定 32 轮",
    inputs=[
        "4\n29 255 0 1\n",
        "3\n7 8 1024\n",
        "2\n2147483647 2147483648\n",
        "1\n4294967295\n",
        "5\n0 0 1 2 3\n",
        "6\n65535 65536 123456789 1000000000 536870912 1073741823\n",
    ],
    samples=3,
    oracle=_oracle_02a,
    solution=r'''#include <cstdio>
using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 0; i < n; i++) {
        unsigned x;
        if (scanf("%u", &x) != 1) return 0;
        int c = 0;
        unsigned t = x;
        while (t) {          // 每轮抹掉最低位的 1
            t &= t - 1;
            c++;
        }
        printf("%u %d\n", x, c);
    }
    return 0;
}
''',
    alt=r'''#include <cstdio>
using namespace std;

// 独立点：不写循环，直接调用编译器内建的 popcount（底层是查表/硬件指令），
// 与参考解「x &= x-1 逐位消 1」是两条完全不同的实现路径。
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 0; i < n; i++) {
        unsigned x;
        if (scanf("%u", &x) != 1) return 0;
        printf("%u %d\n", x, __builtin_popcount(x));
    }
    return 0;
}
''',
)


def _oracle_02b(text: str) -> str:
    """阶梯水费：按档位表逐段累加（不用任何分段公式）。"""
    d = text.split()
    q = int(d[0])
    tiers = [(10, 3), (20, 4), (30, 5), (10 ** 18, 6)]
    out = []
    for tok in d[1:1 + q]:
        x = int(tok)
        fee = 0
        prev = 0
        level = len(tiers)
        for i, (cap, price) in enumerate(tiers, 1):
            take = min(x, cap) - prev
            if take > 0:
                fee += take * price
            if x <= cap:
                level = i
                break
            prev = cap
        out.append("level=%d fee=%d" % (level, fee))
    return "\n".join(out) + "\n"


add(
    title="switch 贯穿实现阶梯水费",
    section=SEC_02,
    difficulty=2, score=15,
    tags=["C++基础", "switch", "贯穿", "分段计费"],
    statement_md=(
        "阶梯水价：每月用水 `x` 吨（整数），计价规则是\n\n"
        "| 档位 | 用水量 | 单价 |\n|---|---|---|\n"
        "| 1 | 1~10 吨 | 3 元/吨 |\n"
        "| 2 | 11~20 吨 | 超出 10 吨的部分 4 元/吨 |\n"
        "| 3 | 21~30 吨 | 超出 20 吨的部分 5 元/吨 |\n"
        "| 4 | 31 吨以上 | 超出 30 吨的部分 6 元/吨 |\n\n"
        "对每次查询输出 `level=<档位> fee=<总费用>`。\n\n"
        "★ 为什么这题值得用 `switch` 写：算总费用天生是「**从最高档往低档逐段累加**」——"
        "先用 `x` 落档，再让 `switch` **故意不写 break** 一路贯穿下去，"
        "每落一层就把该段的水量乘单价加进 `fee`。这正好是讲义 2.4.2 里"
        "「漏 break 会贯穿」那个坑的**正面用法**：贯穿不是 bug，是「连续做几件相关的事」的语法。\n\n"
        "⚠️ 贯穿写法必须保证每一段的水量都算对：第 4 档要加 `x-30`（10 吨）、"
        "第 3 档加 `min(x,30)-20`（又 10 吨）…… 一旦写成 `x-20` 就会把前面已经算过的水量重复计费。\n\n"
        "⚠️ 费用用 `long long`：`x` 取 10⁹ 时费用是 6×10⁹，`int` 直接溢出。"
    ),
    input_format="第一行 `q`（查询次数）；第二行 `q` 个非负整数，表示用水量。",
    output_format="`q` 行，每行 `level=<1~4> fee=<总费用>`。",
    constraints_md="- 1 ≤ q ≤ 10⁵\n- 0 ≤ x ≤ 10⁹\n- 费用需要用 64 位整数",
    inputs=[
        "3\n0 10 11\n",
        "4\n20 21 30 31\n",
        "5\n1 15 25 100 999\n",
        "1\n1000000000\n",
        "2\n9 10\n",
        "6\n0 1 29 30 31 32\n",
    ],
    samples=3,
    oracle=_oracle_02b,
    solution=r'''#include <cstdio>
using namespace std;

int main() {
    int q;
    if (scanf("%d", &q) != 1) return 0;
    for (int i = 0; i < q; i++) {
        long long x;
        scanf("%lld", &x);
        int level;
        long long fee;
        if (x <= 10)      { level = 1; fee = 3 * x; }
        else if (x <= 20) { level = 2; fee = 30 + 4 * (x - 10); }
        else if (x <= 30) { level = 3; fee = 70 + 5 * (x - 20); }
        else              { level = 4; fee = 120 + 6 * (x - 30); }
        printf("level=%d fee=%lld\n", level, fee);
    }
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <algorithm>
using namespace std;

// 独立点：先落档，再用 switch **故意贯穿**从高档往低档逐段累加 ——
// 参考解是一条 if-else 链直接算出总价，这里是「累加式」的另一种推导。
int main() {
    int q;
    if (scanf("%d", &q) != 1) return 0;
    for (int i = 0; i < q; i++) {
        long long x;
        scanf("%lld", &x);
        int level = (x <= 10) ? 1 : (x <= 20) ? 2 : (x <= 30) ? 3 : 4;
        long long fee = 0;
        switch (level) {
            case 4: fee += 6 * (x - 30);              [[fallthrough]];
            case 3: fee += 5 * (min<long long>(x, 30) - 20); [[fallthrough]];
            case 2: fee += 4 * (min<long long>(x, 20) - 10); [[fallthrough]];
            case 1: fee += 3 * min<long long>(x, 10); break;
        }
        printf("level=%d fee=%lld\n", level, fee);
    }
    return 0;
}
''',
)


# ===================================================================== #
#  第 03 讲 · 函数
# ===================================================================== #

def _oracle_03a(text: str) -> str:
    """汉诺塔：用显式列表当栈做迭代，不写递归（与 C++ 参考解不同路）。"""
    n = int(text.split()[0])
    total = (1 << n) - 1
    out = [str(total)]
    stack = [(n, "A", "B", "C", 0)]
    while stack:
        k, a, via, c, stage = stack.pop()
        if k == 0:
            continue
        if stage == 0:
            stack.append((k, a, via, c, 1))
            stack.append((k - 1, a, c, via, 0))
        elif stage == 1:
            out.append("%s->%s" % (a, c))
            stack.append((k, a, via, c, 2))
        else:
            stack.append((k - 1, via, a, c, 0))
    return "\n".join(out) + "\n"


add(
    title="递归打印汉诺塔移动序列",
    section=SEC_03,
    difficulty=3, score=20,
    tags=["C++函数", "递归", "递归三要素", "运行栈"],
    statement_md=(
        "把 `n` 个盘子从 A 柱借助 B 柱搬到 C 柱，大盘不能压在小盘上。"
        "第一行输出**最少移动步数**，随后按顺序输出每一步 `源->目标`。\n\n"
        "★ 递归三要素在这题上一目了然：\n"
        "1. **出口**：`n == 0` 直接返回（一步都不用走）；\n"
        "2. **递推步**：挪 `n` 层 = 先挪上面 `n-1` 层让路 + 挪最底下那 1 层 + 再把 `n-1` 层归位；\n"
        "3. **规模缩小**：每次递归 `n` 都减 1，一定撞到出口。\n\n"
        "★ 为什么先输出步数：`T(n) = 2·T(n−1) + 1` 解出 `T(n) = 2ⁿ − 1`，"
        "讲义里 n=20 实测 1048575 次调用 —— 每加一层工作量翻倍，这就是「指数爆炸」。"
        "所以本题 `n ≤ 12`，输出行数最多 4095 行；再大就不是判题机能救的了。\n\n"
        "⚠️ 参数顺序是最大的坑：`hanoi(n-1, from, to, via)` 里的第三、四个实参"
        "**交换了位置**（借助 to 挪到 via）。写反了不报错，但前几步就全错。"
    ),
    input_format="一个整数 `n`。",
    output_format="第一行是最少步数 `2^n-1`；随后每行一步，形如 `A->C`（无空格）。",
    constraints_md="- 1 ≤ n ≤ 12\n- 输出行数 ≤ 4096 行",
    inputs=[
        "1\n",
        "2\n",
        "3\n",
        "4\n",
        "7\n",
        "11\n",
    ],
    samples=3,
    oracle=_oracle_03a,
    solution=r'''#include <cstdio>
using namespace std;

static void hanoi(int n, char from, char via, char to) {
    if (n == 0) return;                       // 出口
    hanoi(n - 1, from, to, via);              // 上面 n-1 层让路
    printf("%c->%c\n", from, to);             // 挪最大的那 1 层
    hanoi(n - 1, via, from, to);              // 再归位
}

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    printf("%lld\n", (1LL << n) - 1);
    hanoi(n, 'A', 'B', 'C');
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <vector>
using namespace std;

// 独立点：完全不递归 —— 自己开一个 vector 当运行栈，显式保存
// 「哪一层、从哪到哪、走到第几步」，靠 stage 状态机推进。
// 结果序列与递归版完全一致，但走的是迭代路径。
struct Frame {
    int n;
    char from, via, to;
    int stage;          // 0 未开始 / 1 左半已做完 / 2 已打印本层
};

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    printf("%lld\n", (1LL << n) - 1);

    vector<Frame> st;
    st.push_back({n, 'A', 'B', 'C', 0});
    while (!st.empty()) {
        Frame f = st.back();
        st.pop_back();
        if (f.n == 0) continue;
        if (f.stage == 0) {
            st.push_back({f.n, f.from, f.via, f.to, 1});
            st.push_back({f.n - 1, f.from, f.to, f.via, 0});
        } else if (f.stage == 1) {
            printf("%c->%c\n", f.from, f.to);
            st.push_back({f.n, f.from, f.via, f.to, 2});
        } else {
            st.push_back({f.n - 1, f.via, f.from, f.to, 0});
        }
    }
    return 0;
}
''',
)


def _oracle_03b(text: str) -> str:
    """最值统计：直接 max/min + index（不模拟「一遍扫描引用写回」）。"""
    d = text.split()
    n = int(d[0])
    a = [int(v) for v in d[1:1 + n]]
    mx = max(a)
    mn = min(a)
    max_at = a.index(mx) + 1
    min_at = n - a[::-1].index(mn)       # 最后一次出现的 1 基下标
    return "max=%d min=%d\nmax_at=%d min_at=%d\nrange=%d\n" % (mx, mn, max_at, min_at, mx - mn)


add(
    title="引用传参求最值与首次下标",
    section=SEC_03,
    difficulty=2, score=15,
    tags=["C++函数", "引用传参", "const 引用", "一遍扫描"],
    statement_md=(
        "读入 `n` 个整数，输出三行：\n\n"
        "1. `max=.. min=..`\n"
        "2. `max_at=.. min_at=..`（**1 基**下标；最大值取**第一次**出现的位置，"
        "最小值取**最后一次**出现的位置）\n"
        "3. `range=..`（极差 = 最大值 − 最小值）\n\n"
        "★ 为什么强制用引用传参：一个函数只能 `return` 一个值，"
        "而这里要同时带回「最大值、最小值、两个下标」共四个结果。"
        "C 语言的办法是传指针，C++ 更自然的办法是**引用形参** —— 形参就是实参的别名，"
        "函数里写 `mx = a[i]` 就是在改调用方的变量，调用处还不用写 `&`。\n\n"
        "建议签名：`void minMax(const vector<int>& a, int& mx, int& mn, int& maxAt, int& minAt)`。"
        "注意第一个参数是 **`const` 引用**：只读又不想复制整个数组。\n\n"
        "⚠️ 两个易错点：\n"
        "1. `maxAt` 用 `>` 更新、`minAt` 用 `>=` 更新 —— 这样才能得到"
        "「最大值第一次出现、最小值最后一次出现」，两个比较符号不一样，别抄成一样；\n"
        "2. 下标是 1 基，别把 `i` 直接输出。"
    ),
    input_format="第一行 `n`；第二行 `n` 个整数。",
    output_format="三行，格式见题面（`key=value`，同一行内用一个空格分隔）。",
    constraints_md="- 1 ≤ n ≤ 10⁵\n- |元素| ≤ 10⁹\n- 极差可能超过 `int`，用 `long long` 保存",
    inputs=[
        "5\n3 9 -4 9 -4\n",
        "1\n42\n",
        "4\n5 5 5 5\n",
        "6\n-1 -1 0 0 -1 -1\n",
        "3\n1000000000 -1000000000 0\n",
        "7\n2 7 7 1 3 1 5\n",
    ],
    samples=3,
    oracle=_oracle_03b,
    solution=r'''#include <cstdio>
#include <vector>
using namespace std;

// 四个结果全靠引用带回；数组用 const 引用接，既不复制也不许改。
static void minMax(const vector<int>& a, long long& mx, long long& mn,
                   int& maxAt, int& minAt) {
    mx = mn = a[0];
    maxAt = minAt = 1;
    for (int i = 1; i < (int)a.size(); i++) {
        if (a[i] > mx)  { mx = a[i]; maxAt = i + 1; }   // 严格大于：取第一次
        if (a[i] <= mn) { mn = a[i]; minAt = i + 1; }   // 小于等于：取最后一次
    }
}

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<int> a(n);
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);

    long long mx, mn;
    int maxAt, minAt;
    minMax(a, mx, mn, maxAt, minAt);

    printf("max=%lld min=%lld\n", mx, mn);
    printf("max_at=%d min_at=%d\n", maxAt, minAt);
    printf("range=%lld\n", mx - mn);
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;

// 独立点：不手写扫描 —— 最大值交给 max_element（并列返回第一个），
// 最小值「最后一次出现」用反向迭代器 find。参考解是单趟双 if，
// 这里是「标准库 + 反向区间」两条腿。
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<int> a(n);
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);

    auto mxit = max_element(a.begin(), a.end());        // 并列时返回第一个
    long long mx = *mxit, mn = *min_element(a.begin(), a.end());

    int maxAt = int(mxit - a.begin()) + 1;
    auto rit = find(a.rbegin(), a.rend(), (int)mn);     // 反向找 -> 最后一次
    int minAt = n - int(rit - a.rbegin());

    printf("max=%lld min=%lld\n", mx, mn);
    printf("max_at=%d min_at=%d\n", maxAt, minAt);
    printf("range=%lld\n", mx - mn);
    return 0;
}
''',
)


# ===================================================================== #
#  第 04 讲 · 类与对象
# ===================================================================== #

def _oracle_04a(text: str) -> str:
    """账户存取款：直接用一个变量记余额 + 三个计数器（不建类）。"""
    d = text.split()
    bal = int(d[0])
    q = int(d[1])
    pos = 2
    dep = wd = fail = 0
    out = []
    for _ in range(q):
        op = d[pos]; pos += 1
        amt = int(d[pos]); pos += 1
        if op == "D":
            bal += amt
            dep += 1
            out.append("deposit %d -> %d" % (amt, bal))
        else:
            if amt > bal:
                fail += 1
                out.append("withdraw %d FAILED balance=%d" % (amt, bal))
            else:
                bal -= amt
                wd += 1
                out.append("withdraw %d -> %d" % (amt, bal))
    out.append("final=%d deposit=%d withdraw=%d failed=%d" % (bal, dep, wd, fail))
    return "\n".join(out) + "\n"


add(
    title="账户类存取款模拟",
    section=SEC_04,
    difficulty=2, score=15,
    tags=["C++类与对象", "构造函数", "封装", "成员函数"],
    statement_md=(
        "实现一个最小的银行账户类：余额是私有成员，只能通过 `deposit` / `withdraw` 改动。"
        "读入初始余额和 `q` 条操作（`D 金额` 存款、`W 金额` 取款），"
        "逐条输出操作结果，最后输出一行统计。\n\n"
        "输出格式：\n\n"
        "```text\n"
        "deposit 100 -> 300\n"
        "withdraw 50 -> 250\n"
        "withdraw 500 FAILED balance=250\n"
        "final=250 deposit=1 withdraw=1 failed=1\n"
        "```\n\n"
        "★ 为什么要把余额设成 `private`：如果余额是 public 的，谁都能写 `acc.balance -= 500` "
        "把它扣成负数，而「余额不能透支」这条业务规则就无处安放。"
        "封装的意义就是**把规则和它保护的数据放同一个类里** —— "
        "`withdraw` 先检查再扣款，检查不过就返回 `false` 并且**一个字节都不改**。\n\n"
        "★ 那个 `bool` 返回值是讲义 4.8 的写法：错误用返回值上报，正常路径继续往下走；"
        "第 12 讲会把它换成抛异常。\n\n"
        "⚠️ 边界：取款金额**恰好等于**余额是允许的（扣完为 0）；取款金额为 0 也算成功。"
        "别把判断写成 `>=`。"
    ),
    input_format="第一行初始余额 `b`；第二行 `q`；随后 `q` 行，每行 `D amt` 或 `W amt`。",
    output_format="每条操作一行结果；最后一行 `final=<余额> deposit=<成功存款数> withdraw=<成功取款数> failed=<失败数>`。",
    constraints_md="- 0 ≤ b ≤ 10¹²\n- 1 ≤ q ≤ 10⁵\n- 0 ≤ amt ≤ 10¹²\n- 余额与金额用 `long long`",
    inputs=[
        "100\n4\nD 100\nW 50\nW 500\nD 0\n",
        "0\n3\nW 1\nD 5\nW 5\n",
        "1000\n3\nW 1000\nD 1\nW 1\n",
        "50\n2\nD 450\nW 500\n",
        "7\n5\nW 3\nW 4\nW 1\nD 100\nW 99\n",
        "1000000000000\n3\nW 1000000000000\nD 1\nW 999999999999\n",
    ],
    samples=3,
    oracle=_oracle_04a,
    solution=r'''#include <cstdio>
using namespace std;

class Account {
private:
    long long balance_;                 // 私有：外部只能看，不能改
public:
    explicit Account(long long b = 0) : balance_(b) {}

    void deposit(long long amt) { balance_ += amt; }

    bool withdraw(long long amt) {      // 先检查再扣款
        if (amt > balance_) return false;
        balance_ -= amt;
        return true;
    }
    long long balance() const { return balance_; }   // 常成员函数：只读
};

int main() {
    long long b;
    int q;
    if (scanf("%lld %d", &b, &q) != 2) return 0;

    Account acc(b);
    int dep = 0, wd = 0, fail = 0;
    for (int i = 0; i < q; i++) {
        char op[4];
        long long amt;
        scanf("%s %lld", op, &amt);
        if (op[0] == 'D') {
            acc.deposit(amt);
            dep++;
            printf("deposit %lld -> %lld\n", amt, acc.balance());
        } else {
            if (acc.withdraw(amt)) {
                wd++;
                printf("withdraw %lld -> %lld\n", amt, acc.balance());
            } else {
                fail++;
                printf("withdraw %lld FAILED balance=%lld\n", amt, acc.balance());
            }
        }
    }
    printf("final=%lld deposit=%d withdraw=%d failed=%d\n",
           acc.balance(), dep, wd, fail);
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <string>
#include <iostream>
using namespace std;

// 独立点：余额改成「以分为单位的整数 + 三个计数器放在类里」，
// withdraw 用「先记账再回滚」而不是「先检查再扣款」，输出口径一致。
// 另外 IO 换成 cin/cout（参考解用 scanf/printf），行尾仍是 '\n'。
class Account {
    long long cents_;
    int dep_, wd_, fail_;
public:
    explicit Account(long long yuan = 0) : cents_(yuan), dep_(0), wd_(0), fail_(0) {}

    void deposit(long long yuan) {
        cents_ += yuan;
        dep_++;
    }
    bool withdraw(long long yuan) {
        long long next = cents_ - yuan;      // 先算目标余额
        if (next < 0) {                      // 余额不足：回滚（这里其实没动过）
            fail_++;
            return false;
        }
        cents_ = next;
        wd_++;
        return true;
    }
    long long balance() const { return cents_; }
    int depCount() const { return dep_; }
    int wdCount() const { return wd_; }
    int failCount() const { return fail_; }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long b;
    int q;
    if (!(cin >> b >> q)) return 0;

    Account acc(b);
    for (int i = 0; i < q; i++) {
        string op;
        long long amt;
        cin >> op >> amt;
        if (op == "D") {
            acc.deposit(amt);
            cout << "deposit " << amt << " -> " << acc.balance() << '\n';
        } else if (acc.withdraw(amt)) {
            cout << "withdraw " << amt << " -> " << acc.balance() << '\n';
        } else {
            cout << "withdraw " << amt << " FAILED balance=" << acc.balance() << '\n';
        }
    }
    cout << "final=" << acc.balance()
         << " deposit=" << acc.depCount()
         << " withdraw=" << acc.wdCount()
         << " failed=" << acc.failCount() << '\n';
    return 0;
}
''',
)


def _oracle_04b(text: str) -> str:
    """有理数累加：用 fractions.Fraction 这个标准库实现（与 C++ 手写约分不同来源）。"""
    from fractions import Fraction

    d = text.split()
    n = int(d[0])
    total = Fraction(0, 1)
    out = []
    for tok in d[1:1 + n]:
        a, b = tok.split("/")
        f = Fraction(int(a), int(b))
        total += f
        out.append("%d/%d" % (f.numerator, f.denominator))
    out.append("sum=%d/%d" % (total.numerator, total.denominator))
    return "\n".join(out) + "\n"


add(
    title="有理数类的构造函数重载与约分",
    section=SEC_04,
    difficulty=3, score=20,
    tags=["C++类与对象", "构造函数重载", "常成员函数", "gcd"],
    statement_md=(
        "读入 `n` 个分数（形如 `a/b`，`b ≠ 0`），对每个分数输出**约分后**的形式，"
        "最后输出它们的累加和（同样约分）。\n\n"
        "输出的分母**永远为正**，负号只出现在分子上：`-6/8` → `-3/4`，`3/-4` → `-3/4`。\n\n"
        "★ 这道题练的是「构造函数重载」这一族东西：\n"
        "- `Rational()` 默认构造 0/1；\n"
        "- `Rational(long long n)` 整数变分数（分母补 1）—— 有它才能写 `Rational(3)`；\n"
        "- `Rational(long long a, long long b)` 才是通用版本。\n\n"
        "真正的**不变量**在构造函数里建立：任何对象出生时都必须满足「分母 > 0 且已约分」。"
        "把归一化写进构造函数（而不是写进每个成员函数），就没有任何一条路径能造出"
        "未约分的对象 —— 这叫「用构造函数守住类的约束」。\n\n"
        "⚠️ 三个坑：\n"
        "1. 符号要先搬到分子再求 gcd，否则 `gcd(-6, -8)` 的符号约定会让你算错；\n"
        "2. `gcd(0, 4) = 4`，`0/4` 要归一成 `0/1`，别在 gcd 为 0 时除零；\n"
        "3. 通分用 `long long`：分母相乘会快过 `int`。"
    ),
    input_format="第一行 `n`；随后 `n` 个分数，每个占一行，形如 `a/b`。",
    output_format="前 `n` 行是每个分数约分后的形式；最后一行 `sum=<分子>/<分母>`。",
    constraints_md="- 1 ≤ n ≤ 6\n- |a| ≤ 1000，1 ≤ |b| ≤ 1000\n- 结果用 `long long` 保存",
    inputs=[
        "2\n1/2\n1/3\n",
        "3\n-6/8\n3/-4\n0/5\n",
        "1\n7/1\n",
        "4\n1/2\n1/2\n1/2\n1/2\n",
        "5\n-1/3\n2/6\n5/-10\n7/14\n-1/2\n",
        "3\n999/1000\n-999/1000\n1/999\n",
    ],
    samples=3,
    oracle=_oracle_04b,
    solution=r'''#include <cstdio>
#include <string>
#include <numeric>
#include <cstdlib>
using namespace std;

class Rational {
private:
    long long num_, den_;               // 不变量：den_ > 0 且已约分
    void normalize() {
        if (den_ < 0) { num_ = -num_; den_ = -den_; }
        long long a = num_ < 0 ? -num_ : num_;
        long long g = std::gcd(a, den_);
        if (g > 1) { num_ /= g; den_ /= g; }
    }
public:
    Rational() : num_(0), den_(1) {}
    explicit Rational(long long n) : num_(n), den_(1) {}          // 重载 1
    Rational(long long n, long long d) : num_(n), den_(d) {       // 重载 2
        normalize();
    }
    Rational add(const Rational& o) const {
        return Rational(num_ * o.den_ + o.num_ * den_, den_ * o.den_);
    }
    long long num() const { return num_; }
    long long den() const { return den_; }
};

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    Rational sum;
    char buf[64];
    for (int i = 0; i < n; i++) {
        scanf("%63s", buf);
        string s(buf);
        size_t p = s.find('/');
        Rational f = (p == string::npos)
                     ? Rational(atoll(s.c_str()))
                     : Rational(atoll(s.substr(0, p).c_str()),
                                atoll(s.substr(p + 1).c_str()));
        printf("%lld/%lld\n", f.num(), f.den());
        sum = sum.add(f);
    }
    printf("sum=%lld/%lld\n", sum.num(), sum.den());
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <string>
#include <numeric>
#include <cstdlib>
using namespace std;

// 独立点：不做「每加一次就约分」，而是先把所有分数通分到同一个公分母
// （边读边求 lcm），加完只约分一次。两条路径的结果必然相同，
// 但中间量与运算次数完全不一样。
struct Frac { long long a, b; };

static Frac reduce(Frac f) {
    if (f.b < 0) { f.a = -f.a; f.b = -f.b; }
    long long g = std::gcd(f.a < 0 ? -f.a : f.a, f.b);
    if (g > 1) { f.a /= g; f.b /= g; }
    return f;
}

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;

    char buf[64];
    Frac fs[16];
    for (int i = 0; i < n; i++) {
        scanf("%63s", buf);
        string s(buf);
        size_t p = s.find('/');
        Frac f;
        if (p == string::npos) { f.a = atoll(s.c_str()); f.b = 1; }
        else {
            f.a = atoll(s.substr(0, p).c_str());
            f.b = atoll(s.substr(p + 1).c_str());
        }
        fs[i] = reduce(f);
        printf("%lld/%lld\n", fs[i].a, fs[i].b);
    }

    // 通分到所有分母的最小公倍数，最后只约分一次
    long long L = 1;
    for (int k = 0; k < n; k++) {
        long long g = std::gcd(L, fs[k].b);
        L = L / g * fs[k].b;
    }
    long long s2 = 0;
    for (int k = 0; k < n; k++) s2 += fs[k].a * (L / fs[k].b);
    Frac r = reduce({s2, L});
    printf("sum=%lld/%lld\n", r.a, r.b);
    return 0;
}
''',
)


# ===================================================================== #
#  第 05 讲 · 数据的共享与保护
# ===================================================================== #

def _oracle_05(text: str) -> str:
    """静态成员统计：用一个字典存账户 + 三个普通变量当计数器（没有「类」的概念）。"""
    d = text.split()
    q = int(d[0])
    pos = 1
    accounts: dict[int, int] = {}
    opened = 0
    out = []
    for _ in range(q):
        op = d[pos]; pos += 1
        if op == "N":
            aid = int(d[pos]); bal = int(d[pos + 1]); pos += 2
            accounts[aid] = bal
            opened += 1
        elif op == "C":
            aid = int(d[pos]); pos += 1
            accounts.pop(aid, None)
        elif op == "D":
            aid = int(d[pos]); amt = int(d[pos + 1]); pos += 2
            accounts[aid] = accounts.get(aid, 0) + amt
        elif op == "W":
            aid = int(d[pos]); amt = int(d[pos + 1]); pos += 2
            if accounts.get(aid, 0) >= amt:
                accounts[aid] -= amt
        else:  # Q
            out.append("alive=%d total=%d opened=%d"
                       % (len(accounts), sum(accounts.values()), opened))
    return "\n".join(out) + "\n"


add(
    title="静态成员统计存活账户数",
    section=SEC_05,
    difficulty=3, score=20,
    tags=["C++共享与保护", "静态数据成员", "静态成员函数", "对象生命周期"],
    statement_md=(
        "用一个 `Account` 类管理账户，类里放**三个静态数据成员**：\n\n"
        "- `alive_`：当前存活的账户数；\n"
        "- `opened_`：历史累计开过户数（只增不减）；\n"
        "- `total_`：所有账户余额之和。\n\n"
        "支持 5 种指令：`N id bal` 开户、`C id` 销户、`D id amt` 存款、`W id amt` 取款"
        "（余额不足则什么也不做）、`Q` 查询。**只有 `Q` 产生输出**，格式：\n\n"
        "```text\n"
        "alive=2 total=1500 opened=3\n"
        "```\n\n"
        "★ 为什么这三个数必须是 `static`：它们描述的是「这一类东西的总体状况」，"
        "而不是「某个账户自己的状况」。普通成员是每个对象一份，`static` 成员是**全类一份、"
        "全体对象共享** —— 建一个账户 `alive_++`，销一个账户 `~Account()` 里 `alive_--`，"
        "不用谁去专门维护一个全局表。\n\n"
        "★ 构造函数/析构函数是这两个计数器的唯一入口：`alive_` 在构造里加、在析构里减，"
        "`opened_` 只在构造里加。这样即使对象是 `new` 出来又 `delete` 掉的，账也永远是平的。\n\n"
        "⚠️ 静态数据成员**类内只声明、类外必须定义**：`int Account::alive_ = 0;`。"
        "漏了这三行编译能过，**连接**才报 `undefined reference`。\n\n"
        "⚠️ 销户时 `total_` 要减去该账户的余额，否则总量永远只涨不跌。"
    ),
    input_format="第一行 `q`（指令条数）；随后 `q` 行指令，格式见题面。",
    output_format="对每条 `Q` 输出一行 `alive=<存活数> total=<余额总和> opened=<历史开户数>`。",
    constraints_md="- 1 ≤ q ≤ 10⁵\n- 账户 id 唯一，0 ≤ id ≤ 10⁹\n- 余额与金额 ≤ 10⁹，总和用 `long long`",
    inputs=[
        "6\nN 1 1000\nN 2 500\nD 1 200\nQ\nC 2\nQ\n",
        "3\nN 7 0\nC 7\nQ\n",
        "5\nN 1 10\nN 2 20\nW 1 5\nW 1 100\nQ\n",
        "4\nN 5 100\nC 5\nN 5 40\nQ\n",
        "6\nN 1 1\nN 2 2\nD 2 3\nQ\nC 1\nQ\n",
        "5\nN 1000000000 1000000000\nD 1000000000 1000000000\nQ\nC 1000000000\nQ\n",
    ],
    samples=3,
    oracle=_oracle_05,
    solution=r'''#include <cstdio>
#include <map>
using namespace std;

class Account {
private:
    int id_;
    long long balance_;
    static int alive_;          // 类内声明
    static int opened_;
    static long long total_;
public:
    Account(int id, long long bal) : id_(id), balance_(bal) {
        alive_++;
        opened_++;
        total_ += bal;
    }
    ~Account() {
        alive_--;
        total_ -= balance_;
    }
    void deposit(long long amt) { balance_ += amt; total_ += amt; }
    bool withdraw(long long amt) {
        if (amt > balance_) return false;
        balance_ -= amt;
        total_ -= amt;
        return true;
    }
    static int alive() { return alive_; }
    static int opened() { return opened_; }
    static long long total() { return total_; }
};

// 类外定义并初始化 —— 漏了就连接失败
int Account::alive_ = 0;
int Account::opened_ = 0;
long long Account::total_ = 0;

int main() {
    int q;
    if (scanf("%d", &q) != 1) return 0;
    map<int, Account*> book;
    char op[4];
    for (int i = 0; i < q; i++) {
        scanf("%s", op);
        if (op[0] == 'N') {
            int id; long long bal;
            scanf("%d %lld", &id, &bal);
            book[id] = new Account(id, bal);
        } else if (op[0] == 'C') {
            int id; scanf("%d", &id);
            auto it = book.find(id);
            if (it != book.end()) {
                delete it->second;          // 析构里把 alive_ / total_ 减回去
                book.erase(it);
            }
        } else if (op[0] == 'D') {
            int id; long long amt;
            scanf("%d %lld", &id, &amt);
            auto it = book.find(id);
            if (it != book.end()) it->second->deposit(amt);
        } else if (op[0] == 'W') {
            int id; long long amt;
            scanf("%d %lld", &id, &amt);
            auto it = book.find(id);
            if (it != book.end()) it->second->withdraw(amt);
        } else {
            printf("alive=%d total=%lld opened=%d\n",
                   Account::alive(), Account::total(), Account::opened());
        }
    }
    for (auto& kv : book) delete kv.second;
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <map>
using namespace std;

// 独立点：不用 new/delete，账户按**值**存进 map<int, Account>，
// 销户时 erase 掉元素，析构照样自动触发 —— 静态计数器靠「容器管理生命周期」维护，
// 与参考解的「裸指针 + 手动 delete」是两种对象管理方式。
class Account {
    int id_;
    long long balance_;
    static int alive_;
    static int opened_;
    static long long total_;
public:
    Account() : id_(0), balance_(0) {}
    Account(int id, long long bal) : id_(id), balance_(bal) {
        alive_++; opened_++; total_ += bal;
    }
    Account(const Account& o) : id_(o.id_), balance_(o.balance_) {
        alive_++; total_ += balance_;          // map 拷贝也要记账
    }
    ~Account() { alive_--; total_ -= balance_; }
    void deposit(long long amt) { balance_ += amt; total_ += amt; }
    bool withdraw(long long amt) {
        if (amt > balance_) return false;
        balance_ -= amt; total_ -= amt;
        return true;
    }
    static int alive() { return alive_; }
    static int opened() { return opened_; }
    static long long total() { return total_; }
};

int Account::alive_ = 0;
int Account::opened_ = 0;
long long Account::total_ = 0;

int main() {
    int q;
    if (scanf("%d", &q) != 1) return 0;
    map<int, Account> book;
    char op[4];
    for (int i = 0; i < q; i++) {
        scanf("%s", op);
        if (op[0] == 'N') {
            int id; long long bal;
            scanf("%d %lld", &id, &bal);
            book.emplace(id, Account(id, bal));
        } else if (op[0] == 'C') {
            int id; scanf("%d", &id);
            book.erase(id);
        } else if (op[0] == 'D') {
            int id; long long amt;
            scanf("%d %lld", &id, &amt);
            auto it = book.find(id);
            if (it != book.end()) it->second.deposit(amt);
        } else if (op[0] == 'W') {
            int id; long long amt;
            scanf("%d %lld", &id, &amt);
            auto it = book.find(id);
            if (it != book.end()) it->second.withdraw(amt);
        } else {
            printf("alive=%d total=%lld opened=%d\n",
                   Account::alive(), Account::total(), Account::opened());
        }
    }
    return 0;
}
''',
)


# ===================================================================== #
#  第 06 讲 · 数组指针与字符串
# ===================================================================== #

def _oracle_06a(text: str) -> str:
    """逐词扫描：用正则切词，再对每个词做长度比较（与手写 isalnum 循环不同路）。"""
    import re

    line = text.rstrip("\n")
    words = re.findall(r"[0-9A-Za-z]+", line)
    out = ["len=%d words=%d" % (len(line), len(words))]
    if not words:
        out.append("longest=-(0)")
        out.append("shortest=-(0)")
        return "\n".join(out) + "\n"

    longest = words[0]
    shortest = words[0]
    for w in words:
        if len(w) > len(longest):
            longest = w
        if len(w) < len(shortest):
            shortest = w
    out.append("longest=%s(%d)" % (longest, len(longest)))
    out.append("shortest=%s(%d)" % (shortest, len(shortest)))
    return "\n".join(out) + "\n"


add(
    title="string 逐词扫描与最长最短词",
    section=SEC_06,
    difficulty=2, score=15,
    tags=["C++字符串", "getline", "string", "边界处理"],
    statement_md=(
        "读入**一整行**文本（可能含空格），统计：\n\n"
        "1. `len=<字符数> words=<单词数>`\n"
        "2. `longest=<单词>(<长度>)` —— 长度并列时取**最先出现**的\n"
        "3. `shortest=<单词>(<长度>)` —— 同样取最先出现的\n\n"
        "「单词」= 连续的字母或数字，其它字符都算分隔符。没有任何单词时，"
        "后两行输出 `longest=-(0)` / `shortest=-(0)`。\n\n"
        "★ 为什么必须用 `getline`：`cin >> s` 遇到空格就停，"
        "一行 `hello world` 只能读到 `hello`。读整行要用 `getline(cin, line)`。\n\n"
        "★ 逐词扫描的骨架（不额外开数组）：\n\n"
        "```cpp\n"
        "for (size_t i = 0; i < s.size(); ) {\n"
        "    if (!isalnum((unsigned char)s[i])) { i++; continue; }\n"
        "    size_t j = i;\n"
        "    while (j < s.size() && isalnum((unsigned char)s[j])) j++;\n"
        "    string w = s.substr(i, j - i);   // 一个单词\n"
        "    i = j;\n"
        "}\n"
        "```\n\n"
        "⚠️ 两个坑：\n"
        "1. `isalnum` 的形参要转 `unsigned char`：直接传负的 `char` 是未定义行为"
        "（中文/高位字节会踩到）；\n"
        "2. `len` 统计的是**整行字符数**，含空格和标点；空行时是 0 而不是 1"
        "（`getline` 读到换行为止，换行符不进字符串）。"
    ),
    input_format="一整行文本（可含空格与标点，ASCII）。",
    output_format="三行：`len=.. words=..`、`longest=词(长度)`、`shortest=词(长度)`。",
    constraints_md="- 行长 ≤ 10⁵\n- 仅 ASCII 可见字符与空格\n- 单词只由字母和数字组成",
    inputs=[
        "hello world 123\n",
        "C++ is fun!\n",
        "\n",
        "   \n",
        "a bb ccc dddd\n",
        "abc123 456def\n",
        "x\n",
    ],
    samples=3,
    oracle=_oracle_06a,
    solution=r'''#include <cstdio>
#include <string>
#include <cctype>
#include <iostream>
using namespace std;

int main() {
    string s;
    if (!getline(cin, s)) return 0;

    int words = 0;
    string longest, shortest;
    for (size_t i = 0; i < s.size(); ) {
        if (!isalnum((unsigned char)s[i])) { i++; continue; }
        size_t j = i;
        while (j < s.size() && isalnum((unsigned char)s[j])) j++;
        string w = s.substr(i, j - i);
        words++;
        if (longest.empty() || w.size() > longest.size()) longest = w;
        if (shortest.empty() || w.size() < shortest.size()) shortest = w;
        i = j;
    }

    printf("len=%d words=%d\n", (int)s.size(), words);
    if (words == 0) {
        printf("longest=-(0)\n");
        printf("shortest=-(0)\n");
    } else {
        printf("longest=%s(%d)\n", longest.c_str(), (int)longest.size());
        printf("shortest=%s(%d)\n", shortest.c_str(), (int)shortest.size());
    }
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <string>
#include <vector>
#include <cctype>
#include <algorithm>
#include <iostream>
using namespace std;

// 独立点：不手工扫下标 —— 先把所有单词抽进 vector<string>，
// 再用 std::max_element / min_element 配自定义比较器求最长最短。
// 参考解是一趟扫描边扫边比，这里是「先收集、再比较」。
static bool isWordChar(char c) { return isalnum((unsigned char)c) != 0; }

int main() {
    string s;
    if (!getline(cin, s)) return 0;

    vector<string> ws;
    size_t i = 0;
    while (i < s.size()) {
        while (i < s.size() && !isWordChar(s[i])) i++;
        size_t j = i;
        while (j < s.size() && isWordChar(s[j])) j++;
        if (j > i) ws.push_back(s.substr(i, j - i));
        i = j;
    }

    printf("len=%d words=%d\n", (int)s.size(), (int)ws.size());
    if (ws.empty()) {
        printf("longest=-(0)\n");
        printf("shortest=-(0)\n");
        return 0;
    }
    // 严格大于 / 严格小于 => 并列时保留最先出现的那个
    auto lg = max_element(ws.begin(), ws.end(),
        [](const string& a, const string& b) { return a.size() < b.size(); });
    auto sh = min_element(ws.begin(), ws.end(),
        [](const string& a, const string& b) { return a.size() < b.size(); });
    printf("longest=%s(%d)\n", lg->c_str(), (int)lg->size());
    printf("shortest=%s(%d)\n", sh->c_str(), (int)sh->size());
    return 0;
}
''',
)


def _oracle_06b(text: str) -> str:
    """最大/最小子段和：O(n²) 枚举所有 (l, r)，用前缀和相减（笨办法）。"""
    d = text.split()
    n = int(d[0])
    a = [int(v) for v in d[1:1 + n]]
    pre = [0] * (n + 1)
    for i, v in enumerate(a):
        pre[i + 1] = pre[i] + v
    best = None
    worst = None
    for l in range(n):
        for r in range(l + 1, n + 1):
            s = pre[r] - pre[l]
            if best is None or s > best:
                best = s
            if worst is None or s < worst:
                worst = s
    return "max=%d\nmin=%d\n" % (best, worst)


add(
    title="new 动态数组求最大最小子段和",
    section=SEC_06,
    difficulty=3, score=20,
    tags=["C++数组与指针", "动态内存", "Kadane", "复杂度"],
    statement_md=(
        "读入 `n` 个整数，求**非空连续子段**的最大和与最小和。\n\n"
        "★ 为什么题面强调 `new` / `delete[]`：第 6 讲的核心是「数组名不是指针，但会退化成指针」。"
        "要用运行时才定下来的 `n` 开数组，标准做法是 `int* a = new int[n];` …… "
        "用完必须 `delete[] a;` —— **`new[]` 配 `delete[]`**，配错了就是未定义行为。\n\n"
        "★ 正解是 Kadane，一遍 O(n)：\n\n"
        "```cpp\n"
        "cur = max(a[i], cur + a[i]);   // 要么接着上一段，要么从自己重新开始\n"
        "best = max(best, cur);\n"
        "```\n\n"
        "最小和把比较方向反过来即可（也可以用「取负求最大再取负」，但注意溢出）。\n\n"
        "⚠️ 这题的坑几乎全在初始化：\n"
        "1. `best` 不能初始化成 0 —— 全是负数时正确答案是「最大的那个负数」，"
        "初始化成 0 会输出 0；必须用 `a[0]` 起步；\n"
        "2. 子段必须非空，所以不能用「空前缀」当答案；\n"
        "3. 累加用 `long long`：本题上界 1000×10⁴ = 10⁷，`int` 还撑得住；"
        "但真实数据一上到 10⁵ 就溢出，一律用 64 位是省心的习惯。"
    ),
    input_format="第一行 `n`；第二行 `n` 个整数。",
    output_format="两行：`max=<最大子段和>`、`min=<最小子段和>`。",
    constraints_md="- 1 ≤ n ≤ 1000\n- |aᵢ| ≤ 10⁴\n- 子段非空；结果用 `long long`",
    inputs=[
        "5\n1 -2 3 4 -1\n",
        "3\n-5 -2 -9\n",
        "1\n7\n",
        "6\n2 -8 3 -2 4 -10\n",
        "4\n0 0 0 0\n",
        "8\n10000 -10000 10000 -10000 10000 -10000 10000 -10000\n",
    ],
    samples=3,
    oracle=_oracle_06b,
    solution=r'''#include <cstdio>
using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;

    // 运行时才知道 n，只能用 new[]；配对释放必须是 delete[]
    long long* a = new long long[n];
    for (int i = 0; i < n; i++) scanf("%lld", &a[i]);

    long long curMax = a[0], bestMax = a[0];
    long long curMin = a[0], bestMin = a[0];
    for (int i = 1; i < n; i++) {
        curMax = (curMax + a[i] > a[i]) ? curMax + a[i] : a[i];
        if (curMax > bestMax) bestMax = curMax;
        curMin = (curMin + a[i] < a[i]) ? curMin + a[i] : a[i];
        if (curMin < bestMin) bestMin = curMin;
    }

    printf("max=%lld\nmin=%lld\n", bestMax, bestMin);
    delete[] a;                       // 与 new[] 配对
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;

// 独立点：完全不用 Kadane，改成分治 —— 跨中点的最优子段 = 左半最大后缀 + 右半最大前缀。
// 求最小和时把数组取负做同一套分治再取负回来。
struct Node { long long sum, pref, suff, best; };

static Node combine(const Node& L, const Node& R) {
    Node r;
    r.sum  = L.sum + R.sum;
    r.pref = max(L.pref, L.sum + R.pref);
    r.suff = max(R.suff, R.sum + L.suff);
    r.best = max(max(L.best, R.best), L.suff + R.pref);
    return r;
}

static Node solve(const vector<long long>& a, int l, int r) {   // [l, r)
    if (r - l == 1) return {a[l], a[l], a[l], a[l]};
    int m = (l + r) / 2;
    return combine(solve(a, l, m), solve(a, m, r));
}

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<long long> a(n), b(n);
    for (int i = 0; i < n; i++) { scanf("%lld", &a[i]); b[i] = -a[i]; }

    long long bestMax = solve(a, 0, n).best;
    long long bestMin = -solve(b, 0, n).best;    // 最小和 = -(取负后的最大和)
    printf("max=%lld\nmin=%lld\n", bestMax, bestMin);
    return 0;
}
''',
)


# ===================================================================== #
#  第 07 讲 · 类的继承
# ===================================================================== #

def _oracle_07(text: str) -> str:
    """账户派生类：用「类型字段 + 分情况处理」的扁平字典模拟，不建类层次。"""
    d = text.split()
    pos = 0
    m = int(d[pos]); pos += 1
    acc: dict[int, list] = {}
    for _ in range(m):
        kind = d[pos]; pos += 1
        aid = int(d[pos]); bal = int(d[pos + 1]); extra = int(d[pos + 2]); pos += 3
        acc[aid] = [kind, bal, extra]          # extra: 储蓄=利率(千分比)，信用=额度
    q = int(d[pos]); pos += 1
    total_interest = 0
    out = []
    for _ in range(q):
        op = d[pos]; pos += 1
        aid = int(d[pos]); pos += 1
        rec = acc[aid]
        kind, bal, extra = rec
        if op == "D":
            amt = int(d[pos]); pos += 1
            rec[1] = bal + amt
            out.append("D %d %d -> %d" % (aid, amt, rec[1]))
        elif op == "W":
            amt = int(d[pos]); pos += 1
            if kind == "S":
                ok = amt <= bal
            else:
                ok = bal - amt >= -extra
            if ok:
                rec[1] = bal - amt
                out.append("W %d %d -> %d" % (aid, amt, rec[1]))
            else:
                out.append("W %d %d FAILED" % (aid, amt))
        else:  # Y
            years = int(d[pos]); pos += 1
            if kind != "S":
                out.append("Y %d %d SKIP" % (aid, years))
            else:
                interest = rec[1] * extra * years // 1000
                rec[1] += interest
                total_interest += interest
                out.append("Y %d %d interest=%d -> %d" % (aid, years, interest, rec[1]))
    out.append("TOTAL interest=%d" % total_interest)
    return "\n".join(out) + "\n"


add(
    title="账户派生类的利息结算",
    section=SEC_07,
    difficulty=3, score=20,
    tags=["C++继承", "protected", "派生类构造", "同名遮蔽"],
    statement_md=(
        "在 `Account` 基类（`id`、`balance`，能存能取、余额不足则取款失败）上派生出两个类：\n\n"
        "- `SavingsAccount`：多一个利率 `rate`（**千分比**整数，15 表示 1.5%），"
        "提供 `settle(years)`：`利息 = 余额 × rate × years / 1000`（整数除法截断），利息计入余额；\n"
        "- `CreditAccount`：多一个透支额度 `limit`，**重写**取款规则：余额可以取到 `-limit` 为止。\n\n"
        "指令：`D id amt` 存款、`W id amt` 取款、`Y id years` 结算利息（信用账户输出 `SKIP`）。"
        "每条指令输出一行，最后输出 `TOTAL interest=<所有储蓄账户利息之和>`。\n\n"
        "★ 为什么余额要放 `protected` 而不是 `private`：派生类的 `settle` 想直接改余额，"
        "`private` 的墙连派生类也拦；`protected` 正好是「自己人可进、外人不可进」的折中。"
        "（第 7 讲也提醒过：这是继承版的妥协 —— 更干净的办法是让基类提供 `record()`。）\n\n"
        "★ 为什么这题不写成 `Account* p = &sa;` 统一调用：本讲**还没有虚函数**，"
        "经基类指针调到的永远是基类那一版（静态绑定），信用账户的透支规则会被吃掉 —— "
        "这正是第 8 讲要引入 `virtual` 的原因。\n\n"
        "⚠️ 构造链：派生类构造函数必须在**初始化列表**里把 `id/balance` 递给基类，"
        "基类构造不接受参数就得自己写默认构造。\n\n"
        "⚠️ 利息用**整数**算：先乘后除、截断向下（余额非负，所以等价于向零取整），"
        "别用 `double` —— 浮点会有 `0.9999` 这类尾差。"
    ),
    input_format=("第一行 `m`；随后 `m` 行：`S id bal rate` 或 `C id bal limit`。\n"
                  "接着一行 `q`；随后 `q` 行：`D id amt` / `W id amt` / `Y id years`。"),
    output_format=("每条指令一行：`D id amt -> 余额`、`W id amt -> 余额`（失败为 `W id amt FAILED`）、"
                   "`Y id years interest=利息 -> 余额`（信用账户为 `Y id years SKIP`）。"
                   "最后一行 `TOTAL interest=总和`。"),
    constraints_md="- 1 ≤ m, q ≤ 10⁵\n- 0 ≤ bal, amt, limit ≤ 10⁹\n- 1 ≤ rate ≤ 1000，0 ≤ years ≤ 100",
    inputs=[
        "2\nS 1 10000 15\nC 2 0 5000\n6\nD 1 1000\nW 2 3000\nW 2 3000\nY 1 1\nY 2 1\nW 1 200\n",
        "1\nS 9 100 1000\n2\nY 9 2\nW 9 1\n",
        "1\nC 4 100 0\n3\nW 4 100\nW 4 1\nD 4 5\n",
        "2\nS 1 0 500\nS 2 1000 1\n4\nY 1 3\nY 2 7\nD 1 250\nY 1 4\n",
        "1\nS 5 999 333\n2\nY 5 1\nY 5 3\n",
        "2\nC 1 10 20\nS 2 20 25\n5\nW 1 30\nW 1 31\nY 2 4\nD 1 100\nW 1 130\n",
    ],
    samples=3,
    oracle=_oracle_07,
    solution=r'''#include <cstdio>
#include <map>
using namespace std;

class Account {
protected:
    int id_;
    long long balance_;
    void record(long long amount) { balance_ += amount; }   // 给派生类留的口子
public:
    Account(int id, long long balance = 0) : id_(id), balance_(balance) {}
    int id() const { return id_; }
    long long balance() const { return balance_; }
    void deposit(long long amount) { record(amount); }
    bool withdraw(long long amount) {
        if (amount > balance_) return false;
        record(-amount);
        return true;
    }
};

class SavingsAccount : public Account {
private:
    long long rate_;                    // 千分比
public:
    SavingsAccount(int id, long long balance, long long rate)
        : Account(id, balance), rate_(rate) {}          // 构造链：参数递给基类
    long long settle(int years) {
        long long interest = balance_ * rate_ * years / 1000;
        record(interest);
        return interest;
    }
};

class CreditAccount : public Account {
private:
    long long limit_;
public:
    CreditAccount(int id, long long balance, long long limit)
        : Account(id, balance), limit_(limit) {}
    // 同名遮蔽：这是派生类自己的取款规则，经基类指针调不到（本讲还没 virtual）
    bool withdraw(long long amount) {
        if (balance_ - amount < -limit_) return false;
        record(-amount);
        return true;
    }
};

int main() {
    int m;
    if (scanf("%d", &m) != 1) return 0;
    map<int, SavingsAccount*> sav;
    map<int, CreditAccount*> cre;
    for (int i = 0; i < m; i++) {
        char kind[4];
        int id; long long bal, extra;
        scanf("%s %d %lld %lld", kind, &id, &bal, &extra);
        if (kind[0] == 'S') sav[id] = new SavingsAccount(id, bal, extra);
        else                cre[id] = new CreditAccount(id, bal, extra);
    }

    int q;
    scanf("%d", &q);
    long long totalInterest = 0;
    char op[4];
    for (int i = 0; i < q; i++) {
        scanf("%s", op);
        int id;
        scanf("%d", &id);
        if (op[0] == 'D') {
            long long amt;
            scanf("%lld", &amt);
            auto s = sav.find(id);
            if (s != sav.end()) { s->second->deposit(amt); printf("D %d %lld -> %lld\n", id, amt, s->second->balance()); }
            else { auto c = cre.find(id); c->second->deposit(amt); printf("D %d %lld -> %lld\n", id, amt, c->second->balance()); }
        } else if (op[0] == 'W') {
            long long amt;
            scanf("%lld", &amt);
            bool ok;
            long long now;
            auto s = sav.find(id);
            if (s != sav.end()) { ok = s->second->withdraw(amt); now = s->second->balance(); }
            else { auto c = cre.find(id); ok = c->second->withdraw(amt); now = c->second->balance(); }
            if (ok) printf("W %d %lld -> %lld\n", id, amt, now);
            else    printf("W %d %lld FAILED\n", id, amt);
        } else {
            int years;
            scanf("%d", &years);
            auto s = sav.find(id);
            if (s == sav.end()) {
                printf("Y %d %d SKIP\n", id, years);
            } else {
                long long in = s->second->settle(years);
                totalInterest += in;
                printf("Y %d %d interest=%lld -> %lld\n", id, years, in, s->second->balance());
            }
        }
    }
    printf("TOTAL interest=%lld\n", totalInterest);
    for (auto& kv : sav) delete kv.second;
    for (auto& kv : cre) delete kv.second;
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <map>
using namespace std;

// 独立点：账户**按值**放进容器（不开堆、不 delete），且把「利息累计」交给
// 一个独立的累加器结构，而不是 main 里的裸变量。
// 类层次与语义完全一致，只是对象管理方式换了。
class Account {
protected:
    int id_;
    long long balance_;
    void record(long long amount) { balance_ += amount; }
public:
    Account(int id = 0, long long balance = 0) : id_(id), balance_(balance) {}
    long long balance() const { return balance_; }
    void deposit(long long amount) { record(amount); }
    bool withdraw(long long amount) {
        if (amount > balance_) return false;
        record(-amount);
        return true;
    }
};

class SavingsAccount : public Account {
    long long rate_;
public:
    SavingsAccount(int id = 0, long long balance = 0, long long rate = 0)
        : Account(id, balance), rate_(rate) {}
    long long settle(int years) {
        long long interest = balance_ * rate_ * years / 1000;
        record(interest);
        return interest;
    }
};

class CreditAccount : public Account {
    long long limit_;
public:
    CreditAccount(int id = 0, long long balance = 0, long long limit = 0)
        : Account(id, balance), limit_(limit) {}
    bool withdraw(long long amount) {
        if (balance_ - amount < -limit_) return false;
        record(-amount);
        return true;
    }
};

int main() {
    int m;
    if (scanf("%d", &m) != 1) return 0;
    map<int, SavingsAccount> sav;
    map<int, CreditAccount> cre;
    for (int i = 0; i < m; i++) {
        char kind[4];
        int id; long long bal, extra;
        scanf("%s %d %lld %lld", kind, &id, &bal, &extra);
        if (kind[0] == 'S') sav[id] = SavingsAccount(id, bal, extra);
        else                cre[id] = CreditAccount(id, bal, extra);
    }

    int q;
    scanf("%d", &q);
    long long totalInterest = 0;
    char op[4];
    for (int i = 0; i < q; i++) {
        scanf("%s", op);
        int id; scanf("%d", &id);
        if (op[0] == 'Y') {
            int years; scanf("%d", &years);
            auto s = sav.find(id);
            if (s == sav.end()) { printf("Y %d %d SKIP\n", id, years); continue; }
            long long in = s->second.settle(years);
            totalInterest += in;
            printf("Y %d %d interest=%lld -> %lld\n", id, years, in, s->second.balance());
            continue;
        }
        long long amt; scanf("%lld", &amt);
        auto s = sav.find(id);
        if (op[0] == 'D') {
            if (s != sav.end()) s->second.deposit(amt);
            else cre[id].deposit(amt);
            printf("D %d %lld -> %lld\n", id, amt,
                   s != sav.end() ? s->second.balance() : cre[id].balance());
        } else {
            bool ok; long long now;
            if (s != sav.end()) { ok = s->second.withdraw(amt); now = s->second.balance(); }
            else { ok = cre[id].withdraw(amt); now = cre[id].balance(); }
            if (ok) printf("W %d %lld -> %lld\n", id, amt, now);
            else    printf("W %d %lld FAILED\n", id, amt);
        }
    }
    printf("TOTAL interest=%lld\n", totalInterest);
    return 0;
}
''',
)


# ===================================================================== #
#  第 08 讲 · 多态性
# ===================================================================== #

def _oracle_08a(text: str) -> str:
    """复数：用元组手算 +、✕、==（没有运算符重载这回事）。"""
    d = text.split()
    n = int(d[0])
    nums = []
    for i in range(n):
        nums.append((int(d[1 + 2 * i]), int(d[2 + 2 * i])))
    sr = si = 0
    pr, pi = 1, 0
    for r, i in nums:
        sr += r
        si += i
        pr, pi = pr * r - pi * i, pr * i + pi * r
    return "sum=(%d, %d)\nprod=(%d, %d)\neq=%d\n" % (
        sr, si, pr, pi, 1 if (sr == pr and si == pi) else 0)


add(
    title="复数类的运算符重载",
    section=SEC_08,
    difficulty=3, score=20,
    tags=["C++多态性", "运算符重载", "友元", "常成员函数"],
    statement_md=(
        "实现 `Complex` 类（实部、虚部都是**整数**），重载 `+`、`*`、`==` 和 `<<`，"
        "读入 `n` 个复数，输出：\n\n"
        "```text\n"
        "sum=(a, b)\n"
        "prod=(a, b)\n"
        "eq=0\n"
        "```\n\n"
        "`sum` 是全部相加，`prod` 是全部相乘（乘法的单位元是 `1+0i`），"
        "`eq` 表示两者是否相等。输出格式固定为 `(实部, 虚部)` —— **逗号后有一个空格**。\n\n"
        "★ 为什么 `operator<<` 必须是**非成员**函数：`cout << c` 的左操作数是 `ostream`，"
        "而成员版的左操作数只能是本类对象。想给 `ostream` 加成员函数是不可能的，"
        "所以只能写成 `ostream& operator<<(ostream&, const Complex&)`；"
        "要读私有成员就在类里写 `friend` 声明 —— 友元不是可选项。\n\n"
        "★ `+` 和 `*` 写成**成员**函数：左操作数天然是 `*this`，右操作数是形参。"
        "但 `1 + c` 这种「整数在左边」的写法成员版接不住（`1` 不是 Complex），"
        "要支持就得再加非成员版重载 —— 本题不要求。\n\n"
        "⚠️ 乘法公式别记错：`(a+bi)(c+di) = (ac−bd) + (ad+bc)i`。"
        "写成 `ac+bd` 是最常见的错。\n\n"
        "⚠️ 返回类型：`+` / `*` 返回**新对象**（不能返回引用，局部对象出了函数就没了）；"
        "`==` 返回 `bool` 且必须是 `const` 成员函数，否则常对象调不了。"
    ),
    input_format="第一行 `n`；随后 `n` 行，每行两个整数 `a b`（表示 `a+bi`）。",
    output_format="三行：`sum=(实部, 虚部)`、`prod=(实部, 虚部)`、`eq=0/1`。",
    constraints_md="- 1 ≤ n ≤ 6\n- |a|, |b| ≤ 100\n- 结果 ∣实部∣、∣虚部∣ < 10¹⁴，用 `long long`",
    inputs=[
        "2\n1 2\n3 4\n",
        "1\n5 -3\n",
        "3\n1 0\n0 1\n1 1\n",
        "2\n0 0\n0 0\n",
        "2\n1 1\n1 -1\n",
        "4\n-100 100\n100 -100\n-1 -1\n2 2\n",
    ],
    samples=3,
    oracle=_oracle_08a,
    solution=r'''#include <cstdio>
#include <iostream>
using namespace std;

class Complex {
private:
    long long real_, imag_;
public:
    Complex(long long r = 0, long long i = 0) : real_(r), imag_(i) {}

    // 双目 +：左操作数是 *this
    Complex operator+(const Complex& o) const {
        return Complex(real_ + o.real_, imag_ + o.imag_);
    }
    Complex operator*(const Complex& o) const {
        return Complex(real_ * o.real_ - imag_ * o.imag_,
                       real_ * o.imag_ + imag_ * o.real_);
    }
    bool operator==(const Complex& o) const {
        return real_ == o.real_ && imag_ == o.imag_;
    }
    // 非成员版必须声明为友元才能读私有成员
    friend ostream& operator<<(ostream& os, const Complex& c);
};

ostream& operator<<(ostream& os, const Complex& c) {
    os << "(" << c.real_ << ", " << c.imag_ << ")";
    return os;                 // 返回流本身才能连锁 <<
}

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    Complex sum(0, 0), prod(1, 0);
    for (int i = 0; i < n; i++) {
        long long a, b;
        scanf("%lld %lld", &a, &b);
        Complex c(a, b);
        sum = sum + c;
        prod = prod * c;
    }
    cout << "sum=" << sum << '\n';
    cout << "prod=" << prod << '\n';
    cout << "eq=" << (sum == prod ? 1 : 0) << '\n';
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <iostream>
#include <vector>
using namespace std;

// 独立点：所有运算符都写成**非成员**的友元函数（参考解是成员版 + 一个非成员 <<），
// 并且把累加/累乘交给 std::accumulate 的 lambda，不手写循环。
class Complex {
    long long real_, imag_;
public:
    Complex(long long r = 0, long long i = 0) : real_(r), imag_(i) {}
    long long real() const { return real_; }
    long long imag() const { return imag_; }
    friend Complex operator+(const Complex& a, const Complex& b);
    friend Complex operator*(const Complex& a, const Complex& b);
    friend bool operator==(const Complex& a, const Complex& b);
    friend ostream& operator<<(ostream& os, const Complex& c);
};

Complex operator+(const Complex& a, const Complex& b) {
    return Complex(a.real_ + b.real_, a.imag_ + b.imag_);
}
Complex operator*(const Complex& a, const Complex& b) {
    return Complex(a.real_ * b.real_ - a.imag_ * b.imag_,
                   a.real_ * b.imag_ + a.imag_ * b.real_);
}
bool operator==(const Complex& a, const Complex& b) {
    return a.real_ == b.real_ && a.imag_ == b.imag_;
}
ostream& operator<<(ostream& os, const Complex& c) {
    os << "(" << c.real_ << ", " << c.imag_ << ")";
    return os;
}

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<Complex> v;
    for (int i = 0; i < n; i++) {
        long long a, b;
        scanf("%lld %lld", &a, &b);
        v.push_back(Complex(a, b));
    }

    Complex sum(0, 0), prod(1, 0);
    for (size_t i = 0; i < v.size(); i++) { sum = sum + v[i]; prod = prod * v[i]; }

    cout << "sum=" << sum << '\n';
    cout << "prod=" << prod << '\n';
    cout << "eq=" << (sum == prod ? 1 : 0) << '\n';
    return 0;
}
''',
)


def _oracle_08b(text: str) -> str:
    """图形面积：按类型分支直接算，没有虚函数这回事。"""
    d = text.split()
    q = int(d[0])
    pos = 1
    areas = []
    names = []
    cnt = {"R": 0, "S": 0, "T": 0}
    for _ in range(q):
        kind = d[pos]; pos += 1
        if kind == "S":
            a = int(d[pos]); pos += 1
            area = a * a; name = "Square"
        else:
            a = int(d[pos]); b = int(d[pos + 1]); pos += 2
            if kind == "R":
                area = a * b; name = "Rect"
            else:
                area = a * b // 2; name = "Tri"
        cnt[kind] += 1
        areas.append(area)
        names.append(name)
    best = 0
    for i in range(1, q):
        if areas[i] > areas[best]:
            best = i
    return "total=%d\nmax=%s %d\ncount R=%d S=%d T=%d\n" % (
        sum(areas), names[best], areas[best], cnt["R"], cnt["S"], cnt["T"])


add(
    title="抽象图形类的虚函数面积求和",
    section=SEC_08,
    difficulty=4, score=25,
    tags=["C++多态性", "虚函数", "抽象类", "虚析构"],
    statement_md=(
        "定义**抽象类** `Shape`：`virtual long long area() const = 0;`、"
        "`virtual const char* name() const = 0;`、`virtual ~Shape() {}`。"
        "派生出三个具体类：\n\n"
        "| 类型 | 输入 | 面积 | `name()` |\n|---|---|---|---|\n"
        "| `R w h` | 矩形 | `w × h` | `Rect` |\n"
        "| `S s` | 正方形 | `s × s` | `Square` |\n"
        "| `T b h` | 直角三角形 | `b × h / 2` | `Tri` |\n\n"
        "把对象**用 `Shape*` 存进 `vector<Shape*>`**，只用基类指针遍历算总面积、"
        "找面积最大的图形（并列取**最先出现**的那个），最后统计各类个数。\n\n"
        "★ 为什么必须 `virtual`：`Shape* p` 的静态类型是 `Shape`，"
        "没有 `virtual` 时编译器只能按声明类型绑定到 `Shape::area()` —— "
        "而它是纯虚的，根本调不了。加了 `virtual` 才会在运行期按**实际类型**查表（vtable）分派。\n\n"
        "★ 为什么基类要 `virtual ~Shape()`：最后 `delete` 这些指针时，"
        "若析构不是虚的，只析构 `Shape` 那部分，派生类的成员全泄漏。"
        "「有虚函数的类就该有虚析构」是硬规矩。\n\n"
        "⚠️ 边界：\n"
        "1. `T` 的 `b×h` 保证是偶数，面积是整数，不会出现 0.5；\n"
        "2. 面积相同的图形可能有多个，取**先出现**的，别用 `>=` 更新；\n"
        "3. 面积用 `long long`：`w,h` 可到 10⁹，乘积到 10¹⁸。"
    ),
    input_format="第一行 `q`；随后 `q` 行，每行 `R w h` / `S s` / `T b h`。",
    output_format=("三行：`total=<总面积>`、`max=<类名> <面积>`、"
                   "`count R=<矩形数> S=<正方形数> T=<三角形数>`。"),
    constraints_md="- 1 ≤ q ≤ 10⁵\n- 1 ≤ w, h, s ≤ 10⁹（`T` 的 `b×h` 为偶数）\n- 面积用 `long long`",
    inputs=[
        "3\nR 2 3\nS 2\nT 4 3\n",
        "1\nS 7\n",
        "4\nR 1 1\nS 1\nT 2 1\nR 1 1\n",
        "3\nT 2 3\nR 3 1\nS 1\n",
        "2\nR 1000000000 1000000000\nS 999999999\n",
        "5\nS 2\nR 2 2\nT 4 2\nR 2 2\nT 8 1\n",
    ],
    samples=3,
    oracle=_oracle_08b,
    solution=r'''#include <cstdio>
#include <vector>
using namespace std;

class Shape {
public:
    virtual long long area() const = 0;         // 纯虚：只定合同
    virtual const char* name() const = 0;
    virtual ~Shape() {}                         // 虚析构：经基类指针 delete 才安全
};

class Rect : public Shape {
    long long w_, h_;
public:
    Rect(long long w, long long h) : w_(w), h_(h) {}
    long long area() const override { return w_ * h_; }
    const char* name() const override { return "Rect"; }
};

class Square : public Shape {
    long long s_;
public:
    explicit Square(long long s) : s_(s) {}
    long long area() const override { return s_ * s_; }
    const char* name() const override { return "Square"; }
};

class Tri : public Shape {
    long long b_, h_;
public:
    Tri(long long b, long long h) : b_(b), h_(h) {}
    long long area() const override { return b_ * h_ / 2; }
    const char* name() const override { return "Tri"; }
};

int main() {
    int q;
    if (scanf("%d", &q) != 1) return 0;

    vector<Shape*> shapes;
    int cr = 0, cs = 0, ct = 0;
    for (int i = 0; i < q; i++) {
        char kind[4];
        long long a, b = 0;
        scanf("%s %lld", kind, &a);
        if (kind[0] == 'S') {
            shapes.push_back(new Square(a)); cs++;
        } else {
            scanf("%lld", &b);
            if (kind[0] == 'R') { shapes.push_back(new Rect(a, b)); cr++; }
            else                { shapes.push_back(new Tri(a, b)); ct++; }
        }
    }

    long long total = 0;
    int best = 0;
    for (int i = 0; i < (int)shapes.size(); i++) {
        long long ar = shapes[i]->area();       // 动态绑定
        total += ar;
        if (ar > shapes[best]->area()) best = i;   // 严格大于：并列取先出现的
    }

    printf("total=%lld\n", total);
    printf("max=%s %lld\n", shapes[best]->name(), shapes[best]->area());
    printf("count R=%d S=%d T=%d\n", cr, cs, ct);

    for (Shape* p : shapes) delete p;           // 虚析构保证派生类部分也释放
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <vector>
#include <memory>
#include <algorithm>
using namespace std;

// 独立点：容器用 vector<unique_ptr<Shape>> 管生命周期（不手写 delete），
// 最大值改用 std::max_element + 自定义比较器（比较 area()）。
// 类层次相同，但「谁负责释放」和「怎么找最大」都换了实现。
class Shape {
public:
    virtual long long area() const = 0;
    virtual const char* name() const = 0;
    virtual ~Shape() = default;
};

struct Rect : Shape {
    long long w, h;
    Rect(long long a, long long b) : w(a), h(b) {}
    long long area() const override { return w * h; }
    const char* name() const override { return "Rect"; }
};
struct Square : Shape {
    long long s;
    explicit Square(long long a) : s(a) {}
    long long area() const override { return s * s; }
    const char* name() const override { return "Square"; }
};
struct Tri : Shape {
    long long b, h;
    Tri(long long x, long long y) : b(x), h(y) {}
    long long area() const override { return b * h / 2; }
    const char* name() const override { return "Tri"; }
};

int main() {
    int q;
    if (scanf("%d", &q) != 1) return 0;

    vector<unique_ptr<Shape>> shapes;
    int cr = 0, cs = 0, ct = 0;
    for (int i = 0; i < q; i++) {
        char kind[4];
        long long a, b = 0;
        scanf("%s %lld", kind, &a);
        if (kind[0] == 'S') { shapes.emplace_back(new Square(a)); cs++; }
        else {
            scanf("%lld", &b);
            if (kind[0] == 'R') { shapes.emplace_back(new Rect(a, b)); cr++; }
            else                { shapes.emplace_back(new Tri(a, b)); ct++; }
        }
    }

    long long total = 0;
    for (auto& p : shapes) total += p->area();
    auto best = max_element(shapes.begin(), shapes.end(),
        [](const unique_ptr<Shape>& x, const unique_ptr<Shape>& y) {
            return x->area() < y->area();          // 严格小于 => 并列留第一个
        });

    printf("total=%lld\n", total);
    printf("max=%s %lld\n", (*best)->name(), (*best)->area());
    printf("count R=%d S=%d T=%d\n", cr, cs, ct);
    return 0;
}
''',
)


# ===================================================================== #
#  第 09 讲 · 模板与群体数据
# ===================================================================== #

def _oracle_09(text: str) -> str:
    """逆波兰求值：用 Python 列表当栈，操作符分情况（与类模板无关的直白写法）。"""
    toks = text.split()
    q = int(toks[0])
    items = toks[1:1 + q]
    st: list[int] = []
    max_depth = 0
    for t in items:
        if t in ("+", "-", "*", "/"):
            b = st.pop()
            a = st.pop()
            if t == "+":
                st.append(a + b)
            elif t == "-":
                st.append(a - b)
            elif t == "*":
                st.append(a * b)
            else:
                q2 = abs(a) // abs(b)
                st.append(q2 if (a >= 0) == (b >= 0) else -q2)
        else:
            st.append(int(t))
            max_depth = max(max_depth, len(st))
    return "value=%d\nmaxdepth=%d\n" % (st[-1], max_depth)


add(
    title="类模板 Stack 求逆波兰表达式",
    section=SEC_09,
    difficulty=4, score=25,
    tags=["C++模板", "类模板", "栈", "后缀表达式"],
    statement_md=(
        "把讲义里的栈类模板化：`template <typename T> class Stack`，"
        "支持 `push` / `pop` / `size`，容量不够时自动翻倍。然后用 `Stack<long long>` "
        "求一个**后缀（逆波兰）表达式**的值，同时统计过程中栈达到过的最大深度。\n\n"
        "输入是一串 token：整数或 `+ - * /`。除法保证能整除、除数不为 0。\n\n"
        "★ 为什么这题适合用类模板：求值本身与「存什么类型」无关，"
        "同一份 `Stack<T>` 既能装 `int`、`long long`，也能装 `char`（拿去写括号匹配）。"
        "模板不是运行期的东西，是**给编译器的图纸** —— 你写 `Stack<long long>` 时，"
        "编译器才照着图纸生成一个专门的类。\n\n"
        "★ 类模板的两个硬规矩：\n"
        "1. 使用时**必须显式**给类型参数（`Stack<long long> st;`），编译器推不出来；\n"
        "2. 成员函数在类外定义时要写两遍前缀：`template <typename T>` + `Stack<T>::`。\n\n"
        "⚠️ 求值的减法和除法**不能交换**：先弹出的是右操作数 `b`，后弹出的是左操作数 `a`，"
        "算的是 `a - b`、`a / b`。反了就是 `b - a`，一半用例会错得莫名其妙。\n\n"
        "⚠️ 栈的 `pop` 建议写成 `bool pop(T& out)`：空栈返回 false，而不是让调用方去猜。"
    ),
    input_format="第一行 `q`（token 个数）；随后 `q` 个 token，空格或换行分隔。",
    output_format="两行：`value=<表达式的值>`、`maxdepth=<过程中栈的最大深度>`。",
    constraints_md="- 1 ≤ q ≤ 10⁵\n- 保证表达式合法；除法整除、除数非 0\n- 结果与中间值用 `long long`",
    inputs=[
        "3\n2 3 +\n",
        "5\n2 3 + 4 *\n",
        "7\n5 1 2 + 4 * + 3 -\n",
        "1\n42\n",
        "5\n-8 2 / -3 +\n",
        "7\n1000000 1000000 * 1000000 * 2 /\n",
    ],
    samples=3,
    oracle=_oracle_09,
    solution=r'''#include <cstdio>
#include <string>
#include <iostream>
#include <cstdlib>
using namespace std;

template <typename T>
class Stack {
private:
    T* data_;
    int top_, cap_;
    void grow() {
        int nc = cap_ * 2;
        T* nd = new T[nc];
        for (int i = 0; i < top_; i++) nd[i] = data_[i];
        delete[] data_;
        data_ = nd;
        cap_ = nc;
    }
public:
    explicit Stack(int cap = 8) : data_(new T[cap]), top_(0), cap_(cap) {}
    ~Stack() { delete[] data_; }
    Stack(const Stack&) = delete;               // 含裸指针，禁止浅复制
    Stack& operator=(const Stack&) = delete;

    void push(const T& e) {
        if (top_ == cap_) grow();
        data_[top_++] = e;
    }
    bool pop(T& out) {
        if (top_ == 0) return false;
        out = data_[--top_];
        return true;
    }
    int size() const { return top_; }
    bool empty() const { return top_ == 0; }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int q;
    if (!(cin >> q)) return 0;

    Stack<long long> st;
    int maxDepth = 0;
    for (int i = 0; i < q; i++) {
        string tok;
        cin >> tok;
        if (tok.size() == 1 && (tok[0] == '+' || tok[0] == '-' ||
                                tok[0] == '*' || tok[0] == '/')) {
            long long b = 0, a = 0;
            st.pop(b);
            st.pop(a);
            long long r = 0;
            if (tok[0] == '+') r = a + b;
            else if (tok[0] == '-') r = a - b;
            else if (tok[0] == '*') r = a * b;
            else r = a / b;                     // 保证整除
            st.push(r);
        } else {
            st.push(atoll(tok.c_str()));
            if (st.size() > maxDepth) maxDepth = st.size();
        }
    }

    long long v = 0;
    st.pop(v);
    printf("value=%lld\n", v);
    printf("maxdepth=%d\n", maxDepth);
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <vector>
#include <string>
#include <iostream>
#include <cstdlib>
using namespace std;

// 独立点：类模板内部换成 std::vector<T> 当存储（不自己 new[]/delete[]），
// 求值循环改用「双栈 + 显式长度记录」的写法，输出口径不变。
template <typename T>
class Stack {
    vector<T> v_;
public:
    void push(const T& e) { v_.push_back(e); }
    bool pop(T& out) {
        if (v_.empty()) return false;
        out = v_.back();
        v_.pop_back();
        return true;
    }
    int size() const { return (int)v_.size(); }
    bool empty() const { return v_.empty(); }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int q;
    if (!(cin >> q)) return 0;

    Stack<long long> operands;
    int maxDepth = 0;
    for (int i = 0; i < q; i++) {
        string tok;
        cin >> tok;
        char c = tok.size() == 1 ? tok[0] : '\0';
        if (c == '+' || c == '-' || c == '*' || c == '/') {
            long long b, a;
            operands.pop(b);
            operands.pop(a);
            switch (c) {
                case '+': operands.push(a + b); break;
                case '-': operands.push(a - b); break;
                case '*': operands.push(a * b); break;
                default:  operands.push(a / b); break;
            }
        } else {
            operands.push(strtoll(tok.c_str(), nullptr, 10));
            if (operands.size() > maxDepth) maxDepth = operands.size();
        }
    }

    long long v;
    operands.pop(v);
    printf("value=%lld\n", v);
    printf("maxdepth=%d\n", maxDepth);
    return 0;
}
''',
)


# ===================================================================== #
#  第 10 讲 · 泛型程序设计与 STL
# ===================================================================== #

def _oracle_10a(text: str) -> str:
    """词频榜：Counter + 两趟排序（先按词字典序、再按次数稳定降序）。"""
    from collections import Counter
    import re

    lines = text.split("\n")
    k = int(lines[0].split()[0])
    body = "\n".join(lines[1:])
    words = [w.lower() for w in re.findall(r"[0-9A-Za-z]+", body)]
    cnt = Counter(words)
    items = list(cnt.items())
    items.sort(key=lambda p: p[0])                       # 先字典序
    items.sort(key=lambda p: -p[1])                      # 再稳定地按次数降序
    out = ["%s %d" % (w, c) for w, c in items[:k]]
    return "\n".join(out) + "\n"


add(
    title="map 词频榜（同频按字典序）",
    section=SEC_10,
    difficulty=3, score=20,
    tags=["STL", "map", "排序", "lambda"],
    statement_md=(
        "读入一行文本，统计每个单词出现的次数（**统一转小写**，单词 = 连续的字母或数字），"
        "输出出现次数最多的前 `k` 个：次数相同的按**字典序升序**排。\n\n"
        "每行输出 `单词 次数`（一个空格）。不同单词少于 `k` 个时，有多少输出多少。\n\n"
        "★ 为什么用 `map<string,int>` 计数：`map` 是红黑树，键天然有序且插入/查找 O(log n)，"
        "`++cnt[w]` 一行就完成「没有就插入 0 再自增」。"
        "（顺带记住讲义 10.5 的坑：`cnt[w]` **查询也会插入**，只想查就改用 `find`。）\n\n"
        "★ 排序为什么要拷进 `vector`：`map` 只能按键排，本题要按**值**排，"
        "所以先把 `(词, 次数)` 拷进 `vector<pair<string,int>>` 再 `sort`，比较器写成\n\n"
        "```cpp\n"
        "[](const auto& a, const auto& b) {\n"
        "    if (a.second != b.second) return a.second > b.second;  // 次数降序\n"
        "    return a.first < b.first;                              // 同频字典序升序\n"
        "}\n"
        "```\n\n"
        "⚠️ 只用「次数降序」一个键是错的：同频时 `sort` 不保证顺序（不稳定），"
        "结果会随实现变化 —— 必须把字典序写成第二关键字。\n\n"
        "⚠️ `k` 可能大于不同单词数，输出时要取 `min(k, size)`，别越界。"
    ),
    input_format="第一行 `k`；第二行起是文本（可能含多行，读到 EOF）。",
    output_format="最多 `k` 行，每行 `单词 次数`。",
    constraints_md="- 1 ≤ k ≤ 1000\n- 文本总长 ≤ 10⁵\n- 单词只由字母数字组成，比较时不区分大小写",
    inputs=[
        "3\nthe quick brown fox the lazy dog the end\n",
        "2\nApple apple APPLE banana\n",
        "5\none two three\n",
        "3\nb a c b a b\n",
        "2\nx1 x2 x1-x2 x1\n",
        "4\nA b C d a B c D\n",
    ],
    samples=3,
    oracle=_oracle_10a,
    solution=r'''#include <cstdio>
#include <string>
#include <map>
#include <vector>
#include <algorithm>
#include <cctype>
#include <iostream>
using namespace std;

int main() {
    int k;
    if (scanf("%d", &k) != 1) return 0;

    map<string, int> cnt;
    string w;
    char ch;
    bool inWord = false;
    string cur;
    while (cin.get(ch)) {
        if (isalnum((unsigned char)ch)) {
            cur.push_back((char)tolower((unsigned char)ch));
            inWord = true;
        } else if (inWord) {
            cnt[cur]++;
            cur.clear();
            inWord = false;
        }
    }
    if (inWord) cnt[cur]++;

    vector<pair<string, int>> v(cnt.begin(), cnt.end());
    sort(v.begin(), v.end(), [](const pair<string, int>& a, const pair<string, int>& b) {
        if (a.second != b.second) return a.second > b.second;   // 次数降序
        return a.first < b.first;                               // 同频字典序升序
    });

    int lim = min<int>(k, (int)v.size());
    for (int i = 0; i < lim; i++)
        printf("%s %d\n", v[i].first.c_str(), v[i].second);
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <string>
#include <map>
#include <set>
#include <cctype>
#include <iostream>
using namespace std;

// 独立点：不用 vector + sort —— 把 (次数取负, 单词) 塞进 std::set，
// 靠 set 自身的红黑树排序直接按「次数降序、字典序升序」取出，天然不需要比较器。
int main() {
    int k;
    if (scanf("%d", &k) != 1) return 0;

    map<string, int> cnt;
    string cur;
    char ch;
    bool inWord = false;
    while (cin.get(ch)) {
        if (isalnum((unsigned char)ch)) {
            cur.push_back((char)tolower((unsigned char)ch));
            inWord = true;
        } else if (inWord) {
            cnt[cur]++;
            cur.clear();
            inWord = false;
        }
    }
    if (inWord) cnt[cur]++;

    set<pair<int, string>> ranked;
    for (auto& kv : cnt) ranked.insert({-kv.second, kv.first});

    int printed = 0;
    for (auto& p : ranked) {
        if (printed++ >= k) break;
        printf("%s %d\n", p.second.c_str(), -p.first);
    }
    return 0;
}
''',
)


def _oracle_10b(text: str) -> str:
    """去重排序：一个元素一个元素地往结果表里插，查重用线性扫描（真·笨办法）。"""
    d = text.split()
    n = int(d[0])
    a = [int(v) for v in d[1:1 + n]]
    keep: list[int] = []
    for x in a:
        dup = False
        for y in keep:            # O(n²) 线性查重
            if y == x:
                dup = True
                break
        if not dup:
            keep.append(x)
    keep.sort()                   # 最后整体排序
    return "read=%d\nunique=%d\n%s\n" % (n, len(keep), " ".join(map(str, keep)))


add(
    title="vector 排序去重（unique-erase）",
    section=SEC_10,
    difficulty=3, score=20,
    tags=["STL", "vector", "sort", "unique-erase"],
    statement_md=(
        "读入 `n` 个整数，输出去重并升序后的结果，同时报告读入个数与去重后的个数。\n\n"
        "```text\n"
        "read=7\n"
        "unique=4\n"
        "1 3 5 9\n"
        "```\n\n"
        "★ 为什么标准套路是「先 `sort` 再 `unique` 再 `erase`」：\n"
        "`std::unique` 只删除**相邻**的重复元素，它不会把整个容器扫一遍去重。"
        "所以必须先排序把相等的元素赶到一起，否则 `1 2 1` 里的两个 1 根本不相邻，"
        "`unique` 一个都不会删。\n\n"
        "★ `unique` 的返回值是「新的逻辑末尾」迭代器，它**不改变容器大小** —— "
        "后面那些元素还在，只是内容不确定。所以第三刀 `erase(newEnd, end())` 才是必须的。"
        "漏掉 `erase` 时 `v.size()` 还是原来的 `n`，这是最经典的错。\n\n"
        "★ 另一种写法是 `set<int>`：插入自动去重又天然有序，代价是每个元素一次 O(log n) "
        "的树插入、常数更大。`vector` 的 `sort`+`unique` 是 O(n log n) 但常数小得多，"
        "且内存连续 —— 这就是为什么大数据量下更推荐后者。\n\n"
        "⚠️ `n = 1` 时 `unique` 返回 `begin()+1`，`erase` 空区间也完全合法；别为它单开分支。"
    ),
    input_format="第一行 `n`；第二行 `n` 个整数。",
    output_format="三行：`read=<n>`、`unique=<k>`、去重升序后的序列（空格分隔）。",
    constraints_md="- 1 ≤ n ≤ 10⁵\n- |aᵢ| ≤ 10⁹",
    inputs=[
        "7\n3 1 2 3 1 5 2\n",
        "1\n42\n",
        "5\n-1 -1 0 0 1\n",
        "4\n9 9 9 9\n",
        "6\n1000000000 -1000000000 0 0 -1 1\n",
        "8\n5 4 3 2 1 2 3 4\n",
    ],
    samples=3,
    oracle=_oracle_10b,
    solution=r'''#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;

    vector<int> v(n);
    for (int i = 0; i < n; i++) scanf("%d", &v[i]);

    sort(v.begin(), v.end());                       // 第一刀：让相等元素相邻
    auto tail = unique(v.begin(), v.end());         // 第二刀：相邻去重，返回新末尾
    v.erase(tail, v.end());                         // 第三刀：真正删掉尾巴

    printf("read=%d\n", n);
    printf("unique=%d\n", (int)v.size());
    for (size_t i = 0; i < v.size(); i++) {
        if (i) putchar(' ');
        printf("%d", v[i]);
    }
    putchar('\n');
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <set>
using namespace std;

// 独立点：完全不碰 vector/unique —— 直接往 std::set 里塞，
// 红黑树自动去重 + 自动升序，最后顺序遍历输出。
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    set<int> s;
    for (int i = 0; i < n; i++) {
        int x;
        scanf("%d", &x);
        s.insert(x);
    }

    printf("read=%d\n", n);
    printf("unique=%d\n", (int)s.size());
    bool first = true;
    for (int x : s) {
        if (!first) putchar(' ');
        printf("%d", x);
        first = false;
    }
    putchar('\n');
    return 0;
}
''',
)


# ===================================================================== #
#  第 11 讲 · 流类库与输入输出
# ===================================================================== #

def _oracle_11(text: str) -> str:
    """报表：用 f-string 的对齐/精度格式模拟 setw + fixed + setprecision。"""
    lines = text.split("\n")
    n = int(lines[0].split()[0])
    out = ["%-10s%6s%12s" % ("name", "qty", "amount")]
    tot_qty = 0
    tot_cents = 0
    for i in range(n):
        name, qty, price = lines[1 + i].split()
        q = int(qty)
        p = int(price)
        cents = q * p
        tot_qty += q
        tot_cents += cents
        out.append("%-10s%6d%12.2f" % (name, q, cents / 100.0))
    out.append("%-10s%6d%12.2f" % ("TOTAL", tot_qty, tot_cents / 100.0))
    return "\n".join(out) + "\n"


add(
    title="setw 与 fixed 的报表对齐",
    section=SEC_11,
    difficulty=3, score=20,
    tags=["C++流类库", "iomanip", "setw", "fixed"],
    statement_md=(
        "读入 `n` 条商品记录（名称、数量、单价），输出一张对齐的报表，"
        "最后加一行合计。格式要求：\n\n"
        "- 名称**左对齐**，宽度 10；\n"
        "- 数量**右对齐**，宽度 6；\n"
        "- 金额**右对齐**，宽度 12，`fixed` + 保留 **2 位小数**；\n"
        "- 单价以「分」为单位给出，金额 = 数量 × 单价 ÷ 100（元）。\n\n"
        "表头是 `name`、`qty`、`amount`，合计行的名称列写 `TOTAL`。\n\n"
        "★ `setw(n)` 只对**下一个输出项**生效，用完立即失效 —— 所以每一列都必须重新写一次 "
        "`setw`。这也是为什么报表代码里 `setw` 到处都是，看着啰嗦但一个都不能省。\n\n"
        "★ `fixed` 是**粘性**的：设过之后一直有效，`setprecision(n)` 的含义也从「有效数字」"
        "变成「小数位数」。所以 `fixed` 写在表头之前一次就够，`setprecision` 同理；"
        "但 `setw` 必须逐列写。\n\n"
        "★ 对齐也是粘性的（`left` / `right` 同样一直有效），所以金额列前面要记得把 "
        "`left` 切回 `right`，否则合计行会左对齐。\n\n"
        "⚠️ 宽度不够时 `setw` **不会截断**，而是整段照输出、把后面的列顶歪 —— "
        "本题保证名称长度 ≤ 8。"
    ),
    input_format="第一行 `n`；随后 `n` 行，每行 `名称 数量 单价(分)`。",
    output_format="表头 1 行 + 明细 `n` 行 + 合计 1 行；列宽与精度见题面。",
    constraints_md="- 1 ≤ n ≤ 1000\n- 名称长度 ≤ 8（仅 ASCII 字母）\n- 0 ≤ 数量 ≤ 10⁴，0 ≤ 单价(分) ≤ 10⁶",
    inputs=[
        "2\nApple 3 1250\nPear 10 99\n",
        "1\nPen 1 100\n",
        "3\nA 0 500\nBB 2 50\nCCC 100 1\n",
        "2\nWidget 7 12345\nGizmo 13 250\n",
        "3\nx 1 1\ny 1 2\nz 1 3\n",
        "2\nLongName 10000 1000000\nShort 1 0\n",
    ],
    samples=3,
    oracle=_oracle_11,
    solution=r'''#include <cstdio>
#include <string>
#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    cout << left << setw(10) << "name"
         << right << setw(6) << "qty"
         << setw(12) << "amount" << '\n';

    cout << fixed << setprecision(2);          // 粘性：设一次即可

    long long totQty = 0, totCents = 0;
    for (int i = 0; i < n; i++) {
        string name;
        long long qty, price;
        cin >> name >> qty >> price;
        long long cents = qty * price;
        totQty += qty;
        totCents += cents;

        cout << left << setw(10) << name            // setw 只管下一项
             << right << setw(6) << qty
             << setw(12) << (double)cents / 100.0 << '\n';
    }

    cout << left << setw(10) << "TOTAL"
         << right << setw(6) << totQty
         << setw(12) << (double)totCents / 100.0 << '\n';
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <string>
#include <cstring>
#include <iostream>
#include <sstream>
#include <iomanip>
using namespace std;

// 独立点：先把每行拼进 ostringstream（内存里的小文件），再统一输出；
// 宽度/精度照样用操纵符，但「怎么攒行」换成了字符串流。
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    ostringstream out;
    out << left << setw(10) << "name"
        << right << setw(6) << "qty"
        << setw(12) << "amount" << '\n';
    out << fixed << setprecision(2);

    long long totQty = 0, totCents = 0;
    for (int i = 0; i < n; i++) {
        string name;
        long long qty, price;
        cin >> name >> qty >> price;
        long long cents = qty * price;
        totQty += qty;
        totCents += cents;
        out << left << setw(10) << name
            << right << setw(6) << qty
            << setw(12) << (double)cents / 100.0 << '\n';
    }
    out << left << setw(10) << "TOTAL"
        << right << setw(6) << totQty
        << setw(12) << (double)totCents / 100.0 << '\n';

    cout << out.str();
    return 0;
}
''',
)


# ===================================================================== #
#  第 12 讲 · 异常处理
# ===================================================================== #

def _oracle_12(text: str) -> str:
    """异常题：用 Python 的 try/except 模拟（自定义异常 + 标准异常两条路）。"""
    d = text.split()
    bal = int(d[0])
    q = int(d[1])
    pos = 2
    out = []
    for _ in range(q):
        op = d[pos]; amt = int(d[pos + 1]); pos += 2
        if amt <= 0:
            out.append("%s %d BAD" % (op, amt))
            continue
        if op == "D":
            bal += amt
            out.append("D %d OK balance=%d" % (amt, bal))
        else:
            if amt > bal:
                out.append("W %d FAIL need=%d balance=%d" % (amt, amt - bal, bal))
            else:
                bal -= amt
                out.append("W %d OK balance=%d" % (amt, bal))
    out.append("final=%d" % bal)
    return "\n".join(out) + "\n"


add(
    title="自定义异常处理取款超额",
    section=SEC_12,
    difficulty=4, score=25,
    tags=["C++异常处理", "自定义异常", "栈展开", "异常安全"],
    statement_md=(
        "把账户的存取款**异常化**：\n\n"
        "- 金额 ≤ 0 → 抛 `BadAmount`（继承 `std::invalid_argument`）；\n"
        "- 取款超额 → 抛 `InsufficientFunds`（继承 `std::runtime_error`），"
        "对象里带走「还差多少钱」；\n"
        "- 正常存取就不抛，直接改余额。\n\n"
        "主循环里对**每条**指令包一层 `try`，按异常类型分别处理，输出：\n\n"
        "```text\n"
        "D 100 OK balance=200\n"
        "W 500 FAIL need=300 balance=200\n"
        "W -5 BAD\n"
        "final=200\n"
        "```\n\n"
        "★ 为什么用异常而不是返回 `bool`：`withdraw` 现在有**两种**失败原因"
        "（参数非法、余额不足），而调用方对它们的处理不一样。"
        "返回 `bool` 只能表达「成功/失败」，细节得靠出参或全局变量捎带；"
        "异常可以**带类型和数据一起飞**，`catch (const InsufficientFunds& e)` 里直接问 "
        "`e.deficit()`。\n\n"
        "★ `catch` 的顺序：派生类写在基类**前面**。这里 `BadAmount` 与 "
        "`InsufficientFunds` 是兄弟，谁先都行；但只要写了 `catch (const std::exception&)`，"
        "它就必须放最后 —— 否则前面那个会把所有异常截走。\n\n"
        "★ **异常安全**的最低要求：抛异常时对象状态不被污染。"
        "所以 `withdraw` 必须**先检查再扣款**，绝不能「先扣了再说」。\n\n"
        "⚠️ `throw` 抛出的是**副本**，`catch` 要用 `const 引用` 接：既避免再复制一次，"
        "也避免对象切片。"
    ),
    input_format="第一行余额 `b`；第二行 `q`；随后 `q` 行，每行 `D amt` 或 `W amt`。",
    output_format=("每条指令一行：`D amt OK balance=..`、`W amt OK balance=..`、"
                   "`W amt FAIL need=.. balance=..`、`<op> amt BAD`。最后一行 `final=<余额>`。"),
    constraints_md="- 0 ≤ b ≤ 10⁹\n- 1 ≤ q ≤ 10⁵\n- |amt| ≤ 10⁹",
    inputs=[
        "100\n4\nD 100\nW 50\nW 500\nW 0\n",
        "0\n3\nW 1\nD 10\nW 10\n",
        "5\n3\nD -1\nW 5\nD 0\n",
        "1000000000\n2\nW 1000000000\nD 1000000000\n",
        "50\n4\nW 49\nW 1\nW 1\nD 3\n",
        "7\n3\nD 3\nW 10\nW 10\n",
    ],
    samples=3,
    oracle=_oracle_12,
    solution=r'''#include <cstdio>
#include <stdexcept>
#include <string>
using namespace std;

class BadAmount : public std::invalid_argument {
public:
    explicit BadAmount(const char* msg) : std::invalid_argument(msg) {}
};

class InsufficientFunds : public std::runtime_error {
private:
    long long deficit_;
public:
    explicit InsufficientFunds(long long deficit)
        : std::runtime_error("insufficient funds"), deficit_(deficit) {}
    long long deficit() const { return deficit_; }
};

class Account {
private:
    long long balance_;
public:
    explicit Account(long long b = 0) : balance_(b) {}

    void deposit(long long amt) {
        if (amt <= 0) throw BadAmount("amount must be positive");
        balance_ += amt;                       // 检查通过才动状态
    }
    void withdraw(long long amt) {
        if (amt <= 0) throw BadAmount("amount must be positive");
        if (amt > balance_) throw InsufficientFunds(amt - balance_);  // 先检查再扣
        balance_ -= amt;
    }
    long long balance() const { return balance_; }
};

int main() {
    long long b;
    int q;
    if (scanf("%lld %d", &b, &q) != 2) return 0;

    Account acc(b);
    for (int i = 0; i < q; i++) {
        char op[4];
        long long amt;
        scanf("%s %lld", op, &amt);
        try {
            if (op[0] == 'D') {
                acc.deposit(amt);
                printf("D %lld OK balance=%lld\n", amt, acc.balance());
            } else {
                acc.withdraw(amt);
                printf("W %lld OK balance=%lld\n", amt, acc.balance());
            }
        } catch (const InsufficientFunds& e) {        // 派生类在前
            printf("W %lld FAIL need=%lld balance=%lld\n",
                   amt, e.deficit(), acc.balance());
        } catch (const std::invalid_argument&) {      // 标准异常
            printf("%c %lld BAD\n", op[0], amt);
        }
    }
    printf("final=%lld\n", acc.balance());
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <string>
#include <iostream>
#include <sstream>
#include <string>
#include <stdexcept>
using namespace std;

// 独立点：两个异常类与题面一致，但把「一条指令的完整处理（含 try/catch）」收进
// 独立的 handle() 函数，用 ostringstream 拼好整行再交回 main ——
// 参考解是在 main 里就地 try/catch 直接 printf。catch 顺序一样是派生类在前。
class BadAmount : public std::invalid_argument {
public:
    BadAmount() : std::invalid_argument("amount must be positive") {}
};

class InsufficientFunds : public std::runtime_error {
    long long deficit_;
public:
    explicit InsufficientFunds(long long d)
        : std::runtime_error("insufficient funds"), deficit_(d) {}
    long long deficit() const { return deficit_; }
};

class Account {
    long long balance_;
public:
    explicit Account(long long b) : balance_(b) {}
    void deposit(long long amt) {
        if (amt <= 0) throw BadAmount();
        balance_ += amt;
    }
    void withdraw(long long amt) {
        if (amt <= 0) throw BadAmount();
        if (amt > balance_) throw InsufficientFunds(amt - balance_);
        balance_ -= amt;
    }
    long long balance() const { return balance_; }
};

static string handle(Account& acc, char op, long long amt) {
    ostringstream os;
    try {
        if (op == 'D') {
            acc.deposit(amt);
            os << "D " << amt << " OK balance=" << acc.balance();
        } else {
            acc.withdraw(amt);
            os << "W " << amt << " OK balance=" << acc.balance();
        }
    } catch (const InsufficientFunds& e) {              // 派生类在前
        os << "W " << amt << " FAIL need=" << e.deficit()
           << " balance=" << acc.balance();
    } catch (const std::invalid_argument&) {            // 标准异常兜底
        os << op << ' ' << amt << " BAD";
    }
    return os.str();
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long b;
    int q;
    if (!(cin >> b >> q)) return 0;

    Account acc(b);
    for (int i = 0; i < q; i++) {
        string op;
        long long amt;
        cin >> op >> amt;
        cout << handle(acc, op[0], amt) << '\n';
    }
    cout << "final=" << acc.balance() << '\n';
    return 0;
}
''',
)


# --------------------------------------------------------------------- #
#  汇总
# --------------------------------------------------------------------- #

HEADER = '''# -*- coding: utf-8 -*-
"""C++ 基础（subject=cpp）编程题库 —— 自动生成，**不要手改本文件**。

生成器：tools/gen_cpp_prog.py
分节：第 02 ~ 12 讲，共 17 题

重生成：python tools/gen_cpp_prog.py
"""

CPP_PROG_PROBLEMS: list[dict] = '''

TAIL = "\n"


def build() -> list[dict]:
    out: list[dict] = []
    for p in PROBLEMS:
        n_sample = int(p.get("samples", 1))
        cases = []
        for i, inp in enumerate(p["inputs"]):
            exp = p["oracle"](inp)
            if not isinstance(exp, str):
                raise SystemExit("题目《%s》第 %d 个输入的 oracle 返回了 %s（应为 str）"
                                 % (p["title"], i + 1, type(exp).__name__))
            is_s = i < n_sample
            cases.append({
                "stdin": inp,
                "expected_stdout": exp,
                "is_sample": 1 if is_s else 0,
                "kind": "sample" if is_s else "manual",
                "explanation": "",
            })
        out.append({
            "title": p["title"],
            "subject": SUBJECT,
            "line": LINE,
            "difficulty": int(p.get("difficulty", 2)),
            "total_score": int(p.get("score", 10)),
            "tags": list(p.get("tags", [])),
            "statement_md": p["statement_md"],
            "input_format": p.get("input_format", ""),
            "output_format": p.get("output_format", ""),
            "constraints_md": p.get("constraints_md", ""),
            "time_limit_ms": int(p.get("time_limit_ms", 2000)),
            "memory_limit_mb": int(p.get("memory_limit_mb", 256)),
            "checker": "standard",
            "float_eps": 1e-6,
            "origin": "manual",
            "status": "published",
            "source_section": p["section"],
            "ref_interpreter": "gpp",
            "reference_solution": p["solution"],
            "alt_solution": p["alt"],
            "cases": cases,
        })
    return out


def _dump(probs: list[dict]) -> str:
    body = json.dumps(probs, ensure_ascii=False, indent=4)
    body = body.replace(": null", ": None").replace(": true", ": True").replace(": false", ": False")
    return HEADER + body + TAIL


def _sanity(probs: list[dict]) -> list[str]:
    problems: list[str] = []
    seen: set[str] = set()
    for i, p in enumerate(probs, 1):
        t = p["title"]
        if t in seen:
            problems.append("[%d] 标题重复：%s" % (i, t))
        seen.add(t)
        for k in ("statement_md", "input_format", "output_format", "constraints_md",
                  "reference_solution", "alt_solution", "source_section"):
            if not str(p.get(k) or "").strip():
                problems.append("[%d] %s 缺字段 %s" % (i, t, k))
        if p["subject"] != "cpp" or p["line"] != "cpp":
            problems.append("[%d] %s 的 subject/line 不是 cpp" % (i, t))
        if p["checker"] != "standard":
            problems.append("[%d] %s 的 checker 应为 standard" % (i, t))
        if not p["cases"]:
            problems.append("[%d] %s 没有测试用例" % (i, t))
        if not (5 <= len(p["cases"]) <= 8):
            problems.append("[%d] %s 测试点数 %d 不在 5~8" % (i, t, len(p["cases"])))
        if p["total_score"] <= 0:
            problems.append("[%d] %s 满分非法" % (i, t))
        for j, c in enumerate(p["cases"], 1):
            if not c["expected_stdout"]:
                problems.append("[%d] %s 第 %d 个用例期望输出为空" % (i, t, j))
            if not c["expected_stdout"].endswith("\n"):
                problems.append("[%d] %s 第 %d 个用例期望输出没以换行结尾" % (i, t, j))
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description="生成 C++ 基础编程题库")
    ap.add_argument("--check", action="store_true", help="只校验，不写文件")
    args = ap.parse_args()

    probs = build()
    total_cases = sum(len(p["cases"]) for p in probs)
    total_score = sum(p["total_score"] for p in probs)
    print("题目数：%d    测试点：%d    总分：%d"
          % (len(probs), total_cases, total_score))

    bad = _sanity(probs)
    if bad:
        print("★ 自检不通过：")
        for b in bad:
            print("   " + b)
        return 1
    print("自检通过 ✅")

    if args.check:
        return 0

    OUT_PATH.write_text(_dump(probs), encoding="utf-8", newline="\n")
    print("已写入 %s（%d 字节）" % (OUT_PATH, OUT_PATH.stat().st_size))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
