from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ParagraphGeometry:
    """
    Physical geometry of a paragraph on a page.

    These values are collected by the Reader and are
    later used by the Planner, Optimizer and Validator
    to preserve the original layout.
    """

    # Page position
    page_number: int

    # Printable area
    available_width: float

    available_height: float

    # Paragraph position (future)
    x: float | None = None
    y: float | None = None

    # Estimated occupied size
    estimated_width: float | None = None
    estimated_height: float | None = None

    # Estimated rendering
    estimated_line_count: int = 1

    # Overflow information
    may_overflow: bool = False