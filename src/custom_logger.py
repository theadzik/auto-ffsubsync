import logging
import os
import sys


def get_logger(name: str) -> logging.Logger:
    """Create and configure a logger with a standard format."""

    logger = logging.getLogger(name)

    if not logger.hasHandlers():  # Prevents adding multiple handlers
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        log_level = logging.getLevelName(log_level)  # Convert string to log level

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level)
        handler.setFormatter(logging.Formatter(
            "%(levelname)s %(message)s"
        ))

        logger.setLevel(log_level)
        logger.addHandler(handler)
        logger.propagate = False  # Prevents duplicate logs if used in multiple modules

    return logger
