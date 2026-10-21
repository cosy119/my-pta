# -*- coding: utf-8 -*-
"""C++ 基础编程题 · 第 8 册：动态规划（20）+ 综合模拟与数学（20）= 40 题。

对应教材第 04 讲「函数的递归调用」与第 06 讲「数组」的综合运用：把「递归 + 记忆化」
推广到「状态 + 转移」，再把一批纯模拟/数论题用 C++ 手工实现一遍。

★ 动态规划题的 oracle 一律是「小规模暴力」——枚举所有子集/所有切分/所有路径/BFS，
  绝不把 C++ 的转移方程抄一遍当答案。
★ 约束因此刻意压小：DP 题 n ≤ 20、模拟题量级 ≤ 10^4，保证暴力 oracle 秒出。

重生成：python tools/gen_cpp_basic8.py
"""
from __future__ import annotations

import math
import sys
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cpp_basic_kit import cases, cli, stmt          # noqa: E402

SEC_DP = "C++ 编程 · 动态规划"
SEC_SIM = "C++ 编程 · 综合模拟与数学"

PROBLEMS: list[dict] = []


def A(title, sec, d, st, inf, outf, con, inp, orc, sol, alt, tags):
    PROBLEMS.append(dict(title=title, section=sec, difficulty=d, statement_md=st,
                         input_format=inf, output_format=outf, constraints_md=con,
                         inputs=inp, oracle=orc, solution=sol, alt=alt, tags=tags))


def toks(t: str) -> list[int]:
    return [int(x) for x in t.split()]


def arr_of(t: str) -> list[int]:
    return toks(t)[1:]


def rows(t: str) -> list[list[str]]:
    return [ln.split() for ln in t.strip().splitlines() if ln.strip()]


def strs(t: str) -> list[str]:
    return [ln.strip() for ln in t.strip().splitlines() if ln.strip()]


# ===================================================================== #
#  SEC_DP · 动态规划（20 题）
# ===================================================================== #

def _knap01(t):
    """01 背包：枚举所有子集。"""
    r = rows(t)
    _, V = int(r[0][0]), int(r[0][1])
    it = [(int(a), int(b)) for a, b in r[1:]]
    best = 0
    for mask in range(1 << len(it)):
        w = sum(it[i][0] for i in range(len(it)) if mask >> i & 1)
        if w <= V:
            v = sum(it[i][1] for i in range(len(it)) if mask >> i & 1)
            best = max(best, v)
    return "%d\n" % best


def _knapfull(t):
    """完全背包：枚举每种物品的件数（笛卡尔积）。"""
    r = rows(t)
    n, V = int(r[0][0]), int(r[0][1])
    it = [(int(a), int(b)) for a, b in r[1:]]
    best = [0]

    def go(i, cap, val):
        if i == n:
            best[0] = max(best[0], val)
            return
        k = 0
        while k * it[i][0] <= cap:
            go(i + 1, cap - k * it[i][0], val + k * it[i][1])
            k += 1
    go(0, V, 0)
    return "%d\n" % best[0]


def _lis(t):
    a = arr_of(t)
    n = len(a)
    best = 0
    for mask in range(1 << n):
        sub = [a[i] for i in range(n) if mask >> i & 1]
        if len(sub) <= best:
            continue
        if all(sub[k] < sub[k + 1] for k in range(len(sub) - 1)):
            best = len(sub)
    return "%d\n" % best


def _lcs(t):
    a, b = strs(t)[:2]
    n = len(a)
    best = 0
    for mask in range(1 << n):
        sub = "".join(a[i] for i in range(n) if mask >> i & 1)
        if len(sub) <= best:
            continue
        it = iter(b)
        if all(ch in it for ch in sub):
            best = len(sub)
    return "%d\n" % best


def _triangle(t):
    r = [[int(x) for x in ln] for ln in rows(t)][1:]     # 首行是 n，不是三角形的一行
    n = len(r)
    best = [-10 ** 9]

    def go(i, j, s):
        s += r[i][j]
        if i == n - 1:
            best[0] = max(best[0], s)
            return
        go(i + 1, j, s)
        go(i + 1, j + 1, s)
    go(0, 0, 0)
    return "%d\n" % best[0]


def _maxseg(t):
    a = arr_of(t)
    n = len(a)
    return "%d\n" % max(sum(a[i:j + 1]) for i in range(n) for j in range(i, n))


