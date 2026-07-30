from __future__ import annotations

from app.engine.writer.models.write_context import (
    WriteContext,
)


class LayoutPreserver:
    """
    Writer V2 layout preservation.

    Layout is preserved by editing a cloned DOCX.
    """

    def preserve(
        self,
        context: WriteContext,
    ) -> None:
        return