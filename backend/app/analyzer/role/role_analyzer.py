"""
app.analyzer.role.role_analyzer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Infers engineering roles from detected skills.
"""

from __future__ import annotations

from app.analyzer.contracts.role_analyzer_contract import (
    RoleAnalyzerContract,
)
from app.analyzer.models.document_model import (
    DocumentModel,
)
from app.analyzer.models.role_model import (
    RoleModel,
)
from app.analyzer.role.role_detector import (
    RoleDetector,
)
from app.knowledge.provider import (
    get_knowledge,
)


class RoleAnalyzer(RoleAnalyzerContract):
    """
    Infers engineering roles using the Knowledge Runtime.
    """

    def __init__(self) -> None:
        self._runtime = get_knowledge()
        self._detector = RoleDetector()

    def analyze(
        self,
        document: DocumentModel,
    ) -> DocumentModel:
        """
        Populate document.roles from detected skills.
        """

        document.roles.clear()

        role_ids = self._detector.detect(
            set(document.skills.keys())
        )

        for role_id in role_ids:

            role = self._runtime.roles.find_by_id(
                role_id
            )

            if role is None:
                continue

            required_skills = set(
                role.get(
                    "required_skill_ids",
                    [],
                )
            )

            matched_skills = (
                required_skills
                & set(document.skills.keys())
            )

            confidence = (
                len(matched_skills)
                / len(required_skills)
                if required_skills
                else 0.0
            )

            model = RoleModel(
                id=role["id"],
                name=role["name"],
                confidence=confidence,
                matched_skills=matched_skills,
            )

            for skill_id in matched_skills:
                model.sections.update(
                    document.skills[
                        skill_id
                    ].sections
                )

            document.roles[
                model.id
            ] = model

        return document