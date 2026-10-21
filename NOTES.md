# 本地 PTA 平台 · 实现笔记

> 这份文件是 `E:\学习\001\pta\` 的**实现细节备忘**，随仓库走。
> 面向「下次改这个项目时要先知道什么」——每条都是踩过坑之后写下来的结论。
> 工作区长期记忆 `E:\学习\001\.workbuddy\memory\MEMORY.md` 里只留操作要点，细节看这里。

## 架构与部署

```
GitHub Pages（docs/ 静态前端）
        │  X-User-Token 请求头，跨源
        ▼
免费云后端（Render，FastAPI + uvicorn）
        │  云盘 PTA_DB=/data/pta.db
        ▼
SQLite（题库 + 提交记录 + 进度）
```

- 仓库 <https://github.com/cosy119/my-pta>（公开，main）；Pages 源 = `main` / `/docs`。
- 在线地址 <https://cosy119.github.io/my-pta/>；本地双击 `run.bat` → <http://127.0.0.1:8765>。
- `data/` **零文件被跟踪**（`.gitignore` 覆盖 `data/`、`__pycache__/`）。
- ★ **Render 必须挂持久化 Disk 到 `/data`**，否则每次重新部署进度全丢。
- 静态快照 `docs/problems.json` **不覆盖库里已有的题**（seed 只补新的）——改了题面记得重新导出。

### 推送机制（别再踩）

- token 在 `C:\Users\Lijh\.git-credentials`（账号那栏写 `2029691715-dot`，实际登录 `cosy119`，`gho_` 开头 40 字符）。
- ★ **直接 `git push` 会挂到 SIGTERM**。必须：把 token 内联进 push URL + `GIT_TERMINAL_PROMPT=0` + `-c credential.helper=`。
- 推完 `git remote set-url` 还原（用内联 URL 时其实没改 remote，但养成习惯）。
- 输出里有 token，重定向到文件后 `sed` 打码再打印。

### 改了东西之后的固定动作

```bat
python tools\export_static.py      &rem ★ 改题库/前端后必须重跑，重新生成 docs/
python tools\verify_bank.py        &rem 861 题 / 1819 点，双实现对拍
python tools\selftest_cpp.py       &rem 9 项
python tools\selftest_theory.py    &rem 14 项
python tools\selfcheck.py          &rem 62 项
git add -A && git commit && git push（用上面的内联 token 姿势）
```

★ 改了 `editor-src/` 或 `web/index.html` 还要多两步（顺序不能反）：

```bat
npm run build:editor                        &rem editor-src → web/editor/editor.js
python tools\export_static.py --with-cases  &rem 顺手把 web/editor/ + web/index.html 同步进 docs/
node tools\ui_e2e_editor.mjs                &rem 真 Chrome 复验 63 项（必须对着刚导出的 docs/）
```

`export_static.py` 的 `_STRIP_FIELDS` 会剥掉 `reference_solution` / `ref_interpreter` / `ai_meta` / `ai_model` —— 静态站上绝不出现参考解。验收时要复查这一条。

## CI（`.github/workflows/ci.yml`）

两个 job：`linux`（ubuntu-latest）、`windows`（windows-latest），都跑 sandbox → cpp → theory → selfcheck → verify_bank。

- ★ **顶层钉了 `PYTHONUTF8: "1"` + `PYTHONIOENCODING: utf-8`**。
  没有这两行时，Windows job 在**第一步就崩**（打印中文撞 cp1252），后面全部 skip —— 等于所有自检白加。
- 查 CI 结果：本机 **`gh` 不可用**（报 `mise-shim: failed to execute mise`）→ 走 GitHub API + token 的 curl。
  - job 列表：`GET /repos/{o}/{r}/actions/runs/{id}/jobs`
  - 某个 job 的日志：`GET /repos/{o}/{r}/actions/jobs/{job_id}/logs`，**用 `curl -sL`**：该接口 302 到 blob 存储，curl 在跨主机重定向时**会自动丢掉 Authorization**，正好是需要的；用 Python urllib 会因为把 token 带过去而 401。
- 本机测不到的只有 **Linux 沙箱分支**（本机是 Windows；`/proc` 是模拟的；Docker 未装）→ 靠这个 workflow 验证。

## 控制台编码（`tools/_console.py`）

工具脚本全程打印中文。Windows 的 Python 默认按**系统 ANSI 代码页**写 stdout：

| 环境 | 代码页 | 打印中文的后果 |
|---|---|---|
| 中文 Windows（用户本机） | cp936 | 能编码，最多乱码 |
| **英文 Windows（GitHub runner）** | **cp1252** | **`UnicodeEncodeError` 当场崩** |
| 本机开了 `PYTHONUTF8=1` | utf-8 | 一切正常 → 所以本机一直没暴露 |

修法两层：

1. CI 顶层钉 `PYTHONUTF8`（覆盖所有 Python 步骤）
2. `tools/_console.py` —— **导入即生效**，把所有脚本的 stdout/stderr `reconfigure(encoding="utf-8", errors="replace")`。新写工具脚本记得加 `import _console`。

`errors="replace"` 是刻意的：宁可某个字符显示成问号，也**绝不让整个自检脚本崩在打印上**（自检的价值在结论）。

## 身份机制（无账号密码）

- 前端首开用 `crypto.getRandomValues()` 生成 32 位 hex token → `localStorage['pta.userToken']` → 每个请求带 `X-User-Token` 头。
- 后端 `users.resolve()` **首见即注册**。
- `_TOKEN_RE = ^[0-9a-f]{16,64}$`；非法 / 缺失 token 一律归到 `local-default-user`（界面显示「本机用户」）。
- 自动昵称：`"学习者-" + sha1(token)[:6]`。
- 所有读接口按 `user_id` 过滤；越权访问返回 **404**（不泄露「这个 id 存不存在」）。

## 数据隔离与迁移

- `mastery` 主键从 `problem_id` 单列改成 **`(user_id, problem_id)` 复合**；`submissions` 加 `user_id`。
- **SQLite 不能改主键** → `_rebuild_mastery()`：建 `mastery_new` → `INSERT OR REPLACE ... SELECT` → `DROP` 旧表 → `RENAME`。
- ★★ **顺序不能错**：`executescript(schema.sql)` → `_migrate()` → `executescript(index.sql)`。
  坑：schema 里带着 `CREATE INDEX ... ON mastery(user_id)`，老库还没补上 `user_id` 列就建索引 → `no such column: user_id`。**索引必须拆到独立的 `app/index.sql`**。
- `_update_mastery` 要加空 uid 兜底 `users.user_id_of(None)`，否则 selfcheck 裸 insert 会触发外键崩。
- ★ `db.py` 的 `_with_retry`（6 次退避重试）覆盖 `execute` / `executemany`。
  起因：**这台机器的杀软会在 .db 被改写的一瞬间锁住文件**，症状是判题中途所有提交变 IE、`attempt to write a readonly database`，而同进程的 Web 线程插新提交却成功（文件权限、磁盘、WAL 全都正常，同一路径连写 300 次也没事）。

## 沙箱：两个平台两套实现

| | Windows | Linux |
|---|---|---|
| 限内存 | Job Object | `preexec_fn` 设 `RLIMIT_AS` → 退 `RLIMIT_DATA` → `RLIMIT_FSIZE` |
| 杀进程树 | `taskkill /F /T` | `os.killpg` + `start_new_session=True` |
| 内存峰值 | Job Object 查询 | ★ **运行期间起采样线程**读 `/proc/<pid>/status` 的 VmHWM |

### ★★ Linux 峰值必须采样（2026-10-13 修）

原来的写法是**运行前读一次 + 运行后读一次，取 max** —— 两条路都读 0：

- 运行前：进程刚 exec，还没分配内存
- 运行后：进程已退出，`/proc/<pid>` 条目消失

结果 `near_limit`（峰值 ≥ 限额×0.9）永远不成立 → **内存超限被判成 RE**。
CI 上实测的报错就是 `[FAIL] 判 MLE -- RE 峰值 0 MB / 限额 128 MB`。

修法：起一个 5ms 间隔的采样线程，进程存活期间不停读 VmHWM 记最大值。

- 为什么 5ms 也够（不会漏中间尖峰）：**VmHWM 是进程自身的历史峰值、单调不减**，存活期间采到**任意一次**就拿到了截至那一刻的最高值。
- 为什么一定有采样窗口：Linux 的 `RLIMIT_AS` 是**软限制** —— 分配失败时进程自己抛 `MemoryError` 后正常退出，不是被内核秒杀。
- 兜底：采样全为 0 时用 `getrusage(RUSAGE_CHILDREN).ru_maxrss`，但**必须要求本次刷新了历史记录**（`after > before`）才采信 —— 否则会拿上一个用例的峰值来判这一个，造成假 MLE。
  （`ru_maxrss` 在 Linux 是 KB，macOS 是字节。）

### ★ MLE 判据 = 两条**独立**的证据链，任一条成立即判

抽取成纯函数 `sandbox.memory_exceeded()`（可被直接断言，见下面「自检脚本」里的判据矩阵）：

```python
if not mem_bytes or not (exit_code != 0 or timed_out):
    return False                     # 没设限额 / 正常跑完 → 一律不算
if OOM_MARKER in stderr:
    return True                      # 链 A（直接证据）
return peak >= mem_bytes * 0.9 and not stdout.strip()   # 链 B（间接证据）
```

**链 A（直接）**：stderr 里明确出现内存不足的字样。Linux 的 `RLIMIT_AS` 触发时
Python 抛 `MemoryError` 并打印 traceback —— 最硬的证据，不需要再拿峰值去凑比例。

> ★★ 为什么不能只靠峰值比例（2026-10-13 踩到）：Linux 限的是**地址空间**（`RLIMIT_AS`），
> 而 `VmHWM` 量的是**实际驻留 RSS**，两个不是同一个量纲。地址空间打满时 RSS 往往只到八成就上不去了。
> CI 上实测 **51 MB / 64 MB 限额（比值 0.80 < 0.9）**，只靠比例那条链必然漏判成 RE。
> 这个错只有 Linux 会暴露，本机（Windows）怎么跑都是对的。

**链 B（间接）**：峰值顶到限额附近 **且** 异常结束 **且** 没有正常输出。
这一条是为 Windows 准备的：**Job Object 的进程内存限额不杀进程** ——
它让那次分配失败，于是 Python 抛 `MemoryError`、以退出码 1 结束，峰值稳定停在限额的 ~99.7%
（实测 65340/65536 KB）。「没有输出」必须一起看：机器有负载时进程可能没跑到峰值就被别的原因带崩。

- `_OOM_MARKERS` = `MemoryError` / `can't allocate memory` / `cannot allocate memory` /
  `std::bad_alloc` / `out of memory`
- **反向验证必须一直成立**：正常程序、普通崩溃、`exit(1)`（峰值 13 MB）两条链都不成立 → 判 RE，不误判成 MLE。
  这 7 种组合现在是 `selftest_sandbox` 的 [7] 节，逐条断言。

### 另两条坑

1. 超时必须杀**整棵进程树**，否则子进程残留、临时目录删不掉。
2. **`-I` 不能用**：3.11+ 的 `-I` 隐含 `-P`，会把脚本所在目录移出 `sys.path`。只用 `-X utf8=1 -u`。

### ★ 本机进程启动开销：160~400 ms（做性能题必须知道）

2026-10-13 实测（本机 Windows + Kaspersky + 金山毒霸两套杀软）：

| 场景 | 耗时 |
|---|---|
| 空 C 程序（`int main(void){return 0;}`），**裸** `subprocess` 跑 | **164 ~ 179 ms** |
| 同一个空程序，走沙箱（多一个 Job Object） | **180 ~ 310 ms** |
| Python 解释器起一下（`-c pass`） | **362 ~ 396 ms** |

**结论：这台机器上「启动一个进程」本身就是几百毫秒。** 一个什么都不做的程序都要 164 ms，
所以量出来的 `time_ms` 里有一大块根本不是被测量代码的耗时。

后果：

1. **本机判题时，1000 ms 的题目限制里学生代码实际只剩 600~800 ms**。
   临界题会**偶发 TLE**（实测撞到过一次：204 题全量对拍里「循环队列操作模拟」的 alt 解在
   测试点 3 报 `TLE 1918 ms`，单独重跑同一份解 **5/5 通过**）。
2. **云端 / CI 不受影响**（Linux、无杀软），所以**不要去调题库的时间限制** ——
   那是给学生的题目约束，应该基于干净环境。改了反而让题目对学生放水。
3. 对拍工具里给 TLE 加了一次重试（只有两次都 TLE 才算真 TLE，真死循环照样抓得住）。
   **真实判题绝不这么做** —— 学生提交超时就该判超时。

写性能相关题解、或跟用户解释「为什么你这题在本机 TLE 但交上去 AC」时，记得这条。

## 云适配与启动器

- `config.path(key)` 支持 `PTA_<KEY>` 环境变量覆盖（`PTA_DB` / `PTA_LOGS` / `PTA_TMP_JUDGE`）。
- `run.py` 探测 `$PORT` 或 `$PTA_CLOUD` → 绑 `0.0.0.0:$PORT`、不开浏览器、不 pause。
- CORS 默认 `["*"]` + `allow_origin_regex=r"https://.*\.github\.io"`，`allow_credentials=False`（身份走头不走 cookie）。
- ★ **启动逻辑全在 `run.py`，`.bat` 只是纯 ASCII 入口**（防 GBK 解析破坏 bat 结构）。

  `run.py` 的四种情形都要处理：

  | 情形 | 行为 |
  |---|---|
  | 端口空闲 | 起服务 + **轮询 `/api/health` 就绪后自动开默认浏览器** |
  | 端口被占且 health 通 | 判「已在跑」，直接开浏览器 |
  | 端口被占但 health 不通 | 报「被别的程序占了」+ 三条出路 + pause |
  | 启动崩溃 | traceback + pause |

  全程写 `data\logs\server.log`。**给用户的「一键启动」必须自己处理端口冲突并把界面送到眼前。**

- `run.bat` 必须保持**非 ASCII 字节数 0**：
  `[System.IO.File]::ReadAllBytes($f) | ? { $_ -gt 127 }` 计数要为 0。

### ★★ 云端那条启动分支：两个一部署就炸的 bug（2026-10-14 修）

