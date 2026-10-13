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
    """建表（幂等）+ 补列（迁移）。返回数据库路径。"""
    global _LAST_MIGRATION
    path = Path(db_path) if db_path else config.get().db_path
    sql = SCHEMA_PATH.read_text(encoding="utf-8")
    with connect_ctx(path) as conn:
        conn.executescript(sql)
        _LAST_MIGRATION = _migrate(conn)
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
)


def _table_columns(conn: sqlite3.Connection, table: str) -> set[str]:
    rows = conn.execute("PRAGMA table_info(%s)" % table).fetchall()
    return {r["name"] for r in rows}


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
