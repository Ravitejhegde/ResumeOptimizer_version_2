"""
app.ai.client.claude_client
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Claude implementation of AIClient.
"""

from __future__ import annotations

from app.ai.client.ai_client import (
    AIClient,
)


class ClaudeClient(AIClient):
    """
    Claude implementation.

    Placeholder implementation.
    """

    def generate(
        self,
        prompt: str,
    ) -> str:
        raise NotImplementedError(
            "ClaudeClient is not implemented yet."
        )