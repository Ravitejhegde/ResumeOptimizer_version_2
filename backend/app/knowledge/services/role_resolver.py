"""
app.knowledge.services.role_resolver
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Runtime service for resolving roles.
"""

from __future__ import annotations

from app.knowledge.models.knowledge_model import KnowledgeModel


class RoleResolver:
    """
    Runtime service for resolving roles.
    """

    def __init__(
        self,
        knowledge: KnowledgeModel,
    ) -> None:
        self._knowledge = knowledge

    def all(self) -> list[dict]:
        """
        Return every role.
        """
        return list(
            self._knowledge.data
            .get("role_index", {})
            .get("by_id", {})
            .values()
        )

    def find_by_id(
        self,
        role_id: str,
    ) -> dict | None:
        """
        Find a role by its identifier.
        """
        return (
            self._knowledge.data
            .get("role_index", {})
            .get("by_id", {})
            .get(role_id)
        )

    def find_by_skill(
        self,
        skill_id: str,
    ) -> list[dict]:
        """
        Return every role associated with a skill.
        """
        return (
            self._knowledge.data
            .get("role_index", {})
            .get("by_skill", {})
            .get(skill_id, [])
        )

    def exists(
        self,
        role_id: str,
    ) -> bool:
        """
        Check whether a role exists.
        """
        return self.find_by_id(role_id) is not None