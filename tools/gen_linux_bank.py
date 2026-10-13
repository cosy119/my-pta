"""生成 `app/problems_bank_linux.py` —— Linux 线题库。

为什么单独用一个生成脚本
------------------------
Linux 线的题绝大多数是**理论题**（选择 / 判断 / 填命令），用 `app/bank_kit.py`
里的三个工厂函数能省掉一堆样板字段，也顺带避免「漏写 checker」这类低级错。

题源（都是已经核实过的材料）
----------------------------
1. **课程下发的《基础命令部分》** —— 10 个命令的提纲。
   ★ 那份提纲有 **6 处写法会把人带偏**（`-Z`/`-z`、`-V`/`-v`、`-C`/`-c`、
   `head -n +N`、`cat -n` 当数行、`ls [0-9]`），本文件里逐条出了题。
2. **《Linux基础命令》讲义的 A/B/C 三组习题**（认命令 / 写命令 / 找错）。
3. **课程下发的 4 份实验 PDF**（实验 2/3/4 各 10 题）—— 抽每题的关键考点。
4. **第 01 ~ 10 讲讲义**里的核心概念。

答案口径
--------
- 选择题：一个字母，`oneof` 比对上大写
- 判断题：`对` / `错`（写 `正确`/`√`/`T` 也认）
- 填命令：**按 `cmd` 口径比** —— 空白多少无所谓，`-l -a` 与 `-la` 等价、
  `-la` 与 `-al` 等价（见 `app/judge/compare.py` 的 `_norm_cmd`）。
  所以只要语义对、参数顺序别太离谱，就能过。

用法
----
    python tools/gen_linux_bank.py            # 生成 app/problems_bank_linux.py
    python tools/gen_linux_bank.py --check    # 只校验，不写文件（CI 用）
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = ROOT / "app" / "problems_bank_linux.py"
sys.path.insert(0, str(ROOT))

from app.bank_kit import fill, mc, tf                          # noqa: E402

SUBJ = "linux"

PROBLEMS: list[dict] = []


def add(p: dict) -> None:
    PROBLEMS.append(p)


# ===================================================================== #
#  一、课程《基础命令部分》—— 必须先纠正的六处
# ===================================================================== #
def part_fix_six() -> None:
    sec = "基础命令 · 先纠正六处"

    add(mc(
        "tar 的 -Z 到底压什么",
        "你在网上抄到一条备份命令 `tar -Zcvf bak.tar.gz dir/`，"
        "想用它做 **gzip** 压缩。\n\n"
        "问题出在 `-Z` 上：它**不是** gzip。那 `-Z` 是什么？",
        ["调用 gzip 压缩", "调用 compress（老式 .Z 格式）压缩",
         "调用 zip 压缩", "调用 zstd 压缩"],
        "B",
        subject=SUBJ, section=sec,
        explanation=(
            "`-Z` 是 **compress**，处理的是 1970 年代的老 `.Z` 格式，"
            "现在很多机器根本没装这个工具。\n\n"
            "**gzip 是小写 `-z`**。所以正确写法是 `tar -czvf bak.tar.gz dir/`。\n\n"
            "★ 这类坑的根因是：tar 的选项**大小写都真实存在**（`-z`/`-Z`、`-v`/`-V`、`-c`/`-C`），"
            "抄错一个字母不会报错，只会静默地干了另一件事。\n"
            "锚点：**日常用的那批全是小写**。"),
        tags=["tar", "压缩", "大小写", "课程纠错"], difficulty=2,
    ))

    add(mc(
        "tar 里「显示处理过程」是哪个选项",
        "打包一个几 GB 的目录时，你想看到 tar 正在处理哪些文件。"
        "应该加哪个选项？",
        ["-V（大写）", "-v（小写）", "-x", "-t"],
        "B",
        subject=SUBJ, section=sec,
        explanation=(
            "小写 **`-v` = verbose（啰嗦模式）**，把正在处理的文件名逐个打出来。\n\n"
            "大写 `-V` 是 **`--label`** —— 给归档写一个**卷标**（不是打印过程），"
            "跟「显示进度」毫无关系。\n\n"
            "另外两个：`-x` 解包、`-t` 只列内容不解包。\n"
            "口诀：`czvf` 打包、`xzvf` 解包、`tzvf` 看内容。"),
        tags=["tar", "verbose", "大小写", "课程纠错"], difficulty=2,
    ))

    add(mc(
        "tar 里「创建归档」是哪个选项",
        "下面四个 tar 选项，哪一个表示「**创建**一个新的归档文件」？",
        ["-C（大写）", "-c（小写）", "-x", "-j"],
        "B",
        subject=SUBJ, section=sec,
        explanation=(
            "小写 **`-c` = create**，创建归档。\n\n"
            "大写 `-C` 是 **`--directory`** —— **切换目录**，"
            "最常和解压连用：`tar -xzvf bak.tar.gz -C /tmp/out`（解到指定目录）。\n\n"
            "`-x` 解包；`-j` 走 bzip2（配 `.tar.bz2`）。"),
        tags=["tar", "create", "大小写", "课程纠错"], difficulty=2,
    ))

    add(mc(
        "从第 1000 行开始显示的正确写法",
        "课程提纲里写「`head -n +1000 file` 从 1000 行开始显示」。\n\n"
        "这条命令**会直接报错**。从第 1000 行显示到末尾，正确写法是？",
        ["head -n +1000 file", "head -n -1000 file",
         "tail -n +1000 file", "tail -n -1000 file"],
        "C",
        subject=SUBJ, section=sec,
        explanation=(
            "**`head` 不认 `+`**，会报 `head: invalid number of lines: '+1000'`。\n\n"
            "`+N` 这个语义**只属于 tail**：`tail -n +1000 file` = 从第 1000 行到末尾。\n\n"
            "顺便记牢另一半：`-N` 归 head —— `head -n -10 file` 是「去掉**最后** 10 行」。\n\n"
            "★ 一句口诀：**`+` 归 tail，`-` 归 head**。\n"
            "验证：`tail -n -5 f` 也会报错（tail 的 `-n` 只认数字或 `+数字`）。"),
        tags=["head", "tail", "coreutils", "课程纠错"], difficulty=3,
    ))

    add(mc(
        "统计文件有多少行的正确命令",
        "提纲里写「`cat -n file1` 表示文件的行数」。这个说法**不准确**。\n\n"
        "想**统计**一个文件有多少行，正确命令是？",
        ["cat -n file1", "wc -l file1", "tail -n file1", "ls -l file1"],
        "B",
        subject=SUBJ, section=sec,
        explanation=(
            "`cat -n` 是**给输出的每一行加上行号**，不是统计行数 —— "
            "对一个几十万行的文件，它既刷屏又慢。\n\n"
            "**`wc -l file1`** 才是数行数（`wc` = word count，`-l` = lines），"
            "输出形如 `42 file1`。\n\n"
            "★ 「用 `cat -n` 看最后一行行号，也能看出总行数」—— 能，但那是歪门邪道：\n"
            "大文件不划算，而且会往屏幕上倒几万行。"),
        tags=["wc", "cat", "统计", "课程纠错"], difficulty=2,
    ))

    add(mc(
        "列出「名字里含数字」的文件",
        "提纲里写「`ls [0-9]` 显示包含数字的文件名」。\n\n"
        "实际敲下去，你会发现 `report2.txt`、`log2026` 一个都没列出来。为什么？",
        ["方括号是正则语法，ls 不支持",
         "[0-9] 只匹配「名字恰好是一个数字」的条目",
         "必须先 cd 到目标目录才行",
         "要写成 [0-9]* 才有用"],
        "B",
        subject=SUBJ, section=sec,
        explanation=(
            "`[0-9]` 是 shell 的 glob（通配符），它匹配的是「**整个名字恰好是一个字符、"
            "且这个字符是数字**」的条目 —— 比如 `1`、`7`。\n\n"
            "`report2.txt` 名字有 11 个字符，当然不匹配。\n\n"
            "正解：\n"
            "- **名字里含数字** → `ls *[0-9]*`\n"
            "- **以数字开头** → `ls [0-9]*`\n\n"
            "★ 顺带一提：`*` 是 shell 展开的（不是 ls 干的），"
            "所以匹配不上时 shell 会把 `*[0-9]*` 原样传给 ls。"),
        tags=["ls", "通配符", "glob", "课程纠错"], difficulty=3,
    ))


# ===================================================================== #
#  二、《Linux基础命令》A 组 —— 认命令
# ===================================================================== #
def part_a_group() -> None:
    sec = "基础命令 · A 组 认命令"

    add(tf(
        "cd - 与 cd .. 效果相同吗",
        "`cd -` 和 `cd ..` 是同一个意思，都用来回到上一级目录。",
        False,
        subject=SUBJ, section=sec,
        explanation=(
            "**错**。两件事完全不同：\n\n"
            "- `cd ..` —— 按**目录结构**往上走一级。在 `/a/b/c` 里执行就到 `/a/b`。\n"
            "- `cd -` —— 按**访问历史**回到上一次所在的目录（用的是环境变量 `$OLDPWD`）。"
            "在 `/a/b/c` 里执行，可能跳到毫不相干的 `/var/log`。\n\n"
            "命令执行完，`cd -` 还会把目标目录打印出来（`cd ..` 不会）。"),
        tags=["cd", "OLDPWD", "易混"], difficulty=2,
    ))

    add(mc(
        "查看目录本身（而不是里面）的权限",
        "你想看 `/etc` **这个目录自己**的权限信息，输出只要一行。哪条命令对？",
        ["ls -l /etc", "ls -ld /etc", "ls -a /etc", "ls -R /etc"],
        "B",
        subject=SUBJ, section=sec,
        explanation=(
            "**`ls -ld /etc`**。\n\n"
            "- `ls -l /etc` 列的是 `/etc` **里面**的条目 —— 输出几十行，但没有一行是 `/etc` 自己。\n"
            "- **`-d` = directory**，让 ls「**别展开**这个目录，只报它自己」。\n\n"
            "★ 这是「问某个目录的权限，答成了里面文件的权限」这个高频错点的正解。\n\n"
            "输出长这样（第一列就是权限）：\n"
            "```\n"
            "drwxr-xr-x. 1 root root 8192 Oct 12 09:00 /etc\n"
            "```"),
        tags=["ls", "-d", "权限", "高频错点"], difficulty=2,
    ))

    add(tf(
        "ls -a 与 ls -A 输出一样吗",
        "`ls -a` 和 `ls -A` 的输出完全一样，都能列出隐藏文件。",
        False,
        subject=SUBJ, section=sec,
        explanation=(
            "**错**。差在最前面那两行：\n\n"
            "| 选项 | 含义 | 是否含 `.` 和 `..` |\n"
            "|---|---|---|\n"
            "| `-a` | all | **含** |\n"
            "| `-A` | almost all | **不含** |\n\n"
            "`.` 是当前目录、`..` 是上级目录，它俩永远存在、不是「隐藏文件」。\n"
            "所以在脚本里遍历目录时用 `-A`，能省掉手动过滤 `.` 和 `..` 的麻烦。"),
        tags=["ls", "-a", "-A", "隐藏文件"], difficulty=3,
    ))

    add(mc(
        "复制目录并保留符号链接与权限时间",
        "把 `~/docs` 整个目录复制到备份盘，要求**保留权限、属主、时间戳，"
        "并且符号链接原样照搬**。用哪个？",
        ["cp -r ~/docs /backup/", "cp -a ~/docs /backup/",
         "cp -p ~/docs /backup/", "cp -f ~/docs /backup/"],
        "B",
        subject=SUBJ, section=sec,
        explanation=(
            "**`cp -a`** —— 归档模式，等价于 `-dR --preserve=all`：\n"
            "递归 + 符号链接原样 + 权限/属主/时间全保留。\n\n"
            "其余三个为什么不够：\n"
            "- `-r` 只递归，**权限按 umask 重算**（私钥会从 600 变 644，就是这条坑）\n"
            "- `-p` 保留属性，但**不保证递归**（要写 `-rp` 一起）\n"
            "- `-f` 是「强制覆盖」，跟保留属性没关系\n\n"
            "★ 备份 `~/.ssh` 时尤其要用 `-a` —— 用 `-r` 备份出来的私钥权限太开放，"
            "ssh 会**拒绝使用**它。"),
        tags=["cp", "-a", "权限", "备份"], difficulty=3,
    ))

    add(tf(
        "rm -rf 删掉的文件能从回收站找回吗",
        "在终端里用 `rm -rf` 删掉的文件，可以从「回收站」里找回来。",
        False,
        subject=SUBJ, section=sec,
        explanation=(
            "**错**，而且是本讲最危险的一条。\n\n"
            "命令行的 `rm` **没有回收站**。图形界面能「从回收站还原」，"
            "那是**文件管理器自己实现的功能**（它把文件挪到 `~/.local/share/Trash`），"
            "和 `rm` 是两套完全独立的东西。\n\n"
            "安全习惯三条：\n"
            "1. 删之前先 `ls` 看清单\n"
            "2. 用通配符时先 `echo rm -rf *` 让它**只打印展开结果**，确认无误再删\n"
            "3. 需要可回滚就 `mv` 到 `~/trash` 目录，别直接 rm\n\n"
            "★ 铁律：**永远不要**在 `/` 或 `~` 下敲 `rm -rf *`（中间那个空格是致命的）。"),
        tags=["rm", "回收站", "安全", "高频错点"], difficulty=2,
    ))

    add(mc(
        "tail -n +5 输出什么",
        "文件 `a.txt` 有 20 行，`tail -n +5 a.txt` 输出什么？",
        ["最后 5 行", "前 5 行", "从第 5 行到文件末尾", "除最后 5 行外的全部"],
        "C",
        subject=SUBJ, section=sec,
        explanation=(
            "**从第 5 行一路输出到末尾**（第 5~20 行，共 16 行）。\n\n"
            "`+N` 的含义是「**从第 N 行开始**数」，不是「取 N 行」。\n\n"
            "对照记忆：\n"
            "| 写法 | 含义 |\n"
            "|---|---|\n"
            "| `tail -n 5 f` | 最后 5 行 |\n"
            "| `tail -n +5 f` | 从第 5 行到末尾 |\n"
            "| `head -n 5 f` | 前 5 行 |\n"
            "| `head -n -5 f` | 去掉最后 5 行 |\n\n"
            "真机上验证：`seq 1 20 > a.txt && tail -n +5 a.txt | head -1` 会打出 `5`。"),
        tags=["tail", "+N", "取行"], difficulty=3,
    ))

    add(tf(
        "head -n -3 是语法错误吗",
        "`head -n -3 f` 是非法的写法，head 不接受负数。",
        False,
        subject=SUBJ, section=sec,
        explanation=(
            "**错**，它是合法的。\n\n"
            "`head -n -3 f` 表示「**去掉最后 3 行**，把其余的全部输出」。"
            "`-` 在这里是「从末尾砍掉」的意思。\n\n"
            "真正非法的是 `head -n +3 f` —— **head 不认 `+`**，"
            "会报 `invalid number of lines: '+3'`。\n\n"
            "★ 口诀：**`+` 归 tail，`-` 归 head**。\n"
            "（反过来说，`tail -n -5 f` 也是非法的 —— tail 的 `-n` 只认数字或 `+数字`。）"),
        tags=["head", "负数", "易混"], difficulty=3,
    ))

    add(mc(
        "tar -zcvf 里的 z 是什么",
        "`tar -zcvf a.tar.gz dir/` 里的 `z` 表示什么？",
        ["compress（.Z 老格式）", "gzip", "zip", "zstd"],
        "B",
        subject=SUBJ, section=sec,
        explanation=(
            "小写 **`-z` = gzip**。\n\n"
            "顺带把四个压缩选项一次分清：\n\n"
            "| 选项 | 压缩器 | 典型后缀 |\n"
            "|---|---|---|\n"
            "| `-z` | gzip | `.tar.gz` / `.tgz` |\n"
            "| `-j` | bzip2 | `.tar.bz2` / `.tbz2` |\n"
            "| `-Z` | compress | `.tar.Z`（老古董） |\n"
            "| `-J` | xz | `.tar.xz` |\n\n"
            "`zip` 是另一个**独立命令**（`zip -r a.zip dir/`），不是 tar 的选项。"),
        tags=["tar", "gzip", "压缩格式"], difficulty=2,
    ))

    add(tf(
        "touch 已存在的文件会清空内容吗",
        "对一个已经存在且有内容的文件执行 `touch`，会把它的内容清空。",
        False,
        subject=SUBJ, section=sec,
        explanation=(
            "**错**。`touch` 只改**时间戳**（访问时间 atime / 修改时间 mtime），"
            "文件内容一个字都不会动。\n\n"
            "`touch` 的两个用途：\n"
            "1. 文件**不存在**时新建一个空文件\n"
            "2. 文件**已存在**时把时间更新成现在（常用在 make 里强制重新编译）\n\n"
            "真想清空内容，用**重定向**：`> 文件名`（注意前面**没有命令**）。\n"
            "验证：`echo hi > a.txt && touch a.txt && cat a.txt` —— 还是打出 `hi`。\n\n"
            "★ 这是典型的「想当然」错点：名字叫 touch（触碰），"
            "确实就是「碰一下改个时间」，仅此而已。"),
        tags=["touch", "时间戳", "清空", "易混"], difficulty=2,
    ))

    add(mc(
        "mkdir -p 里的 p 是什么",
        "`mkdir -p a/b/c` 里的 `-p` 表示什么？",
        ["permission（指定权限）", "protect（保护，存在就不覆盖）",
         "parents（缺失的父目录一并创建）", "print（打印创建了哪些）"],
        "C",
        subject=SUBJ, section=sec,
        explanation=(
            "**`-p` = parents**，把缺失的父目录**一路补建**出来。\n\n"
            "`mkdir a/b/c` 在 `a` 不存在时会直接报错：\n"
            "`mkdir: cannot create directory 'a/b/c': No such file or directory`\n\n"
            "加 `-p` 之后，`a`、`a/b`、`a/b/c` 三层一次建出来，"
            "而且**目标已存在也不报错**（幂等）—— 所以脚本里写 `mkdir -p` 最省心。\n\n"
            "指定权限是 **`-m`**：`mkdir -m 700 secret`。"),
        tags=["mkdir", "-p", "多级目录"], difficulty=1,
    ))

    add(tf(
        "tar xf 不写 z 会解压失败吗",
        "`tar xf a.tar.gz`（不写 `z`）会解压失败，必须写成 `tar xzf a.tar.gz`。",
        False,
        subject=SUBJ, section=sec,
        explanation=(
            "**错**。**现代 GNU tar 读归档时会自动识别压缩格式**，"
            "所以 `tar xf a.tar.gz` 能正常解压（GNU tar 官方手册原话："
            "读压缩包不需要额外选项，tar 会自动检测）。\n\n"
            "★ 但要分清**读**和**写**：\n"
            "- **解压**可以省：`tar xf a.tar.gz` ✅ 自动识别\n"
            "- **打包不行**：`tar cf a.tar.gz dir/` 会打出一个**不压缩**的 tar "
            "（白白顶着 `.gz` 后缀），必须写明 `-z`\n\n"
            "因为创建时要**决定调用哪个压缩程序**，tar 猜不出来。\n\n"
            "（`xz`/`bzip2` 同理：解压可省，打包要写。）"),
        tags=["tar", "自动识别", "解压"], difficulty=4,
    ))

    add(mc(
        "只看 zip 包里有什么，不解压",
        "你想先看看 `a.zip` 里装了哪些文件，**不想真的解压**。用哪条命令？",
        ["unzip a.zip", "unzip -l a.zip", "unzip -d a.zip", "zip -l a.zip"],
        "B",
        subject=SUBJ, section=sec,
        explanation=(
            "**`unzip -l a.zip`**（`-l` = list）—— 只列出内容清单。\n\n"
            "其余三个为什么不对：\n"
            "- `unzip a.zip` 会**真的解压**到当前目录\n"
            "- `unzip -d a.zip` 的 `-d` 后面跟的是「**解压到哪个目录**」，"
            "把 `a.zip` 当目录名用，语义全错\n"
            "- `zip -l a.zip` 是**压缩**命令 `zip`，不是解压命令 `unzip`\n\n"
            "tar 那边对应的写法是 `tar -tzvf bak.tar.gz`（`t` = list，只看不解）。"),
        tags=["unzip", "zip", "查看内容"], difficulty=2,
    ))

    add(tf(
        "less 比 more 强在哪",
        "`less` 可以往回翻页，`more` 不能。",
        True,
        subject=SUBJ, section=sec,
        explanation=(
            "**对**。这正是 `less` 存在的理由 —— 名字就是个冷幽默："
            "「less is more」。\n\n"
            "| | more | less |\n"
            "|---|---|---|\n"
            "| 向下翻页 | 空格 / Enter | 空格 / PgDn |\n"
            "| **向上翻页** | ❌ 不行 | ✅ ↑ / PgUp / b |\n"
            "| 搜索 | ❌ | ✅ `/关键词`，`n` 下一个 |\n"
            "| 退出后是否清屏 | 不清 | **清屏** ★ |\n\n"
            "★ 最后一行是实验报告里最容易吃亏的点："
            "`less` 退出（按 `q`）会把整屏清掉，所以**必须先截图再退出**。\n\n"
            "两个命令 Fedora 44 上都是默认装好的（`more` 由 util-linux-core 提供）。"),
        tags=["less", "more", "分页器"], difficulty=1,
    ))

    add(tf(
        "删掉符号链接会删掉真实目录吗",
        "用 `rm /myshare` 删掉一个指向目录的符号链接，那个真实目录也会被删掉。",
        False,
        subject=SUBJ, section=sec,
        explanation=(
            "**错**。符号链接相当于 Windows 的快捷方式 —— "
            "它只是一个存着目标路径的**小文件**，删掉它**不会碰到**真实目录。\n\n"
            "★ 但有个**末尾斜杠**的陷阱必须记住：\n"
            "```bash\n"
            "rm /myshare        # ✅ 删链接本身\n"
            "rm -r /myshare/    # ❌ 末尾那个斜杠会让内核「解引用」链接，\n"
            "                   #    真的去删目标目录里的东西！\n"
            "```\n"
            "所以删符号链接时**末尾不要带斜杠**，也**不要加 `-r`**。\n\n"
            "怎么一眼认出符号链接：`ls -l` 输出的**第一个字符是 `l`**，"
            "并且中间有 `-> 目标路径`：\n"
            "```\n"
            "lrwxrwxrwx. 1 root root 20 10月 12 08:0x myshare -> /usr/local/sdutshare\n"
            "```"),
        tags=["ln", "符号链接", "rm", "安全"], difficulty=3,
    ))

    add(tf(
        "/etc/shells 是什么",
        "`/etc/shells` 文件登记的是系统上「合法的登录 shell」白名单。",
        True,
        subject=SUBJ, section=sec,
        explanation=(
            "**对**。`/etc/shells` 是系统认可的**合法登录 shell 白名单**，"
            "一行一个绝对路径。\n\n"
            "Fedora 44 上通常长这样：\n"
            "```\n"
            "/bin/sh\n"
            "/bin/bash\n"
            "/usr/bin/sh\n"
            "/usr/bin/bash\n"
            "```\n"
            "（装了 zsh / tmux 之类才会多出对应的行。）\n\n"
            "**谁在用它**：`chsh` 改默认 shell 时会**到这里查** —— "
            "你想把 shell 改成 `/usr/local/bin/myshell`，"
            "必须先把这行加进 `/etc/shells`，否则会被拒绝。\n\n"
            "**怎么列**：`cat /etc/shells`，或者 `chsh -l`（效果一样）。"),
        tags=["shells", "chsh", "shell"], difficulty=2,
    ))

    add(tf(
        "用相对路径切到子目录，`cd share` 与 `cd ../share` 等价吗",
        "当前在 `/usr/local`，`cd share` 和 `cd ../share` 会到达同一个目录。",
        False,
        subject=SUBJ, section=sec,
        explanation=(
            "**错**。这是「相对路径」最阴的一个坑，因为**两条命令都不会报错**：\n\n"
            "| 命令 | 到达 | 说明 |\n"
            "|---|---|---|\n"
            "| `cd share` | `/usr/local/share` | ✅ 子目录 |\n"
            "| `cd ../share` | `/usr/share` | ❌ 上级目录下的 share |\n\n"
            "而 `/usr/share` 在真实系统上**确实存在**（一大堆文档、man 手册都放那）——"
            "所以 `cd ../share` 不会报 `No such file`，它会**安安静静地把你带到错的地方**。\n\n"
            "★ 防御习惯：**切完目录顺手 `pwd`**。\n"
            "实验报告里带上 `pwd` 输出，既证明路径对，又方便老师核对。"),
        tags=["cd", "相对路径", "pwd", "易混"], difficulty=3,
    ))


# ===================================================================== #
#  三、《Linux基础命令》B 组 —— 写命令
# --------------------------------------------------------------------- #
#  这些题用 fill（填空），判定走 cmd 宽容口径：
#  `-l -a` 与 `-la`、`-la` 与 `-al` 都被认为是同一条命令。
# ===================================================================== #
def part_b_group() -> None:
    sec = "基础命令 · B 组 写命令"

    add(fill(
        "一步回到上一个目录",
        "你现在的提示符在某处，先执行了 `cd /etc`，"
        "现在想**用一条命令**回到进 `/etc` 之前的位置。写出这条命令。",
        ["cd -"],
        subject=SUBJ, section=sec, difficulty=2, total_score=10,
        explanation=(
            "**`cd -`**。它读环境变量 **`$OLDPWD`** —— shell 每次切换目录前，"
            "都会把「原来在哪」记到这里。\n\n"
            "两个附带效果：\n"
            "1. 切换完会把目标路径**打印出来**（所以你能一眼确认跳对没有）\n"
            "2. 再执行一次 `cd -` 会**跳回去**（两个目录之间来回横跳）\n\n"
            "真机验证：\n"
            "```bash\n"
            "cd /tmp; cd /etc; cd -     # 打出 /tmp，并回到 /tmp\n"
            "echo $OLDPWD               # /etc\n"
            "```"),
        tags=["cd", "OLDPWD"], hint="提示：用的是 shell 记录历史的那个变量，只要两个字符。",
    ))

    add(fill(
        "列出目录下所有条目（含隐藏）的长格式",
        "用 `ls` 列出 `/etc` 下所有条目（**包括隐藏文件**）的详细长格式。",
        ["ls -la /etc", "ls -al /etc", "ls -lah /etc", "ls -alh /etc",
         "ls -lA /etc", "ls -Al /etc", "ls -l -a /etc"],
        subject=SUBJ, section=sec, difficulty=1, total_score=10,
        explanation=(
            "**`ls -la /etc`**（或 `ls -al /etc`，两个选项顺序无所谓）。\n\n"
            "- `-l` = long，详细格式（权限 / 链接数 / 属主 / 属组 / 大小 / 时间 / 名字）\n"
            "- `-a` = all，含隐藏文件\n\n"
            "三种常见变体都是对的，判题时都认：\n"
            "- `ls -lah /etc` —— 多一个 `-h`，把大小显示成 `4.0K` 这种人类可读格式\n"
            "- `ls -lA /etc` —— 用 `-A` 替 `-a`，**不列 `.` 和 `..` 那两行**\n"
            "- `ls -l -a /etc` —— 选项分开写\n\n"
            "★ 本平台的命令题按「宽容口径」判：空白多少、`-l -a` 还是 `-la`、"
            "`-la` 还是 `-al`，都算对。"),
        tags=["ls", "-l", "-a"], hint="提示：两个短选项组合，长格式 + 全部。",
    ))

    add(fill(
        "复制目录并保留权限与时间戳",
        "把 `~/docs` 整个目录复制到 `/tmp/` 下，"
        "要求**保留权限、属主和时间戳**。写出这条命令。",
        ["cp -a ~/docs /tmp/", "cp -a ~/docs /tmp", "cp -rp ~/docs /tmp/",
         "cp -a /home/lijihao/docs /tmp/"],
        subject=SUBJ, section=sec, difficulty=3, total_score=12,
        explanation=(
            "**`cp -a ~/docs /tmp/`**。\n\n"
            "`-a` = 归档模式（archive），等价于 `-dR --preserve=all`，一次满足全部要求：\n"
            "- `-R` 递归\n"
            "- `-d` 符号链接原样复制（不跟随）\n"
            "- `--preserve=all` 保留权限、属主、时间戳、扩展属性\n\n"
            "**`cp -rp ~/docs /tmp/`** 也常被接受（递归 + 保留属性），"
            "差别只在 `-r` 会**跟随符号链接**而不是照搬。\n\n"
            "★ 反面教材：裸 `cp ~/docs /tmp/` 会报 "
            "`cp: -r not specified; omitting directory` —— **什么都不复制**，"
            "但它**不报错退出**（退出码是 1，但只打印一句警告），很容易以为成功了。"),
        tags=["cp", "-a", "归档模式"], hint="提示：一个选项就能全搞定，首字母是「归档」的那个。",
    ))

    add(fill(
        "只看目录本身的一行信息",
        "只想看 `/etc` **目录自己**（不是它里面的内容）的信息，输出一行。写出命令。",
        ["ls -ld /etc", "ls -dl /etc"],
        subject=SUBJ, section=sec, difficulty=2, total_score=10,
        explanation=(
            "**`ls -ld /etc`**。\n\n"
            "关键是 **`-d`**：它告诉 ls「遇到目录**不要展开**，只报这个目录本身」。\n\n"
            "对照：\n"
            "```bash\n"
            "ls -l /etc      # 几十行，全是 /etc 里面的东西\n"
            "ls -ld /etc     # 一行：drwxr-xr-x. 1 root root 8192 Oct 12 09:00 /etc\n"
            "```\n\n"
            "★ 这个要求还有个常见用法：`ls -d */` 只列当前目录下的**子目录**"
            "（`*/` 是通配符，先被 shell 展开成各子目录名）。"),
        tags=["ls", "-d"], hint="提示：加一个「别展开目录」的选项。",
    ))

    add(fill(
        "取文件的前 50 行",
        "取 `a.log` 的前 50 行。写出这条命令（用现代写法）。",
        ["head -n 50 a.log", "head -50 a.log"],
        subject=SUBJ, section=sec, difficulty=1, total_score=10,
        explanation=(
            "**`head -n 50 a.log`**。\n\n"
            "`-n` 后面跟行数，**不写 `-n` 时 head 默认取前 10 行**。\n\n"
            "老式写法 `head -50 a.log` 也能用（数字紧跟选项），"
            "但 coreutils 手册把它归为**过时写法**，建议统一用 `-n 50`。\n\n"
            "★ 前 50 行 vs 后 50 行：\n"
            "- 前 50 → `head -n 50`\n"
            "- 后 50 → `tail -n 50`（**不加 `+`**！）\n\n"
            "真机验证：`seq 1 100 > a.log && head -n 50 a.log | tail -1` 打出 `50`。"),
        tags=["head", "-n"], hint="提示：head + -n + 数字 + 文件名。",
    ))

    add(fill(
        "取从第 100 行到末尾",
        "取 `a.log` 从第 100 行开始、一直到文件末尾的内容。写出这条命令。",
        ["tail -n +100 a.log", "tail +100 a.log"],
        subject=SUBJ, section=sec, difficulty=3, total_score=12,
        explanation=(
            "**`tail -n +100 a.log`**。\n\n"
            "`+100` 的意思是「**从第 100 行开始数**」，不是「取 100 行」。\n\n"
            "★ 这里是最容易写错的地方 —— **必须用 tail，不能用 head**：\n"
            "```bash\n"
            "tail -n +100 a.log       # ✅ 第 100 行 → 末尾\n"
            "head -n +100 a.log       # ❌ head: invalid number of lines: '+100'\n"
            "```\n\n"
            "等价写法（思路不同，结果一样）：\n"
            "```bash\n"
            "sed -n '100,$p' a.log    # $ 表示最后一行\n"
            "awk 'NR>=100' a.log\n"
            "```"),
        tags=["tail", "+N", "取行"], hint="提示：从中间取到末尾，用的是 tail 的特殊写法（带加号）。",
    ))

    add(fill(
        "取除最后 10 行外的全部内容",
        "取 `a.log` 中**除最后 10 行之外**的所有行。写出这条命令。",
        ["head -n -10 a.log", "head -10 a.log"],
        subject=SUBJ, section=sec, difficulty=3, total_score=12,
        explanation=(
            "**`head -n -10 a.log`**。\n\n"
            "`-10` 表示「**从末尾砍掉 10 行**」，剩下的全输出。\n\n"
            "★ 这里正是和上一题**对称**的机关：\n"
            "| 想要什么 | 写法 | 谁的特权 |\n"
            "|---|---|---|\n"
            "| 从第 N 行到末尾 | `tail -n +N` | `+` 是 tail 的 |\n"
            "| 去掉最后 N 行 | `head -n -N` | `-` 是 head 的 |\n\n"
            "反过来写都会报 `invalid number`：`head -n +N` ❌、`tail -n -N` ❌。\n\n"
            "等价写法：`sed '$-10,$d'` 不太好写，实际工作中 `head -n -10` 最省事。"),
        tags=["head", "负数", "取行"], hint="提示：和「从第 N 行开始」正好相反 —— 这次 `-` 号归 head 用。",
    ))

    add(fill(
        "打包并 gzip 压缩",
        "把 `~/project` 目录打包并用 gzip 压缩，生成 `project.tar.gz`。"
        "写出这条命令（**不需要**显示处理过程）。",
        ["tar -czf project.tar.gz ~/project", "tar -czf project.tar.gz /home/lijihao/project",
         "tar czf project.tar.gz ~/project", "tar -zcf project.tar.gz ~/project"],
        subject=SUBJ, section=sec, difficulty=2, total_score=12,
        explanation=(
            "**`tar -czf project.tar.gz ~/project`**。\n\n"
            "四个字母各管一摊：\n"
            "| 字母 | 作用 |\n"
            "|---|---|\n"
            "| `-c` | create，创建归档 |\n"
            "| `-z` | 走 gzip 压缩（**小写！大写 `-Z` 是 compress**） |\n"
            "| `-v` | verbose，显示处理过程（本题不需要，所以省掉） |\n"
            "| `-f` | file，**后面紧跟归档文件名** |\n\n"
            "★ `-f` 必须是**最后一个**（或者说它的参数必须紧跟其后）：\n"
            "`tar -czf project.tar.gz ~/project` ✅\n"
            "`tar -cfz project.tar.gz ~/project` ❌ —— 会把 `z` 当成归档文件名。\n\n"
            "口诀：**`czvf` 打包、`xzvf` 解包、`tzvf` 看内容**。"),
        tags=["tar", "gzip", "打包"], hint="提示：tar + 创建 + gzip + 指定文件名。",
    ))

    add(fill(
        "查看压缩包里有哪些文件",
        "查看 `bak.tar.gz` 里包含哪些文件，**但不要解压**。写出这条命令。",
        ["tar -tzvf bak.tar.gz", "tar -tzf bak.tar.gz", "tar tzf bak.tar.gz"],
        subject=SUBJ, section=sec, difficulty=2, total_score=10,
        explanation=(
            "**`tar -tzvf bak.tar.gz`**（`t` = list）。\n\n"
            "三个字母的分工：`-t` 列出内容、`-z` 让 tar 先解 gzip、`-v` 显示详细信息"
            "（权限/属主/大小/时间）。\n\n"
            "嫌 `-v` 太啰嗦就省掉：`tar -tzf bak.tar.gz` 只打文件名。\n\n"
            "★ 它的价值：**解压前先看一眼包里是什么**。\n"
            "很多压缩包解出来是 `pkg/pkg/...` 这种双层嵌套 —— "
            "先 `-t` 看一眼，就知道该不该加 `--strip-components=1`。\n\n"
            "（z 其实也可以省：现代 GNU tar 读归档时会自动识别压缩格式，"
            "但显式写出来更好读。）"),
        tags=["tar", "-t", "查看归档"], hint="提示：tar + 一个表示「列出」的选项。",
    ))

    add(fill(
        "把压缩包解压到指定目录",
        "把 `bak.tar.gz` 解压到 `/tmp/out` 目录下。写出完整的命令序列"
        "（`/tmp/out` **可能还不存在**）。",
        ["mkdir -p /tmp/out && tar -xzvf bak.tar.gz -C /tmp/out",
         "mkdir -p /tmp/out; tar -xzvf bak.tar.gz -C /tmp/out",
         "mkdir -p /tmp/out; tar -xzf bak.tar.gz -C /tmp/out",
         "mkdir -p /tmp/out && tar -xzf bak.tar.gz -C /tmp/out"],
        subject=SUBJ, section=sec, difficulty=4, total_score=15,
        explanation=(
            "```bash\n"
            "mkdir -p /tmp/out\n"
            "tar -xzvf bak.tar.gz -C /tmp/out\n"
            "```\n\n"
            "★ **两个必须踩对的点**：\n\n"
            "**1. `-C` 指定的目录必须已存在** —— tar **不会**替你建。\n"
            "漏了 `mkdir` 会报 `tar: /tmp/out: Cannot open: No such file or directory`。\n\n"
            "**2. `-C` 要放在归档文件名之后**：\n"
            "```bash\n"
            "tar -xzvf bak.tar.gz -C /tmp/out     # ✅\n"
            "tar -xzvf bak.tar.gz -C /tmp/out    # -C 前面的 -f 已经吃掉包名了，这里顺序对\n"
            "tar -xzvf -C /tmp/out bak.tar.gz     # ❌ -f 后面跟的是 -C，tar 把 \"-C\" 当归档名\n"
            "```\n"
            "记法：**`-f` 后面永远紧跟包名，其他选项都排它后面**。\n\n"
            "顺带一提：`tar` 解压时会打一句 `Removing leading '/' from member names` —— "
            "**这是正常的**（防止把文件覆盖回绝对路径），不是错误。"),
        tags=["tar", "-C", "解压", "目录"], hint="提示：先建目录（可能要多级），再用 `-C` 指定解压目标。",
    ))

    add(fill(
        "一次性创建多级目录",
        "一次性创建多级目录 `data/2026/10/report`（中间几层都还不存在）。写出命令。",
        ["mkdir -p data/2026/10/report"],
        subject=SUBJ, section=sec, difficulty=1, total_score=10,
        explanation=(
            "**`mkdir -p data/2026/10/report`**。\n\n"
            "`-p`（parents）会把缺失的 `data`、`data/2026`、`data/2026/10` 一并建出来。\n\n"
            "不加 `-p` 会直接报错：\n"
            "`mkdir: cannot create directory 'data/2026/10': No such file or directory`\n"
            "（`data` 都不存在，没法在它下面建 `2026`。）\n\n"
            "★ `-p` 还有个隐性好处：**目标已存在也不报错**，"
            "所以脚本开头写 `mkdir -p /var/tmp/x` 可以放心重复执行。"),
        tags=["mkdir", "-p"], hint="提示：mkdir + 一个选项。",
    ))

    add(fill(
        "一次建三个空文件",
        "在 `/tmp` 下**用一条命令**创建三个空文件 `a.txt`、`b.txt`、`c.txt`。"
        "写出这条命令。",
        ["touch /tmp/a.txt /tmp/b.txt /tmp/c.txt",
         "touch /tmp/{a,b,c}.txt",
         "cd /tmp && touch a.txt b.txt c.txt",
         "touch /tmp/a.txt; touch /tmp/b.txt; touch /tmp/c.txt"],
        subject=SUBJ, section=sec, difficulty=2, total_score=12,
        explanation=(
            "最直接的写法 —— **`touch` 接受多个文件名**：\n"
            "```bash\n"
            "touch /tmp/a.txt /tmp/b.txt /tmp/c.txt\n"
            "```\n\n"
            "更短的**花括号展开**（bash 特性，shell 先展开再交给 touch）：\n"
            "```bash\n"
            "touch /tmp/{a,b,c}.txt\n"
            "```\n"
            "展开规则：`{a,b,c}.txt` → `a.txt b.txt c.txt`。\n"
            "还能写区间：`{1..5}` → `1 2 3 4 5`、`{a..e}` → `a b c d e`。\n\n"
            "先切目录也行：`cd /tmp && touch a.txt b.txt c.txt`。\n\n"
            "★ 记住 `touch` 的两副面孔：文件**不存在就建**，**存在就只改时间戳**（不动内容）。"),
        tags=["touch", "多文件", "花括号展开"], hint="提示：touch 可以一次接好几个文件名；bash 还支持花括号简写。",
    ))


# ===================================================================== #
#  四、《Linux基础命令》C 组 —— 找错（改写成选择题）
# --------------------------------------------------------------------- #
#  原题是「下面这条命令哪里不对」，开放式。平台上改成
#  「下面哪条是正确写法」，判定明确，考点一分不减。
# ===================================================================== #
def part_c_group() -> None:
    sec = "基础命令 · C 组 找错"

    add(mc(
        "用 gzip 压缩，哪条对",
        "下面四条都想「用 **gzip** 把 `dir/` 打包成 `bak.tar.gz`」，只有一条是对的。",
        ["tar -Zcvf bak.tar.gz dir/", "tar -zcvf bak.tar.gz dir/",
         "tar -jcvf bak.tar.gz dir/", "tar -Jcvf bak.tar.gz dir/"],
        "B",
        subject=SUBJ, section=sec,
        explanation=(
            "**`tar -zcvf bak.tar.gz dir/`**（小写 `-z` = gzip）。\n\n"
            "另外三条错在哪：\n\n"
            "| 写法 | 实际行为 |\n"
            "|---|---|\n"
            "| `-Z` | 调用 **compress**（老 `.Z` 格式）。没装的机器直接报错，"
            "有的版本会兜底成 gzip —— 看着像成功，其实不符合预期 |\n"
            "| `-j` | 调用 **bzip2**，产出的是 `.tar.bz2` 格式，"
            "顶着 `.gz` 后缀名不符实 |\n"
            "| `-J` | 调用 **xz**，同上 |\n\n"
            "★ 一句话记牢：**z 小写 gzip、Z 大写 compress、j 是 bzip2、J 是 xz**。"),
        tags=["tar", "gzip", "找错"], difficulty=3,
    ))

    add(mc(
        "从第 100 行开始显示，哪条对",
        "下面四条都想「从 `a.log` 的**第 100 行**开始显示到末尾」，只有一条能跑通。",
        ["head -n +100 a.log", "head -n -100 a.log",
         "tail -n +100 a.log", "tail -n -100 a.log"],
        "C",
        subject=SUBJ, section=sec,
        explanation=(
            "**`tail -n +100 a.log`**。\n\n"
            "另外三条都会报 `invalid number of lines`：\n\n"
            "| 写法 | 报错/行为 |\n"
            "|---|---|\n"
            "| `head -n +100` | ❌ head **不认 `+`**，报 `invalid number: '+100'` |\n"
            "| `head -n -100` | ⚠️ **合法但意思不同** —— 是「去掉最后 100 行」，"
            "不是「从第 100 行开始」 |\n"
            "| `tail -n -100` | ❌ tail 的 `-n` 只认数字或 `+数字`，不认负号 |\n\n"
            "★ **`+` 归 tail，`-` 归 head** —— 这八个字能挡掉这一族所有的错。"),
        tags=["head", "tail", "找错", "取行"], difficulty=3,
    ))

    add(mc(
        "想统计行数，哪条对",
        "你想知道 `a.log` 一共有多少行。下面哪条的命令**用途正确**？",
        ["cat -n a.log", "wc -l a.log", "tail -n a.log", "head -n a.log"],
        "B",
        subject=SUBJ, section=sec,
        explanation=(
            "**`wc -l a.log`** —— 输出 `行数 文件名`，比如 `1024 a.log`。\n\n"
            "其余三条的问题：\n"
            "- `cat -n a.log` 是**给每行加行号后全打印出来**，"
            "不是统计 —— 大文件会刷几万行屏，慢且没用\n"
            "- `tail -n a.log` 语法不完整（`-n` 后面缺数字）\n"
            "- `head -n a.log` 同上\n\n"
            "★ 只想要数字（不要文件名）时：`wc -l < a.log`，"
            "或者 `cat a.log | wc -l`。\n\n"
            "补充：`wc` 还能数单词（`-w`）和字符（`-c`），不加选项三个都打。"),
        tags=["wc", "cat", "找错"], difficulty=2,
    ))

    add(mc(
        "想删掉一个目录，哪条对",
        "你想删掉 `/tmp/lab` 这个目录，**不要**影响当前目录里的其他文件。"
        "下面哪条是对的？",
        ["rm -rf /tmp/lab *", "rm -rf /tmp/lab", "rm /tmp/lab", "rm -r /tmp/lab *"],
        "B",
        subject=SUBJ, section=sec,
        explanation=(
            "**`rm -rf /tmp/lab`** —— 只有一个目标，干净利落。\n\n"
            "★ 前两条为什么危险（这是本组最要命的一题）：\n\n"
            "```bash\n"
            "rm -rf /tmp/lab *\n"
            "                ↑ 这个空格让它变成两个参数\n"
            "```\n"
            "`*` 会被 shell 展开成**当前目录下的所有条目** —— "
            "等于顺手把你当前所在的目录清空了，完全不是本意。\n\n"
            "第三条 `rm /tmp/lab` 也错：删目录**必须加 `-r`**，"
            "否则报 `rm: cannot remove '/tmp/lab': Is a directory`。\n\n"
            "**两条保命习惯**：\n"
            "1. 删之前先 `ls /tmp/lab` 看看里面有什么\n"
            "2. 用通配符时先 `echo rm -rf *` —— **只让它打印展开结果**，确认无误再去掉 echo"),
        tags=["rm", "-rf", "找错", "安全"], difficulty=3,
    ))

    add(mc(
        "备份 ssh 私钥，哪条对",
        "你要把 `~/.ssh` 备份到 `/tmp/ssh_backup`，"
        "备份出来**必须**还能被 ssh 直接用（私钥权限不能被改宽）。哪条对？",
        ["cp -r ~/.ssh /tmp/ssh_backup", "cp -a ~/.ssh /tmp/ssh_backup",
         "cp ~/.ssh /tmp/ssh_backup", "mv ~/.ssh /tmp/ssh_backup"],
        "B",
        subject=SUBJ, section=sec,
        explanation=(
            "**`cp -a ~/.ssh /tmp/ssh_backup`**。\n\n"
            "★ `-r` 的隐患（本题的机关）：它会**按 umask 重算权限**。"
            "`~/.ssh` 里的私钥本来是 `600`（只有属主可读写），"
            "用 `-r` 复制出来可能变成 `644`（同组和其他人可读）。\n\n"
            "后果：用这份备份恢复后，**ssh 会拒绝使用私钥**，报\n"
            "```\n"
            "Permissions 0644 for '/home/user/.ssh/id_rsa' are too open.\n"
            "```\n\n"
            "`-a`（归档模式）= 递归 + 保留权限/属主/时间 + 符号链接原样。\n\n"
            "另外两个：`cp`（不带选项）会报 `omitting directory` 什么都不干；"
            "`mv` 是**移动**不是复制 —— 源文件会消失，那就不是「备份」了。"),
        tags=["cp", "-a", "ssh", "权限", "找错"], difficulty=4,
    ))

    add(mc(
        "复制目录，哪条对",
        "把 `~/docs` 整个目录复制到 `/tmp/` 下。下面哪条**真的会复制成功**？",
        ["cp ~/docs /tmp/", "cp -r ~/docs /tmp/",
         "cp -u ~/docs /tmp/", "cp -i ~/docs /tmp/"],
        "B",
        subject=SUBJ, section=sec,
        explanation=(
            "**`cp -r ~/docs /tmp/`** —— 复制目录**必须**加递归开关 "
            "（`-r`、`-R` 或 `-a`）。\n\n"
            "不加会得到：\n"
            "```\n"
            "cp: -r not specified; omitting directory '/home/lijihao/docs'\n"
            "```\n"
            "⚠️ **注意这是个「温柔的错误」**：它只打印一句警告、跳过这个目录，"
            "而不是报错崩掉 —— 在脚本里跑的话，你以为复制成功了，其实什么都没发生。\n\n"
            "另外两个选项：\n"
            "- `-u`（update）只在目标比源**旧**时才复制 —— 跟「能不能复制目录」无关\n"
            "- `-i`（interactive）覆盖前先问一句 —— 同理，不解决递归问题\n\n"
            "★ 更好的选择是 **`cp -a ~/docs /tmp/`**：递归 + 保留权限时间。"),
        tags=["cp", "-r", "找错", "递归"], difficulty=2,
    ))

    add(mc(
        "解压到指定目录，哪条对",
        "把 `bak.tar.gz` 解压到 `dir/` 目录下。下面哪条对？",
        ["tar -xzvf dir/ bak.tar.gz", "tar -xzvf bak.tar.gz -C dir/",
         "tar -xzvf bak.tar.gz dir/", "tar -xzvf -C bak.tar.gz dir/"],
        "B",
        subject=SUBJ, section=sec,
        explanation=(
            "**`tar -xzvf bak.tar.gz -C dir/`**。\n\n"
            "★ 每条错误写法的病因都是**同一个**：`-f` 后面必须紧跟归档文件名。\n\n"
            "| 写法 | 报错 |\n"
            "|---|---|\n"
            "| `-f dir/ bak.tar.gz` | tar 把 `dir/` 当成包名 → "
            "`tar: dir/: Cannot open: No such file or directory` |\n"
            "| `bak.tar.gz dir/`（用位置当 `-C`） | tar 把 `dir/` 当成"
            "「要解压的成员名」→ 报找不到成员 |\n"
            "| `-C bak.tar.gz dir/` | tar 把 `bak.tar.gz` 当成目录、把 `dir/` 当成员 |\n\n"
            "**一句话记牢**：`-f` 后面永远紧跟着那个压缩包的**文件名**，"
            "其他所有选项（包括 `-C`）都排在它后面。"),
        tags=["tar", "-C", "找错", "解压"], difficulty=3,
    ))

    add(mc(
        "父目录不存在时建多级目录，哪条对",
        "当前目录下**没有** `data`，你要建出 `data/2026/10`。哪条对？",
        ["mkdir data/2026/10", "mkdir -p data/2026/10",
         "mkdir -r data/2026/10", "mkdir -a data/2026/10"],
        "B",
        subject=SUBJ, section=sec,
        explanation=(
            "**`mkdir -p data/2026/10`**。\n\n"
            "不加 `-p` 的报错很直白：\n"
            "```\n"
            "mkdir: cannot create directory 'data/2026/10': No such file or directory\n"
            "```\n"
            "`data` 都不存在，怎么在它下面建 `2026` 呢？\n\n"
            "`-r` 和 `-a` 都**不是 mkdir 的选项**，会报 `invalid option`：\n"
            "- `-r`（recursive）是 `cp` / `rm` / `chmod` 的\n"
            "- `-a`（archive）是 `cp` / `ls` / `tar` 的\n\n"
            "★ 各命令的选项字母**不通用**，别凭感觉套。记 mkdir 就记 **`-p` = parents**。"),
        tags=["mkdir", "-p", "找错"], difficulty=1,
    ))

    add(mc(
        "zip 压缩目录，哪条对",
        "你要把一个**目录** `doc/` 连同里面的文件一起压缩成 `doc.zip`。哪条对？",
        ["zip doc.zip doc/", "zip -r doc.zip doc/",
         "zip -a doc.zip doc/", "zip -x doc.zip doc/"],
        "B",
        subject=SUBJ, section=sec,
        explanation=(
            "**`zip -r doc.zip doc/`**（`-r` = recursive）。\n\n"
            "★ 漏了 `-r` 的后果特别隐蔽：zip **不报错**，"
            "但只把 `doc/` 这个**目录条目本身**记进去，里面的文件一个都没有。\n"
            "解压出来就是一个空目录 —— 所以这题的经典症状是「**压完解开发现是空的**」。\n\n"
            "对照 tar：tar 打包目录**天然递归**（不用加 -r），"
            "而 zip 必须显式写 `-r`。这是两个工具最容易混的一处。\n\n"
            "另外两个：`-a` 是「把文本文件转成 ASCII 模式」（跟递归无关）；"
            "`-x` 是「排除某些文件」。\n\n"
            "顺带：`zip -q -r doc.zip doc/` 的 `-q` 是安静模式（不打印过程）。"),
        tags=["zip", "-r", "找错", "递归"], difficulty=3,
    ))

    add(mc(
        "取最后 5 行，哪条对",
        "取 `a.log` 的**最后 5 行**。下面哪条对？",
        ["tail -n -5 a.log", "tail -n 5 a.log",
         "head -n -5 a.log", "head -n 5 a.log"],
        "B",
        subject=SUBJ, section=sec,
        explanation=(
            "**`tail -n 5 a.log`** —— 不需要任何符号，tail 默认就**从末尾数**。\n\n"
            "| 写法 | 结果 |\n"
            "|---|---|\n"
            "| `tail -n 5` | ✅ 最后 5 行 |\n"
            "| `tail -n -5` | ❌ `invalid number of lines: '-5'` —— tail **不认负号** |\n"
            "| `head -n 5` | ⚠️ 合法，但拿到的是**前** 5 行 |\n"
            "| `head -n -5` | ⚠️ 合法，但意思是「**去掉最后 5 行**」 |\n\n"
            "★ 为什么 tail 不认负号？因为对 tail 来说，「取最后 N 行」是**默认行为**，"
            "负号是多余的；而「从第 N 行开始」才需要用 `+N` 特别说明。\n\n"
            "所以这一族的规律是：\n"
            "- **tail**：默认从末尾数，`+N` = 从第 N 行开始\n"
            "- **head**：默认从头数，`-N` = 砍掉末尾 N 行"),
        tags=["tail", "找错", "取行"], difficulty=2,
    ))

    add(mc(
        "列出名字里含数字的文件，哪条对",
        "当前目录里有 `1`、`report2.txt`、`log2026`、`notes`。"
        "你要列出**名字里含数字**的全部条目。哪条对？",
        ["ls [0-9]", "ls *[0-9]*", "ls [0-9]*", "ls ?[0-9]?"],
        "B",
        subject=SUBJ, section=sec,
        explanation=(
            "**`ls *[0-9]*`** —— 匹配「名字**任意位置**含一个数字」。\n"
            "结果：`1`、`report2.txt`、`log2026`（`notes` 不含数字，不列）。\n\n"
            "逐条对比（假设目录里还有 `3abc.txt`、`7`）：\n\n"
            "| 写法 | 匹配到什么 | 说明 |\n"
            "|---|---|---|\n"
            "| `ls [0-9]` | 只有 `1`、`7` | ★ **名字恰好是一个数字字符** |\n"
            "| `ls *[0-9]*` | `1`、`report2.txt`、`log2026`、`3abc.txt`、`7` | ✅ 含数字 |\n"
            "| `ls [0-9]*` | `1`、`7`、`3abc.txt` | **以数字开头** |\n"
            "| `ls ?[0-9]?` | 名字**恰好 3 个字符**、中间是数字的 | 太窄 |\n\n"
            "★ 通配符三板斧：`*` 任意多个字符、`?` **恰好一个**字符、`[abc]` 字符集。\n"
            "题目问「含数字」多半要 `*[0-9]*`，而 `[0-9]` 单独用只匹配一个字符。"),
        tags=["ls", "通配符", "找错", "glob"], difficulty=3,
    ))


# ===================================================================== #
#  五、课程下发的 4 份实验 PDF —— 抽关键考点
# --------------------------------------------------------------------- #
#  实验 1 是「装虚拟机 + 截 12 张图」，没有可判题的命令；
#  实验 2/3/4 各 10 题，每题抓 1~2 个真正的考点出成题。
# ===================================================================== #
def part_experiments() -> None:
    sec2 = "实验 2 · 基本命令"
    sec3 = "实验 3 · 常用命令"
    sec4 = "实验 4 · 综合命令"

    # ---------- 实验 2 ----------
    add(fill(
        "用相对路径往上走两级",
        "当前在 `/usr/local/bin`，要求**只用相对路径**切换到 `/usr`。写出这条命令。",
        ["cd ../..", "cd ../../"],
        subject=SUBJ, section=sec2, difficulty=2, total_score=10,
        explanation=(
            "**`cd ../..`**。\n\n"
            "`..` 是「上一级目录」，连着写两次就是往上两级：\n"
            "`/usr/local/bin` → `/usr/local` → `/usr` —— 刚好。\n\n"
            "★ 写完顺手 `pwd` 确认。实验报告里带上 `pwd` 输出更清楚。\n\n"
            "顺便记住三种起点的区别：\n"
            "| 写法 | 从哪里算起 |\n"
            "|---|---|\n"
            "| `/usr/local/bin` | 绝对路径，从根 `/` 开始 |\n"
            "| `local/bin` | 相对路径，从**当前目录**开始 |\n"
            "| `../..` | 相对路径，从当前目录往**上**走 |\n\n"
            "还有几个简写：`~` 主目录、`.` 当前目录、`-` 上一个目录。"),
        tags=["cd", "相对路径", "实验 2"], hint="提示：往上两级，每一级两个点。",
    ))

    add(fill(
        "查看系统支持哪些 shell 类型",
        "查看**当前系统支持的 shell 类型**有哪些。写出这条命令。",
        ["cat /etc/shells", "chsh -l", "less /etc/shells", "more /etc/shells"],
        subject=SUBJ, section=sec2, difficulty=2, total_score=10,
        explanation=(
            "**`cat /etc/shells`**（或者 `chsh -l`，两者效果一样）。\n\n"
            "`/etc/shells` 存的是**合法登录 shell 的白名单**，一行一个绝对路径：\n"
            "```\n"
            "/bin/sh\n"
            "/bin/bash\n"
            "/usr/bin/sh\n"
            "/usr/bin/bash\n"
            "```\n\n"
            "★ 这个文件不只是给人看的 —— `chsh` 改默认 shell 时会**查它**。"
            "想换成自定义 shell 必须先加进这个文件。\n\n"
            "**别答错题目**：「系统支持哪些 shell 类型」问的是这份**清单**；"
            "「当前默认用的是哪个 shell」才是 `echo $SHELL`。"),
        tags=["shells", "shell", "实验 2"], hint="提示：这个清单是个文件，直接看它就行。",
    ))

    add(fill(
        "查看当前默认使用的 shell",
        "查看**终端当前默认使用**的 shell。写出这条命令。",
        ["echo $SHELL", "echo ${SHELL}"],
        subject=SUBJ, section=sec2, difficulty=1, total_score=10,
        explanation=(
            "**`echo $SHELL`** —— Fedora Workstation 上打出 `/bin/bash`。\n\n"
            "★ 三个命令看着像，含义有细微差别，实验里可以三个一起截：\n\n"
            "| 命令 | 看的是 |\n"
            "|---|---|\n"
            "| `echo $SHELL` | **登录时登记的**默认 shell（一个环境变量） |\n"
            "| `echo $0` | **当前这个 shell 进程**的名字（交互式 bash 会显示 `-bash`） |\n"
            "| `ps -p $$ -o comm=` | 直接查当前 shell **进程名** → `bash` |\n\n"
            "`$$` 是当前 shell 的 PID（进程号）。"),
        tags=["SHELL", "环境变量", "实验 2"], hint="提示：SHELL 是个大写环境变量。",
    ))

    add(mc(
        "su 后面那个减号到底管什么",
        "实验里要求「切到 root，**打印 root 主目录的绝对路径**」。\n\n"
        "下面哪条能拿到**正确**结果？",
        ["su 然后 pwd", "su - 然后 pwd", "sudo pwd", "su root 然后 echo $HOME"],
        "B",
        subject=SUBJ, section=sec2,
        explanation=(
            "**`su -`** —— 那个减号（等价于 `su - root` / `su -l`）是本题唯一的机关。\n\n"
            "| 命令 | 换身份 | 换环境 | `$HOME` | `pwd` 落点 |\n"
            "|---|---|---|---|---|\n"
            "| `su` | ✅ | ❌ | 还是 `/home/lijihao` | 还在原目录 |\n"
            "| **`su -`** | ✅ | ✅ **完整登录** | `/root` | `/root` |\n\n"
            "所以不带减号时，你虽然已经**是 root 了**，但 `$HOME` 还留着普通用户的值 ——"
            "打印出来的「root 主目录」是错的，而且**不会报任何错**。\n\n"
            "★ 另外两条也不行：`sudo pwd` 只是用 root 权限跑了一下 pwd，"
            "**没有切换身份**，还在原目录；`su root` 同样没带减号。\n\n"
            "**前提**：Fedora 安装时默认**不给 root 设密码**（用 sudo 代替）。"
            "真要用 `su -` 得先 `sudo passwd root` 设一个。"),
        tags=["su", "环境变量", "$HOME", "实验 2"], difficulty=3,
    ))

    add(fill(
        "把目录列表重定向到文件并带行号查看",
        "把 `/usr/local` 下的文件列表输出重定向到家目录的 `test1.txt`，"
        "然后用 `cat` 查看并**显示行号**。写出这两条命令（用 `&&` 或 `;` 连起来）。",
        ["ls /usr/local > ~/test1.txt && cat -n ~/test1.txt",
         "ls /usr/local > ~/test1.txt; cat -n ~/test1.txt",
         "ls /usr/local > /home/lijihao/test1.txt && cat -n /home/lijihao/test1.txt",
         "ls /usr/local > ~/test1.txt && cat -n /home/lijihao/test1.txt"],
        subject=SUBJ, section=sec2, difficulty=3, total_score=12,
        explanation=(
            "```bash\n"
            "ls /usr/local > ~/test1.txt      # 覆盖重定向（会先清空原文件）\n"
            "cat -n ~/test1.txt               # -n 显示行号\n"
            "```\n\n"
            "★ 三个要点：\n\n"
            "**1. `>` 是覆盖，`>>` 是追加。** 用错 `>` 会把文件原有内容清空。\n"
            "（`>` 在命令执行**之前**就把文件截断了 —— 所以\n"
            "`cat a.txt > a.txt` 会得到**空文件**，因为 a.txt 先被清零了。）\n\n"
            "**2. `cat -n` 是「加行号输出」，不是「统计行数」。** 数行数用 `wc -l`。\n\n"
            "**3. 怎么验证自己做对了**：`cat -n` 输出的总行数应当等于"
            "`ls /usr/local | wc -l`，两个数对得上就没错。"),
        tags=["重定向", "cat", "wc", "实验 2"], hint="提示：一个重定向符号 + cat 的加行号选项。",
    ))

    add(fill(
        "仅列出 /etc 下名字含 pass 的文件",
        "切换到 `/etc` 目录后，**仅显示名字里包含字符串 `pass` 的文件**。写出命令。",
        ["ls -d *pass*", "cd /etc && ls -d *pass*", "ls /etc | grep pass",
         "find /etc -maxdepth 1 -name '*pass*'", "ls -d /etc/*pass*"],
        subject=SUBJ, section=sec2, difficulty=3, total_score=12,
        explanation=(
            "**`ls -d *pass*`**（先 `cd /etc`）。\n\n"
            "两个部分各管一摊：\n"
            "- **`*pass*`** 是 shell 的通配符，匹配「名字里任意位置含 pass」→ `passwd`、`passwd-`\n"
            "- **`-d`** 让 ls「只报匹配项本身」—— 万一匹配到目录，不会把里面的内容也列出来\n\n"
            "三条等价写法（实验报告里可以一并截图）：\n"
            "```bash\n"
            "ls -d *pass*                     # 当前就在 /etc 里\n"
            "ls /etc | grep pass              # 管道给 grep 过滤\n"
            "find /etc -maxdepth 1 -name '*pass*'   # 最通用\n"
            "```\n\n"
            "★ **为什么要先 `cd /etc`**：`*pass*` 是**相对于当前目录**展开的。"
            "人在 `/home` 里敲 `ls -d *pass*`，展开的是 `/home` 下的匹配项 —— "
            "结果会是「没有那个文件」或者列错东西。"),
        tags=["ls", "-d", "通配符", "实验 2"], hint="提示：通配符匹配名字里含 pass，再加一个「别展开目录」的选项。",
    ))

    # ---------- 实验 3 ----------
    add(mc(
        "把目录复制到 /usr 需要什么",
        "把 `/tmp/a1`（含多级子目录）复制到 `/usr` 下。普通的 `cp /tmp/a1 /usr/` 会失败。"
        "下面哪条**能成功**？",
        ["cp -r /tmp/a1 /usr/", "sudo cp /tmp/a1 /usr/",
         "sudo cp -r /tmp/a1 /usr/", "cp -a /tmp/a1 /usr/"],
        "C",
        subject=SUBJ, section=sec3,
        explanation=(
            "**`sudo cp -r /tmp/a1 /usr/`** —— 两个条件**缺一不可**。\n\n"
            "这道题的坑在于：**两个错误信息完全不同，得两个都补上**。\n\n"
            "| 少写了什么 | 报错 | 症状 |\n"
            "|---|---|---|\n"
            "| 少 `-r` | `cp: -r not specified; omitting directory '/tmp/a1'` | "
            "⚠️ **不报错退出，只打一句警告**，什么都没复制 |\n"
            "| 少 `sudo` | `cp: cannot create directory '/usr/a1': Permission denied` | "
            "`/usr` 是系统目录，普通用户**只读** |\n\n"
            "★ 题目原文**没提 `sudo`** —— 但在 Fedora 上不加必然失败。"
            "「我知道要提权」这件事写进实验报告是加分项。\n\n"
            "（`cp -a` 也能替换 `-r`，但同样要加 `sudo`。）"),
        tags=["cp", "sudo", "权限", "实验 3"], difficulty=3,
    ))

    add(mc(
        "vi 里把内容存下来并退出",
        "用 `vi ~/hello` 打开一个文件，按 `i` 输入了内容之后，"
        "**要保存并退出**，接下来敲什么？",
        ["Esc 然后 :q!", "Esc 然后 :wq", "直接 :wq", "Ctrl+S 然后 Ctrl+Q"],
        "B",
        subject=SUBJ, section=sec3,
        explanation=(
            "**先 `Esc` 回到命令模式，再敲 `:wq` 回车。**\n\n"
            "vi / vim 是**模式编辑器**，这是它和记事本最大的区别：\n\n"
            "| 键 | 作用 |\n"
            "|---|---|\n"
            "| `i` | 进入**插入模式**，开始打字（左下角出现 `-- INSERT --`） |\n"
            "| **`Esc`** | 退回**命令模式**（`-- INSERT --` 消失） |\n"
            "| `:wq` | **w**rite + **q**uit，保存并退出 |\n"
            "| `:q!` | 不保存**强制**退出（改错了想重来用这个） |\n"
            "| `:w` | 只保存，继续编辑 |\n\n"
            "★ 为什么不能直接敲 `:wq`：在插入模式下，`:` 就是个**普通字符**，"
            "会被打进文件内容里 —— 结果文件里多出一行 `:wq`。\n\n"
            "截图验证：存完回到终端敲 `cat ~/hello`，看到内容就对了。"),
        tags=["vi", "vim", "编辑器", "实验 3"], difficulty=2,
    ))

    add(mc(
        "mv 到底是「改名」还是「移进去」",
        "`mv /test7 /test8` 和 `mv /test7 /tmp/` 这两条命令分别做了什么？",
        ["两条都是改名",
         "前者把 /test7 移进 /test8 目录，后者改名成 tmp",
         "前者改名为 /test8，后者移进 /tmp 目录",
         "两条都是移动"],
        "C",
        subject=SUBJ, section=sec3,
        explanation=(
            "**`mv` 的语义只有一句话：目标位置不存在就「改名」，存在且是目录就「移进去」。**\n\n"
            "| 命令 | `/test8`、`/tmp` 的状态 | 结果 |\n"
            "|---|---|---|\n"
            "| `mv /test7 /test8` | `/test8` **不存在** | 改名为 `/test8` ✅ |\n"
            "| `mv /test7 /tmp/` | `/tmp` **是已存在的目录** | 移成 `/tmp/test7` ✅ |\n\n"
            "★ 所以想**改名**时，目标路径必须指向一个**不存在**的名字。\n"
            "手滑写成 `mv /test7 /tmp/` 想改名 —— 结果只是搬进去了，名字没变。\n\n"
            "**配套的两个坑**：\n"
            "1. `/`、`/usr/local` 都是系统目录，**每一步都要 `sudo`**\n"
            "2. 一次搬多个文件时，**最后一个参数必须是目录**（带 `/`），"
            "否则报 `target 'xxx' is not a directory`"),
        tags=["mv", "改名", "移动", "实验 3"], difficulty=3,
    ))

    add(fill(
        "把 /boot 下 vmlinuz 开头的文件拷到家目录",
        "把 `/boot` 下所有以 `vmlinuz` 开头的文件，拷贝到 `~/abc` 目录下"
        "（`abc` 不存在就先建）。写出这一串命令（用 `&&` 或 `;` 连起来）。",
        ["mkdir -p ~/abc && sudo cp /boot/vmlinuz* ~/abc/",
         "mkdir -p ~/abc; sudo cp /boot/vmlinuz* ~/abc/",
         "mkdir -p ~/abc && cp /boot/vmlinuz* ~/abc/",
         "mkdir -p ~/abc; cp /boot/vmlinuz* ~/abc/",
         "mkdir -p /home/lijihao/abc && sudo cp /boot/vmlinuz* /home/lijihao/abc/"],
        subject=SUBJ, section=sec3, difficulty=4, total_score=15,
        explanation=(
            "```bash\n"
            "ls /boot/vmlinuz*          # ★ 先自证：这些文件真的存在\n"
            "mkdir -p ~/abc             # -p：已存在也不报错\n"
            "sudo cp /boot/vmlinuz* ~/abc/\n"
            "```\n\n"
            "★ 三个要点：\n\n"
            "**1. `mkdir -p` 而不是裸 `mkdir`** —— 目录已存在时裸 `mkdir` 会报错，"
            "`-p` 幂等，脚本里更稳。\n\n"
            "**2. 通配符先自证** —— 万一 `/boot` 下没有 `vmlinuz*`，shell 会把它"
            "**原样传给 cp**，报 `cp: cannot stat '/boot/vmlinuz*': No such file or directory`。"
            "看到这个错就知道是「根本没匹配上」，不是权限问题。\n\n"
            "**3. `cp` 支持一次拷多个** —— `*` 展开成若干文件名，通通扔进 `~/abc/`。"
            "（`/boot/vmlinuz-*` 通常是 `-rw-r--r--` 人人可读，普通用户其实也能拷；"
            "加 `sudo` 是求稳。）"),
        tags=["cp", "通配符", "mkdir", "实验 3"], hint="提示：先建目录（用幂等的那版），再用通配符一次拷多个。",
    ))

    add(tf(
        "ll 在脚本里也能用吗",
        "`ll` 是 `ls -l` 的**别名**，所以写在 `.sh` 脚本里也能正常执行。",
        False,
        subject=SUBJ, section=sec3,
        explanation=(
            "**错**。`ll` **只在交互式 shell 里有效**。\n\n"
            "查明真相的三条命令：\n"
            "```bash\n"
            "alias ll            # alias ll='ls -l'\n"
            "type ll             # ll 是 `ls -l` 的别名\n"
            "command -v ll       # 无输出 —— 系统里根本没有 ll 这个可执行文件\n"
            "```\n\n"
            "它是 Fedora 的 `/etc/profile.d/` 下的脚本在**每次启动交互式 shell 时**定义的。\n\n"
            "**什么时候会失效**：\n"
            "- 写在 `.sh` 脚本里 → `ll: command not found`\n"
            "- `sudo ll` → 同样报错（`sudo` 走自己那套，不认别名）\n"
            "- 放进 cron 定时任务 → 同样不行（非交互式环境）\n\n"
            "★ 那种场合请用**真命令 `ls -l`**。\n\n"
            "顺带：`alias` 定义的东西**可以覆盖真命令** —— 如果哪天发现"
            "`ls` 行为怪怪的，先 `type ls` 看一眼是不是被别名改了。"),
        tags=["alias", "ll", "交互式", "实验 3"], difficulty=3,
    ))

    # ---------- 实验 4 ----------
    add(mc(
        "tar 打包时那句 Removing leading / 警告",
        "执行 `sudo tar czvf ~/test5.tar.gz /usr/test5` 时，屏幕上出现：\n\n"
        "```\n"
        "tar: Removing leading `/' from member names\n"
        "```\n\n"
        "这说明什么？",
        ["压缩失败了，要重来", "只是警告，压缩正常完成，包内路径是相对路径",
         "要加 -P 选项才能去掉这个警告", "说明 /usr/test5 不存在"],
        "B",
        subject=SUBJ, section=sec4,
        explanation=(
            "**这是 tar 的正常行为，不是错误** —— 压缩会正常完成。\n\n"
            "tar 会把成员名开头的 `/` **去掉**，也就是包内存的是 `usr/test5/...` "
            "而不是 `/usr/test5/...`。\n\n"
            "**为什么要这么做**：防止你解压时把文件**直接覆盖回绝对路径**。\n"
            "想想看，如果包内记的是绝对路径，在别的机器上 `tar xf` 就可能"
            "直接改写对方系统的 `/usr` —— 这是很危险的行为。\n\n"
            "**怎么验证**：解压前后各看一眼，或者直接列包内路径：\n"
            "```bash\n"
            "tar tzf ~/test5.tar.gz | head -3\n"
            "# usr/test5/\n"
            "# usr/test5/xxx\n"
            "```\n"
            "★ 所以**解压位置由 `-C` 决定**，包内路径是相对的。\n\n"
            "（真想带绝对路径得显式加 `-P`，但**几乎不该这么做**。）"),
        tags=["tar", "警告", "绝对路径", "实验 4"], difficulty=3,
    ))

    add(mc(
        "ln -s 的两个参数谁在前",
        "要在根目录建一个名为 `myshare` 的符号链接，指向 `/usr/local/sdutshare`。"
        "正确的命令是？",
        ["ln -s /myshare /usr/local/sdutshare",
         "ln -s /usr/local/sdutshare /myshare",
         "ln /usr/local/sdutshare /myshare",
         "ln -s myshare /usr/local/sdutshare"],
        "B",
        subject=SUBJ, section=sec4,
        explanation=(
            "**`ln -s 真实目标 链接名`** —— 顺序是「**先目标，后链接名**」。\n\n"
            "记法：跟 `cp 源 目标` 一个方向，`-s` 只是声明「建的是软链接」。\n\n"
            "★ **顺序写反的后果很严重**：\n"
            "```bash\n"
            "ln -s /myshare /usr/local/sdutshare\n"
            "```\n"
            "这会建出一个**指向自己的死循环链接**（`/usr/local/sdutshare` 指向 `/myshare`，"
            "而 `/myshare` 又指向它）。\n\n"
            "**怎么一眼认出符号链接**：`ls -l` 输出**第一个字符是 `l`**：\n"
            "```\n"
            "lrwxrwxrwx. 1 root root 20 10月 12 08:0x myshare -> /usr/local/sdutshare\n"
            "```\n"
            "（普通文件是 `-`、目录是 `d`。）\n\n"
            "另外两条错在：`ln` 不带 `-s` 建的是**硬链接**（不能指向目录、也不能跨文件系统）；"
            "第四条把链接名写成了目标。"),
        tags=["ln", "-s", "符号链接", "实验 4"], difficulty=3,
    ))

    add(fill(
        "按字典逆序排序文件内容",
        "`~/mysort1` 里有四行：`is` / `this` / `excellent` / `my`。"
        "把它按**字典逆序**排序显示。写出这条命令。",
        ["sort -r ~/mysort1", "sort -r /home/lijihao/mysort1"],
        subject=SUBJ, section=sec4, difficulty=2, total_score=10,
        explanation=(
            "**`sort -r ~/mysort1`**（`-r` = reverse）。\n\n"
            "输出：\n"
            "```\n"
            "this\n"
            "my\n"
            "is\n"
            "excellent\n"
            "```\n\n"
            "对照（默认是字典**升序**，也就是 `-r` 的倒过来）：\n"
            "```\n"
            "excellent\n"
            "is\n"
            "my\n"
            "this\n"
            "```\n\n"
            "★ 两个容易混的选项：\n"
            "- `sort -n` 是**按数值**排（`2` 排在 `10` 前面）—— 这题是纯字符串，用不上\n"
            "- `sort -k2` 是**按第 2 列**排\n\n"
            "注意字典序是**逐字符比 ASCII 码**，所以**大写字母全部排在小写字母前面**"
            "（`Z` = 90 < `a` = 97）。混大小写时 `sort` 的结果可能和直觉不一样。\n\n"
            "（`sort` **不改原文件**，只往屏幕输出。要写回用 `sort -r f > f.sorted`。）"),
        tags=["sort", "-r", "排序", "实验 4"], hint="提示：sort 加一个表示「反过来」的选项。",
    ))

    add(fill(
        "输出字符串但不换行",
        "用 `echo` 输出字符串 `hello everyone!`，要求**输出后不换行**。写出命令。",
        ["echo -n \"hello everyone!\"", "echo -n hello everyone!",
         "printf \"hello everyone!\"", "echo -e \"hello everyone!\\c\""],
        subject=SUBJ, section=sec4, difficulty=2, total_score=10,
        explanation=(
            "**`echo -n \"hello everyone!\"`**（`-n` = no newline）。\n\n"
            "三种写法都能做到：\n"
            "```bash\n"
            "echo -n \"hello everyone!\"        # -n：结尾不加换行\n"
            "echo -e \"hello everyone!\\c\"      # \\c：到此为止\n"
            "printf \"hello everyone!\"         # printf 默认就不加换行（最标准）\n"
            "```\n\n"
            "★ **怎么自证「真的没换行」**（截图时这样截最有说服力）：\n"
            "```bash\n"
            "echo -n \"hello everyone!\"; echo \"|\"\n"
            "# hello everyone!|\n"
            "#                ↑ 竖线紧贴着感叹号\n"
            "\n"
            "echo \"hello everyone!\"; echo \"|\"      # 对照组\n"
            "# hello everyone!\n"
            "# |\n"
            "# ↑ 竖线跑到下一行了\n"
            "```\n\n"
            "顺带：内容里有空格**建议用引号括起来**。不括的话 `this is a` 会被拆成三个参数"
            "交给 echo —— 打印结果看着一样，但一旦内容里有 `*`、`>` 就会出事。"),
        tags=["echo", "-n", "printf", "实验 4"], hint="提示：echo 有个选项专门管「结尾不加换行」。",
    ))

    add(mc(
        "man 手册的章节号",
        "`man grep` 打开的是第 1 章。那么 **`/etc/passwd` 这种配置文件的说明**"
        "在第几章？",
        ["第 1 章", "第 5 章", "第 8 章", "第 9 章"],
        "B",
        subject=SUBJ, section=sec4,
        explanation=(
            "**第 5 章（文件格式与约定）** —— `man 5 passwd`。\n\n"
            "man 一共分 9 章，常用的四章：\n\n"
            "| 章 | 内容 | 例子 |\n"
            "|---|---|---|\n"
            "| **1** | 用户命令 | `man 1 grep` |\n"
            "| **2** | 系统调用 | `man 2 open` |\n"
            "| **3** | 库函数 | `man 3 printf` |\n"
            "| **5** | **配置文件格式** | `man 5 passwd`、`man 5 fstab` |\n"
            "| **8** | **系统管理命令**（多数要 root） | `man 8 mount` |\n\n"
            "★ **同名不同章**很常见：`passwd` 既是个命令（第 1 章）"
            "又是个文件（第 5 章）。直接 `man passwd` 默认给**章号最小**的那个 —— "
            "想看文件格式就必须写明 `man 5 passwd`。\n\n"
            "两个配套技巧：\n"
            "- **`man -k 关键词`**（≈ `apropos`）搜「哪些手册页提到它」\n"
            "- **`grep --help`** 比 man 短，快速看选项"),
        tags=["man", "章节", "文档", "实验 4"], difficulty=3,
    ))

    add(mc(
        "在终端启动当前目录下的程序",
        "你把 Eclipse 解压到 `~/eclipse`，用 `cd ~/eclipse` 进去了。"
        "想启动里面的 `eclipse` 可执行文件，怎么写？",
        ["eclipse", "./eclipse", "/eclipse", "sudo eclipse"],
        "B",
        subject=SUBJ, section=sec4,
        explanation=(
            "**`./eclipse`** —— `./` 不能省。\n\n"
            "**为什么**：出于安全，Linux 的 shell **默认不搜索当前目录**"
            "（`PATH` 里**没有** `.`）。\n\n"
            "这个设计是有道理的：如果当前目录会被自动搜索，"
            "那么你 `cd` 进一个从网上下载的目录、敲了个 `ls`，"
            "就可能执行了攻击者放的同名恶意程序。\n\n"
            "**报错长这样**：\n"
            "```\n"
            "eclipse: command not found\n"
            "```\n"
            "★ 看到 `command not found`，先想两件事：\n"
            "1. 这个程序**真的装了吗** → `dnf provides '*/eclipse'` 反查属于哪个包\n"
            "2. 是不是**就在当前目录**、但漏了 `./`\n\n"
            "另外两条：写 `/eclipse` 是在找**根目录下**的 eclipse（不存在）；"
            "`sudo eclipse` 同样过不了「不搜当前目录」这一关。\n\n"
            "顺带：解压时**别下错平台**，`linux-gtk-x86_64` 才是 Linux 版；"
            "首次启动要解压插件，等一两分钟是正常的。"),
        tags=["PATH", "./", "可执行文件", "实验 4"], difficulty=3,
    ))

    add(mc(
        "装 MySQL 到底装哪个包",
        "实验要求「用 `dnf` 安装 mysql，然后启动它」。\n\n"
        "如果你直接敲 `sudo dnf install mysql`，装完之后 "
        "`sudo systemctl start mysqld` 会报 `Unit mysqld.service not found.`。为什么？",
        ["服务名写错了，应该是 mysql.service",
         "mysql 是客户端包，服务端在 mysql-server 里",
         "要先 systemctl daemon-reload",
         "MariaDB 把端口占了，得先停掉它"],
        "B",
        subject=SUBJ, section=sec4,
        explanation=(
            "**Fedora 44 仓库里 `mysql` 和 `mysql-server` 是两个不同的包。**\n\n"
            "| 包名 | 内容 |\n"
            "|---|---|\n"
            "| `mysql` | **只有客户端**（`mysql` 命令 + 共享库），**没有服务端** |\n"
            "| `mysql-server` | **服务端**（`mysqld`、`mysqladmin`、systemd 服务单元） |\n\n"
            "装了客户端当然没有 `mysqld.service` —— 所以正确做法是装 **`mysql-server`**"
            "（它会自动把客户端也带上）。\n\n"
            "完整流程：\n"
            "```bash\n"
            "sudo dnf install -y mysql-server\n"
            "sudo systemctl start mysqld\n"
            "sudo grep 'temporary password' /var/log/mysqld.log   # 取初始 root 临时密码\n"
            "mysql -u root -p                                      # 粘进去\n"
            "```\n"
            "进去之后题目要的是：`show databases;`（能看到 `information_schema`、`mysql`、"
            "`performance_schema`、`sys` 四个库），然后 `exit;`。\n\n"
            "★ **另外三条**（真踩到时看）：\n"
            "- MySQL 与 MariaDB **冲突**（提供同名文件），一台机器只能装一个\n"
            "- 日志里找不到临时密码 → 可能是空密码初始化，直接 `sudo mysql -u root` 进去后马上改密码\n"
            "- 服务起不来先 `journalctl -u mysqld -n 50`，**别顺手 `setenforce 0`**"),
        tags=["dnf", "mysql", "服务", "实验 4"], difficulty=4,
    ))

    add(fill(
        "把两个文件的内容拼进第三个文件",
        "`file11` 内容为 `sdut11`、`file12` 内容为 `sdut12`，"
        "`dir1` 目录已建好。把两者的内容依次写进 `dir1/file13`。写出命令。",
        ["cat file11 file12 > dir1/file13", "cat ~/file11 ~/file12 > ~/dir1/file13",
         "cat file11 file12 > ~/dir1/file13"],
        subject=SUBJ, section=sec4, difficulty=3, total_score=12,
        explanation=(
            "**`cat file11 file12 > dir1/file13`**。\n\n"
            "`cat` 接**多个文件**时，会**按顺序**把所有内容连起来输出到标准输出；"
            "`>` 再把它写进新文件。结果 `file13` 是两行：\n"
            "```\n"
            "sdut11\n"
            "sdut12\n"
            "```\n\n"
            "★ **最容易踩的坑**：输出文件**不能是输入文件之一**。\n"
            "```bash\n"
            "cat file11 file12 > file11     # ❌ file11 先被清空，结果只剩 file12 的内容\n"
            "```\n"
            "因为 `>` 是在命令**执行之前**就把目标文件截断成 0 字节的 —— "
            "cat 去读 file11 时它已经空了。\n\n"
            "**另外两个配套操作**（实验题 (d) 问的那个）：\n"
            "```bash\n"
            "mv file11 file12 dir1/     # ★ 一次搬多个，最后一个参数必须是目录\n"
            "ls -l ~/dir1               # 应该看到 file11 file12 file13\n"
            "```\n"
            "`mv` 一次搬多个时如果最后一个是文件名，会报 `target 'dir1' is not a directory`。"),
        tags=["cat", "重定向", "mv", "实验 4"], hint="提示：cat 可以接多个文件，最后用重定向写进新文件。",
    ))

    add(fill(
        "反查一个命令属于哪个包",
        "你在 Fedora 上敲某个命令，报 `command not found`。"
        "想查「这个命令由哪个软件包提供」，用 `dnf` 的哪个子命令？"
        "（写出完整命令，命令名用 `ls` 举例即可）",
        ["dnf provides '*/ls'", "dnf provides ls", "dnf provides */ls",
         "dnf provides '*/ls' -q"],
        subject=SUBJ, section=sec4, difficulty=4, total_score=12,
        explanation=(
            "**`dnf provides '*/ls'`**（拿 `ls` 举例）。\n\n"
            "`command not found` 之后想「它到底属于哪个包」，这条是最靠谱的路 —— "
            "因为它查的是**真实的文件归属关系**，不是猜。\n\n"
            "★ **为什么要写 `*/命令名` 这种带通配符的样子**：\n"
            "- `dnf provides ls` 会匹配**所有**名字里带 `ls` 的包"
            "（`alsa`、`lsblk` 一大堆噪音）\n"
            "- `dnf provides '*/ls'` 精确表示「**某个路径下名为 ls 的文件**」\n"
            "- 通配符**必须用单引号包起来**，否则 shell 会抢先展开它\n\n"
            "**为什么这条特别值得记**：本机实测过，很多时候**站内搜不到某工具**"
            "并不等于它不存在 —— 用 `dnf provides` 查文件归属才是权威答案。\n\n"
            "配套命令：\n"
            "```bash\n"
            "rpm -qf /usr/bin/ls          # 反过来：这个文件属于哪个已装的包\n"
            "dnf search 关键词            # 按描述搜包\n"
            "dnf repoquery -l 包名        # 看这个包里都有哪些文件\n"
            "```"),
        tags=["dnf", "provides", "排错", "实验 4"],
        hint="提示：dnf 的一个子命令，查「文件属于哪个包」；命令名前要加通配符路径。",
    ))


# ===================================================================== #
#  六、第 01 ~ 05 讲讲义概念题
# --------------------------------------------------------------------- #
#  全部从各讲的「附录 A · 陷阱清单」和正文里抽 —— 那些是我已经核过
#  （查过官方手册 / 在本机 Fedora 44 上真跑过）的结论，不是凭印象写的。
# ===================================================================== #
def part_lectures_a() -> None:
    # ---------- 第 01 讲 ----------
    s1 = "第 01 讲 · Linux 概述"

    add(mc(
        "你敲一条命令，中间经过了什么",
        "在终端敲下 `ls` 并回车，从你按下回车到看见输出，中间的顺序是？",
        ["内核 → Shell → ls 程序 → 终端",
         "Shell 解析并找到 ls → 内核 fork/exec → ls 运行 → 结果回终端",
         "ls 程序 → 内核 → Shell → 终端",
         "终端直接调用内核，Shell 只是显示界面"],
        "B",
        subject=SUBJ, section=s1,
        explanation=(
            "正确链路：\n"
            "```\n"
            "你敲 ls\n"
            "  → Shell(bash) 解析这行文字，去 PATH 里找到 /usr/bin/ls\n"
            "  → 调用内核的系统调用 fork() + execve()\n"
            "  → 内核调度 CPU 执行 ls 程序\n"
            "  → ls 通过内核读目录内容\n"
            "  → 结果返回 Shell → 打印到终端\n"
            "```\n\n"
            "★ **Shell 只是个普通程序**（跑在用户态），本身也能换"
            "（bash / zsh / fish）。它不干实事，只负责「解析 + 派活」。\n\n"
            "真正干活的是**内核**：进程调度、内存管理、设备驱动、网络，全在它手里。"
            "任何程序想碰硬件，都得**经过内核的系统调用**。"),
        tags=["体系结构", "shell", "内核", "第 01 讲"], difficulty=2,
    ))

    add(mc(
        "Linux 的分层结构，Shell 在哪一层",
        "教材把 Linux 系统从下往上分成四层。**Shell 位于哪一层**？",
        ["第 1 层，和内核并列", "第 2 层，和文件系统同层",
         "第 3 层，在文件系统之上、应用程序之下", "第 4 层，就是应用程序"],
        "C",
        subject=SUBJ, section=s1,
        explanation=(
            "四层结构（从下往上）：\n"
            "```\n"
            "4. 应用程序        浏览器 / 编辑器 / 你自己的程序\n"
            "3. Shell（命令解释器）  bash —— 你和内核之间的翻译\n"
            "2. 文件系统 + 用户界面   ext4 / btrfs；GNOME 桌面\n"
            "1. 内核 kernel      进程 / 内存 / 驱动 / 网络\n"
            "   ───────────────\n"
            "   硬件             CPU / 内存 / 磁盘 / 网卡\n"
            "```\n\n"
            "Shell 在第 3 层，位置很关键：**它夹在「用户敲的东西」和「内核提供的服务」之间**。"
            "往上，它把命令翻译给内核；往下，它把内核的返回组织成你能看的形式。\n\n"
            "★ 记住这个位置，就能回答「为什么换个 shell 不影响系统」—— "
            "因为它只是上面的一层皮，内核和文件系统都没动。"),
        tags=["体系结构", "shell", "第 01 讲"], difficulty=2,
    ))

    add(mc(
        "哪个目录放配置文件",
        "Linux 的**所有系统配置文件**（比如 `passwd`、`fstab`、`sshd_config`）"
        "统一放在哪个目录下？",
        ["/bin", "/etc", "/var", "/lib"],
        "B",
        subject=SUBJ, section=s1,
        explanation=(
            "**`/etc`** —— 系统配置文件的集中地，记不住别的也得记住它。\n\n"
            "根目录下主要目录的职责：\n\n"
            "| 目录 | 装什么 |\n"
            "|---|---|\n"
            "| `/bin`、`/usr/bin` | 普通用户能用的命令（ls、cp……） |\n"
            "| `/sbin`、`/usr/sbin` | 管理员命令（fdisk、iptables……） |\n"
            "| **`/etc`** | **所有配置文件** |\n"
            "| `/home` | 普通用户的家目录 |\n"
            "| `/root` | root 的家目录（**不在 /home 下**） |\n"
            "| `/dev` | 设备文件（硬盘 sda、终端 tty……） |\n"
            "| `/proc` | 内存里的内核状态（虚拟文件系统，不占磁盘） |\n"
            "| `/var` | 变化的数据：日志、邮件、数据库 |\n"
            "| `/tmp` | 临时文件，重启可能清空 |\n\n"
            "★ 实验里凡是「改配置文件」的步骤，八成都在 `/etc` 下（"
            "`/etc/vsftpd/`、`/etc/httpd/`、`/etc/named.conf`……）。"),
        tags=["目录结构", "/etc", "第 01 讲"], difficulty=1,
    ))

    add(tf(
        "root 的家目录在哪",
        "root 用户的家目录是 `/home/root`，和其他普通用户放在一起。",
        False,
        subject=SUBJ, section=s1,
        explanation=(
            "**错**。root 的家目录是 **`/root`** —— 直接挂在根目录下，**不在 `/home` 里**。\n\n"
            "为什么要分开：`/home` 在有些系统上会**单独挂一块盘**"
            "（或者被网络文件系统挂载）。如果 root 的家目录也在 `/home` 里，"
            "一旦那块盘出问题挂不上，root 就**没有家目录可落脚**了，"
            "连救援都难做。\n\n"
            "验证（实验 2 第 10 题正是考这个）：\n"
            "```bash\n"
            "su -              # ★ 必须带减号，才会换 $HOME\n"
            "echo $HOME        # /root\n"
            "pwd               # /root\n"
            "```"),
        tags=["目录结构", "/root", "第 01 讲"], difficulty=2,
    ))

    add(mc(
        "Linux 的文件系统是几棵树",
        "和 Windows 的 C: / D: / E: 相比，Linux 的文件系统结构特点是？",
        ["也是多个并列的盘符", "单根倒树，一切都在 / 之下",
         "按设备分树，每块盘一棵", "没有固定结构，看发行版"],
        "B",
        subject=SUBJ, section=s1,
        explanation=(
            "**单根倒树** —— 只有一个根 `/`，所有东西都挂在它下面。\n\n"
            "| | Windows | Linux |\n"
            "|---|---|---|\n"
            "| 顶层 | `C:` `D:` `E:` **多个并列** | `/` **只有一个** |\n"
            "| 新设备 | 自动分配一个盘符 | 必须**挂载**到某个目录下才能访问 |\n\n"
            "「挂载」的意思是：把一块盘（或一个分区、一个 U 盘）"
            "**接到现有目录树的某个位置**上。比如把 U 盘挂到 `/mnt/usb`，"
            "之后 `cd /mnt/usb` 就是进 U 盘。\n\n"
            "验证：`lsblk` 看块设备，`findmnt` 看谁挂在哪。"
            "在 `/etc/fstab` 里就能看到开机自动挂载的配置。"),
        tags=["文件系统", "根目录", "挂载", "第 01 讲"], difficulty=2,
    ))

    # ---------- 第 03 讲 ----------
    s3 = "第 03 讲 · X Window 的使用"

    add(mc(
        "X Window 是什么角色",
        "在 Linux 桌面里，**X Window 系统**负责的是哪一层？",
        ["它就是 GNOME 桌面本身", "底层显示服务：管画面输出、键盘鼠标输入",
         "管文件管理的那部分", "管软件安装的那部分"],
        "B",
        subject=SUBJ, section=s3,
        explanation=(
            "**X Window 是最底层的显示服务**（`X Server` / Wayland 同层），"
            "负责：\n"
            "- 把画面**画到屏幕上**\n"
            "- 接收**键盘、鼠标**的输入并分发\n"
            "- 管理窗口的绘制区域\n\n"
            "而 **GNOME 是「桌面环境」** —— 它在 X 之上，"
            "提供任务栏、活动概览、文件管理器、设置面板等一整套东西。\n\n"
            "分层关系：\n"
            "```\n"
            "GNOME 桌面环境（任务栏、文件管理器、设置面板…）\n"
            "        ↓ 依赖\n"
            "X Window / Wayland（画图 + 输入）\n"
            "        ↓ 依赖\n"
            "内核（显卡驱动、输入设备驱动）\n"
            "```\n\n"
            "★ 所以可以「换桌面环境不换 X」：同一台机器上装 KDE、XFCE，"
            "都跑在同一个 X 之上，登录时切换即可。\n\n"
            "补充：`echo $XDG_SESSION_TYPE` 能看当前用的是 X11 还是 Wayland。"),
        tags=["XWindow", "GNOME", "分层", "第 03 讲"], difficulty=3,
    ))

    add(tf(
        "自建的应用菜单项放哪里",
        "想让自建的程序出现在 GNOME 的应用程序菜单里，"
        "可以往 `~/.local/share/applications/` 放一个 `.desktop` 文件。",
        True,
        subject=SUBJ, section=s3,
        explanation=(
            "**对**。`.desktop` 文件就是应用的「菜单项定义」，有两个放的层次：\n\n"
            "| 位置 | 生效范围 |\n"
            "|---|---|\n"
            "| **`~/.local/share/applications/`** | 只对**当前用户**生效 |\n"
            "| `/usr/share/applications/` | **所有用户**（要 root 权限写） |\n\n"
            "最简模板：\n"
            "```ini\n"
            "[Desktop Entry]\n"
            "Type=Application\n"
            "Name=我的工具\n"
            "Exec=/home/lijihao/tools/run.sh\n"
            "Icon=/home/lijihao/tools/icon.png\n"
            "Terminal=false\n"
            "```\n\n"
            "★ 三个容易卡住的点：\n"
            "1. **`Exec=` 要用绝对路径**（菜单启动时的 `PATH` 和你的终端不一样）\n"
            "2. 想让它在终端里跑就写 `Terminal=true`\n"
            "3. 写完可能**要重新登录**菜单才刷新（或者 `update-desktop-database`）\n\n"
            "权限别忘：`chmod +x` 那个 `.desktop` 文件并不必需，但 `Exec=` 指向的脚本**必须**可执行。"),
        tags=["desktop", "GNOME", "应用菜单", "第 03 讲"], difficulty=3,
    ))

    # ---------- 第 04 讲 ----------
    s4 = "第 04 讲 · 常用软件"

    add(mc(
        "LibreOffice 的三个主力组件",
        "LibreOffice 里，**文档、表格、演示**分别对应哪三个组件？",
        ["Writer / Calc / Impress", "Word / Excel / PowerPoint",
         "Docs / Sheets / Slides", "Text / Grid / Show"],
        "A",
        subject=SUBJ, section=s4,
        explanation=(
            "**Writer（文档）/ Calc（表格）/ Impress（演示）**。\n\n"
            "和 MS Office 的对应关系：\n\n"
            "| LibreOffice | MS Office | 用途 | 文件格式 |\n"
            "|---|---|---|---|\n"
            "| **Writer** | Word | 文字文档 | `.odt` / `.docx` |\n"
            "| **Calc** | Excel | 电子表格 | `.ods` / `.xlsx` |\n"
            "| **Impress** | PowerPoint | 演示文稿 | `.odp` / `.pptx` |\n"
            "| Base | Access | 数据库 | `.odb` |\n"
            "| Draw | Visio | 矢量绘图 | `.odg` |\n\n"
            "★ B 选项 `Word/Excel/PowerPoint` 是**微软**的，C 选项是 **Google 文档**的 —— "
            "别混。\n\n"
            "补充：LibreOffice 默认存 ODF 格式（`.odt` 等开放标准），"
            "存 Office 格式要去「另存为」里选，或者改默认格式设置。\n"
            "（第 04 讲有专门讲怎么办文档兼容。）"),
        tags=["LibreOffice", "办公软件", "第 04 讲"], difficulty=2,
    ))

    add(tf(
        "Flatpak 装的软件能在 dnf 里看到吗",
        "用 Flatpak 安装的软件，可以用 `dnf list installed` 查到。",
        False,
        subject=SUBJ, section=s4,
        explanation=(
            "**错**。Flatpak 和 RPM（dnf）是**两套完全独立的软件体系**。\n\n"
            "| | RPM / dnf | Flatpak |\n"
            "|---|---|---|\n"
            "| 来源 | Fedora 官方仓库 | Flathub 等 |\n"
            "| 查询 | `dnf list installed`、`rpm -qa` | **`flatpak list`** |\n"
            "| 安装 | `sudo dnf install xxx` | `flatpak install xxx` |\n"
            "| 沙箱 | 无（能访问全系统） | **有沙箱**，权限要单独授予 |\n"
            "| 依赖 | 系统共享库 | **自带运行时**（所以体积大） |\n\n"
            "★ 所以「装完 `dnf list installed` 里找不到」**不是没装上** —— "
            "换 `flatpak list` 查就看到了。\n\n"
            "反过来说，用 dnf 装的软件也不会出现在 `flatpak list` 里。"
            "两套包管理器各管各的，互不知情。"),
        tags=["Flatpak", "dnf", "包管理", "第 04 讲"], difficulty=3,
    ))

    # ---------- 第 05 讲 ----------
    s5 = "第 05 讲 · 硬件与软件安装"

    add(mc(
        "装本地 rpm 包的正确姿势",
        "你下载了一个 `x.rpm` 到当前目录，它**有一堆依赖**需要一并装上。"
        "推荐用哪条命令？",
        ["rpm -ivh x.rpm", "sudo rpm -ivh x.rpm",
         "sudo dnf install ./x.rpm", "sudo dnf localinstall ./x.rpm"],
        "C",
        subject=SUBJ, section=s5,
        explanation=(
            "**`sudo dnf install ./x.rpm`** —— 让 dnf 经手，它会**自动把依赖装齐**。\n\n"
            "为什么不用 `rpm -ivh`：`rpm` **不管依赖**。缺了谁就直接报错退出，"
            "然后你就得手工一个个 `dnf install` 补 —— 这叫「**依赖地狱**」，"
            "补到第 5 个依赖又缺别的依赖时最崩溃。\n\n"
            "★ **两个 DNF5 的坑**（Fedora 41+ 改的）：\n"
            "- `dnf localinstall ./x.rpm` —— **这个子命令已被移除**，会报错\n"
            "- 直接 `dnf install ./x.rpm` 就对了（**路径里的 `./` 不能省**，"
            "不然 dnf 会当成包名去仓库里找）\n\n"
            "真要用 rpm 也不是不行，但只适合「确定依赖齐全」的场合：\n"
            "```bash\n"
            "sudo rpm -ivh x.rpm        # -i 安装、-v 显示过程、-h 打进度条\n"
            "rpm -qpl x.rpm             # 先看看这个包会往哪放什么文件\n"
            "```"),
        tags=["rpm", "dnf", "依赖", "第 05 讲"], difficulty=3,
    ))

    add(mc(
        "编译时提示找不到头文件，该装什么包",
        "你编译一个程序，报错 `fatal error: xxx.h: No such file or directory`。"
        "应该装哪个包？",
        ["xxx", "xxx-devel", "xxx-libs", "xxx-headers"],
        "B",
        subject=SUBJ, section=s5,
        explanation=(
            "**`xxx-devel`** —— 头文件放在 `-devel` 包里。\n\n"
            "Fedora 把每个库**拆成两个包**：\n\n"
            "| 包名 | 装什么 | 谁需要 |\n"
            "|---|---|---|\n"
            "| `xxx` | **运行时**：`.so` 共享库 | 只想**运行**用它的程序 |\n"
            "| **`xxx-devel`** | **开发用**：`.h` 头文件 + 链接用的 `.so` 符号链接 | **要编译** |\n\n"
            "★ 所以「明明装了那个库，编译还是找不到头文件」是**最常见的误解** —— "
            "你装的是运行时包，头文件压根不在里面。\n\n"
            "**一次装齐编译环境**（比一个个补依赖靠谱）：\n"
            "```bash\n"
            "sudo dnf group install development-tools     # ★ 是 dev tools，不是 build-essential\n"
            "sudo dnf builddep 包名.spec                  # 从 spec 里自动装齐全部编译依赖\n"
            "```\n"
            "（`build-essential` 是 **Ubuntu 的包名**，Fedora 上不存在。）"),
        tags=["编译", "devel", "头文件", "第 05 讲"], difficulty=3,
    ))

    add(mc(
        "DNF5 里怎么装一个软件包组",
        "在 Fedora 44（DNF5）里，想安装一个「软件包组」（比如开发工具组），"
        "正确写法是？",
        ["sudo dnf groupinstall development-tools",
         "sudo dnf group install development-tools",
         "sudo dnf install group development-tools",
         "sudo dnf install @group development-tools"],
        "B",
        subject=SUBJ, section=s5,
        explanation=(
            "**`sudo dnf group install development-tools`** —— DNF5 要求 "
            "`group` 和 `install` **分成两个词**。\n\n"
            "★ `groupinstall`（一个词）是 **DNF4 / yum 时代的写法**，"
            "DNF5 里已经**不是有效子命令**。无数网上教程还在用老写法，"
            "照抄会报 `Unknown command: groupinstall`。\n\n"
            "同理还有一对：\n"
            "| 老写法（DNF4/yum） | 新写法（DNF5） |\n"
            "|---|---|\n"
            "| `dnf groupinstall xxx` | **`dnf group install xxx`** |\n"
            "| `dnf groupremove xxx` | `dnf group remove xxx` |\n"
            "| `dnf grouplist` | `dnf group list` |\n\n"
            "★ 这类「七年换了三轮」的差异，第 05 讲整章都是 —— "
            "因为教材是 2020 年 / Fedora 30 蓝本写的，包管理变化最剧烈。\n\n"
            "查有哪些组：`dnf group list`。"),
        tags=["dnf5", "group", "版本差异", "第 05 讲"], difficulty=4,
    ))

    add(mc(
        "装完显卡驱动能不能立刻重启",
        "你 `sudo dnf install akmod-nvidia` 装完闭源显卡驱动，"
        "想立刻重启看看效果。**先做什么**更安全？",
        ["直接重启，装完就能用", "先 `modinfo -F version nvidia` 确认模块编好了",
         "先 `dnf remove` 卸掉 nouveau", "先 `setsebool` 放行显卡"],
        "B",
        subject=SUBJ, section=s5,
        explanation=(
            "**先确认内核模块真的编好了再重启**：\n"
            "```bash\n"
            "modinfo -F version nvidia     # 能打出驱动版本号 = 编好了，可以重启\n"
            "```\n\n"
            "★ **为什么不能立刻重启**：`akmod` 是「**a**utomatic **kmod**」—— "
            "它在你装完后**才开始后台编译**内核模块（要几十秒到几分钟）。"
            "编译没完就重启，新驱动起不来，屏幕直接**黑屏**，"
            "而且黑屏之后你连终端都进不去，只能靠 rescue 模式救。\n\n"
            "**`akmod` vs `kmod`**（这是第 05 讲的一个考点）：\n\n"
            "| 包名 | 行为 |\n"
            "|---|---|\n"
            "| `kmod-nvidia` | 预先编好的，**内核一升级就失效**，得手动重装 |\n"
            "| **`akmod-nvidia`** | `a` = **automatic**，内核升级后**自动重建** ✅ |\n\n"
            "所以永远选 `akmod`。"),
        tags=["nvidia", "akmod", "显卡驱动", "第 05 讲"], difficulty=4,
    ))

    add(tf(
        "Fedora 上有 dpkg 吗",
        "Fedora 上可以用 `dpkg -i xxx.deb` 来安装 Debian 系的 deb 软件包。",
        False,
        subject=SUBJ, section=s5,
        explanation=(
            "**错**。**Fedora 上没有 `dpkg`** —— 那是 **Debian / Ubuntu** 的包管理器。\n\n"
            "两个体系的分工：\n\n"
            "| 发行版系 | 包格式 | 底层工具 | 高层工具 |\n"
            "|---|---|---|---|\n"
            "| **Red Hat 系**（Fedora、RHEL、CentOS） | `.rpm` | `rpm` | **`dnf`** |\n"
            "| **Debian 系**（Debian、Ubuntu） | `.deb` | **`dpkg`** | `apt` |\n\n"
            "**真想装 deb 包**：只能先转换，用 `alien`：\n"
            "```bash\n"
            "sudo dnf install alien\n"
            "sudo alien -r xxx.deb     # 转成 .rpm\n"
            "```\n"
            "★ 但**三个已知风险**（第 05 讲专门列过）：\n"
            "1. 依赖名对不上（`libfoo2` 在 Fedora 可能叫 `libfoo`）\n"
            "2. 库版本不匹配\n"
            "3. SELinux 标签可能不对\n\n"
            "**结论：转换出来的 rpm 只在虚拟机里试，别往主力机上装。**\n"
            "正确做法是找 Fedora 原生包，或者找上游的 Flatpak / 源码编译。"),
        tags=["dpkg", "deb", "包管理", "第 05 讲"], difficulty=3,
    ))

    add(fill(
        "一键回滚上一次软件安装",
        "你刚用 `dnf` 装了一堆东西，结果把系统搞坏了。"
        "想**撤销刚才那次操作**，用哪条命令？（先要查到操作编号）",
        ["sudo dnf history undo 1", "dnf history undo 1",
         "sudo dnf history undo last", "dnf history undo last"],
        subject=SUBJ, section=s5, difficulty=4, total_score=12,
        explanation=(
            "```bash\n"
            "dnf history                 # 先看历史，找到要撤销的编号\n"
            "sudo dnf history undo 12    # 把编号 12 那次操作完整回滚\n"
            "```\n\n"
            "★ 这是**改坏系统之后的正解** —— 不用重装，dnf 会按那次事务的记录"
            "把装上的包卸掉、把升级的包降回去。\n\n"
            "常用配套：\n"
            "```bash\n"
            "dnf history list            # 简表\n"
            "dnf history info 12         # 看这次到底动了什么\n"
            "sudo dnf history rollback 12  # 回滚到 12 号那次之后的状态（比 undo 更狠）\n"
            "```\n\n"
            "★ 另一个「零风险预演」技巧：\n"
            "```bash\n"
            "sudo dnf install --assumeno 一堆包    # 只打印「将会做什么」，不真装\n"
            "```\n"
            "装之前先跑一遍，能看出它要带进来多少东西 —— 避免装完才发现拖家带口。"),
        tags=["dnf", "history", "回滚", "第 05 讲"], hint="提示：dnf 的子命令，配合 `undo` 和事务编号。",
    ))


# ===================================================================== #
#  七、第 06 ~ 10 讲讲义概念题
# --------------------------------------------------------------------- #
#  这一批的重点是「**教材写法 vs Fedora 44 现实**」——
#  教材 2020 年 / Fedora 30 蓝本，而本机是 Fedora 44，
#  七年里包管理、服务管理、网络工具都换过。这些差异全部查证过。
# ===================================================================== #
def part_lectures_b() -> None:
    # ---------- 第 06 讲 ----------
    s6 = "第 06 讲 · 网络的基本配置"

    add(mc(
        "教材让你敲 ifconfig，但机器上没这个命令",
        "教材 6.2.4 节讲用 `ifconfig` 看网卡信息。你在 Fedora 44 上敲，"
        "报 `command not found`。怎么办？",
        ["装回 net-tools 包，恢复 ifconfig",
         "改用 ip addr",
         "用 sudo 提权就能用",
         "先 systemctl start network 启动网络服务"],
        "B",
        subject=SUBJ, section=s6,
        explanation=(
            "**改用 `ip addr`**（或简写 `ip a`）。\n\n"
            "Fedora 22 起**默认不再安装 `net-tools`** —— 那个包里装的就是"
            "`ifconfig`、`netstat`、`route` 这些**已被淘汰**的工具。"
            "它们被 `iproute2` 套件取代了：\n\n"
            "| 老命令（net-tools） | 新命令（iproute2） |\n"
            "|---|---|\n"
            "| `ifconfig` | **`ip addr`** / `ip link` |\n"
            "| `route -n` | `ip route` |\n"
            "| `netstat -anp` | **`ss -tulpn`** |\n"
            "| `arp -a` | `ip neigh` |\n\n"
            "★ 为什么**不建议装回 net-tools**：装回来会让**两套工具共存** —— "
            "`ifconfig` 和 `ip` 的显示口径不一样，排查问题时更容易搞混。"
            "直接适应 `ip` 是正路。\n\n"
            "补充：`ip addr` 加的地址是**临时的**，重启就没。永久配置得用 `nmcli`。"),
        tags=["ifconfig", "ip", "net-tools", "第 06 讲"], difficulty=3,
    ))

    add(mc(
        "nmcli 改完 IP 为什么不生效",
        "你用 `nmcli con modify 连接名 ipv4.addresses 192.168.1.100/24` 改了 IP，"
        "但 `ip addr` 看还是老地址。为什么？",
        ["命令写错了，要加 sudo",
         "modify 只写配置文件，必须再 con down 再 con up 才生效",
         "要先重启 NetworkManager 服务",
         "必须改 /etc/resolv.conf"],
        "B",
        subject=SUBJ, section=s6,
        explanation=(
            "**`nmcli con modify` 只把改动写进配置文件，不重连连接** —— "
            "所以得手动让它重新加载：\n"
            "```bash\n"
            "nmcli con down 连接名\n"
            "nmcli con up 连接名\n"
            "```\n\n"
            "★ **远程操作时这里有个致命陷阱**：如果你正通过 SSH 连着这台机器改 IP，"
            "`con down` 一敲**连接当场就断了**，后面的 `con up` 根本没机会执行。\n\n"
            "**三种保命方案**：\n"
            "```bash\n"
            "# ① 用图形化 TUI（断线也能重连，因为你人在本地）\n"
            "sudo nmtui\n"
            "\n"
            "# ② 把 up 推迟到 5 秒后执行，给自己留出重连的时间\n"
            "sudo sh -c 'sleep 5; nmcli con up 连接名' &\n"
            "\n"
            "# ③ 一次性下上（down 和 up 写在一起，但仍有短暂断线）\n"
            "sudo nmcli con down X && sudo nmcli con up X\n"
            "```\n\n"
            "**验证**：`ip addr show` 看地址有没有变、`nmcli con show X | grep ipv4` 看配置。"),
        tags=["nmcli", "网络配置", "第 06 讲"], difficulty=4,
    ))

    add(mc(
        "能 ping 通 IP 但打不开网页",
        "`ping 8.8.8.8` 通，但 `ping www.baidu.com` 报 `Name or service not known`，"
        "浏览器也打不开网页。问题最可能在哪？",
        ["网卡坏了，要换硬件", "IP 地址配错了",
         "DNS 解析有问题", "防火墙把 80 端口封了"],
        "C",
        subject=SUBJ, section=s6,
        explanation=(
            "**DNS 解析问题，不是网络问题。**\n\n"
            "★ 这个判据要背下来：\n\n"
            "| 现象 | 结论 |\n"
            "|---|---|\n"
            "| `ping IP` **通**、`ping 域名` **不通** | **DNS 问题**（网络本身是通的）|\n"
            "| `ping IP` **也不通** | 网络层问题（网线/路由/网关） |\n\n"
            "**排查顺序**：\n"
            "```bash\n"
            "cat /etc/resolv.conf          # 看配了哪些 DNS 服务器\n"
            "getent hosts www.baidu.com    # ★ 看系统「真实的解析结果」\n"
            "systemd-resolve --status       # 看当前实际用的 DNS（Fedora 上）\n"
            "```\n\n"
            "**怎么修（注意别用错方法）**：\n"
            "```bash\n"
            "# ❌ 直接改 /etc/resolv.conf —— 它是 NetworkManager 自动生成的，\n"
            "#    下次重连就被覆盖回去\n"
            "# ✅ 通过 nmcli 改：\n"
            "sudo nmcli con modify 连接名 ipv4.dns \"8.8.8.8 114.114.114.114\"\n"
            "sudo nmcli con down 连接名 && sudo nmcli con up 连接名\n"
            "```\n\n"
            "★ 为什么用 `getent hosts` 而不是直接看 `resolv.conf`："
            "`resolv.conf` 可能被覆盖，而 `getent` 走的是 **glibc 的完整解析链路**"
            "（`/etc/nsswitch.conf` 决定先查 `/etc/hosts` 还是先问 DNS），"
            "看到的是**系统真实的解析结果**。"),
        tags=["DNS", "resolv.conf", "排错", "第 06 讲"], difficulty=4,
    ))

    add(fill(
        "查看网卡的「真实名字」",
        "你照教材写 `ifconfig eth0`，报 `Device not found`。"
        "不确定这台机器的网卡到底叫什么名字 —— 用哪条命令**一眼看出所有网卡名**？",
        ["ip -br link", "ip link show", "ip -brief link", "ip -br addr",
         "ip link", "nmcli device status"],
        subject=SUBJ, section=s6, difficulty=3, total_score=12,
        explanation=(
            "**`ip -br link`**（`-br` = brief，简洁模式）。\n\n"
            "输出形如：\n"
            "```\n"
            "lo               UNKNOWN        00:00:00:00:00:00 <LOOPBACK,UP,LOWER_UP>\n"
            "enp1s0           UP             aa:bb:cc:dd:ee:ff <BROADCAST,MULTICAST,UP,LOWER_UP>\n"
            "wlp2s0           DOWN           ff:ee:dd:cc:bb:aa <BROADCAST,MULTICAST>\n"
            "```\n"
            "一眼就能看到真名（`enp1s0`、`wlp2s0`），而不是想当然的 `eth0`。\n\n"
            "★ **为什么不是 `eth0`**：现代 Linux 用**可预测网卡名**"
            "（predictable network interface names）。\n\n"
            "| 名字 | 含义 |\n"
            "|---|---|\n"
            "| `enp1s0` | **e**thernet、**n**etwork、**p**CI 总线 1、**s**lot 0 |\n"
            "| `wlp2s0` | **w**ireless、PCI 总线 2、slot 0 |\n"
            "| `lo` | 回环接口（永远存在） |\n\n"
            "这么改是为了防止「插拔网卡顺序一变，eth0 和 eth1 就换了个」—— "
            "那种情况下防火墙规则、网卡配置全都会错位。\n\n"
            "顺带：`nmcli device status` 也能列出网卡，而且带上连接状态，同样好用。"),
        tags=["网卡名", "ip", "第 06 讲"], hint="提示：ip 命令的简洁模式，只看链路（link）不看地址。",
    ))

    add(mc(
        "替代 netstat 看端口",
        "教材用 `netstat -anp` 查看监听端口。Fedora 44 上应该用哪条？",
        ["sudo lsof -i", "ss -tulpn", "netstat -tulpn", "ip port show"],
        "B",
        subject=SUBJ, section=s6,
        explanation=(
            "**`ss -tulpn`** —— 参数逐个拆开看：\n\n"
            "| 参数 | 含义 |\n"
            "|---|---|\n"
            "| `-t` | **t**cp |\n"
            "| `-u` | **u**dp |\n"
            "| `-l` | **l**istening，只看监听中的 |\n"
            "| `-p` | **p**rocess，显示是哪个进程占着（**要 sudo 才看得到别人的进程**）|\n"
            "| `-n` | **n**umeric，**端口和地址都用数字**，不做服务名反查 |\n\n"
            "★ **`-n` 为什么要加**：不加的话，`ss` 会把端口号反向解析成服务名"
            "（`:80` → `:http`）。问题是解析依赖 `/etc/services`，"
            "**某些端口能解析出来、某些不能** —— 一条输出里混着 `http` 和 `54321` 两种风格，"
            "排查时看着特别乱。**排障一律 `-n`**。\n\n"
            "典型输出：\n"
            "```\n"
            "tcp   LISTEN 0  4096  0.0.0.0:22    0.0.0.0:*  users:((\"sshd\",pid=1234,fd=3))\n"
            "tcp   LISTEN 0  511   0.0.0.0:80    0.0.0.0:*  users:((\"httpd\",pid=2345,fd=4))\n"
            "```\n\n"
            "★ 另一条好用的：`sudo lsof -i :80`（查**谁占着 80 端口**）。"),
        tags=["ss", "netstat", "端口", "第 06 讲"], difficulty=3,
    ))

    add(mc(
        "scp 和 ssh 的端口参数大小写",
        "SSH 服务跑在 2222 端口（不是默认的 22）。用 `scp` 传文件时，"
        "指定端口应该怎么写？",
        ["scp -p 2222 文件 远端:", "scp -P 2222 文件 远端:",
         "scp -port 2222 文件 远端:", "scp --port=2222 文件 远端:"],
        "B",
        subject=SUBJ, section=s6,
        explanation=(
            "**`scp -P 2222 ...`（大写 P）**。\n\n"
            "★ 这就是最坑的地方 —— **`ssh` 和 `scp` 的大小写刚好相反**：\n\n"
            "| 命令 | 指定端口 | 那另一个大小写是什么 |\n"
            "|---|---|---|\n"
            "| `ssh` | **`-p 2222`**（小写） | `-P` 是「不分配伪终端」 |\n"
            "| `scp` | **`-P 2222`**（大写） | `-p` 是「保留文件的时间戳和权限」 |\n"
            "| `sftp` | **`-P 2222`**（大写） | 同 scp |\n\n"
            "**用小写 `-p` 的后果**：scp **不报错**，只是默默地连到 22 端口 —— "
            "如果 22 上没服务，你会看到 `Connection refused`，"
            "然后开始怀疑网络、怀疑防火墙，**就是想不到是大写小写的问题**。\n\n"
            "**另一条路**（记不住就用这个）：在 `~/.ssh/config` 里给主机建个别名：\n"
            "```\n"
            "Host myserver\n"
            "    HostName 192.168.1.10\n"
            "    Port 2222\n"
            "    User lijihao\n"
            "```\n"
            "之后 `scp 文件 myserver:` 和 `ssh myserver` 都不用再写端口了。"),
        tags=["scp", "ssh", "端口", "第 06 讲"], difficulty=3,
    ))

    add(mc(
        "改主机名的正确方式",
        "你想把主机名从 `fedora` 改成 `mypc`。用 `hostname mypc` 改完，"
        "**重启后变回去了**。怎么回事？",
        ["要用 sudo hostname mypc",
         "hostname 只改当前运行时的值，永久生效要用 hostnamectl set-hostname",
         "还得改 /etc/resolv.conf",
         "主机名不能改，只能重装"],
        "B",
        subject=SUBJ, section=s6,
        explanation=(
            "**`hostname` 只改「当前运行时的值」，不写配置文件** —— 重启就复原。\n\n"
            "**永久修改要用**：\n"
            "```bash\n"
            "sudo hostnamectl set-hostname mypc\n"
            "```\n"
            "它会同时写入 `/etc/hostname`，重启后依然生效。\n\n"
            "**验证**：\n"
            "```bash\n"
            "hostnamectl                # 看 Static hostname\n"
            "cat /etc/hostname          # 看配置文件\n"
            "```\n\n"
            "★ **一个让人以为「没生效」的正常现象**：改完之后，"
            "**当前终端提示符里的主机名不会立刻变** —— 因为提示符是"
            "**登录时**拼好存在 `$PS1` 里的。**重新登录**（或 `exec bash`）才会变。\n\n"
            "**相关文件理清楚**：\n"
            "| 文件 | 作用 |\n"
            "|---|---|\n"
            "| `/etc/hostname` | 静态主机名（`hostnamectl` 写这个）|\n"
            "| `/etc/hosts` | 本机名字 → IP 的**即时映射**，改完立刻生效，不用重启 |\n"
            "| `/etc/resolv.conf` | **DNS 服务器**地址，跟主机名没关系 |\n\n"
            "（`/etc/hosts` 里那行 `127.0.0.1 localhost` **绝不能删** —— "
            "删了本机通信会出各种怪问题。）"),
        tags=["hostname", "hostnamectl", "第 06 讲"], difficulty=3,
    ))

    add(tf(
        "ping 不通就一定是网络故障",
        "`ping 某台主机` 不通，就可以确定是网络有问题。",
        False,
        subject=SUBJ, section=s6,
        explanation=(
            "**错**。**很多主机主动禁掉了 ICMP**（ping 用的协议）—— "
            "这是一种常见的安全/防扫措施，跟「网络通不通」是两件事。\n\n"
            "**更靠谱的连通性验证**：\n"
            "```bash\n"
            "nc -zv 主机 端口        # 测 TCP 端口能不能连上（最实用）\n"
            "curl -I http://主机/    # 只取 HTTP 响应头\n"
            "ss -tulpn | grep 端口   # 在本机确认服务真的在监听\n"
            "traceroute 主机         # 看卡在哪一跳\n"
            "```\n\n"
            "★ **另一个必加的参数**：`ping` **不带 `-c` 会一直发**，"
            "忘了停就一直在那刷。脚本里必须写 **`ping -c 4 主机`**"
            "（发 4 个包就停）。\n\n"
            "**还有一对容易搞反的**：\n"
            "```bash\n"
            "ping 域名        # 同时验证 DNS 解析 + 网络连通\n"
            "ping IP          # 只验证网络连通\n"
            "```\n"
            "两者对比一下，就能区分「是 DNS 坏还是网络坏」。"),
        tags=["ping", "ICMP", "排错", "第 06 讲"], difficulty=2,
    ))

    # ---------- 第 07 讲 ----------
    s7 = "第 07 讲 · 常用网络服务"

    add(mc(
        "systemctl enable 之后服务在跑吗",
        "你执行了 `sudo systemctl enable httpd`，以为网站已经能访问了。"
        "结果浏览器打不开。为什么？",
        ["Apache 装错了",
         "enable 只是「设为开机自启」，不会启动服务。要用 enable --now",
         "要重启机器才生效",
         "防火墙没放行"],
        "B",
        subject=SUBJ, section=s7,
        explanation=(
            "**`enable` 和 `start` 是两件事。**\n\n"
            "| 命令 | 作用 | 现在跑不跑 |\n"
            "|---|---|---|\n"
            "| `systemctl start X` | **立刻启动** | ✅ 跑 |\n"
            "| `systemctl enable X` | **设为开机自启**（写符号链接） | ❌ **不跑** |\n"
            "| **`systemctl enable --now X`** | 两个一起做 | ✅ 跑 |\n\n"
            "★ 正确姿势基本永远是 **`enable --now`** —— 既设了自启，又立刻起来。\n\n"
            "**怎么确认状态**（这是排查服务的第一步）：\n"
            "```bash\n"
            "systemctl status httpd\n"
            "```\n"
            "输出里两行要分清：\n"
            "```\n"
            "Loaded: loaded (/usr/lib/systemd/system/httpd.service; enabled; ...)\n"
            "                                     ↑ 这是「自启状态」\n"
            "Active: active (running) since ...\n"
            "        ↑ 这才是「运行状态」\n"
            "```\n"
            "★ **`Loaded: enabled` 完全不代表服务在跑** —— "
            "`enabled` 只是说「下次开机我会拉起它」。只有 `Active: active (running)` 才是真在跑。\n\n"
            "另外：改完 unit 文件**必须 `systemctl daemon-reload`**，"
            "否则改动不生效（这个坑很多人踩）。"),
        tags=["systemctl", "enable", "服务", "第 07 讲"], difficulty=2,
    ))

    add(mc(
        "四个服务的「户口本」",
        "在 Fedora 上，**Apache / vsFTPd / Samba / BIND 这四个服务**，"
        "各自的**包名**和**服务名**对应关系是？",
        ["包名和服务名全都一样",
         "Apache 包 httpd 服务 httpd；Samba 包 samba 服务 smb；BIND 包 bind 服务 named；vsFTPd 两者都叫 vsftpd",
         "Apache 包 apache2 服务 httpd；Samba 包 smbd 服务 samba；BIND 包 named 服务 named",
         "全都得用 systemctl list-unit-files 现查才知道"],
        "B",
        subject=SUBJ, section=s7,
        explanation=(
            "这是第 07 讲最该背下来的一张表 —— **包名和服务名不一定相同**：\n\n"
            "| 服务 | 包名 | **服务名**（systemctl 用的） |\n"
            "|---|---|---|\n"
            "| Apache HTTP | `httpd` | `httpd` |\n"
            "| vsFTPd | `vsftpd` | `vsftpd` |\n"
            "| **Samba** | `samba` | **`smb`** ★ |\n"
            "| **BIND（DNS）** | `bind` + `bind-utils` | **`named`** ★ |\n\n"
            "★ 两个「名不副实」的：\n"
            "- Samba **包**叫 `samba`，**服务**叫 `smb` —— "
            "敲 `systemctl enable samba` 会报 `Unit samba.service not found`\n"
            "- BIND **包**叫 `bind`，**服务**叫 `named`（**n**ame **d**aemon）—— "
            "同理，敲 `systemctl enable bind` 也找不到\n\n"
            "**另外两个常见错**：\n"
            "- `dnf install apache` / `apache2` —— Fedora 上是 **`httpd`**"
            "（`apache2` 是 Debian/Ubuntu 的叫法）\n"
            "- 想不起来服务叫什么 → `systemctl list-unit-files | grep 关键字` 查一下最快"),
        tags=["httpd", "smb", "named", "服务名", "第 07 讲"], difficulty=3,
    ))

    add(mc(
        "服务配好了，外面还是访问不到",
        "你把 Apache 配好了，`systemctl status httpd` 显示 `active (running)`，"
        "但**从别的机器访问不到**。按第 07 讲的经验，应该**按什么顺序**排查？",
        ["先看 SELinux，再看防火墙",
         "先查 firewall-cmd，再查 SELinux",
         "先重装 Apache",
         "先看 /var/log/messages"],
        "B",
        subject=SUBJ, section=s7,
        explanation=(
            "**先查 firewalld，再查 SELinux** —— 这个顺序有讲究。\n\n"
            "Fedora 上有**两道门禁**，服务要在外面能访问，两道都得放行：\n\n"
            "| | 管什么 | 怎么放行 | 报错特征 |\n"
            "|---|---|---|\n"
            "| **firewalld** | **端口**能不能进 | "
            "`firewall-cmd --permanent --add-service=http` + `--reload` | "
            "**连接被拒/超时**（包根本没进来） |\n"
            "| **SELinux** | 进程能不能读写**这个文件** | "
            "`semanage fcontext` + `restorecon` | **403 / 权限拒绝**（进程起来了但读不到文件）|\n\n"
            "★ **为什么先防火墙**：因为它更靠外 —— "
            "如果端口都没放行，包压根到不了 Apache，SELinux 根本没机会参与。"
            "先解决外层的，再看内层的，否则会白折腾。\n\n"
            "**怎么快速判断是哪一层**：\n"
            "- **本机 curl 通、外部不通** → **防火墙**问题\n"
            "- **本机 curl 也 403** → 大概率是 **SELinux**（或者文件权限）\n\n"
            "查防火墙：`sudo firewall-cmd --list-all`\n"
            "查 SELinux：`sudo ausearch -m avc -ts recent`（**要 sudo**，否则误判「没有 AVC」）"),
        tags=["firewalld", "SELinux", "双重门禁", "第 07 讲"], difficulty=4,
    ))

    add(mc(
        "chcon 和 semanage 的区别",
        "要给一个自建目录打上正确的 SELinux 标签，"
        "`chcon` 和 `semanage fcontext` 应该用哪个？",
        ["chcon，它是标准做法",
         "semanage fcontext + restorecon，chcon 是临时的会被冲掉",
         "两个完全等价，随便用",
         "两个都不用，改文件权限就行"],
        "B",
        subject=SUBJ, section=s7,
        explanation=(
            "**用 `semanage fcontext` + `restorecon`**（两步缺一不可）。\n\n"
            "| 命令 | 性质 | 会被覆盖吗 |\n"
            "|---|---|---|\n"
            "| `chcon` | **临时**改文件标签 | ✅ 会被 `restorecon` 或重启冲掉 |\n"
            "| **`semanage fcontext`** | **登记一条规则**（写进策略） | ❌ 永久 |\n"
            "| **`restorecon`** | **按规则刷新已有文件的标签** | —— |\n\n"
            "★ **关键认知**：`semanage fcontext` **只是登记规则，不碰现有文件**。"
            "很多人跑完 `semanage` 就去测试，怎么都不生效 —— "
            "**因为还得跑 `restorecon` 把旧标签刷一遍**。\n\n"
            "标准两步：\n"
            "```bash\n"
            "sudo semanage fcontext -a -t httpd_sys_content_t \"/srv/www(/.*)?\"\n"
            "sudo restorecon -Rv /srv/www\n"
            "```\n"
            "★ 注意那个 **`(/.*)?`** 正则 —— 不写它的话"
            "**只匹配目录本身、管不到里面的文件**，"
            "症状就是「目录能进、文件 403」。\n\n"
            "另外 `semanage` 命令本身在 Fedora 上**默认没装**，"
            "要 `sudo dnf install policycoreutils-python-utils`。\n\n"
            "**绝对不要对 `/etc`、`/usr` 做 `chcon -R`** —— 会严重破坏系统。"),
        tags=["SELinux", "semanage", "chcon", "第 07 讲"], difficulty=4,
    ))

    add(mc(
        "改完 unit 文件为什么没生效",
        "你用 `systemctl edit myservice` 写了 drop-in 覆盖 `ExecStart`，"
        "然后 `systemctl restart myservice` 却报 `multiple ExecStart`。"
        "少了什么？",
        ["少写一行空的 ExecStart= 先把原值清掉",
         "drop-in 应该写在 /usr/lib 下",
         "要加 --force 参数",
         "要先 systemctl daemon-reload —— 重载了就没事"],
        "A",
        subject=SUBJ, section=s7,
        explanation=(
            "**必须先写一行空的 `ExecStart=` 把原值清空。**\n\n"
            "systemd 的规则是：**同一个指令出现多次 = 追加**。"
            "所以 drop-in 里直接写 `ExecStart=/新命令` 会变成\n"
            "「旧命令 + 新命令」两条启动命令 → 报 `multiple ExecStart`。\n\n"
            "正确写法：\n"
            "```ini\n"
            "[Service]\n"
            "ExecStart=                    # ★ 这一行空的，作用是「清空原值」\n"
            "ExecStart=/opt/myservice/bin/run --new-flag\n"
            "```\n"
            "★ 空行看着莫名其妙，但它**就是这个用途** —— 记住「先清空、再赋值」。\n\n"
            "**另外两个配套要点**：\n"
            "1. **改完 unit 文件必须 `sudo systemctl daemon-reload`** —— "
            "不然 systemd 用的还是老配置（这个坑比 `ExecStart` 那个更常见）\n"
            "2. **不要去改 `/usr/lib/systemd/system/*.service`** —— "
            "包升级时你的改动会被覆盖。要用 `systemctl edit X` 写 drop-in，"
            "它落在 `/etc/systemd/system/X.service.d/` 下，升级不丢"),
        tags=["systemd", "drop-in", "ExecStart", "第 07 讲"], difficulty=4,
    ))

    add(mc(
        "disable 和 mask 有什么不同",
        "`systemctl disable X` 和 `systemctl mask X` 的区别是？",
        ["完全一样",
         "disable 只取消自启（还能手动 start）；mask 彻底禁死（连手动都起不来）",
         "disable 是临时的，mask 是永久的",
         "mask 会卸载软件包"],
        "B",
        subject=SUBJ, section=s7,
        explanation=(
            "**两个力度完全不同**：\n\n"
            "| 命令 | 做了什么 | 还能手动 start 吗 |\n"
            "|---|---|---|\n"
            "| `disable` | 删掉开机自启的符号链接 | ✅ **能** |\n"
            "| `mask` | 把服务**链到 `/dev/null`** | ❌ **不能**，会报 "
            "`Unit X is masked` |\n\n"
            "★ **`mask` 的使用场景**：某个服务被别的服务依赖，"
            "老是自动被拉起来，你**根本不想让它跑**（比如和另一个方案冲突）—— "
            "这时才用 `mask`。\n\n"
            "**取消 mask**：`sudo systemctl unmask X`。\n\n"
            "**`enable` 和 `start` 的对应关系**（一起记）：\n"
            "| | 立刻跑 | 开机自启 |\n"
            "|---|---|---|\n"
            "| `start` | ✅ | ❌ |\n"
            "| `enable` | ❌ | ✅ |\n"
            "| `enable --now` | ✅ | ✅ |\n\n"
            "再加一个：**`restart` vs `reload`** —— 改的是「仅配置类」的变更优先用 "
            "`reload`（**不中断现有连接**）；拿不准就 `reload-or-restart`。"),
        tags=["systemctl", "disable", "mask", "第 07 讲"], difficulty=3,
    ))

    # ---------- 第 08 讲 ----------
    s8 = "第 08 讲 · 系统管理与监视"

    add(mc(
        "useradd 之后为什么登录不了",
        "你执行了 `sudo useradd zhang`，然后用 `su - zhang` 却进不去。为什么？",
        ["要先 usermod 加 shell",
         "useradd 建的账号是锁死的（shadow 里是 !!），必须再 passwd 设密码",
         "要重启系统",
         "要先 useradd -m 建家目录"],
        "B",
        subject=SUBJ, section=s8,
        explanation=(
            "**`useradd` 只建账号，不给密码** —— 建出来的账号是**锁死状态**"
            "（`/etc/shadow` 里密码字段是 `!!`）。\n\n"
            "```bash\n"
            "sudo useradd -m zhang     # -m 顺便建家目录并放好骨架文件\n"
            "sudo passwd zhang         # ★ 这一步不能少：交互式设密码\n"
            "```\n\n"
            "★ **`useradd` vs `adduser`**（Fedora 上两个都在）：\n"
            "| | 行为 |\n"
            "|---|---|\n"
            "| `useradd` | **底层**命令，只建账号，什么都不问；不建家目录（除非 `-m`）|\n"
            "| `adduser` | Fedora 上是 `useradd` 的**友好包装**，会交互式问你密码、全名等 |\n\n"
            "（注意：Debian 系上 `adduser` 是完全不同的实现，行为差得更远。）\n\n"
            "**验证账号状态**：\n"
            "```bash\n"
            "sudo passwd -S zhang      # 输出第二列：L = 锁定 / P = 已设密码\n"
            "sudo grep zhang /etc/shadow   # 看密码字段\n"
            "```\n\n"
            "★ 相关陷阱：**别用 `passwd -d` 想禁用账号** —— "
            "`-d` 是**删掉密码**，等于**免密登录**（更危险）。"
            "想禁要用 **`passwd -l`**（lock）。"),
        tags=["useradd", "passwd", "用户管理", "第 08 讲"], difficulty=3,
    ))

    add(mc(
        "usermod 加附加组，-G 还是 -aG",
        "你要把用户 `zhang` 加进 `wheel` 组，**同时保留他原来已经在的所有组**。"
        "正确的是哪条？",
        ["sudo usermod -G wheel zhang", "sudo usermod -aG wheel zhang",
         "sudo usermod -g wheel zhang", "sudo groupadd -a wheel zhang"],
        "B",
        subject=SUBJ, section=s8,
        explanation=(
            "**`sudo usermod -aG wheel zhang`** —— `-a`（append，追加）不能省。\n\n"
            "★ **漏掉 `-a` 的后果很严重**：`-G` 是「**设置**附加组」，"
            "会**覆盖**掉用户原有的全部附加组。\n\n"
            "举个例子：某用户本来在 `wheel`、`audio`、`video`、`libvirt` 四个组里，"
            "你执行 `usermod -G docker zhang` 想加 docker 组 —— 结果变成**只有 docker 组**，"
            "声音没了（audio 丢了）、显卡加速没了（video 丢了）、sudo 用不了（wheel 丢了）。\n\n"
            "**三个 G 分清楚**：\n\n"
            "| 参数 | 作用 | 危险度 |\n"
            "|---|---|---|\n"
            "| `-g`（小写）| 改**主组** | 高（覆盖）|\n"
            "| `-G`（大写）| **设置**附加组列表 | ★ **高，覆盖** |\n"
            "| **`-aG`** | **追加**附加组 | 低 ✅ |\n\n"
            "★ **口诀：加组永远写 `-aG`**。\n\n"
            "**另一个「以为没生效」的正常现象**：加完组当场用新权限**不生效** —— "
            "因为**组身份是登录时快照的**。要 `exec bash` 或重新登录。\n\n"
            "**查自己在哪些组**：`id -nG`（`whoami` 只看名字，看不到组）。"),
        tags=["usermod", "附加组", "-aG", "第 08 讲"], difficulty=3,
    ))

    add(mc(
        "想看系统日志，该打开哪个文件",
        "照教材敲 `cat /var/log/messages` 想看系统日志，"
        "结果报 `No such file or directory`。应该用什么？",
        ["装 rsyslog 才有这个文件", "用 journalctl",
         "改用 /var/log/syslog", "改用 dmesg"],
        "B",
        subject=SUBJ, section=s8,
        explanation=(
            "**用 `journalctl`** —— Fedora 默认**不装 rsyslog**，"
            "`/var/log/messages` 这个文件根本不存在。\n\n"
            "Fedora 用的是 **systemd-journald**，日志收在**二进制**日志里，"
            "要用 `journalctl` 读：\n\n"
            "```bash\n"
            "journalctl -n 50                 # 最近 50 条\n"
            "journalctl -u httpd              # 只看某个服务的\n"
            "journalctl -p err                # 只看 error 级别以上\n"
            "journalctl --since \"1 hour ago\"  # 最近一小时\n"
            "journalctl -f                    # 实时跟（类似 tail -f）\n"
            "journalctl -b                    # 本次开机以来的\n"
            "```\n\n"
            "★ **一个必知的默认行为**：journald **默认不持久化** —— "
            "日志只存在内存里（`/run/log/journal/`），**重启就没了**。\n\n"
            "想保留重启前的日志，要手动开启持久化：\n"
            "```bash\n"
            "sudo mkdir -p /var/log/journal\n"
            "sudo systemd-tmpfiles --create --prefix /var/log/journal\n"
            "sudo systemctl restart systemd-journald\n"
            "```\n"
            "之后重启才能用 `journalctl -b -1` 查**上一次开机**的日志"
            "（**不开持久化的话，`-b -1` 查不到任何东西**）。\n\n"
            "（`rsyslog` 装了会同时生成 `/var/log/messages`，但 Fedora 默认没有。）"),
        tags=["journalctl", "日志", "rsyslog", "第 08 讲"], difficulty=3,
    ))

    add(mc(
        "chmod -R 644 目录的后果",
        "你执行了 `chmod -R 644 /home/zhang/project`，想把文件权限统一。"
        "结果 `cd` 进那个目录都报 Permission denied。为什么？",
        ["要 sudo",
         "目录失去 x 权限就进不去了 —— 目录要 755、文件才 644",
         "要 chown 一下",
         "644 的 6 太少了"],
        "B",
        subject=SUBJ, section=s8,
        explanation=(
            "**因为目录的权限位含义和文件不一样：目录的 `x` 是「能进入/能穿过」。**\n\n"
            "| 位 | 对**文件** | 对**目录** |\n"
            "|---|---|---|\n"
            "| `r` | 读内容 | **列出**里面有什么（`ls`）|\n"
            "| `w` | 写内容 | **在里面建/删**文件 |\n"
            "| **`x`** | 当作程序执行 | ★ **能进去（`cd`）、能访问里面的文件** |\n\n"
            "`644` 的权限是 `rw-r--r--` —— **没有 `x`**。"
            "对文件无所谓，对目录就是「**连进都进不去**」。\n\n"
            "**正确做法：目录和文件分开设**。\n"
            "```bash\n"
            "find /home/zhang/project -type d -exec chmod 755 {} \\;   # 目录 755\n"
            "find /home/zhang/project -type f -exec chmod 644 {} \\;   # 文件 644\n"
            "```\n\n"
            "★ **记住这组常规值**：\n"
            "| 对象 | 权限 | 含义 |\n"
            "|---|---|---|\n"
            "| 普通目录 | `755` | 人人能进、只有属主能写 |\n"
            "| 普通文件 | `644` | 人人能读、只有属主能写 |\n"
            "| 私钥 / 密码文件 | `600` | **只有属主**能读写 |\n\n"
            "**`777` 在什么场合都不该用**（生产环境等于取消整个权限体系）。"),
        tags=["chmod", "目录权限", "x 位", "第 08 讲"], difficulty=3,
    ))

    add(mc(
        "杀进程该用哪个信号",
        "一个进程卡住了，你要杀掉它。第 08 讲的建议是？",
        ["直接 kill -9，一步到位",
         "先 kill（默认 15），等几秒不行再 kill -9",
         "先 kill -1，再 kill -9",
         "用 killall -9 批量杀"],
        "B",
        subject=SUBJ, section=s8,
        explanation=(
            "**先 `kill`（默认发 15 号信号），等几秒，还不行再 `kill -9`。**\n\n"
            "两个信号的本质区别：\n\n"
            "| 信号 | 名字 | 行为 |\n"
            "|---|---|---|\n"
            "| **15（默认）** | SIGTERM | **请求**进程自己收尾退出 —— 进程能**捕获**它，"
            "先把缓存刷盘、关文件、释放锁，然后干净地退出 |\n"
            "| **9** | SIGKILL | **内核直接宰掉**，进程**无法捕获、无法反抗** |\n\n"
            "★ **为什么不能一上来 `-9`**：进程被硬杀时**没机会收尾**，"
            "可能留下：\n"
            "- 数据库写到一半（数据损坏）\n"
            "- 端口没释放（下次启动报 `Address already in use`）\n"
            "- 锁文件残留（下次启动说「已经在运行」）\n"
            "- 临时文件堆积\n\n"
            "**所以正确顺序是**：\n"
            "```bash\n"
            "kill PID            # 15，给它机会好好退\n"
            "sleep 3\n"
            "kill -9 PID         # 还赖着才硬来\n"
            "```\n\n"
            "**另外两个易错点**：\n"
            "1. **僵尸进程杀不掉** —— 它**已经死了**，`kill -9` 完全无效。"
            "要处理它的**父进程**（父进程 wait 之后它才会消失）\n"
            "2. **别用 `ps aux | grep x` 找进程** —— 输出里总会多出 `grep x` 自己那一行。"
            "用 `pgrep -a 名字`\n"
            "3. **`ps aux` 没有 PPID 列** —— 想找父进程用 `ps -ef` 或 `ps -eo pid,ppid,cmd`"),
        tags=["kill", "SIGTERM", "SIGKILL", "第 08 讲"], difficulty=3,
    ))

    add(mc(
        "给脚本设 SUID 想以 root 运行",
        "你写了个 shell 脚本，`chmod 4755 script.sh` 设了 SUID 位，"
        "想让普通用户执行时以 root 身份运行。结果没有效果。为什么？",
        ["要 chown root 才行",
         "内核直接忽略脚本的 SUID 位，SUID 只对二进制程序生效",
         "要放到 /usr/bin 下才行",
         "要 chmod 6755"],
        "B",
        subject=SUBJ, section=s8,
        explanation=(
            "**内核故意忽略脚本上的 SUID 位** —— 这是**安全设计**，不是 bug。\n\n"
            "**为什么**：脚本是文本，解释器（bash）会逐行读它。"
            "如果 SUID 对脚本生效，那么任何能写这个脚本的人"
            "（哪怕只是能改中间几行）就相当于**获得了 root 执行任意命令的能力** —— "
            "提权门槛低到离谱。\n\n"
            "**正确的做法有两条**：\n\n"
            "**① 用 `sudo`**（最推荐）—— 给特定命令开白名单：\n"
            "```bash\n"
            "sudo visudo      # ★ 永远用 visudo，别直接改 /etc/sudoers\n"
            "# 加一行：\n"
            "zhang ALL=(root) NOPASSWD: /usr/local/bin/mywork.sh\n"
            "```\n\n"
            "**② 写个小 C 包装程序**（SUID 对二进制生效）。\n\n"
            "★ 顺带记一个相关坑：`chmod 4755` 之后 `ls -l` 看到的是 `rwSr-xr-x` —— "
            "**大写 `S` 表示「SUID 设了，但执行位没设」**，配置有问题。\n"
            "正确顺序是**先 `chmod +x`，再设特殊位**，这样才显示小写 `s`（`rwsr-xr-x`）。\n\n"
            "（`visudo` 为什么必用：它会**校验语法**。直接改 `/etc/sudoers` "
            "写错一个字符，你就**再也 sudo 不了了**。）"),
        tags=["SUID", "脚本", "权限", "第 08 讲"], difficulty=4,
    ))

    add(tf(
        "wheel 组能限制 su 吗",
        "把用户从 `wheel` 组里移除，他就无法使用 `su` 命令了。",
        False,
        subject=SUBJ, section=s8,
        explanation=(
            "**错**。**默认情况下 `su` 没有任何组限制** —— "
            "任何知道 root 密码的用户都能 `su` 上去。\n\n"
            "所谓「wheel 组才能 su」的机制**是存在的，但默认是关的** —— "
            "它由 PAM 控制，相关那行在 `/etc/pam.d/su` 里**被注释掉了**：\n"
            "```\n"
            "#auth  required  pam_wheel.so use_uid\n"
            " ↑ 开头的 # 就是「没启用」\n"
            "```\n"
            "要去掉那个 `#` 才会生效。\n\n"
            "★ **分清两个不同的限制**：\n\n"
            "| 机制 | 管什么 | 默认状态 |\n"
            "|---|---|---|\n"
            "| **`wheel` 组 + `sudo`** | 谁能用 sudo | Fedora 上**默认启用** |\n"
            "| **`pam_wheel` + `su`** | 谁能用 su | **默认关闭** |\n\n"
            "所以在 Fedora 上，普通用户用不了 `sudo`（不在 wheel 组），"
            "但只要知道 root 密码，`su -` 照样能上去。\n\n"
            "**另外**：Fedora Workstation 安装时**默认不给 root 设密码**，"
            "所以默认状态下其实连 `su -` 都用不了，全靠 sudo —— "
            "这也正是 Fedora 推荐的工作方式。"),
        tags=["su", "wheel", "pam", "第 08 讲"], difficulty=4,
    ))

    add(mc(
        "free 显示的内存很小，是不是不够用",
        "`free -h` 输出里 `free` 那一列只有 500 MB，但机器是 16 GB 内存。"
        "是不是内存要满了？",
        ["是的，要赶紧关程序",
         "看 available 那一列才是真实可用内存，cache 是可回收的",
         "要加内存条",
         "free 输出不准"],
        "B",
        subject=SUBJ, section=s8,
        explanation=(
            "**看 `available` 列，别看 `free` 列。**\n\n"
            "Linux 的设计理念是「**空闲的内存就是浪费的内存**」—— "
            "它会把暂时用不到的内存拿去做**磁盘缓存**（cache/buffers），"
            "加速读写。这些缓存在程序需要内存时**可以立刻回收**。\n\n"
            "```\n"
            "               total   used   free   shared  buff/cache   available\n"
            "Mem:           15Gi   4.2Gi  500Mi   120Mi      10Gi        10Gi\n"
            "                       ↑ used        ↑ free   ↑ 缓存      ↑ ★ 看这个\n"
            "```\n\n"
            "| 列 | 含义 |\n"
            "|---|---|\n"
            "| `free` | **完全没被用过**的内存 —— 数字小是**正常且健康的** |\n"
            "| `buff/cache` | 磁盘缓存，**随时可回收** |\n"
            "| **`available`** | **真正可用于新程序的内存** ≈ free + 可回收的 cache ✅ |\n\n"
            "★ 所以 `free` 小**恰恰说明系统在充分利用内存**，不是坏事。\n\n"
            "**想主动释放缓存**（一般没必要）：\n"
            "```bash\n"
            "sync && echo 3 | sudo tee /proc/sys/vm/drop_caches\n"
            "```\n\n"
            "**配套的两个存储排查命令**：\n"
            "- `df -h` 看**磁盘空间**\n"
            "- **`df -i`** 看 **inode 用尽** —— 磁盘报 `No space left` 但 `df -h` 显示有空间时，"
            "八成是 inode 满了（有大量小文件）"),
        tags=["free", "内存", "available", "第 08 讲"], difficulty=3,
    ))

    add(mc(
        "cron 任务里为什么找不到命令",
        "你在 `crontab -e` 里写了个任务 `* * * * * python3 /home/zhang/x.py`，"
        "但日志里报 `python3: command not found`。手动执行却没问题。为什么？",
        ["cron 没有权限跑 python",
         "cron 的 PATH 极小，必须写绝对路径 /usr/bin/python3",
         "要加 sudo",
         "要写 python 而不是 python3"],
        "B",
        subject=SUBJ, section=s8,
        explanation=(
            "**cron 执行时的 `PATH` 极小**（通常只有 `/usr/bin:/bin`），"
            "和你的交互式 shell 完全不是一回事。\n\n"
            "★ 你的终端里能跑，是因为 `~/.bashrc` / `/etc/profile` 帮你"
            "**扩过 PATH** 了；而 **cron 不读这些文件**。\n\n"
            "**正确写法：全部用绝对路径**\n"
            "```\n"
            "* * * * * /usr/bin/python3 /home/zhang/x.py > /home/zhang/cron.log 2>&1\n"
            "```\n\n"
            "**顺带几个 cron 的必知坑**：\n\n"
            "| 坑 | 正确做法 |\n"
            "|---|---|\n"
            "| 输出没地方去，全被邮件系统收着 | 加 `> /path/log 2>&1` 重定向 |\n"
            "| 时间格式里的 `%` 被当成换行 | 转义：`date +\\%F` |\n"
            "| 以为能写「每 30 秒」 | **最小粒度是 1 分钟**；要更细用 systemd timer |\n"
            "| `crontab -r` 手一抖 | **一次删光所有任务、不询问**。想安全用 `crontab -i -r` |\n\n"
            "**时间格式速记**：\n"
            "```\n"
            "* * * * *  命令\n"
            "│ │ │ │ └── 星期（0-7，0 和 7 都是周日）\n"
            "│ │ │ └──── 月（1-12）\n"
            "│ │ └────── 日（1-31）\n"
            "│ └──────── 时（0-23）\n"
            "└────────── 分（0-59）\n"
            "```"),
        tags=["cron", "PATH", "计划任务", "第 08 讲"], difficulty=4,
    ))

    # ---------- 第 09 讲 ----------
    s9 = "第 09 讲 · 系统安全管理"

    add(tf(
        "/etc/hosts.allow 能限制 SSH 来源吗",
        "在 `/etc/hosts.allow` 里配置规则，可以限制哪些 IP 能连 SSH。",
        False,
        subject=SUBJ, section=s9,
        explanation=(
            "**错**。**对 sshd 完全失效**。\n\n"
            "TCP Wrappers（`hosts.allow` / `hosts.deny`）这套机制要求"
            "程序**动态链接 `libwrap`** 才会生效。而 "
            "**OpenSSH 7.5 起就不再链接 libwrap 了** —— 所以你写在 "
            "`hosts.allow` 里的规则**被完全忽略，且不报任何错**。\n\n"
            "★ 这是最阴的一种失效：**你配了、看着像生效了、实际什么都没发生**。\n\n"
            "**自证方法**（一条命令就能确认）：\n"
            "```bash\n"
            "ldd $(which sshd) | grep libwrap\n"
            "# 空输出 = 没有链接 libwrap = hosts.allow 对 sshd 无效\n"
            "```\n\n"
            "**正确的做法**（改 `sshd_config`）：\n"
            "```\n"
            "AllowUsers zhang admin@192.168.1.*\n"
            "DenyUsers baduser\n"
            "Match Address 192.168.2.0/24\n"
            "    PasswordAuthentication no\n"
            "```\n"
            "★ 改完**必须**：\n"
            "```bash\n"
            "sudo sshd -t           # ★ 先校验语法！错一个字符就永久失联\n"
            "sudo systemctl reload sshd    # 用 reload 不用 restart\n"
            "```"),
        tags=["TCPWrappers", "hosts.allow", "sshd", "第 09 讲"], difficulty=4,
    ))

    add(mc(
        "手动加的 iptables 规则为什么消失了",
        "你用 `iptables -A INPUT ...` 手动加了几条规则，测试时是好的。"
        "过了一阵再看，规则没了。为什么？",
        ["被系统自动清理了",
         "firewalld 重载时会冲掉手写的规则",
         "iptables 有超时机制",
         "要 iptables-save 才生效"],
        "B",
        subject=SUBJ, section=s9,
        explanation=(
            "**firewalld 在重载时会接管（并冲掉）底层的 iptables 规则。**\n\n"
            "在 Fedora 上，`iptables` 命令其实**不是真的 iptables** —— "
            "它是 `iptables-nft`，**转发到 nftables 内核框架**。"
            "而 firewalld 也是通过 nftables 管理规则的 —— **两者共用同一套底层**，"
            "firewalld 一 reload 就会按自己的规则表重写。\n\n"
            "★ **必须二选一，不能混着用**：\n\n"
            "**方案 A：只用 firewalld**（Fedora 的推荐做法）\n"
            "```bash\n"
            "sudo firewall-cmd --permanent --add-service=http\n"
            "sudo firewall-cmd --reload      # ★ 不加这步，永久规则不生效\n"
            "sudo firewall-cmd --list-all    # 验证\n"
            "```\n"
            "（`--timeout=300` 可以加个自动过期，防止把自己锁在外面。）\n\n"
            "**方案 B：直用 iptables 裸命令**\n"
            "```bash\n"
            "sudo systemctl disable --now firewalld   # ★ 必须先停掉 firewalld\n"
            "sudo iptables -A INPUT ...\n"
            "sudo iptables-save > /etc/sysconfig/iptables   # 手动持久化\n"
            "```\n\n"
            "★ **另一个认知纠正**：即使在 iptables 里写了 `-j ACCEPT`，"
            "**包还是可能过不去** —— 因为 ACCEPT 只表示「这条链放行」，"
            "后面 firewalld 的规则还可能拦。"),
        tags=["iptables", "firewalld", "nftables", "第 09 讲"], difficulty=4,
    ))

    add(mc(
        "setsebool 忘了加什么会失效",
        "你执行 `sudo setsebool httpd_can_network_connect on` 让 Apache 能连网络，"
        "测试通了。**重启之后又不通了**。漏了什么？",
        ["漏了 sudo -i",
         "漏了 -P 参数，改动没写进策略",
         "漏了 systemctl reload httpd",
         "漏了 semanage"],
        "B",
        subject=SUBJ, section=s9,
        explanation=(
            "**漏了 `-P`。**\n\n"
            "```bash\n"
            "sudo setsebool httpd_can_network_connect on      # ❌ 只在内存里有效，重启就没了\n"
            "sudo setsebool -P httpd_can_network_connect on   # ✅ -P = Persistent，写进策略\n"
            "```\n\n"
            "★ **这个坑为什么特别阴**：\n"
            "1. 改完当场测试**是通的** → 你以为搞定了\n"
            "2. 重启后失效 → 但你已经把这事忘了，只会觉得「怎么又坏了」\n"
            "3. 事后极难定位，因为「同一个操作」在重启前后表现不同\n\n"
            "**一句话规矩**：`setsebool` **永远加 `-P`**。\n\n"
            "**查看当前值**：\n"
            "```bash\n"
            "getsebool -a | grep httpd_can_network_connect\n"
            "```\n"
            "★ 补充：`setsebool -P` 会**重写整个 SELinux 策略**，"
            "所以第一次跑要等几十秒到几分钟，**那是在正常干活，不是卡死了**。\n\n"
            "**相关的另一对**（第 09 讲反复强调的）：\n"
            "- `setenforce 0` = **临时**切到宽容模式，重启复原\n"
            "- 想永久改要改 `/etc/selinux/config` 里的 `SELINUX=`"),
        tags=["setsebool", "-P", "SELinux", "第 09 讲"], difficulty=4,
    ))

    add(mc(
        "semanage 报 command not found",
        "你在 Fedora 44 上敲 `semanage fcontext ...`，报 `command not found`。"
        "怎么办？",
        ["semanage 命令不存在，用 chcon 代替",
         "sudo dnf install policycoreutils-python-utils",
         "要 sudo 才有这个命令",
         "要先启动 SELinux"],
        "B",
        subject=SUBJ, section=s9,
        explanation=(
            "**装 `policycoreutils-python-utils` —— Fedora 默认不装它。**\n\n"
            "```bash\n"
            "sudo dnf install policycoreutils-python-utils\n"
            "```\n"
            "装完 `semanage`、`audit2allow`、`sealert` 这类工具就都有了。\n\n"
            "★ **为什么默认不装**：这些是「**管理 SELinux 策略**」的工具，"
            "普通桌面用户根本用不上；默认装的只有 `selinux-policy` 和基础客户端。\n\n"
            "**装完之后有个必知的坑**（第 09 讲陷阱清单第 7 条）：\n"
            "```bash\n"
            "sudo semanage fcontext -a -t httpd_sys_content_t \"/srv/www\"     # ❌\n"
            "```\n"
            "**不写正则的话，只匹配目录本身，里面的文件管不到** —— "
            "症状就是「目录能进、文件 403」。正确写法：\n"
            "```bash\n"
            "sudo semanage fcontext -a -t httpd_sys_content_t \"/srv/www(/.*)?\"\n"
            "sudo restorecon -Rv /srv/www     # ★ 还必须刷一遍标签，两步缺一不可\n"
            "```\n\n"
            "**相关的一族命令**：\n"
            "| 命令 | 用途 |\n"
            "|---|---|\n"
            "| `semanage fcontext -l` | 列出所有文件上下文规则 |\n"
            "| `semanage port -a -t http_port_t -p tcp 8080` | **给端口打标签**（改服务端口时要）|\n"
            "| `semanage boolean -l` | 列出所有布尔开关 |\n"
            "| `restorecon -Rv 目录` | 按策略刷新文件标签 |\n"
            "| `ls -Z 文件` | 看文件的 SELinux 标签 |"),
        tags=["semanage", "SELinux", "安装", "第 09 讲"], difficulty=4,
    ))

    add(mc(
        "SELINUX=disabled 有什么代价",
        "嫌 SELinux 麻烦，把 `/etc/selinux/config` 改成 `SELINUX=disabled`。"
        "会有什么代价？",
        ["没什么代价，只是省事",
         "新建的文件全都没有标签；日后想再启用要全盘 relabel，可能开不了机",
         "只影响防火墙",
         "会让系统变慢"],
        "B",
        subject=SUBJ, section=s9,
        explanation=(
            "**代价很大，而且会积累 —— 到你想启用时才爆发。**\n\n"
            "**问题链条**：\n"
            "1. SELinux 关闭期间，所有**新建/修改的文件都没有安全标签**\n"
            "2. 哪天你想重新启用 → 系统**不认这些无标签的文件** → "
            "连开机都起不来（启动早期就被拦）\n"
            "3. 唯一的解法是**全盘重新打标签**：\n"
            "```bash\n"
            "sudo touch /.autorelabel\n"
            "sudo reboot\n"
            "```\n"
            "★ 这会给**整个文件系统每一行**重打标签，"
            "几百 GB 的盘可能要跑**几十分钟到几小时**，期间系统不可用。\n\n"
            "**正确做法：要宽松就用 `permissive`，不要 `disabled`**\n"
            "```\n"
            "SELINUX=permissive     # 只记录违规、不阻止 —— 日志里有 AVC，但服务照跑\n"
            "```\n"
            "★ `permissive` 下文件**仍然会被打标签**，所以日后切回 `enforcing` "
            "只要改一个词 + 重启，不用 relabel。\n\n"
            "**还有一条更重要的认知**（第 09 讲反复讲）：\n"
            "> **`setenforce 0` 是诊断手段，不是解决方案。**\n\n"
            "正确流程是「先看 AVC 日志搞清楚它在拦什么 → 针对性放行」：\n"
            "```bash\n"
            "sudo ausearch -m avc -ts recent      # ★ 必须 sudo，否则误判「没有 AVC」\n"
            "sudo journalctl -t setroubleshoot\n"
            "```\n"
            "★ **另外**：遇到 403 就 `chmod -R 777` **对 SELinux 引起的 403 完全无效** —— "
            "那是第二关，DAC 权限早就过了。"),
        tags=["SELinux", "disabled", "permissive", "第 09 讲"], difficulty=4,
    ))

    add(tf(
        "firewall-cmd --permanent 之后立刻生效吗",
        "`sudo firewall-cmd --permanent --add-service=http` 执行后，"
        "规则会立刻生效。",
        False,
        subject=SUBJ, section=s9,
        explanation=(
            "**错**。`--permanent` 写的规则进的是**永久配置**，"
            "**不会立即作用到当前运行时的防火墙**。\n\n"
            "需要再执行一次**重载**：\n"
            "```bash\n"
            "sudo firewall-cmd --permanent --add-service=http\n"
            "sudo firewall-cmd --reload         # ★ 不加这步，现在还是访问不了\n"
            "```\n\n"
            "★ **为什么这么设计**：`--permanent` 是为「下次启动」准备的配置；"
            "运行时的规则是另一套内存态。这样你在改配置的过程中，"
            "正在跑的服务**不会被打断**。\n\n"
            "**两类操作对照**：\n"
            "| 命令 | 生效时机 | 重启后 |\n"
            "|---|---|---|\n"
            "| `firewall-cmd --add-service=http`（不带 --permanent）| **立刻** | ❌ 丢失 |\n"
            "| `firewall-cmd --permanent --add-service=http` | **不立刻** | ✅ 保留 |\n"
            "| 两条都写（推荐）| 立刻 + 保留 | ✅ |\n\n"
            "**怎么验证**：\n"
            "```bash\n"
            "sudo firewall-cmd --list-services            # 当前运行时\n"
            "sudo firewall-cmd --permanent --list-services  # 永久配置\n"
            "sudo firewall-cmd --list-all                  # 综合视图（含 zone）\n"
            "```\n\n"
            "**Workstation 的一个现实**：Fedora Workstation 的默认区域"
            "**已经放行了 ssh**，所以 `--add-service=ssh` 是多余的 —— "
            "先 `--list-services` 看一眼再决定要不要加。"),
        tags=["firewall-cmd", "permanent", "reload", "第 09 讲"], difficulty=3,
    ))

    add(mc(
        "改 sshd_config 的正确流程",
        "你想改 SSH 端口并禁用密码登录。改完 `/etc/ssh/sshd_config` 之后，"
        "正确的下一步是？",
        ["直接 systemctl restart sshd",
         "先 sudo sshd -t 校验语法，再 systemctl reload sshd",
         "直接 reboot",
         "不用做什么，自动生效"],
        "B",
        subject=SUBJ, section=s9,
        explanation=(
            "**先校验、再重载 —— 顺序不能颠倒。**\n\n"
            "```bash\n"
            "sudo sshd -t                    # ★ 只做语法检查，不改变任何东西\n"
            "sudo systemctl reload sshd      # 校验通过才重载\n"
            "```\n\n"
            "★ **为什么必须校验**：`sshd_config` **错一个字符**"
            "（比如把 `Port` 打成 `Prot`，或者漏个引号），"
            "`restart` 就会**直接失败**。而你多半是**通过 SSH 连过去改的** —— "
            "服务一停，你的连接断了，**再也连不回去**，只能去机房（或虚拟化控制台）救。\n\n"
            "**`reload` 而不是 `restart`**：\n"
            "| | 行为 |\n"
            "|---|---|\n"
            "| `restart` | **停掉再起** —— 现有连接全断 |\n"
            "| **`reload`** | 重新读配置，**现有连接不受影响** |\n\n"
            "（`sshd` 的 reload 会优雅处理：老连接保持，新连接用新配置。）\n\n"
            "**两个保命习惯**：\n"
            "1. **改 sshd 配置前，先留一个已经登录的会话别关** —— "
            "新会话连不上时，还能用老会话改回来\n"
            "2. **改 PAM 之前更要留 root 会话** —— PAM 配错会让**所有账号**"
            "（图形 + SSH）都登不进去，只能进单用户模式救援"),
        tags=["sshd_config", "sshd -t", "reload", "第 09 讲"], difficulty=4,
    ))

    add(mc(
        "pam_tally2 在新系统上还能用吗",
        "你想做「登录失败多次就锁定账号」，照老教程配 `pam_tally2`。"
        "在 Fedora 44 上会怎样？",
        ["正常生效",
         "pam_tally2 已被移除，要用 pam_faillock（authselect enable-feature with-faillock）",
         "要装 pam-tally2 包",
         "参数要改成新格式"],
        "B",
        subject=SUBJ, section=s9,
        explanation=(
            "**`pam_tally2` 已经被移除**，新系统用 **`pam_faillock`**。\n\n"
            "```bash\n"
            "sudo authselect enable-feature with-faillock\n"
            "```\n\n"
            "★ **用 `authselect` 而不是直接改 PAM 文件** —— 这是 Fedora 28+ 的规矩：\n"
            "```\n"
            "你在 /etc/pam.d/system-auth 里手改的内容\n"
            "        ↓\n"
            "下一次 authselect 一跑，全被覆盖掉\n"
            "```\n"
            "正路是 `authselect enable-feature ...`，"
            "它会帮你把改动**生成**进配置文件。\n\n"
            "**第 09 讲列的 PAM 相关变更（都是「老教程不适用了」的例子）**：\n\n"
            "| 老写法 | 现在的做法 |\n"
            "|---|---|\n"
            "| 手改 `/etc/pam.d/system-auth` | `authselect enable-feature` |\n"
            "| `pam_tally2` | **`pam_faillock`** |\n"
            "| 改 `/etc/login.defs` 的 `PASS_MIN_LEN` 限密码长度 | **此项已废弃**，"
            "密码长度由 `pam_pwquality` 管 |\n\n"
            "**另一个反直觉的点**（`pam_pwquality` 的配置）：\n"
            "```\n"
            "dcredit = -1     # 负数是「至少 N 个」，不是「减分」\n"
            "                 # 所以 -1 = 至少要有 1 个数字\n"
            "ucredit = 1      # 正数是「有就加分」\n"
            "```\n"
            "**正负含义和直觉相反** —— 这是第 09 讲点名的坑。"),
        tags=["pam", "authselect", "faillock", "第 09 讲"], difficulty=5,
    ))

    add(tf(
        "setenforce 0 是不是解决方案",
        "服务被 SELinux 拦住了，执行 `setenforce 0` 让它跑起来，问题就解决了。",
        False,
        subject=SUBJ, section=s9,
        explanation=(
            "**错**。`setenforce 0` 只是**诊断手段**，不是解决方案。\n\n"
            "**它做了什么**：把 SELinux 从 `enforcing`（强制执行）"
            "临时切到 `permissive`（只记录不阻止）。\n\n"
            "**两个问题**：\n"
            "1. **它只是把防盗门拆了** —— 程序的问题一个都没解决，"
            "只是不再被拦了。攻击面反而变大了\n"
            "2. **它是临时的** —— 重启就恢复成 `enforcing`，"
            "到时候同样的问题会**再冒出来一次**，而你可能已经忘了是为什么\n\n"
            "**正确流程**：\n"
            "```bash\n"
            "# ① 先看看到底在拦什么\n"
            "sudo ausearch -m avc -ts recent\n"
            "sudo journalctl -t setroubleshoot\n"
            "\n"
            "# ② 针对性放行（三选一，按场景）\n"
            "sudo setsebool -P httpd_can_network_connect on      # 布尔开关\n"
            "sudo semanage fcontext -a -t httpd_sys_content_t \"/srv/www(/.*)?\"  # 文件标签\n"
            "sudo semanage port -a -t http_port_t -p tcp 8080    # 端口标签\n"
            "sudo restorecon -Rv /srv/www\n"
            "```\n\n"
            "**`setenforce 0` 什么时候可以用**：\n"
            "- **验证「这个故障是不是 SELinux 引起的」** —— 如果切到 permissive 就好了，"
            "那基本确认是它\n"
            "- 然后**切回 enforcing**（`sudo setenforce 1`），再按上面的方式正式修\n\n"
            "★ **用 `ausearch` 别忘了 sudo** —— 审计日志属 root，"
            "普通用户跑会**空输出**，然后你就会误判成「没有 AVC 记录」。"),
        tags=["setenforce", "SELinux", "诊断", "第 09 讲"], difficulty=3,
    ))

    # ---------- 第 10 讲 ----------
    s10 = "第 10 讲 · Linux 系统的定制"

    add(mc(
        "make install 之后为什么 GRUB 里没有新内核",
        "你编译完内核，跑了 `make install`，屏幕上最后出现一句：\n\n"
        "```\n"
        "Cannot find LILO.\n"
        "```\n\n"
        "重启后 GRUB 菜单里**没有新内核**。为什么？",
        ["编译失败了",
         "make install 在 Fedora 上不会建启动项 —— 它是给 LILO 时代写的",
         "要 sudo 才行",
         "GRUB_TIMEOUT 太短看不见"],
        "B",
        subject=SUBJ, section=s10,
        explanation=(
            "**`make install` 在 Fedora 上装不出启动项** —— 那句 "
            "`Cannot find LILO.` 就是证据。\n\n"
            "**LILO 是什么**：一个**上世纪**的引导程序，早就被 GRUB 取代了。"
            "内核源码树的 `make install` 目标还是按老流程写的："
            "先找 LILO，找不到就打印这句，然后**默默结束**（不报错、不退出非零）。\n\n"
            "**更麻烦的是它还会把文件拷乱**：\n"
            "`make install` 会把内核拷成 **`/boot/vmlinuz`（不带版本号）**，"
            "还会把原来的 `/boot/vmlinuz` 挪成 `vmlinuz.old` —— "
            "这套**没版本号**的命名体系会破坏 Fedora 原有的"
            "`vmlinuz-<版本>` 结构，日后排查内核问题时一片混乱。\n\n"
            "**正确做法（Fedora 的两条正路）**：\n\n"
            "**① 用 `kernel-install`**（推荐）\n"
            "```bash\n"
            "sudo make modules_install\n"
            "sudo kernel-install add <版本号> /path/to/bzImage\n"
            "# 它会自动生成 initramfs（经 50-dracut.install 钩子）\n"
            "# 并在 /boot/loader/entries/ 下建好 BLS 条目 → GRUB 里就有了\n"
            "```\n\n"
            "**② 打成 RPM**（最规范，可被 dnf 管理）\n"
            "```bash\n"
            "fedpkg local     # 产出 kernel-*.rpm，然后 dnf install 它\n"
            "```\n\n"
            "**验证**：`sudo grubby --info=ALL` 看有没有你的版本。"),
        tags=["内核编译", "make install", "kernel-install", "第 10 讲"], difficulty=5,
    ))

    add(tf(
        "编译内核该用哪个用户",
        "编译内核需要用 root 身份，否则会有权限问题。",
        False,
        subject=SUBJ, section=s10,
        explanation=(
            "**错，正好相反：编译要用普通用户，只有最后安装才 sudo。**\n\n"
            "**为什么不能全程 root**：编译过程中会生成**几万个中间文件**，"
            "如果全程 root，这些文件**属主全是 root**。后果：\n"
            "- 之后你用普通用户想清理、重新配置，处处 `Permission denied`\n"
            "- 想删掉整个源码目录都得 `sudo rm -rf`\n"
            "- 一次踩坑，后面每一步都被卡\n\n"
            "**正确分界**：\n"
            "```bash\n"
            "# 普通用户身份做这些\n"
            "cp /boot/config-$(uname -r) .config\n"
            "make olddefconfig\n"
            "make -j2\n"
            "\n"
            "# 只有这两步 sudo\n"
            "sudo make modules_install\n"
            "sudo kernel-install add ...\n"
            "```\n\n"
            "★ **顺带两个编译相关的准备**（第 10 讲的必查项）：\n\n"
            "| 准备 | 要求 | 不满足会怎样 |\n"
            "|---|---|---|\n"
            "| **磁盘空间** | `/` 留 **25~30 GB**，`/boot` 留 500 MB | "
            "编到 80% 报 `No space left on device`，**全部白干** |\n"
            "| **内存** | ≤ 4 GB 用 **`-j2`**，别 `-j$(nproc)` | "
            "`gcc: fatal error: Killed signal terminated program cc1` —— "
            "★ **看着像代码错，其实是 OOM 被杀了** |\n\n"
            "（`make -j$(nproc)` 在内存不够的机器上是经典陷阱："
            "并行度按 CPU 核数算，但 GCC 每个进程都吃几百 MB 内存。）"),
        tags=["内核编译", "权限", "-j2", "第 10 讲"], difficulty=4,
    ))

    add(mc(
        "编译内核第一步该做什么",
        "你下载了内核源码，解压后进了目录。**配置菜单（menuconfig）之前**"
        "第一步应该做什么？",
        ["直接 make menuconfig，从头配",
         "cp /boot/config-$(uname -r) .config 然后 make olddefconfig",
         "先 make mrproper",
         "先 make modules_install"],
        "B",
        subject=SUBJ, section=s10,
        explanation=(
            "**第一步永远是：拿现有内核的配置当底子。**\n\n"
            "```bash\n"
            "cp /boot/config-$(uname -r) .config      # 用当前能跑的内核配置\n"
            "make olddefconfig                        # 新增项按默认值补上\n"
            "```\n\n"
            "★ **为什么不能从零配**：从 `defconfig` 从零起步，"
            "编出来的内核**能启动，但你的网卡、声卡、无线全没了** —— "
            "甚至直接 panic。因为 `defconfig` 只是个「最小可用」模板，"
            "**不认识你这台机器的硬件**。\n\n"
            "★ **为什么用 `olddefconfig` 而不是 `oldconfig`**：\n"
            "| 命令 | 行为 |\n"
            "|---|---|\n"
            "| `make oldconfig` | 对每个新增选项**逐条问你**（几百个问题）|\n"
            "| **`make olddefconfig`** | 新增项**直接用默认值**，不问你 ✅ |\n\n"
            "「一路瞎回车」用 `oldconfig` 是第 10 讲点名的坑："
            "配置里会混进大量你不知道的默认值，编出来和预期完全不一样。\n\n"
            "★ **`make mrproper` 千万别随便用** —— 它会**连 `.config` 一起删掉**！"
            "想清理编译产物用 **`make clean`**（只删中间文件，保留 `.config`）。\n\n"
            "**配完**：`grep 你的选项 .config` 确认改动真的写进去了"
            "（改了 menuconfig 忘了保存也是常见坑）。"),
        tags=["内核配置", "olddefconfig", "第 10 讲"], difficulty=4,
    ))

    add(mc(
        "编译到 80% 报 Killed signal terminated program cc1",
        "编译内核时突然报：\n\n"
        "```\n"
        "gcc: fatal error: Killed signal terminated program cc1\n"
        "```\n\n"
        "看起来像编译器崩了。真实原因最可能是？",
        ["代码有语法错误",
         "内存不足，cc1 被 OOM killer 杀了",
         "gcc 版本太老",
         "硬盘坏了"],
        "B",
        subject=SUBJ, section=s10,
        explanation=(
            "**内存不足，`cc1` 进程被 OOM killer 杀了。**\n\n"
            "★ **这个报错极具迷惑性**：它打着 `gcc: fatal error` 的旗号，"
            "看着像「代码写错了」，实际是**系统内存不够** —— "
            "内核的 OOM killer 把占内存最多的 `cc1`（GCC 的编译进程）干掉了。\n\n"
            "**怎么确认**：\n"
            "```bash\n"
            "free -h                    # 看 available\n"
            "dmesg | grep -i 'killed process'   # ★ 能看到 OOM 的记录，证据确凿\n"
            "```\n\n"
            "**怎么解决**：\n"
            "```bash\n"
            "make -j2                   # ★ 降低并行度（每个编译进程吃几百 MB）\n"
            "# 内存 ≤ 4 GB 就别用 -j$(nproc)\n"
            "```\n\n"
            "★ **`-j$(nproc)` 为什么危险**：它按**CPU 核数**开并行任务。"
            "8 核就同时跑 8 个编译进程 —— 每个吃 500 MB 就是 4 GB。"
            "再加上系统本身的开销，16 GB 的机器都可能被压垮。\n\n"
            "**配套的另一个编译前检查**（第 10 讲 A 组第 1 条）：\n"
            "```bash\n"
            "df -h /        # ★ / 要留 25~30 GB\n"
            "df -h /boot    # ★ /boot 要留 500 MB\n"
            "```\n"
            "空间不够的表现是「编到 80% 报 `No space left on device`」—— "
            "同样是**全部白干**，而且是最气人的一种失败。"),
        tags=["内核编译", "OOM", "-j2", "第 10 讲"], difficulty=4,
    ))

    add(mc(
        "uname -r 没变，是编译失败了吗",
        "你编译安装了新内核，重启后 `uname -r` 显示的还是旧版本号。"
        "说明编译失败了？",
        ["是的，要重新编译",
         "不一定 —— 新内核可能装了，但默认启动项还是旧的",
         "是因为没跑 depmod",
         "是因为没生成 initramfs"],
        "B",
        subject=SUBJ, section=s10,
        explanation=(
            "**不一定。最常见的原因是「新内核装了，但默认启动项没切过去」。**\n\n"
            "**先确认新内核到底装上没**：\n"
            "```bash\n"
            "sudo grubby --info=ALL              # ★ 列出所有启动项，看有没有你的版本\n"
            "ls /boot/vmlinuz-*                  # 看文件在不在\n"
            "ls /lib/modules/                    # 看模块目录有没有新版本\n"
            "ls /boot/loader/entries/            # Fedora 的 BLS 启动条目\n"
            "```\n\n"
            "**如果在，就手动切默认启动项**：\n"
            "```bash\n"
            "sudo grubby --set-default /boot/vmlinuz-<完整版本号>\n"
            "```\n"
            "★ **必须用 `grubby --info=ALL` 输出里的完整 kernel 路径** —— "
            "写个不带版本号的名字 grubby 找不到，会报错或者干脆没反应。\n\n"
            "**另外两个「看起来像失败」的正常现象**：\n"
            "| 现象 | 真相 |\n"
            "|---|---|\n"
            "| GRUB 菜单一闪而过，来不及选 | `GRUB_TIMEOUT` 是 0。"
            "改 `/etc/default/grub` 调到 5 秒以上，再 `grub2-mkconfig` |\n"
            "| 新内核起来了，但硬件大面积失效 | `make modules_install` 忘了跑 → "
            "`ls /lib/modules/<版本>/` 是空的 |\n\n"
            "★ **一条不能违背的规矩**：`installonly_limit` **保持默认值 3**。"
            "调成 1 的话，装新内核时**旧内核被自动删掉** —— "
            "一旦新内核有问题，你就**没有任何退路**了。\n"
            "查：`dnf config-manager getopt installonly_limit`"),
        tags=["内核", "grubby", "启动项", "第 10 讲"], difficulty=5,
    ))


# ===================================================================== #
#  组装 & 落盘
# ===================================================================== #
HEADER = '''"""Linux 线题库 —— **自动生成，不要手改**。

