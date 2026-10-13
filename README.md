# 本地 AI 出题 + 批改平台

浏览器打开的「个人版 PTA」：**AI 按讲义出题 → 你写代码 → 真跑判题 → AI 归因讲解**。

判题不是让 AI 看代码猜，而是**真起进程跑**，再拿真实输出比对 —— 所以判定和 OJ 一致。

> 仓库：<https://github.com/cosy119/my-pta>

## 两种用法

| 用法 | 适合 | 怎么做 |
|---|---|---|
| **本机跑** | 自己一个人用，最省事 | 双击 `run.bat` |
| **部署上网** | 想在手机/别的电脑刷，或者分享给别人 | 见 **[DEPLOY.md](DEPLOY.md)**（约 10 分钟） |

上网那种是「**GitHub Pages 放前端 + 一个免费后端专门判题**」。
**每个人的进度各自独立** —— 不需要注册，浏览器自己带一串通行证，
后端按它区分是谁（详见 DEPLOY.md 第三节）。

## 新机器上跑起来（克隆后三步）

```bat
git clone https://github.com/cosy119/my-pta.git
cd my-pta
run.bat
```

第一次跑会自动做这些事（不用手动初始化）：

1. 建 `data/` 目录和空数据库
2. 自动补表结构、补列、**把老数据归到「本机用户」**（老库也适用，不动已有数据）
3. **自动灌入 56 道题**（按标题判重，重复执行不会灌两遍）
4. 打开浏览器

`config/settings.toml` 里的解释器路径是我机器上的（`D:/Pythontools/...`）。
换机器不用改：**配置里的路径不存在时会自动在本机找 Python**（PATH → 常见安装位置）。
真要固定用某个解释器，才需要手改这个文件。

## 快速开始

```
双击 run.bat      ← 会自动帮你打开浏览器
```

或者命令行：

```bat
cd /d E:\学习\001\pta
run.bat
```

**不用自己记网址** —— 服务一就绪，默认浏览器会自动打开 <http://127.0.0.1:8765>。

启动器（`run.py`）会自己处理几种情况：

| 情况 | 表现 |
|---|---|
| 端口空闲 | 起服务 → 等 `/api/health` 就绪 → 自动开浏览器，黑窗口留着（日志在里面） |
| 服务已经在跑 | 直接开浏览器，3 秒后窗口自动关闭（不会报错、不会起第二个） |
| 端口被**别的程序**占 | 明确报出来，给出 `netstat` / `taskkill` 命令和「改 `run.py` 顶部 PORT」两条出路，并停住等你按键 |
| 依赖缺失 / 启动崩溃 | 打印完整 traceback + 装依赖提示，并停住等你按键（不会一闪而过） |

**停止服务**：黑窗口里按 `Ctrl+C`；如果窗口已经关了、服务还在后台，双击 `stop.bat`（会找到占用 8765 的进程并杀掉）。

启动日志写在 `data/logs/server.log`，出问题先看它。

## 现在能做什么

| 能力 | 状态 |
|---|---|
| Python 判题（AC / WA / PE / TLE / MLE / RE / CE / OLE） | ✅ |
| 双解释器可选（3.13.14 讲义环境 / 3.14.4 Thonny 环境） | ✅ |
| 限时（看门狗 + 杀整棵进程树） | ✅ |
| 限内存（Job Object，峰值可见） | ✅ |
| 4 种输出比对口径（standard / ignore_trailing / token / float） | ✅ |
| 运行自测（不判题，直接看输出） | ✅ |
| **每个测试点独立分值 · 部分正确** | ✅ |
| **每题进度（最高分 / 最后一次 / 首次满分时间）** | ✅ |
| **提交历史 + 一键回填某次代码** | ✅ |
| **打开题目自动回填上次提交的代码** | ✅ |
| **题库 56 道 / 860 分 / 230 个测试点（第 02~11 讲）** | ✅ |
| **数据备份 / 导出 JSON / 恢复** | ✅ |
| C / C++ 判题 | ⏳ P2 |
| AI 按讲义出题 | ⏳ P3 |
| Linux Shell 判题（SSH 到 Fedora） | ⏳ P4 |
| AI 讲解 / 双解释器对拍 / 导出 Obsidian | ⏳ P5 |

## 评分怎么算（对齐 PTA）

PTA 的模型是「**测试点**」：一道题由若干测试点组成，**每个测试点单独带分值**。

