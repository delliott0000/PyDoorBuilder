from __future__ import annotations

from asyncio import gather, run
from contextlib import AsyncExitStack
from logging import getLogger
from typing import TYPE_CHECKING

from aiohttp import web

from Common import global_config

from .http_service import HTTPService
from .postgre_client import ServerPostgreSQLClient
from .websocket_service import WebSocketService

if TYPE_CHECKING:
    ...

__all__ = ("Server",)


_logger = getLogger()


task_config = global_config["server"]["tasks"]


class Server:
    def __init__(self):
        self.db = ServerPostgreSQLClient()

        self.app = web.Application()

        self.services = (
            HTTPService(self, task_config["http_interval"]),
            WebSocketService(self, task_config["ws_interval"]),
        )

    def run(self) -> None:
        async def _run_service():
            async with AsyncExitStack() as stack:

                for context in (*self.services, self.db):
                    await stack.enter_async_context(context)

                await gather(*(service.task for service in self.services))

        try:
            run(_run_service())
        except (KeyboardInterrupt, SystemExit):
            _logger.info("Received signal to terminate program.")
        finally:
            _logger.info("Done. Have a nice day!")
