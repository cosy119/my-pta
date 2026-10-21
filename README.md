# my-pta：多科目题库与在线判题

浏览器打开的学习题库：按科目、讲次和题型找题，写代码或回答理论题，再看真实评测结果和个人进度。AI 出题与讲解仍在规划中；当前判题依据测试点或标准答案，不由 AI 猜测结果。

判题不是让 AI 看代码猜，而是**真起进程跑**，再拿真实输出比对 —— 所以判定和 OJ 一致。

> 仓库：<https://github.com/cosy119/my-pta>

## 直接在网页使用（无需安装）

打开 <https://cosy119.github.io/my-pta/>，即可在浏览器中完成已发布题目（Linux 理论、Python 编程和数据结构 C/C++）的提交判题。首次做 Python 题时会加载约 14 MB 的运行时；首次做 C/C++ 题时会加载约 29 MB 的 Clang/WASI 编译器。浏览器内的 C/C++ 环境与后端 GCC 有差异，成绩保存在当前浏览器；换设备前请在「设置」中导出进度。**不需要注册、不需要安装任何东西**，一个现代浏览器就够了（进度存在各人自己的浏览器里）。引擎下载偶尔会被网络掐断 —— 报「评测机内部错误」时**再点一次「提交并判题」**就会重新下载，不用刷新页面。

## 也可以在本机运行

| 用法 | 适合 | 怎么做 |
|---|---|---|
| **直接打开网页** | 分享给别人，无需安装 | 打开上方网址；已发布题目均可在浏览器判 |
| **本机跑** | 想用 GCC 后端或保存本机后端进度 | 按下方步骤安装后双击 `run.bat` |
| **部署后端** | 想让网页使用 GCC 后端与跨设备后端进度 | 见 **[DEPLOY.md](DEPLOY.md)** |

网页可独立判理论题、Python 和 C/C++ 题；C/C++ 在浏览器内使用 Clang/WASI，GCC 判题仍需后端。
**每个人的进度各自独立** —— 不需要注册，浏览器自己带一串通行证，
后端按它区分是谁（详见 DEPLOY.md 第三节）。

## 新机器上跑起来

先安装 **Python 3.13**（安装时启用 Python Launcher 或将 `python.exe` 加入 PATH）。首次使用还需安装依赖：

```bat
git clone https://github.com/cosy119/my-pta.git
cd my-pta
py -3.13 -m pip install -r requirements.txt
run.bat
```

如果电脑没有 `py` 命令、但 `python --version` 显示 3.13，可将上面的安装命令改为 `python -m pip install -r requirements.txt`。`run.bat` 会自动选择可用的 Python 3.13；缺少解释器或依赖时会打印处理方法。数据结构题还需要安装 `gcc` 和 `g++`，并将它们加入 PATH（或在 `config/settings.toml` 的 `[compilers]` 中填写路径）。

第一次跑会自动做这些事（不用手动初始化）：

1. 建 `data/` 目录和空数据库
2. 自动补表结构、补列、**把老数据归到「本机用户」**（老库也适用，不动已有数据）
3. **自动导入当前题库**（按标题判重，重复执行不会灌两遍）
4. 打开浏览器

`config/settings.toml` 里的解释器路径是作者机器上的（`D:/Pythontools/...`）。
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

## 学习中心与复习

网页顶部「学习中心」可按题库现有科目（含独立 C++）组卷，并使用：

- 连续练习、逐题提交考试、统一交卷评测，保留本场考试答案和最近50轮练习。
- 评测任务与原轮次绑定；交卷后结果继续补回，失败可重试。关闭页面会中断本地引擎，重新打开后从任务列表手动重试。
- 多标签页按字段合并学习记录；同一场考试支持明确接管，避免旧页继续提交。
- 近7/30天学习周报、科目/题型分布、重复错题和未来7天复习安排。
- 每题自定义多组自测输入与预期输出；运行自测不计成绩。
- 提交记录每页50条、跨页选取同题对比、直接回到题目。
- 导入备份前预览新增/已有数量及备注冲突，可取消或先导出当前快照。
- 按章节、收藏或错题生成A4复习单，支持浏览器打印/另存PDF；答案与自己的错因可另起一页。

