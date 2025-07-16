from __future__ import annotations

from typing import TYPE_CHECKING

from Common import Door

from .abcs import ImplementsBOM

if TYPE_CHECKING:
    from ._types import AnyBOMItem
    from .abcs import Piece


__all__ = ("APDoor",)


class APDoor(Door, ImplementsBOM):

    def pieces(self) -> tuple[Piece, ...]:
        # TODO: implement this
        return ()

    def bom(self) -> tuple[AnyBOMItem, ...]:
        # TODO: implement this
        return ()
