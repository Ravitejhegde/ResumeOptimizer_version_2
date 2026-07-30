from __future__ import annotations

import logging

from app.engine.ai.clients.ai_provider import (
    AIProvider,
)

from app.engine.ai.models.ai_prompt import (
    AIPrompt,
)

from app.engine.ai.models.ai_response import (
    AIOptimizationResponse,
)

from app.engine.ai.parsers.ai_response_parser import (
    AIResponseParser,
)


logger = logging.getLogger(__name__)



class AIWriter:
    """
    Coordinates AI resume optimization.

    Pipeline:

        OptimizationContext
                |
                v
        ResumePromptBuilder
                |
                v
             AIPrompt
                |
                v
        AIProvider(OpenRouter)
                |
                v
          Raw JSON Response
                |
                v
        AIResponseParser
                |
                v
     AIOptimizationResponse


    Responsibilities:

        - Make exactly ONE AI API call.
        - Send structured messages.
        - Parse AI response.


    Does NOT:

        - Build prompts.
        - Modify DOCX.
        - Validate document.
    """



    def __init__(
        self,
        provider: AIProvider,
        parser: AIResponseParser,
    ) -> None:

        self._provider = provider

        self._parser = parser



    async def optimize(
        self,
        prompt: AIPrompt,
    ) -> AIOptimizationResponse:
        """
        Execute single AI optimization request.
        """


        if not prompt.has_messages():

            raise ValueError(
                "AI prompt is empty."
            )



        logger.info(
            "[AIWriter] "
            "Sending single AI request."
        )



        # ----------------------------------
        # ONE AND ONLY AI CALL
        # ----------------------------------

        raw_response = await (

            self._provider.generate(

                prompt.messages

            )

        )
        logger.info(
    "[AIWriter] RAW RESPONSE:\n%s",
    raw_response,
)



        logger.info(
            "[AIWriter] "
            "AI response received."
        )



        # ----------------------------------
        # Parse AI JSON response
        # ----------------------------------

        result = (

            self._parser.parse(

                raw_response

            )

        )



        logger.info(
            "[AIWriter] "
            "Response parsed successfully."
        )


        return result