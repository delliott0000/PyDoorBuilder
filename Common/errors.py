from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

    from aiohttp import ClientResponse

    Json = dict[str, Any]

__all__ = ("HTTPException", "ValidationError")


class HTTPException(Exception):
    def __init__(self, response: ClientResponse, data: Json, /):
        super().__init__(f"{response.status} {response.reason}")
        self.response: ClientResponse = response
        self.data: Json = dict(data)


class ValidationError(Exception):
    def __init__(self, results: set[str], /):
        super().__init__("\n".join(results))
        self.results: set[str] = set(results)
