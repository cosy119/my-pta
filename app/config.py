"""平台配置：读 config/settings.toml，解析成绝对路径。

平台只读配置、不写回（避免把注释和顺序搞乱）。Python 3.11+ 自带 tomllib。
"""
from __future__ import annotations

import os
import shutil
import tomllib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent          # E:\学习\001\pta
CONFIG_PATH = ROOT / "config" / "settings.toml"

_DEFAULTS: dict[str, dict[str, Any]] = {
    "server": {"host": "127.0.0.1", "port": 8765, "allow_origins": ["*"]},
    "paths": {
        "db": "data/pta.db",
        "tmp_judge": "data/tmp/judge",
        "media": "data/media",
        "logs": "data/logs",
    },
    "interpreters": {"py313": "", "py314": "", "default": "py313"},
    "compilers": {"gcc": "", "gpp": ""},
    "judge": {
        "concurrency": 1,
        "default_time_limit_ms": 1000,
        "default_memory_limit_mb": 256,
        "max_output_bytes": 1048576,
        "kill_grace_ms": 300,
    },
    "shell": {
        "ssh_target": "",
        "ssh_key": "",
        "remote_tmp": "/tmp/pta-judge",
        "ssh_timeout_s": 15,
    },
    "ai": {
        "key_env": "OPENAI_API_KEY",
        "default_base_url": "https://api.deepseek.com/v1",
        "default_model": "deepseek-chat",
        "temperature": 0.3,
        "timeout_s": 120,
        "slice_max_chars": 6000,
    },
}

_cache: "Settings | None" = None


class Settings:
    """点号取值 + 路径解析。所有路径都返回绝对 Path。"""

    def __init__(self, data: dict[str, Any], config_path: Path = CONFIG_PATH):
        self._data = data
        self.config_path = config_path

    # ---- 取值 ----
    def get(self, section: str, key: str, default: Any = None) -> Any:
        return self._data.get(section, {}).get(key, default)

    def section(self, name: str) -> dict[str, Any]:
        return dict(self._data.get(name, {}))

    # ---- 常用快捷方式 ----
    @property
    def host(self) -> str:
        return str(self.get("server", "host"))

    @property
    def port(self) -> int:
        return int(self.get("server", "port"))

    @property
    def allow_origins(self) -> list[str]:
        """CORS 允许的来源。默认 ["*"]（个人学习平台，身份走 X-User-Token）。

        可用环境变量 `PTA_ALLOW_ORIGINS` 收紧（逗号分隔），例如
        `PTA_ALLOW_ORIGINS=https://cosy119.github.io`。
        """
        env = os.environ.get("PTA_ALLOW_ORIGINS")
        if env:
            return [s.strip() for s in env.split(",") if s.strip()]
        v = self.get("server", "allow_origins", ["*"])
        if isinstance(v, str):
            return [s.strip() for s in v.split(",") if s.strip()]
        return list(v or ["*"])

    @property
    def host_env(self) -> str:
        """云平台会注入 $PORT 并要求绑 0.0.0.0。

        ★ 顺序很重要：`HOST` 环境变量优先；没写 HOST 但明显在云上
        （有 `PORT` 或 `PTA_CLOUD`）就必须绑 `0.0.0.0` —— 否则会绑到
        `127.0.0.1`，容器内部自己连得通、平台健康检查却连不上，
        部署直接判失败。（本地跑仍然绑 127.0.0.1，别把服务暴露到局域网。）
        """
        h = os.environ.get("HOST", "").strip()
        if h:
            return h
        if os.environ.get("PTA_CLOUD") or os.environ.get("PORT"):
            return "0.0.0.0"          # noqa: S104 —— 容器里必须监听全网卡
        return self.host

    @property
    def port_env(self) -> int:
        """云平台注入的 $PORT 优先（Render/Railway/Fly 都是这个约定）。"""
        p = os.environ.get("PORT")
        try:
            return int(p) if p else self.port
        except ValueError:
            return self.port

    @property
    def concurrency(self) -> int:
        return max(1, int(self.get("judge", "concurrency", 1)))

    @property
    def default_time_limit_ms(self) -> int:
        return int(self.get("judge", "default_time_limit_ms", 1000))

    @property
    def default_memory_limit_mb(self) -> int:
        return int(self.get("judge", "default_memory_limit_mb", 256))

    @property
    def max_output_bytes(self) -> int:
        return int(self.get("judge", "max_output_bytes", 1048576))

    @property
    def kill_grace_ms(self) -> int:
        return int(self.get("judge", "kill_grace_ms", 300))

    @property
    def interpreters(self) -> dict[str, str]:
        return self.section("interpreters")

    @property
    def compilers(self) -> dict[str, str]:
        return self.section("compilers")

    # ---- 路径 ----
    def path(self, key: str) -> Path:
        """按 [paths] 里的名字取绝对路径。

        ★ 环境变量 `PTA_<KEY>` 优先（如 `PTA_DB=/data/pta.db`）。
        云平台的持久化卷挂载点跟仓库目录不是一个地方，必须能外部指定，
        否则容器一重启进度就没了。
        """
        env = os.environ.get("PTA_" + key.upper())
        if env:
            p = Path(env)
            return p if p.is_absolute() else (ROOT / p)
        rel = self.get("paths", key)
        if rel is None:
            raise KeyError(f"settings.toml [paths] 缺少 {key!r}")
        p = Path(str(rel))
        return p if p.is_absolute() else (ROOT / p)

    @property
    def db_path(self) -> Path:
        return self.path("db")

    @property
    def tmp_judge(self) -> Path:
        return self.path("tmp_judge")

    @property
    def media_dir(self) -> Path:
        return self.path("media")

    @property
    def logs_dir(self) -> Path:
        return self.path("logs")

    # ---- 解释器 / 编译器挑选 ----
    def interpreter_path(self, name: str | None) -> str:
        """name 形如 py313 / py314；认不出就回退 default。

        配置里的路径在原机器上可能是对的，但克隆到别的机器就失效了。
        所以这里做一层**兜底探测**：配置的路径不存在时，自动去找
        `python` / `python3` / 本机常见安装位置，找到就用，避免「配置写死了
        某个人的路径 → 别人克隆下来跑不了」。
        """
        interps = self.interpreters
        chosen = name or str(interps.get("default") or "py313")
        path = str(interps.get(chosen) or "")
        if not path:
            path = str(interps.get(str(interps.get("default"))) or "")
        if path and Path(path).exists():
            return path
        return _probe_python(path)

    def compiler_path(self, name: str) -> str:
        """gcc / g++ 路径。同样带兜底探测（Windows 上常见 mingw64 位置）。"""
        comps = self.compilers
        if name in ("c", "gcc"):
            want = "gcc"
        elif name in ("cpp", "g++", "gpp"):
            want = "gpp"
        else:
            return ""
        path = str(comps.get(want) or "")
        if path and Path(path).exists():
            return path

        exe = "gcc.exe" if want == "gcc" else "g++.exe"
        cands = [shutil.which(want), shutil.which("gcc" if want == "gcc" else "g++")]
        for drive in ("C:", "D:", "E:"):
            for pat in ("Programs/mingw64/bin/", "mingw64/bin/", "msys64/mingw64/bin/",
                        "Program Files/mingw64/bin/"):
                cands.append(str(Path(drive + "/") / pat / exe))
        for c in cands:
            if c and Path(c).exists():
                return c
        return path

    # ---- AI key 解析：环境变量优先 ----
    def resolve_api_key(self, stored_key: str = "", stored_env: str = "") -> str:
        env_name = stored_env or str(self.get("ai", "key_env") or "")
        if env_name:
            v = os.environ.get(env_name)
            if v:
                return v
        return stored_key or ""

    def to_dict(self) -> dict[str, Any]:
        return self._data


