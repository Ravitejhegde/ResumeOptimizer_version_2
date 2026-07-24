from app.services.intelligence.skills.skills_models import (
    SkillCategoryGroup,
)


class SkillsSectionParser:
    """
    Converts Skills paragraphs into
    SkillCategoryGroup objects.
    """

    @classmethod
    def parse(
        cls,
        paragraphs,
    ) -> list[SkillCategoryGroup]:

        categories = []

        for paragraph in paragraphs:

            text = paragraph.text.strip()

            if not text:
                continue

            if ":" not in text:
                continue

            name, technologies = text.split(
                ":",
                1,
            )

            category = SkillCategoryGroup(

                name=name.strip(),

                technologies=[

                    technology.strip()

                    for technology in technologies.split(",")

                    if technology.strip()

                ],

            )

            categories.append(
                category
            )

        return categories