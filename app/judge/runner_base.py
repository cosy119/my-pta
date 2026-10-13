"""判题 runner 的统一接口与共享数据类。

三种语言的 runner 都实现同一套 prepare / run_case / cleanup，
worker 只认这个接口，不关心下面跑的是解释器、编译器还是 SSH。
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from . import sandbox


@dataclass
class Limits:
    time_ms: int = 1000
    memory_mb: int = 256
    max_output_bytes: int = 1048576
    kill_grace_ms: int = 300


@dataclass
class CaseResult:
    """单个用例的结果。

    verdict == "OK" 表示进程正常结束 —— 还没比对，由 worker 拿 stdout 去比。
    其余取值：CE / TLE / MLE / RE / OLE / IE
    """
    verdict: str = "OK"
    time_ms: int = 0
    mem_kb: int = 0
    stdout: bytes = b""
    stderr: bytes = b""
    exit_code: int = 0
    detail: str = ""
    note: str = ""

    @property
    def finished_normally(self) -> bool:
        return self.verdict == "OK"


class Runner(Protocol):
    lang: str

    def prepare(self, code: str, workdir: Path) -> tuple[bool, str]:
        """编译或语法预检。返回 (是否通过, 错误信息)。"""
        ...

    def run_case(self, workdir: Path, stdin_bytes: bytes, limits: Limits) -> CaseResult:
        ...

    def cleanup(self, workdir: Path) -> None:
        ...


def verdict_from_run(r: "sandbox.RunResult", lang_hint: str = "") -> tuple[str, str, str]:
    """把沙箱运行结果翻译成判题判定。

    返回 (verdict, detail, note)。
    顺序很关键：先看内存/超时（这两者是「我们主动干预」造成的非零退出），
    再看输出超限，最后才看退出码 —— 否则 MLE/TLE 会被误判成 RE。
    """
    note = r.raw_note or ""
    if r.mem_exceeded:
        tail = _last_lines(r.stderr, 2)
        detail = f"峰值内存 {r.mem_kb // 1024} MB，撞到内存限制"
        if tail:
            detail += f"（{tail}）"
        return "MLE", detail, note
    if r.timed_out:
        return "TLE", f"运行超过 {r.time_ms} ms 仍没结束", note
    if r.truncated:
        return "OLE", "输出超过上限被截断（检查是否打印了不该打印的内容）", note
    if r.exit_code != 0:
        # 非零退出才是 RE；注意 Python 的 warning 走 stderr 但退出码是 0，不能只看 stderr
        tail = _last_lines(r.stderr)
        detail = f"进程以退出码 {r.exit_code} 结束"
        if tail:
            detail += f"：{tail}"
        return "RE", detail, note
    return "OK", "", note


def _last_lines(data: bytes, n: int = 3) -> str:
    if not data:
        return ""
    text = data.decode("utf-8", "replace").strip()
    if not text:
        return ""
    lines = [ln for ln in text.splitlines() if ln.strip()]
    return " | ".join(lines[-n:])[:400]


VERDICT_LABEL = {
    "AC": "Accepted 通过",
    "WA": "Wrong Answer 答案错误",
    "PE": "Presentation Error 格式错误",
    "TLE": "Time Limit Exceeded 超时",
    "MLE": "Memory Limit Exceeded 内存超限",
    "RE": "Runtime Error 运行错误",
    "CE": "Compile Error 编译错误",
    "OLE": "Output Limit Exceeded 输出超限",
    "IE": "Internal Error 判题器内部错误",
    "pending": "排队中",
}


def verdict_label(v: str) -> str:
    return VERDICT_LABEL.get(v, v)
