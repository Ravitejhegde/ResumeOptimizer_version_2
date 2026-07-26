from __future__ import annotations

from dataclasses import dataclass

from app.engine.models.page_geometry import PageGeometry
from app.engine.models.paragraph_geometry import ParagraphGeometry


@dataclass(slots=True)
class LayoutBudget:
    """
    Represents the layout constraints of a paragraph.

    The optimizer MUST remain within this budget
    unless an explicit override is approved.

    This model is the foundation of ResumeOptimizer's
    document preservation engine.
    """

    # ----------------------------------------
    # Original Content Metrics
    # ----------------------------------------

    original_characters: int
    original_words: int
    original_lines: int

    # ----------------------------------------
    # Allowed Budget
    # ----------------------------------------

    max_characters: int
    max_words: int
    max_lines: int

    # ----------------------------------------
    # Page Information
    # ----------------------------------------

    page_number: int

    page_geometry: PageGeometry | None = None

    # ----------------------------------------
    # Paragraph Geometry
    # ----------------------------------------

    paragraph_geometry: ParagraphGeometry | None = None

    # ----------------------------------------
    # Paragraph Formatting
    # ----------------------------------------

    left_indent: float | None = None
    right_indent: float | None = None
    first_line_indent: float | None = None

    line_spacing: float | None = None

    space_before: float | None = None
    space_after: float | None = None

    # ----------------------------------------
    # Validation
    # ----------------------------------------

    allow_overflow: bool = False
    tolerance_percentage: float = 0.0

    @property
    def remaining_characters(self) -> int:
        """Characters that may still be inserted."""
        return max(
            0,
            self.max_characters - self.original_characters,
        )

    @property
    def remaining_words(self) -> int:
        """Words that may still be inserted."""
        return max(
            0,
            self.max_words - self.original_words,
        )