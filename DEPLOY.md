# 部署到网上（GitHub Pages 前端 + 后端判题）

目标：**让网页进一步支持 C/C++ 判题和后端进度。** Linux 理论题与 Python 编程题已经可直接在 GitHub Pages 的浏览器中判，无需按本文部署后端。

为什么是「前端 + 后端」两半，而不是全塞进 GitHub Pages：

| | GitHub Pages | 判题后端 |
|---|---|---|
| 能干什么 | 发静态文件 | 跑 Python / C / C++ 代码、真判题 |
| 成本 | 免费、永久、秒开 | 见下面三选一 |
| 能不能判题 | ❌ 纯静态，跑不了代码 | ✅ |

所以：**题目浏览 + 你的进度**在 Pages 上；**真判题**连后端。

> 前端已经部署好了：<https://cosy119.github.io/my-pta/>
> 下面只需要挑一个后端。

---

## 一、先搞清楚一个坑：进度要靠「持久化磁盘」

后端的题库**不用管** —— 它每次启动会从代码里重建（204 题 532 个测试点都在 `app/problems_bank*.py`）。
会丢的只有**做题记录**（`submissions` / `mastery`）。

| 平台 | 价格 | 持久化磁盘 | 结果 |
|---|---|---|---|
| Render 免费档 | $0 | ❌ **官方明确不支持** | 15 分钟没人访问就休眠，**休眠/重启/重新部署后进度全部归零** |
| Render Starter | $7/月 + 磁盘 $0.25/月 | ✅ | 不休眠，进度稳定留着 |
| 你自己的 VPS | 已付费 | ✅ | 免费，但要和 3x-ui 抢 1 核 / 1 GB |

★ 网上很多教程让你「在 Render 免费档挂个 Disk」—— **现在做不到了**。
Render 2026 年的免费档限制里写得很清楚：free web service 无 SSH、**无持久化磁盘**、
重启即丢本地文件。所以要么付 $7，要么换地方。

---

## 二、部署方式 A：Render（最省事）

### 1. 建服务

1. 打开 <https://dashboard.render.com/blueprints>，用 GitHub 账号登录
2. **New Blueprint Instance** → 选仓库 `cosy119/my-pta`
3. Render 读 `render.yaml`，配置基本都填好了；点确认
4. 等构建 3~6 分钟（要装 gcc/g++，比纯 Python 慢）
5. 记下网址，形如 `https://my-pta.onrender.com`
6. 打开 `<网址>/api/health`，看到 `{"ok":true,...}` 就成了

### 2. 关于「要不要留进度」

`render.yaml` 默认 `plan: free`，**能跑但不留进度**（见上面的表）。

想留进度，改两处：

```yaml
    plan: starter        # ① free → starter（$7/月）
```

```yaml
    # ② 把文件末尾这段前面的注释去掉
    disk:
      name: pta-data
      mountPath: /data
      sizeGB: 1
```

### ★ 两个必须知道的配置要点

**① 必须用 Docker 运行时。** 数据结构线的 C/C++ 题要真编译，
而 Render 的原生 python 运行时**不带 gcc/g++** —— 用原生运行时一提交 C++ 就是 CE。
`render.yaml` 里已经是 `runtime: docker`，镜像见 `Dockerfile`。

**② 免费档只有 0.1 vCPU / 512 MB。** 编译 C++ 会慢，计算量大的题
可能比在你本机更早撞上时间限制。个人刷题够用，想舒服点上 starter（0.5 vCPU）。

### 3. 换成 Railway / Fly.io（可选）

都一样，关键是四条：

```
运行时   : Docker（镜像里必须装 gcc g++，否则 C/C++ 题全 CE）
启动命令 : python run.py          （Dockerfile 的 CMD 已经写好了）
健康检查 : /api/health
环境变量 : PTA_CLOUD=1            ← 让它绑 0.0.0.0:$PORT、不开浏览器
           PTA_DB=/data/pta.db    ← 指向持久化卷（挂了卷才有意义）
```

`run.py` 见到 `$PORT` 或 `PTA_CLOUD` 就自动走云端模式，不用改代码。
**不用手动设 `HOST`** —— 有 `PTA_CLOUD` / `PORT` 时会自动绑 `0.0.0.0`。

---

## 三、部署方式 B：自己的 VPS（如果不想每月付 $7）

你手上的 HostPapa VPS（1 核 E5-2680v2 / 1 GB / 18 GB）能跑，但**它同时在做 3x-ui 代理**，
判题（尤其 g++ 编译）会抢 CPU 和内存，可能把代理拖卡。要跑的话：

