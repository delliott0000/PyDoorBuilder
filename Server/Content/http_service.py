from __future__ import annotations

from typing import TYPE_CHECKING

from .base_service import BaseService
from .decorators import BucketType, ratelimit, route, validate_access

if TYPE_CHECKING:
    from aiohttp.web import Request, Response

__all__ = ("AuthService",)


class AuthService(BaseService):
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
