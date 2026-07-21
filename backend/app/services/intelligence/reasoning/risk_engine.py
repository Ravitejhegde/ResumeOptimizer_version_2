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

        risks: list[Risk] = []

        # -----------------------------------------
        # Too many missing skills
        # -----------------------------------------

        if len(missing) >= 10:

            risks.append(

                Risk(

                    title="High Skill Gap",

                    level="HIGH",

                    description=(
                        "The resume is missing a large number of required technologies. "
                        "Only technologies with genuine experience should be added."
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

                    level="MEDIUM",

                    description=(
                        f"High-priority technologies are missing: {names}."
                    ),

                )

            )

        # -----------------------------------------
        # Low confidence recommendations
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

                    level="LOW",

                    description=(
                        "Some technology recommendations have low confidence "
                        "and should be reviewed before optimization."
                    ),

                )

            )

        return risks