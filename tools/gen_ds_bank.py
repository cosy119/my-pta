"""生成 `app/problems_bank_ds.py` —— 数据结构线的 C/C++ 题库。

★ 为什么用「生成」而不是手写
----------------------------
加题铁律第一条：**期望输出必须由另一套独立实现预先算出**，不能拿参考解
现跑现填（那是自己给自己判卷，永远满分、毫无意义）。

这里的做法：
- **期望输出** ← 本文件里的 `oracle`（纯 Python 实现，跟 C++ 参考解毫无关系）
- **参考解 solution** ← C++ 实现
- **第二套实现 alt_solution** ← 另一套 C++ 实现（换算法/换数据结构）

三者互不牵连：oracle 算错了，C++ 两套实现会同时撞不上；
C++ 参考解写错了，alt 解和 oracle 会把它顶出来。
最后 `tools/verify_bank.py` 把两套 C++ 都跑一遍，逐字节对拍 oracle 的输出。

用法
----
    python tools/gen_ds_bank.py            # 生成 app/problems_bank_ds.py
    python tools/gen_ds_bank.py --check    # 只校验，不写文件（CI 用）
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))     # 为了能 import _console
import _console                                               # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = ROOT / "app" / "problems_bank_ds.py"

# ===================================================================== #
#  一、题目定义
# --------------------------------------------------------------------- #
#  每道题：
#    title / section / difficulty / score / tags
#    statement_md / input_format / output_format / constraints_md
#    inputs   ← 测试点输入（手写）
#    samples  ← 前几个当样例（其余为隐藏测试点）
#    oracle   ← 独立 Python 实现，算期望输出
#    solution / alt ← 两套 C++ 实现
# ===================================================================== #

PROBLEMS: list[dict] = []


def add(**kw) -> None:
    PROBLEMS.append(kw)


# --------------------------------------------------------------------- #
#  第 02 讲 · 线性表
# --------------------------------------------------------------------- #

def _oracle_01(text: str) -> str:
    d = text.split()
    n = int(d[0])
    a = [int(v) for v in d[1:1 + n]]
    i = int(d[1 + n])
    x = int(d[2 + n])
    a.insert(i - 1, x)
    return " ".join(map(str, a)) + "\n"

add(
    title="顺序表按位插入",
    section="第 02 讲 · 线性表",
    difficulty=2, score=15, tags=["顺序表", "插入", "位序"],
    statement_md=(
        "在一个顺序表中，把 `x` 插入到**位序 `i`** 的位置上（原来的第 `i` 个及"
        "以后的元素统统后移一位）。\n\n"
        "★ 教材里的**位序从 1 开始**，而 C 数组下标从 0 开始 —— "
        "位序 `i` 对应下标 `i-1`。这是本讲最容易出错的地方。\n\n"
        "搬移必须**从后往前**做。反过来写（`j` 从小到大）会把后面的元素"
        "一路覆盖掉，而且编译器一个警告都不会给。"
    ),
    input_format=(
        "第一行一个整数 `n`（当前表长）。\n\n"
        "第二行 `n` 个整数，顺序表的元素。\n\n"
        "第三行一个整数 `i`，插入位置（位序，1 ≤ i ≤ n+1）。\n\n"
        "第四行一个整数 `x`，要插入的值。"
    ),
    output_format="一行，插入后的顺序表，元素之间用一个空格分隔。",
    constraints_md="- 1 ≤ n ≤ 1000\n- 1 ≤ i ≤ n+1",
    inputs=[
        "5\n1 2 3 4 5\n1\n9\n",
        "5\n1 2 3 4 5\n6\n9\n",
        "5\n1 2 3 4 5\n3\n9\n",
        "1\n7\n1\n0\n",
        "1\n7\n2\n8\n",
    ],
    samples=2,

    oracle=_oracle_01,

    solution=r'''#include <stdio.h>
#define MAXN 2005
int a[MAXN];
int main(void) {
    int n, i, x;
    scanf("%d", &n);
    for (int k = 0; k < n; k++) scanf("%d", &a[k]);
    scanf("%d %d", &i, &x);
    // ★ 从后往前搬：位序 i 对应下标 i-1，把 [i-1, n-1] 整体后移一格
    for (int j = n - 1; j >= i - 1; j--) a[j + 1] = a[j];
    a[i - 1] = x;
    n++;
    for (int k = 0; k < n; k++) printf("%d%c", a[k], k + 1 == n ? '\n' : ' ');
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n; cin >> n;
    vector<int> a(n);
    for (int &v : a) cin >> v;
    int i, x; cin >> i >> x;
    vector<int> b;                       // 另一套：不原地搬，重新拼一份
    for (int k = 0; k < n; k++) {
        if (k == i - 1) b.push_back(x);
        b.push_back(a[k]);
    }
    if (i == n + 1) b.push_back(x);      // 插到末尾（原表后无元素可触发）
    for (size_t k = 0; k < b.size(); k++)
        cout << b[k] << (k + 1 == b.size() ? '\n' : ' ');
    return 0;
}
''',
)

def _oracle_02(text: str) -> str:
    d = text.split()
    n = int(d[0])
    a = [int(v) for v in d[1:1 + n]]
    x = int(d[1 + n])
    kept = [v for v in a if v != x]
    return (" ".join(map(str, kept)) if kept else "empty") + "\n"

add(
    title="顺序表删除所有值为 x 的元素",
    section="第 02 讲 · 线性表",
    difficulty=2, score=15, tags=["顺序表", "删除", "双指针"],
    statement_md=(
        "删除顺序表中**所有**值为 `x` 的元素，剩下的元素保持原来的相对次序。\n\n"
        "要求 O(n) 时间、O(1) 额外空间 —— 也就是用一个写指针 `k` "
        "把「该留下的」往前压，不要每次都搬一整个数组。\n\n"
        "若删完表为空，输出 `empty`。"
    ),
    input_format=(
        "第一行一个整数 `n`。\n\n"
        "第二行 `n` 个整数。\n\n"
        "第三行一个整数 `x`。"
    ),
    output_format="一行，删除后的顺序表（空格分隔）；若为空则输出 `empty`。",
    constraints_md="- 1 ≤ n ≤ 1000",
    inputs=[
        "5\n1 2 3 2 4\n2\n",
        "3\n2 2 2\n2\n",
        "4\n1 2 3 4\n5\n",
        "1\n5\n5\n",
        "6\n1 1 2 2 3 3\n1\n",
    ],
    samples=2,

    oracle=_oracle_02,

    solution=r'''#include <stdio.h>
int a[1005];
int main(void) {
    int n, x;
    scanf("%d", &n);
    for (int k = 0; k < n; k++) scanf("%d", &a[k]);
    scanf("%d", &x);
    int k = 0;                       // k = 写指针：下一个该留下的位置
    for (int j = 0; j < n; j++)
        if (a[j] != x) a[k++] = a[j];
    if (k == 0) { printf("empty\n"); return 0; }
    for (int j = 0; j < k; j++) printf("%d%c", a[j], j + 1 == k ? '\n' : ' ');
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n; cin >> n;
    vector<int> a(n);
    for (int &v : a) cin >> v;
    int x; cin >> x;
    vector<int> out;                 // 另一套：直接挑出该留的，不原地压缩
    for (int v : a) if (v != x) out.push_back(v);
    if (out.empty()) { cout << "empty\n"; return 0; }
    for (size_t k = 0; k < out.size(); k++)
        cout << out[k] << (k + 1 == out.size() ? '\n' : ' ');
    return 0;
}
''',
)

def _oracle_03(text: str) -> str:
    d = text.split()
    n = int(d[0])
    a = [int(v) for v in d[1:1 + n]]
    i, j = int(d[1 + n]), int(d[2 + n])
    kept = a[:i - 1] + a[j:]
    return (" ".join(map(str, kept)) if kept else "empty") + "\n"

add(
    title="顺序表删除区间元素",
    section="第 02 讲 · 线性表",
    difficulty=2, score=15, tags=["顺序表", "删除", "区间"],
    statement_md=(
        "删除顺序表中**位序**从 `i` 到 `j`（含两端）的所有元素，"
        "后面的元素整体前移。\n\n"
        "搬移方向跟插入**正好相反**：这里是**从前往后**搬"
        "（把 `j` 后面的元素往前填），写反了同样会静默出错。"
    ),
    input_format=(
        "第一行一个整数 `n`。\n\n"
        "第二行 `n` 个整数。\n\n"
        "第三行两个整数 `i` `j`（1 ≤ i ≤ j ≤ n）。"
    ),
    output_format="一行，删除后的顺序表（空格分隔）；若为空则输出 `empty`。",
    constraints_md="- 1 ≤ n ≤ 1000",
    inputs=[
        "6\n10 20 30 40 50 60\n2 4\n",
        "5\n1 2 3 4 5\n1 5\n",
        "5\n1 2 3 4 5\n1 1\n",
        "5\n1 2 3 4 5\n5 5\n",
        "4\n9 8 7 6\n2 3\n",
    ],
    samples=2,

    oracle=_oracle_03,

    solution=r'''#include <stdio.h>
int a[1005];
int main(void) {
    int n, i, j;
    scanf("%d", &n);
    for (int k = 0; k < n; k++) scanf("%d", &a[k]);
    scanf("%d %d", &i, &j);
    int cnt = j - i + 1;                     // 要删掉几个
    for (int k = j; k < n; k++) a[k - cnt] = a[k];   // 从前往后搬
    n -= cnt;
    if (n == 0) { printf("empty\n"); return 0; }
    for (int k = 0; k < n; k++) printf("%d%c", a[k], k + 1 == n ? '\n' : ' ');
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n; cin >> n;
    vector<int> a(n);
    for (int &v : a) cin >> v;
    int i, j; cin >> i >> j;
    vector<int> out;                       // 另一套：按下标挑，不做原地搬移
    for (int k = 0; k < n; k++)
        if (k < i - 1 || k > j - 1) out.push_back(a[k]);
    if (out.empty()) { cout << "empty\n"; return 0; }
    for (size_t k = 0; k < out.size(); k++)
        cout << out[k] << (k + 1 == out.size() ? '\n' : ' ');
    return 0;
}
''',
)

def _oracle_04(text: str) -> str:
    d = text.split()
    n = int(d[0])
    a = [int(v) for v in d[1:1 + n]]
    return " ".join(map(str, a[::-1])) + "\n"

add(
    title="顺序表原地逆置",
    section="第 02 讲 · 线性表",
    difficulty=2, score=15, tags=["顺序表", "逆置", "首尾交换"],
    statement_md=(
        "把顺序表**原地**逆置（不借第二个数组），用首尾交换向中间收拢的写法。\n\n"
        "这是考研高频题：O(n) 时间、O(1) 空间。\n\n"
        "注意循环条件是 `i < j` 而不是 `i <= j` —— 写成 `<=` 时中间那个元素"
        "会自己跟自己换一次，结果**碰巧还是对的**，于是这个错误永远暴露不出来。"
    ),
    input_format="第一行一个整数 `n`。\n\n第二行 `n` 个整数。",
    output_format="一行，逆置后的顺序表（空格分隔）。",
    constraints_md="- 1 ≤ n ≤ 1000",
    inputs=[
        "5\n1 2 3 4 5\n",
        "4\n1 2 3 4\n",
        "1\n42\n",
        "2\n7 8\n",
        "6\n-1 -2 -3 -4 -5 -6\n",
    ],
    samples=2,

    oracle=_oracle_04,

    solution=r'''#include <stdio.h>
int a[1005];
int main(void) {
    int n;
    scanf("%d", &n);
    for (int k = 0; k < n; k++) scanf("%d", &a[k]);
    for (int i = 0, j = n - 1; i < j; i++, j--) {
        int t = a[i]; a[i] = a[j]; a[j] = t;
    }
    for (int k = 0; k < n; k++) printf("%d%c", a[k], k + 1 == n ? '\n' : ' ');
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <algorithm>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n; cin >> n;
    int a[1005];
    for (int k = 0; k < n; k++) cin >> a[k];
    reverse(a, a + n);                    // 另一套：直接用标准库的逆置
    for (int k = 0; k < n; k++) cout << a[k] << (k + 1 == n ? '\n' : ' ');
    return 0;
}
''',
)

def _oracle_05(text: str) -> str:
    d = text.split()
    n = int(d[0])
    p = 1
    a = [int(v) for v in d[p:p + n]]
    p += n
    m = int(d[p])
    p += 1
    b = [int(v) for v in d[p:p + m]]
    out = sorted(a + b)
    return (" ".join(map(str, out)) if out else "empty") + "\n"

add(
    title="合并两个有序顺序表",
    section="第 02 讲 · 线性表",
    difficulty=3, score=20, tags=["顺序表", "归并", "双指针"],
    statement_md=(
        "把两个**非递减**顺序表合并成一个非递减顺序表。\n\n"
        "标准做法是双指针归并：谁小先输出谁，一个走完就把另一个整段接上。\n\n"
        "要求 O(n+m) —— 把两段拼起来再排序虽然结果也对，但那是 O((n+m)log)。"
    ),
    input_format=(
        "第一行一个整数 `n`，第二行 `n` 个非递减整数。\n\n"
        "第三行一个整数 `m`，第四行 `m` 个非递减整数。\n\n"
        "（`n` 和 `m` 都可能为 0，此时对应的那行为空行。）"
    ),
    output_format="一行，合并后的非递减序列（空格分隔）；两者都空则输出 `empty`。",
    constraints_md="- 0 ≤ n, m ≤ 1000",
    inputs=[
        "3\n1 3 5\n3\n2 4 6\n",
        "4\n1 2 3 4\n0\n\n",
        "0\n\n3\n7 8 9\n",
        "0\n\n0\n\n",
        "3\n1 1 2\n3\n1 2 2\n",
    ],
    samples=2,

    oracle=_oracle_05,

    solution=r'''#include <stdio.h>
int a[1005], b[1005], c[2010];
int main(void) {
    int n, m;
    scanf("%d", &n);
    for (int k = 0; k < n; k++) scanf("%d", &a[k]);
    scanf("%d", &m);
    for (int k = 0; k < m; k++) scanf("%d", &b[k]);
    int i = 0, j = 0, t = 0;
    while (i < n && j < m) c[t++] = (a[i] <= b[j]) ? a[i++] : b[j++];
    while (i < n) c[t++] = a[i++];
    while (j < m) c[t++] = b[j++];
    if (t == 0) { printf("empty\n"); return 0; }
    for (int k = 0; k < t; k++) printf("%d%c", c[k], k + 1 == t ? '\n' : ' ');
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n; cin >> n;
    vector<int> a(n); for (int &v : a) cin >> v;
    int m; cin >> m;
    vector<int> b(m); for (int &v : b) cin >> v;
    // 另一套：先整体拼接，再用 stable_sort —— 结果同样是全局非递减
    vector<int> c = a;
    c.insert(c.end(), b.begin(), b.end());
    stable_sort(c.begin(), c.end());
    if (c.empty()) { cout << "empty\n"; return 0; }
    for (size_t k = 0; k < c.size(); k++)
        cout << c[k] << (k + 1 == c.size() ? '\n' : ' ');
    return 0;
}
''',
)

def _oracle_06(text: str) -> str:
    d = text.split()
    n = int(d[0])
    a = [int(v) for v in d[1:1 + n]]
    if not a:
        return "NULL\n"
    return "".join("%d -> " % v for v in a) + "NULL\n"

add(
    title="单链表尾插建表并遍历",
    section="第 02 讲 · 线性表",
    difficulty=2, score=15, tags=["单链表", "尾插法", "遍历"],
    statement_md=(
        "用**尾插法**建立带头结点的单链表，然后从头到尾遍历输出。\n\n"
        "尾插法的关键在于**始终维护一个尾指针 `rear`**：\n\n"
        "```c\n"
        "s->next = NULL;   /* 新结点自己就是尾巴，next 必须先置空 */\n"
        "rear->next = s;   /* 挂到尾巴后面 */\n"
        "rear = s;         /* 尾巴挪到新结点 */\n"
        "```\n\n"
        "★ 第一句 `s->next = NULL` **不能省**。少了它，最后一个结点的 `next` "
        "就是 malloc 拿到的随机地址，遍历时不是打印垃圾就是段错误 —— "
        "而且**有时正常、有时崩**，是最难查的一类 bug。\n\n"
        "输出格式：每个结点后面跟 ` -> `，最后以 `NULL` 结尾。"
    ),
    input_format="第一行一个整数 `n`。\n\n第二行 `n` 个整数（`n` 可以为 0）。",
    output_format="一行，形如 `1 -> 2 -> 3 -> NULL`；空表输出 `NULL`。",
    constraints_md="- 0 ≤ n ≤ 1000",
    inputs=[
        "3\n1 2 3\n",
        "5\n10 20 30 40 50\n",
        "0\n\n",
        "1\n7\n",
        "4\n-1 0 1 2\n",
    ],
    samples=2,

    oracle=_oracle_06,

    solution=r'''#include <stdio.h>
#include <stdlib.h>
typedef struct LNode { int data; struct LNode *next; } LNode, *LinkList;
int main(void) {
    int n;
    scanf("%d", &n);
    LinkList head = (LinkList)malloc(sizeof(LNode));   /* 头结点 */
    head->next = NULL;
    LNode *rear = head;                               /* ★ 尾指针 */
    for (int k = 0; k < n; k++) {
        int v; scanf("%d", &v);
        LNode *s = (LNode *)malloc(sizeof(LNode));
        s->data = v;
        s->next = NULL;            /* ★ 不能省，否则尾结点 next 是随机地址 */
        rear->next = s;
        rear = s;
    }
    for (LNode *p = head->next; p; p = p->next) printf("%d -> ", p->data);
    printf("NULL\n");
    return 0;
}
''',
    alt=r'''#include <iostream>
using namespace std;
typedef struct LNode { int data; struct LNode *next; } LNode, *LinkList;
// 另一套：先**头插**把元素倒着接进去，再整体逆置——结果与尾插一致
static LinkList insertHead(LinkList head, int v) {
    LNode *s = new LNode(); s->data = v; s->next = head->next; head->next = s;
    return head;
}
static void reverseList(LinkList head) {
    LNode *p = head->next, *q = NULL;
    while (p) { LNode *r = p->next; p->next = q; q = p; p = r; }
    head->next = q;
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n; cin >> n;
    LinkList head = new LNode(); head->next = NULL;
    for (int k = 0; k < n; k++) { int v; cin >> v; insertHead(head, v); }
    reverseList(head);
    for (LNode *p = head->next; p; p = p->next) cout << p->data << " -> ";
    cout << "NULL\n";
    return 0;
}
''',
)

def _oracle_07(text: str) -> str:
    d = text.split()
    n = int(d[0])
    a = [int(v) for v in d[1:1 + n]]
    x = int(d[1 + n])
    kept = [v for v in a if v != x]
    if not kept:
        return "NULL\n"
    return "".join("%d -> " % v for v in kept) + "NULL\n"

add(
    title="单链表删除所有值为 x 的结点",
    section="第 02 讲 · 线性表",
    difficulty=3, score=20, tags=["单链表", "删除", "双指针"],
    statement_md=(
        "删除带头结点单链表中**所有**值为 `x` 的结点，保持其余结点次序不变。\n\n"
        "★ 关键在 `else`：**只有没删的时候 `p` 才前进**。\n\n"
        "```c\n"
        "if (p->next->data == x) { q = p->next; p->next = q->next; free(q); }\n"
        "else p = p->next;          /* ← 删了就在原地再查一次 */\n"
        "```\n\n"
        "写成「每次都 `p = p->next`」，遇到**连续两个 `x`** 时会漏删后面那个。\n\n"
        "输出格式与上一题一致。"
    ),
    input_format="第一行一个整数 `n`。\n\n第二行 `n` 个整数。\n\n第三行一个整数 `x`。",
    output_format="一行，形如 `1 -> 3 -> NULL`；删空则输出 `NULL`。",
    constraints_md="- 0 ≤ n ≤ 1000",
    inputs=[
        "6\n1 2 3 2 4 2\n2\n",
        "3\n5 5 5\n5\n",
        "4\n1 2 3 4\n9\n",
        "2\n7 7\n7\n",
        "5\n1 1 2 1 1\n1\n",
    ],
    samples=2,

    oracle=_oracle_07,

    solution=r'''#include <stdio.h>
#include <stdlib.h>
typedef struct LNode { int data; struct LNode *next; } LNode, *LinkList;
int main(void) {
    int n, x;
    scanf("%d", &n);
    LinkList head = (LinkList)malloc(sizeof(LNode));
    head->next = NULL;
    LNode *rear = head;
    for (int k = 0; k < n; k++) {
        int v; scanf("%d", &v);
        LNode *s = (LNode *)malloc(sizeof(LNode));
        s->data = v; s->next = NULL;
        rear->next = s; rear = s;
    }
    scanf("%d", &x);
    LNode *p = head;
    while (p->next) {
        if (p->next->data == x) {
            LNode *q = p->next;
            p->next = q->next;      /* 先摘链，再 free */
            free(q);
        } else {
            p = p->next;            /* ★ 删了就不前进，原地再查 */
        }
    }
    for (LNode *t = head->next; t; t = t->next) printf("%d -> ", t->data);
    printf("NULL\n");
    return 0;
}
''',
    alt=r'''#include <iostream>
using namespace std;
typedef struct LNode { int data; struct LNode *next; } LNode, *LinkList;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n; cin >> n;
    LinkList head = new LNode(); head->next = NULL;
    LNode *rear = head;
    for (int k = 0; k < n; k++) {
        int v; cin >> v;
        LNode *s = new LNode(); s->data = v; s->next = NULL;
        rear->next = s; rear = s;
    }
    int x; cin >> x;
    // 另一套：建一条**新链表**，只把不等于 x 的结点尾插过去
    LinkList h2 = new LNode(); h2->next = NULL;
    LNode *r2 = h2;
    for (LNode *p = head->next; p; p = p->next)
        if (p->data != x) {
            LNode *s = new LNode(); s->data = p->data; s->next = NULL;
            r2->next = s; r2 = s;
        }
    for (LNode *t = h2->next; t; t = t->next) cout << t->data << " -> ";
    cout << "NULL\n";
    return 0;
}
''',
)

def _oracle_08(text: str) -> str:
    d = text.split()
    n = int(d[0])
    a = [int(v) for v in d[1:1 + n]]
    rev = a[::-1]
    if not rev:
        return "NULL\n"
    return "".join("%d -> " % v for v in rev) + "NULL\n"

add(
    title="单链表就地逆置",
    section="第 02 讲 · 线性表",
    difficulty=3, score=20, tags=["单链表", "逆置", "指针"],
    statement_md=(
        "把带头结点的单链表**就地**逆置（不新建结点、不借数组）。\n\n"
        "经典三指针写法：`p` 走原链，`q` 攒新链，`r` 提前记住下一个。\n\n"
        "```c\n"
        "while (p) { r = p->next; p->next = q; q = p; p = r; }\n"
        "head->next = q;\n"
        "```\n\n"
        "★ 顺序不能乱：**先存 `r = p->next` 再改 `p->next`**。"
        "反过来写的话，改完之后 `p->next` 已经指向新链，原来的后续结点就找不回来了。"
    ),
    input_format="第一行一个整数 `n`。\n\n第二行 `n` 个整数。",
    output_format="一行，形如 `3 -> 2 -> 1 -> NULL`；空表输出 `NULL`。",
    constraints_md="- 0 ≤ n ≤ 1000",
    inputs=[
        "5\n1 2 3 4 5\n",
        "1\n9\n",
        "0\n\n",
        "4\n10 20 30 40\n",
        "6\n-1 -2 -3 -4 -5 -6\n",
    ],
    samples=2,

    oracle=_oracle_08,

    solution=r'''#include <stdio.h>
#include <stdlib.h>
typedef struct LNode { int data; struct LNode *next; } LNode, *LinkList;
int main(void) {
    int n;
    scanf("%d", &n);
    LinkList head = (LinkList)malloc(sizeof(LNode));
    head->next = NULL;
    LNode *rear = head;
    for (int k = 0; k < n; k++) {
        int v; scanf("%d", &v);
        LNode *s = (LNode *)malloc(sizeof(LNode));
        s->data = v; s->next = NULL;
        rear->next = s; rear = s;
    }
    LNode *p = head->next, *q = NULL;
    while (p) {
        LNode *r = p->next;     /* ★ 先记下后继，再改 next */
        p->next = q;
        q = p; p = r;
    }
    head->next = q;
    for (LNode *t = head->next; t; t = t->next) printf("%d -> ", t->data);
    printf("NULL\n");
    return 0;
}
''',
    alt=r'''#include <iostream>
using namespace std;
typedef struct LNode { int data; struct LNode *next; } LNode, *LinkList;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n; cin >> n;
    // 另一套：**头插法**建表，读进来就是逆序的，不需要再逆置
    LinkList head = new LNode(); head->next = NULL;
    for (int k = 0; k < n; k++) {
        int v; cin >> v;
        LNode *s = new LNode(); s->data = v;
        s->next = head->next; head->next = s;
    }
    for (LNode *t = head->next; t; t = t->next) cout << t->data << " -> ";
    cout << "NULL\n";
    return 0;
}
''',
)


# --------------------------------------------------------------------- #
#  第 03 讲 · 栈和队列
# --------------------------------------------------------------------- #

def _oracle_09(text: str) -> str:
    s = text.strip()
    pairs = {")": "(", "]": "[", "}": "{"}
    st = []
    for ch in s:
        if ch in "([{":
            st.append(ch)
        elif ch in pairs:
            if not st or st[-1] != pairs[ch]:
                return "no\n"
            st.pop()
    return "yes\n" if not st else "no\n"

add(
    title="括号匹配",
    section="第 03 讲 · 栈和队列",
    difficulty=2, score=15, tags=["栈", "括号匹配", "基础应用"],
    statement_md=(
        "给定一个只由 `()[]{}` 组成的字符串，判断括号是否**正确配对**。\n\n"
        "栈的教科书应用。三条判据缺一不可：\n\n"
        "1. 遇到**左**括号 → 压栈\n"
        "2. 遇到**右**括号 → 栈必须非空，且栈顶是**对应的左**括号\n"
        "3. 扫完之后栈必须**空**\n\n"
        "★ 最容易漏的是第 3 条：`(()` 在第 2 条上一点问题都没有，"
        "只有在收尾检查栈时才会暴露。\n\n"
        "配对输出 `yes`，否则 `no`。"
    ),
    input_format="一行，一个不含空格的字符串，只由 `()[]{}` 组成。",
    output_format="一行，`yes` 或 `no`。",
    constraints_md="- 字符串长度不超过 10000",
    inputs=["()\n", "(]\n", "([{}])\n", "(()\n", ")(\n", "{[()]}\n"],
    samples=3,

    oracle=_oracle_09,

    solution=r'''#include <stdio.h>
#include <string.h>
char s[10005], st[10005];
int main(void) {
    scanf("%s", s);
    int n = (int)strlen(s), top = 0;
    for (int i = 0; i < n; i++) {
        char c = s[i];
        if (c == '(' || c == '[' || c == '{') {
            st[top++] = c;
        } else {
            char want = (c == ')') ? '(' : (c == ']') ? '[' : '{';
            if (top == 0 || st[top - 1] != want) { printf("no\n"); return 0; }
            top--;
        }
    }
    printf(top == 0 ? "yes\n" : "no\n");   /* ★ 收尾必须查栈空 */
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <string>
#include <stack>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s; cin >> s;
    stack<char> st;
    bool ok = true;
    for (char c : s) {
        if (c == '(') st.push(')');
        else if (c == '[') st.push(']');
        else if (c == '{') st.push('}');
        else {                                  // 另一套：存「期望的右括号」，比对更直接
            if (st.empty() || st.top() != c) { ok = false; break; }
            st.pop();
        }
    }
    if (!st.empty()) ok = false;
    cout << (ok ? "yes" : "no") << "\n";
    return 0;
}
''',
)

def _oracle_10(text: str) -> str:
    d = text.split()
    n, r = int(d[0]), int(d[1])
    if n == 0:
        return "0\n"
    digits = "0123456789ABCDEF"
    out = []
    while n:
        out.append(digits[n % r])
        n //= r
    return "".join(reversed(out)) + "\n"

add(
    title="用栈实现进制转换",
    section="第 03 讲 · 栈和队列",
    difficulty=2, score=15, tags=["栈", "进制转换", "取余"],
    statement_md=(
        "把十进制非负整数 `n` 转换成 `r` 进制（2 ≤ r ≤ 16）。\n\n"
        "转换过程是**除 r 取余、倒着读**：「倒着读」正好就是栈的后进先出，"
        "所以一边算一边压栈，最后依次弹出即可。\n\n"
        "10~15 用**大写**字母 `A`~`F` 表示。"
    ),
    input_format="一行，两个整数 `n` 和 `r`。",
    output_format="一行，`n` 的 `r` 进制表示（不含前导零；`n = 0` 输出 `0`）。",
    constraints_md="- 0 ≤ n ≤ 2^31-1\n- 2 ≤ r ≤ 16",
    inputs=["10 2\n", "255 16\n", "0 2\n", "1000 8\n", "255 2\n", "1 16\n"],
    samples=3,

    oracle=_oracle_10,

    solution=r'''#include <stdio.h>
int st[64];
int main(void) {
    long long n; int r;
    scanf("%lld %d", &n, &r);
    if (n == 0) { printf("0\n"); return 0; }
    const char *D = "0123456789ABCDEF";
    int top = 0;
    while (n > 0) { st[top++] = (int)(n % r); n /= r; }
    while (top > 0) putchar(D[st[--top]]);
    putchar('\n');
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <string>
using namespace std;
static void conv(long long n, int r, string &out) {
    // 另一套：递归。回溯时把当前位接到结果后面，天然就是「倒着读」
    if (n == 0) return;
    conv(n / r, r, out);
    out += "0123456789ABCDEF"[n % r];
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    long long n; int r; cin >> n >> r;
    if (n == 0) { cout << "0\n"; return 0; }
    string out;
    conv(n, r, out);
    cout << out << "\n";
    return 0;
}
''',
)

def _oracle_11(text: str) -> str:
    d = text.split()
    n = int(d[0])
    want = [int(v) for v in d[1:1 + n]]
    st, p = [], 1
    for v in want:
        while p <= n and (not st or st[-1] != v):
            st.append(p)
            p += 1
        if st and st[-1] == v:
            st.pop()
        else:
            return "no\n"
    return "yes\n"

add(
    title="判断出栈序列是否合法",
    section="第 03 讲 · 栈和队列",
    difficulty=3, score=20, tags=["栈", "出栈序列", "模拟"],
    statement_md=(
        "入栈序列固定为 `1, 2, 3, …, n`（按此顺序推进去），"
        "中途可以随时出栈。判断给定的序列**有没有可能**是出栈序列。\n\n"
        "判定方法是「跟着走一遍」：\n\n"
        "```c\n"
        "int p = 1;                /* 下一个要入栈的数 */\n"
        "for (每个目标值 v) {\n"
        "    while (p <= n && (栈空 || 栈顶 != v)) 压入 p++;\n"
        "    if (栈顶 == v) 弹出; else 非法;\n"
        "}\n"
        "```\n\n"
        "结论记牢：**`n` 个元素出栈序列的个数是卡特兰数**，`n = 3` 时只有 5 种合法。\n\n"
        "合法输出 `yes`，否则 `no`。"
    ),
    input_format="第一行一个整数 `n`。\n\n第二行 `n` 个整数，是待判断的出栈序列。",
    output_format="一行，`yes` 或 `no`。",
    constraints_md="- 1 ≤ n ≤ 1000",
    inputs=[
        "3\n1 2 3\n",
        "3\n3 2 1\n",
        "3\n3 1 2\n",
        "4\n1 3 2 4\n",
        "4\n4 3 2 1\n",
        "1\n1\n",
        "5\n1 2 4 5 3\n",
    ],
    samples=3,

    oracle=_oracle_11,

    solution=r'''#include <stdio.h>
int st[1005];
int main(void) {
    int n;
    scanf("%d", &n);
    int p = 1, top = 0, ok = 1;
    for (int i = 0; i < n; i++) {
        int v; scanf("%d", &v);
        while (p <= n && (top == 0 || st[top - 1] != v)) st[top++] = p++;
        if (top > 0 && st[top - 1] == v) top--;
        else ok = 0;
    }
    printf(ok ? "yes\n" : "no\n");
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
#include <stack>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n; cin >> n;
    vector<int> want(n);
    for (int &v : want) cin >> v;
    // 另一套：换一种推进节奏 —— 先按目标值压栈，再统一判断
    stack<int> st;
    int p = 1;
    bool ok = true;
    for (int i = 0; i < n && ok; i++) {
        while (p <= n && (st.empty() || st.top() != want[i])) { st.push(p); p++; }
        if (!st.empty() && st.top() == want[i]) st.pop();
        else ok = false;
    }
    cout << (ok ? "yes" : "no") << "\n";
    return 0;
}
''',
)

def _oracle_12(text: str) -> str:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    m = int(lines[0])
    cap = max(0, m - 1)          # 牺牲一个单元
    q: list[int] = []
    out: list[str] = []
    for ln in lines[1:]:
        if ln == "end":
            break
        if ln == "out":
            out.append(str(q.pop(0)) if q else "empty")
        elif ln.startswith("in"):
            v = ln.split()[1]
            if len(q) >= cap:
                out.append("full")
            else:
                q.append(int(v))
    out.append(" ".join(map(str, q)) if q else "empty")
    return "\n".join(out) + "\n"

add(
    title="循环队列操作模拟",
    section="第 03 讲 · 栈和队列",
    difficulty=3, score=20, tags=["队列", "循环队列", "队满队空"],
    statement_md=(
        "循环队列容量为 `m`，按给定顺序处理入队 / 出队操作。\n\n"
        "★ 循环队列用「牺牲一个存储单元」区分队空与队满，这是教材的经典设计：\n\n"
        "```c\n"
        "队空：(rear + 1) % m == front   /* 不对，这里容易记反 */\n"
        "队空：front == rear\n"
        "队满：(rear + 1) % m == front   /* 尾指针再走一格就顶上头指针 */\n"
        "```\n\n"
        "因为要用一个空位来区分，所以**容量 `m` 的循环队列最多只能存 `m-1` 个元素**。"
        "这点想通了，队满条件就不会记反。\n\n"
        "本机模拟时可以直接用「长度计数」，只要**输出与判据一致**即可。\n\n"
        "> [!warning] 一个专治流式输入的坑\n"
        "> `in x` 里那个 `x`，**不管队满没满都得先读进来**。\n"
        "> 只在不满的分支里读，队满时 `x` 就留在输入流里，"
        "> 下一次读操作符会把它读走 —— 后面整段输出错位，"
        "> 而现象只是「莫名其妙多打了几个 full」，极难 debug。"
    ),
    input_format=(
        "第一行一个整数 `m`（队列容量）。\n\n"
        "随后若干行，每行是下面三种之一：\n\n"
        "- `in x` —— 把 `x` 入队\n"
        "- `out` —— 出队\n"
        "- `end` —— 结束\n\n"
        "`out` 时若队空，输出 `empty`；`in` 时若队满，输出 `full`。"
    ),
    output_format=(
        "对每个 `out` 输出出队元素、对每个失败的 `in` 输出 `full`（各占一行）；\n\n"
        "最后一行输出队列中剩余元素（空格分隔），队空则输出 `empty`。"
    ),
    constraints_md="- 1 ≤ m ≤ 100\n- 操作数不超过 500",
    inputs=[
        "3\nin 1\nin 2\nout\nin 3\nin 4\nin 5\nout\nout\nout\nend\n",
        "2\nout\nend\n",
        "2\nin 5\nin 6\nin 7\nin 8\nout\nend\n",
        "1\nin 1\nout\nin 2\nout\nend\n",
        "4\nin 1\nin 2\nin 3\nout\nin 9\nout\nend\n",
    ],
    samples=2,

    oracle=_oracle_12,

    solution=r'''#include <stdio.h>
#include <string.h>
int q[105];
int main(void) {
    int m;
    scanf("%d", &m);
    int cap = m - 1;                 /* ★ 牺牲一个单元 */
    if (cap < 0) cap = 0;
    int front = 0, rear = 0, size = 0;   /* 用 size 计数，判据更直白 */
    char op[16];
    while (scanf("%s", op) == 1 && strcmp(op, "end") != 0) {
        if (strcmp(op, "out") == 0) {
            if (size == 0) printf("empty\n");
            else { printf("%d\n", q[front]); front = (front + 1) % m; size--; }
        } else {
            int x;
            /* ★ 无论队满不满，都要先把入队元素读掉。
               漏掉这一句（只在 else 里读），队满时那个数字就会留在输入流里，
               下一次 scanf("%s") 会把它当成一条新指令 —— 输出开始整段错位，
               而且看起来只是「多打了几个 full」，极难定位。 */
            scanf("%d", &x);
            if (size >= cap) printf("full\n");
            else { q[rear] = x; rear = (rear + 1) % m; size++; }
        }
    }
    if (size == 0) printf("empty\n");
    else {
        for (int k = 0; k < size; k++)
            printf("%d%c", q[(front + k) % m], k + 1 == size ? '\n' : ' ');
    }
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <string>
#include <deque>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int m; cin >> m;
    int cap = (m - 1 < 0) ? 0 : m - 1;
    deque<int> q;                    // 另一套：直接用双端队列，靠 size 模拟
    string op;
    while (cin >> op && op != "end") {
        if (op == "out") {
            if (q.empty()) cout << "empty\n";
            else { cout << q.front() << "\n"; q.pop_front(); }
        } else {
            int x; cin >> x;
            if ((int)q.size() >= cap) cout << "full\n";
            else q.push_back(x);
        }
    }
    if (q.empty()) cout << "empty\n";
    else {
        for (size_t k = 0; k < q.size(); k++)
            cout << q[k] << (k + 1 == q.size() ? '\n' : ' ');
    }
    return 0;
}
''',
)

def _oracle_13(text: str) -> str:
    st: list[int] = []
    for tk in text.split():
        if tk in ("+", "-", "*", "/"):
            b = st.pop()          # 先弹的是右操作数
            a = st.pop()
            if tk == "+":
                st.append(a + b)
            elif tk == "-":
                st.append(a - b)
            elif tk == "*":
                st.append(a * b)
            else:
                # C 语言整除是向零取整，Python 的 // 是向下取整，必须分开处理
                q = abs(a) // abs(b)
                st.append(q if (a < 0) == (b < 0) else -q)
        else:
            st.append(int(tk))
    return "%d\n" % st[-1]

add(
    title="后缀表达式求值",
    section="第 03 讲 · 栈和队列",
    difficulty=3, score=20, tags=["栈", "表达式求值", "后缀表达式"],
    statement_md=(
        "计算一个**后缀表达式**（也叫逆波兰式）的值。\n\n"
        "规则很简单：遇到操作数就压栈；遇到运算符就弹出**两个**操作数算一下再压回去。\n\n"
        "★ 弹出顺序不能反：**先弹出来的是右操作数**。写成 `a - b`（先弹的在前）"
        "做减法／除法时结果就错了，而加法乘法恰好看不出来 —— "
        "这是后缀求值最隐蔽的坑。\n\n"
        "除法按 **C 语言整数除法**（向零取整，如 `-7 / 2 = -3`），保证除数非 0。"
    ),
    input_format="一行，若干 token 用空格分隔。token 是整数或 `+ - * /` 之一。",
    output_format="一行，一个整数，表达式的值。",
    constraints_md="- token 数不超过 1000\n- 中间结果在 64 位整数范围内",
    inputs=[
        "3 4 +\n",
        "5 1 2 + 4 * + 3 -\n",
        "7 2 /\n",
        "2 3 4 * +\n",
        "10 3 - 2 *\n",
        "3 5 -\n",
        "2 3 + 4 5 + *\n",
    ],
    samples=3,

    oracle=_oracle_13,

    solution=r'''#include <stdio.h>
#include <string.h>
#include <stdlib.h>
long long st[1005];
int main(void) {
    char tk[64];
    int top = 0;
    while (scanf("%s", tk) == 1) {
        if (!strcmp(tk, "+") || !strcmp(tk, "-") || !strcmp(tk, "*") || !strcmp(tk, "/")) {
            long long b = st[--top];     /* ★ 先弹出来的是右操作数 */
            long long a = st[--top];
            long long v = 0;
            if (tk[0] == '+') v = a + b;
            else if (tk[0] == '-') v = a - b;
            else if (tk[0] == '*') v = a * b;
            else v = a / b;              /* C 的整除天然向零取整 */
            st[top++] = v;
        } else {
            st[top++] = atoll(tk);
        }
    }
    printf("%lld\n", st[top - 1]);
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <string>
#include <vector>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    vector<long long> st;
    string tk;
    while (cin >> tk) {
        if (tk.size() == 1 && string("+-*/").find(tk[0]) != string::npos) {
            long long b = st.back(); st.pop_back();
            long long a = st.back(); st.pop_back();
            long long v;
            // 另一套：先算「先弹的那个」的相反数思路 → 用 switch 显式区分左右
            switch (tk[0]) {
                case '+': v = a + b; break;
                case '-': v = a - b; break;
                case '*': v = a * b; break;
                default:  v = a / b; break;
            }
            st.push_back(v);
        } else {
            st.push_back(stoll(tk));
        }
    }
    cout << st.back() << "\n";
    return 0;
}
''',
)

def _oracle_14(text: str) -> str:
    s = text.strip()
    return "yes\n" if s == s[::-1] else "no\n"

add(
    title="用栈判断回文串",
    section="第 03 讲 · 栈和队列",
    difficulty=1, score=10, tags=["栈", "回文", "字符串"],
    statement_md=(
        "判断一个字符串是不是**回文**（正着读和倒着读一样）。\n\n"
        "用栈的做法：把整个串压栈，再依次弹出与原串逐字符比较。\n"
        "弹出的顺序正好是倒序，所以这就是「倒着读」。\n\n"
        "★ **大小写敏感**：`Aba` 不是回文（`A` 与 `a` 是不同的字符）。"
    ),
    input_format="一行，一个不含空格的字符串。",
    output_format="一行，`yes` 或 `no`。",
    constraints_md="- 串长不超过 10000",
    inputs=["abcba\n", "abba\n", "abc\n", "a\n", "ab\n", "Aba\n", "12321\n"],
    samples=3,

    oracle=_oracle_14,

    solution=r'''#include <stdio.h>
#include <string.h>
char s[10005], st[10005];
int main(void) {
    scanf("%s", s);
    int n = (int)strlen(s), top = 0;
    for (int i = 0; i < n; i++) st[top++] = s[i];
    int ok = 1;
    for (int i = 0; i < n; i++) if (st[--top] != s[i]) { ok = 0; break; }
    printf(ok ? "yes\n" : "no\n");
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <string>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s; cin >> s;
    // 另一套：双指针从两头往中间夹，不用栈
    int i = 0, j = (int)s.size() - 1;
    bool ok = true;
    while (i < j) { if (s[i] != s[j]) { ok = false; break; } i++; j--; }
    cout << (ok ? "yes" : "no") << "\n";
    return 0;
}
''',
)

def _oracle_15(text: str) -> str:
    n = int(text.split()[0])
    moves: list[str] = []

    def hanoi(k: int, f: str, v: str, t: str) -> None:
        if k == 0:
            return
        hanoi(k - 1, f, t, v)
        moves.append("%s->%s" % (f, t))
        hanoi(k - 1, v, f, t)

    hanoi(n, "A", "B", "C")
    return "%d\n" % (2 ** n - 1) + "".join(m + "\n" for m in moves)

add(
    title="汉诺塔的移动序列",
    section="第 03 讲 · 栈和队列",
    difficulty=3, score=20, tags=["递归", "汉诺塔", "栈"],
    statement_md=(
        "`n` 个盘子在 `A` 柱上，要全部移到 `C` 柱，`B` 柱当辅助。"
        "每次只能移动一个盘，且大盘不能压在小盘上。\n\n"
        "递归三步（`n` 个盘从 `from` 经 `via` 到 `to`）：\n\n"
        "```c\n"
        "Hanoi(n-1, from, to, via);   /* 上面 n-1 个先挪到辅助柱 */\n"
        "move(n, from, to);           /* 最大的那个直接到位 */\n"
        "Hanoi(n-1, via, from, to);   /* 再从那根辅助柱挪到目标 */\n"
        "```\n\n"
        "最少步数是 `2ⁿ - 1` —— 这是递归式 `T(n) = 2T(n-1) + 1` 的解。\n\n"
        "**递归和栈的关系**：整个递归过程完全可以用一个显式栈模拟出来，"
        "`n = 64` 时调用的深度也才 64 层，这就是「递归之所以能用栈实现」的直观例子。"
    ),
    input_format="一行，一个整数 `n`。",
    output_format=(
        "第一行一个整数，最少移动步数 `2ⁿ - 1`。\n\n"
        "随后每行一步，格式为 `X->Y`（`X`、`Y` 为 `A`/`B`/`C`）。"
    ),
    constraints_md="- 1 ≤ n ≤ 12",
    inputs=["1\n", "2\n", "3\n", "4\n", "5\n"],
    samples=3,

    oracle=_oracle_15,

    solution=r'''#include <stdio.h>
static void hanoi(int n, char from, char via, char to) {
    if (n == 0) return;
    hanoi(n - 1, from, to, via);
    printf("%c->%c\n", from, to);
    hanoi(n - 1, via, from, to);
}
int main(void) {
    int n;
    scanf("%d", &n);
    printf("%d\n", (1 << n) - 1);
    hanoi(n, 'A', 'B', 'C');
    return 0;
}
''',
    alt=r'''#include <iostream>
using namespace std;
// 另一套：**不用递归**，用一个显式栈模拟调用过程
struct Frame { int n; char from, via, to; int stage; };
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n; cin >> n;
    cout << ((1 << n) - 1) << "\n";
    Frame st[64];
    int top = 0;
    st[top++] = Frame{n, 'A', 'B', 'C', 0};
    while (top > 0) {
        Frame &f = st[top - 1];
        if (f.n == 0) { top--; continue; }
        if (f.stage == 0) {
            f.stage = 1;
            st[top++] = Frame{f.n - 1, f.from, f.to, f.via, 0};
        } else if (f.stage == 1) {
            f.stage = 2;
            cout << f.from << "->" << f.to << "\n";
            st[top++] = Frame{f.n - 1, f.via, f.from, f.to, 0};
        } else {
            top--;
        }
    }
    return 0;
}
''',
)

def _oracle_16(text: str) -> str:
    d = text.split()
    n, k = int(d[0]), int(d[1])
    q = list(range(1, n + 1))
    out: list[int] = []
    i = 0
    while q:
        i = (i + k - 1) % len(q)       # 从当前位置数 k 个
        out.append(q.pop(i))
    return " ".join(map(str, out)) + "\n"

add(
    title="约瑟夫环的出列顺序",
    section="第 03 讲 · 栈和队列",
    difficulty=3, score=20, tags=["队列", "约瑟夫环", "模拟"],
    statement_md=(
        "`n` 个人围成一圈，编号 `1` 到 `n`。从 1 号开始报数，"
        "报到 `k` 的人出列，然后**从他的下一个人重新从 1 报数**，直到所有人出列。\n\n"
        "用队列模拟最直观：\n\n"
        "```c\n"
        "for (报数到 k-1 的人) { 出队 → 再从队尾入队; }   /* 报 1..k-1 的跳过 */\n"
        "第 k 个：出队 → 直接输出（不再入队）\n"
        "```\n\n"
        "★ 队列判空有两种写法：`front == rear`（不带头结点、不牺牲单元）"
        "和「牺牲一个单元」的循环队列写法。**同一个程序里不能混用**，"
        "混了就会出现「少输出一个」或「多输出一个」的静默错误。"
    ),
    input_format="一行，两个整数 `n` 和 `k`。",
    output_format="一行，`n` 个整数，按出列先后排列，空格分隔。",
    constraints_md="- 1 ≤ n ≤ 1000\n- 1 ≤ k ≤ 1000",
    inputs=["5 2\n", "7 3\n", "1 1\n", "6 6\n", "10 4\n", "2 3\n"],
    samples=3,

    oracle=_oracle_16,

    solution=r'''#include <stdio.h>
#define CAP 1005
int q[CAP];
int main(void) {
    int n, k;
    scanf("%d %d", &n, &k);
    for (int i = 0; i < n; i++) q[i] = i + 1;
    int front = 0, rear = n, cnt = n;
    while (cnt > 0) {
        for (int c = 1; c < k; c++) {          /* 报 1..k-1 的：出队再从队尾入队 */
            q[rear] = q[front];
            rear = (rear + 1) % CAP;
            front = (front + 1) % CAP;
        }
        int v = q[front];                      /* 报 k 的：出队直接输出 */
        front = (front + 1) % CAP;
        cnt--;
        printf("%d%c", v, cnt == 0 ? '\n' : ' ');
    }
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k; cin >> n >> k;
    // 另一套：**不模拟报数**，直接算下一个出列者的下标（数学做法）
    vector<int> alive;
    for (int i = 1; i <= n; i++) alive.push_back(i);
    size_t pos = 0;
    for (int left = n; left > 0; left--) {
        pos = (pos + (size_t)k - 1) % alive.size();
        cout << alive[pos] << (left == 1 ? '\n' : ' ');
        alive.erase(alive.begin() + (long)pos);
    }
    return 0;
}
''',
)


# --------------------------------------------------------------------- #
#  第 04 讲 · 串、数组和广义表
# --------------------------------------------------------------------- #

def _oracle_17(text: str) -> str:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    s, t = lines[0], lines[1]
    pos = s.find(t)
    return "%d\n" % (pos + 1 if pos >= 0 else 0)

add(
    title="BF 模式匹配求首次位置",
    section="第 04 讲 · 串、数组和广义表",
    difficulty=2, score=15, tags=["串", "BF算法", "模式匹配"],
    statement_md=(
        "朴素模式匹配（BF，Brute Force）：在主串 `S` 中找模式串 `T` "
        "**第一次**出现的位置。\n\n"
        "找不到输出 `0`。**位置从 1 开始数**（教材口径）。\n\n"
        "★ BF 的写法里最容易错的是**失配后的回退**：\n\n"
        "```c\n"
        "i = i - j + 2;   /* 主串回到本轮起点的下一个字符 */\n"
        "j = 1;           /* 模式串从头来 */\n"
        "```\n\n"
        "写成 `i = i - j + 1` 的话，失配时会原地打转 → **死循环**。"
    ),
    input_format="第一行主串 `S`（不含空格）。\n\n第二行模式串 `T`（不含空格，非空）。",
    output_format="一行，`T` 在 `S` 中首次出现的起始位置（1 起）；不存在输出 `0`。",
    constraints_md="- 1 ≤ |S|, |T| ≤ 10000",
    inputs=[
        "abcabc\nbc\n",
        "aaaa\naa\n",
        "abc\nd\n",
        "a\na\n",
        "ababab\nabab\n",
        "abcde\ncde\n",
        "abcdef\nf\n",
    ],
    samples=3,

    oracle=_oracle_17,

    solution=r'''#include <stdio.h>
#include <string.h>
char s[10005], t[10005];
int main(void) {
    scanf("%s %s", s, t);
    int n = (int)strlen(s), m = (int)strlen(t);
    int i = 0, j = 0;
    while (i < n && j < m) {
        if (s[i] == t[j]) { i++; j++; }
        else { i = i - j + 1; j = 0; }   /* ★ 回退到本轮起点的下一个 */
    }
    printf("%d\n", j == m ? i - m + 1 : 0);
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <string>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s, t;
    cin >> s >> t;
    // 另一套：直接用标准库的 find（KMP 实现），结果与 BF 一致
    size_t p = s.find(t);
    cout << (p == string::npos ? 0 : (int)p + 1) << "\n";
    return 0;
}
''',
)

def _oracle_18(text: str) -> str:
    """★ 按**定义**暴力算（枚举所有前后缀），不是照抄递推算法 —— 两条路才叫真独立。"""
    p = text.strip()
    m = len(p)
    nxt = [0] * (m + 1)          # 1-based
    nxt[1] = 0
    for j in range(2, m + 1):
        seg = p[:j - 1]          # p[1..j-1]
        best = 0
        for L in range(1, len(seg)):          # L 是前后缀长度（必须真短于 seg）
            if seg[:L] == seg[-L:]:
                best = L
        nxt[j] = best + 1
    return " ".join(str(nxt[j]) for j in range(1, m + 1)) + "\n"

add(
    title="求模式串的 next 数组",
    section="第 04 讲 · 串、数组和广义表",
    difficulty=4, score=25, tags=["串", "KMP", "next数组"],
    statement_md=(
        "求模式串的 `next` 数组。这里用的是**教材（严蔚敏）的经典定义**，"
        "下标从 1 开始：\n\n"
        "- `next[1] = 0`\n"
        "- `next[j]` = 「`p[1..j-1]` 的**最长相等前后缀**长度」`+ 1`（长度可以为 0）\n\n"
        "拿 `abaabc` 手算一遍就懂了：\n\n"
        "| j | p[1..j-1] | 最长相等前后缀 | next[j] |\n"
        "|---|---|---|---|\n"
        "| 1 | — | — | 0 |\n"
        "| 2 | `a` | 无 | 1 |\n"
        "| 3 | `ab` | 无 | 1 |\n"
        "| 4 | `aba` | `a` | 2 |\n"
        "| 5 | `abaa` | `a` | 2 |\n"
        "| 6 | `abaab` | `ab` | 3 |\n\n"
        "★ 别和 `nextval`（优化后的数组）搞混 —— 那是两道题。"
        "本机实测过：`nextval` 并不是万能优化，某些串上反而会多比较几次。"
    ),
    input_format="一行，模式串（不含空格）。",
    output_format="一行，`m` 个整数，用空格分隔，依次是 `next[1]` 到 `next[m]`。",
    constraints_md="- 1 ≤ m ≤ 1000",
    inputs=["abaabc\n", "aaaa\n", "ababaa\n", "a\n", "abcabx\n", "aaab\n", "abcabcaa\n"],
    samples=2,

    oracle=_oracle_18,

    solution=r'''#include <stdio.h>
#include <string.h>
char p[1005];
int nxt[1005];
int main(void) {
    scanf("%s", p + 1);                 /* 从下标 1 开始存，与教材一致 */
    int m = (int)strlen(p + 1);
    nxt[1] = 0;
    int i = 1, j = 0;
    while (i < m) {
        if (j == 0 || p[i] == p[j]) { i++; j++; nxt[i] = j; }
        else j = nxt[j];
    }
    for (int k = 1; k <= m; k++) printf("%d%c", nxt[k], k == m ? '\n' : ' ');
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <string>
#include <vector>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string p; cin >> p;
    int m = (int)p.size();
    // 另一套：对每个 j 直接**暴力枚举**候选长度（O(m^3)，m 小就够用）
    vector<int> nxt(m + 1, 0);
    nxt[1] = 0;
    for (int j = 2; j <= m; j++) {
        int best = 0;
        for (int L = 1; L < j - 1; L++) {
            bool same = true;
            for (int k = 0; k < L; k++)
                if (p[k] != p[j - 1 - L + k]) { same = false; break; }
            if (same) best = L;
        }
        nxt[j] = best + 1;
    }
    for (int k = 1; k <= m; k++) cout << nxt[k] << (k == m ? '\n' : ' ');
    return 0;
}
''',
)

def _oracle_19(text: str) -> str:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    s, t = lines[0], lines[1]
    cnt, pos = 0, 0
    while True:
        k = s.find(t, pos)
        if k < 0:
            break
        cnt += 1
        pos = k + len(t)          # ★ 不重叠：跳到本次匹配之后
    return "%d\n" % cnt

add(
    title="KMP 统计不重叠出现次数",
    section="第 04 讲 · 串、数组和广义表",
    difficulty=4, score=25, tags=["串", "KMP", "计数"],
    statement_md=(
        "统计模式串 `T` 在主串 `S` 中出现了多少次，**两次出现不允许重叠**"
        "（匹配成功后从下一个位置继续找）。\n\n"
        "KMP 的核心好处是**主串指针 `i` 永不回退**，串越长优势越明显："
        "本机实测同一个任务 BF 比较 91001 次、KMP 只要 1901 次。\n\n"
        "★ 但 KMP 也**不是总更快**：本机实测过 `\"ab\"×400` 去匹配 `aaab`，"
        "BF 比较 1200 次、KMP 反而 1600 次 —— 因为模式串里根本没有"
        "值得跳过的前后缀。别把「KMP 一定更快」当定理记。"
    ),
    input_format="第一行主串 `S`（不含空格）。\n\n第二行模式串 `T`（不含空格，非空）。",
    output_format="一行，一个整数，不重叠出现的次数。",
    constraints_md="- 1 ≤ |S|, |T| ≤ 10000",
    inputs=[
        "aaaaa\naa\n",
        "abcabcabc\nabc\n",
        "abababa\naba\n",
        "abc\nd\n",
        "aaa\naaaa\n",
        "aabaaab\naab\n",
        "abcabxabcd\nabc\n",
    ],
    samples=3,

    oracle=_oracle_19,

    solution=r'''#include <stdio.h>
#include <string.h>
char s[10005], t[10005];
int nxt[10005];
int main(void) {
    scanf("%s %s", s, t);
    int n = (int)strlen(s), m = (int)strlen(t);
    /* ---- 建 next（0-based 存法：nxt[k] = 前 k 个字符的最长相等前后缀长度）---- */
    nxt[0] = -1;
    int i = 0, j = -1;
    while (i < m) {
        if (j == -1 || t[i] == t[j]) { i++; j++; nxt[i] = j; }
        else j = nxt[j];
    }
    /* ---- 匹配：主串指针 i 永不回退 ---- */
    int cnt = 0;
    i = 0; j = 0;
    while (i < n) {
        if (j == -1 || s[i] == t[j]) { i++; j++; }
        else j = nxt[j];
        if (j == m) {                  /* 命中一次 */
            cnt++;
            i = i - m + m;             /* 不重叠：主串指针停在本次匹配之后 */
            j = 0;                     /* 模式串从头开始 */
        }
    }
    printf("%d\n", cnt);
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <string>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s, t;
    cin >> s >> t;
    // 另一套：反复调用标准库 find（内部是 KMP/BM 之类的高效实现）
    int cnt = 0;
    size_t pos = 0;
    while (true) {
        size_t k = s.find(t, pos);
        if (k == string::npos) break;
        cnt++;
        pos = k + t.size();
    }
    cout << cnt << "\n";
    return 0;
}
''',
)

def _oracle_20(text: str) -> str:
    d = text.split()
    r, c, t = int(d[0]), int(d[1]), int(d[2])
    trip = []
    p = 3
    for _ in range(t):
        rr, cc, vv = int(d[p]), int(d[p + 1]), int(d[p + 2])
        p += 3
        trip.append((rr, cc, vv))
    # 转置 = 每个元素行列对调，再按 (行, 列) 排序
    out = sorted(((cc, rr, vv) for (rr, cc, vv) in trip), key=lambda x: (x[0], x[1]))
    lines = ["%d %d %d" % (c, r, t)]
    lines += ["%d %d %d" % e for e in out]
    return "\n".join(lines) + "\n"

add(
    title="稀疏矩阵三元组快速转置",
    section="第 04 讲 · 串、数组和广义表",
    difficulty=4, score=25, tags=["数组", "稀疏矩阵", "快速转置"],
    statement_md=(
        "把稀疏矩阵的三元组顺序表**转置**：把每个元素的「行、列」对调，"
        "并且结果仍然是**行优先**排列的三元组表。\n\n"
        "朴素做法要扫两遍（对每一列都从头扫一遍全表），复杂度 `O(n·t)`。\n"
        "**快速转置**只扫一遍，靠两张辅助表：\n\n"
        "- `num[col]` —— 原矩阵第 `col` 列有几个非零元\n"
        "- `cpot[col]` —— 该列的第一个非零元在转置结果里应该放的**起始位置**\n\n"
        "```c\n"
        "cpot[1] = 1;\n"
        "cpot[col] = cpot[col-1] + num[col-1];   /* 前缀和 */\n"
        "```\n\n"
        "★ 最隐蔽的错误是**忘了 `cpot[col]++`** —— 同一列有多个元素时它们会挤在"
        "同一个位置，后写的把先写的**静默覆盖**掉，输出少几行、一个报错都没有。"
    ),
    input_format=(
        "第一行三个整数 `r` `c` `t`：原矩阵行数、列数、非零元个数。\n\n"
        "随后 `t` 行，每行三个整数 `row col value`（行列下标从 **1** 开始，"
        "按**行优先**顺序给出，`value` 非零）。"
    ),
    output_format=(
        "第一行三个整数 `c` `r` `t`：转置后矩阵的列数、行数、非零元个数。\n\n"
        "随后 `t` 行，每行 `row col value`，按**行优先**排列。"
    ),
    constraints_md="- 1 ≤ r, c ≤ 1000\n- 0 ≤ t ≤ 1000",
    inputs=[
        "3 4 3\n1 1 5\n2 3 7\n3 2 9\n",
        "3 3 4\n1 1 1\n1 3 2\n2 2 3\n3 1 4\n",
        "2 2 0\n",
        "1 5 2\n1 2 8\n1 4 6\n",
        "4 1 2\n2 1 3\n4 1 7\n",
        "3 3 1\n2 2 9\n",
    ],
    samples=2,

    oracle=_oracle_20,

    solution=r'''#include <stdio.h>
int ar[1005], ac[1005], av[1005];
int br[1005], bc[1005], bv[1005];
int num[1005], cpot[1005];
int main(void) {
    int r, c, t;
    scanf("%d %d %d", &r, &c, &t);
    for (int k = 0; k < t; k++) scanf("%d %d %d", &ar[k], &ac[k], &av[k]);
    for (int col = 1; col <= c; col++) num[col] = 0;
    for (int k = 0; k < t; k++) num[ac[k]]++;        /* 统计每列的非零元个数 */
    cpot[1] = 0;                                     /* 0-based 存法 */
    for (int col = 2; col <= c; col++) cpot[col] = cpot[col - 1] + num[col - 1];
    for (int k = 0; k < t; k++) {
        int col = ac[k];
        int pos = cpot[col];
        br[pos] = ac[k]; bc[pos] = ar[k]; bv[pos] = av[k];
        cpot[col]++;                                 /* ★ 忘了这句就会静默覆盖 */
    }
    printf("%d %d %d\n", c, r, t);
    for (int k = 0; k < t; k++) printf("%d %d %d\n", br[k], bc[k], bv[k]);
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
struct Trip { int r, c, v; };
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int r, c, t; cin >> r >> c >> t;
    vector<Trip> a(t);
    for (auto &e : a) cin >> e.r >> e.c >> e.v;
    // 另一套：不建 num/cpot，直接对调后整体排序（朴素但结果等价）
    vector<Trip> b(t);
    for (int k = 0; k < t; k++) b[k] = Trip{a[k].c, a[k].r, a[k].v};
    stable_sort(b.begin(), b.end(), [](const Trip &x, const Trip &y) {
        if (x.r != y.r) return x.r < y.r;
        return x.c < y.c;
    });
    cout << c << " " << r << " " << t << "\n";
    for (const auto &e : b) cout << e.r << " " << e.c << " " << e.v << "\n";
    return 0;
}
''',
)

def _oracle_21(text: str) -> str:
    d = text.split()
    n = int(d[0])
    q = int(d[1])
    p = 2
    out = []
    for _ in range(q):
        i, j = int(d[p]), int(d[p + 1])
        p += 2
        out.append(i * (i - 1) // 2 + j if i >= j else j * (j - 1) // 2 + i)
    return "\n".join(map(str, out)) + "\n"

add(
    title="对称矩阵压缩存储的下标计算",
    section="第 04 讲 · 串、数组和广义表",
    difficulty=3, score=20, tags=["数组", "对称矩阵", "压缩存储", "下标计算"],
    statement_md=(
        "`n` 阶**对称矩阵** `A`，满足 `A[i][j] = A[j][i]`，"
        "只需要存**下三角（含对角线）**，共 `n(n+1)/2` 个元素，"
        "按**行优先**塞进一维数组 `sa`。\n\n"
        "已知 `i`、`j`（都从 1 开始），求对应的一维下标 `k`（也从 1 开始）：\n\n"
        "```c\n"
        "if (i >= j) k = i * (i - 1) / 2 + j;   /* 在下三角，直接算 */\n"
        "else        k = j * (j - 1) / 2 + i;   /* 在上三角，用对称性换成 A[j][i] */\n"
        "```\n\n"
        "★ 理解的关键是 `i(i-1)/2` 这一项：它是**前面 `i-1` 行元素的总个数**"
        "（第 1 行 1 个、第 2 行 2 个……累加起来就是 `1+2+…+(i-1)`）。\n\n"
        "注意 `i` 和 `j` 谁大谁小：写反了不会报错，只会静默算出一个错的 `k`。"
    ),
    input_format=(
        "第一行一个整数 `n`。\n\n"
        "第二行一个整数 `q`（查询个数）。\n\n"
        "随后 `q` 行，每行两个整数 `i` `j`（1 ≤ i, j ≤ n）。"
    ),
    output_format="`q` 行，每行一个整数，表示对应的一维下标 `k`。",
    constraints_md="- 1 ≤ n ≤ 1000\n- 1 ≤ q ≤ 1000",
    inputs=[
        "4\n6\n3 2\n2 3\n1 1\n4 4\n1 4\n2 2\n",
        "1\n1\n1 1\n",
        "5\n4\n5 5\n5 1\n1 5\n3 4\n",
        "3\n3\n1 2\n2 1\n3 3\n",
    ],
    samples=2,

    oracle=_oracle_21,

    solution=r'''#include <stdio.h>
int main(void) {
    int n, q;
    scanf("%d %d", &n, &q);
    for (int k = 0; k < q; k++) {
        int i, j;
        scanf("%d %d", &i, &j);
        int idx = (i >= j) ? (i * (i - 1) / 2 + j) : (j * (j - 1) / 2 + i);
        printf("%d\n", idx);
    }
    return 0;
}
''',
    alt=r'''#include <iostream>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q; cin >> n >> q;
    while (q--) {
        int i, j; cin >> i >> j;
        // 另一套：先按对称性把下标换成「大行小列」，再老实累加前面几行的个数
        int a = (i > j) ? i : j;
        int b = (i < j) ? i : j;
        int base = 0;
        for (int row = 1; row < a; row++) base += row;
        cout << base + b << "\n";
    }
    return 0;
}
''',
)

def _oracle_22(text: str) -> str:
    """★ 按定义递归解析（与「数括号层数」是两条独立的路）。"""
    s = text.strip()

    def parse(pos: int) -> tuple[int, int]:
        """返回 (深度, 下一个字符的位置)。pos 指向 '(' 或原子。"""
        if s[pos] != "(":
            return 0, pos + 1
        pos += 1
        inner = 0
        if s[pos] == ")":                 # 空表
            return 1, pos + 1
        while True:
            d, pos = parse(pos)
            inner = max(inner, d)
            if pos < len(s) and s[pos] == ",":
                pos += 1
                continue
            break
        return 1 + inner, pos + 1      # 跳过 ')'

    return "%d\n" % parse(0)[0]

add(
    title="求广义表的深度",
    section="第 04 讲 · 串、数组和广义表",
    difficulty=4, score=25, tags=["广义表", "深度", "递归"],
    statement_md=(
        "求广义表的**深度**。教材口径：\n\n"
        "- **原子**（单个元素）的深度是 `0`\n"
        "- **空表** `()` 的深度是 `1`\n"
        "- 表的深度 = `1 + 各元素的深度的最大值`\n\n"
        "举例：\n\n"
        "| 广义表 | 深度 | 理由 |\n"
        "|---|---|---|\n"
        "| `a` | 0 | 原子 |\n"
        "| `()` | 1 | 空表 |\n"
        "| `(a)` | 1 | 1 + max(0) |\n"
        "| `(a,b)` | 1 | 1 + max(0,0) |\n"
        "| `((a))` | 2 | 1 + (1 + 0) |\n"
        "| `(a,(b,c))` | 2 | 1 + max(0, 1) |\n\n"
        "★ 换算成一个**等价判据**：广义表的深度正好等于**括号的最大嵌套层数**。"
        "`(())` 嵌套 2 层、深度 2；`()` 嵌套 1 层、深度 1 —— 因为空表算 1 层。"
        "内部用递归解析也行，但两条路都得走通才算真懂。"
    ),
    input_format="一行，一个合法的广义表（元素为单个字母，表用逗号分隔、用括号括起）。",
    output_format="一行，一个整数，广义表的深度。",
    constraints_md="- 长度不超过 1000\n- 嵌套层数不超过 100",
    inputs=[
        "a\n",
        "()\n",
        "(a)\n",
        "(a,b)\n",
        "((a))\n",
        "(a,(b,c))\n",
        "((),())\n",
        "((a),(b,((c))))\n",
    ],
    samples=4,

    oracle=_oracle_22,

    solution=r'''#include <stdio.h>
#include <string.h>
char s[1005];
int pos;
static int parse(void) {
    if (s[pos] != '(') { pos++; return 0; }      /* 原子：深度 0 */
    pos++;                                       /* 跳过 '(' */
    if (s[pos] == ')') { pos++; return 1; }      /* 空表：深度 1 */
    int inner = 0;
    while (1) {
        int d = parse();
        if (d > inner) inner = d;
        if (s[pos] == ',') { pos++; continue; }
        break;
    }
    pos++;                                       /* 跳过 ')' */
    return 1 + inner;
}
int main(void) {
    scanf("%s", s);
    pos = 0;
    printf("%d\n", parse());
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <string>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s; cin >> s;
    // 另一套：**完全不解析**，只数括号的最大嵌套层数
    int d = 0, mx = 0;
    for (char ch : s) {
        if (ch == '(') { d++; if (d > mx) mx = d; }
        else if (ch == ')') d--;
    }
    cout << mx << "\n";
    return 0;
}
''',
)

def _oracle_23(text: str) -> str:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    s, t = lines[0], lines[1]
    while t in s:
        s = s.replace(t, "")        # 反复删，直到不再出现
    return (s if s else "empty") + "\n"

add(
    title="反复删除所有指定子串",
    section="第 04 讲 · 串、数组和广义表",
    difficulty=3, score=20, tags=["串", "删除子串", "循环处理"],
    statement_md=(
        "从主串 `S` 中删除**所有**出现的子串 `T`。\n\n"
        "★ 注意是**反复删**：删完之后如果又拼出了新的 `T`，还要接着删，"
        "一直删到不再出现为止。\n\n"
        "例如 `S = aabbcc`、`T = ab`：\n"
        "第一次删掉中间的 `ab` 得到 `abcc`（这里又出现了一个 `ab`）→ "
        "删掉得到 `cc` → 结束。\n\n"
        "删空则输出 `empty`。"
    ),
    input_format="第一行主串 `S`（不含空格）。\n\n第二行子串 `T`（不含空格，非空）。",
    output_format="一行，删除后的字符串；若为空输出 `empty`。",
    constraints_md="- 1 ≤ |S|, |T| ≤ 1000",
    inputs=[
        "aaa\naa\n",
        "aabbaabb\naabb\n",
        "abcabc\nabc\n",
        "hello\nl\n",
        "abcabc\nxyz\n",
        "ababab\nab\n",
        "aabbcc\nab\n",
    ],
    samples=3,

    oracle=_oracle_23,

    solution=r'''#include <stdio.h>
#include <string.h>
char s[1005], t[1005];
int main(void) {
    scanf("%s %s", s, t);
    int m = (int)strlen(t);
    int changed = 1;
    while (changed) {
        changed = 0;
        char *p;
        while ((p = strstr(s, t)) != NULL) {          /* strstr 返回首次出现的指针 */
            changed = 1;
            /* 把 p+m 起的部分（含结尾 '\0'）搬到 p 处 */
            memmove(p, p + m, strlen(p + m) + 1);
        }
    }
    printf("%s\n", s[0] ? s : "empty");
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <string>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s, t;
    cin >> s >> t;
    // 另一套：手写扫描 —— 用一个「结果串 + 待处理位置」的循环
    string out;
    size_t i = 0;
    while (i < s.size()) {
        if (i + t.size() <= s.size() && s.compare(i, t.size(), t) == 0) { i += t.size(); }
        else {
            out += s[i++];
            // 新加进来的字符可能和 out 的尾巴拼出 t → 回头检查一次
            while (out.size() >= t.size() &&
                   out.compare(out.size() - t.size(), t.size(), t) == 0)
                out.erase(out.size() - t.size());
        }
    }
    cout << (out.empty() ? "empty" : out) << "\n";
    return 0;
}
''',
)


# --------------------------------------------------------------------- #
#  第 05 讲 · 树和二叉树
# --------------------------------------------------------------------- #
#  约定：二叉树用**带空标记的前序序列**给出，结点是大写字母，`#` 表示空。
#  例：`AB#D##C##` 表示  A(B(∅, D), C)
# --------------------------------------------------------------------- #

def _oracle_24(text: str) -> str:
    s = text.strip()

    def rec(i: int):
        if i >= len(s) or s[i] == "#":
            return None, i + 1          # ★ 空也要吃掉一个位置
        v = s[i]
        left, i = rec(i + 1)
        right, i = rec(i)
        return (v, left, right), i

    root, _ = rec(0)
    out: list[str] = []

    def inorder(n) -> None:
        if n is None:
            return
        inorder(n[1])
        out.append(n[0])
        inorder(n[2])

    inorder(root)
    return ("".join(out) if out else "empty") + "\n"

add(
    title="前序建二叉树并输出中序",
    section="第 05 讲 · 树和二叉树",
    difficulty=3, score=20, tags=["二叉树", "前序建树", "中序遍历"],
    statement_md=(
        "按**带空标记的前序序列**建立二叉树（`#` 表示空子树），然后输出**中序**遍历。\n\n"
        "例如 `AB#D##C##`：\n\n"
        "```text\n"
        "        A\n"
        "       / \\\n"
        "      B   C\n"
        "       \\\n"
        "        D\n"
        "```\n\n"
        "中序（左-根-右）得到 `BDAC`。\n\n"
        "★ 建树时最容易踩的坑：递归里**每个 `#` 也要吃掉一个字符位置**"
        "（`i` 必须往后走），否则整棵树会错位 —— 而且错得很隐蔽，"
        "本机实测过：漏了它重建出来的是一棵**看起来很像、其实完全不同**的树。"
    ),
    input_format="一行，带空标记的前序序列（结点为大写字母，`#` 表示空）。",
    output_format="一行，中序遍历的结点序列（无分隔符）；空树输出 `empty`。",
    constraints_md="- 序列长度不超过 2000",
    inputs=["AB#D##C##\n", "A##\n", "AB##C##\n", "#\n", "ABC####\n", "ABD##E##C#F##\n"],
    samples=3,

    oracle=_oracle_24,

    solution=r'''#include <stdio.h>
#include <string.h>
#include <stdlib.h>
typedef struct BTNode { char data; struct BTNode *l, *r; } BTNode;
char s[2005];
int pos;
static BTNode *build(void) {
    char c = s[pos++];                      /* ★ 空标记也要吃掉一个位置 */
    if (c == '#' || c == '\0') return NULL;
    BTNode *t = (BTNode *)malloc(sizeof(BTNode));
    t->data = c;
    t->l = build();
    t->r = build();
    return t;
}
static int any = 0;
static void inorder(BTNode *t) {
    if (!t) return;
    inorder(t->l);
    putchar(t->data); any = 1;
    inorder(t->r);
}
int main(void) {
    scanf("%s", s);
    pos = 0;
    BTNode *root = build();
    inorder(root);
    if (!any) printf("empty");
    putchar('\n');
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <string>
#include <vector>
#include <functional>
using namespace std;
struct Node { char c; int l, r; };
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s; cin >> s;
    // 另一套：结点存 vector（下标代替指针），中序用**显式栈**迭代做（不写递归）
    vector<Node> pool;
    int pos = 0;
    function<int()> build = [&]() -> int {
        char c = s[pos++];
        if (c == '#' || pos > (int)s.size()) return -1;
        int id = (int)pool.size();
        pool.push_back(Node{c, -1, -1});
        int l = build(), r = build();
        pool[id].l = l; pool[id].r = r;
        return id;
    };
    int root = build();
    string out;
    // 迭代中序：一路向左压栈，弹出即访问，再转向右
    vector<int> st;
    int cur = root;
    while (cur != -1 || !st.empty()) {
        while (cur != -1) { st.push_back(cur); cur = pool[cur].l; }
        cur = st.back(); st.pop_back();
        out += pool[cur].c;
        cur = pool[cur].r;
    }
    cout << (out.empty() ? "empty" : out) << "\n";
    return 0;
}
''',
)

def _oracle_25(text: str) -> str:
    s = text.strip()

    def rec(i: int):
        if i >= len(s) or s[i] == "#":
            return 0, i + 1
        dl, i = rec(i + 1)
        dr, i = rec(i)
        return 1 + max(dl, dr), i

    return "%d\n" % rec(0)[0]

add(
    title="求二叉树的深度",
    section="第 05 讲 · 树和二叉树",
    difficulty=2, score=15, tags=["二叉树", "深度", "递归"],
    statement_md=(
        "求二叉树的**深度**（根到最远叶子的结点层数，只有根时深度为 1，空树为 0）。\n\n"
        "递归式：`depth(t) = 1 + max(depth(左), depth(右))`，空树返回 0。\n\n"
        "★ **空树的深度是 0，不是 1** —— 这一点只在输入就是 `#` 的时候才会暴露。"
        "本机实测过：把这个基准情况写成 1，所有非空树的答案照样正确，"
        "只有空树悄悄多出 1，非常容易漏测。"
    ),
    input_format="一行，带空标记的前序序列。",
    output_format="一行，一个整数，树的深度。",
    constraints_md="- 序列长度不超过 2000",
    inputs=["AB#D##C##\n", "A##\n", "#\n", "ABC####\n", "A#B#C#D###\n", "ABD##E##C#F##\n"],
    samples=3,

    oracle=_oracle_25,

    solution=r'''#include <stdio.h>
#include <string.h>
char s[2005];
int pos, any = 0;
static int depth(void) {
    char c = s[pos++];
    if (c == '#' || c == '\0') return 0;     /* ★ 空树深度 0 */
    int dl = depth(), dr = depth();
    any = 1;
    return 1 + (dl > dr ? dl : dr);
}
int main(void) {
    scanf("%s", s);
    pos = 0;
    printf("%d\n", depth());
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <string>
#include <vector>
#include <functional>
using namespace std;
struct Node { char c; int l, r; };
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s; cin >> s;
    // 另一套：结点存 vector，深度用「反复收敛」算 —— 不写递归求深度
    vector<Node> pool;
    int pos = 0;
    function<int()> build = [&]() -> int {
        char c = s[pos++];
        if (c == '#' || pos > (int)s.size()) return -1;
        int id = (int)pool.size();
        pool.push_back(Node{c, -1, -1});
        int l = build(), r = build();
        pool[id].l = l; pool[id].r = r;
        return id;
    };
    int root = build();
    if (root < 0) { cout << 0 << "\n"; return 0; }
    // 父结点的编号恒小于孩子（先创建父），所以**倒着扫一遍**就够了
    vector<int> h(pool.size(), 0);
    for (int i = (int)pool.size() - 1; i >= 0; i--) {
        int a = (pool[i].l < 0) ? 0 : h[pool[i].l];
        int b = (pool[i].r < 0) ? 0 : h[pool[i].r];
        h[i] = 1 + (a > b ? a : b);
    }
    cout << h[root] << "\n";
    return 0;
}
''',
)

def _oracle_26(text: str) -> str:
    s = text.strip()

    def rec(i: int):
        if i >= len(s) or s[i] == "#":
            return (0, 0), i + 1
        (nl, ll), i = rec(i + 1)
        (nr, lr), i = rec(i)
        leaves = (ll + lr) if (nl + nr) else 1     # 左右都空 → 自己是叶子
        return (1 + nl + nr, leaves), i

    (n, leaf), _ = rec(0)
    return "%d %d\n" % (n, leaf)

add(
    title="统计二叉树的结点数与叶子数",
    section="第 05 讲 · 树和二叉树",
    difficulty=2, score=15, tags=["二叉树", "结点数", "叶子"],
    statement_md=(
        "统计二叉树的**结点总数**和**叶子结点数**。\n\n"
        "叶子 = 左、右孩子都为空的结点。\n\n"
        "★ 别忘了空树：空树的结点数和叶子数**都是 0**，"
        "而且 0 个结点的树也没有叶子 —— 这两句话看着像废话，"
        "但写成代码时把「根为空」的基准情况漏掉，空输入就会崩。"
    ),
    input_format="一行，带空标记的前序序列。",
    output_format="一行，两个整数，用空格分隔：结点总数 叶子数。",
    constraints_md="- 序列长度不超过 2000",
    inputs=["AB#D##C##\n", "A##\n", "#\n", "ABC####\n", "AB##C##\n", "ABD##E##C#F##\n"],
    samples=3,

    oracle=_oracle_26,

    solution=r'''#include <stdio.h>
#include <string.h>
#include <stdlib.h>
typedef struct BTNode { char data; struct BTNode *l, *r; } BTNode;
char s[2005];
int pos, total = 0, leaves = 0;
static BTNode *build(void) {
    char c = s[pos++];
    if (c == '#' || c == '\0') return NULL;
    BTNode *t = (BTNode *)malloc(sizeof(BTNode));
    t->data = c;
    t->l = build();
    t->r = build();
    return t;
}
static void count(BTNode *t) {
    if (!t) return;
    total++;
    if (!t->l && !t->r) leaves++;      /* 左右都空 → 叶子 */
    count(t->l);
    count(t->r);
}
int main(void) {
    scanf("%s", s);
    pos = 0;
    BTNode *root = build();
    count(root);
    printf("%d %d\n", total, leaves);
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <string>
#include <vector>
#include <functional>
using namespace std;
struct Node { char c; int l, r; };
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s; cin >> s;
    // 另一套：结点存进 vector（下标代替指针），统计用后序回溯一次算完
    vector<Node> pool;
    int pos = 0;
    function<int()> build = [&]() -> int {
        char c = s[pos++];
        if (c == '#' || pos > (int)s.size()) return -1;
        int id = (int)pool.size();
        pool.push_back(Node{c, -1, -1});
        int l = build(), r = build();
        pool[id].l = l; pool[id].r = r;
        return id;
    };
    int root = build();
    if (root < 0) { cout << "0 0\n"; return 0; }
    // 倒着扫 pool（父结点一定先于孩子被创建，所以逆序就是后序）
    vector<int> n(pool.size(), 0), lf(pool.size(), 0);
    for (int i = (int)pool.size() - 1; i >= 0; i--) {
        int a = (pool[i].l < 0) ? 0 : n[pool[i].l];
        int b = (pool[i].r < 0) ? 0 : n[pool[i].r];
        n[i] = 1 + a + b;
        if (a + b == 0) lf[i] = 1;
        else lf[i] = (pool[i].l < 0 ? 0 : lf[pool[i].l]) + (pool[i].r < 0 ? 0 : lf[pool[i].r]);
    }
    cout << n[root] << " " << lf[root] << "\n";
    return 0;
}
''',
)

def _oracle_27(text: str) -> str:
    s = text.strip()

    def rec(i: int):
        if i >= len(s) or s[i] == "#":
            return None, i + 1
        v = s[i]
        left, i = rec(i + 1)
        right, i = rec(i)
        return (v, left, right), i

    root, _ = rec(0)
    if root is None:
        return "empty\n"
    q = [root]
    out = []
    while q:
        n = q.pop(0)
        out.append(n[0])                 # 入队时已保证非空
        if n[1] is not None:
            q.append(n[1])
        if n[2] is not None:
            q.append(n[2])
    return "".join(out) + "\n"

add(
    title="二叉树的层次遍历",
    section="第 05 讲 · 树和二叉树",
    difficulty=3, score=20, tags=["二叉树", "层次遍历", "队列"],
    statement_md=(
        "输出二叉树的**层次遍历**序列（从上到下、从左到右，逐层输出）。\n\n"
        "层次遍历靠的是**队列**：根入队 → 出队一个就把它**非空**的左右孩子入队 → "
        "直到队空。\n\n"
        "★ 这里再次体现「队列判空」的重要性：入队时如果**把空结点也塞进去**，"
        "队就会一直非空，程序**永远停不下来**。所以要么入队前判空，"
        "要么出队后跳过空结点并额外记录「已产出几个」。"
    ),
    input_format="一行，带空标记的前序序列。",
    output_format="一行，层次遍历的结点序列（无分隔符）；空树输出 `empty`。",
    constraints_md="- 序列长度不超过 2000",
    inputs=["AB#D##C##\n", "AB##C##\n", "#\n", "A##\n", "ABC####\n", "ABD##E##C#F##\n"],
    samples=3,

    oracle=_oracle_27,

    solution=r'''#include <stdio.h>
#include <string.h>
#include <stdlib.h>
typedef struct BTNode { char data; struct BTNode *l, *r; } BTNode;
char s[2005];
int pos;
BTNode *build(void) {
    char c = s[pos++];
    if (c == '#' || c == '\0') return NULL;
    BTNode *t = (BTNode *)malloc(sizeof(BTNode));
    t->data = c;
    t->l = build();
    t->r = build();
    return t;
}
int main(void) {
    scanf("%s", s);
    pos = 0;
    BTNode *root = build();
    if (!root) { printf("empty\n"); return 0; }
    BTNode *q[2005];
    int front = 0, rear = 0;
    q[rear++] = root;
    while (front < rear) {
        BTNode *t = q[front++];
        putchar(t->data);
        if (t->l) q[rear++] = t->l;      /* ★ 只把非空的入队，否则永不终止 */
        if (t->r) q[rear++] = t->r;
    }
    putchar('\n');
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <string>
#include <vector>
#include <functional>
#include <queue>
using namespace std;
struct Node { char c; int l, r; };
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s; cin >> s;
    // 另一套：vector 池 + std::queue，并且把**空结点也入队**再跳过
    vector<Node> pool;
    int pos = 0;
    function<int()> build = [&]() -> int {
        char c = s[pos++];
        if (c == '#' || pos > (int)s.size()) return -1;
        int id = (int)pool.size();
        pool.push_back(Node{c, -1, -1});
        int l = build(), r = build();
        pool[id].l = l; pool[id].r = r;
        return id;
    };
    int root = build();
    if (root < 0) { cout << "empty\n"; return 0; }
    string out;
    queue<int> q;
    q.push(root);
    while (!q.empty()) {
        int id = q.front(); q.pop();
        if (id < 0) continue;                    // ★ 空的直接跳过
        out += pool[id].c;
        q.push(pool[id].l);                      // 空孩子也入队 —— 靠上面那句跳过
        q.push(pool[id].r);
    }
    cout << out << "\n";
    return 0;
}
''',
)

def _oracle_28(text: str) -> str:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    pre, ino = lines[0], lines[1]

    def build(p: str, i: str):
        if not p:
            return None
        root = p[0]
        k = i.index(root)
        return (root, build(p[1:1 + k], i[:k]), build(p[1 + k:], i[k + 1:]))

    t = build(pre, ino)
    out: list[str] = []

    def post(n) -> None:
        if n is None:
            return
        post(n[1]); post(n[2]); out.append(n[0])

    post(t)
    return "".join(out) + "\n"

add(
    title="由先序和中序序列求后序",
    section="第 05 讲 · 树和二叉树",
    difficulty=4, score=25, tags=["二叉树", "重建", "遍历序列"],
    statement_md=(
        "给定二叉树的**先序**和**中序**遍历序列（结点互不相同），求**后序**序列。\n\n"
        "核心只有一句话：**先序的第一个元素就是根**，拿着这个根去中序里一劈两半，"
        "左边是左子树、右边是右子树，然后递归。\n\n"
        "```text\n"
        "先序: A B D E C\n"
        "中序: D B E A C\n"
        "根 A → 中序里 A 左边是 DBE（左子树）、右边是 C（右子树）\n"
        "后序: D E B C A\n"
        "```\n\n"
        "★ 只给「先序 + 后序」是**推不出唯一二叉树**的；"
        "必须是「先序 + 中序」或者「后序 + 中序」。"
    ),
    input_format="第一行先序序列。\n\n第二行中序序列。\n\n（两行都是不含分隔符的字符串，长度相同。）",
    output_format="一行，后序遍历的结点序列。",
    constraints_md="- 结点数不超过 1000\n- 结点用不重复的大写字母表示",
    inputs=[
        "ABDEC\nDBEAC\n",
        "A\nA\n",
        "ABC\nBAC\n",
        "AB\nAB\n",
        "AB\nBA\n",
        "ABC\nACB\n",
        "ABCDEFG\nCBDAFEG\n",
    ],
    samples=3,

    oracle=_oracle_28,

    solution=r'''#include <stdio.h>
#include <string.h>
char pre[1005], ino[1005];
int idx[256];
static void solve(int pl, int pr, int il, int ir) {
    if (pl > pr) return;
    int k = idx[(unsigned char)pre[pl]];      /* 根在中序里的位置 */
    int ln = k - il;                          /* 左子树结点个数 */
    solve(pl + 1, pl + ln, il, k - 1);        /* 左 */
    solve(pl + ln + 1, pr, k + 1, ir);        /* 右 */
    putchar(pre[pl]);                         /* 根（后序最后输出） */
}
int main(void) {
    scanf("%s %s", pre, ino);
    int n = (int)strlen(pre);
    for (int i = 0; i < n; i++) idx[(unsigned char)ino[i]] = i;
    solve(0, n - 1, 0, n - 1);
    putchar('\n');
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <string>
#include <vector>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string pre, ino; cin >> pre >> ino;
    int n = (int)pre.size();
    int idx[256] = {0};
    for (int i = 0; i < n; i++) idx[(unsigned char)ino[i]] = i;
    // 另一套：**从后往前**把后序填进数组 —— 先放根，再走右子树、再走左子树
    vector<char> post(n);
    int pi = n;
    struct R {
        string &pre; int *idx; vector<char> &post; int &pi;
        void go(int pl, int pr, int il, int ir) {
            if (pl > pr) return;
            int k = idx[(unsigned char)pre[pl]];
            int ln = k - il;
            post[--pi] = pre[pl];                       // 根排在本段末尾
            go(pl + ln + 1, pr, k + 1, ir);             // ★ 倒填 → 先右后左
            go(pl + 1, pl + ln, il, k - 1);
        }
    } rec{pre, idx, post, pi};
    rec.go(0, n - 1, 0, n - 1);
    for (char c : post) cout << c;
    cout << "\n";
    return 0;
}
''',
)

def _oracle_29(text: str) -> str:
    s = text.strip()

    def rec(i: int):
        if i >= len(s) or s[i] == "#":
            return None, i + 1
        v = s[i]
        left, i = rec(i + 1)
        right, i = rec(i)
        return (v, left, right), i

    root, _ = rec(0)
    if root is None:
        return "yes\n"
    q = [root]
    seen_null = False
    ok = True
    while q:
        n = q.pop(0)
        if n is None:
            seen_null = True
            continue
        if seen_null:                # 空结点之后又出现非空 → 不是完全二叉树
            ok = False
            break
        q.append(n[1])
        q.append(n[2])
    return ("yes\n" if ok else "no\n")

add(
    title="判断一棵二叉树是否为完全二叉树",
    section="第 05 讲 · 树和二叉树",
    difficulty=4, score=25, tags=["二叉树", "完全二叉树", "层次遍历"],
    statement_md=(
        "判断给定的二叉树是不是**完全二叉树**。\n\n"
        "完全二叉树的定义：**按层序编号后，编号与满二叉树一一对应，中间不能缺号**。\n\n"
        "判定方法是层次遍历的一个小改造：\n\n"
        "1. 把结点**连同空孩子一起**按层序排开\n"
        "2. 一旦遇到第一个空结点，**后面不允许再出现非空结点**\n\n"
        "这个判据一句话就够用：**空结点出现之后，全是空结点**。\n\n"
        "举例：`A(∅, B)`（结点 B 只有右孩子，左边是空的）—— "
        "排开后 `A, ∅, B`，空结点后面又冒出 B，所以**不是**完全二叉树。"
    ),
    input_format="一行，带空标记的前序序列。",
    output_format="一行，`yes` 或 `no`（空树视为完全二叉树）。",
    constraints_md="- 序列长度不超过 2000",
    inputs=["A##\n", "AB##C##\n", "A#B##\n", "AB#D##C##\n", "AB##\n", "#\n", "ABC####\n"],
    samples=3,

    oracle=_oracle_29,

    solution=r'''#include <stdio.h>
#include <string.h>
#include <stdlib.h>
typedef struct BTNode { char data; struct BTNode *l, *r; } BTNode;
char s[2005];
int pos;
BTNode *build(void) {
    char c = s[pos++];
    if (c == '#' || c == '\0') return NULL;
    BTNode *t = (BTNode *)malloc(sizeof(BTNode));
    t->data = c; t->l = build(); t->r = build();
    return t;
}
int main(void) {
    scanf("%s", s);
    pos = 0;
    BTNode *root = build();
    if (!root) { printf("yes\n"); return 0; }
    BTNode *q[4005];                 /* ★ 空结点也要入队，所以容量翻倍 */
    int front = 0, rear = 0, seenNull = 0;
    q[rear++] = root;
    while (front < rear) {
        BTNode *t = q[front++];
        if (!t) { seenNull = 1; continue; }
        if (seenNull) { printf("no\n"); return 0; }
        q[rear++] = t->l;            /* 空孩子照样入队 */
        q[rear++] = t->r;
    }
    printf("yes\n");
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <string>
#include <vector>
using namespace std;
struct Node { char c; int l = -1, r = -1; };
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s; cin >> s;
    vector<Node> pool;
    int pos = 0;
    struct R {
        string &s; vector<Node> &pool; int &pos;
        int build() {
            char c = s[pos++];
            if (c == '#' || pos > (int)s.size()) return -1;
            int id = (int)pool.size();
            pool.push_back(Node{c, -1, -1});
            int l = build(), r = build();
            pool[id].l = l; pool[id].r = r;
            return id;
        }
    } rec{s, pool, pos};
    int root = rec.build();
    if (root < 0) { cout << "yes\n"; return 0; }
    // 另一套：**不用队列**，按完全二叉树的编号性质检查
    // 完全二叉树存在 ⇔ 层序编号 1..n 连续且每层填满
    vector<int> q{root};
    bool ok = true;
    for (size_t i = 0; i < q.size() && ok; i++) {
        int id = q[i];
        if (id < 0) {                       // 遇到空位：后面必须全空
            for (size_t j = i + 1; j < q.size(); j++)
                if (q[j] >= 0) { ok = false; break; }
            if (i + 1 >= q.size()) break;   // 空位之后还没展开，继续看
            break;
        }
        q.push_back(pool[id].l);
        q.push_back(pool[id].r);
    }
    cout << (ok ? "yes" : "no") << "\n";
    return 0;
}
''',
)

def _oracle_30(text: str) -> str:
    d = text.split()
    n = int(d[0])
    w = sorted(int(v) for v in d[1:1 + n])
    if n <= 1:
        return "0\n"
    total = 0
    while len(w) > 1:
        a = w.pop(0)
        b = w.pop(0)
        s = a + b
        total += s                    # ★ WPL = 内部结点权值之和
        # 插回有序位置（保持列表有序）
        lo, hi = 0, len(w)
        while lo < hi:
            mid = (lo + hi) // 2
            if w[mid] < s:
                lo = mid + 1
            else:
                hi = mid
        w.insert(lo, s)
    return "%d\n" % total

add(
    title="哈夫曼树的带权路径长度",
    section="第 05 讲 · 树和二叉树",
    difficulty=4, score=25, tags=["哈夫曼树", "WPL", "贪心"],
    statement_md=(
        "给定 `n` 个权值，求构造出的**哈夫曼树**的**带权路径长度 WPL**。\n\n"
        "构造方法是贪心：**每次取两个最小的合并**，新结点权值为两者之和，"
        "再放回去，重复到只剩一个结点。\n\n"
        "求 WPL 有个**非常省事的等价算法**：\n\n"
        "> WPL = **所有内部结点（新合成的结点）权值之和**\n\n"
        "因为每合并一次，那个新结点就代表「这批叶子整体多走一层」，"
        "累加起来正好等于 Σ(权值 × 层数)。不用去建树、也不用算每个叶子的深度。\n\n"
        "本机实测过：`1 2 3 4 5` → 合并过程 3、6、9、15，"
        "WPL = 3+6+9+15 = **33**。"
    ),
    input_format="第一行一个整数 `n`。\n\n第二行 `n` 个正整数，表示各叶子结点的权值。",
    output_format="一行，一个整数，WPL。（`n = 1` 时 WPL 为 `0`。）",
    constraints_md="- 1 ≤ n ≤ 1000\n- 权值 ≤ 10^9",
    inputs=[
        "5\n1 2 3 4 5\n",
        "1\n7\n",
        "2\n3 5\n",
        "4\n1 1 1 1\n",
        "3\n5 5 5\n",
        "6\n1 2 3 4 5 6\n",
        "3\n1 2 100\n",
    ],
    samples=3,

    oracle=_oracle_30,

    solution=r'''#include <stdio.h>
#include <queue>
#include <vector>
using namespace std;
int main(void) {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    priority_queue<long long, vector<long long>, greater<long long> > pq;
    for (int i = 0; i < n; i++) {
        long long v; scanf("%lld", &v);
        pq.push(v);
    }
    long long wpl = 0;
    while (pq.size() > 1) {
        long long a = pq.top(); pq.pop();
        long long b = pq.top(); pq.pop();
        wpl += a + b;              /* ★ 内部结点权值累加即可 */
        pq.push(a + b);
    }
    printf("%lld\n", wpl);
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n; cin >> n;
    vector<long long> w(n);
    for (auto &v : w) cin >> v;
    // 另一套：不用堆，每次**线性扫描**找两个最小的（O(n^2)，n 小够用）
    long long wpl = 0;
    while (w.size() > 1) {
        size_t i1 = 0;
        for (size_t k = 1; k < w.size(); k++) if (w[k] < w[i1]) i1 = k;
        long long a = w[i1];
        w.erase(w.begin() + (long)i1);
        size_t i2 = 0;
        for (size_t k = 1; k < w.size(); k++) if (w[k] < w[i2]) i2 = k;
        long long b = w[i2];
        w.erase(w.begin() + (long)i2);
        wpl += a + b;
        w.push_back(a + b);
    }
    cout << wpl << "\n";
    return 0;
}
''',
)

def _oracle_31(text: str) -> str:
    d = text.split()
    p = 0
    n, m = int(d[p]), int(d[p + 1]); p += 2
    parent = list(range(n + 1))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]      # 路径压缩
            x = parent[x]
        return x

    for _ in range(m):
        u, v = int(d[p]), int(d[p + 1]); p += 2
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
    comps = sum(1 for i in range(1, n + 1) if find(i) == i)
    q = int(d[p]); p += 1
    out = [str(comps)]
    for _ in range(q):
        u, v = int(d[p]), int(d[p + 1]); p += 2
        out.append("yes" if find(u) == find(v) else "no")
    return "\n".join(out) + "\n"

add(
    title="并查集统计连通块",
    section="第 05 讲 · 树和二叉树",
    difficulty=3, score=20, tags=["并查集", "连通块", "路径压缩"],
    statement_md=(
        "`n` 个点和 `m` 条无向边，求**连通块个数**，并回答若干「两点是否连通」的询问。\n\n"
        "并查集的两个优化（本机实测差距很大）：\n\n"
        "| 做法 | 找一次根要走几步 |\n"
        "|---|---|\n"
        "| 朴素合并（总把后一个挂到前一个） | 平均 **91** 步，最深 13 层 |\n"
        "| 按大小合并 | **13** 步，深 1 层 |\n"
        "| 只做路径压缩 | **25** 步，深 1 层 |\n"
        "| 两个都做 | **13** 步，深 1 层 |\n\n"
        "★ **路径压缩只在查找时把路径压平**，所以第一次查还是会长；"
        "**按大小合并**才是让树一开始就矮的关键。两者都做效果最好。\n\n"
        "输出：第一行连通块个数；随后每个询问输出 `yes` / `no`。"
    ),
    input_format=(
        "第一行两个整数 `n` `m`。\n\n"
        "随后 `m` 行，每行两个整数 `u` `v`，表示一条无向边（可能有自环或重复边）。\n\n"
        "接着一行一个整数 `q`（询问个数）。\n\n"
        "随后 `q` 行，每行两个整数 `u` `v`。"
    ),
    output_format="第一行连通块个数；随后 `q` 行，每行 `yes` 或 `no`。",
    constraints_md="- 1 ≤ n ≤ 1000\n- 0 ≤ m ≤ 2000\n- 1 ≤ q ≤ 1000",
    inputs=[
        "5 3\n1 2\n2 3\n4 5\n2\n1 3\n1 4\n",
        "1 0\n1\n1 1\n",
        "4 0\n3\n1 2\n3 4\n1 1\n",
        "6 5\n1 2\n2 3\n3 1\n4 5\n5 6\n2\n1 3\n1 6\n",
        "3 2\n1 2\n1 2\n2\n2 1\n2 3\n",
    ],
    samples=2,

    oracle=_oracle_31,

    solution=r'''#include <stdio.h>
int parent[1005], sz[1005];
static int find(int x) {
    while (parent[x] != x) {
        parent[x] = parent[parent[x]];      /* 路径压缩（隔代压缩） */
        x = parent[x];
    }
    return x;
}
int main(void) {
    int n, m;
    scanf("%d %d", &n, &m);
    for (int i = 1; i <= n; i++) { parent[i] = i; sz[i] = 1; }
    for (int k = 0; k < m; k++) {
        int u, v;
        scanf("%d %d", &u, &v);
        int ru = find(u), rv = find(v);
        if (ru == rv) continue;
        if (sz[ru] < sz[rv]) { int t = ru; ru = rv; rv = t; }  /* 按大小合并 */
        parent[rv] = ru;
        sz[ru] += sz[rv];
    }
    int comps = 0;
    for (int i = 1; i <= n; i++) if (find(i) == i) comps++;
    printf("%d\n", comps);
    int q;
    scanf("%d", &q);
    for (int k = 0; k < q; k++) {
        int u, v;
        scanf("%d %d", &u, &v);
        printf(find(u) == find(v) ? "yes\n" : "no\n");
    }
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
#include <queue>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m; cin >> n >> m;
    // 另一套：**完全不用并查集**，直接建邻接表跑 BFS 求连通块
    vector<vector<int>> g(n + 1);
    for (int k = 0; k < m; k++) {
        int u, v; cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }
    vector<int> comp(n + 1, 0);
    int cid = 0;
    for (int s = 1; s <= n; s++) {
        if (comp[s]) continue;
        cid++;
        queue<int> q; q.push(s); comp[s] = cid;
        while (!q.empty()) {
            int x = q.front(); q.pop();
            for (int y : g[x]) if (!comp[y]) { comp[y] = cid; q.push(y); }
        }
    }
    cout << cid << "\n";
    int qq; cin >> qq;
    while (qq--) {
        int u, v; cin >> u >> v;
        cout << (comp[u] == comp[v] ? "yes" : "no") << "\n";
    }
    return 0;
}
''',
)


HEADER = '''"""数据结构线题库（C / C++）—— **自动生成，不要手改**。

