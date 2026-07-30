"""
End-to-end integration tests for the complete Knowledge Builder.

These tests exercise the entire public pipeline:

Raw Sources
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

from knowledge_builder.builders import (
    KnowledgeArtifacts,
    KnowledgeBuilder,
)
from knowledge_builder.main import (
    build_knowledge_store,
    export_knowledge,
)
from knowledge_builder.models import KnowledgeStore


def test_complete_pipeline_builds_store() -> None:
    """
    Verify the complete pipeline builds a valid KnowledgeStore.
    """
    store = build_knowledge_store()

    assert isinstance(store, KnowledgeStore)


def test_complete_pipeline_builds_artifacts() -> None:
    """
    Verify runtime artifacts are successfully produced.
    """
    store = build_knowledge_store()

    artifacts = KnowledgeBuilder(store).build()

    assert isinstance(
        artifacts,
        KnowledgeArtifacts,
    )


def test_complete_pipeline_exports_files(
    tmp_path: Path,
) -> None:
    """
    Verify exported runtime artifacts exist.
    """
    exported = export_knowledge(tmp_path)

    assert len(exported) == 2

    for file in exported:
        assert file.exists()
        assert file.is_file()


def test_complete_pipeline_exports_expected_files(
    tmp_path: Path,
) -> None:
    """
    Verify default export filenames.
    """
    exported = export_knowledge(tmp_path)

    names = {
        file.name
        for file in exported
    }

    assert names == {
        "knowledge.json",
        "knowledge.cache",
    }


def test_runtime_artifacts_are_not_empty() -> None:
    """
    Ensure every generated runtime artifact contains data structures.
    """
    store = build_knowledge_store()

    artifacts = KnowledgeBuilder(store).build()

    assert artifacts.category_index is not None
    assert artifacts.technology_graph is not None
    assert artifacts.skill_index is not None
    assert artifacts.role_index is not None
    assert artifacts.keyword_index is not None
    assert artifacts.synonym_index is not None


def test_multiple_builds_are_independent() -> None:
    """
    Running the pipeline twice should create independent objects.
    """
    first = build_knowledge_store()
    second = build_knowledge_store()

    assert first is not second

    first_artifacts = KnowledgeBuilder(first).build()
    second_artifacts = KnowledgeBuilder(second).build()

    assert first_artifacts is not second_artifacts