from dataclasses import dataclass, field

from app.services.document.models.paragraph_model import (
    ParagraphModel,
)

from app.services.document.models.table_model import (
    TableModel,
)

from app.services.document.models.header_model import (
    HeaderModel,
)

from app.services.document.models.footer_model import (
    FooterModel,
)


@dataclass
class SectionModel:
    """
    Represents one Word document section.
    """

    index: int = 0

    # -----------------------------------------
    # Page Layout
    # -----------------------------------------

    page_width: float = 0

    page_height: float = 0

    orientation: str = "portrait"

    margin_top: float = 0

    margin_bottom: float = 0

    margin_left: float = 0

    margin_right: float = 0

    columns: int = 1

    # -----------------------------------------
    # Content
    # -----------------------------------------

    paragraphs: list[ParagraphModel] = field(
        default_factory=list
    )

    tables: list[TableModel] = field(
        default_factory=list
    )

    # -----------------------------------------
    # Header / Footer
    # -----------------------------------------

    header: HeaderModel = field(
        default_factory=HeaderModel
    )

    footer: FooterModel = field(
        default_factory=FooterModel
    )

    # -----------------------------------------
    # Section Properties
    # -----------------------------------------

    different_first_page: bool = False

    different_odd_even: bool = False

    start_type: str = "continuous"