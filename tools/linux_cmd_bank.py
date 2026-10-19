"""Linux 命令题库 —— 「给场景，写命令」。

为什么要独立成一个文件
----------------------
命令题是本线的主力（200+ 道），塞进 `gen_linux_bank.py` 会把那个文件撑到
读不动。这里只负责「出题」，`gen_linux_bank.py` 负责合并 + 自检 + 落盘。

出题口径（和旧版「填输出」的区别）
---------------------------------
旧版：做完实验 → 贴验收命令的**输出**。问题是会背答案的人不用会写命令。
新版：题干给**场景与约束** → 提交**命令本身**。判题做文本等价比对
（见 `app/judge/compare.py` 的 `_norm_cmd` / `_norm_home`，
以及 `app/bank_kit.py::_quote_forms` 补的引号变体）。

★ 每族的出题梯度（这就是「举一反三」的落地方式）
1. **基本用法** —— 最朴素的一条
2. **参数组合** —— 加两个选项，考「选哪个参数」
3. **真实场景** —— 不给命令名，只给需求，逼你自己选工具
4. **易错辨析** —— 同族里两个近义命令/参数，选错就废

★ 答案纪律
`answers` 里列的是**语义完全等价**的写法（引号/长短参数/绝对相对路径的
等价形式）。宁可多列，不可漏列 —— 漏一条就是让人白掉一次分。
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.bank_kit import SCORE_COMMAND, practical                    # noqa: E402

SUBJ = "linux"

# 难度 → 分值。命令题比选择题重，比综合实验轻。
SCORE_BY_DIFF = {1: SCORE_COMMAND - 2, 2: SCORE_COMMAND,
                 3: SCORE_COMMAND + 3, 4: SCORE_COMMAND + 6}


def C(title: str, statement_md: str, answers: list[str], *,
      sec: str, exp: str, tags: list[str], diff: int = 2,
      hint: str = "") -> dict:
    """出一道命令题。"""
    return practical(
        title, statement_md, answers,
        subject=SUBJ, section=sec,
        explanation=exp, tags=tags,
        difficulty=diff, total_score=SCORE_BY_DIFF[diff], hint=hint)


# ===================================================================== #
#  一、课程实验 1~5（照实验指导书的步骤，但改成「写命令」）
# ===================================================================== #
def part_experiments() -> list[dict]:
    s1 = "实验 1 · 环境搭建"
    s2 = "实验 2 · 基本命令"
    s3 = "实验 3 · 常用命令"
    s4 = "实验 4 · 综合命令"
    s5 = "实验 5 · 用户与权限"
    out: list[dict] = []

    # ---------------- 实验 1 ----------------
    out.append(C(
        "装完系统，一条命令问出 Fedora 主版本号",
        "**作业 1（装机）**：装好 Fedora Workstation 后，第一件事是确认装的是哪一版。\n\n"
        "要求：只从 `/etc/os-release` 里取出**主版本号那一行**，"
        "输出形如 `VERSION_ID=44`。\n\n"
        "写出这条命令。",
        ["grep ^VERSION_ID= /etc/os-release",
         "grep VERSION_ID= /etc/os-release",
         "grep '^VERSION_ID=' /etc/os-release"],
        sec=s1, diff=2,
        exp=(
            "`grep ^VERSION_ID= /etc/os-release`。\n\n"
            "`/etc/os-release` 是 systemd 定下的**跨发行版标准文件**"
            "（Fedora 上它是指向 `/usr/lib/os-release` 的软链，`grep` 会顺着链读）。"
            "`^` 锚定行首，只捞出 `VERSION_ID=` 开头的那一行。\n\n"
            "★ 为什么不用 `cat /etc/fedora-release` —— 那行写的是 "
            "`Fedora release 44 (Forty Four)`，代号随版本变；"
            "`VERSION_ID` 永远是纯数字，拿来当判据最稳。\n\n"
            "★ **迁移**：任何发行版先 `grep VERSION_ID /etc/os-release`，"
            "比 `lsb_release -a` 靠谱 —— 后者在最小化安装里经常没装。"),
        tags=["实验 1", "os-release", "grep", "装机"]))

    out.append(C(
        "查内核版本（只要版本号，不要整串信息）",
        "你的驱动装不上，厂商让你报**内核版本**。\n\n"
        "要求：只输出内核版本号，形如 `6.8.5-301.fc40.x86_64`，"
        "不要 `Linux hostname ...` 那一整行。\n\n"
        "写出这条命令。",
        ["uname -r", "uname --kernel-release"],
        sec=s1, diff=1,
        exp=(
            "`uname -r`（长写法 `uname --kernel-release`）。\n\n"
            "`uname` 各选项是**各管一段**的，不是「越多越详细」：\n"
            "- `-r` → 内核 release 号（`6.8.x-fc40.x86_64`）\n"
            "- `-a` → 全部信息（内核名 + 主机名 + 版本 + 架构 + …）\n"
            "- `-s` → 只有 `Linux`\n"
            "- `-m` → 架构（`x86_64`）\n\n"
            "★ 报漏洞、报驱动问题时要的是 `-r`；`-a` 那一整行带主机名，"
            "贴到公开场合等于自曝主机名。\n\n"
            "★ **迁移**：`cat /proc/version` 也能看到，但它带编译时间与 gcc 版本，"
            "脚本里要干净的值，还是 `uname -r`。"),
        tags=["实验 1", "uname", "内核"]))

    # ---------------- 实验 2 ----------------
    out.append(C(
        "用相对路径从 /usr/local/bin 退回 /usr",
        "**实验 2 第 1 步**：你现在在 `/usr/local/bin`。\n\n"
        "要求：**不许写绝对路径**，用 `..` 退回 `/usr`。\n\n"
        "写出这条命令（假设起点就是 `/usr/local/bin`）。",
        ["cd ../..", "cd ../../"],
        sec=s2, diff=2,
        exp=(
            "`cd ../..`。\n\n"
            "`/usr/local/bin` 往上走：一次 `..` 到 `/usr/local`，再一次 `..` 到 `/usr`，"
            "所以是**两级**。`cd ../../` 末尾多一个 `/` 也完全等价。\n\n"
            "★ 最常见的错：把 `..` 当成「回根目录」或「回上一个访问过的目录」。"
            "`..` 永远只表示**父目录**，与 shell 的历史无关。\n\n"
            "★ 辨析：`cd -` 才是「回上一次待过的目录」（靠 `$OLDPWD`），"
            "它跟 `..` 是两个完全不同的概念。\n\n"
            "★ **迁移**：路径里连续几层 `..` 都能合并——`a/b/../../c` 等价于 `c`，"
            "写脚本时先化简再传参，能少踩很多「文件找不到」。"),
        tags=["实验 2", "cd", "相对路径"]))

    out.append(C(
        "打印当前所在目录的绝对路径",
        "**实验 2 第 2 步**：连着 `cd` 了好几次，你现在到底在哪？\n\n"
        "要求：输出**绝对路径**（形如 `/usr/local/bin`），不要只显示目录名。\n\n"
        "写出这条命令。",
        ["pwd"],
        sec=s2, diff=1,
        exp=(
            "`pwd`（print working directory）。\n\n"
            "★ 为什么强调「绝对路径」：`pwd` 默认带 `-L`，输出的是**逻辑路径**——"
            "如果你是从软链 `cd` 进去的，它显示软链那条路径。"
            "想要**物理路径**（把软链解析成真实位置）得用 `pwd -P`。\n\n"
            "★ 脚本里的坑：`pwd` 是外部命令，`echo $PWD` 是读 shell 变量。"
            "两者值一般一样，但 `cd` 失败时 `$PWD` 可能没更新——"
            "**判断 `cd` 成没成功，看退出码 `$?`，别信 `$PWD`**。\n\n"
            "★ **迁移**：脚本开头写 `cd \"$(dirname \"$0\")\" || exit 1`，"
            "让脚本总是以自己所在目录为基准，这是最稳的写法。"),
        tags=["实验 2", "pwd", "绝对路径"]))

    # ---------------- 实验 3 ----------------
    out.append(C(
        "一条命令建出 a1/a2/a3/a4 四级目录",
        "**实验 3 第 1 步**：在 `/tmp` 下建一条四层深的目录链 "
        "`a1/a2/a3/a4`。\n\n"
        "要求：**只准用一条 `mkdir`**，不许分开建四次。\n\n"
        "写出这条命令。",
        ["mkdir -p /tmp/a1/a2/a3/a4", "mkdir --parents /tmp/a1/a2/a3/a4"],
        sec=s3, diff=1,
        exp=(
            "`mkdir -p /tmp/a1/a2/a3/a4`。\n\n"
            "`-p`（`--parents`）一个选项干两件事：\n"
            "1. **逐级自动创建**中间的父目录（不用先建 a1 再建 a2…）\n"
            "2. **已存在也不报错**（幂等）\n\n"
            "★ 没 `-p` 会怎样：`mkdir: cannot create directory '/tmp/a1/a2': "
            "No such file or directory` —— 因为父目录还不存在。\n\n"
            "★ 幂等这一点在脚本里价值最大：`mkdir -p /var/log/myapp` 写两遍"
            "也不会失败，所以安装脚本里到处是它。\n\n"
            "★ **迁移**：`mkdir -p a/{b,c,d}` 的花括号展开一次建三个平级目录，"
            "建项目骨架时很省事。"),
        tags=["实验 3", "mkdir", "多级目录"]))

    out.append(C(
        "把整棵目录树复制走，并且保留权限与时间戳",
        "**实验 3 第 2 步**：把 `/tmp/a1`（含下面三层子目录）整个复制到 `/usr`。\n\n"
        "要求：复制完**权限、属主、时间戳都和原来一样**，"
        "符号链接照抄成符号链接（不要跟进去复制目标内容）。\n\n"
        "写出这条命令。",
        ["cp -a /tmp/a1 /usr/", "cp -a /tmp/a1 /usr",
         "cp -a /tmp/a1/ /usr/", "cp -a /tmp/a1/ /usr",
         "cp --archive /tmp/a1 /usr/"],
        sec=s3, diff=3,
        exp=(
            "`cp -a /tmp/a1 /usr/`（`-a` = `--archive`）。\n\n"
            "`-a` 是**一个等于一串**的选项：`-dR --preserve=all`\n"
            "- `-R` 递归\n"
            "- `-d` 不跟随符号链接（链路照抄）\n"
            "- `--preserve=all` 保 权限 + 属主 + 时间戳 + 扩展属性\n\n"
            "★ 别用 `cp -r`：它**不保属主与时间戳**，"
            "也不处理「软链变成实体文件」的问题（不加 `-d` 时 `-r` 会跟进去）。\n\n"
            "★ 末尾 `/` 的区别（很多人的误区）："
            "`cp -a a1 /usr` 与 `cp -a a1/ /usr` 在这里结果**一样**，"
            "都是往 `/usr/a1` 里放。真正决定「拷进去还是改名」的是"
            "**目标是否已存在**——目标目录存在就放进去，不存在就改名复制。\n\n"
            "★ **迁移**：备份整个 `/etc` 用 `cp -a /etc /backup/`；"
            "要跨机器保持原样，`cp -a` 强于 `tar` 以外的任何方式。"),
        tags=["实验 3", "cp", "归档复制", "preserve"]))

    out.append(C(
        "只看目录本身那一行，不要列里面的内容",
        "**实验 3 第 3 步**：想知道 `/usr/a1` 这个**目录本身**的权限和属主。\n\n"
        "要求：`ls` 只输出它**自己那一行**，不许把它里面的四个子目录刷出来。\n\n"
        "写出这条命令。",
        ["ls -ld /usr/a1", "ls -dl /usr/a1", "ls -ld /usr/a1/"],
        sec=s3, diff=2,
        exp=(
            "`ls -ld /usr/a1`。\n\n"
            "- `-l` 长格式（权限、硬链接数、属主、属组、大小、时间、名字）\n"
            "- `-d` **对目录本身操作**，而不是「列出目录里的内容」\n\n"
            "★ 这是 `ls` 最反直觉的一个选项：平时 `ls -l /usr` 列的是"
            "**里面的东西**；加 `-d` 才变成「看这个目录当作一个文件时的属性」。\n\n"
            "★ 参数顺序无所谓：`-ld` 与 `-dl` 完全等价"
            "（判题系统会把短选项簇排序后比）。\n\n"
            "★ **迁移**：想知道 `/tmp` 这个目录权限是不是 1777，"
            "只能 `ls -ld /tmp`；`ls -l /tmp` 看到的是里面每个人文件。"),
        tags=["实验 3", "ls", "-d"]))

    # ---------------- 实验 4 ----------------
    out.append(C(
        "把 /usr/test5 打包成 gzip 压缩包",
        "**实验 4 第 1 步**：把 `/usr/test5` 目录树打包并压缩，"
        "产出 `test5.tar.gz`（放在当前目录）。\n\n"
        "要求：**打包 + gzip 压缩一步完成**，并且显示处理了哪些文件。\n\n"
        "写出这条命令。",
        ["tar -czvf test5.tar.gz /usr/test5",
         "tar czvf test5.tar.gz /usr/test5",
         "tar --create --gzip --verbose --file test5.tar.gz /usr/test5"],
        sec=s4, diff=2,
        exp=(
            "`tar -czvf test5.tar.gz /usr/test5`。\n\n"
            "四个字母各管一段：\n"
            "- `-c` create，**创建**归档\n"
            "- `-z` 走 **gzip**\n"
            "- `-v` verbose，边打边报文件名\n"
            "- `-f` 后面跟**归档文件名**（`-f` 必须紧挨着文件名）\n\n"
            "★ 顺序的坑：`-f` 后面那一个词一定会被当成文件名。"
            "写成 `tar -cfv test5.tar.gz /usr/test5`，tar 会以为归档叫 `v`，"
            "于是多出一个叫 `v` 的文件、`test5.tar.gz` 反而被当要打包的路径。\n\n"
            "★ `-Z` 不是 gzip！`-Z` 调的是 `compress`（老式 `.Z` 格式）。"
            "教材和网上抄来的 `-Zcvf` 是错的。\n\n"
            "★ **迁移**：zstd 用 `--zstd`，xz 用 `-J`，bzip2 用 `-j`，"
            "其余字母位置不变。"),
        tags=["实验 4", "tar", "gzip", "打包"]))

    out.append(C(
        "把压缩包解到 /usr/local（别解在当前目录）",
        "**实验 4 第 2 步**：`test5.tar.gz` 已经做好，现在要解压到 "
        "`/usr/local` 下，最终得到 `/usr/local/test5/`。\n\n"
        "要求：**不许先 cd 过去**，一条命令完成。\n\n"
        "写出这条命令。",
        ["tar -xzvf test5.tar.gz -C /usr/local",
         "tar xzvf test5.tar.gz -C /usr/local",
         "tar --extract --gzip --verbose --file test5.tar.gz -C /usr/local",
         "tar -xzvf test5.tar.gz --directory=/usr/local"],
        sec=s4, diff=3,
        exp=(
            "`tar -xzvf test5.tar.gz -C /usr/local`。\n\n"
            "- `-x` extract，解包（与 `-c` 二选一）\n"
            "- `-C`（`--directory`）**先切到目标目录再解**，"
            "解包结束后**不会**把你留在那个目录里\n\n"
            "★ 为什么强调「不许 cd」：脚本里 `cd /usr/local && tar …` "
            "会让**后续所有相对路径**都基于 `/usr/local`，"
            "忘了 `cd` 回来就是一连串「文件找不到」。`-C` 是局部生效的，没这个副作用。\n\n"
            "★ 打包时若用了**绝对路径**（`tar -czf x.tar.gz /usr/test5`），"
            "GNU tar 会把开头的 `/` 去掉，所以包里是 `usr/test5/`，"
            "解到 `/usr/local` 就变成 `/usr/local/usr/test5` —— "
            "**想解出 `/usr/local/test5` 得用 `-C /`，或者打包前 `cd /usr` 再打相对路径**。\n\n"
            "★ **迁移**：`tar -tzf x.tar.gz` 先看一眼包内路径，再决定 `-C` 放哪，"
            "这是解压前最省事的一次检查。"),
        tags=["实验 4", "tar", "解压", "-C"]))

    out.append(C(
        "给 /usr/local/sdutshare 在根目录挂一个软链 /myshare",
        "**实验 4 第 3 步**：想让 `/myshare` 这个路径指向 "
        "`/usr/local/sdutshare`，像目录一样能用。\n\n"
        "要求：建**符号链接**（不是硬链接）。\n\n"
        "写出这条命令。",
        ["ln -s /usr/local/sdutshare /myshare",
         "ln --symbolic /usr/local/sdutshare /myshare"],
        sec=s4, diff=2,
        exp=(
            "`ln -s /usr/local/sdutshare /myshare`。\n\n"
            "`ln -s 目标 链接名` —— **源在前，链接名在后**，"
            "与 `cp 源 目标` 的顺序一致，但方向相反：`cp` 造副本，`ln -s` 造指针。\n\n"
            "★ 顺序写反是最常见的错：`ln -s /myshare /usr/local/sdutshare` "
            "会在 `/usr/local` 里造一个叫 `sdutshare` 的链接指向 `/myshare`，"
            "而 `/usr/local/sdutshare` 若是已存在的目录，还会在里面塞一个 `myshare`。\n\n"
            "★ 硬链接不能跨文件系统，也不能链目录 —— 所以这里只能 `-s`。\n\n"
            "★ **迁移**：软链用**相对路径**写目标（`ln -s ../sdutshare myshare`）"
            "更适合随目录整体搬家；用绝对路径则目标位置一变就断。"
            "检查断链：`find / -xtype l`。"),
        tags=["实验 4", "ln", "符号链接"]))

    out.append(C(
        "把单词表按字典序逆序排",
        "**实验 4 第 4 步**：有个文件 `/tmp/words.txt`，每行一个单词。\n\n"
        "要求：按**字典序倒序**输出到屏幕（不改原文件）。\n\n"
        "写出这条命令。",
        ["sort -r /tmp/words.txt", "sort --reverse /tmp/words.txt"],
        sec=s4, diff=1,
        exp=(
            "`sort -r /tmp/words.txt`。\n\n"
            "`sort` 默认按当前 locale 的字典序**升序**；`-r`（`--reverse`）翻过来。\n\n"
            "★ 要落到文件里必须重定向：`sort -r f > g`。"
            "`sort -r f -o f` 才是**原地**排序（`-o` 会先写临时文件再替换，安全）；"
            "写成 `sort -r f > f` 会把文件**清空**——shell 先截断再执行 `sort`。\n\n"
            "★ 数字排序别用 `-r`：`sort file` 会把 `10` 排在 `9` 前面，"
            "要 `sort -n`（或 `-h` 识别人性化单位）。\n\n"
            "★ **迁移**：`sort -k2 -n` 按第二列数值排；`sort -t: -k3` 以冒号分列。"
            "排序题九成的坑都在「没声明字段分隔符」和「按文本比了数字」。"),
        tags=["实验 4", "sort", "逆序"]))

    out.append(C(
        "把两个文件的内容拼成第三个文件",
        "**实验 4 第 5 步**：`file11` 和 `file12` 各有一段内容，"
        "要把它们**首尾相接**写进 `file13`。\n\n"
        "要求：`file11` 在前、`file12` 在后；一条命令完成。\n\n"
        "写出这条命令。",
        ["cat file11 file12 > file13"],
        sec=s4, diff=2,
        exp=(
            "`cat file11 file12 > file13`。\n\n"
            "`cat` 接多个文件时**按给出的顺序依次输出**，"
            "`>` 把整串重新导向 `file13`。\n\n"
            "★ `>` 会**先清空**目标再写；`>>` 是追加。"
            "所以 `cat a b > c` 里若 `c` 恰好是 `a` 或 `b`，内容就没了——"
            "「输出到源文件之一」是这类操作最隐蔽的自毁。\n\n"
            "★ 另一个容易踩的：`cat a b > c` 里 `c` 若已存在且是软链，"
            "写入会跟着软链走（`>` 不替换软链本身）；"
            "要替换软链本身得 `rm c && cat a b > c`。\n\n"
            "★ **迁移**：拼三个以上文件也是同一招；"
            "想加分隔符就 `cat a <(echo '---') b > c`（bash 进程替换）。"),
        tags=["实验 4", "cat", "重定向"]))

    # ---------------- 实验 5 ----------------
    out.append(C(
        "把 11.txt 改成 rwxr-x--x（数字模式）",
        "**实验 5 第 1 步**：`11.txt` 现在的权限不对，要改成 "
        "`-rwxr-x--x`。\n\n"
        "要求：用**八进制数字模式**一条命令改掉，不要用字母模式。\n\n"
        "写出这条命令。",
        ["chmod 751 11.txt", "chmod 0751 11.txt"],
        sec=s5, diff=2,
        exp=(
            "`chmod 751 11.txt`。\n\n"
            "三位八进制依次是 **属主 / 属组 / 其他**，每位由 r=4、w=2、x=1 相加：\n"
            "- 属主 `rwx` = 4+2+1 = **7**\n"
            "- 属组 `r-x` = 4+0+1 = **5**\n"
            "- 其他 `--x` = 0+0+1 = **1**\n\n"
            "所以是 `751`。\n\n"
            "★ 硬链接陷阱：`chmod` 只有一个写法 —— 它会改**inode**，"
            "同一个 inode 的所有硬链接**权限一起变**（这与 `chown` 不同，"
            "`chown` 也是改 inode，同样全变）。\n\n"
            "★ `-rwxr-x--x` 开头那个 `-` 是文件类型位，不是权限位；"
            "`d` 是目录、`l` 是软链。别把它算进数字里。\n\n"
            "★ **迁移**：目录的 `x` 位含义与文件不同 —— "
            "目录没有 `x` 就**进不去**（哪怕有 `r` 能列出名字）。"
            "所以目录常用 `755`、`750`，很少给 `644`。"),
        tags=["实验 5", "chmod", "八进制", "权限"]))

    out.append(C(
        "把 abc 整棵树（含子目录）交给 user02",
        "**实验 5 第 2 步**：`abc` 目录下有多层文件，"
        "要全部改成属主与属组都是 `user02`。\n\n"
        "要求：**递归**，一条命令，别一个一个改。\n\n"
        "写出这条命令。",
        ["chown -R user02:user02 abc", "chown -R user02.user02 abc",
         "chown --recursive user02:user02 abc",
         "chown -R user02:user02 abc/"],
        sec=s5, diff=2,
        exp=(
            "`chown -R user02:user02 abc`。\n\n"
            "- `-R`（`--recursive`）递归整棵子树\n"
            "- `属主:属组` 用冒号分隔；老式写法 `user02.user02` 也认"
            "（但用户名里若带点会歧义，优先用冒号）\n"
            "- 只写 `user02` 时**只改属主**，属组保持不动\n\n"
            "★ 只改属组可以写 `chown :user02 abc`（冒号前留空）。\n\n"
            "★ `-R` 的副作用：符号链接默认**不跟随**（改的是链接自身），"
            "想连目标一起改要 `-h` 或 `-L`，含义完全不同。\n\n"
            "★ 实操时才发现的坑：`chown` 改的是 **inode**，"
            "同 inode 的硬链接会一起变；要只影响一个路径，先确认 `ls -li` 的链接数。\n\n"
            "★ **迁移**：拷完家目录忘了属主，`chown -R ~user ~user` 一条修好——"
            "这是接手别人机器时最常敲的一条。"),
        tags=["实验 5", "chown", "递归", "属主"]))

    out.append(C(
        "改成 744 之后，长格式里长什么样",
        "**实验 5 第 3 步**：某文件执行 `chmod 744 f`。\n\n"
        "要求：写出这条命令（题目要考的是「744 对应哪几个符号位」，"
        "所以请同时把它落到文件上）。",
        ["chmod 744 f", "chmod 0744 f"],
        sec=s5, diff=2,
        exp=(
            "`chmod 744 f`。\n\n"
            "744 = 属主 `rwx`（7）+ 属组 `r--`（4）+ 其他 `r--`（4），"
            "长格式显示为 `-rwxr--r--`。\n\n"
            "★ 这里最容易错的是把 744 记成 `-rwxr--r--` 之外的什么 ——"
            "**4 只有读，没有执行**，所以属组和其他都是 `r--` 而不是 `r-x`。"
            "`744` 与 `755` 差的就是那一个 `x`。\n\n"
            "★ 脚本文件给了 `744` 会怎样：属主自己能跑，"
            "同组和别人的账号想跑就是 `Permission denied`。"
            "所以放在公共目录里的脚本一般给 `755`。\n\n"
            "★ **迁移**：`stat -c '%a %A %n' f` 一条命令同时看"
            "八进制与符号位，比 `ls -l` 逐个对更快。"),
        tags=["实验 5", "chmod", "744"]))

    out.append(C(
        "400 再给「其他」加写权限，最后是多少",
        "**实验 5 第 4 步**：某文件原权限 `400`（`-r--------`）。\n\n"
        "任务：用**符号模式**给「其他用户（o）」**加上写权限**。\n\n"
        "写出这条命令。",
        ["chmod o+w f", "chmod o=w f"],
        sec=s5, diff=3,
        exp=(
            "`chmod o+w f`（若原来 o 位为空，`o=w` 结果相同）。\n\n"
            "符号模式的三个部分：**谁 / 怎么改 / 什么权限**\n"
            "- 谁：`u` 属主、`g` 属组、`o` 其他、`a` 全部\n"
            "- 怎么改：`+` 加、`-` 减、`=` 直接赋值（会把该组其余位清掉）\n"
            "- 什么：`r`/`w`/`x`\n\n"
            "★ `400` 加 `o+w` = `402`（`-r------w-`），"
            "**不是 420、也不是 602** —— 因为 `w` 的权值是 2，加在「其他」那一位上。\n\n"
            "★ `+` 与 `=` 的区别是本题真正的考点："
            "`o=w` 会把 o 位原有的 `r`/`x` 一并清掉；"
            "原来 o 是全空的，所以两者结果一样。"
            "换个起点（比如 `o=rx`）结果就完全不同了。\n\n"
            "★ **迁移**：想知道某文件到底该给什么，"
            "`ls -l` 看现状再决定用 `+`/`-` 微调，别一上来 `=`，那是覆盖式改。"),
        tags=["实验 5", "chmod", "符号模式"]))

    out.append(C(
        "把 temp1 全部交给 root",
        "**实验 5 第 5 步**：`temp1` 这个文件属于普通用户，"
        "要移交 root（属主与属组都改成 `root`）。\n\n"
        "要求：只改这一个文件，不要递归。\n\n"
        "写出这条命令。",
        ["chown root:root temp1", "chown root.root temp1",
         "chown root: temp1"],
        sec=s5, diff=1,
        exp=(
            "`chown root:root temp1`。\n\n"
            "★ 关键点：`chown` 改属主是**特权操作**，"
            "普通用户只能「把自己的文件送给别人」且**不能改属组到不在自己组列表里的组**；"
            "要改给别人必须 `sudo`。所以真跑起来是 "
            "`sudo chown root:root temp1`。\n\n"
            "★ `root.root` 是老的 BSD 写法，GNU coreutils 仍兼容；"
            "`root:`（冒号后留空）等价于 `root:root` 再跟文件名？"
            "不完全等价 —— `chown root: temp1` 里的冒号表示「属组改成当前登录主组」，"
            "在 root 下就是 `root:root`。三者结果相同、语义不同。\n\n"
            "★ 与 `chmod` 的分工：`chmod` 管「谁能读/写/执行」，"
            "`chown` 管「这个文件是谁的」。改权限永远改不了属主，反之亦然。\n\n"
            "★ **迁移**：把网站目录交给 web 用户："
            "`chown -R nginx:nginx /usr/share/nginx/html`。"),
        tags=["实验 5", "chown", "root"]))

    return out


# ===================================================================== #
#  二、命令特训 · 文件与目录
# ===================================================================== #
def part_files() -> list[dict]:
    sec = "命令特训 · 文件与目录"
    out: list[dict] = []

    out.append(C(
        "列出所有条目（含隐藏），按修改时间倒序，大小人性化",
        "你要看一个目录里**最近改过**的东西，包括以点开头的隐藏文件，"
        "大小要能一眼看懂（`4.0K` 而不是 `4096`）。\n\n"
        "写出这条命令（就在当前目录）。",
        ["ls -lath", "ls -alht", "ls -lat --human-readable", "ls -lAhT"],
        sec=sec, diff=2,
        exp=(
            "`ls -lath`。四个选项各管一件事：\n"
            "- `-a` 含隐藏文件（`.` 与 `..` 也在里面；只想去掉这两个用 `-A`）\n"
            "- `-t` 按**修改时间**排序，新的在前\n"
            "- `-h` 大小人性化（`-h` 必须和 `-l` 一起才有意义）\n"
            "- `-l` 长格式\n\n"
            "★ 参数顺序完全无所谓：`-lath`、`-alht`、`-t -h -a -l` 判题都算同一个"
            "（短选项簇会被排序去重后比）。\n\n"
            "★ `-h` 是 `--human-readable` 的短写法，但它**只对 `-l` 里的 Size 列生效**；"
            "单敲 `ls -h` 什么也不会变。\n\n"
            "★ **迁移**：想按时间**正序**（老的在前）用 `-tr`；"
            "想按大小排用 `-S`。`ls -lt | head` 是「最近改了啥」的日常起手式。"),
        tags=["ls", "隐藏文件", "排序", "-h"]))

    out.append(C(
        "只列出子目录，不要文件",
        "当前目录里文件和子目录混在一起。你只想看**有哪些子目录**。\n\n"
        "写出这条命令（不要递归进去）。",
        ["ls -d */", "ls -d */ .*/ 2>/dev/null", "find . -maxdepth 1 -type d"],
        sec=sec, diff=3,
        exp=(
            "`ls -d */`。\n\n"
            "`*/` 是 shell 的**通配**：只匹配「以 `/` 结尾」的名字，"
            "而只有目录才会展开成这种形式（文件不会 `*/` 匹配上）。"
            "`-d` 让 `ls` 停留在**目录本身**，不要展开里面的内容。\n\n"
            "★ 少了 `-d` 会怎样：`ls */` 会把每个子目录**里面的内容**全列出来，"
            "输出立刻变成几百行。这是本题唯一的分水岭。\n\n"
            "★ 想连隐藏目录一起要：`ls -d */ .*/`（`.*/` 顺带把 `.` 和 `..` 也带出来，"
            "常见做法是再 `grep -v '^\\.\\.\\?$'` 过滤掉）。\n\n"
            "★ **迁移**：`find . -maxdepth 1 -type d` 是更精确的写法，"
            "它不依赖 shell 通配、也不怕名字里有空格；"
            "`-maxdepth 1` 就是「别递归」的意思。"),
        tags=["ls", "-d", "通配", "find"]))

    out.append(C(
        "列出某目录下所有普通文件的完整路径",
        "要从 `/etc` 往下把**所有普通文件**（不含目录、不含软链）的路径列出来，"
        "用于喂给另一个脚本。\n\n"
        "写出这条命令。",
        ["find /etc -type f", "find /etc -type f -print"],
        sec=sec, diff=2,
        exp=(
            "`find /etc -type f`。\n\n"
            "`-type` 的取值是本题的核心：\n"
            "- `f` 普通文件\n"
            "- `d` 目录\n"
            "- `l` 符号链接\n"
            "- `b`/`c` 块设备/字符设备\n\n"
            "★ 注意 `-type f` **不包含**软链 —— 软链是 `l`，"
            "哪怕它指向一个普通文件。想「软链也当文件算」得写 "
            "`-type f -o -type l`（或用 GNU 的 `-xtype f`）。\n\n"
            "★ `find` 默认就打印路径（`-print` 可省），所以两个写法等价。\n\n"
            "★ **迁移**：`find` 的输出**带 `./` 前缀**看情况——"
            "`find .` 会输出 `./a.txt`，`find /etc` 输出 `/etc/a.conf`。"
            "脚本里拿它做参数，路径基准必须想清楚。"),
        tags=["find", "-type", "普通文件"]))

    out.append(C(
        "一次建出三个空文件",
        "要同时创建 `a.txt`、`b.txt`、`c.txt` 三个空文件。\n\n"
        "写出这条命令（一条命令搞定，别写三行）。",
        ["touch a.txt b.txt c.txt", "touch {a,b,c}.txt"],
        sec=sec, diff=1,
        exp=(
            "`touch a.txt b.txt c.txt`（或花括号展开 `touch {a,b,c}.txt`）。\n\n"
            "`touch` 的本职其实是**改时间戳**（把访问/修改时间刷成当前），"
            "「文件不存在就建一个空文件」只是它的副作用 —— 但这个副作用太好用，"
            "所以大家都当它是「创建文件」。\n\n"
            "★ `{a,b,c}.txt` 是 **bash 的花括号展开**（brace expansion），"
            "由 shell 先展开成三个词再交给 `touch`。"
            "注意它**不经过文件系统**，即使文件名里有通配符也会照样生成。"
            "在 `sh`（dash）里不支持花括号展开。\n\n"
            "★ **迁移**：`touch -t 202610190800 f` 可以把时间戳设成指定时刻；"
            "`touch -d '2 days ago' f` 更好读。造测试数据时很常用。"),
        tags=["touch", "花括号展开", "创建文件"]))

    out.append(C(
        "只把文件时间戳刷成当前，内容一个字都别动",
        "`/var/log/app.log` 被一个监控脚本盯着，只要它的 mtime 太旧就会报警。\n\n"
        "你要把它的 mtime 刷成**现在**，但**绝对不能改内容**。\n\n"
        "写出这条命令。",
        ["touch /var/log/app.log"],
        sec=sec, diff=2,
        exp=(
            "`touch /var/log/app.log`。\n\n"
            "这是 `touch` 的**本职用途**，不是副作用：它只更新时间戳，"
            "不会打开文件写入，所以内容分毫不动。\n\n"
            "★ 对比一下常见的错法：`echo '' >> /var/log/app.log` 确实也刷了 mtime，"
            "但**往文件末尾追加了一个换行**——"
            "日志解析器会看到一个空行，`wc -l` 也会 +1。"
            "`touch` 才是干净的做法。\n\n"
            "★ `touch` 会同时更新 **atime 和 mtime**；只想改 atime 用 `touch -a`，"
            "只想改 mtime 用 `touch -m`。\n\n"
            "★ **迁移**：`touch -r ref.txt target.txt` 把 target 的时间刷成和 "
            "ref 一致 —— 造「看起来很久没改」的测试文件时很省事。"),
        tags=["touch", "mtime", "时间戳"]))

    out.append(C(
        "复制文件到另一个名字（目标已存在就覆盖）",
        "把 `report.txt` 复制一份叫 `report.bak`，**覆盖**已有同名文件、不要提问。\n\n"
        "写出这条命令。",
        ["cp report.txt report.bak", "cp -f report.txt report.bak"],
        sec=sec, diff=1,
        exp=(
            "`cp report.txt report.bak`（`-f` 是「强制」，一般可省）。\n\n"
            "`cp 源 目标`：目标不存在就新建；存在就**直接覆盖内容**，"
            "且**保留目标原有的权限与属主**（这一点很容易被忽略）。\n\n"
            "★ 覆盖时 inode 不变：所以原文件的硬链接看到的也是新内容。\n\n"
            "★ 为什么 `-f` 一般可省：`cp` 默认不提问；只有你的 `alias cp='cp -i'` "
            "或系统里配了 `cp -i` 时才会问。`-f` 是硬关掉这种交互。\n\n"
            "★ **迁移**：想「保留源文件权限」而不是继承目标的，用 `cp -p`；"
            "整个目录树用 `cp -a`。日常改配置文件前先 "
            "`cp -a /etc/nginx/nginx.conf{,.bak}` 备份，花括号展开一次到位。"),
        tags=["cp", "覆盖", "备份"]))

    out.append(C(
        "改名（同目录内移动）",
        "把 `old.log` 改名为 `new.log`，内容与原位置都不变。\n\n"
        "写出这条命令。",
        ["mv old.log new.log"],
        sec=sec, diff=1,
        exp=(
            "`mv old.log new.log`。\n\n"
            "★ 关键认知：Linux **没有独立的 rename 命令**，改名就是 `mv`。"
            "同目录内 `mv` 只改目录项，**不改 inode 内容**，所以瞬间完成、不占额外空间"
            "（哪怕文件有 10G，也一样是瞬间）。\n\n"
            "★ 目标已存在时 `mv` **直接覆盖，且不提示**（除非配了 `-i` 别名）。"
            "这是 `mv` 最危险的地方：`mv a b` 里 b 已存在，b 就没了，没有回收站。\n\n"
            "★ 跨文件系统 `mv` 会退化成「复制 + 删除」，"
            "此时 inode 变了、属主可能变、耗时也和大小有关。\n\n"
            "★ **迁移**：批量改名别用 `mv *.log *.txt`（通配会展开成多对参数，"
            "`mv` 只认最后一个是目标）——用 `rename` 或 `for` 循环。"),
        tags=["mv", "改名"]))

    out.append(C(
        "删除空目录",
        "`/tmp/empty_dir` 已经空了，删掉它。\n\n"
        "要求：用**专门删空目录**的那个命令（不要用能删一切的 `rm -r`）。",
        ["rmdir /tmp/empty_dir"],
        sec=sec, diff=1,
        exp=(
            "`rmdir /tmp/empty_dir`。\n\n"
            "`rmdir` 的设计哲学就是**安全**：目录非空时它会直接报错拒绝"
            "（`Directory not empty`），所以永远不会误删数据。\n\n"
            "★ `rm -r` 也能删空目录，但它是「什么都能删」的推土机。"
            "脚本里删临时目录用 `rmdir`，等于给自己加了一道保险："
            "**万一目录里还有东西，它会失败而不是静默删掉**。\n\n"
            "★ `rmdir -p a/b/c` 可以「删完 c 再顺手删空的 b、a」，"
            "清除多级空目录链时很好用。\n\n"
            "★ **迁移**：`rm -rf` 之前先 `ls` 一眼，或者干脆 `rm -ri` "
            "让它逐个确认。生产环境里 `rm -rf $VAR/` 里 `$VAR` 为空"
            "就等于 `rm -rf /`，加 `set -u` 能防住。"),
        tags=["rmdir", "空目录", "安全"]))

    out.append(C(
        "递归删除整个目录树",
        "`/tmp/build` 整个目录（含所有子目录和文件）都要清掉。\n\n"
        "写出这条命令。",
        ["rm -rf /tmp/build", "rm -r /tmp/build"],
        sec=sec, diff=2,
        exp=(
            "`rm -rf /tmp/build`。\n\n"
            "- `-r`（`--recursive`）递归\n"
            "- `-f`（`--force`）忽略不存在的文件、不提示确认\n\n"
            "★ 只写 `rm -r` 时，遇到**只读文件**会逐个问你要不要删；"
            "`-f` 让它闭嘴照删。批量清临时目录几乎总是要 `-rf`。\n\n"
            "★ 顺序无所谓：`rm -fr` 一样。但**别写 `rm -rf / tmp/build`**"
            "（多一个空格就是删根目录，某些 `rm` 实现有保护，但不能赌）。\n\n"
            "★ 变量为空是头号杀手：`rm -rf $DIR/` 里 `DIR` 没赋值就成了 `rm -rf /`。"
            "脚本里用 `rm -rf \"${DIR:?}\"` —— `:?` 会在变量为空时直接报错退出。\n\n"
            "★ **迁移**：想「删之前先看一眼」，`ls -R /tmp/build | head -50`；"
            "重要目录先 `mv` 到回收目录放一天，比 `rm` 稳。"),
        tags=["rm", "递归删除", "-rf"]))

    out.append(C(
        "给同一个文件再起一个名字（不复制内容）",
        "`/data/big.img` 有 8G，你想在 `/backup/big.img` 也能访问到它，"
        "但**不想多占 8G 空间**。\n\n"
        "要求：同一文件系统内，用**硬链接**。\n\n"
        "写出这条命令。",
        ["ln /data/big.img /backup/big.img"],
        sec=sec, diff=3,
        exp=(
            "`ln /data/big.img /backup/big.img`（不带 `-s` 就是硬链接）。\n\n"
            "硬链接的本质：**多个目录项指向同一个 inode**。"
            "所以不占额外空间、删除其中一个名字文件照样在（"
            "`ls -l` 第二列那个数字就是链接数，减到 0 才真删数据）。\n\n"
            "★ 硬链接的两条硬限制：\n"
            "1. **不能跨文件系统**（inode 编号只在单个文件系统内唯一）\n"
            "2. **不能链目录**（会造出环，`fsck` 会疯）\n\n"
            "★ 与软链的区别：硬链接是「另一个名字」，软链是「一个指向路径的文件」。"
            "删掉源文件，硬链接照样能读；软链会变成断链。\n\n"
            "★ **迁移**：`ls -li` 看 inode 号，两个名字 inode 相同就是硬链接；"
            "`find /data -samefile /data/big.img` 可以找出所有硬链接。"),
        tags=["ln", "硬链接", "inode"]))

    out.append(C(
        "查一个软链到底指向哪里",
        "`/usr/bin/python3` 很可能是个软链。想知道它**链到哪个真实路径**。\n\n"
        "要求：只输出目标路径，不要那一整行 `ls -l` 的权限信息。",
        ["readlink /usr/bin/python3", "readlink -f /usr/bin/python3",
         "namei -l /usr/bin/python3 | tail -1"],
        sec=sec, diff=2,
        exp=(
            "`readlink /usr/bin/python3`。\n\n"
            "`readlink` 只干一件事：把软链的目标路径打印出来，"
            "输出干净，最适合塞进脚本变量：`TARGET=$(readlink /usr/bin/python3)`。\n\n"
            "★ `-f`（`--canonicalize`）会**一路跟到底**，"
            "把多级软链全解析成最终的真实绝对路径。"
            "链条长的时候（`python3 → python3.12 → /usr/bin/python3.12`）"
            "只有 `-f` 能给到终点。\n\n"
            "★ `ls -l` 也能看出目标，但它输出的是整行，"
            "而且**相对软链只显示相对写法**，你还得自己拼路径。\n\n"
            "★ **迁移**：`readlink -f .` 等于 `pwd -P`（物理路径）；"
            "排查「命令到底跑的是哪个文件」用 `type -a` 或 `which -a`，"
            "再用 `readlink -f` 看终点。"),
        tags=["readlink", "软链", "realpath"]))

    out.append(C(
        "删掉目录里所有内容，但保留目录本身",
        "`/var/www/html` 这个目录要留着（属主属组都不能变），"
        "但里面的**所有文件和子目录**都要清空。\n\n"
        "写出这条命令。",
        ["rm -rf /var/www/html/*", "rm -rf /var/www/html/* /var/www/html/.[!.]*"],
        sec=sec, diff=3,
        exp=(
            "`rm -rf /var/www/html/*`（严格说还要处理隐藏文件，见下）。\n\n"
            "★ 为什么不能 `rm -rf /var/www/html`：那会把目录本身也删掉，"
            "重建出来的属主属组、SELinux 上下文、挂载点全都变了。"
            "「清空」和「删除重建」在权限体系里是两件事。\n\n"
            "★ 隐藏文件是这道题真正的坑：`*` **不匹配**以点开头的名字。"
            "所以要连 `.*` 一起删：`rm -rf /var/www/html/* /var/www/html/.[!.]*`\n"
            "（`.[!.]*` 是「点开头、第二个字符不是点」，避免把 `.` 和 `..` 也带进来）\n\n"
            "★ bash 里更省心的写法：`shopt -s dotglob` 之后 `*` 就含隐藏文件了。\n\n"
            "★ **迁移**：`find /var/www/html -mindepth 1 -delete` "
            "是另一种干净写法（`-mindepth 1` 正好排除目录自身）。"),
        tags=["rm", "清空目录", "隐藏文件"]))

    out.append(C(
        "复制时只覆盖「源比目标新」的那些",
        "`/src` 和 `/dst` 是两份同构的目录。你要做增量同步："
        "**只复制比目标更新的文件**，别浪费时间重拷全部。\n\n"
        "要求：用 `cp` 的选项，不要用 `rsync`。",
        ["cp -ru /src/. /dst/", "cp -u -r /src/. /dst/", "cp -a -u /src/. /dst/"],
        sec=sec, diff=4,
        exp=(
            "`cp -ru /src/. /dst/`。\n\n"
            "`-u`（`--update`）的判据是 **mtime**："
            "源比目标新（或目标不存在）才复制，否则跳过。\n\n"
            "★ `/src/.` 那个点很关键：`cp -r /src /dst/` 会造出 `/dst/src/`，"
            "而 `cp -r /src/. /dst/` 是把 src 的**内容**倒进 dst。"
            "少了这个点，整个目录结构就多套一层。\n\n"
            "★ `-u` 只看**时间**，不看内容。文件被删了它不会删（还是同步工具更合适），"
            "时间戳被改过（`touch`）它就误判。所以真要同步还是 `rsync -a`。\n\n"
            "★ **迁移**：`rsync -av --delete src/ dst/` 才是完整的镜像同步"
            "（`--delete` 才会删掉目标里多出来的文件）。"
            "`cp -u` 适合「补一遍新文件」这种轻量场景。"),
        tags=["cp", "-u", "增量", "rsync"]))

    out.append(C(
        "看文件占用的 inode 号",
        "两个文件看起来内容一样，你要确认它们**是不是同一个 inode**"
        "（即硬链接）。\n\n"
        "要求：`ls` 输出里带 inode 号。",
        ["ls -li file1 file2", "ls -il file1 file2", "stat -c '%i %n' file1 file2"],
        sec=sec, diff=2,
        exp=(
            "`ls -li file1 file2`。\n\n"
            "`-i` 让 `ls` 在最前面多打一列 **inode 编号**。"
            "两行 inode 相同 → 同一个文件（硬链接）；不同 → 就是两个独立文件。\n\n"
            "★ inode 是**每个文件系统内部**的编号，跨分区不唯一，"
            "所以 `ls -i` 的结果不能跨分区比较大小或相等。\n\n"
            "★ 第二种写法 `stat -c '%i %n'` 输出更干净，"
            "脚本里比对更好解析（`%i` 是 inode，`%n` 是文件名）。\n\n"
            "★ **迁移**：`df -i` 看 inode 使用率 —— "
            "「磁盘还有空间但写不进文件」多半是 inode 用完了（海量小文件场景）。"),
        tags=["ls", "-i", "inode", "stat"]))

    out.append(C(
        "建多级目录并立刻进去（一条命令）",
        "要创建 `~/project/src/{main,test}` 这套目录并**马上进入 `src`**。\n\n"
        "写出这条命令（用 `&&` 串起来）。",
        ["mkdir -p ~/project/src/{main,test} && cd ~/project/src",
         "mkdir -p ~/project/src/main ~/project/src/test && cd ~/project/src"],
        sec=sec, diff=3,
        exp=(
            "`mkdir -p ~/project/src/{main,test} && cd ~/project/src`。\n\n"
            "两个知识点叠在一起：\n"
            "1. **花括号展开**：`{main,test}` 被 shell 展开成两个路径参数，"
            "`mkdir -p` 一次建完\n"
            "2. **`&&`**：前一条**成功**才执行后一条。"
            "写 `;` 的话，`mkdir` 失败了照样 `cd`（然后 cd 也失败），"
            "报错信息会叠成一堆看不出因果。\n\n"
            "★ 为什么用 `-p`：父目录 `~/project` 可能不存在；"
            "`-p` 逐级创建且**已存在不报错**，重跑安全。\n\n"
            "★ **迁移**：`cd` 到不存在的目录会失败，"
            "所以「建完就进」必须 `&&` 而不是 `;`。"
            "脚本里更稳的写法是 `mkdir -p X && cd X || exit 1` —— 显式失败退出。"),
        tags=["mkdir", "cd", "&&", "花括号展开"]))

    out.append(C(
        "查看目录树结构（不要一堆 ls 输出）",
        "给一个目录，想用**树状缩进**看清层级（最多两层），"
        "不要 `ls -R` 那种平铺。\n\n"
        "写出这条命令。",
        ["tree -L 2 /etc", "tree -L 2 -d /etc", "find /etc -maxdepth 2 | sort"],
        sec=sec, diff=3,
        exp=(
            "`tree -L 2 /etc`。\n\n"
            "`-L 2` 限制**递归深度**为 2 层，不然 `/etc` 能刷满整个屏幕。\n\n"
            "★ `tree` 不是 coreutils 的一部分，最小化安装常常没有："
            "Fedora 上 `sudo dnf install tree`。没有它时的替代是 "
            "`find /etc -maxdepth 2 | sort`（平铺但可控），"
            "或者 `ls -R`（平铺且不好读）。\n\n"
            "★ 只看目录不要文件：`tree -d`；只看目录且限制深度：`tree -L 2 -d`。\n\n"
            "★ **迁移**：`tree -L 1` 是「这目录里大概有什么」最快的一眼；"
            "`tree -h --du` 顺便看每层占多大，排查空间问题时比 `du -sh *` 直观。"),
        tags=["tree", "目录结构", "find"]))

    out.append(C(
        "把文件内容清空（但保留文件本身与权限）",
        "`/var/log/app.log` 涨到 2G 了。要**清空内容**，"
        "但文件名、属主、权限都必须原样保留（服务还开着这个文件句柄）。\n\n"
        "写出这条命令。",
        ["truncate -s 0 /var/log/app.log", ": > /var/log/app.log",
         "> /var/log/app.log", "cat /dev/null > /var/log/app.log"],
        sec=sec, diff=4,
        exp=(
            "`truncate -s 0 /var/log/app.log`（或 `: > /var/log/app.log`、`> /var/log/app.log`）。\n\n"
            "★ 为什么**不能** `rm` 再 `touch`：那样 inode 变了，"
            "而正在写日志的进程**握着旧 inode 的句柄**，会继续往那个已删除的 inode 写 —— "
            "`df` 显示空间没释放，`ls` 又看不到文件。这就是经典的「删了日志但磁盘没空出来」。\n\n"
            "★ `>` 重定向是**原地截断**（O_TRUNC），inode 不变，"
            "所有已打开的句柄立刻看到文件长度归零。这是处理「进程占用日志」的正确姿势。\n\n"
            "★ `logrotate` 的 `copytruncate` 选项就是干这件事的；"
            "不用它的话通常配 `postrotate` 发信号让进程重开日志。\n\n"
            "★ **迁移**：`truncate -s 100M f` 还能把文件**撑大**（稀疏文件），"
            "造大文件测限速时很有用，而且不真占磁盘。"),
        tags=["truncate", "重定向", "日志", "inode"]))

    return out


# ===================================================================== #
#  三、命令特训 · 查看文件内容
# ===================================================================== #
def part_view() -> list[dict]:
    sec = "命令特训 · 查看文件内容"
    out: list[dict] = []

    out.append(C(
        "只看前 50 行",
        "`access.log` 有几十万行。你只想看**开头 50 行**。\n\n"
        "写出这条命令。",
        ["head -n 50 access.log", "head -50 access.log", "head --lines=50 access.log"],
        sec=sec, diff=1,
        exp=(
            "`head -n 50 access.log`。\n\n"
            "三种写法都合法：`-n 50`、`-50`（省略 `-n` 的简写）、"
            "`--lines=50`。`-50` 这种老写法在新版 coreutils 里仍支持，"
            "但脚本里建议写全 `-n 50`，可读性更好。\n\n"
            "★ 不写 `-n` 时默认 **10 行**。所以 `head f` 就是前 10 行。\n\n"
            "★ **迁移**：`head -n -10 f` 表示「除最后 10 行外的全部」，"
            "负数是「从末尾倒数」的意思 —— 这个用法很多人不知道，"
            "配合 `tail -n +N` 就能精确切任意区间。"),
        tags=["head", "前N行"]))

    out.append(C(
        "实时跟踪日志新增内容",
        "服务在跑，你要盯着 `/var/log/messages` **持续输出新行**，"
        "而不是只看某一刻。\n\n"
        "写出这条命令。",
        ["tail -f /var/log/messages", "tail -F /var/log/messages",
         "tail -f -n 10 /var/log/messages"],
        sec=sec, diff=2,
        exp=(
            "`tail -f /var/log/messages`。\n\n"
            "`-f`（follow）让 `tail` **不退出**，文件一有新行就刷出来。"
            "`Ctrl+C` 结束。\n\n"
            "★ `-f` 与 `-F` 的关键差别（生产环境必知）：\n"
            "- `-f` 跟的是**文件描述符**。日志被 `logrotate` 改名轮转后，"
            "你还钉在旧 inode 上，**新日志一行也看不到**。\n"
            "- `-F` = `--follow=name --retry`，跟**文件名**。"
            "文件被轮转/删除重建后会自动重新打开。\n\n"
            "★ **迁移**：长期盯日志用 `-F`；一次性看增量用 `-f`。"
            "配合 `grep` 做过滤：`tail -F app.log | grep -i error`。"),
        tags=["tail", "-f", "-F", "日志"]))

    out.append(C(
        "从第 100 行一直看到文件末尾",
        "`data.csv` 前 99 行是表头说明（要跳过），你要从**第 100 行**开始看。\n\n"
        "写出这条命令。",
        ["tail -n +100 data.csv", "tail -n+100 data.csv", "tail --lines=+100 data.csv"],
        sec=sec, diff=2,
        exp=(
            "`tail -n +100 data.csv`。\n\n"
            "★ `+N` 是 `tail` 里最容易记反的语法："
            "`-n +100` 表示「**从第 100 行开始**往后全部」，"
            "而不是「最后 100 行」（那是 `-n 100`）。\n\n"
            "记忆法：`+` 是「起点在正数第 N 行」，`-` 或省略是「尾部倒数 N 行」。\n\n"
            "★ 等价思路：`sed -n '100,$p'` 或 `awk 'NR>=100'` 也能干，"
            "但 `tail -n +N` 是最省事的。\n\n"
            "★ **迁移**：跳过表头还有一个专用写法 `tail -n +2`，"
            "处理 CSV 时几乎每天都要用一次。"),
        tags=["tail", "+N", "跳过表头"]))

    out.append(C(
        "只统计文件有多少行",
        "`/etc/passwd` 里有多少个用户？只要**行数**，别的都不要。\n\n"
        "写出这条命令。",
        ["wc -l /etc/passwd"],
        sec=sec, diff=1,
        exp=(
            "`wc -l /etc/passwd`。\n\n"
            "`wc` 三个常用选项各数字段：\n"
            "- `-l` 行数（line）\n"
            "- `-w` 词数（word）\n"
            "- `-c` 字节数（byte）\n"
            "- `-m` 字符数（character，多字节字符才和 `-c` 不同）\n\n"
            "★ 不写选项时输出三列 `行 词 字节 文件名`。"
            "要用这个数字做判断，通常还要 `awk '{print $1}'` 或 "
            "`wc -l < f`（重定向进来就没有文件名那一列）。\n\n"
            "★ 「行数」的定义是**换行符个数**：文件末尾没有换行符时，"
            "`wc -l` 会少算一行。造数据时容易踩。\n\n"
            "★ **迁移**：`printf '%s\\n' {1..100} | wc -l` 造 100 行；"
            "「有多少条匹配」用 `grep -c` 比 `grep | wc -l` 快。"),
        tags=["wc", "-l", "行数"]))

    out.append(C(
        "同时看行数、词数、字节数",
        "要一次性拿到某个文件的**三个统计值**，不要跑三遍。\n\n"
        "写出这条命令。",
        ["wc /etc/passwd", "wc -lwc /etc/passwd", "wc -l -w -c /etc/passwd"],
        sec=sec, diff=1,
        exp=(
            "`wc /etc/passwd`（不带选项默认就是行/词/字节三列）。\n\n"
            "输出形如：`37  62 1932 /etc/passwd`\n\n"
            "★ 三列顺序固定是 **行 → 词 → 字节**，不随你写选项的顺序变。"
            "所以 `wc -c -l` 输出的还是行在前。\n\n"
            "★ 只要部分列就明确写选项：脚本里解析时优先 "
            "`wc -l f | awk '{print $1}'`，别指望「取第一列」永远对。\n\n"
            "★ **迁移**：多个文件一起统计时，`wc` 会在最后多打一行 `total`，"
            "脚本里遍历文件时要记得跳过它。"),
        tags=["wc", "统计"]))

    out.append(C(
        "带行号显示文件内容",
        "要给同事贴一段代码片段，需要**行号**方便他定位。\n\n"
        "要求：用 `cat`，不要 `nl`。",
        ["cat -n config.conf", "cat --number config.conf"],
        sec=sec, diff=1,
        exp=(
            "`cat -n config.conf`。\n\n"
            "★ 一个常见误区：**`cat -b` 与 `cat -n` 不同**。"
            "`-n` 给**所有行**编号（空行也占号），"
            "`-b` 只给**非空行**编号（空行不占号）。"
            "贴配置文件时 `-b` 往往更好看，但定位到具体行要 `-n`。\n\n"
            "★ `cat -n` 是**显示行号**，不是「统计行数」——"
            "统计行数要用 `wc -l`。这是个高频混淆点。\n\n"
            "★ `cat` 的编号是**显示层**的，不会写回文件。"
            "真想改文件得 `sed -i '=' f` 之类的工具。\n\n"
            "★ **迁移**：`nl -ba f` 功能等价且默认不编空行，"
            "还能 `nl -s '. ' -w 3` 定制分隔符与宽度。"),
        tags=["cat", "-n", "行号"]))

    out.append(C(
        "分页查看大文件，还能在里面搜索",
        "要读一个 200M 的配置文件。`cat` 会刷屏、`less` 才能翻。\n\n"
        "写出这条命令。",
        ["less config.big", "less -N config.big"],
        sec=sec, diff=1,
        exp=(
            "`less config.big`。\n\n"
            "`less` 的核心操作（比记选项更值钱）：\n"
            "- `/关键词` 向下搜，`?关键词` 向上搜，`n`/`N` 跳下一个/上一个\n"
            "- `g` 到文件头，`G` 到文件尾，`50g` 跳到第 50 行\n"
            "- `PgUp`/`PgDn`/空格 翻页；`q` 退出\n"
            "- `-N` 打开行号显示\n\n"
            "★ 为什么用 `less` 不用 `more`：`more` **只能往下翻**，"
            "而且很多实现不支持回滚。`less` 是 `more` 的超集"
            "（名字就是「less is more」的玩笑）。\n\n"
            "★ `less` 不会把整个文件读进内存，所以 200M 甚至 10G 都能瞬间打开。\n\n"
            "★ **迁移**：`less +F f` 等于 `tail -F`（进入跟随模式，`Ctrl+C` 退出跟随、"
            "`F` 再次进入）；管道也能喂给 `less`：`dmesg | less`。"),
        tags=["less", "分页", "搜索"]))

    out.append(C(
        "判断一个文件到底是什么类型",
        "有个文件叫 `data`，没有扩展名。你要知道它是文本、gzip 包、还是 ELF 可执行文件。\n\n"
        "写出这条命令。",
        ["file data"],
        sec=sec, diff=1,
        exp=(
            "`file data`。\n\n"
            "`file` 看的是**文件头部的魔数（magic number）**，不是扩展名。"
            "所以 `mv a.png b.txt` 之后 `file b.txt` 照样报 `PNG image data`。\n\n"
            "★ 这是 Linux 与 Windows 思维差异最大的一处："
            "**Linux 不靠扩展名判断类型**，扩展名只对人类和某些软件有意义。\n\n"
            "★ 常见输出：`ASCII text`、`UTF-8 Unicode text`、"
            "`gzip compressed data`、`ELF 64-bit LSB executable`、"
            "`symbolic link to ...`、`directory`。\n\n"
            "★ **迁移**：`file *` 批量判断目录下所有文件；"
            "`file -i f` 输出 MIME 类型（`text/plain; charset=utf-8`），"
            "排查编码问题时比猜有用。"),
        tags=["file", "文件类型", "魔数"]))

    out.append(C(
        "把文件内容倒过来逐行输出",
        "日志是追加写的，最新的在最后。你要**从最后一行往前**看（不排序，纯倒序）。\n\n"
        "写出这条命令。",
        ["tac app.log"],
        sec=sec, diff=2,
        exp=(
            "`tac app.log`。\n\n"
            "`tac` 就是 `cat` 反过来写 —— 它把文件**按行倒序**输出，"
            "不做任何排序。与 `sort -r` 完全不同："
            "`sort -r` 会按字典序重排，`tac` 只翻转原来的顺序。\n\n"
            "★ 为什么不用 `tail -r`：那是 BSD/macOS 的写法，"
            "GNU coreutils 里没有。Linux 上用 `tac`。\n\n"
            "★ `tac` 会把整个文件读进内存再倒着输出，"
            "超大文件（几个 G）会吃内存；那种场景用 `tail -n 1000 | tac` 截断后再倒。\n\n"
            "★ **迁移**：`tac` 和 `sed '1!G;h;$!d'` 效果一样"
            "（后者纯 sed 实现，某些极简环境里只有它可用）。"),
        tags=["tac", "倒序", "日志"]))

    out.append(C(
        "看二进制文件里的可打印字符",
        "有个文件 `file .bin` 报的是 `data`，你想看看里面有没有可读的字符串/结构。\n\n"
        "要求：以**八进制 + 可打印字符**的形式 dump 出来。",
        ["od -c binfile", "od -tc binfile", "od -An -c binfile"],
        sec=sec, diff=3,
        exp=(
            "`od -c binfile`。\n\n"
            "`od`（octal dump）默认输出八进制字节值；"
            "`-c` 让它把**可打印字符直接显示成字符**，"
            "不可打印的用 `\\n`、`\\t`、`\\0` 这类转义表示 —— "
            "这才是「看懂二进制文件结构」的姿势。\n\n"
            "★ 常用组合：\n"
            "- `od -An -c f` 去掉左侧偏移地址列（`-An`）\n"
            "- `od -tx1 f` 十六进制字节（最常用）\n"
            "- `hexdump -C f` 十六进制 + ASCII 双栏（更好读，但不是 coreutils）\n\n"
            "★ **迁移**：`strings f | head` 直接从二进制里捞出连续可打印字符串，"
            "查「这个二进制里有没有硬编码路径/密钥」时比 `od` 快。"),
        tags=["od", "二进制", "hexdump"]))

    out.append(C(
        "一次看多个文件的开头，并且分得清哪个是哪个",
        "`a.conf`、`b.conf`、`c.conf` 三个配置文件，你要各看前 5 行做对比。\n\n"
        "要求：一条命令，输出里必须**带文件名分隔**。",
        ["head -n 5 a.conf b.conf c.conf"],
        sec=sec, diff=2,
        exp=(
            "`head -n 5 a.conf b.conf c.conf`。\n\n"
            "★ 关键细节：**只要给了多于一个文件，`head` 就会自动加标题行**：\n"
            "```\n==> a.conf <==\n...\n==> b.conf <==\n...\n```\n"
            "只给一个文件时**不会**加 —— 所以脚本里解析单文件输出时，"
            "别指望永远有 `==>` 这一行。\n\n"
            "★ 想强制加标题：`head -v`；想强制不加：`head -q`（quiet）。\n"
            "这两个选项在写脚本时比默认行为更可控。\n\n"
            "★ **迁移**：`tail` 有一模一样的行为（`-v`/`-q`/多文件加标题）；"
            "`cat` 多文件时**不加**标题，需要分隔得自己 `echo`。"),
        tags=["head", "多文件", "标题"]))

    out.append(C(
        "看文件末尾 20 行，但不要跟进去等新内容",
        "排查报错时你只想看**最后 20 行**，看完就退出，不要卡在跟踪模式。\n\n"
        "写出这条命令。",
        ["tail -n 20 app.log", "tail -20 app.log", "tail --lines=20 app.log"],
        sec=sec, diff=1,
        exp=(
            "`tail -n 20 app.log`。\n\n"
            "`tail` 不带 `-f` 时就是「看末尾 N 行然后退出」，默认 N=10。\n\n"
            "★ 与 `-f` 的区别是本题的核心：`-f` 会**一直挂着不退出**，"
            "在脚本里或 CI 里误用会让整条流水线卡死。"
            "「看一眼就完」永远不加 `-f`。\n\n"
            "★ 排查报错的高频组合：`tail -n 50 app.log | grep -i error`，"
            "或者 `grep -i error app.log | tail -n 20` —— "
            "**后者的语义是「最近 20 条错误」，前者是「最后 50 行里的错误」**，"
            "差别很大，别混。\n\n"
            "★ **迁移**：`tail -c 200 f` 按**字节**取末尾，"
            "处理「最后一行巨长」的场景（比如没有换行的 JSON）时比 `-n` 有用。"),
        tags=["tail", "末尾", "-n"]))

    out.append(C(
        "数一数某个词在文件里出现了多少次",
        "`access.log` 里 `ERROR` 出现了多少次？只要**次数**。\n\n"
        "写出这条命令（不要输出匹配到的行）。",
        ["grep -c ERROR access.log", "grep -c 'ERROR' access.log"],
        sec=sec, diff=1,
        exp=(
            "`grep -c ERROR access.log`。\n\n"
            "`-c`（`--count`）只输出**匹配的行数**，不是匹配次数 —— "
            "一行里出现 10 次 `ERROR` 也只算 1。要真数「次数」得 `grep -o ERROR f | wc -l`。\n\n"
            "★ 大小写：`-i` 忽略大小写，`grep -ci error f` 会把 `Error`/`ERROR` 都算上。"
            "日志里两种写法混用是常态，别漏了 `-i`。\n\n"
            "★ `-c` 与 `grep ... | wc -l` 结果一般相同，但 `-c` **快得多**"
            "（不用把每一行都传给下一个进程）。\n\n"
            "★ **迁移**：`grep -c` 返回 0 匹配时退出码是 **1**，"
            "脚本里 `set -e` 会因此中断；用 `grep -c pattern f || true` 兜一下。"),
        tags=["grep", "-c", "计数"]))

    return out


# ===================================================================== #
#  四、命令特训 · 查找与定位
# ===================================================================== #
def part_find() -> list[dict]:
    sec = "命令特训 · 查找与定位"
    out: list[dict] = []

    out.append(C(
        "在 /etc 下按名字找所有 .conf 文件",
        "配置改错了想对照一堆同类配置。要在 `/etc` 整棵树里找出**所有** "
        "`.conf` 结尾的文件。\n\n"
        "写出这条命令。",
        ["find /etc -name '*.conf'", "find /etc -name \"*.conf\"", "find /etc -name *.conf"],
        sec=sec, diff=1,
        exp=(
            "`find /etc -name '*.conf'`。\n\n"
            "★ **引号是必须的**（判题会宽容没加引号的写法，但真实 shell 里不宽容）："
            "不加引号时 `*` 会被 shell **先展开**成当前目录下已存在的 `.conf` 文件，"
            "然后 `find` 拿到的是一个个具体文件名，语义就变成「找这几个文件」了。"
            "当前目录恰好没有 `.conf` 时 shell 会把 `*.conf` 原样传过去，"
            "于是「有时对有时错」—— 这类 bug 最难查。\n\n"
            "★ `-name` 只匹配**文件名本身**（不含路径），所以 `*.conf` 能命中 "
            "`/etc/a/b/c.conf`；要匹配整条路径得用 `-path`。\n\n"
            "★ **迁移**：找完想批量处理，别用管道接 `xargs` 带空格的文件名会断——"
            "用 `find ... -print0 | xargs -0 cmd` 或 `find ... -exec cmd {} +`。"),
        tags=["find", "-name", "通配"]))

    out.append(C(
        "忽略大小写找文件",
        "用户把文件存成了 `README`、`Readme`、`readme` 混着来。"
        "你要**不分大小写**地把它们全找出来。\n\n"
        "写出这条命令（在当前目录往下找）。",
        ["find . -iname 'readme*'", "find . -iname \"readme*\"", "find . -iname readme*"],
        sec=sec, diff=2,
        exp=(
            "`find . -iname 'readme*'`。\n\n"
            "`-iname` 就是 `-name` 的**不分大小写**版（i = insensitive）。"
            "其余行为完全一样。\n\n"
            "★ 这是 Linux 上最常见的挫败来源之一："
            "`find . -name 'readme*'` 找不到 `README.md`，"
            "因为 `-name` 用的是 **shell glob 语义，区分大小写**。\n\n"
            "★ 注意：`-iname` 是 GNU find 的扩展，"
            "POSIX 标准里没有，某些精简系统（busybox）不认。\n\n"
            "★ **迁移**：`grep -ri pattern .` 是「在文件**内容**里不分大小写地搜」，"
            "和 `-iname` 是两件事 —— "
            "一个是按**名字**找文件，一个是按**内容**找行。"),
        tags=["find", "-iname", "大小写"]))

    out.append(C(
        "找出大于 100M 的文件",
        "磁盘快满了。要找 `/var` 下**单个文件大于 100M** 的那些。\n\n"
        "写出这条命令。",
        ["find /var -size +100M", "find /var -type f -size +100M"],
        sec=sec, diff=2,
        exp=(
            "`find /var -type f -size +100M`。\n\n"
            "★ `-size` 的符号语义：\n"
            "- `+100M` 大于 100M\n"
            "- `-100M` 小于 100M\n"
            "- `100M` **恰好**等于 100M（几乎永远匹配不到，别用）\n\n"
            "★ 单位大小写很要紧：`M` = 1048576 字节，`k` = 1024 字节，"
            "`c` = 字节，`G` = 1G。写成 `-size +100m` 在 GNU find 下是**错的**"
            "（小写 `m` 不存在），会直接报错。\n\n"
            "★ 一定要加 `-type f`：不加的话目录也会被算进来，"
            "而目录的「大小」是目录项本身占的字节数，跟里面有多少东西无关，"
            "结果会莫名其妙。\n\n"
            "★ **迁移**：`du -ah /var | sort -rh | head -20` 是另一条常用路线，"
            "它按**实际占用**（含稀疏文件、硬链接去重）排，"
            "比 `find -size` 更贴近 `df` 的数字。"),
        tags=["find", "-size", "磁盘"]))

    out.append(C(
        "找出 7 天内修改过的文件",
        "排查「最近一周谁动过配置」，要在 `/etc` 下找 **mtime 在 7 天以内**的文件。\n\n"
        "写出这条命令。",
        ["find /etc -type f -mtime -7", "find /etc -mtime -7 -type f"],
        sec=sec, diff=3,
        exp=(
            "`find /etc -type f -mtime -7`。\n\n"
            "★ `-mtime` 的符号是**最反直觉**的一处，务必记准：\n"
            "- `-mtime -7` → 修改时间在 **7 天以内**（小于 7 天）\n"
            "- `-mtime +7` → 修改时间在 **7 天以前**（大于 7 天）\n"
            "- `-mtime 7` → **恰好第 7 天那一天**（24 小时为一个整数区间）\n\n"
            "记忆法：**负数表示「最近」**（数值小 = 时间近），"
            "正数表示「很久以前」。\n\n"
            "★ 三个时间参数别混：`-mtime` 内容修改时间、`-atime` 访问时间、"
            "`-ctime` **inode 变更时间**（改权限/属主/改名都会动它，"
            "内容没变它也会变）。\n\n"
            "★ **迁移**：要精确到分钟用 `-mmin -60`（60 分钟内）；"
            "要「比某个参考文件新」用 `-newer ref.txt`，做增量备份时最稳。"),
        tags=["find", "-mtime", "时间"]))

    out.append(C(
        "找出并删除所有 .tmp 临时文件",
        "`/tmp/work` 下散落了大量 `*.tmp`。要**一条命令**找出并删掉它们。\n\n"
        "要求：用 `find` 的删除动作，不要管道接 `rm`。",
        ["find /tmp/work -name '*.tmp' -delete",
         "find /tmp/work -name '*.tmp' -type f -delete"],
        sec=sec, diff=3,
        exp=(
            "`find /tmp/work -name '*.tmp' -delete`。\n\n"
            "`-delete` 是 find 的**内置动作**，边匹配边删，"
            "不经过管道，所以**天然不怕文件名里有空格或换行**。\n\n"
            "★ 为什么不用 `find ... | xargs rm`："
            "`xargs` 按**空白**切分输入，文件名里带空格就会被拆成两个参数，"
            "轻则报错、重则删错东西。真要管道必须 "
            "`find ... -print0 | xargs -0 rm`。\n\n"
            "★ `-delete` 有个顺序要求：它**必须放在所有条件之后**"
            "（`find . -delete -name '*.tmp'` 会直接把整个目录删掉，"
            "因为 `-delete` 已经执行了，后面的条件才被判）。这是 find 里最昂贵的一课。\n\n"
            "★ **迁移**：删之前先不带 `-delete` 跑一遍看清单；"
            "`-delete` 也隐含 `-depth`（先删子项），"
            "所以它和 `-prune` 不能一起用。"),
        tags=["find", "-delete", "批量删除"]))

    out.append(C(
        "找出所有 .sh 并批量加上执行权限",
        "`~/scripts` 下有一批 shell 脚本，权限都是 644，"
        "要**全部**改成可执行。\n\n"
        "要求：一条 `find` 命令搞定（用 `-exec`）。",
        ["find ~/scripts -name '*.sh' -exec chmod +x {} \\;",
         "find ~/scripts -name '*.sh' -exec chmod +x {} +",
         "find ~/scripts -name '*.sh' -type f -exec chmod +x {} +"],
        sec=sec, diff=4,
        exp=(
            "`find ~/scripts -name '*.sh' -exec chmod +x {} \\;`。\n\n"
            "`-exec` 的语法有三个**必须记住**的点：\n"
            "1. `{}` 是占位符，会被替换成当前匹配到的文件路径\n"
            "2. 结尾必须是 `\\;`（分号前加反斜杠转义，防止被 shell 吃掉）"
            "或者 `+`\n"
            "3. `\\;` 表示**每个文件执行一次**；`+` 表示**攒成一批执行一次**"
            "（更快，等价于 `xargs`，而且同样不怕空格）\n\n"
            "★ 为什么 `\\;` 要转义：`;` 在 shell 里是命令分隔符，"
            "不转义的话 shell 会在传给 `find` 之前就把它吃掉，"
            "`find` 会以为参数没结束而报错。\n\n"
            "★ **迁移**：`-exec ... {} +` 只能放在**最后**；"
            "`\\;` 可以中间再用 `-exec`。"
            "要「找到后问一句」用 `-ok`（与 `-exec` 同语法，逐个确认）。"),
        tags=["find", "-exec", "chmod", "批量"]))

    out.append(C(
        "只看当前这一层，别往下递归",
        "`/etc` 下面太深了，你只想知道 `/etc` **这一层**有哪些普通文件。\n\n"
        "写出这条命令。",
        ["find /etc -maxdepth 1 -type f", "find /etc -maxdepth 1 -type f -print"],
        sec=sec, diff=2,
        exp=(
            "`find /etc -maxdepth 1 -type f`。\n\n"
            "★ `-maxdepth 1` = 只处理 `/etc` 这**一层**（深度 1）；"
            "`-mindepth 1` = 从**子里**开始，不含 `/etc` 自己。"
            "两者组合 `-mindepth 1 -maxdepth 1` 就是「只看直接子项，不看自己」。\n\n"
            "★ 顺序很重要：`-maxdepth` 是**全局选项**，"
            "必须放在其它测试条件**之前**（GNU find 会警告，"
            "有些版本直接报错）。`find /etc -type f -maxdepth 1` 是错的。\n\n"
            "★ `-maxdepth 1` 比 `ls` 强在哪："
            "它能直接接 `-type`/`-size`/`-newer` 这些条件，"
            "而 `ls` 只能靠 `-l` 输出再 `grep` 解析。\n\n"
            "★ **迁移**：`find . -maxdepth 2 | sort` 是「看一眼目录骨架」最快的方式，"
            "比 `tree -L 2` 更通用（tree 常常没装）。"),
        tags=["find", "-maxdepth", "深度"]))

    out.append(C(
        "查一个命令的可执行文件在哪",
        "`python3` 到底在哪？脚本要用它的**绝对路径**写进 crontab。\n\n"
        "写出这条命令。",
        ["which python3", "type -p python3", "command -v python3"],
        sec=sec, diff=1,
        exp=(
            "`which python3`（或 `command -v python3`）。\n\n"
            "`which` 顺着 `$PATH` 从左到右找，返回**第一个**匹配到的可执行文件。\n\n"
            "★ 为什么 crontab 里必须写绝对路径：cron 的 `$PATH` **极短**"
            "（通常只有 `/usr/bin:/bin`），你在交互 shell 里能跑的命令它可能找不到。"
            "所以 `which` 一下再写全路径是标准做法。\n\n"
            "★ `which` 的局限：它**不认 shell 内建命令和别名**。"
            "`which cd` 会找不到（cd 是内建），"
            "`which ls` 在有 `alias ls='ls --color'` 时也可能给不出你以为的答案。\n\n"
            "★ **迁移**：`command -v` 是 POSIX 标准写法，"
            "内建/别名/函数/外部命令**都能识别**，脚本里比 `which` 更可靠。"),
        tags=["which", "command -v", "PATH"]))

    out.append(C(
        "查一个命令出现在 PATH 里的所有位置",
        "机器上装了多个 Python（系统自带 + pyenv + conda），"
        "你要看 `python3` 在 `$PATH` 里**所有**候选路径。\n\n"
        "写出这条命令。",
        ["which -a python3", "type -a python3"],
        sec=sec, diff=3,
        exp=(
            "`which -a python3`（或 `type -a python3`）。\n\n"
            "`-a`（all）让它**不提前退出**，把 `$PATH` 里所有匹配都列出来，"
            "顺序就是查找顺序 —— 第一行就是实际会被执行的那个。\n\n"
            "★ `type -a` 比 `which -a` 信息更全：它会标注每个候选是"
            "`is /path/to/x`（外部命令）、`is aliased to ...`（别名）"
            "还是 `is a shell builtin`（内建）。\n\n"
            "★ 排查「为什么跑的不是我装的版本」的完整套路：\n"
            "1. `type -a python3` 看有几个、谁是第一\n"
            "2. `echo $PATH` 看顺序（**左边优先**）\n"
            "3. 查 alias 和 `hash -r`（bash 会缓存命令路径，装了新版本要清缓存）\n\n"
            "★ **迁移**：`hash -r` 这一条能解决一大半「明明装了却还是旧版本」——"
            "bash 缓存了旧路径，新装的没被看见。"),
        tags=["which", "-a", "type", "PATH"]))

    out.append(C(
        "查命令的类型（别名 / 内建 / 外部）",
        "`cd` 到底是文件还是 shell 内建？`ll` 为什么 `which` 找不到却能敲？\n\n"
        "要求：用能**区分内建、别名、函数、外部命令**的那条命令查 `cd`。",
        ["type cd", "type -a cd"],
        sec=sec, diff=2,
        exp=(
            "`type cd`。\n\n"
            "`type` 是 shell 内建，能分辨四类东西：\n"
            "- `cd is a shell builtin` —— **内建**（没有对应的可执行文件）\n"
            "- `ll is aliased to 'ls -l --color=auto'` —— **别名**\n"
            "- `python3 is /usr/bin/python3` —— **外部命令**\n"
            "- `f is a function` —— **函数**\n\n"
            "★ 这就解释了为什么 `which cd` 什么也不输出："
            "`which` 只在 `$PATH` 目录里找**文件**，而 `cd` 是 bash 自己实现的，"
            "磁盘上根本没有 `cd` 这个可执行文件。\n\n"
            "★ 同理 `ll` 能敲是因为 `alias ll='ls -l'`，"
            "它不是命令，是**敲命令前做的文本替换**。\n\n"
            "★ **迁移**：`type -t cd` 只输出类型词（`builtin`/`alias`/`file`/`function`），"
            "写脚本时判断更好用。"),
        tags=["type", "内建", "别名"]))

    out.append(C(
        "查这个可执行文件属于哪个软件包",
        "`/usr/bin/ls` 被你误删了，想重新装回来，但不知道它属于哪个包。\n\n"
        "写出这条命令（用 rpm 系工具）。",
        ["rpm -qf /usr/bin/ls", "rpm --query --file /usr/bin/ls",
         "dnf provides /usr/bin/ls"],
        sec=sec, diff=3,
        exp=(
            "`rpm -qf /usr/bin/ls`。\n\n"
            "- `-q` query（查询）\n"
            "- `-f` file（按**文件路径**反查所属包）\n\n"
            "输出形如 `coreutils-9.4-7.fc40.x86_64`，"
            "于是 `sudo dnf reinstall coreutils` 就能装回来。\n\n"
            "★ `-qf` 只能查**已安装包**里的文件。"
            "查「哪个包**提供**某个文件」而它还没装，要用 "
            "`dnf provides '*/ls'`（`dnf whatprovides` 的别名）。\n\n"
            "★ 路径必须**完全准确**：`rpm -qf ls` 会报 `file ls is not owned` —— "
            "它要的是文件系统里的真实路径，不是命令名。所以先 `which ls` 拿到路径。\n\n"
            "★ **迁移**：卸载前先 `rpm -qf` 反查是哪个包，"
            "再 `rpm -q --whatrequires <包名>` 看谁会受影响 —— "
            "这两步能避免「卸了一个包，半个桌面没了」。"),
        tags=["rpm", "-qf", "软件包", "dnf"]))

    out.append(C(
        "找出所有空文件与空目录",
        "清理项目目录时，想先看看哪些是**空文件**、哪些是**空目录**。\n\n"
        "要求：一条 `find` 命令同时覆盖两者。",
        ["find . -empty", "find . -empty -print"],
        sec=sec, diff=3,
        exp=(
            "`find . -empty`。\n\n"
            "`-empty` 是「大小为 0 的普通文件」**或**「不含任何条目的目录」的简写，"
            "一条条件同时命中两类。\n\n"
            "★ 想只清空目录：`find . -empty -type d`；"
            "只清空文件：`find . -empty -type f`。\n\n"
            "★ 注意「空文件」的定义是 **size == 0**。"
            "一个只有换行的文件不算空（它有 1 字节），"
            "用 `-empty` 找不到它 —— 想找「只有空白行的文件」得 "
            "`find . -type f -exec grep -qL '[^[:space:]]' {} +`。\n\n"
            "★ **迁移**：`find . -empty -delete` 能一次清掉所有空文件与空目录，"
            "但 `-delete` 隐含 `-depth`，会**先删子后删父**，"
            "所以一个「只含空目录的目录」会被判定为删完之后才空……"
            "实际 GNU find 是逐层处理的，多跑一次才彻底清干净。"),
        tags=["find", "-empty", "清理"]))

    out.append(C(
        "按权限精确查找文件",
        "做安全审计，要找出**权限恰好是 `644`** 的那些文件（不含 664、600）。\n\n"
        "写出这条命令。",
        ["find . -type f -perm 644", "find . -type f -perm 0644"],
        sec=sec, diff=3,
        exp=(
            "`find . -type f -perm 644`。\n\n"
            "★ `-perm` 不带符号（`-`/`/`）时是**精确匹配**："
            "必须有且仅有这几位，664、600 都不算。\n\n"
            "★ 带符号的三档语义是本题的重点延伸：\n"
            "- `-perm -644`（减号）= **至少包含**这些位（可以更多）\n"
            "- `-perm /644`（斜杠）= **任意一位**匹配即可（或关系）\n"
            "- `-perm 644` = 精确相等\n\n"
            "★ 注意 `rwxr--r--` 这种符号写法不能直接给 `-perm`，"
            "要么换八进制，要么用符号模式 `-perm u=rwx,g=r,o=r`（GNU 扩展）。\n\n"
            "★ **迁移**：找「所有人可写」的隐患文件是 "
            "`find / -type f -perm -o+w`（减号，只要 o 位有 w 就算），"
            "这一条比精确匹配有用得多 —— 安全隐患往往是「至少」而不是「恰好」。"),
        tags=["find", "-perm", "安全审计"]))

    out.append(C(
        "找出所有设置了 SUID 的文件",
        "提权漏洞排查第一步：列出系统里所有 **SUID** 位的可执行文件。\n\n"
        "写出这条命令（从根开始，忽略错误输出）。",
        ["find / -perm -4000 -type f 2>/dev/null",
         "find / -type f -perm -4000 2>/dev/null",
         "find / -user root -perm -4000 -type f 2>/dev/null"],
        sec=sec, diff=4,
        exp=(
            "`find / -perm -4000 -type f 2>/dev/null`。\n\n"
            "`4000` 就是 SUID 位（八进制的**第四位**）。"
            "用 `-4000`（减号）而不是 `4000` 是**必须的**："
            "SUID 文件通常还有 755 之类的普通权限位，"
            "精确匹配 `4000` 只能找到「权限恰好是 4000」的，"
            "等于一个都找不到。\n\n"
            "★ `2>/dev/null` 不是可选项：`/proc`、`/sys` 下大量目录不让普通用户读，"
            "不加就会有成百上千行 `Permission denied` 淹没真正的结果。\n\n"
            "★ SUID 的含义：**执行时临时获得文件属主（通常是 root）的权限**。"
            "`/usr/bin/passwd` 就是靠它让普通用户能改自己的密码。"
            "也正因如此，被人塞进来的 SUID 程序就是提权后门。\n\n"
            "★ **迁移**：SGID 是 `2000`，sticky 是 `1000`（目录上的 `t`）。"
            "三个特殊位一起查：`find / -perm /7000`。"),
        tags=["find", "SUID", "安全", "4000"]))

    out.append(C(
        "找出所有指向已失效目标的软链（断链）",
        "目录整理完，想知道哪些软链**指向的目标已经不存在**了。\n\n"
        "写出这条命令。",
        ["find . -xtype l", "find . -type l -xtype l", "find . -type l ! -exec test -e {} \\; -print"],
        sec=sec, diff=4,
        exp=(
            "`find . -xtype l`。\n\n"
            "`-xtype` 是「按**链接指向的目标**判断类型」："
            "`-xtype l` 意思是「目标是链接」—— 而**断链的目标根本不存在，"
            "find 会把它归为 `l`**，所以这一条正好筛出所有断链。\n\n"
            "★ 为什么不用 `-type l`：那会列出**所有**软链（好的坏的都要），"
            "你还得逐个 `test -e`。`-xtype l` 一步到位。\n\n"
            "★ 另一种等价思路（可读性更好）："
            "`find . -type l ! -exec test -e {} \\; -print` —— "
            "「是链接」且「目标不存在」。\n\n"
            "★ **迁移**：`readlink -f` 对断链会返回空、"
            "`ls -l` 里断链会显示成红色（多数发行版），"
            "但这些都是逐个人眼看；批量排查只有 `-xtype l` 可靠。"),
        tags=["find", "-xtype", "断链", "软链"]))

    out.append(C(
        "找文件名里带空格的文件",
        "要把一批文件导进另一个系统，那个系统受不了文件名里的空格。\n\n"
        "先找出**名字里含空格**的普通文件。\n\n"
        "写出这条命令。",
        ["find . -type f -name '* *'", "find . -name '* *' -type f"],
        sec=sec, diff=3,
        exp=(
            "`find . -type f -name '* *'`。\n\n"
            "`'* *'` 里两个 `*` 之间是一个**空格**，所以匹配「名字里至少有一个空格」。\n\n"
            "★ 引号不能省：不写引号的话 shell 会把 `* *` 拆成两个独立参数，"
            "`find` 会收到 `-name` 后面跟两个词，语法直接错。\n\n"
            "★ 为什么空格文件名是麻烦：几乎所有按空白切分的工具都会断 —— "
            "`for f in $(ls)`、`xargs`、`awk '{print $1}'` 全废。"
            "这就是为什么「处理 find 结果」必须用 `-print0` + `xargs -0`，"
            "或者 `-exec`。\n\n"
            "★ **迁移**：批量改名用 `rename 's/ /_/g' *`（util-linux 或 perl-rename 版），"
            "或 `find . -name '* *' -exec bash -c 'mv \"$1\" \"${1// /_}\"' _ {} \\;`。"),
        tags=["find", "空格", "文件名"]))

    return out


# ===================================================================== #
#  五、命令特训 · 文本处理
# ===================================================================== #
def part_text() -> list[dict]:
    sec = "命令特训 · 文本处理"
    out: list[dict] = []

    out.append(C(
        "在日志里搜一个关键词",
        "`app.log` 里找所有包含 `timeout` 的行。\n\n"
        "写出这条命令。",
        ["grep timeout app.log", "grep 'timeout' app.log", "grep \"timeout\" app.log"],
        sec=sec, diff=1,
        exp=(
            "`grep timeout app.log`。\n\n"
            "`grep 模式 文件`：**模式在前，文件在后**。"
            "写成 `grep app.log timeout` 会去一个叫 `timeout` 的目录里找 `app.log`，"
            "报 `No such file or directory`。\n\n"
            "★ 默认输出是**整行**，不是只输出匹配到的片段。"
            "只要片段得加 `-o`。\n\n"
            "★ 默认是**正则**（BRE）。`timeout` 里没有特殊字符所以没事，"
            "但搜 `.`、`*`、`[` 这些字符时必须转义或加 `-F`（固定字符串）。\n\n"
            "★ **迁移**：`grep -F 'a.b' f` 把模式当**纯文本**，"
            "搜代码/配置里的符号时最省心（`grep -F '[INFO]' log`）。"),
        tags=["grep", "基础"]))

    out.append(C(
        "忽略大小写搜索",
        "日志里 `Error`、`ERROR`、`error` 混着出现，你想一次全抓到。\n\n"
        "写出这条命令。",
        ["grep -i error app.log", "grep -i 'error' app.log", "grep --ignore-case error app.log"],
        sec=sec, diff=1,
        exp=(
            "`grep -i error app.log`。\n\n"
            "`-i`（`--ignore-case`）让匹配不分大小写。\n\n"
            "★ 与 `-i` 容易混的两个：\n"
            "- `-w`（word）只匹配**完整单词**：`grep -w error` 不会命中 `errors`\n"
            "- `-v`（invert）**反选**：输出不匹配的行\n\n"
            "★ 组合使用非常常见：`grep -iv 'debug' app.log` = 排除掉所有 debug 行。"
            "注意 `-iv` 也能写成 `-vi`，判题与 shell 都认。\n\n"
            "★ **迁移**：日志分析的三板斧是 `-i`（不分大小写）、"
            "`-v`（排除噪声）、`-c`（只数条数）。"
            "`grep -ic error f` 一行就给出「有多少行报 error」。"),
        tags=["grep", "-i", "大小写"]))

    out.append(C(
        "过滤掉配置文件的注释行和空行",
        "`sshd_config` 里注释占了八成。你要看**实际生效的配置**："
        "去掉以 `#` 开头的行，也去掉空行。\n\n"
        "写出这条命令。",
        ["grep -v '^#' sshd_config | grep -v '^$'",
         "grep -Ev '^#|^$' sshd_config",
         "grep -vE '^(#|$)' sshd_config"],
        sec=sec, diff=3,
        exp=(
            "`grep -v '^#' sshd_config | grep -v '^$'`（或一条 `grep -Ev '^#|^$'`）。\n\n"
            "★ `^#` 匹配**行首**的 `#`，这是关键 —— 只写 `grep -v '#'` 会把"
            "「行尾注释」和「含 `#` 的值」一起删掉"
            "（比如 `PasswordAuthentication yes # 备注` 整行都会消失）。\n\n"
            "★ `^$` 匹配**空行**。注意 `$` 在正则里是行尾锚点，"
            "写成 `grep -v '^ $'` 是「含一个空格的行」，不是空行。\n\n"
            "★ `-E` 打开扩展正则，`|` 才表示「或」；"
            "不加 `-E` 时 `\\|` 才是或，`|` 是字面竖线。\n\n"
            "★ **迁移**：去掉行尾注释（`#` 及之后）用 `sed 's/#.*//'`；"
            "两者合起来 `sed -e 's/#.*//' -e '/^$/d' f` 就是「只看有效配置」。"),
        tags=["grep", "-v", "注释", "正则"]))

    out.append(C(
        "只输出匹配到的那一段，不输出整行",
        "日志行很长，你只想知道里面出现的**所有 IP 地址**。\n\n"
        "要求：只输出匹配到的片段，不要整行。",
        ["grep -oE '([0-9]{1,3}\\.){3}[0-9]{1,3}' app.log",
         "grep -o -E '([0-9]{1,3}\\.){3}[0-9]{1,3}' app.log"],
        sec=sec, diff=4,
        exp=(
            "`grep -oE '([0-9]{1,3}\\.){3}[0-9]{1,3}' app.log`。\n\n"
            "- `-o`（only-matching）**只输出匹配的那一段**，"
            "一行里有多个匹配就输出多行\n"
            "- `-E` 扩展正则，这样 `{1,3}`、`()` 才能直接用\n\n"
            "★ 正则要点：`([0-9]{1,3}\\.){3}` 表示「1~3 位数字 + 点」重复 3 次，"
            "再跟一段 1~3 位数字。`\\.` 必须转义 —— "
            "不转义的 `.` 匹配任意字符，会把 `1x2x3x4` 也算成 IP。\n\n"
            "★ 这个正则**不校验范围**（`999.999.999.999` 也会被抓），"
            "做严格校验得上 `grep -oP` 配合 lookahead，或者用 `awk` 拆段判断。\n\n"
            "★ **迁移**：`grep -o` 配合 `sort | uniq -c | sort -rn` 是"
            "「找出最高频的 XX」的标准套路 —— "
            "统计访问最多的 IP、最常见的错误码都靠它。"),
        tags=["grep", "-o", "-E", "正则"]))

    out.append(C(
        "递归搜索目录里所有文件的某个关键字",
        "`src/` 下有几十个文件，你要找**哪个文件**里写了 `TODO`。\n\n"
        "要求：输出里要能看出是哪个文件。",
        ["grep -r TODO src/", "grep -rn TODO src/", "grep -r 'TODO' src/"],
        sec=sec, diff=2,
        exp=(
            "`grep -r TODO src/`。\n\n"
            "`-r`（recursive）递归整棵目录树。"
            "**多文件/递归时 grep 会自动加文件名前缀**，所以你能看出是哪个文件。\n\n"
            "★ 只给一个文件时**不会**加前缀 —— 这与 `head` 多文件加标题的逻辑正好相反，"
            "脚本里解析时要注意。\n\n"
            "★ `-r` 与 `-R` 的差别：`-r` **不跟随**符号链接，"
            "`-R` **跟随**。跟了软链可能死循环（软链指回上级），"
            "所以默认用 `-r`。\n\n"
            "★ 加 `-n` 带行号（`grep -rn`），"
            "这是日常最常用的组合 —— 能直接 `vim +行号 文件` 跳过去。\n\n"
            "★ **迁移**：想排除 `.git`、`node_modules` 用 "
            "`grep -rn --exclude-dir={.git,node_modules} TODO .`。"),
        tags=["grep", "-r", "递归"]))

    out.append(C(
        "带行号搜索（方便直接跳转）",
        "找到报错行之后，你要用 `vim +行号 文件` 跳过去。\n\n"
        "所以搜索时必须**带上行号**。\n\n"
        "写出这条命令。",
        ["grep -n error app.log", "grep -n 'error' app.log", "grep --line-number error app.log"],
        sec=sec, diff=1,
        exp=(
            "`grep -n error app.log`。\n\n"
            "输出形如 `42:2026-10-19 connect error`——"
            "**行号 + 冒号 + 行内容**。冒号是关键分隔符，"
            "`cut -d: -f1` 就能把行号单独取出来。\n\n"
            "★ `-n` 与 `-c`、`-l` 的区分：\n"
            "- `-n` 显示**每行的行号**\n"
            "- `-c` 只给**匹配行数**\n"
            "- `-l` 只给**匹配的文件名**\n"
            "三个都是「少输出点东西」，但输出的是什么完全不同。\n\n"
            "★ **迁移**：`grep -rn` 是搜索代码的起手式；"
            "配 `--color=auto` 让命中处高亮，"
            "大多数发行版默认就是 `alias grep='grep --color=auto'`。"),
        tags=["grep", "-n", "行号"]))

    out.append(C(
        "看匹配行前后各 3 行",
        "报错信息只有一行，但**上下文**才是关键。"
        "要看每次匹配的**前 3 行和后 3 行**。\n\n"
        "写出这条命令。",
        ["grep -A 3 -B 3 error app.log", "grep -B 3 -A 3 error app.log",
         "grep -C 3 error app.log"],
        sec=sec, diff=2,
        exp=(
            "`grep -C 3 error app.log`（等价于 `-A 3 -B 3`）。\n\n"
            "- `-A n`（After）匹配行之后 n 行\n"
            "- `-B n`（Before）匹配行之前 n 行\n"
            "- `-C n`（Context）前后各 n 行\n\n"
            "★ 上下文行与匹配行之间用 `--` 分隔，"
            "上下文行本身的显示格式是 `行号-内容`（**减号**不是冒号），"
            "匹配行才是 `行号:内容`。写脚本解析时这个区别很重要。\n\n"
            "★ 上下文窗口会**合并**：两个匹配离得近时，"
            "重叠部分只输出一次，不会重复。\n\n"
            "★ **迁移**：`tail -f app.log | grep -C 5 -i error` "
            "是盯线上问题的标准组合 —— 既实时又带上下文。"),
        tags=["grep", "-A", "-B", "-C", "上下文"]))

    out.append(C(
        "把文件里的 old 全部换成 new（不破坏原文件）",
        "要预览一次全局替换的效果，**先别动原文件**，只输出替换后的内容。\n\n"
        "写出这条命令。",
        ["sed 's/old/new/g' config.txt",
         "sed -e 's/old/new/g' config.txt",
         "sed 's/old/new/g' < config.txt"],
        sec=sec, diff=2,
        exp=(
            "`sed 's/old/new/g' config.txt`。\n\n"
            "`s/旧/新/` 里的三个斜杠是分隔符，`g`（global）表示**一行内全部替换**。\n\n"
            "★ 没有 `g` 只替换**每行第一次**出现 —— "
            "这是 sed 最常见的一个坑："
            "`sed 's/a/b/' f` 对 `aaa` 得到 `baa`，加了 `g` 才得到 `bbb`。\n\n"
            "★ 默认**只输出到 stdout**，不改文件。"
            "要落盘必须 `-i`（原地改）或重定向到新文件。\n\n"
            "★ 分隔符可以换：路径里全是斜杠时写 `s|/usr/local|/opt|g` 更清爽。\n\n"
            "★ **迁移**：`sed -n 's/old/new/p'` 只打印**发生替换的行**，"
            "做「替换前先确认会影响哪些行」的检查时特别有用。"),
        tags=["sed", "s///", "替换"]))

    out.append(C(
        "原地修改文件（直接改在硬盘上）",
        "确认替换没问题了，现在要**直接把文件改掉**，不要重定向到新文件。\n\n"
        "写出这条命令。",
        ["sed -i 's/old/new/g' config.txt",
         "sed -i.bak 's/old/new/g' config.txt",
         "sed --in-place 's/old/new/g' config.txt"],
        sec=sec, diff=2,
        exp=(
            "`sed -i 's/old/new/g' config.txt`。\n\n"
            "`-i`（in-place）直接改写文件。\n\n"
            "★ **`-i` 的实现是个陷阱**：它不是真的「原地」写，"
            "而是**新建一个临时文件、写完再重命名覆盖原文件**。"
            "后果有两条：\n"
            "1. **inode 变了** —— 原文件的硬链接全部断开，"
            "正在写这个文件的进程还握着旧 inode\n"
            "2. **软链被替换成实体文件** —— `sed -i` 一个软链，"
            "软链本身变成普通文件，目标文件反而没改\n\n"
            "★ `-i.bak` 会先备份成 `config.txt.bak`，"
            "**改配置前务必带上**，出事能一秒回滚。\n\n"
            "★ GNU sed 的 `-i` 后面**不能有空格**：`-i .bak` 会被理解成"
            "「备份后缀为空」+ 一个叫 `.bak` 的脚本文件。\n\n"
            "★ **迁移**：真要保 inode（比如改日志配置），"
            "用 `sed ... > tmp && cat tmp > 原文件`（重定向回原文件不换 inode）。"),
        tags=["sed", "-i", "原地修改"]))

    out.append(C(
        "删掉文件里的所有空行",
        "整理配置或代码时，空行太多影响阅读。\n\n"
        "写出这条命令（输出到屏幕）。",
        ["sed '/^$/d' config.txt", "grep -v '^$' config.txt", "awk 'NF' config.txt"],
        sec=sec, diff=2,
        exp=(
            "`sed '/^$/d' config.txt`。\n\n"
            "`/正则/d` 是 sed 的「**匹配就删**」：`^$` 是「空行」，`d` 是 delete。\n\n"
            "★ 三种写法各有微妙差别：\n"
            "- `sed '/^$/d'` 只删**完全空**的行\n"
            "- `sed '/^[[:space:]]*$/d'` 连**只有空格/制表符**的行也删（更实用）\n"
            "- `awk 'NF'` 删掉所有**没有字段**的行（同上，且更短）\n"
            "- `grep -v '^$'` 与第一种等价\n\n"
            "★ **迁移**：合并连续空行成一行用 `cat -s f`（squeeze）；"
            "连注释一起清掉：`sed -e '/^#/d' -e '/^$/d' f`，"
            "这就是「只看有效配置」的一行版。"),
        tags=["sed", "空行", "删除"]))

    out.append(C(
        "只打印第 10 到第 20 行",
        "要给同事贴一段配置，只想要**第 10~20 行**这个区间。\n\n"
        "写出这条命令。",
        ["sed -n '10,20p' config.txt", "sed -n '10,20 p' config.txt",
         "awk 'NR>=10 && NR<=20' config.txt"],
        sec=sec, diff=2,
        exp=(
            "`sed -n '10,20p' config.txt`。\n\n"
            "★ `-n` 是必须的：不加 `-n` 时 sed 默认会**把每一行都打印一遍**，"
            "`p` 又多打一次，结果是「全文 + 区间重复一遍」。"
            "`-n` 抑制默认输出，只留 `p` 打的那部分。\n\n"
            "★ 区间是**含两端**的：`10,20p` 包含第 10 行和第 20 行，共 11 行。\n\n"
            "★ 等价写法：`awk 'NR>=10 && NR<=20'`（NR = 当前行号），"
            "或者 `head -n 20 f | tail -n 11` —— "
            "后者要自己算「11」这个数，很容易算错，不推荐。\n\n"
            "★ **迁移**：`sed -n '10,$p'` 从第 10 行到末尾；"
            "`sed -n '10~5p'` 从第 10 行起每 5 行取一行（GNU 扩展，采样日志很好用）。"),
        tags=["sed", "-n", "行区间"]))

    out.append(C(
        "按冒号分列，取每行第一列",
        "`/etc/passwd` 是冒号分隔的。你只要**所有用户名**。\n\n"
        "写出这条命令。",
        ["cut -d: -f1 /etc/passwd", "cut -d ':' -f 1 /etc/passwd",
         "awk -F: '{print $1}' /etc/passwd"],
        sec=sec, diff=2,
        exp=(
            "`cut -d: -f1 /etc/passwd`。\n\n"
            "- `-d` 指定**分隔符**，`:` 是冒号\n"
            "- `-f` 指定要**第几列**（1 起算）\n\n"
            "★ `cut` 的三个坑（都是真会踩的）：\n"
            "1. **默认分隔符是 TAB**，不是空格。用空格分隔的文本必须 `-d' '`\n"
            "2. **不合并连续分隔符**：`a::b` 用 `-d: -f2` 得到**空**，"
            "而不是 `b` —— 想要「跳过空字段」得用 awk\n"
            "3. **只能按单一字符或字节切**，不支持正则\n\n"
            "★ 所以字段数不定、有空字段的场景，`awk -F: '{print $1}'` 更稳。\n\n"
            "★ **迁移**：`cut -c1-10 f` 按**字符位置**切（不需要分隔符），"
            "处理定长格式（旧式报表）时很有用。"),
        tags=["cut", "-d", "-f", "分列"]))

    out.append(C(
        "取第 3 列，但文件是空格分隔且空格数量不固定",
        "`ps aux` 这类输出里，列之间有**多个空格**。你要取第 3 列。\n\n"
        "写出这条命令。",
        ["awk '{print $3}' file.txt", "awk '{ print $3 }' file.txt"],
        sec=sec, diff=3,
        exp=(
            "`awk '{print $3}' file.txt`。\n\n"
            "★ 这就是 **awk 与 cut 的分水岭**："
            "awk 默认按「**任意数量的空白**」切分，"
            "多个空格、前导空格都自动吃掉；"
            "而 `cut -d' '` 会把每个空格都当分隔符，"
            "`a   b` 会切出 `a`、空、空、`b`，`-f3` 拿到空串。\n\n"
            "★ 所以：**固定单字符分隔用 cut，空白分隔用 awk**。"
            "这是选工具时最实用的一条判据。\n\n"
            "★ `$0` 是整行，`$NF` 是**最后一个字段**"
            "（NF = number of fields，字段数）。"
            "`awk '{print $NF}'` 取最后一列是高频用法。\n\n"
            "★ **迁移**：`awk -F: '{print $1}'` 指定冒号分隔；"
            "`awk 'BEGIN{FS=\"\\t\"}'` 在脚本里设制表符。"),
        tags=["awk", "字段", "空格分隔"]))

    out.append(C(
        "取第 3 列数值大于 100 的行",
        "有个报表 `sales.txt`，第 3 列是金额。要筛出**金额 > 100** 的行。\n\n"
        "写出这条命令。",
        ["awk '$3 > 100' sales.txt", "awk '$3>100' sales.txt",
         "awk '$3 > 100 {print}' sales.txt"],
        sec=sec, diff=3,
        exp=(
            "`awk '$3 > 100' sales.txt`。\n\n"
            "awk 的程序结构是 `模式 { 动作 }`："
            "**模式为真就执行动作，动作省略时默认 `print $0`（打印整行）**。"
            "所以 `'$3 > 100'` 就够，不用写 `{print}`。\n\n"
            "★ 数值 vs 字符串：awk 会根据上下文自动转型。"
            "`$3 > 100` 里 `100` 是数字，awk 就把 `$3` 当数字比；"
            "但写成 `$3 > \"100\"` 就变成**字符串比较**，"
            "`\"99\" > \"100\"` 为**真**（按字典序 `9` > `1`）。这个坑非常经典。\n\n"
            "★ awk 比 grep 强的地方就在这：grep 只能按**文本模式**匹配，"
            "awk 能做**数值/逻辑判断**、跨列计算、求和。\n\n"
            "★ **迁移**：`awk '$3 > 100 {sum += $3} END {print sum}'` 求和；"
            "`awk '$3 > 100 {n++} END {print n}'` 计数。"
            "这是「统计报表」最轻量的做法，不用写 Python。"),
        tags=["awk", "条件", "数值"]))

    out.append(C(
        "按冒号取第一列，然后排序去重",
        "`/etc/passwd` 里很多用户的**登录 shell**（第 7 列）重复。"
        "你要看有哪几种 shell 在用。\n\n"
        "写出这条命令。",
        ["cut -d: -f7 /etc/passwd | sort -u",
         "cut -d: -f7 /etc/passwd | sort | uniq",
         "awk -F: '{print $7}' /etc/passwd | sort -u"],
        sec=sec, diff=3,
        exp=(
            "`cut -d: -f7 /etc/passwd | sort -u`。\n\n"
            "★ `sort -u`（unique）在排序的同时去重，一条命令干两件事。"
            "它**隐含了排序**，所以不需要额外的 `uniq`。\n\n"
            "★ 为什么不能直接 `uniq`：`uniq` 只能去掉**相邻**的重复行。"
            "没排序就 `uniq`，`a b a` 会原样保留。"
            "所以经典写法是 `sort | uniq`，或者直接 `sort -u`。\n\n"
            "★ 注意 `/etc/passwd` 第 7 列是登录 shell，"
            "`/sbin/nologin` 和 `/bin/false` 表示「不许登录」，"
            "这类账号很多 —— 它们出现在结果里是正常的。\n\n"
            "★ **迁移**：`sort f | uniq -c | sort -rn` 是"
            "「统计每种值出现多少次并按次数排」的标准三连，"
            "分析日志里的错误码、URL、IP 都用它。"),
        tags=["cut", "sort", "-u", "uniq"]))

    out.append(C(
        "统计每种取值出现了几次，按次数从多到少排",
        "`access.log` 里有一列是状态码。你要看**哪个状态码最多**。\n\n"
        "假设已经用 `awk '{print $9}' access.log` 拿到了状态码这一列。\n\n"
        "写出「统计每行出现次数并按次数降序」这条命令。",
        ["sort access.log | uniq -c | sort -rn",
         "sort access.log | uniq -c | sort -nr",
         "sort access.log | uniq -c | sort -k1,1nr"],
        sec=sec, diff=3,
        exp=(
            "`sort access.log | uniq -c | sort -rn`。\n\n"
            "三步各有分工，**顺序不能换**：\n"
            "1. `sort` —— 把相同的行排到一起（`uniq` 只认相邻重复）\n"
            "2. `uniq -c` —— 去重并**在行首加上出现次数**\n"
            "3. `sort -rn` —— 按**数字**（`-n`）**降序**（`-r`）重排\n\n"
            "★ 第二个 `sort` 的 `-n` 不能省："
            "不加的话 `10` 会排在 `9` 前面（按字典序 `1` < `9`），"
            "结果看起来「挺像那么回事」，其实完全是错的。\n\n"
            "★ `uniq -c` 的输出格式是「**空格 + 次数 + 空格 + 内容**」，"
            "次数前面有**对齐用的填充空格**，所以 `awk '{print $1}'` 比 "
            "`cut -d' ' -f1` 安全。\n\n"
            "★ **迁移**：真正的实战写法是把它接在 `awk` 后面 —— "
            "`awk '{print $9}' access.log | sort | uniq -c | sort -rn | head`，"
            "一步得到「Top 10 状态码」。"),
        tags=["sort", "uniq", "-c", "统计"]))

    out.append(C(
        "把文件里所有小写字母转成大写",
        "要把一个单词表全部转成大写。\n\n"
        "写出这条命令（输出到屏幕，不改原文件）。",
        ["tr 'a-z' 'A-Z' < words.txt", "tr a-z A-Z < words.txt",
         "tr '[:lower:]' '[:upper:]' < words.txt"],
        sec=sec, diff=2,
        exp=(
            "`tr 'a-z' 'A-Z' < words.txt`。\n\n"
            "★ **`tr` 只从标准输入读，不接受文件名参数**。"
            "写 `tr 'a-z' 'A-Z' words.txt` 会把 `words.txt` 当成"
            "**第二组要替换的字符**，然后把终端挂在那里等输入。"
            "这是 `tr` 最容易踩的一脚。\n\n"
            "★ `'a-z' 'A-Z'` 是**字符区间**映射，不是「把字符串 a-z 换掉」。"
            "`tr` 逐字符一一对应替换，所以能正确做大小写转换。\n\n"
            "★ 想**原地改**：`tr ... < f > tmp && mv tmp f`（不能直接 `> f`，"
            "shell 会先截断 f，`tr` 读到空文件）。\n\n"
            "★ **迁移**：`tr -d '\\r'` 干掉 Windows 换行残留（超高频）；"
            "`tr -s ' '` 把连续空格压成一个；"
            "`tr -cd '0-9'` 只保留数字（`-c` 取补集、`-d` 删除）。"),
        tags=["tr", "大小写", "标准输入"]))

    out.append(C(
        "比较两个文件有什么不同",
        "`config.old` 和 `config.new` 改了什么？要看出**具体哪几行不一样**。\n\n"
        "写出这条命令。",
        ["diff config.old config.new", "diff -u config.old config.new"],
        sec=sec, diff=2,
        exp=(
            "`diff config.old config.new`。\n\n"
            "默认输出的三个符号要会读：\n"
            "- `a`（add）—— 右边多了行\n"
            "- `d`（delete）—— 左边多了行\n"
            "- `c`（change）—— 两边都有但不同\n"
            "行号格式是 `旧文件行号 动作 新文件行号`。\n\n"
            "★ `-u`（unified）输出**带上下文的补丁格式**（`---`/`+++`/`@@`），"
            "这才是能用 `patch` 应用的格式，也是 `git diff` 的默认样式。"
            "肉眼看也比默认格式清楚得多。\n\n"
            "★ `-u` 还有个好处：`diff -u a b > p.patch` 之后 "
            "`patch -p0 < p.patch` 就能打上。\n\n"
            "★ **迁移**：`diff <(cmd1) <(cmd2)` 能直接比较**两条命令的输出**，"
            "不用先落盘（bash 进程替换）。"
            "比较目录用 `diff -r dir1 dir2`。"),
        tags=["diff", "-u", "比较"]))

    out.append(C(
        "取两个文件共有的行",
        "`a.txt` 和 `b.txt` 各有一批 ID。你要**同时出现在两个文件里**的那些。\n\n"
        "写出这条命令。",
        ["comm -12 a.txt b.txt", "comm -1 -2 a.txt b.txt"],
        sec=sec, diff=4,
        exp=(
            "`comm -12 a.txt b.txt`。\n\n"
            "★ `comm` 的前提**必须满足**：两个文件都**已排序**，"
            "否则结果不可信。没排序先 `sort -o a.txt a.txt`。\n\n"
            "它的输出是**三栏**：\n"
            "- 第 1 栏：只在 a 里的\n"
            "- 第 2 栏：只在 b 里的\n"
            "- 第 3 栏：两边都有的\n\n"
            "`-1`/`-2`/`-3` 就是「**去掉第 N 栏**」，所以 `-12` = 只留第 3 栏 = 交集。\n"
            "同理 `-13` = 只在 b 里的，`-23` = 只在 a 里的。\n\n"
            "★ 想要**并集**就三栏全留（不加选项，但要自己处理缩进）。\n\n"
            "★ **迁移**：`comm` 比 `grep -Ff` 精确（后者是子串匹配，"
            "`abc` 会命中 `xabcd`）；要交集又不想先排序，"
            "可以用 `awk 'NR==FNR{a[$0];next} $0 in a' a.txt b.txt`。"),
        tags=["comm", "交集", "排序"]))

    out.append(C(
        "把制表符换成 4 个空格",
        "代码里混进了制表符，编辑器显示不对齐。要统一换成 4 个空格。\n\n"
        "写出这条命令（输出到屏幕）。",
        ["expand -t 4 code.c", "expand -t4 code.c", "sed 's/\\t/    /g' code.c"],
        sec=sec, diff=3,
        exp=(
            "`expand -t 4 code.c`。\n\n"
            "`expand` 是专门干这件事的工具：把 **TAB 展开成空格**，"
            "`-t 4` 指定制表宽度为 4。反向操作是 `unexpand`。\n\n"
            "★ 为什么优先 `expand` 而不是 `sed 's/\\t/    /g'`："
            "TAB 在**列对齐**时不是一个固定宽度 —— 它把光标推到下一个制表位。"
            "所以 `a\\tb` 里的 TAB 展开后**可能是 1~8 个空格**，取决于 `a` 的长度。"
            "`expand` 会按列位置正确计算，`sed` 只会无脑换成固定数量。\n\n"
            "★ 原地改：`expand -t 4 f > tmp && mv tmp f`。\n\n"
            "★ **迁移**：`expand -i` 只转**行首**的 TAB（保留缩进之外的 TAB），"
            "处理 Makefile 时要格外小心 —— "
            "**Makefile 的缩进必须是真 TAB**，一转就废。"),
        tags=["expand", "制表符", "缩进"]))

    out.append(C(
        "只保留文件里的数字",
        "有个文件混着字母和数字（如 `abc123def456`），你只想把**所有数字**提取出来。\n\n"
        "写出这条命令（输出到屏幕）。",
        ["tr -cd '0-9' < mixed.txt", "tr -cd '[:digit:]' < mixed.txt"],
        sec=sec, diff=4,
        exp=(
            "`tr -cd '0-9' < mixed.txt`。\n\n"
            "两个选项叠在一起：\n"
            "- `-c`（complement）取**补集**，即「除 0-9 之外的字符」\n"
            "- `-d`（delete）**删除**这些字符\n\n"
            "合起来 = 删掉所有非数字 = 只留数字。"
            "顺序可以写 `-cd` 或 `-dc`，都对。\n\n"
            "★ 注意它**会连换行一起删**（换行不是数字），"
            "所以输出会变成一整行 `123456...`。"
            "想保留行结构，得按行处理（`sed 's/[^0-9]//g'` 不会删换行）。\n\n"
            "★ **迁移**：`tr -d '[:space:]'` 删掉所有空白（含换行、TAB）；"
            "`tr -cd '[:print:]'` 只留可见字符（清二进制垃圾很有效）。"),
        tags=["tr", "-c", "-d", "提取"]))

    out.append(C(
        "把多行合并成一行（用逗号分隔）",
        "文件里每行一个 IP，你要拼成 `1.1.1.1,2.2.2.2,...` 这样一行。\n\n"
        "写出这条命令。",
        ["paste -sd, ips.txt", "paste -s -d, ips.txt", "paste -sd ',' ips.txt"],
        sec=sec, diff=4,
        exp=(
            "`paste -sd, ips.txt`。\n\n"
            "- `-s`（serial）把**整个文件**当一组，按行串起来（而不是默认的并排多列）\n"
            "- `-d,` 指定**分隔符**为逗号\n\n"
            "★ 不加 `-s` 时 `paste` 是「把多个文件**按列并排**」，"
            "完全不同的用途（`paste a b` 会得到 `a1 b1` 这样的两列）。\n\n"
            "★ 结果**末尾会多一个逗号**（因为每行后面都加分隔符）——"
            "要干净的输出得再 `sed 's/,$//'`。\n\n"
            "★ `-d` 支持列表轮换：`-d',\\n'` 表示「逗号、换行交替」，"
            "能把长列表折成每行 N 个。\n\n"
            "★ **迁移**：`paste - - < f` 把单列变成两列；"
            "`paste -d' ' a b c` 把三个文件并成三列 —— "
            "生成对账表格时比 `awk` 省事。"),
        tags=["paste", "-s", "-d", "合并"]))

    return out


# ===================================================================== #
#  六、命令特训 · 权限与属性
# ===================================================================== #
def part_perm() -> list[dict]:
    sec = "命令特训 · 权限与属性"
    out: list[dict] = []

    out.append(C(
        "给脚本加上可执行权限（不改变其他位）",
        "`deploy.sh` 现在是 `644`，要让它能直接 `./deploy.sh` 跑起来。\n\n"
        "要求：**只加执行位**，别改动读写位。",
        ["chmod +x deploy.sh", "chmod a+x deploy.sh", "chmod ugo+x deploy.sh"],
        sec=sec, diff=1,
        exp=(
            "`chmod +x deploy.sh`。\n\n"
            "`+x` 不给「谁」时，等价于 **`a+x`（所有人）**，"
            "但实际行为是「**只给那些已经有某种执行位的身份加 x**」——"
            "所以 `644` 会变成 `755`，`640` 会变成 `750`。这是最常用也最安全的一档。\n\n"
            "★ 只想让属主能跑：`chmod u+x f`（得到 `744`）。"
            "放在公共目录里给别人也要跑的，才用 `a+x`。\n\n"
            "★ 目录的 `x` 意义不同：目录的 `x` 是「**能进入/穿过**」"
            "（`cd` 进去、访问里面的文件）。"
            "对一个目录执行 `chmod +x` 会让人可以 `cd` 进去，"
            "但看不见里面有什么（那需要 `r`）。\n\n"
            "★ **迁移**：`chmod -x f` 是收回执行位；"
            "`chmod =x` 会把**其他所有位清掉**只留 x —— "
            "`=` 是覆盖，别当成「加」。"),
        tags=["chmod", "+x", "执行权限"]))

    out.append(C(
        "把一个目录树全部设成 755（目录）和 644（文件）",
        "网站根目录被人改乱了权限，要**规范化**："
        "所有目录 `755`、所有普通文件 `644`。\n\n"
        "写出这两条命令（一条处理目录，一条处理文件）。",
        ["find /var/www -type d -exec chmod 755 {} \\; && find /var/www -type f -exec chmod 644 {} \\;",
         "find /var/www -type d -exec chmod 755 {} + && find /var/www -type f -exec chmod 644 {} +"],
        sec=sec, diff=4,
        exp=(
            "分两条，各管一类：\n"
            "```bash\n"
            "find /var/www -type d -exec chmod 755 {} \\;\n"
            "find /var/www -type f -exec chmod 644 {} \\;\n"
            "```\n\n"
            "★ 为什么不能一句 `chmod -R 755 /var/www`："
            "那会把**文件**也变成 `755`（可执行）。"
            "普通文件多一个 `x` 位虽然大多无害，但会让"
            "「哪些是脚本」这件事彻底失去意义，安全审计也会报一堆可疑项。\n\n"
            "★ 目录要 `x` 才能真正进去，所以目录不能给 `644` —— "
            "反过来文件不该给 `755`，这是权限规范化的核心两条。\n\n"
            "★ 用 `-exec ... +` 比 `\\;` 快得多（攒批执行，少 fork 很多次）。\n\n"
            "★ **迁移**：`chmod -R a+rX dir` 里的**大写 `X`** 是专门解决这件事的 —— "
            "「目录加 x，文件只在**原本就有 x** 时才加 x」，"
            "一条命令就能安全递归授权。"),
        tags=["chmod", "递归", "规范化", "find"]))

    out.append(C(
        "把目录设成「只有属主能删自己文件」的粘滞位",
        "你建了个公共上传目录 `/srv/share`，所有人可写，"
        "但要求**每个人只能删自己的文件**（不能删别人的）。\n\n"
        "写出这条命令。",
        ["chmod 1777 /srv/share", "chmod +t /srv/share", "chmod o+t /srv/share"],
        sec=sec, diff=4,
        exp=(
            "`chmod 1777 /srv/share`（或 `chmod +t /srv/share`）。\n\n"
            "`1777` 开头的 **`1` 就是 sticky 位**（粘滞位），"
            "长格式里显示为权限串最后的 **`t`**：`drwxrwxrwt`。"
            "`/tmp` 就是标准的 `1777`。\n\n"
            "★ 它解决的问题：目录有 `w` 位时，"
            "任何有写权限的人都能**删除目录里任何文件**（哪怕文件不是他的）。"
            "加了 sticky 位，就只能删**自己的**文件或自己是属主的。\n\n"
            "★ 特殊位三兄弟的八进制位置："
            "**SUID = 4000、SGID = 2000、sticky = 1000**，"
            "都写在普通三位之前（所以是四位数）。\n\n"
            "★ **迁移**：`ls -ld /tmp` 看一眼就知道什么是标准配置；"
            "去掉粘滞位是 `chmod -t dir`。"),
        tags=["chmod", "sticky", "1777", "/tmp"]))

    out.append(C(
        "让一个程序以文件属主的身份运行（SUID）",
        "有个工具脚本需要读 `/etc/shadow`，普通用户没权限。\n"
        "你要给它加 **SUID** 位，让它执行时临时获得属主权限。\n\n"
        "写出这条命令。",
        ["chmod u+s tool", "chmod 4755 tool", "chmod 4u+s tool"],
        sec=sec, diff=4,
        exp=(
            "`chmod u+s tool`（数字写法 `chmod 4755 tool`）。\n\n"
            "- `u+s` 给**属主位**加 SUID，长格式显示属主的 `x` 变成 **`s`**："
            "`-rwsr-xr-x`\n"
            "- 如果原本属主**没有 `x`**，`s` 会显示成**大写 `S`** —— "
            "那是「有 SUID 但不可执行」的无效状态，等于白设\n\n"
            "★ 数字写法：`4` 是 SUID 的位置，写在三位权限之前，"
            "所以 `755 + SUID` = `4755`。\n\n"
            "★ **安全警告**：SUID 是提权漏洞的头号载体。"
            "给 shell 脚本加 SUID **在 Linux 上通常无效**"
            "（内核会忽略脚本的 SUID 位），"
            "而且能被利用的 SUID 程序等于给了所有人 root。"
            "能用 `sudo` 精确授权就别用 SUID。\n\n"
            "★ **迁移**：SGID（`g+s` / `2000`）对**目录**的意义不同 —— "
            "在该目录里新建的文件会**继承目录的属组**，"
            "这是团队共享目录的标准做法。"),
        tags=["chmod", "SUID", "u+s", "安全"]))

    out.append(C(
        "查看文件的八进制权限（不要符号位）",
        "脚本里要判断某个文件的权限是不是 `600`，需要**纯数字**。\n\n"
        "写出这条命令。",
        ["stat -c '%a' secret.key", "stat -c %a secret.key", "stat -c '%a %n' secret.key"],
        sec=sec, diff=3,
        exp=(
            "`stat -c '%a' secret.key`。\n\n"
            "`stat` 的 `-c`（`--format`）可以自定义输出格式，`%a` = **八进制权限**。"
            "输出形如 `600`（不带前导 0，所以别拿它直接和 `0600` 字符串比较）。\n\n"
            "★ 其他常用占位符：\n"
            "- `%A` 符号位（`-rw-------`）\n"
            "- `%U` 属主名、`%G` 属组名\n"
            "- `%s` 字节大小、`%n` 文件名\n"
            "- `%i` inode 号\n\n"
            "★ 想要 `0600` 带前导零的格式用 `%04a`。\n\n"
            "★ **迁移**：`find . -perm 600` 是按权限查文件；"
            "`stat -c '%a'` 是**看某一个**文件。"
            "批量审计时用前者，单点确认用后者。"),
        tags=["stat", "%a", "八进制"]))

    out.append(C(
        "查看文件的符号权限与属主（一行说清）",
        "要在一个脚本里同时拿到**权限串 + 属主 + 属组 + 文件名**。\n\n"
        "写出这条命令。",
        ["stat -c '%A %U %G %n' file", "stat -c '%A %U:%G %n' file",
         "ls -l file"],
        sec=sec, diff=3,
        exp=(
            "`stat -c '%A %U %G %n' file`。\n\n"
            "输出形如 `-rw-r--r-- root root app.conf` —— "
            "**格式由你定**，这是 `stat` 比 `ls -l` 强的地方："
            "`ls -l` 的列宽与顺序是给人看的，字段位置随内容浮动；"
            "`stat -c` 的输出**字段顺序固定**，脚本里 `cut`/`awk` 才可靠。\n\n"
            "★ `%A` 是符号权限（10 位，含文件类型位）；"
            "`%a` 是八进制权限（3~4 位数字）。差一个大小写，意思完全不同。\n\n"
            "★ 为什么不用 `ls -l | awk '{print $1}'`："
            "文件名里有空格时 `ls` 的列会错位；"
            "`stat -c` 按文件名逐个处理，不受影响。\n\n"
            "★ **迁移**：`stat -c '%y'` 看人类可读的修改时间，"
            "`%Y` 是 Unix 时间戳 —— 写「文件是不是 24 小时没更新了」的判断时用后者。"),
        tags=["stat", "%A", "属主", "ls -l"]))

    out.append(C(
        "只改属组，不动属主",
        "`/srv/data/report.csv` 的属主是对的，但属组要改成 `dev`。\n\n"
        "写出这条命令。",
        ["chgrp dev /srv/data/report.csv", "chown :dev /srv/data/report.csv"],
        sec=sec, diff=2,
        exp=(
            "`chgrp dev /srv/data/report.csv`（或 `chown :dev 文件`）。\n\n"
            "`chgrp` 是「change group」的专用命令，只动属组。"
            "`chown :dev` 里冒号前留空，也是「只改属组」的意思 —— "
            "两种写法效果一样，`chgrp` 语义更清楚。\n\n"
            "★ 权限要求：普通用户只能把文件的属组改成**自己所属的组**"
            "（`id` 里能看到的那几个）；改到别的组需要 root。\n\n"
            "★ 递归改整棵树：`chgrp -R dev /srv/data`。\n\n"
            "★ **迁移**：`chown user: file` 里的冒号后留空 = "
            "「属组改成该用户的**登录主组**」，"
            "很多人以为那是「属组不变」，其实变了 —— 这点极易搞混。"),
        tags=["chgrp", "属组", "chown"]))

    out.append(C(
        "给单个用户单独授权（不改变文件属主）",
        "`project/` 属于 `alice`，但要让 `bob` 也能读写里面的内容，"
        "而**不能改属主**（alice 还要用）。\n\n"
        "要求：用 ACL 给 bob 单独授权（递归）。",
        ["setfacl -R -m u:bob:rw project/",
         "setfacl -Rm u:bob:rw project/",
         "setfacl --recursive -m u:bob:rw project/"],
        sec=sec, diff=4,
        exp=(
            "`setfacl -R -m u:bob:rw project/`。\n\n"
            "ACL（Access Control List）解决的就是传统 9 位权限做不到的事："
            "**给特定某个人单独授权**，而不是只能按「属主/组/其他」三档。\n\n"
            "★ 参数拆解：\n"
            "- `-m`（modify）修改 ACL 条目\n"
            "- `u:bob:rw` 用户 bob 给读写权限\n"
            "- `-R` 递归\n\n"
            "★ 递归设完还要 `setfacl -R -d -m u:bob:rw project/` 设**默认 ACL**，"
            "否则**之后新建**的文件不会继承这条授权 —— "
            "这是 ACL 最常被漏掉的一步。`-d` 就是「default」。\n\n"
            "★ 设完之后 `ls -l` 会在权限串末尾多一个 **`+`** 号"
            "（`-rw-rw-r--+`），表示「这个文件有扩展 ACL」。\n\n"
            "★ **迁移**：`getfacl project/` 查看，`setfacl -x u:bob project/` 撤销，"
            "`setfacl -b` 清空所有 ACL。"),
        tags=["setfacl", "ACL", "授权"]))

    out.append(C(
        "查看文件上的 ACL 规则",
        "有个文件的权限串末尾带 `+`，你要看它到底给了谁什么权限。\n\n"
        "写出这条命令。",
        ["getfacl file", "getfacl -p file"],
        sec=sec, diff=2,
        exp=(
            "`getfacl file`。\n\n"
            "输出会列出：\n"
            "- `# file:` / `# owner:` / `# group:` 注释行\n"
            "- `user::rw-`（属主，两个冒号之间为空）\n"
            "- `user:bob:rw-`（**具名用户**，这就是 ACL 加的那条）\n"
            "- `group::r--`（属组）\n"
            "- `mask::rw-`（**有效权限上限**）\n"
            "- `other::r--`\n\n"
            "★ `mask` 是 ACL 的核心概念：**所有具名用户和组的权限都会被 mask 截断**。"
            "所以 `user:bob:rwx` + `mask::r--` 实际只有 `r`。"
            "「明明给了 rwx 却不能用」八成就是 mask 挡着。\n\n"
            "★ 只想看有效权限：`getfacl -e file`。\n\n"
            "★ **迁移**：`getfacl -R dir > acl.txt` 备份、"
            "`setfacl --restore=acl.txt` 恢复 —— "
            "迁移目录时比手动重设省太多事。"),
        tags=["getfacl", "ACL", "mask"]))

    out.append(C(
        "批量找出所有「其他人可写」的文件",
        "安全审计：找出系统里**任何用户都能写**的文件（这是提权风险）。\n\n"
        "写出这条命令（从 /etc 开始，忽略错误）。",
        ["find /etc -type f -perm -o+w 2>/dev/null",
         "find /etc -type f -perm /o+w 2>/dev/null",
         "find /etc -type f -perm -002 2>/dev/null"],
        sec=sec, diff=4,
        exp=(
            "`find /etc -type f -perm -o+w 2>/dev/null`。\n\n"
            "★ 必须用**减号** `-o+w`（或 `/o+w`），不能用 `-perm o+w`："
            "不带符号是「精确相等」，而「其他人可写」的文件通常还带一堆别的位，"
            "精确匹配等于什么都找不到。\n\n"
            "★ `-o+w` 与 `-002` 是同一件事的两种写法"
            "（`002` 是「其他」位的写权限）。符号写法可读性更好。\n\n"
            "★ 这类文件为什么危险：`/etc/cron.d/` 下如果有个人人可写的文件，"
            "任何用户都能往里塞定时任务，直接提权到 root。\n\n"
            "★ **迁移**：配合 `-ls` 看详情："
            "`find /etc -perm -o+w -ls`；"
            "查目录用 `-type d`（目录人人可写同样是大事，"
            "`/tmp` 除外——它有 sticky 位保护）。"),
        tags=["find", "-perm", "安全", "o+w"]))

    out.append(C(
        "看当前 umask 值",
        "新建文件默认是 `644`、目录是 `755`，这个「默认」由 umask 决定。\n\n"
        "要求：把当前 umask **以符号形式**显示出来。",
        ["umask -S", "umask"],
        sec=sec, diff=3,
        exp=(
            "`umask -S`（符号形式）。\n\n"
            "两种输出的区别：\n"
            "- `umask` → `0022`（**遮掉的位**）\n"
            "- `umask -S` → `u=rwx,g=rx,o=rx`（**实际允许的位**）\n\n"
            "★ umask 是**掩码**，算的是「减」：\n"
            "- 文件基准是 `666`，`666 - 022` = `644`\n"
            "- 目录基准是 `777`，`777 - 022` = `755`\n\n"
            "★ 注意「减」不是十进制减法，是**按位去掉**。"
            "所以 `umask 027` 得到文件 `640`、目录 `750`。\n\n"
            "★ `umask` 只影响**新建**的文件，对已存在的文件毫无作用 —— "
            "这是它与 `chmod` 最本质的区别。\n\n"
            "★ **迁移**：临时改用 `umask 077`（会话内有效）；"
            "永久改写到 `/etc/profile` 或 `~/.bashrc`。"
            "共享目录想让新文件归属组可写，用 `umask 002`。"),
        tags=["umask", "-S", "默认权限"]))

    out.append(C(
        "递归把整个目录的属主改成 www-data",
        "网站文件被 root 拷进去了，现在要整体交给 `www-data`（保持属组不变）。\n\n"
        "写出这条命令。",
        ["chown -R www-data /var/www/html",
         "chown -R www-data:www-data /var/www/html",
         "chown --recursive www-data /var/www/html"],
        sec=sec, diff=2,
        exp=(
            "`chown -R www-data /var/www/html`。\n\n"
            "★ 只写用户名 = **只改属主**，属组保持原样。"
            "要连属组一起改是 `www-data:www-data`（或 `www-data.www-data`）。\n\n"
            "★ 两者的选择：很多场景**属组保持不变更好**，"
            "因为组权限可能是刻意配的（比如 `nginx` 组）。"
            "盲目 `chown -R user:group` 会把组的授权关系一起冲掉。\n\n"
            "★ `-R` 对软链默认**不跟随**（改的是链接自身）。"
            "想连目标一起改要 `-h`（改链接）或 `-L`（改目标），"
            "但 `-L` 有跟到 `/` 的风险，慎用。\n\n"
            "★ **迁移**：`chown -R --from=root www-data /var/www` "
            "只改**原本属主是 root** 的那些，"
            "避免把已正确设置的目录也重刷一遍（大目录树能省很多时间）。"),
        tags=["chown", "-R", "www-data"]))

    out.append(C(
        "确认某个目录的权限串到底对不对（含特殊位）",
        "排查「为什么别人进不去 `/srv/share`」，你要看**这个目录本身**的完整权限串。\n\n"
        "写出这条命令。",
        ["ls -ld /srv/share", "stat -c '%A %U:%G %n' /srv/share"],
        sec=sec, diff=2,
        exp=(
            "`ls -ld /srv/share`。\n\n"
            "★ `-d` 是关键：`ls -l /srv/share` 列的是**里面**的东西，"
            "要看目录自己必须 `-d`。\n\n"
            "★ 读权限串的四个要点：\n"
            "1. 第一个字符是**类型**：`d` 目录、`-` 文件、`l` 软链\n"
            "2. 后 9 位分三组：属主 / 属组 / 其他\n"
            "3. **特殊位**会覆盖 `x` 的位置：`s`（SUID/SGID）、`t`（sticky）、"
            "大写 `S`/`T` 表示「有位但没 `x`」（无效状态）\n"
            "4. 末尾的 `+` 表示有 ACL，`.` 表示有 SELinux 上下文\n\n"
            "★ 「进不去」的排查顺序：\n"
            "- 目录本身有没有 `x`（没有 `x` 就 `cd` 不进去）\n"
            "- 路径上**每一级**父目录有没有 `x`（少一级都不行）\n"
            "- SELinux 有没有拦（`ls -Z` 看上下文）\n\n"
            "★ **迁移**：`namei -l /srv/share` 一次列出**整条路径每一级**的权限，"
            "这是排查「进不去」最快的工具。"),
        tags=["ls", "-ld", "权限串", "排查"]))

    out.append(C(
        "把文件的属主和属组换成数字 UID/GID",
        "容器里没有对应的用户名（`/etc/passwd` 里查不到），"
        "只能用数字 ID 1000:1000 改属主。\n\n"
        "写出这条命令。",
        ["chown 1000:1000 file", "chown -R 1000:1000 file"],
        sec=sec, diff=3,
        exp=(
            "`chown 1000:1000 file`。\n\n"
            "★ `chown` 完全接受**数字 UID/GID**，不需要先建用户。"
            "这在容器/挂载卷场景是刚需 —— "
            "宿主机上的 UID 到容器里往往没有对应名字，`ls -l` 会直接显示数字。\n\n"
            "★ 为什么不建议用名字：`chown www-data` 依赖当前系统的 `/etc/passwd`；"
            "换台机器（或容器）用户名可能不同甚至不存在，脚本就崩了。"
            "用**数字**才是可移植的。\n\n"
            "★ 但数字的代价是可读性差 —— 所以「在配置文件里写数字、"
            "在注释里写名字」是常见折中。\n\n"
            "★ **迁移**：`ls -n` 以数字形式显示属主属组，"
            "排查「这个 UID 到底是谁」时先用它，再 `id -nu <uid>` 反查名字。"),
        tags=["chown", "UID", "GID", "容器"]))

    out.append(C(
        "去掉文件的 SUID 位（安全加固）",
        "审计发现 `/usr/local/bin/oldtool` 带着 SUID，要**去掉这个危险位**。\n\n"
        "写出这条命令。",
        ["chmod u-s /usr/local/bin/oldtool", "chmod 0755 /usr/local/bin/oldtool"],
        sec=sec, diff=3,
        exp=(
            "`chmod u-s /usr/local/bin/oldtool`。\n\n"
            "`u-s` 精确地只摘掉 SUID，其他位一个不动 —— 这是最安全的手术式做法。\n\n"
            "★ `chmod 0755` 也能达到效果（四位数写 `0` 前缀就是显式声明无特殊位），"
            "但它**顺带把权限重设成 755** —— "
            "如果原文件是 `4711`，你会把属组/其他的执行位也一起改掉。"
            "「精确去掉一位」和「重设整个权限」是两件事。\n\n"
            "★ 为什么写成 `0755` 而不是 `755`："
            "四位数时最高位就是特殊位，`0755` 明确表示「SUID/SGID/sticky 全为 0」。"
            "`755` 会被理解成三位权限、特殊位不动 —— "
            "**这就是去掉 SUID 时 `755` 不管用的原因**（实际 GNU chmod 会把 `755` 当 `0755` 处理，"
            "但写全四位更不容易误解）。\n\n"
            "★ **迁移**：批量清理：`find / -perm -4000 -type f -exec chmod u-s {} +`，"
            "但**先确认清单**——把 `/usr/bin/passwd`、`/usr/bin/sudo` 的 SUID 去掉会锁死系统。"),
        tags=["chmod", "u-s", "SUID", "加固"]))

    return out


# ===================================================================== #
#  七、命令特训 · 用户与组
# ===================================================================== #
def part_user() -> list[dict]:
    sec = "命令特训 · 用户与组"
    out: list[dict] = []

    out.append(C(
        "建一个新用户并顺手建家目录",
        "要给实习生开账号 `zhangsan`，家目录默认位置，"
        "**同时创建家目录**并把骨架文件拷进去。\n\n"
        "写出这条命令。",
        ["useradd -m zhangsan", "useradd --create-home zhangsan",
         "adduser zhangsan"],
        sec=sec, diff=2,
        exp=(
            "`useradd -m zhangsan`。\n\n"
            "★ **`-m` 在不同发行版上默认值相反**，这是最大的一处坑：\n"
            "- **Fedora / RHEL / CentOS**：默认 **不** 建家目录，必须写 `-m`\n"
            "- **Debian / Ubuntu**：`useradd` 默认不建，但 `adduser` 会建\n\n"
            "没建家目录的后果：登录后落在 `/`，`~/.bashrc` 不存在，"
            "一切「用户配置」都失效，而且**不会报错**——只是到处不对劲。\n\n"
            "★ `adduser` 是发行版的**友好封装**（Fedora 上它其实是 `useradd` 的软链，"
            "Debian 上是个交互式脚本）。脚本里要可移植，用 `useradd` 并把选项写全。\n\n"
            "★ **迁移**：`useradd -m -s /bin/bash -G wheel zhangsan` "
            "一次把家目录、shell、附加组都定好，比事后 `usermod` 三次干净。"),
        tags=["useradd", "-m", "家目录"]))

    out.append(C(
        "改用户的登录 shell",
        "`zhangsan` 现在的 shell 是 `/bin/sh`，要改成 `/bin/bash`。\n\n"
        "写出这条命令。",
        ["usermod -s /bin/bash zhangsan", "usermod --shell /bin/bash zhangsan",
         "chsh -s /bin/bash zhangsan"],
        sec=sec, diff=2,
        exp=(
            "`usermod -s /bin/bash zhangsan`。\n\n"
            "`-s`（`--shell`）改的是 `/etc/passwd` 第 7 个字段。\n\n"
            "★ 三个必须同时满足才会生效：\n"
            "1. 目标 shell **必须写在 `/etc/shells` 里**，"
            "否则登录程序（`login`/`sshd`）会拒绝并回退到 `/bin/sh`\n"
            "2. 用户**当前没登录**时才能改（正在用的话改完不生效，下次登录才生效）\n"
            "3. 文件本身可执行\n\n"
            "★ `chsh -s /bin/bash zhangsan` 也能改，"
            "但它是**交互式**的（会问你密码），脚本里不适合，"
            "而且需要 `util-linux-user` 包。\n\n"
            "★ **迁移**：`grep zhangsan /etc/passwd | cut -d: -f7` "
            "直接查当前 shell，比 `finger` 之类的工具可靠。"),
        tags=["usermod", "-s", "shell"]))

    out.append(C(
        "把用户加到一个附加组（不动主组）",
        "要让 `zhangsan` 能用 `sudo`，需要把他加进 `wheel` 组。\n\n"
        "要求：**保留**他原有的其他附加组，只新增一个。",
        ["usermod -aG wheel zhangsan", "usermod -a -G wheel zhangsan",
         "gpasswd -a zhangsan wheel"],
        sec=sec, diff=3,
        exp=(
            "`usermod -aG wheel zhangsan`。\n\n"
            "★ **`-a` 绝对不能漏** —— 这是 Linux 用户管理里最著名的一脚："
            "`usermod -G wheel zhangsan`（没有 `-a`）会把用户的附加组**整个替换**成 "
            "`wheel`，之前加的所有组（`docker`、`libvirt`…）**全部丢失**。"
            "而且没有任何提示。\n\n"
            "记忆法：`-a` = append（追加），`-G` = 附加组（groups）。"
            "**改附加组永远要 `-aG`**。\n\n"
            "★ 注意大小写：`-G` 是附加组，`-g` 是**主组**（会改 `/etc/passwd` 第 4 字段）。"
            "`-g` 用错了用户的家目录归属关系都会变。\n\n"
            "★ **迁移**：`gpasswd -a user group` 是另一种写法（同样安全，"
            "不会有覆盖问题）；`groups zhangsan` 或 `id zhangsan` 验证结果。"),
        tags=["usermod", "-aG", "附加组", "wheel"]))

    out.append(C(
        "设置/修改用户密码",
        "给 `zhangsan` 设密码（交互式输入，不写在命令行里）。\n\n"
        "写出这条命令。",
        ["passwd zhangsan", "sudo passwd zhangsan"],
        sec=sec, diff=2,
        exp=(
            "`passwd zhangsan`（普通用户改自己用 `passwd`，"
            "root 改别人要指定用户名）。\n\n"
            "★ 为什么不在命令行里写密码：`passwd zhangsan mypass` 这种写法"
            "**根本不存在** —— `passwd` 只从 stdin 读。"
            "脚本里批量设密码要用 `chpasswd`（`echo 'user:pass' | chpasswd`）"
            "或 `passwd --stdin`（仅 RHEL 系）。\n\n"
            "★ 密码存在 `/etc/shadow`（root 可读、权限 `000` 或 `400`），"
            "`/etc/passwd` 里那个 `x` 只是个占位符 —— "
            "这是「shadow 套件」的核心设计：把密码哈希从人人可读的文件里挪走。\n\n"
            "★ **迁移**：`chage -l zhangsan` 看密码有效期；"
            "`passwd -l` 锁定账号、`passwd -u` 解锁；"
            "`passwd -e` 强制下次登录改密码。"),
        tags=["passwd", "密码", "shadow"]))

    out.append(C(
        "删除用户，连家目录一起删掉",
        "实习生走了，要把 `zhangsan` 彻底清掉：账号 + 家目录 + 邮件目录。\n\n"
        "写出这条命令。",
        ["userdel -r zhangsan", "userdel --remove zhangsan"],
        sec=sec, diff=2,
        exp=(
            "`userdel -r zhangsan`。\n\n"
            "★ 不加 `-r` 的后果：账号在 `/etc/passwd` 里没了，"
            "但 `/home/zhangsan` 原样留着，属主变成一串**数字 UID**"
            "（因为名字查不到了）。下次新建用户恰好分配到同一个 UID 时，"
            "**新用户直接继承旧用户的所有文件** —— 这是个真实存在的安全事故。\n\n"
            "★ `-r` 会删家目录与邮件池（`/var/mail/zhangsan`），"
            "但**不删**该用户在系统其它位置创建的文件（比如 `/srv` 下的）。"
            "彻底清理还得 `find / -uid <旧UID> -ls` 查一遍。\n\n"
            "★ 用户**正在登录**时 `userdel` 会失败，"
            "得先 `pkill -u zhangsan` 或等他退出。\n\n"
            "★ **迁移**：更温和的做法是先 `usermod -L`（锁定）观察一段时间，"
            "确认无影响再 `userdel -r`。"),
        tags=["userdel", "-r", "删除用户"]))

    out.append(C(
        "看自己属于哪些组",
        "写 Docker 命令报 `permission denied`，怀疑是自己不在 `docker` 组。\n\n"
        "要求：输出**当前用户**的 UID、GID 和所有组。",
        ["id", "id $(whoami)", "groups"],
        sec=sec, diff=1,
        exp=(
            "`id`。\n\n"
            "输出形如 `uid=1000(cosy) gid=1000(cosy) groups=1000(cosy),10(wheel),994(docker)`。\n\n"
            "★ 三个字段分别对应：\n"
            "- `uid` 用户 ID\n"
            "- `gid` **主组** ID（决定新建文件的默认属组）\n"
            "- `groups` 主组 + 所有**附加组**\n\n"
            "★ 为什么 `groups` 里明明有 `docker` 还是不能用："
            "**组成员关系在登录时被读进进程的凭证里**，"
            "改完组必须**重新登录**（或 `newgrp docker` 开个新 shell）才生效。"
            "`usermod` 完马上试，永远失败。\n\n"
            "★ **迁移**：`id zhangsan` 查别人；"
            "`id -nG` 只列组名；"
            "`id -u` 只给 UID（脚本里判断是不是 root 用 `[ $(id -u) -eq 0 ]`）。"),
        tags=["id", "组", "docker"]))

    out.append(C(
        "看当前谁登录着、在干什么",
        "要确认同事是不是还挂在服务器上（准备重启）。\n\n"
        "要求：显示登录用户 + 他们在跑的**命令**。",
        ["w"],
        sec=sec, diff=2,
        exp=(
            "`w`。\n\n"
            "`w` 的输出比 `who` 多两样最关键的东西：**每个用户当前在跑什么命令**"
            "（`WHAT` 列）和**系统负载**（第一行）。\n\n"
            "★ 各列含义：`USER` 用户、`TTY` 终端、`FROM` 来源 IP、"
            "`LOGIN@` 登录时间、`IDLE` 空闲时长、`JCPU`/`PCPU` CPU 占用、"
            "`WHAT` 当前命令。\n\n"
            "★ `JCPU` 是「该终端上所有进程累计占用」，"
            "`PCPU` 是「`WHAT` 那个进程占用」—— 两个别混。\n\n"
            "★ **迁移**：`who` 只列登录会话（不含命令）；"
            "`last` 看**历史**登录记录（从 `/var/log/wtmp` 读）；"
            "`lastb` 看失败的登录尝试（排查暴力破解）。"),
        tags=["w", "who", "登录"]))

    out.append(C(
        "以另一个用户的身份执行一条命令",
        "你是 root，要**以 `zhangsan` 的身份**跑 `whoami` 验证权限，"
        "而不是切过去再切回来。\n\n"
        "写出这条命令。",
        ["su - zhangsan -c whoami", "su zhangsan -c whoami",
         "sudo -u zhangsan whoami", "runuser -u zhangsan -- whoami"],
        sec=sec, diff=3,
        exp=(
            "`su - zhangsan -c whoami`（或 `sudo -u zhangsan whoami`）。\n\n"
            "★ **`su -` 与 `su` 的区别是本题的重点**：\n"
            "- `su - zhangsan`（带横杠）= **登录式**切换："
            "加载对方的完整环境（`$HOME`、`$PATH`、`$SHELL`、`.bash_profile`）\n"
            "- `su zhangsan` = **非登录式**：保持当前环境变量，只换 uid\n\n"
            "不带横杠时 `$HOME` 还是原来的，"
            "于是「以 zhangsan 身份」跑出来的东西可能读写的是**你的**家目录 —— "
            "排查权限问题时这会造成大量假象。\n\n"
            "★ `-c` 让命令跑完就退出，不用交互。\n\n"
            "★ **迁移**：`sudo -u user cmd` 不需要知道对方密码（靠 sudoers 授权），"
            "审计更清晰（有日志）；`su` 需要对方密码。"
            "生产环境里优先 `sudo -u`。"),
        tags=["su", "sudo", "-c", "切换用户"]))

    out.append(C(
        "建一个新组",
        "项目需要一个新的组 `devteam`，GID 指定为 3000。\n\n"
        "写出这条命令。",
        ["groupadd -g 3000 devteam", "groupadd --gid 3000 devteam"],
        sec=sec, diff=1,
        exp=(
            "`groupadd -g 3000 devteam`。\n\n"
            "★ `-g` 指定 **GID**（组 ID）；不指定则由系统按 `GID_MIN`~`GID_MAX` "
            "自动挑一个。\n\n"
            "★ 为什么有时要手动指定 GID：**跨机器保持一致**。"
            "NFS / 共享存储 / 容器挂载都靠数字 GID 认人，"
            "两台机器上同名组 GID 不同就会互相看不到对方文件的组权限。\n\n"
            "★ 同名组已存在会报 `group 'devteam' already exists`；"
            "`-f`（force）可以强制成功返回 0，写幂等脚本时有用。\n\n"
            "★ **迁移**：`groupmod -n newname oldname` 改组名（GID 不变，"
            "所以文件权限关系不受影响）；"
            "`groupdel` 删组（组里还有用户时会警告，但不会阻止）。"),
        tags=["groupadd", "-g", "GID"]))

    out.append(C(
        "看一个用户的 UID、主组和附加组（一次问全）",
        "要给 `zhangsan` 配权限，先得知道他到底属于哪些组。\n\n"
        "写出这条命令。",
        ["id zhangsan", "groups zhangsan"],
        sec=sec, diff=1,
        exp=(
            "`id zhangsan`。\n\n"
            "`groups` 只给组名列表，`id` 还给 **UID 和主组**，信息更全。\n\n"
            "★ 输出里 `gid=1000(zhangsan)` 是**主组**，"
            "后面 `groups=` 里的才是附加组。"
            "主组决定新建文件的属组（没有 SGID 的情况下）。\n\n"
            "★ 注意 `id` 输出的是**目标用户当前的数据库状态**，"
            "如果该用户有活跃会话，他的进程凭证里可能还是**旧**的组 —— "
            "这就是「`id` 说在 docker 组里，但命令还是权限不足」的原因。\n\n"
            "★ **迁移**：`id -u zhangsan` 拿 UID 用来 `find -uid`；"
            "`id -Gn zhangsan` 只看组名；"
            "`getent group devteam` 看某个组里有谁（比 `/etc/group` 可靠，"
            "因为能覆盖 LDAP/SSSD 等外部目录）。"),
        tags=["id", "groups", "getent"]))

    out.append(C(
        "查看系统里所有用户（含系统账号）",
        "要清点系统上的账号。\n\n"
        "要求：列表形式输出**所有**用户（包括 UID < 1000 的系统账号）。",
        ["cut -d: -f1 /etc/passwd", "awk -F: '{print $1}' /etc/passwd"],
        sec=sec, diff=2,
        exp=(
            "`cut -d: -f1 /etc/passwd`。\n\n"
            "`/etc/passwd` 第 1 列就是用户名，共 7 个字段：\n"
            "`用户名:密码占位:UID:GID:注释:家目录:登录shell`\n\n"
            "★ 为什么不用 `getent passwd`：两者**都能列出全部用户**，"
            "但 `getent` 还会包含 LDAP/SSSD/NIS 等外部目录的用户，"
            "`/etc/passwd` 只有本地账号。"
            "「清点本机账号」用前者，「清点所有能登录的身份」用 `getent`。\n\n"
            "★ 只想要**能登录**的用户：`awk -F: '$7 !~ /nologin|false/ {print $1}' /etc/passwd`。\n\n"
            "★ **迁移**：`awk -F: '$3 >= 1000 {print $1}' /etc/passwd` "
            "只列普通用户（Fedora 的 `UID_MIN` 是 1000）；"
            "`lastlog` 看每个账号最后一次登录时间，清账号前很有用。"),
        tags=["passwd", "cut", "账号清单"]))

    out.append(C(
        "让用户下次登录必须改密码",
        "新建的账号要给本人，密码是临时的，**必须强制他首次登录就改**。\n\n"
        "写出这条命令。",
        ["passwd -e zhangsan", "chage -d 0 zhangsan", "passwd --expire zhangsan"],
        sec=sec, diff=3,
        exp=(
            "`passwd -e zhangsan`（或 `chage -d 0 zhangsan`）。\n\n"
            "原理：把 `/etc/shadow` 里的「最后修改密码日期」置为 **0**，"
            "于是系统判定密码已过期，下次登录强制改。\n\n"
            "★ 三种等效写法：\n"
            "- `passwd -e user`（expire，最直白）\n"
            "- `chage -d 0 user`（把最后修改日设为 1970-01-01）\n"
            "- `chage -d $(date +%s | awk '{print int($1/86400)}')` 才是「今天」，别用\n\n"
            "★ **迁移**：`chage -l user` 看密码策略全貌；"
            "`chage -M 90 user` 设「90 天必须改」；"
            "`chage -W 7 user` 提前 7 天开始提醒。"
            "企业环境的密码策略基本都靠 `chage` 配。"),
        tags=["passwd", "-e", "chage", "密码过期"]))

    out.append(C(
        "临时让别人用一次 admin 权限（不用给 root 密码）",
        "要允许 `zhangsan` 执行 `/usr/bin/systemctl restart nginx`，"
        "但**不给完整 root**。\n\n"
        "要求：写出打开 sudoers 编辑器的命令（用 visudo 而不是直接 vim）。",
        ["visudo", "sudo visudo"],
        sec=sec, diff=3,
        exp=(
            "`visudo`。\n\n"
            "★ **为什么必须用 `visudo` 而不是 `vim /etc/sudoers`**："
            "`visudo` 会在保存时**做语法检查**。"
            "sudoers 语法错了会导致**所有人（含 root）都无法 sudo**，"
            "而普通用户没权限改回来 —— 只能进单用户模式修复。"
            "这是教科书级的「一条命令锁死系统」。\n\n"
            "★ 里面加一行实现本题：\n"
            "```\nzhangsan ALL=(root) NOPASSWD: /usr/bin/systemctl restart nginx\n```\n"
            "`NOPASSWD:` 表示免密码，`/usr/bin/` 必须写**绝对路径**（权限校验按路径精确匹配）。\n\n"
            "★ 更规范的做法是放到 `/etc/sudoers.d/` 下单独一个文件，"
            "不动主文件，便于审计与回滚。\n\n"
            "★ **迁移**：`sudo -l -U zhangsan` 列出某人能执行什么，"
            "排「为什么他 sudo 被拒」时第一步就看这个。"),
        tags=["visudo", "sudoers", "授权"]))

    out.append(C(
        "查某个用户最近登录过没有",
        "要清理长期不用的账号，先看 `zhangsan` **上次登录**是什么时候。\n\n"
        "写出这条命令。",
        ["lastlog -u zhangsan", "last zhangsan", "lastlog | grep zhangsan"],
        sec=sec, diff=3,
        exp=(
            "`lastlog -u zhangsan`。\n\n"
            "`lastlog` 从 `/var/log/lastlog` 读**每个账号最后一次登录**的记录，"
            "`-u` 只看指定用户。输出 `Never logged in` 表示从没登录过。\n\n"
            "★ `last zhangsan` 是**另一回事**：它列该用户的**登录历史**"
            "（从 `/var/log/wtmp` 读，含登录/登出时间、来源 IP、会话时长），"
            "能看到「最近 10 次都从哪登的」。"
            "「最后登录时间」用 `lastlog`，「登录历史」用 `last`。\n\n"
            "★ 两者都依赖日志文件存在与轮转策略 —— "
            "`/var/log/wtmp` 被清过的话 `last` 就空了，"
            "但 `lastlog` 仍然有（它是每用户一个记录，不是流水账）。\n\n"
            "★ **迁移**：`lastlog | grep Never` 一把捞出所有「从没登录过」的账号，"
            "这是清理僵尸账号的起手式。"),
        tags=["lastlog", "last", "审计"]))

    out.append(C(
        "看系统里有哪些组、各自的 GID",
        "要给新用户配组，先摸清现有的组。\n\n"
        "写出这条命令（本地组）。",
        ["cut -d: -f1,3 /etc/group", "awk -F: '{print $1, $3}' /etc/group",
         "getent group"],
        sec=sec, diff=2,
        exp=(
            "`cut -d: -f1,3 /etc/group`。\n\n"
            "`/etc/group` 每行 4 个字段：`组名:密码占位:GID:成员列表`。"
            "`-f1,3` 一次取两列。\n\n"
            "★ `getent group` 才是「系统真正认的组列表」—— "
            "如果配了 LDAP/SSSD，`/etc/group` 里**看不到**外部目录的组，"
            "但 `getent group` 能列出来。排查「组的名字明明存在却用不了」时，"
            "`getent` 是分水岭。\n\n"
            "★ 第 4 字段是**附加组**成员列表，**主组**成员不写在这里"
            "（主组信息在 `/etc/passwd` 第 4 字段）。"
            "所以 `grep devteam /etc/group` 看不到「主组是 devteam」的那些人，"
            "这是高频误会。\n\n"
            "★ **迁移**：`getent group devteam` 精确查一个组；"
            "`lid -g devteam`（libuser 包）能连主组成员一起列出。"),
        tags=["group", "getent", "GID"]))

    return out


# ===================================================================== #
#  八、命令特训 · 进程与作业
# ===================================================================== #
def part_proc() -> list[dict]:
    sec = "命令特训 · 进程与作业"
    out: list[dict] = []

    out.append(C(
        "看系统里所有进程（完整命令行）",
        "要排查一个服务起了几个实例，需要看**完整命令行**而不是被截断的名字。\n\n"
        "写出这条命令。",
        ["ps aux", "ps -ef", "ps -efl"],
        sec=sec, diff=1,
        exp=(
            "`ps aux`（BSD 风格）或 `ps -ef`（System V 风格）。\n\n"
            "★ **两种风格的选项写法不一样，混用会报错**：\n"
            "- BSD：`ps aux` —— 不带横杠，`a` 所有终端的进程、`u` 用户格式、"
            "`x` 含无终端的进程\n"
            "- SysV：`ps -ef` —— 带横杠，`-e` 所有进程、`-f` 完整格式\n"
            "写成 `ps auxf` 或 `ps -aux` 都能跑（Linux 的 ps 很宽容），"
            "但严格 POSIX 环境只认 `-ef`。\n\n"
            "★ `aux` 的 `x` 很关键：不加它**看不到后台守护进程**"
            "（它们没有控制终端），于是「服务明明在跑却 ps 不到」。\n\n"
            "★ 命令行太长会被截断到终端宽度；"
            "`ps -ef` 配 `-w -w`（`--width`）或 `ps auxww` 才显示全。\n\n"
            "★ **迁移**：`ps -eo pid,ppid,user,%cpu,%mem,cmd --sort=-%cpu | head` "
            "按 CPU 排序取前几名，比 `top` 更适合脚本化。"),
        tags=["ps", "aux", "-ef", "进程"]))

    out.append(C(
        "按名字找进程的 PID",
        "要重启 nginx，先拿到它的 PID。\n\n"
        "写出这条命令（按**进程名**精确匹配）。",
        ["pgrep nginx", "pidof nginx", "ps -C nginx -o pid="],
        sec=sec, diff=2,
        exp=(
            "`pgrep nginx`。\n\n"
            "★ `pgrep` 匹配的是**进程名**（`comm`，即去掉路径的可执行文件名），"
            "默认是**子串**匹配 —— `pgrep nginx` 会同时命中 `nginx` 和 `nginx-worker`。"
            "要精确匹配加 `-x`：`pgrep -x nginx`。\n\n"
            "★ 三种工具的差别：\n"
            "- `pgrep` 按名字匹配，支持 `-u`（按用户）、`-f`（匹配完整命令行）\n"
            "- `pidof` 精确匹配可执行文件名，**只输出 PID**，最干净\n"
            "- `ps -C` 按 `comm` 精确匹配，`-o pid=` 去掉表头只有数字\n\n"
            "★ `pgrep` **没有匹配时退出码是 1**（不是 0）—— "
            "脚本里 `set -e` 会因此中断，写 `pgrep nginx || true`。\n\n"
            "★ **迁移**：`pgrep -a nginx` 连命令行一起显示；"
            "`pgrep -f 'python.*worker'` 匹配完整命令（适合解释器类进程，"
            "因为它们的进程名都是 `python3`）。"),
        tags=["pgrep", "pidof", "PID"]))

    out.append(C(
        "结束一个进程（先礼后兵）",
        "某个 `python3` 进程卡住了，PID 是 4567。\n\n"
        "要求：先发**默认终止信号**（礼貌请求退出），不要一上来就强杀。",
        ["kill 4567", "kill -15 4567", "kill -TERM 4567"],
        sec=sec, diff=1,
        exp=(
            "`kill 4567`（等价于 `kill -15` / `-TERM`）。\n\n"
            "★ `kill` 这个名字**名不副实**：它其实是「**发信号**」，"
            "发什么信号由参数决定。默认是 `SIGTERM(15)`，"
            "意思是「请你退出」—— 进程可以捕获它做清理（关连接、刷缓冲、删临时文件）。\n\n"
            "★ 只有进程不响应 TERM 时才用 `kill -9`（`SIGKILL`）："
            "**KILL 无法被捕获**，进程被内核直接干掉，"
            "**没有任何清理机会** —— 数据库可能留半截事务，"
            "文件可能写坏，临时文件留着。\n\n"
            "★ 正确姿势是「**先 15，等几秒，再 9**」：\n"
            "```bash\nkill 4567; sleep 3; kill -0 4567 2>/dev/null && kill -9 4567\n```\n\n"
            "★ **迁移**：`kill -l` 列出所有信号；"
            "`kill -HUP 1234` 常被守护进程用来「重读配置」（不重启）。"),
        tags=["kill", "-15", "SIGTERM"]))

    out.append(C(
        "强制杀掉一个杀不掉的进程",
        "`kill 4567` 发了三次都没反应。\n\n"
        "写出这条命令。",
        ["kill -9 4567", "kill -KILL 4567", "kill -SIGKILL 4567"],
        sec=sec, diff=2,
        exp=(
            "`kill -9 4567`。\n\n"
            "`SIGKILL(9)` 由**内核**直接执行，进程**无法捕获、无法阻塞、无法忽略**，"
            "所以「杀不掉」的情况理论上不存在。\n\n"
            "★ 但有一种情况 `kill -9` 也没用：进程处于 **不可中断睡眠（D 状态）**，"
            "卡在磁盘 I/O 或 NFS 里。这时它连 KILL 都不响应 —— "
            "`ps` 里状态列显示 `D`。只能等 I/O 超时或重启。\n\n"
            "★ 如果进程是**僵尸（Z 状态）**，`kill -9` 也没用："
            "僵尸已经死了，只剩一个表项等父进程回收。"
            "解决办法是杀掉/重启**它的父进程**。\n\n"
            "★ **迁移**：`ps -o pid,stat,cmd -p 4567` 看状态；"
            "`ps -eo stat,pid,cmd | grep '^[DZ]'` 一把捞出 D/Z 状态的进程。"),
        tags=["kill", "-9", "SIGKILL"]))

    out.append(C(
        "按名字批量杀进程（不用一个个 PID）",
        "起了 20 个 `worker` 进程，要一次全干掉。\n\n"
        "写出这条命令。",
        ["pkill worker", "pkill -x worker", "killall worker"],
        sec=sec, diff=3,
        exp=(
            "`pkill worker`（或 `killall worker`）。\n\n"
            "★ **危险警告**：`pkill` 默认是**子串匹配进程名**，"
            "`pkill worker` 会连带杀掉 `worker-manager`、`my-worker` 之类。"
            "上线机器上按名字杀之前，先用 `pgrep -a worker` **看一眼清单**。\n\n"
            "★ 精确匹配用 `-x`：`pkill -x worker` 只杀名字**完全等于** `worker` 的。\n\n"
            "★ `killall` 的行为**因系统而异**：Linux 上是「按进程名杀」，"
            "但 Solaris 上 `killall` 是「**杀掉所有进程**」（等于关机）。"
            "跨平台脚本里千万别用 `killall`。\n\n"
            "★ **迁移**：`pkill -u zhangsan` 杀某用户所有进程（踢人下线）；"
            "`pkill -f 'python3 app.py'` 按完整命令行匹配（杀解释器类进程必须用 `-f`）；"
            "`pkill -9 -f pattern` 强杀。"),
        tags=["pkill", "killall", "批量"]))

    out.append(C(
        "让命令在退出终端后继续跑",
        "SSH 上去跑一个几小时的备份，**关掉终端不能中断它**。\n\n"
        "要求：用最经典的「忽略挂断信号」那条命令。",
        ["nohup ./backup.sh &", "nohup ./backup.sh > backup.log 2>&1 &"],
        sec=sec, diff=3,
        exp=(
            "`nohup ./backup.sh &`。\n\n"
            "两个部分各解决一个问题：\n"
            "- **`nohup`** 让进程**忽略 SIGHUP**（终端关闭时内核发的「挂断」信号）\n"
            "- **`&`** 把它放到**后台**，立刻把提示符还给你\n\n"
            "★ 只写 `&` 不写 `nohup`：终端一关，SIGHUP 就把进程带走了。"
            "只写 `nohup` 不写 `&`：进程在前台，你没法继续用这个终端。\n\n"
            "★ `nohup` 会把输出**追加到 `nohup.out`**（当前目录不可写时落到 `$HOME`）。"
            "所以实际写法通常是 `nohup cmd > out.log 2>&1 &` —— "
            "`2>&1` 把 stderr 也并进同一个文件，否则报错信息会丢。\n\n"
            "★ 更现代的替代是 `tmux`/`screen`（能回去看）或 `systemd-run --user`（能纳管）。\n\n"
            "★ **迁移**：`disown` 可以把**已经跑起来**的后台任务从作业表里摘掉，"
            "效果类似 nohup。"),
        tags=["nohup", "后台", "&", "SIGHUP"]))

    out.append(C(
        "看当前 shell 里有哪些后台作业",
        "你之前按 `Ctrl+Z` 挂起了几个任务，要看看它们还在不在。\n\n"
        "写出这条命令。",
        ["jobs", "jobs -l"],
        sec=sec, diff=2,
        exp=(
            "`jobs`（`-l` 带 PID）。\n\n"
            "★ **作业（job）与进程是两个概念**：作业是**当前 shell** 管的，"
            "换个终端窗口 `jobs` 就是空的 —— 它只列本 shell 的子进程。\n\n"
            "★ 作业号（`[1]`、`[2]`）与 PID 不是一回事。"
            "`fg %1`、`bg %2`、`kill %1` 用的是**作业号**，前面要带 `%`。\n\n"
            "★ `Ctrl+Z` 发的是 **SIGTSTP**（暂停），不是终止 —— "
            "进程还在内存里，只是不跑了。所以挂起一堆任务会一直占内存。\n\n"
            "★ **迁移**：`fg` 把最近一个作业拉回前台；"
            "`bg` 让挂起的作业在后台**继续跑**；"
            "如果终端关了，`jobs` 里的东西就随 shell 一起没了（除非用了 nohup/disown）。"),
        tags=["jobs", "后台作业", "Ctrl+Z"]))

    out.append(C(
        "把挂起的作业放到后台继续跑",
        "你按了 `Ctrl+Z` 暂停了一个编译任务（作业号 1），现在想让它**在后台跑完**。\n\n"
        "写出这条命令。",
        ["bg %1", "bg"],
        sec=sec, diff=2,
        exp=(
            "`bg %1`。\n\n"
            "★ 前提是作业**已被挂起**（`Ctrl+Z` 或 `kill -TSTP`）。"
            "对已在前台运行的作业直接 `bg` 是无效的。\n\n"
            "★ 关键：`bg` 之后进程**继续往终端写输出** —— "
            "如果它话很多，会一直刷屏干扰你。"
            "所以标准操作是「挂起 → bg → 输出重定向」的顺序已经晚了，"
            "更稳的做法是**一开始就 `cmd > log 2>&1 &`**。\n\n"
            "★ `bg %1` 与 `bg` 的区别：不带参数时对「当前作业」（最近挂起的那个）操作。\n\n"
            "★ **迁移**：`fg %1` 拉回前台；"
            "`jobs -l` 确认状态（`Stopped` 是挂起、`Running` 是后台运行）；"
            "要彻底脱离终端还是得 `nohup` 或 `disown`。"),
        tags=["bg", "fg", "作业控制"]))

    out.append(C(
        "以低优先级跑一个大编译（不抢占前台）",
        "你要编译一个大项目，但机器同时在跑线上服务，"
        "希望编译**尽量让出 CPU**。\n\n"
        "写出这条命令（nice 值设 10）。",
        ["nice -n 10 make", "nice -10 make", "nice --adjustment=10 make"],
        sec=sec, diff=3,
        exp=(
            "`nice -n 10 make`。\n\n"
            "**nice 值范围 -20（最高优先级）到 19（最低）**，默认 0。"
            "普通用户**只能调高**（让自己更「客气」），只有 root 能调到负值。\n\n"
            "★ `nice -10 make` 与 `nice -n 10 make` 都表示「+10」，"
            "但 `nice --10 make` 是 **-10（提高优先级）** —— "
            "少写一个 `n` 意思完全反过来，而且普通用户会报 `Permission denied`。"
            "所以**永远写 `-n`**，别用简写。\n\n"
            "★ nice 只影响**相对调度权重**，不是硬限速。"
            "机器空闲时低优先级的进程照样能跑满 CPU。\n\n"
            "★ **迁移**：进程已经在跑了怎么改？用 `renice`："
            "`renice -n 10 -p 1234`（按 PID）、`renice -n 10 -u zhangsan`（按用户）。\n\n"
            "★ 真要**限制资源**（CPU 百分比、内存上限）得用 `systemd-run` 或 cgroup，"
            "nice 做不到。"),
        tags=["nice", "-n", "优先级"]))

    out.append(C(
        "改一个正在运行的进程的优先级",
        "那个编译已经跑起来了（PID 1234），现在才想起来要降优先级。\n\n"
        "写出这条命令（nice 值改成 15）。",
        ["renice -n 15 -p 1234", "renice 15 -p 1234", "renice -n 15 1234"],
        sec=sec, diff=3,
        exp=(
            "`renice -n 15 -p 1234`。\n\n"
            "★ `renice` 与 `nice` 的分工：`nice` **启动时**设定，"
            "`renice` 改**已在运行**的进程。\n\n"
            "★ `-p` 后跟 PID（默认就是这个），`-u` 按**用户**（改组里所有进程），"
            "`-g` 按**进程组**。"
            "`renice -n 10 -u zhangsan` 是「把这个用户的所有进程都降级」，"
            "踢人限流时很好用。\n\n"
            "★ 权限规则同 `nice`：普通用户只能**降**优先级（数值变大），"
            "不能提；root 随便改。\n\n"
            "★ **迁移**：`ps -o pid,ni,cmd -p 1234` 看当前 nice 值（`NI` 列）；"
            "`top` 里按 `r` 键再输 PID 也能交互式 renice。"),
        tags=["renice", "nice", "优先级"]))

    out.append(C(
        "实时看 CPU / 内存占用排行",
        "线上机器变慢，要**实时**看哪个进程在吃 CPU。\n\n"
        "写出这条命令（交互式监控）。",
        ["top", "htop", "top -o %CPU"],
        sec=sec, diff=1,
        exp=(
            "`top`。\n\n"
            "`top` 的分区与关键列：\n"
            "- 顶部 `load average`：1/5/15 分钟的平均负载。"
            "**与核数一起看** —— 4 核机器 load 4.0 就是满载\n"
            "- `%Cpu(s)` 一行：`us` 用户态、`sy` 内核态、`wa` **I/O 等待**、"
            "`id` 空闲。**`wa` 高说明瓶颈在磁盘不在 CPU**\n"
            "- `MiB Mem`：`free`/`buff/cache`/`available`。"
            "★ 别只看 `free` 就说「内存不够」—— Linux 会主动用空闲内存做缓存，"
            "**该看 `available`**\n\n"
            "★ 常用交互键：`P` 按 CPU 排、`M` 按内存排、`k` 杀进程、"
            "`r` renice、`1` 展开每个核、`q` 退出。\n\n"
            "★ **迁移**：`top -b -n 1` 是**批处理模式**（输出一次就退出），"
            "最适合塞进脚本或日志；`htop` 更好看但要另装。"),
        tags=["top", "load", "CPU", "内存"]))

    out.append(C(
        "看一个进程打开的文件和网络连接",
        "某个进程占着文件删不掉，你要看它到底打开了什么。\n\n"
        "写出这条命令（指定 PID 1234）。",
        ["lsof -p 1234", "ls -l /proc/1234/fd"],
        sec=sec, diff=4,
        exp=(
            "`lsof -p 1234`。\n\n"
            "`lsof`（list open files）列出进程打开的所有文件描述符 —— "
            "既包括普通文件，也包括**网络套接字、管道、设备**"
            "（Linux 里「一切皆文件」）。\n\n"
            "★ 最经典的用途：**删了文件但磁盘没释放**。"
            "`lsof | grep deleted` 能找出「已被删但仍有进程持有句柄」的文件，"
            "空间要等进程关句柄（或重启）才真正释放。\n\n"
            "★ 另一条路 `ls -l /proc/1234/fd` 不用装任何工具："
            "`/proc/<pid>/fd/` 下每个符号链接就是一个打开的 fd，"
            "链接目标就是文件或 `socket:[inode]`。\n\n"
            "★ 只差「谁占着 80 端口」：`lsof -i :80` 或 `ss -ltnp | grep :80`。\n\n"
            "★ **迁移**：`lsof +D /path` 列出某目录下被打开的所有文件；"
            "`fuser -v /mnt` 看谁在用某个挂载点（卸载失败时必查）。"),
        tags=["lsof", "/proc", "文件描述符"]))

    out.append(C(
        "看进程树（谁是谁的父进程）",
        "要搞清楚 20 个 worker 是谁拉起来的。\n\n"
        "写出这条命令（树状显示）。",
        ["pstree -p", "ps -ejH", "ps axjf"],
        sec=sec, diff=3,
        exp=(
            "`pstree -p`。\n\n"
            "`pstree` 用缩进表达**父子关系**，`-p` 顺带标出每个进程的 PID。"
            "看「一个服务起了多少子进程」比 `ps` 直观得多。\n\n"
            "★ 重点看**父进程（PPID）**：如果 worker 的父进程是 `1`（systemd），"
            "说明它是被 systemd 直接拉起的（或者是孤儿被 init 收养）；"
            "如果是某个 `bash`，说明是人工启动的。\n\n"
            "★ `pstree -u` 标出**切换过用户的**进程（比如 root 启动后 setuid 成 nobody），"
            "排查权限问题时很有用。\n\n"
            "★ `ps -ejH` 是 POSIX 风格的树（不依赖 pstree 包）；"
            "`ps axjf` 带更多列。\n\n"
            "★ **迁移**：`pstree -p 1234` 只看某个进程的子树；"
            "`ps -o pid,ppid,cmd --ppid 1234` 列出某进程的所有直接子进程。"),
        tags=["pstree", "父子进程", "PPID"]))

    out.append(C(
        "查谁在监听某个端口",
        "部署时报 `Address already in use`，要知道**哪个进程占了 8080**。\n\n"
        "写出这条命令。",
        ["ss -ltnp | grep :8080", "ss -ltnp 'sport = :8080'",
         "lsof -i :8080", "netstat -ltnp | grep :8080"],
        sec=sec, diff=3,
        exp=(
            "`ss -ltnp | grep :8080`。\n\n"
            "`ss` 的选项拆解：\n"
            "- `-l` 只看**监听**状态的套接字\n"
            "- `-t` TCP（`-u` 是 UDP）\n"
            "- `-n` 用**数字**显示端口（不解析成服务名，且更快）\n"
            "- `-p` 显示**进程**（需要 root 才能看到别人的进程）\n\n"
            "★ `netstat` 已被 `ss` 取代（net-tools 包在新系统里默认不装），"
            "**记住 `ss` 就够了**。\n\n"
            "★ 「占了端口」不一定是 `LISTEN`：也可能是已建立的连接。"
            "那时 `-ltnp` 看不到，得去掉 `-l`。\n\n"
            "★ **迁移**：`ss -s` 看套接字统计汇总；"
            "`ss -tnp state established` 看所有已建立的 TCP 连接"
            "（排查「连接数暴涨」时必用）。"),
        tags=["ss", "-ltnp", "端口", "netstat"]))

    out.append(C(
        "查一个进程的启动时间与运行时长",
        "要确认服务是不是刚重启过。\n\n"
        "写出这条命令（指定 PID 1234）。",
        ["ps -o pid,lstart,etime,cmd -p 1234", "ps -p 1234 -o lstart,etime",
         "ps -o pid,etime,lstart -p 1234"],
        sec=sec, diff=4,
        exp=(
            "`ps -o pid,lstart,etime,cmd -p 1234`。\n\n"
            "- `lstart` 精确到秒的**启动时刻**（`Sat Oct 19 08:12:33 2026`）\n"
            "- `etime` **已运行时长**（`2-03:15:42` = 2 天 3 小时…）\n\n"
            "★ `etime` 的格式是 `[[DD-]hh:]mm:ss`，"
            "机器解析起来麻烦；要算精确秒数用 "
            "`ps -o etimes=`（GNU 扩展，直接给秒）。\n\n"
            "★ `-o` 后面跟列名，可以自定义任意组合，"
            "这是 `ps` 最强大的地方（`ps -eo pid,ppid,user,%cpu,%mem,stat,etime,cmd`）。\n\n"
            "★ **迁移**：`systemctl show nginx -p ActiveEnterTimestamp` "
            "看服务的启动时刻（比 ps 更适合 systemd 管理的服务）；"
            "`uptime -s` 看系统启动时间。"),
        tags=["ps", "lstart", "etime", "运行时长"]))

    out.append(C(
        "在后台跑命令，并把错误输出也一起收进日志",
        "要让 `deploy.sh` 后台跑，正常输出和错误输出**都**写进 `deploy.log`。\n\n"
        "写出这条命令。",
        ["nohup ./deploy.sh > deploy.log 2>&1 &",
         "./deploy.sh > deploy.log 2>&1 &"],
        sec=sec, diff=4,
        exp=(
            "`nohup ./deploy.sh > deploy.log 2>&1 &`。\n\n"
            "★ `2>&1` 是本题的核心，拆开看：\n"
            "- `2` 是 **stderr** 的文件描述符号，`1` 是 **stdout**\n"
            "- `>&` 是「把 fd 复制/重定向到另一个 fd」\n"
            "- 所以 `2>&1` = 「让 stderr 也写进 stdout 当前指向的地方」\n\n"
            "★ **顺序绝对不能反**：`> log 2>&1` 正确，`2>&1 > log` 错误。"
            "后者是「先把 stderr 指向**终端**，再把 stdout 指向文件」——"
            "结果错误信息仍然打在屏幕上，日志里只有正常输出。"
            "这是 shell 重定向最经典的一脚。\n\n"
            "★ `&` 与 `2>&1` 的先后：`&` 只是「放后台」，"
            "位置在整条命令最后，不影响重定向。\n\n"
            "★ **迁移**：想**丢弃**输出用 `> /dev/null 2>&1`；"
            "想分开存用 `> out.log 2> err.log`（注意这里写 `2>` 不是 `2>&`）。"),
        tags=["重定向", "2>&1", "后台", "日志"]))

    out.append(C(
        "监控一个进程什么时候退出（并在退出时报警）",
        "等一个编译任务跑完，但不想守着 —— "
        "要写「**等这个 PID 退出后**打印一句话」的一行命令。\n\n"
        "写出这条命令（PID 用 1234 举例）。",
        ["while kill -0 1234 2>/dev/null; do sleep 1; done; echo done",
         "tail --pid=1234 -f /dev/null"],
        sec=sec, diff=4,
        exp=(
            "`while kill -0 1234 2>/dev/null; do sleep 1; done; echo done`。\n\n"
            "★ `kill -0 PID` 是「**发 0 号信号**」—— 不真发信号，"
            "只做**存在性检查**：进程存在返回 0，不存在返回 1。"
            "这是 shell 里判断「进程还在不在」的标准做法。\n\n"
            "★ `2>/dev/null` 不能省：进程不存在时 `kill` 会往 stderr 喷 "
            "`No such process`，轮询几百次就刷屏了。\n\n"
            "★ 更省的写法：`tail --pid=1234 -f /dev/null` —— "
            "`tail` 会**阻塞**直到那个 PID 消失。"
            "纯 GNU 扩展，但一行顶一段循环，非常适合脚本。\n\n"
            "★ **迁移**：`wait 1234` 只能等**本 shell 的子进程**，"
            "对别人的进程无效 —— 这是很多人第一次踩的坑。"),
        tags=["kill -0", "轮询", "tail --pid"]))

    out.append(C(
        "看内存使用情况（要看真实可用内存）",
        "同事说「内存只剩 200M 了要挂了」，你要用**人类可读单位**看真实情况。\n\n"
        "写出这条命令。",
        ["free -h", "free --human"],
        sec=sec, diff=1,
        exp=(
            "`free -h`。\n\n"
            "★ 关键认知：**不要看 `free` 那一列**。"
            "Linux 会把空闲内存拿去做 `buff/cache`（页缓存），"
            "看起来「内存快用完了」，其实缓存随时可以被回收。\n\n"
            "★ **该看的是 `available` 列** —— 它是「在不触发 swap 的前提下"
            "还能给新进程用多少」，这才是真实余量。\n\n"
            "★ 各列含义：`total` 总量、`used` 已用、`free` 完全空闲、"
            "`shared` 共享内存、`buff/cache` 缓存、`available` 可用。\n\n"
            "★ `-h` 是人性化单位（`Gi`/`Mi`）；`-m` 固定按 MiB 显示（脚本里更好解析）。\n\n"
            "★ **迁移**：`free -s 2` 每 2 秒刷新一次；"
            "`vmstat 1` 看内存与 swap 活动的**变化趋势**，"
            "排查「内存泄漏」看的是趋势不是瞬时值。"),
        tags=["free", "-h", "内存", "available"]))

    return out


# ===================================================================== #
#  九、命令特训 · 磁盘与存储
# ===================================================================== #
def part_disk() -> list[dict]:
    sec = "命令特训 · 磁盘与存储"
    out: list[dict] = []

    out.append(C(
        "看各分区用了多少空间（人类可读）",
        "磁盘告警了，先确认是哪个分区满了。\n\n"
        "写出这条命令。",
        ["df -h", "df -hT", "df --human-readable"],
        sec=sec, diff=1,
        exp=(
            "`df -h`。\n\n"
            "`df`（disk free）按**挂载点**汇总，`-h` 人性化单位。\n\n"
            "★ `df -hT` 多一列**文件系统类型**（`xfs`/`ext4`/`btrfs`/`tmpfs`）—— "
            "排查时很有用：`tmpfs` 满说明是**内存**被吃了，不是硬盘。\n\n"
            "★ `Use%` 到 100% 不一定是唯一问题："
            "**`df -i` 看 inode 使用率** —— "
            "「磁盘还有空间但写不进文件」几乎都是 inode 用光"
            "（海量小文件，如邮件队列、session 文件）。\n\n"
            "★ 注意 `df` 显示的是**文件系统**层面，"
            "删了文件但进程还持有句柄时，`df` 不会立刻下降。\n\n"
            "★ **迁移**：`df -h /var` 只看某个路径所在的分区，"
            "比在整张表里找快。"),
        tags=["df", "-h", "磁盘"]))

    out.append(C(
        "看某个目录下每个子项占多少空间",
        "`/var` 快满了，要知道**是哪个子目录**吃的。\n\n"
        "要求：只统计**第一层**，按大小排序。",
        ["du -sh /var/* | sort -rh", "du -sh /var/* | sort -hr",
         "du -h --max-depth=1 /var | sort -rh"],
        sec=sec, diff=3,
        exp=(
            "`du -sh /var/* | sort -rh`。\n\n"
            "★ 三个组件：\n"
            "- `du -s`（summary）每个参数**只给总计**，不展开内部\n"
            "- `du -h` 人性化单位（注意：`-h` 与 `sort` 配合会有精度问题，见下）\n"
            "- `sort -rh` 按**人类可读单位**倒序（`-h` 让他认识 `1.2G`）\n\n"
            "★ `sort -h` 是 GNU 扩展，"
            "不认 `--human-readable` 的老系统上要换成 `sort -rn` + `du -k`（统一 KB）。\n\n"
            "★ **`du` 比 `df` 小是正常现象**："
            "`du` 只统计「看到的文件」，而 `df` 算的是「文件系统已用块」——"
            "被删但句柄未释放的文件、被挂载覆盖的目录，`du` 都看不到。\n\n"
            "★ **迁移**：`du -ah /var | sort -rh | head -20` "
            "直接找「最大的 20 个文件」，比逐层 `du -sh` 快得多；"
            "`du -sh /var/* 2>/dev/null` 加错误丢弃，避免权限报错刷屏。"),
        tags=["du", "-sh", "sort", "空间"]))

    out.append(C(
        "用一个命令看清所有块设备（含未挂载的）",
        "加了块新硬盘，要确认系统认到了没有、叫什么名字。\n\n"
        "写出这条命令。",
        ["lsblk", "lsblk -f", "lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT"],
        sec=sec, diff=2,
        exp=(
            "`lsblk`。\n\n"
            "`lsblk`（list block devices）用**树状结构**列出所有块设备，"
            "比 `fdisk -l` 清楚得多，而且**不需要 root**。\n\n"
            "★ `-f` 额外显示**文件系统**信息（FSTYPE、UUID、挂载点），"
            "挂载新盘前必看 —— 能直接拿到 `blkid` 里的 UUID。\n\n"
            "★ 关键列：`NAME` 设备名、`SIZE` 容量、`TYPE`（`disk`/`part`/`lvm`/`rom`）、"
            "`MOUNTPOINT`（空 = 没挂载）。\n\n"
            "★ `TYPE` 是 `disk` 但下面**没有 `part` 子项** → 这块盘还没分区；"
            "有 `part` 但 `MOUNTPOINT` 空 → 分了区没挂。两种情况处理完全不同。\n\n"
            "★ **迁移**：`lsblk -d -o name,size,rota` 只看整盘"
            "（`rota=1` 是机械盘、`0` 是 SSD）；"
            "`lsblk --json` 输出 JSON，适合脚本解析。"),
        tags=["lsblk", "块设备", "磁盘"]))

    out.append(C(
        "挂载一个新分区到指定目录",
        "`/dev/sdb1` 已经格式化好了（ext4），要挂到 `/data`。\n\n"
        "写出这条命令。",
        ["mount /dev/sdb1 /data", "mount -t ext4 /dev/sdb1 /data"],
        sec=sec, diff=2,
        exp=(
            "`mount /dev/sdb1 /data`。\n\n"
            "`mount 设备 挂载点` —— 顺序是「**谁**挂到**哪**」。"
            "写反了会报 `special device /data does not exist`。\n\n"
            "★ `-t ext4` 通常可省：`mount` 会**自动探测**文件系统类型。"
            "但探测失败时（比如没装 `ext4` 模块）显式写 `-t` 更快定位问题。\n\n"
            "★ 挂载点**必须已存在**，而且最好是**空目录**。"
            "非空目录挂上去之后，原来里面的文件会被**遮住**（不是删除，是不再可见）——"
            "卸载后又能看到。这个特性曾让不少人以为「数据丢了」。\n\n"
            "★ 临时挂载重启后失效，要持久化必须写 `/etc/fstab`。\n\n"
            "★ **迁移**：`mount -o remount,rw /` 把根分区改回可写（救援时必用）；"
            "`findmnt /data` 看某个挂载点的详细信息（比 `mount | grep` 干净）。"),
        tags=["mount", "挂载", "分区"]))

    out.append(C(
        "卸载一个分区",
        "要把 `/data` 卸下来换硬盘。\n\n"
        "写出这条命令。",
        ["umount /data", "umount /dev/sdb1"],
        sec=sec, diff=1,
        exp=(
            "`umount /data`（按**挂载点**）或 `umount /dev/sdb1`（按**设备**）。\n\n"
            "★ 命令名是 `umount`，**不是** `unmount` —— 少一个 `n`，"
            "这个拼写错误新手几乎都犯过。\n\n"
            "★ `target is busy` 是最常见的失败原因，含义是「有进程在用这个挂载点」。"
            "排查顺序：\n"
            "1. `lsof +D /data` 或 `fuser -vm /data` 找出是谁\n"
            "2. 自己的 shell 就在 `/data` 里 —— `cd` 出来\n"
            "3. 还有 NFS 客户端连着 / 有进程 cwd 在里面\n\n"
            "★ `umount -l`（lazy）会「先解除挂载、等没人用了再清理」，"
            "能强行成功但**可能造成数据不一致**，只在卡死时用。\n\n"
            "★ **迁移**：`umount -a` 卸载 `/etc/mtab` 里所有非根挂载点；"
            "卸载前 `sync` 一下，确保缓冲刷盘。"),
        tags=["umount", "卸载", "busy"]))

    out.append(C(
        "把新硬盘分区并格式化成 ext4",
        "`/dev/sdb` 是块空盘，要建一个分区并格式化成 ext4。\n\n"
        "要求：写出**格式化**那一步（假设分区 `/dev/sdb1` 已建好）。",
        ["mkfs.ext4 /dev/sdb1", "mkfs -t ext4 /dev/sdb1"],
        sec=sec, diff=3,
        exp=(
            "`mkfs.ext4 /dev/sdb1`（或 `mkfs -t ext4 /dev/sdb1`）。\n\n"
            "★ **这是破坏性操作**：`mkfs` 会**抹掉**目标设备上所有数据，"
            "没有确认提示。动手前务必 `lsblk` 确认设备名 —— "
            "把 `/dev/sda1`（系统盘）当 `/dev/sdb1` 敲下去，系统就没了。\n\n"
            "★ `mkfs.ext4` 是 `mkfs -t ext4` 的**简写软链**。"
            "文件系统具体参数（`-L` 卷标、`-b` 块大小、`-m` 保留百分比）"
            "用 `mkfs.ext4` 这种带类型的写法能直接传。\n\n"
            "★ 默认 ext4 会保留 **5%** 空间给 root 专用 —— "
            "大容量数据盘上这 5% 很浪费，可以 `mkfs.ext4 -m 1 /dev/sdb1`。\n\n"
            "★ **迁移**：`mkfs.xfs /dev/sdb1`（RHEL 系默认）、"
            "`mkfs.btrfs`；格式化前想看原有签名：`wipefs -n /dev/sdb1`（`-n` 是 dry-run）。"),
        tags=["mkfs", "ext4", "格式化"]))

    out.append(C(
        "查看分区的 UUID（写 fstab 要用）",
        "要在 `/etc/fstab` 里写一条挂载，必须用 **UUID** 而不是设备名。\n\n"
        "写出这条命令。",
        ["blkid /dev/sdb1", "blkid", "lsblk -f"],
        sec=sec, diff=3,
        exp=(
            "`blkid /dev/sdb1`。\n\n"
            "输出形如 `UUID=\"a1b2c3d4-...\" TYPE=\"ext4\"`。\n\n"
            "★ **`fstab` 为什么必须用 UUID**："
            "`/dev/sdb1` 这种名字是**内核枚举顺序**分配的，"
            "插拔硬盘、加装设备后可能变成 `/dev/sdc1`，"
            "结果就是**开机挂载失败甚至进不了系统**。"
            "UUID 写在文件系统里，跟设备名无关，永远指向同一个分区。\n\n"
            "★ 现代 systemd 还支持更可读的写法："
            "`LABEL=名字`、`PARTUUID=`（GPT 分区表里的 UUID，"
            "格式化后不变）、`/dev/disk/by-uuid/...`。\n\n"
            "★ `blkid` 需要 root 才能读全部信息；普通用户可用 `lsblk -f`（不需要 root）。\n\n"
            "★ **迁移**：`findmnt --verify` 检查 fstab 语法 —— "
            "改完 fstab **务必先验证再重启**，否则可能开不了机。"),
        tags=["blkid", "UUID", "fstab"]))

    out.append(C(
        "看系统整体负载与运行时长",
        "要迅速判断机器「忙不忙、开了多久」。\n\n"
        "写出这条命令。",
        ["uptime", "w"],
        sec=sec, diff=1,
        exp=(
            "`uptime`。\n\n"
            "输出形如 `08:12:33 up 3 days, 2:15, 2 users, load average: 0.52, 0.48, 0.41`。\n\n"
            "★ **load average 三个数** = 1 / 5 / 15 分钟的**平均活跃进程数**"
            "（运行中 + 不可中断睡眠）。\n\n"
            "★ 判断标准：**和 CPU 核数比**。"
            "4 核机器 load 4.0 ≈ 满载；load 8.0 = 严重超载（一堆进程在排队）。"
            "`nproc` 拿核数。\n\n"
            "★ 注意 load 包含 **D 状态（I/O 等待）**的进程 —— "
            "所以「load 很高但 CPU 空闲」说明瓶颈在**磁盘**。"
            "这时看 `top` 的 `wa` 列或 `iostat -x 1`。\n\n"
            "★ **迁移**：`uptime -p` 输出人类语言（`up 3 days, 2 hours`）；"
            "`uptime -s` 给出**系统启动时刻**（判断是不是刚重启过）。"),
        tags=["uptime", "load", "运行时长"]))

    out.append(C(
        "检查某个路径是不是一个独立挂载点",
        "`/data` 到底是一个独立分区，还是只是根分区上的一个普通目录？\n\n"
        "写出这条命令。",
        ["findmnt /data", "mountpoint /data", "df /data"],
        sec=sec, diff=3,
        exp=(
            "`findmnt /data`（最清楚）。\n\n"
            "★ 三种手段的差别：\n"
            "- `findmnt /data` 打印该挂载点的**全部信息**（源、类型、选项），"
            "是挂载就一定有输出\n"
            "- `mountpoint /data` 输出 `is a mountpoint` / `is not a mountpoint`，"
            "**退出码**可判断（脚本友好）\n"
            "- `df /data` 看它落在哪个文件系统上，"
            "**如果和 `/` 一样就说明没单独挂载**\n\n"
            "★ 为什么这件事重要："
            "在根分区上存数据，系统盘一满整个系统都会出问题；"
            "而独立分区满只影响那一个目录。"
            "部署前确认「数据目录是不是独立挂载」是好习惯。\n\n"
            "★ **迁移**：`findmnt -R /data` 递归列出该挂载点下的**所有子挂载**，"
            "排查「嵌套挂载把目录遮住了」时必用。"),
        tags=["findmnt", "mountpoint", "挂载点"]))

    out.append(C(
        "看磁盘 I/O 压力（哪个盘在忙）",
        "系统很卡但 CPU 不高，怀疑是磁盘 I/O 瓶颈。\n\n"
        "写出这条命令（每秒刷新，显示扩展统计）。",
        ["iostat -x 1", "iostat -xz 1", "iostat -dx 1"],
        sec=sec, diff=4,
        exp=(
            "`iostat -x 1`。\n\n"
            "★ 关键列：\n"
            "- `%util` —— 设备**忙碌时间占比**。接近 100% 说明磁盘是瓶颈\n"
            "- `await` —— 平均**等待时间**（ms）。机械盘 > 20ms、SSD > 5ms 就该警惕\n"
            "- `r/s`、`w/s` —— 每秒读写次数（IOPS）\n"
            "- `rkB/s`、`wkB/s` —— 每秒吞吐\n\n"
            "★ `%util` 在**多队列 NVMe** 上会失真（可能显示 100% 但性能还好），"
            "那种场景更该看 `await` 和队列深度。\n\n"
            "★ `-z` 隐藏「零活动」的设备，输出干净很多；"
            "`-d` 只显示设备（不含 CPU 统计）。\n\n"
            "★ `iostat` 来自 **sysstat** 包，最小化安装常常没有（`dnf install sysstat`）。\n\n"
            "★ **迁移**：`pidstat -d 1` 看**哪个进程**在狂读写；"
            "`iotop`（需另装）按进程实时排序，直观但吃 CPU。"),
        tags=["iostat", "%util", "IO", "sysstat"]))

    out.append(C(
        "找出被删除但仍占用空间的文件",
        "`df` 显示用了 90%，但 `du` 加起来只有 40%。这是「文件删了但句柄没释放」。\n\n"
        "写出这条命令（找出这些文件）。",
        ["lsof | grep deleted", "lsof +L1", "lsof -n | grep deleted"],
        sec=sec, diff=4,
        exp=(
            "`lsof | grep deleted`（或 `lsof +L1`）。\n\n"
            "★ 现象解释：文件被 `rm` 后**目录项没了**，"
            "但如果还有进程持有它的**文件描述符**，inode 就**不会被回收**，"
            "磁盘块也不会释放。"
            "于是 `du` 看不到（目录里没有这个名字了），`df` 却还算着。\n\n"
            "★ 解决办法二选一：\n"
            "1. 重启那个进程\n"
            "2. **不重启**的话，用 `> /proc/<pid>/fd/<n>` 把它截断（这招能救急）\n\n"
            "★ `lsof +L1` 是「link count 小于 1」的简写，"
            "正好就是「已无目录项但仍被打开」的文件，比 `grep deleted` 精确。\n\n"
            "★ **迁移**：根本对策是**日志用截断而不是删除**——"
            "`truncate -s 0 app.log` 或 `: > app.log`。"
            "这也是 `logrotate` 的 `copytruncate` 选项存在的原因。"),
        tags=["lsof", "deleted", "空间未释放"]))

    out.append(C(
        "看 inode 使用率（是否被小文件耗尽）",
        "磁盘明明还有 20G，但 `touch` 新文件报 `No space left on device`。\n\n"
        "写出这条命令。",
        ["df -i", "df -ih"],
        sec=sec, diff=3,
        exp=(
            "`df -i`。\n\n"
            "★ 每个文件（含目录、软链）都要占一个 **inode**。"
            "inode 总数在**格式化时定死**（ext4 默认约为每 16KB 一个）。"
            "inode 用完时，哪怕磁盘有空余也**创建不了任何新文件**，"
            "报错还是那句容易误导的 `No space left on device`。\n\n"
            "★ 典型场景：邮件队列堆积、session 文件、"
            "大量小日志（每个请求一个文件）、"
            "`node_modules` 这种海量小文件的目录。\n\n"
            "★ 排查：`df -i` 看 `IUse%`；"
            "找是哪个目录：`for d in /var/*; do echo \"$(find $d | wc -l) $d\"; done | sort -rn | head`\n\n"
            "★ **迁移**：inode 用完了只能删文件或重新格式化（`mkfs -N` 指定更多 inode）。"
            "所以「设计时预留足够 inode」比事后补救重要。"),
        tags=["df", "-i", "inode", "磁盘满"]))

    return out


# ===================================================================== #
#  十、命令特训 · 压缩与打包
# ===================================================================== #
def part_archive() -> list[dict]:
    sec = "命令特训 · 压缩与打包"
    out: list[dict] = []

    out.append(C(
        "把目录打成 tar 包（只打包，不压缩）",
        "要备份 `/etc/nginx`，打成 `nginx.tar`（不压缩，方便以后追加）。\n\n"
        "写出这条命令。",
        ["tar -cvf nginx.tar /etc/nginx", "tar cvf nginx.tar /etc/nginx",
         "tar --create --verbose --file nginx.tar /etc/nginx"],
        sec=sec, diff=2,
        exp=(
            "`tar -cvf nginx.tar /etc/nginx`。\n\n"
            "`c`/`v`/`f` 三件事：创建、啰嗦、指定文件名。\n\n"
            "★ **`-f` 必须紧跟文件名**，这也是 `-cfv` 这种顺序危险的原因："
            "`-f` 后面那个词一定会被当文件名，所以 `-cfv x.tar src` 里 "
            "`tar` 认为归档叫 `v`，`x.tar` 和 `src` 都成了要打包的路径 —— "
            "结果多出一个叫 `v` 的文件。**选项里 `f` 永远放最后**。\n\n"
            "★ 用**绝对路径**打包时 GNU tar 会**自动去掉开头的 `/`**，"
            "所以包里是 `etc/nginx/...`，解压时相对当前目录展开。"
            "这是「解压完多了一层 `etc/`」的原因（不是 bug）。\n\n"
            "★ **迁移**：不想多那一层，打包前 `cd /etc && tar -cvf nginx.tar nginx`；"
            "或者用 `-C`：`tar -cvf nginx.tar -C /etc nginx`。"),
        tags=["tar", "-cvf", "打包"]))

    out.append(C(
        "打包并用 bzip2 压缩",
        "要打 `src.tar.bz2`，压缩算法用 **bzip2**（压得更小但更慢）。\n\n"
        "写出这条命令。",
        ["tar -cjvf src.tar.bz2 src/", "tar cjvf src.tar.bz2 src/",
         "tar -cvjf src.tar.bz2 src/"],
        sec=sec, diff=2,
        exp=(
            "`tar -cjvf src.tar.bz2 src/`。\n\n"
            "★ **压缩算法的字母对照**（必背）：\n"
            "- `-z` → **gzip**（`.tar.gz`，最快最通用）\n"
            "- `-j` → **bzip2**（`.tar.bz2`，压缩比高，慢）\n"
            "- `-J` → **xz**（`.tar.xz`，压缩比最高，最慢）\n"
            "- `--zstd` → zstd（`.tar.zst`，快且比高，新系统首选）\n"
            "- **`-Z` 不是任何一种现代压缩** —— 它调 `compress`（老式 `.Z`）\n\n"
            "★ 大写 `J` 与小写 `j` 是两个不同算法，**大小写写错不会报错，"
            "但生成的是另一种格式**（后缀却还是你写的那个）—— 极难排查。\n\n"
            "★ **迁移**：不确定该用哪个，就 `-z`（gzip）；"
            "要给别人发又怕他解不开，也是 `-z`。"
            "zstd 是性能与压缩比的甜点，但老系统可能没装。"),
        tags=["tar", "-j", "bzip2", "压缩"]))

    out.append(C(
        "只看压缩包里有什么，不解压",
        "拿到一个 `backup.tar.gz`，解压前想知道里面到底是什么结构。\n\n"
        "写出这条命令。",
        ["tar -tzvf backup.tar.gz", "tar tzvf backup.tar.gz", "tar -tvf backup.tar.gz"],
        sec=sec, diff=2,
        exp=(
            "`tar -tzvf backup.tar.gz`。\n\n"
            "`t`（list）是「**列出内容但不解压**」—— "
            "这是 tar 里最该先养成习惯的一个动作：**解压前先看一眼**。\n\n"
            "★ 为什么必须看：包里可能是绝对路径或带 `../` 的路径，"
            "解压时会覆盖系统文件（`tar` 的 **tar-slip / zip-slip** 漏洞）。"
            "看一眼结构就能发现异常。\n\n"
            "★ `-v` 让 `t` 输出长格式（权限、属主、大小、时间），"
            "不加 `-v` 只给文件名。\n\n"
            "★ 压缩算法**不用指定**：GNU tar 会自己识别（靠文件头魔数），"
            "所以 `-tzvf` 里的 `z` 其实可以省。\n\n"
            "★ **迁移**：`tar -tzvf x.tar.gz | head -30` 只看前 30 项；"
            "`tar -tzvf x.tar.gz | wc -l` 数总条目。"),
        tags=["tar", "-t", "查看内容"]))

    out.append(C(
        "从 tar.gz 里只解出某一个文件",
        "`backup.tar.gz` 有几千个文件，你只要里面的 `etc/nginx/nginx.conf`。\n\n"
        "写出这条命令。",
        ["tar -xzvf backup.tar.gz etc/nginx/nginx.conf",
         "tar -xzvf backup.tar.gz etc/nginx/nginx.conf -C /tmp"],
        sec=sec, diff=3,
        exp=(
            "`tar -xzvf backup.tar.gz etc/nginx/nginx.conf`。\n\n"
            "★ 路径必须**和包内路径完全一致** —— "
            "包里是 `etc/nginx/nginx.conf`，"
            "你写 `/etc/nginx/nginx.conf`（带开头斜杠）就匹配不上。"
            "所以先用 `-t` 看清楚。\n\n"
            "★ 支持**通配**（GNU tar）：`tar -xzvf x.tar.gz --wildcards '*.conf'`。"
            "注意不加 `--wildcards` 时 `*` 不生效。\n\n"
            "★ 解出来会**按包内路径建目录**（`./etc/nginx/`），"
            "想解到指定位置加 `-C /tmp`。\n\n"
            "★ **迁移**：只解一个目录：`tar -xzvf x.tar.gz path/to/dir/`；"
            "要「解压但排除某些文件」用 `--exclude='*.log'`（注意"
            "**`--exclude` 必须放在文件名之前**）。"),
        tags=["tar", "-x", "部分解压"]))

    out.append(C(
        "压缩单个文件（不打包成 tar）",
        "要压一个 `access.log`，产出 `access.log.gz`。\n\n"
        "要求：用最通用的 gzip，**保留原文件**。",
        ["gzip -k access.log", "gzip -c access.log > access.log.gz"],
        sec=sec, diff=2,
        exp=(
            "`gzip -k access.log`（`-k` = keep，保留原文件）。\n\n"
            "★ **`gzip` 默认会删除原文件**！"
            "`gzip access.log` 之后只剩下 `access.log.gz`，原文件没了。"
            "这个行为让无数人第一次用时心里一凉。`-k` 就是为此存在的。\n\n"
            "★ `-c`（stdout）写法 `gzip -c f > f.gz` 也能保原文件，"
            "但多一步重定向，且**别写成 `gzip -c f > f`**（会把源文件截断）。\n\n"
            "★ 解压：`gzip -d f.gz` 或 `gunzip f.gz`。"
            "`zcat f.gz` 可以直接看内容不解压。\n\n"
            "★ **`gzip` 只能压单个文件**（压完就是 `f.gz`，不含文件名信息）——"
            "这就是为什么需要 tar：**tar 负责「打包成单文件」，gzip 负责「压这一个文件」**，"
            "两者分工明确。\n\n"
            "★ **迁移**：`gzip -9` 最高压缩（更慢）、`-1` 最快；"
            "`zless f.gz` 分页看；`zgrep pattern f.gz` 直接搜压缩包。"),
        tags=["gzip", "-k", "压缩", "gunzip"]))

    out.append(C(
        "解压一个 .gz 文件",
        "手上有 `app.log.gz`，要还原成 `app.log`。\n\n"
        "写出这条命令。",
        ["gunzip app.log.gz", "gzip -d app.log.gz", "gzip -dk app.log.gz"],
        sec=sec, diff=1,
        exp=(
            "`gunzip app.log.gz`（等价 `gzip -d`）。\n\n"
            "★ 解压后**压缩包会被删除**（与 `gzip` 压缩时删原文件对称）。"
            "要保留压缩包用 `-k`。\n\n"
            "★ `gunzip` 自动识别 `.gz`/`.Z`/`.tgz`，"
            "解 `.tgz` 得到 `.tar`（**不会**自动展开 tar）—— "
            "要「一次解到底」用 `tar -xzf f.tgz`。\n\n"
            "★ **迁移**：`zcat f.gz | less` 只看不落地；"
            "`tar -xzf` 才是平时最常用的「压缩包解开」——"
            "`gunzip` 只在「这就是个单文件」时用。"),
        tags=["gunzip", "解压", "gz"]))

    out.append(C(
        "把一个目录做成 zip（要给 Windows 用户）",
        "要把 `report/` 目录打成 `report.zip`，对方是 Windows，"
        "希望解压后直接得到 `report/` 目录。\n\n"
        "写出这条命令。",
        ["zip -r report.zip report/", "zip -r report.zip report"],
        sec=sec, diff=3,
        exp=(
            "`zip -r report.zip report/`。\n\n"
            "★ `-r` 是**必须的**：不加就只压目录里的**空壳**"
            "（zip 会报 `name not matched` 或者只存个目录项）。\n\n"
            "★ 为什么用 zip 而不用 tar.gz：**Windows 原生支持 zip**，"
            "而 `.tar.gz` 得装 7-Zip / WinRAR。跨平台交付一律 zip。\n\n"
            "★ **中文文件名**：Linux 上 zip 默认用 UTF-8 存名字，"
            "老版 Windows 解压可能乱码。需要兼容就用 "
            "`zip -r -UN=UTF8`，或者干脆改用 `7z`。\n\n"
            "★ `-r` 会**保留相对路径**：`zip -r a.zip report/` 里是 `report/xxx`；"
            "想「解压后不要那层 report」，得 `cd report && zip -r ../a.zip .`。\n\n"
            "★ **迁移**：`unzip -l a.zip` 看内容；"
            "`unzip -d /tmp a.zip` 解到指定目录；"
            "`unzip -O GBK` 处理 Windows 传来的乱码包。"),
        tags=["zip", "-r", "跨平台"]))

    out.append(C(
        "解压 zip 到指定目录",
        "要把 `assets.zip` 解到 `/var/www/html/static`，"
        "**别散在当前位置**。\n\n"
        "写出这条命令。",
        ["unzip assets.zip -d /var/www/html/static",
         "unzip -d /var/www/html/static assets.zip"],
        sec=sec, diff=2,
        exp=(
            "`unzip assets.zip -d /var/www/html/static`。\n\n"
            "★ `-d`（directory）指定解压目标。与 `tar -C` 不同的是，"
            "**`-d` 放在前面或后面都行**（`unzip` 的参数解析比较宽松），"
            "但习惯上写在 zip 文件名之后。\n\n"
            "★ 目标目录**不存在时 `unzip` 会自动创建**（`tar -C` 不会）。"
            "这个差别在脚本里要留意。\n\n"
            "★ 解压时如果文件已存在，`unzip` 会**交互式询问**"
            "（`replace ...? [y]es, [n]o, [A]ll`）—— "
            "脚本里必须加 `-o`（覆盖）或 `-n`（不覆盖），"
            "否则会**卡死在等输入**上。\n\n"
            "★ **迁移**：`unzip -l a.zip` 先看清单；"
            "`unzip -q` 安静模式（不刷文件名），CI 日志里很清爽。"),
        tags=["unzip", "-d", "解压"]))

    out.append(C(
        "看一个压缩包是什么格式（后缀不可信）",
        "拿到一个叫 `data.bin` 的文件，别人说它是压缩包，但不知道是哪种。\n\n"
        "写出这条命令。",
        ["file data.bin", "file data.bin && tar -tf data.bin"],
        sec=sec, diff=3,
        exp=(
            "`file data.bin`。\n\n"
            "★ 后缀是**人看的**，`file` 看的是**文件头魔数**，"
            "所以能识别出「后缀写错了」的情况（`.tar.gz` 其实是 `.tar.bz2`）。\n\n"
            "★ 输出会明确写出算法："
            "`gzip compressed data`、`bzip2 compressed data`、"
            "`XZ compressed data`、`Zstandard compressed data`、"
            "`Zip archive data`、`POSIX tar archive`。\n\n"
            "★ `tar` 本身**不需要知道压缩算法**："
            "GNU tar 会自己探测，所以 `tar -xf data.bin` 通常能直接解开"
            "（`-x` 后面**不写** `z`/`j`/`J`）。\n\n"
            "★ **迁移**：`tar -xf`（不带压缩字母）是兼容性最好的写法，"
            "尤其在「别人给的包，不确定算法」的场景。"
            "反过来，自己打包时明确写算法更可读。"),
        tags=["file", "魔数", "压缩格式"]))

    out.append(C(
        "把压缩包追加上一个新文件（不重新打包）",
        "已经打好的 `app.tar` 里少了一个文件，要**追加**进去，"
        "不要重新打一遍（里面有几十 G）。\n\n"
        "写出这条命令。",
        ["tar -rvf app.tar newfile.conf", "tar rf app.tar newfile.conf",
         "tar --append --file=app.tar newfile.conf"],
        sec=sec, diff=4,
        exp=(
            "`tar -rvf app.tar newfile.conf`。\n\n"
            "`-r`（`--append`）在归档**末尾追加**条目，"
            "不重写前面的内容 —— 所以对超大包也很快。\n\n"
            "★ **前提：包不能是压缩过的**。`.tar.gz` 是**一条压缩流**，"
            "不可能在一个 gzip 流中间插入数据，"
            "所以 `-r` 对压缩包会直接报错。"
            "这是「为什么我特意打成 .tar 不压缩」的原因之一。\n\n"
            "★ 追加的条目会**覆盖同名的旧条目吗**？不会 —— "
            "tar 里会出现**两个同名条目**，解压时**后一个覆盖前一个**。"
            "所以「更新」场景下追加是可行的（解压结果是对的）。\n\n"
            "★ **迁移**：`-u`（`--update`）是「只追加比包里更新的文件」，"
            "做增量备份更合适；`-A`（`--concatenate`）能把两个 tar 包拼起来。"),
        tags=["tar", "-r", "追加"]))

    out.append(C(
        "把 tar 包压缩成最小体积（讲究压缩比）",
        "要把一个 2G 的归档发给别人，带宽有限，要**尽可能小**。\n\n"
        "要求：用压缩比最高的算法。",
        ["xz -9 app.tar", "tar -cJvf app.tar.xz app/", "xz -9e app.tar"],
        sec=sec, diff=4,
        exp=(
            "`xz -9 app.tar`（产出 `app.tar.xz`）。\n\n"
            "★ **压缩比排序（大致）**："
            "xz > bzip2 > zstd(高等级) > gzip。"
            "**速度排序反过来**。`-9` 是最高压缩等级。\n\n"
            "★ xz 的代价：**解压也要 CPU**，而且内存占用高。"
            "在低配机器上解一个 10G 的 xz 包可能要几分钟 —— "
            "所以服务器上更常用 zstd。\n\n"
            "★ `-9e` 里的 `e` 是「极致模式」（更多 CPU 换更小体积），"
            "只建议压缩时用一次、解压端不需要。\n\n"
            "★ xz **默认删除原文件**（和 gzip 一样），要保留加 `-k`。\n\n"
            "★ **迁移**：`tar -cJvf` 一步打包+压缩；"
            "`xz -l app.tar.xz` 看压缩率；"
            "要「压得快又能解」选 `zstd -19`（比 xz 快一个数量级）。"),
        tags=["xz", "-9", "压缩比"]))

    out.append(C(
        "解压时跳过出错的文件继续解",
        "一个大 zip 里有个文件损坏了，`unzip` 到一半就退出。"
        "你要**跳过坏文件把所有能解的解开**。\n\n"
        "写出这条命令。",
        ["unzip -o assets.zip -x broken.txt", "unzip -n assets.zip"],
        sec=sec, diff=4,
        exp=(
            "`unzip -o assets.zip`（`-o` 覆盖不提问，遇错继续），"
            "或 `unzip -x` 显式排除坏文件。\n\n"
            "★ `unzip` 的几种「不提问」选项要分清：\n"
            "- `-o` 覆盖已有文件，**不问**\n"
            "- `-n` 不覆盖已有文件（已存在的跳过）\n"
            "- `-q` 安静模式（只影响输出，不影响提问）\n\n"
            "★ 遇到**损坏条目**时 `unzip` 会报 `bad CRC` 并返回非 0 退出码，"
            "但前面已经解出的文件**是好的**。"
            "所以脚本里可以 `unzip ... || true`，"
            "再检查关键文件在不在。\n\n"
            "★ **迁移**：`unzip -t a.zip` 先**测试完整性**（只校验不解压），"
            "知道有几个坏条目再决定策略；"
            "`-x` 后面跟通配符可以排除一整类文件：`unzip a.zip -x '*.log'`。"),
        tags=["unzip", "-o", "损坏", "容错"]))

    return out


# ===================================================================== #
#  十一、命令特训 · 网络与远程
# ===================================================================== #
def part_net() -> list[dict]:
    sec = "命令特训 · 网络与远程"
    out: list[dict] = []

    out.append(C(
        "看本机的 IP 地址",
        "要知道这台机器的 IP（给别人连过来用）。\n\n"
        "要求：用现代工具（不要 `ifconfig`）。",
        ["ip addr", "ip a", "ip addr show", "ip -brief addr"],
        sec=sec, diff=1,
        exp=(
            "`ip addr`（可简写 `ip a`）。\n\n"
            "★ `ifconfig` **已经被淘汰**：net-tools 包在新版 Fedora "
            "默认不装，`netstat`/`route`/`ifconfig` 都不在。"
            "教材上那些命令能「想起来」就行，实操一律用 `ip`。\n\n"
            "★ 一个网卡可能有多行 `inet`：**一个 IPv4、一个 IPv6**。"
            "回给别人时别贴错了。\n\n"
            "★ `-brief`（`-br`）输出极简表格，"
            "`ip -br a` 是目前最快的「我 IP 是多少」。\n\n"
            "★ **迁移**：`ip -4 addr show dev eth0` 只看某网卡的 IPv4；"
            "`hostname -I` 一行输出所有 IPv4（**注意大写 I**，"
            "小写 `-i` 是解析主机名的 IP，结果可能不同）。"),
        tags=["ip", "addr", "IP", "ifconfig"]))

    out.append(C(
        "看路由表（默认网关是谁）",
        "机器上不了外网，要先确认默认网关对不对。\n\n"
        "写出这条命令。",
        ["ip route", "ip r", "ip route show"],
        sec=sec, diff=2,
        exp=(
            "`ip route`（简写 `ip r`）。\n\n"
            "★ 找 `default via <网关IP> dev <网卡>` 那一行 —— "
            "它就是默认路由。没有这一行 = **没有默认网关**，"
            "内网能通、外网不通，症状是「能 ping 通 192.168.x.x 但 ping 不通 8.8.8.8」。\n\n"
            "★ 各列含义：`default` 目标、`via` 下一跳、`dev` 出接口、"
            "`proto` 来源（`dhcp`/`static`/`kernel`）、`metric` 优先级（**小的优先**）。\n\n"
            "★ 也有 `169.254.x.x` 这种地址时要注意：那是 **link-local 自配地址**，"
            "说明 DHCP 拿不到地址，网络其实是有问题的。\n\n"
            "★ **迁移**：`ip route get 8.8.8.8` 直接问「去这个地址会走哪条路」，"
            "排查策略路由时最准；`ip -6 route` 看 IPv6 路由。"),
        tags=["ip", "route", "网关"]))

    out.append(C(
        "测试到某台主机的连通性（只 ping 4 次）",
        "`ping` 默认会一直跑，脚本里要**发 4 个包就停**。\n\n"
        "写出这条命令。",
        ["ping -c 4 8.8.8.8", "ping -c4 8.8.8.8", "ping -c 4 www.example.com"],
        sec=sec, diff=1,
        exp=(
            "`ping -c 4 8.8.8.8`。\n\n"
            "`-c`（count）指定发包数，不写就**永远跑下去**（`Ctrl+C` 停）。\n\n"
            "★ **`ping` 通不代表服务通**：ping 只测 ICMP，"
            "而防火墙常常只放行特定 TCP 端口。"
            "判断「服务是否可用」必须测端口（`curl` 或 `ss`）。\n\n"
            "★ **`ping` 不通也不代表主机不通**："
            "很多云主机默认**屏蔽 ICMP**。所以 ping 失败时下一步是测端口，"
            "而不是直接判定「机器挂了」。\n\n"
            "★ 看 `packet loss` 与 `time`：丢包率与延迟才是价值所在，"
            "「通了」这个结论本身信息量很小。\n\n"
            "★ **迁移**：`ping -c 4 -i 0.2 host` 加快间隔；"
            "`ping -s 1400 host` 测 MTU 分片问题。"),
        tags=["ping", "-c", "连通性"]))

    out.append(C(
        "测某个端口通不通（不是 ping 主机）",
        "对方说服务启动了，但你要确认 **TCP 8080 端口**真的能连上。\n\n"
        "写出这条命令。",
        ["curl -v telnet://10.0.0.5:8080",
         "nc -zv 10.0.0.5 8080",
         "ss -tn 10.0.0.5:8080",
         "timeout 3 bash -c '</dev/tcp/10.0.0.5/8080'"],
        sec=sec, diff=3,
        exp=(
            "`nc -zv 10.0.0.5 8080`。\n\n"
            "- `-z` 只扫描**不发数据**（zero-I/O）\n"
            "- `-v` 显示结果\n\n"
            "★ 输出 `succeeded` / `Connection refused` 直接给结论。"
            "`Connection refused` = 端口**没有监听**；"
            "`timed out` = 中间被**防火墙拦了**。两者含义完全不同。\n\n"
            "★ `nc` 来自 nmap-ncat 包，可能没装。"
            "**不需要装任何东西的写法**是 bash 的 `/dev/tcp` 伪设备：\n"
            "```bash\n"
            "timeout 3 bash -c '</dev/tcp/10.0.0.5/8080' && echo open\n"
            "```\n\n"
            "★ **迁移**：`curl -v telnet://ip:port` 也是通用写法"
            "（curl 几乎处处都有）；"
            "`telnet` 命令在 Fedora 上默认不装，别依赖它。"),
        tags=["nc", "端口", "/dev/tcp", "连通性"]))

    out.append(C(
        "用 curl 只看 HTTP 响应头",
        "要确认一个网址返回的状态码和 Content-Type，"
        "但**不想下载整个响应体**。\n\n"
        "写出这条命令。",
        ["curl -I https://example.com", "curl --head https://example.com",
         "curl -s -o /dev/null -w '%{http_code}' https://example.com"],
        sec=sec, diff=2,
        exp=(
            "`curl -I https://example.com`。\n\n"
            "`-I`（`--head`）发 **HEAD 请求**，只拿响应头。"
            "注意：有些服务器不支持 HEAD（返回 405），"
            "那就得用 `-D -` 配合 `GET`。\n\n"
            "★ 状态码速查：`200` 正常、`301/302` 跳转、"
            "`403` 无权限、`404` 不存在、`500` 服务端错、"
            "`502` 网关后面的服务挂了、`504` 网关超时。\n\n"
            "★ 只想要状态码数字（写监控脚本）："
            "`curl -s -o /dev/null -w '%{http_code}' URL` —— "
            "`-s` 静默、`-o /dev/null` 丢弃正文、`-w` 打印指定变量。"
            "这是最好用的一条。\n\n"
            "★ **迁移**：`curl -L` 跟随跳转（否则 301 就停了）；"
            "`curl -k` 忽略证书错误（自签证书测试时用，生产别用）；"
            "`curl -m 5` 设超时，避免脚本卡死。"),
        tags=["curl", "-I", "HTTP", "状态码"]))

    out.append(C(
        "下载一个文件并保存成指定名字",
        "要下载 `https://example.com/data.tar.gz` 并**直接存成 `data.tgz`**。\n\n"
        "写出这条命令。",
        ["wget -O data.tgz https://example.com/data.tar.gz",
         "curl -o data.tgz https://example.com/data.tar.gz",
         "curl -L -o data.tgz https://example.com/data.tar.gz"],
        sec=sec, diff=2,
        exp=(
            "`wget -O data.tgz https://example.com/data.tar.gz`。\n\n"
            "★ **`wget` 的 `-O` 是大写**，指定**输出文件名**；"
            "小写 `-o` 是「把**日志**写到哪个文件」。"
            "大小写搞反会出现「下载的文件变成了一堆日志」的经典事故。\n\n"
            "★ **`curl` 的 `-o` 是小写**（`--output`）指定输出文件名，"
            "`-O` 大写是「用 URL 里的文件名」。"
            "curl 与 wget 的大小写含义**正好相反** —— 这是最容易记混的一对。\n\n"
            "★ `curl` 必须加 `-L` 才跟随 301/302 跳转，"
            "`wget` **默认就跟随**。\n\n"
            "★ **迁移**：`wget -c` 断点续传；"
            "`wget -q --show-progress` 有进度条但不刷屏；"
            "`curl -C -` 是 curl 的断点续传。"),
        tags=["wget", "curl", "-O", "下载"]))

    out.append(C(
        "远程登录一台服务器（指定用户名和端口）",
        "要登录 `10.0.0.5`，用户名 `deploy`，SSH 端口是 **2222**（不是 22）。\n\n"
        "写出这条命令。",
        ["ssh -p 2222 deploy@10.0.0.5", "ssh -p2222 deploy@10.0.0.5"],
        sec=sec, diff=2,
        exp=(
            "`ssh -p 2222 deploy@10.0.0.5`。\n\n"
            "★ **`ssh` 的端口选项是小写 `-p`**，而 `scp` 和 `sftp` 是**大写 `-P`**。"
            "这个不对称是 SSH 工具链里最著名的一处不一致 —— "
            "`scp -p` 的含义是「保留时间戳」，完全另一件事。\n\n"
            "★ 用户名的两种写法：`ssh deploy@host` 或 `ssh -l deploy host`。"
            "长期用建议写 `~/.ssh/config`：\n"
            "```\nHost prod\n    HostName 10.0.0.5\n    User deploy\n    Port 2222\n```\n"
            "之后 `ssh prod` 一条搞定。\n\n"
            "★ **迁移**：`ssh -v` 打印握手细节（排查认证失败必用）；"
            "`ssh-keygen -R host` 清掉变了的主机指纹（重装系统后必踩）。"),
        tags=["ssh", "-p", "远程登录"]))

    out.append(C(
        "免密登录：把自己的公钥传到对方机器",
        "每次 ssh 都要输密码太麻烦，要把本机公钥装到 `deploy@10.0.0.5`。\n\n"
        "写出这条命令。",
        ["ssh-copy-id deploy@10.0.0.5", "ssh-copy-id -p 2222 deploy@10.0.0.5"],
        sec=sec, diff=3,
        exp=(
            "`ssh-copy-id deploy@10.0.0.5`。\n\n"
            "它做的事：把 `~/.ssh/id_*.pub` 追加到对方 "
            "`~/.ssh/authorized_keys`，并**顺手设好目录权限**（`700` / `600`）。\n\n"
            "★ **权限是免密登录失败的第一原因**："
            "`~/.ssh` 必须是 `700`、`authorized_keys` 必须是 `600`、"
            "家目录**不能对 group/other 可写**。"
            "sshd 会**静默忽略**权限过松的密钥文件 —— "
            "日志里只有一句 `Authentication refused: bad ownership`，"
            "不仔细看会以为密钥没传对。\n\n"
            "★ 没装 `ssh-copy-id` 时的等价手工操作：\n"
            "`cat ~/.ssh/id_ed25519.pub | ssh user@host 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys'`\n\n"
            "★ **迁移**：`ssh-keygen -t ed25519 -C 'me@laptop'` 生成密钥；"
            "`-p 2222` 指定端口（注意这里也是小写 `-p`，和 `ssh` 一致）。"),
        tags=["ssh-copy-id", "免密", "公钥"]))

    out.append(C(
        "把本地文件传到远程服务器",
        "要把 `deploy.sh` 传到 `10.0.0.5` 的 `/home/deploy/` 下，端口 2222。\n\n"
        "写出这条命令。",
        ["scp -P 2222 deploy.sh deploy@10.0.0.5:/home/deploy/",
         "scp -P2222 deploy.sh deploy@10.0.0.5:/home/deploy/",
         "rsync -av -e 'ssh -p 2222' deploy.sh deploy@10.0.0.5:/home/deploy/"],
        sec=sec, diff=3,
        exp=(
            "`scp -P 2222 deploy.sh deploy@10.0.0.5:/home/deploy/`。\n\n"
            "★ **`scp` 的端口是**大写 **`-P`**（与 `ssh -p` 相反，见上题）。\n\n"
            "★ 路径末尾的 `/` 有讲究：目标写 `/home/deploy/`（带斜杠）"
            "表示「放进这个目录」；写 `/home/deploy` 而它是个目录时结果一样；"
            "但如果目标是**文件名**，就变成改名复制。\n\n"
            "★ **`scp` 已不推荐用于大批量传输**："
            "它基于老式协议，大文件速度上不去、不支持断点续传、"
            "不能增量。**`rsync -av` 是现代替代**（走 SSH，只传差异）。\n\n"
            "★ **迁移**：`scp -r dir/ user@host:/path` 传目录；"
            "`rsync -avz --progress src/ user@host:/dst/` "
            "（**注意 `src/` 带斜杠 = 传内容，不带 = 传目录本身**，"
            "这个斜杠是 rsync 的头号坑）。"),
        tags=["scp", "-P", "传输", "rsync"]))

    out.append(C(
        "同步本地目录到远程（只传改过的）",
        "要把 `./site` 同步到服务器的 `/var/www`，"
        "**只传有变化的文件**，并显示进度。\n\n"
        "写出这条命令。",
        ["rsync -avz --progress site/ deploy@10.0.0.5:/var/www/",
         "rsync -av --progress site/ deploy@10.0.0.5:/var/www/",
         "rsync -avz site/ deploy@10.0.0.5:/var/www/"],
        sec=sec, diff=4,
        exp=(
            "`rsync -avz --progress site/ deploy@10.0.0.5:/var/www/`。\n\n"
            "选项拆解：\n"
            "- `-a`（archive）= `-rlptgoD`，保权限/时间/软链/属主，最常用\n"
            "- `-v` 详细输出、`-z` 传输时压缩（跨网络才划算）\n"
            "- `--progress` 显示每个文件的进度\n\n"
            "★ **`site/` 与 `site` 的区别是 rsync 的头号坑**：\n"
            "- `rsync -a site/ host:/var/www/` → 得到 `/var/www/xxx`（**传内容**）\n"
            "- `rsync -a site host:/var/www/` → 得到 `/var/www/site/xxx`（**传目录本身**）\n"
            "记法：**源路径带斜杠 = 只要里面的东西**。\n\n"
            "★ 默认**不删除**目标里多出来的文件，"
            "要镜像同步必须加 `--delete`（危险，先 `-n` dry-run 看一遍）。\n\n"
            "★ **迁移**：`rsync -avn` 是**演练**（`-n` = dry-run），"
            "真正执行前必做；`--exclude='.git'` 排除目录。"),
        tags=["rsync", "-avz", "同步", "增量"]))

    out.append(C(
        "看主机名（临时改名，不重启）",
        "要给机器设个新主机名 `web01`，**立刻生效**（不用重启）。\n\n"
        "写出这条命令。",
        ["hostnamectl set-hostname web01", "hostnamectl set-hostname web01 --static"],
        sec=sec, diff=2,
        exp=(
            "`hostnamectl set-hostname web01`。\n\n"
            "★ 它是 systemd 提供的工具，"
            "会同时更新**运行中的主机名**和 `/etc/hostname` 文件，"
            "所以**立刻生效且重启后保持**。\n\n"
            "★ 老写法 `hostname web01` 只改**运行时**的值，"
            "重启就回去了 —— 这是「我明明改了名字，重开又变回去」的原因。\n\n"
            "★ 与 `hosts` 文件的关系：`hostnamectl` **不碰** `/etc/hosts`。"
            "如果本机服务依赖「主机名能解析到自己」，还得手动在 `/etc/hosts` 加一行 "
            "`127.0.1.1 web01`（否则 `sudo` 可能变慢、"
            "某些服务启动时解析失败）。\n\n"
            "★ **迁移**：`hostnamectl` 不带参数就是**查看**"
            "（系统版本、内核、架构、主机名一次看全）。"),
        tags=["hostnamectl", "主机名", "systemd"]))

    out.append(C(
        "看当前系统的网络设备列表与状态",
        "要确认网卡是不是**起来了**（UP/DOWN）。\n\n"
        "写出这条命令。",
        ["ip link", "ip link show", "ip -br link"],
        sec=sec, diff=2,
        exp=(
            "`ip link`（`ip -br link` 更简洁）。\n\n"
            "★ 输出里每个网卡的第一行末尾有状态标记：\n"
            "- `UP` —— 网卡已启用\n"
            "- `NO-CARRIER` —— **没插网线 / 没连上对端**\n"
            "- `DOWN` —— 被管理员 `ip link set down` 关了\n"
            "- `LOWER_UP` —— 物理链路真的通着\n\n"
            "★ `ip link` 是**链路层**（MAC、状态），"
            "`ip addr` 是**网络层**（IP 地址）。"
            "「网卡起来了但没 IP」和「网卡根本没起来」是两种完全不同的故障。\n\n"
            "★ **迁移**：`ip link set eth0 up` 启用网卡；"
            "`ip -s link` 看收发统计（有没有丢包）；"
            "`ethtool eth0` 看速率/双工（`Speed: 1000Mb/s`）。"),
        tags=["ip", "link", "网卡"]))

    out.append(C(
        "在远程机器上执行一条命令（不登录）",
        "要在 `10.0.0.5` 上跑 `df -h` 并把结果拿回来，**不进入交互 shell**。\n\n"
        "写出这条命令。",
        ["ssh deploy@10.0.0.5 df -h", "ssh deploy@10.0.0.5 'df -h'",
         "ssh -p 2222 deploy@10.0.0.5 df -h"],
        sec=sec, diff=2,
        exp=(
            "`ssh deploy@10.0.0.5 df -h`。\n\n"
            "★ `ssh host 命令` 里，**命令之后的所有参数都会被原样传给远程 shell**，"
            "所以 `ssh host df -h` 等价于 `ssh host 'df -h'`。\n\n"
            "★ 但一旦有**重定向、管道、变量**就必须加引号："
            "`ssh host 'ls | wc -l'` 里的 `|` 才会在**远程**执行；"
            "不加引号的话 `|` 会被**本地** shell 先解释，"
            "变成「把 ssh 的输出管道给本地的 wc」。这个坑极常见。\n\n"
            "★ ssh 不带 `-t` 时**没有 TTY**，"
            "所以 `sudo`、`top` 这类需要终端的命令会报错，"
            "要加 `-t`（分两次：`-t -t` 强制）。\n\n"
            "★ **迁移**：`ssh host 'cmd' > local.txt` 把远程结果存到本地；"
            "`for h in h1 h2 h3; do ssh $h uptime; done` 批量巡检。"),
        tags=["ssh", "远程执行", "引号"]))

    out.append(C(
        "查本机的 DNS 配置与解析结果",
        "域名解析不对，要先确认用的是哪个 DNS 服务器。\n\n"
        "写出这条命令。",
        ["cat /etc/resolv.conf", "resolvectl status", "systemd-resolve --status"],
        sec=sec, diff=2,
        exp=(
            "`cat /etc/resolv.conf`。\n\n"
            "★ 关键认知：**在现代 Fedora 上这个文件通常是「生成物」**，"
            "由 `systemd-resolved` 或 NetworkManager 写入，"
            "手工改会被下次网络变化覆盖。真正的配置在 "
            "`/etc/systemd/resolved.conf` 或 NetworkManager 的连接配置里。\n\n"
            "★ `resolvectl status` 是看**实际生效** DNS 的正确工具"
            "（含每个网卡分别用哪个 DNS、哪个域走哪个链路）。\n\n"
            "★ `nameserver 127.0.0.53` 是 `systemd-resolved` 的**本地存根**，"
            "不是真的 DNS 服务器 —— 看到它别以为配错了。\n\n"
            "★ **迁移**：验证解析：`getent hosts example.com`（走系统解析器，"
            "和程序行为一致）或 `dig example.com`（直接问 DNS，"
            "绕过 `/etc/hosts`）。两者结果不同就说明是 hosts 文件在起作用。"),
        tags=["DNS", "resolv.conf", "resolvectl"]))

    return out


# ===================================================================== #
#  十二、命令特训 · 软件包与服务
# ===================================================================== #
def part_pkg() -> list[dict]:
    sec = "命令特训 · 软件包与服务"
    out: list[dict] = []

    out.append(C(
        "搜一个软件包（还没装）",
        "要装 `htop`，先确认仓库里有没有这个包。\n\n"
        "写出这条命令（Fedora/dnf）。",
        ["dnf search htop", "dnf list htop", "dnf info htop"],
        sec=sec, diff=1,
        exp=(
            "`dnf search htop`（`dnf info htop` 更精确）。\n\n"
            "★ 三者的侧重不同：\n"
            "- `dnf search` 搜**名称与描述**，可能给出一堆相关结果\n"
            "- `dnf info` 查**指定包**的版本、大小、简介、仓库 —— 最有用\n"
            "- `dnf list` 列**已安装 + 可安装**，`--installed` / `--available` 过滤\n\n"
            "★ `dnf` 是 Fedora 的包管理器（`yum` 是它的前身，"
            "现在 `yum` 是指向 `dnf` 的软链，敲哪个都一样）。\n\n"
            "★ **迁移**：`dnf provides '*/bin/htop'` 按**文件**反查包；"
            "`dnf search --all` 连描述里的关键词一起搜；"
            "`dnf repoquery -l htop` 看一个包会装哪些文件。"),
        tags=["dnf", "search", "软件包"]))

    out.append(C(
        "安装一个软件包（自动确认）",
        "脚本里要装 `nginx`，**不能卡在 `Is this ok [y/N]` 上**。\n\n"
        "写出这条命令。",
        ["dnf install -y nginx", "dnf -y install nginx", "dnf install --assumeyes nginx"],
        sec=sec, diff=2,
        exp=(
            "`dnf install -y nginx`。\n\n"
            "★ `-y`（`--assumeyes`）**自动回答 yes**，"
            "这是所有自动化脚本的必备项 —— 不加就会挂在交互提示上，"
            "在 CI 里表现为「任务超时」。\n\n"
            "★ **`-y` 是有风险的**：它连「要卸载 200 个包」这种事也会答应。"
            "所以在生产机上，安装前先 `dnf install --assumeno nginx` "
            "看一遍**它打算做什么**（`--assumeno` 会在最后一步拒绝，但会打印完整计划）。\n\n"
            "★ 更稳的做法：`dnf install -y --setopt=install_weak_deps=False nginx` "
            "避免拉进来一堆推荐包。\n\n"
            "★ **迁移**：`dnf upgrade --refresh` 升级全部（`upgrade` 与 `update` 同义）；"
            "`dnf remove` 卸载；`dnf autoremove` 清孤儿依赖。"),
        tags=["dnf", "install", "-y"]))

    out.append(C(
        "查一个包装了哪些文件",
        "要知道 `nginx` 到底把配置装到哪了。\n\n"
        "写出这条命令。",
        ["rpm -ql nginx", "dnf repoquery -l nginx", "rpm -q --list nginx"],
        sec=sec, diff=3,
        exp=(
            "`rpm -ql nginx`。\n\n"
            "`rpm -q`（query）+ `-l`（list）= 列出该包安装的**所有文件**。"
            "配置一般在 `/etc/nginx/`，二进制在 `/usr/sbin/nginx`，"
            "unit 文件在 `/usr/lib/systemd/system/nginx.service`。\n\n"
            "★ **`rpm -ql` 只能查已安装的包**。"
            "查「**还没装**的包会装哪些文件」要用 `dnf repoquery -l nginx` —— "
            "这是两者最关键的差别。\n\n"
            "★ 反过来「这个文件属于哪个包」是 `rpm -qf <路径>`。\n\n"
            "★ **迁移**：`rpm -qpl x.rpm` 看一个 **.rpm 文件**的内容"
            "（安装前检查，避免装进来一堆东西）；"
            "`rpm -qc nginx` 只列**配置文件**，改配置前先看它更省事。"),
        tags=["rpm", "-ql", "文件清单"]))

    out.append(C(
        "启动一个服务并设为开机自启",
        "装好 `nginx` 之后，要**现在启动**并且**开机自动起**。\n\n"
        "写出这条命令（一条搞定）。",
        ["systemctl enable --now nginx", "systemctl enable nginx --now",
         "systemctl enable --now nginx.service"],
        sec=sec, diff=2,
        exp=(
            "`systemctl enable --now nginx`。\n\n"
            "两个动作合成一条：\n"
            "- `enable` 建**开机自启**的软链（写进 target 的 wants 目录）\n"
            "- `--now` 顺手**立刻启动**\n\n"
            "★ 分开写是 `systemctl enable nginx && systemctl start nginx`。"
            "`--now` 的价值是「不会漏做一步」—— "
            "「只 enable 没 start」是最常见的部署失误："
            "当前这次开机里服务仍然是停的。\n\n"
            "★ **`enable` 不等于 `start`，`start` 也不等于 `enable`**，"
            "这是 systemd 最该记清楚的一对概念：\n"
            "- `start` 管**现在**\n"
            "- `enable` 管**以后**\n\n"
            "★ **迁移**：`systemctl disable --now nginx` 反之；"
            "`systemctl restart nginx` 重启（会中断连接）；"
            "`systemctl reload nginx` 只重载配置（不断连接，改配置后优先用它）。"),
        tags=["systemctl", "enable", "--now", "自启"]))

    out.append(C(
        "看一个服务的运行状态",
        "`nginx` 起不来，先看它现在什么状态。\n\n"
        "写出这条命令。",
        ["systemctl status nginx", "systemctl status nginx.service"],
        sec=sec, diff=1,
        exp=(
            "`systemctl status nginx`。\n\n"
            "输出要点：\n"
            "- `Active:` 那行是核心 —— `active (running)` 正常、"
            "`failed` 失败、`inactive (dead)` 没启动\n"
            "- `Loaded:` 是否 enabled\n"
            "- `Main PID` 主进程号\n"
            "- 最后几行日志（其实等于 `journalctl -u nginx -n 10`）\n\n"
            "★ **`status` 会截断日志**，"
            "真正排查要看 `journalctl -u nginx -xe`（`-e` 跳到末尾、"
            "`-x` 附带说明）。\n\n"
            "★ **迁移**：`systemctl status --failed` 列所有失败的服务；"
            "`systemctl is-active nginx` 只输出状态词（脚本用）；"
            "`systemctl is-enabled nginx` 查是否开机自启。"),
        tags=["systemctl", "status", "服务"]))

    out.append(C(
        "查看某个服务的日志",
        "`nginx` 报错，要看它的日志（不带分页、直接看最后 50 行）。\n\n"
        "写出这条命令。",
        ["journalctl -u nginx -n 50", "journalctl -u nginx --no-pager -n 50",
         "journalctl -u nginx -n 50 --no-pager"],
        sec=sec, diff=3,
        exp=(
            "`journalctl -u nginx -n 50`。\n\n"
            "- `-u` 按 **unit** 过滤（服务名）\n"
            "- `-n 50` 最后 50 行\n"
            "- `--no-pager` 不分页（脚本里必须加，否则会进 `less` 卡住）\n\n"
            "★ 其他高频选项：\n"
            "- `-f` 实时跟随（等于 `tail -f`）\n"
            "- `-e` 直接跳到末尾\n"
            "- `-b` 只看**本次开机**（排查「重启后好了但不知道为什么」，"
            "`-b -1` 看上一次开机）\n"
            "- `--since '10 min ago'` / `--since today` 按时间过滤\n"
            "- `-p err` 只看 error 及以上级别\n\n"
            "★ journal 是**二进制日志**，不能用 `grep` 直接读文件，"
            "但可以 `journalctl -u nginx | grep 关键字`。\n\n"
            "★ **迁移**：`journalctl -u nginx -p err -b --since '1 hour ago'` "
            "是排查「刚才出了什么错」的最短路径。"),
        tags=["journalctl", "-u", "日志"]))

    out.append(C(
        "让改过的配置立即生效（不重启服务）",
        "改完 `nginx.conf` 要让它生效，但**不想断开现有连接**。\n\n"
        "写出这条命令。",
        ["systemctl reload nginx", "nginx -s reload", "systemctl reload nginx.service"],
        sec=sec, diff=2,
        exp=(
            "`systemctl reload nginx`。\n\n"
            "`reload` 发的是 **SIGHUP**，语义由服务自己实现："
            "nginx 会**开新 worker 接管流量、优雅关闭旧 worker**，"
            "已有连接不中断。\n\n"
            "★ **`restart` 与 `reload` 的区别是运维基本功**：\n"
            "- `restart` = stop + start，**所有连接立刻断开**\n"
            "- `reload` = 重读配置，连接保持\n\n"
            "★ **不是所有服务都支持 reload**："
            "`systemctl reload` 前先确认 `systemctl show nginx -p CanReload` "
            "返回 `CanReload=yes`，否则会报 `Job type reload is not applicable`。\n\n"
            "★ **改完配置先测语法**：`nginx -t`。"
            "配置有错时 `reload` 会失败但**旧进程还在跑**，"
            "看起来「没反应」，实际是配置压根没通过校验。\n\n"
            "★ **迁移**：`systemctl daemon-reload` 是**另一件事** —— "
            "改了 `.service` 文件本身之后才需要它。"),
        tags=["systemctl", "reload", "nginx"]))

    out.append(C(
        "查一个包装没装、装的是什么版本",
        "要确认 `nginx` 有没有装、装的是哪个版本。\n\n"
        "写出这条命令。",
        ["rpm -q nginx", "dnf list installed nginx", "rpm -qi nginx"],
        sec=sec, diff=2,
        exp=(
            "`rpm -q nginx`。\n\n"
            "输出 `nginx-1.26.2-1.fc40.x86_64` 表示已装；"
            "输出 `package nginx is not installed` 表示没装。"
            "**注意：没装时退出码是 1**，脚本里要处理。\n\n"
            "★ `rpm -qi` 看**详细信息**（版本、安装日期、许可证、简介）；"
            "`dnf list installed nginx` 输出格式更友好且能识别仓库来源。\n\n"
            "★ **`rpm -q` 查不到但 `dnf` 说装了**的情况："
            "可能装的是**模块流（module stream）**版本，"
            "或者来自第三方仓库。`dnf list --installed` 会标出来源。\n\n"
            "★ **迁移**：`rpm -qa | wc -l` 数装了多少包；"
            "`rpm -qa --last | head` 看**最近装了什么**"
            "（排查「今天开始出问题」时非常有用）。"),
        tags=["rpm", "-q", "版本"]))

    out.append(C(
        "卸载一个软件包（连同不再需要的依赖）",
        "要彻底清掉 `httpd` 及其孤儿依赖。\n\n"
        "写出这条命令。",
        ["dnf remove httpd", "dnf autoremove httpd", "dnf remove -y httpd"],
        sec=sec, diff=3,
        exp=(
            "`dnf remove httpd`（清理孤儿依赖再补一条 `dnf autoremove`）。\n\n"
            "★ **`dnf remove` 默认会连带卸载「只被这个包依赖」的包** —— "
            "所以它可能一次删掉比你预期更多的东西。"
            "动手前用 `dnf remove --assumeno httpd` 看完整计划。\n\n"
            "★ `autoremove` 单独使用时清的是「**已经没有任何包依赖它**的残留包」"
            "（通常来自历史卸载）。它不是「删除某个包并清理依赖」的专用工具。\n\n"
            "★ **配置文件**默认保留（改名为 `.rpmsave`）—— "
            "重装后旧配置还在，有时会被吓一跳。\n\n"
            "★ **迁移**：`dnf history` 看操作历史，"
            "`dnf history undo <ID>` 撤销某次操作 —— "
            "「刚才手滑删了一堆东西」的救命命令。"),
        tags=["dnf", "remove", "autoremove"]))

    out.append(C(
        "列出所有已启用的软件仓库",
        "装不上某个包，怀疑是仓库没开或者被禁用了。\n\n"
        "写出这条命令。",
        ["dnf repolist", "dnf repolist --enabled", "dnf repolist -v"],
        sec=sec, diff=3,
        exp=(
            "`dnf repolist`。\n\n"
            "默认只列**已启用**的仓库；`--all` 连禁用的也列出来。"
            "`-v` 显示每个仓库的 baseurl 与包数量。\n\n"
            "★ **启用/禁用**：`dnf config-manager --set-enabled <repo>` / "
            "`--set-disabled <repo>`（`config-manager` 需要 `dnf-plugins-core`）。\n\n"
            "★ 临时从某个仓库装：`dnf --enablerepo=updates install pkg`；"
            "临时排除：`dnf --disablerepo=* --enablerepo=fedora install pkg`。\n\n"
            "★ 排查套路："
            "「包找不到」→ 先 `dnf repolist` 看仓库在不在、"
            "再 `dnf search`、再 `dnf provides`。"
            "很多时候是**仓库镜像还没同步**，换镜像或等一会儿。\n\n"
            "★ **迁移**：`dnf clean all` 清缓存"
            "（元数据损坏时必做）；`dnf makecache` 重建缓存。"),
        tags=["dnf", "repolist", "仓库"]))

    out.append(C(
        "看系统启动时哪些服务失败了",
        "机器重启后某个服务没起来，但不知道是哪个。\n\n"
        "写出这条命令。",
        ["systemctl --failed", "systemctl list-units --failed", "systemctl list-units --state=failed"],
        sec=sec, diff=2,
        exp=(
            "`systemctl --failed`。\n\n"
            "它列出所有 **load 状态为 failed** 的 unit —— "
            "开机自启失败、运行中崩溃的都会在这里。\n\n"
            "★ 输出为空 = 没有失败的服务（正常的机器就应该是空的）。\n\n"
            "★ 找到之后的标准流程：\n"
            "1. `systemctl status <name>` 看退出码与最后几条日志\n"
            "2. `journalctl -u <name> -xe` 看完整报错\n"
            "3. `systemctl reset-failed <name>` 清掉 failed 标记（改了配置后）\n\n"
            "★ **迁移**：`systemctl list-units --type=service --all` 看全部服务"
            "（含没启动的）；"
            "`systemd-analyze blame` 看**开机时谁最慢**"
            "（排查开机慢的第一条命令）。"),
        tags=["systemctl", "--failed", "启动失败"]))

    out.append(C(
        "看一个 .rpm 文件里有什么（安装前检查）",
        "别人给了一个 `custom.rpm`，装之前想知道它会往系统里放什么。\n\n"
        "写出这条命令。",
        ["rpm -qpl custom.rpm", "rpm -qlp custom.rpm", "rpm -qpi custom.rpm"],
        sec=sec, diff=4,
        exp=(
            "`rpm -qpl custom.rpm`。\n\n"
            "★ **`-p` 是关键**：它让 `rpm` 处理「**一个包文件**」而不是「已安装的包」。"
            "所以 `-qpl` = query + package file + list。\n\n"
            "★ 没有 `-p` 时 `rpm -ql custom.rpm` 会去查一个**名叫 `custom.rpm` 的已装包**，"
            "报 `package custom.rpm is not installed` —— 这个报错很有迷惑性，"
            "看起来像「文件不存在」，其实是用错了模式。\n\n"
            "★ `-qpi` 看包信息（版本、依赖、简介），`-qpR` 看**依赖要求**。\n\n"
            "★ **迁移**：装之前最该看的是 `-qpl` 里有没有奇怪路径"
            "（比如 `/etc/passwd` 这种覆盖系统文件），"
            "以及 `-qp --scripts` 里的安装前后脚本（`%post` 可能干任何事）。"),
        tags=["rpm", "-qpl", "-p", "rpm 文件"]))

    out.append(C(
        "查看某个服务依赖哪些其他服务",
        "要停一个服务，但怕影响到别人，先看**依赖关系**。\n\n"
        "写出这条命令。",
        ["systemctl list-dependencies nginx", "systemctl list-dependencies --reverse nginx"],
        sec=sec, diff=4,
        exp=(
            "`systemctl list-dependencies nginx`。\n\n"
            "默认显示「**这个服务需要什么**」（依赖树，向下）；"
            "`--reverse` 显示「**谁需要这个服务**」（被依赖关系，向上）—— "
            "后者才是「停掉它会影响谁」的答案。\n\n"
            "★ 停服务前真正该查的两件事：\n"
            "1. `systemctl list-dependencies --reverse nginx` 谁会受影响\n"
            "2. `ss -ltnp | grep nginx` 它占着什么端口\n\n"
            "★ 依赖类型也很重要："
            "`Requires` 是强依赖（停这个，被依赖的也停）；"
            "`Wants` 是弱依赖（尽力而为，不阻塞）；"
            "`After`/`Before` 只是**启动顺序**，不构成依赖。\n\n"
            "★ **迁移**：`systemctl list-dependencies --all` 展开完整树；"
            "`systemctl show nginx -p Requires,Wants` 只看关键字段。"),
        tags=["systemctl", "依赖", "reverse"]))

    out.append(C(
        "清理 dnf 缓存与无用包",
        "`/var/cache` 涨得厉害，要清掉包管理器缓存。\n\n"
        "写出这条命令。",
        ["dnf clean all", "dnf clean packages", "dnf clean all && dnf autoremove -y"],
        sec=sec, diff=2,
        exp=(
            "`dnf clean all`。\n\n"
            "它会清掉：`packages`（下载的 rpm）、`metadata`（仓库元数据）、"
            "`dbcache`、`expire-cache`。"
            "**其中 metadata 占的空间常常比包本身还大**。\n\n"
            "★ 只清包不清元数据：`dnf clean packages`（下次装包不用重新拉元数据，更快）。\n\n"
            "★ 清完下次 `dnf` 操作会**重新下载元数据**，"
            "所以第一次会慢一点 —— 这是正常的，不是出问题。\n\n"
            "★ **`/var/cache/dnf` 是主要占用点**，"
            "另外 `/var/cache` 下还有 `PackageKit`、`fwupd` 等缓存。"
            "排查用 `du -sh /var/cache/*`。\n\n"
            "★ **迁移**：`dnf autoremove -y` 清孤儿包；"
            "`journalctl --vacuum-size=500M` 清 journal 日志"
            "（`/var/log/journal` 涨到几个 G 是常态）。"),
        tags=["dnf", "clean", "缓存"]))

    return out


# ===================================================================== #
#  十三、命令特训 · Shell 与管道
# ===================================================================== #
def part_shell() -> list[dict]:
    sec = "命令特训 · Shell 与管道"
    out: list[dict] = []

    out.append(C(
        "把一条命令的输出存到文件（覆盖）",
        "要把 `ls -l` 的结果存进 `list.txt`（**覆盖**原内容）。\n\n"
        "写出这条命令。",
        ["ls -l > list.txt", "ls -l 1> list.txt"],
        sec=sec, diff=1,
        exp=(
            "`ls -l > list.txt`。\n\n"
            "★ `>` 是**覆盖**（会先清空文件），`>>` 才是**追加**。"
            "搞混的后果是「文件里只剩最后一次的内容」。\n\n"
            "★ `>` 的执行顺序是：**先由 shell 打开并截断文件，再执行命令**。"
            "所以 `cmd > file` 里 `file` 在命令跑起来时就**已经空了**。"
            "这解释了两个经典事故：\n"
            "- `sort f > f` → 把 f 清空后排序空文件，结果 f 变空\n"
            "- 命令执行失败时，目标文件也已经被清空\n\n"
            "★ `1>` 是 `>` 的显式写法（fd 1 = stdout），日常直接写 `>`。\n\n"
            "★ **迁移**：不想覆盖已有文件：`set -o noclobber`（`>|` 可强制覆盖）；"
            "`tee` 能同时显示到屏幕并存文件。"),
        tags=["重定向", ">", "覆盖"]))

    out.append(C(
        "把错误输出丢弃，只留正常输出",
        "跑一条命令，屏幕被 `Permission denied` 刷满了，"
        "你只想看**正常结果**。\n\n"
        "写出这条命令（以 `find / -name x` 为例）。",
        ["find / -name x 2>/dev/null", "find / -name x 2> /dev/null"],
        sec=sec, diff=2,
        exp=(
            "`find / -name x 2>/dev/null`。\n\n"
            "★ `2` 是 **stderr** 的 fd 号，`/dev/null` 是「黑洞」设备"
            "（写进去就没了）。合起来 = 「把错误信息扔掉」。\n\n"
            "★ fd 速查：`0` stdin、`1` stdout、`2` stderr。"
            "所以 `2>` 是「重定向错误输出」，`1>` 是「重定向正常输出」。\n\n"
            "★ **`2>/dev/null` 与 `&>/dev/null` 的区别**："
            "前者只丢错误、后者**全丢**。"
            "还有 `2>&1`（错误并入正常输出）—— 三个写法经常被混用，"
            "结果一个报错都没看到。\n\n"
            "★ **迁移**：调试时**不要**丢错误输出 —— "
            "「命令没输出也没报错」是最难查的状态。"
            "宁可 `2>&1 | less` 看清楚。"),
        tags=["重定向", "2>", "/dev/null"]))

    out.append(C(
        "前一条命令成功才执行后一条",
        "要在 `mkDIR` 成功之后才 `cd` 进去，失败就**不要**往下走。\n\n"
        "写出这条命令（以 `mkdir -p /tmp/x` 和 `cd /tmp/x` 为例）。",
        ["mkdir -p /tmp/x && cd /tmp/x"],
        sec=sec, diff=1,
        exp=(
            "`mkdir -p /tmp/x && cd /tmp/x`。\n\n"
            "★ shell 的三种连接符语义完全不同：\n"
            "- `&&` —— 前面**成功**（退出码 0）才执行\n"
            "- `||` —— 前面**失败**才执行\n"
            "- `;` —— **无条件**都执行\n\n"
            "★ 写成 `mkdir -p /tmp/x ; cd /tmp/x` 的后果："
            "`mkdir` 失败时 `cd` 照样跑，于是你在错误的目录里继续操作，"
            "后面所有相对路径全错 —— 而且没有任何一处报错指向真正的原因。\n\n"
            "★ 退出码约定：**0 = 成功，非 0 = 失败**（与 C 的 `main` 返回一致）。`$?` 取上一条的退出码。\n\n"
            "★ **迁移**：`cmd1 && cmd2 || cmd3` 是「成功走 A、失败走 B」；"
            "但注意 `A && B || C` 里若 B 失败也会走 C（不是三元运算），"
            "要严格分支用 `if`。"),
        tags=["&&", "||", "退出码"]))

    out.append(C(
        "统计目录下文件个数",
        "要数当前目录下有多少个文件（**含子目录，不含目录本身**）。\n\n"
        "写出这条命令（管道 + 计数）。",
        ["find . -type f | wc -l", "ls -R | wc -l"],
        sec=sec, diff=2,
        exp=(
            "`find . -type f | wc -l`。\n\n"
            "★ 这是「**管道**」最典型的用法："
            "`|` 把前一条命令的 **stdout** 接到后一条的 **stdin**。\n\n"
            "★ **`ls -R | wc -l` 是错的**（本题的坑）："
            "`ls -R` 的输出里混着 `./subdir:` 这样的**目录标题行**和空行，"
            "数出来的数字比真实文件数多。"
            "「用 `ls` 数文件」几乎总是不准 —— 因为 `ls` 是给人看的。\n\n"
            "★ **`ls | wc -l` 也有坑**：文件名里有换行时会被算成两个；"
            "隐藏文件不在里面；目录也算进去了。\n\n"
            "★ **迁移**：只要当前层：`find . -maxdepth 1 -type f | wc -l`；"
            "要「真数字」用 `find ... -print0 | tr -cd '\\0' | wc -c`。"),
        tags=["管道", "wc", "find", "计数"]))

    out.append(C(
        "在管道里同时看输出又存文件",
        "想让命令的输出**既显示在屏幕上又存一份到文件**。\n\n"
        "写出这条命令（以 `make` 为例）。",
        ["make 2>&1 | tee build.log", "make | tee build.log"],
        sec=sec, diff=3,
        exp=(
            "`make 2>&1 | tee build.log`。\n\n"
            "★ `tee` 像三通管：**stdin 同时流向 stdout 和文件**。\n"
            "`-a` 是追加（默认覆盖）。\n\n"
            "★ **为什么这里必须 `2>&1`**：`|` 只接 stdout，"
            "错误信息走 stderr，**不会进管道**。"
            "所以不加 `2>&1` 的话，屏幕上能看到报错、"
            "但 `build.log` 里一条错误都没有 —— "
            "拿着日志去问人，人家看不出问题。\n\n"
            "★ 顺序：`2>&1` 必须在 `|` **之前**。"
            "写 `make | tee log 2>&1` 是把 `tee` 的 stderr 重定向，"
            "完全另一回事。\n\n"
            "★ **迁移**：`sudo cmd | tee /root/out.log` —— "
            "`sudo` 只作用于 `cmd`，重定向由**当前 shell**执行，"
            "所以往 root 目录写会失败。正确写法：`sudo sh -c 'cmd > /root/out.log'`。\n\n"
            "★ 同时写两个文件：`tee a.log b.log`。"),
        tags=["tee", "管道", "2>&1", "日志"]))

    out.append(C(
        "定义一个变量并在命令里使用",
        "要设 `DIR=/var/log` 然后用它做 `ls`。\n\n"
        "写出这两条命令（赋值 + 使用）。",
        ["DIR=/var/log && ls $DIR", "DIR=/var/log; ls \"$DIR\"", "DIR=/var/log\nls $DIR"],
        sec=sec, diff=2,
        exp=(
            "`DIR=/var/log` 然后 `ls \"$DIR\"`。\n\n"
            "★ **`=` 两边不能有空格**！"
            "`DIR = /var/log` 会被解释成「执行一个叫 `DIR` 的命令，参数是 `=` 和 `/var/log`」，"
            "报 `DIR: command not found`。这是 shell 变量赋值的第一条铁律。\n\n"
            "★ 使用时要加 **`$`**，赋值时**不加**。"
            "`$DIR` 展开成值，`${DIR}` 是同一件事但边界更清楚"
            "（`${DIR}_log` 才不会把 `_log` 当成变量名的一部分）。\n\n"
            "★ **永远给变量加双引号**：`\"$DIR\"`。"
            "不加引号时值里有空格会被拆成多个参数，"
            "`ls $DIR` 遇到 `/my docs` 就变成 `ls /my docs`（两个参数）。\n\n"
            "★ **迁移**：`export DIR=...` 让子进程也能看到；"
            "`readonly DIR=...` 防误改；"
            "`unset DIR` 删除。"),
        tags=["变量", "赋值", "引号"]))

    out.append(C(
        "给一条长命令起个别名",
        "每次都要敲 `ls -alh --color=auto` 太累，要起个别名 `ll`。\n\n"
        "写出这条命令。",
        ["alias ll='ls -alh --color=auto'", "alias ll=\"ls -alh --color=auto\""],
        sec=sec, diff=2,
        exp=(
            "`alias ll='ls -alh --color=auto'`。\n\n"
            "★ **单引号不能省**：不加引号时 `alias ll=ls -alh` 会被解析成"
            "「`alias ll=ls`」加「`-alh` 作为参数」，"
            "结果别名只等于 `ls`，而且 shell 会报 `-alh: command not found`。\n\n"
            "★ 别名只在**当前 shell 会话**有效。"
            "要持久化写进 `~/.bashrc`（交互式非登录 shell）"
            "或 `~/.bash_profile`（登录 shell）。"
            "**改完要 `source ~/.bashrc` 或重开终端**。\n\n"
            "★ 别名的局限：只做**文本替换**，不能带参数逻辑、不能用在脚本里"
            "（非交互 shell 默认不展开别名）。复杂需求用**函数**。\n\n"
            "★ **迁移**：`alias` 不带参数列出所有别名；"
            "`unalias ll` 删除；"
            "`\\ls` 或 `command ls` 可以**绕过别名**执行原始命令。"),
        tags=["alias", "别名", "bashrc"]))

    out.append(C(
        "把命令的输出作为另一个命令的参数",
        "要把 `find` 找到的文件交给 `rm` 删除（**文件名可能有空格**）。\n\n"
        "写出这条安全写法。",
        ["find . -name '*.tmp' -print0 | xargs -0 rm",
         "find . -name '*.tmp' -exec rm {} +",
         "find . -name '*.tmp' -delete"],
        sec=sec, diff=4,
        exp=(
            "`find . -name '*.tmp' -print0 | xargs -0 rm`（或 `-exec rm {} +`）。\n\n"
            "★ **`-print0` + `-0` 这一对是核心**："
            "`-print0` 用 **NUL 字节**分隔文件名（文件名里不可能有 NUL），"
            "`xargs -0` 按 NUL 切分。"
            "这样就**彻底免疫空格、换行、引号**。\n\n"
            "★ 普通写法 `find ... | xargs rm` 的后果："
            "文件名 `my file.tmp` 会被切成 `my` 和 `file.tmp` 两个参数，"
            "于是 `rm my` —— **删错文件**。"
            "这是 Linux 上最经典的「一句话删库」事故。\n\n"
            "★ `-exec cmd {} +` 是另一种安全写法（直接传参，不经过文本），"
            "而且**性能更好**（攒批执行）。"
            "`-exec cmd {} \\;` 是逐个执行（慢但能用在中间位置）。\n\n"
            "★ **迁移**：`xargs -n 1 -0` 逐个执行；"
            "`xargs -p` 执行前确认；"
            "`xargs -I{}` 把 `{}` 放到命令中间：`xargs -0 -I{} mv {} /backup/`。"),
        tags=["xargs", "-print0", "空格", "安全"]))

    out.append(C(
        "在 shell 里做算术运算",
        "要让 `count` 加 1。\n\n"
        "写出这条命令（假设 `count=5`）。",
        ["count=$((count+1))", "((count++))", "let count=count+1"],
        sec=sec, diff=2,
        exp=(
            "`count=$((count+1))`。\n\n"
            "★ `$(( ))` 是**算术展开**，POSIX 标准，所有 shell 都支持。"
            "里面可以写 `+ - * / % **`、比较、位运算。\n\n"
            "★ 三种写法的区别：\n"
            "- `$(( ))` 返回**值**，可以赋给变量\n"
            "- `(( ))` 返回**退出码**（结果非 0 时退出码为 0），"
            "适合写 `if (( count > 10 ))`\n"
            "- `let` 是老式写法，语义同 `(( ))`\n\n"
            "★ **shell 默认全是整数运算**：`$((5/2))` = `2`，不是 `2.5`。"
            "要小数必须 `bc` 或 `awk`：`echo '5/2' | bc -l`。\n\n"
            "★ `&&` 与 `||` 别当逻辑运算用："
            "shell 里它们是「命令连接符」，"
            "逻辑判断要用 `[ ]` / `[[ ]]`。\n\n"
            "★ **迁移**：`$((count++))` 的返回值是**自增前的值**，"
            "所以 `x=$((count++))` 里 x 拿到旧值；"
            "要新值用 `x=$((++count))`。"),
        tags=["算术", "$(())", "变量"]))

    out.append(C(
        "判断一个文件存不存在（脚本写法）",
        "脚本里要先判断 `/etc/nginx/nginx.conf` 在不在，"
        "不存在就退出。\n\n"
        "写出这个判断条件（`if` 的那一行）。",
        ["if [ ! -f /etc/nginx/nginx.conf ]; then",
         "if [[ ! -f /etc/nginx/nginx.conf ]]; then",
         "if test ! -f /etc/nginx/nginx.conf; then"],
        sec=sec, diff=3,
        exp=(
            "`if [ ! -f /etc/nginx/nginx.conf ]; then`。\n\n"
            "★ 文件测试符常用几个：\n"
            "- `-f` 是**普通文件**（存在且不是目录）\n"
            "- `-d` 是目录、`-e` 存在（任何类型）\n"
            "- `-r`/`-w`/`-x` 可读/可写/可执行\n"
            "- `-s` **存在且非空**（大小为 0 时为假）\n\n"
            "★ **`[` 是一个命令**（等价 `test`），"
            "所以 `[` 后面、`]` 前面**必须各有一个空格**。"
            "写成 `[-f x]` 会报 `[-f: command not found` —— "
            "这个报错让人一脸懵，但原因就是这么朴素。\n\n"
            "★ `[ ]`（POSIX）与 `[[ ]]`（bash 扩展）的区别："
            "`[[ ]]` 里**不需要给变量加引号**、支持 `&&`/`||`/正则 `=~`；"
            "`[ ]` 里变量为空时会报 `unary operator expected`。"
            "脚本里用 `[[ ]]` 更省心（但 `sh`/dash 不支持）。\n\n"
            "★ **迁移**：`[ -f f ] && echo yes || echo no` 是简写；"
            "目录不存在就建：`[ -d d ] || mkdir -p d`。"),
        tags=["if", "test", "-f", "脚本"]))

    out.append(C(
        "遍历一个目录下所有 .log 文件并逐个处理",
        "要对 `./logs` 下每个 `.log` 文件执行 `gzip`（**文件名可能有空格**）。\n\n"
        "写出这个 for 循环（一行写完）。",
        ["for f in ./logs/*.log; do gzip \"$f\"; done",
         "find ./logs -name '*.log' -exec gzip {} +"],
        sec=sec, diff=4,
        exp=(
            "`for f in ./logs/*.log; do gzip \"$f\"; done`。\n\n"
            "★ **`\"$f\"` 的引号是必须的**："
            "不加引号时文件名里的空格会让 `$f` 展开成多个词，"
            "`gzip my file.log` 就变成「压 my 和 file.log 两个文件」。\n\n"
            "★ **通配符不会被拆开**：`for f in *.log` 里 shell 是先展开通配再赋值，"
            "所以带空格的文件名**整体**赋给 `f`（这一步是安全的）。"
            "危险的是后面**使用** `$f` 时不加引号。\n\n"
            "★ 目录为空时 `for f in *.log` 会得到**字面量** `*.log`"
            "（bash 默认不报错），于是去处理一个叫 `*.log` 的文件、"
            "报 `No such file`。"
            "加 `shopt -s nullglob` 或先判断 `[ -e \"$f\" ] || continue`。\n\n"
            "★ **迁移**：要处理**递归**（子目录也要），"
            "`for` 循环不够，得用 `find ... -exec` 或 `while IFS= read -r -d '' f` "
            "配合 `find -print0`（后者是处理任意文件名的标准做法）。"),
        tags=["for", "循环", "引号", "通配"]))

    out.append(C(
        "在管道里过滤出想要的行并排序",
        "要从 `ps aux` 里取出所有 `python` 进程，只显示**用户名和命令行**，"
        "并按用户名排序。\n\n"
        "写出这条命令。",
        ["ps aux | grep python | awk '{print $1, $11}' | sort",
         "ps aux | grep [p]ython | awk '{print $1, $11}' | sort"],
        sec=sec, diff=4,
        exp=(
            "`ps aux | grep python | awk '{print $1, $11}' | sort`。\n\n"
            "★ 四个环节各干一件事：`ps` 取进程、`grep` 过滤、"
            "`awk` 挑列、`sort` 排序 —— 这就是管道的思维方式：**每条只做一件事**。\n\n"
            "★ **`grep [p]ython` 这个写法的意义**（本题的进阶点）："
            "`grep python` 会**匹配到 grep 自己**（因为它的命令行里就含 `python`）。"
            "`[p]ython` 是正则「p 或 …」的写法，"
            "**grep 自己的命令行里是 `[p]ython` 而不是 `python`**，"
            "所以它不会匹配自己。这是老运维的经典技巧。\n\n"
            "★ **更干净的替代**：`pgrep -af python` —— "
            "直接按名字找并显示命令行，不需要管道，也不会匹配自己。\n\n"
            "★ **迁移**：`ps aux --sort=-%cpu | head -5` 取 CPU 前 5，"
            "比 `| sort` 更准确（`ps` 自己会排序，而且按数值而不是文本）。"),
        tags=["管道", "grep", "awk", "ps"]))

    out.append(C(
        "写一个简单的 if-elif-else 判断",
        "脚本要根据参数值 `dev`/`prod` 输出不同内容，其他值报错退出。\n\n"
        "写出这个完整的 if 结构（`$1` 是参数）。",
        ["if [ \"$1\" = dev ]; then echo dev; elif [ \"$1\" = prod ]; then echo prod; else echo err; exit 1; fi"],
        sec=sec, diff=4,
        exp=(
            "```bash\n"
            "if [ \"$1\" = dev ]; then\n"
            "    echo dev\n"
            "elif [ \"$1\" = prod ]; then\n"
            "    echo prod\n"
            "else\n"
            "    echo err\n"
            "    exit 1\n"
            "fi\n"
            "```\n\n"
            "★ **字符串比较用单个 `=`**（POSIX 写法），bash 里 `==` 也认，"
            "但 `sh`/dash 只认 `=`。数值比较要用 `-eq`/`-lt`/`-gt`，"
            "**不能用 `=` 或 `<`**（`<` 在 `[ ]` 里会被当成重定向）。\n\n"
            "★ **`\"$1\"` 的引号不能省**：参数没给时 `$1` 为空，"
            "不加引号会变成 `[ = dev ]` —— `[` 收到 2 个参数，"
            "报 `unary operator expected`。\n\n"
            "★ **`fi` 是 `if` 倒着写**，收尾用。"
            "`elif` 可以有多层，`else` 可选。\n\n"
            "★ **迁移**：多个固定值匹配用 `case` 更清爽："
            "`case \"$1\" in dev) ... ;; prod) ... ;; *) ... ;; esac`。\n\n"
            "★ 脚本开头加 `set -euo pipefail`："
            "出错即停、用未定义变量即停、管道任一环失败即失败 —— "
            "这是 shell 脚本健壮性的三大开关。"),
        tags=["if", "elif", "参数", "脚本"]))

    out.append(C(
        "查一条命令在历史里执行过几次",
        "前几天敲过一条很长的 `rsync`，想找回来。\n\n"
        "写出这条命令（用历史搜索）。",
        ["history | grep rsync", "history | grep 'rsync'"],
        sec=sec, diff=1,
        exp=(
            "`history | grep rsync`。\n\n"
            "★ `history` 输出的是**带行号的历史列表**，"
            "想重新执行某条用 `!123`（行号）或 `!!`（上一条）。\n\n"
            "★ **交互式更快的方式**是 `Ctrl+R`："
            "进入反向增量搜索，敲几个字母就定位到最近匹配的命令，"
            "再按 `Ctrl+R` 继续往前找，`Enter` 执行、`Esc` 退出编辑。\n\n"
            "★ **历史默认不被立即写入**：一个终端里的命令要**退出后**才进历史文件，"
            "所以在另一个窗口 `history | grep` 找不到刚敲的。"
            "想让历史实时写入：`shopt -s histappend` + "
            "`PROMPT_COMMAND='history -a'`。\n\n"
            "★ **历史里有敏感信息**（密码、token）的风险："
            "命令行带密码会被记进 `~/.bash_history`。"
            "脚本里用环境变量或 stdin 传密码，别写在命令行。\n\n"
            "★ **迁移**：`history -c` 清空当前会话；"
            "`history -w` 立即写盘；"
            "`HISTTIMEFORMAT='%F %T '` 让历史带上时间。"),
        tags=["history", "Ctrl+R", "历史"]))

    out.append(C(
        "让脚本在任何一步失败时立即退出",
        "写的部署脚本跑了半截失败了却还在继续，最后留下一个坏状态。\n\n"
        "要求：写出脚本**开头**该加的那一行。",
        ["set -e", "set -euo pipefail", "set -eu"],
        sec=sec, diff=3,
        exp=(
            "`set -e`。\n\n"
            "★ `set -e`（errexit）让脚本在**任一命令返回非 0** 时立刻退出。"
            "默认行为是「不管失败，继续往下跑」——"
            "这就是「跑了一半、状态烂掉」的根源。\n\n"
            "★ 三个开关一起写是实践标准：\n"
            "- `set -e` 出错即停\n"
            "- `set -u`（nounset）**使用未定义变量就报错**（默认是展开成空串，"
            "于是 `rm -rf $DIR/` 里 `$DIR` 没设就变成 `rm -rf /`）\n"
            "- `set -o pipefail` 管道里**任一环**失败都算失败"
            "（默认只看最后一环）\n\n"
            "★ `set -e` 有几个**失效场景**要知道："
            "命令在 `if` 条件里、在 `&&`/`||` 前面、"
            "或者用的是 `!` 取反时，都不触发退出。\n\n"
            "★ **迁移**：临时放宽某一条：`cmd || true`；"
            "调试时 `set -x` 打印每条执行的命令，`set +x` 关掉。"),
        tags=["set -e", "pipefail", "健壮性"]))

    out.append(C(
        "把命令放在子 shell 里执行，不影响当前环境",
        "要在**不改变当前目录**的前提下，在一个目录里跑几条命令。\n\n"
        "写出这条命令（用子 shell 括号）。",
        ["(cd /tmp/x && ls)", "(cd /tmp/x; ls -l)"],
        sec=sec, diff=3,
        exp=(
            "`(cd /tmp/x && ls)`。\n\n"
            "★ **圆括号 `( )` 开一个子 shell**：里面的 `cd`、变量赋值、"
            "`umask` 改动**全都不影响外面**。"
            "这是「临时切目录干活，干完自动回来」最干净的做法，"
            "比 `cd somewhere && cmd && cd -` 稳（后者中途失败就回不去了）。\n\n"
            "★ **花括号 `{ }` 的区别**：`{ cd /tmp/x && ls; }` 在**当前 shell** 里执行，"
            "`cd` 会**留下来**。而且 `{` 后面必须有空格、`}` 前面必须有 `;`。\n\n"
            "★ 子 shell 会**复制父 shell 的环境**，"
            "所以里面的变量能读到，但**改不了外面**。\n\n"
            "★ **迁移**：`(cd x && make) 2>&1 | tee log` 常用于「在子目录构建但不污染当前环境」；"
            "脚本里 `tar -C` 也是同一个思路（局部生效）。"),
        tags=["子shell", "括号", "cd"]))

    out.append(C(
        "把多行文本喂给命令（不建临时文件）",
        "要造两行测试数据喂给 `grep`，**不落盘**。\n\n"
        "要求：用一条管道完成（不要 `echo` 两次再用 `;`）。",
        ["printf 'line1\\nline2\\n' | grep pattern",
         "printf \"line1\\nline2\\n\" | grep pattern",
         "echo -e 'line1\\nline2' | grep pattern"],
        sec=sec, diff=4,
        exp=(
            "`printf 'line1\\nline2\\n' | grep pattern`。\n\n"
            "★ **为什么用 `printf` 不用 `echo`**："
            "`echo` 对转义序列的处理**因 shell 而异** —— "
            "bash 内建的 `echo` 默认**不解释** `\\n`（要 `-e`），"
            "而 `sh` 的 `echo` 常常解释。"
            "`printf` 是 POSIX 标准工具，行为**确定**，"
            "所以脚本里输出/造数据一律优先 `printf`。\n\n"
            "★ 末尾那个 `\\n` 别漏："
            "不写的话最后一行**没有换行符**，"
            "接 `grep`/`wc -l` 时会少算一行 —— "
            "这是「造的数据看起来少一行」的常见原因。\n\n"
            "★ 真正的**多行文本**用 heredoc：\n"
            "```bash\ngrep pattern <<'EOF'\nline1\nline2\nEOF\n```\n"
            "`'EOF'` 加引号表示内容原样传（`$VAR` 不展开）—— "
            "生成配置文件时**必须**加引号。\n\n"
            "★ **迁移**：`printf '%s\\n' a b c` 一次造三行；"
            "`<<<` 是 herestring（bash 特性）：`grep x <<< \"$VAR\"`。"),
        tags=["printf", "heredoc", "标准输入"]))

    out.append(C(
        "提取命令输出里的某一列并求和",
        "`du -sk /var/*` 输出的第一列是 KB 数。要把它们**加起来**得到总量。\n\n"
        "写出这条命令。",
        ["du -sk /var/* | awk '{sum += $1} END {print sum}'",
         "du -sk /var/* | awk '{s+=$1} END {print s}'"],
        sec=sec, diff=4,
        exp=(
            "`du -sk /var/* | awk '{sum += $1} END {print sum}'`。\n\n"
            "★ awk 的三段结构在这里全用上了：\n"
            "- `{sum += $1}` —— **每行执行一次**，累加第一列\n"
            "- `END {print sum}` —— **所有行处理完之后**执行一次\n"
            "（省略的 `BEGIN` 是「开始前执行一次」）\n\n"
            "★ **为什么要 `-k`**：`du -h` 输出的是 `1.2G`、`340M` 这种，"
            "awk **没法直接相加**（`1.2G + 340M` 不是数字）。"
            "`-k` 统一成 KB 整数，加完再换算。"
            "这是「想求和就别用 `-h`」的通用原则。\n\n"
            "★ awk 里未定义的变量**默认为 0**，所以 `sum` 不用初始化。\n\n"
            "★ **迁移**：`awk '{s+=$1} END {printf \"%.2f MB\\n\", s/1024}'` "
            "直接换算单位；"
            "求平均：`END {print sum/NR}`（`NR` 是总行数）。"),
        tags=["awk", "END", "求和", "du"]))

    return out


def build() -> list[dict]:
    """汇总所有命令题。"""
    out: list[dict] = []
    out += part_experiments()
    out += part_files()
    out += part_view()
    out += part_find()
    out += part_text()
    out += part_perm()
    out += part_user()
    out += part_proc()
    out += part_disk()
    out += part_archive()
    out += part_net()
    out += part_pkg()
    out += part_shell()
    return out
