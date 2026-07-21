from dataclasses import dataclass, field

from app.services.document.models.cell_model import (
    CellModel,
)


@dataclass
class RowModel:
    """
    Represents one table row.
    """

    index: int = 0

    height: float = 0

    allow_break_across_pages: bool = True

    is_header: bool = False

    cells: list[CellModel] = field(
        default_factory=list
    )