from __future__ import annotations

from abc import ABC, abstractmethod


class AIProvider(ABC):
    """
    Base interface for AI providers.

    Implementations:

        OpenRouterProvider
        GeminiProvider
        Other LLM providers


    Responsibilities:

        - Define provider contract.

    Does NOT:

        - Build prompts.
        - Parse responses.
        - Validate AI output.
    """



    @abstractmethod
    async def generate(
        self,
        messages: list[dict[str, str]],
    ) -> str:
        """
        Send messages to AI provider.

        Returns:
            Raw AI response.
        """

        raise NotImplementedError



    @abstractmethod
    def name(
        self,
    ) -> str:
        """
        Provider name.
        """

        raise NotImplementedError