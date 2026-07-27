from __future__ import annotations

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class DatabaseSettings(BaseSettings):
    """
    Database configuration.

    This module is responsible only for
    database connectivity and connection pool
    settings.
    """

    DATABASE_URL: str = Field(
        default="postgresql+psycopg://postgres:password@localhost:5432/resume_optimizer",
    )

    DATABASE_ECHO: bool = Field(
        default=False,
    )

    DATABASE_POOL_SIZE: int = Field(
        default=10,
        ge=1,
    )

    DATABASE_MAX_OVERFLOW: int = Field(
        default=20,
        ge=0,
    )

    DATABASE_POOL_TIMEOUT: int = Field(
        default=30,
        ge=1,
    )

    DATABASE_POOL_RECYCLE: int = Field(
        default=1800,
        ge=60,
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",
        case_sensitive=True,
        extra="ignore",
    )




