from .prompts import (
    SUMMARY_PROMPT,
    EXPERIENCE_PROMPT,
    PROJECT_PROMPT,
    SKILLS_PROMPT,
    EDUCATION_PROMPT,
)

PROMPTS = {
    "SUMMARY": SUMMARY_PROMPT,
    "PROFILE": SUMMARY_PROMPT,
    "EXPERIENCE": EXPERIENCE_PROMPT,
    "WORK EXPERIENCE": EXPERIENCE_PROMPT,
    "PROJECTS": PROJECT_PROMPT,
    "PROJECT": PROJECT_PROMPT,
    "SKILLS": SKILLS_PROMPT,
    "TECHNICAL SKILLS": SKILLS_PROMPT,
    "EDUCATION": EDUCATION_PROMPT,
}


class SectionOptimizer:

    def get_prompt(self, section_title: str) -> str:
        return PROMPTS.get(
            section_title.upper(),
            "Improve this resume section while preserving factual accuracy."
        )