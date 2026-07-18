from dataclasses import dataclass
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT


@dataclass(slots=True)
class LayoutFormat:
    """
    Layout properties of a paragraph.
    Responsible only for visual positioning,
    not spacing or indentation.
    """

    alignment: WD_PARAGRAPH_ALIGNMENT | None = None

    outline_level: int | None = None

    bidi: bool | None = None

    mirror_indents: bool | None = None