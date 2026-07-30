"""
knowledge_builder.pipeline.build_pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

High-level pipeline for building the complete KnowledgeStore.

Pipeline

Sources
    │
    ▼
Loaders
    │
    ▼
StoreBuilder
    │
    ▼
Validated KnowledgeStore
    │
    ▼
Builders
    │
    ▼
Exporters

This pipeline intentionally contains no business logic. It simply
coordinates the construction of the knowledge platform.
"""

from __future__ import annotations

from knowledge_builder.models import KnowledgeStore
from knowledge_builder.store import StoreBuilder


class BuildPipeline:
    """
    Coordinates construction of the complete knowledge platform.
    """

    def __init__(self) -> None:
        self._builder = StoreBuilder()

    @property
    def store(self) -> KnowledgeStore:
        """
        Return the currently built KnowledgeStore.
        """
        return self._builder.store

    def run(self) -> KnowledgeStore:
        """
        Execute the complete build pipeline.

        Returns
        -------
        KnowledgeStore
            Fully populated and validated knowledge store.
        """
        return self._builder.build()

    def rebuild(self) -> KnowledgeStore:
        """
        Rebuild the entire knowledge platform.

        Returns
        -------
        KnowledgeStore
            Newly rebuilt validated knowledge store.
        """
        return self._builder.rebuild()