"""
knowledge_builder.exporters.export_manager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Coordinates exporting KnowledgeArtifacts into one or more output
formats.

Responsibilities
----------------
- Execute multiple exporters
- Collect exported file paths
- Keep exporter execution centralized

The ExportManager never:
- Reads knowledge sources
- Builds knowledge artifacts
- Validates knowledge
- Modifies exported artifacts
"""

from __future__ import annotations

from pathlib import Path

from knowledge_builder.builders import KnowledgeArtifacts
from knowledge_builder.exporters.base_exporter import BaseExporter


class ExportManager:
    """
    Executes multiple exporters against the same KnowledgeArtifacts.
    """

    def __init__(self) -> None:
        self._exporters: list[BaseExporter[KnowledgeArtifacts]] = []

    @property
    def exporters(self) -> tuple[BaseExporter[KnowledgeArtifacts], ...]:
        """
        Registered exporters.
        """
        return tuple(self._exporters)

    def register(
        self,
        exporter: BaseExporter[KnowledgeArtifacts],
    ) -> None:
        """
        Register an exporter.

        Raises
        ------
        ValueError
            If the exporter has already been registered.
        """
        if exporter in self._exporters:
            raise ValueError(
                f"{exporter.__class__.__name__} is already registered."
            )

        self._exporters.append(exporter)

    def unregister(
        self,
        exporter: BaseExporter[KnowledgeArtifacts],
    ) -> None:
        """
        Remove a registered exporter.
        """
        self._exporters.remove(exporter)

    def clear(self) -> None:
        """
        Remove every registered exporter.
        """
        self._exporters.clear()

    def export(
        self,
        artifacts: KnowledgeArtifacts,
    ) -> list[Path]:
        """
        Execute every registered exporter.

        Parameters
        ----------
        artifacts:
            Optimized knowledge artifacts.

        Returns
        -------
        list[Path]
            Paths of every generated artifact.
        """
        exported_files: list[Path] = []

        for exporter in self._exporters:
            exported_files.append(
                exporter.run(artifacts)
            )

        return exported_files

    def __len__(self) -> int:
        return len(self._exporters)

    def __bool__(self) -> bool:
        return bool(self._exporters)