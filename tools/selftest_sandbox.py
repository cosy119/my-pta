"""跨平台沙箱自检 —— 部署到 Linux 云平台后**在那个容器里跑一遍**。

Windows 上跑这个脚本会只测 Windows 分支（Job Object）；
Linux 上（Docker 容器 / Render shell）跑就会测 setrlimit + killpg 分支。

为什么单独一个脚本：`tools/selfcheck.py` 是判题内核的完整回归，跑得久；
这个只盯「沙箱能不能在这台机器上正确限内存 / 杀进程树」，几秒钟出结果，
适合部署后第一时间确认环境 OK。

用法：
    python tools/selftest_sandbox.py
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.judge import sandbox                                    # noqa: E402
from app.judge.runner_base import verdict_from_run               # noqa: E402

_passed = 0
_failed = 0


def check(name: str, ok: bool, extra: str = "") -> None:
    global _passed, _failed
    if ok:
        _passed += 1
        print(f"  [OK]   {name}" + (f"  -- {extra}" if extra else ""))
    else:
        _failed += 1
        print(f"  [FAIL] {name}" + (f"  -- {extra}" if extra else ""))


def py() -> list[str]:
    return [sys.executable, "-X", "utf8=1", "-u", "prog.py"]


def main() -> int:
    import tempfile

    print("=" * 72)
    print("  沙箱跨平台自检")
    print(f"  平台: {'Windows' if sandbox._IS_WINDOWS else 'POSIX/Linux'}")
    print(f"  Python: {sys.version.split()[0]}  @ {sys.executable}")
    print("=" * 72)

    work = Path(tempfile.mkdtemp(prefix="pta_sbtest_"))
    print(f"\n临时目录: {work}")

    try:
        # ---------- 1 正常跑 ----------
        print("\n[1] 正常程序")
        (work / "prog.py").write_text(
            "import sys\na, b = map(int, sys.stdin.read().split())\nprint(a + b)\n",
            encoding="utf-8")
        r = sandbox.run(py(), stdin_bytes=b"3 4\n", cwd=work, time_limit_ms=10000,
                        memory_limit_mb=256)
        check("正常结束（exit 0）", r.exit_code == 0, f"exit={r.exit_code}")
        check("输出正确", r.stdout.strip() == b"7", repr(r.stdout))
        check("没判 MLE", not r.mem_exceeded, f"峰值 {r.mem_kb} KB")
        check("记到了内存峰值（> 0）", r.mem_kb > 0, f"{r.mem_kb} KB")

        # ---------- 2 超时 + 杀进程树 ----------
        print("\n[2] 超时：进程树必须被杀干净")
        (work / "prog.py").write_text(
            "import subprocess, sys, time\n"
            "# 起一个孙进程，看超时后它会不会被带走\n"
            "subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(300)'])\n"
            "time.sleep(300)\n", encoding="utf-8")
        t0 = time.time()
        r = sandbox.run(py(), cwd=work, time_limit_ms=1500, memory_limit_mb=256)
        dt = time.time() - t0
        check("判 TLE", r.timed_out, f"{r.time_ms} ms")
        check("没拖太久就返回（< 8s）", dt < 8, f"{dt:.1f}s")
        verdict, detail, _ = verdict_from_run(r)
        check("verdict_from_run 给出 TLE", verdict == "TLE", detail[:60])

        # ---------- 3 爆内存 ----------
        print("\n[3] 爆内存：必须判 MLE，不是 RE")
        (work / "prog.py").write_text(
            "x = []\n"
            "for _ in range(60):\n"
            "    x.append(b' ' * (10 * 1024 * 1024))\n"
            "print('done')\n", encoding="utf-8")
        r = sandbox.run(py(), cwd=work, time_limit_ms=30000, memory_limit_mb=128)
        verdict, detail, _ = verdict_from_run(r)
        check("判 MLE", verdict == "MLE",
              f"{verdict} 峰值 {r.mem_kb // 1024} MB / 限额 128 MB")
        check("峰值确实顶到限额附近", r.mem_kb * 1024 >= 128 * 1024 * 1024 * 0.8,
              f"{r.mem_kb // 1024} MB")

        # ---------- 4 反向：主动 exit(1) 不该误判 MLE ----------
        print("\n[4] 反向验证：主动崩溃不误判 MLE")
        (work / "prog.py").write_text("import sys\nsys.exit(1)\n", encoding="utf-8")
        r = sandbox.run(py(), cwd=work, time_limit_ms=10000, memory_limit_mb=256)
        verdict, detail, _ = verdict_from_run(r)
        check("判 RE（不是 MLE）", verdict == "RE",
              f"{verdict} 峰值 {r.mem_kb // 1024} MB")

        # ---------- 5 输出超限 ----------
        print("\n[5] 输出超限")
        (work / "prog.py").write_text(
            "print('x' * 300000)\n", encoding="utf-8")
        r = sandbox.run(py(), cwd=work, time_limit_ms=10000,
                        memory_limit_mb=256, max_output_bytes=1024)
        check("截断并打标", r.truncated and len(r.stdout) == 1024,
              f"truncated={r.truncated} len={len(r.stdout)}")

        # ---------- 6 乱写文件也不该影响别的用例 ----------
        print("\n[6] 清理能力")
        (work / "junk").mkdir(exist_ok=True)
        (work / "junk" / "a.txt").write_text("x" * 100, encoding="utf-8")
        ok = sandbox.rmtree_force(work)
        check("rmtree_force 能删干净", ok and not work.exists())

    finally:
        if work.exists():
            sandbox.rmtree_force(work)

    print("\n" + "=" * 72)
    print(f"通过 {_passed} 项，失败 {_failed} 项")
    print("=" * 72)
    return 0 if _failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
