from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    ...

__all__ = ("Permissions", "DEFAULT_PERMISSIONS", "ADMIN_PERMISSIONS", "EMPTY_PERMISSIONS")


@dataclass(kw_only=True, frozen=True, slots=True)
class Permissions:
    pass


DEFAULT_PERMISSIONS = Permissions()
ADMIN_PERMISSIONS = Permissions()
EMPTY_PERMISSIONS = Permissions()
