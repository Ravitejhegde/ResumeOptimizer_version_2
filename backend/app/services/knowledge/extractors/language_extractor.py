import re

from app.services.knowledge.models import ResumeSection


class LanguageExtractor:
    """
    Extracts spoken languages from resume.
    """

    SPLIT_PATTERN = re.compile(
        r"[,|;/•\n]+"
    )

    SECTION_NAMES = (
        "language",
        "languages",
    )

    @classmethod
    def extract(
        cls,
        sections: list[ResumeSection],
    ) -> list[str]:

        languages: list[str] = []

        for section in sections:

            title = section.title.lower()

            if not any(
                keyword in title
                for keyword in cls.SECTION_NAMES
            ):
                continue

            for paragraph in section.paragraphs:

                for part in cls.SPLIT_PATTERN.split(paragraph):

                    language = part.strip()

                    if (
                        language
                        and language not in languages
                    ):
                        languages.append(
                            language,
                        )

        return languages