Dockerfile 和 render.yaml 早就写好了，但**云分支从来没人真跑过** —— 于是埋了两个雷，
都是「本地双击 `run.bat` 永远碰不到、`e2e_ui` / `selfcheck` 也抓不到」的那一类
（它们都默认「服务已经手动起好了」）：

| 症状 | 根因 |
|---|---|
| 部署后进程秒退，日志 `NameError: name 'config' is not defined` | `run.py` 云分支里用了 `config.get()`，但 `config` **只在 `main()` 的分支里才需要**，模块顶部根本没导入 |
| 部署判「不健康」，但容器内部 curl 得通 | `host_env` 返回 `self.host` = `127.0.0.1`（`config/settings.toml` 里的值）。容器绑本地回环，平台健康检查从外面连不上 |

修法：

- 云分支里 `from app import config as _config` 显式导入，并给 import / uvicorn 都包上 try，
  崩溃时打完整 traceback（云上只看得到 stdout，静默退出等于没法排）。
- `host_env` 改成：`HOST` 环境变量优先 → 否则**有 `PTA_CLOUD` 或 `PORT` 就返回 `0.0.0.0`**
  → 再否则返回配置里的 `127.0.0.1`（本地跑别把服务暴露到局域网）。
- `/api/health` 和启动日志改报 `host_env` / `port_env`（实际监听值），
  不是配置里那份 —— 否则在 Render 上看到 `"port": 8765` 会一脸问号。

**新增 `tools/smoke_cloud.py` 把这条路径锁住**（13 项）：真起一个子进程
`python run.py`、环境照抄云端（`PTA_CLOUD=1` + `PORT=<空闲端口>`、清掉 `HOST`），
然后断言：起得来 / health 的 host 是 `0.0.0.0` / port 等于注入值 / 三科目目录齐 /
静态前端拿得到 / **C++ 与 Python 各交一次都要 AC**。

最后那一对是关键：CI 的 ubuntu runner 上 `settings.toml` 里那串 `D:/mingw64/...`
根本不存在，能 AC 就证明**兜底探测**（`shutil.which("g++")` / `_probe_python`）真的生效了 ——
也就是容器镜像里的工具链被正确找到了。

> 教训：**配置文件里写了 `runtime: python` 就等于没装编译器**。
> 数据结构线要真编 C/C++，Render 必须走 `runtime: docker`（镜像 `apt install gcc g++ libc6-dev`）。

### ★★ Render 免费档不能挂持久化 Disk（2026-10）

很多教程让你「在 Render 免费实例上挂个 Disk 存 SQLite」—— **现在做不到**。
官方免费档限制：free web service **无 SSH、无持久化磁盘**，
且每次休眠 / 重启 / 重新部署都会丢掉本地文件系统的一切改动
（免费实例 15 分钟无访问即休眠 → 进度基本留不住）。

- 免费档还能跑：题库每次启动从 `app/problems_bank*.py` 重建，**题目永远在**；
  只有 `submissions` / `mastery` 会丢。
- 要留进度：`plan: starter`（$7/月）+ 磁盘（$0.25/GB/月）。
- 所以 `render.yaml` 里 disk 段默认**注释掉**，否则免费档部署会直接报错。
- 免费档还有 0.1 vCPU / 512 MB —— 编译 C++ 慢，计算量大的题更容易撞时间限制。

## 判题与评分

- 架构：FastAPI + uvicorn → API 只入队 → **独立后台单线程**（concurrency=1）→ 每个用例独立子进程 → 限内存 + 墙钟看门狗。
- ★ **评分模型对齐 PTA「测试点」**：每个点单独带分值，**得分 = 通过点的分值之和**（不是通过个数 × 均分）。
  `points` 没写就按满分均分、余数给前面（求和恒等于满分）；拿分没满 = **部分正确**；进度取**历史最高分**。核心在 `app/scoring.py`。
- **每题三个指针**：`best_submission_id`（最高分）/ `last_submission_id`（**打开题目时自动回填其代码**）/ `solved_at`。
- **老库升级全自动**：`MIGRATIONS` 用 `PRAGMA table_info` 查完再 `ALTER TABLE ADD COLUMN`；
  `backfill_points()` 对种子题强制同步 满分/分值/讲次（⚠️ ADD COLUMN 的默认值会给所有老行填同一个值）；`backfill_legacy_scores()` 换算旧口径。
- ★ `worker.py` 的 `flush_cases()` **必须在写最终结论之前调用**，否则前端会出现「结论出来了但逐测试点明细还没落库」的空窗。

## 题库（1137 题 / 14114 分 / 2325 测试点）

| subject | 题库文件 | 题数 | 分 | line | 语言 |
|---|---|---|---|---|---|
| `python` | `seed.py::CORE_PROBLEMS`(3) + `problems_bank.py`(78 = 53 编程 + ext2 14 + bits 11) + `problems_bank_py_prog.py`(10) + `problems_bank_py_tricks.py`(30) + 理论 `problems_bank_py_theory.py`(66) + `problems_bank_py_theory2.py`(68 = 49 + 进制转换 14 + 异或 2 + 进制解析 3) | **255** | **3160** | python | Python |
| `ds` | `problems_bank_ds.py` + `problems_bank_ds_prog.py` + `problems_bank_ds_theory.py` + `problems_bank_ds_tricks.py`(39) | **240** | **3486** | cpp | **C 或 C++ 任选** |
| `cpp` | `problems_bank_cpp_theory.py`(111) + `problems_bank_cpp_theory2.py`(112) + `problems_bank_cpp_prog.py`(17) + `problems_bank_cpp_tricks.py`(20) | **260** | **2957** | text / cpp | **C++ 基础线（12 讲各 20 题 + 技巧特训 20 题）** |
| `linux` | `problems_bank_linux.py` | **382** | **4511** | text | 理论题（单选 / 多选 / 判断 / 填空）+ **实操题 203**（写命令） |

- ★★ **CORE 住在 `seed.py` 而不是 `problems_bank.py`** —— `verify_bank` 曾经因此只验了 `BANK_PROBLEMS`，
  **CORE 那 3 题连单撞都没有**。现在 `LINES` 用的是 `CORE_PROBLEMS + BANK_PROBLEMS`。
  **加题库时先确认对拍覆盖到了。**
- Python 讲次分布：02→4 / 03→7 / 04→5 / 05→7 / 06→6 / 07→4 / 08→6 / 09→5 / 10→5 / 11→7 / 12→5 / 13→5 / 14→4（第 12~14 讲由 `problems_bank_ext2.py` 覆盖，全书 01~14 全有题）。
- Linux 讲次分布：01→5 / 03→2 / 04→2 / 05→6 / 06→8 / 07→**7** / 08→9 / 09→9 / 10→5 /
  **11→7 / 12→14 / 13→14 / 14→14 / 15→6 / 16→6**；另加「基础命令」45 + 「实验」20。
  （第 02 讲的内容由「基础命令」组覆盖 —— 那 45 道就是围绕 Shell 命令出的。）
  - 2026-10-15 再补：`part_multi()` 8 道**多选**，落在 07 / 11 / 12（×2）/ 13（×2）/ 14（×2）。
  - 2026-10-19 再补：`part_practical()` **15 道实操题**，把作业 1~5 的 46 个操作步骤全覆盖
    （实验1 装机 1 / 实验2 2 / 实验3 3 / 实验4 4 / 实验5 5）。
  - **2026-10-19 晚大改**：实操题从「跑验收命令 → 填输出」改成「**给场景 → 写命令**」，
    并且从 15 道扩到 **203 道**（`tools/linux_cmd_bank.py`，见下面「★ 命令题」一节）。
    原因见那节开头 —— 旧形态考的是「会不会抄屏幕」，不是「会不会用命令」。
- **题型分布（全库）**：编程 309 / 单选 355 / 实操 203 / 判断 114 / 填空 91 / 多选 47 / 简答 18。
  Linux 线单独一份：单选 115 / 多选 8 / 判断 31 / 填空 25 / **实操 203** = 382 题。
  C++ 基础线单独一份：单选 153 / 编程 37 / 判断 29 / 填空 20 / 多选 13 / 简答 8 = 260 题。
  （这行跟着题库涨，别当常量用 —— 要准数就 `SELECT question_type, COUNT(*) FROM problems GROUP BY 1`。）

### ★ C++ 基础线（2026-10-21 建线，260 题 / 2957 分）

第四条学科线，对应 Obsidian 的 `C++基础` 线（郑莉《C++语言程序设计》第5版，544 页 12 讲）。
`subject = "cpp"`、`line = "text"`（理论）/ `"cpp"`（编程），前端题号前缀 **CP**。

**每讲固定 20 题**（二轮扩题后拉齐，循序渐进：讲内 difficulty 1→4，全库 1:22 / 2:72 / 3:97 / 4:49）：

| 讲 | 题数 | | 讲 | 题数 | | 讲 | 题数 |
|---|---|---|---|---|---|---|---|
| 01 绪论 | 20 | | 05 数据的共享与保护 | 20 | | 09 模板与群体数据 | 20 |
| 02 简单程序设计 | 20 | | 06 数组指针与字符串 | 20 | | 10 泛型程序设计与 STL | 20 |
| 03 函数 | 20 | | 07 类的继承 | 20 | | 11 流类库与输入输出 | 20 |
| 04 类与对象 | 20 | | 08 多态性 | 20 | | 12 异常处理 | 20 |

- 二轮扩题（2026-10-21 下午）：理论 119 → 223（`_theory.py` 111 + `_theory2.py` 112），编程 17 不变；
  新增 104 道里 **63 道答案由 `run_cpp()` 真跑反推**，其余为纯概念（生成器里逐题标「无计算」）。
- ★★ **答案字母必须打散**：二轮扩题时 `_theory2` 出现过「80 道单选答案全在 A」——等于闭眼选 A 就满分。
  已改为**按标题 sha256 取模的确定性轮转**（先转选项、再用值找位置），分布 A33 / B40 / C45 / D35，
  并加两条 `_sanity()` 断言：任一字母占比 >40% 直接报错、解析里出现「选 X / 选项 X」字母引用直接报错。
  **多选题**同步轮转，答案组合落在 ABC/ABD/ACD/BCD 多种。
- 模块与生成器（都是「自动生成，不要手改」）：
  `tools/gen_cpp_theory.py` → `app/problems_bank_cpp_theory.py`（01~06 讲 111 题）
  `tools/gen_cpp_theory2.py` → `app/problems_bank_cpp_theory2.py`（07~12 讲 112 题）
  `tools/gen_cpp_prog.py` → `app/problems_bank_cpp_prog.py`（17 道编程题）
- **答案可信度**：生成阶段共调用 `run_cpp()` **118 次**（`gen_cpp_theory.py` 76 次 / `gen_cpp_theory2.py` 42 次，实测计数，
  不是估的）——凡「这段代码输出什么 / sizeof 多少 / 构造析构顺序 / 字节数」的题，答案都是真编译真运行取回输出，
  再拿输出到选项里反推字母（命中 0 次或多次直接中断生成）。纯概念题在生成器里逐题标「无计算」。
  编程题 17 道全部「Python oracle 独立算期望 + solution/alt 双撞」，103 个测试点逐字节对拍。
- 挂载点（**加新科目线要动五处，漏一处就有一半人看不到**）：
  1. `app/seed.py`：三个 import + `SUBJECT_LABELS["cpp"]` + `SEED_PROBLEMS`（顺序 = 前端展示顺序）；
  2. `tools/verify_bank.py`：import 三模块 + `LINES` 加 `("cpp", "C++ 基础线", ...)`；
  3. `app/api/problems.py::SUBJECT_ORDER`：`cpp: 2`（linux 顺延到 3）；
  4. `web/index.html`：`SUBJECT_LABELS` + `SUBJ_PREFIX`（`cpp: 'CP'`）+ `SUBJECT_ORDER` 三处；
  5. `tools/selftest_theory.py::ALL_THEORY` 要并进新理论题，否则多选的「漏选必须判错」没人守。
- 两个新工装（全线通用）：
  - `tools/cpp_eval.py`：`run_cpp(src, stdin_text="")` 编译并运行一段 C++，返回 stdout（带 sha1 编译缓存）。
    ★ `std_flags` 是**单个字符串整体传给 g++**，写 `-std=c++17 -fno-elide-constructors` 会被当成一个参数报错；
    只想关拷贝消除时只传 `-fno-elide-constructors`。★ 不支持指定工作目录，需要落盘的实验自己写临时文件并清理。
  - `tools/check_title_unique.py`：全模块标题查重（`seed.ensure()` 按标题判重且**静默跳过**，撞名不报错）。
    ★ `--new` 后面的标题**必须逐个加引号**，否则按空格被拆成多个词，报「撞车 0 条」是假绿。
    它报出的 25 组「已有重复」是 `problems_bank` / `py_bits` / `ext2` 之间的历史遗留，不是新引入的。
- 验收（2026-10-21 实跑，扩题后复验）：
  `verify_bank.py --cpp` → **240 题 / 326 测试点 / 参考解 326 全过，alt 也全过**；
  `selftest_theory.py` → 732 道理论题、15 项全过（含 41 道多选穷举子集）；
  `export_static.py --with-cases` → `docs/problems.json` 1117 题 / 2205 测试点，四科齐全。
  （★ 2026-10-21 晚加完「技巧特训 · C++」20 题后复验：**260 题 / 446 点 / 参考解 446 全过**，
  全库 1137 题 / 14114 分 / 2325 点 —— 上面这组是建章当时的快照，别当现值。）

- **笔记区也接进来了**（2026-10-21）：`tools/export_notes.py` 的 `LINES` 加 `("C++基础", "cpp", "C++ 基础")`、
  `TOP_DOCS` 加 `C++基础总览`；`LECTURE_DIR_RE` / `SECTION_RE` 都加了**可选 `Cpp` 前缀**
  （`^(?:Cpp)?(\d{1,2})讲…`）—— 不加的话每条分节都会掉进「命名不规范 → sec=99」兜底分支。
  现在笔记 639 篇 / 8.3 MB，四线：Linux 192 / Python 180 / 数据结构 108 / **C++ 159**（146 分节 + 12 索引 + 总览）。

