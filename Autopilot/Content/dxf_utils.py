from __future__ import annotations

from typing import TYPE_CHECKING

from ezdxf import new

from Common import DXF_VERSION

if TYPE_CHECKING:
    from typing import Any

    from ezdxf.layouts import Modelspace


__all__ = ("new_msp", "draw_rectangle")


def new_msp() -> Modelspace:
    return new(DXF_VERSION).modelspace()


def draw_rectangle(
    msp: Modelspace, x: float, y: float, w: float, h: float, **kwargs: Any
) -> None:
    msp.add_lwpolyline(
        ((x, y), (x + w, y), (x + w, y + h), (x, y + h)),
        close=kwargs.pop("close", True),
        dxfattribs=kwargs,
    )
