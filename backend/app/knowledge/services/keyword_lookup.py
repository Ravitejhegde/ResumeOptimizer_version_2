"""
app.knowledge.services.keyword_lookup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Keyword lookup service used by the Resume Optimizer.

This service provides read-only access to keyword knowledge.
"""

from __future__ import annotations

from app.knowledge.provider import get_knowledge


class KeywordLookup:
    """
    Read-only keyword lookup service.
    """

    @property
    def runtime(self):
        return get_knowledge()

    def get(
        self,
        keyword_id: str,
    ) -> dict | None:
        """
        Return a keyword by id.
        """
        return (
            self.runtime.knowledge.data
            .get("keyword_index", {})
            .get("by_id", {})
            .get(keyword_id)
        )

    def exists(
        self,
        keyword_id: str,
    ) -> bool:
        """
        Return True if the keyword exists.
        """
        return self.get(keyword_id) is not None

    def all(self) -> dict[str, dict]:
        """
        Return every keyword.
        """
        return (
            self.runtime.knowledge.data
            .get("keyword_index", {})
            .get("by_id", {})
        )