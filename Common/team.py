from __future__ import annotations

from typing import TYPE_CHECKING

from .bases import ComparesIDABC, ComparesIDMixin

if TYPE_CHECKING:
    from asyncpg import Record

    from .company import Company
    from .permissions import Permission

__all__ = ("Team",)


class Team(ComparesIDMixin, ComparesIDABC):
    __slots__ = ("_id", "_name", "_hierarchy_index", "_company", "_permissions")

    def __init__(
        self,
        team_record: Record | dict,
        company: Company,
        permissions: frozenset[Permission],
        /,
    ):
        self._id = team_record["id"]
        self._name = team_record["name"]
        self._hierarchy_index = team_record["hierarchy_index"]
        self._company = company
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
    def hierarchy_index(self) -> int:
        return self._hierarchy_index

    @property
    def company(self) -> Company:
        return self._company

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
                perm.scope > permission.scope
                for perm in self._permissions
            )
        )
        # fmt: on
