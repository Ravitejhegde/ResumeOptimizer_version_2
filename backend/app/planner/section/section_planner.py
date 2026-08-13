"""
app.planner.section.section_planner
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Determines where optimization should be applied.
"""

from __future__ import annotations

from app.planner.evidence.evidence_report import (
    EvidenceReport,
)
from app.planner.priority.priority_plan import (
    PriorityPlan,
)
from app.planner.section.section_plan import (
    SectionPlan,
)


class SectionPlanner:
    """
    Maps supported optimization items to resume sections.
    """

    def build(
        self,
        priorities: PriorityPlan,
        evidence: EvidenceReport,
    ) -> SectionPlan:
        """
        Build a section-level optimization plan.
        """

        plan = SectionPlan()

        evidence_map = {
            item.id: item
            for item in evidence.items
        }

        for priority in priorities.items:

            item_evidence = evidence_map.get(
                priority.id
            )

            # Skip unsupported recommendations.
            if (
                item_evidence is None
                or not item_evidence.supported
            ):
                continue

            # Use the affected sections defined by the priority.
            sections = (
                priority.affected_sections
                or ["Experience"]
            )

            for section in sections:

                plan.sections.setdefault(
                    section,
                    [],
                ).append(
                    priority.id
                )

                plan.reasoning[
                    section
                ] = (
                    f"'{priority.title}' is supported by resume evidence."
                )

        # Sections that should never be modified automatically.
        plan.untouched_sections = [
            "Personal Information",
            "Education",
            "Certificates",
        ]

        return plan