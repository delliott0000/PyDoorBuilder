from __future__ import annotations

from typing import TYPE_CHECKING

from Common import Door

from .abcs import ImplementsBOM

if TYPE_CHECKING:
    from ._types import AnyBOMItem
    from .abcs import Piece


__all__ = ("APDoor",)


class APDoor(Door, ImplementsBOM):
    @property
    def pieces(self) -> tuple[Piece, ...]:
        # TODO: implement this
        return ()

    @property
    def leaf_bom(self) -> tuple[AnyBOMItem, ...]:
        # TODO: implement this
        return ()

    @property
    def frame_bom(self) -> tuple[AnyBOMItem, ...]:
        # TODO: implement this
        return ()

    @property
    def bom(self) -> tuple[AnyBOMItem, ...]:
        # TODO: implement this
        if ... and ...:
            raise ...
        elif ...:
            return self.frame_bom
        elif ...:
            return self.leaf_bom
        else:
            return self.frame_bom + self.leaf_bom
