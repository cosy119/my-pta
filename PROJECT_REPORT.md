# 本地 PTA 刷题平台 · 项目总报告

> 生成时间：2026-10-15 10:50（GMT+8）
> 用途：交给外部 AI（ChatGPT）做独立审阅。**不含任何机密**（token、凭据均未写入）。
> 数据来源：真实库只读查询 + 最近一次全量自检（2026-10-15）+ GitHub API，全部数字可复核。

---

## 1. 项目一句话

一个**仿 PTA（pintia.cn）的本地/静态在线评测平台**：FastAPI + SQLite 后端负责 C/C++/Python 代码判题与理论题判分，GitHub Pages 静态前端可独立运行（Linux 理论题在浏览器本地判，零后端），题库覆盖三条自学线（Python / 数据结构 / Linux）。

- **仓库**：https://github.com/cosy119/my-pta （公开，main 分支）
- **线上站点**：https://cosy119.github.io/my-pta/ （GitHub Pages，已上线）
- **本地启动**：双击 `run.bat` → http://127.0.0.1:8765
- **当前提交**：`2a7dba1`（本地与远程一致；CI ubuntu+windows 双 job）
- **规模**：约 3.2 万行（含生成器与题库源码），26 个后端模块，16 个自检/测试脚本

## 2. 架构

```
GitHub Pages（docs/ 静态前端，index.html + problems.json + judge_text.js）
        │  X-User-Token 请求头（跨源）
        ▼
FastAPI + uvicorn 后端（本地 run.bat 或云端 PTA_CLOUD=1 + $PORT）
        │  API 只入队 → 独立后台单线程（concurrency=1）
        ▼
判题 worker：每个测试点独立子进程
        ├── Python: python main.py（stdin/stdout）
        ├── C:      gcc -std=gnu11 main.c（沙箱限内存+墙钟）
        ├── C++:    g++ -std=c++17 main.cpp
        └── 理论题: TextRunner（不启子进程，提交文本当输出做归一化比对）
        ▼
SQLite（题库 204 + 测试点 532 + 提交记录 + 掌握度）
```

- 前端**离线降级**：连不上后端时读 `problems.json` + localStorage，拼出与在线一致的界面；此时 **Linux 117 道理论题可在浏览器本地判题**（`web/judge_text.js`，是把后端 `app/judge/compare.py` 的判题口径逐字移植的 JS 版，3463 条答案对拍与 Python 端逐字段一致）。
- 后端定位已**从「必须」降级为「可选增强」**：跨设备进度同步、C/C++ 判题、防作弊。

## 3. 代码结构（模块清单）

| 位置 | 内容 | 行数（约） |
|---|---|---|
| `app/` | FastAPI 后端 26 个模块 | 13,100 |
| ├ `app/judge/` | 判题核心：`sandbox.py`(522) / `worker.py`(343) / `compare.py` / `runner_python.py` / `runner_cpp.py` / `runner_text.py` | ~1,600 |
| ├ `app/scoring.py` | 评分模型（PTA 测试点口径） | — |
| ├ `app/seed.py` | 题库播种 + 老库自动迁移 | 379 |
| ├ `app/problems_bank*.py` | 题库源码（linux 4,164 / ext 2,545 / ds 2,187 / py 599） | ~7,500 |
| `web/index.html` | 前端单页（PTA 风格，hash 路由三层） | 1,745 |
| `web/judge_text.js` | 浏览器端理论题判题器（UMD） | ~470 |
| `tools/` | 19 个 Python + 5 个 mjs 自检/工具脚本 | ~11,700 |
| `experiments/pyodide-judge/` | 纯前端判 Python 题的可行性 PoC（已验证，未并产线） | 915 |
| `docs/` | Pages 发布产物（前端 + problems.json 快照） | 生成物 |

## 4. 题库数据（真实库只读实测）

| 科目 | 题数 | 总分 | 测试点 | 形态 |
|---|---|---|---|---|
| `python` | 56 | 860 | — | 编程题（Python 源码判） |
| `ds` | 31 | 595 | — | 编程题（**C 或 C++ 任选**，双通道） |
| `linux` | 117 | 1,160 | — | 理论题（选择/判断/填空，`oneof` 多备选口径） |
| **合计** | **204** | **2,615** | **532** | |

- 每道编程题都有**两套独立实现**（`alt_solution`），`verify_bank` 逐字节对拍参考输出。
- 库状态干净：`problems 204 / testcases 532 / submissions 0 / mastery 0 / users 1`（`local-default-user` 为程序默认身份，非脏数据）。

## 5. 判题与评分设计

