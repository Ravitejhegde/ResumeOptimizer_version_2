from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

from app.services.hyperlink.models.hyperlink import (
    Hyperlink,
)


class HyperlinkXmlParser:
    """
    Reads <w:hyperlink> elements from a paragraph
    and converts them into Hyperlink models.
    """

    @classmethod
    def parse(
        cls,
        paragraph: Paragraph,
    ) -> list[Hyperlink]:

        hyperlinks: list[Hyperlink] = []

        paragraph_xml = paragraph._p

        for node in paragraph_xml:

            if node.tag != qn("w:hyperlink"):
                continue

            hyperlink = Hyperlink()

            hyperlink.relationship_id = node.get(
                qn("r:id"),
                "",
            )

            hyperlink.bookmark = node.get(
                qn("w:anchor"),
                "",
            )

            text_parts = []

            run_index = 0

            for child in node:

                if child.tag != qn("w:r"):
                    continue

                for text_node in child.findall(
                    ".//" + qn("w:t")
                ):

                    if text_node.text:

                        text_parts.append(
                            text_node.text
                        )

                run_index += 1

            hyperlink.text = "".join(
                text_parts
            )

            hyperlink.run_count = run_index

            hyperlinks.append(
                hyperlink
            )

        return hyperlinks