#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""理论题答案的「实证核验」——用真实命令跑出来，再拿去对答案键。

为什么需要它
------------
`tools/verify_bank.py` 对代码题是「双实现对拍」，但理论题**没有第二套实现可言**
（原文注释就这么写的）。于是这 117 道 Linux 理论题的答案键处于「没人独立核过」的状态。

这个脚本补上这一环，但**只补能补的那部分**：题库里大部分题目描述的是
GNU coreutils / bash / GNU tar 的真实行为，这些在本机（Git Bash = GNU coreutils 8.32）
就能跑出来。凡是能跑的，一律**先跑出事实、再跟答案键比**——绝不拿答案键当前提。

跑不了的（Fedora/systemd/SELinux/dnf/网络/内核/GNOME 等）如实列为「无法核验」，
不假装验过。

★ 极性约定：判断题的检查返回「题干那句话是否为真」的真值，直接跟答案键（对/错）比；
  选择/填空题的检查返回「答案键里的命令确实达成了题干要求」。

    python tools/verify_theory_facts.py
"""

from __future__ import annotations

import os
import posixpath
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _console                                                   # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "pta.db"

SB = ""            # 沙箱目录（Windows 视角），main() 里建
SBP = ""           # 沙箱目录（bash 视角的 posix 路径）

TRUE_W = {"对", "正确", "是", "√", "✓", "T", "t", "true", "y", "yes", "right"}
FALSE_W = {"错", "错误", "否", "×", "x", "✗", "F", "f", "false", "n", "no", "wrong"}


def run(cmd: str, timeout: int = 25):
    """在沙箱里跑一条 bash 命令。★ 命令里的 tar/ls 是 GNU 版（bash 自己的 PATH），
    不是 Windows System32 里那个 bsdtar。"""
    p = subprocess.run(["bash", "-c", cmd], cwd=SB, capture_output=True,
                       text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def sub(name: str) -> str:
    """建一个独立的子目录（每题夹具互不干扰），返回相对沙箱的路径。"""
    os.makedirs(os.path.join(SB, name), exist_ok=True)
    return name


def mk(rel: str, content: str = "") -> str:
    p = os.path.join(SB, rel)
    os.makedirs(os.path.dirname(p) or SB, exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    return rel


def seq(n: int, prefix: str = "L") -> str:
    return "".join("%s%d\n" % (prefix, i) for i in range(1, n + 1))


def is_tf(alts: list) -> bool:
    """判断题 ⟺ 备选答案全部落在 对/错 词表里。"""
    s = {a.strip() for a in alts}
    return bool(s) and s <= (TRUE_W | FALSE_W)


C = {}


def chk(pid, desc):
    def deco(fn):
        C[pid] = (desc, fn)
        return fn
    return deco


# ---------------- 判断题：派生「题干那句话是否为真」 ----------------

@chk(94, "`cd -` 与 `cd ..` 是同一个意思")
def _94():
    os.makedirs(os.path.join(SB, "d94aa"), exist_ok=True)
    # 进 aa → cd .. 退到 X → cd - 会回到 aa。若两者同义，cd - 应停在 X 的父级。
    rc, out, _ = run("cd d94aa && cd .. && cd - >/dev/null 2>&1 && pwd")
    landed = out.strip()
    parent = posixpath.dirname(SBP)
    return (landed == parent), "cd - 落在 %s；若与 cd .. 同义应落在 %s（实际回到了 %s）" % (
        landed, parent, posixpath.join(SBP, "d94aa"))


@chk(96, "`ls -a` 与 `ls -A` 输出完全一样")
def _96():
    sub("d96")
    mk("d96/.hidden", "x")
    mk("d96/plain", "x")
    rc1, a, _ = run("ls -a d96")
    rc2, b, _ = run("ls -A d96")
    return (a.strip() == b.strip()), "-a %d 项 / -A %d 项（差集：. 和 ..）" % (
        len(a.split()), len(b.split()))


@chk(98, "`rm -rf` 删掉的文件能从回收站找回")
def _98():
    return None, "「有没有回收站」是设计事实，本机无法从命令行为反证；属概念题"


@chk(100, "`head -n -3 f` 是非法的写法")
def _100():
    mk("f100", seq(10))
    rc, out, err = run("head -n -3 f100")
    return (rc != 0), "退出码 %d，输出 %d 行（10 行文件去掉最后 3 行）" % (rc, len(out.splitlines()))


@chk(102, "`touch` 已存在的文件会清空内容")
def _102():
    mk("f102", "important content\n")
    run("touch f102")
    size = os.path.getsize(os.path.join(SB, "f102"))
    return (size == 0), "touch 之后文件 %d 字节（原文 18 字节）" % size


@chk(104, "`tar xf a.tar.gz` 不写 z 会解压失败")
def _104():
    mk("d104/inner.txt", "hi\n")
    run("tar -czf a104.tar.gz -C d104 inner.txt")
    rc, out, err = run("mkdir -p x104 && tar xf a104.tar.gz -C x104")
    got = os.path.exists(os.path.join(SB, "x104", "inner.txt"))
    return (rc != 0), "`tar xf` 退出码 %d，解出的文件存在=%s（GNU tar 自动识别 gzip）" % (rc, got)


@chk(106, "`less` 可以往回翻页，`more` 不能")
def _106():
    return None, "「能不能往回翻」要在交互式终端里按键才能验，本机无法自动核验"


@chk(107, "用 `rm` 删指向目录的符号链接，真实目录也会被删掉")
def _107():
    sub("d107")
    mk("d107/real/inside.txt", "x")
    rc0, _, e0 = run("cd d107 && ln -s real link")
    rc, _, _ = run("cd d107 && rm link")
    alive = os.path.exists(os.path.join(SB, "d107", "real", "inside.txt"))
    return (not alive), "删链接退出码 %d，真实目录还在=%s（rm 只删链接本身）" % (rc, alive)


@chk(109, "在 /usr/local 下 `cd share` 与 `cd ../share` 到同一个目录")
def _109():
    sub("d109/usr/local/share")
    sub("d109/usr/share")
    rc, a, _ = run("cd d109/usr/local && cd share && pwd")
    rc, b, _ = run("cd d109/usr/local && cd ../share && pwd")
    return (a.strip() == b.strip()), "%s  vs  %s" % (a.strip(), b.strip())


@chk(143, "`ll` 是 `ls -l` 的别名，写在 .sh 脚本里也能正常执行")
def _143():
    mk("s143.sh", "#!/bin/bash\nll >/dev/null 2>&1\necho rc=$?\n")
    rc, out, err = run("bash s143.sh")
    m = re.search(r"rc=(\d+)", out)
    code = int(m.group(1)) if m else -1
    return (code == 0), "脚本里执行 ll 的退出码 = %d（脚本默认不开 alias）" % code


@chk(156, "root 用户的家目录是 /home/root")
def _156():
    return None, "本机没有 /etc/passwd（MSYS 的 passwd 也不能代表 Linux），无法核验"


@chk(161, "用 Flatpak 安装的软件可以用 `dnf list installed` 查到")
def _161():
    return None, "本机无 dnf/flatpak（两者是不同包管理器、各自独立数据库），无法核验"


@chk(166, "Fedora 上可以用 `dpkg -i xxx.deb` 安装 deb 包")
def _166():
    has = shutil.which("dpkg") is not None
    return has, "本机 dpkg 存在=%s（dpkg/deb 属 Debian 系；Fedora 系自带 rpm/dnf）" % has


@chk(175, "`ping` 不通就可以确定是网络有问题")
def _175():
    return None, "要构造「ICMP 被屏蔽但 TCP 通」的网络环境才能反证，本机不稳定；属概念题"


# ---------------- 选择/填空题：跑答案键里的命令，看效果对不对 ----------------

@chk(91, "提纲说 `head -n +1000 file` 从 1000 行开始显示——真实行为是什么；`tail -n +1000` 才对吗")
def _91():
    mk("f91", seq(1005))
    rc_h, out_h, _ = run("head -n +1000 f91")
    rc_t, out_t, _ = run("tail -n +1000 f91")
    h_lines = out_h.splitlines()
    t_first = out_t.splitlines()[0] if out_t.splitlines() else ""
    # 事实①：head -n +1000 不报错，但输出的是前 1000 行（末行 L1000）
    fact_head = (rc_h == 0 and len(h_lines) == 1000 and h_lines[-1] == "L1000")
    # 事实②：tail -n +1000 才是从第 1000 行开始
    fact_tail = (rc_t == 0 and t_first == "L1000")
    return (fact_head and fact_tail), \
        "head -n +1000 退出码 %d、输出 %d 行、末行 %s（= 前 1000 行，不报错）；" \
        "tail -n +1000 首行 %s" % (rc_h, len(h_lines), h_lines[-1] if h_lines else "?", t_first)


@chk(92, "`cat -n file` 是「统计行数」吗；`wc -l` 才是")
def _92():
    mk("f92", seq(7))
    rc, out, _ = run("cat -n f92 | head -1")
    rc2, n, _ = run("wc -l < f92")
    return (out.strip().startswith("1") and n.strip() == "7"), \
        "cat -n 首行=%r（是加行号不是计数）；wc -l = %s" % (out.strip(), n.strip())


@chk(93, "`ls [0-9]` 能列出「名字里含数字」的条目吗")
def _93():
    sub("d93")
    for n in ("1", "report2.txt", "log2026", "notes"):
        mk("d93/" + n, "x")
    rc, out, _ = run("cd d93 && ls [0-9]")
    got = sorted(out.split())
    return (got == ["1"]), "ls [0-9] 只列出 %s（report2.txt / log2026 没被列出）" % got


@chk(95, "`ls -ld /etc` 只看目录自己、输出只要一行")
def _95():
    rc, out, _ = run("ls -ld /etc")
    lines = out.splitlines()
    ok = (len(lines) == 1) and bool(lines) and lines[0].startswith("d")
    return ok, "输出 %d 行，首字符 %r（d=目录自身）" % (len(lines), lines[0][0] if lines else "?")


@chk(97, "`cp -a` 能保住权限、符号链接、时间戳")
def _97():
    sub("d97")
    mk("d97/src/f.txt", "abc\n")
    run("chmod 700 d97/src/f.txt && ln -s f.txt d97/src/lnk "
        "&& touch -d '2020-01-02 03:04:05' d97/src/f.txt")
    run("cp -a d97/src d97/dst")
    rc, ms, _ = run("stat -c %a d97/src/f.txt && stat -c %a d97/dst/f.txt "
                    "&& ([ -L d97/src/lnk ] && echo SRC_LINK=Y || echo SRC_LINK=N) "
                    "&& ([ -L d97/dst/lnk ] && echo DST_LINK=Y || echo DST_LINK=N) "
                    "&& stat -c %Y d97/src/f.txt && stat -c %Y d97/dst/f.txt")
    toks = ms.split()
    if len(toks) != 6:
        return None, "stat 输出异常：%r" % ms.strip()
    m1, m2, sl, dl, t1, t2 = toks
    if sl == "N":
        return None, ("本机建不出符号链接（MSYS 把 ln -s 降级成副本），符号链接没法在本机验；"
                      "chmod 也只是近似映射（700 落成 %s），权限位同样验不了。时间戳部分见 [112]" % m1)
    if dl != "Y":
        return None, ("MSYS 环境里 cp -a 对符号链接的处理与 Linux 不一致"
                      "（src 是链接、dst 不是），不能当 Linux 行为的证据")
    return (m1 == m2 and t1 == t2), \
        "权限 %s→%s，符号链接保留=%s，时间戳一致=%s" % (m1, m2, dl == "Y", t1 == t2)


@chk(99, "`tail -n +5 a.txt` 输出从第 5 行到文件末尾")
def _99():
    mk("a99.txt", seq(20))
    rc, out, _ = run("tail -n +5 a99.txt")
    lines = out.splitlines()
    return (lines[0] == "L5" and len(lines) == 16), \
        "首行 %s，共 %d 行（20-5+1=16）" % (lines[0] if lines else "?", len(lines))


@chk(101, "`tar -zcvf` 里的 z 表示 gzip")
def _101():
    mk("d101/x.txt", "hi\n")
    run("tar -zcvf a101.tar.gz -C d101 x.txt")
    rc, out, _ = run("tar tzf a101.tar.gz")
    rc2, magic, _ = run("head -c 2 a101.tar.gz | od -An -tx1 | tr -d ' \\n'")
    return (rc == 0 and magic == "1f8b"), "tar tzf 可读=%s；文件魔数=%s（1f8b 即 gzip）" % (
        rc == 0, magic)


@chk(103, "`mkdir -p a/b/c` 的 p 表示缺失的父目录一并创建")
def _103():
    sub("d103")
    rc0, _, _ = run("cd d103 && mkdir noparent/a/b 2>/dev/null")
    rc1, _, _ = run("cd d103 && mkdir -p hasparent/a/b/c")
    ok = os.path.isdir(os.path.join(SB, "d103", "hasparent", "a", "b", "c"))
    return (rc0 != 0 and ok), "不带 -p 退出码=%d（失败）；带 -p 建出三级目录=%s" % (rc0, ok)


@chk(105, "`unzip -l a.zip` 能只看清单、不真的解压")
def _105():
    # 本机没有 zip 命令 —— 用 Python 的 zipfile 造夹具，unzip 本身是有的
    zp = os.path.join(SB, "a105.zip")
    with zipfile.ZipFile(zp, "w") as z:
        z.writestr("y.txt", "hi\n")
    rc, out, _ = run("unzip -l a105.zip")
    leaked = os.path.exists(os.path.join(SB, "y.txt"))
    return ("y.txt" in out and not leaked), "unzip -l 列出 y.txt=%s，没解出文件=%s" % (
        "y.txt" in out, not leaked)


@chk(110, "`cd -` 能回到进当前目录之前的位置")
def _110():
    os.makedirs(os.path.join(SB, "d110"), exist_ok=True)
    rc, out, _ = run("cd d110 && cd - >/dev/null 2>&1 && pwd")
    return (out.strip() == SBP), "cd 回到 %s（=沙箱初始目录）" % out.strip()


@chk(111, "`ls -la` 能列出包括隐藏文件在内的长格式")
def _111():
    sub("d111")
    mk("d111/.hidden", "x")
    mk("d111/visible", "x")
    rc, a, _ = run("ls -la d111")
    rc, b, _ = run("ls -l d111")
    has_hidden = ".hidden" in a
    long_fmt = a.startswith("total")
    return (has_hidden and long_fmt and ".hidden" not in b), \
        "-la 首行=%r、含 .hidden=%s；-l 不含 .hidden=%s" % (
            a.splitlines()[0][:12] if a else "?", has_hidden, ".hidden" not in b)


@chk(112, "`cp -a` 一个选项满足权限+属主+时间戳")
def _112():
    sub("d112")
    mk("d112/z.txt", "abc\n")
    run("chmod 750 d112/z.txt && touch -d '2019-05-06 07:08:09' d112/z.txt")
    run("cp -a d112 d112dst")
    rc, ms, _ = run("stat -c %a d112/z.txt && stat -c %a d112dst/z.txt "
                    "&& stat -c %Y d112/z.txt && stat -c %Y d112dst/z.txt")
    toks = ms.split()
    if len(toks) != 4:
        return None, "stat 输出异常：%r" % ms.strip()
    m1, m2, t1, t2 = toks
    if m1 != "750":
        # Windows 上 chmod 是近似映射（750 落成 644），权限位验不出差别 —— 只剩时间戳是真验证
        return None, ("时间戳保留已验证（2019 → cp -a 后一致=%s），但权限位在本机是近似映射"
                      "（chmod 750 落成 %s），权限部分无法真实验证" % (t1 == t2, m1))
    return (m1 == m2 and t1 == t2), "权限 %s→%s，时间戳一致=%s" % (m1, m2, t1 == t2)


@chk(113, "`ls -ld /etc` 输出一行")
def _113():
    rc, out, _ = run("ls -ld /etc")
    return (len(out.splitlines()) == 1), "输出 %d 行" % len(out.splitlines())


@chk(114, "`head -n 50 a.log` 取前 50 行")
def _114():
    mk("a114.log", seq(200))
    rc, out, _ = run("head -n 50 a114.log")
    lines = out.splitlines()
    return (len(lines) == 50 and lines[-1] == "L50"), "输出 %d 行，末行 %s" % (len(lines), lines[-1])


@chk(115, "`tail -n +100 a.log` 从第 100 行取到末尾")
def _115():
    mk("a115.log", seq(150))
    rc, out, _ = run("tail -n +100 a115.log")
    lines = out.splitlines()
    return (lines[0] == "L100" and len(lines) == 51), "首行 %s，共 %d 行" % (lines[0], len(lines))


@chk(116, "`head -n -10 a.log` 取除最后 10 行之外的所有行")
def _116():
    mk("a116.log", seq(100))
    rc, out, _ = run("head -n -10 a116.log")
    lines = out.splitlines()
    return (len(lines) == 90 and lines[-1] == "L90"), "输出 %d 行，末行 %s" % (len(lines), lines[-1])


@chk(117, "`tar -czf project.tar.gz dir` 生成 gzip 压缩包")
def _117():
    mk("proj117/f.txt", "hi\n")
    rc, _, err = run("tar -czf proj117.tar.gz proj117")
    magic = ""
    if os.path.exists(os.path.join(SB, "proj117.tar.gz")):
        with open(os.path.join(SB, "proj117.tar.gz"), "rb") as f:
            magic = f.read(2).hex()
    return (rc == 0 and magic == "1f8b"), "退出码 %d，魔数 %s" % (rc, magic)


@chk(118, "`tar -tzf bak.tar.gz` 只列出内容、不解压")
def _118():
    mk("d118/in.txt", "hi\n")
    run("tar -czf bak118.tar.gz -C d118 in.txt")
    rc, out, _ = run("tar -tzf bak118.tar.gz")
    leaked = os.path.exists(os.path.join(SB, "in.txt"))
    return ("in.txt" in out and not leaked), "列出 %r，外层没解出文件=%s" % (out.strip(), not leaked)


@chk(119, "`mkdir -p /tmp/out && tar -xzvf bak.tar.gz -C /tmp/out` 能解到指定目录")
def _119():
    mk("d119/in.txt", "hi\n")
    run("tar -czf bak119.tar.gz -C d119 in.txt")
    rc, _, _ = run("mkdir -p out119 && tar -xzf bak119.tar.gz -C out119")
    got = os.path.exists(os.path.join(SB, "out119", "in.txt"))
    return got, "解出的文件存在=%s" % got


@chk(120, "`mkdir -p data/2026/10/report` 一次建出多级目录")
def _120():
    rc, _, _ = run("mkdir -p d120/2026/10/report")
    got = os.path.isdir(os.path.join(SB, "d120", "2026", "10", "report"))
    return got, "多级目录建出=%s" % got


@chk(121, "`touch /tmp/{a,b,c}.txt` 花括号简写一次建三个文件")
def _121():
    sub("d121")
    rc, _, _ = run("touch d121/{a,b,c}.txt")
    got = sorted(x for x in os.listdir(os.path.join(SB, "d121")) if x.endswith(".txt"))
    return (got == ["a.txt", "b.txt", "c.txt"]), "建出 %s" % got


@chk(131, "`tail -n 5 a.log` 取最后 5 行")
def _131():
    mk("a131.log", seq(30))
    rc, out, _ = run("tail -n 5 a131.log")
    return (out.split() == ["L26", "L27", "L28", "L29", "L30"]), "输出 %s" % out.split()


@chk(132, "`ls *[0-9]*` 列出名字里含数字的全部条目")
def _132():
    sub("d132")
    for n in ("1", "report2.txt", "log2026", "notes"):
        mk("d132/" + n, "x")
    rc, out, _ = run("cd d132 && ls *[0-9]*")
    got = sorted(out.split())
    return (got == ["1", "log2026", "report2.txt"]), "列出 %s" % got


@chk(133, "从 /usr/local/bin 用 `cd ../..` 到 /usr")
def _133():
    sub("u/usr/local/bin")
    rc, out, _ = run("cd u/usr/local/bin && cd ../.. && pwd")
    want = posixpath.join(SBP, "u/usr")
    return (out.strip() == want), "落点 %s（期望 %s）" % (out.strip(), want)


@chk(135, "`echo $SHELL` 打印当前默认 shell")
def _135():
    rc, out, _ = run("echo $SHELL")
    return (out.strip() != "" and "/" in out.strip()), "$SHELL = %r" % out.strip()


@chk(137, "`ls /usr/local > ~/test1.txt && cat -n ~/test1.txt` 重定向并带行号查看")
def _137():
    sub("d137")
    mk("d137/a", "x")
    mk("d137/b", "x")
    rc, out, _ = run("ls d137 > t137.txt && cat -n t137.txt")
    lines = out.splitlines()
    return (len(lines) == 2 and lines[0].strip().startswith("1")), "cat -n 输出 %r" % lines[:1]


@chk(138, "`ls -d *pass*` 只列名字含 pass 的")
def _138():
    sub("d138")
    for n in ("passwd", "mypass.txt", "group"):
        mk("d138/" + n, "x")
    rc, out, _ = run("cd d138 && ls -d *pass*")
    got = sorted(out.split())
    return (got == ["mypass.txt", "passwd"]), "列出 %s" % got


@chk(141, "`mv /test7 /test8` 是改名、`mv /test7 /tmp/` 是移进目录")
def _141():
    sub("d141")
    mk("d141/test7", "x")
    run("mv d141/test7 d141/test8")
    step1 = (not os.path.exists(os.path.join(SB, "d141", "test7"))
             and os.path.exists(os.path.join(SB, "d141", "test8")))
    mk("d141/test7", "x")
    run("mkdir -p d141/tmpd && mv d141/test7 d141/tmpd/")
    step2 = (os.path.exists(os.path.join(SB, "d141", "tmpd", "test7"))
             and not os.path.exists(os.path.join(SB, "d141", "test7")))
    return (step1 and step2), "改名=%s，移进目录=%s" % (step1, step2)


@chk(145, "`ln -s /usr/local/sdutshare /myshare` 能建出指向目标的符号链接")
def _145():
    sub("d145")
    mk("d145/target", "x")
    rc, _, e = run("cd d145 && ln -s target mylink")
    rc2, islink, _ = run("[ -L d145/mylink ] && echo Y || echo N")
    if islink.strip() == "N":
        return None, "本机建不出符号链接（Windows 降级成副本），无法核验"
    rc3, points, _ = run("readlink d145/mylink")
    return (rc == 0 and points.strip() == "target"), "建出链接=%s，指向 %r" % (
        rc == 0, points.strip())


@chk(146, "`sort -r` 按字典逆序排序")
def _146():
    mk("mysort146", "is\nthis\nexcellent\nmy\n")
    rc, out, _ = run("sort -r mysort146")
    return (out.split() == ["this", "my", "is", "excellent"]), "逆序结果 %s" % out.split()


@chk(147, "`echo -n` 输出后不换行")
def _147():
    rc, a, _ = run("echo -n 'hello everyone!' | wc -c")
    rc, b, _ = run("echo 'hello everyone!' | wc -c")
    return (a.strip() == "15" and b.strip() == "16"), \
        "-n 输出 %s 字节，不带 -n 是 %s 字节（差的那个就是换行）" % (a.strip(), b.strip())


@chk(149, "`./eclipse` 能启动当前目录下的可执行文件")
def _149():
    sub("d149")
    mk("d149/eclipse", "#!/bin/bash\necho started\n")
    run("chmod +x d149/eclipse")
    rc1, _, _ = run("cd d149 && ./eclipse")
    rc2, _, _ = run("cd d149 && eclipse 2>/dev/null")
    return (rc1 == 0 and rc2 != 0), "./eclipse 退出码=%d；直接敲 eclipse 退出码=%d" % (rc1, rc2)


@chk(151, "`cat file11 file12 > dir1/file13` 把两者内容依次写进去")
def _151():
    sub("d151")
    mk("d151/file11", "sdut11\n")
    mk("d151/file12", "sdut12\n")
    run("cd d151 && mkdir -p dir1 && cat file11 file12 > dir1/file13")
    got = open(os.path.join(SB, "d151", "dir1", "file13"), encoding="utf-8").read()
    return (got == "sdut11\nsdut12\n"), "结果 %r" % got


# ---------------- 第 11 讲（Shell）：bash 语法不依赖发行版，这几条本机可实证 ----------------

@chk(205, "`[ $v = x ]` 而 v 为空 → 报 unary operator expected（答案键选 B）")
def _205():
    rc, out, err = run("v=; [ $v = x ] && echo yes")
    hit = "unary operator expected" in err
    return hit, "退出码 %d，stderr=%r（`[` 是命令，空展开后只剩一个操作数）" % (
        rc, err.strip()[:70])


@chk(206, "`[[ 10 > 9 ]]` 为假 —— > 在双方括号里是字符串比较（答案键选 B：small）")
def _206():
    rc, out, _ = run("if [[ 10 > 9 ]]; then echo big; else echo small; fi")
    rc2, out2, _ = run("if [[ 10 -gt 9 ]]; then echo big; else echo small; fi")
    return (out.strip() == "small" and out2.strip() == "big"), \
        "`>` -> %s（字典序 '1'<'9'）；`-gt` -> %s" % (out.strip(), out2.strip())


@chk(207, "管道里的 while 在子 shell，改的变量出不来（答案键选 B：0）")
def _207():
    rc, out, _ = run("n=0; printf 'a\\nb\\nc\\n' | while read x; do n=$((n+1)); done; echo n=$n")
    return ("n=0" in out.strip()), \
        "三行数据流过循环后 %r（循环内部确实加到了 3，外面拿不到）" % out.strip()


@chk(208, "`local x=$(false)` 之后 $? 恒为 0（判断题答案：对）")
def _208():
    rc, out, _ = run("f(){ local n=$(false); return $?; }; f; echo rc=$?")
    rc2, out2, _ = run("g(){ local n; n=$(false); return $?; }; g; echo rc=$?")
    return ("rc=0" in out and "rc=1" in out2), \
        "`local n=$(false)` -> %r；拆成两句 -> %r（拆开后错误码才透得出来）" % (
            out.strip(), out2.strip())


@chk(209, "`for f in $(ls)` 把含空格的文件名切碎（答案键选 B：3 行）")
def _209():
    sub("d209")
    mk("d209/a 1.md", "x")
    mk("d209/b.md", "x")
    rc, out, _ = run("cd d209 && for f in $(ls); do echo \"[$f]\"; done | wc -l")
    # 反证：glob 不切碎
    rc2, out2, _ = run("cd d209 && for f in *.md; do echo \"[$f]\"; done | wc -l")
    return (out.strip() == "3" and out2.strip() == "2"), \
        "`$(ls)` -> %s 行；`*.md` -> %s 行（两个文件，其中一个名里有空格）" % (
            out.strip(), out2.strip())


@chk(210, "`${v:-fallback}` 为空/未定义时替换、有值时保留（答案键）")
def _210():
    rc, out, _ = run("v=; echo \"${v:-fallback}\"; v=set; echo \"${v:-fallback}\"")
    lines = out.split()
    return (lines[:2] == ["fallback", "set"]), "空值 -> %s；有值 -> %s" % (
        lines[0] if lines else "?", lines[1] if len(lines) > 1 else "?")


# ----------------------------------------------------------------------


def load_keys() -> dict:
    con = sqlite3.connect("file:%s?mode=ro" % DB.as_posix(), uri=True)
    con.row_factory = sqlite3.Row
    rows = con.execute("""
        SELECT p.id, p.choices, t.expected_stdout
          FROM problems p JOIN testcases t ON t.problem_id = p.id
         WHERE p.status = 'published' AND p.line = 'text'""").fetchall()
    out = {}
    for r in rows:
        alts = [x[1:].strip() for x in (r["expected_stdout"] or "").split("\n")
                if x.startswith("|")]
        out[r["id"]] = {"alts": alts}
    con.close()
    return out


def main() -> int:
    global SB, SBP
    SB = tempfile.mkdtemp(prefix="ptatheory_")
    # run() 依赖全局 SB —— 先设好，再取 bash 视角的 posix 路径
    p = subprocess.run(["bash", "-c", "pwd"], cwd=SB, capture_output=True, text=True)
    SBP = p.stdout.strip()
    print("沙箱目录：%s（bash 视角 %s）" % (SB, SBP))
    rc, ver_ls, _ = run("ls --version | head -1")
    rc, ver_tar, _ = run("tar --version | head -1")
    print("本机命令：%s  /  %s" % (ver_ls.strip(), ver_tar.strip()))

    keys = load_keys()
    print("题库：%d 道理论题（published / line=text）\n" % len(keys))

    n_pass = n_bad = n_skip = 0
    skipped = []

    for pid in sorted(C):
        desc, fn = C[pid]
        if pid not in keys:
            continue
        alts = keys[pid]["alts"]
        tf = is_tf(alts)
        try:
            res = fn()
        except Exception as e:                                   # noqa: BLE001
            n_skip += 1
            skipped.append((pid, desc, "执行异常：%s" % e))
            continue
        if not res or res[0] is None:
            n_skip += 1
            skipped.append((pid, desc, res[1] if res else ""))
            continue
        derived, evidence = res
        if tf:
            expect = (alts[0].strip() in TRUE_W) if alts else True
            ok = (bool(derived) == bool(expect))
            key_str = "对（题干为真）" if expect else "错（题干为假）"
        else:
            ok = bool(derived)
            key_str = " / ".join(alts[:3]) + (" 等 %d 种" % len(alts) if len(alts) > 3 else "")
        if ok:
            n_pass += 1
            print("  ✓ [%3d] %s" % (pid, desc))
            print("        %s" % evidence)
        else:
            n_bad += 1
            print("  ✗ [%3d] %s" % (pid, desc))
            print("        实测：%s" % evidence)
            print("        答案键：%s   ← 对不上！" % key_str)

    print("\n" + "=" * 64)
    print("实证核验：通过 %d 项，不符 %d 项，无法核验 %d 项（共 %d 项已建检查）"
          % (n_pass, n_bad, n_skip, n_pass + n_bad + n_skip))
    print("题库总量 %d 道，本次可实证 %d 道（%.0f%%）"
          % (len(keys), n_pass + n_bad, (n_pass + n_bad) * 100.0 / len(keys)))
    print("=" * 64)

    if skipped:
        print("\n无法在本机实证的（如实列出，不假装验过）：")
        for pid, desc, why in skipped:
            print("  · [%3d] %s" % (pid, desc))
            if why:
                print("        原因：%s" % why)

    shutil.rmtree(SB, ignore_errors=True)
    print("\n沙箱已清理")
    return 1 if n_bad else 0


if __name__ == "__main__":
    sys.exit(main())
