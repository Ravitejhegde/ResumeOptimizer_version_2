"""
knowledge_builder.builders.technology_graph_builder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Builds a graph for technology relationships.

The graph enables fast traversal between technologies using the
relationships already stored inside each Technology model.

Graph edges are derived from:

- related_technology_ids

The builder never modifies the KnowledgeStore.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from knowledge_builder.builders.base_builder import BaseBuilder
from knowledge_builder.models import Technology


@dataclass(slots=True)
class TechnologyGraph:
    """
    Immutable graph-like lookup structure for technologies.
    """

    nodes: dict[str, Technology] = field(default_factory=dict)
    adjacency: dict[str, set[str]] = field(default_factory=dict)

    @property
    def size(self) -> int:
        """
        Number of technologies.
        """
        return len(self.nodes)

    def has(self, technology_id: str) -> bool:
        return technology_id in self.nodes

    def get(self, technology_id: str) -> Technology | None:
        return self.nodes.get(technology_id)

    def neighbors(self, technology_id: str) -> tuple[Technology, ...]:
        """
        Return directly related technologies.
        """
        related_ids = self.adjacency.get(technology_id, set())

        return tuple(
            self.nodes[related_id]
            for related_id in related_ids
            if related_id in self.nodes
        )

    def related_ids(self, technology_id: str) -> frozenset[str]:
        """
        Return IDs of directly connected technologies.
        """
        return frozenset(
            self.adjacency.get(
                technology_id,
                set(),
            )
        )


class TechnologyGraphBuilder(BaseBuilder[TechnologyGraph]):
    """
    Builds an optimized technology relationship graph.
    """

    def build(self) -> TechnologyGraph:
        graph = TechnologyGraph()

        # ---------------------------------------------------------
        # Create nodes
        # ---------------------------------------------------------

        for technology in self.store.technologies.values():

            graph.nodes[technology.id] = technology
            graph.adjacency.setdefault(
                technology.id,
                set(),
            )

        # ---------------------------------------------------------
        # Create edges
        # ---------------------------------------------------------

        for technology in self.store.technologies.values():

            current = technology.id

            for related in technology.related_technology_ids:

                if related not in graph.nodes:
                    raise ValueError(
                        f"Technology '{current}' references "
                        f"unknown technology '{related}'."
                    )

                graph.adjacency[current].add(related)

                # Keep graph undirected for traversal
                graph.adjacency[related].add(current)

        return graph