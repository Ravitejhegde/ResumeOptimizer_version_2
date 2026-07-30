"""
Tests for the public package structure of Knowledge Builder.
"""

from __future__ import annotations

import knowledge_builder
import knowledge_builder.builders
import knowledge_builder.exporters
import knowledge_builder.loaders
import knowledge_builder.models
import knowledge_builder.pipeline
import knowledge_builder.store
import knowledge_builder.validators

from knowledge_builder.main import (
    build_knowledge_store,
    export_knowledge,
    rebuild_knowledge_store,
)


def test_root_package_imports() -> None:
    """
    Root package should import successfully.
    """
    assert knowledge_builder is not None


def test_models_package_imports() -> None:
    """
    Models package should import successfully.
    """
    assert knowledge_builder.models is not None


def test_loaders_package_imports() -> None:
    """
    Loaders package should import successfully.
    """
    assert knowledge_builder.loaders is not None


def test_store_package_imports() -> None:
    """
    Store package should import successfully.
    """
    assert knowledge_builder.store is not None


def test_validators_package_imports() -> None:
    """
    Validators package should import successfully.
    """
    assert knowledge_builder.validators is not None


def test_builders_package_imports() -> None:
    """
    Builders package should import successfully.
    """
    assert knowledge_builder.builders is not None


def test_pipeline_package_imports() -> None:
    """
    Pipeline package should import successfully.
    """
    assert knowledge_builder.pipeline is not None


def test_exporters_package_imports() -> None:
    """
    Exporters package should import successfully.
    """
    assert knowledge_builder.exporters is not None


def test_public_api_functions_exist() -> None:
    """
    Public API should expose the expected functions.
    """
    assert callable(build_knowledge_store)
    assert callable(rebuild_knowledge_store)
    assert callable(export_knowledge)


def test_public_packages_expose_symbols() -> None:
    """
    Public packages should expose exported symbols.
    """
    assert len(dir(knowledge_builder.models)) > 0
    assert len(dir(knowledge_builder.loaders)) > 0
    assert len(dir(knowledge_builder.store)) > 0
    assert len(dir(knowledge_builder.validators)) > 0
    assert len(dir(knowledge_builder.builders)) > 0
    assert len(dir(knowledge_builder.exporters)) > 0
    assert len(dir(knowledge_builder.pipeline)) > 0