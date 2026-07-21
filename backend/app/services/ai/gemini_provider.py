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

    Responsible only for sending prompts
    to Gemini and returning the raw response.
    """

    def __init__(self):

        if not settings.GEMINI_API_KEY:
            raise AIConfigurationError(
                "GEMINI_API_KEY not found."
            )

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    def generate(
        self,
        prompt: str,
    ) -> str:

        logger.info(
            "Sending request to Gemini..."
        )

        try:

            response = self.client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
            )

            logger.info(
                "Gemini response received."
            )

        except Exception as e:

            logger.exception(
                "Gemini request failed."
            )

            raise AIRequestError(
                f"Gemini request failed: {e}"
            ) from e

        content = response.text

        if not content:

            raise AIResponseError(
                "Gemini returned an empty response."
            )

        return content.strip()