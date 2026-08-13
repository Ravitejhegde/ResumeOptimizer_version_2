"""
app.ai.client.ai_client
~~~~~~~~~~~~~~~~~~~~~~~

Base interface for all AI providers.

Every AI provider (OpenRouter, Gemini, OpenAI, Claude)
must implement this interface.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class AIClient(ABC):
    """
    Abstract AI client.

    Defines the contract that every AI provider
    must implement.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate a response from the AI model.

        Args:
            prompt:
                Prompt sent to the language model.

        Returns:
            Generated text.

        Raises:
            RuntimeError:
                If generation fails.
        """
        raise NotImplementedError