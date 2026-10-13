"""本地 AI 出题 + 批改平台 —— 启动器。

双击 run.bat 会调用本文件，做四件事：

1. 先探测 127.0.0.1:8765 有没有人在监听
   - 有 → 说明服务已经在跑，**直接打开浏览器**，本窗口随即退出（不报错）
   - 没有 → 往下走
2. 后台线程轮询 /api/health，服务一就绪就打开默认浏览器
3. 前台跑 uvicorn（阻塞，关掉窗口 = 停服务，Ctrl+C 也可以）
4. 任何启动失败都打印原因并等你按键，**不让窗口一闪而过**

日志同时写一份到 data/logs/server.log，方便出问题时回看。
"""
from __future__ import annotations

import socket
import sys
import threading
import time
import webbrowser
from datetime import datetime
from pathlib import Path

HOST = "127.0.0.1"
PORT = 8765
URL = "http://%s:%d" % (HOST, PORT)

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LOG_DIR = ROOT / "data" / "logs"
LOG_FILE = LOG_DIR / "server.log"


# --------------------------------------------------------------------------- #
# 小工具
# --------------------------------------------------------------------------- #
def say(msg: str = "") -> None:
    """同时打印到控制台和日志文件。"""
    print(msg, flush=True)
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write("%s %s\n" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg))
    except Exception:
        pass


def port_in_use(host: str = HOST, port: int = PORT, timeout: float = 0.6) -> bool:
    """能不能连上这个端口 —— 能连上就说明有服务在监听。"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        return s.connect_ex((host, port)) == 0


def wait_healthy(deadline_s: float = 40.0) -> bool:
    """/api/health 返回 200 就算就绪。"""
    import urllib.request

    t0 = time.time()
    while time.time() - t0 < deadline_s:
        try:
            with urllib.request.urlopen(URL + "/api/health", timeout=1.5) as r:
                if getattr(r, "status", 200) == 200:
                    return True
        except Exception:
            pass
        time.sleep(0.3)
    return False


def open_browser_when_ready() -> None:
    if wait_healthy():
        say("[i] Server is healthy -> opening browser: %s" % URL)
        try:
            opened = webbrowser.open(URL)
            if not opened:
                say("[!] Could not auto-open a browser. Please open manually: %s" % URL)
        except Exception as e:  # noqa: BLE001
            say("[!] Auto-open failed (%s). Please open manually: %s" % (e, URL))
    else:
        say("[!] Server did not become healthy in time. Check the log above.")


def pause_if_interactive() -> None:
    """双击运行时窗口不会立刻消失。"""
    try:
        if sys.stdin and sys.stdin.isatty():
            input("Press Enter to close this window ...")
    except Exception:
        pass


# --------------------------------------------------------------------------- #
# 主流程
# --------------------------------------------------------------------------- #
def main() -> int:
    say("=" * 60)
    say("  Local AI problem-generating + judging platform")
    say("  %s" % URL)
    say("=" * 60)

    # ---- 1. 端口已被占用？分两种情况，别一律当成「服务在跑」 ----
    if port_in_use():
        if wait_healthy(deadline_s=3.0):
            say("[i] Port %d is already serving this platform -> opening browser." % PORT)
            say("[i] Nothing else to do; the running server keeps serving.")
            try:
                opened = webbrowser.open(URL)
            except Exception as e:  # noqa: BLE001
                opened = False
                say("[!] Auto-open failed: %s" % e)
            if not opened:
                say("[!] Could not auto-open a browser. Open manually: %s" % URL)
                pause_if_interactive()   # 别把唯一的线索一起关掉
                return 0
            say("[i] This window will close in 3 seconds.")
            time.sleep(3)
            return 0

        # 端口被别的程序占了 —— 这时不能装作没事，否则浏览器打开也是白页
        say("[ERROR] Port %d is occupied by ANOTHER program." % PORT)
        say("        It is NOT this platform (%s/api/health does not answer)." % URL)
        say("")
        say("        Options:")
        say("          a) Find and close whatever is using the port:")
        say("             netstat -ano | findstr :%d" % PORT)
        say("             taskkill /F /PID <the pid from above>")
        say("          b) Or change PORT at the top of run.py to e.g. 8766,")
        say("             and use http://127.0.0.1:8766 afterwards.")
        pause_if_interactive()
        return 1

    # ---- 2. 服务就绪后自动开浏览器（后台线程，不阻塞） ----
    threading.Thread(target=open_browser_when_ready, daemon=True).start()

    # ---- 3. 前台跑 uvicorn ----
    try:
        import uvicorn
        from app.main import app as fastapi_app
    except Exception as e:  # noqa: BLE001
        say("[ERROR] Failed to import the application: %s: %s" % (type(e).__name__, e))
        import traceback
        say(traceback.format_exc())
        say("")
        say("Hint: make sure dependencies are installed, e.g.")
        say('      "D:\\Pythontools\\Python\\python.exe" -m pip install fastapi uvicorn openai httpx')
        pause_if_interactive()
        return 1

    say("[i] Starting uvicorn on %s ..." % URL)
    say("[i] Keep this window open while you use the platform.")
    say("[i] Press Ctrl+C (or close the window) to stop.")
    say("")

    try:
        uvicorn.run(fastapi_app, host=HOST, port=PORT, log_level="info")
    except KeyboardInterrupt:
        say("")
        say("[i] Stopped by user. Bye.")
        return 0
    except Exception as e:  # noqa: BLE001
        say("")
        say("[ERROR] Server crashed: %s: %s" % (type(e).__name__, e))
        import traceback
        say(traceback.format_exc())
        pause_if_interactive()
        return 1

    say("")
    say("[i] Server stopped normally.")
    pause_if_interactive()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except BaseException as e:  # noqa: BLE001
        say("[ERROR] Unhandled: %s: %s" % (type(e).__name__, e))
        import traceback
        say(traceback.format_exc())
        pause_if_interactive()
        raise SystemExit(1)
