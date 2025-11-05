from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

    from aiohttp import ClientResponse

    from .resource import Resource
    from .session import Session

    Json = dict[str, Any]

__all__ = (
    "HTTPException",
    "ValidationError",
    "ResourceConflict",
    "ResourceLocked",
    "SessionBound",
    "ResourceNotOwned",
)


class HTTPException(Exception):
    def __init__(self, response: ClientResponse, data: Json, /):
        super().__init__(f"{response.status} {response.reason}")
        self.response: ClientResponse = response
        self.data: Json = dict(data)


class ValidationError(Exception):
    def __init__(self, results: set[str], /):
        super().__init__("\n".join(results))
        self.results: set[str] = set(results)


class ResourceConflict(Exception):
    def __init__(self, session: Session, resource: Resource, *args: Any):
        super().__init__(*args)
        self.session: Session = session  # The *requesting* session
        self.resource: Resource = resource  # The *requested* resource


class ResourceLocked(ResourceConflict):
    def __init__(self, session: Session, resource: Resource, /):
        super().__init__(
            session, resource, "Requested resource is already locked by another session."
        )


class SessionBound(ResourceConflict):
    def __init__(self, session: Session, resource: Resource, /):
        super().__init__(
            session, resource, "Requesting session is already bound to a resource."
        )


class ResourceNotOwned(ResourceConflict):
    def __init__(self, session: Session, resource: Resource, /):
        super().__init__(
            session, resource, "Requesting session is not bound to the requested resource."
        )
