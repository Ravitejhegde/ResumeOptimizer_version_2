from .models import (
    Risk,
    SkillGap,
)


class RiskEngine:
    """
    Evaluates optimization risks before
    sending instructions to the AI.
    """

    @classmethod
    def evaluate(
        cls,
        missing: list[SkillGap],
    ) -> list[Risk]:

        risks = []

        # -----------------------------------------
        # Too many missing skills
        # -----------------------------------------

        if len(missing) >= 10:

            risks.append(

                Risk(

                    title="High Skill Gap",

                    description=(
                        "The resume is missing many important technologies. "
                        "Only add technologies you genuinely know."
                    ),

                    severity=90,

                    recommendation=(
                        "Review missing technologies carefully."
                    ),

                )

            )

        # -----------------------------------------
        # Critical missing skills
        # -----------------------------------------

        critical = [

            gap

            for gap in missing

            if gap.priority >= 90

        ]

        if critical:

            names = ", ".join(

                gap.name

                for gap in critical

            )

            risks.append(

                Risk(

                    title="Critical Missing Skills",

                    description=(
                        f"Critical technologies missing: {names}"
                    ),

                    severity=70,

                    recommendation=(
                        "Add only if you have real experience."
                    ),

                )

            )

        # -----------------------------------------
        # Low confidence matches
        # -----------------------------------------

        low_confidence = [

            gap

            for gap in missing

            if gap.confidence < 70

        ]

        if low_confidence:

            risks.append(

                Risk(

                    title="Low Confidence Matches",

                    description=(
                        "Some recommendations have low confidence."
                    ),

                    severity=40,

                    recommendation=(
                        "Review these manually."
                    ),

                )

            )

        return risks