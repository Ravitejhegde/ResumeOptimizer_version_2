"""
app.optimizer.services.experience_optimizer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Optimizes resume experience using AI.
"""

from __future__ import annotations

from app.ai.models.ai_request import (
    AIRequest,
)
from app.ai.parser.ai_response_parser import (
    AIResponseParser,
)
from app.ai.prompt.experience_prompt import (
    ExperiencePrompt,
)
from app.ai.services.ai_optimizer import (
    AIOptimizer,
)
from app.analyzer.models.document_model import (
    DocumentModel,
)
from app.planner.blueprint.optimization_blueprint import (
    OptimizationBlueprint,
)


class ExperienceOptimizer:
    """
    Optimizes resume experience using AI.
    """

    def __init__(self) -> None:

        self._prompt = ExperiencePrompt()

        self._ai = AIOptimizer()

        self._parser = AIResponseParser()

    def optimize(
        self,
        document: DocumentModel,
        blueprint: OptimizationBlueprint,
    ) -> DocumentModel:
        """
        Optimize every experience entry.
        """

        if not document.experiences:
            return document

        if (
            "Experience"
            not in blueprint.section_plan.sections
        ):
            return document

        for experience in document.experiences:

            prompt = self._prompt.build(
                experience,
                blueprint,
            )

            request = AIRequest(
                prompt=prompt,
            )

            response = self._ai.optimize(
                request,
            )

            if not response.success:
                continue

            bullets = (
                self._parser.parse_bullets(
                    response.content,
                )
            )

            if bullets:

                experience.description = bullets

        return document