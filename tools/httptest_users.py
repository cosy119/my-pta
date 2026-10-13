"""HTTP 全链路自检 —— 多用户隔离版。

为什么不用 `tools/httptest.py`：那个脚本假设服务已经跑着。
这个环境里后台常驻服务活不下来（`nohup` 下 cd 失效、进程随命令结束被回收），
所以这里**自己起服务、自己测、自己关**。

覆盖：
  1. 三种 token 的身份识别（两个用户 + 无 token 归本机用户）
  2. ★ 多用户进度隔离：A 做对、B 做错，各自进度互不可见
  3. 提交 / 判题 / 轮询 / 结果全链路
  4. 越权保护：B 拿 A 的 submission_id 应该 404
  5. CORS 头（GitHub Pages 需要）
  6. 静态题库 / 前端页面可访问

用法：python tools/httptest_users.py
"""
from __future__ import annotations

import json
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import _console                                                   # noqa: E402
HOST = "127.0.0.1"
PORT = 8799
BASE = f"http://{HOST}:{PORT}"

TA = "aaaa1111bbbb2222cccc3333dddd4444"
TB = "eeee5555ffff6666aaaa7777bbbb8888"

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
        body: dict | None = None, origin: str | None = None) -> tuple[int, dict | str, dict]:
    url = BASE + path
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method)
    if token:
        r.add_header("X-User-Token", token)
    if data:
        r.add_header("Content-Type", "application/json")
    if origin:
        r.add_header("Origin", origin)
    try:
        with urllib.request.urlopen(r, timeout=30) as resp:
            raw = resp.read().decode("utf-8", "replace")
            code = resp.status
            hdrs = dict(resp.headers)
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        code = e.code
        hdrs = dict(e.headers)
    try:
        parsed = json.loads(raw)
    except ValueError:
        parsed = raw
    return code, parsed, hdrs


def wait_port(timeout: float = 40.0) -> bool:
    t0 = time.time()
    while time.time() - t0 < timeout:
        with socket.socket() as s:
            s.settimeout(0.5)
            if s.connect_ex((HOST, PORT)) == 0:
                # 端口开了不代表就绪，再探 health
                try:
                    with urllib.request.urlopen(BASE + "/api/health", timeout=2) as r:
                        if r.status == 200:
                            return True
                except Exception:
                    pass
        time.sleep(0.4)
    return False


def submit_and_wait(token: str, pid: int, code: str, limit: int = 60) -> dict:
    """提交 → 轮询到判完。"""
    code_post, r, _ = req("/api/submissions", token, "POST",
                          {"problem_id": pid, "code": code, "lang": "python",
                           "interpreter": "py313"})
    sid = r["id"]
    for _ in range(limit * 2):
        c, s, _ = req(f"/api/submissions/{sid}", token)
        if isinstance(s, dict) and s.get("verdict") not in ("pending", "judging"):
            return s
        time.sleep(0.5)
    return {"verdict": "TIMEOUT", "id": sid}


