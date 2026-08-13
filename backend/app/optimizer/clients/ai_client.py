"""
app.optimizer.clients.ai_client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Optimizer AI client.

Acts as a thin adapter over the
shared AI provider infrastructure.
"""

from __future__ import annotations

from app.ai.provider.provider_factory import (
    ProviderFactory,
)


class AIClient:
    """
    Optimizer AI adapter.
    """

    def __init__(
        self,
    ) -> None:

        self._provider = (
            ProviderFactory.create()
        )

    def optimize(
        self,
        prompt: str,
    ) -> str:
        """
        Send prompt to the configured AI provider.
        """

        return self._provider.generate(
            prompt
        )