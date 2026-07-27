from __future__ import annotations

from app.engine.models.document import Document
from app.engine.models.promotion_plan import (
    PromotionPlan,
)


class ParagraphTargetSelector:
    """
    Selects the most suitable paragraph
    for every promoted skill.

    AI does not decide placement.

    The planner decides first.
    """

    SECTION_PRIORITY = {

        "summary": [
            "summary",
            "profile",
            "objective",
        ],

        "experience": [
            "experience",
            "work experience",
        ],

        "projects": [
            "projects",
            "project",
        ],

        "skills": [
            "skills",
            "technical skills",
        ],

    }

    @classmethod
    def assign(
        cls,
        document: Document,
        plan: PromotionPlan,
    ) -> PromotionPlan:

        for decision in plan.decisions:

            if decision.action != "promote":
                continue

            wanted = cls.SECTION_PRIORITY.get(
                decision.target_section,
                [],
            )

            for paragraph in document.paragraphs:

                section = (
                    paragraph.section or ""
                ).lower()

                if section in wanted:

                    decision.reason += (
                        f" Assigned to {section}."
                    )

                    break

        return plan




