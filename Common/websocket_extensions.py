from __future__ import annotations

from enum import IntEnum, StrEnum
from json import JSONDecodeError
from typing import TYPE_CHECKING

from aiohttp import ClientWebSocketResponse, WSCloseCode, WSMsgType
from aiohttp.web import WebSocketResponse

from .utils import check_ratelimit

if TYPE_CHECKING:
    from typing import Any

    from aiohttp import WSMessage

__all__ = (
    "CustomWSCloseCode",
    "CustomWSMessageType",
    "WSResponseMixin",
    "CustomWSResponse",
    "CustomClientWSResponse",
)


# fmt: off
class CustomWSCloseCode(IntEnum):
    TokenExpired       = 4000
    InvalidFrameType   = 4001
    InvalidJSON        = 4002
    InvalidMessageType = 4003


class CustomWSMessageType(StrEnum):
    Event = "event"
    Ack   = "ack"
# fmt: on


class WSResponseMixin:
    def __init__(
        self,
        *,
        ratelimited: bool = False,
        limit: int | None = None,
        interval: float | None = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)

        if ratelimited and (limit is None or interval is None):
            raise TypeError("Limit and interval must both be specified.")

        self.__ratelimited = ratelimited
        self.__limit = limit
        self.__interval = interval
        self.__hits = []

    async def __anext__(self) -> WSMessage:
        message = await super().__anext__()  # noqa

        if self.__ratelimited:
            try:
                self.__hits = check_ratelimit(
                    self.__hits, limit=self.__limit, interval=self.__interval
                )
            except RuntimeError:
                await self.__close_and_break__(code=WSCloseCode.POLICY_VIOLATION)

        if message.type != WSMsgType.TEXT:
            await self.__close_and_break__(code=CustomWSCloseCode.InvalidFrameType)

        try:
            message.json()
        except JSONDecodeError:
            await self.__close_and_break__(code=CustomWSCloseCode.InvalidJSON)

        # TODO: build a custom message object from the JSON object
        # TODO: and process/return that instead of the aiohttp object

        return message

    async def __close_and_break__(self, **kwargs: Any) -> None:
        await self.close(**kwargs)  # noqa
        raise StopAsyncIteration


class CustomWSResponse(WSResponseMixin, WebSocketResponse):
    pass


class CustomClientWSResponse(WSResponseMixin, ClientWebSocketResponse):
    pass
