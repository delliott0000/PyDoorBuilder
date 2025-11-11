from __future__ import annotations

from typing import TYPE_CHECKING

from .bases import ComparesIDFormattedABC, ComparesIDFormattedMixin
from .enums import DoorType
from .errors import ValidationError
from .rules import door_rules

if TYPE_CHECKING:
    from typing import Any

__all__ = ("Door",)


class Door(ComparesIDFormattedMixin, ComparesIDFormattedABC):
    def __init__(self, **kwargs: Any):
        self.__type = DoorType(kwargs.get("type", DoorType.Single))

        self.__so_x: float = kwargs.get("so_x", 1000)
        self.__so_y: float = kwargs.get("so_y", 2100)

        self.__leaf_split: tuple[float, float] | None
        self.reset_leaf_split()

    @property
    def id(self) -> int: ...

    @property
    def formatted_id(self) -> str: ...

    @property
    def type(self) -> DoorType:
        return self.__type

    @type.setter
    def type(self, value: DoorType):
        self.__type = value
        self.reset_leaf_split()

    @property
    def is_double(self) -> bool:
        return self.type == DoorType.Double

    @property
    def so_x(self) -> float:
        return self.__so_x

    @so_x.setter
    def so_x(self, value: float):
        self.__so_x = value
        self.reset_leaf_split()

    @property
    def so_y(self) -> float:
        return self.__so_y

    @so_y.setter
    def so_y(self, value: float):
        self.__so_y = value

    @property
    def so_to_frame_x(self) -> float:
        return -15

    @property
    def so_to_frame_y(self) -> float:
        return -10

    @property
    def frame_x(self) -> float:
        return self.so_x + self.so_to_frame_x

    @frame_x.setter
    def frame_x(self, value: float):
        self.so_x = value - self.so_to_frame_x

    @property
    def frame_y(self) -> float:
        return self.so_y + self.so_to_frame_y

    @frame_y.setter
    def frame_y(self, value: float):
        self.so_y = value - self.so_to_frame_y

    @property
    def frame_to_leaf_x(self) -> float:
        if self.is_double:
            return -95
        else:
            return -92

    @property
    def frame_to_leaf_y(self) -> float:
        return -50

    @property
    def leaf_sum_x(self) -> float:
        return self.frame_x + self.frame_to_leaf_x

    @property
    def active_leaf_x(self) -> float:
        if self.is_double:
            return self.__leaf_split[0]
        else:
            return self.leaf_sum_x

    @active_leaf_x.setter
    def active_leaf_x(self, value: float):
        if not self.is_double:
            self.frame_x = value - self.frame_to_leaf_x
        elif value >= self.leaf_sum_x:
            raise ValueError(f"Active leaf width of {value}mm is out of range.")
        else:
            self.__leaf_split = (value, self.leaf_sum_x - value)

    @property
    def passive_leaf_x(self) -> float | None:
        if self.is_double:
            return self.__leaf_split[1]
        else:
            return None

    @passive_leaf_x.setter
    def passive_leaf_x(self, value: float):
        if not self.is_double:
            pass
        elif value >= self.leaf_sum_x:
            raise ValueError(f"Passive leaf width of {value}mm is out of range.")
        else:
            self.__leaf_split = (self.leaf_sum_x - value, value)

    @property
    def leaf_y(self) -> float:
        return self.frame_y + self.frame_to_leaf_y

    @leaf_y.setter
    def leaf_y(self, value: float):
        self.frame_y = value - self.frame_to_leaf_y

    def reset_leaf_split(self) -> None:
        if self.is_double:
            self.__leaf_split = (self.leaf_sum_x / 2, self.leaf_sum_x / 2)
        else:
            self.__leaf_split = None

    def validate(self) -> None:
        results = set()

        for rule in door_rules:
            result = rule(self)
            results.add(result)

        results.discard(None)

        if results:
            raise ValidationError(results)
