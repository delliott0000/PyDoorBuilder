from dataclasses import dataclass
from enum import Enum

__all__ = ("PermissionType", "PermissionScope", "Permission")


# fmt: off
class PermissionType(Enum):
    create   = "create"
    preview  = "preview"
    view     = "view"
    acquire  = "acquire"
    update   = "update"
    generate = "generate"
    delete   = "delete"
    reassign = "reassign"


class PermissionScope(Enum):
    safe      = "safe"
    company   = "company"
    universal = "universal"
    null      = None

    __rank__ = {safe: 0, company: 1, universal: 2}

    def __check_null__(self, other):
        if not isinstance(other, PermissionScope):
            return NotImplemented
        return self.value is None or other.value is None

    def __lt__(self, other):
        return self.__check_null__(other) or self.__rank__[self.value] < self.__rank__[other.value]  # noqa

    def __gt__(self, other):
        return self.__check_null__(other) or self.__rank__[self.value] > self.__rank__[other.value]  # noqa


@dataclass(kw_only=True, slots=True, frozen=True)
class Permission:
    type:  PermissionType
    scope: PermissionScope
