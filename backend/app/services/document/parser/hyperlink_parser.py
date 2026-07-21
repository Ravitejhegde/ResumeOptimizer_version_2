from docx.text.paragraph import Paragraph

from app.services.document.models.hyperlink_model import (
    HyperlinkModel,
)


class HyperlinkParser:
    """
    Parses hyperlinks from a Word paragraph.

    python-docx has no public hyperlink API,
    so we inspect the XML relationships.
    """

    @classmethod
    def parse(
        cls,
        paragraph: Paragraph,
    ) -> list[HyperlinkModel]:

        hyperlinks = []

        part = paragraph.part

        for hyperlink in paragraph._p.xpath(".//w:hyperlink"):

            model = HyperlinkModel()

            # -----------------------------
            # Relationship
            # -----------------------------

            r_id = hyperlink.get(
                "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
            )

            model.relationship_id = r_id or ""

            # -----------------------------
            # URL
            # -----------------------------

            if r_id:

                relationship = part.rels.get(r_id)

                if relationship:

                    model.url = relationship.target_ref

            # -----------------------------
            # Display Text
            # -----------------------------

            text = []

            for node in hyperlink.xpath(".//w:t"):

                if node.text:

                    text.append(node.text)

            model.text = "".join(text)

            model.is_external = bool(model.url)

            hyperlinks.append(model)

        return hyperlinks