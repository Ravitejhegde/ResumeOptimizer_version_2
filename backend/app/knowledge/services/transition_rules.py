from __future__ import annotations

from app.knowledge.domains.software_engineering.domain import (
    SoftwareEngineeringDomain,
)


class TransitionRules:
    """
    Provides access to role transition rules.

    The rules are loaded from the Knowledge Platform
    and are used by the Planner before generating
    an optimization strategy.

    This class never stores transition data itself.
    """

    def __init__(
        self,
        domain: SoftwareEngineeringDomain,
    ) -> None:

        self._domain = domain

    # --------------------------------------------------

    def get(
        self,
        source_role: str,
        target_role: str,
    ) -> dict | None:

        return self._domain.transition(
            source_role,
            target_role,
        )

    # --------------------------------------------------

    def exists(
        self,
        source_role: str,
        target_role: str,
    ) -> bool:

        return (
            self.get(
                source_role,
                target_role,
            )
            is not None
        )

    # --------------------------------------------------

    def all_rules(
        self,
    ) -> list[dict]:

        return self._domain.all_transitions()
