from __future__ import annotations

from asyncio import sleep
from logging import getLogger
from time import time
from typing import TYPE_CHECKING

from aiohttp import ClientSession

from .config import global_config
from .errors import HTTPException

if TYPE_CHECKING:
    from collections.abc import Coroutine
    from typing import Any

    from .route import Route

    Json = dict[str, Any]
    JsonCoro = Coroutine[Any, Any, Json]

__all__ = ("HTTPClient",)


_logger = getLogger()


class HTTPClient:
    def __init__(self):
        self.config: dict[str, Any] = global_config["api"]["http"]
        self.__session: ClientSession | None = None

    @property
    def is_open(self) -> bool:
        return self.__session is not None and not self.__session.closed

    def get_retry_after(self, error: HTTPException, /) -> float | None:
        try:
            return float(error.response.headers.get("Retry-After"))
        except (AttributeError, TypeError, ValueError):
            return None

    async def create_connection(self) -> None:
        self.__session = ClientSession()

    async def close_connection(self) -> None:
        if self.is_open is True:
            await self.__session.close()

    async def make_request(self, method: str, raw_url: str, /, **kwargs: Any) -> Json:
        if self.is_open is False:
            raise RuntimeError("HTTP session is closed.")

        pre_time = time()
        async with self.__session.request(method, raw_url, **kwargs) as response:
            _logger.info(
                "%s %s returned %s %s in %.3fs",
                method.upper(),
                raw_url,
                response.status,
                response.reason,
                time() - pre_time,
            )
            data = await response.json()

            if 200 <= response.status < 300:
                return data

            raise HTTPException(response, data)

    async def request(self, method: str, url: str | Route, /, **kwargs: Any) -> Json:
        url = str(url)
        config = self.config

        tries = 0
        total_slept = 0
        backoff = config["backoff_start"]

        while True:
            tries += 1
            sleep_time = 0

            try:
                return await self.make_request(method, url, **kwargs)

            except HTTPException as error:
                if tries >= config["max_retries"]:
                    raise error

                elif error.response.status == 429:
                    retry_after = self.get_retry_after(error)

                    if retry_after is not None:
                        if (
                            config["handle_ratelimits"] is True
                            and retry_after <= config["max_retry_after"]
                        ):
                            sleep_time = retry_after

                    else:
                        backoff *= config["backoff_factor"]
                        if (
                            config["handle_backoffs"] is True
                            and backoff <= config["backoff_cap"]
                        ):
                            sleep_time = backoff

                elif error.response.status >= 500:
                    sleep_time = 2 * (tries - 1) + 0.5

                if sleep_time > 0:
                    total_slept += sleep_time
                    if total_slept >= config["max_sleep_time"]:
                        raise error

                    _logger.info(
                        "Retrying %s %s in %.3fs...",
                        method.upper(),
                        url,
                        sleep_time,
                    )

                    await sleep(sleep_time)
                    continue

                raise error

    def get(self, url: str | Route, /, **kwargs) -> JsonCoro:
        return self.request("get", url, **kwargs)

    def put(self, url: str | Route, /, **kwargs) -> JsonCoro:
        return self.request("put", url, **kwargs)

    def post(self, url: str | Route, /, **kwargs) -> JsonCoro:
        return self.request("post", url, **kwargs)

    def patch(self, url: str | Route, /, **kwargs) -> JsonCoro:
        return self.request("patch", url, **kwargs)

    def delete(self, url: str | Route, /, **kwargs) -> JsonCoro:
        return self.request("delete", url, **kwargs)
