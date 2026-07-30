from __future__ import annotations

from google import genai

from app.core.config import settings
from app.core.logger import logger

from .ai_provider import AIProvider
from .exceptions import (
    AIConfigurationError,
    AIRequestError,
    AIResponseError,
)


class GeminiProvider(AIProvider):
    """
    Gemini AI provider.

    Responsible only for:
        - Sending prompts to Gemini.
        - Returning raw responses.

    Does not:
        - Build prompts.
        - Parse JSON.
        - Optimize resumes.
    """


    def __init__(self) -> None:


        if not settings.GEMINI_API_KEY:

            raise AIConfigurationError(
                "GEMINI_API_KEY not found."
            )


        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )


    async def generate(
        self,
        prompt: str,
    ) -> str:


        logger.info(
            "Sending request to Gemini."
        )


        try:

            response = (
                await self.client.aio.models.generate_content(
                    model=settings.GEMINI_MODEL,
                    contents=prompt,
                )
            )


            logger.info(
                "Gemini response received."
            )


        except Exception as exc:

            logger.exception(
                "Gemini request failed."
            )


            raise AIRequestError(
                "Gemini request failed."
            ) from exc



        content = getattr(
            response,
            "text",
            None,
        )


        if not content:

            raise AIResponseError(
                "Gemini returned an empty response."
            )


        return content.strip()



    def name(
        self,
    ) -> str:

        return "Gemini"