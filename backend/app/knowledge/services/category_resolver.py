"""
app.knowledge.services.category_resolver
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Runtime service for resolving categories.
"""

from __future__ import annotations

from app.knowledge.models.knowledge_model import KnowledgeModel


class CategoryResolver:
    """
    Runtime service for resolving categories.
    """

    def __init__(
        self,
        knowledge: KnowledgeModel,
    ) -> None:
        self._knowledge = knowledge

    def all(self) -> list[dict]:
        """
        Return every category.
        """
        return self._knowledge.get("categories", [])

    def find_by_id(
        self,
        category_id: str,
    ) -> dict | None:
        """
        Find a category by its identifier.
        """
        for category in self.all():
            if category.get("id") == category_id:
                return category

        return None

    def exists(
        self,
        category_id: str,
    ) -> bool:
        """
        Check whether a category exists.
        """
        return self.find_by_id(category_id) is not None