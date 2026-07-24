from dataclasses import dataclass, field


@dataclass
class RunModel:
    text: str
    bold: bool
    italic: bool
    underline: bool
    font_name: str | None
    font_size: float | None
    color: str | None = None


@dataclass
class ParagraphModel:
    index: int
    text: str
    style: str

    alignment: int | None = None

    left_indent: float | None = None
    right_indent: float | None = None
    first_line_indent: float | None = None

    space_before: float | None = None
    space_after: float | None = None
    line_spacing: float | None = None

    is_heading: bool = False
    heading_level: int | None = None

    run_count: int = 0
    character_count: int = 0

    page_break_before: bool = False
    keep_together: bool = False
    keep_with_next: bool = False

    runs: list[RunModel] = field(
        default_factory=list,
    )


@dataclass
class TableCellModel:
    row: int
    column: int
    text: str


@dataclass
class TableModel:
    index: int
    cells: list[TableCellModel] = field(
        default_factory=list,
    )


@dataclass
class ResumeDocument:
    paragraphs: list[ParagraphModel] = field(
        default_factory=list,
    )

    tables: list[TableModel] = field(
        default_factory=list,
    )

    total_paragraphs: int = 0
    total_tables: int = 0
    total_runs: int = 0
    total_characters: int = 0

    has_tables: bool = False
    has_headings: bool = False