from __future__ import annotations

from enum import Enum
from time import time
from typing import TYPE_CHECKING

from aiohttp.web import HTTPTooManyRequests

from Common import log

if TYPE_CHECKING:
    from collections.abc import Callable, Coroutine
    from typing import Any

    from aiohttp.web import Request, Response

    from .base_service import BaseService

    RespCoro = Coroutine[Any, Any, Response]
    RespFunc = Callable[[BaseService, Request], RespCoro]
    RespDeco = Callable[[RespFunc], RespFunc]

__all__ = ("ensure_meta", "BucketType", "ratelimit", "route", "validate_access")


def ensure_meta(obj: Any, /) -> dict[str, Any]:
    if not hasattr(obj, "__meta__"):
        obj.__meta__ = {}
    return obj.__meta__


class BucketType(Enum):
    IP = 0
    User = 1
    Token = 2
    Route = 3

    def get_source(self, service: BaseService, request: Request, /) -> Any:
        if self == BucketType.IP:
            return request.remote or "anon"
        elif self == BucketType.User:
            return service.user_from_request(request) or "anon"
        elif self == BucketType.Token:
            return service.token_from_request(request) or "anon"
        elif self == BucketType.Route:
            return request.match_info.route.name or "global"
        else:
            raise NotImplementedError("Bucket type not implemented.")


def ratelimit(*, limit: int, interval: float, bucket_type: BucketType) -> RespDeco:
    k1, k2 = "ratelimits", bucket_type.name

    def decorator(func: RespFunc, /) -> RespFunc:

        async def wrapper(service: BaseService, request: Request, /) -> Response:
            source = bucket_type.get_source(service, request)

            now = time()
            meta = ensure_meta(wrapper)
            hits = meta[k1][k2].get(source, ())
            hits = [hit for hit in hits if hit + interval > now]

            if len(hits) >= limit:
                raise HTTPTooManyRequests(
                    reason="Too many requests", headers={"Retry-After": str(interval)}
                )

            hits.append(now)
            meta[k1][k2][source] = hits

            if len(hits) >= limit:
                method, endpoint = service.decode_route_name(request.match_info.route.name)
                log(
                    f"{method.upper()} {endpoint} " f"has hit the {bucket_type.name} ratelimit."
                )

            return await func(service, request)

        wrapper.__meta__ = ensure_meta(func)
        wrapper.__meta__.setdefault(k1, {})[k2] = {}

        return wrapper

    return decorator


def route(method: str, endpoint: str, /) -> RespDeco:

    def decorator(func: RespFunc, /) -> RespFunc:
        meta = ensure_meta(func)
        routes = meta.setdefault("routes", [])
        routes.append({"method": method, "endpoint": endpoint})

        return func

    return decorator


def validate_access(func: RespFunc, /) -> RespFunc:

    async def wrapper(service: BaseService, request: Request, /) -> Response:
        access = service.access_from_request(request)
        service.check_key(access)

        return await func(service, request)

    wrapper.__meta__ = ensure_meta(func)

    return wrapper
