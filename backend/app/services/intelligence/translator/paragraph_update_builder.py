from app.services.intelligence.translator.paragraph_optimizer import (
    ParagraphOptimizer,
)


class ParagraphUpdateBuilder:

    @classmethod
    def build(
        cls,
        snapshot,
        optimization_plan,
        job_description,
    ):

        return ParagraphOptimizer.optimize(
            snapshot,
            optimization_plan,
            job_description,
        )