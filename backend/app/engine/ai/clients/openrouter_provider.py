from __future__ import annotations

from openai import AsyncOpenAI

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
    OpenRouter LLM provider.

    Responsibilities:

        - Communicate with OpenRouter API.
        - Send chat completion requests.
        - Return raw AI response.

    Does NOT:

        - Build prompts.
        - Parse JSON.
        - Validate resume content.
    """



    def __init__(
        self,
    ) -> None:


        if not settings.OPENROUTER_API_KEY:

            raise AIConfigurationError(
                "OPENROUTER_API_KEY missing."
            )


        self.client = AsyncOpenAI(

            base_url=(
                "https://openrouter.ai/api/v1"
            ),

            api_key=(
                settings.OPENROUTER_API_KEY
            ),

            timeout=getattr(
                settings,
                "AI_TIMEOUT",
                120.0,
            ),

        )



    async def generate(
        self,
        messages: list[dict[str, str]],
    ) -> str:
        """
        Send request to OpenRouter.

        Returns:
            Raw AI JSON string.
        """



        logger.info(
            "[OpenRouter] Sending request."
        )



        try:

            response = await (
                self.client.chat.completions.create(

                    model=settings.OPENROUTER_MODEL,

                    messages=messages,

                    temperature=getattr(
                        settings,
                        "AI_TEMPERATURE",
                        0.2,
                    ),

                    max_tokens=getattr(
                        settings,
                        "AI_MAX_TOKENS",
                        4000,
                    ),

                    response_format={
                        "type": "json_object"
                    },

                )
            )


            logger.info(
                "[OpenRouter] Response received from API."
            )



        except Exception as exc:


            logger.exception(
                "[OpenRouter] Request failed."
            )


            raise AIRequestError(
                "OpenRouter request failed."
            ) from exc



        if not response.choices:

            raise AIResponseError(
                "Empty AI response."
            )



        content = (
            response
            .choices[0]
            .message
            .content
        )



        if not content:

            raise AIResponseError(
                "Empty content returned."
            )



        logger.info(
            "[OpenRouter] Content extracted successfully."
        )


        return content.strip()



    def name(
        self,
    ) -> str:

        return "OpenRouter"