def _climb(t):
    n = toks(t)[0]
    return "%d\n" % sum(math.comb(n - k, k) for k in range(n // 2 + 1))


def _rob(t):
    a = arr_of(t)
    n = len(a)
    best = 0
    for mask in range(1 << n):
        if any((mask >> i & 1) and (mask >> (i + 1) & 1) for i in range(n - 1)):
            continue
        best = max(best, sum(a[i] for i in range(n) if mask >> i & 1))
    return "%d\n" % best


def _edit(t):
    """编辑距离：在 (i, j) 状态图上做 0-1 BFS —— 字符相同是 0 权边，三种操作是 1 权边。"""
    v = strs(t)
    a = v[0]
    b = v[1] if len(v) > 1 else ""
    INF = 10 ** 9
    dist = {(0, 0): 0}
    dq = deque([(0, 0)])
    while dq:
        i, j = dq.popleft()
        d = dist[(i, j)]
        if i == len(a) and j == len(b):
            return "%d\n" % d
        moves = []
        if i < len(a) and j < len(b):
            if a[i] == b[j]:
                moves.append(((i + 1, j + 1), 0))       # 直接对齐，不花代价
            moves.append(((i + 1, j + 1), 1))           # 替换
        if i < len(a):
            moves.append(((i + 1, j), 1))               # 删除
        if j < len(b):
            moves.append(((i, j + 1), 1))               # 插入
        for s, w in moves:
            nd = d + w
            if dist.get(s, INF) > nd:
                dist[s] = nd
                if w:
                    dq.append(s)
                else:
                    dq.appendleft(s)
    return "%d\n" % dist.get((len(a), len(b)), 0)


def _stone(t):
    """石子合并：枚举所有相邻合并顺序。"""
    a = arr_of(t)
    best = [None]

    def go(st, cost):
        if len(st) == 1:
            if best[0] is None or cost < best[0]:
                best[0] = cost
            return
        for i in range(len(st) - 1):
            go(st[:i] + [st[i] + st[i + 1]] + st[i + 2:], cost + st[i] + st[i + 1])
    go(list(a), 0)
    return "%d\n" % best[0]


A("【DP】01 背包最大价值", SEC_DP, 2,
  stmt("有 `n` 件物品和一个容量为 `V` 的背包。第 `i` 件物品重 `w[i]`、价值 `v[i]`，"
       "每件**最多取一次**，求不超过容量能装下的最大总价值。",
       ["`f[j]` = 容量 `j` 时的最大价值；**容量必须倒着枚举** `j = V → w[i]`",
        "倒序是为了保证 `f[j-w[i]]` 还是「没放第 i 件」的旧值 —— 正序就变成完全背包了",
        "输出一个整数"]),
  "第一行 `n V`；之后 `n` 行，每行 `w v`。",
  "一行：最大总价值。",
  "- 1 ≤ n ≤ 10\n- 0 ≤ V ≤ 30\n- 1 ≤ w, v ≤ 50",
  lambda: cases("1 5\n3 10", "2 3\n1 5\n2 6", "3 5\n2 3\n3 4\n4 5",
                "4 10\n5 10\n4 40\n6 30\n3 50", "3 0\n1 100\n2 200\n3 300",
                "5 15\n1 2\n2 3\n3 5\n4 7\n5 11"),
  _knap01,
  r'''#include <cstdio>
int main() {
    int n, V;
    if (scanf("%d %d", &n, &V) != 2) return 0;
    int w[20], v[20];
    for (int i = 0; i < n; i++) scanf("%d %d", &w[i], &v[i]);
    long long f[205] = {0};
    for (int i = 0; i < n; i++)
        for (int j = V; j >= w[i]; j--)          // ★ 倒序：每件只用一次
            if (f[j - w[i]] + v[i] > f[j]) f[j] = f[j - w[i]] + v[i];
    printf("%lld\n", f[V]);
    return 0;
}
''',
  r'''#include <cstdio>
long long f[15][205];                            // f[i][j]：前 i 件、容量 j
int main() {
    int n, V, w[20], v[20];
    if (scanf("%d %d", &n, &V) != 2) return 0;
    for (int i = 0; i < n; i++) scanf("%d %d", &w[i], &v[i]);
    for (int i = 1; i <= n; i++)
        for (int j = 0; j <= V; j++) {
            f[i][j] = f[i - 1][j];
            if (j >= w[i - 1] && f[i - 1][j - w[i - 1]] + v[i - 1] > f[i][j])
                f[i][j] = f[i - 1][j - w[i - 1]] + v[i - 1];
        }
    printf("%lld\n", f[n][V]);
    return 0;
}
''',
  ["DP", "背包", "倒序枚举"])

A("【DP】完全背包最大价值", SEC_DP, 2,
  stmt("有 `n` 种物品和一个容量为 `V` 的背包。第 `i` 种物品重 `w[i]`、价值 `v[i]`，"
       "每种有**无限多件**，求不超过容量能装下的最大总价值。",
       ["和 01 背包只差一个字符：容量**正着枚举** `j = w[i] → V`",
        "正序时 `f[j-w[i]]` 已经是「本轮可能放过第 i 种」的新值，正好允许重复取",
        "输出一个整数"]),
  "第一行 `n V`；之后 `n` 行，每行 `w v`。",
  "一行：最大总价值。",
  "- 1 ≤ n ≤ 6\n- 0 ≤ V ≤ 20\n- 1 ≤ w, v ≤ 50",
  lambda: cases("1 10\n2 3", "2 5\n1 5\n2 12", "2 4\n2 3\n3 4",
                "3 7\n1 1\n3 4\n4 6", "1 0\n5 9", "4 12\n2 4\n3 6\n4 9\n5 12"),
  _knapfull,
  r'''#include <cstdio>
int main() {
    int n, V;
    if (scanf("%d %d", &n, &V) != 2) return 0;
    int w[20], v[20];
    for (int i = 0; i < n; i++) scanf("%d %d", &w[i], &v[i]);
    long long f[205] = {0};
    for (int i = 0; i < n; i++)
        for (int j = w[i]; j <= V; j++)          // ★ 正序：可反复取
            if (f[j - w[i]] + v[i] > f[j]) f[j] = f[j - w[i]] + v[i];
    printf("%lld\n", f[V]);
    return 0;
}
''',
  r'''#include <cstdio>
long long memo[10][205];
int n, V, w[20], v[20];
long long best(int i, int cap) {                 // 记忆化递归：自顶向下
    if (i == n) return 0;
    if (memo[i][cap] >= 0) return memo[i][cap];
    long long r = best(i + 1, cap);              // 这一种一件都不拿
    if (cap >= w[i]) {
        long long t = best(i, cap - w[i]) + v[i];  // 注意仍是第 i 种
        if (t > r) r = t;
    }
    return memo[i][cap] = r;
}
int main() {
    if (scanf("%d %d", &n, &V) != 2) return 0;
    for (int i = 0; i < n; i++) scanf("%d %d", &w[i], &v[i]);
    for (int i = 0; i <= n; i++)
        for (int j = 0; j <= V; j++) memo[i][j] = -1;
    printf("%lld\n", best(0, V));
    return 0;
}
''',
  ["DP", "完全背包", "正序枚举"])

A("【DP】最长上升子序列长度", SEC_DP, 2,
  stmt("给定 `n` 个整数，求**最长严格上升子序列**的长度（子序列不要求连续）。",
       ["`d[i]` = 以 `a[i]` 结尾的最长上升子序列长度：`d[i] = 1 + max{d[j] | j<i 且 a[j]<a[i]}`",
        "答案是 `max(d)`，不是 `d[n-1]` —— 这一点最容易写错",
        "输出一个整数"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：最长严格上升子序列长度。",
  "- 1 ≤ n ≤ 12\n- -100 ≤ a[i] ≤ 100",
  lambda: cases("5\n1 3 2 4 5", "4\n4 3 2 1", "5\n1 2 3 4 5",
                "6\n10 9 2 5 3 7", "3\n5 5 5", "8\n-3 0 -1 2 -2 4 1 6"),
  _lis,
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    int a[30], d[30], best = 0;
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    for (int i = 0; i < n; i++) {
        d[i] = 1;
        for (int j = 0; j < i; j++)
            if (a[j] < a[i] && d[j] + 1 > d[i]) d[i] = d[j] + 1;   // 严格上升
        if (d[i] > best) best = d[i];
    }
    printf("%d\n", best);
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int main() {                                     // 贪心 + 二分：O(n log n)
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    int tails[30], len = 0;
    for (int i = 0; i < n; i++) {
        int x;
        scanf("%d", &x);
        int p = (int)(std::lower_bound(tails, tails + len, x) - tails);
        tails[p] = x;                            // 严格上升：替换第一个 >= x 的
        if (p == len) len++;
    }
    printf("%d\n", len);
    return 0;
}
''',
  ["DP", "LIS", "二分"])

A("【DP】最长公共子序列", SEC_DP, 3,
  stmt("给定两个只含小写字母的字符串 `a`、`b`，求它们**最长公共子序列**的长度。",
       ["`f[i][j]` = `a` 前 `i` 个字符与 `b` 前 `j` 个字符的 LCS 长度",
        "字符相等就 `f[i][j] = f[i-1][j-1] + 1`，否则取 `max(f[i-1][j], f[i][j-1])`",
        "输出一个整数"]),
  "两行，各一个字符串。",
  "一行：LCS 长度。",
  "- 1 ≤ 串长 ≤ 10\n- 只含小写字母",
  lambda: cases("abcde\nace", "abc\nabc", "abc\ndef", "aab\naab",
                "zx\nyy", "algorithm\nlogarithm"),
  _lcs,
  r'''#include <cstdio>
#include <cstring>
int f[20][20];
int main() {
    char a[30], b[30];
    if (scanf("%29s %29s", a, b) != 2) return 0;
    int n = (int)strlen(a), m = (int)strlen(b);
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= m; j++)
            f[i][j] = (a[i - 1] == b[j - 1])
                      ? f[i - 1][j - 1] + 1
                      : (f[i - 1][j] > f[i][j - 1] ? f[i - 1][j] : f[i][j - 1]);
    printf("%d\n", f[n][m]);
    return 0;
}
''',
  r'''#include <cstdio>
#include <cstring>
char a[30], b[30];
int memo[20][20];
int go(int i, int j) {                           // 记忆化递归
    if (!i || !j) return 0;
    if (memo[i][j] >= 0) return memo[i][j];
    int r = (a[i - 1] == b[j - 1]) ? go(i - 1, j - 1) + 1
                                   : (go(i - 1, j) > go(i, j - 1) ? go(i - 1, j) : go(i, j - 1));
    return memo[i][j] = r;
}
int main() {
    if (scanf("%29s %29s", a, b) != 2) return 0;
    memset(memo, -1, sizeof memo);
    printf("%d\n", go((int)strlen(a), (int)strlen(b)));
    return 0;
}
''',
  ["DP", "LCS", "记忆化"])

A("【DP】数字三角形最大路径和", SEC_DP, 2,
  stmt("给出一个 `n` 行的数字三角形。从顶部出发，每步只能走到**下一行的相邻位置**，"
       "一直走到底部，求路径上数字之和的最大值。",
       ["自底向上：`f[i][j] = a[i][j] + max(f[i+1][j], f[i+1][j+1])`",
        "自顶向下要额外处理边界，倒着推更省事 —— 最后一行的值就是它自己",
        "输出一个整数"]),
  "第一行 `n`；之后 `n` 行，第 `i` 行有 `i` 个整数。",
  "一行：最大路径和。",
  "- 1 ≤ n ≤ 8\n- 0 ≤ 数字 ≤ 99",
  lambda: cases("1\n5", "3\n1\n2 3\n4 5 6", "4\n9\n1 2\n3 1 4\n1 2 3 1",
                "5\n7\n3 8\n8 1 0\n2 7 4 4\n4 5 2 6 5", "2\n0\n0 0", "3\n100\n0 0\n0 0 0"),
  _triangle,
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    int a[15][15];
    for (int i = 0; i < n; i++)
        for (int j = 0; j <= i; j++) scanf("%d", &a[i][j]);
    for (int i = n - 2; i >= 0; i--)             // 自底向上
        for (int j = 0; j <= i; j++)
            a[i][j] += (a[i + 1][j] > a[i + 1][j + 1] ? a[i + 1][j] : a[i + 1][j + 1]);
    printf("%d\n", a[0][0]);
    return 0;
}
''',
  r'''#include <cstdio>
int n, a[15][15];
int best(int i, int j) {                         // 记忆化：自顶向下
    if (i == n - 1) return a[i][j];
    static int memo[15][15];
    static int done[15][15];
    if (done[i][j]) return memo[i][j];
    int x = best(i + 1, j), y = best(i + 1, j + 1);
    done[i][j] = 1;
    return memo[i][j] = a[i][j] + (x > y ? x : y);
}
int main() {
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    for (int i = 0; i < n; i++)
        for (int j = 0; j <= i; j++) scanf("%d", &a[i][j]);
    printf("%d\n", best(0, 0));
    return 0;
}
''',
  ["DP", "数字三角形", "自底向上"])

A("【DP】最大子段和", SEC_DP, 2,
  stmt("给定 `n` 个整数（可能为负），求**连续子段**的最大和。子段至少要取一个数。",
       ["`cur = max(a[i], cur + a[i])`，`ans = max(ans, cur)` —— 这就是 Kadane",
        "`cur` 一旦变负就直接放弃、从当前数重开，因为负数只会拖累后面的和",
        "输出一个整数"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：最大子段和。",
  "- 1 ≤ n ≤ 12\n- -100 ≤ a[i] ≤ 100",
  lambda: cases("5\n1 -2 3 4 -1", "3\n-1 -2 -3", "1\n0", "4\n2 2 -1 2",
                "6\n-2 1 -3 4 -1 2", "5\n5 -1 5 -1 5"),
  _maxseg,
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    long long cur = 0, ans = 0;
    for (int i = 0; i < n; i++) {
        long long x;
        scanf("%lld", &x);
        if (i == 0 || cur < 0) cur = x;          // 前面的和对后面没贡献就丢掉
        else cur += x;
        if (i == 0 || cur > ans) ans = cur;
    }
    printf("%lld\n", ans);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {                                     // 前缀和 + 维护最小前缀
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    long long s = 0, mn = 0, ans = 0;
    for (int i = 0; i < n; i++) {
        long long x;
        scanf("%lld", &x);
        s += x;
        if (i == 0 || s - mn > ans) ans = s - mn;
        if (s < mn) mn = s;                      // 更新最小前缀（当前元素之后才用）
    }
    printf("%lld\n", ans);
    return 0;
}
''',
  ["DP", "最大子段和", "Kadane"])

A("【DP】爬楼梯方案数", SEC_DP, 1,
  stmt("楼梯共 `n` 级，每次可以上 **1 级或 2 级**，问从地面走到第 `n` 级共有多少种走法。",
       ["`f[n] = f[n-1] + f[n-2]`，也就是斐波那契数列（`f[1]=1, f[2]=2`）",
        "也可以直接用组合数算：走了 `k` 次两级，方案数 `C(n-k, k)`，对 `k` 求和",
        "输出一个整数"]),
  "一行，一个整数 `n`。",
  "一行：走法总数。",
  "- 1 ≤ n ≤ 20",
  lambda: cases("1", "2", "3", "5", "10", "20"),
  _climb,
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    long long f[30];
    f[1] = 1;
    f[2] = 2;
    for (int i = 3; i <= n; i++) f[i] = f[i - 1] + f[i - 2];
    printf("%lld\n", f[n]);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {                                     // 只用两个滚动变量
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    long long a = 1, b = 2;                      // a = f[1], b = f[2]
    if (n == 1) { printf("1\n"); return 0; }
    for (int i = 3; i <= n; i++) {
        long long c = a + b;
        a = b;
        b = c;
    }
    printf("%lld\n", b);
    return 0;
}
''',
  ["DP", "斐波那契", "滚动变量"])

A("【DP】打家劫舍", SEC_DP, 3,
  stmt("一条街上有 `n` 户人家，第 `i` 户有现金 `a[i]`。若一夜之内偷了两户**相邻**的人家，"
       "报警器就会响。求一夜最多能偷到多少钱。",
       ["`f[i]` = 考虑前 `i` 户的最大收益：`f[i] = max(f[i-1], f[i-2] + a[i])`",
        "含义是「第 i 户不偷」或「偷第 i 户、但第 i-1 户不能偷」",
        "输出一个整数"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：最大金额。",
  "- 1 ≤ n ≤ 12\n- 0 ≤ a[i] ≤ 100",
  lambda: cases("4\n1 2 3 1", "5\n2 7 9 3 1", "1\n5", "2\n2 7",
                "5\n0 0 0 0 0", "6\n10 1 1 10 1 1"),
  _rob,
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    long long p2 = 0, p1 = 0;                    // p2 = f[i-2], p1 = f[i-1]
    for (int i = 0; i < n; i++) {
        long long x;
        scanf("%lld", &x);
        long long cur = p1 > p2 + x ? p1 : p2 + x;
        p2 = p1;
        p1 = cur;
    }
    printf("%lld\n", p1);
    return 0;
}
''',
  r'''#include <cstdio>
long long a[30];
long long f(int i) {                             // 记忆化递归，从后往前
    if (i < 0) return 0;
    if (i == 0) return a[0];
    static long long memo[30];
    static int done[30];
    if (done[i]) return memo[i];
    long long x = f(i - 1), y = f(i - 2) + a[i];
    done[i] = 1;
    return memo[i] = (x > y ? x : y);
}
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    for (int i = 0; i < n; i++) scanf("%lld", &a[i]);
    printf("%lld\n", f(n - 1));
    return 0;
}
''',
  ["DP", "打家劫舍", "相邻约束"])

A("【DP】编辑距离", SEC_DP, 4,
  stmt("给定两个字符串 `a`、`b`，每次可以**插入 / 删除 / 替换**一个字符，"
       "求把 `a` 变成 `b` 所需的最少操作次数。",
       ["`f[i][j]` = `a` 前 `i` 个变成 `b` 前 `j` 个的最少操作数",
        "字符相同：`f[i][j] = f[i-1][j-1]`；不同：`1 + min(删, 增, 换)`",
        "输出一个整数"]),
  "两行，各一个字符串（可含空格以外字符）。",
  "一行：最少操作次数。",
  "- 1 ≤ 串长 ≤ 8",
  lambda: cases("abc\nabc", "abc\nabd", "abc\nbc", "kitten\nsitting",
                "a\nb", "abcd\nbadc"),
  _edit,
  r'''#include <cstdio>
#include <cstring>
int f[20][20];
int main() {
    char a[30] = "", b[30] = "";
    if (scanf("%29s", a) != 1) return 0;
    scanf("%29s", b);
    int n = (int)strlen(a), m = (int)strlen(b);
    for (int i = 0; i <= n; i++) f[i][0] = i;    // 全删
    for (int j = 0; j <= m; j++) f[0][j] = j;    // 全插
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= m; j++) {
            if (a[i - 1] == b[j - 1]) f[i][j] = f[i - 1][j - 1];
            else {
                int t = f[i - 1][j - 1];         // 替换
                if (f[i - 1][j] < t) t = f[i - 1][j];   // 删除
                if (f[i][j - 1] < t) t = f[i][j - 1];   // 插入
                f[i][j] = t + 1;
            }
        }
    printf("%d\n", f[n][m]);
    return 0;
}
''',
  r'''#include <cstdio>
#include <cstring>
char a[30], b[30];
int memo[20][20];
int go(int i, int j) {                           // 记忆化递归（后缀版）
    if (i == 0) return j;
    if (j == 0) return i;
    if (memo[i][j] >= 0) return memo[i][j];
    int r;
    if (a[i - 1] == b[j - 1]) r = go(i - 1, j - 1);
    else {
        int t = go(i - 1, j - 1);
        int x = go(i - 1, j), y = go(i, j - 1);
        if (x < t) t = x;
        if (y < t) t = y;
        r = t + 1;
    }
    return memo[i][j] = r;
}
int main() {
    a[0] = b[0] = 0;
    if (scanf("%29s", a) != 1) return 0;
    scanf("%29s", b);
    memset(memo, -1, sizeof memo);
    printf("%d\n", go((int)strlen(a), (int)strlen(b)));
    return 0;
}
''',
  ["DP", "编辑距离", "字符串"])

A("【DP】石子合并最小代价", SEC_DP, 4,
  stmt("有 `n` 堆石子排成一排，第 `i` 堆有 `a[i]` 个。每次只能把**相邻两堆**合并成一堆，"
       "代价是这两堆石子数之和。求合并成一堆的**最小总代价**。",
       ["`f[l][r]` = 把 `[l, r]` 合并成一堆的最小代价 = `w(l,r) + min(f[l][k] + f[k+1][r])`",
        "`w(l,r)` 是这段石子的总和，先做前缀和，否则每次重算就是 O(n) 拖慢一层",
        "输出一个整数"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：最小总代价。",
  "- 1 ≤ n ≤ 5\n- 1 ≤ a[i] ≤ 10",
  lambda: cases("2\n1 2", "1\n5", "3\n1 2 3", "4\n4 1 2 3", "5\n1 1 1 1 1", "3\n10 1 10"),
  _stone,
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    long long a[30], s[30] = {0}, f[30][30] = {0};
    for (int i = 1; i <= n; i++) { scanf("%lld", &a[i]); s[i] = s[i - 1] + a[i]; }
    for (int len = 2; len <= n; len++)
        for (int l = 1; l + len - 1 <= n; l++) {
            int r = l + len - 1;
            f[l][r] = -1;
            for (int k = l; k < r; k++) {
                long long t = f[l][k] + f[k + 1][r];
                if (f[l][r] < 0 || t < f[l][r]) f[l][r] = t;
            }
            f[l][r] += s[r] - s[l - 1];           // 加上本区间的总石子数
        }
    printf("%lld\n", n == 1 ? 0LL : f[1][n]);
    return 0;
}
''',
  r'''#include <cstdio>
#include <cstring>
long long a[30], s[30], memo[30][30];
long long go(int l, int r) {                     // 记忆化递归（区间版）
    if (l == r) return 0;
    if (memo[l][r] >= 0) return memo[l][r];
    long long best = -1;
    for (int k = l; k < r; k++) {
        long long t = go(l, k) + go(k + 1, r);
        if (best < 0 || t < best) best = t;
    }
    return memo[l][r] = best + s[r] - s[l - 1];
}
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    for (int i = 1; i <= n; i++) { scanf("%lld", &a[i]); s[i] = s[i - 1] + a[i]; }
    memset(memo, -1, sizeof memo);
    printf("%lld\n", go(1, n));
    return 0;
}
''',
  ["DP", "区间DP", "石子合并"])


def _pathobs(t):
    """带障碍路径计数：DFS 枚举所有走法。"""
    r = rows(t)
    n, m = int(r[0][0]), int(r[0][1])
    g = [x[0] for x in r[1:]]
    cnt = [0]

    def go(i, j):
        if i >= n or j >= m or g[i][j] == '#':
            return
        if i == n - 1 and j == m - 1:
            cnt[0] += 1
            return
        go(i + 1, j)
        go(i, j + 1)
    go(0, 0)
    return "%d\n" % cnt[0]


def _stock1(t):
    p = arr_of(t)
    best = 0
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            best = max(best, p[j] - p[i])
    return "%d\n" % best


def _coins(t):
    """最少硬币数：BFS 从 0 元往外扩，第一次到 amount 就是最少张数。"""
    v = toks(t)
    n, amount = v[0], v[1]
    c = v[2:2 + n]
    dist = {0: 0}
    q = deque([0])
    while q:
        s = q.popleft()
        if s == amount:
            return "%d\n" % dist[s]
        for x in c:
            if s + x <= amount and s + x not in dist:
                dist[s + x] = dist[s] + 1
                q.append(s + x)
    return "-1\n"


def _maxprod(t):
    a = arr_of(t)
    n = len(a)
    best = None
    for i in range(n):
        for j in range(i, n):
            p = 1
            for k in range(i, j + 1):
                p *= a[k]
            best = p if best is None else max(best, p)
    return "%d\n" % best


def _maxsubmat(t):
    r = [[int(x) for x in ln] for ln in rows(t)]
    n, m = int(r[0][0]), int(r[0][1])
    g = r[1:1 + n]
    best = None
    for r1 in range(n):
        for r2 in range(r1, n):
            for c1 in range(m):
                for c2 in range(c1, m):
                    s = sum(g[i][j] for i in range(r1, r2 + 1) for j in range(c1, c2 + 1))
                    best = s if best is None else max(best, s)
    return "%d\n" % best


def _gknap(t):
    """分组背包：每组的选择做笛卡尔积。"""
    r = rows(t)
    g, V = int(r[0][0]), int(r[0][1])
    groups, k = [], 1
    for _ in range(g):
        cnt = int(r[k][0])
        groups.append([(int(a), int(b)) for a, b in r[k + 1:k + 1 + cnt]])
        k += 1 + cnt
    best = [0]

    def go(i, cap, val):
        if i == g:
            best[0] = max(best[0], val)
            return
        go(i + 1, cap, val)                       # 这组一件都不选
        for w, v in groups[i]:
            if w <= cap:
                go(i + 1, cap - w, val + v)
    go(0, V, 0)
    return "%d\n" % best[0]


def _lps(t):
    s = strs(t)[0]
    n = len(s)
    best = 0
    for mask in range(1 << n):
        sub = "".join(s[i] for i in range(n) if mask >> i & 1)
        if len(sub) <= best:
            continue
        if sub == sub[::-1]:
            best = len(sub)
    return "%d\n" % best


def _wordbreak(t):
    v = strs(t)
    s = v[0]
    n = int(v[1].split()[0])
    words = [x.strip() for x in v[2:2 + n]]
    ok = [False]

    def go(pos):
        if pos == len(s):
            ok[0] = True
            return
        for w in words:
            if s.startswith(w, pos):
                go(pos + len(w))
    go(0)
    return "YES\n" if ok[0] else "NO\n"


def _chain(t):
    """矩阵链：枚举所有括号化（Catalan 种），逐个算代价取最小。"""
    tok = toks(t)
    n = tok[0]
    p = tok[1:1 + n + 1]                          # p[0..n]，第 i 个矩阵是 p[i] x p[i+1]

    def shapes(l, r):
        if l == r:
            return [("leaf", l)]
        out = []
        for k in range(l, r):
            for a in shapes(l, k):
                for b in shapes(k + 1, r):
                    out.append(("node", a, b))
        return out

    def cost(sh):
        if sh[0] == "leaf":
            i = sh[1]
            return 0, p[i], p[i + 1]
        c1, r1, m1 = cost(sh[1])
        c2, m2, c2b = cost(sh[2])
        return c1 + c2 + r1 * m1 * c2b, r1, c2b

    return "%d\n" % min(cost(sh)[0] for sh in shapes(0, n - 1))


def _coinways(t):
    """硬币组合方案数：枚举每种硬币取几枚（组合，与顺序无关）。"""
    v = toks(t)
    n, amount = v[0], v[1]
    c = v[2:2 + n]
    cnt = [0]

    def go(i, rest):
        if rest == 0:
            cnt[0] += 1
            return
        if i == n:
            return
        k = 0
        while k * c[i] <= rest:
            go(i + 1, rest - k * c[i])
            k += 1
    go(0, amount)
    return "%d\n" % cnt[0]


A("【DP】带障碍路径计数", SEC_DP, 2,
  stmt("给一个 `n` 行 `m` 列的网格，`.` 表示空地、`#` 表示障碍。从左上角出发，"
       "每步只能**向右或向下**，求走到右下角的路径条数（障碍不能踩）。",
       ["`f[i][j] = f[i-1][j] + f[i][j-1]`，但 `grid[i][j] == '#'` 时 `f[i][j] = 0`",
        "第一行和第一列要单独初始化：碰到第一个障碍之后全是 0",
        "输出一个整数"]),
  "第一行 `n m`；之后 `n` 行，每行 `m` 个字符（`.` 或 `#`）。",
  "一行：路径条数。",
  "- 1 ≤ n, m ≤ 5",
  lambda: cases("2 2\n..\n..", "2 2\n.#\n#.", "1 3\n...", "3 3\n...\n.#.\n...",
                "2 3\n...\n...", "3 3\n#..\n...\n..."),
  _pathobs,
  r'''#include <cstdio>
int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    char g[15][15];
    long long f[15][15] = {0};
    for (int i = 0; i < n; i++) scanf("%14s", g[i]);
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++) {
            if (g[i][j] == '#') { f[i][j] = 0; continue; }
            if (!i && !j) { f[i][j] = 1; continue; }
            long long up = i ? f[i - 1][j] : 0;
            long long lf = j ? f[i][j - 1] : 0;
            f[i][j] = up + lf;
        }
    printf("%lld\n", f[n - 1][m - 1]);
    return 0;
}
''',
  r'''#include <cstdio>
int n, m;
char g[15][15];
long long memo[15][15];
int done[15][15];
long long go(int i, int j) {                     // 记忆化递归（从终点往回数）
    if (i < 0 || j < 0 || g[i][j] == '#') return 0;
    if (!i && !j) return 1;
    if (done[i][j]) return memo[i][j];
    done[i][j] = 1;
    return memo[i][j] = go(i - 1, j) + go(i, j - 1);
}
int main() {
    if (scanf("%d %d", &n, &m) != 2) return 0;
    for (int i = 0; i < n; i++) scanf("%14s", g[i]);
    printf("%lld\n", go(n - 1, m - 1));
    return 0;
}
''',
  ["DP", "路径计数", "障碍"])

A("【DP】股票买卖一次最大利润", SEC_DP, 2,
  stmt("给定 `n` 天的股票价格，你最多能**买入一次再卖出一次**（必须先买后卖，也可以不交易），"
       "求最大利润。",
       ["遍历时维护「到目前为止的最低买入价」，当天的最大利润就是 `price - minPrice`",
        "不交易时利润为 0，所以答案至少是 0 —— 别让全跌的情况输出负数",
        "输出一个整数"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：最大利润。",
  "- 1 ≤ n ≤ 10\n- 0 ≤ 价格 ≤ 100",
  lambda: cases("6\n7 1 5 3 6 4", "5\n7 6 4 3 1", "1\n5", "2\n1 5", "4\n2 4 1 7", "3\n1 2 3"),
  _stock1,
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    int mn = 1 << 30, best = 0;
    for (int i = 0; i < n; i++) {
        int x;
        scanf("%d", &x);
        if (x < mn) mn = x;
        if (x - mn > best) best = x - mn;
    }
    printf("%d\n", best);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {                                     // 正序求后缀最大值，再扫一遍
    int n, p[30];
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    for (int i = 0; i < n; i++) scanf("%d", &p[i]);
    int best = 0;
    static int mx[30];
    mx[n - 1] = p[n - 1];
    for (int i = n - 2; i >= 0; i--) mx[i] = p[i] > mx[i + 1] ? p[i] : mx[i + 1];
    for (int i = 0; i + 1 < n; i++)
        if (mx[i + 1] - p[i] > best) best = mx[i + 1] - p[i];
    printf("%d\n", best);
    return 0;
}
''',
  ["DP", "股票", "一次交易"])

A("【DP】最少硬币数", SEC_DP, 3,
  stmt("有 `n` 种面额的硬币，每种有**无限多枚**。要凑出金额 `amount`，求**最少**需要几枚；"
       "凑不出来输出 `-1`。",
       ["`f[j]` = 凑出 `j` 元的最少枚数，`f[0] = 0`，其余初始化为「无穷大」",
        "`f[j] = min(f[j], f[j-coin] + 1)`，最后看 `f[amount]` 是否还是无穷大",
        "输出一个整数"]),
  "第一行 `n amount`；第二行 `n` 个面额。",
  "一行：最少硬币数，或 `-1`。",
  "- 1 ≤ n ≤ 4\n- 0 ≤ amount ≤ 20\n- 1 ≤ 面额 ≤ 20",
  lambda: cases("3 11\n1 2 5", "1 3\n2", "2 6\n1 3", "3 0\n1 2 5", "2 7\n2 4", "4 20\n1 5 10 25"),
  _coins,
  r'''#include <cstdio>
int main() {
    int n, amount;
    if (scanf("%d %d", &n, &amount) != 2) return 0;
    int c[10];
    for (int i = 0; i < n; i++) scanf("%d", &c[i]);
    const int INF = 1000000;
    int f[105];
    for (int j = 0; j <= amount; j++) f[j] = INF;
    f[0] = 0;
    for (int i = 0; i < n; i++)
        for (int j = c[i]; j <= amount; j++)       // 正序：每种可用多次
            if (f[j - c[i]] + 1 < f[j]) f[j] = f[j - c[i]] + 1;
    printf("%d\n", f[amount] >= INF ? -1 : f[amount]);
    return 0;
}
''',
  r'''#include <cstdio>
int n, amount, c[10];
int memo[105];
int best(int rest) {                             // 记忆化：剩下 rest 元的最少枚数
    if (rest == 0) return 0;
    if (memo[rest] >= 0) return memo[rest];
    const int INF = 1000000;
    int r = INF;
    for (int i = 0; i < n; i++)
        if (c[i] <= rest) {
            int t = best(rest - c[i]);
            if (t + 1 < r) r = t + 1;
        }
    return memo[rest] = r;
}
int main() {
    if (scanf("%d %d", &n, &amount) != 2) return 0;
    for (int i = 0; i < n; i++) scanf("%d", &c[i]);
    for (int j = 0; j <= amount; j++) memo[j] = -1;
    int r = best(amount);
    printf("%d\n", r >= 1000000 ? -1 : r);
    return 0;
}
''',
  ["DP", "完全背包", "最少硬币"])

A("【DP】最大乘积子数组", SEC_DP, 4,
  stmt("给定 `n` 个整数（可正可负），求**连续子数组**的最大乘积。子数组至少要取一个数。",
       ["负负得正 —— 所以必须**同时**维护以当前元素结尾的最大值和最小值",
        "`mx = max(a, mx*a, mn*a)`、`mn = min(a, mx*a, mn*a)`，注意要用旧值算新值",
        "输出一个整数"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：最大乘积。",
  "- 1 ≤ n ≤ 8\n- -10 ≤ a[i] ≤ 10",
  lambda: cases("3\n2 3 -2", "1\n-2", "3\n-2 0 -1", "3\n-2 3 -4", "2\n0 2", "5\n1 -2 -3 4 -5"),
  _maxprod,
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    long long a[30];
    for (int i = 0; i < n; i++) scanf("%lld", &a[i]);
    long long fmax[30], fmin[30], best = a[0];
    fmax[0] = fmin[0] = a[0];
    for (int i = 1; i < n; i++) {
        long long p1 = fmax[i - 1] * a[i], p2 = fmin[i - 1] * a[i];
        fmax[i] = a[i];
        if (p1 > fmax[i]) fmax[i] = p1;
        if (p2 > fmax[i]) fmax[i] = p2;
        fmin[i] = a[i];
        if (p1 < fmin[i]) fmin[i] = p1;
        if (p2 < fmin[i]) fmin[i] = p2;
        if (fmax[i] > best) best = fmax[i];
    }
    printf("%lld\n", best);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    long long mx = 0, mn = 0, best = 0;
    for (int i = 0; i < n; i++) {
        long long x;
        scanf("%lld", &x);
        if (i == 0) { mx = mn = best = x; continue; }
        long long a = mx * x, b = mn * x;
        long long hi = x, lo = x;
        if (a > hi) hi = a;
        if (b > hi) hi = b;
        if (a < lo) lo = a;
        if (b < lo) lo = b;
        mx = hi;
        mn = lo;
        if (mx > best) best = mx;
    }
    printf("%lld\n", best);
    return 0;
}
''',
  ["DP", "乘积", "正负号"])

A("【DP】最大子矩阵和", SEC_DP, 4,
  stmt("给定一个 `n` 行 `m` 列的整数矩阵，求它的**子矩阵**（连续的行区间 × 连续的列区间）"
       "元素和的最大值。子矩阵至少要含一个元素。",
       ["先用二维前缀和把「任意子矩阵求和」降到 O(1)，再枚举四条边 —— `n,m ≤ 4` 完全够用",
        "更快的做法是「枚举行的上下界 + 压成一维跑 Kadane」，复杂度 O(n²m)",
        "输出一个整数"]),
  "第一行 `n m`；之后 `n` 行，每行 `m` 个整数。",
  "一行：最大子矩阵和。",
  "- 1 ≤ n, m ≤ 4\n- -50 ≤ 元素 ≤ 50",
  lambda: cases("1 1\n-5", "2 2\n1 2\n3 4", "2 2\n-1 -2\n-3 -4",
                "3 3\n1 -2 3\n-4 5 -6\n7 -8 9", "1 3\n-1 5 -2", "3 2\n2 -1\n-1 2\n-1 -1"),
  _maxsubmat,
  r'''#include <cstdio>
int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    long long a[15][15], s[15][15] = {0};
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= m; j++) scanf("%lld", &a[i][j]);
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= m; j++)
            s[i][j] = a[i][j] + s[i - 1][j] + s[i][j - 1] - s[i - 1][j - 1];
    long long best = 0;
    int first = 1;
    for (int r1 = 1; r1 <= n; r1++)
        for (int r2 = r1; r2 <= n; r2++)
            for (int c1 = 1; c1 <= m; c1++)
                for (int c2 = c1; c2 <= m; c2++) {
                    long long t = s[r2][c2] - s[r1 - 1][c2] - s[r2][c1 - 1] + s[r1 - 1][c1 - 1];
                    if (first || t > best) { best = t; first = 0; }
                }
    printf("%lld\n", best);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {                                     // 枚举上下界，压成一维跑 Kadane
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    long long a[15][15];
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= m; j++) scanf("%lld", &a[i][j]);
    long long best = 0;
    int first = 1;
    for (int top = 1; top <= n; top++) {
        long long col[15] = {0};
        for (int bot = top; bot <= n; bot++) {
            for (int j = 1; j <= m; j++) col[j] += a[bot][j];
            long long cur = 0;
            for (int j = 1; j <= m; j++) {       // 一维最大子段和
                cur = (cur > 0 ? cur : 0) + col[j];
                if (first || cur > best) { best = cur; first = 0; }
            }
        }
    }
    printf("%lld\n", best);
    return 0;
}
''',
  ["DP", "最大子矩阵", "前缀和"])

A("【DP】分组背包最大价值", SEC_DP, 3,
  stmt("有 `g` 组物品和一个容量为 `V` 的背包。每组内有若干件物品（各有重量与价值），"
       "**每组最多只能选一件**，求不超过容量能拿到的最大总价值。",
       ["外层循环组，内层**倒序**循环容量 —— 这样每组只可能被选一次",
        "组内的每件物品都要试一遍，等价于「这一组选谁」取最大",
        "输出一个整数"]),
  "第一行 `g V`；之后 `g` 组，每组第一行 `k`，随后 `k` 行 `w v`。",
  "一行：最大总价值。",
  "- 1 ≤ g ≤ 3\n- 每组 1 ≤ k ≤ 2\n- 0 ≤ V ≤ 10\n- 1 ≤ w, v ≤ 100",
  lambda: cases("1 10\n1\n5 8", "2 10\n2\n3 4\n6 9\n1\n4 5", "1 5\n2\n2 3\n3 4",
                "2 3\n1\n5 100\n1\n2 3", "3 8\n1\n2 2\n1\n3 3\n1\n4 4", "2 0\n1\n1 5\n1\n1 6"),
  _gknap,
  r'''#include <cstdio>
int main() {
    int g, V;
    if (scanf("%d %d", &g, &V) != 2) return 0;
    long long f[105] = {0};
    for (int t = 0; t < g; t++) {
        int k;
        scanf("%d", &k);
        int w[10], v[10];
        for (int i = 0; i < k; i++) scanf("%d %d", &w[i], &v[i]);
        for (int j = V; j >= 0; j--)               // ★ 倒序：每组只用一次
            for (int i = 0; i < k; i++)
                if (j >= w[i] && f[j - w[i]] + v[i] > f[j]) f[j] = f[j - w[i]] + v[i];
    }
    printf("%lld\n", f[V]);
    return 0;
}
''',
  r'''#include <cstdio>
long long memo[10][105];
int g, V, wn[10][10], vn[10][10], kn[10];
long long best(int gi, int cap) {                // 记忆化：第 gi 组起、剩 cap 容量
    if (gi == g) return 0;
    if (memo[gi][cap] >= 0) return memo[gi][cap];
    long long r = best(gi + 1, cap);             // 这组不选
    for (int i = 0; i < kn[gi]; i++)
        if (wn[gi][i] <= cap) {
            long long t = best(gi + 1, cap - wn[gi][i]) + vn[gi][i];
            if (t > r) r = t;
        }
    return memo[gi][cap] = r;
}
int main() {
    if (scanf("%d %d", &g, &V) != 2) return 0;
    for (int t = 0; t < g; t++) {
        scanf("%d", &kn[t]);
        for (int i = 0; i < kn[t]; i++) scanf("%d %d", &wn[t][i], &vn[t][i]);
    }
    for (int i = 0; i <= g; i++)
        for (int j = 0; j <= V; j++) memo[i][j] = -1;
    printf("%lld\n", best(0, V));
    return 0;
}
''',
  ["DP", "分组背包", "倒序"])

A("【DP】最长回文子序列长度", SEC_DP, 4,
  stmt("给定一个字符串，求它的**最长回文子序列**长度（子序列不要求连续）。",
       ["`f[l][r]`：若 `s[l] == s[r]` 则 `f[l][r] = f[l+1][r-1] + 2`，否则取两端各让一步的最大值",
        "区间 DP 要按**区间长度从小到大**推，`len = 1` 时答案是 1",
        "输出一个整数"]),
  "一行，一个字符串。",
  "一行：最长回文子序列长度。",
  "- 1 ≤ 串长 ≤ 10\n- 只含小写字母",
  lambda: cases("a", "ab", "aaa", "abcba", "abcd", "aabbaa"),
  _lps,
  r'''#include <cstdio>
#include <cstring>
int f[20][20];
int main() {
    char s[30];
    if (scanf("%29s", s) != 1) return 0;
    int n = (int)strlen(s);
    for (int i = 0; i < n; i++) f[i][i] = 1;
    for (int len = 2; len <= n; len++)
        for (int l = 0; l + len - 1 < n; l++) {
            int r = l + len - 1;
            if (s[l] == s[r]) f[l][r] = (len == 2 ? 2 : f[l + 1][r - 1] + 2);
            else f[l][r] = f[l + 1][r] > f[l][r - 1] ? f[l + 1][r] : f[l][r - 1];
        }
    printf("%d\n", n ? f[0][n - 1] : 0);
    return 0;
}
''',
  r'''#include <cstdio>
#include <cstring>
char a[30], b[30];
int f[20][20];
int main() {                                     // 转成「原串 与 反转串 的 LCS」
    if (scanf("%29s", a) != 1) return 0;
    int n = (int)strlen(a);
    for (int i = 0; i < n; i++) b[i] = a[n - 1 - i];
    b[n] = 0;
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++)
            f[i][j] = (a[i - 1] == b[j - 1])
                      ? f[i - 1][j - 1] + 1
                      : (f[i - 1][j] > f[i][j - 1] ? f[i - 1][j] : f[i][j - 1]);
    printf("%d\n", f[n][n]);
    return 0;
}
''',
  ["DP", "回文", "区间DP"])

A("【DP】单词拆分", SEC_DP, 3,
  stmt("给定一个目标串和一个词典，问目标串能否由词典里的词**首尾相接**拼出来"
       "（每个词可以重复使用）。能则输出 `YES`，否则 `NO`。",
       ["`ok[i]` 表示前 `i` 个字符能否拼出来，`ok[0] = true`",
        "`ok[j]` 为真且 `s[j..i)` 在词典里 → `ok[i] = true`",
        "输出 `YES` 或 `NO`"]),
  "第一行目标串；第二行 `n`；之后 `n` 行，每行一个词。",
  "一行：`YES` 或 `NO`。",
  "- 1 ≤ 目标串长度 ≤ 10\n- 1 ≤ n ≤ 3",
  lambda: cases("leetcode\n2\nleet\ncode", "applepenapple\n2\napple\npen",
                "catsandog\n3\ncats\ndog\nsand", "a\n1\na", "ab\n1\na",
                "aaaa\n2\na\naa"),
  _wordbreak,
  r'''#include <cstdio>
#include <cstring>
int main() {
    char s[40], w[10][40];
    int n;
    if (scanf("%39s", s) != 1) return 0;
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 0; i < n; i++) scanf("%39s", w[i]);
    int L = (int)strlen(s);
    int ok[45] = {1};                             // ok[0] = 1
    for (int i = 0; i < L; i++) {
        if (!ok[i]) continue;
        for (int k = 0; k < n; k++) {
            int m = (int)strlen(w[k]);
            if (i + m <= L && strncmp(s + i, w[k], m) == 0) ok[i + m] = 1;
        }
    }
    printf("%s\n", ok[L] ? "YES" : "NO");
    return 0;
}
''',
  r'''#include <cstdio>
#include <cstring>
char s[40], w[10][40];
int n, L, memo[45];
int go(int pos) {                                // 记忆化递归：从 pos 往后切
    if (pos == L) return 1;
    if (memo[pos] >= 0) return memo[pos];
    memo[pos] = 0;
    for (int k = 0; k < n; k++) {
        int m = (int)strlen(w[k]);
        if (pos + m <= L && strncmp(s + pos, w[k], m) == 0 && go(pos + m)) {
            memo[pos] = 1;
            break;
        }
    }
    return memo[pos];
}
int main() {
    if (scanf("%39s", s) != 1) return 0;
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 0; i < n; i++) scanf("%39s", w[i]);
    L = (int)strlen(s);
    memset(memo, -1, sizeof memo);
    printf("%s\n", go(0) ? "YES" : "NO");
    return 0;
}
''',
  ["DP", "字符串", "单词拆分"])

A("【DP】矩阵链最小乘法次数", SEC_DP, 4,
  stmt("给定 `n` 个矩阵连乘，第 `i` 个矩阵是 `p[i] × p[i+1]`。矩阵乘法满足结合律，"
       "不同的加括号方式标量乘法次数不同，求**最少**次数。",
       ["`f[l][r]` = 第 `l` 到第 `r` 个矩阵相乘的最少次数，枚举断点 `k`",
        "`f[l][r] = min(f[l][k] + f[k+1][r] + p[l]*p[k+1]*p[r+1])`",
        "输出一个整数"]),
  "第一行 `n`；第二行 `n+1` 个整数 `p`。",
  "一行：最小乘法次数。",
  "- 1 ≤ n ≤ 5\n- 1 ≤ p[i] ≤ 100",
  lambda: cases("2\n10 20 30", "1\n5 6", "3\n10 20 30 40", "4\n40 20 30 10 30",
                "2\n1 1 1", "5\n30 35 15 5 10 20"),
  _chain,
  r'''#include <cstdio>
int main() {
    int n;
    long long p[20], f[20][20] = {0};
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    for (int i = 0; i <= n; i++) scanf("%lld", &p[i]);
    for (int len = 2; len <= n; len++)
        for (int l = 1; l + len - 1 <= n; l++) {
            int r = l + len - 1;
            f[l][r] = -1;
            for (int k = l; k < r; k++) {
                long long t = f[l][k] + f[k + 1][r] + p[l - 1] * p[k] * p[r];
                if (f[l][r] < 0 || t < f[l][r]) f[l][r] = t;
            }
        }
    printf("%lld\n", n == 1 ? 0LL : f[1][n]);
    return 0;
}
''',
  r'''#include <cstdio>
#include <cstring>
long long p[20], memo[20][20];
long long go(int l, int r) {                     // 记忆化递归（矩阵下标从 1 起）
    if (l == r) return 0;
    if (memo[l][r] >= 0) return memo[l][r];
    long long best = -1;
    for (int k = l; k < r; k++) {
        long long t = go(l, k) + go(k + 1, r) + p[l - 1] * p[k] * p[r];
        if (best < 0 || t < best) best = t;
    }
    return memo[l][r] = best;
}
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    for (int i = 0; i <= n; i++) scanf("%lld", &p[i]);
    memset(memo, -1, sizeof memo);
    printf("%lld\n", go(1, n));
    return 0;
}
''',
  ["DP", "矩阵链", "区间DP"])

A("【DP】硬币组合方案数", SEC_DP, 4,
  stmt("有 `n` 种面额的硬币，每种有无限多枚。求凑出金额 `amount` 的**方案数**"
       "（**组合**计数：`1+2` 与 `2+1` 算同一种）。",
       ["`f[j] += f[j-coin]`，外层枚举硬币、内层**正序**枚举金额 —— 这个顺序才是组合而不是排列",
        "`f[0] = 1`（凑 0 元有一种方案：什么都不拿）",
        "输出一个整数"]),
  "第一行 `n amount`；第二行 `n` 个面额。",
  "一行：方案数。",
  "- 1 ≤ n ≤ 3\n- 0 ≤ amount ≤ 20\n- 1 ≤ 面额 ≤ 20",
  lambda: cases("3 5\n1 2 5", "2 0\n1 2", "2 4\n1 2", "1 3\n2", "3 6\n1 3 4", "2 10\n2 5"),
  _coinways,
  r'''#include <cstdio>
int main() {
    int n, amount;
    if (scanf("%d %d", &n, &amount) != 2) return 0;
    int c[10];
    for (int i = 0; i < n; i++) scanf("%d", &c[i]);
    long long f[105] = {0};
    f[0] = 1;
    for (int i = 0; i < n; i++)
        for (int j = c[i]; j <= amount; j++)
            f[j] += f[j - c[i]];                   // 外层币、内层正序 = 组合
    printf("%lld\n", f[amount]);
    return 0;
}
''',
  r'''#include <cstdio>
int n, amount, c[10];
long long memo[10][105];
long long go(int i, int rest) {                  // 记忆化：从第 i 种起凑 rest 元
    if (rest == 0) return 1;
    if (i == n) return 0;
    if (memo[i][rest] >= 0) return memo[i][rest];
    long long r = 0;
    int k = 0;
    while (k * c[i] <= rest) {
        r += go(i + 1, rest - k * c[i]);
        k++;
    }
    return memo[i][rest] = r;
}
int main() {
    if (scanf("%d %d", &n, &amount) != 2) return 0;
    for (int i = 0; i < n; i++) scanf("%d", &c[i]);
    for (int i = 0; i <= n; i++)
        for (int j = 0; j <= amount; j++) memo[i][j] = -1;
    printf("%lld\n", go(0, amount));
    return 0;
}
''',
  ["DP", "组合计数", "完全背包"])


# ===================================================================== #
#  SEC_SIM · 综合模拟与数学（20 题）
# ===================================================================== #

def _joseph(t):
    n, m = toks(t)[:2]
    v = list(range(1, n + 1))
    i, out = 0, []
    while v:
        i = (i + m - 1) % len(v)
        out.append(v.pop(i))
    return " ".join(str(x) for x in out) + "\n"


def _snake(t):
    n = toks(t)[0]
    g = [[0] * n for _ in range(n)]
    cur = 1
    for i in range(n):
        for k in range(n):
            j = k if i % 2 == 0 else n - 1 - k
            g[i][j] = cur
            cur += 1
    return "".join(" ".join(str(x) for x in row) + "\n" for row in g)


def _spiral(t):
    n = toks(t)[0]
    g = [[0] * n for _ in range(n)]
    top, bot, lf, rt = 0, n - 1, 0, n - 1
    cur = 1
    while top <= bot and lf <= rt:
        for j in range(lf, rt + 1):
            g[top][j] = cur
            cur += 1
        top += 1
        for i in range(top, bot + 1):
            g[i][rt] = cur
            cur += 1
        rt -= 1
        if top <= bot:
            for j in range(rt, lf - 1, -1):
                g[bot][j] = cur
                cur += 1
            bot -= 1
        if lf <= rt:
            for i in range(bot, top - 1, -1):
                g[i][lf] = cur
                cur += 1
            lf += 1
    return "".join(" ".join(str(x) for x in row) + "\n" for row in g)


def _dates(t):
    import datetime as _dt
    v = [ln.split() for ln in t.strip().splitlines() if ln.strip()]
    d1 = _dt.date(int(v[0][0]), int(v[0][1]), int(v[0][2]))
    d2 = _dt.date(int(v[1][0]), int(v[1][1]), int(v[1][2]))
    return "%d\n" % (d2 - d1).days


DIGITS = "0123456789ABCDEF"


def _base(t):
    n, b = toks(t)[:2]
    if n == 0:
        return "0\n"
    s = ""
    while n:
        s = DIGITS[n % b] + s
        n //= b
    return s + "\n"


def _factzero(t):
    n = toks(t)[0]
    f = math.factorial(n)
    s = str(f)
    z = 0
    for ch in reversed(s):
        if ch != "0":
            break
        z += 1
    return "%d\n" % z


def _gcdlcm(t):
    a, b = toks(t)[:2]

    def g(x, y):
        while y:
            x, y = y, x % y
        return x
    d = g(a, b)
    return "%d %d\n" % (d, a // d * b)


def _primecnt(t):
    n = toks(t)[0]
    cnt = 0
    for x in range(2, n + 1):
        ok = True
        k = 2
        while k * k <= x:
            if x % k == 0:
                ok = False
                break
            k += 1
        if ok:
            cnt += 1
    return "%d\n" % cnt


def _combmod(t):
    n, k = toks(t)[:2]
    return "%d\n" % (math.comb(n, k) % 1000000007)


def _pascal(t):
    n = toks(t)[0]
    row = [math.comb(n, k) for k in range(n + 1)]
    return " ".join(str(x) for x in row) + "\n"


A("【模拟】约瑟夫环出列顺序", SEC_SIM, 2,
  stmt("`n` 个人围成一圈，编号 1 到 `n`。从 1 号开始报数，报到 `m` 的人出列，"
       "下一个人重新从 1 开始报，求所有人出列的顺序。",
       ["下标要来回绕：`i = (i + m - 1) % len(v)`，注意 `-1` 是因为报数从自己算起",
        "用数组模拟时，出列后**不要**把后面的人往前挪再回头找下标 —— 很容易差一位",
        "输出一行，出列编号用空格分隔"]),
  "一行两个整数 `n m`。",
  "一行：出列顺序，空格分隔。",
  "- 1 ≤ n ≤ 6\n- 1 ≤ m ≤ 5",
  lambda: cases("5 2", "1 1", "6 3", "3 5", "4 1", "2 2"),
  _joseph,
  r'''#include <cstdio>
int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2 || n <= 0) return 0;
    int gone[30] = {0}, left = n, pos = 0, first = 1;
    while (left) {
        int step = 0;
        while (step < m) {                        // 数 m 个还在圈里的人
            if (!gone[pos]) step++;
            if (step < m) pos = (pos + 1) % n;
        }
        if (!first) printf(" ");
        printf("%d", pos + 1);
        first = 0;
        gone[pos] = 1;
        left--;
        pos = (pos + 1) % n;
    }
    printf("\n");
    return 0;
}
''',
  r'''#include <cstdio>
int nx[40];
int main() {                                     // 循环链表模拟
    int n, m;
    if (scanf("%d %d", &n, &m) != 2 || n <= 0) return 0;
    for (int i = 0; i < n; i++) nx[i] = (i + 1) % n;
    int prev = n - 1, cur = 0, first = 1;
    for (int left = n; left > 0; left--) {
        for (int s = 1; s < m; s++) { prev = cur; cur = nx[cur]; }
        if (!first) printf(" ");
        printf("%d", cur + 1);
        first = 0;
        nx[prev] = nx[cur];                      // 摘掉 cur
        cur = nx[cur];
    }
    printf("\n");
    return 0;
}
''',
  ["模拟", "约瑟夫环", "循环链表"])

A("【模拟】蛇形填数", SEC_SIM, 2,
  stmt("输出一个 `n` 行 `n` 列的**蛇形矩阵**：第 1 行从左到右填 1 到 `n`，"
       "第 2 行从右到左接着填，第 3 行又从左到右……像蛇一样来回。",
       ["行号是偶数（0 基）就正着填，奇数就反着填",
        "也可以直接算：第 `i` 行第 `k` 个位置的值是 `i*n + k + 1`，只是列号要翻转",
        "输出 `n` 行，每行 `n` 个整数，空格分隔"]),
  "一行，一个整数 `n`。",
  "`n` 行，每行 `n` 个整数。",
  "- 1 ≤ n ≤ 6",
  lambda: cases("1", "2", "3", "4", "5", "6"),
  _snake,
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    int g[15][15], cur = 1;
    for (int i = 0; i < n; i++)
        for (int k = 0; k < n; k++) {
            int j = (i % 2 == 0) ? k : (n - 1 - k);
            g[i][j] = cur;
            cur++;
        }
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (j) printf(" ");
            printf("%d", g[i][j]);
        }
        printf("\n");
    }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {                                     // 不算矩阵，直接按公式输出
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    for (int i = 0; i < n; i++) {
        for (int k = 0; k < n; k++) {
            if (k) printf(" ");
            int v = (i % 2 == 0) ? (i * n + k + 1)          // 偶数行：正着
                                 : (i * n + (n - 1 - k) + 1); // 奇数行：反着
            printf("%d", v);
        }
        printf("\n");
    }
    return 0;
}
''',
  ["模拟", "矩阵", "蛇形"])

A("【模拟】螺旋矩阵", SEC_SIM, 3,
  stmt("输出一个 `n` 行 `n` 列的**螺旋矩阵**：从左上角开始顺时针由外向内填 1 到 `n²`。",
       ["维护四条边界 `top / bot / lf / rt`，每走完一条边就收缩对应的那条",
        "收缩后要重新判断 `top <= bot` 和 `lf <= rt`，否则奇数阶会重复写中心",
        "输出 `n` 行，每行 `n` 个整数，空格分隔"]),
  "一行，一个整数 `n`。",
  "`n` 行，每行 `n` 个整数。",
  "- 1 ≤ n ≤ 5",
  lambda: cases("1", "2", "3", "4", "5", "6"),
  _spiral,
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    int g[15][15], cur = 1;
    int top = 0, bot = n - 1, lf = 0, rt = n - 1;
    while (top <= bot && lf <= rt) {
        for (int j = lf; j <= rt; j++) g[top][j] = cur++;
        top++;
        for (int i = top; i <= bot; i++) g[i][rt] = cur++;
        rt--;
        if (top <= bot) { for (int j = rt; j >= lf; j--) g[bot][j] = cur++; bot--; }
        if (lf <= rt) { for (int i = bot; i >= top; i--) g[i][lf] = cur++; lf++; }
    }
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) { if (j) printf(" "); printf("%d", g[i][j]); }
        printf("\n");
    }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {                                     // 方向数组 + 撞墙转向
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int g[15][15];
    int dr[4] = {0, 1, 0, -1}, dc[4] = {1, 0, -1, 0};
    int r = 0, c = 0, d = 0;
    for (int k = 1; k <= n * n; k++) {
        g[r][c] = k;
        int nr = r + dr[d], nc = c + dc[d];
        if (nr < 0 || nr >= n || nc < 0 || nc >= n || g[nr][nc]) {   // 出界或已填
            d = (d + 1) % 4;
            nr = r + dr[d];
            nc = c + dc[d];
        }
        r = nr;
        c = nc;
    }
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) { if (j) printf(" "); printf("%d", g[i][j]); }
        printf("\n");
    }
    return 0;
}
''',
  ["模拟", "螺旋矩阵", "边界收缩"])

A("【数学】两个日期相差天数", SEC_SIM, 3,
  stmt("给定两个日期（年 月 日），求从第一个日期到第二个日期相差多少天。"
       "结果可能为负（第一个日期更晚时）。",
       ["闰年规则：能被 4 整除且不能被 100 整除，或者能被 400 整除",
        "月天数表里 2 月先按 28 记，是闰年再加 1",
        "输出一个整数"]),
  "两行，每行 `年 月 日`。",
  "一行：相差天数（第二行减第一行）。",
  "- 1900 ≤ 年 ≤ 2100\n- 日期保证合法",
  lambda: cases("2020 1 1\n2020 1 31", "2020 2 28\n2020 3 1", "2000 1 1\n2001 1 1",
                "2019 12 31\n2020 1 1", "2021 5 5\n2021 5 5", "1900 1 1\n1900 3 1"),
  _dates,
  r'''#include <cstdio>
int leap(int y) { return (y % 4 == 0 && y % 100 != 0) || y % 400 == 0; }
long long days(int y, int m, int d) {            // 距 1 年 1 月 1 日的天数
    int md[13] = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    long long s = 0;
    for (int i = 1; i < y; i++) s += leap(i) ? 366 : 365;
    for (int i = 1; i < m; i++) s += md[i] + (i == 2 && leap(y) ? 1 : 0);
    return s + d - 1;
}
int main() {
    int y1, m1, d1, y2, m2, d2;
    if (scanf("%d %d %d %d %d %d", &y1, &m1, &d1, &y2, &m2, &d2) != 6) return 0;
    printf("%lld\n", days(y2, m2, d2) - days(y1, m1, d1));
    return 0;
}
''',
  r'''#include <cstdio>
int leap(int y) { return (y % 4 == 0 && y % 100 != 0) || y % 400 == 0; }
int main() {                                     // 从早的日期逐天往晚的走
    int y1, m1, d1, y2, m2, d2;
    if (scanf("%d %d %d %d %d %d", &y1, &m1, &d1, &y2, &m2, &d2) != 6) return 0;
    int md[13] = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    int sign = 1;
    long long a = (long long)y1 * 10000 + m1 * 100 + d1;
    long long b = (long long)y2 * 10000 + m2 * 100 + d2;
    if (a > b) { sign = -1; int t; t = y1; y1 = y2; y2 = t; t = m1; m1 = m2; m2 = t; t = d1; d1 = d2; d2 = t; }
    long long cnt = 0;
    int y = y1, m = m1, d = d1;
    while (!(y == y2 && m == m2 && d == d2)) {
        int lim = md[m] + (m == 2 && leap(y) ? 1 : 0);
        d++;
        if (d > lim) { d = 1; m++; if (m > 12) { m = 1; y++; } }
        cnt++;
    }
    printf("%lld\n", sign * cnt);
    return 0;
}
''',
  ["数学", "日期", "闰年"])

A("【数学】十进制转任意进制", SEC_SIM, 2,
  stmt("把十进制整数 `n` 转换成 `b` 进制输出（`b` 可能是 2 到 16），"
       "10 以上用**大写字母** `A`~`F` 表示。",
       ["不断 `n % b` 取余数，再把 `n /= b`，最后把余数**倒过来**",
        "`n == 0` 要特判输出 `0` —— 否则循环一次都不进，输出空串",
        "输出一行"]),
  "一行两个整数 `n b`。",
  "一行：`b` 进制表示。",
  "- 0 ≤ n ≤ 100000\n- 2 ≤ b ≤ 16",
  lambda: cases("10 2", "255 16", "0 2", "7 8", "100 3", "100000 16"),
  _base,
  r'''#include <cstdio>
int main() {
    int n, b;
    if (scanf("%d %d", &n, &b) != 2) return 0;
    const char *D = "0123456789ABCDEF";
    if (n == 0) { printf("0\n"); return 0; }
    char s[40];
    int k = 0;
    while (n) { s[k++] = D[n % b]; n /= b; }
    for (int i = k - 1; i >= 0; i--) putchar(s[i]);
    printf("\n");
    return 0;
}
''',
  r'''#include <cstdio>
const char *D = "0123456789ABCDEF";
void pr(int n, int b) {                          // 递归：先处理高位
    if (n >= b) pr(n / b, b);
    putchar(D[n % b]);
}
int main() {
    int n, b;
    if (scanf("%d %d", &n, &b) != 2) return 0;
    if (n == 0) { printf("0\n"); return 0; }
    pr(n, b);
    printf("\n");
    return 0;
}
''',
  ["数学", "进制", "取模"])

A("【数学】阶乘末尾零的个数", SEC_SIM, 3,
  stmt("给定 `n`，求 `n!` 末尾有多少个连续的 0。",
       ["末尾的 0 来自因子 10 = 2 × 5，而 2 远比 5 多，所以只数**因子 5 的个数**",
        "`n/5 + n/25 + n/125 + ...`，因为 25 贡献两个 5、125 贡献三个",
        "`long long` 也不够装 1000! —— 别想着先把阶乘算出来",
        "输出一个整数"]),
  "一行，一个整数 `n`。",
  "一行：末尾零的个数。",
  "- 0 ≤ n ≤ 1000",
  lambda: cases("5", "10", "1", "100", "25", "1000"),
  _factzero,
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    long long cnt = 0;
    for (long long p = 5; p <= n; p *= 5) cnt += n / p;
    printf("%lld\n", cnt);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {                                     // 反复除以 5
    int n;
    if (scanf("%d", &n) != 1) return 0;
    long long cnt = 0;
    int t = n;
    while (t >= 5) { t /= 5; cnt += t; }
    printf("%lld\n", cnt);
    return 0;
}
''',
  ["数学", "阶乘", "因子5"])

A("【数学】最大公约数与最小公倍数", SEC_SIM, 1,
  stmt("给定两个正整数 `a`、`b`，输出它们的最大公约数和最小公倍数。",
       ["辗转相除：`while (b) { t = a % b; a = b; b = t; }`，循环结束 `a` 就是 gcd",
        "`lcm = a / gcd * b` —— **先除后乘**，否则 `a*b` 可能溢出",
        "输出两个整数，空格分隔"]),
  "一行两个正整数 `a b`。",
  "一行：`gcd lcm`。",
  "- 1 ≤ a, b ≤ 1000",
  lambda: cases("12 18", "7 13", "1 1", "100 75", "6 6", "1 1000"),
  _gcdlcm,
  r'''#include <cstdio>
int main() {
    long long a, b;
    if (scanf("%lld %lld", &a, &b) != 2) return 0;
    long long x = a, y = b;
    while (y) { long long t = x % y; x = y; y = t; }
    printf("%lld %lld\n", x, a / x * b);         // 先除后乘防溢出
    return 0;
}
''',
  r'''#include <cstdio>
int main() {                                     // 更相减损：大减小，直到相等
    long long a, b;
    if (scanf("%lld %lld", &a, &b) != 2) return 0;
    long long x = a, y = b;
    while (x != y) {
        if (x > y) x -= y;
        else y -= x;
    }
    printf("%lld %lld\n", x, a / x * b);
    return 0;
}
''',
  ["数学", "gcd", "lcm"])

A("【数学】区间内素数个数", SEC_SIM, 3,
  stmt("给定 `n`，统计 `1` 到 `n` 之间（含 `n`）有多少个素数。",
       ["试除法：判 `x` 是否素数只需试到 `sqrt(x)`，注意用 `k*k <= x` 而不是 `k <= sqrt(x)`",
        "`1` 不是素数、`2` 是素数 —— 这两条最容易漏",
        "输出一个整数"]),
  "一行，一个整数 `n`。",
  "一行：素数个数。",
  "- 1 ≤ n ≤ 10000",
  lambda: cases("1", "2", "10", "100", "1000", "10000"),
  _primecnt,
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int comp[10005];
    int cnt = 0;
    for (int i = 2; i <= n; i++) {               // 埃氏筛
        if (comp[i]) continue;
        cnt++;
        for (long long j = (long long)i * i; j <= n; j += i) comp[j] = 1;
    }
    printf("%d\n", cnt);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {                                     // 逐个试除
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int cnt = 0;
    for (int x = 2; x <= n; x++) {
        int ok = 1;
        for (int k = 2; (long long)k * k <= x; k++)
            if (x % k == 0) { ok = 0; break; }
        if (ok) cnt++;
    }
    printf("%d\n", cnt);
    return 0;
}
''',
  ["数学", "素数", "筛法"])

A("【数学】组合数取模", SEC_SIM, 4,
  stmt("给定 `n` 和 `k`，求 `C(n, k) mod 1000000007`。",
       ["递推式 `C(i, j) = C(i-1, j-1) + C(i-1, j)`（杨辉三角），`n ≤ 30` 直接打表",
        "也可以乘除约分：`res = res * (n-i) / (i+1)`，每一步都能整除，但要保证先乘后除不溢出",
        "输出一个整数"]),
  "一行两个整数 `n k`。",
  "一行：`C(n, k) mod 1000000007`。",
  "- 0 ≤ n ≤ 30\n- 0 ≤ k ≤ n",
  lambda: cases("5 2", "10 0", "30 15", "0 0", "6 3", "20 10"),
  _combmod,
  r'''#include <cstdio>
int main() {
    int n, k;
    if (scanf("%d %d", &n, &k) != 2) return 0;
    long long c[40][40] = {0};
    for (int i = 0; i <= n; i++) {
        c[i][0] = c[i][i] = 1;
        for (int j = 1; j < i; j++)
            c[i][j] = (c[i - 1][j - 1] + c[i - 1][j]) % 1000000007;
    }
    printf("%lld\n", c[n][k] % 1000000007);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {                                     // 乘除约分（n 小时结果不超 long long）
    int n, k;
    if (scanf("%d %d", &n, &k) != 2) return 0;
    if (k > n - k) k = n - k;                    // C(n,k) = C(n,n-k)，少算几步
    long long res = 1;
    for (int i = 1; i <= k; i++) {
        res = res * (n - k + i) / i;             // 每步都能整除
        res %= 1000000007;
    }
    printf("%lld\n", res % 1000000007);
    return 0;
}
''',
  ["数学", "组合数", "取模"])

A("【数学】杨辉三角第 n 行", SEC_SIM, 2,
  stmt("输出杨辉三角第 `n` 行（**从 0 开始编号**，第 0 行就是 `1`）。",
       ["第 `n` 行第 `k` 个数就是 `C(n, k)`",
        "用一维数组**倒序**更新可以原地算出整行（正序会用到本行已更新的值）",
        "输出一行，数字用空格分隔"]),
  "一行，一个整数 `n`。",
  "一行：第 `n` 行的所有数。",
  "- 0 ≤ n ≤ 12",
  lambda: cases("0", "1", "2", "3", "5", "12"),
  _pascal,
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n < 0) return 0;
    long long row[40] = {1};
    for (int i = 1; i <= n; i++)
        for (int j = i; j >= 1; j--) row[j] += row[j - 1];   // 倒序原地更新
    for (int j = 0; j <= n; j++) {
        if (j) printf(" ");
        printf("%lld", row[j]);
    }
    printf("\n");
    return 0;
}
''',
  r'''#include <cstdio>
int main() {                                     // 直接用组合数递推
    int n;
    if (scanf("%d", &n) != 1 || n < 0) return 0;
    long long v = 1;
    for (int k = 0; k <= n; k++) {
        if (k) printf(" ");
        printf("%lld", v);
        v = v * (n - k) / (k + 1);                // C(n,k+1) = C(n,k)*(n-k)/(k+1)
    }
    printf("\n");
    return 0;
}
''',
  ["数学", "杨辉三角", "组合数"])


def _partitions(t):
    n = toks(t)[0]

    def go(rem, mx):
        if rem == 0:
            return 1
        c = 0
        for k in range(min(rem, mx), 0, -1):
            c += go(rem - k, k)                  # 下一块不许比这一块大：天然去重
        return c
    return "%d\n" % go(n, n)


def _queue(t):
    v = [ln.strip() for ln in t.strip().splitlines() if ln.strip()]
    n = int(v[0])
    q, out = [], []
    for op in v[1:1 + n]:
        p = op.split()
        if p[0] == "push":
            q.append(p[1])
        elif p[0] == "pop":
            out.append(q.pop(0) if q else "EMPTY")
        else:
            out.append(str(len(q)))
    return "".join(x + "\n" for x in out)


def _mine(t):
    r = rows(t)
    n, m = int(r[0][0]), int(r[0][1])
    g = [ln[0] for ln in r[1:1 + n]]              # 每行是一个整串，按字符下标取
    res = []
    for i in range(n):
        line = []
        for j in range(m):
            if g[i][j] == "*":
                line.append("*")
                continue
            c = 0
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    if di == 0 and dj == 0:
                        continue
                    a, b = i + di, j + dj
                    if 0 <= a < n and 0 <= b < m and g[a][b] == "*":
                        c += 1
            line.append(str(c))
        res.append("".join(line))
    return "".join(x + "\n" for x in res)


def _frac(t):
    a, b = toks(t)[:2]
    if a == 0:
        return "0\n"
    def g(x, y):
        x, y = abs(x), abs(y)
        while y:
            x, y = y, x % y
        return x
    d = g(a, b)
    a //= d
    b //= d
    if b < 0:
        a, b = -a, -b
    return ("%d\n" % a) if b == 1 else ("%d/%d\n" % (a, b))


def _palindrome(t):
    v = toks(t)[0]
    if v < 0:
        return "NO\n"
    s = str(v)
    return "YES\n" if s == s[::-1] else "NO\n"


def _powmod(t):
    a, b, m = toks(t)[:3]
    return "%d\n" % pow(a, b, m)


def _divcnt(t):
    n = toks(t)[0]
    c = 0
    k = 1
    while k * k <= n:
        if n % k == 0:
            c += 1 if k * k == n else 2
        k += 1
    return "%d\n" % c


def _chicken(t):
    h, f = toks(t)[:2]
    for c in range(h + 1):
        r = h - c
        if 2 * c + 4 * r == f:
            return "%d %d\n" % (c, r)
    return "-1\n"


def _brackets(t):
    s = strs(t)[0]
    st = []
    pair = {")": "(", "]": "[", "}": "{"}
    for ch in s:
        if ch in "([{":
            st.append(ch)
        elif ch in pair:
            if not st or st.pop() != pair[ch]:
                return "NO\n"
    return "YES\n" if not st else "NO\n"


def _gcdall(t):
    a = arr_of(t)
    def g(x, y):
        while y:
            x, y = y, x % y
        return x
    d = 0
    for x in a:
        d = g(d, x)
    return "%d\n" % d


A("【数学】整数拆分方案数", SEC_SIM, 4,
  stmt("把正整数 `n` 写成若干个正整数之和（**不计顺序**，例如 `3 = 1+2` 与 `2+1` 算一种），"
       "求方案数。注意 `n` 本身也算一种拆法。",
       ["拆的时候强制「后一块不大于前一块」，同一种拆法就只会被数一次",
        "或者按完全背包理解：`f[j] += f[j-i]`，`i` 从 1 到 n 外层循环 —— 这才是组合不是排列",
        "输出一个整数"]),
  "一行，一个整数 `n`。",
  "一行：拆分方案数。",
  "- 1 ≤ n ≤ 12",
  lambda: cases("1", "2", "3", "5", "8", "12"),
  _partitions,
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    long long f[30] = {0};
    f[0] = 1;
    for (int i = 1; i <= n; i++)                 // 外层是「用到的最大数」
        for (int j = i; j <= n; j++) f[j] += f[j - i];
    printf("%lld\n", f[n]);
    return 0;
}
''',
  r'''#include <cstdio>
long long memo[30][30];
long long go(int rem, int mx) {                  // 记忆化：剩 rem，下一块不超过 mx
    if (rem == 0) return 1;
    if (memo[rem][mx] >= 0) return memo[rem][mx];
    long long c = 0;
    for (int k = (rem < mx ? rem : mx); k >= 1; k--) c += go(rem - k, k);
    return memo[rem][mx] = c;
}
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    for (int i = 0; i <= n; i++)
        for (int j = 0; j <= n; j++) memo[i][j] = -1;
    printf("%lld\n", go(n, n));
    return 0;
}
''',
  ["数学", "整数拆分", "组合"])

A("【模拟】队列操作序列", SEC_SIM, 2,
  stmt("按顺序执行 `n` 条队列操作：`push x` 入队、`pop` 出队（队列空时输出 `EMPTY`）、"
       "`size` 查询元素个数。按执行顺序输出 `pop` 和 `size` 的结果。",
       ["队列是**先进先出**，别写成栈的 `pop_back`",
        "`pop` 和 `size` 都要输出，`push` 不输出 —— 漏一条输出就全错位",
        "输出若干行，每行一个结果"]),
  "第一行 `n`；之后 `n` 行，每行一条操作。",
  "若干行：每次 `pop` / `size` 的结果。",
  "- 1 ≤ n ≤ 10\n- 0 ≤ x ≤ 100",
  lambda: cases("3\npush 1\npush 2\npop", "2\npop\nsize",
                "5\npush 5\nsize\npop\nsize\npop", "1\nsize",
                "4\npush 0\npush 0\npop\npop", "3\npop\npop\npop"),
  _queue,
  r'''#include <cstdio>
#include <cstring>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int q[105], head = 0, tail = 0;
    char op[20];
    for (int i = 0; i < n; i++) {
        scanf("%19s", op);
        if (!strcmp(op, "push")) { int x; scanf("%d", &x); q[tail++] = x; }
        else if (!strcmp(op, "pop")) {
            if (head == tail) printf("EMPTY\n");
            else printf("%d\n", q[head++]);
        } else printf("%d\n", tail - head);
    }
    return 0;
}
''',
  r'''#include <cstdio>
#include <cstring>
#include <queue>
int main() {                                     // 直接用 STL 的 queue
    int n;
    if (scanf("%d", &n) != 1) return 0;
    std::queue<int> q;
    char op[20];
    for (int i = 0; i < n; i++) {
        scanf("%19s", op);
        if (!strcmp(op, "push")) { int x; scanf("%d", &x); q.push(x); }
        else if (!strcmp(op, "pop")) {
            if (q.empty()) printf("EMPTY\n");
            else { printf("%d\n", q.front()); q.pop(); }
        } else printf("%d\n", (int)q.size());
    }
    return 0;
}
''',
  ["模拟", "队列", "FIFO"])

A("【模拟】扫雷数字统计", SEC_SIM, 3,
  stmt("给一个 `n` 行 `m` 列的雷区，`*` 是雷、`.` 是空地。对每个格子输出："
       "雷格输出 `*`，空地输出它**周围 8 个方向**上的雷数。",
       ["8 个方向就是 `di, dj ∈ {-1,0,1}` 的九宫格去掉 `(0,0)`",
        "越界一定要判，否则读到别的行会算出离谱的数字",
        "输出 `n` 行，每行 `m` 个字符，不要空格"]),
  "第一行 `n m`；之后 `n` 行，每行 `m` 个字符。",
  "`n` 行，每行 `m` 个字符。",
  "- 1 ≤ n, m ≤ 5",
  lambda: cases("1 1\n.", "1 1\n*", "2 2\n**\n**", "3 3\n...\n.*.\n...",
                "2 3\n.*.\n...", "3 3\n***\n***\n***"),
  _mine,
  r'''#include <cstdio>
int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    char g[15][15];
    for (int i = 0; i < n; i++) scanf("%14s", g[i]);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            if (g[i][j] == '*') { putchar('*'); continue; }
            int c = 0;
            for (int di = -1; di <= 1; di++)
                for (int dj = -1; dj <= 1; dj++) {
                    if (!di && !dj) continue;
                    int a = i + di, b = j + dj;
                    if (a >= 0 && a < n && b >= 0 && b < m && g[a][b] == '*') c++;
                }
            putchar('0' + c);
        }
        putchar('\n');
    }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {                                     // 二维前缀和求 3x3 窗口
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    char g[15][15];
    int s[20][20] = {0};
    for (int i = 0; i < n; i++) scanf("%14s", g[i]);
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= m; j++)
            s[i][j] = (g[i - 1][j - 1] == '*') + s[i - 1][j] + s[i][j - 1] - s[i - 1][j - 1];
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            if (g[i][j] == '*') { putchar('*'); continue; }
            int r1 = i - 1, c1 = j - 1, r2 = i + 2, c2 = j + 2;   // 九宫格 → 前缀区间
            if (r1 < 0) r1 = 0;
            if (c1 < 0) c1 = 0;
            if (r2 > n) r2 = n;
            if (c2 > m) c2 = m;
            int c = s[r2][c2] - s[r1][c2] - s[r2][c1] + s[r1][c1];
            putchar('0' + c);
        }
        putchar('\n');
    }
    return 0;
}
''',
  ["模拟", "扫雷", "八方向"])

A("【数学】分数化简", SEC_SIM, 2,
  stmt("给定一个分数 `a/b`（`b ≠ 0`，`a` 可能为负、`b` 也可能为负），把它化成最简形式。"
       "若化简后分母为 1，就只输出整数；负号一律放分子。",
       ["分子分母同除 `gcd(|a|, |b|)`；**负数取模要小心**，先取绝对值算 gcd",
        "分母是负数时把符号翻到分子上，`4/-6` 应输出 `-2/3`",
        "`a == 0` 直接输出 `0`（否则会输出 `0/1`）"]),
  "一行两个整数 `a b`。",
  "一行：最简分数或整数。",
  "- -1000 ≤ a ≤ 1000\n- 1 ≤ |b| ≤ 1000",
  lambda: cases("4 6", "-4 6", "4 -6", "6 3", "0 5", "7 1"),
  _frac,
  r'''#include <cstdio>
long long iabs(long long x) { return x < 0 ? -x : x; }
int main() {
    long long a, b;
    if (scanf("%lld %lld", &a, &b) != 2) return 0;
    if (a == 0) { printf("0\n"); return 0; }
    long long x = iabs(a), y = iabs(b);
    while (y) { long long t = x % y; x = y; y = t; }
    a /= x;
    b /= x;
    if (b < 0) { a = -a; b = -b; }
    if (b == 1) printf("%lld\n", a);
    else printf("%lld/%lld\n", a, b);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {                                     // 更相减损求 gcd
    long long a, b;
    if (scanf("%lld %lld", &a, &b) != 2) return 0;
    if (a == 0) { printf("0\n"); return 0; }
    long long x = a < 0 ? -a : a, y = b < 0 ? -b : b;
    long long p = x, q = y;
    while (p != q) {
        if (p > q) p -= q;
        else q -= p;
    }
    a /= p;
    b /= p;
    if (b < 0) { a = -a; b = -b; }
    if (b == 1) printf("%lld\n", a);
    else printf("%lld/%lld\n", a, b);
    return 0;
}
''',
  ["数学", "分数", "gcd"])

A("【模拟】回文数判断", SEC_SIM, 2,
  stmt("给定一个整数，判断它是不是回文数（正着读和倒着读一样）。负数不算回文。",
       ["转成字符串用双指针从前后来比最直观",
        "不想开字符串就用整数反转：`rev = rev*10 + x%10`，最后比 `rev == 原数`",
        "输出 `YES` 或 `NO`"]),
  "一行，一个整数。",
  "一行：`YES` 或 `NO`。",
  "- -2³¹ ≤ n ≤ 2³¹-1",
  lambda: cases("121", "-121", "10", "0", "12321", "1000"),
  _palindrome,
  r'''#include <cstdio>
int main() {
    long long n;
    if (scanf("%lld", &n) != 1) return 0;
    if (n < 0) { printf("NO\n"); return 0; }
    long long rev = 0, t = n;
    while (t) { rev = rev * 10 + t % 10; t /= 10; }
    printf("%s\n", rev == n ? "YES" : "NO");
    return 0;
}
''',
  r'''#include <cstdio>
#include <cstring>
int main() {                                     // 字符串双指针
    char s[40];
    if (scanf("%39s", s) != 1) return 0;
    if (s[0] == '-') { printf("NO\n"); return 0; }
    int i = 0, j = (int)strlen(s) - 1, ok = 1;
    while (i < j) {
        if (s[i] != s[j]) { ok = 0; break; }
        i++;
        j--;
    }
    printf("%s\n", ok ? "YES" : "NO");
    return 0;
}
''',
  ["模拟", "回文", "整数反转"])

A("【数学】快速幂取模", SEC_SIM, 4,
  stmt("给定 `a`、`b`、`m`，求 `a^b mod m`（`b` 可能很大，不能一层循环乘 `b` 次）。",
       ["把 `b` 按二进制拆开：每右移一位就把底数平方、`b` 的当前位是 1 就把它乘进答案",
        "每次乘完都要 `% m`，否则中途就溢出了",
        "`b == 0` 时答案是 `1 % m`（`m == 1` 时是 0）"]),
  "一行三个整数 `a b m`。",
  "一行：`a^b mod m`。",
  "- 0 ≤ a ≤ 1000\n- 0 ≤ b ≤ 10⁹\n- 1 ≤ m ≤ 10⁹",
  lambda: cases("2 10 1000", "3 0 7", "5 3 13", "7 5 1", "2 1000000000 1000000007",
                "123456 789 99991"),
  _powmod,
  r'''#include <cstdio>
int main() {
    long long a, b, m;
    if (scanf("%lld %lld %lld", &a, &b, &m) != 3) return 0;
    long long res = 1 % m;
    a %= m;
    while (b) {
        if (b & 1) res = res * a % m;            // 当前位是 1，乘进来
        a = a * a % m;                           // 底数平方
        b >>= 1;
    }
    printf("%lld\n", res);
    return 0;
}
''',
  r'''#include <cstdio>
long long pw(long long a, long long b, long long m) {   // 递归版
    if (b == 0) return 1 % m;
    long long t = pw(a, b / 2, m);
    t = t * t % m;
    if (b & 1) t = t * (a % m) % m;
    return t;
}
int main() {
    long long a, b, m;
    if (scanf("%lld %lld %lld", &a, &b, &m) != 3) return 0;
    printf("%lld\n", pw(a, b, m));
    return 0;
}
''',
  ["数学", "快速幂", "二进制"])

A("【数学】正约数个数", SEC_SIM, 3,
  stmt("给定正整数 `n`，求它有多少个正约数。",
       ["只需枚举到 `sqrt(n)`：`k` 是约数，`n/k` 也是，一对算两个",
        "`k*k == n` 时只算一个（完全平方数别重复数）",
        "输出一个整数"]),
  "一行，一个整数 `n`。",
  "一行：正约数个数。",
  "- 1 ≤ n ≤ 100000",
  lambda: cases("1", "12", "36", "97", "100000", "65536"),
  _divcnt,
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    int c = 0;
    for (int k = 1; (long long)k * k <= n; k++)
        if (n % k == 0) c += (k * k == n) ? 1 : 2;
    printf("%d\n", c);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {                                     // 直接枚举 1..n（n 小时也够快）
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    int c = 0;
    for (int k = 1; k <= n; k++)
        if (n % k == 0) c++;
    printf("%d\n", c);
    return 0;
}
''',
  ["数学", "约数", "sqrt"])

A("【数学】鸡兔同笼", SEC_SIM, 1,
  stmt("笼子里有鸡和兔，共有 `h` 个头、`f` 只脚。求鸡和兔各几只；"
       "若数据不可能成立，输出 `-1`。",
       ["设鸡 `c` 只、兔 `r` 只：`c + r = h`、`2c + 4r = f`，联立得 `r = (f - 2h) / 2`",
        "`f - 2h` 必须是**非负偶数**，否则无解",
        "输出 `鸡 兔`，空格分隔"]),
  "一行两个整数 `h f`。",
  "一行：`鸡 兔`，或 `-1`。",
  "- 0 ≤ h ≤ 100\n- 0 ≤ f ≤ 400",
  lambda: cases("35 94", "1 2", "1 3", "0 0", "10 20", "10 40"),
  _chicken,
  r'''#include <cstdio>
int main() {
    int h, f;
    if (scanf("%d %d", &h, &f) != 2) return 0;
    for (int c = 0; c <= h; c++) {               // 枚举鸡的只数
        int r = h - c;
        if (2 * c + 4 * r == f) { printf("%d %d\n", c, r); return 0; }
    }
    printf("-1\n");
    return 0;
}
''',
  r'''#include <cstdio>
int main() {                                     // 直接解方程
    int h, f;
    if (scanf("%d %d", &h, &f) != 2) return 0;
    int t = f - 2 * h;
    if (t < 0 || t % 2 != 0) { printf("-1\n"); return 0; }
    int r = t / 2, c = h - r;
    if (c < 0 || r < 0) { printf("-1\n"); return 0; }
    printf("%d %d\n", c, r);
    return 0;
}
''',
  ["数学", "方程", "枚举"])

A("【模拟】括号匹配判断", SEC_SIM, 3,
  stmt("给定一个只含 `()`、`[]`、`{}` 的字符串，判断括号是否**正确配对**"
       "（既不能多、不能少，也不能交叉）。正确输出 `YES`，否则 `NO`。",
       ["遇到左括号就压栈，遇到右括号就弹栈并检查类型是否对上",
        "右括号来时栈已经空了 = 多了右括号，遍历完栈非空 = 多了左括号，这两种都算 NO",
        "`([)]` 这种交叉嵌套必须判 NO —— 只数个数是查不出来的"]),
  "一行，一个括号串（长度 1 到 20）。",
  "一行：`YES` 或 `NO`。",
  "- 1 ≤ 串长 ≤ 20",
  lambda: cases("()", "([)]", "((", "{[()]}", "]", "()[]{}"),
  _brackets,
  r'''#include <cstdio>
#include <cstring>
int main() {
    char s[40];
    if (scanf("%39s", s) != 1) return 0;
    char st[40];
    int top = 0;
    for (int i = 0; s[i]; i++) {
        char ch = s[i];
        if (ch == '(' || ch == '[' || ch == '{') st[top++] = ch;
        else {
            char want = (ch == ')') ? '(' : (ch == ']' ? '[' : '{');
            if (top == 0 || st[top - 1] != want) { printf("NO\n"); return 0; }
            top--;
        }
    }
    printf("%s\n", top == 0 ? "YES" : "NO");
    return 0;
}
''',
  r'''#include <cstdio>
#include <cstring>
char s[40];
int main() {                                     // 反复消除成对的括号
    if (scanf("%39s", s) != 1) return 0;
    int changed = 1;
    while (changed) {
        changed = 0;
        int n = (int)strlen(s), k = 0;
        char t[40];
        for (int i = 0; i < n; i++) {
            if (i + 1 < n) {
                char a = s[i], b = s[i + 1];
                if ((a == '(' && b == ')') || (a == '[' && b == ']') || (a == '{' && b == '}')) {
                    i++;                             // 整对删掉
                    changed = 1;
                    continue;
                }
            }
            t[k++] = s[i];
        }
        t[k] = 0;
        strcpy(s, t);
    }
    printf("%s\n", s[0] == 0 ? "YES" : "NO");
    return 0;
}
''',
  ["模拟", "栈", "括号匹配"])

A("【数学】多个数的最大公约数", SEC_SIM, 2,
  stmt("给定 `n` 个正整数，求它们的最大公约数。",
       ["`gcd` 满足结合律：一路 `d = gcd(d, a[i])` 下来就是全体的 gcd",
        "`d` 的初值取 0 是安全的 —— `gcd(0, x) = x`",
        "输出一个整数"]),
  "第一行 `n`；第二行 `n` 个正整数。",
  "一行：这 `n` 个数的最大公约数。",
  "- 1 ≤ n ≤ 6\n- 1 ≤ a[i] ≤ 1000",
  lambda: cases("2\n12 18", "1\n7", "3\n8 12 16", "4\n5 10 15 20", "2\n9 28",
                "3\n100 100 100"),
  _gcdall,
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    long long d = 0;
    for (int i = 0; i < n; i++) {
        long long x;
        scanf("%lld", &x);
        long long a = d, b = x;
        while (b) { long long t = a % b; a = b; b = t; }
        d = a;
    }
    printf("%lld\n", d);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {                                     // 更相减损逐个合并
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    long long d = 0;
    for (int i = 0; i < n; i++) {
        long long x;
        scanf("%lld", &x);
        long long a = d, b = x;
        if (a == 0) { d = b; continue; }
        while (a != b) {
            if (a > b) a -= b;
            else b -= a;
        }
        d = a;
    }
    printf("%lld\n", d);
    return 0;
}
''',
  ["数学", "gcd", "结合律"])


if __name__ == "__main__":
    sys.exit(cli(PROBLEMS, "app/problems_bank_cpp_basic8.py",
                 "第 8 册：动态规划 / 综合模拟与数学", "CPP_BASIC8_PROBLEMS"))
