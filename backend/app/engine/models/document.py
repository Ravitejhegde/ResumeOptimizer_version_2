from __future__ import annotations

from dataclasses import dataclass, field

from app.engine.models.paragraph import Paragraph
from app.engine.models.table import Table


@dataclass(slots=True)
class Document:
    """
    Root model representing an entire Word document.

    This is the single source of truth used throughout
    the ResumeOptimizer engine.

    The Reader builds it.
    The Analyzer understands it.
    The Planner plans changes.
    The Optimizer modifies it.
    The Validator verifies it.
    The Writer saves it.
    """

    # Paragraphs in document order
    paragraphs: list[Paragraph] = field(
        default_factory=list
    )

    # Tables in document order
    tables: list[Table] = field(
        default_factory=list
    )

    # Document metadata
    page_count: int = 0
    section_count: int = 0

    # Original source
    source_path: str | None = None

    @property
    def text(self) -> str:
        """
        Returns the complete document text.
        """
        return "\n".join(
            paragraph.text
            for paragraph in self.paragraphs
        )