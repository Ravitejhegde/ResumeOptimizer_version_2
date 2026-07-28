from __future__ import annotations

from docx.text.paragraph import Paragraph


class NumberingWriter:
    """
    Preserves paragraph numbering.

    Responsibilities
    ----------------
    • Preserve bullets
    • Preserve numbered lists
    • Preserve list hierarchy
    • Preserve indentation
    • Never modify text
    • Never call AI

    Paragraph numbering is preserved by
    leaving the original paragraph
    numbering properties unchanged.
    """

    @staticmethod
    def apply(
        source: Paragraph,
        target: Paragraph,
    ) -> None:
        """
        ResumeOptimizer never recreates
        paragraphs.

        Therefore numbering, bullets and
        list hierarchy remain unchanged.

        This stage exists to make the
        writer pipeline explicit and to
        support future numbering features.
        """

        return