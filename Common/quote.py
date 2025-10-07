from __future__ import annotations

from typing import TYPE_CHECKING

from .bases import ComparesIDABC, ComparesIDMixin

if TYPE_CHECKING:
    from .user import User

__all__ = ("Quote",)


class Quote(ComparesIDMixin, ComparesIDABC):
    __slots__ = ()

    @property
    def id(self) -> int: ...

    @property
    def formatted_id(self) -> str: ...

    @property
    def owner(self) -> User: ...
