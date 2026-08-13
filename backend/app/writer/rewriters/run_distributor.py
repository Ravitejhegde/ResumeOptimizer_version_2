"""
app.writer.rewriters.run_distributor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Distributes rewritten text across DOCX runs while
preserving formatting.
"""

from __future__ import annotations

from docx.text.paragraph import Paragraph
from docx.text.run import Run

from app.writer.analyzers.run_locator import (
    RunLocator,
)


class RunDistributor:
    """
    Applies rewritten text to DOCX runs.

    Responsibilities
    ----------------
    - Preserve formatting.
    - Replace only editable runs.
    - Never modify paragraph structure.
    """

    def __init__(self) -> None:

        self._locator = RunLocator()

    def distribute(
        self,
        paragraph: Paragraph,
        text: str,
    ) -> None:
        """
        Apply rewritten text.
        """

        runs = self._locator.locate(
            paragraph
        )

        if not runs:
            return

        self._replace_text(
            runs=runs,
            text=text,
        )

    def _replace_text(
        self,
        runs: list[Run],
        text: str,
    ) -> None:
        """
        MVP implementation.

        Preserve formatting by keeping the
        first editable run and clearing the
        remaining editable runs.
        """

        first_run = runs[0]

        first_run.text = text

        for run in runs[1:]:

            run.text = ""