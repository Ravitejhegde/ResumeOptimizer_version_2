from __future__ import annotations

from docx.text.run import Run


class XMLHelper:
    """
    Low-level helper for inspecting DOCX XML.

    Keeps XML parsing in one place.
    """

    @staticmethod
    def has_tab(run: Run) -> bool:
        return bool(
            run._element.xpath(".//w:tab")
        )

    @staticmethod
    def has_line_break(run: Run) -> bool:
        return bool(
            run._element.xpath(".//w:br")
        )

    @staticmethod
    def has_drawing(run: Run) -> bool:
        return bool(
            run._element.xpath(".//w:drawing")
        )

    @staticmethod
    def has_field(run: Run) -> bool:
        return bool(
            run._element.xpath(".//w:fldChar")
        )

    @staticmethod
    def has_bookmark(run: Run) -> bool:
        return bool(
            run._element.xpath(".//w:bookmarkStart")
        )