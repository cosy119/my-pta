"""校验题库：跑每道题的参考解，与**独立写好的**期望输出逐字节比对。

为什么要这一步
--------------
题库里的 `expected_stdout` 不是拿参考解跑出来的 —— 它由另一套独立实现预先算好
（Python 题用 node 写、数据结构题用 Python 的 oracle 写，都是另一门语言、另一套写法）。
参考解只是**被验证的一方**。两者对不上，就说明有一边错了 —— 这种题绝不入库。
（如果拿参考解现跑现填，就等于自己给自己判卷，永远是满分。）

`alt_solution` 是**第二套独立实现**（换算法或换 API）：
参考解和 alt 解必须**各自都撞过全部测试点**才算通过。
两道独立实现同时和期望值吻合，才能排除「共同盲区」。

支持的语言（按题目 `line` 自动挑 runner）
----------------------------------------
- `python` → CPython 解释执行
- `cpp` / `c` → 先 g++ / gcc 编译再跑（数据结构线：同一道题 C 和 C++ 都能交）
- `text`   → 理论题（选择 / 判断 / 填空），提交内容即答案，不启子进程

用法
----
    python tools/verify_bank.py              # 验全部题（三条线）
    python tools/verify_bank.py 素数          # 只验标题含「素数」的题
    python tools/verify_bank.py --py         # 只验 Python 线
    python tools/verify_bank.py --py --only 二进制统计
                                             # 增量模式：标题/分节/标签任一命中才验
                                             # （本地迭代用，全量留给 CI 兜底）
    python tools/verify_bank.py --ds         # 只验数据结构线
    python tools/verify_bank.py --linux      # 只验 Linux 线
    python tools/verify_bank.py --quiet      # 只打印汇总和失败项
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
from app import config                                       # noqa: E402
from app.judge import sandbox                                # noqa: E402
from app.judge.compare import compare                        # noqa: E402
from app.judge.runner_base import Limits                     # noqa: E402
from app.judge.runner_cpp import LANG_SPECS, CompileRunner, canon_lang  # noqa: E402
from app.judge.runner_python import PythonRunner             # noqa: E402
from app.judge.runner_text import TextRunner                 # noqa: E402
from app.problems_bank import BANK_PROBLEMS                  # noqa: E402
from app.problems_bank_ds import DS_PROBLEMS                 # noqa: E402
from app.seed import CORE_PROBLEMS                           # noqa: E402

try:                                                         # Linux 线可能还没写
    from app.problems_bank_linux import LINUX_PROBLEMS
except ImportError:                                          # pragma: no cover
    LINUX_PROBLEMS = []

try:                                                         # 技巧特训章（两线）
    from app.problems_bank_py_tricks import PY_TRICKS_PROBLEMS
    from app.problems_bank_ds_tricks import DS_TRICKS_PROBLEMS
except ImportError:                                          # pragma: no cover
    PY_TRICKS_PROBLEMS = []
    DS_TRICKS_PROBLEMS = []

try:                                                         # 理论题章（两线，2026-10-19）
    from app.problems_bank_py_theory import PY_THEORY_PROBLEMS
    from app.problems_bank_py_theory2 import PY_THEORY2_PROBLEMS
    from app.problems_bank_ds_theory import DS_THEORY_PROBLEMS
except ImportError:                                          # pragma: no cover
    PY_THEORY_PROBLEMS = []
    PY_THEORY2_PROBLEMS = []
    DS_THEORY_PROBLEMS = []

try:                                                         # 编程精练章（两线，2026-10-19）
    from app.problems_bank_py_prog import PY_PROG_PROBLEMS
    from app.problems_bank_ds_prog import DS_PROG_PROBLEMS
except ImportError:                                          # pragma: no cover
    PY_PROG_PROBLEMS = []
    DS_PROG_PROBLEMS = []

try:                                                         # 二进制统计族（Python 线，2026-10-20）
    from app.problems_bank_py_bits import PY_BITS_PROBLEMS
except ImportError:                                          # pragma: no cover
    PY_BITS_PROBLEMS = []

try:                                                         # C++ 基础线（2026-10-21）
    from app.problems_bank_cpp_theory import CPP_THEORY_PROBLEMS
    from app.problems_bank_cpp_theory2 import CPP_THEORY2_PROBLEMS
    from app.problems_bank_cpp_prog import CPP_PROG_PROBLEMS
    from app.problems_bank_cpp_tricks import CPP_TRICKS_PROBLEMS
except ImportError:                                          # pragma: no cover
    CPP_THEORY_PROBLEMS = []
    CPP_THEORY2_PROBLEMS = []
    CPP_PROG_PROBLEMS = []
    CPP_TRICKS_PROBLEMS = []

# C++ 基础编程题册（2026-10-21，按册生成，逐册可选 —— 单册缺失不该拖垮整线）
CPP_BASIC_BANKS: list[list[dict]] = []
for _n in range(1, 9):
    try:
        _mod = __import__("app.problems_bank_cpp_basic%d" % _n, fromlist=["x"])
        CPP_BASIC_BANKS.append(getattr(_mod, "CPP_BASIC%d_PROBLEMS" % _n))
    except Exception:                                        # pragma: no cover
        pass
CPP_BASIC_PROBLEMS = [p for b in CPP_BASIC_BANKS for p in b]

# ★ CORE 必须并进来。它住在 `app/seed.py` 而不是 `problems_bank.py`，
#   曾经因此完全落在对拍范围之外 —— SEED_PROBLEMS = CORE + BANK + DS + LINUX，
#   而这里只验了 BANK，于是 CORE 那几道题**连单撞都没有**（2026-10-13 发现）。
LINES = (
    ("py", "Python 线", CORE_PROBLEMS + BANK_PROBLEMS + PY_TRICKS_PROBLEMS
                        + PY_THEORY_PROBLEMS + PY_THEORY2_PROBLEMS + PY_PROG_PROBLEMS
                        + PY_BITS_PROBLEMS),
    ("ds", "数据结构线（C/C++）", DS_PROBLEMS + DS_TRICKS_PROBLEMS
                                  + DS_THEORY_PROBLEMS + DS_PROG_PROBLEMS),
    ("cpp", "C++ 基础线", CPP_TRICKS_PROBLEMS + CPP_THEORY_PROBLEMS
                          + CPP_THEORY2_PROBLEMS + CPP_PROG_PROBLEMS
                          + CPP_BASIC_PROBLEMS),
    ("linux", "Linux 线（理论题）", LINUX_PROBLEMS),
)


def make_runner(prob: dict, cfg):
    """按题目声明挑 runner —— 和 worker.build_runner 同一套判断。"""
    line = str(prob.get("line") or "python").strip().lower()
    if line in ("text", "choice", "theory"):
        return TextRunner()
    canon = canon_lang(line)
    if canon:
        spec = LANG_SPECS[canon]
        key = prob.get("ref_interpreter") or spec["compiler_key"]
        return CompileRunner(canon, cfg.compiler_path(key), spec["title"])
    label = prob.get("ref_interpreter") or "py313"
    return PythonRunner(cfg.interpreter_path(label), label)


def run_one_solution(solution: str, prob: dict, cfg, workdir: Path,
                     tag: str) -> tuple[int, list[str]]:
    """跑一套解，返回 (通过数, 失败说明)。

    注意：**不在这里删目录**。同一套解复用同一个工作目录（prepare 会覆盖源文件），
    只在整轮开始/结束时各清一次 —— 否则 50+ 道题会累计上百次删除，
    既慢又容易撞上外层的批量删除保护。
    """
    workdir.mkdir(parents=True, exist_ok=True)

    runner = make_runner(prob, cfg)
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
        stdin_bytes = c["stdin"].encode("utf-8")
        res = runner.run_case(workdir, stdin_bytes, limits)

        # ★ TLE 给一次重试 —— 只在**对拍工具**里，真实判题绝不这么做。
        #
        #   理由：本机（Windows + 两套杀软）**启动一个进程本身就要 160~400 ms**
        #   （实测：一个立刻 return 0 的空 C 程序也要 164 ms，Python 起解释器要 362 ms）。
        #   于是时间限制卡在临界的题会偶发 TLE，那是环境的锅、不是解法的锅 ——
        #   曾经在 204 题全量对拍里随机撞到一次（同一份解单独重跑 5/5 通过）。
        #
        #   只有**两次都 TLE** 才算真 TLE（真死循环照样抓得住），
        #   重试通过会打一行提示，免得把「环境抖动」和「真超时」混为一谈。
        if res.verdict == "TLE":
            retry = runner.run_case(workdir, stdin_bytes, limits)
            if retry.verdict != "TLE":
                print("    [%s] 测试点 %d：首次 TLE（%d ms）→ 重试通过（%d ms）"
                      "，属本机进程启动开销，非解法问题"
                      % (tag, i + 1, res.time_ms, retry.time_ms))
                sys.stdout.flush()
                res = retry

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


_LANG_TAG = {"python": "py ", "cpp": "c++", "c": "c  ", "text": "问 "}


def _lang_tag(p: dict) -> str:
    return _LANG_TAG.get(str(p.get("line") or "python").lower(), "?  ")


def _match_only(p: dict, key: str) -> bool:
    """--only 的命中规则：标题 / 分节 / 标签任一包含即命中。

    比老的位置参数（只匹配标题）宽 —— 出题时一族题共用一个标签或分节，
    一个词就能把整族捞出来做增量对拍。
    """
    if key in p["title"]:
        return True
    if key in str(p.get("section") or ""):
        return True
    return any(key in str(t) for t in (p.get("tags") or []))


def pick_lines() -> list[tuple[str, str, list[dict]]]:
    """按命令行开关挑要验的线（都不写就全验）。"""
    want = [t for t, _n, _p in LINES if ("--" + t) in sys.argv]
    if not want:
        return list(LINES)
    return [(t, n, p) for t, n, p in LINES if t in want]


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    quiet = "--quiet" in sys.argv
    key = args[0] if args else ""
    # --only 增量模式：与位置参数等价，但匹配面更宽（标题/分节/标签）。
    # 两者都给时取 --only（它是有意写的增量意图）。
    only = None
    if "--only" in sys.argv:
        i = sys.argv.index("--only")
        if i + 1 < len(sys.argv):
            only = sys.argv[i + 1]
    if only:
        key = only

    lines = pick_lines()
    probs: list[tuple[int, dict]] = []
    for _tag, _name, bank in lines:
        for p in bank:
            if key and only:
                hit = _match_only(p, key)
            elif key:
                hit = key in p["title"]
            else:
                hit = True
            if hit:
                probs.append((len(probs) + 1, p))
    if not probs:
        print("没有匹配的题目（检查一下筛选参数）")
        return 1

    cfg = config.get()
    # ★ 自己的临时目录**必须**落在判题根目录之外。
    #   原因：服务每次启动都会 `clean_tmp_root()` 把判题根目录下的所有子目录删干净
    #   （那是崩溃兜底清理）。对拍脚本如果也住在里面，只要此时碰巧有服务在跑
    #   （或服务在这中间启动过一次），编译出来的 main.py 就会被顺手删掉，
    #   表现为一连串莫名其妙的 `can't open file ... main.py` RE。
    # ★ 两份对拍**绝不能并发共用同一目录**（2026-10-15 踩到：另一窗口同时跑
    #   --ds，两边互相覆盖 ref/alt 里的 main.py，报 PermissionError）。
    #   并发时用 `PTA_VERIFY_TMP` 给自己起个独立目录名。
    base = Path(os.environ.get("PTA_VERIFY_TMP") or (Path(cfg.tmp_judge).parent / "verify_bank"))
    ref_dir = base / "ref"
    alt_dir = base / "alt"
    sandbox.rmtree_force(ref_dir)
    sandbox.rmtree_force(alt_dir)

    total_n = 0            # 测试点总数
    ref_pass_n = 0         # 参考解通过的测试点
    bad: list[str] = []
    no_alt: list[str] = []

    print("=" * 82)
    print("题库校验：参考解 / 第二套独立实现  双撞期望输出")
    print("本次覆盖：" + "、".join("%s（%d 题）" % (n, len(b)) for _t, n, b in lines))
    print("=" * 82)

    try:
        for idx, p in probs:
            ref_ok, alt_ok, n, fails = verify_one(idx, p, cfg, ref_dir, alt_dir)
            total_n += n
            ref_pass_n += ref_ok

            ok_all = (ref_ok == n) and (alt_ok in (-1, n))
            flag = "✅" if ok_all else "❌"
            if alt_ok == -1:
                # 理论题（line=text）的「参考解」就是答案本身，没有第二套实现可言，
                # 不算「漏了 alt」—— 它们的反向验证在 tools/selftest_theory.py 里做
                if str(p.get("line") or "") != "text":
                    no_alt.append(p["title"])
                alt_txt = "  alt  --"
            else:
                alt_txt = "  alt %d/%d" % (alt_ok, n)

            if not quiet or not ok_all:
                print("%s [%3d] %s %-30s 满分 %-4s 参考 %d/%d%s"
                      % (flag, idx, _lang_tag(p), p["title"],
                         p.get("total_score", 100), ref_ok, n, alt_txt))

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
