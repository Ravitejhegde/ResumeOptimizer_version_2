"""
knowledge_builder.store
~~~~~~~~~~~~~~~~~~~~~~~

Store package for the Knowledge Builder.

The store layer is responsible for creating and exposing the
central KnowledgeStore used throughout ResumeOptimizer.

Pipeline

Raw Sources
      │
      ▼
Loaders
      │
      ▼
StoreBuilder
      │
      ▼
KnowledgeStore
      │
      ▼
Analyzer / Planner / Optimizer / Prompt Engine

The store layer does NOT:
- Read source files directly
- Validate knowledge
- Build relationships
- Export knowledge
"""

from .store_builder import StoreBuilder

__all__ = [
    "StoreBuilder",
]