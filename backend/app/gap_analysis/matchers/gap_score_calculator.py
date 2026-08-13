"""
app.gap_analysis.matchers.gap_score_calculator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calculates overall resume-job match score.
"""

from __future__ import annotations


class GapScoreCalculator:
    """
    Calculates overall match score.
    """

    def calculate(
        self,
        matched: int,
        total: int,
    ) -> float:

        if total == 0:
            return 1.0

        return matched / total