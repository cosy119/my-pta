"""输出比对：4 种口径 + PE 判定。

判题的成败一半在这个文件。「本机跑对、交上去 WA」最常见的原因就是
换行与行尾空白没归一化，所以比对前**一律先做换行归一化**。

四种 checker：
- standard        忽略每行行尾空白 + 忽略末尾空行（默认，最常用）
- ignore_trailing 忽略每行行尾空白，但末尾空行的数量也必须一致（严一点）
- token           把所有空白折叠成单个空格再比（完全不敏感）
- float           逐 token 转 float，按 eps 容差比（同时要求 token 数量一致）

PE（格式错误）只在「归一化后不等、但去掉所有空白后相等」时才判 ——
这样能把「真错」和「只是格式抖动」分开。
"""
from __future__ import annotations

from dataclasses import dataclass

CHECKERS = ("standard", "ignore_trailing", "token", "float")


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
