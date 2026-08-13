"""
app.knowledge.services.skill_lookup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Skill lookup service used by the Resume Optimizer.

This service provides read-only access to skill knowledge.
"""

from __future__ import annotations

from app.knowledge.provider import get_knowledge


class SkillLookup:
    """
    Read-only skill lookup service.
    """

    @property
    def runtime(self):
        return get_knowledge()

    def get(
        self,
        skill_id: str,
    ) -> dict | None:
        """
        Return a skill by id.
        """
        return (
            self.runtime.knowledge.data
            .get("skill_index", {})
            .get("by_id", {})
            .get(skill_id)
        )

    def exists(
        self,
        skill_id: str,
    ) -> bool:
        """
        Return True if the skill exists.
        """
        return self.get(skill_id) is not None

    def all(self) -> dict[str, dict]:
        """
        Return every skill.
        """
        return (
            self.runtime.knowledge.data
            .get("skill_index", {})
            .get("by_id", {})
        )