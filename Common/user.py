from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    ...

__all__ = ("User",)


class User:
    __slots__ = ("_id", "_name")

    def __init__(self, _id: str, name: str, /):
        self._id = _id
        self._name = name

    def __hash__(self):
        return hash(self._id)

    def __str__(self):
        return self._name

    def __eq__(self, other):
        return isinstance(other, User) and self._id == other._id

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name
