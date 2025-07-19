from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Coroutine
    from typing import Any

    ConfigData = dict[str, Any]

    ResponseData = dict[str, Any]
    RDCoro = Coroutine[Any, Any, ResponseData]
