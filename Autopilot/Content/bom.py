from __future__ import annotations

from typing import TYPE_CHECKING

from .abcs import BOMBase, DynamicBOMItem

if TYPE_CHECKING:
    ...


__all__ = ("StaticBOMItem",)


class StaticBOMItem(BOMBase):
    def populate(self) -> None: ...


# TODO: DynamicBOMItem subclasses


class MyDynamicBOMItem(DynamicBOMItem):
    @property
    def description(self) -> str:
        return "..."
