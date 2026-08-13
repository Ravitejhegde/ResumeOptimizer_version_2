"""
app.analyzer.role.role_detector
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Detect candidate roles from detected skills using the Knowledge Runtime.
"""

from __future__ import annotations

from app.knowledge.provider import (
    get_knowledge,
)


class RoleDetector:
    """
    Detects candidate roles from detected skills.
    """

    def __init__(self) -> None:
        self._lookup = get_knowledge().roles

    def detect(
        self,
        skill_ids: set[str],
    ) -> list[str]:
        """
        Detect role IDs associated with the supplied skills.

        Returns a sorted list to ensure deterministic ordering.
        """

        detected: set[str] = set()

        for skill_id in skill_ids:

            for role in self._lookup.find_by_skill(
                skill_id
            ):
                detected.add(
                    role["id"]
                )

        return sorted(detected)