from .models import (
    Recommendation,
    SkillGap,
)


class RecommendationEngine:
    """
    Builds actionable recommendations
    from detected skill gaps.
    """

    @classmethod
    def build(
        cls,
        gaps: list[SkillGap],
    ) -> list[Recommendation]:

        recommendations = []

        ordered = sorted(
            gaps,
            key=lambda gap: gap.priority,
            reverse=True,
        )

        for gap in ordered:

            if not gap.required:
                continue

            recommendations.append(

                Recommendation(

                    title=f"Add {gap.name}",

                    description=(
                        gap.recommendation
                        if gap.recommendation
                        else (
                            f"Add {gap.name} only if you have genuine "
                            "experience using it."
                        )
                    ),

                    priority=gap.priority,

                )

            )

        return recommendations