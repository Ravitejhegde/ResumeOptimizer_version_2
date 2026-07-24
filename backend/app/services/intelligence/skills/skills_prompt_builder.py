from app.services.intelligence.skills.skills_models import (
    SkillCategoryGroup,
)


class SkillsPromptBuilder:
    """
    Builds the AI prompt for optimizing
    the Skills section.
    """

    @classmethod
    def build(
        cls,
        categories: list[SkillCategoryGroup],
        target_role: str,
        max_lines: int,
    ) -> str:

        prompt = f"""
You are an expert ATS Resume Writer.

TARGET ROLE

{target_role}

AVAILABLE LINES

{max_lines}

CURRENT SKILLS

"""

        for category in categories:

            prompt += f"""

{category.name}

{", ".join(category.technologies)}

"""
        prompt += """

TASK

Rewrite the Skills section for ATS optimization.

Rules

1. Prioritize technologies that appear in the Job Description.
2. Never remove core technologies already present in the resume if they are relevant.
3. Always keep the primary programming language if it matches the Job Description.
4. If FastAPI is included, Python must also be included.
5. Group technologies into professional categories.
6. Remove duplicates.
7. Do not invent technologies.
8. Keep approximately the same number of lines.
9. Return ONLY the Skills section.

"""
        

        return prompt