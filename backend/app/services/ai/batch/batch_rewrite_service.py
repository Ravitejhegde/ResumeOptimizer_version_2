from __future__ import annotations

import logging

from app.services.ai.ai_provider import (
    AIProvider,
)

from app.engine.models.ai.prompt_request import (
    BatchRewriteRequest,
)

from app.engine.models.ai.prompt_response import (
    BatchRewriteResult,
)

from app.services.ai.batch.batch_prompt_builder import (
    BatchPromptBuilder,
)

from app.services.ai.batch.batch_response_parser import (
    BatchResponseParser,
)


logger = logging.getLogger(__name__)


class BatchRewriteService:
    """
    Executes resume batch rewriting.

    Pipeline:

        BatchRewriteRequest
                |
                v
        Prompt Builder
                |
                v
        AI Provider
                |
                v
        Response Parser
                |
                v
        BatchRewriteResult
    """


    def __init__(
        self,
        provider: AIProvider,
    ) -> None:

        self._provider = provider


    def rewrite(
        self,
        request: BatchRewriteRequest,
    ) -> BatchRewriteResult:


        prompt = BatchPromptBuilder.build(
            request
        )


        logger.info(
            "Sending batch rewrite request using %s",
            self._provider.__class__.__name__,
        )


        response = self._provider.generate(
            prompt
        )


        logger.info(
            "Received AI response"
        )


        return BatchResponseParser.parse(

            response=response,

            provider=(
                self._provider
                .__class__
                .__name__
            ),

        )