- ★★ **线上核实（2026-10-21 15:04 实测，不是估的）**：下载 `https://cosy119.github.io/my-pta/problems.json`
  到 `data/tmp/pg_live.json`（**8,204,389 字节**，`generated_at` = `2026-10-21 14:43:45`）后逐项对账：
  顶层 `count 1117 / total_score 13762 / total_testcases 2205` 与实算一致；分科 `python 255 / ds 240 / cpp 240 / linux 382`；
  C++ **240 题 / 2605 分 / 326 点 / 十二讲各 20 题 / 无 cases 的题 0 道**；
  题型 单选 153 / 判断 29 / 填空 20 / 多选 13 / 简答 8 / 编程 17；难度 1:22 / 2:72 / 3:97 / 4:49。
  ★ 抓取坑：`curl` 对 8 MB 文件要 `--max-time 150`（40 s 会截断）；**别往 `/tmp` 存**（Windows Git Bash 跨 shell 会丢），
  存 `pta/data/tmp/`；JSON 顶层键是 **`items`** 不是 `problems`，题内分数字段是 **`total_score`**、讲次是 **`source_section`**。
- ★★ **库与模块的 C++ 单选存在「等价但不同」的轮转（2026-10-21 发现，未修，属良性）**：
  `ensure()` 只插不改，所以线上库保留的是**改版前那一轮**选项顺序——42 道单选的选项数组与答案字母跟当前模块不同。
  按「**答案字母指向的选项正文**」逐题比对：**153/153 完全一致，真不一致 0 道**（两套轮转语义等价，不是错题）。
  两个后果要知道：①线上字母分布 **A64 / B29 / C36 / D24（A 占 41.8%）**，比模块侧的 A33/B40/C45/D35（A 21.6%）更偏 A；
  ②从零重建库会再变一次字母，任何笔记里写死的字母会失效。
  想拉平只能重 seed；**别用 `sync_bank_cases.py` 单刷**——它只 `UPDATE testcases`（expected_stdout/explanation/is_sample），
  **不同步 `problems.choices`**，单独刷会把「字母」和「选项正文」拆开，直接变错题。

### ★ 技巧特训 · C++（2026-10-21 建章，20 题 / 352 分）

C++ 线的第二个附加章，与 DS 线那 39 道**刻意分工**：
`gen_ds_tricks.py` 考的是**算法怎么实现**（背包 / 单调栈 / 二分答案 / LIS / 树状数组），
本章考的是**用哪个 STL 设施、写哪一行** —— 同样是「有序数组里数个数」，
DS 线让你手写二分，本章让你写 `upper_bound(...) - lower_bound(...)`。

生成器 `tools/gen_cpp_tricks.py` → `app/problems_bank_cpp_tricks.py`（自动生成，不要手改）。
难度 **1~4 各 5 题**，每题 6 个测试点（前 2 个是公开样例），合计 120 点 / 352 分。

| 难度 | 主题 | 五道题 |
|---|---|---|
| 1 | 算法库一行流 | `count_if` 三问 / `lower_bound`+`upper_bound` 的差 / `rotate` 左旋 / `accumulate` 初值 `0LL` / `find` 切分逗号串 |
| 2 | 排序三件事 | `stable_sort` 稳定性 / 严格弱序比较器 / `merge` 归并 / `priority_queue<greater>` 合并果子 / `stable_partition` |
| 3 | 容器语义 | `set::insert` 的 bool / `map::emplace` 不覆盖 / `nth_element` 次序统计 / `copy_if`+`back_inserter` / `tuple` 字典序 |
| 4 | 竞赛组合套路 | 双指针夹逼三数之和 / 扫描线并集长度 / `a+b<b+a` 拼最小数 / `partial_sum` 前缀和 / 大顶堆最少迟到任务 |

- 每道题都写成「**先给正确的那几行，再点名错法**」：`>=` 破坏严格弱序、
  `accumulate(…, 0)` 溢出、`abs(INT_MIN)`、`x % 2 == 1` 漏负奇数、
  `middle` 不取模越界、`c.reserve` 与 `back_inserter` 的配合、`endl` 刷缓冲。
- ★ 20 题**全部真编真跑**：40 份源码（参考解 + alt）先 `g++ -std=c++17 -O2 -fsyntax-only` 快速筛语法
  （第一轮正好逮到 `string::find` 那题漏 `#include <iostream>`），再真编译，
  120 点 × 2 套解**逐字节全等**（一次性对拍脚本 2 分 18 秒）。
- ★ `alt` 全部换实现路径而不是改名：三次 `reverse` 换 `rotate`、手写二分换 `lower_bound`、
  插入排序换 `stable_sort`、`multiset` 换 `priority_queue`、哈希换双指针、
  事件扫描换区间合并、手写归并排序换 `std::sort`。
- 挂载四处：`seed.py`（import + `SEED_PROBLEMS`，放 cpp 组最前、与 Python/DS 线一致）、
  `verify_bank.py`（import + `LINES`）、`check_title_unique.py::MODULES`、
  `smoke_cloud.py::ref_of`（**技巧章排前面，不加进去「第一道 cpp 题」会取不到参考解**）。
  顺手修了 smoke_cloud 里一条**早就过时的断言** `set(got) == {"python","ds","linux"}` ——
  加 cpp 线之后必挂，改成 `set(got) == set(expected)`。
- 章名「技巧特训 · C++」与 DS 的「技巧特训 · C/C++」只差两个字符，前端按 `source_section` 精确匹配所以不会串，
  但 `grep` 时两个都要带上。
- 验收：`verify_bank.py --cpp` → **260 题 / 446 点 / 参考解 446 全过、alt 全过**；
  `export_static.py --with-cases` → `docs/problems.json` **1137 题 / 14114 分 / 2325 点**；
  `check_title_unique.py` → 1137 条标题、25 组重复**全是 `problems_bank` ↔ `py_bits`/`ext2` 的历史遗留**，
  本章 20 个标题零撞车。

### ★ 技巧特训章（2026-10-18 晚建章，两线各 20 题；2026-10-19 各 +10 进阶；2026-10-19 晚 DS +4 插入维护；2026-10-20 DS +5 整行反转）

讲义没专门讲、但做题（蓝桥杯 / 码蹄杯 / ACM）总会遇到的**技巧性简便用法**单独成章：
`tools/gen_py_tricks.py` → 「技巧特训 · Python」30 题；`tools/gen_ds_tricks.py` → 「技巧特训 · C/C++」39 题。
难度 1→4 递进，四段式：基础语法糖 → 竞赛工具箱（STL/算法套路）→ 竞赛强度（DP/二分/分治）→ **进阶套路**。

| 线 | 分节 | 基础 | 套路 | 竞赛 | 进阶（10 题） |
|---|---|---|---|---|---|
| python | 技巧特训 · Python（8/6/6/10） | upper/负索引切片/split-join/推导式/enumerate-zip/sorted多关键字/dict.get/集合运算 | Counter/heapq/前缀和/**bisect 第一个大于 x**/lru_cache/回文清洗 | 01背包/LIS n log n/快速幂 pow(a,b,m)/区间合并/阶乘大数/筛法 | **str.translate(ROT13)**/re.findall/格式化四连 f-string/**zip(*a) 转置**/itertools 第 k 排列/math.gcd-lcm/**bit_count + lowbit**/**子集枚举 + 线性基**/**二维前缀和**/**deque 单调队列** |
| ds | 技巧特训 · C/C++（7/7/6/10 + **插入维护 4** + **整行反转 5**） | **vector push_back**/string find/sort+cmp/pair/map/set/stringstream | **upper_bound 第一个大于 x**/lower_bound/差分/双指针/单调栈/单调队列/**二分答案·伐木** | 01背包/完全背包/LIS/LCS/快速幂/逆序对归并 | **stable_sort 多关键字**/**priority_queue Top-K**/**next_permutation**/**accumulate + iota**/**bitset 位统计**/unordered_map 词频/**unique 离散化**/**树状数组**/**高精度字符串加法**/**前缀和 + 哈希计数** |

**整行反转 5 题（`getline` + `reverse` 区间，2026-10-20 加）**

| # | 标题 | 难度/分 | 练什么 |
|---|---|---|---|
| 1 | 按单词反转整行（getline + reverse 区间） | 1 / 10 | `cin >> s` 遇空格即停 → 必须 `getline`；扫到空格下标 `i` 直接当 `reverse` 的 `last`（**左闭右开**，空格不动） |
| 2 | 整句翻转（两次 reverse） | 2 / 15 | 整句翻 + 每词再翻：把「词序」和「词内序」同时倒两次，后者抵消；对比不用数组的两套写法 |
| 3 | 按分隔符逐段反转（i <= n 的收尾） | 2 / 15 | 循环必须 `i <= n`，只写 `i < n` **漏最后一段**；空段（`a,,b`）天然安全；分隔符用 `getline` 读，`cin >> c` 读不到空格 |
| 4 | 每 k 个字符分组反转（min 收尾防越界） | 3 / 20 | `min(i+k, n)` 是必须的 —— 越界是 UB；`k > n`、`k = 1` 两个边界 |
| 5 | 只反转字母（非字母原位不动） | 3 / 20 | 抽出字母串 `reverse` 再按 `pos` 填回；直接翻整串会带标点乱位；`isalpha((unsigned char)c)` 防负数 UB |

- ★ 这组题面里都写明了「为什么不能直接整串 `reverse`」和 `s.begin()+n == s.end()` 这个合法性前提。

**插入维护 4 题（`upper_bound` + `insert`，2026-10-19 晚加）**

| # | 标题 | 难度/分 | 练什么 |
|---|---|---|---|
| 1 | 有序表插入（upper_bound + insert） | 1 / 10 | `auto it = upper_bound(...); a.insert(it, x);` 两行模板；下标必须在 insert 前算（insert 后 it 失效）；insert 是 O(n) |
| 2 | 批量插入保持有序 | 2 / 15 | 循环插入 vs 先收完再整体排序的复杂度差（O(m·(n+m)) vs O(N log N)） |
| 3 | lower 与 upper 插入的稳定性 | 2 / 15 | 带 id 的记录插入：lower 插在相同值**前**、upper 插在**后**；只有 value 时两种结果长得一样 |
| 4 | 动态有序表的名次查询 | 3 / 20 | **插入用 upper、查询用 lower**；名次 = `it - begin() + 1`；不存在判 `it==end() || *it!=x` |

- ★ 每条都带「什么时候不该这么写」的说明，避免把 O(n) insert 当 O(log n) 用。

- ★ 独立文件 + seed/verify_bank 各加一行挂载，**不动另一窗口维护的 gen_ds_bank / gen_py_bank**。
- ★ oracle 用「笨办法」（如 LIS O(n²)、背包二维 DP）与参考解不同路；随机大用例用固定种子生成（可复现）。
- ★ 背包口诀写进题面：「倒序 = 0-1，正序 = 完全」。
- ★★ **标题必须全局唯一**（`seed.ensure()` 按 title 去重，跨科目也算重名）——「滑动窗口最大值」在 C++ 章节已用过，
  Python 那道只能改名「滑窗最大值（deque）」才进得了库（2026-10-19 踩到，表现为 ensure 少进 1 题）。
- 踩坑：oracle 里别写 O(maxH) 线性扫（10⁹ 的伐木用例直接卡死 198s）——oracle 也要用与约束匹配的复杂度。
  树状数组题的 oracle 用 √n 分块（独立实现），30000 组操作 ~2s；用暴力会 TLE 在生成阶段。

### ★ DS 经典题型编程题（2026-10-18 补，_oracle_44~56）

按三张经典题型图举一反三，难度 easy→medium 递进，全部「参考解 + alt 双撞」：

| 讲 | 题目（13 道） |
|---|---|
| 02 线性表 | 顺序表建立遍历 / 有序插入 / 合并有序数组（哨兵法 alt）/ 循环右移（三次逆置 + 下标映射 alt）/ 最大子列和（Kadane + 前缀和 alt）/ 单词逆置 / 头插法建链表 / 两有序链表合并（哑结点）/ 约瑟夫环 / 单链表建表与就地逆置 |
| 03 栈和队列 | 括号匹配检验 / 进制转换（递归 alt）/ 出栈序列的合法性 |

- ★ 约瑟夫环参考解曾因 **0 基 idx 与 1 基数组混用**死循环（`%n` 只走 0..n-1、数组填 1..n）→ 已改纯 0 基；ref+alt 均加 `m % 剩余人数` 折算（约束 m ≤ 10⁹，逐个报数必 TLE）。
- ★ 「单词逆置」「两表全空合并」的期望输出是**合法的 `"\n"` 空行**——`gen_ds_bank` 的空输出警示已放行 `"\n"`，仍拦截真空串。
- ★ 尚未覆盖的题型（下轮「举一反三」候选）：链表去重、两有序链表交集、重排链表、双向循环链表、猴子选大王、表达式转换（中缀转后缀）、后缀式求值、堆栈模拟队列、银行业务队列、全排列、直方图最大矩形、一元多项式乘加。
- `seed.py`：`SEED_PROBLEMS = CORE + BANK + DS + LINUX`；`SUBJECT_LABELS` 给三科目中文名；
  `_seed_specs()` 返回四元组 `(total, pts, section, subject)`，`backfill_points()` 同步 `subject`。

### ★ 题型分类（`app/question_types.py`，2026-10-15）

七类 `LABELS`：`single_choice` 单选 / `multiple_choice` 多选 / `true_false` 判断 /
`fill_blank` 填空 / `short_answer` 简答 / `programming` 编程 / `practical` 实操。

- **题型是题目的显式元数据，和 `subject`（科目）、`line`（提交方式）是三件不同的事。**
  老库靠 `infer()` 按「有没有选项 / 选项是不是对错 / `line` 是不是 text」兜底补标；
  **新题一律由题库自己盖章** —— `infer()` 不凭答案长短猜「简答」，更不许猜出「实操」。
- 入库路径：`seed.ensure()` 写 `question_type = infer(题库条目)`；
  `seed.sync_question_types()` 给老库补标（**种子题按题库同步，人工题保留已标类型，幂等**）。
  ★ 两条都是**读题库模块**，所以改完题库必须重新 seed 一次，否则库里还是旧标。

**判定口径（照这个对，别凭感觉）**

| 类型 | 判定标准 | Linux 线现状 |
|---|---|---|
| 单选 | 有 2~8 个选项，答案是**一个**字母 | 115 |
| 多选 | 有选项，答案是**两个以上**字母（库里按升序存，如 `AC`） | **8**（新补） |
| 判断 | 选项恰好是 `对 / 错` | 31 |
| 填空 | 一行文本答案、机器可判（术语 / 参数 / **单条命令**） | 25 |
| 简答 | 用自己的话讲要点，答案不唯一 | 0（Linux 线没有） |
| 编程 | `line != text`，交源代码给判题机 | 0（Python/DS 线的都是） |
| 实操 | 必须真在机器上按步骤做完才能答 | **15**（课程实验 1~5） |

