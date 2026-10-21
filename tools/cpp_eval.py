# -*- coding: utf-8 -*-
"""真机跑 C++ 片段 —— 让「输出是什么」这类答案由 g++ 算出来，而不是手写。

用法（在生成器里）：

    from cpp_eval import run_cpp
    out = run_cpp('''
        #include <iostream>
        int main(){ std::cout << 1+2 << "\\n"; }
    ''')

为什么要有它
------------
C++ 理论题里一大类是「这段代码输出什么」。手算能对，但连着写几十道必然会出现
把 `++i + i++` 算错、把整型提升记错的情况 —— 而且错得很隐蔽：题面、选项、
解析三处会一起错，学生反而被教错。所以这类答案一律**真编译真运行**得到。

实现要点
--------
- 编译缓存：同源码（sha1）只编一次，生成器反复重跑也快；
- 源码写临时目录（data/tmp/cpp_eval），不污染题库目录；
- 编译失败直接抛异常 —— 生成阶段就炸掉，别把编不过的代码写进题库；
- 返回值做 rstrip("\n")，比较时不受末尾换行影响。
"""
from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / "data" / "tmp" / "cpp_eval"

GPP = r"D:\Programs\mingw64\bin\g++.exe"
CACHE: dict[str, str] = {}


def run_cpp(src: str, stdin_text: str = "", *, std_flags: str = "-std=c++17") -> str:
    """编译并运行一段完整 C++ 源码，返回标准输出（去掉末尾换行）。"""
    key = hashlib.sha1((std_flags + "\x00" + src + "\x00" + stdin_text).encode("utf-8")).hexdigest()[:16]
    if key in CACHE:
        return CACHE[key]

    TMP.mkdir(parents=True, exist_ok=True)
    cpp = TMP / ("s_%s.cpp" % key)
    exe = TMP / ("s_%s.exe" % key)
    cpp.write_text(src, encoding="utf-8")
    cp = subprocess.run([GPP, std_flags, "-O0", "-o", str(exe), str(cpp)],
                        capture_output=True, text=True, encoding="utf-8", errors="replace")
    if cp.returncode != 0:
        raise RuntimeError("C++ 片段编译失败：\n%s\n--- 源码 ---\n%s" % (cp.stderr, src))
    rp = subprocess.run([str(exe)], input=stdin_text, capture_output=True, text=True,
                        encoding="utf-8", errors="replace", timeout=20)
    if rp.returncode != 0:
        raise RuntimeError("C++ 片段运行非零退出（%d）：\n%s" % (rp.returncode, rp.stderr))
    out = (rp.stdout or "").replace("\r\n", "\n").rstrip("\n")
    CACHE[key] = out
    return out


def gcc_available() -> bool:
    return Path(GPP).exists()


if __name__ == "__main__":                       # 自检
    print("g++:", GPP, "存在" if gcc_available() else "缺失")
    demo = '#include <iostream>\nint main(){ int i=0; std::cout << (i++ + ++i) << "\\n"; }\n'
    print("i++ + ++i =", run_cpp(demo))
    sys.exit(0 if gcc_available() else 1)
