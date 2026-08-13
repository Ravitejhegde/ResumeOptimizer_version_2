"""
app.evidence.services.evidence_scorer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calculates evidence confidence.
"""

from __future__ import annotations


class EvidenceScorer:
    """
    Scores evidence quality.
    """

    def score(
        self,
        matched: int,
        required: int,
    ) -> float:

        if required == 0:
            return 0.0

        return matched / required