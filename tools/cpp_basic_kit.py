# -*- coding: utf-8 -*-
"""C++ 基础编程题「大规模加题」的共享框架。

为什么单独抽一层
----------------
`tools/gen_cpp_prog.py` 是 17 道精雕题的写法：每题手写 6 段字面量输入。
要做 300+ 道，必须把重复劳动压到框架里，让每个生成器只写 4 样东西：

  1. 题干（`stmt()` 拼装：题意 + 关键点）
  2. 测试数据（`cases()` + 程序化生成，固定 seed 可复现）
  3. Python oracle —— **必须独立于 C++ 解**，一律用笨办法（暴力枚举/字符串转换/直接模拟）
  4. 两套 C++ 解（solution / alt，实现路径不同，输出必须逐字节相同）

其余字段（subject/line/checker/score/cases 结构……）由 `build()` 统一填，
`sanity()` 做结构自检，`verify()` 真编真跑 600+ 次做逐字节对拍。

★ 铁律：oracle 绝不拿 C++ 解跑出来的结果回填 —— 那是自己给自己判卷。
★ 铁律：alt 不是改个变量名，是换一条实现路径（暴力↔公式、循环↔STL、手写↔库函数）。

用法（在各生成器里）
--------------------
    from cpp_basic_kit import *          # noqa
    PROBLEMS = []
    ...
    if __name__ == "__main__":
        cli(PROBLEMS, "app/problems_bank_cpp_basic1.py", "第一册：输入输出/运算/分支/循环/图形")
"""
from __future__ import annotations

import argparse
import concurrent.futures as futures
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GPP = r"D:\Programs\mingw64\bin\g++.exe"
CXXFLAGS = ["-std=c++17", "-O2"]
TMPDIR = ROOT / "data" / "tmp" / "cpp_basic"

SUBJECT = "cpp"
LINE = "cpp"

# 分值随难度走：低难度给基础分，高难度给加权分
SCORE_OF = {1: 10, 2: 12, 3: 14, 4: 16}
N_CASES = 6          # 每题固定 6 个测试点（前 2 个公开）


# ------------------------------------------------------------------ #
#  题干 / 数据 拼装
# ------------------------------------------------------------------ #
def stmt(desc: str, points=(), sample: str = "") -> str:
    """题意 + 关键点 + （可选）样例说明。

    desc    多段文字直接用 \\n\\n 分隔
    points  要点/易错清单，逐条加 '- '
    sample  额外追加的说明块（原样附在末尾）
    """
    s = desc.strip()
    if points:
        s += "\n\n**关键点**\n\n" + "\n".join("- " + str(x) for x in points)
    if sample:
        s += "\n\n" + sample.strip()
    return s


def cases(*blocks) -> list[str]:
    """把若干输入块规整成「每块都以换行结尾」的列表。"""
    out = []
    for b in blocks:
        b = str(b)
        out.append(b if b.endswith("\n") else b + "\n")
    return out


def lines(*rows) -> str:
    return "\n".join(str(r) for r in rows) + "\n"


def join_tokens(seq, sep=" ") -> str:
    return sep.join(str(x) for x in seq)


def nums(seq, sep=" ") -> str:
    return sep.join(str(x) for x in seq)


