from __future__ import annotations

from app.engine.models.document.run import (
    Run,
)


class RunUpdater:
    """
    Updates run text while preserving
    character formatting.
    """

    # --------------------------------------------------

    def update(
        self,
        runs: list[Run],
        text: str,
    ) -> list[Run]:

        if not runs:

            return runs

        runs[0].text = text

        for run in runs[1:]:

            run.text = ""

        return runs
