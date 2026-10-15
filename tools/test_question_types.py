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
    assert counts["multiple_choice"] == 0  # 当前种子题没有多选，不能误标
    assert counts["short_answer"] == 0
    assert counts["practical"] == 0

    # 老库补标幂等；人工题显式类型不应被种子同步覆盖。
    old_id = rows[0]["id"]
    db.execute("UPDATE problems SET question_type='' WHERE id=?", (old_id,))
    assert seed.sync_question_types() == 1
    assert seed.sync_question_types() == 0
    assert db.query_one("SELECT question_type FROM problems WHERE id=?", (old_id,))["question_type"] in LABELS

    assert infer({"line": "text", "choices": ["A", "B", "C"], "reference_solution": "AC"}) == "multiple_choice"
    assert infer({"line": "text", "choices": [], "question_type": "short_answer"}) == "short_answer"
    print("题型分类与老库补标通过：", len(rows), "题，", dict(counts))
