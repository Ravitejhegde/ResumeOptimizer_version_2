"""
knowledge_builder.models.knowledge_package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents the complete knowledge package produced by the
Knowledge Builder.

The package contains both:

1. Raw validated knowledge (KnowledgeStore)
2. Optimized runtime artifacts (KnowledgeArtifacts)

The Runtime never rebuilds knowledge.
It only consumes this package.
"""

from __future__ import annotations

from dataclasses import dataclass

from knowledge_builder.builders.knowledge_builder import KnowledgeArtifacts
from knowledge_builder.models.knowledge_store import KnowledgeStore


@dataclass(slots=True, frozen=True)
class KnowledgePackage:
    """
    Complete package produced by the Knowledge Builder.
    """

    store: KnowledgeStore
    artifacts: KnowledgeArtifacts