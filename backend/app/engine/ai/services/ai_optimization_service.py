from __future__ import annotations

import logging

from app.engine.ai.context.optimization_context import (
    OptimizationContext,
)

from app.engine.ai.models.ai_response import (
    AIOptimizationResponse,
)

from app.engine.ai.prompts.resume_prompt_builder import (
    ResumePromptBuilder,
)

from app.engine.ai.services.ai_writer import (
    AIWriter,
)


logger = logging.getLogger(__name__)


class AIOptimizationService:
    """
    Coordinates complete AI optimization flow.

    Architecture:

        OptimizationContext
                |
                v
        ResumePromptBuilder
                |
                v
             AIPrompt
                |
                v
             AIWriter
                |
                v
        AIOptimizationResponse


    Responsibilities:

        - Prepare AI optimization execution.
        - Build prompt.
        - Execute one AI call.
        - Return structured AI result.


    Does NOT:

        - Modify DOCX.
        - Validate final document.
        - Decide optimization strategy.
        - Create knowledge.
    """



    def __init__(
        self,
        ai_writer: AIWriter,
        prompt_builder: ResumePromptBuilder,
    ) -> None:

        self._ai_writer = ai_writer

        self._prompt_builder = prompt_builder



    async def optimize(
        self,
        context: OptimizationContext,
    ) -> AIOptimizationResponse:
        """
        Execute complete AI optimization.

        One request.
        One response.
        """



        if not context.has_context():

            raise ValueError(
                "Incomplete optimization context."
            )



        logger.info(
            "[AIOptimizationService] "
            "Building AI prompt."
        )



        prompt = (
            self._prompt_builder.build(
                context
            )
        )



        logger.info(
            "[AIOptimizationService] "
            "Executing AI writer."
        )



        response = await (
            self._ai_writer.optimize(
                prompt
            )
        )



        logger.info(

            "[AIOptimizationService] "
            "AI optimization completed."

        )



        return response