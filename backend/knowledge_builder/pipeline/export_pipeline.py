"""
knowledge_builder.pipeline.export_pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Coordinates exporting optimized knowledge artifacts.

Pipeline

KnowledgeStore
      │
      ▼
KnowledgeBuilder
      │
      ▼
KnowledgeArtifacts
      │
      ▼
ExportManager
      │
      ├── JsonExporter
      ├── CacheExporter
      └── Future Exporters
"""

from __future__ import annotations

from pathlib import Path

from knowledge_builder.builders import (
    KnowledgeArtifacts,
    KnowledgeBuilder,
)
from knowledge_builder.exporters import (
    CacheExporter,
    ExportManager,
    JsonExporter,
)
from knowledge_builder.models import KnowledgeStore


class ExportPipeline:
    """
    Builds optimized knowledge artifacts and exports them.
    """

    def __init__(
        self,
        store: KnowledgeStore,
        output_directory: Path | str,
    ) -> None:
        self._store = store
        self._output_directory = Path(output_directory)

    @property
    def store(self) -> KnowledgeStore:
        """
        Return the validated knowledge store.
        """
        return self._store

    @property
    def output_directory(self) -> Path:
        """
        Return the export output directory.
        """
        return self._output_directory

    def build_artifacts(self) -> KnowledgeArtifacts:
        """
        Build optimized runtime artifacts.
        """
        return KnowledgeBuilder(
            self.store
        ).build()

    def create_export_manager(self) -> ExportManager:
        """
        Configure the default exporters.
        """
        manager = ExportManager()

        manager.register(
            JsonExporter(
                self.output_directory,
            )
        )

        manager.register(
            CacheExporter(
                self.output_directory,
            )
        )

        return manager

    def run(self) -> list[Path]:
        """
        Execute the complete export pipeline.

        Returns
        -------
        list[Path]
            Paths of generated export files.
        """
        artifacts = self.build_artifacts()

        manager = self.create_export_manager()

        return manager.export(artifacts)