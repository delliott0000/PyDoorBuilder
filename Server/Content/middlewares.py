from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from aiohttp.web import HTTPException, json_response, middleware
from multidict import CIMultiDict

if TYPE_CHECKING:
    from collections.abc import Callable, Coroutine
    from typing import Any

    from aiohttp.web import Request, Response

    Handler = Callable[[Request], Coroutine[Any, Any, Response]]

__all__ = ("middlewares",)


_logger = getLogger()


@middleware
async def json_wrapper(request: Request, handler: Handler) -> Response:
    try:
        return await handler(request)
    except HTTPException as error:
        headers = CIMultiDict(error.headers or {})
        headers.pop("Content-Type", None)
        return json_response({"message": error.reason}, status=error.status, headers=headers)
    except Exception as error:
        _logger.exception(f"An error occurred whilst processing a request - {error}")
        return json_response({"message": "Internal server error"}, status=500)


middlewares = (json_wrapper,)
