from __future__ import annotations

from app.engine.models.document import (
    Document,
)
from app.engine.optimizer.skill_optimizer import (
    SkillOptimizer,
)
from app.engine.planner.plan import (
    OptimizationPlan,
)


class SkillOptimizationAssistant:
    """
    Handles Skills section optimization.

    Responsibilities
    ----------------
    • Update only Skills section
    • Never call AI
    • Never rewrite experience/projects
    """

    def optimize(
        self,
        document: Document,
        plan: OptimizationPlan,
    ) -> Document:

        if plan.skill_plan is None:
            return document

        optimized_text = ", ".join(
            plan.skill_plan.selected_skills
        )

        if not optimized_text:
            return document

        for index, paragraph in enumerate(
            document.paragraphs
        ):

            if (
                paragraph.section
                and paragraph.section.lower() == "skills"
            ):

                document.paragraphs[index] = (
                    SkillOptimizer.apply(
                        paragraph=paragraph,
                        plan=plan.skill_plan,
                        optimized_text=optimized_text,
                    )
                )

        return document




