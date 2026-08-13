"""
app.knowledge.services.technology_resolver
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Runtime service for resolving technologies.
"""

from __future__ import annotations

from app.knowledge.models.knowledge_model import KnowledgeModel


class TechnologyResolver:
    """
    Runtime service for resolving technologies.
    """

    def __init__(
        self,
        knowledge: KnowledgeModel,
    ) -> None:
        self._knowledge = knowledge

    @property
    def _nodes(self) -> dict[str, dict]:
        """
        Return technology graph nodes.
        """
        return (
            self._knowledge.data
            .get("technology_graph", {})
            .get("nodes", {})
        )

    def all(self) -> list[dict]:
        """
        Return every technology.
        """
        return list(self._nodes.values())

    def find_by_id(
        self,
        technology_id: str,
    ) -> dict | None:
        """
        Find a technology by its identifier.
        """
        return self._nodes.get(
            technology_id
        )

    def exists(
        self,
        technology_id: str,
    ) -> bool:
        """
        Check whether a technology exists.
        """
        return technology_id in self._nodes

    def related(
        self,
        technology_id: str,
    ) -> list[dict]:
        """
        Return technologies related to the supplied technology.
        """
        technology = self.find_by_id(
            technology_id
        )

        if technology is None:
            return []

        related_ids = technology.get(
            "related",
            [],
        )

        return [
            self.find_by_id(item)
            for item in related_ids
            if self.find_by_id(item) is not None
        ]

    def skills(
        self,
        technology_id: str,
    ) -> list[dict]:
        """
        Return skills associated with a technology.
        """
        return (
            self._knowledge.data
            .get("skill_index", {})
            .get("by_technology", {})
            .get(
                technology_id,
                [],
            )
        )

    def roles(
        self,
        technology_id: str,
    ) -> list[dict]:
        """
        Return roles that require this technology.
        """
        roles = []

        skill_ids = {
            skill["id"]
            for skill in self.skills(
                technology_id
            )
        }

        role_index = (
            self._knowledge.data
            .get("role_index", {})
        )

        by_id = role_index.get(
            "by_id",
            {},
        )

        for role in by_id.values():

            required = set(
                role.get(
                    "required_skill_ids",
                    [],
                )
            )

            if required & skill_ids:
                roles.append(role)

        return roles
    