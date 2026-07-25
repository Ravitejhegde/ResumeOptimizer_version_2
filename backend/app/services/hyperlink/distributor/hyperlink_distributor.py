from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

from app.services.hyperlink.models.hyperlink import (
    Hyperlink,
)


class HyperlinkDistributor:
    """
    Finds every hyperlink inside a paragraph
    and preserves its boundaries while text
    around it is optimized.
    """

    @classmethod
    def collect(
        cls,
        paragraph: Paragraph,
    ) -> list[Hyperlink]:

        hyperlinks = []

        paragraph_xml = paragraph._p

        for node in paragraph_xml:

            if node.tag != qn("w:hyperlink"):
                continue

            relationship_id = node.get(
                qn("r:id"),
                "",
            )

            anchor = node.get(
                qn("w:anchor"),
                "",
            )

            text = []

            for run in node.findall(qn("w:r")):

                for t in run.findall(".//" + qn("w:t")):

                    if t.text:

                        text.append(t.text)

            hyperlink = Hyperlink()

            hyperlink.relationship_id = relationship_id

            hyperlink.bookmark = anchor

            hyperlink.text = "".join(text)

            hyperlinks.append(hyperlink)

        return hyperlinks