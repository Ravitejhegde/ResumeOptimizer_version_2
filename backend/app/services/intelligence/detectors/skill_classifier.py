from app.services.intelligence.knowledge.engine import (
    KnowledgeEngine,
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

    @classmethod
    def classify(
        cls,
        technology: str,
        source: str = "resume",
    ) -> Skill:

        category_name = KnowledgeEngine.category(
            technology
        )

        try:

            category = SkillCategory(
                category_name.upper()
            )

        except Exception:

            try:

                category = SkillCategory[
                    category_name.upper()
                ]

            except Exception:

                category = SkillCategory.OTHER

        section = cls.SECTION_MAPPING.get(
            category,
            "Other",
        )

        return Skill(

            name=technology,

            category=category,

            section=section,

            source=source,

            confidence=1.0,

        )