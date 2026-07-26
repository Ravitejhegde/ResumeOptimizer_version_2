from __future__ import annotations

from pathlib import Path

from app.engine.models.document import Document
from app.engine.reader.document_reader import DocumentReader
from app.engine.reader.snapshot_builder import SnapshotBuilder


class DocumentParser:
    """
    ResumeOptimizer V3 Reader

    Entry point for reading a DOCX file into the
    engine document model.

    Pipeline

        DOCX
          │
          ▼
    DocumentReader
          │
          ▼
    SnapshotBuilder
          │
          ▼
      Document Model
    """

    @staticmethod
    def parse(
        file_path: str,
    ) -> Document:

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Document not found: {path}"
            )

        if path.suffix.lower() != ".docx":
            raise ValueError(
                "Only .docx files are supported."
            )

        document = DocumentReader.read(
            str(path)
        )

        document = SnapshotBuilder.build(
            document
        )

        return document