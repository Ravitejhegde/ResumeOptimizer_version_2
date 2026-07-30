"""
knowledge_builder.builders.knowledge_builder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Builds every derived knowledge structure from a validated
KnowledgeStore.

This is the single entry point for all builder components.

Pipeline

KnowledgeStore
      │
      ▼
CategoryIndexBuilder
TechnologyGraphBuilder
SkillIndexBuilder
RoleIndexBuilder
KeywordIndexBuilder
SynonymIndexBuilder
      │
      ▼
KnowledgeArtifacts

The KnowledgeBuilder never:
- Reads source files
- Validates knowledge
- Exports data
"""

from __future__ import annotations

from dataclasses import dataclass

from knowledge_builder.builders.category_index_builder import (
    CategoryIndex,
    CategoryIndexBuilder,
)
from knowledge_builder.builders.keyword_index_builder import (
    KeywordIndex,
    KeywordIndexBuilder,
)
from knowledge_builder.builders.role_index_builder import (
    RoleIndex,
    RoleIndexBuilder,
)
from knowledge_builder.builders.skill_index_builder import (
    SkillIndex,
    SkillIndexBuilder,
)
from knowledge_builder.builders.synonym_index_builder import (
    SynonymIndex,
    SynonymIndexBuilder,
)
from knowledge_builder.builders.technology_graph_builder import (
    TechnologyGraph,
    TechnologyGraphBuilder,
)
from knowledge_builder.models import KnowledgeStore


@dataclass(slots=True, frozen=True)
class KnowledgeArtifacts:
    """
    Collection of every derived knowledge structure.
    """

    category_index: CategoryIndex
    technology_graph: TechnologyGraph
    skill_index: SkillIndex
    role_index: RoleIndex
    keyword_index: KeywordIndex
    synonym_index: SynonymIndex


class KnowledgeBuilder:
    """
    Builds every optimized knowledge structure from a validated
    KnowledgeStore.
    """

    def __init__(self, store: KnowledgeStore) -> None:
        self._store = store

    @property
    def store(self) -> KnowledgeStore:
        """
        Return the validated KnowledgeStore.
        """
        return self._store

    def build(self) -> KnowledgeArtifacts:
        """
        Build every optimized knowledge artifact.

        Returns
        -------
        KnowledgeArtifacts
            Collection of optimized indexes and graphs.
        """

        category_index = (
            CategoryIndexBuilder(self.store)
            .run()
        )

        technology_graph = (
            TechnologyGraphBuilder(self.store)
            .run()
        )

        skill_index = (
            SkillIndexBuilder(self.store)
            .run()
        )

        role_index = (
            RoleIndexBuilder(self.store)
            .run()
        )

        keyword_index = (
            KeywordIndexBuilder(self.store)
            .run()
        )

        synonym_index = (
            SynonymIndexBuilder(self.store)
            .run()
        )

        return KnowledgeArtifacts(
            category_index=category_index,
            technology_graph=technology_graph,
            skill_index=skill_index,
            role_index=role_index,
            keyword_index=keyword_index,
            synonym_index=synonym_index,
        )