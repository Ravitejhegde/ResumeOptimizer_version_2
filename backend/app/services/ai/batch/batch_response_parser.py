import json


class BatchResponseParser:
    """
    Parses AI JSON response.
    """

    @classmethod
    def parse(
        cls,
        response: str,
    ) -> dict:

        try:

            data = json.loads(
                response
            )

            if isinstance(data, dict):

                return data

        except Exception:

            pass

        return {}