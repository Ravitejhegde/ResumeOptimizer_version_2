class RewriteResponseParser:

    @classmethod
    def parse(
        cls,
        response: str,
    ) -> str:

        return response.strip()