"""
Regression tests for the Knowledge Builder public API.

These tests protect the external API and core behavior from
unintentional breaking changes.
"""

from __future__ import annotations

from pathlib import Path

from knowledge_builder.builders import KnowledgeArtifacts
from knowledge_builder.exporters import CacheExporter
from knowledge_builder.main import (
    build_knowledge_store,
    export_knowledge,
    rebuild_knowledge_store,
)
from knowledge_builder.models import KnowledgeStore


def test_build_returns_knowledge_store() -> None:
    """
    Public build API must always return KnowledgeStore.
    """
    store = build_knowledge_store()

    assert isinstance(store, KnowledgeStore)


def test_rebuild_returns_new_instance() -> None:
    """
    Rebuild must always return a fresh store.
    """
    first = build_knowledge_store()
    second = rebuild_knowledge_store()

    assert first is not second


def test_export_returns_file_list(
    tmp_path: Path,
) -> None:
    """
    Export API should always return a list of output files.
    """
    exported = export_knowledge(tmp_path)

    assert isinstance(exported, list)
    assert len(exported) >= 2


def test_default_export_files_exist(
    tmp_path: Path,
) -> None:
    """
    Default export filenames should remain stable.
    """
    export_knowledge(tmp_path)

    assert (tmp_path / "knowledge.json").exists()
    assert (tmp_path / "knowledge.cache").exists()


def test_cache_round_trip(
    tmp_path: Path,
) -> None:
    """
    Cache export/import should preserve artifact type.
    """
    export_knowledge(tmp_path)

    artifacts = CacheExporter.load(
        tmp_path / "knowledge.cache",
    )

    assert isinstance(
        artifacts,
        KnowledgeArtifacts,
    )


def test_multiple_builds_do_not_share_state() -> None:
    """
    Separate builds must remain independent.
    """
    first = build_knowledge_store()
    second = build_knowledge_store()

    assert first is not second


def test_export_directory_created(
    tmp_path: Path,
) -> None:
    """
    Export API should create the output directory if needed.
    """
    output = tmp_path / "runtime"

    export_knowledge(output)

    assert output.exists()
    assert output.is_dir()


def test_public_api_is_stable() -> None:
    """
    Public API functions should remain callable.
    """
    assert callable(build_knowledge_store)
    assert callable(rebuild_knowledge_store)
    assert callable(export_knowledge)