# -*- coding: utf-8 -*-
"""一键出货：校验 → 播种 → 回归 → 重导快照 → 提交（→ 推送）。

把原来手敲的六七条串行命令收成一条，漏步骤当场拦截：

    python tools/ship_batch.py --only 十六进制 \\
        --add app/problems_bank_py_bits.py docs/problems.json NOTES.md \\
        --msg "Add hex-extractor family"

步骤与拦截规则
--------------
1. **verify_bank --only**（可用 --skip-verify 跳过；不给 --only 又不跳过
   就拒绝 —— 全量 5 分钟是 CI 的活，本地只做增量）
2. 播种本地库（ensure + sync_question_types + backfill_points）
3. selftest_theory（理论题判题口径）
4. test_question_types（题型体系回归）
5. export_static --with-cases（重导静态快照）
6. git add **只加 --add 点名的路径** —— ★ 绝不 `git add -A`：
   两个窗口共用这个仓库，另一窗口的 WIP 文件不该被卷进来
   （2026-10-15 踩过：19 个别人的文件进了我的提交）
7. git commit --msg 的内容
8. --push 才推送：凭据管理器取 token（.git-credentials 里那个 gho_ 已失效）
   + openssl 后端，先试活代理 127.0.0.1:10808 再试直连；
   推完 `git ls-remote` 复核，假成功当场拆穿

任何一步失败立即退出（退出码 1），后面步骤不跑。
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

PY = sys.executable


def sh(cmd: list[str] | str, **kw) -> subprocess.CompletedProcess:
    if isinstance(cmd, str):
        cmd = [cmd]
    print("  $ " + " ".join(cmd))
    sys.stdout.flush()
    return subprocess.run([PY] + cmd if kw.pop("with_py", False) else cmd,
                          **kw)


def die(msg: str) -> int:
    print("★ " + msg)
    return 1


def git_token() -> str:
    """凭据管理器里的 token（.git-credentials 里那个 gho_ 已 401）。"""
    r = subprocess.run(["git", "credential", "fill"], input="protocol=https\nhost=github.com\n\n",
                       capture_output=True, text=True)
    for line in r.stdout.splitlines():
        if line.startswith("password="):
            return line.split("=", 1)[1]
    return ""


def main() -> int:
    argv = sys.argv[1:]

    def opt(name: str) -> str | None:
        return argv[argv.index(name) + 1] if name in argv else None

    only = opt("--only")
    msg = opt("--msg")
    # --add 显式收路径（和开关值区分开：--add 后面那个才是路径）
    add_paths: list[str] = []
    i = 0
    while i < len(argv):
        if argv[i] == "--add":
            j = i + 1
            while j < len(argv) and not argv[j].startswith("--"):
                add_paths.append(argv[j])
                j += 1
            i = j
        else:
            i += 1
    do_push = "--push" in argv
    skip_verify = "--skip-verify" in argv

    if not msg:
        return die("必须给 --msg（提交信息）")
    if not add_paths:
        return die("必须给 --add 点名要提交的路径（绝不 git add -A，"
                   "另一窗口的 WIP 不能被卷进来）")

    # 1. 增量对拍
    if not skip_verify:
        if not only:
            return die("给 --only <关键词> 做增量对拍（全量 5 分钟是 CI 的活），"
                       "或 --skip-verify 明确跳过")
        print("\n[1/6] verify_bank --only " + only)
        r = sh([PY, "tools/verify_bank.py", "--py", "--only", only, "--quiet"],
               with_py=False)
        if r.returncode != 0:
            return die("对拍没过，出货中止")
    else:
        print("\n[1/6] verify_bank 跳过（--skip-verify）")

    # 2. 播种
    print("\n[2/6] 播种本地库")
    from app import db, seed                                    # noqa: E402
    db.init_db()
    seed.ensure()
    seed.sync_question_types()
    seed.backfill_points()
    import sqlite3
    n = sqlite3.connect("data/pta.db").execute(
        "select count(*) from problems").fetchone()[0]
    print("  库内总题数: %d" % n)

    # 3/4. 回归
    print("\n[3/6] selftest_theory")
    if sh([PY, "tools/selftest_theory.py"]).returncode != 0:
        return die("理论题判题口径自检没过")
    print("\n[4/6] test_question_types")
    if sh([PY, "tools/test_question_types.py"]).returncode != 0:
        return die("题型体系回归没过")

    # 5. 快照
    print("\n[5/6] export_static --with-cases")
    if sh([PY, "tools/export_static.py", "--with-cases"]).returncode != 0:
        return die("静态快照导出失败")

    # 6. 提交
    print("\n[6/6] git add + commit")
    for p in add_paths:
        if not (ROOT / p).exists():
            return die("要提交的路径不存在：%s" % p)
    if sh(["git", "add"] + add_paths).returncode != 0:
        return die("git add 失败")
    staged = subprocess.run(["git", "diff", "--cached", "--stat"],
                            capture_output=True, text=True).stdout.strip()
    print(staged)
    if not staged:
        return die("暂存区是空的 —— 路径没产生变更？")
    if sh(["git", "commit", "-m", msg]).returncode != 0:
        return die("git commit 失败")

    # 7. 推送（可选）
    if do_push:
        print("\n[push] 凭据管理器取 token → openssl 后端")
        token = git_token()
        if not token:
            return die("拿不到凭据（git credential fill 空）")
        url = "https://%s@github.com/cosy119/my-pta.git" % token
        base = ["git", "-c", "http.sslBackend=openssl", "-c", "credential.helper="]
        r = subprocess.run(base + ["-c", "http.proxy=http://127.0.0.1:10808",
                                   "push", url, "main"],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print("  代理推不动，试直连 …")
            # ★ 直连必须 -c http.proxy= 显式清空 —— 仓库 .git/config 里钉过代理时，
            #   不清空的话「直连重试」其实还在走死代理（2026-10-23 实测踩到）。
            r = subprocess.run(base + ["-c", "http.proxy=", "push", url, "main"],
                               capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout[-400:], r.stderr[-400:])
            return die("推送失败（提交已在本地，修好网络后手动推）")
        ls = subprocess.run(["git", "-c", "http.proxy=", "ls-remote",
                             "origin", "main"],
                            capture_output=True, text=True).stdout.split()[0]
        head = subprocess.run(["git", "rev-parse", "HEAD"],
                              capture_output=True, text=True).stdout.strip()
        if ls != head:
            return die("远端 main=%s ≠ 本地 HEAD=%s，假成功！" % (ls[:7], head[:7]))
        print("  远端已确认 = %s ✅" % ls[:7])
    else:
        print("\n未推送（加 --push 才推）。手动推送：git push 后用 "
              "git ls-remote origin main 复核")

    print("\n出货完成 ✅")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
