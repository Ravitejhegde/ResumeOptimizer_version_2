from app.services.ai.provider.openrouter_provider import (
    OpenRouterProvider,
)

from app.services.ai.batch.batch_prompt_builder import (
    BatchPromptBuilder,
)

from app.services.ai.batch.batch_response_parser import (
    BatchResponseParser,
)


class BatchRewriteEngine:
    """
    Rewrites multiple resume paragraphs
    in a single AI request.
    """

    provider = OpenRouterProvider()

    @classmethod
    def rewrite(
        cls,
        paragraphs,
        optimization_plan,
        job_description,
    ) -> dict:

        if not paragraphs:
            return {}

        prompt = BatchPromptBuilder.build(
            paragraphs,
            optimization_plan,
            job_description,
        )

        response = cls.provider.generate(
            prompt
        )

        return BatchResponseParser.parse(
            response
        )