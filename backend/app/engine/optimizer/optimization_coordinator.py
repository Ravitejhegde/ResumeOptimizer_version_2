from __future__ import annotations

from app.engine.models.document import Document
from app.engine.optimizer.skill_optimizer import (
    SkillOptimizer,
)
from app.engine.optimizer.text_optimizer import (
    TextOptimizer,
)
from app.engine.planner.locked_entity_extractor import (
    LockedEntityExtractor,
)
from app.engine.planner.plan import (
    OptimizationPlan,
)

from app.services.ai.ai_factory import (
    AIFactory,
)
from app.services.ai.batch.batch_models import (
    BatchRewriteRequest,
    ParagraphRewriteRequest,
)
from app.services.ai.batch.batch_rewrite_service import (
    BatchRewriteService,
)


class OptimizationCoordinator:
    """
    Executes an OptimizationPlan.

    Planner decides WHAT to optimize.

    Optimizer only EXECUTES the plan.

    One Resume
        ↓
    One AI Request
    """

    def __init__(self) -> None:

        provider = AIFactory.create()

        self._batch_service = BatchRewriteService(
            provider
        )

    def optimize(
        self,
        document: Document,
        plan: OptimizationPlan,
    ) -> Document:

        document = self._optimize_skills(
            document,
            plan,
        )

        document = self._optimize_text(
            document,
            plan,
        )

        return document

    def _optimize_skills(
        self,
        document: Document,
        plan: OptimizationPlan,
    ) -> Document:

        if plan.skill_plan is None:
            return document

        skills_text = ", ".join(
            plan.skill_plan.selected_skills
        )

        if not skills_text:
            return document

        for paragraph in document.paragraphs:

            if (
                paragraph.section
                and paragraph.section.lower() == "skills"
            ):

                SkillOptimizer.apply(
                    paragraph,
                    plan.skill_plan,
                    skills_text,
                )

        return document

    def _optimize_text(
        self,
        document: Document,
        plan: OptimizationPlan,
    ) -> Document:

        requests: list[
            ParagraphRewriteRequest
        ] = []

        paragraph_lookup: dict[str, object] = {}

        for paragraph in document.paragraphs:

            if (
                paragraph.id
                not in plan.rewrite_paragraph_ids
            ):
                continue

            paragraph_lookup[
                paragraph.id
            ] = paragraph

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

        if not requests:
            return document

        locked_entities = (
            LockedEntityExtractor.extract(
                document
            )
        )

        batch_request = BatchRewriteRequest(

            target_role="",

            selected_skills=(
                plan.skill_plan.selected_skills
                if plan.skill_plan
                else []
            ),

            locked=locked_entities,

            paragraphs=requests,

        )

        result = self._batch_service.rewrite(
            batch_request
        )

        if not result.success:
            return document

        for rewritten in result.paragraphs:

            paragraph = paragraph_lookup.get(
                rewritten.id
            )

            if paragraph is None:
                continue

            TextOptimizer.apply(
                paragraph,
                rewritten.text,
            )

        return document