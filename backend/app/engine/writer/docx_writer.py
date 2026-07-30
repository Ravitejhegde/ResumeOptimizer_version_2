from __future__ import annotations

import logging

from pathlib import Path

from app.engine.writer.models.write_context import (
    WriteContext,
)


logger = logging.getLogger(__name__)


class DocxWriter:
    """
    Final stage of Writer pipeline.

    Responsibilities:

        - Validate writer state.
        - Save optimized DOCX.
        - Confirm output creation.


    Does NOT:

        - Modify document content.
        - Generate text.
        - Apply optimization logic.
    """



    @staticmethod
    def write(
        context: WriteContext,
        output_file: str,
    ) -> None:
        """
        Save final DOCX document.
        """


        logger.info(
            "[DocxWriter] Starting document save..."
        )


        # ----------------------------------
        # Validate path
        # ----------------------------------

        if not output_file:

            context.add_error(
                "Output file path is empty."
            )

            raise ValueError(
                "Output file path is empty."
            )



        # ----------------------------------
        # Validate writer state
        # ----------------------------------

        if not context.valid:

            raise ValueError(

                "Cannot write invalid document:\n"
                +
                "\n".join(
                    context.errors
                )

            )



        output_path = Path(
            output_file
        )



        # ----------------------------------
        # Create directory
        # ----------------------------------

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )



        try:

            # ----------------------------------
            # Save DOCX
            # ----------------------------------

            context.working_doc.save(
                str(output_path)
            )


        except Exception as exc:


            context.add_error(

                f"DOCX save failed: {exc}"

            )


            raise



        # ----------------------------------
        # Verify output
        # ----------------------------------

        if not output_path.exists():

            context.add_error(

                "DOCX file was not created."

            )


            raise RuntimeError(

                "DOCX output missing after save."

            )



        logger.info(

            "[DocxWriter] "
            "Saved successfully: %s",

            output_path,

        )