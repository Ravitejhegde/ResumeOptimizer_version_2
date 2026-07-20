from .models import (
    Risk,
)


class RiskEngine:

    @classmethod
    def evaluate(

        cls,

        missing,

    ):

        risks = []

        if len(missing) > 10:

            risks.append(

                Risk(

                    title="High Skill Gap",

                    level="HIGH",

                    description="Resume is missing many required technologies.",

                )

            )

        return risks