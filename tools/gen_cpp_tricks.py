# -*- coding: utf-8 -*-
"""「技巧特训 · C++」章节生成器 —— 20 题，难度 1→4 递进（每档 5 题）。

这一章考什么（与另外两条技巧章的边界）
------------------------------------
- `gen_py_tricks.py` → 技巧特训 · Python（30 题）：Python 内置容器与库的用法
- `gen_ds_tricks.py` → 技巧特训 · C/C++（39 题）：**算法实现**（背包、单调栈、二分答案、LIS…）
- 本文件 → 技巧特训 · C++（20 题）：**STL 惯用法与竞赛微套路**
  重点不在「算法怎么推」，而在「用哪个设施、写哪一行」——
  `count_if` 配 lambda、`lower_bound` 的区间长度、`rotate` 与三次 `reverse` 等价、
  `accumulate` 的初值类型、`stable_sort` 与比较器的严格弱序、
  `merge` / `priority_queue<greater>` / `stable_partition` / `set::insert` 的 bool 返回值、
  `emplace` 不覆盖、`nth_element` 线性求次序、`copy_if` + `back_inserter`、
  `tuple` 字典序、双指针夹逼、扫描线、`a+b<b+a` 比较器、`partial_sum`……

★ 标题一律写成「设施名 + 它解决的那个具体问题」，与 DS 线那 39 道标题零重合
  （`seed.ensure()` 按 title 判重且**静默跳过**，撞名不会报错，只会少题）。

每题固定字段
------------
title / section / difficulty / score / tags / statement_md
input_format / output_format / constraints_md
inputs   ← 手写测试点（可复现，不含随机）
samples  ← 前几个当样例（公开）
oracle   ← **独立 Python 实现**，算 expected_stdout
solution / alt ← 两套 C++ 实现（必须逐字节同输出）

★ oracle 绝不拿 C++ 参考解跑出来填 —— 那是自己给自己判卷。
★ `alt` 必须是**另一条实现路径**（换算法/换容器/换写法），不能只是改名。

重生成：python tools/gen_cpp_tricks.py
校验：  python tools/verify_bank.py --cpp
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "app" / "problems_bank_cpp_tricks.py"

SUBJECT = "cpp"
LINE = "cpp"
SEC = "技巧特训 · C++"

PROBLEMS: list[dict] = []


def add(**kw) -> None:
    PROBLEMS.append(kw)


# ===================================================================== #
#  难度 1 · 先把算法库这几个「一行流」写熟
# ===================================================================== #

def _oracle_01(text: str) -> str:
    """三个计数：奇数 / 3 的倍数 / 大于均值（纯 Python 手算，跟 STL 无关）。"""
    d = text.split()
    n = int(d[0])
    a = [int(x) for x in d[1:1 + n]]
    avg = sum(a) // n
    return "odd=%d\nmult3=%d\nabove=%d\n" % (
        sum(1 for x in a if x % 2 == 1),
        sum(1 for x in a if x % 3 == 0),
        sum(1 for x in a if x > avg),
    )


add(
    title="count_if 三问：奇数·三的倍数·大于均值",
    section=SEC,
    difficulty=1, score=10,
    tags=["技巧特训", "STL", "count_if", "lambda", "accumulate"],
    statement_md=(
        "给定 `n` 个**非负**整数，按三个口径各数一次：\n\n"
        "1. `odd=` 奇数个数\n"
        "2. `mult3=` 3 的倍数个数（**0 也算 3 的倍数**）\n"
        "3. `above=` **严格大于平均值**的个数；平均值 = 总和整除 `n`（向下取整）\n\n"
        "这一档要练的是「一个 `accumulate` + 三次 `count_if`」这组最常见的组合拳：\n\n"
        "```cpp\n"
        "long long total = accumulate(a.begin(), a.end(), 0LL);\n"
        "int avg = int(total / n);\n"
        "int odd = count_if(a.begin(), a.end(), [](int x) { return x % 2 == 1; });\n"
        "int m3  = count_if(a.begin(), a.end(), [](int x) { return x % 3 == 0; });\n"
        "int up  = count_if(a.begin(), a.end(), [avg](int x) { return x > avg; });\n"
        "```\n\n"
        "⚠️ 三个坑：\n"
        "1. **`accumulate` 的初值写 `0` 得到的是 `int` 累加**，`n` 大、值大时会溢出；写 `0LL` 才是 `long long`。\n"
        "2. `count_if` 的谓词**调用顺序不保证**，别在里面改外部变量。\n"
        "3. 平均值要**先累加再除**，别边加边除 —— 整数除法会一路丢精度。"
    ),
    input_format="第一行 `n`；第二行 `n` 个非负整数。",
    output_format="三行：`odd=<奇数个数>` / `mult3=<3 的倍数个数>` / `above=<大于均值的个数>`。",
    constraints_md="- 1 ≤ n ≤ 100000\n- 0 ≤ a[i] ≤ 10⁶\n- 总和最大 10¹¹，必须用 64 位累加",
    inputs=[
        "5\n1 2 3 4 5\n",
        "6\n0 3 6 9 12 15\n",
        "1\n7\n",
        "8\n1000000 999999 0 0 3 4 5 6\n",
        "4\n0 0 0 0\n",
        "10\n10 20 30 40 50 60 70 80 90 100\n",
    ],
    samples=2,
    oracle=_oracle_01,
    solution=r'''#include <cstdio>
#include <vector>
#include <numeric>
#include <algorithm>
using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<int> a(n);
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);

    long long total = accumulate(a.begin(), a.end(), 0LL);   // ★ 0LL 才有 64 位
    int avg = int(total / n);

    int odd = count_if(a.begin(), a.end(), [](int x) { return x % 2 == 1; });
    int m3  = count_if(a.begin(), a.end(), [](int x) { return x % 3 == 0; });
    int up  = count_if(a.begin(), a.end(), [avg](int x) { return x > avg; });

    printf("odd=%d\nmult3=%d\nabove=%d\n", odd, m3, up);
    return 0;
}
''',
    alt=r'''#include <cstdio>
using namespace std;

// 独立实现：完全不碰 <algorithm>/<numeric>，一个 for 扫一遍，
// 顺便验证「STL 那三个谓词」与手写判断的结果必须一模一样。
int a[100005];

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    long long total = 0;
    for (int i = 0; i < n; i++) {
        scanf("%d", &a[i]);
        total += a[i];
    }
    int avg = int(total / n);
    int odd = 0, m3 = 0, up = 0;
    for (int i = 0; i < n; i++) {
        if (a[i] % 2 == 1) odd++;
        if (a[i] % 3 == 0) m3++;
        if (a[i] > avg) up++;
    }
    printf("odd=%d\nmult3=%d\nabove=%d\n", odd, m3, up);
    return 0;
}
''',
)


def _oracle_02(text: str) -> str:
    """区间内元素个数：排序后直接数（不依赖任何二分）。"""
    d = text.split()
    n = int(d[0])
    a = [int(x) for x in d[1:1 + n]]
    pos = 1 + n
    q = int(d[pos])
    pos += 1
    s = sorted(a)
    out = []
    for _ in range(q):
        lo, hi = int(d[pos]), int(d[pos + 1])
        pos += 2
        out.append(str(sum(1 for x in s if lo <= x <= hi)))
    return "\n".join(out) + "\n"


add(
    title="lower_bound 与 upper_bound 的差就是区间个数",
    section=SEC,
    difficulty=1, score=10,
    tags=["技巧特训", "STL", "lower_bound", "upper_bound", "二分"],
    statement_md=(
        "给定 `n` 个整数（可负）和 `q` 次查询，每次查询给出闭区间 `[lo, hi]`，"
        "求**有多少个元素落在这个区间里**。\n\n"
        "排序一次 `O(n log n)`，之后每次查询 `O(log n)` —— 全部靠这一行：\n\n"
        "```cpp\n"
        "int L = lower_bound(v.begin(), v.end(), lo) - v.begin();  // 第一个 >= lo\n"
        "int R = upper_bound(v.begin(), v.end(), hi) - v.begin();  // 第一个 >  hi\n"
        "printf(\"%d\\n\", R - L);\n"
        "```\n\n"
        "★ 为什么是「差」：`lower_bound` 落在**区间左端**，`upper_bound` 落在**区间右端的后一个位置**，"
        "两者下标相减恰好是夹在中间的个数 —— 空区间时两者相等，差为 0，不需要特判。\n\n"
        "⚠️ 常见错法：`upper_bound(hi) - lower_bound(lo) + 1`（多加了个 1）；"
        "或者拿 `lower_bound` 当「存在性判断」用 `!= end()` —— 那只说明**有元素 ≥ 它**，不是等于它。"
    ),
    input_format="第一行 `n`；第二行 `n` 个整数；第三行 `q`；接下来 `q` 行每行 `lo hi`。",
    output_format="`q` 行，每行一个整数：落在 `[lo, hi]` 内的元素个数。",
    constraints_md="- 1 ≤ n, q ≤ 2000\n- |a[i]|, |lo|, |hi| ≤ 10⁹\n- lo ≤ hi（不必额外判断）",
    inputs=[
        "6\n1 3 3 5 7 9\n3\n1 3\n3 3\n4 8\n",
        "5\n-5 -1 0 2 10\n4\n-10 0\n0 0\n1 9\n-5 10\n",
        "1\n42\n3\n42 42\n41 41\n0 100\n",
        "7\n7 7 7 7 7 7 7\n2\n7 7\n8 9\n",
        "9\n-3 -2 -1 0 1 2 3 4 5\n5\n-1 1\n-3 5\n2 4\n-2 -2\n0 0\n",
        "4\n1000000000 -1000000000 0 500000000\n3\n-1000000000 0\n1 999999999\n-1000000000 1000000000\n",
    ],
    samples=2,
    oracle=_oracle_02,
    solution=r'''#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<int> v(n);
    for (int i = 0; i < n; i++) scanf("%d", &v[i]);
    sort(v.begin(), v.end());

    int q;
    if (scanf("%d", &q) != 1) return 0;
    while (q--) {
        int lo, hi;
        scanf("%d %d", &lo, &hi);
        int L = int(lower_bound(v.begin(), v.end(), lo) - v.begin());
        int R = int(upper_bound(v.begin(), v.end(), hi) - v.begin());
        printf("%d\n", R - L);
    }
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <vector>
using namespace std;

// 独立实现：手写两趟二分（lower / upper 的标准写法），不调用 <algorithm>。
// 边界写错（`<` 与 `<=`）是这里唯一的坑，两趟必须一个用一个不用。
int lb(const vector<int>& v, int x) {
    int l = 0, r = int(v.size());
    while (l < r) {
        int m = l + (r - l) / 2;
        if (v[m] < x) l = m + 1; else r = m;
    }
    return l;
}

int ub(const vector<int>& v, int x) {
    int l = 0, r = int(v.size());
    while (l < r) {
        int m = l + (r - l) / 2;
        if (v[m] <= x) l = m + 1; else r = m;
    }
    return l;
}

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<int> v(n);
    for (int i = 0; i < n; i++) scanf("%d", &v[i]);

    // 手写插入排序，彻底不用 std::sort
    for (int i = 1; i < n; i++) {
        int key = v[i], j = i - 1;
        while (j >= 0 && v[j] > key) { v[j + 1] = v[j]; j--; }
        v[j + 1] = key;
    }

    int q;
    if (scanf("%d", &q) != 1) return 0;
    while (q--) {
        int lo, hi;
        scanf("%d %d", &lo, &hi);
        printf("%d\n", ub(v, hi) - lb(v, lo));
    }
    return 0;
}
''',
)


def _oracle_03(text: str) -> str:
    """左旋 k 位：切片拼接（与 rotate / 三次 reverse 都无关）。"""
    d = text.split()
    n, k = int(d[0]), int(d[1])
    a = [int(x) for x in d[2:2 + n]]
    k %= n
    b = a[k:] + a[:k]
    return "after=" + " ".join(map(str, b)) + "\nfirst=%d\n" % b[0]


add(
    title="rotate 一次搞定左旋，等价于三次 reverse",
    section=SEC,
    difficulty=1, score=10,
    tags=["技巧特训", "STL", "rotate", "reverse", "迭代器区间"],
    statement_md=(
        "把长度为 `n` 的序列**左旋** `k` 位（前面的挪到后面），输出旋转后的整个序列和第一个元素。\n\n"
        "`std::rotate` 一行就够，且它是**原地**的：\n\n"
        "```cpp\n"
        "k %= n;                                        // ★ k 可能大于 n\n"
        "rotate(v.begin(), v.begin() + k, v.end());     // 中点是「新的开头」\n"
        "```\n\n"
        "★ `rotate(first, middle, last)` 的语义是「把 `[middle, last)` 转到前面」，"
        "所以左旋 `k` 位就是让 `middle = first + k`。\n\n"
        "同一个效果还有经典的三次 `reverse` 写法（竞赛里常用来手写，不用记 `rotate` 的参数顺序）：\n\n"
        "```cpp\n"
        "reverse(v.begin(), v.begin() + k);   // 前段反转\n"
        "reverse(v.begin() + k, v.end());     // 后段反转\n"
        "reverse(v.begin(), v.end());         // 整体反转\n"
        "```\n\n"
        "⚠️ 两个坑：\n"
        "1. **先 `k %= n`**。`k == n` 时 `middle == last`，`rotate` 合法但白跑；`k > n` 且不取模时 "
        "`v.begin() + k` 直接越界（UB，`-O2` 下可能不报错但结果乱）。\n"
        "2. 三次 reverse 的**顺序**别乱：先两段各反、再整体反。反过来（先整体）得到的不是左旋。"
    ),
    input_format="第一行 `n k`；第二行 `n` 个整数。",
    output_format="两行：`after=<旋转后序列，空格分隔>` / `first=<旋转后第一个元素>`。",
    constraints_md="- 1 ≤ n ≤ 100000\n- 0 ≤ k ≤ 10⁹",
    inputs=[
        "5 2\n10 20 30 40 50\n",
        "5 0\n1 2 3 4 5\n",
        "4 3\n9 8 7 6\n",
        "3 3\n1 2 3\n",
        "1 1000000000\n7\n",
        "6 4\n-1 -2 -3 -4 -5 -6\n",
    ],
    samples=2,
    oracle=_oracle_03,
    solution=r'''#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n, k;
    if (scanf("%d %d", &n, &k) != 2) return 0;
    vector<int> v(n);
    for (int i = 0; i < n; i++) scanf("%d", &v[i]);

    k %= n;                                          // ★ 不取模就可能越界
    rotate(v.begin(), v.begin() + k, v.end());

    printf("after=");
    for (int i = 0; i < n; i++) printf(i ? " %d" : "%d", v[i]);
    printf("\nfirst=%d\n", v[0]);
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;

// 独立实现：三次 reverse，不用 rotate。
int main() {
    int n, k;
    if (scanf("%d %d", &n, &k) != 2) return 0;
    vector<int> v(n);
    for (int i = 0; i < n; i++) scanf("%d", &v[i]);

    k %= n;
    reverse(v.begin(), v.begin() + k);   // 前段
    reverse(v.begin() + k, v.end());     // 后段
    reverse(v.begin(), v.end());         // 整体

    printf("after=");
    for (int i = 0; i < n; i++) printf(i ? " %d" : "%d", v[i]);
    printf("\nfirst=%d\n", v[0]);
    return 0;
}
''',
)


def _oracle_04(text: str) -> str:
    """大数和与均值：Python 天生大整数，直接算。"""
    d = text.split()
    n = int(d[0])
    a = [int(x) for x in d[1:1 + n]]
    s = sum(a)
    return "sum=%d\navg=%d\n" % (s, s // n)


add(
    title="accumulate 初值写 0LL，否则大数求和会溢出",
    section=SEC,
    difficulty=1, score=10,
    tags=["技巧特训", "STL", "accumulate", "溢出", "long long"],
    statement_md=(
        "给定 `n` 个非负整数（每个可达 10⁹），输出它们的总和与平均值（总和整除 `n`）。\n\n"
        "这题的正确写法只有一行，但**写错的人很多**：\n\n"
        "```cpp\n"
        "long long sum = accumulate(v.begin(), v.end(), 0LL);   // ✅\n"
        "int  bad      = accumulate(v.begin(), v.end(), 0);     // ❌ int 累加，溢出\n"
        "```\n\n"
        "★ 关键在于 `accumulate` 的**返回值类型由初值决定**：它会以初值的类型做累加，"
        "中间结果也是那个类型。初值写 `0` 就是 `int` 一路加过去 —— "
        "`n = 3`、每个元素都是 10⁹ 时总和 3×10⁹ 已经超出 `int` 上限（2147483647），"
        "结果变成负数或乱值，**且编译器不会有任何警告**。\n\n"
        "等价写法（同样正确，读起来更直白）：\n\n"
        "```cpp\n"
        "long long sum = 0;\n"
        "for (int x : v) sum += x;    // sum 是 long long，每次累加都在 64 位里做\n"
        "```\n\n"
        "⚠️ 另一个坑：`sum / n` 里 `n` 是 `int`，`long long / int` 结果仍是 `long long`，"
        "所以先算再窄化没问题；但如果你写 `int avg = sum / n` 而总和真的超过 2³¹，"
        "那**除完再窄化**也会截断 —— 本题保证平均值不超过 10⁹，所以这里安全。"
    ),
    input_format="第一行 `n`；第二行 `n` 个非负整数。",
    output_format="两行：`sum=<总和>` / `avg=<总和整除 n>`。",
    constraints_md="- 1 ≤ n ≤ 100000\n- 0 ≤ a[i] ≤ 10⁹\n- 总和可能到 10¹⁴，必须 64 位",
    inputs=[
        "4\n1000000000 1000000000 1000000000 1000000000\n",
        "3\n1 2 3\n",
        "1\n1000000000\n",
        "5\n2147483647 1 0 0 0\n",
        "2\n1000000000 999999999\n",
        "8\n1 1 1 1 1 1 1 1000000000\n",
    ],
    samples=2,
    oracle=_oracle_04,
    solution=r'''#include <cstdio>
#include <vector>
#include <numeric>
using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<int> v(n);
    for (int i = 0; i < n; i++) scanf("%d", &v[i]);

    long long sum = accumulate(v.begin(), v.end(), 0LL);   // ★ 初值决定累加类型
    printf("sum=%lld\navg=%lld\n", sum, sum / n);
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <vector>
using namespace std;

// 独立实现：range-for 手动累加，不用 accumulate —— 用来证明「初值类型」这件事
// 只要累加变量声明成 long long 就等价。
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<int> v(n);
    for (int i = 0; i < n; i++) scanf("%d", &v[i]);

    long long sum = 0;
    for (auto x : v) sum += x;
    printf("sum=%lld\navg=%lld\n", sum, sum / n);
    return 0;
}
''',
)


def _oracle_05(text: str) -> str:
    """逗号切分：Python 的 split(',') 与 C++ 的 find/substr 语义对齐。"""
    s = text.strip()
    vals = [int(p) for p in s.split(",") if p != ""]
    return "count=%d\nsum=%d\nmax=%d\nmin=%d\n" % (
        len(vals), sum(vals), max(vals), min(vals))


add(
    title="string::find 循环切分逗号串再 stoi",
    section=SEC,
    difficulty=1, score=12,
    tags=["技巧特训", "STL", "string", "find", "substr", "stoi"],
    statement_md=(
        "读入**一行**逗号分隔的整数（可能带负号），输出段数、总和、最大值、最小值。\n\n"
        "`std::string` 上「按单个字符切分」的标准套路是一个 `find` 循环：\n\n"
        "```cpp\n"
        "size_t p = 0;\n"
        "while (true) {\n"
        "    size_t q = s.find(',', p);          // 找下一个分隔符\n"
        "    if (q == string::npos) q = s.size(); // 没有了就一直到尾\n"
        "    v.push_back(stoi(s.substr(p, q - p)));\n"
        "    if (q == s.size()) break;           // ★ 先判断再前移，否则会多切一个空段\n"
        "    p = q + 1;\n"
        "}\n"
        "```\n\n"
        "★ `find` 返回的是 `size_t`，找不到时是 `string::npos`（一个极大值）。"
        "所以**不能**拿它当循环条件写成 `while (s.find(',', p) != npos)`，那样末段永远进不去。\n\n"
        "⚠️ 两个坑：\n"
        "1. **收尾顺序**。上例里 `if (q == s.size()) break;` 必须放在 `p = q + 1` 之前；"
        "顺序反了 `p` 会变成 `size()+1`，`substr` 抛 `out_of_range`。\n"
        "2. `stoi` 遇到不认识的字符会抛 `invalid_argument`，遇到超 `int` 范围抛 `out_of_range`，"
        "本题保证输入合法；但真实场景里它**不像 `atoi` 那样静默返回 0** —— 这既是好事也是坑。"
    ),
    input_format="一行：若干个整数，之间用**一个**逗号分隔（无空格、无空段）。",
    output_format="四行：`count=<段数>` / `sum=<总和>` / `max=<最大值>` / `min=<最小值>`。",
    constraints_md="- 1 ≤ 段数 ≤ 1000\n- |每个整数| ≤ 10⁹\n- 总和可能超 `int` 上限",
    inputs=[
        "-3,7,12,-5,0\n",
        "42\n",
        "1,1,1\n",
        "-1000000000,1000000000\n",
        "5,-5,5,-5,5,-5\n",
        "0,0,0,0,0,0,0,0\n",
    ],
    samples=2,
    oracle=_oracle_05,
    solution=r'''#include <cstdio>
#include <iostream>
#include <string>
#include <vector>
#include <climits>
using namespace std;

int main() {
    string s;
    if (!getline(cin, s)) return 0;

    vector<int> v;
    size_t p = 0;
    while (true) {
        size_t q = s.find(',', p);
        if (q == string::npos) q = s.size();
        v.push_back(stoi(s.substr(p, q - p)));
        if (q == s.size()) break;      // ★ 必须在 p = q + 1 之前
        p = q + 1;
    }

    long long sum = 0;
    int mx = INT_MIN, mn = INT_MAX;
    for (int x : v) { sum += x; if (x > mx) mx = x; if (x < mn) mn = x; }
    printf("count=%zu\nsum=%lld\nmax=%d\nmin=%d\n", v.size(), sum, mx, mn);
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <iostream>
#include <string>
#include <vector>
#include <climits>
using namespace std;

// 独立实现：不用 find/substr/stoi，逐字符手写解析（顺便处理负号）。
// 这是竞赛里读「一行非空格分隔」数据最稳的写法 —— 不依赖任何库函数的异常行为。
int main() {
    string s;
    if (!getline(cin, s)) return 0;

    vector<int> v;
    long long cur = 0;
    bool neg = false, has = false;
    for (size_t i = 0; i <= s.size(); i++) {
        char c = (i < s.size() ? s[i] : ',');
        if (c == ',') {
            if (has) v.push_back(int(neg ? -cur : cur));
            cur = 0; neg = false; has = false;
        } else if (c == '-') {
            neg = true;
        } else {
            cur = cur * 10 + (c - '0');
            has = true;
        }
    }

    long long sum = 0;
    int mx = INT_MIN, mn = INT_MAX;
    for (int x : v) { sum += x; if (x > mx) mx = x; if (x < mn) mn = x; }
    printf("count=%zu\nsum=%lld\nmax=%d\nmin=%d\n", v.size(), sum, mx, mn);
    return 0;
}
''',
)


# ===================================================================== #
#  难度 2 · 排序的三件事：稳定性、比较器、归并
# ===================================================================== #

def _oracle_06(text: str) -> str:
    """分数降序、同分按输入先后（用输入下标当第二关键字，天然稳定）。"""
    lines = [l for l in text.splitlines() if l.strip()]
    n = int(lines[0])
    recs = []
    for i in range(1, n + 1):
        parts = lines[i].split()
        recs.append((parts[0], int(parts[1]), i))
    recs.sort(key=lambda r: (-r[1], r[2]))
    body = "\n".join("%s %d" % (r[0], r[1]) for r in recs)
    return body + "\ntop=%s\n" % recs[0][0]


add(
    title="stable_sort 保住同分者的入场顺序",
    section=SEC,
    difficulty=2, score=15,
    tags=["技巧特训", "STL", "stable_sort", "排序稳定性"],
    statement_md=(
        "按分数**从高到低**排序，**同分的人保持输入的先后顺序**（不打乱）。"
        "输出排序后的名单（每行 `姓名 分数`），最后再输出 `top=<排在第一的姓名>`。\n\n"
        "这一档的核心就一句话：**要稳定就 `stable_sort`，别用 `sort` 再想办法补救**。\n\n"
        "```cpp\n"
        "stable_sort(v.begin(), v.end(), [](const Rec& a, const Rec& b) {\n"
        "    return a.score > b.score;      // ★ 只写 >，绝对不写 >=\n"
        "});\n"
        "```\n\n"
        "★ `sort` 的底层是内省排序（快排 + 堆排 + 插入），**不保证**等价元素的相对次序；"
        "`stable_sort` 通常是归并，等价元素保持原次序。两者复杂度都是 `O(n log n)`，"
        "`stable_sort` 只是要多一块临时空间 —— 需要稳定时没有理由不用它。\n\n"
        "⚠️ 三个坑：\n"
        "1. 比较器写 `a.score >= b.score` 会**破坏严格弱序**（等价元素返回了 true），"
        "`std::sort` 在 `-O2` 下可能直接越界崩掉 —— 这是最经典的「本地没事、评测 RE」。\n"
        "2. 想让 `sort` 也稳定，可以**把输入下标当第二关键字**参与比较，"
        "但那要多存一个字段，不如直接 `stable_sort`。\n"
        "3. 输出第一名的姓名要用**排序后的 `v[0]`**，别用「扫描时记住的最大值」——"
        "同分时两者可能不是同一个人。"
    ),
    input_format="第一行 `n`；接下来 `n` 行，每行 `姓名 分数`（姓名不含空格）。",
    output_format="`n` 行名单（`姓名 分数`），最后一行 `top=<第一名姓名>`。",
    constraints_md="- 1 ≤ n ≤ 100000\n- 0 ≤ 分数 ≤ 1000（**大量同分**，所以要考稳定性）\n- 姓名只含字母，长度 ≤ 20",
    inputs=[
        "5\namy 90\nbob 95\ncid 90\ndan 95\neve 80\n",
        "3\nzoe 100\nmax 100\nli 100\n",
        "1\nsolo 0\n",
        "6\na 60\nb 60\nc 70\nd 60\ne 70\nf 50\n",
        "4\np1 1\np2 2\np3 1\np4 2\n",
        "8\naa 50\nbb 40\ncc 50\ndd 40\nee 50\nff 40\ngg 50\nhh 40\n",
    ],
    samples=2,
    oracle=_oracle_06,
    solution=r'''#include <cstdio>
#include <string>
#include <vector>
#include <algorithm>
using namespace std;

struct Rec {
    string name;
    int score;
};

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<Rec> v(n);
    for (int i = 0; i < n; i++) {
        char buf[64];
        if (scanf("%63s %d", buf, &v[i].score) != 2) return 0;
        v[i].name = buf;
    }

    stable_sort(v.begin(), v.end(), [](const Rec& a, const Rec& b) {
        return a.score > b.score;          // ★ 严格大于，同分交给稳定性
    });

    for (const auto& r : v) printf("%s %d\n", r.name.c_str(), r.score);
    printf("top=%s\n", v[0].name.c_str());
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <string>
#include <vector>
using namespace std;

// 独立实现：手写插入排序（天然稳定：只有严格小于才后移）。
// 顺便证明「stable_sort 的结果 == 稳定排序的结果」，与 sort 的不确定次序不同。
struct Rec {
    string name;
    int score;
};

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<Rec> v(n);
    for (int i = 0; i < n; i++) {
        char buf[64];
        if (scanf("%63s %d", buf, &v[i].score) != 2) return 0;
        v[i].name = buf;
    }

    for (int i = 1; i < n; i++) {
        Rec key = v[i];
        int j = i - 1;
        while (j >= 0 && v[j].score < key.score) {   // 只挪严格更小的 → 稳定
            v[j + 1] = v[j];
            j--;
        }
        v[j + 1] = key;
    }

    for (const auto& r : v) printf("%s %d\n", r.name.c_str(), r.score);
    printf("top=%s\n", v[0].name.c_str());
    return 0;
}
''',
)


def _oracle_07(text: str) -> str:
    """|x| 降序、同绝对值按值升序：Python 排序键直接写出来，两段式不用技巧。"""
    d = text.split()
    n = int(d[0])
    a = [int(x) for x in d[1:1 + n]]
    b = sorted(a, key=lambda x: (-abs(x), x))
    return " ".join(map(str, b)) + "\n"


add(
    title="比较器必须是严格弱序：绝对值降序再按值升序",
    section=SEC,
    difficulty=2, score=15,
    tags=["技巧特训", "STL", "sort", "比较器", "严格弱序"],
    statement_md=(
        "给定 `n` 个整数（可负），按下面的规则排序并输出：\n\n"
        "1. **绝对值大的在前**；\n"
        "2. 绝对值相同时，**数值小的在前**（所以 `-5` 排在 `5` 前面，`3` 排在 `-3` 后面）。\n\n"
        "两段式比较器是最干净的写法：\n\n"
        "```cpp\n"
        "sort(v.begin(), v.end(), [](int a, int b) {\n"
        "    int x = abs(a), y = abs(b);\n"
        "    if (x != y) return x > y;     // 第一关键字：|x| 降序\n"
        "    return a < b;                 // 第二关键字：值升序\n"
        "});\n"
        "```\n\n"
        "★ 「严格弱序」的四条要求里，实践上只要记住一条："
        "**比较器对任意两个元素 `comp(a, a)` 必须返回 `false`，且不能出现 `>=` / `<=`**。"
        "写成 `if (x != y) return x > y; return a <= b;` 就违反了 —— 当 `a == b` 时它返回 `true`，"
        "排序算法会认为「a 必须排在 a 前面」，`-O2` 下的内省排序可能算出非法下标并越界。\n\n"
        "⚠️ 另一个常见错法：只写 `return abs(a) > abs(b);`（漏了第二关键字）。"
        "这时绝对值相同的元素次序**不确定**，而本题要求同绝对值按值升序，会稳定错样例。\n\n"
        "💡 想不写比较器也行：把键做成 pair，`pair` 自带字典序 —— "
        "`sort` 一个 `vector<pair<int,int>>` 存 `{-abs(x), x}`，升序排就是题目要的结果。"
    ),
    input_format="第一行 `n`；第二行 `n` 个整数（可负）。",
    output_format="一行：排序后的 `n` 个整数，空格分隔。",
    constraints_md="- 1 ≤ n ≤ 100000\n- |a[i]| ≤ 10⁶（不会碰到 `abs(INT_MIN)` 的 UB）",
    inputs=[
        "5\n3 -5 5 -3 0\n",
        "4\n1 -1 1 -1\n",
        "1\n0\n",
        "6\n-10 10 -9 9 0 0\n",
        "7\n2 -100 100 -2 50 -50 7\n",
        "5\n-1000000 1000000 -1 1 0\n",
    ],
    samples=2,
    oracle=_oracle_07,
    solution=r'''#include <cstdio>
#include <vector>
#include <algorithm>
#include <cstdlib>
using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<int> v(n);
    for (int i = 0; i < n; i++) scanf("%d", &v[i]);

    sort(v.begin(), v.end(), [](int a, int b) {
        int x = abs(a), y = abs(b);
        if (x != y) return x > y;    // 严格：只在不等时比
        return a < b;                // 严格：相等时返回 false
    });

    for (int i = 0; i < n; i++) printf(i ? " %d" : "%d", v[i]);
    printf("\n");
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <vector>
#include <algorithm>
#include <cstdlib>
using namespace std;

// 独立实现：两次 stable_sort 组合，完全不写「两段式 if」比较器。
//   ① 先按值升序（稳定）
//   ② 再按 |x| 降序（稳定）→ 同 |x| 的元素保住 ① 的值升序
// 这是「多关键字排序」的另一个标准套路：从次要关键字往主要关键字，一路稳定排序。
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<int> v(n);
    for (int i = 0; i < n; i++) scanf("%d", &v[i]);

    stable_sort(v.begin(), v.end());                              // 次要关键字
    stable_sort(v.begin(), v.end(), [](int a, int b) {            // 主要关键字
        return abs(a) > abs(b);
    });

    for (int i = 0; i < n; i++) printf(i ? " %d" : "%d", v[i]);
    printf("\n");
    return 0;
}
''',
)


def _oracle_08(text: str) -> str:
    """归并两段有序序列 = 整体排序（结果必然相同，所以直接用 sorted 当独立校验）。"""
    d = text.split()
    n, m = int(d[0]), int(d[1])
    a = [int(x) for x in d[2:2 + n]]
    b = [int(x) for x in d[2 + n:2 + n + m]]
    c = sorted(a + b)
    return "merged=" + " ".join(map(str, c)) + "\nfirst=%d\nlast=%d\n" % (c[0], c[-1])


add(
    title="merge 把两段有序序列一次并起来",
    section=SEC,
    difficulty=2, score=15,
    tags=["技巧特训", "STL", "merge", "back_inserter", "归并"],
    statement_md=(
        "给定两段**已经升序**的序列（长度 `n`、`m`），把它们合并成一段仍升序的序列。"
        "输出合并结果，以及合并后的首元素与末元素。\n\n"
        "标准答案是 `std::merge`，注意它**不返回值、写到第三个区间**，所以要配 `back_inserter`：\n\n"
        "```cpp\n"
        "vector<int> c;\n"
        "c.reserve(n + m);                       // ★ 不 reserve 也行，但会多次扩容\n"
        "merge(a.begin(), a.end(), b.begin(), b.end(), back_inserter(c));\n"
        "```\n\n"
        "★ 为什么不用 `sort(a+b)`：`merge` 是 `O(n+m)`，而重新排序是 `O((n+m)log(n+m))`。"
        "数据量大时差一倍以上 —— 「已经有序」这个前提本身就是资源，别浪费。\n\n"
        "⚠️ 三个坑：\n"
        "1. 忘记 `c.reserve()` 不会错，但会反复扩容；`back_inserter` 每次 `push_back`，"
        "配合 `reserve` 才是 `O(n+m)` 的常数。\n"
        "2. **输入必须真是有序的**。`merge` 不检查，乱序输入只会得到一段乱序结果，"
        "而且在 `-O2` 下不会有任何提示。\n"
        "3. `merge` 不会去重。要「并集且去重」得用 `set_union`（同样写两个区间 + 输出迭代器）。"
    ),
    input_format="第一行 `n m`；第二行 `n` 个升序整数；第三行 `m` 个升序整数。",
    output_format="三行：`merged=<合并后序列>` / `first=<首元素>` / `last=<末元素>`。",
    constraints_md="- 1 ≤ n, m ≤ 100000\n- 两段各自升序（不保证严格）\n- |元素| ≤ 10⁹",
    inputs=[
        "3 3\n1 4 7\n2 3 9\n",
        "1 1\n5\n1\n",
        "4 2\n-10 -5 0 5\n-7 6\n",
        "3 3\n1 1 1\n1 1 1\n",
        "5 1\n1 2 3 4 5\n3\n",
        "2 5\n100 200\n1 2 3 4 5\n",
    ],
    samples=2,
    oracle=_oracle_08,
    solution=r'''#include <cstdio>
#include <vector>
#include <algorithm>
#include <iterator>
using namespace std;

int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    vector<int> a(n), b(m);
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    for (int i = 0; i < m; i++) scanf("%d", &b[i]);

    vector<int> c;
    c.reserve(n + m);
    merge(a.begin(), a.end(), b.begin(), b.end(), back_inserter(c));

    printf("merged=");
    for (size_t i = 0; i < c.size(); i++) printf(i ? " %d" : "%d", c[i]);
    printf("\nfirst=%d\nlast=%d\n", c.front(), c.back());
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <vector>
using namespace std;

// 独立实现：双指针手工归并，不用 std::merge，也不用 back_inserter。
int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    vector<int> a(n), b(m);
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    for (int i = 0; i < m; i++) scanf("%d", &b[i]);

    vector<int> c;
    c.reserve(n + m);
    int i = 0, j = 0;
    while (i < n && j < m) {
        if (a[i] <= b[j]) c.push_back(a[i++]);
        else c.push_back(b[j++]);
    }
    while (i < n) c.push_back(a[i++]);
    while (j < m) c.push_back(b[j++]);

    printf("merged=");
    for (size_t k = 0; k < c.size(); k++) printf(k ? " %d" : "%d", c[k]);
    printf("\nfirst=%d\nlast=%d\n", c.front(), c.back());
    return 0;
}
''',
)


def _oracle_09(text: str) -> str:
    """合并果子总代价：堆模拟（Python heapq 是小顶堆，语义一致但实现独立）。"""
    import heapq

    d = text.split()
    n = int(d[0])
    a = [int(x) for x in d[1:1 + n]]
    heapq.heapify(a)
    cost = 0
    while len(a) > 1:
        x = heapq.heappop(a)
        y = heapq.heappop(a)
        cost += x + y
        heapq.heappush(a, x + y)
    return "cost=%d\n" % cost


add(
    title="priority_queue 设 greater 做小顶堆：合并果子",
    section=SEC,
    difficulty=2, score=15,
    tags=["技巧特训", "STL", "priority_queue", "greater", "堆", "贪心"],
    statement_md=(
        "有 `n` 堆果子，每堆 `a[i]` 个。每次可以把**任意两堆**合并成一堆，"
        "这次合并的代价是两堆果子数之和。重复直到只剩一堆，求**总代价最小**是多少。\n\n"
        "策略很简单：**每次合并当前最小的两堆**（这样大的数被少算几次）。"
        "要反复取最小，用小顶堆：\n\n"
        "```cpp\n"
        "priority_queue<long long, vector<long long>, greater<long long>> pq;\n"
        "```\n\n"
        "★ `priority_queue` 默认是**大顶堆**，`greater<T>` 把它翻成小顶堆。三个模板参数一个都不能少："
        "`<元素类型, 底层容器, 比较器>` —— 不能只写 `priority_queue<long long, greater<long long>>`。\n\n"
        "⚠️ 三个坑：\n"
        "1. **`greater<>` 在 C++11 之后才能不写类型**（`greater<long long>` 写成 `greater<>` 也行），"
        "老编译器上要写全。\n"
        "2. 用 `long long` 存：`n` 大、每堆大时总代价会超 `int`。\n"
        "3. `n == 1` 时**一次都不合并**，答案是 0（别把初始那堆算进代价）。\n\n"
        "💡 等价容器：`multiset<long long>` 取 `begin()` 也算小顶堆语义，"
        "但每轮要 `erase` 两次再 `insert`，常数比 `priority_queue` 大。"
    ),
    input_format="第一行 `n`；第二行 `n` 个正整数，表示每堆的果子数。",
    output_format="一行：`cost=<最小总代价>`。",
    constraints_md="- 1 ≤ n ≤ 100000\n- 1 ≤ a[i] ≤ 10⁴\n- 总代价可能到 10⁹ 以上，用 64 位",
    inputs=[
        "3\n1 2 9\n",
        "1\n5\n",
        "4\n1 1 1 1\n",
        "2\n10000 10000\n",
        "5\n10 20 30 40 50\n",
        "6\n1 2 3 4 5 6\n",
    ],
    samples=2,
    oracle=_oracle_09,
    solution=r'''#include <cstdio>
#include <queue>
#include <vector>
#include <functional>
using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;

    // ★ 小顶堆：<类型, 底层容器, 比较器> 三个参数都要写
    priority_queue<long long, vector<long long>, greater<long long>> pq;
    for (int i = 0; i < n; i++) {
        long long x;
        scanf("%lld", &x);
        pq.push(x);
    }

    long long cost = 0;
    while (pq.size() > 1) {
        long long x = pq.top(); pq.pop();
        long long y = pq.top(); pq.pop();
        cost += x + y;
        pq.push(x + y);
    }
    printf("cost=%lld\n", cost);
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <set>
using namespace std;

// 独立实现：multiset 当有序可重集，每轮取最小的两个（begin()），
// 不依赖 priority_queue 的模板参数写法。
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;

    multiset<long long> s;
    for (int i = 0; i < n; i++) {
        long long x;
        scanf("%lld", &x);
        s.insert(x);
    }

    long long cost = 0;
    while (s.size() > 1) {
        auto it = s.begin();
        long long x = *it;
        s.erase(it);
        it = s.begin();
        long long y = *it;
        s.erase(it);
        cost += x + y;
        s.insert(x + y);
    }
    printf("cost=%lld\n", cost);
    return 0;
}
''',
)


def _oracle_10(text: str) -> str:
    """偶数前移、各自保序：两个列表按原序收集再拼接。"""
    d = text.split()
    n = int(d[0])
    a = [int(x) for x in d[1:1 + n]]
    ev = [x for x in a if x % 2 == 0]
    od = [x for x in a if x % 2 != 0]
    return " ".join(map(str, ev + od)) + "\neven=%d\n" % len(ev)


add(
    title="stable_partition 偶数前移且不打乱相对序",
    section=SEC,
    difficulty=2, score=15,
    tags=["技巧特训", "STL", "stable_partition", "partition", "谓词"],
    statement_md=(
        "把序列里**所有偶数挪到前面、奇数留在后面**，并且**两部分各自保持原来的先后顺序**。"
        "输出重排后的序列，再输出偶数的个数。\n\n"
        "`stable_partition` 的返回值就是分界点，用它数个数最省事：\n\n"
        "```cpp\n"
        "auto mid = stable_partition(v.begin(), v.end(), [](int x) { return x % 2 == 0; });\n"
        "long long even = mid - v.begin();     // 满足谓词的元素个数\n"
        "```\n\n"
        "★ 为什么不能用 `partition`：`partition` 只保证「满足谓词的都在前面」，"
        "**不保证**内部次序 —— 它用交换实现，`O(n)` 但会打乱。"
        "`stable_partition` 通常要额外空间，复杂度 `O(n log n)`（空间不够时）或 `O(n)`（够时）。\n\n"
        "⚠️ 三个坑：\n"
        "1. 谓词返回 `true` 的元素**去前面**，别把条件写反（写成 `x % 2 != 0` 就成了奇数在前）。\n"
        "2. 负数的取模：`-3 % 2` 在 C++ 里是 `-1`（不是 0），所以「`!= 0` 即奇数」对负数同样成立；"
        "但如果写成 `x % 2 == 1` 就**漏掉所有负奇数** —— 这是本题最大的陷阱。\n"
        "3. 用返回值减 `begin()` 得到个数，比再跑一遍 `count_if` 更省，也更不容易写错。"
    ),
    input_format="第一行 `n`；第二行 `n` 个整数（可负）。",
    output_format="两行：重排后的序列（空格分隔）/ `even=<偶数个数>`。",
    constraints_md="- 1 ≤ n ≤ 100000\n- |a[i]| ≤ 10⁹\n- **含负奇数**，注意 `%` 的符号",
    inputs=[
        "6\n1 2 3 4 5 6\n",
        "5\n-3 -2 -1 0 1\n",
        "4\n1 3 5 7\n",
        "3\n2 4 6\n",
        "7\n0 -1 2 -3 4 -5 6\n",
        "5\n-7 -6 -5 -4 -3\n",
    ],
    samples=2,
    oracle=_oracle_10,
    solution=r'''#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<int> v(n);
    for (int i = 0; i < n; i++) scanf("%d", &v[i]);

    // ★ 谓词用 != 0，负数也判得对
    auto mid = stable_partition(v.begin(), v.end(), [](int x) { return x % 2 == 0; });
    long long even = mid - v.begin();

    for (int i = 0; i < n; i++) printf(i ? " %d" : "%d", v[i]);
    printf("\neven=%lld\n", even);
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <vector>
using namespace std;

// 独立实现：两个桶分别收集再拼回去，不用任何 partition。
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<int> ev, od;
    for (int i = 0; i < n; i++) {
        int x;
        scanf("%d", &x);
        if (x % 2 != 0) od.push_back(x);
        else ev.push_back(x);
    }

    vector<int> v;
    v.reserve(n);
    for (int x : ev) v.push_back(x);
    for (int x : od) v.push_back(x);

    for (int i = 0; i < n; i++) printf(i ? " %d" : "%d", v[i]);
    printf("\neven=%d\n", int(ev.size()));
    return 0;
}
''',
)


# ===================================================================== #
#  难度 3 · 容器语义：set 的返回值、map 的不覆盖、nth_element 的次序
# ===================================================================== #

def _oracle_11(text: str) -> str:
    """去重与计数：set 语义用 sorted(set(...)) 表达。"""
    d = text.split()
    n = int(d[0])
    a = [int(x) for x in d[1:1 + n]]
    s = sorted(set(a))
    second = str(s[1]) if len(s) >= 2 else "none"
    return "unique=%d\ndup=%d\nsecond=%s\n" % (len(s), n - len(s), second)


add(
    title="set::insert 的 bool 返回值直接数出重复",
    section=SEC,
    difficulty=3, score=20,
    tags=["技巧特训", "STL", "set", "insert", "去重"],
    statement_md=(
        "给定 `n` 个整数（可负），输出三行：\n\n"
        "- `unique=` 不同值的个数\n"
        "- `dup=` **多出来的重复次数**（总个数 − 不同值个数）\n"
        "- `second=` 第二小的不同值；不足两个不同值时输出 `none`\n\n"
        "`set::insert` 有一个很多人不知道的返回值：`pair<iterator, bool>`，"
        "`bool` 表示**这次插入是否真的插进去了**（元素已存在就是 `false`）。于是计数不用 `find` 再 `insert` 两趟：\n\n"
        "```cpp\n"
        "set<int> s;\n"
        "int dup = 0;\n"
        "for (int x : a) {\n"
        "    if (!s.insert(x).second) dup++;   // 插不进去 = 之前就有了\n"
        "}\n"
        "```\n\n"
        "C++17 之后还能直接解构：`auto [it, ok] = s.insert(x);`\n\n"
        "★ `set` 的迭代器是**中序**的，所以 `s.begin()` 是最小值，`next(s.begin())` 是第二小 —— "
        "不需要排序，本身就维护了有序性。\n\n"
        "⚠️ 三个坑：\n"
        "1. `s.insert(x).second` 的 `second` **不能省**，光看返回值是 `pair`，`if (s.insert(x))` 编不过。\n"
        "2. 取第二小之前必须判 `s.size() >= 2`；`next(s.begin())` 在只有 1 个元素时是 `end()`，"
        "解引用它是 UB（`-O2` 下读到垃圾值，不崩但答案错）。\n"
        "3. `set` 是 `O(log n)` 插入 + 每个元素一次内存分配，比「`sort` + `unique`」慢且更吃内存；"
        "只要能先收完再排序，`vector` 往往更快。"
    ),
    input_format="第一行 `n`；第二行 `n` 个整数（可负）。",
    output_format="三行：`unique=<不同值个数>` / `dup=<重复次数>` / `second=<第二小不同值或 none>`。",
    constraints_md="- 1 ≤ n ≤ 100000\n- |a[i]| ≤ 10⁹",
    inputs=[
        "6\n5 3 5 7 3 3\n",
        "4\n1 1 1 1\n",
        "1\n42\n",
        "5\n-10 -10 0 10 10\n",
        "3\n1000000000 999999999 1000000000\n",
        "7\n9 8 7 6 5 4 3\n",
    ],
    samples=2,
    oracle=_oracle_11,
    solution=r'''#include <cstdio>
#include <set>
#include <iterator>
using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;

    set<int> s;
    int dup = 0;
    for (int i = 0; i < n; i++) {
        int x;
        scanf("%d", &x);
        if (!s.insert(x).second) dup++;      // ★ 插不进去说明早有
    }

    if (s.size() >= 2) {
        auto it = s.begin();
        ++it;                                // 第二小
        printf("unique=%zu\ndup=%d\nsecond=%d\n", s.size(), dup, *it);
    } else {
        printf("unique=%zu\ndup=%d\nsecond=none\n", s.size(), dup);
    }
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;

// 独立实现：先 sort，再用 unique 的手工版（自己数不同值），完全不用 set。
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<int> a(n);
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    sort(a.begin(), a.end());

    int uniq = 0;
    for (int i = 0; i < n; i++) {
        if (i == 0 || a[i] != a[i - 1]) uniq++;
    }
    int dup = n - uniq;

    // 第二小的不同值：扫描到第二个「与前一个不等」的位置
    int seen = 0, second = 0;
    bool has_second = false;
    for (int i = 0; i < n; i++) {
        if (i == 0 || a[i] != a[i - 1]) {
            seen++;
            if (seen == 2) { second = a[i]; has_second = true; break; }
        }
    }

    printf("unique=%d\ndup=%d\n", uniq, dup);
    if (has_second) printf("second=%d\n", second);
    else printf("second=none\n");
    return 0;
}
''',
)


def _oracle_12(text: str) -> str:
    """首次成绩为准：字典里只存第一次见到的分数。"""
    lines = [l for l in text.splitlines() if l.strip()]
    n = int(lines[0])
    best: dict[str, int] = {}
    for i in range(1, n + 1):
        parts = lines[i].split()
        name, sc = parts[0], int(parts[1])
        if name not in best:
            best[name] = sc
    body = "\n".join("%s %d" % (k, best[k]) for k in sorted(best))
    return body + "\ncount=%d\n" % len(best)


add(
    title="map::emplace 不覆盖：同一人的成绩以首次为准",
    section=SEC,
    difficulty=3, score=20,
    tags=["技巧特训", "STL", "map", "emplace", "operator[]"],
    statement_md=(
        "输入 `n` 条成绩记录（同一个人可能出现多次），"
        "**每人只保留第一次出现的成绩**，最后按姓名字典序输出 `姓名 分数`，再输出人数。\n\n"
        "`emplace` 和 `operator[]` 的差别就在这一行：\n\n"
        "```cpp\n"
        "m.emplace(name, score);   // ✅ 已存在就什么都不做（保留首次）\n"
        "m[name] = score;          // ❌ 直接覆盖成最后一次\n"
        "m.insert({name, score});  // ✅ 同 emplace，但要多构造一次临时 pair\n"
        "```\n\n"
        "★ `map::emplace` 用的是「**构造即插入、失败即丢弃**」：键已存在时连值都不会构造（C++17 起保证），"
        "所以它同时是「不覆盖」和「少一次构造」两个优化。\n\n"
        "⚠️ 三个坑：\n"
        "1. **`operator[]` 会先默认构造再赋值**。对 `map<string,int>` 只是多写一个 0；"
        "对没有默认构造函数的 value 类型直接编译不过。而且它还有一个更隐蔽的副作用 —— "
        "**查询也会插入**：`if (m[\"nothere\"] == 0)` 会把键插进去。\n"
        "2. 想「保留最大」而不是「保留首次」，得 `m[name] = max(m[name], score)`，"
        "但这样 `operator[]` 的插入副作用就变成有用的了 —— 场景不同，选法不同。\n"
        "3. `map` 已按 key 有序，输出**不需要再排序**；`unordered_map` 就没有这个便利，必须自己排。"
    ),
    input_format="第一行 `n`；接下来 `n` 行，每行 `姓名 分数`。",
    output_format="若干行 `姓名 分数`（按姓名字典序），最后一行 `count=<人数>`。",
    constraints_md="- 1 ≤ n ≤ 100000\n- 姓名只含小写字母，长度 ≤ 10\n- 0 ≤ 分数 ≤ 1000",
    inputs=[
        "5\namy 90\nbob 80\namy 60\ncid 70\nbob 100\n",
        "1\nzoe 1\n",
        "4\na 1\na 2\na 3\na 4\n",
        "6\nb 2\na 1\nc 3\nb 20\nc 30\na 10\n",
        "3\nx 0\ny 1000\nx 1000\n",
        "5\nm 5\nk 4\nm 3\nk 2\nm 1\n",
    ],
    samples=2,
    oracle=_oracle_12,
    solution=r'''#include <cstdio>
#include <string>
#include <map>
using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;

    map<string, int> m;
    for (int i = 0; i < n; i++) {
        char buf[64];
        int sc;
        if (scanf("%63s %d", buf, &sc) != 2) return 0;
        m.emplace(buf, sc);          // ★ 已存在则丢弃，保留首次
    }

    for (const auto& kv : m) printf("%s %d\n", kv.first.c_str(), kv.second);
    printf("count=%zu\n", m.size());
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <string>
#include <vector>
#include <set>
#include <algorithm>
using namespace std;

// 独立实现：vector 记「首次出现的顺序」，set 只用来判重，最后整体排序输出。
// 完全不用 map，验证 emplace 的语义。
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;

    vector<pair<string, int>> recs;
    set<string> seen;
    for (int i = 0; i < n; i++) {
        char buf[64];
        int sc;
        if (scanf("%63s %d", buf, &sc) != 2) return 0;
        string name = buf;
        if (seen.insert(name).second) {        // 第一次见
            recs.push_back({name, sc});
        }
    }

    sort(recs.begin(), recs.end());            // pair 先比 first 再比 second，此处 first 唯一
    for (const auto& kv : recs) printf("%s %d\n", kv.first.c_str(), kv.second);
    printf("count=%zu\n", recs.size());
    return 0;
}
''',
)


def _oracle_13(text: str) -> str:
    """次序统计量：全排序后按下标取（与 nth_element 的「部分排序」完全独立）。"""
    d = text.split()
    n = int(d[0])
    a = sorted(int(x) for x in d[1:1 + n])
    if n % 2 == 1:
        med = a[n // 2]
    else:
        med = (a[n // 2 - 1] + a[n // 2]) // 2
    q1 = a[n // 4]
    q3 = a[min(3 * n // 4, n - 1)]
    return "median=%d\nq1=%d\nq3=%d\n" % (med, q1, q3)


add(
    title="nth_element 线性求中位数与四分位",
    section=SEC,
    difficulty=3, score=20,
    tags=["技巧特训", "STL", "nth_element", "次序统计量", "部分排序"],
    statement_md=(
        "给定 `n` 个**非负**整数，先把它们升序排好（想象一个排好的数组 `b`，下标从 0 开始），然后输出：\n\n"
        "- `median=` `n` 为奇数时取 `b[n/2]`；`n` 为偶数时取 `(b[n/2-1] + b[n/2]) / 2`（整除）\n"
        "- `q1=` `b[n/4]`\n"
        "- `q3=` `b[min(3n/4, n-1)]`\n\n"
        "全排序是 `O(n log n)`，但「**只求第 k 小**」其实 `O(n)` 就够 —— `nth_element`：\n\n"
        "```cpp\n"
        "vector<int> b = v;\n"
        "nth_element(b.begin(), b.begin() + n / 2, b.end());   // 让 b[n/2] 就位\n"
        "long long hi = b[n / 2];\n"
        "long long lo = *max_element(b.begin(), b.begin() + n / 2);  // 偶数 n 的下中位数\n"
        "```\n\n"
        "★ `nth_element(first, nth, last)` 只保证「`nth` 位置上的元素就是排序后该位置的值」，"
        "**左右两侧不保证有序**。所以取 `b[n/2]` 安全，取 `b[n/2-1]` 就不安全 —— "
        "但「前 `n/2` 个里最大的那个」一定等于 `b[n/2-1]`，于是用 `max_element` 补上。\n\n"
        "⚠️ 三个坑：\n"
        "1. 对同一个数组连续 `nth_element` 不同位置是安全的，但**别假设已经就位的位置还保持原值**"
        "（每次调用只承诺 `nth` 那一个）。稳妥做法：拷一份原始数组，或每次从副本重新来。\n"
        "2. `nth_element` 要求 `nth` 在 `[first, last)` 内；`n == 1` 时 `begin() + 0` 合法，不会崩。\n"
        "3. 偶数长度的「中位数」是两数平均，**先加后除**；本题输入非负，所以 C++ 的截断除法与数学向下取整一致。"
    ),
    input_format="第一行 `n`；第二行 `n` 个非负整数。",
    output_format="三行：`median=<中位数>` / `q1=<下四分位>` / `q3=<上四分位>`。",
    constraints_md="- 1 ≤ n ≤ 200000\n- 0 ≤ a[i] ≤ 10⁹",
    inputs=[
        "5\n3 1 4 1 5\n",
        "4\n1 2 3 4\n",
        "1\n7\n",
        "6\n10 20 30 40 50 60\n",
        "8\n0 0 0 0 100 100 100 100\n",
        "7\n9 8 7 6 5 4 3\n",
    ],
    samples=2,
    oracle=_oracle_13,
    solution=r'''#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<int> v(n);
    for (int i = 0; i < n; i++) scanf("%d", &v[i]);

    vector<int> b = v;                       // 拷一份，nth_element 会打乱
    nth_element(b.begin(), b.begin() + n / 2, b.end());
    long long hi = b[n / 2];
    long long med;
    if (n % 2 == 1) {
        med = hi;
    } else {
        long long lo = *max_element(b.begin(), b.begin() + n / 2);  // 下中位数
        med = (lo + hi) / 2;
    }

    // q1 / q3 各自从原始副本重新 nth，避免相互干扰
    vector<int> c = v;
    nth_element(c.begin(), c.begin() + n / 4, c.end());
    long long q1 = c[n / 4];

    vector<int> e = v;
    int i3 = min(3 * n / 4, n - 1);
    nth_element(e.begin(), e.begin() + i3, e.end());
    long long q3 = e[i3];

    printf("median=%lld\nq1=%lld\nq3=%lld\n", med, q1, q3);
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;

// 独立实现：老老实实全排序，直接按下标取 —— 用来验证 nth_element 那套「部分排序」的结果。
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<int> a(n);
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    sort(a.begin(), a.end());

    long long med;
    if (n % 2 == 1) med = a[n / 2];
    else med = ((long long)a[n / 2 - 1] + a[n / 2]) / 2;

    long long q1 = a[n / 4];
    long long q3 = a[min(3 * n / 4, n - 1)];
    printf("median=%lld\nq1=%lld\nq3=%lld\n", med, q1, q3);
    return 0;
}
''',
)


def _oracle_14(text: str) -> str:
    """子集抽取：条件取交集，保持原序。"""
    d = text.split()
    n = int(d[0])
    a = [int(x) for x in d[1:1 + n]]
    lo, hi = int(d[1 + n]), int(d[2 + n])
    kept = [x for x in a if lo <= x <= hi and x % 3 != 0]
    return "kept=%d\n%s\n" % (len(kept), " ".join(map(str, kept)))


add(
    title="copy_if 配 back_inserter 一次抽子集",
    section=SEC,
    difficulty=3, score=20,
    tags=["技巧特训", "STL", "copy_if", "back_inserter", "谓词"],
    statement_md=(
        "给定 `n` 个整数和区间 `[lo, hi]`，抽出**同时满足**下面两个条件的元素：\n\n"
        "1. `lo <= x <= hi`\n"
        "2. `x` **不是** 3 的倍数\n\n"
        "抽出来的元素**保持原来的先后顺序**，输出个数与它们本身。\n\n"
        "一行流写法（这是「按条件收集」的标准套路）：\n\n"
        "```cpp\n"
        "vector<int> kept;\n"
        "copy_if(v.begin(), v.end(), back_inserter(kept), [&](int x) {\n"
        "    return x >= lo && x <= hi && x % 3 != 0;\n"
        "});\n"
        "```\n\n"
        "★ 为什么必须 `back_inserter`：`copy_if` 的第三个参数是**输出迭代器**，"
        "直接传 `kept.begin()` 会在空 `vector` 上写越界（UB，`-O2` 下可能不崩）。"
        "`back_inserter` 包成「每写一个就 `push_back`」，容器自己长。\n\n"
        "⚠️ 三个坑：\n"
        "1. `copy_if` **不 reserve**，元素多时会多次扩容；知道上界就先 `kept.reserve(n)`。\n"
        "2. 谓词捕获 `lo/hi` 建议用 `[&]` 或 `[=]`；显式写 `[lo, hi]` 更清楚，"
        "但别捕获成引用后又改了它们 —— 谓词调用时机由实现决定。\n"
        "3. **负数取模**：`-6 % 3 == 0` ✓，所以「不是 3 的倍数」写 `x % 3 != 0` 对负数也对；"
        "写成 `x % 3 > 0` 就会把 `-6`（模为 0）之外的 `-4`（模为 -1）漏掉。\n\n"
        "💡 `remove_if` 是「原地删」，`copy_if` 是「抽到别处」。要保留原数组就用 `copy_if`。"
    ),
    input_format="第一行 `n`；第二行 `n` 个整数；第三行 `lo hi`。",
    output_format="两行：`kept=<个数>` / 保留的元素（空格分隔；没有则输出空行）。",
    constraints_md="- 1 ≤ n ≤ 100000\n- |a[i]|, |lo|, |hi| ≤ 10⁹\n- lo ≤ hi",
    inputs=[
        "6\n1 2 3 4 5 6\n2 5\n",
        "5\n-6 -4 -3 -1 0\n-10 10\n",
        "4\n1 2 4 5\n10 20\n",
        "3\n3 6 9\n0 100\n",
        "7\n0 3 6 9 12 15 18\n0 18\n",
        "5\n-9 -8 -7 -6 -5\n-9 -5\n",
    ],
    samples=2,
    oracle=_oracle_14,
    solution=r'''#include <cstdio>
#include <vector>
#include <algorithm>
#include <iterator>
using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<int> v(n);
    for (int i = 0; i < n; i++) scanf("%d", &v[i]);
    long long lo, hi;
    if (scanf("%lld %lld", &lo, &hi) != 2) return 0;

    vector<int> kept;
    kept.reserve(n);                      // 知道上界就先要空间
    copy_if(v.begin(), v.end(), back_inserter(kept), [lo, hi](int x) {
        return x >= lo && x <= hi && x % 3 != 0;
    });

    printf("kept=%zu\n", kept.size());
    for (size_t i = 0; i < kept.size(); i++) printf(i ? " %d" : "%d", kept[i]);
    printf("\n");
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <vector>
using namespace std;

// 独立实现：手写 for + push_back，不用 copy_if / back_inserter。
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<int> v(n);
    for (int i = 0; i < n; i++) scanf("%d", &v[i]);
    long long lo, hi;
    if (scanf("%lld %lld", &lo, &hi) != 2) return 0;

    vector<int> kept;
    for (int x : v) {
        if (x >= lo && x <= hi && x % 3 != 0) kept.push_back(x);
    }

    printf("kept=%zu\n", kept.size());
    for (size_t i = 0; i < kept.size(); i++) printf(i ? " %d" : "%d", kept[i]);
    printf("\n");
    return 0;
}
''',
)


def _oracle_15(text: str) -> str:
    """三段记录排序：科目升、分数降、学号升（负分数当第二键实现降序）。"""
    lines = [l for l in text.splitlines() if l.strip()]
    n = int(lines[0])
    recs = []
    for i in range(1, n + 1):
        sub, sc, sid = lines[i].split()
        recs.append((sub, int(sc), int(sid)))
    recs.sort(key=lambda r: (r[0], -r[1], r[2]))
    return "\n".join("%s %d %d" % r for r in recs) + "\n"


add(
    title="tuple 的字典序就是三段排序：科目·分数·学号",
    section=SEC,
    difficulty=3, score=20,
    tags=["技巧特训", "STL", "tuple", "结构化绑定", "字典序"],
    statement_md=(
        "输入 `n` 条记录 `科目 分数 学号`，按下面的优先级排序后逐行输出：\n\n"
        "1. **科目**字典序升\n"
        "2. 分数**降序**\n"
        "3. 学号**升序**\n\n"
        "`tuple` 自带的比较是**逐个元素字典序**，所以把「降序的字段取负」塞进去，排序就变成零成本：\n\n"
        "```cpp\n"
        "vector<tuple<string, int, int>> v;      // (科目, -分数, 学号)\n"
        "v.emplace_back(sub, -score, sid);\n"
        "sort(v.begin(), v.end());               // 直接排，不用写比较器\n"
        "for (const auto& [sub, neg, sid] : v)   // C++17 结构化绑定\n"
        "    printf(\"%s %d %d\\n\", sub.c_str(), -neg, sid);\n"
        "```\n\n"
        "★ 为什么用「取负」而不是写比较器：`tuple` 的 `operator<` 已经是「先比第 0 个，相等再比第 1 个……」，"
        "把要降序的整数字段取负，升序排出来就是降序。前提是**字段类型是整数**；"
        "字符串要降序就没法取负了，得改用 `greater<>` 包住或写自定义比较器。\n\n"
        "⚠️ 三个坑：\n"
        "1. **别混着用 `vector<pair>`**：pair 只有两个字段，第三个塞不进去。\n"
        "2. 结构化绑定是 C++17 的（本平台 `-std=c++17` 支持）；C++14 下要写 `get<0>(t)`。\n"
        "3. 输出时**记得把分数取回正号** —— 忘了就是全班负分。"
    ),
    input_format="第一行 `n`；接下来 `n` 行，每行 `科目 分数 学号`。",
    output_format="`n` 行，每行 `科目 分数 学号`（分数为正）。",
    constraints_md="- 1 ≤ n ≤ 100000\n- 科目只含小写字母，长度 ≤ 10\n- 0 ≤ 分数 ≤ 100\n- 1 ≤ 学号 ≤ 10⁹",
    inputs=[
        "4\nmath 90 2\nmath 90 1\nphysics 80 3\nmath 95 4\n",
        "1\nart 60 7\n",
        "5\nb 50 1\na 50 2\nb 70 3\na 70 4\nb 50 0\n",
        "3\nz 100 1\ny 0 2\nx 50 3\n",
        "6\ncs 90 10\ncs 90 9\ncs 85 8\nbio 85 7\nbio 85 6\nbio 95 5\n",
        "2\nsame 1 1000000000\nsame 1 1\n",
    ],
    samples=2,
    oracle=_oracle_15,
    solution=r'''#include <cstdio>
#include <string>
#include <vector>
#include <tuple>
#include <algorithm>
using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;

    vector<tuple<string, int, int>> v;      // (科目, -分数, 学号)
    v.reserve(n);
    for (int i = 0; i < n; i++) {
        char sub[64];
        int score, sid;
        if (scanf("%63s %d %d", sub, &score, &sid) != 3) return 0;
        v.emplace_back(string(sub), -score, sid);
    }

    sort(v.begin(), v.end());               // tuple 字典序，无需比较器

    for (const auto& [sub, neg, sid] : v) {
        printf("%s %d %d\n", sub.c_str(), -neg, sid);
    }
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <string>
#include <vector>
#include <algorithm>
using namespace std;

// 独立实现：struct + 手写三段比较器（不取负、不用 tuple 字典序）。
struct Rec {
    string sub;
    int score;
    long long sid;
};

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;

    vector<Rec> v(n);
    for (int i = 0; i < n; i++) {
        char sub[64];
        int score;
        long long sid;
        if (scanf("%63s %d %lld", sub, &score, &sid) != 3) return 0;
        v[i] = {string(sub), score, sid};
    }

    sort(v.begin(), v.end(), [](const Rec& a, const Rec& b) {
        if (a.sub != b.sub) return a.sub < b.sub;       // 科目升
        if (a.score != b.score) return a.score > b.score;  // 分数降
        return a.sid < b.sid;                           // 学号升
    });

    for (const auto& r : v) printf("%s %d %lld\n", r.sub.c_str(), r.score, r.sid);
    return 0;
}
''',
)


# ===================================================================== #
#  难度 4 · 竞赛风的组合套路
# ===================================================================== #

def _oracle_16(text: str) -> str:
    """三数之和为 0 的不同取值三元组个数：排序 + 双指针（Python 版，与 C++ 版独立）。"""
    d = text.split()
    n = int(d[0])
    a = sorted(int(x) for x in d[1:1 + n])
    cnt = 0
    for i in range(n - 2):
        if i > 0 and a[i] == a[i - 1]:
            continue
        lo, hi = i + 1, n - 1
        while lo < hi:
            s = a[i] + a[lo] + a[hi]
            if s == 0:
                cnt += 1
                v = a[lo]
                while lo < hi and a[lo] == v:
                    lo += 1
                v = a[hi]
                while lo < hi and a[hi] == v:
                    hi -= 1
            elif s < 0:
                lo += 1
            else:
                hi -= 1
    return "triples=%d\n" % cnt


add(
    title="排序后双指针夹逼：和为 0 的三元组",
    section=SEC,
    difficulty=4, score=25,
    tags=["技巧特训", "竞赛", "双指针", "去重", "三数之和"],
    statement_md=(
        "给定 `n` 个整数（可负、可重复），数出**有多少个不同的三元组**（按取值，不看下标）"
        "满足 `a + b + c = 0`。\n\n"
        "暴力三重循环是 `O(n³)`，`n = 3000` 直接超时。标准做法是**先排序，再固定一个数、双指针夹逼**：\n\n"
        "```cpp\n"
        "sort(a.begin(), a.end());\n"
        "for (int i = 0; i + 2 < n; i++) {\n"
        "    if (i && a[i] == a[i - 1]) continue;        // ① 第一层去重\n"
        "    int lo = i + 1, hi = n - 1;\n"
        "    while (lo < hi) {\n"
        "        long long s = (long long)a[i] + a[lo] + a[hi];\n"
        "        if (s == 0) {\n"
        "            cnt++;\n"
        "            int v = a[lo]; while (lo < hi && a[lo] == v) lo++;   // ② 第二层去重\n"
        "            v = a[hi];     while (lo < hi && a[hi] == v) hi--;\n"
        "        } else if (s < 0) lo++;\n"
        "        else hi--;\n"
        "    }\n"
        "}\n"
        "```\n\n"
        "★ 为什么能夹逼：数组有序后，`a[i]` 固定时 `a[lo] + a[hi]` 随 `lo` 增大单调增、随 `hi` 减小单调减，"
        "于是「和太小就抬 `lo`、太大就压 `hi`」每一步都在排除一整片不可能的解，总复杂度 `O(n²)`。\n\n"
        "⚠️ 四个坑：\n"
        "1. **两层去重缺一不可**。漏了 ①，同一组值会被不同 `i` 重复数；漏了 ②，同一组值在 `lo/hi` 上重复数。\n"
        "2. `a[i] + a[lo] + a[hi]` 用 `int` 累加会溢出（三个 10⁵ 没问题，但换到 10⁹ 级就炸）；"
        "**先转 `long long` 再相加**是习惯动作。\n"
        "3. 去重时 `lo`/`hi` 的移动必须**自己带边界检查**（`lo < hi`），否则可能越界。\n"
        "4. 三元组要求三个**不同下标**，所以内层从 `i + 1` 起步；若从 0 起步，`[0,0,0]` 这种会被数出来。"
    ),
    input_format="第一行 `n`；第二行 `n` 个整数（可负）。",
    output_format="一行：`triples=<不同取值三元组的个数>`。",
    constraints_md="- 1 ≤ n ≤ 3000\n- |a[i]| ≤ 10⁵\n- 要求 O(n²)；O(n³) 会超时",
    inputs=[
        "6\n-1 0 1 2 -1 -4\n",
        "3\n0 0 0\n",
        "4\n1 2 3 4\n",
        "5\n0 0 0 0 0\n",
        "7\n-2 -1 0 1 2 3 -3\n",
        "8\n-4 -2 -2 0 2 2 4 4\n",
    ],
    samples=2,
    oracle=_oracle_16,
    solution=r'''#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<int> a(n);
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    sort(a.begin(), a.end());

    long long cnt = 0;
    for (int i = 0; i + 2 < n; i++) {
        if (i > 0 && a[i] == a[i - 1]) continue;          // ① 第一层去重
        int lo = i + 1, hi = n - 1;
        while (lo < hi) {
            long long s = (long long)a[i] + a[lo] + a[hi]; // ★ 先转 64 位
            if (s == 0) {
                cnt++;
                int v = a[lo];
                while (lo < hi && a[lo] == v) lo++;        // ② 第二层去重
                v = a[hi];
                while (lo < hi && a[hi] == v) hi--;
            } else if (s < 0) {
                lo++;
            } else {
                hi--;
            }
        }
    }
    printf("triples=%lld\n", cnt);
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <vector>
#include <set>
#include <unordered_set>
#include <algorithm>
using namespace std;

// 独立实现：不用双指针。固定 i 与 j，用哈希表查第三个数是否存在，
// 命中的三元组丢进 set<vector<int>> 去重。O(n²) 但常数更大、思路完全不同。
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<int> a(n);
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    sort(a.begin(), a.end());

    set<vector<int>> found;
    for (int i = 0; i + 2 < n; i++) {
        if (i > 0 && a[i] == a[i - 1]) continue;
        unordered_set<int> seen;                 // j 之前出现过的值
        for (int j = i + 1; j < n; j++) {
            long long need = -(long long)a[i] - a[j];
            if (need >= -2147483648LL && need <= 2147483647LL &&
                seen.count((int)need)) {
                vector<int> t = {a[i], (int)need, a[j]};
                sort(t.begin(), t.end());
                found.insert(t);
            }
            seen.insert(a[j]);
        }
    }
    printf("triples=%zu\n", found.size());
    return 0;
}
''',
)


def _oracle_17(text: str) -> str:
    """区间并集总长度：排序后线性合并。"""
    d = text.split()
    n = int(d[0])
    segs = []
    for i in range(n):
        segs.append((int(d[1 + 2 * i]), int(d[2 + 2 * i])))
    segs.sort()
    total = 0
    cl = cr = None
    for l, r in segs:
        if cl is None:
            cl, cr = l, r
        elif l <= cr:
            cr = max(cr, r)
        else:
            total += cr - cl
            cl, cr = l, r
    if cl is not None:
        total += cr - cl
    return "covered=%d\n" % total


add(
    title="扫描线求区间并集总长度",
    section=SEC,
    difficulty=4, score=25,
    tags=["技巧特训", "竞赛", "扫描线", "区间合并", "差分"],
    statement_md=(
        "给定 `n` 个闭区间 `[l, r]`，求它们**并集的总长度**。"
        "长度按 `r - l` 计算（线段长度，不是整数点个数）。端点相接（`[1,3]` 与 `[3,5]`）视为连通，总长 `4`。\n\n"
        "标准扫描：按左端点排序，维护「当前合并段的左右端」：\n\n"
        "```cpp\n"
        "sort(segs.begin(), segs.end());\n"
        "long long cl = segs[0].first, cr = segs[0].second, total = 0;\n"
        "for (size_t i = 1; i < segs.size(); i++) {\n"
        "    if (segs[i].first <= cr) cr = max(cr, segs[i].second);   // ★ 相交或相接 → 合并\n"
        "    else { total += cr - cl; cl = segs[i].first; cr = segs[i].second; }\n"
        "}\n"
        "total += cr - cl;      // 最后一段别忘了收尾\n"
        "```\n\n"
        "★ 另一种完全等价的思路是**差分/事件点**：每个区间记两个事件 `(l, +1)`、`(r, -1)`，"
        "按坐标排序后扫一遍，只要「当前覆盖数 > 0」就把相邻两个坐标之间的距离累加。"
        "这招能直接推广到「求被覆盖至少 k 层的长度」，比合并段更通用。\n\n"
        "⚠️ 四个坑：\n"
        "1. **`<=` 还是 `<`**：题面说端点相接算连通，所以合并条件是 `l <= cr`。写成 `<` 会把相邻区间断开，"
        "总长不变但段数算多（本题只问总长，所以 `<=` 与 `<` 结果其实相同 —— 但换成「求段数」就会错）。\n"
        "2. **收尾**：循环结束后最后一段的 `cr - cl` 要单独加，漏了就是「少算一段」。\n"
        "3. 坐标可负、可达 10⁹，长度用 `long long`。\n"
        "4. 包在别的区间里的小区间（`[2,3]` 落在 `[1,10]` 内）不能让 `cr` 变小 —— 必须 `cr = max(cr, r)`。"
    ),
    input_format="第一行 `n`；接下来 `n` 行，每行 `l r`（`l ≤ r`）。",
    output_format="一行：`covered=<并集总长度>`。",
    constraints_md="- 1 ≤ n ≤ 100000\n- |l|, |r| ≤ 10⁹，l ≤ r\n- 总长度可能到 10⁹ 以上",
    inputs=[
        "2\n1 3\n3 5\n",
        "3\n1 4\n2 6\n8 10\n",
        "1\n0 0\n",
        "3\n-5 -1\n-2 2\n10 20\n",
        "4\n5 6\n1 2\n6 7\n2 3\n",
        "3\n1 10\n2 3\n4 5\n",
    ],
    samples=2,
    oracle=_oracle_17,
    solution=r'''#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<pair<long long, long long>> segs(n);
    for (int i = 0; i < n; i++) scanf("%lld %lld", &segs[i].first, &segs[i].second);
    sort(segs.begin(), segs.end());

    long long cl = segs[0].first, cr = segs[0].second, total = 0;
    for (int i = 1; i < n; i++) {
        if (segs[i].first <= cr) {
            if (segs[i].second > cr) cr = segs[i].second;   // ★ 别让 cr 变小
        } else {
            total += cr - cl;
            cl = segs[i].first;
            cr = segs[i].second;
        }
    }
    total += cr - cl;                                       // 收尾
    printf("covered=%lld\n", total);
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;

// 独立实现：差分 / 事件点扫描，不做区间合并。
// 每个区间贡献 (l, +1) 与 (r, -1) 两个事件；同一坐标上的事件要先全部处理，
// 再决定「接下来这一段」是否被覆盖 —— 否则端点相接会算错。
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<pair<long long, int>> ev;
    ev.reserve(2 * n);
    for (int i = 0; i < n; i++) {
        long long l, r;
        scanf("%lld %lld", &l, &r);
        ev.push_back({l, 1});
        ev.push_back({r, -1});
    }
    sort(ev.begin(), ev.end());

    long long total = 0;
    int cover = 0;
    for (size_t i = 0; i < ev.size(); i++) {
        size_t j = i;
        long long x = ev[i].first;
        while (j < ev.size() && ev[j].first == x) {   // 同一坐标的事件一起消化
            cover += ev[j].second;
            j++;
        }
        if (j < ev.size() && cover > 0) {
            total += ev[j].first - x;                 // 被覆盖的一段
        }
        i = j - 1;
    }
    printf("covered=%lld\n", total);
    return 0;
}
''',
)


def _oracle_18(text: str) -> str:
    """拼成最小数：比较器 a+b < b+a（Python 用 cmp_to_key 表达同一规则）。"""
    from functools import cmp_to_key

    d = text.split()
    n = int(d[0])
    toks = d[1:1 + n]

    def cmp(x: str, y: str) -> int:
        if x + y < y + x:
            return -1
        if x + y > y + x:
            return 1
        return 0

    s = "".join(sorted(toks, key=cmp_to_key(cmp))).lstrip("0")
    return "%s\n" % (s if s else "0")


add(
    title="换一种比较器：把数拼成最小的数字（a+b<b+a）",
    section=SEC,
    difficulty=4, score=25,
    tags=["技巧特训", "竞赛", "比较器", "贪心", "字符串拼接"],
    statement_md=(
        "给定 `n` 个非负整数，把它们**全部用上**、按某种顺序拼成一个数字，要求结果**最小**。"
        "输出这个数字（去掉前导零；全是 0 时输出 `0`）。\n\n"
        "这题的难点是：**按字典序排是错的**。比如 `9` 与 `30`，字典序 `30 < 9`，"
        "拼出来 `309`；但 `930` 更大，所以正确答案是 `309` —— 这个例子字典序碰巧对了。"
        "换成 `3` 与 `30`：字典序 `3 < 30` 得到 `330`，而 `303` 更小。所以必须比「拼接后的结果」：\n\n"
        "```cpp\n"
        "sort(s.begin(), s.end(), [](const string& a, const string& b) {\n"
        "    return a + b < b + a;      // ★ 比较的是拼接结果，不是单个数\n"
        "});\n"
        "string res;\n"
        "for (auto& t : s) res += t;\n"
        "size_t p = res.find_first_not_of('0');\n"
        "res = (p == string::npos) ? \"0\" : res.substr(p);\n"
        "```\n\n"
        "★ 为什么这个比较器成立：`a+b < b+a` 定义了一个**全序**（可以证明它满足传递性），"
        "于是「按它排序后顺序拼接」就是最小解 —— 这是贪心的典型形态：\n"
        "把「整体最优」归结为「相邻两元素该谁在前」的局部判断。\n\n"
        "⚠️ 四个坑：\n"
        "1. **千万别按数值大小排**。`9` 和 `90`：数值 `9 < 90`，但该 `909`？不对，最小是 `909`… "
        "而 `9` 与 `91` 应该拼成 `991` 还是 `919`？`919` 更小 —— 数值序完全失效。\n"
        "2. 比较器里 `a + b` 每次都会**新建字符串**，`n` 大时开销明显；"
        "本项目 `n ≤ 1000` 无妨，`n = 10⁵` 时要改用「按重复次数补全」的技巧。\n"
        "3. 前导零必须处理：输入 `[0, 0]` 拼出来是 `00`，应输出 `0`。\n"
        "4. 用**字符串**存每个数，别转成 `int` —— `10⁹` 以上会溢出，且前导零信息也会丢。"
    ),
    input_format="第一行 `n`；第二行 `n` 个非负整数（无前导零）。",
    output_format="一行：拼成的最小数字字符串（无前导零；全零输出 `0`）。",
    constraints_md="- 1 ≤ n ≤ 1000\n- 0 ≤ 每个数 < 10⁹\n- 结果长度 ≤ 9000",
    inputs=[
        "3\n3 30 34\n",
        "2\n10 2\n",
        "2\n0 0\n",
        "4\n9 91 1 0\n",
        "3\n121 12 1\n",
        "5\n999999999 1 0 10 100\n",
    ],
    samples=2,
    oracle=_oracle_18,
    solution=r'''#include <cstdio>
#include <string>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<string> s(n);
    for (int i = 0; i < n; i++) {
        char buf[32];
        if (scanf("%31s", buf) != 1) return 0;
        s[i] = buf;
    }

    sort(s.begin(), s.end(), [](const string& a, const string& b) {
        return a + b < b + a;          // ★ 比拼接结果，不比单个数
    });

    string res;
    for (const auto& t : s) res += t;
    size_t p = res.find_first_not_of('0');
    if (p == string::npos) res = "0";
    else res = res.substr(p);
    printf("%s\n", res.c_str());
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <string>
#include <vector>
using namespace std;

// 独立实现：手写归并排序，同一个比较规则但完全不用 std::sort。
static bool less_concat(const string& a, const string& b) { return a + b < b + a; }

static void msort(vector<string>& v, vector<string>& tmp, int l, int r) {
    if (r - l <= 1) return;
    int m = l + (r - l) / 2;
    msort(v, tmp, l, m);
    msort(v, tmp, m, r);
    int i = l, j = m, k = l;
    while (i < m && j < r) {
        if (less_concat(v[j], v[i])) tmp[k++] = v[j++];
        else tmp[k++] = v[i++];              // 相等时取左边 → 稳定
    }
    while (i < m) tmp[k++] = v[i++];
    while (j < r) tmp[k++] = v[j++];
    for (int t = l; t < r; t++) v[t] = tmp[t];
}

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<string> s(n);
    for (int i = 0; i < n; i++) {
        char buf[32];
        if (scanf("%31s", buf) != 1) return 0;
        s[i] = buf;
    }

    vector<string> tmp(n);
    msort(s, tmp, 0, n);

    string res;
    for (const auto& t : s) res += t;
    size_t p = res.find_first_not_of('0');
    if (p == string::npos) res = "0";
    else res = res.substr(p);
    printf("%s\n", res.c_str());
    return 0;
}
''',
)


def _oracle_19(text: str) -> str:
    """前缀和：显式累加数组，查询时相减。"""
    d = text.split()
    n, q = int(d[0]), int(d[1])
    a = [int(x) for x in d[2:2 + n]]
    pre = [0]
    for x in a:
        pre.append(pre[-1] + x)
    out = []
    pos = 2 + n
    for _ in range(q):
        l, r = int(d[pos]), int(d[pos + 1])
        pos += 2
        out.append(str(pre[r] - pre[l - 1]))
    return "\n".join(out) + "\n"


add(
    title="partial_sum 建前缀和后每次查询 O(1)",
    section=SEC,
    difficulty=4, score=25,
    tags=["技巧特训", "STL", "partial_sum", "前缀和", "long long"],
    statement_md=(
        "给定 `n` 个整数（可负）和 `q` 次查询，每次查询 `[l, r]`（**1 起、闭区间**），"
        "输出该区间的元素之和。\n\n"
        "前缀和一遍 `O(n)`，之后每次查询 `O(1)`：`pre[r] - pre[l-1]`。"
        "建前缀和可以用 `partial_sum`（注意写到 `pre.begin() + 1`，让 `pre[0] = 0` 当哨兵）：\n\n"
        "```cpp\n"
        "vector<long long> pre(n + 1, 0);\n"
        "partial_sum(a.begin(), a.end(), pre.begin() + 1);   // pre[i] = a[0..i-1] 之和\n"
        "printf(\"%lld\\n\", pre[r] - pre[l - 1]);             // l 是 1 起的，正好\n"
        "```\n\n"
        "★ `pre` 多开一位并置 0，是为了让 `l == 1` 时 `pre[l-1] = pre[0] = 0` 自然成立 —— "
        "**不用特判左边界**。这是前缀和最基本的纪律：**只要下标是 1 起，前缀数组就开 `n+1`**。\n\n"
        "⚠️ 四个坑：\n"
        "1. **必须 `long long`**。`n = 2×10⁵`、每个 `10⁹` 时总和 2×10¹⁴，`int` 直接溢出。\n"
        "2. `partial_sum` 的第二区间**不检查长度**：写到 `pre.begin()` 会让 `pre[0]` 变成 `a[0]`，"
        "于是 `l = 1` 的查询全部错 —— 而且不会崩，是个纯逻辑错。\n"
        "3. 格式上的小习惯：C 的 `printf` 用 `\\n` 就够快；如果改用 C++ 的 `cout`，"
        "**别用 `endl`** —— 它会每次强制刷缓冲，`q = 2×10⁵` 时明显拖慢。\n"
        "4. 如果查询**不要求在线**，还能用差分/离线排序，但前缀和已经是最简。"
    ),
    input_format="第一行 `n q`；第二行 `n` 个整数；接下来 `q` 行每行 `l r`（1 ≤ l ≤ r ≤ n）。",
    output_format="`q` 行，每行一个整数：区间和。",
    constraints_md="- 1 ≤ n, q ≤ 200000\n- |a[i]| ≤ 10⁹\n- 总和可能到 2×10¹⁴，必须 64 位",
    inputs=[
        "5 3\n1 2 3 4 5\n1 5\n2 3\n5 5\n",
        "3 2\n-1 -2 -3\n1 3\n2 2\n",
        "1 1\n1000000000\n1 1\n",
        "4 3\n1000000000 1000000000 1000000000 1000000000\n1 4\n1 1\n2 3\n",
        "6 2\n0 0 0 0 0 0\n1 6\n3 4\n",
        "5 2\n-1000000000 1000000000 -5 5 0\n1 5\n2 4\n",
    ],
    samples=2,
    oracle=_oracle_19,
    solution=r'''#include <cstdio>
#include <vector>
#include <numeric>
using namespace std;

int main() {
    int n, q;
    if (scanf("%d %d", &n, &q) != 2) return 0;
    vector<long long> a(n);
    for (int i = 0; i < n; i++) scanf("%lld", &a[i]);

    vector<long long> pre(n + 1, 0);
    partial_sum(a.begin(), a.end(), pre.begin() + 1);   // ★ 从 +1 开始写

    while (q--) {
        int l, r;
        scanf("%d %d", &l, &r);
        printf("%lld\n", pre[r] - pre[l - 1]);
    }
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <vector>
using namespace std;

// 独立实现：手写累加建前缀，不用 partial_sum。
int main() {
    int n, q;
    if (scanf("%d %d", &n, &q) != 2) return 0;

    vector<long long> pre(n + 1, 0);
    for (int i = 1; i <= n; i++) {
        long long x;
        scanf("%lld", &x);
        pre[i] = pre[i - 1] + x;
    }

    while (q--) {
        int l, r;
        scanf("%d %d", &l, &r);
        printf("%lld\n", pre[r] - pre[l - 1]);
    }
    return 0;
}
''',
)


def _oracle_20(text: str) -> str:
    """最少迟到任务数：按截止期排序 + 大顶堆（Moore-Hodgson 贪心）。"""
    import heapq

    d = text.split()
    n = int(d[0])
    jobs = []
    for i in range(n):
        jobs.append((int(d[2 + 2 * i]), int(d[1 + 2 * i])))   # (截止期, 耗时)
    jobs.sort()
    heap = []
    total = 0
    late = 0
    for deadline, dur in jobs:
        total += dur
        heapq.heappush(heap, -dur)
        if total > deadline:
            total += heapq.heappop(heap)     # 弹出最大耗时（负数加回去 = 减）
            late += 1
    return "late=%d\n" % late


add(
    title="大顶堆做贪心：单机任务最少迟到几个",
    section=SEC,
    difficulty=4, score=25,
    tags=["技巧特训", "竞赛", "priority_queue", "贪心", "调度"],
    statement_md=(
        "有 `n` 个任务，每个任务有耗时 `t` 和截止期 `d`。单机从时刻 0 开始、中途不停，"
        "一个任务只要**完成时刻 > 它的截止期**就算迟到。求**最少有几个任务会迟到**。\n\n"
        "经典贪心（Moore-Hodgson）：**按截止期升序处理**，先把任务全部排进去；"
        "一旦累计耗时超过当前截止期，就**踢掉已排任务里耗时最大的那个**（记为迟到）：\n\n"
        "```cpp\n"
        "sort(jobs.begin(), jobs.end());            // 按截止期升序\n"
        "priority_queue<long long> pq;              // 默认就是大顶堆\n"
        "long long total = 0, late = 0;\n"
        "for (auto& j : jobs) {\n"
        "    total += j.second;                     // 先接进来\n"
        "    pq.push(j.second);\n"
        "    if (total > j.first) {                 // 超期了\n"
        "        total -= pq.top(); pq.pop();       // 踢掉最费时的\n"
        "        late++;\n"
        "    }\n"
        "}\n"
        "```\n\n"
        "★ 为什么踢「耗时最大」：把最大的那个任务拿掉，既能最大程度地把总时长压回截止期以内，"
        "又只损失 1 个任务 —— 换掉任何别的任务，时长降得都没它多。"
        "而「按截止期升序」保证每次判定用的都是当前最紧的那条线。\n\n"
        "⚠️ 四个坑：\n"
        "1. `priority_queue<long long>` **默认就是大顶堆**，这里要的正是最大值，"
        "所以千万别顺手加 `greater<>`（那是小顶堆，会踢掉最省时的，答案直接错）。\n"
        "2. 累计耗时用 `long long`：`n = 10⁵`、单个 `10⁹` 时总和到 10¹⁴。\n"
        "3. 注意「先加后判」的顺序。先判后加会漏掉「这一个任务自己就使它超期」的情形。\n"
        "4. 截止期可以重复、可以很大，不需要离散化 —— 排一次序 + 一次堆操作就够，总复杂度 `O(n log n)`。"
    ),
    input_format="第一行 `n`；接下来 `n` 行，每行 `耗时 截止期`。",
    output_format="一行：`late=<最少迟到任务数>`。",
    constraints_md="- 1 ≤ n ≤ 100000\n- 1 ≤ 耗时 ≤ 10⁹\n- 0 ≤ 截止期 ≤ 10¹⁴",
    inputs=[
        "3\n3 5\n2 3\n1 1\n",
        "1\n5 5\n",
        "2\n5 4\n5 4\n",
        "4\n2 2\n2 2\n2 2\n2 2\n",
        "5\n10 100\n1 1\n1 2\n1 3\n1 4\n",
        "3\n100 100\n100 100\n100 100\n",
    ],
    samples=2,
    oracle=_oracle_20,
    solution=r'''#include <cstdio>
#include <vector>
#include <queue>
#include <algorithm>
using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<pair<long long, long long>> jobs(n);   // (截止期, 耗时)
    for (int i = 0; i < n; i++) scanf("%lld %lld", &jobs[i].second, &jobs[i].first);
    sort(jobs.begin(), jobs.end());               // 按截止期升序

    priority_queue<long long> pq;                 // ★ 默认大顶堆，正好要最大
    long long total = 0, late = 0;
    for (const auto& j : jobs) {
        total += j.second;
        pq.push(j.second);
        if (total > j.first) {
            total -= pq.top();
            pq.pop();
            late++;
        }
    }
    printf("late=%lld\n", late);
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <vector>
#include <set>
#include <algorithm>
using namespace std;

// 独立实现：multiset 维护已排任务，踢人时取最后一个（最大）。
// 不用 priority_queue，也不用它的模板参数。
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<pair<long long, long long>> jobs(n);
    for (int i = 0; i < n; i++) scanf("%lld %lld", &jobs[i].second, &jobs[i].first);
    sort(jobs.begin(), jobs.end());

    multiset<long long> chosen;
    long long total = 0, late = 0;
    for (const auto& j : jobs) {
        total += j.second;
        chosen.insert(j.second);
        if (total > j.first) {
            auto it = prev(chosen.end());        // 最大的那个
            total -= *it;
            chosen.erase(it);
            late++;
        }
    }
    printf("late=%lld\n", late);
    return 0;
}
''',
)


HEADER = '''# -*- coding: utf-8 -*-
"""C++ 技巧特训题库（subject=cpp，分节「技巧特训 · C++」）—— 自动生成，**不要手改本文件**。

