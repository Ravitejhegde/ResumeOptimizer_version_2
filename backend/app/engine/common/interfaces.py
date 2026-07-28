from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from app.engine.models.document.document import Document


class Reader(ABC):
    """
    Base interface for document readers.
    """

    @abstractmethod
    def read(
        self,
        file_path: str,
    ) -> Document:
        """
        Read a document and return the engine model.
        """
        raise NotImplementedError


class Analyzer(ABC):
    """
    Base interface for analyzers.
    """

    @abstractmethod
    def analyze(
        self,
        document: Document,
    ) -> Document:
        """
        Analyze the document.
        """
        raise NotImplementedError


class Planner(ABC):
    """
    Base interface for planners.
    """

    @abstractmethod
    def build_plan(
        self,
        document: Document,
        job_description: str,
    ):
        """
        Build an optimization plan.
        """
        raise NotImplementedError


class Optimizer(ABC):
    """
    Base interface for optimizers.
    """

    @abstractmethod
    def optimize(
        self,
        document: Document,
        plan,
    ) -> Document:
        """
        Optimize the document.
        """
        raise NotImplementedError


class Validator(ABC):
    """
    Base interface for validators.
    """

    @abstractmethod
    def validate(
        self,
        original: Document,
        optimized: Document,
    ):
        """
        Validate optimized document.
        """
        raise NotImplementedError


class Writer(ABC):
    """
    Base interface for writers.
    """

    @abstractmethod
    def write(
        self,
        document: Document,
        output_path: str,
    ) -> None:
        """
        Write document to destination.
        """
        raise NotImplementedError


class Recovery(ABC):
    """
    Base interface for recovery handlers.
    """

    @abstractmethod
    def rollback(
        self,
        document: Document,
    ) -> Document:
        """
        Restore document after failure.
        """
        raise NotImplementedError




