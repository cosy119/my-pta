"""SQLite 访问层：短连接 + Row 工厂 + schema 初始化。

设计要点（对齐计划 §五）：
- 每次操作开一个短连接，绝不在判题期间持有事务（判题是长任务，持锁会锁死 Web 写入）
- WAL + busy_timeout 由 schema.sql 的 PRAGMA 设定
"""
from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Iterator, Sequence

from . import config

SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"
INDEX_SQL = (Path(__file__).resolve().parent / "index.sql").read_text(encoding="utf-8")


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def connect(db_path: Path | None = None) -> sqlite3.Connection:
    """开一个短连接。调用方负责关（或用 connect_ctx）。"""
    path = Path(db_path) if db_path else config.get().db_path
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), timeout=5.0, isolation_level=None)
    conn.row_factory = sqlite3.Row
    # 每个连接都要设：WAL 是库级属性，busy_timeout 是连接级
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


@contextmanager
def connect_ctx(db_path: Path | None = None) -> Iterator[sqlite3.Connection]:
    conn = connect(db_path)
    try:
        yield conn
    finally:
        conn.close()


def init_db(db_path: Path | None = None) -> Path:
    """建表（幂等）+ 补列（迁移）。返回数据库路径。

    顺序很关键（踩过）：**建表 → 迁移 → 建索引**。
    schema.sql 里若有「针对新列的索引」，在老库上直接建会报
    `no such column: user_id` —— 因为老表还没补列。所以索引单独拆到最后。
    """
    global _LAST_MIGRATION
    path = Path(db_path) if db_path else config.get().db_path
    sql = SCHEMA_PATH.read_text(encoding="utf-8")
    with connect_ctx(path) as conn:
        conn.executescript(sql)
        _LAST_MIGRATION = _migrate(conn)
        conn.executescript(INDEX_SQL)      # 迁移之后再建索引
    return path


_LAST_MIGRATION: list[str] = []


def last_migration() -> list[str]:
    """上一次 init_db/migrate 实际新增的列（给启动日志用）。"""
    return list(_LAST_MIGRATION)


# 已有库要补的列：(表, 列, 声明)
# 新建的库 schema.sql 里已经有这些列，这里对老库生效。
# 只做 ADD COLUMN —— 不重建表、不搬数据，所以老提交记录一条都不会丢。
MIGRATIONS: tuple[tuple[str, str, str], ...] = (
    ("problems", "total_score", "INTEGER DEFAULT 100"),
    ("submissions", "max_score", "INTEGER DEFAULT 0"),
    ("submission_cases", "points", "INTEGER DEFAULT 0"),
    ("submission_cases", "earned", "INTEGER DEFAULT 0"),
    ("mastery", "best_score", "INTEGER DEFAULT 0"),
    ("mastery", "best_submission_id", "INTEGER"),
    ("mastery", "last_submission_id", "INTEGER"),
    ("mastery", "solved_at", "TEXT DEFAULT ''"),
    # ---- 多用户改造（2026-10-13）----
    # 老库的 submissions 没有 user_id，补上后统一归到「本机用户」
    ("submissions", "user_id", "INTEGER"),
)


def _table_columns(conn: sqlite3.Connection, table: str) -> set[str]:
    rows = conn.execute("PRAGMA table_info(%s)" % table).fetchall()
    return {r["name"] for r in rows}


def _table_exists(conn: sqlite3.Connection, table: str) -> bool:
    return bool(conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)).fetchone())


def _needs_mastery_rebuild(conn: sqlite3.Connection) -> bool:
    """老库的 mastery 是 problem_id 单列主键 —— 多用户必须改成 (user_id, problem_id)。

    SQLite 不支持改主键，只能「建新表 → 搬数据 → 换名」。这里判断是否要做。
    """
    if not _table_exists(conn, "mastery"):
        return False
    cols = _table_columns(conn, "mastery")
    if "user_id" not in cols:
        return True
    # 有 user_id 了，还得确认主键真的是复合的（PRAGMA 里 pk 序号 >0 的列数）
    info = conn.execute("PRAGMA table_info(mastery)").fetchall()
    pk_cols = [r["name"] for r in info if r["pk"]]
    return "user_id" not in pk_cols


