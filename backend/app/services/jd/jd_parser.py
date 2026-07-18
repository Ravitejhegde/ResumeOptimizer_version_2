from app.services.knowledge.technology_classifier import (
    TechnologyClassifier,
)

from .jd_knowledge import JDKnowledge


class JDParser:

    @staticmethod
    def parse(
        job_description: str,
    ) -> JDKnowledge:

        knowledge = JDKnowledge()

        jd = job_description.lower()

        technologies = (
            TechnologyClassifier.get_all()
        )

        for technology in technologies:

            if technology in jd:

                knowledge.required.add(
                    technology
                )

        return knowledge