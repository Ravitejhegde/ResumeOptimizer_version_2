"""
knowledge_builder.exporters.json_exporter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Exports KnowledgeArtifacts to a JSON file.

This exporter produces a portable JSON representation of the optimized
knowledge artifacts. It is intended for debugging, inspection, and
future runtime loading.

The exporter never modifies the artifacts.
"""

from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

from knowledge_builder.builders import KnowledgeArtifacts
from knowledge_builder.exporters.base_exporter import BaseExporter


class JsonExporter(BaseExporter[KnowledgeArtifacts]):
    """
    Export KnowledgeArtifacts as JSON.
    """

    DEFAULT_FILENAME = "knowledge.json"

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
        Output filename.
        """
        return self._filename

    def export(
        self,
        artifact: KnowledgeArtifacts,
    ) -> Path:
        """
        Export KnowledgeArtifacts into a JSON file.
        """
        output_path = self.output_directory / self.filename

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        payload = self._serialize(artifact)

        with output_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                payload,
                file,
                indent=2,
                ensure_ascii=False,
                sort_keys=True,
            )

        return output_path

    def _serialize(
        self,
        value: Any,
    ) -> Any:
        """
        Convert Python objects into JSON-serializable values.
        """

        if is_dataclass(value):
            return self._serialize(
                asdict(value)
            )

        if isinstance(value, dict):
            return {
                str(key): self._serialize(item)
                for key, item in value.items()
            }

        if isinstance(value, (list, tuple)):
            return [
                self._serialize(item)
                for item in value
            ]

        if isinstance(value, set):
            return [
                self._serialize(item)
                for item in sorted(
                    value,
                    key=lambda item: repr(item),
                )
            ]

        if isinstance(value, Path):
            return str(value)

        return value