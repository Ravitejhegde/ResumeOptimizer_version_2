from docx.text.paragraph import Paragraph

from app.services.hyperlink.models.hyperlink import (
    Hyperlink,
)

from .hyperlink_xml_parser import (
    HyperlinkXmlParser,
)

from .relationship_parser import (
    RelationshipParser,
)


class HyperlinkParser:
    """
    Parses all hyperlinks from a paragraph.

    Combines XML information and relationship
    information into Hyperlink models.
    """

    @classmethod
    def parse(
        cls,
        paragraph: Paragraph,
    ) -> list[Hyperlink]:

        hyperlinks = HyperlinkXmlParser.parse(
            paragraph
        )

        relationships = RelationshipParser.parse(
            paragraph.part
        )

        for hyperlink in hyperlinks:

            relationship = relationships.get(
                hyperlink.relationship_id
            )

            if relationship is None:
                continue

            hyperlink.url = relationship.url

            hyperlink.is_external = (
                relationship.is_external
            )

            if hasattr(
                relationship,
                "relationship_type",
            ):
                hyperlink.relationship_type = (
                    relationship.relationship_type
                )

            if hasattr(
                relationship,
                "target_mode",
            ):
                hyperlink.target_mode = (
                    relationship.target_mode
                )

        return hyperlinks