from __future__ import annotations

from abc import ABC, abstractmethod
from asyncio import CancelledError, create_task, sleep
from inspect import getmembers
from inspect import ismethod as isfunc
from logging import getLogger
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from asyncio import Task
    from collections.abc import Callable
    from typing import ParamSpec, Self, TypeVar

    from .server import Server

    P = ParamSpec("P")
    T = TypeVar("T")
    F = Callable[P, T]

__all__ = (
    "route",
    "BaseService",
)


_logger = getLogger()


def route(method: str, endpoint: str, /) -> Callable[[F], F]:
    def decorator(f: F, /) -> F:
        setattr(f, "__route__", (method, endpoint))
        return f

    return decorator


class BaseService(ABC):
    def __init__(self, server: Server, interval: float, /):
        self.server: Server = server
        self.interval: float = interval
        self.register_routes()
        self.__task: Task | None = None

    async def __aenter__(self) -> Self:
        self.__task = create_task(self.task_coro_loop(), name=self.task_name)
        _logger.info(f"{self.task_name} started.")
        return self

    async def __aexit__(self, *_) -> None:
        if self.__task is None:
            return
        elif not self.__task.done():
            self.__task.cancel()

        try:
            await self.__task
        except CancelledError:
            _logger.info(f"{self.task_name} cancelled.")
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
    async def task_coro(self) -> None:
        pass

    async def task_coro_loop(self) -> None:
        while True:
            await sleep(self.interval)
            await self.task_coro()

    def register_routes(self) -> None:
        for func_name, func in getmembers(self, predicate=isfunc):

            route_info: tuple[str, str] | None = getattr(func, "__route__", None)
            if route_info is not None:

                method, endpoint = route_info
                self.server.app.router.add_route(method, endpoint, func)

                _logger.info(
                    f"Registered listener: [{method.upper()}] {endpoint} -> {type(self).__name__}.{func_name}()"
                )
