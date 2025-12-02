# Introduction
This file documents shared behaviour and definitions that are used across all HTTP endpoints. For more information on specific endpoints, please see [Contents](https://github.com/delliott0000/PyDoorBuilder/tree/master/API/HTTP/Contents).

Before we can jump straight in, we must first define a few things, and consider our end goals for the API.

# Definitions
- **Client** - A normal, "human" client application.
- **Autopilot** - An automated, headless client application.
- **User** - `Client`s and `Autopilot`s are collectively referred to as `User`s.
- **Instance** - A running copy of the program that a `User` is using to interact with the API.
- **Resource** - An abstract entity that `Client`s can acquire, release, read from, and write to.
- **Session** - A temporary context that keeps track of `User` activity, independent of authentication.
- **State** - A container for a `Session`'s real-time snapshot. Only applicable to `Client`s.

# Considerations
- `Client`s can have many ongoing `Session`s.
- `Client`s can recover previous `Session`s by supplying the `Session`'s ID.
- Similarly, two or more `Instance`s that belong to the same `Client` account, may share the same `Session`. In this case, their `State`s are automatically synced together.
- Each `Session` can acquire up to one `Resource` at a time; each `Resource` can be acquired by up to one `Session` at a time. These restrictions prevent race conditions, since a `Session` must acquire a `Resource` before modifying it.

# Models
With all of this in mind, we will organise the functionality of the server into the following models. Each bullet point includes a JSON-like representation of the model that it describes. Fields marked `ISO 8601` follow the format `%Y-%m-%dT%H:%M:%S.%f%z`.
- **User** - See Definitions.
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
- **State** - See Definitions. This is stored by the server mainly to prevent loss of progress.
```py
# TODO: Define fields and types.
```
- **Resource** - See Definitions. Different `Resource` types will implement their own fields.
```py
{
    "id": int,
    "owner": User
}
# All resources must include these fields as a bare minimum.
```
- **Session** - See Definitions. Each `Session` is associated with a `User` (many-to-one) and a `State` (one-to-one).
```py
{
    "id": str,
    "user": User,
    "state": State,
    "resource": Resource | None
}
```
- **Token** - An authentication context. `User`s exchange their username and password for a `Token`. Each `Token` is associated with a `Session` (many-to-one).
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