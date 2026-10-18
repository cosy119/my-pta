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
sys.path.insert(0, str(ROOT))
from app.bank_kit import mc, tf, multi                     # noqa: E402

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


# --------------------------------------------------------------------- #
#  第 06 讲 · 图
# --------------------------------------------------------------------- #

def _oracle_32(text: str) -> str:
    d = text.split()
    n, m = int(d[0]), int(d[1])
    adj = [[] for _ in range(n + 1)]
    idx = 2
    for _ in range(m):
        u, v = int(d[idx]), int(d[idx + 1]); idx += 2
        adj[u].insert(0, v)          # 头插法：后进来的边排在链前头
        adj[v].insert(0, u)
    return "\n".join(" ".join([str(i) + ":"] + [str(v) for v in adj[i]])
                     for i in range(1, n + 1)) + "\n"

add(
    title="无向图的邻接表（头插法）",
    section="第 06 讲 · 图",
    difficulty=2, score=15, tags=["邻接表", "头插法", "链式存储"],
    statement_md=(
        "读入一个无向图，用**头插法**建立邻接表，然后按顶点序号 `1` ~ `n` "
        "依次输出每个顶点的邻接点链。\n\n"
        "★ 教材的 `firstedge/nextarc` 写法就是**头插法**：后读入的边结点"
        "插到链的最前面。所以每个顶点的邻接点顺序与输入顺序**正好相反**——"
        "这也是判题的点：你要是按 `vector.push_back` 顺序输出，样例第一个就过不去。\n\n"
        "孤立顶点输出 `i:`（冒号后什么都没有，也没有空格）。"
    ),
    input_format=(
        "第一行 `n m`（顶点数、边数）。\n\n"
        "接下来 `m` 行，每行 `u v` 表示一条无向边（`1 ≤ u,v ≤ n`，"
        "无重边、无自环）。"
    ),
    output_format=(
        "`n` 行，第 `i` 行为顶点 `i` 的邻接链，格式 `i: v1 v2 ...`"
        "（邻接点按头插法顺序，即与输入顺序相反；孤立顶点输出 `i:`）。"
    ),
    constraints_md="- 1 ≤ n ≤ 100\n- 0 ≤ m ≤ n(n-1)/2",
    inputs=[
        "4 5\n1 2\n1 3\n1 4\n2 3\n3 4\n",
        "3 1\n2 3\n",
        "1 0\n",
        "5 6\n1 2\n2 3\n3 4\n4 5\n5 1\n2 4\n",
        "2 1\n1 2\n",
    ],
    samples=2,

    oracle=_oracle_32,

    solution=r'''#include <stdio.h>
#define MAXN 105
#define MAXE 4005
int head[MAXN], nxt[MAXE], to[MAXE], ecnt = 0;
/* 教材式头插法：新边结点插到链的最前面 */
void add_edge(int u, int v) {
    ++ecnt; to[ecnt] = v; nxt[ecnt] = head[u]; head[u] = ecnt;
}
int main(void) {
    int n, m;
    scanf("%d %d", &n, &m);
    for (int k = 0; k < m; k++) {
        int u, v; scanf("%d %d", &u, &v);
        add_edge(u, v); add_edge(v, u);
    }
    for (int i = 1; i <= n; i++) {
        printf("%d:", i);
        for (int e = head[i]; e; e = nxt[e]) printf(" %d", to[e]);
        printf("\n");
    }
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
/* 另一套：不用链表，用 vector 顺序收、输出时整体 reverse */
int main() {
    int n, m; cin >> n >> m;
    vector<vector<int>> adj(n + 1);
    for (int k = 0; k < m; k++) {
        int u, v; cin >> u >> v;
        adj[u].push_back(v); adj[v].push_back(u);
    }
    for (int i = 1; i <= n; i++) {
        vector<int> r = adj[i];
        reverse(r.begin(), r.end());     // 头插法的效果 = 逆输入序
        cout << i << ":";
        for (int v : r) cout << " " << v;
        cout << "\n";
    }
    return 0;
}
''',
)

def _oracle_33(text: str) -> str:
    d = text.split()
    n, m, s, t = int(d[0]), int(d[1]), int(d[2]), int(d[3])
    g = [[] for _ in range(n + 1)]
    idx = 4
    for _ in range(m):
        u, v = int(d[idx]), int(d[idx + 1]); idx += 2
        g[u].append(v); g[v].append(u)
    from collections import deque
    dist = [-1] * (n + 1)
    dist[s] = 0
    q = deque([s])
    while q:
        x = q.popleft()
        for y in g[x]:
            if dist[y] < 0:
                dist[y] = dist[x] + 1
                q.append(y)
    return "%d\n" % dist[t]

add(
    title="无权图的最短跳数（BFS）",
    section="第 06 讲 · 图",
    difficulty=2, score=15, tags=["BFS", "队列", "最短路径"],
    statement_md=(
        "给一个无权无向图和两个顶点 `s`、`t`，求从 `s` 走到 `t` 最少要经过"
        "几条边（跳数）。到不了输出 `-1`。\n\n"
        "★ BFS 是「按跳数分层」的：队列里先放跳数 0 的、再放跳数 1 的……"
        "所以**第一次摸到 `t` 时记录的跳数就是答案**。这题用的正是讲义里"
        "「BFS 副产品：最短跳数」的那套写法——用 `dist[]` 边入队边标距离，"
        "别用「出队时才标记」的反面教材。"
    ),
    input_format=(
        "第一行 `n m s t`（顶点数、边数、起点、终点，`s ≠ t`）。\n\n"
        "接下来 `m` 行，每行 `u v` 表示一条无向边（无重边、无自环）。"
    ),
    output_format="一行，一个整数：最少跳数；不可达为 `-1`。",
    constraints_md="- 2 ≤ n ≤ 100\n- 0 ≤ m ≤ n(n-1)/2",
    inputs=[
        "6 7 1 5\n1 2\n1 3\n2 4\n3 4\n4 5\n3 5\n2 6\n",
        "4 2 1 4\n1 2\n3 4\n",
        "2 1 1 2\n1 2\n",
        "5 5 1 4\n1 2\n2 3\n3 4\n4 5\n5 1\n",
        "3 0 1 3\n",
    ],
    samples=2,

    oracle=_oracle_33,

    solution=r'''#include <iostream>
#include <vector>
#include <queue>
using namespace std;
int main() {
    int n, m, s, t; cin >> n >> m >> s >> t;
    vector<vector<int>> g(n + 1);
    for (int k = 0; k < m; k++) {
        int u, v; cin >> u >> v;
        g[u].push_back(v); g[v].push_back(u);
    }
    vector<int> dist(n + 1, -1);
    queue<int> q;
    dist[s] = 0; q.push(s);              // 入队即标记
    while (!q.empty()) {
        int x = q.front(); q.pop();
        for (int y : g[x])
            if (dist[y] < 0) { dist[y] = dist[x] + 1; q.push(y); }
    }
    cout << dist[t] << "\n";
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
using namespace std;
/* 另一套：不用队列，按「层」扩展——cur 是跳数为 k 的全部顶点 */
int main() {
    int n, m, s, t; cin >> n >> m >> s >> t;
    vector<vector<int>> g(n + 1);
    for (int k = 0; k < m; k++) {
        int u, v; cin >> u >> v;
        g[u].push_back(v); g[v].push_back(u);
    }
    vector<char> seen(n + 1, 0);
    vector<int> cur = {s};
    seen[s] = 1;
    int hops = 0, ans = -1;
    while (!cur.empty()) {
        vector<int> nxt;
        for (int x : cur) {
            if (x == t) { ans = hops; cur.clear(); break; }
            for (int y : g[x]) if (!seen[y]) { seen[y] = 1; nxt.push_back(y); }
        }
        if (ans >= 0) break;
        cur = nxt; hops++;
    }
    cout << ans << "\n";
    return 0;
}
''',
)

def _oracle_34(text: str) -> str:
    d = text.split()
    n, m, s = int(d[0]), int(d[1]), int(d[2])
    INF = float("inf")
    w = [[INF] * (n + 1) for _ in range(n + 1)]
    idx = 3
    for _ in range(m):
        u, v, c = int(d[idx]), int(d[idx + 1]), int(d[idx + 2]); idx += 3
        if u != v and c < w[u][v]:
            w[u][v] = c                  # 重边取最小
    dist = [INF] * (n + 1)
    done = [False] * (n + 1)
    dist[s] = 0
    for _ in range(n):
        x = -1
        for i in range(1, n + 1):
            if not done[i] and dist[i] < INF and (x < 0 or dist[i] < dist[x]):
                x = i
        if x < 0:
            break
        done[x] = True
        for y in range(1, n + 1):
            if w[x][y] < INF and dist[x] + w[x][y] < dist[y]:
                dist[y] = dist[x] + w[x][y]
    return " ".join("-1" if dist[i] == INF else str(dist[i])
                    for i in range(1, n + 1)) + "\n"

add(
    title="单源最短路径（Dijkstra）",
    section="第 06 讲 · 图",
    difficulty=3, score=20, tags=["Dijkstra", "贪心", "最短路径"],
    statement_md=(
        "给一个**边权非负**的有向图和源点 `s`，输出 `s` 到每个顶点的最短距离，"
        "到不了的输出 `-1`（`s` 到自己是 `0`）。\n\n"
        "★ Dijkstra 的贪心内核：每轮从「未定」的顶点里挑 `dist` 最小的"
        "（用不用堆都行，数据规模小，O(n²) 的教材写法就够），"
        "把它标成「已定」，再用它松驰出边。\n\n"
        "**它不能处理负权边**——讲义里给过反例（Dijkstra 会翻车而 Floyd 正确），"
        "所以本题保证所有边权 > 0。"
    ),
    input_format=(
        "第一行 `n m s`（顶点数、边数、源点）。\n\n"
        "接下来 `m` 行，每行 `u v w` 表示一条 `u → v`、权 `w`（1 ≤ w ≤ 100）"
        "的有向边；可能有重边（取最小即可），无自环。"
    ),
    output_format=(
        "一行 `n` 个整数（空格分隔）：`s` 到各顶点的最短距离；"
        "不可达为 `-1`。"
    ),
    constraints_md="- 1 ≤ n ≤ 50\n- 0 ≤ m ≤ n(n-1)\n- 1 ≤ w ≤ 100",
    inputs=[
        "4 5 1\n1 2 5\n1 3 1\n3 2 1\n2 4 2\n3 4 6\n",
        "3 1 1\n1 2 7\n",
        "2 0 1\n",
        "4 6 2\n1 2 3\n2 3 1\n3 4 1\n1 3 5\n2 4 10\n1 4 100\n",
        "5 7 1\n1 2 10\n1 4 30\n1 5 100\n2 3 50\n3 5 10\n4 3 20\n4 5 60\n",
    ],
    samples=2,

    oracle=_oracle_34,

    solution=r'''#include <iostream>
#include <vector>
using namespace std;
int main() {
    int n, m, s; cin >> n >> m >> s;
    const long long INF = (long long)1e18;
    vector<vector<long long>> w(n + 1, vector<long long>(n + 1, INF));
    for (int k = 0; k < m; k++) {
        int u, v; long long c; cin >> u >> v >> c;
        if (u != v && c < w[u][v]) w[u][v] = c;
    }
    vector<long long> dist(n + 1, INF);
    vector<char> done(n + 1, 0);
    dist[s] = 0;
    for (int round = 0; round < n; round++) {
        int x = -1;
        for (int i = 1; i <= n; i++)
            if (!done[i] && dist[i] < INF && (x < 0 || dist[i] < dist[x])) x = i;
        if (x < 0) break;
        done[x] = 1;
        for (int y = 1; y <= n; y++)
            if (w[x][y] < INF && dist[x] + w[x][y] < dist[y])
                dist[y] = dist[x] + w[x][y];
    }
    for (int i = 1; i <= n; i++) {
        if (i > 1) cout << " ";
        if (dist[i] < INF) cout << dist[i]; else cout << -1;
    }
    cout << "\n";
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
using namespace std;
/* 另一套：Floyd 全源最短路，最后只打印 s 那一行（n ≤ 50，三次方也毫无压力） */
int main() {
    int n, m, s; cin >> n >> m >> s;
    const long long INF = (long long)1e18;
    vector<vector<long long>> d(n + 1, vector<long long>(n + 1, INF));
    for (int i = 1; i <= n; i++) d[i][i] = 0;
    for (int k = 0; k < m; k++) {
        int u, v; long long c; cin >> u >> v >> c;
        if (c < d[u][v]) d[u][v] = c;
    }
    for (int k = 1; k <= n; k++)
        for (int i = 1; i <= n; i++)
            for (int j = 1; j <= n; j++)
                if (d[i][k] < INF && d[k][j] < INF && d[i][k] + d[k][j] < d[i][j])
                    d[i][j] = d[i][k] + d[k][j];
    for (int j = 1; j <= n; j++) {
        if (j > 1) cout << " ";
        if (d[s][j] < INF) cout << d[s][j]; else cout << -1;
    }
    cout << "\n";
    return 0;
}
''',
)

def _oracle_35(text: str) -> str:
    import heapq
    d = text.split()
    n, m = int(d[0]), int(d[1])
    g = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    idx = 2
    for _ in range(m):
        u, v = int(d[idx]), int(d[idx + 1]); idx += 2
        g[u].append(v); indeg[v] += 1
    heap = [i for i in range(1, n + 1) if indeg[i] == 0]
    heapq.heapify(heap)
    order = []
    while heap:
        x = heapq.heappop(heap)
        order.append(x)
        for y in g[x]:
            indeg[y] -= 1
            if indeg[y] == 0:
                heapq.heappush(heap, y)
    if len(order) < n:
        return "loop\n"
    return " ".join(map(str, order)) + "\n"

add(
    title="拓扑排序（字典序最小）",
    section="第 06 讲 · 图",
    difficulty=3, score=20, tags=["拓扑排序", "AOV 网", "贪心"],
    statement_md=(
        "给一个有向无环图（也可能有环），输出它的一个拓扑序——要求"
        "**字典序最小**的那个；如果图里有环（顶点数不足 `n`），输出 `loop`。\n\n"
        "★ 教材用**栈**存入度为 0 的顶点，弹出来的顺序是「某种」合法拓扑序；"
        "本题要字典序最小，把栈换成**小根堆**就行，算法骨架一模一样。\n\n"
        "环检测就是讲义里那句：**出堆个数 < n ⇒ 有环**。"
    ),
    input_format=(
        "第一行 `n m`（顶点数、弧数）。\n\n"
        "接下来 `m` 行，每行 `u v` 表示弧 `<u, v>`（无重边、无自环）。"
    ),
    output_format=(
        "一行：字典序最小的拓扑序（`n` 个数，空格分隔）；"
        "有环输出 `loop`。"
    ),
    constraints_md="- 1 ≤ n ≤ 100\n- 0 ≤ m ≤ n(n-1)",
    inputs=[
        "5 6\n1 2\n1 3\n3 4\n2 4\n4 5\n2 5\n",
        "5 6\n1 3\n1 2\n2 4\n3 4\n4 5\n3 5\n",
        "5 5\n2 1\n2 3\n1 4\n3 4\n4 5\n",
        "3 3\n1 2\n2 3\n3 1\n",
        "6 6\n1 4\n2 4\n2 5\n3 5\n4 6\n5 6\n",
    ],
    samples=2,

    oracle=_oracle_35,

    solution=r'''#include <iostream>
#include <vector>
#include <queue>
#include <functional>
using namespace std;
int main() {
    int n, m; cin >> n >> m;
    vector<vector<int>> g(n + 1);
    vector<int> indeg(n + 1, 0);
    for (int k = 0; k < m; k++) {
        int u, v; cin >> u >> v;
        g[u].push_back(v); indeg[v]++;
    }
    priority_queue<int, vector<int>, greater<int>> pq;   // 小根堆
    for (int i = 1; i <= n; i++) if (indeg[i] == 0) pq.push(i);
    vector<int> order;
    while (!pq.empty()) {
        int x = pq.top(); pq.pop();
        order.push_back(x);
        for (int y : g[x]) if (--indeg[y] == 0) pq.push(y);
    }
    if ((int)order.size() < n) { cout << "loop\n"; return 0; }
    for (size_t i = 0; i < order.size(); i++)
        cout << (i ? " " : "") << order[i];
    cout << "\n";
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
using namespace std;
/* 另一套：不用堆，每轮线性扫「未用过的入度 0 顶点里编号最小的」（O(n²)） */
int main() {
    int n, m; cin >> n >> m;
    vector<vector<int>> g(n + 1);
    vector<int> indeg(n + 1, 0);
    for (int k = 0; k < m; k++) {
        int u, v; cin >> u >> v;
        g[u].push_back(v); indeg[v]++;
    }
    vector<char> used(n + 1, 0);
    vector<int> order;
    for (int round = 0; round < n; round++) {
        int x = -1;
        for (int i = 1; i <= n; i++)
            if (!used[i] && indeg[i] == 0) { x = i; break; }
        if (x < 0) break;
        used[x] = 1;
        order.push_back(x);
        for (int y : g[x]) indeg[y]--;
    }
    if ((int)order.size() < n) { cout << "loop\n"; return 0; }
    for (size_t i = 0; i < order.size(); i++)
        cout << (i ? " " : "") << order[i];
    cout << "\n";
    return 0;
}
''',
)


# --------------------------------------------------------------------- #
#  第 07 讲 · 查找
# --------------------------------------------------------------------- #

def _oracle_36(text: str) -> str:
    d = text.split()
    n = int(d[0])
    a = [int(v) for v in d[1:1 + n]]
    x = int(d[1 + n])
    low, high = 1, n
    probes, pos = [], -1
    while low <= high:
        mid = (low + high) // 2          # 教材口径：向下取整
        probes.append(a[mid - 1])
        if a[mid - 1] == x:
            pos = mid
            break
        elif a[mid - 1] < x:
            low = mid + 1
        else:
            high = mid - 1
    return " ".join(map(str, probes)) + "\n%d\n" % pos

add(
    title="折半查找的每次比较",
    section="第 07 讲 · 查找",
    difficulty=2, score=15, tags=["折半查找", "判定树", "有序表"],
    statement_md=(
        "对一张**严格递增**的有序表做折半查找，输出**依次与之比较的元素**，"
        "以及查找结果。\n\n"
        "★ 口径钉死（教材写法）：下标 `low=1`、`high=n`，"
        "`mid = ⌊(low+high)/2⌋`；`a[mid] == x` 命中，`a[mid] < x` 去 "
        "`[mid+1, high]`，否则去 `[low, mid-1]`。\n\n"
        "查不到也要把比较过的元素列全——失败 happens 在 `low > high` 那一刻，"
        "比较次数和成功一样有讲究（讲义里 n=11 时查 25 也是 4 次）。"
    ),
    input_format=(
        "第一行 `n`（表长）。\n\n"
        "第二行 `n` 个严格递增的整数。\n\n"
        "第三行 `x`，要找的值。"
    ),
    output_format=(
        "第一行：依次与 `x` 比较过的元素（空格分隔）。\n\n"
        "第二行：命中位序（1 基）；查不到为 `-1`。"
    ),
    constraints_md="- 1 ≤ n ≤ 1000\n- 表元素严格递增且互不相同",
    inputs=[
        "11\n7 14 18 21 23 29 31 35 38 42 46\n23\n",
        "11\n7 14 18 21 23 29 31 35 38 42 46\n25\n",
        "11\n7 14 18 21 23 29 31 35 38 42 46\n7\n",
        "11\n7 14 18 21 23 29 31 35 38 42 46\n46\n",
        "11\n7 14 18 21 23 29 31 35 38 42 46\n5\n",
    ],
    samples=2,

    oracle=_oracle_36,

    solution=r'''#include <stdio.h>
#define MAXN 1005
int a[MAXN];
int main(void) {
    int n, x;
    scanf("%d", &n);
    for (int k = 0; k < n; k++) scanf("%d", &a[k]);
    scanf("%d", &x);
    int low = 1, high = n, pos = -1, first = 1;
    while (low <= high) {
        int mid = (low + high) / 2;      /* 教材口径：向下取整 */
        printf(first ? "%d" : " %d", a[mid - 1]);
        first = 0;
        if (a[mid - 1] == x) { pos = mid; break; }
        else if (a[mid - 1] < x) low = mid + 1;
        else high = mid - 1;
    }
    printf("\n%d\n", pos);
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
using namespace std;
/* 另一套：递归折半，探到的元素攒在 vector 里最后一起打 */
vector<int> probes;
int pos = -1;
void bsearch(const vector<int>& a, int low, int high, int x) {
    if (low > high) return;
    int mid = low + (high - low) / 2;    // 与 (low+high)/2 等价，防溢出写法
    probes.push_back(a[mid - 1]);
    if (a[mid - 1] == x) { pos = mid; return; }
    if (a[mid - 1] < x) bsearch(a, mid + 1, high, x);
    else bsearch(a, low, mid - 1, x);
}
int main() {
    int n, x; cin >> n;
    vector<int> a(n);
    for (int &v : a) cin >> v;
    cin >> x;
    bsearch(a, 1, n, x);
    for (size_t i = 0; i < probes.size(); i++)
        cout << (i ? " " : "") << probes[i];
    cout << "\n" << pos << "\n";
    return 0;
}
''',
)

def _oracle_37(text: str) -> str:
    d = text.split()
    n = int(d[0])
    keys = [int(v) for v in d[1:1 + n]]
    x = int(d[1 + n])

    class N:
        def __init__(self, v):
            self.v, self.l, self.r = v, None, None

    root = None
    for k in keys:                        # 教材递归插入
        if root is None:
            root = N(k); continue
        p = root
        while True:
            if k < p.v:
                if p.l is None: p.l = N(k); break
                p = p.l
            else:
                if p.r is None: p.r = N(k); break
                p = p.r

    inorder = []
    def walk(t):
        if t is None: return
        walk(t.l); inorder.append(t.v); walk(t.r)
    walk(root)

    def height(t):
        if t is None: return 0
        return 1 + max(height(t.l), height(t.r))

    cnt, p = 0, root
    while p is not None:
        cnt += 1
        if p.v == x: break
        p = p.l if x < p.v else p.r
    return " ".join(map(str, inorder)) + "\n%d\n%d\n" % (height(root), cnt)

add(
    title="二叉排序树：建树、遍历与查找",
    section="第 07 讲 · 查找",
    difficulty=3, score=20, tags=["二叉排序树", "BST", "中序遍历"],
    statement_md=(
        "按输入顺序把 `n` 个互不相同的数插入一棵**空的二叉排序树**，然后：\n\n"
        "1. 输出**中序遍历**序列（BST 的中序 = 升序，这是它的招牌性质）；\n"
        "2. 输出树高（**空树为 0，只有根为 1**；树高 = 最长路径上的结点数）；\n"
        "3. 在树中查找 `x`，输出**比较次数**（沿根往下走，每碰一个结点记 1 次，"
        "走到空指针为止——不存在也是这个口径）。\n\n"
        "★ 讲义里 n=11 顺序插入 1..15 那组实测：BST 会退化成链，"
        "树高直接飙到 n——插入顺序决定一切。"
    ),
    input_format=(
        "第一行 `n`（插入个数）。\n\n"
        "第二行 `n` 个互不相同的整数（按插入顺序给出）。\n\n"
        "第三行 `x`，要查找的值。"
    ),
    output_format=(
        "第一行：中序遍历序列（空格分隔）。\n\n"
        "第二行：树高。\n\n"
        "第三行：查找 `x` 的比较次数。"
    ),
    constraints_md="- 1 ≤ n ≤ 500\n- 插入值互不相同，|值| ≤ 10⁹",
    inputs=[
        "6\n45 24 53 12 37 93\n37\n",
        "6\n45 24 53 12 37 93\n40\n",
        "1\n10\n10\n",
        "3\n2 1 3\n4\n",
        "5\n5 4 3 2 1\n1\n",
    ],
    samples=2,

    oracle=_oracle_37,

    solution=r'''#include <stdio.h>
#include <stdlib.h>
typedef struct Btnode {
    int v;
    struct Btnode *l, *r;
} Btnode;
Btnode* New(int v) {
    Btnode* p = (Btnode*)malloc(sizeof(Btnode));
    p->v = v; p->l = p->r = NULL;
    return p;
}
/* 教材式递归插入 */
Btnode* Insert(Btnode* t, int v) {
    if (!t) return New(v);
    if (v < t->v) t->l = Insert(t->l, v);
    else if (v > t->v) t->r = Insert(t->r, v);
    return t;
}
void Inorder(Btnode* t, int* first) {
    if (!t) return;
    Inorder(t->l, first);
    if (*first) printf("%d", t->v); else printf(" %d", t->v);
    *first = 0;
    Inorder(t->r, first);
}
int Height(Btnode* t) {
    if (!t) return 0;
    int a = Height(t->l), b = Height(t->r);
    return 1 + (a > b ? a : b);
}
int main(void) {
    int n, x;
    scanf("%d", &n);
    Btnode* root = NULL;
    for (int k = 0; k < n; k++) {
        int v; scanf("%d", &v);
        root = Insert(root, v);
    }
    scanf("%d", &x);
    int first = 1;
    Inorder(root, &first);
    printf("\n%d\n", Height(root));
    int cnt = 0;
    Btnode* p = root;
    while (p) {
        cnt++;
        if (p->v == x) break;
        p = (x < p->v) ? p->l : p->r;
    }
    printf("%d\n", cnt);
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
using namespace std;
/* 另一套：插入/查找/求高全用迭代写法，结构上不碰递归 */
struct N { int v; N *l = nullptr, *r = nullptr; };
int main() {
    int n, x; cin >> n;
    N *root = nullptr;
    for (int k = 0; k < n; k++) {
        int v; cin >> v;
        if (!root) { root = new N{v}; continue; }
        N *p = root;
        while (true) {
            if (v < p->v) { if (!p->l) { p->l = new N{v}; break; } p = p->l; }
            else          { if (!p->r) { p->r = new N{v}; break; } p = p->r; }
        }
    }
    cin >> x;
    vector<int> in;
    vector<N*> st;
    N *p = root;                          // 迭代中序（模拟栈）
    while (p || !st.empty()) {
        while (p) { st.push_back(p); p = p->l; }
        p = st.back(); st.pop_back();
        in.push_back(p->v);
        p = p->r;
    }
    for (size_t i = 0; i < in.size(); i++) cout << (i ? " " : "") << in[i];
    cout << "\n";
    vector<vector<N*>> lvl;               // 层序求高
    if (root) lvl.push_back({root});
    for (size_t i = 0; i < lvl.size(); i++) {
        vector<N*> nx;
        for (N* q : lvl[i]) {
            if (q->l) nx.push_back(q->l);
            if (q->r) nx.push_back(q->r);
        }
        if (!nx.empty()) lvl.push_back(nx);
    }
    cout << lvl.size() << "\n";
    int cnt = 0; p = root;
    while (p) { cnt++; if (p->v == x) break; p = (x < p->v) ? p->l : p->r; }
    cout << cnt << "\n";
    return 0;
}
''',
)

def _oracle_38(text: str) -> str:
    d = text.split()
    m, p, n = int(d[0]), int(d[1]), int(d[2])
    keys = [int(v) for v in d[3:3 + n]]
    slot = [None] * m
    total = 0
    for k in keys:
        h = k % p
        cnt = 0
        while True:
            cnt += 1
            if slot[h] is None:
                slot[h] = k
                break
            h = (h + 1) % m
        total += cnt
    line1 = " ".join("#" if s is None else str(s) for s in slot)
    return line1 + "\n%.2f\n" % (total / n)

add(
    title="散列表：除留余数 + 线性探测",
    section="第 07 讲 · 查找",
    difficulty=3, score=20, tags=["散列表", "线性探测", "ASL"],
    statement_md=(
        "表长 `m`，散列函数 `H(key) = key % p`，冲突用**线性探测**"
        "（`Hi = (H(key) + i) % m`，i = 0,1,2,…）处理。\n\n"
        "输出两行：\n\n"
        "1. 槽位 `0` ~ `m-1` 的最终分布（空槽输出 `#`，空格分隔）；\n"
        "2. **成功查找的平均查找长度** = 各键探测次数之和 ÷ `n`，"
        "保留 2 位小数（`printf(\"%.2f\")` 的口径）。\n\n"
        "★ 讲义实测：教材那组 12 个键（m=16, p=13）里，`79` 因为探到 "
        "`1%13` 之后的一长串占用，**整整探了 9 次**才落进 `[9]`——"
        "「一次冲突不算什么，连锁冲突才是线性探测的命门」。"
    ),
    input_format=(
        "第一行 `m p n`（表长、模数、键个数，保证 n < m 且都能插进去）。\n\n"
        "第二行 `n` 个互不相同的非负整数。"
    ),
    output_format=(
        "第一行：`m` 个槽位的分布（空槽 `#`，空格分隔）。\n\n"
        "第二行：成功查找 ASL，保留 2 位小数。"
    ),
    constraints_md="- 2 ≤ p ≤ m ≤ 100\n- 1 ≤ n < m\n- 0 ≤ key ≤ 10⁹",
    inputs=[
        "16 13 12\n19 14 23 1 68 20 84 27 55 11 10 79\n",
        "7 7 5\n10 3 17 24 31\n",
        "5 5 5\n0 5 10 15 20\n",
        "8 5 4\n1 6 11 16\n",
        "6 3 3\n3 6 9\n",
    ],
    samples=2,

    oracle=_oracle_38,

    solution=r'''#include <stdio.h>
#define MAXM 105
long long slot[MAXM];                    /* -1 = 空 */
int has[MAXM];
int main(void) {
    int m, p, n;
    scanf("%d %d %d", &m, &p, &n);
    long long sum = 0;
    for (int k = 0; k < n; k++) {
        long long key; scanf("%lld", &key);
        int h = (int)(key % p), cnt = 0;
        while (1) {
            cnt++;
            if (!has[h]) { has[h] = 1; slot[h] = key; break; }
            h = (h + 1) % m;
        }
        sum += cnt;
    }
    for (int i = 0; i < m; i++)
        printf(i ? has[i] ? " %lld" : " #" : has[i] ? "%lld" : "#",
               slot[i]);
    printf("\n%.2f\n", (double)sum / n);
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
using namespace std;
/* 另一套：先算好每键落点与探测次数存进 pair，再统一输出 */
int main() {
    int m, p, n; cin >> m >> p >> n;
    vector<long long> key(n);
    vector<int> land(n), cost(n);
    vector<long long> slot(m, -1);
    long long sum = 0;
    for (int k = 0; k < n; k++) {
        cin >> key[k];
        int h = (int)(key[k] % p), c = 0;
        while (slot[h] != -1) { h = (h + 1) % m; c++; }
        c++;                              /* 命中空槽也算一次探测 */
        slot[h] = key[k];
        land[k] = h; cost[k] = c;
        sum += c;
    }
    vector<string> cell(m);
    for (int i = 0; i < m; i++)
        cell[i] = (slot[i] == -1) ? "#" : to_string(slot[i]);
    for (int i = 0; i < m; i++) cout << (i ? " " : "") << cell[i];
    cout << "\n";
    printf("%.2f\n", (double)sum / n);
    return 0;
}
''',
)

def _oracle_39(text: str) -> str:
    d = text.split()
    m, p, n = int(d[0]), int(d[1]), int(d[2])
    keys = [int(v) for v in d[3:3 + n]]
    buck = [[] for _ in range(m)]
    for k in keys:
        buck[k % p].insert(0, k)          # 教材头插法
    lines = []
    for i in range(m):
        lines.append(" ".join([str(i) + ":"] + [str(v) for v in buck[i]]))
    total = 0
    for k in keys:
        total += buck[k % p].index(k) + 1  # 链上第几个结点
    return "\n".join(lines) + "\n%.2f\n" % (total / n)

add(
    title="散列表：链地址法（头插法）",
    section="第 07 讲 · 查找",
    difficulty=3, score=20, tags=["散列表", "链地址", "同义词"],
    statement_md=(
        "表长 `m`，散列函数 `H(key) = key % p`，冲突用**链地址法**处理："
        "同义词挂一条链，新结点用**头插法**插进链头（教材 `Unsorted` 链的插法）。\n\n"
        "输出：\n\n"
        "1. `m` 行，桶 `i` 的链：`i: k1 k2 ...`（**链头在前**，即与插入顺序相反；"
        "空桶输出 `i:`）；\n"
        "2. 最后一行：成功查找 ASL = 每个键在**自己链上**的位置（1 基）之和 ÷ `n`，"
        "保留 2 位小数。\n\n"
        "★ 同一组教材键，链地址的 ASL（1.75）比线性探测（2.50）好看得多——"
        "代价是额外的指针空间。"
    ),
    input_format=(
        "第一行 `m p n`（表长、模数、键个数）。\n\n"
        "第二行 `n` 个互不相同的非负整数。"
    ),
    output_format=(
        "前 `m` 行：桶分布，格式 `i: k1 k2 ...`（链头在前，空桶为 `i:`）。\n\n"
        "第 `m+1` 行：成功查找 ASL，保留 2 位小数。"
    ),
    constraints_md="- 2 ≤ p ≤ m ≤ 100\n- 1 ≤ n ≤ 200\n- 0 ≤ key ≤ 10⁹",
    inputs=[
        "13 13 12\n19 14 23 1 68 20 84 27 55 11 10 79\n",
        "5 5 6\n0 5 10 15 20 25\n",
        "3 3 3\n1 4 7\n",
        "7 7 4\n2 9 16 23\n",
        "6 6 3\n12 18 6\n",
    ],
    samples=2,

    oracle=_oracle_39,

    solution=r'''#include <stdio.h>
#include <stdlib.h>
#define MAXM 105
typedef struct Node {
    long long v;
    struct Node *next;
} Node;
Node* bucket[MAXM];
long long keys[205];
int main(void) {
    int m, p, n;
    scanf("%d %d %d", &m, &p, &n);
    for (int k = 0; k < n; k++) {
        scanf("%lld", &keys[k]);
        int h = (int)(keys[k] % p);
        Node* q = (Node*)malloc(sizeof(Node));
        q->v = keys[k]; q->next = bucket[h];
        bucket[h] = q;                   /* 头插法 */
    }
    for (int i = 0; i < m; i++) {
        printf("%d:", i);
        for (Node* q = bucket[i]; q; q = q->next) printf(" %lld", q->v);
        printf("\n");
    }
    long long sum = 0;
    for (int k = 0; k < n; k++) {
        int pos = 1;
        for (Node* q = bucket[keys[k] % p]; q && q->v != keys[k]; q = q->next)
            pos++;
        sum += pos;
    }
    printf("%.2f\n", (double)sum / n);
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
/* 另一套：桶用 vector 顺序收，输出时 reverse；ASL 按「值在桶里的下标」算 */
int main() {
    int m, p, n; cin >> m >> p >> n;
    vector<vector<long long>> buck(m);
    vector<long long> keys(n);
    for (int k = 0; k < n; k++) {
        cin >> keys[k];
        buck[keys[k] % p].push_back(keys[k]);
    }
    for (int i = 0; i < m; i++) {
        vector<long long> r = buck[i];
        reverse(r.begin(), r.end());     // 头插法效果
        cout << i << ":";
        for (long long v : r) cout << " " << v;
        cout << "\n";
    }
    long long sum = 0;
    for (int k = 0; k < n; k++) {
        const vector<long long>& b = buck[keys[k] % p];
        int pos = 0;
        while (b[pos] != keys[k]) pos++;
        sum += (int)b.size() - pos;      // reverse 后的位置 = 链上位序
    }
    printf("%.2f\n", (double)sum / n);
    return 0;
}
''',
)


# --------------------------------------------------------------------- #
#  第 08 讲 · 排序
# --------------------------------------------------------------------- #

def _oracle_40(text: str) -> str:
    d = text.split()
    n = int(d[0])
    a = [int(v) for v in d[1:1 + n]]
    lines, t = [], 0
    for i in range(n - 1):
        swapped = False
        for j in range(n - i - 1):       # 每趟少比一个：最大值已沉底
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        t += 1
        lines.append(" ".join(map(str, a)))
        if not swapped:
            break                        # 提前终止：这趟没交换 = 已经有序
    return "\n".join(lines) + "\n%d\n" % t

