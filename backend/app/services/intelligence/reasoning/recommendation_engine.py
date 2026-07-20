from .models import (
    Recommendation,
)


class RecommendationEngine:

    @classmethod
    def build(

        cls,

        gaps,

    ):

        recommendations = []

        for gap in gaps[:5]:

            recommendations.append(

                Recommendation(

                    title=f"Add {gap.name}",

                    description=f"Include {gap.name} where you have genuine experience.",

                    priority=gap.priority,

                )

            )

        return recommendations