from app.services.intelligence.pipelines.resume_pipeline import (
    ResumePipeline,
)


class ResumeAnalyzer:
    """
    High-level entry point for resume analysis.

    Delegates all processing to ResumePipeline.
    """

    @classmethod
    def analyze(
        cls,
        blocks,
    ):

        return ResumePipeline.run(
            blocks
        )