这些新增学习资料保存在当前浏览器，换设备请导出完整备份。学习周报仅依据浏览器现存提交记录，不将历史最高分当作近期正确率。

## 现在能做什么

| 能力 | 状态 |
|---|---|
| Python 判题（AC / WA / PE / TLE / MLE / RE / CE / OLE） | ✅ |
| **C 与 C++ 判题（同一道题任选一种交）** | ✅ |
| **Linux 理论题（单选 / 判断 / 命令填空）** | ✅ |
| **三科目分类（Python / 数据结构 / Linux）+ PTA 风格界面** | ✅ |
| 双解释器可选（3.13.14 讲义环境 / 3.14.4 Thonny 环境） | ✅ |
| 限时（看门狗 + 杀整棵进程树） | ✅ |
| 限内存（Job Object，峰值可见） | ✅ |
| 5 种输出比对口径（standard / ignore_trailing / token / float / **oneof**） | ✅ |
| 运行自测（不判题，直接看输出） | ✅ |
| **每个测试点独立分值 · 部分正确** | ✅ |
| **每题进度（最高分 / 最后一次 / 首次满分时间）** | ✅ |
| **提交历史 + 一键回填某次代码** | ✅ |
| **打开题目自动回填上次提交的代码** | ✅ |
| **智能编辑器（自托管 CodeMirror：缩进 / 括号配对 / 本地关键词与片段提示）** | ✅ |
| **Python、数据结构、Linux 三科目题库（题数以页面统计为准）** | ✅ |
| **笔记区：Obsidian 讲义搬上网页（480 篇 / 248 万字 · 目录树 · 全文搜索 · 双链跳转）** | ✅ |
| **题目 ↔ 笔记双向互跳（题目页「看本讲笔记」／笔记页「本讲配了 N 道题」）** | ✅ |
| **数据备份 / 导出 JSON / 恢复** | ✅ |
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

## 智能编辑器（Python / C / C++ 题）

编程题的代码框是**自托管的 CodeMirror 6**，不连任何在线服务、不调 AI、不依赖后端 ——
`docs/` 是纯静态站点，打开就能用。理论题保持原来的输入框（选择题没有代码可写）。

| 能力 | 怎么做 |
|---|---|
| 语言缩进 | 回车按当前语言的语法自动缩进（Python 冒号后缩进、C/C++ 大括号后缩进） |
| 括号 / 引号配对 | 输入 `(` `[` `{` `"` `'` 自动补另一半；**选中一段文字**再敲括号或引号，直接包起来 |
| 补全提示 | 打字时提示**本地关键词**（`for` `if` `return` `printf`…）与**代码片段**（`main` `class` `fori`…），`Ctrl+空格` 主动打开 |
| Tab | 有候选词时**接受补全**；没有候选时**缩进一级**；`Shift+Tab` **减少缩进**；`Enter` 照常换行 |
| 离开编辑器 | 按 `Esc` 关掉补全面板后再按 `Tab`，焦点移到下一个控件（键盘可全程操作，不用摸鼠标） |
| 切 C ↔ C++ | 只换语言高亮与补全源，**代码不清空**，草稿 / 提交 / 自测 / 分栏高度行为都不变 |
| 加载失败 | 自动回退到原来的 `textarea`，并提示一句；回退后功能一切照旧 |
| 草稿 | 与原来同一套 `localStorage` 草稿，切题再切回来、刷新页面都还在 |

源码在 `editor-src/index.js`（约 6 KB），用 esbuild 打成单文件：

```bat
cd /d E:\学习\001\pta
npm install                                     &rem 首次
npm run build:editor                            &rem → web/editor/editor.js（约 500 KB，已进仓库）
D:\Pythontools\Python\python.exe -X utf8 tools\export_static.py --with-cases   &rem → docs/editor/
```

改完源码记得**两条都跑**：`web/editor/` 是本地服务用的，`docs/editor/` 是 Pages 用的，
`export_static.py` 会把前者拷进后者（顺手把 `web/index.html` 也同步过去）。

