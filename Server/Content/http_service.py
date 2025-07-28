from __future__ import annotations

from collections import defaultdict
from logging import getLogger
from secrets import token_urlsafe
from typing import TYPE_CHECKING

from aiohttp.web import HTTPBadRequest, HTTPForbidden, HTTPUnauthorized, json_response

from Common import Session, global_config, to_json

from .base_service import BaseService
from .decorators import BucketType, ratelimit, route, validate_token

if TYPE_CHECKING:
    from aiohttp.web import Request, Response

__all__ = ("HTTPService",)


_logger = getLogger()


config = global_config["server"]["api"]
duration = config["token_duration"]
max_tokens = config["max_tokens_per_user"]


class HTTPService(BaseService):
    async def task_coro(self) -> None:
        dead_sessions = defaultdict(int)

        for token in list(self.server.token_to_session):
            session = self.server.token_to_session[token]

            if not session.active:
                self.server.token_to_session.pop(token, None)
                self.server.session_id_to_session.pop(session.id, None)

                tokens = self.server.user_id_to_tokens.get(session.user.id)
                if tokens is None:
                    continue

                tokens.discard(token)
                if not tokens:
                    self.server.user_id_to_tokens.pop(session.user.id, None)

                dead_sessions[session] += 1

        for session, token_count in dead_sessions.items():
            _logger.info(
                f"Discarded session and {token_count} token{'' if token_count == 1 else 's'} "
                f"for user {session.user}. (Session ID: {session.id})"
            )

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

        user = await self.server.db.get_user(username=username, password=password)
        if user is None:
            raise HTTPUnauthorized(reason="Incorrect username/password")

        tokens = self.server.user_id_to_tokens.setdefault(user.id, set())
        if len(tokens) >= max_tokens:
            raise HTTPForbidden(reason="Too many active tokens")

        token = token_urlsafe(32)
        tokens.add(token)
        _logger.info(f"Issued new token for user {user}.")

        try:
            session_id = data["session_id"]
            session = self.server.session_id_to_session[session_id]

            if not session.active or session.user != user:
                raise ValueError("Invalid session ID.")

            session.renew(duration)

        except (KeyError, ValueError):
            session_id = token_urlsafe(16)
            session = Session(session_id, user, duration)

            self.server.session_id_to_session[session_id] = session
            _logger.info(f"Issued new session for user {user}. (Session ID: {session_id})")

        self.server.token_to_session[token] = session

        return json_response(
            {
                "message": "Ok",
                "token": token,
                "duration": duration,
                "user_id": user.id,
                "username": username,
                "session_id": session_id,
                "state": session.state.to_json(),
            },
            status=200,
        )

    @route("post", "/auth/renew")
    @ratelimit(limit=10, interval=60, bucket_type=BucketType.Token)
    @validate_token
    async def renew(self, request: Request, /) -> Response:
        token = self.token_from_request(request)
        session = self.session_from_request(request)
        session.renew(duration)
        return json_response(
            {
                "message": "Ok",
                "token": token,
                "duration": duration,
                "user_id": session.user.id,
                "username": session.user.name,
                "session_id": session.id,
                "state": session.state.to_json(),
            },
            status=200,
        )

    @route("post", "/auth/logout")
    @ratelimit(limit=10, interval=60, bucket_type=BucketType.User)
    @validate_token
    async def logout(self, request: Request, /) -> Response:
        session = self.session_from_request(request)
        session.kill()
        return json_response(
            {
                "message": "Ok",
                "user_id": session.user.id,
                "username": session.user.name,
                "session_id": session.id,
                "state": session.state.to_json(),
            },
            status=200,
        )
