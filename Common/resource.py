from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

    from .session import Session
    from .user import User

__all__ = ("Resource",)


class Resource(ABC):
    __slots__ = ()  # Defer to subclasses

    def __init__(self, _id: str, session: Session | None = None, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._id = _id  # noqa
        self._session = session  # noqa

    def __eq__(self, other):
        return isinstance(other, Resource) and self._id == other._id

    def __hash__(self):
        return hash(self._id)

    @property
    def id(self) -> str:
        return self._id

    @property
    def user(self) -> User | None:
        try:
            return self._session.user
        except AttributeError:
            return None

    @property
    def locked(self) -> bool:
        return self._session is not None

    def acquire(self, session: Session, /) -> None:
        if self.locked:
            raise RuntimeError("Cannot acquire a locked resource.")
        else:
            self._session = session  # noqa

    def release(
        self, session: Session | None = None, /, *, unconditional: bool = False
    ) -> None:
        if not self.locked:
            return
        elif not unconditional and self._session != session:
            raise RuntimeError("Cannot release a resource locked by another session.")
        else:
            self._session = None  # noqa
