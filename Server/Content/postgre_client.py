from Common import PostgreSQLClient, Team, User, check_password, encrypt_password

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

        team_assignment_records = await self.fetch_all(
            "SELECT team_id FROM team_assignments WHERE user_id = $1", user_record["id"]
        )
        team_ids = (record["team_id"] for record in team_assignment_records)
        teams = await self.get_teams(*team_ids)

        return User(user_record, teams)

    async def get_teams(self, *team_ids: int) -> frozenset[Team]:
        if not team_ids:
            return frozenset()

        team_records = await self.fetch_all("SELECT * FROM teams WHERE id = ANY($1)", team_ids)

        if not team_records:
            return frozenset()

        ...
