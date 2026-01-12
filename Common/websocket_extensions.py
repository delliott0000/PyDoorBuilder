from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING

from aiohttp import WSCloseCode
from aiohttp.web import WebSocketResponse

from .utils import check_ratelimit

if TYPE_CHECKING:
    from typing import Any

    from aiohttp import WSMessage

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

    async def __anext__(self) -> WSMessage:
        message = await super().__anext__()

        try:
            self.__hits = check_ratelimit(
                self.__hits, limit=self.__limit, interval=self.__interval
            )
        except RuntimeError:
            await self.close(code=WSCloseCode.POLICY_VIOLATION)
            raise StopAsyncIteration

        return message
