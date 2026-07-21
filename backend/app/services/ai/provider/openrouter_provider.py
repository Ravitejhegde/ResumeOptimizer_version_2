import os

import requests

from app.services.ai.provider.ai_provider import (
    AIProvider,
)


class OpenRouterProvider(AIProvider):
    """
    OpenRouter AI Provider.
    """

    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

    DEFAULT_MODEL = (
        "openai/gpt-4.1-mini"
    )

    def __init__(self):

        self.api_key = os.getenv(
            "OPENROUTER_API_KEY"
        )

        if not self.api_key:

            raise ValueError(
                "OPENROUTER_API_KEY not found."
            )

    def generate(
        self,
        prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 1500,
        model: str | None = None,
    ) -> str:

        model = model or self.DEFAULT_MODEL

        headers = {

            "Authorization":
                f"Bearer {self.api_key}",

            "Content-Type":
                "application/json",

        }

        payload = {

            "model": model,

            "temperature": temperature,

            "max_tokens": max_tokens,

            "messages": [

                {

                    "role": "user",

                    "content": prompt,

                }

            ],

        }

        response = requests.post(

            self.BASE_URL,

            headers=headers,

            json=payload,

            timeout=120,

        )

        response.raise_for_status()

        data = response.json()

        return (

            data["choices"][0]

            ["message"]

            ["content"]

            .strip()

        )