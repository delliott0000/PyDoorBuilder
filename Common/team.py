from __future__ import annotations

from typing import TYPE_CHECKING

from .bases import ComparesIDABC, ComparesIDMixin

if TYPE_CHECKING:
    from asyncpg import Record

__all__ = ("Team",)


class Team(ComparesIDMixin, ComparesIDABC):
    __slots__ = ("_id", "_name")

    def __init__(self, team_record: Record | dict, /):
        self._id = team_record["id"]
        self._name = team_record["name"]

    def __str__(self):
        return self._name

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name
