from __future__ import annotations

import logging
from pathlib import Path

from app.engine.models.document.document import (
    Document,
)
from app.engine.reader.document_reader import (
    DocumentReader,
)
from app.engine.reader.snapshot_builder import (
    SnapshotBuilder,
)


logger = logging.getLogger(__name__)


class DocumentParser:
    """
    ResumeOptimizer V3 Document Parser.

    Entry point for converting a DOCX file
    into the internal Document model.

    Pipeline:

        DOCX
          |
          v
    DocumentReader
          |
          v
    SnapshotBuilder
          |
          v
      Document Model


    Responsibilities:
        - Validate input file
        - Start reader pipeline
        - Return canonical Document object

    Does not:
        - Analyze resume
        - Optimize content
        - Write DOCX
    """

    @staticmethod
    def parse(
        file_path: str,
    ) -> Document:

        path = Path(
            file_path
        ).resolve()


        # ----------------------------------
        # Validate input
        # ----------------------------------

        if not path.exists():

            raise FileNotFoundError(
                f"Document not found: {path}"
            )


        if not path.is_file():

            raise ValueError(
                "Provided path is not a file."
            )


        if path.suffix.lower() != ".docx":

            raise ValueError(
                "Only DOCX files are supported."
            )


        logger.info(
            "Parsing document: %s",
            path.name,
        )


        # ----------------------------------
        # Read DOCX
        # ----------------------------------

        document = DocumentReader.read(
            str(path)
        )


        logger.info(
            "Document read successfully. "
            "Paragraphs=%s Tables=%s",
            len(document.paragraphs),
            len(document.tables),
        )


        # ----------------------------------
        # Build snapshot
        # ----------------------------------

        document = SnapshotBuilder.build(
            document
        )


        logger.info(
            "Document snapshot completed."
        )


        return document