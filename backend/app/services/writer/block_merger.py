from app.services.batch.models import (
    AIBlockUpdate,
)

from app.services.docx.document_block import (
    DocumentBlock,
)


class BlockMerger:
    """
    Safely merges AI updates into the original
    document blocks while preserving formatting,
    runs and hyperlinks.
    """

    @classmethod
    def merge(
        cls,
        original_blocks: list[DocumentBlock],
        updated_blocks: list[AIBlockUpdate],
    ) -> list[DocumentBlock]:

        # -----------------------------------------
        # Index original blocks
        # -----------------------------------------

        block_map = {
            block.id: block
            for block in original_blocks
        }

        # -----------------------------------------
        # Apply AI updates
        # -----------------------------------------

        for update in updated_blocks:

            block = block_map.get(update.id)

            if block is None:
                continue

            # Only update paragraph text.
            # Everything else is preserved.
            block.text = update.text

        # -----------------------------------------
        # Explicitly preserve metadata
        # -----------------------------------------

        for block in original_blocks:

            block.runs = block.runs

            block.hyperlinks = block.hyperlinks

            block.paragraph_format = (
                block.paragraph_format
            )

            block.style = block.style

            block.can_optimize = (
                block.can_optimize
            )

        # -----------------------------------------
        # Preserve original order
        # -----------------------------------------

        return original_blocks