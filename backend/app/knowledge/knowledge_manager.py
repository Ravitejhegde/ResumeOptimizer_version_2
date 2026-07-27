from __future__ import annotations

from pathlib import Path

from app.knowledge.domains.software_engineering.domain import (
    SoftwareEngineeringDomain,
)


class KnowledgeManager:
    """
    Central entry point for all knowledge domains.

    Every analyzer, planner, optimizer and AI
    service should obtain knowledge through this
    manager.

    Future domains:

    - Medical
    - Finance
    - Legal
    - Agriculture
    - Manufacturing
    """

    def __init__(self) -> None:

        root = (
            Path(__file__).parent
            / "domains"
            / "software_engineering"
        )

        self.software_engineering = (
            SoftwareEngineeringDomain(
                root
            )
        )

    def initialize(self) -> None:

        self.software_engineering.load()

    def get_domain(
        self,
        name: str,
    ):

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