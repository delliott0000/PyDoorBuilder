from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Self

__all__ = ("State",)


class State:
    __slots__ = ()

    @classmethod
    def from_json(cls, json: dict[str, Any], /) -> Self: ...

    def to_json(self) -> dict[str, Any]: ...
