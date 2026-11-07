"""输出比对：4 种口径 + PE 判定。

判题的成败一半在这个文件。「本机跑对、交上去 WA」最常见的原因就是
换行与行尾空白没归一化，所以比对前**一律先做换行归一化**。

五种 checker：
- standard        忽略每行行尾空白 + 忽略末尾空行（默认，最常用）
- ignore_trailing 忽略每行行尾空白，但末尾空行的数量也必须一致（严一点）
- token           把所有空白折叠成单个空格再比（完全不敏感）
- float           逐 token 转 float，按 eps 容差比（同时要求 token 数量一致）
- oneof           **多个可接受答案**：期望值里以 `|` 开头的每一行都是一个答案，
                  命中任意一个即通过（按 token 口径比）。用于填空题 / 理论题 ——
                  比如「查看根目录含隐藏文件」写 `ls -a /` 和 `ls -la /` 都对。

PE（格式错误）只在「归一化后不等、但去掉所有空白后相等」时才判 ——
这样能把「真错」和「只是格式抖动」分开。
"""
from __future__ import annotations

import re
from dataclasses import dataclass

CHECKERS = ("standard", "ignore_trailing", "token", "float", "oneof", "oneof_strict")

# oneof 口径下，期望值里每一行可接受答案的前缀
_ALT_PREFIX = "|"


@dataclass
class CompareResult:
    ok: bool
    kind: str = "wa"          # ok | wa | pe
    detail: str = ""

    def __bool__(self) -> bool:
        return self.ok


def to_text(x: bytes | str | None) -> str:
    if x is None:
        return ""
    if isinstance(x, bytes):
        return x.decode("utf-8", "replace")
    return str(x)


def normalize_newlines(text: str) -> str:
    """\\r\\n 和孤立 \\r 都归一成 \\n。这一步是防「交上去 WA」的关键。"""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _lines_drop_trailing_blank(text: str) -> list[str]:
    lines = text.split("\n")
    while lines and lines[-1].strip() == "":
        lines.pop()
    return lines


def _squeeze_ws(text: str) -> str:
    return " ".join(text.split())


# 人手打答案时最容易顺手带上的「排版类」标点（全角标点 + 中文引号 + 顿号…）。
#
# ★★ 刻意**不含** ASCII 的 `. ' " ( ) [ ]` —— 它们在命令行里是有意义的：
#    `cd ../..`、`echo -n "hello"`、`dnf provides '*/ls'`。
#    早期版本把它们也当成「顺手标的标点」剥掉，结果是**答案的最后一个字符被吃掉**：
#    `cd ../..` 变成 `cd ../`，三条填空题的参考答案永远判不过自己。
_IF_LIKE_RE = re.compile(r"^\s*(if|elif|while|until)\b")

_EDGE_PUNCT = " \t\r\n。，、；：（）【】《》〈〉「」『』“”‘’…！？"


