from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .server import MainService

__all__ = ("WebSocketService",)


class WebSocketService:
    def __init__(self, core: MainService, /):
        self.core: MainService = core

    async def start(self) -> None:
        pass
