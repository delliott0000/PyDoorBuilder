from __future__ import annotations

from typing import TYPE_CHECKING

from Common import PostgreSQLClient, User, check_password

if TYPE_CHECKING:
    ...

__all__ = ("ServerPostgreSQLClient",)


class ServerPostgreSQLClient(PostgreSQLClient):
    async def get_user(
        self,
        *,
        user_id: int | None = None,
        username: str | None = None,
        password: str | None = None,
        with_password: bool = True,
    ) -> User | None:
        if password is None and with_password is True:
            raise ValueError("Password is required.")
        elif user_id is not None:
            record = await self.fetch_one("SELECT * FROM users WHERE id = $1", user_id)
        elif username is not None:
            record = await self.fetch_one("SELECT * FROM users WHERE username = $1", username)
        else:
            raise ValueError("Username or ID is required.")

        if record is None:
            return None
        elif with_password and not check_password(password, record["password"]):
            raise ValueError("Incorrect password.")

        return User(record)
