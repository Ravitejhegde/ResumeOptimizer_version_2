"""
app.ai.client.openrouter_client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Production-ready OpenRouter client.
"""

from __future__ import annotations

import time

import requests

from app.ai.client.ai_client import (
    AIClient,
)
from app.core.config.settings import (
    settings,
)


class OpenRouterClient(AIClient):
    """
    OpenRouter implementation of AIClient.
    """

    BASE_URL = (
        "https://openrouter.ai/api/v1/chat/completions"
    )

    def __init__(self) -> None:

        self._api_key = (
            settings.OPENROUTER_API_KEY
        )

        self._model = (
            settings.OPENROUTER_MODEL
        )

        self._timeout = (
            settings.AI_TIMEOUT
        )

        self._max_retries = (
            settings.AI_MAX_RETRIES
        )

        self._temperature = (
            settings.AI_TEMPERATURE
        )

        self._max_tokens = (
            settings.AI_MAX_TOKENS
        )

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate text using OpenRouter.
        """

        payload = {
            "model": self._model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "temperature": self._temperature,
            "max_tokens": self._max_tokens,
        }

        headers = {
            "Authorization": (
                f"Bearer {self._api_key}"
            ),
            "Content-Type": (
                "application/json"
            ),
        }

        last_error: Exception | None = None

        for _ in range(
            self._max_retries + 1
        ):

            try:

                response = requests.post(
                    self.BASE_URL,
                    json=payload,
                    headers=headers,
                    timeout=self._timeout,
                )

                if not response.ok:
                    raise RuntimeError(
                        f"{response.status_code}: {response.text}"
                    )

                data = response.json()

                print("\n========== OPENROUTER RAW RESPONSE ==========")
                print(data)
                print("============================================\n")

                return (
                    data["choices"][0]
                    ["message"]["content"]
                    .strip()
                )

            except Exception as exc:

                last_error = exc

                time.sleep(1)

        raise RuntimeError(
            "OpenRouter request failed."
        ) from last_error