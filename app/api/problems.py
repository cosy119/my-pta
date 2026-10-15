"""题目接口：列表 / 详情 / 平台元信息。

★ 多用户（2026-10-13）：题库是**大家共用**的，进度（mastery）是**每人一份**。
  所有带进度的接口都按 `X-User-Token` 过滤。
"""
from __future__ import annotations

import re

from fastapi import APIRouter, Depends, HTTPException, Request

from .. import config, db, users
from ..question_types import LABELS as QUESTION_TYPE_LABELS
from ..seed import SUBJECT_LABELS

router = APIRouter(prefix="/api", tags=["problems"])

# 「第 03 讲 · 流程控制语句」→ 3；匹配不到就是 0（排在该科目的最前面）
_LECTURE_RE = re.compile(r"第\s*(\d+)\s*讲")

# 科目展示顺序：Python → 数据结构 → Linux
SUBJECT_ORDER = {"python": 0, "ds": 1, "linux": 2}

# 题目的语言选项：由 `line` 推导出「这道题能用哪些语言提交」
# ★ 数据结构线是重点：`cpp` 表示**编译型**，学生可以用 C **或** C++ 交，
#   两条路走不同的编译器（见 app/judge/runner_cpp.py）
LANG_OPTIONS = {
    "python": [{"lang": "python", "label": "Python", "hint": "解释执行"}],
    "cpp": [
        {"lang": "cpp", "label": "C++ (g++)", "hint": "-std=c++17"},
        {"lang": "c", "label": "C (gcc)", "hint": "-std=gnu11"},
    ],
    "c": [{"lang": "c", "label": "C (gcc)", "hint": "-std=gnu11"}],
    "text": [],
}


def current_user(request: Request) -> dict:
    """从 X-User-Token 解析当前用户（首见即注册）。"""
    return users.resolve(request.headers.get("x-user-token")) or {}


def lang_options_for(line: str) -> list[dict]:
    return LANG_OPTIONS.get(str(line or "python").lower(), LANG_OPTIONS["python"])


def _subject_key(subject) -> int:
    return SUBJECT_ORDER.get(str(subject or "python"), 9)


def _order_key(row: dict) -> tuple:
    """学习顺序：先按**科目**，再按讲义讲次，最后按录入顺序。

    ★ 最后用 `id` 而不是 `difficulty`：题库是按「由易到难」的编排顺序录进去的，
      再按难度排一次反而会把精心设计的顺序打乱
      （而且 Linux 线里「基础命令 / 实验 N」这两组没有讲次号，本来就得靠 id 定序）。
    """
    m = _LECTURE_RE.search(str(row.get("source_section") or ""))
    lec = int(m.group(1)) if m else 0
    return (_subject_key(row.get("subject")), lec, row["id"])


@router.get("/me")
def me(user: dict = Depends(current_user)):
    """当前身份 + 这个人自己的进度概况。前端启动时拉一次。"""
    uid = int(user.get("id") or 0)
    s = users.summary(uid)
    return {
        "id": uid,
        "nickname": user.get("nickname") or "",
        "token": (user.get("token") or "")[:8] + "…",   # 只回前 8 位，别把整串 token 到处传
        "attempts": s["attempts"],
        "accepted": s["accepted"],
        "score": s["score"],
        "max_score": s["max_score"],
    }


