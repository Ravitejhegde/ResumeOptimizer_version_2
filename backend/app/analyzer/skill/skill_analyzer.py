"""
app.analyzer.skill.skill_analyzer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Infers engineering skills from detected technologies.
"""

from __future__ import annotations

from app.analyzer.contracts.skill_analyzer_contract import (
    SkillAnalyzerContract,
)
from app.analyzer.models.document_model import (
    DocumentModel,
)
from app.analyzer.models.skill_model import (
    SkillModel,
)
from app.knowledge.provider import (
    get_knowledge,
)


class SkillAnalyzer(SkillAnalyzerContract):
    """
    Infers skills using the Knowledge Runtime.
    """

    def __init__(self) -> None:
        self._runtime = get_knowledge()

    def analyze(
        self,
        document: DocumentModel,
    ) -> DocumentModel:

        for technology in document.technologies.values():

            skills = (
                self._runtime.skills
                .find_by_technology(
                    technology.id
                )
            )

            for skill in skills:

                skill_id = skill["id"]

                if skill_id not in document.skills:

                    document.skills[skill_id] = SkillModel(
                        id=skill_id,
                        name=skill["name"],
                        description=skill.get(
                            "description",
                            "",
                        ),
                        importance=skill.get(
                            "importance",
                            0,
                        ),
                    )

                document.skills[
                    skill_id
                ].technologies.add(
                    technology.id
                )

                document.skills[
                    skill_id
                ].sections.add(
                    technology.section
                )

        return document