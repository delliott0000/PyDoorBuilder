from __future__ import annotations

from typing import TYPE_CHECKING

from Common import PostgreSQLClient, User

if TYPE_CHECKING:
    ...

__all__ = ("ServerPostgreSQLClient",)


class ServerPostgreSQLClient(PostgreSQLClient):
    async def get_user(
        self,
        *,
        user_id: str | None = None,
        username: str | None = None,
        password: str | None = None,
        with_password: bool = True,
    ) -> User | None:
        lookup = user_id or username
        if lookup is None:
            raise ValueError("Username or ID is required.")
        elif password is None and with_password is True:
            raise ValueError("Password is required.")

        ...

        return User("...", "...")
