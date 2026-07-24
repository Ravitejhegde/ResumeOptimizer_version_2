import os
import time

import requests

from dotenv import load_dotenv

from app.services.ai.provider.ai_provider import (
    AIProvider,
)

load_dotenv()


class OpenRouterProvider(AIProvider):
    """
    OpenRouter AI Provider.

    Features
    --------
    - Retry logic
    - Timeout protection
    - JSON response mode
    - Better error handling
    - Configurable model
    """

    BASE_URL = (
        "https://openrouter.ai/api/v1/chat/completions"
    )

    DEFAULT_MODEL = "openai/gpt-4.1-mini"

    MAX_RETRIES = 3

    RETRY_DELAY = 2

    TIMEOUT = 180

    def __init__(self):

        self.api_key = os.getenv(
            "OPENROUTER_API_KEY"
        )

        if not self.api_key:

            raise RuntimeError(
                "OPENROUTER_API_KEY is missing.\n"
                "Create backend/.env and add:\n"
                "OPENROUTER_API_KEY=your_key"
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

            "Authorization": (
                f"Bearer {self.api_key}"
            ),

            "Content-Type": "application/json",

            # Recommended by OpenRouter
            "HTTP-Referer": (
                "http://localhost:5173"
            ),

            "X-Title": (
                "Resume Optimizer"
            ),

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

        last_error = None

        for attempt in range(
            1,
            self.MAX_RETRIES + 1,
        ):

            response = None

            try:

                response = requests.post(

                    self.BASE_URL,

                    headers=headers,

                    json=payload,

                    timeout=self.TIMEOUT,

                )

                response.raise_for_status()

                data = response.json()

                content = (

                    data

                    .get("choices", [{}])[0]

                    .get("message", {})

                    .get("content", "")

                )

                if not content:

                    raise RuntimeError(
                        "AI returned an empty response."
                    )

                return content.strip()

            except requests.RequestException as e:

                last_error = e

                print()

                print("=" * 60)

                print(
                    f"OpenRouter Retry "
                    f"{attempt}/{self.MAX_RETRIES}"
                )

                if response is not None:

                    try:

                        print(
                            response.status_code
                        )

                        print(
                            response.text
                        )

                    except Exception:

                        print(e)

                else:

                    print(e)

                print("=" * 60)

                if attempt < self.MAX_RETRIES:

                    time.sleep(
                        self.RETRY_DELAY
                    )

        raise RuntimeError(

            "OpenRouter request failed after "

            f"{self.MAX_RETRIES} attempts."

        ) from last_error