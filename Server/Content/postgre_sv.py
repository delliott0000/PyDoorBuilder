from __future__ import annotations

from typing import TYPE_CHECKING

from Common import PostgreSQLClient

if TYPE_CHECKING:
    ...


__all__ = ("ServerPostgreSQLClient",)


class ServerPostgreSQLClient(PostgreSQLClient):
    ...
