"""
Tests for runtime KnowledgeArtifacts.
"""

from __future__ import annotations

from knowledge_builder.builders import (
    KnowledgeArtifacts,
)


def test_artifacts_instance(
    knowledge_artifacts: KnowledgeArtifacts,
) -> None:
    """
    Runtime artifacts should be created successfully.
    """
    assert isinstance(
        knowledge_artifacts,
        KnowledgeArtifacts,
    )


def test_category_index_exists(
    knowledge_artifacts: KnowledgeArtifacts,
) -> None:
    """
    Category index should exist.
    """
    assert knowledge_artifacts.category_index is not None


def test_technology_graph_exists(
    knowledge_artifacts: KnowledgeArtifacts,
) -> None:
    """
    Technology graph should exist.
    """
    assert knowledge_artifacts.technology_graph is not None


def test_skill_index_exists(
    knowledge_artifacts: KnowledgeArtifacts,
) -> None:
    """
    Skill index should exist.
    """
    assert knowledge_artifacts.skill_index is not None


def test_role_index_exists(
    knowledge_artifacts: KnowledgeArtifacts,
) -> None:
    """
    Role index should exist.
    """
    assert knowledge_artifacts.role_index is not None


def test_keyword_index_exists(
    knowledge_artifacts: KnowledgeArtifacts,
) -> None:
    """
    Keyword index should exist.
    """
    assert knowledge_artifacts.keyword_index is not None


def test_synonym_index_exists(
    knowledge_artifacts: KnowledgeArtifacts,
) -> None:
    """
    Synonym index should exist.
    """
    assert knowledge_artifacts.synonym_index is not None


def test_category_index_lookup(
    category_index,
) -> None:
    """
    Category index should expose lookup dictionaries.
    """
    assert hasattr(
        category_index,
        "by_id",
    )

    assert hasattr(
        category_index,
        "by_name",
    )

    assert hasattr(
        category_index,
        "by_alias",
    )


def test_skill_index_lookup(
    skill_index,
) -> None:
    """
    Skill index should expose lookup dictionaries.
    """
    assert hasattr(skill_index, "by_id")
    assert hasattr(skill_index, "by_name")
    assert hasattr(skill_index, "by_alias")
    assert hasattr(skill_index, "by_keyword")
    assert hasattr(skill_index, "by_technology")


def test_role_index_lookup(
    role_index,
) -> None:
    """
    Role index should expose lookup dictionaries.
    """
    assert hasattr(role_index, "by_id")
    assert hasattr(role_index, "by_name")
    assert hasattr(role_index, "by_skill")
    assert hasattr(role_index, "by_keyword")
    assert hasattr(role_index, "by_section")
    assert hasattr(role_index, "by_technology")


def test_keyword_index_lookup(
    keyword_index,
) -> None:
    """
    Keyword index should expose lookup dictionaries.
    """
    assert hasattr(keyword_index, "by_id")
    assert hasattr(keyword_index, "by_value")
    assert hasattr(keyword_index, "by_alias")
    assert hasattr(keyword_index, "by_skill")
    assert hasattr(keyword_index, "by_role")
    assert hasattr(keyword_index, "by_technology")


def test_synonym_index_lookup(
    synonym_index,
) -> None:
    """
    Synonym index should expose lookup dictionaries.
    """
    assert hasattr(
        synonym_index,
        "by_id",
    )

    assert hasattr(
        synonym_index,
        "by_canonical",
    )

    assert hasattr(
        synonym_index,
        "by_alias",
    )


def test_technology_graph_lookup(
    technology_graph,
) -> None:
    """
    Technology graph should expose graph structures.
    """
    assert hasattr(
        technology_graph,
        "nodes",
    )

    assert hasattr(
        technology_graph,
        "edges",
    )