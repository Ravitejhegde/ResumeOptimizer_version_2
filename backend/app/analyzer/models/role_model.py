"""
app.analyzer.models.role_model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents a detected role within a resume.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class RoleModel:
    """
    Represents a detected role.
    """

    id: str

    name: str

    confidence: float = 0.0

    matched_skills: set[str] = field(
        default_factory=set
    )

    sections: set[str] = field(
        default_factory=set
    )