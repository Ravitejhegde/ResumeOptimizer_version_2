from app.services.knowledge.models import ResumeSection


class ExperienceExtractor:
    """
    Extracts work experience from resume.
    """

    SECTION_NAMES = (
        "experience",
        "employment",
        "work history",
        "professional experience",
    )

    @classmethod
    def extract(
        cls,
        sections: list[ResumeSection],
    ) -> list[str]:

        experiences: list[str] = []

        for section in sections:

            title = section.title.lower()

            if not any(
                keyword in title
                for keyword in cls.SECTION_NAMES
            ):
                continue

            for paragraph in section.paragraphs:

                text = paragraph.strip()

                if (
                    text
                    and text not in experiences
                ):
                    experiences.append(
                        text,
                    )

        return experiences