from __future__ import annotations

from typing import Optional

from docx.text.run import Run as DocxRun


class HyperlinkReader:
    """
    Extracts hyperlink information from a Word Run.

    Returns the target URL if the run belongs to a
    hyperlink; otherwise returns None.

    This reader never modifies the document.
    """

    @staticmethod
    def read(
        run: DocxRun,
    ) -> Optional[str]:

        part = run.part

        parent = run._element.getparent()

        if parent is None:
            return None

        if not parent.tag.endswith("hyperlink"):
            return None

        relationship_id = parent.get(
            "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
        )

        if relationship_id is None:
            return None

        relationship = part.rels.get(relationship_id)

        if relationship is None:
            return None

        return relationship.target_ref




