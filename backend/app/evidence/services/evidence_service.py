"""
app.evidence.services.evidence_service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Public entry point for evidence collection.
"""

from __future__ import annotations

from app.understanding.models.resume_understanding import (
    ResumeUnderstanding,
)

from app.gap_analysis.models.gap_analysis_model import (
    GapAnalysisModel,
)

from app.evidence.models.evidence_report import (
    EvidenceReport,
)

from app.evidence.services.evidence_engine import (
    EvidenceEngine,
)


class EvidenceService:
    """
    Public service responsible for building
    evidence from the resume.
    """

    def __init__(
        self,
    ) -> None:

        self._engine = EvidenceEngine()

    def analyze(
        self,
        resume: ResumeUnderstanding,
        gap: GapAnalysisModel,
    ) -> EvidenceReport:

        return self._engine.analyze(
            resume,
            gap,
        )