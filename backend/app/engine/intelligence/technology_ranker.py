from __future__ import annotations

from dataclasses import dataclass

from app.engine.intelligence.role_classifier import (
    RoleProfile,
)
from app.engine.intelligence.technology_graph import (
    TechnologyGraph,
    TechnologyNode,
)


@dataclass(slots=True, frozen=True)
class RankedTechnology:
    """
    A technology with its calculated
    optimization priority.
    """

    technology: str

    category: str

    score: int

    graph_priority: int

    role_weight: int

    related: list[str]


class TechnologyRanker:
    """
    Calculates technology importance
    for the detected role.

    Higher score means the optimizer
    should prioritize promoting the
    technology.
    """

    def __init__(self) -> None:

        self._graph = TechnologyGraph()

    def rank(
        self,
        technologies: list[str],
        role_profile: RoleProfile,
    ) -> list[RankedTechnology]:

        ranked: list[
            RankedTechnology
        ] = []

        visited: set[str] = set()

        for technology in technologies:

            node = self._graph.get(
                technology
            )

            if node is None:
                continue

            if node.name in visited:
                continue

            visited.add(
                node.name
            )

            graph_priority = (
                node.priority
            )

            role_weight = (
                role_profile.category_weights.get(
                    node.category,
                    50,
                )
            )

            score = int(

                graph_priority * 0.6

                +

                role_weight * 0.4

            )

            ranked.append(

                RankedTechnology(

                    technology=node.name,

                    category=node.category,

                    score=score,

                    graph_priority=graph_priority,

                    role_weight=role_weight,

                    related=node.related,

                )

            )

        ranked.sort(

            key=lambda item: item.score,

            reverse=True,

        )

        return ranked




