from app.services.ai.provider.openrouter_provider import (
    OpenRouterProvider,
)

from app.services.ai.rewrite.rewrite_prompt_builder import (
    RewritePromptBuilder,
)

from app.services.ai.rewrite.rewrite_response_parser import (
    RewriteResponseParser,
)


class RewriteEngine:

    provider = OpenRouterProvider()

    @classmethod
    def rewrite(
        cls,
        paragraph,
        optimization_plan,
        job_description,
    ):

        prompt = RewritePromptBuilder.build(

            paragraph,

            optimization_plan,

            job_description,

        )

        response = cls.provider.generate(
            prompt
        )

        return RewriteResponseParser.parse(
            response
        )