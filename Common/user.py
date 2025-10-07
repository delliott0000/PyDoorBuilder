from __future__ import annotations

from typing import TYPE_CHECKING

from .bases import ComparesIDABC, ComparesIDMixin

if TYPE_CHECKING:
    from typing import Any

    from asyncpg import Record

    from .team import Team

__all__ = ("User",)


class User(ComparesIDMixin, ComparesIDABC):
    __slots__ = (
        "_id",
        "_username",
        "_display_name",
        "_email",
        "_autopilot",
        "_admin",
        "_teams",
    )

    def __init__(self, user_record: Record | dict, /):
        self._id = user_record["id"]
        self._username = user_record["username"]
        self._display_name = user_record["display_name"]
        self._email = user_record["email"]
        self._autopilot = user_record["autopilot"]
        self._admin = user_record["admin"]
        self._teams = ...

    def __str__(self):
        return self._display_name or self._username

    @property
    def id(self) -> int:
        return self._id

    @property
    def username(self) -> str:
        return self._username

    @property
    def display_name(self) -> str | None:
        return self._display_name

    @property
    def email(self) -> str | None:
        return self._email

    @property
    def autopilot(self) -> bool:
        return self._autopilot

    @property
    def admin(self) -> bool:
        return self._admin

    @property
    def teams(self) -> frozenset[Team]:
        return self._teams

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self._id,
            "username": self._username,
            "display_name": self._display_name,
            "email": self._email,
            "autopilot": self._autopilot,
            "admin": self._admin,
            "teams": list(team.to_json() for team in self._teams),
        }