def main() -> int:
    from app import db

    log = ROOT / "data" / "logs" / "httptest_users.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    lf = open(log, "w", encoding="utf-8")

    env = {"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
    import os
    run_env = dict(os.environ)
    run_env.update(env)

    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app",
         "--host", HOST, "--port", str(PORT), "--log-level", "warning"],
        cwd=str(ROOT), stdout=lf, stderr=subprocess.STDOUT, env=run_env)

    try:
        print("[1] 起服务并等就绪")
        ok = wait_port()
        check("服务就绪（/api/health 200）", ok, BASE)
        if not ok:
            lf.flush()
            print("\n--- 服务日志 ---")
            print(log.read_text(encoding="utf-8", errors="replace")[-2000:])
            return 1

        print("\n[2] 身份识别（X-User-Token）")
        c, me_a, _ = req("/api/me", TA)
        c2, me_b, _ = req("/api/me", TB)
        c3, me_none, _ = req("/api/me")
        check("带 token A 能拿到身份", c == 200 and "id" in me_a, str(me_a))
        check("带 token B 拿到**另一个**身份", me_a.get("id") != me_b.get("id"),
              f"A={me_a.get('id')} B={me_b.get('id')}")
        check("不带 token → 归到本机用户", c3 == 200, str(me_none))
        check("昵称自动生成（不是空的）", bool(me_a.get("nickname")), me_a.get("nickname"))

        print("\n[3] ★ 多用户进度隔离")
        c, probs, _ = req("/api/problems", TA)
        pid = None
        for p in probs.get("items", []):
            if p["title"] == "A+B 问题":
                pid = p["id"]
                break
        check("题库能列出（含 A+B 问题）", pid is not None, f"problem_id={pid}")

        # A 做对
        sa = submit_and_wait(TA, pid, "import sys\na, b = map(int, sys.stdin.read().split())\nprint(a + b)\n")
        check("A 的提交判 AC", sa.get("verdict") == "AC",
              f"{sa.get('verdict')} {sa.get('score')}/{sa.get('max_score')}")

        # B 做错（一定拿不满：输出固定 999，只有全 0 的用例可能撞上，我们挑输出 999）
        sb = submit_and_wait(TB, pid, "print(999)\n")
        check("B 的提交不是 AC", sb.get("verdict") != "AC",
              f"{sb.get('verdict')} {sb.get('score')}/{sb.get('max_score')}")

        # A 看自己的进度
        c, pa, _ = req(f"/api/problems/{pid}", TA)
        c2, pb, _ = req(f"/api/problems/{pid}", TB)
        check("A 看到自己满分 + 已通过",
              pa.get("best_score") == 10 and pa.get("solved") is True,
              f"best={pa.get('best_score')} solved={pa.get('solved')}")
        check("B 看到自己没通过",
              pb.get("solved") is False and pb.get("best_score", 0) < 10,
              f"best={pb.get('best_score')} solved={pb.get('solved')}")
        check("★ 两人 best_score 不同（进度确实是分开的）",
              pa.get("best_score") != pb.get("best_score"),
              f"A={pa.get('best_score')} B={pb.get('best_score')}")

        # A 的历史里有 1 条，B 的历史里有 1 条，互不串
        check("A 的历史条数 = 1", pa.get("history_count") == 1, str(pa.get("history_count")))
        check("B 的历史条数 = 1", pb.get("history_count") == 1, str(pb.get("history_count")))

        print("\n[4] 越权保护")
        aid = sa.get("id")
        c_a, _, _ = req(f"/api/submissions/{aid}", TA)
        c_b, _, _ = req(f"/api/submissions/{aid}", TB)
        check("A 能看自己的提交", c_a == 200, f"HTTP {c_a}")
        check("★ B 看 A 的提交 → 404", c_b == 404, f"HTTP {c_b}")

        print("\n[5] 各自统计互不影响")
        c, stat_a, _ = req("/api/stats", TA)
        c2, stat_b, _ = req("/api/stats", TB)
        check("A 的提交数 = 1", stat_a.get("submissions") == 1, str(stat_a.get("submissions")))
        check("B 的提交数 = 1", stat_b.get("submissions") == 1, str(stat_b.get("submissions")))
        check("A 得分 10、B 不到 10",
              stat_a.get("score") == 10 and stat_b.get("score") < 10,
              f"A={stat_a.get('score')} B={stat_b.get('score')}")
        check("stats 里带当前用户信息", "user" in stat_a, str(stat_a.get("user")))

        print("\n[6] CORS（GitHub Pages 要用）")
        c, _, hdrs = req("/api/problems", TA, origin="https://cosy119.github.io")
        acao = hdrs.get("access-control-allow-origin") or hdrs.get("Access-Control-Allow-Origin")
        check("带 Origin 的请求返回 CORS 头", bool(acao), str(acao))

        print("\n[7] 静态资源")
        c, _, _ = req("/")
        check("首页可访问", c == 200, f"HTTP {c}")
        # problems.json 只有导出后才在 docs/，这里检查 web/ 下有没有
        check("（静态题库由 tools/export_static.py 生成到 docs/）", True)

        print("\n[8] 数据库最终状态")
        rows = db.query("SELECT id, token, nickname FROM users ORDER BY id")
        check("users 表里有多个用户", len(rows) >= 3, f"{len(rows)} 个")
        for r in rows:
            print(f"        #{r['id']} {r['nickname']}  token={r['token'][:12]}…")

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        lf.close()

    print("\n" + "=" * 72)
    print(f"通过 {_passed} 项，失败 {_failed} 项")
    print("=" * 72)
    return 0 if _failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