```
得分 = 通过的测试点分值之和       ← 不是「通过了几个」
满分 = 所有测试点分值之和
拿到分但没拿满 = 部分正确
```

- 题目有 `total_score`（满分）；测试点的 `points` 不写就**按满分均分**，余数给前面的测试点
  （100 分 6 个点 → `17 17 17 17 16 16`，求和恒等于满分）
- **每题进度取历史最高分**，刷题不倒退：低分提交不会把最好成绩冲掉
- `last_submission` 记最后一次、`best_submission_id` 记最高分那次 ——
  打开题目时自动回填**最后一次**的代码，历史面板里可以「回填」任意一次
- 部分正确时判定显示为「部分正确」，并标出**丢在哪个测试点、丢了几分**

老库升级不用手动做什么：启动时会自动补列（`ALTER TABLE ADD COLUMN`，不动老数据）、
同步种子题的分值与讲次、把旧口径的提交换算成得分制。

## 题库（按讲义进度循序渐进）

题目列表**按讲义讲次排序**（同讲次按难度），学习顺序就是列表顺序。
共 **56 道 / 860 分 / 230 个测试点**：

| 讲次 | 题数 | 分 | 题目 |
|---|---|---|---|
| 第 02 讲 · 编程基础 | 4 | 40 | A+B 问题(10) · 圆的面积(10) · 温度转换(10) · 三位数拆分(10) |
| 第 03 讲 · 流程控制 | 7 | 100 | 判断闰年(10) · 区间求和(20) · 数字三角形(10) · 素数判断(15) · 成绩等级(10) · 九九乘法表(15) · 水仙花数(15) |
| 第 04 讲 · 字符串 | 5 | 60 | 字符串反转与回文(10) · 单词计数(10) · 大小写互换(10) · 统计字符类型(15) · 查找子串(15) |
| 第 05 讲 · 列表与元组 | 7 | 105 | 求平均值(10) · 去重保序(15) · 第 k 大的数(15) · 极差(10) · 成绩统计(15) · 合并有序列表(20) · 矩阵转置(20) |
| 第 06 讲 · 字典与集合 | 6 | 105 | 词频统计(20) · 两数之和(20) · 集合运算(15) · 首字母分组(15) · 众数(15) · 缺失的最小正整数(20) |
| 第 07 讲 · 函数 | 4 | 65 | 最大公约数(10) · 海伦公式(15) · 可变默认参数的陷阱(20) · 哥德巴赫猜想(20) |
| 第 08 讲 · 函数（递归） | 6 | 105 | 斐波那契数列(15) · 递归求阶乘(15) · 汉诺塔(20) · 数位之和(15) · 爬楼梯(20) · 二分查找(15) |
| 第 09 讲 · 模块与包 | 5 | 75 | math 模块(10) · 日期相差天数(20) · 均值与中位数(15) · 累乘(15) · 最高分学生(15) |
| 第 10 讲 · 面向对象（上） | 5 | 80 | 矩形类(10) · 对象计数器(15) · 银行账户(20) · 两点距离(15) · 成绩管理器(20) |
| 第 11 讲 · 面向对象（下） | 7 | 125 | 形状面积（继承）(20) · 动物叫声（多态）(15) · 初始化顺序（super）(20) · 点的排序(20) · 向量相加(20) · 年龄校验(20) · 形状总面积（多态）(20) |

题库定义在 `app/problems_bank.py`（第一批）和 `app/problems_bank_ext.py`（第二批）。

**加题的两条铁律**：

1. **期望输出先独立算好**，再让参考解去撞它 —— 拿参考解现跑现填，就是自己给自己判卷，永远满分。
   本项目的 `expected_stdout` 全部由 **node 独立实现**预先算出（另一门语言、另一套算法）。
2. **第二套独立实现要对拍**（`alt_solution` 字段）。两套实现必须**各自都撞过全部测试点**，
   才能排除「单套实现有共同盲区」。

校验工具（改完题库必跑，全过才入库）：

```bat
D:\Pythontools\Python\python.exe -X utf8 tools\verify_bank.py          &rem 全部
D:\Pythontools\Python\python.exe -X utf8 tools\verify_bank.py 素数      &rem 只验标题含「素数」的
D:\Pythontools\Python\python.exe -X utf8 tools\verify_bank.py --quiet  &rem 只看汇总和失败项
```

## 目录