生成器：tools/gen_cpp_tricks.py
共 20 题：难度 1~4 各 5 题，STL 惯用法与竞赛微套路。

重生成：python tools/gen_cpp_tricks.py
校验：  python tools/verify_bank.py --cpp
"""

CPP_TRICKS_PROBLEMS: list[dict] = '''

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
            "question_type": "programming",
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
    prev_diff = 0
    for i, p in enumerate(probs, 1):
        t = p["title"]
        if t in seen:
            problems.append("[%d] 标题重复：%s" % (i, t))
        seen.add(t)
        for k in ("statement_md", "input_format", "output_format", "constraints_md",
                  "reference_solution", "alt_solution"):
            if not str(p.get(k) or "").strip():
                problems.append("[%d] %s 缺字段 %s" % (i, t, k))
        if p["subject"] != SUBJECT or p["line"] != LINE:
            problems.append("[%d] %s 的 subject/line 不是 cpp" % (i, t))
        if p["source_section"] != SEC:
            problems.append("[%d] %s 的分节不是「%s」" % (i, t, SEC))
        if p["question_type"] != "programming":
            problems.append("[%d] %s 的题型必须显式盖章为 programming" % (i, t))
        if p["checker"] != "standard":
            problems.append("[%d] %s 的 checker 应为 standard" % (i, t))
        if not p["cases"]:
            problems.append("[%d] %s 没有测试用例" % (i, t))
        if not (5 <= len(p["cases"]) <= 8):
            problems.append("[%d] %s 测试点数 %d 不在 5~8" % (i, t, len(p["cases"])))
        if not (1 <= p["difficulty"] <= 4):
            problems.append("[%d] %s 难度 %s 不在 1~4" % (i, t, p["difficulty"]))
        if p["difficulty"] < prev_diff:
            problems.append("[%d] %s 难度回退了（题目顺序必须按难度非递减）" % (i, t))
        prev_diff = p["difficulty"]
        if p["total_score"] <= 0:
            problems.append("[%d] %s 满分非法" % (i, t))
        for j, c in enumerate(p["cases"], 1):
            if not c["expected_stdout"]:
                problems.append("[%d] %s 第 %d 个用例期望输出为空" % (i, t, j))
            elif not c["expected_stdout"].endswith("\n"):
                problems.append("[%d] %s 第 %d 个用例期望输出没以换行结尾" % (i, t, j))
        if p["reference_solution"].strip() == p["alt_solution"].strip():
            problems.append("[%d] %s 的 alt 与参考解完全相同（不是独立实现）" % (i, t))
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description="生成 C++ 技巧特训题库")
    ap.add_argument("--check", action="store_true", help="只校验，不写文件")
    args = ap.parse_args()

    probs = build()
    total_cases = sum(len(p["cases"]) for p in probs)
    total_score = sum(p["total_score"] for p in probs)
    diff = {}
    for p in probs:
        diff[p["difficulty"]] = diff.get(p["difficulty"], 0) + 1
    print("题目数：%d    测试点：%d    总分：%d" % (len(probs), total_cases, total_score))
    print("难度分布：%s" % dict(sorted(diff.items())))

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
