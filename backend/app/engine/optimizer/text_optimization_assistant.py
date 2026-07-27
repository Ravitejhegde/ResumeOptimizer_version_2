from __future__ import annotations

from app.engine.models.document import (
    Document,
)
from app.engine.optimizer.ai_request_builder import (
    AIRequestBuilder,
)
from app.engine.optimizer.ai_response_applier import (
    AIResponseApplier,
)
from app.engine.planner.plan import (
    OptimizationPlan,
)

from app.services.ai.ai_factory import (
    AIFactory,
)
from app.services.ai.batch.batch_rewrite_service import (
    BatchRewriteService,
)


class TextOptimizationAssistant:
    """
    Executes AI-powered text optimization.

    Responsibilities
    ----------------
    • Build AI request
    • Call AI once
    • Apply AI response

    Never decides WHAT to optimize.
    Those decisions are already contained
    inside OptimizationStrategy.
    """

    def __init__(self) -> None:

        provider = AIFactory.create()

        self._batch_service = (
            BatchRewriteService(
                provider
            )
        )

    def optimize(
        self,
        document: Document,
        plan: OptimizationPlan,
    ) -> Document:

        # Nothing to optimize
        if (
            plan.optimization_strategy is None
            or
            not plan.rewrite_paragraph_ids
        ):
            return document

        # Build a single AI request
        batch_request = (
            AIRequestBuilder.build(
                document=document,
                plan=plan,
            )
        )

        if not batch_request.paragraphs:
            return document

        # Single AI call
        result = (
            self._batch_service.rewrite(
                batch_request
            )
        )

        if not result.success:
            return document

        # Apply rewritten paragraphs
        return AIResponseApplier.apply(
            document=document,
            result=result,
        )