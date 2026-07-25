from app.document.snapshot.document_snapshot import (
    DocumentSnapshot,
)

from app.services.docx.document_block import (
    DocumentBlock,
)

from app.services.docx.document_run import (
    DocumentRun,
)


class BlockBuilder:
    """
    Converts a DocumentSnapshot into editable
    DocumentBlock objects used by the optimizer.
    """

    @staticmethod
    def build(
        snapshot: DocumentSnapshot,
    ) -> list[DocumentBlock]:

        blocks: list[DocumentBlock] = []

        for index, paragraph in enumerate(
            snapshot.paragraphs
        ):

            # -----------------------------------------
            # Create Block
            # -----------------------------------------

            block = DocumentBlock(

                id=index,

                paragraph_index=index,

                text=paragraph.text,

                block_type="paragraph",

                style=paragraph.style,

                hyperlinks=paragraph.hyperlinks,

            )

            # -----------------------------------------
            # Copy Runs
            # -----------------------------------------

            for run in paragraph.runs:

                block.runs.append(

                    DocumentRun(

                        text=run.text,

                        bold=run.bold,

                        italic=run.italic,

                        underline=run.underline,

                        font_name=getattr(
                            run,
                            "font_name",
                            getattr(run, "font", None),
                        ),

                        font_size=getattr(
                            run,
                            "font_size",
                            getattr(run, "size", None),
                        ),

                        color=getattr(
                            run,
                            "color",
                            None,
                        ),

                        hyperlink=getattr(
                            run,
                            "hyperlink",
                            None,
                        ),

                        editable=getattr(
                            run,
                            "editable",
                            True,
                        ),

                        object_type=getattr(
                            run,
                            "object_type",
                            "text",
                        ),

                        locked_reason=getattr(
                            run,
                            "locked_reason",
                            None,
                        ),

                    )

                )

            blocks.append(block)

        return blocks