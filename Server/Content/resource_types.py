from __future__ import annotations

from typing import TYPE_CHECKING

from Common import Quote, ResourceABC, ResourceMixin

if TYPE_CHECKING:
    from collections.abc import Iterable
    from typing import Self

    from asyncpg import Record

__all__ = ("QuoteResource",)


class QuoteResource(ResourceMixin, Quote, ResourceABC):
    __slots__ = ("_session",)

    @classmethod
    def new(cls, data: dict[str, Record | Iterable[Record]], /) -> Self: ...
