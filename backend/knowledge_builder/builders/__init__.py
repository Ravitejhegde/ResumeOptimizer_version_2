"""
knowledge_builder.builders
~~~~~~~~~~~~~~~~~~~~~~~~~~

Builders package for the Knowledge Builder.

Builders transform a validated KnowledgeStore into optimized runtime
artifacts such as indexes, graphs, and lookup tables.

Architecture

KnowledgeStore
      │
      ▼
KnowledgeBuilder
      │
      ├── CategoryIndexBuilder
      ├── TechnologyGraphBuilder
      ├── SkillIndexBuilder
      ├── RoleIndexBuilder
      ├── KeywordIndexBuilder
      └── SynonymIndexBuilder
      │
      ▼
KnowledgeArtifacts

Builders never:
- Read raw source files
- Validate knowledge
- Export knowledge
- Modify the KnowledgeStore
"""

from .base_builder import BaseBuilder
from .category_index_builder import (
    CategoryIndex,
    CategoryIndexBuilder,
)
from .knowledge_builder import (
    KnowledgeArtifacts,
    KnowledgeBuilder,
)
from .keyword_index_builder import (
    KeywordIndex,
    KeywordIndexBuilder,
)
from .role_index_builder import (
    RoleIndex,
    RoleIndexBuilder,
)
from .skill_index_builder import (
    SkillIndex,
    SkillIndexBuilder,
)
from .synonym_index_builder import (
    SynonymIndex,
    SynonymIndexBuilder,
)
from .technology_graph_builder import (
    TechnologyGraph,
    TechnologyGraphBuilder,
)

__all__ = [
    "BaseBuilder",

    "CategoryIndex",
    "CategoryIndexBuilder",

    "TechnologyGraph",
    "TechnologyGraphBuilder",

    "SkillIndex",
    "SkillIndexBuilder",

    "RoleIndex",
    "RoleIndexBuilder",

    "KeywordIndex",
    "KeywordIndexBuilder",

    "SynonymIndex",
    "SynonymIndexBuilder",

    "KnowledgeArtifacts",
    "KnowledgeBuilder",
]