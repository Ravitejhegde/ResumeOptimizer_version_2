from __future__ import annotations

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class SecuritySettings(BaseSettings):
    """
    Security configuration.

    Responsible only for application
    security settings.
    """

    SECRET_KEY: str = Field(
        default="CHANGE_ME_IN_PRODUCTION",
    )

    ALGORITHM: str = Field(
        default="HS256",
    )

    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=60,
        ge=1,
    )

    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=30,
        ge=1,
    )

    PASSWORD_MIN_LENGTH: int = Field(
        default=8,
        ge=6,
    )

    ENABLE_CORS: bool = Field(
        default=True,
    )

    ALLOWED_ORIGINS: tuple[str, ...] = Field(
        default=(
            "http://localhost:5173",
        ),
    )

    ENABLE_RATE_LIMITING: bool = Field(
        default=False,
    )

    API_KEY_HEADER: str = Field(
        default="X-API-Key",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",
        case_sensitive=True,
        extra="ignore",
    )