```bash
# 在 VPS 上（有 Docker 的话）
git clone https://github.com/cosy119/my-pta.git && cd my-pta
docker build -t my-pta .
docker run -d --name my-pta -p 8000:8000 \
  -e PORT=8000 -e PTA_CLOUD=1 \
  -e PTA_DB=/data/pta.db -e PTA_LOGS=/data/logs \
  -v /root/pta-data:/data \
  my-pta
```

> 1 GB 内存跑 g++ 会紧张，建议给容器加 `--memory=600m` 之类的上限，
> 别让它把 Xray 一起拖垮。
> 端口对外要放行（`firewall-cmd`），想上 HTTPS 就在前面挂个 Nginx。

---

## 四、前端（已经做好了，这里只是说明）

1. 仓库 → **Settings → Pages** → Source 选 `Deploy from a branch`，
   Branch `main`，目录 **`/docs`**
2. 网址：`https://cosy119.github.io/my-pta/`
3. 打开后点右上角 **设置**，填后端地址（如 `https://my-pta.onrender.com`），回车即可。
   地址存在浏览器里，下次自动连。

> 想让别人一步到位，把网址写成
> `https://cosy119.github.io/my-pta/?api=https://my-pta.onrender.com`
> —— 打开就自动配好后端。

---

## 五、每个人的进度怎么存的

**没有账号密码**。第一次打开时你的浏览器生成一串随机通行证（存在 localStorage），
之后每次请求都带上它，后端按它区分是谁。所以：

- ✅ 同一台电脑、同一个浏览器 → 关掉再打开，进度还在（前提是后端有持久化磁盘）
- ✅ 换个浏览器 / 换台电脑 → **是另一份全新进度**（天然隔离）
- ⚠️ **清浏览器数据 = 丢那份通行证**（后端数据还留着，但你找不回它了）
- 💡 想跨设备接同一份进度：点右上角你的名字 → 弹出框里有通行证，
  抄到新设备的 localStorage（键名 `pta.userToken`）即可

> 想更保险就定期在本地跑 `python tools/backup_db.py export -o 我的进度.json`。

---

## 六、加题之后要做什么

改了题库（`app/problems_bank*.py`、或重新跑了 `tools/gen_ds_bank.py` / `tools/gen_linux_bank.py`）之后：

```bash
python tools/export_static.py     # 重新导出 docs/problems.json ★ 忘了这步，线上还是旧题库
git add docs/ && git commit -m "加题" && git push
```

Render 会自动重新部署，Pages 也会更新。

> 线上题库是 `docs/problems.json` 那份**静态快照**（离线浏览 + 没连后端时用）。
> 后端自己的题库则来自启动时的 `seed.ensure()` —— 按标题判重，**已有题不会被覆盖**，
> 所以改了某道题的题面 / 分值 / 案例，只重新部署是**不生效**的：
> 要么改标题，要么手动改库。加新题则不受影响。

---

## 七、排查

| 症状 | 原因 | 怎么办 |
|---|---|---|
| 页面能开，右上角显示「离线浏览」 | 没填后端地址，或后端在休眠 | 点「设置」填地址；等 30 秒再刷新 |
| 提交后一直「排队中」 | 后端挂了 | 打开 `<后端>/api/health` 看还在不在 |
| **部署后进度全没了** | **免费档没有持久化磁盘**（见第一节） | 升级 starter 并解开 `render.yaml` 里的 disk 段 |
| **服务起不来，日志 `NameError: name 'config' is not defined`** | 老版本 `run.py` 云分支的 bug | 拉最新代码（已修）；本地可跑 `python tools/smoke_cloud.py` 自检 |
| **部署判「不健康」但容器内部能连** | 绑到了 `127.0.0.1` | 拉最新代码（`host_env` 已修）；确认有设 `PTA_CLOUD=1` |
| 数据结构题交上去总是 CE | 镜像里没有 gcc/g++ | `render.yaml` 必须是 `runtime: docker`（见第二节 ★①） |
| 数据结构题交上去总是 CE（另一种） | 语言选错了（C 的写法交给 C++ 编译器，或反过来） | 答题页右上角切换语言；教材里的 `&` 引用用 gcc 编不过，改用 C++ 交即可 |
| 判题报 IE | 容器里解释器路径不对 | 容器用 `python run.py` 起，会兜底探测 `python3` / `gcc`；`Dockerfile` 已装好工具链 |
| 想确认容器判题正常 | — | 在 Render 的 Shell 里跑 `python tools/smoke_cloud.py`（13 项，含真编 C++） |
