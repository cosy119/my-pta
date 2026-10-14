"""为「前端判题」PoC 导出验证夹具。

读什么、为什么
--------------
前端判题的验证必须是**真判题**：拿题库自己的参考解跑题库自己的样例，
看能不能全 AC。所以夹具要三样东西：

1. 题目元信息（checker / 时间限制）—— 判题口径要跟着题走
2. 样例（stdin + expected_stdout）—— 前端真能拿到的数据
3. 参考解 —— **只在验证时用**，正式前端里 `docs/problems.json` 不含它

★ 只读真实库，不 import `_testdb`（那是给自检隔离用的）。
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]                      # experiments/pyodide-judge -> pta
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))     # _console.py 在 tools/ 下

import _console                                                   # noqa: E402
from app import db                                                # noqa: E402

OUT = HERE / "fixtures.json"


def main() -> int:
    rows = db.query("""
        SELECT id, title, subject, checker, float_eps, time_limit_ms,
               memory_limit_mb, reference_solution
        FROM problems
        WHERE status = 'published' AND subject = 'python'
        ORDER BY id ASC
    """)

    items: list[dict] = []
    no_ref = 0
    no_case = 0
    total_cases = 0

    for p in rows:
        cases = db.query(
            "SELECT stdin, expected_stdout, is_sample FROM testcases "
            "WHERE problem_id = ? ORDER BY ord, id", (p["id"],))
        # PoC 阶段前端只有样例（隐藏点没导出），所以只取样例
        samples = [{"stdin": c["stdin"] or "", "expected_stdout": c["expected_stdout"] or ""}
                   for c in cases if c["is_sample"]]
        ref = (p["reference_solution"] or "").strip()
        if not ref:
            no_ref += 1
        if not samples:
            no_case += 1
        total_cases += len(samples)

        items.append({
            "id": p["id"],
            "title": p["title"],
            "checker": p["checker"] or "standard",
            "float_eps": float(p["float_eps"] or 1e-6),
            "time_limit_ms": int(p["time_limit_ms"] or 1000),
            "reference_solution": ref,
            "samples": samples,
            "sample_count": len(samples),
        })

    OUT.write_text(json.dumps({
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "count": len(items),
        "total_samples": total_cases,
        "items": items,
    }, ensure_ascii=False, indent=1), encoding="utf-8")

    print("已导出 %d 道 Python 题 / %d 个样例 → %s" % (len(items), total_cases, OUT))
    print("  参考解缺失：%d 道   样例缺失：%d 道" % (no_ref, no_case))
    print("  夹具大小：%.1f KB" % (OUT.stat().st_size / 1024))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
