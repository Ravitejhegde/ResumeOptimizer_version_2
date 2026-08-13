"""
Runtime contract for the Knowledge Runtime.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class RuntimeContract(ABC):
    """
    Public runtime interface.

    Every runtime implementation must follow this contract.
    """

    @abstractmethod
    def load(self) -> None:
        """
        Load runtime knowledge.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def is_loaded(self) -> bool:
        """
        Returns True after runtime is loaded.
        """
        raise NotImplementedError