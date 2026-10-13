"""校验题库：跑每道题的参考解，与**独立写好的**期望输出逐字节比对。

为什么要这一步
--------------
题库里的 `expected_stdout` 是先用 **node 独立实现**算好的（另一门语言、另一套写法），
Python 参考解只是**被验证的一方**。两者对不上，就说明有一边错了 —— 这种题绝不入库。
（如果拿参考解现跑现填，就等于自己给自己判卷，永远是满分。）

`alt_solution` 是**第二套独立实现**（换算法或换 API）：
参考解和 alt 解必须**各自都撞过全部测试点**才算通过。
两道独立实现同时和期望值吻合，才能排除「共同盲区」。

用法
----
    python tools/verify_bank.py              # 验全部题
    python tools/verify_bank.py 素数          # 只验标题含「素数」的题
    python tools/verify_bank.py --quiet      # 只打印汇总和失败项
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

from app import config                               # noqa: E402
from app.judge import sandbox                        # noqa: E402
from app.judge.compare import compare                # noqa: E402
from app.judge.runner_base import Limits             # noqa: E402
from app.judge.runner_python import PythonRunner     # noqa: E402
from app.problems_bank import BANK_PROBLEMS          # noqa: E402


def run_one_solution(solution: str, prob: dict, cfg, workdir: Path,
                     tag: str) -> tuple[int, list[str]]:
    """跑一套解，返回 (通过数, 失败说明)。

    注意：**不在这里删目录**。同一套解复用同一个工作目录（prepare 会覆盖 main.py），
    只在整轮开始/结束时各清一次 —— 否则 50+ 道题会累计上百次删除，
    既慢又容易撞上外层的批量删除保护。
    """
    workdir.mkdir(parents=True, exist_ok=True)

    runner = PythonRunner(cfg.interpreter_path("py313"), "py313")
    ok, msg = runner.prepare(solution, workdir)
    if not ok:
        return 0, ["    [%s] 没跑起来：\n%s" % (tag, msg)]

    limits = Limits(
        time_ms=int(prob.get("time_limit_ms") or 1000),
        memory_mb=int(prob.get("memory_limit_mb") or 256),
        max_output_bytes=cfg.max_output_bytes,
        kill_grace_ms=cfg.kill_grace_ms,
    )
    checker = prob.get("checker", "standard")
    eps = float(prob.get("float_eps") or 1e-6)

    passed, fails = 0, []
    for i, c in enumerate(prob["cases"]):
        res = runner.run_case(workdir, c["stdin"].encode("utf-8"), limits)
        if res.verdict != "OK":
            fails.append("    [%s] 测试点 %d：运行异常 %s  %s"
                         % (tag, i + 1, res.verdict, (res.detail or "")[:120]))
            continue
        cmp = compare(c["expected_stdout"], res.stdout, checker, eps)
        if cmp.ok:
            passed += 1
        else:
            fails.append(
                "    [%s] 测试点 %d 对不上（%s）\n"
                "      stdin    = %r\n      期望输出 = %r\n      解得     = %r"
                % (tag, i + 1, cmp.detail, c["stdin"],
                   c["expected_stdout"], res.stdout.decode("utf-8", "replace")))

    return passed, fails


def verify_one(idx: int, prob: dict, cfg, ref_dir: Path,
               alt_dir: Path) -> tuple[int, int, int, list[str]]:
    """返回 (参考解通过数, alt 通过数, 测试点总数, 失败说明)。

    没写 `alt_solution` 的题，alt 通过数记成 -1（表示「不适用」）。
    """
    n = len(prob["cases"])

    ref_ok, fails = run_one_solution(
        prob["reference_solution"], prob, cfg, ref_dir, "参考解")

    alt_ok = -1
    if prob.get("alt_solution"):
        alt_ok, alt_fails = run_one_solution(
            prob["alt_solution"], prob, cfg, alt_dir, "alt解")
        fails += alt_fails

    return ref_ok, alt_ok, n, fails


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    quiet = "--quiet" in sys.argv
    key = args[0] if args else ""

    probs = [(i, p) for i, p in enumerate(BANK_PROBLEMS, 1)
             if not key or key in p["title"]]

    cfg = config.get()
    base = Path(cfg.tmp_judge)
    ref_dir = base / "verify_bank_ref"
    alt_dir = base / "verify_bank_alt"
    sandbox.rmtree_force(ref_dir)
    sandbox.rmtree_force(alt_dir)

    total_n = 0            # 测试点总数
    ref_pass_n = 0         # 参考解通过的测试点
    bad: list[str] = []
    no_alt: list[str] = []

    print("=" * 82)
    print("题库校验：参考解 / 第二套独立实现  双撞期望输出")
    print("=" * 82)

    try:
        for idx, p in probs:
            ref_ok, alt_ok, n, fails = verify_one(idx, p, cfg, ref_dir, alt_dir)
            total_n += n
            ref_pass_n += ref_ok

            ok_all = (ref_ok == n) and (alt_ok in (-1, n))
            flag = "✅" if ok_all else "❌"
            if alt_ok == -1:
                no_alt.append(p["title"])
                alt_txt = "  alt  --"
            else:
                alt_txt = "  alt %d/%d" % (alt_ok, n)

            if not quiet or not ok_all:
                print("%s [%2d] %-18s 满分 %-3s 参考 %d/%d%s"
                      % (flag, idx, p["title"], p.get("total_score", 100),
                         ref_ok, n, alt_txt))

            if fails or not ok_all:
                bad.append(p["title"])
                for f in fails:
                    print(f)
                sys.stdout.flush()
    finally:
        sandbox.rmtree_force(ref_dir)
        sandbox.rmtree_force(alt_dir)

    print("=" * 82)
    print("题目数：%d    测试点总数：%d    参考解通过：%d"
          % (len(probs), total_n, ref_pass_n))
    if no_alt:
        print("未提供第二套实现（只单撞）：%s" % "、".join(no_alt))
    if bad:
        print("★ 有问题的题：%s" % "、".join(bad))
    else:
        print("全部通过 ✅")
    print("=" * 82)
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
