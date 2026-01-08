from enum import IntEnum

from aiohttp.web import WebSocketResponse

__all__ = ("CustomWSCloseCode", "CustomWSResponse")


# fmt: off
class CustomWSCloseCode(IntEnum):
    TokenExpired       = 4000
    InvalidFrameType   = 4001
    InvalidJSON        = 4002
    InvalidMessageType = 4003
# fmt: on


class CustomWSResponse(WebSocketResponse): ...
