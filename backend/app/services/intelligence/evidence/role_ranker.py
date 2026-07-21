class RoleRanker:
    """
    Produces ranked roles instead of
    only the best role.
    """

    @classmethod
    def rank(
        cls,
        scores: dict[str, int],
    ):

        ranking = sorted(

            scores.items(),

            key=lambda item: item[1],

            reverse=True,

        )

        if not ranking:

            return []

        total = sum(

            score

            for _, score in ranking

        )

        results = []

        for role, score in ranking:

            confidence = (

                round(

                    score / total * 100,

                    1,

                )

                if total

                else 0

            )

            results.append(

                {

                    "role": role,

                    "score": score,

                    "confidence": confidence,

                }

            )

        return results