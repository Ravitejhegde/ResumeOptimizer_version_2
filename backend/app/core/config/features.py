from __future__ import annotations

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class FeatureSettings(BaseSettings):
    """
    Feature flags.
    """

    ENABLE_AI: bool = Field(
        default=True,
    )

    ENABLE_ANALYSIS: bool = Field(
        default=True,
    )

    ENABLE_OPTIMIZATION: bool = Field(
        default=True,
    )

    ENABLE_BILLING: bool = Field(
        default=False,
    )

    ENABLE_AUTHENTICATION: bool = Field(
        default=False,
    )

    ENABLE_EMAIL: bool = Field(
        default=False,
    )

    ENABLE_ANALYTICS: bool = Field(
        default=False,
    )

    ENABLE_REPORTS: bool = Field(
        default=True,
    )

    ENABLE_RATE_LIMITING: bool = Field(
        default=False,
    )

    ENABLE_DEBUG_ENDPOINTS: bool = Field(
        default=False,
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )




