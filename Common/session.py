from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from .utils import now

if TYPE_CHECKING:
    from datetime import datetime

    from .user import User

__all__ = ("Session",)


class Session:
    __slots__ = ("_user", "_token", "_expires", "_killed")

    def __init__(self, user: User, token: str, duration: float, /, *, killed: bool = False):
        self._user: User = user
        self._token: str = token
        self._expires: datetime
        self._killed: bool = killed
        self.refresh(duration)

    @property
    def user(self) -> User:
        return self._user

    @property
    def token(self) -> str:
        return self._token

    @property
    def expires(self) -> datetime:
        return self._expires

    @property
    def killed(self) -> bool:
        return self._killed

    @property
    def expired(self) -> bool:
        return self.expires <= now()

    @property
    def active(self) -> bool:
        return not self.killed and not self.expired

    def kill(self) -> None:
        self._killed = True

    def refresh(self, duration: float, /) -> None:
        if not self.killed:
            self._expires = now() + timedelta(seconds=duration)
