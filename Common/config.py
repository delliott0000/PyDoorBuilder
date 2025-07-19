from __future__ import annotations

from tomllib import load
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._types import ConfigData


__all__ = ("global_config",)


config_file = Path(__file__).parent.parent / "config.toml"

with config_file.open("rb") as file:
    global_config: ConfigData = load(file)
