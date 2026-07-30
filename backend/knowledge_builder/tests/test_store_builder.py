"""
Integration tests for StoreBuilder.

These tests verify that the complete Knowledge Builder pipeline can
construct and validate a KnowledgeStore successfully.
"""

from __future__ import annotations

import pytest

from knowledge_builder.models import KnowledgeStore
from knowledge_builder.store import StoreBuilder


def test_build_returns_knowledge_store() -> None:
    """
    StoreBuilder should return a KnowledgeStore instance.
    """
    builder = StoreBuilder()

    store = builder.build()

    assert isinstance(store, KnowledgeStore)


def test_rebuild_returns_new_store() -> None:
    """
    Rebuild should return a fresh KnowledgeStore instance.
    """
    builder = StoreBuilder()

    first_store = builder.build()
    rebuilt_store = builder.rebuild()

    assert isinstance(rebuilt_store, KnowledgeStore)
    assert rebuilt_store is not first_store


def test_store_property_matches_built_store() -> None:
    """
    Builder.store should reference the most recently built store.
    """
    builder = StoreBuilder()

    store = builder.build()

    assert builder.store is store


def test_store_contains_dictionary_collections() -> None:
    """
    Every collection should exist even when source directories are empty.
    """
    builder = StoreBuilder()

    store = builder.build()

    assert isinstance(store.categories, dict)
    assert isinstance(store.technologies, dict)
    assert isinstance(store.skills, dict)
    assert isinstance(store.roles, dict)
    assert isinstance(store.sections, dict)
    assert isinstance(store.synonyms, dict)
    assert isinstance(store.keywords, dict)
    assert isinstance(store.relationships, dict)
    assert isinstance(store.ats_rules, dict)


def test_total_entities_is_non_negative() -> None:
    """
    Total entities should always be a valid integer.
    """
    builder = StoreBuilder()

    store = builder.build()

    assert isinstance(store.total_entities, int)
    assert store.total_entities >= 0


@pytest.mark.parametrize(
    "attribute",
    [
        "categories",
        "technologies",
        "skills",
        "roles",
        "sections",
        "synonyms",
        "keywords",
        "relationships",
        "ats_rules",
    ],
)
def test_store_has_expected_collections(attribute: str) -> None:
    """
    Ensure every expected collection exists.
    """
    builder = StoreBuilder()

    store = builder.build()

    assert hasattr(store, attribute)