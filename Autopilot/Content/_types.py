from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .abcs import DynamicBOMItem
    from .bom import StaticBOMItem

    AnyBOMItem = StaticBOMItem | DynamicBOMItem
