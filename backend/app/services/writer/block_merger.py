class BlockMerger:

    @staticmethod
    def merge(
        original_blocks,
        ai_response,
    ):

        updates = {}

        for block in ai_response["blocks"]:

            if block["status"] == "updated":

                updates[block["id"]] = block["text"]

        for block in original_blocks:

            if block.id in updates:

                block.text = updates[block.id]

        return original_blocks