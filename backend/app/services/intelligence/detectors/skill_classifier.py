from app.services.intelligence.constants import (
    TECHNOLOGY_CATEGORY,
)

from app.services.intelligence.models import (
    Skill,
    SkillCategory,
)


class SkillClassifier:

    SECTION_MAPPING = {

        SkillCategory.PROGRAMMING:
            "Programming Languages",

        SkillCategory.FRONTEND:
            "Frontend Technologies",

        SkillCategory.BACKEND:
            "Backend Technologies",

        SkillCategory.DATABASE:
            "Databases",

        SkillCategory.FRAMEWORK:
            "Frameworks",

        SkillCategory.DEVOPS:
            "DevOps",

        SkillCategory.CLOUD:
            "Cloud",

        SkillCategory.TESTING:
            "Testing",

        SkillCategory.TOOLS:
            "Tools & Platforms",

        SkillCategory.MOBILE:
            "Mobile",

        SkillCategory.AI:
            "Artificial Intelligence",

        SkillCategory.SOFT:
            "Soft Skills",

        SkillCategory.OTHER:
            "Other",

    }

    @staticmethod
    def classify(
        technology: str,
        source: str = "resume",
    ) -> Skill:

        key = technology.lower().strip()

        category = TECHNOLOGY_CATEGORY.get(
            key,
            SkillCategory.OTHER,
        )

        section = SkillClassifier.SECTION_MAPPING[
            category
        ]

        return Skill(

            name=technology,

            category=category,

            section=section,

            source=source,
        )