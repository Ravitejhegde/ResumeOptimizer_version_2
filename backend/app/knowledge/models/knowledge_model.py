"""
app.knowledge.models.knowledge_model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Root runtime model.

Represents the complete knowledge loaded into memory.

Every runtime service reads data through this model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class KnowledgeModel:
    """
    Runtime representation of the exported knowledge.
    """

    data: dict[str, Any] = field(default_factory=dict)

    def clear(self) -> None:
        """
        Remove all loaded knowledge.
        """
        self.data.clear()

    @property
    def is_empty(self) -> bool:
        """
        Returns True when no knowledge is loaded.
        """
        return not self.data

    def get(self, key: str, default: Any = None) -> Any:
        """
        Safe lookup.
        """
        return self.data.get(key, default)