- ★ **「填空」和「实操」的界线是「动不动手」，不是「答案长不长」**：
  「写出查看网卡名的命令」动脑就能答 → 填空；
  「装好系统、建好目录、改完权限，再把 `stat` 的输出贴回来」→ 实操。
  ★ 但实操题**不靠人工自评**：它仍然带测试点（验收命令的真实输出），
  所以线上线下都能判、能拿真分、进度也一致。详见下面「★ 实操题」。
- ★ **多选题的答案口径**（`app/bank_kit.py::multi()`）：
  1. 库里存**字母升序**串 —— 网页端是多选点选，字母按选项顺序拼，**天然就是升序**；
  2. 字母数 ≤ 3 时把**全排列**一并列为可接受答案（`AC` 与 `CA` 都认），
     免得 API 直接提交时把顺序写反白判一次 WA；4 个以上不列（24 种会把提示刷屏）；
  3. 分值 `SCORE_MULTI = 14`（比单选 10 高 —— 要对若干个才对）。
- ★ **多选题的验收点不是「答案判得过」，而是「漏选也必须判错」**：
  `selftest_theory.py` 把选项集合的**所有子集**穷举一遍（只选一个、多选一个、全选…），
  除了正确答案本身，其余必须全 WA —— 否则「只选一半也能 AC」等于这道题白出。

### ★ 命令题（实操题 = 给场景写命令，2026-10-19 晚重构）

#### 形态为什么改过

**旧形态（已废弃）**：题干给完整实验步骤 + 附一条**验收命令**，学生提交那条命令的**输出**。

能跑，但考错了东西：学生把实验做完，答案就是屏幕上复制一段文字，
**到底会不会写命令完全没被考察** —— 写不出命令的人照样拿分，
背下 `VERSION_ID=44` 的人甚至不用碰机器。

**现形态**：题干给**场景与约束**，提交**命令本身**。
会写就写得出，不会写就是不会 —— 这才是命令题该考的东西。

#### 判题怎么做到「宽容但不放水」

平台不执行提交内容（云端跑任意 shell 是 RCE），只做**文本等价比对**。
宽容度全压在两层：

| 层 | 做什么 | 位置 |
|---|---|---|
| 空白 | 多少空格、换行都折成一个 | `compare._squeeze_ws` |
| 标点 | 只剥排版类标点（全角、中文引号），ASCII 的 `. ' " ( )` 不动 | `compare._EDGE_PUNCT` |
| 短选项 | `-l -a` ≡ `-la`；`-la` ≡ `-al`（簇内字母排序去重） | `compare._norm_cmd` |
| 家目录 | `/home/<任意名>` ≡ `~` | `compare._norm_home` |
| 引号 | `'*.log'` ≡ `"*.log"` ≡ `*.log`（**仅当引号内无空白**） | `bank_kit._quote_forms` |
| 单字母 | `w` 也认 `W`（`runner_text` 会把单字母转大写） | `bank_kit.practical` |

★★ **自动归一化兜不住「真正的两套写法」** ——
`chmod 751 f` 与 `chmod u=rwx,g=rx,o=x f` 得在 `answers` 里手工都列上。
漏一条就是让人白掉一次分，所以每道题的备选都逐条核过参考解。

#### 203 道怎么组织（「举一反三」的落地方式）

`tools/linux_cmd_bank.py`，一族一个函数，**每族按同一套梯度出题**：

1. **基本用法** —— 最朴素的一条
2. **参数组合** —— 加两个选项，考「选哪个参数」
3. **真实场景** —— 不给命令名，只给需求，逼你自己选工具
4. **易错辨析** —— 同族两个近义命令/参数，选错就废

| 分节 | 题数 | 覆盖 |
|---|---|---|
| 实验 1~5 | 17 | 五份实验指导书的关键步骤（改写成命令） |
| 文件与目录 | 17 | ls / cp / mv / rm / mkdir / ln / readlink / truncate |
| 查看文件内容 | 13 | head / tail / wc / cat / less / file / tac / od |
| 查找与定位 | 16 | find 全家（-name/-size/-mtime/-perm/-exec）+ which/whereis/type/rpm -qf |
| 文本处理 | 22 | grep / sed / awk / cut / sort / uniq / tr / paste / diff / comm |
| 权限与属性 | 15 | chmod（数字+符号+特殊位）/ chown / chgrp / ACL / umask / stat |
| 用户与组 | 15 | useradd / usermod / userdel / passwd / id / su / visudo / lastlog |
| 进程与作业 | 18 | ps / pgrep / kill / pkill / nohup / jobs / bg / nice / top / lsof / pstree |
| 磁盘与存储 | 12 | df / du / lsblk / mount / blkid / iostat / inode |
| 压缩与打包 | 12 | tar 全参数 / gzip / zip / unzip / xz / 追加与部分解压 |
| 网络与远程 | 14 | ip / ss / ping / curl / wget / ssh / scp / rsync / DNS |
| 软件包与服务 | 14 | dnf / rpm -q* / systemctl / journalctl |
| Shell 与管道 | 18 | 重定向 / 变量 / alias / xargs / 算术 / if / for / set -e / awk 求和 |

分值按难度：1→10 / 2→12 / 3→15 / 4→18（`SCORE_BY_DIFF`）。

#### 铁律（改题库前必读）

- ★ **一道命令题只能有 1 个测试点**：`runner_text` 把**同一份提交**当作每个测试点的
  stdout，两个期望值不同的点，参考答案必然只能过一个。
- ★ **答案里不能出现换行**：期望值约定是「一行一个可接受答案」，
  答案自带换行的话第二行会被当成另一个答案。`practical()` 统一 `" ".join(x.split())`。
- ★ **单字母命令（`w`）要补大写备选** —— 已在 `practical()` 里自动补，不用记。
- ★ 改完 `linux_cmd_bank.py` 后必跑：
  `gen_linux_bank.py --check` → `verify_bank.py --linux` → `selftest_theory.py`
  → `test_question_types.py` → `export_static.py --with-cases` → `ui_test_linux_user.mjs`。
- ★ **改老题（含删题）后必须重 seed**，否则库里还是旧版本。
  `ensure()` 只插不改；删题还要**手工删 `testcases`**（本次删 15 道旧实操题就是这么做）。

### ★ Linux 登录名 `{user}`（2026-10-19）

题面与解析里出现「你的家目录」这种东西时，**绝不能写死作者自己的登录名**。
现在统一走占位符：

1. 题库里写 `{user}`（例：`/home/{user}/docs`、`User {user}`）。
   **只出现在 `statement_md` / 解析里，绝不出现在 `expected_stdout`**。
2. 前端第一次打开 Linux 题时弹卡片要登录名（`pta.linuxUser`，存在 localStorage），
   没填就**不让交**（`readTheoryAnswer()` 会拦）；题面顶部常驻一行
   「本机登录名 `xxx` · 家目录 `~/` 就是 `/home/xxx`」。
3. `mdRender()` 开头统一 `subUser()` —— 题干、输入输出格式、选项、格式提示全走这条路。
4. **判题完全不需要知道名字**：答案只认 `~/...`，
   `compare._norm_home()` 会把 `/home/<任意登录名>` 折成 `~` 再比。
   JS 侧 `web/judge_text.js` 有同款 `normHome()`，两边靠 `verify_text_judge` 对拍守住。
   - 前提：**一道题的答案里不会出现两个不同用户的家目录**（题库里没有这种题）；
     真要出，这条归一化会把区分抹掉。
- ⚠️ 界面**目前没有「题解」展示位**（解析只入库、不渲染），所以 `{user}` 在解析里
  暂时看不见；真正看得见的是题面顶部那行环境提示。

### ★ `tools/sync_bank_cases.py`（改老题答案后必跑）

`seed.ensure()` **只插入不改已有题** —— 改了一道老题的答案，库里还是旧的，
而 `verify_bank` / `export_static` 读的是**库**，于是你改完一验全绿、导出却对不上。

```bash
python tools/sync_bank_cases.py --subject linux --title "某道题" [--title ...] --apply
```

- 必须 `--title` **点名**，工具刻意不提供「整条线一把梭」：
  库里有些题的答案**比题库模块多**，那是 `seed.backfill_choice_alts()` 补的
  「选项正文也算答案」，整条线覆盖会把这些悄悄冲掉。
- `--apply` 之后会自动再跑一遍 `backfill_choice_alts()` 把它们补回来（幂等）。

### ★ 加题铁律「三件套」

1. `expected_stdout` 必须**由另一套独立实现预先算出** —— 绝不拿参考解现跑现填（那是自己给自己判卷，永远满分、毫无意义）。
2. 每题必带 `alt_solution`（第二套独立实现），**两套都要撞过全部测试点**。
3. `tools/verify_bank.py` 逐字节对拍。

- ⚠️ `alt_solution` **不入库** —— `seed.ensure()` 必须 `spec.pop("alt_solution", None)`。
- ⚠️ `verify_bank.py` 里**同一套解复用同一目录**，整轮只删 4 次 —— 若每题都删目录会累计 100+ 次 > 阈值 50，被 `SAFE_DELETE_BULK_CONFIRM_REQUIRED` 拦停。
- ⚠️ `verify_bank` 的临时目录**必须落在判题根目录之外**（用 `data/tmp/verify_bank/`）。
  若住在 `data/tmp/judge/` 下，服务启动时的 `clean_tmp_root()` 会把编译产物顺手删掉，表现为一连串 `can't open file ... main.py` RE。
  **别把对拍和判题服务同时跑。**

### 生成器

`tools/gen_ds_bank.py` / `tools/gen_linux_bank.py`，各带 `_sanity()` 把关（必填字段 / 标题重复 / `line` / `checker` / **理论题样例必须为 0**）。

- `_dump()` 输出 Python 字面量（把 JSON 的 `null`/`true`/`false` 换掉）。
- ⚠️ 生成器里**不能把 `def oracle` 写进 `add(...)` 的实参列表** —— `def` 是语句不是表达式，整份文件一行都跑不了。

### ★ 第 11 ~ 16 讲题库（2026-10-15 补，第三部分「Linux 平台上的程序设计」）

`gen_linux_bank.py` 里新增 `part_lectures_c()`，六讲共 **54 题**：

| 讲 | 主题 | 题数 | | 讲 | 主题 | 题数 |
|---|---|---|---|---|---|---|
| 11 | Shell 程序设计 | 6 | | 14 | Qt 图形界面 | **12** |
| 12 | GCC 的使用与开发 | **12** | | 15 | Python 程序开发环境 | 6 |
| 13 | GTK 图形界面 | **12** | | 16 | Eclipse | 6 |

- **重点讲（12 / 13 / 14）加倍** —— 那三讲是第三部分的硬骨头（四道工序 / 链接顺序 / moc / moc 与 vtable）。
- 题源：各讲的「**一分钟速览**」+「**附录 A · 陷阱清单**」——
  后者每条本来就是讲义里已核过的结论（本机实跑 / 官方文档 / 包仓库），不是现编的。
- ★ **加题入库三步**（少一步就出错）：
  1. 改 `tools/gen_linux_bank.py` → 跑它（会重写 `app/problems_bank_linux.py`）；
  2. **跑一次 seed 把它灌进本地库**：`db.init_db()` → `seed.ensure()` → `backfill_points()`
     → `backfill_choice_alts()`（幂等，只新增，不删改）；
  3. `export_static.py --with-cases` 重导 `docs/`。
- ⚠️ **第 2 步最容易忘，而后果最隐蔽**：`verify_text_judge.py` 和 `export_static.py`
  **读的是数据库，不是题库模块** —— 忘了 seed 的话这两个脚本看到的还是旧题量，
  而且**不会报错**（表现为「明明加了题，静态站上却没有」）。
- ★ 判题口径的两个数字会自动跟着涨（**别写死**）：`verify_text_judge` 现在是 **195 题 / 5785 条**，
  `selftest_theory` 是 **115 道单选 + 8 道多选**（多选另把选项集合的全部子集穷举一遍）。
- ★ 其中**第 11 讲的 6 道全部进了 `verify_theory_facts.py` 的可实证名单**（ID 205~210）——
  bash 语法不依赖发行版，本机能真跑出事实再对答案键。

### 理论题样板工厂 `app/bank_kit.py`

- `mc()` / `tf()` / `fill()`；分值 `SCORE_CHOICE=10` / `SCORE_JUDGE=8` / `SCORE_FILL=12`。
- 理论题 `is_sample` **恒为 0** —— 样例会在静态站公开，对选择题来说就是**把答案印在题面上**。

### ★ 补 `alt_solution` 的可靠姿势

2026-10-13 用这套流程给 14 道老题补上了第二套实现，值得复用：

1. 先写一份 `{标题: 源码}` 表放在 `data/`（不进 git），**逐测试点验证对齐现有期望输出**；
2. 全部对齐后，再按 `"title": "..."` 正则定位到本题字典，在 `"cases": [` 之前插入用 `json.dumps` 生成的字面量；
3. 跑第二遍确认**幂等**（已有 `alt_solution` 的跳过）。

⚠️ 定位正则必须 `ensure_ascii=False`，否则中文标题会被转成 `\uXXXX` 而匹配不到。

「独立」的判断标准（写 alt 时逐题自查）：

| 题目 | 参考解 | 第二套实现 | 独立在哪 |
|---|---|---|---|
| 区间求和 | 等差数列公式 | 前缀和相减 | 不同推导（暴力 `sum(range())` 在 2e9 宽度上会 TLE，不能用） |
| 判断闰年 | 手写四条判断 | `calendar.isleap` | 换实现来源（标准库） |
| 素数判断 | `while` 试除 + break | `all()` + `int(n**0.5)` 上界 | 换控制结构 |
| 单词计数 | `str.split()` | 正则 `\S+` | 换 API |
| 去重保序 | `set` + 循环 append | `dict.fromkeys` | 换数据结构 |
| 第 k 大 | 整体降序排序取 `[k-1]` | `heapq.nlargest` | 换算法 |
| 词频统计 | 单趟 `sorted(key=(-次数, 单词))` | **两趟稳定排序** | 复合键 vs 稳定性利用（⚠️ **不能用 `Counter.most_common()`**：它同频时按插入顺序，第 5 个测试点会挂） |
| 最大公约数 | 手写欧几里得 | `math.gcd` | 换实现来源 |
| 斐波那契 | 双变量迭代滚动 | `lru_cache` 记忆化递归 | 自底向上 vs 自顶向下 |

