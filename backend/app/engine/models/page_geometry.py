from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class PageGeometry:
    """
    Physical page measurements.

    These values come directly from the DOCX
    section properties.
    """

    width: float

    height: float

    margin_left: float

    margin_right: float

    margin_top: float

    margin_bottom: float

    header_distance: float

    footer_distance: float

    gutter: float

    columns: int = 1

    @property
    def printable_width(self) -> float:

        return (
            self.width
            - self.margin_left
            - self.margin_right
        )

    @property
    def printable_height(self) -> float:

        return (
            self.height
            - self.margin_top
            - self.margin_bottom
        )




