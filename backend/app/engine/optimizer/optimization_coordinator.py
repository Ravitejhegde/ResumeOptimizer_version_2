from __future__ import annotations

from app.engine.models.document import (
    Document,
)
from app.engine.optimizer.skill_optimization_assistant import (
    SkillOptimizationAssistant,
)
from app.engine.optimizer.text_optimization_assistant import (
    TextOptimizationAssistant,
)
from app.engine.planner.plan import (
    OptimizationPlan,
)


class OptimizationCoordinator:
    """
    Executes an OptimizationPlan.

    Responsibilities
    ----------------
    • Coordinate optimization stages
    • Never contain business logic
    • Never build AI requests
    • Never process AI responses

    Every responsibility belongs to an
    assistant class.
    """

    def __init__(self) -> None:

        self._skill_optimizer = (
            SkillOptimizationAssistant()
        )

        self._text_optimizer = (
            TextOptimizationAssistant()
        )

    def optimize(
        self,
        document: Document,
        plan: OptimizationPlan,
    ) -> Document:

        document = (
            self._skill_optimizer.optimize(
                document=document,
                plan=plan,
            )
        )

        document = (
            self._text_optimizer.optimize(
                document=document,
                plan=plan,
            )
        )

        return document




