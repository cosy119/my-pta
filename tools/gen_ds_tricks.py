# -*- coding: utf-8 -*-
"""C/C++ 技巧特训题库生成器 —— 「技巧特训 · C/C++」分节。

定位：数据结构讲义里没专门讲、但做题（蓝桥杯 / 码蹄杯 / ACM 风格）总会遇到的
STL 与算法套路，单独成章，量大、循序渐进（difficulty 1 → 4）。

每道题：
  title / section / difficulty / score / tags
  statement_md / input_format / output_format / constraints_md
  inputs   ← 测试点输入（手写或生成）
  samples  ← 前几个当样例
  oracle   ← 独立 Python 实现，算期望输出（用"笨办法"，与参考解不同路）
  solution / alt ← 两套 C++ 实现（verify_bank 双撞）

章节结构：
  STL 基础     7 题（vector push_back / string / sort+cmp / pair / map / set /
               stringstream）
  算法套路     7 题（upper_bound / lower_bound / 差分 / 双指针 / 单调栈 /
               单调队列 / 二分答案）
  竞赛强度     6 题（01 背包 / 完全背包 / LIS / LCS / 快速幂 / 逆序对）
  进阶套路    10 题（stable_sort 多关键字 / priority_queue Top-K /
               next_permutation / accumulate-iota / bitset 位统计 /
               unordered_map 词频 / unique 离散化 / 树状数组 /
               高精度加法 / 前缀和 + 哈希计数）
  插入维护     4 题（upper_bound + insert：单次插入 / 批量插入 /
               lower 与 upper 的稳定性差异 / 动态有序表名次查询）
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "app" / "problems_bank_ds_tricks.py"

PROBLEMS: list[dict] = []


def add(**kw) -> None:
    PROBLEMS.append(kw)


def _rand_big_case() -> str:
    """D10 的大用例：n = m1 = m2 = 1e5，固定种子可复现。"""
    import random
    rnd = random.Random(20261018)
    n = 100000
    m1 = 100000
    m2 = 100000
    lines = ["%d %d %d" % (n, m1, m2)]
    lines.append(" ".join(str(rnd.randint(-1000, 1000)) for _ in range(n)))
    for _ in range(m1):
        l = rnd.randint(1, n)
        r = rnd.randint(l, n)
        lines.append("1 %d %d %d" % (l, r, rnd.randint(-100, 100)))
    for _ in range(m2):
        lines.append("%d" % rnd.randint(1, n))
    return "\n".join(lines) + "\n"


def _rand_lis_case() -> str:
    """D17 的大用例：n = 3000。"""
    import random
    rnd = random.Random(7)
    n = 3000
    a = [rnd.randint(-10 ** 9, 10 ** 9) for _ in range(n)]
    return "%d\n%s\n" % (n, " ".join(map(str, a)))


def _rand_win_case() -> str:
    """D13 的大用例：n = 2000。"""
    import random
    rnd = random.Random(99)
    n = 2000
    k = 137
    a = [rnd.randint(0, 10 ** 9) for _ in range(n)]
    return "%d %d\n%s\n" % (n, k, " ".join(map(str, a)))


def _rand_inv_case() -> str:
    """D20 的大用例：n = 2000。"""
    import random
    rnd = random.Random(555)
    n = 2000
    a = [rnd.randint(-10 ** 9, 10 ** 9) for _ in range(n)]
    return "%d\n%s\n" % (n, " ".join(map(str, a)))


def _rand_knap_case() -> str:
    """D15 的大用例：n = 100, W = 10000。"""
    import random
    rnd = random.Random(314)
    n, W = 100, 10000
    lines = ["%d %d" % (n, W)]
    for _ in range(n):
        lines.append("%d %d" % (rnd.randint(1, 500), rnd.randint(0, 10000)))
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------- #
#  STL 基础（difficulty 1~2）
# --------------------------------------------------------------------- #

def _oracle_01(text: str) -> str:
    d = text.split()
    n = int(d[0])
    a = [int(v) for v in d[1:1 + n]]
    head = "%d\n" % n
    if n == 0:
        return head + "EMPTY\nEMPTY\n"
    rev = [a[n - 1 - k] for k in range(n)]
    return (head + "%d %d\n" % (max(a), min(a))
            + " ".join(map(str, rev)) + "\n")

add(
    title="vector 动态收集",
    section="技巧特训 · C/C++",
    difficulty=1, score=10, tags=["技巧特训", "vector", "push_back", "STL"],
    statement_md=(
        "读入 `n` 和 `n` 个整数（n 可为 0），用 `vector` 装下来，输出三行：\n\n"
        "1. 元素个数\n"
        "2. 最大值 最小值（n = 0 输出 `EMPTY`）\n"
        "3. 逆序输出（空格分隔）\n\n"
        "★ 技巧点：`vector<int> a; a.push_back(x);` —— **不用预知长度**的动态数组，"
        "配合 `a.size() / a.empty() / a.back()` 是 STL 第一课。"
        "逆序遍历用 `for (int i = n-1; i >= 0; i--)` 或反向迭代器 `rbegin()/rend()`。"
    ),
    input_format="第一行 `n`（0 ≤ n ≤ 10⁵）；第二行 `n` 个整数（n = 0 时此行为空或省略）。",
    output_format="三行，如题面所述。",
    constraints_md="- 0 ≤ n ≤ 10⁵\n- |元素| ≤ 10⁹",
    inputs=[
        "5\n3 1 4 1 5\n",
        "0\n\n",
        "1\n42\n",
        "3\n-7 0 -7\n",
        "6\n1000000000 -1000000000 0 5 -5 5\n",
    ],
    samples=2,
    oracle=_oracle_01,
    solution=r'''#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<int> a;
    for (int k = 0; k < n; k++) {
        int x; scanf("%d", &x);
        a.push_back(x);              /* 长度未知也能一路装 */
    }
    printf("%d\n", (int)a.size());
    if (a.empty()) {
        printf("EMPTY\nEMPTY\n");
        return 0;
    }
    int mx = a[0], mn = a[0];
    for (int x : a) { mx = max(mx, x); mn = min(mn, x); }
    printf("%d %d\n", mx, mn);
    for (auto it = a.rbegin(); it != a.rend(); ++it)
        printf("%d%c", *it, it + 1 == a.rend() ? '\n' : ' ');
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
using namespace std;
int main() {
    int n;
    cin >> n;
    vector<int> a(n);                /* 先开 n 格，下标访问 */
    for (int k = 0; k < n; k++) cin >> a[k];
    cout << n << "\n";
    if (n == 0) {
        cout << "EMPTY\nEMPTY\n";
        return 0;
    }
    int mx = a[0], mn = a[0];
    for (size_t k = 0; k < a.size(); k++) {
        mx = a[k] > mx ? a[k] : mx;
        mn = a[k] < mn ? a[k] : mn;
    }
    cout << mx << " " << mn << "\n";
    for (int k = n - 1; k >= 0; k--)
        cout << a[k] << (k ? " " : "\n");
    return 0;
}
''',
)


def _oracle_02(text: str) -> str:
    lines = text.rstrip("\n").split("\n")
    s, t = lines[0], lines[1]
    first = -1
    for i in range(len(s) - len(t) + 1):
        if s[i:i + len(t)] == t:
            first = i
            break
    cnt = 0
    i = 0
    while i <= len(s) - len(t):
        if s[i:i + len(t)] == t:
            cnt += 1
            i += 1
        else:
            i += 1
    removed = []
    i = 0
    while i < len(s):
        if i + len(t) <= len(s) and s[i:i + len(t)] == t:
            i += len(t)
        else:
            removed.append(s[i])
            i += 1
    return "%d\n%d\n%s\n" % (first, cnt, "".join(removed))

add(
    title="string 查找与删除",
    section="技巧特训 · C/C++",
    difficulty=2, score=12, tags=["技巧特训", "string", "find", "substr"],
    statement_md=(
        "读入主串 `s` 与模式串 `t`，输出三行：\n\n"
        "1. `t` 在 `s` 中第一次出现的位置（0 基，没有输出 `-1`）\n"
        "2. `t` 在 `s` 中出现的次数（**可重叠**，如 `aaaa` 里 `aa` 算 3 次）\n"
        "3. 把 `s` 中所有 `t` **删掉**后的串（不重叠、从左到右贪心删）\n\n"
        "★ 技巧点：`s.find(t)` 返回下标或 `string::npos`；`s.find(t, pos)` "
        "从 pos 起继续找——循环 `find` 就是「计数所有出现」的写法。"
        "拼接删除结果用 `s.substr(i, len)` 或直接累积字符。"
    ),
    input_format="两行：主串 `s`（≤ 10⁵）、模式串 `t`（≤ 100，非空）。",
    output_format="三行，如题面所述。",
    constraints_md="- 1 ≤ |t| ≤ |s| ≤ 10⁵",
    inputs=[
        "abcabcabc\nabc\n",
        "hello world hello\nhello\n",
        "aaaa\naa\n",
        "abcdef\nxyz\n",
        "abababab\nabab\n",
    ],
    samples=2,
    oracle=_oracle_02,
    solution=r'''#include <cstdio>
#include <cstring>
#include <string>
using namespace std;
int main() {
    static char buf[100005];
    if (!fgets(buf, sizeof buf, stdin)) return 0;
    string s(buf);
    if (!s.empty() && s[s.size() - 1] == '\n') s.erase(s.size() - 1);   /* s 可含空格，必须整行读 */
    if (!fgets(buf, sizeof buf, stdin)) return 0;
    string t(buf);
    if (!t.empty() && t[t.size() - 1] == '\n') t.erase(t.size() - 1);
    size_t pos = s.find(t);
    printf("%d\n", pos == string::npos ? -1 : (int)pos);
    int cnt = 0;
    size_t i = s.find(t);
    while (i != string::npos) {
        cnt++;
        i = s.find(t, i + 1);        /* +1：允许重叠 */
    }
    printf("%d\n", cnt);
    string res;
    size_t p = 0;
    while (p < s.size()) {
        if (p + t.size() <= s.size() && s.compare(p, t.size(), t) == 0)
            p += t.size();           /* 贪心整段跳过 */
        else
            res += s[p++];
    }
    printf("%s\n", res.c_str());
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <string>
using namespace std;
int main() {
    string s, t;
    getline(cin, s);                 /* s 可含空格，getline 整行读 */
    getline(cin, t);
    while (!s.empty() && (s[s.size()-1] == '\r' || s[s.size()-1] == '\n')) s.erase(s.size()-1);
    while (!t.empty() && (t[t.size()-1] == '\r' || t[t.size()-1] == '\n')) t.erase(t.size()-1);
    int first = (int)s.find(t);
    cout << first << "\n";
    int cnt = 0;
    for (size_t i = 0; i + t.size() <= s.size(); i++)
        if (s.compare(i, t.size(), t) == 0) cnt++;
    cout << cnt << "\n";
    string res;
    size_t i = 0;
    while (i < s.size()) {
        if (s.substr(i, t.size()) == t) i += t.size();
        else res += s[i++];
    }
    cout << res << "\n";
    return 0;
}
''',
)


def _oracle_03(text: str) -> str:
    lines = text.rstrip("\n").split("\n")
    n = int(lines[0])
    rows = []
    for i in range(1, n + 1):
        p = lines[i].split()
        total = int(p[1]) + int(p[2]) + int(p[3])
        rows.append((p[0], total))
    rows.sort(key=lambda r: (-r[1], r[0]))
    return "".join("%s %d\n" % (nm, sc) for nm, sc in rows)

add(
    title="sort 自定义比较成绩单",
    section="技巧特训 · C/C++",
    difficulty=2, score=15, tags=["技巧特训", "sort", "比较函数", "结构体"],
    statement_md=(
        "读入 `n` 个学生的「姓名 语文 数学 英语」，输出排名：**总分降序**，"
        "同分按**姓名字典序升序**。每行 `姓名 总分`。\n\n"
        "★ 技巧点：`sort(v.begin(), v.end(), cmp)` 的第三参是**比较函数**，"
        "返回「前者应排在前面」的 bool。多关键字有两个写法：cmp 里先比主键再比次键，"
        "或者**利用 sort 的稳定性**（C++ 的 sort 不稳定！要用 stable_sort 或在 cmp "
        "里把次键显式写全——本模板采用后者，语义自足）。"
    ),
    input_format="第一行 `n`；随后 `n` 行 `姓名 语文 数学 英语`（姓名不含空格，各科 0~150）。",
    output_format="`n` 行，排序后的 `姓名 总分`。",
    constraints_md="- 1 ≤ n ≤ 1000",
    inputs=[
        "3\nAlice 90 80 70\nBob 80 90 70\nCindy 90 85 65\n",
        "4\nzhou 100 100 100\nli 100 100 100\nzhao 60 60 60\nqian 100 99 101\n",
        "2\nab 0 0 0\naa 1 0 0\n",
        "5\ne 1 1 1\nd 2 2 2\nc 3 3 3\nb 4 4 4\na 5 5 5\n",
        "3\nTom 60 70 80\nJerry 80 70 60\nSpike 70 70 70\n",
    ],
    samples=2,
    oracle=_oracle_03,
    solution=r'''#include <cstdio>
#include <string>
#include <vector>
#include <algorithm>
using namespace std;
struct Stu { string name; int total; };
int main() {
    int n;
    scanf("%d", &n);
    vector<Stu> v;
    for (int k = 0; k < n; k++) {
        char buf[64];
        int c, m, e;
        scanf("%s %d %d %d", buf, &c, &m, &e);
        v.push_back({buf, c + m + e});
    }
    sort(v.begin(), v.end(), [](const Stu &a, const Stu &b) {
        if (a.total != b.total) return a.total > b.total;   /* 总分降序 */
        return a.name < b.name;                             /* 同分名字升序 */
    });
    for (auto &s : v) printf("%s %d\n", s.name.c_str(), s.total);
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
using namespace std;
int main() {
    int n;
    cin >> n;
    vector<pair<int, string> > v;    /* <总分取负, 姓名>：直接默认比较 */
    for (int k = 0; k < n; k++) {
        string nm; int c, m, e;
        cin >> nm >> c >> m >> e;
        v.push_back(make_pair(-(c + m + e), nm));
    }
    sort(v.begin(), v.end());        /* pair 默认字典序 = 总分降序 + 名字升序 */
    for (size_t k = 0; k < v.size(); k++)
        cout << v[k].second << " " << -v[k].first << "\n";
    return 0;
}
''',
)


def _oracle_04(text: str) -> str:
    lines = text.rstrip("\n").split("\n")
    n = int(lines[0])
    pts = []
    for i in range(1, n + 1):
        x, y = lines[i].split()
        pts.append((int(x), int(y)))
    pts.sort(key=lambda p: (p[0], -p[1]))
    return "".join("%d %d\n" % p for p in pts)

add(
    title="pair 排序坐标",
    section="技巧特训 · C/C++",
    difficulty=2, score=12, tags=["技巧特训", "pair", "sort", "坐标"],
    statement_md=(
        "读入 `n` 个平面上的点（整数坐标），按 **x 升序**、x 相同按 **y 降序**"
        "排序后输出，每行 `x y`。\n\n"
        "★ 技巧点：`pair<int,int>` 自带**字典序比较**（先 first 后 second），"
        "直接可 sort。要「second 降序」时最省事的招是**给 second 存负值**"
        "（或自定义比较函数），排序取出来时再翻回来。"
    ),
    input_format="第一行 `n`；随后 `n` 行每行 `x y`（|坐标| ≤ 10⁹）。",
    output_format="`n` 行，排序后的 `x y`。",
    constraints_md="- 1 ≤ n ≤ 10⁵",
    inputs=[
        "4\n1 2\n1 5\n0 3\n1 2\n",
        "3\n2 2\n2 1\n2 3\n",
        "5\n5 5\n-5 5\n5 -5\n-5 -5\n0 0\n",
        "2\n7 1\n7 1\n",
        "4\n9 9\n-9 9\n9 -9\n-9 -9\n",
    ],
    samples=2,
    oracle=_oracle_04,
    solution=r'''#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;
int main() {
    int n;
    scanf("%d", &n);
    vector<pair<int, int> > v(n);
    for (int k = 0; k < n; k++) scanf("%d %d", &v[k].first, &v[k].second);
    sort(v.begin(), v.end(), [](const pair<int,int> &a, const pair<int,int> &b) {
        if (a.first != b.first) return a.first < b.first;
        return a.second > b.second;              /* x 同则 y 降序 */
    });
    for (auto &p : v) printf("%d %d\n", p.first, p.second);
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
int main() {
    int n;
    cin >> n;
    vector<pair<int, int> > v(n);
    for (int k = 0; k < n; k++) {
        cin >> v[k].first >> v[k].second;
        v[k].second = -v[k].second;      /* second 存负值 → 默认排序即 y 降序 */
    }
    sort(v.begin(), v.end());
    for (auto &p : v) cout << p.first << " " << -p.second << "\n";
    return 0;
}
''',
)


def _oracle_05(text: str) -> str:
    w = text.split()[1:]             # 第一个 token 是 n，跳过
    cnt = {}
    for x in w:
        cnt[x] = cnt.get(x, 0) + 1
    out = "".join("%s %d\n" % (k, cnt[k]) for k in sorted(cnt))
    return out + "DISTINCT %d\n" % len(cnt)

add(
    title="map 计数与有序输出",
    section="技巧特训 · C/C++",
    difficulty=2, score=12, tags=["技巧特训", "map", "计数", "字典序"],
    statement_md=(
        "读入 `n` 个单词，**按字典序**输出每个不同单词及其出现次数"
        "（每行 `单词 次数`），最后一行 `DISTINCT 不同单词数`。\n\n"
        "★ 技巧点：`map<string,int>` 是**红黑树**，插入时自动按 key 有序，"
        "遍历即字典序——「计数 + 有序输出」一步到位。"
        "对 key 用 `[]` 访问会在不存在时**自动插入默认值 0**，所以 "
        "`m[w]++` 一行就是计数器。只要有序不要计数时换 `unordered_map`（哈希，更快）。"
    ),
    input_format="第一行 `n`；第二行 `n` 个单词（长度 ≤ 20，小写字母）。",
    output_format="如题面所述。",
    constraints_md="- 1 ≤ n ≤ 10⁵",
    inputs=[
        "6\nbanana apple cherry apple banana apple\n",
        "3\none two three\n",
        "5\na a b b a\n",
        "1\nsolo\n",
        "7\nd c b a d c b\n",
    ],
    samples=2,
    oracle=_oracle_05,
    solution=r'''#include <cstdio>
#include <string>
#include <map>
using namespace std;
int main() {
    int n;
    scanf("%d", &n);
    map<string, int> m;
    for (int k = 0; k < n; k++) {
        char buf[32];
        scanf("%s", buf);
        m[buf]++;                    /* [] 不存在自动置 0 */
    }
    for (map<string, int>::iterator it = m.begin(); it != m.end(); ++it)
        printf("%s %d\n", it->first.c_str(), it->second);
    printf("DISTINCT %d\n", (int)m.size());
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <string>
#include <map>
using namespace std;
int main() {
    int n;
    cin >> n;
    map<string, int> m;
    string w;
    for (int k = 0; k < n; k++) {
        cin >> w;
        m[w] = m[w] + 1;
    }
    for (auto &kv : m) cout << kv.first << " " << kv.second << "\n";
    cout << "DISTINCT " << m.size() << "\n";
    return 0;
}
''',
)


def _oracle_06(text: str) -> str:
    d = text.split()
    n = int(d[0])
    a = [int(v) for v in d[1:1 + n]]
    s = sorted(set(a))
    return "%d\n%s\n" % (len(s), " ".join(map(str, s)))

add(
    title="set 去重与有序",
    section="技巧特训 · C/C++",
    difficulty=1, score=10, tags=["技巧特训", "set", "去重", "二分树"],
    statement_md=(
        "读入 `n` 个整数（可重复、乱序），输出两行：\n\n"
        "1. 去重后的个数\n"
        "2. 去重后**升序**排列的序列（空格分隔）\n\n"
        "★ 技巧点：`set<int>` 插入时自动**去重 + 有序**，"
        "`s.insert(x)` 一行完成；取出来直接遍历。"
        "数组做法要么排序后 unique，要么开超大桶——`set` 一句话的事。"
        "配套记忆：`s.count(x)` 判存在（O(log n)），`unordered_set` 更快但无序。"
    ),
    input_format="第一行 `n`；第二行 `n` 个整数（1 ≤ n ≤ 10⁵，|元素| ≤ 10⁹）。",
    output_format="两行，如题面所述。",
    constraints_md="- 1 ≤ n ≤ 10⁵",
    inputs=[
        "8\n3 1 4 1 5 9 2 6\n",
        "5\n7 7 7 7 7\n",
        "3\n-1 -1 0\n",
        "6\n5 4 3 2 1 5\n",
        "1\n1000000000\n",
    ],
    samples=2,
    oracle=_oracle_06,
    solution=r'''#include <cstdio>
#include <set>
using namespace std;
int main() {
    int n;
    scanf("%d", &n);
    set<int> s;
    for (int k = 0; k < n; k++) {
        int x; scanf("%d", &x);
        s.insert(x);
    }
    printf("%d\n", (int)s.size());
    int first = 1;
    for (set<int>::iterator it = s.begin(); it != s.end(); ++it) {
        printf(first ? "%d" : " %d", *it);
        first = 0;
    }
    printf("\n");
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int k = 0; k < n; k++) cin >> a[k];
    sort(a.begin(), a.end());
    a.erase(unique(a.begin(), a.end()), a.end());   /* 排序 + unique + 截断 */
    cout << a.size() << "\n";
    for (size_t k = 0; k < a.size(); k++)
        cout << a[k] << (k + 1 < a.size() ? " " : "\n");
    return 0;
}
''',
)


def _oracle_07(text: str) -> str:
    w = text.split()
    out = "".join(x + "\n" for x in w)
    return out + "TOTAL %d\n" % len(w)

add(
    title="stringstream 拆词",
    section="技巧特训 · C/C++",
    difficulty=2, score=10, tags=["技巧特训", "stringstream", "流", "分词"],
    statement_md=(
        "读入一行（单词间可能有多个空格），把每个单词单独输出一行，"
        "最后一行 `TOTAL 词数`。\n\n"
        "★ 技巧点：`stringstream ss(line); while (ss >> w) {...}` —— "
        "把一行字符串**当输入流再用一遍**，`>>` 自动按空白切分、自动跳连续空格，"
        "C 里手写扫描器十几行的活一行循环完成。配套：`getline(cin, line)` 读整行"
        "（混用 `cin >>` 与 getline 时注意吃掉残留换行）。"
    ),
    input_format="一行，若干个单词（1 ≤ 词数 ≤ 2000，长度 ≤ 20）。",
    output_format="每行一个单词；最后一行 `TOTAL 词数`。",
    constraints_md="- 1 ≤ 词数 ≤ 2000",
    inputs=[
        "the quick   brown fox\n",
        "solo\n",
        "a  b c   d e\n",
        "one two three four five six\n",
        "x\n",
    ],
    samples=2,
    oracle=_oracle_07,
    solution=r'''#include <cstdio>
#include <cstring>
#include <sstream>
#include <string>
using namespace std;
int main() {
    char buf[100005];
    if (!fgets(buf, sizeof buf, stdin)) return 0;
    string line(buf);
    stringstream ss(line);
    string w;
    int cnt = 0;
    while (ss >> w) {
        printf("%s\n", w.c_str());
        cnt++;
    }
    printf("TOTAL %d\n", cnt);
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <sstream>
#include <string>
#include <vector>
using namespace std;
int main() {
    string line;
    getline(cin, line);
    istringstream iss(line);
    vector<string> ws;
    string w;
    while (iss >> w) ws.push_back(w);
    for (size_t k = 0; k < ws.size(); k++) cout << ws[k] << "\n";
    cout << "TOTAL " << ws.size() << "\n";
    return 0;
}
''',
)


# --------------------------------------------------------------------- #
#  算法套路（difficulty 2~3）
# --------------------------------------------------------------------- #

def _oracle_08(text: str) -> str:
    d = text.split()
    i = 0
    n = int(d[i]); i += 1
    q = int(d[i]); i += 1
    a = [int(d[i + k]) for k in range(n)]
    i += n
    out = []
    for _ in range(q):
        x = int(d[i]); i += 1
        ans = "NONE"
        for v in a:
            if v > x:
                ans = str(v)
                break
        out.append(ans)
    return "".join(s + "\n" for s in out)

add(
    title="第一个大于 x 的数 upper_bound",
    section="技巧特训 · C/C++",
    difficulty=2, score=15, tags=["技巧特训", "upper_bound", "二分", "STL"],
    statement_md=(
        "读入**升序**数组（可重复）和 `q` 个询问 `x`。对每个询问，"
        "输出数组中**第一个严格大于 x** 的元素；不存在输出 `NONE`。\n\n"
        "★ 技巧点：`upper_bound(a.begin(), a.end(), x)` 返回**第一个 > x** 的迭代器"
        "（减 `begin()` 得下标）；配套 `lower_bound` 是第一个 **≥ x**。"
        "这两个函数是 STL 二分的全部入口——有序数组的手写二分可以不写，"
        "但两者语义（>/≥）必须分清，这是面试和竞赛的双高频考点。"
    ),
    input_format=(
        "第一行 `n q`；第二行 `n` 个升序整数；随后 `q` 行每行一个 `x`。\n"
        "- 1 ≤ n, q ≤ 2×10⁵，|值| ≤ 10⁹"
    ),
    output_format="`q` 行，每行一个数或 `NONE`。",
    constraints_md="- 1 ≤ n, q ≤ 2×10⁵",
    inputs=[
        "8 4\n1 2 4 4 4 7 9 9\n4\n5\n9\n0\n",
        "5 3\n2 2 2 2 2\n1\n2\n3\n",
        "1 2\n10\n10\n11\n",
        "6 2\n-5 -2 0 3 8 8\n-6\n8\n",
        "4 3\n1 3 5 7\n7\n6\n1\n",
    ],
    samples=2,
    oracle=_oracle_08,
    solution=r'''#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;
int main() {
    int n, q;
    scanf("%d %d", &n, &q);
    vector<int> a(n);
    for (int k = 0; k < n; k++) scanf("%d", &a[k]);
    while (q--) {
        int x; scanf("%d", &x);
        auto it = upper_bound(a.begin(), a.end(), x);   /* 第一个 > x */
        if (it == a.end()) printf("NONE\n");
        else printf("%d\n", *it);
    }
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
using namespace std;
int main() {
    int n, q;
    cin >> n >> q;
    vector<int> a(n);
    for (int k = 0; k < n; k++) cin >> a[k];
    while (q--) {
        int x; cin >> x;
        int lo = 0, hi = n;
        while (lo < hi) {              /* 手写二分：第一个 > x */
            int mid = (lo + hi) / 2;
            if (a[mid] > x) hi = mid;
            else lo = mid + 1;
        }
        if (lo < n) cout << a[lo] << "\n";
        else cout << "NONE\n";
    }
    return 0;
}
''',
)


def _oracle_09(text: str) -> str:
    d = text.split()
    i = 0
    n = int(d[i]); i += 1
    q = int(d[i]); i += 1
    a = [int(d[i + k]) for k in range(n)]
    i += n
    out = []
    for _ in range(q):
        x = int(d[i]); i += 1
        ans = n
        j = 0
        while j < n:
            if a[j] >= x:
                ans = j
                break
            j += 1
        out.append(ans)
    return "".join("%d\n" % v for v in out)

add(
    title="插入位置 lower_bound",
    section="技巧特训 · C/C++",
    difficulty=2, score=12, tags=["技巧特训", "lower_bound", "二分", "插入位置"],
    statement_md=(
        "读入**升序**数组和 `q` 个询问 `x`。对每个询问，输出「把 x 插入数组以"
        "保持有序」的**下标**（0 基；x 不小于所有元素时输出 `n`）。\n\n"
        "★ 技巧点：这就是 `lower_bound(a.begin(), a.end(), x) - a.begin()` 的定义"
        "——第一个 **≥ x** 的下标。`vector::insert(v.begin()+pos, x)` 配合它，"
        "有序插入两行完成。与 upper_bound 的区分：`1 2 2 3` 里找 2，"
        "lower_bound 给 1（第一个 2），upper_bound 给 3（2 之后）。"
    ),
    input_format=(
        "第一行 `n q`；第二行 `n` 个升序整数；随后 `q` 行每行一个 `x`。\n"
        "- 1 ≤ n, q ≤ 2×10⁵，|值| ≤ 10⁹"
    ),
    output_format="`q` 行，每行一个下标。",
    constraints_md="- 1 ≤ n, q ≤ 2×10⁵",
    inputs=[
        "4 4\n1 2 2 3\n2\n0\n4\n3\n",
        "1 3\n5\n4\n5\n6\n",
        "5 2\n2 2 2 2 2\n2\n3\n",
        "6 1\n-5 -2 0 3 8 8\n1\n",
        "3 2\n10 20 30\n15\n30\n",
    ],
    samples=2,
    oracle=_oracle_09,
    solution=r'''#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;
int main() {
    int n, q;
    scanf("%d %d", &n, &q);
    vector<int> a(n);
    for (int k = 0; k < n; k++) scanf("%d", &a[k]);
    while (q--) {
        int x; scanf("%d", &x);
        printf("%d\n", (int)(lower_bound(a.begin(), a.end(), x) - a.begin()));
    }
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
using namespace std;
int main() {
    int n, q;
    cin >> n >> q;
    vector<int> a(n);
    for (int k = 0; k < n; k++) cin >> a[k];
    while (q--) {
        int x; cin >> x;
        int lo = 0, hi = n;
        while (lo < hi) {              /* 第一个 >= x */
            int mid = (lo + hi) / 2;
            if (a[mid] >= x) hi = mid;
            else lo = mid + 1;
        }
        cout << lo << "\n";
    }
    return 0;
}
''',
)


def _oracle_10(text: str) -> str:
    d = text.split()
    i = 0
    n = int(d[i]); i += 1
    m1 = int(d[i]); i += 1
    m2 = int(d[i]); i += 1
    a = [int(d[i + k]) for k in range(n)]
    i += n
    diff = [0] * (n + 1)
    for _ in range(m1):
        l = int(d[i + 1]); r = int(d[i + 2]); v = int(d[i + 3]); i += 4
        diff[l - 1] += v
        diff[r] -= v
    cur = 0
    res = [0] * n
    for k in range(n):
        cur += diff[k]
        res[k] = a[k] + cur
    out = []
    for _ in range(m2):
        p = int(d[i]); i += 1
        out.append(res[p - 1])
    return "".join("%d\n" % v for v in out)

add(
    title="差分：区间加与单点查",
    section="技巧特训 · C/C++",
    difficulty=3, score=25, tags=["技巧特训", "差分", "前缀和", "BIT"],
    statement_md=(
        "数组 `a`（下标 1..n）。先来 `m1` 次**区间加**：每行 `1 l r v` 表示 "
        "a[l..r] 每个元素加 v；再来 `m2` 次**单点查询**：每行一个 `i`，"
        "输出 a[i] 的最终值。\n\n"
        "★ 技巧点：**差分数组**——区间加 l..r 只动两个格子：`d[l]+=v; d[r+1]-=v`；"
        "全部加完后对 d 做一遍前缀和就得到每个位置的净变化。"
        "「区间改、最后统一查」用差分 O(n+m)；若是「边改边查」就要上树状数组/线段树了"
        "（alt 解给出树状数组版本，感受一下差别）。"
    ),
    input_format=(
        "第一行 `n m1 m2`；第二行 `n` 个整数 a₁..aₙ；\n"
        "随后 `m1` 行每行 `1 l r v`（1 ≤ l ≤ r ≤ n，|v| ≤ 10⁴）；\n"
        "随后 `m2` 行每行一个 `i`（查询下标）。\n"
        "- 1 ≤ n, m1, m2 ≤ 10⁵，|aᵢ| ≤ 10⁹（用 64 位整数装和）"
    ),
    output_format="`m2` 行，每行一个最终值。",
    constraints_md="- 1 ≤ n, m1, m2 ≤ 10⁵",
    inputs=[
        "5 2 3\n1 2 3 4 5\n1 1 3 10\n1 2 5 -1\n1\n3\n5\n",
        "3 3 1\n0 0 0\n1 1 1 5\n1 2 3 5\n1 3 3 5\n3\n",
        "1 1 2\n100\n1 1 1 -100\n1\n1\n",
        _rand_big_case(),
    ],
    samples=2,
    oracle=_oracle_10,
    solution=r'''#include <cstdio>
#include <vector>
using namespace std;
int main() {
    int n, m1, m2;
    scanf("%d %d %d", &n, &m1, &m2);
    vector<long long> a(n + 1), d(n + 2, 0);
    for (int k = 1; k <= n; k++) scanf("%lld", &a[k]);
    for (int k = 0; k < m1; k++) {
        int op; scanf("%d", &op);
        int l, r; long long v;
        scanf("%d %d %lld", &l, &r, &v);
        d[l] += v; d[r + 1] -= v;     /* 差分：O(1) 区间加 */
    }
    long long cur = 0;
    vector<long long> res(n + 1);
    for (int k = 1; k <= n; k++) {
        cur += d[k];
        res[k] = a[k] + cur;
    }
    while (m2--) {
        int p; scanf("%d", &p);
        printf("%lld\n", res[p]);
    }
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <vector>
using namespace std;
/* 另一套：树状数组在差分序列上做区间加 + 单点查（边改边查也吃得下） */
int n;
vector<long long> bit;
void add(int i, long long v) {
    for (; i <= n; i += i & (-i)) bit[i] += v;
}
long long ask(int i) {
    long long s = 0;
    for (; i > 0; i -= i & (-i)) s += bit[i];
    return s;
}
int main() {
    int m1, m2;
    scanf("%d %d %d", &n, &m1, &m2);
    vector<long long> a(n + 1);
    bit.assign(n + 1, 0);
    for (int k = 1; k <= n; k++) scanf("%lld", &a[k]);
    for (int k = 0; k < m1; k++) {
        int op; scanf("%d", &op);
        int l, r; long long v;
        scanf("%d %d %lld", &l, &r, &v);
        add(l, v);
        if (r + 1 <= n) add(r + 1, -v);
    }
    while (m2--) {
        int p; scanf("%d", &p);
        printf("%lld\n", a[p] + ask(p));
    }
    return 0;
}
''',
)


def _oracle_11(text: str) -> str:
    d = text.split()
    i = 0
    n = int(d[i]); i += 1
    target = int(d[i]); i += 1
    a = [int(d[i + k]) for k in range(n)]
    i += n
    seen = {}
    ans_i = ans_j = -1
    for j in range(n):
        need = target - a[j]
        if need in seen:
            ans_i = seen[need]
            ans_j = j
            break
        if a[j] not in seen:
            seen[a[j]] = j
    if ans_i < 0:
        return "NONE\n"
    return "%d %d\n" % (ans_i + 1, ans_j + 1)

add(
    title="有序数组两数之和",
    section="技巧特训 · C/C++",
    difficulty=2, score=15, tags=["技巧特训", "双指针", "两数之和"],
    statement_md=(
        "读入 `n`、目标和 `target`，以及 **升序** 的 `n` 个整数。"
        "找出一对下标 `i < j`（1 基）使 `aᵢ + aⱼ = target`，输出 `i j`"
        "（保证解若存在则唯一）；不存在输出 `NONE`。\n\n"
        "★ 技巧点：**双指针**——左指针在头、右指针在尾：和小了左移 `lo`，"
        "和大了左移 `hi`，相遇即无解。有序数组上它把 O(n²) 压成 O(n)，"
        "空间 O(1)。配合「序列有序」这个前提，是双指针家族最入门的一道。"
    ),
    input_format=(
        "第一行 `n target`；第二行 `n` 个**升序**整数。\n"
        "- 2 ≤ n ≤ 10⁵，|元素|、|target| ≤ 10⁹"
    ),
    output_format="一行 `i j`（1 基、i < j）或 `NONE`。",
    constraints_md="- 2 ≤ n ≤ 10⁵",
    inputs=[
        "5 9\n1 2 4 7 11\n",
        "4 10\n1 3 5 7\n",
        "3 100\n1 2 3\n",
        "6 10\n-3 0 2 5 8 12\n",
        "2 4\n2 2\n",
    ],
    samples=2,
    oracle=_oracle_11,
    solution=r'''#include <cstdio>
#include <vector>
using namespace std;
int main() {
    int n;
    long long target;
    scanf("%d %lld", &n, &target);
    vector<long long> a(n);
    for (int k = 0; k < n; k++) scanf("%lld", &a[k]);
    int lo = 0, hi = n - 1;
    while (lo < hi) {
        long long s = a[lo] + a[hi];
        if (s == target) {
            printf("%d %d\n", lo + 1, hi + 1);
            return 0;
        }
        if (s < target) lo++;
        else hi--;
    }
    printf("NONE\n");
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <unordered_map>
#include <vector>
using namespace std;
int main() {
    int n;
    long long target;
    cin >> n >> target;
    vector<long long> a(n);
    for (int k = 0; k < n; k++) cin >> a[k];
    unordered_map<long long, int> seen;      /* 值 -> 下标 */
    for (int j = 0; j < n; j++) {
        long long need = target - a[j];
        if (seen.count(need)) {
            cout << seen[need] + 1 << " " << j + 1 << "\n";
            return 0;
        }
        if (!seen.count(a[j])) seen[a[j]] = j;
    }
    cout << "NONE\n";
    return 0;
}
''',
)


def _oracle_12(text: str) -> str:
    d = text.split()
    n = int(d[0])
    a = [int(v) for v in d[1:1 + n]]
    out = []
    for i in range(n):
        ans = -1
        for j in range(i + 1, n):
            if a[j] > a[i]:
                ans = a[j]
                break
        out.append(ans)
    return " ".join(map(str, out)) + "\n"

add(
    title="下一个更大元素 单调栈",
    section="技巧特训 · C/C++",
    difficulty=2, score=15, tags=["技巧特训", "单调栈", "栈", "下一个更大"],
    statement_md=(
        "读入 `n` 个整数，对每个位置输出**它右边第一个比它大的元素**"
        "（没有则输出 `-1`），一行内空格分隔。\n\n"
        "★ 技巧点：**单调栈**——栈里存「还在等答案的下标」，新元素把栈里"
        "所有比它小的位置弹出来结算，栈内值自底向顶**严格递减**，"
        "每个元素进栈出栈各一次，整体 O(n)。暴力是 O(n²)，n=10⁵ 直接超时。"
        "「下一个更大 / 更小、左右第一个」一类问题全是单调栈的主场。"
    ),
    input_format="第一行 `n`；第二行 `n` 个整数（1 ≤ n ≤ 2×10⁵，|元素| ≤ 10⁹）。",
    output_format="一行，`n` 个答案（空格分隔）。",
    constraints_md="- 1 ≤ n ≤ 2×10⁵",
    inputs=[
        "5\n2 1 3 2 5\n",
        "4\n4 3 2 1\n",
        "1\n7\n",
        "6\n1 2 3 4 5 6\n",
        "8\n3 7 1 7 8 4 5 8\n",
    ],
    samples=2,
    oracle=_oracle_12,
    solution=r'''#include <cstdio>
#include <vector>
#include <stack>
using namespace std;
int main() {
    int n;
    scanf("%d", &n);
    vector<long long> a(n), ans(n);
    for (int k = 0; k < n; k++) scanf("%lld", &a[k]);
    stack<int> st;                   /* 存下标，栈内值严格递减 */
    for (int k = 0; k < n; k++) {
        while (!st.empty() && a[st.top()] < a[k]) {
            ans[st.top()] = a[k];    /* k 是栈顶右边第一个更大的 */
            st.pop();
        }
        st.push(k);
    }
    while (!st.empty()) { ans[st.top()] = -1; st.pop(); }
    for (int k = 0; k < n; k++) printf("%lld%c", ans[k], k + 1 == n ? '\n' : ' ');
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
using namespace std;
int main() {
    int n;
    cin >> n;
    vector<long long> a(n), ans(n), st;
    for (int k = 0; k < n; k++) cin >> a[k];
    /* 从右往左扫：栈顶即当前元素右侧的候选 */
    for (int k = n - 1; k >= 0; k--) {
        while (!st.empty() && st.back() <= a[k]) st.pop_back();
        ans[k] = st.empty() ? -1 : st.back();
        st.push_back(a[k]);
    }
    for (int k = 0; k < n; k++) cout << ans[k] << (k + 1 == n ? "\n" : " ");
    return 0;
}
''',
)


def _oracle_13(text: str) -> str:
    d = text.split()
    n = int(d[0])
    k = int(d[1])
    a = [int(v) for v in d[2:2 + n]]
    out = []
    for i in range(n - k + 1):
        out.append(max(a[i:i + k]))
    return " ".join(map(str, out)) + "\n"

add(
    title="滑动窗口最大值",
    section="技巧特训 · C/C++",
    difficulty=3, score=20, tags=["技巧特训", "单调队列", "deque", "滑动窗口"],
    statement_md=(
        "读入 `n`、窗口大小 `k` 和 `n` 个整数。窗口从左到右每次滑动一格，"
        "输出**每个窗口的最大值**（一行，空格分隔，共 n−k+1 个）。\n\n"
        "★ 技巧点：**单调队列（deque）**——队头永远是当前窗口最大："
        "新元素入队前把队尾所有 ≤ 它的弹掉（它们永无出头之日）；"
        "队头滑出窗口范围就从队头弹。每个元素进出各一次，O(n)。"
        "暴力 O(nk)，multiset 做 O(n log k)——这题是单调队列的教科书场景。"
    ),
    input_format=(
        "第一行 `n k`（1 ≤ k ≤ n）；第二行 `n` 个整数（|元素| ≤ 10⁹）。\n"
        "- 1 ≤ n ≤ 2×10⁵"
    ),
    output_format="一行，n−k+1 个窗口最大值（空格分隔）。",
    constraints_md="- 1 ≤ k ≤ n ≤ 2×10⁵",
    inputs=[
        "8 3\n1 3 -1 -3 5 3 6 7\n",
        "4 1\n2 7 1 8\n",
        "5 5\n4 3 2 1 5\n",
        "6 2\n9 1 9 1 9 1\n",
        _rand_win_case(),
    ],
    samples=2,
    oracle=_oracle_13,
    solution=r'''#include <cstdio>
#include <vector>
#include <deque>
using namespace std;
int main() {
    int n, k;
    scanf("%d %d", &n, &k);
    vector<long long> a(n);
    for (int k2 = 0; k2 < n; k2++) scanf("%lld", &a[k2]);
    deque<int> dq;                   /* 存下标，值自队头到队尾递减 */
    for (int k2 = 0; k2 < n; k2++) {
        if (!dq.empty() && dq.front() <= k2 - k) dq.pop_front();  /* 队头出窗 */
        while (!dq.empty() && a[dq.back()] <= a[k2]) dq.pop_back();  /* 弱者让位 */
        dq.push_back(k2);
        if (k2 >= k - 1)
            printf("%lld%c", a[dq.front()], k2 + 1 == n ? '\n' : ' ');
    }
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <set>
#include <vector>
using namespace std;
int main() {
    int n, k;
    cin >> n >> k;
    vector<long long> a(n);
    for (int k2 = 0; k2 < n; k2++) cin >> a[k2];
    multiset<long long> win;
    for (int k2 = 0; k2 < n; k2++) {
        win.insert(a[k2]);
        if (k2 >= k) win.erase(win.find(a[k2 - k]));   /* 移除滑出窗口的 */
        if (k2 >= k - 1)
            cout << *win.rbegin() << (k2 + 1 == n ? "\n" : " ");
    }
    return 0;
}
''',
)


def _oracle_14(text: str) -> str:
    d = text.split()
    i = 0
    n = int(d[i]); i += 1
    need = int(d[i]); i += 1
    h = [int(d[i + k]) for k in range(n)]
    i += n

    def wood(cut):
        s = 0
        for v in h:
            if v > cut:
                s += v - cut
        return s

    lo, hi = 0, max(h)                   # 闭区间 [lo, hi] 内找最大可行 cut
    ans = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if wood(mid) >= need:
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return "%d\n" % ans

add(
    title="二分答案 伐木",
    section="技巧特训 · C/C++",
    difficulty=3, score=20, tags=["技巧特训", "二分答案", "贪心", "蓝桥杯"],
    statement_md=(
        "伐木场有 `n` 棵树，第 `i` 棵高 `hᵢ` 米。锯片定在高度 `h`，"
        "每棵树贡献 `max(0, hᵢ − h)` 米木材。需要**至少** `m` 米木材，"
        "求锯片**最高**能定多高。\n\n"
        "★ 技巧点：**二分答案**——答案 `h` 有单调性（锯得越高木材越少），"
        "于是「猜一个 h → O(n) 验算」加二分框架，O(n log maxH) 收工。"
        "「答案单调 → 二分答案」是蓝桥杯 / ACM 的常客套路，"
        "识别出单调性比写代码本身重要。"
    ),
    input_format=(
        "第一行 `n m`；第二行 `n` 个高度 hᵢ。\n"
        "- 1 ≤ n ≤ 2×10⁵，1 ≤ hᵢ ≤ 10⁹，1 ≤ m ≤ Σhᵢ（用 64 位整数装木材量）"
    ),
    output_format="一行，锯片的最大高度。",
    constraints_md="- 1 ≤ n ≤ 2×10⁵\n- 1 ≤ hᵢ ≤ 10⁹",
    inputs=[
        "5 20\n4 42 40 26 7\n",
        "3 3\n1 2 3\n",
        "4 10\n5 5 5 5\n",
        "2 2500000000\n1000000000 1000000000 1000000000\n",
        "1 999999999\n1000000000\n",
    ],
    samples=2,
    oracle=_oracle_14,
    solution=r'''#include <cstdio>
#include <vector>
using namespace std;
int n;
long long need;
vector<long long> h;
long long wood(long long cut) {
    long long s = 0;
    for (int k = 0; k < n; k++)
        if (h[k] > cut) s += h[k] - cut;
    return s;
}
int main() {
    scanf("%d %lld", &n, &need);
    h.resize(n);
    long long mx = 0;
    for (int k = 0; k < n; k++) {
        scanf("%lld", &h[k]);
        if (h[k] > mx) mx = h[k];
    }
    long long lo = 0, hi = mx, ans = 0;
    while (lo <= hi) {               /* 闭区间二分：[lo, hi] 里找最大可行 cut */
        long long mid = (lo + hi) / 2;
        if (wood(mid) >= need) { ans = mid; lo = mid + 1; }
        else hi = mid - 1;
    }
    printf("%lld\n", ans);
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
int n;
long long need;
vector<long long> h;
bool ok(long long cut) {             /* 判定式写法：cut 是否可行 */
    long long s = 0;
    for (long long v : h)
        if (v > cut) s += v - cut;
    return s >= need;
}
int main() {
    cin >> n >> need;
    h.resize(n);
    for (int k = 0; k < n; k++) cin >> h[k];      /* 读入高度！ */
    long long hi = *max_element(h.begin(), h.end());
    long long lo = 0;
    while (lo < hi) {                /* 半开区间二分：找第一个不可行的前一个 */
        long long mid = (lo + hi + 1) / 2;
        if (ok(mid)) lo = mid;
        else hi = mid - 1;
    }
    cout << lo << "\n";
    return 0;
}
''',
)


# --------------------------------------------------------------------- #
#  竞赛强度（difficulty 3~4）
# --------------------------------------------------------------------- #

def _oracle_15(text: str) -> str:
    d = text.split()
    i = 0
    n = int(d[i]); i += 1
    W = int(d[i]); i += 1
    items = []
    for _ in range(n):
        w = int(d[i]); v = int(d[i + 1]); i += 2
        items.append((w, v))
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for k in range(1, n + 1):
        w, v = items[k - 1]
        for j in range(W + 1):
            dp[k][j] = dp[k - 1][j]
            if j >= w and dp[k - 1][j - w] + v > dp[k][j]:
                dp[k][j] = dp[k - 1][j - w] + v
    return "%d\n" % dp[n][W]

add(
    title="01 背包（C++）",
    section="技巧特训 · C/C++",
    difficulty=3, score=25, tags=["技巧特训", "DP", "背包", "滚动数组"],
    statement_md=(
        "0-1 背包：`n` 件物品（重量 `wᵢ`、价值 `vᵢ`），容量 `W`，"
        "每件至多选一次，求最大总价值。\n\n"
        "★ 技巧点：二维 DP 压成一维——`dp[j] = max(dp[j], dp[j-w]+v)`，"
        "**内层 j 从 W 到 w 倒序枚举**（正序会让一件物品被用两次）。"
        "C++ 里一维 `vector<long long>` 又快又省内存，是背包容族的默认写法。"
        "细节：和可能超 int（100 件 × 10⁴ 价值），用 long long 稳妥。"
    ),
    input_format=(
        "第一行 `n W`；随后 `n` 行每行 `w v`。\n"
        "- 1 ≤ n ≤ 100，1 ≤ W ≤ 10⁴，1 ≤ w ≤ W，0 ≤ v ≤ 10⁴"
    ),
    output_format="一行，最大总价值。",
    constraints_md="- 1 ≤ n ≤ 100\n- 1 ≤ W ≤ 10⁴",
    inputs=[
        "4 5\n1 2\n2 3\n3 4\n4 5\n",
        "3 10\n5 10\n4 8\n6 12\n",
        "1 1\n1 100\n",
        "5 7\n2 3\n3 4\n4 5\n5 6\n1 1\n",
        _rand_knap_case(),
    ],
    samples=2,
    oracle=_oracle_15,
    solution=r'''#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;
int main() {
    int n, W;
    scanf("%d %d", &n, &W);
    vector<long long> dp(W + 1, 0);
    for (int k = 0; k < n; k++) {
        long long w, v;
        scanf("%lld %lld", &w, &v);
        for (long long j = W; j >= w; j--)          /* 倒序 = 每件一次 */
            dp[j] = max(dp[j], dp[j - w] + v);
    }
    printf("%lld\n", dp[W]);
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <cstring>
#include <algorithm>
using namespace std;
/* 另一套：记忆化递归（自顶向下），与前者的递推方向互为镜像 */
int n, W;
long long ws[105], vs[105];
long long memo[105][10005];
bool seen[105][10005];
long long f(int k, int cap) {        /* 前 k 件、剩余容量 cap */
    if (k == 0) return 0;
    if (seen[k][cap]) return memo[k][cap];
    long long best = f(k - 1, cap);
    if (ws[k] <= cap) {
        long long cand = f(k - 1, cap - ws[k]) + vs[k];
        if (cand > best) best = cand;
    }
    seen[k][cap] = true;
    memo[k][cap] = best;
    return best;
}
int main() {
    scanf("%d %d", &n, &W);
    for (int k = 1; k <= n; k++) scanf("%lld %lld", &ws[k], &vs[k]);
    memset(seen, 0, sizeof seen);
    printf("%lld\n", f(n, W));
    return 0;
}
''',
)


def _oracle_16(text: str) -> str:
    d = text.split()
    i = 0
    n = int(d[i]); i += 1
    W = int(d[i]); i += 1
    items = []
    for _ in range(n):
        w = int(d[i]); v = int(d[i + 1]); i += 2
        items.append((w, v))
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for k in range(1, n + 1):
        w, v = items[k - 1]
        for j in range(W + 1):
            dp[k][j] = dp[k - 1][j]
            # 完全背包：同一件可以再选（k 行自己转移）
            if j >= w and dp[k][j - w] + v > dp[k][j]:
                dp[k][j] = dp[k][j - w] + v
    return "%d\n" % dp[n][W]

add(
    title="完全背包",
    section="技巧特训 · C/C++",
    difficulty=3, score=20, tags=["技巧特训", "DP", "背包", "完全背包"],
    statement_md=(
        "完全背包：`n` 种物品（重量 `wᵢ`、价值 `vᵢ`），容量 `W`，"
        "每种**可以选无限件**，求最大总价值。\n\n"
        "★ 技巧点：和 0-1 背包只差**一个方向**——内层 `j` **正序**枚举"
        "（`dp[j-w]` 已经包含「本题再选一件」的转移）。"
        "把 0-1 与完全放一起记：「倒序 = 0-1，正序 = 完全」。"
        "alt 解给出朴素三重循环（枚举选几件），对比感受正序一维的妙处。"
    ),
    input_format=(
        "第一行 `n W`；随后 `n` 行每行 `w v`。\n"
        "- 1 ≤ n ≤ 20，1 ≤ W ≤ 1000，1 ≤ w ≤ W，0 ≤ v ≤ 10⁴"
    ),
    output_format="一行，最大总价值。",
    constraints_md="- 1 ≤ n ≤ 20\n- 1 ≤ W ≤ 10³",
    inputs=[
        "3 10\n2 3\n3 4\n4 5\n",
        "2 5\n1 2\n5 9\n",
        "1 1000\n1 1\n",
        "4 7\n3 5\n2 2\n4 8\n1 1\n",
        "2 6\n6 100\n3 49\n",
    ],
    samples=2,
    oracle=_oracle_16,
    solution=r'''#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;
int main() {
    int n, W;
    scanf("%d %d", &n, &W);
    vector<long long> dp(W + 1, 0);
    for (int k = 0; k < n; k++) {
        long long w, v;
        scanf("%lld %lld", &w, &v);
        for (long long j = w; j <= W; j++)          /* 正序 = 每种无限件 */
            dp[j] = max(dp[j], dp[j - w] + v);
    }
    printf("%lld\n", dp[W]);
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <algorithm>
using namespace std;
/* 另一套：朴素二维 + 枚举选几件（三重循环），直接对应状态定义 */
long long dp[25][1005];
int main() {
    int n, W;
    scanf("%d %d", &n, &W);
    long long ws[25], vs[25];
    for (int k = 1; k <= n; k++) scanf("%lld %lld", &ws[k], &vs[k]);
    for (int k = 1; k <= n; k++)
        for (int j = 0; j <= W; j++) {
            dp[k][j] = dp[k - 1][j];
            for (int c = 1; c * (int)ws[k] <= j; c++) {
                long long cand = dp[k - 1][j - c * (int)ws[k]] + c * vs[k];
                if (cand > dp[k][j]) dp[k][j] = cand;
            }
        }
    printf("%lld\n", dp[n][W]);
    return 0;
}
''',
)


def _oracle_17(text: str) -> str:
    d = text.split()
    n = int(d[0])
    a = [int(v) for v in d[1:1 + n]]
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if a[j] < a[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
    return "%d\n" % (max(dp) if n else 0)

add(
    title="LIS n log n（C++）",
    section="技巧特训 · C/C++",
    difficulty=3, score=20, tags=["技巧特训", "LIS", "upper_bound", "贪心"],
    statement_md=(
        "读入 `n` 个整数，输出**严格上升**子序列的最长长度。\n\n"
        "★ 技巧点：贪心 + 二分——`tails` 数组存「长度为 len 的上升子序列的"
        "最小结尾」，对每个 x 用 `lower_bound` 找位置：末尾外就追加，否则替换。"
        "`tails` 天然有序，全程 O(n log n)。C++ 的写法比 Python 还短："
        "一个 `vector` + `lower_bound` 就是全部。"
    ),
    input_format="第一行 `n`；第二行 `n` 个整数（1 ≤ n ≤ 2×10⁵，|元素| ≤ 10⁹）。",
    output_format="一行，严格 LIS 长度。",
    constraints_md="- 1 ≤ n ≤ 2×10⁵",
    inputs=[
        "8\n1 3 2 3 1 4 2 5\n",
        "5\n5 4 3 2 1\n",
        "6\n1 2 3 4 5 6\n",
        "1\n7\n",
        "10\n2 2 2 2 3 3 3 1 9 9\n",
        _rand_lis_case(),
    ],
    samples=2,
    oracle=_oracle_17,
    solution=r'''#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;
int main() {
    int n;
    scanf("%d", &n);
    vector<int> a(n), tails;
    for (int k = 0; k < n; k++) scanf("%d", &a[k]);
    for (int k = 0; k < n; k++) {
        auto it = lower_bound(tails.begin(), tails.end(), a[k]);  /* 严格 → lower */
        if (it == tails.end()) tails.push_back(a[k]);
        else *it = a[k];
    }
    printf("%d\n", (int)tails.size());
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <set>
using namespace std;
/* 另一套：set 维护所有「结尾候选」。每次把 >= x 的最小者删掉、放进 x，
   集合大小就是当前 LIS 长度——性质与 tails 法等价，实现完全不同 */
int main() {
    int n;
    cin >> n;
    set<int> s;
    for (int k = 0; k < n; k++) {
        int x; cin >> x;
        auto it = s.lower_bound(x);
        if (it != s.end()) s.erase(it);
        s.insert(x);
    }
    cout << s.size() << "\n";
    return 0;
}
''',
)


def _oracle_18(text: str) -> str:
    lines = text.rstrip("\n").split("\n")
    s, t = lines[0], lines[1]
    m, n = len(s), len(t)
    prev = [0] * (n + 1)
    for i in range(1, m + 1):
        cur = [0] * (n + 1)
        for j in range(1, n + 1):
            if s[i - 1] == t[j - 1]:
                cur[j] = prev[j - 1] + 1
            elif prev[j] >= cur[j - 1]:
                cur[j] = prev[j]
            else:
                cur[j] = cur[j - 1]
        prev = cur
    return "%d\n" % prev[n]

add(
    title="最长公共子序列 LCS",
    section="技巧特训 · C/C++",
    difficulty=3, score=25, tags=["技巧特训", "LCS", "DP", "滚动数组"],
    statement_md=(
        "读入两个字符串 `s`、`t`，输出最长公共子序列（LCS）的长度。\n\n"
        "★ 技巧点：二维 DP `f[i][j] = (sᵢ==tⱼ) ? f[i-1][j-1]+1 : max(f[i-1][j], f[i][j-1])`。"
        "空间优化：每一行只依赖上一行，**滚动两行**即可，"
        "2000×2000 的 int 表从 16 MB 压到 16 KB——滚动数组是所有二维 DP 的通用省法。"
    ),
    input_format="两行，各一个字符串（长度 1 ≤ |s|,|t| ≤ 2000，仅小写字母）。",
    output_format="一行，LCS 长度。",
    constraints_md="- 1 ≤ |s|, |t| ≤ 2000",
    inputs=[
        "abcde\nace\n",
        "abc\nabc\n",
        "abc\nxyz\n",
        "aggtab\naxtxbaygt\n",
        "aaaaaaaaaa\naaabaaaa\n",
    ],
    samples=2,
    oracle=_oracle_18,
    solution=r'''#include <cstdio>
#include <cstring>
#include <vector>
#include <algorithm>
using namespace std;
int main() {
    static char s[2005], t[2005];
    scanf("%s %s", s, t);
    int m = (int)strlen(s), n = (int)strlen(t);
    vector<vector<int> > f(2, vector<int>(n + 1, 0));
    int cur = 0;
    for (int i = 1; i <= m; i++) {
        cur ^= 1;                    /* 滚动两行：cur 写，cur^1 读 */
        for (int j = 1; j <= n; j++) {
            if (s[i - 1] == t[j - 1])
                f[cur][j] = f[cur ^ 1][j - 1] + 1;
            else
                f[cur][j] = max(f[cur ^ 1][j], f[cur][j - 1]);
        }
    }
    printf("%d\n", f[cur][n]);
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
using namespace std;
int main() {
    string s, t;
    cin >> s >> t;
    int m = s.size(), n = t.size();
    vector<vector<int> > f(m + 1, vector<int>(n + 1, 0));   /* 全量表 */
    for (int i = 1; i <= m; i++)
        for (int j = 1; j <= n; j++) {
            if (s[i - 1] == t[j - 1]) f[i][j] = f[i - 1][j - 1] + 1;
            else f[i][j] = max(f[i - 1][j], f[i][j - 1]);
        }
    cout << f[m][n] << "\n";
    return 0;
}
''',
)


def _oracle_19(text: str) -> str:
    d = text.split()
    a, b, m = int(d[0]), int(d[1]), int(d[2])
    return "%d\n" % pow(a, b, m)

add(
    title="快速幂（C++）",
    section="技巧特训 · C/C++",
    difficulty=2, score=15, tags=["技巧特训", "快速幂", "位运算", "取模"],
    statement_md=(
        "读入 `a b m`，输出 `a^b mod m`（b 最大 10¹⁸）。\n\n"
        "★ 技巧点：手写快速幂——指数按二进制拆位：底数每步自乘（平方），"
        "指数末位为 1 就把当前底数乘进答案。**乘法在取模前可能溢出 long long**"
        "（10⁹ × 10⁹ = 10¹⁸ 压线），本题 m ≤ 10⁹ 故安全，若 m 更大需 __int128 或慢乘。"
        "这是 C++ 里没有内置 powmod 时必须会的标准件。"
    ),
    input_format="一行 `a b m`（1 ≤ a, m ≤ 10⁹；0 ≤ b ≤ 10¹⁸）。",
    output_format="一行，`a^b mod m`。",
    constraints_md="- 1 ≤ a, m ≤ 10⁹\n- 0 ≤ b ≤ 10¹⁸",
    inputs=[
        "2 10 1000\n",
        "3 0 7\n",
        "2 62 1000000007\n",
        "5 100 1000000007\n",
        "123456789 999999999999999998 998244353\n",
    ],
    samples=2,
    oracle=_oracle_19,
    solution=r'''#include <cstdio>
int main() {
    long long a, b, m;
    scanf("%lld %lld %lld", &a, &b, &m);
    long long r = 1 % m, base = a % m;
    while (b > 0) {
        if (b & 1) r = r * base % m;
        base = base * base % m;
        b >>= 1;
    }
    printf("%lld\n", r);
    return 0;
}
''',
    alt=r'''#include <iostream>
using namespace std;
long long mpow(long long base, long long e, long long m) {   /* 递归版 */
    if (e == 0) return 1 % m;
    long long half = mpow(base, e / 2, m);
    long long r = half * half % m;
    if (e & 1) r = r * (base % m) % m;
    return r;
}
int main() {
    long long a, b, m;
    cin >> a >> b >> m;
    cout << mpow(a, b, m) << "\n";
    return 0;
}
''',
)


def _oracle_20(text: str) -> str:
    d = text.split()
    n = int(d[0])
    a = [int(v) for v in d[1:1 + n]]
    cnt = 0
    for i in range(n):
        for j in range(i + 1, n):
            if a[i] > a[j]:
                cnt += 1
    return "%d\n" % cnt

add(
    title="逆序对 归并",
    section="技巧特训 · C/C++",
    difficulty=4, score=25, tags=["技巧特训", "归并排序", "分治", "逆序对"],
    statement_md=(
        "读入 `n` 个整数，输出**逆序对**个数（i < j 且 aᵢ > aⱼ 的对数）。"
        "n 可达 2×10⁵，O(n²) 暴力会超时。\n\n"
        "★ 技巧点：**归并排序顺手数逆序对**——合并两段有序数组时，"
        "右半的元素被拿走之前，左半剩余的每一个都与它构成逆序对，"
        "`cnt += 左半剩余个数` 一句完事。这是分治的经典应用："
        "排序的过程就是统计跨段逆序对的过程。树状数组 + 离散化（alt 解）是另一条路。"
    ),
    input_format="第一行 `n`；第二行 `n` 个整数（1 ≤ n ≤ 2×10⁵，|元素| ≤ 10⁹）。",
    output_format="一行，逆序对个数（long long 内）。",
    constraints_md="- 1 ≤ n ≤ 2×10⁵",
    inputs=[
        "5\n3 1 4 1 5\n",
        "4\n4 3 2 1\n",
        "1\n0\n",
        "6\n1 2 3 4 5 6\n",
        "10\n2 2 2 2 3 3 3 1 9 9\n",
        _rand_inv_case(),
    ],
    samples=2,
    oracle=_oracle_20,
    solution=r'''#include <cstdio>
#include <vector>
using namespace std;
long long cnt = 0;
void msort(vector<int> &a, vector<int> &tmp, int l, int r) {
    if (r - l <= 1) return;
    int mid = (l + r) / 2;
    msort(a, tmp, l, mid);
    msort(a, tmp, mid, r);
    int i = l, j = mid, k = l;
    while (i < mid && j < r) {
        if (a[i] <= a[j]) tmp[k++] = a[i++];      /* 相等不算逆序 */
        else {
            cnt += mid - i;                       /* 右半出牌，左半剩余全成对 */
            tmp[k++] = a[j++];
        }
    }
    while (i < mid) tmp[k++] = a[i++];
    while (j < r) tmp[k++] = a[j++];
    for (int p = l; p < r; p++) a[p] = tmp[p];
}
int main() {
    int n;
    scanf("%d", &n);
    vector<int> a(n), tmp(n);
    for (int k = 0; k < n; k++) scanf("%d", &a[k]);
    msort(a, tmp, 0, n);
    printf("%lld\n", cnt);
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
/* 另一套：树状数组 + 离散化。从右往左插，问左边已插入的、严格比当前小的个数 */
int n;
vector<int> bit;
void add(int i) {
    for (; i <= n; i += i & (-i)) bit[i]++;
}
long long ask(int i) {
    long long s = 0;
    for (; i > 0; i -= i & (-i)) s += bit[i];
    return s;
}
int main() {
    cin >> n;
    vector<long long> a(n);
    for (int k = 0; k < n; k++) cin >> a[k];
    vector<long long> vals(a);
    sort(vals.begin(), vals.end());
    vals.erase(unique(vals.begin(), vals.end()), vals.end());
    bit.assign(n + 1, 0);
    long long cnt = 0;
    for (int k = n - 1; k >= 0; k--) {
        int r = (int)(lower_bound(vals.begin(), vals.end(), a[k]) - vals.begin()) + 1;
        cnt += ask(r - 1);            /* 严格更小的已插入个数 */
        add(r);
    }
    cout << cnt << "\n";
    return 0;
}
''',
)


# --------------------------------------------------------------------- #
#  进阶套路（difficulty 2~4，第二批量）
# --------------------------------------------------------------------- #

def _oracle_21(text: str) -> str:
    d = text.split()
    n = int(d[0])
    rows = []
    for i in range(n):
        rows.append((d[1 + 2 * i], int(d[2 + 2 * i]), i))
    rows.sort(key=lambda t: (-t[1], t[2]))
    return "".join("%s %d\n" % (t[0], t[1]) for t in rows)

add(
    title="成绩表稳定排序",
    section="技巧特训 · C/C++",
    difficulty=2, score=15, tags=["技巧特训", "struct", "stable_sort", "多关键字"],
    statement_md=(
        "读入 `n` 个学生的姓名与成绩，按**成绩从高到低**输出；"
        "**成绩相同的学生保持输入顺序**（这就是「稳定」）。每行输出 `姓名 成绩`。\n\n"
        "★ 技巧点：`stable_sort(begin, end, cmp)` 在比较函数只比成绩时，"
        "天然保证相等元素不换位；若用普通 `sort`，就必须在结构体里记下原始下标 "
        "`id`，比较时补一句 `if (score 相同) return id 更小`——这是"
        "「多关键字排序」的标准写法。两者都能过，但 `stable_sort` 少一个字段、"
        "也少一次排序键的维护，是成绩/排名类题目的首选。"
    ),
    input_format="第一行 `n`；随后 `n` 行每行 `姓名 成绩`（姓名不含空格）。",
    output_format="`n` 行，每行 `姓名 成绩`。",
    constraints_md="- 1 ≤ n ≤ 10⁵\n- 姓名长度 ≤ 20（小写字母）\n- 0 ≤ 成绩 ≤ 10⁹",
    inputs=[
        "5\nalice 90\nbob 85\ncarol 90\ndave 85\neve 100\n",
        "1\nsolo 0\n",
        "4\na 5\nb 5\nc 5\nd 5\n",
        "3\nx -1\ny 1000000000\nz -1\n",
        "6\nn1 70\nn2 60\nn3 70\nn4 80\nn5 60\nn6 80\n",
    ],
    samples=2,
    oracle=_oracle_21,
    solution=r'''#include <cstdio>
#include <algorithm>
using namespace std;
struct Stu { char name[32]; long long score; };
bool byScore(const Stu& a, const Stu& b) { return a.score > b.score; }
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    Stu* v = new Stu[n];
    for (int i = 0; i < n; i++) scanf("%s %lld", v[i].name, &v[i].score);
    stable_sort(v, v + n, byScore);   /* 只比成绩，相等时自动保持原顺序 */
    for (int i = 0; i < n; i++) printf("%s %lld\n", v[i].name, v[i].score);
    delete[] v;
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;
struct Stu { string name; long long score; int id; };
int main() {
    int n;
    scanf("%d", &n);
    vector<Stu> v(n);
    for (int i = 0; i < n; i++) {
        char buf[64];
        scanf("%s %lld", buf, &v[i].score);
        v[i].name = buf;
        v[i].id = i;                  /* 普通 sort 要靠 id 补稳定性 */
    }
    sort(v.begin(), v.end(), [](const Stu& a, const Stu& b) {
        if (a.score != b.score) return a.score > b.score;
        return a.id < b.id;
    });
    for (size_t i = 0; i < v.size(); i++)
        printf("%s %lld\n", v[i].name.c_str(), v[i].score);
    return 0;
}
''',
)


def _oracle_22(text: str) -> str:
    d = text.split()
    n = int(d[0]); k = int(d[1])
    a = [int(x) for x in d[2:2 + n]]
    a.sort(reverse=True)
    return " ".join(map(str, a[:k])) + "\n"

add(
    title="前 k 大的数",
    section="技巧特训 · C/C++",
    difficulty=3, score=20, tags=["技巧特训", "priority_queue", "小根堆", "TopK"],
    statement_md=(
        "读入 `n` 个数和 `k`，输出其中最大的 `k` 个（从大到小，空格分隔）。\n\n"
        "★ 技巧点：**用「小根堆」求 Top-K**。维护一个大小不超过 `k` 的小根堆——"
        "新数进来就 `push`，堆超过 `k` 就 `pop` 掉堆顶（当前 k 个里最小的）。"
        "扫完一遍，堆里就是最大的 `k` 个，复杂度 `O(n log k)`，内存只有 `O(k)`；"
        "`n = 10⁷、k = 10` 时比全部排序快得多。\n\n"
        "写法：`priority_queue<int, vector<int>, greater<int>>` 是小根堆；"
        "**只写 `priority_queue<int>` 是大根堆**——这两个的区别是本题最容易踩的坑。"
        "最后把堆里的数倒出来再逆序输出。"
    ),
    input_format="第一行 `n k`；第二行 `n` 个整数。",
    output_format="一行 `k` 个整数，从大到小，空格分隔。",
    constraints_md="- 1 ≤ k ≤ n ≤ 10⁵\n- |元素| ≤ 10⁹",
    inputs=[
        "5 3\n1 5 3 9 7\n",
        "1 1\n42\n",
        "6 6\n-3 -1 -2 -5 -4 -6\n",
        "8 2\n5 5 5 5 5 5 5 1\n",
        "7 4\n1000000000 -1000000000 0 7 -7 3 3\n",
    ],
    samples=2,
    oracle=_oracle_22,
    solution=r'''#include <cstdio>
#include <vector>
#include <queue>
#include <functional>
using namespace std;
int main() {
    int n, k;
    scanf("%d %d", &n, &k);
    priority_queue<int, vector<int>, greater<int>> pq;   /* ★ 小根堆 */
    for (int i = 0; i < n; i++) {
        int x; scanf("%d", &x);
        pq.push(x);
        if ((int)pq.size() > k) pq.pop();                /* 挤掉最小的 */
    }
    vector<int> res;
    while (!pq.empty()) { res.push_back(pq.top()); pq.pop(); }
    for (int i = (int)res.size() - 1; i >= 0; i--)
        printf("%d%c", res[i], i ? ' ' : '\n');
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <queue>
using namespace std;
int main() {
    int n, k;
    scanf("%d %d", &n, &k);
    priority_queue<int> pq;              /* 默认大根堆，全装进去 */
    for (int i = 0; i < n; i++) { int x; scanf("%d", &x); pq.push(x); }
    for (int i = 0; i < k; i++) {
        printf("%d%c", pq.top(), i + 1 == k ? '\n' : ' ');
        pq.pop();
    }
    return 0;
}
''',
)


def _oracle_23(text: str) -> str:
    from itertools import permutations
    d = text.split()
    n = int(d[0])
    a = [int(x) for x in d[1:1 + n]]
    k = int(d[1 + n])
    perms = sorted(permutations(sorted(a)))
    return " ".join(map(str, perms[k - 1])) + "\n"

add(
    title="下一个排列推 k 次",
    section="技巧特训 · C/C++",
    difficulty=3, score=20, tags=["技巧特训", "next_permutation", "全排列", "字典序"],
    statement_md=(
        "读入 `n`、`n` 个互不相同的整数、以及 `k`，"
        "先把它们升序排列，再输出**字典序第 `k` 个**排列（`k` 从 1 起，空格分隔）。\n\n"
        "★ 技巧点：`next_permutation(first, last)` 就地把区间改成「字典序下一个排列」，"
        "返回 `false` 表示已到最后一个。求第 `k` 个就是先 `sort`，再循环 `k-1` 次。"
        "它还能当**去重排列生成器**用：有重复元素时配合 `sort` 也不会产出重复排列。\n\n"
        "另一套解是手写「找降序后缀 → 交换 → 反转」三步，理解它比背 STL 更有用——"
        "很多面试题正考这个。"
    ),
    input_format="第一行 `n`；第二行 `n` 个互不相同的整数；第三行 `k`。",
    output_format="一行 `n` 个整数。",
    constraints_md="- 1 ≤ n ≤ 8\n- 1 ≤ k ≤ n!\n- |元素| ≤ 10⁹",
    inputs=[
        "3\n3 1 2\n4\n",
        "1\n7\n1\n",
        "4\n1 2 3 4\n24\n",
        "5\n5 4 3 2 1\n120\n",
        "3\n0 -1 1\n2\n",
    ],
    samples=2,
    oracle=_oracle_23,
    solution=r'''#include <cstdio>
#include <algorithm>
using namespace std;
int a[10];
int main() {
    int n, k;
    scanf("%d", &n);
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    scanf("%d", &k);
    sort(a, a + n);                          /* 从最小排列出发 */
    for (int t = 1; t < k; t++) next_permutation(a, a + n);
    for (int i = 0; i < n; i++) printf("%d%c", a[i], i + 1 == n ? '\n' : ' ');
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <algorithm>
using namespace std;
int a[10];
int main() {
    int n, k;
    scanf("%d", &n);
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    scanf("%d", &k);
    sort(a, a + n);
    for (int t = 1; t < k; t++) {
        int i = n - 2;
        while (i >= 0 && a[i] >= a[i + 1]) i--;   /* 找最右的升序对 */
        int j = n - 1;
        while (a[j] <= a[i]) j--;                 /* 找最小的更大值 */
        swap(a[i], a[j]);
        reverse(a + i + 1, a + n);                /* 后缀反转成最小 */
    }
    for (int i = 0; i < n; i++) printf("%d%c", a[i], i + 1 == n ? '\n' : ' ');
    return 0;
}
''',
)


def _oracle_24(text: str) -> str:
    d = text.split()
    n = int(d[0])
    a = [int(x) for x in d[1:1 + n]]
    pre = []
    s = 0
    for x in a:
        s += x
        pre.append(s)
    prod = 1
    for x in a:
        prod = prod * (x % 1000000007) % 1000000007
    best = pre[0]
    bi = 1
    for i, v in enumerate(pre, 1):
        if v > best:
            best = v
            bi = i
    return " ".join(map(str, pre)) + "\n%d\n%d %d\n" % (prod, best, bi)

add(
    title="前缀和与累计乘积",
    section="技巧特训 · C/C++",
    difficulty=2, score=15, tags=["技巧特训", "accumulate", "partial_sum", "iota"],
    statement_md=(
        "读入 `n` 个整数，输出三行：\n\n"
        "1. 前缀和（`n` 个数，空格分隔）\n"
        "2. 全部数的乘积对 `1000000007` 取模\n"
        "3. 最大的前缀和，以及它第一次出现的下标（从 1 起）\n\n"
        "★ 技巧点：`<numeric>` 里三个轮子——`partial_sum` 一次算完前缀和，"
        "`accumulate` 带自定义函数做累计乘积，`iota` 把 `1..n` 填进下标数组。"
        "`accumulate` 的初值一定要写成 `1LL`（乘积）或 `0LL`（求和）："
        "写 `0` 或 `1` 会让整个计算退回 `int`，`n = 10⁵` 时乘积早就溢出了。\n\n"
        "本题元素可为负，所以「最大前缀和」不能用「前缀和单调递增」的直觉，"
        "得老老实实扫一遍。"
    ),
    input_format="第一行 `n`；第二行 `n` 个整数。",
    output_format="三行，如题面所述。",
    constraints_md="- 1 ≤ n ≤ 10⁵\n- |aᵢ| ≤ 10⁴",
    inputs=[
        "5\n1 -2 3 4 -1\n",
        "1\n7\n",
        "4\n0 0 0 0\n",
        "3\n-5 -1 -3\n",
        "6\n2 3 -10 5 5 5\n",
    ],
    samples=2,
    oracle=_oracle_24,
    solution=r'''#include <cstdio>
#include <vector>
#include <numeric>
#include <algorithm>
using namespace std;
const long long MOD = 1000000007LL;
int main() {
    int n;
    scanf("%d", &n);
    vector<long long> a(n), pre(n);
    for (int i = 0; i < n; i++) scanf("%lld", &a[i]);
    partial_sum(a.begin(), a.end(), pre.begin());       /* ★ 前缀和 */
    auto mulmod = [](long long x, long long y) {
        long long v = (y % MOD + MOD) % MOD;            /* 负数先转正 */
        return x * v % MOD;
    };
    long long prod = accumulate(a.begin(), a.end(), 1LL, mulmod);
    vector<int> idx(n);
    iota(idx.begin(), idx.end(), 1);                    /* 1..n */
    int bi = *max_element(idx.begin(), idx.end(), [&](int x, int y) {
        if (pre[x - 1] != pre[y - 1]) return pre[x - 1] < pre[y - 1];
        return x > y;                                   /* 并列取更小下标 */
    });
    for (int i = 0; i < n; i++) printf("%lld%c", pre[i], i + 1 == n ? '\n' : ' ');
    printf("%lld\n%lld %d\n", prod, pre[bi - 1], bi);
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <vector>
#include <numeric>
using namespace std;
const long long MOD = 1000000007LL;
int main() {
    int n;
    scanf("%d", &n);
    vector<long long> a(n);
    for (int i = 0; i < n; i++) scanf("%lld", &a[i]);
    long long s = 0, prod = 1, best = 0, bi = 1;
    for (int i = 0; i < n; i++) {
        s += a[i];
        long long v = (a[i] % MOD + MOD) % MOD;   /* 负数先转正再取模 */
        prod = prod * v % MOD;
        if (i == 0 || s > best) { best = s; bi = i + 1; }
        printf("%lld%c", s, i + 1 == n ? '\n' : ' ');
    }
    printf("%lld\n%lld %lld\n", prod, best, bi);
    return 0;
}
''',
)


def _oracle_25(text: str) -> str:
    d = text.split()
    n = int(d[0])
    a = [int(x) for x in d[1:1 + n]]
    o = 0
    mx = 0
    tot = 0
    for x in a:
        o |= x
        pc = bin(x).count("1")
        if pc > mx:
            mx = pc
        tot += pc
    return "%d\n%d\n%d\n" % (o, mx, tot)

add(
    title="bitset 做按位统计",
    section="技巧特训 · C/C++",
    difficulty=3, score=20, tags=["技巧特训", "bitset", "位运算", "popcount"],
    statement_md=(
        "读入 `n` 个非负整数（每个 < 2⁶⁰），输出三行：\n\n"
        "1. 所有数**按位或**的结果（十进制）\n"
        "2. 单个数里二进制 1 的个数的最大值\n"
        "3. 所有数二进制 1 的个数之和\n\n"
        "★ 技巧点：`bitset<64>(x).count()` 直接数 1，`b1 | b2` 直接按位或——"
        "定长位集让「每一位」变成容器的元素，写起来比手写移位干净。"
        "追求速度就用编译器内建 `__builtin_popcountll(x)`（一条硬件指令）；"
        "想手写则用 `while (x) { x &= x - 1; cnt++; }`——"
        "`x & (x-1)` 每次抹掉最低位的 1，循环次数就是 1 的个数。"
    ),
    input_format="第一行 `n`；第二行 `n` 个整数。",
    output_format="三行，如题面所述。",
    constraints_md="- 1 ≤ n ≤ 10⁵\n- 0 ≤ aᵢ < 2⁶⁰",
    inputs=[
        "3\n1 2 4\n",
        "1\n0\n",
        "4\n7 7 7 7\n",
        "5\n1152921504606846975 1 2 3 4\n",
        "6\n123456789012345678 987654321098765432 1 0 5 9\n",
    ],
    samples=2,
    oracle=_oracle_25,
    solution=r'''#include <cstdio>
#include <bitset>
using namespace std;
int main() {
    int n;
    scanf("%d", &n);
    unsigned long long orv = 0;
    int mx = 0, tot = 0;
    for (int i = 0; i < n; i++) {
        unsigned long long x;
        scanf("%llu", &x);
        orv |= x;                                  /* 按位或 */
        int pc = (int)bitset<64>(x).count();       /* ★ 数 1 */
        if (pc > mx) mx = pc;
        tot += pc;
    }
    printf("%llu\n%d\n%d\n", orv, mx, tot);
    return 0;
}
''',
    alt=r'''#include <cstdio>
using namespace std;
int main() {
    int n;
    scanf("%d", &n);
    unsigned long long orv = 0;
    int mx = 0, tot = 0;
    for (int i = 0; i < n; i++) {
        unsigned long long x;
        scanf("%llu", &x);
        orv |= x;
        int pc = __builtin_popcountll(x);          /* 硬件指令版 */
        if (pc > mx) mx = pc;
        tot += pc;
    }
    printf("%llu\n%d\n%d\n", orv, mx, tot);
    return 0;
}
''',
)


def _oracle_26(text: str) -> str:
    from collections import Counter
    d = text.split()
    n = int(d[0])
    words = d[1:1 + n]
    c = Counter(words)
    items = sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))
    return "".join("%s %d\n" % (w, m) for w, m in items)

add(
    title="词频统计再排序",
    section="技巧特训 · C/C++",
    difficulty=2, score=15, tags=["技巧特训", "unordered_map", "词频", "排序"],
    statement_md=(
        "读入 `n` 个单词（只含小写字母），统计每个单词出现的次数，"
        "按「次数从高到低、次数相同按字典序从小到大」输出，每行 `单词 次数`。\n\n"
        "★ 技巧点：`unordered_map<string,int>` 做桶计数是 O(1) 摊还，"
        "但**它本身无序**——想按次数排序必须先倒进 `vector<pair<...>>` 再 `sort`。"
        "反过来说，如果只要「按单词字典序」输出，直接用 `map` 就够了，"
        "连 sort 都省了。选容器先问自己：**最后按什么顺序输出？**"
    ),
    input_format="第一行 `n`；第二行 `n` 个单词（空格分隔）。",
    output_format="每行 `单词 次数`，按题面规则排序。",
    constraints_md="- 1 ≤ n ≤ 10⁵\n- 单词长度 ≤ 20，只含小写字母",
    time_limit_ms=2000,
    inputs=[
        "6\napple banana apple cherry banana apple\n",
        "1\nz\n",
        "5\na b c d e\n",
        "4\nbb aa aa bb\n",
        "7\nx x y y z z z\n",
    ],
    samples=2,
    oracle=_oracle_26,
    solution=r'''#include <cstdio>
#include <string>
#include <vector>
#include <unordered_map>
#include <algorithm>
using namespace std;
int main() {
    int n;
    scanf("%d", &n);
    unordered_map<string, int> mp;
    mp.reserve((size_t)n * 2 + 10);
    char buf[64];
    for (int i = 0; i < n; i++) {
        scanf("%s", buf);
        mp[buf]++;                       /* 桶计数 */
    }
    vector<pair<string, int>> v(mp.begin(), mp.end());   /* 倒进 vector 才能排序 */
    sort(v.begin(), v.end(), [](const pair<string, int>& a,
                                const pair<string, int>& b) {
        if (a.second != b.second) return a.second > b.second;
        return a.first < b.first;
    });
    for (size_t i = 0; i < v.size(); i++)
        printf("%s %d\n", v[i].first.c_str(), v[i].second);
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <string>
#include <vector>
#include <map>
#include <algorithm>
using namespace std;
int main() {
    int n;
    scanf("%d", &n);
    map<string, int> mp;                 /* 有序 map：遍历即字典序 */
    char buf[64];
    for (int i = 0; i < n; i++) { scanf("%s", buf); mp[buf]++; }
    vector<pair<string, int>> v;
    for (map<string, int>::iterator it = mp.begin(); it != mp.end(); ++it)
        v.push_back(*it);
    stable_sort(v.begin(), v.end(),
                [](const pair<string, int>& a, const pair<string, int>& b) {
                    return a.second > b.second;   /* 只按次数，稳定排序保住字典序 */
                });
    for (size_t i = 0; i < v.size(); i++)
        printf("%s %d\n", v[i].first.c_str(), v[i].second);
    return 0;
}
''',
)


def _oracle_27(text: str) -> str:
    d = text.split()
    n = int(d[0])
    a = [int(x) for x in d[1:1 + n]]
    u = sorted(set(a))
    rank = {v: i + 1 for i, v in enumerate(u)}
    return "%d\n%s\n%s\n" % (len(u), " ".join(map(str, u)),
                             " ".join(str(rank[x]) for x in a))

add(
    title="排序去重与离散化",
    section="技巧特训 · C/C++",
    difficulty=3, score=20, tags=["技巧特训", "unique", "离散化", "lower_bound"],
    statement_md=(
        "读入 `n` 个整数，输出三行：\n\n"
        "1. 去重后有多少个不同的值\n"
        "2. 所有不同的值，从小到大（空格分隔）\n"
        "3. 原数组每个元素的「名次」——比它小的不同值的个数 + 1\n\n"
        "★ 技巧点：**排序去重三件套**\n\n"
        "```\n"
        "sort(a.begin(), a.end());\n"
        "a.erase(unique(a.begin(), a.end()), a.end());\n"
        "```\n\n"
        "`unique` 只是把重复元素挪到末尾并返回「新末尾」，**并不真的删除**，"
        "所以必须自己 `erase`——这是最经典的坑。\n\n"
        "名次用 `lower_bound` 一查就有：`rank = lower_bound(u, x) - u.begin() + 1`，"
        "这就是**离散化**——把 `±10⁹` 的大值压成 `1..m` 的小下标，"
        "之后就能拿它当树状数组 / 计数数组的下标用。"
    ),
    input_format="第一行 `n`；第二行 `n` 个整数。",
    output_format="三行，如题面所述。",
    constraints_md="- 1 ≤ n ≤ 10⁵\n- |元素| ≤ 10⁹",
    inputs=[
        "6\n5 3 5 1 3 9\n",
        "1\n0\n",
        "4\n-1 -1 -1 -1\n",
        "5\n1000000000 -1000000000 0 0 7\n",
        "8\n3 1 4 1 5 9 2 6\n",
    ],
    samples=2,
    oracle=_oracle_27,
    solution=r'''#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;
int main() {
    int n;
    scanf("%d", &n);
    vector<int> a(n);
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    vector<int> u = a;
    sort(u.begin(), u.end());
    u.erase(unique(u.begin(), u.end()), u.end());   /* ★ 排序去重三件套 */
    printf("%d\n", (int)u.size());
    for (size_t i = 0; i < u.size(); i++)
        printf("%d%c", u[i], i + 1 == u.size() ? '\n' : ' ');
    for (int i = 0; i < n; i++) {
        int r = (int)(lower_bound(u.begin(), u.end(), a[i]) - u.begin()) + 1;
        printf("%d%c", r, i + 1 == n ? '\n' : ' ');
    }
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <vector>
#include <map>
using namespace std;
int main() {
    int n;
    scanf("%d", &n);
    vector<int> a(n);
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    map<int, int> rank;                 /* 有序 map 天然去重 + 排序 */
    for (int i = 0; i < n; i++) rank[a[i]] = 0;
    int id = 0;
    for (map<int, int>::iterator it = rank.begin(); it != rank.end(); ++it)
        it->second = ++id;
    printf("%d\n", id);
    id = 0;
    for (map<int, int>::iterator it = rank.begin(); it != rank.end(); ++it) {
        ++id;
        printf("%d%c", it->first, id == (int)rank.size() ? '\n' : ' ');
    }
    for (int i = 0; i < n; i++)
        printf("%d%c", rank[a[i]], i + 1 == n ? '\n' : ' ');
    return 0;
}
''',
)


def _rand_big_case_28() -> str:
    """28 号的大用例：n = q = 30000，操作五五开，固定种子可复现。"""
    import random
    rnd = random.Random(20261019)
    n = q = 30000
    lines = ["%d %d" % (n, q)]
    lines.append(" ".join(str(rnd.randint(-1000, 1000)) for _ in range(n)))
    for _ in range(q):
        if rnd.random() < 0.5:
            lines.append("1 %d %d" % (rnd.randint(1, n), rnd.randint(-1000, 1000)))
        else:
            l = rnd.randint(1, n)
            r = rnd.randint(l, n)
            lines.append("2 %d %d" % (l, r))
    return "\n".join(lines) + "\n"


def _oracle_28(text: str) -> str:
    d = text.split()
    i = 0
    n = int(d[i]); i += 1
    q = int(d[i]); i += 1
    a = [int(d[i + k]) for k in range(n)]
    i += n
    B = 200
    nb = (n + B - 1) // B
    blk = [0] * nb
    for k in range(n):
        blk[k // B] += a[k]
    out = []
    for _ in range(q):
        op = d[i]
        if op == "1":
            pos = int(d[i + 1]) - 1
            v = int(d[i + 2])
            i += 3
            a[pos] += v
            blk[pos // B] += v
        else:
            l = int(d[i + 1]) - 1
            r = int(d[i + 2]) - 1
            i += 3
            b1 = l // B
            b2 = r // B
            if b1 == b2:
                s = 0
                for k in range(l, r + 1):
                    s += a[k]
            else:
                s = 0
                for k in range(l, (b1 + 1) * B):
                    s += a[k]
                for b in range(b1 + 1, b2):
                    s += blk[b]
                for k in range(b2 * B, r + 1):
                    s += a[k]
            out.append(str(s))
    return "".join(x + "\n" for x in out)

add(
    title="单点修改与区间求和",
    section="技巧特训 · C/C++",
    difficulty=4, score=25, tags=["技巧特训", "树状数组", "Fenwick", "lowbit"],
    statement_md=(
        "维护一个长度为 `n` 的数组，支持 `q` 次操作：\n\n"
        "- `1 i v`：把 `a[i]` 加上 `v`\n"
        "- `2 l r`：输出 `a[l] + a[l+1] + ... + a[r]`\n\n"
        "★ 技巧点：**树状数组（Fenwick）**。核心只有两个循环、一个 `lowbit`：\n\n"
        "```\n"
        "lowbit(i) = i & -i\n"
        "add(i, v)   : for (; i <= n; i += i & -i) t[i] += v;\n"
        "sum(i)      : for (; i > 0; i -= i & -i) s += t[i];\n"
        "```\n\n"
        "`t[i]` 存的是「以 i 结尾、长度为 lowbit(i)」那一段的和，所以 `sum(i)` "
        "跳着累加正好不重不漏。单点加 `O(log n)`、前缀和 `O(log n)`、"
        "区间和 = 两个前缀和相减。代码比线段树短一半，常数也小——"
        "**只要操作是「单点改 + 前缀查」，闭眼选树状数组**。\n\n"
        "另一套解用迭代式线段树（自底向上），思路对照着看更清楚。"
    ),
    input_format=(
        "第一行 `n q`；第二行 `n` 个整数；\n"
        "随后 `q` 行，每行 `1 i v` 或 `2 l r`。"
    ),
    output_format="每个 `2` 操作输出一行区间和。",
    constraints_md="- 1 ≤ n, q ≤ 3×10⁴\n- |元素|、|v| ≤ 10³\n- 保证 1 ≤ i, l ≤ r ≤ n",
    time_limit_ms=2000,
    inputs=[
        "5 4\n1 2 3 4 5\n2 1 3\n1 2 10\n2 1 5\n2 3 3\n",
        "1 2\n7\n2 1 1\n1 1 -7\n",
        "3 3\n0 0 0\n1 1 5\n1 3 5\n2 1 3\n",
        _rand_big_case_28(),
    ],
    samples=2,
    oracle=_oracle_28,
    solution=r'''#include <cstdio>
#include <vector>
using namespace std;
int n, q;
vector<long long> t;

void add(int i, long long v) {
    for (; i <= n; i += i & -i) t[i] += v;    /* ★ lowbit 往上跳 */
}

long long sum(int i) {
    long long s = 0;
    for (; i > 0; i -= i & -i) s += t[i];     /* ★ lowbit 往下跳 */
    return s;
}

int main() {
    scanf("%d %d", &n, &q);
    t.assign(n + 1, 0);
    for (int i = 1; i <= n; i++) {
        long long x;
        scanf("%lld", &x);
        add(i, x);
    }
    while (q--) {
        int op;
        scanf("%d", &op);
        if (op == 1) {
            int i; long long v;
            scanf("%d %lld", &i, &v);
            add(i, v);
        } else {
            int l, r;
            scanf("%d %d", &l, &r);
            printf("%lld\n", sum(r) - sum(l - 1));
        }
    }
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <vector>
using namespace std;
int main() {
    int n, q;
    scanf("%d %d", &n, &q);
    int sz = 1;
    while (sz < n) sz <<= 1;
    vector<long long> t(2 * sz, 0);           /* 迭代式线段树 */
    for (int i = 0; i < n; i++) scanf("%lld", &t[sz + i]);
    for (int i = sz - 1; i >= 1; i--) t[i] = t[2 * i] + t[2 * i + 1];
    while (q--) {
        int op;
        scanf("%d", &op);
        if (op == 1) {
            int pos; long long v;
            scanf("%d %lld", &pos, &v);
            int p = sz + pos - 1;
            t[p] += v;
            for (p >>= 1; p >= 1; p >>= 1) t[p] = t[2 * p] + t[2 * p + 1];
        } else {
            int l, r;
            scanf("%d %d", &l, &r);
            int a = sz + l - 1, b = sz + r;
            long long s = 0;
            while (a < b) {
                if (a & 1) s += t[a++];
                if (b & 1) s += t[--b];
                a >>= 1; b >>= 1;
            }
            printf("%lld\n", s);
        }
    }
    return 0;
}
''',
)


def _rand_big_case_29() -> str:
    """29 号的大用例：两个 500 位大整数，固定种子可复现。"""
    import random
    rnd = random.Random(20261019)

    def big():
        return str(rnd.randint(1, 9)) + "".join(str(rnd.randint(0, 9)) for _ in range(499))

    return big() + "\n" + big() + "\n"


def _oracle_29(text: str) -> str:
    lines = text.rstrip("\n").split("\n")
    return str(int(lines[0]) + int(lines[1])) + "\n"

add(
    title="高精度加法",
    section="技巧特训 · C/C++",
    difficulty=3, score=20, tags=["技巧特训", "高精度", "字符串模拟", "进位"],
    statement_md=(
        "读入两个正整数（每个最多 500 位，可能带前导零），输出它们的和"
        "（十进制，不带前导零；和为 0 时输出 `0`）。\n\n"
        "★ 技巧点：C++ 没有内置大整数，**只能拿字符串模拟竖式加法**：\n\n"
        "1. 两个串都 `reverse`，让低位对齐在下标 0\n"
        "2. 从低位往高位加，`carry` 记进位，每位 `s % 10` 留下、`s / 10` 进上去\n"
        "3. 加完后还要把 `carry` 补一位\n"
        "4. 结果再 `reverse` 回正常顺序，去掉前导零\n\n"
        "`long long` 上限约 9.2×10¹⁸（19 位），500 位的数必须走这条路。"
        "同样的框架改一改就能做高精度减法 / 乘法 / 阶乘。"
    ),
    input_format="两行，每行一个正整数（位数 ≤ 500）。",
    output_format="一行，两数之和。",
    constraints_md="- 1 ≤ 位数 ≤ 500\n- 输入可能有前导零",
    inputs=[
        "123\n456\n",
        "999\n1\n",
        "0\n0\n",
        "000123\n000077\n",
        _rand_big_case_29(),
    ],
    samples=2,
    oracle=_oracle_29,
    solution=r'''#include <cstdio>
#include <cstring>
#include <string>
#include <algorithm>
using namespace std;
int main() {
    char A[1005], B[1005];
    if (scanf("%s", A) != 1) return 0;
    scanf("%s", B);
    reverse(A, A + strlen(A));            /* 低位对齐到下标 0 */
    reverse(B, B + strlen(B));
    int na = (int)strlen(A), nb = (int)strlen(B);
    string res;
    int carry = 0;
    for (int i = 0; i < na || i < nb || carry; i++) {
        int s = carry;
        if (i < na) s += A[i] - '0';
        if (i < nb) s += B[i] - '0';
        res.push_back(char('0' + s % 10));
        carry = s / 10;
    }
    reverse(res.begin(), res.end());
    size_t p = 0;
    while (p + 1 < res.size() && res[p] == '0') p++;   /* 去前导零 */
    printf("%s\n", res.c_str() + p);
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <cstring>
#include <vector>
#include <algorithm>
using namespace std;
int main() {
    char A[1005], B[1005];
    if (scanf("%s %s", A, B) != 2) return 0;
    vector<int> x, y;
    for (int i = (int)strlen(A) - 1; i >= 0; i--) x.push_back(A[i] - '0');
    for (int i = (int)strlen(B) - 1; i >= 0; i--) y.push_back(B[i] - '0');
    size_t n = max(x.size(), y.size());
    x.resize(n + 1, 0);
    y.resize(n + 1, 0);
    for (size_t i = 0; i < n; i++) {
        x[i] += y[i];
        if (x[i] >= 10) { x[i] -= 10; x[i + 1]++; }   /* 进位 */
    }
    int hi = (int)n;
    while (hi > 0 && x[hi] == 0) hi--;
    for (int i = hi; i >= 0; i--) printf("%d", x[i]);
    printf("\n");
    return 0;
}
''',
)


def _rand_big_case_30() -> str:
    """30 号的大用例：n = 100000，固定种子可复现。"""
    import random
    rnd = random.Random(20261019)
    n = 100000
    k = rnd.randint(-50, 50)
    return ("%d %d\n" % (n, k)
            + " ".join(str(rnd.randint(-100, 100)) for _ in range(n)) + "\n")


def _oracle_30(text: str) -> str:
    from bisect import bisect_left
    d = text.split()
    n = int(d[0]); k = int(d[1])
    a = [int(x) for x in d[2:2 + n]]
    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + a[i]
    pos = {}
    for idx, v in enumerate(pref):
        pos.setdefault(v, []).append(idx)
    ans = 0
    for j, v in enumerate(pref):
        lst = pos.get(v - k)
        if lst:
            ans += bisect_left(lst, j)      # 只数下标在 j 之前的
    return "%d\n" % ans

add(
    title="和为 k 的连续子数组计数",
    section="技巧特训 · C/C++",
    difficulty=4, score=25, tags=["技巧特训", "前缀和", "哈希表", "计数"],
    statement_md=(
        "读入 `n`、`k` 和 `n` 个整数（可为负），统计**和恰好等于 `k`** 的"
        "连续子数组有多少个。\n\n"
        "★ 技巧点：**前缀和 + 哈希表**。设 `pre[j]` 是前 `j` 个数之和，"
        "那么区间 `(i, j]` 的和就是 `pre[j] - pre[i]`。要它等于 `k`，"
        "就等价于 `pre[i] = pre[j] - k`——于是**边扫边记**：\n\n"
        "```\n"
        "mp[0] = 1;                    // 空前缀，别漏\n"
        "for (每个 x) {\n"
        "    pre += x;\n"
        "    ans += mp[pre - k];       // 之前有多少个前缀能凑成 k\n"
        "    mp[pre]++;\n"
        "}\n"
        "```\n\n"
        "`O(n)` 一趟过。两个经典坑：① `mp[0] = 1` 忘了写，从下标 0 开始的区间全丢；"
        "② 元素有负数，滑动窗口会失效，**必须用前缀和哈希**。\n\n"
        "另一套解先攒全部前缀和，再用有序 map + 二分查「下标更小的同值前缀」，"
        "`O(n log n)`，可以对照理解为什么哈希版更快。"
    ),
    input_format="第一行 `n k`；第二行 `n` 个整数。",
    output_format="一行：满足条件的子数组个数。",
    constraints_md="- 1 ≤ n ≤ 10⁵\n- |元素| ≤ 10⁴\n- |k| ≤ 10⁹",
    time_limit_ms=2000,
    inputs=[
        "5 3\n1 2 3 4 5\n",
        "3 0\n0 0 0\n",
        "1 5\n5\n",
        "6 -2\n-1 -1 -1 1 1 1\n",
        "4 100\n1 2 3 4\n",
        _rand_big_case_30(),
    ],
    samples=2,
    oracle=_oracle_30,
    solution=r'''#include <cstdio>
#include <unordered_map>
using namespace std;
int main() {
    int n;
    long long k;
    scanf("%d %lld", &n, &k);
    unordered_map<long long, long long> mp;
    mp.reserve((size_t)n * 2 + 10);
    mp[0] = 1;                       /* ★ 空前缀，漏了就从这错起 */
    long long pre = 0, ans = 0;
    for (int i = 0; i < n; i++) {
        long long x;
        scanf("%lld", &x);
        pre += x;
        auto it = mp.find(pre - k);
        if (it != mp.end()) ans += it->second;
        mp[pre]++;
    }
    printf("%lld\n", ans);
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <map>
#include <vector>
#include <algorithm>
using namespace std;
int main() {
    int n;
    long long k;
    scanf("%d %lld", &n, &k);
    map<long long, vector<int>> pos;         /* 值 → 出现过的下标（升序） */
    vector<long long> pref;
    pref.push_back(0);
    pos[0].push_back(0);
    long long pre = 0;
    for (int i = 1; i <= n; i++) {
        long long x;
        scanf("%lld", &x);
        pre += x;
        pref.push_back(pre);
        pos[pre].push_back(i);
    }
    long long ans = 0;
    for (int j = 0; j <= n; j++) {
        auto it = pos.find(pref[j] - k);
        if (it != pos.end())
            ans += lower_bound(it->second.begin(), it->second.end(), j)
                   - it->second.begin();     /* 只数下标 < j 的 */
    }
    printf("%lld\n", ans);
    return 0;
}
''',
)


# --------------------------------------------------------------------- #
#  有序表的插入维护（upper_bound + insert）　difficulty 1~3
#
#  这组题专门练 `auto it = upper_bound(...); a.insert(it, x);` 这一对：
#  找位置、插进去、保持有序。四道题分别覆盖「一次插入」「批量插入」
#  「lower_bound 与 upper_bound 的稳定性差异」「插完还要按位置查询」。

def _oracle_31(text: str) -> str:
    d = text.split()
    i = 0
    n = int(d[i]); i += 1
    a = [int(d[i + k]) for k in range(n)]
    i += n
    x = int(d[i])
    pos = 0
    while pos < n and a[pos] <= x:         # 第一个严格大于 x 的位置
        pos += 1
    a.insert(pos, x)
    return "%d\n%s\n" % (pos, " ".join(map(str, a)))


add(
    title="有序表插入（upper_bound + insert）",
    section="技巧特训 · C/C++",
    difficulty=1, score=10, tags=["技巧特训", "upper_bound", "insert", "有序表"],
    statement_md=(
        "读入一个**升序**数组和一个整数 `x`，把 `x` 插进去并保持升序。\n\n"
        "输出两行：第一行是插入的**下标**（0 基）；第二行是插入后的数组。\n\n"
        "★ 技巧点，两行就能写完：\n"
        "```cpp\n"
        "auto it = upper_bound(a.begin(), a.end(), x);\n"
        "a.insert(it, x);\n"
        "```\n"
        "三件事必须记住：\n"
        "1. `upper_bound` 返回**第一个严格大于 x** 的位置。`x` 和已有元素相等时，"
        "新元素落在这些相等元素的**后面**（这就是它和 `lower_bound` 的唯一区别）。\n"
        "2. 下标要在 `insert` **之前**算：`int pos = it - a.begin();`。"
        "`insert` 之后 `it` 已经失效，继续用是未定义行为。\n"
        "3. `insert` 的代价是 O(n)（后面的元素整体后移）。插一次很便宜，"
        "在循环里插 10⁵ 次就是 O(n²) —— 那时候要换平衡树或树状数组。"
    ),
    input_format=(
        "第一行 `n`；第二行 `n` 个**升序**整数；第三行一个整数 `x`。\n"
        "- 1 ≤ n ≤ 10⁵，|值| ≤ 10⁹"
    ),
    output_format="两行：插入下标；插入后的数组（空格分隔）。",
    constraints_md="- 1 ≤ n ≤ 10⁵；输入保证数组升序",
    inputs=[
        "5\n1 3 5 7 9\n4\n",
        "5\n1 3 5 7 9\n5\n",
        "3\n2 2 2\n2\n",
        "1\n5\n3\n",
        "1\n-1000000000\n1000000000\n",
    ],
    samples=2,
    oracle=_oracle_31,
    solution=r'''#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;
int main() {
    int n;
    scanf("%d", &n);
    vector<int> a(n);
    for (int k = 0; k < n; k++) scanf("%d", &a[k]);
    int x;
    scanf("%d", &x);
    /* 第一个「严格大于 x」的位置：相等的元素都排在它前面 */
    auto it = upper_bound(a.begin(), a.end(), x);
    int pos = (int)(it - a.begin());     /* ★ 下标必须在 insert 之前算 */
    a.insert(it, x);                     /* O(n) 搬移；此后 it 失效 */
    printf("%d\n", pos);
    for (int k = 0; k < (int)a.size(); k++) printf(k ? " %d" : "%d", a[k]);
    printf("\n");
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
using namespace std;
int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int k = 0; k < n; k++) cin >> a[k];
    int x;
    cin >> x;
    int lo = 0, hi = n;                  /* 手写二分：第一个 > x */
    while (lo < hi) {
        int mid = (lo + hi) / 2;
        if (a[mid] <= x) lo = mid + 1;
        else hi = mid;
    }
    a.insert(a.begin() + lo, x);
    cout << lo << "\n";
    for (size_t k = 0; k < a.size(); k++) cout << (k ? " " : "") << a[k];
    cout << "\n";
    return 0;
}
''',
)


def _oracle_32(text: str) -> str:
    d = text.split()
    i = 0
    n = int(d[i]); i += 1
    a = [int(d[i + k]) for k in range(n)]
    i += n
    m = int(d[i]); i += 1
    for k in range(m):                     # 插完再排，结果与逐个 upper_bound 插入一致
        a.append(int(d[i + k]))
    a.sort()
    return " ".join(map(str, a)) + "\n"


def _rand_case_32() -> str:
    import random
    rnd = random.Random(20261019)
    n, m = 1500, 1500
    base = sorted(rnd.randint(-10 ** 9, 10 ** 9) for _ in range(n))   # ★ 题面要求升序
    lines = ["%d" % n, " ".join(map(str, base))]
    lines.append("%d" % m)
    lines.append(" ".join(str(rnd.randint(-10 ** 9, 10 ** 9)) for _ in range(m)))
    return "\n".join(lines) + "\n"


add(
    title="批量插入保持有序",
    section="技巧特训 · C/C++",
    difficulty=2, score=15, tags=["技巧特训", "upper_bound", "insert", "批量插入"],
    statement_md=(
        "有 `n` 个**升序**元素，再来 `m` 个待插入的整数。**按给出的顺序**逐个插入，"
        "每次都插到 `upper_bound` 找到的位置（相同值的插在已有的相同值之后），"
        "最后输出整个数组。\n\n"
        "★ 套路：\n"
        "```cpp\n"
        "for (int k = 0; k < m; k++) {\n"
        "    a.insert(upper_bound(a.begin(), a.end(), x[k]), x[k]);\n"
        "}\n"
        "```\n"
        "一行完成「找位置 + 插入」。注意这不是排序算法：每插一个都是 O(n) 的搬移，"
        "`m` 次就是 O(m·(n+m))。\n\n"
        "★ 什么时候不该这么写：`n`、`m` 都到 10⁵ 时，上面的写法会 TLE。"
        "要么像参考解那样先插完再**整体排一次**（O((n+m)log(n+m))），"
        "要么用 `multiset` / 树状数组。"
        "本题数据量小，两种写法都能过 —— 重点是看清代价差在哪。"
    ),
    input_format=(
        "第一行 `n`；第二行 `n` 个升序整数；第三行 `m`；第四行 `m` 个整数。\n"
        "- 1 ≤ n, m ≤ 2000，|值| ≤ 10⁹"
    ),
    output_format="一行，插入完成后的数组（空格分隔）。",
    constraints_md="- 1 ≤ n, m ≤ 2000",
    inputs=[
        "3\n1 3 5\n2\n2 0\n",
        "4\n2 2 4 8\n3\n2 2 6\n",
        "1\n0\n4\n-3 -1 1 2\n",
        "5\n-10 -5 0 5 10\n5\n-100 100 -1 1 0\n",
        _rand_case_32(),
    ],
    samples=2,
    oracle=_oracle_32,
    solution=r'''#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;
int main() {
    int n, m;
    scanf("%d", &n);
    vector<int> a(n);
    for (int k = 0; k < n; k++) scanf("%d", &a[k]);
    scanf("%d", &m);
    vector<int> x(m);
    for (int k = 0; k < m; k++) scanf("%d", &x[k]);
    for (int k = 0; k < m; k++)
        a.insert(upper_bound(a.begin(), a.end(), x[k]), x[k]);   /* 找位置 + 插入一行 */
    for (int k = 0; k < (int)a.size(); k++) printf(k ? " %d" : "%d", a[k]);
    printf("\n");
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
int main() {
    int n, m;
    cin >> n;
    vector<int> a(n);
    for (int k = 0; k < n; k++) cin >> a[k];
    cin >> m;
    for (int k = 0; k < m; k++) {         /* 先全部收进来，最后一次排序 */
        int x;
        cin >> x;
        a.push_back(x);
    }
    sort(a.begin(), a.end());
    for (size_t k = 0; k < a.size(); k++) cout << (k ? " " : "") << a[k];
    cout << "\n";
    return 0;
}
''',
)


def _oracle_33(text: str) -> str:
    lines = [ln for ln in text.strip("\n").split("\n") if ln.strip()]
    n = int(lines[0])
    recs = []
    for k in range(1, n + 1):
        v, rid = lines[k].split()
        recs.append((int(v), int(rid)))
    x, newid = map(int, lines[n + 1].split())
    lo = 0
    while lo < n and recs[lo][0] < x:      # 第一个 >= x
        lo += 1
    up = lo
    while up < n and recs[up][0] <= x:     # 第一个 > x
        up += 1
    low_seq = [r[1] for r in recs[:lo]] + [newid] + [r[1] for r in recs[lo:]]
    up_seq = [r[1] for r in recs[:up]] + [newid] + [r[1] for r in recs[up:]]
    return "%d %d\n%s\n%s\n" % (lo, up,
                                " ".join(map(str, low_seq)),
                                " ".join(map(str, up_seq)))


add(
    title="lower 与 upper 插入的稳定性",
    section="技巧特训 · C/C++",
    difficulty=2, score=15, tags=["技巧特训", "lower_bound", "upper_bound", "稳定性"],
    statement_md=(
        "`n` 条记录，每条有 `value` 和 `id`，按 value 升序给出（value 可以重复）。"
        "现在要插入一条新记录 `(x, newid)`。\n\n"
        "分别用两种写法插一次，输出三行：\n"
        "1. 两个插入下标：`lo up`（`lo` 用 `lower_bound`，`up` 用 `upper_bound`）\n"
        "2. 用 `lower_bound` 插入后的 **id 序列**\n"
        "3. 用 `upper_bound` 插入后的 **id 序列**\n\n"
        "★ 这就是两个函数的本质区别：\n"
        "| 函数 | 返回 | 相等元素时新记录落在 |\n"
        "|---|---|---|\n"
        "| `lower_bound` | 第一个 **≥ x** | 已有相同值的**前面** |\n"
        "| `upper_bound` | 第一个 **> x** | 已有相同值的**后面** |\n\n"
        "★ 只有 value 没有 id 时，两种插入得到的数组**长得一模一样**——"
        "差异只在「谁是第一个」。一旦记录带 id、带时间戳、带原始顺序，"
        "选错函数就会把「后到的排在后面」这个稳定性破坏掉。\n"
        "需要稳定插入时用 `upper_bound`。"
    ),
    input_format=(
        "第一行 `n`；随后 `n` 行每行 `value id`（按 value 升序，id 互不相同）；"
        "最后一行 `x newid`。\n"
        "- 1 ≤ n ≤ 10⁵，|value|, |x| ≤ 10⁹，1 ≤ id, newid ≤ 10⁹"
    ),
    output_format="三行：`lo up`；lower 插入后的 id 序列；upper 插入后的 id 序列。",
    constraints_md="- 1 ≤ n ≤ 10⁵",
    inputs=[
        "4\n1 10\n2 20\n2 21\n4 40\n2 99\n",
        "3\n1 1\n3 3\n5 5\n3 9\n",
        "2\n5 1\n7 2\n1 9\n",
        "2\n5 1\n7 2\n9 9\n",
        "3\n4 1\n4 2\n4 3\n4 9\n",
    ],
    samples=2,
    oracle=_oracle_33,
    solution=r'''#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;
struct Rec { int v, id; };
int main() {
    int n;
    scanf("%d", &n);
    vector<Rec> a(n);
    for (int k = 0; k < n; k++) scanf("%d %d", &a[k].v, &a[k].id);
    int x, newid;
    scanf("%d %d", &x, &newid);

    /* lower_bound：第一个 v >= x —— 比较函数写成 (元素, 值) */
    auto itLo = lower_bound(a.begin(), a.end(), x,
                            [](const Rec &r, int val) { return r.v < val; });
    /* upper_bound：第一个 v > x —— 注意参数顺序是 (值, 元素) */
    auto itUp = upper_bound(a.begin(), a.end(), x,
                            [](int val, const Rec &r) { return val < r.v; });
    int lo = (int)(itLo - a.begin());
    int up = (int)(itUp - a.begin());
    printf("%d %d\n", lo, up);

    int pos[2] = {lo, up};
    for (int pass = 0; pass < 2; pass++) {
        vector<Rec> b = a;
        b.insert(b.begin() + pos[pass], Rec{x, newid});
        for (int k = 0; k < (int)b.size(); k++) printf(k ? " %d" : "%d", b[k].id);
        printf("\n");
    }
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
struct Rec { int v, id; };
int main() {
    int n;
    cin >> n;
    vector<Rec> a(n);
    for (int k = 0; k < n; k++) cin >> a[k].v >> a[k].id;
    int x, newid;
    cin >> x >> newid;
    int lo = 0, up = 0;                       /* 手写两套边界，不调 STL */
    while (lo < n && a[lo].v < x) lo++;       /* 第一个 >= x */
    while (up < n && a[up].v <= x) up++;      /* 第一个 > x */
    cout << lo << " " << up << "\n";
    for (int pass = 0; pass < 2; pass++) {
        vector<Rec> b = a;
        b.insert(b.begin() + (pass == 0 ? lo : up), Rec{x, newid});
        for (size_t k = 0; k < b.size(); k++) cout << (k ? " " : "") << b[k].id;
        cout << "\n";
    }
    return 0;
}
''',
)


def _oracle_34(text: str) -> str:
    lines = [ln for ln in text.strip("\n").split("\n") if ln.strip()]
    n, m = map(int, lines[0].split())
    a = sorted(map(int, lines[1].split())) if n else []
    out = []
    for k in range(2, 2 + m):
        op, x = map(int, lines[k].split())
        if op == 1:
            lo, hi = 0, len(a)
            while lo < hi:                     # 第一个 > x，插在相等元素之后
                mid = (lo + hi) // 2
                if a[mid] <= x:
                    lo = mid + 1
                else:
                    hi = mid
            a.insert(lo, x)
        else:
            lo, hi = 0, len(a)
            while lo < hi:                     # 第一个 >= x
                mid = (lo + hi) // 2
                if a[mid] < x:
                    lo = mid + 1
                else:
                    hi = mid
            out.append(str(lo + 1) if lo < len(a) and a[lo] == x else "-1")
    return "\n".join(out) + ("\n" if out else "")


def _rand_case_34() -> str:
    import random
    rnd = random.Random(20261020)
    n, m = 1200, 1600
    base = sorted(rnd.randint(-10 ** 6, 10 ** 6) for _ in range(n))
    lines = ["%d %d" % (n, m), " ".join(map(str, base))]
    for _ in range(m):
        if rnd.random() < 0.5:
            lines.append("1 %d" % rnd.randint(-10 ** 6, 10 ** 6))
        else:
            lines.append("2 %d" % rnd.choice(base) if rnd.random() < 0.7
                         else "2 %d" % rnd.randint(-2 * 10 ** 6, 2 * 10 ** 6))
    return "\n".join(lines) + "\n"


add(
    title="动态有序表的名次查询",
    section="技巧特训 · C/C++",
    difficulty=3, score=20, tags=["技巧特训", "upper_bound", "lower_bound", "insert", "名次"],
    statement_md=(
        "维护一个始终**升序**的集合，支持两种操作（共 `m` 次）：\n\n"
        "- `1 x`：把 `x` 插入集合（相同的值允许重复，新值插在已有的相同值之后）\n"
        "- `2 x`：查询 `x` 的**名次**（1 基，即**第一个** `x` 的位置）；`x` 不存在输出 `-1`\n\n"
        "对每个 `2` 操作输出一行。\n\n"
        "★ 两个函数各管一件事，正好对上两种操作：\n"
        "```cpp\n"
        "if (op == 1) a.insert(upper_bound(a.begin(), a.end(), x), x);   // 插：第一个 > x\n"
        "else {\n"
        "    auto it = lower_bound(a.begin(), a.end(), x);               // 查：第一个 >= x\n"
        "    if (it == a.end() || *it != x) puts(\"-1\");\n"
        "    else printf(\"%d\\n\", int(it - a.begin()) + 1);\n"
        "}\n"
        "```\n"
        "**插入用 upper、查询用 lower** —— 记住这条就不会把重复元素的名次算错。"
        "用 `upper_bound` 查询的话，重复元素会返回最后一个之后的位置，名次偏大，"
        "而且分不清「存在」还是「不存在」。\n\n"
        "★ 复杂度：`vector::insert` 是 O(n)，本套做法整体 O(m·n)。"
        "数据量再大就得换成 `multiset` + 树状数组，或者干脆离线离散化后用 Fenwick 求排名。"
    ),
    input_format=(
        "第一行 `n m`；第二行 `n` 个**升序**整数（初始集合）；"
        "随后 `m` 行，每行 `op x`（`op` = 1 插入 / 2 查询）。\n"
        "- 1 ≤ n ≤ 2000，1 ≤ m ≤ 2000，|值| ≤ 10⁹"
    ),
    output_format="每个 `2` 操作输出一行：名次（1 基），不存在输出 `-1`。",
    constraints_md="- 1 ≤ n, m ≤ 2000",
    inputs=[
        "5 5\n1 2 4 8 9\n1 5\n2 5\n1 2\n2 2\n2 100\n",
        "3 4\n1 1 1\n2 1\n1 1\n2 1\n2 2\n",
        "1 3\n7\n2 7\n1 7\n2 7\n",
        "2 4\n-5 5\n2 -5\n1 0\n2 0\n2 -100\n",
        _rand_case_34(),
    ],
    samples=2,
    oracle=_oracle_34,
    solution=r'''#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;
int main() {
    int n, m;
    scanf("%d %d", &n, &m);
    vector<int> a(n);
    for (int k = 0; k < n; k++) scanf("%d", &a[k]);
    while (m--) {
        int op, x;
        scanf("%d %d", &op, &x);
        if (op == 1) {
            a.insert(upper_bound(a.begin(), a.end(), x), x);   /* 插在相等元素之后 */
        } else {
            auto it = lower_bound(a.begin(), a.end(), x);      /* 第一个 >= x */
            if (it == a.end() || *it != x) printf("-1\n");
            else printf("%d\n", (int)(it - a.begin()) + 1);    /* 下标 + 1 = 名次 */
        }
    }
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <set>
using namespace std;
int main() {
    int n, m;
    scanf("%d %d", &n, &m);
    multiset<int> s;
    for (int k = 0; k < n; k++) {
        int v;
        scanf("%d", &v);
        s.insert(v);
    }
    while (m--) {
        int op, x;
        scanf("%d %d", &op, &x);
        if (op == 1) {
            s.insert(x);
        } else {
            auto it = s.lower_bound(x);
            if (it == s.end() || *it != x) printf("-1\n");
            else printf("%d\n", (int)distance(s.begin(), it) + 1);   /* distance 是 O(n) */
        }
    }
    return 0;
}
''',
)


# --------------------------------------------------------------------- #

HEADER = '''"""C/C++ 技巧特训题库 —— **自动生成，不要手改**。

