from app.services.intelligence.pipelines.resume_pipeline import (
    ResumePipeline,
)


class ResumeAnalyzer:

    @classmethod
    def analyze(
        cls,
        blocks,
    ):

        return ResumePipeline.run(
            blocks
        )