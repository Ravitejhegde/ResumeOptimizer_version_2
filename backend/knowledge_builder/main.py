"""
knowledge_builder.main
~~~~~~~~~~~~~~~~~~~~~~

Public entry point for the entire Knowledge Builder.

This module exposes a very small API while hiding the internal
implementation details.

Pipeline

Sources
    │
    ▼
Loaders
    │
    ▼
KnowledgeStore
    │
    ▼
Validators
    │
    ▼
KnowledgeBuilder
    │
    ▼
KnowledgeArtifacts
    │
    ▼
ExportPipeline
"""

from __future__ import annotations


from pathlib import Path


from knowledge_builder.models import (
    KnowledgeStore,
)

from knowledge_builder.pipeline.build_pipeline import (
    BuildPipeline,
)

from knowledge_builder.pipeline.export_pipeline import (
    ExportPipeline,
)



def build_knowledge_store() -> KnowledgeStore:
    """
    Build and validate the KnowledgeStore.

    Returns
    -------
    KnowledgeStore
        Validated knowledge representation.
    """

    pipeline = BuildPipeline()

    return pipeline.run()



def rebuild_knowledge_store() -> KnowledgeStore:
    """
    Rebuild the KnowledgeStore from sources.

    Returns
    -------
    KnowledgeStore
        Freshly rebuilt knowledge store.
    """

    pipeline = BuildPipeline()

    return pipeline.rebuild()



def export_knowledge(
    output_directory: Path | str,
) -> list[Path]:
    """
    Build, validate and export knowledge artifacts.

    Parameters
    ----------
    output_directory:
        Destination directory for generated artifacts.

    Returns
    -------
    list[Path]
        Generated artifact paths.
    """


    store = build_knowledge_store()


    pipeline = ExportPipeline(
        store=store,
        output_directory=output_directory,
    )


    return pipeline.run()



__all__ = [
    "KnowledgeStore",
    "BuildPipeline",
    "ExportPipeline",
    "build_knowledge_store",
    "rebuild_knowledge_store",
    "export_knowledge",
]