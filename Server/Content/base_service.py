from __future__ import annotations

from abc import ABC, abstractmethod
from asyncio import CancelledError, create_task
from logging import getLogger
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from asyncio import Task
    from typing import Self

    from .server import Server

__all__ = ("BaseService",)


_logger = getLogger()


class BaseService(ABC):
    def __init__(self, server: Server, /):
        self.server: Server = server
        self.register_routes()
        self.__task: Task | None = None

    async def __aenter__(self) -> Self:
        self.__task = create_task(self.task_coro_loop(), name=self.task_name)
        _logger.debug(f"{self.task_name} started.")
        return self

    async def __aexit__(self, *_) -> None:
        if self.__task is None:
            return
        elif not self.__task.done():
            self.__task.cancel()

        try:
            await self.__task
        except CancelledError:
            _logger.debug(f"{self.task_name} cancelled.")
        except Exception as error:
            _logger.exception(f"{self.task_name} raised {type(error).__name__}.")

        self.__task = None

    @property
    def task(self) -> Task | None:
        return self.__task

    @property
    def task_name(self) -> str:
        return f"{type(self).__name__}Task"

    @abstractmethod
    def register_routes(self) -> None:
        pass

    @abstractmethod
    async def task_coro(self) -> None:
        pass

    async def task_coro_loop(self) -> None:
        while True:
            await self.task_coro()
