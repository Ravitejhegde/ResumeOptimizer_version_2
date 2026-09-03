from __future__ import annotations

from pathlib import Path

from app.knowledge.domains.software_engineering.loaders.graph_loader import (
    GraphLoader,
)
from app.knowledge.domains.software_engineering.loaders.metadata_loader import (
    MetadataLoader,
)
from app.knowledge.domains.software_engineering.loaders.role_loader import (
    RoleLoader,
)
from app.knowledge.domains.software_engineering.loaders.section_loader import (
    SectionLoader,
)
from app.knowledge.domains.software_engineering.loaders.synonym_loader import (
    SynonymLoader,
)
from app.knowledge.domains.software_engineering.loaders.taxonomy_loader import (
    TaxonomyLoader,
)
from app.knowledge.domains.software_engineering.loaders.profile_loader import (
    ProfileLoader,
)


class SoftwareEngineeringDomain:
    """
    Software Engineering Knowledge Domain.

    Central access point for all software engineering
    knowledge used by analyzers, planners and optimizers.
    """

    def __init__(
        self,
        root: str | Path,
    ) -> None:

        root = Path(root)

        data = root / "data"

        self.metadata = MetadataLoader(
            data / "metadata.json",
        )

        self.taxonomy = TaxonomyLoader(
            data / "taxonomy",
        )

        self.synonyms = SynonymLoader(
            data / "synonyms",
        )

        self.graph = GraphLoader(
            data / "graph",
        )

        self.roles = RoleLoader(
            data / "roles",
        )

        self.profiles = ProfileLoader(
            data / "profiles",
        )

        self.sections = SectionLoader(
            data / "sections",
        )

    # --------------------------------------------------
    # Load Knowledge
    # --------------------------------------------------

    def load(
        self,
    ) -> None:

        loaders = [
            ("metadata", self.metadata.load),
            ("taxonomy", self.taxonomy.load),
            ("synonyms", self.synonyms.load),
            ("graph", self.graph.load),
            ("roles", self.roles.load),
            ("profiles", self.profiles.load),
            ("sections", self.sections.load),
        ]

        for name, loader in loaders:
            try:
                loader()
            except Exception as ex:
                print(f"[Knowledge] Failed to load {name}: {ex}")

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    def metadata_info(
        self,
    ) -> dict:

        return self.metadata.metadata

    # --------------------------------------------------
    # Categories
    # --------------------------------------------------

    def categories(
        self,
    ) -> list[dict]:

        return self.taxonomy.categories

    # --------------------------------------------------
    # Technologies
    # --------------------------------------------------

    def technologies(
        self,
    ) -> dict[str, list[dict]]:

        return self.taxonomy.technologies

    def technology_exists(
        self,
        technology: str,
    ) -> bool:

        return (
            self.taxonomy.category(
                technology.lower(),
            )
            is not None
        )

    # --------------------------------------------------
    # Synonyms
    # --------------------------------------------------

    def canonical(
        self,
        value: str,
    ) -> str:

        return self.synonyms.canonical(
            value,
        )

    # --------------------------------------------------
    # Category Lookup
    # --------------------------------------------------

    def category(
        self,
        technology: str,
    ) -> str | None:

        return self.taxonomy.category(
            technology,
        )

    # --------------------------------------------------
    # Relationships
    # --------------------------------------------------

    def related(
        self,
        technology: str,
    ) -> list[str]:

        return self.graph.related(
            self.canonical(
                technology,
            ),
        )

    # --------------------------------------------------
    # Roles
    # --------------------------------------------------

    def role(
        self,
        role_id: str,
    ) -> dict | None:

        return self.roles.find(
            role_id,
        )

    # --------------------------------------------------
    # Sections
    # --------------------------------------------------

    def section(
        self,
        section_id: str,
    ) -> dict | None:

        return self.sections.get(
            section_id,
        )

    def all_sections(
        self,
    ) -> list[dict]:

        return self.sections.all()
        # --------------------------------------------------
    # Profiles
    # --------------------------------------------------

    def profile(
        self,
        profile_id: str,
    ) -> dict | None:

        return self.profiles.get(
            profile_id,
        )

    def all_profiles(
        self,
    ) -> list[dict]:

        return self.profiles.all()