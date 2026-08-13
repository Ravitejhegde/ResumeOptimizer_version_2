"""
app.knowledge.loaders.knowledge_loader
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Loads the exported knowledge package into memory.

Responsibilities
----------------
- Locate exported knowledge
- Read exported files
- Validate package existence
- Return loaded runtime objects

This loader never:
- Analyze resumes
- Compare skills
- Resolve roles
- Perform business logic
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class KnowledgeLoader:
    """
    Loads exported knowledge package.
    """

    def __init__(
        self,
        package_directory: Path | str,
    ) -> None:
        self._package_directory = Path(package_directory)

    @property
    def package_directory(self) -> Path:
        """
        Exported package directory.
        """
        return self._package_directory

    def exists(self) -> bool:
        """
        Returns True if the package exists.
        """
        return self.package_directory.exists()

    def load_json(
        self,
        filename: str,
    ) -> Any:
        """
        Load a JSON file from the package.
        """
        path = self.package_directory / filename

        if not path.exists():
            raise FileNotFoundError(
                f"Knowledge file not found: {path}"
            )

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)