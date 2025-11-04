from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from .bases import ComparesIDABC, ComparesIDMixin
from .errors import ResourceLocked, ResourceNotOwned

if TYPE_CHECKING:
    from collections.abc import Iterable
    from typing import Any, Self

    from asyncpg import Record

    from .session import Session
    from .user import User

    Json = dict[str, Any]

__all__ = ("ResourceJSONVersion", "ResourceABC", "ResourceMixin", "Resource")


# fmt: off
class ResourceJSONVersion(Enum):
    metadata = 0
    preview  = 1
    view     = 2
# fmt: on


class ResourceABC(ComparesIDABC, ABC):
    __slots__ = ()

    @property
    @abstractmethod
    def owner(self) -> User:
        pass

    @classmethod
    @abstractmethod
    def new(cls, data: dict[str, Record | Iterable[Record]], /) -> Self:
        pass

    @abstractmethod
    def to_json(self, *, version: ResourceJSONVersion) -> Json:
        pass


class ResourceMixin(ComparesIDMixin):
    __slots__ = ()

    def __init__(self, session: Session | None = None, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._session = session  # noqa

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
            raise ResourceLocked(session, self)  # noqa
        else:
            self._session = session  # noqa

    def release(
        self, session: Session | None = None, /, *, unconditional: bool = False
    ) -> None:
        if not self.locked:
            return
        elif not unconditional and self._session != session:
            raise ResourceNotOwned(session, self)  # noqa
        else:
            self._session = None  # noqa


@runtime_checkable
class Resource(Protocol):
    def __init__(
        self, session: Session | None = None, *args: Any, **kwargs: Any  # noqa
    ) -> None:
        raise TypeError("Resource can not be directly instantiated.")

    def __init_subclass__(cls, **kwargs: Any):
        raise TypeError("Inherit from (ResourceMixin, ResourceABC) instead.")

    @property
    def id(self) -> Any: ...
    @property
    def user(self) -> User | None: ...
    @property
    def locked(self) -> bool: ...
    def acquire(self, session: Session, /) -> None: ...
    def release(
        self, session: Session | None = None, /, *, unconditional: bool = False
    ) -> None: ...
    @property
    def owner(self) -> User: ...
    @classmethod
    def new(cls, data: dict[str, Record | Iterable[Record]], /) -> Self: ...
    def to_json(self, *, version: ResourceJSONVersion) -> Json: ...
