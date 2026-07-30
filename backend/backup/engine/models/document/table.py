from __future__ import annotations

from dataclasses import dataclass, field

from app.engine.models.document.paragraph import (
    Paragraph,
)


@dataclass(slots=True)
class Table:
    """
    Represents a Word table.

    Tables are preserved exactly as they appear in the
    original document. Each cell contains Paragraph objects,
    allowing the optimizer to edit text without losing layout.
    """

    # Identity
    id: str

    # Structure
    rows: int
    columns: int

    # Content
    # cells[row][column] -> list[Paragraph]
    cells: list[list[list[Paragraph]]] = field(
        default_factory=list
    )

    # Metadata
    editable: bool = True




