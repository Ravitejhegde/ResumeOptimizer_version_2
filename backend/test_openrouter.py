from app.services.ai.openrouter_provider import OpenRouterProvider

provider = OpenRouterProvider()

paragraph = (
    "Developed REST APIs using Spring Boot."
)

job_description = """
Looking for a Java Backend Developer.

Skills:
Java
Spring Boot
REST API
Docker
AWS
"""

result = provider.optimize_paragraph(
    paragraph,
    job_description,
)

print("=" * 60)
print(result)