本文件由 `tools/gen_linux_bank.py` 产出，重新生成：

    python tools/gen_linux_bank.py

题源（全部已核实）
------------------
1. 课程下发的《基础命令部分》—— ★ 那份提纲有 **6 处写法会把人带偏**
   （`-Z`/`-z`、`-V`/`-v`、`-C`/`-c`、`head -n +N`、`cat -n` 当数行、`ls [0-9]`），
   本文件逐条出了题。
2. 《Linux基础命令》讲义的 **A 组（认命令）/ B 组（写命令）/ C 组（找错）**。
3. 课程下发的 4 份实验 PDF（实验 2/3/4 各 10 题）—— 抽每题的关键考点。
4. 第 01 ~ 10 讲讲义里的核心概念。

题目形态
--------
全部是**理论题**（`line = "text"`）：选择题 / 判断题 / 命令填空。
提交内容即答案，不启子进程 —— 由 `app/judge/runner_text.py` 归一化后，
交给 `oneof` checker 按「多个可接受答案」比对。

填命令题的宽容度（`app/judge/compare.py` 的 `_norm_cmd`）
- 空白多少无所谓
- `-l -a` 与 `-la` 等价
- `-la` 与 `-al` 等价（短选项簇内字母排序去重）
- 带参数的选项（`-n 50`、`-k2`）和长选项（`--permanent`）**不参与**归一化

