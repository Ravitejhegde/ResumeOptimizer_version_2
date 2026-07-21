class TextReplacer:
    """
    Replaces text while preserving run boundaries.

    This class NEVER knows anything about Word.

    It only transforms strings.
    """

    @classmethod
    def replace(
        cls,
        original: str,
        optimized: str,
    ) -> str:

        if not optimized:
            return original

        return optimized.strip()