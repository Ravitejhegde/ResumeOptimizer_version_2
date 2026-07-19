from app.services.intelligence.pipelines.jd_pipeline import (
    JDPipeline,
)


class JDAnalyzer:

    @classmethod
    def analyze(
        cls,
        job_description,
    ):

        return JDPipeline.run(
            job_description
        )