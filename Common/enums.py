from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    ...


__all__ = ("DoorType",)


class DoorType(Enum):
    Single = 0
    Double = 1
