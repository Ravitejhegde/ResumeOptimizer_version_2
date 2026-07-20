import os

from dotenv import load_dotenv
from openai import OpenAI

from .ai_provider import AIProvider

load_dotenv()


class OpenRouterProvider(AIProvider):
    """
    OpenRouter AI provider.

    Responsible only for sending prompts
    to OpenRouter and returning the raw response.
    """

    def __init__(self):

        api_key = os.getenv(
            "OPENROUTER_API_KEY"
        )

        if not api_key:
            raise ValueError(
                "OPENROUTER_API_KEY not found."
            )

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

    def generate(
        self,
        prompt: str,
    ) -> str:

        model = os.getenv(
            "OPENROUTER_MODEL",
            "deepseek/deepseek-chat-v3-0324",
        )

        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        content = response.choices[0].message.content

        if not content:
            raise RuntimeError(
                "OpenRouter returned an empty response."
            )

        return content.strip()