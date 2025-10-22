from __future__ import annotations

from typing import TYPE_CHECKING

from Common import (
    Permission,
    PermissionScope,
    PermissionType,
    PostgreSQLClient,
    Team,
    User,
    check_password,
    encrypt_password,
)

if TYPE_CHECKING:
    from asyncpg import Record

__all__ = ("ServerPostgreSQLClient",)


DUMMY_HASH = encrypt_password("my_dummy_password")


class ServerPostgreSQLClient(PostgreSQLClient):
    async def new_id(self) -> int:
        record = await self.fetch_one("INSERT INTO ids DEFAULT VALUES RETURNING id")
        return record["id"]

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
            user_record = await self.fetch_one("SELECT * FROM users WHERE id = $1", user_id)
        elif username is not None:
            user_record = await self.fetch_one(
                "SELECT * FROM users WHERE username = $1", username
            )
        else:
            raise ValueError("Username or ID is required.")

        if user_record is None:
            if with_password:
                # Dummy check so we don't leak any info through query timing
                check_password(password, DUMMY_HASH)
            return None
        elif with_password and not check_password(password, user_record["password"]):
            return None

        return User(user_record, frozenset())

    async def get_team_records(self, *team_ids: int) -> dict[int, Record]: ...

    async def get_company_records(self, *company_ids: int) -> dict[int, Record]: ...

    async def get_permission_records(self, *team_ids: int) -> dict[int, list[Record]]: ...
