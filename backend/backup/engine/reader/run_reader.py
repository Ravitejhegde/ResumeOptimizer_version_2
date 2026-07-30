from __future__ import annotations

from docx.text.run import Run as DocxRun

from app.engine.common.enums import (
    ObjectType,
)
from app.engine.models.document.run import (
    Run,
)
from app.engine.reader.hyperlink_reader import (
    HyperlinkReader,
)
from app.engine.reader.style_reader import (
    StyleReader,
)


class RunReader:
    """
    Converts a python-docx Run into the engine Run model.

    Responsibilities:
        - Extract text
        - Extract character style
        - Extract hyperlink
        - Create editable Run object

    Does not:
        - Modify DOCX
        - Optimize text
        - Rewrite content
    """

    @staticmethod
    def read(
        docx_run: DocxRun,
    ) -> Run:
        """
        Convert python-docx Run into engine Run.
        """

        if docx_run is None:
            raise ValueError(
                "DOCX run cannot be None."
            )


        style = StyleReader.read(
            docx_run
        )


        hyperlink = HyperlinkReader.read(
            docx_run
        )


        return Run(

            # -----------------------------
            # Content
            # -----------------------------

            text=docx_run.text or "",


            # -----------------------------
            # Formatting
            # -----------------------------

            style=style,


            # -----------------------------
            # Hyperlink
            # -----------------------------

            hyperlink=hyperlink,


            # -----------------------------
            # Editing rules
            # -----------------------------

            editable=True,

            locked_reason=None,


            # -----------------------------
            # Object information
            # -----------------------------

            object_type=(
                ObjectType.TEXT.value
            ),
        )