"""
Email configuration.
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class EmailSettings(BaseSettings):
    """
    Email delivery configuration.

    Responsible only for email-related settings.
    """

    ENABLE_EMAIL: bool = Field(
        default=False,
    )

    SMTP_HOST: str = Field(
        default="",
    )

    SMTP_PORT: int = Field(
        default=587,
        ge=1,
        le=65535,
    )

    SMTP_USERNAME: str = Field(
        default="",
    )

    SMTP_PASSWORD: str = Field(
        default="",
    )

    EMAIL_FROM: str = Field(
        default="",
    )

    EMAIL_FROM_NAME: str = Field(
        default="ResumeOptimizer",
    )

    EMAIL_VERIFICATION_EXPIRE_HOURS: int = Field(
        default=24,
        ge=1,
    )

    FRONTEND_URL: str = Field(
        default="http://localhost:5173",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",
        case_sensitive=True,
        extra="ignore",
    )