- **评分对齐 PTA 测试点口径**：每个测试点独立带分值，得分 = 通过点分值之和；没满分 = 部分正确；进度取**历史最高分**（`app/scoring.py`）。
- **每题三个指针**：`best_submission_id`（最高分）/ `last_submission_id`（打开题目自动回填代码）/ `solved_at`。
- **沙箱**（`app/judge/sandbox.py`，双平台两套）：
  - Windows：Job Object 限内存 + 墙钟看门狗；
  - Linux：`RLIMIT_AS` + `/proc/<pid>/status` 的 `VmHWM` **5ms 采样线程**（峰值只在进程结束后读会永远读到 0——踩过的坑）。
  - **MLE 判据 = 两条独立证据链任一成立**：① stderr 含 OOM 字样；② 峰值 ≥ 限额×0.9 且异常退出且无输出。★ 量纲要点：`RLIMIT_AS` 限**地址空间**，`VmHWM` 量 **RSS**，两者不能直接比——这个错只有 Linux 上才暴露。
- **理论题宽容口径**（`compare.py` 的 `answer_forms()` 三层）：原文 → 剥**排版类**标点（全角句号、多余空格等）→ 命令归一化（短选项拆合、乱序）。★ ASCII 的 `. ' "` 在命令行里有语义，**绝不剥**。
- **浏览器端判题**（`web/judge_text.js`）：`normalize_answer` / `answer_forms` / `_norm_cmd` / `oneof_alternatives` / `_uses_oneof` / `compare` / `scoring.grade` 逐函数从 Python 移植；对拍 **3463 条答案逐字段一致**（1854 AC / 1609 非 AC，正反两面都有，非恒真）。

## 6. 身份与多用户

- **无账号密码**：首次访问随机生成通行证（UUID），后续请求走 `X-User-Token` 头；换设备把通行证复制过去即接续进度。
- CORS 允许 `*`（Pages ↔ 后端跨源必需），预检放行 `x-user-token`。
- 前端设置里有**进度导出/导入 JSON**（含进度+草稿+通行证；导入按**取最高分**合并，绝不覆盖）。

## 7. 验证与测试体系（最近一轮全绿，2026-10-15）

| 脚本 | 结果 | 覆盖 |
|---|---|---|
| `verify_bank.py` | 204 题 / 532 点全过 | 全库双实现逐字节对拍 |
| `verify_text_judge.{py,mjs}` | 3463 条逐字段一致 | JS 判题口径 vs 后端 Python |
| `verify_theory_facts.py` | 39 过 / 0 不符 / 8 无法核验 | **理论题答案实证核验**（先真跑 GNU 命令得出事实，再对答案键） |
| `selfcheck.py` | 62/62 | 内核 41 + 评分 21 |
| `selftest_sandbox.py` | 19/19 | 超时杀孙进程、MLE 判据矩阵 7 项断言 |
| `selftest_cpp.py` | 9/9 | C/C++ AC·CE·WA·TLE、产物不串 |
| `selftest_theory.py` | 14/14 | 72 道单选干扰项全判错、判断题双向 |
| `smoke_cloud.py` | 13/13 | **云端启动分支**真起子进程（PTA_CLOUD=1+$PORT）、绑 0.0.0.0、真编 C++/真跑 Python 各 AC |
| `e2e_ui.py` | 33/33 | 端到端过 HTTP |
| `ui_smoke.mjs` | 41/41 | jsdom 真渲染（离线+假后端两遍） |
| `ui_test_local_judge.mjs` | 45/45 | 离线本地判题，真 jsdom + 真加载外链脚本 |
| `ui_e2e_local_judge.mjs` | 25/25 | **真 Chrome**（puppeteer-core + 系统 Chrome）跑发布产物：真判题、真下载、真上传导入 |
| `httptest_users / split / httptest` | 23/23、18/18、18/18 | 多用户隔离、越权 404、CORS 预检 |
| `show_text_judge.mjs` | 全过 | 判题器行为说明：309 标准答案全 AC / 351 胡写全 WA / 72 变异错答案 71 被抓 |
| **CI** | ubuntu + windows 双 job **success** | sandbox→cpp→theory→selfcheck→verify_bank |

- 所有会写库的自检走**测试库**（`tools/_testdb.py` 导入即生效隔离；起服务脚本显式把 `PTA_DB` 塞进子进程 env）——起因是 selfcheck 曾三次污染真实库（详见 NOTES.md「血的教训」节）。
- 断言**不写死数量**（`count == 56` 这类全改成对权威来源现数），测试可重复跑。

## 8. 部署状态与路线

- **已完成**：Pages 静态站上线（含前端本地判题 + 隐藏测试点下发）；本地后端 `run.bat` 完整可用。
- **后端云端托管：用户尚未部署**。曾评估三条路：
  1. Render Starter $7/月 + Disk（进度可留）；
  2. Render 免费档（**不支持持久化 Disk**，进度留不住；15 分钟休眠）；
  3. 自有 VPS 107.173.155.115（1 vCore，上面跑着 3x-ui/Xray，判题抢 CPU）。
  用户均未选，转向**前端本地判题**路线。
