from __future__ import annotations

from collections import defaultdict


class TechnologyGraph:
    """
    Represents relationships between technologies.

    The graph is used by the Planner and Optimizer to:

    - Find related technologies
    - Discover neighbouring skills
    - Suggest replacements
    - Build technology clusters

    This class NEVER performs AI reasoning.
    """

    def __init__(self) -> None:

        self._graph: dict[str, set[str]] = defaultdict(set)

    @staticmethod
    def _normalize(
        technology: str,
    ) -> str:

        return technology.strip().lower()

    def add_relationship(
        self,
        technology_a: str,
        technology_b: str,
    ) -> None:

        a = self._normalize(
            technology_a,
        )

        b = self._normalize(
            technology_b,
        )

        if a == b:
            return

        self._graph[a].add(b)
        self._graph[b].add(a)

    def related_to(
        self,
        technology: str,
    ) -> list[str]:

        node = self._normalize(
            technology,
        )

        return sorted(
            self._graph.get(
                node,
                set(),
            )
        )

    def has_relationship(
        self,
        technology_a: str,
        technology_b: str,
    ) -> bool:

        a = self._normalize(
            technology_a,
        )

        b = self._normalize(
            technology_b,
        )

        return b in self._graph.get(
            a,
            set(),
        )

    def technologies(
        self,
    ) -> list[str]:

        return sorted(
            self._graph.keys()
        )