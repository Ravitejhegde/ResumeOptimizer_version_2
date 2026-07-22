class PriorityEngine:
    """
    Calculates optimization priority for a missing skill.
    """

    @classmethod
    def score(
        cls,
        gap,
    ) -> int:

        score = gap.priority

        if gap.required:
            score += 40

        score += int(gap.confidence * 0.1)

        return min(score, 100)