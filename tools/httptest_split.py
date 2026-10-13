"""模拟「GitHub Pages 前端 + 独立后端」的端到端自检。

为什么要单独测这个：真实的部署形态是**两个源**
- 前端：静态文件（模拟 Pages，本脚本用 8888 端口伺服 docs/）
- 后端：判题 API（8799 端口）

跨源会踩到的问题，本地同源跑是**测不出来**的：
- CORS 预检（带自定义头 X-User-Token 的 POST 会触发 OPTIONS 预检）
- 前端能不能正确拼后端地址

用法：python tools/httptest_split.py
"""
from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
sys.path.insert(0, str(ROOT))

API_PORT = 8799
WEB_PORT = 8888
API = f"http://127.0.0.1:{API_PORT}"
WEB = f"http://127.0.0.1:{WEB_PORT}"

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


def wait_http(url: str, timeout: float = 40.0) -> bool:
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with urllib.request.urlopen(url, timeout=2) as r:
                if r.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(0.4)
    return False


def raw_request(url: str, method: str = "GET", headers: dict | None = None,
                body: bytes | None = None) -> tuple[int, dict, str]:
    r = urllib.request.Request(url, data=body, method=method)
    for k, v in (headers or {}).items():
        r.add_header(k, v)
    try:
        with urllib.request.urlopen(r, timeout=30) as resp:
            return resp.status, dict(resp.headers), resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read().decode("utf-8", "replace")


def main() -> int:
    from app import db
    from app import users as _users

    # ---- 1. 起后端 ----
    log = ROOT / "data" / "logs" / "httptest_split.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    lf = open(log, "w", encoding="utf-8")

    run_env = dict(os.environ)
    run_env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8",
                    "PTA_ALLOW_ORIGINS": f"http://127.0.0.1:{WEB_PORT}"})

    api_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app",
         "--host", "127.0.0.1", "--port", str(API_PORT), "--log-level", "warning"],
        cwd=str(ROOT), stdout=lf, stderr=subprocess.STDOUT, env=run_env)

    # ---- 2. 起静态站（模拟 GitHub Pages）----
    handler = partial(SimpleHTTPRequestHandler, directory=str(DOCS))
    httpd = ThreadingHTTPServer(("127.0.0.1", WEB_PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()

    try:
        print("[1] 起两个源")
        ok_api = wait_http(API + "/api/health")
        check("后端就绪", ok_api, API)
        check("静态站就绪（模拟 Pages）", (WEB + "/index.html") and
              wait_http(WEB + "/index.html", 10), WEB)
        if not ok_api:
            lf.flush()
            print(log.read_text(encoding="utf-8", errors="replace")[-1500:])
            return 1

        print("\n[2] 静态站能提供前端 + 题库")
        code, _, body = raw_request(WEB + "/index.html")
        check("index.html 可访问", code == 200 and "<script>" in body, f"HTTP {code}")
        code, _, body = raw_request(WEB + "/problems.json")
        try:
            bank = json.loads(body)
            n = bank.get("count")
        except Exception:
            n = 0
        check("problems.json 可访问且是合法 JSON", code == 200 and n == 56,
              f"HTTP {code} · {n} 题")
        check("静态题库不含参考解", "reference_solution" not in body, "")

        print("\n[3] ★ 跨源 CORS（本地同源测不出来的部分）")
        origin = WEB
        # 3a 简单请求
        code, hdrs, _ = raw_request(
            API + "/api/problems", headers={"Origin": origin,
                                            "X-User-Token": "a" * 32})
        acao = hdrs.get("access-control-allow-origin") or hdrs.get("Access-Control-Allow-Origin")
        check("GET 带 Origin → 回 CORS 头", code == 200 and bool(acao),
              f"HTTP {code} ACAO={acao}")
        check("ACAO 是我们要的源（或者通配 *）",
              acao in (origin, "*"), str(acao))

        # 3b 预检请求（POST + 自定义头会触发）
        code, hdrs, _ = raw_request(
            API + "/api/submissions", method="OPTIONS",
            headers={"Origin": origin,
                     "Access-Control-Request-Method": "POST",
                     "Access-Control-Request-Headers": "content-type,x-user-token"})
        allow_h = (hdrs.get("access-control-allow-headers")
                   or hdrs.get("Access-Control-Allow-Headers") or "")
        check("★ OPTIONS 预检通过（200/204）", code in (200, 204), f"HTTP {code}")
        check("预检允许 x-user-token 头",
              "x-user-token" in allow_h.lower() or allow_h == "*", allow_h)

        # 3c 预检之后真的能跨源 POST
        tok = "cc" * 16
        pid = db.query_one("SELECT id FROM problems WHERE title=?", ("A+B 问题",))["id"]
        payload = json.dumps({"problem_id": pid,
                              "code": "import sys\na,b=map(int,sys.stdin.read().split())\nprint(a+b)\n",
                              "lang": "python", "interpreter": "py313"}).encode()
        code, _, body = raw_request(
            API + "/api/submissions", method="POST",
            headers={"Origin": origin, "Content-Type": "application/json",
                     "X-User-Token": tok}, body=payload)
        sid = json.loads(body).get("id") if code == 200 else None
        check("★ 跨源 POST 提交成功", code == 200 and sid, f"HTTP {code} sid={sid}")

        # 等判完
        verdict = None
        for _ in range(60):
            c, _, b = raw_request(API + f"/api/submissions/{sid}",
                                  headers={"Origin": origin, "X-User-Token": tok})
            v = json.loads(b).get("verdict")
            if v not in ("pending", "judging", None):
                verdict = v
                break
            time.sleep(0.5)
        check("跨源提交能判完并拿到结果", verdict == "AC", str(verdict))

        print("\n[4] 前端 JS 里没有硬编码同源假设")
        html = (DOCS / "index.html").read_text(encoding="utf-8")
        check("有「后端地址」设置项", "pta.backend" in html, "")
        check("请求会自动带 X-User-Token", "X-User-Token" in html, "")
        check("支持 ?api= 一次性指定后端", 'get("api")' in html, "")
        check("后端连不上时降级读静态题库", "problems.json" in html, "")
        check("有本地草稿（离线也不丢代码）", "pta.draft." in html, "")
        check("有本地进度镜像", "pta.localProgress" in html, "")

        print("\n[5] 身份与进度（跨源情况下仍然隔离）")
        t1, t2 = "11" * 16, "22" * 16
        _, _, b1 = raw_request(API + "/api/me",
                               headers={"Origin": origin, "X-User-Token": t1})
        _, _, b2 = raw_request(API + "/api/me",
                               headers={"Origin": origin, "X-User-Token": t2})
        check("两个 token 是两个身份",
              json.loads(b1)["id"] != json.loads(b2)["id"],
              f"{json.loads(b1)['id']} vs {json.loads(b2)['id']}")

    finally:
        httpd.shutdown()
        api_proc.terminate()
        try:
            api_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            api_proc.kill()
        lf.close()

    print("\n" + "=" * 72)
    print(f"通过 {_passed} 项，失败 {_failed} 项")
    print("=" * 72)
    return 0 if _failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
