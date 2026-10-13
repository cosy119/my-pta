"""提交与判题查询接口。

★ 多用户（2026-10-13）：所有接口都按请求头 `X-User-Token` 隔离，
  各人的提交记录与进度互不可见。
"""
from __future__ import annotations

import os
import time
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel

from .. import config, db, users
from ..judge import sandbox
from ..judge.runner_base import Limits
from ..judge.worker import build_runner, get_worker

router = APIRouter(prefix="/api", tags=["submissions"])


def current_user(request: Request) -> dict:
    """从 X-User-Token 解析当前用户（首见即注册）。"""
    return users.resolve(request.headers.get("x-user-token")) or {}


class SubmitIn(BaseModel):
    problem_id: int
    code: str
    lang: str = "python"
    interpreter: str = "py313"


class RunIn(BaseModel):
    code: str
    lang: str = "python"
    interpreter: str = "py313"
    stdin: str = ""
    time_limit_ms: int = 5000
    memory_limit_mb: int = 256


@router.post("/submissions")
def create_submission(body: SubmitIn, user: dict = Depends(current_user)):
    p = db.query_one("SELECT id, line FROM problems WHERE id=?", (body.problem_id,))
    if not p:
        raise HTTPException(status_code=404, detail="题目不存在")
    if not body.code or not body.code.strip():
        raise HTTPException(status_code=400, detail="代码是空的")

    sid = db.insert("submissions", {
        "user_id": int(user.get("id") or 0),
        "problem_id": body.problem_id,
        "lang": body.lang or p["line"] or "python",
        "interpreter": body.interpreter or "py313",
        "code": body.code,
        "verdict": "pending",
        "created_at": db.now_iso(),
    })
    get_worker().submit(sid)
    return {"id": sid, "verdict": "pending"}


