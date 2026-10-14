# -*- coding: utf-8 -*-
"""把测试脚本的数据库钉到**测试库**，绝不碰 `data/pta.db`。

**为什么单独一个模块**

`app/config.py` 的 `db_path` 是「读取时定格」的：第一次 `config.get()` 时
从环境变量 `PTA_DB` 取值，之后再改环境变量也没用。
所以「切到测试库」这件事必须在**任何 `from app import ...` 之前**做完 ——
放在函数里、放在 `main()` 开头都太晚了。

于是抽成这个模块：**导入即生效**。写法：

    import _console          # noqa: E402
    import _testdb           # noqa: E402   ← 必须在 app 之前
    from app import db

**为什么需要它**

2026-10-13 的教训：`selfcheck.py` 默认连真实库，一天跑了三次，
把用户的做题记录从 11 条灌到 33 条。
2026-10-14 同类问题又咬了一次：`httptest_users.py` 起服务时只复制了
`os.environ`，没设 `PTA_DB` —— 它自己那个进程和服务进程**双双连到真实库**，
凭空多出 2 条提交 / 2 个测试账号。

**给脚本作者的两条规矩**

1. 自己会 `Popen` 起服务的脚本（`httptest_users` / `httptest_split`）：
   除了 import 本模块，还要把 `PTA_DB` **显式塞进子进程的 env** ——
   子进程不会因为父进程 import 过什么而自动继承一个没写进 `os.environ` 的值。
   本模块在导入时就把 `PTA_DB` 写进了 `os.environ`，所以 `dict(os.environ)` 就够了。
2. 只是**连接**已有服务的脚本（`e2e_ui` / `httptest`）：
   不要设 `PTA_DB`（服务在别人手里），但要用 `guard_live_db()` 先问一句
   `/api/health` 连的是哪个库，是真实库就大声警告。
"""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

#: 所有自检脚本共用的测试库（`.gitignore` 已忽略 `data/`）
TEST_DB = ROOT / "data" / "_bank_test.db"


def use_test_db(force: bool = True) -> str:
    """把 `PTA_DB` 指向测试库，并返回路径。

    `force=False` 时**不覆盖**已经设好的 `PTA_DB`（尊重调用方的显式指定）。

    只动 `PTA_DB` 一个变量 —— 判题临时目录之类的不碰，
    免得「导入一个模块」产生意料之外的副作用。
    """
    if not force and os.environ.get("PTA_DB"):
        return os.environ["PTA_DB"]
    os.environ["PTA_DB"] = str(TEST_DB)
    return str(TEST_DB)


def fresh_test_db() -> str:
    """把测试库**删掉重建**（连同 `-wal` / `-shm`），返回路径。

    给「用固定通行证 + 断言条数」的脚本用（`httptest_users` / `httptest_split`）：
    「A 的历史条数 = 1」这种断言只有在**干净的库**上才成立，
    否则第二次跑就会数到上一次留下的记录，报一堆假失败。

    测试库本来就是拿来被蹂躏的，删了不心疼。
    schema 不用管 —— `app/db.py` 的 `connect()` 会自己建表。

    ★ 自带一道保险：函数里只可能碰 `TEST_DB`，绝不可能是真实库。
    """
    assert TEST_DB.name != "pta.db", "测试库路径不能是真实库"
    for suffix in ("", "-wal", "-shm"):
        p = Path(str(TEST_DB) + suffix)
        try:
            if p.exists():
                p.unlink()
        except OSError:
            pass
    return use_test_db()


def guard_live_db(health: dict) -> str:
    """看看对面服务连的是哪个库。返回一句人话提示。

    给「连已有服务」的脚本用（`e2e_ui` / `httptest`）——
    它们没法决定服务用哪个库，但至少要在日志里说清楚，
    免得测试数据悄悄写进真实库又没人发现。
    """
    db = str((health or {}).get("db") or "")
    name = Path(db.replace("\\", "/")).name if db else "?"
    if name == "pta.db":
        return ("⚠️⚠️ 注意：对面服务连的是**真实库** %s —— 这次测试会往里面写数据！\n"
                "        下次请用测试库起服务：\n"
                "            set PTA_DB=E:\\学习\\001\\pta\\data\\_bank_test.db\n"
                "        或者直接跑 tools\\smoke_cloud.py（它自己起进程、自带隔离）" % db)
    return "对面服务连的是 %s（不是真实库，安全）" % (db or "未知")


# 导入即生效，但不覆盖调用方已经设好的 PTA_DB。
# 想强制切到测试库：显式再调一次 use_test_db()。
# 想让它**别**自动切（例如 selfcheck.py --live 要对着真实库跑）：
# 先设 os.environ["PTA_TESTDB_AUTO"] = "0" 再 import 本模块。
if os.environ.get("PTA_TESTDB_AUTO", "1") != "0":
    use_test_db(force=False)
