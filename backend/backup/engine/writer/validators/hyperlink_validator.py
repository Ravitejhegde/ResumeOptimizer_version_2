from __future__ import annotations

from app.engine.writer.models.run_type import RunType
from app.engine.writer.models.write_context import WriteContext


class HyperlinkValidator:
    """
    Validates hyperlink integrity before saving.
    """

    def validate(
        self,
        context: WriteContext,
    ) -> None:

        for paragraph in context.paragraph_mappings:

            for run in paragraph.run_mappings:

                if run.run_type != RunType.HYPERLINK:
                    continue

                if not run.relationship_id:
                    context.valid = False
                    context.errors.append(
                        f"Hyperlink missing relationship id "
                        f"(paragraph={paragraph.paragraph_index}, run={run.run_index})"
                    )

                if not run.hyperlink_target:
                    context.valid = False
                    context.errors.append(
                        f"Hyperlink missing target "
                        f"(paragraph={paragraph.paragraph_index}, run={run.run_index})"
                    )