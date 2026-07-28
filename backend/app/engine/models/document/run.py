from __future__ import annotations

from dataclasses import dataclass

from app.engine.models.document.text_style import (
    TextStyle,
)


@dataclass(slots=True)
class Run:
    """
    Smallest editable text unit in a document.

    A Run owns text and references its character formatting.
    """

    # Content
    text: str

    # Character formatting
    style: TextStyle

    # Hyperlink
    hyperlink: str | None = None

    # Protection
    editable: bool = True
    locked_reason: str | None = None

    # Object metadata
    object_type: str = "text"




