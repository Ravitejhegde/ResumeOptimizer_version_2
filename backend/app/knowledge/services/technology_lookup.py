"""
app.knowledge.services.technology_lookup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Technology lookup service used by the Resume Optimizer.

This service provides read-only access to technology knowledge.
"""

from __future__ import annotations

from app.knowledge.provider import get_knowledge


class TechnologyLookup:
    """
    Read-only technology lookup service.
    """

    @property
    def runtime(self):
        return get_knowledge()

    def get(
        self,
        technology_id: str,
    ) -> dict | None:
        """
        Return a technology by id.
        """
        return (
            self.runtime.knowledge.data
            .get("technology_graph", {})
            .get("nodes", {})
            .get(technology_id)
        )

    def exists(
        self,
        technology_id: str,
    ) -> bool:
        """
        Return True if the technology exists.
        """
        return self.get(technology_id) is not None

    def all(self) -> dict[str, dict]:
        """
        Return every technology.
        """
        return (
            self.runtime.knowledge.data
            .get("technology_graph", {})
            .get("nodes", {})
        )