# -*- coding: utf-8 -*-
"""C++ 基础编程题 · 第 6 册：结构体与共用体（20）+ 链表（20）= 40 题。

对应教材第 06 讲「结构体」与第 09 讲「链表」（p230~251、p360~380）。这一册专练「数据组织」：
结构体是「把几个字段打包成一个整体」，共用体是「同一段内存的两种解释」，
链表是「用指针把散落的结点串起来」—— 三件事都绕不开「内存里到底放了什么」。

★ 共用体题**刻意避开字节序**：凡结果会随大小端变化的写法（写 int 读 char[4]）一律不写。
★ oracle 用 Python 的 dict/list 直接模拟，绝不复用 C++ 解的结果。
★ 每题 alt 换一条实现路径（数组模拟↔真指针链表、手写排序↔std::sort、迭代↔递归）。

重生成：python tools/gen_cpp_basic6.py
"""
from __future__ import annotations

import random
import string
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cpp_basic_kit import cases, cli, stmt          # noqa: E402

SEC_ST = "C++ 编程 · 结构体与共用体"
SEC_LK = "C++ 编程 · 链表"

PROBLEMS: list[dict] = []


def A(title, sec, d, st, inf, outf, con, inp, orc, sol, alt, tags):
    PROBLEMS.append(dict(title=title, section=sec, difficulty=d, statement_md=st,
                         input_format=inf, output_format=outf, constraints_md=con,
                         inputs=inp, oracle=orc, solution=sol, alt=alt, tags=tags))


# ------------------------------------------------------------------ #
#  数据助手
# ------------------------------------------------------------------ #
def rints(seed: int, n: int, lo: int = -50, hi: int = 50) -> list[int]:
    rng = random.Random(seed)
    return [rng.randint(lo, hi) for _ in range(n)]


def rword(seed: int, n: int = 4) -> str:
    rng = random.Random(seed)
    return "".join(rng.choice(string.ascii_lowercase) for _ in range(n))


def toks(t: str) -> list[int]:
    return [int(x) for x in t.split()]


def rows(t: str):
    return [ln.split() for ln in t.strip().splitlines()]


# ===================================================================== #
#  SEC_ST · 结构体与共用体（20 题）
# ===================================================================== #

def _sort_students(t: str) -> str:
    """按总分降序、同分按学号升序。"""
    rs = rows(t)
    n = int(rs[0][0])
    v = []
    for r in rs[1:1 + n]:
        sid = int(r[0])
        v.append((sid, sum(int(x) for x in r[1:4])))
    v.sort(key=lambda p: (-p[1], p[0]))
    return "".join("%d %d\n" % p for p in v)


def _best_student(t: str) -> str:
    rs = rows(t)
    n = int(rs[0][0])
    v = [(int(r[0]), int(r[1])) for r in rs[1:1 + n]]
    top = max(v, key=lambda p: p[1])
    return "%d %d\n" % top


def _avg_by_ptr(t: str) -> str:
    v = toks(t)[1:]
    return "%.2f\n" % (sum(v) / len(v))


def _date_cmp(t: str) -> str:
    v = toks(t)
    a, b = v[0:3], v[3:6]
    if a < b:
        return "%d %d %d\n" % tuple(a)
    if a > b:
        return "%d %d %d\n" % tuple(b)
    return "same\n"


def _time_diff(t: str) -> str:
    v = toks(t)
    s1 = v[0] * 3600 + v[1] * 60 + v[2]
    s2 = v[3] * 3600 + v[4] * 60 + v[5]
    return "%d\n" % abs(s1 - s2)


def _complex_calc(t: str) -> str:
    ln = [x.strip() for x in t.strip().splitlines()]
    op = ln[0]
    a = [int(x) for x in ln[1].split()]
    b = [int(x) for x in ln[2].split()]
    if op == "+":
        return "%d %d\n" % (a[0] + b[0], a[1] + b[1])
    return "%d %d\n" % (a[0] - b[0], a[1] - b[1])


def _union_sum(t: str) -> str:
    rs = rows(t)
    n = int(rs[0][0])
    si, sd = 0, 0.0
    for r in rs[1:1 + n]:
        if r[0] == "i":
            si += int(r[1])
        else:
            sd += float(r[1])
    return "%d %.2f\n" % (si, sd)


WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def _week_name(t: str) -> str:
    k = int(t.strip())
    return (WEEK[k - 1] if 1 <= k <= 7 else "Invalid") + "\n"


def _find_by_name(t: str) -> str:
    rs = rows(t)
    n = int(rs[0][0])
    q = rs[1 + n][0]
    for r in rs[1:1 + n]:
        if r[0] == q:
            return "%d\n" % int(r[1])
    return "-1\n"


def _manhattan(t: str) -> str:
    x1, y1, x2, y2 = toks(t)
    return "%d\n" % (abs(x1 - x2) + abs(y1 - y2))


def _rect(t: str) -> str:
    x1, y1, x2, y2 = toks(t)
    w, h = abs(x1 - x2), abs(y1 - y2)
    return "%d %d\n" % (w * h, 2 * (w + h))


def _grades(t: str) -> str:
    v = toks(t)[1:]
    out = []
    for x in v:
        out.append("A" if x >= 90 else "B" if x >= 80 else "C" if x >= 70
                   else "D" if x >= 60 else "F")
    return " ".join(out) + "\n"


def _dedup_by_id(t: str) -> str:
    rs = rows(t)
    n = int(rs[0][0])
    seen, out = set(), []
    for r in rs[1:1 + n]:
        sid = int(r[0])
        if sid not in seen:
            seen.add(sid)
            out.append("%d %d" % (sid, int(r[1])))
    return "".join(x + "\n" for x in out)


def _top3(t: str) -> str:
    rs = rows(t)
    n = int(rs[0][0])
    v = [(r[0], int(r[1])) for r in rs[1:1 + n]]
    v.sort(key=lambda p: -p[1])          # 同分保持原顺序（稳定排序）
    return "".join("%s %d\n" % p for p in v[:3])


def _reduce_frac(t: str) -> str:
    a, b = toks(t)
    g = __import__("math").gcd(abs(a), abs(b)) or 1
    a, b = a // g, b // g
    if b < 0:
        a, b = -a, -b
    return "%d %d\n" % (a, b)


def _del_by_id(t: str) -> str:
    rs = rows(t)
    n = int(rs[0][0])
    target = int(rs[1 + n][0])
    out = [r for r in rs[1:1 + n] if int(r[0]) != target]
    if not out:
        return "empty\n"
    return "".join("%s %s\n" % (r[0], r[1]) for r in out)


def _multi_sort(t: str) -> str:
    rs = rows(t)
    n = int(rs[0][0])
    v = [(int(r[0]), int(r[1]), r[2]) for r in rs[1:1 + n]]
    v.sort(key=lambda p: (p[0], -p[1], p[2]))   # 班级升序、分数降序、姓名升序
    return "".join("%d %d %s\n" % p for p in v)


A("【结构体】学生成绩排序", SEC_ST, 2,
  stmt("定义结构体存学号和 3 门课成绩，按**总分降序**排序，总分相同按**学号升序**。"
       "每行输出学号与总分。",
       ["结构体排序的关键是写对比较函数：先比总分（降序），总分相等再比学号（升序）",
        "`std::sort` 要求严格弱序，比较函数里不能写 `>=`",
        "总分用 `int` 就够：3 门课各 100 分"]),
  "第一行 `n`；之后 `n` 行，每行 `学号 成绩1 成绩2 成绩3`。",
  "`n` 行，每行 `学号 总分`。",
  "- 1 ≤ n ≤ 1000\n- 0 ≤ 成绩 ≤ 100\n- 学号唯一",
  lambda: cases("3\n1 90 80 70\n2 70 70 70\n3 100 100 100",
                "1\n5 60 60 60",
                "3\n2 80 80 80\n1 80 80 80\n3 79 79 79",
                "4\n10 100 0 0\n11 0 100 0\n12 0 0 100\n13 50 50 50",
                "%d\n%s" % (5, "\n".join(
                    "%d %d %d %d" % (i + 1, *(rints(200 + i, 3, 50, 100))) for i in range(5))),
                "2\n1 100 100 100\n2 100 100 100"),
  _sort_students,
  r'''#include <cstdio>
#include <algorithm>
struct Student {
    int id;
    int s[3];
    int total() const { return s[0] + s[1] + s[2]; }
};
bool cmp(const Student &a, const Student &b) {
    if (a.total() != b.total()) return a.total() > b.total();   // 总分降序
    return a.id < b.id;                                         // 同分学号升序
}
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static Student v[1005];
    for (int i = 0; i < n; i++)
        scanf("%d %d %d %d", &v[i].id, &v[i].s[0], &v[i].s[1], &v[i].s[2]);
    std::sort(v, v + n, cmp);
    for (int i = 0; i < n; i++) printf("%d %d\n", v[i].id, v[i].total());
    return 0;
}
''',
  r'''#include <cstdio>
#include <vector>
#include <algorithm>
struct Student { int id, total; };
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    std::vector<Student> v;
    for (int i = 0; i < n; i++) {
        int id, a, b, c;
        scanf("%d %d %d %d", &id, &a, &b, &c);
        v.push_back({id, a + b + c});           // 读的时候就先算好总分
    }
    std::sort(v.begin(), v.end(), [](const Student &x, const Student &y) {
        return x.total != y.total ? x.total > y.total : x.id < y.id;
    });
    for (auto &x : v) printf("%d %d\n", x.id, x.total);
    return 0;
}
''',
  ["结构体", "排序", "多关键字"])

A("【结构体】结构体数组求最高分", SEC_ST, 1,
  stmt("读入 `n` 个学生的学号和成绩，输出成绩最高的那个学生的学号与成绩"
       "（有并列时输出**最先出现**的）。",
       ["结构体数组的遍历和普通数组一样，只是取字段时写 `v[i].score`",
        "初值取第一个元素，别写 `max = 0`（成绩可能全 0）",
        "输出一行"]),
  "第一行 `n`；之后 `n` 行，每行 `学号 成绩`。",
  "一行：`学号 成绩`。",
  "- 1 ≤ n ≤ 1000\n- 0 ≤ 成绩 ≤ 100",
  lambda: cases("3\n1 90\n2 95\n3 88", "1\n7 0", "3\n1 60\n2 60\n3 60",
                "4\n10 100\n11 100\n12 99\n13 100",
                "%d\n%s" % (5, "\n".join("%d %d" % (i + 1, v)
                                         for i, v in enumerate(rints(210, 5, 0, 100)))),
                "2\n5 0\n6 0"),
  _best_student,
  r'''#include <cstdio>
struct Student { int id, score; };
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static Student v[1005];
    for (int i = 0; i < n; i++) scanf("%d %d", &v[i].id, &v[i].score);
    int k = 0;
    for (int i = 1; i < n; i++)
        if (v[i].score > v[k].score) k = i;   // 严格大于，取最先出现的
    printf("%d %d\n", v[k].id, v[k].score);
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
struct Student { int id, score; };
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static Student v[1005];
    for (int i = 0; i < n; i++) scanf("%d %d", &v[i].id, &v[i].score);
    Student *p = std::max_element(v, v + n, [](const Student &a, const Student &b) {
        return a.score < b.score;             // max_element 取第一个最大
    });
    printf("%d %d\n", p->id, p->score);       // 结构体指针用 ->
    return 0;
}
''',
  ["结构体", "最值", "指针"])

