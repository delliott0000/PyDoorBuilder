from __future__ import annotations

from asyncio import gather
from datetime import timedelta
from typing import TYPE_CHECKING

from aiohttp.web import HTTPConflict, HTTPForbidden, HTTPNotFound, json_response

from Common import (
    PermissionType,
    ResourceConflict,
    ResourceJSONVersion,
    ResourceLocked,
    ResourceNotOwned,
    Session,
    SessionBound,
    log,
)

from .base_service import BaseService
from .decorators import BucketType, ratelimit, route, user_only, validate_access
from .resource_types import QuoteResource

if TYPE_CHECKING:
    from typing import Any

    from aiohttp.web import Request, Response

    from Common import Resource, User

__all__ = ("ResourceService",)


class ResourceService(BaseService):
    @property
    def map(self) -> dict[str, Any]:
        # Confirm the structure for later
        return {
            "quote": {
                "class": QuoteResource,
                "executors": {
                    "...": {
                        "func": ...,
                        "query": ...,
                        "check": ...,
                        "exception": ...,
                    }
                },
            }
        }

    def ok_response(
        self,
        resource: Resource,
        /,
        *,
        version: ResourceJSONVersion = ResourceJSONVersion.metadata,
    ) -> Response:
        return json_response(
            {
                "message": "Ok",
                "resource": resource.to_json(version=version),
            },
            status=200,
        )

    def convert_conflict(
        self, error: ResourceConflict, data: dict[str, Any], /
    ) -> HTTPConflict:
        return self.attach_extra_data(HTTPConflict(reason=str(error).strip(".")), data)

    def permission_check(
        self, user: User, resource: Resource, permission_type: PermissionType, /
    ) -> None:
        if not user.has_permission_for(permission_type, resource):
            raise self.attach_extra_data(
                HTTPForbidden(reason="Missing required permission"),
                {"permission": permission_type.value},
            )

    def acquisition_check(self, session: Session, resource: Resource, /) -> None:
        try:
            resource.ensure_acquired(session)
        except ResourceNotOwned as error:
            raise self.convert_conflict(error, {"session": session.to_json()})

    async def run_executor(
        self, rid: str, key: str, executor: dict[str, Any], /
    ) -> tuple[str, Any]:
        func = executor["func"]
        query = executor["query"]
        check = executor["check"]
        exception = executor["exception"]

        args = query, rid
        result = await func(*args)

        if not check(result):
            raise exception

        return key, result

    async def load_resource(self, request: Request, /) -> Resource:
        rtype = request.match_info["rtype"]
        rid = request.match_info["rid"]
        cache_key = rtype, rid

        cached = self.server.rtype_rid_to_resource.get(cache_key)
        if cached is not None:
            return cached

        try:
            loader = self.map[rtype]
        except KeyError:
            raise HTTPNotFound(reason="Unknown resource type")

        class_ = loader["class"]
        executors = loader["executors"]

        tasks = (self.run_executor(rid, key, executor) for key, executor in executors.items())
        results = await gather(*tasks)
        data = {key: result for key, result in results}

        resource = class_.new(data)
        self.server.rtype_rid_to_resource[cache_key] = resource

        log(f"Resource {resource} loaded.")

        return resource

    async def task_coro(self) -> None:
        rtype_rid_to_resource = self.server.rtype_rid_to_resource
        grace = timedelta(seconds=self.server.config.resource_grace)

        for key in list(rtype_rid_to_resource):
            try:
                resource = rtype_rid_to_resource[key]
            except KeyError:
                continue

            if resource.is_idle(grace):
                rtype_rid_to_resource.pop(key, None)

                last_active = resource.last_active.strftime("%Y-%m-%d %H:%M:%S")
                log(f"Resource {resource} unloaded. Last active at {last_active}.")

    @route("post", "/resource/{rtype}/{rid}/acquire")
    @ratelimit(limit=10, interval=60, bucket_type=BucketType.User)
    @user_only
    @validate_access
    async def acquire(self, request: Request, /) -> Response:
        resource = await self.load_resource(request)
        session = self.session_from_request(request)

        self.permission_check(session.user, resource, PermissionType.acquire)
        # No acquisition check necessary

        try:
            session.acquire_resource(resource)
        except ResourceLocked as error:
            raise self.convert_conflict(error, {"locked_by": str(resource.user)})
        except SessionBound as error:
            raise self.convert_conflict(error, {"session": session.to_json()})

        return self.ok_response(resource)

    @route("post", "/resource/{rtype}/{rid}/release")
    @ratelimit(limit=10, interval=60, bucket_type=BucketType.User)
    @user_only
    @validate_access
    async def release(self, request: Request, /) -> Response:
        resource = await self.load_resource(request)
        session = self.session_from_request(request)

        # No permission check necessary
        # No acquisition check necessary

        try:
            resource.release(session)
        except ResourceNotOwned as error:
            raise self.convert_conflict(error, {"session": session.to_json()})

        return self.ok_response(resource)

    @route("get", "/resource/{rtype}/{rid}/preview")
    @ratelimit(limit=10, interval=60, bucket_type=BucketType.User)
    @user_only
    @validate_access
    async def preview(self, request: Request, /) -> Response:
        resource = await self.load_resource(request)
        session = self.session_from_request(request)

        self.permission_check(session.user, resource, PermissionType.preview)
        self.acquisition_check(session, resource)

        return self.ok_response(resource, version=ResourceJSONVersion.preview)

    @route("get", "/resource/{rtype}/{rid}/view")
    @ratelimit(limit=10, interval=60, bucket_type=BucketType.User)
    @user_only
    @validate_access
    async def view(self, request: Request, /) -> Response:
        resource = await self.load_resource(request)
        session = self.session_from_request(request)

        self.permission_check(session.user, resource, PermissionType.view)
        self.acquisition_check(session, resource)

        return self.ok_response(resource, version=ResourceJSONVersion.view)
