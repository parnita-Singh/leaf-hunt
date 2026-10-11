"""Load and validate config.toml. Nothing in this module talks to a model."""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlparse

LOOPBACK_HOSTS = frozenset({"127.0.0.1", "localhost", "::1"})


class ConfigError(ValueError):
    """Invalid or missing configuration."""


@dataclass(frozen=True)
class Config:
    region: str
    last_spring_frost: date
    data_dir: Path
    backend: str
    vlm_model: str
    stt_model: str
    tts_voice: str
    low_confidence_threshold: float
    ollama_host: str
    source_path: Path


def default_config_path() -> Path:
    """Prefer LEAF_HUNT_CONFIG, then ./config.toml, then the repo copy."""
    env = os.environ.get("LEAF_HUNT_CONFIG")
    if env:
        return Path(env).expanduser()

    cwd_copy = Path.cwd() / "config.toml"
    if cwd_copy.is_file():
        return cwd_copy

    repo_copy = Path(__file__).resolve().parents[2] / "config.toml"
    return repo_copy


def load_config(path: Path | None = None) -> Config:
    config_path = path or default_config_path()
    if not config_path.is_file():
        raise ConfigError(f"config not found: {config_path}")

    with config_path.open("rb") as fh:
        raw = tomllib.load(fh)

    models = raw.get("models")
    if not isinstance(models, dict):
        raise ConfigError("missing [models] table")

    region = _require_str(raw, "region")
    frost = _parse_iso_date(_require_str(raw, "last_spring_frost"), "last_spring_frost")
    data_dir = Path(_require_str(raw, "data_dir")).expanduser()
    if not data_dir.is_absolute():
        data_dir = (config_path.parent / data_dir).resolve()

    backend = _require_str(models, "backend")
    vlm_model = _require_str(models, "vlm_model")
    stt_model = _require_str(models, "stt_model")
    tts_voice = _require_str(models, "tts_voice")
    threshold = _require_float(models, "low_confidence_threshold")
    if not 0.0 <= threshold <= 1.0:
        raise ConfigError("low_confidence_threshold must be between 0 and 1")

    ollama_host = _require_str(models, "ollama_host")
    _assert_loopback(ollama_host)

    return Config(
        region=region,
        last_spring_frost=frost,
        data_dir=data_dir,
        backend=backend,
        vlm_model=vlm_model,
        stt_model=stt_model,
        tts_voice=tts_voice,
        low_confidence_threshold=threshold,
        ollama_host=ollama_host,
        source_path=config_path.resolve(),
    )


def _require_str(table: dict, key: str) -> str:
    value = table.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ConfigError(f"missing or empty string: {key}")
    return value.strip()


def _require_float(table: dict, key: str) -> float:
    value = table.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ConfigError(f"missing or invalid number: {key}")
    return float(value)


def _parse_iso_date(value: str, key: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ConfigError(f"{key} must be YYYY-MM-DD") from exc


def _assert_loopback(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ConfigError("ollama_host must be an http(s) URL")
    host = (parsed.hostname or "").lower()
    if host not in LOOPBACK_HOSTS:
        raise ConfigError("ollama_host must be loopback (127.0.0.1, localhost, or ::1)")
