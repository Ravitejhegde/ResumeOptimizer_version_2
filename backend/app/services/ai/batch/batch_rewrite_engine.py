from app.services.ai.batch.batch_prompt_builder import (
    BatchPromptBuilder,
)


class BatchRewriteEngine:
    """
    Temporary rewrite engine for integration testing.

    Returns original paragraph text without calling AI.
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

        # Build prompt (for debugging only)
        BatchPromptBuilder.build(
            paragraphs,
            optimization_plan,
            job_description,
        )

        updates = {}

        for paragraph in paragraphs:
            updates[paragraph.id] = paragraph.text

        return updates