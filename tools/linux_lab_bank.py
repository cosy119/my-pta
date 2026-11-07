"""Linux 实验报告题库（上）—— 实验 2~5，共 35 题。

## 为什么单独一个文件

`gen_linux_bank.py` 里的 `part_experiments()` 只有 17 道「照实验指导书改编」的
场景题，标题是自拟的，学生对着实验报告一题一题找**对不上号**。
这个文件按**实验报告原题号**出，标题统一 `实验 N-M`，
学生做完实验报告第几题，就能在题库里找到第几题。

## 出题口径

* **单命令题**（`multi=False`）：拿一条命令解决一件事，跟命令族题一样。
* **多步任务**（`multi=True`）：实验报告一题里本来就有 3~5 个动作。
  一行一条命令，答案给「换行版」和「分号版」两种写法，两种都认。

★ 判分仍然是**文本等价比对**（`app/judge/compare.py`）：
  空白折叠 / 短选项重排 / `~/x` ≡ `/home/你/x` / 引号有无。
  多步题的分号与换行不是一回事 —— 所以两种都列进答案，别只列一种。

★ `sudo` 必须写：实验报告里的题目凡是动系统目录（`/usr`、`/etc`、`/boot`）
  都要求提权。判分不执行命令，但**写不写 sudo 是这道题要考的点之一**。

## 与 `linux_cmd_bank.py` 的分工

* `linux_cmd_bank.py` —— 按**命令族**出题（find 一族 16 题、grep 一族 22 题…），
  练的是「这个命令还有什么参数」。
* 本文件 —— 按**实验报告**出题，练的是「这次实验我到底做了哪几步」。
  两者会重复覆盖同一批命令，这是**故意**的：同一个知识点换两种考法。
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.bank_kit import SCORE_COMMAND, practical                    # noqa: E402

SUBJ = "linux"

S2 = "实验 2 · 基本命令"
S3 = "实验 3 · 常用命令"
S4 = "实验 4 · 综合命令"
S5 = "实验 5 · 用户与权限"

MULTI_TIP = "多步任务：一行一条命令，按实验报告的顺序写（Shift+回车 换行）；分号写法也认"


def L(sec: str, title: str, stem: str, answers: list[str], *,
      exp: str, tags: list[str], diff: int = 2, hint: str = "",
      multi: bool = False) -> dict:
    return practical(
        title, stem, answers,
        subject=SUBJ, section=sec,
        explanation=exp, tags=tags,
        difficulty=diff,
        total_score=SCORE_COMMAND + (4 if multi else 0),
        hint=hint,
        input_format=MULTI_TIP if multi else "")


def part_exp2() -> list[dict]:
    out: list[dict] = []

    out.append(L(
        S2, "实验 2-1 绝对路径进目录，再用相对路径回两级",
        "**实验 2 第 1 题。**\n\n"
        "用 `cd` 以**绝对路径**进入 `/usr/local/bin` 并查看该目录内容；"
        "然后用**相对路径**回到 `/usr` 并查看该目录内容。\n\n"
        "（把这两步写出来。不要写 `pwd` —— 题目没有要求打印路径。）",
        ["cd /usr/local/bin\nls\ncd ../..\nls",
         "cd /usr/local/bin; ls; cd ../..; ls"],
        exp=(
            "`cd /usr/local/bin` → `ls` → `cd ../..` → `ls`。\n\n"
            "★ 关键在 `../..`：`bin` 的上一级是 `local`，再上一级才是 `usr`，"
            "所以是**两级**。写成 `cd ..` 会停在 `/usr/local`。\n\n"
            "★ `..` 是「上一级目录」的硬链接，每个目录都有，由内核维护，"
            "不是谁建出来的。`cd ../..` 等价于 `cd /usr`，但题目要的是**相对路径**，"
            "所以不能写绝对路径。"),
        tags=["cd", "相对路径", "..", "实验2"], diff=2, multi=True))

    out.append(L(
        S2, "实验 2-2 连隐藏文件一起看根目录",
        "**实验 2 第 2 题。**\n\n使用 `ls` 查看根目录下的**所有**文件（包含隐藏文件）。",
        ["ls -a /"],
        exp=(
            "`ls -a /`。\n\n"
            "`-a` = all，把以 `.` 开头的隐藏文件也列出来。\n\n"
            "★ 这题**不要**写 `-l`：题目只说「查看所有文件」，没要长格式。"
            "`ls -la /` 能跑，但多答了不是题目要求的东西 —— 实验报告里对齐题目要求是习惯，"
            "题库判分时也把 `ls -la /` 算作等价（见 `compare._norm_cmd` 的短选项簇处理）。\n\n"
            "★ 根目录下的隐藏项很少：`/` 通常是 `.`、`..`、`.autorelabel`（装过 SELinux 重打标签）"
            "这几个，真正的大头在 `/etc` 和各家目录里。"),
        tags=["ls", "-a", "隐藏文件", "实验2"], diff=1))

    out.append(L(
        S2, "实验 2-3 主目录有什么",
        "**实验 2 第 3 题。**\n\n"
        "切换到普通用户的主目录，并查看主目录下有哪些文件。",
        ["cd ~\nls -a", "ls -a ~"],
        exp=(
            "`cd ~` 然后 `ls -a`；或者一步 `ls -a ~`。\n\n"
            "★ `~` 是 shell 的**波浪号展开**：在命令交给程序之前，bash 会把它换成 `$HOME`。"
            "所以 `ls ~` 和 `ls /home/你的名字` 是一回事 —— 题库判分把这两种写法折成同一个"
            "（`compare._norm_home`）。\n\n"
            "★ 主目录下那几个点开头的目录（`.config`、`.cache`、`.local`）是桌面环境自己建的，"
            "删了会丢应用配置，别当垃圾清。"),
        tags=["cd", "~", "ls", "实验2"], diff=1, multi=True))

    out.append(L(
        S2, "实验 2-4 连下三级，再一级一级往回走",
        "**实验 2 第 4 题。**\n\n"
        "先切到 `/usr/local/share/applications` 并查看内容；"
        "用相对路径切到 `local` 并查看；"
        "再用相对路径切到 `share` 并查看。",
        ["cd /usr/local/share/applications\nls\ncd ../..\nls\ncd share\nls",
         "cd /usr/local/share/applications; ls; cd ../..; ls; cd share; ls"],
        exp=(
            "`cd /usr/local/share/applications` → `ls` → `cd ../..` → `ls` → `cd share` → `ls`。\n\n"
            "★★ 这题的机关在最后一步：`share` 就在 `/usr/local` **下面**，所以是 `cd share`。\n"
            "如果顺着前面 `cd ../..` 的惯性写 `cd ../share`，你会到 `/usr/share` —— "
            "**那个目录真实存在，不会报错**，所以特别容易蒙混过关。\n\n"
            "★ 自查办法：`pwd`。题目没要求打印路径，所以答案里不写它，"
            "但你自己做实验时该敲一下确认。"),
        tags=["cd", "相对路径", "陷阱", "实验2"], diff=3, multi=True))

    out.append(L(
        S2, "实验 2-5 日志目录的长格式全清单",
        "**实验 2 第 5 题。**\n\n"
        "查看 `/var/log` 下的所有文件（含隐藏文件），**以长格式**显示。",
        ["ls -la /var/log"],
        exp=(
            "`ls -la /var/log`。\n\n"
            "`-l` 长格式（权限、属主、大小、时间、名字），`-a` 含隐藏文件，"
            "两个一起写就是这题的最小答案。\n\n"
            "★ 长格式里第一列那串 `-rw-r--r--.` 末尾的**点**是 SELinux 安全上下文标记，"
            "Fedora 默认开着 SELinux 才有；`+` 表示带 ACL。\n\n"
            "★ Fedora 的 `/var/log` 里持久化日志没几条 —— 大头被 `journald` 收进了"
            "二进制日志（`journalctl` 查看），不再往文本文件里写。"),
        tags=["ls", "-l", "-a", "var/log", "实验2"], diff=2))

    out.append(L(
        S2, "实验 2-6 用重定向把目录清单存成文件，再带行号看",
        "**实验 2 第 6 题。**\n\n"
        "把 `/usr/local` 目录下的文件名**重定向**到主目录的 `test1.txt`；"
        "然后用 `cat` 查看 `test1.txt` 的内容并**显示行号**。",
        ["ls /usr/local > ~/test1.txt\ncat -n ~/test1.txt",
         "ls /usr/local > ~/test1.txt; cat -n ~/test1.txt",
         "ls /usr/local > test1.txt\ncat -n test1.txt"],
        exp=(
            "`ls /usr/local > ~/test1.txt` → `cat -n ~/test1.txt`。\n\n"
            "★ `>` 是**覆盖**重定向（先截断再写），`>>` 是追加。写错成 `>>` 多做几次实验，"
            "文件里就会堆出几份重复清单。\n\n"
            "★ `cat -n` 显示行号；`cat -b` 只给非空行编号，这两个别混。\n\n"
            "★ 行数对得上不对得上可以自查：`ls /usr/local | wc -l` 的数应当和 "
            "`cat -n` 打印的最后一行的编号一致。这一步属于自查，不写进答案。"),
        tags=["重定向", "cat -n", "实验2"], diff=2, multi=True))

    out.append(L(
        S2, "实验 2-7 系统认哪些登录 shell",
        "**实验 2 第 7 题。**\n\n查看当前系统支持哪些 shell 类型。",
        ["cat /etc/shells"],
        exp=(
            "`cat /etc/shells`。\n\n"
            "`/etc/shells` 是「合法登录 shell」白名单：`chsh` 改 shell 时会对照它，"
            "不在名单里的会被拒绝。Fedora 44 上一般是 sh、bash、tmux（有的版本还有 zsh）。\n\n"
            "★ `chsh -l` 也能列，效果一样，但题目问的是「系统支持哪些」，"
            "`cat /etc/shells` 是最直接的答案。"),
        tags=["cat", "/etc/shells", "实验2"], diff=1))

    out.append(L(
        S2, "实验 2-8 我现在的默认 shell 是哪个",
        "**实验 2 第 8 题。**\n\n查看终端当前默认使用的 shell。",
        ["echo $SHELL"],
        exp=(
            "`echo $SHELL`。\n\n"
            "`$SHELL` 是**登录时**写进环境变量的那个 shell 路径，Fedora Workstation 上是 "
            "`/bin/bash`。\n\n"
            "★ 想验证还可以看 `echo $0`（当前这个 shell 进程的名字，显示 `-bash`）或者 "
            "`ps -p $$ -o comm=`。三者的区别：`$SHELL` 是「登记的默认值」，"
            "`$0` 是「现在跑着的这个」。题目问「当前默认」，`$SHELL` 最贴题。"),
        tags=["echo", "SHELL", "环境变量", "实验2"], diff=1))

    out.append(L(
        S2, "实验 2-9 分页看配置文件：more 与 less 各来一遍",
        "**实验 2 第 9 题。**\n\n"
        "分别用 `more` 和 `less` 查看 `/etc/ssh/ssh_config` 的内容（截取部分即可）。",
        ["more /etc/ssh/ssh_config\nless /etc/ssh/ssh_config",
         "less /etc/ssh/ssh_config"],
        exp=(
            "`more /etc/ssh/ssh_config` → `less /etc/ssh/ssh_config`。\n\n"
            "★ 操作差别：`more` 只能往下翻（空格一页、回车一行、`q` 退出）；"
            "`less` 能往回翻（`↑`/`↓`、`b` 上一页、`/关键词` 向下搜、`n` 下一个匹配、`q` 退出）。"
            "`less` 是 `more` 的超集，日常都用 `less`。\n\n"
            "★ 退出 `less` 会**清屏**：要截「翻页中的画面」，得按 `q` 之前截。"),
        tags=["more", "less", "分页", "实验2"], diff=2, multi=True))

    out.append(L(
        S2, "实验 2-10 su 的那个减号：root 与普通用户的家目录分别是哪",
        "**实验 2 第 10 题。**\n\n"
        "切到 root，查看 root 主目录下有哪些文件并打印它的**绝对路径**；"
        "退回普通用户，切到自己的主目录并打印其绝对路径。",
        ["su -\npwd\nls -a\nexit\ncd ~\npwd",
         "su -\npwd\nls -a\nexit\ncd\npwd"],
        exp=(
            "`su -` → `pwd` → `ls -a` → `exit` → `cd ~` → `pwd`。\n\n"
            "★★ **这题的全部机关就是 `su` 后面那个减号：**\n"
            "- `su -`（完整登录）：环境变量整套换掉，`$HOME` 变成 `/root`，落点也在 `/root`，"
            "所以 `pwd` 打 `/root`。\n"
            "- `su`（不带减号）：只换身份**不换环境**，`$HOME` 还是 `/home/你`，"
            "`pwd` 停在原来的目录 —— 打印出来的「root 主目录」彻底是错的。\n\n"
            "★ 这题要「打印绝对路径」，所以此处 `pwd` 是题目要求的，不算多余命令。\n\n"
            "★ Fedora Workstation 装机时默认**不设 root 密码**（走 `sudo`），"
            "真机上要 `su -` 得先 `sudo passwd root` 给 root 设个密码。"),
        tags=["su", "pwd", "root", "实验2"], diff=3, multi=True))

    return out


def part_exp3() -> list[dict]:
    out: list[dict] = []

    out.append(L(
        S3, "实验 3-1 根目录清单落到 sdut1.txt",
        "**实验 3 第 1 题。**\n\n"
        "查看根目录下有哪些文件，把输出重定向到主目录的 `sdut1.txt`，然后查看这个文件的内容。",
        ["ls / > ~/sdut1.txt\ncat ~/sdut1.txt",
         "ls / > ~/sdut1.txt; cat ~/sdut1.txt",
         "ls / > sdut1.txt\ncat sdut1.txt"],
        exp=(
            "`ls / > ~/sdut1.txt` → `cat ~/sdut1.txt`。\n\n"
            "跟实验 2 第 6 题同一套路，只是这次源目录是 `/`、少了个 `-n`。\n\n"
            "★ 一条命令里 `>` 后面的路径**由 shell 展开**，所以 `~/sdut1.txt` 会先变成 "
            "`/home/你/sdut1.txt` 再交给 `ls`。\n\n"
            "★ 重定向的坏习惯要早改：`ls / > /etc/xxx` 这种写错路径的操作，"
            "普通用户因为没有写权限会被挡住 —— 这正是权限体系在保护你。"),
        tags=["重定向", "ls", "cat", "实验3"], diff=2, multi=True))

    out.append(L(
        S3, "实验 3-2 在 /tmp 下建目录，还要一次建出四层",
        "**实验 3 第 2 题。**\n\n"
        "切到 `/tmp`，在那里建目录 `aa`；再建多级目录 `a1/a2/a3/a4`；"
        "最后查看目录是否建好（要能看到层层嵌套）。",
        ["cd /tmp\nmkdir aa\nmkdir -p a1/a2/a3/a4\nls -R a1",
         "cd /tmp; mkdir aa; mkdir -p a1/a2/a3/a4; ls -R a1"],
        exp=(
            "`cd /tmp` → `mkdir aa` → `mkdir -p a1/a2/a3/a4` → `ls -R a1`。\n\n"
            "★★ `mkdir` **不带 `-p` 建不了多级目录**：`mkdir a1/a2` 会报 "
            "`No such file or directory`，因为 `a1` 还不存在。`-p`（parents）"
            "会把整条路径缺的父目录一起建出来，而且**目录已存在也不报错**。\n\n"
            "★ `ls -R` 递归列出，能一眼看到 `a1/a2/a3/a4` 四层。"),
        tags=["mkdir", "-p", "ls -R", "实验3"], diff=2, multi=True))

    out.append(L(
        S3, "实验 3-3 把 /tmp/a1 整棵子树复制到 /usr",
        "**实验 3 第 3 题。**\n\n"
        "把 `/tmp/a1` 目录及其子目录用 `cp` 复制到 `/usr` 下，然后切到 `/usr` 查看是否复制成功。",
        ["sudo cp -r /tmp/a1 /usr/\ncd /usr\nls -R a1",
         "sudo cp -r /tmp/a1 /usr/\ncd /usr\nls a1",
         "cp -r /tmp/a1 /usr/\ncd /usr\nls -R a1"],
        exp=(
            "`sudo cp -r /tmp/a1 /usr/` → `cd /usr` → `ls -R a1`。\n\n"
            "★★ 两个点必须都在：\n"
            "- `-r`：复制目录**必须**递归，不加会报 `omitting directory`。\n"
            "- `sudo`：`/usr` 是 root 的目录（755），普通用户写不进去。\n\n"
            "★ 目标写成 `/usr/`（带斜杠）和 `/usr`（不带）在 `cp` 这里结果一样 —— "
            "都是「把 a1 放进 /usr 里」。真正会咬人的是 `rsync`，它对末尾斜杠非常敏感。"),
        tags=["cp", "-r", "sudo", "实验3"], diff=3, multi=True))

    out.append(L(
        S3, "实验 3-4 在 /etc 里只挑名字含 pass 的",
        "**实验 3 第 4 题。**\n\n"
        "切到 `/etc`，**仅显示**名字里包含 `pass` 的文件。",
        ["cd /etc\nls -d *pass*", "cd /etc; ls -d *pass*", "ls -d /etc/*pass*"],
        exp=(
            "`cd /etc` → `ls -d *pass*`。\n\n"
            "★ 这里的 `*pass*` 是 **shell 通配符**，不是 `ls` 的功能："
            "bash 先把 `*pass*` 展开成 `passwd passwd-` 这些真实文件名，再交给 `ls`。\n"
            "如果没有任何文件匹配，bash 会把 `*pass*` **原样**传给 `ls`，"
            "于是报 `No such file or directory` —— 这是通配符的经典坑。\n\n"
            "★ `-d` 让 `ls` 把目录本身列出来、而不是列它的内容。这题匹配到的都是文件，"
            "但养成 `ls -d */` 的习惯能少踩很多坑。\n\n"
            "★ 也可以 `ls | grep pass`（管道过滤），但题目说「显示文件」，"
            "`ls -d *pass*` 是最贴题的一条。"),
        tags=["ls", "通配符", "grep", "实验3"], diff=3, multi=True))

    out.append(L(
        S3, "实验 3-5 在 /usr/local/games 里建 game1 并打印它的绝对路径",
        "**实验 3 第 5 题。**\n\n"
        "切到 `/usr/local/games`，在那里建新目录 `game1`，切进 `game1`，"
        "并**打印当前所在目录的绝对路径**。",
        ["cd /usr/local/games\nsudo mkdir game1\ncd game1\npwd",
         "cd /usr/local/games; sudo mkdir game1; cd game1; pwd"],
        exp=(
            "`cd /usr/local/games` → `sudo mkdir game1` → `cd game1` → `pwd`。\n\n"
            "★ 系统目录下建东西要 `sudo`：`/usr/local/games` 是 root:root 755，"
            "普通用户没有写权限。\n\n"
            "★ 这里 `pwd` 是**题目要求**的（要打印绝对路径），所以必须写 —— "
            "跟「题目没要求就删掉 pwd」的规矩不冲突。"),
        tags=["mkdir", "pwd", "sudo", "实验3"], diff=2, multi=True))

    out.append(L(
        S3, "实验 3-6 按通配符把 /boot 的内核文件拷进 ~/abc",
        "**实验 3 第 6 题。**\n\n"
        "用 `cp` 把 `/boot` 下所有以 `vmlinuz` 开头的文件拷到主目录的 `abc` 目录"
        "（不存在就先建），然后进去查看是否已复制。",
        ["mkdir -p ~/abc\nsudo cp /boot/vmlinuz* ~/abc/\ncd ~/abc\nls -lh",
         "mkdir -p ~/abc; sudo cp /boot/vmlinuz* ~/abc/; cd ~/abc; ls -lh",
         "mkdir -p ~/abc\ncp /boot/vmlinuz* ~/abc/\ncd ~/abc\nls -lh"],
        exp=(
            "`mkdir -p ~/abc` → `sudo cp /boot/vmlinuz* ~/abc/` → `cd ~/abc` → `ls -lh`。\n\n"
            "★ `mkdir -p` 的 `-p` 让「目录已存在」不报错，这样重复做实验也不会中断。\n\n"
            "★ `/boot` 下的文件大多 **600 root**，普通用户连读都不行，所以必须 `sudo cp`。"
            "这一条没有 sudo 会报 `Permission denied`，是本题最常见的错法。\n\n"
            "★ 通配符 `vmlinuz*` 由 shell 展开成 `vmlinuz-7.1.12-...` 这类真实文件名；"
            "`/boot` 里通常只有一个版本。\n\n"
            "★ `ls -lh` 的 `-h` 把大小显示成人能读的 `13M` 这种。内核映像动辄十几兆，"
            "不换算单位看不出「拷成功了但只拷了一半」。"),
        tags=["cp", "通配符", "sudo", "boot", "实验3"], diff=3, multi=True))

    out.append(L(
        S3, "实验 3-7 建个空文件，交给 vi 改内容",
        "**实验 3 第 7 题。**\n\n"
        "用 `touch` 在主目录建空文件 `hello`，然后用 `vi` 把它改成 "
        "`this is a file of sdut`，再查看内容。",
        ["touch ~/hello\nvi ~/hello", "touch hello\nvi hello"],
        exp=(
            "`touch ~/hello` → `vi ~/hello`。\n\n"
            "★ `touch` **已存在的文件不会清空**，只更新修改时间；这是它和 "
            "`> file`（会截断）最大的差别。\n\n"
            "★ `vi` 的三步是**模式**而不是菜单：\n"
            "1. `i` 进插入模式（左下角出现 `-- INSERT --`），把 `this is a file of sdut` 打进去\n"
            "2. `Esc` 回命令模式\n"
            "3. `:wq` 保存退出（`:w` 只存不退，`:q!` 不存硬退）\n\n"
            "★ `vi` 是交互式程序，题库不执行它，只比对命令 —— "
            "但实验报告里的截图必须是「`cat` 出来是那句话」，所以真机上这一步别省。"),
        tags=["touch", "vi", "实验3"], diff=2, multi=True))

    out.append(L(
        S3, "实验 3-8 echo 写文件，再用分页器看",
        "**实验 3 第 8 题。**\n\n"
        "在主目录用 `echo` 把 `this is my new file` 重定向到文件 `mysdutfile`，"
        "再用 `less`（或 `more`）查看它。",
        ["echo \"this is my new file\" > ~/mysdutfile\nless ~/mysdutfile",
         "echo \"this is my new file\" > ~/mysdutfile\nmore ~/mysdutfile",
         "echo 'this is my new file' > ~/mysdutfile\nless ~/mysdutfile"],
        exp=(
            "`echo \"this is my new file\" > ~/mysdutfile` → `less ~/mysdutfile`。\n\n"
            "★ 这句话里有**空格**，所以必须加引号：不加的话 `echo` 会把五个词都吞下、"
            "但 `>` 重定向只属于最后那个词所在的命令 —— 实际上不加引号 `echo this is my new file > f` "
            "结果也正确（echo 接受多个参数），真正会翻车的是 `var=this is my new file` 这种赋值。\n\n"
            "★ 引号加单还是加双：单引号里的一切都按字面，双引号里 `$` 和 `\\` 仍会被解释。"
            "所以带 `$` 的字符串想原样输出用单引号。"),
        tags=["echo", "重定向", "less", "实验3"], diff=2, multi=True))

    out.append(L(
        S3, "实验 3-9 建了挪到根目录再改名",
        "**实验 3 第 9 题。**\n\n"
        "在 `/usr/local` 下建 `test7`，把它**移动到根目录**；"
        "再把根目录下的 `test7` **改名**为 `test8`；最后查看根目录内容。",
        ["sudo mkdir /usr/local/test7\nsudo mv /usr/local/test7 /\nsudo mv /test7 /test8\nls /",
         "sudo mkdir /usr/local/test7; sudo mv /usr/local/test7 /; sudo mv /test7 /test8; ls /"],
        exp=(
            "`sudo mkdir /usr/local/test7` → `sudo mv /usr/local/test7 /` → "
            "`sudo mv /test7 /test8` → `ls /`。\n\n"
            "★★ **`mv` 同时是「移动」和「改名」**：目标路径不存在时就是改名，"
            "存在且是目录就是往里移。这题两次 `mv` 刚好各演一次。\n\n"
            "★ 每步都要 `sudo`：`/usr/local` 和 `/` 都只有 root 能写。\n\n"
            "★ `mv /usr/local/test7 /` 后面那个 `/` 是目标目录；"
            "写成 `mv /usr/local/test7 /test8` 一步就能到终点，但题目要的是「先移动、再改名」"
            "两个动作，实验报告里要能看到两次操作。"),
        tags=["mv", "重命名", "sudo", "实验3"], diff=3, multi=True))

    out.append(L(
        S3, "实验 3-10 删掉 /test8 并确认删干净",
        "**实验 3 第 10 题。**\n\n"
        "删除根目录下的 `test8` 目录，并查看是否已经删除。",
        ["sudo rm -r /test8\nls / | grep test8",
         "sudo rm -r /test8; ls / | grep test8",
         "sudo rm -rf /test8\nls / | grep test8"],
        exp=(
            "`sudo rm -r /test8` → `ls / | grep test8`。\n\n"
            "★★ 删目录必须 `-r`：`rm /test8` 会报 `Is a directory`。"
            "`rm -rf` 的 `-f` 是「不存在的也不报错」，题目没要求，`-r` 就够。\n\n"
            "★ 第二句用 `grep` 过滤：**没有任何输出**才代表删干净了。"
            "空输出在 shell 里是正常现象，不是命令失败 —— 别把「什么都没有」当报错。\n\n"
            "★ 危险动作提醒：`rm -rf` 一旦手滑写成 `rm -rf / test8`（多一个空格），"
            "就是删全盘。真机上删系统目录前先 `ls -ld` 确认一遍。"),
        tags=["rm", "-r", "grep", "实验3"], diff=3, multi=True))

    return out


def part_exp4() -> list[dict]:
    out: list[dict] = []

    out.append(L(
        S4, "实验 4-1 建目录、打包备份、再解到别处",
        "**实验 4 第 1 题。**\n\n"
        "在 `/usr` 下建目录 `test5`，用 `tar` 压缩备份到主目录的 `test5.tar.gz` 并确认；"
        "再把它解压到 `/usr/local` 并确认。",
        ["sudo mkdir /usr/test5\nsudo tar czvf ~/test5.tar.gz /usr/test5\nls -lh ~/test5.tar.gz\n"
         "sudo tar xzvf ~/test5.tar.gz -C /usr/local\nls -l /usr/local/test5",
         "sudo mkdir /usr/test5; sudo tar czvf ~/test5.tar.gz /usr/test5; ls -lh ~/test5.tar.gz; "
         "sudo tar xzvf ~/test5.tar.gz -C /usr/local; ls -l /usr/local/test5"],
        exp=(
            "`sudo mkdir /usr/test5` → `sudo tar czvf ~/test5.tar.gz /usr/test5` → "
            "`ls -lh ~/test5.tar.gz` → `sudo tar xzvf ~/test5.tar.gz -C /usr/local` → "
            "`ls -l /usr/local/test5`。\n\n"
            "★ 四个字母各管一件事：`c` 创建、`z` gzip 压缩、`v` 显示过程、`f` 指定文件名。"
            "解压时把 `c` 换成 `x`。\n\n"
            "★★ `-C` 必须紧挨着**目标目录**，且要放在包名**后面**："
            "`tar xzvf 包 -C 目录`。写成 `tar -C 目录 xzvf 包` 在某些实现里会被当成另一回事。\n\n"
            "★ 解压出来的路径是 `usr/test5` 还是 `/usr/local/test5`，取决于打包时用的路径写法。"
            "本题打包用的是绝对路径 `/usr/test5`，解压时 GNU tar 会剥掉前导 `/` 并提示 "
            "`Removing leading / from member names`。"),
        tags=["tar", "czvf", "xzvf", "-C", "实验4"], diff=4, multi=True))

    out.append(L(
        S4, "实验 4-2 确认 vim 装没装，再用它写个文件",
        "**实验 4 第 2 题。**\n\n"
        "先确认 `vim` 是否已安装（没装就用 `dnf` 装）；然后到 `/usr/local` 下用 `vim` 新建 "
        "`sdutfile`，内容为 `hellosdut`。",
        ["rpm -q vim-enhanced\nsudo dnf install -y vim\ncd /usr/local\nsudo vim sdutfile",
         "rpm -q vim-enhanced; sudo dnf install -y vim; cd /usr/local; sudo vim sdutfile"],
        exp=(
            "`rpm -q vim-enhanced` → `sudo dnf install -y vim` → `cd /usr/local` → `sudo vim sdutfile`。\n\n"
            "★ `rpm -q 包名` 才是「查本地装没装」的正确姿势，`rpm -qa` 是列全部（再 `| grep vim`）。"
            "已装时 `dnf install` 只会提示 `Nothing to do`，不会坏事。\n\n"
            "★ `dnf install` 的包名是 `vim`（元包），实际装的是 `vim-enhanced`。"
            "用 `rpm -q` 查的时候要查**真实的包名** `vim-enhanced`。\n\n"
            "★ `/usr/local` 普通用户写不进去，所以 `vim` 前面要 `sudo`。"
            "（不想提权就把文件建在自己家目录，这也是实验报告里更省事的做法。）"),
        tags=["rpm", "dnf", "vim", "实验4"], diff=3, multi=True))

    out.append(L(
        S4, "实验 4-3 在根目录挂一个符号链接",
        "**实验 4 第 3 题。**\n\n"
        "在 `/usr/local` 下建目录 `sdutshare`，在**根目录**建一个名为 `myshare` 的"
        "**符号链接**指向它，然后在根目录查看链接是否建好。",
        ["sudo mkdir /usr/local/sdutshare\nsudo ln -s /usr/local/sdutshare /myshare\nls -l / | grep myshare",
         "sudo mkdir /usr/local/sdutshare; sudo ln -s /usr/local/sdutshare /myshare; ls -l / | grep myshare"],
        exp=(
            "`sudo mkdir /usr/local/sdutshare` → `sudo ln -s /usr/local/sdutshare /myshare` → "
            "`ls -l / | grep myshare`。\n\n"
            "★★ `ln -s` 的参数顺序是 **`ln -s <真实目标> <链接名>`** —— 跟 `cp 源 目标` 一致，"
            "但跟中文语序刚好相反，是这题最常写反的地方。写反了会得到一个「指向自己」的死链。\n\n"
            "★ 查链接要看 `ls -l`：软链的第一列是 `l`，最后有 `myshare -> /usr/local/sdutshare` 的箭头。\n\n"
            "★ 软链 vs 硬链：软链是**另一个文件**，存的是目标路径；硬链是**同一个 inode 的第二个名字**，"
            "`ls -l` 里看不出来（只能靠 `ls -i` 的 inode 号相同来认）。"),
        tags=["ln", "-s", "符号链接", "实验4"], diff=4, multi=True))

    out.append(L(
        S4, "实验 4-4 按字典逆序排四行字",
        "**实验 4 第 4 题。**\n\n"
        "主目录下有一个 `mysort1` 文件，四行分别是 `is`、`this`、`excellent`、`my`。"
        "把它按**字典逆序**排序显示。",
        ["sort -r ~/mysort1", "sort -r mysort1"],
        exp=(
            "`sort -r ~/mysort1`。\n\n"
            "★ `-r` = reverse，倒序；不加是升序（`excellent`、`is`、`my`、`this`）。\n\n"
            "★ 逆序结果：`this`、`my`、`is`、`excellent`。\n\n"
            "★ 别和 `sort -n` 混：`-n` 按**数值**排，非数字行会被当成 0 全堆在最前面。"
            "这题全是单词，只能用默认的字典序。\n\n"
            "★ 想**原地**改文件内容要写 `sort -r mysort1 -o mysort1`（或重定向到临时文件再搬回去），"
            "直接 `sort -r f > f` 会把文件清空 —— 重定向在命令执行**之前**就把文件截断了。"),
        tags=["sort", "-r", "逆序", "实验4"], diff=2))

    out.append(L(
        S4, "实验 4-5 输出一句话但不换行",
        "**实验 4 第 5 题。**\n\n"
        "用 `echo` 输出 `hello everyone!`，要求输出之后**不换行**。",
        ["echo -n \"hello everyone!\"", "echo -n 'hello everyone!'", "printf \"hello everyone!\""],
        exp=(
            "`echo -n \"hello everyone!\"`。\n\n"
            "★ `-n` 就是不输出行尾换行。验证办法：`echo -n hi; echo -n there` 会挤在同一行 "
            "`hithere`，而 `echo hi; echo there` 是两行。\n\n"
            "★ `echo -e` 是另一回事：它让 `\\n`、`\\t` 这类**转义**生效，"
            "`echo -e \"a\\nb\"` 会打印两行。两个开关别混。\n\n"
            "★ 更可控的替代是 `printf`（不带 `\\n` 就不换行）。脚本里推荐 `printf`，"
            "因为不同 shell 的 `echo` 对 `-e` 的处理历史上并不统一。"),
        tags=["echo", "-n", "不换行", "实验4"], diff=2))

    out.append(L(
        S4, "实验 4-6 查 grep 的手册页",
        "**实验 4 第 6 题。**\n\n用 `man` 查看 `grep` 命令的使用方法。",
        ["man grep"],
        exp=(
            "`man grep`。\n\n"
            "★ 手册页的分区：1 用户命令、5 文件格式、8 系统管理。`man 5 passwd` 看的是"
            "**文件格式**，`man 1 passwd` 看的才是**命令** —— 同名不同区时用数字指定。\n\n"
            "★ 常用操作跟 `less` 一样（`man` 就是拿 `less` 当分页器）：空格翻页、`/关键词` 搜索、"
            "`q` 退出。\n\n"
            "★ 只想看某个选项：`man grep | grep -A3 -- -E`，或者直接用 `grep --help`。"),
        tags=["man", "grep", "手册", "实验4"], diff=1))

    out.append(L(
        S4, "实验 4-7 解压 Eclipse 并启动它",
        "**实验 4 第 7 题。**\n\n"
        "把下载好的 `eclipse-java-*-linux-gtk-x86_64.tar.gz` 放在 `~/下载` 里。"
        "解压它、进入解压出的 `eclipse` 目录、启动 `./eclipse`。",
        ["cd ~/下载\ntar xzvf eclipse-java-2026-09-R-linux-gtk-x86_64.tar.gz\ncd eclipse\n./eclipse",
         "cd ~/Downloads\ntar xzvf eclipse-java-2026-09-R-linux-gtk-x86_64.tar.gz\ncd eclipse\n./eclipse"],
        exp=(
            "`cd ~/下载` → `tar xzvf eclipse-java-....tar.gz` → `cd eclipse` → `./eclipse`。\n\n"
            "★ `./eclipse` 前面那个 `./` **不能省**：Linux 默认不把当前目录放进 `PATH`，"
            "直接敲 `eclipse` 会报 `command not found`。这是新手最常卡住的一步。\n\n"
            "★ `tar xzvf` 不写 `-C` 就解到当前目录，包里自带顶层的 `eclipse/` 目录，"
            "所以解完就能 `cd eclipse`。\n\n"
            "★ 想以后随时能启动，加个软链：`sudo ln -s ~/下载/eclipse/eclipse /usr/local/bin/eclipse`。"),
        tags=["tar", "eclipse", "./", "PATH", "实验4"], diff=3, multi=True))

    out.append(L(
        S4, "实验 4-8 两个文件拼成第三个，再一起搬进目录",
        "**实验 4 第 8 题（四小问一次做完）。**\n\n"
        "(a) 主目录建 `file11`、`file12`，内容分别是 `sdut11`、`sdut12`；\n"
        "(b) 建目录 `dir1`；\n"
        "(c) 用 `cat` 让 `dir1/file13` 同时含这两个文件的内容，并查看；\n"
        "(d) 把 `file11`、`file12` 移进 `dir1` 并查看结果。",
        ["cd ~\necho \"sdut11\" > file11\necho \"sdut12\" > file12\nmkdir dir1\n"
         "cat file11 file12 > dir1/file13\ncat dir1/file13\nmv file11 file12 dir1/\nls -l ~/dir1",
         "echo \"sdut11\" > file11\necho \"sdut12\" > file12\nmkdir dir1\n"
         "cat file11 file12 > dir1/file13\ncat dir1/file13\nmv file11 file12 dir1/\nls -l dir1"],
        exp=(
            "`echo \"sdut11\" > file11` → `echo \"sdut12\" > file12` → `mkdir dir1` → "
            "`cat file11 file12 > dir1/file13` → `cat dir1/file13` → "
            "`mv file11 file12 dir1/` → `ls -l dir1`。\n\n"
            "★ `cat a b > c` 是**按顺序拼接**：`file13` 里第一行是 `sdut11`、第二行是 `sdut12`。"
            "顺序写反了内容顺序就反了。\n\n"
            "★★ `mv` 可以**一次搬多个**：最后一个参数必须是**目录**，前面几个是要搬的东西。"
            "`mv file11 file12 dir1/` 合法，`mv file11 file12` 会被当成「file11 改名成 file12」。\n\n"
            "★ 目标末尾那个 `/` 是提示「这是目录」，写不写都行，写了更不容易看错。"),
        tags=["cat", "重定向", "mv", "多文件", "实验4"], diff=3, multi=True))

    out.append(L(
        S4, "实验 4-9 Fedora 装 MySQL 的正确包名",
        "**实验 4 第 9 题。**\n\n"
        "用 `dnf` 在 Fedora 上安装 MySQL，启动服务。"
        "（写出安装与启动这两步的命令即可，登录进去看库是后续操作。）",
        ["sudo dnf install -y mysql-server\nsudo systemctl start mysqld",
         "sudo dnf install -y mysql-server; sudo systemctl start mysqld"],
        exp=(
            "`sudo dnf install -y mysql-server` → `sudo systemctl start mysqld`。\n\n"
            "★★ 两处名字不一样，这是本题唯一但最容易丢分的地方：\n"
            "- **包名**是 `mysql-server`（Fedora 里没有叫 `mysql` 的包）\n"
            "- **服务名**是 `mysqld`（不是 `mysql-server`，也不是 `mysql`）\n\n"
            "★ 在 Debian/Ubuntu 上包名是 `mysql-server`、服务名是 `mysql` —— 教程混着抄就翻车。\n\n"
            "★ Fedora 装完 MySQL 8 会生成一个**临时 root 密码**，在日志里："
            "`sudo grep 'temporary password' /var/log/mysqld.log`。第一次登录要用它，"
            "登录后必须立刻改密码，否则什么都不能做。\n\n"
            "★ 顺手把服务设成开机自启：`sudo systemctl enable mysqld`。"),
        tags=["dnf", "mysql-server", "systemctl", "mysqld", "实验4"], diff=4, multi=True))

    out.append(L(
        S4, "实验 4-10 以 root 身份建目录建文件，再用 ll 看权限",
        "**实验 4 第 10 题。**\n\n"
        "切到 root，在 `/usr/local` 下建目录 `perm`，在 `perm` 里建文件 `newfile`，"
        "用 `ll` 查看该文件的详细信息，然后退回普通用户。",
        ["su -\nmkdir /usr/local/perm\ntouch /usr/local/perm/newfile\nll /usr/local/perm/newfile\nexit",
         "su -\nmkdir /usr/local/perm\ntouch /usr/local/perm/newfile\nls -l /usr/local/perm/newfile\nexit"],
        exp=(
            "`su -` → `mkdir /usr/local/perm` → `touch /usr/local/perm/newfile` → "
            "`ll /usr/local/perm/newfile` → `exit`。\n\n"
            "★ 切到 root 之后**不用再写 sudo** —— 已经是 root 了。\n\n"
            "★ `ll` 是 Fedora 里预先定义好的**别名**（`alias ll='ls -l'`），"
            "在 `~/.bashrc` 或 `/etc/profile.d/` 里。换一个 shell 或换台机器可能就没有，"
            "所以脚本里一律写 `ls -l`，交互时才用 `ll`。\n\n"
            "★ 看到 `-rw-r--r--. 1 root root` 就说明文件属主属组都是 root —— "
            "普通用户之后改不了它，除非 sudo。"),
        tags=["su", "ll", "alias", "touch", "实验4"], diff=3, multi=True))

    return out


def part_exp5() -> list[dict]:
    out: list[dict] = []

    out.append(L(
        S5, "实验 5-1 连建两个用户，切到第一个",
        "**实验 5 第 1 题。**\n\n新建 `user01` 和 `user02` 两个用户，并切换到 `user01`。",
        ["sudo useradd -m user01\nsudo useradd -m user02\nsudo -iu user01",
         "sudo useradd -m user01; sudo useradd -m user02; sudo -iu user01",
         "sudo useradd -m user01\nsudo useradd -m user02\nsu - user01"],
        exp=(
            "`sudo useradd -m user01` → `sudo useradd -m user02` → `sudo -iu user01`。\n\n"
            "★ `-m` 让 `useradd` 建家目录（`/home/user01`）。Fedora 的 `/etc/login.defs` 里 "
            "`CREATE_HOME yes` 其实已经默认建，但实验报告要求显式写，写上是好习惯。\n\n"
            "★ 新建用户**默认没有密码**（`passwd` 那一列是 `!!`），所以 `su - user01` 用不了；"
            "`sudo -iu user01` 靠 sudo 提权过去，不需要密码 —— 实验里推荐这个。\n\n"
            "★ `-iu` = `-i`（模拟完整登录，环境变量整套换）+ `-u 用户`。"),
        tags=["useradd", "-m", "sudo -iu", "实验5"], diff=3, multi=True))

    out.append(L(
        S5, "实验 5-2 在 user01 家目录里建文件与目录",
        "**实验 5 第 2 题。**\n\n（当前身份是 `user01`，在家目录里。）\n\n新建文件 `11.txt` 和目录 `abc`。",
        ["touch 11.txt\nmkdir abc", "touch 11.txt; mkdir abc", "touch ~/11.txt\nmkdir ~/abc"],
        exp=(
            "`touch 11.txt` → `mkdir abc`。\n\n"
            "★ `touch` 建空文件（0 字节）；`mkdir` 建目录。两者创建出来的东西在 `ls -l` 里"
            "第一列分别是 `-` 和 `d`。\n\n"
            "★ 家目录下新建的文件默认权限受 **umask** 影响：Fedora 的 umask 是 `002`，"
            "所以文件是 `664`、目录是 `775`（组内可写）。这也是为什么实验报告里看到的权限"
            "是 `-rw-rw-r--` 而不是 `-rw-r--r--`。"),
        tags=["touch", "mkdir", "umask", "实验5"], diff=1, multi=True))

    out.append(L(
        S5, "实验 5-3 一个文件一个目录的权限分别怎么看",
        "**实验 5 第 3 题。**\n\n查看 `11.txt` 文件和 `abc` 目录的权限。",
        ["ls -l 11.txt\nls -ld abc", "ls -l 11.txt; ls -ld abc"],
        exp=(
            "`ls -l 11.txt` → `ls -ld abc`。\n\n"
            "★★ 查目录本身要 `-d`：不加 `-d` 的 `ls -l abc` 列的是 **abc 里面**的东西，"
            "永远看不到 abc 自己的权限。这是本题唯一的考点。\n\n"
            "★ 目录的 `x` 位含义跟文件不同：对目录来说 `x` 是**能进去**（`cd`）的权限，"
            "`r` 是「能列出里面有什么」，`w` 是「能在里面增删文件」。"
            "所以 `r--` 的目录能看名字但进不去。"),
        tags=["ls", "-d", "权限", "实验5"], diff=2, multi=True))

    out.append(L(
        S5, "实验 5-4 把 11.txt 设成 rwxr-x--x（字符法）",
        "**实验 5 第 4 题（第 1 问）。**\n\n"
        "用**字符表示法**把 `11.txt` 的权限改成 `-rwxr-x--x`，并查看结果。",
        ["chmod u=rwx,g=rx,o=x 11.txt\nls -l 11.txt",
         "chmod u=rwx,g=rx,o=x 11.txt; ls -l 11.txt",
         "chmod u=rwx,g=rx,o=x 11.txt\nls -l 11.txt"],
        exp=(
            "`chmod u=rwx,g=rx,o=x 11.txt` → `ls -l 11.txt`。\n\n"
            "★ 目标权限 `-rwxr-x--x` 拆开看：属主 `rwx`(7)、属组 `r-x`(5)、其他 `--x`(1) → 八进制 **751**。"
            "所以 `chmod 751 11.txt` 也对 —— 两种写法题库都认。\n\n"
            "★★ `=` 是**赋值**，`+`/`-` 是增减。`chmod g=rx` 会把组权限**压成** `r-x`，"
            "哪怕原来有 `w` 也一并去掉；`chmod g+w` 只加不减。实验报告这题要的是 `=`。\n\n"
            "★ 一次写完三段（`u=,g=,o=` 用逗号连）比敲三次清爽，也不会中间态残留。"),
        tags=["chmod", "字符法", "751", "实验5"], diff=3, multi=True))

    out.append(L(
        S5, "实验 5-4b 给其他人加写权限",
        "**实验 5 第 4 题（第 2 问）。**\n\n"
        "用**字符表示法**为**其他用户**增加**可写**权限（文件 `11.txt`），并查看结果。",
        ["chmod o+w 11.txt\nls -l 11.txt", "chmod o+w 11.txt; ls -l 11.txt"],
        exp=(
            "`chmod o+w 11.txt` → `ls -l 11.txt`。\n\n"
            "★ `o` = other（其他用户），`+w` = 加写。`a+w` 是三段全加，跟这题要的不一样。\n\n"
            "★ 加完之后 `--x` 会变成 `-wx`。注意：**给文件加 `w` 不等于对方能删它** —— "
            "删文件看的是**父目录**的 `w` 权限。"),
        tags=["chmod", "o+w", "实验5"], diff=2, multi=True))

    out.append(L(
        S5, "实验 5-4c 把属组的权限设成只有写",
        "**实验 5 第 4 题（第 3 问）。**\n\n"
        "用**字符表示法**把 `11.txt` 的**所属用户组**权限设为 `-w-`，并查看结果。",
        ["chmod g=w 11.txt\nls -l 11.txt", "chmod g=w 11.txt; ls -l 11.txt"],
        exp=(
            "`chmod g=w 11.txt` → `ls -l 11.txt`。\n\n"
            "★ `g=w` 是**赋值**：组权限只剩 `w`，原来的 `r`、`x` 全部清掉。"
            "如果想「只去掉读」，应该写 `chmod g-r`。\n\n"
            "★ 只有 `w`（`-w-`）的目录是个特例：能往里写文件，但**列不出**里面有什么，"
            "因为列目录需要 `r`。"),
        tags=["chmod", "g=w", "实验5"], diff=2, multi=True))

    out.append(L(
        S5, "实验 5-4d 让属主和属组都不能执行",
        "**实验 5 第 4 题（第 4 问）。**\n\n"
        "用字符表示法为文件 `11.txt` 的**拥有者和用户组**取消可执行权限，并查看结果。",
        ["chmod u-x,g-x 11.txt\nls -l 11.txt", "chmod u-x,g-x 11.txt; ls -l 11.txt"],
        exp=(
            "`chmod u-x,g-x 11.txt` → `ls -l 11.txt`。\n\n"
            "★ 两段用逗号连起来一次做完。\n\n"
            "★ `-x` 只去掉**执行**位，读写不动。看结果时盯住第 4 位和第 7 位："
            "`rwx` 变 `rw-`、`r-x` 变 `r--`。\n\n"
            "★ 补一个 `chmod a-x` 就是三段一起去执行位，这里不能这么写 —— "
            "题目只说拥有者和组，其他用户的 `x` 要留着。"),
        tags=["chmod", "u-x", "g-x", "实验5"], diff=2, multi=True))

    out.append(L(
        S5, "实验 5-5 目录连里面的文件一起改属主",
        "**实验 5 第 5 题。**\n\n"
        "在 `abc` 目录里建文件 `22.txt`，然后把 `abc` 及其内部文件的**所属用户和用户组**"
        "都改成 `user02`，并核对。",
        ["cd abc\ntouch 22.txt\ncd ..\nsudo chown -R user02:user02 abc\nls -ld abc",
         "touch abc/22.txt\nsudo chown -R user02:user02 abc\nls -ld abc"],
        exp=(
            "`cd abc` → `touch 22.txt` → `cd ..` → `sudo chown -R user02:user02 abc` → `ls -ld abc`。\n\n"
            "★★ 三个要点：\n"
            "- `-R` 递归：不加只改 `abc` 这一层，里面的 `22.txt` 还是 user01 的。\n"
            "- `用户:组` 一次写两组，中间是**冒号**（老写法是点，`chown user02.user02`，现在也认）。\n"
            "- `sudo` 必须有：把自己的文件送给别人，只有 root 干得成。\n\n"
            "★ 改完之后 `ls -ld abc` 显示 `drwxrwxr-x. 2 user02 user02`；"
            "里面那个 `22.txt` 要用 `ls -l abc` 另外看 —— `-d` 只看目录本身。"),
        tags=["chown", "-R", "user:group", "实验5"], diff=4, multi=True))

    out.append(L(
        S5, "实验 5-6 换 user02 身份在新家目录里建目录建文件",
        "**实验 5 第 6 题。**\n\n"
        "切到 `user02`，在其主目录建目录 `sdutjsj`，进目录建空文件 `sdutfile1`，"
        "用**长格式**查看该文件的信息（权限、属主、属组）。",
        ["sudo -iu user02\nmkdir sdutjsj\ncd sdutjsj\ntouch sdutfile1\nls -l sdutfile1",
         "sudo -iu user02; mkdir sdutjsj; cd sdutjsj; touch sdutfile1; ls -l sdutfile1"],
        exp=(
            "`sudo -iu user02` → `mkdir sdutjsj` → `cd sdutjsj` → `touch sdutfile1` → "
            "`ls -l sdutfile1`。\n\n"
            "★ `sudo -iu` 是**完整登录**：`$HOME` 会变成 `/home/user02`，"
            "所以接着的 `mkdir` 落在 user02 的家目录里。\n\n"
            "★ 建出来的文件属主是 user02、属组是 user02 的**主组**。Fedora 的 `useradd` "
            "默认会建一个同名用户组（UPG，user private group），所以 `user02:user02`。"),
        tags=["sudo -iu", "mkdir", "touch", "ls -l", "实验5"], diff=3, multi=True))

    out.append(L(
        S5, "实验 5-7 放开其他人的写权限",
        "**实验 5 第 7 题。**\n\n"
        "让**其他用户**可以对 `sdutfile1` 进行**写**操作，并查看更改后的结果。",
        ["chmod o+w sdutfile1\nls -l sdutfile1", "chmod o+w sdutfile1; ls -l sdutfile1"],
        exp=(
            "`chmod o+w sdutfile1` → `ls -l sdutfile1`。\n\n"
            "★ 结果从 `-rw-rw-r--` 变成 `-rw-rw-rw-`，最后三位 `r--` → `rw-`。\n\n"
            "★ 想让「所有人都能写」用 `chmod a+w`（等于 `u+w,g+w,o+w`）。"
            "这题只要求 other，写 `a+w` 就多做了一半。"),
        tags=["chmod", "o+w", "实验5"], diff=2, multi=True))

    out.append(L(
        S5, "实验 5-8 收回同组的读权限",
        "**实验 5 第 8 题。**\n\n"
        "取消**同组用户**对 `sdutfile1` 的**读**权限，并查看更改后的结果。",
        ["chmod g-r sdutfile1\nls -l sdutfile1", "chmod g-r sdutfile1; ls -l sdutfile1"],
        exp=(
            "`chmod g-r sdutfile1` → `ls -l sdutfile1`。\n\n"
            "★ 结果从 `-rw-rw-rw-` 变成 `-rw--w-rw-`：第 5 位 `r` 被去掉。\n\n"
            "★★ 注意这里用的是 `-` 而不是 `=`：`chmod g-r` 只删读位、写位留着；"
            "`chmod g=r` 会把组权限**重置**成只有读。这两条命令差一个字符，结果完全不同。"),
        tags=["chmod", "g-r", "实验5"], diff=2, multi=True))

    out.append(L(
        S5, "实验 5-9 八进制 744",
        "**实验 5 第 9 题。**\n\n"
        "用**八进制表示法**设置 `sdutfile1`：属主可读可写可执行，组和其他只有可读。"
        "设置完查看结果。",
        ["chmod 744 sdutfile1\nls -l sdutfile1", "chmod 744 sdutfile1; ls -l sdutfile1"],
        exp=(
            "`chmod 744 sdutfile1` → `ls -l sdutfile1`。\n\n"
            "★ 三位数字各管一段：`7`=rwx（属主）、`4`=r--（组）、`4`=r--（其他），"
            "对应权限串 `-rwxr--r--`。\n\n"
            "★ 数字怎么来的：r=4、w=2、x=1，相加。所以 `rwx`=7、`r-x`=5、`r--`=4、`---`=0。\n\n"
            "★ 第四位（如 `4755`）是特殊位：setuid。实验里不要求，但 `ls -l` 里看到 "
            "`-rwsr-xr-x` 那个 `s` 就是它。"),
        tags=["chmod", "八进制", "744", "实验5"], diff=2, multi=True))

    out.append(L(
        S5, "实验 5-10 八进制 400：只有属主能读",
        "**实验 5 第 10 题。**\n\n"
        "用八进制把 `sdutfile1` 改成：属主**只读**，组和其他**没有任何权限**。设置完查看结果。",
        ["chmod 400 sdutfile1\nls -l sdutfile1", "chmod 400 sdutfile1; ls -l sdutfile1"],
        exp=(
            "`chmod 400 sdutfile1` → `ls -l sdutfile1`。\n\n"
            "★ 结果是 `-r--------`。连属主自己都不能写 —— 想改内容得先 `chmod u+w` 回来。\n\n"
            "★ 400 是 SSH 私钥的标准权限。私钥权限放宽到 644 时 `ssh` 会直接拒绝使用，"
            "就是这个原因。"),
        tags=["chmod", "400", "实验5"], diff=2, multi=True))

    out.append(L(
        S5, "实验 5-11 八进制 402：只给其他人写",
        "**实验 5 第 11 题。**\n\n"
        "用八进制给 `sdutfile1` 的**其他用户**加上**写**权限（属主仍只读、组无权限），"
        "设置完查看结果。",
        ["chmod 402 sdutfile1\nls -l sdutfile1", "chmod 402 sdutfile1; ls -l sdutfile1"],
        exp=(
            "`chmod 402 sdutfile1` → `ls -l sdutfile1`。\n\n"
            "★ 结果是 `-r-----w-`：属主 `r--`(4)、组 `---`(0)、其他 `-w-`(2)。\n\n"
            "★ 这题是在上一题 `400` 的基础上把最后一位从 0 改成 2 —— "
            "所以也可以写 `chmod o+w sdutfile1`，效果完全一样。两种写法都对。\n\n"
            "★ 注意：只有「写」没有「读」其他人是**读不到内容**的，但能改（比如 `echo x >> f`）。"
            "这种权限组合在实际里很少见，实验专门考它是为了让你分清 r 和 w。"),
        tags=["chmod", "402", "实验5"], diff=3, multi=True))

    out.append(L(
        S5, "实验 5-12 建用户 zhangsan 并设密码，最后看 passwd 尾巴",
        "**实验 5 第 12 题。**\n\n"
        "新建用户 `zhangsan`，把密码设成 `123`，然后用 `tail` 查看 `/etc/passwd` 的最后 10 行。",
        ["sudo useradd -m zhangsan\necho 'zhangsan:123' | sudo chpasswd\ntail -n 10 /etc/passwd",
         "sudo useradd -m zhangsan\necho \"zhangsan:123\" | sudo chpasswd\ntail -n 10 /etc/passwd",
         "sudo useradd -m zhangsan\necho 'zhangsan:123' | sudo chpasswd\ntail -10 /etc/passwd"],
        exp=(
            "`sudo useradd -m zhangsan` → `echo 'zhangsan:123' | sudo chpasswd` → "
            "`tail -n 10 /etc/passwd`。\n\n"
            "★ `passwd zhangsan` 是交互式的（要敲两遍密码），脚本/实验报告里用 "
            "`echo '用户:密码' | chpasswd` 更省事，**记得加 sudo**。\n\n"
            "★ `tail -n 10` 和 `tail -10` 等价。默认就是 10 行，所以 `tail /etc/passwd` 也行，"
            "但题目写了「最后 10 行」，显式写出来更贴题。\n\n"
            "★ `/etc/passwd` 每行 7 段：`用户名:x:UID:GID:描述:家目录:登录shell`。"
            "第二段的 `x` 表示真密码在 `/etc/shadow`（普通用户读不到那个文件）。"),
        tags=["useradd", "chpasswd", "tail", "passwd", "实验5"], diff=3, multi=True))

    out.append(L(
        S5, "实验 5-13 建组 sdutstuff，看 group 尾巴",
        "**实验 5 第 13 题。**\n\n新建用户组 `sdutstuff`，然后查看 `/etc/group` 的最后 5 行。",
        ["sudo groupadd sdutstuff\ntail -n 5 /etc/group",
         "sudo groupadd sdutstuff; tail -n 5 /etc/group"],
        exp=(
            "`sudo groupadd sdutstuff` → `tail -n 5 /etc/group`。\n\n"
            "★ `/etc/group` 每行 4 段：`组名:x:GID:成员列表`。新建的组在文件末尾，"
            "所以 `tail` 一定看得到。\n\n"
            "★ 成员列表是逗号分隔的**附加成员**；主组不写在这里（主组在 `/etc/passwd` 的第 4 段）。\n\n"
            "★ `groupadd` 不指定 `-g` 时会自动取一个没用过的 GID（从 `GID_MIN` 往上找）。"),
        tags=["groupadd", "group", "tail", "实验5"], diff=2, multi=True))

    out.append(L(
        S5, "实验 5-14 删组再看 group 尾巴",
        "**实验 5 第 14 题。**\n\n删除用户组 `sdutstuff`，然后查看 `/etc/group` 的最后 5 行。",
        ["sudo groupdel sdutstuff\ntail -n 5 /etc/group",
         "sudo groupdel sdutstuff; tail -n 5 /etc/group"],
        exp=(
            "`sudo groupdel sdutstuff` → `tail -n 5 /etc/group`。\n\n"
            "★ 删完之后那行就没了，`tail` 里自然看不到 —— 这就是「验证删掉了」的方式。\n\n"
            "★ `groupdel` 删不掉「某人的主组」：那样的组在删掉前会报 "
            "`cannot remove the primary group of user ...`。得先给那个用户换主组。"),
        tags=["groupdel", "group", "tail", "实验5"], diff=2, multi=True))

    out.append(L(
        S5, "实验 5-15 把 zhangsan 家目录里的 temp1 改成 root 的",
        "**实验 5 第 15 题。**\n\n"
        "在 `zhangsan` 主目录下建目录 `temp1`，查看它的所属用户与用户组；"
        "然后把它的所属用户与用户组都设为 `root`，再看一遍。",
        ["sudo mkdir -p /home/zhangsan/temp1\nls -ld /home/zhangsan/temp1\n"
         "sudo chown root:root /home/zhangsan/temp1\nls -ld /home/zhangsan/temp1",
         "sudo mkdir -p /home/zhangsan/temp1; ls -ld /home/zhangsan/temp1; "
         "sudo chown root:root /home/zhangsan/temp1; ls -ld /home/zhangsan/temp1"],
        exp=(
            "`sudo mkdir -p /home/zhangsan/temp1` → `ls -ld /home/zhangsan/temp1` → "
            "`sudo chown root:root /home/zhangsan/temp1` → `ls -ld /home/zhangsan/temp1`。\n\n"
            "★★ 这题有个「本来就已经是 root」的坑：用 `sudo mkdir` 建出来的目录，"
            "属主**天然就是 root**。所以第二次 `chown` 看起来什么都没变 —— 但它必须写，"
            "实验报告要的是「显式设置」这个动作和两张截图。\n\n"
            "★ 如果想让 zhangsan 自己拥有它，那要 `sudo chown zhangsan:zhangsan`。"
            "「谁建的归谁」只在使用自己身份时成立，`sudo` 建的一律归 root。\n\n"
            "★ `-p` 让父目录缺失时一起建（这里父目录存在，写不写都行，写上更稳）。"),
        tags=["mkdir", "chown", "-ld", "root", "实验5"], diff=3, multi=True))

    return out


def build() -> list[dict]:
    out: list[dict] = []
    out += part_exp2()
    out += part_exp3()
    out += part_exp4()
    out += part_exp5()
    return out
