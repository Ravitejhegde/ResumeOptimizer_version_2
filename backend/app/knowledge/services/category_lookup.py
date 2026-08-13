"""
app.knowledge.services.category_lookup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Category lookup service used by the Resume Optimizer.

This service provides read-only access to category knowledge.
"""

from __future__ import annotations

from app.knowledge.provider import get_knowledge


class CategoryLookup:
    """
    Read-only category lookup service.
    """

    @property
    def runtime(self):
        return get_knowledge()

    def get(
        self,
        category_id: str,
    ) -> dict | None:
        """
        Return a category by id.
        """
        return (
            self.runtime.knowledge.data
            .get("category_index", {})
            .get("by_id", {})
            .get(category_id)
        )

    def exists(
        self,
        category_id: str,
    ) -> bool:
        """
        Return True if the category exists.
        """
        return self.get(category_id) is not None

    def all(self) -> dict[str, dict]:
        """
        Return every category.
        """
        return (
            self.runtime.knowledge.data
            .get("category_index", {})
            .get("by_id", {})
        )