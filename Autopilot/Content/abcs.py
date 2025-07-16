from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

    from ezdxf.document import Drawing

    from ._types import AnyBOMItem
    from .door_ap import APDoor


__all__ = ("BOMBase", "DynamicBOMItem", "ImplementsBOM", "Piece", "Hardware")


class BOMBase(ABC):
    def __init__(self, item_code: str, quantity: float, /):
        self.item_code: str = item_code
        self.quantity: float = quantity


class DynamicBOMItem(BOMBase, ABC):
    # TODO: implement abstract methods for fields
    ...


class ImplementsBOM(ABC):
    @abstractmethod
    def bom(self) -> Iterable[AnyBOMItem]:
        pass


class Piece(ImplementsBOM, ABC):
    def __init__(self, door: APDoor, /):
        self.door: APDoor = door

    @abstractmethod
    def dxf(self) -> Drawing:
        pass


class Hardware(ImplementsBOM, ABC):
    @abstractmethod
    def pieces(self) -> Iterable[Piece]:
        pass

    @abstractmethod
    def edit_dxf(self, dxf: Drawing, /) -> None:
        pass
