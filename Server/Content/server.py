from __future__ import annotations

from asyncio import Runner
from logging import getLogger
from typing import TYPE_CHECKING

from aiohttp.web import Application

from .http_service import HTTPService
from .postgre_client_server import ServerPostgreSQLClient
from .websocket_service import WebSocketService

if TYPE_CHECKING:
    ...

__all__ = ("MainService",)


_logger = getLogger()


class MainService:
    def __init__(self):
        self.app = Application()

        self.http = HTTPService(self)
        self.ws = WebSocketService(self)
        self.db = ServerPostgreSQLClient()

    def run(self) -> None:
        async def _services():
            ...

        async def _cleanup():
            ...

        with Runner() as runner:
            try:
                runner.run(_services())
            except (KeyboardInterrupt, SystemExit):
                _logger.info("Received signal to terminate service.")
            finally:
                _logger.info("Cleaning up tasks and connections...")
                runner.run(_cleanup())
                _logger.info("Done. Have a nice day!")
