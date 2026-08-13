"""
app.ai.provider.provider_factory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Factory for selecting the configured AI provider.
"""

from __future__ import annotations

from app.ai.client.ai_client import (
    AIClient,
)
from app.ai.client.claude_client import (
    ClaudeClient,
)
from app.ai.client.gemini_client import (
    GeminiClient,
)
from app.ai.client.openai_client import (
    OpenAIClient,
)
from app.ai.client.openrouter_client import (
    OpenRouterClient,
)
from app.core.config.settings import (
    settings,
)


class ProviderFactory:
    """
    Creates the configured AI provider.
    """

    @staticmethod
    def create() -> AIClient:
        """
        Return the configured AI client.
        """

        provider = (
            settings.AI_PROVIDER
            .strip()
            .casefold()
        )

        match provider:

            case "openrouter":
                return OpenRouterClient()

            case "gemini":
                return GeminiClient()

            case "openai":
                return OpenAIClient()

            case "claude":
                return ClaudeClient()

            case _:
                raise ValueError(
                    f"Unsupported AI provider: {provider}"
                )