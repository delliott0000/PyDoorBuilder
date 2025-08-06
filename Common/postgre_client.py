from __future__ import annotations

from logging import ERROR
from typing import TYPE_CHECKING

from asyncpg import create_pool

from .utils import log

if TYPE_CHECKING:
    from collections.abc import Callable, Coroutine
    from typing import Any, Self, TypeVar

    from asyncpg import Connection, Pool, Record

    from .config import PostgresConfig

    T = TypeVar("T")

__all__ = ("PostgreSQLClient",)


class PostgreSQLClient:
    def __init__(self, *, config: PostgresConfig):
        self.config = config
        self.__pool: Pool | None = None

    async def __aenter__(self) -> Self:
        await self.connect()
        return self

    async def __aexit__(self, *_) -> None:
        await self.disconnect()

    @property
    def is_open(self) -> bool:
        return self.__pool is not None and not self.__pool.is_closing()

    async def connect(self) -> None:
        if self.is_open:
            return

        config = self.config

        try:
            self.__pool = await create_pool(
                host=config.host,
                port=config.port,
                database=config.database,
                user=config.user,
                password=config.password,
                min_size=config.min_pool_size,
                max_size=config.max_pool_size,
            )
            log(f"Connected to {config.database} as {config.user}.")
        except Exception as error:
            log(f"Failed to connect to {config.database} - {type(error).__name__}.", ERROR)
            raise

    async def disconnect(self) -> None:
        if not self.is_open:
            return

        config = self.config

        try:
            await self.__pool.close()
            log(f"Disconnected from {config.database}.")
        except Exception as error:
            log(f"Failed to disconnect from {config.database} - {type(error).__name__}.", ERROR)

        self.__pool = None

    async def make_call(self, func: Callable[[Connection], Coroutine[Any, Any, T]], /) -> T:
        if not self.is_open:
            raise RuntimeError("Postgres connection pool is closed.")

        async with self.__pool.acquire() as connection:
            return await func(connection)

    async def fetch_one(self, query: str, *args: Any) -> Record | None:
        return await self.make_call(lambda connection: connection.fetchrow(query, *args))

    async def fetch_all(self, query: str, *args: Any) -> list[Record]:
        return await self.make_call(lambda connection: connection.fetch(query, *args))

    async def execute(self, query: str, *args: Any) -> str:
        return await self.make_call(lambda connection: connection.execute(query, *args))
