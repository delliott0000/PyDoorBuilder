from enum import IntEnum

from aiohttp import WSCloseCode

__all__ = ("WSCloseCode", "CustomWSCloseCode")


# fmt: off
class CustomWSCloseCode(IntEnum):
    TokenExpired       = 4000
    InvalidFrameType   = 4001
    InvalidJSON        = 4002
    InvalidMessageType = 4003
