from __future__ import annotations

from abc import ABC, abstractmethod
from asyncio import CancelledError, create_task, sleep
from inspect import getmembers, isfunction
from logging import getLogger
from typing import TYPE_CHECKING

from aiohttp.web import HTTPBadRequest, HTTPUnauthorized

from .decorators import ensure_meta

if TYPE_CHECKING:
    from asyncio import Task
    from typing import Self

    from aiohttp.web import Request

    from Common import Session, Token, User

    from .server import Server

__all__ = ("BaseService",)


_logger = getLogger()


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

    def key_is_valid(self, key: str, /, *, for_refresh: bool = False) -> bool:
        try:
            token = self.server.key_to_token[key]
        except KeyError:
            return False

        if for_refresh:
            return not token.expired
        else:
            return token.active

    def check_key(self, key: str | None, /, *, for_refresh: bool = False) -> None:
        _type = "refresh" if for_refresh else "access"
        if key is None:
            raise HTTPBadRequest(reason=f"Missing {_type} token")
        elif not self.key_is_valid(key, for_refresh=for_refresh):
            raise HTTPUnauthorized(reason=f"Invalid {_type} token")

    def access_from_request(self, request: Request, /) -> str | None:
        try:
            return request["access"]
        except KeyError:
            authorization = request.headers.get("Authorization")

            if isinstance(authorization, str) and authorization.startswith("Bearer "):
                access = authorization.removeprefix("Bearer ")
                request["access"] = access
                return access

            else:
                return None

    def token_from_request(self, request: Request, /) -> Token | None:
        try:
            return self.server.key_to_token[self.access_from_request(request)]
        except KeyError:
            return None

    def session_from_request(self, request: Request, /) -> Session | None:
        try:
            return self.token_from_request(request).session
        except AttributeError:
            return None

    def user_from_request(self, request: Request, /) -> User | None:
        try:
            return self.session_from_request(request).user
        except AttributeError:
            return None

    def encode_route_name(self, method: str, endpoint: str, /) -> str:
        return f"{method}.{endpoint[1:]}".replace("/", "-")

    def decode_route_name(self, name: str, /) -> tuple[str, str]:
        method, endpoint = name.split(".", 1)
        return method, "/" + endpoint.replace("-", "/")

    def register_routes(self) -> None:
        for func_name, func in getmembers(type(self), predicate=isfunction):

            routes = ensure_meta(func).get("routes", ())
            for route in routes:
                try:
                    method = route["method"]
                    endpoint = route["endpoint"]
                except KeyError:
                    continue

                self.server.app.router.add_route(
                    method,
                    endpoint,
                    func.__get__(self),
                    name=self.encode_route_name(method, endpoint),
                )
                _logger.info(
                    f"Registered listener: {method.upper()} {endpoint} -> {type(self).__name__}.{func_name}()"
                )
