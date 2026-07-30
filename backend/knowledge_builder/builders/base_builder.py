"""
knowledge_builder.builders.base_builder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Base class for every Knowledge Builder component.

A builder transforms an already validated KnowledgeStore into a
derived structure such as indexes, lookup tables, graphs, or caches.

Builders never:
- Read source files
- Modify the KnowledgeStore
- Perform validation
- Export data
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from knowledge_builder.models import KnowledgeStore

T = TypeVar("T")


class BaseBuilder(ABC, Generic[T]):
    """
    Base class for all builders.

    Parameters
    ----------
    store:
        A validated KnowledgeStore.

    Notes
    -----
    Implementations should treat the store as read-only.
    """

    def __init__(self, store: KnowledgeStore) -> None:
        self._store = store

    @property
    def store(self) -> KnowledgeStore:
        """
        Return the validated KnowledgeStore.
        """
        return self._store

    def run(self) -> T:
        """
        Execute the builder.

        Returns
        -------
        T
            The derived structure produced by the builder.
        """
        self.before_build()

        result = self.build()

        self.after_build(result)

        return result

    def before_build(self) -> None:
        """
        Hook executed immediately before build().

        Subclasses may override when needed.
        """
        return

    @abstractmethod
    def build(self) -> T:
        """
        Build and return the derived structure.
        """
        raise NotImplementedError

    def after_build(self, result: T) -> None:
        """
        Hook executed immediately after build().

        Parameters
        ----------
        result:
            The object returned by build().

        Subclasses may override when needed.
        """
        return