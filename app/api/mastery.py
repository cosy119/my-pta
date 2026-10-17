"""收藏 / 错题本 / 备注 —— mastery 表里「个人标注」那一半。

★ 为什么单独一个文件：`is_starred` / `level` / `note` 三列从多用户改造
  （2026-10-13）起就在 schema 里，`/api/problems` 和 `/api/stats` 也会把它
  们**读**出来，但全项目**没有任何一处写入** —— 判题只更新
  attempts / ac_count / best_score / verdict / solved_at。
  结果就是「收藏」按钮无处可点、错题备注无处可存。这里补的是那条缺失的写通道。

★ 三列语义分工，别再混：
  - is_starred  纯手动标星（收藏）
  - level       掌握度 0 未掌握 / 1 薄弱 / 2 熟练。判题会自动推（见
                judge/worker.py），用户也可以手改 —— 所以这里允许写。
  - note        自己写的备注（错因、思路、下次注意）。可编辑、可清空。
  - 「错题」**不落库**，由 `attempts > 0 且 best_score < total_score` 算出来。
    它是进度的派生量，存一份必然与判题结果打架（判完还要记得同步它）。
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request

from .. import db, users

router = APIRouter(prefix="/api", tags=["mastery"])

# 备注长度上限。够写一段错因分析，又不至于把库撑坏。
NOTE_MAX = 2000


def current_user(request: Request) -> dict:
    """从 X-User-Token 解析当前用户（首见即注册）。"""
    return users.resolve(request.headers.get("x-user-token")) or {}


def _norm_star(v) -> int:
    """星星只收 0 / 1。前端传 true/false 也认。"""
    if isinstance(v, bool):
        return 1 if v else 0
    try:
        n = int(v)
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail="is_starred 只能是 0 或 1")
    if n not in (0, 1):
        raise HTTPException(status_code=400, detail="is_starred 只能是 0 或 1")
    return n


def _norm_level(v) -> int:
    """掌握度只收 0 / 1 / 2（与 mastery.level 的定义一致）。"""
    try:
        n = int(v)
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail="level 只能是 0/1/2")
    if n not in (0, 1, 2):
        raise HTTPException(status_code=400, detail="level 只能是 0/1/2")
    return n


def _norm_note(v) -> str:
    s = "" if v is None else str(v)
    s = s.replace("\r\n", "\n").replace("\r", "\n").strip()
    if len(s) > NOTE_MAX:
        raise HTTPException(status_code=400, detail=f"备注最多 {NOTE_MAX} 字（现在 {len(s)}）")
    return s


def _row_of(uid: int, pid: int) -> dict:
    return db.query_one("SELECT * FROM mastery WHERE user_id=? AND problem_id=?",
                        (uid, pid)) or {}


def _ensure_row(uid: int, pid: int) -> dict:
    """没有就建一行空进度 —— 收藏/写备注不该依赖「先提交过一次」。

    ★ attempts 保持 0：只是收藏一下、写句备注，不算做过这题。
      否则首页「已尝试」和错题本会被一堆 0 分假错题污染。
    """
    row = _row_of(uid, pid)
    if row:
        return row
    db.insert("mastery", {
        "user_id": uid,
        "problem_id": pid,
        "attempts": 0,
        "ac_count": 0,
        "best_score": 0,
        "last_verdict": "",
        "last_at": "",
        "solved_at": "",
        "is_starred": 0,
        "level": 0,
        "note": "",
    })
    return _row_of(uid, pid)


def _shape(r: dict) -> dict:
    """统一前端要用的形状（跟 /api/problems 的字段名对齐）。"""
    total = int(r.get("total_score") or 0)
    best = int(r.get("best_score") or 0)
    attempts = int(r.get("attempts") or 0)
    return {
        "id": int(r["id"]),
        "title": r.get("title") or "",
        "subject": r.get("subject") or "python",
        "line": r.get("line") or "python",
        "question_type": r.get("question_type") or "",
        "total_score": total,
        "best_score": best,
        "attempts": attempts,
        "ac_count": int(r.get("ac_count") or 0),
        "last_verdict": r.get("last_verdict") or "",
        "is_starred": int(r.get("is_starred") or 0),
        "level": int(r.get("level") or 0),
        "note": r.get("note") or "",
        "source_section": r.get("source_section") or "",
        "last_at": r.get("last_at") or "",
        "solved_at": r.get("solved_at") or "",
        # 「错题」= 做过但没拿到满分。满分才算解决，与 /api/progress 的口径一致。
        "is_wrong": bool(attempts > 0 and best < total),
        "solved": bool(r.get("solved_at")),
    }


@router.get("/mastery")
def list_mastery(user: dict = Depends(current_user)):
    """当前用户的所有标注（含空的也返回，方便前端整块替换本地缓存）。

    只返回**有标注或有进度**的行，不返回空行。
    """
    uid = int(user.get("id") or 0)
    rows = db.query("""
        SELECT p.id, p.title, p.subject, p.line, p.question_type,
               p.total_score, p.source_section,
               COALESCE(m.attempts, 0)      AS attempts,
               COALESCE(m.ac_count, 0)      AS ac_count,
               COALESCE(m.best_score, 0)    AS best_score,
               COALESCE(m.last_verdict, '') AS last_verdict,
               COALESCE(m.is_starred, 0)    AS is_starred,
               COALESCE(m.level, 0)         AS level,
               COALESCE(m.note, '')         AS note,
               m.last_at                    AS last_at,
               m.solved_at                  AS solved_at
        FROM problems p
        JOIN mastery m ON m.problem_id = p.id AND m.user_id = ?
        WHERE m.attempts > 0 OR m.is_starred = 1 OR COALESCE(m.note, '') <> ''
        ORDER BY p.id ASC
    """, (uid,))
    return {"items": [_shape(r) for r in rows], "total": len(rows)}


@router.patch("/mastery/{pid}")
def patch_mastery(pid: int, body: dict, user: dict = Depends(current_user)):
    """增量更新一道题的标注：星标 / 掌握度 / 备注。

    ★ 增量语义：body 里出现哪个字段就只改哪个，没出现的保持原值。
      这样「点星星」不会把备注冲掉，「存备注」也不会把星星取消
      （前端两个入口各自只管自己那一半）。
    """
    uid = int(user.get("id") or 0)
    prob = db.query_one("SELECT id FROM problems WHERE id=?", (pid,))
    if not prob:
        raise HTTPException(status_code=404, detail="题目不存在")

    sets, params = [], []
    if "is_starred" in body:
        sets.append("is_starred=?")
        params.append(_norm_star(body.get("is_starred")))
    if "level" in body:
        sets.append("level=?")
        params.append(_norm_level(body.get("level")))
    if "note" in body:
        sets.append("note=?")
        params.append(_norm_note(body.get("note")))
    if not sets:
        raise HTTPException(status_code=400,
                            detail="至少要给 is_starred / level / note 之一")

    _ensure_row(uid, pid)
    params += [uid, pid]
    db.execute("UPDATE mastery SET " + ", ".join(sets)
               + " WHERE user_id=? AND problem_id=?", tuple(params))
    return {"ok": True, "item": _shape(_row_of_full(uid, pid))}


def _row_of_full(uid: int, pid: int) -> dict:
    """带题目信息的单行（_shape 需要 total_score / title 这些）。"""
    return db.query_one("""
        SELECT p.id, p.title, p.subject, p.line, p.question_type,
               p.total_score, p.source_section,
               COALESCE(m.attempts, 0)      AS attempts,
               COALESCE(m.ac_count, 0)      AS ac_count,
               COALESCE(m.best_score, 0)    AS best_score,
               COALESCE(m.last_verdict, '') AS last_verdict,
               COALESCE(m.is_starred, 0)    AS is_starred,
               COALESCE(m.level, 0)         AS level,
               COALESCE(m.note, '')         AS note,
               m.last_at                    AS last_at,
               m.solved_at                  AS solved_at
        FROM problems p
        JOIN mastery m ON m.problem_id = p.id AND m.user_id = ?
        WHERE p.id = ?
    """, (uid, pid)) or {}


@router.get("/wrongbook")
def wrongbook(user: dict = Depends(current_user)):
    """错题本：把「错题 / 收藏 / 有备注」三类归到一起，另给各桶数量。

    ★ 三类是**可能重叠**的（一道收藏了的错题两个都算），所以 items 只返回一份，
      用 is_wrong / is_starred 两个布尔让前端自己筛，别在后端切三份列表 ——
      那样前端改筛选条件就得改接口。
    """
    uid = int(user.get("id") or 0)
    rows = db.query("""
        SELECT p.id, p.title, p.subject, p.line, p.question_type,
               p.total_score, p.source_section,
               COALESCE(m.attempts, 0)      AS attempts,
               COALESCE(m.ac_count, 0)      AS ac_count,
               COALESCE(m.best_score, 0)    AS best_score,
               COALESCE(m.last_verdict, '') AS last_verdict,
               COALESCE(m.is_starred, 0)    AS is_starred,
               COALESCE(m.level, 0)         AS level,
               COALESCE(m.note, '')         AS note,
               m.last_at                    AS last_at,
               m.solved_at                  AS solved_at
        FROM problems p
        JOIN mastery m ON m.problem_id = p.id AND m.user_id = ?
        WHERE m.attempts > 0 OR m.is_starred = 1 OR COALESCE(m.note, '') <> ''
        ORDER BY p.id ASC
    """, (uid,))
    items = [_shape(r) for r in rows]
    return {
        "items": items,
        "counts": {
            "total": len(items),
            "wrong": sum(1 for x in items if x["is_wrong"]),
            "starred": sum(1 for x in items if x["is_starred"]),
            "noted": sum(1 for x in items if x["note"]),
            "solved": sum(1 for x in items if x["solved"]),
        },
    }
