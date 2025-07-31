from __future__ import annotations

from typing import TYPE_CHECKING

from Common import Token

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

    async def task_coro(self) -> None: ...

    @route("post", "/auth/login")
    @ratelimit(limit=10, interval=60, bucket_type=BucketType.IP)
    @ratelimit(limit=100, interval=60, bucket_type=BucketType.Route)
    async def login(self, request: Request, /) -> Response: ...

    @route("post", "/auth/refresh")
    @ratelimit(limit=10, interval=60, bucket_type=BucketType.IP)
    @ratelimit(limit=10, interval=60, bucket_type=BucketType.Token)
    async def renew(self, request: Request, /) -> Response: ...

    @route("post", "/auth/logout")
    @ratelimit(limit=10, interval=60, bucket_type=BucketType.IP)
    @ratelimit(limit=10, interval=60, bucket_type=BucketType.User)
    @validate_access
    async def logout(self, request: Request, /) -> Response: ...
