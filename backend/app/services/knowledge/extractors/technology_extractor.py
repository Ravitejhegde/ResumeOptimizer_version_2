import re

from app.services.knowledge.models import ResumeSection


class TechnologyExtractor:
    """
    Extracts technologies from resume sections.

    Recognizes:
    - Technologies
    - Technical Skills
    - Tools
    - Frameworks
    """

    SPLIT_PATTERN = re.compile(
        r"[,|;/•\n]+"
    )

    SECTION_NAMES = (
        "technology",
        "technical",
        "tool",
        "framework",
        "platform",
    )

    @classmethod
    def extract(
        cls,
        sections: list[ResumeSection],
    ) -> list[str]:

        technologies: list[str] = []

        for section in sections:

            title = section.title.lower()

            if not any(
                keyword in title
                for keyword in cls.SECTION_NAMES
            ):
                continue

            for paragraph in section.paragraphs:

                for part in cls.SPLIT_PATTERN.split(paragraph):

                    tech = part.strip()

                    if (
                        tech
                        and tech not in technologies
                    ):
                        technologies.append(
                            tech,
                        )

        return technologies