```
pta/
├─ run.bat                 启动入口（纯 ASCII，只调用 run.py）
├─ run.py                  启动器：端口探测 / 自动开浏览器 / 错误不闪退 / 写日志
│                          ★ 见到 $PORT 或 $PTA_CLOUD 就走云端模式（绑 0.0.0.0，不开浏览器）
├─ stop.bat                停止服务（杀掉占用 8765 的进程）
├─ DEPLOY.md               ★ 部署上网的完整步骤（Pages + 免费后端）
├─ Dockerfile              ★ 云端镜像（Render / Railway / Fly.io）
├─ render.yaml             ★ Render 一键配置（含持久化 Disk）
├─ requirements.txt        ★ 后端依赖（部署用）
├─ README.md               本文件
├─ .github/workflows/ci.yml ★ 每次推送自动跑自检（Linux + Windows 双平台）
├─ config/
│  ├─ settings.toml        平台配置（解释器路径、时限、CORS、AI key 环境变量名…）
│  └─ prompts/             出题与讲解的提示词模板（P3/P5 用）
├─ app/
│  ├─ main.py              FastAPI 入口（含 CORS）
│  ├─ config.py            读 settings.toml + 环境变量覆盖（PTA_DB / PTA_ALLOW_ORIGINS…）
│  ├─ db.py / schema.sql   数据库（含老库自动补列迁移）+ index.sql（迁移后建索引）
│  ├─ users.py             ★ 轻量身份：浏览器生成的 token 就是账号，首见即注册
│  ├─ scoring.py           评分：分值分配 / 计分 / 部分正确判定
│  ├─ seed.py              种子题（核心题 + 题库）与老库升级
│  ├─ problems_bank.py     题库第一批（11 道）
│  ├─ problems_bank_ext.py 题库第二批（42 道，带第二套实现对拍字段）
│  ├─ api/                 HTTP 接口（problems / submissions / progress / me）
│  └─ judge/               判题内核
│     ├─ sandbox.py        进程沙箱（★ 跨平台：Windows Job Object / Linux setrlimit+killpg）
│     ├─ compare.py        输出比对
│     ├─ runner_python.py  Python runner
│     └─ worker.py         判题队列（单线程，按测试点分值计分，按用户记账）
├─ web/index.html          前端（单文件，无构建工具）
├─ docs/                   ★ GitHub Pages 发布目录（由 export_static.py 生成）
│  ├─ index.html           前端副本
│  ├─ problems.json        题库快照（不含参考解）
│  └─ .nojekyll            别让 Jekyll 处理
├─ tools/
│  ├─ selfcheck.py         判题内核 + 评分 自检（62 项）
│  ├─ selftest_sandbox.py  ★ 沙箱跨平台自检（12 项，部署后在容器里跑它）
│  ├─ httptest_users.py    ★ 多用户隔离自检（23 项，自己起服务）
│  ├─ httptest_split.py    ★ 跨源（Pages + 后端）自检（18 项，含 CORS 预检）
│  ├─ httptest.py          HTTP 层自检（18 项，需服务在跑）
│  ├─ verify_bank.py       题库校验（双实现撞独立算出的期望输出）
│  ├─ export_static.py     ★ 导出静态题库 + 生成 docs/ 站点
│  ├─ backup_db.py         数据备份 / 导出 JSON / 恢复
│  └─ reset_progress.py    清空做题记录（保留题目；加 --yes 才真删）
└─ data/                   ← 不进 Git（见 .gitignore）
   ├─ pta.db               题库与记录
   ├─ tmp/judge/           判题临时目录（判完即删）
   └─ logs/server.log      启动日志
```

## 自检

脚本都是「真跑出证据」，不是断言假设：

```bat
cd /d E:\学习\001\pta
D:\Pythontools\Python\python.exe -X utf8 tools\selfcheck.py        &rem 62 项：判题内核 + 评分
D:\Pythontools\Python\python.exe -X utf8 tools\selftest_sandbox.py &rem 12 项：沙箱（跨平台）
D:\Pythontools\Python\python.exe -X utf8 tools\httptest_users.py   &rem 23 项：多用户隔离（自起服务）
D:\Pythontools\Python\python.exe -X utf8 tools\httptest_split.py   &rem 18 项：跨源 CORS（自起两个源）
D:\Pythontools\Python\python.exe -X utf8 tools\verify_bank.py      &rem 215 个测试点：题库双实现对拍
D:\Pythontools\Python\python.exe -X utf8 tools\httptest.py         &rem 18 项：HTTP（需服务已在跑）
D:\Pythontools\Python\python.exe -X utf8 tools\reset_progress.py   &rem 清空记录（加 --yes 才真删）
```

