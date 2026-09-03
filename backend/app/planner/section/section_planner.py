"""
app.planner.section.section_planner
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Determines where optimization should be applied.
"""

from __future__ import annotations

from app.analyzer.models.document_model import (
    DocumentModel,
)
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
    Maps optimization items to actual resume sections.

    Knowledge presentation categories such as
    "Frontend Technologies" or "Tools & Platforms"
    are not treated as physical resume sections.

    Physical sections come from DocumentModel.sections.
    """

    _UNTOUCHED_SECTIONS = {
        "contact",
        "education",
        "certifications",
    }

    _CONTENT_SECTIONS = {
        "summary",
        "experience",
        "projects",
        "skills",
        "achievements",
        "publications",
    }

    def build(
        self,
        document: DocumentModel,
        priorities: PriorityPlan,
        evidence: EvidenceReport,
    ) -> SectionPlan:
        """
        Build a section-level optimization plan.

        Existing supported skills may be strengthened in
        Skills, Experience, and Projects.

        User-selected missing skills are explicitly authorized
        for incorporation, but without existing evidence they
        are targeted only at the Skills section.

        This prevents unsupported skills from being presented
        as prior professional experience.
        """

        plan = SectionPlan()

        available_sections = {
            section.casefold()
            for section in document.sections.keys()
        }

        evidence_map = {
            item.id: item
            for item in evidence.items
        }

        for priority in priorities.items:

            item_evidence = evidence_map.get(
                priority.id
            )

            if item_evidence is None:
                continue

            user_selected = (
                priority.metadata.get(
                    "user_selected"
                ) == "True"
            )

            supported = item_evidence.supported

            # ---------------------------------
            # Unsupported + not selected
            # ---------------------------------

            if not supported and not user_selected:
                continue

            target_sections: list[str] = []

            # ---------------------------------
            # User-selected missing skill
            # ---------------------------------

            if user_selected and not supported:

                if "skills" in available_sections:
                    target_sections.append(
                        "skills"
                    )

            # ---------------------------------
            # Existing supported skill
            # ---------------------------------

            elif supported:

                if "skills" in available_sections:
                    target_sections.append(
                        "skills"
                    )

                for section in (
                    "experience",
                    "projects",
                ):
                    if section in available_sections:
                        target_sections.append(
                            section
                        )

            # ---------------------------------
            # Safety filter
            # ---------------------------------

            target_sections = [
                section
                for section in target_sections
                if (
                    section.casefold()
                    not in self._UNTOUCHED_SECTIONS
                )
            ]

            # Remove duplicates while preserving order.
            target_sections = list(
                dict.fromkeys(
                    target_sections
                )
            )

            # ---------------------------------
            # Store section plan
            # ---------------------------------

            for section in target_sections:

                plan.sections.setdefault(
                    section,
                    [],
                )

                if priority.id not in plan.sections[
                    section
                ]:
                    plan.sections[
                        section
                    ].append(
                        priority.id
                    )

                if supported:
                    plan.reasoning[
                        section
                    ] = (
                        f"'{priority.title}' is supported "
                        "by existing resume evidence "
                        "and may be strengthened."
                    )
                else:
                    plan.reasoning[
                        section
                    ] = (
                        f"'{priority.title}' was explicitly "
                        "selected by the user and will be "
                        "incorporated in the Skills section "
                        "without fabricating experience."
                    )

        # ---------------------------------
        # Protected sections
        # ---------------------------------

        plan.untouched_sections = [
            "contact",
            "education",
            "certifications",
        ]

        return plan