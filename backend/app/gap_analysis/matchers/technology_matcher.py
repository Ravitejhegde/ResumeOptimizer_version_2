"""
app.gap_analysis.matchers.technology_matcher
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Matches resume technologies against job technologies.
"""

from __future__ import annotations


class TechnologyMatcher:
    """
    Compares technologies.
    """

    def match(
        self,
        resume_technologies: set[str],
        job_technologies: set[str],
    ) -> tuple[set[str], set[str]]:

        matched = (
            resume_technologies
            & job_technologies
        )

        missing = (
            job_technologies
            - resume_technologies
        )

        return matched, missing