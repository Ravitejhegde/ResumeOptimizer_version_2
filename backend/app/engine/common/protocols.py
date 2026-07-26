from __future__ import annotations

from typing import Protocol

from app.engine.models.document import Document


class ReaderProtocol(Protocol):
    """
    Reads a document and builds the engine model.
    """

    def read(
        self,
        file_path: str,
    ) -> Document: ...


class AnalyzerProtocol(Protocol):
    """
    Analyzes a document.
    """

    def analyze(
        self,
        document: Document,
    ) -> Document: ...


class PlannerProtocol(Protocol):
    """
    Produces an optimization plan.
    """

    def build_plan(
        self,
        document: Document,
        job_description: str,
    ): ...


class OptimizerProtocol(Protocol):
    """
    Applies optimization to a document.
    """

    def optimize(
        self,
        document: Document,
        plan,
    ) -> Document: ...


class ValidatorProtocol(Protocol):
    """
    Validates an optimized document.
    """

    def validate(
        self,
        original: Document,
        optimized: Document,
    ): ...


class WriterProtocol(Protocol):
    """
    Writes a document to disk.
    """

    def write(
        self,
        document: Document,
        output_path: str,
    ) -> None: ...


class RecoveryProtocol(Protocol):
    """
    Restores engine state after failures.
    """

    def rollback(
        self,
        document: Document,
    ) -> Document: ...