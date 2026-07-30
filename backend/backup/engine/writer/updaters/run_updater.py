from __future__ import annotations

from app.engine.writer.models.write_context import (
    WriteContext,
)
from app.engine.writer.updaters.run_distributor import (
    RunDistributor,
)


class RunUpdater:
    """
    Updates editable runs only.
    """

    def __init__(self) -> None:
        self._distributor = RunDistributor()

    def update(
        self,
        context: WriteContext,
    ) -> None:

        for paragraph in context.paragraph_mappings:

            if not paragraph.editable:
                continue

            if paragraph.rewrite is None:
                continue

            self._distributor.distribute(
                paragraph,
            )