from __future__ import annotations

from typing import TYPE_CHECKING

from Common import (
    Company,
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
    from collections.abc import Iterable

__all__ = ("ServerPostgreSQLClient",)


DUMMY_HASH = encrypt_password("my_dummy_password")


class ServerPostgreSQLClient(PostgreSQLClient):
    def validate_ids(
        self,
        passed_ids: Iterable[int],
        found_ids: Iterable[int],
        /,
        *,
        context: str | None = None,
    ) -> None:
        missing_ids = set(passed_ids) - set(found_ids)
        if missing_ids:
            formatted_missing_ids = ", ".join(map(str, sorted(missing_ids)))
            formatted_context = context or "item"
            raise ValueError(
                f"Some of the requested {formatted_context} IDs were not found: {formatted_missing_ids}"
            )

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
        teams = await self.get_teams(*team_ids)

        return User(user_record, frozenset(teams.values()))

    async def get_teams(self, *team_ids: int) -> dict[int, Team]:
        if not team_ids:
            return {}

        ...

        teams = {}
        self.validate_ids(team_ids, teams.keys(), context="team")

        return teams

    async def get_companies(self, *company_ids: int) -> dict[int, Company]:
        if not company_ids:
            return {}

        company_records = await self.fetch_all(
            "SELECT * FROM companies WHERE id = ANY($1)", company_ids
        )

        companies = {record["id"]: Company(record) for record in company_records}
        self.validate_ids(company_ids, companies.keys(), context="company")

        return companies

    async def get_permissions(self, *team_ids: int) -> dict[int, list[Permission]]:
        if not team_ids:
            return {}

        permission_records = await self.fetch_all(
            "SELECT * FROM team_permissions WHERE team_id = ANY($1)", team_ids
        )

        permissions = {id_: [] for id_ in team_ids}

        for record in permission_records:
            permissions[record["team_id"]].append(
                Permission(
                    type=PermissionType(record["permission_type"]),
                    scope=PermissionScope(record["permission_scope"]),
                )
            )

        return permissions

    async def get_assignments(self, *ids: int, inverse: bool = False) -> dict[int, list[int]]:
        if not ids:
            return {}

        key_map = {False: "user_id", True: "team_id"}
        key = key_map[inverse]
        val = key_map[not inverse]

        assignment_records = await self.fetch_all(
            f"SELECT * FROM team_assignments WHERE {key} = ANY($1)", ids
        )

        assignments = {id_: [] for id_ in ids}

        for record in assignment_records:
            assignments[record[key]].append(record[val])

        return assignments
