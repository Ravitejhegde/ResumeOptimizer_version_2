from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class SectionPlan:
    """
    Planning information for one resume section.

    Produced by Planner.

    Consumed by:
        - Optimizer
        - Writer

    Responsibilities:
        - Decide whether section can change
        - Define optimization priority
        - Track affected paragraphs
        - Preserve document structure

    Does NOT:
        - Edit DOCX
        - Generate text
    """

    # --------------------------------------------------
    # Section Identity
    # --------------------------------------------------

    section: str

    # --------------------------------------------------
    # Control
    # --------------------------------------------------

    editable: bool = True

    selected: bool = True

    priority: int = 0

    confidence: float = 0.0

    # --------------------------------------------------
    # Optimization Targets
    # --------------------------------------------------

    technologies: list[str] = field(
        default_factory=list,
    )

    paragraphs: list[str] = field(
        default_factory=list,
    )

    # --------------------------------------------------
    # Constraints
    # --------------------------------------------------

    purpose: str | None = None

    max_changes: int | None = None

    preserve_formatting: bool = True

    # --------------------------------------------------
    # Explanation
    # --------------------------------------------------

    notes: list[str] = field(
        default_factory=list,
    )

    warnings: list[str] = field(
        default_factory=list,
    )

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def can_edit(
        self,
    ) -> bool:

        return (
            self.editable
            and self.selected
        )

    def has_paragraphs(
        self,
    ) -> bool:

        return bool(
            self.paragraphs
        )