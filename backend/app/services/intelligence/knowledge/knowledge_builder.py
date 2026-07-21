from app.services.intelligence.knowledge.resume_knowledge import (
    ResumeKnowledge,
)

from app.services.intelligence.knowledge.engine import (
    KnowledgeEngine,
)


class KnowledgeBuilder:
    """
    Builds ResumeKnowledge from DocumentSnapshot.
    """

    @classmethod
    def build(
        cls,
        snapshot,
    ) -> ResumeKnowledge:

        knowledge = ResumeKnowledge()

        all_text = "\n".join(
            paragraph.text
            for paragraph in snapshot.paragraphs
        )

        technologies = []

        for tech in KnowledgeEngine.technologies():

            name = tech["name"]

            if name.lower() in all_text.lower():

                technologies.append(name)

        knowledge.technologies = sorted(
            set(technologies)
        )

        knowledge.keywords = (
            knowledge.technologies.copy()
        )

        if snapshot.paragraphs:

            knowledge.summary = (
                snapshot.paragraphs[0].text
            )

        return knowledge