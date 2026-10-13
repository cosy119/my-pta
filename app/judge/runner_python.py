"""Python 判题 runner。

流程：
1. prepare：先用内置 compile() 做语法预检 —— 语法错就直接 CE，不必真跑一次
2. run_case：在 Job Object 沙箱里跑 `main.py`，stdin 走字节

关于命令行参数：不加 `-I`（isolated）。因为 `-I` 在 3.11+ 隐含 `-P`，
会把脚本所在目录移出 sys.path，跟 OJ 的真实行为不一致。只用 `-X utf8=1 -u`：
- `-X utf8=1`：强制 UTF-8 模式，中文不会乱码
- `-u`：无缓冲输出（Thonny 也是这么跑的），程序中途崩了也不会丢已打印的内容
"""
from __future__ import annotations

import os
from pathlib import Path

from . import sandbox
from .runner_base import CaseResult, Limits, verdict_from_run

SRC_NAME = "main.py"

# 子进程环境：强制 UTF-8，且不生成 __pycache__（保持临时目录干净）
_PY_ENV = {
    "PYTHONUTF8": "1",
    "PYTHONIOENCODING": "utf-8",
    "PYTHONDONTWRITEBYTECODE": "1",
}


def format_syntax_error(e: SyntaxError, filename: str = SRC_NAME) -> str:
    """把 SyntaxError 拼成接近真实 traceback 的样子，方便展示。"""
    lines: list[str] = []
    lineno = e.lineno or 0
    lines.append(f'  File "{filename}", line {lineno}')
    if e.text:
        lines.append("    " + e.text.rstrip("\n"))
        if e.offset:
            lines.append("    " + " " * max(0, e.offset - 1) + "^")
    lines.append(f"SyntaxError: {e.msg or e}")
    return "\n".join(lines)


class PythonRunner:
    lang = "python"

    def __init__(self, interpreter: str, label: str = "py313"):
        self.interpreter = interpreter or ""
        self.label = label
        self._baseline_ms: int | None = None

    # ---------- 编译/语法预检 ----------
    def prepare(self, code: str, workdir: Path) -> tuple[bool, str]:
        try:
            compile(code, SRC_NAME, "exec")
        except SyntaxError as e:
            return False, format_syntax_error(e)
        except ValueError as e:                       # 例如源码里有 NUL 字节
            return False, f"SyntaxError: {e}"
        (Path(workdir) / SRC_NAME).write_text(code, encoding="utf-8")
        return True, ""

    # ---------- 单用例运行 ----------
    def run_case(self, workdir: Path, stdin_bytes: bytes, limits: Limits) -> CaseResult:
        if not self.interpreter or not os.path.exists(self.interpreter):
            return CaseResult(
                verdict="IE",
                detail=f"解释器不存在：{self.interpreter!r}（检查 config/settings.toml）")

        cmd = [self.interpreter, "-X", "utf8=1", "-u", SRC_NAME]
        r = sandbox.run(
            cmd,
            stdin_bytes=stdin_bytes,
            cwd=workdir,
            env=_PY_ENV,
            time_limit_ms=limits.time_ms,
            memory_limit_mb=limits.memory_mb,
            max_output_bytes=limits.max_output_bytes,
            kill_grace_ms=limits.kill_grace_ms,
        )
        verdict, detail, note = verdict_from_run(r)
        return CaseResult(
            verdict=verdict,
            time_ms=r.time_ms,
            mem_kb=r.mem_kb,
            stdout=r.stdout,
            stderr=r.stderr,
            exit_code=r.exit_code,
            detail=detail,
            note=note,
        )

    # ---------- 启动基线（可选信息） ----------
    def startup_baseline_ms(self) -> int:
        """空跑一次，量出「解释器启动 + 退出」大概要多少毫秒。

        判题用的是墙钟总时间，包含这段开销；把基线报给用户，方便他判断
        「是程序慢还是解释器启动慢」。
        """
        if self._baseline_ms is None:
            if not self.interpreter or not os.path.exists(self.interpreter):
                self._baseline_ms = 0
            else:
                r = sandbox.run([self.interpreter, "-X", "utf8=1", "-c", "pass"],
                                time_limit_ms=5000, memory_limit_mb=0)
                self._baseline_ms = r.time_ms
        return self._baseline_ms

    def cleanup(self, workdir: Path) -> None:
        sandbox.rmtree_force(workdir)
