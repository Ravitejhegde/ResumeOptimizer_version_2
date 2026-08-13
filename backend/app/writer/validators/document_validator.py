"""
app.writer.validators.document_validator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Validates the Writer context before export.
"""

from __future__ import annotations

from app.writer.models.write_context import (
    WriteContext,
)


class DocumentValidator:
    """
    Validates the document before saving.
    """

    def validate(
        self,
        context: WriteContext,
    ) -> None:
        """
        Perform basic validation.
        """

        if context.working_document is None:

            context.add_error(
                "Working document is missing."
            )

        if context.document is None:

            context.add_error(
                "Document model is missing."
            )

        if context.optimization is None:

            context.add_error(
                "Optimization result is missing."
            )