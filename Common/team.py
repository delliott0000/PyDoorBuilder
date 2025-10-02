from .bases import ComparesIDABC, ComparesIDMixin

__all__ = ("Team",)


class Team(ComparesIDMixin, ComparesIDABC):
    def __init__(self): ...

    @property
    def id(self) -> int: ...
