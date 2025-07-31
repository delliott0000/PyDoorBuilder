from __future__ import annotations

from asyncio import Runner, gather
from contextlib import AsyncExitStack
from logging import getLogger
from typing import TYPE_CHECKING

from aiohttp.web import Application, AppRunner, TCPSite

from Common import ServerAPIConfig

from .http_service import AuthService
from .middlewares import middlewares
from .postgre_client import ServerPostgreSQLClient
from .websocket_service import AutopilotWebSocketService, ClientWebSocketService

if TYPE_CHECKING:
    from typing import Any

    from Common import Session, Token, User

    from .base_service import BaseService

__all__ = ("Server",)


_logger = getLogger()


class Server:
    def __init__(self, *, config: dict[str, Any]):
        self.__config = ServerAPIConfig(**config)

        self.db = ServerPostgreSQLClient()

        self.app = Application(middlewares=middlewares)
        self.runner: AppRunner | None = None

        self.auth = AuthService(self)
        self.client_ws = ClientWebSocketService(self)
        self.autopilot_ws = AutopilotWebSocketService(self)

        self.key_to_token: dict[str, Token] = {}
        self.user_to_tokens: dict[User, set[Token]] = {}
        self.session_id_to_session: dict[str, Session] = {}

    @property
    def config(self) -> ServerAPIConfig:
        return self.__config

    @property
    def services(self) -> tuple[BaseService, ...]:
        return self.auth, self.client_ws, self.autopilot_ws

    def run(self) -> None:
        async def _service():
            _logger.info("Starting up service...")

            self.runner = AppRunner(self.app, access_log=None)
            await self.runner.setup()

            site = TCPSite(self.runner, self.__config.host, self.__config.port)
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
