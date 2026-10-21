# -*- coding: utf-8 -*-
"""C++ 基础编程题 · 第 7 册：排序与查找（20）+ 贪心（20）= 40 题。

对应教材第 09 讲「排序与查找」的思路延伸。这一册练「把 O(n²) 换成 O(n log n)」：
冒泡/选择/插入各自的交换与比较次数、归并顺带数逆序对、二分要有单调性、
贪心要能证明「局部最优能推到全局最优」。

★ 贪心题的 oracle 一律用「暴力枚举最优」在小规模上验证，绝不拿贪心校贪心。
★ 排序题不考「输出排序结果」，一律问排序之后的一个统计量。

重生成：python tools/gen_cpp_basic7.py
"""
from __future__ import annotations

import itertools
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cpp_basic_kit import cases, cli, stmt          # noqa: E402

SEC_SORT = "C++ 编程 · 排序与查找"
SEC_GRD = "C++ 编程 · 贪心"

PROBLEMS: list[dict] = []


def A(title, sec, d, st, inf, outf, con, inp, orc, sol, alt, tags):
    PROBLEMS.append(dict(title=title, section=sec, difficulty=d, statement_md=st,
                         input_format=inf, output_format=outf, constraints_md=con,
                         inputs=inp, oracle=orc, solution=sol, alt=alt, tags=tags))


def rints(seed: int, n: int, lo: int = -50, hi: int = 50) -> list[int]:
    rng = random.Random(seed)
    return [rng.randint(lo, hi) for _ in range(n)]


def barr(seed: int, n: int, lo: int = -50, hi: int = 50) -> str:
    v = rints(seed, n, lo, hi)
    return "%d\n%s\n" % (n, " ".join(str(x) for x in v))


def toks(t: str) -> list[int]:
    return [int(x) for x in t.split()]


def arr_of(t: str) -> list[int]:
    return toks(t)[1:]


def out(v) -> str:
    return " ".join(str(x) for x in v) + "\n"


# ===================================================================== #
#  SEC_SORT · 排序与查找（20 题）
# ===================================================================== #

def _bubble_swaps(t: str) -> str:
    a = arr_of(t)
    sw = 0
    n = len(a)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                sw += 1
    return "%d\n" % sw


def _select_positions(t: str) -> str:
    a = arr_of(t)
    n = len(a)
    res = []
    for i in range(n - 1):
        k = i
        for j in range(i + 1, n):
            if a[j] < a[k]:
                k = j
        res.append(k + 1)
        a[i], a[k] = a[k], a[i]
    return out(res)


def _insert_moves(t: str) -> str:
    a = arr_of(t)
    moves = 0
    for i in range(1, len(a)):
        key, j = a[i], i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
            moves += 1
        a[j + 1] = key
    return "%d\n" % moves


def _count_sort(t: str) -> str:
    a = arr_of(t)
    cnt = {}
    for x in a:
        cnt[x] = cnt.get(x, 0) + 1
    return out("%d:%d" % (k, cnt[k]) for k in sorted(cnt))


def _inv_count(t: str) -> str:
    a = arr_of(t)
    return "%d\n" % sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > a[j])


def _bin_search_cmp(t: str) -> str:
    tok = toks(t)
    n, x = tok[0], tok[1]
    a = tok[2:2 + n]
    lo, hi, cnt = 0, n - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        cnt += 1
        if a[mid] == x:
            return "%d %d\n" % (mid + 1, cnt)
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return "%d %d\n" % (-1, cnt)


def _split_max(t: str) -> str:
    tok = toks(t)
    n, m = tok[0], tok[1]
    a = tok[2:2 + n]
    best = None
    for cut in itertools.combinations(range(1, n), m - 1):
        segs, prev = [], 0
        for c in cut:
            segs.append(sum(a[prev:c]))
            prev = c
        segs.append(sum(a[prev:]))
        v = max(segs)
        if best is None or v < best:
            best = v
    return "%d\n" % best


def _kth(t: str) -> str:
    tok = toks(t)
    n, k = tok[0], tok[1]
    return "%d\n" % sorted(tok[2:2 + n])[k - 1]


def _sort_dedup(t: str) -> str:
    a = arr_of(t)
    seen, res = set(), []
    for x in sorted(a):
        if x not in seen:
            seen.add(x)
            res.append(x)
    return out(res)


def _stable_names(t: str) -> str:
    ln = [x.split() for x in t.strip().splitlines()]
    n = int(ln[0][0])
    v = [(r[0], int(r[1])) for r in ln[1:1 + n]]
    v.sort(key=lambda p: -p[1])           # 稳定排序：同分保持输入顺序
    return "\n".join(p[0] for p in v) + "\n"      # 题目要求每行一个姓名


def _rank(t: str) -> str:
    a = arr_of(t)
    s = sorted(a, reverse=True)
    return out(s.index(x) + 1 for x in a)


def _merge_intervals(t: str) -> str:
    ln = [x.split() for x in t.strip().splitlines()]
    n = int(ln[0][0])
    iv = sorted((int(r[0]), int(r[1])) for r in ln[1:1 + n])
    cnt, cur_l, cur_r = 0, None, None
    for l, r in iv:
        if cur_l is None:
            cnt, cur_l, cur_r = 1, l, r
        elif l <= cur_r:
            cur_r = max(cur_r, r)
        else:
            cnt += 1
            cur_l, cur_r = l, r
    return "%d\n" % cnt