add(
    title="冒泡排序：逐趟输出",
    section="第 08 讲 · 排序",
    difficulty=2, score=15, tags=["冒泡", "交换排序", "提前终止"],
    statement_md=(
        "对 `n` 个整数做**冒泡排序**（升序），把**每一趟结束后的序列**都打出来。\n\n"
        "★ 口径（教材写法）：第 `i` 趟（`i` 从 1 起）让下标 `j` 从 `0` 扫到 "
        "`n-i-1`，`a[j] > a[j+1]` 就交换。**用严格大于**——相等的元素不交换，"
        "这正是冒泡「稳定」的原因。\n\n"
        "某趟一次交换都没发生就**提前终止**，且这趟本身要输出（它是最后一行）。"
        "最后一行输出实际执行的趟数。"
    ),
    input_format=(
        "第一行 `n`（2 ≤ n，元素互异性不保证——相等元素不影响确定性）。\n\n"
        "第二行 `n` 个整数。"
    ),
    output_format=(
        "若干行：每趟结束后的序列（空格分隔），最后一趟之后再输出一行趟数。"
    ),
    constraints_md="- 2 ≤ n ≤ 1000\n- |元素| ≤ 10⁹",
    inputs=[
        "5\n5 4 3 2 1\n",
        "5\n1 2 3 4 5\n",
        "6\n3 1 4 1 5 9\n",
        "4\n2 3 1 5\n",
        "7\n49 38 65 97 76 13 27\n",
    ],
    samples=2,

    oracle=_oracle_40,

    solution=r'''#include <stdio.h>
#define MAXN 1005
int a[MAXN];
int main(void) {
    int n;
    scanf("%d", &n);
    for (int k = 0; k < n; k++) scanf("%d", &a[k]);
    int rounds = 0;
    for (int i = 0; i < n - 1; i++) {
        int swapped = 0;
        for (int j = 0; j < n - i - 1; j++)
            if (a[j] > a[j + 1]) {
                int t = a[j]; a[j] = a[j + 1]; a[j + 1] = t;
                swapped = 1;
            }
        rounds++;
        for (int k = 0; k < n; k++)
            printf(k ? " %d" : "%d", a[k]);
        printf("\n");
        if (!swapped) break;             /* 提前终止 */
    }
    printf("%d\n", rounds);
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
using namespace std;
/* 另一套：「无交换就重来一遍」的写法——效果等价于带提前终止的冒泡 */
int main() {
    int n; cin >> n;
    vector<int> a(n);
    for (int &v : a) cin >> v;
    int rounds = 0;
    while (rounds < n - 1) {
        bool moved = false;
        for (int j = 0; j + 1 < n - rounds; j++)
            if (a[j] > a[j + 1]) { swap(a[j], a[j + 1]); moved = true; }
        rounds++;
        for (int k = 0; k < n; k++) cout << (k ? " " : "") << a[k];
        cout << "\n";
        if (!moved) break;
    }
    cout << rounds << "\n";
    return 0;
}
''',
)

def _oracle_41(text: str) -> str:
    d = text.split()
    n = int(d[0])
    a = [int(v) for v in d[1:1 + n]]
    pivot = a[0]
    low, high = 0, n - 1
    while low < high:
        while low < high and a[high] > pivot:
            high -= 1
        a[low] = a[high]
        while low < high and a[low] < pivot:
            low += 1
        a[high] = a[low]
    a[low] = pivot
    return " ".join(map(str, a)) + "\n%d\n" % (low + 1)

add(
    title="快速排序的一趟划分",
    section="第 08 讲 · 排序",
    difficulty=3, score=20, tags=["快速排序", "Partition", "枢轴"],
    statement_md=(
        "对 `n` 个**互不相同**的整数做快排的**第一趟划分**（教材双向扫描法），"
        "输出划分后的序列和枢轴最终落位。\n\n"
        "★ 口径（教材写法，一个字都不能变）：\n\n"
        "- 枢轴 `pivot = a[0]`（取**第一个**元素），`low=0`、`high=n-1`；\n"
        "- `high` 从右往左找第一个 **< pivot** 的元素，填到 `a[low]`；\n"
        "- `low` 从左往右找第一个 **> pivot** 的元素，填到 `a[high]`；\n"
        "- 反复直到 `low == high`，把枢轴放进去。\n\n"
        "位序输出为 **1 基**（`low+1`）。这一趟做完，枢轴左边的全比它小、"
        "右边的全比它大——它就位了，以后再也不动。"
    ),
    input_format=(
        "第一行 `n`。\n\n"
        "第二行 `n` 个互不相同的整数。"
    ),
    output_format=(
        "第一行：一趟划分后的序列（空格分隔）。\n\n"
        "第二行：枢轴最终位序（1 基）。"
    ),
    constraints_md="- 1 ≤ n ≤ 1000\n- 元素互不相同，|元素| ≤ 10⁹",
    inputs=[
        "8\n49 38 65 97 76 13 27 50\n",
        "5\n3 1 2 5 4\n",
        "1\n1\n",
        "2\n2 1\n",
        "6\n50 20 70 10 90 60\n",
    ],
    samples=2,

    oracle=_oracle_41,

    solution=r'''#include <stdio.h>
#define MAXN 1005
int a[MAXN];
int main(void) {
    int n;
    scanf("%d", &n);
    for (int k = 0; k < n; k++) scanf("%d", &a[k]);
    int pivot = a[0], low = 0, high = n - 1;
    while (low < high) {
        while (low < high && a[high] > pivot) high--;   /* 右找小 */
        a[low] = a[high];
        while (low < high && a[low] < pivot) low++;     /* 左找大 */
        a[high] = a[low];
    }
    a[low] = pivot;                      /* 枢轴就位 */
    for (int k = 0; k < n; k++) printf(k ? " %d" : "%d", a[k]);
    printf("\n%d\n", low + 1);
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
using namespace std;
/* 另一套：把「挖坑」改成「swap 对调」，落位序列与教材法完全一致 */
int main() {
    int n; cin >> n;
    vector<int> a(n);
    for (int &v : a) cin >> v;
    int pivot = a[0], low = 0, high = n - 1;
    while (low < high) {
        while (low < high && a[high] > pivot) high--;
        if (low < high) { a[low] = a[high]; }
        while (low < high && a[low] < pivot) low++;
        if (low < high) { a[high] = a[low]; }
    }
    a[low] = pivot;
    for (int k = 0; k < n; k++) cout << (k ? " " : "") << a[k];
    cout << "\n" << low + 1 << "\n";
    return 0;
}
''',
)

