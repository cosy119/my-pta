# -*- coding: utf-8 -*-
"""C/C++ 编程精练题库生成器 —— 「编程精练 · C/C++」分节。

与「技巧特训 · C/C++」的分工：
  - 技巧特训 = STL 套路与竞赛技巧（stable_sort / bitset / 树状数组 / next_permutation）
  - 编程精练 = **把讲义里的数据结构真正手写出来**（顺序表、静态链表、循环队列、
               调度场、二叉树重建、哈夫曼、图遍历、拓扑排序、快排划分、BST）

每道题：
  title / section / difficulty / score / tags
  statement_md / input_format / output_format / constraints_md
  inputs   ← 测试点输入（手写 + 固定种子生成，可复现）
  samples  ← 前几个当样例
  oracle   ← **独立 Python 实现**，算期望输出（尽量用"笨办法"，与 C++ 参考解不同路）
  solution / alt ← 两套 C++ 实现（verify_bank 双撞，必须逐字节同输出）

章节结构（difficulty 2 → 4 递进）：
  线性表    2 题（顺序表去重 / 静态链表就地逆置）
  栈与队列  2 题（循环队列操作序列 / 中缀转后缀并求值）
  树        3 题（先序中序建树 / 哈夫曼 WPL / 二叉排序树）
  图        2 题（BFS-DFS 遍历 / 拓扑排序最小字典序）
  排序      1 题（快排一趟划分）

★ 全库标题必须唯一（seed.ensure 按 title 判重，撞名会被静默跳过）。
★ C++ 输出用 '\n'；判题端会归一化 CRLF，但两套实现必须同一种行尾风格。
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "app" / "problems_bank_ds_prog.py"

SECTION = "编程精练 · C/C++"

PROBLEMS: list[dict] = []


def add(**kw) -> None:
    PROBLEMS.append(kw)


# --------------------------------------------------------------------- #
#  线性表（difficulty 2）
# --------------------------------------------------------------------- #

def _oracle_01(text: str) -> str:
    """顺序表去重：逐项与「已保留的最后一个」比较（笨办法，靠已有序）。"""
    d = text.split()
    n = int(d[0])
    a = [int(v) for v in d[1:1 + n]]
    keep: list[int] = []
    for x in a:
        if not keep or keep[-1] != x:
            keep.append(x)
    return "%d\n%s\n" % (len(keep), " ".join(map(str, keep)))


add(
    title="顺序表删除重复元素",
    section=SECTION,
    difficulty=2, score=10, tags=["编程精练", "顺序表", "双指针"],
    statement_md=(
        "给定一个**非降序**的顺序表，**就地**删除所有重复元素（每个值只保留一个），"
        "输出删除后的长度和序列。\n\n"
        "要求空间复杂度 `O(1)`——不许开新数组。\n\n"
        "★ 这题的钥匙是「有序」两个字：重复元素一定**挨在一起**。"
        "于是维护一个慢指针 `i` 指向「已保留部分的末尾」，快指针 `j` 一路向前扫；"
        "只要 `a[j] != a[i]`，就把 `a[j]` 挪到 `i+1` 去。\n\n"
        "⚠️ 如果表无序，这个双指针法就**不成立**了，只能 `O(n²)` 对每个元素往回扫，"
        "或者开哈希表——那就不是 `O(1)` 空间了。题目条件不是摆设。"
    ),
    input_format="第一行 `n`；第二行 `n` 个整数（**非降序**）。",
    output_format="两行：去重后的长度；去重后的序列（空格分隔）。",
    constraints_md="- 1 ≤ n ≤ 10⁵\n- 序列非降序\n- 要求 O(1) 额外空间",
    inputs=[
        "6\n1 1 2 2 3 3\n",
        "1\n7\n",
        "5\n1 2 3 4 5\n",
        "8\n-3 -3 -3 0 0 5 5 5\n",
        "4\n2 2 2 2\n",
    ],
    samples=3,
    oracle=_oracle_01,
    solution=r'''#include <cstdio>
#include <vector>
using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<int> a(n);
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);

    int i = 0;                        // 慢指针：已保留部分的末尾
    for (int j = 1; j < n; j++) {
        if (a[j] != a[i]) {
            i++;
            a[i] = a[j];
        }
    }
    int len = i + 1;

    printf("%d\n", len);
    for (int k = 0; k < len; k++) {
        printf("%d", a[k]);
        putchar(k + 1 == len ? '\n' : ' ');
    }
    return 0;
}
''',
    alt=r'''#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    // 另一条路：std::unique（它做的就是「相邻去重 + 返回新末尾」，
    // 正好是本题双指针的库版本），配上 distance 求长度。
    auto tail = unique(a.begin(), a.end());
    int len = (int)distance(a.begin(), tail);

    cout << len << '\n';
    for (int k = 0; k < len; k++) {
        if (k) cout << ' ';
        cout << a[k];
    }
    cout << '\n';
    return 0;
}
''',
)


def _oracle_02(text: str) -> str:
    """静态链表就地逆置：用两个数组模拟 next 指针，真的去改指针。"""
    d = text.split()
    n = int(d[0])
    a = [int(v) for v in d[1:1 + n]]
    data = [0] * (n + 1)
    nxt = [0] * (n + 1)
    for i in range(1, n + 1):
        data[i] = a[i - 1]
        nxt[i] = i + 1 if i < n else 0
    head = 1
    # 就地逆置：不新开节点，只改 next
    prev = 0
    cur = head
    rewrites = 0
    while cur:
        follow = nxt[cur]
        nxt[cur] = prev
        prev = cur
        cur = follow
        rewrites += 1
    head = prev
    seq = []
    p = head
    while p:
        seq.append(data[p])
        p = nxt[p]
    return "%s\n%d\n%d\n" % (" ".join(map(str, seq)), head, rewrites)


add(
    title="用数组模拟链表就地逆置",
    section=SECTION,
    difficulty=2, score=10, tags=["编程精练", "链表", "指针", "静态链表"],
    statement_md=(
        "用**静态链表**存 `n` 个整数：`data[i]` 放值，`next[i]` 放下一个节点的下标"
        "（下标从 1 起，`0` 表示空）。初始 `head = 1`，节点依次串联。\n\n"
        "把这个链表**就地**逆置（不许新建节点、不许开新数组存值，只能改 `next`），输出三行：\n"
        "1. 逆置后从头遍历得到的序列\n"
        "2. 新的 `head`\n"
        "3. 逆置过程中 **`next` 被改写的次数**\n\n"
        "★ 逆置三件套：`follow = next[cur]` 先记住后路，`next[cur] = prev` 掉头，"
        "`prev = cur; cur = follow` 一起前进。\n\n"
        "⚠️ 顺序千万不能乱：**先存 `follow` 再改 `next[cur]`**。"
        "反过来写的话，`cur` 的后继信息已经被覆盖，链当场断掉——这是链表题第一大坑。\n\n"
        "★ 每个节点恰好被改一次 `next`，所以改写次数就是 `n`。能自己推导出这个数，"
        "说明你真的看懂了循环执行了几轮。"
    ),
    input_format="第一行 `n`；第二行 `n` 个整数（按链表顺序）。",
    output_format="三行：逆置后序列；新的 head 下标；next 改写次数。",
    constraints_md="- 1 ≤ n ≤ 10⁵\n- |元素| ≤ 10⁹",
    inputs=[
        "5\n1 2 3 4 5\n",
        "1\n42\n",
        "2\n-1 -2\n",
        "6\n10 20 30 40 50 60\n",
    ],
    samples=3,
    oracle=_oracle_02,
    solution=r'''#include <cstdio>
#include <vector>
using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;

    vector<int> data(n + 1), nxt(n + 1);
    for (int i = 1; i <= n; i++) {
        scanf("%d", &data[i]);
        nxt[i] = (i < n) ? i + 1 : 0;
    }

    int head = 1;
    int prev = 0, cur = head, rewrites = 0;
    while (cur) {
        int follow = nxt[cur];   // 先记后路
        nxt[cur] = prev;         // 再掉头
        prev = cur;
        cur = follow;
        rewrites++;
    }
    head = prev;

    int p = head;
    bool first = true;
    while (p) {
        if (!first) putchar(' ');
        printf("%d", data[p]);
        first = false;
        p = nxt[p];
    }
    putchar('\n');
    printf("%d\n%d\n", head, rewrites);
    return 0;
}
''',
    alt=r'''#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;
    vector<int> data(n + 1), nxt(n + 1);
    for (int i = 1; i <= n; i++) {
        cin >> data[i];
        nxt[i] = (i < n) ? i + 1 : 0;
    }

    // 另一条路：三指针同时推进，但把「头结点的接管」放在循环外单独做，
    // 循环里只处理「已经确定 prev 的情况」。
    int head = 1;
    if (head != 0) {
        int prev = head;
        int cur = nxt[head];
        nxt[head] = 0;              // 原来的头变成新尾巴
        while (cur) {
            int follow = nxt[cur];
            nxt[cur] = prev;
            prev = cur;
            cur = follow;
        }
        head = prev;
    }

    int rewrites = n;               // 每个节点恰好改一次 next
    int p = head;
    string out;
    out.reserve((size_t)n * 4);
    while (p) {
        out += to_string(data[p]);
        p = nxt[p];
        if (p) out += ' ';
    }
    cout << out << '\n' << head << '\n' << rewrites << '\n';
    return 0;
}
''',
)


# --------------------------------------------------------------------- #
#  栈与队列（difficulty 3）
# --------------------------------------------------------------------- #

def _oracle_03(text: str) -> str:
    """循环队列：用 Python 列表手工维护 front/rear 与「牺牲一个单元」的判满规则。"""
    lines = [ln.strip() for ln in text.strip().split("\n") if ln.strip()]
    MAXS = 5
    q = [0] * MAXS
    f = r = 0
    out = []
    for ln in lines[1:]:
        parts = ln.split()
        op = parts[0]
        if op == "push":
            x = int(parts[1])
            if (r + 1) % MAXS == f:
                out.append("FULL")
            else:
                q[r] = x
                r = (r + 1) % MAXS
                out.append("OK")
        elif op == "pop":
            if f == r:
                out.append("EMPTY")
            else:
                out.append(str(q[f]))
                f = (f + 1) % MAXS
        elif op == "front":
            out.append("EMPTY" if f == r else str(q[f]))
        elif op == "size":
            out.append(str((r - f + MAXS) % MAXS))
    return "\n".join(out) + "\n"


add(
    title="循环队列的操作序列模拟",
    section=SECTION,
    difficulty=3, score=12, tags=["编程精练", "队列", "循环队列", "判空判满"],
    statement_md=(
        "用一个**容量 `MAXSIZE = 5`** 的循环队列（数组实现，"
        "**牺牲一个存储单元**来区分队空与队满），依次执行 `m` 条操作，"
        "对每条操作输出一行结果。\n\n"
        "队空 `front == rear`，队满 `(rear + 1) % MAXSIZE == front`，"
        "元素个数 `(rear - front + MAXSIZE) % MAXSIZE`。因此**实际最多存 4 个元素**。\n\n"
        "| 操作 | 输出 |\n"
        "|---|---|\n"
        "| `push x` | 队满输出 `FULL`，否则入队并输出 `OK` |\n"
        "| `pop` | 队空输出 `EMPTY`，否则弹出队头并输出该值 |\n"
        "| `front` | 队空输出 `EMPTY`，否则输出队头（不弹出） |\n"
        "| `size` | 输出当前元素个数 |\n\n"
        "★ 为什么必须「牺牲一个单元」：只用 `front == rear` 一个条件，"
        "**队空和队满的表达式完全一样**，没法区分。留一个空位后，"
        "`rear` 永远追不上 `front`，两者就分开了。\n\n"
        "★ 另一种做法是额外维护 `count`，那就不必牺牲单元（能存满 5 个）——"
        "但本题**明确规定**用牺牲单元法，注意别把容量上限搞错。"
    ),
    input_format="第一行 `m`；之后 `m` 行，每行一条操作。",
    output_format="`m` 行，每行对应一条操作的输出。",
    constraints_md="- 1 ≤ m ≤ 10⁵\n- 1 ≤ x ≤ 10⁹\n- MAXSIZE 固定为 5（最多存 4 个）",
    inputs=[
        "8\npush 1\npush 2\npush 3\npush 4\npush 5\nfront\npop\nsize\n",
        "6\npop\nfront\nsize\npush 9\nfront\nsize\n",
        "9\npush 1\npop\npush 2\npop\nsize\nfront\npop\npop\nfront\n",
        "5\nsize\npush 7\npush 8\nsize\nfront\n",
    ],
    samples=3,
    oracle=_oracle_03,
    solution=r'''#include <cstdio>
#include <cstring>
using namespace std;

const int MAXSIZE = 5;

int main() {
    int m;
    if (scanf("%d", &m) != 1) return 0;

    static int q[MAXSIZE];
    int front = 0, rear = 0;

    char op[16];
    for (int i = 0; i < m; i++) {
        scanf("%s", op);
        if (strcmp(op, "push") == 0) {
            int x;
            scanf("%d", &x);
            if ((rear + 1) % MAXSIZE == front) {
                printf("FULL\n");
            } else {
                q[rear] = x;
                rear = (rear + 1) % MAXSIZE;
                printf("OK\n");
            }
        } else if (strcmp(op, "pop") == 0) {
            if (front == rear) {
                printf("EMPTY\n");
            } else {
                printf("%d\n", q[front]);
                front = (front + 1) % MAXSIZE;
            }
        } else if (strcmp(op, "front") == 0) {
            if (front == rear) printf("EMPTY\n");
            else printf("%d\n", q[front]);
        } else {
            printf("%d\n", (rear - front + MAXSIZE) % MAXSIZE);
        }
    }
    return 0;
}
''',
    alt=r'''#include <bits/stdc++.h>
using namespace std;

const int MAXSIZE = 5;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int m;
    if (!(cin >> m)) return 0;

    // 另一条路：不用 front/rear 两个游标，改成「基址 + 头 + 计数器」。
    // 只要 count 上限写成 MAXSIZE-1，行为就与牺牲单元法完全等价。
    vector<int> buf(MAXSIZE);
    int base = 0;       // 队头所在的物理下标
    int count = 0;

    string op;
    for (int i = 0; i < m; i++) {
        cin >> op;
        if (op == "push") {
            int x;
            cin >> x;
            if (count == MAXSIZE - 1) {
                cout << "FULL\n";
            } else {
                buf[(base + count) % MAXSIZE] = x;
                count++;
                cout << "OK\n";
            }
        } else if (op == "pop") {
            if (count == 0) {
                cout << "EMPTY\n";
            } else {
                cout << buf[base] << '\n';
                base = (base + 1) % MAXSIZE;
                count--;
            }
        } else if (op == "front") {
            if (count == 0) cout << "EMPTY\n";
            else cout << buf[base] << '\n';
        } else {
            cout << count << '\n';
        }
    }
    return 0;
}
''',
)


_PREC = {"+": 1, "-": 1, "*": 2, "/": 2, "(": 0}


def _trunc_div(a: int, b: int) -> int:
    """与 C/C++ 一致的整数除法：向零截断。"""
    q = abs(a) // abs(b)
    return -q if (a < 0) != (b < 0) else q


def _to_postfix(s: str) -> str:
    out: list[str] = []
    st: list[str] = []
    for ch in s:
        if ch.isalnum():
            out.append(ch)
        elif ch == "(":
            st.append(ch)
        elif ch == ")":
            while st and st[-1] != "(":
                out.append(st.pop())
            st.pop()
        else:
            while st and _PREC[st[-1]] >= _PREC[ch]:
                out.append(st.pop())
            st.append(ch)
    while st:
        out.append(st.pop())
    return "".join(out)


def _eval_postfix(post: str) -> int:
    st: list[int] = []
    for ch in post:
        if ch.isdigit():
            st.append(int(ch))
        elif ch.isalpha():
            st.append(ord(ch) - ord("a") + 1)     # 与 C++ 的 ch - 'a' + 1 一致
        else:
            b = st.pop()
            a = st.pop()
            if ch == "+":
                st.append(a + b)
            elif ch == "-":
                st.append(a - b)
            elif ch == "*":
                st.append(a * b)
            else:
                st.append(_trunc_div(a, b))
    return st[0]


def _oracle_04(text: str) -> str:
    """中缀转后缀：照调度场规则一步步走（不复用任何现成转换）。"""
    s = text.strip()
    post = _to_postfix(s)
    return "%s\n%d\n" % (post, _eval_postfix(post))


add(
    title="中缀表达式转后缀",
    section=SECTION,
    difficulty=3, score=12, tags=["编程精练", "栈", "表达式求值", "调度场"],
    statement_md=(
        "读入一行**中缀表达式**（操作数为单个 `0-9` 数字或小写字母，"
        "运算符只有 `+ - * /` 与括号，**不含空格、不含一元负号**），输出两行：\n"
        "1. 对应的**后缀表达式**（逆波兰式，不加空格）\n"
        "2. 该表达式的值（整数，除法**向零截断**，与 C/C++ 的 `/` 一致）\n\n"
        "调度场（shunting-yard）的规则只有三条：\n"
        "- 遇操作数：直接进输出\n"
        "- 遇 `(`：压栈\n"
        "- 遇运算符：把栈顶**优先级 ≥ 自己**的运算符全弹到输出，再压自己（`(` 优先级最低，弹不动）\n"
        "- 遇 `)`：弹到遇到 `(` 为止，`(` 丢弃\n\n"
        "★ 后缀求值只要一个栈：遇数字压栈，遇运算符就弹两个（**先弹出来的是右操作数**）算完压回。\n\n"
        "⚠️ 两个高频错：\n"
        "1. 减法/除法弹出顺序写反 → `a-b` 算成 `b-a`；\n"
        "2. 用 Python 的 `//` 做整除——它是**向下取整**，`-7//2 = -4`，"
        "而 C 的 `-7/2 = -3`（向零截断）。跨语言对照时必须自己实现截断除法。"
    ),
    input_format="一行中缀表达式（长度 ≤ 200）。",
    output_format="两行：后缀表达式；表达式的值。",
    constraints_md="- 1 ≤ 表达式长度 ≤ 200\n- 保证合法、除数非 0、中间结果在 32 位整数内",
    inputs=[
        "3+4*2\n",
        "(3+4)*2\n",
        "8/3\n",
        "a+b*c-d/e\n",
        "((1+2)*(3+4))\n",
        "1+2*3-4/2\n",
        "2*(3+4*5)/7\n",
    ],
    samples=3,
    oracle=_oracle_04,
    solution=r'''#include <cstdio>
#include <cstring>
#include <string>
#include <vector>
using namespace std;

static int prec(char c) {
    if (c == '+' || c == '-') return 1;
    if (c == '*' || c == '/') return 2;
    return 0;                       // '('
}

int main() {
    char buf[512];
    if (!fgets(buf, sizeof(buf), stdin)) return 0;
    string s(buf);
    while (!s.empty() && (s.back() == '\n' || s.back() == '\r')) s.pop_back();

    string out;
    vector<char> st;
    for (char ch : s) {
        if ((ch >= '0' && ch <= '9') || (ch >= 'a' && ch <= 'z')) {
            out += ch;
        } else if (ch == '(') {
            st.push_back(ch);
        } else if (ch == ')') {
            while (!st.empty() && st.back() != '(') {
                out += st.back();
                st.pop_back();
            }
            if (!st.empty()) st.pop_back();
        } else {
            while (!st.empty() && prec(st.back()) >= prec(ch)) {
                out += st.back();
                st.pop_back();
            }
            st.push_back(ch);
        }
    }
    while (!st.empty()) {
        out += st.back();
        st.pop_back();
    }

    vector<long long> vs;
    for (char ch : out) {
        if (ch >= '0' && ch <= '9') {
            vs.push_back(ch - '0');
        } else if (ch >= 'a' && ch <= 'z') {
            vs.push_back(ch - 'a' + 1);
        } else {
            long long b = vs.back(); vs.pop_back();
            long long a = vs.back(); vs.pop_back();
            long long r = 0;
            if (ch == '+') r = a + b;
            else if (ch == '-') r = a - b;
            else if (ch == '*') r = a * b;
            else r = a / b;          // C 的整除天然向零截断
            vs.push_back(r);
        }
    }

    printf("%s\n%lld\n", out.c_str(), vs.back());
    return 0;
}
''',
    alt=r'''#include <bits/stdc++.h>
using namespace std;

static int prec(char c) {
    switch (c) {
        case '+': case '-': return 1;
        case '*': case '/': return 2;
        default: return 0;
    }
}

// 另一条路：求值不走后缀栈，改用**递归下降**直接按优先级算。
// 后缀串仍然用调度场单独生成——两条腿互不依赖。
struct Parser {
    const string& s;
    size_t i = 0;
    explicit Parser(const string& t) : s(t) {}

    long long expr() {
        long long v = term();
        while (i < s.size() && (s[i] == '+' || s[i] == '-')) {
            char op = s[i++];
            long long r = term();
            v = (op == '+') ? v + r : v - r;
        }
        return v;
    }
    long long term() {
        long long v = factor();
        while (i < s.size() && (s[i] == '*' || s[i] == '/')) {
            char op = s[i++];
            long long r = factor();
            v = (op == '*') ? v * r : v / r;
        }
        return v;
    }
    long long factor() {
        if (s[i] == '(') {
            i++;
            long long v = expr();
            i++;                     // 跳过 ')'
            return v;
        }
        char c = s[i++];
        if (c >= '0' && c <= '9') return c - '0';
        return c - 'a' + 1;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    getline(cin, s);
    while (!s.empty() && (s.back() == '\r' || s.back() == '\n')) s.pop_back();

    string out;
    vector<char> st;
    for (char ch : s) {
        if (isalnum((unsigned char)ch)) {
            out += ch;
        } else if (ch == '(') {
            st.push_back(ch);
        } else if (ch == ')') {
            while (!st.empty() && st.back() != '(') { out += st.back(); st.pop_back(); }
            if (!st.empty()) st.pop_back();
        } else {
            while (!st.empty() && prec(st.back()) >= prec(ch)) { out += st.back(); st.pop_back(); }
            st.push_back(ch);
        }
    }
    while (!st.empty()) { out += st.back(); st.pop_back(); }

    Parser p(s);
    long long val = p.expr();
    cout << out << '\n' << val << '\n';
    return 0;
}
''',
)


# --------------------------------------------------------------------- #
#  树（difficulty 3~4）
# --------------------------------------------------------------------- #

def _oracle_05(text: str) -> str:
    """先序 + 中序 → 后序与高度：老老实实建树再遍历。"""
    d = text.split()
    n = int(d[0])
    pre = d[1:1 + n]
    ino = d[1 + n:1 + 2 * n]
    out: list[str] = []

    def walk(pl: int, pr: int, il: int, ir: int) -> int:
        if pl > pr:
            return 0
        root = pre[pl]
        k = il
        while ino[k] != root:
            k += 1
        left_n = k - il
        hl = walk(pl + 1, pl + left_n, il, k - 1)
        hr = walk(pl + left_n + 1, pr, k + 1, ir)
        out.append(root)
        return (hl if hl > hr else hr) + 1

    h = walk(0, n - 1, 0, n - 1)
    return "%s\n%d\n" % (" ".join(out), h)


def _tree_case(pre: list[int], ino: list[int]) -> str:
    return "%d\n%s\n%s\n" % (len(pre), " ".join(map(str, pre)), " ".join(map(str, ino)))


def _rand_tree_case() -> str:
    """随机生成一棵 400 结点的树，导出它的先序与中序（可复现）。"""
    import random
    rnd = random.Random(20261021)
    n = 400
    vals = list(range(1, n + 1))
    rnd.shuffle(vals)
    lch = [None] * n
    rch = [None] * n
    root = 0
    for i in range(1, n):
        # 随机插入到某个空位置（模拟一棵大体平衡的树）
        cur = root
        while True:
            side = rnd.randint(0, 1)
            tgt = lch if side == 0 else rch
            if tgt[cur] is None:
                tgt[cur] = i
                break
            cur = tgt[cur]

    pre, ino = [], []

    def dfs(u):
        if u is None:
            return
        pre.append(vals[u])
        dfs(lch[u])
        ino.append(vals[u])
        dfs(rch[u])

    dfs(root)
    return _tree_case(pre, ino)


add(
    title="由先序中序建树并输出后序",
    section=SECTION,
    difficulty=3, score=12, tags=["编程精练", "二叉树", "遍历", "递归"],
    statement_md=(
        "给定一棵二叉树的**先序**序列与**中序**序列（结点值互不相同），输出两行：\n"
        "1. **后序**遍历序列\n"
        "2. 树的**高度**（空树为 0，单结点为 1）\n\n"
        "★ 为什么这两组序列能唯一确定一棵树：**先序的第一个一定是根**；"
        "拿着这个根去中序里一找，左边那段就是左子树的中序、右边那段是右子树的中序，"
        "而它们的元素个数又反过来把先序切成了两段。于是递归成立。\n\n"
        "★ 想清楚三件事，这题就不会写错：\n"
        "- 根在哪：`pre[pl]`\n"
        "- 左子树有几个结点：`k - il`（`k` 是根在中序里的位置）\n"
        "- 左子树的先序区间：`[pl+1, pl+left_n]`，右子树是 `[pl+left_n+1, pr]`\n\n"
        "⚠️ 只给「先序 + 后序」是**不能**唯一建树的——那时左/右子树分不清，"
        "必须配中序（或「同时给出空指针位置的扩展先序」）。"
    ),
    input_format="第一行 `n`；第二行 `n` 个整数（先序）；第三行 `n` 个整数（中序）。",
    output_format="两行：后序序列（空格分隔）；树高。",
    constraints_md="- 1 ≤ n ≤ 2000\n- 结点值互不相同",
    inputs=[
        _tree_case([1, 2, 4, 5, 3, 6], [4, 2, 5, 1, 6, 3]),
        _tree_case([1], [1]),
        _tree_case([1, 2, 3], [3, 2, 1]),
        _tree_case([3, 9, 20, 15, 7], [9, 3, 15, 20, 7]),
        _rand_tree_case(),
    ],
    samples=3,
    oracle=_oracle_05,
    solution=r'''#include <cstdio>
#include <vector>
#include <unordered_map>
using namespace std;

int n;
vector<int> pre, ino, post;
unordered_map<int, int> pos;

int walk(int pl, int pr, int il, int ir) {
    if (pl > pr) return 0;
    int root = pre[pl];
    int k = pos[root];
    int leftN = k - il;
    int hl = walk(pl + 1, pl + leftN, il, k - 1);
    int hr = walk(pl + leftN + 1, pr, k + 1, ir);
    post.push_back(root);
    return (hl > hr ? hl : hr) + 1;
}

int main() {
    if (scanf("%d", &n) != 1) return 0;
    pre.resize(n);
    ino.resize(n);
    for (int i = 0; i < n; i++) scanf("%d", &pre[i]);
    for (int i = 0; i < n; i++) {
        scanf("%d", &ino[i]);
        pos[ino[i]] = i;
    }

    post.reserve(n);
    int h = walk(0, n - 1, 0, n - 1);

    for (int i = 0; i < n; i++) {
        printf("%d", post[i]);
        putchar(i + 1 == n ? '\n' : ' ');
    }
    printf("%d\n", h);
    return 0;
}
''',
    alt=r'''#include <bits/stdc++.h>
using namespace std;

// 另一条路：**不建树**，直接用区间递归把后序压进结果里，
// 高度也在同一趟递归里返回。
struct Solver {
    vector<int> pre, ino;
    vector<int> post;

    int rec(int pl, int pr, int il, int ir) {
        if (pl > pr) return 0;
        int root = pre[pl];
        int k = il;
        while (ino[k] != root) k++;      // 线性找根，不用哈希表
        int leftN = k - il;
        int hl = rec(pl + 1, pl + leftN, il, k - 1);
        int hr = rec(pl + leftN + 1, pr, k + 1, ir);
        post.push_back(root);
        return max(hl, hr) + 1;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    if (!(cin >> n)) return 0;
    Solver s;
    s.pre.resize(n);
    s.ino.resize(n);
    for (int i = 0; i < n; i++) cin >> s.pre[i];
    for (int i = 0; i < n; i++) cin >> s.ino[i];
    int h = s.rec(0, n - 1, 0, n - 1);
    for (int i = 0; i < n; i++) {
        if (i) cout << ' ';
        cout << s.post[i];
    }
    cout << '\n' << h << '\n';
    return 0;
}
''',
)


def _oracle_06(text: str) -> str:
    """哈夫曼 WPL：小根堆反复取两个最小合并（不建树，只累加）。"""
    import heapq
    d = text.split()
    n = int(d[0])
    w = [int(v) for v in d[1:1 + n]]
    if n == 1:
        return "0\n"
    h = list(w)
    heapq.heapify(h)
    total = 0
    while len(h) > 1:
        a = heapq.heappop(h)
        b = heapq.heappop(h)
        s = a + b
        total += s
        heapq.heappush(h, s)
    return "%d\n" % total


def _rand_huffman_case() -> str:
    import random
    rnd = random.Random(20261022)
    n = 2000
    w = rnd.sample(range(1, 10 ** 9), n)      # 互不相同
    return "%d\n%s\n" % (n, " ".join(map(str, w)))


add(
    title="哈夫曼编码的总长度",
    section=SECTION,
    difficulty=4, score=14, tags=["编程精练", "哈夫曼树", "贪心", "堆"],
    statement_md=(
        "给定 `n` 个字符的权值（出现频次），按哈夫曼算法构造最优二叉树，"
        "输出**带权路径长度 WPL**（`Σ 权值 × 编码长度`）。\n\n"
        "算法只有一句话：**每次取出权值最小的两个结点合并，新结点权值 = 两者之和，"
        "把新结点放回集合**，重复 `n-1` 次。\n\n"
        "★ 一个省事的恒等式：**WPL 恰好等于每次合并产生的新权值之和**。"
        "所以根本不用真的建树，边合并边累加就行。\n\n"
        "★ 为什么贪心是对的：权值最小的两个字符必须放在**最深**的位置（它们的贡献被乘的次数最多、"
        "但基数最小，这样换出来最划算）。合并之后，这个「两兄弟」在后续计算里就等价于一个"
        "权值为和的新字符——于是子问题结构完全一样。\n\n"
        "⚠️ 别把它和「构建哈夫曼编码串」混了：**WPL 唯一，但树的形态和每个字符的码长不唯一**"
        "（权值相同的结点谁当左谁当右都行）。这也是本题只验 WPL、不验具体编码的原因。\n\n"
        "⚠️ `n` 到 10⁵ 时，`WPL` 可能达到 10¹⁴ 量级，**必须用 64 位整数**。"
    ),
    input_format="第一行 `n`；第二行 `n` 个权值（保证互不相同）。",
    output_format="一行：WPL。",
    constraints_md="- 2 ≤ n ≤ 10⁵（n = 1 时 WPL 记为 0）\n- 1 ≤ wᵢ ≤ 10⁹\n- WPL 可能超过 32 位",
    inputs=[
        "5\n1 2 3 4 5\n",
        "2\n7 3\n",
        "1\n9\n",
        "4\n10 20 30 40\n",
        "6\n5 9 12 13 16 45\n",
        _rand_huffman_case(),
    ],
    samples=3,
    oracle=_oracle_06,
    solution=r'''#include <cstdio>
#include <queue>
#include <vector>
using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;

    priority_queue<long long, vector<long long>, greater<long long>> pq;
    for (int i = 0; i < n; i++) {
        long long w;
        scanf("%lld", &w);
        pq.push(w);
    }
    if (n == 1) {
        printf("0\n");
        return 0;
    }

    long long wpl = 0;
    while (pq.size() > 1) {
        long long a = pq.top(); pq.pop();
        long long b = pq.top(); pq.pop();
        long long s = a + b;
        wpl += s;
        pq.push(s);
    }
    printf("%lld\n", wpl);
    return 0;
}
''',
    alt=r'''#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;
    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    if (n == 1) {
        cout << 0 << '\n';
        return 0;
    }

    // 另一条路：不用堆，每轮线性扫出两个最小值并「标记为已用」。
    // O(n^2)，n 小的用例够用；结果与堆版本必须一致。
    sort(a.begin(), a.end());
    vector<long long> cur = a;
    long long wpl = 0;
    int m = n;
    while (m > 1) {
        // cur 保持有序（插入时用 lower_bound 维护），取前两个即可
        long long x = cur[0], y = cur[1];
        long long s = x + y;
        wpl += s;
        cur.erase(cur.begin(), cur.begin() + 2);
        cur.insert(lower_bound(cur.begin(), cur.end(), s), s);
        m--;
    }
    cout << wpl << '\n';
    return 0;
}
''',
)


def _oracle_07(text: str) -> str:
    """图的 BFS / DFS：邻接表 + 队列 / 递归，邻接点升序。"""
    d = text.split()
    n, m, s = int(d[0]), int(d[1]), int(d[2])
    adj: dict[int, list[int]] = {}
    pos = 3
    for _ in range(m):
        u, v = int(d[pos]), int(d[pos + 1])
        pos += 2
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)
    for k in adj:
        adj[k].sort()

    visited = [False] * (n + 1)
    bfs: list[int] = []
    from collections import deque
    dq = deque([s])
    visited[s] = True
    while dq:
        u = dq.popleft()
        bfs.append(u)
        for v in adj.get(u, []):
            if not visited[v]:
                visited[v] = True
                dq.append(v)

    visited = [False] * (n + 1)
    dfs: list[int] = []

    def go(u: int) -> None:
        visited[u] = True
        dfs.append(u)
        for v in adj.get(u, []):
            if not visited[v]:
                go(v)

    go(s)
    return "%s\n%s\n" % (" ".join(map(str, bfs)), " ".join(map(str, dfs)))


def _rand_graph_undirected() -> str:
    import random
    rnd = random.Random(20261023)
    n, m = 60, 150
    edges = set()
    while len(edges) < m:
        u = rnd.randint(1, n)
        v = rnd.randint(1, n)
        if u == v:
            continue
        edges.add((min(u, v), max(u, v)))
    lines = ["%d %d 1" % (n, len(edges))]
    for u, v in sorted(edges):
        lines.append("%d %d" % (u, v))
    return "\n".join(lines) + "\n"


add(
    title="图的广度优先与深度优先遍历",
    section=SECTION,
    difficulty=3, score=12, tags=["编程精练", "图", "BFS", "DFS", "邻接表"],
    statement_md=(
        "给定 `n` 个点、`m` 条**无向**边和起点 `s`，输出两行：\n"
        "1. 从 `s` 出发的 **BFS** 序列\n"
        "2. 从 `s` 出发的 **DFS** 序列\n\n"
        "规定：**访问某个点时，按邻接点编号从小到大处理**。只遍历 `s` 所在的连通分量。\n\n"
        "★ BFS 用队列：出队一个就把它所有未访问的邻居**一次性全部入队**并立刻标记访问。"
        "「入队时就标记」是关键——不然同一个点可能被相邻的多个点重复塞进队列。\n\n"
        "★ DFS 用递归（或显式栈）。**如果用栈做迭代版，要注意压栈顺序要反过来**："
        "想按编号升序访问，就得**降序压栈**（栈是后进先出）。"
        "顺序压栈会得到「降序访问」的结果，与递归版对不上。\n\n"
        "★ 无向边要**双向加**。只加 `u→v` 是这道题最隐蔽的错——图看起来能跑，"
        "但序列会缺一大截。"
    ),
    input_format="第一行 `n m s`；接着 `m` 行 `u v`（无向边）。",
    output_format="两行：BFS 序列；DFS 序列。",
    constraints_md="- 1 ≤ n ≤ 10⁵，0 ≤ m ≤ 2×10⁵\n- 1 ≤ s ≤ n",
    inputs=[
        "5 4 1\n1 2\n1 3\n2 4\n3 5\n",
        "1 0 1\n",
        "6 6 2\n1 2\n2 3\n3 4\n4 5\n5 6\n6 2\n",
        "4 4 3\n1 2\n2 3\n3 4\n4 1\n",
        _rand_graph_undirected(),
    ],
    samples=3,
    oracle=_oracle_07,
    solution=r'''#include <cstdio>
#include <vector>
#include <queue>
#include <algorithm>
using namespace std;

int n, m, s;
vector<vector<int>> adj;
vector<char> vis;
vector<int> dfsOrder;

void dfs(int u) {
    vis[u] = 1;
    dfsOrder.push_back(u);
    for (int v : adj[u]) {
        if (!vis[v]) dfs(v);
    }
}

int main() {
    if (scanf("%d %d %d", &n, &m, &s) != 3) return 0;
    adj.assign(n + 1, {});
    for (int i = 0; i < m; i++) {
        int u, v;
        scanf("%d %d", &u, &v);
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    for (int i = 1; i <= n; i++) sort(adj[i].begin(), adj[i].end());

    vis.assign(n + 1, 0);
    vector<int> bfsOrder;
    queue<int> q;
    q.push(s);
    vis[s] = 1;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        bfsOrder.push_back(u);
        for (int v : adj[u]) {
            if (!vis[v]) {
                vis[v] = 1;
                q.push(v);
            }
        }
    }

    vis.assign(n + 1, 0);
    dfsOrder.clear();
    dfs(s);

    for (size_t i = 0; i < bfsOrder.size(); i++) {
        if (i) putchar(' ');
        printf("%d", bfsOrder[i]);
    }
    putchar('\n');
    for (size_t i = 0; i < dfsOrder.size(); i++) {
        if (i) putchar(' ');
        printf("%d", dfsOrder[i]);
    }
    putchar('\n');
    return 0;
}
''',
    alt=r'''#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, s;
    if (!(cin >> n >> m >> s)) return 0;

    // 另一条路：邻接矩阵 + 迭代 DFS（显式栈）。
    // n 小时矩阵更直观；DFS 想按升序访问就必须**逆序压栈**。
    vector<vector<char>> g(n + 1, vector<char>(n + 1, 0));
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        g[u][v] = g[v][u] = 1;
    }

    vector<char> vis(n + 1, 0);
    vector<int> bfs;
    queue<int> q;
    q.push(s);
    vis[s] = 1;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        bfs.push_back(u);
        for (int v = 1; v <= n; v++) {
            if (g[u][v] && !vis[v]) {
                vis[v] = 1;
                q.push(v);
            }
        }
    }

    fill(vis.begin(), vis.end(), 0);
    vector<int> dfs;
    vector<int> st;
    st.push_back(s);
    while (!st.empty()) {
        int u = st.back();
        st.pop_back();
        if (vis[u]) continue;
        vis[u] = 1;
        dfs.push_back(u);
        for (int v = n; v >= 1; v--) {       // 逆序压栈 → 升序出栈
            if (g[u][v] && !vis[v]) st.push_back(v);
        }
    }

    for (size_t i = 0; i < bfs.size(); i++) { if (i) cout << ' '; cout << bfs[i]; }
    cout << '\n';
    for (size_t i = 0; i < dfs.size(); i++) { if (i) cout << ' '; cout << dfs[i]; }
    cout << '\n';
    return 0;
}
''',
)


def _oracle_08(text: str) -> str:
    """拓扑排序：小根堆 Kahn（每次取当前入度 0 的最小点）。"""
    import heapq
    d = text.split()
    n, m = int(d[0]), int(d[1])
    adj: dict[int, list[int]] = {}
    indeg = [0] * (n + 1)
    pos = 2
    for _ in range(m):
        u, v = int(d[pos]), int(d[pos + 1])
        pos += 2
        adj.setdefault(u, []).append(v)
        indeg[v] += 1
    h = [i for i in range(1, n + 1) if indeg[i] == 0]
    heapq.heapify(h)
    out: list[int] = []
    while h:
        u = heapq.heappop(h)
        out.append(u)
        for v in adj.get(u, []):
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(h, v)
    if len(out) != n:
        return "CYCLE\n"
    return " ".join(map(str, out)) + "\n"


def _rand_dag_case() -> str:
    import random
    rnd = random.Random(20261024)
    n, m = 200, 600
    edges = set()
    while len(edges) < m:
        u = rnd.randint(1, n)
        v = rnd.randint(1, n)
        if u < v:                       # 只连「小编号 → 大编号」，保证无环
            edges.add((u, v))
    lines = ["%d %d" % (n, len(edges))]
    for u, v in sorted(edges):
        lines.append("%d %d" % (u, v))
    return "\n".join(lines) + "\n"


add(
    title="拓扑排序的最小字典序",
    section=SECTION,
    difficulty=3, score=12, tags=["编程精练", "图", "拓扑排序", "Kahn", "堆"],
    statement_md=(
        "给定 `n` 个点和 `m` 条**有向**边（可能有重边），输出**字典序最小**的拓扑序；"
        "若图中有环，输出 `CYCLE`。\n\n"
        "★ 普通 Kahn 用队列就够了，但要**字典序最小**，就得把队列换成**小根堆**："
        "「当前所有入度为 0 的点」里永远优先取编号最小的那个。\n\n"
        "★ 为什么这样贪心是对的：入度为 0 的点之间**没有任何先后约束**，"
        "谁先走都不影响可行性；既然可以随便选，那当然选最小的。"
        "选完它只可能让更多点入度归零，不会把局面弄坏——这是标准的「交换论证」。\n\n"
        "⚠️ 重边会让入度算多。如果没去重，删边时减两次、入度归零的时机就错了"
        "（本题的数据可能含重边，注意按边的条数老老实实加减，别自作聪明去重）。\n\n"
        "⚠️ 判环：如果最后输出的点数 `< n`，说明剩下的点互相卡住了 → 有环。"
    ),
    input_format="第一行 `n m`；接着 `m` 行 `u v`（有向边 u→v）。",
    output_format="一行：字典序最小的拓扑序；有环输出 `CYCLE`。",
    constraints_md="- 1 ≤ n ≤ 10⁵，0 ≤ m ≤ 2×10⁵\n- 可能有重边",
    inputs=[
        "6 6\n6 3\n6 1\n5 1\n5 2\n3 4\n4 2\n",
        "3 0\n",
        "3 3\n1 2\n2 3\n3 1\n",
        "4 4\n1 2\n2 3\n3 4\n1 4\n",
        "2 2\n1 2\n1 2\n",
        _rand_dag_case(),
    ],
    samples=3,
    oracle=_oracle_08,
    solution=r'''#include <cstdio>
#include <vector>
#include <queue>
#include <functional>
using namespace std;

int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;

    vector<vector<int>> adj(n + 1);
    vector<int> indeg(n + 1, 0);
    for (int i = 0; i < m; i++) {
        int u, v;
        scanf("%d %d", &u, &v);
        adj[u].push_back(v);
        indeg[v]++;
    }

    priority_queue<int, vector<int>, greater<int>> pq;
    for (int i = 1; i <= n; i++) {
        if (indeg[i] == 0) pq.push(i);
    }

    vector<int> order;
    order.reserve(n);
    while (!pq.empty()) {
        int u = pq.top();
        pq.pop();
        order.push_back(u);
        for (int v : adj[u]) {
            if (--indeg[v] == 0) pq.push(v);
        }
    }

    if ((int)order.size() != n) {
        printf("CYCLE\n");
        return 0;
    }
    for (int i = 0; i < n; i++) {
        printf("%d", order[i]);
        putchar(i + 1 == n ? '\n' : ' ');
    }
    return 0;
}
''',
    alt=r'''#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    if (!(cin >> n >> m)) return 0;
    vector<vector<int>> adj(n + 1);
    vector<int> indeg(n + 1, 0);
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        indeg[v]++;
    }

    // 另一条路：不用堆，每轮线性扫一遍找「入度为 0 的最小未用点」。
    // O(n^2)，n 大的用例会慢，但逻辑与堆版本等价。
    vector<char> used(n + 1, 0);
    vector<int> order;
    order.reserve(n);
    for (int step = 0; step < n; step++) {
        int pick = 0;
        for (int i = 1; i <= n; i++) {
            if (!used[i] && indeg[i] == 0) { pick = i; break; }
        }
        if (pick == 0) break;
        used[pick] = 1;
        order.push_back(pick);
        for (int v : adj[pick]) indeg[v]--;
    }

    if ((int)order.size() != n) {
        cout << "CYCLE\n";
        return 0;
    }
    for (int i = 0; i < n; i++) {
        if (i) cout << ' ';
        cout << order[i];
    }
    cout << '\n';
    return 0;
}
''',
)


# --------------------------------------------------------------------- #
#  排序（difficulty 3）
# --------------------------------------------------------------------- #

def _oracle_09(text: str) -> str:
    """快排一趟划分：教材的「挖坑填数」法（枢轴取首元素）。"""
    d = text.split()
    n = int(d[0])
    a = [int(v) for v in d[1:1 + n]]
    pivot = a[0]
    low, high = 0, n - 1
    while low < high:
        while low < high and a[high] >= pivot:
            high -= 1
        a[low] = a[high]
        while low < high and a[low] <= pivot:
            low += 1
        a[high] = a[low]
    a[low] = pivot
    return "%s\n%d\n" % (" ".join(map(str, a)), low + 1)


add(
    title="快排划分后主元的落点",
    section=SECTION,
    difficulty=3, score=12, tags=["编程精练", "排序", "快速排序", "划分"],
    statement_md=(
        "对给定序列做**一趟快速排序的划分**：以**第一个元素**为枢轴，"
        "按教材的**「挖坑填数」**法划分。输出两行：\n"
        "1. 划分后的序列\n"
        "2. 枢轴的最终下标（**1-based**）\n\n"
        "挖坑法的流程（务必照这个来，不同划分法的结果不同）：\n"
        "```\n"
        "pivot = a[low]\n"
        "while low < high:\n"
        "    while low < high and a[high] >= pivot: high--\n"
        "    a[low] = a[high]                      # 右边的坑填到左边\n"
        "    while low < high and a[low] <= pivot: low++\n"
        "    a[high] = a[low]                      # 左边的坑填到右边\n"
        "a[low] = pivot\n"
        "```\n\n"
        "★ 「挖坑」这个名字来自过程本身：`a[low]` 的值已经被 `pivot` 存下来了，"
        "所以那个位置**空了**，是个可以随便覆盖的坑。于是就不需要 `swap`，"
        "一路「拿右边的填左边的坑、再拿左边的填右边的坑」，最后把 `pivot` 补进最后一个坑。\n\n"
        "★ 划分完的性质：`pivot` 左边全 `≤ pivot`、右边全 `≥ pivot`——"
        "**枢轴从此就位**，后面递归只需要处理左右两段（这就是快排的分治点）。\n\n"
        "⚠️ 内层两个 `while` 的边界条件都带 `low < high`，不能省。"
        "省掉的话，`high--` 会一路减到越界。"
    ),
    input_format="第一行 `n`；第二行 `n` 个整数。",
    output_format="两行：划分后的序列；枢轴的 1-based 下标。",
    constraints_md="- 1 ≤ n ≤ 10⁵\n- |元素| ≤ 10⁹\n- 枢轴取第一个元素",
    inputs=[
        "6\n5 2 9 1 7 3\n",
        "1\n42\n",
        "5\n1 2 3 4 5\n",
        "5\n5 4 3 2 1\n",
        "7\n4 4 2 4 9 4 1\n",
    ],
    samples=3,
    oracle=_oracle_09,
    solution=r'''#include <cstdio>
#include <vector>
using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<long long> a(n);
    for (int i = 0; i < n; i++) scanf("%lld", &a[i]);

    long long pivot = a[0];
    int low = 0, high = n - 1;
    while (low < high) {
        while (low < high && a[high] >= pivot) high--;
        a[low] = a[high];
        while (low < high && a[low] <= pivot) low++;
        a[high] = a[low];
    }
    a[low] = pivot;

    for (int i = 0; i < n; i++) {
        printf("%lld", a[i]);
        putchar(i + 1 == n ? '\n' : ' ');
    }
    printf("%d\n", low + 1);
    return 0;
}
''',
    alt=r'''#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;
    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    // 另一条路：显式维护「坑位」变量 hole，而不是靠 low/high 兼作坑位。
    // 逻辑等价，但读起来「谁现在是坑」一目了然。
    long long pivot = a[0];
    int lo = 0, hi = n - 1;
    int hole = 0;                       // 当前空坑的下标
    while (lo < hi) {
        while (lo < hi && a[hi] >= pivot) hi--;
        a[hole] = a[hi];
        hole = hi;
        while (lo < hi && a[lo] <= pivot) lo++;
        if (lo < hi) {
            a[hole] = a[lo];
            hole = lo;
        }
    }
    a[hole] = pivot;

    for (int i = 0; i < n; i++) {
        if (i) cout << ' ';
        cout << a[i];
    }
    cout << '\n' << hole + 1 << '\n';
    return 0;
}
''',
)


def _oracle_10(text: str) -> str:
    """二叉排序树：数组模拟 lch/rch，中序 + 查找比较次数。"""
    d = text.split()
    n = int(d[0])
    vals = [int(v) for v in d[1:1 + n]]
    q = int(d[1 + n])
    qs = [int(v) for v in d[2 + n:2 + n + q]]

    val = [0] * (n + 2)
    lch = [0] * (n + 2)
    rch = [0] * (n + 2)
    cnt = 0

    def insert(x: int) -> None:
        nonlocal cnt
        if cnt == 0:
            cnt = 1
            val[1] = x
            return
        cur = 1
        while True:
            if x == val[cur]:
                return                      # 已存在，忽略
            if x < val[cur]:
                if lch[cur] == 0:
                    cnt += 1
                    val[cnt] = x
                    lch[cur] = cnt
                    return
                cur = lch[cur]
            else:
                if rch[cur] == 0:
                    cnt += 1
                    val[cnt] = x
                    rch[cur] = cnt
                    return
                cur = rch[cur]

    for x in vals:
        insert(x)

    ino: list[int] = []

    def walk(u: int) -> None:
        if u == 0:
            return
        walk(lch[u])
        ino.append(val[u])
        walk(rch[u])

    if cnt:
        walk(1)

    out = [" ".join(map(str, ino))]
    for x in qs:
        steps = 0
        cur = 1
        found = False
        while cur:
            steps += 1
            if x == val[cur]:
                found = True
                break
            cur = lch[cur] if x < val[cur] else rch[cur]
        out.append(str(steps) if found else "-1")
    return "\n".join(out) + "\n"


def _rand_bst_case() -> str:
    import random
    rnd = random.Random(20261025)
    n = 500
    vals = rnd.sample(range(-10 ** 6, 10 ** 6), n)
    qs = [rnd.choice(vals) for _ in range(200)] + [10 ** 9, -10 ** 9]
    return "%d\n%s\n%d\n%s\n" % (n, " ".join(map(str, vals)),
                                 len(qs), " ".join(map(str, qs)))


add(
    title="二叉排序树的插入与查找次数",
    section=SECTION,
    difficulty=3, score=12, tags=["编程精练", "二叉排序树", "BST", "查找"],
    statement_md=(
        "把 `n` 个整数**依次**插入一棵初始为空的二叉排序树（BST），"
        "**插入时遇到已存在的值则忽略**。然后回答 `q` 次查找。\n\n"
        "输出：\n"
        "1. 第一行：BST 的**中序遍历**（一定是升序，空格分隔；树为空时输出空行）\n"
        "2. 之后 `q` 行：每次查找**比较了多少个结点**（找到则输出比较次数，找不到输出 `-1`）\n\n"
        "比较次数的定义：从根开始，每拿一个结点与目标比一次就 +1；"
        "一路比较到命中。若走到空指针仍未命中，说明不存在。\n\n"
        "★ BST 的定义只有一句：**左子树上所有结点 < 根 < 右子树上所有结点**。"
        "所以插入/查找都是一条道走到黑——不需要回溯。\n\n"
        "★ 中序遍历天然升序，这是 BST 最实用的性质："
        "「判断一棵树是不是 BST」最稳的做法就是中序遍历看是否严格递增。\n\n"
        "⚠️ 比较次数就是**结点在树中的深度**。这意味着 BST 的效率完全取决于树高："
        "数据是随机的时候树高约 `O(log n)`，但**如果按升序插入，树会退化成一链**，"
        "查找变成 `O(n)`。这就是为什么工程上要用 AVL / 红黑树做平衡。"
    ),
    input_format="第一行 `n`；第二行 `n` 个整数（依次插入）；第三行 `q`；第四行 `q` 个查询值。",
    output_format="第一行中序遍历；之后 `q` 行每行一个比较次数（不存在为 `-1`）。",
    constraints_md="- 1 ≤ n ≤ 2000，1 ≤ q ≤ 2000\n- |值| ≤ 10⁹\n- 插入重复值时忽略",
    inputs=[
        "7\n50 30 70 20 40 60 80\n4\n50 20 80 100\n",
        "1\n5\n2\n5 6\n",
        "5\n10 10 5 15 5\n3\n5 10 15\n",
        _rand_bst_case(),
    ],
    samples=3,
    oracle=_oracle_10,
    solution=r'''#include <cstdio>
#include <vector>
using namespace std;

struct Node {
    int val;
    Node* lch;
    Node* rch;
    Node(int v) : val(v), lch(nullptr), rch(nullptr) {}
};

Node* insert(Node* root, int x) {
    if (!root) return new Node(x);
    if (x < root->val)      root->lch = insert(root->lch, x);
    else if (x > root->val) root->rch = insert(root->rch, x);
    // x == root->val 时忽略
    return root;
}

void inorder(Node* root, vector<int>& out) {
    if (!root) return;
    inorder(root->lch, out);
    out.push_back(root->val);
    inorder(root->rch, out);
}

void destroy(Node* root) {
    if (!root) return;
    destroy(root->lch);
    destroy(root->rch);
    delete root;
}

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    Node* root = nullptr;
    for (int i = 0; i < n; i++) {
        int x;
        scanf("%d", &x);
        root = insert(root, x);
    }

    vector<int> ino;
    inorder(root, ino);
    for (size_t i = 0; i < ino.size(); i++) {
        if (i) putchar(' ');
        printf("%d", ino[i]);
    }
    putchar('\n');

    int q;
    scanf("%d", &q);
    for (int i = 0; i < q; i++) {
        int x;
        scanf("%d", &x);
        Node* cur = root;
        int steps = 0;
        bool found = false;
        while (cur) {
            steps++;
            if (x == cur->val) { found = true; break; }
            cur = (x < cur->val) ? cur->lch : cur->rch;
        }
        printf("%d\n", found ? steps : -1);
    }

    destroy(root);
    return 0;
}
''',
    alt=r'''#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    // 另一条路：不用 new/指针，用数组下标模拟（lch/rch 存下标，0 表示空）。
    // 这样既不涉及内存管理，也更容易看出「退化成一链」是怎么回事。
    vector<int> val(n + 2, 0), lch(n + 2, 0), rch(n + 2, 0);
    int cnt = 0;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        if (cnt == 0) {
            cnt = 1;
            val[1] = x;
            continue;
        }
        int cur = 1;
        while (true) {
            if (x == val[cur]) break;
            if (x < val[cur]) {
                if (lch[cur] == 0) { cnt++; val[cnt] = x; lch[cur] = cnt; break; }
                cur = lch[cur];
            } else {
                if (rch[cur] == 0) { cnt++; val[cnt] = x; rch[cur] = cnt; break; }
                cur = rch[cur];
            }
        }
    }

    // 中序遍历用显式栈做迭代版
    vector<int> ino;
    if (cnt) {
        vector<int> st;
        int cur = 1;
        while (cur || !st.empty()) {
            while (cur) { st.push_back(cur); cur = lch[cur]; }
            cur = st.back();
            st.pop_back();
            ino.push_back(val[cur]);
            cur = rch[cur];
        }
    }
    for (size_t i = 0; i < ino.size(); i++) {
        if (i) cout << ' ';
        cout << ino[i];
    }
    cout << '\n';

    int q;
    cin >> q;
    for (int i = 0; i < q; i++) {
        int x;
        cin >> x;
        int cur = cnt ? 1 : 0;
        int steps = 0;
        bool found = false;
        while (cur) {
            steps++;
            if (x == val[cur]) { found = true; break; }
            cur = (x < val[cur]) ? lch[cur] : rch[cur];
        }
        cout << (found ? steps : -1) << '\n';
    }
    return 0;
}
''',
)


# --------------------------------------------------------------------- #
#  汇总
# --------------------------------------------------------------------- #

HEADER = '''# -*- coding: utf-8 -*-
"""C/C++ 编程精练题库 —— 自动生成，**不要手改本文件**。

生成器：tools/gen_ds_prog.py
分节：编程精练 · C/C++（10 题）

重生成：python tools/gen_ds_prog.py
"""

DS_PROG_PROBLEMS: list[dict] = '''

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
            "subject": "ds",
            "line": "cpp",
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
    ap = argparse.ArgumentParser(description="生成 C/C++ 编程精练题库")
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
