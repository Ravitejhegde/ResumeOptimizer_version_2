from app.services.intelligence.skill import Skill


class SectionAllocator:

    SECTION_MAP = {

        "frontend": "Frontend Technologies",

        "backend": "Backend Technologies",

        "database": "Databases",

        "programming_languages": "Programming Languages",

        "cloud": "Cloud",

        "devops": "DevOps",

        "tools": "Tools & Platforms",

        "frameworks": "Frameworks",

        "testing": "Testing",

        "mobile": "Mobile",

        "other": "Other Skills",

    }

    @classmethod
    def allocate(

        cls,

        skills: list[Skill],

    ) -> list[Skill]:

        for skill in skills:

            skill.section = cls.SECTION_MAP.get(

                skill.category,

                "Other Skills",

            )

        return skills