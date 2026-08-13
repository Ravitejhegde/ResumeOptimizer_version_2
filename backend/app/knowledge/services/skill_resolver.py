"""
app.knowledge.services.skill_resolver
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Runtime service for resolving skills.
"""

from __future__ import annotations

from app.knowledge.models.knowledge_model import KnowledgeModel


class SkillResolver:
    """
    Runtime service for resolving skills.
    """

    def __init__(
        self,
        knowledge: KnowledgeModel,
    ) -> None:
        self._knowledge = knowledge

    def all(self) -> list[dict]:
        """
        Return every skill.
        """
        return list(
            self._knowledge.data
            .get("skill_index", {})
            .get("by_id", {})
            .values()
        )

    def find_by_id(
        self,
        skill_id: str,
    ) -> dict | None:
        """
        Find a skill by its identifier.
        """
        return (
            self._knowledge.data
            .get("skill_index", {})
            .get("by_id", {})
            .get(skill_id)
        )

    def find_by_technology(
        self,
        technology_id: str,
    ) -> list[dict]:
        """
        Return all skills associated with a technology.
        """
        return (
            self._knowledge.data
            .get("skill_index", {})
            .get("by_technology", {})
            .get(technology_id, [])
        )

    def exists(
        self,
        skill_id: str,
    ) -> bool:
        """
        Check whether a skill exists.
        """
        return self.find_by_id(skill_id) is not None