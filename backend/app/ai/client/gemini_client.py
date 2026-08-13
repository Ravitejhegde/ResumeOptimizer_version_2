"""
app.ai.client.gemini_client
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Google Gemini implementation of AIClient.
"""

from __future__ import annotations

from app.ai.client.ai_client import (
    AIClient,
)


class GeminiClient(AIClient):
    """
    Gemini implementation.

    This provider will be implemented later.
    """

    def generate(
        self,
        prompt: str,
    ) -> str:
        raise NotImplementedError(
            "GeminiClient is not implemented yet."
        )