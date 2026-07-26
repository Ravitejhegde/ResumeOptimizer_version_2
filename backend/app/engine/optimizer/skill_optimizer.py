from __future__ import annotations

from dataclasses import replace

from app.engine.models.paragraph import Paragraph
from app.engine.planner.skill_planner import SkillPlan


class SkillOptimizer:
    """
    Updates the Skills section according to the
    approved SkillPlan.

    Responsibilities
    ----------------
    - Preserve existing skills
    - Insert approved missing skills
    - Preserve category structure
    - Preserve formatting
    - Preserve run order

    This class NEVER calls AI.
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

        optimized.runs[0].text = optimized_text

        for run in optimized.runs[1:]:

            run.text = ""

        return optimized