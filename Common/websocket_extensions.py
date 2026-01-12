from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING

from aiohttp.web import WebSocketResponse

if TYPE_CHECKING:
    from typing import Any

__all__ = ("CustomWSCloseCode", "CustomWSResponse")


# fmt: off
class CustomWSCloseCode(IntEnum):
    TokenExpired       = 4000
    InvalidFrameType   = 4001
    InvalidJSON        = 4002
    InvalidMessageType = 4003
# fmt: on


class CustomWSResponse(WebSocketResponse):
    def __init__(
        self,
        *args: Any,
        limit: int,
        interval: float,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.__limit = limit
        self.__interval = interval
        self.__hits = []
