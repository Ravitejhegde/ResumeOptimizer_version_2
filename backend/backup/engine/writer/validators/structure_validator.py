from __future__ import annotations

from app.engine.writer.models.write_context import WriteContext


class StructureValidator:
    """
    Performs basic structural validation before writing.
    """

    def validate(
        self,
        context: WriteContext,
    ) -> None:

        if len(context.working_doc.paragraphs) != len(
            context.working_model.paragraphs
        ):
            context.valid = False
            context.errors.append(
                "Paragraph count mismatch."
            )