def answer_forms(text: bytes | str | None, *, fold_and: bool = True) -> set[str]:
    """同一个答案的「宽容形式」集合（从严格到宽松）。

    只往里**加**等价写法，绝不删掉原样 —— 这样任何原本判得过的答案
    在加了宽容之后依然判得过，不会引入回归。

    五层：
    1. 原文（空白折叠）
    2. 剥掉首尾的**排版类**标点（`ls -la /etc。` → `ls -la /etc`）
    3. 换行当命令分隔符（`cd /tmp\\nmkdir aa` → `cd /tmp ; mkdir aa`）
    4. 命令口径归一化（`ls -l -a /` → `ls -al /`，见 `_norm_cmd`）
    5. 「家目录」归一化（`/home/zhangsan/docs` → `~/docs`，见 `_norm_home`）

    ★ 第 3 层只影响**学生交上来的答案**：`oneof_alternatives` 取出来的
      每条可接受答案都是单行（按行解析），本身不含换行。
      所以这一层做的事情是「学生把多步命令一行一条地敲」也能判过 ——
      这正是多步命令题最常见的输入方式。

    ★ 第 6 层 `fold_and`：把 `A && B` 当作 `A; B`。
      绝大多数题的答案写成 `cd /etc && ls -d *pass*`，而学生按实验步骤
      「一行一条」写出来是 `cd /etc` + 换行 + `ls -d *pass*` —— 判题会把换行
      折成 `; `，于是两边差在 `&&` 与 `;` 上，明明对却判错（2026-11-07 反馈）。
      两边的 `&&` 都折成 `;` 再比，就都通了。
      **例外**：专考 `&&` 语义的题（「前一条成功才执行后一条」）用
      `checker = "oneof_strict"` 关掉这一层 —— 否则写 `;` 也算对，
      那道题就白出了。
    """
    t = normalize_newlines(to_text(text)).strip()
    seeds = [t]
    # 多步命令题：学生敲完一条按回车，和答案里写 `;` 完全等价。
    # 派生一个「换行 → ; 」的种子，顺便把「一半换行一半分号」的混写也覆盖掉。
    # ★ 空行要**先滤掉**再拼：`cmd1` 空一行 `cmd2` 会拼出 `cmd1 ; ; cmd2`，
    #   多出来的那个空分隔符会让答案永远对不上。
    if "\n" in t:
        lines = [ln.strip() for ln in t.split("\n") if ln.strip()]
        seeds.append(" ; ".join(lines))
    # `A && B` ≡ `A; B`（除非题目明说考 && 的语义，见 fold_and 的说明）。
    # 只折命令分隔符位置上的 `&&`：`if [ x ] && [ y ]; then` 里的 `&&`
    # 是 shell 语法的一部分，折掉就成了一段不存在的代码。
    if fold_and and " && " in t and not _IF_LIKE_RE.match(t):
        seeds.append(t.replace(" && ", "; "))

    forms: set[str] = set()
    for s in seeds:
        s = s.strip()
        if not s:
            continue
        forms.add(_squeeze_ws(s))
        core = s.strip(_EDGE_PUNCT).strip()
        if core and core != s:
            forms.add(_squeeze_ws(core))
    for f in list(forms):
        forms.add(_squeeze_ws(_norm_cmd(f)))
    for f in list(forms):
        forms.add(_squeeze_ws(_norm_home(f)))
    return forms


# `/home/<某个名字>` 这一整段（不含其后的路径分隔符）
_HOME_RE = re.compile(r"(?<![\w/])/home/[^/\s]+(?=/|\s|$)")


def _norm_home(text: str) -> str:
    """把 `/home/<谁>` 折成 `~`：`cp -a /home/zhangsan/docs /tmp/` → `cp -a ~/docs /tmp/`。

    为什么需要
    ----------
    Linux 线的题面里，别人的家目录写法是 `/home/<你的登录名>/...`，
    登录名**因人而异**（题库里写成占位符 `{user}`，显示时才替换）。
    如果答案只认 `~/docs`，那照着题面写 `/home/zhangsan/docs` 的人就白判一次错。

    所以不再往答案里堆「每个名字一个备选」（那永远堆不完），
    而是两边都折成 `~` 再比 —— 任意用户名都通吃。

    ★ 前提：**一道题的答案里不会出现「两个不同用户的家目录」**。
      题库里确实没有这种题（`/etc/passwd`、`chown` 这类考的是 `%U:%G` 用户名，
      不带 `/home/`）。真要出那种题，这条归一化就会把区分抹掉，得给题目开个开关。
    """
    return _HOME_RE.sub("~", text)


# 纯字母的短选项，如 -l / -a / -lah（两个横杠的长选项、带数字的 -9、单独的 - 都不匹配）
_SHORT_OPT_RE = re.compile(r"^-[A-Za-z]+$")

# 引号包起来的整段（单引号 / 双引号，允许跨行）
_QUOTED_RE = re.compile(r"'[^']*'|\"[^\"]*\"", re.S)

# shell 里连接多条命令的运算符。`||` `&&` 必须排在 `|` 前面，
# 否则 `a||b` 会先被 `|` 切成两半。
_OPER_RE = re.compile(r"\s*(\|\||&&|;|\|)\s*")


