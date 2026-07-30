"""
Integration tests for the Knowledge Export Pipeline.
"""

from __future__ import annotations

from pathlib import Path

from knowledge_builder.builders import KnowledgeArtifacts
from knowledge_builder.main import (
    build_knowledge_store,
)
from knowledge_builder.pipeline.export_pipeline import (
    ExportPipeline,
)


def test_build_artifacts() -> None:
    """
    ExportPipeline should successfully build runtime artifacts.
    """
    store = build_knowledge_store()

    pipeline = ExportPipeline(
        store=store,
        output_directory=Path("output"),
    )

    artifacts = pipeline.build_artifacts()

    assert isinstance(
        artifacts,
        KnowledgeArtifacts,
    )


def test_create_export_manager() -> None:
    """
    Default exporters should be registered.
    """
    store = build_knowledge_store()

    pipeline = ExportPipeline(
        store=store,
        output_directory=Path("output"),
    )

    manager = pipeline.create_export_manager()

    assert len(manager) == 2


def test_export_pipeline_creates_files(
    tmp_path: Path,
) -> None:
    """
    Running the pipeline should create JSON and cache files.
    """
    store = build_knowledge_store()

    pipeline = ExportPipeline(
        store=store,
        output_directory=tmp_path,
    )

    exported = pipeline.run()

    assert len(exported) == 2

    for file in exported:
        assert file.exists()
        assert file.is_file()


def test_exported_filenames(
    tmp_path: Path,
) -> None:
    """
    Verify default filenames.
    """
    store = build_knowledge_store()

    pipeline = ExportPipeline(
        store=store,
        output_directory=tmp_path,
    )

    exported = pipeline.run()

    names = {
        file.name
        for file in exported
    }

    assert "knowledge.json" in names
    assert "knowledge.cache" in names


def test_output_directory_created(
    tmp_path: Path,
) -> None:
    """
    Output directory should exist after export.
    """
    output = tmp_path / "knowledge"

    store = build_knowledge_store()

    pipeline = ExportPipeline(
        store=store,
        output_directory=output,
    )

    pipeline.run()

    assert output.exists()
    assert output.is_dir()