# ------------------------------------------------------------------ #
#  build：把「题目定义」变成评分系统认得的数据结构
# ------------------------------------------------------------------ #
def build(problems: list[dict]) -> list[dict]:
    out: list[dict] = []
    for p in problems:
        ins = p["inputs"]
        if callable(ins):
            ins = ins()
        if len(ins) != N_CASES:
            raise SystemExit("《%s》给了 %d 个测试点，本框架要求恰好 %d 个"
                             % (p["title"], len(ins), N_CASES))
        n_sample = int(p.get("samples", 2))
        cs = []
        for i, inp in enumerate(ins):
            inp = str(inp)
            if not inp.endswith("\n"):
                inp += "\n"
            exp = p["oracle"](inp)
            if not isinstance(exp, str):
                raise SystemExit("《%s》第 %d 个输入的 oracle 返回 %s（应为 str）"
                                 % (p["title"], i + 1, type(exp).__name__))
            if not exp.endswith("\n"):
                exp += "\n"
            is_s = i < n_sample
            cs.append({
                "stdin": inp,
                "expected_stdout": exp,
                "is_sample": 1 if is_s else 0,
                "kind": "sample" if is_s else "manual",
                "explanation": p.get("explanation", ""),
            })
        diff = int(p.get("difficulty", 2))
        out.append({
            "title": p["title"],
            "subject": SUBJECT,
            "line": LINE,
            "difficulty": diff,
            "total_score": int(p.get("score") or SCORE_OF.get(diff, 12)),
            "tags": list(p.get("tags", [])),
            "statement_md": p["statement_md"],
            "input_format": p.get("input_format", ""),
            "output_format": p.get("output_format", ""),
            "constraints_md": p.get("constraints_md", ""),
            "time_limit_ms": int(p.get("time_limit_ms", 2000)),
            "memory_limit_mb": int(p.get("memory_limit_mb", 256)),
            "checker": "standard",
            "float_eps": 1e-6,
            "origin": "manual",
            "status": "published",
            "source_section": p["section"],
            "ref_interpreter": "gpp",
            "reference_solution": p["solution"],
            "alt_solution": p["alt"],
            "cases": cs,
        })
    return out


# ------------------------------------------------------------------ #
#  结构自检
# ------------------------------------------------------------------ #
def sanity(probs: list[dict], *, max_per_section: int = 40) -> list[str]:
    bad: list[str] = []
    seen: dict[str, int] = {}
    by_sec: dict[str, int] = {}
    for i, p in enumerate(probs, 1):
        t = p["title"]
        if t in seen:
            bad.append("[%d] 标题重复：%s" % (i, t))
        seen[t] = i
        by_sec[p["source_section"]] = by_sec.get(p["source_section"], 0) + 1
        for k in ("statement_md", "input_format", "output_format", "constraints_md",
                  "reference_solution", "alt_solution", "source_section"):
            if not str(p.get(k) or "").strip():
                bad.append("[%d] %s 缺字段 %s" % (i, t, k))
        if p["subject"] != SUBJECT or p["line"] != LINE:
            bad.append("[%d] %s 的 subject/line 不是 cpp" % (i, t))
        if p["checker"] != "standard":
            bad.append("[%d] %s 的 checker 应为 standard" % (i, t))
        if p["difficulty"] not in (1, 2, 3, 4):
            bad.append("[%d] %s 难度 %s 不在 1~4" % (i, t, p["difficulty"]))
        if len(p["cases"]) != N_CASES:
            bad.append("[%d] %s 测试点数 %d ≠ %d" % (i, t, len(p["cases"]), N_CASES))
        if p["total_score"] <= 0:
            bad.append("[%d] %s 满分非法" % (i, t))
        # 无输入题（打印固定图形/常数表）的 stdin 只可能是空串或单个换行，
        # 期望输出也可能是单个换行（如「k = 0 时输出空行」），所以只拦「完全空」。
        for j, c in enumerate(p["cases"], 1):
            e = c["expected_stdout"]
            if e == "":
                bad.append("[%d] %s 第 %d 点期望输出是空字符串" % (i, t, j))
            if not e.endswith("\n"):
                bad.append("[%d] %s 第 %d 点期望输出没以换行结尾" % (i, t, j))
    for sec, n in sorted(by_sec.items()):
        if n < 6:
            bad.append("分节《%s》只有 %d 题，少于 6 题" % (sec, n))
        if n > max_per_section:
            bad.append("分节《%s》有 %d 题，超过上限 %d" % (sec, n, max_per_section))
    return bad


