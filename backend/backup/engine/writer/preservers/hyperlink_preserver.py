from __future__ import annotations

from app.engine.writer.models.run_type import RunType
from app.engine.writer.models.write_context import WriteContext


class HyperlinkPreserver:
    """
    Ensures hyperlink metadata remains intact.

    This class does not recreate hyperlinks.
    It validates that hyperlink metadata collected during
    classification is still available before writing.
    """

    def preserve(
        self,
        context: WriteContext,
    ) -> None:

        for paragraph in context.paragraph_mappings:

            for run in paragraph.run_mappings:

                if run.run_type != RunType.HYPERLINK:
                    continue

                if run.relationship_id is None:
                    context.valid = False
                    context.errors.append(
                        f"Missing relationship id in paragraph "
                        f"{paragraph.paragraph_index}, run {run.run_index}"
                    )

                if run.hyperlink_target is None:
                    context.valid = False
                    context.errors.append(
                        f"Missing hyperlink target in paragraph "
                        f"{paragraph.paragraph_index}, run {run.run_index}"
                    )