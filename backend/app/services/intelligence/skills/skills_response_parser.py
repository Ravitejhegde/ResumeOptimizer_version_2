import re

from app.services.intelligence.skills.skills_models import (
    SkillCategoryGroup,
)


class SkillsResponseParser:
    """
    Parses AI-generated Skills sections.

    Supports both plain text and Markdown output.
    """

    @classmethod
    def parse(
        cls,
        response: str,
    ) -> list[SkillCategoryGroup]:

        categories = []

        current = None

        for line in response.splitlines():

            line = line.strip()

            if not line:
                continue

            # Remove Markdown formatting
            line = re.sub(r"\*\*", "", line).strip()

            # Ignore standalone title
            if line.lower() == "skills":
                continue

            # Category
            if ":" in line:

                name, values = line.split(":", 1)

                current = SkillCategoryGroup(
                    name=name.strip(),
                    technologies=[],
                )

                technologies = [
                    item.strip()
                    for item in values.split(",")
                    if item.strip()
                ]

                current.technologies.extend(technologies)

                categories.append(current)

                continue

        return categories