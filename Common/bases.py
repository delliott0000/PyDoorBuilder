from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

__all__ = ("ComparesIDABC", "ComparesIDMixin")


class ComparesIDABC(ABC):
    __slots__ = ()

    @property
    @abstractmethod
    def id(self) -> Any:
        pass


class ComparesIDMixin:
    __slots__ = ()

    def __hash__(self):
        return hash((type(self), self.id))  # noqa

    def __eq__(self, other):
        return type(self) is type(other) and self.id == other.id  # noqa
