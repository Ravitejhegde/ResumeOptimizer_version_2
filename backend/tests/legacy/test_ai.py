from app.services.ai.prompt_builder import PromptBuilder
from backend.app._legacy.services.ai.gemini_provider import GeminiProvider

paragraph = (
    "Developed REST APIs using Spring Boot."
)

jd = (
    "Looking for Java and Spring Boot developer."
)

prompt = PromptBuilder.build(
    paragraph,
    jd,
)

print("=" * 60)
print(prompt)

provider = GeminiProvider()

print("=" * 60)

print(

    provider.optimize_paragraph(

        paragraph,

        jd,

    )

)