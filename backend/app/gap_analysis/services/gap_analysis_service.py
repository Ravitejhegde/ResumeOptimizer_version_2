"""
app.gap_analysis.services.gap_analysis_service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Public entry point for gap analysis.
"""

from __future__ import annotations

from app.understanding.models.resume_understanding import (
    ResumeUnderstanding,
)

from app.job_understanding.models.job_understanding import (
    JobUnderstanding,
)

from app.gap_analysis.models.gap_analysis_model import (
    GapAnalysisModel,
)

from app.gap_analysis.services.gap_analyzer import (
    GapAnalyzer,
)


class GapAnalysisService:
    """
    Public service for performing gap analysis.
    """

    def __init__(self) -> None:

        self._analyzer = GapAnalyzer()

    def analyze(
        self,
        resume: ResumeUnderstanding,
        job: JobUnderstanding,
    ) -> GapAnalysisModel:

        return self._analyzer.analyze(
            resume,
            job,
        )