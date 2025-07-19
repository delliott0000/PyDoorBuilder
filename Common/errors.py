from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._types import ResponseData

    from aiohttp import ClientResponse


__all__ = ("HTTPException",)


class HTTPException(Exception):
    def __init__(self, response: ClientResponse, data: ResponseData, /):
        super().__init__(f"{response.status} {response.reason}")
        self.response: ClientResponse = response
        self.data: ResponseData = deepcopy(data)
