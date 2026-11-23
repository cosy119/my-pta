"""本地伺服 `docs/`（静态站产物），把 `.mjs` 的 MIME 修对。

为什么需要它
------------
`python -m http.server` 在 Windows 上会把 `.mjs` 当成 `text/plain`
（Python 的 mimetypes 表 + 系统注册表都没登记这个扩展名）。

后果不是「样式不对」这种小事：`python-worker.js` 是 **module worker**，
里面 `import { loadPyodide } from './pyodide/pyodide.mjs'` —— 浏览器按 MIME
判断模块，`text/plain` 一律拒绝执行，页面只会报一句
「Python Worker 加载失败」，看起来像判题坏了。

GitHub Pages 返回 `text/javascript`，**线上没有这个问题**，纯本机开发的坑。
（`tools/ui_e2e_local_engines.mjs` 自己维护了 MIME 表，也是同一个原因。）

用法
----
    python tools/serve_docs.py              # http://127.0.0.1:8801/
    python tools/serve_docs.py 8802 docs    # 换端口 / 换目录

配套的 SW 回归测试：
    python tools/serve_docs.py 8802 docs &
    PTA_LOCAL=http://127.0.0.1:8802/ node tools/ui_test_sw_cache.mjs
"""
from __future__ import annotations

import functools
import http.server
import mimetypes
import sys
from pathlib import Path

mimetypes.add_type("text/javascript", ".mjs")
mimetypes.add_type("text/javascript", ".js")
mimetypes.add_type("application/wasm", ".wasm")


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".mjs": "text/javascript",
        ".js": "text/javascript",
        ".wasm": "application/wasm",
        ".json": "application/json",
    }

    def end_headers(self):
        # 本地调试就该永远拿最新的：顺着 Pages 那套 max-age=600 会让人怀疑人生
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):        # 请求日志太吵，只留错误
        pass


def main() -> int:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8801
    root = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("docs")
    if not (root / "index.html").is_file():
        print("目录里没有 index.html：%s（先跑 tools/export_static.py --with-cases）" % root)
        return 2
    handler = functools.partial(Handler, directory=str(root))
    with http.server.ThreadingHTTPServer(("127.0.0.1", port), handler) as httpd:
        print("serving %s at http://127.0.0.1:%d/  （.mjs → text/javascript）" % (root, port))
        print("按 Ctrl+C 停止")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n已停止")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
