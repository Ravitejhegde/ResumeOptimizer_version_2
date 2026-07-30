from __future__ import annotations

import logging

from app.services.ai.ai_provider import (
    AIProvider,
)

from app.services.ai.rewrite.prompt_builder import (
    PromptBuilder,
)

from app.services.ai.rewrite.rewrite_models import (
    RewriteRequest,
    RewriteResult,
)


logger = logging.getLogger(__name__)


class RewriteService:
    """
    Legacy single paragraph rewrite service.

    Deprecated:
        Use BatchRewriteService.

    Responsibilities:
        - Convert request to prompt.
        - Call AI provider.
        - Return rewrite result.
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


        try:

            prompt = PromptBuilder.build(
                request
            )


            response = (
                self._provider.generate(
                    prompt
                )
            )


            response = (
                response.strip()
            )


            if not response:

                return RewriteResult(

                    optimized_text=(
                        request.paragraph
                    ),

                    success=False,

                    provider=(
                        self._provider
                        .__class__
                        .__name__
                    ),

                    error="Empty AI response",

                )


            return RewriteResult(

                optimized_text=response,

                success=True,

                provider=(
                    self._provider
                    .__class__
                    .__name__
                ),

            )


        except Exception as exc:

            logger.exception(
                "Rewrite failed"
            )


            return RewriteResult(

                optimized_text=(
                    request.paragraph
                ),

                success=False,

                provider=(
                    self._provider
                    .__class__
                    .__name__
                ),

                error=str(exc),

            )