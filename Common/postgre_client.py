from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Self

    from asyncpg import Pool

    from Common import PostgresConfig

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

    async def connect(self) -> None: ...

    async def disconnect(self) -> None: ...
