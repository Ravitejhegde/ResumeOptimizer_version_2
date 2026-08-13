"""
app.optimizer.models.paragraph_update
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents a single AI optimization for one resume paragraph.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ParagraphUpdate:
    """
    Represents an optimized paragraph.

    Produced by:
        - AI Response Parser

    Consumed by:
        - Writer
    """

    # -----------------------------------------
    # Paragraph Identification
    # -----------------------------------------

    paragraph_id: str

    section: str

    # -----------------------------------------
    # Content
    # -----------------------------------------

    original_text: str

    optimized_text: str

    # -----------------------------------------
    # AI Metadata
    # -----------------------------------------

    confidence: float = 0.0

    reason: str = ""

    # -----------------------------------------
    # Validation
    # -----------------------------------------

    approved: bool = True

    formatting_safe: bool = True

    # -----------------------------------------
    # Helpers
    # -----------------------------------------

    @property
    def changed(self) -> bool:
        """
        True if AI changed the paragraph.
        """

        return (
            self.original_text.strip()
            != self.optimized_text.strip()
        )

    @property
    def original_length(self) -> int:
        return len(
            self.original_text
        )

    @property
    def optimized_length(self) -> int:
        return len(
            self.optimized_text
        )

    @property
    def length_difference(self) -> int:
        return (
            self.optimized_length
            - self.original_length
        )