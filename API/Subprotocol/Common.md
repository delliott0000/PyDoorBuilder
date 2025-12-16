# Introduction
This file documents shared behaviour and workflows that are used in our WebSocket subprotocol.

It is recommended to read through [HTTP](../HTTP) in its entirety first.

# Scope & Purpose
The subprotocol only defines application-level messages and behaviours. Transport-level semantics, such as connection liveliness and message size limits, are handled solely at the WebSocket layer and are not documented here.

Before we get into the details, a reminder of the purpose of this subprotocol:
- Send & receive `States` for syncing and store them for later recovery.
- Defer resource-intensive tasks, such as file generation, to another process.

# Message Flow
Each message must be an `Event` or an `Ack` (acknowledgement).

The following rules define the `Event`/`Ack` message flow:
- Each `Event` must be acknowledged exactly once and within an agreed-upon time limit.
- Each `Ack` must reference an `Event` that exists and has not already been acknowledged.
- An `Ack` must not be acknowledged.

# Message Structure
Each message must be "JSON-like". That is to say that it must be a text frame that can be parsed into a valid JSON object.

# Close Codes
If and only if a sending peer sends a message that violates the subprotocol, then the receiving peer must immediately close the WebSocket connection with the appropriate custom WebSocket close code.

Close codes and their corresponding failure scenarios:
- **4001** - The message is not a text frame.
- **4002** - The message cannot be parsed into a valid JSON object.

Not part of the subprotocol per se, but still application-specific:
- **4000** - Sent by the server when the `Token` that was used to open the WebSocket connection is no longer valid.

# Final Notes
...