import os

from dotenv import load_dotenv
from google import genai

from .ai_provider import AIProvider

load_dotenv()


class GeminiProvider(AIProvider):
    """
    Gemini AI provider.

    Responsible only for sending prompts
    to Gemini and returning the raw response.
    """

    def __init__(self):

        api_key = os.getenv(
            "GEMINI_API_KEY"
        )

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found."
            )

        self.client = genai.Client(
            api_key=api_key
        )

    def generate(
        self,
        prompt: str,
    ) -> str:

        model = os.getenv(

            "GEMINI_MODEL",

            "gemini-2.5-flash-lite",

        )

        response = self.client.models.generate_content(

            model=model,

            contents=prompt,

        )

        return response.text.strip()