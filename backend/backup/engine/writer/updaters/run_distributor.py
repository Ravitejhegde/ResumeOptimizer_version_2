from __future__ import annotations

from app.engine.writer.models.paragraph_mapping import (
    ParagraphMapping,
)
from app.engine.writer.models.run_type import (
    RunType,
)


class RunDistributor:
    """
    Distributes optimized text across editable runs.

    This implementation is intentionally simple.
    It never modifies protected runs.
    """

    def distribute(
        self,
        paragraph: ParagraphMapping,
    ) -> None:

        if paragraph.rewrite is None:
            return

        editable_runs = [
            run
            for run in paragraph.run_mappings
            if run.run_type == RunType.TEXT
            and run.editable
        ]

        if not editable_runs:
            return

        optimized_text = paragraph.rewrite.optimized_text

        # Temporary strategy:
        # Put all optimized text into the first editable run.
        editable_runs[0].docx_run.text = optimized_text

        # Clear remaining editable runs.
        for run in editable_runs[1:]:
            run.docx_run.text = ""