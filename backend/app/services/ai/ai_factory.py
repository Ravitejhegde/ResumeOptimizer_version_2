from __future__ import annotations

from app.core.config import settings
from app.core.exceptions import ConfigurationError

from app.services.ai.ai_provider import (
    AIProvider,
)

from app.services.ai.gemini_provider import (
    GeminiProvider,
)

from app.services.ai.openrouter_provider import (
    OpenRouterProvider,
)


class AIFactory:
    """
    Creates AI provider instances.

    Supported providers:
        - gemini
        - openrouter

    The rest of the application does not
    know provider implementation details.
    """


    @staticmethod
    def create() -> AIProvider:

        provider = (
            settings.AI_PROVIDER
            .lower()
            .strip()
        )


        if provider == "gemini":

            return GeminiProvider()


        if provider == "openrouter":

            return OpenRouterProvider()


        raise ConfigurationError(
            f"Unsupported AI provider: {provider}"
        )