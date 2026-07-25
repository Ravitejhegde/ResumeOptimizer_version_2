from copy import deepcopy

from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

from app.services.hyperlink.models.hyperlink import (
    Hyperlink,
)


class XmlWriter:
    """
    Restores hyperlink XML into a paragraph.

    Current implementation preserves existing
    hyperlink XML nodes. Future versions may
    rebuild hyperlinks from scratch when needed.
    """

    @classmethod
    def restore(
        cls,
        paragraph: Paragraph,
        hyperlink: Hyperlink,
    ) -> None:

        paragraph_xml = paragraph._p

        for node in paragraph_xml:

            if node.tag != qn("w:hyperlink"):
                continue

            relationship_id = node.get(
                qn("r:id"),
                "",
            )

            if relationship_id != hyperlink.relationship_id:
                continue

            # Preserve the existing hyperlink XML.
            preserved_xml = deepcopy(node)

            parent = node.getparent()

            if parent is None:
                return

            index = parent.index(node)

            parent.remove(node)

            parent.insert(index, preserved_xml)

            return