from __future__ import annotations


class TechnologyTaxonomy:
    """
    Registry of known technologies.

    Responsibilities
    ----------------
    • Register technologies
    • Lookup technology category
    • Check existence
    • Enumerate technologies

    Never performs normalization.
    Never performs extraction.
    Never performs AI reasoning.
    """

    def __init__(self) -> None:

        self._categories: dict[str, set[str]] = {}

        self._technology_to_category: dict[
            str,
            str,
        ] = {}

    # --------------------------------------------------

    def register(
        self,
        category: str,
        *technologies: str,
    ) -> None:

        values = self._categories.setdefault(
            category,
            set(),
        )

        for technology in technologies:

            technology = technology.strip()

            if not technology:
                continue

            values.add(
                technology
            )

            self._technology_to_category[
                technology.lower()
            ] = category

    # --------------------------------------------------

    def category_of(
        self,
        technology: str,
    ) -> str | None:

        return self._technology_to_category.get(
            technology.lower().strip()
        )

    # --------------------------------------------------

    def exists(
        self,
        technology: str,
    ) -> bool:

        return (
            technology.lower().strip()
            in self._technology_to_category
        )

    # --------------------------------------------------

    def technologies(
        self,
    ) -> list[str]:

        return sorted(

            self._technology_to_category.keys()

        )

    # --------------------------------------------------

    @property
    def categories(
        self,
    ) -> dict[str, list[str]]:

        return {

            category: sorted(values)

            for category, values

            in self._categories.items()

        }




