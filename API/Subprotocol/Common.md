# Introduction
This file documents shared behaviour and workflows that are used in the WebSocket subprotocol.

It is recommended to read through [HTTP](../HTTP) in its entirety first; this subfolder will reference some things that are defined there.

# Scope & Purpose
The subprotocol only defines application-level messages and behaviours. Transport semantics, such as connection liveliness and message size limits, are handled solely at the WebSocket level and are not documented here.

Before we get into the details, a reminder of the purpose of this subprotocol:
- Send & receive `States` for syncing and store them for later recovery.
- Defer resource-intensive tasks, such as file generation, to an `Autopilot`.

# Message Flow
Each message must be an `Event` or an `Ack`. An `Event` contains information. An `Ack` simply acknowledges an `Event`.

The following rules define the `Event`/`Ack` message flow:
- Each `Event` must be assigned a Universally Unique Identifier (UUID).
- Each `Event` must be acknowledged exactly once, within the time limit negotiated during the [handshake phase](Common.md#connection-phases).
- Each `Ack` must reference an `Event` by specifying the UUID of that `Event`.
- Each `Ack` must reference an `Event` that exists and has not already been acknowledged.
- `Events` and `Acks` may be sent & received out of order.

Please note that whilst UUIDs should ideally be unique within the scope of the WebSocket connection, this is not strictly required in practice. An implementation may discard an outgoing `Event` and its UUID as soon as it has been acknowledged - this is actually recommended to reduce the memory usage of a long-lasting or high-throughput connection. Therefore, a sending peer is only required to ensure UUID uniqueness within its current set of unacknowledged outgoing `Events`.

# Message Structure
Each message must be a text frame that can be parsed into a valid JSON object.

...

...
```py
{
    "type": "event",  # By definition
    "id": str,  # UUID
    "sent_at": str  # ISO 8601
}
```

...
```py
{
    "type": "ack",  # By definition
    "id": str,  # UUID of an Event
    "sent_at": str  # ISO 8601
}
```

# Connection Phases
Each connection is divided into two application-level phases; the handshake phase and the messaging phase.

...

# Close Codes
If and only if a peer violates the subprotocol, then the other peer must immediately close the WebSocket connection with the appropriate custom WebSocket close code.

Close codes and their corresponding failure scenarios:
- **4001** - A message is not a text frame.
- **4002** - A message cannot be parsed into a valid JSON object.

Not part of the subprotocol per se, but still application-specific:
- **4000** - Sent by the server when the `Token` that was used to open the WebSocket connection is no longer valid.

# Final Notes
...