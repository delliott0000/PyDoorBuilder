from __future__ import annotations

from typing import TYPE_CHECKING

from .state import State

if TYPE_CHECKING:
    from typing import Any

    from .user import User

__all__ = ("Session",)


class Session:
    __slots__ = ("_id", "_user", "_state")

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

    def to_json(self) -> dict[str, Any]:
        return {"id": self._id, "state": self._state.to_json()}
