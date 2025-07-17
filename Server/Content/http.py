from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .core import CoreService


__all__ = ("HTTPService",)


class HTTPService:
    def __init__(self, core: CoreService, /):
        self.core: CoreService = core
