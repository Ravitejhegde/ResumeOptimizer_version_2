"""
app.analyzer.models.technology_model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents a technology detected in a resume.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class TechnologyModel:
    """
    A detected technology.
    """

    id: str

    name: str

    occurrences: int = 1

    confidence: float = 1.0

    section: str = ""

    @property
    def is_high_confidence(self) -> bool:
        """
        True if confidence is at least 80%.
        """
        return self.confidence >= 0.8