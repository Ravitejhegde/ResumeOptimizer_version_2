from pathlib import Path

from docx.document import Document

from .document_block import DocumentBlock
from .paragraph_formatter import (
    ParagraphFormatter,
)
from .run_text_distributor import (
    RunTextDistributor,
)


class DocxWriter:

    @staticmethod
    def replace_blocks(
        document: Document,
        blocks: list[DocumentBlock],
    ) -> None:

        for block in blocks:

            if not block.can_optimize:
                continue

            paragraph = document.paragraphs[
                block.paragraph_index
            ]

            # Restore original paragraph formatting
            ParagraphFormatter.restore(
                paragraph,
                block.paragraph_format,
            )

            # Distribute optimized text while preserving runs
            RunTextDistributor.distribute(
                paragraph=paragraph,
                block=block,
            )

    @staticmethod
    def save(
        document: Document,
        output_path: str | Path,
    ) -> None:

        document.save(output_path)