def _median(t: str) -> str:
    a = sorted(arr_of(t))
    n = len(a)
    if n % 2:
        return "%d\n" % a[n // 2]
    return "%.1f\n" % ((a[n // 2 - 1] + a[n // 2]) / 2.0)


def _common(t: str) -> str:
    tok = toks(t)
    n = tok[0]
    a = tok[1:1 + n]
    m = tok[1 + n]
    b = tok[2 + n:2 + n + m]
    return "%d\n" % len(set(a) & set(b))


def _max_gap(t: str) -> str:
    a = sorted(set(arr_of(t)))
    return "%d\n" % max((a[i + 1] - a[i] for i in range(len(a) - 1)), default=0)


def _abs_sort(t: str) -> str:
    a = arr_of(t)
    return out(sorted(a, key=lambda x: (abs(x), x)))


def _digit_sort(t: str) -> str:
    a = arr_of(t)
    return out(sorted(a, key=lambda x: (abs(x) % 10, x)))


def _quick_sort(t: str) -> str:
    def qs(v):
        if len(v) <= 1:
            return v
        p = v[0]
        return qs([x for x in v[1:] if x < p]) + [p] + qs([x for x in v[1:] if x >= p])
    return out(qs(arr_of(t)))


def _count_cmp(t: str) -> str:
    tok = toks(t)
    n, x = tok[0], tok[1]
    a = tok[2:2 + n]
    lin = a.index(x) + 1 if x in a else n
    lo, hi, bin_c = 0, n - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        bin_c += 1
        if a[mid] == x:
            break
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return "%d %d\n" % (lin, bin_c)


def _mode(t: str) -> str:
    a = arr_of(t)
    cnt = {}
    for x in a:
        cnt[x] = cnt.get(x, 0) + 1
    best = max(cnt.values())
    return "%d\n" % min(k for k, v in cnt.items() if v == best)


A("【排序】冒泡排序统计交换次数", SEC_SORT, 1,
  stmt("用冒泡排序把数组排成升序，输出**发生交换的次数**（不输出数组）。",
       ["只有 `a[j] > a[j+1]` 时才交换，相等不交换 —— 这决定了交换次数",
        "交换次数正好等于逆序对个数，可以拿来对数",
        "输出一个整数"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：交换次数。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases(barr(1, 5), "5\n1 2 3 4 5", "5\n5 4 3 2 1", "4\n3 3 3 3",
                barr(2, 20), barr(3, 50, -10, 10)),
  _bubble_swaps,
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    long long sw = 0;
    for (int i = 0; i < n - 1; i++)
        for (int j = 0; j < n - 1 - i; j++)
            if (a[j] > a[j + 1]) {                 // 严格大于才换
                int t = a[j]; a[j] = a[j + 1]; a[j + 1] = t;
                sw++;
            }
    printf("%lld\n", sw);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    long long sw = 0;                              // 直接数逆序对，结果一样
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            if (a[i] > a[j]) sw++;
    printf("%lld\n", sw);
    return 0;
}
''',
  ["排序", "冒泡", "逆序对"])

A("【排序】选择排序每轮最小值位置", SEC_SORT, 2,
  stmt("用选择排序把数组排成升序，输出**每一轮选出的最小值所在位置**（从 1 开始）。"
       "共 `n-1` 轮，输出 `n-1` 个数，一行。",
       ["第 i 轮是在 `[i, n-1]` 范围内找最小值，位置按原数组下标记",
        "并列最小值取**最先出现**的那个（比较用严格小于）",
        "共 `n-1` 个数（最后剩一个不用选）"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：`n-1` 个位置下标（1 起）。",
  "- 2 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases("5\n5 4 3 2 1", "5\n1 2 3 4 5", "4\n2 1 4 3", "2\n2 1",
                barr(4, 8), barr(5, 10, -10, 10)),
  _select_positions,
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n < 2) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    for (int i = 0; i < n - 1; i++) {
        int k = i;
        for (int j = i + 1; j < n; j++) if (a[j] < a[k]) k = j;   // 严格小于
        printf("%d%c", k + 1, i == n - 2 ? '\n' : ' ');
        int t = a[i]; a[i] = a[k]; a[k] = t;
    }
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n < 2) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    for (int i = 0; i < n - 1; i++) {
        int *p = std::min_element(a + i, a + n);     // 指针版最小元
        printf("%d%c", (int)(p - a) + 1, i == n - 2 ? '\n' : ' ');
        int t = a[i]; a[i] = *p; *p = t;
    }
    return 0;
}
''',
  ["排序", "选择排序"])

A("【排序】插入排序统计移动次数", SEC_SORT, 2,
  stmt("用插入排序把数组排成升序，统计**元素后移的总次数**（每次 `a[j+1] = a[j]` 记 1 次），"
       "输出这个次数。",
       ["插入时比 `key` 大的元素都要往后挪一格，挪一次记一次",
        "已经有序的数组移动次数是 0；完全逆序是 `n(n-1)/2`",
        "输出一个整数"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：后移次数。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases("5\n5 4 3 2 1", "5\n1 2 3 4 5", "4\n2 1 4 3", "1\n7",
                barr(6, 10), barr(7, 30, -10, 10)),
  _insert_moves,
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    long long moves = 0;
    for (int i = 1; i < n; i++) {
        int key = a[i], j = i - 1;
        while (j >= 0 && a[j] > key) {   // 严格大于才后移
            a[j + 1] = a[j];
            j--;
            moves++;
        }
        a[j + 1] = key;
    }
    printf("%lld\n", moves);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    long long moves = 0;                 // 等价于数逆序对
    for (int i = 1; i < n; i++)
        for (int j = 0; j < i; j++)
            if (a[j] > a[i]) moves++;
    printf("%lld\n", moves);
    return 0;
}
''',
  ["排序", "插入排序"])

A("【排序】计数排序输出频次表", SEC_SORT, 2,
  stmt("数组元素都在 `0`~`100` 之间。用计数排序统计每个值出现的次数，按值升序输出"
       "`值:次数`，用空格分隔（只输出出现过的值）。",
       ["计数排序的核心是「值 → 下标」直接映射，不做比较",
        "输出格式是 `值:次数`，注意冒号两边没有空格",
        "输出一行"]),
  "第一行 `n`，第二行 `n` 个整数（0 ≤ x ≤ 100）。",
  "一行：`值:次数` 序列。",
  "- 1 ≤ n ≤ 1000\n- 0 ≤ x ≤ 100",
  lambda: cases("5\n3 1 3 2 3", "1\n0", "3\n100 100 1",
                barr(8, 10, 0, 5), barr(9, 20, 90, 100), barr(10, 15, 0, 3)),
  _count_sort,
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    int cnt[101] = {0};
    for (int i = 0; i < n; i++) { int x; scanf("%d", &x); cnt[x]++; }
    bool first = true;
    for (int v = 0; v <= 100; v++) {
        if (!cnt[v]) continue;
        printf("%s%d:%d", first ? "" : " ", v, cnt[v]);
        first = false;
    }
    printf("\n");
    return 0;
}
''',
  r'''#include <cstdio>
#include <map>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    std::map<int, int> cnt;              // map 天然按 key 升序
    for (int i = 0; i < n; i++) { int x; scanf("%d", &x); cnt[x]++; }
    bool first = true;
    for (auto &kv : cnt) {
        printf("%s%d:%d", first ? "" : " ", kv.first, kv.second);
        first = false;
    }
    printf("\n");
    return 0;
}
''',
  ["排序", "计数排序", "频次"])

A("【排序】归并排序求逆序对", SEC_SORT, 4,
  stmt("用归并排序统计数组的逆序对个数（`i < j` 且 `a[i] > a[j]` 的数对数量）。",
       ["归并时，右半段某个元素被取走时，左半段剩下的元素都比它大，一次就能贡献一批逆序对",
        "n 到 2×10⁵ 时逆序对最多约 2×10¹⁰，答案用 `long long`",
        "输出一个整数"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：逆序对个数。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases("5\n5 4 3 2 1", "5\n1 2 3 4 5", "4\n2 1 4 3", "1\n7",
                barr(11, 10), barr(12, 15, -5, 5)),
  _inv_count,
  r'''#include <cstdio>
int a[1005], tmp[1005];
long long cnt = 0;
void msort(int l, int r) {
    if (l >= r) return;
    int m = (l + r) / 2;
    msort(l, m);
    msort(m + 1, r);
    int i = l, j = m + 1, k = l;
    while (i <= m && j <= r) {
        if (a[i] <= a[j]) tmp[k++] = a[i++];
        else { cnt += m - i + 1; tmp[k++] = a[j++]; }   // 左半段剩下的都比它大
    }
    while (i <= m) tmp[k++] = a[i++];
    while (j <= r) tmp[k++] = a[j++];
    for (int t = l; t <= r; t++) a[t] = tmp[t];
}
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    msort(0, n - 1);
    printf("%lld\n", cnt);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    long long c = 0;                      // 暴力 O(n²)，对拍用
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            if (a[i] > a[j]) c++;
    printf("%lld\n", c);
    return 0;
}
''',
  ["排序", "归并", "逆序对"])

A("【查找】二分查找并统计比较次数", SEC_SORT, 2,
  stmt("数组升序。读入 `n x` 和 `n` 个整数，用二分查找找 `x`，输出「位置（1 起，找不到 -1）」"
       "与「比较次数」，一行，空格分隔。",
       ["每比较一次 `mid` 记 1 次，不管是否命中",
        "`mid = (lo + hi) / 2`，循环条件是 `lo <= hi`",
        "输出一行两个整数"]),
  "第一行 `n x`；第二行 `n` 个升序整数。",
  "一行：`位置 比较次数`。",
  "- 1 ≤ n ≤ 1000\n- |x|, |a[i]| ≤ 10⁶",
  lambda: cases("5 3\n1 3 5 7 9", "5 4\n1 3 5 7 9", "1 1\n1", "1 2\n1",
                "7 9\n1 3 5 7 9 11 13", "4 1\n1 2 3 4"),
  _bin_search_cmp,
  r'''#include <cstdio>
int main() {
    int n, x;
    if (scanf("%d %d", &n, &x) != 2) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int lo = 0, hi = n - 1, cnt = 0;
    while (lo <= hi) {
        int mid = (lo + hi) / 2;
        cnt++;                            // 每次比较都计数
        if (a[mid] == x) { printf("%d %d\n", mid + 1, cnt); return 0; }
        if (a[mid] < x) lo = mid + 1;
        else hi = mid - 1;
    }
    printf("-1 %d\n", cnt);
    return 0;
}
''',
  r'''#include <cstdio>
int bs(const int a[], int lo, int hi, int x, int &cnt) {   // 递归版
    if (lo > hi) return -1;
    int mid = (lo + hi) / 2;
    cnt++;
    if (a[mid] == x) return mid + 1;
    if (a[mid] < x) return bs(a, mid + 1, hi, x, cnt);
    return bs(a, lo, mid - 1, x, cnt);
}
int main() {
    int n, x;
    if (scanf("%d %d", &n, &x) != 2) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int cnt = 0;
    int p = bs(a, 0, n - 1, x, cnt);
    printf("%d %d\n", p, cnt);
    return 0;
}
''',
  ["查找", "二分", "比较次数"])

A("【查找】二分答案求最小最大段和", SEC_SORT, 4,
  stmt("把长度为 `n` 的正整数数组切成 `m` 段**连续**子数组，让「各段和的最大值」尽量小，"
       "输出这个最小值。",
       ["答案有单调性：给定上限 `L`，段数不超过 `m` 是否可行，随 `L` 增大而变容易 —— 这就是二分答案的前提",
        "判定函数：从左往右贪心累加，超了就切一刀，统计需要几段",
        "下界是 `max(a[i])`，上界是 `sum(a)`"]),
  "第一行 `n m`；第二行 `n` 个正整数。",
  "一行：最小的「最大段和」。",
  "- 1 ≤ n ≤ 1000\n- 1 ≤ m ≤ n\n- 1 ≤ a[i] ≤ 10⁶",
  lambda: cases("5 2\n7 2 5 10 8", "1 1\n5", "3 3\n1 2 3", "4 2\n1 1 1 1",
                "8 2\n" + " ".join(str(x) for x in rints(13, 8, 1, 20)) + "\n",
                "%d %d\n%s" % (10, 3, " ".join(str(x) for x in rints(14, 10, 1, 30)))),
  _split_max,
  r'''#include <cstdio>
int n, m;
int a[1005];
bool ok(long long lim) {                 // 上限 lim 时能否切成不超过 m 段
    long long cur = 0;
    int seg = 1;
    for (int i = 0; i < n; i++) {
        if (cur + a[i] <= lim) cur += a[i];
        else { seg++; cur = a[i]; }
    }
    return seg <= m;
}
int main() {
    if (scanf("%d %d", &n, &m) != 2) return 0;
    long long lo = 0, hi = 0;
    for (int i = 0; i < n; i++) {
        scanf("%d", &a[i]);
        if (a[i] > lo) lo = a[i];        // 下界：单个最大值
        hi += a[i];                      // 上界：总和
    }
    while (lo < hi) {
        long long mid = lo + (hi - lo) / 2;
        if (ok(mid)) hi = mid; else lo = mid + 1;
    }
    printf("%lld\n", lo);
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int n, m, a[1005];
bool ok(long long lim) {
    int seg = 1; long long cur = 0;
    for (int i = 0; i < n; i++) {
        if (cur + a[i] <= lim) cur += a[i];
        else { seg++; cur = a[i]; }
    }
    return seg <= m;
}
int main() {
    if (scanf("%d %d", &n, &m) != 2) return 0;
    long long sum = 0, mx = 0;
    for (int i = 0; i < n; i++) { scanf("%d", &a[i]); sum += a[i]; mx = std::max(mx, (long long)a[i]); }
    long long lo = mx - 1, hi = sum;     // 开区间写法：lo 恒不可行
    while (hi - lo > 1) {
        long long mid = (lo + hi) / 2;
        if (ok(mid)) hi = mid; else lo = mid;
    }
    printf("%lld\n", hi);
    return 0;
}
''',
  ["查找", "二分答案", "单调性"])

A("【排序】求第 k 小的数", SEC_SORT, 3,
  stmt("读入 `n k` 和 `n` 个整数，输出第 `k` 小的数（`k` 从 1 开始，重复值分别计数）。",
       ["排序后取 `a[k-1]` 最直观，O(n log n)",
        "只要第 k 小的话，`nth_element` 平均 O(n)",
        "输出一个整数"]),
  "第一行 `n k`；第二行 `n` 个整数。",
  "一行：第 `k` 小的数。",
  "- 1 ≤ n ≤ 1000\n- 1 ≤ k ≤ n\n- |x| ≤ 10⁶",
  lambda: cases("5 1\n5 3 1 4 2", "5 5\n5 3 1 4 2", "5 3\n5 3 1 4 2", "1 1\n7",
                "6 4\n2 2 3 3 1 1", "%d %d\n%s" % (8, 3, " ".join(str(x) for x in rints(15, 8)))),
  _kth,
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n, k;
    if (scanf("%d %d", &n, &k) != 2 || k < 1 || k > n) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    std::nth_element(a, a + k - 1, a + n);   // 平均 O(n)
    printf("%d\n", a[k - 1]);
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n, k;
    if (scanf("%d %d", &n, &k) != 2 || k < 1 || k > n) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    std::sort(a, a + n);                     // 全排一遍也对
    printf("%d\n", a[k - 1]);
    return 0;
}
''',
  ["排序", "第k小", "nth_element"])

A("【排序】排序后去重输出", SEC_SORT, 2,
  stmt("读入 `n` 个整数，升序输出去重后的结果（每个值只出现一次）。",
       ["先排序，相邻相等就跳过 —— 这样去重是 O(n) 的",
        "也可以用 `unique` 配 `erase`（数组用「逻辑长度」模拟）",
        "输出一行"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：升序去重结果。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases("5\n3 1 3 2 3", "1\n7", "4\n1 1 1 1", "5\n5 4 3 2 1",
                barr(16, 12, 1, 5), barr(17, 10, -3, 3)),
  _sort_dedup,
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    std::sort(a, a + n);
    int k = 0;
    for (int i = 0; i < n; i++)
        if (i == 0 || a[i] != a[i - 1]) a[k++] = a[i];   // 相邻相等就跳过
    for (int i = 0; i < k; i++) printf("%d%c", a[i], i + 1 == k ? '\n' : ' ');
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    std::sort(a, a + n);
    int k = (int)(std::unique(a, a + n) - a);   // unique 返回新末尾
    for (int i = 0; i < k; i++) printf("%d%c", a[i], i + 1 == k ? '\n' : ' ');
    return 0;
}
''',
  ["排序", "去重", "unique"])

A("【排序】稳定排序保原顺序", SEC_SORT, 3,
  stmt("读入 `n` 个人（姓名、分数），按分数**降序**输出姓名，**分数相同的保持输入顺序**。",
       ["`std::sort` 不保证稳定，同分时顺序可能被打乱 —— 这题就是要你意识到这点",
        "`std::stable_sort` 或「比较函数里加原始下标」都能解决",
        "每行一个姓名"]),
  "第一行 `n`；之后 `n` 行，每行 `姓名 分数`。",
  "`n` 行：按分数降序的姓名。",
  "- 1 ≤ n ≤ 1000\n- 0 ≤ 分数 ≤ 100",
  lambda: cases("3\na 90\nb 90\nc 80", "3\na 80\nb 90\nc 80",
                "1\nsolo 100", "4\nw 70\nx 70\ny 70\nz 70",
                "5\na 60\nb 70\nc 60\nd 80\ne 60",
                "4\np 100\nq 100\nr 90\ns 100"),
  _stable_names,
  r'''#include <cstdio>
#include <algorithm>
struct Person {
    char name[32];
    int score;
};
bool cmp(const Person &a, const Person &b) { return a.score > b.score; }
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static Person v[1005];
    for (int i = 0; i < n; i++) scanf("%31s %d", v[i].name, &v[i].score);
    std::stable_sort(v, v + n, cmp);       // 稳定排序
    for (int i = 0; i < n; i++) printf("%s\n", v[i].name);
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
struct Person { char name[32]; int score, idx; };
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static Person v[1005];
    for (int i = 0; i < n; i++) { scanf("%31s %d", v[i].name, &v[i].score); v[i].idx = i; }
    std::sort(v, v + n, [](const Person &a, const Person &b) {
        if (a.score != b.score) return a.score > b.score;
        return a.idx < b.idx;              // 用原始下标把稳定性补回来
    });
    for (int i = 0; i < n; i++) printf("%s\n", v[i].name);
    return 0;
}
''',
  ["排序", "稳定排序"])

A("【排序】成绩排名（同分同名次）", SEC_SORT, 2,
  stmt("读入 `n` 个分数，按**从高到低**输出每个分数对应的名次（同分同名次，名次按"
       "「比我高的人数 + 1」计算），保持输入顺序输出。",
       ["名次 = 严格大于它的元素个数 + 1，所以同分必然同名次",
        "不要用「排序后下标 +1」，那样同分会拿到不同名次",
        "输出一行 `n` 个整数"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：`n` 个名次。",
  "- 1 ≤ n ≤ 1000\n- 0 ≤ 分数 ≤ 100",
  lambda: cases("5\n90 80 90 70 100", "5\n50 50 50 50 50", "1\n60",
                "3\n100 90 80", barr(18, 8, 60, 100), barr(19, 10, 0, 3)),
  _rank,
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    for (int i = 0; i < n; i++) {
        int r = 1;
        for (int j = 0; j < n; j++) if (a[j] > a[i]) r++;   // 比我高的 +1
        printf("%d%c", r, i + 1 == n ? '\n' : ' ');
    }
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005], t[1005];
    for (int i = 0; i < n; i++) { scanf("%d", &a[i]); t[i] = a[i]; }
    std::sort(t, t + n);                                       // 升序
    for (int i = 0; i < n; i++) {
        int le = (int)(std::upper_bound(t, t + n, a[i]) - t);   // <= a[i] 的个数
        printf("%d%c", n - le + 1, i + 1 == n ? '\n' : ' ');    // 比我高的 +1
    }
    return 0;
}
''',
  ["排序", "排名", "并列"])

A("【排序】区间合并计数", SEC_SORT, 3,
  stmt("读入 `n` 个闭区间 `[l, r]`，把有重叠（含端点相接）的区间合并，输出合并后的区间个数。",
       ["先按左端点排序，再线性扫描：能接上就扩右端点，接不上就新开一段",
        "「端点相接」算重叠：`l <= cur_r` 就合并",
        "输出一个整数"]),
  "第一行 `n`；之后 `n` 行，每行 `l r`。",
  "一行：合并后的区间数。",
  "- 1 ≤ n ≤ 1000\n- 0 ≤ l ≤ r ≤ 10⁶",
  lambda: cases("3\n1 3\n2 4\n5 6", "1\n0 0", "3\n1 2\n3 4\n5 6", "2\n1 10\n2 3",
                "4\n5 6\n1 3\n2 2\n8 9", "3\n1 1\n1 1\n2 2"),
  _merge_intervals,
  r'''#include <cstdio>
#include <algorithm>
struct Seg { int l, r; };
bool cmp(const Seg &a, const Seg &b) { return a.l < b.l; }
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static Seg v[1005];
    for (int i = 0; i < n; i++) scanf("%d %d", &v[i].l, &v[i].r);
    std::sort(v, v + n, cmp);              // 按左端点排序
    int cnt = 1, cr = v[0].r;
    for (int i = 1; i < n; i++) {
        if (v[i].l <= cr) { if (v[i].r > cr) cr = v[i].r; }   // 能接上
        else { cnt++; cr = v[i].r; }
    }
    printf("%d\n", cnt);
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int L[1005], R[1005];
    for (int i = 0; i < n; i++) { scanf("%d %d", &L[i], &R[i]); }
    static int idx[1005];
    for (int i = 0; i < n; i++) idx[i] = i;
    std::sort(idx, idx + n, [&](int x, int y) { return L[x] < L[y]; });
    int cnt = 1, cr = R[idx[0]];
    for (int k = 1; k < n; k++) {
        int i = idx[k];
        if (L[i] <= cr) { if (R[i] > cr) cr = R[i]; }
        else { cnt++; cr = R[i]; }
    }
    printf("%d\n", cnt);
    return 0;
}
''',
  ["排序", "区间合并", "扫描线"])

A("【排序】求中位数", SEC_SORT, 2,
  stmt("读入 `n` 个整数，输出中位数。`n` 为奇数时就是中间那个；为偶数时是中间两个的平均值，"
       "保留 1 位小数。",
       ["奇数个直接取 `a[n/2]`；偶数个取 `(a[n/2-1] + a[n/2]) / 2.0`",
        "偶数时除以 2.0，写 `/ 2` 会截断",
        "输出一行"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：中位数（偶数个时保留 1 位小数）。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases("5\n3 1 4 1 5", "4\n1 2 3 4", "1\n7", "2\n4 4",
                barr(20, 8), barr(21, 9, -10, 10)),
  _median,
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    std::sort(a, a + n);
    if (n % 2) printf("%d\n", a[n / 2]);
    else printf("%.1f\n", (a[n / 2 - 1] + a[n / 2]) / 2.0);   // 除以 2.0
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    std::nth_element(a, a + n / 2, a + n);        // 只保证中间位置对
    if (n % 2) { printf("%d\n", a[n / 2]); return 0; }
    int hi = a[n / 2];
    std::nth_element(a, a + n / 2 - 1, a + n);    // 再找低一位
    printf("%.1f\n", (a[n / 2 - 1] + hi) / 2.0);
    return 0;
}
''',
  ["排序", "中位数"])

A("【排序】两数组共同元素个数", SEC_SORT, 3,
  stmt("读入两个数组，输出它们的**不同**共同元素个数（同一个值在两数组都出现就算 1 个，"
       "不重复计数）。",
       ["排序 + 双指针：相等就计数并同时前移，谁小谁前移",
        "也可以直接 `set` 求交集",
        "格式：第一行 `n`，第二行 `n` 个数；第三行 `m`，第四行 `m` 个数"]),
  "第一行 `n`；第二行 `n` 个整数；第三行 `m`；第四行 `m` 个整数。",
  "一行：共同元素个数。",
  "- 1 ≤ n, m ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases("3\n1 2 3\n3\n2 3 4", "1\n5\n1\n5", "2\n1 2\n2\n3 4",
                "4\n1 1 2 2\n3\n2 3 3", "3\n9 8 7\n2\n7 6", "1\n0\n1\n1"),
  _common,
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n, m;
    if (scanf("%d", &n) != 1) return 0;
    static int a[1005], b[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    if (scanf("%d", &m) != 1) return 0;
    for (int i = 0; i < m; i++) scanf("%d", &b[i]);
    std::sort(a, a + n);
    std::sort(b, b + m);
    int i = 0, j = 0, c = 0;
    while (i < n && j < m) {
        if (a[i] == b[j]) { c++; i++; j++; }
        else if (a[i] < b[j]) i++;
        else j++;
    }
    printf("%d\n", c);
    return 0;
}
''',
  r'''#include <cstdio>
#include <set>
int main() {
    int n, m;
    if (scanf("%d", &n) != 1) return 0;
    std::set<int> s;
    for (int i = 0; i < n; i++) { int x; scanf("%d", &x); s.insert(x); }
    if (scanf("%d", &m) != 1) return 0;
    std::set<int> t;
    for (int i = 0; i < m; i++) { int x; scanf("%d", &x); if (s.count(x)) t.insert(x); }
    printf("%d\n", (int)t.size());
    return 0;
}
''',
  ["排序", "双指针", "交集"])

A("【排序】排序后相邻最大差值", SEC_SORT, 2,
  stmt("读入 `n` 个整数，排序后求**相邻两个不同值**之间的最大差值；只有一个不同值时输出 0。",
       ["先去重再算相邻差，否则重复值会让差值恒为 0",
        "排序后一趟扫描就够",
        "输出一个整数"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：最大相邻差。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases("5\n1 5 3 9 7", "3\n5 5 5", "1\n7", "2\n1 100",
                barr(22, 10), barr(23, 12, 0, 20)),
  _max_gap,
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    std::sort(a, a + n);
    int best = 0;
    for (int i = 1; i < n; i++) {
        int d = a[i] - a[i - 1];
        if (d > best) best = d;          // 重复值差为 0，不影响
    }
    printf("%d\n", best);
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    std::sort(a, a + n);
    int k = (int)(std::unique(a, a + n) - a);    // 先去重
    int best = 0;
    for (int i = 1; i < k; i++) best = std::max(best, a[i] - a[i - 1]);
    printf("%d\n", best);
    return 0;
}
''',
  ["排序", "相邻差"])

A("【排序】按绝对值排序", SEC_SORT, 2,
  stmt("读入 `n` 个整数，按**绝对值升序**输出；绝对值相同时负数排前面。",
       ["比较器写 `abs(x) < abs(y)`，相等时再比大小",
        "绝对值相等时若要求「负数在前」，就是 `x < y`",
        "输出一行"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：按绝对值升序的结果。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases("4\n-3 1 2 -1", "3\n5 -5 0", "1\n-7", "4\n4 -4 2 -2",
                barr(24, 10, -20, 20), barr(25, 8, -5, 5)),
  _abs_sort,
  r'''#include <cstdio>
#include <cstdlib>
#include <algorithm>
bool cmp(int x, int y) {
    int ax = abs(x), ay = abs(y);
    if (ax != ay) return ax < ay;     // 绝对值升序
    return x < y;                     // 绝对值相同负数在前
}
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    std::sort(a, a + n, cmp);
    for (int i = 0; i < n; i++) printf("%d%c", a[i], i + 1 == n ? '\n' : ' ');
    return 0;
}
''',
  r'''#include <cstdio>
#include <cstdlib>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    std::sort(a, a + n, [](int x, int y) {
        return std::make_pair(abs(x), x) < std::make_pair(abs(y), y);   // pair 字典序
    });
    for (int i = 0; i < n; i++) printf("%d%c", a[i], i + 1 == n ? '\n' : ' ');
    return 0;
}
''',
  ["排序", "绝对值", "比较器"])

A("【排序】按个位数字排序", SEC_SORT, 3,
  stmt("读入 `n` 个整数，按**个位数字升序**输出；个位相同的按数值升序。"
       "负数的个位取其绝对值的最低位。",
       ["`abs(x) % 10` 才是「个位数字」，`x % 10` 对负数会得到负数",
        "比较器里第二个关键字用 `x < y`",
        "输出一行"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：按个位数字升序的结果。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases("4\n23 11 45 12", "3\n-23 23 0", "1\n7", "4\n9 19 29 39",
                barr(26, 10, -30, 30), barr(27, 9, 0, 50)),
  _digit_sort,
  r'''#include <cstdio>
#include <cstdlib>
#include <algorithm>
bool cmp(int x, int y) {
    int dx = abs(x) % 10, dy = abs(y) % 10;   // 负数取绝对值再取个位
    if (dx != dy) return dx < dy;
    return x < y;
}
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    std::sort(a, a + n, cmp);
    for (int i = 0; i < n; i++) printf("%d%c", a[i], i + 1 == n ? '\n' : ' ');
    return 0;
}
''',
  r'''#include <cstdio>
#include <cstdlib>
#include <vector>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    std::vector<int> bucket[10];            // 桶排序：按个位分 10 个桶
    for (int i = 0; i < n; i++) {
        int x; scanf("%d", &x);
        bucket[abs(x) % 10].push_back(x);
    }
    bool first = true;
    for (int d = 0; d < 10; d++) {
        std::sort(bucket[d].begin(), bucket[d].end());   // 桶内按数值升序
        for (int x : bucket[d]) {
            printf("%s%d", first ? "" : " ", x);
            first = false;
        }
    }
    printf("\n");
    return 0;
}
''',
  ["排序", "个位", "比较器"])

A("【排序】快速排序递归实现", SEC_SORT, 3,
  stmt("用快速排序（以第一个元素为基准）把数组排成升序并输出。",
       ["划分：把小于基准的放左边、大于等于的放右边",
        "边界取 `(l, p-1)` 和 `(p+1, r)`，别写成 `(l, p)` 否则死循环",
        "输出一行"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：升序结果。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases("5\n5 3 1 4 2", "1\n7", "4\n1 1 1 1", "5\n5 4 3 2 1",
                barr(28, 10), barr(29, 12, -10, 10)),
  _quick_sort,
  r'''#include <cstdio>
void qsort2(int a[], int l, int r) {
    if (l >= r) return;
    int p = a[l], i = l, j = r;
    while (i < j) {
        while (i < j && a[j] >= p) j--;
        a[i] = a[j];
        while (i < j && a[i] <= p) i++;
        a[j] = a[i];
    }
    a[i] = p;                              // 基准归位
    qsort2(a, l, i - 1);
    qsort2(a, i + 1, r);
}
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    qsort2(a, 0, n - 1);
    for (int i = 0; i < n; i++) printf("%d%c", a[i], i + 1 == n ? '\n' : ' ');
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    std::sort(a, a + n);                   // 库里的 introsort
    for (int i = 0; i < n; i++) printf("%d%c", a[i], i + 1 == n ? '\n' : ' ');
    return 0;
}
''',
  ["排序", "快排", "划分"])

A("【查找】线性查找与二分查找的比较次数", SEC_SORT, 2,
    stmt("数组升序。读入 `n x` 和 `n` 个整数，分别用线性查找和二分查找找 `x`，"
         "输出两种方法各自的比较次数（线性查找找不到时比较了 `n` 次）。",
         ["线性查找从头比到尾，找到 `x` 时比较次数就是它的位置",
          "二分查找每轮比较一次 `mid`",
          "输出一行两个整数"]),
    "第一行 `n x`；第二行 `n` 个升序整数。",
    "一行：`线性比较次数 二分比较次数`。",
    "- 1 ≤ n ≤ 1000\n- |x|, |a[i]| ≤ 10⁶",
    lambda: cases("5 3\n1 3 5 7 9", "5 9\n1 3 5 7 9", "5 100\n1 3 5 7 9", "1 1\n1",
                  "7 1\n1 3 5 7 9 11 13", "4 2\n1 2 3 4"),
    _count_cmp,
    r'''#include <cstdio>
int main() {
    int n, x;
    if (scanf("%d %d", &n, &x) != 2) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int lin = n, bc = 0;                    // 找不到时线性比较 n 次
    for (int i = 0; i < n; i++) if (a[i] == x) { lin = i + 1; break; }
    int lo = 0, hi = n - 1;
    while (lo <= hi) {
        int mid = (lo + hi) / 2;
        bc++;
        if (a[mid] == x) break;
        if (a[mid] < x) lo = mid + 1; else hi = mid - 1;
    }
    printf("%d %d\n", lin, bc);
    return 0;
}
''',
    r'''#include <cstdio>
#include <algorithm>
int main() {
    int n, x;
    if (scanf("%d %d", &n, &x) != 2) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int *p = std::lower_bound(a, a + n, x);
    int lin = (p != a + n && *p == x) ? (int)(p - a) + 1 : n;
    int bc = 0, lo = 0, hi = n - 1;
    while (lo <= hi) {
        int mid = (lo + hi) / 2;
        bc++;
        if (a[mid] == x) break;
        if (a[mid] < x) lo = mid + 1; else hi = mid - 1;
    }
    printf("%d %d\n", lin, bc);
    return 0;
}
''',
    ["查找", "线性", "二分"])

A("【排序】排序后求众数", SEC_SORT, 2,
    stmt("读入 `n` 个整数，输出出现次数最多的值；并列时输出**最小**的那个。",
         ["先排序，相同的值会连成一段，扫一遍数每段长度",
          "也可以直接统计频次再取最大（并列取最小）",
          "输出一个整数"]),
    "第一行 `n`，第二行 `n` 个整数。",
    "一行：众数。",
    "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
    lambda: cases("5\n1 2 2 3 3", "3\n5 5 5", "1\n7", "6\n4 4 2 2 3 3",
                  barr(30, 10, 1, 3), barr(31, 12, -2, 2)),
    _mode,
    r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    std::sort(a, a + n);
    int bestV = a[0], bestC = 0;
    for (int i = 0; i < n;) {
        int j = i;
        while (j < n && a[j] == a[i]) j++;
        if (j - i > bestC) { bestC = j - i; bestV = a[i]; }   // 严格大于才换，并列留最小
        i = j;
    }
    printf("%d\n", bestV);
    return 0;
}
''',
    r'''#include <cstdio>
#include <map>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    std::map<int, int> cnt;
    for (int i = 0; i < n; i++) { int x; scanf("%d", &x); cnt[x]++; }
    int bv = 0, bc = -1;
    for (auto &kv : cnt)                  // map 按 key 升序，先遇到的就是小的
        if (kv.second > bc) { bc = kv.second; bv = kv.first; }
    printf("%d\n", bv);
    return 0;
}
''',
    ["排序", "众数", "频次"])

# ===================================================================== #
#  SEC_GRD · 贪心（20 题）
# ===================================================================== #

def _ivs(t: str):
    ln = [x.split() for x in t.strip().splitlines()]
    n = int(ln[0][0])
    return [(int(r[0]), int(r[1])) for r in ln[1:1 + n]]


def _act_sel(t: str) -> str:
    """最多不重叠区间：用 DP 求（独立于贪心）。"""
    iv = sorted(_ivs(t), key=lambda p: p[1])
    n = len(iv)
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if iv[j][1] <= iv[i][0]:
                dp[i] = max(dp[i], dp[j] + 1)
    return "%d\n" % max(dp)


def _min_points(t: str) -> str:
    """区间选点：暴力枚举端点子集。"""
    iv = _ivs(t)
    cand = sorted({x for p in iv for x in p})
    for k in range(1, len(cand) + 1):
        for sel in itertools.combinations(cand, k):
            if all(any(p[0] <= s <= p[1] for s in sel) for p in iv):
                return "%d\n" % k
    return "%d\n" % len(cand)


def _change(t: str) -> str:
    """找零钱最少张数：DP。"""
    amount = int(t.strip())
    coins = [100, 25, 10, 5, 1]
    dp = [0] + [10 ** 9] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] = min(dp[a], dp[a - c] + 1)
    return "%d\n" % dp[amount]


def _frac_knap(t: str) -> str:
    """分数背包：枚举所有取用顺序，取最优（验证「按性价比」确实最优）。"""
    tok = t.split()
    n, cap = int(tok[0]), int(tok[1])
    items = [(int(tok[2 + 2 * i]), int(tok[3 + 2 * i])) for i in range(n)]
    best = 0.0
    for perm in itertools.permutations(range(n)):
        left, val = cap, 0.0
        for i in perm:
            w, v = items[i]
            take = min(left, w)
            val += v * take / w
            left -= take
            if left == 0:
                break
        best = max(best, val)
    return "%.2f\n" % best


def _merge_fruit(t: str) -> str:
    """合并果子：暴力枚举所有合并顺序，取最小总代价。"""
    v = tuple(arr_of(t))
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def go(state):
        if len(state) <= 1:
            return 0
        best = None
        m = len(state)
        for i in range(m):
            for j in range(i + 1, m):
                rest = list(state)
                b = rest.pop(j)
                a = rest.pop(i)
                nxt = tuple(sorted(rest + [a + b]))
                r = a + b + go(nxt)
                if best is None or r < best:
                    best = r
        return best
    return "%d\n" % go(tuple(sorted(v)))


def _queue_water(t: str) -> str:
    """排队接水总等待：枚举排列取最小。"""
    v = arr_of(t)
    best = None
    for perm in itertools.permutations(v):
        s, total = 0, 0
        for x in perm:
            total += s
            s += x
        if best is None or total < best:
            best = total
    return "%d\n" % best


def _jump(t: str) -> str:
    """跳跃游戏最少步数：BFS。"""
    v = arr_of(t)
    n = len(v)
    dist = {0: 0}
    q = [0]
    while q:
        nq = []
        for i in q:
            for j in range(i + 1, min(n - 1, i + v[i]) + 1):
                if j not in dist:
                    dist[j] = dist[i] + 1
                    nq.append(j)
        q = nq
    return "%d\n" % dist[n - 1]


def _gas(t: str) -> str:
    """加油站：暴力试每个起点。"""
    ln = [x.split() for x in t.strip().splitlines()]
    n = int(ln[0][0])
    g = [(int(r[0]), int(r[1])) for r in ln[1:1 + n]]
    for s in range(n):
        tank, ok = 0, True
        for k in range(n):
            i = (s + k) % n
            tank += g[i][0] - g[i][1]
            if tank < 0:
                ok = False
                break
        if ok:
            return "%d\n" % (s + 1)
    return "-1\n"


def _rooms(t: str) -> str:
    """最少会议室：半开区间 [l, r)，数每个时刻有多少会议覆盖（结束时刻房间即可复用）。"""
    iv = _ivs(t)
    best = 0
    for p in {x for s in iv for x in s}:
        c = sum(1 for l, r in iv if l <= p < r)
        best = max(best, c)
    return "%d\n" % best


def _max_num(t: str) -> str:
    """最大数拼接：枚举全排列取最大。"""
    v = [str(x) for x in arr_of(t)]
    return max("".join(p) for p in itertools.permutations(v)) + "\n"


def _cookies(t: str) -> str:
    """分饼干：暴力二分图匹配。"""
    tok = toks(t)
    n = tok[0]
    g = tok[1:1 + n]
    m = tok[1 + n]
    s = tok[2 + n:2 + n + m]
    match = [-1] * m

    def try_kid(k, seen):
        for j in range(m):
            if s[j] >= g[k] and not seen[j]:
                seen[j] = True
                if match[j] == -1 or try_kid(match[j], seen):
                    match[j] = k
                    return True
        return False
    c = 0
    for k in range(n):
        if try_kid(k, [False] * m):
            c += 1
    return "%d\n" % c


def _non_overlap(t: str) -> str:
    iv = sorted(_ivs(t), key=lambda p: p[1])
    n = len(iv)
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if iv[j][1] <= iv[i][0]:
                dp[i] = max(dp[i], dp[j] + 1)
    return "%d\n" % (n - max(dp))


def _stock1(t: str) -> str:
    v = arr_of(t)
    best = 0
    for i in range(len(v)):
        for j in range(i + 1, len(v)):
            best = max(best, v[j] - v[i])
    return "%d\n" % best


def _stock2(t: str) -> str:
    v = arr_of(t)
    cash, hold = 0, -10 ** 18
    for p in v:
        cash, hold = max(cash, hold + p), max(hold, cash - p)
    return "%d\n" % cash


def _del_digits(t: str) -> str:
    ln = [x.strip() for x in t.strip().splitlines()]
    s, k = ln[0], int(ln[1])
    if k >= len(s):
        return "0\n"
    best = None
    for keep in itertools.combinations(range(len(s)), len(s) - k):
        cand = "".join(s[i] for i in keep).lstrip("0") or "0"
        if best is None or (len(cand), cand) < (len(best), best):
            best = cand
    return best + "\n"


def _tian(t: str) -> str:
    tok = toks(t)
    n = tok[0]
    a = tok[1:1 + n]
    b = tok[1 + n:1 + 2 * n]
    best = -1
    for perm in itertools.permutations(a):
        w = sum(1 for x, y in zip(perm, b) if x > y)
        best = max(best, w)
    return "%d\n" % best


def _missile(t: str) -> str:
    v = arr_of(t)
    n = len(v)
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if v[j] >= v[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return "%d\n" % max(dp)


def _boxes(t: str) -> str:
    v = arr_of(t)
    left = []
    for sz in v:
        for i in range(len(left)):
            if left[i] >= sz:
                left[i] -= sz
                break
        else:
            left.append(100 - sz)
    return "%d\n" % len(left)


def _bulbs(t: str) -> str:
    ln = [x.split() for x in t.strip().splitlines()]
    n, m = int(ln[0][0]), int(ln[0][1])
    diff = [0] * (n + 2)
    for r in ln[1:1 + m]:
        l, rr = int(r[0]), int(r[1])
        diff[l] += 1
        diff[rr + 1] -= 1
    cur = lit = 0
    for i in range(1, n + 1):
        cur += diff[i]
        if cur % 2:
            lit += 1
    return "%d\n" % lit


def _seq_range(t: str) -> str:
    v = arr_of(t)

    def best(state, want_max):
        if len(state) == 1:
            return state[0]
        res = None
        m = len(state)
        for i in range(m):
            for j in range(i + 1, m):
                rest = list(state)
                b = rest.pop(j)
                a = rest.pop(i)
                rest.append(a * b + 1)
                r = best(tuple(rest), want_max)
                res = r if res is None else (max(res, r) if want_max else min(res, r))
        return res
    hi = best(tuple(sorted(v)), True)
    lo = best(tuple(sorted(v)), False)
    return "%d\n" % (hi - lo)


A("【贪心】活动选择（最多不重叠区间）", SEC_GRD, 2,
  stmt("读入 `n` 个时间段 `[l, r]`，一个人最多能参加多少个**互不重叠**的活动？"
       "（一个活动结束的时刻等于下一个开始的时刻，算不重叠）",
       ["按**结束时间**升序排，能接上就选 —— 按开始时间排是错的",
        "贪心的正确性靠「交换论证」：任何最优解都能换成以最早结束者打头",
        "输出一个整数"]),
  "第一行 `n`；之后 `n` 行，每行 `l r`。",
  "一行：最多能参加的活动数。",
  "- 1 ≤ n ≤ 1000\n- 0 ≤ l < r ≤ 10⁶",
  lambda: cases("3\n1 3\n2 4\n3 5", "1\n1 2", "3\n1 2\n2 3\n3 4", "3\n1 10\n2 3\n4 5",
                "4\n0 1\n1 2\n2 3\n3 4", "5\n5 9\n1 2\n3 4\n6 7\n8 10"),
  _act_sel,
  r'''#include <cstdio>
#include <algorithm>
struct Seg { int l, r; };
bool cmp(const Seg &a, const Seg &b) { return a.r < b.r; }   // 按结束时间排
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static Seg v[1005];
    for (int i = 0; i < n; i++) scanf("%d %d", &v[i].l, &v[i].r);
    std::sort(v, v + n, cmp);
    int cnt = 0, last = -1;
    for (int i = 0; i < n; i++)
        if (v[i].l >= last) { cnt++; last = v[i].r; }   // 能接上就选
    printf("%d\n", cnt);
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int n, L[1005], R[1005];
int dp[1005];
int main() {
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    for (int i = 0; i < n; i++) scanf("%d %d", &L[i], &R[i]);
    static int idx[1005];
    for (int i = 0; i < n; i++) idx[i] = i;
    std::sort(idx, idx + n, [&](int x, int y) { return R[x] < R[y]; });
    int best = 1;
    for (int k = 0; k < n; k++) {
        int i = idx[k];
        dp[k] = 1;
        for (int p = 0; p < k; p++) {
            int j = idx[p];
            if (R[j] <= L[i] && dp[p] + 1 > dp[k]) dp[k] = dp[p] + 1;
        }
        if (dp[k] > best) best = dp[k];
    }
    printf("%d\n", best);       // DP 版：不依赖贪心假设
    return 0;
}
''',
  ["贪心", "活动选择", "区间"])

A("【贪心】区间选点（最少点数覆盖所有区间）", SEC_GRD, 3,
  stmt("读入 `n` 个闭区间，在数轴上选尽量少的点，使每个区间里**至少有一个**被选中的点。"
       "输出最少的点数。",
       ["按右端点升序排；当前区间还没被覆盖时，就把点放在它的**右端点**",
        "点放在右端点最「贪」—— 能同时盖住后面尽可能多的区间",
        "输出一个整数"]),
  "第一行 `n`；之后 `n` 行，每行 `l r`。",
  "一行：最少点数。",
  "- 1 ≤ n ≤ 1000\n- 0 ≤ l ≤ r ≤ 10⁶",
  lambda: cases("3\n1 3\n2 4\n5 6", "1\n0 0", "2\n1 1\n1 1", "3\n1 2\n3 4\n5 6",
                "3\n1 10\n2 3\n4 5", "2\n1 5\n5 9"),
  _min_points,
  r'''#include <cstdio>
#include <algorithm>
struct Seg { int l, r; };
bool cmp(const Seg &a, const Seg &b) { return a.r < b.r; }
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static Seg v[1005];
    for (int i = 0; i < n; i++) scanf("%d %d", &v[i].l, &v[i].r);
    std::sort(v, v + n, cmp);
    int cnt = 0, last = -1;
    for (int i = 0; i < n; i++) {
        if (last >= v[i].l && last <= v[i].r) continue;   // 已被盖住
        cnt++;
        last = v[i].r;                                    // 点放右端点
    }
    printf("%d\n", cnt);
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
struct Seg { int l, r; };
bool cmpL(const Seg &a, const Seg &b) { return a.l > b.l; }   // 按左端点降序
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static Seg v[1005];
    for (int i = 0; i < n; i++) scanf("%d %d", &v[i].l, &v[i].r);
    std::sort(v, v + n, cmpL);
    int cnt = 0, last = -1;      // 从右往左，点放左端点
    for (int i = 0; i < n; i++) {
        if (last <= v[i].r && last >= v[i].l) continue;
        cnt++;
        last = v[i].l;
    }
    printf("%d\n", cnt);
    return 0;
}
''',
  ["贪心", "区间选点"])

A("【贪心】找零钱最少张数", SEC_GRD, 2,
  stmt("纸币面值为 100、25、10、5、1，读入金额 `x`，输出凑出 `x` 需要的最少张数。",
       ["这套面值满足「每个面值都是前一个的约数或更大」，贪心（先用大面值）恰好最优",
        "如果面值是 1、3、4 这类，贪心就**不**最优了 —— 那时必须 DP",
        "输出一个整数"]),
  "一行一个整数 `x`。",
  "一行：最少张数。",
  "- 0 ≤ x ≤ 10⁶",
  lambda: cases("0", "1", "30", "99", "100", "12345"),
  _change,
  r'''#include <cstdio>
int main() {
    int x;
    if (scanf("%d", &x) != 1) return 0;
    int coin[5] = {100, 25, 10, 5, 1}, cnt = 0;
    for (int i = 0; i < 5; i++) { cnt += x / coin[i]; x %= coin[i]; }   // 先用大的
    printf("%d\n", cnt);
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int dp[1000005];
int main() {
    int x;
    if (scanf("%d", &x) != 1) return 0;
    int coin[5] = {100, 25, 10, 5, 1};
    dp[0] = 0;
    for (int a = 1; a <= x; a++) {
        dp[a] = 1 << 30;
        for (int k = 0; k < 5; k++)
            if (coin[k] <= a) dp[a] = std::min(dp[a], dp[a - coin[k]] + 1);
    }
    printf("%d\n", dp[x]);      // DP 版：换面值也不会错
    return 0;
}
''',
  ["贪心", "找零", "DP"])

A("【贪心】分数背包", SEC_GRD, 4,
  stmt("有 `n` 件物品，每件有重量和价值，背包容量为 `w`。物品**可以切开**拿走一部分，"
       "价值按比例计算。求能装下的最大总价值，保留 2 位小数。",
       ["按「单位重量价值」降序取，直到装满 —— 分数背包是贪心能保证最优的少数情况之一",
        "比较 `v1/w1` 与 `v2/w2` 时用交叉相乘 `v1*w2 > v2*w1`，避免浮点误差",
        "输出一行，两位小数"]),
  "第一行 `n w`；之后 `n` 行，每行 `重量 价值`。",
  "一行：最大总价值（2 位小数）。",
  "- 1 ≤ n ≤ 5\n- 1 ≤ w ≤ 1000\n- 1 ≤ 重量 ≤ 100\n- 1 ≤ 价值 ≤ 1000",
  lambda: cases("2 50\n10 60\n20 100", "1 5\n10 100", "2 10\n10 10\n10 20",
                "3 30\n10 60\n20 100\n15 90", "1 100\n100 1",
                "4 50\n10 10\n20 30\n30 40\n40 50"),
  _frac_knap,
  r'''#include <cstdio>
#include <algorithm>
struct Item { int w, v; };
bool cmp(const Item &a, const Item &b) {
    return (long long)a.v * b.w > (long long)b.v * a.w;   // 交叉相乘比性价比
}
int main() {
    int n, cap;
    if (scanf("%d %d", &n, &cap) != 2) return 0;
    static Item it[10];
    for (int i = 0; i < n; i++) scanf("%d %d", &it[i].w, &it[i].v);
    std::sort(it, it + n, cmp);
    double ans = 0;
    int left = cap;
    for (int i = 0; i < n && left > 0; i++) {
        int take = it[i].w < left ? it[i].w : left;       // 能拿多少拿多少
        ans += (double)it[i].v * take / it[i].w;
        left -= take;
    }
    printf("%.2f\n", ans);
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
struct Item { int w, v; double r; };
bool cmpRatio(const Item &a, const Item &b) { return a.r > b.r; }
int main() {
    int n, cap;
    if (scanf("%d %d", &n, &cap) != 2) return 0;
    static Item it[10];
    for (int i = 0; i < n; i++) {
        scanf("%d %d", &it[i].w, &it[i].v);
        it[i].r = (double)it[i].v / it[i].w;              // 直接用浮点比值
    }
    std::sort(it, it + n, cmpRatio);
    double ans = 0; int left = cap;
    for (int i = 0; i < n && left > 0; i++) {
        int take = std::min(it[i].w, left);
        ans += it[i].r * take;
        left -= take;
    }
    printf("%.2f\n", ans);
    return 0;
}
''',
  ["贪心", "分数背包", "性价比"])

A("【贪心】合并果子", SEC_GRD, 3,
  stmt("有 `n` 堆果子，每次把两堆合并成一堆，花费的体力等于两堆重量之和。"
       "把所有堆合并成一堆的最小总体力是多少？",
       ["每次都挑**最轻的两堆**合并（哈夫曼思想），用最小堆维护",
        "`priority_queue<int, vector<int>, greater<int>>` 才是小顶堆，默认是大顶堆",
        "输出一个整数"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：最小总体力。",
  "- 1 ≤ n ≤ 1000\n- 1 ≤ 重量 ≤ 1000",
  lambda: cases("3\n1 2 3", "1\n5", "4\n1 1 1 1", "5\n3 1 4 1 5",
                "3\n10 20 30", "6\n2 3 4 5 6 7"),
  _merge_fruit,
  r'''#include <cstdio>
#include <queue>
#include <vector>
#include <functional>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    std::priority_queue<int, std::vector<int>, std::greater<int>> pq;   // 小顶堆
    for (int i = 0; i < n; i++) { int x; scanf("%d", &x); pq.push(x); }
    long long cost = 0;
    while (pq.size() > 1) {
        int a = pq.top(); pq.pop();
        int b = pq.top(); pq.pop();
        cost += a + b;
        pq.push(a + b);
    }
    printf("%lld\n", cost);
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    std::sort(a, a + n);               // 有序数组，每次取前两个
    long long cost = 0;
    int len = n;
    while (len > 1) {
        int s = a[0] + a[1];
        cost += s;
        for (int i = 2; i < len; i++) a[i - 2] = a[i];   // 前移两位
        len -= 2;
        int pos = len;
        for (int i = 0; i < len; i++) if (a[i] > s) { pos = i; break; }   // 插入
        for (int i = len; i > pos; i--) a[i] = a[i - 1];
        a[pos] = s;
        len++;
    }
    printf("%lld\n", cost);
    return 0;
}
''',
  ["贪心", "哈夫曼", "优先队列"])

A("【贪心】排队接水总等待时间", SEC_GRD, 3,
  stmt("`n` 个人排队接水，第 `i` 个人需要 `t[i]` 时间。合理安排顺序，使所有人的"
       "**等待时间之和**最小，输出这个最小值（第一个人的等待时间为 0）。",
       ["按接水时间**从短到长**排，短的先来，后面的人少等",
        "总等待时间 = `n-1` 个 `t1` + `n-2` 个 `t2` + …，可以用前缀和累加",
        "输出一个整数"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：最小总等待时间。",
  "- 1 ≤ n ≤ 6\n- 1 ≤ t[i] ≤ 100",
  lambda: cases("3\n3 1 2", "1\n5", "4\n4 3 2 1", "2\n10 1",
                "3\n10 10 10", "5\n5 4 3 2 1"),
  _queue_water,
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int t[15];
    for (int i = 0; i < n; i++) scanf("%d", &t[i]);
    std::sort(t, t + n);              // 短的先接
    long long wait = 0, pre = 0;
    for (int i = 0; i < n; i++) { wait += pre; pre += t[i]; }   // 前缀和累加
    printf("%lld\n", wait);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int t[15], cnt[105] = {0};
    for (int i = 0; i < n; i++) { scanf("%d", &t[i]); cnt[t[i]]++; }
    long long wait = 0, pre = 0, done = 0;
    for (int v = 1; v <= 100; v++)          // 计数排序代替 std::sort
        for (int k = 0; k < cnt[v]; k++) {
            wait += pre;
            pre += v;
            done++;
        }
    printf("%lld\n", wait);
    (void)done;
    return 0;
}
''',
  ["贪心", "排队", "前缀和"])

A("【贪心】跳跃游戏最少步数", SEC_GRD, 4,
  stmt("数组 `a`，从下标 0 出发，站在 `i` 时最多能跳到 `i + a[i]`。求跳到最后一个下标的"
       "**最少步数**（保证能到达）。",
       ["按「层」扩展：当前层的可达范围是 `[0, curEnd]`，走一步后范围扩到 `[0, nextEnd]`",
        "每扩一次层，步数加 1；`curEnd` 到 `i` 时才换层",
        "输出一个整数"]),
  "第一行 `n`，第二行 `n` 个非负整数。",
  "一行：最少步数。",
  "- 1 ≤ n ≤ 1000\n- 0 ≤ a[i] ≤ 100",
  lambda: cases("5\n2 3 1 1 4", "1\n0", "3\n1 1 1", "5\n1 2 3 4 5",
                "4\n2 0 1 1", "6\n1 1 2 1 1 1"),
  _jump,
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int steps = 0, curEnd = 0, far = 0;
    for (int i = 0; i < n - 1; i++) {
        if (i + a[i] > far) far = i + a[i];      // 本层能到的最远处
        if (i == curEnd) { steps++; curEnd = far; }   // 换层
    }
    printf("%d\n", steps);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005], dp[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    for (int i = 1; i < n; i++) dp[i] = 1 << 30;    // DP：从哪跳过来最省
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j <= i + a[i] && j < n; j++)
            if (dp[i] + 1 < dp[j]) dp[j] = dp[i] + 1;
    printf("%d\n", dp[n - 1]);
    return 0;
}
''',
  ["贪心", "跳跃游戏", "BFS"])

A("【贪心】加油站绕行起点", SEC_GRD, 4,
  stmt("`n` 个加油站围成一圈，第 `i` 站能加 `gas[i]` 升油，到下一站要消耗 `cost[i]` 升。"
       "油箱初始为空。输出能绕行一圈的起点编号（从 1 开始）；无解输出 `-1`。",
       ["先看总油量：`sum(gas) < sum(cost)` 必然无解",
        "有解时，从某个点开始的累计油量一旦变负，说明之前所有点都不可能是起点，直接跳到下一点",
        "输出一个整数"]),
  "第一行 `n`；之后 `n` 行，每行 `gas cost`。",
  "一行：起点编号或 `-1`。",
  "- 1 ≤ n ≤ 1000\n- 0 ≤ gas, cost ≤ 10⁶",
  lambda: cases("3\n1 2\n2 3\n3 4", "1\n5 3", "1\n3 5", "2\n2 3\n3 4",
                "4\n4 5\n5 4\n3 3\n2 4", "3\n0 1\n0 1\n2 1"),
  _gas,
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static long long gas[1005], cost[1005];
    long long total = 0, tank = 0;
    int start = 0;
    for (int i = 0; i < n; i++) {
        scanf("%lld %lld", &gas[i], &cost[i]);
        total += gas[i] - cost[i];
        tank += gas[i] - cost[i];
        if (tank < 0) { start = i + 1; tank = 0; }   // 之前都不可能是起点
    }
    printf("%d\n", total < 0 ? -1 : start + 1);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static long long gas[1005], cost[1005];
    for (int i = 0; i < n; i++) scanf("%lld %lld", &gas[i], &cost[i]);
    for (int s = 0; s < n; s++) {          // 暴力试每个起点
        long long tank = 0;
        bool ok = true;
        for (int k = 0; k < n; k++) {
            int i = (s + k) % n;
            tank += gas[i] - cost[i];
            if (tank < 0) { ok = false; break; }
        }
        if (ok) { printf("%d\n", s + 1); return 0; }
    }
    printf("-1\n");
    return 0;
}
''',
  ["贪心", "加油站", "环"])

A("【贪心】最少会议室", SEC_GRD, 3,
  stmt("读入 `n` 个会议时间段 `[l, r]`，同一时刻一个会议室只能开一个会，"
       "问最少需要几个会议室（输出任意时刻的最大重叠数）。",
       ["答案是「任意时刻同时进行的会议数的最大值」",
        "区间按**半开**算：`[0,5)` 与 `[5,10)` 不冲突，前一散场房间立刻能给后一场用",
        "把开始和结束分别排序，用双指针扫：开始就 +1，结束就 -1",
        "输出一个整数"]),
  "第一行 `n`；之后 `n` 行，每行 `l r`。",
  "一行：最少会议室数。",
  "- 1 ≤ n ≤ 1000\n- 0 ≤ l < r ≤ 10⁶",
  lambda: cases("3\n0 30\n5 10\n15 20", "1\n0 1", "2\n0 5\n5 10", "3\n0 10\n1 2\n3 4",
                "4\n0 1\n0 1\n0 1\n0 1", "3\n1 5\n2 6\n3 7"),
  _rooms,
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int L[1005], R[1005];
    for (int i = 0; i < n; i++) scanf("%d %d", &L[i], &R[i]);
    std::sort(L, L + n);
    std::sort(R, R + n);
    int i = 0, j = 0, cur = 0, best = 0;
    while (i < n) {
        if (L[i] < R[j]) { cur++; if (cur > best) best = cur; i++; }   // 开始
        else { cur--; j++; }                                           // 结束
    }
    printf("%d\n", best);
    return 0;
}
''',
  r'''#include <cstdio>
#include <map>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    std::map<int, int> ev;                 // 扫描线：+1 开始、-1 结束
    for (int i = 0; i < n; i++) {
        int l, r;
        scanf("%d %d", &l, &r);
        ev[l] += 1;
        ev[r] -= 1;
    }
    int cur = 0, best = 0;
    for (auto &kv : ev) { cur += kv.second; if (cur > best) best = cur; }
    printf("%d\n", best);
    return 0;
}
''',
  ["贪心", "扫描线", "会议室"])

A("【贪心】拼接最大数", SEC_GRD, 4,
  stmt("读入 `n` 个正整数，把它们按某种顺序拼成一个最长的数字串（位数固定，就是字典序最大），"
       "输出这个数。",
       ["排序规则不是「谁大谁前」，而是 `a+b > b+a` 时 a 排前面",
        "比较要按**字符串拼接**比，不能按数值比：`9` 和 `91`，9 在前得 991 更大",
        "输出一行"]),
  "第一行 `n`，第二行 `n` 个正整数。",
  "一行：拼接出的最大数。",
  "- 1 ≤ n ≤ 6\n- 1 ≤ 数值 ≤ 10⁶",
  lambda: cases("3\n9 91 1", "1\n5", "2\n12 121", "3\n3 30 34",
                "3\n1 2 3", "4\n10 2 9 39"),
  _max_num,
  r'''#include <cstdio>
#include <string>
#include <algorithm>
bool cmp(const std::string &a, const std::string &b) {
    return a + b > b + a;              // 拼起来比较，不是直接比大小
}
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    std::string v[10];
    for (int i = 0; i < n; i++) { int x; scanf("%d", &x); v[i] = std::to_string(x); }
    std::sort(v, v + n, cmp);
    for (int i = 0; i < n; i++) printf("%s", v[i].c_str());
    printf("\n");
    return 0;
}
''',
  r'''#include <cstdio>
#include <cstring>
char s[10][32];
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    for (int i = 0; i < n; i++) { int x; scanf("%d", &x); snprintf(s[i], 32, "%d", x); }
    for (int i = 0; i < n - 1; i++)          // 手写冒泡 + 拼接比较
        for (int j = 0; j < n - 1 - i; j++) {
            char ab[64], ba[64];
            snprintf(ab, 64, "%s%s", s[j], s[j + 1]);
            snprintf(ba, 64, "%s%s", s[j + 1], s[j]);
            if (strcmp(ab, ba) < 0) {
                char t[32];
                strcpy(t, s[j]); strcpy(s[j], s[j + 1]); strcpy(s[j + 1], t);
            }
        }
    for (int i = 0; i < n; i++) printf("%s", s[i]);
    printf("\n");
    return 0;
}
''',
  ["贪心", "拼接", "比较器"])

A("【贪心】分饼干", SEC_GRD, 3,
  stmt("有 `n` 个孩子和 `m` 块饼干，孩子的胃口是 `g[i]`，饼干大小是 `s[j]`。"
       "一块饼干只能给一个孩子，且饼干大小不小于胃口才算满足。求最多能满足几个孩子。",
       ["两个数组都升序排，然后双指针：能喂就喂，喂不了就换更大的饼干",
        "小饼干先给胃口小的，避免浪费大饼干",
        "输入格式：第一行 `n`，第二行 `n` 个胃口；第三行 `m`，第四行 `m` 个饼干大小"]),
  "第一行 `n`；第二行 `n` 个整数；第三行 `m`；第四行 `m` 个整数。",
  "一行：最多满足的孩子数。",
  "- 1 ≤ n, m ≤ 6\n- 1 ≤ 胃口, 饼干 ≤ 100",
  lambda: cases("3\n1 2 3\n2\n1 1", "2\n1 2\n3\n1 2 3", "1\n5\n1\n4",
                "3\n10 20 30\n3\n10 20 30", "2\n5 5\n2\n5 5", "3\n1 2 3\n1\n2"),
  _cookies,
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n, m;
    if (scanf("%d", &n) != 1) return 0;
    static int g[15], s[15];
    for (int i = 0; i < n; i++) scanf("%d", &g[i]);
    if (scanf("%d", &m) != 1) return 0;
    for (int j = 0; j < m; j++) scanf("%d", &s[j]);
    std::sort(g, g + n);
    std::sort(s, s + m);
    int i = 0, j = 0, c = 0;
    while (i < n && j < m) {
        if (s[j] >= g[i]) { c++; i++; j++; }   // 喂得饱就配一对
        else j++;                              // 这块饼干废了
    }
    printf("%d\n", c);
    return 0;
}
''',
  r'''#include <cstdio>
#include <set>
int main() {
    int n, m;
    if (scanf("%d", &n) != 1) return 0;
    static int g[15];
    for (int i = 0; i < n; i++) scanf("%d", &g[i]);
    if (scanf("%d", &m) != 1) return 0;
    std::multiset<int> box;
    for (int j = 0; j < m; j++) { int x; scanf("%d", &x); box.insert(x); }
    int c = 0;
    for (int i = 0; i < n; i++) {
        auto it = box.lower_bound(g[i]);          // 找第一块够大的
        if (it != box.end()) { c++; box.erase(it); }
    }
    printf("%d\n", c);
    return 0;
}
''',
  ["贪心", "双指针", "匹配"])

A("【贪心】无重叠区间最少删除数", SEC_GRD, 3,
  stmt("读入 `n` 个区间，最少删掉几个才能让剩下的区间互不重叠？",
       ["等价于 `n - 最多能保留几个不重叠区间`",
        "按右端点排序，能接上就保留 —— 和「活动选择」是同一个问题换个问法",
        "输出一个整数"]),
  "第一行 `n`；之后 `n` 行，每行 `l r`。",
  "一行：最少删除数。",
  "- 1 ≤ n ≤ 1000\n- 0 ≤ l < r ≤ 10⁶",
  lambda: cases("3\n1 2\n2 3\n1 3", "1\n1 2", "4\n1 2\n2 3\n3 4\n1 3",
                "2\n1 2\n3 4", "3\n1 10\n2 3\n4 5", "2\n1 2\n1 2"),
  _non_overlap,
  r'''#include <cstdio>
#include <algorithm>
struct Seg { int l, r; };
bool cmp(const Seg &a, const Seg &b) { return a.r < b.r; }
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static Seg v[1005];
    for (int i = 0; i < n; i++) scanf("%d %d", &v[i].l, &v[i].r);
    std::sort(v, v + n, cmp);
    int keep = 0, last = -1;
    for (int i = 0; i < n; i++)
        if (v[i].l >= last) { keep++; last = v[i].r; }
    printf("%d\n", n - keep);        // 删掉的就是接不上的
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int L[1005], R[1005];
    for (int i = 0; i < n; i++) scanf("%d %d", &L[i], &R[i]);
    int keep = 0;                    // 暴力选：每轮找右端点最小的可选区间
    static bool used[1005] = {false};
    int last = -1;
    while (true) {
        int pick = -1;
        for (int i = 0; i < n; i++)
            if (!used[i] && L[i] >= last && (pick == -1 || R[i] < R[pick])) pick = i;
        if (pick == -1) break;
        used[pick] = true;
        keep++;
        last = R[pick];
    }
    printf("%d\n", n - keep);
    return 0;
}
''',
  ["贪心", "区间", "删除"])

A("【贪心】股票买卖一次最大利润", SEC_GRD, 2,
  stmt("给定每天的股价，只允许买卖**一次**（先买后卖），求最大利润；不能盈利时输出 0。",
       ["遍历时维护「到目前为止的最低买入价」，每天算一次「今天卖能赚多少」",
        "不要求最后一天卖，随时更新答案",
        "输出一个整数"]),
  "第一行 `n`，第二行 `n` 个整数股价。",
  "一行：最大利润。",
  "- 1 ≤ n ≤ 1000\n- 0 ≤ 股价 ≤ 10⁶",
  lambda: cases("5\n7 1 5 3 6", "5\n7 6 4 3 1", "1\n5", "2\n1 10",
                barr(40, 10), barr(41, 6, 0, 100)),
  _stock1,
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int p[1005];
    for (int i = 0; i < n; i++) scanf("%d", &p[i]);
    int low = p[0], best = 0;
    for (int i = 1; i < n; i++) {
        if (p[i] - low > best) best = p[i] - low;   // 今天卖
        if (p[i] < low) low = p[i];                 // 更新最低买入价
    }
    printf("%d\n", best);
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int p[1005];
    for (int i = 0; i < n; i++) scanf("%d", &p[i]);
    int cash = 0, hold = -1000000000;      // 状态机：空仓 / 持仓
    for (int i = 0; i < n; i++) {
        int nc = std::max(cash, hold + p[i]);   // 卖出
        int nh = std::max(hold, -p[i]);         // 买入（只允许一次）
        cash = nc; hold = nh;
    }
    printf("%d\n", cash);
    return 0;
}
''',
  ["贪心", "股票", "状态机"])

A("【贪心】股票买卖多次总利润", SEC_GRD, 2,
  stmt("给定每天的股价，允许**多次**买卖（同一天可以先卖再买，但手上最多一股），"
       "求能获得的最大总利润。",
       ["把所有「上涨的相邻差」加起来就是答案 —— 涨就持有，跌就空仓",
        "`p[i] > p[i-1]` 时累加 `p[i]-p[i-1]`",
        "输出一个整数"]),
  "第一行 `n`，第二行 `n` 个整数股价。",
  "一行：最大总利润。",
  "- 1 ≤ n ≤ 1000\n- 0 ≤ 股价 ≤ 10⁶",
  lambda: cases("5\n7 1 5 3 6", "5\n7 6 4 3 1", "1\n5", "2\n1 10",
                barr(42, 10), barr(43, 6, 0, 100)),
  _stock2,
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int p[1005];
    for (int i = 0; i < n; i++) scanf("%d", &p[i]);
    long long profit = 0;
    for (int i = 1; i < n; i++)
        if (p[i] > p[i - 1]) profit += p[i] - p[i - 1];   // 涨就赚这段
    printf("%lld\n", profit);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int p[1005];
    for (int i = 0; i < n; i++) scanf("%d", &p[i]);
    long long profit = 0;
    int i = 0;
    while (i < n - 1) {                     // 峰谷法：找每一段上升
        while (i < n - 1 && p[i + 1] <= p[i]) i++;
        int buy = p[i];
        while (i < n - 1 && p[i + 1] > p[i]) i++;
        profit += p[i] - buy;
    }
    printf("%lld\n", profit);
    return 0;
}
''',
  ["贪心", "股票", "峰谷"])

A("【贪心】删 k 位使剩下最小", SEC_GRD, 4,
  stmt("给定一个数字串和整数 `k`，删掉其中 `k` 个字符，使剩下的数字最小。"
       "输出剩下的数（去掉前导零；全删光输出 `0`）。",
       ["从左往右扫，一旦「当前位比后一位大」就删掉当前位 —— 用栈实现最自然",
        "扫完后如果还没删够，就从末尾继续删（此时串已非递减）",
        "输出一行"]),
  "第一行一个数字串，第二行整数 `k`。",
  "一行：剩下最小的数。",
  "- 1 ≤ 位数 ≤ 12\n- 0 ≤ k ≤ 位数",
  lambda: cases("1432219\n3", "10200\n1", "10\n2", "1234\n0",
                "4321\n2", "100200\n1"),
  _del_digits,
  r'''#include <cstdio>
#include <cstring>
int main() {
    char s[32], st[32];
    int k;
    if (scanf("%31s", s) != 1) return 0;
    if (scanf("%d", &k) != 1) return 0;
    int n = (int)strlen(s), top = 0;
    for (int i = 0; i < n; i++) {
        while (top > 0 && k > 0 && st[top - 1] > s[i]) { top--; k--; }   // 栈顶更大就弹
        st[top++] = s[i];
    }
    while (k > 0 && top > 0) { top--; k--; }        // 还得多删就从尾部删
    st[top] = '\0';
    int p = 0;
    while (p < top && st[p] == '0') p++;            // 去前导零
    if (p == top) printf("0\n");
    else printf("%s\n", st + p);
    return 0;
}
''',
  r'''#include <cstdio>
#include <cstring>
int main() {
    char s[32];
    int k;
    if (scanf("%31s", s) != 1) return 0;
    if (scanf("%d", &k) != 1) return 0;
    int n = (int)strlen(s);
    for (int t = 0; t < k; t++) {                   // 每轮删一个「峰」
        int i = 0;
        while (i + 1 < n && s[i] <= s[i + 1]) i++;
        for (int j = i; j + 1 < n; j++) s[j] = s[j + 1];   // 直接删掉 s[i]
        n--;
        if (n == 0) break;
    }
    s[n] = '\0';
    int p = 0;
    while (p < n && s[p] == '0') p++;
    if (p == n) printf("0\n");
    else printf("%s\n", s + p);
    return 0;
}
''',
  ["贪心", "删数", "单调栈"])

A("【贪心】田忌赛马", SEC_GRD, 4,
  stmt("田忌和齐王各有 `n` 匹马，速度分别是 `a[i]` 和 `b[i]`。每场各出一匹，快的赢。"
       "田忌知道齐王的出场顺序，可以任意安排自己的出场顺序，求最多能赢几场。",
       ["两边都排序，然后双指针：用自己最慢的马去「消耗」对方最快的马，或直接赢下对方最慢的",
        "能赢就赢（自己最慢 > 对方最慢）；不能赢就用自己最慢去换对方最快",
        "输入格式：第一行 `n`，第二行田忌的 `n` 匹，第三行齐王的 `n` 匹"]),
  "第一行 `n`；第二行 `n` 个整数；第三行 `n` 个整数。",
  "一行：最多胜场数。",
  "- 1 ≤ n ≤ 6\n- 1 ≤ 速度 ≤ 100",
  lambda: cases("3\n1 2 3\n1 2 3", "3\n3 2 1\n1 2 3", "1\n5\n4", "2\n10 10\n10 10",
                "3\n1 5 9\n2 6 8", "4\n1 2 3 4\n4 3 2 1"),
  _tian,
  r'''#include <cstdio>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[20], b[20];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    for (int i = 0; i < n; i++) scanf("%d", &b[i]);
    std::sort(a, a + n);
    std::sort(b, b + n);
    int i = 0, j = 0, win = 0;
    while (i < n && j < n) {
        if (a[i] > b[j]) { win++; i++; j++; }   // 我能赢对方最弱的，就先赢
        else i++;                               // 赢不了，这匹马废了
    }
    printf("%d\n", win);
    return 0;
}
''',
  r'''#include <cstdio>
#include <set>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int b[20];
    std::multiset<int> mine;
    for (int i = 0; i < n; i++) { int x; scanf("%d", &x); mine.insert(x); }
    for (int i = 0; i < n; i++) scanf("%d", &b[i]);
    int win = 0;
    for (int i = 0; i < n; i++) {                 // 对每匹敌马，找最小的能赢的马
        auto it = mine.upper_bound(b[i]);
        if (it != mine.end()) { win++; mine.erase(it); }
        else mine.erase(mine.begin());            // 赢不了就丢最小的
    }
    printf("%d\n", win);
    return 0;
}
''',
  ["贪心", "双指针", "田忌赛马"])

A("【贪心】导弹拦截（最长不上升子序列）", SEC_GRD, 4,
  stmt("读入 `n` 个导弹高度，一套拦截系统每次只能拦截高度**不高于**前一发的导弹。"
       "一套系统最多能拦下多少发（即最长不上升子序列长度）？",
       ["不是「最长下降」，而是「不上升」：相等也算接得上",
        "贪心 + 二分：维护一个「每条系统当前最低拦截高度」的序列，用 `upper_bound` 定位",
        "输出一个整数"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：最长不上升子序列长度。",
  "- 1 ≤ n ≤ 1000\n- 1 ≤ 高度 ≤ 30000",
  lambda: cases("8\n389 207 155 300 299 170 158 65", "1\n5", "3\n1 2 3",
                "3\n3 2 1", "5\n5 5 5 5 5", "6\n1 3 2 4 3 5"),
  _missile,
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int tails[1005];
    int len = 0;
    for (int i = 0; i < n; i++) {
        int x; scanf("%d", &x);
        int lo = 0, hi = len;               // 找第一个 tails[p] < x 的位置
        while (lo < hi) {
            int mid = (lo + hi) / 2;
            if (tails[mid] >= x) lo = mid + 1;
            else hi = mid;
        }
        tails[lo] = x;
        if (lo == len) len++;
    }
    printf("%d\n", len);
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int a[1005], dp[1005];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    int best = 1;
    for (int i = 0; i < n; i++) {
        dp[i] = 1;
        for (int j = 0; j < i; j++)
            if (a[j] >= a[i] && dp[j] + 1 > dp[i]) dp[i] = dp[j] + 1;   // 不上升
        if (dp[i] > best) best = dp[i];
    }
    printf("%d\n", best);
    return 0;
}
''',
  ["贪心", "LIS", "二分"])

A("【贪心】装箱问题（首次适应）", SEC_GRD, 3,
  stmt("箱子容量固定为 100，物品按给定顺序到达，每个物品放进**第一个装得下**的箱子"
       "（首次适应策略），装不下就开新箱。读入 `n` 和 `n` 个物品大小，输出用了几个箱子。",
       ["这题考的是「按规则模拟」，不是求最优装箱 —— 顺序会影响结果",
        "维护每个箱子的剩余空间，从左往右找第一个 `剩余 >= 物品` 的",
        "输出一个整数"]),
  "第一行 `n`，第二行 `n` 个整数（1 ≤ 大小 ≤ 100）。",
  "一行：箱子数。",
  "- 1 ≤ n ≤ 1000\n- 1 ≤ 大小 ≤ 100",
  lambda: cases("4\n60 40 30 30", "1\n100", "3\n100 100 100", "5\n10 20 30 40 50",
                "4\n50 60 50 60", "6\n30 30 30 30 30 30"),
  _boxes,
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int left[1005];
    int cnt = 0;
    for (int i = 0; i < n; i++) {
        int sz; scanf("%d", &sz);
        int placed = 0;
        for (int k = 0; k < cnt; k++)
            if (left[k] >= sz) { left[k] -= sz; placed = 1; break; }   // 首次适应
        if (!placed) { left[cnt++] = 100 - sz; }
    }
    printf("%d\n", cnt);
    return 0;
}
''',
  r'''#include <cstdio>
#include <vector>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    std::vector<int> left;                 // 只存剩余空间
    for (int i = 0; i < n; i++) {
        int sz; scanf("%d", &sz);
        for (size_t k = 0; k < left.size(); k++)
            if (left[k] >= sz) { left[k] -= sz; goto next; }
        left.push_back(100 - sz);
    next:;
    }
    printf("%d\n", (int)left.size());
    return 0;
}
''',
  ["贪心", "装箱", "模拟"])

A("【贪心】区间翻转后亮灯数", SEC_GRD, 3,
  stmt("`n` 盏灯初始全灭（编号 1~n）。进行 `m` 次操作，第 `i` 次把区间 `[l, r]` 内的灯"
       "状态全部翻转。输出最后亮着的灯数。",
       ["暴力逐个翻转是 O(nm)，用差分数组把每次操作降到 O(1)",
        "差分：`d[l] ^= 1`、`d[r+1] ^= 1`，最后求前缀「异或」就知道每盏灯的状态",
        "输出一个整数"]),
  "第一行 `n m`；之后 `m` 行，每行 `l r`。",
  "一行：亮着的灯数。",
  "- 1 ≤ n ≤ 1000\n- 1 ≤ m ≤ 1000\n- 1 ≤ l ≤ r ≤ n",
  lambda: cases("5 1\n1 3", "5 2\n1 3\n2 5", "1 1\n1 1", "4 3\n1 2\n3 4\n1 4",
                "6 2\n1 6\n1 6", "5 3\n1 1\n2 2\n3 3"),
  _bulbs,
  r'''#include <cstdio>
int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    static int d[1005];
    for (int i = 0; i < m; i++) {
        int l, r; scanf("%d %d", &l, &r);
        d[l] ^= 1;                      // 翻转区间的差分
        d[r + 1] ^= 1;
    }
    int cur = 0, lit = 0;
    for (int i = 1; i <= n; i++) {
        cur ^= d[i];                    // 前缀异或 = 当前灯的状态
        if (cur) lit++;
    }
    printf("%d\n", lit);
    return 0;
}
''',
  r'''#include <cstdio>
#include <map>
int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    std::map<int, int> ev;              // 事件点：在这里切换状态
    for (int i = 0; i < m; i++) {
        int l, r; scanf("%d %d", &l, &r);
        ev[l] ^= 1;
        ev[r + 1] ^= 1;
    }
    int cur = 0, lit = 0, prev = 1;
    for (auto &kv : ev) {
        if (cur) lit += kv.first - prev;   // 上一段是亮的
        cur ^= kv.second;
        prev = kv.first;
    }
    if (cur) lit += n + 1 - prev;
    printf("%d\n", lit);
    return 0;
}
''',
  ["贪心", "差分", "区间翻转"])

A("【贪心】数列极差", SEC_GRD, 4,
  stmt("给定 `n` 个正整数。每次操作取两个数 `a`、`b`，把它们删掉，加入 `a*b+1`，"
       "直到只剩一个数。不同的操作顺序会得到不同的结果，求「最大值 - 最小值」。",
       ["想要最大，每次都挑**最小**的两个乘（小数先乘，留大数最后放大）",
        "想要最小，每次都挑**最大**的两个乘",
        "输出一个整数"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：最大值与最小值之差。",
  "- 2 ≤ n ≤ 5\n- 1 ≤ 数值 ≤ 20",
  lambda: cases("3\n1 2 3", "2\n2 3", "3\n2 2 2", "4\n1 2 3 4",
                "3\n5 1 2", "5\n1 1 1 1 1"),
  _seq_range,
  r'''#include <cstdio>
#include <algorithm>
// 真·贪心：每轮重排后取指定的两个数合并（n<=5，直接排序足够）
long long greedy(int *src, int n, int wantMax) {
    long long v[20];
    for (int i = 0; i < n; i++) v[i] = src[i];
    int m = n;
    for (int step = 0; step < n - 1; step++) {
        std::sort(v, v + m);                     // 升序
        long long c;
        if (wantMax) {                           // 最大：取最小两个
            c = v[0] * v[1] + 1;
            v[0] = c;
            for (int t = 1; t < m - 1; t++) v[t] = v[t + 1];
        } else {                                 // 最小：取最大两个
            c = v[m - 1] * v[m - 2] + 1;
            v[m - 2] = c;
        }
        m--;
    }
    return v[0];
}
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n < 2) return 0;
    static int a[20];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    printf("%lld\n", greedy(a, n, 1) - greedy(a, n, 0));
    return 0;
}
''',
  r'''#include <cstdio>
long long go(long long *v, int n, int wantMax) {   // 暴力枚举所有操作顺序
    if (n == 1) return v[0];
    long long best = wantMax ? -1 : -1;
    bool first = true;
    long long tmp[20];
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++) {
            int k = 0;
            for (int t = 0; t < n; t++) if (t != i && t != j) tmp[k++] = v[t];
            tmp[k] = v[i] * v[j] + 1;
            long long r = go(tmp, k + 1, wantMax);
            if (first) { best = r; first = false; }
            else best = wantMax ? (r > best ? r : best) : (r < best ? r : best);
        }
    return best;
}
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n < 2) return 0;
    long long v[20], w[20];
    for (int i = 0; i < n; i++) { scanf("%lld", &v[i]); w[i] = v[i]; }
    printf("%lld\n", go(v, n, 1) - go(w, n, 0));
    return 0;
}
''',
  ["贪心", "极差", "排序"])


if __name__ == "__main__":
    sys.exit(cli(PROBLEMS, "app/problems_bank_cpp_basic7.py",
                 "第 7 册：排序与查找 / 贪心", "CPP_BASIC7_PROBLEMS"))
