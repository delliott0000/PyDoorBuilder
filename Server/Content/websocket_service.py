from __future__ import annotations

from typing import TYPE_CHECKING

from .base_service import BaseService

if TYPE_CHECKING:
    ...

__all__ = ("ClientWebSocketService", "AutopilotWebSocketService")


class ClientWebSocketService(BaseService):
    async def task_coro(self) -> None:
        pass


class AutopilotWebSocketService(BaseService):
    async def task_coro(self) -> None:
        pass
