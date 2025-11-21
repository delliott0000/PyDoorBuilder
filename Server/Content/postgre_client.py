from Common import PostgreSQLClient

__all__ = ("ServerPostgreSQLClient",)


class ServerPostgreSQLClient(PostgreSQLClient):
    async def new_id(self) -> int:
        record = await self.fetch_one("INSERT INTO ids DEFAULT VALUES RETURNING id")
        return record["id"]