★ 两个实现上的细节，免得再踩：

- **CodeMirror 没有单独的 C 语法** —— `@codemirror/lang-cpp` 一个 grammar 同时服务 C 和 C++，
  所以 C ↔ C++ 切换时**高亮本来就不变**，真正跟着变的是**补全源与片段**
  （C 的 `main` 展开成 `int main(void)`，C++ 的展开成 `int main()`）。跨语言（Python ↔ C++）高亮才不同。
- **编辑器加载失败的 promise 不能缓存** —— 早期写法把「第一次失败」永久缓存成「这辈子都用不上编辑器」，
  网络恢复、换题都不会再试。现在失败会把缓存清掉，下一题重新加载。

## 笔记区（Obsidian 讲义搬上网页）

顶栏第二个入口「笔记」是**三本教材的完整讲义**：480 篇、约 248 万字。
构建期从 Obsidian vault 转成静态数据，跟题库一样「打开网页就能看」——
不登录、不连后端、也不需要装 Obsidian。

| 里面有什么 | 说明 |
|---|---|
| 目录树 | 三条学习线（Linux 16 讲 / Python 14 讲 / 数据结构 8 讲）→ 讲 → 分节，左侧常驻 |
| 全文搜索 | 480 篇正文建索引（构建期生成，约 3 MB），标题命中优先，命中词高亮 |
| 双向链接 | Obsidian 的 `[[…]]` 全转成站内跳转；**重名的按「同一条学习线」消歧** |
| 折叠答案 | 笔记里 1200+ 处「答案收起」原样保留（`<details>`），点标题展开 |
| 代码高亮 | 1500+ 个带语言的代码块真高亮（highlight.js，只打包用到的语法） |
| 题目互跳 | 题目页有「📖 看本讲笔记」，笔记页反过来显示「本讲配了 N 道题」 |

### 它怎么来的

笔记源在 Obsidian vault（默认 `D:\work\Obsidian`，用 `--vault` 或环境变量
`PTA_NOTES_VAULT` 可以指到别处），由 `tools/export_notes.py` 转成 `docs/notes/`：

```bat
set PYTHONUTF8=1
D:\Pythontools\Python\python.exe tools\export_notes.py    &rem 480 篇 → docs/notes/
```

产出三样：`index.json`（目录树）、`p/<slug>.json`（单篇正文）、`search.json`（全文索引）。
`export_static.py` 已经带上这一步，所以平时**跑了 `export_static.py` 就不用单独跑它**；
vault 不在的机器上（比如 CI）会自动跳过，不会因为那儿没有 Obsidian 就报错。

### Obsidian 语法是怎么转的

| Obsidian 写法 | 转成 | 说明 |
|---|---|---|
| `[[目标\|别名]]` | `[别名](#/notes/<slug>)` | 解析不出来就退化成纯文本，页面上不留 `[[ ]]` |
| `> [!info] 标题` | `:::callout note open 标题` | 2210 个 callout，其中 574 个内部还嵌着代码块 |
| `> [!success]- 答案` | `:::callout ok fold 答案` | `-` = 默认折叠，就是笔记里的「答案收起」 |
| `==高亮==` / `%%注释%%` | `<mark>` / 删掉 | — |
| `← 返回本讲 · ← 上一节 · 下一节 →` | 整行删掉 | 前端按目录结构生成统一导航条，留着就重复了 |

★ 三个必须知道的坑（都真踩过）：

- **代码块里的一切原样保留**。笔记里全是 bash，`[[ -f $f ]]`、`[[ 10 > 9 ]]`
  跟 Obsidian 双链**长得一模一样**，误替换就把命令改坏了；行内代码
  ``` `[[ -f $f ]]` ``` 同理，都得先护住（第一版就是这么毁了 11 处）。
- **callout 必须先摘掉 `>` 前缀再递归处理**。callout 里的代码块在源文件里每行都带 `> `，
  不先摘前缀，围栏检测根本认不出来 —— 顺序写反，那 574 个内嵌代码块会全乱。
