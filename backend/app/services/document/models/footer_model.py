from dataclasses import dataclass, field

from app.services.document.models.paragraph_model import (
    ParagraphModel,
)


@dataclass
class FooterModel:
    """
    Represents a document footer.
    """

    paragraphs: list[ParagraphModel] = field(
        default_factory=list
    )

    different_first_page: bool = False

    different_odd_even: bool = False