from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class RoleTransition:
    """
    Represents an allowed career transition.

    Example:
        AI Engineer -> Full Stack Developer
        Java Developer -> Backend Developer
        Accountant -> Financial Analyst
    """

    source_role: str

    target_role: str

    transferable_skills: frozenset[str] = frozenset()

    suggested_skills: frozenset[str] = frozenset()

    forbidden_replacements: frozenset[str] = frozenset()

    confidence: float = 1.0


class TransitionRules:
    """
    Registry of role transition rules.

    The Planner consults this registry before
    creating an optimization plan.

    It ensures career transitions remain realistic.
    """

    def __init__(self) -> None:

        self._rules: dict[
            tuple[str, str],
            RoleTransition,
        ] = {}

    @staticmethod
    def _key(
        source: str,
        target: str,
    ) -> tuple[str, str]:

        return (
            source.strip().lower(),
            target.strip().lower(),
        )

    def register(
        self,
        rule: RoleTransition,
    ) -> None:

        self._rules[
            self._key(
                rule.source_role,
                rule.target_role,
            )
        ] = rule

    def get(
        self,
        source_role: str,
        target_role: str,
    ) -> RoleTransition | None:

        return self._rules.get(

            self._key(
                source_role,
                target_role,
            )

        )

    def exists(
        self,
        source_role: str,
        target_role: str,
    ) -> bool:

        return (

            self._key(
                source_role,
                target_role,
            )

            in self._rules

        )

    def all_rules(
        self,
    ) -> list[RoleTransition]:

        return list(
            self._rules.values()
        )