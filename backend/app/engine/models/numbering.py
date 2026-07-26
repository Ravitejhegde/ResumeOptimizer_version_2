from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Numbering:
    """
    Represents Word numbering/bullet information
    for a paragraph.

    Used to preserve ordered lists and bullet lists
    exactly as they appear in the original document.
    """

    # List identity
    num_id: int | None = None
    level: int = 0

    # List type
    is_bulleted: bool = False
    is_numbered: bool = False

    # Display
    format: str | None = None
    text: str | None = None

    # Restart behaviour
    restart: bool = False