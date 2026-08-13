"""
app.knowledge.services.role_lookup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Role lookup service used by the Resume Optimizer.

This service provides read-only access to role knowledge.
"""

from __future__ import annotations

from app.knowledge.provider import get_knowledge


class RoleLookup:
    """
    Read-only role lookup service.
    """

    @property
    def runtime(self):
        return get_knowledge()

    def get(
        self,
        role_id: str,
    ) -> dict | None:
        """
        Return a role by id.
        """
        return (
            self.runtime.knowledge.data
            .get("role_index", {})
            .get("by_id", {})
            .get(role_id)
        )

    def exists(
        self,
        role_id: str,
    ) -> bool:
        """
        Return True if the role exists.
        """
        return self.get(role_id) is not None

    def all(self) -> dict[str, dict]:
        """
        Return every role.
        """
        return (
            self.runtime.knowledge.data
            .get("role_index", {})
            .get("by_id", {})
        )