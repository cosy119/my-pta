"""用户身份：**无账号密码**的轻量标识。

设计取舍
--------
这是个人学习平台，不是公网服务 —— 加注册/登录只会让 cosy 多记一个密码，
没有任何收益。所以这里用「**浏览器自己生成的通行证**」：

1. 前端第一次打开时生成一个随机 token（32 位十六进制），存在 localStorage；
2. 之后每次请求都带 `X-User-Token: <token>` 头；
3. 后端见到新 token 就自动建一条 users 记录（**首见即注册**）；
4. 所有 submissions / mastery 都按 user_id 过滤 → 各人进度天然隔离。

代价（必须说清楚）：**清浏览器数据 = 丢身份 = 看不到旧进度**。
所以提供了「导出/导入通行证」的能力，用同一串 token 就能在别的设备接上同一份进度。
"""
from __future__ import annotations

import hashlib
import re
import secrets
from typing import Any

from . import db

# token 形态：32 位小写十六进制（前端 crypto.getRandomValues 生成）
_TOKEN_RE = re.compile(r"^[0-9a-f]{16,64}$")

# 没有 token 时（比如 curl 调试、老脚本）归到这台机器的「本机用户」，
# 这样 `tools/` 下面的自检脚本不用改就能继续用。
DEFAULT_TOKEN = "local-default-user"
DEFAULT_NAME = "本机用户"


def is_valid(token: str | None) -> bool:
    return bool(token) and bool(_TOKEN_RE.match(token))


def new_token() -> str:
    """给前端生成时用的样例 token（32 位十六进制）。"""
    return secrets.token_hex(16)


def _nickname_for(token: str) -> str:
    """没有昵称时，用 token 前 6 位拼一个，方便在界面上认出「这是哪一份进度」。"""
    h = hashlib.sha1(token.encode("utf-8")).hexdigest()[:6]
    return "学习者-" + h


def resolve(token: str | None, *, create: bool = True) -> dict[str, Any] | None:
    """把 token 解析成 user 记录。不存在则创建（首见即注册）。

    返回 None 只有一种情况：token 格式非法且 create=False。
    """
    tok = (token or "").strip()
    if not tok:
        tok = DEFAULT_TOKEN
    elif not is_valid(tok):
        if not create:
            return None
        # 非法 token 一律归到默认用户，避免前端写错一个字符就凭空造用户
        tok = DEFAULT_TOKEN

    row = db.query_one("SELECT * FROM users WHERE token=?", (tok,))
    if row:
        # 记一次「最后出现」，方便以后做清理/统计
        db.execute("UPDATE users SET last_seen=? WHERE id=?", (db.now_iso(), row["id"]))
        return row

    if not create:
        return None

    uid = db.insert("users", {
        "token": tok,
        "nickname": DEFAULT_NAME if tok == DEFAULT_TOKEN else _nickname_for(tok),
        "created_at": db.now_iso(),
        "last_seen": db.now_iso(),
    })
    return db.query_one("SELECT * FROM users WHERE id=?", (uid,))


def user_id_of(token: str | None) -> int:
    """最常用的一条：拿 user_id。拿不到就返回默认用户 id。"""
    u = resolve(token)
    if u:
        return int(u["id"])
    d = resolve(DEFAULT_TOKEN)
    return int(d["id"]) if d else 0


def rename(uid: int, nickname: str) -> None:
    nick = (nickname or "").strip()[:40]
    if nick:
        db.execute("UPDATE users SET nickname=? WHERE id=?", (nick, int(uid)))


def summary(uid: int) -> dict[str, Any]:
    """给界面用的：这个人的进度概况。"""
    agg = db.query_one("""
        SELECT COUNT(*) AS attempts,
               SUM(CASE WHEN verdict='AC' THEN 1 ELSE 0 END) AS accepted
        FROM submissions WHERE user_id=?
    """, (int(uid),)) or {}
    sc = db.query_one("""
        SELECT COALESCE(SUM(best_score),0) AS got
        FROM mastery WHERE user_id=?
    """, (int(uid),)) or {}
    full = db.query_one("SELECT COALESCE(SUM(total_score),0) AS n FROM problems") or {}
    return {
        "attempts": agg.get("attempts") or 0,
        "accepted": agg.get("accepted") or 0,
        "score": sc.get("got") or 0,
        "max_score": full.get("n") or 0,
    }