- **重名消歧**：`NN-01 一页速览` 在 Python 和数据结构里**同名**（8 组），
  双链解析按「同一条学习线 → 同一讲 → 同目录」逐级收敛，否则索引页会跳到隔壁教材去。

### 改了笔记之后

改的是 Obsidian 里的 `.md`（源在 vault，不在这个仓库），改完重跑：

```bat
D:\Pythontools\Python\python.exe tools\export_notes.py
D:\Pythontools\Python\python.exe tools\export_static.py --with-cases
node tools\ui_e2e_notes.mjs          &rem 29 项真浏览器验收
```

渲染器（`notes-src/index.js`，marked + highlight.js）只在改渲染逻辑时才要重打包：
`npm run build:notes` → `web/notes/notes.js` → 导出时拷进 `docs/notes/`。

★ 渲染器加载失败的处理跟编辑器同款：**不缓存失败的 promise**，而且换个 URL
（`?retry=N`）再试一次 —— 浏览器对加载失败的动态 import 也按 URL 记住结果，
光清变量、不换地址是没用的。

## 题库与题型

主页是**题集广场**（三张科目卡片 + 进度条），点进去是**题集内页**（按讲次 / 实验分组，
带状态筛选与搜索），再点题目进**答题页**（左题面右编辑区）。三层都比较贴近 PTA。

| 科目 | 主要作答方式 | 题库文件 |
|---|---|---|
| **Python 快乐编程基础入门** | Python 编程 | `problems_bank.py` + `problems_bank_ext.py` |
| **数据结构（C 语言版）** | C/C++ 编程与理论题 | `problems_bank_ds.py` |
| **Linux 系统应用与开发** | 单选、多选、判断、命令填空、**实验实操** | `problems_bank_linux.py` |

每道题现在有独立的 `question_type`，与科目 `subject`、提交方式 `line` 分开。题集页可按题型筛选，列表和题目页显示同一标签；API 与静态导出的 `problems.json` 也带此字段。

| 题型 | 字段值 | 当前情况 |
|---|---|---|
| 单选题 | `single_choice` | 点击一个选项作答 |
| 多选题 | `multiple_choice` | 界面可选多个；Linux 线有 8 道，答错漏选都算错 |
| 判断题 | `true_false` | 点击「对」或「错」 |
| 填空题 | `fill_blank` | 输入短文本；现有 Linux 命令题是**命令填空**，没有实际执行 Shell |
| 简答题 | `short_answer` | 题型预留；尚无自动语义评分器 |
| 编程题 | `programming` | Python/C/C++ 代码运行与测试点评测 |
| 实操题 | `practical` | **课程实验 1~5 共 15 道**：题目给多步任务 + 一条验收命令，你做完把命令的**真实输出**贴回来，按测试点判分 |

旧题会按提交方式与选项自动补标，也支持出题时显式填写 `question_type`。分类不修改原有答案、分值或提交记录。**多选题**的标准答案用升序字母组合（如 `AC`）；**实操题**不搞人工自评，靠「验收命令的输出」做机器可判的证据（离线、连线行为一致）。


### 数据结构线：同一道题 C 与 C++ 都能交

教材是 C 语言版，但很多人日常写 C++。所以提交时自己选语言：

| 语言 | 编译器 | 源文件 | 标准 |
|---|---|---|---|
| C++ | `g++` | `main.cpp` | `-std=c++17` |
| C | `gcc` | `main.c` | `-std=gnu11` |

两条路的可执行文件**分别命名**（`main_c` / `main_cpp`），否则同一个目录里先编 C 再编 C++ 会
「跑了上一次的产物」（`selftest_cpp.py` 有一项专门盯这个）。
另外**编译阶段单独给额度**（1 GB / 20 秒）：g++ 自己就要吃几十上百 MB，
套用题目的 256 MB 会变成莫名其妙的 CE。

### Linux 线：理论题走同一条判题管道

