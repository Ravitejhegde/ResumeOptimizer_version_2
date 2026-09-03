"""
app.analyzer.document.document_analyzer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Reads a resume document and converts it into a DocumentModel.

Responsibilities
----------------
- Load a DOCX resume
- Extract readable text
- Preserve paragraph order
- Produce a DocumentModel

This analyzer intentionally does NOT:
- Detect sections
- Detect skills
- Detect roles
- Calculate ATS score
"""

from __future__ import annotations

from pathlib import Path

from docx import Document

from app.analyzer.contracts.document_analyzer_contract import (
    DocumentAnalyzerContract,
)
from app.analyzer.exceptions.analyzer_errors import (
    DocumentAnalysisError,
    EmptyDocumentError,
    UnsupportedDocumentError,
)
from app.analyzer.models.document_model import (
    DocumentModel,
)


class DocumentAnalyzer(DocumentAnalyzerContract):
    """
    Reads a DOCX resume into a DocumentModel.
    """

    def analyze(
        self,
        document: Path | str,
    ) -> DocumentModel:

        path = Path(document)

        if path.suffix.lower() != ".docx":
            raise UnsupportedDocumentError(
                f"Unsupported file type: {path.suffix}"
            )

        try:
            doc = Document(path)

        except Exception as exc:
            raise DocumentAnalysisError(
                f"Unable to open '{path}'."
            ) from exc

        paragraphs = [
    paragraph.text.strip()
    for paragraph in doc.paragraphs
]

        text = "\n".join(paragraphs)

        if not text:
            raise EmptyDocumentError(
                "The document contains no readable text."
            )

        return DocumentModel(
            filename=path.name,
            text=text,
            paragraphs=paragraphs,
        )