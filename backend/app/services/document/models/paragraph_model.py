from dataclasses import dataclass, field

from app.services.document.models.run_model import (
    RunModel,
)

from app.services.document.models.hyperlink_model import (
    HyperlinkModel,
)


@dataclass
class ParagraphModel:
    """
    Represents one paragraph in a Word document.

    This is the primary editable unit
    used by ResumeOptimizer.
    """

    # -----------------------------------------
    # Identity
    # -----------------------------------------

    id: int = 0

    style: str = ""

    text: str = ""

    editable: bool = True

    # -----------------------------------------
    # Runs
    # -----------------------------------------

    runs: list[RunModel] = field(
        default_factory=list
    )

    hyperlinks: list[HyperlinkModel] = field(
        default_factory=list
    )

    # -----------------------------------------
    # Paragraph Formatting
    # -----------------------------------------

    alignment: str = "left"

    left_indent: float = 0

    right_indent: float = 0

    first_line_indent: float = 0

    hanging_indent: float = 0

    line_spacing: float = 1.0

    spacing_before: float = 0

    spacing_after: float = 0

    keep_with_next: bool = False

    keep_together: bool = False

    page_break_before: bool = False

    widow_control: bool = True

    # -----------------------------------------
    # Lists
    # -----------------------------------------

    is_list: bool = False

    list_level: int = 0

    list_type: str = ""

    list_id: int = -1

    # -----------------------------------------
    # Borders / Background
    # -----------------------------------------

    border: bool = False

    shading: str = ""

    # -----------------------------------------
    # Bookmark
    # -----------------------------------------

    bookmarks: list[str] = field(
        default_factory=list
    )