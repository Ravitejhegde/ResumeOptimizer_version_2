"""
app.planner.evidence.evidence_engine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Validates whether planner recommendations are supported
by resume evidence.
"""

from __future__ import annotations

from app.analyzer.models.document_model import (
    DocumentModel,
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

    Evidence analysis is based on the resume document and
    the priorities already prepared by the Planner.
    """

    @staticmethod
    def _normalize(value: str) -> str:
        """
        Normalize a skill or technology name so that
        equivalent representations can be compared.

        Examples:
            Node.js  -> nodejs
            Node-JS  -> nodejs
            node_js  -> nodejs
            AWS      -> aws
        """

        return (
            value
            .casefold()
            .replace(".", "")
            .replace("-", "")
            .replace("_", "")
            .replace(" ", "")
        )

    def build(
        self,
        document: DocumentModel,
        priorities: PriorityPlan,
    ) -> EvidenceReport:
        """
        Build an evidence report for all optimization priorities.

        Evidence sources are limited to information already
        present in the analyzed resume.

        User-selected missing skills are treated differently:
        they are not considered existing evidence, but they are
        authorized for incorporation without fabricating claims.
        """

        report = EvidenceReport()

        # -----------------------------------
        # Resume evidence
        # -----------------------------------

        resume_skills = {
            self._normalize(skill)
            for skill in document.skills.keys()
        }

        resume_technologies = {
            self._normalize(technology)
            for technology in document.technologies.keys()
        }

        # -----------------------------------
        # Evaluate each optimization priority
        # -----------------------------------

        for item in priorities.items:

            supported = False
            confidence = 0.0

            sources: list[str] = []
            reasoning: list[str] = []

            item_id = self._normalize(item.id)

            # -----------------------------------
            # Direct skill evidence
            # -----------------------------------

            if item_id in resume_skills:

                supported = True
                confidence = 1.0

                sources.append(
                    "skills"
                )

                reasoning.append(
                    "Directly found in resume skills."
                )

            # -----------------------------------
            # Direct technology evidence
            # -----------------------------------

            if (
                not supported
                and item_id in resume_technologies
            ):

                supported = True
                confidence = 1.0

                sources.append(
                    "technologies"
                )

                reasoning.append(
                    "Directly found in resume technologies."
                )

            # -----------------------------------
            # Recommendation
            # -----------------------------------

            if supported:

                action = (
                    "Strengthen existing evidence."
                )

            elif (
                item.metadata.get(
                    "user_selected"
                ) == "True"
            ):

                action = (
                    "User authorized this skill. "
                    "Incorporate it where truthful "
                    "without fabricating evidence."
                )

                reasoning.append(
                    "Skill was explicitly selected by the user."
                )

            else:

                action = (
                    "Do not fabricate. "
                    "Recommend only if truthful."
                )

            # -----------------------------------
            # Add evidence result
            # -----------------------------------

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