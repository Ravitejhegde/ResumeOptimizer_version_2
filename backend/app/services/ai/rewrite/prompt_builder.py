from __future__ import annotations

from app.services.ai.rewrite.rewrite_models import (
    RewriteRequest,
)


class PromptBuilder:
    """
    Builds prompts for resume rewriting.

    This class is responsible only for prompt
    generation. It never calls an AI provider.
    """

    @staticmethod
    def build(
        request: RewriteRequest,
    ) -> str:

        skills = ", ".join(
            request.selected_skills
        )

        return f"""
You are an expert ATS resume writer.

Rewrite the following resume paragraph.

Requirements:

- Preserve the original meaning.
- Improve clarity and professionalism.
- Naturally incorporate these technologies when relevant:
{skills}

- Do not invent experience.
- Do not add fake projects.
- Do not exaggerate achievements.
- Keep the paragraph under {request.max_words} words.
- Return ONLY the rewritten paragraph.
- Do not use markdown.
- Do not use bullet points unless the original paragraph already uses them.

Original Paragraph:

{request.paragraph}
""".strip()




