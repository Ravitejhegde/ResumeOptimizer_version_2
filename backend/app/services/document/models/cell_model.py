from dataclasses import dataclass, field

from app.services.document.models.paragraph_model import (
    ParagraphModel,
)


@dataclass
class CellModel:
    """
    Represents one table cell.
    """

    row: int = 0

    column: int = 0

    width: float = 0

    height: float = 0

    colspan: int = 1

    rowspan: int = 1

    vertical_alignment: str = "top"

    background_color: str = ""

    paragraphs: list[ParagraphModel] = field(
        default_factory=list
    )