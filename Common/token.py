from __future__ import annotations

from datetime import datetime, timedelta
from secrets import token_urlsafe
from typing import TYPE_CHECKING

from .utils import now

if TYPE_CHECKING:
    from .session import Session

    ExpirationType = datetime | timedelta | float


class Token:
    __slots__ = (
        "_id",
        "_nbytes",
        "_session",
        "_killed",
        "_killed_at",
        "_access",
        "_refresh",
        "_access_expires",
        "_refresh_expires",
    )

    def __init__(
        self,
        nbytes: int,
        session: Session,
        /,
        *,
        access_expires: ExpirationType,
        refresh_expires: ExpirationType,
        killed: bool = False,
    ):
        self._id = token_urlsafe(nbytes)
        self._nbytes = nbytes
        self._session = session
        self._killed = killed
        self._killed_at = None
        self.renew(access_expires=access_expires, refresh_expires=refresh_expires)

    def __hash__(self):
        return hash(self._id)

    def __eq__(self, other):
        return isinstance(other, Token) and self._id == other._id

    @property
    def id(self) -> str:
        return self._id

    @property
    def session(self) -> Session:
        return self._session

    @property
    def killed(self) -> bool:
        return self._killed

    @property
    def killed_at(self) -> datetime | None:
        return self._killed_at

    @property
    def access(self) -> str:
        return self._access

    @property
    def refresh(self) -> str:
        return self._refresh

    @property
    def access_expires(self) -> datetime:
        return self._access_expires

    @property
    def refresh_expires(self) -> datetime:
        return self._refresh_expires

    @property
    def active(self) -> bool:
        return not self._killed and self._access_expires > now()

    @property
    def expired(self) -> bool:
        return self._killed or self._refresh_expires < now()

    def kill(self) -> bool:
        if not self._killed:
            self._killed = True
            self._killed_at = now()

            return True
        else:
            return False

    def renew(
        self,
        *,
        access_expires: ExpirationType,
        refresh_expires: ExpirationType,
    ) -> bool:
        if not self._killed:
            t = now()
            attrs = {}

            for attr, arg in (
                ("_access_expires", access_expires),
                ("_refresh_expires", refresh_expires),
            ):
                if isinstance(arg, datetime):
                    attrs[attr] = arg
                elif isinstance(arg, timedelta):
                    attrs[attr] = t + arg
                elif isinstance(arg, (float, int)):
                    attrs[attr] = t + timedelta(seconds=arg)
                else:
                    raise TypeError("Expiration type not supported.")

            self._access = token_urlsafe(self._nbytes)
            self._refresh = token_urlsafe(self._nbytes)

            for attr in attrs:
                setattr(self, attr, attrs[attr])

            return True
        else:
            return False
