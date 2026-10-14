"""前端判题驱动 —— Node 与浏览器共用同一份。

和 `app/judge/runner_python.py` 的区别**只有一个**：

| | 现有后端 | 这里 |
|---|---|---|
| 怎么执行 | 起子进程 `python main.py` | 同一个解释器里 `exec()` |
| stdin/stdout | 真实管道 | `io.StringIO` 替换 `sys.stdin/out` |
| 判题口径 | `compare.compare()` | **同一份 `compare.py`，原样 import** |

也就是说：**判题口径零重写**，只有「执行方式」换了。这样前端判出来的
AC/WA 才和后端一致 —— 换个口径重写一遍，两边必然对不上。

为什么返回 JSON 字符串而不是 dict：跨 JS/Python 传参时，字符串最不容易踩
类型转换的坑（dict → PyProxy 还要手动 toJs）。
"""
from __future__ import annotations

import io
import json
import sys
import time
import traceback

import compare as _cmp

SRC_NAME = "main.py"


def run_code(source: str, stdin_text: str) -> dict:
    """执行源码并捕获输出。等价于后端跑一次 `python main.py`。"""
    saved = (sys.stdin, sys.stdout, sys.stderr)
    out_buf = io.StringIO()
    err_buf = io.StringIO()
    sys.stdin = io.StringIO(stdin_text)
    sys.stdout = out_buf
    sys.stderr = err_buf

    status = "OK"
    detail = ""
    code = None
    try:
        code = compile(source, SRC_NAME, "exec")
    except SyntaxError:
        status, detail = "CE", traceback.format_exc()
    except ValueError as exc:            # 源码里有 NUL 字节之类
        status, detail = "CE", "SyntaxError: %s" % exc

    if code is not None:
        try:
            exec(code, {"__name__": "__main__", "__file__": SRC_NAME})
        except SystemExit:
            pass                          # 程序自己 sys.exit() 算正常结束
        except BaseException:
            status, detail = "RE", traceback.format_exc()

    out, err = out_buf.getvalue(), err_buf.getvalue()
    sys.stdin, sys.stdout, sys.stderr = saved
    return {"status": status, "stdout": out, "stderr": err, "detail": detail}


def judge(source: str, stdin_text: str, expected: str,
          checker: str = "standard", eps: float = 1e-6) -> str:
    """判一个用例，返回 JSON 字符串。"""
    t0 = time.perf_counter()
    r = run_code(source, stdin_text)
    ms = (time.perf_counter() - t0) * 1000.0

    verdict = r["status"]
    detail = r["detail"]
    if verdict == "OK":
        res = _cmp.compare(expected, r["stdout"], checker, eps)
        if res.ok:
            verdict = "AC"
        else:
            verdict = "PE" if res.kind == "pe" else "WA"
        detail = res.detail

    return json.dumps({
        "verdict": verdict,
        "ms": round(ms, 2),
        "detail": detail,
        "stdout": r["stdout"],
        "stderr": r["stderr"],
    }, ensure_ascii=False)
