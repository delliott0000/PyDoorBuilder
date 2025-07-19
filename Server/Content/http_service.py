from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .server import MainService

__all__ = ("HTTPService",)


class HTTPService:
    def __init__(self, core: MainService, /):
        self.core: MainService = core
