# Introduction
This file documents shared behaviour and definitions that are used across all HTTP endpoints.

Before we can jump straight in, we must first define a few things, and consider our end goals for the API.

# Definitions
- **Client** - A normal, "human" client application.
- **Autopilot** - An automated, headless client application.
- **User** - `Clients` and `Autopilots` are collectively referred to as `Users`.
- **Instance** - A running copy of the program that a `User` is using to interact with the API.
- **Session** - A temporary context that keeps track of `User` activity, independent of authentication.
- **Resource** - An abstract entity that `Sessions` can acquire, release, read from, and write to.
- **State** - A container for a `Session's` real-time snapshot.

# Considerations
- `Users` can have many ongoing `Sessions`.
- `Users` can recover previous `Sessions` by supplying the `Session's` ID.
- Therefore, two or more `Instances` that belong to the same `User` account, may share the same `Session`. In this case, their `States` are automatically synced together.
- Each `Session` can acquire up to one `Resource` at a time; each `Resource` can be acquired by up to one `Session` at a time. These restrictions prevent race conditions, since a `Session` must acquire a `Resource` before modifying it.
- `Sessions` owned by an `Autopilot` can not maintain a non-empty `State` or acquire a `Resource`.

# Models
With all of this in mind, we will organise the functionality of the server into the following models. Each bullet point includes a JSON-like representation of the model that it describes. Fields marked `ISO 8601` follow the format `%Y-%m-%dT%H:%M:%S.%f%z`.
- **User** - See [Definitions](https://github.com/delliott0000/PyDoorBuilder/blob/master/API/HTTP/Common.md#definitions).
```py
{
    "id": int,
    "username": str,
    "display_name": str | None,
    "email": str | None,
    "autopilot": bool,
    "admin": bool
}
# Omitted the "teams" field; this is not relevant here.
```
- **State** - See [Definitions](https://github.com/delliott0000/PyDoorBuilder/blob/master/API/HTTP/Common.md#definitions). This is stored by the server mainly to prevent loss of progress.
```py
{
}
# TODO: Define fields and types.
```
- **Resource** - See [Definitions](https://github.com/delliott0000/PyDoorBuilder/blob/master/API/HTTP/Common.md#definitions). Different `Resource` types will implement their own fields.
```py
{
    "id": int,
    "owner": User
}
# All resources must include these fields as a bare minimum.
```
- **Session** - See [Definitions](https://github.com/delliott0000/PyDoorBuilder/blob/master/API/HTTP/Common.md#definitions). Each `Session` is associated with a `User` (many-to-one) and a `State` (one-to-one).
```py
{
    "id": str,
    "user": User,
    "state": State,
    "resource": Resource | None
}
```
- **Token** - An authentication context. `Users` exchange their username and password for a `Token`. Each `Token` is associated with a `Session` (many-to-one).
```py
{
    "access": str,
    "refresh": str,
    "access_expires": str,  # ISO 8601
    "refresh_expires": str,  # ISO 8601
    "killed_at": str | None,  # ISO 8601 or None
    "session": Session
}
```

# Common Endpoint Behaviour
Unless stated otherwise, every endpoint exposed by the API follows the below rules. They are listed in descending order of precedence.

## Response Structure
The API will return a JSON object with every response.

For unsuccessful requests, this object will contain a `"message": ...` field describing what went wrong.

For successful requests, this object will contain `"message": "OK"` along with the relevant information.

## Authentication
Except for `/auth/login` and `/auth/refresh`, every endpoint requires an `"Authorization": "Bearer ..."` header, where `...` is a `Token` access key.

If the `Authorization` header is missing, of the wrong type, or can not be parsed, the API will return `400 Bad Request`.

If the `Authorization` header is incorrect, the API will return `401 Unauthorized`.

## Client/Autopilot/Admin-Only
Endpoints can be `Client-only`, `Autopilot-only` or `Admin-only`. An `Admin` is simply a `User` with elevated permissions.

If a `User` sends a request to one of these endpoints and does not meet the required criteria, the API will return `403 Forbidden`.

## Ratelimits
Every endpoint is rate limited. Ratelimits can be applied per endpoint, per `Token`, per `User` or per IP address. Exact ratelimits are not published in this documentation.

If a request is rate limited, the API will return `429 Too Many Requests`.

## Success
If a request is considered successful, the API will return `200 OK`.

# Final Notes
Please see [Contents](https://github.com/delliott0000/PyDoorBuilder/tree/master/API/HTTP/Contents) for more details on individual endpoints. Endpoints are organised into groups based on their functionality. For instance, endpoints related to authentication can be found in [Contents/Auth.md](https://github.com/delliott0000/PyDoorBuilder/tree/master/API/HTTP/Contents/Auth.md).