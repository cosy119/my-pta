"""FastAPI 入口。

启动顺序：建表 → 清残留判题目录 → 写种子题 → 标记中断的提交 → 起判题线程。
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from . import config, db, seed
from .api import mastery, problems, submissions
from .judge import sandbox
from .judge.worker import get_worker

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-7s %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("pta")

WEB_DIR = config.ROOT / "web"


@asynccontextmanager
async def lifespan(app: FastAPI):
    cfg = config.get()

    db.init_db()
    log.info("数据库就绪：%s", cfg.db_path)
    cols = db.last_migration()
    if cols:
        log.info("数据库补列（老库升级）：%s", ", ".join(cols))

    n = sandbox.clean_tmp_root(cfg.tmp_judge)
    if n:
        log.info("清掉 %d 个上次残留的判题目录", n)

    added = seed.ensure()
    if added:
        log.info("写入 %d 道种子题", added)

    typed = seed.sync_question_types()
    if typed:
        log.info("标注了 %d 道题的题型", typed)

    fixed = seed.backfill_points()
    if fixed:
        log.info("同步了 %d 道题的测试点分值", fixed)

    # 选择题的期望值原本只有选项字母；把选项正文也加成可接受答案，
    # 这样「点选项」和「填字母」两种提交都判得过
    choice_alts = seed.backfill_choice_alts()
    if choice_alts:
        log.info("给 %d 道选择题补上了「选项正文」这种答案写法", choice_alts)

    n_legacy = seed.backfill_legacy_scores()
    if n_legacy:
        log.info("换算 %d 条老提交的分数（旧口径 → 得分制）", n_legacy)

    # 服务重启前卡在 pending/judging 的提交，一律标成 IE，免得前端一直转圈
    stuck = db.execute(
        "UPDATE submissions SET verdict='IE', message='服务重启，本次判题中断' "
        "WHERE verdict IN ('pending', 'judging')")
    if stuck:
        log.info("标记 %d 条中断的提交", stuck)

    get_worker().start()
    log.info("就绪 → http://%s:%s", cfg.host_env, cfg.port_env)

    yield

    get_worker().stop()
    log.info("已停止判题线程")


app = FastAPI(title="本地 AI 出题 + 批改平台", version="0.2.0", lifespan=lifespan)

# ★ CORS：前端要能放在 GitHub Pages（另一个域名）上，后端只提供 API。
# 允许的来源由 settings.toml [server] allow_origins 控制；默认 "*" 适合个人学习平台
# （身份靠 X-User-Token 而不是 cookie，所以不需要 allow_credentials）。
_cors = config.get().allow_origins or ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors,
    allow_origin_regex=r"https://.*\.github\.io",   # 顺手放行 Pages 的预览域名
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(problems.router)
app.include_router(submissions.router)
app.include_router(mastery.router)   # 收藏 / 错题本 / 备注（mastery 的写通道）

if WEB_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(WEB_DIR)), name="static")


@app.get("/")
def index():
    return FileResponse(str(WEB_DIR / "index.html"))


@app.get("/api/health")
def health():
    cfg = config.get()
    return {
        "ok": True,
        # ★ 报实际监听的 host/port（云端是 0.0.0.0:$PORT），
        #   不是配置里那份 —— 否则在 Render 上看到 "port":8765 会一脸问号。
        "host": cfg.host_env,
        "port": cfg.port_env,
        "pending": get_worker().pending(),
        "db": str(cfg.db_path),
        "web": str(WEB_DIR),
    }
