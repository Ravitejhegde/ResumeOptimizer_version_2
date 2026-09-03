"""
app.writer.analyzers.run_locator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Utilities for locating DOCX runs.
"""

from __future__ import annotations

from docx.text.run import Run


class RunLocator:
    """
    Finds runs inside a DOCX paragraph.

    Responsibilities
    ----------------
    - Return all existing runs.
    - Preserve whitespace and tab runs.
    - Never modify the document.
    """

    def locate(
        self,
        paragraph,
    ) -> list[Run]:
        """
        Return all existing runs in their original order.

        Whitespace-only and tab runs are intentionally retained
        because they may carry important formatting.
        """

        return list(paragraph.runs)