def _norm_oper(text: str) -> str:
    """引号外的 shell 运算符，两边统一成一个空格。

    为什么需要
    ----------
    多步命令题的标准答案写成 `cd /tmp; mkdir aa`，学生照着敲成
    `cd /tmp;mkdir aa`（分号后不留空格）或者 `cd /tmp ;  mkdir aa`
    （两边都留空格）。这三条执行结果一模一样，按字面比却判成三个答案。
    实测实验 2~5 的 41 道多步题里，有 **30 道**会被这两种写法误判成错。

    引号里的内容**原样不动** —— `grep "a|b" f` 里的 `|` 是字面量，
    动了它就把「匹配竖线」改成「管道」了。
    """
    parts = _QUOTED_RE.split(text)
    quoted = _QUOTED_RE.findall(text)
    out: list[str] = []
    for i, seg in enumerate(parts):
        out.append(_OPER_RE.sub(r" \1 ", seg))
        if i < len(quoted):
            out.append(quoted[i])
    return "".join(out).strip()


def _norm_cmd(text: str) -> str:
    """命令行的宽容归一化：空白折叠 + 运算符对齐 + 相邻短选项合并 + 簇内字母排序。

    为什么需要
    ----------
    `ls -la /etc`、`ls -al /etc`、`ls -l -a /etc` 是**同一件事**，
    但按字面比会被判成三个不同答案 —— 命令题这样判会把人逼疯。

    处理规则（只动「明显等价」的地方）
    - 空白多少无所谓
    - 引号外的 `;` `&&` `||` `|` 两边统一成一个空格（见 `_norm_oper`）
    - 相邻的纯字母短选项合并：`-l -a` → `-la`
    - 簇内字母排序并去重：`-lah` → `-ahl`，`-ll` → `-l`

    **刻意不碰**的情况：`--long`（两个横杠）、`-9`（带数字）、`-k2`、单独的 `-`、
    以及任何后面跟着参数的选项 —— 合并它们会把语义改掉
    （比如 `head -n -10` 里的 `-n` 和 `-10`，合并了就成另一个意思了）。

    ★ 运算符归一化必须**排在短选项合并之前**：`ls -l;ls -a` 先变成
      `ls -l ; ls -a`，`-l` 和 `-a` 才不会被并成 `-al`
      （它们是两条命令的选项，合并就把分号语义丢了）。

    只在 `oneof` 口径（理论题 / 填空命令题）里使用，编程题的输出比对不受影响。
    """
    toks = _norm_oper(text).split()
    out: list[str] = []
    i = 0
    while i < len(toks):
        if _SHORT_OPT_RE.match(toks[i]):
            buf = ""
            while i < len(toks) and _SHORT_OPT_RE.match(toks[i]):
                buf += toks[i][1:]
                i += 1
            out.append("-" + "".join(sorted(set(buf))))
            continue
        out.append(toks[i])
        i += 1
    return " ".join(out)


def oneof_alternatives(expected: str) -> list[str]:
    """从期望值里取出「多个可接受答案」清单。

    约定：只要期望值里出现以 `|` 开头的行，就按 oneof 口径解析 ——
    每一行去掉前缀 `|` 就是一个可接受答案（前后空白无所谓）。
    没有 `|` 行就返回空列表，表示「这不是 oneof 题」。
    """
    alts = [ln[1:].strip() for ln in normalize_newlines(to_text(expected)).split("\n")
            if ln.startswith(_ALT_PREFIX)]
    return [a for a in alts if a != ""]


def _diff_hint(expected: str, actual: str, max_lines: int = 6) -> str:
    """给一个「第几行开始不一样」的短提示，便于人眼快速定位。"""
    e_lines = _lines_drop_trailing_blank(expected)
    a_lines = _lines_drop_trailing_blank(actual)
    for i in range(max(len(e_lines), len(a_lines))):
        e = e_lines[i] if i < len(e_lines) else "<缺行>"
        a = a_lines[i] if i < len(a_lines) else "<缺行>"
        if e.rstrip() != a.rstrip():
            return f"第 {i + 1} 行起不同：期望 {e!r} / 实际 {a!r}"
    if len(e_lines) != len(a_lines):
        return f"行数不同：期望 {len(e_lines)} 行 / 实际 {len(a_lines)} 行"
    return ""


