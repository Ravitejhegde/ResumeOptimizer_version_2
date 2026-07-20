from app.services.intelligence.const.role_weights import (
    ROLE_WEIGHTS,
)


class JDRoleDetector:
    """
    Detects the target role from Job Description skills.
    """

    @classmethod
    def detect(
        cls,
        skills,
    ) -> str:

        scores = {
            role: 0
            for role in ROLE_WEIGHTS
        }

        for skill in skills:

            key = skill.name.lower().strip()

            for role, weights in ROLE_WEIGHTS.items():

                if key in weights:

                    scores[role] += weights[key]

        print()
        print("========== JD ROLE SCORE ==========")

        for role, score in sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True,
        ):
            print(f"{role:<25} {score}")

        print()

        return max(
            scores,
            key=scores.get,
        )