选择 / 判断 / 填空没有可执行的东西，但**不另开一条判题链路** ——
`TextRunner` 把提交内容直接当作「输出」交回，后面的比对 / 计分 / 历史 / 进度**全部复用**。
一只答案写法的差异交给 `oneof` checker：期望值里以 `|` 开头的每一行都是一个可接受答案。

命令题还额外宽容：空白多少无所谓，`ls -l -a /` 与 `ls -la /`（相邻短选项合并 + 簇内排序）
算同一条；但**刻意不碰** `--long`、带数字的、带参数的写法 —— 合并它们会改语义。

### 加题的两条铁律

1. **期望输出先独立算好**，再让参考解去撞它 —— 拿参考解现跑现填，就是自己给自己判卷，永远满分。
   本项目的 `expected_stdout` 全部由**另一套独立实现**预先算出（换语言 / 换算法）。
2. **第二套独立实现要对拍**（`alt_solution` 字段）。两套实现必须**各自都撞过全部测试点**，
   才能排除「单套实现有共同盲区」。

> 只有「正确答案判得过」还不够：`tools/selftest_theory.py` 专门反向验证
> **错误答案判得错** —— 否则 checker 过宽会让所有题都满分，而正面对拍依然报「全部通过」。

校验工具（改完题库必跑，全过才入库）：

```bat
D:\Pythontools\Python\python.exe -X utf8 tools\verify_bank.py           &rem 三线全跑
D:\Pythontools\Python\python.exe -X utf8 tools\verify_bank.py --ds      &rem 只跑数据结构线
D:\Pythontools\Python\python.exe -X utf8 tools\verify_bank.py --linux   &rem 只跑 Linux 线
D:\Pythontools\Python\python.exe -X utf8 tools\verify_bank.py 素数       &rem 只验标题含「素数」的
D:\Pythontools\Python\python.exe -X utf8 tools\verify_bank.py --quiet   &rem 只看汇总和失败项
```

