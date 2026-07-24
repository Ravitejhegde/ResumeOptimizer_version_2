from app.services.intelligence.skills.skills_models import (
    SkillCategoryGroup,
)


class SkillsUpdateBuilder:
    """
    Converts optimized skills into
    paragraph updates.
    """

    @classmethod
    def build(
        cls,
        paragraph_ids: list[str],
        categories: list[SkillCategoryGroup],
    ) -> dict[str, str]:

        updates = {}

        lines = []

        for category in categories:

            lines.append(

                f"{category.name}: "
                + ", ".join(category.technologies)

            )

        for index, paragraph_id in enumerate(
            paragraph_ids
        ):

            if index < len(lines):

                updates[paragraph_id] = lines[index]

            else:

                updates[paragraph_id] = ""

        return updates