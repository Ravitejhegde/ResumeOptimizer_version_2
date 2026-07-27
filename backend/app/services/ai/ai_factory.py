from app.core.config import settings
from app.services.ai.gemini_provider import GeminiProvider
from app.services.ai.openrouter_provider import OpenRouterProvider


class AIFactory:

    @staticmethod
    def create():

        if settings.AI_PROVIDER == "gemini":
            return GeminiProvider()

        return OpenRouterProvider()




