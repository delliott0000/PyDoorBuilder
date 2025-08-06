from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from tomllib import load
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

__all__ = (
    "ClientAPIConfig",
    "PostgresConfig",
    "ServerAPIConfig",
    "global_config",
)


@dataclass(kw_only=True, frozen=True)
class ClientAPIConfig:
    domain: str
    secure: bool
    local: bool
    host: str
    port: int


@dataclass(kw_only=True, frozen=True)
class PostgresConfig:
    host: str
    port: int
    database: str
    user: str
    password: str
    min_pool_size: int
    max_pool_size: int


@dataclass(kw_only=True, frozen=True)
class ServerAPIConfig:
    host: str
    port: int
    access_time: float
    refresh_time: float
    max_tokens_per_user: int
    task_interval: float
    ws_heartbeat: float


config_file = Path(__file__).parent.parent / "config.toml"

with config_file.open("rb") as file:
    global_config: dict[str, Any] = load(file)
