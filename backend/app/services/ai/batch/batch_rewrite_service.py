from __future__ import annotations

from app.services.ai.ai_provider import AIProvider
from app.services.ai.batch.batch_models import (
    BatchRewriteRequest,
    BatchRewriteResult,
)
from app.services.ai.batch.batch_prompt_builder import (
    BatchPromptBuilder,
)
from app.services.ai.batch.batch_response_parser import (
    BatchResponseParser,
)


class BatchRewriteService:
    """
    Performs a single AI request for the
    entire resume.

    One Resume
        ↓
    One Prompt
        ↓
    One AI Call
        ↓
    One JSON Response
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

        response = self._provider.generate(
            prompt
        )
        print("\n" + "=" * 80)
        print("RAW AI RESPONSE")
        print("=" * 80)
        print(response)
        print("=" * 80 + "\n")

        return BatchResponseParser.parse(
            response=response,
            provider=self._provider.__class__.__name__,
        )