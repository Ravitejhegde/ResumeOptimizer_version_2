from .base import BaseAIProvider


class OpenAIProvider(BaseAIProvider):

    def optimize_section(
        self,
        prompt: str,
        section_content: str,
        job_description: str,
    ) -> str:

        # Temporary implementation.
        # Replace this with a real LLM call later.

        return section_content