题库生成器（题目多，用脚本写比手写可靠）：`tools/gen_ds_bank.py` / `tools/gen_linux_bank.py`，
各自带 `_sanity()` 把关（必填字段 / 标题重复 / `line` / `checker` / **理论题的样例必须为 0** ——
样例会在静态站公开，对选择题来说就是**把答案印在题面上**）。

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
│  ├─ seed.py              种子题（核心题 + 三个题库）与老库升级
│  ├─ bank_kit.py          ★ 理论题工厂（mc / tf / fill）：选项、答案、分值一次配好
│  ├─ problems_bank.py     题库：Python 第一批（11 道）
│  ├─ problems_bank_ext.py 题库：Python 第二批（42 道）
│  ├─ problems_bank_ds.py  题库：数据结构（由 gen_ds_bank.py 生成）
│  ├─ problems_bank_linux.py 题库：Linux 理论题（由 gen_linux_bank.py 生成）
│  ├─ api/                 HTTP 接口（problems / submissions / progress / me / catalog）
│  └─ judge/               判题内核
│     ├─ sandbox.py        进程沙箱（★ 跨平台：Windows Job Object / Linux setrlimit+killpg）
│     ├─ compare.py        输出比对（★ 5 种口径，含 oneof 多答案与命令宽容）
│     ├─ runner_python.py  Python runner
│     ├─ runner_cpp.py     ★ C / C++ runner（同一目录下两套产物分开命名）
│     ├─ runner_text.py    ★ 理论题 runner（提交内容即输出，复用整条管道）
│     └─ worker.py         判题队列（单线程，按测试点分值计分，按用户记账）
├─ web/index.html          前端（单文件，无构建工具；三层 hash 路由）
├─ web/editor/editor.js    ★ 智能编辑器产物（CodeMirror 打包结果，已进仓库）
├─ web/notes/notes.js      ★ 笔记渲染器产物（marked + highlight.js 打包结果，已进仓库）
├─ editor-src/index.js     ★ 智能编辑器源码（改完 `npm run build:editor`）
├─ notes-src/index.js      ★ 笔记渲染器源码（改完 `npm run build:notes`）
├─ package.json            ★ 前端构建脚本与依赖（esbuild + CodeMirror / marked / highlight.js）
├─ docs/                   ★ GitHub Pages 发布目录（由 export_static.py 生成）
│  ├─ index.html           前端副本
│  ├─ problems.json        题库快照（含 subject / choices，**不含参考答案**）
│  ├─ editor/editor.js     ★ 编辑器副本
│  ├─ notes/               ★ 笔记区：index.json（目录树）+ p/<slug>.json（480 篇）
│  │                            + search.json（全文索引）+ notes.js（渲染器）
│  └─ .nojekyll            别让 Jekyll 处理
├─ tools/
│  ├─ selfcheck.py         判题内核 + 评分 自检（62 项）
│  ├─ selftest_sandbox.py  ★ 沙箱跨平台自检（19 项，部署后在容器里跑它）
│  ├─ selftest_cpp.py      ★ C/C++ 双通道自检（9 项：AC/CE/WA/TLE/产物不串/别名）
│  ├─ selftest_theory.py   ★ 理论题判题自检（14 项：含「错答案必须判错」的反向验证）
│  ├─ smoke_cloud.py       ★ 云端启动路径自检（13 项：真用 PTA_CLOUD+$PORT 起进程、真编 C++）
│  ├─ e2e_ui.py            ★ 端到端过 HTTP（33 项：前端真正走的那条路）
│  ├─ httptest_users.py    ★ 多用户隔离自检（23 项，自己起服务）
│  ├─ httptest_split.py    ★ 跨源（Pages + 后端）自检（18 项，含 CORS 预检）
│  ├─ httptest.py          HTTP 层自检（18 项，需服务在跑）
│  ├─ gen_ds_bank.py       ★ 数据结构题库生成器（含 _sanity 把关）
│  ├─ gen_linux_bank.py    ★ Linux 题库生成器（含 _sanity 把关）
│  ├─ verify_bank.py       题库校验（三线双实现撞独立算出的期望输出）
│  ├─ ui_e2e_editor.mjs    ★ 智能编辑器真浏览器测试（63 项：缩进/配对/补全/Tab/切题/回退/语言切换）
│  ├─ ui_e2e_notes.mjs     ★ 笔记区真浏览器测试（29 项：目录树/双链重名消歧/锚点/搜索/题目互跳）
│  ├─ export_notes.py      ★ 把 Obsidian vault 导成笔记区数据（480 篇，Obsidian 语法 → 前端 markdown）
│  ├─ _console.py          ★ 把控制台切成 UTF-8（被上面这些脚本 import）
│  ├─ _testdb.py           ★ 把自检脚本的库钉到测试库（导入即生效，别写进真实库）
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
D:\Pythontools\Python\python.exe -X utf8 tools\selfcheck.py         &rem 62 项：判题内核 + 评分
D:\Pythontools\Python\python.exe -X utf8 tools\selftest_sandbox.py  &rem 19 项：沙箱（跨平台）
D:\Pythontools\Python\python.exe -X utf8 tools\selftest_cpp.py      &rem  9 项：C/C++ 双通道
D:\Pythontools\Python\python.exe -X utf8 tools\selftest_theory.py   &rem 14 项：理论题正反双向
D:\Pythontools\Python\python.exe -X utf8 tools\smoke_cloud.py       &rem 13 项：云端启动路径（自起进程，含真编 C++）
D:\Pythontools\Python\python.exe -X utf8 tools\e2e_ui.py 8792       &rem 33 项：端到端过 HTTP（需服务）
D:\Pythontools\Python\python.exe -X utf8 tools\httptest_users.py    &rem 23 项：多用户隔离（自起服务）
D:\Pythontools\Python\python.exe -X utf8 tools\httptest_split.py    &rem 18 项：跨源 CORS（自起两个源）
D:\Pythontools\Python\python.exe -X utf8 tools\verify_bank.py       &rem 三线双实现对拍
D:\Pythontools\Python\python.exe -X utf8 tools\httptest.py          &rem 18 项：HTTP（需服务已在跑）
D:\Pythontools\Python\python.exe -X utf8 tools\reset_progress.py    &rem 清空记录（加 --yes 才真删）
```

`selftest_sandbox` / `selftest_cpp` / `selftest_theory` / `smoke_cloud` /
`httptest_users` / `httptest_split`
会**自己起服务、测完自己关**，不依赖外部状态，适合部署后在容器里立刻确认环境。

CI（`.github/workflows/ci.yml`）在 Ubuntu 和 Windows 上各跑一遍 ——
**Linux 那份专门用来验证沙箱的 setrlimit + killpg 分支**（本机是 Windows，测不到）。

前端另有一组 **Node 测试**（不依赖 Python、不在 CI 里跑，因为要真浏览器）：

```bat
cd /d E:\学习\001\pta
set NODE_MODULES_DIR=E:\学习\001\pta  &rem ★ jsdom 测试要它；必须绝对路径（写 . 会 ERR_INVALID_ARG_VALUE）
node tools\ui_smoke.mjs              &rem jsdom 冒烟：界面渲染、路由、提交流程（41 项）
node tools\ui_test_local_judge.mjs   &rem 本地判题（含草稿导入导出）（45 项）
node tools\ui_e2e_local_judge.mjs    &rem 真 Chrome 跑发布产物的判题全流程
node tools\ui_e2e_editor.mjs         &rem ★ 真 Chrome 测智能编辑器（63 项，约 2 分钟）
node tools\ui_e2e_notes.mjs          &rem ★ 真 Chrome 测笔记区（29 项，含 3 MB 搜索索引首次加载）
node tools\ui_e2e_local_engines.mjs  &rem ★ 真 Chrome 测浏览器判题引擎的「下载被掐→重试恢复」（C/C++ 5 项；Python 2 项本机拦 .zip 时跳过）
node tools\verify_text_judge.mjs     &rem 前端判题器口径与后端对拍
```

`ui_e2e_editor.mjs` 是本机唯一会**真的敲键盘**的测试：它用系统 Chrome 打开 `docs/` 静态站点，
逐条验证缩进、括号配对、补全面板、Tab / Shift+Tab / `Esc`+`Tab`、切题草稿、C↔C++ 语言切换，
以及「加载失败回退到 `textarea` 且不缓存失败」。跑之前确保 `docs/` 是刚导出的。

★ 三条实操注意：

- `verify_bank.py` 会**编译 / 运行**东西，别跟一个正在跑的服务同时跑
  （早期两者共用判题临时目录，服务启动时的崩溃兜底清理会把对拍编译出来的文件删掉，
  表现成一串 `can't open file ... main.py` 的 RE。现在对拍用独立目录，不会再撞）。