def _oracle_42(text: str) -> str:
    d = text.split()
    n = int(d[0])
    a = [0] + [int(v) for v in d[1:1 + n]]     # 1 基

    def sift(i, size):
        while True:
            c = 2 * i
            if c > size:
                break
            if c + 1 <= size and a[c + 1] > a[c]:
                c += 1                    # 挑较大的孩子
            if a[c] > a[i]:
                a[i], a[c] = a[c], a[i]
                i = c
            else:
                break

    for i in range(n // 2, 0, -1):        # 从最后一个非叶结点倒着建堆
        sift(i, n)
    heap = a[1:]
    size = n
    while size > 1:                       # 排序：堆顶与末尾交换后重沉
        a[1], a[size] = a[size], a[1]
        size -= 1
        sift(1, size)
    return " ".join(map(str, heap)) + "\n" + " ".join(map(str, a[1:])) + "\n"

add(
    title="堆排序：建大顶堆与排序结果",
    section="第 08 讲 · 排序",
    difficulty=3, score=20, tags=["堆排序", "大顶堆", "筛选"],
    statement_md=(
        "把 `n` 个**互不相同**的整数建成一棵**大顶堆**，再做堆排序。\n\n"
        "输出两行：\n\n"
        "1. **建成的堆**（1 基数组，即完全二叉树的层序）；\n"
        "2. 升序排序结果。\n\n"
        "★ 口径（教材写法）：堆用 1 起点的数组存（`i` 的孩子是 `2i`、`2i+1`，"
        "这就是全书「下标从 1 起」隐形坑的主场）；建堆从**最后一个非叶结点 "
        "`⌊n/2⌋** 倒着到 1 逐个**下沉筛选**；排序阶段每轮「堆顶与末尾交换 → "
        "堆大小减一 → 堆顶重新下沉」。\n\n"
        "想看反例的话：升序排序用**大顶**堆——新手十次有九次先想成小顶堆。"
    ),
    input_format=(
        "第一行 `n`。\n\n"
        "第二行 `n` 个互不相同的整数。"
    ),
    output_format=(
        "第一行：建成后的大顶堆（层序，空格分隔）。\n\n"
        "第二行：升序排序结果（空格分隔）。"
    ),
    constraints_md="- 1 ≤ n ≤ 1000\n- 元素互不相同，|元素| ≤ 10⁹",
    inputs=[
        "8\n49 38 65 97 76 13 27 50\n",
        "5\n1 2 3 4 5\n",
        "1\n7\n",
        "6\n12 5 9 20 3 15\n",
        "4\n4 3 2 1\n",
    ],
    samples=2,

    oracle=_oracle_42,

    solution=r'''#include <stdio.h>
#define MAXN 1005
int h[MAXN];
void sift(int i, int size) {             /* 迭代下沉 */
    while (1) {
        int c = 2 * i;
        if (c > size) break;
        if (c + 1 <= size && h[c + 1] > h[c]) c++;
        if (h[c] > h[i]) { int t = h[i]; h[i] = h[c]; h[c] = t; i = c; }
        else break;
    }
}
int main(void) {
    int n;
    scanf("%d", &n);
    for (int k = 1; k <= n; k++) scanf("%d", &h[k]);
    for (int i = n / 2; i >= 1; i--) sift(i, n);
    for (int k = 1; k <= n; k++) printf(k > 1 ? " %d" : "%d", h[k]);
    printf("\n");
    int size = n;                        /* 排序：堆顶换末尾后重沉 */
    while (size > 1) {
        int t = h[1]; h[1] = h[size]; h[size] = t;
        size--;
        sift(1, size);
    }
    for (int k = 1; k <= n; k++) printf(k > 1 ? " %d" : "%d", h[k]);
    printf("\n");
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
using namespace std;
/* 另一套：递归版下沉 + 边排边输出 */
vector<int> h;
void sift(int i, int size) {
    int c = 2 * i;
    if (c > size) return;
    if (c + 1 <= size && h[c + 1] > h[c]) c++;
    if (h[c] > h[i]) { swap(h[i], h[c]); sift(c, size); }
}
int main() {
    int n; cin >> n;
    h.assign(n + 1, 0);
    for (int k = 1; k <= n; k++) cin >> h[k];
    for (int i = n / 2; i >= 1; i--) sift(i, n);
    vector<int> built(h.begin() + 1, h.end());
    for (size_t k = 0; k < built.size(); k++) cout << (k ? " " : "") << built[k];
    cout << "\n";
    for (int size = n; size > 1; size--) {
        swap(h[1], h[size]);
        sift(1, size - 1);
    }
    for (int k = 1; k <= n; k++) cout << (k > 1 ? " " : "") << h[k];
    cout << "\n";
    return 0;
}
''',
)

def _oracle_43(text: str) -> str:
    d = text.split()
    n = int(d[0])
    a = [int(v) for v in d[1:1 + n]]
    out, w = [], 1
    while w < n:
        b = []
        for i in range(0, n, 2 * w):
            L = a[i:i + w]
            R = a[i + w:i + 2 * w]
            p = q = 0
            while p < len(L) and q < len(R):
                if L[p] <= R[q]:          # 相等取左段 = 归并的稳定性
                    b.append(L[p]); p += 1
                else:
                    b.append(R[q]); q += 1
            b.extend(L[p:]); b.extend(R[q:])
        a = b
        out.append(" ".join(map(str, a)))
        w *= 2
    return "\n".join(out) + "\n"

add(
    title="二路归并排序：逐趟输出（非递归）",
    section="第 08 讲 · 排序",
    difficulty=3, score=20, tags=["归并排序", "分治", "稳定性"],
    statement_md=(
        "对 `n` 个整数做**非递归**的二路归并排序（升序），输出**每一趟**结束后"
        "的序列。\n\n"
        "★ 口径：`width` 从 1 开始，每趟把 `[0..n)` 按 `2*width` 分组，"
        "组内 `[i, i+width)` 与 `[i+width, i+2*width)` 两段归并"
        "（右段不足整段就原样保留）；`width ≥ n` 时结束。"
        "**归并时两边相等取左段**——这就是归并排序稳定的实现根据。\n\n"
        "和递归版「先分后合」不同，非递归版**自底向上**：第 1 趟 length-1 有序段"
        "两两归并出 length-2，第 2 趟出 length-4……趟数就是 `⌈log₂n⌉`。"
    ),
    input_format=(
        "第一行 `n`（2 ≤ n，元素可重复）。\n\n"
        "第二行 `n` 个整数。"
    ),
    output_format=(
        "若干行：第 `k` 趟结束后的完整序列（空格分隔），"
        "共 `⌈log₂n⌉` 行。"
    ),
    constraints_md="- 2 ≤ n ≤ 1000\n- |元素| ≤ 10⁹",
    inputs=[
        "10\n49 38 65 97 76 13 27 50 5 62\n",
        "2\n2 1\n",
        "5\n3 1 2 5 4\n",
        "8\n8 7 6 5 4 3 2 1\n",
        "6\n2 2 1 1 3 3\n",
    ],
    samples=2,

    oracle=_oracle_43,

    solution=r'''#include <stdio.h>
#define MAXN 1005
int a[MAXN], b[MAXN];
int main(void) {
    int n;
    scanf("%d", &n);
    for (int k = 0; k < n; k++) scanf("%d", &a[k]);
    for (int w = 1; w < n; w *= 2) {
        int len = 0;
        for (int i = 0; i < n; i += 2 * w) {
            int p = i, q = i + w, pe = i + w, qe = i + 2 * w;
            if (pe > n) pe = n;
            if (qe > n) qe = n;
            while (p < pe && q < qe)
                b[len++] = (a[p] <= a[q]) ? a[p++] : a[q++];
            while (p < pe) b[len++] = a[p++];
            while (q < qe) b[len++] = a[q++];
        }
        for (int k = 0; k < n; k++) a[k] = b[k];
        for (int k = 0; k < n; k++) printf(k ? " %d" : "%d", a[k]);
        printf("\n");
    }
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
using namespace std;
/* 另一套：in-place merge 用「切开重拼」的思路，先拷左段再按序插右段 */
int main() {
    int n; cin >> n;
    vector<int> a(n);
    for (int &v : a) cin >> v;
    for (int w = 1; w < n; w *= 2) {
        vector<int> nxt;
        for (int i = 0; i < n; i += 2 * w) {
            vector<int> L(a.begin() + i, a.begin() + min(i + w, n));
            vector<int> R(a.begin() + min(i + w, n),
                          a.begin() + min(i + 2 * w, n));
            size_t p = 0, q = 0;
            while (p < L.size() && q < R.size())
                nxt.push_back(L[p] <= R[q] ? L[p++] : R[q++]);
            while (p < L.size()) nxt.push_back(L[p++]);
            while (q < R.size()) nxt.push_back(R[q++]);
        }
        a = nxt;
        for (int k = 0; k < n; k++) cout << (k ? " " : "") << a[k];
        cout << "\n";
    }
    return 0;
}
''',
)


# --------------------------------------------------------------------- #
#  第 02 / 03 讲扩充：经典题型批次（顺序表 / 链表 / 栈和队列），难度递进
# --------------------------------------------------------------------- #

def _oracle_44(text: str) -> str:
    d = text.split()
    n = int(d[0])
    return " ".join(d[1:1 + n]) + "\n"

add(
    title="顺序表的建立及遍历",
    section="第 02 讲 · 线性表",
    difficulty=1, score=10, tags=["顺序表", "建表", "遍历"],
    statement_md=(
        "把 `n` 个整数依次存入顺序表（**尾插法**：读一个存一个，"
        "表尾追加），然后按存放顺序遍历输出。\n\n"
        "★ 这是所有顺序表题的「地基动作」：`SqList` 建表 → 遍历。"
        "后面对照着看：**头插法**建出来正好是反序（见「头插法创建单链表」一题）。"
    ),
    input_format="第一行 `n`（1 ≤ n）。第二行 `n` 个整数。",
    output_format="一行，`n` 个整数（空格分隔）。",
    constraints_md="- 1 ≤ n ≤ 1000\n- |元素| ≤ 10⁹",
    inputs=[
        "3\n1 2 3\n",
        "1\n-5\n",
        "4\n2 2 2 2\n",
        "5\n5 4 3 2 1\n",
    ],
    samples=2,
    oracle=_oracle_44,
    solution=r'''#include <stdio.h>
#define MAXN 1005
int a[MAXN];
int main(void) {
    int n;
    scanf("%d", &n);
    for (int k = 0; k < n; k++) scanf("%d", &a[k]);   /* 尾插 */
    for (int k = 0; k < n; k++) printf(k ? " %d" : "%d", a[k]);
    printf("\n");
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
using namespace std;
int main() {
    int n; cin >> n;
    vector<int> a;
    for (int k = 0; k < n; k++) { int v; cin >> v; a.push_back(v); }
    for (size_t k = 0; k < a.size(); k++) cout << (k ? " " : "") << a[k];
    cout << "\n";
    return 0;
}
''',
)

def _oracle_45(text: str) -> str:
    d = text.split()
    n = int(d[0])
    a = [int(v) for v in d[1:1 + n]]
    x = int(d[1 + n])
    i = 0
    while i < n and a[i] <= x:
        i += 1
    a.insert(i, x)
    return " ".join(map(str, a)) + "\n"

add(
    title="递增有序顺序表的插入（保持有序）",
    section="第 02 讲 · 线性表",
    difficulty=1, score=10, tags=["顺序表", "有序插入", "搬移"],
    statement_md=(
        "在**严格递增**的顺序表里插入 `x`，插完后**仍然递增**。\n\n"
        "★ 和「按位插入」的区别：位置不告诉你，得自己找——从前往后扫，"
        "找到第一个**大于 x** 的位置就是插入点（等值元素插在它们**后面**）。"
        "找位置 O(n)、搬移 O(n)，先找后搬一步都不能少。"
    ),
    input_format=(
        "第一行 `n`。\n\n第二行 `n` 个严格递增的整数。\n\n第三行 `x`。"
    ),
    output_format="一行，插入后仍递增的表（空格分隔）。",
    constraints_md="- 1 ≤ n ≤ 1000\n- |元素|、|x| ≤ 10⁹",
    inputs=[
        "5\n1 3 5 7 9\n6\n",
        "5\n1 3 5 7 9\n0\n",
        "5\n1 3 5 7 9\n10\n",
        "3\n2 2 2\n2\n",
        "1\n7\n7\n",
    ],
    samples=2,
    oracle=_oracle_45,
    solution=r'''#include <stdio.h>
#define MAXN 1005
int a[MAXN];
int main(void) {
    int n, x;
    scanf("%d", &n);
    for (int k = 0; k < n; k++) scanf("%d", &a[k]);
    scanf("%d", &x);
    int i = 0;
    while (i < n && a[i] <= x) i++;      /* 第一个 > x 的位置 */
    for (int j = n - 1; j >= i; j--) a[j + 1] = a[j];   /* 从后往前搬 */
    a[i] = x;
    for (int k = 0; k <= n; k++) printf(k ? " %d" : "%d", a[k]);
    printf("\n");
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
using namespace std;
/* 另一套：新开结果表，边扫边落，x 落一次 */
int main() {
    int n, x; cin >> n;
    vector<int> a(n), b;
    for (int &v : a) cin >> v;
    cin >> x;
    bool placed = false;
    for (int v : a) {
        if (!placed && x < v) { b.push_back(x); placed = true; }
        b.push_back(v);
    }
    if (!placed) b.push_back(x);         // 比谁都大 / 表里全相等
    for (size_t k = 0; k < b.size(); k++) cout << (k ? " " : "") << b[k];
    cout << "\n";
    return 0;
}
''',
)

def _oracle_46(text: str) -> str:
    d = text.split()
    n, m = int(d[0]), int(d[1])
    a = [int(v) for v in d[2:2 + n]]
    b = [int(v) for v in d[2 + n:2 + n + m]]
    out, i, j = [], 0, 0
    while i < n and j < m:
        if a[i] <= b[j]:
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1
    out.extend(a[i:]); out.extend(b[j:])
    return " ".join(map(str, out)) + "\n"

add(
    title="合并有序数组",
    section="第 02 讲 · 线性表",
    difficulty=1, score=10, tags=["归并", "双指针", "有序表"],
    statement_md=(
        "两个**非递减**数组 `a`（长 `n`）和 `b`（长 `m`），合并成一个"
        "**非递减**数组，不许先拼起来再排序——用**双指针**一次扫完。\n\n"
        "★ 相等时取 `a` 的（`<=` 归左边）——这就是归并排序「稳定」的同一套写法，"
        "第 08 讲的归并题里还会见到它。"
    ),
    input_format=(
        "第一行 `n m`（n、m 允许为 0）。\n\n"
        "第二行 `a` 的 `n` 个非递减整数（可为空行）。\n\n"
        "第三行 `b` 的 `m` 个非递减整数（可为空行）。"
    ),
    output_format="一行，合并后的非递减数组（空表合并结果为空行）。",
    constraints_md="- 0 ≤ n, m ≤ 1000\n- |元素| ≤ 10⁹",
    inputs=[
        "3 3\n1 3 5\n2 4 6\n",
        "2 2\n1 1\n1 1\n",
        "1 1\n9\n1\n",
        "4 0\n1 2 3 4\n\n",
        "0 3\n\n5 6 7\n",
    ],
    samples=2,
    oracle=_oracle_46,
    solution=r'''#include <stdio.h>
#define MAXN 2005
int a[MAXN], b[MAXN];
int main(void) {
    int n, m;
    scanf("%d %d", &n, &m);
    for (int k = 0; k < n; k++) scanf("%d", &a[k]);
    for (int k = 0; k < m; k++) scanf("%d", &b[k]);
    int i = 0, j = 0, first = 1;
    while (i < n && j < m) {
        if (a[i] <= b[j]) printf(first ? "%d" : " %d", a[i++]);
        else              printf(first ? "%d" : " %d", b[j++]);
        first = 0;
    }
    while (i < n) { printf(first ? "%d" : " %d", a[i++]); first = 0; }
    while (j < m) { printf(first ? "%d" : " %d", b[j++]); first = 0; }
    printf("\n");
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
using namespace std;
/* 另一套：哨兵法——两表各补一个 +∞，循环 n+m 次，每轮挑小的（归并排序原味） */
int main() {
    int n, m; cin >> n >> m;
    vector<int> a(n), b(m);
    for (int &v : a) cin >> v;
    for (int &v : b) cin >> v;
    a.push_back(2000000000); b.push_back(2000000000);
    vector<int> out;
    int i = 0, j = 0;
    for (int k = 0; k < n + m; k++) {
        if (a[i] <= b[j]) { out.push_back(a[i]); i++; }
        else { out.push_back(b[j]); j++; }
    }
    for (size_t k = 0; k < out.size(); k++) cout << (k ? " " : "") << out[k];
    cout << "\n";
    return 0;
}
''',
)

def _oracle_47(text: str) -> str:
    d = text.split()
    n, k = int(d[0]), int(d[1])
    a = [int(v) for v in d[2:2 + n]]
    k %= n if n else 0
    a = a[-k:] + a[:-k] if k else a
    return " ".join(map(str, a)) + "\n"

add(
    title="数组元素循环右移 n 位",
    section="第 02 讲 · 线性表",
    difficulty=2, score=15, tags=["循环移位", "数组", "下标变换"],
    statement_md=(
        "把长度为 `n` 的数组**循环右移 `k` 位**：每个元素后移 `k` 格，"
        "移出右端的绕回左端。\n\n"
        "★ 两个坑：① `k` 可能比 `n` 大，先 `k %= n`；② `k % n == 0` 时"
        "数组**原样不动**——直接按 `a[-k:] + a[:-k]` 切片写，k=0 时会算出"
        "整个数组的两倍拼接，记得特判。\n\n"
        "三次逆置法（教材延伸）：逆置前 n-k 位 → 逆置后 k 位 → 整体逆置，"
        "原地 O(1) 空间完成，值得手玩一遍。"
    ),
    input_format="第一行 `n k`。第二行 `n` 个整数。",
    output_format="一行，右移后的数组（空格分隔）。",
    constraints_md="- 1 ≤ n ≤ 1000\n- 0 ≤ k ≤ 10⁹",
    inputs=[
        "5 2\n1 2 3 4 5\n",
        "5 7\n1 2 3 4 5\n",
        "5 5\n1 2 3 4 5\n",
        "1 100\n9\n",
        "3 1\n7 8 9\n",
    ],
    samples=2,
    oracle=_oracle_47,
    solution=r'''#include <stdio.h>
#define MAXN 1005
int a[MAXN];
void rev(int l, int r) {                 /* 逆置 a[l..r]（闭区间） */
    while (l < r) { int t = a[l]; a[l] = a[r]; a[r] = t; l++; r--; }
}
int main(void) {
    int n, k;
    scanf("%d %d", &n, &k);
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    k %= n;
    if (k) {                             /* 三次逆置法：原地完成 */
        rev(0, n - k - 1);
        rev(n - k, n - 1);
        rev(0, n - 1);
    }
    for (int i = 0; i < n; i++) printf(i ? " %d" : "%d", a[i]);
    printf("\n");
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
using namespace std;
/* 另一套：直接按下标映射——新位置 (i + k) % n，O(n) 空间换直白 */
int main() {
    int n, k; cin >> n >> k;
    vector<int> a(n), b(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    k %= n;
    for (int i = 0; i < n; i++) b[(i + k) % n] = a[i];
    for (int i = 0; i < n; i++) cout << (i ? " " : "") << b[i];
    cout << "\n";
    return 0;
}
''',
)

def _oracle_48(text: str) -> str:
    d = text.split()
    n = int(d[0])
    a = [int(v) for v in d[1:1 + n]]
    best, cur = 0, 0
    for v in a:
        cur = cur + v if cur > 0 else v
        if cur > best:
            best = cur
    return "%d\n" % best

add(
    title="最大子列和问题",
    section="第 02 讲 · 线性表",
    difficulty=2, score=15, tags=["最大子列和", "Kadane", "动态规划"],
    statement_md=(
        "在 `n` 个整数（可正可负）里找**连续**子列，使和最大，输出这个最大和。\n\n"
        "★ 口径：**允许空子列**——全负数时输出 `0`（一个元素都不选也是合法子列）。\n\n"
        "Kadane 思想：从头扫，`cur` 记「以当前元素结尾的最大子列和」——"
        "前缀和是负数就**果断丢弃重开**（`cur = max(v, cur + v)` 的手写版），"
        "`best` 只记历史最高。O(n) 一趟完事，枚举所有起止点的 O(n³)/O(n²) "
        "都能被它秒。"
    ),
    input_format="第一行 `n`。第二行 `n` 个整数。",
    output_format="一行，最大子列和（全负输出 `0`）。",
    constraints_md="- 1 ≤ n ≤ 100000\n- |元素| ≤ 1000",
    inputs=[
        "6\n-2 11 -4 13 -5 -2\n",
        "4\n-1 -2 -3 -4\n",
        "1\n5\n",
        "5\n1 2 3 4 5\n",
        "8\n4 -3 5 -2 -1 2 6 -2\n",
    ],
    samples=2,
    oracle=_oracle_48,
    solution=r'''#include <stdio.h>
#define MAXN 100005
int a[MAXN];
int main(void) {
    int n;
    scanf("%d", &n);
    for (int k = 0; k < n; k++) scanf("%d", &a[k]);
    long long best = 0, cur = 0;
    for (int k = 0; k < n; k++) {
        cur = (cur > 0) ? cur + a[k] : a[k];   /* 负前缀果断丢 */
        if (cur > best) best = cur;
    }
    printf("%lld\n", best);
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
using namespace std;
/* 另一套：前缀和视角——最大子列和 = max(前缀和) - min(此前前缀和)，前缀里自带空子列(0) */
int main() {
    int n; cin >> n;
    long long run = 0, mn = 0, best = 0;
    for (int k = 0; k < n; k++) {
        long long v; cin >> v;
        run += v;
        if (run - mn > best) best = run - mn;
        if (run < mn) mn = run;
    }
    cout << best << "\n";
    return 0;
}
''',
)

def _oracle_49(text: str) -> str:
    words = text.split()
    return " ".join(reversed(words)) + "\n"

add(
    title="单词逆置",
    section="第 02 讲 · 线性表",
    difficulty=2, score=15, tags=["字符串", "逆置", "分词"],
    statement_md=(
        "把一行英文里的**单词顺序颠倒**：输入 `hello world`，输出 "
        "`world hello`。\n\n"
        "★ 口径：单词间可能**有多个空格**、首尾也可能有空格——输出一律"
        "以**单个空格**分隔，没有多余空白；整行没有单词就输出空行。\n\n"
        "用栈想最自然：单词一个个**进栈**，再逐个**出栈**拼接——"
        "后进先出天然就是逆序。"
    ),
    input_format="一行英文（长度 ≤ 10000，只含空格和大小写字母）。",
    output_format="一行，单词顺序颠倒、单空格分隔；无单词则为空行。",
    constraints_md="- 1 ≤ 单词数 ≤ 2000",
    inputs=[
        "hello world\n",
        "  the   quick  fox \n",
        "one\n",
        "  \n",
        "a b a\n",
    ],
    samples=2,
    oracle=_oracle_49,
    solution=r'''#include <stdio.h>
#include <string.h>
#include <ctype.h>
int main(void) {
    char line[10005];
    if (!fgets(line, sizeof line, stdin)) { printf("\n"); return 0; }
    /* 扫一遍：一个单词 = 一段连续字母，找到就从末尾倒着写 */
    char *w[2005];
    int cnt = 0;
    for (char *p = line; *p; ) {
        while (*p && isspace((unsigned char)*p)) p++;
        if (!*p) break;
        w[cnt++] = p;
        while (*p && !isspace((unsigned char)*p)) p++;
        if (*p) *p++ = '\0';
    }
    for (int k = cnt - 1; k >= 0; k--)
        printf(k == cnt - 1 ? "%s" : " %s", w[k]);
    printf("\n");
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <sstream>
#include <stack>
#include <string>
using namespace std;
/* 另一套：正经用栈——单词进栈，出栈拼接（后进先出 = 逆序） */
int main() {
    string line;
    if (!getline(cin, line)) { cout << "\n"; return 0; }
    istringstream in(line);
    stack<string> st;
    string w;
    while (in >> w) st.push(w);
    bool first = true;
    while (!st.empty()) {
        if (!first) cout << " ";
        cout << st.top();
        st.pop();
        first = false;
    }
    cout << "\n";
    return 0;
}
''',
)

def _oracle_50(text: str) -> str:
    d = text.split()
    n = int(d[0])
    a = [int(v) for v in d[1:1 + n]]
    return " ".join(map(str, reversed(a))) + "\n"

add(
    title="头插法创建单链表、遍历链表",
    section="第 02 讲 · 线性表",
    difficulty=1, score=10, tags=["单链表", "头插法", "遍历"],
    statement_md=(
        "读 `n` 个整数，按输入顺序用**头插法**建一条带头结点的单链表，"
        "再从头到尾遍历输出。\n\n"
        "★ 头插法 = 新结点总插在**表头**，建好后结点次序与输入**正好相反**"
        "（理论题考过的同款结论）。想输出与输入同序，得用尾插法——"
        "或者干脆建完再**就地逆置**（下一题）。"
    ),
    input_format="第一行 `n`。第二行 `n` 个整数（按插入顺序给出）。",
    output_format="一行，遍历链表得到的 `n` 个整数（与输入顺序相反）。",
    constraints_md="- 1 ≤ n ≤ 1000",
    inputs=[
        "4\n1 2 3 4\n",
        "1\n9\n",
        "3\n5 5 5\n",
        "6\n1 2 3 4 5 6\n",
    ],
    samples=2,
    oracle=_oracle_50,
    solution=r'''#include <stdio.h>
#include <stdlib.h>
typedef struct Lnode {
    int v;
    struct Lnode *next;
} Lnode;
int main(void) {
    int n;
    scanf("%d", &n);
    Lnode head; head.next = NULL;          /* 带头结点 */
    for (int k = 0; k < n; k++) {
        int v; scanf("%d", &v);
        Lnode *p = (Lnode*)malloc(sizeof(Lnode));
        p->v = v;
        p->next = head.next;               /* 头插：插在首元结点前 */
        head.next = p;
    }
    int first = 1;
    for (Lnode *p = head.next; p; p = p->next) {
        printf(first ? "%d" : " %d", p->v);
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
/* 另一套：不用指针，vector 顺序收 + reverse（头插法的效果） */
int main() {
    int n; cin >> n;
    vector<int> a;
    for (int k = 0; k < n; k++) { int v; cin >> v; a.push_back(v); }
    reverse(a.begin(), a.end());
    for (size_t k = 0; k < a.size(); k++) cout << (k ? " " : "") << a[k];
    cout << "\n";
    return 0;
}
''',
)

def _oracle_51(text: str) -> str:
    d = text.split()
    a, b = [], []
    cur = a
    for tok in d:
        v = int(tok)
        if v == -1:
            cur = b
            continue
        cur.append(v)
    out, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1
    out.extend(a[i:]); out.extend(b[j:])
    return " ".join(map(str, out)) + "\n"

add(
    title="两个有序链表序列的合并",
    section="第 02 讲 · 线性表",
    difficulty=2, score=15, tags=["单链表", "合并", "哨兵结点"],
    statement_md=(
        "两条**非递减**的单链表 `L1`、`L2`（各以 `-1` 结尾，链表可以有空表），"
        "合并成一条**非递减**链表并输出。\n\n"
        "★ 教材做法：设一个**哨兵/哑结点**当结果链表的头，两路指针比大小，"
        "小的摘下来接到结果尾部——**不许新建结点**，重组现有指针。"
        "相等时取 `L1` 的。这题就是 PTA 经典「数据结构」开篇题的口吻。"
    ),
    input_format=(
        "两行：第一行 `L1` 的元素（`-1` 结尾），第二行 `L2` 的元素（`-1` 结尾）。"
        "元素非递减；`-1` 只作结束标志。"
    ),
    output_format="一行，合并后的非递减序列（空格分隔；两表全空则为空行）。",
    constraints_md="- 链表长度 0 ≤ len ≤ 1000\n- |元素| ≤ 10⁹",
    inputs=[
        "1 3 5 -1\n2 4 6 -1\n",
        "-1\n1 2 -1\n",
        "1 1 -1\n1 -1\n",
        "3 1 2 -1\n-1\n",
        "-1\n-1\n",
    ],
    samples=2,
    oracle=_oracle_51,
    solution=r'''#include <stdio.h>
#include <stdlib.h>
typedef struct Lnode { int v; struct Lnode *next; } Lnode;
Lnode* build(void) {                     /* 尾插建表，返回首元指针（NULL = 空表） */
    Lnode *h = NULL, *t = NULL;
    int v;
    while (scanf("%d", &v) == 1 && v != -1) {
        Lnode *p = (Lnode*)malloc(sizeof(Lnode));
        p->v = v; p->next = NULL;
        if (t) t->next = p; else h = p;
        t = p;
    }
    return h;
}
int main(void) {
    Lnode *a = build(), *b = build();
    Lnode dummy; Lnode *tail = &dummy;   /* 哑结点收结果 */
    dummy.next = NULL;
    while (a && b) {
        if (a->v <= b->v) { tail->next = a; a = a->next; }
        else              { tail->next = b; b = b->next; }
        tail = tail->next;
    }
    tail->next = a ? a : b;
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
/* 另一套：读入同款，合并改用「先接 a 剩余再穿插」的朴素双数组写法 */
int main() {
    vector<int> a, b;
    int v;
    auto read = [&](vector<int>& s) {
        while (cin >> v && v != -1) s.push_back(v);
    };
    read(a); read(b);
    vector<int> out;
    size_t i = 0, j = 0;
    while (i < a.size() && j < b.size())
        out.push_back(a[i] <= b[j] ? a[i++] : b[j++]);
    while (i < a.size()) out.push_back(a[i++]);
    while (j < b.size()) out.push_back(b[j++]);
    for (size_t k = 0; k < out.size(); k++) cout << (k ? " " : "") << out[k];
    cout << "\n";
    return 0;
}
''',
)

def _oracle_52(text: str) -> str:
    d = text.split()
    n, m = int(d[0]), int(d[1])
    people = list(range(1, n + 1))
    idx = 0
    out = []
    while people:
        idx = (idx + m - 1) % len(people)
        out.append(people.pop(idx))
    return " ".join(map(str, out)) + "\n"

add(
    title="约瑟夫环",
    section="第 02 讲 · 线性表",
    difficulty=2, score=15, tags=["约瑟夫", "环形", "模拟"],
    statement_md=(
        "`n` 个人围成一圈，编号 `1..n`。从编号 1 的开始**报数**，报到 `m` 的"
        "人出圈，下一个人从 1 重新报数——输出全部出圈顺序。\n\n"
        "★ 数据结构味最浓的写法是**循环链表**：删结点 = 前驱 `next` 跨过去。"
        "用数组模拟等价：出圈下标 `idx = (idx + m - 1) % 剩余人数`，"
        "删掉后**原地接着**从「刚出圈那位的位置」继续数。\n\n"
        "几个边界心里过一遍：`m=1` 就是按编号顺序全出；`n=1` 直接出自己；"
        "`m` 比人数大会绕圈（取模兜底）。"
    ),
    input_format="一行 `n m`（1 ≤ n ≤ 1000，1 ≤ m ≤ 10⁹）。",
    output_format="一行，`n` 个出圈编号（空格分隔）。",
    constraints_md="- 1 ≤ n ≤ 1000\n- 1 ≤ m ≤ 10⁹",
    inputs=[
        "5 3\n",
        "7 2\n",
        "5 1\n",
        "1 7\n",
        "6 5\n",
    ],
    samples=2,
    oracle=_oracle_52,
    solution=r'''#include <stdio.h>
#define MAXN 1005
int a[MAXN];                             /* a[i]：0 基，1 = 还在圈内 */
int main(void) {
    int n, m;
    scanf("%d %d", &n, &m);
    for (int i = 0; i < n; i++) a[i] = 1;
    int left = n, idx = 0, first = 1;    /* idx：当前报数人的下标（0 基） */
    while (left) {
        /* m 可达 1e9，先按剩余人数折算步长：报 m = 绕 alive 圈后的 step */
        int step = (int)((long long)m % left);
        if (!step) step = left;
        int cnt = 0;
        while (1) {
            if (a[idx]) cnt++;           /* 在圈内的才计数 */
            if (cnt == step) break;
            idx = (idx + 1) % n;
        }
        a[idx] = 0;
        printf(first ? "%d" : " %d", idx + 1);
        first = 0;
        left--;
        if (!left) break;
        do { idx = (idx + 1) % n; } while (!a[idx]);   /* 从下一位重新报 1 */
    }
    printf("\n");
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
#include <list>
using namespace std;
/* 另一套：list 模拟循环链表——迭代器绕圈，erase 返回下一个位置 */
int main() {
    int n, m; cin >> n >> m;
    list<int> ring;
    for (int i = 1; i <= n; i++) ring.push_back(i);
    auto it = ring.begin();
    bool first = true;
    while (!ring.empty()) {
        long long k = (long long)(m - 1) % (long long)ring.size();  /* m 可达 1e9，先折算 */
        for (long long c = 0; c < k; c++) {
            if (++it == ring.end()) it = ring.begin();
        }
        if (!first) cout << " ";
        cout << *it;
        first = false;
        it = ring.erase(it);             /* 出圈；erase 给的下一个位置接着报 1 */
        if (it == ring.end()) it = ring.begin();
    }
    cout << "\n";
    return 0;
}
''',
)

def _oracle_53(text: str) -> str:
    d = text.split()
    n = int(d[0])
    a = [int(v) for v in d[1:1 + n]]
    return " ".join(map(str, a)) + "\n" + " ".join(map(str, reversed(a))) + "\n"

add(
    title="单链表建表与就地逆置",
    section="第 02 讲 · 线性表",
    difficulty=2, score=15, tags=["单链表", "就地逆置", "指针"],
    statement_md=(
        "用**尾插法**建一条带头结点的单链表，先遍历输出一次；然后**就地逆置**"
        "（一个新结点都不许开，纯指针重排），再遍历输出一次。\n\n"
        "★ 就地逆置三指针套路（教材 2.5 的标准动作）：\n\n"
        "```c\np = 首元结点; 原表拆空;\nwhile (p) { q = p->next; p->next = 新表头后; 头插 p; p = q; }\n```\n\n"
        "本质 = 把结点按原序逐个**头插**进新链——练的就是「头插法反序」的"
        "指针手感。"
    ),
    input_format="第一行 `n`。第二行 `n` 个整数。",
    output_format=(
        "两行：第一行建表后的正序遍历；第二行就地逆置后的遍历。"
    ),
    constraints_md="- 1 ≤ n ≤ 1000",
    inputs=[
        "5\n1 2 3 4 5\n",
        "1\n8\n",
        "3\n1 1 2\n",
        "4\n-1 0 -1 3\n",
    ],
    samples=2,
    oracle=_oracle_53,
    solution=r'''#include <stdio.h>
#include <stdlib.h>
typedef struct Lnode { int v; struct Lnode *next; } Lnode;
int main(void) {
    int n;
    scanf("%d", &n);
    Lnode head; head.next = NULL;
    Lnode *tail = &head;                 /* 尾插建表 */
    for (int k = 0; k < n; k++) {
        int v; scanf("%d", &v);
        Lnode *p = (Lnode*)malloc(sizeof(Lnode));
        p->v = v; p->next = NULL;
        tail->next = p; tail = p;
    }
    int first = 1;
    for (Lnode *p = head.next; p; p = p->next) {
        printf(first ? "%d" : " %d", p->v); first = 0;
    }
    printf("\n");
    /* 就地逆置：摘下首元结点起的一串，逐个头插回 head */
    Lnode *p = head.next, *newhead = NULL;
    while (p) {
        Lnode *q = p->next;
        p->next = newhead;
        newhead = p;
        p = q;
    }
    head.next = newhead;
    first = 1;
    for (Lnode *p2 = head.next; p2; p2 = p2->next) {
        printf(first ? "%d" : " %d", p2->v); first = 0;
    }
    printf("\n");
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
/* 另一套：数组建表，双端翻转对照（行为等价；指针版的正确性由对拍保证） */
int main() {
    int n; cin >> n;
    vector<int> a(n);
    for (int &v : a) cin >> v;
    for (int k = 0; k < n; k++) cout << (k ? " " : "") << a[k];
    cout << "\n";
    reverse(a.begin(), a.end());
    for (int k = 0; k < n; k++) cout << (k ? " " : "") << a[k];
    cout << "\n";
    return 0;
}
''',
)

def _oracle_54(text: str) -> str:
    pairs = {')': '(', ']': '[', '}': '{'}
    st = []
    for ch in text.strip():
        if ch in "([{":
            st.append(ch)
        elif ch in pairs:
            if not st or st[-1] != pairs[ch]:
                return "no\n"
            st.pop()
    return "yes\n" if not st else "no\n"

add(
    title="括号匹配检验",
    section="第 03 讲 · 栈和队列",
    difficulty=1, score=10, tags=["栈", "括号匹配", "顺序栈应用"],
    statement_md=(
        "判断一行括号串（只含 `()[]{}` 六种字符）是否**匹配**："
        "每种左括号都有同类的右括号按正确顺序闭合。匹配输出 `yes`，否则 `no`。\n\n"
        "★ 栈的招牌应用（3.3.2 的第一个例子）：左括号**进栈**，碰到右括号就"
        "**弹栈对暗号**——弹出来的必须同类；最后栈必须是**空的**"
        "（不空 = 左括号多了）。三种失配全在这题里：类型对不上、右括号多了、"
        "左括号多了。"
    ),
    input_format="一行，仅由 `()[]{}` 组成的非空串（长度 ≤ 10000）。",
    output_format="一行，`yes` 或 `no`。",
    constraints_md="- 1 ≤ 串长 ≤ 10000",
    inputs=[
        "()[]{}\n",
        "([)]\n",
        "((\n",
        ")]\n",
        "{[()]}\n",
    ],
    samples=2,
    oracle=_oracle_54,
    solution=r'''#include <stdio.h>
#define MAXN 10005
char st[MAXN];
int main(void) {
    char line[MAXN];
    if (!fgets(line, sizeof line, stdin)) { printf("no\n"); return 0; }
    int top = -1, ok = 1;
    for (char *p = line; *p && ok; p++) {
        char c = *p;
        if (c == '(' || c == '[' || c == '{') st[++top] = c;
        else if (c == ')' || c == ']' || c == '}') {
            char want = (c == ')') ? '(' : (c == ']') ? '[' : '{';
            if (top < 0 || st[top] != want) ok = 0;
            else top--;
        }
        /* 其他字符忽略，防御性 */
    }
    printf(ok && top < 0 ? "yes\n" : "no\n");   /* 栈空才叫匹配完 */
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <stack>
#include <string>
using namespace std;
/* 另一套：map 存配对关系，STL 栈直译 */
int main() {
    string line;
    if (!getline(cin, line)) { cout << "no\n"; return 0; }
    string open = "([{", close = ")]}";
    stack<char> st;
    bool ok = true;
    for (char c : line) {
        size_t o = open.find(c), cl = close.find(c);
        if (o != string::npos) st.push(c);
        else if (cl != string::npos) {
            if (st.empty() || st.top() != open[cl]) { ok = false; break; }
            st.pop();
        }
    }
    cout << (ok && st.empty() ? "yes" : "no") << "\n";
    return 0;
}
''',
)

def _oracle_55(text: str) -> str:
    d = text.split()
    n, b = int(d[0]), int(d[1])
    if n == 0:
        return "0\n"
    digits = "0123456789ABCDEF"
    st = []
    while n:
        st.append(digits[n % b])
        n //= b
    return "".join(reversed(st)) + "\n"

add(
    title="进制转换",
    section="第 03 讲 · 栈和队列",
    difficulty=1, score=10, tags=["栈", "进制转换", "数制"],
    statement_md=(
        "把十进制非负整数 `n` 转成 `b` 进制（`2 ≤ b ≤ 16`），"
        "超过 9 的数字用**大写** `A`~`F`。\n\n"
        "★ 教材算法 3.1 的直译：反复 `n % b` **进栈**、`n /= b`，"
        "最后**出栈**拼串——除基取余倒序读，栈天生干这个。\n\n"
        "坑只有两个：`n = 0` 要特判输出 `0`（循环一次都不走）；"
        "字母是大写，`A` 不是 `a`。"
    ),
    input_format="一行 `n b`（0 ≤ n ≤ 10⁹，2 ≤ b ≤ 16）。",
    output_format="一行，`n` 的 `b` 进制表示（`n=0` 输出 `0`）。",
    constraints_md="- 0 ≤ n ≤ 10⁹\n- 2 ≤ b ≤ 16",
    inputs=[
        "0 2\n",
        "255 16\n",
        "100 2\n",
        "31 8\n",
        "1023 16\n",
        "16 16\n",
    ],
    samples=2,
    oracle=_oracle_55,
    solution=r'''#include <stdio.h>
int main(void) {
    long long n; int b;
    scanf("%lld %d", &n, &b);
    char st[40];
    int top = -1;
    if (n == 0) st[++top] = '0';         /* 特判：0 转几进制都是 0 */
    while (n) {
        int r = (int)(n % b);
        st[++top] = (char)(r < 10 ? '0' + r : 'A' + r - 10);
        n /= b;
    }
    while (top >= 0) putchar(st[top--]); /* 出栈 = 倒序读余数 */
    printf("\n");
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <stack>
#include <string>
using namespace std;
/* 另一套：递归版——先递归处理高位，再印当前位（系统栈替你倒序） */
void conv(long long n, int b) {
    if (!n) return;
    conv(n / b, b);
    int r = n % b;
    putchar(r < 10 ? '0' + r : 'A' + r - 10);
}
int main() {
    long long n; int b;
    cin >> n >> b;
    if (n == 0) cout << "0";
    else conv(n, b);
    cout << "\n";
    return 0;
}
''',
)

def _oracle_56(text: str) -> str:
    d = text.split()
    n = int(d[0])
    target = [int(v) for v in d[1:1 + n]]
    st, nxt = [], 1
    for want in target:
        while not st or st[-1] != want:
            if nxt > n:
                return "no\n"
            st.append(nxt)
            nxt += 1
        st.pop()
    return "yes\n"

add(
    title="出栈序列的合法性",
    section="第 03 讲 · 栈和队列",
    difficulty=2, score=15, tags=["栈", "出栈序列", "模拟"],
    statement_md=(
        "`1..n` 依次**进栈**（进栈和出栈可以任意交错），给定一个出栈序列，"
        "判断它是否合法。合法输出 `yes`，否则 `no`。\n\n"
        "★ 判定法：拿目标序列当清单，`1` 到 `n` 顺序进栈，**栈顶一等于目标"
        "就弹出**；某一步弹不出还进不进去，就是假序列。理论题里 "
        "「`3 1 2` 不可能」的通用版判法就是它。"
    ),
    input_format=(
        "第一行 `n`。\n\n第二行 `n` 个互不相同的整数（是 `1..n` 的一个排列）。"
    ),
    output_format="一行，`yes` 或 `no`。",
    constraints_md="- 1 ≤ n ≤ 1000",
    inputs=[
        "5\n1 2 3 4 5\n",
        "3\n3 1 2\n",
        "3\n3 2 1\n",
        "4\n2 1 4 3\n",
        "5\n5 4 3 2 1\n",
        "4\n4 1 2 3\n",
    ],
    samples=2,
    oracle=_oracle_56,
    solution=r'''#include <stdio.h>
#define MAXN 1005
int st[MAXN], target[MAXN];
int main(void) {
    int n, top = -1, nxt = 1;
    scanf("%d", &n);
    for (int k = 0; k < n; k++) scanf("%d", &target[k]);
    int ok = 1;
    for (int k = 0; k < n && ok; k++) {
        int want = target[k];
        while (top < 0 || st[top] != want) {
            if (nxt > n) { ok = 0; break; }   /* 进完还没有 = 假 */
            st[++top] = nxt++;
        }
        if (ok) top--;                        /* 弹出目标元素 */
    }
    printf(ok ? "yes\n" : "no\n");
    return 0;
}
''',
    alt=r'''#include <iostream>
#include <stack>
#include <vector>
using namespace std;
/* 另一套：反着走——枚举每次「先弹到弹不动为止」，弹的顺序必须恰好等于目标 */
int main() {
    int n; cin >> n;
    vector<int> t(n);
    for (int &v : t) cin >> v;
    stack<int> st;
    int nxt = 1, j = 0;
    while (j < n) {
        if (!st.empty() && st.top() == t[j]) { st.pop(); j++; continue; }
        if (nxt > n) break;
        st.push(nxt++);
    }
    cout << (j == n ? "yes" : "no") << "\n";
    return 0;
}
''',
)


# --------------------------------------------------------------------- #
#  理论题（第 01 / 06 / 07 / 08 讲的考概念部分）
#  - 用 app/bank_kit.py 的 mc / tf 造，line = "text"，浏览器本地判题同样支持
#  - verify_bank 对 line=text 的题不要求 alt_solution（答案本身跑得通即可）
# --------------------------------------------------------------------- #
#  第 04 讲扩充：串、数组和广义表经典题型（循序渐进 + 举一反三）
# --------------------------------------------------------------------- #

def _oracle_57(text: str) -> str:
    d = text.split()
    n = int(d[0])
    a = [int(v) for v in d[1:1 + n * n]]
    ok = True
    for i in range(n):
        for j in range(i + 1, n):
            if a[i * n + j] != a[j * n + i]:
                ok = False
                break
    return ("yes\n" if ok else "no\n")

add(
    title="判断对称矩阵",
    section="第 04 讲 · 串、数组和广义表",
    difficulty=1, score=10, tags=["数组", "对称矩阵", "二维数组"],
    statement_md=(
        "给定一个 `n` 阶方阵 `A`，判断它是否为**对称矩阵**（即对任意 "
        "`1 ≤ i, j ≤ n` 都满足 `A[i][j] == A[j][i]`）。\n\n"
        "★ 只需要检查**上三角**（`j > i`）的元素是否等于对应的下三角元素；"
        "主对角线元素 `A[i][i]` 天然等于自己，不用比。这是后面学习"
        "「对称矩阵压缩存储」的前置直觉。"
    ),
    input_format="第一行一个整数 `n`。\n\n随后 `n` 行，每行 `n` 个整数，表示矩阵 `A`。",
    output_format="一行，若是对称矩阵输出 `yes`，否则输出 `no`。",
    constraints_md="- 1 ≤ n ≤ 100\n- |A[i][j]| ≤ 10^9",
    inputs=[
        "3\n1 2 3\n2 4 5\n3 5 6\n",
        "3\n1 2 3\n2 4 5\n9 5 6\n",
        "1\n42\n",
        "4\n0 -1 2 3\n-1 5 0 4\n2 0 7 -2\n3 4 -2 9\n",
        "2\n1 2\n1 2\n",
    ],
    samples=2,
    oracle=_oracle_57,
    solution=r"""#include <stdio.h>
int a[105][105];
int main(void) {
    int n;
    scanf("%d", &n);
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            scanf("%d", &a[i][j]);
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            if (a[i][j] != a[j][i]) { printf("no\n"); return 0; }
    printf("yes\n");
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
using namespace std;
int main() {
    int n; cin >> n;
    vector<long long> a(n * n);
    for (int i = 0; i < n * n; i++) cin >> a[i];
    bool ok = true;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            if (a[i * n + j] != a[j * n + i]) ok = false;
    cout << (ok ? "yes\n" : "no\n");
    return 0;
}
""",
)

def _oracle_58(text: str) -> str:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    s, t = lines[0], lines[1]
    cnt = 0
    first = 0
    for i in range(len(s) - len(t) + 1):
        if s[i:i + len(t)] == t:
            cnt += 1
            if first == 0:
                first = i + 1
    return "%d %d\n" % (cnt, first)

add(
    title="统计子串",
    section="第 04 讲 · 串、数组和广义表",
    difficulty=1, score=10, tags=["串", "子串统计", "模式匹配"],
    statement_md=(
        "给定主串 `S` 和模式串 `T`，统计 `T` 在 `S` 中出现的**总次数**（**允许重叠**），"
        "以及首次出现的位置（从 1 开始计，未出现则为 `0`）。\n\n"
        "★ 对比「KMP 统计不重叠出现次数」：在 `S = aaaaa` 中找 `T = aa`，"
        "不重叠算 `2` 次，而**允许重叠**时起始位置 `1, 2, 3, 4` 全算，共 `4` 次。"
        "用 KMP 写允许重叠时，每次匹配成功后模式串指针不是清零，而是跳到 `next[m]`！"
    ),
    input_format="第一行主串 `S`（不含空格）。\n\n第二行模式串 `T`（不含空格，非空）。",
    output_format="一行两个整数，空格分隔：`出现总次数 首次位置`（未出现输出 `0 0`）。",
    constraints_md="- 1 ≤ |S|, |T| ≤ 10000",
    inputs=[
        "aaaaa\naa\n",
        "abababa\naba\n",
        "abcde\nxyz\n",
        "hello\nll\n",
        "abc\nabcde\n",
        "aaaa\na\n",
    ],
    samples=2,
    oracle=_oracle_58,
    solution=r"""#include <stdio.h>
#include <string.h>
char s[10005], t[10005];
int main(void) {
    scanf("%s %s", s, t);
    int n = (int)strlen(s), m = (int)strlen(t);
    int cnt = 0, first = 0;
    for (int i = 0; i + m <= n; i++) {
        if (strncmp(s + i, t, m) == 0) {
            cnt++;
            if (!first) first = i + 1;
        }
    }
    printf("%d %d\n", cnt, first);
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <string>
using namespace std;
int main() {
    string s, t; cin >> s >> t;
    int cnt = 0, first = 0;
    size_t pos = 0;
    while (true) {
        size_t k = s.find(t, pos);
        if (k == string::npos) break;
        cnt++;
        if (!first) first = (int)k + 1;
        pos = k + 1;    /* ★ 允许重叠：每次只前进 1 格 */
    }
    cout << cnt << " " << first << "\n";
    return 0;
}
""",
)

def _oracle_59(text: str) -> str:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    s = lines[0]
    q = int(lines[1])
    out = []
    for k in range(q):
        t = lines[2 + k]
        pos = s.find(t)
        out.append(s[pos:] if pos >= 0 else "Not Found")
    return "\n".join(out) + "\n"

add(
    title="字符串模式匹配（KMP）",
    section="第 04 讲 · 串、数组和广义表",
    difficulty=2, score=15, tags=["串", "KMP", "strstr"],
    statement_md=(
        "给定主串 `S` 和 `q` 个待查模式串 `T`，对每个模式串，在 `S` 中查找它首次出现的位置：\n\n"
        "- 若找到，输出从该位置一直到 `S` 末尾的子串（行为与 C 标准库的 `strstr(S, T)` 完全一致）；\n"
        "- 若找不到，输出 `Not Found`。\n\n"
        "★ 这是 PTA 数据结构题集里的经典原题：主串很长、查询有多次，"
        "对每个模式串先预处理 `next` 数组再做 KMP 扫描，每次查询都是线性的 `O(|S| + |T|)`。"
    ),
    input_format=(
        "第一行主串 `S`（不含空格）。\n\n"
        "第二行正整数 `q`（查询个数）。\n\n"
        "随后 `q` 行，每行一个非空模式串 `T`。"
    ),
    output_format="`q` 行，每行输出匹配位置起的后缀子串，或 `Not Found`。",
    constraints_md="- 1 ≤ |S| ≤ 100000\n- 1 ≤ q ≤ 20\n- 1 ≤ |T| ≤ 10000",
    inputs=[
        "abcabcabcd\n3\nabcabcd\nabcx\ncd\n",
        "ababababca\n2\nababca\nxyz\n",
        "aaaaaa\n2\naaa\naaaaaaa\n",
        "datastructure\n3\nstruct\ndata\nalgo\n",
    ],
    samples=2,
    oracle=_oracle_59,
    solution=r"""#include <stdio.h>
#include <string.h>
char s[100005], t[10005];
int nxt[10005];
int kmp_find(const char *s, int n, const char *t, int m) {
    nxt[0] = -1;
    int i = 0, j = -1;
    while (i < m) {
        if (j == -1 || t[i] == t[j]) { i++; j++; nxt[i] = j; }
        else j = nxt[j];
    }
    i = 0; j = 0;
    while (i < n && j < m) {
        if (j == -1 || s[i] == t[j]) { i++; j++; }
        else j = nxt[j];
    }
    return j == m ? i - m : -1;
}
int main(void) {
    int q;
    scanf("%s %d", s, &q);
    int n = (int)strlen(s);
    while (q--) {
        scanf("%s", t);
        int m = (int)strlen(t);
        int pos = kmp_find(s, n, t, m);
        if (pos >= 0) printf("%s\n", s + pos);
        else printf("Not Found\n");
    }
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <string>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s; int q;
    cin >> s >> q;
    while (q--) {
        string t; cin >> t;
        size_t p = s.find(t);
        if (p == string::npos) cout << "Not Found\n";
        else cout << s.substr(p) << "\n";
    }
    return 0;
}
""",
)

def _oracle_60(text: str) -> str:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    s, t = lines[0], lines[1]
    pos = []
    for i in range(len(s) - len(t) + 1):
        if s[i:i + len(t)] == t:
            pos.append(str(i + 1))
    m = len(t)
    pi = [0] * m
    for i in range(1, m):
        sub = t[:i + 1]
        best = 0
        for L in range(1, len(sub)):
            if sub[:L] == sub[-L:]:
                best = L
        pi[i] = best
    line1 = " ".join(pos) if pos else "none"
    line2 = " ".join(map(str, pi))
    return line1 + "\n" + line2 + "\n"

add(
    title="【模板】KMP字符串匹配",
    section="第 04 讲 · 串、数组和广义表",
    difficulty=3, score=20, tags=["串", "KMP模板", "前缀函数"],
    statement_md=(
        "KMP 算法的完整模板题：\n\n"
        "1. 输出模式串 `T` 在主串 `S` 中**所有出现的位置**（起始下标从 1 开始，允许重叠；若未出现输出 `none`）；\n"
        "2. 输出模式串 `T` 每个前缀 `T[1..i]` 的**最长真公共前后缀长度 `pi[i]`**（即现代算法竞赛常用的 Border 数组，满足 `nxt[i] = pi[i-1] + 1`）。\n\n"
        "★ 把 `pi[i]` 和严蔚敏教材的 `next[j]` 对照着看：\n"
        "`ABABC` 的 `pi` 是 `0 0 1 2 0`，而教材 `next` 是 `0 1 1 2 3` —— "
        "教材的 `next[j]` 正好等于 `pi[j-2] + 1`（`j ≥ 2`）。掌握这层换算，两套口径永远不会混。"
    ),
    input_format="第一行主串 `S`。\n\n第二行模式串 `T`。",
    output_format=(
        "第一行：`T` 在 `S` 中所有匹配的起始位置（1 起，空格分隔；无匹配输出 `none`）。\n\n"
        "第二行：`|T|` 个整数（空格分隔），依次表示 `T[1..i]` 的最长真公共前后缀长度。"
    ),
    constraints_md="- 1 ≤ |S|, |T| ≤ 10000",
    inputs=[
        "ABABABC\nABA\n",
        "AAAAA\nAA\n",
        "ABCDEFG\nXYZ\n",
        "AABAACAADAABAABA\nAABA\n",
        "ABCABC\nABCABC\n",
    ],
    samples=2,
    oracle=_oracle_60,
    solution=r"""#include <stdio.h>
#include <string.h>
char s[10005], t[10005];
int pi[10005];
int main(void) {
    scanf("%s %s", s, t);
    int n = (int)strlen(s), m = (int)strlen(t);
    pi[0] = 0;
    for (int i = 1; i < m; i++) {
        int j = pi[i - 1];
        while (j > 0 && t[i] != t[j]) j = pi[j - 1];
        if (t[i] == t[j]) j++;
        pi[i] = j;
    }
    int first = 1, j = 0;
    for (int i = 0; i < n; i++) {
        while (j > 0 && s[i] != t[j]) j = pi[j - 1];
        if (s[i] == t[j]) j++;
        if (j == m) {
            printf(first ? "%d" : " %d", i - m + 2);
            first = 0;
            j = pi[j - 1];               /* ★ 继续找重叠匹配 */
        }
    }
    if (first) printf("none");
    printf("\n");
    for (int i = 0; i < m; i++) printf(i ? " %d" : "%d", pi[i]);
    printf("\n");
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <string>
#include <vector>
using namespace std;
int main() {
    string s, t; cin >> s >> t;
    int n = (int)s.size(), m = (int)t.size();
    vector<int> pos;
    for (int i = 0; i + m <= n; i++)
        if (s.compare(i, m, t) == 0) pos.push_back(i + 1);
    if (pos.empty()) cout << "none\n";
    else {
        for (size_t i = 0; i < pos.size(); i++) cout << (i ? " " : "") << pos[i];
        cout << "\n";
    }
    for (int i = 1; i <= m; i++) {
        int best = 0;
        for (int L = 1; L < i; L++)
            if (t.compare(0, L, t, i - L, L) == 0) best = L;
        cout << (i > 1 ? " " : "") << best;
    }
    cout << "\n";
    return 0;
}
""",
)

def _oracle_61(text: str) -> str:
    s = text.strip()
    n = len(s)
    for L in range(n - 2, 0, -1):
        cand = s[:L]
        if s.endswith(cand) and s.find(cand, 1, n - 1) != -1:
            return cand + "\n"
    return "none\n"

add(
    title="好中缀",
    section="第 04 讲 · 串、数组和广义表",
    difficulty=2, score=15, tags=["串", "KMP", "前后缀", "Border"],
    statement_md=(
        "如果一个非空字符串 `T` 既是主串 `S` 的**前缀**、又是 `S` 的**后缀**，"
        "同时还在 `S` 的**内部**（即不作为整串首尾的位置 `2 ≤ i ≤ |S|-|T|`）出现过至少一次，"
        "就称 `T` 是 `S` 的一个**好中缀**。\n\n"
        "请找出 `S` **最长**的好中缀；若不存在，输出 `none`。\n\n"
        "★ KMP 思路：整个串的公共前后缀长度只能沿着 `pi[n-1] → pi[pi[n-1]-1] → …` 这条链取；"
        "而「在内部出现过」等价于该长度不超过内部位置的最大前缀函数值 `max(pi[1..n-2])`。"
    ),
    input_format="一行，一个非空字符串 `S`（不含空格）。",
    output_format="一行，最长的好中缀字符串；若不存在则输出 `none`。",
    constraints_md="- 1 ≤ |S| ≤ 5000",
    inputs=[
        "fixprefixsuffix\n",
        "abcdabc\n",
        "aaaaa\n",
        "ababab\n",
        "abcde\n",
        "ababa\n",
    ],
    samples=3,
    oracle=_oracle_61,
    solution=r"""#include <stdio.h>
#include <string.h>
char s[5005];
int pi[5005];
int main(void) {
    scanf("%s", s);
    int n = (int)strlen(s);
    pi[0] = 0;
    int max_mid = 0;
    for (int i = 1; i < n; i++) {
        int j = pi[i - 1];
        while (j > 0 && s[i] != s[j]) j = pi[j - 1];
        if (s[i] == s[j]) j++;
        pi[i] = j;
        if (i < n - 1 && pi[i] > max_mid) max_mid = pi[i];
    }
    int L = pi[n - 1];
    while (L > max_mid) L = pi[L - 1];
    if (L == 0) printf("none\n");
    else { s[L] = '\0'; printf("%s\n", s); }
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <string>
using namespace std;
int main() {
    string s; cin >> s;
    int n = (int)s.size();
    for (int L = n - 2; L >= 1; L--) {
        if (s.compare(0, L, s, n - L, L) != 0) continue;
        string cand = s.substr(0, L);
        size_t p = s.find(cand, 1);
        if (p != string::npos && (int)p + L < n) {
            cout << cand << "\n";
            return 0;
        }
    }
    cout << "none\n";
    return 0;
}
""",
)

def _oracle_62(text: str) -> str:
    d = text.split()
    q = int(d[0])
    out = []
    idx = 1
    for _ in range(q):
        v, h = d[idx], d[idx + 1]; idx += 2
        m = len(v)
        vv = v + v
        hit = any(vv[i:i + m] in h for i in range(m))
        out.append("YES" if hit else "NO")
    return "\n".join(out) + "\n"

add(
    title="病毒变种",
    section="第 04 讲 · 串、数组和广义表",
    difficulty=2, score=15, tags=["串", "环状串", "模式匹配"],
    statement_md=(
        "教材案例 4.1「病毒感染检测」：由于病毒的 DNA 序列是**环状**的，"
        "长度为 `m` 的病毒序列可以从任意位置断开，形成 `m` 种线性变种（例如 `baa` 的变种有 `baa`、`aab`、`aba`）。\n\n"
        "给定若干对 `(病毒序列, 待测人类序列)`，判断每条待测人类序列中是否包含该病毒的**任意一种变种**。\n\n"
        "★ 环状串的经典破环成链技巧：把病毒串复制拼接成长度为 `2m` 的 `V + V`，"
        "里面所有长度为 `m` 的连续子串就恰好枚举了全部 `m` 种变种！"
    ),
    input_format="第一行正整数 `q`（检测组数）。\n\n随后 `q` 行，每行两个不含空格的字符串：`病毒DNA 人类DNA`。",
    output_format="`q` 行，若感染（含任意变种）输出 `YES`，否则输出 `NO`。",
    constraints_md="- 1 ≤ q ≤ 20\n- 1 ≤ |病毒DNA|, |人类DNA| ≤ 1000",
    inputs=[
        "4\naab bbaabbba\naab aabbaa\nabc acbxyz\nxyz xy\n",
        "2\nabba bababbaa\nabc cab\n",
        "3\na b\na a\nabcd cdab\n",
    ],
    samples=2,
    oracle=_oracle_62,
    solution=r"""#include <stdio.h>
#include <string.h>
char v[1005], h[1005], vv[2010], pat[1005];
int main(void) {
    int q;
    scanf("%d", &q);
    while (q--) {
        scanf("%s %s", v, h);
        int m = (int)strlen(v);
        strcpy(vv, v);
        strcat(vv, v);
        int hit = 0;
        for (int i = 0; i < m; i++) {
            strncpy(pat, vv + i, m);
            pat[m] = '\0';
            if (strstr(h, pat) != NULL) { hit = 1; break; }
        }
        printf(hit ? "YES\n" : "NO\n");
    }
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <string>
using namespace std;
int main() {
    int q; cin >> q;
    while (q--) {
        string v, h; cin >> v >> h;
        int m = (int)v.size();
        bool hit = false;
        for (int i = 0; i < m; i++) {
            string rot = v.substr(i) + v.substr(0, i);
            if (h.find(rot) != string::npos) { hit = true; break; }
        }
        cout << (hit ? "YES\n" : "NO\n");
    }
    return 0;
}
""",
)

def _oracle_63(text: str) -> str:
    d = text.split()
    n, m = int(d[0]), int(d[1])
    a = [[int(d[2 + i * m + j]) for j in range(m)] for i in range(n)]
    rmax = [max(row) for row in a]
    cmin = [min(a[i][j] for i in range(n)) for j in range(m)]
    for i in range(n):
        for j in range(m):
            if a[i][j] == rmax[i] and a[i][j] == cmin[j]:
                return "%d %d %d\n" % (i + 1, j + 1, a[i][j])
    return "NONE\n"

add(
    title="矩阵鞍点查找",
    section="第 04 讲 · 串、数组和广义表",
    difficulty=2, score=15, tags=["数组", "鞍点", "二维数组"],
    statement_md=(
        "在一个 `n × m` 的矩阵中，若某个元素 `A[i][j]` 既是第 `i` 行的**最大值**"
        "（`≥` 同行所有元素），又是第 `j` 列的**最小值**（`≤` 同列所有元素），"
        "则称它为该矩阵的一个**鞍点**。\n\n"
        "请按行优先顺序找出第一个鞍点，输出它的行号、列号（均从 1 开始）与元素值；"
        "若不存在鞍点，输出 `NONE`。"
    ),
    input_format="第一行两个正整数 `n m`。\n\n随后 `n` 行，每行 `m` 个整数。",
    output_format="一行，输出 `row col value`；若无鞍点则输出 `NONE`。",
    constraints_md="- 1 ≤ n, m ≤ 100\n- |A[i][j]| ≤ 10^9",
    inputs=[
        "3 3\n1 7 3\n4 5 6\n7 8 9\n",
        "2 2\n1 2\n2 1\n",
        "3 4\n9 80 205 40\n90 -60 96 1\n210 -3 101 89\n",
        "1 1\n5\n",
    ],
    samples=2,
    oracle=_oracle_63,
    solution=r"""#include <stdio.h>
int a[105][105], rmax[105], cmin[105];
int main(void) {
    int n, m;
    scanf("%d %d", &n, &m);
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            scanf("%d", &a[i][j]);
    for (int i = 0; i < n; i++) {
        rmax[i] = a[i][0];
        for (int j = 1; j < m; j++) if (a[i][j] > rmax[i]) rmax[i] = a[i][j];
    }
    for (int j = 0; j < m; j++) {
        cmin[j] = a[0][j];
        for (int i = 1; i < n; i++) if (a[i][j] < cmin[j]) cmin[j] = a[i][j];
    }
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            if (a[i][j] == rmax[i] && a[i][j] == cmin[j]) {
                printf("%d %d %d\n", i + 1, j + 1, a[i][j]);
                return 0;
            }
    printf("NONE\n");
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
using namespace std;
int main() {
    int n, m; cin >> n >> m;
    vector<vector<int>> a(n, vector<int>(m));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++) cin >> a[i][j];
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            bool ok = true;
            for (int k = 0; k < m; k++) if (a[i][k] > a[i][j]) ok = false;
            for (int k = 0; k < n; k++) if (a[k][j] < a[i][j]) ok = false;
            if (ok) { cout << i + 1 << " " << j + 1 << " " << a[i][j] << "\n"; return 0; }
        }
    }
    cout << "NONE\n";
    return 0;
}
""",
)

def _oracle_64(text: str) -> str:
    d = text.split()
    r, c, t = int(d[0]), int(d[1]), int(d[2])
    trip = []
    p = 3
    for _ in range(t):
        rr, cc, vv = int(d[p]), int(d[p + 1]), int(d[p + 2]); p += 3
        trip.append((rr, cc, vv))
    out = []
    for col in range(1, c + 1):
        for rr, cc, vv in trip:
            if cc == col:
                out.append((cc, rr, vv))
    lines = ["%d %d %d" % (c, r, t)]
    lines += ["%d %d %d" % e for e in out]
    return "\n".join(lines) + "\n"

add(
    title="三元组顺序表表示的稀疏矩阵转置运算I",
    section="第 04 讲 · 串、数组和广义表",
    difficulty=2, score=15, tags=["数组", "稀疏矩阵", "按列序转置"],
    statement_md=(
        "教材算法 5.1（按列序朴素转置）：给定稀疏矩阵 `M` 的三元组顺序表（行优先），"
        "按列号 `col = 1..c` 外层循环、内层从头到尾扫描全部 `t` 个三元组，"
        "挑出列号等于 `col` 的元素并交换行列下标，依次填入转置矩阵 `T`。\n\n"
        "★ 为什么不能直接「把每个三元组的 row 和 col 对调完事」？因为原表按**行优先**排，"
        "直接对调后变成按**列优先**，不再是合法的行优先三元组顺序表！"
    ),
    input_format=(
        "第一行三个整数 `r c t`（行数、列数、非零元个数）。\n\n"
        "随后 `t` 行，每行 `row col value`（1 起，按行优先排列）。"
    ),
    output_format="第一行 `c r t`；随后 `t` 行输出转置后的行优先三元组 `row col value`。",
    constraints_md="- 1 ≤ r, c ≤ 500\n- 0 ≤ t ≤ 1000",
    inputs=[
        "3 4 4\n1 2 12\n1 3 9\n3 1 -3\n3 4 14\n",
        "2 3 2\n1 3 5\n2 1 8\n",
        "3 3 0\n",
        "4 2 3\n1 2 7\n2 1 6\n4 2 9\n",
    ],
    samples=2,
    oracle=_oracle_64,
    solution=r"""#include <stdio.h>
int ar[1005], ac[1005], av[1005];
int main(void) {
    int r, c, t;
    scanf("%d %d %d", &r, &c, &t);
    for (int k = 0; k < t; k++) scanf("%d %d %d", &ar[k], &ac[k], &av[k]);
    printf("%d %d %d\n", c, r, t);
    for (int col = 1; col <= c; col++) {
        for (int k = 0; k < t; k++) {
            if (ac[k] == col) printf("%d %d %d\n", ac[k], ar[k], av[k]);
        }
    }
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
struct E { int r, c, v; };
int main() {
    int r, c, t; cin >> r >> c >> t;
    vector<E> a(t);
    for (auto &x : a) { cin >> x.r >> x.c >> x.v; swap(x.r, x.c); }
    sort(a.begin(), a.end(), [](const E &x, const E &y) {
        return x.r != y.r ? x.r < y.r : x.c < y.c;
    });
    cout << c << " " << r << " " << t << "\n";
    for (auto &x : a) cout << x.r << " " << x.c << " " << x.v << "\n";
    return 0;
}
""",
)

def _oracle_65(text: str) -> str:
    d = text.split()
    r, c, t = int(d[0]), int(d[1]), int(d[2])
    trip = []
    p = 3
    num = [0] * (c + 1)
    for _ in range(t):
        rr, cc, vv = int(d[p]), int(d[p + 1]), int(d[p + 2]); p += 3
        trip.append((rr, cc, vv))
        num[cc] += 1
    cpot = [0] * (c + 1)
    cpot[1] = 1
    for col in range(2, c + 1):
        cpot[col] = cpot[col - 1] + num[col - 1]
    lines = [
        "num: " + " ".join(str(num[col]) for col in range(1, c + 1)),
        "cpot: " + " ".join(str(cpot[col]) for col in range(1, c + 1)),
    ]
    out = sorted(((cc, rr, vv) for rr, cc, vv in trip), key=lambda x: (x[0], x[1]))
    lines += ["%d %d %d" % e for e in out]
    return "\n".join(lines) + "\n"

add(
    title="三元组顺序表表示的稀疏矩阵转置II",
    section="第 04 讲 · 串、数组和广义表",
    difficulty=3, score=20, tags=["数组", "稀疏矩阵", "快速转置", "cpot"],
    statement_md=(
        "教材算法 5.2（快速转置）的核心是先算出两张辅助向量：\n\n"
        "- `num[col]`：原矩阵第 `col` 列中非零元的个数；\n"
        "- `cpot[col]`：原矩阵第 `col` 列的第一个非零元在转置三元组表中的**位序**（从 **1** 开始）：\n"
        "  `cpot[1] = 1`，`cpot[col] = cpot[col-1] + num[col-1]`。\n\n"
        "本题要求**先把初始的 `num[1..c]` 和 `cpot[1..c]` 打出来**，再输出快速转置后的三元组表——"
        "专门检验你是不是真的算对了辅助数组，而不是拿排序糊弄过去。"
    ),
    input_format=(
        "第一行三个整数 `r c t`（1 ≤ r, c ≤ 500，0 ≤ t ≤ 1000）。\n\n"
        "随后 `t` 行，每行 `row col value`（1 起，按行优先排列）。"
    ),
    output_format=(
        "第一行：`num: num[1] num[2] ... num[c]`\n\n"
        "第二行：`cpot: cpot[1] cpot[2] ... cpot[c]`\n\n"
        "随后 `t` 行：转置后的三元组 `row col value`。"
    ),
    constraints_md="- 1 ≤ r, c ≤ 500\n- 0 ≤ t ≤ 1000",
    inputs=[
        "6 7 8\n1 2 12\n1 3 9\n3 1 -3\n3 6 14\n4 3 24\n5 2 18\n6 1 15\n6 4 -7\n",
        "3 4 3\n1 1 5\n2 3 7\n3 2 9\n",
        "2 3 0\n",
        "3 3 4\n1 3 2\n2 1 4\n2 3 6\n3 2 8\n",
    ],
    samples=2,
    oracle=_oracle_65,
    solution=r"""#include <stdio.h>
int ar[1005], ac[1005], av[1005];
int br[1005], bc[1005], bv[1005];
int num[505], cpot[505];
int main(void) {
    int r, c, t;
    scanf("%d %d %d", &r, &c, &t);
    for (int col = 1; col <= c; col++) num[col] = 0;
    for (int k = 0; k < t; k++) {
        scanf("%d %d %d", &ar[k], &ac[k], &av[k]);
        num[ac[k]]++;
    }
    cpot[1] = 1;
    for (int col = 2; col <= c; col++) cpot[col] = cpot[col - 1] + num[col - 1];
    printf("num:");
    for (int col = 1; col <= c; col++) printf(" %d", num[col]);
    printf("\ncpot:");
    for (int col = 1; col <= c; col++) printf(" %d", cpot[col]);
    printf("\n");
    for (int k = 0; k < t; k++) {
        int pos = cpot[ac[k]]++;
        br[pos] = ac[k]; bc[pos] = ar[k]; bv[pos] = av[k];
    }
    for (int k = 1; k <= t; k++) printf("%d %d %d\n", br[k], bc[k], bv[k]);
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
struct E { int r, c, v; };
int main() {
    int r, c, t; cin >> r >> c >> t;
    vector<E> a(t);
    vector<int> num(c + 1, 0), cpot(c + 1, 0);
    for (auto &x : a) { cin >> x.r >> x.c >> x.v; num[x.c]++; }
    cpot[1] = 1;
    for (int j = 2; j <= c; j++) cpot[j] = cpot[j - 1] + num[j - 1];
    cout << "num:";
    for (int j = 1; j <= c; j++) cout << " " << num[j];
    cout << "\ncpot:";
    for (int j = 1; j <= c; j++) cout << " " << cpot[j];
    cout << "\n";
    for (auto &x : a) swap(x.r, x.c);
    stable_sort(a.begin(), a.end(), [](const E &x, const E &y) {
        return x.r != y.r ? x.r < y.r : x.c < y.c;
    });
    for (auto &x : a) cout << x.r << " " << x.c << " " << x.v << "\n";
    return 0;
}
""",
)

def _oracle_66(text: str) -> str:
    d = text.split()
    r, c, t1, t2 = int(d[0]), int(d[1]), int(d[2]), int(d[3])
    p = 4
    mp: dict[tuple[int, int], int] = {}
    for _ in range(t1 + t2):
        rr, cc, vv = int(d[p]), int(d[p + 1]), int(d[p + 2]); p += 3
        mp[(rr, cc)] = mp.get((rr, cc), 0) + vv
    out = [(rr, cc, vv) for (rr, cc), vv in sorted(mp.items()) if vv != 0]
    lines = ["%d %d %d" % (r, c, len(out))]
    lines += ["%d %d %d" % e for e in out]
    return "\n".join(lines) + "\n"

add(
    title="稀疏矩阵加法",
    section="第 04 讲 · 串、数组和广义表",
    difficulty=3, score=20, tags=["数组", "稀疏矩阵", "矩阵加法", "双指针"],
    statement_md=(
        "给定两个同型（`r × c`）稀疏矩阵 `A` 和 `B` 的行优先三元组顺序表，"
        "求 `C = A + B` 的行优先三元组顺序表。\n\n"
        "★ 两个关键点：\n"
        "1. 两个三元组表都已经按 `(row, col)` 字典序排好，用**二路归并双指针**扫一遍就能合并，复杂度 `O(t1 + t2)`；\n"
        "2. **正负抵消得 0 的项绝不能写进结果表**（三元组表只存非零元），否则非零元计数 `t3` 和表内容都会错！"
    ),
    input_format=(
        "第一行四个整数 `r c t1 t2`（行数、列数、A 的非零元数、B 的非零元数）。\n\n"
        "随后 `t1` 行给出 `A` 的三元组 `row col val`（行优先）。\n\n"
        "随后 `t2` 行给出 `B` 的三元组 `row col val`（行优先）。"
    ),
    output_format="第一行 `r c t3`；随后 `t3` 行按行优先输出 `C` 的非零三元组。",
    constraints_md="- 1 ≤ r, c ≤ 1000\n- 0 ≤ t1, t2 ≤ 1000",
    inputs=[
        "3 3 3 3\n1 1 2\n1 3 5\n2 2 -4\n1 2 7\n1 3 -5\n2 2 9\n",
        "2 2 2 2\n1 1 3\n2 2 -3\n1 1 -3\n2 2 3\n",
        "3 4 2 0\n1 2 6\n3 4 8\n",
        "2 3 1 2\n2 1 4\n1 3 9\n2 1 6\n",
    ],
    samples=2,
    oracle=_oracle_66,
    solution=r"""#include <stdio.h>
struct E { int r, c, v; } a[1005], b[1005], res[2005];
int cmp_pos(struct E x, struct E y) {
    if (x.r != y.r) return x.r < y.r ? -1 : 1;
    if (x.c != y.c) return x.c < y.c ? -1 : 1;
    return 0;
}
int main(void) {
    int r, c, t1, t2;
    scanf("%d %d %d %d", &r, &c, &t1, &t2);
    for (int i = 0; i < t1; i++) scanf("%d %d %d", &a[i].r, &a[i].c, &a[i].v);
    for (int i = 0; i < t2; i++) scanf("%d %d %d", &b[i].r, &b[i].c, &b[i].v);
    int i = 0, j = 0, k = 0;
    while (i < t1 && j < t2) {
        int s = cmp_pos(a[i], b[j]);
        if (s < 0) res[k++] = a[i++];
        else if (s > 0) res[k++] = b[j++];
        else {
            int sum = a[i].v + b[j].v;
            if (sum != 0) res[k++] = (struct E){a[i].r, a[i].c, sum};
            i++; j++;
        }
    }
    while (i < t1) res[k++] = a[i++];
    while (j < t2) res[k++] = b[j++];
    printf("%d %d %d\n", r, c, k);
    for (int idx = 0; idx < k; idx++)
        printf("%d %d %d\n", res[idx].r, res[idx].c, res[idx].v);
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <map>
using namespace std;
int main() {
    int r, c, t1, t2;
    cin >> r >> c >> t1 >> t2;
    map<pair<int, int>, int> mp;
    for (int i = 0; i < t1 + t2; i++) {
        int rr, cc, vv; cin >> rr >> cc >> vv;
        mp[{rr, cc}] += vv;
    }
    int cnt = 0;
    for (auto &kv : mp) if (kv.second != 0) cnt++;
    cout << r << " " << c << " " << cnt << "\n";
    for (auto &kv : mp)
        if (kv.second != 0)
            cout << kv.first.first << " " << kv.first.second << " " << kv.second << "\n";
    return 0;
}
""",
)

def _oracle_67(text: str) -> str:
    d = text.split()
    r, k, c, t1, t2 = int(d[0]), int(d[1]), int(d[2]), int(d[3]), int(d[4])
    p = 5
    A = []
    for _ in range(t1):
        A.append((int(d[p]), int(d[p + 1]), int(d[p + 2]))); p += 3
    B = []
    for _ in range(t2):
        B.append((int(d[p]), int(d[p + 1]), int(d[p + 2]))); p += 3
    mp: dict[tuple[int, int], int] = {}
    for ar, ac, av in A:
        for br, bc, bv in B:
            if ac == br:
                mp[(ar, bc)] = mp.get((ar, bc), 0) + av * bv
    out = [(rr, cc, vv) for (rr, cc), vv in sorted(mp.items()) if vv != 0]
    lines = ["%d %d %d" % (r, c, len(out))]
    lines += ["%d %d %d" % e for e in out]
    return "\n".join(lines) + "\n"

add(
    title="稀疏矩阵乘法",
    section="第 04 讲 · 串、数组和广义表",
    difficulty=3, score=20, tags=["数组", "稀疏矩阵", "矩阵乘法", "行逻辑链接"],
    statement_md=(
        "给定稀疏矩阵 `A`（`r × k`）和 `B`（`k × c`）的三元组顺序表，"
        "求乘积矩阵 `C = A × B`（`r × c`）的行优先三元组顺序表。\n\n"
        "★ 教材「行逻辑链接顺序表」乘法思路：逐行处理 `A` 的第 `i` 行，"
        "开一个长度为 `c` 的累加器 `ctemp[1..c]`；对 `A` 第 `i` 行的每个非零元 `(i, m, av)`，"
        "去 `B` 的第 `m` 行把所有 `(m, j, bv)` 乘积累加进 `ctemp[j]`。"
        "第 `i` 行扫完后，`ctemp[1..c]` 中非零的项天然按列递增，直接输出即可！"
    ),
    input_format=(
        "第一行五个整数 `r k c t1 t2`。\n\n"
        "随后 `t1` 行给出 `A` 的三元组 `row col val`。\n\n"
        "随后 `t2` 行给出 `B` 的三元组 `row col val`。"
    ),
    output_format="第一行 `r c t3`；随后 `t3` 行按行优先输出 `C` 的非零三元组。",
    constraints_md="- 1 ≤ r, k, c ≤ 200\n- 0 ≤ t1, t2 ≤ 1000",
    inputs=[
        "2 3 2 3 3\n1 1 2\n1 3 1\n2 2 3\n1 1 4\n2 2 5\n3 1 -8\n",
        "2 2 2 2 2\n1 1 1\n1 2 2\n1 1 2\n2 1 -1\n",
        "3 3 3 2 2\n1 2 3\n3 1 4\n1 3 5\n2 1 6\n",
        "2 3 2 0 2\n1 1 5\n2 2 7\n",
    ],
    samples=2,
    oracle=_oracle_67,
    solution=r"""#include <stdio.h>
struct E { int r, c; long long v; } A[1005], B[1005], C[40005];
long long ctemp[205];
int main(void) {
    int r, k, c, t1, t2;
    scanf("%d %d %d %d %d", &r, &k, &c, &t1, &t2);
    for (int i = 0; i < t1; i++) scanf("%d %d %lld", &A[i].r, &A[i].c, &A[i].v);
    for (int i = 0; i < t2; i++) scanf("%d %d %lld", &B[i].r, &B[i].c, &B[i].v);
    int t3 = 0, p = 0;
    for (int row = 1; row <= r; row++) {
        for (int col = 1; col <= c; col++) ctemp[col] = 0;
        while (p < t1 && A[p].r == row) {
            int mid = A[p].c;
            for (int q = 0; q < t2; q++)
                if (B[q].r == mid) ctemp[B[q].c] += A[p].v * B[q].v;
            p++;
        }
        for (int col = 1; col <= c; col++)
            if (ctemp[col] != 0) C[t3++] = (struct E){row, col, ctemp[col]};
    }
    printf("%d %d %d\n", r, c, t3);
    for (int i = 0; i < t3; i++)
        printf("%d %d %lld\n", C[i].r, C[i].c, C[i].v);
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
#include <map>
using namespace std;
struct E { int r, c; long long v; };
int main() {
    int r, k, c, t1, t2;
    cin >> r >> k >> c >> t1 >> t2;
    vector<E> A(t1), B(t2);
    for (auto &x : A) cin >> x.r >> x.c >> x.v;
    for (auto &x : B) cin >> x.r >> x.c >> x.v;
    map<pair<int, int>, long long> mp;
    for (auto &a : A)
        for (auto &b : B)
            if (a.c == b.r) mp[{a.r, b.c}] += a.v * b.v;
    int cnt = 0;
    for (auto &kv : mp) if (kv.second != 0) cnt++;
    cout << r << " " << c << " " << cnt << "\n";
    for (auto &kv : mp)
        if (kv.second != 0)
            cout << kv.first.first << " " << kv.first.second << " " << kv.second << "\n";
    return 0;
}
""",
)

def _oracle_68(text: str) -> str:
    d = text.split()
    n, m = int(d[0]), int(d[1])
    a = [[int(d[2 + i * m + j]) for j in range(m)] for i in range(n)]
    best = a[0][0]
    for r1 in range(n):
        col = [0] * m
        for r2 in range(r1, n):
            cur = 0
            for j in range(m):
                col[j] += a[r2][j]
                cur = col[j] if cur <= 0 else cur + col[j]
                if cur > best:
                    best = cur
    return "%d\n" % best

add(
    title="最大子矩阵和问题",
    section="第 04 讲 · 串、数组和广义表",
    difficulty=3, score=20, tags=["数组", "最大子矩阵和", "降维", "动态规划"],
    statement_md=(
        "给定一个 `n × m` 的整数矩阵，求其中元素之和最大的**非空连续子矩阵**（至少包含 1 个元素），"
        "输出该最大和。\n\n"
        "★ 经典「二维压一维」技巧：\n"
        "固定子矩阵的上下边界 `r1` 和 `r2`，把 `[r1..r2]` 这一带每一列的元素加起来，"
        "就变成了一个长度为 `m` 的一维数组 `col[0..m-1]` —— 随后直接套第 02 讲的"
        "**一维最大子段和（Kadane 算法）**！复杂度从 `O(n²m²)` 降到 `O(n²m)`。"
    ),
    input_format="第一行两个正整数 `n m`。\n\n随后 `n` 行，每行 `m` 个整数。",
    output_format="一行一个整数，表示非空连续子矩阵的最大元素和。",
    constraints_md="- 1 ≤ n, m ≤ 80\n- -10^5 ≤ A[i][j] ≤ 10^5",
    inputs=[
        "3 3\n0 -2 -7\n9 2 -6\n-4 1 -4\n",
        "2 2\n-5 -2\n-9 -3\n",
        "3 4\n1 2 -1 -4\n-8 -3 4 2\n3 8 10 -8\n",
        "1 5\n-2 3 -1 4 -5\n",
    ],
    samples=2,
    oracle=_oracle_68,
    solution=r"""#include <stdio.h>
int a[85][85];
long long col[85];
int main(void) {
    int n, m;
    scanf("%d %d", &n, &m);
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            scanf("%d", &a[i][j]);
    long long best = a[0][0];
    for (int r1 = 0; r1 < n; r1++) {
        for (int j = 0; j < m; j++) col[j] = 0;
        for (int r2 = r1; r2 < n; r2++) {
            long long cur = 0;
            for (int j = 0; j < m; j++) {
                col[j] += a[r2][j];
                cur = (cur > 0) ? (cur + col[j]) : col[j];
                if (cur > best) best = cur;
            }
        }
    }
    printf("%lld\n", best);
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
int main() {
    int n, m; cin >> n >> m;
    vector<vector<long long>> ps(n + 1, vector<long long>(m + 1, 0));
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= m; j++) {
            long long v; cin >> v;
            ps[i][j] = ps[i - 1][j] + ps[i][j - 1] - ps[i - 1][j - 1] + v;
        }
    long long best = ps[1][1];
    for (int r1 = 1; r1 <= n; r1++) {
        for (int r2 = r1; r2 <= n; r2++) {
            long long min_pre = 0;
            for (int c = 1; c <= m; c++) {
                long long cur = ps[r2][c] - ps[r1 - 1][c];
                best = max(best, cur - min_pre);
                min_pre = min(min_pre, cur);
            }
        }
    }
    cout << best << "\n";
    return 0;
}
""",
)

def _oracle_69(text: str) -> str:
    s = text.strip()
    inner = s[1:-1]
    depth = 0
    split_pos = -1
    for i, ch in enumerate(inner):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch == "," and depth == 0:
            split_pos = i
            break
    if split_pos == -1:
        head = inner
        tail = "()"
    else:
        head = inner[:split_pos]
        tail = "(" + inner[split_pos + 1:] + ")"
    return head + "\n" + tail + "\n"

add(
    title="广义表的表头与表尾",
    section="第 04 讲 · 串、数组和广义表",
    difficulty=3, score=20, tags=["广义表", "表头表尾", "括号匹配"],
    statement_md=(
        "给定一个**非空**广义表 `L`（如 `(a,(b,c),d)`），求它的**表头 `GetHead(L)`** "
        "和**表尾 `GetTail(L)`**。\n\n"
        "★ 教材铁律（几乎每次考试必考）：\n"
        "- **表头**是广义表的第一个顶层元素，它**既可以是原子，也可以是子表**；\n"
        "- **表尾**是除去第一个顶层元素后**其余元素组成的广义表**，因此**表尾永远是一个表（外层必带括号 `(...)`）**！\n\n"
        "例如 `L = (a)` 的表头是 `a`，表尾是空表 `()`；`L = ((a,b),c)` 的表头是 `(a,b)`，表尾是 `(c)`。"
    ),
    input_format="一行，一个非空广义表字符串（外层以 `(` 开头、` )` 结尾，且不是 `()`）。",
    output_format="第一行输出表头 `GetHead(L)`；第二行输出表尾 `GetTail(L)`。",
    constraints_md="- 3 ≤ |L| ≤ 1000",
    inputs=[
        "(a,(b,c),d)\n",
        "(a)\n",
        "((a,b),c)\n",
        "((),a)\n",
        "(((a)))\n",
    ],
    samples=3,
    oracle=_oracle_69,
    solution=r"""#include <stdio.h>
#include <string.h>
char s[1005];
int main(void) {
    scanf("%s", s);
    int n = (int)strlen(s);
    int depth = 0, comma = -1;
    for (int i = 1; i < n - 1; i++) {
        if (s[i] == '(') depth++;
        else if (s[i] == ')') depth--;
        else if (s[i] == ',' && depth == 0) { comma = i; break; }
    }
    if (comma == -1) {
        for (int i = 1; i < n - 1; i++) putchar(s[i]);
        printf("\n()\n");
    } else {
        for (int i = 1; i < comma; i++) putchar(s[i]);
        printf("\n(");
        for (int i = comma + 1; i < n - 1; i++) putchar(s[i]);
        printf(")\n");
    }
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <string>
#include <vector>
using namespace std;
int main() {
    string s; cin >> s;
    string in = s.substr(1, s.size() - 2);
    vector<string> items;
    int d = 0, last = 0;
    for (int i = 0; i < (int)in.size(); i++) {
        if (in[i] == '(') d++;
        else if (in[i] == ')') d--;
        else if (in[i] == ',' && d == 0) {
            items.push_back(in.substr(last, i - last));
            last = i + 1;
        }
    }
    items.push_back(in.substr(last));
    cout << items[0] << "\n(";
    for (size_t i = 1; i < items.size(); i++)
        cout << (i > 1 ? "," : "") << items[i];
    cout << ")\n";
    return 0;
}
""",
)

# --------------------------------------------------------------------- #
#  第 05 讲扩充：树和二叉树、哈夫曼树、并查集经典题型（循序渐进 + 举一反三）
# --------------------------------------------------------------------- #

def _oracle_70(text: str) -> str:
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
        return "empty\nempty\nempty\n"
    pre, ino, post = [], [], []

    def walk(n) -> None:
        if n is None:
            return
        pre.append(n[0])
        walk(n[1])
        ino.append(n[0])
        walk(n[2])
        post.append(n[0])

    walk(root)
    return "".join(pre) + "\n" + "".join(ino) + "\n" + "".join(post) + "\n"

add(
    title="建立与遍历二叉树",
    section="第 05 讲 · 树和二叉树",
    difficulty=1, score=10, tags=["二叉树", "前序建树", "三种遍历"],
    statement_md=(
        "根据带空指针标记 `#` 的扩展先序序列建立二叉树，依次输出它的"
        "**先序遍历**、**中序遍历**和**后序遍历**序列。\n\n"
        "★ 三种递归遍历在代码上**走的是完全同一条路线**（每个结点都被经过三次）：\n"
        "- 第 1 次经过时打印 → **先序**（根-左-右）\n"
        "- 第 2 次（从左子树回来）打印 → **中序**（左-根-右）\n"
        "- 第 3 次（从右子树回来）打印 → **后序**（左-右-根）"
    ),
    input_format="一行，带 `#` 空标记的先序序列（结点为大写字母）。",
    output_format="三行，依次为先序、中序、后序序列；若为空树则三行均输出 `empty`。",
    constraints_md="- 序列长度 ≤ 2000",
    inputs=[
        "AB#D##C##\n",
        "AB##C##\n",
        "#\n",
        "A##\n",
        "ABD##E##CF##G##\n",
    ],
    samples=2,
    oracle=_oracle_70,
    solution=r"""#include <stdio.h>
#include <stdlib.h>
typedef struct Node { char c; struct Node *l, *r; } Node;
char s[2005];
int pos;
Node *build(void) {
    char c = s[pos++];
    if (c == '#' || c == '\0') return NULL;
    Node *t = (Node *)malloc(sizeof(Node));
    t->c = c; t->l = build(); t->r = build();
    return t;
}
void pre(Node *t)  { if (!t) return; putchar(t->c); pre(t->l); pre(t->r); }
void ino(Node *t)  { if (!t) return; ino(t->l); putchar(t->c); ino(t->r); }
void post(Node *t) { if (!t) return; post(t->l); post(t->r); putchar(t->c); }
int main(void) {
    scanf("%s", s);
    pos = 0;
    Node *root = build();
    if (!root) { printf("empty\nempty\nempty\n"); return 0; }
    pre(root);  putchar('\n');
    ino(root);  putchar('\n');
    post(root); putchar('\n');
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <string>
#include <vector>
#include <functional>
using namespace std;
struct N { char c; int l, r; };
int main() {
    string s; cin >> s;
    vector<N> pool;
    int pos = 0;
    function<int()> build = [&]() -> int {
        char c = s[pos++];
        if (c == '#') return -1;
        int id = (int)pool.size();
        pool.push_back({c, -1, -1});
        int l = build(), r = build();
        pool[id].l = l; pool[id].r = r;
        return id;
    };
    int root = build();
    if (root < 0) { cout << "empty\nempty\nempty\n"; return 0; }
    string a, b, c;
    function<void(int)> go = [&](int u) {
        if (u < 0) return;
        a += pool[u].c;
        go(pool[u].l);
        b += pool[u].c;
        go(pool[u].r);
        c += pool[u].c;
    };
    go(root);
    cout << a << "\n" << b << "\n" << c << "\n";
    return 0;
}
""",
)

def _oracle_71(text: str) -> str:
    s = text.strip()

    def rec(i: int):
        if i >= len(s) or s[i] == "#":
            return None, i + 1
        v = s[i]
        left, i = rec(i + 1)
        right, i = rec(i)
        return (v, right, left), i   # 交换左右孩子

    root, _ = rec(0)
    if root is None:
        return "empty\nempty\n"
    ino, pre = [], []

    def walk(n) -> None:
        if n is None:
            return
        pre.append(n[0])
        walk(n[1])
        ino.append(n[0])
        walk(n[2])

    walk(root)
    return "".join(ino) + "\n" + "".join(pre) + "\n"

add(
    title="交换二叉树中每个结点的左孩子和右孩子",
    section="第 05 讲 · 树和二叉树",
    difficulty=1, score=10, tags=["二叉树", "镜像反转", "递归"],
    statement_md=(
        "读入带 `#` 空标记的先序序列建立二叉树，把树中**每一个结点的左孩子和右孩子互换**"
        "（即二叉树的镜像翻转），然后输出翻转后的**中序遍历**和**先序遍历**。\n\n"
        "★ 值得想清楚的一个性质：镜像翻转后，新的**中序遍历**（左-根-右）"
        "恰好等于原树中序遍历的**整体逆序**（右-根-左）！"
    ),
    input_format="一行，带 `#` 空标记的先序序列。",
    output_format="第一行翻转后的中序序列，第二行翻转后的先序序列；空树输出两行 `empty`。",
    constraints_md="- 序列长度 ≤ 2000",
    inputs=[
        "AB#D##C##\n",
        "AB##C##\n",
        "A##\n",
        "#\n",
        "ABD##E##C#F##\n",
    ],
    samples=2,
    oracle=_oracle_71,
    solution=r"""#include <stdio.h>
#include <stdlib.h>
typedef struct Node { char c; struct Node *l, *r; } Node;
char s[2005];
int pos;
Node *build(void) {
    char c = s[pos++];
    if (c == '#' || c == '\0') return NULL;
    Node *t = (Node *)malloc(sizeof(Node));
    t->c = c; t->l = build(); t->r = build();
    return t;
}
void mirror(Node *t) {
    if (!t) return;
    Node *tmp = t->l; t->l = t->r; t->r = tmp;
    mirror(t->l); mirror(t->r);
}
void ino(Node *t) { if (!t) return; ino(t->l); putchar(t->c); ino(t->r); }
void pre(Node *t) { if (!t) return; putchar(t->c); pre(t->l); pre(t->r); }
int main(void) {
    scanf("%s", s);
    pos = 0;
    Node *root = build();
    if (!root) { printf("empty\nempty\n"); return 0; }
    mirror(root);
    ino(root); putchar('\n');
    pre(root); putchar('\n');
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <string>
#include <vector>
#include <functional>
using namespace std;
struct N { char c; int l, r; };
int main() {
    string s; cin >> s;
    vector<N> pool;
    int pos = 0;
    function<int()> build = [&]() -> int {
        char c = s[pos++];
        if (c == '#') return -1;
        int id = (int)pool.size();
        pool.push_back({c, -1, -1});
        int l = build(), r = build();
        pool[id].l = l; pool[id].r = r;
        return id;
    };
    int root = build();
    if (root < 0) { cout << "empty\nempty\n"; return 0; }
    /* 另一套：不改指针，遍历时直接先走右子树再走左子树 */
    string ino, pre;
    function<void(int)> go = [&](int u) {
        if (u < 0) return;
        pre += pool[u].c;
        go(pool[u].r);
        ino += pool[u].c;
        go(pool[u].l);
    };
    go(root);
    cout << ino << "\n" << pre << "\n";
    return 0;
}
""",
)

def _oracle_72(text: str) -> str:
    d = text.split()
    n = int(d[0])
    L = [-1] * n
    R = [-1] * n
    indeg = [0] * n
    p = 1
    for i in range(n):
        ls, rs = d[p], d[p + 1]; p += 2
        if ls != "-":
            L[i] = int(ls); indeg[L[i]] += 1
        if rs != "-":
            R[i] = int(rs); indeg[R[i]] += 1
    root = next(i for i in range(n) if indeg[i] == 0)
    q = [root]
    leaves = []
    while q:
        u = q.pop(0)
        if L[u] == -1 and R[u] == -1:
            leaves.append(str(u))
        if L[u] != -1:
            q.append(L[u])
        if R[u] != -1:
            q.append(R[u])
    return " ".join(leaves) + "\n"

add(
    title="列出叶结点",
    section="第 05 讲 · 树和二叉树",
    difficulty=2, score=15, tags=["二叉树", "静态链表", "找根", "层序遍历"],
    statement_md=(
        "PTA 经典题 `List Leaves`：给定一棵二叉树的静态数组表示（结点编号 `0` ~ `N-1`），"
        "按**从上到下、从左到右**的顺序输出所有叶结点。\n\n"
        "★ 这道题最关键的第一步是**自己找根**：题目不会告诉你谁是根，"
        "但**根是唯一没有父结点的结点**（即没有出现在任何一行的左右孩子里，入度为 0）！"
        "找到根之后跑一遍队列 BFS，遇到左右孩子都为 `-` 的结点就输出。"
    ),
    input_format=(
        "第一行正整数 `N`（1 ≤ N ≤ 20）。\n\n"
        "随后 `N` 行，第 `i` 行（对应结点 `i`，从 0 开始）给出左孩子和右孩子编号；"
        "无该孩子则用 `-` 表示。"
    ),
    output_format="一行，按从上到下、从左到右顺序输出所有叶结点编号（空格分隔）。",
    constraints_md="- 1 ≤ N ≤ 20",
    inputs=[
        "8\n1 -\n- -\n0 -\n2 7\n- -\n- -\n5 -\n4 6\n",
        "1\n- -\n",
        "3\n1 2\n- -\n- -\n",
        "5\n- 1\n- 2\n- 3\n- 4\n- -\n",
    ],
    samples=2,
    oracle=_oracle_72,
    solution=r"""#include <stdio.h>
#include <stdlib.h>
int L[25], R[25], indeg[25], q[25];
int main(void) {
    int n;
    scanf("%d", &n);
    for (int i = 0; i < n; i++) {
        char ls[8], rs[8];
        scanf("%s %s", ls, rs);
        L[i] = (ls[0] == '-') ? -1 : atoi(ls);
        R[i] = (rs[0] == '-') ? -1 : atoi(rs);
        if (L[i] != -1) indeg[L[i]]++;
        if (R[i] != -1) indeg[R[i]]++;
    }
    int root = 0;
    for (int i = 0; i < n; i++) if (indeg[i] == 0) { root = i; break; }
    int f = 0, r = 0, first = 1;
    q[r++] = root;
    while (f < r) {
        int u = q[f++];
        if (L[u] == -1 && R[u] == -1) {
            printf(first ? "%d" : " %d", u);
            first = 0;
        }
        if (L[u] != -1) q[r++] = L[u];
        if (R[u] != -1) q[r++] = R[u];
    }
    printf("\n");
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <functional>
using namespace std;
int main() {
    int n; cin >> n;
    vector<int> L(n, -1), R(n, -1), indeg(n, 0);
    for (int i = 0; i < n; i++) {
        string a, b; cin >> a >> b;
        if (a != "-") { L[i] = stoi(a); indeg[L[i]]++; }
        if (b != "-") { R[i] = stoi(b); indeg[R[i]]++; }
    }
    int root = 0;
    for (int i = 0; i < n; i++) if (!indeg[i]) root = i;
    vector<tuple<int, int, int>> leaves;
    function<void(int, int, int)> dfs = [&](int u, int dep, int mask) {
        if (u < 0) return;
        if (L[u] < 0 && R[u] < 0) leaves.emplace_back(dep, mask, u);
        dfs(L[u], dep + 1, mask * 2);
        dfs(R[u], dep + 1, mask * 2 + 1);
    };
    dfs(root, 0, 0);
    sort(leaves.begin(), leaves.end());
    for (size_t i = 0; i < leaves.size(); i++)
        cout << (i ? " " : "") << get<2>(leaves[i]);
    cout << "\n";
    return 0;
}
""",
)

def _oracle_73(text: str) -> str:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    n = int(lines[0])
    pre, ino = lines[1][:n], lines[2][:n]

    def height(p: str, i: str) -> int:
        if not p:
            return 0
        k = i.index(p[0])
        return 1 + max(height(p[1:1 + k], i[:k]), height(p[1 + k:], i[k + 1:]))

    return "%d\n" % height(pre, ino)

add(
    title="还原二叉树",
    section="第 05 讲 · 树和二叉树",
    difficulty=2, score=15, tags=["二叉树", "先序中序", "树高", "分治"],
    statement_md=(
        "PTA 经典题 `还原二叉树`：给定一棵二叉树的**先序遍历序列**和**中序遍历序列**"
        "（结点为互不相同的字符），要求还原该二叉树并输出它的**高度（深度）**。\n\n"
        "★ 其实求高度根本不需要把指针树真正 `malloc` 出来：在分治切分 `[pl..pr]` 与 `[il..ir]` 的同时，"
        "直接返回 `1 + max(左子树高度, 右子树高度)`，10 行代码就能搞定！"
    ),
    input_format=(
        "第一行正整数 `N`（结点个数）。\n\n"
        "第二行长度为 `N` 的先序序列字符串。\n\n"
        "第三行长度为 `N` 的中序序列字符串。"
    ),
    output_format="一行一个整数，表示二叉树的高度。",
    constraints_md="- 1 ≤ N ≤ 60\n- 结点字符互不相同",
    inputs=[
        "9\nABDFGHIEC\nFDHGIBEAC\n",
        "1\nA\nA\n",
        "4\nABCD\nDCBA\n",
        "7\nABDECFG\nDBEAFCG\n",
    ],
    samples=2,
    oracle=_oracle_73,
    solution=r"""#include <stdio.h>
char pre[105], ino[105];
int solve(int pl, int pr, int il, int ir) {
    if (pl > pr) return 0;
    int k = il;
    while (ino[k] != pre[pl]) k++;
    int ln = k - il;
    int hl = solve(pl + 1, pl + ln, il, k - 1);
    int hr = solve(pl + ln + 1, pr, k + 1, ir);
    return 1 + (hl > hr ? hl : hr);
}
int main(void) {
    int n;
    scanf("%d %s %s", &n, pre, ino);
    printf("%d\n", solve(0, n - 1, 0, n - 1));
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <string>
#include <algorithm>
#include <functional>
using namespace std;
int main() {
    int n; string pre, ino;
    cin >> n >> pre >> ino;
    function<int(string, string)> h = [&](string p, string i) -> int {
        if (p.empty()) return 0;
        size_t k = i.find(p[0]);
        return 1 + max(h(p.substr(1, k), i.substr(0, k)),
                       h(p.substr(1 + k), i.substr(k + 1)));
    };
    cout << h(pre, ino) << "\n";
    return 0;
}
""",
)

def _oracle_74(text: str) -> str:
    d = text.split()
    n = int(d[0])
    post = [int(v) for v in d[1:1 + n]]
    ino = [int(v) for v in d[1 + n:1 + 2 * n]]
    pre = []

    def go(pl: int, pr: int, il: int, ir: int) -> None:
        if pl > pr:
            return
        root = post[pr]
        pre.append(str(root))
        k = ino.index(root, il, ir + 1)
        ln = k - il
        go(pl, pl + ln - 1, il, k - 1)
        go(pl + ln, pr - 1, k + 1, ir)

    go(0, n - 1, 0, n - 1)
    return "Preorder: " + " ".join(pre) + "\n"

add(
    title="根据后序和中序遍历输出前序遍历",
    section="第 05 讲 · 树和二叉树",
    difficulty=2, score=15, tags=["二叉树", "后序中序", "前序遍历"],
    statement_md=(
        "给定一棵二叉树的**后序遍历**和**中序遍历**整数序列（结点值互不相同），"
        "输出它的先序遍历序列。\n\n"
        "★ 和「先序 + 中序求后序」正好镜像：\n"
        "- **后序的最后一个元素** `post[pr]` 就是当前子树的**根**；\n"
        "- 拿着根去中序里找到位置 `k`，算出左子树长度 `ln = k - il`；\n"
        "- 后序里左子树是 `[pl .. pl+ln-1]`，右子树是 `[pl+ln .. pr-1]`！"
    ),
    input_format=(
        "第一行正整数 `N`。\n\n"
        "第二行 `N` 个整数，表示后序遍历序列。\n\n"
        "第三行 `N` 个整数，表示中序遍历序列。"
    ),
    output_format="一行，格式为 `Preorder: v1 v2 ...`（冒号后与数字间均以单个空格分隔）。",
    constraints_md="- 1 ≤ N ≤ 30\n- 结点值互不相同",
    inputs=[
        "7\n2 3 1 5 7 6 4\n1 2 3 4 5 6 7\n",
        "1\n10\n10\n",
        "5\n4 5 2 3 1\n4 2 5 1 3\n",
        "4\n4 3 2 1\n1 2 3 4\n",
    ],
    samples=2,
    oracle=_oracle_74,
    solution=r"""#include <stdio.h>
int post[35], ino[35];
void solve(int pl, int pr, int il, int ir) {
    if (pl > pr) return;
    int root = post[pr];
    printf(" %d", root);
    int k = il;
    while (ino[k] != root) k++;
    int ln = k - il;
    solve(pl, pl + ln - 1, il, k - 1);
    solve(pl + ln, pr - 1, k + 1, ir);
}
int main(void) {
    int n;
    scanf("%d", &n);
    for (int i = 0; i < n; i++) scanf("%d", &post[i]);
    for (int i = 0; i < n; i++) scanf("%d", &ino[i]);
    printf("Preorder:");
    solve(0, n - 1, 0, n - 1);
    printf("\n");
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
#include <functional>
using namespace std;
struct N { int v, l, r; };
int main() {
    int n; cin >> n;
    vector<int> post(n), ino(n);
    for (int &x : post) cin >> x;
    for (int &x : ino) cin >> x;
    vector<N> pool;
    function<int(int, int, int, int)> build = [&](int pl, int pr, int il, int ir) -> int {
        if (pl > pr) return -1;
        int root = post[pr], k = il;
        while (ino[k] != root) k++;
        int ln = k - il;
        int id = (int)pool.size();
        pool.push_back({root, -1, -1});
        int l = build(pl, pl + ln - 1, il, k - 1);
        int r = build(pl + ln, pr - 1, k + 1, ir);
        pool[id].l = l; pool[id].r = r;
        return id;
    };
    int rt = build(0, n - 1, 0, n - 1);
    cout << "Preorder:";
    vector<int> st{rt};
    while (!st.empty()) {
        int u = st.back(); st.pop_back();
        if (u < 0) continue;
        cout << " " << pool[u].v;
        st.push_back(pool[u].r);
        st.push_back(pool[u].l);
    }
    cout << "\n";
    return 0;
}
""",
)

def _oracle_75(text: str) -> str:
    d = text.split()
    n = int(d[0])
    post = [int(v) for v in d[1:1 + n]]
    ino = [int(v) for v in d[1 + n:1 + 2 * n]]

    def build(pl: int, pr: int, il: int, ir: int):
        if pl > pr:
            return None
        root = post[pr]
        k = ino.index(root, il, ir + 1)
        ln = k - il
        return (root,
                build(pl, pl + ln - 1, il, k - 1),
                build(pl + ln, pr - 1, k + 1, ir))

    q = [build(0, n - 1, 0, n - 1)]
    out = []
    while q:
        u = q.pop(0)
        if u is None:
            continue
        out.append(str(u[0]))
        q.append(u[1])
        q.append(u[2])
    return " ".join(out) + "\n"

add(
    title="树的遍历",
    section="第 05 讲 · 树和二叉树",
    difficulty=3, score=20, tags=["二叉树", "后序中序", "层序遍历", "L2-006"],
    statement_md=(
        "PTA 天梯赛经典题 `L2-006 树的遍历`：给定一棵二叉树的**后序遍历**和**中序遍历**，"
        "请你输出它的**层序遍历**序列。\n\n"
        "★ 两种写法都值得掌握：\n"
        "1. 标准写法：先由后序+中序递归建出二叉树，再用队列做一次 BFS；\n"
        "2. 巧算写法：递归切分时多传一个 `depth` 参数，由于左子树总是比右子树先递归，"
        "直接 `levels[depth].push_back(root)`，最后按层拼起来就是层序遍历！"
    ),
    input_format=(
        "第一行正整数 `N`。\n\n"
        "第二行 `N` 个整数，表示后序序列。\n\n"
        "第三行 `N` 个整数，表示中序序列。"
    ),
    output_format="一行，输出层序遍历序列（`N` 个整数，空格分隔）。",
    constraints_md="- 1 ≤ N ≤ 30\n- 结点值互不相同",
    inputs=[
        "7\n2 3 1 5 7 6 4\n1 2 3 4 5 6 7\n",
        "1\n8\n8\n",
        "5\n4 5 2 3 1\n4 2 5 1 3\n",
        "6\n3 2 1 6 5 4\n1 2 3 4 5 6\n",
    ],
    samples=2,
    oracle=_oracle_75,
    solution=r"""#include <stdio.h>
#include <stdlib.h>
typedef struct Node { int v; struct Node *l, *r; } Node;
int post[35], ino[35];
Node *build(int pl, int pr, int il, int ir) {
    if (pl > pr) return NULL;
    int root = post[pr], k = il;
    while (ino[k] != root) k++;
    int ln = k - il;
    Node *t = (Node *)malloc(sizeof(Node));
    t->v = root;
    t->l = build(pl, pl + ln - 1, il, k - 1);
    t->r = build(pl + ln, pr - 1, k + 1, ir);
    return t;
}
int main(void) {
    int n;
    scanf("%d", &n);
    for (int i = 0; i < n; i++) scanf("%d", &post[i]);
    for (int i = 0; i < n; i++) scanf("%d", &ino[i]);
    Node *q[40];
    int f = 0, r = 0, first = 1;
    q[r++] = build(0, n - 1, 0, n - 1);
    while (f < r) {
        Node *u = q[f++];
        printf(first ? "%d" : " %d", u->v);
        first = 0;
        if (u->l) q[r++] = u->l;
        if (u->r) q[r++] = u->r;
    }
    printf("\n");
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
#include <functional>
using namespace std;
int main() {
    int n; cin >> n;
    vector<int> post(n), ino(n);
    for (int &x : post) cin >> x;
    for (int &x : ino) cin >> x;
    vector<vector<int>> lv(n);
    function<void(int, int, int, int, int)> go = [&](int pl, int pr, int il, int ir, int d) {
        if (pl > pr) return;
        int root = post[pr], k = il;
        while (ino[k] != root) k++;
        int ln = k - il;
        lv[d].push_back(root);
        go(pl, pl + ln - 1, il, k - 1, d + 1);
        go(pl + ln, pr - 1, k + 1, ir, d + 1);
    };
    go(0, n - 1, 0, n - 1, 0);
    bool first = true;
    for (auto &row : lv)
        for (int v : row) { cout << (first ? "" : " ") << v; first = false; }
    cout << "\n";
    return 0;
}
""",
)

def _oracle_76(text: str) -> str:
    d = text.split()
    n = int(d[0])
    ino = [int(v) for v in d[1:1 + n]]
    pre = [int(v) for v in d[1 + n:1 + 2 * n]]

    def build(pl: int, pr: int, il: int, ir: int):
        if pl > pr:
            return None
        root = pre[pl]
        k = ino.index(root, il, ir + 1)
        ln = k - il
        return (root,
                build(pl + 1, pl + ln, il, k - 1),
                build(pl + ln + 1, pr, k + 1, ir))

    q = [build(0, n - 1, 0, n - 1)]
    out = []
    while q:
        u = q.pop(0)
        if u is None:
            continue
        out.append(str(u[0]))
        q.append(u[2])   # ★ 镜面反转：先入队右孩子，再入队左孩子
        q.append(u[1])
    return " ".join(out) + "\n"

add(
    title="玩转二叉树",
    section="第 05 讲 · 树和二叉树",
    difficulty=3, score=20, tags=["二叉树", "前序中序", "镜面反转", "L2-011"],
    statement_md=(
        "PTA 天梯赛经典题 `L2-011 玩转二叉树`：给定一棵二叉树的**中序遍历**和**前序遍历**，"
        "请你先将树做个**镜面反转**（交换每个结点的左、右孩子），再输出反转后的**层序遍历**序列。\n\n"
        "★ 注意输入顺序是**第一行中序、第二行前序**（别惯性当成先给前序）！"
        "而镜面反转后的层序遍历，只需在 BFS 入队时**先把右孩子入队、再把左孩子入队**即可。"
    ),
    input_format=(
        "第一行正整数 `N`。\n\n"
        "第二行 `N` 个整数，表示**中序**序列。\n\n"
        "第三行 `N` 个整数，表示**前序**序列。"
    ),
    output_format="一行，镜面反转后的层序遍历序列（空格分隔）。",
    constraints_md="- 1 ≤ N ≤ 30\n- 结点值互不相同",
    inputs=[
        "7\n1 2 3 4 5 6 7\n4 1 3 2 6 5 7\n",
        "1\n5\n5\n",
        "5\n4 2 5 1 3\n1 2 4 5 3\n",
        "4\n1 2 3 4\n1 2 3 4\n",
    ],
    samples=2,
    oracle=_oracle_76,
    solution=r"""#include <stdio.h>
#include <stdlib.h>
typedef struct Node { int v; struct Node *l, *r; } Node;
int ino[35], pre[35];
Node *build(int pl, int pr, int il, int ir) {
    if (pl > pr) return NULL;
    int root = pre[pl], k = il;
    while (ino[k] != root) k++;
    int ln = k - il;
    Node *t = (Node *)malloc(sizeof(Node));
    t->v = root;
    t->l = build(pl + 1, pl + ln, il, k - 1);
    t->r = build(pl + ln + 1, pr, k + 1, ir);
    return t;
}
int main(void) {
    int n;
    scanf("%d", &n);
    for (int i = 0; i < n; i++) scanf("%d", &ino[i]);
    for (int i = 0; i < n; i++) scanf("%d", &pre[i]);
    Node *q[40];
    int f = 0, r = 0, first = 1;
    q[r++] = build(0, n - 1, 0, n - 1);
    while (f < r) {
        Node *u = q[f++];
        printf(first ? "%d" : " %d", u->v);
        first = 0;
        if (u->r) q[r++] = u->r;     /* ★ 先右后左 = 镜面层序 */
        if (u->l) q[r++] = u->l;
    }
    printf("\n");
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
#include <functional>
using namespace std;
int main() {
    int n; cin >> n;
    vector<int> ino(n), pre(n);
    for (int &x : ino) cin >> x;
    for (int &x : pre) cin >> x;
    vector<vector<int>> lv(n);
    function<void(int, int, int, int, int)> go = [&](int pl, int pr, int il, int ir, int d) {
        if (pl > pr) return;
        int root = pre[pl], k = il;
        while (ino[k] != root) k++;
        int ln = k - il;
        lv[d].push_back(root);
        go(pl + ln + 1, pr, k + 1, ir, d + 1);   // ★ 先递归右子树，再递归左子树
        go(pl + 1, pl + ln, il, k - 1, d + 1);
    };
    go(0, n - 1, 0, n - 1, 0);
    bool first = true;
    for (auto &row : lv)
        for (int v : row) { cout << (first ? "" : " ") << v; first = false; }
    cout << "\n";
    return 0;
}
""",
)

def _oracle_77(text: str) -> str:
    d = text.split()
    n = int(d[0])
    post = [int(v) for v in d[1:1 + n]]
    tree = [0] * (n + 1)
    idx = 0

    def walk(u: int) -> None:
        nonlocal idx
        if u > n:
            return
        walk(2 * u)
        walk(2 * u + 1)
        tree[u] = post[idx]
        idx += 1

    walk(1)
    return " ".join(str(tree[i]) for i in range(1, n + 1)) + "\n"

add(
    title="完全二叉树的层序遍历",
    section="第 05 讲 · 树和二叉树",
    difficulty=3, score=20, tags=["完全二叉树", "顺序存储", "后序还原", "L2-035"],
    statement_md=(
        "PTA 天梯赛经典题 `L2-035 完全二叉树的层序遍历`：给定一棵 `N` 个结点的**完全二叉树**的**后序遍历**序列，"
        "请输出它的**层序遍历**序列。\n\n"
        "★ 看似只给了后序（没给中序）怎么可能还原唯一二叉树？"
        "因为「**完全二叉树**」四个字已经把树的形状彻底锁死了！\n"
        "用一维数组 `tree[1..N]` 按层序编号存完全二叉树（结点 `u` 的左孩子是 `2u`、右孩子是 `2u+1`），"
        "对下标 `1..N` 跑一遍后序递归，边走边从输入里读一个数填进 `tree[u]`，"
        "最后把 `tree[1..N]` 从头到尾打印出来就是层序遍历！"
    ),
    input_format="第一行正整数 `N`。\n\n第二行 `N` 个整数，表示完全二叉树的后序遍历序列。",
    output_format="一行 `N` 个整数（空格分隔），表示该完全二叉树的层序遍历序列。",
    constraints_md="- 1 ≤ N ≤ 30",
    inputs=[
        "8\n91 71 2 34 10 15 55 18\n",
        "1\n42\n",
        "5\n4 5 2 3 1\n",
        "7\n1 2 3 4 5 6 7\n",
    ],
    samples=2,
    oracle=_oracle_77,
    solution=r"""#include <stdio.h>
int n, post[35], tree[35], idx = 0;
void fill_post(int u) {
    if (u > n) return;
    fill_post(2 * u);
    fill_post(2 * u + 1);
    tree[u] = post[idx++];
}
int main(void) {
    scanf("%d", &n);
    for (int i = 0; i < n; i++) scanf("%d", &post[i]);
    fill_post(1);
    for (int i = 1; i <= n; i++) printf(i > 1 ? " %d" : "%d", tree[i]);
    printf("\n");
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
#include <functional>
using namespace std;
int main() {
    int n; cin >> n;
    vector<int> post(n);
    for (int &x : post) cin >> x;
    vector<int> order;
    function<void(int)> dfs = [&](int u) {
        if (u > n) return;
        dfs(u * 2);
        dfs(u * 2 + 1);
        order.push_back(u);
    };
    dfs(1);
    vector<int> ans(n + 1);
    for (int i = 0; i < n; i++) ans[order[i]] = post[i];
    for (int i = 1; i <= n; i++) cout << (i > 1 ? " " : "") << ans[i];
    cout << "\n";
    return 0;
}
""",
)

def _oracle_78(text: str) -> str:
    d = text.split()
    n = int(d[0])
    par = [int(v) for v in d[1:1 + n]]
    ch = [[] for _ in range(n + 1)]
    root = 1
    for i in range(1, n + 1):
        if par[i - 1] == 0:
            root = i
        else:
            ch[par[i - 1]].append(i)
    q = [root]
    out = []
    while q:
        u = q.pop(0)
        out.append(str(u))
        for v in ch[u]:
            q.append(v)
    return " ".join(out) + "\n"

add(
    title="树层次遍历",
    section="第 05 讲 · 树和二叉树",
    difficulty=2, score=15, tags=["树", "双亲表示法", "孩子链表", "层次遍历"],
    statement_md=(
        "给定一棵含 `N` 个结点（编号 `1` ~ `N`）的**普通多叉树**（双亲表示法给出每个结点的父结点编号，"
        "根结点的父结点为 `0`），请按从上到下、同父结点的孩子按编号从小到大的顺序输出树的**层次遍历**。\n\n"
        "★ 普通树的存储转换：输入是**双亲表示法** `parent[i]`（找父亲 O(1)，找孩子慢），"
        "先扫一遍把每个 `i` 挂到 `children[parent[i]]` 里转成**孩子表示法**，就能直接跑 BFS 队列了！"
    ),
    input_format="第一行正整数 `N`。\n\n第二行 `N` 个整数 `p[1] p[2] ... p[N]`，表示结点 `1..N` 的父结点（根为 `0`）。",
    output_format="一行 `N` 个整数（空格分隔），表示树的层次遍历序列。",
    constraints_md="- 1 ≤ N ≤ 200",
    inputs=[
        "7\n0 1 1 2 2 2 3\n",
        "1\n0\n",
        "6\n2 0 2 1 1 3\n",
        "5\n0 1 2 3 4\n",
    ],
    samples=2,
    oracle=_oracle_78,
    solution=r"""#include <stdio.h>
int head[205], nxt[205], to[205], ecnt = 0;
int q[205];
/* 按编号从大到小头插，遍历时正好从小到大 */
int par[205];
int main(void) {
    int n, root = 1;
    scanf("%d", &n);
    for (int i = 1; i <= n; i++) {
        scanf("%d", &par[i]);
        if (par[i] == 0) root = i;
    }
    for (int i = n; i >= 1; i--) {
        if (par[i] != 0) {
            ++ecnt; to[ecnt] = i; nxt[ecnt] = head[par[i]]; head[par[i]] = ecnt;
        }
    }
    int f = 0, r = 0;
    q[r++] = root;
    while (f < r) {
        int u = q[f++];
        printf(f == 1 ? "%d" : " %d", u);
        for (int e = head[u]; e; e = nxt[e]) q[r++] = to[e];
    }
    printf("\n");
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
using namespace std;
int main() {
    int n, root = 1; cin >> n;
    vector<vector<int>> ch(n + 1);
    for (int i = 1; i <= n; i++) {
        int p; cin >> p;
        if (p == 0) root = i;
        else ch[p].push_back(i);
    }
    vector<int> cur{root}, out;
    while (!cur.empty()) {
        vector<int> nxt;
        for (int u : cur) {
            out.push_back(u);
            for (int v : ch[u]) nxt.push_back(v);
        }
        cur = nxt;
    }
    for (size_t i = 0; i < out.size(); i++) cout << (i ? " " : "") << out[i];
    cout << "\n";
    return 0;
}
""",
)

def _oracle_79(text: str) -> str:
    d = text.split()
    n = int(d[0])
    ino = [int(v) for v in d[1:1 + n]]
    post = [int(v) for v in d[1 + n:1 + 2 * n]]
    lv: list[list[int]] = []

    def go(pl: int, pr: int, il: int, ir: int, dep: int) -> None:
        if pl > pr:
            return
        while len(lv) <= dep:
            lv.append([])
        root = post[pr]
        lv[dep].append(root)
        k = ino.index(root, il, ir + 1)
        ln = k - il
        go(pl, pl + ln - 1, il, k - 1, dep + 1)
        go(pl + ln, pr - 1, k + 1, ir, dep + 1)

    go(0, n - 1, 0, n - 1, 0)
    r_view = " ".join(str(row[-1]) for row in lv)
    l_view = " ".join(str(row[0]) for row in lv)
    return "R: " + r_view + "\nL: " + l_view + "\n"

add(
    title="浪漫侧影",
    section="第 05 讲 · 树和二叉树",
    difficulty=3, score=20, tags=["二叉树", "右视图", "左视图", "层序分层"],
    statement_md=(
        "PTA 经典题 `浪漫侧影`：给定一棵二叉树的**中序遍历**和**后序遍历**序列，"
        "请你分别输出从树的右侧和左侧观察到的「侧影」：\n\n"
        "- **右视图（`R:`）**：从上到下每一层的**最右边**那个结点；\n"
        "- **左视图（`L:`）**：从上到下每一层的**最左边**那个结点。\n\n"
        "★ 按层 BFS（或带深度 `dep` 的先序 DFS）收集每一层的结点列表 `level[dep]`，"
        "每层的第一个元素就是左视图、最后一个元素就是右视图！"
    ),
    input_format=(
        "第一行正整数 `N`。\n\n"
        "第二行 `N` 个整数，表示**中序**序列。\n\n"
        "第三行 `N` 个整数，表示**后序**序列。"
    ),
    output_format=(
        "第一行：`R: r1 r2 ...`（从根层向下的右视图结点，空格分隔）\n\n"
        "第二行：`L: l1 l2 ...`（从根层向下的左视图结点，空格分隔）"
    ),
    constraints_md="- 1 ≤ N ≤ 30\n- 结点值互不相同",
    inputs=[
        "8\n6 8 7 4 5 1 3 2\n8 5 4 7 6 3 2 1\n",
        "1\n9\n9\n",
        "5\n4 2 5 1 3\n4 5 2 3 1\n",
        "7\n1 2 3 4 5 6 7\n2 3 1 5 7 6 4\n",
    ],
    samples=2,
    oracle=_oracle_79,
    solution=r"""#include <stdio.h>
int ino[35], post[35], first_v[35], last_v[35], max_d = -1;
void dfs(int pl, int pr, int il, int ir, int d) {
    if (pl > pr) return;
    if (d > max_d) { max_d = d; first_v[d] = post[pr]; }
    last_v[d] = post[pr];
    int k = il;
    while (ino[k] != post[pr]) k++;
    int ln = k - il;
    dfs(pl, pl + ln - 1, il, k - 1, d + 1);
    dfs(pl + ln, pr - 1, k + 1, ir, d + 1);
}
int main(void) {
    int n;
    scanf("%d", &n);
    for (int i = 0; i < n; i++) scanf("%d", &ino[i]);
    for (int i = 0; i < n; i++) scanf("%d", &post[i]);
    dfs(0, n - 1, 0, n - 1, 0);
    printf("R:");
    for (int d = 0; d <= max_d; d++) printf(" %d", last_v[d]);
    printf("\nL:");
    for (int d = 0; d <= max_d; d++) printf(" %d", first_v[d]);
    printf("\n");
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
#include <functional>
using namespace std;
struct N { int v, l, r; };
int main() {
    int n; cin >> n;
    vector<int> ino(n), post(n);
    for (int &x : ino) cin >> x;
    for (int &x : post) cin >> x;
    vector<N> pool;
    function<int(int, int, int, int)> build = [&](int pl, int pr, int il, int ir) -> int {
        if (pl > pr) return -1;
        int root = post[pr], k = il;
        while (ino[k] != root) k++;
        int ln = k - il;
        int id = (int)pool.size();
        pool.push_back({root, -1, -1});
        int l = build(pl, pl + ln - 1, il, k - 1);
        int r = build(pl + ln, pr - 1, k + 1, ir);
        pool[id].l = l; pool[id].r = r;
        return id;
    };
    vector<int> cur{build(0, n - 1, 0, n - 1)}, R, L;
    while (!cur.empty()) {
        L.push_back(pool[cur.front()].v);
        R.push_back(pool[cur.back()].v);
        vector<int> nxt;
        for (int u : cur) {
            if (pool[u].l >= 0) nxt.push_back(pool[u].l);
            if (pool[u].r >= 0) nxt.push_back(pool[u].r);
        }
        cur = nxt;
    }
    cout << "R:";
    for (int v : R) cout << " " << v;
    cout << "\nL:";
    for (int v : L) cout << " " << v;
    cout << "\n";
    return 0;
}
""",
)

def _oracle_80(text: str) -> str:
    s = text.strip()
    cnt: dict[int, int] = {}

    def rec(i: int, d: int) -> int:
        if i >= len(s) or s[i] == "#":
            return i + 1
        cnt[d] = cnt.get(d, 0) + 1
        i = rec(i + 1, d + 1)
        return rec(i, d + 1)

    rec(0, 1)
    best_w, best_lv = 0, 1
    for lv in sorted(cnt):
        if cnt[lv] > best_w:
            best_w = cnt[lv]
            best_lv = lv
    return "%d %d\n" % (best_w, best_lv)

add(
    title="二叉树的最大宽度与层号",
    section="第 05 讲 · 树和二叉树",
    difficulty=2, score=15, tags=["二叉树", "宽度", "层序统计"],
    statement_md=(
        "二叉树的**宽度**定义为各层结点数的最大值（根在第 1 层）。"
        "给定带 `#` 空标记的先序序列（保证非空树），求该二叉树的**最大宽度**以及达到最大宽度的**最小层号**。"
    ),
    input_format="一行，带 `#` 空标记的先序序列（非空树）。",
    output_format="一行两个整数，空格分隔：`最大宽度 对应层号`。",
    constraints_md="- 序列长度 ≤ 2000",
    inputs=[
        "ABD##E##CF##G##\n",
        "AB#D##C##\n",
        "A##\n",
        "ABC####\n",
    ],
    samples=2,
    oracle=_oracle_80,
    solution=r"""#include <stdio.h>
char s[2005];
int pos = 0, cnt[2005], max_d = 0;
void dfs(int d) {
    char c = s[pos++];
    if (c == '#' || c == '\0') return;
    cnt[d]++;
    if (d > max_d) max_d = d;
    dfs(d + 1);
    dfs(d + 1);
}
int main(void) {
    scanf("%s", s);
    dfs(1);
    int bw = 0, bl = 1;
    for (int d = 1; d <= max_d; d++)
        if (cnt[d] > bw) { bw = cnt[d]; bl = d; }
    printf("%d %d\n", bw, bl);
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <string>
#include <vector>
#include <functional>
using namespace std;
struct N { int l, r; };
int main() {
    string s; cin >> s;
    vector<N> pool;
    int pos = 0;
    function<int()> build = [&]() -> int {
        if (s[pos++] == '#') return -1;
        int id = (int)pool.size();
        pool.push_back({-1, -1});
        int l = build(), r = build();
        pool[id].l = l; pool[id].r = r;
        return id;
    };
    vector<int> cur{build()};
    int bw = 0, bl = 1, lv = 1;
    while (!cur.empty()) {
        if ((int)cur.size() > bw) { bw = (int)cur.size(); bl = lv; }
        vector<int> nxt;
        for (int u : cur) {
            if (pool[u].l >= 0) nxt.push_back(pool[u].l);
            if (pool[u].r >= 0) nxt.push_back(pool[u].r);
        }
        cur = nxt; lv++;
    }
    cout << bw << " " << bl << "\n";
    return 0;
}
""",
)

def _oracle_81(text: str) -> str:
    d = text.split()
    n, q = int(d[0]), int(d[1])
    pre = [int(v) for v in d[2:2 + n]]
    ino = [int(v) for v in d[2 + n:2 + 2 * n]]
    par: dict[int, int] = {}
    dep: dict[int, int] = {}

    def build(pl: int, pr: int, il: int, ir: int, p: int, depth: int) -> None:
        if pl > pr:
            return
        root = pre[pl]
        par[root] = p
        dep[root] = depth
        k = ino.index(root, il, ir + 1)
        ln = k - il
        build(pl + 1, pl + ln, il, k - 1, root, depth + 1)
        build(pl + ln + 1, pr, k + 1, ir, root, depth + 1)

    build(0, n - 1, 0, n - 1, 0, 0)
    idx = 2 + 2 * n
    out = []
    for _ in range(q):
        u, v = int(d[idx]), int(d[idx + 1]); idx += 2
        while dep[u] > dep[v]:
            u = par[u]
        while dep[v] > dep[u]:
            v = par[v]
        while u != v:
            u = par[u]
            v = par[v]
        out.append(str(u))
    return "\n".join(out) + "\n"

add(
    title="二叉树的最近公共祖先（LCA）",
    section="第 05 讲 · 树和二叉树",
    difficulty=3, score=20, tags=["二叉树", "LCA", "最近公共祖先", "递归"],
    statement_md=(
        "给定一棵 `N` 个结点的二叉树的**先序遍历**和**中序遍历**（结点值互不相同），"
        "以及 `Q` 次询问 `(u, v)`，每次输出结点 `u` 和 `v` 的**最近公共祖先（LCA）**。\n\n"
        "★ 递归求 LCA 的经典三分支：\n"
        "- 若当前根为空，或等于 `u` 或 `v`，直接返回当前根；\n"
        "- 递归查左子树和右子树：若两边都返回非空，说明 `u`、`v` 分居左右两侧，当前根就是 LCA；\n"
        "- 否则哪边非空就返回哪边！"
    ),
    input_format=(
        "第一行两个正整数 `N Q`。\n\n"
        "第二行 `N` 个整数（先序遍历）。\n\n"
        "第三行 `N` 个整数（中序遍历）。\n\n"
        "随后 `Q` 行，每行两个整数 `u v`（保证在树中）。"
    ),
    output_format="`Q` 行，每行输出对应询问的最近公共祖先结点值。",
    constraints_md="- 1 ≤ N ≤ 200\n- 1 ≤ Q ≤ 200",
    inputs=[
        "8 4\n5 3 2 1 4 8 6 7\n1 2 3 4 5 6 7 8\n1 4\n2 4\n6 7\n1 7\n",
        "3 2\n1 2 3\n2 1 3\n2 3\n2 1\n",
        "5 3\n1 2 3 4 5\n5 4 3 2 1\n5 3\n4 2\n1 5\n",
    ],
    samples=2,
    oracle=_oracle_81,
    solution=r"""#include <stdio.h>
#include <stdlib.h>
typedef struct Node { int v; struct Node *l, *r; } Node;
int pre[205], ino[205];
Node *build(int pl, int pr, int il, int ir) {
    if (pl > pr) return NULL;
    int root = pre[pl], k = il;
    while (ino[k] != root) k++;
    int ln = k - il;
    Node *t = (Node *)malloc(sizeof(Node));
    t->v = root;
    t->l = build(pl + 1, pl + ln, il, k - 1);
    t->r = build(pl + ln + 1, pr, k + 1, ir);
    return t;
}
Node *lca(Node *t, int u, int v) {
    if (!t || t->v == u || t->v == v) return t;
    Node *L = lca(t->l, u, v);
    Node *R = lca(t->r, u, v);
    if (L && R) return t;
    return L ? L : R;
}
int main(void) {
    int n, q;
    scanf("%d %d", &n, &q);
    for (int i = 0; i < n; i++) scanf("%d", &pre[i]);
    for (int i = 0; i < n; i++) scanf("%d", &ino[i]);
    Node *root = build(0, n - 1, 0, n - 1);
    while (q--) {
        int u, v; scanf("%d %d", &u, &v);
        printf("%d\n", lca(root, u, v)->v);
    }
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
#include <map>
#include <functional>
using namespace std;
int main() {
    int n, q; cin >> n >> q;
    vector<int> pre(n), ino(n);
    for (int &x : pre) cin >> x;
    for (int &x : ino) cin >> x;
    map<int, int> par, dep;
    function<void(int, int, int, int, int, int)> go = [&](int pl, int pr, int il, int ir, int p, int d) {
        if (pl > pr) return;
        int root = pre[pl], k = il;
        while (ino[k] != root) k++;
        int ln = k - il;
        par[root] = p; dep[root] = d;
        go(pl + 1, pl + ln, il, k - 1, root, d + 1);
        go(pl + ln + 1, pr, k + 1, ir, root, d + 1);
    };
    go(0, n - 1, 0, n - 1, 0, 0);
    while (q--) {
        int u, v; cin >> u >> v;
        while (dep[u] > dep[v]) u = par[u];
        while (dep[v] > dep[u]) v = par[v];
        while (u != v) { u = par[u]; v = par[v]; }
        cout << u << "\n";
    }
    return 0;
}
""",
)

def _oracle_82(text: str) -> str:
    import heapq
    d = text.split()
    n = int(d[0])
    w = [int(v) for v in d[1:1 + n]]
    if n <= 1:
        return "0\n"
    heapq.heapify(w)
    cost = 0
    while len(w) > 1:
        a = heapq.heappop(w)
        b = heapq.heappop(w)
        cost += a + b
        heapq.heappush(w, a + b)
    return "%d\n" % cost

add(
    title="修理牧场",
    section="第 05 讲 · 树和二叉树",
    difficulty=2, score=15, tags=["哈夫曼树", "优先队列", "贪心", "锯木头"],
    statement_md=(
        "PTA 经典题 `05-树8 修理牧场`：农夫要把一根长木头锯成给定的 `N` 段。\n"
        "每次把一根长度为 `L` 的木头锯成两段，需要花费 `L` 个铜板。\n"
        "求把木头锯成这 `N` 段的**最少总花费**。\n\n"
        "★ 逆向思维：正向看是「一根长木头不断一分为二」，倒过来看就是"
        "「每次挑两根最短的木头粘合起来」—— 花费恰好等于**哈夫曼树的带权路径长度 WPL**！\n"
        "注意边界：若 `N = 1`，木头本来就是一整段，一刀都不用锯，花费为 `0`。"
    ),
    input_format="第一行正整数 `N`。\n\n第二行 `N` 个正整数，表示每段木头的长度。",
    output_format="一行一个整数，表示最少总花费。",
    constraints_md="- 1 ≤ N ≤ 10000\n- 每段长度 ≤ 10^5",
    inputs=[
        "8\n4 5 1 2 1 3 1 1\n",
        "1\n25\n",
        "3\n8 5 8\n",
        "4\n10 20 30 40\n",
    ],
    samples=2,
    oracle=_oracle_82,
    solution=r"""#include <iostream>
#include <queue>
#include <vector>
using namespace std;
int main() {
    int n; cin >> n;
    priority_queue<long long, vector<long long>, greater<long long>> pq;
    for (int i = 0; i < n; i++) { long long v; cin >> v; pq.push(v); }
    long long ans = 0;
    while (pq.size() > 1) {
        long long a = pq.top(); pq.pop();
        long long b = pq.top(); pq.pop();
        ans += a + b;
        pq.push(a + b);
    }
    cout << ans << "\n";
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
using namespace std;
/* 另一套：双队列线性哈夫曼算法（初始排序放 q1，合成结点放 q2，永远单调递增） */
int main() {
    int n; cin >> n;
    vector<long long> a(n);
    for (auto &v : a) cin >> v;
    if (n <= 1) { cout << 0 << "\n"; return 0; }
    sort(a.begin(), a.end());
    queue<long long> q1, q2;
    for (auto v : a) q1.push(v);
    auto pop_min = [&]() -> long long {
        if (q2.empty() || (!q1.empty() && q1.front() <= q2.front())) {
            long long v = q1.front(); q1.pop(); return v;
        }
        long long v = q2.front(); q2.pop(); return v;
    };
    long long ans = 0;
    for (int k = 1; k < n; k++) {
        long long s = pop_min() + pop_min();
        ans += s;
        q2.push(s);
    }
    cout << ans << "\n";
    return 0;
}
""",
)

def _oracle_83(text: str) -> str:
    import heapq
    d = text.split()
    n = int(d[0])
    w = [int(v) for v in d[1:1 + n]]
    hp = list(w)
    heapq.heapify(hp)
    wpl = 0
    while len(hp) > 1:
        a = heapq.heappop(hp)
        b = heapq.heappop(hp)
        wpl += a + b
        heapq.heappush(hp, a + b)
    m = int(d[1 + n])
    p = 2 + n
    out = [str(wpl)]
    for _ in range(m):
        codes = d[p:p + n]; p += n
        tot = sum(w[i] * len(codes[i]) for i in range(n))
        sc = sorted(codes)
        prefix_free = all(not sc[i + 1].startswith(sc[i]) for i in range(n - 1))
        out.append("YES" if (tot == wpl and prefix_free) else "NO")
    return "\n".join(out) + "\n"

add(
    title="哈夫曼树",
    section="第 05 讲 · 树和二叉树",
    difficulty=4, score=25, tags=["哈夫曼树", "前缀编码", "最优性判定", "Trie"],
    statement_md=(
        "PTA 经典题 `Huffman Codes`：哈夫曼编码的形态**不唯一**（同权结点谁左谁右、谁先合并都可能不同），"
        "但任何一套合法的最优哈夫曼编码都必须同时满足两条铁律：\n\n"
        "1. **带权路径长度最优**：`Σ(w[i] × |code[i]|)` 恰好等于哈夫曼树的最小 `WPL`；\n"
        "2. **前缀码性质**：没有任何一个编码是另一个编码的前缀（即字符全部住在叶子上）。\n\n"
        "给定 `N` 个字符的权值与 `M` 套候选编码方案，请先输出最优 `WPL`，再逐套判定是否合法（`YES` / `NO`）。"
    ),
    input_format=(
        "第一行整数 `N`（2 ≤ N ≤ 60）。\n\n"
        "第二行 `N` 个正整数 `w[1..N]`。\n\n"
        "第三行正整数 `M`（候选方案数）。\n\n"
        "随后 `M` 组，每组 `N` 行，第 `i` 行为第 `i` 个字符的 `0/1` 编码串。"
    ),
    output_format="第一行输出最优 `WPL`；随后 `M` 行每行输出 `YES` 或 `NO`。",
    constraints_md="- 2 ≤ N ≤ 60\n- 1 ≤ M ≤ 20\n- 1 ≤ |编码串| ≤ 60",
    inputs=[
        "4\n1 1 3 3\n3\n000\n001\n01\n1\n01\n01\n0\n1\n00\n01\n10\n11\n",
        "3\n2 3 6\n2\n00\n01\n1\n0\n10\n11\n",
        "2\n5 5\n2\n0\n1\n0\n01\n",
    ],
    samples=2,
    oracle=_oracle_83,
    solution=r"""#include <iostream>
#include <vector>
#include <string>
#include <queue>
using namespace std;
struct Trie { int ch[2] = {0, 0}; bool end = false; };
int main() {
    int n; cin >> n;
    vector<long long> w(n);
    priority_queue<long long, vector<long long>, greater<long long>> pq;
    for (int i = 0; i < n; i++) { cin >> w[i]; pq.push(w[i]); }
    long long wpl = 0;
    while (pq.size() > 1) {
        long long a = pq.top(); pq.pop();
        long long b = pq.top(); pq.pop();
        wpl += a + b; pq.push(a + b);
    }
    cout << wpl << "\n";
    int m; cin >> m;
    while (m--) {
        vector<string> c(n);
        long long tot = 0;
        for (int i = 0; i < n; i++) { cin >> c[i]; tot += w[i] * (long long)c[i].size(); }
        vector<Trie> tr(1);
        bool ok = (tot == wpl);
        for (int i = 0; i < n && ok; i++) {
            int u = 0;
            for (char b : c[i]) {
                int d = b - '0';
                if (!tr[u].ch[d]) { tr[u].ch[d] = (int)tr.size(); tr.push_back(Trie()); }
                u = tr[u].ch[d];
                if (tr[u].end) ok = false;
            }
            if (tr[u].ch[0] || tr[u].ch[1]) ok = false;
            tr[u].end = true;
        }
        cout << (ok ? "YES\n" : "NO\n");
    }
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;
int main() {
    int n; cin >> n;
    vector<long long> w(n), hp;
    for (int i = 0; i < n; i++) { cin >> w[i]; hp.push_back(w[i]); }
    long long wpl = 0;
    while (hp.size() > 1) {
        sort(hp.begin(), hp.end());
        long long s = hp[0] + hp[1];
        wpl += s;
        hp.erase(hp.begin(), hp.begin() + 2);
        hp.push_back(s);
    }
    cout << wpl << "\n";
    int m; cin >> m;
    while (m--) {
        vector<string> c(n);
        long long tot = 0;
        for (int i = 0; i < n; i++) { cin >> c[i]; tot += w[i] * (long long)c[i].size(); }
        sort(c.begin(), c.end());
        bool ok = (tot == wpl);
        for (int i = 0; i + 1 < n && ok; i++)
            if (c[i + 1].compare(0, c[i].size(), c[i]) == 0) ok = false;
        cout << (ok ? "YES\n" : "NO\n");
    }
    return 0;
}
""",
)

def _oracle_84(text: str) -> str:
    d = text.split()
    n, m = int(d[0]), int(d[1])
    par = list(range(n + 1))
    sz = [1] * (n + 1)

    def find(x: int) -> int:
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            par[rb] = ra
            sz[ra] += sz[rb]

    p = 2
    for _ in range(m):
        k = int(d[p]); p += 1
        first = int(d[p]); p += 1
        for _ in range(k - 1):
            union(first, int(d[p])); p += 1
    return "%d\n" % max(sz[1:n + 1])

add(
    title="朋友圈",
    section="第 05 讲 · 树和二叉树",
    difficulty=2, score=15, tags=["并查集", "连通块大小", "等价类"],
    statement_md=(
        "PTA 经典题 `朋友圈`：学校里有 `N` 个学生（编号 `1` ~ `N`）和 `M` 个俱乐部。\n"
        "每个俱乐部里的学生都是朋友，而且「朋友的朋友也是朋友」（传递性）。"
        "请计算**最大的朋友圈**里有多少个学生。\n\n"
        "★ 并查集的经典「按大小合并」：维护 `sz[root]` 表示以 `root` 为代表元的集合大小，"
        "每次合并两个不同集合 `ru` 和 `rv` 时令 `sz[ru] += sz[rv]`；最后取 `max(sz)` 即可！"
    ),
    input_format=(
        "第一行两个整数 `N M`（学生总数、俱乐部个数）。\n\n"
        "随后 `M` 行，每行先给一个正整数 `k`，后跟 `k` 个学生编号。"
    ),
    output_format="一行一个整数，表示最大朋友圈的人数。",
    constraints_md="- 1 ≤ N ≤ 30000\n- 0 ≤ M ≤ 1000",
    inputs=[
        "7 4\n3 1 2 3\n2 1 4\n3 5 6 7\n1 6\n",
        "5 0\n",
        "6 3\n2 1 2\n2 3 4\n3 2 3 6\n",
        "4 2\n2 1 2\n2 1 2\n",
    ],
    samples=2,
    oracle=_oracle_84,
    solution=r"""#include <stdio.h>
int par[30005], sz[30005];
int find(int x) {
    while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }
    return x;
}
int main(void) {
    int n, m;
    scanf("%d %d", &n, &m);
    for (int i = 1; i <= n; i++) { par[i] = i; sz[i] = 1; }
    for (int i = 0; i < m; i++) {
        int k, first, x;
        scanf("%d %d", &k, &first);
        for (int j = 1; j < k; j++) {
            scanf("%d", &x);
            int a = find(first), b = find(x);
            if (a != b) { par[b] = a; sz[a] += sz[b]; }
        }
    }
    int best = 1;
    for (int i = 1; i <= n; i++) if (find(i) == i && sz[i] > best) best = sz[i];
    printf("%d\n", best);
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
#include <queue>
using namespace std;
/* 另一套：学生 (1..n) 与俱乐部 (n+1..n+m) 建二分图，跑 BFS 统计连通块里的学生数 */
int main() {
    int n, m; cin >> n >> m;
    vector<vector<int>> g(n + m + 1);
    for (int i = 1; i <= m; i++) {
        int k; cin >> k;
        while (k--) {
            int u; cin >> u;
            g[u].push_back(n + i);
            g[n + i].push_back(u);
        }
    }
    vector<char> vis(n + m + 1, 0);
    int best = 1;
    for (int s = 1; s <= n; s++) {
        if (vis[s]) continue;
        int cnt = 0;
        queue<int> q; q.push(s); vis[s] = 1;
        while (!q.empty()) {
            int u = q.front(); q.pop();
            if (u <= n) cnt++;
            for (int v : g[u]) if (!vis[v]) { vis[v] = 1; q.push(v); }
        }
        if (cnt > best) best = cnt;
    }
    cout << best << "\n";
    return 0;
}
""",
)

def _oracle_85(text: str) -> str:
    d = text.split()
    n = int(d[0])
    par = list(range(10005))
    seen = set()

    def find(x: int) -> int:
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    p = 1
    for _ in range(n):
        k = int(d[p]); p += 1
        first = int(d[p]); p += 1
        seen.add(first)
        for _ in range(k - 1):
            x = int(d[p]); p += 1
            seen.add(x)
            ra, rb = find(first), find(x)
            if ra != rb:
                par[rb] = ra
    tribes = sum(1 for u in seen if find(u) == u)
    q = int(d[p]); p += 1
    out = ["%d %d" % (len(seen), tribes)]
    for _ in range(q):
        u, v = int(d[p]), int(d[p + 1]); p += 2
        out.append("Y" if find(u) == find(v) else "N")
    return "\n".join(out) + "\n"

add(
    title="部落",
    section="第 05 讲 · 树和二叉树",
    difficulty=3, score=20, tags=["并查集", "连通分量", "L2-024"],
    statement_md=(
        "PTA 天梯赛经典题 `L2-024 部落`：社区里有若干个小圈子，只要两个人出现在同一个小圈子里，"
        "他们就属于同一个**部落**（部落关系具有传递性）。\n\n"
        "给定 `N` 个小圈子的成员名单，请你：\n"
        "1. 统计社区里的**总人数**（出现过的不同人员编号个数）与互不相交的**部落总数**；\n"
        "2. 对随后的 `Q` 次询问 `(u, v)`，判断两人是否属于同一个部落（输出 `Y` 或 `N`）。"
    ),
    input_format=(
        "第一行正整数 `N`（小圈子个数）。\n\n"
        "随后 `N` 行，每行格式为 `k p1 p2 ... pk`（圈子人数与成员编号，编号为 1~10000 内的正整数）。\n\n"
        "接着一行正整数 `Q`，随后 `Q` 行每行两个编号 `u v`。"
    ),
    output_format=(
        "第一行两个整数：`社区总人数 部落数`。\n\n"
        "随后 `Q` 行，每行输出 `Y` 或 `N`。"
    ),
    constraints_md="- 1 ≤ N, Q ≤ 1000\n- 1 ≤ 编号 ≤ 10000",
    inputs=[
        "4\n3 10 1 2\n2 3 4\n4 1 5 7 8\n3 9 6 4\n2\n10 5\n3 7\n",
        "2\n2 1 2\n2 3 4\n2\n1 2\n2 3\n",
        "3\n1 1\n1 2\n1 3\n2\n1 2\n1 1\n",
    ],
    samples=2,
    oracle=_oracle_85,
    solution=r"""#include <stdio.h>
int par[10005], seen[10005];
int find(int x) {
    while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }
    return x;
}
int main(void) {
    for (int i = 1; i <= 10000; i++) par[i] = i;
    int n;
    scanf("%d", &n);
    while (n--) {
        int k, first, x;
        scanf("%d %d", &k, &first);
        seen[first] = 1;
        for (int i = 1; i < k; i++) {
            scanf("%d", &x);
            seen[x] = 1;
            int a = find(first), b = find(x);
            if (a != b) par[b] = a;
        }
    }
    int tot = 0, tribes = 0;
    for (int i = 1; i <= 10000; i++) {
        if (seen[i]) {
            tot++;
            if (find(i) == i) tribes++;
        }
    }
    printf("%d %d\n", tot, tribes);
    int q;
    scanf("%d", &q);
    while (q--) {
        int u, v;
        scanf("%d %d", &u, &v);
        printf(find(u) == find(v) ? "Y\n" : "N\n");
    }
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
#include <queue>
using namespace std;
int main() {
    int n; cin >> n;
    vector<vector<int>> g(10005);
    vector<char> seen(10005, 0);
    while (n--) {
        int k, first; cin >> k >> first;
        seen[first] = 1;
        for (int i = 1; i < k; i++) {
            int x; cin >> x; seen[x] = 1;
            g[first].push_back(x);
            g[x].push_back(first);
        }
    }
    vector<int> comp(10005, 0);
    int tot = 0, cid = 0;
    for (int i = 1; i <= 10000; i++) {
        if (!seen[i]) continue;
        tot++;
        if (comp[i]) continue;
        cid++;
        queue<int> q; q.push(i); comp[i] = cid;
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (int v : g[u]) if (!comp[v]) { comp[v] = cid; q.push(v); }
        }
    }
    cout << tot << " " << cid << "\n";
    int qq; cin >> qq;
    while (qq--) {
        int u, v; cin >> u >> v;
        cout << (comp[u] == comp[v] ? "Y\n" : "N\n");
    }
    return 0;
}
""",
)

# --------------------------------------------------------------------- #
#  第 06 讲扩充：图的存储、遍历、最小生成树、最短路、拓扑与关键路径（循序渐进 + 举一反三）
# --------------------------------------------------------------------- #

def _oracle_86(text: str) -> str:
    d = text.split()
    n, m = int(d[0]), int(d[1])
    g = [[0] * n for _ in range(n)]
    p = 2
    for _ in range(m):
        u, v = int(d[p]) - 1, int(d[p + 1]) - 1; p += 2
        g[u][v] = g[v][u] = 1
    lines = [" ".join(map(str, row)) for row in g]
    lines.append(" ".join(str(sum(row)) for row in g))
    return "\n".join(lines) + "\n"

add(
    title="邻接矩阵表示法创建无向图",
    section="第 06 讲 · 图",
    difficulty=1, score=10, tags=["图", "邻接矩阵", "顶点度"],
    statement_md=(
        "用**邻接矩阵**表示一个含 `n` 个顶点（编号 `1` ~ `n`）、`m` 条边的无向图，"
        "输出该 `n × n` 的 `0/1` 邻接矩阵，并在最后一行输出每个顶点的**度（degree）**。\n\n"
        "★ 无向图邻接矩阵的两条基本性质：\n"
        "1. 矩阵一定关于主对角线**对称**（读入边 `(u, v)` 时必须同时置 `G[u][v] = G[v][u] = 1`）；\n"
        "2. 第 `i` 行（或第 `i` 列）元素之和就是顶点 `i` 的**度**！"
    ),
    input_format="第一行两个整数 `n m`。\n\n随后 `m` 行，每行两个整数 `u v` 表示一条无向边（无重边、无自环）。",
    output_format="前 `n` 行输出邻接矩阵（每行 `n` 个 `0/1` 整数，空格分隔）；第 `n+1` 行输出 `n` 个顶点的度（空格分隔）。",
    constraints_md="- 1 ≤ n ≤ 100\n- 0 ≤ m ≤ n(n-1)/2",
    inputs=[
        "4 5\n1 2\n1 3\n1 4\n2 3\n3 4\n",
        "3 1\n2 3\n",
        "1 0\n",
        "4 6\n1 2\n1 3\n1 4\n2 3\n2 4\n3 4\n",
    ],
    samples=2,
    oracle=_oracle_86,
    solution=r"""#include <stdio.h>
int g[105][105], deg[105];
int main(void) {
    int n, m;
    scanf("%d %d", &n, &m);
    for (int k = 0; k < m; k++) {
        int u, v;
        scanf("%d %d", &u, &v);
        g[u][v] = g[v][u] = 1;
    }
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            printf(j > 1 ? " %d" : "%d", g[i][j]);
            deg[i] += g[i][j];
        }
        printf("\n");
    }
    for (int i = 1; i <= n; i++) printf(i > 1 ? " %d" : "%d", deg[i]);
    printf("\n");
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
#include <numeric>
using namespace std;
int main() {
    int n, m; cin >> n >> m;
    vector<vector<int>> g(n, vector<int>(n, 0));
    while (m--) {
        int u, v; cin >> u >> v;
        --u; --v;
        g[u][v] = g[v][u] = 1;
    }
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) cout << (j ? " " : "") << g[i][j];
        cout << "\n";
    }
    for (int i = 0; i < n; i++)
        cout << (i ? " " : "") << accumulate(g[i].begin(), g[i].end(), 0);
    cout << "\n";
    return 0;
}
""",
)

def _oracle_87(text: str) -> str:
    d = text.split()
    n, m = int(d[0]), int(d[1])
    adj = [[] for _ in range(n + 1)]
    p = 2
    for _ in range(m):
        u, v = int(d[p]), int(d[p + 1]); p += 2
        adj[u].append(v)
        adj[v].append(u)
    return "\n".join(" ".join([str(i) + ":"] + [str(v) for v in adj[i]])
                     for i in range(1, n + 1)) + "\n"

add(
    title="邻接表创建无向图",
    section="第 06 讲 · 图",
    difficulty=1, score=10, tags=["图", "邻接表", "尾插法"],
    statement_md=(
        "读入一个无向图，用**尾插法（保持输入顺序）**建立邻接表，"
        "然后按顶点编号 `1` ~ `n` 依次输出每个顶点的邻接点链表。\n\n"
        "★ 与「无向图的邻接表（头插法）」对照：\n"
        "- **头插法**把新边插在链头，邻接点顺序与输入顺序**相反**；\n"
        "- **尾插法**（或 C++ `vector::push_back`）把新边挂在链尾，邻接点顺序与输入顺序**一致**。"
    ),
    input_format="第一行 `n m`（顶点数、边数）。\n\n接下来 `m` 行，每行 `u v` 表示一条无向边。",
    output_format="`n` 行，第 `i` 行为 `i: v1 v2 ...`（按输入先后顺序排列；孤立顶点输出 `i:`）。",
    constraints_md="- 1 ≤ n ≤ 100\n- 0 ≤ m ≤ n(n-1)/2",
    inputs=[
        "4 5\n1 2\n1 3\n1 4\n2 3\n3 4\n",
        "3 1\n2 3\n",
        "1 0\n",
        "5 4\n1 5\n1 3\n2 4\n3 5\n",
    ],
    samples=2,
    oracle=_oracle_87,
    solution=r"""#include <stdio.h>
int head[105], tail[105], nxt[4005], to[4005], ecnt = 0;
void add_tail(int u, int v) {
    ++ecnt; to[ecnt] = v; nxt[ecnt] = 0;
    if (!head[u]) head[u] = tail[u] = ecnt;
    else { nxt[tail[u]] = ecnt; tail[u] = ecnt; }
}
int main(void) {
    int n, m;
    scanf("%d %d", &n, &m);
    for (int k = 0; k < m; k++) {
        int u, v; scanf("%d %d", &u, &v);
        add_tail(u, v); add_tail(v, u);
    }
    for (int i = 1; i <= n; i++) {
        printf("%d:", i);
        for (int e = head[i]; e; e = nxt[e]) printf(" %d", to[e]);
        printf("\n");
    }
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
using namespace std;
int main() {
    int n, m; cin >> n >> m;
    vector<vector<int>> adj(n + 1);
    while (m--) {
        int u, v; cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    for (int i = 1; i <= n; i++) {
        cout << i << ":";
        for (int v : adj[i]) cout << " " << v;
        cout << "\n";
    }
    return 0;
}
""",
)

def _oracle_88(text: str) -> str:
    d = text.split()
    n, m = int(d[0]), int(d[1])
    adj = [[] for _ in range(n + 1)]
    p = 2
    for _ in range(m):
        u, v = int(d[p]), int(d[p + 1]); p += 2
        adj[u].append(v); adj[v].append(u)
    for i in range(1, n + 1):
        adj[i].sort()
    vis = [False] * (n + 1)
    order = []

    def dfs(u: int) -> None:
        vis[u] = True
        order.append(str(u))
        for v in adj[u]:
            if not vis[v]:
                dfs(v)

    for i in range(1, n + 1):
        if not vis[i]:
            dfs(i)
    return " ".join(order) + "\n"

add(
    title="图深度优先遍历",
    section="第 06 讲 · 图",
    difficulty=2, score=15, tags=["图", "DFS", "深度优先遍历"],
    statement_md=(
        "给定一个含 `n` 个顶点（编号 `1` ~ `n`）和 `m` 条边的无向图，"
        "输出它的**深度优先遍历（DFS）**序列。\n\n"
        "★ 为保证遍历序列唯一，约定：\n"
        "1. 外层按顶点编号 `1 → n` 依次检查，若未访问则从该顶点发起一次 DFS（处理非连通图）；\n"
        "2. 每个顶点扩展邻居时，一律按**邻接点编号从小到大**访问。"
    ),
    input_format="第一行 `n m`。\n\n随后 `m` 行，每行 `u v` 表示一条无向边。",
    output_format="一行 `n` 个整数（空格分隔），表示全图的 DFS 访问序列。",
    constraints_md="- 1 ≤ n ≤ 100\n- 0 ≤ m ≤ n(n-1)/2",
    inputs=[
        "5 5\n1 2\n1 4\n2 3\n2 5\n3 5\n",
        "4 2\n1 3\n2 4\n",
        "1 0\n",
        "6 5\n1 6\n1 3\n3 2\n3 5\n2 4\n",
    ],
    samples=2,
    oracle=_oracle_88,
    solution=r"""#include <stdio.h>
int g[105][105], vis[105], n, m, first = 1;
void dfs(int u) {
    vis[u] = 1;
    printf(first ? "%d" : " %d", u);
    first = 0;
    for (int v = 1; v <= n; v++)
        if (g[u][v] && !vis[v]) dfs(v);
}
int main(void) {
    scanf("%d %d", &n, &m);
    for (int k = 0; k < m; k++) {
        int u, v; scanf("%d %d", &u, &v);
        g[u][v] = g[v][u] = 1;
    }
    for (int i = 1; i <= n; i++)
        if (!vis[i]) dfs(i);
    printf("\n");
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
/* 另一套：邻接表排序 + 显式栈模拟非递归 DFS */
int main() {
    int n, m; cin >> n >> m;
    vector<vector<int>> adj(n + 1);
    while (m--) {
        int u, v; cin >> u >> v;
        adj[u].push_back(v); adj[v].push_back(u);
    }
    for (int i = 1; i <= n; i++)
        sort(adj[i].rbegin(), adj[i].rend()); // 逆序压栈，栈顶就是最小编号
    vector<char> vis(n + 1, 0);
    vector<int> out;
    for (int s = 1; s <= n; s++) {
        if (vis[s]) continue;
        vector<int> st{s};
        while (!st.empty()) {
            int u = st.back(); st.pop_back();
            if (vis[u]) continue;
            vis[u] = 1;
            out.push_back(u);
            for (int v : adj[u]) if (!vis[v]) st.push_back(v);
        }
    }
    for (size_t i = 0; i < out.size(); i++) cout << (i ? " " : "") << out[i];
    cout << "\n";
    return 0;
}
""",
)

def _oracle_89(text: str) -> str:
    d = text.split()
    n, m = int(d[0]), int(d[1])
    g = [[False] * n for _ in range(n)]
    p = 2
    for _ in range(m):
        u, v = int(d[p]), int(d[p + 1]); p += 2
        g[u][v] = g[v][u] = True
    out = []
    vis = [False] * n

    def dfs(u: int, comp: list[int]) -> None:
        vis[u] = True
        comp.append(u)
        for v in range(n):
            if g[u][v] and not vis[v]:
                dfs(v, comp)

    for i in range(n):
        if not vis[i]:
            c: list[int] = []
            dfs(i, c)
            out.append("{ " + " ".join(map(str, c)) + " }")

    vis = [False] * n
    for i in range(n):
        if not vis[i]:
            c = []
            q = [i]
            vis[i] = True
            while q:
                u = q.pop(0)
                c.append(u)
                for v in range(n):
                    if g[u][v] and not vis[v]:
                        vis[v] = True
                        q.append(v)
            out.append("{ " + " ".join(map(str, c)) + " }")
    return "\n".join(out) + "\n"

add(
    title="列出连通集",
    section="第 06 讲 · 图",
    difficulty=2, score=15, tags=["图", "DFS", "BFS", "连通分量", "06-图1"],
    statement_md=(
        "PTA 经典题 `06-图1 列出连通集`：给定一个有 `N` 个顶点（编号 `0` ~ `N-1`）和 `E` 条边的无向图，"
        "请分别用 **DFS** 和 **BFS** 找出图中的所有连通集。\n\n"
        "约定：遍历时总是从编号最小的未访问顶点出发，访问邻接点时也按编号**从小到大**的顺序访问。"
        "每个连通集输出一行，格式为 `{ v1 v2 ... vk }`。"
    ),
    input_format="第一行两个整数 `N E`（1 ≤ N ≤ 15）。\n\n随后 `E` 行，每行两个整数 `u v` 表示一条无向边。",
    output_format="先按 DFS 顺序输出所有连通集（每行一个 `{ ... }`），再按 BFS 顺序输出所有连通集。",
    constraints_md="- 1 ≤ N ≤ 15\n- 0 ≤ E ≤ N(N-1)/2",
    inputs=[
        "8 6\n0 7\n0 1\n2 0\n4 1\n2 4\n3 5\n",
        "4 0\n",
        "5 4\n0 1\n1 2\n2 3\n3 4\n",
        "6 5\n0 2\n0 4\n2 1\n1 4\n3 5\n",
    ],
    samples=2,
    oracle=_oracle_89,
    solution=r"""#include <stdio.h>
int g[20][20], vis[20], q[20], n, e;
void dfs(int u) {
    vis[u] = 1;
    printf(" %d", u);
    for (int v = 0; v < n; v++)
        if (g[u][v] && !vis[v]) dfs(v);
}
int main(void) {
    scanf("%d %d", &n, &e);
    for (int k = 0; k < e; k++) {
        int u, v; scanf("%d %d", &u, &v);
        g[u][v] = g[v][u] = 1;
    }
    for (int i = 0; i < n; i++) {
        if (!vis[i]) {
            printf("{");
            dfs(i);
            printf(" }\n");
        }
    }
    for (int i = 0; i < n; i++) vis[i] = 0;
    for (int i = 0; i < n; i++) {
        if (!vis[i]) {
            printf("{");
            int f = 0, r = 0;
            q[r++] = i; vis[i] = 1;
            while (f < r) {
                int u = q[f++];
                printf(" %d", u);
                for (int v = 0; v < n; v++)
                    if (g[u][v] && !vis[v]) { vis[v] = 1; q[r++] = v; }
            }
            printf(" }\n");
        }
    }
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <functional>
using namespace std;
int main() {
    int n, e; cin >> n >> e;
    vector<vector<int>> adj(n);
    while (e--) {
        int u, v; cin >> u >> v;
        adj[u].push_back(v); adj[v].push_back(u);
    }
    for (int i = 0; i < n; i++) sort(adj[i].begin(), adj[i].end());
    vector<char> vis(n, 0);
    function<void(int)> dfs = [&](int u) {
        vis[u] = 1;
        cout << " " << u;
        for (int v : adj[u]) if (!vis[v]) dfs(v);
    };
    for (int i = 0; i < n; i++)
        if (!vis[i]) { cout << "{"; dfs(i); cout << " }\n"; }
    fill(vis.begin(), vis.end(), 0);
    for (int i = 0; i < n; i++) {
        if (vis[i]) continue;
        cout << "{";
        queue<int> q; q.push(i); vis[i] = 1;
        while (!q.empty()) {
            int u = q.front(); q.pop();
            cout << " " << u;
            for (int v : adj[u]) if (!vis[v]) { vis[v] = 1; q.push(v); }
        }
        cout << " }\n";
    }
    return 0;
}
""",
)

def _oracle_90(text: str) -> str:
    d = text.split()
    n, m = int(d[0]), int(d[1])
    deg = [0] * (n + 1)
    par = list(range(n + 1))

    def find(x: int) -> int:
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    p = 2
    for _ in range(m):
        u, v = int(d[p]), int(d[p + 1]); p += 2
        deg[u] += 1; deg[v] += 1
        ru, rv = find(u), find(v)
        if ru != rv:
            par[rv] = ru
    comps = sum(1 for i in range(1, n + 1) if find(i) == i)
    ok = (comps == 1) and all(deg[i] > 0 and deg[i] % 2 == 0 for i in range(1, n + 1))
    return ("1\n" if ok else "0\n")

add(
    title="哥尼斯堡的“七桥问题”",
    section="第 06 讲 · 图",
    difficulty=2, score=15, tags=["图", "欧拉回路", "连通性", "顶点度"],
    statement_md=(
        "PTA 经典题 `08-图9 哥尼斯堡的“七桥问题”`：给定一个含 `N` 个顶点（编号 `1` ~ `N`）和 `M` 条边的无向图，"
        "判断是否存在一条从某个顶点出发、**每条边恰好走一次**并回到起点的回路（即**欧拉回路**）。\n\n"
        "★ 最容易漏掉的坑：**只判「所有顶点度数为偶数」不够，必须同时检查图是否连通！**\n"
        "比如两个互不相连的三角形，每个顶点的度都是 2（全偶），但你不可能一笔画走完两个三角形！"
    ),
    input_format="第一行两个正整数 `N M`。\n\n随后 `M` 行，每行两个整数 `u v` 表示一条无向边。",
    output_format="一行，若存在欧拉回路输出 `1`，否则输出 `0`。",
    constraints_md="- 1 ≤ N ≤ 1000\n- 0 ≤ M ≤ 5000",
    inputs=[
        "6 10\n1 2\n2 3\n3 1\n4 5\n5 6\n6 4\n1 4\n1 6\n3 4\n3 6\n",
        "7 12\n1 2\n1 3\n1 4\n2 3\n3 4\n4 7\n2 5\n2 6\n5 6\n5 7\n6 7\n3 6\n",
        "6 6\n1 2\n2 3\n3 1\n4 5\n5 6\n6 4\n",
        "4 4\n1 2\n2 3\n3 4\n4 1\n",
    ],
    samples=2,
    oracle=_oracle_90,
    solution=r"""#include <stdio.h>
int par[1005], deg[1005];
int find(int x) {
    while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }
    return x;
}
int main(void) {
    int n, m;
    scanf("%d %d", &n, &m);
    for (int i = 1; i <= n; i++) par[i] = i;
    for (int k = 0; k < m; k++) {
        int u, v; scanf("%d %d", &u, &v);
        deg[u]++; deg[v]++;
        int a = find(u), b = find(v);
        if (a != b) par[b] = a;
    }
    int comps = 0, ok = 1;
    for (int i = 1; i <= n; i++) {
        if (find(i) == i) comps++;
        if (deg[i] == 0 || deg[i] % 2 != 0) ok = 0;
    }
    if (comps != 1) ok = 0;
    printf("%d\n", ok);
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
#include <queue>
using namespace std;
int main() {
    int n, m; cin >> n >> m;
    vector<vector<int>> g(n + 1);
    while (m--) {
        int u, v; cin >> u >> v;
        g[u].push_back(v); g[v].push_back(u);
    }
    vector<char> vis(n + 1, 0);
    queue<int> q; q.push(1); vis[1] = 1;
    int seen = 0;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        seen++;
        for (int v : g[u]) if (!vis[v]) { vis[v] = 1; q.push(v); }
    }
    bool ok = (seen == n);
    for (int i = 1; i <= n; i++)
        if (g[i].empty() || g[i].size() % 2 != 0) ok = false;
    cout << (ok ? 1 : 0) << "\n";
    return 0;
}
""",
)

def _oracle_91(text: str) -> str:
    d = text.split()
    n, m = int(d[0]), int(d[1])
    deg = [0] * (n + 1)
    par = list(range(n + 1))

    def find(x: int) -> int:
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    p = 2
    for _ in range(m):
        u, v = int(d[p]), int(d[p + 1]); p += 2
        deg[u] += 1; deg[v] += 1
        ru, rv = find(u), find(v)
        if ru != rv:
            par[rv] = ru
    comps = sum(1 for i in range(1, n + 1) if find(i) == i)
    odd = sum(1 for i in range(1, n + 1) if deg[i] % 2 == 1)
    if comps != 1:
        return "Non-Eulerian\n"
    if odd == 0:
        return "Eulerian Circuit\n"
    if odd == 2:
        return "Eulerian Path\n"
    return "Non-Eulerian\n"

add(
    title="欧拉通路与欧拉回路判定",
    section="第 06 讲 · 图",
    difficulty=2, score=15, tags=["图", "欧拉通路", "欧拉回路", "奇度顶点"],
    statement_md=(
        "由「哥尼斯堡七桥问题」举一反三：给定一个含 `N` 个顶点（编号 `1` ~ `N`）和 `M` 条边（`M ≥ 1`）的无向图，"
        "判断它的欧拉性质（要求全部 `N` 个顶点连通）：\n\n"
        "- 若连通且**奇度顶点个数为 0** → 存在欧拉回路，输出 `Eulerian Circuit`；\n"
        "- 若连通且**奇度顶点个数恰为 2** → 存在欧拉通路（半欧拉图，可一笔画但起终点不同），输出 `Eulerian Path`；\n"
        "- 若不连通或奇度顶点数为其它值 → 输出 `Non-Eulerian`。"
    ),
    input_format="第一行两个正整数 `N M`。\n\n随后 `M` 行，每行两个整数 `u v` 表示一条无向边。",
    output_format="一行，输出 `Eulerian Circuit`、`Eulerian Path` 或 `Non-Eulerian`。",
    constraints_md="- 2 ≤ N ≤ 1000\n- 1 ≤ M ≤ 5000",
    inputs=[
        "4 4\n1 2\n2 3\n3 4\n4 1\n",
        "4 5\n1 2\n2 3\n3 4\n4 1\n1 3\n",
        "4 6\n1 2\n1 3\n1 4\n2 3\n2 4\n3 4\n",
        "4 2\n1 2\n3 4\n",
    ],
    samples=3,
    oracle=_oracle_91,
    solution=r"""#include <stdio.h>
int par[1005], deg[1005];
int find(int x) {
    while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }
    return x;
}
int main(void) {
    int n, m;
    scanf("%d %d", &n, &m);
    for (int i = 1; i <= n; i++) par[i] = i;
    for (int k = 0; k < m; k++) {
        int u, v; scanf("%d %d", &u, &v);
        deg[u]++; deg[v]++;
        int a = find(u), b = find(v);
        if (a != b) par[b] = a;
    }
    int comps = 0, odd = 0;
    for (int i = 1; i <= n; i++) {
        if (find(i) == i) comps++;
        if (deg[i] % 2 == 1) odd++;
    }
    if (comps != 1) printf("Non-Eulerian\n");
    else if (odd == 0) printf("Eulerian Circuit\n");
    else if (odd == 2) printf("Eulerian Path\n");
    else printf("Non-Eulerian\n");
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
#include <queue>
using namespace std;
int main() {
    int n, m; cin >> n >> m;
    vector<vector<int>> g(n + 1);
    while (m--) {
        int u, v; cin >> u >> v;
        g[u].push_back(v); g[v].push_back(u);
    }
    vector<char> vis(n + 1, 0);
    queue<int> q; q.push(1); vis[1] = 1;
    int seen = 0, odd = 0;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        seen++;
        for (int v : g[u]) if (!vis[v]) { vis[v] = 1; q.push(v); }
    }
    for (int i = 1; i <= n; i++) if (g[i].size() % 2 == 1) odd++;
    if (seen != n) cout << "Non-Eulerian\n";
    else if (odd == 0) cout << "Eulerian Circuit\n";
    else if (odd == 2) cout << "Eulerian Path\n";
    else cout << "Non-Eulerian\n";
    return 0;
}
""",
)

def _oracle_92(text: str) -> str:
    d = text.split()
    n, m = int(d[0]), int(d[1])
    edges = []
    p = 2
    for _ in range(m):
        u, v, w = int(d[p]), int(d[p + 1]), int(d[p + 2]); p += 3
        edges.append((w, u, v))
    edges.sort()
    par = list(range(n + 1))

    def find(x: int) -> int:
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    cost, cnt = 0, 0
    for w, u, v in edges:
        ru, rv = find(u), find(v)
        if ru != rv:
            par[rv] = ru
            cost += w
            cnt += 1
    return "%d\n" % (cost if cnt == n - 1 else -1)

add(
    title="公路村村通",
    section="第 06 讲 · 图",
    difficulty=3, score=20, tags=["图", "最小生成树", "Kruskal", "Prim"],
    statement_md=(
        "PTA 经典题 `08-图7 公路村村通`：现有 `N` 个村庄（编号 `1` ~ `N`）和 `M` 条候选公路及各自的造价，"
        "求让所有村庄都连通的**最低总造价**；若候选公路不足以连通所有村庄，输出 `-1`。\n\n"
        "★ 最小生成树（MST）的两套经典算法：\n"
        "- **Kruskal（加边法）**：边按权值升序排，用并查集判环，选够 `N-1` 条边即成；\n"
        "- **Prim（加点法）**：维护生成树到未选顶点的最短距离 `lowcost[]`，每轮拉进距离最小的顶点。"
    ),
    input_format="第一行两个整数 `N M`。\n\n随后 `M` 行，每行三个整数 `u v cost` 表示连接村庄 `u` 和 `v` 的公路造价。",
    output_format="一行一个整数：最小生成树的总造价；不连通输出 `-1`。",
    constraints_md="- 1 ≤ N ≤ 1000\n- 0 ≤ M ≤ 3000\n- 1 ≤ cost ≤ 10000",
    inputs=[
        "6 15\n1 2 5\n1 3 3\n1 4 7\n1 5 4\n1 6 2\n2 3 4\n2 4 6\n2 5 2\n2 6 6\n3 4 6\n3 5 1\n3 6 1\n4 5 10\n4 6 8\n5 6 3\n",
        "4 2\n1 2 3\n3 4 5\n",
        "1 0\n",
        "4 5\n1 2 1\n2 3 2\n3 4 3\n4 1 4\n1 3 5\n",
    ],
    samples=2,
    oracle=_oracle_92,
    solution=r"""#include <stdio.h>
#include <stdlib.h>
struct Edge { int u, v, w; } e[3005];
int par[1005];
int cmp(const void *a, const void *b) {
    return ((struct Edge *)a)->w - ((struct Edge *)b)->w;
}
int find(int x) {
    while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }
    return x;
}
int main(void) {
    int n, m;
    scanf("%d %d", &n, &m);
    for (int i = 0; i < m; i++) scanf("%d %d %d", &e[i].u, &e[i].v, &e[i].w);
    qsort(e, m, sizeof(struct Edge), cmp);
    for (int i = 1; i <= n; i++) par[i] = i;
    long long cost = 0;
    int cnt = 0;
    for (int i = 0; i < m; i++) {
        int a = find(e[i].u), b = find(e[i].v);
        if (a != b) { par[b] = a; cost += e[i].w; cnt++; }
    }
    printf("%lld\n", cnt == n - 1 ? cost : -1LL);
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
using namespace std;
/* 另一套：Prim 算法 O(N^2) */
int main() {
    int n, m; cin >> n >> m;
    const long long INF = (long long)1e15;
    vector<vector<long long>> g(n + 1, vector<long long>(n + 1, INF));
    while (m--) {
        int u, v; long long w; cin >> u >> v >> w;
        if (w < g[u][v]) g[u][v] = g[v][u] = w;
    }
    vector<long long> low(n + 1, INF);
    vector<char> in(n + 1, 0);
    low[1] = 0;
    long long cost = 0;
    for (int r = 0; r < n; r++) {
        int u = -1;
        for (int i = 1; i <= n; i++)
            if (!in[i] && low[i] < INF && (u < 0 || low[i] < low[u])) u = i;
        if (u < 0) { cout << -1 << "\n"; return 0; }
        in[u] = 1; cost += low[u];
        for (int v = 1; v <= n; v++)
            if (!in[v] && g[u][v] < low[v]) low[v] = g[u][v];
    }
    cout << cost << "\n";
    return 0;
}
""",
)

def _oracle_93(text: str) -> str:
    d = text.split()
    n, m = int(d[0]), int(d[1])
    edges = []
    p = 2
    for _ in range(m):
        u, v, bad, cost = int(d[p]), int(d[p + 1]), int(d[p + 2]), int(d[p + 3]); p += 4
        edges.append((bad, cost, u, v))
    edges.sort()
    par = list(range(n + 1))

    def find(x: int) -> int:
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    tot_bad, tot_cost, cnt = 0, 0, 0
    for bad, cost, u, v in edges:
        ru, rv = find(u), find(v)
        if ru != rv:
            par[rv] = ru
            tot_bad += bad
            tot_cost += cost
            cnt += 1
    if cnt < n - 1:
        return "-1\n"
    return "%d %d\n" % (tot_bad, tot_cost)

add(
    title="森森美图",
    section="第 06 讲 · 图",
    difficulty=4, score=25, tags=["图", "双权最小生成树", "Kruskal", "贪心"],
    statement_md=(
        "在风景区规划 `N` 个景点（编号 `1` ~ `N`）的步道网络，共有 `M` 条候选路线。\n"
        "每条路线 `(u, v)` 有两个指标：**破坏度 `bad`**（越小越美观）和**施工造价 `cost`**。\n\n"
        "请你选出 `N-1` 条路线使所有景点连通，要求：\n"
        "1. 首先让选出路线的**总破坏度最小**；\n"
        "2. 在破坏度相同的情况下，优先选择**造价更低**的边，使**总造价最小**。\n\n"
        "输出最优方案的 `总破坏度 总造价`；若无法连通全部景点，输出 `-1`。"
    ),
    input_format="第一行两个正整数 `N M`。\n\n随后 `M` 行，每行四个整数 `u v bad cost`。",
    output_format="一行两个整数：`总破坏度 总造价`；不连通输出 `-1`。",
    constraints_md="- 1 ≤ N ≤ 1000\n- 0 ≤ M ≤ 5000",
    inputs=[
        "4 5\n1 2 1 10\n1 2 1 6\n2 3 2 5\n2 3 1 8\n3 4 2 4\n",
        "5 6\n1 2 2 5\n2 3 2 3\n1 3 2 4\n3 4 1 10\n4 5 3 8\n3 5 3 2\n",
        "3 1\n1 2 1 5\n",
    ],
    samples=2,
    oracle=_oracle_93,
    solution=r"""#include <stdio.h>
#include <stdlib.h>
struct E { int u, v, bad, cost; } e[5005];
int par[1005];
int cmp(const void *a, const void *b) {
    const struct E *x = (const struct E *)a, *y = (const struct E *)b;
    if (x->bad != y->bad) return x->bad - y->bad;
    return x->cost - y->cost;
}
int find(int x) {
    while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }
    return x;
}
int main(void) {
    int n, m;
    scanf("%d %d", &n, &m);
    for (int i = 0; i < m; i++) scanf("%d %d %d %d", &e[i].u, &e[i].v, &e[i].bad, &e[i].cost);
    qsort(e, m, sizeof(struct E), cmp);
    for (int i = 1; i <= n; i++) par[i] = i;
    long long tb = 0, tc = 0;
    int cnt = 0;
    for (int i = 0; i < m; i++) {
        int a = find(e[i].u), b = find(e[i].v);
        if (a != b) { par[b] = a; tb += e[i].bad; tc += e[i].cost; cnt++; }
    }
    if (cnt < n - 1) printf("-1\n");
    else printf("%lld %lld\n", tb, tc);
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
#include <utility>
using namespace std;
/* 另一套：用二元组权值 (bad, cost) 跑 Prim 算法 */
int main() {
    int n, m; cin >> n >> m;
    const long long INF = (long long)1e15;
    pair<long long, long long> BIG = {INF, INF};
    vector<vector<pair<long long, long long>>> g(n + 1, vector<pair<long long, long long>>(n + 1, BIG));
    while (m--) {
        int u, v; long long b, c; cin >> u >> v >> b >> c;
        pair<long long, long long> w = {b, c};
        if (w < g[u][v]) g[u][v] = g[v][u] = w;
    }
    vector<pair<long long, long long>> low(n + 1, BIG);
    vector<char> in(n + 1, 0);
    low[1] = {0, 0};
    long long tb = 0, tc = 0;
    for (int r = 0; r < n; r++) {
        int u = -1;
        for (int i = 1; i <= n; i++)
            if (!in[i] && low[i] < BIG && (u < 0 || low[i] < low[u])) u = i;
        if (u < 0) { cout << -1 << "\n"; return 0; }
        in[u] = 1;
        tb += low[u].first; tc += low[u].second;
        for (int v = 1; v <= n; v++)
            if (!in[v] && g[u][v] < low[v]) low[v] = g[u][v];
    }
    cout << tb << " " << tc << "\n";
    return 0;
}
""",
)

def _oracle_94(text: str) -> str:
    d = text.split()
    n, m, s, t = int(d[0]), int(d[1]), int(d[2]), int(d[3])
    INF = 10**18
    w = [[INF] * (n + 1) for _ in range(n + 1)]
    p = 4
    for _ in range(m):
        u, v, c = int(d[p]), int(d[p + 1]), int(d[p + 2]); p += 3
        if c < w[u][v]:
            w[u][v] = c
    dist = [INF] * (n + 1)
    pre = [0] * (n + 1)
    done = [False] * (n + 1)
    dist[s] = 0
    for _ in range(n):
        x = -1
        for i in range(1, n + 1):
            if not done[i] and dist[i] < INF and (x < 0 or dist[i] < dist[x]):
                x = i
        if x < 0:
            break
        done[x] = True
        for y in range(1, n + 1):
            if w[x][y] < INF and dist[x] + w[x][y] < dist[y]:
                dist[y] = dist[x] + w[x][y]
                pre[y] = x
    if dist[t] == INF:
        return "-1\n"
    path = []
    cur = t
    while cur != 0:
        path.append(str(cur))
        cur = pre[cur]
    path.reverse()
    return "%d\n%s\n" % (dist[t], " -> ".join(path))

add(
    title="单源最短路径",
    section="第 06 讲 · 图",
    difficulty=3, score=20, tags=["图", "Dijkstra", "最短路径还原", "pre数组"],
    statement_md=(
        "在「单源最短路径（Dijkstra）」的基础上更进一步：给定边权非负的有向图、起点 `s` 和终点 `t`，"
        "不仅要求出 `s` 到 `t` 的最短距离，还要**完整还原并打印最短路径经过的顶点序列** `s -> ... -> t`。\n\n"
        "★ 路径还原靠的是前驱数组 `pre[]`：每当边 `x → y` 松弛成功（`dist[x] + w < dist[y]`）时，"
        "顺手记下 `pre[y] = x`；最后从终点 `t` 顺着 `pre` 一路倒推回 `s`，逆序输出即是完整路径！"
    ),
    input_format="第一行四个整数 `n m s t`。\n\n随后 `m` 行，每行三个整数 `u v w` 表示有向边 `u → v`（权值 `w > 0`）。",
    output_format="若不可达只输出一行 `-1`；若可达，第一行输出最短距离，第二行输出 `v1 -> v2 -> ... -> vk`。",
    constraints_md="- 1 ≤ n ≤ 100\n- 0 ≤ m ≤ 2000\n- 测试数据保证最短路径唯一",
    inputs=[
        "5 7 1 5\n1 2 10\n1 4 30\n1 5 100\n2 3 50\n3 5 10\n4 3 20\n4 5 60\n",
        "4 4 1 4\n1 2 1\n2 3 2\n3 4 3\n1 4 10\n",
        "3 1 1 3\n1 2 5\n",
        "3 2 2 2\n1 2 3\n2 3 4\n",
    ],
    samples=2,
    oracle=_oracle_94,
    solution=r"""#include <stdio.h>
#define INF 1000000000LL
long long w[105][105], dist[105];
int pre[105], done[105], stk[105];
int main(void) {
    int n, m, s, t;
    scanf("%d %d %d %d", &n, &m, &s, &t);
    for (int i = 1; i <= n; i++) {
        dist[i] = INF;
        for (int j = 1; j <= n; j++) w[i][j] = INF;
    }
    for (int k = 0; k < m; k++) {
        int u, v; long long c;
        scanf("%d %d %lld", &u, &v, &c);
        if (c < w[u][v]) w[u][v] = c;
    }
    dist[s] = 0;
    for (int r = 0; r < n; r++) {
        int x = -1;
        for (int i = 1; i <= n; i++)
            if (!done[i] && dist[i] < INF && (x < 0 || dist[i] < dist[x])) x = i;
        if (x < 0) break;
        done[x] = 1;
        for (int y = 1; y <= n; y++)
            if (w[x][y] < INF && dist[x] + w[x][y] < dist[y]) {
                dist[y] = dist[x] + w[x][y];
                pre[y] = x;
            }
    }
    if (dist[t] >= INF) { printf("-1\n"); return 0; }
    printf("%lld\n", dist[t]);
    int top = 0;
    for (int cur = t; cur != 0; cur = pre[cur]) stk[top++] = cur;
    for (int i = top - 1; i >= 0; i--)
        printf(i == top - 1 ? "%d" : " -> %d", stk[i]);
    printf("\n");
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
using namespace std;
int main() {
    int n, m, s, t; cin >> n >> m >> s >> t;
    const long long INF = (long long)1e15;
    vector<vector<pair<int, long long>>> adj(n + 1);
    while (m--) {
        int u, v; long long c; cin >> u >> v >> c;
        adj[u].push_back({v, c});
    }
    vector<long long> dist(n + 1, INF);
    vector<int> pre(n + 1, 0);
    priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<pair<long long, int>>> pq;
    dist[s] = 0; pq.push({0, s});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d > dist[u]) continue;
        for (auto [v, c] : adj[u]) {
            if (dist[u] + c < dist[v]) {
                dist[v] = dist[u] + c;
                pre[v] = u;
                pq.push({dist[v], v});
            }
        }
    }
    if (dist[t] >= INF) { cout << -1 << "\n"; return 0; }
    cout << dist[t] << "\n";
    vector<int> path;
    for (int cur = t; cur != 0; cur = pre[cur]) path.push_back(cur);
    reverse(path.begin(), path.end());
    for (size_t i = 0; i < path.size(); i++)
        cout << (i ? " -> " : "") << path[i];
    cout << "\n";
    return 0;
}
""",
)

def _oracle_95(text: str) -> str:
    d = text.split()
    n, m, q = int(d[0]), int(d[1]), int(d[2])
    INF = 10**18
    dist = [[INF] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dist[i][i] = 0
    p = 3
    for _ in range(m):
        u, v, w = int(d[p]), int(d[p + 1]), int(d[p + 2]); p += 3
        if w < dist[u][v]:
            dist[u][v] = dist[v][u] = w
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    out = []
    for _ in range(q):
        u, v = int(d[p]), int(d[p + 1]); p += 2
        out.append(str(-1 if dist[u][v] >= INF else dist[u][v]))
    return "\n".join(out) + "\n"

add(
    title="最短路径",
    section="第 06 讲 · 图",
    difficulty=2, score=15, tags=["图", "无向有权图", "两点最短路"],
    statement_md=(
        "给定一个含 `N` 个顶点（编号 `1` ~ `N`）和 `M` 条无向带权边的无向图，"
        "回答 `Q` 次两点间的最短路径距离询问 `(s, t)`；若两点不连通，输出 `-1`。"
    ),
    input_format=(
        "第一行三个整数 `N M Q`。\n\n"
        "随后 `M` 行，每行三个整数 `u v w`（无向边，1 ≤ w ≤ 10000）。\n\n"
        "随后 `Q` 行，每行两个整数 `s t`。"
    ),
    output_format="`Q` 行，每行输出 `s` 到 `t` 的最短距离（不可达输出 `-1`）。",
    constraints_md="- 1 ≤ N ≤ 80\n- 0 ≤ M ≤ 2000\n- 1 ≤ Q ≤ 200",
    inputs=[
        "5 6 3\n1 2 2\n2 3 3\n1 3 10\n3 4 1\n1 4 8\n4 5 4\n1 3\n1 5\n2 4\n",
        "4 2 2\n1 2 5\n3 4 7\n1 2\n1 4\n",
        "3 3 2\n1 2 4\n1 2 2\n2 3 3\n1 3\n2 2\n",
    ],
    samples=2,
    oracle=_oracle_95,
    solution=r"""#include <stdio.h>
#define INF 1000000000000000LL
long long d[85][85];
int main(void) {
    int n, m, q;
    scanf("%d %d %d", &n, &m, &q);
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++)
            d[i][j] = (i == j) ? 0 : INF;
    for (int k = 0; k < m; k++) {
        int u, v; long long w;
        scanf("%d %d %lld", &u, &v, &w);
        if (w < d[u][v]) d[u][v] = d[v][u] = w;
    }
    for (int k = 1; k <= n; k++)
        for (int i = 1; i <= n; i++)
            for (int j = 1; j <= n; j++)
                if (d[i][k] + d[k][j] < d[i][j]) d[i][j] = d[i][k] + d[k][j];
    while (q--) {
        int s, t; scanf("%d %d", &s, &t);
        printf("%lld\n", d[s][t] >= INF ? -1LL : d[s][t]);
    }
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
#include <queue>
using namespace std;
/* 另一套：每次询问独立跑一遍堆优化 Dijkstra */
int main() {
    int n, m, q; cin >> n >> m >> q;
    const long long INF = (long long)1e15;
    vector<vector<pair<int, long long>>> adj(n + 1);
    while (m--) {
        int u, v; long long w; cin >> u >> v >> w;
        adj[u].push_back({v, w});
        adj[v].push_back({u, w});
    }
    while (q--) {
        int s, t; cin >> s >> t;
        vector<long long> dist(n + 1, INF);
        priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<pair<long long, int>>> pq;
        dist[s] = 0; pq.push({0, s});
        while (!pq.empty()) {
            auto [d, u] = pq.top(); pq.pop();
            if (d > dist[u]) continue;
            for (auto [v, w] : adj[u])
                if (dist[u] + w < dist[v]) { dist[v] = dist[u] + w; pq.push({dist[v], v}); }
        }
        cout << (dist[t] >= INF ? -1LL : dist[t]) << "\n";
    }
    return 0;
}
""",
)

def _oracle_96(text: str) -> str:
    d = text.split()
    n, m = int(d[0]), int(d[1])
    INF = 10**18
    dist = [[INF] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dist[i][i] = 0
    p = 2
    for _ in range(m):
        u, v, w = int(d[p]), int(d[p + 1]), int(d[p + 2]); p += 3
        if w < dist[u][v]:
            dist[u][v] = w
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if dist[i][k] < INF and dist[k][j] < INF and dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    lines = []
    for i in range(1, n + 1):
        lines.append(" ".join("INF" if dist[i][j] >= INF else str(dist[i][j])
                              for j in range(1, n + 1)))
    return "\n".join(lines) + "\n"

add(
    title="最短路径算法(Floyd-Warshall)",
    section="第 06 讲 · 图",
    difficulty=3, score=20, tags=["图", "Floyd-Warshall", "多源最短路", "动态规划"],
    statement_md=(
        "给定一个含 `n` 个顶点（编号 `1` ~ `n`）和 `m` 条有向边的有向带权图（允许含负权边，保证无负权回路），"
        "使用 **Floyd-Warshall 算法**求出所有顶点对 `(i, j)` 之间的最短路径长度，输出完整的 `n × n` 最短路矩阵。\n\n"
        "★ Floyd 三重循环里最致命的错误是**把 `k` 写在内层**：\n"
        "状态转移是「允许经过前 `k` 个顶点作为中间跳板」，所以**中转点 `k` 必须在最外层**（`k → i → j`）！"
    ),
    input_format="第一行两个整数 `n m`。\n\n随后 `m` 行，每行三个整数 `u v w` 表示有向边 `u → v` 的权值。",
    output_format="`n` 行，每行 `n` 个项（空格分隔）：若 `i` 可达 `j` 输出最短距离，否则输出 `INF`（对角线 `d[i][i] = 0`）。",
    constraints_md="- 1 ≤ n ≤ 60\n- 0 ≤ m ≤ 2000\n- -1000 ≤ w ≤ 1000（无负环）",
    inputs=[
        "4 8\n1 2 2\n1 3 6\n1 4 4\n2 3 3\n3 1 7\n3 4 1\n4 1 5\n4 3 12\n",
        "3 3\n1 2 4\n2 3 -2\n1 3 5\n",
        "3 1\n1 2 10\n",
    ],
    samples=2,
    oracle=_oracle_96,
    solution=r"""#include <stdio.h>
#define INF 1000000000000000LL
long long d[65][65];
int main(void) {
    int n, m;
    scanf("%d %d", &n, &m);
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++)
            d[i][j] = (i == j) ? 0 : INF;
    for (int k = 0; k < m; k++) {
        int u, v; long long w;
        scanf("%d %d %lld", &u, &v, &w);
        if (w < d[u][v]) d[u][v] = w;
    }
    for (int k = 1; k <= n; k++)
        for (int i = 1; i <= n; i++)
            for (int j = 1; j <= n; j++)
                if (d[i][k] < INF && d[k][j] < INF && d[i][k] + d[k][j] < d[i][j])
                    d[i][j] = d[i][k] + d[k][j];
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            if (j > 1) printf(" ");
            if (d[i][j] >= INF) printf("INF");
            else printf("%lld", d[i][j]);
        }
        printf("\n");
    }
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
using namespace std;
/* 另一套：从每个源点 i 分别跑一次 Bellman-Ford（支持负权边） */
struct E { int u, v; long long w; };
int main() {
    int n, m; cin >> n >> m;
    const long long INF = (long long)1e15;
    vector<E> edges(m);
    for (auto &e : edges) cin >> e.u >> e.v >> e.w;
    for (int s = 1; s <= n; s++) {
        vector<long long> dist(n + 1, INF);
        dist[s] = 0;
        for (int r = 1; r < n; r++)
            for (auto &e : edges)
                if (dist[e.u] < INF && dist[e.u] + e.w < dist[e.v])
                    dist[e.v] = dist[e.u] + e.w;
        for (int j = 1; j <= n; j++) {
            if (j > 1) cout << " ";
            if (dist[j] >= INF) cout << "INF";
            else cout << dist[j];
        }
        cout << "\n";
    }
    return 0;
}
""",
)

def _oracle_97(text: str) -> str:
    d = text.split()
    n, m = int(d[0]), int(d[1])
    INF = 10**18
    dist = [[INF] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dist[i][i] = 0
    p = 2
    for _ in range(m):
        u, v, w = int(d[p]), int(d[p + 1]), int(d[p + 2]); p += 3
        if w < dist[u][v]:
            dist[u][v] = dist[v][u] = w
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    best_id, best_max = 0, INF
    for i in range(1, n + 1):
        mx = max(dist[i][1:n + 1])
        if mx < best_max:
            best_max = mx
            best_id = i
    if best_id == 0:
        return "0\n"
    return "%d %d\n" % (best_id, best_max)

add(
    title="哈利·波特的考试",
    section="第 06 讲 · 图",
    difficulty=3, score=20, tags=["图", "Floyd", "图的中心点", "07-图4"],
    statement_md=(
        "PTA 经典题 `07-图4 哈利·波特的考试`：有 `N` 种动物（编号 `1` ~ `N`）和 `M` 条双向变形魔咒及各自的咒语长度。\n"
        "哈利想带**一只动物**去考场，使得把它变成**最难变的另一种动物**所需的总魔咒长度**最小**（即求图的中心点：`min_i max_j dist(i, j)`）。\n\n"
        "- 若有多只动物并列最优，输出**编号最小**的那只动物编号及其最大最短距离；\n"
        "- 若带哪只动物都无法变成所有其它动物（图不连通），输出 `0`。"
    ),
    input_format="第一行两个正整数 `N M`。\n\n随后 `M` 行，每行三个整数 `u v w` 表示动物 `u` 与 `v` 之间魔咒长度为 `w`。",
    output_format="一行，输出最优动物编号与对应的最大魔咒长度（空格分隔）；若图不连通输出 `0`。",
    constraints_md="- 1 ≤ N ≤ 100\n- 0 ≤ M ≤ 2000",
    inputs=[
        "6 11\n3 4 70\n1 2 1\n5 4 50\n2 6 50\n5 6 60\n1 3 70\n4 6 60\n3 6 80\n5 1 100\n2 4 60\n5 2 80\n",
        "4 2\n1 2 10\n3 4 20\n",
        "3 3\n1 2 5\n2 3 5\n1 3 5\n",
    ],
    samples=2,
    oracle=_oracle_97,
    solution=r"""#include <stdio.h>
#define INF 1000000000LL
long long d[105][105];
int main(void) {
    int n, m;
    scanf("%d %d", &n, &m);
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++)
            d[i][j] = (i == j) ? 0 : INF;
    for (int k = 0; k < m; k++) {
        int u, v; long long w;
        scanf("%d %d %lld", &u, &v, &w);
        if (w < d[u][v]) d[u][v] = d[v][u] = w;
    }
    for (int k = 1; k <= n; k++)
        for (int i = 1; i <= n; i++)
            for (int j = 1; j <= n; j++)
                if (d[i][k] + d[k][j] < d[i][j]) d[i][j] = d[i][k] + d[k][j];
    int best_i = 0;
    long long best_mx = INF;
    for (int i = 1; i <= n; i++) {
        long long mx = 0;
        for (int j = 1; j <= n; j++) if (d[i][j] > mx) mx = d[i][j];
        if (mx < best_mx) { best_mx = mx; best_i = i; }
    }
    if (best_i == 0) printf("0\n");
    else printf("%d %lld\n", best_i, best_mx);
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
using namespace std;
/* 另一套：对每个动物 i 跑一次 Dijkstra 求它的偏心率 */
int main() {
    int n, m; cin >> n >> m;
    const long long INF = (long long)1e15;
    vector<vector<pair<int, long long>>> adj(n + 1);
    while (m--) {
        int u, v; long long w; cin >> u >> v >> w;
        adj[u].push_back({v, w}); adj[v].push_back({u, w});
    }
    int best_i = 0;
    long long best_mx = INF;
    for (int s = 1; s <= n; s++) {
        vector<long long> dist(n + 1, INF);
        priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<pair<long long, int>>> pq;
        dist[s] = 0; pq.push({0, s});
        while (!pq.empty()) {
            auto [d, u] = pq.top(); pq.pop();
            if (d > dist[u]) continue;
            for (auto [v, w] : adj[u])
                if (dist[u] + w < dist[v]) { dist[v] = dist[u] + w; pq.push({dist[v], v}); }
        }
        long long mx = *max_element(dist.begin() + 1, dist.end());
        if (mx < best_mx) { best_mx = mx; best_i = s; }
    }
    if (best_i == 0) cout << 0 << "\n";
    else cout << best_i << " " << best_mx << "\n";
    return 0;
}
""",
)

def _oracle_98(text: str) -> str:
    d = text.split()
    n, m, s, dst = int(d[0]), int(d[1]), int(d[2]), int(d[3])
    INF = 10**18
    adj = [[] for _ in range(n)]
    p = 4
    for _ in range(m):
        u, v, L, C = int(d[p]), int(d[p + 1]), int(d[p + 2]), int(d[p + 3]); p += 4
        adj[u].append((v, L, C))
        adj[v].append((u, L, C))
    dist = [(INF, INF)] * n
    done = [False] * n
    dist[s] = (0, 0)
    for _ in range(n):
        u = -1
        for i in range(n):
            if not done[i] and dist[i] < (INF, INF) and (u < 0 or dist[i] < dist[u]):
                u = i
        if u < 0:
            break
        done[u] = True
        for v, L, C in adj[u]:
            cand = (dist[u][0] + L, dist[u][1] + C)
            if cand < dist[v]:
                dist[v] = cand
    return "%d %d\n" % (dist[dst][0], dist[dst][1])

add(
    title="旅游规划",
    section="第 06 讲 · 图",
    difficulty=3, score=20, tags=["图", "Dijkstra", "双权最短路", "07-图6"],
    statement_md=(
        "PTA 经典题 `07-图6 旅游规划`：城市编号 `0` ~ `N-1`，有 `M` 条双向高速公路，"
        "每条公路既给出了**长度 `len`**，又给出了**过路费 `cost`**。\n\n"
        "请找出从出发地 `S` 到目的地 `D` 的**最短路径**；若最短路径不唯一，"
        "则选择其中**过路费总和最便宜**的一条，输出 `最短距离 最少过路费`。\n\n"
        "★ 双权 Dijkstra 的松弛模板：\n"
        "- 当 `dist[u] + len < dist[v]` 时：距离和费用一起更新；\n"
        "- 当 `dist[u] + len == dist[v]` 且 `cost[u] + c < cost[v]` 时：只把费用更新得更便宜！"
    ),
    input_format=(
        "第一行四个整数 `N M S D`（城市数、公路数、起点、终点，城市编号 0 ~ N-1）。\n\n"
        "随后 `M` 行，每行四个整数 `u v len cost`。"
    ),
    output_format="一行两个整数，空格分隔：`最短距离 最少过路费`。",
    constraints_md="- 2 ≤ N ≤ 500\n- 1 ≤ M ≤ 5000\n- 保证 S 可达 D",
    inputs=[
        "4 5 0 3\n0 1 1 20\n1 3 2 30\n0 3 4 10\n0 2 2 20\n2 3 1 20\n",
        "3 3 0 2\n0 1 2 10\n1 2 2 10\n0 2 4 25\n",
        "4 4 0 3\n0 1 5 5\n1 3 5 10\n0 2 3 8\n2 3 7 4\n",
    ],
    samples=2,
    oracle=_oracle_98,
    solution=r"""#include <stdio.h>
#define INF 1000000000LL
long long g_len[505][505], g_cost[505][505], d_len[505], d_cost[505];
int done[505];
int main(void) {
    int n, m, s, dst;
    scanf("%d %d %d %d", &n, &m, &s, &dst);
    for (int i = 0; i < n; i++) {
        d_len[i] = d_cost[i] = INF;
        for (int j = 0; j < n; j++) g_len[i][j] = g_cost[i][j] = INF;
    }
    for (int k = 0; k < m; k++) {
        int u, v; long long L, C;
        scanf("%d %d %lld %lld", &u, &v, &L, &C);
        if (L < g_len[u][v] || (L == g_len[u][v] && C < g_cost[u][v])) {
            g_len[u][v] = g_len[v][u] = L;
            g_cost[u][v] = g_cost[v][u] = C;
        }
    }
    d_len[s] = 0; d_cost[s] = 0;
    for (int r = 0; r < n; r++) {
        int u = -1;
        for (int i = 0; i < n; i++)
            if (!done[i] && d_len[i] < INF && (u < 0 || d_len[i] < d_len[u])) u = i;
        if (u < 0) break;
        done[u] = 1;
        for (int v = 0; v < n; v++) {
            if (g_len[u][v] >= INF) continue;
            if (d_len[u] + g_len[u][v] < d_len[v]) {
                d_len[v] = d_len[u] + g_len[u][v];
                d_cost[v] = d_cost[u] + g_cost[u][v];
            } else if (d_len[u] + g_len[u][v] == d_len[v] && d_cost[u] + g_cost[u][v] < d_cost[v]) {
                d_cost[v] = d_cost[u] + g_cost[u][v];
            }
        }
    }
    printf("%lld %lld\n", d_len[dst], d_cost[dst]);
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
#include <queue>
#include <tuple>
using namespace std;
int main() {
    int n, m, s, dst; cin >> n >> m >> s >> dst;
    const long long INF = (long long)1e15;
    vector<vector<tuple<int, long long, long long>>> adj(n);
    while (m--) {
        int u, v; long long L, C; cin >> u >> v >> L >> C;
        adj[u].emplace_back(v, L, C);
        adj[v].emplace_back(u, L, C);
    }
    vector<pair<long long, long long>> dist(n, {INF, INF});
    using T = tuple<long long, long long, int>;
    priority_queue<T, vector<T>, greater<T>> pq;
    dist[s] = {0, 0}; pq.push({0, 0, s});
    while (!pq.empty()) {
        auto [L, C, u] = pq.top(); pq.pop();
        if (make_pair(L, C) > dist[u]) continue;
        for (auto [v, wL, wC] : adj[u]) {
            pair<long long, long long> cand = {L + wL, C + wC};
            if (cand < dist[v]) {
                dist[v] = cand;
                pq.push({cand.first, cand.second, v});
            }
        }
    }
    cout << dist[dst].first << " " << dist[dst].second << "\n";
    return 0;
}
""",
)

def _oracle_99(text: str) -> str:
    d = text.split()
    n = int(d[0])
    adj = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    p = 1
    for i in range(1, n + 1):
        k = int(d[p]); p += 1
        for _ in range(k):
            pre = int(d[p]); p += 1
            adj[pre].append(i)
            indeg[i] += 1
    q = [i for i in range(1, n + 1) if indeg[i] == 0]
    cnt = 0
    while q:
        u = q.pop(0)
        cnt += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return ("1\n" if cnt == n else "0\n")

add(
    title="任务调度的合理性",
    section="第 06 讲 · 图",
    difficulty=2, score=15, tags=["图", "拓扑排序", "AOV网", "判环"],
    statement_md=(
        "PTA 经典题 `08-图8 任务调度的合理性`：假定一个工程项目由一组子任务构成（编号 `1` ~ `N`），"
        "给出每个子任务必须先完成的直接前置子任务列表，判断整个任务调度方案是否合理（即**AOV 网中是否不存在有向环**）。\n\n"
        "★ 判环既可以用 **Kahn 入度拓扑排序**（看最终出队的顶点数是否等于 `N`），"
        "也可以用 **三色 DFS**（`0=未访问`、`1=当前递归栈中`、`2=已完成`，一旦摸到状态 `1` 的点即是有向环）！"
    ),
    input_format=(
        "第一行正整数 `N`（子任务数）。\n\n"
        "随后 `N` 行，第 `i` 行先给一个整数 `K`（前置任务数），随后跟 `K` 个前置任务编号。"
    ),
    output_format="一行，若调度方案合理（无环）输出 `1`，否则输出 `0`。",
    constraints_md="- 1 ≤ N ≤ 100",
    inputs=[
        "9\n0\n2 1 5\n1 1\n1 1\n2 3 4\n1 4\n2 2 5\n2 5 6\n2 7 8\n",
        "4\n1 2\n1 3\n1 1\n0\n",
        "3\n0\n1 1\n2 1 2\n",
        "2\n1 2\n1 1\n",
    ],
    samples=2,
    oracle=_oracle_99,
    solution=r"""#include <stdio.h>
int g[105][105], indeg[105], q[105];
int main(void) {
    int n;
    scanf("%d", &n);
    for (int i = 1; i <= n; i++) {
        int k; scanf("%d", &k);
        while (k--) {
            int pre; scanf("%d", &pre);
            if (!g[pre][i]) { g[pre][i] = 1; indeg[i]++; }
        }
    }
    int f = 0, r = 0;
    for (int i = 1; i <= n; i++) if (indeg[i] == 0) q[r++] = i;
    while (f < r) {
        int u = q[f++];
        for (int v = 1; v <= n; v++)
            if (g[u][v] && --indeg[v] == 0) q[r++] = v;
    }
    printf("%d\n", r == n ? 1 : 0);
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
#include <functional>
using namespace std;
/* 另一套：三色 DFS 判有向环 */
int main() {
    int n; cin >> n;
    vector<vector<int>> adj(n + 1);
    for (int i = 1; i <= n; i++) {
        int k; cin >> k;
        while (k--) { int p; cin >> p; adj[p].push_back(i); }
    }
    vector<int> col(n + 1, 0);
    bool cyc = false;
    function<void(int)> dfs = [&](int u) {
        col[u] = 1;
        for (int v : adj[u]) {
            if (col[v] == 1) cyc = true;
            else if (col[v] == 0) dfs(v);
        }
        col[u] = 2;
    };
    for (int i = 1; i <= n; i++) if (!col[i]) dfs(i);
    cout << (cyc ? 0 : 1) << "\n";
    return 0;
}
""",
)

def _oracle_100(text: str) -> str:
    d = text.split()
    n, m = int(d[0]), int(d[1])
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    p = 2
    for _ in range(m):
        u, v, w = int(d[p]), int(d[p + 1]), int(d[p + 2]); p += 3
        adj[u].append((v, w))
        indeg[v] += 1
    q = [i for i in range(n) if indeg[i] == 0]
    ve = [0] * n
    cnt = 0
    while q:
        u = q.pop(0)
        cnt += 1
        for v, w in adj[u]:
            if ve[u] + w > ve[v]:
                ve[v] = ve[u] + w
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    if cnt < n:
        return "Impossible\n"
    return "%d\n" % max(ve)

add(
    title="最短工期",
    section="第 06 讲 · 图",
    difficulty=3, score=20, tags=["图", "AOE网", "拓扑排序", "最早发生时间"],
    statement_md=(
        "PTA 经典题 `08-图8 最短工期（How Long Does It Take）`：一个项目有 `N` 个里程碑事件（编号 `0` ~ `N-1`）"
        "和 `M` 项有向活动 `(u, v, w)`，表示事件 `u` 达成后还需耗时 `w` 才能完成指向事件 `v` 的这项活动。\n\n"
        "请计算完成全部里程碑所需的**最短总工期**（即 `max(ve[0..N-1])`）；"
        "若计划中存在循环依赖（有向环），输出 `Impossible`。"
    ),
    input_format="第一行两个整数 `N M`。\n\n随后 `M` 行，每行三个非负整数 `u v w`。",
    output_format="一行，输出最短总工期；若有环则输出 `Impossible`。",
    constraints_md="- 1 ≤ N ≤ 100\n- 0 ≤ M ≤ 2000",
    inputs=[
        "9 12\n0 1 6\n0 2 4\n0 3 5\n1 4 1\n2 4 1\n3 5 2\n5 4 0\n4 6 9\n4 7 7\n5 7 4\n6 8 2\n7 8 4\n",
        "4 4\n0 1 1\n0 2 2\n2 1 3\n1 3 4\n",
        "3 3\n0 1 5\n1 2 5\n2 0 5\n",
    ],
    samples=2,
    oracle=_oracle_100,
    solution=r"""#include <stdio.h>
int head[105], nxt[2005], to[2005], wt[2005], ecnt = 0;
int indeg[105], q[105], ve[105];
int main(void) {
    int n, m;
    scanf("%d %d", &n, &m);
    for (int k = 0; k < m; k++) {
        int u, v, w; scanf("%d %d %d", &u, &v, &w);
        ++ecnt; to[ecnt] = v; wt[ecnt] = w; nxt[ecnt] = head[u]; head[u] = ecnt;
        indeg[v]++;
    }
    int f = 0, r = 0;
    for (int i = 0; i < n; i++) if (indeg[i] == 0) q[r++] = i;
    while (f < r) {
        int u = q[f++];
        for (int e = head[u]; e; e = nxt[e]) {
            int v = to[e], w = wt[e];
            if (ve[u] + w > ve[v]) ve[v] = ve[u] + w;
            if (--indeg[v] == 0) q[r++] = v;
        }
    }
    if (r < n) { printf("Impossible\n"); return 0; }
    int ans = 0;
    for (int i = 0; i < n; i++) if (ve[i] > ans) ans = ve[i];
    printf("%d\n", ans);
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
#include <algorithm>
#include <functional>
using namespace std;
int main() {
    int n, m; cin >> n >> m;
    vector<vector<pair<int, int>>> rev(n);
    while (m--) {
        int u, v, w; cin >> u >> v >> w;
        rev[v].push_back({u, w});
    }
    vector<int> state(n, 0), dp(n, 0);
    bool cyc = false;
    function<int(int)> solve = [&](int v) -> int {
        if (state[v] == 1) { cyc = true; return 0; }
        if (state[v] == 2) return dp[v];
        state[v] = 1;
        int best = 0;
        for (auto [u, w] : rev[v]) best = max(best, solve(u) + w);
        state[v] = 2;
        return dp[v] = best;
    };
    int ans = 0;
    for (int i = 0; i < n; i++) ans = max(ans, solve(i));
    if (cyc) cout << "Impossible\n";
    else cout << ans << "\n";
    return 0;
}
""",
)

def _oracle_101(text: str) -> str:
    d = text.split()
    n, m = int(d[0]), int(d[1])
    adj = [[] for _ in range(n + 1)]
    edges = []
    indeg = [0] * (n + 1)
    p = 2
    for idx in range(m):
        u, v, w = int(d[p]), int(d[p + 1]), int(d[p + 2]); p += 3
        adj[u].append((v, w, idx))
        edges.append((u, v, w, idx))
        indeg[v] += 1
    q = [i for i in range(1, n + 1) if indeg[i] == 0]
    topo = []
    ve = [0] * (n + 1)
    while q:
        u = q.pop(0)
        topo.append(u)
        for v, w, _ in adj[u]:
            if ve[u] + w > ve[v]:
                ve[v] = ve[u] + w
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    if len(topo) < n:
        return "0\n"
    total = max(ve[1:n + 1])
    vl = [total] * (n + 1)
    for u in reversed(topo):
        for v, w, _ in adj[u]:
            if vl[v] - w < vl[u]:
                vl[u] = vl[v] - w
    crit = [(u, -idx, v) for u, v, w, idx in edges if ve[u] + w == vl[v]]
    crit.sort()
    lines = [str(total)] + ["%d->%d" % (u, v) for u, _, v in crit]
    return "\n".join(lines) + "\n"

add(
    title="关键活动",
    section="第 06 讲 · 图",
    difficulty=4, score=25, tags=["图", "AOE网", "关键路径", "ve与vl", "08-图9"],
    statement_md=(
        "PTA 经典压轴题 `08-图9 关键活动`：给定 AOE 网的 `N` 个事件（编号 `1` ~ `N`）和 `M` 项有向活动 `(u, v, w)`：\n\n"
        "1. 若网络中有环（调度不可行），只输出一行 `0`；\n"
        "2. 若可行，第一行输出整个工程的**最短完成时间 `T = max(ve)`**，随后输出所有**关键活动**（满足 `ve[u] + w == vl[v]` 的活动 `u->v`）。\n\n"
        "★ 两个经典的 PTA 判分细节（踩过的人无数）：\n"
        "- 汇点可能不止一个，所以逆拓扑求最迟发生时间时，**全体 `vl[1..N]` 统一初始化为总工期 `T`**；\n"
        "- 输出顺序规定：按起点 `u` **从小到大**；起点相同时，按**输入时出现的先后顺序相反**（即邻接表**头插法**的自然遍历顺序）！"
    ),
    input_format="第一行两个正整数 `N M`。\n\n随后 `M` 行，每行三个正整数 `u v w`。",
    output_format="若不可行输出 `0`；否则第一行输出总工期，随后每行输出一条关键活动 `u->v`。",
    constraints_md="- 1 ≤ N ≤ 100\n- 1 ≤ M ≤ 1000",
    inputs=[
        "7 8\n1 2 4\n1 3 3\n2 4 5\n3 4 3\n4 5 1\n4 6 6\n5 7 5\n6 7 2\n",
        "4 4\n1 2 3\n1 3 3\n2 4 4\n3 4 4\n",
        "3 3\n1 2 2\n2 3 2\n3 1 2\n",
    ],
    samples=2,
    oracle=_oracle_101,
    solution=r"""#include <stdio.h>
int head[105], nxt[1005], to[1005], wt[1005], ecnt = 0;
int indeg[105], q[105], ve[105], vl[105];
/* 头插法建邻接表：同一个 u 的出边天然按输入逆序排列！ */
int main(void) {
    int n, m;
    scanf("%d %d", &n, &m);
    for (int k = 0; k < m; k++) {
        int u, v, w; scanf("%d %d %d", &u, &v, &w);
        ++ecnt; to[ecnt] = v; wt[ecnt] = w; nxt[ecnt] = head[u]; head[u] = ecnt;
        indeg[v]++;
    }
    int f = 0, r = 0;
    for (int i = 1; i <= n; i++) if (indeg[i] == 0) q[r++] = i;
    while (f < r) {
        int u = q[f++];
        for (int e = head[u]; e; e = nxt[e]) {
            int v = to[e], w = wt[e];
            if (ve[u] + w > ve[v]) ve[v] = ve[u] + w;
            if (--indeg[v] == 0) q[r++] = v;
        }
    }
    if (r < n) { printf("0\n"); return 0; }
    int tot = 0;
    for (int i = 1; i <= n; i++) if (ve[i] > tot) tot = ve[i];
    for (int i = 1; i <= n; i++) vl[i] = tot;
    for (int i = r - 1; i >= 0; i--) {
        int u = q[i];
        for (int e = head[u]; e; e = nxt[e]) {
            int v = to[e], w = wt[e];
            if (vl[v] - w < vl[u]) vl[u] = vl[v] - w;
        }
    }
    printf("%d\n", tot);
    for (int u = 1; u <= n; u++)
        for (int e = head[u]; e; e = nxt[e])
            if (ve[u] + wt[e] == vl[to[e]])
                printf("%d->%d\n", u, to[e]);
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
struct E { int u, v, w, idx; };
int main() {
    int n, m; cin >> n >> m;
    vector<E> edges(m);
    vector<vector<int>> adj(n + 1);
    vector<int> indeg(n + 1, 0);
    for (int i = 0; i < m; i++) {
        cin >> edges[i].u >> edges[i].v >> edges[i].w;
        edges[i].idx = i;
        adj[edges[i].u].push_back(i);
        indeg[edges[i].v]++;
    }
    vector<int> q;
    for (int i = 1; i <= n; i++) if (!indeg[i]) q.push_back(i);
    vector<int> ve(n + 1, 0);
    for (size_t f = 0; f < q.size(); f++) {
        int u = q[f];
        for (int id : adj[u]) {
            int v = edges[id].v, w = edges[id].w;
            ve[v] = max(ve[v], ve[u] + w);
            if (--indeg[v] == 0) q.push_back(v);
        }
    }
    if ((int)q.size() < n) { cout << 0 << "\n"; return 0; }
    int tot = *max_element(ve.begin() + 1, ve.end());
    vector<int> vl(n + 1, tot);
    for (int i = n - 1; i >= 0; i--) {
        int u = q[i];
        for (int id : adj[u]) {
            int v = edges[id].v, w = edges[id].w;
            vl[u] = min(vl[u], vl[v] - w);
        }
    }
    vector<E> crit;
    for (auto &e : edges) if (ve[e.u] + e.w == vl[e.v]) crit.push_back(e);
    sort(crit.begin(), crit.end(), [](const E &a, const E &b) {
        return a.u != b.u ? a.u < b.u : a.idx > b.idx;
    });
    cout << tot << "\n";
    for (auto &e : crit) cout << e.u << "->" << e.v << "\n";
    return 0;
}
""",
)

def _oracle_102(text: str) -> str:
    d = text.split()
    n = int(d[0])
    par = list(range(10000))
    seen = set()
    sets_mp = {}
    area_mp = {}

    def find(x: int) -> int:
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            if ra < rb:
                par[rb] = ra
            else:
                par[ra] = rb

    p = 1
    for _ in range(n):
        uid = int(d[p]); fa = int(d[p + 1]); mo = int(d[p + 2]); k = int(d[p + 3]); p += 4
        seen.add(uid)
        if fa != -1:
            seen.add(fa); union(uid, fa)
        if mo != -1:
            seen.add(mo); union(uid, mo)
        for _ in range(k):
            ch = int(d[p]); p += 1
            seen.add(ch); union(uid, ch)
        sets_mp[uid] = int(d[p]); area_mp[uid] = int(d[p + 1]); p += 2
    fams: dict[int, list[int]] = {}
    for u in seen:
        r = find(u)
        fams.setdefault(r, []).append(u)
    res = []
    for r, members in fams.items():
        cnt = len(members)
        ts = sum(sets_mp.get(u, 0) for u in members)
        ta = sum(area_mp.get(u, 0) for u in members)
        res.append((r, cnt, ts, ta))
    res.sort(key=lambda x: (-x[3] / x[1], x[0]))
    lines = [str(len(res))]
    for r, cnt, ts, ta in res:
        lines.append("%04d %d %.3f %.3f" % (r, cnt, ts / cnt, ta / cnt))
    return "\n".join(lines) + "\n"

add(
    title="家庭房产",
    section="第 06 讲 · 图",
    difficulty=4, score=25, tags=["并查集", "图连通块", "多关键字排序", "L2-007"],
    statement_md=(
        "PTA 天梯赛经典综合题 `L2-007 家庭房产`：给定每个人的家庭成员关系（父母、子女）以及各自名下的房产套数与总面积，"
        "凡有亲属关系的人都属于同一个**家庭**。\n\n"
        "请统计共有多少个家庭，并对每个家庭输出：\n"
        "`家庭最小编号（4位补零） 家庭人口数 人均房产套数 人均房产面积`（两位均值均保留 3 位小数）。\n"
        "按**人均面积降序**排列；若人均面积相同，则按**家庭最小编号升序**排列。\n\n"
        "★ 巧用并查集：合并两个集合时**永远让编号更小的当根**（`if (ra < rb) par[rb] = ra`），"
        "这样每个连通块的根天然就是该家庭的最小编号！"
    ),
    input_format=(
        "第一行正整数 `N`。\n\n"
        "随后 `N` 行，每行格式为：`编号 父 母 k 孩子1 ... 孩子k 房产套数 总面积`"
        "（编号为 0~9999 的整数，父母未知或去世填 `-1`）。"
    ),
    output_format=(
        "第一行输出家庭个数。\n\n"
        "随后每行输出一个家庭的信息：`%04d 人数 人均套数 人均面积`（保留 3 位小数）。"
    ),
    constraints_md="- 1 ≤ N ≤ 1000\n- 编号范围 0000 ~ 9999",
    inputs=[
        "4\n6666 5551 5552 1 7777 1 100\n1234 5678 9012 1 0002 2 300\n8888 -1 -1 0 1 1000\n2468 0001 0004 1 2222 1 500\n",
        "2\n0005 -1 -1 1 0002 3 150\n0008 -1 -1 0 2 100\n",
        "3\n0010 0020 -1 0 2 200\n0020 -1 -1 1 0030 2 200\n0030 -1 -1 0 0 0\n",
    ],
    samples=2,
    oracle=_oracle_102,
    solution=r"""#include <stdio.h>
#include <stdlib.h>
int par[10000], seen[10000], sets_v[10000], area_v[10000];
struct Fam { int id, cnt, ts, ta; } fams[10000];
int find(int x) {
    while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }
    return x;
}
void uni(int a, int b) {
    int ra = find(a), rb = find(b);
    if (ra == rb) return;
    if (ra < rb) par[rb] = ra;
    else par[ra] = rb;
}
int cmp(const void *a, const void *b) {
    const struct Fam *x = (const struct Fam *)a, *y = (const struct Fam *)b;
    long long lhs = (long long)x->ta * y->cnt, rhs = (long long)y->ta * x->cnt;
    if (lhs != rhs) return lhs > rhs ? -1 : 1;
    return x->id - y->id;
}
int main(void) {
    for (int i = 0; i < 10000; i++) par[i] = i;
    int n;
    scanf("%d", &n);
    while (n--) {
        int id, fa, mo, k;
        scanf("%d %d %d %d", &id, &fa, &mo, &k);
        seen[id] = 1;
        if (fa != -1) { seen[fa] = 1; uni(id, fa); }
        if (mo != -1) { seen[mo] = 1; uni(id, mo); }
        while (k--) { int ch; scanf("%d", &ch); seen[ch] = 1; uni(id, ch); }
        scanf("%d %d", &sets_v[id], &area_v[id]);
    }
    int fcnt = 0;
    for (int i = 0; i < 10000; i++) {
        if (seen[i] && find(i) == i) {
            fams[fcnt++] = (struct Fam){i, 0, 0, 0};
        }
    }
    for (int i = 0; i < 10000; i++) {
        if (!seen[i]) continue;
        int r = find(i);
        for (int j = 0; j < fcnt; j++) {
            if (fams[j].id == r) {
                fams[j].cnt++;
                fams[j].ts += sets_v[i];
                fams[j].ta += area_v[i];
                break;
            }
        }
    }
    qsort(fams, fcnt, sizeof(struct Fam), cmp);
    printf("%d\n", fcnt);
    for (int i = 0; i < fcnt; i++) {
        printf("%04d %d %.3f %.3f\n", fams[i].id, fams[i].cnt,
               (double)fams[i].ts / fams[i].cnt, (double)fams[i].ta / fams[i].cnt);
    }
    return 0;
}
""",
    alt=r"""#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <iomanip>
using namespace std;
struct Fam { int id, cnt, ts, ta; };
int main() {
    int n; cin >> n;
    vector<vector<int>> adj(10000);
    vector<char> seen(10000, 0);
    vector<int> sv(10000, 0), av(10000, 0);
    while (n--) {
        int id, fa, mo, k;
        cin >> id >> fa >> mo >> k;
        seen[id] = 1;
        if (fa != -1) { seen[fa] = 1; adj[id].push_back(fa); adj[fa].push_back(id); }
        if (mo != -1) { seen[mo] = 1; adj[id].push_back(mo); adj[mo].push_back(id); }
        while (k--) {
            int ch; cin >> ch;
            seen[ch] = 1; adj[id].push_back(ch); adj[ch].push_back(id);
        }
        cin >> sv[id] >> av[id];
    }
    vector<char> vis(10000, 0);
    vector<Fam> fams;
    for (int i = 0; i < 10000; i++) {
        if (!seen[i] || vis[i]) continue;
        queue<int> q; q.push(i); vis[i] = 1;
        Fam f{i, 0, 0, 0};
        while (!q.empty()) {
            int u = q.front(); q.pop();
            f.id = min(f.id, u);
            f.cnt++; f.ts += sv[u]; f.ta += av[u];
            for (int v : adj[u]) if (!vis[v]) { vis[v] = 1; q.push(v); }
        }
        fams.push_back(f);
    }
    sort(fams.begin(), fams.end(), [](const Fam &x, const Fam &y) {
        long long lhs = 1LL * x.ta * y.cnt, rhs = 1LL * y.ta * x.cnt;
        return lhs != rhs ? lhs > rhs : x.id < y.id;
    });
    cout << fams.size() << "\n" << fixed << setprecision(3);
    for (auto &f : fams)
        cout << setw(4) << setfill('0') << f.id << " " << f.cnt << " "
             << (double)f.ts / f.cnt << " " << (double)f.ta / f.cnt << "\n";
    return 0;
}
""",
)


# --------------------------------------------------------------------- #

def _sa(title: str, statement_md: str, answers: list[str], *, section: str,
        explanation: str, tags: list[str], difficulty: int = 2,
        total_score: int = 12, hint: str = "") -> dict:
    """简答题（本地实现，不动共享的 bank_kit）。

    用 bank_kit 的 oneof 口径判分：答案归一化后逐 token 比对，
    `answers` 列出全部可接受表述。归类 question_type = "short_answer"。
    """
    from app import bank_kit
    d = bank_kit._theory(
        title=title, subject="ds", section=section,
        statement_md=statement_md, answers=answers,
        explanation=explanation, tags=tags, difficulty=difficulty,
        total_score=total_score,
        output_format="一句话作答（不要写解释、不要抄题目）",
        tip=hint, question_type="short_answer")
    return d


def _theory_problems() -> list[dict]:
    p: list[dict] = []

    p.append(mc(
        "「逻辑结构」到底指什么",
        "数据结构里说的**逻辑结构**，指的是下面哪一个？",
        ["数据在计算机内存里的具体存放方式",
         "数据元素之间的逻辑关系，与怎么存储无关",
         "算法执行时间的度量方法",
         "数据的运算在机器上的实现"],
        "B",
        subject="ds", section="第 01 讲 · 绪论",
        explanation=(
            "**逻辑结构描述的是「元素之间什么关系」**——集合、线性、树、图四种，"
            "只跟数据本身有关。\n\n"
            "「放到内存里怎么放」是**存储结构**（顺序/链式/索引/散列）的事，"
            "同一张线性表既可以用数组存也可以用链表存，逻辑结构不变。"),
        tags=["逻辑结构", "基本概念"], difficulty=1,
    ))

    p.append(tf(
        "同一逻辑结构可以有多种存储结构",
        "同一种逻辑结构（比如线性表）可以采用多种不同的存储结构来实现——"
        "顺序存储、链式存储都行，两边互不影响逻辑结构本身。",
        True,
        subject="ds", section="第 01 讲 · 绪论",
        explanation=(
            "**对**。逻辑结构与存储结构是两个层面：线性表逻辑上就是"
            "「一对一」的关系，落地时用顺序表还是链表任选，各有优劣——"
            "教材后面「顺序表 vs 链表怎么选」整节都在讲这件事。"),
        tags=["逻辑结构", "存储结构"], difficulty=1,
    ))

    p.append(mc(
        "常数次内层循环的时间复杂度",
        "看这段代码：\n\n"
        "```c\nfor (int i = 1; i <= n; i++)\n    for (int j = 1; j <= 100; j++)\n"
        "        s++;\n```\n\n它的时间复杂度是？",
        ["O(1)", "O(log n)", "O(n)", "O(n²)"],
        "C",
        subject="ds", section="第 01 讲 · 绪论",
        explanation=(
            "内层循环**固定跑 100 次**，跟 n 无关——它是常数。"
            "总执行次数 ≈ 100n，大 O 记法丢掉常数因子，就是 **O(n)**。\n\n"
            "★ 常见错误是看到两层循环就条件反射选 O(n²)。"
            "判 O(n²) 的标准是**内层次数也随 n 增长**（比如 `j <= i`）。"),
        tags=["时间复杂度", "大 O 记法"], difficulty=2,
    ))

    p.append(mc(
        "无向完全图的边数",
        "`n` 个顶点的**无向完全图**有多少条边？",
        ["n(n-1)/2", "n(n-1)", "n²", "n-1"],
        "A",
        subject="ds", section="第 06 讲 · 图",
        explanation=(
            "每个顶点都和其余 `n-1` 个顶点相连，共 `n(n-1)` 个「端点计数」，"
            "但每条边被数了两次（无向边两端各记一次）→ **n(n-1)/2**。\n\n"
            "有向完全图才是 `n(n-1)`——弧有方向，`<u,v>` 和 `<v,u>` 是两条。"),
        tags=["基本术语", "完全图"], difficulty=1,
    ))

    p.append(tf(
        "邻接矩阵第 i 行的非零元个数 = 顶点 i 的出度",
        "对**有向图**，邻接矩阵 `A[i][j] = 1` 表示弧 `<vi, vj>` 存在，"
        "所以第 `i` 行的非零元素个数就是顶点 `vi` 的出度，"
        "第 `i` 列的非零元素个数是入度。",
        True,
        subject="ds", section="第 06 讲 · 图",
        explanation=(
            "**对**。行是「我指向谁」（出度），列是「谁指向我」（入度）。"
            "这就是讲义 demo 里「行和出度、列和入度」那句实测结论——"
            "求度数连邻接表都不用建。"),
        tags=["邻接矩阵", "出度入度"], difficulty=1,
    ))

    p.append(mc(
        "单源最短路径该用哪个算法",
        "求**边权非负**的带权图上，从一个源点到其余各顶点的最短路径，"
        "经典教材算法是？",
        ["Prim", "Kruskal", "Floyd", "Dijkstra"],
        "D",
        subject="ds", section="第 06 讲 · 图",
        explanation=(
            "**Dijkstra**：贪心地一轮一轮把「离源点最近的未定顶点」定下来。"
            "Prim/Kruskal 是**最小生成树**的算法（树，不是路径）；"
            "Floyd 求**全源**最短路，用它求单源是杀鸡用牛刀，而且它靠"
            "三重循环动态规划、复杂度 O(n³)。\n\n"
            "★ Dijkstra 的命门：**不能有负权边**——讲义给过实测反例。"),
        tags=["Dijkstra", "最短路径"], difficulty=1,
    ))

    p.append(mc(
        "折半查找的适用前提",
        "折半查找（二分查找）要求线性表满足什么条件？",
        ["链式存储即可，元素有无序都行",
         "顺序存储，且元素按关键字有序",
         "任意存储，只要元素互不相同",
         "必须是用散列函数组织好的表"],
        "B",
        subject="ds", section="第 07 讲 · 查找",
        explanation=(
            "两个条件**缺一不可**：**有序**（才能判断去左半还是右半）＋"
            "**顺序存储**（才能 O(1) 跳到 mid）。\n\n"
            "链表虽然也可以有序，但找 mid 只能顺着链走 O(n)，折半的效率优势"
            "整个消失——所以教材口径是「顺序存储的有序表」。"),
        tags=["折半查找", "有序表"], difficulty=1,
    ))

    p.append(mc(
        "11 个元素折半查找的平均查找长度",
        "对含 `n = 11` 个元素的有序表做折半查找，**成功查找**的平均查找长度 "
        "ASL 是多少？\n\n（提示：比较次数分布为 1 次 ×1、2 次 ×2、3 次 ×4、4 次 ×4）",
        ["3.0", "4.0", "11/4 ≈ 2.75", "log₂11 ≈ 3.46"],
        "A",
        subject="ds", section="第 07 讲 · 查找",
        explanation=(
            "ASL = (1×1 + 2×2 + 3×4 + 4×4) / 11 = 33/11 = **3.0**。\n\n"
            "这是讲义 demo 的实测值：判定树逐层数结点，最多比较层数是"
            " `⌊log₂11⌋ + 1 = 4`，失败查找同样 4 次。选 D 的人是把"
            "「层数公式」当成了平均长度。"),
        tags=["折半查找", "ASL", "判定树"], difficulty=2,
    ))

    p.append(tf(
        "散列冲突可以完全避免",
        "只要散列函数设计得足够好，散列表的冲突就可以完全避免。",
        False,
        subject="ds", section="第 07 讲 · 查找",
        explanation=(
            "**错**。散列是「任意键 → 有限槽位」的映射，键的取值空间通常远大于"
            "槽位数，冲突在数学上**不可避免**（鸽笼原理）。\n\n"
            "好的散列函数只能**减少**冲突，真正的功夫在**怎么处理冲突**："
            "线性探测、链地址法……这正是 7.4 节半章篇幅的内容。"),
        tags=["散列表", "冲突"], difficulty=1,
    ))

    p.append(mc(
        "下列排序算法中稳定的是",
        "下面几种内部排序中，**稳定**的是？",
        ["直接插入排序", "简单选择排序", "快速排序", "堆排序"],
        "A",
        subject="ds", section="第 08 讲 · 排序",
        explanation=(
            "**直接插入稳定**：相等元素只从后往前找插入点、遇到相等就停，"
            "不会越过同类。\n\n"
            "另外三个都不稳定（讲义 demo 用 {3a, 3h, 1} 最小反例实测现形）：\n"
            "- **简单选择**：first-min 远距离交换会跨越等值元素；\n"
            "- **快排**：双向扫描会把等值元素甩到枢轴另一侧；\n"
            "- **堆排**：堆顶换末尾的远距离交换同理。\n\n"
            "★ 稳定的还有：冒泡、归并、基数——口诀「插冒归基稳」。"),
        tags=["稳定性", "内部排序"], difficulty=2,
    ))

    p.append(mc(
        "快速排序最坏情况的时间复杂度",
        "快速排序在**最坏情况**（比如每次枢轴都选到最值、序列已经有序）下，"
        "时间复杂度是？",
        ["O(n)", "O(n log n)", "O(n²)", "O(log n)"],
        "C",
        subject="ds", section="第 08 讲 · 排序",
        explanation=(
            "最坏时每趟划分只分出「1 个 vs n-1 个」，递归深度退到 n 层，"
            "总比较次数是等差数列之和 → **O(n²)**。\n\n"
            "平均才是 O(n log n)。这就是「快排怕有序」——讲义实测 "
            "1..15 顺序插入再快排，划分退化得一模一样。"
            "工程上用三者取中/随机枢轴来躲开这个坑。"),
        tags=["快速排序", "时间复杂度"], difficulty=2,
    ))

    p.append(tf(
        "基本有序时直接插入排序接近 O(n)",
        "如果初始序列**基本有序**，直接插入排序的比较和移动次数都会很少，"
        "整体时间接近 O(n)。",
        True,
        subject="ds", section="第 08 讲 · 排序",
        explanation=(
            "**对**。每个元素的插入点都几乎在原地，内层 while 基本一两次就停。"
            "极端情况：完全有序时每趟只比较 1 次，共 n-1 次——O(n)。\n\n"
            "这正是**希尔排序**存在的理由：先用大步长把序列「拍得基本有序」，"
            "最后一趟直接插入收尾时就是 O(n) 的舒适区。"),
        tags=["直接插入", "希尔排序", "时间复杂度"], difficulty=1,
    ))

    # ---- 多选题 ----
    p.append(multi(
        "稳定的排序算法有哪些",
        "下列内部排序算法中，**稳定**的有哪些？\n\n"
        "（提醒：稳定性 = 相等元素排序后相对次序不变）",
        ["直接插入排序", "冒泡排序", "堆排序", "归并排序"],
        ["A", "B", "D"],
        subject="ds", section="第 08 讲 · 排序",
        explanation=(
            "稳定的三个：**直接插入**（相等就停，不越过同类）、**冒泡**"
            "（严格大于才交换）、**归并**（两边相等取左段）。\n\n"
            "**堆排序不稳定**：堆顶与末尾的远距离交换会把等值元素甩开——"
            "讲义 demo 用 {3a, 3h, 1} 实测现形。\n\n"
            "口诀：**插冒归基稳，选择快希堆不稳**。"),
        tags=["稳定性", "内部排序", "多选"], difficulty=3,
    ))

    p.append(multi(
        "邻接矩阵与邻接表的说法辨析",
        "关于图的两种存储结构，下列说法**正确**的有哪些？",
        ["无向图的邻接矩阵一定是对称矩阵",
         "邻接表更适合存稀疏图",
         "邻接矩阵更适合存稀疏图",
         "邻接矩阵判断两个顶点是否邻接是 O(1)"],
        ["A", "B", "D"],
        subject="ds", section="第 06 讲 · 图",
        explanation=(
            "A 对：无向边 (u,v) 在矩阵里两个方向都置 1，必然对称。\n\n"
            "B 对、**C 错**：邻接表空间 O(n+e)，稀疏图省得厉害；"
            "邻接矩阵固定 O(n²)——边少时全是浪费，它适合**稠密图**。\n\n"
            "D 对：矩阵下标直接查 `A[u][v]`，一步到位；邻接表反而要扫链 O(deg)。"),
        tags=["邻接矩阵", "邻接表", "存储结构", "多选"], difficulty=3,
    ))

    # ---- 简答题 ----
    p.append(_sa(
        "一句话说明什么是稳定排序",
        "**简答题**：用一句话说明「稳定排序」的含义。\n\n"
        "按下面的句式作答：`相等元素……相对次序……`",
        ["相等元素排序后相对次序保持不变",
         "相等元素排序后相对次序不变",
         "相等的元素排序后相对次序保持不变",
         "值相同的元素排序后相对次序不变"],
        section="第 08 讲 · 排序",
        explanation=(
            "参考答案：**相等元素排序后相对次序保持不变**。\n\n"
            "展开说：序列里若有多个关键字相同的记录，稳定排序保证排完序后"
            "它们的先后顺序与排序前一致（如 49a 一直在 49h 前面）；"
            "不稳定排序则可能交换它们的相对位置。\n\n"
            "稳定性有什么用？对**多关键字排序**是刚需：先按次要关键字排好，"
            "再用稳定的主关键字排序，次要关键字的次序得以保留——基数排序"
            "就是靠「每趟都用稳定排序」立住的。"),
        tags=["稳定性", "简答"], difficulty=2,
    ))

    p.append(_sa(
        "写出数据结构的三要素",
        "**简答题**：写出**数据结构的三要素**，用顿号或空格分隔"
        "（按讲义顺序：两个「结构」在前，运算在后）。",
        ["逻辑结构、存储结构、运算",
         "逻辑结构 存储结构 运算",
         "数据的逻辑结构、数据的存储结构、数据的运算",
         "逻辑结构、存储结构、数据的运算"],
        section="第 01 讲 · 绪论",
        explanation=(
            "参考答案：**逻辑结构、存储结构、运算**。\n\n"
            "- **逻辑结构**：元素之间「什么关系」（集合/线性/树/图）；\n"
            "- **存储结构**：关系「怎么落进内存」（顺序/链式/索引/散列）；\n"
            "- **运算**：在这种结构上「能干什么」（定义在逻辑结构上、"
            "实现在存储结构上）。\n\n"
            "三者缺一不可：只讲关系不讲落地是数学，只讲落地不讲关系是纯编程。"),
        tags=["三要素", "基本概念", "简答"], difficulty=1,
    ))

    # ---- 02~05 讲理论题（此前这几讲只有编程题，理论空缺）----
    p.append(mc(
        "顺序表插入的平均移动次数",
        "长度为 `n` 的顺序表，在**等概率**下按位序插入一个元素，平均要移动"
        "多少个元素？",
        ["n/2", "n", "(n-1)/2", "n-1"],
        "A",
        subject="ds", section="第 02 讲 · 线性表",
        explanation=(
            "插到第 `i` 位要移动 `n-i+1` 个，i 取 1..n+1 等概率平均："
            "Σ(n-i+1)/(n+1) = **n/2**。\n\n"
            "对照记忆：删除的平均移动是 **(n-1)/2** —— 插删这两个公式"
            "考试最爱配对出现，别背混。"),
        tags=["顺序表", "平均移动次数"], difficulty=2,
    ))

    p.append(mc(
        "头插法建单链表的结点次序",
        "用**头插法**把 `a1, a2, a3` 依次插入空单链表，建好后的结点次序是？",
        ["a1 a2 a3", "a3 a2 a1", "a2 a1 a3", "a1 a3 a2"],
        "B",
        subject="ds", section="第 02 讲 · 线性表",
        explanation=(
            "头插法 = 新结点总插在**表头**。a1 先进，a2 插到它前面，"
            "a3 再插到最前面 → **a3 a2 a1**，与输入顺序**正好相反**。\n\n"
            "图、散列桶的邻接链用的也是这个插法（教材惯例）——"
            "PTA 里那道「无向图的邻接表（头插法）」考的就是这条。"
            "想保持原序就得用**尾插法**。"),
        tags=["单链表", "头插法"], difficulty=1,
    ))

    p.append(tf(
        "循环单链表尾结点的 next 指向头结点",
        "在**带头结点**的循环单链表里，尾结点的 `next` 域指向**头结点**。",
        True,
        subject="ds", section="第 02 讲 · 线性表",
        explanation=(
            "**对**。这正是「循环」的含义：`尾.next == 头`，整条链成环。\n\n"
            "实战价值：判空是 `head->next == head`（而不是普通单链表的 "
            "`head->next == NULL`）；从任一结点出发都能扫全表——"
            "所以「只设尾指针 R」的循环链表能做到两头 O(1) 操作。"),
        tags=["循环链表", "单链表"], difficulty=1,
    ))

    p.append(mc(
        "哪个出栈序列是不可能的",
        "三个元素按 `1, 2, 3` 的顺序依次进栈（进出可以交错），"
        "**不可能**得到的出栈序列是？",
        ["1 2 3", "3 2 1", "2 1 3", "3 1 2"],
        "D",
        subject="ds", section="第 03 讲 · 栈和队列",
        explanation=(
            "**3 1 2 不可能**：想先弹出 3，必须 1、2、3 都已进栈；"
            "3 出来后栈顶是 2，第二个只能弹 2，弹不出 1。\n\n"
            "判定法（讲义里的「逐个模拟」）：把出栈序列当目标，元素按 1..n 进栈，"
            "栈顶一等于目标就弹——弹不动还不齐，就是假序列。\n\n"
            "★ n 个元素合法出栈序列数 = 卡特兰数 C(2n,n)/(n+1)，n=3 时 5 种"
            "（总共 6 种排列，恰好只有 `3 1 2` 这一种不合法）。"),
        tags=["栈", "出栈序列", "卡特兰数"], difficulty=2,
    ))

    p.append(tf(
        "循环队列牺牲一格的队满条件",
        "循环队列用「牺牲一个存储单元」区分队空与队满时，队满条件是"
        "`(rear + 1) % m == front`（m 为队列容量）。",
        True,
        subject="ds", section="第 03 讲 · 栈和队列",
        explanation=(
            "**对**。不牺牲一格的话，队空（`front == rear`）和队满（也 "
            "`front == rear`）没法区分——这就是讲义里「假溢出」之后必须做的取舍。\n\n"
            "代价：实际最多存 `m-1` 个元素。另两种方案：设 size 计数器、"
            "设 tag 标记上一次是入队还是出队。"),
        tags=["循环队列", "队满条件", "假溢出"], difficulty=2,
    ))

    p.append(mc(
        "递归调用背后是什么结构",
        "函数递归调用（比如阶乘、汉诺塔）的「保存现场、返回时恢复」，"
        "系统背后用的是哪种数据结构？",
        ["队列", "栈", "线性表（顺序）", "树"],
        "B",
        subject="ds", section="第 03 讲 · 栈和队列",
        explanation=(
            "**栈**——递归工作栈。每次调用压一帧（参数+局部变量+返回地址），"
            "返回时弹一帧。后进先出正好匹配「最后调用的最先返回」。\n\n"
            "所以任何递归都能**用显式栈改成非递归**（3.4.4 的方法）；"
            "递归太深爆的「栈溢出」就是这栈满了。"),
        tags=["栈", "递归", "递归工作栈"], difficulty=1,
    ))

    p.append(mc(
        "教材口径的 next[1] 等于几",
        "KMP 算法里，模式串位序**从 1 开始**（教材口径），`next[1]` 的值是？",
        ["-1", "0", "1", "不存在"],
        "B",
        subject="ds", section="第 04 讲 · 串、数组和广义表",
        explanation=(
            "教材（位序从 1 起）规定 **next[1] = 0**——它是个「哨兵」："
            "表示「主串指针 i 前移一位、模式串回到开头重比」。\n\n"
            "★ 下标从 1 起是全书的隐形坑：网上不少资料位序从 0 起、next[0] = -1，"
            "那套值和教材的整套差一位，抄之前先看清自己的下标口径。"),
        tags=["KMP", "next 数组", "下标口径"], difficulty=2,
    ))

    p.append(mc(
        "对称矩阵下三角压缩的下标公式",
        "`n` 阶对称矩阵按**下三角**（含对角线）行优先压缩进一维数组 `sa`，"
        "且 `sa` 的**位序也从 1 起**。元素 `a[i][j]`（`i ≥ j`）存在 `sa[k]`，"
        "则 `k` = ？",
        ["i(i-1)/2 + j", "i(i-1)/2 + j - 1", "j(j-1)/2 + i", "i(i+1)/2 + j"],
        "A",
        subject="ds", section="第 04 讲 · 串、数组和广义表",
        explanation=(
            "第 `i` 行之前有 1..i-1 行，共 `1+2+…+(i-1) = i(i-1)/2` 个元素；"
            "行内 `a[i][j]` 前面还有 `j-1` 个 → k = i(i-1)/2 + (j-1) + 1 = "
            "**i(i-1)/2 + j**。\n\n"
            "验算两头：`a[1][1]` → k=1（sa 第一个），`a[2][1]` → k=2，"
            "`a[2][2]` → k=3 —— 全对得上。\n\n"
            "★ 本讲最大的坑就是**下标口径**：教材位序从 1 起，网上不少资料从 "
            "0 起（那种口径才是 `i(i-1)/2 + j - 1`，即 B 项）。"
            "套公式前先核对题面的「从几起」，B/C/D 都是一个符号位错出来的干扰项。"),
        tags=["特殊矩阵", "压缩存储", "下标口径"], difficulty=3,
        answer_note="提示：题面已钉死「sa 位序从 1 起」，套公式前先验算 a[1][1]",
    ))

    p.append(tf(
        "快速转置需要预先算 num 和 cpot",
        "稀疏矩阵的**快速转置**之所以快，是因为它先用一遍扫描统计每列非零元"
        "个数 `num[]`，再推出每列第一个非零元在目标三元组表中的位置 `cpot[]`，"
        "然后一遍放好——不需要按列反复扫描整个表。",
        True,
        subject="ds", section="第 04 讲 · 串、数组和广义表",
        explanation=(
            "**对**。普通转置 O(nu × tu)（对每一列扫全表），快速转置"
            "O(nu + tu)（两个线性趟）。\n\n"
            "★ 讲义实测大坑：`cpot[col+1] = cpot[col] + num[col]` 这步的"
            "累加基准要是写漏，数据会整段错位——demo 里「漏 cpot++ 丢数据」"
            "那条陷阱说的就是它。"),
        tags=["稀疏矩阵", "快速转置", "三元组"], difficulty=2,
    ))

    p.append(mc(
        "二叉树叶子数与度 2 结点数的关系",
        "任意一棵二叉树，叶子结点数 `n0` 与度数为 2 的结点数 `n2` 满足？",
        ["n0 = n2", "n0 = n2 + 1", "n2 = n0 + 1", "n0 = 2·n2"],
        "B",
        subject="ds", section="第 05 讲 · 树和二叉树",
        explanation=(
            "**n0 = n2 + 1**。从边的条数推：n 个结点 n-1 条边，"
            "每条边出自一个非叶结点，即 n-1 = n1 + 2·n2；又 n = n0+n1+n2，"
            "两式一消就得到 n0 = n2+1。\n\n"
            "它跟「度数」无关地恒成立——考题常给几个 n1/n2 让你算叶子数，"
            "直接套这个式子比画树快。"),
        tags=["二叉树性质", "叶子结点"], difficulty=1,
    ))

    p.append(mc(
        "哪种遍历组合能唯一确定一棵二叉树",
        "已知两种遍历序列，**能唯一确定**一棵二叉树的组合是？",
        ["先序 + 后序", "先序 + 中序", "只有先序", "层次 + 后序"],
        "B",
        subject="ds", section="第 05 讲 · 树和二叉树",
        explanation=(
            "**先序 + 中序**（以及中序 + 后序、中序 + 层次）可以；"
            "**先序 + 后序不行**——两个都缺「左右子树的分界」信息，"
            "只有一个结点的子树时分不清它在左还是右（反例：任何一条链都有"
            "多棵树对应）。\n\n"
            "原理：先序首个是根 → 在中序里切出左右子树 → 递归。"
            "教材 5.5.1「由遍历序列确定二叉树」的高频大题就考这个。"),
        tags=["遍历", "唯一确定", "先序中序"], difficulty=2,
    ))

    p.append(tf(
        "哈夫曼树没有度为 1 的结点",
        "哈夫曼树（最优二叉树）中不存在度数为 1 的结点。",
        True,
        subject="ds", section="第 05 讲 · 树和二叉树",
        explanation=(
            "**对**。哈夫曼树每次合并**两个**最小权结点成一个新的度 2 结点，"
            "从不产生独苗——所以结点只有叶（n0）和度 2（n2），且 n0 = n2+1，"
            "总结点数 = 2·n0 − 1（奇数）。\n\n"
            "推论也是考点：n 个权值建哈夫曼树，一共要合并 n−1 次。"
            "「WPL = Σ 权值 × 路长」另有一条捷径：WPL 也等于**所有非叶结点"
            "权值之和**——讲义 demo 双路复算对过。"),
        tags=["哈夫曼树", "二叉树性质", "WPL"], difficulty=2,
    ))

    return p


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

覆盖范围：数据结构第 01 ~ 08 讲（绪论理论题 / 线性表 / 栈与队列 / 串数组广义表 /
树与二叉树 / 图 / 查找 / 排序）。编程题集中在 02~08 讲；01 讲纯理论（考概念）。
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
    out.extend(_theory_problems())       # 理论题（line=text）排在编程题后面
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
        if p.get("line") == "text":
            # 理论题：没有 alt_solution / 用例输入，字段要求不同
            for k in ("statement_md", "reference_solution", "source_section"):
                if not str(p.get(k) or "").strip():
                    problems.append("[%d] %s 缺字段 %s" % (i, t, k))
            if not p["cases"]:
                problems.append("[%d] %s 没有测试用例" % (i, t))
            continue
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

    # 每个 oracle 都必须产出非空输出 —— 空输出几乎一定是 oracle 写错了。
    # 例外：恰好 "\n"（空一行）是合法的边界输出（如「整行无单词→空行」「两表全空→空行」）
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
