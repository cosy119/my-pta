# 部署到网上（GitHub Pages 前端 + 免费后端判题）

目标：**你（或别人）打开一个网址就能刷题，每人进度各自独立。**

为什么是「前端 + 后端」两半，而不是全塞进 GitHub Pages：

| | GitHub Pages | 判题后端 |
|---|---|---|
| 能干什么 | 发静态文件 | 跑 Python/C 代码、真判题 |
| 成本 | 免费、永久、秒开 | 免费额度够用，会休眠 |
| 能不能判题 | ❌ 纯静态，不能跑 Python | ✅ |

所以：**题目浏览 + 你的进度**在 Pages 上；**真判题**连后端。

---

## 一、后端（约 5 分钟）

推荐 **Render**（能直接读仓库里的 `render.yaml`，配置最简单）。

### 1. 建服务

1. 打开 <https://render.com>，用 GitHub 账号登录
2. **New → Web Service** → 选仓库 `cosy119/my-pta`
3. Render 会读到 `render.yaml`，配置基本都填好了
4. 唯一要确认的两件事：
   - **Environment 里要有 `PTA_DB=/data/pta.db`**（`render.yaml` 已写）
   - **挂一个 Disk 到 `/data`**（`render.yaml` 已写 `sizeGB: 1`）
     > ★ **不挂 Disk 的话，每次重新部署你所有进度就没了。** 这是最容易踩的坑。

5. 点 **Create Web Service**，等 2~5 分钟构建完
6. 记下 Render 给你的网址，形如 `https://my-pta.onrender.com`
7. 打开 `<网址>/api/health`，看到 `{"ok":true,...}` 就成了

> 免费实例 **15 分钟没人访问会休眠**，下次打开要等约 30 秒冷启动。
> 想避免就换 Railway（有 5 美元试用额度）或 Fly.io。

### 2. 换成 Railway / Fly.io（可选）

都一样，关键是三条：

```
启动命令 : python run.py
健康检查 : /api/health
环境变量 : PTA_DB=/data/pta.db   ← 指向持久化卷
           PTA_CLOUD=1           ← 让它绑 0.0.0.0:$PORT、不开浏览器
```

`run.py` 见到 `$PORT` 或 `$PTA_CLOUD` 就自动走云端模式，不用改代码。

---

## 二、前端（约 2 分钟）

### 1. 打开 Pages

1. 仓库 → **Settings → Pages**
2. **Source** 选 `Deploy from a branch`
3. **Branch** 选 `main`，目录选 **`/docs`** → Save
4. 等 1~2 分钟，网址是 `https://cosy119.github.io/my-pta/`

### 2. 指向前端到后端

打开 Pages 网址，点右上角 **设置**，填后端地址（如 `https://my-pta.onrender.com`），
回车即可。地址存在浏览器里，下次自动连。

> 想让别人一步到位：把网址写成
> `https://cosy119.github.io/my-pta/?api=https://my-pta.onrender.com`
> —— 打开就自动配好后端。

---

## 三、每个人的进度怎么存的

**没有账号密码**。第一次打开时你的浏览器生成一串随机通行证（存在 localStorage），
之后每次请求都带上它，后端按它区分是谁。所以：

- ✅ 同一台电脑、同一个浏览器 → 关掉再打开，进度还在
- ✅ 换个浏览器 / 换台电脑 → **是另一份全新进度**（天然隔离）
- ⚠️ **清浏览器数据 = 丢那份进度**（后端还留着，但你找不回通行证了）
- 💡 想跨设备接同一份进度：点右上角你的名字 → 弹出框里有通行证，
  抄到新设备的 localStorage（键名 `pta.userToken`）即可

> 想更保险就定期在本地跑 `python tools/backup_db.py export -o 我的进度.json`。

---

## 四、加题之后要做什么

改了题库（`app/problems_bank*.py`）之后：

```bash
python tools/export_static.py     # 重新导出 docs/problems.json
git add docs/ && git commit -m "加题" && git push
```

Render 会自动重新部署，Pages 也会更新。

---

## 五、排查

| 症状 | 原因 | 怎么办 |
|---|---|---|
| 页面能开，右上角显示「后端未连接」 | 没填后端地址，或后端在休眠 | 点「设置」填地址；等 30 秒再刷新 |
| 提交后一直「排队中」 | 后端挂了 | 打开 `<后端>/api/health` 看还在不在 |
| 部署后进度全没了 | **没挂持久化 Disk** | 见上面「★」那一条，挂 Disk 到 `/data` |
| 判题报 IE | 容器里 Python 路径不对 | 容器用 `python run.py` 起，解释器会自动探测 |
| 想确认容器判题正常 | — | 在 Render 的 Shell 里跑 `python tools/selftest_sandbox.py` |
