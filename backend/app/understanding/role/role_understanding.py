"""
app.understanding.role.role_understanding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Determines the primary and secondary roles of a resume.
"""

from __future__ import annotations

from app.analyzer.models.document_model import (
    DocumentModel,
)
from app.knowledge.provider import (
    get_knowledge,
)
from app.understanding.models.resume_understanding import (
    ResumeUnderstanding,
)


class RoleUnderstanding:
    """
    Determines role-related understanding.
    """

    def __init__(self) -> None:
        self._roles = get_knowledge().roles

    def analyze(
        self,
        document: DocumentModel,
        understanding: ResumeUnderstanding,
    ) -> ResumeUnderstanding:

        if not document.roles:
            return understanding

        def sort_key(role):
            data = self._roles.find_by_id(role.id)

            importance = 0

            if data is not None:
                importance = data.get(
                    "importance",
                    0,
                )

            return (
                role.confidence,
                importance,
                len(role.matched_skills),
                role.name,
            )

        roles = sorted(
            document.roles.values(),
            key=sort_key,
            reverse=True,
        )

        understanding.primary_role = (
            roles[0].name
        )

        understanding.secondary_roles = [
            role.name
            for role in roles[1:]
        ]

        return understanding