from dataclasses import dataclass, field

from app.services.document.models.row_model import (
    RowModel,
)


@dataclass
class TableModel:
    """
    Represents one Word table.
    """

    index: int = 0

    style: str = ""

    alignment: str = ""

    autofit: bool = True

    rows: list[RowModel] = field(
        default_factory=list
    )

    has_header_row: bool = False

    allow_page_break: bool = True