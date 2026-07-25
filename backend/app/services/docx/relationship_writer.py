from copy import deepcopy

from app.core.logger import logger


class RelationshipWriter:
    """
    Copies hyperlink relationships from the
    original document part to the optimized
    document part.
    """

    @classmethod
    def copy_relationships(
        cls,
        source_paragraph,
        target_paragraph,
    ) -> None:

        source_part = source_paragraph.part
        target_part = target_paragraph.part

        for rel_id, rel in source_part.rels.items():

            try:

                if rel.is_external:

                    target_part.rels.add_relationship(

                        rel.reltype,

                        deepcopy(rel._target),

                        rel_id,

                        is_external=True,

                    )

            except Exception as e:

                logger.debug(
                    f"Relationship {rel_id} skipped: {e}"
                )