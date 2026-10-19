"""题型回归：使用临时数据库，不碰用户正在使用的进度。"""
from __future__ import annotations

import os
import sys
import tempfile
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

with tempfile.TemporaryDirectory(prefix="pta-types-") as tmp:
    os.environ["PTA_DB"] = str(Path(tmp) / "pta.db")

    from app import db, seed
    from app.question_types import LABELS, infer

    db.init_db()
    added = seed.ensure()
    assert added == len(seed.SEED_PROBLEMS)

    rows = db.query("SELECT id, title, line, choices, question_type FROM problems")
    assert len(rows) == len(seed.SEED_PROBLEMS)
    assert all(r["question_type"] in LABELS for r in rows)
    counts = Counter(r["question_type"] for r in rows)
    assert counts["programming"] > 0
    assert counts["single_choice"] > 0
    assert counts["true_false"] > 0
    assert counts["fill_blank"] > 0
    # ★ 「多选 / 简答 / 实操」这三类**只能来自题库里的显式标注**，
    #   推断（infer）不许凭答案长短或字母个数猜出来 —— 所以库里这三类的数量
    #   必须与「题库里显式写了这几类的条数」**完全相等**，
    #   多一条就是误标，少一条就是漏入库。这样两边同时加题也不会互相踩。
    explicit = Counter(p["question_type"] for p in seed.SEED_PROBLEMS
                       if p.get("question_type"))
    for k in ("multiple_choice", "short_answer", "practical"):
        assert counts[k] == explicit.get(k, 0), \
            f"{k} 只能来自题库显式标注：库里 {counts[k]} 条 / 题库 {explicit.get(k, 0)} 条"
    assert counts["multiple_choice"] > 0, "题库里应当有多选题"
    assert counts["practical"] > 0, "题库里应当有实操题（课程实验那 15 道）"

    # 老库补标幂等；人工题显式类型不应被种子同步覆盖。
    old_id = rows[0]["id"]
    db.execute("UPDATE problems SET question_type='' WHERE id=?", (old_id,))
    assert seed.sync_question_types() == 1
    assert seed.sync_question_types() == 0
    assert db.query_one("SELECT question_type FROM problems WHERE id=?", (old_id,))["question_type"] in LABELS

    assert infer({"line": "text", "choices": ["A", "B", "C"], "reference_solution": "AC"}) == "multiple_choice"
    assert infer({"line": "text", "choices": [], "question_type": "short_answer"}) == "short_answer"
    # 实操题 / 简答题不许被推断出来：没有显式标注的话，一律按填空题算
    assert infer({"line": "text", "choices": [], "reference_solution": "744 -rwxr--r--"}) == "fill_blank"
    print("题型分类与老库补标通过：", len(rows), "题，", dict(counts))
