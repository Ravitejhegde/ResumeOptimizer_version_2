from app.services.intelligence.skill import Skill

from app.services.knowledge.resume_knowledge import (
    ResumeKnowledge,
)

from app.services.jd.jd_knowledge import (
    JDKnowledge,
)


class KnowledgeConverter:

    @staticmethod
    def from_resume(
        knowledge: ResumeKnowledge,
    ) -> list[Skill]:

        skills: list[Skill] = []

        def convert(values: set[str], category: str):

            for value in values:

                skills.append(

                    Skill(

                        name=value,

                        category=category,

                        section="",

                        source="resume",

                    )

                )

        convert(knowledge.frontend, "frontend")
        convert(knowledge.backend, "backend")
        convert(knowledge.database, "database")
        convert(
            knowledge.programming_languages,
            "programming_languages",
        )
        convert(knowledge.cloud, "cloud")
        convert(knowledge.devops, "devops")
        convert(knowledge.tools, "tools")
        convert(knowledge.frameworks, "frameworks")
        convert(knowledge.testing, "testing")
        convert(knowledge.mobile, "mobile")
        convert(knowledge.other, "other")

        return skills

    @staticmethod
    def from_jd(
        knowledge: JDKnowledge,
    ) -> list[Skill]:

        skills: list[Skill] = []

        # Required skills
        for value in knowledge.required:

            skills.append(

                Skill(

                    name=value,

                    category="other",

                    section="",

                    source="jd",

                )

            )

        # Preferred skills
        for value in knowledge.preferred:

            skills.append(

                Skill(

                    name=value,

                    category="other",

                    section="",

                    source="jd",

                )

            )

        return skills