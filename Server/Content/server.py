from __future__ import annotations

from asyncio import Runner, gather
from contextlib import AsyncExitStack
from logging import getLogger
from typing import TYPE_CHECKING

from aiohttp.web import Application, AppRunner, TCPSite

from Common import global_config

from .http_service import HTTPService
from .middlewares import middlewares
from .postgre_client import ServerPostgreSQLClient
from .websocket_service import AutopilotWebSocketService, ClientWebSocketService

if TYPE_CHECKING:
    from Common import Session

    from .base_service import BaseService

__all__ = ("Server",)


_logger = getLogger()


task_config = global_config["server"]["tasks"]
api_config = global_config["server"]["api"]


class Server:
    def __init__(self):
        self.db: ServerPostgreSQLClient = ServerPostgreSQLClient()

        self.app: Application = Application(middlewares=middlewares)
        self.runner: AppRunner | None = None

        self.http = HTTPService(self, task_config["http_interval"])
        self.client_ws = ClientWebSocketService(self, task_config["client_ws_interval"])
        self.autopilot_ws = AutopilotWebSocketService(
            self, task_config["autopilot_ws_interval"]
        )

        self.token_to_session: dict[str, Session] = {}
        self.user_id_to_tokens: dict[str, set[str]] = {}
        self.session_id_to_session: dict[str, Session] = {}

    @property
    def services(self) -> tuple[BaseService, ...]:
        return self.http, self.client_ws, self.autopilot_ws

    def run(self) -> None:
        async def _service():
            _logger.info("Starting up service...")

            self.runner = AppRunner(self.app, access_log=None)
            await self.runner.setup()

            host = api_config["host"]
            port = api_config["port"]

            site = TCPSite(self.runner, host, port)
            await site.start()

            _logger.info("Service running.")

            services = self.services
            contexts = services + (self.db,)
            tasks = (service.task for service in services)

            async with AsyncExitStack() as stack:

                for context in contexts:
                    await stack.enter_async_context(context)

                await gather(*tasks)

        async def _cleanup():
            await self.runner.cleanup()

        with Runner() as runner:
            try:
                runner.run(_service())
            except (KeyboardInterrupt, SystemExit):
                _logger.info("Received signal to terminate program.")
            finally:
                _logger.info("Cleaning up...")
                runner.run(_cleanup())
                _logger.info("Done. Have a nice day!")
