class PriorityEngine:

    @classmethod
    def score(

        cls,

        gap,

    ):

        score = 50

        if gap.required:

            score += 40

        return min(

            score,

            100,

        )