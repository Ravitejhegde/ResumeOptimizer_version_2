from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class TextStyle:
    """
    Immutable character formatting.

    Shared by runs throughout the engine.
    """

    # Font
    font_name: str | None = None
    font_size: float | None = None

    # Basic formatting
    bold: bool = False
    italic: bool = False
    underline: bool = False
    strike: bool = False

    # Typography
    subscript: bool = False
    superscript: bool = False
    small_caps: bool = False
    all_caps: bool = False

    # Colors
    color: str | None = None
    highlight: str | None = None

    # Visibility
    hidden: bool = False