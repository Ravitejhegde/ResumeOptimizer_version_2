"""
app.evidence.services.evidence_engine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Determines whether missing requirements can be safely introduced.
"""

from __future__ import annotations

from app.evidence.models.evidence_item import (
    EvidenceItem,
)
from app.evidence.models.evidence_report import (
    EvidenceReport,
)
from app.evidence.services.evidence_scorer import (
    EvidenceScorer,
)
from app.gap_analysis.models.gap_analysis_model import (
    GapAnalysisModel,
)
from app.knowledge.provider import (
    get_knowledge,
)
from app.understanding.models.resume_understanding import (
    ResumeUnderstanding,
)


class EvidenceEngine:
    """
    Builds evidence for missing requirements.
    """

    def __init__(self) -> None:

        self._knowledge = get_knowledge()

        self._scorer = EvidenceScorer()

    def analyze(
        self,
        resume: ResumeUnderstanding,
        gap: GapAnalysisModel,
    ) -> EvidenceReport:
        """
        Analyze missing technologies and determine whether
        they can be safely introduced.

        NOTE:
        This is the current MVP implementation.
        It will later be upgraded to use Knowledge
        relationships instead of hardcoded rules.
        """

        report = EvidenceReport()

        for technology in gap.missing_technologies:

            item = EvidenceItem()

            item.id = technology.lower()

            item.type = "technology"

            item.target = technology

            #
            # MVP implementation.
            #
            if (
                resume.primary_role
                == "Backend Developer"
                and technology == "FastAPI"
            ):

                item.supported = True

                item.confidence = 0.90

                item.reason = (
                    "Backend experience supports "
                    "FastAPI introduction."
                )

                item.recommended_action = (
                    "Safe to strengthen."
                )

                item.matched_resume_skills = (
                    resume.primary_skills.copy()
                )

                item.matched_resume_technologies = (
                    resume.primary_technologies.copy()
                )

                report.safe_targets.append(
                    technology
                )

            else:

                item.supported = False

                item.confidence = 0.0

                item.reason = (
                    "No supporting evidence."
                )

                item.recommended_action = (
                    "Do not fabricate."
                )

                report.unsafe_targets.append(
                    technology
                )

            report.items.append(
                item
            )

        return report