def _run_once_sync(body: RunIn) -> dict:
    """只跑一次、不判题 —— 给界面上的「运行自测」按钮用。"""
    cfg = config.get()
    tag = f"run_{int(time.time() * 1000)}_{os.getpid()}"
    workdir = Path(cfg.tmp_judge) / tag
    sandbox.rmtree_force(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    try:
        runner = build_runner(body.lang, body.interpreter, cfg)
        ok, msg = runner.prepare(body.code, workdir)
        if not ok:
            return {"ok": False, "verdict": "CE", "compile_output": msg,
                    "stdout": "", "stderr": "", "time_ms": 0, "mem_kb": 0, "detail": ""}
        limits = Limits(
            time_ms=max(100, min(60000, int(body.time_limit_ms))),
            memory_mb=max(16, min(2048, int(body.memory_limit_mb))),
            max_output_bytes=cfg.max_output_bytes,
            kill_grace_ms=cfg.kill_grace_ms,
        )
        res = runner.run_case(workdir, body.stdin.encode("utf-8"), limits)
        return {
            "ok": res.verdict == "OK",
            "verdict": res.verdict,
            "stdout": res.stdout.decode("utf-8", "replace"),
            "stderr": res.stderr.decode("utf-8", "replace"),
            "time_ms": res.time_ms,
            "mem_kb": res.mem_kb,
            "detail": res.detail,
            "compile_output": "",
        }
    finally:
        sandbox.rmtree_force(workdir)


@router.post("/run")
async def run_once(body: RunIn):
    """自测：跑一次看输出。丢到线程池，别占着事件循环。"""
    if not body.code or not body.code.strip():
        raise HTTPException(status_code=400, detail="代码是空的")
    return await run_in_threadpool(_run_once_sync, body)


@router.get("/submissions/{sid}")
def get_submission(sid: int, with_cases: bool = True, user: dict = Depends(current_user)):
    """取一次提交。★ 只能看自己的 —— 别人的提交直接 404。"""
    s = db.query_one("SELECT * FROM submissions WHERE id=? AND user_id=?",
                     (sid, int(user.get("id") or 0)))
    if not s:
        raise HTTPException(status_code=404, detail="提交不存在")
    if with_cases:
        s["cases"] = db.query(
            "SELECT id, case_id, ord, verdict, points, earned, time_ms, mem_kb, "
            "       stdout, stderr, expected, stdin, exit_code, detail "
            "FROM submission_cases WHERE submission_id=? ORDER BY ord, id", (sid,))
    return s


@router.get("/submissions")
def list_submissions(problem_id: int | None = None, limit: int = 50,
                     user: dict = Depends(current_user)):
    sql = ("SELECT id, problem_id, lang, interpreter, verdict, score, max_score, "
           "       passed, total, time_ms, mem_kb, created_at, judged_at "
           "FROM submissions WHERE user_id = ?")
    params: list = [int(user.get("id") or 0)]
    if problem_id:
        sql += " AND problem_id = ?"
        params.append(problem_id)
    sql += " ORDER BY id DESC LIMIT ?"
    params.append(max(1, min(500, limit)))
    return {"items": db.query(sql, params)}


@router.get("/progress")
def progress(user: dict = Depends(current_user)):
    """总进度：按题目汇总「已得 / 满分」，以及逐题明细。

    只算每题的**历史最高分**（best_score），跟 PTA 一样 —— 刷题不倒退。
    ★ 只看当前用户的 mastery。
    """
    uid = int(user.get("id") or 0)
    rows = db.query("""
        SELECT p.id, p.title, p.line, p.difficulty, p.total_score,
               COALESCE(m.best_score, 0) AS best_score,
               COALESCE(m.attempts, 0)   AS attempts,
               COALESCE(m.ac_count, 0)   AS ac_count,
               COALESCE(m.last_verdict, '') AS last_verdict,
               m.solved_at,
               COALESCE(m.is_starred, 0) AS is_starred
        FROM problems p
        LEFT JOIN mastery m ON m.problem_id = p.id AND m.user_id = ?
        ORDER BY p.id ASC
    """, (uid,))
    full = sum(int(r["total_score"] or 0) for r in rows)
    got = sum(int(r["best_score"] or 0) for r in rows)
    solved = sum(1 for r in rows if r["solved_at"])
    attempted = sum(1 for r in rows if (r["attempts"] or 0) > 0)
    return {
        "problems": len(rows),
        "solved": solved,
        "attempted": attempted,
        "score": got,
        "max_score": full,
        "percent": round(got * 100.0 / full, 1) if full else 0.0,
        "items": rows,
    }


@router.get("/stats")
def stats(user: dict = Depends(current_user)):
    """首页角标用：题目数、提交数、通过率、总得分等（全部限当前用户）。"""
    uid = int(user.get("id") or 0)
    prob = db.query_one("SELECT COUNT(*) AS n FROM problems") or {}
    pub = db.query_one("SELECT COUNT(*) AS n FROM problems WHERE status='published'") or {}
    sub = db.query_one("SELECT COUNT(*) AS n FROM submissions WHERE user_id=?", (uid,)) or {}
    ac = db.query_one(
        "SELECT COUNT(*) AS n FROM submissions WHERE user_id=? AND verdict='AC'", (uid,)) or {}
    star = db.query_one(
        "SELECT COUNT(*) AS n FROM mastery WHERE user_id=? AND is_starred=1", (uid,)) or {}

    # 得分汇总：每题取历史最高分
    agg = db.query_one("""
        SELECT SUM(COALESCE(p.total_score, 0))   AS full,
               SUM(COALESCE(m.best_score, 0))    AS got,
               SUM(CASE WHEN COALESCE(m.solved_at,'') <> '' THEN 1 ELSE 0 END) AS solved
        FROM problems p
        LEFT JOIN mastery m ON m.problem_id = p.id AND m.user_id = ?
    """, (uid,)) or {}

    return {
        "problems": prob.get("n", 0),
        "published": pub.get("n", 0),
        "submissions": sub.get("n", 0),
        "accepted": ac.get("n", 0),
        "starred": star.get("n", 0),
        "solved": agg.get("solved", 0) or 0,
        "score": agg.get("got", 0) or 0,
        "max_score": agg.get("full", 0) or 0,
        "pending": get_worker().pending(),
        "user": {"id": uid, "nickname": user.get("nickname") or ""},
    }
