from pathlib import Path

from docx import Document

from app.services.docx.parser import (
    DocxParser,
)

from app.services.docx.writer import (
    DocxWriter,
)

from app.services.docx.block_update_builder import (
    BlockUpdateBuilder,
)


class EditorPipeline:
    """
    Applies paragraph updates using the
    formatting-preserving DOCX engine.
    """

    @classmethod
    def apply(
        cls,
        input_file: str,
        output_file: str,
        paragraph_updates: dict[str, str],
    ) -> None:

        # -----------------------------------------
        # Load original document
        # -----------------------------------------

        document = Document(input_file)

        # -----------------------------------------
        # Parse into DocumentBlocks
        # -----------------------------------------

        blocks = DocxParser.parse(
            document
        )

        # -----------------------------------------
        # Apply AI updates
        # -----------------------------------------

        BlockUpdateBuilder.apply(
            blocks=blocks,
            paragraph_updates=paragraph_updates,
        )

        # -----------------------------------------
        # Restore formatting + replace text
        # -----------------------------------------

        DocxWriter.replace_blocks(
            document=document,
            blocks=blocks,
        )

        # -----------------------------------------
        # Save
        # -----------------------------------------

        DocxWriter.save(
            document=document,
            output_path=Path(output_file),
        )