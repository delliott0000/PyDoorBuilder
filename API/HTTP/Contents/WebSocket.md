# Resource Endpoints
This file documents the group of endpoints related to WebSockets.

If you haven't already, please read [Common.md](../Common.md) first.

Please see the documentation for our [WebSocket subprotocol](../../Subprotocol) after finishing this page.

## Group-Level Rules
- If the supplied `Token` already has a WebSocket connection open, the API will return `409 Conflict`.

## GET /ws/user
Open a WebSocket connection with the server as a `Client`. `State` updates will take place over this connection.

The API will return `101 Switching Protocols`.

This endpoint is `Client-only`.

## GET /ws/autopilot
Open a WebSocket connection with the server as an `Autopilot`. Task-related communications will take place over this connection.

The API will return `101 Switching Protocols`.

This endpoint is `Autopilot-only`.