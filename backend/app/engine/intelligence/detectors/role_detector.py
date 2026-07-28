from __future__ import annotations

from app.engine.models.analysis.analysis_result import (
    AnalysisResult,
)
from app.engine.models.intelligence.role_profile import (
    RoleProfile,
)
from app.knowledge.knowledge_manager import (
    KnowledgeManager,
)


class RoleDetector:
    """
    Detects the most appropriate role using
    the Knowledge Platform.
    """

    def __init__(
        self,
        knowledge: KnowledgeManager,
    ) -> None:

        self._knowledge = knowledge

    # --------------------------------------------------

    def detect(
        self,
        analysis: AnalysisResult,
    ) -> RoleProfile | None:

        role_id = (
            analysis.job_description.role
            or analysis.keywords.normalized[0]
            if analysis.keywords.normalized
            else None
        )

        if role_id is None:

            return None

        data = self._knowledge.role(
            role_id,
        )

        if data is None:

            return None

        return RoleProfile(

            id=data["id"],

            name=data["name"],

            confidence=1.0,

            category=data.get(
                "category",
            ),

            required_skills=data.get(
                "required_skills",
                [],
            ),

            optional_skills=data.get(
                "optional_skills",
                [],
            ),

            related_roles=data.get(
                "related_roles",
                [],
            ),

        )
