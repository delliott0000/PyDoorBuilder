from Common import Quote, ResourceABC, ResourceMixin

__all__ = ("QuoteResource",)


class QuoteResource(ResourceMixin, Quote, ResourceABC):
    __slots__ = ("_session", "_last_active")
