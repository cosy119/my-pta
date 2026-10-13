# 判题后端的容器镜像（部署到 Render / Railway / Fly.io 用）
#
# 要点：
# - Python 标准库 + 4 个纯 Python 包 + C/C++ 编译器（数据结构线要真编；gcc/g++ 约 200 MB）
# - 判题要跑用户代码，所以**不能**用 distroless；用 slim 但去掉多余工具
# - 数据库路径由 PTA_DB 环境变量指向持久化卷（见 render.yaml / 部署说明）
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUTF8=1 \
    PYTHONIOENCODING=utf-8 \
    PTA_CLOUD=1

WORKDIR /app

# ★ 数据结构线要真编 C / C++，镜像里必须有编译器。
#   只用标准库的题目其实只要 gcc；但教材里的 `&` 引用之类写法在 gcc 下编不过，
#   学生可以改用 C++ 提交 —— 所以 g++ 也得在。
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc g++ libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# 先装依赖（利用层缓存：只要 requirements 没变，改代码不会重装）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY config/ ./config/
COPY web/ ./web/
COPY run.py .

# 云端通常以非 root 跑；建个目录给判题临时文件 + 数据库兜底
RUN mkdir -p /data /app/data/tmp/judge /app/data/logs \
    && (id -u pta >/dev/null 2>&1 || useradd -m pta) \
    && chown -R pta:pta /app /data

USER pta

# 数据库默认放 /data（挂持久化卷的地方）；没挂卷也能跑，只是重启会丢
ENV PTA_DB=/data/pta.db \
    PTA_LOGS=/data/logs \
    PTA_TMP_JUDGE=/tmp/pta-judge

EXPOSE 8765

# run.py 见到 $PORT / $PTA_CLOUD 就直接绑 0.0.0.0:$PORT，不开浏览器
CMD ["python", "run.py"]
