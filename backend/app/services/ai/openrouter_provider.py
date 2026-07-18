import os

from dotenv import load_dotenv
from openai import OpenAI

from .ai_provider import AIProvider
from .prompt_builder import PromptBuilder

load_dotenv()


class OpenRouterProvider(AIProvider):

    def __init__(self):

        api_key = os.getenv("OPENROUTER_API_KEY")

        print("OPENROUTER_API_KEY =", api_key)

        if not api_key:
            raise ValueError(
                "OPENROUTER_API_KEY not found in .env"
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

        return response.choices[0].message.content.strip()

    def optimize_paragraph(
        self,
        paragraph: str,
        job_description: str,
    ) -> str:

        prompt = PromptBuilder.build(
            paragraph,
            job_description,
        )

        return  self.generate(prompt)