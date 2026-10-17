# -*- coding: utf-8 -*-
"""收藏 / 错题本 / 备注 —— HTTP 层验收。

验的是 `app/api/mastery.py` 三个端点：
  GET   /api/mastery          当前用户的全部标注
  PATCH /api/mastery/{pid}    增量改星标 / 掌握度 / 备注
  GET   /api/wrongbook        错题 + 收藏 + 有备注的归集与计数

★ 每个用例都用**随机 token**（= 全新用户），所以不删库也不会互相污染，
  跑第二遍照样绿。服务仍用 `_testdb` 的测试库，真实库一动不动。

跑法（仓库根目录）：
  D:\\Pythontools\\Python\\python.exe -X utf8 tools\\httptest_mastery.py
"""
from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import _console                                                   # noqa: E402
import _testdb                                                    # noqa: E402  ★ 必须在 app 之前

HOST = "127.0.0.1"
PORT = 8798
BASE = f"http://{HOST}:{PORT}"

_passed = 0
_failed = 0


def check(name: str, ok: bool, extra: str = "") -> None:
    global _passed, _failed
    if ok:
        _passed += 1
        print(f"  [OK]   {name}" + (f"  -- {extra}" if extra else ""))
    else:
        _failed += 1
        print(f"  [FAIL] {name}" + (f"  -- {extra}" if extra else ""))


def req(path: str, token: str | None = None, method: str = "GET",
        body: dict | None = None, timeout: float = 30.0) -> tuple[int, dict | str]:
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(BASE + path, data=data, method=method)
    if token:
        r.add_header("X-User-Token", token)
    if data:
        r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", "replace")
            code = resp.status
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        code = e.code
    try:
        return code, json.loads(raw)
    except ValueError:
        return code, raw


def wait_ready(timeout: float = 150.0) -> bool:
    t0 = time.time()
    while time.time() - t0 < timeout:
        with socket.socket() as s:
            s.settimeout(0.5)
            if s.connect_ex((HOST, PORT)) == 0:
                try:
                    with urllib.request.urlopen(BASE + "/api/health", timeout=2) as r:
                        if r.status == 200:
                            return True
                except Exception:
                    pass
        time.sleep(0.4)
    return False


def new_token() -> str:
    """全新用户（32 位十六进制，符合前端的 token 正则）。"""
    return uuid.uuid4().hex


def pick_wrong_verdict(token: str) -> tuple[int, str]:
    """挑一道 python 编程题，提交一个必然 WA 的代码，返回 (pid, verdict)。

    ★ 用 `print("__NOPE__")` 而不是 `print(0)`：后者在「输出一个 0」这类题上
      可能**真就 AC 了**，那就测不出错题归集。
    """
    code, r = req("/api/problems?status=published&subject=python", token)
    items = (r or {}).get("items") or []
    cand = [p for p in items if p.get("line") == "python" and not p.get("is_choice")
            and not p.get("is_theory")]
    if not cand:
        raise RuntimeError("题库里没有可提交的 python 编程题")
    pid = int(cand[0]["id"])
    code, sub = req("/api/submissions", token, "POST",
                    {"problem_id": pid, "lang": "python",
                     "code": 'print("__NOPE__")\n'}, timeout=60)
    if code != 200:
        raise RuntimeError(f"提交失败 HTTP {code}: {sub}")
    sid = int(sub.get("id") or 0)
    for _ in range(120):
        time.sleep(0.5)
        c2, s2 = req(f"/api/submissions/{sid}", token)
        v = (s2 or {}).get("verdict") or ""
        if v and v not in ("pending", "judging"):
            return pid, v
    raise RuntimeError("判题超时")


print("=" * 72)
print("收藏 / 错题本 验收 |", BASE)
print("=" * 72)

run_env = dict(os.environ)
run_env["PTA_DB"] = _testdb.use_test_db()
print("测试库：%s" % run_env["PTA_DB"])

proc = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "app.main:app",
     "--host", HOST, "--port", str(PORT), "--log-level", "warning"],
    cwd=str(ROOT), env=run_env,
    stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

