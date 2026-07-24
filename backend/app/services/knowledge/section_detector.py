from app.services.knowledge.models import ResumeSection
from app.services.parser.models import ResumeDocument


class SectionDetector:
    """
    Detects logical resume sections
    from parsed paragraphs.
    """

    DEFAULT_HEADINGS = {
        "summary",
        "professional summary",
        "profile",
        "skills",
        "technical skills",
        "experience",
        "work experience",
        "professional experience",
        "employment",
        "education",
        "projects",
        "certifications",
        "languages",
        "achievements",
        "interests",
    }

    @staticmethod
    def detect(
        document: ResumeDocument,
    ) -> list[ResumeSection]:

        sections: list[ResumeSection] = []

        current_section: ResumeSection | None = None

        for paragraph in document.paragraphs:

            text = paragraph.text.strip()

            if not text:
                continue

            normalized = text.lower().rstrip(":")

            if (
                paragraph.is_heading
                or normalized in SectionDetector.DEFAULT_HEADINGS
            ):

                current_section = ResumeSection(
                    title=text,
                )

                sections.append(
                    current_section,
                )

                continue

            if current_section is None:

                current_section = ResumeSection(
                    title="General",
                )

                sections.append(
                    current_section,
                )

            current_section.paragraphs.append(
                text,
            )

        return sections