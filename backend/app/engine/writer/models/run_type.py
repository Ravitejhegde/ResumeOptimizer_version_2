from __future__ import annotations

from enum import Enum


class RunType(str, Enum):
    """
    Classification of a DOCX run.

    Used by the Writer to decide
    whether a run can be modified.
    """

    TEXT = "text"

    HYPERLINK = "hyperlink"

    TAB = "tab"

    LINE_BREAK = "line_break"

    FIELD = "field"

    BOOKMARK = "bookmark"

    IMAGE = "image"

    UNKNOWN = "unknown"