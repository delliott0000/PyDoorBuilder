from __future__ import annotations

from typing import TYPE_CHECKING

from .bases import ComparesIDABC, ComparesIDMixin

if TYPE_CHECKING:
    from asyncpg import Record

    from .permissions import Permission

__all__ = ("Team",)


class Team(ComparesIDMixin, ComparesIDABC):
    __slots__ = ("_id", "_name", "_permissions")

    def __init__(self, team_record: Record | dict, permissions: frozenset[Permission], /):
        self._id = team_record["id"]
        self._name = team_record["name"]
        self._permissions = permissions

    def __str__(self):
        return self._name

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def permissions(self) -> frozenset[Permission]:
        return self._permissions

    def has_permission(self, permission: Permission, /) -> bool:
        # fmt: off
        return (
            permission in self._permissions
            or
            any(
                perm.type == permission.type
                and
                perm.scope >= permission.scope
                for perm in self._permissions
            )
        )
        # fmt: on
