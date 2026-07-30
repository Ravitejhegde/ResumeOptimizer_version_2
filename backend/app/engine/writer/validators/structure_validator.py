from __future__ import annotations

import logging

from app.engine.writer.models.write_context import (
    WriteContext,
)


logger = logging.getLogger(__name__)


class StructureValidator:
    """
    Validates DOCX structure before writing.

    Pipeline:

        Writer Pipeline
              |
              v
        StructureValidator
              |
              v
        DocxWriter


    Responsibilities:

        - Ensure document structure is intact.
        - Validate mappings.
        - Prevent corrupted DOCX output.


    Does NOT:

        - Modify document.
        - Rewrite text.
        - Change formatting.
    """



    def validate(
        self,
        context: WriteContext,
    ) -> None:
        """
        Validate document structure.
        """


        logger.info(
            "[StructureValidator] "
            "Validating structure..."
        )


        self._validate_document_exists(
            context
        )


        self._validate_paragraph_count(
            context
        )


        self._validate_table_count(
            context
        )


        self._validate_section_count(
            context
        )


        self._validate_mappings(
            context
        )


        logger.info(
            "[StructureValidator] "
            "Structure validation completed."
        )



    # --------------------------------------------------

    def _validate_document_exists(
        self,
        context: WriteContext,
    ) -> None:


        if (
            context.working_doc is None
            or
            context.working_model is None
        ):

            context.add_error(
                "Working document is missing."
            )



    # --------------------------------------------------

    def _validate_paragraph_count(
        self,
        context: WriteContext,
    ) -> None:


        docx_count = len(
            context.working_doc.paragraphs
        )


        model_count = len(
            context.working_model.paragraphs
        )


        if docx_count != model_count:

            context.add_error(

                "Paragraph count mismatch "
                f"DOCX={docx_count} "
                f"MODEL={model_count}"

            )



    # --------------------------------------------------

    def _validate_table_count(
        self,
        context: WriteContext,
    ) -> None:


        docx_tables = len(
            context.working_doc.tables
        )


        model_tables = len(
            context.working_model.tables
        )


        if docx_tables != model_tables:

            context.add_error(

                "Table count mismatch "
                f"DOCX={docx_tables} "
                f"MODEL={model_tables}"

            )



    # --------------------------------------------------

    def _validate_section_count(
        self,
        context: WriteContext,
    ) -> None:


        doc_sections = len(
            context.working_doc.sections
        )


        source_sections = len(
            context.source_doc.sections
        )


        if doc_sections != source_sections:

            context.add_error(

                "Section count changed "
                f"{source_sections}->{doc_sections}"

            )



    # --------------------------------------------------

    def _validate_mappings(
        self,
        context: WriteContext,
    ) -> None:
        """
        Ensure writer mappings are valid.
        """


        for mapping in context.paragraph_mappings:


            if mapping.model_paragraph is None:

                context.add_error(

                    "Missing model paragraph mapping."

                )


            if mapping.docx_paragraph is None:

                context.add_error(

                    "Missing DOCX paragraph mapping."

                )


            if not mapping.valid:

                context.add_error(

                    f"Invalid paragraph mapping "
                    f"index={mapping.paragraph_index}"

                )