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

        hyperlinks: list[HyperlinkModel] = []

        part = paragraph.part

        run_index = 0

        for element in paragraph._p:

            # Normal run
            if element.tag.endswith("}r"):
                run_index += 1
                continue

            # Hyperlink element
            if not element.tag.endswith("}hyperlink"):
                continue

            model = HyperlinkModel()

            # -----------------------------
            # Relationship ID
            # -----------------------------

            r_id = element.get(
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

            hyperlink_run_count = 0

            for node in element.xpath(".//w:t"):

                if node.text:
                    text.append(node.text)

            hyperlink_run_count = len(
                element.xpath(".//w:r")
            )

            model.text = "".join(text)

            model.is_external = bool(model.url)

            # -----------------------------
            # Preserve Run Position
            # -----------------------------

            model.start_run = run_index

            model.end_run = (
                run_index + hyperlink_run_count - 1
            )

            run_index += hyperlink_run_count

            hyperlinks.append(model)

        return hyperlinks