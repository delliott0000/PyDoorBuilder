from __future__ import annotations

from typing import TYPE_CHECKING

from .base_service import BaseService

if TYPE_CHECKING:
    ...

__all__ = ("HTTPService",)


class HTTPService(BaseService):
    async def task_coro(self) -> None:
        pass

    def register_routes(self) -> None:
        pass
