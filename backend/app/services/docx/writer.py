from pathlib import Path

from docx.document import Document

from app.services.hyperlink.distributor.run_distributor import (
    RunDistributor,
)

from app.services.hyperlink.writer.hyperlink_writer import (
    HyperlinkWriter,
)

from .document_block import (
    DocumentBlock,
)

from .paragraph_formatter import (
    ParagraphFormatter,
)


class DocxWriter:
    """
    Writes optimized blocks back into the original DOCX
    while preserving formatting and hyperlinks.
    """

    @staticmethod
    def replace_blocks(
        document: Document,
        blocks: list[DocumentBlock],
    ) -> None:

        for block in blocks:

            paragraph = document.paragraphs[
                block.paragraph_index
            ]

            # -----------------------------------------
            # Restore paragraph formatting
            # -----------------------------------------

            if block.paragraph_format is not None:

                ParagraphFormatter.restore(
                    paragraph,
                    block.paragraph_format,
                )

            # -----------------------------------------
            # Restore optimized text
            # (Hyperlink runs are preserved)
            # -----------------------------------------

            if block.can_optimize:

                RunDistributor.distribute(
                    paragraph=paragraph,
                    new_text=block.text,
                )

            # -----------------------------------------
            # Restore hyperlinks
            # -----------------------------------------

            HyperlinkWriter.write(
                paragraph=paragraph,
                hyperlinks=block.hyperlinks,
            )

    @staticmethod
    def save(
        document: Document,
        output_path: str | Path,
    ) -> None:

        document.save(output_path)