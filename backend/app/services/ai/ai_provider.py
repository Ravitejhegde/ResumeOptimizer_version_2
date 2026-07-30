from __future__ import annotations

from abc import ABC, abstractmethod


class AIProvider(ABC):
    """
    Base interface for all AI providers.

    Responsibilities:
        - Send prompts to LLM.
        - Return raw generated response.

    Does not:
        - Build prompts.
        - Parse responses.
        - Validate resume content.
    """


    @abstractmethod
    async def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Send prompt to AI model.

        Returns:
            Raw model response.
        """

        raise NotImplementedError


    @abstractmethod
    def name(
        self,
    ) -> str:
        """
        Human readable provider name.
        """

        raise NotImplementedError