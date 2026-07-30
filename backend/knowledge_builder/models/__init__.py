"""
knowledge_builder.models
~~~~~~~~~~~~~~~~~~~~~~~~

Strongly typed domain models used throughout the Knowledge Builder.

These models represent the normalized knowledge graph that powers
ResumeOptimizer.
"""

from .ats_rule import ATSRule, ATSRuleSeverity
from .category import Category
from .keyword import Keyword
from .knowledge_store import KnowledgeStore
from .metadata import BuildMetadata
from .relationship import Relationship, RelationshipType
from .role import Role
from .section import Section
from .skill import Skill
from .synonym import Synonym
from .technology import Technology

__all__ = [
    "ATSRule",
    "ATSRuleSeverity",
    "BuildMetadata",
    "Category",
    "Keyword",
    "KnowledgeStore",
    "Relationship",
    "RelationshipType",
    "Role",
    "Section",
    "Skill",
    "Synonym",
    "Technology",
]