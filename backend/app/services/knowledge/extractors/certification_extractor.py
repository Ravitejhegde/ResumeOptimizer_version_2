from app.services.knowledge.models import ResumeSection


class CertificationExtractor:
    """
    Extracts certifications from resume.
    """

    SECTION_NAMES = (
        "certification",
        "certifications",
        "certificate",
        "licenses",
        "license",
    )

    @classmethod
    def extract(
        cls,
        sections: list[ResumeSection],
    ) -> list[str]:

        certifications: list[str] = []

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
                    and text not in certifications
                ):
                    certifications.append(
                        text,
                    )

        return certifications