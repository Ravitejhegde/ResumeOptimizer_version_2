from __future__ import annotations

from pathlib import Path

from app.knowledge.domains.software_engineering.loaders.graph_loader import (
    GraphLoader,
)
from app.knowledge.domains.software_engineering.loaders.synonym_loader import (
    SynonymLoader,
)
from app.knowledge.domains.software_engineering.loaders.taxonomy_loader import (
    TaxonomyLoader,
)


class SoftwareEngineeringDomain:
    """
    Software Engineering knowledge domain.

    Provides search APIs over the knowledge
    instead of exposing raw JSON.

    Future analyzers should only call these
    methods.
    """

    def __init__(
        self,
        root: str | Path,
    ) -> None:

        root = Path(root)

        data = root / "data"

        self.taxonomy = TaxonomyLoader(
            data / "taxonomy.json"
        )

        self.synonyms = SynonymLoader(
            data / "synonyms.json"
        )

        self.graph = GraphLoader(
            data / "graph.json"
        )

    def load(self) -> None:

        self.taxonomy.load()
        self.synonyms.load()
        self.graph.load()

    # --------------------------------------------------
    # Categories
    # --------------------------------------------------

    def categories(self) -> list[dict]:

        return self.taxonomy.categories

    # --------------------------------------------------
    # Technologies
    # --------------------------------------------------

    def technologies(self) -> dict:

        return self.taxonomy.technologies

    def technology_exists(
        self,
        technology: str,
    ) -> bool:

        technology = technology.lower()

        for technologies in self.taxonomy.technologies.values():

            for item in technologies:

                if item["id"] == technology:

                    return True

        return False

    # --------------------------------------------------
    # Synonyms
    # --------------------------------------------------

    def canonical(
        self,
        value: str,
    ) -> str:

        value = value.lower().strip()

        for item in self.synonyms.synonyms:

            if item["canonical"] == value:

                return value

            if value in item["aliases"]:

                return item["canonical"]

        return value

    # --------------------------------------------------
    # Relationships
    # --------------------------------------------------

    def related(
        self,
        technology: str,
    ) -> list[str]:

        technology = self.canonical(
            technology
        )

        for relation in self.graph.relationships:

            if relation["technology"] == technology:

                return relation["related"]

        return []




