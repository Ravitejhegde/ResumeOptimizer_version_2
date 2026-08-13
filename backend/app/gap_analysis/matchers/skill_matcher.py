"""
app.gap_analysis.matchers.skill_matcher
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Matches resume skills against job skills.
"""

from __future__ import annotations


class SkillMatcher:
    """
    Compares resume skills with job skills.
    """

    def match(
        self,
        resume_skills: set[str],
        job_skills: set[str],
    ) -> tuple[set[str], set[str]]:

        matched = (
            resume_skills
            & job_skills
        )

        missing = (
            job_skills
            - resume_skills
        )

        return matched, missing