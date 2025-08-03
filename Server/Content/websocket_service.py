from __future__ import annotations

from abc import ABC
from logging import ERROR
from typing import TYPE_CHECKING

from aiohttp.web import HTTPConflict, WebSocketResponse

from Common import log

from .base_service import BaseService
from .decorators import (
    BucketType,
    autopilot_only,
    ratelimit,
    route,
    user_only,
    validate_access,
)

if TYPE_CHECKING:
    from aiohttp.web import Request

    from Common import Token

__all__ = ("BaseWebSocketService", "UserWebSocketService", "AutopilotWebSocketService")


class BaseWebSocketService(BaseService, ABC):
    async def prepare_ws(self, request: Request, token: Token, /) -> WebSocketResponse:
        if token in token.session.connections:
            raise HTTPConflict(reason="Already connected")

        response = WebSocketResponse(heartbeat=self.server.config.ws_heartbeat)
        token.session.connections[token] = response

        await response.prepare(request)
        log(f"Opened WebSocket. (Token ID: {token.id})")

        return response

    async def cleanup_ws(self, token: Token, /) -> None:
        response = token.session.connections.pop(token, None)

        try:
            await response.close()
            log(f"Closed WebSocket. (Token ID: {token.id})")
        except AttributeError:
            pass
        except Exception as error:
            log(f"Failed to close WebSocket - {type(error).__name__}.", ERROR)


class UserWebSocketService(BaseWebSocketService):
    async def task_coro(self) -> None:
        pass

    @route("get", "/ws/user")
    @ratelimit(limit=10, interval=60, bucket_type=BucketType.Token)
    @user_only
    @validate_access
    async def serve_ws(self, request: Request, /) -> WebSocketResponse:
        token = self.token_from_request(request)
        response = await self.prepare_ws(request, token)

        try:
            ...
        finally:
            await self.cleanup_ws(token)

        return response


class AutopilotWebSocketService(BaseWebSocketService):
    async def task_coro(self) -> None:
        pass

    @route("get", "/ws/autopilot")
    @ratelimit(limit=10, interval=60, bucket_type=BucketType.Token)
    @autopilot_only
    @validate_access
    async def serve_ws(self, request: Request, /) -> WebSocketResponse:
        token = self.token_from_request(request)
        response = await self.prepare_ws(request, token)

        try:
            ...
        finally:
            await self.cleanup_ws(token)

        return response
