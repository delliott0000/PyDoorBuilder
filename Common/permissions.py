from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    ...

__all__ = ("Permissions", "ADMIN_PERMISSIONS", "DEFAULT_PERMISSIONS")


@dataclass(kw_only=True, frozen=True, slots=True)
class Permissions:
    pass


ADMIN_PERMISSIONS = Permissions()
DEFAULT_PERMISSIONS = Permissions()