# --------------------------------------------------------------------- #
# 解释器探测：配置里的路径失效时找本机的 Python
# --------------------------------------------------------------------- #
_probe_cache: dict[str, str] = {}


def _probe_python(configured: str = "") -> str:
    """配置里的解释器不可用时，在本机找一个能用的。

    顺序：PATH 上的 python / python3 → Windows 常见安装位置 → 本机 Python 工具目录。
    找到就返回，都找不到就原样返回配置值（上层会报「解释器不存在」，信息更明确）。
    """
    key = configured or "__auto__"
    if key in _probe_cache:
        return _probe_cache[key]

    cands: list[str] = []

    # 1) PATH 里能直接调起来的
    for exe in ("python", "python3"):
        p = shutil.which(exe)
        if p:
            cands.append(p)

    # 2) Windows 常见位置 / py launcher
    launcher = shutil.which("py")
    if launcher:
        cands.append(launcher)
    local = Path(os.environ.get("LOCALAPPDATA") or "")
    if local:
        cands += sorted(str(p) for p in (local / "Programs" / "Python").glob("Python*/python.exe"))
    for drive in ("C:", "D:", "E:"):
        cands += sorted(str(p) for p in Path(drive + "/").glob("Pythontools/Python/python.exe"))
        cands += sorted(str(p) for p in Path(drive + "/").glob("Python*/python.exe"))

    if configured:
        cands.append(configured)          # 保底：还是用它，报错更明确

    for c in cands:
        if c and Path(c).exists():
            _probe_cache[key] = c
            return c

    _probe_cache[key] = configured
    return configured


def _deep_merge(base: dict, over: dict) -> dict:
    out = dict(base)
    for k, v in (over or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load(config_path: Path | None = None) -> Settings:
    """读取配置并与默认值合并（缺项用默认值补）。"""
    path = Path(config_path) if config_path else CONFIG_PATH
    raw: dict[str, Any] = {}
    if path.exists():
        with open(path, "rb") as f:
            raw = tomllib.load(f)
    return Settings(_deep_merge(_DEFAULTS, raw), path)


def get(refresh: bool = False) -> Settings:
    """取全局单例配置。"""
    global _cache
    if _cache is None or refresh:
        _cache = load()
    return _cache