A("【结构体】结构体指针遍历求平均分", SEC_ST, 1,
  stmt("读入 `n` 个学生的成绩，用结构体指针遍历数组求平均分，输出保留 2 位小数。",
       ["`Student *p = v;` 之后 `p->score` 等价于 `(*p).score`",
        "指针遍历写 `for (Student *p = v; p < v + n; ++p)`",
        "平均值用 `double` 算"]),
  "第一行 `n`；之后 `n` 行，每行一个整数成绩。",
  "一行：平均分（2 位小数）。",
  "- 1 ≤ n ≤ 1000\n- 0 ≤ 成绩 ≤ 100",
  lambda: cases("3\n90\n80\n70", "1\n100", "4\n100\n100\n0\n0",
                "5\n60\n61\n62\n63\n64",
                "%d\n%s" % (6, "\n".join(str(x) for x in rints(220, 6, 0, 100))),
                "2\n59\n61"),
  _avg_by_ptr,
  r'''#include <cstdio>
struct Student { int score; };
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static Student v[1005];
    for (int i = 0; i < n; i++) scanf("%d", &v[i].score);
    long long s = 0;
    for (Student *p = v; p < v + n; ++p) s += p->score;   // 结构体指针遍历
    printf("%.2f\n", (double)s / n);
    return 0;
}
''',
  r'''#include <cstdio>
struct Student { int score; };
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static Student v[1005];
    for (int i = 0; i < n; i++) scanf("%d", &v[i].score);
    double s = 0;
    for (int i = 0; i < n; i++) s += (*&v[i]).score;
    printf("%.2f\n", s / n);
    return 0;
}
''',
  ["结构体", "指针", "平均分"])

A("【结构体】日期结构体比较先后", SEC_ST, 2,
  stmt("定义嵌套结构体表示日期（年、月、日），比较两个日期哪个更早，输出较早的那个"
       "（格式 `年 月 日`）；两者相同时输出 `same`。",
       ["年月日按「年优先」比较，不能只看日",
        "把三个字段按字典序比较：先年、再月、再日",
        "相同时只输出 `same`"]),
  "一行六个整数 `y1 m1 d1 y2 m2 d2`。",
  "一行：较早的日期，或 `same`。",
  "- 1 ≤ 年 ≤ 9999\n- 1 ≤ 月 ≤ 12\n- 1 ≤ 日 ≤ 31",
  lambda: cases("2024 1 1 2023 12 31", "2024 5 1 2024 5 1", "2024 5 1 2024 5 2",
                "2000 1 1 1999 12 31", "2024 12 31 2025 1 1", "2024 2 29 2024 3 1"),
  _date_cmp,
  r'''#include <cstdio>
struct Date { int y, m, d; };
bool earlier(const Date &a, const Date &b) {
    if (a.y != b.y) return a.y < b.y;
    if (a.m != b.m) return a.m < b.m;
    return a.d < b.d;
}
bool same(const Date &a, const Date &b) {
    return a.y == b.y && a.m == b.m && a.d == b.d;
}
int main() {
    Date a, b;
    if (scanf("%d %d %d %d %d %d", &a.y, &a.m, &a.d, &b.y, &b.m, &b.d) != 6) return 0;
    if (same(a, b)) { printf("same\n"); return 0; }
    Date &e = earlier(a, b) ? a : b;
    printf("%d %d %d\n", e.y, e.m, e.d);
    return 0;
}
''',
  r'''#include <cstdio>
struct Date { int y, m, d; };
int key(const Date &x) { return x.y * 10000 + x.m * 100 + x.d; }  // 压成一个整数比较
int main() {
    Date a, b;
    if (scanf("%d %d %d %d %d %d", &a.y, &a.m, &a.d, &b.y, &b.m, &b.d) != 6) return 0;
    int ka = key(a), kb = key(b);
    if (ka == kb) printf("same\n");
    else {
        Date &e = ka < kb ? a : b;
        printf("%d %d %d\n", e.y, e.m, e.d);
    }
    return 0;
}
''',
  ["结构体", "嵌套", "日期"])

A("【结构体】按值传参与按引用传参的差别", SEC_ST, 2,
  stmt("结构体作参数时，**按值传递**改不动原对象，**按引用传递**才能改。"
       "读入 `学号 成绩`，先调用按值的函数给它加 10 分，输出成绩；"
       "再调用按引用的函数加 10 分，输出成绩。两行输出。",
       ["结构体按值传参会把整个对象**复制**一份，函数里改的是副本",
        "按引用传参写 `Student &s`，改的就是原对象",
        "结构体一大，按值传递连性能都亏"]),
  "一行 `学号 成绩`。",
  "两行：按值调用后的成绩、按引用调用后的成绩。",
  "- 0 ≤ 成绩 ≤ 100",
  lambda: cases("1 60", "2 0", "3 100", "4 45", "5 90", "6 59"),
  lambda t: "%d\n%d\n" % (lambda v: (v[1], v[1] + 10))(toks(t)),
  r'''#include <cstdio>
struct Student { int id, score; };
void addByValue(Student s) { s.score += 10; }    // 改的是副本
void addByRef(Student &s)  { s.score += 10; }    // 改的是原对象
int main() {
    Student a;
    if (scanf("%d %d", &a.id, &a.score) != 2) return 0;
    addByValue(a);
    printf("%d\n", a.score);
    addByRef(a);
    printf("%d\n", a.score);
    return 0;
}
''',
  r'''#include <cstdio>
struct Student { int id, score; };
void addByPtr(Student *s) { s->score += 10; }    // 指针达到同样效果
int main() {
    Student a;
    if (scanf("%d %d", &a.id, &a.score) != 2) return 0;
    Student copy = a;
    addByPtr(&copy);
    printf("%d\n", a.score);                     // 原对象没变
    addByPtr(&a);
    printf("%d\n", a.score);
    return 0;
}
''',
  ["结构体", "值传递", "引用"])

A("【结构体】时间结构体求秒差", SEC_ST, 2,
  stmt("读入两个时刻（时、分、秒），输出它们相差多少秒（取绝对值）。",
       ["统一换算成「从 0 点起的秒数」再相减",
        "差可能为负，最后取绝对值",
        "输出一个整数"]),
  "一行六个整数 `h1 m1 s1 h2 m2 s2`。",
  "一行：相差的秒数。",
  "- 0 ≤ 时 ≤ 23\n- 0 ≤ 分, 秒 ≤ 59",
  lambda: cases("0 0 0 0 0 1", "12 0 0 12 0 0", "1 0 0 0 0 0", "23 59 59 0 0 0",
                "8 30 15 9 45 50", "5 0 0 4 59 59"),
  _time_diff,
  r'''#include <cstdio>
#include <cstdlib>
struct Time { int h, m, s; };
int toSec(const Time &t) { return t.h * 3600 + t.m * 60 + t.s; }
int main() {
    Time a, b;
    if (scanf("%d %d %d %d %d %d", &a.h, &a.m, &a.s, &b.h, &b.m, &b.s) != 6) return 0;
    printf("%d\n", abs(toSec(a) - toSec(b)));   // 记得取绝对值
    return 0;
}
''',
  r'''#include <cstdio>
struct Time { int h, m, s; };
int main() {
    Time a, b;
    if (scanf("%d %d %d %d %d %d", &a.h, &a.m, &a.s, &b.h, &b.m, &b.s) != 6) return 0;
    int x = a.h * 3600 + a.m * 60 + a.s;
    int y = b.h * 3600 + b.m * 60 + b.s;
    printf("%d\n", x > y ? x - y : y - x);
    return 0;
}
''',
  ["结构体", "时间", "换算"])

A("【结构体】复数结构体加减", SEC_ST, 2,
  stmt("用结构体表示复数（实部、虚部都是整数），实现加减法。第一行是运算符 `+` 或 `-`，"
       "之后两行各是一个复数 `实部 虚部`。输出运算结果的 `实部 虚部`。",
       ["复数加减就是实部与实部、虚部与虚部分别运算",
        "输出不带 `i`，就是两个整数",
        "运算符是字符串，用 `%s` 读"]),
  "第一行 `+` 或 `-`；第二行 `a1 b1`；第三行 `a2 b2`。",
  "一行：结果的 `实部 虚部`。",
  "- |实部|, |虚部| ≤ 10⁶",
  lambda: cases("+\n1 2\n3 4", "-\n1 2\n3 4", "+\n0 0\n0 0", "-\n-1 -2\n-3 -4",
                "+\n100 -200\n-50 200", "-\n5 5\n5 5"),
  _complex_calc,
  r'''#include <cstdio>
#include <cstring>
struct Complex { int re, im; };
Complex add(const Complex &x, const Complex &y) { return {x.re + y.re, x.im + y.im}; }
Complex sub(const Complex &x, const Complex &y) { return {x.re - y.re, x.im - y.im}; }
int main() {
    char op[4];
    Complex a, b;
    if (scanf("%3s", op) != 1) return 0;
    if (scanf("%d %d", &a.re, &a.im) != 2) return 0;
    if (scanf("%d %d", &b.re, &b.im) != 2) return 0;
    Complex r = (op[0] == '+') ? add(a, b) : sub(a, b);
    printf("%d %d\n", r.re, r.im);
    return 0;
}
''',
  r'''#include <cstdio>
struct Complex { int re, im; };
int main() {
    char op[4];
    Complex a, b;
    if (scanf("%3s", op) != 1) return 0;
    if (scanf("%d %d", &a.re, &a.im) != 2) return 0;
    if (scanf("%d %d", &b.re, &b.im) != 2) return 0;
    int sign = (op[0] == '+') ? 1 : -1;          // 用符号统一处理
    printf("%d %d\n", a.re + sign * b.re, a.im + sign * b.im);
    return 0;
}
''',
  ["结构体", "复数", "函数返回结构体"])

A("【结构体】结构体数组求总分与平均分", SEC_ST, 1,
  stmt("读入 `n` 个学生的成绩，输出总分与平均分（平均分保留 2 位小数），一行，空格分隔。",
       ["总分用 `long long`，n 到 10⁵ 时总和能到 10⁷",
        "平均分是 `(double)total / n`",
        "输出一行两个数"]),
  "第一行 `n`；之后 `n` 行，每行一个整数成绩。",
  "一行：`总分 平均分`。",
  "- 1 ≤ n ≤ 1000\n- 0 ≤ 成绩 ≤ 100",
  lambda: cases("3\n90\n80\n70", "1\n100", "4\n0\n0\n0\n0", "2\n59\n61",
                "%d\n%s" % (5, "\n".join(str(x) for x in rints(230, 5, 0, 100))),
                "%d\n%s" % (7, "\n".join(str(x) for x in rints(231, 7, 60, 100)))),
  lambda t: "%d %.2f\n" % (lambda v: (sum(v), sum(v) / len(v)))(toks(t)[1:]),
  r'''#include <cstdio>
struct Student { int score; };
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static Student v[1005];
    long long s = 0;
    for (int i = 0; i < n; i++) { scanf("%d", &v[i].score); s += v[i].score; }
    printf("%lld %.2f\n", s, (double)s / n);
    return 0;
}
''',
  r'''#include <cstdio>
struct Student { int score; };
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static Student v[1005];
    double s = 0;
    for (int i = 0; i < n; i++) { scanf("%d", &v[i].score); s += v[i].score; }
    printf("%.0f %.2f\n", s, s / n);      // 总和是整数，用 %.0f 输出
    return 0;
}
''',
  ["结构体", "统计"])

A("【共用体】用 union 存整数或小数并求和", SEC_ST, 3,
  stmt("一条记录要么是整数要么是小数，类型由标记位决定。用 `union { int i; double d; }` 存放，"
       "读入 `n` 条记录（`i 5` 或 `d 2.5`），输出整数之和与小数之和（小数保留 2 位）。",
       ["共用体的所有成员**共享同一段内存**，同一时刻只有一种解释是有效的",
        "所以必须另外存一个「类型标记」，否则不知道当前该按哪个成员读",
        "共用体的大小等于最大成员的大小（`double` 是 8 字节）"]),
  "第一行 `n`；之后 `n` 行，每行 `类型标记 值`（`i` 或 `d`）。",
  "一行：`整数和 小数和`（小数保留 2 位）。",
  "- 1 ≤ n ≤ 1000\n- |整数| ≤ 10⁶\n- |小数| ≤ 10⁶",
  lambda: cases("3\ni 5\nd 2.5\ni 10", "1\ni 0", "1\nd 0.5",
                "4\nd 1.25\nd 2.25\nd 3.5\nd 0.0",
                "2\ni -3\ni 3", "5\nd 1.5\ni 2\nd 2.5\ni -2\nd 0.25"),
  _union_sum,
  r'''#include <cstdio>
union Number {
    int i;
    double d;
};
struct Record {
    char kind;              // 类型标记，和 union 一起组成「带标签的联合」
    Number num;
};
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    long long si = 0;
    double sd = 0;
    for (int k = 0; k < n; k++) {
        Record r;
        char buf[8];
        scanf("%7s", buf);
        r.kind = buf[0];
        if (r.kind == 'i') { scanf("%d", &r.num.i); si += r.num.i; }
        else { scanf("%lf", &r.num.d); sd += r.num.d; }
    }
    printf("%lld %.2f\n", si, sd);
    return 0;
}
''',
  r'''#include <cstdio>
union Number { int i; double d; };
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    long long si = 0;
    double sd = 0;
    for (int k = 0; k < n; k++) {
        char kind;
        Number u;
        scanf(" %c", &kind);
        if (kind == 'i') { scanf("%d", &u.i); si += u.i; }
        else { scanf("%lf", &u.d); sd += u.d; }
    }
    printf("%lld %.2f\n", si, sd);
    return 0;
}
''',
  ["共用体", "union", "类型标记"])

