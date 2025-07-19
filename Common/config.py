from tomllib import load
from pathlib import Path


__all__ = ("config",)


config_file = Path(__file__).parent.parent / "config.toml"

with config_file.open("rb") as file:
    config = load(file)
