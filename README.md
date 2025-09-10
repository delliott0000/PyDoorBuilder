[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/imports-isort-ef8336.svg)](https://github.com/PyCQA/isort)

**Still in early development.**

# PyDoorBuilder
PyDoorBuilder is a CPQ (Configure, Price, Quote) software solution originally designed for steel door configurations. However, it can be easily adapted to support a wide range of products across various industries.

This project is split into a few different modules:

- [Client](https://github.com/delliott0000/PyDoorBuilder/tree/master/Client) - The front-end program that the user interacts with directly.
- [Server](https://github.com/delliott0000/PyDoorBuilder/tree/master/Server) - This module communicates user sessions and specification states with the client.
- [Autopilot](https://github.com/delliott0000/PyDoorBuilder/tree/master/Autopilot) - The server will offload certain tasks to the autopilot module, such as generating documents.
- [Common](https://github.com/delliott0000/PyDoorBuilder/tree/master/Common) - Objects that are used across more than one module are defined here.

# Features
- Built-in HTTP API that manages user sessions and enforces rate limits.
- Real-time communication of client states via WebSocket to prevent the loss of progress in the event of a crash.
- Use of the `asyncio` framework to handle many IO-bound tasks concurrently.
- Support for many autopilots running simultaneously.