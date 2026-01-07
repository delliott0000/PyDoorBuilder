from enum import IntEnum

from aiohttp import WSCloseCode

__all__ = ("WSCloseCode", "CustomWSCloseCode")


# fmt: off
class CustomWSCloseCode(IntEnum):
    TokenExpired       = 4000
    InvalidMessageType = 4001
    InvalidJSON        = 4002
