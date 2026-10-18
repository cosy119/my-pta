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
