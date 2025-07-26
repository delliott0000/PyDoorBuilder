from __future__ import annotations

from datetime import datetime
from logging import DEBUG, basicConfig, getLogger
from os import makedirs
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

    from aiohttp import ClientResponse
    from aiohttp.web import Request

    Json = dict[str, Any]

__all__ = ("now", "setup_logging", "to_json")


_logger = getLogger()


def now() -> datetime:
    return datetime.now().astimezone()


def setup_logging(file: str, level: int = DEBUG, /) -> None:
    current_module = Path(file).parent
    log_destination = current_module.parent / "Logs" / current_module.name

    timestamp = now().strftime("%Y-%m-%d_%H-%M-%S")

    makedirs(log_destination, exist_ok=True)

    basicConfig(
        filename=log_destination / f"{timestamp}.txt",
        filemode="w",
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


async def to_json(r: Request | ClientResponse, /, *, strict: bool = False) -> Json:
    try:
        data = await r.json()
        if not isinstance(data, dict):
            raise ValueError(f"Expected dict, got {type(data).__name__}.")
        return data
    except Exception as error:
        if strict:
            raise
        _logger.exception(f"Failed to parse JSON payload: {error}.")
        return {}
