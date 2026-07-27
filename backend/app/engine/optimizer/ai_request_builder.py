from __future__ import annotations

from app.engine.models.document import (
    Document,
)
from app.engine.models.optimization_strategy import (
    OptimizationStrategy,
)
from app.engine.optimizer.paragraph_selector import (
    ParagraphSelector,
)
from app.engine.planner.locked_entity_extractor import (
    LockedEntityExtractor,
)
from app.engine.planner.plan import (
    OptimizationPlan,
)

from app.services.ai.batch.batch_models import (
    BatchRewriteRequest,
    ParagraphRewriteRequest,
)


class AIRequestBuilder:
    """
    Builds the complete AI rewrite request.
    """

    @staticmethod
    def build(
        document: Document,
        plan: OptimizationPlan,
    ) -> BatchRewriteRequest:

        requests: list[
            ParagraphRewriteRequest
        ] = []

        paragraphs = (
            ParagraphSelector.select(
                document,
                plan,
            )
        )

        for paragraph in paragraphs:

            constraints = (
                plan.layout_constraints.get(
                    paragraph.id
                )
            )

            if constraints:

                max_characters = (
                    constraints.max_characters
                )

                max_words = (
                    constraints.max_words
                )

            else:

                max_characters = 500
                max_words = 80

            requests.append(

                ParagraphRewriteRequest(

                    id=paragraph.id,

                    type=(
                        paragraph.section
                        or "paragraph"
                    ),

                    text=paragraph.text,

                    max_characters=max_characters,

                    max_words=max_words,

                    rewrite=True,

                )

            )

        locked = (
            LockedEntityExtractor.extract(
                document
            )
        )

        strategy: OptimizationStrategy | None = (
            plan.optimization_strategy
        )

        # -------------------------------------------------
        # DEBUG
        # -------------------------------------------------

        print("\n" + "=" * 80)
        print("OPTIMIZATION STRATEGY DEBUG")
        print("=" * 80)

        print("Type:", type(strategy))
        print("Module:", strategy.__class__.__module__)
        print("Class :", strategy.__class__.__name__)

        if hasattr(strategy, "__dataclass_fields__"):
            print(
                "Fields:",
                list(strategy.__dataclass_fields__.keys())
            )

        print("Object:", strategy)

        print("=" * 80 + "\n")

        # -------------------------------------------------

        return BatchRewriteRequest(

            optimization_strategy=strategy,

            target_role=(
                strategy.role
                if strategy
                else ""
            ),

            selected_skills=(
                plan.skill_plan.selected_skills
                if plan.skill_plan
                else []
            ),

            locked=locked,

            paragraphs=requests,

        )