## C / C++ 双通道（数据结构线）

- 同一道题 **C 与 C++ 任选提交**：按提交里的 `lang` 选编译器与源文件后缀。
  `c → gcc + main.c + -std=gnu11`，`cpp → g++ + main.cpp + -std=c++17`。
- ★ **两条路的可执行文件必须分开命名**（`main_c` / `main_cpp`）——
  否则同一目录里先编 C 再编 C++，第二次会「跑了上一次的产物」。`selftest_cpp.py` 有一项专门盯这个：先编 C++ 跑、再编 C 跑、再跑 C++ 的产物，必须还是 `I_AM_CPP`。
- **编译阶段单独给额度**：`COMPILE_MEMORY_MB = 1024` / `COMPILE_TIME_MS = 20000`。
  **不能套用题目的 256 MB** —— g++ 自己就要吃几十上百 MB，会表现为莫名其妙的 CE。
- `app/judge/runner_cpp.py`：`LANG_SPECS` + `LANG_ALIAS`（`c++`/`g++`/`c99`/`c11`/`gnu11`… 全收敛）+ `canon_lang()`；`CppRunner = CompileRunner` 保留旧名。
- `worker.build_runner()` 按 `python | text | canon_lang` 三分支分发。
- `Dockerfile` 里必须装 `gcc g++ libc6-dev` —— 原来的基础镜像没有编译器，云端数据结构题会全部 CE。

## 理论题判题（Linux 线）

- `app/judge/runner_text.py`：`TextRunner` **不启子进程**，把提交文本当 stdout 交回，
  后面的 compare / scoring / 历史 / 进度**全部复用**，判题逻辑一行没另写。空答案**不报 CE**（判 WA 更诚实）。
- `normalize_answer()`：去首尾空白与标点 → 判断题收成「对/错」→ 单 ASCII 字母转大写 → 剥掉「选 B」「答案：B」的**前缀**。
- **`oneof` checker**：期望值里以 `|` 开头的每一行都是可接受答案，命中任意一个即通过。
  `_uses_oneof()` 要求**必须真的有 `|` 行**（否则空备选清单会把所有答案都判错）。
  `seed.backfill_choice_alts()` 把选择题的**选项正文**也补成可接受答案 → 前端交字母、交正文两条路都通。

### ★★ 命令题宽容口径：ASCII 标点绝不能剥

`_norm_cmd()`：空白折叠 + 相邻短选项合并（`-l -a` → `-la`）+ 簇内字母排序去重（`-lah` → `-ahl`）。
**刻意不碰**长选项、带数字的、带参数的 —— 合并会改语义。

踩过的坑：`runner_text._EDGE` 里含 ASCII 的 `.` `'` `"`，`normalize_answer` 统一 `strip()` 掉，于是

| 参考答案 | 被判成 | 少了什么 |
|---|---|---|
| `cd ../..` | `cd ../` | 末字符 |
| `echo -n "hello everyone!"` | 少了结尾的 `"` | 引号 |
| `dnf provides '*/ls'` | 少了结尾的 `'` | 单引号 |

**这三个字符在命令行里是有意义的。** 修法：

- `_EDGE` 只用来**识别「这是不是一个选项字母」**，识别完只返回那个字母，绝不拿它裁长答案；
- 宽容挪到 `compare.answer_forms()`，只剥**排版类**标点（全角、中文引号、顿号…），且作为**额外**形式加进去，不在原答案上裁。

### ★ 反方向测试必须有

`verify_bank` 只证明「正确答案判得**过**」—— 一个过宽的 checker 会让所有题都满分而它依然报「全部通过」。

`tools/selftest_theory.py`（14 项）负责证明「错误答案判得**错**」：

- 逐题试**单选题其余每一个选项**（115 道）
- 判断题双向
- 命令填空的宽容度
- **全库扫三条**：每道题的参考答案都判得过自己 / 期望值里每条可接受答案都判得过 / 乱写加料仍判错

### ★★ 浏览器端判题（`web/judge_text.js`，2026-10-14）

理论题没有「可执行的东西」—— 用户交的就是答案本身，判题 = 字符串归一化 + 比对。
所以这件事**浏览器完全干得了**，不需要任何后端。于是把上面这套口径**逐字移植成 JS**，
让 GitHub Pages 那份纯静态站在没有后端时也能判题。

- **口径零重写**：`app/judge/compare.py` 是纯逻辑（只依赖 `re` + `dataclasses`），
  移植时按原函数逐个对着写 —— `normalize_answer` / `answer_forms` / `_norm_cmd` /
  `oneof_alternatives` / `_uses_oneof` / `compare` / `scoring.grade` 一个不落。
- ★★ **口径分叉是这里最大的风险**，而且极其隐蔽：大多数答案仍然判得对，只在边角处悄悄不一致。
  所以配了 `tools/verify_text_judge.mjs` —— 题库全部 **195 道理论题 × 多种答案 = 5785 条**，
  在 JS 侧跑一遍、在 Python 侧（**真实实现**，不是另写一套「差不多的」）跑一遍，
  逐字段比对 verdict / score。现状：**5785 条全部一致**（3127 AC / 2658 非 AC —— 正反两面都有，不是恒真）。
  改 `judge_text.js` 之后必须重跑它。

移植时踩到的坑（都写在文件头了）：

| 坑 | 说明 |
|---|---|
| Unicode 空白**不等价** | Python `str.split()` / `strip()` 认的是 `Py_UNICODE_ISSPACE`；JS 的 `\s` **多了 `\ufeff`、少了 `\x1c`~`\x1f` 和 `\x85`**。用显式字符类把 Python 那张表抄下来。 |
| `strip(chars)` 按**码点**剥字符集合 | 不是按子串。得用 `[...s]` 展开码点，用下标会在非 BMP 字符上错位。 |
| 带 `g` 的正则 `.test()` 会记住 `lastIndex` | 「只看单字符是不是空白」的那个正则**绝不能带 `g`**，否则连续调用时对时错。 |
| 块注释里的 `*/` | 注释里写 `'*/ls'` 会**提前闭合块注释** → 整个文件语法崩。 |

文件是 UMD：浏览器挂 `window.TextJudge`，Node 里 `require` 得到同一个对象（对拍脚本用）。

**离线本地判题的边界（2026-10-15 更新）**：最初只有 `line === 'text'` 的题（Linux 线 179 道）能本地判；
现在 **三条线都能在浏览器里判** —— 理论题走 `judge_text.js`，Python 走 **Pyodide**（`web/pyodide/`，约 13 MB，随仓库分发）、
C/C++ 走 **Clang/WASI**（`web/clang/`，约 29 MB，随仓库分发），引擎全部**从本站加载、零 CDN 依赖**。
后端从「必须」变成「可选增强」：跨设备进度、更准的 GCC 环境、防作弊。

### ★★ 引擎下载被掐：失败态绝不能缓存（2026-10-15 线上踩到）

C/C++ 编译器 `clang.wasm.gz` 有 **15.7 MB**，真实用户下载中途被掐
（fetch 流报 `network error`）→「评测机内部错误」。下载失败本身拦不住，
**真 bug 是 `cpp-worker.js` 把 rejected 的 `toolchainPromise` 缓存住了** ——
之后每次点「提交并判题」都瞬间失败，唯一出路是刷新整页。

- 修法与编辑器那次同款：`createToolchain(...).catch(e => { toolchainPromise = null; throw e; })`。
  这是本项目**第二次**踩「失败态被永久缓存」这个坑（第一次是编辑器的 `smartEditorLoad`）——
  **任何 `if (!p) p = somethingAsync()` 的写法都要配 catch 清缓存。**
- Python 侧（`python-local.js`）本来就写对了：`ready` 失败即置 null，重试会起新 worker。
- 顺手把英文报错翻成人话（`localJudgeHint` / `friendlyLoad`）：「下载中断了，再点一次就会重新下载，不用刷新页面」。
- 回归测试 `tools/ui_e2e_local_engines.mjs`（C/C++ 5/5；Python 两项本机环境跳过）：本地服务器**故意掐断**第一次传输（先给 1 KB 正文再 destroy，
  比 404 更接近真实故障），断言 IE + 提示 → 重试 → 引擎重新下载并真判出来。

## 自检脚本

| 脚本 | 项数 | 说明 |
|---|---|---|
| `selfcheck.py` | **62/62** | 内核 41 + 评分 21 |
| `selftest_sandbox.py` | **19/19** | 超时杀孙进程、爆内存判 MLE、`exit(1)` 反向不误判、**MLE 判据矩阵（7 项纯函数断言）** |
| `selftest_cpp.py` | **9/9** | C/C++ AC·CE·WA·TLE、**同目录产物不串**、编译器路径无效给人话、别名收敛 |
| `selftest_theory.py` | **15/15** | 115 道单选其余选项全判错、**8 道多选穷举全部子集**、判断题双向、命令宽容度、全库扫 |
| `smoke_cloud.py` | **13/13** | **云端启动路径**：真起 `python run.py`（`PTA_CLOUD=1` + `$PORT`）、绑 0.0.0.0、三科目齐、**真编 C++ / 真跑 Python 各 AC 一次** |
| `e2e_ui.py` | **33/33** | 端到端过 HTTP（**需先起服务**）。期望值（总分 / 题数 / 分组数 / 列表顺序 / 目标题 id）全部**从题库定义现算**，不写死。2026-10-16 修好，见文末 |
| `ui_smoke.mjs` | **41/41** | jsdom 真渲染前端（离线 + 假后端两遍） |
| `ui_test_local_judge.mjs` | **45/45** | 离线本地判题：**真 jsdom + 真加载 `judge_text.js`**（专门起静态服务，让外链脚本真被取到）。含「答对后再答错最高分不被冲掉」「导入低分备份不冲掉高分」两条回归 |
| `ui_e2e_local_judge.mjs` | **25/25** | **真 Chrome**（puppeteer-core + 系统 Chrome）跑 `docs/` **发布产物**：真点按钮判题、**真下载**进度 JSON、**真上传**导入回来 |
| `ui_e2e_local_engines.mjs` | **5 通过 / 2 跳过**（本机环境拦 `.zip`，详见文末） | ★★ **浏览器判题引擎的「下载被掐 → 重试恢复」回归**：本地伺服 `docs/`，第一次故意掐断 `clang.wasm.gz` / `pyodide.asm.wasm` 传输（模拟线上 2026-10-15 的 `network error`），断言第一次判 IE + 有人话指引、**重试后引擎重新下载并真判出来**（Python A+B 浏览器内满分；C++ 真编译运行判 WA）。这也是浏览器 C/C++ 判题的第一条端到端测试 |
| `ui_e2e_editor.mjs` | **63/63** | ★ **真 Chrome 测智能编辑器**（唯一真敲键盘的测试）：三种语言的缩进 / 配对 / 补全 / Tab / Shift+Tab / `Esc`+`Tab` / 切题草稿 / C↔C++ 语言切换 / 加载失败回退 |
| `ui_e2e_notes.mjs` | **29/29** | ★ **真 Chrome 测笔记区**：目录树导航、双链跳转（含**重名消歧**）、带锚点的链接定位、折叠答案（`<details>`）展开、全文搜索（首次拉 3 MB 索引）、上下节导航、**题目 ↔ 笔记双向互跳**、零外部主机。跑之前先 `export_notes.py` 再 `export_static.py` |
| `httptest_users.py` | **23/23** | 多用户隔离、越权 404、CORS |
| `httptest_mastery.py` | **39/39** | 收藏 / 掌握度 / 备注：增量更新不互相冲掉、**收藏不冒充做过（attempts 仍 0）**、错题由「做过但没满分」算出、多用户隔离、参数越界全 400、老接口不回归。自带起服务（测试库）+ 随机 token，可重复跑 |
| `ui_e2e_wrongbook.mjs` | **23/23** | ★ **真 Chrome 测错题本**，两轮：① 在线（真 uvicorn + `/api` 反代）——点星、写备注、**刷新后备注还在**（= 真进库）、掌握度、题面收藏与备注、删备注归零；② 离线（只服务 `docs/`）——收藏与备注靠 localStorage，刷新不丢。零 JS 报错 |
| `httptest_split.py` | **18/18** | Pages + 后端跨源（OPTIONS 预检 / 允许 x-user-token） |
| `httptest.py` | **18/18** | HTTP 层（需服务已在跑） |
| `verify_bank.py` | **333 题 / 791 点全过** | 三线双实现；`--py` / `--ds` / `--linux` 可单跑 |
| `show_text_judge.mjs` | **全过** | 本地判题器的「行为说明书」：多种等价写法都认、变异错答案 71/72 被抓、309 个标准答案全 AC、351 个胡写全 WA |
| `verify_theory_facts.py` | **45 过 / 0 不符 / 8 无法核验** | **理论题答案的实证核验**：179 道理论题里凡本机（Git Bash GNU coreutils 8.32 / GNU tar 1.35）能跑的，先跑出事实再对答案键；跑不了的如实列「无法核验」。**抓到过真 bug**：91/100 题的 explanation 曾写「`head -n +N` 报错」「`tail -n -N` 非法」——GNU 上全都不成立（`+N` 就是前 N 行；`-N` 归 tail 是最后 N 行），已改 |


> ★ **jsdom 的两个测试**（`ui_smoke.mjs` 41/41、`ui_test_local_judge.mjs` 45/45）需要 jsdom：
> 已作为 devDependency 装进 `pta/node_modules`。跑的时候指一下路径 ——
> `NODE_MODULES_DIR="E:/学习/001/pta" node tools/ui_smoke.mjs`（Windows 下反斜杠亦可）。
> **必须给绝对路径**：写 `.` 会让 ESM loader 直接抛 `ERR_INVALID_ARG_VALUE`，
> 而没装 jsdom 时脚本只吐一句「找不到 jsdom」就退出（容易被误当成「测试没跑」而漏掉）。

跑 `e2e_ui` 的正确姿势（**用测试库，绝不碰真实库**；⚠️ 本机要带 `NO_PROXY`，见下节）：

```bat
set PTA_DB=E:\学习\001\pta\data\_bank_test.db
D:\Pythontools\Python\python.exe -m uvicorn app.main:app --port 8792
set NO_PROXY=127.0.0.1,localhost
D:\Pythontools\Python\python.exe tools\e2e_ui.py 8792
```

