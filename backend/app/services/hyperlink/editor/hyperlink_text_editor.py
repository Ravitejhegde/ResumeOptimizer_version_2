from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

from app.services.hyperlink.models.hyperlink import (
    Hyperlink,
)


class HyperlinkTextEditor:
    """
    Updates only the display text of a hyperlink.

    The relationship ID, URL, formatting,
    and hyperlink XML remain untouched.
    """

    @classmethod
    def update(
        cls,
        paragraph: Paragraph,
        hyperlink: Hyperlink,
        new_text: str,
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

            text_updated = False

            for run in node.findall(qn("w:r")):

                for text_node in run.findall(qn("w:t")):

                    if not text_updated:

                        text_node.text = new_text

                        text_updated = True

                    else:

                        text_node.text = ""

            break