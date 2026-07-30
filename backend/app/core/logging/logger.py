"""
Centralized logging configuration for ResumeOptimizer.
"""

from __future__ import annotations

import logging
import sys
from logging import Logger


_DEFAULT_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
)

_DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def configure_logging(level: int = logging.INFO) -> None:
    """
    Configure the root logger.

    This function should be called once during application startup.
    """

    root_logger = logging.getLogger()

    if root_logger.handlers:
        return

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            fmt=_DEFAULT_FORMAT,
            datefmt=_DEFAULT_DATE_FORMAT,
        )
    )

    root_logger.setLevel(level)
    root_logger.addHandler(handler)


def get_logger(name: str) -> Logger:
    """
    Return a configured logger.
    """

    return logging.getLogger(name)