from __future__ import annotations

from typing import TYPE_CHECKING

from aiohttp import ClientSession

if TYPE_CHECKING:
    ...


__all__ = ("HTTPClient",)


class HTTPClient:
    def __init__(self):
        self.__session: ClientSession | None = None

    @property
    def is_open(self) -> bool:
        return self.__session is not None and not self.__session.closed

    async def create_connection(self) -> None:
        self.__session = ClientSession()

    async def close_connection(self) -> None:
        if self.is_open is True:
            await self.__session.close()
