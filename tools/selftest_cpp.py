"""编译型判题自测：C 与 C++ 两条通道都要真跑一遍。

为什么单开一个脚本
------------------
数据结构教材是 **C 语言版**，但平台上同一道题允许 C / C++ 任选其一提交
（见 `app/judge/runner_cpp.py`）。两条通道的差异全在编译那一步：

| | 源文件 | 编译器 | 标准 |
|---|---|---|---|
| C++ | `main.cpp` | g++ | `-std=c++17` |
| C   | `main.c`   | gcc | `-std=gnu11` |

如果只测了 C++，C 这条通道出问题（编译器路径没配、源文件后缀写错、
两个产物互相覆盖）是**不会有人发现**的 —— 直到学生用 C 交题被判 CE。

检查项（每项都真跑）
--------------------
1. C++ 正常程序 → AC
2. C   正常程序 → AC
3. C++ 编译错误 → CE，且错误信息里带编译器原话
4. C   编译错误 → CE
5. C++ 答案错 → WA（判定链路要判得出来，不能只认 AC）
6. C   运行时超时 → TLE
7. C   `stdio` 与 C++ `iostream` 程序在**同一工作目录**里先后编译，
   各自的产物不能串（这是最容易踩且最难发现的坑）
8. 编译器路径不存在时的报错是不是人话（不是一段 traceback）

用法
----
    python tools/selftest_cpp.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

import _console                                                   # noqa: E402
import _testdb                                                   # noqa: E402  ★ 别让自检写进真实库
from app import config                                        # noqa: E402
from app.judge import sandbox                                 # noqa: E402
from app.judge.compare import compare                         # noqa: E402
from app.judge.runner_base import Limits                      # noqa: E402
from app.judge.runner_cpp import LANG_SPECS, CompileRunner, canon_lang  # noqa: E402

CFG = config.get()
BASE = Path(CFG.tmp_judge) / "selftest_cpp"

PASSED: list[str] = []
FAILED: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    (PASSED if ok else FAILED).append(name)
    print("%s %s%s" % ("✅" if ok else "❌", name, ("  → " + detail) if detail else ""))
    sys.stdout.flush()


def make(lang: str) -> CompileRunner:
    spec = LANG_SPECS[lang]
    return CompileRunner(lang, CFG.compiler_path(spec["compiler_key"]), spec["title"])


def run(runner: CompileRunner, code: str, stdin: str, workdir: Path,
        time_ms: int = 2000, mem_mb: int = 256):
    """编译 + 跑第 1 个用例，返回 (CaseResult, prepare 信息)。"""
    workdir.mkdir(parents=True, exist_ok=True)
    ok, msg = runner.prepare(code, workdir)
    if not ok:
        return None, msg
    limits = Limits(time_ms=time_ms, memory_mb=mem_mb,
                    max_output_bytes=CFG.max_output_bytes,
                    kill_grace_ms=CFG.kill_grace_ms)
    return runner.run_case(workdir, stdin.encode("utf-8"), limits), msg


# --------------------------------------------------------------------- #
#  1 / 2 · 两条通道都能 AC
# --------------------------------------------------------------------- #
CPP_OK = r'''#include <iostream>
#include <string>
using namespace std;
int main() {
    string s;
    if (!(cin >> s)) return 0;
    // 反转输出（用 C++ 的 string）
    for (int i = (int)s.size() - 1; i >= 0; i--) cout << s[i];
    cout << "\n";
    return 0;
}
'''

C_OK = r'''#include <stdio.h>
#include <string.h>
int main(void) {
    char s[256];
    if (scanf("%255s", s) != 1) return 0;
    int n = (int)strlen(s);
    for (int i = n - 1; i >= 0; i--) putchar(s[i]);
    putchar('\n');
    return 0;
}
'''

# --------------------------------------------------------------------- #
#  3 / 4 · 编译错误
# --------------------------------------------------------------------- #
CPP_CE = r'''#include <iostream>
int main() {
    std::cout << "missing semicolon"    // ★ 少分号
    return 0;
}
'''

C_CE = r'''#include <stdio.h>
int main(void) {
    printf("%d\n", ;     // ★ 语法错
    return 0;
}
'''

# --------------------------------------------------------------------- #
#  5 · 答案错（本机不该只认 AC）
# --------------------------------------------------------------------- #
CPP_WA = r'''#include <iostream>
int main() { std::cout << "definitely wrong\n"; return 0; }
'''

# --------------------------------------------------------------------- #
#  6 · 死循环 → TLE
# --------------------------------------------------------------------- #
C_TLE = r'''#include <stdio.h>
int main(void) {
    volatile long long x = 0;
    while (1) x++;            /* ★ 明显的死循环 */
    return 0;
}
'''

# --------------------------------------------------------------------- #
#  7 · 同一目录不串（C 与 C++ 各编一份，产物必须分开）
# --------------------------------------------------------------------- #
CPP_TAG = r'''#include <iostream>
int main() { std::cout << "I_AM_CPP\n"; return 0; }
'''
C_TAG = r'''#include <stdio.h>
int main(void) { printf("I_AM_C\n"); return 0; }
'''


def main() -> int:
    sandbox.rmtree_force(BASE)
    print("=" * 78)
    print("编译型判题自测（C / C++ 两条通道）")
    print("编译器： gpp=%s" % CFG.compiler_path("gpp"))
    print("         gcc=%s" % CFG.compiler_path("gcc"))
    print("=" * 78)

    try:
        # --- 1 / 2 ---
        res, _ = run(make("cpp"), CPP_OK, "hello\n", BASE / "cpp_ok")
        check("C++ 正常程序判 AC",
              res is not None and res.verdict == "OK"
              and compare("olleh\n", res.stdout).ok,
              "" if res is None else "%s / %r" % (res.verdict, res.stdout[:40]))

        res, _ = run(make("c"), C_OK, "hello\n", BASE / "c_ok")
        check("C   正常程序判 AC",
              res is not None and res.verdict == "OK"
              and compare("olleh\n", res.stdout).ok,
              "" if res is None else "%s / %r" % (res.verdict, res.stdout[:40]))

        # --- 3 / 4 ---
        res, msg = run(make("cpp"), CPP_CE, "", BASE / "cpp_ce")
        check("C++ 语法错判 CE，且带编译器原话",
              res is None and "error" in msg.lower(),
              (msg or "").splitlines()[0][:70] if msg else "没有错误信息")

        res, msg = run(make("c"), C_CE, "", BASE / "c_ce")
        check("C   语法错判 CE，且带编译器原话",
              res is None and "error" in msg.lower(),
              (msg or "").splitlines()[0][:70] if msg else "没有错误信息")

        # --- 5 ---
        res, _ = run(make("cpp"), CPP_WA, "hello\n", BASE / "cpp_wa")
        ok = (res is not None and res.verdict == "OK"
              and not compare("olleh\n", res.stdout).ok)
        check("C++ 答案错判 WA（不是只看 AC）", ok,
              "" if res is None else repr(res.stdout[:30]))

        # --- 6 ---
        res, _ = run(make("c"), C_TLE, "", BASE / "c_tle", time_ms=700)
        check("C   死循环判 TLE（整棵进程树被杀掉）",
              res is not None and res.verdict == "TLE",
              "" if res is None else res.verdict)

        # --- 7 · 同一目录、两个语言，产物不串 ---
        shared = BASE / "shared"
        shared.mkdir(parents=True, exist_ok=True)
        r_cpp = make("cpp")
        r_c, _ = r_cpp, None
        ok1, m1 = r_cpp.prepare(CPP_TAG, shared)
        res1 = r_cpp.run_case(shared, b"", Limits(
            time_ms=2000, memory_mb=256,
            max_output_bytes=CFG.max_output_bytes, kill_grace_ms=CFG.kill_grace_ms))
        r_c = make("c")
        ok2, m2 = r_c.prepare(C_TAG, shared)
        res2 = r_c.run_case(shared, b"", Limits(
            time_ms=2000, memory_mb=256,
            max_output_bytes=CFG.max_output_bytes, kill_grace_ms=CFG.kill_grace_ms))
        # 再跑一次 C++ 的产物：它必须还是 C++ 那份（没被 C 覆盖）
        res3 = r_cpp.run_case(shared, b"", Limits(
            time_ms=2000, memory_mb=256,
            max_output_bytes=CFG.max_output_bytes, kill_grace_ms=CFG.kill_grace_ms))
        check("C 与 C++ 的产物在同目录下互不覆盖",
              ok1 and ok2
              and res1.stdout.strip() == b"I_AM_CPP"
              and res2.stdout.strip() == b"I_AM_C"
              and res3.stdout.strip() == b"I_AM_CPP",
              "cpp=%r c=%r cpp_again=%r" % (res1.stdout.strip(), res2.stdout.strip(),
                                            res3.stdout.strip()))

        # --- 8 · 编译器不存在时的报错是人话 ---
        bad = CompileRunner("cpp", "Z:/definitely/not/here/g++.exe", "C++ (g++)")
        ok, msg = bad.prepare("int main(){}", BASE / "no_compiler")
        check("编译器路径无效时给的是人话（不是 traceback）",
              (not ok) and ("找不到" in msg) and ("Traceback" not in msg),
              (msg or "").splitlines()[0][:70] if msg else "没有信息")

        # --- 附带：别名收敛 ---
        check("语言别名能收敛到规范名",
              canon_lang("c++") == "cpp" and canon_lang("GCC") == "c"
              and canon_lang("g++") == "cpp" and canon_lang("rust") == "")
    finally:
        sandbox.rmtree_force(BASE)

    print("=" * 78)
    print("通过 %d 项，失败 %d 项" % (len(PASSED), len(FAILED)))
    if FAILED:
        print("★ 失败项：%s" % "、".join(FAILED))
    else:
        print("全部通过 ✅")
    print("=" * 78)
    return 1 if FAILED else 0


if __name__ == "__main__":
    raise SystemExit(main())
