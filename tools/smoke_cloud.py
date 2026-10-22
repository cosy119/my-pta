# -*- coding: utf-8 -*-
"""云端启动路径自检 —— 真的按云平台的方式把服务拉起来跑一遍。

**为什么单独写这一个**

Dockerfile 和 render.yaml 早就写好了，但「云端那条启动分支」
（`PTA_CLOUD=1` + 平台注入 `$PORT`）**从来没有被真跑过**，于是攒下两个一部署就炸的 bug：

1. `run.py` 的云分支里 `config` 根本没被导入 → `NameError`，进程起来就退出。
   本地双击 `run.bat` 走的是另一条分支，永远碰不到。
2. 绑定地址会落到 `127.0.0.1` → 容器内部自己连得通、平台健康检查连不上，
   部署直接判「不健康」。

`e2e_ui.py` / `selfcheck.py` 都抓不到这两个 —— 它们默认「服务已经手动起好了」。
所以必须单独立一个脚本，自己负责把服务按云端的方式拉起来。

**它断言什么**

- 云分支能起来（不再是 NameError），且在超时内变成 healthy
- **绑的是 `0.0.0.0`**、health 报的端口 = 我们给的 `$PORT`
- 静态前端拿得到（GET `/` 返回 200）
- 三科目目录齐：python 56 / ds 31 / linux 117
- ★ **C++ 与 Python 各交一次，都要 AC**
  —— 这一条是给容器镜像把关的：镜像里没装 g++ 就会 CE，
  `config/settings.toml` 里那串 Windows 路径在 Linux 上不存在，
  必须靠兜底探测（`which g++`）自己找 —— 找不到就判不过。

跑法：
    python tools/smoke_cloud.py
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
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import _console                                                   # noqa: E402

_ok: list[str] = []
_bad: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    (_ok if ok else _bad).append(name)
    print(("  [OK]   " if ok else "  [FAIL] ") + name
          + (("  -- " + str(detail)) if detail else ""))


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


# 绕过环境代理：本机 HTTP_PROXY 会让 127.0.0.1 的请求也走代理
_OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def http(path: str, body: dict | None = None, token: str = "smoke-cloud",
         base: str = "") -> tuple[int, object]:
    url = base + path
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data,
                                 method="POST" if data is not None else "GET")
    req.add_header("X-User-Token", token)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with _OPENER.open(req, timeout=20) as r:
            raw = r.read().decode("utf-8", "replace")
            try:
                return r.status, json.loads(raw)
            except json.JSONDecodeError:
                return r.status, raw
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except Exception as e:  # noqa: BLE001
        return 0, "%s: %s" % (type(e).__name__, e)


# 判题还没出结论时的中间态（worker 会先把 verdict 写成 judging）
_NOT_DONE = {"", "PD", "pending", "judging", "queued", "running"}


def wait_verdict(sid: int, base: str, timeout_s: float = 180.0) -> tuple[str, str]:
    """轮询到出结论为止。返回 (verdict, detail)。"""
    t1 = time.time()
    while time.time() - t1 < timeout_s:
        st, s = http("/api/submissions/%d?with_cases=1" % sid, base=base)
        if isinstance(s, dict) and str(s.get("verdict") or "").lower() not in _NOT_DONE:
            return str(s.get("verdict") or ""), str(s.get("detail") or "")
        time.sleep(1.0)
    return "TIMEOUT", "等待 %ss 仍无结论" % int(timeout_s)


def kill_tree(proc: subprocess.Popen) -> None:
    if proc.poll() is not None:
        return
    if os.name == "nt":
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                       capture_output=True)
    else:
        import signal
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except Exception:  # noqa: BLE001
            proc.kill()


def main() -> int:
    port = free_port()
    db = ROOT / "data" / "_smoke_cloud.db"
    for suffix in ("", "-wal", "-shm"):
        p = Path(str(db) + suffix)
        if p.exists():
            p.unlink()

    env = dict(os.environ)
    env.update({
        "PTA_CLOUD": "1",              # ← 关键：走云端分支
        "PORT": str(port),
        "PTA_DB": str(db),
        "PTA_LOGS": str(ROOT / "data" / "logs"),
        "PTA_TMP_JUDGE": str(ROOT / "data" / "tmp" / "judge_cloud"),
        "PYTHONUNBUFFERED": "1",
    })
    # 清掉可能干扰的变量，保证确实是"只有 PORT + PTA_CLOUD"这条路
    env.pop("HOST", None)

    base = "http://127.0.0.1:%d" % port

    print("=" * 72)
    print("云端启动路径自检")
    print("  命令: python run.py")
    print("  环境: PTA_CLOUD=1  PORT=%d  （照着 Render/Railway/Fly 的约定）" % port)
    print("  库  : %s" % db)
    print("=" * 72)

    log: list[str] = []
    kwargs: dict = dict(cwd=str(ROOT), env=env, stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT, text=True,
                        encoding="utf-8", errors="replace", bufsize=1)
    if os.name != "nt":
        kwargs["start_new_session"] = True
    proc = subprocess.Popen([sys.executable, str(ROOT / "run.py")], **kwargs)

    def drain() -> None:
        assert proc.stdout is not None
        for line in proc.stdout:
            log.append(line.rstrip("\n"))

    threading.Thread(target=drain, daemon=True).start()

    # ---------- 1. 等它 healthy ----------
    t0 = time.time()
    healthy = False
    while time.time() - t0 < 90:
        if proc.poll() is not None:
            break
        st, body = http("/api/health", base=base)
        if st == 200 and isinstance(body, dict) and body.get("ok"):
            healthy = True
            break
        time.sleep(0.5)

    exited = proc.poll()

    check("云端分支能起来（不再是 config 的 NameError）",
          exited is None,
          "进程已退出，exit=%s；输出见下" % exited if exited is not None else "")
    check("90 秒内 /api/health 变 healthy", healthy,
          "" if healthy else "没等到；最后 6 行日志：\n" + "\n".join(log[-6:]))

    if not healthy:
        kill_tree(proc)
        print("\n----- 子进程完整输出 -----")
        print("\n".join(log[-40:]))
        print("-" * 72)
        print("通过 %d / %d" % (len(_ok), len(_ok) + len(_bad)))
        return 1

    # ---------- 2. health 自述 ----------
    st, body = http("/api/health", base=base)
    check("health 报的 host 是 0.0.0.0（不是 127.0.0.1）",
          isinstance(body, dict) and body.get("host") == "0.0.0.0",
          "实际 host=%r" % (body.get("host") if isinstance(body, dict) else body))
    check("health 报的 port 等于平台注入的 $PORT",
          isinstance(body, dict) and int(body.get("port") or 0) == port,
          "期望 %d，实际 %r" % (port, body.get("port") if isinstance(body, dict) else body))
    check("数据库指向我们指定的测试库",
          isinstance(body, dict) and str(body.get("db", "")).replace("\\", "/").endswith("_smoke_cloud.db"),
          str(body.get("db") if isinstance(body, dict) else body))

    # ---------- 3. 静态前端 ----------
    st, html = http("/", base=base)
    check("GET / 返回 200 且确实是这个平台的前端",
          st == 200 and isinstance(html, str) and "cosy 题集" in html,
          "status=%s len=%s" % (st, len(html) if isinstance(html, str) else "-"))

    # ---------- 4. 三科目目录 ----------
    st, cat = http("/api/catalog", base=base)
    got: dict[str, tuple[int, int]] = {}
    if isinstance(cat, dict):
        for s in cat.get("subjects") or []:
            got[s.get("key")] = (s.get("total"), s.get("max_score"))
    from app.seed import SEED_PROBLEMS  # noqa: E402
    expected: dict[str, tuple[int, int]] = {}
    for p in SEED_PROBLEMS:
        subject = p.get("subject", "python")
        count, score = expected.get(subject, (0, 0))
        expected[subject] = (count + 1, score + int(p.get("total_score") or 100))
    check("目录与当前种子题库的题数及总分一致",
          got == expected and set(got) == set(expected),
          "实际=%s 预期=%s" % (got, expected))

    # ---------- 5. ★ 真编真跑：C++ 与 Python 各来一发 ----------
    from app.problems_bank import BANK_PROBLEMS                 # noqa: E402
    from app.problems_bank_ds import DS_PROBLEMS                # noqa: E402
    from app.problems_bank_ds_tricks import DS_TRICKS_PROBLEMS  # noqa: E402
    from app.problems_bank_ds_theory import DS_THEORY_PROBLEMS  # noqa: E402
    from app.problems_bank_py_theory import PY_THEORY_PROBLEMS  # noqa: E402
    from app.problems_bank_py_tricks import PY_TRICKS_PROBLEMS  # noqa: E402
    from app.problems_bank_py_prog import PY_PROG_PROBLEMS      # noqa: E402
    from app.problems_bank_ds_prog import DS_PROG_PROBLEMS     # noqa: E402
    from app.problems_bank_cpp_tricks import CPP_TRICKS_PROBLEMS  # noqa: E402
    from app.problems_bank_cpp_prog import CPP_PROG_PROBLEMS   # noqa: E402
    from app.problems_bank_cpp_theory import CPP_THEORY_PROBLEMS  # noqa: E402
    from app.problems_bank_cpp_theory2 import CPP_THEORY2_PROBLEMS  # noqa: E402
    from app.seed import CORE_PROBLEMS                          # noqa: E402

    # C++ 基础编程题册（按册生成，逐册可选，单册缺失不拖垮冒烟）
    CPP_BASIC_PROBLEMS: list[dict] = []
    for _n in range(1, 9):
        try:
            _m = __import__("app.problems_bank_cpp_basic%d" % _n, fromlist=["x"])
            CPP_BASIC_PROBLEMS += list(getattr(_m, "CPP_BASIC%d_PROBLEMS" % _n))
        except Exception:
            pass

    def ref_of(title: str) -> str:
        # ★ 技巧特训 / 理论题 / 编程精练章的题按分节名排在前头，会被「第一道 xx 题」选中——
        #   所以这里必须把各条附加库都搜进来（2026-10-18、10-19、10-21 各踩过一次）
        for p in (list(CPP_TRICKS_PROBLEMS) + list(CPP_PROG_PROBLEMS)
                  + list(CPP_THEORY_PROBLEMS) + list(CPP_THEORY2_PROBLEMS)
                  + list(CPP_BASIC_PROBLEMS)
                  + list(DS_TRICKS_PROBLEMS) + list(PY_TRICKS_PROBLEMS)
                  + list(DS_THEORY_PROBLEMS) + list(PY_THEORY_PROBLEMS)
                  + list(DS_PROG_PROBLEMS) + list(PY_PROG_PROBLEMS)
                  + list(DS_PROBLEMS) + list(CORE_PROBLEMS) + list(BANK_PROBLEMS)):
            if p.get("title") == title:
                return p.get("reference_solution") or ""
        return ""

    # DS 线既有 cpp 编程题也有 text 理论题（2026-10-15 起）。试编译必须挑
    # line == "cpp" 的编程题 —— 把理论题的字母答案喂给 g++ 只会收获 CE。
    st, plist = http("/api/problems?subject=ds", base=base)
    items = (plist or {}).get("items") if isinstance(plist, dict) else None
    items = items or []
    ds_item = next((x for x in items if str(x.get("line")) == "cpp"), None)

    if not ds_item:
        check("找到一道数据结构题用来试编译", False, str(plist)[:200])
    else:
        code = ref_of(ds_item["title"])
        check("能取到该题的参考解（用于试编译）", bool(code), ds_item["title"])
        if code:
            st, sub = http("/api/submissions",
                           {"problem_id": ds_item["id"], "code": code,
                            "lang": "cpp", "interpreter": "gpp"}, base=base)
            sid = (sub or {}).get("id") if isinstance(sub, dict) else None
            check("提交 C++ 代码被受理", bool(sid), str(sub)[:200])
            if sid:
                verdict, detail = wait_verdict(sid, base)
                check("★ C++ 真编过并 AC（证明 g++ 在 PATH 上被兜底探测找到了）",
                      verdict == "AC", "verdict=%s  %s" % (verdict, detail[:160]))

    st, plist = http("/api/problems?subject=python", base=base)
    items = (plist or {}).get("items") if isinstance(plist, dict) else None
    # 科目列表包含理论题；按执行通道选编程题，不依赖章节排序。
    py_item = next((x for x in (items or []) if str(x.get("line")) == "python"), None)
    if not py_item:
        check("找到一道 Python 编程题用来试跑", False, str(plist)[:200])
    else:
        code = ref_of(py_item["title"])
        if not code:
            check("能取到该题的参考解（Python）", False, py_item["title"])
        else:
            st, sub = http("/api/submissions",
                           {"problem_id": py_item["id"], "code": code,
                            "lang": "python", "interpreter": "py313"}, base=base)
            sid = (sub or {}).get("id") if isinstance(sub, dict) else None
            check("提交 Python 代码被受理", bool(sid), str(sub)[:200])
            if sid:
                verdict, detail = wait_verdict(sid, base, timeout_s=150)
                check("★ Python 真跑过并 AC（证明解释器路径兜底探测有效）",
                      verdict == "AC", "verdict=%s  %s" % (verdict, detail[:160]))

    # ---------- 收尾 ----------
    kill_tree(proc)
    time.sleep(0.8)

    # 服务器日志里不该出现 traceback
    noisy = [ln for ln in log if "Traceback" in ln or "NameError" in ln]
    check("服务器日志里没有 Traceback / NameError", not noisy,
          " | ".join(noisy[:3]))

    for suffix in ("", "-wal", "-shm"):
        p = Path(str(db) + suffix)
        try:
            if p.exists():
                p.unlink()
        except OSError:
            pass

    print()
    print("通过 %d / %d" % (len(_ok), len(_ok) + len(_bad)))
    if _bad:
        print("失败项：")
        for b in _bad:
            print("  -", b)
    return 0 if not _bad else 1


if __name__ == "__main__":
    raise SystemExit(main())
