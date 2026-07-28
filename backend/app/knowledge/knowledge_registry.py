from __future__ import annotations

from dataclasses import dataclass

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
from app.knowledge.services.technology_extractor import (
    TechnologyExtractor,
)


@dataclass(slots=True)
class KnowledgeRegistry:
    """
    Stores every initialized knowledge component.

    The registry is shared throughout the
    application after initialization.
    """

    software_engineering: SoftwareEngineeringDomain

    index: TechnologyIndex

    extractor: TechnologyExtractor

    normalizer: SkillNormalizer

    categorizer: SkillCategorizer
