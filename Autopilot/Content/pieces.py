from __future__ import annotations

from typing import TYPE_CHECKING

from .abcs import Piece
from .dxf_utils import draw_rectangle, new_msp

if TYPE_CHECKING:
    from ezdxf.document import Drawing

    from .bom import StaticBOMItem


__all__ = ()


# TODO: Piece subclasses


class MyPiece(Piece):
    def bom(self) -> tuple[StaticBOMItem, ...]:
        return ()

    def dxf(self) -> Drawing:
        msp = new_msp()
        draw_rectangle(msp, 0, 0, 1, 1)

        return msp.doc
