from __future__ import annotations

from knowledge_builder.models.category import Category
from knowledge_builder.models.relationship import Relationship
from knowledge_builder.models.source_package import SourcePackage
from knowledge_builder.models.synonym import Synonym
from knowledge_builder.models.technology import Technology


class KnowledgeStore:
    """
    Central in-memory knowledge repository.

    Every builder and validator uses this class.
    """

    def __init__(self) -> None:

        self.categories: dict[str, Category] = {}

        self.technologies: dict[str, Technology] = {}

        self.relationships: list[Relationship] = []

        self.synonyms: list[Synonym] = []

    # --------------------------------------------

    def load(
        self,
        packages: list[SourcePackage],
    ) -> None:

        self.categories.clear()

        self.technologies.clear()

        self.relationships.clear()

        self.synonyms.clear()

        for package in packages:

            self.add_package(package)

    # --------------------------------------------

    def add_package(
        self,
        package: SourcePackage,
    ) -> None:

        category = package.category

        self.categories[
            category.id
        ] = category

        for technology in category.technologies:

            self.technologies[
                technology.id
            ] = technology

        self.relationships.extend(
            package.relationships,
        )

        self.synonyms.extend(
            package.synonyms,
        )

    # --------------------------------------------

    def technology(
        self,
        technology_id: str,
    ) -> Technology | None:

        return self.technologies.get(
            technology_id,
        )

    def category(
        self,
        category_id: str,
    ) -> Category | None:

        return self.categories.get(
            category_id,
        )
    