from __future__ import annotations

from dataclasses import dataclass, field

from app.engine.models.document.paragraph import Paragraph
from app.engine.models.document.table import Table
from app.engine.models.document.page_geometry import PageGeometry
from app.engine.models.document.layout_budget import LayoutBudget
from app.engine.models.document.numbering import Numbering


@dataclass(slots=True)
class Document:
    """
    Canonical document representation.

    Shared between:

    Reader
      ↓
    Analyzer
      ↓
    Planner
      ↓
    Optimizer
      ↓
    Writer
    """

    # --------------------------------------------------
    # Content
    # --------------------------------------------------

    paragraphs: list[Paragraph] = field(
        default_factory=list
    )

    tables: list[Table] = field(
        default_factory=list
    )

    # --------------------------------------------------
    # Structure
    # --------------------------------------------------

    sections: list = field(
        default_factory=list
    )

    # --------------------------------------------------
    # Document resources
    # --------------------------------------------------

    numbering: list[Numbering] = field(
        default_factory=list
    )

    hyperlinks: list = field(
        default_factory=list
    )

    # --------------------------------------------------
    # Layout
    # --------------------------------------------------

    page_geometry: PageGeometry | None = None

    layout_budget: LayoutBudget | None = None

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    metadata: dict = field(
        default_factory=dict
    )

    source_path: str | None = None


    @property
    def text(self) -> str:

        return "\n".join(
            paragraph.text
            for paragraph in self.paragraphs
        )


    @property
    def is_empty(self) -> bool:

        return not self.text.strip()


    @property
    def paragraph_count(self) -> int:

        return len(self.paragraphs)


    @property
    def table_count(self) -> int:

        return len(self.tables)