"""把题库导出成静态 JSON + 生成 GitHub Pages 站点。

为什么需要这个
--------------
前端要放到 GitHub Pages（纯静态，没有 Python）。所以：

1. **题目列表**必须能在没有后端时也显示出来 → 导出成 `docs/problems.json`
2. 真正的判题仍然连后端（同一个人自己部署的免费实例）
3. 后端连不上时，前端至少能：浏览题目、看样例、本地草稿（存 localStorage）

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

from app import db, scoring                                   # noqa: E402

WEB = ROOT / "web"
DEFAULT_OUT = ROOT / "docs"

# 这些字段是「内部资料」，绝不外传
_STRIP_FIELDS = ("reference_solution", "ref_interpreter", "ai_meta", "ai_model")


def build_bank() -> dict:
    """把库里的题目拼成前端能直接吃的结构。"""
    rows = db.query("""
        SELECT id, line, title, difficulty, total_score, tags,
               statement_md, input_format, output_format, constraints_md,
               time_limit_ms, memory_limit_mb, checker, float_eps,
               source_section, source_anchor, origin, status
        FROM problems
        ORDER BY id ASC
    """)

    items: list[dict] = []
    for p in rows:
        for f in _STRIP_FIELDS:
            p.pop(f, None)
        p["tags"] = db.jloads(p["tags"], [])

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


def export(out_dir: Path) -> None:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1) 题库
    bank = build_bank()
    (out_dir / "problems.json").write_text(
        json.dumps(bank, ensure_ascii=False, indent=1), encoding="utf-8")
    print("题目 %d 道 / %d 分 / %d 个测试点 → %s"
          % (bank["count"], bank["total_score"], bank["total_testcases"],
             out_dir / "problems.json"))

    # 2) 前端
    if WEB.exists():
        for f in WEB.iterdir():
            if f.is_file():
                shutil.copy2(f, out_dir / f.name)
        print("前端已拷到", out_dir)

    # 3) 别让 Jekyll 处理（否则 _ 开头的文件会被吃掉）
    (out_dir / ".nojekyll").write_text("", encoding="utf-8")

    # 4) 一个最小的 CORS 说明，免得以后忘了
    (out_dir / "backend.txt").write_text(
        "这个静态站默认连「同源」后端。\n"
        "部署到 GitHub Pages 后，请在页面右上角「设置」里填你自己的后端地址，\n"
        "例如 https://my-pta.onrender.com —— 部署方法见仓库 README。\n",
        encoding="utf-8")

    print("\n产物清单：")
    for f in sorted(out_dir.rglob("*")):
        if f.is_file():
            print("  %-32s %8d 字节" % (f.relative_to(out_dir), f.stat().st_size))


def main() -> int:
    ap = argparse.ArgumentParser(description="导出静态题库 + 生成 Pages 站点")
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="输出目录（默认 docs/）")
    args = ap.parse_args()
    export(Path(args.out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
