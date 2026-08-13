"""
app.planner.evidence.evidence_engine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Validates whether planner recommendations are supported by resume evidence.
"""

from __future__ import annotations

from app.analyzer.models.document_model import (
    DocumentModel,
)
from app.knowledge.provider import (
    get_knowledge,
)
from app.planner.evidence.evidence_item import (
    EvidenceItem,
)
from app.planner.evidence.evidence_report import (
    EvidenceReport,
)
from app.planner.priority.priority_plan import (
    PriorityPlan,
)


class EvidenceEngine:
    """
    Validates optimization items against resume evidence.
    """

    def __init__(self) -> None:
        self._runtime = get_knowledge()

    def build(
        self,
        document: DocumentModel,
        priorities: PriorityPlan,
    ) -> EvidenceReport:

        report = EvidenceReport()

        resume_skills = set(
            document.skills.keys()
        )

        resume_technologies = set(
            document.technologies.keys()
        )

        for item in priorities.items:

            supported = False

            confidence = 0.0

            sources: list[str] = []

            reasoning: list[str] = []

            # -----------------------------------
            # Direct skill evidence
            # -----------------------------------

            if item.id in resume_skills:

                supported = True

                confidence = 1.0

                sources.append("skills")

                reasoning.append(
                    "Directly found in resume skills."
                )

            # -----------------------------------
            # Technology relationship evidence
            # -----------------------------------

            if not supported:

                related = (
                    self._runtime.skills
                    .find_by_id(item.id)
                )

                if related:

                    related_tech = set(
                        related.get(
                            "technology_ids",
                            [],
                        )
                    )

                    matched = (
                        related_tech
                        & resume_technologies
                    )

                    if matched:

                        supported = True

                        confidence = 0.80

                        sources.append(
                            "technology_relationship"
                        )

                        reasoning.append(
                            "Supported through related technologies."
                        )

            # -----------------------------------
            # Recommendation
            # -----------------------------------

            if supported:

                action = (
                    "Strengthen existing evidence."
                )

            else:

                action = (
                    "Do not fabricate. Recommend only if truthful."
                )

            report.items.append(
                EvidenceItem(
                    id=item.id,
                    type=item.type,
                    supported=supported,
                    confidence=confidence,
                    evidence_sources=sources,
                    reasoning=reasoning,
                    recommended_action=action,
                )
            )

        return report