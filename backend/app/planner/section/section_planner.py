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
    Maps optimization items to actual resume sections
    and, where possible, to the exact paragraphs that
    should be modified.
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
        for incorporation in the Skills section.

        For Skills optimization, the planner narrows the
        authorization to the paragraph whose category label
        matches the skill's presentation category.
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

            target_sections = list(
                dict.fromkeys(
                    target_sections
                )
            )

            # ---------------------------------
            # Store section plan
            # ---------------------------------

            for section in target_sections:

                section_model = document.sections.get(
                    section
                )

                if section_model is None:
                    continue

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

                # ---------------------------------
                # Skills paragraph targeting
                # ---------------------------------

                if section.casefold() == "skills":

                    presentation_category = (
                        priority.metadata.get(
                            "presentation_category",
                            "",
                        ).strip()
                    )

                    matching_paragraph_ids = (
                        self._find_skill_paragraphs(
                            document,
                            section_model,
                            presentation_category,
                        )
                    )

                    if matching_paragraph_ids:

                        plan.paragraph_ids.setdefault(
                            section,
                            [],
                        )

                        for paragraph_id in (
                            matching_paragraph_ids
                        ):
                            if paragraph_id not in (
                                plan.paragraph_ids[
                                    section
                                ]
                            ):
                                plan.paragraph_ids[
                                    section
                                ].append(
                                    paragraph_id
                                )

                    continue

                # ---------------------------------
                # Other content sections
                # ---------------------------------

                plan.paragraph_ids.setdefault(
                    section,
                    [],
                )

                for paragraph_index in (
                    section_model.paragraph_indexes
                ):
                    paragraph_id = (
                        f"p{paragraph_index}"
                    )

                    if paragraph_id not in (
                        plan.paragraph_ids[
                            section
                        ]
                    ):
                        plan.paragraph_ids[
                            section
                        ].append(
                            paragraph_id
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

    def _find_skill_paragraphs(
        self,
        document: DocumentModel,
        section_model,
        presentation_category: str,
    ) -> list[str]:
        """
        Find Skills paragraphs whose leading category
        label matches the Knowledge presentation category.

        Uses the section's global paragraph indexes to
        read the actual paragraphs from DocumentModel.

        Example:

            Tools & Platforms:
            Git, GitHub, Docker

        matches:

            presentation_category =
            "Tools & Platforms"
        """

        if not presentation_category:
            return []

        target = self._normalize_category(
            presentation_category
        )

        matches: list[str] = []

        for paragraph_index in (
            section_model.paragraph_indexes
        ):
            if not (
                0 <= paragraph_index
                < len(document.paragraphs)
            ):
                continue

            paragraph = document.paragraphs[
                paragraph_index
            ]

            label = self._extract_category_label(
                paragraph
            )

            if not label:
                continue

            if (
                self._normalize_category(label)
                == target
            ):
                matches.append(
                    f"p{paragraph_index}"
                )

        return matches

    @staticmethod
    def _extract_category_label(
        paragraph: str,
    ) -> str:
        """
        Extract the text before the first colon.

        Example:

            "Tools & Platforms: Git, GitHub"

        becomes:

            "Tools & Platforms"
        """

        if not paragraph:
            return ""

        if ":" not in paragraph:
            return ""

        return paragraph.split(
            ":",
            1,
        )[0].strip()

    @staticmethod
    def _normalize_category(
        value: str,
    ) -> str:
        """
        Normalize category labels for comparison.
        """

        return " ".join(
            value.casefold()
            .replace("&", "and")
            .split()
        )