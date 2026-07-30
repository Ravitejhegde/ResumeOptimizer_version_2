from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class PromptContext:
    """
    Context provided to an AI rewrite request.

    Contains information required for safe
    resume optimization.

    Does NOT contain prompt templates.
    """

    # --------------------------------------------------
    # Resume Context
    # --------------------------------------------------

    section: str

    original_text: str

    paragraph_id: str | None = None

    # --------------------------------------------------
    # Optimization Context
    # --------------------------------------------------

    target_role: str | None = None

    technologies: list[str] = field(
        default_factory=list,
    )

    keywords: list[str] = field(
        default_factory=list,
    )

    instructions: list[str] = field(
        default_factory=list,
    )

    # --------------------------------------------------
    # Constraints
    # --------------------------------------------------

    preserve_formatting: bool = True

    max_length_change_percentage: float = 10.0