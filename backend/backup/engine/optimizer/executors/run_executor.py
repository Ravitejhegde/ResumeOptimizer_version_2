from __future__ import annotations

from app.engine.models.document.run import (
    Run,
)
from app.engine.models.planner.rewrite_plan import (
    RewritePlan,
)


class RunExecutor:
    """
    Executes optimization on paragraph runs.

    This class prepares the runs that will
    later be rewritten by AI.
    """

    # --------------------------------------------------

    def execute(
        self,
        runs: list[Run],
        rewrites: list[RewritePlan],
    ) -> tuple[
        list[Run],
        list[RewritePlan],
    ]:

        if not rewrites:

            return (
                runs,
                [],
            )

        editable = [

            run

            for run in runs

            if run.editable

        ]

        return (
            editable,
            rewrites,
        )
