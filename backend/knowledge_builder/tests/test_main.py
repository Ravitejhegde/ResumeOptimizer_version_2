"""
Integration tests for the public Knowledge Builder API.
"""

from __future__ import annotations

from pathlib import Path

from knowledge_builder.main import (
    build_knowledge_store,
    export_knowledge,
    rebuild_knowledge_store,
)
from knowledge_builder.models import KnowledgeStore


def test_build_knowledge_store() -> None:
    """
    Public API should build a KnowledgeStore.
    """
    store = build_knowledge_store()

    assert isinstance(store, KnowledgeStore)


def test_rebuild_knowledge_store() -> None:
    """
    Public rebuild API should return a new KnowledgeStore.
    """
    first = build_knowledge_store()
    second = rebuild_knowledge_store()

    assert isinstance(second, KnowledgeStore)
    assert second is not first


def test_export_knowledge(
    tmp_path: Path,
) -> None:
    """
    Public export API should generate every artifact.
    """
    exported = export_knowledge(tmp_path)

    assert len(exported) == 2

    for file in exported:
        assert file.exists()
        assert file.is_file()


def test_export_contains_expected_files(
    tmp_path: Path,
) -> None:
    """
    Verify exported filenames.
    """
    exported = export_knowledge(tmp_path)

    names = {
        file.name
        for file in exported
    }

    assert "knowledge.json" in names
    assert "knowledge.cache" in names