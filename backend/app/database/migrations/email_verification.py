"""
Email verification database migration.
"""

from __future__ import annotations

from sqlalchemy import inspect

from app.database.engine import engine
from app.database.base import Base

# Make sure the model is registered.
from app.database.models.email_verification_token import (
    EmailVerificationToken,
)


def ensure_email_verification_table() -> None:
    """
    Create the email verification token table if it does not exist.

    This migration is intentionally limited to the
    email verification table.
    """

    inspector = inspect(engine)

    if (
        "email_verification_tokens"
        in inspector.get_table_names()
    ):
        return

    EmailVerificationToken.__table__.create(
        bind=engine,
        checkfirst=True,
    )