def compare(expected: bytes | str, actual: bytes | str, checker: str = "standard",
            eps: float = 1e-6) -> CompareResult:
    """比对实际输出与期望输出。"""
    e = normalize_newlines(to_text(expected))
    a = normalize_newlines(to_text(actual))
    checker = checker if checker in CHECKERS else "standard"

    # ---- 完全一致（归一化后）----
    if e == a:
        return CompareResult(True, "ok", "")

    # ---- oneof 口径：命中任意一个可接受答案即通过 ----
    # 注意要放在最前面 —— 这种题的期望值形如 "|B"，跟实际输出 "B" 永远不可能相等
    if _uses_oneof(checker, e):
        alts = oneof_alternatives(e)
        fold = checker != "oneof_strict"
        a_forms = answer_forms(a, fold_and=fold)
        for alt in alts:
            if answer_forms(alt, fold_and=fold) & a_forms:
                return CompareResult(True, "ok", "")
        shown = " / ".join(repr(x) for x in alts[:4])
        if len(alts) > 4:
            shown += f" 等 {len(alts)} 个"
        return CompareResult(False, "wa", f"都不匹配，可接受答案：{shown}")

    # ---- float 口径 ----
    if checker == "float":
        return _compare_float(e, a, eps)

    # ---- token 口径 ----
    if checker == "token":
        if _squeeze_ws(e) == _squeeze_ws(a):
            return CompareResult(True, "ok", "")
        return CompareResult(False, "wa", _diff_hint(e, a))

    # ---- standard / ignore_trailing：按行比 ----
    if checker == "ignore_trailing":
        e_lines = e.split("\n")
        a_lines = a.split("\n")
    else:  # standard：丢掉末尾空行
        e_lines = _lines_drop_trailing_blank(e)
        a_lines = _lines_drop_trailing_blank(a)

    e_norm = [ln.rstrip() for ln in e_lines]
    a_norm = [ln.rstrip() for ln in a_lines]

    if e_norm == a_norm:
        # 忽略行尾空白/末尾空行后相等 → 只是格式抖动，不判 WA
        return CompareResult(True, "ok", "输出了多余的行尾空白，已按该题口径忽略")

    # 去掉**所有**空白后相等 → PE（内容对、格式乱）
    if _squeeze_ws(e) == _squeeze_ws(a):
        return CompareResult(False, "pe", "内容正确但空白/换行与期望不符")

    return CompareResult(False, "wa", _diff_hint(e, a))


def _uses_oneof(checker: str, expected: str) -> bool:
    """这道题该不该按 oneof 口径判。

    两种情况：
    1. 题目显式写了 `checker = "oneof"`，**并且**期望值里确实有 `|` 行
    2. 题目写的是别的 checker，但期望值里出现了 `|` 行 ——
       建题时漏改 checker 是很常见的失误，按内容自动兜住，别让题白判错
       （反之：没有 `|` 行就老老实实按原口径走，不受影响）

    ★ 第 1 条必须**同时**要求有 `|` 行：写错了 checker 却没写 `|` 时，
      按 oneof 走会得到一份空的备选清单 —— 那等于把所有答案都判错，
      比老老实实按 standard 比还糟。
    """
    if not oneof_alternatives(expected):
        return False
    return checker in ("oneof", "oneof_strict") or expected.lstrip().startswith(_ALT_PREFIX)


def _compare_float(e: str, a: str, eps: float) -> CompareResult:
    e_tokens = e.split()
    a_tokens = a.split()
    if len(e_tokens) != len(a_tokens):
        return CompareResult(
            False, "wa",
            f"输出项数不同：期望 {len(e_tokens)} 项 / 实际 {len(a_tokens)} 项")
    for i, (et, at) in enumerate(zip(e_tokens, a_tokens)):
        if et == at:
            continue
        try:
            ev, av = float(et), float(at)
        except ValueError:
            return CompareResult(
                False, "wa", f"第 {i + 1} 项不是数字：期望 {et!r} / 实际 {at!r}")
        if not _close(ev, av, eps):
            return CompareResult(
                False, "wa",
                f"第 {i + 1} 项超出容差：期望 {et!r} / 实际 {at!r}（eps={eps:g}）")
    return CompareResult(True, "ok", "")


def _close(a: float, b: float, eps: float) -> bool:
    if a == b:
        return True
    if a != a or b != b:            # NaN
        return False
    diff = abs(a - b)
    if diff <= eps:
        return True
    scale = max(abs(a), abs(b))
    return scale > 0 and diff / scale <= eps