**注意：所有理论题的用例 `is_sample` 恒为 0。**
样例会在静态站里原样公开，对选择题来说那就是把答案印在题面上。
"""
from __future__ import annotations

LINUX_PROBLEMS: list[dict] = '''


def build() -> list[dict]:
    PROBLEMS.clear()
    part_fix_six()
    part_a_group()
    part_b_group()
    part_c_group()
    part_experiments()
    part_lectures_a()
    part_lectures_b()
    return list(PROBLEMS)


def _dump(probs: list[dict]) -> str:
    body = json.dumps(probs, ensure_ascii=False, indent=4)
    body = (body.replace(": null", ": None")
                .replace(": true", ": True")
                .replace(": false", ": False"))
    return HEADER + body + "\n"


def _sanity(probs: list[dict]) -> list[str]:
    bad: list[str] = []
    seen: set[str] = set()
    for i, p in enumerate(probs, 1):
        t = p["title"]
        if t in seen:
            bad.append("[%d] 标题重复：%s" % (i, t))
        seen.add(t)
        if p["line"] != "text":
            bad.append("[%d] %s 的 line 不是 text" % (i, t))
        for k in ("statement_md", "source_section", "reference_solution", "cases"):
            if not p.get(k):
                bad.append("[%d] %s 缺字段 %s" % (i, t, k))
        if p["checker"] != "oneof":
            bad.append("[%d] %s 的 checker 不是 oneof" % (i, t))
        for c in p["cases"]:
            if c.get("is_sample"):
                bad.append("[%d] %s 有样例点 —— 理论题的样例会把答案公开" % (i, t))
            if not (c.get("expected_stdout") or "").startswith("|"):
                bad.append("[%d] %s 的期望值没有 | 前缀（oneof 格式）" % (i, t))
    return bad


def main() -> int:
    ap = argparse.ArgumentParser(description="生成 Linux 线题库")
    ap.add_argument("--check", action="store_true", help="只校验，不写文件")
    args = ap.parse_args()

    probs = build()
    kinds = {"mc": 0, "tf": 0, "fill": 0}
    for p in probs:
        if p.get("choices"):
            kinds["mc" if p["choices"] != ["对", "错"] else "tf"] += 1
        else:
            kinds["fill"] += 1

    print("题目数：%d    总分：%d" % (len(probs), sum(p["total_score"] for p in probs)))
    print("选择 %d / 判断 %d / 填空 %d" % (kinds["mc"], kinds["tf"], kinds["fill"]))
    secs: dict[str, int] = {}
    for p in probs:
        secs[p["source_section"]] = secs.get(p["source_section"], 0) + 1
    for s, n in secs.items():
        print("   %-26s %d 题" % (s, n))

    bad = _sanity(probs)
    if bad:
        print("★ 自检不通过：")
        for b in bad:
            print("   " + b)
        return 1
    print("自检通过 ✅")

    if args.check:
        return 0

    OUT_PATH.write_text(_dump(probs), encoding="utf-8", newline="\n")
    print("已写入 %s（%d 字节）" % (OUT_PATH, OUT_PATH.stat().st_size))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
