"""
knowledge_builder.config
~~~~~~~~~~~~~~~~~~~~~~~~

Central configuration for the Knowledge Builder.

Every path used by the builder originates here.

This module is the only place where filesystem locations are defined.
"""

from __future__ import annotations

from pathlib import Path

# ---------------------------------------------------------------------
# Project Root
# ---------------------------------------------------------------------

BACKEND_ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------
# Knowledge Database
# ---------------------------------------------------------------------

KNOWLEDGE_DATABASE = (
    BACKEND_ROOT
    / "knowledge_database"
)

# ---------------------------------------------------------------------
# Export Directory
# ---------------------------------------------------------------------

OUTPUT_DIRECTORY = (
    BACKEND_ROOT
    / "output"
)

# ---------------------------------------------------------------------
# Individual Sources
# ---------------------------------------------------------------------

CATEGORIES_DIRECTORY = (
    KNOWLEDGE_DATABASE
    / "categories"
)

TECHNOLOGIES_DIRECTORY = (
    KNOWLEDGE_DATABASE
    / "technologies"
)



DATA_DIRECTORY = Path(__file__).parent / "data"

SKILLS_DIRECTORY = DATA_DIRECTORY / "skills"

ROLES_DIRECTORY = (
    KNOWLEDGE_DATABASE
    / "roles"
)

RELATIONSHIPS_DIRECTORY = (
    KNOWLEDGE_DATABASE
    / "relationships"
)

ATS_RULES_DIRECTORY = (
    KNOWLEDGE_DATABASE
    / "ats_rules"
)

SECTIONS_DIRECTORY = (
    KNOWLEDGE_DATABASE
    / "sections"
)

SYNONYMS_DIRECTORY = (
    KNOWLEDGE_DATABASE
    / "synonyms"
)

KEYWORDS_DIRECTORY = (
    KNOWLEDGE_DATABASE
    / "keywords"
)

RESUME_PATTERNS_DIRECTORY = (
    KNOWLEDGE_DATABASE
    / "resume_patterns"
)