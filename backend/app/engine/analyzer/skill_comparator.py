from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SkillComparison:
    """
    Result of comparing resume skills
    against job description skills.
    """

    matched_skills: list[str]

    missing_skills: list[str]

    extra_skills: list[str]

    match_percentage: int


class SkillComparator:
    """
    Compares resume technologies with
    job description technologies.

    Responsibilities
    ----------------
    • Find matched skills
    • Find missing skills
    • Find extra skills
    • Calculate match percentage

    This class performs only comparison.
    It never extracts or normalizes skills.
    """

    @staticmethod
    def compare(
        resume_skills: list[str],
        jd_skills: list[str],
    ) -> SkillComparison:

        resume = SkillComparator._prepare(
            resume_skills
        )

        jd = SkillComparator._prepare(
            jd_skills
        )

        matched = sorted(
            resume & jd
        )

        missing = sorted(
            jd - resume
        )

        extra = sorted(
            resume - jd
        )

        score = SkillComparator._calculate_score(
            matched,
            jd,
        )

        return SkillComparison(

            matched_skills=matched,

            missing_skills=missing,

            extra_skills=extra,

            match_percentage=score,

        )

    @staticmethod
    def _prepare(
        skills: list[str],
    ) -> set[str]:
        """
        Cleans and deduplicates skills.
        """

        return {

            skill.lower().strip()

            for skill in skills

            if skill.strip()

        }

    @staticmethod
    def _calculate_score(
        matched: list[str],
        jd: set[str],
    ) -> int:
        """
        Calculates exact-match percentage.
        """

        if not jd:

            return 100

        return round(

            len(matched)
            / len(jd)
            * 100

        )