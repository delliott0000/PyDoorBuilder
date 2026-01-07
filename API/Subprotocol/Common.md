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

Please note that while UUIDs should ideally be unique within the scope of the WebSocket connection, this is not strictly required in practice. An implementation may discard an outgoing `Event` and its UUID as soon as it has been acknowledged - this is actually recommended to reduce the memory usage of a long-lasting or high-throughput connection. Therefore, a sending peer is only required to ensure UUID uniqueness within its current set of unacknowledged outgoing `Events`.  Peers may generate UUIDs using any method they choose.

# Message Structure
Each message must be a text frame that can be parsed into a valid JSON object.

Below is a list of top-level fields and their corresponding types and enumerations for each message type.

Each field is mandatory unless `None` is listed as an allowed type, in which case that field is optional. Omitting an optional field should be interpreted in the same way as an explicit `None` for that field.

`Event` fields:
```py
{
    "type": "event",  # By definition; Enum ["event"]
    "id": str,  # UUID
    "sent_at": str,  # ISO 8601
    "status": str,  # Enum ["ok", "error", "fatal"]
    "reason": str | None,  # For human-readable logging and traceback
    "payload": dict[str, Any]  # Required, but may be empty
}
```

`Ack` fields:
```py
{
    "type": "ack",  # By definition; Enum ["ack"]
    "id": str,  # UUID of an Event
    "sent_at": str  # ISO 8601
}
```

...

It *is* a violation of the subprotocol to:
- Miss a mandatory top-level field.
- Supply a value of an incorrect type.
- Supply a value that is not a member of the field's designated enumeration.
- Send an `Event` with `"status": "fatal"`.

It *is not* a violation of the subprotocol to:
- Supply an undocumented top-level field. The receiving peer can safely ignore this.
- Send bad payload-level data. The receiving peer can handle this by sending back an `Event` with `"status": "error"` or `"status": "fatal"`.

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