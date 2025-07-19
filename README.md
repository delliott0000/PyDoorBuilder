[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/imports-isort-ef8336.svg)](https://github.com/PyCQA/isort)

**Still in early development.**

# PyDoorBuilder
The goal of PyDoorBuilder is to automatically generate quotation documents, BOMs and DXFs for steel doors.

This project is split into a few different modules:

- [Client](https://github.com/delliott0000/PyDoorBuilder/tree/master/Client) - The front-end program that the user interacts with directly.
- [Server](https://github.com/delliott0000/PyDoorBuilder/tree/master/Server) - This module communicates user sessions and specification states with the client.
- [Autopilot](https://github.com/delliott0000/PyDoorBuilder/tree/master/Autopilot) - The server will offload certain tasks to the autopilot module, such as generating documents.
- [Common](https://github.com/delliott0000/PyDoorBuilder/tree/master/Common) - Models that are used across more than one module are defined here.

# Features (Planned)

- Built-in HTTP API that manages user sessions and enforces rate limits.
- Real-time communication of client states via WebSocket to prevent the loss of progress in the event of a crash.
- Use of the `asyncio` framework to handle many IO-bound tasks concurrently.
- Support for many autopilots running simultaneously.