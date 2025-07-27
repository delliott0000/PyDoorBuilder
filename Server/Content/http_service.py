from __future__ import annotations

from secrets import token_urlsafe
from typing import TYPE_CHECKING

from aiohttp.web import HTTPBadRequest, HTTPForbidden, HTTPUnauthorized, json_response

from Common import Session, global_config, to_json

from .base_service import BaseService
from .decorators import BucketType, ratelimit, route, validate_token

if TYPE_CHECKING:
    from aiohttp.web import Request, Response

__all__ = ("HTTPService",)


config = global_config["server"]["api"]
duration = config["token_duration"]
max_tokens = config["max_tokens_per_user"]


class HTTPService(BaseService):
    async def task_coro(self) -> None:
        pass

    @route("post", "/auth/login")
    @ratelimit(limit=10, interval=60, bucket_type=BucketType.IP)
    @ratelimit(limit=100, interval=60, bucket_type=BucketType.Route)
    async def login(self, request: Request, /) -> Response:
        data = await to_json(request)

        try:
            username = data["username"]
            password = data["password"]
        except KeyError:
            raise HTTPBadRequest(reason="Missing username/password")

        user = self.server.db.get_user(username=username, password=password)
        if user is None:
            raise HTTPUnauthorized(reason="Incorrect username/password")

        tokens = self.server.user_id_to_tokens.setdefault(user.id, set())
        if len(tokens) >= max_tokens:
            raise HTTPForbidden(reason="Too many active tokens")

        token = token_urlsafe(32)
        tokens.add(token)

        session_id = token_urlsafe(16)
        session = Session(session_id, user, token, duration)
        self.server.token_to_session[token] = session

        return json_response(
            {
                "message": "Ok",
                "token": token,
                "duration": duration,
                "user_id": user.id,
                "username": username,
            },
            status=200,
        )

    @route("post", "/auth/renew")
    @ratelimit(limit=10, interval=60, bucket_type=BucketType.Token)
    @validate_token
    async def renew(self, request: Request, /) -> Response:
        session = self.session_from_request(request)
        session.renew(duration)
        return json_response(
            {
                "message": "Ok",
                "token": session.token,
                "duration": duration,
                "user_id": session.user.id,
                "username": session.user.name,
            },
            status=200,
        )

    @route("post", "/auth/logout")
    @ratelimit(limit=1, interval=60, bucket_type=BucketType.Token)
    @ratelimit(limit=10, interval=60, bucket_type=BucketType.User)
    @validate_token
    async def logout(self, request: Request, /) -> Response:
        session = self.session_from_request(request)
        session.kill()
        return json_response({"message": "Ok"}, status=200)
