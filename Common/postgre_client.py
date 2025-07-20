from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Self

__all__ = ("PostgreSQLClient",)


class PostgreSQLClient:
    def __init__(self):
        pass

    async def __aenter__(self) -> Self:
        await self.connect()
        return self

    async def __aexit__(self, *_) -> None:
        await self.disconnect()

    async def connect(self) -> None: ...

    async def disconnect(self) -> None: ...