A("【枚举】用 enum 输出星期英文名", SEC_ST, 1,
  stmt("用 `enum Week { MON = 1, TUE, WED, THU, FRI, SAT, SUN };` 读入 `1`~`7`，"
       "输出对应的英文名（`Monday`…`Sunday`）；超出范围输出 `Invalid`。",
       ["枚举的底层就是整数，`MON = 1` 之后 `TUE` 自动是 2",
        "数组下标从 0 开始，枚举从 1 开始，取值时要 `-1`",
        "英文名注意大小写"]),
  "一行一个整数。",
  "一行：英文名或 `Invalid`。",
  "- -10 ≤ 输入 ≤ 20",
  lambda: cases("1", "7", "0", "8", "3", "-1"),
  _week_name,
  r'''#include <cstdio>
enum Week { MON = 1, TUE, WED, THU, FRI, SAT, SUN };
const char *name[] = {"", "Monday", "Tuesday", "Wednesday", "Thursday",
                      "Friday", "Saturday", "Sunday"};
int main() {
    int k;
    if (scanf("%d", &k) != 1) return 0;
    if (k < MON || k > SUN) { printf("Invalid\n"); return 0; }
    printf("%s\n", name[k]);
    return 0;
}
''',
  r'''#include <cstdio>
enum Week { MON = 1, TUE, WED, THU, FRI, SAT, SUN };
int main() {
    int k;
    if (scanf("%d", &k) != 1) return 0;
    switch (k) {                    // switch 配枚举更直观
        case MON: printf("Monday\n"); break;
        case TUE: printf("Tuesday\n"); break;
        case WED: printf("Wednesday\n"); break;
        case THU: printf("Thursday\n"); break;
        case FRI: printf("Friday\n"); break;
        case SAT: printf("Saturday\n"); break;
        case SUN: printf("Sunday\n"); break;
        default:  printf("Invalid\n");
    }
    return 0;
}
''',
  ["枚举", "enum", "switch"])

A("【结构体】按姓名查找成绩", SEC_ST, 2,
    stmt("读入 `n` 个学生的姓名与成绩，再读一个姓名，输出他的成绩；查不到输出 `-1`。",
         ["姓名用 `char[32]` 存，比较用 `strcmp`（或用 `std::string` 的 `==`）",
          "找到就立刻返回，别继续覆盖",
          "输出一个整数"]),
    "第一行 `n`；之后 `n` 行，每行 `姓名 成绩`；最后一行一个姓名。",
    "一行：成绩或 `-1`。",
    "- 1 ≤ n ≤ 1000\n- 姓名只含小写字母，长度 ≤ 20",
    lambda: cases("3\nalice 90\nbob 85\ncarol 70\nalice",
                  "1\nzoe 100\nzoe",
                  "2\naa 1\nbb 2\ncc",
                  "%d\n%s\n%s" % (5, "\n".join(
                      "%s %d" % (rword(240 + i, 4), v)
                      for i, v in enumerate(rints(240, 5, 0, 100))),
                      rword(240 + 2, 4)),
                  "3\nx 60\ny 70\nz 80\nw",
                  "1\nonly 0\nonly"),
    _find_by_name,
    r'''#include <cstdio>
#include <cstring>
struct Student {
    char name[32];
    int score;
};
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static Student v[1005];
    for (int i = 0; i < n; i++) scanf("%31s %d", v[i].name, &v[i].score);
    char q[32];
    if (scanf("%31s", q) != 1) return 0;
    for (int i = 0; i < n; i++)
        if (strcmp(v[i].name, q) == 0) { printf("%d\n", v[i].score); return 0; }
    printf("-1\n");
    return 0;
}
''',
    r'''#include <cstdio>
#include <iostream>
#include <string>
#include <vector>
struct Student { std::string name; int score; };
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    std::vector<Student> v(n);
    for (int i = 0; i < n; i++) std::cin >> v[i].name >> v[i].score;
    std::string q;
    if (!(std::cin >> q)) return 0;
    for (auto &s : v) if (s.name == q) { printf("%d\n", s.score); return 0; }
    printf("-1\n");
    return 0;
}
''',
    ["结构体", "查找", "strcmp"])

A("【结构体】点结构体求曼哈顿距离", SEC_ST, 1,
  stmt("用结构体表示平面上的点，读入两个点的坐标，输出它们的曼哈顿距离 `|x1-x2| + |y1-y2|`。",
       ["曼哈顿距离是「横着走 + 竖着走」的总步数，不是直线距离",
        "`abs` 在 `<cstdlib>` 里，注意参数是 `int`",
        "输出一个整数"]),
  "一行四个整数 `x1 y1 x2 y2`。",
  "一行：曼哈顿距离。",
  "- |坐标| ≤ 10⁶",
  lambda: cases("0 0 3 4", "0 0 0 0", "-1 -1 2 2", "100 -100 -100 100",
                "5 5 5 6", "-3 7 4 -2"),
  _manhattan,
  r'''#include <cstdio>
#include <cstdlib>
struct Point { int x, y; };
int manhattan(const Point &a, const Point &b) {
    return abs(a.x - b.x) + abs(a.y - b.y);
}
int main() {
    Point a, b;
    if (scanf("%d %d %d %d", &a.x, &a.y, &b.x, &b.y) != 4) return 0;
    printf("%d\n", manhattan(a, b));
    return 0;
}
''',
  r'''#include <cstdio>
struct Point { int x, y; };
int main() {
    Point a, b;
    if (scanf("%d %d %d %d", &a.x, &a.y, &b.x, &b.y) != 4) return 0;
    int dx = a.x - b.x, dy = a.y - b.y;
    if (dx < 0) dx = -dx;              // 手写绝对值
    if (dy < 0) dy = -dy;
    printf("%d\n", dx + dy);
    return 0;
}
''',
  ["结构体", "几何", "距离"])

A("【结构体】矩形结构体求面积与周长", SEC_ST, 2,
  stmt("用两个对角点表示一个矩形，读入两个点的坐标，输出矩形的面积与周长（一行，空格分隔）。",
       ["边长是两点坐标差的**绝对值**，输入的第二个点不一定在右上方",
        "面积为 0 也要照常输出（退化矩形）",
        "输出一行两个整数"]),
  "一行四个整数 `x1 y1 x2 y2`。",
  "一行：`面积 周长`。",
  "- |坐标| ≤ 10⁶",
  lambda: cases("0 0 3 4", "3 4 0 0", "0 0 0 0", "-2 -3 2 3", "5 5 5 10", "1 1 2 2"),
  _rect,
  r'''#include <cstdio>
#include <cstdlib>
struct Point { int x, y; };
struct Rect { Point a, b; };                 // 嵌套结构体
int width(const Rect &r)  { return abs(r.a.x - r.b.x); }
int height(const Rect &r) { return abs(r.a.y - r.b.y); }
int main() {
    Rect r;
    if (scanf("%d %d %d %d", &r.a.x, &r.a.y, &r.b.x, &r.b.y) != 4) return 0;
    int w = width(r), h = height(r);
    printf("%d %d\n", w * h, 2 * (w + h));
    return 0;
}
''',
  r'''#include <cstdio>
struct Point { int x, y; };
struct Rect { Point a, b; };
int main() {
    Rect r;
    if (scanf("%d %d %d %d", &r.a.x, &r.a.y, &r.b.x, &r.b.y) != 4) return 0;
    int w = r.a.x > r.b.x ? r.a.x - r.b.x : r.b.x - r.a.x;
    int h = r.a.y > r.b.y ? r.a.y - r.b.y : r.b.y - r.a.y;
    printf("%d %d\n", w * h, 2 * (w + h));
    return 0;
}
''',
  ["结构体", "嵌套", "矩形"])

A("【结构体】按成绩分档输出等级", SEC_ST, 2,
  stmt("读入 `n` 个成绩，按 `A(≥90) B(≥80) C(≥70) D(≥60) F(<60)` 转成等级，"
       "一行输出，空格分隔。",
       ["分档判断从高到低写，或用「除以 10」查表",
        "100 分是 A，60 分是 D，59 分是 F",
        "输出 `n` 个字母"]),
  "第一行 `n`；之后 `n` 行，每行一个整数成绩。",
  "一行：`n` 个等级字母。",
  "- 1 ≤ n ≤ 1000\n- 0 ≤ 成绩 ≤ 100",
  lambda: cases("5\n90\n80\n70\n60\n59", "1\n100", "1\n0", "3\n89\n79\n69",
                "%d\n%s" % (6, "\n".join(str(x) for x in rints(250, 6, 0, 100))),
                "4\n100\n99\n60\n59"),
  _grades,
  r'''#include <cstdio>
struct Student { int score; char grade; };
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static Student v[1005];
    for (int i = 0; i < n; i++) {
        scanf("%d", &v[i].score);
        int s = v[i].score;
        v[i].grade = s >= 90 ? 'A' : s >= 80 ? 'B' : s >= 70 ? 'C' : s >= 60 ? 'D' : 'F';
    }
    for (int i = 0; i < n; i++) printf("%c%c", v[i].grade, i + 1 == n ? '\n' : ' ');
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    const char *tab = "FFFFFFDCBAA";      // 下标 = 分数 / 10（100 落在最后一位 A）
    for (int i = 0; i < n; i++) {
        int s; scanf("%d", &s);
        char g = (s < 60) ? 'F' : tab[s / 10];
        printf("%c%c", g, i + 1 == n ? '\n' : ' ');
    }
    return 0;
}
''',
  ["结构体", "分档", "查表"])

A("【结构体】按学号去重保序", SEC_ST, 2,
  stmt("读入 `n` 条学生记录（学号可能重复），只保留每个学号**第一次**出现的那条，"
       "按原顺序输出 `学号 成绩`。",
       ["用一个「已出现」标记数组（学号范围小）或 `set`",
        "去重但**不打乱顺序** —— 所以不能先排序",
        "每行一条记录"]),
  "第一行 `n`；之后 `n` 行，每行 `学号 成绩`。",
  "若干行：去重后的记录。",
  "- 1 ≤ n ≤ 1000\n- 1 ≤ 学号 ≤ 1000",
  lambda: cases("4\n1 90\n2 85\n1 70\n3 60", "1\n5 50", "3\n1 1\n1 2\n1 3",
                "5\n2 10\n1 20\n2 30\n3 40\n1 50",
                "%d\n%s" % (6, "\n".join("%d %d" % (v % 3 + 1, w) for v, w in
                                         zip(rints(260, 6, 0, 5), rints(261, 6, 0, 100)))),
                "2\n7 80\n7 90"),
  _dedup_by_id,
  r'''#include <cstdio>
struct Student { int id, score; };
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static bool seen[1005];
    for (int i = 0; i < n; i++) {
        Student s;
        scanf("%d %d", &s.id, &s.score);
        if (seen[s.id]) continue;        // 出现过就丢掉
        seen[s.id] = true;
        printf("%d %d\n", s.id, s.score);
    }
    return 0;
}
''',
  r'''#include <cstdio>
#include <set>
struct Student { int id, score; };
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static Student v[1005];
    std::set<int> seen;
    for (int i = 0; i < n; i++) scanf("%d %d", &v[i].id, &v[i].score);
    for (int i = 0; i < n; i++)
        if (seen.insert(v[i].id).second)      // insert 返回是否新插入
            printf("%d %d\n", v[i].id, v[i].score);
    return 0;
}
''',
  ["结构体", "去重", "保序"])

