"""
knowledge_builder.exporters.base_exporter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Base class for all Knowledge Builder exporters.

Exporters are responsible for persisting optimized knowledge artifacts
to external storage formats (JSON, binary cache, databases, etc.).

Exporters never:
- Read raw knowledge sources
- Build indexes or graphs
- Validate knowledge
- Modify exported objects
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generic, TypeVar

T = TypeVar("T")


class BaseExporter(ABC, Generic[T]):
    """
    Base class for all exporters.

    Parameters
    ----------
    output_directory:
        Directory where exported artifacts will be written.
    """

    def __init__(self, output_directory: Path | str) -> None:
        self._output_directory = Path(output_directory)

    @property
    def output_directory(self) -> Path:
        """
        Directory where exported files are written.
        """
        return self._output_directory

    def ensure_output_directory(self) -> None:
        """
        Create the output directory if it does not already exist.
        """
        self._output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def run(self, artifact: T) -> Path:
        """
        Execute the complete export process.

        Parameters
        ----------
        artifact:
            Object to export.

        Returns
        -------
        Path
            Path to the exported artifact.
        """
        self.ensure_output_directory()

        self.before_export(artifact)

        output_path = self.export(artifact)

        self.after_export(output_path)

        return output_path

    def before_export(self, artifact: T) -> None:
        """
        Hook executed immediately before export().

        Subclasses may override when needed.
        """
        return

    @abstractmethod
    def export(self, artifact: T) -> Path:
        """
        Export the artifact.

        Parameters
        ----------
        artifact:
            Object being exported.

        Returns
        -------
        Path
            Path of the exported file.
        """
        raise NotImplementedError

    def after_export(self, output_path: Path) -> None:
        """
        Hook executed after export().

        Parameters
        ----------
        output_path:
            Path returned by export().
        """
        return