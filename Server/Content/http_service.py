from __future__ import annotations

from logging import getLogger
from secrets import token_urlsafe
from typing import TYPE_CHECKING

from aiohttp.web import HTTPBadRequest, HTTPUnauthorized, json_response

from Common import Session, Token, to_json

from .base_service import BaseService
from .decorators import BucketType, ratelimit, route, validate_access

if TYPE_CHECKING:
    from aiohttp.web import Request, Response

__all__ = ("AuthService",)


_logger = getLogger()


class AuthService(BaseService):
    def add_token_keys(self, token: Token, /) -> None:
        self.server.key_to_token[token.access] = token
        self.server.key_to_token[token.refresh] = token

    def pop_token_keys(self, token: Token, /) -> None:
        self.server.key_to_token.pop(token.access, None)
        self.server.key_to_token.pop(token.refresh, None)

    def ok_response(self, token: Token, /) -> Response:
        session = token.session
        user = session.user
        return json_response(
            {
                "message": "Ok",
                "token": token.to_json(),
                "session": session.to_json(),
                "user": user.to_json(),
            },
            status=200,
        )

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

        tokens = self.server.user_to_tokens.setdefault(user, set())
        if len(tokens) >= self.server.config.max_tokens_per_user:
            raise HTTPUnauthorized(reason="Too many unexpired tokens")

        try:
            session = self.server.session_id_to_session[data["session_id"]]
            if session.user != user:
                raise ValueError("Invalid session ID.")

        except (KeyError, ValueError):
            session = Session(token_urlsafe(16), user)
            self.server.session_id_to_session[session.id] = session
            _logger.info(f"Session issued for {user}. (Session ID: {session.id})")

        token = Token(
            session,
            access_expires=self.server.config.access_time,
            refresh_expires=self.server.config.refresh_time,
        )
        tokens.add(token)
        self.add_token_keys(token)
        _logger.info(f"Token issued for {user}. (Token ID: {token.id})")

        return self.ok_response(token)

    @route("post", "/auth/refresh")
    @ratelimit(limit=10, interval=60, bucket_type=BucketType.IP)
    @ratelimit(limit=10, interval=60, bucket_type=BucketType.Token)
    async def refresh(self, request: Request, /) -> Response:
        data = await to_json(request)

        refresh = data.get("refresh")
        self.check_key(refresh, for_refresh=True)

        token = self.server.key_to_token[refresh]
        self.pop_token_keys(token)
        token.renew(
            access_expires=self.server.config.access_time,
            refresh_expires=self.server.config.refresh_time,
        )
        self.add_token_keys(token)
        _logger.info(f"Token renewed for {token.session.user}. (Token ID: {token.id})")

        return self.ok_response(token)

    @route("post", "/auth/logout")
    @ratelimit(limit=10, interval=60, bucket_type=BucketType.IP)
    @ratelimit(limit=10, interval=60, bucket_type=BucketType.User)
    @validate_access
    async def logout(self, request: Request, /) -> Response:
        token = self.token_from_request(request)
        token.kill()
        _logger.info(f"Token killed for {token.session.user}. (Token ID: {token.id})")
        return self.ok_response(token)
