# Auth Endpoints
This file documents endpoints related to authentication.

Each section will include the following:
- A brief description of the endpoint.
- The JSON object that the client application should supply with the request. If this is omitted, then the API does not expect a JSON object to be supplied. Unexpected JSON objects/fields will be ignored and will not cause an error to be returned.
- The JSON object that the API will return if the request is successful.
- Possible HTTP error codes specific to the endpoint, listed in descending order of precedence.
- Any additional information, such as whether the endpoint is restricted to a certain type of `User`.

If you haven't done so already, please read [Common.md](https://github.com/delliott0000/PyDoorBuilder/tree/master/API/HTTP/Common.md) first.

# POST /auth/login
Exchange a username and password for a `Token`. If a valid `session_id` is supplied, then the API will retrieve that `Session`. Otherwise, it will open a new `Session`.

Supplied by the client application:
```py
{
    "username": str,
    "password": str
    "session_id": str  # Optional
}
```

Returned by the API:
```py
{
    "token": Token
}
```

- If the username/password is missing or of the wrong type, the API will return `400 Bad Request`.
- If the username/password is incorrect, the API will return `401 Unauthorized`.

# POST /auth/refresh
Renew a `Token` by supplying the refresh key, extending the duration that it is valid for.

Supplied by the client application:
```py
{
    "refresh": str
}
```

Returned by the API:
```py
{
    "token": Token
}
```

- If the refresh key is missing or of the wrong type, the API will return `400 Bad Request`.
- If the refresh key is incorrect, the API will return `401 Unauthorized`.

# POST /auth/logout
Invalidate a `Token`, preventing it from being used for any subsequent requests, including renewals.

Returned by the API:
```py
{
    "token": Token
}
```