@router.post("/me")
def rename_me(body: dict, user: dict = Depends(current_user)):
    """给这份进度起个名字，方便在界面上认出来。"""
    users.rename(int(user.get("id") or 0), str(body.get("nickname") or ""))
    return {"ok": True}


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
        {
            # ★ 数据结构线：同一道题 C 和 C++ 都能交，走不同的编译器
            "lang": "cpp",
            "label": "C++ (g++)",
            "default": "gpp",
            "interpreters": [
                {"key": "gpp", "label": "g++ -std=c++17",
                 "path": cfg.compiler_path("gpp")},
            ],
        },
        {
            "lang": "c",
            "label": "C (gcc)",
            "default": "gcc",
            "interpreters": [
                {"key": "gcc", "label": "gcc -std=gnu11",
                 "path": cfg.compiler_path("gcc")},
            ],
        },
        {
            # 理论题（选择 / 判断 / 填空）：提交内容即答案，不需要任何运行时
            "lang": "text",
            "label": "文本答案",
            "default": "text",
            "interpreters": [],
        },
    ]
    return {
        "langs": langs,
        "question_types": [{"key": k, "label": v} for k, v in QUESTION_TYPE_LABELS.items()],
        "subjects": [{"key": k, "label": v} for k, v in SUBJECT_LABELS.items()],
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


@router.get("/catalog")
def catalog(user: dict = Depends(current_user)):
    """科目目录：科目 → 分组（讲次 / 实验 / 基础命令）→ 题数与我的进度。

    前端主界面（题集广场）用它渲染卡片和进度条，一次请求就够，
    不用把整个题库拉下来再自己聚合。
    """
    uid = int(user.get("id") or 0)
    rows = db.query("""
        SELECT p.subject, p.line, p.source_section, p.total_score, p.difficulty,
               COALESCE(m.best_score, 0) AS best_score,
               m.solved_at               AS solved_at,
               COALESCE(m.attempts, 0)   AS attempts
        FROM problems p
        LEFT JOIN mastery m ON m.problem_id = p.id AND m.user_id = ?
        WHERE p.status = 'published'
    """, (uid,))

    subs: dict[str, dict] = {}
    for r in rows:
        key = str(r["subject"] or "python")
        s = subs.setdefault(key, {
            "key": key,
            "label": SUBJECT_LABELS.get(key, key),
            "total": 0, "solved": 0, "attempted": 0,
            "score": 0, "max_score": 0,
            "difficulty": {}, "lines": {},
            "sections": {},
        })
        s["total"] += 1
        s["score"] += int(r["best_score"] or 0)
        s["max_score"] += int(r["total_score"] or 0)
        if r["solved_at"]:
            s["solved"] += 1
        if int(r["attempts"] or 0) > 0:
            s["attempted"] += 1
        s["difficulty"][str(r["difficulty"] or 1)] = \
            s["difficulty"].get(str(r["difficulty"] or 1), 0) + 1
        s["lines"][str(r["line"] or "python")] = \
            s["lines"].get(str(r["line"] or "python"), 0) + 1

        # 分组名：优先用讲义讲次（「第 03 讲 · 流程控制语句」），
        # 没有讲次号的（基础命令 / 实验 N）就按 section 原文分组
        sec = str(r["source_section"] or "未分组")
        g = s["sections"].setdefault(sec, {
            "name": sec, "total": 0, "solved": 0, "score": 0, "max_score": 0,
        })
        g["total"] += 1
        g["score"] += int(r["best_score"] or 0)
        g["max_score"] += int(r["total_score"] or 0)
        if r["solved_at"]:
            g["solved"] += 1

    out = []
    for key, s in subs.items():
        secs = list(s.pop("sections").values())
        # 组内顺序：跟题库录入顺序一致（讲次号在前、其余按名字）
        secs.sort(key=lambda x: (
            int(_LECTURE_RE.search(x["name"]).group(1))
            if _LECTURE_RE.search(x["name"]) else 0,
            x["name"]))
        s["sections"] = secs
        out.append(s)
    out.sort(key=lambda x: _subject_key(x["key"]))
    return {"subjects": out, "user_score": sum(x["score"] for x in out),
            "user_max_score": sum(x["max_score"] for x in out)}


@router.get("/problems")
def list_problems(line: str | None = None, status: str | None = None,
                  subject: str | None = None, q: str | None = None,
                  question_type: str | None = None,
                  user: dict = Depends(current_user)):
    uid = int(user.get("id") or 0)
    sql = """
        SELECT p.id, p.subject, p.line, p.question_type, p.title, p.difficulty, p.tags,
               p.origin, p.status, p.choices,
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
        LEFT JOIN mastery m ON m.problem_id = p.id AND m.user_id = ?
        WHERE 1 = 1
    """
    params: list = [uid]
    if line:
        sql += " AND p.line = ?"
        params.append(line)
    if subject:
        sql += " AND p.subject = ?"
        params.append(subject)
    if question_type:
        if question_type not in QUESTION_TYPE_LABELS:
            raise HTTPException(status_code=400, detail="未知题型")
        sql += " AND p.question_type = ?"
        params.append(question_type)
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
        r["choices"] = db.jloads(r["choices"], [])
        r["is_choice"] = bool(r["choices"])
        r["score_label"] = "%d/%d" % (r["best_score"] or 0, r["total_score"] or 0)
        r["solved"] = bool(r["solved_at"])
        r["langs"] = lang_options_for(r["line"])
    rows.sort(key=_order_key)          # ★ 按讲义讲次排序，循序渐进
    return {"items": rows, "total": len(rows)}


@router.get("/problems/{pid}")
def get_problem(pid: int, user: dict = Depends(current_user)):
    uid = int(user.get("id") or 0)
    p = db.query_one("SELECT * FROM problems WHERE id=?", (pid,))
    if not p:
        raise HTTPException(status_code=404, detail="题目不存在")

    p["tags"] = db.jloads(p["tags"], [])
    p["choices"] = db.jloads(p["choices"], [])
    p["is_choice"] = bool(p["choices"])
    # 这道题能用哪些语言提交（数据结构线 = C / C++ 二选一）
    p["langs"] = lang_options_for(p["line"])
    p["subject_label"] = SUBJECT_LABELS.get(str(p["subject"] or "python"), "")
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

    # ---------- 每题进度 + 历史（★ 只看当前用户的） ----------
    m = db.query_one("SELECT * FROM mastery WHERE user_id=? AND problem_id=?",
                     (uid, pid)) or {}
    p["mastery"] = m
    p["best_score"] = int(m.get("best_score") or 0)
    p["solved_at"] = m.get("solved_at") or ""
    p["solved"] = bool(p["solved_at"])

    # 打开题目时回填用的「最后一次提交」（自己的）
    p["last_submission"] = None
    if m.get("last_submission_id"):
        p["last_submission"] = db.query_one(
            "SELECT id, verdict, score, max_score, passed, total, lang, interpreter, "
            "       code, created_at, judged_at FROM submissions WHERE id=? AND user_id=?",
            (m["last_submission_id"], uid))

    # 历史提交（每次提交都留档，默认给最近 50 条；★ 只看自己的）
    p["history"] = db.query(
        "SELECT id, verdict, score, max_score, passed, total, lang, interpreter, "
        "       time_ms, mem_kb, created_at, judged_at "
        "FROM submissions WHERE user_id=? AND problem_id=? ORDER BY id DESC LIMIT 50",
        (uid, pid))

    p["history_count"] = (db.query_one(
        "SELECT COUNT(*) AS n FROM submissions WHERE user_id=? AND problem_id=?",
        (uid, pid)) or {}).get("n", 0)

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
