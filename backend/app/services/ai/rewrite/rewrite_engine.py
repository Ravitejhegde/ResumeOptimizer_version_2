from app.services.ai.rewrite.rewrite_prompt_builder import (
    RewritePromptBuilder,
)

from app.services.ai.rewrite.rewrite_response_parser import (
    RewriteResponseParser,
)


class RewriteEngine:
    """
    Temporary rewrite engine.

    AI is disabled during integration testing.
    Returns the original paragraph text.
    """

    @classmethod
    def rewrite(
        cls,
        paragraph,
        optimization_plan,
        job_description,
    ):

        # Build the prompt so we can verify it later
        prompt = RewritePromptBuilder.build(
            paragraph,
            optimization_plan,
            job_description,
        )

        # TODO:
        # Enable OpenRouter after the backend
        # pipeline is fully working.
        response = paragraph.text

        return RewriteResponseParser.parse(
            response
        )