- **三步走**（2026-10-14 定）：
  1. ✅ Linux 117 道理论题改前端本地判（已落地验证）；
  2. ⏳ Python 56 道走 Pyodide（**可行性已真跑验证**：`experiments/pyodide-judge/`，Node 15/15 + 真 Chrome 10/10；CPython 3.14.2；单样例中位 0.2 ms；死循环 2 秒被 terminate 且页面不冻）；
  3. ⏳ C/C++ 31 道缓做（浏览器内 clang ≈95 MB 换 15% 覆盖不划算；本地 g++ 反而更对）。

## 9. 已知限制与公开风险（如实申报）

1. **期望输出是公开的**：`docs/problems.json` 带**全部 532 个测试点**（`--with-cases` 导出，gzip 后仅多 6.8 KB）。这是浏览器本地判题的固有代价——自学无碍（随时对答案是加分项），但**分享给别人刷题就有作弊空间**。参考解 `reference_solution` 等 4 个内部字段**绝不出库**（`export_static.py::_STRIP_FIELDS` 强制剥离，已复核线上产物 0 泄露）。回退方式：不加参数重导即可。
2. **离线进度单设备**：localStorage 按浏览器隔离，换设备/清缓存即丢——已用「导出/导入」缓解，跨设备自动同步仍需后端。
3. **理论题答案核验的边界**：117 道理论题中 39 项已用真实 GNU coreutils 实证核验，8 项本机做不了（Fedora 专属、符号链接 MSYS 降级、交互式 less 等）如实标「无法核验」，其余靠教材与常识——这部分**没有第二套实现兜底**。
4. **核出并修掉过答案键 bug**：91/100 题解析曾写「`head -n +N` 报错」「`tail -n -N` 非法」——GNU 上全不成立（实测 `head -n +1000` 退出码 0 输出前 1000 行）。已改源码 + 直接 UPDATE 真实库（备份 `pta.db.bak_before_q91fix`）+ 重导 docs。
5. **MLE 判据的量纲坑**（已修）：Linux `RLIMIT_AS`（地址空间）vs `VmHWM`（RSS）不能直接比，本机怎么跑都对、只有 Linux CI 才暴露——这是 CI 存在的最大理由之一。
6. **本机判题时间含大块进程启动开销**（160~400 ms，双杀软实时扫描）——真实判题不加 TLE 重试，只有对拍工具加。
7. Python 题覆盖到第 11 讲（第 12 讲「文件」及以后尚无题）；Linux 理论题 117 道按教材 01~10 讲生成。

## 10. 工程纪律（给审阅者的参考点）

- **推送机制**：token 存本机凭据文件（不入仓库）；推送用内联 URL + `GIT_TERMINAL_PROMPT=0`。曾撞 `CRYPT_E_REVOCATION_OFFLINE`，`schannelCheckRevoke=false` 不生效，**换 openssl 后端 + 系统 CA 才是有效解**。
- **改题库源码不会自动刷库**（`seed.ensure()` 按标题跳过已存在）——必须同时改源码 + UPDATE 真实库（先备份）+ 重导 docs。
- **`data/` 整目录被 git 忽略**（曾差点把含参考解的 dump 推上公开仓库）。
- 收尾固定动作：`export_static → verify_bank → selftest_cpp → selftest_theory → selfcheck → smoke_cloud`。
- **用户库有真实数据时绝不自动清空**（2026-10-09 误清过一次真实刷题记录，已立规矩：先备份 → dry-run 预览 → 确认后才 `--yes`）。

## 11. 待办（按优先级）

1. **P3**：Python 56 道接入 Pyodide 前端判题（PoC 已验证，待产线化）；
2. **P4**：C/C++ 31 道的本地跑方案（或浏览器 clang 评估）；
3. **P5**：后端云端托管决策（Render 付费 / VPS）——跨设备进度的前提；
4. AI 出题管线、AI 讲解、Obsidian 导出（远期）。

## 12. 给审阅者的入口建议

- 想**快速判断工程质量**：看 `app/judge/sandbox.py`（MLE 判据纯函数 + 判据矩阵断言）、`app/judge/compare.py`（理论题口径）、`app/scoring.py`（测试点评分）。
- 想**复核判题一致性**：跑 `python tools/verify_bank.py` 与 `node tools/verify_text_judge.mjs`（需先 `python tools/verify_text_judge.py` 生成夹具）。
- 想**复核答案可信度**：跑 `python tools/verify_theory_facts.py`（先跑事实再对答案键）与 `node tools/show_text_judge.mjs`（判题器行为演示）。
- 想**看踩坑史与决策依据**：`NOTES.md`（随仓库，600 行实现笔记，每条都是踩坑后写的）。
- 前端单文件在 `web/index.html`（1,745 行，hash 路由 + 离线降级 + 本地判题接入）。