它每轮用**新通行证**（进度是按人存的，复用同一个 token 会让断言被上一轮污染）。

### ★★ `selfcheck.py` 默认改用测试库（2026-10-13 修）

`selfcheck.py` 会 `db.insert` 一批测试提交（AC / WA / RE / TLE / CE / MLE 各一条，共 **11 条**）。
它原来默认连的是**真实库** `data/pta.db` —— 于是每跑一次就往用户记录里多 11 条假提交。

真踩了：一天里跑了三次自检，真实库的 `submissions` 从 11 涨到 **33**。
三批数据的指纹一模一样（verdict 顺序、code 长度逐一对应、时间戳都在十几秒内连续），
一眼能认出不是人做题的节奏 —— **但用户打开「我的提交」会莫名其妙多出一堆自己没写过的代码。**

修法：在 `config.get()` **之前**（配置是读取时定格的）把 `PTA_DB` 指到 `data/_bank_test.db`；
要对着真实库跑就显式加 `--live`，脚本会在表头把数据库路径和警告打出来。

只改了 `selfcheck.py` —— `selftest_cpp` / `selftest_theory` / `selftest_sandbox` 都是
**只编译只运行、不碰数据库**的，已核对过。`httptest*.py` 走真服务，写哪个库取决于服务连的库
（起服务时用 `PTA_DB` 指过去就行）。

### ★★ 又踩了一次：`httptest_users` 也连真实库（2026-10-14 修）

上面那条「`httptest*.py` 起服务时用 `PTA_DB` 指过去就行」是**嘴上说说**，代码里没人做。
结果 2026-10-14 清空真实库之后跑了一遍回归，真实库又长出
**2 条提交 + 2 个测试账号**（`aaaa1111…` / `eeee5555…`，14:05:39 那批）。

两个坑叠在一起：

1. `httptest_users.py` / `httptest_split.py` 起服务时只 `dict(os.environ)` 复制了一份环境，
   **没设 `PTA_DB`** → 服务连真实库。
2. 脚本**自己**也 `from app import db`（要查 `users` 表）→ 连的也是真实库。
   所以是「测试进程 + 服务进程」双双写真实库。

修法：新增 `tools/_testdb.py`，**导入即生效**地在 `config.get()` 之前把 `PTA_DB` 钉到测试库。

为什么必须是「导入即生效」而不是「`main()` 里设一下」：
`app/config.py` 的 `db_path` 是**读取时定格**的（第一次 `config.get()` 从环境变量取值，
之后再改环境变量也没用）。放在函数里太晚。

配套的三条规矩：

| 脚本类型 | 该怎么做 |
|---|---|
| 自己 `Popen` 起服务（`httptest_users` / `httptest_split`） | import `_testdb`，**并且把 `PTA_DB` 显式塞进子进程 env** —— 子进程不继承「父进程 import 过什么」，只认 `os.environ` |
| 只连已有服务（`e2e_ui` / `httptest`） | 不设 `PTA_DB`（服务在别人手里），但要先读 `/api/health` 的 `db` 字段，用 `guard_live_db()` 大声警告 |
| 本来就是操作真实库的（`export_static` / `backup_db` / `reset_progress`） | **绝不**import `_testdb` |

### ★ `httptest_users` 的可重复性（2026-10-14 修）

两个连带问题，都是「换了测试库之后才暴露」的：

1. **非幂等**：脚本用**固定通行证**，还断言「A 的历史条数 = 1」。
   以前它在真实库上跑、跑完真实库被清掉，所以看不出问题；
   改用持久的测试库之后，第二次跑必定数到上一次留下的记录 → 假失败。
   → 加 `_testdb.fresh_test_db()`：开跑前把测试库**删掉重建**
   （schema 不用管，`app/db.py` 的 `connect()` 会自己建表）。
2. **等待时限刚好卡边界**：删库重建后服务要重新播种 861 题 / 1819 个测试点，
   本机实测约 40 秒，而 `wait_port` / `wait_http` 的默认上限**正好是 40 秒**。
   → 提到 120 秒。

### ★ `httptest_split` 里三条过期的前端断言（2026-10-14 修）

前端重写成 PTA 风格之后，这个脚本的断言没跟着改，于是长期假失败：

| 旧断言 | 现实 |
|---|---|
| `problems.json` 的 `count == 56` | 题库早就 308 题了 → 改成**对着 `docs/problems.json` 自己数一遍**，别硬编码 |
| HTML 里有 `pta.backend` | 新前端的键是 `pta.apiBase` |
| HTML 里有 `get("api")` | 新前端是 `new URLSearchParams(location.search).get('api')` |

> 教训：**断言里的数量都是定时炸弹**。凡是「应该等于 N」的地方，
> 优先写成「和权威来源比一遍」，而不是写死一个数。

## 环境与工具的注意事项

其它注意事项：

- ⚠️ `ui_smoke.mjs` 用 `createRequire` + `NODE_MODULES_DIR` 环境变量定位 jsdom（ESM `import` 找不到）。
- ⚠️ 日志**不要写 `/tmp`**（触发安全策略 SIGTERM），写项目目录（如 `data/vb.log`）。
- ⚠️ 后台跑的脚本**重定向到文件时输出是全缓冲**，跑完才落盘 —— 别拿「日志还是 0 行」当失败。
- ⚠️ 本机 curl 报 `CRYPT_E_REVOCATION_OFFLINE` → 加 `--ssl-no-revoke`。
- ⚠️ **git push 也会撞 `CRYPT_E_REVOCATION_OFFLINE`**（2026-10-15 起出现过一次；昨天还好的，
  疑似杀软 TLS 拦截/系统代理波动）。`-c http.schannelCheckRevoke=false` **不生效**，
  有效的是换 openssl 后端：

  ```bash
  git -c http.sslBackend=openssl \
      -c http.sslCAInfo="C:/Program Files/Git/mingw64/etc/ssl/certs/ca-bundle.crt" push ...
  ```
- ⚠️ **`HTTP_PROXY` / `HTTPS_PROXY` 会被注进环境**（端口每次不一定一样，2026-10-14 实测是 `127.0.0.1:51814`）。
  curl 测本机端口用 `--noproxy '*'`（`"*"` 在 Git Bash 里会被 glob 展开，要加单引号）。
- ★★ **Python `urllib` 同样会走它** —— 笔记里原先写的「urllib 实测能直连、不受影响」**是错的**
  （2026-10-14 翻案）：`tools/e2e_ui.py` 打 `http://127.0.0.1:8792` 被代理接走，报 **502 Bad Gateway**
  —— 不是「连不上」，很容易误判成「服务挂了」。跑任何打本机端口的脚本都要带：

  ```bash
  NO_PROXY=127.0.0.1,localhost no_proxy=127.0.0.1,localhost python tools/e2e_ui.py
  ```

  `e2e_ui` / `httptest_*` / `selfcheck` / `smoke_cloud` 全都要加。
- ⚠️ **Windows 自带 bsdtar 陷阱**：`subprocess.run(["tar", ...])` 不经过 bash 时拿到的是
  System32 的 `tar.exe`（bsdtar 3.8.8），行为与 GNU tar 1.35 有差异。要 GNU 版一律
  `subprocess.run(["bash", "-c", "tar ..."])`（`verify_theory_facts.py` 就这么做）。
- ⚠️ **MSYS 上符号链接与 chmod 不可信**：`ln -s` 会被降级成副本（`[ -L ]` 为假），
  且同一命令在不同启动方式下行为不一致（一次建出真链接、一次降级）；`chmod 700`
  落成 644（ACL 近似映射）。凡是涉及权限位/符号链接的「实证」，在这台机器上做不了，
  如实降级成「无法核验」，别硬验。

## 前端（PTA 风格）

- **三层 hash 路由**：`#/` 题集广场（hero 总分进度 + 科目卡片）→ `#/set/<subject>` 题集内（状态筛选 + 搜索 + 按 `source_section` 分组折叠表格）→ `#/p/<id>` 题目页（左题面右编辑区）。另有 `#/subs` 我的提交、`#/notes` 笔记区、`#/wrongbook` 错题本。
- ★ **科目独立编号（2026-10-18）**：每科从 1 起独立编号 —— `SUBJ_PREFIX={python:'PY',ds:'DS',linux:'LX'}` + `buildSubjSeq()`（PROBLEMS 排序后按 科目→讲次→id 现算 `SUBJ_SEQ[id]`）。表格与题面角标显示 `DS-12` 这类编号，**全局 id 只活在链接与 `data-pid` 属性**——脚本里别再拿角标文本当 id 用（`ui_e2e_editor.mjs` 已改成比 `dataset.pid`）。
- 题目页按 `is_choice` 分支：选择题渲染可点选项圆标（**提交选项字母**）、判断题提交「对/错」正文、填空题 textarea、编程题按 `langs` 给 C/C++ 下拉。
- **`GET /api/catalog`** 一次请求给出「科目 → 分组 → 题数 + 我的进度 + 总分」，前端不用拉全库自己聚合。
- **离线降级**：连不上后端就读 `problems.json` + `localStorage`，拼成和在线一样的 CATALOG。
  - ⚠️ 静态快照**不含 `langs`** → 前端有一份 `LANG_OPTIONS` 本地副本，否则离线时语言下拉是空的。
  - ⚠️ 启动必须 `loadMeta → loadProblems → loadCatalog` **串行** —— 离线兜底要从题库现聚合，并行会拿到空题库（首页 0 张卡片）。
- **离线本地判题**（2026-10-14）：离线 + `line === 'text'` + 题库带了 `cases` 时，按钮从
  「标记为已掌握」换成「提交并判题」，走 `web/judge_text.js` 现场判分。
  判题结果**直接复用同一套 `renderResult`** —— `TextJudge.judgeTextProblem()` 的返回字段与后端
  提交结果**完全对齐**（verdict / score / max_score / passed / total / cases[]），所以显示层零改动。
  在线时仍然走后端，不会被本地判题抢走（`ui_test_local_judge.mjs` 的 [5] 专门守这条）。
- ★ **本地进度取历史最高分**：`setLocalProgress()` 默认 keep-max。本地判题会反复写它，
  直接覆盖的话「答对之后再交一次错的」会把「已掌握」冲掉（后端口径也是取最高分）。
  手动标记的「部分掌握」要的就是强制改值，所以走 `{force:true}`。
- **设置里有「导出进度 / 导入进度」**（JSON 含进度 + 草稿 + 通行证）。导入按**取最高分**合并，
  绝不覆盖已有高分。离线判题的进度只活在这台设备的 localStorage 里 —— 这是它唯一的安全绳。
- 理论题取答案抽成 `readTheoryAnswer()`，在线（`doSubmit`）与离线（`doSubmitLocal`）两条路共用，
  免得各写一份而分叉。
- 离线横幅里的「N 道理论题可本地判」是**现算的**（`PROBLEMS.filter(...)`），不是写死的数字。
- 分组折叠用**下标传参**（`toggleGroup(i)` + `GNAMES`），避免题目名字里的引号打断内联 JS。
- `prefers-color-scheme` 双主题。
- ⚠️ `Write` 工具对**未 Read 过的已有文件**会报 `File has not been read yet` —— 要么先 Read，要么先 `cp` 备份再 `rm` 腾路径。

## 智能编辑器（CodeMirror 6，2026-10-15）

把编程题的代码框从 `textarea` 换成**自托管 CodeMirror 6**：不连 CDN、不调 AI、不需要后端，
纯静态站打开就能用（理论题保持原输入框不动）。

```
editor-src/index.js  ──esbuild──▶  web/editor/editor.js  ──export_static──▶  docs/editor/editor.js
   （约 6 KB 源码）                  （约 500 KB，进仓库）                   （Pages 用）
```

- `web/index.html` 里 `smartMountEditor()` 动态 `import('./editor/editor.js')` → `mountEditor({parent, doc, lang, onChange})`；
  任何一步失败就回退到原来的 `textarea`，功能不受影响。
- 只对 Python / C / C++ 题挂载；`line === 'text'` 的理论题不走这条路。

### 关键实现点

| 需求 | 做法 |
|---|---|
| Tab 三种含义 | keymap 用 `Prec.highest` 抢在默认键位之前：有补全 → `acceptCompletion`；有片段占位符 → `nextSnippetField`；否则 `indentMore` |
| `Esc` 后按 Tab 离开编辑器 | `Escape` 关补全面板时置「刚按过 Esc」标志，下一次 `Tab` 直接 `blur()` 把焦点放出去（键盘可全程操作） |
| 切 C↔C++ | `Compartment.reconfigure` 只换语言扩展与补全源，**代码不清空**，草稿 / 提交 / 自测 / 分栏高度都不变 |
| 括号 / 引号配对 | `closeBrackets()`（含「选中文字再敲括号或引号 → 直接包起来」） |
| 补全提示 | `autocompletion({override:[本地 source]})`，source = 代码片段（`snippet()`）+ 本地关键词词表，**零网络、零 AI** |

### ★★ 踩过的坑（都钉进 `ui_e2e_editor.mjs` 了）

1. **CodeMirror 没有单独的 C 语法** —— `@codemirror/lang-cpp` 一个 grammar 同时服务 C 和 C++。
   所以 **C↔C++ 切换时高亮本来就不变**，真正跟着变的只有补全源与片段。
   想验「高亮跟着语言换」必须**跨语言比**（Python ↔ C++）。第一版测试断言 C↔C++ 高亮不同 → 假失败。
   顺带：判据也不能用「有没有着色 span」——`defaultHighlightStyle` 里 `definition(variableName)` 会让普通变量名也有样式。
2. **`acceptCompletion` 有 75 ms 的 `interactionDelay`** —— 面板刚弹出就按 Tab 会被拒。
   真人不这么快，**测试脚本会**。测「Tab 接受补全」之前必须等够 100 ms。
3. **puppeteer 25 不认合并键名** —— `'Control+Space'` / `'Shift+Tab'` 整串拿去查键表 → `Unknown key`。
   组合键一律 `down` / `press` / `up` 拆开写。
4. **`${}` 是合法的 snippet 空占位符**（查过 `@codemirror/autocomplete` 的 `parseSnippet`），里面可以什么都不填。
5. ★★ **加载失败的 promise 不能缓存** —— `if (!p) p = import(...)` 会把 rejected 的 promise 一直留着，
   于是「第一次加载失败」变成「这辈子都用不上编辑器」：换题、网络恢复都不会再试。
   现在失败时把缓存清空，下一题重新加载（测试 [9] 拿「先屏蔽脚本、再放开切题」验这条）。
