from __future__ import annotations

from pathlib import Path

from app.knowledge.domains.software_engineering.domain import (
    SoftwareEngineeringDomain,
)
from app.knowledge.domains.software_engineering.index import (
    TechnologyIndex,
)
from app.knowledge.services.categorizer import (
    SkillCategorizer,
)
from app.knowledge.services.normalizer import (
    SkillNormalizer,
)
from app.knowledge.services.synonyms import (
    SynonymDictionary,
)
from app.knowledge.services.taxonomy import (
    TechnologyTaxonomy,
)
from app.knowledge.services.technology_extractor import (
    TechnologyExtractor,
)


class KnowledgeManager:
    """
    Central entry point to the Knowledge Platform.

    All analyzers, planners and optimizers
    access knowledge only through this class.
    """

    def __init__(
        self,
    ) -> None:

        root = (
            Path(__file__).parent
            / "domains"
            / "software_engineering"
        )

        self.software_engineering = (
            SoftwareEngineeringDomain(
                root,
            )
        )

        self._initialized = False

    # --------------------------------------------------

    def initialize(
        self,
    ) -> None:

        if self._initialized:
            return

        self.software_engineering.load()

        self.index = TechnologyIndex(
            self.software_engineering,
        )

        self.extractor = TechnologyExtractor(
            self.index,
        )

        self.taxonomy = TechnologyTaxonomy()

        self.synonyms = SynonymDictionary()

        self._normalizer = SkillNormalizer(
            self.synonyms,
        )

        self._categorizer = SkillCategorizer(
            self.taxonomy,
        )

        self._initialized = True

    # --------------------------------------------------

    def extract(
        self,
        text: str,
    ) -> list[str]:

        self.initialize()

        return self.extractor.extract(
            text,
        )

    # --------------------------------------------------

    def normalize(
        self,
        skill: str,
    ) -> str:

        self.initialize()

        return self._normalizer.normalize(
            skill,
        )

    # --------------------------------------------------

    def normalize_many(
        self,
        skills: list[str],
    ) -> list[str]:

        self.initialize()

        return self._normalizer.normalize_many(
            skills,
        )

    # --------------------------------------------------

    def categorize(
        self,
        skills: list[str],
    ) -> dict[str, list[str]]:

        self.initialize()

        return self._categorizer.categorize(
            skills,
        )

    # --------------------------------------------------

    def get_domain(
        self,
        name: str,
    ):

        self.initialize()

        domains = {
            "software_engineering":
                self.software_engineering,
        }

        try:

            return domains[name]

        except KeyError as exc:

            raise ValueError(
                f"Unknown knowledge domain: {name}"
            ) from exc