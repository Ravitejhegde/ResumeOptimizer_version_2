from docx.opc.package import Part


class RelationshipValidator:
    """
    Validates hyperlink relationships
    inside a DOCX part.
    """

    @classmethod
    def exists(
        cls,
        part: Part,
        relationship_id: str,
    ) -> bool:

        if not relationship_id:
            return False

        return relationship_id in part.rels

    @classmethod
    def is_hyperlink(
        cls,
        part: Part,
        relationship_id: str,
    ) -> bool:

        if relationship_id not in part.rels:
            return False

        relationship = part.rels[
            relationship_id
        ]

        return relationship.reltype.endswith(
            "/hyperlink"
        )