from openai import OpenAI

from app.core.config import settings
from app.core.logger import logger
from .ai_provider import AIProvider
from .exceptions import (
    AIConfigurationError,
    AIRequestError,
    AIResponseError,
)


class OpenRouterProvider(AIProvider):
    """
    OpenRouter AI provider.

    Responsible only for sending prompts
    to OpenRouter and returning the raw response.
    """

    def __init__(self):

        if not settings.OPENROUTER_API_KEY:
            raise AIConfigurationError(
                "OPENROUTER_API_KEY not found."
            )

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.OPENROUTER_API_KEY,
        )

    def generate(
        self,
        prompt: str,
    ) -> str:
        logger.info(
        "Sending request to OpenRouter..."
    )

        try:

            response = self.client.chat.completions.create(
                model=settings.OPENROUTER_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )
            logger.info(
    "OpenRouter response received."
)
        except Exception as e:

            logger.exception(
                "OpenRouter request failed."
        )

            raise AIRequestError(
            f"OpenRouter request failed: {e}"
            ) from e

        content = response.choices[0].message.content

        if not content:

            raise AIResponseError(
                "OpenRouter returned an empty response."
            )

        return content.strip()