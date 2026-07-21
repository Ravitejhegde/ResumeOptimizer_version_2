from app.services.ai.batch.batch_rewrite_engine import (
    BatchRewriteEngine,
)

from app.services.intelligence.translator.paragraph_selector import (
    ParagraphSelector,
)


class ParagraphOptimizer:

    @classmethod
    def optimize(
        cls,
        snapshot,
        optimization_plan,
        job_description,
    ):

        paragraphs = ParagraphSelector.select(
            snapshot
        )

        updates = BatchRewriteEngine.rewrite(
            paragraphs,
            optimization_plan,
            job_description,
        )

        return updates