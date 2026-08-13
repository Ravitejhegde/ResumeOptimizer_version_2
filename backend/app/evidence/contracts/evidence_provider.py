"""
app.evidence.contracts.evidence_provider
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Provides evidence relationships from the Knowledge Platform.
"""

from __future__ import annotations

from typing import Protocol


class EvidenceProvider(Protocol):
    """
    Contract implemented by the Knowledge Platform.
    """

    def required_skills_for_technology(
        self,
        technology_id: str,
    ) -> list[str]:
        ...

    def required_technologies_for_skill(
        self,
        skill_id: str,
    ) -> list[str]:
        ...

    def related_skills(
        self,
        skill_id: str,
    ) -> list[str]:
        ...