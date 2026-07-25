from docx.text.paragraph import Paragraph

from app.services.hyperlink.models.hyperlink import (
    Hyperlink,
)


class RelationshipWriter:
    """
    Ensures hyperlink relationships remain valid.

    If the relationship already exists,
    nothing is changed.

    Future versions may recreate missing
    relationships if required.
    """

    @classmethod
    def restore(
        cls,
        paragraph: Paragraph,
        hyperlink: Hyperlink,
    ) -> None:

        if not hyperlink.relationship_id:
            return

        relationships = paragraph.part.rels

        if hyperlink.relationship_id in relationships:
            return

        # Future implementation:
        # Recreate missing relationship
        # using hyperlink.url.