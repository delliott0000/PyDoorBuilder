from aiohttp import ClientWebSocketResponse as BasicClientWSResponse
from aiohttp import WSCloseCode
from aiohttp.web import WebSocketResponse as BasicWSResponse

__all__ = ("ClientWebSocketResponse", "WebSocketResponse")


class _WSResponseMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._sent_close_code = None

    @property
    def sent_close_code(self) -> int | None:
        return self._sent_close_code

    @property
    def recv_close_code(self) -> int | None:  # More explicit
        return self.close_code  # noqa

    async def close(self, *, code: int = WSCloseCode.OK, **kwargs) -> bool:
        result = await super().close(code=code, **kwargs)  # noqa
        if result is True:
            self._sent_close_code = code
        return result


class ClientWebSocketResponse(_WSResponseMixin, BasicClientWSResponse):
    pass


class WebSocketResponse(_WSResponseMixin, BasicWSResponse):
    pass
