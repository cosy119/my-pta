"""平台配置：读 config/settings.toml，解析成绝对路径。

平台只读配置、不写回（避免把注释和顺序搞乱）。Python 3.11+ 自带 tomllib。
"""
from __future__ import annotations

import os
import tomllib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent          # E:\学习\001\pta
CONFIG_PATH = ROOT / "config" / "settings.toml"

_DEFAULTS: dict[str, dict[str, Any]] = {
    "server": {"host": "127.0.0.1", "port": 8765},
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
        """按 [paths] 里的名字取绝对路径。"""
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
        """name 形如 py313 / py314；认不出就回退 default。"""
        interps = self.interpreters
        chosen = name or str(interps.get("default") or "py313")
        path = str(interps.get(chosen) or "")
        if not path:
            path = str(interps.get(str(interps.get("default"))) or "")
        return path

    def compiler_path(self, name: str) -> str:
        comps = self.compilers
        if name in ("c", "gcc"):
            return str(comps.get("gcc") or "")
        return str(comps.get("gpp") or "")

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
