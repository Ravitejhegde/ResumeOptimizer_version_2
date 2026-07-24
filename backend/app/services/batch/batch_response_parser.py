import json
import re

from app.services.batch.models import (
    AIBlockUpdate,
)


class BatchResponseParser:
    """
    Parses, cleans and validates AI responses.
    """

    @classmethod
    def parse(
        cls,
        response: str,
    ) -> list[AIBlockUpdate]:

        if not response:
            return []

        # -----------------------------------------
        # Remove Markdown
        # -----------------------------------------

        response = response.strip()

        response = re.sub(
            r"^```(?:json)?",
            "",
            response,
            flags=re.IGNORECASE,
        )

        response = re.sub(
            r"```$",
            "",
            response,
        )

        response = response.strip()

        # -----------------------------------------
        # Extract JSON object if AI added text
        # -----------------------------------------

        start = response.find("{")
        end = response.rfind("}")

        if start != -1 and end != -1:
            response = response[start:end + 1]

        # -----------------------------------------
        # Parse JSON
        # -----------------------------------------

        try:
            data = json.loads(response)

        except Exception as e:
            raise ValueError(
                f"Invalid AI JSON response:\n{e}\n\n{response}"
            )

        # -----------------------------------------
        # Legacy format
        #
        # {
        #   "P00001":"text",
        #   "P00002":"text"
        # }
        # -----------------------------------------

        if isinstance(data, dict) and "blocks" not in data:

            updates = []

            for paragraph_id, text in data.items():

                updates.append(

                    AIBlockUpdate(

                        id=paragraph_id,

                        status="updated",

                        text=str(text).strip(),

                    )

                )

            return updates

        # -----------------------------------------
        # New format
        #
        # {
        #   "blocks":[]
        # }
        # -----------------------------------------

        if not isinstance(data, dict):

            raise ValueError(
                "AI response must be a JSON object."
            )

        blocks = data.get("blocks", [])

        if not isinstance(blocks, list):

            raise ValueError(
                "'blocks' must be a list."
            )

        updates = []

        for block in blocks:

            if not isinstance(block, dict):
                continue

            paragraph_id = block.get("id")

            text = block.get("text")

            if not paragraph_id:
                continue

            if text is None:
                continue

            updates.append(

                AIBlockUpdate(

                    id=str(paragraph_id),

                    status=block.get(
                        "status",
                        "updated",
                    ),

                    text=str(text).strip(),

                )

            )

        return updates