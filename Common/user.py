from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

__all__ = ("User",)


class User:
    __slots__ = ("_id", "_name", "_autopilot")

    def __init__(self, _id: str, name: str, autopilot: bool, /):
        self._id = _id
        self._name = name
        self._autopilot: bool = autopilot

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

    @property
    def autopilot(self) -> bool:
        return self._autopilot

    def to_json(self) -> dict[str, Any]:
        return {"id": self._id, "name": self._name, "autopilot": self._autopilot}
