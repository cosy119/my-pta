# -*- coding: utf-8 -*-
"""C++ 基础编程题 · 第 3 册：一维数组（26）+ 二维数组与矩阵（14）= 40 题。

对应教材第 06 讲「数组、指针与字符串」的前半（p189~251）。
这一册专门练「下标」：越界、从 0 还是从 1 起、区间开闭、原地修改后长度变化。

★ 测试数据由固定 seed 的随机生成器产出，可复现；oracle 一律用 Python 直接模拟。
★ 矩阵题一律 `n ≤ 50`，栈上开 `int a[55][55]` 足够。

重生成：python tools/gen_cpp_basic3.py
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cpp_basic_kit import cases, cli, stmt          # noqa: E402

SEC_ARR = "C++ 编程 · 一维数组"
SEC_MAT = "C++ 编程 · 二维数组与矩阵"

PROBLEMS: list[dict] = []


def A(title, sec, d, st, inf, outf, con, inp, orc, sol, alt, tags):
    PROBLEMS.append(dict(title=title, section=sec, difficulty=d, statement_md=st,
                         input_format=inf, output_format=outf, constraints_md=con,
                         inputs=inp, oracle=orc, solution=sol, alt=alt, tags=tags))


# ------------------------------------------------------------------ #
#  数据生成
# ------------------------------------------------------------------ #
def arr(seed: int, n: int, lo: int = -50, hi: int = 50) -> str:
    rng = random.Random(seed)
    v = [rng.randint(lo, hi) for _ in range(n)]
    return "%d\n%s\n" % (n, " ".join(str(x) for x in v))


def arr_pos(seed: int, n: int, lo: int = 1, hi: int = 100) -> str:
    return arr(seed, n, lo, hi)


def sorted_arr(seed: int, n: int, lo: int = -50, hi: int = 50) -> str:
    rng = random.Random(seed)
    v = sorted(rng.randint(lo, hi) for _ in range(n))
    return "%d\n%s\n" % (n, " ".join(str(x) for x in v))


def mat(seed: int, n: int, lo: int = -20, hi: int = 20) -> str:
    rng = random.Random(seed)
    rows = [[rng.randint(lo, hi) for _ in range(n)] for _ in range(n)]
    return "%d\n" % n + "\n".join(" ".join(str(x) for x in r) for r in rows) + "\n"


def arr_with(seed: int, n: int, extra: int, lo: int = -50, hi: int = 50) -> str:
    """第一行写成 `n extra`，第二行是 n 个随机数（用于「n 和 x」类输入）。"""
    body = arr(seed, n, lo, hi).split("\n")[1]
    return "%d %d\n%s\n" % (n, extra, body)


def sorted_with(seed: int, n: int, extra: int, lo: int = -50, hi: int = 50) -> str:
    body = sorted_arr(seed, n, lo, hi).split("\n")[1]
    return "%d %d\n%s\n" % (n, extra, body)


def read_ints(t: str) -> list[int]:
    return list(map(int, t.split()))


def read_mat(t: str) -> tuple[int, list[list[int]]]:
    d = read_ints(t)
    n = d[0]
    v = d[1:]
    return n, [v[i * n:(i + 1) * n] for i in range(n)]


def out_row(v) -> str:
    return " ".join(str(x) for x in v) + "\n"


# ===================================================================== #
#  SEC_ARR · 一维数组（26 题）
# ===================================================================== #

A("【一维数组】求和与平均值", SEC_ARR, 1,
  stmt("读入 `n` 个整数，输出它们的和与平均值（平均值保留两位小数）。",
       ["和用 `long long`，100 个 10⁹ 级数会超 `int`",
        "平均值是 `(double)sum / n`，别写成 `sum / n`",
        "两行输出：先和，后平均"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "两行：和、平均值（两位小数）。",
  "- 1 ≤ n ≤ 100\n- |x| ≤ 10⁶",
  lambda: cases(arr(1, 5), arr(2, 1), arr(3, 20), arr(4, 100, -1000, 1000), arr(5, 7), arr(6, 33)),
  lambda t: "%d\n%.2f\n" % (lambda v: (sum(v), sum(v) / len(v)))(read_ints(t)[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    long long s = 0;
    for (int i = 0; i < n; i++) { int x; scanf("%d", &x); s += x; }
    printf("%lld\n", s);
    printf("%.2f\n", (double)s / n);
    return 0;
}
''',
  r'''#include <cstdio>
#include <vector>
#include <numeric>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    std::vector<int> a(n);
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    long long s = std::accumulate(a.begin(), a.end(), 0LL);   // 初值 0LL
    printf("%lld\n%.2f\n", s, (double)s / n);
    return 0;
}
''',
  ["C++基础", "数组", "累加"])

A("【一维数组】最大值及其首次下标", SEC_ARR, 1,
  stmt("读入 `n` 个整数，输出最大值和它**第一次出现**的下标（下标从 0 开始）。",
       ["初值用 `a[0]`，不要用 0 —— 全负数时 0 会变成答案",
        "比较用严格大于 `>`，这样相等时保留**首次**下标",
        "输出 `最大值 下标`，空格分隔"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行两个整数。",
  "- 1 ≤ n ≤ 100\n- |x| ≤ 10⁹",
  lambda: cases(arr(11, 5), arr(12, 1, -9, -1), arr(13, 10, -5, 5), arr(14, 100), arr(15, 6, 0, 3), arr(16, 8)),
  lambda t: (lambda v: "%d %d\n" % (max(v), v.index(max(v))))(read_ints(t)[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[105];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int best = 0;                     // 记录下标，靠 a 取值
    for (int i = 1; i < n; i++)
        if (a[i] > a[best]) best = i; // 严格大于 → 保留首次
    printf("%d %d\n", a[best], best);
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[105];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int *p = std::max_element(a, a + n);       // 返回首个最大值的指针
    printf("%d %d\n", *p, (int)(p - a));
    return 0;
}
''',
  ["C++基础", "数组", "最大值"])

A("【一维数组】最小值及其最后下标", SEC_ARR, 2,
  stmt("读入 `n` 个整数，输出最小值和它**最后一次出现**的下标。",
       ["要「最后」一次，比较必须用 `<=` 而不是 `<`",
        "这题专门和上一题对照：一个用 `>` 取首次，一个用 `<=` 取末次",
        "下标从 0 开始"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行两个整数。",
  "- 1 ≤ n ≤ 100\n- |x| ≤ 10⁹",
  lambda: cases(arr(21, 5, -3, 3), arr(22, 1), arr(23, 12, 0, 2), arr(24, 30, -1, 1), arr(25, 6, 5, 5), arr(26, 9)),
  lambda t: (lambda v: "%d %d\n" % (min(v), len(v) - 1 - v[::-1].index(min(v))))(read_ints(t)[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[105];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int best = 0;
    for (int i = 1; i < n; i++)
        if (a[i] <= a[best]) best = i;   // 小于等于 → 保留最后一次
    printf("%d %d\n", a[best], best);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[105];
    int mn = 0;
    for (int i = 0; i < n; i++) {
        scanf("%d", &a[i]);
        if (a[i] <= a[mn]) mn = i;       // 边读边判
    }
    printf("%d %d\n", a[mn], mn);
    return 0;
}
''',
  ["C++基础", "数组", "最小值", "下标"])

A("【一维数组】逆序输出", SEC_ARR, 1,
  stmt("读入 `n` 个整数，按**相反顺序**输出，空格分隔。",
       ["从 `n-1` 倒着遍历到 0",
        "输出之间一个空格，行末不要空格",
        "不需要真的把数组翻转，倒着打印就行"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行 `n` 个整数。",
  "- 1 ≤ n ≤ 100\n- |x| ≤ 10⁹",
  lambda: cases(arr(31, 5), arr(32, 1), arr(33, 10), arr(34, 100, -99, 99), arr(35, 2), arr(36, 17)),
  lambda t: out_row(read_ints(t)[1:][::-1]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[105];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    for (int i = n - 1; i >= 0; i--) {
        if (i != n - 1) printf(" ");
        printf("%d", a[i]);
    }
    printf("\n");
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[105];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    std::reverse(a, a + n);              // 原地翻转再正着打
    for (int i = 0; i < n; i++) printf(i ? " %d" : "%d", a[i]);
    printf("\n");
    return 0;
}
''',
  ["C++基础", "数组", "逆序"])

A("【一维数组】大于平均值的个数", SEC_ARR, 1,
  stmt("读入 `n` 个整数，输出**严格大于**平均值（实数平均）的元素个数。\n\n"
       "同时输出平均值本身，保留两位小数，先输出平均值再输出个数。",
       ["平均值用 `double` 算，比较时也用 `double`",
        "严格大于：等于平均值的**不算**",
        "先算完平均值再遍历一遍计数 —— 不能边读边判"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "两行：平均值（两位小数）、个数。",
  "- 1 ≤ n ≤ 100\n- |x| ≤ 10⁶",
  lambda: cases(arr(41, 5, 1, 9), arr(42, 1), arr(43, 10), arr(44, 40, -100, 100), arr(45, 6, 0, 10), arr(46, 33)),
  lambda t: (lambda v: "%.2f\n%d\n" % (sum(v) / len(v), sum(1 for x in v if x > sum(v) / len(v))))(read_ints(t)[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[105];
    long long s = 0;
    for (int i = 0; i < n; i++) { scanf("%d", &a[i]); s += a[i]; }
    double avg = (double)s / n;
    int cnt = 0;
    for (int i = 0; i < n; i++) if (a[i] > avg) cnt++;
    printf("%.2f\n%d\n", avg, cnt);
    return 0;
}
''',
  r'''#include <cstdio>
#include <vector>
#include <numeric>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    std::vector<int> a(n);
    for (int &x : a) scanf("%d", &x);
    double avg = (double)std::accumulate(a.begin(), a.end(), 0LL) / n;
    int cnt = 0;
    for (int x : a) cnt += (x > avg);
    printf("%.2f\n%d\n", avg, cnt);
    return 0;
}
''',
  ["C++基础", "数组", "平均值"])

A("【一维数组】有序数组去重", SEC_ARR, 2,
  stmt("读入一个**已升序**的数组（可能含重复），输出去重后的元素个数与新数组。",
       ["有序数组的去重是双指针：`i` 扫原数组，`j` 写新数组",
        "`a[j] = a[i]` 只在 `a[i] != a[j]` 时发生，`j` 最后就是新长度",
        "先输出个数，再输出数组"]),
  "第一行 `n`，第二行 `n` 个升序整数。",
  "两行：个数、去重后的数组（空格分隔）。",
  "- 1 ≤ n ≤ 100\n- -100 ≤ x ≤ 100",
  lambda: cases(sorted_arr(51, 8, 1, 5), sorted_arr(52, 1), sorted_arr(53, 12, 0, 3),
                sorted_arr(54, 20, -5, 5), sorted_arr(55, 6, 7, 7), sorted_arr(56, 30, 1, 100)),
  lambda t: (lambda v: "%d\n%s\n" % (len(set(v)), out_row(sorted(set(v))).strip()))(read_ints(t)[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[105];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int j = 0;                            // j 是新数组的写指针
    for (int i = 0; i < n; i++)
        if (i == 0 || a[i] != a[j - 1]) a[j++] = a[i];
    printf("%d\n", j);
    for (int i = 0; i < j; i++) printf(i ? " %d" : "%d", a[i]);
    printf("\n");
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[105], b[105];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int m = 0;
    for (int i = 0; i < n; i++)
        if (m == 0 || b[m - 1] != a[i]) b[m++] = a[i];   // 和上一个写入的比较
    printf("%d\n", m);
    for (int i = 0; i < m; i++) printf(i ? " %d" : "%d", b[i]);
    printf("\n");
    return 0;
}
''',
  ["C++基础", "数组", "双指针", "去重"])

A("【一维数组】把 0 移到末尾", SEC_ARR, 2,
  stmt("读入 `n` 个整数，把其中所有的 0 移到数组末尾，**非零元素的相对顺序不变**。\n\n"
       "输出处理后的数组。",
       ["双指针：`j` 指向下一个该放非零数的位置，扫一遍先把非零数往前挪",
        "剩下的 `j ~ n-1` 全部填 0",
        "不能排序（排序会打乱非零元素的相对顺序）"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行 `n` 个整数。",
  "- 1 ≤ n ≤ 100\n- -100 ≤ x ≤ 100",
  lambda: cases("5\n0 1 0 3 12", arr(61, 8, 0, 3), arr(62, 1, 0, 0),
                arr(63, 15, 0, 5), "4\n0 0 0 0", arr(64, 20, -3, 3)),
  lambda t: out_row([x for x in read_ints(t)[1:] if x != 0] +
                    [0] * sum(1 for x in read_ints(t)[1:] if x == 0)),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[105];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int j = 0;
    for (int i = 0; i < n; i++)
        if (a[i] != 0) a[j++] = a[i];     // 非零数依次前移
    while (j < n) a[j++] = 0;             // 尾部补零
    for (int i = 0; i < n; i++) printf(i ? " %d" : "%d", a[i]);
    printf("\n");
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[105], b[105];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int m = 0, zeros = 0;
    for (int i = 0; i < n; i++) {
        if (a[i] == 0) zeros++;
        else b[m++] = a[i];               // 先挑非零
    }
    for (int i = 0; i < zeros; i++) b[m++] = 0;
    for (int i = 0; i < n; i++) printf(i ? " %d" : "%d", b[i]);
    printf("\n");
    return 0;
}
''',
  ["C++基础", "数组", "双指针", "移动零"])

A("【一维数组】循环右移 k 位", SEC_ARR, 2,
  stmt("读入 `n` 与 `k`，把长度为 `n` 的数组**循环右移** `k` 位后输出。\n\n"
       "例如 `1 2 3 4 5` 右移 2 位得到 `4 5 1 2 3`。",
       ["`k` 可能大于 `n`，先 `k %= n`",
        "右移 `k` 位 = 新数组第 `i` 位来自原数组第 `(i - k + n) % n` 位",
        "`k = 0` 或 `k` 是 `n` 的倍数时原样输出"]),
  "第一行 `n k`，第二行 `n` 个整数。",
  "一行 `n` 个整数。",
  "- 1 ≤ n ≤ 100\n- 0 ≤ k ≤ 10⁹\n- |x| ≤ 100",
  lambda: cases("5 2\n1 2 3 4 5", "4 0\n1 2 3 4", "3 3\n7 8 9",
                "6 8\n1 2 3 4 5 6", arr_with(71, 10, 3), arr_with(72, 7, 1000000000)),
  lambda t: (lambda d: out_row((lambda n, k, v: [v[(i - k % n + n) % n] for i in range(n)])(
      d[0], d[1], d[2:])))(read_ints(t)),
  r'''#include <cstdio>
int main() {
    int n, k;
    if (scanf("%d %d", &n, &k) != 2) return 0;
    static int a[105], b[105];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    k %= n;                                   // 先取模
    for (int i = 0; i < n; i++) b[(i + k) % n] = a[i];   // 正着搬到新位置
    for (int i = 0; i < n; i++) printf(i ? " %d" : "%d", b[i]);
    printf("\n");
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n, k;
    if (scanf("%d %d", &n, &k) != 2) return 0;
    static int a[105];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    k %= n;
    std::rotate(a, a + n - k, a + n);         // 标准库直接旋转
    for (int i = 0; i < n; i++) printf(i ? " %d" : "%d", a[i]);
    printf("\n");
    return 0;
}
''',
  ["C++基础", "数组", "循环移位"])

A("【一维数组】第二大值", SEC_ARR, 3,
  stmt("读入 `n` 个整数（至少两个**不同**的值），输出**严格第二大**的元素。",
       ["`-1` 或 `0` 当前值初值都是错的，要用最小可能值 `LLONG_MIN`",
        "遇到比最大还大的要先把旧最大降级成第二大；相等则跳过",
        "和最大值相同的元素不算「第二大」"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行一个整数。",
  "- 2 ≤ n ≤ 100\n- |x| ≤ 10⁹\n- 保证至少有两个不同的值",
  lambda: cases("4\n1 2 3 4", "3\n5 5 3", arr(81, 10, -20, 20),
                arr(82, 30, -1000, 1000), "5\n-5 -1 -3 -1 -2", arr(83, 6, 0, 1)),
  lambda t: "%d\n" % sorted(set(read_ints(t)[1:]))[-2],
  r'''#include <cstdio>
#include <climits>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    long long m1 = LLONG_MIN, m2 = LLONG_MIN;
    for (int i = 0; i < n; i++) {
        long long x;
        scanf("%lld", &x);
        if (x > m1)      { m2 = m1; m1 = x; }   // 新最大，旧最大降级
        else if (x < m1 && x > m2) m2 = x;      // 严格小于最大才可能是第二
    }
    printf("%lld\n", m2);
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static long long a[105];
    for (int i = 0; i < n; i++) scanf("%lld", &a[i]);
    std::sort(a, a + n);
    int i = n - 1;
    while (i > 0 && a[i - 1] == a[i]) i--;      // 跳过与最大相等的
    printf("%lld\n", a[i - 1]);
    return 0;
}
''',
  ["C++基础", "数组", "第二大"])

A("【一维数组】查找元素首次位置", SEC_ARR, 1,
  stmt("读入 `n` 个整数和一个目标值 `x`，输出 `x` 第一次出现的下标（从 0 开始）；"
       "若不存在输出 `-1`。",
       ["找到就 `break`，否则会拿到最后一次的位置",
        "用标志变量或直接 `return` 都行",
        "输出单个整数"]),
  "第一行 `n x`，第二行 `n` 个整数。",
  "一行一个整数。",
  "- 1 ≤ n ≤ 100\n- |x| ≤ 10⁹",
  lambda: cases("5 3\n1 2 3 4 3", "5 9\n1 2 3 4 5", "1 7\n7",
                "6 -1\n-1 -1 -1 0 1 2", arr_with(91, 20, 5),
                arr_with(92, 15, -999)),
  lambda t: (lambda v, x: "%d\n" % (v.index(x) if x in v else -1))(
      read_ints(t)[2:], read_ints(t)[1]),
  r'''#include <cstdio>
int main() {
    int n, x;
    if (scanf("%d %d", &n, &x) != 2) return 0;
    static int a[105];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int pos = -1;
    for (int i = 0; i < n; i++)
        if (a[i] == x) { pos = i; break; }   // 首次命中就停
    printf("%d\n", pos);
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n, x;
    if (scanf("%d %d", &n, &x) != 2) return 0;
    static int a[105];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int *p = std::find(a, a + n, x);
    printf("%d\n", p == a + n ? -1 : (int)(p - a));
    return 0;
}
''',
  ["C++基础", "数组", "查找"])

A("【一维数组】计数排序", SEC_ARR, 2,
  stmt("读入 `n` 个 1~100 之间的整数，用**计数排序**（不比较大小）升序输出。",
       ["开一个 `cnt[101]` 桶，读一个加一个",
        "再按值从小到大，每个值输出 `cnt[v]` 次",
        "这是 O(n + 值域) 的排序，值域小的时候最快"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行 `n` 个整数，升序。",
  "- 1 ≤ n ≤ 100\n- 1 ≤ x ≤ 100",
  lambda: cases(arr_pos(101, 8, 1, 10), arr_pos(102, 1), arr_pos(103, 20, 1, 5),
                arr_pos(104, 50, 90, 100), arr_pos(105, 6, 50, 50), arr_pos(106, 100)),
  lambda t: out_row(sorted(read_ints(t)[1:])),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int cnt[101];
    for (int i = 0; i < n; i++) { int x; scanf("%d", &x); cnt[x]++; }
    bool first = true;
    for (int v = 1; v <= 100; v++)
        for (int k = 0; k < cnt[v]; k++) {
            if (!first) printf(" ");
            printf("%d", v);
            first = false;
        }
    printf("\n");
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[105];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    std::sort(a, a + n);                  // 直接比较排序
    for (int i = 0; i < n; i++) printf(i ? " %d" : "%d", a[i]);
    printf("\n");
    return 0;
}
''',
  ["C++基础", "数组", "计数排序"])

A("【一维数组】区间和查询（前缀和）", SEC_ARR, 3,
  stmt("读入长度为 `n` 的数组，再读 `q` 个查询 `l r`（下标从 1 开始，闭区间），"
       "输出每个区间的元素和。",
       ["`pre[i] = pre[i-1] + a[i]`，查询就是 `pre[r] - pre[l-1]`",
        "`pre` 用 `long long`：10⁵ 个 10⁶ 级数累加会超 `int`",
        "别每次查询都循环累加，`q` 大时会超时"]),
  "第一行 `n q`；第二行 `n` 个整数；接下来 `q` 行每行 `l r`。",
  "`q` 行，每行一个整数。",
  "- 1 ≤ n, q ≤ 100\n- 1 ≤ l ≤ r ≤ n\n- |x| ≤ 10⁶",
  lambda: cases("5 3\n1 2 3 4 5\n1 5\n2 4\n3 3",
                "1 1\n7\n1 1",
                "6 4\n-1 2 -3 4 -5 6\n1 3\n2 5\n1 6\n4 4",
                _pfx(4, 20, 10), _pfx(5, 50, 30), _pfx(6, 100, 100)),
  lambda t: _pfx_oracle(t),
  r'''#include <cstdio>
int main() {
    int n, q;
    if (scanf("%d %d", &n, &q) != 2) return 0;
    static long long pre[105];
    for (int i = 1; i <= n; i++) {
        long long x;
        scanf("%lld", &x);
        pre[i] = pre[i - 1] + x;          // 前缀和
    }
    while (q--) {
        int l, r;
        scanf("%d %d", &l, &r);
        printf("%lld\n", pre[r] - pre[l - 1]);
    }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n, q;
    if (scanf("%d %d", &n, &q) != 2) return 0;
    static long long a[105];
    for (int i = 1; i <= n; i++) scanf("%lld", &a[i]);
    while (q--) {
        int l, r;
        scanf("%d %d", &l, &r);
        long long s = 0;                  // 老实累加
        for (int i = l; i <= r; i++) s += a[i];
        printf("%lld\n", s);
    }
    return 0;
}
''',
  ["C++基础", "数组", "前缀和"])

A("【一维数组】每个数的出现次数", SEC_ARR, 2,
  stmt("读入 `n` 个整数，按**数值从小到大**输出「值 : 次数」，每个不同的值一行。",
       ["值域小时用桶 `cnt[值]++` 最省事；值域大就排序后统计连续段",
        "本题值域 -100~100，桶数组开 201 或直接排序",
        "格式是 `值:次数`，冒号两侧没有空格"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "若干行，每行 `值:次数`。",
  "- 1 ≤ n ≤ 100\n- -100 ≤ x ≤ 100",
  lambda: cases(arr(111, 8, -2, 2), arr(112, 1), arr(113, 20, 0, 3),
                arr(114, 50, -5, 5), arr(115, 6, 7, 7), arr(116, 100, -10, 10)),
  lambda t: "".join("%d:%d\n" % (v, n) for v, n in sorted(_count(read_ints(t)[1:]).items())),
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[105];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    std::sort(a, a + n);                       // 排好序，相同的就挨在一起
    for (int i = 0; i < n; ) {
        int j = i;
        while (j < n && a[j] == a[i]) j++;
        printf("%d:%d\n", a[i], j - i);
        i = j;
    }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int cnt[301];                       // 偏移 150，负值也能当下标
    for (int i = 0; i < n; i++) { int x; scanf("%d", &x); cnt[x + 150]++; }
    for (int v = -100; v <= 100; v++)
        if (cnt[v + 150]) printf("%d:%d\n", v, cnt[v + 150]);
    return 0;
}
''',
  ["C++基础", "数组", "计数"])

A("【一维数组】奇数在前偶数在后", SEC_ARR, 2,
  stmt("读入 `n` 个整数，重排成「所有奇数在前、所有偶数在后」，**两组内部的相对顺序都要保持**。\n\n"
       "输出重排后的数组。",
       ["这题不能像快排那样两头交换 —— 交换会打乱相对顺序",
        "正确做法是扫两遍：先挑奇数、再挑偶数",
        "0 是偶数"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行 `n` 个整数。",
  "- 1 ≤ n ≤ 100\n- |x| ≤ 100",
  lambda: cases("5\n1 2 3 4 5", "4\n2 4 6 8", "4\n1 3 5 7",
                arr(121, 20, -10, 10), arr(122, 6, 0, 3), arr(123, 15, 1, 9)),
  lambda t: (lambda v: out_row([x for x in v if x % 2 != 0] + [x for x in v if x % 2 == 0]))(read_ints(t)[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[105], b[105];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int m = 0;
    for (int i = 0; i < n; i++) if (a[i] % 2 != 0) b[m++] = a[i];   // 先奇数
    for (int i = 0; i < n; i++) if (a[i] % 2 == 0) b[m++] = a[i];   // 再偶数
    for (int i = 0; i < n; i++) printf(i ? " %d" : "%d", b[i]);
    printf("\n");
    return 0;
}
''',
  r'''#include <cstdio>
#include <vector>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    std::vector<int> odd, even;
    for (int i = 0; i < n; i++) {
        int x; scanf("%d", &x);
        ((x % 2) ? odd : even).push_back(x);   // 分两堆
    }
    odd.insert(odd.end(), even.begin(), even.end());   // 接起来
    for (int i = 0; i < (int)odd.size(); i++) printf(i ? " %d" : "%d", odd[i]);
    printf("\n");
    return 0;
}
''',
  ["C++基础", "数组", "稳定划分"])

A("【一维数组】删除所有指定元素", SEC_ARR, 2,
  stmt("读入 `n` 个整数和目标值 `x`，删除数组中所有等于 `x` 的元素，输出新长度和新数组。\n\n"
       "若新数组为空，第二行输出空行（只留换行）。",
       ["和去重一样用写指针 `j`：`a[i] != x` 才写入",
        "新长度就是 `j`，不要先算「删了几个」再减",
        "全部删光时第二行是空行，不是 `none`"]),
  "第一行 `n x`，第二行 `n` 个整数。",
  "两行：新长度、新数组。",
  "- 1 ≤ n ≤ 100\n- |x|, |aᵢ| ≤ 100",
  lambda: cases("5 3\n1 3 5 3 7", "4 9\n1 2 3 4", "4 1\n1 1 1 1",
                arr_with(131, 20, 2, 0, 5), arr_with(132, 8, 2, 1, 9),
                arr_with(133, 30, 2, -3, 3)),
  lambda t: (lambda v, x: "%d\n%s\n" % (len([y for y in v if y != x]),
                                        " ".join(str(y) for y in v if y != x)))(
      read_ints(t)[2:], read_ints(t)[1]),
  r'''#include <cstdio>
int main() {
    int n, x;
    if (scanf("%d %d", &n, &x) != 2) return 0;
    static int a[105];
    int j = 0;
    for (int i = 0; i < n; i++) {
        int v;
        scanf("%d", &v);
        if (v != x) a[j++] = v;          // 不等于目标才留下
    }
    printf("%d\n", j);
    for (int i = 0; i < j; i++) printf(i ? " %d" : "%d", a[i]);
    printf("\n");
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n, x;
    if (scanf("%d %d", &n, &x) != 2) return 0;
    static int a[105], b[105];
    int m = 0;
    for (int i = 0; i < n; i++) {
        scanf("%d", &a[i]);
        if (a[i] != x) b[m++] = a[i];
    }
    printf("%d\n", m);
    for (int i = 0; i < m; i++) printf(i ? " %d" : "%d", b[i]);
    printf("\n");
    return 0;
}
''',
  ["C++基础", "数组", "删除元素"])

A("【一维数组】合并两个有序数组", SEC_ARR, 3,
  stmt("读入两个**非降序**数组，合并成一个仍非降序的数组并输出。",
       ["双指针归并：每次取两边较小的那个，取完就后移",
        "一个数组走完后，把另一个剩下的整体接上",
        "不要用 `sort` 合并后再排 —— 那浪费了「已有序」这个条件"]),
  "第一行 `n m`；第二行 `n` 个整数；第三行 `m` 个整数。",
  "一行 `n+m` 个整数。",
  "- 1 ≤ n, m ≤ 50\n- |x| ≤ 100",
  lambda: cases("3 3\n1 3 5\n2 4 6", "1 1\n1\n2", "2 3\n1 2\n3 4 5",
                merg(141, 5, 7), merg(142, 10, 10), merg(143, 1, 20)),
  lambda t: _merge_oracle(t),
  r'''#include <cstdio>
int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    static int a[55], b[55];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    for (int i = 0; i < m; i++) scanf("%d", &b[i]);
    int i = 0, j = 0;
    bool first = true;
    while (i < n || j < m) {
        int v;
        if (j >= m || (i < n && a[i] <= b[j])) v = a[i++];   // 取较小者
        else v = b[j++];
        printf(first ? "%d" : " %d", v);
        first = false;
    }
    printf("\n");
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    static int a[110];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    for (int i = 0; i < m; i++) scanf("%d", &a[n + i]);
    std::sort(a, a + n + m);                 // 全部丢进去再排
    for (int i = 0; i < n + m; i++) printf(i ? " %d" : "%d", a[i]);
    printf("\n");
    return 0;
}
''',
  ["C++基础", "数组", "归并"])

A("【一维数组】判断严格递增", SEC_ARR, 1,
  stmt("读入 `n` 个整数，判断是否**严格递增**（每个元素都严格大于前一个），"
       "是输出 `YES`，否输出 `NO`。",
       ["从 `i = 1` 开始比 `a[i] <= a[i-1]` 就失败",
        "`n = 1` 时算严格递增（没有反例）",
        "相等也不算递增 —— 「严格」二字是关键"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行 `YES` 或 `NO`。",
  "- 1 ≤ n ≤ 100\n- |x| ≤ 100",
  lambda: cases("5\n1 2 3 4 5", "5\n1 2 2 4 5", "1\n7",
                arr(151, 10, 0, 100), sorted_arr(152, 10, 1, 20), "4\n4 3 2 1"),
  lambda t: (lambda v: "YES\n" if all(v[i] > v[i - 1] for i in range(1, len(v))) else "NO\n")(read_ints(t)[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[105];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    bool ok = true;
    for (int i = 1; i < n; i++)
        if (a[i] <= a[i - 1]) { ok = false; break; }
    printf("%s\n", ok ? "YES" : "NO");
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[105];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    bool ok = std::adjacent_find(a, a + n, [](int x, int y) { return y <= x; }) == a + n;
    printf("%s\n", ok ? "YES" : "NO");
    return 0;
}
''',
  ["C++基础", "数组", "递增"])

A("【一维数组】最长连续递增段", SEC_ARR, 2,
  stmt("读入 `n` 个整数，输出**最长的严格连续递增子段**的长度。",
       ["一遍扫描：`a[i] > a[i-1]` 就让当前长度加一，否则重置为 1",
        "每次更新答案，别忘了单独元素长度是 1",
        "注意是「连续」而不是「子序列」"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行一个整数。",
  "- 1 ≤ n ≤ 100\n- |x| ≤ 100",
  lambda: cases("8\n1 2 3 2 3 4 5 1", "5\n5 4 3 2 1", "1\n9",
                "6\n1 2 2 3 4 5", arr(161, 20, 0, 10), arr(162, 15, -5, 5)),
  lambda t: "%d\n" % _lis_run(read_ints(t)[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[105];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int best = 1, cur = 1;
    for (int i = 1; i < n; i++) {
        if (a[i] > a[i - 1]) cur++;
        else cur = 1;                     // 断了就从 1 重新数
        if (cur > best) best = cur;
    }
    printf("%d\n", best);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[105];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int best = 1;
    for (int i = 0; i < n; i++) {         // 枚举每一段起点
        int j = i;
        while (j + 1 < n && a[j + 1] > a[j]) j++;
        if (j - i + 1 > best) best = j - i + 1;
        i = j;                            // 跳过这一段
    }
    printf("%d\n", best);
    return 0;
}
''',
  ["C++基础", "数组", "连续段"])

A("【一维数组】最大子段和", SEC_ARR, 4,
  stmt("读入 `n` 个整数（可能全为负），求**非空连续子段**的最大和。",
       ["`Kadane`：`cur = max(a[i], cur + a[i])`，`ans = max(ans, cur)`",
        "初值不能写 0 —— 全负数时答案应该是最大的那个负数",
        "O(n²) 暴力也能过本题（n ≤ 100），但要理解 O(n) 的做法"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行一个整数。",
  "- 1 ≤ n ≤ 100\n- |x| ≤ 1000",
  lambda: cases("8\n-2 1 -3 4 -1 2 1 -5", "3\n-5 -2 -9", "1\n-7",
                arr(171, 20, -10, 10), arr(172, 30, -100, 100), "5\n1 2 3 4 5"),
  lambda t: "%d\n" % _max_sub(read_ints(t)[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[105];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    long long cur = a[0], best = a[0];
    for (int i = 1; i < n; i++) {
        cur = (cur > 0 ? cur + a[i] : a[i]);   // 前缀为负就丢掉
        if (cur > best) best = cur;
    }
    printf("%lld\n", best);
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[105];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    long long best = a[0];
    for (int i = 0; i < n; i++) {              // O(n²) 暴力枚举
        long long s = 0;
        for (int j = i; j < n; j++) {
            s += a[j];
            best = std::max(best, s);
        }
    }
    printf("%lld\n", best);
    return 0;
}
''',
  ["C++基础", "数组", "最大子段和", "Kadane"])

A("【一维数组】数组升序排序", SEC_ARR, 2,
  stmt("读入 `n` 个整数，用**冒泡排序**升序排序后输出。\n\n"
       "（要求真的写两层循环交换，不要用 `sort` —— 这道题考的是排序过程本身。）",
       ["外层跑 `n-1` 轮，内层比较相邻两个、逆序就交换",
        "加一个 `swapped` 标志，某一轮没换过就说明已经有序，可以提前结束",
        "输出一行，空格分隔"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行 `n` 个整数，升序。",
  "- 1 ≤ n ≤ 100\n- |x| ≤ 1000",
  lambda: cases(arr(181, 8), arr(182, 1), arr(183, 20), "10\n10 9 8 7 6 5 4 3 2 1",
                arr(184, 50, -100, 100), arr(185, 6, 3, 3)),
  lambda t: out_row(sorted(read_ints(t)[1:])),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[105];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    for (int i = 0; i < n - 1; i++) {
        bool swapped = false;
        for (int j = 0; j < n - 1 - i; j++)
            if (a[j] > a[j + 1]) {              // 逆序就换
                int t = a[j]; a[j] = a[j + 1]; a[j + 1] = t;
                swapped = true;
            }
        if (!swapped) break;                    // 已有序，提前收工
    }
    for (int i = 0; i < n; i++) printf(i ? " %d" : "%d", a[i]);
    printf("\n");
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[105];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    for (int i = 0; i < n - 1; i++) {           // 选择排序：每轮找最小放前面
        int k = i;
        for (int j = i + 1; j < n; j++) if (a[j] < a[k]) k = j;
        if (k != i) { int t = a[i]; a[i] = a[k]; a[k] = t; }
    }
    for (int i = 0; i < n; i++) printf(i ? " %d" : "%d", a[i]);
    printf("\n");
    return 0;
}
''',
  ["C++基础", "数组", "冒泡排序"])

A("【一维数组】有序数组插入", SEC_ARR, 2,
  stmt("读入一个**升序**数组和一个整数 `x`，把 `x` 插入到正确位置后输出新数组。",
       ["从后往前找位置，一边找一边把元素后移，最后填 `x`",
        "`x` 比所有元素都大时插到末尾，比所有都小时插到开头",
        "长度变成 `n + 1`，数组容量要留够"]),
  "第一行 `n x`，第二行 `n` 个升序整数。",
  "一行 `n+1` 个整数，升序。",
  "- 1 ≤ n ≤ 100\n- |x| ≤ 1000",
  lambda: cases("5 3\n1 2 4 5 6", "3 0\n1 2 3", "3 9\n1 2 3",
                "1 5\n5", sorted_with(191, 20, 25, 1, 50),
                sorted_with(192, 10, -20, -10, 10)),
  lambda t: (lambda v, x: out_row(sorted(v + [x])))(read_ints(t)[2:], read_ints(t)[1]),
  r'''#include <cstdio>
int main() {
    int n, x;
    if (scanf("%d %d", &n, &x) != 2) return 0;
    static int a[110];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int i = n - 1;
    while (i >= 0 && a[i] > x) { a[i + 1] = a[i]; i--; }  // 比 x 大的后移
    a[i + 1] = x;                                          // 空位填 x
    for (int k = 0; k <= n; k++) printf(k ? " %d" : "%d", a[k]);
    printf("\n");
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n, x;
    if (scanf("%d %d", &n, &x) != 2) return 0;
    static int a[110], b[110];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int pos = 0;
    while (pos < n && a[pos] <= x) pos++;      // 找到第一个比 x 大的位置
    for (int i = 0; i < pos; i++) b[i] = a[i];
    b[pos] = x;
    for (int i = pos; i < n; i++) b[i + 1] = a[i];
    for (int i = 0; i <= n; i++) printf(i ? " %d" : "%d", b[i]);
    printf("\n");
    return 0;
}
''',
  ["C++基础", "数组", "插入"])

A("【一维数组】删除首次出现的元素", SEC_ARR, 2,
  stmt("读入 `n` 个整数和 `x`，删除 `x` **第一次出现**的那个元素（后面的元素前移），"
       "输出新长度和新数组。\n\n若 `x` 不存在，输出 `not found`（只一行）。",
       ["先找位置，找到了再整体前移一位",
        "只删第一个，不要用「删除所有」的写法",
        "找不到时**不要**输出数组，只输出 `not found`"]),
  "第一行 `n x`，第二行 `n` 个整数。",
  "找到时两行（新长度、新数组）；否则一行 `not found`。",
  "- 1 ≤ n ≤ 100\n- |x|, |aᵢ| ≤ 100",
  lambda: cases("5 3\n1 3 5 3 7", "4 9\n1 2 3 4", "3 1\n1 1 1",
                "2 5\n5 6", arr_with(201, 20, 2, 0, 5), arr_with(202, 8, 99, 1, 9)),
  lambda t: _del_first(read_ints(t)[1], read_ints(t)[2:]),
  r'''#include <cstdio>
int main() {
    int n, x;
    if (scanf("%d %d", &n, &x) != 2) return 0;
    static int a[105];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int pos = -1;
    for (int i = 0; i < n; i++) if (a[i] == x) { pos = i; break; }
    if (pos < 0) { printf("not found\n"); return 0; }
    for (int i = pos; i < n - 1; i++) a[i] = a[i + 1];   // 后面整体前移
    printf("%d\n", n - 1);
    for (int i = 0; i < n - 1; i++) printf(i ? " %d" : "%d", a[i]);
    printf("\n");
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n, x;
    if (scanf("%d %d", &n, &x) != 2) return 0;
    static int a[105], b[105];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int m = 0;
    bool removed = false;
    for (int i = 0; i < n; i++) {
        if (!removed && a[i] == x) { removed = true; continue; }  // 只跳过一个
        b[m++] = a[i];
    }
    if (!removed) { printf("not found\n"); return 0; }
    printf("%d\n", m);
    for (int i = 0; i < m; i++) printf(i ? " %d" : "%d", b[i]);
    printf("\n");
    return 0;
}
''',
  ["C++基础", "数组", "删除"])

A("【一维数组】众数（并列取最小值）", SEC_ARR, 3,
  stmt("读入 `n` 个整数，输出出现次数**最多**的数；若并列，输出其中**值最小**的。",
       ["先排序再扫连续段，或者用桶统计",
        "更新条件写 `cnt > best_cnt`（严格大于），并列时就保留先遇到的（排好序后就是最小的）",
        "并列取最小，用桶从值小到大扫最自然"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行一个整数。",
  "- 1 ≤ n ≤ 100\n- -100 ≤ x ≤ 100",
  lambda: cases("6\n1 2 2 3 3 3", "5\n1 2 2 1 3", "1\n7",
                arr(211, 20, -3, 3), arr(212, 30, -10, 10), "4\n9 9 1 1"),
  lambda t: "%d\n" % _mode(read_ints(t)[1:]),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int cnt[301];
    for (int i = 0; i < n; i++) { int x; scanf("%d", &x); cnt[x + 150]++; }
    int best = -100, bc = -1;
    for (int v = -100; v <= 100; v++)        // 从小到大扫
        if (cnt[v + 150] > bc) { bc = cnt[v + 150]; best = v; }  // 严格大于
    printf("%d\n", best);
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[105];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    std::sort(a, a + n);
    int best = a[0], bc = 0;
    for (int i = 0; i < n; ) {
        int j = i;
        while (j < n && a[j] == a[i]) j++;
        if (j - i > bc) { bc = j - i; best = a[i]; }   // 并列不换 → 保留小值
        i = j;
    }
    printf("%d\n", best);
    return 0;
}
''',
  ["C++基础", "数组", "众数"])

A("【一维数组】按绝对值排序", SEC_ARR, 3,
  stmt("读入 `n` 个整数，按**绝对值升序**排序；绝对值相同时按**原值升序**。输出排序结果。",
       ["比较函数写成 `fabs(x) < fabs(y)`，并列时再比 `x < y`",
        "`sort` 的比较器必须是**严格弱序**，不能写 `<=`",
        "自己写排序时，比较条件同样要两段"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行 `n` 个整数。",
  "- 1 ≤ n ≤ 100\n- -1000 ≤ x ≤ 1000",
  lambda: cases("5\n-3 1 -2 4 -1", "4\n5 -5 3 -3", "1\n-7",
                arr(221, 20, -10, 10), arr(222, 30, -100, 100), "6\n0 -1 1 -2 2 0"),
  lambda t: out_row(sorted(read_ints(t)[1:], key=lambda x: (abs(x), x))),
  r'''#include <cstdio>
#include <algorithm>
#include <cstdlib>
bool cmp(int x, int y) {
    if (abs(x) != abs(y)) return abs(x) < abs(y);   // 先比绝对值
    return x < y;                                   // 再比原值
}
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[105];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    std::sort(a, a + n, cmp);
    for (int i = 0; i < n; i++) printf(i ? " %d" : "%d", a[i]);
    printf("\n");
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[105];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    for (int i = 0; i < n - 1; i++)             // 手写选择排序
        for (int j = i + 1; j < n; j++) {
            int ax = a[i] < 0 ? -a[i] : a[i];
            int ay = a[j] < 0 ? -a[j] : a[j];
            if (ay < ax || (ay == ax && a[j] < a[i])) {
                int t = a[i]; a[i] = a[j]; a[j] = t;
            }
        }
    for (int i = 0; i < n; i++) printf(i ? " %d" : "%d", a[i]);
    printf("\n");
    return 0;
}
''',
  ["C++基础", "数组", "绝对值", "比较器"])

A("【一维数组】有序数组两数之和", SEC_ARR, 4,
  stmt("读入一个**升序**数组和目标 `target`，找出两个不同位置的元素使其和等于 `target`，"
       "输出它们的下标（**从 1 开始，小的在前**）。\n\n"
       "数据保证恰好有一组解。",
       ["双指针：`l = 0, r = n-1`，和大了 `r--`，和小了 `l++`",
        "不能用两层循环，那样 O(n²) 在 n 大时慢（本题 n ≤ 100 也能过，但要会双指针）",
        "下标是 1-based，输出时记得 +1"]),
  "第一行 `n target`，第二行 `n` 个升序整数。",
  "一行两个整数。",
  "- 2 ≤ n ≤ 100\n- |x|, |target| ≤ 10⁵\n- 保证唯一解",
  lambda: cases("4 9\n2 7 11 15", "3 6\n1 2 4", "2 0\n-1 1",
                "5 8\n1 2 3 4 5", "6 13\n1 3 5 7 8 9", "4 -3\n-5 -2 -1 2"),
  lambda t: _two_sum_oracle(t),
  r'''#include <cstdio>
int main() {
    int n, target;
    if (scanf("%d %d", &n, &target) != 2) return 0;
    static int a[105];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int l = 0, r = n - 1;
    while (l < r) {
        long long s = (long long)a[l] + a[r];
        if (s == target) { printf("%d %d\n", l + 1, r + 1); return 0; }  // 1-based
        if (s < target) l++;             // 和太小，左指针右移
        else r--;                        // 和太大，右指针左移
    }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n, target;
    if (scanf("%d %d", &n, &target) != 2) return 0;
    static int a[105];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    for (int i = 0; i < n; i++)                 // 暴力两两枚举
        for (int j = i + 1; j < n; j++)
            if ((long long)a[i] + a[j] == target) {
                printf("%d %d\n", i + 1, j + 1);
                return 0;
            }
    return 0;
}
''',
  ["C++基础", "数组", "双指针"])


# ===================================================================== #
#  SEC_MAT · 二维数组与矩阵（14 题）
# ===================================================================== #

A("【矩阵】转置", SEC_MAT, 1,
  stmt("读入一个 `n×n` 矩阵，输出它的转置（行列互换）。",
       ["转置就是 `b[j][i] = a[i][j]`",
        "按行输出，每行 `n` 个数，空格分隔",
        "方阵转置可以原地做（交换 `a[i][j]` 与 `a[j][i]`，只遍历上三角）"]),
  "第一行 `n`，接下来 `n` 行每行 `n` 个整数。",
  "`n` 行，每行 `n` 个整数。",
  "- 1 ≤ n ≤ 20\n- |x| ≤ 100",
  lambda: cases(mat(301, 3), mat(302, 1), mat(303, 4), mat(304, 5), mat(305, 2), mat(306, 6)),
  lambda t: (lambda n, a: "".join(out_row([a[i][j] for i in range(n)]) for j in range(n)))(*read_mat(t)),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[25][25];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) scanf("%d", &a[i][j]);
    for (int j = 0; j < n; j++) {           // 外层是列
        for (int i = 0; i < n; i++) printf(i ? " %d" : "%d", a[i][j]);
        printf("\n");
    }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[25][25];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) scanf("%d", &a[i][j]);
    for (int i = 0; i < n; i++)             // 原地交换上三角
        for (int j = i + 1; j < n; j++) {
            int t = a[i][j]; a[i][j] = a[j][i]; a[j][i] = t;
        }
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) printf(j ? " %d" : "%d", a[i][j]);
        printf("\n");
    }
    return 0;
}
''',
  ["C++基础", "二维数组", "转置"])

A("【矩阵】每行元素之和", SEC_MAT, 1,
  stmt("读入 `n×n` 矩阵，输出每一行元素之和，每行一个结果。",
       ["固定行、遍历列：`for (j) s += a[i][j]`",
        "`n` 行，每行一个整数",
        "别把内外层循环写反（那样就是列和）"]),
  "第一行 `n`，接下来 `n` 行。",
  "`n` 行，每行一个整数。",
  "- 1 ≤ n ≤ 20\n- |x| ≤ 100",
  lambda: cases(mat(311, 3), mat(312, 1), mat(313, 4), mat(314, 5), mat(315, 2), mat(316, 6)),
  lambda t: (lambda n, a: "".join("%d\n" % sum(r) for r in a))(*read_mat(t)),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[25][25];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) scanf("%d", &a[i][j]);
    for (int i = 0; i < n; i++) {
        long long s = 0;
        for (int j = 0; j < n; j++) s += a[i][j];
        printf("%lld\n", s);
    }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 0; i < n; i++) {           // 不存矩阵，边读边加
        long long s = 0;
        for (int j = 0; j < n; j++) { int x; scanf("%d", &x); s += x; }
        printf("%lld\n", s);
    }
    return 0;
}
''',
  ["C++基础", "二维数组", "行和"])

A("【矩阵】每列元素之和", SEC_MAT, 2,
  stmt("读入 `n×n` 矩阵，输出每一列元素之和，**一行内**用空格分隔。",
       ["外层是列、内层是行：`for (j) { s += a[i][j] }`",
        "必须先把矩阵全部读进来，不能边读边算（除非按列重排输入）",
        "输出一行 `n` 个数"]),
  "第一行 `n`，接下来 `n` 行。",
  "一行 `n` 个整数。",
  "- 1 ≤ n ≤ 20\n- |x| ≤ 100",
  lambda: cases(mat(321, 3), mat(322, 1), mat(323, 4), mat(324, 5), mat(325, 2), mat(326, 6)),
  lambda t: (lambda n, a: out_row([sum(a[i][j] for i in range(n)) for j in range(n)]))(*read_mat(t)),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[25][25];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) scanf("%d", &a[i][j]);
    for (int j = 0; j < n; j++) {
        long long s = 0;
        for (int i = 0; i < n; i++) s += a[i][j];    // 固定列，累加各行
        printf(j ? " %lld" : "%lld", s);
    }
    printf("\n");
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static long long col[25] = {0};
    for (int i = 0; i < n; i++)             // 边读边累加到列上
        for (int j = 0; j < n; j++) {
            int x; scanf("%d", &x);
            col[j] += x;
        }
    for (int j = 0; j < n; j++) printf(j ? " %lld" : "%lld", col[j]);
    printf("\n");
    return 0;
}
''',
  ["C++基础", "二维数组", "列和"])

A("【矩阵】主对角线元素之和", SEC_MAT, 1,
  stmt("读入 `n×n` 矩阵，输出**主对角线**（左上到右下）元素之和。",
       ["主对角线满足 `i == j`",
        "`n = 1` 时就是那个唯一元素",
        "只需一次循环 `for (i) s += a[i][i]`"]),
  "第一行 `n`，接下来 `n` 行。",
  "一行一个整数。",
  "- 1 ≤ n ≤ 20\n- |x| ≤ 100",
  lambda: cases(mat(331, 3), mat(332, 1), mat(333, 4), mat(334, 5), mat(335, 2), mat(336, 6)),
  lambda t: (lambda n, a: "%d\n" % sum(a[i][i] for i in range(n)))(*read_mat(t)),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[25][25];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) scanf("%d", &a[i][j]);
    long long s = 0;
    for (int i = 0; i < n; i++) s += a[i][i];   // i == j
    printf("%lld\n", s);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    long long s = 0;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) {
            int x; scanf("%d", &x);
            if (i == j) s += x;                 // 读的时候顺手挑
        }
    printf("%lld\n", s);
    return 0;
}
''',
  ["C++基础", "二维数组", "对角线"])

A("【矩阵】副对角线元素之和", SEC_MAT, 2,
  stmt("读入 `n×n` 矩阵，输出**副对角线**（右上到左下）元素之和。",
       ["副对角线满足 `i + j == n - 1`，即 `j = n-1-i`",
        "别和主对角线搞混 —— 这是最常见的错",
        "奇数阶时中心元素只属于主对角线，副对角线不含它"]),
  "第一行 `n`，接下来 `n` 行。",
  "一行一个整数。",
  "- 1 ≤ n ≤ 20\n- |x| ≤ 100",
  lambda: cases(mat(341, 3), mat(342, 1), mat(343, 4), mat(344, 5), mat(345, 2), mat(346, 6)),
  lambda t: (lambda n, a: "%d\n" % sum(a[i][n - 1 - i] for i in range(n)))(*read_mat(t)),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[25][25];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) scanf("%d", &a[i][j]);
    long long s = 0;
    for (int i = 0; i < n; i++) s += a[i][n - 1 - i];   // i + j == n-1
    printf("%lld\n", s);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[25][25];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) scanf("%d", &a[i][j]);
    long long s = 0;
    for (int i = 0, j = n - 1; i < n; i++, j--) s += a[i][j];   // 双指针式
    printf("%lld\n", s);
    return 0;
}
''',
  ["C++基础", "二维数组", "副对角线"])

A("【矩阵】最大值及其位置", SEC_MAT, 2,
  stmt("读入 `n×n` 矩阵，输出最大值以及它第一次出现的行、列号（**从 1 开始**）。\n\n"
       "按行优先顺序，取第一个最大值。",
       ["按行扫描，`>` 严格大于才更新，保证取到第一个",
        "行号列号输出时要 +1（题目要求 1-based）",
        "初值用 `a[0][0]`，不要用 0"]),
  "第一行 `n`，接下来 `n` 行。",
  "一行三个整数 `max row col`。",
  "- 1 ≤ n ≤ 20\n- |x| ≤ 1000",
  lambda: cases(mat(351, 3), mat(352, 1), mat(353, 4), mat(354, 5), mat(355, 2), mat(356, 6)),
  lambda t: _mat_max(*read_mat(t)),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[25][25];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) scanf("%d", &a[i][j]);
    int bi = 0, bj = 0;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            if (a[i][j] > a[bi][bj]) { bi = i; bj = j; }   // 严格大于
    printf("%d %d %d\n", a[bi][bj], bi + 1, bj + 1);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[25][25];
    int best = 0, bi = 0, bj = 0, first = 1;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) {
            scanf("%d", &a[i][j]);
            if (first) { best = a[i][j]; first = 0; }
            else if (a[i][j] > best) { best = a[i][j]; bi = i; bj = j; }
        }
    printf("%d %d %d\n", best, bi + 1, bj + 1);
    return 0;
}
''',
  ["C++基础", "二维数组", "最大值"])

A("【矩阵】矩阵加法", SEC_MAT, 1,
  stmt("读入两个 `n×n` 矩阵，输出它们的和矩阵（对应位置相加）。",
       ["先读第一个，再读第二个，边读边加",
        "输出 `n` 行，每行 `n` 个数",
        "输入顺序：`n`、矩阵 A 的 `n` 行、矩阵 B 的 `n` 行"]),
  "第一行 `n`；接下来 `n` 行是 A；再 `n` 行是 B。",
  "`n` 行，每行 `n` 个整数。",
  "- 1 ≤ n ≤ 20\n- |x| ≤ 100",
  lambda: cases(_mat2(361, 3), _mat2(362, 4), _mat2(363, 1),
                _mat2(364, 5), _mat2(365, 2), _mat2(366, 6)),
  lambda t: _mat_add_oracle(t),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[25][25], b[25][25];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) scanf("%d", &a[i][j]);
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) scanf("%d", &b[i][j]);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) printf(j ? " %d" : "%d", a[i][j] + b[i][j]);
        printf("\n");
    }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[25][25];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) scanf("%d", &a[i][j]);
    for (int i = 0; i < n; i++)             // 读到 B 就直接加到 A 上
        for (int j = 0; j < n; j++) {
            int x; scanf("%d", &x);
            a[i][j] += x;
        }
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) printf(j ? " %d" : "%d", a[i][j]);
        printf("\n");
    }
    return 0;
}
''',
  ["C++基础", "二维数组", "矩阵加法"])

A("【矩阵】矩阵乘法", SEC_MAT, 4,
  stmt("读入两个 `n×n` 矩阵 A、B，输出 `C = A × B`。\n\n"
       "`C[i][j] = Σ A[i][k] * B[k][j]`（k 从 0 到 n-1）。",
       ["三重循环：`i`、`j`、`k`，最内层累加",
        "累加变量用 `long long`：100×100×100 会超 `int`",
        "别把 `B[k][j]` 写成 `B[j][k]` —— 那算的是 `A × Bᵀ`"]),
  "第一行 `n`；接下来 `n` 行是 A；再 `n` 行是 B。",
  "`n` 行，每行 `n` 个整数。",
  "- 1 ≤ n ≤ 20\n- |x| ≤ 100",
  lambda: cases(_mat2(371, 3), _mat2(372, 1), _mat2(373, 4), _mat2(374, 5),
                _mat2(375, 2), _mat2(376, 6)),
  lambda t: _mat_mul_oracle(t),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[25][25], b[25][25];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) scanf("%d", &a[i][j]);
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) scanf("%d", &b[i][j]);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            long long s = 0;
            for (int k = 0; k < n; k++) s += (long long)a[i][k] * b[k][j];
            printf(j ? " %lld" : "%lld", s);
        }
        printf("\n");
    }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[25][25], b[25][25];
    static long long c[25][25];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) scanf("%d", &a[i][j]);
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) scanf("%d", &b[i][j]);
    for (int i = 0; i < n; i++)             // 以 i,k 为外层，写入整行
        for (int k = 0; k < n; k++) {
            long long aik = a[i][k];
            for (int j = 0; j < n; j++) c[i][j] += aik * b[k][j];
        }
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) printf(j ? " %lld" : "%lld", c[i][j]);
        printf("\n");
    }
    return 0;
}
''',
  ["C++基础", "二维数组", "矩阵乘法"])

A("【矩阵】鞍点查找", SEC_MAT, 4,
  stmt("读入 `n×n` 矩阵，找一个**鞍点**：它在所在行里最大、同时在所在列里最小。\n\n"
       "输出它的行、列（从 1 开始）和值；若有多个取**行优先第一个**；没有则输出 `No`。",
       ["先扫一行找出最大值所在的列，再验这一列里它是不是最小",
        "一行可能有多个相同的最大值，要逐个当候选验（本题数据保证不重复，简化成取第一个）",
        "判断列最小要用严格小于比较"]),
  "第一行 `n`，接下来 `n` 行。",
  "一行 `row col value` 或 `No`。",
  "- 1 ≤ n ≤ 20\n- |x| ≤ 1000\n- 保证同行最大值不重复",
  lambda: cases(_saddle_cases(381, 3, True), _saddle_cases(382, 1, True),
                _saddle_cases(383, 4, False), _saddle_cases(384, 5, False),
                _saddle_cases(385, 2, True), _saddle_cases(386, 6, False)),
  lambda t: _saddle_oracle(t),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[25][25];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) scanf("%d", &a[i][j]);
    for (int i = 0; i < n; i++) {
        int bc = 0;
        for (int j = 1; j < n; j++) if (a[i][j] > a[i][bc]) bc = j;   // 行最大
        bool ok = true;
        for (int k = 0; k < n; k++) if (a[k][bc] < a[i][bc]) { ok = false; break; }
        if (ok) { printf("%d %d %d\n", i + 1, bc + 1, a[i][bc]); return 0; }
    }
    printf("No\n");
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[25][25];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) scanf("%d", &a[i][j]);
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) {
            bool rowMax = true, colMin = true;
            for (int k = 0; k < n; k++) {
                if (a[i][k] > a[i][j]) rowMax = false;
                if (a[k][j] < a[i][j]) colMin = false;
            }
            if (rowMax && colMin) {
                printf("%d %d %d\n", i + 1, j + 1, a[i][j]);
                return 0;
            }
        }
    printf("No\n");
    return 0;
}
''',
  ["C++基础", "二维数组", "鞍点"])

A("【矩阵】上三角判断", SEC_MAT, 2,
  stmt("读入 `n×n` 矩阵，判断它是否为**上三角矩阵**：主对角线**下方**（`i > j`）的元素全为 0。\n\n"
       "是输出 `YES`，否输出 `NO`。",
       ["只需检查 `i > j` 的位置，对角线和上三角随便是什么",
        "找到第一个非零就可以直接判否",
        "`n = 1` 一定是上三角"]),
  "第一行 `n`，接下来 `n` 行。",
  "一行 `YES` 或 `NO`。",
  "- 1 ≤ n ≤ 20\n- |x| ≤ 100",
  lambda: cases(_upper_cases(391, 3, True), _upper_cases(392, 1, True),
                _upper_cases(393, 4, False), _upper_cases(394, 5, True),
                _upper_cases(395, 2, False), _upper_cases(396, 6, True)),
  lambda t: _upper_oracle(t),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[25][25];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) scanf("%d", &a[i][j]);
    bool ok = true;
    for (int i = 0; i < n && ok; i++)
        for (int j = 0; j < i; j++)          // 只看主对角线下方
            if (a[i][j] != 0) { ok = false; break; }
    printf("%s\n", ok ? "YES" : "NO");
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int bad = 0;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) {
            int x; scanf("%d", &x);
            if (i > j && x != 0) bad++;      // 边读边判
        }
    printf("%s\n", bad == 0 ? "YES" : "NO");
    return 0;
}
''',
  ["C++基础", "二维数组", "上三角"])

A("【矩阵】螺旋矩阵", SEC_MAT, 4,
  stmt("读入 `n`，输出 `n×n` 的螺旋矩阵：从左上角开始填 1，按**顺时针**方向由外向内绕圈。\n\n"
       "例如 `n = 3`：\n\n```\n1 2 3\n8 9 4\n7 6 5\n```",
       ["用四个边界 `top/bottom/left/right`，每走完一条边就收缩",
        "顺序是：上行左→右、右列上→下、下行右→左、左列下→上",
        "收缩后要重新判 `top <= bottom && left <= right`，否则内层会重复填"]),
  "一行一个整数 `n`。",
  "`n` 行，每行 `n` 个整数。",
  "- 1 ≤ n ≤ 20",
  lambda: cases("1", "2", "3", "4", "5", "6"),
  lambda t: _spiral(int(t)),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[25][25];
    int v = 1, top = 0, bot = n - 1, left = 0, right = n - 1;
    while (top <= bot && left <= right) {
        for (int j = left; j <= right; j++) a[top][j] = v++;      // 上边
        top++;
        for (int i = top; i <= bot; i++) a[i][right] = v++;       // 右边
        right--;
        if (top <= bot) for (int j = right; j >= left; j--) a[bot][j] = v++;   // 下边
        bot--;
        if (left <= right) for (int i = bot; i >= top; i--) a[i][left] = v++;  // 左边
        left++;
    }
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) printf(j ? " %d" : "%d", a[i][j]);
        printf("\n");
    }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[25][25];
    int dr[4] = {0, 1, 0, -1}, dc[4] = {1, 0, -1, 0};   // 右下左上
    int r = 0, c = 0, d = 0;
    for (int v = 1; v <= n * n; v++) {
        a[r][c] = v;
        int nr = r + dr[d], nc = c + dc[d];
        if (nr < 0 || nr >= n || nc < 0 || nc >= n || a[nr][nc]) {
            d = (d + 1) % 4;                 // 撞墙就右转
            nr = r + dr[d]; nc = c + dc[d];
        }
        r = nr; c = nc;
    }
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) printf(j ? " %d" : "%d", a[i][j]);
        printf("\n");
    }
    return 0;
}
''',
  ["C++基础", "二维数组", "螺旋矩阵", "模拟"])

A("【矩阵】边界元素之和", SEC_MAT, 2,
  stmt("读入 `n×n` 矩阵，输出**最外一圈**（四条边）元素之和。\n\n"
       "四个角只能算一次。",
       ["条件：`i == 0 || i == n-1 || j == 0 || j == n-1`",
        "`n = 1` 时只有一个元素，算一次",
        "`n = 2` 时四个元素都是边界"]),
  "第一行 `n`，接下来 `n` 行。",
  "一行一个整数。",
  "- 1 ≤ n ≤ 20\n- |x| ≤ 100",
  lambda: cases(mat(401, 3), mat(402, 1), mat(403, 2), mat(404, 4), mat(405, 5), mat(406, 6)),
  lambda t: (lambda n, a: "%d\n" % sum(a[i][j] for i in range(n) for j in range(n)
                                       if i in (0, n - 1) or j in (0, n - 1)))(*read_mat(t)),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[25][25];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) scanf("%d", &a[i][j]);
    long long s = 0;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            if (i == 0 || i == n - 1 || j == 0 || j == n - 1) s += a[i][j];
    printf("%lld\n", s);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[25][25];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) scanf("%d", &a[i][j]);
    if (n == 1) { printf("%d\n", a[0][0]); return 0; }
    long long s = 0;
    for (int j = 0; j < n; j++) s += a[0][j] + a[n - 1][j];        // 上下两行
    for (int i = 1; i < n - 1; i++) s += a[i][0] + a[i][n - 1];    // 左右两列（去角）
    printf("%lld\n", s);
    return 0;
}
''',
  ["C++基础", "二维数组", "边界"])

A("【矩阵】每行升序排列", SEC_MAT, 3,
  stmt("读入 `n×n` 矩阵，把**每一行**分别升序排序后输出。",
       ["外层遍历行，内层对这一行做排序",
        "行与行之间互不影响，不要整体排序",
        "自己写冒泡或直接 `sort(a[i], a[i]+n)`"]),
  "第一行 `n`，接下来 `n` 行。",
  "`n` 行，每行 `n` 个整数。",
  "- 1 ≤ n ≤ 20\n- |x| ≤ 100",
  lambda: cases(mat(411, 3), mat(412, 1), mat(413, 4), mat(414, 5), mat(415, 2), mat(416, 6)),
  lambda t: (lambda n, a: "".join(out_row(sorted(r)) for r in a))(*read_mat(t)),
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[25][25];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) scanf("%d", &a[i][j]);
    for (int i = 0; i < n; i++) {
        std::sort(a[i], a[i] + n);          // 只排这一行
        for (int j = 0; j < n; j++) printf(j ? " %d" : "%d", a[i][j]);
        printf("\n");
    }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[25][25];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) scanf("%d", &a[i][j]);
    for (int i = 0; i < n; i++)
        for (int x = 0; x < n - 1; x++)      // 手写冒泡，只在本行内
            for (int y = 0; y < n - 1 - x; y++)
                if (a[i][y] > a[i][y + 1]) {
                    int t = a[i][y]; a[i][y] = a[i][y + 1]; a[i][y + 1] = t;
                }
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) printf(j ? " %d" : "%d", a[i][j]);
        printf("\n");
    }
    return 0;
}
''',
  ["C++基础", "二维数组", "行排序"])

A("【矩阵】顺时针旋转 90 度", SEC_MAT, 4,
  stmt("读入 `n×n` 矩阵，输出它**顺时针旋转 90 度**后的结果。\n\n"
       "规律：新矩阵第 `i` 行第 `j` 列 = 原矩阵第 `n-1-j` 行第 `i` 列。",
       ["公式记牢：`b[i][j] = a[n-1-j][i]`",
        "先转置再左右翻转也能得到同样结果，那是另一条思路",
        "不要在原地转置后忘了翻转，那样得到的是逆时针"]),
  "第一行 `n`，接下来 `n` 行。",
  "`n` 行，每行 `n` 个整数。",
  "- 1 ≤ n ≤ 20\n- |x| ≤ 100",
  lambda: cases(mat(421, 3), mat(422, 1), mat(423, 2), mat(424, 4), mat(425, 5), mat(426, 6)),
  lambda t: (lambda n, a: "".join(out_row([a[n - 1 - j][i] for j in range(n)]) for i in range(n)))(*read_mat(t)),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[25][25];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) scanf("%d", &a[i][j]);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) printf(j ? " %d" : "%d", a[n - 1 - j][i]);
        printf("\n");
    }
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[25][25];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) scanf("%d", &a[i][j]);
    for (int i = 0; i < n; i++)                  // 先转置
        for (int j = i + 1; j < n; j++) { int t = a[i][j]; a[i][j] = a[j][i]; a[j][i] = t; }
    for (int i = 0; i < n; i++) std::reverse(a[i], a[i] + n);   // 再每行翻转
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) printf(j ? " %d" : "%d", a[i][j]);
        printf("\n");
    }
    return 0;
}
''',
  ["C++基础", "二维数组", "旋转"])

A("【矩阵】矩阵周边元素平均值", SEC_MAT, 3,
  stmt("读入 `n×n` 矩阵，输出**最外一圈**元素的平均值，保留两位小数。",
       ["和上一册「边界元素之和」同一组位置，只是最后除以元素个数",
        "`n = 1` 时个数是 1；`n ≥ 2` 时个数是 `4n - 4`",
        "别把 `4n - 4` 写成 `4n` —— 四个角重复算了"]),
  "第一行 `n`，接下来 `n` 行。",
  "一行，保留两位小数。",
  "- 1 ≤ n ≤ 20\n- |x| ≤ 100",
  lambda: cases(mat(431, 3), mat(432, 1), mat(433, 2), mat(434, 4), mat(435, 5), mat(436, 6)),
  lambda t: (lambda n, a: (lambda v: "%.2f\n" % (sum(v) / len(v)))(
      [a[i][j] for i in range(n) for j in range(n)
       if i in (0, n - 1) or j in (0, n - 1)]))(*read_mat(t)),
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[25][25];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) scanf("%d", &a[i][j]);
    long long s = 0;
    int cnt = 0;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            if (i == 0 || i == n - 1 || j == 0 || j == n - 1) { s += a[i][j]; cnt++; }
    printf("%.2f\n", (double)s / cnt);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    static int a[25][25];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) scanf("%d", &a[i][j]);
    long long s = 0;
    int cnt = (n == 1) ? 1 : 4 * n - 4;      // 周长元素个数
    if (n == 1) s = a[0][0];
    else {
        for (int j = 0; j < n; j++) s += a[0][j] + a[n - 1][j];
        for (int i = 1; i < n - 1; i++) s += a[i][0] + a[i][n - 1];
    }
    printf("%.2f\n", (double)s / cnt);
    return 0;
}
''',
  ["C++基础", "二维数组", "边界", "平均值"])


# ===================================================================== #
#  本地辅助（Python oracle 用）
# ===================================================================== #
def _count(v: list[int]) -> dict[int, int]:
    d: dict[int, int] = {}
    for x in v:
        d[x] = d.get(x, 0) + 1
    return d


def _lis_run(v: list[int]) -> int:
    best = cur = 1
    for i in range(1, len(v)):
        cur = cur + 1 if v[i] > v[i - 1] else 1
        best = max(best, cur)
    return best


def _max_sub(v: list[int]) -> int:
    best = cur = v[0]
    for x in v[1:]:
        cur = cur + x if cur > 0 else x
        best = max(best, cur)
    return best


def _mode(v: list[int]) -> int:
    c = _count(v)
    best_v, best_c = None, -1
    for val in sorted(c):
        if c[val] > best_c:
            best_c, best_v = c[val], val
    return best_v


def _del_first(x: int, v: list[int]) -> str:
    if x not in v:
        return "not found\n"
    i = v.index(x)
    nv = v[:i] + v[i + 1:]
    return "%d\n%s\n" % (len(nv), " ".join(str(y) for y in nv))


def _pfx(seed: int, n: int, q: int) -> str:
    rng = random.Random(seed)
    v = [rng.randint(-1000, 1000) for _ in range(n)]
    lines = ["%d %d" % (n, q), " ".join(str(x) for x in v)]
    for _ in range(q):
        l = rng.randint(1, n)
        r = rng.randint(l, n)
        lines.append("%d %d" % (l, r))
    return "\n".join(lines) + "\n"


def _pfx_oracle(t: str) -> str:
    d = read_ints(t)
    n, q = d[0], d[1]
    v = d[2:2 + n]
    idx = 2 + n
    out = []
    for _ in range(q):
        l, r = d[idx], d[idx + 1]
        idx += 2
        out.append("%d\n" % sum(v[l - 1:r]))
    return "".join(out)


def merg(seed: int, n: int, m: int) -> str:
    rng = random.Random(seed)
    a = sorted(rng.randint(-50, 50) for _ in range(n))
    b = sorted(rng.randint(-50, 50) for _ in range(m))
    return "%d %d\n%s\n%s\n" % (n, m, " ".join(map(str, a)), " ".join(map(str, b)))


def _merge_oracle(t: str) -> str:
    d = read_ints(t)
    n, m = d[0], d[1]
    a = d[2:2 + n]
    b = d[2 + n:2 + n + m]
    return out_row(sorted(a + b))


def _two_sum_oracle(t: str) -> str:
    d = read_ints(t)
    n, target = d[0], d[1]
    v = d[2:2 + n]
    for i in range(n):
        for j in range(i + 1, n):
            if v[i] + v[j] == target:
                return "%d %d\n" % (i + 1, j + 1)
    return ""


def _mat2(seed: int, n: int) -> str:
    rng = random.Random(seed)
    a = [[rng.randint(-9, 9) for _ in range(n)] for _ in range(n)]
    b = [[rng.randint(-9, 9) for _ in range(n)] for _ in range(n)]
    return ("%d\n" % n
            + "".join(" ".join(str(x) for x in r) + "\n" for r in a)
            + "".join(" ".join(str(x) for x in r) + "\n" for r in b))


def _mat_add_oracle(t: str) -> str:
    d = read_ints(t)
    n = d[0]
    v = d[1:]
    a = [v[i * n:(i + 1) * n] for i in range(n)]
    b = [v[n * n + i * n:n * n + (i + 1) * n] for i in range(n)]
    return "".join(out_row([a[i][j] + b[i][j] for j in range(n)]) for i in range(n))


def _mat_mul_oracle(t: str) -> str:
    d = read_ints(t)
    n = d[0]
    v = d[1:]
    a = [v[i * n:(i + 1) * n] for i in range(n)]
    b = [v[n * n + i * n:n * n + (i + 1) * n] for i in range(n)]
    out = []
    for i in range(n):
        row = [sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)]
        out.append(out_row(row))
    return "".join(out)


def _mat_max(n: int, a: list[list[int]]) -> str:
    best = a[0][0]
    br = bc = 0
    for i in range(n):
        for j in range(n):
            if a[i][j] > best:
                best, br, bc = a[i][j], i, j
    return "%d %d %d\n" % (best, br + 1, bc + 1)


def _saddle_cases(seed: int, n: int, has: bool) -> str:
    if has:
        # 构造一个一定有鞍点的矩阵：第 0 行整体最大，且 a[0][0] 是第 0 列最小
        rng = random.Random(seed)
        a = [[rng.randint(1, 20) for _ in range(n)] for _ in range(n)]
        for j in range(n):
            a[0][j] = 90 + j          # 第 0 行最大在 a[0][n-1]
        for i in range(n):
            a[i][n - 1] = max(a[i][n - 1], 1) if i else a[0][n - 1]
        # 让 a[0][n-1] 成为该列最小
        for i in range(1, n):
            a[i][n - 1] = 100 + i
        return "%d\n" % n + "".join(" ".join(str(x) for x in r) + "\n" for r in a)
    rng = random.Random(seed)
    a = [[rng.randint(1, 9) for _ in range(n)] for _ in range(n)]
    return "%d\n" % n + "".join(" ".join(str(x) for x in r) + "\n" for r in a)


def _saddle_oracle(t: str) -> str:
    n, a = read_mat(t)
    for i in range(n):
        bc = max(range(n), key=lambda j: a[i][j])
        if all(a[k][bc] >= a[i][bc] for k in range(n)):
            return "%d %d %d\n" % (i + 1, bc + 1, a[i][bc])
    return "No\n"


def _upper_cases(seed: int, n: int, yes: bool) -> str:
    rng = random.Random(seed)
    a = [[rng.randint(1, 9) if (yes and i <= j) else (rng.randint(1, 9) if (not yes and i <= j) else 0)
          for j in range(n)] for i in range(n)]
    if not yes:
        a[n - 1][0] = rng.randint(1, 9)      # 保证下三角有个非零
    return "%d\n" % n + "".join(" ".join(str(x) for x in r) + "\n" for r in a)


def _upper_oracle(t: str) -> str:
    n, a = read_mat(t)
    for i in range(n):
        for j in range(i):
            if a[i][j] != 0:
                return "NO\n"
    return "YES\n"


def _spiral(n: int) -> str:
    a = [[0] * n for _ in range(n)]
    v, top, bot, left, right = 1, 0, n - 1, 0, n - 1
    while top <= bot and left <= right:
        for j in range(left, right + 1):
            a[top][j] = v
            v += 1
        top += 1
        for i in range(top, bot + 1):
            a[i][right] = v
            v += 1
        right -= 1
        if top <= bot:
            for j in range(right, left - 1, -1):
                a[bot][j] = v
                v += 1
        bot -= 1
        if left <= right:
            for i in range(bot, top - 1, -1):
                a[i][left] = v
                v += 1
        left += 1
    return "".join(out_row(r) for r in a)


if __name__ == "__main__":
    raise SystemExit(cli(PROBLEMS, "app/problems_bank_cpp_basic3.py",
                         "C++ 编程题第三册：一维数组 / 二维数组与矩阵（40 题）",
                         "CPP_BASIC3_PROBLEMS"))