6. **切题后等编辑器就绪，不能只看 `#codeEditor` 在不在** —— 那个宿主 div 一开始就在（hidden），
   是给回退留的位置。可靠信号是「`#codeEditor` 不再 hidden **且** 里面真有 `.cm-content`」。

### ★★ 顺手修掉的既有 bug：草稿 key 拼错了

`web/index.html` 里 `LS.draft` 是**函数** `p => 'pta.draft.' + p`，但三处调用都写成 `LS.draft + p.id`
—— 字符串拼函数对象，真实 key 是 `"p => 'pta.draft.' + p1"` 这么个东西。

- 为什么一直没暴露：**读和写用的是同一个错 key**，答题、切题、刷新全都正常。
- 什么时候会炸：**「导出进度」按 `pta.draft.` 前缀筛草稿** → 永远筛不到 → 导出的备份里草稿恒为 0 份。
  真踩了：`ui_test_local_judge` 的「已导出：3 道题 + **1 份草稿**」原来是「+ 0 份」。
- 修法：抽 `draftKey(id)` 统一出口，并**带旧 key 迁移**（新 key 读不到时回查旧 key，命中就搬过来再删旧的），已存草稿一份不丢。

## 数据工具

- `tools/export_static.py`：导出 `docs/`（题库快照 + 前端 + `.nojekyll`；`web/editor/` 也会一起拷过去，2026-10-15 加）。
  **`--with-cases`**（2026-10-14 加）会把**完整测试点**一并写进 `problems.json`，
  前端本地判题就靠它。★ 不开这个开关时**不加 `cases` 键**，默认导出与历史产物**字节级一致**
  （只差 `generated_at` 时间戳）—— 这条专门回归过，免得顺手把默认行为改掉。
  体积实测：281 KB → 351 KB（**gzip 后 47 KB → 54 KB**，多 6.8 KB）。
- `tools/backup_db.py`：`backup` / `export -o x.json` / `import <json|db>` / `list`。
  **去重键 = 题目 + `created_at` + `verdict` + `code.strip()`**。`_import_db()` 用 `ATTACH DATABASE`；题目按**标题**跨库对应。
- `tools/reset_progress.py`：清空做题记录（只删 submissions / submission_cases / mastery，题目保留；默认预览，加 `--yes` 才真删）。

### ★★ 血的教训（2026-10-09）

用户报「重启 `run.bat` 后记录没了」—— 排查发现**启动流程全程没有任何 DELETE**。
**真凶是收尾时误跑的 `reset_progress.py --yes`，把用户真实刷题记录当自测垃圾清了。**

> **用户库里有真实数据时，绝不在收尾自动清空；要清必须先问。**

## 解释器

- **Thonny 装在 `D:\Thonny\Thonny\`，自带 Python 3.14.4** —— 用户平时做题的环境。
- 讲义实测用的是 `D:\Pythontools\Python\python.exe`（3.13.14）。
- **两者是不同解释器**：4 条报错原文有差异，3 个 3.14 独有语法（t-string / 无括号多异常 / 注解延迟求值）。
- Thonny 的 `thonny.exe` **没有**跑完即退的 CLI 模式 —— 「接入 Thonny」的正确做法是用它自带的 `python.exe`。

## 进度

**P0 + P1 + 评分系统 + 三科目题库(308 道) + C/C++ 双通道 + 理论题判题 + PTA 风格前端 +
数据备份 + 多用户隔离 + Pages 发布 + 前端本地判题（Linux 理论 179 道）+ 进度导出/导入 +
智能编辑器（自托管 CodeMirror 6，Python/C/C++ 题）** 已完成。

### 部署路线（2026-10-14 定）：不是「VPS vs 纯前端」二选一，而是三步走

1. ✅ **Linux 179 道理论题改前端本地判** —— 零依赖、当天可见，已落地并验证
2. ⏳ **Python 56 道走 Pyodide** —— 可行性已在 `experiments/pyodide-judge/` 真跑验证
   （Node 15/15 + 真浏览器 10/10；CPython 3.14.2；单样例中位 0.2 ms；死循环 2 s 被 terminate 且不冻页面）
3. ⏳ **C/C++ 31 道缓做** —— 浏览器内跑 clang 要下 ≈95 MB 换 15% 覆盖，不划算；
   在 Fedora 上本地 g++ 跑反而更对

后端的定位因此**从「必须」降级为「可选增强」**，只干三件事：
**跨设备进度、C/C++ 判题、防作弊**。

> ★★ 代价必须记住：`docs/problems.json` 现在**带全部 1819 个测试点**（`--with-cases`），
> 也就是**期望输出是公开的**（仓库公开、Pages 公开）。自学平台无所谓（随时对答案反而是加分项），
> 但**分享给别人刷题就有作弊空间**。**参考解 `reference_solution` 仍然绝不外传**。
> 想回退到「不下发」：不加该参数重导一次即可（前端会自动退回手动标记，不会报错）。

待做：

- **P3** AI 出题管线
- **P4** Shell（SSH）runner —— 需用户提供 SSH 目标（`hosts` 里没有 `fedora`；`wsl.exe` 被安全策略列入程序黑名单）
- **P5** AI 讲解 + 双解释器对拍 + Obsidian 导出
- 「进度跨设备」的轻量方案（导出/导入已经能用；真要**自动**同步才需要一台服务器）

**待用户操作**：

1. 在 Render 部署后端（连 GitHub → 读 `render.yaml` → ★ **挂 Disk 到 `/data`**）
2. 回 Pages 点「设置」填后端地址（或 `?api=` 一步到位）

## 2026-10-15 · 题库扩容 + 题型分类（DS 窗口完成部分）

- **题库 204 → 308 题 / 715 测试点**（python 70 / ds 59 / linux 179），verify_bank 全过。
- **DS 线补齐 4 讲**（tools/gen_ds_bank.py）：06 图 4 编程题（邻接表头插法/BFS 跳数/Dijkstra/拓扑字典序）、07 查找 4 题（折半过程/BST/散列线性探测/链地址）、08 排序 4 题（冒泡逐趟/快排一趟划分/堆排/归并逐趟）——全部 oracle+solution+alt 三件套对拍。
- **题型六类标注齐了**（question_type 列，前端徽标/筛选/多选交互由另一窗口完成）：单选 123 / 判断 35 / 填空 25 / 多选 10 / 简答 2 / 编程 113。DS 侧多选 2 + 简答 2 用 bank_kit.multi() 和 gen_ds_bank 本地 _sa()（简答工厂没动共享的 bank_kit）。
- ★ smoke_cloud 被理论题坑过：它拿 subject=ds 的**第一道题**喂 g++ 试编译，理论题排前就会 CE——已改成只挑 `line=="cpp"` 的题。
- ★ 本机跑 smoke_cloud 用 `D:/Pythontools/Python/python.exe`（fastapi 装在系统 Python，venv 里没有）。
- 未推送：工作树混着另一窗口的未提交改动，push 由两窗口协调后统一做。

## 2026-10-16 · 笔记区：Obsidian 480 篇讲义搬上静态站

**目标**：把 `D:\work\Obsidian` 四条学习线的全部笔记（含习题、实验题库、代码解释）部署到
Pages，并且和题库双向互跳。

**产出**：`tools/export_notes.py`（vault → 静态数据）+ `notes-src/index.js`（渲染器，
esbuild 打包 **124.8 KB**）+ 前端 `#/notes` 路由 + `tools/ui_e2e_notes.mjs`（**29/29** 真浏览器）。
**2026-10-21 起 639 篇 / 283.5 万字**（加 C++ 基础线 159 篇），`docs/notes` 约 **8.3 MB**
（`search.json` 3.6 MB 是最大头，懒加载）。

### ★ 三个坑（都真踩了）

1. **代码块与行内代码必须先护住，再替换双链**。笔记里满是 bash：`[[ -f $f ]]`、`[[ 10 > 9 ]]`、
   `[[ "$a" < "$b" ]]` —— 跟 Obsidian 的 `[[双链]]` **字面完全一样**。第一版只护了围栏、
   没护行内代码，导出后冒出 11 个「未解析的双链目标」，全是 shell 条件表达式。
   修法：先按反引号把行切成段，只有非代码段才做替换。
   （和 `moc_check.py` 当年加「行内码方括号盾牌」是**同一个坑的第二次显形**。）

2. **callout 必须先摘 `>` 前缀，再递归处理内容**。2210 个 callout 里有 **574 个内部嵌着代码块**，
   而源文件里那些代码块**每行都带 `> `** —— 不先摘前缀，围栏检测根本认不出来。
   正确顺序是「识别 callout → 逐行摘 `>` → 递归回同一套逐行状态机」；引用块里的围栏也靠这个递归解决。

3. **`this.lexer` 在 marked 18 的 renderer 里不存在**。callout 扩展原本在 renderer 里
   `this.lexer.inlineTokens(标题)` → `Cannot read properties of undefined`，
   marked 还会附一句 "Please report this to github.com/markedjs/marked"，
   **把人往它自己的 bug 上引**。标题的 inline token 要**在 tokenizer 阶段**算好塞进 token，
   renderer 里用 `this.parser.parseInline` 取。

### ★ 2026-10-16 二次导出（DS 线补 C++ 后重跑）又修的两个导出缺陷

这两个都**不是本次引入**，是重跑时冒出来的既有缺口：

1. **同页锚点链接 `[[#小标题]]` 完全不支持**。Python「习题工具箱」那张表整列在用（13 条），
   target 为空、只有锚点，旧代码走到 `resolve("")` 必然失败，于是 `unknown` 里多一个**空字符串**目标，
   告警打出来是「有 1 个双链目标没解析出来：」（后面什么都没有，完全无从下手）。
   修法：`target` 空而 `anchor` 非空 → 视为**当前这篇笔记自己**，渲染成
   `[label](#/notes/<self-slug>#<anchor>)`；label 退回用锚点名。实测 13 条全部成为真链接。
