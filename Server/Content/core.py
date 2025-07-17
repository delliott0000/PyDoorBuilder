from __future__ import annotations

from typing import TYPE_CHECKING

from .http import HTTPService
from .postgre_sv import ServerPostgreSQLClient
from .websocket import WebSocketService

if TYPE_CHECKING:
    ...


__all__ = ("CoreService",)


class CoreService:
    def __init__(self):
        self.http = HTTPService(self)
        self.ws = WebSocketService(self)
        self.db = ServerPostgreSQLClient()

    def run(self) -> None:
        ...
