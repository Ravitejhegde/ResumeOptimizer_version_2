from __future__ import annotations

import logging

from app.engine.writer.models.write_context import (
    WriteContext,
)


logger = logging.getLogger(__name__)


class LayoutPreserver:
    """
    Validates DOCX layout preservation.

    Pipeline:

        RunUpdater
             |
             v
        LayoutPreserver
             |
             v
        DocxWriter


    Responsibilities:

        - Verify page settings.
        - Verify document structure.
        - Detect layout risks.
        - Protect original formatting.


    Does NOT:

        - Reformat document.
        - Change margins.
        - Insert pages.
        - Modify DOCX structure.
    """



    def preserve(
        self,
        context: WriteContext,
    ) -> None:
        """
        Validate layout consistency.
        """


        logger.info(
            "[LayoutPreserver] Checking layout..."
        )


        self._validate_page_settings(
            context
        )


        self._validate_paragraph_count(
            context
        )


        self._validate_tables(
            context
        )


        logger.info(
            "[LayoutPreserver] Layout validation completed."
        )



    # --------------------------------------------------

    def _validate_page_settings(
        self,
        context: WriteContext,
    ) -> None:
        """
        Ensure page dimensions and margins
        are unchanged.
        """


        source_sections = (
            context.source_doc.sections
        )


        working_sections = (
            context.working_doc.sections
        )


        if len(source_sections) != len(
            working_sections
        ):

            context.add_warning(
                "Section count changed."
            )

            return



        for index, (
            source,
            working,
        ) in enumerate(
            zip(
                source_sections,
                working_sections,
            )
        ):


            checks = [

                (
                    source.page_width,
                    working.page_width,
                    "page width",
                ),

                (
                    source.page_height,
                    working.page_height,
                    "page height",
                ),

                (
                    source.top_margin,
                    working.top_margin,
                    "top margin",
                ),

                (
                    source.bottom_margin,
                    working.bottom_margin,
                    "bottom margin",
                ),

                (
                    source.left_margin,
                    working.left_margin,
                    "left margin",
                ),

                (
                    source.right_margin,
                    working.right_margin,
                    "right margin",
                ),

            ]


            for original, current, name in checks:

                if original != current:

                    context.add_warning(

                        f"Layout changed: {name} "
                        f"section={index}"

                    )



    # --------------------------------------------------

    def _validate_paragraph_count(
        self,
        context: WriteContext,
    ) -> None:
        """
        Ensure paragraphs are not added
        or removed accidentally.
        """


        source_count = len(
            context.source_doc.paragraphs
        )


        working_count = len(
            context.working_doc.paragraphs
        )


        if source_count != working_count:

            context.add_warning(

                "Paragraph count changed "
                f"{source_count}->{working_count}"

            )



    # --------------------------------------------------

    def _validate_tables(
        self,
        context: WriteContext,
    ) -> None:
        """
        Ensure tables remain unchanged.
        """


        source_tables = len(
            context.source_doc.tables
        )


        working_tables = len(
            context.working_doc.tables
        )


        if source_tables != working_tables:

            context.add_warning(

                "Table count changed "
                f"{source_tables}->{working_tables}"

            )