"""Linux 线题库 —— **自动生成，不要手改**。

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
5. 第 11 ~ 16 讲讲义（第三部分：Shell / GCC / GTK / Qt / Python 环境 / Eclipse）——
   取自各讲的「一分钟速览」与「附录 A · 陷阱清单」。

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

LINUX_PROBLEMS: list[dict] = [
    {
        "title": "tar 的 -Z 到底压什么",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "tar",
            "压缩",
            "大小写",
            "课程纠错"
        ],
        "choices": [
            "调用 gzip 压缩",
            "调用 compress（老式 .Z 格式）压缩",
            "调用 zip 压缩",
            "调用 zstd 压缩"
        ],
        "source_section": "基础命令 · 先纠正六处",
        "statement_md": "你在网上抄到一条备份命令 `tar -Zcvf bak.tar.gz dir/`，想用它做 **gzip** 压缩。\n\n问题出在 `-Z` 上：它**不是** gzip。那 `-Z` 是什么？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`-Z` 是 **compress**，处理的是 1970 年代的老 `.Z` 格式，现在很多机器根本没装这个工具。\n\n**gzip 是小写 `-z`**。所以正确写法是 `tar -czvf bak.tar.gz dir/`。\n\n★ 这类坑的根因是：tar 的选项**大小写都真实存在**（`-z`/`-Z`、`-v`/`-V`、`-c`/`-C`），抄错一个字母不会报错，只会静默地干了另一件事。\n锚点：**日常用的那批全是小写**。"
            }
        ]
    },
    {
        "title": "tar 里「显示处理过程」是哪个选项",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "tar",
            "verbose",
            "大小写",
            "课程纠错"
        ],
        "choices": [
            "-V（大写）",
            "-v（小写）",
            "-x",
            "-t"
        ],
        "source_section": "基础命令 · 先纠正六处",
        "statement_md": "打包一个几 GB 的目录时，你想看到 tar 正在处理哪些文件。应该加哪个选项？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "小写 **`-v` = verbose（啰嗦模式）**，把正在处理的文件名逐个打出来。\n\n大写 `-V` 是 **`--label`** —— 给归档写一个**卷标**（不是打印过程），跟「显示进度」毫无关系。\n\n另外两个：`-x` 解包、`-t` 只列内容不解包。\n口诀：`czvf` 打包、`xzvf` 解包、`tzvf` 看内容。"
            }
        ]
    },
    {
        "title": "tar 里「创建归档」是哪个选项",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "tar",
            "create",
            "大小写",
            "课程纠错"
        ],
        "choices": [
            "-C（大写）",
            "-c（小写）",
            "-x",
            "-j"
        ],
        "source_section": "基础命令 · 先纠正六处",
        "statement_md": "下面四个 tar 选项，哪一个表示「**创建**一个新的归档文件」？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "小写 **`-c` = create**，创建归档。\n\n大写 `-C` 是 **`--directory`** —— **切换目录**，最常和解压连用：`tar -xzvf bak.tar.gz -C /tmp/out`（解到指定目录）。\n\n`-x` 解包；`-j` 走 bzip2（配 `.tar.bz2`）。"
            }
        ]
    },
    {
        "title": "从第 1000 行开始显示的正确写法",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "head",
            "tail",
            "coreutils",
            "课程纠错"
        ],
        "choices": [
            "head -n +1000 file",
            "head -n -1000 file",
            "tail -n +1000 file",
            "tail -n -1000 file"
        ],
        "source_section": "基础命令 · 先纠正六处",
        "statement_md": "课程提纲里写「`head -n +1000 file` 从 1000 行开始显示」。\n\n这条命令**会直接报错**。从第 1000 行显示到末尾，正确写法是？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "C",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|C\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`head` 不认 `+`**，会报 `head: invalid number of lines: '+1000'`。\n\n`+N` 这个语义**只属于 tail**：`tail -n +1000 file` = 从第 1000 行到末尾。\n\n顺便记牢另一半：`-N` 归 head —— `head -n -10 file` 是「去掉**最后** 10 行」。\n\n★ 一句口诀：**`+` 归 tail，`-` 归 head**。\n验证：`tail -n -5 f` 也会报错（tail 的 `-n` 只认数字或 `+数字`）。"
            }
        ]
    },
    {
        "title": "统计文件有多少行的正确命令",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "wc",
            "cat",
            "统计",
            "课程纠错"
        ],
        "choices": [
            "cat -n file1",
            "wc -l file1",
            "tail -n file1",
            "ls -l file1"
        ],
        "source_section": "基础命令 · 先纠正六处",
        "statement_md": "提纲里写「`cat -n file1` 表示文件的行数」。这个说法**不准确**。\n\n想**统计**一个文件有多少行，正确命令是？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`cat -n` 是**给输出的每一行加上行号**，不是统计行数 —— 对一个几十万行的文件，它既刷屏又慢。\n\n**`wc -l file1`** 才是数行数（`wc` = word count，`-l` = lines），输出形如 `42 file1`。\n\n★ 「用 `cat -n` 看最后一行行号，也能看出总行数」—— 能，但那是歪门邪道：\n大文件不划算，而且会往屏幕上倒几万行。"
            }
        ]
    },
    {
        "title": "列出「名字里含数字」的文件",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "ls",
            "通配符",
            "glob",
            "课程纠错"
        ],
        "choices": [
            "方括号是正则语法，ls 不支持",
            "[0-9] 只匹配「名字恰好是一个数字」的条目",
            "必须先 cd 到目标目录才行",
            "要写成 [0-9]* 才有用"
        ],
        "source_section": "基础命令 · 先纠正六处",
        "statement_md": "提纲里写「`ls [0-9]` 显示包含数字的文件名」。\n\n实际敲下去，你会发现 `report2.txt`、`log2026` 一个都没列出来。为什么？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`[0-9]` 是 shell 的 glob（通配符），它匹配的是「**整个名字恰好是一个字符、且这个字符是数字**」的条目 —— 比如 `1`、`7`。\n\n`report2.txt` 名字有 11 个字符，当然不匹配。\n\n正解：\n- **名字里含数字** → `ls *[0-9]*`\n- **以数字开头** → `ls [0-9]*`\n\n★ 顺带一提：`*` 是 shell 展开的（不是 ls 干的），所以匹配不上时 shell 会把 `*[0-9]*` 原样传给 ls。"
            }
        ]
    },
    {
        "title": "cd - 与 cd .. 效果相同吗",
        "subject": "linux",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 2,
        "total_score": 8,
        "tags": [
            "cd",
            "OLDPWD",
            "易混"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "基础命令 · A 组 认命令",
        "statement_md": "`cd -` 和 `cd ..` 是同一个意思，都用来回到上一级目录。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "错",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|错\n|错误\n|×\n|F\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**错**。两件事完全不同：\n\n- `cd ..` —— 按**目录结构**往上走一级。在 `/a/b/c` 里执行就到 `/a/b`。\n- `cd -` —— 按**访问历史**回到上一次所在的目录（用的是环境变量 `$OLDPWD`）。在 `/a/b/c` 里执行，可能跳到毫不相干的 `/var/log`。\n\n命令执行完，`cd -` 还会把目标目录打印出来（`cd ..` 不会）。"
            }
        ]
    },
    {
        "title": "查看目录本身（而不是里面）的权限",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "ls",
            "-d",
            "权限",
            "高频错点"
        ],
        "choices": [
            "ls -l /etc",
            "ls -ld /etc",
            "ls -a /etc",
            "ls -R /etc"
        ],
        "source_section": "基础命令 · A 组 认命令",
        "statement_md": "你想看 `/etc` **这个目录自己**的权限信息，输出只要一行。哪条命令对？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`ls -ld /etc`**。\n\n- `ls -l /etc` 列的是 `/etc` **里面**的条目 —— 输出几十行，但没有一行是 `/etc` 自己。\n- **`-d` = directory**，让 ls「**别展开**这个目录，只报它自己」。\n\n★ 这是「问某个目录的权限，答成了里面文件的权限」这个高频错点的正解。\n\n输出长这样（第一列就是权限）：\n```\ndrwxr-xr-x. 1 root root 8192 Oct 12 09:00 /etc\n```"
            }
        ]
    },
    {
        "title": "ls -a 与 ls -A 输出一样吗",
        "subject": "linux",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 3,
        "total_score": 8,
        "tags": [
            "ls",
            "-a",
            "-A",
            "隐藏文件"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "基础命令 · A 组 认命令",
        "statement_md": "`ls -a` 和 `ls -A` 的输出完全一样，都能列出隐藏文件。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "错",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|错\n|错误\n|×\n|F\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**错**。差在最前面那两行：\n\n| 选项 | 含义 | 是否含 `.` 和 `..` |\n|---|---|---|\n| `-a` | all | **含** |\n| `-A` | almost all | **不含** |\n\n`.` 是当前目录、`..` 是上级目录，它俩永远存在、不是「隐藏文件」。\n所以在脚本里遍历目录时用 `-A`，能省掉手动过滤 `.` 和 `..` 的麻烦。"
            }
        ]
    },
    {
        "title": "复制目录并保留符号链接与权限时间",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "cp",
            "-a",
            "权限",
            "备份"
        ],
        "choices": [
            "cp -r ~/docs /backup/",
            "cp -a ~/docs /backup/",
            "cp -p ~/docs /backup/",
            "cp -f ~/docs /backup/"
        ],
        "source_section": "基础命令 · A 组 认命令",
        "statement_md": "把 `~/docs` 整个目录复制到备份盘，要求**保留权限、属主、时间戳，并且符号链接原样照搬**。用哪个？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`cp -a`** —— 归档模式，等价于 `-dR --preserve=all`：\n递归 + 符号链接原样 + 权限/属主/时间全保留。\n\n其余三个为什么不够：\n- `-r` 只递归，**权限按 umask 重算**（私钥会从 600 变 644，就是这条坑）\n- `-p` 保留属性，但**不保证递归**（要写 `-rp` 一起）\n- `-f` 是「强制覆盖」，跟保留属性没关系\n\n★ 备份 `~/.ssh` 时尤其要用 `-a` —— 用 `-r` 备份出来的私钥权限太开放，ssh 会**拒绝使用**它。"
            }
        ]
    },
    {
        "title": "rm -rf 删掉的文件能从回收站找回吗",
        "subject": "linux",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 2,
        "total_score": 8,
        "tags": [
            "rm",
            "回收站",
            "安全",
            "高频错点"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "基础命令 · A 组 认命令",
        "statement_md": "在终端里用 `rm -rf` 删掉的文件，可以从「回收站」里找回来。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "错",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|错\n|错误\n|×\n|F\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**错**，而且是本讲最危险的一条。\n\n命令行的 `rm` **没有回收站**。图形界面能「从回收站还原」，那是**文件管理器自己实现的功能**（它把文件挪到 `~/.local/share/Trash`），和 `rm` 是两套完全独立的东西。\n\n安全习惯三条：\n1. 删之前先 `ls` 看清单\n2. 用通配符时先 `echo rm -rf *` 让它**只打印展开结果**，确认无误再删\n3. 需要可回滚就 `mv` 到 `~/trash` 目录，别直接 rm\n\n★ 铁律：**永远不要**在 `/` 或 `~` 下敲 `rm -rf *`（中间那个空格是致命的）。"
            }
        ]
    },
    {
        "title": "tail -n +5 输出什么",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "tail",
            "+N",
            "取行"
        ],
        "choices": [
            "最后 5 行",
            "前 5 行",
            "从第 5 行到文件末尾",
            "除最后 5 行外的全部"
        ],
        "source_section": "基础命令 · A 组 认命令",
        "statement_md": "文件 `a.txt` 有 20 行，`tail -n +5 a.txt` 输出什么？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "C",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|C\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**从第 5 行一路输出到末尾**（第 5~20 行，共 16 行）。\n\n`+N` 的含义是「**从第 N 行开始**数」，不是「取 N 行」。\n\n对照记忆：\n| 写法 | 含义 |\n|---|---|\n| `tail -n 5 f` | 最后 5 行 |\n| `tail -n +5 f` | 从第 5 行到末尾 |\n| `head -n 5 f` | 前 5 行 |\n| `head -n -5 f` | 去掉最后 5 行 |\n\n真机上验证：`seq 1 20 > a.txt && tail -n +5 a.txt | head -1` 会打出 `5`。"
            }
        ]
    },
    {
        "title": "head -n -3 是语法错误吗",
        "subject": "linux",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 3,
        "total_score": 8,
        "tags": [
            "head",
            "负数",
            "易混"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "基础命令 · A 组 认命令",
        "statement_md": "`head -n -3 f` 是非法的写法，head 不接受负数。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "错",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|错\n|错误\n|×\n|F\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**错**，它是合法的。\n\n`head -n -3 f` 表示「**去掉最后 3 行**，把其余的全部输出」。`-` 在这里是「从末尾砍掉」的意思。\n\n真正非法的是 `head -n +3 f` —— **head 不认 `+`**，会报 `invalid number of lines: '+3'`。\n\n★ 口诀：**`+` 归 tail，`-` 归 head**。\n（反过来说，`tail -n -5 f` 也是非法的 —— tail 的 `-n` 只认数字或 `+数字`。）"
            }
        ]
    },
    {
        "title": "tar -zcvf 里的 z 是什么",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "tar",
            "gzip",
            "压缩格式"
        ],
        "choices": [
            "compress（.Z 老格式）",
            "gzip",
            "zip",
            "zstd"
        ],
        "source_section": "基础命令 · A 组 认命令",
        "statement_md": "`tar -zcvf a.tar.gz dir/` 里的 `z` 表示什么？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "小写 **`-z` = gzip**。\n\n顺带把四个压缩选项一次分清：\n\n| 选项 | 压缩器 | 典型后缀 |\n|---|---|---|\n| `-z` | gzip | `.tar.gz` / `.tgz` |\n| `-j` | bzip2 | `.tar.bz2` / `.tbz2` |\n| `-Z` | compress | `.tar.Z`（老古董） |\n| `-J` | xz | `.tar.xz` |\n\n`zip` 是另一个**独立命令**（`zip -r a.zip dir/`），不是 tar 的选项。"
            }
        ]
    },
    {
        "title": "touch 已存在的文件会清空内容吗",
        "subject": "linux",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 2,
        "total_score": 8,
        "tags": [
            "touch",
            "时间戳",
            "清空",
            "易混"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "基础命令 · A 组 认命令",
        "statement_md": "对一个已经存在且有内容的文件执行 `touch`，会把它的内容清空。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "错",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|错\n|错误\n|×\n|F\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**错**。`touch` 只改**时间戳**（访问时间 atime / 修改时间 mtime），文件内容一个字都不会动。\n\n`touch` 的两个用途：\n1. 文件**不存在**时新建一个空文件\n2. 文件**已存在**时把时间更新成现在（常用在 make 里强制重新编译）\n\n真想清空内容，用**重定向**：`> 文件名`（注意前面**没有命令**）。\n验证：`echo hi > a.txt && touch a.txt && cat a.txt` —— 还是打出 `hi`。\n\n★ 这是典型的「想当然」错点：名字叫 touch（触碰），确实就是「碰一下改个时间」，仅此而已。"
            }
        ]
    },
    {
        "title": "mkdir -p 里的 p 是什么",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "mkdir",
            "-p",
            "多级目录"
        ],
        "choices": [
            "permission（指定权限）",
            "protect（保护，存在就不覆盖）",
            "parents（缺失的父目录一并创建）",
            "print（打印创建了哪些）"
        ],
        "source_section": "基础命令 · A 组 认命令",
        "statement_md": "`mkdir -p a/b/c` 里的 `-p` 表示什么？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "C",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|C\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`-p` = parents**，把缺失的父目录**一路补建**出来。\n\n`mkdir a/b/c` 在 `a` 不存在时会直接报错：\n`mkdir: cannot create directory 'a/b/c': No such file or directory`\n\n加 `-p` 之后，`a`、`a/b`、`a/b/c` 三层一次建出来，而且**目标已存在也不报错**（幂等）—— 所以脚本里写 `mkdir -p` 最省心。\n\n指定权限是 **`-m`**：`mkdir -m 700 secret`。"
            }
        ]
    },
    {
        "title": "tar xf 不写 z 会解压失败吗",
        "subject": "linux",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 4,
        "total_score": 8,
        "tags": [
            "tar",
            "自动识别",
            "解压"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "基础命令 · A 组 认命令",
        "statement_md": "`tar xf a.tar.gz`（不写 `z`）会解压失败，必须写成 `tar xzf a.tar.gz`。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "错",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|错\n|错误\n|×\n|F\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**错**。**现代 GNU tar 读归档时会自动识别压缩格式**，所以 `tar xf a.tar.gz` 能正常解压（GNU tar 官方手册原话：读压缩包不需要额外选项，tar 会自动检测）。\n\n★ 但要分清**读**和**写**：\n- **解压**可以省：`tar xf a.tar.gz` ✅ 自动识别\n- **打包不行**：`tar cf a.tar.gz dir/` 会打出一个**不压缩**的 tar （白白顶着 `.gz` 后缀），必须写明 `-z`\n\n因为创建时要**决定调用哪个压缩程序**，tar 猜不出来。\n\n（`xz`/`bzip2` 同理：解压可省，打包要写。）"
            }
        ]
    },
    {
        "title": "只看 zip 包里有什么，不解压",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "unzip",
            "zip",
            "查看内容"
        ],
        "choices": [
            "unzip a.zip",
            "unzip -l a.zip",
            "unzip -d a.zip",
            "zip -l a.zip"
        ],
        "source_section": "基础命令 · A 组 认命令",
        "statement_md": "你想先看看 `a.zip` 里装了哪些文件，**不想真的解压**。用哪条命令？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`unzip -l a.zip`**（`-l` = list）—— 只列出内容清单。\n\n其余三个为什么不对：\n- `unzip a.zip` 会**真的解压**到当前目录\n- `unzip -d a.zip` 的 `-d` 后面跟的是「**解压到哪个目录**」，把 `a.zip` 当目录名用，语义全错\n- `zip -l a.zip` 是**压缩**命令 `zip`，不是解压命令 `unzip`\n\ntar 那边对应的写法是 `tar -tzvf bak.tar.gz`（`t` = list，只看不解）。"
            }
        ]
    },
    {
        "title": "less 比 more 强在哪",
        "subject": "linux",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 1,
        "total_score": 8,
        "tags": [
            "less",
            "more",
            "分页器"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "基础命令 · A 组 认命令",
        "statement_md": "`less` 可以往回翻页，`more` 不能。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "对",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|对\n|正确\n|√\n|T\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**对**。这正是 `less` 存在的理由 —— 名字就是个冷幽默：「less is more」。\n\n| | more | less |\n|---|---|---|\n| 向下翻页 | 空格 / Enter | 空格 / PgDn |\n| **向上翻页** | ❌ 不行 | ✅ ↑ / PgUp / b |\n| 搜索 | ❌ | ✅ `/关键词`，`n` 下一个 |\n| 退出后是否清屏 | 不清 | **清屏** ★ |\n\n★ 最后一行是实验报告里最容易吃亏的点：`less` 退出（按 `q`）会把整屏清掉，所以**必须先截图再退出**。\n\n两个命令 Fedora 44 上都是默认装好的（`more` 由 util-linux-core 提供）。"
            }
        ]
    },
    {
        "title": "删掉符号链接会删掉真实目录吗",
        "subject": "linux",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 3,
        "total_score": 8,
        "tags": [
            "ln",
            "符号链接",
            "rm",
            "安全"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "基础命令 · A 组 认命令",
        "statement_md": "用 `rm /myshare` 删掉一个指向目录的符号链接，那个真实目录也会被删掉。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "错",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|错\n|错误\n|×\n|F\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**错**。符号链接相当于 Windows 的快捷方式 —— 它只是一个存着目标路径的**小文件**，删掉它**不会碰到**真实目录。\n\n★ 但有个**末尾斜杠**的陷阱必须记住：\n```bash\nrm /myshare        # ✅ 删链接本身\nrm -r /myshare/    # ❌ 末尾那个斜杠会让内核「解引用」链接，\n                   #    真的去删目标目录里的东西！\n```\n所以删符号链接时**末尾不要带斜杠**，也**不要加 `-r`**。\n\n怎么一眼认出符号链接：`ls -l` 输出的**第一个字符是 `l`**，并且中间有 `-> 目标路径`：\n```\nlrwxrwxrwx. 1 root root 20 10月 12 08:0x myshare -> /usr/local/sdutshare\n```"
            }
        ]
    },
    {
        "title": "/etc/shells 是什么",
        "subject": "linux",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 2,
        "total_score": 8,
        "tags": [
            "shells",
            "chsh",
            "shell"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "基础命令 · A 组 认命令",
        "statement_md": "`/etc/shells` 文件登记的是系统上「合法的登录 shell」白名单。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "对",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|对\n|正确\n|√\n|T\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**对**。`/etc/shells` 是系统认可的**合法登录 shell 白名单**，一行一个绝对路径。\n\nFedora 44 上通常长这样：\n```\n/bin/sh\n/bin/bash\n/usr/bin/sh\n/usr/bin/bash\n```\n（装了 zsh / tmux 之类才会多出对应的行。）\n\n**谁在用它**：`chsh` 改默认 shell 时会**到这里查** —— 你想把 shell 改成 `/usr/local/bin/myshell`，必须先把这行加进 `/etc/shells`，否则会被拒绝。\n\n**怎么列**：`cat /etc/shells`，或者 `chsh -l`（效果一样）。"
            }
        ]
    },
    {
        "title": "用相对路径切到子目录，`cd share` 与 `cd ../share` 等价吗",
        "subject": "linux",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 3,
        "total_score": 8,
        "tags": [
            "cd",
            "相对路径",
            "pwd",
            "易混"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "基础命令 · A 组 认命令",
        "statement_md": "当前在 `/usr/local`，`cd share` 和 `cd ../share` 会到达同一个目录。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "错",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|错\n|错误\n|×\n|F\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**错**。这是「相对路径」最阴的一个坑，因为**两条命令都不会报错**：\n\n| 命令 | 到达 | 说明 |\n|---|---|---|\n| `cd share` | `/usr/local/share` | ✅ 子目录 |\n| `cd ../share` | `/usr/share` | ❌ 上级目录下的 share |\n\n而 `/usr/share` 在真实系统上**确实存在**（一大堆文档、man 手册都放那）——所以 `cd ../share` 不会报 `No such file`，它会**安安静静地把你带到错的地方**。\n\n★ 防御习惯：**切完目录顺手 `pwd`**。\n实验报告里带上 `pwd` 输出，既证明路径对，又方便老师核对。"
            }
        ]
    },
    {
        "title": "一步回到上一个目录",
        "subject": "linux",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "cd",
            "OLDPWD"
        ],
        "choices": [],
        "source_section": "基础命令 · B 组 写命令",
        "statement_md": "你现在的提示符在某处，先执行了 `cd /etc`，现在想**用一条命令**回到进 `/etc` 之前的位置。写出这条命令。\n\n提示：用的是 shell 记录历史的那个变量，只要两个字符。",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "cd -",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|cd -\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`cd -`**。它读环境变量 **`$OLDPWD`** —— shell 每次切换目录前，都会把「原来在哪」记到这里。\n\n两个附带效果：\n1. 切换完会把目标路径**打印出来**（所以你能一眼确认跳对没有）\n2. 再执行一次 `cd -` 会**跳回去**（两个目录之间来回横跳）\n\n真机验证：\n```bash\ncd /tmp; cd /etc; cd -     # 打出 /tmp，并回到 /tmp\necho $OLDPWD               # /etc\n```"
            }
        ]
    },
    {
        "title": "列出目录下所有条目（含隐藏）的长格式",
        "subject": "linux",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "ls",
            "-l",
            "-a"
        ],
        "choices": [],
        "source_section": "基础命令 · B 组 写命令",
        "statement_md": "用 `ls` 列出 `/etc` 下所有条目（**包括隐藏文件**）的详细长格式。\n\n提示：两个短选项组合，长格式 + 全部。",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ls -la /etc",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ls -la /etc\n|ls -al /etc\n|ls -lah /etc\n|ls -alh /etc\n|ls -lA /etc\n|ls -Al /etc\n|ls -l -a /etc\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`ls -la /etc`**（或 `ls -al /etc`，两个选项顺序无所谓）。\n\n- `-l` = long，详细格式（权限 / 链接数 / 属主 / 属组 / 大小 / 时间 / 名字）\n- `-a` = all，含隐藏文件\n\n三种常见变体都是对的，判题时都认：\n- `ls -lah /etc` —— 多一个 `-h`，把大小显示成 `4.0K` 这种人类可读格式\n- `ls -lA /etc` —— 用 `-A` 替 `-a`，**不列 `.` 和 `..` 那两行**\n- `ls -l -a /etc` —— 选项分开写\n\n★ 本平台的命令题按「宽容口径」判：空白多少、`-l -a` 还是 `-la`、`-la` 还是 `-al`，都算对。"
            }
        ]
    },
    {
        "title": "复制目录并保留权限与时间戳",
        "subject": "linux",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 3,
        "total_score": 12,
        "tags": [
            "cp",
            "-a",
            "归档模式"
        ],
        "choices": [],
        "source_section": "基础命令 · B 组 写命令",
        "statement_md": "把 `~/docs` 整个目录复制到 `/tmp/` 下，要求**保留权限、属主和时间戳**。写出这条命令。\n\n提示：一个选项就能全搞定，首字母是「归档」的那个。",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "cp -a ~/docs /tmp/",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|cp -a ~/docs /tmp/\n|cp -a ~/docs /tmp\n|cp -rp ~/docs /tmp/\n|cp -a /home/lijihao/docs /tmp/\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`cp -a ~/docs /tmp/`**。\n\n`-a` = 归档模式（archive），等价于 `-dR --preserve=all`，一次满足全部要求：\n- `-R` 递归\n- `-d` 符号链接原样复制（不跟随）\n- `--preserve=all` 保留权限、属主、时间戳、扩展属性\n\n**`cp -rp ~/docs /tmp/`** 也常被接受（递归 + 保留属性），差别只在 `-r` 会**跟随符号链接**而不是照搬。\n\n★ 反面教材：裸 `cp ~/docs /tmp/` 会报 `cp: -r not specified; omitting directory` —— **什么都不复制**，但它**不报错退出**（退出码是 1，但只打印一句警告），很容易以为成功了。"
            }
        ]
    },
    {
        "title": "只看目录本身的一行信息",
        "subject": "linux",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "ls",
            "-d"
        ],
        "choices": [],
        "source_section": "基础命令 · B 组 写命令",
        "statement_md": "只想看 `/etc` **目录自己**（不是它里面的内容）的信息，输出一行。写出命令。\n\n提示：加一个「别展开目录」的选项。",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ls -ld /etc",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ls -ld /etc\n|ls -dl /etc\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`ls -ld /etc`**。\n\n关键是 **`-d`**：它告诉 ls「遇到目录**不要展开**，只报这个目录本身」。\n\n对照：\n```bash\nls -l /etc      # 几十行，全是 /etc 里面的东西\nls -ld /etc     # 一行：drwxr-xr-x. 1 root root 8192 Oct 12 09:00 /etc\n```\n\n★ 这个要求还有个常见用法：`ls -d */` 只列当前目录下的**子目录**（`*/` 是通配符，先被 shell 展开成各子目录名）。"
            }
        ]
    },
    {
        "title": "取文件的前 50 行",
        "subject": "linux",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "head",
            "-n"
        ],
        "choices": [],
        "source_section": "基础命令 · B 组 写命令",
        "statement_md": "取 `a.log` 的前 50 行。写出这条命令（用现代写法）。\n\n提示：head + -n + 数字 + 文件名。",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "head -n 50 a.log",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|head -n 50 a.log\n|head -50 a.log\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`head -n 50 a.log`**。\n\n`-n` 后面跟行数，**不写 `-n` 时 head 默认取前 10 行**。\n\n老式写法 `head -50 a.log` 也能用（数字紧跟选项），但 coreutils 手册把它归为**过时写法**，建议统一用 `-n 50`。\n\n★ 前 50 行 vs 后 50 行：\n- 前 50 → `head -n 50`\n- 后 50 → `tail -n 50`（**不加 `+`**！）\n\n真机验证：`seq 1 100 > a.log && head -n 50 a.log | tail -1` 打出 `50`。"
            }
        ]
    },
    {
        "title": "取从第 100 行到末尾",
        "subject": "linux",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 3,
        "total_score": 12,
        "tags": [
            "tail",
            "+N",
            "取行"
        ],
        "choices": [],
        "source_section": "基础命令 · B 组 写命令",
        "statement_md": "取 `a.log` 从第 100 行开始、一直到文件末尾的内容。写出这条命令。\n\n提示：从中间取到末尾，用的是 tail 的特殊写法（带加号）。",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "tail -n +100 a.log",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|tail -n +100 a.log\n|tail +100 a.log\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`tail -n +100 a.log`**。\n\n`+100` 的意思是「**从第 100 行开始数**」，不是「取 100 行」。\n\n★ 这里是最容易写错的地方 —— **必须用 tail，不能用 head**：\n```bash\ntail -n +100 a.log       # ✅ 第 100 行 → 末尾\nhead -n +100 a.log       # ❌ head: invalid number of lines: '+100'\n```\n\n等价写法（思路不同，结果一样）：\n```bash\nsed -n '100,$p' a.log    # $ 表示最后一行\nawk 'NR>=100' a.log\n```"
            }
        ]
    },
    {
        "title": "取除最后 10 行外的全部内容",
        "subject": "linux",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 3,
        "total_score": 12,
        "tags": [
            "head",
            "负数",
            "取行"
        ],
        "choices": [],
        "source_section": "基础命令 · B 组 写命令",
        "statement_md": "取 `a.log` 中**除最后 10 行之外**的所有行。写出这条命令。\n\n提示：和「从第 N 行开始」正好相反 —— 这次 `-` 号归 head 用。",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "head -n -10 a.log",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|head -n -10 a.log\n|head -10 a.log\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`head -n -10 a.log`**。\n\n`-10` 表示「**从末尾砍掉 10 行**」，剩下的全输出。\n\n★ 这里正是和上一题**对称**的机关：\n| 想要什么 | 写法 | 谁的特权 |\n|---|---|---|\n| 从第 N 行到末尾 | `tail -n +N` | `+` 是 tail 的 |\n| 去掉最后 N 行 | `head -n -N` | `-` 是 head 的 |\n\n反过来写都会报 `invalid number`：`head -n +N` ❌、`tail -n -N` ❌。\n\n等价写法：`sed '$-10,$d'` 不太好写，实际工作中 `head -n -10` 最省事。"
            }
        ]
    },
    {
        "title": "打包并 gzip 压缩",
        "subject": "linux",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "tar",
            "gzip",
            "打包"
        ],
        "choices": [],
        "source_section": "基础命令 · B 组 写命令",
        "statement_md": "把 `~/project` 目录打包并用 gzip 压缩，生成 `project.tar.gz`。写出这条命令（**不需要**显示处理过程）。\n\n提示：tar + 创建 + gzip + 指定文件名。",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "tar -czf project.tar.gz ~/project",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|tar -czf project.tar.gz ~/project\n|tar -czf project.tar.gz /home/lijihao/project\n|tar czf project.tar.gz ~/project\n|tar -zcf project.tar.gz ~/project\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`tar -czf project.tar.gz ~/project`**。\n\n四个字母各管一摊：\n| 字母 | 作用 |\n|---|---|\n| `-c` | create，创建归档 |\n| `-z` | 走 gzip 压缩（**小写！大写 `-Z` 是 compress**） |\n| `-v` | verbose，显示处理过程（本题不需要，所以省掉） |\n| `-f` | file，**后面紧跟归档文件名** |\n\n★ `-f` 必须是**最后一个**（或者说它的参数必须紧跟其后）：\n`tar -czf project.tar.gz ~/project` ✅\n`tar -cfz project.tar.gz ~/project` ❌ —— 会把 `z` 当成归档文件名。\n\n口诀：**`czvf` 打包、`xzvf` 解包、`tzvf` 看内容**。"
            }
        ]
    },
    {
        "title": "查看压缩包里有哪些文件",
        "subject": "linux",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "tar",
            "-t",
            "查看归档"
        ],
        "choices": [],
        "source_section": "基础命令 · B 组 写命令",
        "statement_md": "查看 `bak.tar.gz` 里包含哪些文件，**但不要解压**。写出这条命令。\n\n提示：tar + 一个表示「列出」的选项。",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "tar -tzvf bak.tar.gz",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|tar -tzvf bak.tar.gz\n|tar -tzf bak.tar.gz\n|tar tzf bak.tar.gz\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`tar -tzvf bak.tar.gz`**（`t` = list）。\n\n三个字母的分工：`-t` 列出内容、`-z` 让 tar 先解 gzip、`-v` 显示详细信息（权限/属主/大小/时间）。\n\n嫌 `-v` 太啰嗦就省掉：`tar -tzf bak.tar.gz` 只打文件名。\n\n★ 它的价值：**解压前先看一眼包里是什么**。\n很多压缩包解出来是 `pkg/pkg/...` 这种双层嵌套 —— 先 `-t` 看一眼，就知道该不该加 `--strip-components=1`。\n\n（z 其实也可以省：现代 GNU tar 读归档时会自动识别压缩格式，但显式写出来更好读。）"
            }
        ]
    },
    {
        "title": "把压缩包解压到指定目录",
        "subject": "linux",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 4,
        "total_score": 15,
        "tags": [
            "tar",
            "-C",
            "解压",
            "目录"
        ],
        "choices": [],
        "source_section": "基础命令 · B 组 写命令",
        "statement_md": "把 `bak.tar.gz` 解压到 `/tmp/out` 目录下。写出完整的命令序列（`/tmp/out` **可能还不存在**）。\n\n提示：先建目录（可能要多级），再用 `-C` 指定解压目标。",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "mkdir -p /tmp/out && tar -xzvf bak.tar.gz -C /tmp/out",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|mkdir -p /tmp/out && tar -xzvf bak.tar.gz -C /tmp/out\n|mkdir -p /tmp/out; tar -xzvf bak.tar.gz -C /tmp/out\n|mkdir -p /tmp/out; tar -xzf bak.tar.gz -C /tmp/out\n|mkdir -p /tmp/out && tar -xzf bak.tar.gz -C /tmp/out\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "```bash\nmkdir -p /tmp/out\ntar -xzvf bak.tar.gz -C /tmp/out\n```\n\n★ **两个必须踩对的点**：\n\n**1. `-C` 指定的目录必须已存在** —— tar **不会**替你建。\n漏了 `mkdir` 会报 `tar: /tmp/out: Cannot open: No such file or directory`。\n\n**2. `-C` 要放在归档文件名之后**：\n```bash\ntar -xzvf bak.tar.gz -C /tmp/out     # ✅\ntar -xzvf bak.tar.gz -C /tmp/out    # -C 前面的 -f 已经吃掉包名了，这里顺序对\ntar -xzvf -C /tmp/out bak.tar.gz     # ❌ -f 后面跟的是 -C，tar 把 \"-C\" 当归档名\n```\n记法：**`-f` 后面永远紧跟包名，其他选项都排它后面**。\n\n顺带一提：`tar` 解压时会打一句 `Removing leading '/' from member names` —— **这是正常的**（防止把文件覆盖回绝对路径），不是错误。"
            }
        ]
    },
    {
        "title": "一次性创建多级目录",
        "subject": "linux",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "mkdir",
            "-p"
        ],
        "choices": [],
        "source_section": "基础命令 · B 组 写命令",
        "statement_md": "一次性创建多级目录 `data/2026/10/report`（中间几层都还不存在）。写出命令。\n\n提示：mkdir + 一个选项。",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "mkdir -p data/2026/10/report",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|mkdir -p data/2026/10/report\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`mkdir -p data/2026/10/report`**。\n\n`-p`（parents）会把缺失的 `data`、`data/2026`、`data/2026/10` 一并建出来。\n\n不加 `-p` 会直接报错：\n`mkdir: cannot create directory 'data/2026/10': No such file or directory`\n（`data` 都不存在，没法在它下面建 `2026`。）\n\n★ `-p` 还有个隐性好处：**目标已存在也不报错**，所以脚本开头写 `mkdir -p /var/tmp/x` 可以放心重复执行。"
            }
        ]
    },
    {
        "title": "一次建三个空文件",
        "subject": "linux",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "touch",
            "多文件",
            "花括号展开"
        ],
        "choices": [],
        "source_section": "基础命令 · B 组 写命令",
        "statement_md": "在 `/tmp` 下**用一条命令**创建三个空文件 `a.txt`、`b.txt`、`c.txt`。写出这条命令。\n\n提示：touch 可以一次接好几个文件名；bash 还支持花括号简写。",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "touch /tmp/a.txt /tmp/b.txt /tmp/c.txt",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|touch /tmp/a.txt /tmp/b.txt /tmp/c.txt\n|touch /tmp/{a,b,c}.txt\n|cd /tmp && touch a.txt b.txt c.txt\n|touch /tmp/a.txt; touch /tmp/b.txt; touch /tmp/c.txt\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "最直接的写法 —— **`touch` 接受多个文件名**：\n```bash\ntouch /tmp/a.txt /tmp/b.txt /tmp/c.txt\n```\n\n更短的**花括号展开**（bash 特性，shell 先展开再交给 touch）：\n```bash\ntouch /tmp/{a,b,c}.txt\n```\n展开规则：`{a,b,c}.txt` → `a.txt b.txt c.txt`。\n还能写区间：`{1..5}` → `1 2 3 4 5`、`{a..e}` → `a b c d e`。\n\n先切目录也行：`cd /tmp && touch a.txt b.txt c.txt`。\n\n★ 记住 `touch` 的两副面孔：文件**不存在就建**，**存在就只改时间戳**（不动内容）。"
            }
        ]
    },
    {
        "title": "用 gzip 压缩，哪条对",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "tar",
            "gzip",
            "找错"
        ],
        "choices": [
            "tar -Zcvf bak.tar.gz dir/",
            "tar -zcvf bak.tar.gz dir/",
            "tar -jcvf bak.tar.gz dir/",
            "tar -Jcvf bak.tar.gz dir/"
        ],
        "source_section": "基础命令 · C 组 找错",
        "statement_md": "下面四条都想「用 **gzip** 把 `dir/` 打包成 `bak.tar.gz`」，只有一条是对的。",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`tar -zcvf bak.tar.gz dir/`**（小写 `-z` = gzip）。\n\n另外三条错在哪：\n\n| 写法 | 实际行为 |\n|---|---|\n| `-Z` | 调用 **compress**（老 `.Z` 格式）。没装的机器直接报错，有的版本会兜底成 gzip —— 看着像成功，其实不符合预期 |\n| `-j` | 调用 **bzip2**，产出的是 `.tar.bz2` 格式，顶着 `.gz` 后缀名不符实 |\n| `-J` | 调用 **xz**，同上 |\n\n★ 一句话记牢：**z 小写 gzip、Z 大写 compress、j 是 bzip2、J 是 xz**。"
            }
        ]
    },
    {
        "title": "从第 100 行开始显示，哪条对",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "head",
            "tail",
            "找错",
            "取行"
        ],
        "choices": [
            "head -n +100 a.log",
            "head -n -100 a.log",
            "tail -n +100 a.log",
            "tail -n -100 a.log"
        ],
        "source_section": "基础命令 · C 组 找错",
        "statement_md": "下面四条都想「从 `a.log` 的**第 100 行**开始显示到末尾」，只有一条能跑通。",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "C",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|C\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`tail -n +100 a.log`**。\n\n另外三条都会报 `invalid number of lines`：\n\n| 写法 | 报错/行为 |\n|---|---|\n| `head -n +100` | ❌ head **不认 `+`**，报 `invalid number: '+100'` |\n| `head -n -100` | ⚠️ **合法但意思不同** —— 是「去掉最后 100 行」，不是「从第 100 行开始」 |\n| `tail -n -100` | ❌ tail 的 `-n` 只认数字或 `+数字`，不认负号 |\n\n★ **`+` 归 tail，`-` 归 head** —— 这八个字能挡掉这一族所有的错。"
            }
        ]
    },
    {
        "title": "想统计行数，哪条对",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "wc",
            "cat",
            "找错"
        ],
        "choices": [
            "cat -n a.log",
            "wc -l a.log",
            "tail -n a.log",
            "head -n a.log"
        ],
        "source_section": "基础命令 · C 组 找错",
        "statement_md": "你想知道 `a.log` 一共有多少行。下面哪条的命令**用途正确**？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`wc -l a.log`** —— 输出 `行数 文件名`，比如 `1024 a.log`。\n\n其余三条的问题：\n- `cat -n a.log` 是**给每行加行号后全打印出来**，不是统计 —— 大文件会刷几万行屏，慢且没用\n- `tail -n a.log` 语法不完整（`-n` 后面缺数字）\n- `head -n a.log` 同上\n\n★ 只想要数字（不要文件名）时：`wc -l < a.log`，或者 `cat a.log | wc -l`。\n\n补充：`wc` 还能数单词（`-w`）和字符（`-c`），不加选项三个都打。"
            }
        ]
    },
    {
        "title": "想删掉一个目录，哪条对",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "rm",
            "-rf",
            "找错",
            "安全"
        ],
        "choices": [
            "rm -rf /tmp/lab *",
            "rm -rf /tmp/lab",
            "rm /tmp/lab",
            "rm -r /tmp/lab *"
        ],
        "source_section": "基础命令 · C 组 找错",
        "statement_md": "你想删掉 `/tmp/lab` 这个目录，**不要**影响当前目录里的其他文件。下面哪条是对的？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`rm -rf /tmp/lab`** —— 只有一个目标，干净利落。\n\n★ 前两条为什么危险（这是本组最要命的一题）：\n\n```bash\nrm -rf /tmp/lab *\n                ↑ 这个空格让它变成两个参数\n```\n`*` 会被 shell 展开成**当前目录下的所有条目** —— 等于顺手把你当前所在的目录清空了，完全不是本意。\n\n第三条 `rm /tmp/lab` 也错：删目录**必须加 `-r`**，否则报 `rm: cannot remove '/tmp/lab': Is a directory`。\n\n**两条保命习惯**：\n1. 删之前先 `ls /tmp/lab` 看看里面有什么\n2. 用通配符时先 `echo rm -rf *` —— **只让它打印展开结果**，确认无误再去掉 echo"
            }
        ]
    },
    {
        "title": "备份 ssh 私钥，哪条对",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "cp",
            "-a",
            "ssh",
            "权限",
            "找错"
        ],
        "choices": [
            "cp -r ~/.ssh /tmp/ssh_backup",
            "cp -a ~/.ssh /tmp/ssh_backup",
            "cp ~/.ssh /tmp/ssh_backup",
            "mv ~/.ssh /tmp/ssh_backup"
        ],
        "source_section": "基础命令 · C 组 找错",
        "statement_md": "你要把 `~/.ssh` 备份到 `/tmp/ssh_backup`，备份出来**必须**还能被 ssh 直接用（私钥权限不能被改宽）。哪条对？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`cp -a ~/.ssh /tmp/ssh_backup`**。\n\n★ `-r` 的隐患（本题的机关）：它会**按 umask 重算权限**。`~/.ssh` 里的私钥本来是 `600`（只有属主可读写），用 `-r` 复制出来可能变成 `644`（同组和其他人可读）。\n\n后果：用这份备份恢复后，**ssh 会拒绝使用私钥**，报\n```\nPermissions 0644 for '/home/user/.ssh/id_rsa' are too open.\n```\n\n`-a`（归档模式）= 递归 + 保留权限/属主/时间 + 符号链接原样。\n\n另外两个：`cp`（不带选项）会报 `omitting directory` 什么都不干；`mv` 是**移动**不是复制 —— 源文件会消失，那就不是「备份」了。"
            }
        ]
    },
    {
        "title": "复制目录，哪条对",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "cp",
            "-r",
            "找错",
            "递归"
        ],
        "choices": [
            "cp ~/docs /tmp/",
            "cp -r ~/docs /tmp/",
            "cp -u ~/docs /tmp/",
            "cp -i ~/docs /tmp/"
        ],
        "source_section": "基础命令 · C 组 找错",
        "statement_md": "把 `~/docs` 整个目录复制到 `/tmp/` 下。下面哪条**真的会复制成功**？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`cp -r ~/docs /tmp/`** —— 复制目录**必须**加递归开关 （`-r`、`-R` 或 `-a`）。\n\n不加会得到：\n```\ncp: -r not specified; omitting directory '/home/lijihao/docs'\n```\n⚠️ **注意这是个「温柔的错误」**：它只打印一句警告、跳过这个目录，而不是报错崩掉 —— 在脚本里跑的话，你以为复制成功了，其实什么都没发生。\n\n另外两个选项：\n- `-u`（update）只在目标比源**旧**时才复制 —— 跟「能不能复制目录」无关\n- `-i`（interactive）覆盖前先问一句 —— 同理，不解决递归问题\n\n★ 更好的选择是 **`cp -a ~/docs /tmp/`**：递归 + 保留权限时间。"
            }
        ]
    },
    {
        "title": "解压到指定目录，哪条对",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "tar",
            "-C",
            "找错",
            "解压"
        ],
        "choices": [
            "tar -xzvf dir/ bak.tar.gz",
            "tar -xzvf bak.tar.gz -C dir/",
            "tar -xzvf bak.tar.gz dir/",
            "tar -xzvf -C bak.tar.gz dir/"
        ],
        "source_section": "基础命令 · C 组 找错",
        "statement_md": "把 `bak.tar.gz` 解压到 `dir/` 目录下。下面哪条对？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`tar -xzvf bak.tar.gz -C dir/`**。\n\n★ 每条错误写法的病因都是**同一个**：`-f` 后面必须紧跟归档文件名。\n\n| 写法 | 报错 |\n|---|---|\n| `-f dir/ bak.tar.gz` | tar 把 `dir/` 当成包名 → `tar: dir/: Cannot open: No such file or directory` |\n| `bak.tar.gz dir/`（用位置当 `-C`） | tar 把 `dir/` 当成「要解压的成员名」→ 报找不到成员 |\n| `-C bak.tar.gz dir/` | tar 把 `bak.tar.gz` 当成目录、把 `dir/` 当成员 |\n\n**一句话记牢**：`-f` 后面永远紧跟着那个压缩包的**文件名**，其他所有选项（包括 `-C`）都排在它后面。"
            }
        ]
    },
    {
        "title": "父目录不存在时建多级目录，哪条对",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "mkdir",
            "-p",
            "找错"
        ],
        "choices": [
            "mkdir data/2026/10",
            "mkdir -p data/2026/10",
            "mkdir -r data/2026/10",
            "mkdir -a data/2026/10"
        ],
        "source_section": "基础命令 · C 组 找错",
        "statement_md": "当前目录下**没有** `data`，你要建出 `data/2026/10`。哪条对？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`mkdir -p data/2026/10`**。\n\n不加 `-p` 的报错很直白：\n```\nmkdir: cannot create directory 'data/2026/10': No such file or directory\n```\n`data` 都不存在，怎么在它下面建 `2026` 呢？\n\n`-r` 和 `-a` 都**不是 mkdir 的选项**，会报 `invalid option`：\n- `-r`（recursive）是 `cp` / `rm` / `chmod` 的\n- `-a`（archive）是 `cp` / `ls` / `tar` 的\n\n★ 各命令的选项字母**不通用**，别凭感觉套。记 mkdir 就记 **`-p` = parents**。"
            }
        ]
    },
    {
        "title": "zip 压缩目录，哪条对",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "zip",
            "-r",
            "找错",
            "递归"
        ],
        "choices": [
            "zip doc.zip doc/",
            "zip -r doc.zip doc/",
            "zip -a doc.zip doc/",
            "zip -x doc.zip doc/"
        ],
        "source_section": "基础命令 · C 组 找错",
        "statement_md": "你要把一个**目录** `doc/` 连同里面的文件一起压缩成 `doc.zip`。哪条对？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`zip -r doc.zip doc/`**（`-r` = recursive）。\n\n★ 漏了 `-r` 的后果特别隐蔽：zip **不报错**，但只把 `doc/` 这个**目录条目本身**记进去，里面的文件一个都没有。\n解压出来就是一个空目录 —— 所以这题的经典症状是「**压完解开发现是空的**」。\n\n对照 tar：tar 打包目录**天然递归**（不用加 -r），而 zip 必须显式写 `-r`。这是两个工具最容易混的一处。\n\n另外两个：`-a` 是「把文本文件转成 ASCII 模式」（跟递归无关）；`-x` 是「排除某些文件」。\n\n顺带：`zip -q -r doc.zip doc/` 的 `-q` 是安静模式（不打印过程）。"
            }
        ]
    },
    {
        "title": "取最后 5 行，哪条对",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "tail",
            "找错",
            "取行"
        ],
        "choices": [
            "tail -n -5 a.log",
            "tail -n 5 a.log",
            "head -n -5 a.log",
            "head -n 5 a.log"
        ],
        "source_section": "基础命令 · C 组 找错",
        "statement_md": "取 `a.log` 的**最后 5 行**。下面哪条对？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`tail -n 5 a.log`** —— 不需要任何符号，tail 默认就**从末尾数**。\n\n| 写法 | 结果 |\n|---|---|\n| `tail -n 5` | ✅ 最后 5 行 |\n| `tail -n -5` | ❌ `invalid number of lines: '-5'` —— tail **不认负号** |\n| `head -n 5` | ⚠️ 合法，但拿到的是**前** 5 行 |\n| `head -n -5` | ⚠️ 合法，但意思是「**去掉最后 5 行**」 |\n\n★ 为什么 tail 不认负号？因为对 tail 来说，「取最后 N 行」是**默认行为**，负号是多余的；而「从第 N 行开始」才需要用 `+N` 特别说明。\n\n所以这一族的规律是：\n- **tail**：默认从末尾数，`+N` = 从第 N 行开始\n- **head**：默认从头数，`-N` = 砍掉末尾 N 行"
            }
        ]
    },
    {
        "title": "列出名字里含数字的文件，哪条对",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "ls",
            "通配符",
            "找错",
            "glob"
        ],
        "choices": [
            "ls [0-9]",
            "ls *[0-9]*",
            "ls [0-9]*",
            "ls ?[0-9]?"
        ],
        "source_section": "基础命令 · C 组 找错",
        "statement_md": "当前目录里有 `1`、`report2.txt`、`log2026`、`notes`。你要列出**名字里含数字**的全部条目。哪条对？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`ls *[0-9]*`** —— 匹配「名字**任意位置**含一个数字」。\n结果：`1`、`report2.txt`、`log2026`（`notes` 不含数字，不列）。\n\n逐条对比（假设目录里还有 `3abc.txt`、`7`）：\n\n| 写法 | 匹配到什么 | 说明 |\n|---|---|---|\n| `ls [0-9]` | 只有 `1`、`7` | ★ **名字恰好是一个数字字符** |\n| `ls *[0-9]*` | `1`、`report2.txt`、`log2026`、`3abc.txt`、`7` | ✅ 含数字 |\n| `ls [0-9]*` | `1`、`7`、`3abc.txt` | **以数字开头** |\n| `ls ?[0-9]?` | 名字**恰好 3 个字符**、中间是数字的 | 太窄 |\n\n★ 通配符三板斧：`*` 任意多个字符、`?` **恰好一个**字符、`[abc]` 字符集。\n题目问「含数字」多半要 `*[0-9]*`，而 `[0-9]` 单独用只匹配一个字符。"
            }
        ]
    },
    {
        "title": "用相对路径往上走两级",
        "subject": "linux",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "cd",
            "相对路径",
            "实验 2"
        ],
        "choices": [],
        "source_section": "实验 2 · 基本命令",
        "statement_md": "当前在 `/usr/local/bin`，要求**只用相对路径**切换到 `/usr`。写出这条命令。\n\n提示：往上两级，每一级两个点。",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "cd ../..",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|cd ../..\n|cd ../../\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`cd ../..`**。\n\n`..` 是「上一级目录」，连着写两次就是往上两级：\n`/usr/local/bin` → `/usr/local` → `/usr` —— 刚好。\n\n★ 写完顺手 `pwd` 确认。实验报告里带上 `pwd` 输出更清楚。\n\n顺便记住三种起点的区别：\n| 写法 | 从哪里算起 |\n|---|---|\n| `/usr/local/bin` | 绝对路径，从根 `/` 开始 |\n| `local/bin` | 相对路径，从**当前目录**开始 |\n| `../..` | 相对路径，从当前目录往**上**走 |\n\n还有几个简写：`~` 主目录、`.` 当前目录、`-` 上一个目录。"
            }
        ]
    },
    {
        "title": "查看系统支持哪些 shell 类型",
        "subject": "linux",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "shells",
            "shell",
            "实验 2"
        ],
        "choices": [],
        "source_section": "实验 2 · 基本命令",
        "statement_md": "查看**当前系统支持的 shell 类型**有哪些。写出这条命令。\n\n提示：这个清单是个文件，直接看它就行。",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "cat /etc/shells",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|cat /etc/shells\n|chsh -l\n|less /etc/shells\n|more /etc/shells\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`cat /etc/shells`**（或者 `chsh -l`，两者效果一样）。\n\n`/etc/shells` 存的是**合法登录 shell 的白名单**，一行一个绝对路径：\n```\n/bin/sh\n/bin/bash\n/usr/bin/sh\n/usr/bin/bash\n```\n\n★ 这个文件不只是给人看的 —— `chsh` 改默认 shell 时会**查它**。想换成自定义 shell 必须先加进这个文件。\n\n**别答错题目**：「系统支持哪些 shell 类型」问的是这份**清单**；「当前默认用的是哪个 shell」才是 `echo $SHELL`。"
            }
        ]
    },
    {
        "title": "查看当前默认使用的 shell",
        "subject": "linux",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "SHELL",
            "环境变量",
            "实验 2"
        ],
        "choices": [],
        "source_section": "实验 2 · 基本命令",
        "statement_md": "查看**终端当前默认使用**的 shell。写出这条命令。\n\n提示：SHELL 是个大写环境变量。",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "echo $SHELL",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|echo $SHELL\n|echo ${SHELL}\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`echo $SHELL`** —— Fedora Workstation 上打出 `/bin/bash`。\n\n★ 三个命令看着像，含义有细微差别，实验里可以三个一起截：\n\n| 命令 | 看的是 |\n|---|---|\n| `echo $SHELL` | **登录时登记的**默认 shell（一个环境变量） |\n| `echo $0` | **当前这个 shell 进程**的名字（交互式 bash 会显示 `-bash`） |\n| `ps -p $$ -o comm=` | 直接查当前 shell **进程名** → `bash` |\n\n`$$` 是当前 shell 的 PID（进程号）。"
            }
        ]
    },
    {
        "title": "su 后面那个减号到底管什么",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "su",
            "环境变量",
            "$HOME",
            "实验 2"
        ],
        "choices": [
            "su 然后 pwd",
            "su - 然后 pwd",
            "sudo pwd",
            "su root 然后 echo $HOME"
        ],
        "source_section": "实验 2 · 基本命令",
        "statement_md": "实验里要求「切到 root，**打印 root 主目录的绝对路径**」。\n\n下面哪条能拿到**正确**结果？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`su -`** —— 那个减号（等价于 `su - root` / `su -l`）是本题唯一的机关。\n\n| 命令 | 换身份 | 换环境 | `$HOME` | `pwd` 落点 |\n|---|---|---|---|---|\n| `su` | ✅ | ❌ | 还是 `/home/lijihao` | 还在原目录 |\n| **`su -`** | ✅ | ✅ **完整登录** | `/root` | `/root` |\n\n所以不带减号时，你虽然已经**是 root 了**，但 `$HOME` 还留着普通用户的值 ——打印出来的「root 主目录」是错的，而且**不会报任何错**。\n\n★ 另外两条也不行：`sudo pwd` 只是用 root 权限跑了一下 pwd，**没有切换身份**，还在原目录；`su root` 同样没带减号。\n\n**前提**：Fedora 安装时默认**不给 root 设密码**（用 sudo 代替）。真要用 `su -` 得先 `sudo passwd root` 设一个。"
            }
        ]
    },
    {
        "title": "把目录列表重定向到文件并带行号查看",
        "subject": "linux",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 3,
        "total_score": 12,
        "tags": [
            "重定向",
            "cat",
            "wc",
            "实验 2"
        ],
        "choices": [],
        "source_section": "实验 2 · 基本命令",
        "statement_md": "把 `/usr/local` 下的文件列表输出重定向到家目录的 `test1.txt`，然后用 `cat` 查看并**显示行号**。写出这两条命令（用 `&&` 或 `;` 连起来）。\n\n提示：一个重定向符号 + cat 的加行号选项。",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ls /usr/local > ~/test1.txt && cat -n ~/test1.txt",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ls /usr/local > ~/test1.txt && cat -n ~/test1.txt\n|ls /usr/local > ~/test1.txt; cat -n ~/test1.txt\n|ls /usr/local > /home/lijihao/test1.txt && cat -n /home/lijihao/test1.txt\n|ls /usr/local > ~/test1.txt && cat -n /home/lijihao/test1.txt\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "```bash\nls /usr/local > ~/test1.txt      # 覆盖重定向（会先清空原文件）\ncat -n ~/test1.txt               # -n 显示行号\n```\n\n★ 三个要点：\n\n**1. `>` 是覆盖，`>>` 是追加。** 用错 `>` 会把文件原有内容清空。\n（`>` 在命令执行**之前**就把文件截断了 —— 所以\n`cat a.txt > a.txt` 会得到**空文件**，因为 a.txt 先被清零了。）\n\n**2. `cat -n` 是「加行号输出」，不是「统计行数」。** 数行数用 `wc -l`。\n\n**3. 怎么验证自己做对了**：`cat -n` 输出的总行数应当等于`ls /usr/local | wc -l`，两个数对得上就没错。"
            }
        ]
    },
    {
        "title": "仅列出 /etc 下名字含 pass 的文件",
        "subject": "linux",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 3,
        "total_score": 12,
        "tags": [
            "ls",
            "-d",
            "通配符",
            "实验 2"
        ],
        "choices": [],
        "source_section": "实验 2 · 基本命令",
        "statement_md": "切换到 `/etc` 目录后，**仅显示名字里包含字符串 `pass` 的文件**。写出命令。\n\n提示：通配符匹配名字里含 pass，再加一个「别展开目录」的选项。",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ls -d *pass*",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ls -d *pass*\n|cd /etc && ls -d *pass*\n|ls /etc | grep pass\n|find /etc -maxdepth 1 -name '*pass*'\n|ls -d /etc/*pass*\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`ls -d *pass*`**（先 `cd /etc`）。\n\n两个部分各管一摊：\n- **`*pass*`** 是 shell 的通配符，匹配「名字里任意位置含 pass」→ `passwd`、`passwd-`\n- **`-d`** 让 ls「只报匹配项本身」—— 万一匹配到目录，不会把里面的内容也列出来\n\n三条等价写法（实验报告里可以一并截图）：\n```bash\nls -d *pass*                     # 当前就在 /etc 里\nls /etc | grep pass              # 管道给 grep 过滤\nfind /etc -maxdepth 1 -name '*pass*'   # 最通用\n```\n\n★ **为什么要先 `cd /etc`**：`*pass*` 是**相对于当前目录**展开的。人在 `/home` 里敲 `ls -d *pass*`，展开的是 `/home` 下的匹配项 —— 结果会是「没有那个文件」或者列错东西。"
            }
        ]
    },
    {
        "title": "把目录复制到 /usr 需要什么",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "cp",
            "sudo",
            "权限",
            "实验 3"
        ],
        "choices": [
            "cp -r /tmp/a1 /usr/",
            "sudo cp /tmp/a1 /usr/",
            "sudo cp -r /tmp/a1 /usr/",
            "cp -a /tmp/a1 /usr/"
        ],
        "source_section": "实验 3 · 常用命令",
        "statement_md": "把 `/tmp/a1`（含多级子目录）复制到 `/usr` 下。普通的 `cp /tmp/a1 /usr/` 会失败。下面哪条**能成功**？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "C",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|C\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`sudo cp -r /tmp/a1 /usr/`** —— 两个条件**缺一不可**。\n\n这道题的坑在于：**两个错误信息完全不同，得两个都补上**。\n\n| 少写了什么 | 报错 | 症状 |\n|---|---|---|\n| 少 `-r` | `cp: -r not specified; omitting directory '/tmp/a1'` | ⚠️ **不报错退出，只打一句警告**，什么都没复制 |\n| 少 `sudo` | `cp: cannot create directory '/usr/a1': Permission denied` | `/usr` 是系统目录，普通用户**只读** |\n\n★ 题目原文**没提 `sudo`** —— 但在 Fedora 上不加必然失败。「我知道要提权」这件事写进实验报告是加分项。\n\n（`cp -a` 也能替换 `-r`，但同样要加 `sudo`。）"
            }
        ]
    },
    {
        "title": "vi 里把内容存下来并退出",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "vi",
            "vim",
            "编辑器",
            "实验 3"
        ],
        "choices": [
            "Esc 然后 :q!",
            "Esc 然后 :wq",
            "直接 :wq",
            "Ctrl+S 然后 Ctrl+Q"
        ],
        "source_section": "实验 3 · 常用命令",
        "statement_md": "用 `vi ~/hello` 打开一个文件，按 `i` 输入了内容之后，**要保存并退出**，接下来敲什么？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**先 `Esc` 回到命令模式，再敲 `:wq` 回车。**\n\nvi / vim 是**模式编辑器**，这是它和记事本最大的区别：\n\n| 键 | 作用 |\n|---|---|\n| `i` | 进入**插入模式**，开始打字（左下角出现 `-- INSERT --`） |\n| **`Esc`** | 退回**命令模式**（`-- INSERT --` 消失） |\n| `:wq` | **w**rite + **q**uit，保存并退出 |\n| `:q!` | 不保存**强制**退出（改错了想重来用这个） |\n| `:w` | 只保存，继续编辑 |\n\n★ 为什么不能直接敲 `:wq`：在插入模式下，`:` 就是个**普通字符**，会被打进文件内容里 —— 结果文件里多出一行 `:wq`。\n\n截图验证：存完回到终端敲 `cat ~/hello`，看到内容就对了。"
            }
        ]
    },
    {
        "title": "mv 到底是「改名」还是「移进去」",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "mv",
            "改名",
            "移动",
            "实验 3"
        ],
        "choices": [
            "两条都是改名",
            "前者把 /test7 移进 /test8 目录，后者改名成 tmp",
            "前者改名为 /test8，后者移进 /tmp 目录",
            "两条都是移动"
        ],
        "source_section": "实验 3 · 常用命令",
        "statement_md": "`mv /test7 /test8` 和 `mv /test7 /tmp/` 这两条命令分别做了什么？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "C",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|C\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`mv` 的语义只有一句话：目标位置不存在就「改名」，存在且是目录就「移进去」。**\n\n| 命令 | `/test8`、`/tmp` 的状态 | 结果 |\n|---|---|---|\n| `mv /test7 /test8` | `/test8` **不存在** | 改名为 `/test8` ✅ |\n| `mv /test7 /tmp/` | `/tmp` **是已存在的目录** | 移成 `/tmp/test7` ✅ |\n\n★ 所以想**改名**时，目标路径必须指向一个**不存在**的名字。\n手滑写成 `mv /test7 /tmp/` 想改名 —— 结果只是搬进去了，名字没变。\n\n**配套的两个坑**：\n1. `/`、`/usr/local` 都是系统目录，**每一步都要 `sudo`**\n2. 一次搬多个文件时，**最后一个参数必须是目录**（带 `/`），否则报 `target 'xxx' is not a directory`"
            }
        ]
    },
    {
        "title": "把 /boot 下 vmlinuz 开头的文件拷到家目录",
        "subject": "linux",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 4,
        "total_score": 15,
        "tags": [
            "cp",
            "通配符",
            "mkdir",
            "实验 3"
        ],
        "choices": [],
        "source_section": "实验 3 · 常用命令",
        "statement_md": "把 `/boot` 下所有以 `vmlinuz` 开头的文件，拷贝到 `~/abc` 目录下（`abc` 不存在就先建）。写出这一串命令（用 `&&` 或 `;` 连起来）。\n\n提示：先建目录（用幂等的那版），再用通配符一次拷多个。",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "mkdir -p ~/abc && sudo cp /boot/vmlinuz* ~/abc/",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|mkdir -p ~/abc && sudo cp /boot/vmlinuz* ~/abc/\n|mkdir -p ~/abc; sudo cp /boot/vmlinuz* ~/abc/\n|mkdir -p ~/abc && cp /boot/vmlinuz* ~/abc/\n|mkdir -p ~/abc; cp /boot/vmlinuz* ~/abc/\n|mkdir -p /home/lijihao/abc && sudo cp /boot/vmlinuz* /home/lijihao/abc/\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "```bash\nls /boot/vmlinuz*          # ★ 先自证：这些文件真的存在\nmkdir -p ~/abc             # -p：已存在也不报错\nsudo cp /boot/vmlinuz* ~/abc/\n```\n\n★ 三个要点：\n\n**1. `mkdir -p` 而不是裸 `mkdir`** —— 目录已存在时裸 `mkdir` 会报错，`-p` 幂等，脚本里更稳。\n\n**2. 通配符先自证** —— 万一 `/boot` 下没有 `vmlinuz*`，shell 会把它**原样传给 cp**，报 `cp: cannot stat '/boot/vmlinuz*': No such file or directory`。看到这个错就知道是「根本没匹配上」，不是权限问题。\n\n**3. `cp` 支持一次拷多个** —— `*` 展开成若干文件名，通通扔进 `~/abc/`。（`/boot/vmlinuz-*` 通常是 `-rw-r--r--` 人人可读，普通用户其实也能拷；加 `sudo` 是求稳。）"
            }
        ]
    },
    {
        "title": "ll 在脚本里也能用吗",
        "subject": "linux",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 3,
        "total_score": 8,
        "tags": [
            "alias",
            "ll",
            "交互式",
            "实验 3"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "实验 3 · 常用命令",
        "statement_md": "`ll` 是 `ls -l` 的**别名**，所以写在 `.sh` 脚本里也能正常执行。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "错",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|错\n|错误\n|×\n|F\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**错**。`ll` **只在交互式 shell 里有效**。\n\n查明真相的三条命令：\n```bash\nalias ll            # alias ll='ls -l'\ntype ll             # ll 是 `ls -l` 的别名\ncommand -v ll       # 无输出 —— 系统里根本没有 ll 这个可执行文件\n```\n\n它是 Fedora 的 `/etc/profile.d/` 下的脚本在**每次启动交互式 shell 时**定义的。\n\n**什么时候会失效**：\n- 写在 `.sh` 脚本里 → `ll: command not found`\n- `sudo ll` → 同样报错（`sudo` 走自己那套，不认别名）\n- 放进 cron 定时任务 → 同样不行（非交互式环境）\n\n★ 那种场合请用**真命令 `ls -l`**。\n\n顺带：`alias` 定义的东西**可以覆盖真命令** —— 如果哪天发现`ls` 行为怪怪的，先 `type ls` 看一眼是不是被别名改了。"
            }
        ]
    },
    {
        "title": "tar 打包时那句 Removing leading / 警告",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "tar",
            "警告",
            "绝对路径",
            "实验 4"
        ],
        "choices": [
            "压缩失败了，要重来",
            "只是警告，压缩正常完成，包内路径是相对路径",
            "要加 -P 选项才能去掉这个警告",
            "说明 /usr/test5 不存在"
        ],
        "source_section": "实验 4 · 综合命令",
        "statement_md": "执行 `sudo tar czvf ~/test5.tar.gz /usr/test5` 时，屏幕上出现：\n\n```\ntar: Removing leading `/' from member names\n```\n\n这说明什么？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**这是 tar 的正常行为，不是错误** —— 压缩会正常完成。\n\ntar 会把成员名开头的 `/` **去掉**，也就是包内存的是 `usr/test5/...` 而不是 `/usr/test5/...`。\n\n**为什么要这么做**：防止你解压时把文件**直接覆盖回绝对路径**。\n想想看，如果包内记的是绝对路径，在别的机器上 `tar xf` 就可能直接改写对方系统的 `/usr` —— 这是很危险的行为。\n\n**怎么验证**：解压前后各看一眼，或者直接列包内路径：\n```bash\ntar tzf ~/test5.tar.gz | head -3\n# usr/test5/\n# usr/test5/xxx\n```\n★ 所以**解压位置由 `-C` 决定**，包内路径是相对的。\n\n（真想带绝对路径得显式加 `-P`，但**几乎不该这么做**。）"
            }
        ]
    },
    {
        "title": "ln -s 的两个参数谁在前",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "ln",
            "-s",
            "符号链接",
            "实验 4"
        ],
        "choices": [
            "ln -s /myshare /usr/local/sdutshare",
            "ln -s /usr/local/sdutshare /myshare",
            "ln /usr/local/sdutshare /myshare",
            "ln -s myshare /usr/local/sdutshare"
        ],
        "source_section": "实验 4 · 综合命令",
        "statement_md": "要在根目录建一个名为 `myshare` 的符号链接，指向 `/usr/local/sdutshare`。正确的命令是？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`ln -s 真实目标 链接名`** —— 顺序是「**先目标，后链接名**」。\n\n记法：跟 `cp 源 目标` 一个方向，`-s` 只是声明「建的是软链接」。\n\n★ **顺序写反的后果很严重**：\n```bash\nln -s /myshare /usr/local/sdutshare\n```\n这会建出一个**指向自己的死循环链接**（`/usr/local/sdutshare` 指向 `/myshare`，而 `/myshare` 又指向它）。\n\n**怎么一眼认出符号链接**：`ls -l` 输出**第一个字符是 `l`**：\n```\nlrwxrwxrwx. 1 root root 20 10月 12 08:0x myshare -> /usr/local/sdutshare\n```\n（普通文件是 `-`、目录是 `d`。）\n\n另外两条错在：`ln` 不带 `-s` 建的是**硬链接**（不能指向目录、也不能跨文件系统）；第四条把链接名写成了目标。"
            }
        ]
    },
    {
        "title": "按字典逆序排序文件内容",
        "subject": "linux",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "sort",
            "-r",
            "排序",
            "实验 4"
        ],
        "choices": [],
        "source_section": "实验 4 · 综合命令",
        "statement_md": "`~/mysort1` 里有四行：`is` / `this` / `excellent` / `my`。把它按**字典逆序**排序显示。写出这条命令。\n\n提示：sort 加一个表示「反过来」的选项。",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "sort -r ~/mysort1",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|sort -r ~/mysort1\n|sort -r /home/lijihao/mysort1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`sort -r ~/mysort1`**（`-r` = reverse）。\n\n输出：\n```\nthis\nmy\nis\nexcellent\n```\n\n对照（默认是字典**升序**，也就是 `-r` 的倒过来）：\n```\nexcellent\nis\nmy\nthis\n```\n\n★ 两个容易混的选项：\n- `sort -n` 是**按数值**排（`2` 排在 `10` 前面）—— 这题是纯字符串，用不上\n- `sort -k2` 是**按第 2 列**排\n\n注意字典序是**逐字符比 ASCII 码**，所以**大写字母全部排在小写字母前面**（`Z` = 90 < `a` = 97）。混大小写时 `sort` 的结果可能和直觉不一样。\n\n（`sort` **不改原文件**，只往屏幕输出。要写回用 `sort -r f > f.sorted`。）"
            }
        ]
    },
    {
        "title": "输出字符串但不换行",
        "subject": "linux",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "echo",
            "-n",
            "printf",
            "实验 4"
        ],
        "choices": [],
        "source_section": "实验 4 · 综合命令",
        "statement_md": "用 `echo` 输出字符串 `hello everyone!`，要求**输出后不换行**。写出命令。\n\n提示：echo 有个选项专门管「结尾不加换行」。",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "echo -n \"hello everyone!\"",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|echo -n \"hello everyone!\"\n|echo -n hello everyone!\n|printf \"hello everyone!\"\n|echo -e \"hello everyone!\\c\"\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`echo -n \"hello everyone!\"`**（`-n` = no newline）。\n\n三种写法都能做到：\n```bash\necho -n \"hello everyone!\"        # -n：结尾不加换行\necho -e \"hello everyone!\\c\"      # \\c：到此为止\nprintf \"hello everyone!\"         # printf 默认就不加换行（最标准）\n```\n\n★ **怎么自证「真的没换行」**（截图时这样截最有说服力）：\n```bash\necho -n \"hello everyone!\"; echo \"|\"\n# hello everyone!|\n#                ↑ 竖线紧贴着感叹号\n\necho \"hello everyone!\"; echo \"|\"      # 对照组\n# hello everyone!\n# |\n# ↑ 竖线跑到下一行了\n```\n\n顺带：内容里有空格**建议用引号括起来**。不括的话 `this is a` 会被拆成三个参数交给 echo —— 打印结果看着一样，但一旦内容里有 `*`、`>` 就会出事。"
            }
        ]
    },
    {
        "title": "man 手册的章节号",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "man",
            "章节",
            "文档",
            "实验 4"
        ],
        "choices": [
            "第 1 章",
            "第 5 章",
            "第 8 章",
            "第 9 章"
        ],
        "source_section": "实验 4 · 综合命令",
        "statement_md": "`man grep` 打开的是第 1 章。那么 **`/etc/passwd` 这种配置文件的说明**在第几章？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**第 5 章（文件格式与约定）** —— `man 5 passwd`。\n\nman 一共分 9 章，常用的四章：\n\n| 章 | 内容 | 例子 |\n|---|---|---|\n| **1** | 用户命令 | `man 1 grep` |\n| **2** | 系统调用 | `man 2 open` |\n| **3** | 库函数 | `man 3 printf` |\n| **5** | **配置文件格式** | `man 5 passwd`、`man 5 fstab` |\n| **8** | **系统管理命令**（多数要 root） | `man 8 mount` |\n\n★ **同名不同章**很常见：`passwd` 既是个命令（第 1 章）又是个文件（第 5 章）。直接 `man passwd` 默认给**章号最小**的那个 —— 想看文件格式就必须写明 `man 5 passwd`。\n\n两个配套技巧：\n- **`man -k 关键词`**（≈ `apropos`）搜「哪些手册页提到它」\n- **`grep --help`** 比 man 短，快速看选项"
            }
        ]
    },
    {
        "title": "在终端启动当前目录下的程序",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "PATH",
            "./",
            "可执行文件",
            "实验 4"
        ],
        "choices": [
            "eclipse",
            "./eclipse",
            "/eclipse",
            "sudo eclipse"
        ],
        "source_section": "实验 4 · 综合命令",
        "statement_md": "你把 Eclipse 解压到 `~/eclipse`，用 `cd ~/eclipse` 进去了。想启动里面的 `eclipse` 可执行文件，怎么写？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`./eclipse`** —— `./` 不能省。\n\n**为什么**：出于安全，Linux 的 shell **默认不搜索当前目录**（`PATH` 里**没有** `.`）。\n\n这个设计是有道理的：如果当前目录会被自动搜索，那么你 `cd` 进一个从网上下载的目录、敲了个 `ls`，就可能执行了攻击者放的同名恶意程序。\n\n**报错长这样**：\n```\neclipse: command not found\n```\n★ 看到 `command not found`，先想两件事：\n1. 这个程序**真的装了吗** → `dnf provides '*/eclipse'` 反查属于哪个包\n2. 是不是**就在当前目录**、但漏了 `./`\n\n另外两条：写 `/eclipse` 是在找**根目录下**的 eclipse（不存在）；`sudo eclipse` 同样过不了「不搜当前目录」这一关。\n\n顺带：解压时**别下错平台**，`linux-gtk-x86_64` 才是 Linux 版；首次启动要解压插件，等一两分钟是正常的。"
            }
        ]
    },
    {
        "title": "装 MySQL 到底装哪个包",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "dnf",
            "mysql",
            "服务",
            "实验 4"
        ],
        "choices": [
            "服务名写错了，应该是 mysql.service",
            "mysql 是客户端包，服务端在 mysql-server 里",
            "要先 systemctl daemon-reload",
            "MariaDB 把端口占了，得先停掉它"
        ],
        "source_section": "实验 4 · 综合命令",
        "statement_md": "实验要求「用 `dnf` 安装 mysql，然后启动它」。\n\n如果你直接敲 `sudo dnf install mysql`，装完之后 `sudo systemctl start mysqld` 会报 `Unit mysqld.service not found.`。为什么？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**Fedora 44 仓库里 `mysql` 和 `mysql-server` 是两个不同的包。**\n\n| 包名 | 内容 |\n|---|---|\n| `mysql` | **只有客户端**（`mysql` 命令 + 共享库），**没有服务端** |\n| `mysql-server` | **服务端**（`mysqld`、`mysqladmin`、systemd 服务单元） |\n\n装了客户端当然没有 `mysqld.service` —— 所以正确做法是装 **`mysql-server`**（它会自动把客户端也带上）。\n\n完整流程：\n```bash\nsudo dnf install -y mysql-server\nsudo systemctl start mysqld\nsudo grep 'temporary password' /var/log/mysqld.log   # 取初始 root 临时密码\nmysql -u root -p                                      # 粘进去\n```\n进去之后题目要的是：`show databases;`（能看到 `information_schema`、`mysql`、`performance_schema`、`sys` 四个库），然后 `exit;`。\n\n★ **另外三条**（真踩到时看）：\n- MySQL 与 MariaDB **冲突**（提供同名文件），一台机器只能装一个\n- 日志里找不到临时密码 → 可能是空密码初始化，直接 `sudo mysql -u root` 进去后马上改密码\n- 服务起不来先 `journalctl -u mysqld -n 50`，**别顺手 `setenforce 0`**"
            }
        ]
    },
    {
        "title": "把两个文件的内容拼进第三个文件",
        "subject": "linux",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 3,
        "total_score": 12,
        "tags": [
            "cat",
            "重定向",
            "mv",
            "实验 4"
        ],
        "choices": [],
        "source_section": "实验 4 · 综合命令",
        "statement_md": "`file11` 内容为 `sdut11`、`file12` 内容为 `sdut12`，`dir1` 目录已建好。把两者的内容依次写进 `dir1/file13`。写出命令。\n\n提示：cat 可以接多个文件，最后用重定向写进新文件。",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "cat file11 file12 > dir1/file13",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|cat file11 file12 > dir1/file13\n|cat ~/file11 ~/file12 > ~/dir1/file13\n|cat file11 file12 > ~/dir1/file13\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`cat file11 file12 > dir1/file13`**。\n\n`cat` 接**多个文件**时，会**按顺序**把所有内容连起来输出到标准输出；`>` 再把它写进新文件。结果 `file13` 是两行：\n```\nsdut11\nsdut12\n```\n\n★ **最容易踩的坑**：输出文件**不能是输入文件之一**。\n```bash\ncat file11 file12 > file11     # ❌ file11 先被清空，结果只剩 file12 的内容\n```\n因为 `>` 是在命令**执行之前**就把目标文件截断成 0 字节的 —— cat 去读 file11 时它已经空了。\n\n**另外两个配套操作**（实验题 (d) 问的那个）：\n```bash\nmv file11 file12 dir1/     # ★ 一次搬多个，最后一个参数必须是目录\nls -l ~/dir1               # 应该看到 file11 file12 file13\n```\n`mv` 一次搬多个时如果最后一个是文件名，会报 `target 'dir1' is not a directory`。"
            }
        ]
    },
    {
        "title": "反查一个命令属于哪个包",
        "subject": "linux",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 4,
        "total_score": 12,
        "tags": [
            "dnf",
            "provides",
            "排错",
            "实验 4"
        ],
        "choices": [],
        "source_section": "实验 4 · 综合命令",
        "statement_md": "你在 Fedora 上敲某个命令，报 `command not found`。想查「这个命令由哪个软件包提供」，用 `dnf` 的哪个子命令？（写出完整命令，命令名用 `ls` 举例即可）\n\n提示：dnf 的一个子命令，查「文件属于哪个包」；命令名前要加通配符路径。",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "dnf provides '*/ls'",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|dnf provides '*/ls'\n|dnf provides ls\n|dnf provides */ls\n|dnf provides '*/ls' -q\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`dnf provides '*/ls'`**（拿 `ls` 举例）。\n\n`command not found` 之后想「它到底属于哪个包」，这条是最靠谱的路 —— 因为它查的是**真实的文件归属关系**，不是猜。\n\n★ **为什么要写 `*/命令名` 这种带通配符的样子**：\n- `dnf provides ls` 会匹配**所有**名字里带 `ls` 的包（`alsa`、`lsblk` 一大堆噪音）\n- `dnf provides '*/ls'` 精确表示「**某个路径下名为 ls 的文件**」\n- 通配符**必须用单引号包起来**，否则 shell 会抢先展开它\n\n**为什么这条特别值得记**：本机实测过，很多时候**站内搜不到某工具**并不等于它不存在 —— 用 `dnf provides` 查文件归属才是权威答案。\n\n配套命令：\n```bash\nrpm -qf /usr/bin/ls          # 反过来：这个文件属于哪个已装的包\ndnf search 关键词            # 按描述搜包\ndnf repoquery -l 包名        # 看这个包里都有哪些文件\n```"
            }
        ]
    },
    {
        "title": "你敲一条命令，中间经过了什么",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "体系结构",
            "shell",
            "内核",
            "第 01 讲"
        ],
        "choices": [
            "内核 → Shell → ls 程序 → 终端",
            "Shell 解析并找到 ls → 内核 fork/exec → ls 运行 → 结果回终端",
            "ls 程序 → 内核 → Shell → 终端",
            "终端直接调用内核，Shell 只是显示界面"
        ],
        "source_section": "第 01 讲 · Linux 概述",
        "statement_md": "在终端敲下 `ls` 并回车，从你按下回车到看见输出，中间的顺序是？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "正确链路：\n```\n你敲 ls\n  → Shell(bash) 解析这行文字，去 PATH 里找到 /usr/bin/ls\n  → 调用内核的系统调用 fork() + execve()\n  → 内核调度 CPU 执行 ls 程序\n  → ls 通过内核读目录内容\n  → 结果返回 Shell → 打印到终端\n```\n\n★ **Shell 只是个普通程序**（跑在用户态），本身也能换（bash / zsh / fish）。它不干实事，只负责「解析 + 派活」。\n\n真正干活的是**内核**：进程调度、内存管理、设备驱动、网络，全在它手里。任何程序想碰硬件，都得**经过内核的系统调用**。"
            }
        ]
    },
    {
        "title": "Linux 的分层结构，Shell 在哪一层",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "体系结构",
            "shell",
            "第 01 讲"
        ],
        "choices": [
            "第 1 层，和内核并列",
            "第 2 层，和文件系统同层",
            "第 3 层，在文件系统之上、应用程序之下",
            "第 4 层，就是应用程序"
        ],
        "source_section": "第 01 讲 · Linux 概述",
        "statement_md": "教材把 Linux 系统从下往上分成四层。**Shell 位于哪一层**？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "C",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|C\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "四层结构（从下往上）：\n```\n4. 应用程序        浏览器 / 编辑器 / 你自己的程序\n3. Shell（命令解释器）  bash —— 你和内核之间的翻译\n2. 文件系统 + 用户界面   ext4 / btrfs；GNOME 桌面\n1. 内核 kernel      进程 / 内存 / 驱动 / 网络\n   ───────────────\n   硬件             CPU / 内存 / 磁盘 / 网卡\n```\n\nShell 在第 3 层，位置很关键：**它夹在「用户敲的东西」和「内核提供的服务」之间**。往上，它把命令翻译给内核；往下，它把内核的返回组织成你能看的形式。\n\n★ 记住这个位置，就能回答「为什么换个 shell 不影响系统」—— 因为它只是上面的一层皮，内核和文件系统都没动。"
            }
        ]
    },
    {
        "title": "哪个目录放配置文件",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "目录结构",
            "/etc",
            "第 01 讲"
        ],
        "choices": [
            "/bin",
            "/etc",
            "/var",
            "/lib"
        ],
        "source_section": "第 01 讲 · Linux 概述",
        "statement_md": "Linux 的**所有系统配置文件**（比如 `passwd`、`fstab`、`sshd_config`）统一放在哪个目录下？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`/etc`** —— 系统配置文件的集中地，记不住别的也得记住它。\n\n根目录下主要目录的职责：\n\n| 目录 | 装什么 |\n|---|---|\n| `/bin`、`/usr/bin` | 普通用户能用的命令（ls、cp……） |\n| `/sbin`、`/usr/sbin` | 管理员命令（fdisk、iptables……） |\n| **`/etc`** | **所有配置文件** |\n| `/home` | 普通用户的家目录 |\n| `/root` | root 的家目录（**不在 /home 下**） |\n| `/dev` | 设备文件（硬盘 sda、终端 tty……） |\n| `/proc` | 内存里的内核状态（虚拟文件系统，不占磁盘） |\n| `/var` | 变化的数据：日志、邮件、数据库 |\n| `/tmp` | 临时文件，重启可能清空 |\n\n★ 实验里凡是「改配置文件」的步骤，八成都在 `/etc` 下（`/etc/vsftpd/`、`/etc/httpd/`、`/etc/named.conf`……）。"
            }
        ]
    },
    {
        "title": "root 的家目录在哪",
        "subject": "linux",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 2,
        "total_score": 8,
        "tags": [
            "目录结构",
            "/root",
            "第 01 讲"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 01 讲 · Linux 概述",
        "statement_md": "root 用户的家目录是 `/home/root`，和其他普通用户放在一起。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "错",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|错\n|错误\n|×\n|F\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**错**。root 的家目录是 **`/root`** —— 直接挂在根目录下，**不在 `/home` 里**。\n\n为什么要分开：`/home` 在有些系统上会**单独挂一块盘**（或者被网络文件系统挂载）。如果 root 的家目录也在 `/home` 里，一旦那块盘出问题挂不上，root 就**没有家目录可落脚**了，连救援都难做。\n\n验证（实验 2 第 10 题正是考这个）：\n```bash\nsu -              # ★ 必须带减号，才会换 $HOME\necho $HOME        # /root\npwd               # /root\n```"
            }
        ]
    },
    {
        "title": "Linux 的文件系统是几棵树",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "文件系统",
            "根目录",
            "挂载",
            "第 01 讲"
        ],
        "choices": [
            "也是多个并列的盘符",
            "单根倒树，一切都在 / 之下",
            "按设备分树，每块盘一棵",
            "没有固定结构，看发行版"
        ],
        "source_section": "第 01 讲 · Linux 概述",
        "statement_md": "和 Windows 的 C: / D: / E: 相比，Linux 的文件系统结构特点是？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**单根倒树** —— 只有一个根 `/`，所有东西都挂在它下面。\n\n| | Windows | Linux |\n|---|---|---|\n| 顶层 | `C:` `D:` `E:` **多个并列** | `/` **只有一个** |\n| 新设备 | 自动分配一个盘符 | 必须**挂载**到某个目录下才能访问 |\n\n「挂载」的意思是：把一块盘（或一个分区、一个 U 盘）**接到现有目录树的某个位置**上。比如把 U 盘挂到 `/mnt/usb`，之后 `cd /mnt/usb` 就是进 U 盘。\n\n验证：`lsblk` 看块设备，`findmnt` 看谁挂在哪。在 `/etc/fstab` 里就能看到开机自动挂载的配置。"
            }
        ]
    },
    {
        "title": "X Window 是什么角色",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "XWindow",
            "GNOME",
            "分层",
            "第 03 讲"
        ],
        "choices": [
            "它就是 GNOME 桌面本身",
            "底层显示服务：管画面输出、键盘鼠标输入",
            "管文件管理的那部分",
            "管软件安装的那部分"
        ],
        "source_section": "第 03 讲 · X Window 的使用",
        "statement_md": "在 Linux 桌面里，**X Window 系统**负责的是哪一层？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**X Window 是最底层的显示服务**（`X Server` / Wayland 同层），负责：\n- 把画面**画到屏幕上**\n- 接收**键盘、鼠标**的输入并分发\n- 管理窗口的绘制区域\n\n而 **GNOME 是「桌面环境」** —— 它在 X 之上，提供任务栏、活动概览、文件管理器、设置面板等一整套东西。\n\n分层关系：\n```\nGNOME 桌面环境（任务栏、文件管理器、设置面板…）\n        ↓ 依赖\nX Window / Wayland（画图 + 输入）\n        ↓ 依赖\n内核（显卡驱动、输入设备驱动）\n```\n\n★ 所以可以「换桌面环境不换 X」：同一台机器上装 KDE、XFCE，都跑在同一个 X 之上，登录时切换即可。\n\n补充：`echo $XDG_SESSION_TYPE` 能看当前用的是 X11 还是 Wayland。"
            }
        ]
    },
    {
        "title": "自建的应用菜单项放哪里",
        "subject": "linux",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 3,
        "total_score": 8,
        "tags": [
            "desktop",
            "GNOME",
            "应用菜单",
            "第 03 讲"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 03 讲 · X Window 的使用",
        "statement_md": "想让自建的程序出现在 GNOME 的应用程序菜单里，可以往 `~/.local/share/applications/` 放一个 `.desktop` 文件。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "对",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|对\n|正确\n|√\n|T\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**对**。`.desktop` 文件就是应用的「菜单项定义」，有两个放的层次：\n\n| 位置 | 生效范围 |\n|---|---|\n| **`~/.local/share/applications/`** | 只对**当前用户**生效 |\n| `/usr/share/applications/` | **所有用户**（要 root 权限写） |\n\n最简模板：\n```ini\n[Desktop Entry]\nType=Application\nName=我的工具\nExec=/home/lijihao/tools/run.sh\nIcon=/home/lijihao/tools/icon.png\nTerminal=false\n```\n\n★ 三个容易卡住的点：\n1. **`Exec=` 要用绝对路径**（菜单启动时的 `PATH` 和你的终端不一样）\n2. 想让它在终端里跑就写 `Terminal=true`\n3. 写完可能**要重新登录**菜单才刷新（或者 `update-desktop-database`）\n\n权限别忘：`chmod +x` 那个 `.desktop` 文件并不必需，但 `Exec=` 指向的脚本**必须**可执行。"
            }
        ]
    },
    {
        "title": "LibreOffice 的三个主力组件",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "LibreOffice",
            "办公软件",
            "第 04 讲"
        ],
        "choices": [
            "Writer / Calc / Impress",
            "Word / Excel / PowerPoint",
            "Docs / Sheets / Slides",
            "Text / Grid / Show"
        ],
        "source_section": "第 04 讲 · 常用软件",
        "statement_md": "LibreOffice 里，**文档、表格、演示**分别对应哪三个组件？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "A",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|A\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**Writer（文档）/ Calc（表格）/ Impress（演示）**。\n\n和 MS Office 的对应关系：\n\n| LibreOffice | MS Office | 用途 | 文件格式 |\n|---|---|---|---|\n| **Writer** | Word | 文字文档 | `.odt` / `.docx` |\n| **Calc** | Excel | 电子表格 | `.ods` / `.xlsx` |\n| **Impress** | PowerPoint | 演示文稿 | `.odp` / `.pptx` |\n| Base | Access | 数据库 | `.odb` |\n| Draw | Visio | 矢量绘图 | `.odg` |\n\n★ B 选项 `Word/Excel/PowerPoint` 是**微软**的，C 选项是 **Google 文档**的 —— 别混。\n\n补充：LibreOffice 默认存 ODF 格式（`.odt` 等开放标准），存 Office 格式要去「另存为」里选，或者改默认格式设置。\n（第 04 讲有专门讲怎么办文档兼容。）"
            }
        ]
    },
    {
        "title": "Flatpak 装的软件能在 dnf 里看到吗",
        "subject": "linux",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 3,
        "total_score": 8,
        "tags": [
            "Flatpak",
            "dnf",
            "包管理",
            "第 04 讲"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 04 讲 · 常用软件",
        "statement_md": "用 Flatpak 安装的软件，可以用 `dnf list installed` 查到。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "错",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|错\n|错误\n|×\n|F\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**错**。Flatpak 和 RPM（dnf）是**两套完全独立的软件体系**。\n\n| | RPM / dnf | Flatpak |\n|---|---|---|\n| 来源 | Fedora 官方仓库 | Flathub 等 |\n| 查询 | `dnf list installed`、`rpm -qa` | **`flatpak list`** |\n| 安装 | `sudo dnf install xxx` | `flatpak install xxx` |\n| 沙箱 | 无（能访问全系统） | **有沙箱**，权限要单独授予 |\n| 依赖 | 系统共享库 | **自带运行时**（所以体积大） |\n\n★ 所以「装完 `dnf list installed` 里找不到」**不是没装上** —— 换 `flatpak list` 查就看到了。\n\n反过来说，用 dnf 装的软件也不会出现在 `flatpak list` 里。两套包管理器各管各的，互不知情。"
            }
        ]
    },
    {
        "title": "装本地 rpm 包的正确姿势",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "rpm",
            "dnf",
            "依赖",
            "第 05 讲"
        ],
        "choices": [
            "rpm -ivh x.rpm",
            "sudo rpm -ivh x.rpm",
            "sudo dnf install ./x.rpm",
            "sudo dnf localinstall ./x.rpm"
        ],
        "source_section": "第 05 讲 · 硬件与软件安装",
        "statement_md": "你下载了一个 `x.rpm` 到当前目录，它**有一堆依赖**需要一并装上。推荐用哪条命令？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "C",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|C\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`sudo dnf install ./x.rpm`** —— 让 dnf 经手，它会**自动把依赖装齐**。\n\n为什么不用 `rpm -ivh`：`rpm` **不管依赖**。缺了谁就直接报错退出，然后你就得手工一个个 `dnf install` 补 —— 这叫「**依赖地狱**」，补到第 5 个依赖又缺别的依赖时最崩溃。\n\n★ **两个 DNF5 的坑**（Fedora 41+ 改的）：\n- `dnf localinstall ./x.rpm` —— **这个子命令已被移除**，会报错\n- 直接 `dnf install ./x.rpm` 就对了（**路径里的 `./` 不能省**，不然 dnf 会当成包名去仓库里找）\n\n真要用 rpm 也不是不行，但只适合「确定依赖齐全」的场合：\n```bash\nsudo rpm -ivh x.rpm        # -i 安装、-v 显示过程、-h 打进度条\nrpm -qpl x.rpm             # 先看看这个包会往哪放什么文件\n```"
            }
        ]
    },
    {
        "title": "编译时提示找不到头文件，该装什么包",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "编译",
            "devel",
            "头文件",
            "第 05 讲"
        ],
        "choices": [
            "xxx",
            "xxx-devel",
            "xxx-libs",
            "xxx-headers"
        ],
        "source_section": "第 05 讲 · 硬件与软件安装",
        "statement_md": "你编译一个程序，报错 `fatal error: xxx.h: No such file or directory`。应该装哪个包？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`xxx-devel`** —— 头文件放在 `-devel` 包里。\n\nFedora 把每个库**拆成两个包**：\n\n| 包名 | 装什么 | 谁需要 |\n|---|---|---|\n| `xxx` | **运行时**：`.so` 共享库 | 只想**运行**用它的程序 |\n| **`xxx-devel`** | **开发用**：`.h` 头文件 + 链接用的 `.so` 符号链接 | **要编译** |\n\n★ 所以「明明装了那个库，编译还是找不到头文件」是**最常见的误解** —— 你装的是运行时包，头文件压根不在里面。\n\n**一次装齐编译环境**（比一个个补依赖靠谱）：\n```bash\nsudo dnf group install development-tools     # ★ 是 dev tools，不是 build-essential\nsudo dnf builddep 包名.spec                  # 从 spec 里自动装齐全部编译依赖\n```\n（`build-essential` 是 **Ubuntu 的包名**，Fedora 上不存在。）"
            }
        ]
    },
    {
        "title": "DNF5 里怎么装一个软件包组",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "dnf5",
            "group",
            "版本差异",
            "第 05 讲"
        ],
        "choices": [
            "sudo dnf groupinstall development-tools",
            "sudo dnf group install development-tools",
            "sudo dnf install group development-tools",
            "sudo dnf install @group development-tools"
        ],
        "source_section": "第 05 讲 · 硬件与软件安装",
        "statement_md": "在 Fedora 44（DNF5）里，想安装一个「软件包组」（比如开发工具组），正确写法是？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`sudo dnf group install development-tools`** —— DNF5 要求 `group` 和 `install` **分成两个词**。\n\n★ `groupinstall`（一个词）是 **DNF4 / yum 时代的写法**，DNF5 里已经**不是有效子命令**。无数网上教程还在用老写法，照抄会报 `Unknown command: groupinstall`。\n\n同理还有一对：\n| 老写法（DNF4/yum） | 新写法（DNF5） |\n|---|---|\n| `dnf groupinstall xxx` | **`dnf group install xxx`** |\n| `dnf groupremove xxx` | `dnf group remove xxx` |\n| `dnf grouplist` | `dnf group list` |\n\n★ 这类「七年换了三轮」的差异，第 05 讲整章都是 —— 因为教材是 2020 年 / Fedora 30 蓝本写的，包管理变化最剧烈。\n\n查有哪些组：`dnf group list`。"
            }
        ]
    },
    {
        "title": "装完显卡驱动能不能立刻重启",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "nvidia",
            "akmod",
            "显卡驱动",
            "第 05 讲"
        ],
        "choices": [
            "直接重启，装完就能用",
            "先 `modinfo -F version nvidia` 确认模块编好了",
            "先 `dnf remove` 卸掉 nouveau",
            "先 `setsebool` 放行显卡"
        ],
        "source_section": "第 05 讲 · 硬件与软件安装",
        "statement_md": "你 `sudo dnf install akmod-nvidia` 装完闭源显卡驱动，想立刻重启看看效果。**先做什么**更安全？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**先确认内核模块真的编好了再重启**：\n```bash\nmodinfo -F version nvidia     # 能打出驱动版本号 = 编好了，可以重启\n```\n\n★ **为什么不能立刻重启**：`akmod` 是「**a**utomatic **kmod**」—— 它在你装完后**才开始后台编译**内核模块（要几十秒到几分钟）。编译没完就重启，新驱动起不来，屏幕直接**黑屏**，而且黑屏之后你连终端都进不去，只能靠 rescue 模式救。\n\n**`akmod` vs `kmod`**（这是第 05 讲的一个考点）：\n\n| 包名 | 行为 |\n|---|---|\n| `kmod-nvidia` | 预先编好的，**内核一升级就失效**，得手动重装 |\n| **`akmod-nvidia`** | `a` = **automatic**，内核升级后**自动重建** ✅ |\n\n所以永远选 `akmod`。"
            }
        ]
    },
    {
        "title": "Fedora 上有 dpkg 吗",
        "subject": "linux",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 3,
        "total_score": 8,
        "tags": [
            "dpkg",
            "deb",
            "包管理",
            "第 05 讲"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 05 讲 · 硬件与软件安装",
        "statement_md": "Fedora 上可以用 `dpkg -i xxx.deb` 来安装 Debian 系的 deb 软件包。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "错",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|错\n|错误\n|×\n|F\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**错**。**Fedora 上没有 `dpkg`** —— 那是 **Debian / Ubuntu** 的包管理器。\n\n两个体系的分工：\n\n| 发行版系 | 包格式 | 底层工具 | 高层工具 |\n|---|---|---|---|\n| **Red Hat 系**（Fedora、RHEL、CentOS） | `.rpm` | `rpm` | **`dnf`** |\n| **Debian 系**（Debian、Ubuntu） | `.deb` | **`dpkg`** | `apt` |\n\n**真想装 deb 包**：只能先转换，用 `alien`：\n```bash\nsudo dnf install alien\nsudo alien -r xxx.deb     # 转成 .rpm\n```\n★ 但**三个已知风险**（第 05 讲专门列过）：\n1. 依赖名对不上（`libfoo2` 在 Fedora 可能叫 `libfoo`）\n2. 库版本不匹配\n3. SELinux 标签可能不对\n\n**结论：转换出来的 rpm 只在虚拟机里试，别往主力机上装。**\n正确做法是找 Fedora 原生包，或者找上游的 Flatpak / 源码编译。"
            }
        ]
    },
    {
        "title": "一键回滚上一次软件安装",
        "subject": "linux",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 4,
        "total_score": 12,
        "tags": [
            "dnf",
            "history",
            "回滚",
            "第 05 讲"
        ],
        "choices": [],
        "source_section": "第 05 讲 · 硬件与软件安装",
        "statement_md": "你刚用 `dnf` 装了一堆东西，结果把系统搞坏了。想**撤销刚才那次操作**，用哪条命令？（先要查到操作编号）\n\n提示：dnf 的子命令，配合 `undo` 和事务编号。",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "sudo dnf history undo 1",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|sudo dnf history undo 1\n|dnf history undo 1\n|sudo dnf history undo last\n|dnf history undo last\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "```bash\ndnf history                 # 先看历史，找到要撤销的编号\nsudo dnf history undo 12    # 把编号 12 那次操作完整回滚\n```\n\n★ 这是**改坏系统之后的正解** —— 不用重装，dnf 会按那次事务的记录把装上的包卸掉、把升级的包降回去。\n\n常用配套：\n```bash\ndnf history list            # 简表\ndnf history info 12         # 看这次到底动了什么\nsudo dnf history rollback 12  # 回滚到 12 号那次之后的状态（比 undo 更狠）\n```\n\n★ 另一个「零风险预演」技巧：\n```bash\nsudo dnf install --assumeno 一堆包    # 只打印「将会做什么」，不真装\n```\n装之前先跑一遍，能看出它要带进来多少东西 —— 避免装完才发现拖家带口。"
            }
        ]
    },
    {
        "title": "教材让你敲 ifconfig，但机器上没这个命令",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "ifconfig",
            "ip",
            "net-tools",
            "第 06 讲"
        ],
        "choices": [
            "装回 net-tools 包，恢复 ifconfig",
            "改用 ip addr",
            "用 sudo 提权就能用",
            "先 systemctl start network 启动网络服务"
        ],
        "source_section": "第 06 讲 · 网络的基本配置",
        "statement_md": "教材 6.2.4 节讲用 `ifconfig` 看网卡信息。你在 Fedora 44 上敲，报 `command not found`。怎么办？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**改用 `ip addr`**（或简写 `ip a`）。\n\nFedora 22 起**默认不再安装 `net-tools`** —— 那个包里装的就是`ifconfig`、`netstat`、`route` 这些**已被淘汰**的工具。它们被 `iproute2` 套件取代了：\n\n| 老命令（net-tools） | 新命令（iproute2） |\n|---|---|\n| `ifconfig` | **`ip addr`** / `ip link` |\n| `route -n` | `ip route` |\n| `netstat -anp` | **`ss -tulpn`** |\n| `arp -a` | `ip neigh` |\n\n★ 为什么**不建议装回 net-tools**：装回来会让**两套工具共存** —— `ifconfig` 和 `ip` 的显示口径不一样，排查问题时更容易搞混。直接适应 `ip` 是正路。\n\n补充：`ip addr` 加的地址是**临时的**，重启就没。永久配置得用 `nmcli`。"
            }
        ]
    },
    {
        "title": "nmcli 改完 IP 为什么不生效",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "nmcli",
            "网络配置",
            "第 06 讲"
        ],
        "choices": [
            "命令写错了，要加 sudo",
            "modify 只写配置文件，必须再 con down 再 con up 才生效",
            "要先重启 NetworkManager 服务",
            "必须改 /etc/resolv.conf"
        ],
        "source_section": "第 06 讲 · 网络的基本配置",
        "statement_md": "你用 `nmcli con modify 连接名 ipv4.addresses 192.168.1.100/24` 改了 IP，但 `ip addr` 看还是老地址。为什么？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`nmcli con modify` 只把改动写进配置文件，不重连连接** —— 所以得手动让它重新加载：\n```bash\nnmcli con down 连接名\nnmcli con up 连接名\n```\n\n★ **远程操作时这里有个致命陷阱**：如果你正通过 SSH 连着这台机器改 IP，`con down` 一敲**连接当场就断了**，后面的 `con up` 根本没机会执行。\n\n**三种保命方案**：\n```bash\n# ① 用图形化 TUI（断线也能重连，因为你人在本地）\nsudo nmtui\n\n# ② 把 up 推迟到 5 秒后执行，给自己留出重连的时间\nsudo sh -c 'sleep 5; nmcli con up 连接名' &\n\n# ③ 一次性下上（down 和 up 写在一起，但仍有短暂断线）\nsudo nmcli con down X && sudo nmcli con up X\n```\n\n**验证**：`ip addr show` 看地址有没有变、`nmcli con show X | grep ipv4` 看配置。"
            }
        ]
    },
    {
        "title": "能 ping 通 IP 但打不开网页",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "DNS",
            "resolv.conf",
            "排错",
            "第 06 讲"
        ],
        "choices": [
            "网卡坏了，要换硬件",
            "IP 地址配错了",
            "DNS 解析有问题",
            "防火墙把 80 端口封了"
        ],
        "source_section": "第 06 讲 · 网络的基本配置",
        "statement_md": "`ping 8.8.8.8` 通，但 `ping www.baidu.com` 报 `Name or service not known`，浏览器也打不开网页。问题最可能在哪？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "C",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|C\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**DNS 解析问题，不是网络问题。**\n\n★ 这个判据要背下来：\n\n| 现象 | 结论 |\n|---|---|\n| `ping IP` **通**、`ping 域名` **不通** | **DNS 问题**（网络本身是通的）|\n| `ping IP` **也不通** | 网络层问题（网线/路由/网关） |\n\n**排查顺序**：\n```bash\ncat /etc/resolv.conf          # 看配了哪些 DNS 服务器\ngetent hosts www.baidu.com    # ★ 看系统「真实的解析结果」\nsystemd-resolve --status       # 看当前实际用的 DNS（Fedora 上）\n```\n\n**怎么修（注意别用错方法）**：\n```bash\n# ❌ 直接改 /etc/resolv.conf —— 它是 NetworkManager 自动生成的，\n#    下次重连就被覆盖回去\n# ✅ 通过 nmcli 改：\nsudo nmcli con modify 连接名 ipv4.dns \"8.8.8.8 114.114.114.114\"\nsudo nmcli con down 连接名 && sudo nmcli con up 连接名\n```\n\n★ 为什么用 `getent hosts` 而不是直接看 `resolv.conf`：`resolv.conf` 可能被覆盖，而 `getent` 走的是 **glibc 的完整解析链路**（`/etc/nsswitch.conf` 决定先查 `/etc/hosts` 还是先问 DNS），看到的是**系统真实的解析结果**。"
            }
        ]
    },
    {
        "title": "查看网卡的「真实名字」",
        "subject": "linux",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 3,
        "total_score": 12,
        "tags": [
            "网卡名",
            "ip",
            "第 06 讲"
        ],
        "choices": [],
        "source_section": "第 06 讲 · 网络的基本配置",
        "statement_md": "你照教材写 `ifconfig eth0`，报 `Device not found`。不确定这台机器的网卡到底叫什么名字 —— 用哪条命令**一眼看出所有网卡名**？\n\n提示：ip 命令的简洁模式，只看链路（link）不看地址。",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ip -br link",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ip -br link\n|ip link show\n|ip -brief link\n|ip -br addr\n|ip link\n|nmcli device status\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`ip -br link`**（`-br` = brief，简洁模式）。\n\n输出形如：\n```\nlo               UNKNOWN        00:00:00:00:00:00 <LOOPBACK,UP,LOWER_UP>\nenp1s0           UP             aa:bb:cc:dd:ee:ff <BROADCAST,MULTICAST,UP,LOWER_UP>\nwlp2s0           DOWN           ff:ee:dd:cc:bb:aa <BROADCAST,MULTICAST>\n```\n一眼就能看到真名（`enp1s0`、`wlp2s0`），而不是想当然的 `eth0`。\n\n★ **为什么不是 `eth0`**：现代 Linux 用**可预测网卡名**（predictable network interface names）。\n\n| 名字 | 含义 |\n|---|---|\n| `enp1s0` | **e**thernet、**n**etwork、**p**CI 总线 1、**s**lot 0 |\n| `wlp2s0` | **w**ireless、PCI 总线 2、slot 0 |\n| `lo` | 回环接口（永远存在） |\n\n这么改是为了防止「插拔网卡顺序一变，eth0 和 eth1 就换了个」—— 那种情况下防火墙规则、网卡配置全都会错位。\n\n顺带：`nmcli device status` 也能列出网卡，而且带上连接状态，同样好用。"
            }
        ]
    },
    {
        "title": "替代 netstat 看端口",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "ss",
            "netstat",
            "端口",
            "第 06 讲"
        ],
        "choices": [
            "sudo lsof -i",
            "ss -tulpn",
            "netstat -tulpn",
            "ip port show"
        ],
        "source_section": "第 06 讲 · 网络的基本配置",
        "statement_md": "教材用 `netstat -anp` 查看监听端口。Fedora 44 上应该用哪条？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`ss -tulpn`** —— 参数逐个拆开看：\n\n| 参数 | 含义 |\n|---|---|\n| `-t` | **t**cp |\n| `-u` | **u**dp |\n| `-l` | **l**istening，只看监听中的 |\n| `-p` | **p**rocess，显示是哪个进程占着（**要 sudo 才看得到别人的进程**）|\n| `-n` | **n**umeric，**端口和地址都用数字**，不做服务名反查 |\n\n★ **`-n` 为什么要加**：不加的话，`ss` 会把端口号反向解析成服务名（`:80` → `:http`）。问题是解析依赖 `/etc/services`，**某些端口能解析出来、某些不能** —— 一条输出里混着 `http` 和 `54321` 两种风格，排查时看着特别乱。**排障一律 `-n`**。\n\n典型输出：\n```\ntcp   LISTEN 0  4096  0.0.0.0:22    0.0.0.0:*  users:((\"sshd\",pid=1234,fd=3))\ntcp   LISTEN 0  511   0.0.0.0:80    0.0.0.0:*  users:((\"httpd\",pid=2345,fd=4))\n```\n\n★ 另一条好用的：`sudo lsof -i :80`（查**谁占着 80 端口**）。"
            }
        ]
    },
    {
        "title": "scp 和 ssh 的端口参数大小写",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "scp",
            "ssh",
            "端口",
            "第 06 讲"
        ],
        "choices": [
            "scp -p 2222 文件 远端:",
            "scp -P 2222 文件 远端:",
            "scp -port 2222 文件 远端:",
            "scp --port=2222 文件 远端:"
        ],
        "source_section": "第 06 讲 · 网络的基本配置",
        "statement_md": "SSH 服务跑在 2222 端口（不是默认的 22）。用 `scp` 传文件时，指定端口应该怎么写？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`scp -P 2222 ...`（大写 P）**。\n\n★ 这就是最坑的地方 —— **`ssh` 和 `scp` 的大小写刚好相反**：\n\n| 命令 | 指定端口 | 那另一个大小写是什么 |\n|---|---|---|\n| `ssh` | **`-p 2222`**（小写） | `-P` 是「不分配伪终端」 |\n| `scp` | **`-P 2222`**（大写） | `-p` 是「保留文件的时间戳和权限」 |\n| `sftp` | **`-P 2222`**（大写） | 同 scp |\n\n**用小写 `-p` 的后果**：scp **不报错**，只是默默地连到 22 端口 —— 如果 22 上没服务，你会看到 `Connection refused`，然后开始怀疑网络、怀疑防火墙，**就是想不到是大写小写的问题**。\n\n**另一条路**（记不住就用这个）：在 `~/.ssh/config` 里给主机建个别名：\n```\nHost myserver\n    HostName 192.168.1.10\n    Port 2222\n    User lijihao\n```\n之后 `scp 文件 myserver:` 和 `ssh myserver` 都不用再写端口了。"
            }
        ]
    },
    {
        "title": "改主机名的正确方式",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "hostname",
            "hostnamectl",
            "第 06 讲"
        ],
        "choices": [
            "要用 sudo hostname mypc",
            "hostname 只改当前运行时的值，永久生效要用 hostnamectl set-hostname",
            "还得改 /etc/resolv.conf",
            "主机名不能改，只能重装"
        ],
        "source_section": "第 06 讲 · 网络的基本配置",
        "statement_md": "你想把主机名从 `fedora` 改成 `mypc`。用 `hostname mypc` 改完，**重启后变回去了**。怎么回事？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`hostname` 只改「当前运行时的值」，不写配置文件** —— 重启就复原。\n\n**永久修改要用**：\n```bash\nsudo hostnamectl set-hostname mypc\n```\n它会同时写入 `/etc/hostname`，重启后依然生效。\n\n**验证**：\n```bash\nhostnamectl                # 看 Static hostname\ncat /etc/hostname          # 看配置文件\n```\n\n★ **一个让人以为「没生效」的正常现象**：改完之后，**当前终端提示符里的主机名不会立刻变** —— 因为提示符是**登录时**拼好存在 `$PS1` 里的。**重新登录**（或 `exec bash`）才会变。\n\n**相关文件理清楚**：\n| 文件 | 作用 |\n|---|---|\n| `/etc/hostname` | 静态主机名（`hostnamectl` 写这个）|\n| `/etc/hosts` | 本机名字 → IP 的**即时映射**，改完立刻生效，不用重启 |\n| `/etc/resolv.conf` | **DNS 服务器**地址，跟主机名没关系 |\n\n（`/etc/hosts` 里那行 `127.0.0.1 localhost` **绝不能删** —— 删了本机通信会出各种怪问题。）"
            }
        ]
    },
    {
        "title": "ping 不通就一定是网络故障",
        "subject": "linux",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 2,
        "total_score": 8,
        "tags": [
            "ping",
            "ICMP",
            "排错",
            "第 06 讲"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 06 讲 · 网络的基本配置",
        "statement_md": "`ping 某台主机` 不通，就可以确定是网络有问题。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "错",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|错\n|错误\n|×\n|F\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**错**。**很多主机主动禁掉了 ICMP**（ping 用的协议）—— 这是一种常见的安全/防扫措施，跟「网络通不通」是两件事。\n\n**更靠谱的连通性验证**：\n```bash\nnc -zv 主机 端口        # 测 TCP 端口能不能连上（最实用）\ncurl -I http://主机/    # 只取 HTTP 响应头\nss -tulpn | grep 端口   # 在本机确认服务真的在监听\ntraceroute 主机         # 看卡在哪一跳\n```\n\n★ **另一个必加的参数**：`ping` **不带 `-c` 会一直发**，忘了停就一直在那刷。脚本里必须写 **`ping -c 4 主机`**（发 4 个包就停）。\n\n**还有一对容易搞反的**：\n```bash\nping 域名        # 同时验证 DNS 解析 + 网络连通\nping IP          # 只验证网络连通\n```\n两者对比一下，就能区分「是 DNS 坏还是网络坏」。"
            }
        ]
    },
    {
        "title": "systemctl enable 之后服务在跑吗",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "systemctl",
            "enable",
            "服务",
            "第 07 讲"
        ],
        "choices": [
            "Apache 装错了",
            "enable 只是「设为开机自启」，不会启动服务。要用 enable --now",
            "要重启机器才生效",
            "防火墙没放行"
        ],
        "source_section": "第 07 讲 · 常用网络服务",
        "statement_md": "你执行了 `sudo systemctl enable httpd`，以为网站已经能访问了。结果浏览器打不开。为什么？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`enable` 和 `start` 是两件事。**\n\n| 命令 | 作用 | 现在跑不跑 |\n|---|---|---|\n| `systemctl start X` | **立刻启动** | ✅ 跑 |\n| `systemctl enable X` | **设为开机自启**（写符号链接） | ❌ **不跑** |\n| **`systemctl enable --now X`** | 两个一起做 | ✅ 跑 |\n\n★ 正确姿势基本永远是 **`enable --now`** —— 既设了自启，又立刻起来。\n\n**怎么确认状态**（这是排查服务的第一步）：\n```bash\nsystemctl status httpd\n```\n输出里两行要分清：\n```\nLoaded: loaded (/usr/lib/systemd/system/httpd.service; enabled; ...)\n                                     ↑ 这是「自启状态」\nActive: active (running) since ...\n        ↑ 这才是「运行状态」\n```\n★ **`Loaded: enabled` 完全不代表服务在跑** —— `enabled` 只是说「下次开机我会拉起它」。只有 `Active: active (running)` 才是真在跑。\n\n另外：改完 unit 文件**必须 `systemctl daemon-reload`**，否则改动不生效（这个坑很多人踩）。"
            }
        ]
    },
    {
        "title": "四个服务的「户口本」",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "httpd",
            "smb",
            "named",
            "服务名",
            "第 07 讲"
        ],
        "choices": [
            "包名和服务名全都一样",
            "Apache 包 httpd 服务 httpd；Samba 包 samba 服务 smb；BIND 包 bind 服务 named；vsFTPd 两者都叫 vsftpd",
            "Apache 包 apache2 服务 httpd；Samba 包 smbd 服务 samba；BIND 包 named 服务 named",
            "全都得用 systemctl list-unit-files 现查才知道"
        ],
        "source_section": "第 07 讲 · 常用网络服务",
        "statement_md": "在 Fedora 上，**Apache / vsFTPd / Samba / BIND 这四个服务**，各自的**包名**和**服务名**对应关系是？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "这是第 07 讲最该背下来的一张表 —— **包名和服务名不一定相同**：\n\n| 服务 | 包名 | **服务名**（systemctl 用的） |\n|---|---|---|\n| Apache HTTP | `httpd` | `httpd` |\n| vsFTPd | `vsftpd` | `vsftpd` |\n| **Samba** | `samba` | **`smb`** ★ |\n| **BIND（DNS）** | `bind` + `bind-utils` | **`named`** ★ |\n\n★ 两个「名不副实」的：\n- Samba **包**叫 `samba`，**服务**叫 `smb` —— 敲 `systemctl enable samba` 会报 `Unit samba.service not found`\n- BIND **包**叫 `bind`，**服务**叫 `named`（**n**ame **d**aemon）—— 同理，敲 `systemctl enable bind` 也找不到\n\n**另外两个常见错**：\n- `dnf install apache` / `apache2` —— Fedora 上是 **`httpd`**（`apache2` 是 Debian/Ubuntu 的叫法）\n- 想不起来服务叫什么 → `systemctl list-unit-files | grep 关键字` 查一下最快"
            }
        ]
    },
    {
        "title": "服务配好了，外面还是访问不到",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "firewalld",
            "SELinux",
            "双重门禁",
            "第 07 讲"
        ],
        "choices": [
            "先看 SELinux，再看防火墙",
            "先查 firewall-cmd，再查 SELinux",
            "先重装 Apache",
            "先看 /var/log/messages"
        ],
        "source_section": "第 07 讲 · 常用网络服务",
        "statement_md": "你把 Apache 配好了，`systemctl status httpd` 显示 `active (running)`，但**从别的机器访问不到**。按第 07 讲的经验，应该**按什么顺序**排查？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**先查 firewalld，再查 SELinux** —— 这个顺序有讲究。\n\nFedora 上有**两道门禁**，服务要在外面能访问，两道都得放行：\n\n| | 管什么 | 怎么放行 | 报错特征 |\n|---|---|---|\n| **firewalld** | **端口**能不能进 | `firewall-cmd --permanent --add-service=http` + `--reload` | **连接被拒/超时**（包根本没进来） |\n| **SELinux** | 进程能不能读写**这个文件** | `semanage fcontext` + `restorecon` | **403 / 权限拒绝**（进程起来了但读不到文件）|\n\n★ **为什么先防火墙**：因为它更靠外 —— 如果端口都没放行，包压根到不了 Apache，SELinux 根本没机会参与。先解决外层的，再看内层的，否则会白折腾。\n\n**怎么快速判断是哪一层**：\n- **本机 curl 通、外部不通** → **防火墙**问题\n- **本机 curl 也 403** → 大概率是 **SELinux**（或者文件权限）\n\n查防火墙：`sudo firewall-cmd --list-all`\n查 SELinux：`sudo ausearch -m avc -ts recent`（**要 sudo**，否则误判「没有 AVC」）"
            }
        ]
    },
    {
        "title": "chcon 和 semanage 的区别",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "SELinux",
            "semanage",
            "chcon",
            "第 07 讲"
        ],
        "choices": [
            "chcon，它是标准做法",
            "semanage fcontext + restorecon，chcon 是临时的会被冲掉",
            "两个完全等价，随便用",
            "两个都不用，改文件权限就行"
        ],
        "source_section": "第 07 讲 · 常用网络服务",
        "statement_md": "要给一个自建目录打上正确的 SELinux 标签，`chcon` 和 `semanage fcontext` 应该用哪个？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**用 `semanage fcontext` + `restorecon`**（两步缺一不可）。\n\n| 命令 | 性质 | 会被覆盖吗 |\n|---|---|---|\n| `chcon` | **临时**改文件标签 | ✅ 会被 `restorecon` 或重启冲掉 |\n| **`semanage fcontext`** | **登记一条规则**（写进策略） | ❌ 永久 |\n| **`restorecon`** | **按规则刷新已有文件的标签** | —— |\n\n★ **关键认知**：`semanage fcontext` **只是登记规则，不碰现有文件**。很多人跑完 `semanage` 就去测试，怎么都不生效 —— **因为还得跑 `restorecon` 把旧标签刷一遍**。\n\n标准两步：\n```bash\nsudo semanage fcontext -a -t httpd_sys_content_t \"/srv/www(/.*)?\"\nsudo restorecon -Rv /srv/www\n```\n★ 注意那个 **`(/.*)?`** 正则 —— 不写它的话**只匹配目录本身、管不到里面的文件**，症状就是「目录能进、文件 403」。\n\n另外 `semanage` 命令本身在 Fedora 上**默认没装**，要 `sudo dnf install policycoreutils-python-utils`。\n\n**绝对不要对 `/etc`、`/usr` 做 `chcon -R`** —— 会严重破坏系统。"
            }
        ]
    },
    {
        "title": "改完 unit 文件为什么没生效",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "systemd",
            "drop-in",
            "ExecStart",
            "第 07 讲"
        ],
        "choices": [
            "少写一行空的 ExecStart= 先把原值清掉",
            "drop-in 应该写在 /usr/lib 下",
            "要加 --force 参数",
            "要先 systemctl daemon-reload —— 重载了就没事"
        ],
        "source_section": "第 07 讲 · 常用网络服务",
        "statement_md": "你用 `systemctl edit myservice` 写了 drop-in 覆盖 `ExecStart`，然后 `systemctl restart myservice` 却报 `multiple ExecStart`。少了什么？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "A",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|A\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**必须先写一行空的 `ExecStart=` 把原值清空。**\n\nsystemd 的规则是：**同一个指令出现多次 = 追加**。所以 drop-in 里直接写 `ExecStart=/新命令` 会变成\n「旧命令 + 新命令」两条启动命令 → 报 `multiple ExecStart`。\n\n正确写法：\n```ini\n[Service]\nExecStart=                    # ★ 这一行空的，作用是「清空原值」\nExecStart=/opt/myservice/bin/run --new-flag\n```\n★ 空行看着莫名其妙，但它**就是这个用途** —— 记住「先清空、再赋值」。\n\n**另外两个配套要点**：\n1. **改完 unit 文件必须 `sudo systemctl daemon-reload`** —— 不然 systemd 用的还是老配置（这个坑比 `ExecStart` 那个更常见）\n2. **不要去改 `/usr/lib/systemd/system/*.service`** —— 包升级时你的改动会被覆盖。要用 `systemctl edit X` 写 drop-in，它落在 `/etc/systemd/system/X.service.d/` 下，升级不丢"
            }
        ]
    },
    {
        "title": "disable 和 mask 有什么不同",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "systemctl",
            "disable",
            "mask",
            "第 07 讲"
        ],
        "choices": [
            "完全一样",
            "disable 只取消自启（还能手动 start）；mask 彻底禁死（连手动都起不来）",
            "disable 是临时的，mask 是永久的",
            "mask 会卸载软件包"
        ],
        "source_section": "第 07 讲 · 常用网络服务",
        "statement_md": "`systemctl disable X` 和 `systemctl mask X` 的区别是？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**两个力度完全不同**：\n\n| 命令 | 做了什么 | 还能手动 start 吗 |\n|---|---|---|\n| `disable` | 删掉开机自启的符号链接 | ✅ **能** |\n| `mask` | 把服务**链到 `/dev/null`** | ❌ **不能**，会报 `Unit X is masked` |\n\n★ **`mask` 的使用场景**：某个服务被别的服务依赖，老是自动被拉起来，你**根本不想让它跑**（比如和另一个方案冲突）—— 这时才用 `mask`。\n\n**取消 mask**：`sudo systemctl unmask X`。\n\n**`enable` 和 `start` 的对应关系**（一起记）：\n| | 立刻跑 | 开机自启 |\n|---|---|---|\n| `start` | ✅ | ❌ |\n| `enable` | ❌ | ✅ |\n| `enable --now` | ✅ | ✅ |\n\n再加一个：**`restart` vs `reload`** —— 改的是「仅配置类」的变更优先用 `reload`（**不中断现有连接**）；拿不准就 `reload-or-restart`。"
            }
        ]
    },
    {
        "title": "useradd 之后为什么登录不了",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "useradd",
            "passwd",
            "用户管理",
            "第 08 讲"
        ],
        "choices": [
            "要先 usermod 加 shell",
            "useradd 建的账号是锁死的（shadow 里是 !!），必须再 passwd 设密码",
            "要重启系统",
            "要先 useradd -m 建家目录"
        ],
        "source_section": "第 08 讲 · 系统管理与监视",
        "statement_md": "你执行了 `sudo useradd zhang`，然后用 `su - zhang` 却进不去。为什么？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`useradd` 只建账号，不给密码** —— 建出来的账号是**锁死状态**（`/etc/shadow` 里密码字段是 `!!`）。\n\n```bash\nsudo useradd -m zhang     # -m 顺便建家目录并放好骨架文件\nsudo passwd zhang         # ★ 这一步不能少：交互式设密码\n```\n\n★ **`useradd` vs `adduser`**（Fedora 上两个都在）：\n| | 行为 |\n|---|---|\n| `useradd` | **底层**命令，只建账号，什么都不问；不建家目录（除非 `-m`）|\n| `adduser` | Fedora 上是 `useradd` 的**友好包装**，会交互式问你密码、全名等 |\n\n（注意：Debian 系上 `adduser` 是完全不同的实现，行为差得更远。）\n\n**验证账号状态**：\n```bash\nsudo passwd -S zhang      # 输出第二列：L = 锁定 / P = 已设密码\nsudo grep zhang /etc/shadow   # 看密码字段\n```\n\n★ 相关陷阱：**别用 `passwd -d` 想禁用账号** —— `-d` 是**删掉密码**，等于**免密登录**（更危险）。想禁要用 **`passwd -l`**（lock）。"
            }
        ]
    },
    {
        "title": "usermod 加附加组，-G 还是 -aG",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "usermod",
            "附加组",
            "-aG",
            "第 08 讲"
        ],
        "choices": [
            "sudo usermod -G wheel zhang",
            "sudo usermod -aG wheel zhang",
            "sudo usermod -g wheel zhang",
            "sudo groupadd -a wheel zhang"
        ],
        "source_section": "第 08 讲 · 系统管理与监视",
        "statement_md": "你要把用户 `zhang` 加进 `wheel` 组，**同时保留他原来已经在的所有组**。正确的是哪条？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`sudo usermod -aG wheel zhang`** —— `-a`（append，追加）不能省。\n\n★ **漏掉 `-a` 的后果很严重**：`-G` 是「**设置**附加组」，会**覆盖**掉用户原有的全部附加组。\n\n举个例子：某用户本来在 `wheel`、`audio`、`video`、`libvirt` 四个组里，你执行 `usermod -G docker zhang` 想加 docker 组 —— 结果变成**只有 docker 组**，声音没了（audio 丢了）、显卡加速没了（video 丢了）、sudo 用不了（wheel 丢了）。\n\n**三个 G 分清楚**：\n\n| 参数 | 作用 | 危险度 |\n|---|---|---|\n| `-g`（小写）| 改**主组** | 高（覆盖）|\n| `-G`（大写）| **设置**附加组列表 | ★ **高，覆盖** |\n| **`-aG`** | **追加**附加组 | 低 ✅ |\n\n★ **口诀：加组永远写 `-aG`**。\n\n**另一个「以为没生效」的正常现象**：加完组当场用新权限**不生效** —— 因为**组身份是登录时快照的**。要 `exec bash` 或重新登录。\n\n**查自己在哪些组**：`id -nG`（`whoami` 只看名字，看不到组）。"
            }
        ]
    },
    {
        "title": "想看系统日志，该打开哪个文件",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "journalctl",
            "日志",
            "rsyslog",
            "第 08 讲"
        ],
        "choices": [
            "装 rsyslog 才有这个文件",
            "用 journalctl",
            "改用 /var/log/syslog",
            "改用 dmesg"
        ],
        "source_section": "第 08 讲 · 系统管理与监视",
        "statement_md": "照教材敲 `cat /var/log/messages` 想看系统日志，结果报 `No such file or directory`。应该用什么？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**用 `journalctl`** —— Fedora 默认**不装 rsyslog**，`/var/log/messages` 这个文件根本不存在。\n\nFedora 用的是 **systemd-journald**，日志收在**二进制**日志里，要用 `journalctl` 读：\n\n```bash\njournalctl -n 50                 # 最近 50 条\njournalctl -u httpd              # 只看某个服务的\njournalctl -p err                # 只看 error 级别以上\njournalctl --since \"1 hour ago\"  # 最近一小时\njournalctl -f                    # 实时跟（类似 tail -f）\njournalctl -b                    # 本次开机以来的\n```\n\n★ **一个必知的默认行为**：journald **默认不持久化** —— 日志只存在内存里（`/run/log/journal/`），**重启就没了**。\n\n想保留重启前的日志，要手动开启持久化：\n```bash\nsudo mkdir -p /var/log/journal\nsudo systemd-tmpfiles --create --prefix /var/log/journal\nsudo systemctl restart systemd-journald\n```\n之后重启才能用 `journalctl -b -1` 查**上一次开机**的日志（**不开持久化的话，`-b -1` 查不到任何东西**）。\n\n（`rsyslog` 装了会同时生成 `/var/log/messages`，但 Fedora 默认没有。）"
            }
        ]
    },
    {
        "title": "chmod -R 644 目录的后果",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "chmod",
            "目录权限",
            "x 位",
            "第 08 讲"
        ],
        "choices": [
            "要 sudo",
            "目录失去 x 权限就进不去了 —— 目录要 755、文件才 644",
            "要 chown 一下",
            "644 的 6 太少了"
        ],
        "source_section": "第 08 讲 · 系统管理与监视",
        "statement_md": "你执行了 `chmod -R 644 /home/zhang/project`，想把文件权限统一。结果 `cd` 进那个目录都报 Permission denied。为什么？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**因为目录的权限位含义和文件不一样：目录的 `x` 是「能进入/能穿过」。**\n\n| 位 | 对**文件** | 对**目录** |\n|---|---|---|\n| `r` | 读内容 | **列出**里面有什么（`ls`）|\n| `w` | 写内容 | **在里面建/删**文件 |\n| **`x`** | 当作程序执行 | ★ **能进去（`cd`）、能访问里面的文件** |\n\n`644` 的权限是 `rw-r--r--` —— **没有 `x`**。对文件无所谓，对目录就是「**连进都进不去**」。\n\n**正确做法：目录和文件分开设**。\n```bash\nfind /home/zhang/project -type d -exec chmod 755 {} \\;   # 目录 755\nfind /home/zhang/project -type f -exec chmod 644 {} \\;   # 文件 644\n```\n\n★ **记住这组常规值**：\n| 对象 | 权限 | 含义 |\n|---|---|---|\n| 普通目录 | `755` | 人人能进、只有属主能写 |\n| 普通文件 | `644` | 人人能读、只有属主能写 |\n| 私钥 / 密码文件 | `600` | **只有属主**能读写 |\n\n**`777` 在什么场合都不该用**（生产环境等于取消整个权限体系）。"
            }
        ]
    },
    {
        "title": "杀进程该用哪个信号",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "kill",
            "SIGTERM",
            "SIGKILL",
            "第 08 讲"
        ],
        "choices": [
            "直接 kill -9，一步到位",
            "先 kill（默认 15），等几秒不行再 kill -9",
            "先 kill -1，再 kill -9",
            "用 killall -9 批量杀"
        ],
        "source_section": "第 08 讲 · 系统管理与监视",
        "statement_md": "一个进程卡住了，你要杀掉它。第 08 讲的建议是？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**先 `kill`（默认发 15 号信号），等几秒，还不行再 `kill -9`。**\n\n两个信号的本质区别：\n\n| 信号 | 名字 | 行为 |\n|---|---|---|\n| **15（默认）** | SIGTERM | **请求**进程自己收尾退出 —— 进程能**捕获**它，先把缓存刷盘、关文件、释放锁，然后干净地退出 |\n| **9** | SIGKILL | **内核直接宰掉**，进程**无法捕获、无法反抗** |\n\n★ **为什么不能一上来 `-9`**：进程被硬杀时**没机会收尾**，可能留下：\n- 数据库写到一半（数据损坏）\n- 端口没释放（下次启动报 `Address already in use`）\n- 锁文件残留（下次启动说「已经在运行」）\n- 临时文件堆积\n\n**所以正确顺序是**：\n```bash\nkill PID            # 15，给它机会好好退\nsleep 3\nkill -9 PID         # 还赖着才硬来\n```\n\n**另外两个易错点**：\n1. **僵尸进程杀不掉** —— 它**已经死了**，`kill -9` 完全无效。要处理它的**父进程**（父进程 wait 之后它才会消失）\n2. **别用 `ps aux | grep x` 找进程** —— 输出里总会多出 `grep x` 自己那一行。用 `pgrep -a 名字`\n3. **`ps aux` 没有 PPID 列** —— 想找父进程用 `ps -ef` 或 `ps -eo pid,ppid,cmd`"
            }
        ]
    },
    {
        "title": "给脚本设 SUID 想以 root 运行",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "SUID",
            "脚本",
            "权限",
            "第 08 讲"
        ],
        "choices": [
            "要 chown root 才行",
            "内核直接忽略脚本的 SUID 位，SUID 只对二进制程序生效",
            "要放到 /usr/bin 下才行",
            "要 chmod 6755"
        ],
        "source_section": "第 08 讲 · 系统管理与监视",
        "statement_md": "你写了个 shell 脚本，`chmod 4755 script.sh` 设了 SUID 位，想让普通用户执行时以 root 身份运行。结果没有效果。为什么？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**内核故意忽略脚本上的 SUID 位** —— 这是**安全设计**，不是 bug。\n\n**为什么**：脚本是文本，解释器（bash）会逐行读它。如果 SUID 对脚本生效，那么任何能写这个脚本的人（哪怕只是能改中间几行）就相当于**获得了 root 执行任意命令的能力** —— 提权门槛低到离谱。\n\n**正确的做法有两条**：\n\n**① 用 `sudo`**（最推荐）—— 给特定命令开白名单：\n```bash\nsudo visudo      # ★ 永远用 visudo，别直接改 /etc/sudoers\n# 加一行：\nzhang ALL=(root) NOPASSWD: /usr/local/bin/mywork.sh\n```\n\n**② 写个小 C 包装程序**（SUID 对二进制生效）。\n\n★ 顺带记一个相关坑：`chmod 4755` 之后 `ls -l` 看到的是 `rwSr-xr-x` —— **大写 `S` 表示「SUID 设了，但执行位没设」**，配置有问题。\n正确顺序是**先 `chmod +x`，再设特殊位**，这样才显示小写 `s`（`rwsr-xr-x`）。\n\n（`visudo` 为什么必用：它会**校验语法**。直接改 `/etc/sudoers` 写错一个字符，你就**再也 sudo 不了了**。）"
            }
        ]
    },
    {
        "title": "wheel 组能限制 su 吗",
        "subject": "linux",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 4,
        "total_score": 8,
        "tags": [
            "su",
            "wheel",
            "pam",
            "第 08 讲"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 08 讲 · 系统管理与监视",
        "statement_md": "把用户从 `wheel` 组里移除，他就无法使用 `su` 命令了。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "错",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|错\n|错误\n|×\n|F\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**错**。**默认情况下 `su` 没有任何组限制** —— 任何知道 root 密码的用户都能 `su` 上去。\n\n所谓「wheel 组才能 su」的机制**是存在的，但默认是关的** —— 它由 PAM 控制，相关那行在 `/etc/pam.d/su` 里**被注释掉了**：\n```\n#auth  required  pam_wheel.so use_uid\n ↑ 开头的 # 就是「没启用」\n```\n要去掉那个 `#` 才会生效。\n\n★ **分清两个不同的限制**：\n\n| 机制 | 管什么 | 默认状态 |\n|---|---|---|\n| **`wheel` 组 + `sudo`** | 谁能用 sudo | Fedora 上**默认启用** |\n| **`pam_wheel` + `su`** | 谁能用 su | **默认关闭** |\n\n所以在 Fedora 上，普通用户用不了 `sudo`（不在 wheel 组），但只要知道 root 密码，`su -` 照样能上去。\n\n**另外**：Fedora Workstation 安装时**默认不给 root 设密码**，所以默认状态下其实连 `su -` 都用不了，全靠 sudo —— 这也正是 Fedora 推荐的工作方式。"
            }
        ]
    },
    {
        "title": "free 显示的内存很小，是不是不够用",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "free",
            "内存",
            "available",
            "第 08 讲"
        ],
        "choices": [
            "是的，要赶紧关程序",
            "看 available 那一列才是真实可用内存，cache 是可回收的",
            "要加内存条",
            "free 输出不准"
        ],
        "source_section": "第 08 讲 · 系统管理与监视",
        "statement_md": "`free -h` 输出里 `free` 那一列只有 500 MB，但机器是 16 GB 内存。是不是内存要满了？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**看 `available` 列，别看 `free` 列。**\n\nLinux 的设计理念是「**空闲的内存就是浪费的内存**」—— 它会把暂时用不到的内存拿去做**磁盘缓存**（cache/buffers），加速读写。这些缓存在程序需要内存时**可以立刻回收**。\n\n```\n               total   used   free   shared  buff/cache   available\nMem:           15Gi   4.2Gi  500Mi   120Mi      10Gi        10Gi\n                       ↑ used        ↑ free   ↑ 缓存      ↑ ★ 看这个\n```\n\n| 列 | 含义 |\n|---|---|\n| `free` | **完全没被用过**的内存 —— 数字小是**正常且健康的** |\n| `buff/cache` | 磁盘缓存，**随时可回收** |\n| **`available`** | **真正可用于新程序的内存** ≈ free + 可回收的 cache ✅ |\n\n★ 所以 `free` 小**恰恰说明系统在充分利用内存**，不是坏事。\n\n**想主动释放缓存**（一般没必要）：\n```bash\nsync && echo 3 | sudo tee /proc/sys/vm/drop_caches\n```\n\n**配套的两个存储排查命令**：\n- `df -h` 看**磁盘空间**\n- **`df -i`** 看 **inode 用尽** —— 磁盘报 `No space left` 但 `df -h` 显示有空间时，八成是 inode 满了（有大量小文件）"
            }
        ]
    },
    {
        "title": "cron 任务里为什么找不到命令",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "cron",
            "PATH",
            "计划任务",
            "第 08 讲"
        ],
        "choices": [
            "cron 没有权限跑 python",
            "cron 的 PATH 极小，必须写绝对路径 /usr/bin/python3",
            "要加 sudo",
            "要写 python 而不是 python3"
        ],
        "source_section": "第 08 讲 · 系统管理与监视",
        "statement_md": "你在 `crontab -e` 里写了个任务 `* * * * * python3 /home/zhang/x.py`，但日志里报 `python3: command not found`。手动执行却没问题。为什么？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**cron 执行时的 `PATH` 极小**（通常只有 `/usr/bin:/bin`），和你的交互式 shell 完全不是一回事。\n\n★ 你的终端里能跑，是因为 `~/.bashrc` / `/etc/profile` 帮你**扩过 PATH** 了；而 **cron 不读这些文件**。\n\n**正确写法：全部用绝对路径**\n```\n* * * * * /usr/bin/python3 /home/zhang/x.py > /home/zhang/cron.log 2>&1\n```\n\n**顺带几个 cron 的必知坑**：\n\n| 坑 | 正确做法 |\n|---|---|\n| 输出没地方去，全被邮件系统收着 | 加 `> /path/log 2>&1` 重定向 |\n| 时间格式里的 `%` 被当成换行 | 转义：`date +\\%F` |\n| 以为能写「每 30 秒」 | **最小粒度是 1 分钟**；要更细用 systemd timer |\n| `crontab -r` 手一抖 | **一次删光所有任务、不询问**。想安全用 `crontab -i -r` |\n\n**时间格式速记**：\n```\n* * * * *  命令\n│ │ │ │ └── 星期（0-7，0 和 7 都是周日）\n│ │ │ └──── 月（1-12）\n│ │ └────── 日（1-31）\n│ └──────── 时（0-23）\n└────────── 分（0-59）\n```"
            }
        ]
    },
    {
        "title": "/etc/hosts.allow 能限制 SSH 来源吗",
        "subject": "linux",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 4,
        "total_score": 8,
        "tags": [
            "TCPWrappers",
            "hosts.allow",
            "sshd",
            "第 09 讲"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 09 讲 · 系统安全管理",
        "statement_md": "在 `/etc/hosts.allow` 里配置规则，可以限制哪些 IP 能连 SSH。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "错",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|错\n|错误\n|×\n|F\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**错**。**对 sshd 完全失效**。\n\nTCP Wrappers（`hosts.allow` / `hosts.deny`）这套机制要求程序**动态链接 `libwrap`** 才会生效。而 **OpenSSH 7.5 起就不再链接 libwrap 了** —— 所以你写在 `hosts.allow` 里的规则**被完全忽略，且不报任何错**。\n\n★ 这是最阴的一种失效：**你配了、看着像生效了、实际什么都没发生**。\n\n**自证方法**（一条命令就能确认）：\n```bash\nldd $(which sshd) | grep libwrap\n# 空输出 = 没有链接 libwrap = hosts.allow 对 sshd 无效\n```\n\n**正确的做法**（改 `sshd_config`）：\n```\nAllowUsers zhang admin@192.168.1.*\nDenyUsers baduser\nMatch Address 192.168.2.0/24\n    PasswordAuthentication no\n```\n★ 改完**必须**：\n```bash\nsudo sshd -t           # ★ 先校验语法！错一个字符就永久失联\nsudo systemctl reload sshd    # 用 reload 不用 restart\n```"
            }
        ]
    },
    {
        "title": "手动加的 iptables 规则为什么消失了",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "iptables",
            "firewalld",
            "nftables",
            "第 09 讲"
        ],
        "choices": [
            "被系统自动清理了",
            "firewalld 重载时会冲掉手写的规则",
            "iptables 有超时机制",
            "要 iptables-save 才生效"
        ],
        "source_section": "第 09 讲 · 系统安全管理",
        "statement_md": "你用 `iptables -A INPUT ...` 手动加了几条规则，测试时是好的。过了一阵再看，规则没了。为什么？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**firewalld 在重载时会接管（并冲掉）底层的 iptables 规则。**\n\n在 Fedora 上，`iptables` 命令其实**不是真的 iptables** —— 它是 `iptables-nft`，**转发到 nftables 内核框架**。而 firewalld 也是通过 nftables 管理规则的 —— **两者共用同一套底层**，firewalld 一 reload 就会按自己的规则表重写。\n\n★ **必须二选一，不能混着用**：\n\n**方案 A：只用 firewalld**（Fedora 的推荐做法）\n```bash\nsudo firewall-cmd --permanent --add-service=http\nsudo firewall-cmd --reload      # ★ 不加这步，永久规则不生效\nsudo firewall-cmd --list-all    # 验证\n```\n（`--timeout=300` 可以加个自动过期，防止把自己锁在外面。）\n\n**方案 B：直用 iptables 裸命令**\n```bash\nsudo systemctl disable --now firewalld   # ★ 必须先停掉 firewalld\nsudo iptables -A INPUT ...\nsudo iptables-save > /etc/sysconfig/iptables   # 手动持久化\n```\n\n★ **另一个认知纠正**：即使在 iptables 里写了 `-j ACCEPT`，**包还是可能过不去** —— 因为 ACCEPT 只表示「这条链放行」，后面 firewalld 的规则还可能拦。"
            }
        ]
    },
    {
        "title": "setsebool 忘了加什么会失效",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "setsebool",
            "-P",
            "SELinux",
            "第 09 讲"
        ],
        "choices": [
            "漏了 sudo -i",
            "漏了 -P 参数，改动没写进策略",
            "漏了 systemctl reload httpd",
            "漏了 semanage"
        ],
        "source_section": "第 09 讲 · 系统安全管理",
        "statement_md": "你执行 `sudo setsebool httpd_can_network_connect on` 让 Apache 能连网络，测试通了。**重启之后又不通了**。漏了什么？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**漏了 `-P`。**\n\n```bash\nsudo setsebool httpd_can_network_connect on      # ❌ 只在内存里有效，重启就没了\nsudo setsebool -P httpd_can_network_connect on   # ✅ -P = Persistent，写进策略\n```\n\n★ **这个坑为什么特别阴**：\n1. 改完当场测试**是通的** → 你以为搞定了\n2. 重启后失效 → 但你已经把这事忘了，只会觉得「怎么又坏了」\n3. 事后极难定位，因为「同一个操作」在重启前后表现不同\n\n**一句话规矩**：`setsebool` **永远加 `-P`**。\n\n**查看当前值**：\n```bash\ngetsebool -a | grep httpd_can_network_connect\n```\n★ 补充：`setsebool -P` 会**重写整个 SELinux 策略**，所以第一次跑要等几十秒到几分钟，**那是在正常干活，不是卡死了**。\n\n**相关的另一对**（第 09 讲反复强调的）：\n- `setenforce 0` = **临时**切到宽容模式，重启复原\n- 想永久改要改 `/etc/selinux/config` 里的 `SELINUX=`"
            }
        ]
    },
    {
        "title": "semanage 报 command not found",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "semanage",
            "SELinux",
            "安装",
            "第 09 讲"
        ],
        "choices": [
            "semanage 命令不存在，用 chcon 代替",
            "sudo dnf install policycoreutils-python-utils",
            "要 sudo 才有这个命令",
            "要先启动 SELinux"
        ],
        "source_section": "第 09 讲 · 系统安全管理",
        "statement_md": "你在 Fedora 44 上敲 `semanage fcontext ...`，报 `command not found`。怎么办？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**装 `policycoreutils-python-utils` —— Fedora 默认不装它。**\n\n```bash\nsudo dnf install policycoreutils-python-utils\n```\n装完 `semanage`、`audit2allow`、`sealert` 这类工具就都有了。\n\n★ **为什么默认不装**：这些是「**管理 SELinux 策略**」的工具，普通桌面用户根本用不上；默认装的只有 `selinux-policy` 和基础客户端。\n\n**装完之后有个必知的坑**（第 09 讲陷阱清单第 7 条）：\n```bash\nsudo semanage fcontext -a -t httpd_sys_content_t \"/srv/www\"     # ❌\n```\n**不写正则的话，只匹配目录本身，里面的文件管不到** —— 症状就是「目录能进、文件 403」。正确写法：\n```bash\nsudo semanage fcontext -a -t httpd_sys_content_t \"/srv/www(/.*)?\"\nsudo restorecon -Rv /srv/www     # ★ 还必须刷一遍标签，两步缺一不可\n```\n\n**相关的一族命令**：\n| 命令 | 用途 |\n|---|---|\n| `semanage fcontext -l` | 列出所有文件上下文规则 |\n| `semanage port -a -t http_port_t -p tcp 8080` | **给端口打标签**（改服务端口时要）|\n| `semanage boolean -l` | 列出所有布尔开关 |\n| `restorecon -Rv 目录` | 按策略刷新文件标签 |\n| `ls -Z 文件` | 看文件的 SELinux 标签 |"
            }
        ]
    },
    {
        "title": "SELINUX=disabled 有什么代价",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "SELinux",
            "disabled",
            "permissive",
            "第 09 讲"
        ],
        "choices": [
            "没什么代价，只是省事",
            "新建的文件全都没有标签；日后想再启用要全盘 relabel，可能开不了机",
            "只影响防火墙",
            "会让系统变慢"
        ],
        "source_section": "第 09 讲 · 系统安全管理",
        "statement_md": "嫌 SELinux 麻烦，把 `/etc/selinux/config` 改成 `SELINUX=disabled`。会有什么代价？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**代价很大，而且会积累 —— 到你想启用时才爆发。**\n\n**问题链条**：\n1. SELinux 关闭期间，所有**新建/修改的文件都没有安全标签**\n2. 哪天你想重新启用 → 系统**不认这些无标签的文件** → 连开机都起不来（启动早期就被拦）\n3. 唯一的解法是**全盘重新打标签**：\n```bash\nsudo touch /.autorelabel\nsudo reboot\n```\n★ 这会给**整个文件系统每一行**重打标签，几百 GB 的盘可能要跑**几十分钟到几小时**，期间系统不可用。\n\n**正确做法：要宽松就用 `permissive`，不要 `disabled`**\n```\nSELINUX=permissive     # 只记录违规、不阻止 —— 日志里有 AVC，但服务照跑\n```\n★ `permissive` 下文件**仍然会被打标签**，所以日后切回 `enforcing` 只要改一个词 + 重启，不用 relabel。\n\n**还有一条更重要的认知**（第 09 讲反复讲）：\n> **`setenforce 0` 是诊断手段，不是解决方案。**\n\n正确流程是「先看 AVC 日志搞清楚它在拦什么 → 针对性放行」：\n```bash\nsudo ausearch -m avc -ts recent      # ★ 必须 sudo，否则误判「没有 AVC」\nsudo journalctl -t setroubleshoot\n```\n★ **另外**：遇到 403 就 `chmod -R 777` **对 SELinux 引起的 403 完全无效** —— 那是第二关，DAC 权限早就过了。"
            }
        ]
    },
    {
        "title": "firewall-cmd --permanent 之后立刻生效吗",
        "subject": "linux",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 3,
        "total_score": 8,
        "tags": [
            "firewall-cmd",
            "permanent",
            "reload",
            "第 09 讲"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 09 讲 · 系统安全管理",
        "statement_md": "`sudo firewall-cmd --permanent --add-service=http` 执行后，规则会立刻生效。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "错",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|错\n|错误\n|×\n|F\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**错**。`--permanent` 写的规则进的是**永久配置**，**不会立即作用到当前运行时的防火墙**。\n\n需要再执行一次**重载**：\n```bash\nsudo firewall-cmd --permanent --add-service=http\nsudo firewall-cmd --reload         # ★ 不加这步，现在还是访问不了\n```\n\n★ **为什么这么设计**：`--permanent` 是为「下次启动」准备的配置；运行时的规则是另一套内存态。这样你在改配置的过程中，正在跑的服务**不会被打断**。\n\n**两类操作对照**：\n| 命令 | 生效时机 | 重启后 |\n|---|---|---|\n| `firewall-cmd --add-service=http`（不带 --permanent）| **立刻** | ❌ 丢失 |\n| `firewall-cmd --permanent --add-service=http` | **不立刻** | ✅ 保留 |\n| 两条都写（推荐）| 立刻 + 保留 | ✅ |\n\n**怎么验证**：\n```bash\nsudo firewall-cmd --list-services            # 当前运行时\nsudo firewall-cmd --permanent --list-services  # 永久配置\nsudo firewall-cmd --list-all                  # 综合视图（含 zone）\n```\n\n**Workstation 的一个现实**：Fedora Workstation 的默认区域**已经放行了 ssh**，所以 `--add-service=ssh` 是多余的 —— 先 `--list-services` 看一眼再决定要不要加。"
            }
        ]
    },
    {
        "title": "改 sshd_config 的正确流程",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "sshd_config",
            "sshd -t",
            "reload",
            "第 09 讲"
        ],
        "choices": [
            "直接 systemctl restart sshd",
            "先 sudo sshd -t 校验语法，再 systemctl reload sshd",
            "直接 reboot",
            "不用做什么，自动生效"
        ],
        "source_section": "第 09 讲 · 系统安全管理",
        "statement_md": "你想改 SSH 端口并禁用密码登录。改完 `/etc/ssh/sshd_config` 之后，正确的下一步是？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**先校验、再重载 —— 顺序不能颠倒。**\n\n```bash\nsudo sshd -t                    # ★ 只做语法检查，不改变任何东西\nsudo systemctl reload sshd      # 校验通过才重载\n```\n\n★ **为什么必须校验**：`sshd_config` **错一个字符**（比如把 `Port` 打成 `Prot`，或者漏个引号），`restart` 就会**直接失败**。而你多半是**通过 SSH 连过去改的** —— 服务一停，你的连接断了，**再也连不回去**，只能去机房（或虚拟化控制台）救。\n\n**`reload` 而不是 `restart`**：\n| | 行为 |\n|---|---|\n| `restart` | **停掉再起** —— 现有连接全断 |\n| **`reload`** | 重新读配置，**现有连接不受影响** |\n\n（`sshd` 的 reload 会优雅处理：老连接保持，新连接用新配置。）\n\n**两个保命习惯**：\n1. **改 sshd 配置前，先留一个已经登录的会话别关** —— 新会话连不上时，还能用老会话改回来\n2. **改 PAM 之前更要留 root 会话** —— PAM 配错会让**所有账号**（图形 + SSH）都登不进去，只能进单用户模式救援"
            }
        ]
    },
    {
        "title": "pam_tally2 在新系统上还能用吗",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 5,
        "total_score": 10,
        "tags": [
            "pam",
            "authselect",
            "faillock",
            "第 09 讲"
        ],
        "choices": [
            "正常生效",
            "pam_tally2 已被移除，要用 pam_faillock（authselect enable-feature with-faillock）",
            "要装 pam-tally2 包",
            "参数要改成新格式"
        ],
        "source_section": "第 09 讲 · 系统安全管理",
        "statement_md": "你想做「登录失败多次就锁定账号」，照老教程配 `pam_tally2`。在 Fedora 44 上会怎样？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`pam_tally2` 已经被移除**，新系统用 **`pam_faillock`**。\n\n```bash\nsudo authselect enable-feature with-faillock\n```\n\n★ **用 `authselect` 而不是直接改 PAM 文件** —— 这是 Fedora 28+ 的规矩：\n```\n你在 /etc/pam.d/system-auth 里手改的内容\n        ↓\n下一次 authselect 一跑，全被覆盖掉\n```\n正路是 `authselect enable-feature ...`，它会帮你把改动**生成**进配置文件。\n\n**第 09 讲列的 PAM 相关变更（都是「老教程不适用了」的例子）**：\n\n| 老写法 | 现在的做法 |\n|---|---|\n| 手改 `/etc/pam.d/system-auth` | `authselect enable-feature` |\n| `pam_tally2` | **`pam_faillock`** |\n| 改 `/etc/login.defs` 的 `PASS_MIN_LEN` 限密码长度 | **此项已废弃**，密码长度由 `pam_pwquality` 管 |\n\n**另一个反直觉的点**（`pam_pwquality` 的配置）：\n```\ndcredit = -1     # 负数是「至少 N 个」，不是「减分」\n                 # 所以 -1 = 至少要有 1 个数字\nucredit = 1      # 正数是「有就加分」\n```\n**正负含义和直觉相反** —— 这是第 09 讲点名的坑。"
            }
        ]
    },
    {
        "title": "setenforce 0 是不是解决方案",
        "subject": "linux",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 3,
        "total_score": 8,
        "tags": [
            "setenforce",
            "SELinux",
            "诊断",
            "第 09 讲"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 09 讲 · 系统安全管理",
        "statement_md": "服务被 SELinux 拦住了，执行 `setenforce 0` 让它跑起来，问题就解决了。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "错",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|错\n|错误\n|×\n|F\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**错**。`setenforce 0` 只是**诊断手段**，不是解决方案。\n\n**它做了什么**：把 SELinux 从 `enforcing`（强制执行）临时切到 `permissive`（只记录不阻止）。\n\n**两个问题**：\n1. **它只是把防盗门拆了** —— 程序的问题一个都没解决，只是不再被拦了。攻击面反而变大了\n2. **它是临时的** —— 重启就恢复成 `enforcing`，到时候同样的问题会**再冒出来一次**，而你可能已经忘了是为什么\n\n**正确流程**：\n```bash\n# ① 先看看到底在拦什么\nsudo ausearch -m avc -ts recent\nsudo journalctl -t setroubleshoot\n\n# ② 针对性放行（三选一，按场景）\nsudo setsebool -P httpd_can_network_connect on      # 布尔开关\nsudo semanage fcontext -a -t httpd_sys_content_t \"/srv/www(/.*)?\"  # 文件标签\nsudo semanage port -a -t http_port_t -p tcp 8080    # 端口标签\nsudo restorecon -Rv /srv/www\n```\n\n**`setenforce 0` 什么时候可以用**：\n- **验证「这个故障是不是 SELinux 引起的」** —— 如果切到 permissive 就好了，那基本确认是它\n- 然后**切回 enforcing**（`sudo setenforce 1`），再按上面的方式正式修\n\n★ **用 `ausearch` 别忘了 sudo** —— 审计日志属 root，普通用户跑会**空输出**，然后你就会误判成「没有 AVC 记录」。"
            }
        ]
    },
    {
        "title": "make install 之后为什么 GRUB 里没有新内核",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 5,
        "total_score": 10,
        "tags": [
            "内核编译",
            "make install",
            "kernel-install",
            "第 10 讲"
        ],
        "choices": [
            "编译失败了",
            "make install 在 Fedora 上不会建启动项 —— 它是给 LILO 时代写的",
            "要 sudo 才行",
            "GRUB_TIMEOUT 太短看不见"
        ],
        "source_section": "第 10 讲 · Linux 系统的定制",
        "statement_md": "你编译完内核，跑了 `make install`，屏幕上最后出现一句：\n\n```\nCannot find LILO.\n```\n\n重启后 GRUB 菜单里**没有新内核**。为什么？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`make install` 在 Fedora 上装不出启动项** —— 那句 `Cannot find LILO.` 就是证据。\n\n**LILO 是什么**：一个**上世纪**的引导程序，早就被 GRUB 取代了。内核源码树的 `make install` 目标还是按老流程写的：先找 LILO，找不到就打印这句，然后**默默结束**（不报错、不退出非零）。\n\n**更麻烦的是它还会把文件拷乱**：\n`make install` 会把内核拷成 **`/boot/vmlinuz`（不带版本号）**，还会把原来的 `/boot/vmlinuz` 挪成 `vmlinuz.old` —— 这套**没版本号**的命名体系会破坏 Fedora 原有的`vmlinuz-<版本>` 结构，日后排查内核问题时一片混乱。\n\n**正确做法（Fedora 的两条正路）**：\n\n**① 用 `kernel-install`**（推荐）\n```bash\nsudo make modules_install\nsudo kernel-install add <版本号> /path/to/bzImage\n# 它会自动生成 initramfs（经 50-dracut.install 钩子）\n# 并在 /boot/loader/entries/ 下建好 BLS 条目 → GRUB 里就有了\n```\n\n**② 打成 RPM**（最规范，可被 dnf 管理）\n```bash\nfedpkg local     # 产出 kernel-*.rpm，然后 dnf install 它\n```\n\n**验证**：`sudo grubby --info=ALL` 看有没有你的版本。"
            }
        ]
    },
    {
        "title": "编译内核该用哪个用户",
        "subject": "linux",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 4,
        "total_score": 8,
        "tags": [
            "内核编译",
            "权限",
            "-j2",
            "第 10 讲"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 10 讲 · Linux 系统的定制",
        "statement_md": "编译内核需要用 root 身份，否则会有权限问题。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "错",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|错\n|错误\n|×\n|F\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**错，正好相反：编译要用普通用户，只有最后安装才 sudo。**\n\n**为什么不能全程 root**：编译过程中会生成**几万个中间文件**，如果全程 root，这些文件**属主全是 root**。后果：\n- 之后你用普通用户想清理、重新配置，处处 `Permission denied`\n- 想删掉整个源码目录都得 `sudo rm -rf`\n- 一次踩坑，后面每一步都被卡\n\n**正确分界**：\n```bash\n# 普通用户身份做这些\ncp /boot/config-$(uname -r) .config\nmake olddefconfig\nmake -j2\n\n# 只有这两步 sudo\nsudo make modules_install\nsudo kernel-install add ...\n```\n\n★ **顺带两个编译相关的准备**（第 10 讲的必查项）：\n\n| 准备 | 要求 | 不满足会怎样 |\n|---|---|---|\n| **磁盘空间** | `/` 留 **25~30 GB**，`/boot` 留 500 MB | 编到 80% 报 `No space left on device`，**全部白干** |\n| **内存** | ≤ 4 GB 用 **`-j2`**，别 `-j$(nproc)` | `gcc: fatal error: Killed signal terminated program cc1` —— ★ **看着像代码错，其实是 OOM 被杀了** |\n\n（`make -j$(nproc)` 在内存不够的机器上是经典陷阱：并行度按 CPU 核数算，但 GCC 每个进程都吃几百 MB 内存。）"
            }
        ]
    },
    {
        "title": "编译内核第一步该做什么",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "内核配置",
            "olddefconfig",
            "第 10 讲"
        ],
        "choices": [
            "直接 make menuconfig，从头配",
            "cp /boot/config-$(uname -r) .config 然后 make olddefconfig",
            "先 make mrproper",
            "先 make modules_install"
        ],
        "source_section": "第 10 讲 · Linux 系统的定制",
        "statement_md": "你下载了内核源码，解压后进了目录。**配置菜单（menuconfig）之前**第一步应该做什么？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**第一步永远是：拿现有内核的配置当底子。**\n\n```bash\ncp /boot/config-$(uname -r) .config      # 用当前能跑的内核配置\nmake olddefconfig                        # 新增项按默认值补上\n```\n\n★ **为什么不能从零配**：从 `defconfig` 从零起步，编出来的内核**能启动，但你的网卡、声卡、无线全没了** —— 甚至直接 panic。因为 `defconfig` 只是个「最小可用」模板，**不认识你这台机器的硬件**。\n\n★ **为什么用 `olddefconfig` 而不是 `oldconfig`**：\n| 命令 | 行为 |\n|---|---|\n| `make oldconfig` | 对每个新增选项**逐条问你**（几百个问题）|\n| **`make olddefconfig`** | 新增项**直接用默认值**，不问你 ✅ |\n\n「一路瞎回车」用 `oldconfig` 是第 10 讲点名的坑：配置里会混进大量你不知道的默认值，编出来和预期完全不一样。\n\n★ **`make mrproper` 千万别随便用** —— 它会**连 `.config` 一起删掉**！想清理编译产物用 **`make clean`**（只删中间文件，保留 `.config`）。\n\n**配完**：`grep 你的选项 .config` 确认改动真的写进去了（改了 menuconfig 忘了保存也是常见坑）。"
            }
        ]
    },
    {
        "title": "编译到 80% 报 Killed signal terminated program cc1",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "内核编译",
            "OOM",
            "-j2",
            "第 10 讲"
        ],
        "choices": [
            "代码有语法错误",
            "内存不足，cc1 被 OOM killer 杀了",
            "gcc 版本太老",
            "硬盘坏了"
        ],
        "source_section": "第 10 讲 · Linux 系统的定制",
        "statement_md": "编译内核时突然报：\n\n```\ngcc: fatal error: Killed signal terminated program cc1\n```\n\n看起来像编译器崩了。真实原因最可能是？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**内存不足，`cc1` 进程被 OOM killer 杀了。**\n\n★ **这个报错极具迷惑性**：它打着 `gcc: fatal error` 的旗号，看着像「代码写错了」，实际是**系统内存不够** —— 内核的 OOM killer 把占内存最多的 `cc1`（GCC 的编译进程）干掉了。\n\n**怎么确认**：\n```bash\nfree -h                    # 看 available\ndmesg | grep -i 'killed process'   # ★ 能看到 OOM 的记录，证据确凿\n```\n\n**怎么解决**：\n```bash\nmake -j2                   # ★ 降低并行度（每个编译进程吃几百 MB）\n# 内存 ≤ 4 GB 就别用 -j$(nproc)\n```\n\n★ **`-j$(nproc)` 为什么危险**：它按**CPU 核数**开并行任务。8 核就同时跑 8 个编译进程 —— 每个吃 500 MB 就是 4 GB。再加上系统本身的开销，16 GB 的机器都可能被压垮。\n\n**配套的另一个编译前检查**（第 10 讲 A 组第 1 条）：\n```bash\ndf -h /        # ★ / 要留 25~30 GB\ndf -h /boot    # ★ /boot 要留 500 MB\n```\n空间不够的表现是「编到 80% 报 `No space left on device`」—— 同样是**全部白干**，而且是最气人的一种失败。"
            }
        ]
    },
    {
        "title": "uname -r 没变，是编译失败了吗",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 5,
        "total_score": 10,
        "tags": [
            "内核",
            "grubby",
            "启动项",
            "第 10 讲"
        ],
        "choices": [
            "是的，要重新编译",
            "不一定 —— 新内核可能装了，但默认启动项还是旧的",
            "是因为没跑 depmod",
            "是因为没生成 initramfs"
        ],
        "source_section": "第 10 讲 · Linux 系统的定制",
        "statement_md": "你编译安装了新内核，重启后 `uname -r` 显示的还是旧版本号。说明编译失败了？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**不一定。最常见的原因是「新内核装了，但默认启动项没切过去」。**\n\n**先确认新内核到底装上没**：\n```bash\nsudo grubby --info=ALL              # ★ 列出所有启动项，看有没有你的版本\nls /boot/vmlinuz-*                  # 看文件在不在\nls /lib/modules/                    # 看模块目录有没有新版本\nls /boot/loader/entries/            # Fedora 的 BLS 启动条目\n```\n\n**如果在，就手动切默认启动项**：\n```bash\nsudo grubby --set-default /boot/vmlinuz-<完整版本号>\n```\n★ **必须用 `grubby --info=ALL` 输出里的完整 kernel 路径** —— 写个不带版本号的名字 grubby 找不到，会报错或者干脆没反应。\n\n**另外两个「看起来像失败」的正常现象**：\n| 现象 | 真相 |\n|---|---|\n| GRUB 菜单一闪而过，来不及选 | `GRUB_TIMEOUT` 是 0。改 `/etc/default/grub` 调到 5 秒以上，再 `grub2-mkconfig` |\n| 新内核起来了，但硬件大面积失效 | `make modules_install` 忘了跑 → `ls /lib/modules/<版本>/` 是空的 |\n\n★ **一条不能违背的规矩**：`installonly_limit` **保持默认值 3**。调成 1 的话，装新内核时**旧内核被自动删掉** —— 一旦新内核有问题，你就**没有任何退路**了。\n查：`dnf config-manager getopt installonly_limit`"
            }
        ]
    },
    {
        "title": "条件测试里变量不加引号会怎样",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "shell",
            "条件判断",
            "引号",
            "第 11 讲"
        ],
        "choices": [
            "什么都不输出，判断为假",
            "bash: [: =: unary operator expected",
            "bash: [: missing ']'",
            "bash: v: unbound variable"
        ],
        "source_section": "第 11 讲 · Shell 程序设计",
        "statement_md": "脚本里写 `[ $v = x ] && echo yes`，而变量 `v` 从未赋值。bash 会输出什么？\n\n（提示：`[` 在这里不是语法，是一条命令。）",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`[` **是一条命令**（等价于 `test`），不是语法。\n\n`$v` 展开成空串之后，这一行变成了：\n```\n[ = x ]\n```\n命令 `[` 收到两个参数 `=` 和 `x`。它按「两个参数」的规则去解释，发现第一个参数 `=` **不是一个合法的一元运算符**，就报错退出：\n```\nbash: [: =: unary operator expected\n```\n\n★ **修法只有一个：给变量加双引号** —— `[ \"$v\" = x ]`。\n展开后变成 `[ \"\" = x ]`，命令 `[` 收到三个参数，走「二元比较」规则，合法，判为假。\n\n★ 这条是「90% 的 shell 玄学问题都出在没加引号」的典型案例。如果你想彻底避开这类坑，用 `[[ ]]` —— 它是**语法**，不做分词也不做 glob，`[[ $v = x ]]` 里 `$v` 为空也不会报错。"
            }
        ]
    },
    {
        "title": "双方括号里的 > 是数值比较吗",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "shell",
            "条件判断",
            "字符串比较",
            "第 11 讲"
        ],
        "choices": [
            "big",
            "small",
            "报语法错误",
            "取决于系统 locale"
        ],
        "source_section": "第 11 讲 · Shell 程序设计",
        "statement_md": "`if [[ 10 > 9 ]]; then echo big; else echo small; fi` 会打印什么？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**打印 `small`。** `[[ ]]` 里的 `>` 和 `<` 做的是**字符串比较**（字典序），不是数值比较。\n\n`\"10\"` 和 `\"9\"` 从左往右比第一个字符：`'1'` (0x31) < `'9'` (0x39) → 所以 `[[ 10 > 9 ]]` 是**假**。\n\n| 想做的事 | 正确写法 |\n|---|---|\n| 数值比较 | `[[ 10 -gt 9 ]]` 或 `(( 10 > 9 ))` |\n| 字符串比较 | `[[ 10 > 9 ]]` |\n\n★ 顺带一个更凶的坑：**同样写法放进 `[ ]` 里会变成重定向**。\n`[ 10 > 9 ]` 里的 `>` 会被 shell 当成「把输出写进文件 9」，于是当前目录凭空多出一个叫 `9` 的空文件，而判断结果还莫名其妙。\n\n**规律**：`[[ ]]` 内部不重定向、不做分词，是「语法级」的判断；`[ ]` 是普通命令，里面的一切先被 shell 处理一遍。"
            }
        ]
    },
    {
        "title": "管道里的 while 为什么改变不了外面的变量",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "shell",
            "管道",
            "子shell",
            "第 11 讲"
        ],
        "choices": [
            "3",
            "0",
            "报错 unbound variable",
            "1"
        ],
        "source_section": "第 11 讲 · Shell 程序设计",
        "statement_md": "`n=0; seq 3 | while read x; do n=$((n+1)); done; echo $n` 输出什么？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**输出 `0`。** 管道两侧**各在一个子 shell 里跑**，`while` 循环改的 `n` 只活在那个子 shell 里，循环一结束就随子 shell 一起没了。\n\n父 shell 里的 `n` 从头到尾都是 0。\n\n★ 这是 shell 里最典型的「变量设了却出不来」的成因。三种修法：\n\n```bash\n# ① 输入重定向（最常用）—— 循环回到当前 shell 跑\nwhile IFS= read -r x; do n=$((n+1)); done < <(seq 3)\n\n# ② 只把「产生数据」的那步放进管道\nwhile IFS= read -r x; do n=$((n+1)); done < <(seq 3)\n\n# ③ 让子 shell 自己把结果打出来，外面接住\nn=$(seq 3 | wc -l)\n```\n\n⚠️ `for f in $(ls) | ...`、`cmd | while` 都是同一类问题。**判断口诀：管道右侧的整条命令，都在子 shell 里。**"
            }
        ]
    },
    {
        "title": "local 会吞掉命令替换的退出码",
        "subject": "linux",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 4,
        "total_score": 8,
        "tags": [
            "shell",
            "函数",
            "退出码",
            "第 11 讲"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 11 讲 · Shell 程序设计",
        "statement_md": "在函数里写 `local n=$(false)`，紧接着 `echo $?` 会打印 `0`。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "对",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|对\n|正确\n|√\n|T\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**对。** `local` 本身是一条命令，它自己的退出码（成功 = 0）**覆盖**了命令替换里那条命令的退出码。\n\n所以 `local x=$(cmd)` 之后 `$?` 恒为 0 —— 不管 `cmd` 成功还是失败。\n\n★ 这个坑的后果很隐蔽：`set -e` 不会因为 `cmd` 失败而终止，错误处理分支也永远进不去。\n\n**正确写法**（两条语句分开）：\n```bash\nlocal n\nn=$(cmd) || return 1\n```\n\n★ 同类坑还有 `declare x=$(cmd)`、`export x=$(cmd)` —— 凡是「带赋值能力的命令 + 命令替换」都要当心。"
            }
        ]
    },
    {
        "title": "for f in $(ls) 遇到含空格的文件名",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "shell",
            "循环",
            "glob",
            "分词",
            "第 11 讲"
        ],
        "choices": [
            "2 行",
            "3 行",
            "1 行",
            "报错"
        ],
        "source_section": "第 11 讲 · Shell 程序设计",
        "statement_md": "目录里有 `a 1.md` 和 `b.md` 两个文件。\n\n`for f in $(ls); do echo \"[$f]\"; done` 会打印几行？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**3 行。** `$(ls)` 的结果会**按 `IFS`（默认含空格）分词** —— `a 1.md` 被切成 `a` 和 `1.md` 两个词，加上 `b.md` 就是 3 行。\n\n```\n[a]\n[1.md]\n[b.md]\n```\n\n★ 这是「文件名含空格」类事故的头号成因 —— 在 `rm`/`mv` 上就是**删错文件**。\n\n**正解：用 glob，别用 `$(ls)`**\n```bash\nfor f in *.md; do echo \"[$f]\"; done    # 2 行\n```\nglob 由 shell 直接展开，**每个文件名是一个整体**，不会再分词。\n\n⚠️ 顺带两个配套：glob 无匹配时会把 `*.md` 原样当文件名 → 循环里加 `[ -e \"$f\" ] || continue`，或 `shopt -s nullglob`。"
            }
        ]
    },
    {
        "title": "给变量设默认值怎么写",
        "subject": "linux",
        "line": "text",
        "question_type": "fill_blank",
        "difficulty": 3,
        "total_score": 12,
        "tags": [
            "shell",
            "变量",
            "参数扩展",
            "第 11 讲"
        ],
        "choices": [],
        "source_section": "第 11 讲 · Shell 程序设计",
        "statement_md": "要求：变量 `v` **为空或未定义**时用字符串 `fallback` 顶上，其他情况用 `v` 自己的值。\n\n请写出这个**参数扩展**表达式（只写表达式本身，不要写 echo、不要写赋值）。\n\n形如 `${变量:-默认值}`，注意中间那个冒号不能少。",
        "input_format": "",
        "output_format": "一行答案（不要写解释、不要写命令提示符）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "${v:-fallback}",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|${v:-fallback}\n|${v:-fallback}\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`${v:-fallback}`** —— 冒号 `:` 的意思是「**为空或未定义**都算」。\n\n| 写法 | 何时替换 |\n|---|---|\n| `${v:-fallback}` | v **未定义** 或 v **为空串** |\n| `${v-fallback}` | 只有 v **未定义**时（为空时不替换）|\n\n**差一个冒号，语义就不一样** —— 这是参数扩展里最常见的记混点。\n\n同一族还有几个必须认识的：\n```bash\n${v:=fallback}    # 为空/未定义时替换，并且把结果写回 v\n${#v}             # v 的长度\n${v%.txt}         # 去掉末尾的 .txt（最短匹配）\n${v%.*}           # 去掉最后一个后缀名\n${v//a/b}         # 把 v 里所有 a 换成 b\n${v:2:5}          # 从第 3 个字符起取 5 个\n```\n\n★ 参数扩展是第 11 讲分量最重的一节（★★★）—— 它能在**不启动任何子进程**的前提下做掉一大堆字符串处理。"
            }
        ]
    },
    {
        "title": "gcc 的 -c 停在哪一步",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "gcc",
            "编译流程",
            "-c",
            "第 12 讲"
        ],
        "choices": [
            "预处理后停下，产出 hello.i",
            "编译后停下，产出 hello.s（汇编）",
            "汇编后停下，产出 hello.o（目标文件）",
            "一路走到链接，产出可执行文件 hello"
        ],
        "source_section": "第 12 讲 · GCC 的使用与开发",
        "statement_md": "GCC 把「源码 → 可执行文件」分成四道工序。`gcc -c hello.c` 会停在哪儿、产出什么？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "C",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|C\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`-c` 停在第三道工序（汇编），产出目标文件 `.o`。**\n\n```\nhello.c\n  │ -E  预处理（cpp）      → hello.i   纯 C 源码\n  │ -S  编译（cc1）        → hello.s   汇编\n  │ -c  汇编（as）         → hello.o   目标文件  ← 停在这里\n  │     链接（ld）         → hello     可执行文件\n```\n\n★ **记法：三个选项对应「停在前三道工序」，不加选项才走到第四道。**\n\n为什么要能分步？因为**报错的责任人不同**：\n\n| 出错阶段 | 典型报错 | 问题在哪 |\n|---|---|---|\n| ①②③ 编译期 | `error: expected ';'` / `No such file or directory` | 语法、类型、缺头文件 |\n| ④ 链接期 | `undefined reference` / `multiple definition` | 名字找不到 |\n\n★ 分步还很实用：**只改了某一个 `.c` 时，只需重编那一个 `.o`，再链接** —— 这正是 `make` 增量构建干的事。"
            }
        ]
    },
    {
        "title": "-I、-L、-l 各管什么",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "gcc",
            "选项",
            "-I",
            "-L",
            "-l",
            "第 12 讲"
        ],
        "choices": [
            "-Linclude",
            "-Iinclude",
            "-linclude",
            "-Winclude"
        ],
        "source_section": "第 12 讲 · GCC 的使用与开发",
        "statement_md": "编译时报 `fatal error: mylib.h: No such file or directory`，头文件在项目下的 `include/` 目录里。应该加哪个选项？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`-Iinclude`**（大写字母 `I`，是 Include 的首字母）。\n\n三个长得像的选项，分工完全不同 —— **敲错一个字母，报错完全看不懂**：\n\n| 选项 | 管什么 | 例子 |\n|---|---|---|\n| **`-I`**（大写 i） | 头文件的**搜索目录** | `-Iinclude` |\n| **`-L`** | 库文件的**搜索目录** | `-L/usr/local/lib` |\n| **`-l`**（小写 L） | 要链接的**库名** | `-lm`（连 libm） |\n\n★ 两条配套规矩：\n1. **`-I` / `-L` 后面直接跟目录，没有等号** —— `-I=include` 是**不合法**的写法。\n2. `-l` 写的是**去掉 `lib` 前缀和扩展名**的名字：`libm.so` → `-lm`。\n\n★ 链接顺序也归这条管：**`-L` 必须写在 `-l` 之前**（`-L` 只影响它**之后**出现的 `-l`），而 `-l` 必须写在「用到它的那个 `.o`」**之后**。"
            }
        ]
    },
    {
        "title": "-l 写在 .o 前面会怎样",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "gcc",
            "链接",
            "-l",
            "顺序",
            "第 12 讲"
        ],
        "choices": [
            "正常链接成功",
            "报 undefined reference（找不到符号）",
            "报 multiple definition",
            "报找不到库目录 lib"
        ],
        "source_section": "第 12 讲 · GCC 的使用与开发",
        "statement_md": "静态库 `libmyadd.a` 放在 `./lib/` 下，`main.o` 用了它的函数。\n\n`gcc -Llib -lmyadd main.o -o app` 会？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**报 `undefined reference`。** 链接器（ld）**只从左往右扫一遍**：\n\n1. 扫到 `-lmyadd` 时，它去库里找「**目前还没被满足的符号**」—— 可此刻一个都还没有（还没看到 `main.o`）→ **从库里什么都没取**；\n2. 再扫到 `main.o`，这时才冒出一堆「未定义的符号」；\n3. 但库**已经在身后了**，链接器不会回头。\n\n于是最终报：`undefined reference to 'myadd'`。\n\n★ **口诀：依赖者在前，被依赖者在后。**\n```bash\ngcc -Llib main.o -lmyadd -o app      # ✅\ngcc main.o -Llib -lmyadd -o app      # ✅（-L 在 -l 之前就行）\ngcc -Llib -lmyadd main.o -o app      # ❌ undefined reference\n```\n\n★ **同一个库、同一个 `.o`，只换顺序就成败两样** —— 报错看起来像「库坏了」或「函数名写错了」，其实纯粹是顺序问题。\n第 13 讲的 GTK 程序里，这个坑会以「一屏几十行 `undefined reference`」的形式回来。"
            }
        ]
    },
    {
        "title": "-Wno-xxx 该放在哪",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "gcc",
            "-Wall",
            "-Wno-",
            "第 12 讲"
        ],
        "choices": [
            "警告被成功关掉",
            "警告照旧出现（后写的 -Wall 把它又打开了）",
            "报未知选项，编译失败",
            "编译通过，但程序行为改变"
        ],
        "source_section": "第 12 讲 · GCC 的使用与开发",
        "statement_md": "想关掉 `-Wall` 带出来的 `unused-parameter` 警告，写成 `gcc -Wno-unused-parameter -Wall x.c`。结果？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**警告照旧。** GCC 的规则是「**后者覆盖前者**」—— `-Wno-unused-parameter` 先被执行，紧接着 `-Wall` 又把 `unused-parameter` 这一类打开了。\n\n★ **规矩：`-Wno-` 永远写在最后。**\n```bash\ngcc -Wall -Wextra -Wno-unused-parameter x.c    # ✅\ngcc -Wno-unused-parameter -Wall x.c            # ❌ 白写\n```\n\n★ 为什么值得专门记这一条：**默认编译下，严重问题一个警告都不给。**\n讲义里实测过三处：未检查 `malloc` 返回值、double free、内存泄漏 —— 不加 `-Wall` 全部静默通过。\n\n★ 再补两条同族的：\n- **`-Werror` 不要写进项目的默认 `CFLAGS`** —— 编译器一升级就会多出新警告，于是**别人**编不过你的代码。自己作业里用可以，发给别人时只在 CI 里用。\n- `-Wall` 只是「一大把常用警告」的集合，**不是「全部警告」**，配合 `-Wextra` 才接近「该报的都报」。"
            }
        ]
    },
    {
        "title": "为什么 -O2 -g 下断点不命中",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "gcc",
            "-O2",
            "gdb",
            "调试",
            "第 12 讲"
        ],
        "choices": [
            "gdb 版本太旧，认不出新的调试信息格式",
            "优化把函数内联、变量放进寄存器，已经没有「能设断点的代码位置」",
            "-g 没生效，根本没生成调试信息",
            "必须用 -static 才能下断点"
        ],
        "source_section": "第 12 讲 · GCC 的使用与开发",
        "statement_md": "用 `-O2 -g` 编译后，在 gdb 里 `break sum_to` 打断点，程序跑完了**一次都没停**。原因？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**优化把函数「弄没了」。** `-O2` 会做**内联、常量折叠、循环展开、向量化** —— 你写的 `sum_to` 很可能被**整个内联进调用点**，函数的代码边界在二进制里根本不存在了，断点自然没有落脚的地方。\n\n★ 同一个原因还会导致「变量显示 `optimized out`」、单步乱跳、`print` 出来的值和源码对不上。\n\n| 用途 | 该用什么 |\n|---|---|\n| 调试 | **`-O0 -g`** 或 **`-Og -g`**（`-Og` = 为调试保留结构的优化档）|\n| 发布 | `-O2`（不要带 `-g`）|\n| 要体积小 | `-Os` |\n\n★ 两个常见误解：\n- **`-O2` 不一定让文件变小** —— 内联、展开、向量化都会让代码**变多**。\n- **`-O0` 能复现、`-O2` 不复现，就改用 `-O0` 编译了事** —— 那是在**藏炸弹**。这种差异几乎一定是未定义行为（越界 / 未初始化 / 有符号溢出），该用 `-fsanitize=address,undefined` 把它逼出来修掉。"
            }
        ]
    },
    {
        "title": "大写 .S 会先过预处理器",
        "subject": "linux",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 3,
        "total_score": 8,
        "tags": [
            "gcc",
            "汇编",
            "后缀",
            "第 12 讲"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 12 讲 · GCC 的使用与开发",
        "statement_md": "GCC 里 `.S`（大写）后缀的汇编文件会先经过预处理器，`.s`（小写）不会。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "对",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|对\n|正确\n|√\n|T\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**对。** 这条大小写差别是 GCC 明确规定的：\n\n| 后缀 | 先过 cpp 吗 | 能写 `#include` / `#define` 吗 |\n|---|---|---|\n| `.s`（小写） | **不** | 不能 —— `#` 开头的行原样交给汇编器 |\n| `.S`（大写） | **会** | 能 |\n\n★ **内核代码里全靠这个区别** —— 汇编文件里要 `#include` 一堆 C 头文件（架构宏、寄存器定义）时，必须用大写 `.S`。\n\n★ 这也解释了一个常见困惑：手写的 `.s` 文件里写 `#define` 为什么「没生效、还报语法错」—— 它压根没被预处理过。"
            }
        ]
    },
    {
        "title": "ar 命令里 rcs 的 s 做什么",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "gcc",
            "静态库",
            "ar",
            "符号索引",
            "第 12 讲"
        ],
        "choices": [
            "生成/更新库的符号索引",
            "保留调试符号",
            "做静态链接",
            "跳过重复的成员文件"
        ],
        "source_section": "第 12 讲 · GCC 的使用与开发",
        "statement_md": "`ar rcs libmyadd.a add.o` —— 三个字母里 `s` 负责什么？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "A",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|A\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`s` = 写符号索引。** 三个字母分别是：\n\n| 字母 | 作用 |\n|---|---|\n| `r` | **R**eplace —— 插入或替换成员（文件已存在就换掉）|\n| `c` | **C**reate —— 库不存在就创建（并抑制「正在创建」的提示）|\n| `s` | **S**ymbol index —— 写/更新符号索引 |\n\n★ **为什么 `s` 不能省**：索引让链接器能**按名字快速定位**符号属于哪个成员。\n缺了索引，链接器在库里找符号就会失败，报出来的却是普通的 `undefined reference to 'xxx'` —— **报错里一个字都不会提「索引」**。\n这条坑因此极难排查。\n\n漏了也能补救（对已有的 `.a` 补索引）：\n```bash\nranlib libmyadd.a\n```\n\n★ 顺手一条：**`.a` 就是把一堆 `.o` 打包**（跟 tar 一个思路），所以它跟 `.so` 完全不是一回事 —— `:a` 在编译期就被整段复制进可执行文件，`:so` 是**另一份独立程序**，运行时要靠 `ld.so` 去找。"
            }
        ]
    },
    {
        "title": "库文件 libmyadd.a 该写哪个 -l",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 2,
        "total_score": 10,
        "tags": [
            "gcc",
            "静态库",
            "-l",
            "命名",
            "第 12 讲"
        ],
        "choices": [
            "-llibmyadd",
            "-lmyadd",
            "-lmyadd.a",
            "-Lmyadd"
        ],
        "source_section": "第 12 讲 · GCC 的使用与开发",
        "statement_md": "静态库文件叫 `libmyadd.a`。链接它时 `-l` 后面写什么？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`-lmyadd`。** `-l` 会**自动补上 `lib` 前缀和扩展名**：\n\n```\n-lmyadd  →  去找 libmyadd.a（静态）或 libmyadd.so（动态）\n```\n\n所以写 `-llibmyadd` 会让它去找 **`liblibmyadd.a`** —— 当然找不到。\n写 `-lmyadd.a` 同理，会变成找 `libmyadd.a.a`。\n\n★ 三个选项的分工再巩固一次：\n```bash\ngcc main.o -L./lib -lmyadd -o app\n#          └─库目录  └─库名（不带 lib / 不带扩展名）\n```\n\n★ 想知道「一个可执行文件到底连了哪些库」，用 **`ldd`**；但要处理**不可信**的文件时改用 `objdump -p 文件 | grep NEEDED` —— `ldd` 在极端实现路径下**会真的执行目标程序**（历史上出过提权漏洞）。"
            }
        ]
    },
    {
        "title": "编动态库时每个 .o 都要 -fPIC",
        "subject": "linux",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 4,
        "total_score": 8,
        "tags": [
            "gcc",
            "动态库",
            "-fPIC",
            "-shared",
            "第 12 讲"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 12 讲 · GCC 的使用与开发",
        "statement_md": "要把若干 `.o` 链接成 `.so`，组成它的**每一个** `.o` 都必须用 `-fPIC` 编译。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "对",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|对\n|正确\n|√\n|T\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**对。** 动态库会被加载到**进程地址空间的任意位置**，所以库里的代码必须是「位置无关」的 —— 这就是 **PIC = Position Independent Code**。\n\n忘了加 `-fPIC` 的报错长这样（很好认）：\n```\nrelocation R_X86_64_32 against `...' can not be used when making\na shared object; recompile with -fPIC\n```\n★ 报错最后一句已经把答案给你了。\n\n★ 容易混淆的一点：**`-fPIC` 和 `-shared` 不是一回事**。\n| 选项 | 作用 | 加在哪 |\n|---|---|---|\n| `-fPIC` | 让**代码**位置无关 | 编 `.o` 时（每一个）|\n| `-shared` | 让**链接器**产出 `.so` | 最后链接那一步 |\n\n★ 另一个常被误解的：`-static` **不是「链接某个静态库的开关」**，而是**整个程序全静态链接**（连 libc 一起打进去）。只想让某一个库静态连：`-Wl,-Bstatic -lfoo -Wl,-Bdynamic`。"
            }
        ]
    },
    {
        "title": "Makefile 的命令行可以用空格缩进",
        "subject": "linux",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 3,
        "total_score": 8,
        "tags": [
            "make",
            "Makefile",
            "TAB",
            "第 12 讲"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 12 讲 · GCC 的使用与开发",
        "statement_md": "Makefile 里命令行用空格缩进就行，只要看起来对齐了。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "错",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|错\n|错误\n|×\n|F\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**错。命令行的缩进必须是 TAB 字符。**\n\n用空格会报：\n```\n*** missing separator. Stop.\n```\n\n★ 这个报错**完全不告诉你是缩进问题**，新手往往去怀疑「规则写错了」「依赖写错了」。\n\n**怎么确认**：把缩进字符直接打出来看：\n```bash\ncat -A Makefile | head\n# TAB 会显示成 ^I，空格就是空格\n```\n\n**怎么避免**：编辑器里把 `.makefile` / `Makefile` 设成「TAB 不转空格」。\n（注意：**变量的赋值行和条件语句不需要 TAB**，只有「规则下面的命令」需要 —— 所以一个文件里会同时出现两种缩进，这是正常的。）\n\n★ 顺带两条 make 的常见坑：\n- `clean` / `all` 这类**伪目标要写 `.PHONY`**，否则目录里真有同名文件时 make 会认为「目标已最新」而**跳过不执行**。\n- **`make -j$(nproc)` 要小心**：并行度按 CPU 核数算，每个 gcc 进程吃几百 MB 内存，小内存机器会被内核 OOM 杀掉（症状是只有 `Killed` 两个字）。降到 `-j2`。"
            }
        ]
    },
    {
        "title": "$@ $< $^ 分别是什么",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "make",
            "自动变量",
            "Makefile",
            "第 12 讲"
        ],
        "choices": [
            "目标 / 第一个依赖 / 全部依赖",
            "第一个依赖 / 目标 / 全部依赖",
            "全部依赖 / 目标 / 第一个依赖",
            "目标 / 全部依赖 / 第一个依赖"
        ],
        "source_section": "第 12 讲 · GCC 的使用与开发",
        "statement_md": "Makefile 里一条规则写成 `app: main.o util.o`。这条规则的命令里，`$@` / `$<` / `$^` 依次代表？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "A",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|A\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`$@` 目标、`$<` 第一个依赖、`$^` 全部依赖。**\n\n| 自动变量 | 含义（就着 `app: main.o util.o` 看）|\n|---|---|\n| `$@` | **目标** → `app` |\n| `$<` | **第一个**依赖 → `main.o` |\n| `$^` | **全部**依赖（去重）→ `main.o util.o` |\n| `$?` | 比目标新的那些依赖 |\n| `$*` | 模式规则里 `%` 匹配到的部分 |\n\n所以最经典的一条规则长这样：\n```make\napp: main.o util.o\n\t$(CC) -o $@ $^        # gcc -o app main.o util.o\n\n%.o: %.c\n\t$(CC) -c -o $@ $<     # gcc -c -o main.o main.c\n```\n\n★ `$@` 和 `$<` **记反了命令会完全跑错**，而且往往「看起来也能跑」——\n因为 `-o` 后面接的如果不是你想要的，可能只是产出一个名字奇怪的文件。\n\n⚠️ 另外提醒：Makefile 里的 `$` 要写 `$$` 才能传给 shell —— `$$HOME` 才是 shell 的 `$HOME`，直接写 `$HOME` 会被 make 当自己的变量。"
            }
        ]
    },
    {
        "title": "单独编译头文件为什么报找不到 main",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "gcc",
            "头文件",
            "链接",
            "第 12 讲"
        ],
        "choices": [
            "头文件里有语法错误",
            "头文件只有声明、不产生目标代码，而且它本来就不含 main",
            "缺少 -I 指定头文件目录",
            "需要先把 add.c 编译出来"
        ],
        "source_section": "第 12 讲 · GCC 的使用与开发",
        "statement_md": "`gcc add.h` 报 `undefined reference to 'main'`。为什么？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**因为头文件是「被包含」的，不是「被编译」的。**\n\n`.h` 里通常只有**声明**（函数原型、宏、类型），真正的**定义**（函数体）在 `.c` 里。把它当源文件喂给 gcc，编译这一关能过，但链接受不了 —— 链接器要找一个程序入口 `main`，而 `.h` 里根本没有。\n\n```\nundefined reference to 'main'\n```\n\n★ 报错里出现的名字**不是 `add`，是 `main`** —— 这一点很关键：\n**链接器在找的是程序入口，不是 `add`。**（讲义里实测过另一半：把 `main` 拼成 `mian`，链接器同样报「找不到 main」，而且报的**不是**「拼写错误」。）\n\n★ 正确的分工：\n```bash\ngcc -c add.c -o add.o      # 编译实现\ngcc -c main.c -o main.o    # 编译调用者\ngcc add.o main.o -o app    # 链接\n```\n\n★ 顺带一条同族的规矩：**头文件里不要写函数体或 `int g;`** —— 每个包含它的 `.c` 都会生成一份定义，链接时报 `multiple definition`。变量在头文件里写 `extern int g;`，定义放进某一个 `.c`。"
            }
        ]
    },
    {
        "title": "GTK4 的 pkg-config 名字是什么",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "gtk",
            "pkg-config",
            "GTK4",
            "第 13 讲"
        ],
        "choices": [
            "gtk+-4.0",
            "gtk4",
            "gtk+4",
            "gtk-4.0"
        ],
        "source_section": "第 13 讲 · GTK 图形界面程序设计",
        "statement_md": "在 Fedora 44 上要拿到 GTK4 的编译参数，`pkg-config --cflags --libs` 后面该写什么？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`gtk4`** —— **没有加号、没有 `.0`。**\n\n三代命名风格完全不同，这是最容易输错的地方：\n\n| 版本 | pkg-config 名字 | devel 包名 |\n|---|---|---|\n| GTK+ 2 | `gtk+-2.0` | `gtk2-devel` |\n| GTK+ 3（教材用的） | **`gtk+-3.0`** | `gtk3-devel` |\n| GTK 4（你的 Fedora 44） | **`gtk4`** | `gtk4-devel` |\n\n★ **看到加号就是 GTK4 之前的东西。** 有意思的是，三代**头文件的名字完全一样**（都是 `<gtk/gtk.h>`）—— 所以「`#include` 写对了却编不过」时，先怀疑 pkg-config 名字写错。\n\n写错了会看到：\n```\nPackage gtk+-4.0 was not found in the pkg-config search path.\n```\n★ 这句话是 **`pkg-config` 自己发的**，不是 gcc —— 别去怀疑编译器。用 `pkg-config --list-all | grep -i gtk` 看实际有哪些。"
            }
        ]
    },
    {
        "title": "几十个 undefined reference 是什么问题",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "gtk",
            "编译",
            "链接",
            "分诊",
            "第 13 讲"
        ],
        "choices": [
            "代码里函数名写错了",
            "漏了 $(pkg-config --libs gtk4)，没连上 GTK 库",
            "没有安装 gtk4-devel 包",
            "gcc 版本太旧"
        ],
        "source_section": "第 13 讲 · GTK 图形界面程序设计",
        "statement_md": "编译一个 GTK 程序，报错有**四十多行**，全是 `undefined reference to 'gtk_xxx'`。最可能的原因是？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**几十年行 GTK 函数未定义 = 配置问题 → 漏了 `$(pkg-config --libs gtk4)`。**\n\n★ 这里有一条**能省一小时的分诊规则**：\n\n| 报错形态 | 结论 |\n|---|---|\n| **一两个**函数未定义 | **代码问题** —— 函数名拼错 / 用了 GTK4 已删的函数 |\n| **几十个** `gtk_xxx` 未定义 | **配置问题** —— 缺 `-lgtk-4` 那一串 |\n| `fatal error: gtk/gtk.h: No such file or directory` | 缺 `$(pkg-config --cflags gtk4)` 或没装 `gtk4-devel` |\n\n**注意报错发生的阶段完全不同**：\n- 找不到头文件 → **编译期**就停了，一行 `fatal error`；\n- 找不到函数 → 编译全过，**链接期**才炸，几十行。\n\n★ 两类问题的根治办法都是**别手敲那一长串参数**：\n```make\nCFLAGS := $(shell pkg-config --cflags gtk4)\nLIBS   := $(shell pkg-config --libs gtk4)\nhello: hello.c\n\t$(CC) $(CFLAGS) hello.c -o $@ $(LIBS)\n```\n\n⭐ 顺带说一句：`pkg-config` 自己的活只有一件事 —— **把一串 `-I` 和一串 `-l` 吐给你**。它读的是 `/usr/lib64/pkgconfig/gtk4.pc` 这种文本文件。看懂 `.pc` 文件，就再也不会被「这个库要怎么连」卡住。"
            }
        ]
    },
    {
        "title": "GTK 的 -l 顺序能不能重排",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "gtk",
            "链接",
            "-l",
            "顺序",
            "第 13 讲"
        ],
        "choices": [
            "没影响，顺序无关",
            "必然报 undefined reference",
            "编译变快",
            "自动改成动态链接"
        ],
        "source_section": "第 13 讲 · GTK 图形界面程序设计",
        "statement_md": "把 `pkg-config --libs gtk4` 吐出来的 `-lgtk-4 -lgdk-4 ... -lglib-2.0` 手工按字母顺序重排一遍，会？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**必然报 `undefined reference`。**\n\n那串顺序是 `pkg-config` 按 `.pc` 文件里的 `Requires` **拓扑排序**出来的，和链接器「从左到右只扫一遍」的规则**严格对应**：\n\n```\nGTK 4  →  依赖 GDK 4  →  依赖 GLib\n-lgtk-4            -lgdk-4            -lglib-2.0\n  （前者必须写在后者的前面）\n```\n\n★ 这和 **第 12 讲的 `-l` 顺序规则是同一件事**：「依赖者在前，被依赖者在后」。第 12 讲你用一个 `.a` 亲手撞过，这里只是放大成「四十行报错」。\n\n★ **好消息**：`pkg-config` 吐出来的顺序**已经排好了**，你只要**别自己重排**就行。真正要守的只有一条：\n```make\n\t$(CC) $(CFLAGS) hello.c -o $@ $(LIBS)\n#     └ cflags 在前      └ 源文件在中        └ libs 在后\n```\n（把 `--cflags --libs` 合并写在源文件**前面**，`-l` 就跑到了 `.c` 前面 —— 顺序违反规则，同样炸。）"
            }
        ]
    },
    {
        "title": "GTK4 用什么取代 gtk_main",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "gtk",
            "GTK4",
            "主循环",
            "第 13 讲"
        ],
        "choices": [
            "gtk_main() 照旧可用",
            "g_application_run()",
            "g_main_loop_run()",
            "gtk_run()"
        ],
        "source_section": "第 13 讲 · GTK 图形界面程序设计",
        "statement_md": "教材里的程序结尾是 `gtk_main();`。在 GTK4 里应该用什么？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`g_application_run()`。GTK4 把 `gtk_main_*` 整族 API 删除了。**\n\n★ 这是 GTK 3 → 4 最大的一处世界观变化：\n\n> **GTK 4 把「一堆独立的函数」换成了「一个 Application 对象」。**\n\n| 要做的事 | GTK+ 3（教材） | GTK 4 |\n|---|---|---|\n| 初始化 | `gtk_init(&argc, &argv)` | 不需要，`g_application_run()` 里做 |\n| 建窗口 | `gtk_window_new(GTK_WINDOW_TOPLEVEL)` | `gtk_application_window_new(app)` |\n| 挂「界面就绪」处理 | 手动在 main 里写 | 连 `\"activate\"` 信号 |\n| 开主循环 | `gtk_main()` | **`g_application_run(app, argc, argv)`** |\n| 退出主循环 | `gtk_main_quit()` | 由应用对象管理 |\n\n所以 GTK4 的骨架是「**先建应用、告诉应用『被激活时干什么』、然后交给应用去跑**」：\n```c\nGtkApplication *app = gtk_application_new(\"com.example.hello\",\n                                          G_APPLICATION_DEFAULT_FLAGS);\ng_signal_connect(app, \"activate\", G_CALLBACK(on_activate), NULL);\nint status = g_application_run(G_APPLICATION(app), argc, argv);\ng_object_unref(app);\n```\n\n★ 记住这一句话，第 13 讲那张「GTK3 与 GTK4 六处对照表」就是它的六个分身。**考试按教材答 `gtk_main()`，动手按 GTK4 写 `g_application_run()`。**"
            }
        ]
    },
    {
        "title": "GTK4 怎么建顶层窗口",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "gtk",
            "GTK4",
            "窗口",
            "API 迁移",
            "第 13 讲"
        ],
        "choices": [
            "照旧可用，参数不变",
            "gtk_window_new() 不再接收参数，且推荐用 gtk_application_window_new(app)",
            "改名成 gtk_widget_new()",
            "这个函数搬到了 GDK 里"
        ],
        "source_section": "第 13 讲 · GTK 图形界面程序设计",
        "statement_md": "教材里用 `gtk_window_new(GTK_WINDOW_TOPLEVEL)` 建窗口。GTK4 里该怎么做？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`gtk_window_new()` 在 GTK4 里不再接收参数，而且更推荐用 `gtk_application_window_new(app)`。**\n\n两处变化：\n1. **窗口类型参数被删了**（`GTK_WINDOW_TOPLEVEL` / `GTK_WINDOW_POPUP` 那一套），`gtk_window_new()` 变成无参函数；\n2. 有了 Application 对象之后，顶层窗口应当**挂在应用上**。\n\n★ 这两个函数**不只是名字不同**：\n\n| | `gtk_window_new()` | `gtk_application_window_new(app)` |\n|---|---|---|\n| 窗口归属 | 独立窗口，跟应用无关 | **隶属于某个 Application** |\n| 单实例 / 生命周期管理 | 没有 | 有 |\n| 桌面集成（图标、任务栏分组） | 没有 | 有 |\n\n★ 同族被删/改名的还有一串，照抄教材就会撞上：\n- `gtk_window_set_position()` → **被删**（Wayland 下窗口位置归合成器管，客户端无权指定）\n- `gtk_widget_show_all()` → **被删**（控件默认可见）\n- `gtk_container_add()` → **被删**（`GtkContainer` 整个基类没了）\n\n★ 一条经验：**报错数量多不一定是你写错了** —— 照抄 GTK3 代码时，往往是「一批 API 整体消失」，而不是个别函数名打错。"
            }
        ]
    },
    {
        "title": "二维表格控件在 GTK4 里叫什么",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "gtk",
            "GTK4",
            "布局",
            "GtkGrid",
            "第 13 讲"
        ],
        "choices": [
            "GtkTable，照旧可用",
            "GtkGrid",
            "GtkBox",
            "GtkFixed"
        ],
        "source_section": "第 13 讲 · GTK 图形界面程序设计",
        "statement_md": "教材用 `gtk_table_new(4, 4, TRUE)` 做表格布局。GTK4 里对应的控件是？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`GtkGrid`。** `GtkTable` **从 GTK 3.4 起就废弃，在 GTK4 里整个类被删了。**\n\n两处改善：\n1. `gtk_grid_new()` **不用指定行列数** —— 用到几行几列自动扩；\n2. 每个格子可以**跨行列**（`gtk_grid_attach(grid, child, col, row, colspan, rowspan)`）。\n\n★ 顺带把布局这一族都记一下，它们在第 12→13 讲的迁移里是重灾区：\n\n| 想做的事 | GTK+ 3 | GTK 4 |\n|---|---|---|\n| 往容器里放控件 | `gtk_container_add()` | `gtk_window_set_child()` / `gtk_box_append()` |\n| 横向/纵向排列 | `gtk_box_pack_start(box, c, exp, fill, pad)` | `gtk_box_append()` + `hexpand` / `valign` |\n| 二维表格 | `gtk_table_new()` | **`gtk_grid_new()`** |\n| 分隔面板 | `gtk_paned_add1/add2` | `gtk_paned_set_start_child()` / `set_end_child()` |\n| 读输入框内容 | `gtk_entry_get_text()` | `gtk_editable_get_text(GTK_EDITABLE(entry))` |\n\n★ 一个必须记住的设计思想：**GTK 布局不用坐标，用「容器套容器」**。\n你永远不写「x=100, y=50」，你写「把按钮放进一个横向盒子的末尾，盒子右边距 16」。窗口被拉大时 GTK 自己重算位置 —— 这是它和 MFC / Win32 最根本的差别，也是 `GtkFixed` 只该用于画板类场景的原因。"
            }
        ]
    },
    {
        "title": "GTK4 程序跑完窗口不出现，漏了什么",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "gtk",
            "GTK4",
            "窗口显示",
            "排错",
            "第 13 讲"
        ],
        "choices": [
            "gtk_init()",
            "gtk_widget_show_all(window)",
            "gtk_window_present(window)",
            "gtk_main()"
        ],
        "source_section": "第 13 讲 · GTK 图形界面程序设计",
        "statement_md": "一个 GTK4 程序：编译通过、运行没有报错、进程也活着，**但窗口就是不出来**。最可能漏了哪一行？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "C",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|C\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**漏了 `gtk_window_present(window)`。**\n\nGTK4 有个很「反直觉」的变化：\n- **普通控件默认就是可见的** —— 所以 `gtk_widget_show_all()` 被删了，不用也不能再调；\n- **但顶层窗口不会自动呈现** —— 必须显式 `gtk_window_present()`。\n\n★ 这个坑的可怕之处在于：**不报错、不崩溃、进程还在跑**。你看到的只是「程序启动了但什么都没发生」，会本能地去怀疑显示环境、显卡驱动、Wayland 会话……其实就差这一行。\n\n★ 和它配套的两个「看不见的坑」：\n\n| 现象 | 原因 |\n|---|---|\n| 从 cron / systemd 服务里启动 GTK 程序，报 `cannot open display` | 没有 `DISPLAY` / `WAYLAND_DISPLAY` —— 这是「图形程序不能后台跑」的根本原因 |\n| 在 Wayland 会话里用 `xdotool` / `wmctrl` 控制别的 GTK4 窗口，没反应 | Wayland 下**客户端互相隔离**，这是安全性设计不是 bug |\n\n★ 排查 GUI 程序的通用姿势（第 16 讲会再用一次）：**从终端启动**，别双击 —— 双击时 stderr 没有终端接着，错误就凭空消失了（Eclipse 闪退也是这个道理）。"
            }
        ]
    },
    {
        "title": "g_signal_connect 的信号名拼错会怎样",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "gtk",
            "信号",
            "排错",
            "第 13 讲"
        ],
        "choices": [
            "编译期报错，说信号不存在",
            "编译通过，但运行起来毫无反应",
            "程序一启动就崩溃",
            "启动时弹出「未知信号」警告并退出"
        ],
        "source_section": "第 13 讲 · GTK 图形界面程序设计",
        "statement_md": "把信号名写成 `\"activatee\"`（多打了一个 e），会发生什么？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**编译完全通过，运行毫无反应。**\n\n信号名在 `g_signal_connect` 里是一个**字符串**（`gchar *`），**编译器不检查字符串内容** —— 只有运行到那一行、GLib 去信号表里查，才发现「没有这个信号」。而且它**不会让程序退出**，你只会看到「按钮点了没反应」。\n\n★ 这是最典型的「一小时黑洞」：没有报错、没有崩溃、你盯着一堆写对的代码找不到问题。\n\n**排障武器**：让 GLib 把警告当致命错误打出来\n```bash\n./hello --g-fatal-warnings\n```\n\n★ **这条坑正是第 14 讲 Qt 存在的理由**：\n\n| | GTK（C） | Qt（C++） |\n|---|---|---|\n| 信号怎么表示 | **字符串** `\"clicked\"` | **函数指针** `&QPushButton::clicked` |\n| 拼错时 | 编译通过，运行静默失败 | **编译期直接报错并指出位置** |\n\nQt 那套写法（新式 `&Class::method`）就是专门用来消灭这类错误的 —— 这是「类型系统帮你干活」的教科书案例。"
            }
        ]
    },
    {
        "title": "GTK4 里控件默认可见",
        "subject": "linux",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 3,
        "total_score": 8,
        "tags": [
            "gtk",
            "GTK4",
            "可见性",
            "第 13 讲"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 13 讲 · GTK 图形界面程序设计",
        "statement_md": "GTK4 里控件默认就是可见的，不需要再调用 `gtk_widget_show_all()`。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "对",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|对\n|正确\n|√\n|T\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**对。** GTK4 里控件创建出来**默认可见**，所以 `gtk_widget_show()` / `gtk_widget_show_all()` 这族函数**被删除了**。\n\n★ 最容易被这条绊住的人是**照抄 GTK3 代码**的：\n教材那 12 行里有一行 `gtk_widget_show_all(window);` —— 在 GTK4 里编译直接报「没有这个函数」。\n\n★ 但**别把这条和上一题记混**：\n\n| 对象 | GTK4 里的可见性 |\n|---|---|\n| 普通控件（按钮、标签、盒子） | **默认可见**，不用管 |\n| **顶层窗口** | **仍然要显式 `gtk_window_present()`** |\n\n一句话：**「控件自动可见」被删掉了 `show_all`，「窗口要显式呈现」是新加的 `present`。** 两者一减一加，别只记住一半。"
            }
        ]
    },
    {
        "title": "GtkContainer 在 GTK4 里还在吗",
        "subject": "linux",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 3,
        "total_score": 8,
        "tags": [
            "gtk",
            "GTK4",
            "容器",
            "API 迁移",
            "第 13 讲"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 13 讲 · GTK 图形界面程序设计",
        "statement_md": "GTK4 里仍然可以用 `gtk_container_add(GTK_CONTAINER(w), child)` 往窗口里放控件。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "错",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|错\n|错误\n|×\n|F\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**错。`GtkContainer` 这个基类在 GTK4 里整个被删除了。**\n\nGTK3 把所有「能装子控件的对象」统一抽象成 `GtkContainer`，配套一组 `gtk_container_*()` 函数。GTK4 把这层抽象拿掉，改成**每种容器用自己的专用函数**：\n\n| 容器 | GTK4 里怎么加子控件 |\n|---|---|\n| 窗口 | `gtk_window_set_child(window, child)` |\n| 盒子 | `gtk_box_append(box, child)` / `gtk_box_prepend()` |\n| 网格 | `gtk_grid_attach(grid, child, col, row, w, h)` |\n\n★ 顺带两条和「控件归属」有关的硬规矩：\n1. **一个控件只能有一个父容器** —— 把同一个控件 append 到两个容器，会收到 `Gtk-WARNING: Attempting to add widget ... but it already has a parent`。要在两处显示得建两个控件。\n2. **窗口只能有一个子控件** —— 第二次 `set_child` 会把第一个顶掉。要放多个，**先建一个 `GtkBox` 再往里放**。"
            }
        ]
    },
    {
        "title": "Makefile 里 pkg-config 该用哪种赋值",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "make",
            "pkg-config",
            "GTK4",
            "第 13 讲"
        ],
        "choices": [
            "用 =，因为更灵活，值变了能跟着变",
            "用 :=，否则每次用到 CFLAGS 都会重跑一次 pkg-config 子进程",
            "两者完全等价，随便用",
            "都不对，应该把参数写死在编译命令里"
        ],
        "source_section": "第 13 讲 · GTK 图形界面程序设计",
        "statement_md": "下面两种写法，GTK 项目推荐哪一种、为什么？\n\n```make\nCFLAGS =  $(shell pkg-config --cflags gtk4)\nCFLAGS := $(shell pkg-config --cflags gtk4)\n```",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**用 `:=`（立即展开）。**\n\n| 写法 | 展开时机 | 后果 |\n|---|---|---|\n| `CFLAGS = $(shell ...)` | **递归展开** —— 每次**用到**都重新求值 | 用 2 次就起 2 个子进程 |\n| `CFLAGS := $(shell ...)` | **立即展开** —— 定义时求值一次 | 只起 1 个子进程 |\n\n★ 讲义里实测过：`CFLAGS = $(shell ...)` 在同一个 Makefile 里被引用 2 次，子进程就真的被调起 2 次。项目一大、嵌套一深，这个开销会很难看。\n\n★ 顺带两个同族的坑：\n1. **`make -n` 照样会触发 `$(shell ...)`** —— `-n` 只拦「命令行的执行」，**不拦「变量展开」**。所以别拿 `make -n` 当「零副作用」的预览工具。\n2. **Makefile 里用单引号包 `$(pkg-config ...)` 是不行的** —— **单引号里的 `$( )` 不展开**（这是 make 的行为，不是 shell）——\n   报错会变成 `cannot find '$(pkg-config'`，看起来莫名其妙。\n\n★ 一句话记住：**Makefile 里 `:=` 是「现在就做」，`=` 是「用的时候再做」。**要起子进程、要算时间、要读文件的地方，一律用 `:=`。"
            }
        ]
    },
    {
        "title": "gtk_grid_attach 的参数顺序",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "gtk",
            "GTK4",
            "GtkGrid",
            "参数顺序",
            "第 13 讲"
        ],
        "choices": [
            "列、行、跨列数、跨行数",
            "行、列、跨行数、跨列数",
            "x 坐标、y 坐标、宽度、高度（像素）",
            "行、列、宽度、高度"
        ],
        "source_section": "第 13 讲 · GTK 图形界面程序设计",
        "statement_md": "`gtk_grid_attach(grid, child, a, b, c, d)` 里，`a` ~ `d` 依次代表什么？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "A",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|A\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`(col, row, width, height)` —— 先列后行。**\n\n```c\ngtk_grid_attach(grid,   /* 容器 */\n                child,  /* 子控件 */\n                1,      /* a: 第几列 column */\n                0,      /* b: 第几行 row    */\n                2,      /* c: 跨几列 */\n                1);     /* d: 跨几行 */\n```\n\n★ 写反了（先行后列）界面会被**转置 90 度**，而且**看起来「只是有点怪」，不容易发现** —— 尤其是几行几列比较对称的时候。\n\n★ 注意坐标系的两件事：\n- **从 0 开始**（`0` 是第一列 / 第一行）；\n- **不是像素坐标** —— GTK 布局是「声明式」的，你只声明「放在第几格」，具体位置由 GTK 按窗口大小算。\n\n★ 对比着记一下另一套容易混的坐标：**`GtkTable` 时代是 `(列起, 列止, 行起, 行止)`** （半开区间）；换成 `GtkGrid` 后是 **`(列, 行, 跨列, 跨行)`**（起点 + 跨度），语义变了，不是简单改名。"
            }
        ]
    },
    {
        "title": "Qt6 要求哪个 C++ 标准",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "qt",
            "Qt6",
            "C++17",
            "第 14 讲"
        ],
        "choices": [
            "C++98",
            "C++11",
            "C++14",
            "C++17"
        ],
        "source_section": "第 14 讲 · Qt 图形界面程序设计",
        "statement_md": "把 Qt5 项目迁到 Qt6，`CONFIG += c++11` 是常见写法。Qt6 要求的最低 C++ 标准是？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "D",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|D\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**C++17。** Qt6 把最低标准从 Qt5 的 C++11 提到了 **C++17**。\n\n对应到构建系统：\n```make\n# qmake（.pro）\nCONFIG += c++17\n```\n```cmake\n# CMake\nset(CMAKE_CXX_STANDARD 17)\nset(CMAKE_CXX_STANDARD_REQUIRED ON)\n```\n\n★ **不写的报错很难懂** —— 错误会出现在 **Qt 自己的头文件里**，而不是你的代码里，看起来像「Qt 装坏了」。\n\n★ 一个实测细节值得记住：**`-std=c++11` 编译 C++17 代码时，gcc 往往只给 warning 不给 error** —— 也就是说「它编过了」**不能证明标准合规**。要严格验证得加 `-pedantic-errors`。\n\n★ 这条和 GTK 那边形成鲜明对比，值得一并记住：\n\n| | GTK 3 → 4 | Qt 5 → 6 |\n|---|---|---|\n| Hello World 源码 | **12 行改 6 处** | **基本一字不改** |\n| 真正的迁移成本在哪 | 接口大改、源码重写 | **构建系统 + C++ 标准** |\n\n所以：**教材第 13 章的 GTK 示例一行都编不过，而第 14 章的 Qt 示例大概率能直接编过。**"
            }
        ]
    },
    {
        "title": "Qt5 的 Hello World 在 Qt6 下要改吗",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "qt",
            "Qt6",
            "迁移",
            "第 14 讲"
        ],
        "choices": [
            "必须整篇重写",
            "基本一字不改，变的是构建系统和 C++ 标准",
            "要改掉一半左右的 API",
            "只能跑在 Qt5 上，Qt6 不兼容"
        ],
        "source_section": "第 14 讲 · Qt 图形界面程序设计",
        "statement_md": "和 GTK3→GTK4「十二行改六处」完全不同，Qt5 的 Hello World 源码搬到 Qt6？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**基本一字不改。** 这是 Qt6 官方明确的目标：**保持 Qt5 源码兼容**。\n\n★ 两个框架的迁移哲学完全不同：\n\n| | GTK 3 → 4 | Qt 5 → 6 |\n|---|---|---|\n| 官方态度 | 借大版本清理历史包袱 | **尽量不动源码** |\n| Hello World | 12 行改 6 处 | **一行不用改** |\n| 你要搬的东西 | 一堆 API | **构建系统（qmake → CMake）+ C++ 标准（11 → 17）** |\n| 被移走的类 | 直接删（`GtkTable` / `GtkContainer`） | 挪进 **Qt5Compat** 模块（还能用）|\n\n★ **被挪进 Qt5Compat 的代表选手**（用到了才需要处理）：\n- `QRegExp` → 改用 `QRegularExpression`\n- `QTextCodec` 族 → 改用 `QStringConverter` 族\n- `QLinkedList` → 改用 `std::list`（或 `QList`）\n- `QStringRef` → 改用 `QStringView`\n- `QXmlSimpleReader` → 改用 `QXmlStreamReader`\n\n★ 官方给了一个**一键找出全部过时用法**的开关：\n```make\nDEFINES += QT_DISABLE_DEPRECATED_UP_TO=0x050F00\n```\n它把 Qt 5.15 及以前废弃的 API **全部变成编译错误**，于是你得到一份**可执行、可勾选**的迁移清单 —— 比翻文档靠谱得多。"
            }
        ]
    },
    {
        "title": ".pro 里漏了 QT += widgets 会怎样",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "qt",
            "qmake",
            ".pro",
            "widgets",
            "第 14 讲"
        ],
        "choices": [
            "QT += widgets",
            "QT += gui",
            "CONFIG += qt",
            "LIBS += -lQtWidgets"
        ],
        "source_section": "第 14 讲 · Qt 图形界面程序设计",
        "statement_md": "`.pro` 只写了 `QT += core gui`，编译时报 `QApplication: No such file or directory`。缺的是哪一行？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "A",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|A\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**缺 `QT += widgets`。**\n\nQt5 起，「GUI 控件」被从 `QtGui` 模块**拆到了独立的 `QtWidgets`** —— 你想用的 `QApplication` / `QPushButton` / `QLabel` 全在那里。\n\n漏写的两种报错形态：\n```\nQApplication: No such file or directory\nundefined reference to 'QApplication::QApplication(...)'\n```\n★ 前者是「找不到头文件」（编译期），后者是「找不到实现」（链接期）—— 同一件事的两个阶段。\n\n★ **真正的坑在这里**：`qmake6 -project` 自动生成的 `.pro` **恰恰不会写这一行** —— 因为它只扫描源文件，**不解析代码**，猜不出你需不需要 GUI。\n\n所以正确姿势是**生成时就把模块补上**：\n```bash\nqmake6 -project \"QT += widgets\"\n```\n或者生成之后**手工打开 `.pro` 补那一行**。\n\n★ `.pro` 里另外两个「漏写就出事」的：\n- **`HEADERS +=`** —— 这行是**moc 的待办清单**，不是给编译器看的。漏了那个头文件，那个类就没有 moc 输出 → `undefined reference to vtable for XXX`。\n- **`CONFIG += c++17`** —— Qt6 的硬要求，见前一题。"
            }
        ]
    },
    {
        "title": "为什么 qmake -project 生成的 .pro 缺 widgets",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "qt",
            "qmake",
            ".pro",
            "第 14 讲"
        ],
        "choices": [
            "qmake 版本太旧，新版本会自己补上",
            "它只扫描源文件、不解析代码，猜不出你要不要 GUI",
            "需要加 --widgets 参数才行",
            "Fedora 的 Qt 包被裁剪过，缺模块描述"
        ],
        "source_section": "第 14 讲 · Qt 图形界面程序设计",
        "statement_md": "`qmake6 -project` 生成的 `.pro` 里只有 `QT += core gui`，没有 widgets。原因？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`qmake -project` 只「扫源文件」，不「读代码」。**\n\n它做的事情很简单：把当前目录下的 `.cpp` / `.h` / `.ui` 列进 `.pro`，再给一份**最保守的默认模块**（`core gui`）。它**不会去分析你的代码里 `#include` 了什么、用了哪个类** —— 所以当然猜不出你需不需要 `widgets`。\n\n★ 结论：**`qmake -project` 的输出是「起点」，不是「成品」。**\n生成完一定要打开 `.pro` 检查这几行：\n```make\nQT += core gui widgets        # GUI 控件必需\nCONFIG += c++17               # Qt6 必需\nHEADERS += mywidget.h         # 有 Q_OBJECT 的头文件必须列进来\n```\n\n★ 顺带一条实用建议：**`.pro` 只要十几个关键字就能读懂整个工程结构**，所以「先 qmake 后 CMake」是个好顺序 —— 先用 `.pro` 十分钟搞清工程长什么样，再去看 CMake 的自动化配置。\n\n★ 反过来，**Qt6 官方是主推 CMake 的**（Qt6 自身就用 CMake 构建）。qmake 仍然支持、教材那套三步走在 Fedora 44 上照样能跑（只是命令名变成 `qmake6`），但两条路都要认得出。"
            }
        ]
    },
    {
        "title": "Qt 多出来的构建步骤是什么",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "qt",
            "moc",
            "构建",
            "第 14 讲"
        ],
        "choices": [
            "moc（元对象编译器）",
            "uic",
            "rcc",
            "qmake"
        ],
        "source_section": "第 14 讲 · Qt 图形界面程序设计",
        "statement_md": "教材的 GTK 项目构建链是 `cpp → cc1 → as → ld`（GCC 四道工序）。Qt 项目在这之前多插了一道什么？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "A",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|A\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**moc —— 元对象编译器（Meta-Object Compiler）。**\n\n```\nmywidget.h（含 Q_OBJECT 宏）\n      │\n      │  moc        ★ GTK 没有这一步\n      ▼\nmoc_mywidget.cpp\n      │\n      ▼\n   g++（编译 + 汇编 + 链接）\n```\n\n★ **为什么需要它**：Qt 想在 C++ 里实现「信号与槽」这套**运行时的元对象系统**（按名字查找函数、发射信号、反射对象类型），而纯 C++ 在 1995 年做不到这件事 —— 所以 Qt 自己写了一个**代码生成器**。\n\n> **一句话：moc 是 Qt 用来补足 C++ 语言能力的一个预处理步骤。**\n\n★ 记住这句话，后面所有「和 moc 有关的怪现象」都能解释：\n\n| 现象 | 原因 |\n|---|---|\n| `undefined reference to vtable for MyClass` | moc 没工作（漏 `Q_OBJECT` / 头文件没进 `HEADERS +=`）|\n| 改了头文件没重建，看到「幽灵错误」 | `moc_*.cpp` 是**缓存文件**，得 `make clean` 或删 build 目录 |\n| 手写 Makefile 特别痛苦 | 要自己判断 moc / uic / rcc 的处理对象和顺序 |\n\n★ 另外两个名字也要认识（本题的干扰项）：\n- **uic** —— 把 `.ui`（Qt Designer 界面文件）编译成 C++ 头文件；\n- **rcc** —— 把 `.qrc`（资源文件）编译成 C++ 源文件。\n\n★ 一条纪律：**`moc_*.cpp` / `ui_*.h` / `Makefile` 都是生成物，不进版本管理** —— 判断标准是「**能被工具重新生成的都不进**」。"
            }
        ]
    },
    {
        "title": "undefined reference to vtable 通常是什么问题",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "qt",
            "moc",
            "Q_OBJECT",
            "vtable",
            "第 14 讲"
        ],
        "choices": [
            "析构函数没写或写错了",
            "moc 没工作 —— 漏了 Q_OBJECT，或头文件没进 HEADERS",
            "忘了链接 -lQt6Core",
            "C++ 标准不是 17"
        ],
        "source_section": "第 14 讲 · Qt 图形界面程序设计",
        "statement_md": "链接时报 `undefined reference to vtable for MyClass`。在 Qt 里这几乎总是？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**建立这个映射：`vtable undefined` ≈ moc 问题。**\n\n报错里出现 `vtable` 会让人本能地去查析构函数、虚函数表、继承 —— **方向完全错**。这条报错的绝大多数成因是：\n\n1. 类里**忘了写 `Q_OBJECT`** 宏 —— `Q_OBJECT` 会插入一批虚函数**声明**，实现由 moc 生成；没有它就没有那些实现；\n2. 写是写了，但**头文件没进 `.pro` 的 `HEADERS +=`** —— 那行就是 moc 的待办清单，不在清单里就不会被 moc 处理；\n3. 改了头文件**没重建**，拿着旧的 `moc_*.cpp` 在链接。\n\n**排查顺序**：\n```bash\n① 类定义第一行有 Q_OBJECT 吗\n② .pro 的 HEADERS += 里有这个头文件吗（CMake 项目看 AUTOMOC 是否打开）\n③ make clean（或删 build 目录）重建一次\n```\n\n★ 顺带把「信号 / 槽」两个区最容易记混的一条钉住：\n\n| | 要写实现吗 |\n|---|---|\n| `signals:` 区 | **不要** —— 只写声明，实现由 moc 生成（手写会报重复定义）|\n| `slots:` 区 | **要** —— 槽就是普通函数，必须自己写函数体 |\n\n★ 还有一条：**`emit` 不是 C++ 关键字**，它是 Qt 定义的一个**空宏**，只为可读性 —— `emit sig();` 和 `sig();` 编译结果完全相同。"
            }
        ]
    },
    {
        "title": "哪种信号槽写法能在编译期查出拼写错误",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "qt",
            "信号槽",
            "connect",
            "类型安全",
            "第 14 讲"
        ],
        "choices": [
            "connect(a, SIGNAL(clicked()), b, SLOT(onClick()))",
            "connect(a, &QPushButton::clicked, b, &MyWidget::onClick)",
            "两种都会编译期报错",
            "两种都不会，都要运行时才发现"
        ],
        "source_section": "第 14 讲 · Qt 图形界面程序设计",
        "statement_md": "下列哪种 `connect` 写法，在**信号名拼错**时会**编译期报错**？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`&Class::method` 新语法。** 这是第 14 讲**最值钱的一条**。\n\n| | 老式字符串宏 | 新式函数指针 |\n|---|---|---|\n| 写法 | `SIGNAL(clicked())` / `SLOT(onClick())` | `&QPushButton::clicked` |\n| 名字是 | **字符串** | **函数指针** |\n| 拼错时 | **编译通过、运行时静默失败**（连接返回失败但不报错、程序不崩）| **编译期报错并指出位置** |\n| 能连 lambda 吗 | 不能 | 能 |\n| 现在推荐吗 | 不推荐（但 Qt6 仍支持）| **推荐** |\n\n★ 这一步正好补上了第 13 讲留下的那个坑 —— GTK 的 `g_signal_connect(widget, \"activatee\", ...)` 拼错后**编译通过、运行毫无反应**；Qt 的新语法用**类型系统**把这类错误提前到了编译期。\n\n★ 顺带三条：\n- **`connect` 还有第四个参数**（连接类型）：跨线程用 `Qt::QueuedConnection`，防重复连接用 `Qt::UniqueConnection`。默认 `Qt::AutoConnection` 是「同线程直连、跨线程排队」，一般够用。\n- **信号可以连信号** —— 这是**封装的标准手段**：把内部控件的信号转发成自己的信号，外部就不知道你的内部结构了。\n- **Qt 对象销毁时会自动断开连接**（它跟踪 `QObject` 生命周期），所以「放心 new 一堆控件」是有依据的。"
            }
        ]
    },
    {
        "title": "emit 是 C++ 关键字吗",
        "subject": "linux",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 3,
        "total_score": 8,
        "tags": [
            "qt",
            "信号槽",
            "emit",
            "第 14 讲"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 14 讲 · Qt 图形界面程序设计",
        "statement_md": "`emit` 是 C++ 关键字，写信号发射时去掉它信号就不会发射。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "错",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|错\n|错误\n|×\n|F\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**错。`emit` 是 Qt 定义的一个空宏，只为可读性。**\n\n```cpp\nemit mysignal();      // 等价于\nmysignal();           // 编译结果完全相同\n```\n\n★ 它存在的意义是**给读代码的人一个提示**：「这一行是在发射信号，不是在调普通函数」。编译器看到 `emit` 就被展开成空，什么也不做。\n\n★ 同族还有两个「看起来像语法、其实是宏」的：\n- **`signals:`** → 展开成 `public`（Qt 自己加的一层访问控制标记）\n- **`slots:`** → 同样只是个标记，展开成 `public`/`protected`/`private`\n\n★ 所以「信号和槽只是普通成员函数 + 一点元信息」这个理解是对的 —— **唯一的特殊性在于 moc 会读取它们，为信号生成实现、并往元对象表里登记名字**。"
            }
        ]
    },
    {
        "title": "signals 区的函数要不要写实现",
        "subject": "linux",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 4,
        "total_score": 8,
        "tags": [
            "qt",
            "信号槽",
            "moc",
            "第 14 讲"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 14 讲 · Qt 图形界面程序设计",
        "statement_md": "`signals:` 区里声明的函数必须自己写函数体，否则链接不过。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "错",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|错\n|错误\n|×\n|F\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**错。信号只写声明 —— 实现由 moc 生成。**\n\n```cpp\nclass MyWidget : public QWidget {\n    Q_OBJECT\nsignals:\n    void clicked2();          // ✅ 只写声明，不写实现\npublic slots:\n    void onClick();           // 槽 —— 实现写在 .cpp 里\n};\n```\n\n★ **这两个区最容易记混，记法如下**：\n\n| 区 | 声明 | 实现 | 为什么 |\n|---|---|---|---|\n| `signals:` | 要写 | **不要写** | moc 会生成「遍历连接、逐个调用槽」的代码 |\n| `slots:` | 要写 | **要写** | 槽就是普通成员函数，只是可以被信号调用 |\n\n★ 手写信号的实现会报**「重复定义」** —— 因为 moc 已经替你在 `moc_xxx.cpp` 里生成了一份。\n\n★ 一句话记：**信号是「出口」，声明即完整；槽是「入口」，必须自己实现。**"
            }
        ]
    },
    {
        "title": "Fedora 上 qmake 指向哪一代",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "qt",
            "qmake",
            "工具链",
            "第 14 讲"
        ],
        "choices": [
            "Qt6",
            "Qt5",
            "报错 command not found",
            "随机，看先装哪个"
        ],
        "source_section": "第 14 讲 · Qt 图形界面程序设计",
        "statement_md": "机器上 Qt5 和 Qt6 的开发包都装了。直接敲 `qmake` 会指向？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**指向 Qt5。** Fedora 上 `qmake` 属于 Qt5 的包，**Qt6 的命令名是 `qmake6`。**\n\n★ 后果很严重而且很隐蔽：**你写的是 Qt6 代码，却用 Qt5 的 qmake 生成 Makefile** → 链的是 Qt5 的库 → 一串 `undefined reference`。查了半天代码，问题其实在「你用的是哪一代 qmake」。\n\n**先确认再动手**：\n```bash\nqmake --version          # 看它报 Qt version 5.x 还是 6.x\nqmake6 --version         # 明确要用 Qt6 就叫这个名字\n```\n\n★ 一条通用经验：**遇到一堆链接错误，先怀疑「工具链指向了哪一代」**，再去看代码。同族的分诊动作还有（第 16 讲会再用到）：\n\n```bash\nwhich -a java            # 装了多个 JDK 时，看 PATH 里排第一个的是谁\nwhich -a python3         # 装了多个 Python 时同理\n```\n\n★ 教材那套 `qmake -project && qmake && make` 三步走在 Fedora 44 上**依然能跑**，只是命令名要换成 `qmake6`。"
            }
        ]
    },
    {
        "title": "QRegExp 在 Qt6 里去哪了",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "qt",
            "Qt6",
            "QRegExp",
            "迁移",
            "第 14 讲"
        ],
        "choices": [
            "照旧留在核心模块里",
            "移入 Qt5Compat，新代码应该用 QRegularExpression",
            "改名成 QRegex",
            "被彻底删除，没有任何替代"
        ],
        "source_section": "第 14 讲 · Qt 图形界面程序设计",
        "statement_md": "Qt5 代码里常用的 `QRegExp`，在 Qt6 里的状况是？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**移入 Qt5Compat 模块 —— 还能用，但新代码该换 `QRegularExpression`。**\n\n★ 这是 Qt6 处理历史类的**统一手法**：**不删，挪走**。和 GTK4 那种「整个类删掉、必须重写」完全不同的路线。\n\n| Qt5 里的类 | Qt6 里 | 该换成 |\n|---|---|---|\n| `QRegExp` | Qt5Compat | **`QRegularExpression`** |\n| `QTextCodec` / `QTextEncoder` / `QTextDecoder` | Qt5Compat | `QStringConverter` 族 |\n| `QLinkedList` | Qt5Compat | `std::list`（或 `QList`）|\n| `QStringRef` | Qt5Compat | `QStringView` |\n| `QXmlSimpleReader` | Qt5Compat | `QXmlStreamReader` |\n\n要临时继续用 Qt5Compat 里的东西，得显式加模块：\n```make\nQT += core5compat\n```\n★ **不推荐长期这么做** —— 它只是让老代码先跑起来的过渡手段。\n\n★ 另外几个「不是挪走、是真的变了」的，别记混：\n- **`QTextStream::setCodec()`** → **被删除**（不是废弃），改用 `setEncoding()`\n- **Qt Quick Controls 1** → **整个删除**（QML 侧最大的一处断裂，必须重写）\n- **`QList` / `QVector`** → **两者合一**（`QVector` 成为 `QList` 的别名），不用再纠结选哪个\n- **高 DPI 支持** → **Qt6 默认开启**，那些设置属性/环境变量的代码可以删掉了"
            }
        ]
    },
    {
        "title": "Qt 控件要不要手动 delete",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "qt",
            "对象树",
            "内存管理",
            "第 14 讲"
        ],
        "choices": [
            "要，否则会内存泄漏",
            "不用，父对象销毁时会自动清理子对象",
            "要，必须在析构函数里逐个删掉",
            "只有顶层窗口需要手动删"
        ],
        "source_section": "第 14 讲 · Qt 图形界面程序设计",
        "statement_md": "用 `new` 创建的控件，已经通过 `setParent()` 或容器加到了父对象上。还需要手动 `delete` 吗？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**不用。Qt 有「对象树」：子对象由父对象销毁时自动清理。**\n\n只要控件被 `setParent()`、或者作为子控件加进了某个容器，它就成了父对象的孩子；父对象析构时会**递归把自己的孩子都删掉**。\n\n★ **重复 delete 会崩** —— 这是「手动删」最危险的后果。\n\n```cpp\nauto *btn = new QPushButton(\"ok\", this);   // this 是父对象\n// ... 用完不用管，父对象析构时自动删 btn\n```\n\n★ 三个配套结论，一起记：\n1. **对象销毁时会自动断开信号槽连接** —— Qt 跟踪 `QObject` 生命周期。这就是「为什么可以放心 new 一堆控件」的完整答案；\n2. 但**跨线程要小心**：如果显式指定了 `Qt::DirectConnection`，跨线程时槽会在**发送者线程**里执行 → 访问到别的线程的对象 → 崩溃。跨线程用默认的 `AutoConnection`（会排队）或显式 `QueuedConnection`；\n3. **主窗口选型**：`QMainWindow`（有菜单栏/状态栏位置）/ `QDialog`（对话框）/ `QWidget`（其余）。拿 `QLabel` 当主窗口能跑但不正规。\n\n★ 这条和 GTK4 的「一个控件只能有一个父容器」是同一个思想的两面：**GUI 框架普遍用「所有权树」来管内存**，你只要把父子关系摆对，就不需要自己写 delete。"
            }
        ]
    },
    {
        "title": "pip install 被拒绝后加 --user 能绕过吗",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "python",
            "PEP 668",
            "pip",
            "venv",
            "第 15 讲"
        ],
        "choices": [
            "装成功，装到用户目录",
            "仍被同样拒绝（退出码 1）",
            "会提示需要 sudo",
            "会装到系统 site-packages"
        ],
        "source_section": "第 15 讲 · Python 程序开发环境",
        "statement_md": "`pip install requests` 报 `error: externally-managed-environment`。\n\n改成 `pip install --user requests` 会怎样？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**绕不过去 —— 仍被同样拒绝，退出码 1。**\n\n★ 这是第 15 讲**最值钱的一条**（讲义里 ★★★ 实测，退出码为 1）。\n\n**为什么 `--user` 没用**：PEP 668 检查的对象是**解释器**，不是目录。Fedora 38 起系统 Python 被标记为「外部管理」（`/usr/lib/python3.x/EXTERNALLY-MANAGED` 那个文件），而 `--user` 只是换个安装目录，**没换解释器**。\n\n★ **正解有三条，按场景选**：\n\n| 场景 | 做法 |\n|---|---|\n| 项目里要用第三方库 | **`python3 -m venv .venv` + 激活** |\n| 装命令行工具 | **`pipx install xxx`** |\n| 有官方 RPM 的库 | **`sudo dnf install python3-xxx`** |\n\n★ 还有个逃生门 `--break-system-packages` —— 它是官方给的，含义就是「**后果我承担**」。**只在容器 / 一次性环境里用**，名字里的 `break-system` 就是警告。判断法：**这个环境坏了能整个重建吗？**\n\n⚠️ 网上大量帖子写「加 `--user` 就行」—— **那是 Fedora 38 之前的答案**，在今天的 Fedora 上一字不差地失败。"
            }
        ]
    },
    {
        "title": "Fedora 上装第三方 Python 包的正解",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "python",
            "venv",
            "包管理",
            "第 15 讲"
        ],
        "choices": [
            "sudo pip install 包名",
            "pip install --break-system-packages 包名",
            "python3 -m venv .venv → 激活 → pip install 包名",
            "改 /usr/bin/python3 的软链接指向另一个 Python"
        ],
        "source_section": "第 15 讲 · Python 程序开发环境",
        "statement_md": "在一个项目里要用第三方库，正确做法是？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "C",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|C\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`python3 -m venv .venv` + `source .venv/bin/activate` + `pip install`。**\n\n```bash\ncd 项目目录\npython3 -m venv .venv\nsource .venv/bin/activate\npip install requests\n```\n\n★ **venv 为什么轻**（★★★ 实测）：它**不复制标准库** —— 环境里那一项仍指向系统那份；**venv 只隔断 `site-packages`**。所以建得飞快（一两秒）、占地很小。\n\n★ 三个「看着像正解、其实是错路」的选项，各自错在哪：\n\n| 做法 | 为什么不行 |\n|---|---|\n| `sudo pip install` | ① 会被 PEP 668 拦；② **如果没被拦，说明你在破坏系统** |\n| `--break-system-packages` | 官方逃生门，只该在容器里用 |\n| 改 `/usr/bin/python3` 软链接 | **最危险** —— `dnf` 的第一行就是 `#!/usr/bin/python3`，改坏了 **dnf 直接起不来**，而修它又要用 dnf |\n\n★ 两条配套纪律：\n1. **每次操作前先核对「我在不在 venv 里」** —— 建了环境但忘了 activate，`pip install` 还是装到系统 Python（照样撞 PEP 668）；\n2. **`activate` 只影响当前 shell** —— 新开一个终端要**重新 activate**（它改的是那个 shell 的 `PATH` 和环境变量）。\n\n⚠️ 用 `--system-site-packages` 建环境做「干净测试」是**假的干净**：系统 `site-packages` 仍然可见（排在 venv 之后），结论不可信。"
            }
        ]
    },
    {
        "title": "怎么判断自己是不是在 venv 里",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "python",
            "venv",
            "环境判断",
            "第 15 讲"
        ],
        "choices": [
            "sys.prefix != sys.base_prefix",
            "sys.executable == sys.base_executable",
            "os.path.exists('venv')",
            "sys.version 末尾带着 'venv' 字样"
        ],
        "source_section": "第 15 讲 · Python 程序开发环境",
        "statement_md": "写脚本想自动判断「当前解释器跑在虚拟环境里」。官方推荐、**不依赖环境变量**的判据是？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "A",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|A\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`sys.prefix != sys.base_prefix`。**\n\n- `sys.base_prefix` = **那台机器的原始 Python 安装前缀**（永远不变）；\n- `sys.prefix` = **当前生效的前缀**。\n\n在 venv 里，`sys.prefix` 被改成 venv 的目录，于是两者不等 → 判定为「在 venv 里」。\n\n```bash\npython3 -c \"import sys; print(sys.prefix != sys.base_prefix)\"\n# True  → 在 venv 里\n# False → 用的是系统 Python\n```\n\n★ **为什么强调「不依赖环境变量」**：`VIRTUAL_ENV` 这类变量**靠 activate 脚本设置** —— 你没 activate 就没这个变量，「没 activate 但确实在用 venv 的解释器」这种情况会误判。\n\n★ 这一行是**第 15 讲最实用的防御性写法** —— 把它嵌进项目的启动脚本，「我明明装了却 import 不到」这类问题当场现形。\n\n★ 配套的另一条：**一律写 `python3 -m pip`，不要写裸 `pip`** —— ★★★ 实测里 `pip` 和 `python` **指向两个不同的 Python 安装**。`python3 -m pip` 表达的是「**我现在这个 Python 的 pip**」，这才是「装到哪去了」的可靠答案。"
            }
        ]
    },
    {
        "title": "python3 -m 和直接跑脚本差在哪",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "python",
            "-m",
            "sys.path",
            "导入",
            "第 15 讲"
        ],
        "choices": [
            "sys.path[0] 不同：前者是当前工作目录，后者是脚本所在目录",
            "前者不能带命令行参数",
            "前者用不了第三方库",
            "没有任何差别，只是写法不同"
        ],
        "source_section": "第 15 讲 · Python 程序开发环境",
        "statement_md": "`python3 -m pkg.mod` 与 `python3 pkg/mod.py` 的关键差别之一是？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "A",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|A\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`sys.path[0]` 不同** —— 这是第 15 讲技术含量最高的一条。\n\n| | `python3 pkg/mod.py` | `python3 -m pkg.mod` |\n|---|---|---|\n| `sys.path[0]` | **脚本所在目录**（`pkg/`） | **当前工作目录** |\n| `__package__` | `None` | `'pkg'` |\n| 相对导入（`from . import x`）| **不可用** | 可用 |\n\n★ 两个直接后果：\n1. **包内模块直接跑**会报 `attempted relative import with no known parent package` —— 因为 `__package__` 是 `None`，那个 `.` 无处可指。**包内模块一律用 `python3 -m pkg.mod`**；\n2. `-m` 报 `No module named pkg` 时，**是因为你没站在 `pkg/` 的父目录里** —— `-m` 的 `sys.path[0]` 是**当前工作目录**。\n\n★ 顺带两条：\n- `-m` 后面要写**模块名（点号分隔）**，写路径是语法错误：`python3 -m pkg.mymod` ✅ / `python3 -m pkg/mymod.py` ❌；\n- 日常一大堆命令都是 `-m` 形式，教材一个字都没提：\n  `python3 -m venv`、`python3 -m pip`、`python3 -m http.server`、`python3 -m json.tool`。\n\n★ **口诀：「直接跑 = 脚本当主角，`-m` = 包里的一员」。**\n谁当 `sys.path[0]`，就决定了「你能看见谁」。"
            }
        ]
    },
    {
        "title": "为什么一律写 python3 -m pip",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "python",
            "pip",
            "解释器",
            "第 15 讲"
        ],
        "choices": [
            "sudo pip install",
            "python3 -m pip install",
            "pip3 install",
            "先 which pip 看一眼再说"
        ],
        "source_section": "第 15 讲 · Python 程序开发环境",
        "statement_md": "★★★ 实测：本机 `pip` 与 `python` 可能指向**两个不同的 Python 安装**。所以装包时推荐怎么写？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`python3 -m pip install ...`。**\n\n`python3 -m pip` 的语义是「**用我现在这个 Python 解释器去跑它自己的 pip 模块**」—— 解释器和 pip **必然配套**，装到哪去一目了然。\n\n裸 `pip` 则是一个**独立的可执行入口**，它被哪个 Python 拥有，取决于 `PATH` 顺序和安装方式（尤其装了 Anaconda 之后，`~/anaconda3` 里那一套会和系统的并存）。\n\n★ **典型症状**：\n```\n$ pip install requests        # 提示装好了\n$ python3 -c \"import requests\"  # ModuleNotFoundError\n```\n—— 因为它装到了**另一个** Python 里。\n\n**排查工具**：\n```bash\npython3 -m pip show requests      # 看它到底来自哪个目录\nwhich -a python3                  # 装了哪些 python3\npython3 -c \"import sys; print(sys.executable, sys.prefix)\"\n```\n\n★ 一个更隐蔽的同族坑：**先用 `dnf install python3-xxx` 装了一个库，后来又 `pip install xxx` 装同名库** → 两个版本同时存在于不同目录，`import` 到哪个取决于 `sys.path` 顺序 → 表现为「怎么改了没用」。\n\n★ 记住这一条的模式：**凡是有「裸命令」和「`-m` 形式」两种写法的，永远选 `-m` 形式** —— 它把「用哪个解释器」这件事钉死在工作目录之外。"
            }
        ]
    },
    {
        "title": "tkinter 报 ModuleNotFoundError 说明 Python 装坏了",
        "subject": "linux",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 3,
        "total_score": 8,
        "tags": [
            "python",
            "tkinter",
            "devel",
            "第 15 讲"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 15 讲 · Python 程序开发环境",
        "statement_md": "在 Fedora 上 `import tkinter` 报 `ModuleNotFoundError`，说明 Python 安装损坏了，需要重装 Python。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "错",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|错\n|错误\n|×\n|F\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**错。`tkinter` 在 Fedora 上被拆成了独立的子包 `python3-tkinter`，装它就行。**\n\n```bash\nsudo dnf install python3-tkinter\n```\n\n★ 这是 Fedora 的一个通用规律：**Python 标准库被拆包**。教材时代「装一个 `python3` 包全给了」，现在是分开的：\n\n| 想要的东西 | Fedora 上要装的包 |\n|---|---|\n| `tkinter`（图形界面） | `python3-tkinter` |\n| IDLE（自带编辑器） | `python3-idle`（它依赖 tkinter）|\n| 编译 C 扩展（`Python.h`） | `python3-devel` |\n| 开发用的库文件 | `python3-devel` |\n\n★ 「`Python.h: No such file or directory`」同理 —— 缺 `python3-devel`。**这和第 13 讲「编译 GTK 要 `gtk4-devel`」是同一条规律**：\n\n> **Fedora 系：要编译就必须装 `-devel` 包。**\n\n★ 顺带一条：**连 `idle` 命令都没有**也别慌，它在 `python3-idle` 里，Fedora 上要单独装 —— 教材「Python 的获取与安装」那一节，在 Fedora 44 上九成可以跳过（系统自带 `python3`）。"
            }
        ]
    },
    {
        "title": "Fedora 44 上装 JDK 8 为什么失败",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "eclipse",
            "jdk",
            "fedora",
            "第 16 讲"
        ],
        "choices": [
            "镜像源没同步全，换一个源就好",
            "这个包在 Fedora 42 被 retired（下架）了",
            "需要先启用 extra 仓库",
            "要加 --nogpgcheck 才能装"
        ],
        "source_section": "第 16 讲 · 集成开发环境 Eclipse 的使用",
        "statement_md": "照教材 16.2.1 执行 `sudo dnf install java-1.8.0-openjdk`，报 `Unable to find a match`。原因？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`java-1.8.0-openjdk` 在 Fedora 42 被 retired —— 已经下架了。**\n\n★ 换镜像源无效：**这不是同步问题，是上游没有这个包了。**\n\n这条被下架的路线走了三部曲：\n```\nFedora 39~41   标记废弃，安装时打印警告\nFedora 42      retired —— 从仓库里移除\nFedora 44      系统 JDK 是 java-25-openjdk（LTS）\n```\n\n★ **所以教材 16.2.1 那一节照做会失败** —— 不是「版本旧了」，是「这条路被拆了」。\n\n**要 JDK 8 的正确姿势**（走 Adoptium）：\n```bash\nsudo dnf install adoptium-temurin-java-repository\nsudo dnf install temurin-8-jdk\n```\n但先问自己：**真的需要 8 吗？** 教材用它只是当年的默认，新代码用系统自带的 Java 25 完全没问题。\n\n★ 顺带一条同族规律：**Fedora 仓库里装不到的东西，先查是不是 retired** —— 这个判断在第 16 讲出现了两次（JDK 8 和 Eclipse IDE 本身）。"
            }
        ]
    },
    {
        "title": "为什么 dnf 装不到 Eclipse IDE",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "eclipse",
            "安装",
            "ECJ",
            "第 16 讲"
        ],
        "choices": [
            "包名打错了，应该叫 eclipse-ide",
            "Fedora 仓库里没有 Eclipse IDE，只有 ecj、eclipse-swt 这些零件",
            "需要先装 JDK 8 才能装 Eclipse",
            "必须用 flatpak 才能装"
        ],
        "source_section": "第 16 讲 · 集成开发环境 Eclipse 的使用",
        "statement_md": "`sudo dnf install eclipse` 报 `Unable to find a match`。为什么？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**Fedora 仓库里没有 Eclipse IDE** —— 只有 **`ecj`**（Eclipse 的 Java 编译器）和 **`eclipse-swt`** 这类**库**。\n\n★ 两个原因：\n1. Eclipse 是**季度发布**（每年 3/6/9/12 月），节奏和发行版对不上；\n2. 它**自带 p2 更新机制**（Eclipse 世界的软件源），自己就能装插件、升级，不需要发行版代管。\n\n**装 Eclipse 走过的三条路**（仍然没有 dnf 这条）：\n```bash\n① 官网 Installer（推荐新手）\n② 官网 tar.gz 解压即用\n③ Flatpak\n```\n\n★ **别把 `ecj` 当成 Eclipse**：`ecj` 是 Eclipse 的**Java 编译器**，是一个命令行工具，不是 IDE。\n\n★ 这里藏着一个第 16 讲的核心知识点：**Eclipse 编译 Java 用的是自己的 ECJ，不是 `javac`** —— 两者在泛型推断、注解处理等边界上判断可能不同。所以「Eclipse 里编译通过」**不等于**「`javac` / Maven 也通过」，**最终交付和 CI 以 `javac` 为准**。\n\n★ 顺带把 JDK 的装法记住，这个是真有 dnf 包的：\n```bash\nsudo dnf install java-25-openjdk-devel\n```\n（**要 `-devel`** —— `javac` / `jar` / `javap` 都在里面，只装 JRE 的话 `javac` 会报 command not found。）"
            }
        ]
    },
    {
        "title": "javac 编译成功却运行时报 ClassNotFoundException",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 5,
        "total_score": 10,
        "tags": [
            "eclipse",
            "javac",
            "classpath",
            "包名",
            "第 16 讲"
        ],
        "choices": [
            "少写了 -cp out",
            "javac 没加 -d，.class 没按包名建目录，落错了位置",
            "类名拼错了",
            "需要加 --release 选项"
        ],
        "source_section": "第 16 讲 · 集成开发环境 Eclipse 的使用",
        "statement_md": "源文件首行是 `package com.example.demo;`。\n\n`javac Demo.java` **退出码 0（编译成功）**，但 `java -cp . com.example.demo.Demo` 报 `ClassNotFoundException`。原因？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`javac` 会「编译成功」但把 `.class` 放错位置。**\n\n源文件里有 `package com.example.demo;` 时，`.class` **必须**落在 `com/example/demo/` 目录下 —— **包名与目录必须一一对应**，这是 Java 的硬约束。\n\n```\njavac Demo.java                  # ❌ 退出码 0，但 Demo.class 落在当前目录\njavac -d out Demo.java           # ✅ 落成 out/com/example/demo/Demo.class\n```\n\n★ 这是「**编译通过 ≠ 能跑**」的教科书案例：**编译器认为语法没问题就返回 0**，至于产物放得对不对，它不负责。\n\n★ 顺带两个同族的「找不到类」：\n```bash\njava Hello.class                 # ❌ java 后面是「类名」不是文件名\n                                 #    报 ClassNotFoundException: Hello.class\njava -cp out Demo                # ❌ 有包名的类要写全名 com.example.demo.Demo\njava -cp out com.example.demo.Demo   # ✅\n```\n\n★ **根因值得记住**：**Java 没有独立的「链接」步骤。**\nC 的「找不到符号」在链接期就报出来，而 Java 的「找不到类」**全都在运行时才炸** —— 所以 `jar` 打包、`-cp` 指定路径，本质上是在补上 C 那边「链接器」的位置。"
            }
        ]
    },
    {
        "title": "classpath 的分隔符",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 3,
        "total_score": 10,
        "tags": [
            "eclipse",
            "classpath",
            "跨平台",
            "第 16 讲"
        ],
        "choices": [
            "分号 ;",
            "冒号 :",
            "逗号 ,",
            "与平台无关，都一样"
        ],
        "source_section": "第 16 讲 · 集成开发环境 Eclipse 的使用",
        "statement_md": "指定多个 classpath 条目时，**Linux** 上用的分隔符是？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**Linux / macOS 用冒号 `:`；Windows 用分号 `;`。**\n\n```bash\n# Linux\njava -cp \"libs:.\" com.example.demo.Demo\n# Windows\njava -cp \"libs;.\" com.example.demo.Demo\n```\n\n★ **同一行命令换个平台就废** —— 这是讲义里 ★★★ 实测过的一条。**写文档、写 README、写 CI 脚本时必须两个都写。**\n\n★ 三条配套规矩：\n1. **classpath 才是 Java 的「搜索路径」** —— 它对应 Python 的 `sys.path`、C 的 `-I` / `-L`。「我明明有这个类」这类问题，十有八九是 classpath 指错了；\n2. **不给 `-cp` 时默认就是 `.`（当前目录）** —— 所以「在 A 目录编译、跑到 B 目录去执行」会报 `NoClassDefFoundError`：**换目录就等于换了搜索范围**；\n3. **用 `-cp` 显式给路径，别指望默认值** —— 这和「第 15 讲一律写 `python3 -m pip`」是同一种**防御性写法**：把「我用的是哪个」写死在命令里。\n\n★ 有意思的是，同一个坑在 C 那边叫「`-I` / `-L` 没给对」，在 Python 那边叫「`sys.path` 顺序不对」—— **语言换了，问题还是那些问题。**"
            }
        ]
    },
    {
        "title": "限制最低运行版本该用哪个选项",
        "subject": "linux",
        "line": "text",
        "question_type": "single_choice",
        "difficulty": 4,
        "total_score": 10,
        "tags": [
            "eclipse",
            "--release",
            "class 版本",
            "javap",
            "第 16 讲"
        ],
        "choices": [
            "-source 11 -target 11",
            "--release 11",
            "-target 11 就够了",
            "-java 11"
        ],
        "source_section": "第 16 讲 · 集成开发环境 Eclipse 的使用",
        "statement_md": "用新 JDK 编译，但希望产物能在 **Java 11** 上运行。发布时应该用哪个选项？",
        "input_format": "",
        "output_format": "一个选项字母（`A`~`D`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "B",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|B\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**`--release 11`。**\n\n★ 两者的差别是一句话：\n\n| 选项 | 管什么 | 漏掉了什么 |\n|---|---|---|\n| `-source 11 -target 11` | 语法 + 字节码版本 | **不管 API** —— 你调用了 Java 12+ 才有的库方法，照样在 Java 11 上崩 |\n| **`--release 11`** | 语法 + 字节码 + **可用 API** | —— 它是完整的三件套 |\n\n所以：**发布永远用 `--release`。**\n\n★ 报错长什么样（对方机器上）：\n```\nUnsupportedClassVersionError: Demo has been compiled by\na more recent version of the Java Runtime\n```\n根因是 **class 文件里的 `major` 版本号**。\n\n★ 顺便记住这条公式和它的实测值：\n\n```\nmajor = Java 版本 + 44\n```\n| Java 版本 | 8 | 11 | 17 | 21 |\n|---|---|---|---|---|\n| class major | 52 | 55 | 61 | 65 |\n\n★ 兼容是**单向**的：**新 JVM 能跑旧 class**（本机实证过），**反过来不行**。所以「用新 JDK 编、发给用旧 JDK 的人」必须显式降目标版本。\n\n★ 想知道一个 `.class` 到底是什么版本，一条命令：\n```bash\njavap -v Demo.class | grep major\n```\n（`javap` 一个顶三个：`-c` 看字节码、`-v` 看常量池与版本、**`-p` 看 private 成员** —— 默认它只显示 public。）"
            }
        ]
    },
    {
        "title": "运行 .class 要写 java Hello.class",
        "subject": "linux",
        "line": "text",
        "question_type": "true_false",
        "difficulty": 2,
        "total_score": 8,
        "tags": [
            "eclipse",
            "java",
            "类名",
            "第 16 讲"
        ],
        "choices": [
            "对",
            "错"
        ],
        "source_section": "第 16 讲 · 集成开发环境 Eclipse 的使用",
        "statement_md": "编译出 `Hello.class` 之后，要用 `java Hello.class` 来运行它。",
        "input_format": "",
        "output_format": "`对` 或 `错`（写 `正确`/`√`/`T` 也认）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "错",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|错\n|错误\n|×\n|F\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**错。`java` 后面要写的是「类名」，不是文件名。**\n\n```bash\njava Hello            # ✅ 运行\njava Hello.class      # ❌ 它去找一个叫 \"Hello.class\" 的类\n                      #    报 ClassNotFoundException: Hello.class\n```\n\n★ 这条错法很常见，因为 `.class` 是「文件」，而 `java` 想要的是「类」。\n\n**三条路的正确写法**：\n```bash\njavac Hello.java && java Hello      # ① 经典两步（编译 + 运行）\njava Hello.java                     # ② JDK 11+ 单文件源码启动（不落 .class）\njava -jar app.jar                   # ③ 跑打包好的 jar\n```\n\n★ **② 要专门说一下**：`java Hello.java` 是 JDK 11 引入的**单文件源码启动** —— 编译**在内存里完成**，**不会留下 `.class` 文件**。所以它适合「快速试一下」，但要交付给别人还是得走 ① 或 ③。\n\n★ 顺带一条同一个「名字 vs 文件」的坑：**有包名的类必须写全名** ——\n`java -cp out com.example.demo.Demo` ✅ / `java -cp out Demo` ❌。类的全名是「包名 + 类名」，`java` 一个字母都不能少。"
            }
        ]
    },
    {
        "title": "链接库的 -l 该写在哪",
        "subject": "linux",
        "line": "text",
        "question_type": "multiple_choice",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "gcc",
            "链接",
            "选项顺序",
            "第 12 讲"
        ],
        "choices": [
            "`gcc main.o -lm -o app`",
            "`gcc -lm main.o -o app`",
            "`gcc main.c -lm -o app`",
            "`gcc -o app -lm main.o`"
        ],
        "source_section": "第 12 讲 · GCC 的使用与开发",
        "statement_md": "在 Fedora 上用 `gcc` 链接一个需要 `libm` 的程序，要链接的目标文件是 `main.o`。\n\n下列哪些写法能**正确链接**？\n\n**多选题**：正确选项不止一个，点选切换，再次点击可取消。",
        "input_format": "",
        "output_format": "若干个选项字母，按字母升序连写（如 `AC`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "AC",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|AC\n|CA\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "判断标准只有一条：**`-l` 必须出现在「用到它的目标文件」之后。**\n\n链接器（GNU ld）是从左往右扫的：读到一个 `.o`，先记下它**还没被满足的符号**；再读到 `-lm`，才去 `libm` 里把这些符号找出来填上。所以 `-l` 排在前面时，那一刻**还没有任何未定义符号**，`libm` 被整个跳过 → 最后仍然报：\n```\nundefined reference to `sqrt'\n```\n\n| 写法 | 顺序对吗 | 说明 |\n|---|---|---|\n| `gcc main.o -lm -o app` | ✅ | 目标是 `.o`，只要它排在 `-lm` 前面 |\n| `gcc main.c -lm -o app` | ✅ | 源文件会被编成 `.o` 放在**同一个位置**，仍在 `-lm` 前 |\n| `gcc -lm main.o -o app` | ❌ | `-lm` 跑到目标文件前面，库被跳过 |\n| `gcc -o app -lm main.o` | ❌ | `-o app` 不影响顺序，`main.o` 仍然在 `-lm` 之后 |\n\n★ **同一条规则还解释另一件事**：为什么 GTK / Qt 的 `$(pkg-config --libs ...)` 也非得写在源文件后面。`pkg-config` 吐出来的 `-l` 顺序是**排好**的，唯一要做的就是别自己重排、别把它提前。"
            }
        ]
    },
    {
        "title": "四道工序各停在哪一步",
        "subject": "linux",
        "line": "text",
        "question_type": "multiple_choice",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "gcc",
            "四道工序",
            "预处理",
            "汇编",
            "第 12 讲"
        ],
        "choices": [
            "`gcc -E hello.c -o hello.i` 只做预处理，`hello.i` 是展开后的 C 代码",
            "`gcc -S hello.c` 停在编译之后，产出汇编文件 `hello.s`",
            "`gcc -c hello.c -o hello.o` 产出的是可以直接运行的可执行文件",
            "`gcc hello.c -o hello` 会依次走完预处理 / 编译 / 汇编 / 链接"
        ],
        "source_section": "第 12 讲 · GCC 的使用与开发",
        "statement_md": "关于 `gcc` 把 `hello.c` 变成可执行文件的过程，下列哪些说法**正确**？\n\n**多选题**：正确选项不止一个，点选切换，再次点击可取消。",
        "input_format": "",
        "output_format": "若干个选项字母，按字母升序连写（如 `AC`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ABD",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ABD\n|ADB\n|BAD\n|BDA\n|DAB\n|DBA\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "四道工序各有各的干活人：\n\n| 工序 | 谁干 | 停在这步的选项 | 产物 |\n|---|---|---|---|\n| ① 预处理 | `cpp` | `-E` | `.i`（展开后的 C 代码） |\n| ② 编译 | `cc1` | `-S` | `.s`（汇编） |\n| ③ 汇编 | `as` | `-c` | `.o`（可重定位目标文件） |\n| ④ 链接 | `ld` | （没有选项，走到头） | 无后缀的可执行文件 |\n\n所以 A ✅、B ✅、D ✅（不带任何「停一下」的选项，四步一次走完）。\n\n**C ❌**：`.o` 只是**目标文件**，里面的符号还没被链接、地址还没定下来，单独跑不起来 —— 它离可执行文件还差最后一趟 `ld`。\n\n★ **看后缀就能判断停在哪一步**：`.i` / `.s` / `.o` / 无后缀，一眼对应「哪道工序刚做完」。这也是排查「我明明改了代码怎么没变」的入口 ——先看命令停在哪一步，再看那一步的产物。"
            }
        ]
    },
    {
        "title": "几十行 undefined reference 从哪下手",
        "subject": "linux",
        "line": "text",
        "question_type": "multiple_choice",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "gtk",
            "编译",
            "pkg-config",
            "undefined reference",
            "第 13 讲"
        ],
        "choices": [
            "换成 `gcc hello.c -o hello $(pkg-config --cflags --libs gtk4)`",
            "让 `$(pkg-config --libs gtk4)` 出现在**源文件之后**",
            "把 `-l` 那一串**提到源文件前面**，gcc 自己就能找到库",
            "这是代码写错了，应该逐行改代码"
        ],
        "source_section": "第 13 讲 · GTK 图形界面程序设计",
        "statement_md": "写了个 GTK4 程序，`gcc hello.c -o hello` 报了几十行 `undefined reference to gtk_...`。\n\n下列哪些做法是**对的**？\n\n**多选题**：正确选项不止一个，点选切换，再次点击可取消。",
        "input_format": "",
        "output_format": "若干个选项字母，按字母升序连写（如 `AC`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "AB",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|AB\n|BA\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "**几十行 `undefined reference` ≈ 链接参数没给对**，几乎从来不是代码的错。\n\nA ✅ `gcc hello.c -o hello` 里**一个 `-l` 都没有** —— gcc 不会自动替你去连 GTK，所有 `gtk_*` 符号自然全是「未定义」。`pkg-config` 就是替你把 `-I`（头文件在哪）和 `-l`（库在哪）一次吐全的工具。\n\nB ✅ 而且**必须在源文件之后**：`-l` 写在前面时，链接器读到它那一刻还没有任何未定义符号，整库被跳过，等读到源文件才发现缺符号 —— 照样报错。`pkg-config` 吐出来的顺序已经是排好的，**唯一要做的就是别重排**。\n\nC ❌ 方向反了，理由同上（这正是「越改越乱」的那一步）。\n\nD ❌ 几十行 `undefined reference` 从头到尾都是**同一批符号**在报，这是「库没连上」的典型长相；真的代码写错，报的是你自己的函数名、行号也对得上。\n\n★ 先自查一行：`pkg-config --modversion gtk4` 有输出，说明包在、名字对；没输出就是 `gtk4-devel` 没装，或包名写成了 `gtk+-3.0`。"
            }
        ]
    },
    {
        "title": "教材的 GTK 写法搬到 Fedora 44 上",
        "subject": "linux",
        "line": "text",
        "question_type": "multiple_choice",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "gtk",
            "GTK4",
            "信号",
            "教材对照",
            "第 13 讲"
        ],
        "choices": [
            "`pkg-config` 的包名从 `gtk+-3.0` 变成 `gtk4`（那个加号没了）",
            "显示窗口用 `gtk_window_present()`，不再需要 `gtk_widget_show_all()`",
            "二维表格容器 `GtkGrid` 在 GTK4 里仍然可用",
            "信号连接改成了 `&Class::method` 的指针写法"
        ],
        "source_section": "第 13 讲 · GTK 图形界面程序设计",
        "statement_md": "教材蓝本是 Fedora 30，里面的 GTK 写法搬到 Fedora 44（GTK4）上，下列哪些说法**正确**？\n\n**多选题**：正确选项不止一个，点选切换，再次点击可取消。",
        "input_format": "",
        "output_format": "若干个选项字母，按字母升序连写（如 `AC`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ABC",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ABC\n|ACB\n|BAC\n|BCA\n|CAB\n|CBA\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "A ✅ 包名一路是 `gtk+-2.0` → `gtk+-3.0` → **`gtk4`**。那个加号是 GTK3 时代的产物，4 去掉了 —— 写成 `gtk+-4.0` 会直接查不到包。\n\nB ✅ GTK4 里控件**默认可见**，`gtk_widget_show` / `show_all` 那一套不需要了；窗口用 `gtk_window_present()`（它同时负责「显示 + 抢焦点 + 提到最前」）。\n\nC ✅ `GtkTable` 整个类没了（3.4 起就已废弃），替代品正是 **`GtkGrid`**。\n\nD ❌ **这是 Qt 的写法，不是 GTK 的。** GTK 一直是字符串信号名：\n```c\ng_signal_connect(app, \"activate\", G_CALLBACK(on_activate), NULL);\n```\n★ 代价是**拼错信号名编译期不报错**：`\"activat\"` 少一个 `e` 照样编译通过，运行时 GLib 只打一条 warning，然后**静默什么都不发生**。要查就用 `--g-fatal-warnings` 启动，或检查 `g_signal_connect` 的返回值是否为 0。"
            }
        ]
    },
    {
        "title": "Qt 的 signals 与槽",
        "subject": "linux",
        "line": "text",
        "question_type": "multiple_choice",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "qt",
            "信号槽",
            "moc",
            "lambda",
            "第 14 讲"
        ],
        "choices": [
            "`signals:` 下的函数只写声明、**不写实现**（实现由 moc 生成）",
            "槽就是普通成员函数，需要正常写实现",
            "新式 `connect` 用 `&Class::method` 指针写法，成员名写错在**编译期**就报错",
            "只有老式的 `SIGNAL()` / `SLOT()` 宏写法才能连 lambda"
        ],
        "source_section": "第 14 讲 · Qt 图形界面程序设计",
        "statement_md": "关于 Qt 的 `signals` / 槽，下列哪些说法**正确**？\n\n**多选题**：正确选项不止一个，点选切换，再次点击可取消。",
        "input_format": "",
        "output_format": "若干个选项字母，按字母升序连写（如 `AC`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ABC",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ABC\n|ACB\n|BAC\n|BCA\n|CAB\n|CBA\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "A ✅ 这是最容易记混的一处：「**信号不写实现，槽要写实现**」。信号的实现由 **moc**（元对象编译器）在预处理之后生成 ——这也是为什么改过 `Q_OBJECT` 相关的东西必须让 moc 重跑一次。\n\nB ✅ 槽没有任何语法魔法，就是个普通成员函数，可以正常调用、正常写实现、正常被 `connect` 连上。\n\nC ✅ 新式写法的本质是把函数**指针**交给 `connect`：\n```cpp\nconnect(btn, &QPushButton::clicked, this, &MyClass::onClick);\n```\n成员名写错 → 取不到成员 → **当场编译报错**；IDE 也能跳转、能重构。\n\nD ❌ 正好说反了。老写法 `SIGNAL(clicked())` 把函数名当**字符串**，编译期查不出来，拼错只在运行时打一条 warning ——**而且它连不了 lambda**；能连 lambda 恰恰是新语法额外带来的好处。"
            }
        ]
    },
    {
        "title": "Qt6 里的这些类去哪了",
        "subject": "linux",
        "line": "text",
        "question_type": "multiple_choice",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "qt",
            "Qt6",
            "迁移",
            "Qt5Compat",
            "第 14 讲"
        ],
        "choices": [
            "`QRegExp` 移入 Qt5Compat，替代品是 `QRegularExpression`",
            "`QTextStream::setCodec()` 被移除，改用 `setEncoding()`",
            "`QStringRef` 仍然留在 Qt6 的核心模块里",
            "`QVector` 现在是 `QList` 的别名（两者已经合并）"
        ],
        "source_section": "第 14 讲 · Qt 图形界面程序设计",
        "statement_md": "从 Qt5 迁到 Qt6，下列哪些对应关系**正确**？\n\n**多选题**：正确选项不止一个，点选切换，再次点击可取消。",
        "input_format": "",
        "output_format": "若干个选项字母，按字母升序连写（如 `AC`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ABD",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ABD\n|ADB\n|BAD\n|BDA\n|DAB\n|DBA\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "A ✅ `QRegExp` 被 `QRegularExpression` 取代，老类**移出核心模块**、挪进 `Qt5Compat`。临时救急可以 `QT += core5compat`，长期要换掉。\n\nB ✅ 注意这一条是**被删除**（不是废弃）：函数名换了，`setCodec()` 直接不存在，编译期就报错。\n\nC ❌ `QStringRef` 也挪进了 `Qt5Compat`，替代品是 **`QStringView`**。「名字带 QString 所以肯定在核心模块里」是个想当然的坑。\n\nD ✅ `QList` 与 `QVector` 两者合一，`QVector` 保留为 `QList` 的别名 ——以后不用再纠结「该用哪个」。\n\n★ 记这一类迁移有个好办法：**先问「它现在在哪」**。\n\n| 情况 | 例子 |\n|---|---|\n| 还在核心模块里（改个名字就行）| `setCodec` → `setEncoding`、`QList`/`QVector` 合一 |\n| 挪去了 `Qt5Compat`（要么加模块、要么换类）| `QRegExp` / `QTextCodec` / `QStringRef` |\n| 真删除（必须重写）| Qt Quick Controls 1 |"
            }
        ]
    },
    {
        "title": "方括号与双方括号",
        "subject": "linux",
        "line": "text",
        "question_type": "multiple_choice",
        "difficulty": 3,
        "total_score": 14,
        "tags": [
            "shell",
            "条件判断",
            "引号",
            "重定向",
            "第 11 讲"
        ],
        "choices": [
            "`[` 是一条命令（等价于 `test`），不是 shell 语法",
            "`[[ ]]` 里的 `>` 也会像 `[ ]` 一样触发文件重定向",
            "变量没赋值时 `[ $v = x ]` 会报 `unary operator expected`，给变量加双引号即可",
            "`[[ 10 > 9 ]]` 做的是字符串比较、结果为假；数值比较要写 `-gt` 或 `(( ))`"
        ],
        "source_section": "第 11 讲 · Shell 程序设计",
        "statement_md": "关于 shell 里的条件测试，下列哪些说法**正确**？\n\n**多选题**：正确选项不止一个，点选切换，再次点击可取消。",
        "input_format": "",
        "output_format": "若干个选项字母，按字母升序连写（如 `AC`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ACD",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ACD\n|ADC\n|CAD\n|CDA\n|DAC\n|DCA\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "A ✅ `[` 就是 `/usr/bin/[` 这个可执行文件（等价于 `test`）。**既然是普通命令，参数就要先被 shell 展开、分词、glob** ——「90% 的 shell 玄学问题」都出在这句话上。\n\nB ❌ 说反了：`[[ ]]` 是**语法**，内部不重定向、不做分词、不做 glob；真正会出事的是 `[ 10 > 9 ]` —— `>` 被当成重定向，当前目录会凭空多出一个叫 `9` 的空文件，而判断结果还莫名其妙。\n\nC ✅ `$v` 展开成空串后，`[ = x ]` 只收到两个参数，命令 `[` 发现第一个参数 `=` 不是合法的一元运算符，直接报错退出。加上双引号变成 `[ \"\" = x ]`（三个参数），走二元比较规则，合法且判为假。\n\nD ✅ `[[ ]]` 里的 `>` 是**字符串比较**（字典序）：`'1'`(0x31) < `'9'`(0x39)，所以 `[[ 10 > 9 ]]` 是假。数值比较要写成 `[[ 10 -gt 9 ]]` 或 `(( 10 > 9 ))`。"
            }
        ]
    },
    {
        "title": "让 httpd 对外可访问的正确步骤",
        "subject": "linux",
        "line": "text",
        "question_type": "multiple_choice",
        "difficulty": 4,
        "total_score": 14,
        "tags": [
            "httpd",
            "firewalld",
            "SELinux",
            "systemctl",
            "第 07 讲"
        ],
        "choices": [
            "`sudo dnf install httpd`",
            "`sudo systemctl enable --now httpd`",
            "直接把 SELinux 关掉，否则网页一定打不开",
            "`sudo firewall-cmd --permanent --add-service=http` 之后还要 `sudo firewall-cmd --reload`"
        ],
        "source_section": "第 07 讲 · 常用网络服务",
        "statement_md": "在 Fedora 上把 Apache（httpd）配到「装好 + 开机自启 + 立刻能访问」的状态，下列哪些做法是**正确步骤**？\n\n**多选题**：正确选项不止一个，点选切换，再次点击可取消。",
        "input_format": "",
        "output_format": "若干个选项字母，按字母升序连写（如 `AC`）",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ABD",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ABD\n|ADB\n|BAD\n|BDA\n|DAB\n|DBA\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "A ✅ 先有软件包才谈得上服务。\n\nB ✅ `--now` 是「立刻启动」的简写，`enable --now` = **开机自启 + 现在就起来**，一次把两件事办完；只 `enable` 不 `--now` 的话，当前这次开机里服务仍然是停的。\n\nC ❌ 关 SELinux 是**甩掉安全机制**，不是配置。正确做法是按需放行：用 `setsebool -P <布尔值> on` 打开对应的布尔开关（`-P` 才会持久化），或者用 `semanage fcontext` 改规则、再用 `restorecon -Rv 路径` 刷到实际文件上。★ 「只做 `semanage` 不 `restorecon`」是这一步最常见的漏做 ——规则写进去了，但文件上的标签还是旧的，照样拒绝访问。\n\nD ✅ `--permanent` 只把规则**写进配置文件**，当前运行中的防火墙规则并没有变；必须再来一条 `firewall-cmd --reload` 让它生效。★ 「明明配了却没用」的头号原因就是这个 —— 少一条 `--reload`。"
            }
        ]
    }
]
