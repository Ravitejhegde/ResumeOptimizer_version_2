"""
knowledge_builder.exporters.cache_exporter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Exports KnowledgeArtifacts as a binary cache.

The cache is intended for fast application startup, avoiding repeated
construction of indexes and graphs during runtime.

The exporter never modifies the artifacts.
"""

from __future__ import annotations

import pickle
from pathlib import Path

from knowledge_builder.builders import KnowledgeArtifacts
from knowledge_builder.exporters.base_exporter import BaseExporter


class CacheExporter(BaseExporter[KnowledgeArtifacts]):
    """
    Export KnowledgeArtifacts as a binary cache.
    """

    DEFAULT_FILENAME = "knowledge.cache"

    def __init__(
        self,
        output_directory: Path | str,
        filename: str = DEFAULT_FILENAME,
    ) -> None:
        super().__init__(output_directory)
        self._filename = filename

    @property
    def filename(self) -> str:
        """
        Name of the generated cache file.
        """
        return self._filename

    def export(
        self,
        artifact: KnowledgeArtifacts,
    ) -> Path:
        """
        Serialize KnowledgeArtifacts into a binary cache.

        Parameters
        ----------
        artifact:
            Optimized knowledge artifacts.

        Returns
        -------
        Path
            Generated cache file.
        """
        output_path = self.output_directory / self.filename

        with output_path.open("wb") as file:
            pickle.dump(
                artifact,
                file,
                protocol=pickle.HIGHEST_PROTOCOL,
            )

        return output_path

    @staticmethod
    def load(cache_file: Path | str) -> KnowledgeArtifacts:
        """
        Load KnowledgeArtifacts from a binary cache.

        Parameters
        ----------
        cache_file:
            Path to the cache file.

        Returns
        -------
        KnowledgeArtifacts
            Restored optimized knowledge artifacts.
        """
        cache_path = Path(cache_file)

        with cache_path.open("rb") as file:
            artifact = pickle.load(file)

        if not isinstance(artifact, KnowledgeArtifacts):
            raise TypeError(
                "Invalid knowledge cache. "
                "Expected KnowledgeArtifacts."
            )

        return artifact