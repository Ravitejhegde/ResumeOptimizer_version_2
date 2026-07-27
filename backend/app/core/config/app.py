from __future__ import annotations

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class AppSettings(BaseSettings):
    """
    Application configuration.

    This module contains only application-level
    configuration and must never contain settings
    related to AI, database, storage, billing,
    or security.
    """

    APP_NAME: str = Field(
        default="ResumeOptimizer API",
    )

    APP_VERSION: str = Field(
        default="2.0.0",
    )

    APP_DESCRIPTION: str = Field(
        default="AI-powered Resume Optimization Platform",
    )

    APP_ENV: str = Field(
        default="development",
    )

    DEBUG: bool = Field(
        default=True,
    )

    API_PREFIX: str = Field(
        default="/api",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",
        case_sensitive=True,
        extra="ignore",
    )




