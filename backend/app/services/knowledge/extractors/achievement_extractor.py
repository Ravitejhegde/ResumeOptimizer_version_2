from app.services.knowledge.models import ResumeSection


class AchievementExtractor:
    """
    Extracts achievements, awards and recognitions.
    """

    SECTION_NAMES = (
        "achievement",
        "achievements",
        "award",
        "awards",
        "honor",
        "honors",
        "accomplishment",
    )

    @classmethod
    def extract(
        cls,
        sections: list[ResumeSection],
    ) -> list[str]:

        achievements: list[str] = []

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
                    and text not in achievements
                ):
                    achievements.append(
                        text,
                    )

        return achievements