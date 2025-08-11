from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    from .door import Door

    MaybeStr = str | None
    DoorRule = Callable[[Door], MaybeStr]

__all__ = ("door_rules", "door_rule")


door_rules: list[DoorRule] = []


def door_rule(func: DoorRule, /) -> DoorRule:
    door_rules.append(func)
    return func
