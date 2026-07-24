from app.services.knowledge.models import ResumeSection


class EducationExtractor:
    """
    Extracts education entries from the resume.
    """

    SECTION_NAMES = (
        "education",
        "academic",
        "qualification",
    )

    @classmethod
    def extract(
        cls,
        sections: list[ResumeSection],
    ) -> list[str]:

        education: list[str] = []

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
                    and text not in education
                ):
                    education.append(
                        text,
                    )

        return education