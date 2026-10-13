"""题目接口：列表 / 详情 / 平台元信息。"""
from __future__ import annotations

import re

from fastapi import APIRouter, HTTPException

from .. import config, db

router = APIRouter(prefix="/api", tags=["problems"])

# 「第 03 讲 · 流程控制语句」→ 3；匹配不到就排到最后
_LECTURE_RE = re.compile(r"第\s*(\d+)\s*讲")


def _order_key(row: dict) -> tuple:
    """学习顺序：先按讲义讲次，再按难度，最后按 id。

    这样题目列表就是「循序渐进」的 —— 第 02 讲的基础题一定排在第 03 讲前面。
    """
    m = _LECTURE_RE.search(row.get("source_section") or "")
    if m:
        return (0, int(m.group(1)), int(row.get("difficulty") or 0), row["id"])
    return (1, 0, int(row.get("difficulty") or 0), row["id"])


@router.get("/meta")
def meta():
    """前端启动时拉一次：可选语言、解释器、平台信息。"""
    cfg = config.get()
    interps = cfg.interpreters
    langs = [
        {
            "lang": "python",
            "label": "Python",
            "default": interps.get("default", "py313"),
            "interpreters": [
                {"key": "py313",
                 "label": "Python 3.13.14（讲义实测环境）",
                 "path": interps.get("py313", "")},
                {"key": "py314",
                 "label": "Python 3.14.4（Thonny 自带）",
                 "path": interps.get("py314", "")},
            ],
        },
    ]
    return {
        "langs": langs,
        "port": cfg.port,
        "db": str(cfg.db_path),
        "paths": {
            "settings": str(cfg.config_path),
            "tmp_judge": str(cfg.tmp_judge),
        },
        "limits": {
            "default_time_limit_ms": cfg.default_time_limit_ms,
            "default_memory_limit_mb": cfg.default_memory_limit_mb,
            "max_output_bytes": cfg.max_output_bytes,
        },
    }


@router.get("/problems")
def list_problems(line: str | None = None, status: str | None = None,
                  q: str | None = None):
    sql = """
        SELECT p.id, p.line, p.title, p.difficulty, p.tags, p.origin, p.status,
               p.total_score,
               p.source_section, p.source_anchor, p.created_at,
               COALESCE(m.attempts, 0)   AS attempts,
               COALESCE(m.ac_count, 0)   AS ac_count,
               COALESCE(m.level, 0)      AS level,
               COALESCE(m.best_score, 0) AS best_score,
               COALESCE(m.is_starred, 0) AS is_starred,
               COALESCE(m.last_verdict, '') AS last_verdict,
               m.solved_at               AS solved_at,
               (SELECT COUNT(*) FROM testcases t WHERE t.problem_id = p.id) AS testcase_count
        FROM problems p
        LEFT JOIN mastery m ON m.problem_id = p.id
        WHERE 1 = 1
    """
    params: list = []
    if line:
        sql += " AND p.line = ?"
        params.append(line)
    if status:
        sql += " AND p.status = ?"
        params.append(status)
    if q:
        sql += " AND (p.title LIKE ? OR p.tags LIKE ?)"
        params += [f"%{q}%", f"%{q}%"]
    sql += " ORDER BY p.id ASC"

    rows = db.query(sql, params)
    for r in rows:
        r["tags"] = db.jloads(r["tags"], [])
        r["score_label"] = "%d/%d" % (r["best_score"] or 0, r["total_score"] or 0)
        r["solved"] = bool(r["solved_at"])
    rows.sort(key=_order_key)          # ★ 按讲义讲次排序，循序渐进
    return {"items": rows, "total": len(rows)}


@router.get("/problems/{pid}")
def get_problem(pid: int):
    p = db.query_one("SELECT * FROM problems WHERE id=?", (pid,))
    if not p:
        raise HTTPException(status_code=404, detail="题目不存在")

    p["tags"] = db.jloads(p["tags"], [])
    p["samples"] = db.query(
        "SELECT id, ord, stdin, expected_stdout, explanation FROM testcases "
        "WHERE problem_id = ? AND is_sample = 1 ORDER BY ord, id", (pid,))

    cnt = db.query_one(
        "SELECT COUNT(*) AS n, SUM(CASE WHEN is_sample = 0 THEN 1 ELSE 0 END) AS hidden, "
        "       SUM(COALESCE(points, 0)) AS pts "
        "FROM testcases WHERE problem_id = ?", (pid,))
    p["testcase_count"] = (cnt or {}).get("n", 0) or 0
    p["hidden_count"] = (cnt or {}).get("hidden", 0) or 0

    # 测试点分值：库里可能是 0（老数据），用题目满分兜底算一份展示用
    from .. import scoring
    raw = db.query("SELECT points FROM testcases WHERE problem_id=? ORDER BY ord, id", (pid,))
    p["case_points"] = scoring.normalize_points([r["points"] for r in raw],
                                                int(p["total_score"] or 100))
    p["points_sum"] = sum(p["case_points"])

    # ---------- 每题进度 + 历史 ----------
    m = db.query_one("SELECT * FROM mastery WHERE problem_id=?", (pid,)) or {}
    p["mastery"] = m
    p["best_score"] = int(m.get("best_score") or 0)
    p["solved_at"] = m.get("solved_at") or ""
    p["solved"] = bool(p["solved_at"])

    # 打开题目时回填用的「最后一次提交」
    p["last_submission"] = None
    if m.get("last_submission_id"):
        p["last_submission"] = db.query_one(
            "SELECT id, verdict, score, max_score, passed, total, lang, interpreter, "
            "       code, created_at, judged_at FROM submissions WHERE id=?",
            (m["last_submission_id"],))

    # 历史提交（每次提交都留档，默认给最近 50 条）
    p["history"] = db.query(
        "SELECT id, verdict, score, max_score, passed, total, lang, interpreter, "
        "       time_ms, mem_kb, created_at, judged_at "
        "FROM submissions WHERE problem_id=? ORDER BY id DESC LIMIT 50", (pid,))

    p["history_count"] = (db.query_one(
        "SELECT COUNT(*) AS n FROM submissions WHERE problem_id=?", (pid,)) or {}).get("n", 0)

    # 参考解不外传（留着自己判题和日后回看用）
    p.pop("reference_solution", None)
    return p


@router.get("/lectures")
def list_lectures(line: str | None = None):
    """讲义索引（P3 出题用；先给个读接口，方便前端展示回链目标）。"""
    sql = "SELECT id, path, line, title, scanned_at FROM lectures"
    params: list = []
    if line:
        sql += " WHERE line = ?"
        params.append(line)
    return {"items": db.query(sql + " ORDER BY id", params)}
