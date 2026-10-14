#!/usr/bin/env python
"""对拍夹具：理论题判题口径（Python 侧）。

为什么需要
----------
前端有一套**独立的**理论题判题实现（`web/judge_text.js`），它是
`app/judge/compare.py` + `app/judge/runner_text.py` + `app/scoring.py` 的 JS 移植。
两套实现必须给出**逐条相同**的结果，否则同一份答案在「浏览器本地判」和
「后端判」下会得出不同结论 —— 而且只在边角处悄悄分叉，极难发现。

分工
----
    python tools/verify_text_judge.py          # → data/_text_judge_fixtures.json
    node   tools/verify_text_judge.mjs         # JS 侧跑同一批输入，逐条比对

★ 这里必须走**真实的** TextRunner + compare + scoring（连 prepare 都调），
  而不是在夹具里另写一套「差不多的」判题逻辑 —— 否则对拍就成了自己跟自己比。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

import _console                                                   # noqa: E402
from app import db, scoring                                       # noqa: E402
from app.judge.compare import compare, oneof_alternatives         # noqa: E402
from app.judge.runner_text import TextRunner                      # noqa: E402

OUT = ROOT / "data" / "_text_judge_fixtures.json"
WORKDIR = ROOT  # 理论题不落盘，随便给个存在的目录即可


def judge_python(prob: dict, cases: list[dict], answer: str) -> dict:
    """完全复刻 worker.py 对理论题的判题流程（只有沙箱部分不适用）。"""
    runner = TextRunner()
    ok, msg = runner.prepare(answer, WORKDIR)
    if not ok:                       # 理论题的 prepare 永远返回 True，这里只做兜底
        return {"verdict": "CE", "score": 0, "max_score": 0, "passed": 0,
                "total": len(cases), "message": msg, "normalized": "",
                "cases": ["CE"] * len(cases)}

    checker = prob.get("checker") or "standard"
    eps = float(prob.get("float_eps") or 1e-6)
    total_score = int(prob.get("total_score") or 0)

    verdicts: list[str] = []
    messages: list[str] = []
    overall = "AC"
    first_fail = ""
    passed = 0

    for c in cases:
        res = runner.run_case(WORKDIR, (c["stdin"] or "").encode("utf-8"), None)
        if res.verdict == "OK":
            cmp = compare(c["expected_stdout"] or "", res.stdout, checker, eps)
            v = "AC" if cmp.ok else ("PE" if cmp.kind == "pe" else "WA")
            detail = cmp.detail
        else:
            v = res.verdict
            detail = res.detail
        verdicts.append(v)
        messages.append(detail or "")
        if v == "AC":
            passed += 1
        elif overall == "AC":
            overall = v
            first_fail = detail

    g = scoring.grade([c["points"] for c in cases], verdicts, total_score)
    # ★ 必须**先**取值再 cleanup —— cleanup 会把 _answer 清空
    normalized = runner._answer
    runner.cleanup(WORKDIR)

    return {
        "verdict": overall,
        "score": int(g["score"]),
        "max_score": int(g["max_score"]),
        "passed": passed,
        "total": len(cases),
        "message": first_fail or "",
        "normalized": normalized,
        "cases": verdicts,
    }


def answers_for(prob: dict, cases: list[dict]) -> list[str]:
    """给一道题造一批「该判对」和「该判错」的答案。

    覆盖三类边界：
    - 正确答案本体（reference_solution / 每个 `|` 备选）
    - 正确答案的**写法变体**（全角标点、首尾空格、大小写、带「答案：」前缀）
      —— 这些必须仍然判对，否则前端会把学生的正确写法判成 WA
    - 明显错的答案（空、胡写、另一个选项）—— 这些必须判错，
      否则说明判题是「恒真」的，对拍也就没有意义
    """
    outs: list[str] = []
    ref = (prob.get("reference_solution") or "").strip()
    alts: list[str] = []
    for c in cases:
        alts.extend(oneof_alternatives(c["expected_stdout"] or ""))

    if ref:
        outs.append(ref)
    for a in alts:
        outs.append(a)
        outs.append(a + "。")                       # 尾部全角句号（排版类标点，应被宽容）
        outs.append("  " + a + "  ")                # 首尾空格
        outs.append(a + "，")
        outs.append(a.lower())
        outs.append(a.upper())
        outs.append("（" + a + "）")

    base = ref or (alts[0] if alts else "")
    if base:
        outs.append("答案：" + base)
        outs.append("选 " + base)
        outs.append("答" + base)

    # 明显错的答案
    outs.extend(["", "   ", "zzz 这肯定不对", "对", "错", "A", "B", "C", "D",
                 "0", "-1", "ls /tmp"])

    seen, uniq = set(), []
    for o in outs:
        if o not in seen:
            seen.add(o)
            uniq.append(o)
    return uniq


def main() -> int:
    ap = argparse.ArgumentParser(description="导出理论题判题对拍夹具")
    ap.add_argument("--line", default="text", help="只取这个 line 的题（默认 text）")
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args()

    rows = db.query(
        "SELECT id, title, subject, line, checker, float_eps, total_score, "
        "reference_solution, statement_md FROM problems "
        "WHERE status='published' AND line=? ORDER BY id", (args.line,))
    if not rows:
        print("没有找到 line=%s 的题" % args.line)
        return 1

    probs = []
    n_answers = 0
    for p in rows:
        raw = db.query(
            "SELECT ord, stdin, expected_stdout, is_sample, points "
            "FROM testcases WHERE problem_id=? ORDER BY ord, id", (p["id"],))
        cases = [{"ord": r["ord"], "is_sample": bool(r["is_sample"]),
                  "stdin": r["stdin"] or "", "expected_stdout": r["expected_stdout"] or "",
                  "points": int(r["points"] or 0)} for r in raw]

        base = {
            "id": p["id"], "title": p["title"], "subject": p["subject"],
            "checker": p["checker"], "float_eps": p["float_eps"],
            "total_score": int(p["total_score"] or 0), "cases": cases,
        }
        ans = []
        for a in answers_for(p, cases):
            ans.append({"text": a, "py": judge_python(base, cases, a)})
        n_answers += len(ans)
        base["answers"] = ans
        probs.append(base)

    payload = {
        "generated_at": db.now_iso(),
        "line": args.line,
        "count": len(probs),
        "answer_count": n_answers,
        "probs": probs,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print("夹具已写出：%d 道题 / %d 条答案 → %s" % (len(probs), n_answers, out))
    print("下一步：node tools/verify_text_judge.mjs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
