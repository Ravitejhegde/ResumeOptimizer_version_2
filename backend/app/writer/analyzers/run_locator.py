"""
app.writer.analyzers.run_locator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Utilities for locating editable DOCX runs.
"""

from __future__ import annotations

from docx.text.run import Run


class RunLocator:
    """
    Finds editable runs inside a DOCX paragraph.

    Responsibilities
    ----------------
    - Return editable text runs.
    - Ignore empty runs.
    - Never modify the document.
    """

    def locate(
        self,
        paragraph,
    ) -> list[Run]:
        """
        Return editable runs.
        """

        editable_runs: list[Run] = []

        for run in paragraph.runs:

            if self._is_editable(run):

                editable_runs.append(run)

        return editable_runs

    def _is_editable(
        self,
        run: Run,
    ) -> bool:
        """
        Decide whether a run can be rewritten.
        """

        if not run.text:
            return False

        if not run.text.strip():
            return False

        return True