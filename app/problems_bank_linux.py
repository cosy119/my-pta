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
                "expected_stdout": "|cp -a ~/docs /tmp/\n|cp -a ~/docs /tmp\n|cp -rp ~/docs /tmp/\n",
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
                "expected_stdout": "|tar -czf project.tar.gz ~/project\n|tar czf project.tar.gz ~/project\n|tar -zcf project.tar.gz ~/project\n",
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
                "explanation": "**`cp -r ~/docs /tmp/`** —— 复制目录**必须**加递归开关 （`-r`、`-R` 或 `-a`）。\n\n不加会得到：\n```\ncp: -r not specified; omitting directory '/home/{user}/docs'\n```\n⚠️ **注意这是个「温柔的错误」**：它只打印一句警告、跳过这个目录，而不是报错崩掉 —— 在脚本里跑的话，你以为复制成功了，其实什么都没发生。\n\n另外两个选项：\n- `-u`（update）只在目标比源**旧**时才复制 —— 跟「能不能复制目录」无关\n- `-i`（interactive）覆盖前先问一句 —— 同理，不解决递归问题\n\n★ 更好的选择是 **`cp -a ~/docs /tmp/`**：递归 + 保留权限时间。"
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
        "title": "装完系统，一条命令问出 Fedora 主版本号",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "实验 1",
            "os-release",
            "grep",
            "装机"
        ],
        "choices": [],
        "source_section": "实验 1 · 环境搭建",
        "statement_md": "**作业 1（装机）**：装好 Fedora Workstation 后，第一件事是确认装的是哪一版。\n\n要求：只从 `/etc/os-release` 里取出**主版本号那一行**，输出形如 `VERSION_ID=44`。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "grep ^VERSION_ID= /etc/os-release",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|grep ^VERSION_ID= /etc/os-release\n|grep VERSION_ID= /etc/os-release\n|grep '^VERSION_ID=' /etc/os-release\n|grep ^VERSION_ID= /etc/os-release\n|grep \"^VERSION_ID=\" /etc/os-release\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`grep ^VERSION_ID= /etc/os-release`。\n\n`/etc/os-release` 是 systemd 定下的**跨发行版标准文件**（Fedora 上它是指向 `/usr/lib/os-release` 的软链，`grep` 会顺着链读）。`^` 锚定行首，只捞出 `VERSION_ID=` 开头的那一行。\n\n★ 为什么不用 `cat /etc/fedora-release` —— 那行写的是 `Fedora release 44 (Forty Four)`，代号随版本变；`VERSION_ID` 永远是纯数字，拿来当判据最稳。\n\n★ **迁移**：任何发行版先 `grep VERSION_ID /etc/os-release`，比 `lsb_release -a` 靠谱 —— 后者在最小化安装里经常没装。"
            }
        ]
    },
    {
        "title": "查内核版本（只要版本号，不要整串信息）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "实验 1",
            "uname",
            "内核"
        ],
        "choices": [],
        "source_section": "实验 1 · 环境搭建",
        "statement_md": "你的驱动装不上，厂商让你报**内核版本**。\n\n要求：只输出内核版本号，形如 `6.8.5-301.fc40.x86_64`，不要 `Linux hostname ...` 那一整行。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "uname -r",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|uname -r\n|uname --kernel-release\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`uname -r`（长写法 `uname --kernel-release`）。\n\n`uname` 各选项是**各管一段**的，不是「越多越详细」：\n- `-r` → 内核 release 号（`6.8.x-fc40.x86_64`）\n- `-a` → 全部信息（内核名 + 主机名 + 版本 + 架构 + …）\n- `-s` → 只有 `Linux`\n- `-m` → 架构（`x86_64`）\n\n★ 报漏洞、报驱动问题时要的是 `-r`；`-a` 那一整行带主机名，贴到公开场合等于自曝主机名。\n\n★ **迁移**：`cat /proc/version` 也能看到，但它带编译时间与 gcc 版本，脚本里要干净的值，还是 `uname -r`。"
            }
        ]
    },
    {
        "title": "用相对路径从 /usr/local/bin 退回 /usr",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "实验 2",
            "cd",
            "相对路径"
        ],
        "choices": [],
        "source_section": "实验 2 · 基本命令",
        "statement_md": "**实验 2 第 1 步**：你现在在 `/usr/local/bin`。\n\n要求：**不许写绝对路径**，用 `..` 退回 `/usr`。\n\n写出这条命令（假设起点就是 `/usr/local/bin`）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
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
                "explanation": "`cd ../..`。\n\n`/usr/local/bin` 往上走：一次 `..` 到 `/usr/local`，再一次 `..` 到 `/usr`，所以是**两级**。`cd ../../` 末尾多一个 `/` 也完全等价。\n\n★ 最常见的错：把 `..` 当成「回根目录」或「回上一个访问过的目录」。`..` 永远只表示**父目录**，与 shell 的历史无关。\n\n★ 辨析：`cd -` 才是「回上一次待过的目录」（靠 `$OLDPWD`），它跟 `..` 是两个完全不同的概念。\n\n★ **迁移**：路径里连续几层 `..` 都能合并——`a/b/../../c` 等价于 `c`，写脚本时先化简再传参，能少踩很多「文件找不到」。"
            }
        ]
    },
    {
        "title": "打印当前所在目录的绝对路径",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "实验 2",
            "pwd",
            "绝对路径"
        ],
        "choices": [],
        "source_section": "实验 2 · 基本命令",
        "statement_md": "**实验 2 第 2 步**：连着 `cd` 了好几次，你现在到底在哪？\n\n要求：输出**绝对路径**（形如 `/usr/local/bin`），不要只显示目录名。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "pwd",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|pwd\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`pwd`（print working directory）。\n\n★ 为什么强调「绝对路径」：`pwd` 默认带 `-L`，输出的是**逻辑路径**——如果你是从软链 `cd` 进去的，它显示软链那条路径。想要**物理路径**（把软链解析成真实位置）得用 `pwd -P`。\n\n★ 脚本里的坑：`pwd` 是外部命令，`echo $PWD` 是读 shell 变量。两者值一般一样，但 `cd` 失败时 `$PWD` 可能没更新——**判断 `cd` 成没成功，看退出码 `$?`，别信 `$PWD`**。\n\n★ **迁移**：脚本开头写 `cd \"$(dirname \"$0\")\" || exit 1`，让脚本总是以自己所在目录为基准，这是最稳的写法。"
            }
        ]
    },
    {
        "title": "一条命令建出 a1/a2/a3/a4 四级目录",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "实验 3",
            "mkdir",
            "多级目录"
        ],
        "choices": [],
        "source_section": "实验 3 · 常用命令",
        "statement_md": "**实验 3 第 1 步**：在 `/tmp` 下建一条四层深的目录链 `a1/a2/a3/a4`。\n\n要求：**只准用一条 `mkdir`**，不许分开建四次。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "mkdir -p /tmp/a1/a2/a3/a4",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|mkdir -p /tmp/a1/a2/a3/a4\n|mkdir --parents /tmp/a1/a2/a3/a4\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`mkdir -p /tmp/a1/a2/a3/a4`。\n\n`-p`（`--parents`）一个选项干两件事：\n1. **逐级自动创建**中间的父目录（不用先建 a1 再建 a2…）\n2. **已存在也不报错**（幂等）\n\n★ 没 `-p` 会怎样：`mkdir: cannot create directory '/tmp/a1/a2': No such file or directory` —— 因为父目录还不存在。\n\n★ 幂等这一点在脚本里价值最大：`mkdir -p /var/log/myapp` 写两遍也不会失败，所以安装脚本里到处是它。\n\n★ **迁移**：`mkdir -p a/{b,c,d}` 的花括号展开一次建三个平级目录，建项目骨架时很省事。"
            }
        ]
    },
    {
        "title": "把整棵目录树复制走，并且保留权限与时间戳",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "实验 3",
            "cp",
            "归档复制",
            "preserve"
        ],
        "choices": [],
        "source_section": "实验 3 · 常用命令",
        "statement_md": "**实验 3 第 2 步**：把 `/tmp/a1`（含下面三层子目录）整个复制到 `/usr`。\n\n要求：复制完**权限、属主、时间戳都和原来一样**，符号链接照抄成符号链接（不要跟进去复制目标内容）。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "cp -a /tmp/a1 /usr/",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|cp -a /tmp/a1 /usr/\n|cp -a /tmp/a1 /usr\n|cp -a /tmp/a1/ /usr/\n|cp -a /tmp/a1/ /usr\n|cp --archive /tmp/a1 /usr/\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`cp -a /tmp/a1 /usr/`（`-a` = `--archive`）。\n\n`-a` 是**一个等于一串**的选项：`-dR --preserve=all`\n- `-R` 递归\n- `-d` 不跟随符号链接（链路照抄）\n- `--preserve=all` 保 权限 + 属主 + 时间戳 + 扩展属性\n\n★ 别用 `cp -r`：它**不保属主与时间戳**，也不处理「软链变成实体文件」的问题（不加 `-d` 时 `-r` 会跟进去）。\n\n★ 末尾 `/` 的区别（很多人的误区）：`cp -a a1 /usr` 与 `cp -a a1/ /usr` 在这里结果**一样**，都是往 `/usr/a1` 里放。真正决定「拷进去还是改名」的是**目标是否已存在**——目标目录存在就放进去，不存在就改名复制。\n\n★ **迁移**：备份整个 `/etc` 用 `cp -a /etc /backup/`；要跨机器保持原样，`cp -a` 强于 `tar` 以外的任何方式。"
            }
        ]
    },
    {
        "title": "只看目录本身那一行，不要列里面的内容",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "实验 3",
            "ls",
            "-d"
        ],
        "choices": [],
        "source_section": "实验 3 · 常用命令",
        "statement_md": "**实验 3 第 3 步**：想知道 `/usr/a1` 这个**目录本身**的权限和属主。\n\n要求：`ls` 只输出它**自己那一行**，不许把它里面的四个子目录刷出来。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ls -ld /usr/a1",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ls -ld /usr/a1\n|ls -dl /usr/a1\n|ls -ld /usr/a1/\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`ls -ld /usr/a1`。\n\n- `-l` 长格式（权限、硬链接数、属主、属组、大小、时间、名字）\n- `-d` **对目录本身操作**，而不是「列出目录里的内容」\n\n★ 这是 `ls` 最反直觉的一个选项：平时 `ls -l /usr` 列的是**里面的东西**；加 `-d` 才变成「看这个目录当作一个文件时的属性」。\n\n★ 参数顺序无所谓：`-ld` 与 `-dl` 完全等价（判题系统会把短选项簇排序后比）。\n\n★ **迁移**：想知道 `/tmp` 这个目录权限是不是 1777，只能 `ls -ld /tmp`；`ls -l /tmp` 看到的是里面每个人文件。"
            }
        ]
    },
    {
        "title": "把 /usr/test5 打包成 gzip 压缩包",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "实验 4",
            "tar",
            "gzip",
            "打包"
        ],
        "choices": [],
        "source_section": "实验 4 · 综合命令",
        "statement_md": "**实验 4 第 1 步**：把 `/usr/test5` 目录树打包并压缩，产出 `test5.tar.gz`（放在当前目录）。\n\n要求：**打包 + gzip 压缩一步完成**，并且显示处理了哪些文件。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "tar -czvf test5.tar.gz /usr/test5",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|tar -czvf test5.tar.gz /usr/test5\n|tar czvf test5.tar.gz /usr/test5\n|tar --create --gzip --verbose --file test5.tar.gz /usr/test5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`tar -czvf test5.tar.gz /usr/test5`。\n\n四个字母各管一段：\n- `-c` create，**创建**归档\n- `-z` 走 **gzip**\n- `-v` verbose，边打边报文件名\n- `-f` 后面跟**归档文件名**（`-f` 必须紧挨着文件名）\n\n★ 顺序的坑：`-f` 后面那一个词一定会被当成文件名。写成 `tar -cfv test5.tar.gz /usr/test5`，tar 会以为归档叫 `v`，于是多出一个叫 `v` 的文件、`test5.tar.gz` 反而被当要打包的路径。\n\n★ `-Z` 不是 gzip！`-Z` 调的是 `compress`（老式 `.Z` 格式）。教材和网上抄来的 `-Zcvf` 是错的。\n\n★ **迁移**：zstd 用 `--zstd`，xz 用 `-J`，bzip2 用 `-j`，其余字母位置不变。"
            }
        ]
    },
    {
        "title": "把压缩包解到 /usr/local（别解在当前目录）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "实验 4",
            "tar",
            "解压",
            "-C"
        ],
        "choices": [],
        "source_section": "实验 4 · 综合命令",
        "statement_md": "**实验 4 第 2 步**：`test5.tar.gz` 已经做好，现在要解压到 `/usr/local` 下，最终得到 `/usr/local/test5/`。\n\n要求：**不许先 cd 过去**，一条命令完成。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "tar -xzvf test5.tar.gz -C /usr/local",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|tar -xzvf test5.tar.gz -C /usr/local\n|tar xzvf test5.tar.gz -C /usr/local\n|tar --extract --gzip --verbose --file test5.tar.gz -C /usr/local\n|tar -xzvf test5.tar.gz --directory=/usr/local\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`tar -xzvf test5.tar.gz -C /usr/local`。\n\n- `-x` extract，解包（与 `-c` 二选一）\n- `-C`（`--directory`）**先切到目标目录再解**，解包结束后**不会**把你留在那个目录里\n\n★ 为什么强调「不许 cd」：脚本里 `cd /usr/local && tar …` 会让**后续所有相对路径**都基于 `/usr/local`，忘了 `cd` 回来就是一连串「文件找不到」。`-C` 是局部生效的，没这个副作用。\n\n★ 打包时若用了**绝对路径**（`tar -czf x.tar.gz /usr/test5`），GNU tar 会把开头的 `/` 去掉，所以包里是 `usr/test5/`，解到 `/usr/local` 就变成 `/usr/local/usr/test5` —— **想解出 `/usr/local/test5` 得用 `-C /`，或者打包前 `cd /usr` 再打相对路径**。\n\n★ **迁移**：`tar -tzf x.tar.gz` 先看一眼包内路径，再决定 `-C` 放哪，这是解压前最省事的一次检查。"
            }
        ]
    },
    {
        "title": "给 /usr/local/sdutshare 在根目录挂一个软链 /myshare",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "实验 4",
            "ln",
            "符号链接"
        ],
        "choices": [],
        "source_section": "实验 4 · 综合命令",
        "statement_md": "**实验 4 第 3 步**：想让 `/myshare` 这个路径指向 `/usr/local/sdutshare`，像目录一样能用。\n\n要求：建**符号链接**（不是硬链接）。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ln -s /usr/local/sdutshare /myshare",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ln -s /usr/local/sdutshare /myshare\n|ln --symbolic /usr/local/sdutshare /myshare\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`ln -s /usr/local/sdutshare /myshare`。\n\n`ln -s 目标 链接名` —— **源在前，链接名在后**，与 `cp 源 目标` 的顺序一致，但方向相反：`cp` 造副本，`ln -s` 造指针。\n\n★ 顺序写反是最常见的错：`ln -s /myshare /usr/local/sdutshare` 会在 `/usr/local` 里造一个叫 `sdutshare` 的链接指向 `/myshare`，而 `/usr/local/sdutshare` 若是已存在的目录，还会在里面塞一个 `myshare`。\n\n★ 硬链接不能跨文件系统，也不能链目录 —— 所以这里只能 `-s`。\n\n★ **迁移**：软链用**相对路径**写目标（`ln -s ../sdutshare myshare`）更适合随目录整体搬家；用绝对路径则目标位置一变就断。检查断链：`find / -xtype l`。"
            }
        ]
    },
    {
        "title": "把单词表按字典序逆序排",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "实验 4",
            "sort",
            "逆序"
        ],
        "choices": [],
        "source_section": "实验 4 · 综合命令",
        "statement_md": "**实验 4 第 4 步**：有个文件 `/tmp/words.txt`，每行一个单词。\n\n要求：按**字典序倒序**输出到屏幕（不改原文件）。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "sort -r /tmp/words.txt",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|sort -r /tmp/words.txt\n|sort --reverse /tmp/words.txt\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`sort -r /tmp/words.txt`。\n\n`sort` 默认按当前 locale 的字典序**升序**；`-r`（`--reverse`）翻过来。\n\n★ 要落到文件里必须重定向：`sort -r f > g`。`sort -r f -o f` 才是**原地**排序（`-o` 会先写临时文件再替换，安全）；写成 `sort -r f > f` 会把文件**清空**——shell 先截断再执行 `sort`。\n\n★ 数字排序别用 `-r`：`sort file` 会把 `10` 排在 `9` 前面，要 `sort -n`（或 `-h` 识别人性化单位）。\n\n★ **迁移**：`sort -k2 -n` 按第二列数值排；`sort -t: -k3` 以冒号分列。排序题九成的坑都在「没声明字段分隔符」和「按文本比了数字」。"
            }
        ]
    },
    {
        "title": "把两个文件的内容拼成第三个文件",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "实验 4",
            "cat",
            "重定向"
        ],
        "choices": [],
        "source_section": "实验 4 · 综合命令",
        "statement_md": "**实验 4 第 5 步**：`file11` 和 `file12` 各有一段内容，要把它们**首尾相接**写进 `file13`。\n\n要求：`file11` 在前、`file12` 在后；一条命令完成。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "cat file11 file12 > file13",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|cat file11 file12 > file13\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`cat file11 file12 > file13`。\n\n`cat` 接多个文件时**按给出的顺序依次输出**，`>` 把整串重新导向 `file13`。\n\n★ `>` 会**先清空**目标再写；`>>` 是追加。所以 `cat a b > c` 里若 `c` 恰好是 `a` 或 `b`，内容就没了——「输出到源文件之一」是这类操作最隐蔽的自毁。\n\n★ 另一个容易踩的：`cat a b > c` 里 `c` 若已存在且是软链，写入会跟着软链走（`>` 不替换软链本身）；要替换软链本身得 `rm c && cat a b > c`。\n\n★ **迁移**：拼三个以上文件也是同一招；想加分隔符就 `cat a <(echo '---') b > c`（bash 进程替换）。"
            }
        ]
    },
    {
        "title": "把 11.txt 改成 rwxr-x--x（数字模式）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "实验 5",
            "chmod",
            "八进制",
            "权限"
        ],
        "choices": [],
        "source_section": "实验 5 · 用户与权限",
        "statement_md": "**实验 5 第 1 步**：`11.txt` 现在的权限不对，要改成 `-rwxr-x--x`。\n\n要求：用**八进制数字模式**一条命令改掉，不要用字母模式。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "chmod 751 11.txt",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|chmod 751 11.txt\n|chmod 0751 11.txt\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`chmod 751 11.txt`。\n\n三位八进制依次是 **属主 / 属组 / 其他**，每位由 r=4、w=2、x=1 相加：\n- 属主 `rwx` = 4+2+1 = **7**\n- 属组 `r-x` = 4+0+1 = **5**\n- 其他 `--x` = 0+0+1 = **1**\n\n所以是 `751`。\n\n★ 硬链接陷阱：`chmod` 只有一个写法 —— 它会改**inode**，同一个 inode 的所有硬链接**权限一起变**（这与 `chown` 不同，`chown` 也是改 inode，同样全变）。\n\n★ `-rwxr-x--x` 开头那个 `-` 是文件类型位，不是权限位；`d` 是目录、`l` 是软链。别把它算进数字里。\n\n★ **迁移**：目录的 `x` 位含义与文件不同 —— 目录没有 `x` 就**进不去**（哪怕有 `r` 能列出名字）。所以目录常用 `755`、`750`，很少给 `644`。"
            }
        ]
    },
    {
        "title": "把 abc 整棵树（含子目录）交给 user02",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "实验 5",
            "chown",
            "递归",
            "属主"
        ],
        "choices": [],
        "source_section": "实验 5 · 用户与权限",
        "statement_md": "**实验 5 第 2 步**：`abc` 目录下有多层文件，要全部改成属主与属组都是 `user02`。\n\n要求：**递归**，一条命令，别一个一个改。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "chown -R user02:user02 abc",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|chown -R user02:user02 abc\n|chown -R user02.user02 abc\n|chown --recursive user02:user02 abc\n|chown -R user02:user02 abc/\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`chown -R user02:user02 abc`。\n\n- `-R`（`--recursive`）递归整棵子树\n- `属主:属组` 用冒号分隔；老式写法 `user02.user02` 也认（但用户名里若带点会歧义，优先用冒号）\n- 只写 `user02` 时**只改属主**，属组保持不动\n\n★ 只改属组可以写 `chown :user02 abc`（冒号前留空）。\n\n★ `-R` 的副作用：符号链接默认**不跟随**（改的是链接自身），想连目标一起改要 `-h` 或 `-L`，含义完全不同。\n\n★ 实操时才发现的坑：`chown` 改的是 **inode**，同 inode 的硬链接会一起变；要只影响一个路径，先确认 `ls -li` 的链接数。\n\n★ **迁移**：拷完家目录忘了属主，`chown -R ~user ~user` 一条修好——这是接手别人机器时最常敲的一条。"
            }
        ]
    },
    {
        "title": "改成 744 之后，长格式里长什么样",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "实验 5",
            "chmod",
            "744"
        ],
        "choices": [],
        "source_section": "实验 5 · 用户与权限",
        "statement_md": "**实验 5 第 3 步**：某文件执行 `chmod 744 f`。\n\n要求：写出这条命令（题目要考的是「744 对应哪几个符号位」，所以请同时把它落到文件上）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "chmod 744 f",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|chmod 744 f\n|chmod 0744 f\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`chmod 744 f`。\n\n744 = 属主 `rwx`（7）+ 属组 `r--`（4）+ 其他 `r--`（4），长格式显示为 `-rwxr--r--`。\n\n★ 这里最容易错的是把 744 记成 `-rwxr--r--` 之外的什么 ——**4 只有读，没有执行**，所以属组和其他都是 `r--` 而不是 `r-x`。`744` 与 `755` 差的就是那一个 `x`。\n\n★ 脚本文件给了 `744` 会怎样：属主自己能跑，同组和别人的账号想跑就是 `Permission denied`。所以放在公共目录里的脚本一般给 `755`。\n\n★ **迁移**：`stat -c '%a %A %n' f` 一条命令同时看八进制与符号位，比 `ls -l` 逐个对更快。"
            }
        ]
    },
    {
        "title": "400 再给「其他」加写权限，最后是多少",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "实验 5",
            "chmod",
            "符号模式"
        ],
        "choices": [],
        "source_section": "实验 5 · 用户与权限",
        "statement_md": "**实验 5 第 4 步**：某文件原权限 `400`（`-r--------`）。\n\n任务：用**符号模式**给「其他用户（o）」**加上写权限**。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "chmod o+w f",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|chmod o+w f\n|chmod o=w f\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`chmod o+w f`（若原来 o 位为空，`o=w` 结果相同）。\n\n符号模式的三个部分：**谁 / 怎么改 / 什么权限**\n- 谁：`u` 属主、`g` 属组、`o` 其他、`a` 全部\n- 怎么改：`+` 加、`-` 减、`=` 直接赋值（会把该组其余位清掉）\n- 什么：`r`/`w`/`x`\n\n★ `400` 加 `o+w` = `402`（`-r------w-`），**不是 420、也不是 602** —— 因为 `w` 的权值是 2，加在「其他」那一位上。\n\n★ `+` 与 `=` 的区别是本题真正的考点：`o=w` 会把 o 位原有的 `r`/`x` 一并清掉；原来 o 是全空的，所以两者结果一样。换个起点（比如 `o=rx`）结果就完全不同了。\n\n★ **迁移**：想知道某文件到底该给什么，`ls -l` 看现状再决定用 `+`/`-` 微调，别一上来 `=`，那是覆盖式改。"
            }
        ]
    },
    {
        "title": "把 temp1 全部交给 root",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "实验 5",
            "chown",
            "root"
        ],
        "choices": [],
        "source_section": "实验 5 · 用户与权限",
        "statement_md": "**实验 5 第 5 步**：`temp1` 这个文件属于普通用户，要移交 root（属主与属组都改成 `root`）。\n\n要求：只改这一个文件，不要递归。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "chown root:root temp1",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|chown root:root temp1\n|chown root.root temp1\n|chown root: temp1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`chown root:root temp1`。\n\n★ 关键点：`chown` 改属主是**特权操作**，普通用户只能「把自己的文件送给别人」且**不能改属组到不在自己组列表里的组**；要改给别人必须 `sudo`。所以真跑起来是 `sudo chown root:root temp1`。\n\n★ `root.root` 是老的 BSD 写法，GNU coreutils 仍兼容；`root:`（冒号后留空）等价于 `root:root` 再跟文件名？不完全等价 —— `chown root: temp1` 里的冒号表示「属组改成当前登录主组」，在 root 下就是 `root:root`。三者结果相同、语义不同。\n\n★ 与 `chmod` 的分工：`chmod` 管「谁能读/写/执行」，`chown` 管「这个文件是谁的」。改权限永远改不了属主，反之亦然。\n\n★ **迁移**：把网站目录交给 web 用户：`chown -R nginx:nginx /usr/share/nginx/html`。"
            }
        ]
    },
    {
        "title": "列出所有条目（含隐藏），按修改时间倒序，大小人性化",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "ls",
            "隐藏文件",
            "排序",
            "-h"
        ],
        "choices": [],
        "source_section": "命令特训 · 文件与目录",
        "statement_md": "你要看一个目录里**最近改过**的东西，包括以点开头的隐藏文件，大小要能一眼看懂（`4.0K` 而不是 `4096`）。\n\n写出这条命令（就在当前目录）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ls -lath",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ls -lath\n|ls -alht\n|ls -lat --human-readable\n|ls -lAhT\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`ls -lath`。四个选项各管一件事：\n- `-a` 含隐藏文件（`.` 与 `..` 也在里面；只想去掉这两个用 `-A`）\n- `-t` 按**修改时间**排序，新的在前\n- `-h` 大小人性化（`-h` 必须和 `-l` 一起才有意义）\n- `-l` 长格式\n\n★ 参数顺序完全无所谓：`-lath`、`-alht`、`-t -h -a -l` 判题都算同一个（短选项簇会被排序去重后比）。\n\n★ `-h` 是 `--human-readable` 的短写法，但它**只对 `-l` 里的 Size 列生效**；单敲 `ls -h` 什么也不会变。\n\n★ **迁移**：想按时间**正序**（老的在前）用 `-tr`；想按大小排用 `-S`。`ls -lt | head` 是「最近改了啥」的日常起手式。"
            }
        ]
    },
    {
        "title": "只列出子目录，不要文件",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "ls",
            "-d",
            "通配",
            "find"
        ],
        "choices": [],
        "source_section": "命令特训 · 文件与目录",
        "statement_md": "当前目录里文件和子目录混在一起。你只想看**有哪些子目录**。\n\n写出这条命令（不要递归进去）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ls -d */",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ls -d */\n|ls -d */ .*/ 2>/dev/null\n|find . -maxdepth 1 -type d\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`ls -d */`。\n\n`*/` 是 shell 的**通配**：只匹配「以 `/` 结尾」的名字，而只有目录才会展开成这种形式（文件不会 `*/` 匹配上）。`-d` 让 `ls` 停留在**目录本身**，不要展开里面的内容。\n\n★ 少了 `-d` 会怎样：`ls */` 会把每个子目录**里面的内容**全列出来，输出立刻变成几百行。这是本题唯一的分水岭。\n\n★ 想连隐藏目录一起要：`ls -d */ .*/`（`.*/` 顺带把 `.` 和 `..` 也带出来，常见做法是再 `grep -v '^\\.\\.\\?$'` 过滤掉）。\n\n★ **迁移**：`find . -maxdepth 1 -type d` 是更精确的写法，它不依赖 shell 通配、也不怕名字里有空格；`-maxdepth 1` 就是「别递归」的意思。"
            }
        ]
    },
    {
        "title": "列出某目录下所有普通文件的完整路径",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "find",
            "-type",
            "普通文件"
        ],
        "choices": [],
        "source_section": "命令特训 · 文件与目录",
        "statement_md": "要从 `/etc` 往下把**所有普通文件**（不含目录、不含软链）的路径列出来，用于喂给另一个脚本。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "find /etc -type f",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|find /etc -type f\n|find /etc -type f -print\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`find /etc -type f`。\n\n`-type` 的取值是本题的核心：\n- `f` 普通文件\n- `d` 目录\n- `l` 符号链接\n- `b`/`c` 块设备/字符设备\n\n★ 注意 `-type f` **不包含**软链 —— 软链是 `l`，哪怕它指向一个普通文件。想「软链也当文件算」得写 `-type f -o -type l`（或用 GNU 的 `-xtype f`）。\n\n★ `find` 默认就打印路径（`-print` 可省），所以两个写法等价。\n\n★ **迁移**：`find` 的输出**带 `./` 前缀**看情况——`find .` 会输出 `./a.txt`，`find /etc` 输出 `/etc/a.conf`。脚本里拿它做参数，路径基准必须想清楚。"
            }
        ]
    },
    {
        "title": "一次建出三个空文件",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "touch",
            "花括号展开",
            "创建文件"
        ],
        "choices": [],
        "source_section": "命令特训 · 文件与目录",
        "statement_md": "要同时创建 `a.txt`、`b.txt`、`c.txt` 三个空文件。\n\n写出这条命令（一条命令搞定，别写三行）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "touch a.txt b.txt c.txt",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|touch a.txt b.txt c.txt\n|touch {a,b,c}.txt\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`touch a.txt b.txt c.txt`（或花括号展开 `touch {a,b,c}.txt`）。\n\n`touch` 的本职其实是**改时间戳**（把访问/修改时间刷成当前），「文件不存在就建一个空文件」只是它的副作用 —— 但这个副作用太好用，所以大家都当它是「创建文件」。\n\n★ `{a,b,c}.txt` 是 **bash 的花括号展开**（brace expansion），由 shell 先展开成三个词再交给 `touch`。注意它**不经过文件系统**，即使文件名里有通配符也会照样生成。在 `sh`（dash）里不支持花括号展开。\n\n★ **迁移**：`touch -t 202610190800 f` 可以把时间戳设成指定时刻；`touch -d '2 days ago' f` 更好读。造测试数据时很常用。"
            }
        ]
    },
    {
        "title": "只把文件时间戳刷成当前，内容一个字都别动",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "touch",
            "mtime",
            "时间戳"
        ],
        "choices": [],
        "source_section": "命令特训 · 文件与目录",
        "statement_md": "`/var/log/app.log` 被一个监控脚本盯着，只要它的 mtime 太旧就会报警。\n\n你要把它的 mtime 刷成**现在**，但**绝对不能改内容**。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "touch /var/log/app.log",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|touch /var/log/app.log\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`touch /var/log/app.log`。\n\n这是 `touch` 的**本职用途**，不是副作用：它只更新时间戳，不会打开文件写入，所以内容分毫不动。\n\n★ 对比一下常见的错法：`echo '' >> /var/log/app.log` 确实也刷了 mtime，但**往文件末尾追加了一个换行**——日志解析器会看到一个空行，`wc -l` 也会 +1。`touch` 才是干净的做法。\n\n★ `touch` 会同时更新 **atime 和 mtime**；只想改 atime 用 `touch -a`，只想改 mtime 用 `touch -m`。\n\n★ **迁移**：`touch -r ref.txt target.txt` 把 target 的时间刷成和 ref 一致 —— 造「看起来很久没改」的测试文件时很省事。"
            }
        ]
    },
    {
        "title": "复制文件到另一个名字（目标已存在就覆盖）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "cp",
            "覆盖",
            "备份"
        ],
        "choices": [],
        "source_section": "命令特训 · 文件与目录",
        "statement_md": "把 `report.txt` 复制一份叫 `report.bak`，**覆盖**已有同名文件、不要提问。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "cp report.txt report.bak",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|cp report.txt report.bak\n|cp -f report.txt report.bak\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`cp report.txt report.bak`（`-f` 是「强制」，一般可省）。\n\n`cp 源 目标`：目标不存在就新建；存在就**直接覆盖内容**，且**保留目标原有的权限与属主**（这一点很容易被忽略）。\n\n★ 覆盖时 inode 不变：所以原文件的硬链接看到的也是新内容。\n\n★ 为什么 `-f` 一般可省：`cp` 默认不提问；只有你的 `alias cp='cp -i'` 或系统里配了 `cp -i` 时才会问。`-f` 是硬关掉这种交互。\n\n★ **迁移**：想「保留源文件权限」而不是继承目标的，用 `cp -p`；整个目录树用 `cp -a`。日常改配置文件前先 `cp -a /etc/nginx/nginx.conf{,.bak}` 备份，花括号展开一次到位。"
            }
        ]
    },
    {
        "title": "改名（同目录内移动）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "mv",
            "改名"
        ],
        "choices": [],
        "source_section": "命令特训 · 文件与目录",
        "statement_md": "把 `old.log` 改名为 `new.log`，内容与原位置都不变。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "mv old.log new.log",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|mv old.log new.log\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`mv old.log new.log`。\n\n★ 关键认知：Linux **没有独立的 rename 命令**，改名就是 `mv`。同目录内 `mv` 只改目录项，**不改 inode 内容**，所以瞬间完成、不占额外空间（哪怕文件有 10G，也一样是瞬间）。\n\n★ 目标已存在时 `mv` **直接覆盖，且不提示**（除非配了 `-i` 别名）。这是 `mv` 最危险的地方：`mv a b` 里 b 已存在，b 就没了，没有回收站。\n\n★ 跨文件系统 `mv` 会退化成「复制 + 删除」，此时 inode 变了、属主可能变、耗时也和大小有关。\n\n★ **迁移**：批量改名别用 `mv *.log *.txt`（通配会展开成多对参数，`mv` 只认最后一个是目标）——用 `rename` 或 `for` 循环。"
            }
        ]
    },
    {
        "title": "删除空目录",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "rmdir",
            "空目录",
            "安全"
        ],
        "choices": [],
        "source_section": "命令特训 · 文件与目录",
        "statement_md": "`/tmp/empty_dir` 已经空了，删掉它。\n\n要求：用**专门删空目录**的那个命令（不要用能删一切的 `rm -r`）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "rmdir /tmp/empty_dir",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|rmdir /tmp/empty_dir\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`rmdir /tmp/empty_dir`。\n\n`rmdir` 的设计哲学就是**安全**：目录非空时它会直接报错拒绝（`Directory not empty`），所以永远不会误删数据。\n\n★ `rm -r` 也能删空目录，但它是「什么都能删」的推土机。脚本里删临时目录用 `rmdir`，等于给自己加了一道保险：**万一目录里还有东西，它会失败而不是静默删掉**。\n\n★ `rmdir -p a/b/c` 可以「删完 c 再顺手删空的 b、a」，清除多级空目录链时很好用。\n\n★ **迁移**：`rm -rf` 之前先 `ls` 一眼，或者干脆 `rm -ri` 让它逐个确认。生产环境里 `rm -rf $VAR/` 里 `$VAR` 为空就等于 `rm -rf /`，加 `set -u` 能防住。"
            }
        ]
    },
    {
        "title": "递归删除整个目录树",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "rm",
            "递归删除",
            "-rf"
        ],
        "choices": [],
        "source_section": "命令特训 · 文件与目录",
        "statement_md": "`/tmp/build` 整个目录（含所有子目录和文件）都要清掉。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "rm -rf /tmp/build",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|rm -rf /tmp/build\n|rm -r /tmp/build\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`rm -rf /tmp/build`。\n\n- `-r`（`--recursive`）递归\n- `-f`（`--force`）忽略不存在的文件、不提示确认\n\n★ 只写 `rm -r` 时，遇到**只读文件**会逐个问你要不要删；`-f` 让它闭嘴照删。批量清临时目录几乎总是要 `-rf`。\n\n★ 顺序无所谓：`rm -fr` 一样。但**别写 `rm -rf / tmp/build`**（多一个空格就是删根目录，某些 `rm` 实现有保护，但不能赌）。\n\n★ 变量为空是头号杀手：`rm -rf $DIR/` 里 `DIR` 没赋值就成了 `rm -rf /`。脚本里用 `rm -rf \"${DIR:?}\"` —— `:?` 会在变量为空时直接报错退出。\n\n★ **迁移**：想「删之前先看一眼」，`ls -R /tmp/build | head -50`；重要目录先 `mv` 到回收目录放一天，比 `rm` 稳。"
            }
        ]
    },
    {
        "title": "给同一个文件再起一个名字（不复制内容）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "ln",
            "硬链接",
            "inode"
        ],
        "choices": [],
        "source_section": "命令特训 · 文件与目录",
        "statement_md": "`/data/big.img` 有 8G，你想在 `/backup/big.img` 也能访问到它，但**不想多占 8G 空间**。\n\n要求：同一文件系统内，用**硬链接**。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ln /data/big.img /backup/big.img",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ln /data/big.img /backup/big.img\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`ln /data/big.img /backup/big.img`（不带 `-s` 就是硬链接）。\n\n硬链接的本质：**多个目录项指向同一个 inode**。所以不占额外空间、删除其中一个名字文件照样在（`ls -l` 第二列那个数字就是链接数，减到 0 才真删数据）。\n\n★ 硬链接的两条硬限制：\n1. **不能跨文件系统**（inode 编号只在单个文件系统内唯一）\n2. **不能链目录**（会造出环，`fsck` 会疯）\n\n★ 与软链的区别：硬链接是「另一个名字」，软链是「一个指向路径的文件」。删掉源文件，硬链接照样能读；软链会变成断链。\n\n★ **迁移**：`ls -li` 看 inode 号，两个名字 inode 相同就是硬链接；`find /data -samefile /data/big.img` 可以找出所有硬链接。"
            }
        ]
    },
    {
        "title": "查一个软链到底指向哪里",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "readlink",
            "软链",
            "realpath"
        ],
        "choices": [],
        "source_section": "命令特训 · 文件与目录",
        "statement_md": "`/usr/bin/python3` 很可能是个软链。想知道它**链到哪个真实路径**。\n\n要求：只输出目标路径，不要那一整行 `ls -l` 的权限信息。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "readlink /usr/bin/python3",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|readlink /usr/bin/python3\n|readlink -f /usr/bin/python3\n|namei -l /usr/bin/python3 | tail -1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`readlink /usr/bin/python3`。\n\n`readlink` 只干一件事：把软链的目标路径打印出来，输出干净，最适合塞进脚本变量：`TARGET=$(readlink /usr/bin/python3)`。\n\n★ `-f`（`--canonicalize`）会**一路跟到底**，把多级软链全解析成最终的真实绝对路径。链条长的时候（`python3 → python3.12 → /usr/bin/python3.12`）只有 `-f` 能给到终点。\n\n★ `ls -l` 也能看出目标，但它输出的是整行，而且**相对软链只显示相对写法**，你还得自己拼路径。\n\n★ **迁移**：`readlink -f .` 等于 `pwd -P`（物理路径）；排查「命令到底跑的是哪个文件」用 `type -a` 或 `which -a`，再用 `readlink -f` 看终点。"
            }
        ]
    },
    {
        "title": "删掉目录里所有内容，但保留目录本身",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "rm",
            "清空目录",
            "隐藏文件"
        ],
        "choices": [],
        "source_section": "命令特训 · 文件与目录",
        "statement_md": "`/var/www/html` 这个目录要留着（属主属组都不能变），但里面的**所有文件和子目录**都要清空。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "rm -rf /var/www/html/*",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|rm -rf /var/www/html/*\n|rm -rf /var/www/html/* /var/www/html/.[!.]*\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`rm -rf /var/www/html/*`（严格说还要处理隐藏文件，见下）。\n\n★ 为什么不能 `rm -rf /var/www/html`：那会把目录本身也删掉，重建出来的属主属组、SELinux 上下文、挂载点全都变了。「清空」和「删除重建」在权限体系里是两件事。\n\n★ 隐藏文件是这道题真正的坑：`*` **不匹配**以点开头的名字。所以要连 `.*` 一起删：`rm -rf /var/www/html/* /var/www/html/.[!.]*`\n（`.[!.]*` 是「点开头、第二个字符不是点」，避免把 `.` 和 `..` 也带进来）\n\n★ bash 里更省心的写法：`shopt -s dotglob` 之后 `*` 就含隐藏文件了。\n\n★ **迁移**：`find /var/www/html -mindepth 1 -delete` 是另一种干净写法（`-mindepth 1` 正好排除目录自身）。"
            }
        ]
    },
    {
        "title": "复制时只覆盖「源比目标新」的那些",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 4,
        "total_score": 18,
        "tags": [
            "cp",
            "-u",
            "增量",
            "rsync"
        ],
        "choices": [],
        "source_section": "命令特训 · 文件与目录",
        "statement_md": "`/src` 和 `/dst` 是两份同构的目录。你要做增量同步：**只复制比目标更新的文件**，别浪费时间重拷全部。\n\n要求：用 `cp` 的选项，不要用 `rsync`。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "cp -ru /src/. /dst/",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|cp -ru /src/. /dst/\n|cp -u -r /src/. /dst/\n|cp -a -u /src/. /dst/\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`cp -ru /src/. /dst/`。\n\n`-u`（`--update`）的判据是 **mtime**：源比目标新（或目标不存在）才复制，否则跳过。\n\n★ `/src/.` 那个点很关键：`cp -r /src /dst/` 会造出 `/dst/src/`，而 `cp -r /src/. /dst/` 是把 src 的**内容**倒进 dst。少了这个点，整个目录结构就多套一层。\n\n★ `-u` 只看**时间**，不看内容。文件被删了它不会删（还是同步工具更合适），时间戳被改过（`touch`）它就误判。所以真要同步还是 `rsync -a`。\n\n★ **迁移**：`rsync -av --delete src/ dst/` 才是完整的镜像同步（`--delete` 才会删掉目标里多出来的文件）。`cp -u` 适合「补一遍新文件」这种轻量场景。"
            }
        ]
    },
    {
        "title": "看文件占用的 inode 号",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "ls",
            "-i",
            "inode",
            "stat"
        ],
        "choices": [],
        "source_section": "命令特训 · 文件与目录",
        "statement_md": "两个文件看起来内容一样，你要确认它们**是不是同一个 inode**（即硬链接）。\n\n要求：`ls` 输出里带 inode 号。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ls -li file1 file2",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ls -li file1 file2\n|ls -il file1 file2\n|stat -c '%i %n' file1 file2\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`ls -li file1 file2`。\n\n`-i` 让 `ls` 在最前面多打一列 **inode 编号**。两行 inode 相同 → 同一个文件（硬链接）；不同 → 就是两个独立文件。\n\n★ inode 是**每个文件系统内部**的编号，跨分区不唯一，所以 `ls -i` 的结果不能跨分区比较大小或相等。\n\n★ 第二种写法 `stat -c '%i %n'` 输出更干净，脚本里比对更好解析（`%i` 是 inode，`%n` 是文件名）。\n\n★ **迁移**：`df -i` 看 inode 使用率 —— 「磁盘还有空间但写不进文件」多半是 inode 用完了（海量小文件场景）。"
            }
        ]
    },
    {
        "title": "建多级目录并立刻进去（一条命令）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "mkdir",
            "cd",
            "&&",
            "花括号展开"
        ],
        "choices": [],
        "source_section": "命令特训 · 文件与目录",
        "statement_md": "要创建 `~/project/src/{main,test}` 这套目录并**马上进入 `src`**。\n\n写出这条命令（用 `&&` 串起来）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "mkdir -p ~/project/src/{main,test} && cd ~/project/src",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|mkdir -p ~/project/src/{main,test} && cd ~/project/src\n|mkdir -p ~/project/src/main ~/project/src/test && cd ~/project/src\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`mkdir -p ~/project/src/{main,test} && cd ~/project/src`。\n\n两个知识点叠在一起：\n1. **花括号展开**：`{main,test}` 被 shell 展开成两个路径参数，`mkdir -p` 一次建完\n2. **`&&`**：前一条**成功**才执行后一条。写 `;` 的话，`mkdir` 失败了照样 `cd`（然后 cd 也失败），报错信息会叠成一堆看不出因果。\n\n★ 为什么用 `-p`：父目录 `~/project` 可能不存在；`-p` 逐级创建且**已存在不报错**，重跑安全。\n\n★ **迁移**：`cd` 到不存在的目录会失败，所以「建完就进」必须 `&&` 而不是 `;`。脚本里更稳的写法是 `mkdir -p X && cd X || exit 1` —— 显式失败退出。"
            }
        ]
    },
    {
        "title": "查看目录树结构（不要一堆 ls 输出）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "tree",
            "目录结构",
            "find"
        ],
        "choices": [],
        "source_section": "命令特训 · 文件与目录",
        "statement_md": "给一个目录，想用**树状缩进**看清层级（最多两层），不要 `ls -R` 那种平铺。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "tree -L 2 /etc",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|tree -L 2 /etc\n|tree -L 2 -d /etc\n|find /etc -maxdepth 2 | sort\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`tree -L 2 /etc`。\n\n`-L 2` 限制**递归深度**为 2 层，不然 `/etc` 能刷满整个屏幕。\n\n★ `tree` 不是 coreutils 的一部分，最小化安装常常没有：Fedora 上 `sudo dnf install tree`。没有它时的替代是 `find /etc -maxdepth 2 | sort`（平铺但可控），或者 `ls -R`（平铺且不好读）。\n\n★ 只看目录不要文件：`tree -d`；只看目录且限制深度：`tree -L 2 -d`。\n\n★ **迁移**：`tree -L 1` 是「这目录里大概有什么」最快的一眼；`tree -h --du` 顺便看每层占多大，排查空间问题时比 `du -sh *` 直观。"
            }
        ]
    },
    {
        "title": "把文件内容清空（但保留文件本身与权限）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 4,
        "total_score": 18,
        "tags": [
            "truncate",
            "重定向",
            "日志",
            "inode"
        ],
        "choices": [],
        "source_section": "命令特训 · 文件与目录",
        "statement_md": "`/var/log/app.log` 涨到 2G 了。要**清空内容**，但文件名、属主、权限都必须原样保留（服务还开着这个文件句柄）。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "truncate -s 0 /var/log/app.log",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|truncate -s 0 /var/log/app.log\n|: > /var/log/app.log\n|> /var/log/app.log\n|cat /dev/null > /var/log/app.log\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`truncate -s 0 /var/log/app.log`（或 `: > /var/log/app.log`、`> /var/log/app.log`）。\n\n★ 为什么**不能** `rm` 再 `touch`：那样 inode 变了，而正在写日志的进程**握着旧 inode 的句柄**，会继续往那个已删除的 inode 写 —— `df` 显示空间没释放，`ls` 又看不到文件。这就是经典的「删了日志但磁盘没空出来」。\n\n★ `>` 重定向是**原地截断**（O_TRUNC），inode 不变，所有已打开的句柄立刻看到文件长度归零。这是处理「进程占用日志」的正确姿势。\n\n★ `logrotate` 的 `copytruncate` 选项就是干这件事的；不用它的话通常配 `postrotate` 发信号让进程重开日志。\n\n★ **迁移**：`truncate -s 100M f` 还能把文件**撑大**（稀疏文件），造大文件测限速时很有用，而且不真占磁盘。"
            }
        ]
    },
    {
        "title": "只看前 50 行",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "head",
            "前N行"
        ],
        "choices": [],
        "source_section": "命令特训 · 查看文件内容",
        "statement_md": "`access.log` 有几十万行。你只想看**开头 50 行**。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "head -n 50 access.log",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|head -n 50 access.log\n|head -50 access.log\n|head --lines=50 access.log\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`head -n 50 access.log`。\n\n三种写法都合法：`-n 50`、`-50`（省略 `-n` 的简写）、`--lines=50`。`-50` 这种老写法在新版 coreutils 里仍支持，但脚本里建议写全 `-n 50`，可读性更好。\n\n★ 不写 `-n` 时默认 **10 行**。所以 `head f` 就是前 10 行。\n\n★ **迁移**：`head -n -10 f` 表示「除最后 10 行外的全部」，负数是「从末尾倒数」的意思 —— 这个用法很多人不知道，配合 `tail -n +N` 就能精确切任意区间。"
            }
        ]
    },
    {
        "title": "实时跟踪日志新增内容",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "tail",
            "-f",
            "-F",
            "日志"
        ],
        "choices": [],
        "source_section": "命令特训 · 查看文件内容",
        "statement_md": "服务在跑，你要盯着 `/var/log/messages` **持续输出新行**，而不是只看某一刻。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "tail -f /var/log/messages",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|tail -f /var/log/messages\n|tail -F /var/log/messages\n|tail -f -n 10 /var/log/messages\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`tail -f /var/log/messages`。\n\n`-f`（follow）让 `tail` **不退出**，文件一有新行就刷出来。`Ctrl+C` 结束。\n\n★ `-f` 与 `-F` 的关键差别（生产环境必知）：\n- `-f` 跟的是**文件描述符**。日志被 `logrotate` 改名轮转后，你还钉在旧 inode 上，**新日志一行也看不到**。\n- `-F` = `--follow=name --retry`，跟**文件名**。文件被轮转/删除重建后会自动重新打开。\n\n★ **迁移**：长期盯日志用 `-F`；一次性看增量用 `-f`。配合 `grep` 做过滤：`tail -F app.log | grep -i error`。"
            }
        ]
    },
    {
        "title": "从第 100 行一直看到文件末尾",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "tail",
            "+N",
            "跳过表头"
        ],
        "choices": [],
        "source_section": "命令特训 · 查看文件内容",
        "statement_md": "`data.csv` 前 99 行是表头说明（要跳过），你要从**第 100 行**开始看。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "tail -n +100 data.csv",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|tail -n +100 data.csv\n|tail -n+100 data.csv\n|tail --lines=+100 data.csv\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`tail -n +100 data.csv`。\n\n★ `+N` 是 `tail` 里最容易记反的语法：`-n +100` 表示「**从第 100 行开始**往后全部」，而不是「最后 100 行」（那是 `-n 100`）。\n\n记忆法：`+` 是「起点在正数第 N 行」，`-` 或省略是「尾部倒数 N 行」。\n\n★ 等价思路：`sed -n '100,$p'` 或 `awk 'NR>=100'` 也能干，但 `tail -n +N` 是最省事的。\n\n★ **迁移**：跳过表头还有一个专用写法 `tail -n +2`，处理 CSV 时几乎每天都要用一次。"
            }
        ]
    },
    {
        "title": "只统计文件有多少行",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "wc",
            "-l",
            "行数"
        ],
        "choices": [],
        "source_section": "命令特训 · 查看文件内容",
        "statement_md": "`/etc/passwd` 里有多少个用户？只要**行数**，别的都不要。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "wc -l /etc/passwd",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|wc -l /etc/passwd\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`wc -l /etc/passwd`。\n\n`wc` 三个常用选项各数字段：\n- `-l` 行数（line）\n- `-w` 词数（word）\n- `-c` 字节数（byte）\n- `-m` 字符数（character，多字节字符才和 `-c` 不同）\n\n★ 不写选项时输出三列 `行 词 字节 文件名`。要用这个数字做判断，通常还要 `awk '{print $1}'` 或 `wc -l < f`（重定向进来就没有文件名那一列）。\n\n★ 「行数」的定义是**换行符个数**：文件末尾没有换行符时，`wc -l` 会少算一行。造数据时容易踩。\n\n★ **迁移**：`printf '%s\\n' {1..100} | wc -l` 造 100 行；「有多少条匹配」用 `grep -c` 比 `grep | wc -l` 快。"
            }
        ]
    },
    {
        "title": "同时看行数、词数、字节数",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "wc",
            "统计"
        ],
        "choices": [],
        "source_section": "命令特训 · 查看文件内容",
        "statement_md": "要一次性拿到某个文件的**三个统计值**，不要跑三遍。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "wc /etc/passwd",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|wc /etc/passwd\n|wc -lwc /etc/passwd\n|wc -l -w -c /etc/passwd\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`wc /etc/passwd`（不带选项默认就是行/词/字节三列）。\n\n输出形如：`37  62 1932 /etc/passwd`\n\n★ 三列顺序固定是 **行 → 词 → 字节**，不随你写选项的顺序变。所以 `wc -c -l` 输出的还是行在前。\n\n★ 只要部分列就明确写选项：脚本里解析时优先 `wc -l f | awk '{print $1}'`，别指望「取第一列」永远对。\n\n★ **迁移**：多个文件一起统计时，`wc` 会在最后多打一行 `total`，脚本里遍历文件时要记得跳过它。"
            }
        ]
    },
    {
        "title": "带行号显示文件内容",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "cat",
            "-n",
            "行号"
        ],
        "choices": [],
        "source_section": "命令特训 · 查看文件内容",
        "statement_md": "要给同事贴一段代码片段，需要**行号**方便他定位。\n\n要求：用 `cat`，不要 `nl`。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "cat -n config.conf",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|cat -n config.conf\n|cat --number config.conf\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`cat -n config.conf`。\n\n★ 一个常见误区：**`cat -b` 与 `cat -n` 不同**。`-n` 给**所有行**编号（空行也占号），`-b` 只给**非空行**编号（空行不占号）。贴配置文件时 `-b` 往往更好看，但定位到具体行要 `-n`。\n\n★ `cat -n` 是**显示行号**，不是「统计行数」——统计行数要用 `wc -l`。这是个高频混淆点。\n\n★ `cat` 的编号是**显示层**的，不会写回文件。真想改文件得 `sed -i '=' f` 之类的工具。\n\n★ **迁移**：`nl -ba f` 功能等价且默认不编空行，还能 `nl -s '. ' -w 3` 定制分隔符与宽度。"
            }
        ]
    },
    {
        "title": "分页查看大文件，还能在里面搜索",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "less",
            "分页",
            "搜索"
        ],
        "choices": [],
        "source_section": "命令特训 · 查看文件内容",
        "statement_md": "要读一个 200M 的配置文件。`cat` 会刷屏、`less` 才能翻。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "less config.big",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|less config.big\n|less -N config.big\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`less config.big`。\n\n`less` 的核心操作（比记选项更值钱）：\n- `/关键词` 向下搜，`?关键词` 向上搜，`n`/`N` 跳下一个/上一个\n- `g` 到文件头，`G` 到文件尾，`50g` 跳到第 50 行\n- `PgUp`/`PgDn`/空格 翻页；`q` 退出\n- `-N` 打开行号显示\n\n★ 为什么用 `less` 不用 `more`：`more` **只能往下翻**，而且很多实现不支持回滚。`less` 是 `more` 的超集（名字就是「less is more」的玩笑）。\n\n★ `less` 不会把整个文件读进内存，所以 200M 甚至 10G 都能瞬间打开。\n\n★ **迁移**：`less +F f` 等于 `tail -F`（进入跟随模式，`Ctrl+C` 退出跟随、`F` 再次进入）；管道也能喂给 `less`：`dmesg | less`。"
            }
        ]
    },
    {
        "title": "判断一个文件到底是什么类型",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "file",
            "文件类型",
            "魔数"
        ],
        "choices": [],
        "source_section": "命令特训 · 查看文件内容",
        "statement_md": "有个文件叫 `data`，没有扩展名。你要知道它是文本、gzip 包、还是 ELF 可执行文件。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "file data",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|file data\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`file data`。\n\n`file` 看的是**文件头部的魔数（magic number）**，不是扩展名。所以 `mv a.png b.txt` 之后 `file b.txt` 照样报 `PNG image data`。\n\n★ 这是 Linux 与 Windows 思维差异最大的一处：**Linux 不靠扩展名判断类型**，扩展名只对人类和某些软件有意义。\n\n★ 常见输出：`ASCII text`、`UTF-8 Unicode text`、`gzip compressed data`、`ELF 64-bit LSB executable`、`symbolic link to ...`、`directory`。\n\n★ **迁移**：`file *` 批量判断目录下所有文件；`file -i f` 输出 MIME 类型（`text/plain; charset=utf-8`），排查编码问题时比猜有用。"
            }
        ]
    },
    {
        "title": "把文件内容倒过来逐行输出",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "tac",
            "倒序",
            "日志"
        ],
        "choices": [],
        "source_section": "命令特训 · 查看文件内容",
        "statement_md": "日志是追加写的，最新的在最后。你要**从最后一行往前**看（不排序，纯倒序）。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "tac app.log",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|tac app.log\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`tac app.log`。\n\n`tac` 就是 `cat` 反过来写 —— 它把文件**按行倒序**输出，不做任何排序。与 `sort -r` 完全不同：`sort -r` 会按字典序重排，`tac` 只翻转原来的顺序。\n\n★ 为什么不用 `tail -r`：那是 BSD/macOS 的写法，GNU coreutils 里没有。Linux 上用 `tac`。\n\n★ `tac` 会把整个文件读进内存再倒着输出，超大文件（几个 G）会吃内存；那种场景用 `tail -n 1000 | tac` 截断后再倒。\n\n★ **迁移**：`tac` 和 `sed '1!G;h;$!d'` 效果一样（后者纯 sed 实现，某些极简环境里只有它可用）。"
            }
        ]
    },
    {
        "title": "看二进制文件里的可打印字符",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "od",
            "二进制",
            "hexdump"
        ],
        "choices": [],
        "source_section": "命令特训 · 查看文件内容",
        "statement_md": "有个文件 `file .bin` 报的是 `data`，你想看看里面有没有可读的字符串/结构。\n\n要求：以**八进制 + 可打印字符**的形式 dump 出来。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "od -c binfile",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|od -c binfile\n|od -tc binfile\n|od -An -c binfile\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`od -c binfile`。\n\n`od`（octal dump）默认输出八进制字节值；`-c` 让它把**可打印字符直接显示成字符**，不可打印的用 `\\n`、`\\t`、`\\0` 这类转义表示 —— 这才是「看懂二进制文件结构」的姿势。\n\n★ 常用组合：\n- `od -An -c f` 去掉左侧偏移地址列（`-An`）\n- `od -tx1 f` 十六进制字节（最常用）\n- `hexdump -C f` 十六进制 + ASCII 双栏（更好读，但不是 coreutils）\n\n★ **迁移**：`strings f | head` 直接从二进制里捞出连续可打印字符串，查「这个二进制里有没有硬编码路径/密钥」时比 `od` 快。"
            }
        ]
    },
    {
        "title": "一次看多个文件的开头，并且分得清哪个是哪个",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "head",
            "多文件",
            "标题"
        ],
        "choices": [],
        "source_section": "命令特训 · 查看文件内容",
        "statement_md": "`a.conf`、`b.conf`、`c.conf` 三个配置文件，你要各看前 5 行做对比。\n\n要求：一条命令，输出里必须**带文件名分隔**。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "head -n 5 a.conf b.conf c.conf",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|head -n 5 a.conf b.conf c.conf\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`head -n 5 a.conf b.conf c.conf`。\n\n★ 关键细节：**只要给了多于一个文件，`head` 就会自动加标题行**：\n```\n==> a.conf <==\n...\n==> b.conf <==\n...\n```\n只给一个文件时**不会**加 —— 所以脚本里解析单文件输出时，别指望永远有 `==>` 这一行。\n\n★ 想强制加标题：`head -v`；想强制不加：`head -q`（quiet）。\n这两个选项在写脚本时比默认行为更可控。\n\n★ **迁移**：`tail` 有一模一样的行为（`-v`/`-q`/多文件加标题）；`cat` 多文件时**不加**标题，需要分隔得自己 `echo`。"
            }
        ]
    },
    {
        "title": "看文件末尾 20 行，但不要跟进去等新内容",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "tail",
            "末尾",
            "-n"
        ],
        "choices": [],
        "source_section": "命令特训 · 查看文件内容",
        "statement_md": "排查报错时你只想看**最后 20 行**，看完就退出，不要卡在跟踪模式。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "tail -n 20 app.log",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|tail -n 20 app.log\n|tail -20 app.log\n|tail --lines=20 app.log\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`tail -n 20 app.log`。\n\n`tail` 不带 `-f` 时就是「看末尾 N 行然后退出」，默认 N=10。\n\n★ 与 `-f` 的区别是本题的核心：`-f` 会**一直挂着不退出**，在脚本里或 CI 里误用会让整条流水线卡死。「看一眼就完」永远不加 `-f`。\n\n★ 排查报错的高频组合：`tail -n 50 app.log | grep -i error`，或者 `grep -i error app.log | tail -n 20` —— **后者的语义是「最近 20 条错误」，前者是「最后 50 行里的错误」**，差别很大，别混。\n\n★ **迁移**：`tail -c 200 f` 按**字节**取末尾，处理「最后一行巨长」的场景（比如没有换行的 JSON）时比 `-n` 有用。"
            }
        ]
    },
    {
        "title": "数一数某个词在文件里出现了多少次",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "grep",
            "-c",
            "计数"
        ],
        "choices": [],
        "source_section": "命令特训 · 查看文件内容",
        "statement_md": "`access.log` 里 `ERROR` 出现了多少次？只要**次数**。\n\n写出这条命令（不要输出匹配到的行）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "grep -c ERROR access.log",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|grep -c ERROR access.log\n|grep -c 'ERROR' access.log\n|grep -c ERROR access.log\n|grep -c \"ERROR\" access.log\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`grep -c ERROR access.log`。\n\n`-c`（`--count`）只输出**匹配的行数**，不是匹配次数 —— 一行里出现 10 次 `ERROR` 也只算 1。要真数「次数」得 `grep -o ERROR f | wc -l`。\n\n★ 大小写：`-i` 忽略大小写，`grep -ci error f` 会把 `Error`/`ERROR` 都算上。日志里两种写法混用是常态，别漏了 `-i`。\n\n★ `-c` 与 `grep ... | wc -l` 结果一般相同，但 `-c` **快得多**（不用把每一行都传给下一个进程）。\n\n★ **迁移**：`grep -c` 返回 0 匹配时退出码是 **1**，脚本里 `set -e` 会因此中断；用 `grep -c pattern f || true` 兜一下。"
            }
        ]
    },
    {
        "title": "在 /etc 下按名字找所有 .conf 文件",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "find",
            "-name",
            "通配"
        ],
        "choices": [],
        "source_section": "命令特训 · 查找与定位",
        "statement_md": "配置改错了想对照一堆同类配置。要在 `/etc` 整棵树里找出**所有** `.conf` 结尾的文件。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "find /etc -name '*.conf'",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|find /etc -name '*.conf'\n|find /etc -name *.conf\n|find /etc -name \"*.conf\"\n|find /etc -name \"*.conf\"\n|find /etc -name *.conf\n|find /etc -name '*.conf'\n|find /etc -name *.conf\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`find /etc -name '*.conf'`。\n\n★ **引号是必须的**（判题会宽容没加引号的写法，但真实 shell 里不宽容）：不加引号时 `*` 会被 shell **先展开**成当前目录下已存在的 `.conf` 文件，然后 `find` 拿到的是一个个具体文件名，语义就变成「找这几个文件」了。当前目录恰好没有 `.conf` 时 shell 会把 `*.conf` 原样传过去，于是「有时对有时错」—— 这类 bug 最难查。\n\n★ `-name` 只匹配**文件名本身**（不含路径），所以 `*.conf` 能命中 `/etc/a/b/c.conf`；要匹配整条路径得用 `-path`。\n\n★ **迁移**：找完想批量处理，别用管道接 `xargs` 带空格的文件名会断——用 `find ... -print0 | xargs -0 cmd` 或 `find ... -exec cmd {} +`。"
            }
        ]
    },
    {
        "title": "忽略大小写找文件",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "find",
            "-iname",
            "大小写"
        ],
        "choices": [],
        "source_section": "命令特训 · 查找与定位",
        "statement_md": "用户把文件存成了 `README`、`Readme`、`readme` 混着来。你要**不分大小写**地把它们全找出来。\n\n写出这条命令（在当前目录往下找）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "find . -iname 'readme*'",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|find . -iname 'readme*'\n|find . -iname readme*\n|find . -iname \"readme*\"\n|find . -iname \"readme*\"\n|find . -iname readme*\n|find . -iname 'readme*'\n|find . -iname readme*\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`find . -iname 'readme*'`。\n\n`-iname` 就是 `-name` 的**不分大小写**版（i = insensitive）。其余行为完全一样。\n\n★ 这是 Linux 上最常见的挫败来源之一：`find . -name 'readme*'` 找不到 `README.md`，因为 `-name` 用的是 **shell glob 语义，区分大小写**。\n\n★ 注意：`-iname` 是 GNU find 的扩展，POSIX 标准里没有，某些精简系统（busybox）不认。\n\n★ **迁移**：`grep -ri pattern .` 是「在文件**内容**里不分大小写地搜」，和 `-iname` 是两件事 —— 一个是按**名字**找文件，一个是按**内容**找行。"
            }
        ]
    },
    {
        "title": "找出大于 100M 的文件",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "find",
            "-size",
            "磁盘"
        ],
        "choices": [],
        "source_section": "命令特训 · 查找与定位",
        "statement_md": "磁盘快满了。要找 `/var` 下**单个文件大于 100M** 的那些。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "find /var -size +100M",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|find /var -size +100M\n|find /var -type f -size +100M\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`find /var -type f -size +100M`。\n\n★ `-size` 的符号语义：\n- `+100M` 大于 100M\n- `-100M` 小于 100M\n- `100M` **恰好**等于 100M（几乎永远匹配不到，别用）\n\n★ 单位大小写很要紧：`M` = 1048576 字节，`k` = 1024 字节，`c` = 字节，`G` = 1G。写成 `-size +100m` 在 GNU find 下是**错的**（小写 `m` 不存在），会直接报错。\n\n★ 一定要加 `-type f`：不加的话目录也会被算进来，而目录的「大小」是目录项本身占的字节数，跟里面有多少东西无关，结果会莫名其妙。\n\n★ **迁移**：`du -ah /var | sort -rh | head -20` 是另一条常用路线，它按**实际占用**（含稀疏文件、硬链接去重）排，比 `find -size` 更贴近 `df` 的数字。"
            }
        ]
    },
    {
        "title": "找出 7 天内修改过的文件",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "find",
            "-mtime",
            "时间"
        ],
        "choices": [],
        "source_section": "命令特训 · 查找与定位",
        "statement_md": "排查「最近一周谁动过配置」，要在 `/etc` 下找 **mtime 在 7 天以内**的文件。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "find /etc -type f -mtime -7",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|find /etc -type f -mtime -7\n|find /etc -mtime -7 -type f\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`find /etc -type f -mtime -7`。\n\n★ `-mtime` 的符号是**最反直觉**的一处，务必记准：\n- `-mtime -7` → 修改时间在 **7 天以内**（小于 7 天）\n- `-mtime +7` → 修改时间在 **7 天以前**（大于 7 天）\n- `-mtime 7` → **恰好第 7 天那一天**（24 小时为一个整数区间）\n\n记忆法：**负数表示「最近」**（数值小 = 时间近），正数表示「很久以前」。\n\n★ 三个时间参数别混：`-mtime` 内容修改时间、`-atime` 访问时间、`-ctime` **inode 变更时间**（改权限/属主/改名都会动它，内容没变它也会变）。\n\n★ **迁移**：要精确到分钟用 `-mmin -60`（60 分钟内）；要「比某个参考文件新」用 `-newer ref.txt`，做增量备份时最稳。"
            }
        ]
    },
    {
        "title": "找出并删除所有 .tmp 临时文件",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "find",
            "-delete",
            "批量删除"
        ],
        "choices": [],
        "source_section": "命令特训 · 查找与定位",
        "statement_md": "`/tmp/work` 下散落了大量 `*.tmp`。要**一条命令**找出并删掉它们。\n\n要求：用 `find` 的删除动作，不要管道接 `rm`。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "find /tmp/work -name '*.tmp' -delete",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|find /tmp/work -name '*.tmp' -delete\n|find /tmp/work -name *.tmp -delete\n|find /tmp/work -name \"*.tmp\" -delete\n|find /tmp/work -name '*.tmp' -type f -delete\n|find /tmp/work -name *.tmp -type f -delete\n|find /tmp/work -name \"*.tmp\" -type f -delete\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`find /tmp/work -name '*.tmp' -delete`。\n\n`-delete` 是 find 的**内置动作**，边匹配边删，不经过管道，所以**天然不怕文件名里有空格或换行**。\n\n★ 为什么不用 `find ... | xargs rm`：`xargs` 按**空白**切分输入，文件名里带空格就会被拆成两个参数，轻则报错、重则删错东西。真要管道必须 `find ... -print0 | xargs -0 rm`。\n\n★ `-delete` 有个顺序要求：它**必须放在所有条件之后**（`find . -delete -name '*.tmp'` 会直接把整个目录删掉，因为 `-delete` 已经执行了，后面的条件才被判）。这是 find 里最昂贵的一课。\n\n★ **迁移**：删之前先不带 `-delete` 跑一遍看清单；`-delete` 也隐含 `-depth`（先删子项），所以它和 `-prune` 不能一起用。"
            }
        ]
    },
    {
        "title": "找出所有 .sh 并批量加上执行权限",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 4,
        "total_score": 18,
        "tags": [
            "find",
            "-exec",
            "chmod",
            "批量"
        ],
        "choices": [],
        "source_section": "命令特训 · 查找与定位",
        "statement_md": "`~/scripts` 下有一批 shell 脚本，权限都是 644，要**全部**改成可执行。\n\n要求：一条 `find` 命令搞定（用 `-exec`）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "find ~/scripts -name '*.sh' -exec chmod +x {} \\;",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|find ~/scripts -name '*.sh' -exec chmod +x {} \\;\n|find ~/scripts -name *.sh -exec chmod +x {} \\;\n|find ~/scripts -name \"*.sh\" -exec chmod +x {} \\;\n|find ~/scripts -name '*.sh' -exec chmod +x {} +\n|find ~/scripts -name *.sh -exec chmod +x {} +\n|find ~/scripts -name \"*.sh\" -exec chmod +x {} +\n|find ~/scripts -name '*.sh' -type f -exec chmod +x {} +\n|find ~/scripts -name *.sh -type f -exec chmod +x {} +\n|find ~/scripts -name \"*.sh\" -type f -exec chmod +x {} +\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`find ~/scripts -name '*.sh' -exec chmod +x {} \\;`。\n\n`-exec` 的语法有三个**必须记住**的点：\n1. `{}` 是占位符，会被替换成当前匹配到的文件路径\n2. 结尾必须是 `\\;`（分号前加反斜杠转义，防止被 shell 吃掉）或者 `+`\n3. `\\;` 表示**每个文件执行一次**；`+` 表示**攒成一批执行一次**（更快，等价于 `xargs`，而且同样不怕空格）\n\n★ 为什么 `\\;` 要转义：`;` 在 shell 里是命令分隔符，不转义的话 shell 会在传给 `find` 之前就把它吃掉，`find` 会以为参数没结束而报错。\n\n★ **迁移**：`-exec ... {} +` 只能放在**最后**；`\\;` 可以中间再用 `-exec`。要「找到后问一句」用 `-ok`（与 `-exec` 同语法，逐个确认）。"
            }
        ]
    },
    {
        "title": "只看当前这一层，别往下递归",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "find",
            "-maxdepth",
            "深度"
        ],
        "choices": [],
        "source_section": "命令特训 · 查找与定位",
        "statement_md": "`/etc` 下面太深了，你只想知道 `/etc` **这一层**有哪些普通文件。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "find /etc -maxdepth 1 -type f",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|find /etc -maxdepth 1 -type f\n|find /etc -maxdepth 1 -type f -print\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`find /etc -maxdepth 1 -type f`。\n\n★ `-maxdepth 1` = 只处理 `/etc` 这**一层**（深度 1）；`-mindepth 1` = 从**子里**开始，不含 `/etc` 自己。两者组合 `-mindepth 1 -maxdepth 1` 就是「只看直接子项，不看自己」。\n\n★ 顺序很重要：`-maxdepth` 是**全局选项**，必须放在其它测试条件**之前**（GNU find 会警告，有些版本直接报错）。`find /etc -type f -maxdepth 1` 是错的。\n\n★ `-maxdepth 1` 比 `ls` 强在哪：它能直接接 `-type`/`-size`/`-newer` 这些条件，而 `ls` 只能靠 `-l` 输出再 `grep` 解析。\n\n★ **迁移**：`find . -maxdepth 2 | sort` 是「看一眼目录骨架」最快的方式，比 `tree -L 2` 更通用（tree 常常没装）。"
            }
        ]
    },
    {
        "title": "查一个命令的可执行文件在哪",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "which",
            "command -v",
            "PATH"
        ],
        "choices": [],
        "source_section": "命令特训 · 查找与定位",
        "statement_md": "`python3` 到底在哪？脚本要用它的**绝对路径**写进 crontab。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "which python3",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|which python3\n|type -p python3\n|command -v python3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`which python3`（或 `command -v python3`）。\n\n`which` 顺着 `$PATH` 从左到右找，返回**第一个**匹配到的可执行文件。\n\n★ 为什么 crontab 里必须写绝对路径：cron 的 `$PATH` **极短**（通常只有 `/usr/bin:/bin`），你在交互 shell 里能跑的命令它可能找不到。所以 `which` 一下再写全路径是标准做法。\n\n★ `which` 的局限：它**不认 shell 内建命令和别名**。`which cd` 会找不到（cd 是内建），`which ls` 在有 `alias ls='ls --color'` 时也可能给不出你以为的答案。\n\n★ **迁移**：`command -v` 是 POSIX 标准写法，内建/别名/函数/外部命令**都能识别**，脚本里比 `which` 更可靠。"
            }
        ]
    },
    {
        "title": "查一个命令出现在 PATH 里的所有位置",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "which",
            "-a",
            "type",
            "PATH"
        ],
        "choices": [],
        "source_section": "命令特训 · 查找与定位",
        "statement_md": "机器上装了多个 Python（系统自带 + pyenv + conda），你要看 `python3` 在 `$PATH` 里**所有**候选路径。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "which -a python3",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|which -a python3\n|type -a python3\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`which -a python3`（或 `type -a python3`）。\n\n`-a`（all）让它**不提前退出**，把 `$PATH` 里所有匹配都列出来，顺序就是查找顺序 —— 第一行就是实际会被执行的那个。\n\n★ `type -a` 比 `which -a` 信息更全：它会标注每个候选是`is /path/to/x`（外部命令）、`is aliased to ...`（别名）还是 `is a shell builtin`（内建）。\n\n★ 排查「为什么跑的不是我装的版本」的完整套路：\n1. `type -a python3` 看有几个、谁是第一\n2. `echo $PATH` 看顺序（**左边优先**）\n3. 查 alias 和 `hash -r`（bash 会缓存命令路径，装了新版本要清缓存）\n\n★ **迁移**：`hash -r` 这一条能解决一大半「明明装了却还是旧版本」——bash 缓存了旧路径，新装的没被看见。"
            }
        ]
    },
    {
        "title": "查命令的类型（别名 / 内建 / 外部）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "type",
            "内建",
            "别名"
        ],
        "choices": [],
        "source_section": "命令特训 · 查找与定位",
        "statement_md": "`cd` 到底是文件还是 shell 内建？`ll` 为什么 `which` 找不到却能敲？\n\n要求：用能**区分内建、别名、函数、外部命令**的那条命令查 `cd`。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "type cd",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|type cd\n|type -a cd\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`type cd`。\n\n`type` 是 shell 内建，能分辨四类东西：\n- `cd is a shell builtin` —— **内建**（没有对应的可执行文件）\n- `ll is aliased to 'ls -l --color=auto'` —— **别名**\n- `python3 is /usr/bin/python3` —— **外部命令**\n- `f is a function` —— **函数**\n\n★ 这就解释了为什么 `which cd` 什么也不输出：`which` 只在 `$PATH` 目录里找**文件**，而 `cd` 是 bash 自己实现的，磁盘上根本没有 `cd` 这个可执行文件。\n\n★ 同理 `ll` 能敲是因为 `alias ll='ls -l'`，它不是命令，是**敲命令前做的文本替换**。\n\n★ **迁移**：`type -t cd` 只输出类型词（`builtin`/`alias`/`file`/`function`），写脚本时判断更好用。"
            }
        ]
    },
    {
        "title": "查这个可执行文件属于哪个软件包",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "rpm",
            "-qf",
            "软件包",
            "dnf"
        ],
        "choices": [],
        "source_section": "命令特训 · 查找与定位",
        "statement_md": "`/usr/bin/ls` 被你误删了，想重新装回来，但不知道它属于哪个包。\n\n写出这条命令（用 rpm 系工具）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "rpm -qf /usr/bin/ls",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|rpm -qf /usr/bin/ls\n|rpm --query --file /usr/bin/ls\n|dnf provides /usr/bin/ls\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`rpm -qf /usr/bin/ls`。\n\n- `-q` query（查询）\n- `-f` file（按**文件路径**反查所属包）\n\n输出形如 `coreutils-9.4-7.fc40.x86_64`，于是 `sudo dnf reinstall coreutils` 就能装回来。\n\n★ `-qf` 只能查**已安装包**里的文件。查「哪个包**提供**某个文件」而它还没装，要用 `dnf provides '*/ls'`（`dnf whatprovides` 的别名）。\n\n★ 路径必须**完全准确**：`rpm -qf ls` 会报 `file ls is not owned` —— 它要的是文件系统里的真实路径，不是命令名。所以先 `which ls` 拿到路径。\n\n★ **迁移**：卸载前先 `rpm -qf` 反查是哪个包，再 `rpm -q --whatrequires <包名>` 看谁会受影响 —— 这两步能避免「卸了一个包，半个桌面没了」。"
            }
        ]
    },
    {
        "title": "找出所有空文件与空目录",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "find",
            "-empty",
            "清理"
        ],
        "choices": [],
        "source_section": "命令特训 · 查找与定位",
        "statement_md": "清理项目目录时，想先看看哪些是**空文件**、哪些是**空目录**。\n\n要求：一条 `find` 命令同时覆盖两者。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "find . -empty",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|find . -empty\n|find . -empty -print\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`find . -empty`。\n\n`-empty` 是「大小为 0 的普通文件」**或**「不含任何条目的目录」的简写，一条条件同时命中两类。\n\n★ 想只清空目录：`find . -empty -type d`；只清空文件：`find . -empty -type f`。\n\n★ 注意「空文件」的定义是 **size == 0**。一个只有换行的文件不算空（它有 1 字节），用 `-empty` 找不到它 —— 想找「只有空白行的文件」得 `find . -type f -exec grep -qL '[^[:space:]]' {} +`。\n\n★ **迁移**：`find . -empty -delete` 能一次清掉所有空文件与空目录，但 `-delete` 隐含 `-depth`，会**先删子后删父**，所以一个「只含空目录的目录」会被判定为删完之后才空……实际 GNU find 是逐层处理的，多跑一次才彻底清干净。"
            }
        ]
    },
    {
        "title": "按权限精确查找文件",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "find",
            "-perm",
            "安全审计"
        ],
        "choices": [],
        "source_section": "命令特训 · 查找与定位",
        "statement_md": "做安全审计，要找出**权限恰好是 `644`** 的那些文件（不含 664、600）。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "find . -type f -perm 644",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|find . -type f -perm 644\n|find . -type f -perm 0644\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`find . -type f -perm 644`。\n\n★ `-perm` 不带符号（`-`/`/`）时是**精确匹配**：必须有且仅有这几位，664、600 都不算。\n\n★ 带符号的三档语义是本题的重点延伸：\n- `-perm -644`（减号）= **至少包含**这些位（可以更多）\n- `-perm /644`（斜杠）= **任意一位**匹配即可（或关系）\n- `-perm 644` = 精确相等\n\n★ 注意 `rwxr--r--` 这种符号写法不能直接给 `-perm`，要么换八进制，要么用符号模式 `-perm u=rwx,g=r,o=r`（GNU 扩展）。\n\n★ **迁移**：找「所有人可写」的隐患文件是 `find / -type f -perm -o+w`（减号，只要 o 位有 w 就算），这一条比精确匹配有用得多 —— 安全隐患往往是「至少」而不是「恰好」。"
            }
        ]
    },
    {
        "title": "找出所有设置了 SUID 的文件",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 4,
        "total_score": 18,
        "tags": [
            "find",
            "SUID",
            "安全",
            "4000"
        ],
        "choices": [],
        "source_section": "命令特训 · 查找与定位",
        "statement_md": "提权漏洞排查第一步：列出系统里所有 **SUID** 位的可执行文件。\n\n写出这条命令（从根开始，忽略错误输出）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "find / -perm -4000 -type f 2>/dev/null",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|find / -perm -4000 -type f 2>/dev/null\n|find / -type f -perm -4000 2>/dev/null\n|find / -user root -perm -4000 -type f 2>/dev/null\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`find / -perm -4000 -type f 2>/dev/null`。\n\n`4000` 就是 SUID 位（八进制的**第四位**）。用 `-4000`（减号）而不是 `4000` 是**必须的**：SUID 文件通常还有 755 之类的普通权限位，精确匹配 `4000` 只能找到「权限恰好是 4000」的，等于一个都找不到。\n\n★ `2>/dev/null` 不是可选项：`/proc`、`/sys` 下大量目录不让普通用户读，不加就会有成百上千行 `Permission denied` 淹没真正的结果。\n\n★ SUID 的含义：**执行时临时获得文件属主（通常是 root）的权限**。`/usr/bin/passwd` 就是靠它让普通用户能改自己的密码。也正因如此，被人塞进来的 SUID 程序就是提权后门。\n\n★ **迁移**：SGID 是 `2000`，sticky 是 `1000`（目录上的 `t`）。三个特殊位一起查：`find / -perm /7000`。"
            }
        ]
    },
    {
        "title": "找出所有指向已失效目标的软链（断链）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 4,
        "total_score": 18,
        "tags": [
            "find",
            "-xtype",
            "断链",
            "软链"
        ],
        "choices": [],
        "source_section": "命令特训 · 查找与定位",
        "statement_md": "目录整理完，想知道哪些软链**指向的目标已经不存在**了。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "find . -xtype l",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|find . -xtype l\n|find . -type l -xtype l\n|find . -type l ! -exec test -e {} \\; -print\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`find . -xtype l`。\n\n`-xtype` 是「按**链接指向的目标**判断类型」：`-xtype l` 意思是「目标是链接」—— 而**断链的目标根本不存在，find 会把它归为 `l`**，所以这一条正好筛出所有断链。\n\n★ 为什么不用 `-type l`：那会列出**所有**软链（好的坏的都要），你还得逐个 `test -e`。`-xtype l` 一步到位。\n\n★ 另一种等价思路（可读性更好）：`find . -type l ! -exec test -e {} \\; -print` —— 「是链接」且「目标不存在」。\n\n★ **迁移**：`readlink -f` 对断链会返回空、`ls -l` 里断链会显示成红色（多数发行版），但这些都是逐个人眼看；批量排查只有 `-xtype l` 可靠。"
            }
        ]
    },
    {
        "title": "找文件名里带空格的文件",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "find",
            "空格",
            "文件名"
        ],
        "choices": [],
        "source_section": "命令特训 · 查找与定位",
        "statement_md": "要把一批文件导进另一个系统，那个系统受不了文件名里的空格。\n\n先找出**名字里含空格**的普通文件。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "find . -type f -name '* *'",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|find . -type f -name '* *'\n|find . -name '* *' -type f\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`find . -type f -name '* *'`。\n\n`'* *'` 里两个 `*` 之间是一个**空格**，所以匹配「名字里至少有一个空格」。\n\n★ 引号不能省：不写引号的话 shell 会把 `* *` 拆成两个独立参数，`find` 会收到 `-name` 后面跟两个词，语法直接错。\n\n★ 为什么空格文件名是麻烦：几乎所有按空白切分的工具都会断 —— `for f in $(ls)`、`xargs`、`awk '{print $1}'` 全废。这就是为什么「处理 find 结果」必须用 `-print0` + `xargs -0`，或者 `-exec`。\n\n★ **迁移**：批量改名用 `rename 's/ /_/g' *`（util-linux 或 perl-rename 版），或 `find . -name '* *' -exec bash -c 'mv \"$1\" \"${1// /_}\"' _ {} \\;`。"
            }
        ]
    },
    {
        "title": "在日志里搜一个关键词",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "grep",
            "基础"
        ],
        "choices": [],
        "source_section": "命令特训 · 文本处理",
        "statement_md": "`app.log` 里找所有包含 `timeout` 的行。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "grep timeout app.log",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|grep timeout app.log\n|grep 'timeout' app.log\n|grep timeout app.log\n|grep \"timeout\" app.log\n|grep \"timeout\" app.log\n|grep timeout app.log\n|grep 'timeout' app.log\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`grep timeout app.log`。\n\n`grep 模式 文件`：**模式在前，文件在后**。写成 `grep app.log timeout` 会去一个叫 `timeout` 的目录里找 `app.log`，报 `No such file or directory`。\n\n★ 默认输出是**整行**，不是只输出匹配到的片段。只要片段得加 `-o`。\n\n★ 默认是**正则**（BRE）。`timeout` 里没有特殊字符所以没事，但搜 `.`、`*`、`[` 这些字符时必须转义或加 `-F`（固定字符串）。\n\n★ **迁移**：`grep -F 'a.b' f` 把模式当**纯文本**，搜代码/配置里的符号时最省心（`grep -F '[INFO]' log`）。"
            }
        ]
    },
    {
        "title": "忽略大小写搜索",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "grep",
            "-i",
            "大小写"
        ],
        "choices": [],
        "source_section": "命令特训 · 文本处理",
        "statement_md": "日志里 `Error`、`ERROR`、`error` 混着出现，你想一次全抓到。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "grep -i error app.log",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|grep -i error app.log\n|grep -i 'error' app.log\n|grep -i error app.log\n|grep -i \"error\" app.log\n|grep --ignore-case error app.log\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`grep -i error app.log`。\n\n`-i`（`--ignore-case`）让匹配不分大小写。\n\n★ 与 `-i` 容易混的两个：\n- `-w`（word）只匹配**完整单词**：`grep -w error` 不会命中 `errors`\n- `-v`（invert）**反选**：输出不匹配的行\n\n★ 组合使用非常常见：`grep -iv 'debug' app.log` = 排除掉所有 debug 行。注意 `-iv` 也能写成 `-vi`，判题与 shell 都认。\n\n★ **迁移**：日志分析的三板斧是 `-i`（不分大小写）、`-v`（排除噪声）、`-c`（只数条数）。`grep -ic error f` 一行就给出「有多少行报 error」。"
            }
        ]
    },
    {
        "title": "过滤掉配置文件的注释行和空行",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "grep",
            "-v",
            "注释",
            "正则"
        ],
        "choices": [],
        "source_section": "命令特训 · 文本处理",
        "statement_md": "`sshd_config` 里注释占了八成。你要看**实际生效的配置**：去掉以 `#` 开头的行，也去掉空行。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "grep -v '^#' sshd_config | grep -v '^$'",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|grep -v '^#' sshd_config | grep -v '^$'\n|grep -v ^# sshd_config | grep -v '^$'\n|grep -v \"^#\" sshd_config | grep -v '^$'\n|grep -v '^#' sshd_config | grep -v ^$\n|grep -v '^#' sshd_config | grep -v \"^$\"\n|grep -Ev '^#|^$' sshd_config\n|grep -Ev ^#|^$ sshd_config\n|grep -Ev \"^#|^$\" sshd_config\n|grep -vE '^(#|$)' sshd_config\n|grep -vE ^(#|$) sshd_config\n|grep -vE \"^(#|$)\" sshd_config\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`grep -v '^#' sshd_config | grep -v '^$'`（或一条 `grep -Ev '^#|^$'`）。\n\n★ `^#` 匹配**行首**的 `#`，这是关键 —— 只写 `grep -v '#'` 会把「行尾注释」和「含 `#` 的值」一起删掉（比如 `PasswordAuthentication yes # 备注` 整行都会消失）。\n\n★ `^$` 匹配**空行**。注意 `$` 在正则里是行尾锚点，写成 `grep -v '^ $'` 是「含一个空格的行」，不是空行。\n\n★ `-E` 打开扩展正则，`|` 才表示「或」；不加 `-E` 时 `\\|` 才是或，`|` 是字面竖线。\n\n★ **迁移**：去掉行尾注释（`#` 及之后）用 `sed 's/#.*//'`；两者合起来 `sed -e 's/#.*//' -e '/^$/d' f` 就是「只看有效配置」。"
            }
        ]
    },
    {
        "title": "只输出匹配到的那一段，不输出整行",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 4,
        "total_score": 18,
        "tags": [
            "grep",
            "-o",
            "-E",
            "正则"
        ],
        "choices": [],
        "source_section": "命令特训 · 文本处理",
        "statement_md": "日志行很长，你只想知道里面出现的**所有 IP 地址**。\n\n要求：只输出匹配到的片段，不要整行。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "grep -oE '([0-9]{1,3}\\.){3}[0-9]{1,3}' app.log",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|grep -oE '([0-9]{1,3}\\.){3}[0-9]{1,3}' app.log\n|grep -oE ([0-9]{1,3}\\.){3}[0-9]{1,3} app.log\n|grep -oE \"([0-9]{1,3}\\.){3}[0-9]{1,3}\" app.log\n|grep -o -E '([0-9]{1,3}\\.){3}[0-9]{1,3}' app.log\n|grep -o -E ([0-9]{1,3}\\.){3}[0-9]{1,3} app.log\n|grep -o -E \"([0-9]{1,3}\\.){3}[0-9]{1,3}\" app.log\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`grep -oE '([0-9]{1,3}\\.){3}[0-9]{1,3}' app.log`。\n\n- `-o`（only-matching）**只输出匹配的那一段**，一行里有多个匹配就输出多行\n- `-E` 扩展正则，这样 `{1,3}`、`()` 才能直接用\n\n★ 正则要点：`([0-9]{1,3}\\.){3}` 表示「1~3 位数字 + 点」重复 3 次，再跟一段 1~3 位数字。`\\.` 必须转义 —— 不转义的 `.` 匹配任意字符，会把 `1x2x3x4` 也算成 IP。\n\n★ 这个正则**不校验范围**（`999.999.999.999` 也会被抓），做严格校验得上 `grep -oP` 配合 lookahead，或者用 `awk` 拆段判断。\n\n★ **迁移**：`grep -o` 配合 `sort | uniq -c | sort -rn` 是「找出最高频的 XX」的标准套路 —— 统计访问最多的 IP、最常见的错误码都靠它。"
            }
        ]
    },
    {
        "title": "递归搜索目录里所有文件的某个关键字",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "grep",
            "-r",
            "递归"
        ],
        "choices": [],
        "source_section": "命令特训 · 文本处理",
        "statement_md": "`src/` 下有几十个文件，你要找**哪个文件**里写了 `TODO`。\n\n要求：输出里要能看出是哪个文件。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "grep -r TODO src/",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|grep -r TODO src/\n|grep -rn TODO src/\n|grep -r 'TODO' src/\n|grep -r TODO src/\n|grep -r \"TODO\" src/\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`grep -r TODO src/`。\n\n`-r`（recursive）递归整棵目录树。**多文件/递归时 grep 会自动加文件名前缀**，所以你能看出是哪个文件。\n\n★ 只给一个文件时**不会**加前缀 —— 这与 `head` 多文件加标题的逻辑正好相反，脚本里解析时要注意。\n\n★ `-r` 与 `-R` 的差别：`-r` **不跟随**符号链接，`-R` **跟随**。跟了软链可能死循环（软链指回上级），所以默认用 `-r`。\n\n★ 加 `-n` 带行号（`grep -rn`），这是日常最常用的组合 —— 能直接 `vim +行号 文件` 跳过去。\n\n★ **迁移**：想排除 `.git`、`node_modules` 用 `grep -rn --exclude-dir={.git,node_modules} TODO .`。"
            }
        ]
    },
    {
        "title": "带行号搜索（方便直接跳转）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "grep",
            "-n",
            "行号"
        ],
        "choices": [],
        "source_section": "命令特训 · 文本处理",
        "statement_md": "找到报错行之后，你要用 `vim +行号 文件` 跳过去。\n\n所以搜索时必须**带上行号**。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "grep -n error app.log",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|grep -n error app.log\n|grep -n 'error' app.log\n|grep -n error app.log\n|grep -n \"error\" app.log\n|grep --line-number error app.log\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`grep -n error app.log`。\n\n输出形如 `42:2026-10-19 connect error`——**行号 + 冒号 + 行内容**。冒号是关键分隔符，`cut -d: -f1` 就能把行号单独取出来。\n\n★ `-n` 与 `-c`、`-l` 的区分：\n- `-n` 显示**每行的行号**\n- `-c` 只给**匹配行数**\n- `-l` 只给**匹配的文件名**\n三个都是「少输出点东西」，但输出的是什么完全不同。\n\n★ **迁移**：`grep -rn` 是搜索代码的起手式；配 `--color=auto` 让命中处高亮，大多数发行版默认就是 `alias grep='grep --color=auto'`。"
            }
        ]
    },
    {
        "title": "看匹配行前后各 3 行",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "grep",
            "-A",
            "-B",
            "-C",
            "上下文"
        ],
        "choices": [],
        "source_section": "命令特训 · 文本处理",
        "statement_md": "报错信息只有一行，但**上下文**才是关键。要看每次匹配的**前 3 行和后 3 行**。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "grep -A 3 -B 3 error app.log",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|grep -A 3 -B 3 error app.log\n|grep -B 3 -A 3 error app.log\n|grep -C 3 error app.log\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`grep -C 3 error app.log`（等价于 `-A 3 -B 3`）。\n\n- `-A n`（After）匹配行之后 n 行\n- `-B n`（Before）匹配行之前 n 行\n- `-C n`（Context）前后各 n 行\n\n★ 上下文行与匹配行之间用 `--` 分隔，上下文行本身的显示格式是 `行号-内容`（**减号**不是冒号），匹配行才是 `行号:内容`。写脚本解析时这个区别很重要。\n\n★ 上下文窗口会**合并**：两个匹配离得近时，重叠部分只输出一次，不会重复。\n\n★ **迁移**：`tail -f app.log | grep -C 5 -i error` 是盯线上问题的标准组合 —— 既实时又带上下文。"
            }
        ]
    },
    {
        "title": "把文件里的 old 全部换成 new（不破坏原文件）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "sed",
            "s///",
            "替换"
        ],
        "choices": [],
        "source_section": "命令特训 · 文本处理",
        "statement_md": "要预览一次全局替换的效果，**先别动原文件**，只输出替换后的内容。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "sed 's/old/new/g' config.txt",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|sed 's/old/new/g' config.txt\n|sed s/old/new/g config.txt\n|sed \"s/old/new/g\" config.txt\n|sed -e 's/old/new/g' config.txt\n|sed -e s/old/new/g config.txt\n|sed -e \"s/old/new/g\" config.txt\n|sed 's/old/new/g' < config.txt\n|sed s/old/new/g < config.txt\n|sed \"s/old/new/g\" < config.txt\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`sed 's/old/new/g' config.txt`。\n\n`s/旧/新/` 里的三个斜杠是分隔符，`g`（global）表示**一行内全部替换**。\n\n★ 没有 `g` 只替换**每行第一次**出现 —— 这是 sed 最常见的一个坑：`sed 's/a/b/' f` 对 `aaa` 得到 `baa`，加了 `g` 才得到 `bbb`。\n\n★ 默认**只输出到 stdout**，不改文件。要落盘必须 `-i`（原地改）或重定向到新文件。\n\n★ 分隔符可以换：路径里全是斜杠时写 `s|/usr/local|/opt|g` 更清爽。\n\n★ **迁移**：`sed -n 's/old/new/p'` 只打印**发生替换的行**，做「替换前先确认会影响哪些行」的检查时特别有用。"
            }
        ]
    },
    {
        "title": "原地修改文件（直接改在硬盘上）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "sed",
            "-i",
            "原地修改"
        ],
        "choices": [],
        "source_section": "命令特训 · 文本处理",
        "statement_md": "确认替换没问题了，现在要**直接把文件改掉**，不要重定向到新文件。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "sed -i 's/old/new/g' config.txt",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|sed -i 's/old/new/g' config.txt\n|sed -i s/old/new/g config.txt\n|sed -i \"s/old/new/g\" config.txt\n|sed -i.bak 's/old/new/g' config.txt\n|sed -i.bak s/old/new/g config.txt\n|sed -i.bak \"s/old/new/g\" config.txt\n|sed --in-place 's/old/new/g' config.txt\n|sed --in-place s/old/new/g config.txt\n|sed --in-place \"s/old/new/g\" config.txt\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`sed -i 's/old/new/g' config.txt`。\n\n`-i`（in-place）直接改写文件。\n\n★ **`-i` 的实现是个陷阱**：它不是真的「原地」写，而是**新建一个临时文件、写完再重命名覆盖原文件**。后果有两条：\n1. **inode 变了** —— 原文件的硬链接全部断开，正在写这个文件的进程还握着旧 inode\n2. **软链被替换成实体文件** —— `sed -i` 一个软链，软链本身变成普通文件，目标文件反而没改\n\n★ `-i.bak` 会先备份成 `config.txt.bak`，**改配置前务必带上**，出事能一秒回滚。\n\n★ GNU sed 的 `-i` 后面**不能有空格**：`-i .bak` 会被理解成「备份后缀为空」+ 一个叫 `.bak` 的脚本文件。\n\n★ **迁移**：真要保 inode（比如改日志配置），用 `sed ... > tmp && cat tmp > 原文件`（重定向回原文件不换 inode）。"
            }
        ]
    },
    {
        "title": "删掉文件里的所有空行",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "sed",
            "空行",
            "删除"
        ],
        "choices": [],
        "source_section": "命令特训 · 文本处理",
        "statement_md": "整理配置或代码时，空行太多影响阅读。\n\n写出这条命令（输出到屏幕）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "sed '/^$/d' config.txt",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|sed '/^$/d' config.txt\n|sed /^$/d config.txt\n|sed \"/^$/d\" config.txt\n|grep -v '^$' config.txt\n|grep -v ^$ config.txt\n|grep -v \"^$\" config.txt\n|awk 'NF' config.txt\n|awk NF config.txt\n|awk \"NF\" config.txt\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`sed '/^$/d' config.txt`。\n\n`/正则/d` 是 sed 的「**匹配就删**」：`^$` 是「空行」，`d` 是 delete。\n\n★ 三种写法各有微妙差别：\n- `sed '/^$/d'` 只删**完全空**的行\n- `sed '/^[[:space:]]*$/d'` 连**只有空格/制表符**的行也删（更实用）\n- `awk 'NF'` 删掉所有**没有字段**的行（同上，且更短）\n- `grep -v '^$'` 与第一种等价\n\n★ **迁移**：合并连续空行成一行用 `cat -s f`（squeeze）；连注释一起清掉：`sed -e '/^#/d' -e '/^$/d' f`，这就是「只看有效配置」的一行版。"
            }
        ]
    },
    {
        "title": "只打印第 10 到第 20 行",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "sed",
            "-n",
            "行区间"
        ],
        "choices": [],
        "source_section": "命令特训 · 文本处理",
        "statement_md": "要给同事贴一段配置，只想要**第 10~20 行**这个区间。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "sed -n '10,20p' config.txt",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|sed -n '10,20p' config.txt\n|sed -n 10,20p config.txt\n|sed -n \"10,20p\" config.txt\n|sed -n '10,20 p' config.txt\n|awk 'NR>=10 && NR<=20' config.txt\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`sed -n '10,20p' config.txt`。\n\n★ `-n` 是必须的：不加 `-n` 时 sed 默认会**把每一行都打印一遍**，`p` 又多打一次，结果是「全文 + 区间重复一遍」。`-n` 抑制默认输出，只留 `p` 打的那部分。\n\n★ 区间是**含两端**的：`10,20p` 包含第 10 行和第 20 行，共 11 行。\n\n★ 等价写法：`awk 'NR>=10 && NR<=20'`（NR = 当前行号），或者 `head -n 20 f | tail -n 11` —— 后者要自己算「11」这个数，很容易算错，不推荐。\n\n★ **迁移**：`sed -n '10,$p'` 从第 10 行到末尾；`sed -n '10~5p'` 从第 10 行起每 5 行取一行（GNU 扩展，采样日志很好用）。"
            }
        ]
    },
    {
        "title": "按冒号分列，取每行第一列",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "cut",
            "-d",
            "-f",
            "分列"
        ],
        "choices": [],
        "source_section": "命令特训 · 文本处理",
        "statement_md": "`/etc/passwd` 是冒号分隔的。你只要**所有用户名**。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "cut -d: -f1 /etc/passwd",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|cut -d: -f1 /etc/passwd\n|cut -d ':' -f 1 /etc/passwd\n|cut -d : -f 1 /etc/passwd\n|cut -d \":\" -f 1 /etc/passwd\n|awk -F: '{print $1}' /etc/passwd\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`cut -d: -f1 /etc/passwd`。\n\n- `-d` 指定**分隔符**，`:` 是冒号\n- `-f` 指定要**第几列**（1 起算）\n\n★ `cut` 的三个坑（都是真会踩的）：\n1. **默认分隔符是 TAB**，不是空格。用空格分隔的文本必须 `-d' '`\n2. **不合并连续分隔符**：`a::b` 用 `-d: -f2` 得到**空**，而不是 `b` —— 想要「跳过空字段」得用 awk\n3. **只能按单一字符或字节切**，不支持正则\n\n★ 所以字段数不定、有空字段的场景，`awk -F: '{print $1}'` 更稳。\n\n★ **迁移**：`cut -c1-10 f` 按**字符位置**切（不需要分隔符），处理定长格式（旧式报表）时很有用。"
            }
        ]
    },
    {
        "title": "取第 3 列，但文件是空格分隔且空格数量不固定",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "awk",
            "字段",
            "空格分隔"
        ],
        "choices": [],
        "source_section": "命令特训 · 文本处理",
        "statement_md": "`ps aux` 这类输出里，列之间有**多个空格**。你要取第 3 列。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "awk '{print $3}' file.txt",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|awk '{print $3}' file.txt\n|awk '{ print $3 }' file.txt\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`awk '{print $3}' file.txt`。\n\n★ 这就是 **awk 与 cut 的分水岭**：awk 默认按「**任意数量的空白**」切分，多个空格、前导空格都自动吃掉；而 `cut -d' '` 会把每个空格都当分隔符，`a   b` 会切出 `a`、空、空、`b`，`-f3` 拿到空串。\n\n★ 所以：**固定单字符分隔用 cut，空白分隔用 awk**。这是选工具时最实用的一条判据。\n\n★ `$0` 是整行，`$NF` 是**最后一个字段**（NF = number of fields，字段数）。`awk '{print $NF}'` 取最后一列是高频用法。\n\n★ **迁移**：`awk -F: '{print $1}'` 指定冒号分隔；`awk 'BEGIN{FS=\"\\t\"}'` 在脚本里设制表符。"
            }
        ]
    },
    {
        "title": "取第 3 列数值大于 100 的行",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "awk",
            "条件",
            "数值"
        ],
        "choices": [],
        "source_section": "命令特训 · 文本处理",
        "statement_md": "有个报表 `sales.txt`，第 3 列是金额。要筛出**金额 > 100** 的行。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "awk '$3 > 100' sales.txt",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|awk '$3 > 100' sales.txt\n|awk '$3>100' sales.txt\n|awk $3>100 sales.txt\n|awk \"$3>100\" sales.txt\n|awk '$3 > 100 {print}' sales.txt\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`awk '$3 > 100' sales.txt`。\n\nawk 的程序结构是 `模式 { 动作 }`：**模式为真就执行动作，动作省略时默认 `print $0`（打印整行）**。所以 `'$3 > 100'` 就够，不用写 `{print}`。\n\n★ 数值 vs 字符串：awk 会根据上下文自动转型。`$3 > 100` 里 `100` 是数字，awk 就把 `$3` 当数字比；但写成 `$3 > \"100\"` 就变成**字符串比较**，`\"99\" > \"100\"` 为**真**（按字典序 `9` > `1`）。这个坑非常经典。\n\n★ awk 比 grep 强的地方就在这：grep 只能按**文本模式**匹配，awk 能做**数值/逻辑判断**、跨列计算、求和。\n\n★ **迁移**：`awk '$3 > 100 {sum += $3} END {print sum}'` 求和；`awk '$3 > 100 {n++} END {print n}'` 计数。这是「统计报表」最轻量的做法，不用写 Python。"
            }
        ]
    },
    {
        "title": "按冒号取第一列，然后排序去重",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "cut",
            "sort",
            "-u",
            "uniq"
        ],
        "choices": [],
        "source_section": "命令特训 · 文本处理",
        "statement_md": "`/etc/passwd` 里很多用户的**登录 shell**（第 7 列）重复。你要看有哪几种 shell 在用。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "cut -d: -f7 /etc/passwd | sort -u",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|cut -d: -f7 /etc/passwd | sort -u\n|cut -d: -f7 /etc/passwd | sort | uniq\n|awk -F: '{print $7}' /etc/passwd | sort -u\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`cut -d: -f7 /etc/passwd | sort -u`。\n\n★ `sort -u`（unique）在排序的同时去重，一条命令干两件事。它**隐含了排序**，所以不需要额外的 `uniq`。\n\n★ 为什么不能直接 `uniq`：`uniq` 只能去掉**相邻**的重复行。没排序就 `uniq`，`a b a` 会原样保留。所以经典写法是 `sort | uniq`，或者直接 `sort -u`。\n\n★ 注意 `/etc/passwd` 第 7 列是登录 shell，`/sbin/nologin` 和 `/bin/false` 表示「不许登录」，这类账号很多 —— 它们出现在结果里是正常的。\n\n★ **迁移**：`sort f | uniq -c | sort -rn` 是「统计每种值出现多少次并按次数排」的标准三连，分析日志里的错误码、URL、IP 都用它。"
            }
        ]
    },
    {
        "title": "统计每种取值出现了几次，按次数从多到少排",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "sort",
            "uniq",
            "-c",
            "统计"
        ],
        "choices": [],
        "source_section": "命令特训 · 文本处理",
        "statement_md": "`access.log` 里有一列是状态码。你要看**哪个状态码最多**。\n\n假设已经用 `awk '{print $9}' access.log` 拿到了状态码这一列。\n\n写出「统计每行出现次数并按次数降序」这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "sort access.log | uniq -c | sort -rn",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|sort access.log | uniq -c | sort -rn\n|sort access.log | uniq -c | sort -nr\n|sort access.log | uniq -c | sort -k1,1nr\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`sort access.log | uniq -c | sort -rn`。\n\n三步各有分工，**顺序不能换**：\n1. `sort` —— 把相同的行排到一起（`uniq` 只认相邻重复）\n2. `uniq -c` —— 去重并**在行首加上出现次数**\n3. `sort -rn` —— 按**数字**（`-n`）**降序**（`-r`）重排\n\n★ 第二个 `sort` 的 `-n` 不能省：不加的话 `10` 会排在 `9` 前面（按字典序 `1` < `9`），结果看起来「挺像那么回事」，其实完全是错的。\n\n★ `uniq -c` 的输出格式是「**空格 + 次数 + 空格 + 内容**」，次数前面有**对齐用的填充空格**，所以 `awk '{print $1}'` 比 `cut -d' ' -f1` 安全。\n\n★ **迁移**：真正的实战写法是把它接在 `awk` 后面 —— `awk '{print $9}' access.log | sort | uniq -c | sort -rn | head`，一步得到「Top 10 状态码」。"
            }
        ]
    },
    {
        "title": "把文件里所有小写字母转成大写",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "tr",
            "大小写",
            "标准输入"
        ],
        "choices": [],
        "source_section": "命令特训 · 文本处理",
        "statement_md": "要把一个单词表全部转成大写。\n\n写出这条命令（输出到屏幕，不改原文件）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "tr 'a-z' 'A-Z' < words.txt",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|tr 'a-z' 'A-Z' < words.txt\n|tr a-z 'A-Z' < words.txt\n|tr \"a-z\" 'A-Z' < words.txt\n|tr 'a-z' A-Z < words.txt\n|tr 'a-z' \"A-Z\" < words.txt\n|tr a-z A-Z < words.txt\n|tr '[:lower:]' '[:upper:]' < words.txt\n|tr [:lower:] '[:upper:]' < words.txt\n|tr \"[:lower:]\" '[:upper:]' < words.txt\n|tr '[:lower:]' [:upper:] < words.txt\n|tr '[:lower:]' \"[:upper:]\" < words.txt\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`tr 'a-z' 'A-Z' < words.txt`。\n\n★ **`tr` 只从标准输入读，不接受文件名参数**。写 `tr 'a-z' 'A-Z' words.txt` 会把 `words.txt` 当成**第二组要替换的字符**，然后把终端挂在那里等输入。这是 `tr` 最容易踩的一脚。\n\n★ `'a-z' 'A-Z'` 是**字符区间**映射，不是「把字符串 a-z 换掉」。`tr` 逐字符一一对应替换，所以能正确做大小写转换。\n\n★ 想**原地改**：`tr ... < f > tmp && mv tmp f`（不能直接 `> f`，shell 会先截断 f，`tr` 读到空文件）。\n\n★ **迁移**：`tr -d '\\r'` 干掉 Windows 换行残留（超高频）；`tr -s ' '` 把连续空格压成一个；`tr -cd '0-9'` 只保留数字（`-c` 取补集、`-d` 删除）。"
            }
        ]
    },
    {
        "title": "比较两个文件有什么不同",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "diff",
            "-u",
            "比较"
        ],
        "choices": [],
        "source_section": "命令特训 · 文本处理",
        "statement_md": "`config.old` 和 `config.new` 改了什么？要看出**具体哪几行不一样**。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "diff config.old config.new",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|diff config.old config.new\n|diff -u config.old config.new\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`diff config.old config.new`。\n\n默认输出的三个符号要会读：\n- `a`（add）—— 右边多了行\n- `d`（delete）—— 左边多了行\n- `c`（change）—— 两边都有但不同\n行号格式是 `旧文件行号 动作 新文件行号`。\n\n★ `-u`（unified）输出**带上下文的补丁格式**（`---`/`+++`/`@@`），这才是能用 `patch` 应用的格式，也是 `git diff` 的默认样式。肉眼看也比默认格式清楚得多。\n\n★ `-u` 还有个好处：`diff -u a b > p.patch` 之后 `patch -p0 < p.patch` 就能打上。\n\n★ **迁移**：`diff <(cmd1) <(cmd2)` 能直接比较**两条命令的输出**，不用先落盘（bash 进程替换）。比较目录用 `diff -r dir1 dir2`。"
            }
        ]
    },
    {
        "title": "取两个文件共有的行",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 4,
        "total_score": 18,
        "tags": [
            "comm",
            "交集",
            "排序"
        ],
        "choices": [],
        "source_section": "命令特训 · 文本处理",
        "statement_md": "`a.txt` 和 `b.txt` 各有一批 ID。你要**同时出现在两个文件里**的那些。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "comm -12 a.txt b.txt",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|comm -12 a.txt b.txt\n|comm -1 -2 a.txt b.txt\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`comm -12 a.txt b.txt`。\n\n★ `comm` 的前提**必须满足**：两个文件都**已排序**，否则结果不可信。没排序先 `sort -o a.txt a.txt`。\n\n它的输出是**三栏**：\n- 第 1 栏：只在 a 里的\n- 第 2 栏：只在 b 里的\n- 第 3 栏：两边都有的\n\n`-1`/`-2`/`-3` 就是「**去掉第 N 栏**」，所以 `-12` = 只留第 3 栏 = 交集。\n同理 `-13` = 只在 b 里的，`-23` = 只在 a 里的。\n\n★ 想要**并集**就三栏全留（不加选项，但要自己处理缩进）。\n\n★ **迁移**：`comm` 比 `grep -Ff` 精确（后者是子串匹配，`abc` 会命中 `xabcd`）；要交集又不想先排序，可以用 `awk 'NR==FNR{a[$0];next} $0 in a' a.txt b.txt`。"
            }
        ]
    },
    {
        "title": "把制表符换成 4 个空格",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "expand",
            "制表符",
            "缩进"
        ],
        "choices": [],
        "source_section": "命令特训 · 文本处理",
        "statement_md": "代码里混进了制表符，编辑器显示不对齐。要统一换成 4 个空格。\n\n写出这条命令（输出到屏幕）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "expand -t 4 code.c",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|expand -t 4 code.c\n|expand -t4 code.c\n|sed 's/\\t/ /g' code.c\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`expand -t 4 code.c`。\n\n`expand` 是专门干这件事的工具：把 **TAB 展开成空格**，`-t 4` 指定制表宽度为 4。反向操作是 `unexpand`。\n\n★ 为什么优先 `expand` 而不是 `sed 's/\\t/    /g'`：TAB 在**列对齐**时不是一个固定宽度 —— 它把光标推到下一个制表位。所以 `a\\tb` 里的 TAB 展开后**可能是 1~8 个空格**，取决于 `a` 的长度。`expand` 会按列位置正确计算，`sed` 只会无脑换成固定数量。\n\n★ 原地改：`expand -t 4 f > tmp && mv tmp f`。\n\n★ **迁移**：`expand -i` 只转**行首**的 TAB（保留缩进之外的 TAB），处理 Makefile 时要格外小心 —— **Makefile 的缩进必须是真 TAB**，一转就废。"
            }
        ]
    },
    {
        "title": "只保留文件里的数字",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 4,
        "total_score": 18,
        "tags": [
            "tr",
            "-c",
            "-d",
            "提取"
        ],
        "choices": [],
        "source_section": "命令特训 · 文本处理",
        "statement_md": "有个文件混着字母和数字（如 `abc123def456`），你只想把**所有数字**提取出来。\n\n写出这条命令（输出到屏幕）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "tr -cd '0-9' < mixed.txt",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|tr -cd '0-9' < mixed.txt\n|tr -cd 0-9 < mixed.txt\n|tr -cd \"0-9\" < mixed.txt\n|tr -cd '[:digit:]' < mixed.txt\n|tr -cd [:digit:] < mixed.txt\n|tr -cd \"[:digit:]\" < mixed.txt\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`tr -cd '0-9' < mixed.txt`。\n\n两个选项叠在一起：\n- `-c`（complement）取**补集**，即「除 0-9 之外的字符」\n- `-d`（delete）**删除**这些字符\n\n合起来 = 删掉所有非数字 = 只留数字。顺序可以写 `-cd` 或 `-dc`，都对。\n\n★ 注意它**会连换行一起删**（换行不是数字），所以输出会变成一整行 `123456...`。想保留行结构，得按行处理（`sed 's/[^0-9]//g'` 不会删换行）。\n\n★ **迁移**：`tr -d '[:space:]'` 删掉所有空白（含换行、TAB）；`tr -cd '[:print:]'` 只留可见字符（清二进制垃圾很有效）。"
            }
        ]
    },
    {
        "title": "把多行合并成一行（用逗号分隔）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 4,
        "total_score": 18,
        "tags": [
            "paste",
            "-s",
            "-d",
            "合并"
        ],
        "choices": [],
        "source_section": "命令特训 · 文本处理",
        "statement_md": "文件里每行一个 IP，你要拼成 `1.1.1.1,2.2.2.2,...` 这样一行。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "paste -sd, ips.txt",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|paste -sd, ips.txt\n|paste -s -d, ips.txt\n|paste -sd ',' ips.txt\n|paste -sd , ips.txt\n|paste -sd \",\" ips.txt\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`paste -sd, ips.txt`。\n\n- `-s`（serial）把**整个文件**当一组，按行串起来（而不是默认的并排多列）\n- `-d,` 指定**分隔符**为逗号\n\n★ 不加 `-s` 时 `paste` 是「把多个文件**按列并排**」，完全不同的用途（`paste a b` 会得到 `a1 b1` 这样的两列）。\n\n★ 结果**末尾会多一个逗号**（因为每行后面都加分隔符）——要干净的输出得再 `sed 's/,$//'`。\n\n★ `-d` 支持列表轮换：`-d',\\n'` 表示「逗号、换行交替」，能把长列表折成每行 N 个。\n\n★ **迁移**：`paste - - < f` 把单列变成两列；`paste -d' ' a b c` 把三个文件并成三列 —— 生成对账表格时比 `awk` 省事。"
            }
        ]
    },
    {
        "title": "给脚本加上可执行权限（不改变其他位）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "chmod",
            "+x",
            "执行权限"
        ],
        "choices": [],
        "source_section": "命令特训 · 权限与属性",
        "statement_md": "`deploy.sh` 现在是 `644`，要让它能直接 `./deploy.sh` 跑起来。\n\n要求：**只加执行位**，别改动读写位。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "chmod +x deploy.sh",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|chmod +x deploy.sh\n|chmod a+x deploy.sh\n|chmod ugo+x deploy.sh\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`chmod +x deploy.sh`。\n\n`+x` 不给「谁」时，等价于 **`a+x`（所有人）**，但实际行为是「**只给那些已经有某种执行位的身份加 x**」——所以 `644` 会变成 `755`，`640` 会变成 `750`。这是最常用也最安全的一档。\n\n★ 只想让属主能跑：`chmod u+x f`（得到 `744`）。放在公共目录里给别人也要跑的，才用 `a+x`。\n\n★ 目录的 `x` 意义不同：目录的 `x` 是「**能进入/穿过**」（`cd` 进去、访问里面的文件）。对一个目录执行 `chmod +x` 会让人可以 `cd` 进去，但看不见里面有什么（那需要 `r`）。\n\n★ **迁移**：`chmod -x f` 是收回执行位；`chmod =x` 会把**其他所有位清掉**只留 x —— `=` 是覆盖，别当成「加」。"
            }
        ]
    },
    {
        "title": "把一个目录树全部设成 755（目录）和 644（文件）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 4,
        "total_score": 18,
        "tags": [
            "chmod",
            "递归",
            "规范化",
            "find"
        ],
        "choices": [],
        "source_section": "命令特训 · 权限与属性",
        "statement_md": "网站根目录被人改乱了权限，要**规范化**：所有目录 `755`、所有普通文件 `644`。\n\n写出这两条命令（一条处理目录，一条处理文件）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "find /var/www -type d -exec chmod 755 {} \\; && find /var/www -type f -exec chmod 644 {} \\;",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|find /var/www -type d -exec chmod 755 {} \\; && find /var/www -type f -exec chmod 644 {} \\;\n|find /var/www -type d -exec chmod 755 {} + && find /var/www -type f -exec chmod 644 {} +\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "分两条，各管一类：\n```bash\nfind /var/www -type d -exec chmod 755 {} \\;\nfind /var/www -type f -exec chmod 644 {} \\;\n```\n\n★ 为什么不能一句 `chmod -R 755 /var/www`：那会把**文件**也变成 `755`（可执行）。普通文件多一个 `x` 位虽然大多无害，但会让「哪些是脚本」这件事彻底失去意义，安全审计也会报一堆可疑项。\n\n★ 目录要 `x` 才能真正进去，所以目录不能给 `644` —— 反过来文件不该给 `755`，这是权限规范化的核心两条。\n\n★ 用 `-exec ... +` 比 `\\;` 快得多（攒批执行，少 fork 很多次）。\n\n★ **迁移**：`chmod -R a+rX dir` 里的**大写 `X`** 是专门解决这件事的 —— 「目录加 x，文件只在**原本就有 x** 时才加 x」，一条命令就能安全递归授权。"
            }
        ]
    },
    {
        "title": "把目录设成「只有属主能删自己文件」的粘滞位",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 4,
        "total_score": 18,
        "tags": [
            "chmod",
            "sticky",
            "1777",
            "/tmp"
        ],
        "choices": [],
        "source_section": "命令特训 · 权限与属性",
        "statement_md": "你建了个公共上传目录 `/srv/share`，所有人可写，但要求**每个人只能删自己的文件**（不能删别人的）。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "chmod 1777 /srv/share",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|chmod 1777 /srv/share\n|chmod +t /srv/share\n|chmod o+t /srv/share\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`chmod 1777 /srv/share`（或 `chmod +t /srv/share`）。\n\n`1777` 开头的 **`1` 就是 sticky 位**（粘滞位），长格式里显示为权限串最后的 **`t`**：`drwxrwxrwt`。`/tmp` 就是标准的 `1777`。\n\n★ 它解决的问题：目录有 `w` 位时，任何有写权限的人都能**删除目录里任何文件**（哪怕文件不是他的）。加了 sticky 位，就只能删**自己的**文件或自己是属主的。\n\n★ 特殊位三兄弟的八进制位置：**SUID = 4000、SGID = 2000、sticky = 1000**，都写在普通三位之前（所以是四位数）。\n\n★ **迁移**：`ls -ld /tmp` 看一眼就知道什么是标准配置；去掉粘滞位是 `chmod -t dir`。"
            }
        ]
    },
    {
        "title": "让一个程序以文件属主的身份运行（SUID）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 4,
        "total_score": 18,
        "tags": [
            "chmod",
            "SUID",
            "u+s",
            "安全"
        ],
        "choices": [],
        "source_section": "命令特训 · 权限与属性",
        "statement_md": "有个工具脚本需要读 `/etc/shadow`，普通用户没权限。\n你要给它加 **SUID** 位，让它执行时临时获得属主权限。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "chmod u+s tool",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|chmod u+s tool\n|chmod 4755 tool\n|chmod 4u+s tool\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`chmod u+s tool`（数字写法 `chmod 4755 tool`）。\n\n- `u+s` 给**属主位**加 SUID，长格式显示属主的 `x` 变成 **`s`**：`-rwsr-xr-x`\n- 如果原本属主**没有 `x`**，`s` 会显示成**大写 `S`** —— 那是「有 SUID 但不可执行」的无效状态，等于白设\n\n★ 数字写法：`4` 是 SUID 的位置，写在三位权限之前，所以 `755 + SUID` = `4755`。\n\n★ **安全警告**：SUID 是提权漏洞的头号载体。给 shell 脚本加 SUID **在 Linux 上通常无效**（内核会忽略脚本的 SUID 位），而且能被利用的 SUID 程序等于给了所有人 root。能用 `sudo` 精确授权就别用 SUID。\n\n★ **迁移**：SGID（`g+s` / `2000`）对**目录**的意义不同 —— 在该目录里新建的文件会**继承目录的属组**，这是团队共享目录的标准做法。"
            }
        ]
    },
    {
        "title": "查看文件的八进制权限（不要符号位）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "stat",
            "%a",
            "八进制"
        ],
        "choices": [],
        "source_section": "命令特训 · 权限与属性",
        "statement_md": "脚本里要判断某个文件的权限是不是 `600`，需要**纯数字**。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "stat -c '%a' secret.key",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|stat -c '%a' secret.key\n|stat -c %a secret.key\n|stat -c \"%a\" secret.key\n|stat -c %a secret.key\n|stat -c '%a %n' secret.key\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`stat -c '%a' secret.key`。\n\n`stat` 的 `-c`（`--format`）可以自定义输出格式，`%a` = **八进制权限**。输出形如 `600`（不带前导 0，所以别拿它直接和 `0600` 字符串比较）。\n\n★ 其他常用占位符：\n- `%A` 符号位（`-rw-------`）\n- `%U` 属主名、`%G` 属组名\n- `%s` 字节大小、`%n` 文件名\n- `%i` inode 号\n\n★ 想要 `0600` 带前导零的格式用 `%04a`。\n\n★ **迁移**：`find . -perm 600` 是按权限查文件；`stat -c '%a'` 是**看某一个**文件。批量审计时用前者，单点确认用后者。"
            }
        ]
    },
    {
        "title": "查看文件的符号权限与属主（一行说清）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "stat",
            "%A",
            "属主",
            "ls -l"
        ],
        "choices": [],
        "source_section": "命令特训 · 权限与属性",
        "statement_md": "要在一个脚本里同时拿到**权限串 + 属主 + 属组 + 文件名**。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "stat -c '%A %U %G %n' file",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|stat -c '%A %U %G %n' file\n|stat -c '%A %U:%G %n' file\n|ls -l file\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`stat -c '%A %U %G %n' file`。\n\n输出形如 `-rw-r--r-- root root app.conf` —— **格式由你定**，这是 `stat` 比 `ls -l` 强的地方：`ls -l` 的列宽与顺序是给人看的，字段位置随内容浮动；`stat -c` 的输出**字段顺序固定**，脚本里 `cut`/`awk` 才可靠。\n\n★ `%A` 是符号权限（10 位，含文件类型位）；`%a` 是八进制权限（3~4 位数字）。差一个大小写，意思完全不同。\n\n★ 为什么不用 `ls -l | awk '{print $1}'`：文件名里有空格时 `ls` 的列会错位；`stat -c` 按文件名逐个处理，不受影响。\n\n★ **迁移**：`stat -c '%y'` 看人类可读的修改时间，`%Y` 是 Unix 时间戳 —— 写「文件是不是 24 小时没更新了」的判断时用后者。"
            }
        ]
    },
    {
        "title": "只改属组，不动属主",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "chgrp",
            "属组",
            "chown"
        ],
        "choices": [],
        "source_section": "命令特训 · 权限与属性",
        "statement_md": "`/srv/data/report.csv` 的属主是对的，但属组要改成 `dev`。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "chgrp dev /srv/data/report.csv",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|chgrp dev /srv/data/report.csv\n|chown :dev /srv/data/report.csv\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`chgrp dev /srv/data/report.csv`（或 `chown :dev 文件`）。\n\n`chgrp` 是「change group」的专用命令，只动属组。`chown :dev` 里冒号前留空，也是「只改属组」的意思 —— 两种写法效果一样，`chgrp` 语义更清楚。\n\n★ 权限要求：普通用户只能把文件的属组改成**自己所属的组**（`id` 里能看到的那几个）；改到别的组需要 root。\n\n★ 递归改整棵树：`chgrp -R dev /srv/data`。\n\n★ **迁移**：`chown user: file` 里的冒号后留空 = 「属组改成该用户的**登录主组**」，很多人以为那是「属组不变」，其实变了 —— 这点极易搞混。"
            }
        ]
    },
    {
        "title": "给单个用户单独授权（不改变文件属主）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 4,
        "total_score": 18,
        "tags": [
            "setfacl",
            "ACL",
            "授权"
        ],
        "choices": [],
        "source_section": "命令特训 · 权限与属性",
        "statement_md": "`project/` 属于 `alice`，但要让 `bob` 也能读写里面的内容，而**不能改属主**（alice 还要用）。\n\n要求：用 ACL 给 bob 单独授权（递归）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "setfacl -R -m u:bob:rw project/",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|setfacl -R -m u:bob:rw project/\n|setfacl -Rm u:bob:rw project/\n|setfacl --recursive -m u:bob:rw project/\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`setfacl -R -m u:bob:rw project/`。\n\nACL（Access Control List）解决的就是传统 9 位权限做不到的事：**给特定某个人单独授权**，而不是只能按「属主/组/其他」三档。\n\n★ 参数拆解：\n- `-m`（modify）修改 ACL 条目\n- `u:bob:rw` 用户 bob 给读写权限\n- `-R` 递归\n\n★ 递归设完还要 `setfacl -R -d -m u:bob:rw project/` 设**默认 ACL**，否则**之后新建**的文件不会继承这条授权 —— 这是 ACL 最常被漏掉的一步。`-d` 就是「default」。\n\n★ 设完之后 `ls -l` 会在权限串末尾多一个 **`+`** 号（`-rw-rw-r--+`），表示「这个文件有扩展 ACL」。\n\n★ **迁移**：`getfacl project/` 查看，`setfacl -x u:bob project/` 撤销，`setfacl -b` 清空所有 ACL。"
            }
        ]
    },
    {
        "title": "查看文件上的 ACL 规则",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "getfacl",
            "ACL",
            "mask"
        ],
        "choices": [],
        "source_section": "命令特训 · 权限与属性",
        "statement_md": "有个文件的权限串末尾带 `+`，你要看它到底给了谁什么权限。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "getfacl file",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|getfacl file\n|getfacl -p file\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`getfacl file`。\n\n输出会列出：\n- `# file:` / `# owner:` / `# group:` 注释行\n- `user::rw-`（属主，两个冒号之间为空）\n- `user:bob:rw-`（**具名用户**，这就是 ACL 加的那条）\n- `group::r--`（属组）\n- `mask::rw-`（**有效权限上限**）\n- `other::r--`\n\n★ `mask` 是 ACL 的核心概念：**所有具名用户和组的权限都会被 mask 截断**。所以 `user:bob:rwx` + `mask::r--` 实际只有 `r`。「明明给了 rwx 却不能用」八成就是 mask 挡着。\n\n★ 只想看有效权限：`getfacl -e file`。\n\n★ **迁移**：`getfacl -R dir > acl.txt` 备份、`setfacl --restore=acl.txt` 恢复 —— 迁移目录时比手动重设省太多事。"
            }
        ]
    },
    {
        "title": "批量找出所有「其他人可写」的文件",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 4,
        "total_score": 18,
        "tags": [
            "find",
            "-perm",
            "安全",
            "o+w"
        ],
        "choices": [],
        "source_section": "命令特训 · 权限与属性",
        "statement_md": "安全审计：找出系统里**任何用户都能写**的文件（这是提权风险）。\n\n写出这条命令（从 /etc 开始，忽略错误）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "find /etc -type f -perm -o+w 2>/dev/null",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|find /etc -type f -perm -o+w 2>/dev/null\n|find /etc -type f -perm /o+w 2>/dev/null\n|find /etc -type f -perm -002 2>/dev/null\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`find /etc -type f -perm -o+w 2>/dev/null`。\n\n★ 必须用**减号** `-o+w`（或 `/o+w`），不能用 `-perm o+w`：不带符号是「精确相等」，而「其他人可写」的文件通常还带一堆别的位，精确匹配等于什么都找不到。\n\n★ `-o+w` 与 `-002` 是同一件事的两种写法（`002` 是「其他」位的写权限）。符号写法可读性更好。\n\n★ 这类文件为什么危险：`/etc/cron.d/` 下如果有个人人可写的文件，任何用户都能往里塞定时任务，直接提权到 root。\n\n★ **迁移**：配合 `-ls` 看详情：`find /etc -perm -o+w -ls`；查目录用 `-type d`（目录人人可写同样是大事，`/tmp` 除外——它有 sticky 位保护）。"
            }
        ]
    },
    {
        "title": "看当前 umask 值",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "umask",
            "-S",
            "默认权限"
        ],
        "choices": [],
        "source_section": "命令特训 · 权限与属性",
        "statement_md": "新建文件默认是 `644`、目录是 `755`，这个「默认」由 umask 决定。\n\n要求：把当前 umask **以符号形式**显示出来。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "umask -S",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|umask -S\n|umask\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`umask -S`（符号形式）。\n\n两种输出的区别：\n- `umask` → `0022`（**遮掉的位**）\n- `umask -S` → `u=rwx,g=rx,o=rx`（**实际允许的位**）\n\n★ umask 是**掩码**，算的是「减」：\n- 文件基准是 `666`，`666 - 022` = `644`\n- 目录基准是 `777`，`777 - 022` = `755`\n\n★ 注意「减」不是十进制减法，是**按位去掉**。所以 `umask 027` 得到文件 `640`、目录 `750`。\n\n★ `umask` 只影响**新建**的文件，对已存在的文件毫无作用 —— 这是它与 `chmod` 最本质的区别。\n\n★ **迁移**：临时改用 `umask 077`（会话内有效）；永久改写到 `/etc/profile` 或 `~/.bashrc`。共享目录想让新文件归属组可写，用 `umask 002`。"
            }
        ]
    },
    {
        "title": "递归把整个目录的属主改成 www-data",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "chown",
            "-R",
            "www-data"
        ],
        "choices": [],
        "source_section": "命令特训 · 权限与属性",
        "statement_md": "网站文件被 root 拷进去了，现在要整体交给 `www-data`（保持属组不变）。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "chown -R www-data /var/www/html",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|chown -R www-data /var/www/html\n|chown -R www-data:www-data /var/www/html\n|chown --recursive www-data /var/www/html\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`chown -R www-data /var/www/html`。\n\n★ 只写用户名 = **只改属主**，属组保持原样。要连属组一起改是 `www-data:www-data`（或 `www-data.www-data`）。\n\n★ 两者的选择：很多场景**属组保持不变更好**，因为组权限可能是刻意配的（比如 `nginx` 组）。盲目 `chown -R user:group` 会把组的授权关系一起冲掉。\n\n★ `-R` 对软链默认**不跟随**（改的是链接自身）。想连目标一起改要 `-h`（改链接）或 `-L`（改目标），但 `-L` 有跟到 `/` 的风险，慎用。\n\n★ **迁移**：`chown -R --from=root www-data /var/www` 只改**原本属主是 root** 的那些，避免把已正确设置的目录也重刷一遍（大目录树能省很多时间）。"
            }
        ]
    },
    {
        "title": "确认某个目录的权限串到底对不对（含特殊位）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "ls",
            "-ld",
            "权限串",
            "排查"
        ],
        "choices": [],
        "source_section": "命令特训 · 权限与属性",
        "statement_md": "排查「为什么别人进不去 `/srv/share`」，你要看**这个目录本身**的完整权限串。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ls -ld /srv/share",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ls -ld /srv/share\n|stat -c '%A %U:%G %n' /srv/share\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`ls -ld /srv/share`。\n\n★ `-d` 是关键：`ls -l /srv/share` 列的是**里面**的东西，要看目录自己必须 `-d`。\n\n★ 读权限串的四个要点：\n1. 第一个字符是**类型**：`d` 目录、`-` 文件、`l` 软链\n2. 后 9 位分三组：属主 / 属组 / 其他\n3. **特殊位**会覆盖 `x` 的位置：`s`（SUID/SGID）、`t`（sticky）、大写 `S`/`T` 表示「有位但没 `x`」（无效状态）\n4. 末尾的 `+` 表示有 ACL，`.` 表示有 SELinux 上下文\n\n★ 「进不去」的排查顺序：\n- 目录本身有没有 `x`（没有 `x` 就 `cd` 不进去）\n- 路径上**每一级**父目录有没有 `x`（少一级都不行）\n- SELinux 有没有拦（`ls -Z` 看上下文）\n\n★ **迁移**：`namei -l /srv/share` 一次列出**整条路径每一级**的权限，这是排查「进不去」最快的工具。"
            }
        ]
    },
    {
        "title": "把文件的属主和属组换成数字 UID/GID",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "chown",
            "UID",
            "GID",
            "容器"
        ],
        "choices": [],
        "source_section": "命令特训 · 权限与属性",
        "statement_md": "容器里没有对应的用户名（`/etc/passwd` 里查不到），只能用数字 ID 1000:1000 改属主。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "chown 1000:1000 file",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|chown 1000:1000 file\n|chown -R 1000:1000 file\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`chown 1000:1000 file`。\n\n★ `chown` 完全接受**数字 UID/GID**，不需要先建用户。这在容器/挂载卷场景是刚需 —— 宿主机上的 UID 到容器里往往没有对应名字，`ls -l` 会直接显示数字。\n\n★ 为什么不建议用名字：`chown www-data` 依赖当前系统的 `/etc/passwd`；换台机器（或容器）用户名可能不同甚至不存在，脚本就崩了。用**数字**才是可移植的。\n\n★ 但数字的代价是可读性差 —— 所以「在配置文件里写数字、在注释里写名字」是常见折中。\n\n★ **迁移**：`ls -n` 以数字形式显示属主属组，排查「这个 UID 到底是谁」时先用它，再 `id -nu <uid>` 反查名字。"
            }
        ]
    },
    {
        "title": "去掉文件的 SUID 位（安全加固）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "chmod",
            "u-s",
            "SUID",
            "加固"
        ],
        "choices": [],
        "source_section": "命令特训 · 权限与属性",
        "statement_md": "审计发现 `/usr/local/bin/oldtool` 带着 SUID，要**去掉这个危险位**。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "chmod u-s /usr/local/bin/oldtool",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|chmod u-s /usr/local/bin/oldtool\n|chmod 0755 /usr/local/bin/oldtool\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`chmod u-s /usr/local/bin/oldtool`。\n\n`u-s` 精确地只摘掉 SUID，其他位一个不动 —— 这是最安全的手术式做法。\n\n★ `chmod 0755` 也能达到效果（四位数写 `0` 前缀就是显式声明无特殊位），但它**顺带把权限重设成 755** —— 如果原文件是 `4711`，你会把属组/其他的执行位也一起改掉。「精确去掉一位」和「重设整个权限」是两件事。\n\n★ 为什么写成 `0755` 而不是 `755`：四位数时最高位就是特殊位，`0755` 明确表示「SUID/SGID/sticky 全为 0」。`755` 会被理解成三位权限、特殊位不动 —— **这就是去掉 SUID 时 `755` 不管用的原因**（实际 GNU chmod 会把 `755` 当 `0755` 处理，但写全四位更不容易误解）。\n\n★ **迁移**：批量清理：`find / -perm -4000 -type f -exec chmod u-s {} +`，但**先确认清单**——把 `/usr/bin/passwd`、`/usr/bin/sudo` 的 SUID 去掉会锁死系统。"
            }
        ]
    },
    {
        "title": "建一个新用户并顺手建家目录",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "useradd",
            "-m",
            "家目录"
        ],
        "choices": [],
        "source_section": "命令特训 · 用户与组",
        "statement_md": "要给实习生开账号 `zhangsan`，家目录默认位置，**同时创建家目录**并把骨架文件拷进去。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "useradd -m zhangsan",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|useradd -m zhangsan\n|useradd --create-home zhangsan\n|adduser zhangsan\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`useradd -m zhangsan`。\n\n★ **`-m` 在不同发行版上默认值相反**，这是最大的一处坑：\n- **Fedora / RHEL / CentOS**：默认 **不** 建家目录，必须写 `-m`\n- **Debian / Ubuntu**：`useradd` 默认不建，但 `adduser` 会建\n\n没建家目录的后果：登录后落在 `/`，`~/.bashrc` 不存在，一切「用户配置」都失效，而且**不会报错**——只是到处不对劲。\n\n★ `adduser` 是发行版的**友好封装**（Fedora 上它其实是 `useradd` 的软链，Debian 上是个交互式脚本）。脚本里要可移植，用 `useradd` 并把选项写全。\n\n★ **迁移**：`useradd -m -s /bin/bash -G wheel zhangsan` 一次把家目录、shell、附加组都定好，比事后 `usermod` 三次干净。"
            }
        ]
    },
    {
        "title": "改用户的登录 shell",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "usermod",
            "-s",
            "shell"
        ],
        "choices": [],
        "source_section": "命令特训 · 用户与组",
        "statement_md": "`zhangsan` 现在的 shell 是 `/bin/sh`，要改成 `/bin/bash`。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "usermod -s /bin/bash zhangsan",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|usermod -s /bin/bash zhangsan\n|usermod --shell /bin/bash zhangsan\n|chsh -s /bin/bash zhangsan\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`usermod -s /bin/bash zhangsan`。\n\n`-s`（`--shell`）改的是 `/etc/passwd` 第 7 个字段。\n\n★ 三个必须同时满足才会生效：\n1. 目标 shell **必须写在 `/etc/shells` 里**，否则登录程序（`login`/`sshd`）会拒绝并回退到 `/bin/sh`\n2. 用户**当前没登录**时才能改（正在用的话改完不生效，下次登录才生效）\n3. 文件本身可执行\n\n★ `chsh -s /bin/bash zhangsan` 也能改，但它是**交互式**的（会问你密码），脚本里不适合，而且需要 `util-linux-user` 包。\n\n★ **迁移**：`grep zhangsan /etc/passwd | cut -d: -f7` 直接查当前 shell，比 `finger` 之类的工具可靠。"
            }
        ]
    },
    {
        "title": "把用户加到一个附加组（不动主组）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "usermod",
            "-aG",
            "附加组",
            "wheel"
        ],
        "choices": [],
        "source_section": "命令特训 · 用户与组",
        "statement_md": "要让 `zhangsan` 能用 `sudo`，需要把他加进 `wheel` 组。\n\n要求：**保留**他原有的其他附加组，只新增一个。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "usermod -aG wheel zhangsan",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|usermod -aG wheel zhangsan\n|usermod -a -G wheel zhangsan\n|gpasswd -a zhangsan wheel\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`usermod -aG wheel zhangsan`。\n\n★ **`-a` 绝对不能漏** —— 这是 Linux 用户管理里最著名的一脚：`usermod -G wheel zhangsan`（没有 `-a`）会把用户的附加组**整个替换**成 `wheel`，之前加的所有组（`docker`、`libvirt`…）**全部丢失**。而且没有任何提示。\n\n记忆法：`-a` = append（追加），`-G` = 附加组（groups）。**改附加组永远要 `-aG`**。\n\n★ 注意大小写：`-G` 是附加组，`-g` 是**主组**（会改 `/etc/passwd` 第 4 字段）。`-g` 用错了用户的家目录归属关系都会变。\n\n★ **迁移**：`gpasswd -a user group` 是另一种写法（同样安全，不会有覆盖问题）；`groups zhangsan` 或 `id zhangsan` 验证结果。"
            }
        ]
    },
    {
        "title": "设置/修改用户密码",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "passwd",
            "密码",
            "shadow"
        ],
        "choices": [],
        "source_section": "命令特训 · 用户与组",
        "statement_md": "给 `zhangsan` 设密码（交互式输入，不写在命令行里）。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "passwd zhangsan",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|passwd zhangsan\n|sudo passwd zhangsan\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`passwd zhangsan`（普通用户改自己用 `passwd`，root 改别人要指定用户名）。\n\n★ 为什么不在命令行里写密码：`passwd zhangsan mypass` 这种写法**根本不存在** —— `passwd` 只从 stdin 读。脚本里批量设密码要用 `chpasswd`（`echo 'user:pass' | chpasswd`）或 `passwd --stdin`（仅 RHEL 系）。\n\n★ 密码存在 `/etc/shadow`（root 可读、权限 `000` 或 `400`），`/etc/passwd` 里那个 `x` 只是个占位符 —— 这是「shadow 套件」的核心设计：把密码哈希从人人可读的文件里挪走。\n\n★ **迁移**：`chage -l zhangsan` 看密码有效期；`passwd -l` 锁定账号、`passwd -u` 解锁；`passwd -e` 强制下次登录改密码。"
            }
        ]
    },
    {
        "title": "删除用户，连家目录一起删掉",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "userdel",
            "-r",
            "删除用户"
        ],
        "choices": [],
        "source_section": "命令特训 · 用户与组",
        "statement_md": "实习生走了，要把 `zhangsan` 彻底清掉：账号 + 家目录 + 邮件目录。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "userdel -r zhangsan",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|userdel -r zhangsan\n|userdel --remove zhangsan\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`userdel -r zhangsan`。\n\n★ 不加 `-r` 的后果：账号在 `/etc/passwd` 里没了，但 `/home/zhangsan` 原样留着，属主变成一串**数字 UID**（因为名字查不到了）。下次新建用户恰好分配到同一个 UID 时，**新用户直接继承旧用户的所有文件** —— 这是个真实存在的安全事故。\n\n★ `-r` 会删家目录与邮件池（`/var/mail/zhangsan`），但**不删**该用户在系统其它位置创建的文件（比如 `/srv` 下的）。彻底清理还得 `find / -uid <旧UID> -ls` 查一遍。\n\n★ 用户**正在登录**时 `userdel` 会失败，得先 `pkill -u zhangsan` 或等他退出。\n\n★ **迁移**：更温和的做法是先 `usermod -L`（锁定）观察一段时间，确认无影响再 `userdel -r`。"
            }
        ]
    },
    {
        "title": "看自己属于哪些组",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "id",
            "组",
            "docker"
        ],
        "choices": [],
        "source_section": "命令特训 · 用户与组",
        "statement_md": "写 Docker 命令报 `permission denied`，怀疑是自己不在 `docker` 组。\n\n要求：输出**当前用户**的 UID、GID 和所有组。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "id",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|id\n|id $(whoami)\n|groups\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`id`。\n\n输出形如 `uid=1000(cosy) gid=1000(cosy) groups=1000(cosy),10(wheel),994(docker)`。\n\n★ 三个字段分别对应：\n- `uid` 用户 ID\n- `gid` **主组** ID（决定新建文件的默认属组）\n- `groups` 主组 + 所有**附加组**\n\n★ 为什么 `groups` 里明明有 `docker` 还是不能用：**组成员关系在登录时被读进进程的凭证里**，改完组必须**重新登录**（或 `newgrp docker` 开个新 shell）才生效。`usermod` 完马上试，永远失败。\n\n★ **迁移**：`id zhangsan` 查别人；`id -nG` 只列组名；`id -u` 只给 UID（脚本里判断是不是 root 用 `[ $(id -u) -eq 0 ]`）。"
            }
        ]
    },
    {
        "title": "看当前谁登录着、在干什么",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "w",
            "who",
            "登录"
        ],
        "choices": [],
        "source_section": "命令特训 · 用户与组",
        "statement_md": "要确认同事是不是还挂在服务器上（准备重启）。\n\n要求：显示登录用户 + 他们在跑的**命令**。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "w",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|w\n|W\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`w`。\n\n`w` 的输出比 `who` 多两样最关键的东西：**每个用户当前在跑什么命令**（`WHAT` 列）和**系统负载**（第一行）。\n\n★ 各列含义：`USER` 用户、`TTY` 终端、`FROM` 来源 IP、`LOGIN@` 登录时间、`IDLE` 空闲时长、`JCPU`/`PCPU` CPU 占用、`WHAT` 当前命令。\n\n★ `JCPU` 是「该终端上所有进程累计占用」，`PCPU` 是「`WHAT` 那个进程占用」—— 两个别混。\n\n★ **迁移**：`who` 只列登录会话（不含命令）；`last` 看**历史**登录记录（从 `/var/log/wtmp` 读）；`lastb` 看失败的登录尝试（排查暴力破解）。"
            }
        ]
    },
    {
        "title": "以另一个用户的身份执行一条命令",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "su",
            "sudo",
            "-c",
            "切换用户"
        ],
        "choices": [],
        "source_section": "命令特训 · 用户与组",
        "statement_md": "你是 root，要**以 `zhangsan` 的身份**跑 `whoami` 验证权限，而不是切过去再切回来。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "su - zhangsan -c whoami",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|su - zhangsan -c whoami\n|su zhangsan -c whoami\n|sudo -u zhangsan whoami\n|runuser -u zhangsan -- whoami\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`su - zhangsan -c whoami`（或 `sudo -u zhangsan whoami`）。\n\n★ **`su -` 与 `su` 的区别是本题的重点**：\n- `su - zhangsan`（带横杠）= **登录式**切换：加载对方的完整环境（`$HOME`、`$PATH`、`$SHELL`、`.bash_profile`）\n- `su zhangsan` = **非登录式**：保持当前环境变量，只换 uid\n\n不带横杠时 `$HOME` 还是原来的，于是「以 zhangsan 身份」跑出来的东西可能读写的是**你的**家目录 —— 排查权限问题时这会造成大量假象。\n\n★ `-c` 让命令跑完就退出，不用交互。\n\n★ **迁移**：`sudo -u user cmd` 不需要知道对方密码（靠 sudoers 授权），审计更清晰（有日志）；`su` 需要对方密码。生产环境里优先 `sudo -u`。"
            }
        ]
    },
    {
        "title": "建一个新组",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "groupadd",
            "-g",
            "GID"
        ],
        "choices": [],
        "source_section": "命令特训 · 用户与组",
        "statement_md": "项目需要一个新的组 `devteam`，GID 指定为 3000。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "groupadd -g 3000 devteam",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|groupadd -g 3000 devteam\n|groupadd --gid 3000 devteam\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`groupadd -g 3000 devteam`。\n\n★ `-g` 指定 **GID**（组 ID）；不指定则由系统按 `GID_MIN`~`GID_MAX` 自动挑一个。\n\n★ 为什么有时要手动指定 GID：**跨机器保持一致**。NFS / 共享存储 / 容器挂载都靠数字 GID 认人，两台机器上同名组 GID 不同就会互相看不到对方文件的组权限。\n\n★ 同名组已存在会报 `group 'devteam' already exists`；`-f`（force）可以强制成功返回 0，写幂等脚本时有用。\n\n★ **迁移**：`groupmod -n newname oldname` 改组名（GID 不变，所以文件权限关系不受影响）；`groupdel` 删组（组里还有用户时会警告，但不会阻止）。"
            }
        ]
    },
    {
        "title": "看一个用户的 UID、主组和附加组（一次问全）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "id",
            "groups",
            "getent"
        ],
        "choices": [],
        "source_section": "命令特训 · 用户与组",
        "statement_md": "要给 `zhangsan` 配权限，先得知道他到底属于哪些组。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "id zhangsan",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|id zhangsan\n|groups zhangsan\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`id zhangsan`。\n\n`groups` 只给组名列表，`id` 还给 **UID 和主组**，信息更全。\n\n★ 输出里 `gid=1000(zhangsan)` 是**主组**，后面 `groups=` 里的才是附加组。主组决定新建文件的属组（没有 SGID 的情况下）。\n\n★ 注意 `id` 输出的是**目标用户当前的数据库状态**，如果该用户有活跃会话，他的进程凭证里可能还是**旧**的组 —— 这就是「`id` 说在 docker 组里，但命令还是权限不足」的原因。\n\n★ **迁移**：`id -u zhangsan` 拿 UID 用来 `find -uid`；`id -Gn zhangsan` 只看组名；`getent group devteam` 看某个组里有谁（比 `/etc/group` 可靠，因为能覆盖 LDAP/SSSD 等外部目录）。"
            }
        ]
    },
    {
        "title": "查看系统里所有用户（含系统账号）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "passwd",
            "cut",
            "账号清单"
        ],
        "choices": [],
        "source_section": "命令特训 · 用户与组",
        "statement_md": "要清点系统上的账号。\n\n要求：列表形式输出**所有**用户（包括 UID < 1000 的系统账号）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "cut -d: -f1 /etc/passwd",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|cut -d: -f1 /etc/passwd\n|awk -F: '{print $1}' /etc/passwd\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`cut -d: -f1 /etc/passwd`。\n\n`/etc/passwd` 第 1 列就是用户名，共 7 个字段：\n`用户名:密码占位:UID:GID:注释:家目录:登录shell`\n\n★ 为什么不用 `getent passwd`：两者**都能列出全部用户**，但 `getent` 还会包含 LDAP/SSSD/NIS 等外部目录的用户，`/etc/passwd` 只有本地账号。「清点本机账号」用前者，「清点所有能登录的身份」用 `getent`。\n\n★ 只想要**能登录**的用户：`awk -F: '$7 !~ /nologin|false/ {print $1}' /etc/passwd`。\n\n★ **迁移**：`awk -F: '$3 >= 1000 {print $1}' /etc/passwd` 只列普通用户（Fedora 的 `UID_MIN` 是 1000）；`lastlog` 看每个账号最后一次登录时间，清账号前很有用。"
            }
        ]
    },
    {
        "title": "让用户下次登录必须改密码",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "passwd",
            "-e",
            "chage",
            "密码过期"
        ],
        "choices": [],
        "source_section": "命令特训 · 用户与组",
        "statement_md": "新建的账号要给本人，密码是临时的，**必须强制他首次登录就改**。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "passwd -e zhangsan",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|passwd -e zhangsan\n|chage -d 0 zhangsan\n|passwd --expire zhangsan\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`passwd -e zhangsan`（或 `chage -d 0 zhangsan`）。\n\n原理：把 `/etc/shadow` 里的「最后修改密码日期」置为 **0**，于是系统判定密码已过期，下次登录强制改。\n\n★ 三种等效写法：\n- `passwd -e user`（expire，最直白）\n- `chage -d 0 user`（把最后修改日设为 1970-01-01）\n- `chage -d $(date +%s | awk '{print int($1/86400)}')` 才是「今天」，别用\n\n★ **迁移**：`chage -l user` 看密码策略全貌；`chage -M 90 user` 设「90 天必须改」；`chage -W 7 user` 提前 7 天开始提醒。企业环境的密码策略基本都靠 `chage` 配。"
            }
        ]
    },
    {
        "title": "临时让别人用一次 admin 权限（不用给 root 密码）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "visudo",
            "sudoers",
            "授权"
        ],
        "choices": [],
        "source_section": "命令特训 · 用户与组",
        "statement_md": "要允许 `zhangsan` 执行 `/usr/bin/systemctl restart nginx`，但**不给完整 root**。\n\n要求：写出打开 sudoers 编辑器的命令（用 visudo 而不是直接 vim）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "visudo",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|visudo\n|sudo visudo\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`visudo`。\n\n★ **为什么必须用 `visudo` 而不是 `vim /etc/sudoers`**：`visudo` 会在保存时**做语法检查**。sudoers 语法错了会导致**所有人（含 root）都无法 sudo**，而普通用户没权限改回来 —— 只能进单用户模式修复。这是教科书级的「一条命令锁死系统」。\n\n★ 里面加一行实现本题：\n```\nzhangsan ALL=(root) NOPASSWD: /usr/bin/systemctl restart nginx\n```\n`NOPASSWD:` 表示免密码，`/usr/bin/` 必须写**绝对路径**（权限校验按路径精确匹配）。\n\n★ 更规范的做法是放到 `/etc/sudoers.d/` 下单独一个文件，不动主文件，便于审计与回滚。\n\n★ **迁移**：`sudo -l -U zhangsan` 列出某人能执行什么，排「为什么他 sudo 被拒」时第一步就看这个。"
            }
        ]
    },
    {
        "title": "查某个用户最近登录过没有",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "lastlog",
            "last",
            "审计"
        ],
        "choices": [],
        "source_section": "命令特训 · 用户与组",
        "statement_md": "要清理长期不用的账号，先看 `zhangsan` **上次登录**是什么时候。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "lastlog -u zhangsan",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|lastlog -u zhangsan\n|last zhangsan\n|lastlog | grep zhangsan\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`lastlog -u zhangsan`。\n\n`lastlog` 从 `/var/log/lastlog` 读**每个账号最后一次登录**的记录，`-u` 只看指定用户。输出 `Never logged in` 表示从没登录过。\n\n★ `last zhangsan` 是**另一回事**：它列该用户的**登录历史**（从 `/var/log/wtmp` 读，含登录/登出时间、来源 IP、会话时长），能看到「最近 10 次都从哪登的」。「最后登录时间」用 `lastlog`，「登录历史」用 `last`。\n\n★ 两者都依赖日志文件存在与轮转策略 —— `/var/log/wtmp` 被清过的话 `last` 就空了，但 `lastlog` 仍然有（它是每用户一个记录，不是流水账）。\n\n★ **迁移**：`lastlog | grep Never` 一把捞出所有「从没登录过」的账号，这是清理僵尸账号的起手式。"
            }
        ]
    },
    {
        "title": "看系统里有哪些组、各自的 GID",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "group",
            "getent",
            "GID"
        ],
        "choices": [],
        "source_section": "命令特训 · 用户与组",
        "statement_md": "要给新用户配组，先摸清现有的组。\n\n写出这条命令（本地组）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "cut -d: -f1,3 /etc/group",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|cut -d: -f1,3 /etc/group\n|awk -F: '{print $1, $3}' /etc/group\n|getent group\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`cut -d: -f1,3 /etc/group`。\n\n`/etc/group` 每行 4 个字段：`组名:密码占位:GID:成员列表`。`-f1,3` 一次取两列。\n\n★ `getent group` 才是「系统真正认的组列表」—— 如果配了 LDAP/SSSD，`/etc/group` 里**看不到**外部目录的组，但 `getent group` 能列出来。排查「组的名字明明存在却用不了」时，`getent` 是分水岭。\n\n★ 第 4 字段是**附加组**成员列表，**主组**成员不写在这里（主组信息在 `/etc/passwd` 第 4 字段）。所以 `grep devteam /etc/group` 看不到「主组是 devteam」的那些人，这是高频误会。\n\n★ **迁移**：`getent group devteam` 精确查一个组；`lid -g devteam`（libuser 包）能连主组成员一起列出。"
            }
        ]
    },
    {
        "title": "看系统里所有进程（完整命令行）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "ps",
            "aux",
            "-ef",
            "进程"
        ],
        "choices": [],
        "source_section": "命令特训 · 进程与作业",
        "statement_md": "要排查一个服务起了几个实例，需要看**完整命令行**而不是被截断的名字。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ps aux",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ps aux\n|ps -ef\n|ps -efl\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`ps aux`（BSD 风格）或 `ps -ef`（System V 风格）。\n\n★ **两种风格的选项写法不一样，混用会报错**：\n- BSD：`ps aux` —— 不带横杠，`a` 所有终端的进程、`u` 用户格式、`x` 含无终端的进程\n- SysV：`ps -ef` —— 带横杠，`-e` 所有进程、`-f` 完整格式\n写成 `ps auxf` 或 `ps -aux` 都能跑（Linux 的 ps 很宽容），但严格 POSIX 环境只认 `-ef`。\n\n★ `aux` 的 `x` 很关键：不加它**看不到后台守护进程**（它们没有控制终端），于是「服务明明在跑却 ps 不到」。\n\n★ 命令行太长会被截断到终端宽度；`ps -ef` 配 `-w -w`（`--width`）或 `ps auxww` 才显示全。\n\n★ **迁移**：`ps -eo pid,ppid,user,%cpu,%mem,cmd --sort=-%cpu | head` 按 CPU 排序取前几名，比 `top` 更适合脚本化。"
            }
        ]
    },
    {
        "title": "按名字找进程的 PID",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "pgrep",
            "pidof",
            "PID"
        ],
        "choices": [],
        "source_section": "命令特训 · 进程与作业",
        "statement_md": "要重启 nginx，先拿到它的 PID。\n\n写出这条命令（按**进程名**精确匹配）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "pgrep nginx",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|pgrep nginx\n|pidof nginx\n|ps -C nginx -o pid=\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`pgrep nginx`。\n\n★ `pgrep` 匹配的是**进程名**（`comm`，即去掉路径的可执行文件名），默认是**子串**匹配 —— `pgrep nginx` 会同时命中 `nginx` 和 `nginx-worker`。要精确匹配加 `-x`：`pgrep -x nginx`。\n\n★ 三种工具的差别：\n- `pgrep` 按名字匹配，支持 `-u`（按用户）、`-f`（匹配完整命令行）\n- `pidof` 精确匹配可执行文件名，**只输出 PID**，最干净\n- `ps -C` 按 `comm` 精确匹配，`-o pid=` 去掉表头只有数字\n\n★ `pgrep` **没有匹配时退出码是 1**（不是 0）—— 脚本里 `set -e` 会因此中断，写 `pgrep nginx || true`。\n\n★ **迁移**：`pgrep -a nginx` 连命令行一起显示；`pgrep -f 'python.*worker'` 匹配完整命令（适合解释器类进程，因为它们的进程名都是 `python3`）。"
            }
        ]
    },
    {
        "title": "结束一个进程（先礼后兵）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "kill",
            "-15",
            "SIGTERM"
        ],
        "choices": [],
        "source_section": "命令特训 · 进程与作业",
        "statement_md": "某个 `python3` 进程卡住了，PID 是 4567。\n\n要求：先发**默认终止信号**（礼貌请求退出），不要一上来就强杀。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "kill 4567",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|kill 4567\n|kill -15 4567\n|kill -TERM 4567\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`kill 4567`（等价于 `kill -15` / `-TERM`）。\n\n★ `kill` 这个名字**名不副实**：它其实是「**发信号**」，发什么信号由参数决定。默认是 `SIGTERM(15)`，意思是「请你退出」—— 进程可以捕获它做清理（关连接、刷缓冲、删临时文件）。\n\n★ 只有进程不响应 TERM 时才用 `kill -9`（`SIGKILL`）：**KILL 无法被捕获**，进程被内核直接干掉，**没有任何清理机会** —— 数据库可能留半截事务，文件可能写坏，临时文件留着。\n\n★ 正确姿势是「**先 15，等几秒，再 9**」：\n```bash\nkill 4567; sleep 3; kill -0 4567 2>/dev/null && kill -9 4567\n```\n\n★ **迁移**：`kill -l` 列出所有信号；`kill -HUP 1234` 常被守护进程用来「重读配置」（不重启）。"
            }
        ]
    },
    {
        "title": "强制杀掉一个杀不掉的进程",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "kill",
            "-9",
            "SIGKILL"
        ],
        "choices": [],
        "source_section": "命令特训 · 进程与作业",
        "statement_md": "`kill 4567` 发了三次都没反应。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "kill -9 4567",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|kill -9 4567\n|kill -KILL 4567\n|kill -SIGKILL 4567\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`kill -9 4567`。\n\n`SIGKILL(9)` 由**内核**直接执行，进程**无法捕获、无法阻塞、无法忽略**，所以「杀不掉」的情况理论上不存在。\n\n★ 但有一种情况 `kill -9` 也没用：进程处于 **不可中断睡眠（D 状态）**，卡在磁盘 I/O 或 NFS 里。这时它连 KILL 都不响应 —— `ps` 里状态列显示 `D`。只能等 I/O 超时或重启。\n\n★ 如果进程是**僵尸（Z 状态）**，`kill -9` 也没用：僵尸已经死了，只剩一个表项等父进程回收。解决办法是杀掉/重启**它的父进程**。\n\n★ **迁移**：`ps -o pid,stat,cmd -p 4567` 看状态；`ps -eo stat,pid,cmd | grep '^[DZ]'` 一把捞出 D/Z 状态的进程。"
            }
        ]
    },
    {
        "title": "按名字批量杀进程（不用一个个 PID）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "pkill",
            "killall",
            "批量"
        ],
        "choices": [],
        "source_section": "命令特训 · 进程与作业",
        "statement_md": "起了 20 个 `worker` 进程，要一次全干掉。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "pkill worker",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|pkill worker\n|pkill -x worker\n|killall worker\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`pkill worker`（或 `killall worker`）。\n\n★ **危险警告**：`pkill` 默认是**子串匹配进程名**，`pkill worker` 会连带杀掉 `worker-manager`、`my-worker` 之类。上线机器上按名字杀之前，先用 `pgrep -a worker` **看一眼清单**。\n\n★ 精确匹配用 `-x`：`pkill -x worker` 只杀名字**完全等于** `worker` 的。\n\n★ `killall` 的行为**因系统而异**：Linux 上是「按进程名杀」，但 Solaris 上 `killall` 是「**杀掉所有进程**」（等于关机）。跨平台脚本里千万别用 `killall`。\n\n★ **迁移**：`pkill -u zhangsan` 杀某用户所有进程（踢人下线）；`pkill -f 'python3 app.py'` 按完整命令行匹配（杀解释器类进程必须用 `-f`）；`pkill -9 -f pattern` 强杀。"
            }
        ]
    },
    {
        "title": "让命令在退出终端后继续跑",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "nohup",
            "后台",
            "&",
            "SIGHUP"
        ],
        "choices": [],
        "source_section": "命令特训 · 进程与作业",
        "statement_md": "SSH 上去跑一个几小时的备份，**关掉终端不能中断它**。\n\n要求：用最经典的「忽略挂断信号」那条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "nohup ./backup.sh &",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|nohup ./backup.sh &\n|nohup ./backup.sh > backup.log 2>&1 &\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`nohup ./backup.sh &`。\n\n两个部分各解决一个问题：\n- **`nohup`** 让进程**忽略 SIGHUP**（终端关闭时内核发的「挂断」信号）\n- **`&`** 把它放到**后台**，立刻把提示符还给你\n\n★ 只写 `&` 不写 `nohup`：终端一关，SIGHUP 就把进程带走了。只写 `nohup` 不写 `&`：进程在前台，你没法继续用这个终端。\n\n★ `nohup` 会把输出**追加到 `nohup.out`**（当前目录不可写时落到 `$HOME`）。所以实际写法通常是 `nohup cmd > out.log 2>&1 &` —— `2>&1` 把 stderr 也并进同一个文件，否则报错信息会丢。\n\n★ 更现代的替代是 `tmux`/`screen`（能回去看）或 `systemd-run --user`（能纳管）。\n\n★ **迁移**：`disown` 可以把**已经跑起来**的后台任务从作业表里摘掉，效果类似 nohup。"
            }
        ]
    },
    {
        "title": "看当前 shell 里有哪些后台作业",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "jobs",
            "后台作业",
            "Ctrl+Z"
        ],
        "choices": [],
        "source_section": "命令特训 · 进程与作业",
        "statement_md": "你之前按 `Ctrl+Z` 挂起了几个任务，要看看它们还在不在。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "jobs",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|jobs\n|jobs -l\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`jobs`（`-l` 带 PID）。\n\n★ **作业（job）与进程是两个概念**：作业是**当前 shell** 管的，换个终端窗口 `jobs` 就是空的 —— 它只列本 shell 的子进程。\n\n★ 作业号（`[1]`、`[2]`）与 PID 不是一回事。`fg %1`、`bg %2`、`kill %1` 用的是**作业号**，前面要带 `%`。\n\n★ `Ctrl+Z` 发的是 **SIGTSTP**（暂停），不是终止 —— 进程还在内存里，只是不跑了。所以挂起一堆任务会一直占内存。\n\n★ **迁移**：`fg` 把最近一个作业拉回前台；`bg` 让挂起的作业在后台**继续跑**；如果终端关了，`jobs` 里的东西就随 shell 一起没了（除非用了 nohup/disown）。"
            }
        ]
    },
    {
        "title": "把挂起的作业放到后台继续跑",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "bg",
            "fg",
            "作业控制"
        ],
        "choices": [],
        "source_section": "命令特训 · 进程与作业",
        "statement_md": "你按了 `Ctrl+Z` 暂停了一个编译任务（作业号 1），现在想让它**在后台跑完**。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "bg %1",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|bg %1\n|bg\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`bg %1`。\n\n★ 前提是作业**已被挂起**（`Ctrl+Z` 或 `kill -TSTP`）。对已在前台运行的作业直接 `bg` 是无效的。\n\n★ 关键：`bg` 之后进程**继续往终端写输出** —— 如果它话很多，会一直刷屏干扰你。所以标准操作是「挂起 → bg → 输出重定向」的顺序已经晚了，更稳的做法是**一开始就 `cmd > log 2>&1 &`**。\n\n★ `bg %1` 与 `bg` 的区别：不带参数时对「当前作业」（最近挂起的那个）操作。\n\n★ **迁移**：`fg %1` 拉回前台；`jobs -l` 确认状态（`Stopped` 是挂起、`Running` 是后台运行）；要彻底脱离终端还是得 `nohup` 或 `disown`。"
            }
        ]
    },
    {
        "title": "以低优先级跑一个大编译（不抢占前台）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "nice",
            "-n",
            "优先级"
        ],
        "choices": [],
        "source_section": "命令特训 · 进程与作业",
        "statement_md": "你要编译一个大项目，但机器同时在跑线上服务，希望编译**尽量让出 CPU**。\n\n写出这条命令（nice 值设 10）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "nice -n 10 make",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|nice -n 10 make\n|nice -10 make\n|nice --adjustment=10 make\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`nice -n 10 make`。\n\n**nice 值范围 -20（最高优先级）到 19（最低）**，默认 0。普通用户**只能调高**（让自己更「客气」），只有 root 能调到负值。\n\n★ `nice -10 make` 与 `nice -n 10 make` 都表示「+10」，但 `nice --10 make` 是 **-10（提高优先级）** —— 少写一个 `n` 意思完全反过来，而且普通用户会报 `Permission denied`。所以**永远写 `-n`**，别用简写。\n\n★ nice 只影响**相对调度权重**，不是硬限速。机器空闲时低优先级的进程照样能跑满 CPU。\n\n★ **迁移**：进程已经在跑了怎么改？用 `renice`：`renice -n 10 -p 1234`（按 PID）、`renice -n 10 -u zhangsan`（按用户）。\n\n★ 真要**限制资源**（CPU 百分比、内存上限）得用 `systemd-run` 或 cgroup，nice 做不到。"
            }
        ]
    },
    {
        "title": "改一个正在运行的进程的优先级",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "renice",
            "nice",
            "优先级"
        ],
        "choices": [],
        "source_section": "命令特训 · 进程与作业",
        "statement_md": "那个编译已经跑起来了（PID 1234），现在才想起来要降优先级。\n\n写出这条命令（nice 值改成 15）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "renice -n 15 -p 1234",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|renice -n 15 -p 1234\n|renice 15 -p 1234\n|renice -n 15 1234\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`renice -n 15 -p 1234`。\n\n★ `renice` 与 `nice` 的分工：`nice` **启动时**设定，`renice` 改**已在运行**的进程。\n\n★ `-p` 后跟 PID（默认就是这个），`-u` 按**用户**（改组里所有进程），`-g` 按**进程组**。`renice -n 10 -u zhangsan` 是「把这个用户的所有进程都降级」，踢人限流时很好用。\n\n★ 权限规则同 `nice`：普通用户只能**降**优先级（数值变大），不能提；root 随便改。\n\n★ **迁移**：`ps -o pid,ni,cmd -p 1234` 看当前 nice 值（`NI` 列）；`top` 里按 `r` 键再输 PID 也能交互式 renice。"
            }
        ]
    },
    {
        "title": "实时看 CPU / 内存占用排行",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "top",
            "load",
            "CPU",
            "内存"
        ],
        "choices": [],
        "source_section": "命令特训 · 进程与作业",
        "statement_md": "线上机器变慢，要**实时**看哪个进程在吃 CPU。\n\n写出这条命令（交互式监控）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "top",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|top\n|htop\n|top -o %CPU\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`top`。\n\n`top` 的分区与关键列：\n- 顶部 `load average`：1/5/15 分钟的平均负载。**与核数一起看** —— 4 核机器 load 4.0 就是满载\n- `%Cpu(s)` 一行：`us` 用户态、`sy` 内核态、`wa` **I/O 等待**、`id` 空闲。**`wa` 高说明瓶颈在磁盘不在 CPU**\n- `MiB Mem`：`free`/`buff/cache`/`available`。★ 别只看 `free` 就说「内存不够」—— Linux 会主动用空闲内存做缓存，**该看 `available`**\n\n★ 常用交互键：`P` 按 CPU 排、`M` 按内存排、`k` 杀进程、`r` renice、`1` 展开每个核、`q` 退出。\n\n★ **迁移**：`top -b -n 1` 是**批处理模式**（输出一次就退出），最适合塞进脚本或日志；`htop` 更好看但要另装。"
            }
        ]
    },
    {
        "title": "看一个进程打开的文件和网络连接",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 4,
        "total_score": 18,
        "tags": [
            "lsof",
            "/proc",
            "文件描述符"
        ],
        "choices": [],
        "source_section": "命令特训 · 进程与作业",
        "statement_md": "某个进程占着文件删不掉，你要看它到底打开了什么。\n\n写出这条命令（指定 PID 1234）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "lsof -p 1234",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|lsof -p 1234\n|ls -l /proc/1234/fd\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`lsof -p 1234`。\n\n`lsof`（list open files）列出进程打开的所有文件描述符 —— 既包括普通文件，也包括**网络套接字、管道、设备**（Linux 里「一切皆文件」）。\n\n★ 最经典的用途：**删了文件但磁盘没释放**。`lsof | grep deleted` 能找出「已被删但仍有进程持有句柄」的文件，空间要等进程关句柄（或重启）才真正释放。\n\n★ 另一条路 `ls -l /proc/1234/fd` 不用装任何工具：`/proc/<pid>/fd/` 下每个符号链接就是一个打开的 fd，链接目标就是文件或 `socket:[inode]`。\n\n★ 只差「谁占着 80 端口」：`lsof -i :80` 或 `ss -ltnp | grep :80`。\n\n★ **迁移**：`lsof +D /path` 列出某目录下被打开的所有文件；`fuser -v /mnt` 看谁在用某个挂载点（卸载失败时必查）。"
            }
        ]
    },
    {
        "title": "看进程树（谁是谁的父进程）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "pstree",
            "父子进程",
            "PPID"
        ],
        "choices": [],
        "source_section": "命令特训 · 进程与作业",
        "statement_md": "要搞清楚 20 个 worker 是谁拉起来的。\n\n写出这条命令（树状显示）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "pstree -p",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|pstree -p\n|ps -ejH\n|ps axjf\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`pstree -p`。\n\n`pstree` 用缩进表达**父子关系**，`-p` 顺带标出每个进程的 PID。看「一个服务起了多少子进程」比 `ps` 直观得多。\n\n★ 重点看**父进程（PPID）**：如果 worker 的父进程是 `1`（systemd），说明它是被 systemd 直接拉起的（或者是孤儿被 init 收养）；如果是某个 `bash`，说明是人工启动的。\n\n★ `pstree -u` 标出**切换过用户的**进程（比如 root 启动后 setuid 成 nobody），排查权限问题时很有用。\n\n★ `ps -ejH` 是 POSIX 风格的树（不依赖 pstree 包）；`ps axjf` 带更多列。\n\n★ **迁移**：`pstree -p 1234` 只看某个进程的子树；`ps -o pid,ppid,cmd --ppid 1234` 列出某进程的所有直接子进程。"
            }
        ]
    },
    {
        "title": "查谁在监听某个端口",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "ss",
            "-ltnp",
            "端口",
            "netstat"
        ],
        "choices": [],
        "source_section": "命令特训 · 进程与作业",
        "statement_md": "部署时报 `Address already in use`，要知道**哪个进程占了 8080**。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ss -ltnp | grep :8080",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ss -ltnp | grep :8080\n|ss -ltnp 'sport = :8080'\n|lsof -i :8080\n|netstat -ltnp | grep :8080\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`ss -ltnp | grep :8080`。\n\n`ss` 的选项拆解：\n- `-l` 只看**监听**状态的套接字\n- `-t` TCP（`-u` 是 UDP）\n- `-n` 用**数字**显示端口（不解析成服务名，且更快）\n- `-p` 显示**进程**（需要 root 才能看到别人的进程）\n\n★ `netstat` 已被 `ss` 取代（net-tools 包在新系统里默认不装），**记住 `ss` 就够了**。\n\n★ 「占了端口」不一定是 `LISTEN`：也可能是已建立的连接。那时 `-ltnp` 看不到，得去掉 `-l`。\n\n★ **迁移**：`ss -s` 看套接字统计汇总；`ss -tnp state established` 看所有已建立的 TCP 连接（排查「连接数暴涨」时必用）。"
            }
        ]
    },
    {
        "title": "查一个进程的启动时间与运行时长",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 4,
        "total_score": 18,
        "tags": [
            "ps",
            "lstart",
            "etime",
            "运行时长"
        ],
        "choices": [],
        "source_section": "命令特训 · 进程与作业",
        "statement_md": "要确认服务是不是刚重启过。\n\n写出这条命令（指定 PID 1234）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ps -o pid,lstart,etime,cmd -p 1234",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ps -o pid,lstart,etime,cmd -p 1234\n|ps -p 1234 -o lstart,etime\n|ps -o pid,etime,lstart -p 1234\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`ps -o pid,lstart,etime,cmd -p 1234`。\n\n- `lstart` 精确到秒的**启动时刻**（`Sat Oct 19 08:12:33 2026`）\n- `etime` **已运行时长**（`2-03:15:42` = 2 天 3 小时…）\n\n★ `etime` 的格式是 `[[DD-]hh:]mm:ss`，机器解析起来麻烦；要算精确秒数用 `ps -o etimes=`（GNU 扩展，直接给秒）。\n\n★ `-o` 后面跟列名，可以自定义任意组合，这是 `ps` 最强大的地方（`ps -eo pid,ppid,user,%cpu,%mem,stat,etime,cmd`）。\n\n★ **迁移**：`systemctl show nginx -p ActiveEnterTimestamp` 看服务的启动时刻（比 ps 更适合 systemd 管理的服务）；`uptime -s` 看系统启动时间。"
            }
        ]
    },
    {
        "title": "在后台跑命令，并把错误输出也一起收进日志",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 4,
        "total_score": 18,
        "tags": [
            "重定向",
            "2>&1",
            "后台",
            "日志"
        ],
        "choices": [],
        "source_section": "命令特训 · 进程与作业",
        "statement_md": "要让 `deploy.sh` 后台跑，正常输出和错误输出**都**写进 `deploy.log`。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "nohup ./deploy.sh > deploy.log 2>&1 &",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|nohup ./deploy.sh > deploy.log 2>&1 &\n|./deploy.sh > deploy.log 2>&1 &\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`nohup ./deploy.sh > deploy.log 2>&1 &`。\n\n★ `2>&1` 是本题的核心，拆开看：\n- `2` 是 **stderr** 的文件描述符号，`1` 是 **stdout**\n- `>&` 是「把 fd 复制/重定向到另一个 fd」\n- 所以 `2>&1` = 「让 stderr 也写进 stdout 当前指向的地方」\n\n★ **顺序绝对不能反**：`> log 2>&1` 正确，`2>&1 > log` 错误。后者是「先把 stderr 指向**终端**，再把 stdout 指向文件」——结果错误信息仍然打在屏幕上，日志里只有正常输出。这是 shell 重定向最经典的一脚。\n\n★ `&` 与 `2>&1` 的先后：`&` 只是「放后台」，位置在整条命令最后，不影响重定向。\n\n★ **迁移**：想**丢弃**输出用 `> /dev/null 2>&1`；想分开存用 `> out.log 2> err.log`（注意这里写 `2>` 不是 `2>&`）。"
            }
        ]
    },
    {
        "title": "监控一个进程什么时候退出（并在退出时报警）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 4,
        "total_score": 18,
        "tags": [
            "kill -0",
            "轮询",
            "tail --pid"
        ],
        "choices": [],
        "source_section": "命令特训 · 进程与作业",
        "statement_md": "等一个编译任务跑完，但不想守着 —— 要写「**等这个 PID 退出后**打印一句话」的一行命令。\n\n写出这条命令（PID 用 1234 举例）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "while kill -0 1234 2>/dev/null; do sleep 1; done; echo done",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|while kill -0 1234 2>/dev/null; do sleep 1; done; echo done\n|tail --pid=1234 -f /dev/null\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`while kill -0 1234 2>/dev/null; do sleep 1; done; echo done`。\n\n★ `kill -0 PID` 是「**发 0 号信号**」—— 不真发信号，只做**存在性检查**：进程存在返回 0，不存在返回 1。这是 shell 里判断「进程还在不在」的标准做法。\n\n★ `2>/dev/null` 不能省：进程不存在时 `kill` 会往 stderr 喷 `No such process`，轮询几百次就刷屏了。\n\n★ 更省的写法：`tail --pid=1234 -f /dev/null` —— `tail` 会**阻塞**直到那个 PID 消失。纯 GNU 扩展，但一行顶一段循环，非常适合脚本。\n\n★ **迁移**：`wait 1234` 只能等**本 shell 的子进程**，对别人的进程无效 —— 这是很多人第一次踩的坑。"
            }
        ]
    },
    {
        "title": "看内存使用情况（要看真实可用内存）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "free",
            "-h",
            "内存",
            "available"
        ],
        "choices": [],
        "source_section": "命令特训 · 进程与作业",
        "statement_md": "同事说「内存只剩 200M 了要挂了」，你要用**人类可读单位**看真实情况。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "free -h",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|free -h\n|free --human\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`free -h`。\n\n★ 关键认知：**不要看 `free` 那一列**。Linux 会把空闲内存拿去做 `buff/cache`（页缓存），看起来「内存快用完了」，其实缓存随时可以被回收。\n\n★ **该看的是 `available` 列** —— 它是「在不触发 swap 的前提下还能给新进程用多少」，这才是真实余量。\n\n★ 各列含义：`total` 总量、`used` 已用、`free` 完全空闲、`shared` 共享内存、`buff/cache` 缓存、`available` 可用。\n\n★ `-h` 是人性化单位（`Gi`/`Mi`）；`-m` 固定按 MiB 显示（脚本里更好解析）。\n\n★ **迁移**：`free -s 2` 每 2 秒刷新一次；`vmstat 1` 看内存与 swap 活动的**变化趋势**，排查「内存泄漏」看的是趋势不是瞬时值。"
            }
        ]
    },
    {
        "title": "看各分区用了多少空间（人类可读）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "df",
            "-h",
            "磁盘"
        ],
        "choices": [],
        "source_section": "命令特训 · 磁盘与存储",
        "statement_md": "磁盘告警了，先确认是哪个分区满了。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "df -h",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|df -h\n|df -hT\n|df --human-readable\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`df -h`。\n\n`df`（disk free）按**挂载点**汇总，`-h` 人性化单位。\n\n★ `df -hT` 多一列**文件系统类型**（`xfs`/`ext4`/`btrfs`/`tmpfs`）—— 排查时很有用：`tmpfs` 满说明是**内存**被吃了，不是硬盘。\n\n★ `Use%` 到 100% 不一定是唯一问题：**`df -i` 看 inode 使用率** —— 「磁盘还有空间但写不进文件」几乎都是 inode 用光（海量小文件，如邮件队列、session 文件）。\n\n★ 注意 `df` 显示的是**文件系统**层面，删了文件但进程还持有句柄时，`df` 不会立刻下降。\n\n★ **迁移**：`df -h /var` 只看某个路径所在的分区，比在整张表里找快。"
            }
        ]
    },
    {
        "title": "看某个目录下每个子项占多少空间",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "du",
            "-sh",
            "sort",
            "空间"
        ],
        "choices": [],
        "source_section": "命令特训 · 磁盘与存储",
        "statement_md": "`/var` 快满了，要知道**是哪个子目录**吃的。\n\n要求：只统计**第一层**，按大小排序。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "du -sh /var/* | sort -rh",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|du -sh /var/* | sort -rh\n|du -sh /var/* | sort -hr\n|du -h --max-depth=1 /var | sort -rh\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`du -sh /var/* | sort -rh`。\n\n★ 三个组件：\n- `du -s`（summary）每个参数**只给总计**，不展开内部\n- `du -h` 人性化单位（注意：`-h` 与 `sort` 配合会有精度问题，见下）\n- `sort -rh` 按**人类可读单位**倒序（`-h` 让他认识 `1.2G`）\n\n★ `sort -h` 是 GNU 扩展，不认 `--human-readable` 的老系统上要换成 `sort -rn` + `du -k`（统一 KB）。\n\n★ **`du` 比 `df` 小是正常现象**：`du` 只统计「看到的文件」，而 `df` 算的是「文件系统已用块」——被删但句柄未释放的文件、被挂载覆盖的目录，`du` 都看不到。\n\n★ **迁移**：`du -ah /var | sort -rh | head -20` 直接找「最大的 20 个文件」，比逐层 `du -sh` 快得多；`du -sh /var/* 2>/dev/null` 加错误丢弃，避免权限报错刷屏。"
            }
        ]
    },
    {
        "title": "用一个命令看清所有块设备（含未挂载的）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "lsblk",
            "块设备",
            "磁盘"
        ],
        "choices": [],
        "source_section": "命令特训 · 磁盘与存储",
        "statement_md": "加了块新硬盘，要确认系统认到了没有、叫什么名字。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "lsblk",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|lsblk\n|lsblk -f\n|lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`lsblk`。\n\n`lsblk`（list block devices）用**树状结构**列出所有块设备，比 `fdisk -l` 清楚得多，而且**不需要 root**。\n\n★ `-f` 额外显示**文件系统**信息（FSTYPE、UUID、挂载点），挂载新盘前必看 —— 能直接拿到 `blkid` 里的 UUID。\n\n★ 关键列：`NAME` 设备名、`SIZE` 容量、`TYPE`（`disk`/`part`/`lvm`/`rom`）、`MOUNTPOINT`（空 = 没挂载）。\n\n★ `TYPE` 是 `disk` 但下面**没有 `part` 子项** → 这块盘还没分区；有 `part` 但 `MOUNTPOINT` 空 → 分了区没挂。两种情况处理完全不同。\n\n★ **迁移**：`lsblk -d -o name,size,rota` 只看整盘（`rota=1` 是机械盘、`0` 是 SSD）；`lsblk --json` 输出 JSON，适合脚本解析。"
            }
        ]
    },
    {
        "title": "挂载一个新分区到指定目录",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "mount",
            "挂载",
            "分区"
        ],
        "choices": [],
        "source_section": "命令特训 · 磁盘与存储",
        "statement_md": "`/dev/sdb1` 已经格式化好了（ext4），要挂到 `/data`。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "mount /dev/sdb1 /data",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|mount /dev/sdb1 /data\n|mount -t ext4 /dev/sdb1 /data\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`mount /dev/sdb1 /data`。\n\n`mount 设备 挂载点` —— 顺序是「**谁**挂到**哪**」。写反了会报 `special device /data does not exist`。\n\n★ `-t ext4` 通常可省：`mount` 会**自动探测**文件系统类型。但探测失败时（比如没装 `ext4` 模块）显式写 `-t` 更快定位问题。\n\n★ 挂载点**必须已存在**，而且最好是**空目录**。非空目录挂上去之后，原来里面的文件会被**遮住**（不是删除，是不再可见）——卸载后又能看到。这个特性曾让不少人以为「数据丢了」。\n\n★ 临时挂载重启后失效，要持久化必须写 `/etc/fstab`。\n\n★ **迁移**：`mount -o remount,rw /` 把根分区改回可写（救援时必用）；`findmnt /data` 看某个挂载点的详细信息（比 `mount | grep` 干净）。"
            }
        ]
    },
    {
        "title": "卸载一个分区",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "umount",
            "卸载",
            "busy"
        ],
        "choices": [],
        "source_section": "命令特训 · 磁盘与存储",
        "statement_md": "要把 `/data` 卸下来换硬盘。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "umount /data",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|umount /data\n|umount /dev/sdb1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`umount /data`（按**挂载点**）或 `umount /dev/sdb1`（按**设备**）。\n\n★ 命令名是 `umount`，**不是** `unmount` —— 少一个 `n`，这个拼写错误新手几乎都犯过。\n\n★ `target is busy` 是最常见的失败原因，含义是「有进程在用这个挂载点」。排查顺序：\n1. `lsof +D /data` 或 `fuser -vm /data` 找出是谁\n2. 自己的 shell 就在 `/data` 里 —— `cd` 出来\n3. 还有 NFS 客户端连着 / 有进程 cwd 在里面\n\n★ `umount -l`（lazy）会「先解除挂载、等没人用了再清理」，能强行成功但**可能造成数据不一致**，只在卡死时用。\n\n★ **迁移**：`umount -a` 卸载 `/etc/mtab` 里所有非根挂载点；卸载前 `sync` 一下，确保缓冲刷盘。"
            }
        ]
    },
    {
        "title": "把新硬盘分区并格式化成 ext4",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "mkfs",
            "ext4",
            "格式化"
        ],
        "choices": [],
        "source_section": "命令特训 · 磁盘与存储",
        "statement_md": "`/dev/sdb` 是块空盘，要建一个分区并格式化成 ext4。\n\n要求：写出**格式化**那一步（假设分区 `/dev/sdb1` 已建好）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "mkfs.ext4 /dev/sdb1",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|mkfs.ext4 /dev/sdb1\n|mkfs -t ext4 /dev/sdb1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`mkfs.ext4 /dev/sdb1`（或 `mkfs -t ext4 /dev/sdb1`）。\n\n★ **这是破坏性操作**：`mkfs` 会**抹掉**目标设备上所有数据，没有确认提示。动手前务必 `lsblk` 确认设备名 —— 把 `/dev/sda1`（系统盘）当 `/dev/sdb1` 敲下去，系统就没了。\n\n★ `mkfs.ext4` 是 `mkfs -t ext4` 的**简写软链**。文件系统具体参数（`-L` 卷标、`-b` 块大小、`-m` 保留百分比）用 `mkfs.ext4` 这种带类型的写法能直接传。\n\n★ 默认 ext4 会保留 **5%** 空间给 root 专用 —— 大容量数据盘上这 5% 很浪费，可以 `mkfs.ext4 -m 1 /dev/sdb1`。\n\n★ **迁移**：`mkfs.xfs /dev/sdb1`（RHEL 系默认）、`mkfs.btrfs`；格式化前想看原有签名：`wipefs -n /dev/sdb1`（`-n` 是 dry-run）。"
            }
        ]
    },
    {
        "title": "查看分区的 UUID（写 fstab 要用）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "blkid",
            "UUID",
            "fstab"
        ],
        "choices": [],
        "source_section": "命令特训 · 磁盘与存储",
        "statement_md": "要在 `/etc/fstab` 里写一条挂载，必须用 **UUID** 而不是设备名。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "blkid /dev/sdb1",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|blkid /dev/sdb1\n|blkid\n|lsblk -f\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`blkid /dev/sdb1`。\n\n输出形如 `UUID=\"a1b2c3d4-...\" TYPE=\"ext4\"`。\n\n★ **`fstab` 为什么必须用 UUID**：`/dev/sdb1` 这种名字是**内核枚举顺序**分配的，插拔硬盘、加装设备后可能变成 `/dev/sdc1`，结果就是**开机挂载失败甚至进不了系统**。UUID 写在文件系统里，跟设备名无关，永远指向同一个分区。\n\n★ 现代 systemd 还支持更可读的写法：`LABEL=名字`、`PARTUUID=`（GPT 分区表里的 UUID，格式化后不变）、`/dev/disk/by-uuid/...`。\n\n★ `blkid` 需要 root 才能读全部信息；普通用户可用 `lsblk -f`（不需要 root）。\n\n★ **迁移**：`findmnt --verify` 检查 fstab 语法 —— 改完 fstab **务必先验证再重启**，否则可能开不了机。"
            }
        ]
    },
    {
        "title": "看系统整体负载与运行时长",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "uptime",
            "load",
            "运行时长"
        ],
        "choices": [],
        "source_section": "命令特训 · 磁盘与存储",
        "statement_md": "要迅速判断机器「忙不忙、开了多久」。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "uptime",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|uptime\n|w\n|W\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`uptime`。\n\n输出形如 `08:12:33 up 3 days, 2:15, 2 users, load average: 0.52, 0.48, 0.41`。\n\n★ **load average 三个数** = 1 / 5 / 15 分钟的**平均活跃进程数**（运行中 + 不可中断睡眠）。\n\n★ 判断标准：**和 CPU 核数比**。4 核机器 load 4.0 ≈ 满载；load 8.0 = 严重超载（一堆进程在排队）。`nproc` 拿核数。\n\n★ 注意 load 包含 **D 状态（I/O 等待）**的进程 —— 所以「load 很高但 CPU 空闲」说明瓶颈在**磁盘**。这时看 `top` 的 `wa` 列或 `iostat -x 1`。\n\n★ **迁移**：`uptime -p` 输出人类语言（`up 3 days, 2 hours`）；`uptime -s` 给出**系统启动时刻**（判断是不是刚重启过）。"
            }
        ]
    },
    {
        "title": "检查某个路径是不是一个独立挂载点",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "findmnt",
            "mountpoint",
            "挂载点"
        ],
        "choices": [],
        "source_section": "命令特训 · 磁盘与存储",
        "statement_md": "`/data` 到底是一个独立分区，还是只是根分区上的一个普通目录？\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "findmnt /data",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|findmnt /data\n|mountpoint /data\n|df /data\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`findmnt /data`（最清楚）。\n\n★ 三种手段的差别：\n- `findmnt /data` 打印该挂载点的**全部信息**（源、类型、选项），是挂载就一定有输出\n- `mountpoint /data` 输出 `is a mountpoint` / `is not a mountpoint`，**退出码**可判断（脚本友好）\n- `df /data` 看它落在哪个文件系统上，**如果和 `/` 一样就说明没单独挂载**\n\n★ 为什么这件事重要：在根分区上存数据，系统盘一满整个系统都会出问题；而独立分区满只影响那一个目录。部署前确认「数据目录是不是独立挂载」是好习惯。\n\n★ **迁移**：`findmnt -R /data` 递归列出该挂载点下的**所有子挂载**，排查「嵌套挂载把目录遮住了」时必用。"
            }
        ]
    },
    {
        "title": "看磁盘 I/O 压力（哪个盘在忙）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 4,
        "total_score": 18,
        "tags": [
            "iostat",
            "%util",
            "IO",
            "sysstat"
        ],
        "choices": [],
        "source_section": "命令特训 · 磁盘与存储",
        "statement_md": "系统很卡但 CPU 不高，怀疑是磁盘 I/O 瓶颈。\n\n写出这条命令（每秒刷新，显示扩展统计）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "iostat -x 1",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|iostat -x 1\n|iostat -xz 1\n|iostat -dx 1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`iostat -x 1`。\n\n★ 关键列：\n- `%util` —— 设备**忙碌时间占比**。接近 100% 说明磁盘是瓶颈\n- `await` —— 平均**等待时间**（ms）。机械盘 > 20ms、SSD > 5ms 就该警惕\n- `r/s`、`w/s` —— 每秒读写次数（IOPS）\n- `rkB/s`、`wkB/s` —— 每秒吞吐\n\n★ `%util` 在**多队列 NVMe** 上会失真（可能显示 100% 但性能还好），那种场景更该看 `await` 和队列深度。\n\n★ `-z` 隐藏「零活动」的设备，输出干净很多；`-d` 只显示设备（不含 CPU 统计）。\n\n★ `iostat` 来自 **sysstat** 包，最小化安装常常没有（`dnf install sysstat`）。\n\n★ **迁移**：`pidstat -d 1` 看**哪个进程**在狂读写；`iotop`（需另装）按进程实时排序，直观但吃 CPU。"
            }
        ]
    },
    {
        "title": "找出被删除但仍占用空间的文件",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 4,
        "total_score": 18,
        "tags": [
            "lsof",
            "deleted",
            "空间未释放"
        ],
        "choices": [],
        "source_section": "命令特训 · 磁盘与存储",
        "statement_md": "`df` 显示用了 90%，但 `du` 加起来只有 40%。这是「文件删了但句柄没释放」。\n\n写出这条命令（找出这些文件）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "lsof | grep deleted",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|lsof | grep deleted\n|lsof +L1\n|lsof -n | grep deleted\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`lsof | grep deleted`（或 `lsof +L1`）。\n\n★ 现象解释：文件被 `rm` 后**目录项没了**，但如果还有进程持有它的**文件描述符**，inode 就**不会被回收**，磁盘块也不会释放。于是 `du` 看不到（目录里没有这个名字了），`df` 却还算着。\n\n★ 解决办法二选一：\n1. 重启那个进程\n2. **不重启**的话，用 `> /proc/<pid>/fd/<n>` 把它截断（这招能救急）\n\n★ `lsof +L1` 是「link count 小于 1」的简写，正好就是「已无目录项但仍被打开」的文件，比 `grep deleted` 精确。\n\n★ **迁移**：根本对策是**日志用截断而不是删除**——`truncate -s 0 app.log` 或 `: > app.log`。这也是 `logrotate` 的 `copytruncate` 选项存在的原因。"
            }
        ]
    },
    {
        "title": "看 inode 使用率（是否被小文件耗尽）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "df",
            "-i",
            "inode",
            "磁盘满"
        ],
        "choices": [],
        "source_section": "命令特训 · 磁盘与存储",
        "statement_md": "磁盘明明还有 20G，但 `touch` 新文件报 `No space left on device`。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "df -i",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|df -i\n|df -ih\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`df -i`。\n\n★ 每个文件（含目录、软链）都要占一个 **inode**。inode 总数在**格式化时定死**（ext4 默认约为每 16KB 一个）。inode 用完时，哪怕磁盘有空余也**创建不了任何新文件**，报错还是那句容易误导的 `No space left on device`。\n\n★ 典型场景：邮件队列堆积、session 文件、大量小日志（每个请求一个文件）、`node_modules` 这种海量小文件的目录。\n\n★ 排查：`df -i` 看 `IUse%`；找是哪个目录：`for d in /var/*; do echo \"$(find $d | wc -l) $d\"; done | sort -rn | head`\n\n★ **迁移**：inode 用完了只能删文件或重新格式化（`mkfs -N` 指定更多 inode）。所以「设计时预留足够 inode」比事后补救重要。"
            }
        ]
    },
    {
        "title": "把目录打成 tar 包（只打包，不压缩）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "tar",
            "-cvf",
            "打包"
        ],
        "choices": [],
        "source_section": "命令特训 · 压缩与打包",
        "statement_md": "要备份 `/etc/nginx`，打成 `nginx.tar`（不压缩，方便以后追加）。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "tar -cvf nginx.tar /etc/nginx",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|tar -cvf nginx.tar /etc/nginx\n|tar cvf nginx.tar /etc/nginx\n|tar --create --verbose --file nginx.tar /etc/nginx\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`tar -cvf nginx.tar /etc/nginx`。\n\n`c`/`v`/`f` 三件事：创建、啰嗦、指定文件名。\n\n★ **`-f` 必须紧跟文件名**，这也是 `-cfv` 这种顺序危险的原因：`-f` 后面那个词一定会被当文件名，所以 `-cfv x.tar src` 里 `tar` 认为归档叫 `v`，`x.tar` 和 `src` 都成了要打包的路径 —— 结果多出一个叫 `v` 的文件。**选项里 `f` 永远放最后**。\n\n★ 用**绝对路径**打包时 GNU tar 会**自动去掉开头的 `/`**，所以包里是 `etc/nginx/...`，解压时相对当前目录展开。这是「解压完多了一层 `etc/`」的原因（不是 bug）。\n\n★ **迁移**：不想多那一层，打包前 `cd /etc && tar -cvf nginx.tar nginx`；或者用 `-C`：`tar -cvf nginx.tar -C /etc nginx`。"
            }
        ]
    },
    {
        "title": "打包并用 bzip2 压缩",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "tar",
            "-j",
            "bzip2",
            "压缩"
        ],
        "choices": [],
        "source_section": "命令特训 · 压缩与打包",
        "statement_md": "要打 `src.tar.bz2`，压缩算法用 **bzip2**（压得更小但更慢）。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "tar -cjvf src.tar.bz2 src/",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|tar -cjvf src.tar.bz2 src/\n|tar cjvf src.tar.bz2 src/\n|tar -cvjf src.tar.bz2 src/\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`tar -cjvf src.tar.bz2 src/`。\n\n★ **压缩算法的字母对照**（必背）：\n- `-z` → **gzip**（`.tar.gz`，最快最通用）\n- `-j` → **bzip2**（`.tar.bz2`，压缩比高，慢）\n- `-J` → **xz**（`.tar.xz`，压缩比最高，最慢）\n- `--zstd` → zstd（`.tar.zst`，快且比高，新系统首选）\n- **`-Z` 不是任何一种现代压缩** —— 它调 `compress`（老式 `.Z`）\n\n★ 大写 `J` 与小写 `j` 是两个不同算法，**大小写写错不会报错，但生成的是另一种格式**（后缀却还是你写的那个）—— 极难排查。\n\n★ **迁移**：不确定该用哪个，就 `-z`（gzip）；要给别人发又怕他解不开，也是 `-z`。zstd 是性能与压缩比的甜点，但老系统可能没装。"
            }
        ]
    },
    {
        "title": "只看压缩包里有什么，不解压",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "tar",
            "-t",
            "查看内容"
        ],
        "choices": [],
        "source_section": "命令特训 · 压缩与打包",
        "statement_md": "拿到一个 `backup.tar.gz`，解压前想知道里面到底是什么结构。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "tar -tzvf backup.tar.gz",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|tar -tzvf backup.tar.gz\n|tar tzvf backup.tar.gz\n|tar -tvf backup.tar.gz\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`tar -tzvf backup.tar.gz`。\n\n`t`（list）是「**列出内容但不解压**」—— 这是 tar 里最该先养成习惯的一个动作：**解压前先看一眼**。\n\n★ 为什么必须看：包里可能是绝对路径或带 `../` 的路径，解压时会覆盖系统文件（`tar` 的 **tar-slip / zip-slip** 漏洞）。看一眼结构就能发现异常。\n\n★ `-v` 让 `t` 输出长格式（权限、属主、大小、时间），不加 `-v` 只给文件名。\n\n★ 压缩算法**不用指定**：GNU tar 会自己识别（靠文件头魔数），所以 `-tzvf` 里的 `z` 其实可以省。\n\n★ **迁移**：`tar -tzvf x.tar.gz | head -30` 只看前 30 项；`tar -tzvf x.tar.gz | wc -l` 数总条目。"
            }
        ]
    },
    {
        "title": "从 tar.gz 里只解出某一个文件",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "tar",
            "-x",
            "部分解压"
        ],
        "choices": [],
        "source_section": "命令特训 · 压缩与打包",
        "statement_md": "`backup.tar.gz` 有几千个文件，你只要里面的 `etc/nginx/nginx.conf`。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "tar -xzvf backup.tar.gz etc/nginx/nginx.conf",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|tar -xzvf backup.tar.gz etc/nginx/nginx.conf\n|tar -xzvf backup.tar.gz etc/nginx/nginx.conf -C /tmp\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`tar -xzvf backup.tar.gz etc/nginx/nginx.conf`。\n\n★ 路径必须**和包内路径完全一致** —— 包里是 `etc/nginx/nginx.conf`，你写 `/etc/nginx/nginx.conf`（带开头斜杠）就匹配不上。所以先用 `-t` 看清楚。\n\n★ 支持**通配**（GNU tar）：`tar -xzvf x.tar.gz --wildcards '*.conf'`。注意不加 `--wildcards` 时 `*` 不生效。\n\n★ 解出来会**按包内路径建目录**（`./etc/nginx/`），想解到指定位置加 `-C /tmp`。\n\n★ **迁移**：只解一个目录：`tar -xzvf x.tar.gz path/to/dir/`；要「解压但排除某些文件」用 `--exclude='*.log'`（注意**`--exclude` 必须放在文件名之前**）。"
            }
        ]
    },
    {
        "title": "压缩单个文件（不打包成 tar）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "gzip",
            "-k",
            "压缩",
            "gunzip"
        ],
        "choices": [],
        "source_section": "命令特训 · 压缩与打包",
        "statement_md": "要压一个 `access.log`，产出 `access.log.gz`。\n\n要求：用最通用的 gzip，**保留原文件**。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "gzip -k access.log",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|gzip -k access.log\n|gzip -c access.log > access.log.gz\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`gzip -k access.log`（`-k` = keep，保留原文件）。\n\n★ **`gzip` 默认会删除原文件**！`gzip access.log` 之后只剩下 `access.log.gz`，原文件没了。这个行为让无数人第一次用时心里一凉。`-k` 就是为此存在的。\n\n★ `-c`（stdout）写法 `gzip -c f > f.gz` 也能保原文件，但多一步重定向，且**别写成 `gzip -c f > f`**（会把源文件截断）。\n\n★ 解压：`gzip -d f.gz` 或 `gunzip f.gz`。`zcat f.gz` 可以直接看内容不解压。\n\n★ **`gzip` 只能压单个文件**（压完就是 `f.gz`，不含文件名信息）——这就是为什么需要 tar：**tar 负责「打包成单文件」，gzip 负责「压这一个文件」**，两者分工明确。\n\n★ **迁移**：`gzip -9` 最高压缩（更慢）、`-1` 最快；`zless f.gz` 分页看；`zgrep pattern f.gz` 直接搜压缩包。"
            }
        ]
    },
    {
        "title": "解压一个 .gz 文件",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "gunzip",
            "解压",
            "gz"
        ],
        "choices": [],
        "source_section": "命令特训 · 压缩与打包",
        "statement_md": "手上有 `app.log.gz`，要还原成 `app.log`。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "gunzip app.log.gz",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|gunzip app.log.gz\n|gzip -d app.log.gz\n|gzip -dk app.log.gz\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`gunzip app.log.gz`（等价 `gzip -d`）。\n\n★ 解压后**压缩包会被删除**（与 `gzip` 压缩时删原文件对称）。要保留压缩包用 `-k`。\n\n★ `gunzip` 自动识别 `.gz`/`.Z`/`.tgz`，解 `.tgz` 得到 `.tar`（**不会**自动展开 tar）—— 要「一次解到底」用 `tar -xzf f.tgz`。\n\n★ **迁移**：`zcat f.gz | less` 只看不落地；`tar -xzf` 才是平时最常用的「压缩包解开」——`gunzip` 只在「这就是个单文件」时用。"
            }
        ]
    },
    {
        "title": "把一个目录做成 zip（要给 Windows 用户）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "zip",
            "-r",
            "跨平台"
        ],
        "choices": [],
        "source_section": "命令特训 · 压缩与打包",
        "statement_md": "要把 `report/` 目录打成 `report.zip`，对方是 Windows，希望解压后直接得到 `report/` 目录。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "zip -r report.zip report/",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|zip -r report.zip report/\n|zip -r report.zip report\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`zip -r report.zip report/`。\n\n★ `-r` 是**必须的**：不加就只压目录里的**空壳**（zip 会报 `name not matched` 或者只存个目录项）。\n\n★ 为什么用 zip 而不用 tar.gz：**Windows 原生支持 zip**，而 `.tar.gz` 得装 7-Zip / WinRAR。跨平台交付一律 zip。\n\n★ **中文文件名**：Linux 上 zip 默认用 UTF-8 存名字，老版 Windows 解压可能乱码。需要兼容就用 `zip -r -UN=UTF8`，或者干脆改用 `7z`。\n\n★ `-r` 会**保留相对路径**：`zip -r a.zip report/` 里是 `report/xxx`；想「解压后不要那层 report」，得 `cd report && zip -r ../a.zip .`。\n\n★ **迁移**：`unzip -l a.zip` 看内容；`unzip -d /tmp a.zip` 解到指定目录；`unzip -O GBK` 处理 Windows 传来的乱码包。"
            }
        ]
    },
    {
        "title": "解压 zip 到指定目录",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "unzip",
            "-d",
            "解压"
        ],
        "choices": [],
        "source_section": "命令特训 · 压缩与打包",
        "statement_md": "要把 `assets.zip` 解到 `/var/www/html/static`，**别散在当前位置**。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "unzip assets.zip -d /var/www/html/static",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|unzip assets.zip -d /var/www/html/static\n|unzip -d /var/www/html/static assets.zip\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`unzip assets.zip -d /var/www/html/static`。\n\n★ `-d`（directory）指定解压目标。与 `tar -C` 不同的是，**`-d` 放在前面或后面都行**（`unzip` 的参数解析比较宽松），但习惯上写在 zip 文件名之后。\n\n★ 目标目录**不存在时 `unzip` 会自动创建**（`tar -C` 不会）。这个差别在脚本里要留意。\n\n★ 解压时如果文件已存在，`unzip` 会**交互式询问**（`replace ...? [y]es, [n]o, [A]ll`）—— 脚本里必须加 `-o`（覆盖）或 `-n`（不覆盖），否则会**卡死在等输入**上。\n\n★ **迁移**：`unzip -l a.zip` 先看清单；`unzip -q` 安静模式（不刷文件名），CI 日志里很清爽。"
            }
        ]
    },
    {
        "title": "看一个压缩包是什么格式（后缀不可信）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "file",
            "魔数",
            "压缩格式"
        ],
        "choices": [],
        "source_section": "命令特训 · 压缩与打包",
        "statement_md": "拿到一个叫 `data.bin` 的文件，别人说它是压缩包，但不知道是哪种。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "file data.bin",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|file data.bin\n|file data.bin && tar -tf data.bin\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`file data.bin`。\n\n★ 后缀是**人看的**，`file` 看的是**文件头魔数**，所以能识别出「后缀写错了」的情况（`.tar.gz` 其实是 `.tar.bz2`）。\n\n★ 输出会明确写出算法：`gzip compressed data`、`bzip2 compressed data`、`XZ compressed data`、`Zstandard compressed data`、`Zip archive data`、`POSIX tar archive`。\n\n★ `tar` 本身**不需要知道压缩算法**：GNU tar 会自己探测，所以 `tar -xf data.bin` 通常能直接解开（`-x` 后面**不写** `z`/`j`/`J`）。\n\n★ **迁移**：`tar -xf`（不带压缩字母）是兼容性最好的写法，尤其在「别人给的包，不确定算法」的场景。反过来，自己打包时明确写算法更可读。"
            }
        ]
    },
    {
        "title": "把压缩包追加上一个新文件（不重新打包）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 4,
        "total_score": 18,
        "tags": [
            "tar",
            "-r",
            "追加"
        ],
        "choices": [],
        "source_section": "命令特训 · 压缩与打包",
        "statement_md": "已经打好的 `app.tar` 里少了一个文件，要**追加**进去，不要重新打一遍（里面有几十 G）。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "tar -rvf app.tar newfile.conf",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|tar -rvf app.tar newfile.conf\n|tar rf app.tar newfile.conf\n|tar --append --file=app.tar newfile.conf\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`tar -rvf app.tar newfile.conf`。\n\n`-r`（`--append`）在归档**末尾追加**条目，不重写前面的内容 —— 所以对超大包也很快。\n\n★ **前提：包不能是压缩过的**。`.tar.gz` 是**一条压缩流**，不可能在一个 gzip 流中间插入数据，所以 `-r` 对压缩包会直接报错。这是「为什么我特意打成 .tar 不压缩」的原因之一。\n\n★ 追加的条目会**覆盖同名的旧条目吗**？不会 —— tar 里会出现**两个同名条目**，解压时**后一个覆盖前一个**。所以「更新」场景下追加是可行的（解压结果是对的）。\n\n★ **迁移**：`-u`（`--update`）是「只追加比包里更新的文件」，做增量备份更合适；`-A`（`--concatenate`）能把两个 tar 包拼起来。"
            }
        ]
    },
    {
        "title": "把 tar 包压缩成最小体积（讲究压缩比）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 4,
        "total_score": 18,
        "tags": [
            "xz",
            "-9",
            "压缩比"
        ],
        "choices": [],
        "source_section": "命令特训 · 压缩与打包",
        "statement_md": "要把一个 2G 的归档发给别人，带宽有限，要**尽可能小**。\n\n要求：用压缩比最高的算法。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "xz -9 app.tar",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|xz -9 app.tar\n|tar -cJvf app.tar.xz app/\n|xz -9e app.tar\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`xz -9 app.tar`（产出 `app.tar.xz`）。\n\n★ **压缩比排序（大致）**：xz > bzip2 > zstd(高等级) > gzip。**速度排序反过来**。`-9` 是最高压缩等级。\n\n★ xz 的代价：**解压也要 CPU**，而且内存占用高。在低配机器上解一个 10G 的 xz 包可能要几分钟 —— 所以服务器上更常用 zstd。\n\n★ `-9e` 里的 `e` 是「极致模式」（更多 CPU 换更小体积），只建议压缩时用一次、解压端不需要。\n\n★ xz **默认删除原文件**（和 gzip 一样），要保留加 `-k`。\n\n★ **迁移**：`tar -cJvf` 一步打包+压缩；`xz -l app.tar.xz` 看压缩率；要「压得快又能解」选 `zstd -19`（比 xz 快一个数量级）。"
            }
        ]
    },
    {
        "title": "解压时跳过出错的文件继续解",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 4,
        "total_score": 18,
        "tags": [
            "unzip",
            "-o",
            "损坏",
            "容错"
        ],
        "choices": [],
        "source_section": "命令特训 · 压缩与打包",
        "statement_md": "一个大 zip 里有个文件损坏了，`unzip` 到一半就退出。你要**跳过坏文件把所有能解的解开**。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "unzip -o assets.zip -x broken.txt",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|unzip -o assets.zip -x broken.txt\n|unzip -n assets.zip\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`unzip -o assets.zip`（`-o` 覆盖不提问，遇错继续），或 `unzip -x` 显式排除坏文件。\n\n★ `unzip` 的几种「不提问」选项要分清：\n- `-o` 覆盖已有文件，**不问**\n- `-n` 不覆盖已有文件（已存在的跳过）\n- `-q` 安静模式（只影响输出，不影响提问）\n\n★ 遇到**损坏条目**时 `unzip` 会报 `bad CRC` 并返回非 0 退出码，但前面已经解出的文件**是好的**。所以脚本里可以 `unzip ... || true`，再检查关键文件在不在。\n\n★ **迁移**：`unzip -t a.zip` 先**测试完整性**（只校验不解压），知道有几个坏条目再决定策略；`-x` 后面跟通配符可以排除一整类文件：`unzip a.zip -x '*.log'`。"
            }
        ]
    },
    {
        "title": "看本机的 IP 地址",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "ip",
            "addr",
            "IP",
            "ifconfig"
        ],
        "choices": [],
        "source_section": "命令特训 · 网络与远程",
        "statement_md": "要知道这台机器的 IP（给别人连过来用）。\n\n要求：用现代工具（不要 `ifconfig`）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ip addr",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ip addr\n|ip a\n|ip addr show\n|ip -brief addr\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`ip addr`（可简写 `ip a`）。\n\n★ `ifconfig` **已经被淘汰**：net-tools 包在新版 Fedora 默认不装，`netstat`/`route`/`ifconfig` 都不在。教材上那些命令能「想起来」就行，实操一律用 `ip`。\n\n★ 一个网卡可能有多行 `inet`：**一个 IPv4、一个 IPv6**。回给别人时别贴错了。\n\n★ `-brief`（`-br`）输出极简表格，`ip -br a` 是目前最快的「我 IP 是多少」。\n\n★ **迁移**：`ip -4 addr show dev eth0` 只看某网卡的 IPv4；`hostname -I` 一行输出所有 IPv4（**注意大写 I**，小写 `-i` 是解析主机名的 IP，结果可能不同）。"
            }
        ]
    },
    {
        "title": "看路由表（默认网关是谁）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "ip",
            "route",
            "网关"
        ],
        "choices": [],
        "source_section": "命令特训 · 网络与远程",
        "statement_md": "机器上不了外网，要先确认默认网关对不对。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ip route",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ip route\n|ip r\n|ip route show\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`ip route`（简写 `ip r`）。\n\n★ 找 `default via <网关IP> dev <网卡>` 那一行 —— 它就是默认路由。没有这一行 = **没有默认网关**，内网能通、外网不通，症状是「能 ping 通 192.168.x.x 但 ping 不通 8.8.8.8」。\n\n★ 各列含义：`default` 目标、`via` 下一跳、`dev` 出接口、`proto` 来源（`dhcp`/`static`/`kernel`）、`metric` 优先级（**小的优先**）。\n\n★ 也有 `169.254.x.x` 这种地址时要注意：那是 **link-local 自配地址**，说明 DHCP 拿不到地址，网络其实是有问题的。\n\n★ **迁移**：`ip route get 8.8.8.8` 直接问「去这个地址会走哪条路」，排查策略路由时最准；`ip -6 route` 看 IPv6 路由。"
            }
        ]
    },
    {
        "title": "测试到某台主机的连通性（只 ping 4 次）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "ping",
            "-c",
            "连通性"
        ],
        "choices": [],
        "source_section": "命令特训 · 网络与远程",
        "statement_md": "`ping` 默认会一直跑，脚本里要**发 4 个包就停**。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ping -c 4 8.8.8.8",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ping -c 4 8.8.8.8\n|ping -c4 8.8.8.8\n|ping -c 4 www.example.com\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`ping -c 4 8.8.8.8`。\n\n`-c`（count）指定发包数，不写就**永远跑下去**（`Ctrl+C` 停）。\n\n★ **`ping` 通不代表服务通**：ping 只测 ICMP，而防火墙常常只放行特定 TCP 端口。判断「服务是否可用」必须测端口（`curl` 或 `ss`）。\n\n★ **`ping` 不通也不代表主机不通**：很多云主机默认**屏蔽 ICMP**。所以 ping 失败时下一步是测端口，而不是直接判定「机器挂了」。\n\n★ 看 `packet loss` 与 `time`：丢包率与延迟才是价值所在，「通了」这个结论本身信息量很小。\n\n★ **迁移**：`ping -c 4 -i 0.2 host` 加快间隔；`ping -s 1400 host` 测 MTU 分片问题。"
            }
        ]
    },
    {
        "title": "测某个端口通不通（不是 ping 主机）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "nc",
            "端口",
            "/dev/tcp",
            "连通性"
        ],
        "choices": [],
        "source_section": "命令特训 · 网络与远程",
        "statement_md": "对方说服务启动了，但你要确认 **TCP 8080 端口**真的能连上。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "curl -v telnet://10.0.0.5:8080",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|curl -v telnet://10.0.0.5:8080\n|nc -zv 10.0.0.5 8080\n|ss -tn 10.0.0.5:8080\n|timeout 3 bash -c '</dev/tcp/10.0.0.5/8080'\n|timeout 3 bash -c </dev/tcp/10.0.0.5/8080\n|timeout 3 bash -c \"</dev/tcp/10.0.0.5/8080\"\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`nc -zv 10.0.0.5 8080`。\n\n- `-z` 只扫描**不发数据**（zero-I/O）\n- `-v` 显示结果\n\n★ 输出 `succeeded` / `Connection refused` 直接给结论。`Connection refused` = 端口**没有监听**；`timed out` = 中间被**防火墙拦了**。两者含义完全不同。\n\n★ `nc` 来自 nmap-ncat 包，可能没装。**不需要装任何东西的写法**是 bash 的 `/dev/tcp` 伪设备：\n```bash\ntimeout 3 bash -c '</dev/tcp/10.0.0.5/8080' && echo open\n```\n\n★ **迁移**：`curl -v telnet://ip:port` 也是通用写法（curl 几乎处处都有）；`telnet` 命令在 Fedora 上默认不装，别依赖它。"
            }
        ]
    },
    {
        "title": "用 curl 只看 HTTP 响应头",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "curl",
            "-I",
            "HTTP",
            "状态码"
        ],
        "choices": [],
        "source_section": "命令特训 · 网络与远程",
        "statement_md": "要确认一个网址返回的状态码和 Content-Type，但**不想下载整个响应体**。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "curl -I https://example.com",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|curl -I https://example.com\n|curl --head https://example.com\n|curl -s -o /dev/null -w '%{http_code}' https://example.com\n|curl -s -o /dev/null -w %{http_code} https://example.com\n|curl -s -o /dev/null -w \"%{http_code}\" https://example.com\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`curl -I https://example.com`。\n\n`-I`（`--head`）发 **HEAD 请求**，只拿响应头。注意：有些服务器不支持 HEAD（返回 405），那就得用 `-D -` 配合 `GET`。\n\n★ 状态码速查：`200` 正常、`301/302` 跳转、`403` 无权限、`404` 不存在、`500` 服务端错、`502` 网关后面的服务挂了、`504` 网关超时。\n\n★ 只想要状态码数字（写监控脚本）：`curl -s -o /dev/null -w '%{http_code}' URL` —— `-s` 静默、`-o /dev/null` 丢弃正文、`-w` 打印指定变量。这是最好用的一条。\n\n★ **迁移**：`curl -L` 跟随跳转（否则 301 就停了）；`curl -k` 忽略证书错误（自签证书测试时用，生产别用）；`curl -m 5` 设超时，避免脚本卡死。"
            }
        ]
    },
    {
        "title": "下载一个文件并保存成指定名字",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "wget",
            "curl",
            "-O",
            "下载"
        ],
        "choices": [],
        "source_section": "命令特训 · 网络与远程",
        "statement_md": "要下载 `https://example.com/data.tar.gz` 并**直接存成 `data.tgz`**。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "wget -O data.tgz https://example.com/data.tar.gz",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|wget -O data.tgz https://example.com/data.tar.gz\n|curl -o data.tgz https://example.com/data.tar.gz\n|curl -L -o data.tgz https://example.com/data.tar.gz\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`wget -O data.tgz https://example.com/data.tar.gz`。\n\n★ **`wget` 的 `-O` 是大写**，指定**输出文件名**；小写 `-o` 是「把**日志**写到哪个文件」。大小写搞反会出现「下载的文件变成了一堆日志」的经典事故。\n\n★ **`curl` 的 `-o` 是小写**（`--output`）指定输出文件名，`-O` 大写是「用 URL 里的文件名」。curl 与 wget 的大小写含义**正好相反** —— 这是最容易记混的一对。\n\n★ `curl` 必须加 `-L` 才跟随 301/302 跳转，`wget` **默认就跟随**。\n\n★ **迁移**：`wget -c` 断点续传；`wget -q --show-progress` 有进度条但不刷屏；`curl -C -` 是 curl 的断点续传。"
            }
        ]
    },
    {
        "title": "远程登录一台服务器（指定用户名和端口）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "ssh",
            "-p",
            "远程登录"
        ],
        "choices": [],
        "source_section": "命令特训 · 网络与远程",
        "statement_md": "要登录 `10.0.0.5`，用户名 `deploy`，SSH 端口是 **2222**（不是 22）。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ssh -p 2222 deploy@10.0.0.5",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ssh -p 2222 deploy@10.0.0.5\n|ssh -p2222 deploy@10.0.0.5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`ssh -p 2222 deploy@10.0.0.5`。\n\n★ **`ssh` 的端口选项是小写 `-p`**，而 `scp` 和 `sftp` 是**大写 `-P`**。这个不对称是 SSH 工具链里最著名的一处不一致 —— `scp -p` 的含义是「保留时间戳」，完全另一件事。\n\n★ 用户名的两种写法：`ssh deploy@host` 或 `ssh -l deploy host`。长期用建议写 `~/.ssh/config`：\n```\nHost prod\n    HostName 10.0.0.5\n    User deploy\n    Port 2222\n```\n之后 `ssh prod` 一条搞定。\n\n★ **迁移**：`ssh -v` 打印握手细节（排查认证失败必用）；`ssh-keygen -R host` 清掉变了的主机指纹（重装系统后必踩）。"
            }
        ]
    },
    {
        "title": "免密登录：把自己的公钥传到对方机器",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "ssh-copy-id",
            "免密",
            "公钥"
        ],
        "choices": [],
        "source_section": "命令特训 · 网络与远程",
        "statement_md": "每次 ssh 都要输密码太麻烦，要把本机公钥装到 `deploy@10.0.0.5`。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ssh-copy-id deploy@10.0.0.5",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ssh-copy-id deploy@10.0.0.5\n|ssh-copy-id -p 2222 deploy@10.0.0.5\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`ssh-copy-id deploy@10.0.0.5`。\n\n它做的事：把 `~/.ssh/id_*.pub` 追加到对方 `~/.ssh/authorized_keys`，并**顺手设好目录权限**（`700` / `600`）。\n\n★ **权限是免密登录失败的第一原因**：`~/.ssh` 必须是 `700`、`authorized_keys` 必须是 `600`、家目录**不能对 group/other 可写**。sshd 会**静默忽略**权限过松的密钥文件 —— 日志里只有一句 `Authentication refused: bad ownership`，不仔细看会以为密钥没传对。\n\n★ 没装 `ssh-copy-id` 时的等价手工操作：\n`cat ~/.ssh/id_ed25519.pub | ssh user@host 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys'`\n\n★ **迁移**：`ssh-keygen -t ed25519 -C 'me@laptop'` 生成密钥；`-p 2222` 指定端口（注意这里也是小写 `-p`，和 `ssh` 一致）。"
            }
        ]
    },
    {
        "title": "把本地文件传到远程服务器",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "scp",
            "-P",
            "传输",
            "rsync"
        ],
        "choices": [],
        "source_section": "命令特训 · 网络与远程",
        "statement_md": "要把 `deploy.sh` 传到 `10.0.0.5` 的 `/home/deploy/` 下，端口 2222。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "scp -P 2222 deploy.sh deploy@10.0.0.5:/home/deploy/",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|scp -P 2222 deploy.sh deploy@10.0.0.5:/home/deploy/\n|scp -P2222 deploy.sh deploy@10.0.0.5:/home/deploy/\n|rsync -av -e 'ssh -p 2222' deploy.sh deploy@10.0.0.5:/home/deploy/\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`scp -P 2222 deploy.sh deploy@10.0.0.5:/home/deploy/`。\n\n★ **`scp` 的端口是**大写 **`-P`**（与 `ssh -p` 相反，见上题）。\n\n★ 路径末尾的 `/` 有讲究：目标写 `/home/deploy/`（带斜杠）表示「放进这个目录」；写 `/home/deploy` 而它是个目录时结果一样；但如果目标是**文件名**，就变成改名复制。\n\n★ **`scp` 已不推荐用于大批量传输**：它基于老式协议，大文件速度上不去、不支持断点续传、不能增量。**`rsync -av` 是现代替代**（走 SSH，只传差异）。\n\n★ **迁移**：`scp -r dir/ user@host:/path` 传目录；`rsync -avz --progress src/ user@host:/dst/` （**注意 `src/` 带斜杠 = 传内容，不带 = 传目录本身**，这个斜杠是 rsync 的头号坑）。"
            }
        ]
    },
    {
        "title": "同步本地目录到远程（只传改过的）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 4,
        "total_score": 18,
        "tags": [
            "rsync",
            "-avz",
            "同步",
            "增量"
        ],
        "choices": [],
        "source_section": "命令特训 · 网络与远程",
        "statement_md": "要把 `./site` 同步到服务器的 `/var/www`，**只传有变化的文件**，并显示进度。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "rsync -avz --progress site/ deploy@10.0.0.5:/var/www/",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|rsync -avz --progress site/ deploy@10.0.0.5:/var/www/\n|rsync -av --progress site/ deploy@10.0.0.5:/var/www/\n|rsync -avz site/ deploy@10.0.0.5:/var/www/\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`rsync -avz --progress site/ deploy@10.0.0.5:/var/www/`。\n\n选项拆解：\n- `-a`（archive）= `-rlptgoD`，保权限/时间/软链/属主，最常用\n- `-v` 详细输出、`-z` 传输时压缩（跨网络才划算）\n- `--progress` 显示每个文件的进度\n\n★ **`site/` 与 `site` 的区别是 rsync 的头号坑**：\n- `rsync -a site/ host:/var/www/` → 得到 `/var/www/xxx`（**传内容**）\n- `rsync -a site host:/var/www/` → 得到 `/var/www/site/xxx`（**传目录本身**）\n记法：**源路径带斜杠 = 只要里面的东西**。\n\n★ 默认**不删除**目标里多出来的文件，要镜像同步必须加 `--delete`（危险，先 `-n` dry-run 看一遍）。\n\n★ **迁移**：`rsync -avn` 是**演练**（`-n` = dry-run），真正执行前必做；`--exclude='.git'` 排除目录。"
            }
        ]
    },
    {
        "title": "看主机名（临时改名，不重启）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "hostnamectl",
            "主机名",
            "systemd"
        ],
        "choices": [],
        "source_section": "命令特训 · 网络与远程",
        "statement_md": "要给机器设个新主机名 `web01`，**立刻生效**（不用重启）。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "hostnamectl set-hostname web01",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|hostnamectl set-hostname web01\n|hostnamectl set-hostname web01 --static\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`hostnamectl set-hostname web01`。\n\n★ 它是 systemd 提供的工具，会同时更新**运行中的主机名**和 `/etc/hostname` 文件，所以**立刻生效且重启后保持**。\n\n★ 老写法 `hostname web01` 只改**运行时**的值，重启就回去了 —— 这是「我明明改了名字，重开又变回去」的原因。\n\n★ 与 `hosts` 文件的关系：`hostnamectl` **不碰** `/etc/hosts`。如果本机服务依赖「主机名能解析到自己」，还得手动在 `/etc/hosts` 加一行 `127.0.1.1 web01`（否则 `sudo` 可能变慢、某些服务启动时解析失败）。\n\n★ **迁移**：`hostnamectl` 不带参数就是**查看**（系统版本、内核、架构、主机名一次看全）。"
            }
        ]
    },
    {
        "title": "看当前系统的网络设备列表与状态",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "ip",
            "link",
            "网卡"
        ],
        "choices": [],
        "source_section": "命令特训 · 网络与远程",
        "statement_md": "要确认网卡是不是**起来了**（UP/DOWN）。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ip link",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ip link\n|ip link show\n|ip -br link\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`ip link`（`ip -br link` 更简洁）。\n\n★ 输出里每个网卡的第一行末尾有状态标记：\n- `UP` —— 网卡已启用\n- `NO-CARRIER` —— **没插网线 / 没连上对端**\n- `DOWN` —— 被管理员 `ip link set down` 关了\n- `LOWER_UP` —— 物理链路真的通着\n\n★ `ip link` 是**链路层**（MAC、状态），`ip addr` 是**网络层**（IP 地址）。「网卡起来了但没 IP」和「网卡根本没起来」是两种完全不同的故障。\n\n★ **迁移**：`ip link set eth0 up` 启用网卡；`ip -s link` 看收发统计（有没有丢包）；`ethtool eth0` 看速率/双工（`Speed: 1000Mb/s`）。"
            }
        ]
    },
    {
        "title": "在远程机器上执行一条命令（不登录）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "ssh",
            "远程执行",
            "引号"
        ],
        "choices": [],
        "source_section": "命令特训 · 网络与远程",
        "statement_md": "要在 `10.0.0.5` 上跑 `df -h` 并把结果拿回来，**不进入交互 shell**。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ssh deploy@10.0.0.5 df -h",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ssh deploy@10.0.0.5 df -h\n|ssh deploy@10.0.0.5 'df -h'\n|ssh -p 2222 deploy@10.0.0.5 df -h\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`ssh deploy@10.0.0.5 df -h`。\n\n★ `ssh host 命令` 里，**命令之后的所有参数都会被原样传给远程 shell**，所以 `ssh host df -h` 等价于 `ssh host 'df -h'`。\n\n★ 但一旦有**重定向、管道、变量**就必须加引号：`ssh host 'ls | wc -l'` 里的 `|` 才会在**远程**执行；不加引号的话 `|` 会被**本地** shell 先解释，变成「把 ssh 的输出管道给本地的 wc」。这个坑极常见。\n\n★ ssh 不带 `-t` 时**没有 TTY**，所以 `sudo`、`top` 这类需要终端的命令会报错，要加 `-t`（分两次：`-t -t` 强制）。\n\n★ **迁移**：`ssh host 'cmd' > local.txt` 把远程结果存到本地；`for h in h1 h2 h3; do ssh $h uptime; done` 批量巡检。"
            }
        ]
    },
    {
        "title": "查本机的 DNS 配置与解析结果",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "DNS",
            "resolv.conf",
            "resolvectl"
        ],
        "choices": [],
        "source_section": "命令特训 · 网络与远程",
        "statement_md": "域名解析不对，要先确认用的是哪个 DNS 服务器。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "cat /etc/resolv.conf",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|cat /etc/resolv.conf\n|resolvectl status\n|systemd-resolve --status\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`cat /etc/resolv.conf`。\n\n★ 关键认知：**在现代 Fedora 上这个文件通常是「生成物」**，由 `systemd-resolved` 或 NetworkManager 写入，手工改会被下次网络变化覆盖。真正的配置在 `/etc/systemd/resolved.conf` 或 NetworkManager 的连接配置里。\n\n★ `resolvectl status` 是看**实际生效** DNS 的正确工具（含每个网卡分别用哪个 DNS、哪个域走哪个链路）。\n\n★ `nameserver 127.0.0.53` 是 `systemd-resolved` 的**本地存根**，不是真的 DNS 服务器 —— 看到它别以为配错了。\n\n★ **迁移**：验证解析：`getent hosts example.com`（走系统解析器，和程序行为一致）或 `dig example.com`（直接问 DNS，绕过 `/etc/hosts`）。两者结果不同就说明是 hosts 文件在起作用。"
            }
        ]
    },
    {
        "title": "搜一个软件包（还没装）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "dnf",
            "search",
            "软件包"
        ],
        "choices": [],
        "source_section": "命令特训 · 软件包与服务",
        "statement_md": "要装 `htop`，先确认仓库里有没有这个包。\n\n写出这条命令（Fedora/dnf）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "dnf search htop",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|dnf search htop\n|dnf list htop\n|dnf info htop\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`dnf search htop`（`dnf info htop` 更精确）。\n\n★ 三者的侧重不同：\n- `dnf search` 搜**名称与描述**，可能给出一堆相关结果\n- `dnf info` 查**指定包**的版本、大小、简介、仓库 —— 最有用\n- `dnf list` 列**已安装 + 可安装**，`--installed` / `--available` 过滤\n\n★ `dnf` 是 Fedora 的包管理器（`yum` 是它的前身，现在 `yum` 是指向 `dnf` 的软链，敲哪个都一样）。\n\n★ **迁移**：`dnf provides '*/bin/htop'` 按**文件**反查包；`dnf search --all` 连描述里的关键词一起搜；`dnf repoquery -l htop` 看一个包会装哪些文件。"
            }
        ]
    },
    {
        "title": "安装一个软件包（自动确认）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "dnf",
            "install",
            "-y"
        ],
        "choices": [],
        "source_section": "命令特训 · 软件包与服务",
        "statement_md": "脚本里要装 `nginx`，**不能卡在 `Is this ok [y/N]` 上**。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "dnf install -y nginx",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|dnf install -y nginx\n|dnf -y install nginx\n|dnf install --assumeyes nginx\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`dnf install -y nginx`。\n\n★ `-y`（`--assumeyes`）**自动回答 yes**，这是所有自动化脚本的必备项 —— 不加就会挂在交互提示上，在 CI 里表现为「任务超时」。\n\n★ **`-y` 是有风险的**：它连「要卸载 200 个包」这种事也会答应。所以在生产机上，安装前先 `dnf install --assumeno nginx` 看一遍**它打算做什么**（`--assumeno` 会在最后一步拒绝，但会打印完整计划）。\n\n★ 更稳的做法：`dnf install -y --setopt=install_weak_deps=False nginx` 避免拉进来一堆推荐包。\n\n★ **迁移**：`dnf upgrade --refresh` 升级全部（`upgrade` 与 `update` 同义）；`dnf remove` 卸载；`dnf autoremove` 清孤儿依赖。"
            }
        ]
    },
    {
        "title": "查一个包装了哪些文件",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "rpm",
            "-ql",
            "文件清单"
        ],
        "choices": [],
        "source_section": "命令特训 · 软件包与服务",
        "statement_md": "要知道 `nginx` 到底把配置装到哪了。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "rpm -ql nginx",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|rpm -ql nginx\n|dnf repoquery -l nginx\n|rpm -q --list nginx\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`rpm -ql nginx`。\n\n`rpm -q`（query）+ `-l`（list）= 列出该包安装的**所有文件**。配置一般在 `/etc/nginx/`，二进制在 `/usr/sbin/nginx`，unit 文件在 `/usr/lib/systemd/system/nginx.service`。\n\n★ **`rpm -ql` 只能查已安装的包**。查「**还没装**的包会装哪些文件」要用 `dnf repoquery -l nginx` —— 这是两者最关键的差别。\n\n★ 反过来「这个文件属于哪个包」是 `rpm -qf <路径>`。\n\n★ **迁移**：`rpm -qpl x.rpm` 看一个 **.rpm 文件**的内容（安装前检查，避免装进来一堆东西）；`rpm -qc nginx` 只列**配置文件**，改配置前先看它更省事。"
            }
        ]
    },
    {
        "title": "启动一个服务并设为开机自启",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "systemctl",
            "enable",
            "--now",
            "自启"
        ],
        "choices": [],
        "source_section": "命令特训 · 软件包与服务",
        "statement_md": "装好 `nginx` 之后，要**现在启动**并且**开机自动起**。\n\n写出这条命令（一条搞定）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "systemctl enable --now nginx",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|systemctl enable --now nginx\n|systemctl enable nginx --now\n|systemctl enable --now nginx.service\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`systemctl enable --now nginx`。\n\n两个动作合成一条：\n- `enable` 建**开机自启**的软链（写进 target 的 wants 目录）\n- `--now` 顺手**立刻启动**\n\n★ 分开写是 `systemctl enable nginx && systemctl start nginx`。`--now` 的价值是「不会漏做一步」—— 「只 enable 没 start」是最常见的部署失误：当前这次开机里服务仍然是停的。\n\n★ **`enable` 不等于 `start`，`start` 也不等于 `enable`**，这是 systemd 最该记清楚的一对概念：\n- `start` 管**现在**\n- `enable` 管**以后**\n\n★ **迁移**：`systemctl disable --now nginx` 反之；`systemctl restart nginx` 重启（会中断连接）；`systemctl reload nginx` 只重载配置（不断连接，改配置后优先用它）。"
            }
        ]
    },
    {
        "title": "看一个服务的运行状态",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "systemctl",
            "status",
            "服务"
        ],
        "choices": [],
        "source_section": "命令特训 · 软件包与服务",
        "statement_md": "`nginx` 起不来，先看它现在什么状态。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "systemctl status nginx",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|systemctl status nginx\n|systemctl status nginx.service\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`systemctl status nginx`。\n\n输出要点：\n- `Active:` 那行是核心 —— `active (running)` 正常、`failed` 失败、`inactive (dead)` 没启动\n- `Loaded:` 是否 enabled\n- `Main PID` 主进程号\n- 最后几行日志（其实等于 `journalctl -u nginx -n 10`）\n\n★ **`status` 会截断日志**，真正排查要看 `journalctl -u nginx -xe`（`-e` 跳到末尾、`-x` 附带说明）。\n\n★ **迁移**：`systemctl status --failed` 列所有失败的服务；`systemctl is-active nginx` 只输出状态词（脚本用）；`systemctl is-enabled nginx` 查是否开机自启。"
            }
        ]
    },
    {
        "title": "查看某个服务的日志",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "journalctl",
            "-u",
            "日志"
        ],
        "choices": [],
        "source_section": "命令特训 · 软件包与服务",
        "statement_md": "`nginx` 报错，要看它的日志（不带分页、直接看最后 50 行）。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "journalctl -u nginx -n 50",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|journalctl -u nginx -n 50\n|journalctl -u nginx --no-pager -n 50\n|journalctl -u nginx -n 50 --no-pager\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`journalctl -u nginx -n 50`。\n\n- `-u` 按 **unit** 过滤（服务名）\n- `-n 50` 最后 50 行\n- `--no-pager` 不分页（脚本里必须加，否则会进 `less` 卡住）\n\n★ 其他高频选项：\n- `-f` 实时跟随（等于 `tail -f`）\n- `-e` 直接跳到末尾\n- `-b` 只看**本次开机**（排查「重启后好了但不知道为什么」，`-b -1` 看上一次开机）\n- `--since '10 min ago'` / `--since today` 按时间过滤\n- `-p err` 只看 error 及以上级别\n\n★ journal 是**二进制日志**，不能用 `grep` 直接读文件，但可以 `journalctl -u nginx | grep 关键字`。\n\n★ **迁移**：`journalctl -u nginx -p err -b --since '1 hour ago'` 是排查「刚才出了什么错」的最短路径。"
            }
        ]
    },
    {
        "title": "让改过的配置立即生效（不重启服务）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "systemctl",
            "reload",
            "nginx"
        ],
        "choices": [],
        "source_section": "命令特训 · 软件包与服务",
        "statement_md": "改完 `nginx.conf` 要让它生效，但**不想断开现有连接**。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "systemctl reload nginx",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|systemctl reload nginx\n|nginx -s reload\n|systemctl reload nginx.service\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`systemctl reload nginx`。\n\n`reload` 发的是 **SIGHUP**，语义由服务自己实现：nginx 会**开新 worker 接管流量、优雅关闭旧 worker**，已有连接不中断。\n\n★ **`restart` 与 `reload` 的区别是运维基本功**：\n- `restart` = stop + start，**所有连接立刻断开**\n- `reload` = 重读配置，连接保持\n\n★ **不是所有服务都支持 reload**：`systemctl reload` 前先确认 `systemctl show nginx -p CanReload` 返回 `CanReload=yes`，否则会报 `Job type reload is not applicable`。\n\n★ **改完配置先测语法**：`nginx -t`。配置有错时 `reload` 会失败但**旧进程还在跑**，看起来「没反应」，实际是配置压根没通过校验。\n\n★ **迁移**：`systemctl daemon-reload` 是**另一件事** —— 改了 `.service` 文件本身之后才需要它。"
            }
        ]
    },
    {
        "title": "查一个包装没装、装的是什么版本",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "rpm",
            "-q",
            "版本"
        ],
        "choices": [],
        "source_section": "命令特训 · 软件包与服务",
        "statement_md": "要确认 `nginx` 有没有装、装的是哪个版本。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "rpm -q nginx",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|rpm -q nginx\n|dnf list installed nginx\n|rpm -qi nginx\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`rpm -q nginx`。\n\n输出 `nginx-1.26.2-1.fc40.x86_64` 表示已装；输出 `package nginx is not installed` 表示没装。**注意：没装时退出码是 1**，脚本里要处理。\n\n★ `rpm -qi` 看**详细信息**（版本、安装日期、许可证、简介）；`dnf list installed nginx` 输出格式更友好且能识别仓库来源。\n\n★ **`rpm -q` 查不到但 `dnf` 说装了**的情况：可能装的是**模块流（module stream）**版本，或者来自第三方仓库。`dnf list --installed` 会标出来源。\n\n★ **迁移**：`rpm -qa | wc -l` 数装了多少包；`rpm -qa --last | head` 看**最近装了什么**（排查「今天开始出问题」时非常有用）。"
            }
        ]
    },
    {
        "title": "卸载一个软件包（连同不再需要的依赖）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "dnf",
            "remove",
            "autoremove"
        ],
        "choices": [],
        "source_section": "命令特训 · 软件包与服务",
        "statement_md": "要彻底清掉 `httpd` 及其孤儿依赖。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "dnf remove httpd",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|dnf remove httpd\n|dnf autoremove httpd\n|dnf remove -y httpd\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`dnf remove httpd`（清理孤儿依赖再补一条 `dnf autoremove`）。\n\n★ **`dnf remove` 默认会连带卸载「只被这个包依赖」的包** —— 所以它可能一次删掉比你预期更多的东西。动手前用 `dnf remove --assumeno httpd` 看完整计划。\n\n★ `autoremove` 单独使用时清的是「**已经没有任何包依赖它**的残留包」（通常来自历史卸载）。它不是「删除某个包并清理依赖」的专用工具。\n\n★ **配置文件**默认保留（改名为 `.rpmsave`）—— 重装后旧配置还在，有时会被吓一跳。\n\n★ **迁移**：`dnf history` 看操作历史，`dnf history undo <ID>` 撤销某次操作 —— 「刚才手滑删了一堆东西」的救命命令。"
            }
        ]
    },
    {
        "title": "列出所有已启用的软件仓库",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "dnf",
            "repolist",
            "仓库"
        ],
        "choices": [],
        "source_section": "命令特训 · 软件包与服务",
        "statement_md": "装不上某个包，怀疑是仓库没开或者被禁用了。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "dnf repolist",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|dnf repolist\n|dnf repolist --enabled\n|dnf repolist -v\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`dnf repolist`。\n\n默认只列**已启用**的仓库；`--all` 连禁用的也列出来。`-v` 显示每个仓库的 baseurl 与包数量。\n\n★ **启用/禁用**：`dnf config-manager --set-enabled <repo>` / `--set-disabled <repo>`（`config-manager` 需要 `dnf-plugins-core`）。\n\n★ 临时从某个仓库装：`dnf --enablerepo=updates install pkg`；临时排除：`dnf --disablerepo=* --enablerepo=fedora install pkg`。\n\n★ 排查套路：「包找不到」→ 先 `dnf repolist` 看仓库在不在、再 `dnf search`、再 `dnf provides`。很多时候是**仓库镜像还没同步**，换镜像或等一会儿。\n\n★ **迁移**：`dnf clean all` 清缓存（元数据损坏时必做）；`dnf makecache` 重建缓存。"
            }
        ]
    },
    {
        "title": "看系统启动时哪些服务失败了",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "systemctl",
            "--failed",
            "启动失败"
        ],
        "choices": [],
        "source_section": "命令特训 · 软件包与服务",
        "statement_md": "机器重启后某个服务没起来，但不知道是哪个。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "systemctl --failed",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|systemctl --failed\n|systemctl list-units --failed\n|systemctl list-units --state=failed\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`systemctl --failed`。\n\n它列出所有 **load 状态为 failed** 的 unit —— 开机自启失败、运行中崩溃的都会在这里。\n\n★ 输出为空 = 没有失败的服务（正常的机器就应该是空的）。\n\n★ 找到之后的标准流程：\n1. `systemctl status <name>` 看退出码与最后几条日志\n2. `journalctl -u <name> -xe` 看完整报错\n3. `systemctl reset-failed <name>` 清掉 failed 标记（改了配置后）\n\n★ **迁移**：`systemctl list-units --type=service --all` 看全部服务（含没启动的）；`systemd-analyze blame` 看**开机时谁最慢**（排查开机慢的第一条命令）。"
            }
        ]
    },
    {
        "title": "看一个 .rpm 文件里有什么（安装前检查）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 4,
        "total_score": 18,
        "tags": [
            "rpm",
            "-qpl",
            "-p",
            "rpm 文件"
        ],
        "choices": [],
        "source_section": "命令特训 · 软件包与服务",
        "statement_md": "别人给了一个 `custom.rpm`，装之前想知道它会往系统里放什么。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "rpm -qpl custom.rpm",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|rpm -qpl custom.rpm\n|rpm -qlp custom.rpm\n|rpm -qpi custom.rpm\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`rpm -qpl custom.rpm`。\n\n★ **`-p` 是关键**：它让 `rpm` 处理「**一个包文件**」而不是「已安装的包」。所以 `-qpl` = query + package file + list。\n\n★ 没有 `-p` 时 `rpm -ql custom.rpm` 会去查一个**名叫 `custom.rpm` 的已装包**，报 `package custom.rpm is not installed` —— 这个报错很有迷惑性，看起来像「文件不存在」，其实是用错了模式。\n\n★ `-qpi` 看包信息（版本、依赖、简介），`-qpR` 看**依赖要求**。\n\n★ **迁移**：装之前最该看的是 `-qpl` 里有没有奇怪路径（比如 `/etc/passwd` 这种覆盖系统文件），以及 `-qp --scripts` 里的安装前后脚本（`%post` 可能干任何事）。"
            }
        ]
    },
    {
        "title": "查看某个服务依赖哪些其他服务",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 4,
        "total_score": 18,
        "tags": [
            "systemctl",
            "依赖",
            "reverse"
        ],
        "choices": [],
        "source_section": "命令特训 · 软件包与服务",
        "statement_md": "要停一个服务，但怕影响到别人，先看**依赖关系**。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "systemctl list-dependencies nginx",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|systemctl list-dependencies nginx\n|systemctl list-dependencies --reverse nginx\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`systemctl list-dependencies nginx`。\n\n默认显示「**这个服务需要什么**」（依赖树，向下）；`--reverse` 显示「**谁需要这个服务**」（被依赖关系，向上）—— 后者才是「停掉它会影响谁」的答案。\n\n★ 停服务前真正该查的两件事：\n1. `systemctl list-dependencies --reverse nginx` 谁会受影响\n2. `ss -ltnp | grep nginx` 它占着什么端口\n\n★ 依赖类型也很重要：`Requires` 是强依赖（停这个，被依赖的也停）；`Wants` 是弱依赖（尽力而为，不阻塞）；`After`/`Before` 只是**启动顺序**，不构成依赖。\n\n★ **迁移**：`systemctl list-dependencies --all` 展开完整树；`systemctl show nginx -p Requires,Wants` 只看关键字段。"
            }
        ]
    },
    {
        "title": "清理 dnf 缓存与无用包",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "dnf",
            "clean",
            "缓存"
        ],
        "choices": [],
        "source_section": "命令特训 · 软件包与服务",
        "statement_md": "`/var/cache` 涨得厉害，要清掉包管理器缓存。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "dnf clean all",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|dnf clean all\n|dnf clean packages\n|dnf clean all && dnf autoremove -y\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`dnf clean all`。\n\n它会清掉：`packages`（下载的 rpm）、`metadata`（仓库元数据）、`dbcache`、`expire-cache`。**其中 metadata 占的空间常常比包本身还大**。\n\n★ 只清包不清元数据：`dnf clean packages`（下次装包不用重新拉元数据，更快）。\n\n★ 清完下次 `dnf` 操作会**重新下载元数据**，所以第一次会慢一点 —— 这是正常的，不是出问题。\n\n★ **`/var/cache/dnf` 是主要占用点**，另外 `/var/cache` 下还有 `PackageKit`、`fwupd` 等缓存。排查用 `du -sh /var/cache/*`。\n\n★ **迁移**：`dnf autoremove -y` 清孤儿包；`journalctl --vacuum-size=500M` 清 journal 日志（`/var/log/journal` 涨到几个 G 是常态）。"
            }
        ]
    },
    {
        "title": "把一条命令的输出存到文件（覆盖）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "重定向",
            ">",
            "覆盖"
        ],
        "choices": [],
        "source_section": "命令特训 · Shell 与管道",
        "statement_md": "要把 `ls -l` 的结果存进 `list.txt`（**覆盖**原内容）。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ls -l > list.txt",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ls -l > list.txt\n|ls -l 1> list.txt\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`ls -l > list.txt`。\n\n★ `>` 是**覆盖**（会先清空文件），`>>` 才是**追加**。搞混的后果是「文件里只剩最后一次的内容」。\n\n★ `>` 的执行顺序是：**先由 shell 打开并截断文件，再执行命令**。所以 `cmd > file` 里 `file` 在命令跑起来时就**已经空了**。这解释了两个经典事故：\n- `sort f > f` → 把 f 清空后排序空文件，结果 f 变空\n- 命令执行失败时，目标文件也已经被清空\n\n★ `1>` 是 `>` 的显式写法（fd 1 = stdout），日常直接写 `>`。\n\n★ **迁移**：不想覆盖已有文件：`set -o noclobber`（`>|` 可强制覆盖）；`tee` 能同时显示到屏幕并存文件。"
            }
        ]
    },
    {
        "title": "把错误输出丢弃，只留正常输出",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "重定向",
            "2>",
            "/dev/null"
        ],
        "choices": [],
        "source_section": "命令特训 · Shell 与管道",
        "statement_md": "跑一条命令，屏幕被 `Permission denied` 刷满了，你只想看**正常结果**。\n\n写出这条命令（以 `find / -name x` 为例）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "find / -name x 2>/dev/null",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|find / -name x 2>/dev/null\n|find / -name x 2> /dev/null\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`find / -name x 2>/dev/null`。\n\n★ `2` 是 **stderr** 的 fd 号，`/dev/null` 是「黑洞」设备（写进去就没了）。合起来 = 「把错误信息扔掉」。\n\n★ fd 速查：`0` stdin、`1` stdout、`2` stderr。所以 `2>` 是「重定向错误输出」，`1>` 是「重定向正常输出」。\n\n★ **`2>/dev/null` 与 `&>/dev/null` 的区别**：前者只丢错误、后者**全丢**。还有 `2>&1`（错误并入正常输出）—— 三个写法经常被混用，结果一个报错都没看到。\n\n★ **迁移**：调试时**不要**丢错误输出 —— 「命令没输出也没报错」是最难查的状态。宁可 `2>&1 | less` 看清楚。"
            }
        ]
    },
    {
        "title": "前一条命令成功才执行后一条",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "&&",
            "||",
            "退出码"
        ],
        "choices": [],
        "source_section": "命令特训 · Shell 与管道",
        "statement_md": "要在 `mkDIR` 成功之后才 `cd` 进去，失败就**不要**往下走。\n\n写出这条命令（以 `mkdir -p /tmp/x` 和 `cd /tmp/x` 为例）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "mkdir -p /tmp/x && cd /tmp/x",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|mkdir -p /tmp/x && cd /tmp/x\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`mkdir -p /tmp/x && cd /tmp/x`。\n\n★ shell 的三种连接符语义完全不同：\n- `&&` —— 前面**成功**（退出码 0）才执行\n- `||` —— 前面**失败**才执行\n- `;` —— **无条件**都执行\n\n★ 写成 `mkdir -p /tmp/x ; cd /tmp/x` 的后果：`mkdir` 失败时 `cd` 照样跑，于是你在错误的目录里继续操作，后面所有相对路径全错 —— 而且没有任何一处报错指向真正的原因。\n\n★ 退出码约定：**0 = 成功，非 0 = 失败**（与 C 的 `main` 返回一致）。`$?` 取上一条的退出码。\n\n★ **迁移**：`cmd1 && cmd2 || cmd3` 是「成功走 A、失败走 B」；但注意 `A && B || C` 里若 B 失败也会走 C（不是三元运算），要严格分支用 `if`。"
            }
        ]
    },
    {
        "title": "统计目录下文件个数",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "管道",
            "wc",
            "find",
            "计数"
        ],
        "choices": [],
        "source_section": "命令特训 · Shell 与管道",
        "statement_md": "要数当前目录下有多少个文件（**含子目录，不含目录本身**）。\n\n写出这条命令（管道 + 计数）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "find . -type f | wc -l",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|find . -type f | wc -l\n|ls -R | wc -l\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`find . -type f | wc -l`。\n\n★ 这是「**管道**」最典型的用法：`|` 把前一条命令的 **stdout** 接到后一条的 **stdin**。\n\n★ **`ls -R | wc -l` 是错的**（本题的坑）：`ls -R` 的输出里混着 `./subdir:` 这样的**目录标题行**和空行，数出来的数字比真实文件数多。「用 `ls` 数文件」几乎总是不准 —— 因为 `ls` 是给人看的。\n\n★ **`ls | wc -l` 也有坑**：文件名里有换行时会被算成两个；隐藏文件不在里面；目录也算进去了。\n\n★ **迁移**：只要当前层：`find . -maxdepth 1 -type f | wc -l`；要「真数字」用 `find ... -print0 | tr -cd '\\0' | wc -c`。"
            }
        ]
    },
    {
        "title": "在管道里同时看输出又存文件",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "tee",
            "管道",
            "2>&1",
            "日志"
        ],
        "choices": [],
        "source_section": "命令特训 · Shell 与管道",
        "statement_md": "想让命令的输出**既显示在屏幕上又存一份到文件**。\n\n写出这条命令（以 `make` 为例）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "make 2>&1 | tee build.log",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|make 2>&1 | tee build.log\n|make | tee build.log\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`make 2>&1 | tee build.log`。\n\n★ `tee` 像三通管：**stdin 同时流向 stdout 和文件**。\n`-a` 是追加（默认覆盖）。\n\n★ **为什么这里必须 `2>&1`**：`|` 只接 stdout，错误信息走 stderr，**不会进管道**。所以不加 `2>&1` 的话，屏幕上能看到报错、但 `build.log` 里一条错误都没有 —— 拿着日志去问人，人家看不出问题。\n\n★ 顺序：`2>&1` 必须在 `|` **之前**。写 `make | tee log 2>&1` 是把 `tee` 的 stderr 重定向，完全另一回事。\n\n★ **迁移**：`sudo cmd | tee /root/out.log` —— `sudo` 只作用于 `cmd`，重定向由**当前 shell**执行，所以往 root 目录写会失败。正确写法：`sudo sh -c 'cmd > /root/out.log'`。\n\n★ 同时写两个文件：`tee a.log b.log`。"
            }
        ]
    },
    {
        "title": "定义一个变量并在命令里使用",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "变量",
            "赋值",
            "引号"
        ],
        "choices": [],
        "source_section": "命令特训 · Shell 与管道",
        "statement_md": "要设 `DIR=/var/log` 然后用它做 `ls`。\n\n写出这两条命令（赋值 + 使用）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "DIR=/var/log && ls $DIR",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|DIR=/var/log && ls $DIR\n|DIR=/var/log; ls \"$DIR\"\n|DIR=/var/log; ls $DIR\n|DIR=/var/log; ls '$DIR'\n|DIR=/var/log ls $DIR\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`DIR=/var/log` 然后 `ls \"$DIR\"`。\n\n★ **`=` 两边不能有空格**！`DIR = /var/log` 会被解释成「执行一个叫 `DIR` 的命令，参数是 `=` 和 `/var/log`」，报 `DIR: command not found`。这是 shell 变量赋值的第一条铁律。\n\n★ 使用时要加 **`$`**，赋值时**不加**。`$DIR` 展开成值，`${DIR}` 是同一件事但边界更清楚（`${DIR}_log` 才不会把 `_log` 当成变量名的一部分）。\n\n★ **永远给变量加双引号**：`\"$DIR\"`。不加引号时值里有空格会被拆成多个参数，`ls $DIR` 遇到 `/my docs` 就变成 `ls /my docs`（两个参数）。\n\n★ **迁移**：`export DIR=...` 让子进程也能看到；`readonly DIR=...` 防误改；`unset DIR` 删除。"
            }
        ]
    },
    {
        "title": "给一条长命令起个别名",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "alias",
            "别名",
            "bashrc"
        ],
        "choices": [],
        "source_section": "命令特训 · Shell 与管道",
        "statement_md": "每次都要敲 `ls -alh --color=auto` 太累，要起个别名 `ll`。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "alias ll='ls -alh --color=auto'",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|alias ll='ls -alh --color=auto'\n|alias ll=\"ls -alh --color=auto\"\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`alias ll='ls -alh --color=auto'`。\n\n★ **单引号不能省**：不加引号时 `alias ll=ls -alh` 会被解析成「`alias ll=ls`」加「`-alh` 作为参数」，结果别名只等于 `ls`，而且 shell 会报 `-alh: command not found`。\n\n★ 别名只在**当前 shell 会话**有效。要持久化写进 `~/.bashrc`（交互式非登录 shell）或 `~/.bash_profile`（登录 shell）。**改完要 `source ~/.bashrc` 或重开终端**。\n\n★ 别名的局限：只做**文本替换**，不能带参数逻辑、不能用在脚本里（非交互 shell 默认不展开别名）。复杂需求用**函数**。\n\n★ **迁移**：`alias` 不带参数列出所有别名；`unalias ll` 删除；`\\ls` 或 `command ls` 可以**绕过别名**执行原始命令。"
            }
        ]
    },
    {
        "title": "把命令的输出作为另一个命令的参数",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 4,
        "total_score": 18,
        "tags": [
            "xargs",
            "-print0",
            "空格",
            "安全"
        ],
        "choices": [],
        "source_section": "命令特训 · Shell 与管道",
        "statement_md": "要把 `find` 找到的文件交给 `rm` 删除（**文件名可能有空格**）。\n\n写出这条安全写法。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "find . -name '*.tmp' -print0 | xargs -0 rm",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|find . -name '*.tmp' -print0 | xargs -0 rm\n|find . -name *.tmp -print0 | xargs -0 rm\n|find . -name \"*.tmp\" -print0 | xargs -0 rm\n|find . -name '*.tmp' -exec rm {} +\n|find . -name *.tmp -exec rm {} +\n|find . -name \"*.tmp\" -exec rm {} +\n|find . -name '*.tmp' -delete\n|find . -name *.tmp -delete\n|find . -name \"*.tmp\" -delete\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`find . -name '*.tmp' -print0 | xargs -0 rm`（或 `-exec rm {} +`）。\n\n★ **`-print0` + `-0` 这一对是核心**：`-print0` 用 **NUL 字节**分隔文件名（文件名里不可能有 NUL），`xargs -0` 按 NUL 切分。这样就**彻底免疫空格、换行、引号**。\n\n★ 普通写法 `find ... | xargs rm` 的后果：文件名 `my file.tmp` 会被切成 `my` 和 `file.tmp` 两个参数，于是 `rm my` —— **删错文件**。这是 Linux 上最经典的「一句话删库」事故。\n\n★ `-exec cmd {} +` 是另一种安全写法（直接传参，不经过文本），而且**性能更好**（攒批执行）。`-exec cmd {} \\;` 是逐个执行（慢但能用在中间位置）。\n\n★ **迁移**：`xargs -n 1 -0` 逐个执行；`xargs -p` 执行前确认；`xargs -I{}` 把 `{}` 放到命令中间：`xargs -0 -I{} mv {} /backup/`。"
            }
        ]
    },
    {
        "title": "在 shell 里做算术运算",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 2,
        "total_score": 12,
        "tags": [
            "算术",
            "$(())",
            "变量"
        ],
        "choices": [],
        "source_section": "命令特训 · Shell 与管道",
        "statement_md": "要让 `count` 加 1。\n\n写出这条命令（假设 `count=5`）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "count=$((count+1))",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|count=$((count+1))\n|((count++))\n|let count=count+1\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`count=$((count+1))`。\n\n★ `$(( ))` 是**算术展开**，POSIX 标准，所有 shell 都支持。里面可以写 `+ - * / % **`、比较、位运算。\n\n★ 三种写法的区别：\n- `$(( ))` 返回**值**，可以赋给变量\n- `(( ))` 返回**退出码**（结果非 0 时退出码为 0），适合写 `if (( count > 10 ))`\n- `let` 是老式写法，语义同 `(( ))`\n\n★ **shell 默认全是整数运算**：`$((5/2))` = `2`，不是 `2.5`。要小数必须 `bc` 或 `awk`：`echo '5/2' | bc -l`。\n\n★ `&&` 与 `||` 别当逻辑运算用：shell 里它们是「命令连接符」，逻辑判断要用 `[ ]` / `[[ ]]`。\n\n★ **迁移**：`$((count++))` 的返回值是**自增前的值**，所以 `x=$((count++))` 里 x 拿到旧值；要新值用 `x=$((++count))`。"
            }
        ]
    },
    {
        "title": "判断一个文件存不存在（脚本写法）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "if",
            "test",
            "-f",
            "脚本"
        ],
        "choices": [],
        "source_section": "命令特训 · Shell 与管道",
        "statement_md": "脚本里要先判断 `/etc/nginx/nginx.conf` 在不在，不存在就退出。\n\n写出这个判断条件（`if` 的那一行）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "if [ ! -f /etc/nginx/nginx.conf ]; then",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|if [ ! -f /etc/nginx/nginx.conf ]; then\n|if [[ ! -f /etc/nginx/nginx.conf ]]; then\n|if test ! -f /etc/nginx/nginx.conf; then\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`if [ ! -f /etc/nginx/nginx.conf ]; then`。\n\n★ 文件测试符常用几个：\n- `-f` 是**普通文件**（存在且不是目录）\n- `-d` 是目录、`-e` 存在（任何类型）\n- `-r`/`-w`/`-x` 可读/可写/可执行\n- `-s` **存在且非空**（大小为 0 时为假）\n\n★ **`[` 是一个命令**（等价 `test`），所以 `[` 后面、`]` 前面**必须各有一个空格**。写成 `[-f x]` 会报 `[-f: command not found` —— 这个报错让人一脸懵，但原因就是这么朴素。\n\n★ `[ ]`（POSIX）与 `[[ ]]`（bash 扩展）的区别：`[[ ]]` 里**不需要给变量加引号**、支持 `&&`/`||`/正则 `=~`；`[ ]` 里变量为空时会报 `unary operator expected`。脚本里用 `[[ ]]` 更省心（但 `sh`/dash 不支持）。\n\n★ **迁移**：`[ -f f ] && echo yes || echo no` 是简写；目录不存在就建：`[ -d d ] || mkdir -p d`。"
            }
        ]
    },
    {
        "title": "遍历一个目录下所有 .log 文件并逐个处理",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 4,
        "total_score": 18,
        "tags": [
            "for",
            "循环",
            "引号",
            "通配"
        ],
        "choices": [],
        "source_section": "命令特训 · Shell 与管道",
        "statement_md": "要对 `./logs` 下每个 `.log` 文件执行 `gzip`（**文件名可能有空格**）。\n\n写出这个 for 循环（一行写完）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "for f in ./logs/*.log; do gzip \"$f\"; done",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|for f in ./logs/*.log; do gzip \"$f\"; done\n|for f in ./logs/*.log; do gzip $f; done\n|for f in ./logs/*.log; do gzip '$f'; done\n|find ./logs -name '*.log' -exec gzip {} +\n|find ./logs -name *.log -exec gzip {} +\n|find ./logs -name \"*.log\" -exec gzip {} +\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`for f in ./logs/*.log; do gzip \"$f\"; done`。\n\n★ **`\"$f\"` 的引号是必须的**：不加引号时文件名里的空格会让 `$f` 展开成多个词，`gzip my file.log` 就变成「压 my 和 file.log 两个文件」。\n\n★ **通配符不会被拆开**：`for f in *.log` 里 shell 是先展开通配再赋值，所以带空格的文件名**整体**赋给 `f`（这一步是安全的）。危险的是后面**使用** `$f` 时不加引号。\n\n★ 目录为空时 `for f in *.log` 会得到**字面量** `*.log`（bash 默认不报错），于是去处理一个叫 `*.log` 的文件、报 `No such file`。加 `shopt -s nullglob` 或先判断 `[ -e \"$f\" ] || continue`。\n\n★ **迁移**：要处理**递归**（子目录也要），`for` 循环不够，得用 `find ... -exec` 或 `while IFS= read -r -d '' f` 配合 `find -print0`（后者是处理任意文件名的标准做法）。"
            }
        ]
    },
    {
        "title": "在管道里过滤出想要的行并排序",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 4,
        "total_score": 18,
        "tags": [
            "管道",
            "grep",
            "awk",
            "ps"
        ],
        "choices": [],
        "source_section": "命令特训 · Shell 与管道",
        "statement_md": "要从 `ps aux` 里取出所有 `python` 进程，只显示**用户名和命令行**，并按用户名排序。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "ps aux | grep python | awk '{print $1, $11}' | sort",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|ps aux | grep python | awk '{print $1, $11}' | sort\n|ps aux | grep [p]ython | awk '{print $1, $11}' | sort\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`ps aux | grep python | awk '{print $1, $11}' | sort`。\n\n★ 四个环节各干一件事：`ps` 取进程、`grep` 过滤、`awk` 挑列、`sort` 排序 —— 这就是管道的思维方式：**每条只做一件事**。\n\n★ **`grep [p]ython` 这个写法的意义**（本题的进阶点）：`grep python` 会**匹配到 grep 自己**（因为它的命令行里就含 `python`）。`[p]ython` 是正则「p 或 …」的写法，**grep 自己的命令行里是 `[p]ython` 而不是 `python`**，所以它不会匹配自己。这是老运维的经典技巧。\n\n★ **更干净的替代**：`pgrep -af python` —— 直接按名字找并显示命令行，不需要管道，也不会匹配自己。\n\n★ **迁移**：`ps aux --sort=-%cpu | head -5` 取 CPU 前 5，比 `| sort` 更准确（`ps` 自己会排序，而且按数值而不是文本）。"
            }
        ]
    },
    {
        "title": "写一个简单的 if-elif-else 判断",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 4,
        "total_score": 18,
        "tags": [
            "if",
            "elif",
            "参数",
            "脚本"
        ],
        "choices": [],
        "source_section": "命令特训 · Shell 与管道",
        "statement_md": "脚本要根据参数值 `dev`/`prod` 输出不同内容，其他值报错退出。\n\n写出这个完整的 if 结构（`$1` 是参数）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "if [ \"$1\" = dev ]; then echo dev; elif [ \"$1\" = prod ]; then echo prod; else echo err; exit 1; fi",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|if [ \"$1\" = dev ]; then echo dev; elif [ \"$1\" = prod ]; then echo prod; else echo err; exit 1; fi\n|if [ $1 = dev ]; then echo dev; elif [ $1 = prod ]; then echo prod; else echo err; exit 1; fi\n|if [ '$1' = dev ]; then echo dev; elif [ '$1' = prod ]; then echo prod; else echo err; exit 1; fi\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "```bash\nif [ \"$1\" = dev ]; then\n    echo dev\nelif [ \"$1\" = prod ]; then\n    echo prod\nelse\n    echo err\n    exit 1\nfi\n```\n\n★ **字符串比较用单个 `=`**（POSIX 写法），bash 里 `==` 也认，但 `sh`/dash 只认 `=`。数值比较要用 `-eq`/`-lt`/`-gt`，**不能用 `=` 或 `<`**（`<` 在 `[ ]` 里会被当成重定向）。\n\n★ **`\"$1\"` 的引号不能省**：参数没给时 `$1` 为空，不加引号会变成 `[ = dev ]` —— `[` 收到 2 个参数，报 `unary operator expected`。\n\n★ **`fi` 是 `if` 倒着写**，收尾用。`elif` 可以有多层，`else` 可选。\n\n★ **迁移**：多个固定值匹配用 `case` 更清爽：`case \"$1\" in dev) ... ;; prod) ... ;; *) ... ;; esac`。\n\n★ 脚本开头加 `set -euo pipefail`：出错即停、用未定义变量即停、管道任一环失败即失败 —— 这是 shell 脚本健壮性的三大开关。"
            }
        ]
    },
    {
        "title": "查一条命令在历史里执行过几次",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 1,
        "total_score": 10,
        "tags": [
            "history",
            "Ctrl+R",
            "历史"
        ],
        "choices": [],
        "source_section": "命令特训 · Shell 与管道",
        "statement_md": "前几天敲过一条很长的 `rsync`，想找回来。\n\n写出这条命令（用历史搜索）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "history | grep rsync",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|history | grep rsync\n|history | grep 'rsync'\n|history | grep rsync\n|history | grep \"rsync\"\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`history | grep rsync`。\n\n★ `history` 输出的是**带行号的历史列表**，想重新执行某条用 `!123`（行号）或 `!!`（上一条）。\n\n★ **交互式更快的方式**是 `Ctrl+R`：进入反向增量搜索，敲几个字母就定位到最近匹配的命令，再按 `Ctrl+R` 继续往前找，`Enter` 执行、`Esc` 退出编辑。\n\n★ **历史默认不被立即写入**：一个终端里的命令要**退出后**才进历史文件，所以在另一个窗口 `history | grep` 找不到刚敲的。想让历史实时写入：`shopt -s histappend` + `PROMPT_COMMAND='history -a'`。\n\n★ **历史里有敏感信息**（密码、token）的风险：命令行带密码会被记进 `~/.bash_history`。脚本里用环境变量或 stdin 传密码，别写在命令行。\n\n★ **迁移**：`history -c` 清空当前会话；`history -w` 立即写盘；`HISTTIMEFORMAT='%F %T '` 让历史带上时间。"
            }
        ]
    },
    {
        "title": "让脚本在任何一步失败时立即退出",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "set -e",
            "pipefail",
            "健壮性"
        ],
        "choices": [],
        "source_section": "命令特训 · Shell 与管道",
        "statement_md": "写的部署脚本跑了半截失败了却还在继续，最后留下一个坏状态。\n\n要求：写出脚本**开头**该加的那一行。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "set -e",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|set -e\n|set -euo pipefail\n|set -eu\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`set -e`。\n\n★ `set -e`（errexit）让脚本在**任一命令返回非 0** 时立刻退出。默认行为是「不管失败，继续往下跑」——这就是「跑了一半、状态烂掉」的根源。\n\n★ 三个开关一起写是实践标准：\n- `set -e` 出错即停\n- `set -u`（nounset）**使用未定义变量就报错**（默认是展开成空串，于是 `rm -rf $DIR/` 里 `$DIR` 没设就变成 `rm -rf /`）\n- `set -o pipefail` 管道里**任一环**失败都算失败（默认只看最后一环）\n\n★ `set -e` 有几个**失效场景**要知道：命令在 `if` 条件里、在 `&&`/`||` 前面、或者用的是 `!` 取反时，都不触发退出。\n\n★ **迁移**：临时放宽某一条：`cmd || true`；调试时 `set -x` 打印每条执行的命令，`set +x` 关掉。"
            }
        ]
    },
    {
        "title": "把命令放在子 shell 里执行，不影响当前环境",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 3,
        "total_score": 15,
        "tags": [
            "子shell",
            "括号",
            "cd"
        ],
        "choices": [],
        "source_section": "命令特训 · Shell 与管道",
        "statement_md": "要在**不改变当前目录**的前提下，在一个目录里跑几条命令。\n\n写出这条命令（用子 shell 括号）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "(cd /tmp/x && ls)",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|(cd /tmp/x && ls)\n|(cd /tmp/x; ls -l)\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`(cd /tmp/x && ls)`。\n\n★ **圆括号 `( )` 开一个子 shell**：里面的 `cd`、变量赋值、`umask` 改动**全都不影响外面**。这是「临时切目录干活，干完自动回来」最干净的做法，比 `cd somewhere && cmd && cd -` 稳（后者中途失败就回不去了）。\n\n★ **花括号 `{ }` 的区别**：`{ cd /tmp/x && ls; }` 在**当前 shell** 里执行，`cd` 会**留下来**。而且 `{` 后面必须有空格、`}` 前面必须有 `;`。\n\n★ 子 shell 会**复制父 shell 的环境**，所以里面的变量能读到，但**改不了外面**。\n\n★ **迁移**：`(cd x && make) 2>&1 | tee log` 常用于「在子目录构建但不污染当前环境」；脚本里 `tar -C` 也是同一个思路（局部生效）。"
            }
        ]
    },
    {
        "title": "把多行文本喂给命令（不建临时文件）",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 4,
        "total_score": 18,
        "tags": [
            "printf",
            "heredoc",
            "标准输入"
        ],
        "choices": [],
        "source_section": "命令特训 · Shell 与管道",
        "statement_md": "要造两行测试数据喂给 `grep`，**不落盘**。\n\n要求：用一条管道完成（不要 `echo` 两次再用 `;`）。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "printf 'line1\\nline2\\n' | grep pattern",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|printf 'line1\\nline2\\n' | grep pattern\n|printf line1\\nline2\\n | grep pattern\n|printf \"line1\\nline2\\n\" | grep pattern\n|printf \"line1\\nline2\\n\" | grep pattern\n|printf line1\\nline2\\n | grep pattern\n|printf 'line1\\nline2\\n' | grep pattern\n|echo -e 'line1\\nline2' | grep pattern\n|echo -e line1\\nline2 | grep pattern\n|echo -e \"line1\\nline2\" | grep pattern\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`printf 'line1\\nline2\\n' | grep pattern`。\n\n★ **为什么用 `printf` 不用 `echo`**：`echo` 对转义序列的处理**因 shell 而异** —— bash 内建的 `echo` 默认**不解释** `\\n`（要 `-e`），而 `sh` 的 `echo` 常常解释。`printf` 是 POSIX 标准工具，行为**确定**，所以脚本里输出/造数据一律优先 `printf`。\n\n★ 末尾那个 `\\n` 别漏：不写的话最后一行**没有换行符**，接 `grep`/`wc -l` 时会少算一行 —— 这是「造的数据看起来少一行」的常见原因。\n\n★ 真正的**多行文本**用 heredoc：\n```bash\ngrep pattern <<'EOF'\nline1\nline2\nEOF\n```\n`'EOF'` 加引号表示内容原样传（`$VAR` 不展开）—— 生成配置文件时**必须**加引号。\n\n★ **迁移**：`printf '%s\\n' a b c` 一次造三行；`<<<` 是 herestring（bash 特性）：`grep x <<< \"$VAR\"`。"
            }
        ]
    },
    {
        "title": "提取命令输出里的某一列并求和",
        "subject": "linux",
        "line": "text",
        "question_type": "practical",
        "difficulty": 4,
        "total_score": 18,
        "tags": [
            "awk",
            "END",
            "求和",
            "du"
        ],
        "choices": [],
        "source_section": "命令特训 · Shell 与管道",
        "statement_md": "`du -sk /var/*` 输出的第一列是 KB 数。要把它们**加起来**得到总量。\n\n写出这条命令。",
        "input_format": "写**一条完整的命令**（含命令名与参数）；不要贴 `$` 提示符，不要写解释",
        "output_format": "一整条命令",
        "constraints_md": "",
        "time_limit_ms": 1000,
        "memory_limit_mb": 64,
        "checker": "oneof",
        "reference_solution": "du -sk /var/* | awk '{sum += $1} END {print sum}'",
        "cases": [
            {
                "stdin": "",
                "expected_stdout": "|du -sk /var/* | awk '{sum += $1} END {print sum}'\n|du -sk /var/* | awk '{s+=$1} END {print s}'\n",
                "is_sample": 0,
                "kind": "manual",
                "explanation": "`du -sk /var/* | awk '{sum += $1} END {print sum}'`。\n\n★ awk 的三段结构在这里全用上了：\n- `{sum += $1}` —— **每行执行一次**，累加第一列\n- `END {print sum}` —— **所有行处理完之后**执行一次\n（省略的 `BEGIN` 是「开始前执行一次」）\n\n★ **为什么要 `-k`**：`du -h` 输出的是 `1.2G`、`340M` 这种，awk **没法直接相加**（`1.2G + 340M` 不是数字）。`-k` 统一成 KB 整数，加完再换算。这是「想求和就别用 `-h`」的通用原则。\n\n★ awk 里未定义的变量**默认为 0**，所以 `sum` 不用初始化。\n\n★ **迁移**：`awk '{s+=$1} END {printf \"%.2f MB\\n\", s/1024}'` 直接换算单位；求平均：`END {print sum/NR}`（`NR` 是总行数）。"
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
                "explanation": "**`su -`** —— 那个减号（等价于 `su - root` / `su -l`）是本题唯一的机关。\n\n| 命令 | 换身份 | 换环境 | `$HOME` | `pwd` 落点 |\n|---|---|---|---|---|\n| `su` | ✅ | ❌ | 还是 `/home/{user}` | 还在原目录 |\n| **`su -`** | ✅ | ✅ **完整登录** | `/root` | `/root` |\n\n所以不带减号时，你虽然已经**是 root 了**，但 `$HOME` 还留着普通用户的值 ——打印出来的「root 主目录」是错的，而且**不会报任何错**。\n\n★ 另外两条也不行：`sudo pwd` 只是用 root 权限跑了一下 pwd，**没有切换身份**，还在原目录；`su root` 同样没带减号。\n\n**前提**：Fedora 安装时默认**不给 root 设密码**（用 sudo 代替）。真要用 `su -` 得先 `sudo passwd root` 设一个。"
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
                "expected_stdout": "|ls /usr/local > ~/test1.txt && cat -n ~/test1.txt\n|ls /usr/local > ~/test1.txt; cat -n ~/test1.txt\n",
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
                "expected_stdout": "|mkdir -p ~/abc && sudo cp /boot/vmlinuz* ~/abc/\n|mkdir -p ~/abc; sudo cp /boot/vmlinuz* ~/abc/\n|mkdir -p ~/abc && cp /boot/vmlinuz* ~/abc/\n|mkdir -p ~/abc; cp /boot/vmlinuz* ~/abc/\n",
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
                "expected_stdout": "|sort -r ~/mysort1\n",
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
                "explanation": "**对**。`.desktop` 文件就是应用的「菜单项定义」，有两个放的层次：\n\n| 位置 | 生效范围 |\n|---|---|\n| **`~/.local/share/applications/`** | 只对**当前用户**生效 |\n| `/usr/share/applications/` | **所有用户**（要 root 权限写） |\n\n最简模板：\n```ini\n[Desktop Entry]\nType=Application\nName=我的工具\nExec=/home/{user}/tools/run.sh\nIcon=/home/{user}/tools/icon.png\nTerminal=false\n```\n\n★ 三个容易卡住的点：\n1. **`Exec=` 要用绝对路径**（菜单启动时的 `PATH` 和你的终端不一样）\n2. 想让它在终端里跑就写 `Terminal=true`\n3. 写完可能**要重新登录**菜单才刷新（或者 `update-desktop-database`）\n\n权限别忘：`chmod +x` 那个 `.desktop` 文件并不必需，但 `Exec=` 指向的脚本**必须**可执行。"
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
                "explanation": "**`scp -P 2222 ...`（大写 P）**。\n\n★ 这就是最坑的地方 —— **`ssh` 和 `scp` 的大小写刚好相反**：\n\n| 命令 | 指定端口 | 那另一个大小写是什么 |\n|---|---|---|\n| `ssh` | **`-p 2222`**（小写） | `-P` 是「不分配伪终端」 |\n| `scp` | **`-P 2222`**（大写） | `-p` 是「保留文件的时间戳和权限」 |\n| `sftp` | **`-P 2222`**（大写） | 同 scp |\n\n**用小写 `-p` 的后果**：scp **不报错**，只是默默地连到 22 端口 —— 如果 22 上没服务，你会看到 `Connection refused`，然后开始怀疑网络、怀疑防火墙，**就是想不到是大写小写的问题**。\n\n**另一条路**（记不住就用这个）：在 `~/.ssh/config` 里给主机建个别名：\n```\nHost myserver\n    HostName 192.168.1.10\n    Port 2222\n    User {user}\n```\n之后 `scp 文件 myserver:` 和 `ssh myserver` 都不用再写端口了。"
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
