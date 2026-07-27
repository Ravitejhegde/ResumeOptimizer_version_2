from __future__ import annotations

from app.knowledge.services.categorizer import (
    SkillCategorizer,
)
from app.knowledge.services.normalizer import (
    SkillNormalizer,
)
from app.knowledge.services.role_mapper import (
    RoleMapper,
)
from app.knowledge.services.section_rules import (
    SectionRules,
)
from app.knowledge.services.synonyms import (
    SynonymDictionary,
)
from app.knowledge.services.taxonomy import (
    TechnologyTaxonomy,
)
from app.knowledge.services.technology_graph import (
    TechnologyGraph,
)
from app.knowledge.services.transition_rules import (
    TransitionRules,
)


class KnowledgeManager:
    """
    Central knowledge registry.

    Coordinates all knowledge components.
    """

    def __init__(
        self,
    ) -> None:

        self.taxonomy = TechnologyTaxonomy()

        self.synonyms = SynonymDictionary()

        self.graph = TechnologyGraph()

        self.roles = RoleMapper()

        self.transitions = TransitionRules()

        self.section_rules = SectionRules()

        self.normalizer = SkillNormalizer(
            self.synonyms,
        )

        self.categorizer = SkillCategorizer(
            self.taxonomy,
        )

        self.initialize()

    # --------------------------------------------------

    def initialize(
        self,
    ) -> None:

        self._register_taxonomy()

        self._register_synonyms()

        self._register_graph()

        self._register_roles()

    # --------------------------------------------------

    def _register_taxonomy(
        self,
    ) -> None:

        self.taxonomy.register(
            "Programming Language",
            "Python",
            "Java",
            "JavaScript",
            "TypeScript",
            "C",
            "C++",
            "C#",
            ".NET",
            "SQL",
        )

        self.taxonomy.register(
            "Backend",
            "FastAPI",
            "Flask",
            "Django",
            "Spring Boot",
            "Node.js",
            "Express",
            "REST API",
        )

        self.taxonomy.register(
            "Database",
            "PostgreSQL",
            "MySQL",
            "MongoDB",
            "Redis",
        )

        self.taxonomy.register(
            "Cloud",
            "AWS",
            "Azure",
            "GCP",
            "Firebase",
        )

        self.taxonomy.register(
            "DevOps",
            "Docker",
            "Kubernetes",
            "Git",
            "GitHub",
            "CI/CD",
        )

        self.taxonomy.register(
            "AI / ML",
            "TensorFlow",
            "PyTorch",
            "YOLO",
            "OpenCV",
            "Machine Learning",
            "Deep Learning",
            "Artificial Intelligence",
            "Computer Vision",
            "Natural Language Processing",
            "Scikit Learn",
        )

        self.taxonomy.register(
            "Libraries",
            "NumPy",
            "Pandas",
            "Streamlit",
            "OpenAI",
            "Postman",
        )

    # --------------------------------------------------

    def _register_synonyms(
        self,
    ) -> None:

        self.synonyms.register(
            "artificial intelligence",
            "ai",
        )

        self.synonyms.register(
            "machine learning",
            "ml",
        )

        self.synonyms.register(
            "natural language processing",
            "nlp",
        )

        self.synonyms.register(
            "javascript",
            "js",
        )

        self.synonyms.register(
            "typescript",
            "ts",
        )

        self.synonyms.register(
            "node.js",
            "nodejs",
            "node js",
        )

        self.synonyms.register(
            "rest api",
            "rest",
            "restful api",
            "restful apis",
        )

        self.synonyms.register(
            "postgresql",
            "postgres",
            "postgre sql",
        )

        self.synonyms.register(
            "scikit learn",
            "sklearn",
        )

        self.synonyms.register(
            "computer vision",
            "cv",
        )

    # --------------------------------------------------

    def _register_graph(
        self,
    ) -> None:

        self.graph.add_relationship(
            "FastAPI",
            "Python",
        )

        self.graph.add_relationship(
            "Django",
            "Python",
        )

        self.graph.add_relationship(
            "Flask",
            "Python",
        )

        self.graph.add_relationship(
            "Spring Boot",
            "Java",
        )

        self.graph.add_relationship(
            "Express",
            "Node.js",
        )

        self.graph.add_relationship(
            "TensorFlow",
            "Python",
        )

        self.graph.add_relationship(
            "PyTorch",
            "Python",
        )

    # --------------------------------------------------

    def _register_roles(
        self,
    ) -> None:

        # Will be populated in the next milestone.
        pass




