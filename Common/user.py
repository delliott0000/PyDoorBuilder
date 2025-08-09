from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

    from asyncpg import Record

__all__ = ("User",)


class User:
    __slots__ = ("_id", "_username", "_display_name", "_email", "_autopilot", "_admin")

    def __init__(self, record: Record, /):
        self._id = record["id"]
        self._username = record["username"]
        self._display_name = record["display_name"]
        self._email = record["email"]
        self._autopilot = record["autopilot"]
        self._admin = record["admin"]

    def __hash__(self):
        return hash(self._id)

    def __str__(self):
        return self._display_name

    def __eq__(self, other):
        return isinstance(other, User) and self._id == other._id

    @property
    def id(self) -> int:
        return self._id

    @property
    def username(self) -> str:
        return self._username

    @property
    def display_name(self) -> str:
        return self._display_name

    @property
    def email(self) -> str:
        return self._email

    @property
    def autopilot(self) -> bool:
        return self._autopilot

    @property
    def admin(self) -> bool:
        return self._admin

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self._id,
            "username": self._username,
            "display_name": self._display_name,
            "email": self.email,
            "autopilot": self._autopilot,
        }
