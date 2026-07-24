from app.services.ai.provider.openrouter_provider import (
    OpenRouterProvider,
)

provider = OpenRouterProvider()

response = provider.generate(
    "Reply with exactly: OpenRouter OK"
)

print(response)