后三个（`selftest_sandbox` / `httptest_users` / `httptest_split`）会**自己起服务、测完自己关**，
不依赖外部状态，适合部署后在容器里立刻确认环境。

CI（`.github/workflows/ci.yml`）在 Ubuntu 和 Windows 上各跑一遍 ——
**Linux 那份专门用来验证沙箱的 setrlimit + killpg 分支**（本机是 Windows，测不到）。

注意：`selfcheck.py` 和 `httptest.py` 会往题库里写测试提交（也就改变了进度）。
**刷题前先跑自检，跑完再开始做题**；已经做了题就别再跑这两个脚本，
或者跑完用 `backup_db.py import` 把记录导回来。

## 备份与迁移（你的记录不会丢）

**先说清楚一件事：重启服务不会丢记录。**
`run.bat` 启动时只做「建表（IF NOT EXISTS）+ 补列 + 灌题（按标题判重）」，
**没有任何删除操作**，提交记录一条都不会少。

记录唯一会丢的情况是**手动执行**了清空命令：

| 会清空记录的东西 | 说明 |
|---|---|
| `tools/reset_progress.py --yes` | 手动清空（不加 `--yes` 只预览，安全） |
| `tools/selfcheck.py` / `httptest.py` | 会*新增*测试提交，不是删除；但会污染你的进度 |
| 删掉 `data/pta.db` | 直接删文件，当然就没了 |

### 把记录做成能带走的东西

`data/pta.db` **不进 Git**（二进制没法 diff、还会把你的做题过程广播出去）。
想备份/换机器，用这个：

```bat
cd /d E:\学习\001\pta

rem 1) 备份一份带时间戳的库到 backups/
D:\Pythontools\Python\python.exe -X utf8 tools\backup_db.py backup

rem 2) 导出成 JSON（纯文本，可以进 Git、可以人眼看、可以 diff）
D:\Pythontools\Python\python.exe -X utf8 tools\backup_db.py export

rem 3) 换机器后导回来（JSON 或 .db 都认）
D:\Pythontools\Python\python.exe -X utf8 tools\backup_db.py import backups\progress.json

rem 看看有哪些备份
D:\Pythontools\Python\python.exe -X utf8 tools\backup_db.py list
```

导入是**幂等**的：去重键是「题目 + 时间 + 判定 + 代码」，重复导入不会长重复记录，
已有的进度不会被覆盖（本地更权威）。

### 想给你自己定个自动备份

Windows 任务计划程序加一条，每天跑一次 `backup_db.py backup` 就行。
（`backups/` 已在 `.gitignore` 里，不会误提交。）

## 配置要点

`config/settings.toml`：

| 段 | 说明 |
|---|---|
| `[interpreters]` | `py313` / `py314` 两个解释器路径，`default` 选默认 |
| `[judge]` | `concurrency`（别改大，内存紧张）、默认时限、内存上限、输出上限 |
| `[shell]` | `ssh_target` —— **P4 前需要填**（例 `lijihao@192.168.1.10`） |
| `[ai]` | `key_env` 环境变量名、默认 base_url / 模型 |

平台**只读**这个文件，不会写回（免得把注释搞乱）。

## 几个实现上的坑（都实测过，写下来免得再踩）

1. **Job Object 的内存限额不会直接杀进程** —— 它让那次分配失败，Python 抛 `MemoryError` 后以退出码 1 结束，峰值停在限额的 ~99%。所以判 MLE 的判据是「峰值接近限额 + 进程异常结束」，不是 `peak >= limit`。
2. **超时必须杀整棵进程树**（`taskkill /F /T`），否则用户代码起的子进程残留，临时目录删不掉。
3. **输入输出一律字节模式**。`subprocess.run(input=..., text=True)` 会把 `\r\n` 二次翻译成 `\r\r\n`，造出假结论。
4. **比对前必须归一化换行** —— 本机 Python 往管道写的是 `\r\n`，期望值是 `\n`。不归一化就会「本机跑对、交上去 WA」。
5. **`-I`（isolated）不能用** —— 它在 3.11+ 隐含 `-P`，会把脚本目录移出 `sys.path`，跟 OJ 的真实行为不一致。
6. **3.13 与 3.14 的报错原文不同**（如 `1//0`：3.13 是 `integer division or modulo by zero`，3.14 是 `division by zero`）。平台如实反映所选解释器，所以同一份代码在两个环境下报错文字可能不一样。
