# -*- coding: utf-8 -*-
"""链表专题 · PTA 经典 —— 「链表专题 · PTA 经典」分节生成器。

来源：cosy 提供的 6 道浙大 DS 课程组原题（7-1 / 7-2 / 7-3 / 7-4 / 7-6 / 7-7），
按**原题的输入输出约定**收进题库 —— 注意这些约定和「第 02 讲 · 线性表」里
那批教材式简化题（输入 n + 数组）**不一样**：

* `-1` 作序列结束标志（不是先给长度）；
* 「地址-数据-地址」式的静态链表输入（地址是 5 位整数，NULL 用 -1）；
* 空结果要输出 `NULL` 而不是空行。

所以这里单独成节，不跟讲次那批混。

规矩与其它题库一致：
1. `expected_stdout` 由本文件的独立 Python `oracle` 算好（用最直白的写法），
   参考解只是被验证的一方。
2. 每题两套 C++ 实现，verify_bank 双撞。
3. 大用例固定种子生成，可复现。

结构化数据处理一律走「地址 → (数据, next)」的字典/数组，**不按输入行序**——
原题故意把行序打乱，还可能混进不在这条链上的孤立结点。
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "app" / "problems_bank_ds_list.py"

PROBLEMS: list[dict] = []
SECTION = "链表专题 · PTA 经典"


def add(**kw) -> None:
    PROBLEMS.append(kw)


# --------------------------------------------------------------------- #
#  公共：把「地址 数据 next」三行一组读成两张表
# --------------------------------------------------------------------- #

def _read_static_list(text: str):
    """返回 (head, dat, nxt)：dat/nxt 是 {地址: 值} 字典。"""
    d = text.split()
    i = 0
    head = int(d[i]); i += 1
    n = int(d[i]); i += 1
    dat, nxt = {}, {}
    for _ in range(n):
        a = int(d[i]); v = int(d[i + 1]); b = int(d[i + 2]); i += 3
        dat[a] = v
        nxt[a] = b
    return head, dat, nxt


def _walk(head: int, nxt: dict) -> list[int]:
    """顺着 next 走到 -1，返回地址序列（孤立结点自然被跳过）。"""
    out = []
    cur = head
    while cur != -1:
        out.append(cur)
        cur = nxt.get(cur, -1)
    return out


def _fmt_addr(a: int) -> str:
    return "%05d" % a


def _emit_static(order: list[int], dat: dict) -> list[str]:
    """把地址序列按「地址 数据 下一地址」输出，最后一行的 next 打 -1。"""
    lines = []
    for k, a in enumerate(order):
        nb = order[k + 1] if k + 1 < len(order) else -1
        tail = "-1" if nb == -1 else _fmt_addr(nb)
        lines.append("%s %d %s" % (_fmt_addr(a), dat[a], tail))
    return lines


# --------------------------------------------------------------------- #
#  L1  两个有序链表序列的合并（PTA 7-1）
# --------------------------------------------------------------------- #

def _rand_seq_merge(seed: int, n1: int, n2: int) -> str:
    import random
    rnd = random.Random(seed)
    a = sorted(rnd.randint(1, 1000000) for _ in range(n1))
    b = sorted(rnd.randint(1, 1000000) for _ in range(n2))
    return " ".join(map(str, a)) + " -1\n" + " ".join(map(str, b)) + " -1\n"


def _oracle_l1(text: str) -> str:
    d = text.split()
    a, b = [], []
    i = 0
    while i < len(d) and d[i] != "-1":
        a.append(int(d[i])); i += 1
    i += 1                                     # 跳过分隔的 -1
    while i < len(d) and d[i] != "-1":
        b.append(int(d[i])); i += 1
    out = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    return (" ".join(map(str, out)) if out else "NULL") + "\n"


add(
    title="两个有序链表序列的合并（PTA 原题 · NULL 约定）",
    section=SECTION,
    difficulty=2, score=20, tags=["链表", "归并", "PTA 原题", "哨兵结点"],
    statement_md=(
        "已知两个**非降序**链表序列 `S1` 与 `S2`，构造出 `S1` 与 `S2` 合并后的"
        "新的非降序链表 `S3`。\n\n"
        "（原题：PTA 7-1，浙江大学 DS 课程组，20 分）\n\n"
        "★ 三个和教材简化题不一样的地方，也是这题真正考的东西：\n"
        "1. **不给长度**，用 `-1` 作结束标志 —— `while (cin >> v && v != -1)`。"
        "`-1` 不属于序列，读到就停。\n"
        "2. **两条都空要输出 `NULL`**，不是空行。合并后 `dummy.next == nullptr` "
        "就是全空的唯一信号。\n"
        "3. 归并只需要**改指针**：谁小就把谁的结点接到结果尾部，"
        "剩下的那条整段挂上去，**一个结点都不用新建**。\n\n"
        "```cpp\n"
        "Lnode dummy; Lnode *tail = &dummy;   // 哑结点，省掉「第一个结点」的特判\n"
        "while (a && b) {\n"
        "    if (a->v <= b->v) { tail->next = a; a = a->next; }\n"
        "    else              { tail->next = b; b = b->next; }\n"
        "    tail = tail->next;\n"
        "}\n"
        "tail->next = a ? a : b;              // 剩下的整段挂上去\n"
        "```"
    ),
    input_format=(
        "输入分两行，每行给出由若干个**正整数**构成的非降序序列，"
        "用 `-1` 表示序列的结尾（`-1` 不属于这个序列）。数字用空格间隔。"
    ),
    output_format=(
        "在一行中输出合并后新的非降序链表，数字间用空格分开，"
        "**结尾不能有多余空格**；若新链表为空，输出 `NULL`。"
    ),
    constraints_md="- 每个序列长度 0 ≤ len ≤ 10⁵；元素为正整数",
    inputs=[
        "1 3 5 -1\n2 4 6 8 10 -1\n",
        "-1\n-1\n",
        "-1\n1 2 -1\n",
        "1 1 3 -1\n1 2 -1\n",
        _rand_seq_merge(7101, 5000, 5000),
    ],
    samples=2,
    oracle=_oracle_l1,
    solution=r'''#include <cstdio>
struct Lnode { int v; Lnode *next; };

Lnode *build() {                       /* 尾插建表，-1 结束；空表返回 NULL */
    Lnode *head = nullptr, *tail = nullptr;
    int v;
    while (scanf("%d", &v) == 1 && v != -1) {
        Lnode *p = new Lnode;
        p->v = v; p->next = nullptr;
        if (tail) tail->next = p; else head = p;
        tail = p;
    }
    return head;
}

int main() {
    Lnode *a = build(), *b = build();
    Lnode dummy; dummy.next = nullptr;  /* 哑结点收结果，免去首结点特判 */
    Lnode *tail = &dummy;
    while (a && b) {
        if (a->v <= b->v) { tail->next = a; a = a->next; }
        else              { tail->next = b; b = b->next; }
        tail = tail->next;              /* ★ 只改指针，不新建结点 */
    }
    tail->next = a ? a : b;             /* 剩下那条整段挂上去 */
    if (!dummy.next) {                  /* 两条都空 */
        printf("NULL\n");
        return 0;
    }
    int first = 1;
    for (Lnode *p = dummy.next; p; p = p->next) {
        printf(first ? "%d" : " %d", p->v);
        first = 0;
    }
    printf("\n");
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> a, b;
    int v;
    while (cin >> v && v != -1) a.push_back(v);
    while (cin >> v && v != -1) b.push_back(v);
    vector<int> out;
    size_t i = 0, j = 0;                /* 换成双数组归并，结果等价 */
    while (i < a.size() && j < b.size())
        out.push_back(a[i] <= b[j] ? a[i++] : b[j++]);
    while (i < a.size()) out.push_back(a[i++]);
    while (j < b.size()) out.push_back(b[j++]);
    if (out.empty()) { cout << "NULL\n"; return 0; }
    for (size_t k = 0; k < out.size(); k++) cout << (k ? " " : "") << out[k];
    cout << "\n";
    return 0;
}
''',
)


# --------------------------------------------------------------------- #
#  L2  两个有序链表序列的交集（PTA 7-2）
# --------------------------------------------------------------------- #

def _rand_seq_inter(seed: int, n1: int, n2: int) -> str:
    import random
    rnd = random.Random(seed)
    a = sorted(rnd.randint(1, 50000) for _ in range(n1))
    b = sorted(rnd.randint(1, 50000) for _ in range(n2))
    return " ".join(map(str, a)) + " -1\n" + " ".join(map(str, b)) + " -1\n"


def _oracle_l2(text: str) -> str:
    d = text.split()
    a, b = [], []
    i = 0
    while i < len(d) and d[i] != "-1":
        a.append(int(d[i])); i += 1
    i += 1
    while i < len(d) and d[i] != "-1":
        b.append(int(d[i])); i += 1
    out = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            i += 1
        elif a[i] > b[j]:
            j += 1
        else:
            out.append(a[i]); i += 1; j += 1
    return (" ".join(map(str, out)) if out else "NULL") + "\n"


add(
    title="两个有序链表序列的交集（PTA 原题）",
    section=SECTION,
    difficulty=2, score=20, tags=["链表", "双指针", "PTA 原题"],
    statement_md=(
        "已知两个**非降序**链表序列 `S1` 与 `S2`，构造出 `S1` 与 `S2` 的"
        "**交集**新链表 `S3`。\n\n"
        "（原题：PTA 7-2，浙江大学 DS 课程组，20 分）\n\n"
        "★ 和合并题共用「双指针 + `-1` 结尾」，但归并是**小的先走**，"
        "交集是**小的先跳过**：\n"
        "```cpp\n"
        "while (p1 && p2) {\n"
        "    if      (p1->data < p2->data) p1 = p1->next;   // 小的不可能在交集里\n"
        "    else if (p1->data > p2->data) p2 = p2->next;\n"
        "    else { /* 相等：收进结果，两边同时前进 */ }\n"
        "}\n"
        "```\n"
        "两个坑：\n"
        "1. 交集**必须新建结点**（两边都要前进，原结点还得留着往后比），"
        "这一点和合并题刚好相反。\n"
        "2. 重复元素按**多重集**处理：`1 2 2 3` ∩ `2 2 4` = `2 2`。"
        "相等时两边同时前进，自然就得到各取 `min(次数)`。\n"
        "3. 交集为空输出 `NULL`。"
    ),
    input_format=(
        "输入分两行，每行给出由若干个**正整数**构成的非降序序列，"
        "用 `-1` 表示序列的结尾（`-1` 不属于这个序列）。数字用空格间隔。"
    ),
    output_format=(
        "在一行中输出两个输入序列的交集序列，数字间用空格分开，"
        "**结尾不能有多余空格**；若新链表为空，输出 `NULL`。"
    ),
    constraints_md="- 每个序列长度 0 ≤ len ≤ 10⁵；元素为正整数",
    inputs=[
        "1 2 5 -1\n2 4 5 8 10 -1\n",
        "1 2 -1\n3 4 -1\n",
        "1 2 2 3 -1\n2 2 4 -1\n",
        "-1\n-1\n",
        _rand_seq_inter(7102, 3000, 3000),
    ],
    samples=2,
    oracle=_oracle_l2,
    solution=r'''#include <cstdio>
struct Lnode { int v; Lnode *next; };

Lnode *build() {
    Lnode *head = nullptr, *tail = nullptr;
    int v;
    while (scanf("%d", &v) == 1 && v != -1) {
        Lnode *p = new Lnode;
        p->v = v; p->next = nullptr;
        if (tail) tail->next = p; else head = p;
        tail = p;
    }
    return head;
}

int main() {
    Lnode *p1 = build(), *p2 = build();
    Lnode dummy; dummy.next = nullptr;
    Lnode *tail = &dummy;
    while (p1 && p2) {
        if (p1->v < p2->v) {
            p1 = p1->next;               /* 小的不可能出现在交集里 */
        } else if (p1->v > p2->v) {
            p2 = p2->next;
        } else {
            Lnode *p = new Lnode;        /* ★ 交集必须新建结点 */
            p->v = p1->v; p->next = nullptr;
            tail->next = p; tail = p;
            p1 = p1->next; p2 = p2->next;
        }
    }
    if (!dummy.next) { printf("NULL\n"); return 0; }
    int first = 1;
    for (Lnode *p = dummy.next; p; p = p->next) {
        printf(first ? "%d" : " %d", p->v);
        first = 0;
    }
    printf("\n");
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> a, b;
    int v;
    while (cin >> v && v != -1) a.push_back(v);
    while (cin >> v && v != -1) b.push_back(v);
    vector<int> out;
    size_t i = 0, j = 0;
    while (i < a.size() && j < b.size()) {
        if (a[i] < b[j]) i++;
        else if (a[i] > b[j]) j++;
        else { out.push_back(a[i]); i++; j++; }
    }
    if (out.empty()) { cout << "NULL\n"; return 0; }
    for (size_t k = 0; k < out.size(); k++) cout << (k ? " " : "") << out[k];
    cout << "\n";
    return 0;
}
''',
)


# --------------------------------------------------------------------- #
#  L3  重排链表（PTA 7-3）
# --------------------------------------------------------------------- #

def _rand_case_l3() -> str:
    import random
    rnd = random.Random(7103)
    m = 2000                                   # 链上结点数
    pool = rnd.sample(range(0, 100000), m + 20)
    chain, extra = pool[:m], pool[m:]           # 后 20 个是孤立结点
    body = []
    for k, a in enumerate(chain):
        nb = chain[k + 1] if k + 1 < m else -1
        body.append("%s %d %s" % (_fmt_addr(a), rnd.randint(1, 100000),
                                  "-1" if nb == -1 else _fmt_addr(nb)))
    for a in extra:                             # 孤立结点：next 指向链上，但没人指向它
        body.append("%s %d %s" % (_fmt_addr(a), rnd.randint(1, 100000),
                                  _fmt_addr(chain[rnd.randrange(m)])))
    rnd.shuffle(body)                           # ★ 输入行序是乱的
    return "%s %d\n" % (_fmt_addr(chain[0]), m + len(extra)) + "\n".join(body) + "\n"


def _oracle_l3(text: str) -> str:
    head, dat, nxt = _read_static_list(text)
    ordr = _walk(head, nxt)
    res = []
    l, r = 0, len(ordr) - 1
    while l <= r:                               # Ln, L1, Ln-1, L2 ...
        res.append(ordr[r]); r -= 1
        if l <= r:
            res.append(ordr[l]); l += 1
    return "\n".join(_emit_static(res, dat)) + "\n"


add(
    title="重排链表（PTA 原题 · 地址链表）",
    section=SECTION,
    difficulty=3, score=20, tags=["链表", "静态链表", "双指针", "PTA 原题"],
    statement_md=(
        "给定一个单链表 `L1 → L2 → … → Ln-1 → Ln`，请编写程序将链表重新排列为\n"
        "`Ln → L1 → Ln-1 → L2 → …`。\n\n"
        "例如：给定 `L` 为 `1 → 2 → 3 → 4 → 5 → 6`，则输出应该为 "
        "`6 → 1 → 5 → 2 → 4 → 3`。\n\n"
        "（原题：PTA 7-3，陈越，浙江大学，20 分）\n\n"
        "★ 这题是**静态链表**：结点不是 `new` 出来的，而是用「地址」当下标。\n"
        "```cpp\n"
        "int dat[100005], nxt[100005];\n"
        "int cur = head;\n"
        "while (cur != -1) { ord.push_back(cur); cur = nxt[cur]; }   // ① 按地址走成数组\n"
        "int l = 0, r = ord.size() - 1;\n"
        "while (l <= r) { res.push_back(ord[r--]); if (l <= r) res.push_back(ord[l++]); }  // ② 两头取\n"
        "```\n"
        "四个坑：\n"
        "1. **不能按输入行序**。题目给的 N 行是乱序的，必须从首地址顺着 `next` 走"
        "（样例里第一行就是 `00000 4 99999`，它可不是第一个结点）。\n"
        "2. **N 可能大于链长**：会有孤立结点挂在输入里，走到 `-1` 就停，别用 `N` 当循环次数。\n"
        "3. 输出的第三列是**重排后**的下一结点地址，不是原来的 `next`。\n"
        "4. 地址要 `%05d` 补零；最后一个结点的 next 打 `-1`。"
    ),
    input_format=(
        "第 1 行给出第 1 个结点的地址和结点总个数，即正整数 `N`（≤ 10⁵）。"
        "结点的地址是 5 位非负整数，NULL 地址用 `-1` 表示。\n"
        "接下来有 `N` 行，每行格式为：`Address Data Next`。"
        "`Data` 为不超过 10⁵ 的正整数。题目保证给出的链表上至少有两个结点。"
    ),
    output_format="按重排后的顺序，每个结点占一行，格式与输入相同。",
    constraints_md="- 2 ≤ 结点数 ≤ 10⁵；地址 0 ≤ addr ≤ 99999",
    inputs=[
        "00100 6\n00000 4 99999\n00100 1 12309\n68237 6 -1\n"
        "33218 3 00000\n99999 5 68237\n12309 2 33218\n",
        "00001 2\n00002 2 -1\n00001 1 00002\n",
        "0 5\n3 30 -1\n0 10 1\n1 20 2\n2 40 3\n4 50 0\n",
        "00007 4\n00008 8 -1\n00007 7 00003\n00009 99 00007\n00003 3 00008\n",
        _rand_case_l3(),
    ],
    samples=2,
    oracle=_oracle_l3,
    solution=r'''#include <cstdio>
#include <vector>
using namespace std;
int dat[100005], nxt[100005];

int main() {
    int head, n;
    if (scanf("%d %d", &head, &n) != 2) return 0;
    for (int k = 0; k < n; k++) {
        int a, v, b;
        scanf("%d %d %d", &a, &v, &b);
        dat[a] = v; nxt[a] = b;             /* 用地址当下标，跟输入行序无关 */
    }
    vector<int> ord;
    for (int cur = head; cur != -1; cur = nxt[cur])
        ord.push_back(cur);                 /* ★ 走到 -1 为止，孤立结点自然被跳过 */
    vector<int> res;
    int l = 0, r = (int)ord.size() - 1;
    while (l <= r) {                        /* 两头交替取：尾、头、次尾、次头… */
        res.push_back(ord[r]); r--;
        if (l <= r) { res.push_back(ord[l]); l++; }
    }
    for (size_t k = 0; k < res.size(); k++) {
        int nb = (k + 1 < res.size()) ? res[k + 1] : -1;
        if (nb == -1) printf("%05d %d -1\n", res[k], dat[res[k]]);
        else          printf("%05d %d %05d\n", res[k], dat[res[k]], nb);
    }
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;
int dat[100005], nxt[100005];

int main() {
    int head, n;
    if (scanf("%d %d", &head, &n) != 2) return 0;
    for (int k = 0; k < n; k++) {
        int a, v, b;
        scanf("%d %d %d", &a, &v, &b);
        dat[a] = v; nxt[a] = b;
    }
    vector<int> ord;
    for (int cur = head; cur != -1; cur = nxt[cur]) ord.push_back(cur);
    /* 换个切法：前半段原样、后半段整体逆置，然后两段交替取值 */
    int m = (int)ord.size();
    int mid = (m + 1) / 2;
    vector<int> a(ord.begin(), ord.begin() + mid);
    vector<int> b(ord.begin() + mid, ord.end());
    reverse(b.begin(), b.end());
    vector<int> res;
    for (size_t k = 0; k < b.size(); k++) {
        res.push_back(b[k]);
        if (k < a.size()) res.push_back(a[k]);
    }
    if (b.size() < a.size()) res.push_back(a.back());
    for (size_t k = 0; k < res.size(); k++) {
        int nb = (k + 1 < res.size()) ? res[k + 1] : -1;
        if (nb == -1) printf("%05d %d -1\n", res[k], dat[res[k]]);
        else          printf("%05d %d %05d\n", res[k], dat[res[k]], nb);
    }
    return 0;
}
''',
)


# --------------------------------------------------------------------- #
#  L4  约瑟夫环（PTA 7-4）
# --------------------------------------------------------------------- #

def _oracle_l4(text: str) -> str:
    d = text.split()
    n, p = int(d[0]), int(d[1])
    people = list(range(1, n + 1))
    idx = 0
    out = []
    while people:
        idx = (idx + p - 1) % len(people)
        out.append(people.pop(idx))
    return " ".join(map(str, out)) + "\n"


add(
    title="约瑟夫环（链表模拟 · PTA 原题）",
    section=SECTION,
    difficulty=2, score=20, tags=["链表", "循环链表", "模拟", "PTA 原题"],
    statement_md=(
        "`N` 个人围成一圈顺序编号，从 1 号开始按 1、2、3…… 顺序报数，"
        "报 `p` 者退出圈外，其余的人再从 1、2、3 开始报数，报 `p` 的人再退出圈外，"
        "以此类推。请按退出顺序输出每个退出人的原序号。\n\n"
        "（原题：PTA 7-4，李廷元，中国民用航空飞行学院，20 分）\n\n"
        "★ 标准做法是**循环双向链表**：删除一个人就是让他的前驱和后继直接握手。\n"
        "```cpp\n"
        "for (int i = 0; i < p - 1; i++) cur = cur->next;   // 从 1 数到 p，走 p-1 步\n"
        "cout << cur->data;\n"
        "cur->prev->next = cur->next;   // ★ 前驱跨过后继\n"
        "cur->next->prev = cur->prev;\n"
        "cur = cur->next;               // 从下一个人重新报 1\n"
        "```\n"
        "三个细节：\n"
        "1. 走的是 **`p-1` 步**，不是 `p` 步 —— 因为「自己」就是报 1 的那个人。\n"
        "2. 删完必须 `cur = cur->next`：下一个报 1 的人就是被删者的后继。\n"
        "3. `N = 1` 时头结点的 `next`、`prev` 都指向自己，删完直接结束，不用特判。\n\n"
        "为什么这题给 `N ≤ 3000` 而隔壁「约瑟夫环」给 `m ≤ 10⁹`：那个必须用"
        "递推公式，这个可以老老实实模拟。"
    ),
    input_format="只有一行，包括一个整数 `N`（1 ≤ N ≤ 3000）及一个整数 `p`（1 ≤ p ≤ 5000）。",
    output_format="按退出顺序输出每个退出人的原序号，数据间以一个空格分隔，但**行尾无空格**。",
    constraints_md="- 1 ≤ N ≤ 3000；1 ≤ p ≤ 5000",
    inputs=[
        "7 3\n",
        "1 5\n",
        "5 1\n",
        "2 2\n",
        "3000 4999\n",
    ],
    samples=2,
    oracle=_oracle_l4,
    solution=r'''#include <cstdio>
struct node { int data; node *next, *prev; };

int main() {
    int n, p;
    if (scanf("%d %d", &n, &p) != 2) return 0;
    node *head = new node{1, nullptr, nullptr};   /* 带头结点，data 存编号 */
    node *tail = head;
    for (int i = 2; i <= n; i++) {
        node *q = new node{i, nullptr, tail};
        tail->next = q;
        tail = q;
    }
    tail->next = head;                            /* 收成一圈 */
    head->prev = tail;
    node *cur = head;
    int left = n;
    while (left > 0) {
        for (int i = 0; i < p - 1; i++) cur = cur->next;   /* ★ 走 p-1 步 */
        printf(left == n ? "%d" : " %d", cur->data);
        node *t = cur;
        cur->prev->next = cur->next;              /* 前驱直接跨过去 */
        cur->next->prev = cur->prev;
        cur = cur->next;                          /* 下一个报 1 的人 */
        delete t;
        left--;
    }
    printf("\n");
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <vector>
using namespace std;

int main() {
    int n, p;
    if (scanf("%d %d", &n, &p) != 2) return 0;
    /* 不用链表：数组打「活着」标记，一轮轮数，规模 3000×5000 也够快 */
    vector<char> alive(n, 1);
    int pos = 0;
    for (int k = 0; k < n; k++) {
        int step = 0;
        while (true) {
            if (alive[pos] && ++step == p) break;
            pos = (pos + 1) % n;
        }
        alive[pos] = 0;
        printf(k ? " %d" : "%d", pos + 1);
        pos = (pos + 1) % n;
    }
    printf("\n");
    return 0;
}
''',
)


# --------------------------------------------------------------------- #
#  L5  链表去重（PTA 7-6）
# --------------------------------------------------------------------- #

def _rand_case_l5() -> str:
    import random
    rnd = random.Random(7106)
    m = 2000
    pool = rnd.sample(range(0, 100000), m + 15)
    chain, extra = pool[:m], pool[m:]
    keys = [rnd.choice([-1, 1]) * rnd.randint(1, 5000) for _ in range(m)]
    body = []
    for k, a in enumerate(chain):
        nb = chain[k + 1] if k + 1 < m else -1
        body.append("%s %d %s" % (_fmt_addr(a), keys[k],
                                  "-1" if nb == -1 else _fmt_addr(nb)))
    for a in extra:
        body.append("%s %d %s" % (_fmt_addr(a), rnd.randint(-5000, 5000),
                                  _fmt_addr(chain[rnd.randrange(m)])))
    rnd.shuffle(body)
    return "%s %d\n" % (_fmt_addr(chain[0]), m + len(extra)) + "\n".join(body) + "\n"


def _oracle_l5(text: str) -> str:
    head, dat, nxt = _read_static_list(text)
    kept, removed = [], []
    seen = set()
    for a in _walk(head, nxt):
        v = dat[a]
        k = -v if v < 0 else v
        if k in seen:
            removed.append(a)
        else:
            seen.add(k)
            kept.append(a)
    lines = _emit_static(kept, dat)
    if removed:
        lines += _emit_static(removed, dat)
    return "\n".join(lines) + "\n"


add(
    title="链表去重（PTA 原题 · 分离被删结点）",
    section=SECTION,
    difficulty=3, score=20, tags=["链表", "静态链表", "去重", "PTA 原题"],
    statement_md=(
        "给定一个带整数键值的链表 `L`，把其中**绝对值重复**的键值结点删掉。"
        "即对每个键值 `K`，只有第一个绝对值等于 `K` 的结点被保留。"
        "同时，所有被删除的结点须被保存在另一个链表上。\n\n"
        "例如给定 `L` 为 `21 → -15 → -15 → -7 → 15`，"
        "输出删除后的链表 `21 → -15 → -7`，以及被删除的链表 `-15 → 15`。\n\n"
        "（原题：PTA 7-6，陈越，浙江大学，20 分）\n\n"
        "★ 判重看的是**绝对值**，`-15` 和 `15` 算同一个键值 —— "
        "这是这题最容易被忽略的一句。\n"
        "```cpp\n"
        "int k = dat[cur] < 0 ? -dat[cur] : dat[cur];\n"
        "if (!seen[k]) { seen[k] = 1; kept.push_back(cur); }\n"
        "else removed.push_back(cur);\n"
        "```\n"
        "三个坑：\n"
        "1. 判重用 `seen[|键值|]` 数组（键值绝对值 ≤ 10⁴），不用每次回头扫链表。\n"
        "2. 输出时第三列是**同一个链表内部**的相邻结点地址，不是原来的 `next`；"
        "两个链表各自以自己的 `-1` 结尾。\n"
        "3. 没有结点被删时，第二段**整个不输出**（不是输出空行）。\n"
        "4. 同样是乱序输入，必须从首地址顺着走，`N` 可能大于链长。"
    ),
    input_format=(
        "第一行给出 `L` 的第一个结点的地址和一个正整数 `N`（≤ 10⁵，为结点总数）。"
        "一个结点的地址是非负的 5 位整数，空地址 NULL 用 `-1` 表示。\n"
        "随后 `N` 行，每行格式为：`地址 键值 下一个结点`。键值是绝对值不超过 10⁴ 的整数。"
    ),
    output_format=(
        "首先输出去重后的链表，然后输出被删除的链表。每个结点占一行，按输入的格式输出。"
        "没有结点被删除时只输出第一段。"
    ),
    constraints_md="- 1 ≤ 结点数 ≤ 10⁵；|键值| ≤ 10⁴；地址 0 ≤ addr ≤ 99999",
    inputs=[
        "00100 5\n99999 -7 87654\n23854 -15 00000\n87654 15 -1\n"
        "00000 -15 99999\n00100 21 23854\n",
        "00001 3\n00001 5 00002\n00002 -5 00003\n00003 7 -1\n",
        "00010 1\n00010 0 -1\n",
        "00020 4\n00020 1 00021\n00021 -1 00022\n00022 1 00023\n00023 -1 -1\n",
        _rand_case_l5(),
    ],
    samples=2,
    oracle=_oracle_l5,
    solution=r'''#include <cstdio>
#include <vector>
using namespace std;
int dat[100005], nxt[100005];

void print_group(const vector<int> &g) {
    for (size_t i = 0; i < g.size(); i++) {
        int nb = (i + 1 < g.size()) ? g[i + 1] : -1;
        if (nb == -1) printf("%05d %d -1\n", g[i], dat[g[i]]);
        else          printf("%05d %d %05d\n", g[i], dat[g[i]], nb);
    }
}

int main() {
    int head, n;
    if (scanf("%d %d", &head, &n) != 2) return 0;
    for (int k = 0; k < n; k++) {
        int a, v, b;
        scanf("%d %d %d", &a, &v, &b);
        dat[a] = v; nxt[a] = b;
    }
    vector<int> kept, removed;
    vector<char> seen(100005, 0);
    for (int cur = head; cur != -1; cur = nxt[cur]) {
        int v = dat[cur];
        int k = v < 0 ? -v : v;              /* ★ 按绝对值判重 */
        if (!seen[k]) { seen[k] = 1; kept.push_back(cur); }
        else          { removed.push_back(cur); }
    }
    print_group(kept);
    if (!removed.empty()) print_group(removed);   /* ★ 空则不输出这一段 */
    return 0;
}
''',
    alt=r'''#include <cstdio>
#include <vector>
#include <set>
#include <cmath>
using namespace std;
int dat[100005], nxt[100005];

int main() {
    int head, n;
    if (scanf("%d %d", &head, &n) != 2) return 0;
    for (int k = 0; k < n; k++) {
        int a, v, b;
        scanf("%d %d %d", &a, &v, &b);
        dat[a] = v; nxt[a] = b;
    }
    vector<int> kept, removed;
    set<int> seen;                            /* 换 set 判重 */
    for (int cur = head; cur != -1; cur = nxt[cur]) {
        int k = abs(dat[cur]);
        if (seen.insert(k).second) kept.push_back(cur);
        else                       removed.push_back(cur);
    }
    for (int pass = 0; pass < 2; pass++) {
        vector<int> &g = pass == 0 ? kept : removed;
        if (g.empty()) continue;
        for (size_t i = 0; i < g.size(); i++) {
            int nb = (i + 1 < g.size()) ? g[i + 1] : -1;
            printf("%05d %d ", g[i], dat[g[i]]);
            if (nb == -1) printf("-1\n");
            else          printf("%05d\n", nb);
        }
    }
    return 0;
}
''',
)


# --------------------------------------------------------------------- #
#  L6  单链表就地逆置（PTA 7-7）
# --------------------------------------------------------------------- #

def _rand_case_l6() -> str:
    import random
    rnd = random.Random(7107)
    lines = ["3"]
    for _ in range(3):
        a = [rnd.randint(1, 1000000) for _ in range(1000)]
        lines.append(" ".join(map(str, a)) + " -1")
    return "\n".join(lines) + "\n"


def _oracle_l6(text: str) -> str:
    d = text.split()
    i = 0
    t = int(d[i]); i += 1
    out = []
    for _ in range(t):
        a = []
        while i < len(d) and d[i] != "-1":
            a.append(int(d[i])); i += 1
        i += 1                                   # 跳过分隔的 -1
        out.append(" ".join(map(str, a[::-1])))
    return "\n".join(out) + "\n"


add(
    title="单链表就地逆置（PTA 原题 · 多组输入）",
    section=SECTION,
    difficulty=2, score=15, tags=["链表", "逆置", "PTA 原题"],
    statement_md=(
        "输入多个整数，以 `-1` 作为结束标志，顺序建立一个带头结点的单链表，"
        "之后对该单链表进行**就地逆置（不增加新结点）**，并输出逆置后的单链表数据。\n\n"
        "（原题：PTA 7-7，绍兴大学 usx 程序设计类课程组，15 分）\n\n"
        "★ 「就地」= 只改 `next`，不 `new`、不开数组。三指针四步，顺序不能乱：\n"
        "```cpp\n"
        "node *pre = nullptr, *cur = head->next, *nex;\n"
        "while (cur) {\n"
        "    nex = cur->next;   // ① 先存后继，否则一改指针就断链\n"
        "    cur->next = pre;   // ② 掉头\n"
        "    pre = cur;         // ③ pre 前移\n"
        "    cur = nex;         // ④ cur 前移\n"
        "}\n"
        "head->next = pre;      // 收尾：头结点接上新的首元\n"
        "```\n"
        "这题有两处和别的逆置题不同：\n"
        "1. **多组数据**，先读 `T`。所以 `BuildList()` 每轮都要重新建表，"
        "而且它靠 `-1` 收尾 —— 上一组的 `-1` 已经被吃掉，下一组从头读就行。\n"
        "2. **空组是合法的**（一上来就是 `-1`）：`head->next` 是 `nullptr`，"
        "逆置后还是空，输出一行空行。别让 `cur->next` 在 `cur == nullptr` 上崩。"
    ),
    input_format=(
        "首先输入一个正整数 `T`，表示测试数据的组数，然后是 `T` 组测试数据。"
        "每组测试输入多个整数，以 `-1` 作为该组测试的结束（`-1` 不处理）。"
    ),
    output_format="对于每组测试，输出逆置后的单链表数据（数据之间留一个空格）。",
    constraints_md="- 1 ≤ T ≤ 10；每组长度 0 ≤ len ≤ 10⁵",
    inputs=[
        "1\n1 2 3 4 5 -1\n",
        "2\n1 -1\n1 2 -1\n",
        "1\n-1\n",
        "3\n7 7 8 -1\n-1\n1000000 -1000000 -1\n",
        _rand_case_l6(),
    ],
    samples=2,
    oracle=_oracle_l6,
    solution=r'''#include <iostream>
using namespace std;
struct node { int data; node *next; };

node *build() {                          /* 带头结点，尾插；-1 结束 */
    node *head = new node{0, nullptr};
    node *tail = head;
    int v;
    while (cin >> v && v != -1) {
        node *p = new node{v, nullptr};
        tail->next = p;
        tail = p;
    }
    return head;
}

void reverse_list(node *head) {          /* 就地逆置：只改 next */
    node *pre = nullptr, *cur = head->next, *nex;
    while (cur != nullptr) {
        nex = cur->next;                 /* ① 存后继，防断链 */
        cur->next = pre;                 /* ② 掉头 */
        pre = cur;                       /* ③ pre 前移 */
        cur = nex;                       /* ④ cur 前移 */
    }
    head->next = pre;                    /* 头结点接新首元；空表时 pre 就是 nullptr */
}

int main() {
    int T;
    if (!(cin >> T)) return 0;
    while (T--) {
        node *head = build();
        reverse_list(head);
        bool first = true;
        for (node *p = head->next; p; p = p->next) {
            if (!first) cout << " ";
            cout << p->data;
            first = false;
        }
        cout << "\n";
    }
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
using namespace std;

int main() {
    int T;
    if (!(cin >> T)) return 0;
    while (T--) {
        vector<int> a;                   /* 不真逆置，倒着输出，结果等价 */
        int v;
        while (cin >> v && v != -1) a.push_back(v);
        for (int k = (int)a.size() - 1; k >= 0; k--)
            cout << (k == (int)a.size() - 1 ? "" : " ") << a[k];
        cout << "\n";
    }
    return 0;
}
''',
)


# --------------------------------------------------------------------- #

HEADER = '''"""链表专题 · PTA 经典 —— **自动生成，不要手改**。

本文件由 `tools/gen_ds_list.py` 产出，重新生成：

    python tools/gen_ds_list.py

收录的是 PTA（浙大 DS 课程组）那批「地址-数据-地址」式链表原题：

* 7-1 两个有序链表序列的合并（NULL 约定）
* 7-2 两个有序链表序列的交集
* 7-3 重排链表
* 7-4 约瑟夫环（链表模拟）
* 7-6 链表去重（分离被删结点）
* 7-7 单链表就地逆置（多组输入）

它们和「第 02 讲 · 线性表」里那批教材简化题**输入格式不同**（-1 收尾、
静态链表地址、空结果输出 NULL），所以单独成节。

规矩与其它题库一致：期望输出由独立 Python oracle 算好；每题两套 C++ 实现双撞。
"""

DS_LIST_PROBLEMS: list[dict] = '''


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
            "total_score": int(p.get("score", 15)),
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
    ap = argparse.ArgumentParser(description="生成链表专题（PTA 经典）题库")
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
