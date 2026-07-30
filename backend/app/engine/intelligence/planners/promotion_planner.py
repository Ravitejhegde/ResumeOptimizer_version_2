from __future__ import annotations

from app.engine.models.intelligence.promotion_plan import (
    PromotionDecision,
    PromotionPlan,
)

from app.engine.models.intelligence.skill_priority import (
    SkillPriority,
)

from app.knowledge.knowledge_manager import (
    KnowledgeManager,
)


class PromotionPlanner:
    """
    Converts selected technologies into
    promotion decisions.

    Responsibility:

        Skill Priority
              ↓
        Section Decision
              ↓
        Promotion Plan

    Does not rewrite content.
    """


    def __init__(
        self,
        knowledge: KnowledgeManager,
    ) -> None:

        self._knowledge = knowledge


    # --------------------------------------------------

    def build(
        self,
        technologies: list[SkillPriority],
    ) -> PromotionPlan:


        decisions: list[
            PromotionDecision
        ] = []


        for technology in technologies:


            section = self._resolve_section(
                technology.technology,
            )


            decisions.append(

                PromotionDecision(

                    technology=(
                        technology.technology
                    ),

                    section=section,

                    priority=(
                        technology.priority
                    ),

                    confidence=(
                        technology.confidence
                    ),

                    reason=(
                        "Required by target role"
                    ),

                )

            )


        return PromotionPlan(
            decisions=decisions,
        )


    # --------------------------------------------------

    def _resolve_section(
        self,
        technology: str,
    ) -> str:
        """
        Resolve best resume section
        using existing knowledge categories.

        No hardcoded technology mapping.
        Uses KnowledgeManager.
        """


        technology = technology.lower().strip()


        categories = (
            self._knowledge.categorize(
                [
                    technology
                ]
            )
        )


        # Backend technologies
        if "backend" in categories:

            return "experience"


        # Cloud technologies
        if "cloud" in categories:

            return "experience"


        # Database technologies
        if "database" in categories:

            return "experience"


        # AI/ML usually fits projects
        if "ai_ml" in categories:

            return "projects"


        # Safe default
        return "projects"