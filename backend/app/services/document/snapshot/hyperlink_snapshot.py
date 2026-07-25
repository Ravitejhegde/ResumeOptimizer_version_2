from dataclasses import dataclass, field

from app.services.document.models.hyperlink_model import (
    HyperlinkModel,
)


@dataclass
class HyperlinkSnapshot:
    """
    Stores all hyperlinks belonging to a paragraph.
    """

    hyperlinks: list[HyperlinkModel] = field(
        default_factory=list
    )