A("【结构体】排序输出前三名", SEC_ST, 2,
  stmt("读入 `n` 个学生的姓名与成绩，按成绩**降序**输出前 3 名（不足 3 人就有几个输出几个）。"
       "成绩相同时保持输入顺序。",
       ["同分保持原顺序 —— 用 `std::stable_sort` 或比较函数里只比分数",
        "`std::sort` 不保证稳定，同分时顺序可能乱",
        "每行 `姓名 成绩`"]),
  "第一行 `n`；之后 `n` 行，每行 `姓名 成绩`。",
  "最多 3 行：`姓名 成绩`。",
  "- 1 ≤ n ≤ 1000\n- 0 ≤ 成绩 ≤ 100\n- 姓名只含小写字母",
  lambda: cases("4\nalice 90\nbob 85\ncarol 95\ndan 80",
                "2\nx 70\ny 60",
                "1\nonly 100",
                "3\na 80\nb 80\nc 80",
                "%d\n%s" % (6, "\n".join(
                    "%s %d" % (rword(270 + i, 3), v)
                    for i, v in enumerate(rints(270, 6, 60, 100)))),
                "3\na 50\nb 90\nc 70"),
  _top3,
  r'''#include <cstdio>
#include <algorithm>
struct Student {
    char name[32];
    int score;
};
bool cmp(const Student &a, const Student &b) { return a.score > b.score; }
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static Student v[1005];
    for (int i = 0; i < n; i++) scanf("%31s %d", v[i].name, &v[i].score);
    std::stable_sort(v, v + n, cmp);        // 稳定排序，同分保原序
    int k = n < 3 ? n : 3;
    for (int i = 0; i < k; i++) printf("%s %d\n", v[i].name, v[i].score);
    return 0;
}
''',
  r'''#include <cstdio>
#include <algorithm>
struct Student { char name[32]; int score; int idx; };
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static Student v[1005];
    for (int i = 0; i < n; i++) { scanf("%31s %d", v[i].name, &v[i].score); v[i].idx = i; }
    std::sort(v, v + n, [](const Student &a, const Student &b) {
        if (a.score != b.score) return a.score > b.score;
        return a.idx < b.idx;                  // 用原始下标把稳定性「补」回来
    });
    int k = n < 3 ? n : 3;
    for (int i = 0; i < k; i++) printf("%s %d\n", v[i].name, v[i].score);
    return 0;
}
''',
  ["结构体", "稳定排序", "topK"])

A("【结构体】分数结构体约分", SEC_ST, 2,
  stmt("用结构体表示分数（分子、分母），读入一个分数，输出约分后的形式（分母恒为正）。"
       "分子为 0 时输出 `0 1`。",
       ["先求 `gcd(|分子|, |分母|)` 再同除",
        "分母为负时，分子分母同时取反，把负号放到分子上",
        "输出两个整数"]),
  "一行两个整数 `分子 分母`。",
  "一行：约分后的 `分子 分母`。",
  "- |分子| ≤ 10⁶\n- 1 ≤ |分母| ≤ 10⁶\n- 分母不为 0",
  lambda: cases("6 8", "0 5", "-6 8", "6 -8", "100 1", "-5 -10"),
  _reduce_frac,
  r'''#include <cstdio>
#include <cstdlib>
struct Fraction { int num, den; };
int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }
Fraction reduce(Fraction f) {
    if (f.num == 0) return {0, 1};
    int g = gcd(abs(f.num), abs(f.den));
    f.num /= g; f.den /= g;
    if (f.den < 0) { f.num = -f.num; f.den = -f.den; }   // 分母恒正
    return f;
}
int main() {
    Fraction f;
    if (scanf("%d %d", &f.num, &f.den) != 2) return 0;
    Fraction r = reduce(f);
    printf("%d %d\n", r.num, r.den);
    return 0;
}
''',
  r'''#include <cstdio>
#include <numeric>
#include <cstdlib>
struct Fraction { int num, den; };
int main() {
    Fraction f;
    if (scanf("%d %d", &f.num, &f.den) != 2) return 0;
    if (f.num == 0) { printf("0 1\n"); return 0; }
    int g = std::gcd(abs(f.num), abs(f.den));
    int a = f.num / g, b = f.den / g;
    if (b < 0) { a = -a; b = -b; }
    printf("%d %d\n", a, b);
    return 0;
}
''',
  ["结构体", "约分", "gcd"])

A("【结构体】删除指定学号并输出剩余", SEC_ST, 2,
  stmt("读入 `n` 条记录和一个学号，删掉该学号的所有记录，输出剩余记录；"
       "一条不剩时输出 `empty`。",
       ["删除就是「不输出」—— 顺序扫描时跳过目标即可",
        "删完可能为空，要单独判断",
        "每行 `学号 成绩`"]),
  "第一行 `n`；之后 `n` 行，每行 `学号 成绩`；最后一行一个学号。",
  "若干行剩余记录，或 `empty`。",
  "- 1 ≤ n ≤ 1000\n- 1 ≤ 学号 ≤ 1000",
  lambda: cases("3\n1 90\n2 85\n3 70\n2", "1\n1 90\n1", "2\n1 90\n2 80\n9",
                "4\n1 10\n2 20\n1 30\n3 40\n1",
                "%d\n%s\n%d" % (5, "\n".join("%d %d" % (i % 3 + 1, v) for i, v in
                                             enumerate(rints(280, 5, 0, 100))), 1),
                "2\n5 50\n6 60\n5"),
  _del_by_id,
  r'''#include <cstdio>
struct Student { int id, score; };
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static Student v[1005];
    for (int i = 0; i < n; i++) scanf("%d %d", &v[i].id, &v[i].score);
    int target;
    if (scanf("%d", &target) != 1) return 0;
    int c = 0;
    for (int i = 0; i < n; i++) {
        if (v[i].id == target) continue;      // 跳过要删的
        printf("%d %d\n", v[i].id, v[i].score);
        c++;
    }
    if (c == 0) printf("empty\n");
    return 0;
}
''',
  r'''#include <cstdio>
struct Student { int id, score; };
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static Student v[1005];
    for (int i = 0; i < n; i++) scanf("%d %d", &v[i].id, &v[i].score);
    int target;
    if (scanf("%d", &target) != 1) return 0;
    int k = 0;
    for (int i = 0; i < n; i++) if (v[i].id != target) v[k++] = v[i];   // 原地压缩
    if (k == 0) { printf("empty\n"); return 0; }
    for (int i = 0; i < k; i++) printf("%d %d\n", v[i].id, v[i].score);
    return 0;
}
''',
  ["结构体", "删除", "压缩"])

A("【共用体】union 成员写入互相覆盖", SEC_ST, 3,
  stmt("共用体的成员共享同一段内存：写 `a` 再写 `b`，`a` 的值就被覆盖了。"
       "读入两个整数 `x y`，依次给 `u.a`、`u.b` 赋值，输出此时 `u.a` 与 `u.b` 的值。",
       ["`union { int a; int b; }` 里 `a` 和 `b` 是**同一块 4 字节**",
        "写 `u.b = y` 之后，`u.a` 读出来也是 `y` —— 它们物理上是同一个位置",
        "输出一行两个整数，必然相同"]),
  "一行两个整数 `x y`。",
  "一行：`u.a u.b`。",
  "- |x|, |y| ≤ 10⁶",
  lambda: cases("1 2", "0 0", "-5 5", "100 -100", "7 7", "123456 -654321"),
  lambda t: "%d %d\n" % (lambda v: (v[1], v[1]))(toks(t)),
  r'''#include <cstdio>
union Pair {
    int a;
    int b;          // 和 a 共用同一段内存
};
int main() {
    int x, y;
    if (scanf("%d %d", &x, &y) != 2) return 0;
    Pair u;
    u.a = x;        // 先写 a
    u.b = y;        // 再写 b —— a 被覆盖
    printf("%d %d\n", u.a, u.b);
    return 0;
}
''',
  r'''#include <cstdio>
union Pair { int a; int b; };
int main() {
    int x, y;
    if (scanf("%d %d", &x, &y) != 2) return 0;
    Pair u;
    u.a = x;
    u.b = y;
    printf("%d %d\n", u.a, u.b);   // 两者都是 y
    (void)x;
    return 0;
}
''',
  ["共用体", "union", "内存共享"])

A("【结构体】结构体多关键字排序", SEC_ST, 3,
  stmt("读入 `n` 个学生（班级、分数、姓名），先按**班级升序**，同班按**分数降序**，"
       "再同分按姓名升序。输出排序结果（每行 `班级 分数 姓名`）。",
       ["比较函数里三个关键字依次判断，前一个相等才看下一个",
        "班级升序、分数降序、姓名升序，方向不同，别写反",
        "姓名比较用 `strcmp`"]),
  "第一行 `n`；之后 `n` 行，每行 `班级 分数 姓名`。",
  "`n` 行：`班级 分数 姓名`。",
  "- 1 ≤ n ≤ 1000\n- 1 ≤ 班级 ≤ 10\n- 0 ≤ 分数 ≤ 100",
  lambda: cases("3\n2 90 bob\n1 80 alice\n2 95 carol",
                "1\n1 60 solo",
                "3\n1 80 b\n1 80 a\n1 90 c",
                "4\n2 50 x\n1 50 y\n2 50 a\n1 50 b",
                "%d\n%s" % (5, "\n".join(
                    "%d %d %s" % (v % 2 + 1, w, rword(290 + i, 3))
                    for i, (v, w) in enumerate(zip(rints(290, 5, 0, 1),
                                                   rints(291, 5, 60, 100))))),
                "2\n1 100 z\n1 100 a"),
  _multi_sort,
  r'''#include <cstdio>
#include <cstring>
#include <algorithm>
struct Student {
    int cls, score;
    char name[32];
};
bool cmp(const Student &a, const Student &b) {
    if (a.cls != b.cls) return a.cls < b.cls;          // 班级升序
    if (a.score != b.score) return a.score > b.score;  // 分数降序
    return strcmp(a.name, b.name) < 0;                 // 姓名升序
}
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static Student v[1005];
    for (int i = 0; i < n; i++) scanf("%d %d %31s", &v[i].cls, &v[i].score, v[i].name);
    std::sort(v, v + n, cmp);
    for (int i = 0; i < n; i++) printf("%d %d %s\n", v[i].cls, v[i].score, v[i].name);
    return 0;
}
''',
  r'''#include <cstdio>
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <tuple>
struct Student { int cls, score; std::string name; };
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    std::vector<Student> v(n);
    for (int i = 0; i < n; i++) std::cin >> v[i].cls >> v[i].score >> v[i].name;
    std::sort(v.begin(), v.end(), [](const Student &a, const Student &b) {
        return std::make_tuple(a.cls, -a.score, a.name)
             < std::make_tuple(b.cls, -b.score, b.name);   // tuple 字典序一次比完
    });
    for (auto &s : v) printf("%d %d %s\n", s.cls, s.score, s.name.c_str());
    return 0;
}
''',
  ["结构体", "多关键字", "tuple"])

# ===================================================================== #
#  SEC_LK · 链表（20 题）
# ===================================================================== #

def _lst(t: str) -> list[int]:
    return toks(t)[1:]


def _join_out(v, empty_msg=False) -> str:
    if not v:
        return "empty\n" if empty_msg else "\n"
    return " ".join(str(x) for x in v) + "\n"


def _rev(t: str) -> str:
    return _join_out(list(reversed(_lst(t))))


def _len_sum(t: str) -> str:
    v = _lst(t)
    return "%d %d\n" % (len(v), sum(v))


def _first_pos(t: str) -> str:
    tok = toks(t)
    n, x = tok[0], tok[1]
    v = tok[2:2 + n]
    return "%d\n" % (v.index(x) + 1 if x in v else -1)


