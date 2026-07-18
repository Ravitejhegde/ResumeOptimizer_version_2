import json


class BatchResponseParser:

    @staticmethod
    def parse(response: str) -> dict:

        try:
            data = json.loads(response)

        except json.JSONDecodeError:
            raise ValueError(
                "AI returned invalid JSON."
            )

        if "blocks" not in data:
            raise ValueError(
                "Missing 'blocks' field."
            )

        if not isinstance(data["blocks"], list):
            raise ValueError(
                "'blocks' must be a list."
            )

        return data 