本文件由 `tools/gen_ds_bank.py` 产出，重新生成：

    python tools/gen_ds_bank.py

三条规矩写在这里，改题前先读一遍
--------------------------------
1. **期望输出不是拿参考解跑出来的** —— 由生成脚本里的独立 Python `oracle`
   预先算好（另一门语言、另一套写法）。拿参考解现跑现填等于自己给自己判卷。
2. **每题两套 C++ 实现**（`reference_solution` / `alt_solution`），
   `tools/verify_bank.py` 会把两套都跑一遍逐字节对拍。
   `alt_solution` 只在题库校验时用，`seed.py` 入库时会丢掉它。
3. **语言**：`line = "cpp"`，但**同一道题 C 和 C++ 都能交** ——
   C++ 走 g++ -std=c++17，C 走 gcc -std=gnu11（教材是 C 语言版）。
   判题时按提交里带的语言选编译器，见 `app/judge/runner_cpp.py`。

覆盖范围：数据结构第 02 ~ 05 讲（线性表 / 栈与队列 / 串数组广义表 / 树与二叉树）。
"""
from __future__ import annotations

DS_PROBLEMS: list[dict] = '''


def build() -> list[dict]:
    """把 PROBLEMS 展开成入库用的题目 dict（用例的期望输出在这里算出来）。"""
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
            # 编译型：同一道题 C / C++ 任选（见模块 docstring 第 3 条）
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
            # 参考解是 C++；要换成 C 版就把这里改成 "gcc" 并重写两套解
            "ref_interpreter": "gpp",
            "reference_solution": p["solution"],
            "alt_solution": p["alt"],
            "cases": cases,
        })
    return out


def _dump(probs: list[dict]) -> str:
    """序列化成可读的 Python 字面量。

    直接用 json.dumps 打底（缩进好看、转义不用操心），
    再把 JSON 的 null/true/false 换成 Python 的写法。
    我们所有字段都是 str / int / list，不会出现嵌套的裸字面量，替换是安全的。
    """
    body = json.dumps(probs, ensure_ascii=False, indent=4)
    body = body.replace(": null", ": None").replace(": true", ": True").replace(": false", ": False")
    return HEADER + body + "\n"


def _sanity(probs: list[dict]) -> list[str]:
    """入库前的最后一道门：逐题检查必填字段与用例形态。"""
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
        # 样例数不能超过用例总数
        ns = sum(1 for c in p["cases"] if c["is_sample"])
        if ns > len(p["cases"]):
            problems.append("[%d] %s 样例数超了" % (i, t))
        for j, c in enumerate(p["cases"], 1):
            if not c["expected_stdout"]:
                problems.append("[%d] %s 第 %d 个用例期望输出为空" % (i, t, j))
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description="生成数据结构 C/C++ 题库")
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

    # 每个 oracle 都必须产出非空输出 —— 空输出几乎一定是 oracle 写错了
    empties = [p["title"] for p in probs
               if any(not c["expected_stdout"].strip() for c in p["cases"])]
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
