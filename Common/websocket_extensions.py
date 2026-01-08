from enum import IntEnum

__all__ = ("CustomWSCloseCode",)


# fmt: off
class CustomWSCloseCode(IntEnum):
    TokenExpired       = 4000
    InvalidFrameType   = 4001
    InvalidJSON        = 4002
    InvalidMessageType = 4003
# fmt: on
