from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from .base_service import BaseService

if TYPE_CHECKING:
    ...

__all__ = ("BaseWebSocketService", "UserWebSocketService", "AutopilotWebSocketService")


class BaseWebSocketService(BaseService, ABC):
    pass


class UserWebSocketService(BaseWebSocketService):
    async def task_coro(self) -> None:
        pass


class AutopilotWebSocketService(BaseWebSocketService):
    async def task_coro(self) -> None:
        pass
