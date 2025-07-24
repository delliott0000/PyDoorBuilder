from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    ...

__all__ = ("User",)


class User:
    __slots__ = ("_id", "name")

    def __init__(self, _id: str, name: str, /):
        self._id: str = _id
        self.name: str = name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, User) and self.id == other.id

    @property
    def id(self) -> str:
        return self._id