def _insert_at(t: str) -> str:
    tok = toks(t)
    n, k, x = tok[0], tok[1], tok[2]
    v = tok[3:3 + n]
    if k <= 0:
        v = [x] + v
    elif k > n:
        v = v + [x]
    else:
        v = v[:k - 1] + [x] + v[k - 1:]
    return _join_out(v)


def _del_at(t: str) -> str:
    tok = toks(t)
    n, k = tok[0], tok[1]
    v = tok[2:2 + n]
    if 1 <= k <= n:
        v = v[:k - 1] + v[k:]
    return _join_out(v, empty_msg=True)


def _merge(t: str) -> str:
    tok = toks(t)
    n = tok[0]
    a = tok[1:1 + n]
    m = tok[1 + n]
    b = tok[2 + n:2 + n + m]
    return _join_out(sorted(a + b))


def _dedup_list(t: str) -> str:
    seen, out = set(), []
    for x in _lst(t):
        if x not in seen:
            seen.add(x)
            out.append(x)
    return _join_out(out)


def _middle(t: str) -> str:
    v = _lst(t)
    return "%d\n" % v[(len(v) - 1) // 2]


def _joseph(t: str) -> str:
    n, m = toks(t)
    alive = list(range(1, n + 1))
    out, i = [], 0
    while alive:
        i = (i + m - 1) % len(alive)
        out.append(alive.pop(i))
    return " ".join(str(x) for x in out) + "\n"


def _del_value(t: str) -> str:
    tok = toks(t)
    n, x = tok[0], tok[1]
    v = [y for y in tok[2:2 + n] if y != x]
    return _join_out(v, empty_msg=True)


def _max_pos(t: str) -> str:
    v = _lst(t)
    return "%d %d\n" % (max(v), v.index(max(v)) + 1)


def _increasing(t: str) -> str:
    v = _lst(t)
    ok = all(v[i] < v[i + 1] for i in range(len(v) - 1))
    return "YES\n" if ok else "NO\n"


def _partition(t: str) -> str:
    tok = toks(t)
    n, x = tok[0], tok[1]
    v = tok[2:2 + n]
    return _join_out([y for y in v if y < x] + [y for y in v if y >= x])


def _union_list(t: str) -> str:
    tok = toks(t)
    n = tok[0]
    a = tok[1:1 + n]
    m = tok[1 + n]
    b = tok[2 + n:2 + n + m]
    return _join_out(sorted(set(a) | set(b)))


def _insert_sort(t: str) -> str:
    return _join_out(sorted(_lst(t)))


def _odd_even(t: str) -> str:
    v = _lst(t)
    return _join_out(v[0::2] + v[1::2])


def _big_add(t: str) -> str:
    a, b = t.split()
    return "%d\n" % (int(a) + int(b))


def _del_kth_last(t: str) -> str:
    tok = toks(t)
    n, k = tok[0], tok[1]
    v = tok[2:2 + n]
    idx = n - k
    if 0 <= idx < n:
        v = v[:idx] + v[idx + 1:]
    return _join_out(v, empty_msg=True)


A("【链表】尾插法建表并顺序输出", SEC_LK, 1,
  stmt("用**尾插法**建单链表（每次把新结点接到表尾），读入 `n` 和 `n` 个整数，"
       "从头到尾输出链表。",
       ["尾插要维护一个 `tail` 指针，否则每次都要从头找到尾，变成 O(n²)",
        "第一个结点要单独处理：`head = tail = new Node(v)`",
        "输出一行，空格分隔"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：链表的顺序输出。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases("5\n1 2 3 4 5", "1\n7", "3\n-1 -2 -3",
                "%d\n%s" % (8, " ".join(str(x) for x in rints(300, 8))),
                "4\n0 0 0 0", "%d\n%s" % (6, " ".join(str(x) for x in rints(301, 6, -100, 100)))),
  lambda t: _join_out(_lst(t)),
  r'''#include <cstdio>
struct Node {
    int val;
    Node *next;
};
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    Node *head = nullptr, *tail = nullptr;
    for (int i = 0; i < n; i++) {
        int x; scanf("%d", &x);
        Node *p = new Node{x, nullptr};
        if (!head) head = tail = p;        // 第一个结点
        else { tail->next = p; tail = p; } // 挂到表尾
    }
    for (Node *p = head; p; p = p->next) printf("%d%c", p->val, p->next ? ' ' : '\n');
    while (head) { Node *t = head; head = head->next; delete t; }   // 逐个释放
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int val[1005], nxt[1005];       // 数组模拟链表
    int head = -1, tail = -1;
    for (int i = 0; i < n; i++) {
        scanf("%d", &val[i]);
        nxt[i] = -1;
        if (head == -1) head = i;
        else nxt[tail] = i;
        tail = i;
    }
    for (int p = head; p != -1; p = nxt[p]) printf("%d%c", val[p], nxt[p] == -1 ? '\n' : ' ');
    return 0;
}
''',
  ["链表", "尾插", "建表"])

A("【链表】头插法建表（输出逆序）", SEC_LK, 2,
  stmt("用**头插法**建单链表（每次把新结点插在表头），读入 `n` 和 `n` 个整数，输出链表。"
       "因为头插，输出顺序与输入相反。",
       ["头插只有两步：`p->next = head; head = p;`",
        "头插不需要尾指针，但会自然把顺序反过来 —— 这是「逆序建表」的常用技巧",
        "输出一行"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：逆序的链表。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases("5\n1 2 3 4 5", "1\n9", "3\n7 8 9",
                "%d\n%s" % (8, " ".join(str(x) for x in rints(310, 8))),
                "4\n1 1 2 2", "%d\n%s" % (5, " ".join(str(x) for x in rints(311, 5, -50, 50)))),
  _rev,
  r'''#include <cstdio>
struct Node { int val; Node *next; };
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    Node *head = nullptr;
    for (int i = 0; i < n; i++) {
        int x; scanf("%d", &x);
        head = new Node{x, head};          // 头插：新结点的 next 指向原表头
    }
    for (Node *p = head; p; p = p->next) printf("%d%c", p->val, p->next ? ' ' : '\n');
    while (head) { Node *t = head; head = head->next; delete t; }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int val[1005], nxt[1005];
    int head = -1;
    for (int i = 0; i < n; i++) {
        scanf("%d", &val[i]);
        nxt[i] = head;                     // 数组模拟头插
        head = i;
    }
    for (int p = head; p != -1; p = nxt[p]) printf("%d%c", val[p], nxt[p] == -1 ? '\n' : ' ');
    return 0;
}
''',
  ["链表", "头插", "逆序"])

A("【链表】求链表长度与结点和", SEC_LK, 1,
  stmt("读入 `n` 和 `n` 个整数建成链表，遍历一次同时求出长度和所有结点值之和，"
       "输出 `长度 和`（一行）。",
       ["遍历时计数器与累加器一起走，只扫一遍",
        "和用 `long long`",
        "输出一行两个数"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：`长度 和`。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases("5\n1 2 3 4 5", "1\n-7", "3\n0 0 0",
                "%d\n%s" % (10, " ".join(str(x) for x in rints(320, 10))),
                "%d\n%s" % (6, " ".join(str(x) for x in rints(321, 6, -1000, 1000))),
                "2\n1000000 1000000"),
  _len_sum,
  r'''#include <cstdio>
struct Node { int val; Node *next; };
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    Node *head = nullptr, *tail = nullptr;
    for (int i = 0; i < n; i++) {
        int x; scanf("%d", &x);
        Node *p = new Node{x, nullptr};
        if (!head) head = tail = p; else { tail->next = p; tail = p; }
    }
    int len = 0;
    long long s = 0;
    for (Node *p = head; p; p = p->next) { len++; s += p->val; }   // 一趟搞定
    printf("%d %lld\n", len, s);
    while (head) { Node *t = head; head = head->next; delete t; }
    return 0;
}
''',
  r'''#include <cstdio>
struct Node { int val; Node *next; };
int walk(Node *p, int &len, long long &s) {      // 递归遍历
    if (!p) return 0;
    len++;
    s += p->val;
    return walk(p->next, len, s);
}
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    Node *head = nullptr, *tail = nullptr;
    for (int i = 0; i < n; i++) {
        int x; scanf("%d", &x);
        Node *p = new Node{x, nullptr};
        if (!head) head = tail = p; else { tail->next = p; tail = p; }
    }
    int len = 0; long long s = 0;
    walk(head, len, s);
    printf("%d %lld\n", len, s);
    while (head) { Node *t = head; head = head->next; delete t; }
    return 0;
}
''',
  ["链表", "遍历", "统计"])

A("【链表】查找值首次出现的位置", SEC_LK, 2,
  stmt("读入 `n`、`n` 个整数和目标值 `x`，在链表中查找 `x` 第一次出现的位置（从 1 开始），"
       "找不到输出 `-1`。",
       ["遍历时用一个计数器记录位置",
        "找到就立刻返回，不要跑完全程",
        "输出一个整数"]),
  "第一行 `n x`，第二行 `n` 个整数。",
  "一行：位置或 `-1`。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases("5 3\n1 2 3 4 3", "5 9\n1 2 3 4 5", "1 1\n1", "3 2\n2 2 2",
                "%d %d\n%s" % (8, 5, " ".join(str(x) for x in rints(330, 8, 1, 9))),
                "%d %d\n%s" % (4, -1, " ".join(str(x) for x in rints(331, 4, 0, 9)))),
  _first_pos,
  r'''#include <cstdio>
struct Node { int val; Node *next; };
int main() {
    int n, x;
    if (scanf("%d %d", &n, &x) != 2) return 0;
    Node *head = nullptr, *tail = nullptr;
    for (int i = 0; i < n; i++) {
        int v; scanf("%d", &v);
        Node *p = new Node{v, nullptr};
        if (!head) head = tail = p; else { tail->next = p; tail = p; }
    }
    int pos = 0, ans = -1;
    for (Node *p = head; p; p = p->next) {
        pos++;
        if (p->val == x) { ans = pos; break; }   // 第一次就收工
    }
    printf("%d\n", ans);
    while (head) { Node *t = head; head = head->next; delete t; }
    return 0;
}
''',
  r'''#include <cstdio>
struct Node { int val; Node *next; };
int main() {
    int n, x;
    if (scanf("%d %d", &n, &x) != 2) return 0;
    static int val[1005], nxt[1005];
    int head = -1, tail = -1;
    for (int i = 0; i < n; i++) {
        scanf("%d", &val[i]); nxt[i] = -1;
        if (head == -1) head = i; else nxt[tail] = i;
        tail = i;
    }
    int pos = 0, ans = -1;
    for (int p = head; p != -1; p = nxt[p]) {
        pos++;
        if (val[p] == x) { ans = pos; break; }
    }
    printf("%d\n", ans);
    return 0;
}
''',
  ["链表", "查找"])

A("【链表】在第 k 个位置前插入结点", SEC_LK, 3,
  stmt("读入 `n k x` 和 `n` 个整数建成链表，在**第 k 个结点之前**插入值为 `x` 的新结点，"
       "输出插入后的链表。`k = 1` 表示插在表头；`k > n` 表示追加到表尾。",
       ["插在第 k 个之前，要走到**第 k-1 个**结点，然后 `p->next = newNode`",
        "`k = 1` 时没有第 0 个结点，必须单独处理（改 head）",
        "输出一行"]),
  "第一行 `n k x`，第二行 `n` 个整数。",
  "一行：插入后的链表。",
  "- 1 ≤ n ≤ 1000\n- 1 ≤ k ≤ 10⁶\n- |x| ≤ 10⁶",
  lambda: cases("5 1 99\n1 2 3 4 5", "5 3 99\n1 2 3 4 5", "5 6 99\n1 2 3 4 5",
                "1 1 0\n5", "3 2 -1\n7 8 9",
                "%d 2 %d\n%s" % (6, 42, " ".join(str(x) for x in rints(340, 6)))),
  _insert_at,
  r'''#include <cstdio>
struct Node { int val; Node *next; };
int main() {
    int n, k, x;
    if (scanf("%d %d %d", &n, &k, &x) != 3) return 0;
    Node *head = nullptr, *tail = nullptr;
    for (int i = 0; i < n; i++) {
        int v; scanf("%d", &v);
        Node *p = new Node{v, nullptr};
        if (!head) head = tail = p; else { tail->next = p; tail = p; }
    }
    Node *fresh = new Node{x, nullptr};
    if (k <= 1) { fresh->next = head; head = fresh; }      // 插表头
    else {
        Node *p = head;
        int pos = 1;
        while (p->next && pos < k - 1) { p = p->next; pos++; }   // 走到第 k-1 个
        fresh->next = p->next;
        p->next = fresh;
    }
    for (Node *p = head; p; p = p->next) printf("%d%c", p->val, p->next ? ' ' : '\n');
    while (head) { Node *t = head; head = head->next; delete t; }
    return 0;
}
''',
  r'''#include <cstdio>
struct Node { int val; Node *next; };
int main() {
    int n, k, x;
    if (scanf("%d %d %d", &n, &k, &x) != 3) return 0;
    Node dummy{0, nullptr};                 // 哑结点：让「插表头」不用特判
    Node *tail = &dummy;
    for (int i = 0; i < n; i++) {
        int v; scanf("%d", &v);
        tail->next = new Node{v, nullptr};
        tail = tail->next;
    }
    Node *prev = &dummy;
    for (int i = 1; i < k && prev->next; i++) prev = prev->next;
    Node *fresh = new Node{x, prev->next};
    prev->next = fresh;
    for (Node *p = dummy.next; p; p = p->next) printf("%d%c", p->val, p->next ? ' ' : '\n');
    while (dummy.next) { Node *t = dummy.next; dummy.next = t->next; delete t; }
    return 0;
}
''',
  ["链表", "插入", "哑结点"])

A("【链表】删除第 k 个结点", SEC_LK, 3,
  stmt("读入 `n k` 和 `n` 个整数建成链表，删除第 k 个结点，输出剩余链表；"
       "删完为空则输出 `empty`。`k` 超出范围时不做任何删除。",
       ["删除要拿到**前驱**，所以走到第 k-1 个",
        "删表头要改 head；用哑结点可以一并处理",
        "删完记得 `delete`"]),
  "第一行 `n k`，第二行 `n` 个整数。",
  "一行：剩余链表，或 `empty`。",
  "- 1 ≤ n ≤ 1000\n- 1 ≤ k ≤ 10⁶",
  lambda: cases("5 1\n1 2 3 4 5", "5 3\n1 2 3 4 5", "1 1\n7", "5 9\n1 2 3 4 5",
                "3 2\n9 8 7", "%d 4\n%s" % (6, " ".join(str(x) for x in rints(350, 6)))),
  _del_at,
  r'''#include <cstdio>
struct Node { int val; Node *next; };
int main() {
    int n, k;
    if (scanf("%d %d", &n, &k) != 2) return 0;
    Node dummy{0, nullptr};
    Node *tail = &dummy;
    for (int i = 0; i < n; i++) {
        int v; scanf("%d", &v);
        tail->next = new Node{v, nullptr};
        tail = tail->next;
    }
    Node *prev = &dummy;
    for (int i = 1; i < k && prev->next; i++) prev = prev->next;
    if (prev->next) {                            // k 合法才删
        Node *victim = prev->next;
        prev->next = victim->next;
        delete victim;
    }
    if (!dummy.next) { printf("empty\n"); return 0; }
    for (Node *p = dummy.next; p; p = p->next) printf("%d%c", p->val, p->next ? ' ' : '\n');
    while (dummy.next) { Node *t = dummy.next; dummy.next = t->next; delete t; }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n, k;
    if (scanf("%d %d", &n, &k) != 2) return 0;
    static int val[1005], nxt[1005];
    int head = -1, tail = -1;
    for (int i = 0; i < n; i++) {
        scanf("%d", &val[i]); nxt[i] = -1;
        if (head == -1) head = i; else nxt[tail] = i;
        tail = i;
    }
    if (k == 1) head = nxt[head];                // 删表头
    else {
        int prev = head;
        for (int i = 1; i < k - 1 && nxt[prev] != -1; i++) prev = nxt[prev];
        if (nxt[prev] != -1) nxt[prev] = nxt[nxt[prev]];   // 跳过被删结点
    }
    if (head == -1) { printf("empty\n"); return 0; }
    for (int p = head; p != -1; p = nxt[p]) printf("%d%c", val[p], nxt[p] == -1 ? '\n' : ' ');
    return 0;
}
''',
  ["链表", "删除"])

A("【链表】原地逆序链表", SEC_LK, 3,
  stmt("读入 `n` 和 `n` 个整数建成链表，把链表**原地**逆序后输出。",
       ["三指针法：`prev`、`cur`、`next`，每步把 `cur->next` 指向 `prev`",
        "顺序不能错：先存 `next`，再改 `cur->next`，最后两个指针一起前移",
        "输出一行"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：逆序后的链表。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases("5\n1 2 3 4 5", "1\n7", "3\n1 2 3",
                "%d\n%s" % (8, " ".join(str(x) for x in rints(360, 8))),
                "4\n0 0 0 0", "%d\n%s" % (6, " ".join(str(x) for x in rints(361, 6, -9, 9)))),
  _rev,
  r'''#include <cstdio>
struct Node { int val; Node *next; };
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    Node *head = nullptr, *tail = nullptr;
    for (int i = 0; i < n; i++) {
        int v; scanf("%d", &v);
        Node *p = new Node{v, nullptr};
        if (!head) head = tail = p; else { tail->next = p; tail = p; }
    }
    Node *prev = nullptr, *cur = head;
    while (cur) {
        Node *nxt = cur->next;    // ① 先存下一站
        cur->next = prev;         // ② 反转指针
        prev = cur;               // ③ 整体后移
        cur = nxt;
    }
    head = prev;
    for (Node *p = head; p; p = p->next) printf("%d%c", p->val, p->next ? ' ' : '\n');
    while (head) { Node *t = head; head = head->next; delete t; }
    return 0;
}
''',
  r'''#include <cstdio>
struct Node { int val; Node *next; };
Node *rev(Node *p) {                       // 递归逆序
    if (!p || !p->next) return p;
    Node *h = rev(p->next);
    p->next->next = p;
    p->next = nullptr;
    return h;
}
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    Node *head = nullptr, *tail = nullptr;
    for (int i = 0; i < n; i++) {
        int v; scanf("%d", &v);
        Node *p = new Node{v, nullptr};
        if (!head) head = tail = p; else { tail->next = p; tail = p; }
    }
    head = rev(head);
    for (Node *p = head; p; p = p->next) printf("%d%c", p->val, p->next ? ' ' : '\n');
    while (head) { Node *t = head; head = head->next; delete t; }
    return 0;
}
''',
  ["链表", "逆序", "三指针"])

A("【链表】合并两个有序链表", SEC_LK, 3,
  stmt("读入两个**升序**链表，合并成一个仍然升序的链表并输出。"
       "格式：第一行 `n`，第二行 `n` 个数；第三行 `m`，第四行 `m` 个数。",
       ["双指针：每次取两个表头中较小的那个接到结果表尾",
        "一个表走完后，把另一个表的剩余部分整段接上",
        "输出一行"]),
  "第一行 `n`；第二行 `n` 个升序整数；第三行 `m`；第四行 `m` 个升序整数。",
  "一行：合并后的升序链表。",
  "- 1 ≤ n, m ≤ 500\n- |x| ≤ 10⁶",
  lambda: cases("3\n1 4 7\n3\n2 5 8", "1\n1\n1\n2", "3\n1 2 3\n3\n4 5 6",
                "2\n5 6\n2\n1 2", "1\n0\n1\n0",
                "4\n1 3 5 7\n4\n2 4 6 8"),
  _merge,
  r'''#include <cstdio>
struct Node { int val; Node *next; };
Node *build(int n) {
    Node *head = nullptr, *tail = nullptr;
    for (int i = 0; i < n; i++) {
        int v; scanf("%d", &v);
        Node *p = new Node{v, nullptr};
        if (!head) head = tail = p; else { tail->next = p; tail = p; }
    }
    return head;
}
int main() {
    int n, m;
    if (scanf("%d", &n) != 1) return 0;
    Node *a = build(n);
    if (scanf("%d", &m) != 1) return 0;
    Node *b = build(m);
    Node dummy{0, nullptr}, *t = &dummy;
    while (a && b) {                       // 双指针归并
        if (a->val <= b->val) { t->next = a; a = a->next; }
        else { t->next = b; b = b->next; }
        t = t->next;
    }
    t->next = a ? a : b;                   // 剩余部分整段接上
    for (Node *p = dummy.next; p; p = p->next) printf("%d%c", p->val, p->next ? ' ' : '\n');
    return 0;
}
''',
  r'''#include <cstdio>
#include <vector>
#include <algorithm>
int main() {
    int n, m;
    if (scanf("%d", &n) != 1) return 0;
    std::vector<int> v(n);
    for (int i = 0; i < n; i++) scanf("%d", &v[i]);
    if (scanf("%d", &m) != 1) return 0;
    for (int i = 0; i < m; i++) { int x; scanf("%d", &x); v.push_back(x); }
    std::sort(v.begin(), v.end());         // 偷懒版：全排一遍
    for (int i = 0; i < (int)v.size(); i++) printf("%d%c", v[i], i + 1 == (int)v.size() ? '\n' : ' ');
    return 0;
}
''',
  ["链表", "归并", "双指针"])

A("【链表】删除重复元素保序", SEC_LK, 2,
  stmt("读入 `n` 和 `n` 个整数建成链表，删除重复出现的结点，只保留每个值**第一次**出现的位置，"
       "输出结果。",
       ["用一个 `bool seen[]`（值域小时）或 `set` 记录出现过没有",
        "边遍历边删除，注意保存前驱",
        "输出一行"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：去重后的链表。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases("5\n1 2 1 3 2", "3\n1 1 1", "1\n5",
                "%d\n%s" % (8, " ".join(str(x) for x in rints(370, 8, 1, 4))),
                "4\n1 2 3 4", "%d\n%s" % (6, " ".join(str(x) for x in rints(371, 6, 0, 2)))),
  _dedup_list,
  r'''#include <cstdio>
#include <set>
struct Node { int val; Node *next; };
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    Node dummy{0, nullptr}, *tail = &dummy;
    std::set<int> seen;
    for (int i = 0; i < n; i++) {
        int v; scanf("%d", &v);
        if (!seen.insert(v).second) continue;    // 出现过了，直接丢弃
        tail->next = new Node{v, nullptr};
        tail = tail->next;
    }
    for (Node *p = dummy.next; p; p = p->next) printf("%d%c", p->val, p->next ? ' ' : '\n');
    return 0;
}
''',
  r'''#include <cstdio>
struct Node { int val; Node *next; };
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static Node pool[1005];              // 静态结点池，免去 new
    int cnt = 0;
    Node dummy{0, nullptr}, *tail = &dummy;
    for (int i = 0; i < n; i++) {
        int v; scanf("%d", &v);
        bool dup = false;
        for (Node *p = dummy.next; p; p = p->next) if (p->val == v) { dup = true; break; }
        if (dup) continue;
        pool[cnt].val = v; pool[cnt].next = nullptr;
        tail->next = &pool[cnt++];
        tail = tail->next;
    }
    for (Node *p = dummy.next; p; p = p->next) printf("%d%c", p->val, p->next ? ' ' : '\n');
    return 0;
}
''',
  ["链表", "去重"])

A("【链表】求中间结点", SEC_LK, 3,
  stmt("读入 `n` 和 `n` 个整数建成链表，输出**中间结点**的值。`n` 为偶数时取中间偏前的那个"
       "（即第 `n/2` 个）。",
       ["快慢指针：快指针一次走两步，慢指针一次走一步，快指针到头时慢指针就在中间",
        "偶数个结点时，快指针的判断条件决定取偏前还是偏后一个",
        "输出一个整数"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：中间结点的值。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases("5\n1 2 3 4 5", "4\n1 2 3 4", "1\n9", "2\n3 4",
                "%d\n%s" % (8, " ".join(str(x) for x in rints(380, 8))),
                "%d\n%s" % (7, " ".join(str(x) for x in rints(381, 7, 10, 99)))),
  _middle,
  r'''#include <cstdio>
struct Node { int val; Node *next; };
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    Node *head = nullptr, *tail = nullptr;
    for (int i = 0; i < n; i++) {
        int v; scanf("%d", &v);
        Node *p = new Node{v, nullptr};
        if (!head) head = tail = p; else { tail->next = p; tail = p; }
    }
    Node *slow = head, *fast = head;
    while (fast->next && fast->next->next) {   // 偶数时停在偏前那个
        slow = slow->next;
        fast = fast->next->next;
    }
    printf("%d\n", slow->val);
    while (head) { Node *t = head; head = head->next; delete t; }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int val[1005];
    for (int i = 0; i < n; i++) scanf("%d", &val[i]);
    printf("%d\n", val[(n - 1) / 2]);          // 直接算下标，结果一致
    return 0;
}
''',
  ["链表", "快慢指针", "中间结点"])

A("【链表】约瑟夫环出列顺序", SEC_LK, 4,
  stmt("`n` 个人围成一圈（编号 1~n），从 1 号开始报数，报到 `m` 的人出列，"
       "然后从下一个人重新报数。读入 `n m`，按出列顺序输出所有人的编号。",
       ["用循环链表：出列就是把前驱的 `next` 指向被删结点的后继",
        "每轮要走 `m-1` 步（不是 `m` 步），因为当前人算第 1 个",
        "只有一个人时 `next` 指向自己，别写成 `nullptr`"]),
  "一行两个整数 `n m`。",
  "一行：出列顺序，空格分隔。",
  "- 1 ≤ n ≤ 1000\n- 1 ≤ m ≤ 1000",
  lambda: cases("5 3", "1 1", "2 1", "5 1", "7 4", "6 2"),
  _joseph,
  r'''#include <cstdio>
struct Node { int val; Node *next; };
int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2 || n <= 0) return 0;
    Node *head = new Node{1, nullptr};
    Node *tail = head;
    for (int i = 2; i <= n; i++) { tail->next = new Node{i, nullptr}; tail = tail->next; }
    tail->next = head;                         // 首尾相接成环
    Node *prev = tail, *cur = head;
    for (int left = n; left >= 1; left--) {
        for (int s = 1; s < m; s++) { prev = cur; cur = cur->next; }   // 走 m-1 步
        printf("%d%c", cur->val, left == 1 ? '\n' : ' ');
        prev->next = cur->next;                // 出列
        Node *t = cur;
        cur = cur->next;
        delete t;
    }
    return 0;
}
''',
  r'''#include <cstdio>
#include <vector>
int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2 || n <= 0) return 0;
    std::vector<int> a;
    for (int i = 1; i <= n; i++) a.push_back(i);
    int i = 0;
    while (!a.empty()) {                       // 用 vector 模拟环
        i = (i + m - 1) % (int)a.size();
        printf("%d%c", a[i], a.size() == 1 ? '\n' : ' ');
        a.erase(a.begin() + i);
    }
    return 0;
}
''',
  ["链表", "循环链表", "约瑟夫环"])

A("【链表】删除所有等于 x 的结点", SEC_LK, 2,
  stmt("读入 `n x` 和 `n` 个整数建成链表，删除**所有**值等于 `x` 的结点，输出剩余链表；"
       "全被删光输出 `empty`。",
       ["哑结点能省掉「删表头」的特判",
        "删除是循环里最容易写错的：`cur = cur->next` 要在判断之后",
        "输出一行"]),
  "第一行 `n x`，第二行 `n` 个整数。",
  "一行：剩余链表，或 `empty`。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases("5 2\n1 2 3 2 4", "3 1\n1 1 1", "1 5\n5", "4 9\n1 2 3 4",
                "%d 1\n%s" % (6, " ".join(str(x) for x in rints(390, 6, 1, 3))),
                "3 0\n0 1 0"),
  _del_value,
  r'''#include <cstdio>
struct Node { int val; Node *next; };
int main() {
    int n, x;
    if (scanf("%d %d", &n, &x) != 2) return 0;
    Node dummy{0, nullptr}, *tail = &dummy;
    for (int i = 0; i < n; i++) {
        int v; scanf("%d", &v);
        tail->next = new Node{v, nullptr};
        tail = tail->next;
    }
    Node *prev = &dummy;
    while (prev->next) {
        if (prev->next->val == x) {            // 命中就删，prev 不动
            Node *t = prev->next;
            prev->next = t->next;
            delete t;
        } else prev = prev->next;
    }
    if (!dummy.next) { printf("empty\n"); return 0; }
    for (Node *p = dummy.next; p; p = p->next) printf("%d%c", p->val, p->next ? ' ' : '\n');
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n, x;
    if (scanf("%d %d", &n, &x) != 2) return 0;
    static int val[1005], nxt[1005];
    int head = -1, tail = -1;
    for (int i = 0; i < n; i++) {
        scanf("%d", &val[i]); nxt[i] = -1;
        if (head == -1) head = i; else nxt[tail] = i;
        tail = i;
    }
    while (head != -1 && val[head] == x) head = nxt[head];    // 先清表头
    for (int p = head; p != -1; p = nxt[p])
        while (nxt[p] != -1 && val[nxt[p]] == x) nxt[p] = nxt[nxt[p]];
    if (head == -1) { printf("empty\n"); return 0; }
    for (int p = head; p != -1; p = nxt[p]) printf("%d%c", val[p], nxt[p] == -1 ? '\n' : ' ');
    return 0;
}
''',
  ["链表", "删除", "哑结点"])

A("【链表】求最大值与位置", SEC_LK, 2,
  stmt("读入 `n` 和 `n` 个整数建成链表，输出最大值及它第一次出现的结点位置（从 1 开始）。",
       ["遍历时同时维护「当前最大」和「它的位置」",
        "更新条件用严格大于，才能取到第一次出现的位置",
        "输出一行两个整数"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：`最大值 位置`。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases("5\n3 1 4 1 5", "1\n-9", "3\n5 5 1", "4\n-1 -2 -3 -4",
                "%d\n%s" % (7, " ".join(str(x) for x in rints(400, 7))),
                "3\n0 0 0"),
  _max_pos,
  r'''#include <cstdio>
struct Node { int val; Node *next; };
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    Node *head = nullptr, *tail = nullptr;
    for (int i = 0; i < n; i++) {
        int v; scanf("%d", &v);
        Node *p = new Node{v, nullptr};
        if (!head) head = tail = p; else { tail->next = p; tail = p; }
    }
    int mx = head->val, pos = 1, i = 1, best = 1;
    for (Node *p = head; p; p = p->next, i++) {
        if (p->val > mx) { mx = p->val; best = i; }   // 严格大于
    }
    printf("%d %d\n", mx, best);
    (void)pos;
    while (head) { Node *t = head; head = head->next; delete t; }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int val[1005], nxt[1005];
    int head = -1, tail = -1;
    for (int i = 0; i < n; i++) {
        scanf("%d", &val[i]); nxt[i] = -1;
        if (head == -1) head = i; else nxt[tail] = i;
        tail = i;
    }
    int mx = val[head], best = 1, i = 1;
    for (int p = head; p != -1; p = nxt[p], i++)
        if (val[p] > mx) { mx = val[p]; best = i; }
    printf("%d %d\n", mx, best);
    return 0;
}
''',
  ["链表", "最值"])

A("【链表】判断链表是否严格递增", SEC_LK, 2,
  stmt("读入 `n` 和 `n` 个整数建成链表，判断它是否**严格递增**（后一个严格大于前一个）。"
       "是输出 `YES`，否则输出 `NO`。",
       ["只要出现 `cur->val >= cur->next->val` 就不满足",
        "单结点链表算递增",
        "只输出 `YES` 或 `NO`"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：`YES` 或 `NO`。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases("3\n1 2 3", "3\n1 2 2", "1\n5", "3\n3 2 1",
                "%d\n%s" % (5, " ".join(str(x) for x in rints(410, 5))),
                "4\n-3 -2 -1 0"),
  _increasing,
  r'''#include <cstdio>
struct Node { int val; Node *next; };
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    Node *head = nullptr, *tail = nullptr;
    for (int i = 0; i < n; i++) {
        int v; scanf("%d", &v);
        Node *p = new Node{v, nullptr};
        if (!head) head = tail = p; else { tail->next = p; tail = p; }
    }
    bool ok = true;
    for (Node *p = head; p->next; p = p->next)
        if (p->val >= p->next->val) { ok = false; break; }   // 必须严格大于
    printf("%s\n", ok ? "YES" : "NO");
    while (head) { Node *t = head; head = head->next; delete t; }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    static int val[1005];
    for (int i = 0; i < n; i++) scanf("%d", &val[i]);
    bool ok = true;
    for (int i = 0; i + 1 < n; i++) if (val[i] >= val[i + 1]) ok = false;
    printf("%s\n", ok ? "YES" : "NO");
    return 0;
}
''',
  ["链表", "递增", "判断"])

A("【链表】按值分段（小于 x 的在前）", SEC_LK, 4,
  stmt("读入 `n x` 和 `n` 个整数建成链表，把所有小于 `x` 的结点排到前面，"
       "其余排在后面，**两段内部都保持原来的相对顺序**，输出结果。",
       ["建两个子链表：一个挂小于 x 的，一个挂其余的，最后首尾相接",
        "关键是「保持相对顺序」—— 所以必须用尾插，不能头插",
        "输出一行"]),
  "第一行 `n x`，第二行 `n` 个整数。",
  "一行：分段后的链表。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases("5 3\n1 4 2 5 3", "5 10\n1 2 3 4 5", "3 0\n1 2 3", "1 5\n9",
                "%d 5\n%s" % (7, " ".join(str(x) for x in rints(420, 7, 0, 9))),
                "6 100\n1 2 3 4 5 6"),
  _partition,
  r'''#include <cstdio>
struct Node { int val; Node *next; };
int main() {
    int n, x;
    if (scanf("%d %d", &n, &x) != 2) return 0;
    Node less{0, nullptr}, *lt = &less;
    Node rest{0, nullptr}, *rt = &rest;
    for (int i = 0; i < n; i++) {
        int v; scanf("%d", &v);
        if (v < x) { lt->next = new Node{v, nullptr}; lt = lt->next; }   // 尾插保序
        else       { rt->next = new Node{v, nullptr}; rt = rt->next; }
    }
    lt->next = rest.next;                 // 两段接起来
    for (Node *p = less.next; p; p = p->next) printf("%d%c", p->val, p->next ? ' ' : '\n');
    return 0;
}
''',
  r'''#include <cstdio>
#include <vector>
int main() {
    int n, x;
    if (scanf("%d %d", &n, &x) != 2) return 0;
    std::vector<int> v(n), a, b;
    for (int i = 0; i < n; i++) {
        scanf("%d", &v[i]);
        if (v[i] < x) a.push_back(v[i]); else b.push_back(v[i]);
    }
    for (int i = 0; i < (int)b.size(); i++) a.push_back(b[i]);
    for (int i = 0; i < (int)a.size(); i++) printf("%d%c", a[i], i + 1 == (int)a.size() ? '\n' : ' ');
    return 0;
}
''',
  ["链表", "分段", "稳定"])

A("【链表】两个链表的并集", SEC_LK, 3,
  stmt("读入两个链表，输出它们的并集（每个值只出现一次，按升序）。"
       "格式：第一行 `n`，第二行 `n` 个数；第三行 `m`，第四行 `m` 个数。",
       ["「并集」意味着去重，重复值只留一个",
        "先把两个链表结在一起，再去重排序",
        "输出一行"]),
  "第一行 `n`；第二行 `n` 个整数；第三行 `m`；第四行 `m` 个整数。",
  "一行：升序去重的并集。",
  "- 1 ≤ n, m ≤ 500\n- |x| ≤ 10⁶",
  lambda: cases("3\n1 2 3\n3\n2 3 4", "1\n5\n1\n5", "2\n1 2\n2\n3 4",
                "3\n9 8 7\n2\n7 6", "1\n0\n1\n1", "4\n1 1 2 2\n3\n2 3 3"),
  _union_list,
  r'''#include <cstdio>
#include <set>
struct Node { int val; Node *next; };
Node *build(int n) {
    Node *head = nullptr, *tail = nullptr;
    for (int i = 0; i < n; i++) {
        int v; scanf("%d", &v);
        Node *p = new Node{v, nullptr};
        if (!head) head = tail = p; else { tail->next = p; tail = p; }
    }
    return head;
}
int main() {
    int n, m;
    if (scanf("%d", &n) != 1) return 0;
    Node *a = build(n);
    if (scanf("%d", &m) != 1) return 0;
    Node *b = build(m);
    std::set<int> s;                        // set 天然去重 + 升序
    for (Node *p = a; p; p = p->next) s.insert(p->val);
    for (Node *p = b; p; p = p->next) s.insert(p->val);
    int i = 0, k = (int)s.size();
    for (int x : s) printf("%d%c", x, ++i == k ? '\n' : ' ');
    return 0;
}
''',
  r'''#include <cstdio>
#include <vector>
#include <algorithm>
int main() {
    int n, m;
    if (scanf("%d", &n) != 1) return 0;
    std::vector<int> v(n);
    for (int i = 0; i < n; i++) scanf("%d", &v[i]);
    if (scanf("%d", &m) != 1) return 0;
    for (int i = 0; i < m; i++) { int x; scanf("%d", &x); v.push_back(x); }
    std::sort(v.begin(), v.end());
    v.erase(std::unique(v.begin(), v.end()), v.end());   // 排序后去重
    for (int i = 0; i < (int)v.size(); i++) printf("%d%c", v[i], i + 1 == (int)v.size() ? '\n' : ' ');
    return 0;
}
''',
  ["链表", "并集", "去重"])

A("【链表】链表插入排序", SEC_LK, 4,
  stmt("读入 `n` 和 `n` 个整数建成链表，用**插入排序**把链表排成升序后输出。",
       ["维护一个「已排好序」的子链表，每取一个新结点就在里面找到插入位置",
        "在链表上做插入排序不需要移动元素，只改指针 —— 这是它相对数组的优势",
        "输出一行"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：升序链表。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases("5\n3 1 4 1 5", "1\n7", "4\n4 3 2 1", "3\n1 1 1",
                "%d\n%s" % (7, " ".join(str(x) for x in rints(430, 7))),
                "%d\n%s" % (6, " ".join(str(x) for x in rints(431, 6, -50, 50)))),
  _insert_sort,
  r'''#include <cstdio>
struct Node { int val; Node *next; };
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    Node dummy{0, nullptr};                   // dummy.next 是已排序部分的表头
    for (int i = 0; i < n; i++) {
        int v; scanf("%d", &v);
        Node *prev = &dummy;
        while (prev->next && prev->next->val <= v) prev = prev->next;   // 找插入位置
        prev->next = new Node{v, prev->next};
    }
    for (Node *p = dummy.next; p; p = p->next) printf("%d%c", p->val, p->next ? ' ' : '\n');
    while (dummy.next) { Node *t = dummy.next; dummy.next = t->next; delete t; }
    return 0;
}
''',
  r'''#include <cstdio>
#include <vector>
#include <algorithm>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    std::vector<int> v(n);
    for (int i = 0; i < n; i++) scanf("%d", &v[i]);
    std::sort(v.begin(), v.end());            // 等价的库函数版
    for (int i = 0; i < n; i++) printf("%d%c", v[i], i + 1 == n ? '\n' : ' ');
    return 0;
}
''',
  ["链表", "插入排序"])

A("【链表】奇偶位分离", SEC_LK, 3,
  stmt("读入 `n` 和 `n` 个整数建成链表，把**奇数位**（第 1、3、5…个）的结点排在前面，"
       "**偶数位**的排在后面，两段内部保持原顺序，输出结果。",
       ["按「位置」分而不是按「值」分 —— 别写成判断 `val % 2`",
        "和「按值分段」的写法一样：两个子链表尾插，最后相接",
        "输出一行"]),
  "第一行 `n`，第二行 `n` 个整数。",
  "一行：奇偶位分离后的链表。",
  "- 1 ≤ n ≤ 1000\n- |x| ≤ 10⁶",
  lambda: cases("5\n1 2 3 4 5", "1\n7", "4\n10 20 30 40", "6\n1 1 1 1 1 1",
                "%d\n%s" % (7, " ".join(str(x) for x in rints(440, 7))),
                "%d\n%s" % (6, " ".join(str(x) for x in rints(441, 6, -9, 9)))),
  _odd_even,
  r'''#include <cstdio>
struct Node { int val; Node *next; };
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    Node odd{0, nullptr}, *ot = &odd;
    Node even{0, nullptr}, *et = &even;
    for (int i = 1; i <= n; i++) {
        int v; scanf("%d", &v);
        if (i % 2 == 1) { ot->next = new Node{v, nullptr}; ot = ot->next; }   // 按位置分
        else            { et->next = new Node{v, nullptr}; et = et->next; }
    }
    ot->next = even.next;
    for (Node *p = odd.next; p; p = p->next) printf("%d%c", p->val, p->next ? ' ' : '\n');
    return 0;
}
''',
  r'''#include <cstdio>
#include <vector>
int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    std::vector<int> v(n);
    for (int i = 0; i < n; i++) scanf("%d", &v[i]);
    std::vector<int> out;
    for (int i = 0; i < n; i += 2) out.push_back(v[i]);
    for (int i = 1; i < n; i += 2) out.push_back(v[i]);
    for (int i = 0; i < n; i++) printf("%d%c", out[i], i + 1 == n ? '\n' : ' ');
    return 0;
}
''',
  ["链表", "奇偶位", "分离"])

A("【链表】两个大数链表相加", SEC_LK, 4,
  stmt("两个非负整数的每一位按高位到低位存成链表。读入两个整数（十进制，位数 ≤ 30），"
       "按链表相加的做法求和后输出。",
       ["从低位往高位加，所以要先把链表逆序（或者干脆从字符串尾部扫）",
        "每一位 `sum = a + b + carry`，`carry = sum / 10`",
        "两个数可能有 30 位，超过 `long long`（19 位）—— 必须按位做"]),
  "两行，各一个非负整数（位数 ≤ 30）。",
  "一行：两数之和。",
  "- 0 ≤ 数 ≤ 10³⁰\n- 位数 ≤ 30",
  lambda: cases("123\n456", "0\n0", "999\n1", "1\n999999999999999999999",
                "123456789012345678901234567890\n987654321098765432109876543210",
                "5\n5"),
  _big_add,
  r'''#include <cstdio>
#include <cstring>
#include <algorithm>
struct Node { int d; Node *next; };
Node *build(const char *s) {                // 高位在前
    Node *head = nullptr, *tail = nullptr;
    for (int i = 0; s[i]; i++) {
        Node *p = new Node{s[i] - '0', nullptr};
        if (!head) head = tail = p; else { tail->next = p; tail = p; }
    }
    return head;
}
Node *reverse(Node *h) {
    Node *prev = nullptr;
    while (h) { Node *n = h->next; h->next = prev; prev = h; h = n; }
    return prev;
}
int main() {
    char sa[64], sb[64];
    if (scanf("%63s", sa) != 1) return 0;
    if (scanf("%63s", sb) != 1) return 0;
    Node *a = reverse(build(sa));            // 逆序后低位在前
    Node *b = reverse(build(sb));
    int out[64], k = 0, carry = 0;
    while (a || b || carry) {
        int s = carry;
        if (a) { s += a->d; a = a->next; }
        if (b) { s += b->d; b = b->next; }
        out[k++] = s % 10;
        carry = s / 10;
    }
    while (k > 1 && out[k - 1] == 0) k--;    // 去掉前导零
    for (int i = k - 1; i >= 0; i--) printf("%d", out[i]);
    printf("\n");
    return 0;
}
''',
  r'''#include <cstdio>
#include <cstring>
int main() {
    char sa[64], sb[64];
    if (scanf("%63s", sa) != 1) return 0;
    if (scanf("%63s", sb) != 1) return 0;
    int la = (int)strlen(sa), lb = (int)strlen(sb);
    int n = la > lb ? la : lb;
    int out[64] = {0}, carry = 0;
    for (int i = 0; i < n; i++) {            // 直接从字符串尾部扫，不用链表
        int da = i < la ? sa[la - 1 - i] - '0' : 0;
        int db = i < lb ? sb[lb - 1 - i] - '0' : 0;
        int s = da + db + carry;
        out[i] = s % 10;
        carry = s / 10;
    }
    if (carry) out[n++] = carry;
    while (n > 1 && out[n - 1] == 0) n--;
    for (int i = n - 1; i >= 0; i--) printf("%d", out[i]);
    printf("\n");
    return 0;
}
''',
  ["链表", "大数", "进位"])

A("【链表】删除倒数第 k 个结点", SEC_LK, 4,
  stmt("读入 `n k` 和 `n` 个整数建成链表，删除**倒数第 k 个**结点，输出剩余链表；"
       "删完为空输出 `empty`。`k` 超出范围时不删。",
       ["快慢指针：快指针先走 k 步，然后两个一起走，快指针到头时慢指针就在倒数第 k 个的**前驱**",
        "`k == n` 时删的是表头，用哑结点一次处理掉",
        "输出一行"]),
  "第一行 `n k`，第二行 `n` 个整数。",
  "一行：剩余链表，或 `empty`。",
  "- 1 ≤ n ≤ 1000\n- 1 ≤ k ≤ 10⁶",
  lambda: cases("5 1\n1 2 3 4 5", "5 5\n1 2 3 4 5", "1 1\n7", "5 9\n1 2 3 4 5",
                "3 2\n9 8 7", "%d 3\n%s" % (6, " ".join(str(x) for x in rints(450, 6)))),
  _del_kth_last,
  r'''#include <cstdio>
struct Node { int val; Node *next; };
int main() {
    int n, k;
    if (scanf("%d %d", &n, &k) != 2) return 0;
    Node dummy{0, nullptr}, *tail = &dummy;
    for (int i = 0; i < n; i++) {
        int v; scanf("%d", &v);
        tail->next = new Node{v, nullptr};
        tail = tail->next;
    }
    Node *fast = &dummy, *slow = &dummy;
    for (int i = 0; i < k && fast; i++) fast = fast->next;   // 快指针先走 k 步
    if (fast) {
        while (fast->next) { fast = fast->next; slow = slow->next; }
        Node *victim = slow->next;
        slow->next = victim->next;
        delete victim;
    }
    if (!dummy.next) { printf("empty\n"); return 0; }
    for (Node *p = dummy.next; p; p = p->next) printf("%d%c", p->val, p->next ? ' ' : '\n');
    while (dummy.next) { Node *t = dummy.next; dummy.next = t->next; delete t; }
    return 0;
}
''',
  r'''#include <cstdio>
int main() {
    int n, k;
    if (scanf("%d %d", &n, &k) != 2) return 0;
    static int val[1005], nxt[1005];
    int head = -1, tail = -1;
    for (int i = 0; i < n; i++) {
        scanf("%d", &val[i]); nxt[i] = -1;
        if (head == -1) head = i; else nxt[tail] = i;
        tail = i;
    }
    int idx = n - k;                       // 倒数第 k 个就是正数第 n-k+1 个
    if (idx >= 0 && idx < n) {
        if (idx == 0) head = nxt[head];
        else {
            int prev = head;
            for (int i = 0; i < idx - 1; i++) prev = nxt[prev];
            nxt[prev] = nxt[nxt[prev]];
        }
    }
    if (head == -1) { printf("empty\n"); return 0; }
    for (int p = head; p != -1; p = nxt[p]) printf("%d%c", val[p], nxt[p] == -1 ? '\n' : ' ');
    return 0;
}
''',
  ["链表", "快慢指针", "倒数第k"])


if __name__ == "__main__":
    sys.exit(cli(PROBLEMS, "app/problems_bank_cpp_basic6.py",
                 "第 6 册：结构体与共用体 / 链表", "CPP_BASIC6_PROBLEMS"))
