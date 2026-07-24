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
    Rewrites resume paragraphs using OpenRouter.
    """

    @classmethod
    def rewrite(
        cls,
        paragraphs,
        optimization_plan,
        job_description,
    ):

        if not paragraphs:
            return {}

        provider = OpenRouterProvider()

        updates = {}

        for paragraph in paragraphs:

            print("=" * 60)
            print("Rewriting:", paragraph.id)
            print("=" * 60)

            prompt = BatchPromptBuilder.build(
                [paragraph],
                optimization_plan,
                job_description,
            )

            response = provider.generate(
                prompt=prompt,
                temperature=0.2,
                max_tokens=800,
            )

            result = BatchResponseParser.parse(
                response
            )

            # Expected format:
            # {
            #     "P00001": "...new text..."
            # }

            if isinstance(result, dict):

                updates.update(result)

            else:

                updates[paragraph.id] = paragraph.text

        return updates