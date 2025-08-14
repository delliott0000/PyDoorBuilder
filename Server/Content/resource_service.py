from __future__ import annotations

from typing import TYPE_CHECKING

from .base_service import BaseService
from .decorators import BucketType, ratelimit, route, user_only, validate_access

if TYPE_CHECKING:
    from aiohttp.web import Request, Response

    from Common import Resource

__all__ = ("ResourceService",)


class ResourceService(BaseService):
    async def load_resource(self, rtype: str, rid: str, /) -> Resource:
        pass

    async def task_coro(self) -> None:
        pass

    @route("post", "/resource/{rtype}/{rid}/acquire")
    @ratelimit(limit=10, interval=60, bucket_type=BucketType.User)
    @user_only
    @validate_access
    async def acquire(self, request: Request, /) -> Response:
        pass

    @route("post", "/resource/{rtype}/{rid}/release")
    @ratelimit(limit=10, interval=60, bucket_type=BucketType.User)
    @user_only
    @validate_access
    async def release(self, request: Request, /) -> Response:
        pass
