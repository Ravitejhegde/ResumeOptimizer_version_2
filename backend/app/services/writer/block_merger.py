class BlockMerger:
    """
    Safely merges AI updates into the
    original document blocks.
    """

    @classmethod
    def merge(

        cls,

        original_blocks,

        updated_blocks,

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

            block_id = update["id"]

            # Unknown block
            if block_id not in original:

                continue

            block = original[block_id]

            # Replace text only
            block.text = update["text"]

        # -----------------------------
        # Preserve Original Order
        # -----------------------------

        return original_blocks