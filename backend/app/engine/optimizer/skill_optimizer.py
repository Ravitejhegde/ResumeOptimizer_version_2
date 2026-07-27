from __future__ import annotations

from dataclasses import replace

from app.engine.models.paragraph import (
    Paragraph,
)
from app.engine.planner.skill_planner import (
    SkillPlan,
)


class SkillOptimizer:
    """
    Updates the Skills section using the
    prepared SkillPlan.

    No AI.
    No business logic.
    """

    @staticmethod
    def apply(
        paragraph: Paragraph,
        plan: SkillPlan,
        optimized_text: str,
    ) -> Paragraph:

        if not paragraph.editable:
            return paragraph

        optimized = replace(
            paragraph
        )

        if not optimized.runs:
            return optimized

        # Preserve formatting by only
        # replacing the text of existing runs.

        optimized.runs[0].text = (
            optimized_text
        )

        for run in optimized.runs[1:]:

            run.text = ""

        return optimized