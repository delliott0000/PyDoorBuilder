# Introduction
This file documents shared behaviour and workflows that are used in our WebSocket subprotocol.

It is recommended to read through [HTTP](../HTTP) in its entirety first.

# Scope & Purpose
The subprotocol only defines application-level messages and behaviours. Transport-level semantics, such as connection liveliness and message size limits, are handled solely at the WebSocket layer and are not documented here.

Before we get into the details, a reminder of the purpose of this subprotocol:
- Send & receive `States` for syncing and store them for later recovery.
- Defer resource-intensive tasks, such as file generation, to another process.

# Close Codes
If and only if a sending peer sends a message that violates the subprotocol, then the receiving peer must immediately close the WebSocket connection with the appropriate custom WebSocket close code.
- **4001** - The message is not a text frame.
- **4002** - The message cannot be parsed into a valid JSON object.

These are not part of the subprotocol per se, but are still application-specific.
- **4000** - Sent by the server when the `Token` that was used to open the WebSocket connection has expired.

# Final Notes
...