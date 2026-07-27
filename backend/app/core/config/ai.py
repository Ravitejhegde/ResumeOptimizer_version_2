from __future__ import annotations

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class AISettings(BaseSettings):
    """
    AI provider configuration.
    """

    AI_PROVIDER: str = Field(
        default="openrouter",
    )

    OPENROUTER_API_KEY: str = Field(
        default="",
    )

    OPENROUTER_MODEL: str = Field(
        default="deepseek/deepseek-chat-v3-0324",
    )

    OPENAI_API_KEY: str = Field(
        default="",
    )

    OPENAI_MODEL: str = Field(
        default="gpt-5.5",
    )

    GEMINI_API_KEY: str = Field(
        default="",
    )

    GEMINI_MODEL: str = Field(
        default="gemini-2.5-flash-lite",
    )

    CLAUDE_API_KEY: str = Field(
        default="",
    )

    CLAUDE_MODEL: str = Field(
        default="claude-sonnet-4",
    )

    AI_TIMEOUT: int = Field(
        default=120,
        ge=1,
    )

    AI_MAX_RETRIES: int = Field(
        default=3,
        ge=0,
    )

    AI_MAX_TOKENS: int = Field(
        default=4096,
        ge=512,
    )

    AI_TEMPERATURE: float = Field(
        default=0.3,
        ge=0.0,
        le=2.0,
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )




