from __future__ import annotations

from pathlib import Path
from tomllib import load
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

__all__ = ("global_config",)


config_file = Path(__file__).parent.parent / "config.toml"

with config_file.open("rb") as file:
    global_config: dict[str, Any] = load(file)
