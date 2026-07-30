from __future__ import annotations


class TechnologySelector:
    """
    Temporary implementation.

    Accepts the priorities produced by PriorityScorer
    and passes them through unchanged.

    Replace this with the real selection logic later.
    """

    def select(self, priorities):
        return priorities