def _rebuild_mastery(conn: sqlite3.Connection, default_uid: int) -> str | None:
    """把老 mastery 重建成 (user_id, problem_id) 复合主键，老数据归到 default_uid。

    返回 "mastery 重建" 说明做了事；None 说明不用做。
    """
    if not _needs_mastery_rebuild(conn):
        return None

    cols = _table_columns(conn, "mastery")
    has_uid = "user_id" in cols

    conn.execute("""
        CREATE TABLE mastery_new (
          user_id            INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
          problem_id         INTEGER NOT NULL REFERENCES problems(id) ON DELETE CASCADE,
          attempts           INTEGER DEFAULT 0,
          ac_count           INTEGER DEFAULT 0,
          best_score         INTEGER DEFAULT 0,
          best_submission_id INTEGER,
          last_submission_id INTEGER,
          last_verdict       TEXT DEFAULT '',
          last_at            TEXT DEFAULT '',
          solved_at          TEXT DEFAULT '',
          is_starred         INTEGER DEFAULT 0,
          level              INTEGER DEFAULT 0,
          note               TEXT DEFAULT '',
          PRIMARY KEY (user_id, problem_id)
        )
    """)

    # 老表可能缺若干列（更早的版本），缺的用默认值兜住
    def col(name: str, fallback: str) -> str:
        return name if name in cols else fallback

    pick = ", ".join([
        (col("user_id", str(default_uid)) if has_uid else str(default_uid)),
        "problem_id",
        col("attempts", "0"),
        col("ac_count", "0"),
        col("best_score", "0"),
        col("best_submission_id", "NULL"),
        col("last_submission_id", "NULL"),
        col("last_verdict", "''"),
        col("last_at", "''"),
        col("solved_at", "''"),
        col("is_starred", "0"),
        col("level", "0"),
        col("note", "''"),
    ])
    conn.execute(
        "INSERT OR REPLACE INTO mastery_new "
        "(user_id, problem_id, attempts, ac_count, best_score, best_submission_id, "
        " last_submission_id, last_verdict, last_at, solved_at, is_starred, level, note) "
        "SELECT %s FROM mastery" % pick)

    conn.execute("DROP TABLE mastery")
    conn.execute("ALTER TABLE mastery_new RENAME TO mastery")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_mastery_user ON mastery(user_id)")
    return "mastery 重建（加 user_id 复合主键）"


def _ensure_default_user(conn: sqlite3.Connection) -> int:
    """保证「本机用户」存在，返回它的 id。老数据都归到它名下。"""
    from . import users as _users

    row = conn.execute("SELECT id FROM users WHERE token=?",
                       (_users.DEFAULT_TOKEN,)).fetchone()
    if row:
        return int(row["id"])
    cur = conn.execute(
        "INSERT INTO users (token, nickname, created_at, last_seen) VALUES (?,?,?,?)",
        (_users.DEFAULT_TOKEN, _users.DEFAULT_NAME, now_iso(), now_iso()))
    return int(cur.lastrowid)


def _migrate(conn: sqlite3.Connection) -> list[str]:
    """给老库补列。返回本次新增的 "表.列" 列表（幂等：已存在就跳过）。"""
    added: list[str] = []
    for table, col, decl in MIGRATIONS:
        cols = _table_columns(conn, table)
        if not cols:          # 表还不存在（schema.sql 会建，理论上不会走到）
            continue
        if col not in cols:
            conn.execute("ALTER TABLE %s ADD COLUMN %s %s" % (table, col, decl))
            added.append("%s.%s" % (table, col))

    # ---- 多用户迁移：老记录全归「本机用户」，一条都不丢 ----
    if _table_exists(conn, "users"):
        uid = _ensure_default_user(conn)
        rebuilt = _rebuild_mastery(conn, uid)
        if rebuilt:
            added.append(rebuilt)
        # 老提交没有 user_id（NULL）→ 归到本机用户
        n = conn.execute(
            "UPDATE submissions SET user_id=? WHERE user_id IS NULL", (uid,)).rowcount
        if n:
            added.append("submissions.user_id 回填 %d 条" % n)
    return added


def migrate(db_path: Path | None = None) -> list[str]:
    """单独调用迁移（服务启动时用，方便把结果打出来）。"""
    with connect_ctx(db_path) as conn:
        return _migrate(conn)


# ---------------- 便捷查询 ----------------

def query(sql: str, params: Sequence[Any] = (), db_path: Path | None = None) -> list[dict]:
    with connect_ctx(db_path) as conn:
        cur = conn.execute(sql, params)
        return [dict(r) for r in cur.fetchall()]


def query_one(sql: str, params: Sequence[Any] = (), db_path: Path | None = None) -> dict | None:
    rows = query(sql, params, db_path)
    return rows[0] if rows else None


def execute(sql: str, params: Sequence[Any] = (), db_path: Path | None = None) -> int:
    """执行写操作，返回 lastrowid（INSERT）或受影响行数。"""
    with connect_ctx(db_path) as conn:
        cur = conn.execute(sql, params)
        return cur.lastrowid if cur.lastrowid else cur.rowcount


def insert(table: str, data: dict[str, Any], db_path: Path | None = None) -> int:
    cols = ", ".join(data.keys())
    marks = ", ".join("?" for _ in data)
    sql = f"INSERT INTO {table} ({cols}) VALUES ({marks})"
    return execute(sql, tuple(data.values()), db_path)


def update(table: str, data: dict[str, Any], where: str, params: Sequence[Any] = (),
           db_path: Path | None = None) -> int:
    sets = ", ".join(f"{k} = ?" for k in data)
    sql = f"UPDATE {table} SET {sets} WHERE {where}"
    return execute(sql, tuple(data.values()) + tuple(params), db_path)


def executemany(sql: str, seq: Iterable[Sequence[Any]], db_path: Path | None = None) -> None:
    with connect_ctx(db_path) as conn:
        conn.executemany(sql, list(seq))


# ---------------- 小工具 ----------------

def jloads(text: str | None, default: Any = None) -> Any:
    if not text:
        return default if default is not None else []
    try:
        return json.loads(text)
    except (ValueError, TypeError):
        return default if default is not None else []


def jdumps(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False)
