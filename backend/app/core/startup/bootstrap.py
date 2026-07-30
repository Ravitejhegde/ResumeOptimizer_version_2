"""
Application startup bootstrap.
"""

from __future__ import annotations

from app.core.config import settings
from app.core.logging import configure_logging, get_logger

logger = get_logger(__name__)


def bootstrap() -> None:
    """
    Initialize the application.

    This function should be called exactly once during FastAPI startup.
    """

    # Configure logging
    configure_logging()

    logger.info("Starting ResumeOptimizer...")

    # Create required directories
    settings.create_directories()

    logger.info("Required directories verified.")

    logger.info("Core bootstrap completed successfully.")