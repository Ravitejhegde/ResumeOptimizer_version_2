from __future__ import annotations

from docx.text.paragraph import Paragraph


class HyperlinkWriter:
    """
    Preserves hyperlinks in a DOCX paragraph.

    Responsibilities
    ----------------
    • Preserve hyperlink relationships
    • Preserve anchor text
    • Preserve destination URLs
    • Never rewrite hyperlinks
    • Never call AI

    This class exists to make the intent
    of the writer pipeline explicit.

    Hyperlinks are treated as locked
    document entities.
    """

    @staticmethod
    def apply(
        source: Paragraph,
        target: Paragraph,
    ) -> None:
        """
        Hyperlinks are already preserved because
        ResumeOptimizer never edits hyperlink runs.

        This method intentionally performs no
        modifications.

        It exists so DocxWriter has a dedicated
        hyperlink stage and future hyperlink
        features can be added without changing
        the orchestration pipeline.
        """

        return