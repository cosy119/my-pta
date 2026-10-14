# -*- coding: utf-8 -*-
"""HTTP 层验收：真起服务、真发请求、真提交代码。

跑法（服务已在 8765 跑着）：
  D:\\Pythontools\\Python\\python.exe -X utf8 tools\\httptest.py
"""
from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))     # 为了能 import _console
import _console                                               # noqa: E402
import _testdb                                                # noqa: E402  （只用它的 guard_live_db）

BASE = "http://127.0.0.1:8765"
_ok: list[str] = []
_bad: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    (_ok if ok else _bad).append(name)
    print(("  [OK]   " if ok else "  [FAIL] ") + name + (("  -- " + str(detail)) if detail else ""))


def req(method: str, path: str, body=None, timeout: float = 60.0):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    r = urllib.request.Request(BASE + path, data=data, method=method,
                               headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8", "replace")
        ctype = resp.headers.get("Content-Type", "")
        return json.loads(raw) if "json" in ctype else raw


def wait_ready(tries: int = 40) -> bool:
    for _ in range(tries):
        try:
            req("GET", "/api/health", timeout=2)
            return True
        except Exception:
            time.sleep(0.5)
    return False


print("=" * 72)
print("HTTP 层验收 |", BASE)
print("=" * 72)

if not wait_ready():
    print("服务没起来，先检查 uvicorn 是否启动成功")
    sys.exit(1)

# ★ 这个脚本会真的写进去（提交、进度）。先问一句对面连的是哪个库，
#   是真实库就大声说出来 —— 否则测试数据会悄悄混进你的刷题记录。
try:
    print("  " + _testdb.guard_live_db(req("GET", "/api/health")).replace("\n", "\n  "))
except Exception as _e:  # noqa: BLE001
    print("  （读 /api/health 失败，跳过数据库归属检查：%s）" % _e)

# ---------------------------------------------------------------- 1 基础接口
print("\n[1] 基础接口")
h = req("GET", "/api/health")
check("/api/health 返回 ok", h.get("ok") is True, f"pending={h.get('pending')} db={h.get('db')}")

m = req("GET", "/api/meta")
langs = m.get("langs") or []
check("/api/meta 有语言列表", len(langs) >= 1, f"{len(langs)} 种")
if langs:
    interps = langs[0]["interpreters"]
    check("解释器有两个（3.13 / 3.14）", len(interps) == 2,
          " / ".join(i["label"] for i in interps))

idx = req("GET", "/")
check("首页返回 HTML", isinstance(idx, str) and "<title>" in idx,
      f"{len(idx)} 字节" if isinstance(idx, str) else type(idx).__name__)

# ---------------------------------------------------------------- 2 题目接口
print("\n[2] 题目接口")
pl = req("GET", "/api/problems")
items = pl.get("items") or []
check("题目列表非空", len(items) >= 2, f"{len(items)} 道")
for p in items:
    print(f"        #{p['id']} {p['title']}  用例 {p['testcase_count']}  状态 {p['status']}")

pid = items[0]["id"]
pd = req("GET", f"/api/problems/{pid}")
check("题目详情能取到题面", bool(pd.get("statement_md")), pd.get("title"))
check("详情带样例", len(pd.get("samples") or []) >= 1, f"{len(pd.get('samples') or [])} 个样例")
check("详情不泄露参考解", "reference_solution" not in pd)

try:
    req("GET", "/api/problems/999999")
    check("访问不存在的题返回 404", False, "居然没报错")
except urllib.error.HTTPError as e:
    check("访问不存在的题返回 404", e.code == 404, f"HTTP {e.code}")

# ---------------------------------------------------------------- 3 提交与判题
print("\n[3] 提交判题（走完整的 HTTP → 队列 → worker 链路）")


def submit_and_wait(code: str, problem_id: int, interpreter: str = "py313",
                    timeout: float = 60.0) -> dict:
    r = req("POST", "/api/submissions", {
        "problem_id": problem_id, "code": code,
        "lang": "python", "interpreter": interpreter,
    })
    sid = r["id"]
    t0 = time.time()
    while time.time() - t0 < timeout:
        s = req("GET", f"/api/submissions/{sid}")
        if s["verdict"] not in ("pending", "judging"):
            return s
        time.sleep(0.3)
    return req("GET", f"/api/submissions/{sid}")


# 找 A+B 那道题
ab = next((p for p in items if "A+B" in p["title"]), items[0])

s = submit_and_wait("import sys\na, b = map(int, sys.stdin.read().split())\nprint(a + b)\n", ab["id"])
check("正确解 -> AC", s["verdict"] == "AC",
      f"{s['verdict']} {s['passed']}/{s['total']}  {s['time_ms']}ms")
check("结果带回逐用例明细", len(s.get("cases") or []) == 5, f"{len(s.get('cases') or [])} 条")

s = submit_and_wait("import sys\na, b = map(int, sys.stdin.read().split())\nprint(a * b)\n", ab["id"])
check("错误解 -> WA", s["verdict"] == "WA", f"{s['verdict']} {s['passed']}/{s['total']}")

s = submit_and_wait("while True:\n    pass\n", ab["id"], timeout=90)
check("死循环 -> TLE", s["verdict"] == "TLE", f"{s['verdict']}  {s['message'][:50]}")

s = submit_and_wait("import sys\nprint(1 // 0)\n", ab["id"])
check("除零 -> RE", s["verdict"] == "RE", f"{s['verdict']}  {s['message'][:60]}")

s = submit_and_wait("print('hello')\n", ab["id"])
check("输出多余内容 -> WA", s["verdict"] == "WA", f"{s['verdict']}")

# Thonny 的 3.14 环境
s = submit_and_wait("import sys\na, b = map(int, sys.stdin.read().split())\nprint(a + b)\n",
                    ab["id"], interpreter="py314")
check("3.14（Thonny 环境）提交 -> AC", s["verdict"] == "AC",
      f"{s['verdict']} 解释器={s['interpreter']}")

# 空代码
try:
    req("POST", "/api/submissions", {"problem_id": ab["id"], "code": "   "})
    check("空代码被拒", False, "居然收下了")
except urllib.error.HTTPError as e:
    check("空代码被拒（400）", e.code == 400, f"HTTP {e.code}")

# ---------------------------------------------------------------- 4 统计
print("\n[4] 统计")
st = req("GET", "/api/stats")
check("统计接口可用", st.get("submissions", 0) >= 5,
      f"题 {st['problems']} / 提交 {st['submissions']} / 通过 {st['accepted']}")

print("\n" + "=" * 72)
print(f"通过 {len(_ok)} 项，失败 {len(_bad)} 项")
if _bad:
    print("失败清单：")
    for b in _bad:
        print("  -", b)
print("=" * 72)
sys.exit(1 if _bad else 0)