本文件由 `tools/gen_ds_tricks.py` 产出，重新生成：

    python tools/gen_ds_tricks.py

规矩与 gen_ds_bank 一致：
1. 期望输出由生成脚本里的独立 Python `oracle` 预先算好（用"笨办法"实现，
   与参考解不同路），拿参考解现跑现填等于自己给自己判卷。
2. 每题两套 C++ 实现（reference_solution / alt_solution），verify_bank 双撞。
3. line = "cpp"，同一道题 C 和 C++ 都能交（判题按提交语言选编译器）。

分节「技巧特训 · C/C++」：数据结构讲义没专门讲、但做题常用的 STL 与
算法套路，难度 1 → 4 递进，对标蓝桥杯 / 码蹄杯 / ACM 强度。
"""

DS_TRICKS_PROBLEMS: list[dict] = '''


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
            "subject": "ds",
            "line": "cpp",
            "difficulty": int(p.get("difficulty", 2)),
            "total_score": int(p.get("score", 10)),
            "tags": list(p.get("tags", [])),
            "statement_md": p["statement_md"],
            "input_format": p.get("input_format", ""),
            "output_format": p.get("output_format", ""),
            "constraints_md": p.get("constraints_md", ""),
            "time_limit_ms": int(p.get("time_limit_ms", 1000)),
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
    return HEADER + body + "\n"


def _sanity(probs: list[dict]) -> list[str]:
    problems: list[str] = []
    seen: set[str] = set()
    for i, p in enumerate(probs, 1):
        t = p["title"]
        if t in seen:
            problems.append("[%d] 标题重复：%s" % (i, t))
        seen.add(t)
        for k in ("statement_md", "input_format", "output_format",
                  "reference_solution", "alt_solution", "source_section"):
            if not str(p.get(k) or "").strip():
                problems.append("[%d] %s 缺字段 %s" % (i, t, k))
        if not p["cases"]:
            problems.append("[%d] %s 没有测试用例" % (i, t))
        if p["total_score"] <= 0:
            problems.append("[%d] %s 满分非法" % (i, t))
        for j, c in enumerate(p["cases"], 1):
            if not c["expected_stdout"]:
                problems.append("[%d] %s 第 %d 个用例期望输出为空" % (i, t, j))
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description="生成 C/C++ 技巧特训题库")
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

    empties = [p["title"] for p in probs
               if any(c["expected_stdout"].strip() == "" and c["expected_stdout"] != "\n"
                      for c in p["cases"])]
    if empties:
        print("★ 期望输出为空的题：%s" % "、".join(empties))
        return 1

    if args.check:
        return 0

    OUT_PATH.write_text(_dump(probs), encoding="utf-8", newline="\n")
    print("已写入 %s（%d 字节）" % (OUT_PATH, OUT_PATH.stat().st_size))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
