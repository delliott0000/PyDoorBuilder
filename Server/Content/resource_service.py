from __future__ import annotations

from asyncio import gather
from typing import TYPE_CHECKING

from aiohttp.web import HTTPNotFound, json_response

from .base_service import BaseService
from .decorators import BucketType, ratelimit, route, user_only, validate_access
from .resource_types import QuoteResource

if TYPE_CHECKING:
    from typing import Any

    from aiohttp.web import Request, Response

    from Common import Resource

__all__ = ("ResourceService",)


class ResourceService(BaseService):
    @property
    def map(self) -> dict[str, Any]:
        # Confirm the structure for later
        return {
            "quote": {
                "class": QuoteResource,
                "executors": {
                    "...": {
                        "func": ...,
                        "query": ...,
                        "check": ...,
                        "exception": ...,
                    }
                },
            }
        }

    def ok_response(self, resource: Resource, /) -> Response:
        return json_response(
            {
                "message": "Ok",
                "resource": resource.to_json(),
            },
            status=200,
        )

    async def run_executor(
        self, rid: str, key: str, executor: dict[str, Any], /
    ) -> tuple[str, Any]:
        func = executor["func"]
        query = executor["query"]
        check = executor["check"]
        exception = executor["exception"]

        args = query, rid
        result = await func(*args)

        if not check(result):
            raise exception

        return key, result

    async def load_resource(self, request: Request, /) -> Resource:
        rtype = request.match_info["rtype"]
        rid = request.match_info["rid"]
        cache_key = rtype, rid

        cached = self.server.rtype_rid_to_resource.get(cache_key)
        if cached is not None:
            return cached

        try:
            loader = self.map[rtype]
        except KeyError:
            raise HTTPNotFound(reason="Unknown resource type")

        class_ = loader["class"]
        executors = loader["executors"]

        tasks = (self.run_executor(rid, key, executor) for key, executor in executors.items())
        results = await gather(*tasks)
        data = {key: result for key, result in results}

        resource = class_.new(data)
        self.server.rtype_rid_to_resource[cache_key] = resource
        return resource

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
