"""C / C++ 判题 runner（编译型）。

流程（和解释型不同的是多了一步编译）
------------------------------------
1. prepare：把源码落盘 → 用 gcc / g++ 编译成可执行文件
   - 编译**只做一次**，编完 N 个测试点复用同一个可执行文件
   - 编译失败 → 编译器原文回传当 CE 信息（学生最需要看到的就是编译器原话）
2. run_case：跑可执行文件，受 sandbox 的时限 / 内存 / 输出上限约束

★ 同一道题同时支持 C 和 C++
---------------------------
数据结构教材是 **C 语言版**，但很多人习惯用 C++ 写（`cin`、`vector`、`string`）。
所以这两种不该被当成两门语言来出题 —— 出题人写一遍题面，答题人自己挑用哪门。

做法：按提交里带的 `lang` 选编译器与源文件后缀，
    c   → gcc + main.c   + -std=gnu11
    cpp → g++ + main.cpp + -std=c++17
两条路都走同一个类，只有 lang spec 不同。

★ 三条写死在这里的坑
--------------------
1. **编译阶段绝不能套用题目的内存限额**。g++ 自己就要吃几十上百 MB，
   按题目的 256 MB 去限它，带个 `<iostream>` + STL 的小程序都可能崩，
   表现为莫名其妙的 CE。这里给编译单独放宽到 1 GB / 20 秒。
2. **可执行文件的名字分平台**：Windows 上是 `.exe`，Linux 上没有后缀。
   写死 `main` 在 Windows 上会「编译成功但跑不起来」，报找不到文件。
3. **C 与 C++ 的可执行文件必须分开命名**。共用 `main` 的话，
   同一份工作目录里先编过 C 再编 C++（或反过来）会出现「跑了上一次的产物」，
   判题结果完全是错的 —— 而且这种错极难发现。
"""
from __future__ import annotations

import os
from pathlib import Path

from . import sandbox
from .runner_base import CaseResult, Limits, verdict_from_run

# 平台相关的可执行文件后缀
_EXE_SUFFIX = ".exe" if os.name == "nt" else ""

# 语言规格：源文件名 / 编译开关 / 编译器配置键 / 人看的名字
LANG_SPECS: dict[str, dict] = {
    "cpp": {
        "src": "main.cpp",
        "exe": "main_cpp" + _EXE_SUFFIX,
        "flags": ["-O2", "-pipe", "-std=c++17"],
        "compiler_key": "gpp",
        "title": "C++ (g++)",
        "std": "c++17",
    },
    "c": {
        "src": "main.c",
        "exe": "main_c" + _EXE_SUFFIX,
        "flags": ["-O2", "-pipe", "-std=gnu11"],
        "compiler_key": "gcc",
        "title": "C (gcc)",
        "std": "gnu11",
    },
}

# 别名 → 规范语言名（前端/种子题里可能写成各种样子）
LANG_ALIAS = {
    "cpp": "cpp", "c++": "cpp", "g++": "cpp", "gpp": "cpp", "cpp17": "cpp",
    "c": "c", "gcc": "c", "gnu11": "c", "c11": "c", "c99": "c",
}

# 编译阶段单独的额度（★ 不能沿用题目的限额，见模块 docstring）
COMPILE_TIME_MS = 20000
COMPILE_MEMORY_MB = 1024

# 编译期的干净环境：让 gcc/g++ 的错误信息不要因本机 locale 变成乱码
_COMPILE_ENV = {
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
}


def canon_lang(lang: str) -> str:
    """把各种写法收敛成 `c` / `cpp`；认不出返回空串。"""
    return LANG_ALIAS.get(str(lang or "").strip().lower(), "")


def _read_text(data: bytes) -> str:
    return (data or b"").decode("utf-8", "replace").strip()


class CompileRunner:
    """用 gcc / g++ 编译，再跑可执行文件。

    `lang` 决定用哪套规格（源文件后缀 / 标准 / 编译器），见 `LANG_SPECS`。
    """

    def __init__(self, lang: str, compiler: str, label: str = ""):
        self.lang = canon_lang(lang) or "cpp"
        self.spec = LANG_SPECS[self.lang]
        self.compiler = compiler or ""
        self.label = label or self.spec["title"]
        self._built: Path | None = None

    # ---------- 编译 ----------
    def prepare(self, code: str, workdir: Path) -> tuple[bool, str]:
        workdir = Path(workdir)
        workdir.mkdir(parents=True, exist_ok=True)
        src = workdir / self.spec["src"]
        src.write_text(code or "", encoding="utf-8")

        if not self.compiler or not os.path.exists(self.compiler):
            return False, format_compiler_missing(self.lang, self.compiler)

        exe = workdir / self.spec["exe"]
        # ★ 用绝对路径给源文件：cwd 已经是 workdir，但 Windows 上
        # 相对路径配合某些 gcc 包装脚本会被解析歪，写全最稳
        cmd = [self.compiler, *self.spec["flags"], "-o", str(exe), str(src)]

        r = sandbox.run(cmd, cwd=workdir, env=_COMPILE_ENV,
                        time_limit_ms=COMPILE_TIME_MS,
                        memory_limit_mb=COMPILE_MEMORY_MB,
                        max_output_bytes=262144)

        if r.timed_out:
            return False, (f"编译超过 {COMPILE_TIME_MS // 1000} 秒还没结束，已中断"
                           "（代码里是不是有巨型模板或死循环的 constexpr？）")

        if r.exit_code != 0 or not exe.exists():
            detail = _read_text(r.stderr) or _read_text(r.stdout) or "编译器没有给出错误信息"
            return False, detail

        self._built = exe
        # 编译器的**警告**也值得看 —— 很多「本机跑对、交上去错」的根因就写在警告里
        return True, _read_text(r.stderr)

    # ---------- 跑单个测试点 ----------
    def run_case(self, workdir: Path, stdin_bytes: bytes, limits: Limits) -> CaseResult:
        exe = self._built or (Path(workdir) / self.spec["exe"])
        if not Path(exe).exists():
            return CaseResult(verdict="IE", detail="可执行文件不存在，编译阶段可能没成功")

        r = sandbox.run(
            [str(exe)],
            stdin_bytes=stdin_bytes,
            cwd=workdir,
            env=_COMPILE_ENV,
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

    def cleanup(self, workdir: Path) -> None:
        self._built = None
        sandbox.rmtree_force(workdir)


# 兼容旧名字（之前只有 C++ 一份实现，别处可能还在 import）
CppRunner = CompileRunner


def format_compiler_missing(lang: str, compiler: str) -> str:
    """给「机器上根本没有编译器」这种情况一句人话。"""
    spec = LANG_SPECS.get(canon_lang(lang) or "cpp", LANG_SPECS["cpp"])
    key = spec["compiler_key"]
    who = spec["title"]
    return (
        f"找不到 {who} 编译器。\n\n"
        f"当前配置：{compiler!r}（config/settings.toml 的 [compilers] {key}）\n\n"
        "本机装的 MinGW-w64 通常在 D:\\Programs\\mingw64\\bin\\ 下，"
        f"把 {key}.exe 的完整路径写进 [compilers] {key} 即可；\n"
        "Linux 上装一下 gcc 就行：sudo dnf install gcc-c++（C 只要 gcc）。"
    )
