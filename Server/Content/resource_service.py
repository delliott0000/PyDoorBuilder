from __future__ import annotations

from typing import TYPE_CHECKING

from aiohttp.web import HTTPNotFound

from .base_service import BaseService
from .decorators import BucketType, ratelimit, route, user_only, validate_access

if TYPE_CHECKING:
    from typing import Any

    from aiohttp.web import Request, Response

    from Common import Resource

__all__ = ("ResourceService",)


class ResourceService(BaseService):
    @property
    def map(self) -> dict[str, Any]:
        return {}

    async def load_resource(self, request: Request, /) -> Resource:
        rtype = request.match_info["rtype"]
        rid = request.match_info["rid"]
        cache_key = rtype, rid

        cached = self.server.rtype_rid_to_resource.get(cache_key)
        if cached is not None:
            return cached

        try:
            ...
        except KeyError:
            raise HTTPNotFound(reason="Unknown resource type")

        ...

    async def task_coro(self) -> None:
        pass

    @route("post", "/resource/{rtype}/{rid}/acquire")
    @ratelimit(limit=10, interval=60, bucket_type=BucketType.User)
    @user_only
    @validate_access
    async def acquire(self, request: Request, /) -> Response:
        pass

    @route("post", "/resource/release")
    @ratelimit(limit=10, interval=60, bucket_type=BucketType.User)
    @user_only
    @validate_access
    async def release(self, request: Request, /) -> Response:
        pass
