from __future__ import annotations

from pathlib import Path

from app.knowledge.domains.software_engineering.domain import (
    SoftwareEngineeringDomain,
)
from app.knowledge.domains.software_engineering.index import (
    TechnologyIndex,
)
from app.knowledge.services.technology_extractor import (
    TechnologyExtractor,
)


class KnowledgeManager:
    """
    Central entry point to the Knowledge Platform.

    All analyzers, planners and optimizers should
    access knowledge only through this manager.
    """

    def __init__(self) -> None:

        root = (
            Path(__file__).parent
            / "domains"
            / "software_engineering"
        )

        self.software_engineering = (
            SoftwareEngineeringDomain(root)
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
            self.software_engineering
        )

        self.extractor = TechnologyExtractor(
            self.index
        )

        self._initialized = True

    # --------------------------------------------------

    def extract(
        self,
        text: str,
    ) -> list[str]:

        self.initialize()

        return self.extractor.extract(
            text
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

        except KeyError:

            raise ValueError(
                f"Unknown knowledge domain: {name}"
            )




