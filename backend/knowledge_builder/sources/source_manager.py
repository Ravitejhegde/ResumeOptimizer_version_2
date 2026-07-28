from __future__ import annotations

from knowledge_builder.models.source_package import (
    SourcePackage,
)
from knowledge_builder.sources.registry import (
    SourceRegistry,
)


class SourceManager:
    """
    Loads every knowledge source.
    """

    def load_packages(
        self,
    ) -> list[SourcePackage]:

        packages: list[SourcePackage] = []

        for source in SourceRegistry.all():

            packages.append(
                source.load(),
            )

        return packages