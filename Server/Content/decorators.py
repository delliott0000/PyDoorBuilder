from __future__ import annotations

from enum import Enum
from time import time
from typing import TYPE_CHECKING

from aiohttp.web import HTTPBadRequest, HTTPTooManyRequests, HTTPUnauthorized

if TYPE_CHECKING:
    from collections.abc import Callable, Coroutine
    from typing import Any

    from aiohttp.web import Request, Response

    from .base_service import BaseService

    RespCoro = Coroutine[Any, Any, Response]
    RespFunc = Callable[[BaseService, Request], RespCoro]
    RespDeco = Callable[[RespFunc], RespFunc]

__all__ = ("_ensure_meta", "BucketType", "ratelimit", "route", "validate_token")


def _ensure_meta(obj: Any, /) -> dict[str, Any]:
    if not hasattr(obj, "__meta__"):
        obj.__meta__ = {}
    return obj.__meta__


class BucketType(Enum):
    IP = 0
    User = 1
    Token = 2
    Route = 3

    def get_source(self, service: BaseService, request: Request, /) -> str:
        if self == BucketType.IP:
            return request.remote or "anon"
        elif self == BucketType.User:
            return service.user_id_from_request(request) or "anon"
        elif self == BucketType.Token:
            return service.token_from_request(request) or "anon"
        elif self == BucketType.Route:
            return request.match_info.route.name or "global"
        else:
            raise NotImplementedError("Bucket type not implemented.")


def ratelimit(
    *, limit: int, interval: float, bucket_type: BucketType = BucketType.Token
) -> RespDeco:
    k1, k2 = "ratelimits", bucket_type.name

    def decorator(func: RespFunc, /) -> RespFunc:

        async def wrapper(service: BaseService, request: Request, /) -> Response:
            source = bucket_type.get_source(service, request)

            now = time()
            meta = _ensure_meta(wrapper)
            hits = meta[k1][k2].get(source, ())
            hits = [hit for hit in hits if hit + interval > now]

            if len(hits) >= limit:
                return HTTPTooManyRequests(headers={"Retry-After": str(interval)})

            hits.append(now)
            meta[k1][k2][source] = hits

            return await func(service, request)

        wrapper.__meta__ = _ensure_meta(func)
        wrapper.__meta__.setdefault(k1, {})[k2] = {}

        return wrapper

    return decorator


def route(method: str, endpoint: str, /) -> RespDeco:

    def decorator(func: RespFunc, /) -> RespFunc:
        meta = _ensure_meta(func)
        routes = meta.setdefault("routes", [])
        routes.append({"method": method, "endpoint": endpoint})

        return func

    return decorator


def validate_token(func: RespFunc, /) -> RespFunc:

    async def wrapper(service: BaseService, request: Request, /) -> Response:
        token = service.token_from_request(request)
        if token is None:
            return HTTPBadRequest()
        elif not service.token_exists(token):
            return HTTPUnauthorized()

        return await func(service, request)

    wrapper.__meta__ = _ensure_meta(func)

    return wrapper
