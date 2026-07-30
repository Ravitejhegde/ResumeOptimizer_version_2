from __future__ import annotations

from app.engine.writer.models.write_context import (
    WriteContext,
)


class ParagraphUpdater:
    """
    Matches optimization rewrites to paragraph mappings.

    This class never modifies text.
    It only prepares the context for the RunUpdater.
    """

    def update(
        self,
        context: WriteContext,
    ) -> None:

        rewrite_map = {
            rewrite.paragraph_id: rewrite
            for rewrite in context.optimization.rewrites
        }

        print(
    f"[ParagraphUpdater] Paragraph={mapping.paragraph_index} "
    f"ID={mapping.model_paragraph.id} "
    f"Rewrite={'YES' if rewrite else 'NO'}"
)

        for mapping in context.paragraph_mappings:

            rewrite = rewrite_map.get(
                mapping.model_paragraph.id
            )

            if rewrite is None:

                mapping.editable = False

                continue

            # Store the rewrite on the mapping
            mapping.rewrite = rewrite

            mapping.editable = True