"""
Smoke tests for Knowledge Builder imports.

These tests ensure every public module can be imported without
raising import-time errors or creating circular dependencies.
"""

from __future__ import annotations

import importlib


MODULES = (
    "knowledge_builder",
    "knowledge_builder.main",
    "knowledge_builder.config",
    "knowledge_builder.models",
    "knowledge_builder.loaders",
    "knowledge_builder.store",
    "knowledge_builder.validators",
    "knowledge_builder.builders",
    "knowledge_builder.exporters",
    "knowledge_builder.pipeline",
)


def test_public_modules_import() -> None:
    """
    Every public package should import successfully.
    """
    for module in MODULES:
        imported = importlib.import_module(module)

        assert imported is not None


def test_builder_modules_import() -> None:
    """
    Builder modules should import successfully.
    """
    modules = (
        "knowledge_builder.builders.base_builder",
        "knowledge_builder.builders.category_index_builder",
        "knowledge_builder.builders.technology_graph_builder",
        "knowledge_builder.builders.skill_index_builder",
        "knowledge_builder.builders.role_index_builder",
        "knowledge_builder.builders.keyword_index_builder",
        "knowledge_builder.builders.synonym_index_builder",
        "knowledge_builder.builders.knowledge_builder",
    )

    for module in modules:
        assert importlib.import_module(module) is not None


def test_loader_modules_import() -> None:
    """
    Loader modules should import successfully.
    """
    modules = (
        "knowledge_builder.loaders.base_loader",
        "knowledge_builder.loaders.category_loader",
        "knowledge_builder.loaders.technology_loader",
        "knowledge_builder.loaders.skill_loader",
        "knowledge_builder.loaders.role_loader",
        "knowledge_builder.loaders.section_loader",
        "knowledge_builder.loaders.relationship_loader",
        "knowledge_builder.loaders.keyword_loader",
        "knowledge_builder.loaders.synonym_loader",
        "knowledge_builder.loaders.ats_loader",
    )

    for module in modules:
        assert importlib.import_module(module) is not None


def test_validator_modules_import() -> None:
    """
    Validator modules should import successfully.
    """
    modules = (
        "knowledge_builder.validators.knowledge_validator",
        "knowledge_builder.validators.store_validator",
    )

    for module in modules:
        assert importlib.import_module(module) is not None


def test_exporter_modules_import() -> None:
    """
    Exporter modules should import successfully.
    """
    modules = (
        "knowledge_builder.exporters.base_exporter",
        "knowledge_builder.exporters.json_exporter",
        "knowledge_builder.exporters.cache_exporter",
        "knowledge_builder.exporters.export_manager",
    )

    for module in modules:
        assert importlib.import_module(module) is not None


def test_pipeline_modules_import() -> None:
    """
    Pipeline modules should import successfully.
    """
    modules = (
        "knowledge_builder.pipeline.build_pipeline",
        "knowledge_builder.pipeline.export_pipeline",
    )

    for module in modules:
        assert importlib.import_module(module) is not None