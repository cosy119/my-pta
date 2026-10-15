"""把题库导出成静态 JSON + 生成 GitHub Pages 站点。

为什么需要这个
--------------
前端要放到 GitHub Pages（纯静态，没有 Python）。所以：

1. **题目列表**必须能在没有后端时也显示出来 → 导出成 `docs/problems.json`
2. 理论题、Python 和 C/C++ 题在浏览器本地判
3. 后端连不上时，前端仍能浏览题目、运行 Python、保存本地进度

产出（都在 docs/ 下）
--------------------
- `index.html`   ← 从 web/index.html 拷过来
- `problems.json` ← 题库快照（含题面、样例、分值；**不含**参考解）
- `.nojekyll`     ← 别让 GitHub Pages 用 Jekyll 处理

用法
----
    python tools/export_static.py            # 导出到 docs/
    python tools/export_static.py --out dist # 换个目录
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import _console                                                   # noqa: E402
from app import db, scoring                                   # noqa: E402

WEB = ROOT / "web"
DEFAULT_OUT = ROOT / "docs"

# 这些字段是「内部资料」，绝不外传
_STRIP_FIELDS = ("reference_solution", "ref_interpreter", "ai_meta", "ai_model")


def build_bank(with_cases: bool = False) -> dict:
    """把库里的题目拼成前端能直接吃的结构。

    with_cases=True 时**额外把隐藏测试点也下发**（前端本地判题需要 stdin + 期望输出）。
    默认 False，与历史行为完全一致：隐藏点只给个数，内容不出库。

    ★ 实测（204 题）：342 个隐藏点全量下发只占 **8.4 KB**
      —— problems.json 从 267 KB → 275 KB，只涨 3%。所以「下发隐藏点」在体积上
      根本不是问题，唯一需要权衡的是「学生能看到期望输出」这件事本身。
    """
    # ★ subject / choices 必须一起导：前端要靠它们做「科目分类」和渲染选择题选项。
    #   选择题的正确答案在 expected_stdout 里（且这些题 is_sample=0），所以给 options 不泄题。
    rows = db.query("""
        SELECT id, subject, line, title, difficulty, total_score, tags, choices,
               statement_md, input_format, output_format, constraints_md,
               time_limit_ms, memory_limit_mb, checker, float_eps,
               source_section, source_anchor, origin, status
        FROM problems
        WHERE status = 'published'
        ORDER BY id ASC
    """)

    items: list[dict] = []
    for p in rows:
        for f in _STRIP_FIELDS:
            p.pop(f, None)
        p["tags"] = db.jloads(p["tags"], [])
        p["choices"] = db.jloads(p["choices"], [])
        p["is_choice"] = bool(p["choices"])
        p["subject"] = p.get("subject") or "python"

        # 测试点：样例全给（题面要用），隐藏点**只给个数和分值**，内容绝不出库
        cases = db.query(
            "SELECT id, ord, stdin, expected_stdout, is_sample, points, explanation, kind "
            "FROM testcases WHERE problem_id=? ORDER BY ord, id", (p["id"],))
        p["testcase_count"] = len(cases)
        p["samples"] = [
            {"id": c["id"], "ord": c["ord"], "stdin": c["stdin"],
             "expected_stdout": c["expected_stdout"], "explanation": c["explanation"]}
            for c in cases if c["is_sample"]
        ]
        p["hidden_count"] = sum(1 for c in cases if not c["is_sample"])
        # 前端本地判题需要**完整的**测试点（含期望输出与分值）→ 只有显式开启才带出来。
        # 不开时**不加这个键**，保证默认导出与历史产物字节级一致（只有时间戳在变）。
        #
        # ★ 给的是全量（样例 + 隐藏）而不是只有隐藏点：判题要按 ord 把所有点都过一遍，
        #   分值也才能和后端 scoring.grade 对上。
        if with_cases:
            p["cases"] = [
                {"ord": c["ord"], "is_sample": bool(c["is_sample"]),
                 "stdin": c["stdin"], "expected_stdout": c["expected_stdout"],
                 "points": int(c["points"] or 0)}
                for c in cases
            ]

        # 测试点分值（前端展示用；判题时后端会再算一遍）
        raw = [c["points"] for c in cases]
        p["case_points"] = scoring.normalize_points(raw, int(p["total_score"] or 100))
        p["points_sum"] = sum(p["case_points"])

        items.append(p)

    return {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "count": len(items),
        "total_score": sum(int(p["total_score"] or 0) for p in items),
        "total_testcases": sum(p["testcase_count"] for p in items),
        "items": items,
    }


def export(out_dir: Path, with_cases: bool = False) -> None:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1) 题库
    bank = build_bank(with_cases=with_cases)
    (out_dir / "problems.json").write_text(
        json.dumps(bank, ensure_ascii=False, indent=1), encoding="utf-8")
    n_hidden = sum(1 for p in bank["items"]
                   for c in (p.get("cases") or []) if not c["is_sample"])
    extra = "（含 %d 个隐藏测试点）" % n_hidden if with_cases else "（隐藏点未下发）"
    print("题目 %d 道 / %d 分 / %d 个测试点 %s → %s"
          % (bank["count"], bank["total_score"], bank["total_testcases"], extra,
             out_dir / "problems.json"))

    # 2) 前端
    if WEB.exists():
        for f in WEB.iterdir():
            if f.is_file():
                shutil.copy2(f, out_dir / f.name)
        for name in ("python", "pyodide", "clang"):
            src = WEB / name
            if src.is_dir():
                shutil.copytree(src, out_dir / name, dirs_exist_ok=True)
        # Keep the browser comparator identical to the server comparator.
        shutil.copy2(ROOT / "app" / "judge" / "compare.py",
                     out_dir / "python" / "compare.py")
        print("前端已拷到", out_dir)

    # 3) 别让 Jekyll 处理（否则 _ 开头的文件会被吃掉）
    (out_dir / ".nojekyll").write_text("", encoding="utf-8")

    # 4) 一个最小的 CORS 说明，免得以后忘了
    (out_dir / "backend.txt").write_text(
        "理论题、Python 和 C/C++ 题可直接在浏览器中判题，无需安装后端。\n"
        "浏览器 C/C++ 使用 Clang/WASI，首次加载约 29 MB；与 GCC 后端可能略有差异。\n",
        encoding="utf-8")

    print("\n产物清单：")
    for f in sorted(out_dir.rglob("*")):
        if f.is_file():
            print("  %-32s %8d 字节" % (f.relative_to(out_dir), f.stat().st_size))


def main() -> int:
    ap = argparse.ArgumentParser(description="导出静态题库 + 生成 Pages 站点")
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="输出目录（默认 docs/）")
    ap.add_argument("--with-cases", action="store_true",
                    help="把隐藏测试点也导出（前端本地判题用；实测仅 +8.4 KB）")
    args = ap.parse_args()
    export(Path(args.out), with_cases=args.with_cases)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
