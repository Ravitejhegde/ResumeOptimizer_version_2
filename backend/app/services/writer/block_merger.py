from app.services.batch.models import (
    AIBlockUpdate,
)


class BlockMerger:
    """
    Safely merges AI updates into the
    original document blocks.
    """

    @classmethod
    def merge(
        cls,
        original_blocks,
        updated_blocks: list[AIBlockUpdate],
    ):

        # -----------------------------
        # Index original blocks
        # -----------------------------

        original = {
            block.id: block
            for block in original_blocks
        }

        # -----------------------------
        # Apply Updates
        # -----------------------------

        for update in updated_blocks:

            # Unknown block
            if update.id not in original:
                continue

            block = original[update.id]

            # Replace text only
            block.text = update.text

        # -----------------------------
        # Preserve Original Order
        # -----------------------------

        return original_blocks