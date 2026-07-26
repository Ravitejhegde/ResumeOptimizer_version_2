from __future__ import annotations

from app.services.ai.ai_provider import (
    AIProvider,
)

from app.services.ai.rewrite.rewrite_models import (
    RewriteRequest,
    RewriteResult,
)
from app.services.ai.rewrite.prompt_builder import (
    PromptBuilder,
)

class RewriteService:
    """
    Coordinates AI-powered paragraph rewriting.

    Responsibilities
    ----------------
    - Build prompt
    - Send request to AI provider
    - Validate AI response
    - Return RewriteResult

    Never knows about Gemini/OpenRouter internals.
    """

    def __init__(
        self,
        provider: AIProvider,
    ) -> None:

        self._provider = provider

    def rewrite(
    self,
    request: RewriteRequest,
) -> RewriteResult:

        prompt = PromptBuilder.build(
    request
)

        response = self._provider.generate(
    prompt
)

        response = response.strip()

        if not response:

            return RewriteResult(
                optimized_text=request.paragraph,
                success=False,
                provider=self._provider.__class__.__name__,
            )

        return RewriteResult(
            optimized_text=response,
            success=True,
            provider=self._provider.__class__.__name__,
        )