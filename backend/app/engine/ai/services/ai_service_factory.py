from __future__ import annotations

import logging

from app.engine.ai.clients.openrouter_provider import (
    OpenRouterProvider,
)

from app.engine.ai.parsers.ai_response_parser import (
    AIResponseParser,
)

from app.engine.ai.prompts.resume_prompt_builder import (
    ResumePromptBuilder,
)

from app.engine.ai.services.ai_writer import (
    AIWriter,
)

from app.engine.ai.services.ai_optimization_service import (
    AIOptimizationService,
)


logger = logging.getLogger(__name__)


class AIServiceFactory:
    """
    Creates configured AI optimization services.

    Flow:

        OpenRouterProvider
                |
                v
             AIWriter
                |
                v
      AIOptimizationService


    Responsibilities:

        - Wire AI dependencies.
        - Provide ready-to-use AI service.
        - Keep dependency creation centralized.


    Does NOT:

        - Execute optimization.
        - Build prompts.
        - Manage API requests.
    """



    @staticmethod
    def create() -> AIOptimizationService:
        """
        Create complete AI optimization service.
        """


        logger.info(
            "[AIServiceFactory] Creating AI service."
        )



        provider = (
            OpenRouterProvider()
        )


        parser = (
            AIResponseParser()
        )


        writer = AIWriter(

            provider=provider,

            parser=parser,

        )


        prompt_builder = (
            ResumePromptBuilder()
        )



        service = AIOptimizationService(

            ai_writer=writer,

            prompt_builder=prompt_builder,

        )



        logger.info(
            "[AIServiceFactory] AI service ready."
        )


        return service