from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING
from urllib.parse import quote

from .config import global_config

if TYPE_CHECKING:
    from typing import ClassVar

__all__ = ("Route", "HTTPRoute", "WebSocketRoute")


domain = global_config["api"]["domain"]
secure = global_config["api"]["secure"]
local = global_config["api"]["local"]

use_secure = secure and not local

if local:
    host = global_config["server"]["api"]["host"]
    port = global_config["server"]["api"]["port"]
    resolved_domain = f"{host}:{port}"
else:
    resolved_domain = domain


class Route(ABC):
    BASE: ClassVar[str] = ""

    def __init__(self, path: str, /, **kwargs: str):
        if self.BASE == "":
            raise ValueError("Route must have a base.")

        self.__path: str = path
        self.__kwargs: dict[str, str] = {k: quote(v, safe="") for k, v in kwargs.items()}

    def __str__(self):
        return self.url

    @property
    def url(self) -> str:
        return self.BASE + self.__path.format(**self.__kwargs)


class HTTPRoute(Route):
    BASE: ClassVar[str] = f"http{'s' if use_secure else ''}://{resolved_domain}"


class WebSocketRoute(Route):
    BASE: ClassVar[str] = f"ws{'s' if use_secure else ''}://{resolved_domain}"
