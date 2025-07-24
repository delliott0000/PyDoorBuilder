from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

    from aiohttp import ClientResponse

    Json = dict[str, Any]

__all__ = ("HTTPException",)


class HTTPException(Exception):
    def __init__(self, response: ClientResponse, data: Json, /):
        super().__init__(f"{response.status} {response.reason}")
        self.response: ClientResponse = response
        self.data: Json = deepcopy(data)
