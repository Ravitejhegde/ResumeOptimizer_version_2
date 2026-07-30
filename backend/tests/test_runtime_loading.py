"""
Tests for loading exported runtime artifacts.
"""

from __future__ import annotations

from pathlib import Path

from knowledge_builder.builders import (
    KnowledgeArtifacts,
)
from knowledge_builder.exporters import (
    CacheExporter,
)
from knowledge_builder.main import (
    build_knowledge_store,
)
from knowledge_builder.pipeline.export_pipeline import (
    ExportPipeline,
)


def test_cache_can_be_loaded(
    tmp_path: Path,
) -> None:
    """
    Exported cache should be loadable.
    """
    store = build_knowledge_store()

    pipeline = ExportPipeline(
        store=store,
        output_directory=tmp_path,
    )

    pipeline.run()

    cache_file = tmp_path / "knowledge.cache"

    artifacts = CacheExporter.load(
        cache_file,
    )

    assert isinstance(
        artifacts,
        KnowledgeArtifacts,
    )


def test_cache_file_exists(
    tmp_path: Path,
) -> None:
    """
    Cache file should exist after export.
    """
    store = build_knowledge_store()

    ExportPipeline(
        store=store,
        output_directory=tmp_path,
    ).run()

    assert (tmp_path / "knowledge.cache").exists()


def test_json_file_exists(
    tmp_path: Path,
) -> None:
    """
    JSON export should exist after export.
    """
    store = build_knowledge_store()

    ExportPipeline(
        store=store,
        output_directory=tmp_path,
    ).run()

    assert (tmp_path / "knowledge.json").exists()


def test_loaded_artifacts_have_indexes(
    tmp_path: Path,
) -> None:
    """
    Loaded artifacts should expose every runtime index.
    """
    store = build_knowledge_store()

    ExportPipeline(
        store=store,
        output_directory=tmp_path,
    ).run()

    artifacts = CacheExporter.load(
        tmp_path / "knowledge.cache",
    )

    assert artifacts.category_index is not None
    assert artifacts.technology_graph is not None
    assert artifacts.skill_index is not None
    assert artifacts.role_index is not None
    assert artifacts.keyword_index is not None
    assert artifacts.synonym_index is not None


def test_loaded_artifacts_are_independent(
    tmp_path: Path,
) -> None:
    """
    Multiple cache loads should return different objects.
    """
    store = build_knowledge_store()

    ExportPipeline(
        store=store,
        output_directory=tmp_path,
    ).run()

    first = CacheExporter.load(
        tmp_path / "knowledge.cache",
    )

    second = CacheExporter.load(
        tmp_path / "knowledge.cache",
    )

    assert first is not second


def test_cache_preserves_runtime_types(
    tmp_path: Path,
) -> None:
    """
    Runtime cache should preserve object types.
    """
    store = build_knowledge_store()

    ExportPipeline(
        store=store,
        output_directory=tmp_path,
    ).run()

    artifacts = CacheExporter.load(
        tmp_path / "knowledge.cache",
    )

    assert isinstance(
        artifacts,
        KnowledgeArtifacts,
    )

    assert isinstance(
        artifacts.category_index.by_id,
        dict,
    )

    assert isinstance(
        artifacts.skill_index.by_id,
        dict,
    )

    assert isinstance(
        artifacts.role_index.by_id,
        dict,
    )

    assert isinstance(
        artifacts.keyword_index.by_id,
        dict,
    )

    assert isinstance(
        artifacts.synonym_index.by_id,
        dict,
    )