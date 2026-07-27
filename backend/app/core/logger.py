from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from app.core.config.settings import settings


LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(name)s | "
    "%(message)s"
)


def configure_logger() -> logging.Logger:
    """
    Configure application logger.
    """

    logger = logging.getLogger(
        settings.APP_NAME
    )

    if logger.handlers:
        return logger

    logger.setLevel(
        logging.DEBUG
        if settings.DEBUG
        else logging.INFO
    )

    formatter = logging.Formatter(
        LOG_FORMAT
    )

    # Console

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        console_handler
    )

    # File

    log_file = (
        settings.LOG_DIR
        / "resume_optimizer.log"
    )

    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )

    file_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        file_handler
    )

    logger.propagate = False

    return logger


logger = configure_logger()