2. **裸写的 `[[ ]]` 被当成"目标为空的双链"**。`Linux学习总览.md` 那句
   「三兄弟：test / [ / [[ ]] 的差异」**没加反引号**，逃过了行内码盾牌。
   修法：target 与 anchor 都为空 → **原样保留**（当文本），不记 unknown。

修完 `unknown` 为空。顺带把 `export_notes.py` 的说明补一句：**改完讲义必须重跑**，否则站点笔记是旧的。

### 设计取舍

- **渲染器自己打包（marked + highlight.js），不复用题面那个 `mdRender`**：那个是为短题面写的
  简化版，而笔记是 248 万字真实 markdown（嵌套 callout / 表格 / 任务列表 / 1500+ 带语言代码块）。
  124.8 KB 按需加载，值这个钱。highlight.js 只注册笔记里真出现的十几门语言
  （4167 个代码块**没标语言**，直接跳过不高亮）。
- **wikilink 重名按线消歧**：`NN-01 一页速览` 在 Python 和 DS **同名**（8 组），
  解析顺序是「同学习线 → 同讲 → 同目录」逐级收敛；DS 的索引链接是**路径式**
  （`[[02讲_线性表/00 本讲分节索引|…]]`），两条路径都得认。
- **锚点里带方括号**：`#4.2 切片：[start:stop:step]` 这种锚点，正则 `[^\[\]]+` 会整个漏掉
  （页面上原样显示 `[[…]]`）。改成允许一层内嵌 `[...]`，源文件里多打的第三个 `]`（`]]]`）一并收掉。
- **折叠 callout 保持原样**：1237 处 `> [!x]-`（笔记里的「答案收起」）转成 `<details>` 默认关闭，
  但**正文照旧进搜索索引** —— 藏起来的内容也该能被搜到。
- **和编辑器同款的两个缓存坑**：动态 import 失败要「清缓存 + 换 URL（`?retry=N`）」，
  因为浏览器对加载失败的 import 也按 URL 记结果，只清变量没用。渲染器 124.8 KB 同理。
- **题目 ↔ 笔记靠讲号对，不靠讲名**：题目写「第 07 讲 · 函数」，笔记目录是「07讲_函数上」，
  讲名两边写法不一致。Linux 线另有两类非讲次来源：「基础命令 · X」→ `linux-cmd`、
  「实验 N · X」→ `linux-bank`。
- 导出分三块：`index.json`（目录树，63 KB）、`p/<slug>.json`（480 篇单篇，按需取）、
  `search.json`（全文索引）。`export_static.py` 已带上这一步，**vault 不存在时自动跳过**，
  CI 上没有 Obsidian 也不会炸。

### ★ 顺手修掉的过时断言（不是本次引入）

复跑时 `ui_smoke` / `ui_e2e_local_judge` 各有失败，查下来是**题库扩容（204 → 320 题）
之后没跟上的硬编码**：

- `ui_smoke.mjs`：「展开 / 折叠」断言 `=== 4`，而 DS 分组已变 8 → 改用 `subjectGroups('ds')`。
- `ui_e2e_local_judge.mjs`：两处写死 `2615`（旧总分），实际已是 **3945** → 改用 `BANK.total_score`。
- `tools/e2e_ui.py`：**同样的病，2026-10-16 已修完**（见下一节）。

这正是 memory 里那条约定说的：**「断言写成与题库定义对齐，而非硬编码数字」**。

### ★★ `tools/e2e_ui.py` 从 25/33 修回 33/33（2026-10-16）

这个脚本是唯一「起真服务、走真 HTTP」的端到端。题库扩容后它报了 **8 项失败**，
查下来**没有一项是产品坏了**，全是脚本自己过期 —— 修法是把期望值全部改成
「从题库定义现算」，而不是把数字从旧值改成新值（否则下次扩容再烂一遍）：

| 原来的写法 | 病根 | 现在 |
|---|---|---|
| `user_max_score == 2615` | 写死旧总分 | `== sum(题库每道题的 total_score)` → 现算 **3945** |
| `ds 31 题 / 4 组`、`linux 117 题 / 16 组` | 写死旧题数 | 与 `bank_stats()` 现算的题数/分组数比 → **71/8、179/22** |
| `items[0]["langs"] == ["cpp","c"]` | **拿列表第一题当编程题**：DS 线补进「第 01 讲 · 绪论」后首题成了理论题（`langs` 本来就该空） | 先筛出**第一道有 langs 的题**再断 |
| `items[0]["source_section"].startswith("第 02 讲")` | 同上；且真正的不变量是「**列表按讲义讲次排**」 | 直接借接口自己的 `_order_key` 排一遍题库，两边标题序列逐项比 |
| **`/api/problems/57` 与所有 `submit(57, …)`** | ★★ **id 会漂**：57 号现在是一道 Python 题（「wc 三件套」），于是 `subject_label` 拿到 Python 标签 → C/C++ 提交全 WA → 下游「历史最高分 / 已解决 / 总分」跟着塌成 0（**8 项失败里有 6 项来自这一个数字**） | 按标题 `find_by_title("顺序表按位插入")` 找 id，**找不到直接停机报错** |
| `p57row["best_score"] == 15`、`me["score"] >= 15` | 写死该题满分 | 从题目详情读 `total_score` |
| `len(r_c["cases"]) == 5` | 写死测试点数 | `== pdet["testcase_count"]` |

★ 顺带修掉一处**输出说假话**：数据库归属提示用 `"真实库" in _warn` 做判据，
而「安全」那句话里也含「不是真实库，安全」四个字 —— 于是**连测试库时也会多印一行
「这次的数据进了真实库」**。改成认警告自己的 `⚠️` 前缀。

复跑结果：**33 项通过 / 0 项失败**。复现命令（注意本机要带 `NO_PROXY`）：

```bat
set PTA_DB=E:\学习\001\pta\data\_bank_test.db
D:\Pythontools\Python\python.exe -m uvicorn app.main:app --port 8792
set NO_PROXY=127.0.0.1,localhost
D:\Pythontools\Python\python.exe tools\e2e_ui.py 8792
```

### 收尾时顺手挖出的两个真问题（2026-10-16 补）

**1. `ui_e2e_local_engines.mjs` 的 Python 侧一直挂，根因不在产品，在本机浏览器**

表现为重试后 `浏览器判题失败 / Program terminated with exit(1)`（第一次还见过 `[object Object]`）。逐层剥：

- 页面里直接 `fetch('pyodide/python_stdlib.zip')` → **HTTP 204 / 0 字节**；
  而**服务端日志明明写着 `status=200 bytes=2545637`**。
- 同一份内容改叫 `zzprobe.bin`（`application/octet-stream`）→ 200 / 2545637 字节全量到达。
  只换后缀就变，说明拦的是**URL 后缀 `.zip`**，与 Content-Type 无关。
- 排除了两个常见嫌疑：`--no-proxy-server` **无效**（不是代理）；
  `HKLM/HKCU\SOFTWARE\Policies\Google\Chrome` **都不存在**（不是企业策略）。
- 结论：**本机环境拦 `.zip`**（多半是安全软件/浏览器策略），不是产品缺陷。

而 Pyodide 的标准库恰好就是 `python_stdlib.zip`，所以 Python 起不来。
**★ Pyodide 会把这一步的失败吞掉** —— `pyodide.mjs` 的 `installStdlib` 里
`catch (r) { console.error(...) }` 之后照常继续启动，Python 于是崩在一句
没头没脑的 `Failed to import encodings module`。两条改进：

- `python-worker.js` 先自己拉一遍 `python_stdlib.zip` **验字节数**（`assertStdlib`），
  再交给 `loadPyodide`；并把 bootstrap 阶段的 `encodings` / `Program terminated` 报错翻译成人话
  （含「再点一次」的出路）。顺带加了 `describe()` —— 之前 Pyodide/浏览器抛**普通对象**时
  `String(e)` 会变成毫无信息量的 `[object Object]`。
- 副产物：Python 判题失败现在**秒失败 + 人话**，不再先干等 90 秒超时。
- 测试加了 **[0] 环境预检**：fetch 一遍 stdlib，字节数对不上就**明说环境阻断并跳过 Python 两项**，
  C/C++ 两项照跑 → 5 通过 / 2 跳过 / 0 失败。**不把环境问题伪装成产品失败，也不静默跳过。**
- 一次性探针留在 `data/probe_py_retry.mjs`（`data/` 整个被 gitignore），
  下次再遇到「引擎加载失败但看不出为什么」可以直接改它复现。

**2. 种子题写了 78 秒，`smoke_cloud` 因此超时挂掉**

`smoke_cloud` 报 `[FAIL] 90 秒内 /api/health 变 healthy`，日志里 `20:04:42 数据库就绪` →
`20:06:00 写入 320 道种子题` —— **78 秒**。

- 根因：`db.insert` 每条都是 `with connect_ctx(...)`，即**每条 INSERT 新开一次连接**
  （连接 + 3 条 PRAGMA + 提交 + 关闭）。320 题 ≈ **1050 条 INSERT** → 78 秒
  （杀软拦文件读写时更慢）。`isolation_level=None`（自动提交）让每条都真的落盘。
- 修法：`app/db.py` 加 `bulk()` —— **一个连接 + 一个事务**；`insert()` / `query_one()`
  多一个可选 `conn` 参数（带了就用现成连接，不再另开）；`seed.ensure()` 整批走 `bulk()`。
- 实测：**78 秒 → 0.1 秒**；题数 / 测试点数一字不差（320 / 727）；幂等仍成立（第二次 0 道）。
- ★ 对部署是实打实的收益：Render 免费档冷启动本来就可能顶掉健康检查窗口。

## 2026-10-17 · 收藏 / 错题本（可编辑，用于巩固）

### 为什么是「补一条通道」而不是「新建一张表」

`mastery` 表从多用户改造（2026-10-13）起就有 `is_starred` / `level` / `note` 三列，
`/api/problems`、`/api/progress`、`/api/stats` 也一直把它们**读**出来 ——
但全项目**没有任何一处写入**（判题只写 attempts / ac_count / best_score / verdict / solved_at）。

于是「收藏」是个点了没反应的空按钮，「错题备注」无处可存。这次就是把这条缺失的写通道补上：

| 端点 | 作用 |
|---|---|
| `PATCH /api/mastery/{pid}` | **增量**改 `is_starred` / `level` / `note`（出现哪个字段只改哪个） |
| `GET /api/mastery` | 当前用户的全部标注（前端首屏对齐本地缓存用） |
| `GET /api/wrongbook` | 错题 / 收藏 / 有备注的归集 + 各桶计数 |

### 三个语义决定（改之前先看这里）

1. **「错题」不落库，算出来的**：`attempts > 0 且 best_score < total_score`。
   它是进度的派生量，存一份必然与判题结果打架（判完还得记得同步它）。
2. **收藏不冒充「做过」**：`_ensure_row()` 建行时 `attempts = 0`。
   否则首页「已尝试」和错题本会被一堆 0 分假错题污染 —— `httptest_mastery` 有专门一条守这个。
3. **增量而非全量**：点星星不该把备注冲掉，存备注不该取消星星。前端两个入口各自只管自己那半边。

### 前端：本地优先，后端兜底

`localStorage['pta.mastery']` 里存一份，**写操作永远先落本地**：

- 静态站（GitHub Pages）根本没有后端，离线也必须能收藏、能写备注；
- 纯本地又换浏览器就丢，所以连上后端时异步 `PATCH` 过去；
- 写失败**不回滚本地**（用户刚敲的那段字不能因为网络抖一下就没），
  只有后端明确 4xx（参数越界/题目不存在）才回滚并 toast。

`wrongbookData()` 两条腿出同一个形状：在线调 `/api/wrongbook`，离线用 题库 + 本地进度/标注现算。
本地标注**永远覆盖**服务端值（服务端那趟还在路上时，界面不能先把你刚写的字抹掉）。

界面四处入口，共用同一套逻辑：

- 题集表格每行的 ☆（不新增列，塞在「题目」列标题前）
- 题目页 chips 里的「☆ 收藏」
- 题目页题面底部的「我的错题备注」（点一下就能改，跟错题本里是同一个 `.wbNote/.wbEditor`）
- `#/wrongbook`：统计卡（待攻克/已收藏/写了备注/已攻克）+ 分段筛选 + 科目 + 搜索（标题与备注一起搜）+ 掌握度三档 + **随机巩固一题**

### 踩到的坑

1. ★★ **`waitUntil:'networkidle2'` 不代表页面渲染完了**：`boot()` 还在 await 第一批 fetch
   时它就已经达标（页面显示「正在加载题库…」），而我第一版的等待条件里**包含了 `.loading`**
   → 断言全打在骨架上，三项假红，看起来像功能坏了。判据改成「`#app` 里不再有 loading 骨架」。
2. ★ **`#/` 是科目卡片页，不是题目表**：表格在 `#/set/<subject>`。e2e 第一版点星星时找
   `table.ptable` 点了 30 秒。
3. ★ **在线模式不能直接访问 uvicorn 的 `/`**：它返回 `web/index.html`，但页面里 `judge_text.js`
   等是相对路径，后端只把 `web/` 挂在 `/static` → `/judge_text.js` 全 404，脚本一行不跑。
   e2e 改成「服务 `docs/` + 把 `/api/` 反代到 uvicorn」，顺带就是 **Pages + Render 的真实形态**。
4. 顺手补了个**内联 SVG favicon**：之前每次开页面控制台都有一个 `GET /favicon.ico 404`，
   压着 e2e 的「零 JS 报错」断言（也确实是线上一直存在的小毛病）。data: URI 不产生请求。

### 补：线上 Pages 复验揪出的默认筛选 bug（2026-10-17 稍晚）

本地两轮 e2e 全绿，但拿**真 Chrome 打真部署**（`https://cosy119.github.io/my-pta/`）一跑就露馅：

```
✅ 点星变实心    ✅ 统计卡「已收藏 1」
❌ 错题本列表 0 条   ❌ 连备注编辑区都没有
```

**病因**：默认筛选是 `wrong`（待攻克），判据 `is_wrong = attempts>0 && best_score<total_score`。
刚收藏、**还没做过**的题 `attempts = 0` → 它不是错题 → 列表空。
统计卡却按 `is_starred` 单独数，于是出现「写着已收藏 1、列表里啥也没有」的自相矛盾。
本地 e2e 没抓到，是因为它**点星之后先切了「收藏」筛选再断言**，把这个坑绕过去了。

**两处修**：

1. 默认筛选 → `all`（并集：做过 ∪ 收藏 ∪ 有备注），「全部」挪到分段第一项。
   `all` 没有额外成本 —— `/api/wrongbook` 本来就是这个并集，不会把整库题捞出来。
2. 空态不再只说「没有」，而是**列出别的分组有几题并可直接点过去**
   （`.wbJump` / `.wbChip`）—— 老用户 localStorage 里还存着旧的 `wrong`，全靠这块兜。

**顺手把「线上」变成一条常驻测试腿**：`node tools/ui_e2e_wrongbook.mjs --live`
（默认不跑，免得每次都要等 CDN）。这轮按 URL 白名单放过 `/api/*` 的 404 ——
那是静态站**故意的降级探测**，Chrome 会把它记成 console error，不是回归。
另外新增一条回归断言：「默认筛选下直接看得见刚收藏的题（未做过也算）」——
就是上面那个 bug 的守门人。

> 教训记一笔：**本地 e2e 全绿不等于线上对**。这次差别只在「用户第一眼看到什么」，
> 而断言被自己的操作顺序掩盖了。凡涉及"默认值"的东西，断言就得在**不额外操作**的前提下取。


## 2026-10-18 · DS 经典题型第二批扩容（04 串数组广义表 / 05 树和二叉树 / 06 图，+46 道编程题）

按四张 PTA 经典题型截图举一反三、循序渐进（difficulty 1→4），新增 **46 道 C/C++ 编程题**（`_oracle_57` ~ `_oracle_102`），全部满足「独立 Python Oracle + C/C++ 参考解 + 独立第二实现 `alt_solution`」三件套并经 `g++` 全量对拍通过：

| 讲次 | 新增题数 | 覆盖题型（由浅入深 + 举一反三） |
|---|---:|---|
| 第 04 讲 · 串、数组和广义表 | 13 | 判断对称矩阵、统计子串（允许重叠）、字符串模式匹配（KMP / strstr 口径）、【模板】KMP字符串匹配（全部位置 + Border 数组）、好中缀（前后缀且在内部出现）、病毒变种（环状 DNA 破环成链）、矩阵鞍点查找、三元组顺序表表示的稀疏矩阵转置运算I（按列序朴素转置）、三元组顺序表表示的稀疏矩阵转置II（打印 num/cpot + 快速转置）、稀疏矩阵加法（双指针归并 + 零元消去）、稀疏矩阵乘法（行逻辑链接累加）、最大子矩阵和问题（二维压一维 Kadane）、广义表的表头与表尾（GetHead/GetTail） |
| 第 05 讲 · 树和二叉树 | 16 | 建立与遍历二叉树（先/中/后三序）、交换二叉树中每个结点的左孩子和右孩子、列出叶结点（静态链表自找根 + 层序）、还原二叉树（先序+中序求树高）、根据后序和中序遍历输出前序遍历、树的遍历（后序+中序求层序）、玩转二叉树（中序+前序镜面反转层序）、完全二叉树的层序遍历（后序还原完全二叉树）、树层次遍历（双亲表示法转孩子链）、浪漫侧影（二叉树右视图与左视图）、二叉树的最大宽度与层号、二叉树的最近公共祖先（LCA）、修理牧场（哈夫曼锯木头最小花费）、哈夫曼树（WPL + 前缀码最优性判定）、朋友圈（并查集最大连通块）、部落（并查集人数与连通分量计数） |
| 第 06 讲 · 图 | 17 | 邻接矩阵表示法创建无向图（含顶点度）、邻接表创建无向图（尾插法保序）、图深度优先遍历、列出连通集（DFS + BFS 双遍历）、哥尼斯堡的“七桥问题”（连通 + 全偶度）、欧拉通路与欧拉回路判定、公路村村通（MST Kruskal / Prim）、森森美图（双关键字最小生成树）、单源最短路径（Dijkstra + pre 数组还原路径）、最短路径（无向带权多源查询）、最短路径算法(Floyd-Warshall)、哈利·波特的考试（图的中心点 Minimax 最短路）、旅游规划（距离最短且过路费最少双权最短路）、任务调度的合理性（AOV 判环）、最短工期（AOE 最早完成时间）、关键活动（AOE 关键路径 ve/vl + 逆序铁律）、家庭房产（并查集聚合 + 多关键字排序） |

- 题库总量：**333 → 379 题** / **4110 → 4900 分** / **791 → 972 测试点**（DS 线 **84 → 130 题**，其中编程题 102 道、理论题 28 道）。
