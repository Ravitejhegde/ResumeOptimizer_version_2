from app.services.batch.batch_prompt_builder import (
    BatchPromptBuilder,
)

from app.services.batch.batch_response_parser import (
    BatchResponseParser,
)

from app.services.ai.openrouter_provider import (
    OpenRouterProvider,
)


class BatchAIService:

    def __init__(self):

        self.provider = OpenRouterProvider()

    def optimize_resume(
        self,
        blocks,
        knowledge,
        job_description,
    ):

        prompt = BatchPromptBuilder.build(
            blocks,
            knowledge,
            job_description,
        )

        response = self.provider.generate(prompt)

        return BatchResponseParser.parse(

    response,

    original_blocks,

)