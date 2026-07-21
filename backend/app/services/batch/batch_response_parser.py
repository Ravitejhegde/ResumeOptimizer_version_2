import json
import re

from app.services.batch.models import (
    AIBlockUpdate,
)


class BatchResponseParser:
    """
    Parses and validates AI JSON response.
    """

    @classmethod
    def parse(
        cls,
        response: str,
    ) -> list[AIBlockUpdate]:

        # -----------------------------------
        # Remove Markdown code fences
        # -----------------------------------

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

        # -----------------------------------
        # Parse JSON
        # -----------------------------------

        try:

            data = json.loads(response)

        except json.JSONDecodeError as e:

            raise ValueError(
                f"AI returned invalid JSON.\n{e}"
            )

        # -----------------------------------
        # Validate root
        # -----------------------------------

        if not isinstance(data, dict):

            raise ValueError(
                "Response must be a JSON object."
            )

        if "blocks" not in data:

            raise ValueError(
                "Missing 'blocks' field."
            )

        blocks = data["blocks"]

        if not isinstance(blocks, list):

            raise ValueError(
                "'blocks' must be a list."
            )

        validated: list[AIBlockUpdate] = []

        # -----------------------------------
        # Validate every block
        # -----------------------------------

        for block in blocks:

            if not isinstance(block, dict):
                continue

            if "id" not in block:
                continue

            if "text" not in block:
                continue

            validated.append(
                AIBlockUpdate(
                    id=block["id"],
                    status=block.get(
                        "status",
                        "updated",
                    ),
                    text=block["text"],
                )
            )

        return validated