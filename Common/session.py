from __future__ import annotations

from typing import TYPE_CHECKING

from .bases import ComparesIDABC, ComparesIDMixin
from .state import State
from .utils import log

if TYPE_CHECKING:
    from typing import Any

    from aiohttp.web import WebSocketResponse

    from .resource import Resource
    from .token import Token
    from .user import User

__all__ = ("Session",)


class Session(ComparesIDMixin, ComparesIDABC):
    __slots__ = ("_id", "_user", "_state", "_resource", "_connections")

    def __init__(
        self,
        _id: str,
        user: User,
        /,
        *,
        state: State | None = None,
    ):
        self._id = _id
        self._user = user
        self._state = state if state is not None else State()
        self._resource = None
        self._connections = {}

    @property
    def id(self) -> str:
        return self._id

    @property
    def user(self) -> User:
        return self._user

    @property
    def state(self) -> State:
        return self._state

    @property
    def resource(self) -> Resource | None:
        return self._resource

    @property
    def connections(self) -> dict[Token, WebSocketResponse]:
        return self._connections

    @property
    def connected(self) -> bool:
        return bool(self._connections)

    def acquire_resource(self, resource: Resource, /) -> None:
        if self._resource is None:
            resource.acquire(self)
            log(f"{self._user} acquired {resource.id}. (Session ID: {self._id})")
            self._resource = resource
        else:
            raise RuntimeError("Session has already acquired a resource.")

    def release_resource(self) -> None:
        if self._resource is not None:
            self._resource.release(self)
            log(f"{self._user} released {self._resource.id}. (Session ID: {self._id})")
            self._resource = None

    def to_json(self) -> dict[str, Any]:
        try:
            resource_id = self._resource.id
        except AttributeError:
            resource_id = None

        return {
            "id": self._id,
            "user": self._user.to_json(),
            "state": self._state.to_json(),
            "resource_id": resource_id,
        }
