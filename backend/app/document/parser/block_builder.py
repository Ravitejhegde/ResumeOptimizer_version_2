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

    @staticmethod
    def build(
        snapshot: DocumentSnapshot,
    ) -> list[DocumentBlock]:

        blocks: list[DocumentBlock] = []

        for index, paragraph in enumerate(
            snapshot.paragraphs
        ):

            block = DocumentBlock(

                id=index,

                paragraph_index=index,

                text=paragraph.text,

                block_type="paragraph",

                style=paragraph.style,

            )

            for run in paragraph.runs:

                block.runs.append(

                    DocumentRun(

                        text=run.text,

                        bold=run.bold,

                        italic=run.italic,

                        underline=run.underline,

                        font_name=run.font_name,

                        font_size=run.font_size,

                        color=run.color,

                        hyperlink=run.hyperlink,

                    )

                )

            blocks.append(block)

        return blocks