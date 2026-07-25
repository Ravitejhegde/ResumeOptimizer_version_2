from app.core.logger import logger


class RelationshipManager:
    """
    Handles Word relationship IDs (rId).

    Responsibilities:
    - Find relationship IDs
    - Resolve URLs
    - Preserve existing relationships
    - Create new relationships (future)
    """

    @classmethod
    def get_relationship(
        cls,
        paragraph,
        relationship_id: str,
    ):

        if not relationship_id:
            return None

        try:

            return paragraph.part.rels.get(
                relationship_id
            )

        except Exception as e:

            logger.warning(
                f"Relationship lookup failed: {e}"
            )

            return None

    @classmethod
    def get_url(
        cls,
        paragraph,
        relationship_id: str,
    ) -> str:

        relationship = cls.get_relationship(
            paragraph,
            relationship_id,
        )

        if relationship is None:
            return ""

        return relationship.target_ref