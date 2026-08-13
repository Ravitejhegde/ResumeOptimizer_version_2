"""
app.ai.client.openai_client
~~~~~~~~~~~~~~~~~~~~~~~~~~~

OpenAI implementation of AIClient.
"""

from __future__ import annotations

from app.ai.client.ai_client import (
    AIClient,
)


class OpenAIClient(AIClient):
    """
    OpenAI implementation.

    Placeholder implementation.
    """

    def generate(
        self,
        prompt: str,
    ) -> str:
        raise NotImplementedError(
            "OpenAIClient is not implemented yet."
        )