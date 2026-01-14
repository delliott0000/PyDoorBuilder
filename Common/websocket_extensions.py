from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING

from aiohttp import WSCloseCode, WSMsgType
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
        *,
        limit: int,
        interval: float,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
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
            await self.__close_and_break__(code=WSCloseCode.POLICY_VIOLATION)

        if message.type != WSMsgType.TEXT:
            await self.__close_and_break__(code=CustomWSCloseCode.InvalidFrameType)

        return message

    async def __close_and_break__(self, **kwargs: Any) -> None:
        await self.close(**kwargs)
        raise StopAsyncIteration
