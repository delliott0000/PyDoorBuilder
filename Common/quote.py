from __future__ import annotations

from typing import TYPE_CHECKING

from .bases import ComparesIDFormattedABC, ComparesIDFormattedMixin

if TYPE_CHECKING:
    from typing import Any

    from .resource import ResourceJSONVersion
    from .user import PartialUser

__all__ = ("Quote",)


class Quote(ComparesIDFormattedMixin, ComparesIDFormattedABC):
    __slots__ = ()

    @property
    def id(self) -> int: ...

    @property
    def formatted_id(self) -> str: ...

    @property
    def owner(self) -> PartialUser: ...

    def to_json(self, *, version: ResourceJSONVersion) -> dict[str, Any]: ...
