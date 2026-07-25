from app.services.hyperlink.models.hyperlink_relationship import (
    HyperlinkRelationship,
)


class RelationshipParser:
    """
    Parses hyperlink relationships from a DOCX part.

    Maps relationship IDs (rId) to target URLs.
    """

    @classmethod
    def parse(
        cls,
        part,
    ) -> dict[str, HyperlinkRelationship]:

        relationships: dict[
            str,
            HyperlinkRelationship,
        ] = {}

        for r_id, relationship in part.rels.items():

            # Only external hyperlinks
            if not relationship.reltype.endswith(
                "/hyperlink"
            ):
                continue

            model = HyperlinkRelationship()

            model.relationship_id = r_id

            model.relationship_type = (
                relationship.reltype
            )

            model.target_mode = getattr(
                relationship,
                "target_mode",
                "External",
            )

            model.url = relationship.target_ref

            model.is_external = (
                model.target_mode == "External"
            )

            relationships[r_id] = model

        return relationships