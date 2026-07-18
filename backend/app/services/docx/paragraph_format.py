from dataclasses import dataclass


@dataclass
class ParagraphFormat:

    alignment: int | None

    left_indent: float | None

    right_indent: float | None

    first_line_indent: float | None

    space_before: float | None

    space_after: float | None

    line_spacing: float | None

    keep_together: bool | None

    keep_with_next: bool | None

    page_break_before: bool | None