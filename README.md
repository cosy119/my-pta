# 本地 AI 出题 + 批改平台

浏览器打开的「个人版 PTA」：**AI 按讲义出题 → 你写代码 → 真跑判题 → AI 归因讲解**。

判题不是让 AI 看代码猜，而是**真起进程跑**，再拿真实输出比对 —— 所以判定和 OJ 一致。

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
| **题库 14 道 / 180 分 / 75 个测试点（第 02~08 讲）** | ✅ |
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

题目列表**按讲义讲次排序**（同讲次按难度），学习顺序就是列表顺序：

| 讲次 | 题目 |
|---|---|
| 第 02 讲 · 编程基础 | A+B 问题(10) · 圆的面积(10) |
| 第 03 讲 · 流程控制 | 判断闰年(10) · 区间求和(20) · 数字三角形(10) · 素数判断(15) |
| 第 04 讲 · 字符串 | 字符串反转与回文(10) · 单词计数(10) |
| 第 05 讲 · 列表与元组 | 求平均值(10) · 去重保序(15) · 第 k 大的数(15) |
| 第 06 讲 · 字典与集合 | 词频统计(20) |
| 第 07 讲 · 函数 | 最大公约数(10) |
| 第 08 讲 · 函数（下） | 斐波那契数列(15) |

题库定义在 `app/problems_bank.py`，每题都带 `source_section`（对应讲义讲次）。

**加题的铁律**：`expected_stdout` 先**独立算好**，再让参考解去撞它 ——
拿参考解现跑现填就是自己给自己判卷，永远满分。校验工具：

```bat
D:\Pythontools\Python\python.exe -X utf8 tools\verify_bank.py          &rem 全部
D:\Pythontools\Python\python.exe -X utf8 tools\verify_bank.py 素数      &rem 只验标题含「素数」的
```

改完题库先跑这个，60/60 通过才入库。

## 目录

```
pta/
├─ run.bat                 启动入口（纯 ASCII，只调用 run.py）
├─ run.py                  启动器：端口探测 / 自动开浏览器 / 错误不闪退 / 写日志
├─ stop.bat                停止服务（杀掉占用 8765 的进程）
├─ README.md               本文件
├─ config/
│  ├─ settings.toml        平台配置（解释器路径、时限、AI key 环境变量名…）
│  └─ prompts/             出题与讲解的提示词模板（P3/P5 用）
├─ app/
│  ├─ main.py              FastAPI 入口
│  ├─ config.py            读 settings.toml
│  ├─ db.py / schema.sql   数据库（含老库自动补列迁移）
│  ├─ scoring.py           评分：分值分配 / 计分 / 部分正确判定
│  ├─ seed.py              种子题（核心题 + 题库）与老库升级
│  ├─ problems_bank.py     题库（按讲义讲次，11 道）
│  ├─ api/                 HTTP 接口（problems / submissions / progress）
│  └─ judge/               判题内核
│     ├─ sandbox.py        进程沙箱（Job Object + 看门狗）
│     ├─ compare.py        输出比对
│     ├─ runner_python.py  Python runner
│     └─ worker.py         判题队列（单线程，按测试点分值计分）
├─ web/index.html          前端（单文件，无构建工具）
├─ tools/
│  ├─ selfcheck.py         判题内核 + 评分 自检（62 项）
│  ├─ httptest.py          HTTP 层自检（18 项，需服务在跑）
│  ├─ verify_bank.py       题库校验（参考解 vs 独立写好的期望输出）
│  └─ reset_progress.py    清空做题记录（保留题目；加 --yes 才真删）
└─ data/
   ├─ pta.db               题库与记录
   ├─ tmp/judge/           判题临时目录（判完即删）
   └─ logs/server.log      启动日志
```

## 自检

四份脚本都是「真跑出证据」，不是断言假设：

```bat
cd /d E:\学习\001\pta
D:\Pythontools\Python\python.exe -X utf8 tools\selfcheck.py     &rem 62 项：判题内核 + 评分
D:\Pythontools\Python\python.exe -X utf8 tools\verify_bank.py   &rem 60 个测试点：题库
D:\Pythontools\Python\python.exe -X utf8 tools\httptest.py      &rem 18 项：HTTP 全链路（需服务在跑）
D:\Pythontools\Python\python.exe -X utf8 tools\reset_progress.py &rem 清空记录（加 --yes 才真删）
```

注意：`selfcheck.py` 和 `httptest.py` 会往题库里写测试提交（也就改变了进度）。
自己刷题的记录不想被污染的话，跑完用 `reset_progress.py --yes` 清一下。

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
