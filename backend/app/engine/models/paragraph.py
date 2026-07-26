from __future__ import annotations

from dataclasses import dataclass, field

from app.engine.models.layout_budget import LayoutBudget
from app.engine.models.run import Run


@dataclass(slots=True)
class Paragraph:
    """
    Represents a single paragraph in the document.

    A paragraph owns runs and paragraph-level formatting.
    """

    # Identity
    id: str

    # Content
    runs: list[Run] = field(default_factory=list)

    # Paragraph style (Word style name)
    style_name: str = "Normal"

    # Paragraph formatting
    alignment: str | None = None
    left_indent: float | None = None
    right_indent: float | None = None
    first_line_indent: float | None = None

    space_before: float | None = None
    space_after: float | None = None
    line_spacing: float | None = None

    keep_together: bool = False
    keep_with_next: bool = False
    page_break_before: bool = False

    # Layout information
    layout_budget: LayoutBudget | None = None

    # Metadata
    editable: bool = True
    section: str | None = None

    @property
    def text(self) -> str:
        """Returns the full paragraph text."""
        return "".join(run.text for run in self.runs)