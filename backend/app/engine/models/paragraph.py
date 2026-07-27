from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from app.engine.models.layout_budget import (
    LayoutBudget,
)
from app.engine.models.run import Run


@dataclass(slots=True)
class Paragraph:
    """
    Represents a single paragraph in the document.

    A paragraph owns runs and paragraph-level formatting.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    id: str

    # ---------------------------------------------------------
    # Content
    # ---------------------------------------------------------

    runs: list[Run] = field(
        default_factory=list,
    )

    # ---------------------------------------------------------
    # Style
    # ---------------------------------------------------------

    style_name: str = "Normal"

    # ---------------------------------------------------------
    # Formatting
    # ---------------------------------------------------------

    alignment: str | None = None

    left_indent: float | None = None

    right_indent: float |None = None

    first_line_indent: float | None = None

    space_before: float | None = None

    space_after: float | None = None

    line_spacing: float | None = None

    keep_together: bool = False

    keep_with_next: bool = False

    page_break_before: bool = False

    # ---------------------------------------------------------
    # Layout
    # ---------------------------------------------------------

    layout_budget: LayoutBudget | None = None

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    editable: bool = True

    section: str | None = None

    # ---------------------------------------------------------
    # Computed
    # ---------------------------------------------------------

    @property
    def text(
        self,
    ) -> str:
        """
        Returns paragraph text.
        """

        return "".join(
            run.text
            for run in self.runs
        )

    @property
    def is_empty(
        self,
    ) -> bool:
        """
        True if paragraph contains
        no visible text.
        """

        return not self.text.strip()

    @property
    def run_count(
        self,
    ) -> int:
        """
        Number of runs.
        """

        return len(
            self.runs
        )




