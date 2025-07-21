import datetime
import logging
import os
import pathlib

__all__ = ("setup_logging",)


def setup_logging(file: str, /):
    current_module = pathlib.Path(file).parent
    log_destination = current_module.parent / "Logs" / current_module.name

    timestamp = datetime.datetime.now().astimezone().strftime("%Y-%m-%d_%H-%M-%S")

    os.makedirs(log_destination, exist_ok=True)

    logging.basicConfig(
        filename=log_destination / f"{timestamp}.txt",
        filemode="w",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
