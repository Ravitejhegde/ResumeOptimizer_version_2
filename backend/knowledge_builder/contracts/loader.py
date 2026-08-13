"""
knowledge_builder.contracts.loader
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Base contract for every knowledge loader.

Responsibilities
----------------
- Define a common interface for all loaders.
- Ensure every loader returns domain models.
- Keep StoreBuilder independent from concrete loaders.

Rules
-----
Every loader must:
- Load exactly one knowledge entity type.
- Never modify the KnowledgeStore.
- Never validate the KnowledgeStore.
- Never build relationships.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Iterable, TypeVar


T = TypeVar("T")


class LoaderContract(ABC, Generic[T]):
    """
    Contract implemented by every knowledge loader.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Human readable loader name.
        """
        raise NotImplementedError

    @abstractmethod
    def load(self) -> Iterable[T]:
        """
        Load domain objects.

        Returns
        -------
        Iterable[T]
            Collection of strongly typed domain models.
        """
        raise NotImplementedError