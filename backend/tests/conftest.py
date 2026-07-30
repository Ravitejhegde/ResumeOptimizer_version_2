"""
Shared pytest fixtures for Knowledge Builder tests.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from knowledge_builder.builders import (
    KnowledgeArtifacts,
    KnowledgeBuilder,
)
from knowledge_builder.main import (
    build_knowledge_store,
)
from knowledge_builder.models import (
    KnowledgeStore,
)


@pytest.fixture(scope="session")
def knowledge_store() -> KnowledgeStore:
    """
    Build a validated KnowledgeStore once for the entire test session.
    """
    return build_knowledge_store()


@pytest.fixture(scope="session")
def knowledge_artifacts(
    knowledge_store: KnowledgeStore,
) -> KnowledgeArtifacts:
    """
    Build runtime artifacts once for the test session.
    """
    return KnowledgeBuilder(
        knowledge_store,
    ).build()


@pytest.fixture
def output_directory(
    tmp_path: Path,
) -> Path:
    """
    Temporary output directory used by exporter tests.
    """
    output = tmp_path / "knowledge_output"
    output.mkdir(
        parents=True,
        exist_ok=True,
    )
    return output


@pytest.fixture
def empty_directory(
    tmp_path: Path,
) -> Path:
    """
    Empty directory for filesystem-related tests.
    """
    directory = tmp_path / "empty"
    directory.mkdir(
        parents=True,
        exist_ok=True,
    )
    return directory


@pytest.fixture
def category_index(
    knowledge_artifacts: KnowledgeArtifacts,
):
    """
    Reusable CategoryIndex fixture.
    """
    return knowledge_artifacts.category_index


@pytest.fixture
def technology_graph(
    knowledge_artifacts: KnowledgeArtifacts,
):
    """
    Reusable TechnologyGraph fixture.
    """
    return knowledge_artifacts.technology_graph


@pytest.fixture
def skill_index(
    knowledge_artifacts: KnowledgeArtifacts,
):
    """
    Reusable SkillIndex fixture.
    """
    return knowledge_artifacts.skill_index


@pytest.fixture
def role_index(
    knowledge_artifacts: KnowledgeArtifacts,
):
    """
    Reusable RoleIndex fixture.
    """
    return knowledge_artifacts.role_index


@pytest.fixture
def keyword_index(
    knowledge_artifacts: KnowledgeArtifacts,
):
    """
    Reusable KeywordIndex fixture.
    """
    return knowledge_artifacts.keyword_index


@pytest.fixture
def synonym_index(
    knowledge_artifacts: KnowledgeArtifacts,
):
    """
    Reusable SynonymIndex fixture.
    """
    return knowledge_artifacts.synonym_index