try:
    check("服务就绪（/api/health 200）", wait_ready(), BASE)

    A = new_token()

    # ---------- 1. 起点：干净用户 ----------
    print("\n[1] 新用户起点")
    c, r = req("/api/wrongbook", A)
    check("GET /api/wrongbook 200", c == 200, f"HTTP {c}")
    check("新用户错题本为空", (r or {}).get("counts", {}).get("total") == 0,
          str((r or {}).get("counts")))
    c, r = req("/api/mastery", A)
    check("GET /api/mastery 200 且无标注", c == 200 and (r or {}).get("total") == 0,
          f"HTTP {c} total={(r or {}).get('total')}")

    # ---------- 2. 收藏一道题 ----------
    print("\n[2] 收藏（is_starred）")
    c, r = req("/api/problems?status=published", A)
    pid = int(((r or {}).get("items") or [{}])[0].get("id") or 0)
    check("取到一道题", pid > 0, f"pid={pid}")
    c, r = req(f"/api/mastery/{pid}", A, "PATCH", {"is_starred": 1})
    check("PATCH 收藏 200", c == 200, f"HTTP {c}")
    item = (r or {}).get("item") or {}
    check("返回里 is_starred=1", item.get("is_starred") == 1, str(item.get("is_starred")))
    c, r = req("/api/wrongbook", A)
    cnt = (r or {}).get("counts") or {}
    check("错题本出现该题（starred=1）", cnt.get("starred") == 1 and cnt.get("total") == 1,
          str(cnt))
    check("收藏不冒充错题（wrong=0）", cnt.get("wrong") == 0, str(cnt))

    # ★ 关键：收藏 ≠ 做过。attempts 必须还是 0，否则首页「已尝试」被污染。
    c, r = req("/api/progress", A)
    row = next((x for x in ((r or {}).get("items") or []) if x["id"] == pid), {})
    check("收藏不增加 attempts（仍是 0）", int(row.get("attempts") or 0) == 0,
          f"attempts={row.get('attempts')}")
    c, r = req("/api/stats", A)
    check("/api/stats starred=1", (r or {}).get("starred") == 1, str((r or {}).get("starred")))

    # ---------- 3. 写备注（增量语义） ----------
    print("\n[3] 备注与增量更新")
    note = "边界忘了：n=0 时不该进循环。下次先写特殊值。"
    c, r = req(f"/api/mastery/{pid}", A, "PATCH", {"note": note})
    item = (r or {}).get("item") or {}
    check("PATCH 备注 200", c == 200, f"HTTP {c}")
    check("备注存下来了", item.get("note") == note, repr(item.get("note"))[:60])
    check("★ 存备注没把收藏冲掉", item.get("is_starred") == 1, str(item.get("is_starred")))

    c, r = req(f"/api/mastery/{pid}", A, "PATCH", {"level": 2})
    item = (r or {}).get("item") or {}
    check("PATCH 掌握度 200 且 level=2", c == 200 and item.get("level") == 2,
          f"HTTP {c} level={item.get('level')}")
    check("★ 改掌握度没把备注冲掉", item.get("note") == note, repr(item.get("note"))[:40])

    c, r = req(f"/api/wrongbook", A)
    cnt = (r or {}).get("counts") or {}
    check("计数 noted=1 / starred=1", cnt.get("noted") == 1 and cnt.get("starred") == 1, str(cnt))

    # ---------- 4. 清空 / 取消 ----------
    print("\n[4] 清空与取消收藏")
    c, r = req(f"/api/mastery/{pid}", A, "PATCH", {"note": ""})
    check("备注可清空", (r or {}).get("item", {}).get("note") == "", "note=''")
    c, r = req(f"/api/mastery/{pid}", A, "PATCH", {"is_starred": 0})
    item = (r or {}).get("item") or {}
    check("取消收藏 is_starred=0", item.get("is_starred") == 0, str(item.get("is_starred")))
    c, r = req("/api/wrongbook", A)
    # level=2 还留着，所以这一行仍在（level 不是「标注」而是判题推的掌握度）
    cnt = (r or {}).get("counts") or {}
    check("取消收藏后 starred=0 / noted=0",
          cnt.get("starred") == 0 and cnt.get("noted") == 0, str(cnt))

    # ---------- 5. 错题归集（真提交） ----------
    print("\n[5] 错题归集（真提交一次错的）")
    wpid, verdict = pick_wrong_verdict(A)
    check("真提交拿到非 AC 判定", verdict != "AC", f"pid={wpid} verdict={verdict}")
    c, r = req("/api/wrongbook", A)
    hit = next((x for x in ((r or {}).get("items") or []) if x["id"] == wpid), None)
    check("错题进了错题本", hit is not None, f"pid={wpid}")
    if hit:
        check("该项 is_wrong=true", hit.get("is_wrong") is True, str(hit.get("is_wrong")))
        check("带上最后判定", hit.get("last_verdict") == verdict, str(hit.get("last_verdict")))
        check("带上得分 0/满分", hit.get("best_score") == 0 and hit.get("total_score", 0) > 0,
              f"{hit.get('best_score')}/{hit.get('total_score')}")
        check("带上科目与讲次（前端分组要用）",
              hit.get("subject") == "python" and "source_section" in hit,
              f"{hit.get('subject')} / {hit.get('source_section')}")
    cnt = (r or {}).get("counts") or {}
    check("counts.wrong >= 1", cnt.get("wrong", 0) >= 1, str(cnt))

    # 错题写备注 → 两个标记同时成立
    c, r = req(f"/api/mastery/{wpid}", A, "PATCH", {"note": "这题栽在输出格式上", "is_starred": 1})
    c, r = req("/api/wrongbook", A)
    hit = next((x for x in ((r or {}).get("items") or []) if x["id"] == wpid), None) or {}
    check("同一题既错又收藏：两个标记都在",
          hit.get("is_wrong") is True and hit.get("is_starred") == 1,
          f"wrong={hit.get('is_wrong')} star={hit.get('is_starred')}")

    # ---------- 6. 用户隔离 ----------
    print("\n[6] 多用户隔离")
    B = new_token()
    c, r = req("/api/wrongbook", B)
    check("另一个用户看不到别人的收藏/备注",
          (r or {}).get("counts", {}).get("total") == 0, str((r or {}).get("counts")))
    c, r = req(f"/api/mastery/{pid}", B, "PATCH", {"note": "B 的备注"})
    c, r = req("/api/wrongbook", A)
    hit = next((x for x in ((r or {}).get("items") or []) if x["id"] == pid), None) or {}
    check("★ B 改备注不影响 A", hit.get("note") != "B 的备注", repr(hit.get("note"))[:40])

    # ---------- 7. 参数校验 ----------
    print("\n[7] 参数校验（都是 400/404，不能 500）")
    c, _ = req(f"/api/mastery/{pid}", A, "PATCH", {"is_starred": 2})
    check("is_starred=2 → 400", c == 400, f"HTTP {c}")
    c, _ = req(f"/api/mastery/{pid}", A, "PATCH", {"is_starred": "abc"})
    check("is_starred=abc → 400", c == 400, f"HTTP {c}")
    c, _ = req(f"/api/mastery/{pid}", A, "PATCH", {"level": 9})
    check("level=9 → 400", c == 400, f"HTTP {c}")
    c, _ = req(f"/api/mastery/{pid}", A, "PATCH", {})
    check("空 body → 400", c == 400, f"HTTP {c}")
    c, _ = req(f"/api/mastery/{pid}", A, "PATCH", {"note": "x" * 2001})
    check("备注超 2000 字 → 400", c == 400, f"HTTP {c}")
    c, _ = req("/api/mastery/99999999", A, "PATCH", {"note": "hi"})
    check("不存在的题 → 404", c == 404, f"HTTP {c}")

    # ---------- 8. 老接口没被破坏 ----------
    print("\n[8] 回归：老接口照旧")
    c, r = req("/api/problems?status=published", A)
    first = ((r or {}).get("items") or [{}])[0]
    check("/api/problems 仍带 is_starred 字段", "is_starred" in first,
          f"is_starred={first.get('is_starred')}")
    c, r = req(f"/api/problems/{pid}", A)
    check("/api/problems/{id} 仍带 mastery", "mastery" in (r or {}), "mastery ok")
    c, r = req("/api/catalog", A)
    check("/api/catalog 200", c == 200, f"HTTP {c}")

finally:
    proc.terminate()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()

print("\n" + "=" * 72)
print(f"通过 {_passed} 项 / 失败 {_failed} 项")
print("=" * 72)
sys.exit(0 if _failed == 0 else 1)