# ------------------------------------------------------------------ #
#  真编真跑：参考解 + alt 都必须过全部测试点
# ------------------------------------------------------------------ #
def _run_one(args):
    idx, title, which, src, cases_ = args
    key = hashlib.sha1((which + "\x00" + src).encode("utf-8")).hexdigest()[:12]
    TMPDIR.mkdir(parents=True, exist_ok=True)
    cpp = TMPDIR / ("p%03d_%s_%s.cpp" % (idx, which, key))
    exe = TMPDIR / ("p%03d_%s_%s.exe" % (idx, which, key))
    cpp.write_text(src, encoding="utf-8", newline="\n")
    r = subprocess.run([GPP] + CXXFLAGS + ["-o", str(exe), str(cpp)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        return ("COMPILE", idx, title, which, r.stderr[:900])
    errs = []
    for j, c in enumerate(cases_, 1):
        try:
            run = subprocess.run([str(exe)], input=c["stdin"], capture_output=True,
                                 text=True, encoding="utf-8", errors="replace", timeout=5)
        except subprocess.TimeoutExpired:
            errs.append((j, c["stdin"][:200], c["expected_stdout"][:200], "<超时>"))
            continue
        if run.stdout != c["expected_stdout"]:
            errs.append((j, c["stdin"][:200], c["expected_stdout"][:200], run.stdout[:200]))
    return ("OK" if not errs else "WA", idx, title, which, errs)


def verify(probs: list[dict], *, workers: int | None = None, quiet: bool = False) -> int:
    """返回失败条数。failure = 编译失败 + 任一测试点不一致。"""
    workers = workers or max(2, (os.cpu_count() or 4))
    jobs = []
    for i, p in enumerate(probs, 1):
        for which, key in (("solution", "reference_solution"), ("alt", "alt_solution")):
            jobs.append((i, p["title"], which, p[key], p["cases"]))
    fails = 0
    done = 0
    with futures.ThreadPoolExecutor(max_workers=workers) as ex:
        for kind, idx, title, which, payload in ex.map(_run_one, jobs):
            done += 1
            if kind == "OK":
                continue
            fails += 1
            if kind == "COMPILE":
                print("\n✗ [%d] %s / %s 编译失败\n%s" % (idx, title, which, payload))
            else:
                print("\n✗ [%d] %s / %s 有 %d 个测试点不一致" % (idx, title, which, len(payload)))
                for j, sin, exp, got in payload[:2]:
                    print("   第 %d 点  stdin=%r\n     期望=%r\n     实得=%r" % (j, sin, exp, got))
            if fails > 40:
                print("… 失败过多，提前中止")
                return fails
    if not quiet:
        print("对拍：%d 份源码 × %d 个测试点，失败 %d" % (len(jobs), N_CASES, fails))
    return fails


# ------------------------------------------------------------------ #
#  写文件 / CLI
# ------------------------------------------------------------------ #
def dump(probs: list[dict], gen_name: str, doc: str, var: str) -> str:
    body = json.dumps(probs, ensure_ascii=False, indent=4)
    body = (body.replace(": null", ": None")
                .replace(": true", ": True")
                .replace(": false", ": False"))
    head = ('# -*- coding: utf-8 -*-\n'
            '"""%s —— 自动生成，**不要手改本文件**。\n\n'
            '生成器：tools/%s\n'
            '题数：%d 题 / %d 测试点 / 总分 %d\n\n'
            '重生成：python tools/%s\n'
            '"""\n\n'
            '%s: list[dict] = ' % (doc, gen_name, len(probs),
                                   sum(len(p["cases"]) for p in probs),
                                   sum(p["total_score"] for p in probs),
                                   gen_name, var))
    return head + body + "\n"


def cli(problems: list[dict], out_rel: str, doc: str, var: str,
        *, do_verify: bool = True, workers: int | None = None) -> int:
    ap = argparse.ArgumentParser(description=doc)
    ap.add_argument("--check", action="store_true", help="只校验，不写文件")
    ap.add_argument("--no-run", action="store_true", help="跳过真编真跑（不建议）")
    args = ap.parse_args()

    probs = build(problems)
    print("题目数：%d   测试点：%d   总分：%d"
          % (len(probs), sum(len(p["cases"]) for p in probs),
             sum(p["total_score"] for p in probs)))

    bad = sanity(probs)
    if bad:
        print("★ 结构自检不通过：")
        for b in bad:
            print("   " + b)
        return 1
    print("结构自检通过 ✅")

    if do_verify and not args.no_run:
        fails = verify(probs, workers=workers)
        if fails:
            return 2
        print("真编真跑通过 ✅")
    if args.check:
        return 0

    out = ROOT / out_rel
    m = re.search(r"cpp_basic(\d+)", out_rel)
    gen_name = "gen_cpp_basic%s.py" % (m.group(1) if m else "1")
    out.write_text(dump(probs, gen_name, doc, var), encoding="utf-8", newline="\n")
    print("已写入 %s（%d 字节）" % (out, out.stat().st_size))
    return 0
