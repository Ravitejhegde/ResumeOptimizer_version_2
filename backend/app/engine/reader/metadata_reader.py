from __future__ import annotations

from pathlib import Path

from docx import Document as DocxDocument


class MetadataReader:
    """
    Reads document-level metadata.

    This reader extracts only document metadata and
    never inspects document content.
    """

    @staticmethod
    def read(
        document: DocxDocument,
        source_path: str,
    ) -> dict:

        properties = document.core_properties

        return {

            "file_name": Path(source_path).name,

            "file_extension": Path(source_path).suffix.lower(),

            "source_path": str(
                Path(source_path).resolve()
            ),

            "title": properties.title,

            "subject": properties.subject,

            "author": properties.author,

            "keywords": properties.keywords,

            "category": properties.category,

            "comments": properties.comments,

            "language": properties.language,

            "revision": properties.revision,

            "created": properties.created,

            "modified": properties.modified,

            "last_modified_by": properties.last_modified_by,

        }