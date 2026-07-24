from app.services.intelligence.skills.skills_models import (
    SkillCategoryGroup,
)


class CategoryBuilder:
    """
    Groups technologies into logical categories
    based on the target role.
    """

    CATEGORY_MAP = {

        "Backend Technologies": {
            "Python",
            "FastAPI",
            "Django",
            "Flask",
            "Node.js",
            "Express",
            "Spring Boot",
            "REST API",
            "REST APIs",
            "JWT",
            "JWT Authentication",
        },

        "Frontend Technologies": {
            "Angular",
            "React",
            "Vue",
            "Next.js",
            "HTML",
            "HTML5",
            "CSS",
            "CSS3",
            "JavaScript",
            "TypeScript",
            "Bootstrap",
            "Tailwind CSS",
        },

        "Database": {
            "MySQL",
            "PostgreSQL",
            "MongoDB",
            "SQL",
            "Redis",
        },

        "Cloud & DevOps": {
            "AWS",
            "Azure",
            "GCP",
            "Docker",
            "Kubernetes",
            "CI/CD",
            "GitHub Actions",
            "Jenkins",
        },

        "Programming Languages": {
            "Python",
            "Java",
            "C",
            "C++",
            "C#.net",
            "JavaScript",
            "TypeScript",
        },

        "Tools & Platforms": {
            "Git",
            "GitHub",
            "Postman",
            "Swagger",
            "Firebase",
            "VS Code",
        },
    }

    @classmethod
    def build(
        cls,
        technologies: list[str],
    ) -> list[SkillCategoryGroup]:

        groups = {}

        for technology in technologies:

            assigned = False

            for category, values in cls.CATEGORY_MAP.items():

                if technology in values:

                    groups.setdefault(
                        category,
                        []
                    ).append(
                        technology
                    )

                    assigned = True
                    break

            if not assigned:

                groups.setdefault(
                    "Other",
                    []
                ).append(
                    technology
                )

        result = []

        for category, values in groups.items():

            result.append(

                SkillCategoryGroup(

                    name=category,

                    technologies=sorted(
                        list(
                            dict.fromkeys(values)
                        )
                    ),

                )

            )

        return result