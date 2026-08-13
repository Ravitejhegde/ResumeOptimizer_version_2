"""
app.ai.services.ai_optimizer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Central AI optimization service.

All optimizer modules communicate with AI
through this service.
"""

from __future__ import annotations

from app.ai.models.ai_request import (
    AIRequest,
)
from app.ai.models.ai_response import (
    AIResponse,
)
from app.ai.provider.provider_factory import (
    ProviderFactory,
)


class AIOptimizer:
    """
    Executes AI optimization requests.
    """

    def __init__(self) -> None:

        self._client = (
            ProviderFactory.create()
        )

    def optimize(
        self,
        request: AIRequest,
    ) -> AIResponse:
        """
        Execute an AI optimization request.
        """

        response = AIResponse()

        try:

            prompt = request.prompt

            if request.system_prompt:

                prompt = (
                    request.system_prompt
                    + "\n\n"
                    + request.prompt
                )

            content = (
                self._client.generate(
                    prompt
                )
            )

            response.content = content

            response.success = True

            return response

        except Exception as exc:

            response.success = False

            response.error = str(exc)

            return response