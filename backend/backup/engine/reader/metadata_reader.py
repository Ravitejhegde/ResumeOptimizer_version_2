from __future__ import annotations

from pathlib import Path
from typing import Any

from docx import Document as DocxDocument


class MetadataReader:
    """
    Reads document-level metadata.

    Responsibilities:
        - Extract DOCX core properties.
        - Extract file information.
        - Provide metadata for the engine.

    This reader:
        - Does not inspect paragraphs.
        - Does not modify the document.
        - Does not handle optimization logic.
    """

    @staticmethod
    def read(
        document: DocxDocument,
        source_path: str,
    ) -> dict[str, Any]:
        """
        Extract metadata from DOCX document.

        Returns:
            Dictionary containing document metadata.
        """

        path = Path(
            source_path
        ).resolve()

        properties = (
            document.core_properties
        )

        return {

            # ----------------------------------
            # File information
            # ----------------------------------

            "file_name": path.name,

            "file_extension": path.suffix.lower(),

            "source_path": str(path),


            # ----------------------------------
            # DOCX properties
            # ----------------------------------

            "title": properties.title,

            "subject": properties.subject,

            "author": properties.author,

            "keywords": properties.keywords,

            "category": properties.category,

            "comments": properties.comments,


            # ----------------------------------
            # Language / version
            # ----------------------------------

            "language": properties.language,

            "revision": properties.revision,


            # ----------------------------------
            # Audit information
            # ----------------------------------

            "created": properties.created,

            "modified": properties.modified,

            "last_modified_by": (
                properties.last_modified_by
            ),
        }