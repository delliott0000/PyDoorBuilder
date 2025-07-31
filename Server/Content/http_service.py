from __future__ import annotations

from typing import TYPE_CHECKING

from aiohttp.web import HTTPBadRequest, HTTPUnauthorized

from Common import Token, to_json

from .base_service import BaseService
from .decorators import BucketType, ratelimit, route, validate_access

if TYPE_CHECKING:
    from aiohttp.web import Request, Response

__all__ = ("AuthService",)


class AuthService(BaseService):
    def add_token_keys(self, token: Token, /) -> None:
        self.server.key_to_token[token.access] = token
        self.server.key_to_token[token.refresh] = token

    def pop_token_keys(self, token: Token, /) -> None:
        self.server.key_to_token.pop(token.access, None)
        self.server.key_to_token.pop(token.refresh, None)

    def ok_response(self, token: Token, /) -> Response: ...

    async def task_coro(self) -> None: ...

    @route("post", "/auth/login")
    @ratelimit(limit=10, interval=60, bucket_type=BucketType.IP)
    @ratelimit(limit=100, interval=60, bucket_type=BucketType.Route)
    async def login(self, request: Request, /) -> Response:
        data = await to_json(request)

        try:
            username = data["username"]
            password = data["password"]

            user = await self.server.db.get_user(username=username, password=password)

        except (KeyError, ValueError):
            raise HTTPBadRequest(reason="Missing username/password")

        if user is None:
            raise HTTPUnauthorized(reason="Incorrect username/password")

        ...

        return self.ok_response(...)

    @route("post", "/auth/refresh")
    @ratelimit(limit=10, interval=60, bucket_type=BucketType.IP)
    @ratelimit(limit=10, interval=60, bucket_type=BucketType.Token)
    async def refresh(self, request: Request, /) -> Response:
        data = await to_json(request)

        refresh = data.get("refresh")
        self.check_key(refresh, for_refresh=True)

        ...

        return self.ok_response(...)

    @route("post", "/auth/logout")
    @ratelimit(limit=10, interval=60, bucket_type=BucketType.IP)
    @ratelimit(limit=10, interval=60, bucket_type=BucketType.User)
    @validate_access
    async def logout(self, request: Request, /) -> Response: ...