- `selfcheck.py` 会往库里**插 11 条测试提交**（AC / WA / RE / TLE / CE / MLE 各一条）。
  ★ 所以它**默认只对着测试库** `data/_bank_test.db` 跑，**不会碰你的真实进度**；
  真要对着真实库跑（上线前验收之类）显式加 `--live`，脚本会把这件事喊出来。
- ★ **所有会写库的自检都在测试库上跑**，靠 `tools/_testdb.py` 保证（导入即生效，
  把 `PTA_DB` 钉到 `data/_bank_test.db`）。`httptest_users` / `httptest_split` 开跑前还会
  把测试库**删掉重建** —— 它们用固定通行证、断言「历史条数 = 1」，
  不干净的库会让第二次跑假失败。`e2e_ui` / `httptest` 连的是别人起好的服务，
  决定不了库，但会先读 `/api/health` 把库路径打出来警告你。
- ★ **这台机器启动进程本身要 160~400 ms**（两套杀软的实时扫描；实测一个立刻 `return 0` 的
  空 C 程序也要 164 ms）。所以本机量出来的运行时间有一大块不是代码耗时，
  1000 ms 的题目限制里学生代码实际只剩 600~800 ms，临界题会偶发 TLE。
  **云端和 CI 没这个问题** —— 所以别去调题库的时间限制（那是给学生的约束）。
  想自己复核这个数：编译一个空 C 程序，`tools/` 下的沙箱跑十遍看 `time_ms`。

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
