from __future__ import annotations

from docx.document import Document as DocxDocument
from docx.text.run import Run


class RelationshipHelper:
    """
    Helper for resolving DOCX relationships.

    Currently used for hyperlinks.
    """

    @staticmethod
    def get_relationship_id(
        run: Run,
    ) -> str | None:
        """
        Returns the hyperlink relationship id
        if the run belongs to a hyperlink.
        """

        parent = run._element.getparent()

        if parent is None:
            return None

        rid = parent.get(
            "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
        )

        return rid

    @staticmethod
    def get_hyperlink_target(
        document: DocxDocument,
        relationship_id: str | None,
    ) -> str | None:

        if relationship_id is None:
            return None

        rel = document.part.rels.get(
            relationship_id
        )

        if rel is None:
            return None

        return rel.target_ref