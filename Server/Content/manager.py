from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiohttp.web import WebSocketResponse

    from Common import Token

__all__ = ("AutopilotConnection", "AutopilotManager")


class AutopilotConnection:
    __slots__ = ("__token", "__task_id")

    def __init__(self, token: Token, /):
        self.__token = token
        self.__task_id: int | None = None

    def __str__(self):
        return f"Autopilot {self.__token.session.user} (Token ID: {self.__token.id})"

    @property
    def ws(self) -> WebSocketResponse:
        ws = self.__token.session.connections.get(self.__token)
        if ws is None or ws.closed:
            raise RuntimeError(f"{self} is not connected.")
        else:
            return ws

    @property
    def busy(self) -> bool:
        return self.__task_id is not None

    @property
    def task_id(self) -> int | None:
        return self.__task_id

    def set_task(self, task_id: int, /) -> None:
        if self.busy:
            raise RuntimeError(f"{self} is busy.")
        else:
            self.__task_id = task_id

    def clear_task(self) -> None:
        self.__task_id = None


class AutopilotManager:
    def __init__(self):
        self.__task_queue: list[int] = []
        self.__autopilots: dict[Token, AutopilotConnection] = {}

    async def autopilot_connect(self, token: Token, /) -> None: ...

    async def autopilot_disconnect(self, token: Token, /) -> None: ...

    async def wait_for_autopilot(self) -> AutopilotConnection: ...
