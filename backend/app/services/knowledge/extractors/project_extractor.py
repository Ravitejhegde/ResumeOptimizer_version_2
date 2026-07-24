from app.services.knowledge.models import ResumeSection


class ProjectExtractor:
    """
    Extracts project information from the resume.
    """

    SECTION_NAMES = (
        "project",
        "projects",
        "personal project",
        "academic project",
        "professional project",
    )

    @classmethod
    def extract(
        cls,
        sections: list[ResumeSection],
    ) -> list[str]:

        projects: list[str] = []

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
                    and text not in projects
                ):
                    projects.append(
                        text,
                    )

        return projects