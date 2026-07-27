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
    Central knowledge registry.

    All analyzers, planners and optimizers
    share the same knowledge instance.
    """

    def __init__(self) -> None:

        self.taxonomy = TechnologyTaxonomy()

        self.synonyms = SynonymDictionary()

        self.graph = TechnologyGraph()

        self.roles = RoleMapper()

        self.transitions = TransitionRules()

        self.section_rules = SectionRules()

        self.normalizer = SkillNormalizer(
            self.synonyms
        )

        self.categorizer = SkillCategorizer(
            self.taxonomy
        )

    def initialize(self) -> None:

        self._load_taxonomy()

        self._load_synonyms()

    # --------------------------------------------------

    def _load_taxonomy(
        self,
    ) -> None:

        # -----------------------------
        # Programming Languages
        # -----------------------------

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

        # -----------------------------
        # Backend
        # -----------------------------

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

        # -----------------------------
        # AI / ML
        # -----------------------------

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

        # -----------------------------
        # Database
        # -----------------------------

        self.taxonomy.register(
            "Database",
            "PostgreSQL",
            "MySQL",
            "MongoDB",
            "Redis",
        )

        # -----------------------------
        # Cloud
        # -----------------------------

        self.taxonomy.register(
            "Cloud",
            "AWS",
            "Azure",
            "GCP",
            "Firebase",
        )

        # -----------------------------
        # DevOps
        # -----------------------------

        self.taxonomy.register(
            "DevOps",
            "Docker",
            "Kubernetes",
            "Git",
            "GitHub",
            "CI/CD",
        )

        # -----------------------------
        # Libraries
        # -----------------------------

        self.taxonomy.register(
            "Libraries",
            "NumPy",
            "Pandas",
            "Streamlit",
            "OpenAI",
            "Postman",
        )

    # --------------------------------------------------

    def _load_synonyms(
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
            "speech recognition",
            "asr",
        )

        self.synonyms.register(
            "text to speech",
            "tts",
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

        self.synonyms.register(
            "continuous integration",
            "ci",
        )

        self.synonyms.register(
            "continuous delivery",
            "cd",
        )