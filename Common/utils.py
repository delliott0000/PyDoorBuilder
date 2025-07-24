import datetime
import logging
import os
import pathlib

__all__ = ("now", "setup_logging")


def now() -> datetime.datetime:
    return datetime.datetime.now().astimezone()


def setup_logging(file: str, level: int = logging.DEBUG, /) -> None:
    current_module = pathlib.Path(file).parent
    log_destination = current_module.parent / "Logs" / current_module.name

    timestamp = now().strftime("%Y-%m-%d_%H-%M-%S")

    os.makedirs(log_destination, exist_ok=True)

    logging.basicConfig(
        filename=log_destination / f"{timestamp}.txt",
        filemode="w",
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
