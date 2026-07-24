import re

from app.services.knowledge.models import ResumeSection


class SkillsExtractor:
    """
    Extracts skills from the Skills section.
    """

    SPLIT_PATTERN = re.compile(
        r"[,|;/•\n]+"
    )

    @classmethod
    def extract(
        cls,
        sections: list[ResumeSection],
    ) -> list[str]:

        skills: list[str] = []

        for section in sections:

            title = section.title.lower()

            if "skill" not in title:
                continue

            for paragraph in section.paragraphs:

                parts = cls.SPLIT_PATTERN.split(
                    paragraph,
                )

                for part in parts:

                    skill = part.strip()

                    if skill and skill not in skills:

                        skills.append(
                            skill,
                        )

        return skills