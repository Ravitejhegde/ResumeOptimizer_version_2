from dataclasses import dataclass

from .skill_comparator import SkillComparison


@dataclass
class TechnologyPromotion:

    promote: list[str]

    missing: list[str]

    extra: list[str]


class TechnologyPromoter:

    @staticmethod
    def build(
        comparison: SkillComparison,
        selected_skills: list[str] | None = None,
    ) -> TechnologyPromotion:

        selected = {
            skill.strip().lower()
            for skill in (selected_skills or [])
        }

        promote = sorted(
            comparison.matched
        )

        if selected:

            missing = sorted(
                skill
                for skill in comparison.missing
                if skill.lower() in selected
            )

        else:

            # Backward compatible
            missing = sorted(
                comparison.missing
            )

        extra = sorted(
            comparison.extra
        )

        return TechnologyPromotion(

            promote=promote,

            missing=missing,

            extra=extra,

        )