from app.services.intelligence.pipelines.optimization_pipeline import (
    OptimizationPipeline,
)


class IntelligenceEngine:
    """
    Main Resume Intelligence Engine
    """

    @classmethod
    def analyze(
        cls,
        blocks,
        job_description,
    ):

        return OptimizationPipeline.run(
            blocks=blocks,
            job_description=job_description,
        )