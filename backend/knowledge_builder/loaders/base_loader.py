"""
knowledge_builder.loaders.base_loader
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Base loader used by every loader in the Knowledge Builder.

Responsibilities
----------------
- Locate source files.
- Read JSON safely.
- Validate file existence.
- Provide reusable helper methods.

This class intentionally DOES NOT:
- Create relationships
- Modify data
- Build indexes
- Store data

Those responsibilities belong to Builders and KnowledgeStore.
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseLoader(ABC):
    """
    Base class for all knowledge loaders.
    """

    def __init__(self, source_directory: Path | str):
        self._source_directory = Path(source_directory)

    @property
    def source_directory(self) -> Path:
        """
        Returns loader source directory.
        """
        return self._source_directory

    def ensure_directory_exists(self) -> None:
        """
        Raises FileNotFoundError if source directory does not exist.
        """
        if not self._source_directory.exists():
            raise FileNotFoundError(
                f"Source directory does not exist: "
                f"{self._source_directory}"
            )

    def list_json_files(self) -> list[Path]:
        """
        Returns all JSON files sorted alphabetically.
        """
        self.ensure_directory_exists()

        return sorted(
            file
            for file in self._source_directory.glob("*.json")
            if file.is_file()
        )

    @staticmethod
    def read_json(path: Path) -> Any:
        """
        Read JSON file.

        Raises
        ------
        FileNotFoundError

        json.JSONDecodeError
        """
        with path.open(
            mode="r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    @staticmethod
    def read_json_list(path: Path) -> list[dict]:
        """
        Read a JSON file expected to contain a list.
        """
        data = BaseLoader.read_json(path)

        if not isinstance(data, list):
            raise TypeError(
                f"{path} must contain a JSON array."
            )

        return data

    @staticmethod
    def read_json_object(path: Path) -> dict:
        """
        Read a JSON file expected to contain an object.
        """
        data = BaseLoader.read_json(path)

        if not isinstance(data, dict):
            raise TypeError(
                f"{path} must contain a JSON object."
            )

        return data

    @abstractmethod
    def load(self):
        """
        Load source files and return domain models.
        """
        raise NotImplementedError