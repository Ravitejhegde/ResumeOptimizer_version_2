from __future__ import annotations

from pathlib import Path

from app.knowledge.domains.software_engineering.domain import (
    SoftwareEngineeringDomain,
)
from app.knowledge.domains.software_engineering.index import (
    TechnologyIndex,
)
from app.knowledge.knowledge_registry import (
    KnowledgeRegistry,
)
from app.knowledge.services.categorizer import (
    SkillCategorizer,
)
from app.knowledge.services.normalizer import (
    SkillNormalizer,
)
from app.knowledge.services.technology_extractor import (
    TechnologyExtractor,
)


class KnowledgeInitializer:
    """
    Builds the complete Knowledge Platform.
    """

    @staticmethod
    def initialize() -> KnowledgeRegistry:

        root = (
            Path(__file__).parent
            / "domains"
            / "software_engineering"
        )

        domain = SoftwareEngineeringDomain(
            root,
        )

        domain.load()

        index = TechnologyIndex(
            domain,
        )

        extractor = TechnologyExtractor(
            index,
        )

        normalizer = SkillNormalizer(
            domain,
        )

        categorizer = SkillCategorizer(
            domain,
        )

        return KnowledgeRegistry(

            software_engineering=domain,

            index=index,

            extractor=extractor,

            normalizer=normalizer,

            categorizer=categorizer,

        )
