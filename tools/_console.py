"""把控制台输出切成 UTF-8。**导入即生效**，不用调用任何函数。

为什么需要它
------------
这些脚本全程打印中文。Windows 上的 Python 默认按**系统 ANSI 代码页**写
stdout —— 中文 Windows 是 cp936（中文能编码，只是可能乱码），
而**英文 Windows 是 cp1252**，遇到中文会当场崩：

    UnicodeEncodeError: 'charmap' codec can't encode characters in position 2-8

2026-10-13 在 GitHub Actions 的 windows runner 上实测踩到：`selftest_sandbox`
打印表头那行就直接 traceback，导致后面所有自检步骤被 skip。
本机一直没暴露，是因为本机开了 `PYTHONUTF8=1` + Windows「Beta: Unicode UTF-8」。

用法：在脚本的 import 区写一行

    import _console  # noqa: F401  —— 导入即生效，统一控制台编码

`errors="replace"` 保证：万一终端真的编不出某个字符，也只会显示成问号，
**绝不让整个自检脚本崩在打印上** —— 自检的价值在于结论，不在于字符完美。
"""
import sys

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        # 流被重定向成不支持 reconfigure 的对象时不值得让脚本崩掉
        pass

del _stream
