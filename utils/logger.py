import sys
import logging
from logging import Logger


def get_logger(name: str) -> Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # if not any(isinstance(h, logging.FileHandler) for h in logger.handlers):
    #     file_handler = logging.FileHandler("reb_log.log")
    #     file_handler.setLevel(logging.INFO)
    #     formatter = logging.Formatter(
    #         fmt="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    #     )
    #     file_handler.setFormatter(formatter)
    #     logger.addHandler(file_handler)

    # Create a stream handler to log to stdout
    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
        )
        stream_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)

    return logger
