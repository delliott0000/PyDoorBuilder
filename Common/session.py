from __future__ import annotations

from typing import TYPE_CHECKING

from .state import State
from .utils import log

if TYPE_CHECKING:
    from typing import Any

    from .resource import Resource
    from .user import User

__all__ = ("Session",)


class Session:
    __slots__ = ("_id", "_user", "_state", "_resource")

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

    def __hash__(self):
        return hash(self._id)

    def __eq__(self, other):
        return isinstance(other, Session) and self._id == other._id

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

    def acquire_resource(self, resource: Resource, /) -> None:
        if self._resource is None:
            resource.acquire(self)
            log(f"{self.user} acquired {resource.id}. (Session ID: {self._id})")
            self._resource = resource
        else:
            raise RuntimeError("Session has already acquired a resource.")

    def release_resource(self) -> None:
        if self._resource is not None:
            self._resource.release(self)
            log(f"{self.user} released {self._resource.id}. (Session ID: {self._id})")
            self._resource = None

    def to_json(self) -> dict[str, Any]:
        return {"id": self._id, "state": self._state.to_json()}
