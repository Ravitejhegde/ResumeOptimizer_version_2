import os

from dotenv import load_dotenv
from google import genai

from .ai_provider import AIProvider
from .prompt_builder import PromptBuilder


load_dotenv()


class GeminiProvider(AIProvider):

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:

            raise ValueError(
                "GEMINI_API_KEY not found in .env"
            )

        self.client = genai.Client(api_key=api_key)

    def optimize_paragraph(
        self,
        paragraph: str,
        job_description: str,
    ) -> str:

        prompt = PromptBuilder.build(
            paragraph,
            job_description,
        )

        model = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash-lite",
        )

        response = self.client.models.generate_content(
            model=model,
            contents=prompt,
        )

        return response.text.strip()