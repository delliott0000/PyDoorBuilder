from __future__ import annotations

from collections import defaultdict
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

        team_assignments = await self.get_assignments(user_record["id"])
        team_ids = team_assignments.get(user_record["id"], [])
        teams = await self.build_teams(*team_ids)

        return User(user_record, teams)

    async def build_teams(self, *team_ids: int) -> frozenset[Team]: ...

    async def get_team_records(self, *team_ids: int) -> dict[int, Record]: ...

    async def get_company_records(self, *company_ids: int) -> dict[int, Record]: ...

    async def get_permission_records(self, *team_ids: int) -> dict[int, list[Record]]: ...

    async def get_assignments(self, *ids: int, inverse: bool = False) -> dict[int, list[int]]:
        if not ids:
            return {}

        key_map = {False: "user_id", True: "team_id"}
        key = key_map[inverse]
        val = key_map[not inverse]

        assignment_records = await self.fetch_all(
            f"SELECT * FROM team_assignments WHERE {key} = ANY($1)", ids
        )
        assignments = defaultdict(list)

        for record in assignment_records:
            assignments[record[key]].append(record[val])

        return dict(assignments)
