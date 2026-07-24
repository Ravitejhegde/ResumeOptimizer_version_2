import json


class BatchResponseParser:
    """
    Parses the JSON response returned by the AI.
    """

    @classmethod
    def parse(
        cls,
        response: str,
    ) -> dict:

        if not response:
            return {}

        response = response.strip()

        # Remove Markdown code fences if present
        if response.startswith("```"):

            lines = response.splitlines()

            if lines:
                lines = lines[1:]

            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]

            response = "\n".join(lines).strip()

        try:

            data = json.loads(response)

            if isinstance(data, dict):
                return data

        except json.JSONDecodeError as e:

            print()
            print("=" * 60)
            print("INVALID AI RESPONSE")
            print("=" * 60)
            print(e)
            print(response)
            print("=" * 60)

        return {}