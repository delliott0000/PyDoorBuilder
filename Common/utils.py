from __future__ import annotations

from datetime import datetime
from logging import DEBUG, ERROR, INFO, WARNING, basicConfig, getLogger
from os import makedirs
from pathlib import Path
from sys import exc_info
from typing import TYPE_CHECKING

from bcrypt import checkpw, gensalt, hashpw

if TYPE_CHECKING:
    from typing import Any

    from aiohttp import ClientResponse
    from aiohttp.web import Request

    Json = dict[str, Any]

__all__ = (
    "now",
    "decode_datetime",
    "encode_datetime",
    "check_password",
    "encrypt_password",
    "setup_logging",
    "log",
    "to_json",
)


_logger = getLogger()


def now() -> datetime:
    return datetime.now().astimezone()


def decode_datetime(t: str, /) -> datetime:
    return datetime.strptime(t, "%Y-%m-%dT%H:%M:%S.%f%z")


def encode_datetime(t: datetime, /) -> str:
    if t.tzinfo is None:
        raise ValueError("Datetime must be timezone-aware.")
    else:
        return t.strftime("%Y-%m-%dT%H:%M:%S.%f%z")


def check_password(password: str, hashed_password: str, /) -> bool:
    return checkpw(password.encode(), hashed_password.encode())


def encrypt_password(password: str, /) -> str:
    return hashpw(password.encode(), gensalt(rounds=10)).decode()


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


def log(message: str, level: int = INFO, /) -> None:
    with_traceback = exc_info()[0] is not None and level >= ERROR
    _logger.log(level, message, exc_info=with_traceback)


async def to_json(r: Request | ClientResponse, /, *, strict: bool = False) -> Json:
    try:
        data = await r.json()
        if not isinstance(data, dict):
            raise ValueError(f"Expected dict, got {type(data).__name__}.")
        return data
    except Exception as error:
        if strict:
            raise
        log(f"Failed to parse JSON payload - {type(error).__name__}.", WARNING)
        return {}
