from app.services.intelligence.skills.skills_models import (
    SkillCategoryGroup,
)


class LineBudget:
    """
    Ensures the optimized Skills section
    fits inside the original resume layout.
    """

    @classmethod
    def apply(
        cls,
        categories: list[SkillCategoryGroup],
        max_lines: int,
    ) -> list[SkillCategoryGroup]:

        if max_lines <= 0:
            return categories

        # -----------------------------------------
        # Count current lines
        #
        # One category = one line
        # Technologies are wrapped later by AI.
        # -----------------------------------------

        result = []
        used_lines = 0

        for category in categories:

            if not category.technologies:
                continue

            # one heading line
            if used_lines + 1 > max_lines:
                break

            result.append(category)

            used_lines += 1

        return result