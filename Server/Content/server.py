from __future__ import annotations

from typing import TYPE_CHECKING

from aiohttp import web

from .http_service import HTTPService
from .postgre_client_server import ServerPostgreSQLClient
from .websocket_service import WebSocketService

if TYPE_CHECKING:
    ...

__all__ = ("MainService",)


class MainService:
    def __init__(self):
        self.app = web.Application()

        self.http = HTTPService(self)
        self.ws = WebSocketService(self)
        self.db = ServerPostgreSQLClient()

    def start(self) -> None:
        pass
