from __future__ import annotations

from app.engine.knowledge.categorizer import (
    SkillCategorizer,
)
from app.engine.knowledge.normalizer import (
    SkillNormalizer,
)
from app.engine.knowledge.role_mapper import (
    RoleMapper,
)
from app.engine.knowledge.section_rules import (
    SectionRules,
)
from app.engine.knowledge.synonyms import (
    SynonymDictionary,
)
from app.engine.knowledge.taxonomy import (
    TechnologyTaxonomy,
)
from app.engine.knowledge.technology_graph import (
    TechnologyGraph,
)
from app.engine.knowledge.transition_rules import (
    TransitionRules,
)


class KnowledgeBase:
    """
    Central knowledge registry for ResumeOptimizer.

    This is the single source of truth for every
    knowledge component used by the engine.

    Analyzer
        ↓
    Planner
        ↓
    Optimizer

    All access the same KnowledgeBase instance.
    """

    def __init__(self) -> None:

        # -----------------------------------------
        # Core Knowledge
        # -----------------------------------------

        self.taxonomy = TechnologyTaxonomy()

        self.synonyms = SynonymDictionary()

        self.graph = TechnologyGraph()

        self.roles = RoleMapper()

        self.transitions = TransitionRules()

        self.section_rules = SectionRules()

        # -----------------------------------------
        # Intelligent Services
        # -----------------------------------------

        self.normalizer = SkillNormalizer(
            self.synonyms
        )

        self.categorizer = SkillCategorizer(
            self.taxonomy
        )

    def initialize(self) -> None:
        """
        Bootstraps the knowledge base.

        Later this method will load

        - Technology taxonomy
        - Synonyms
        - Role profiles
        - Transition rules
        - Technology graph
        - Section rules

        from versioned knowledge datasets.
        """
        pass