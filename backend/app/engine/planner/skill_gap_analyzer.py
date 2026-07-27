from __future__ import annotations

from app.engine.models.skill_gap import (
    SkillGap,
)
from app.engine.models.skill_priority import (
    SkillPriority,
)


class SkillGapAnalyzer:
    """
    Compares resume skills with
    prioritized JD skills.

    Produces the optimization target.
    """

    MIN_PRIORITY = 70

    @classmethod
    def analyze(

        cls,

        resume_skills: list[str],

        prioritized_skills: list[SkillPriority],

    ) -> SkillGap:

        resume_lookup = {

            skill.lower().strip()

            for skill in resume_skills

        }

        matched = []

        missing = []

        ignored = []

        for skill in prioritized_skills:

            if skill.priority < cls.MIN_PRIORITY:

                ignored.append(
                    skill.skill
                )

                continue

            if skill.skill.lower() in resume_lookup:

                matched.append(
                    skill
                )

            else:

                missing.append(
                    skill
                )

        jd_lookup = {

            skill.skill.lower()

            for skill in prioritized_skills

        }

        extra = [

            skill

            for skill in resume_skills

            if skill.lower() not in jd_lookup

        ]

        total = len(
            matched
        ) + len(
            missing
        )

        score = (

            100.0

            if total == 0

            else round(
                len(matched)
                / total
                * 100,
                1,
            )

        )

        return SkillGap(

            matched=matched,

            missing=missing,

            extra=extra,

            ignored=ignored,

            score=score,

        )