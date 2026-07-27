from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class RoleProfile:
    """
    Represents a normalized job role.

    A role defines:
    - Required technologies
    - Optional technologies
    - Related roles
    """

    name: str

    required_skills: frozenset[str] = frozenset()

    optional_skills: frozenset[str] = frozenset()

    related_roles: frozenset[str] = frozenset()


class RoleMapper:
    """
    Maps resumes and job descriptions
    to normalized roles.

    This module NEVER calls AI.

    It only uses the knowledge base.
    """

    def __init__(self) -> None:

        self._roles: dict[str, RoleProfile] = {}

    def register(
        self,
        role: RoleProfile,
    ) -> None:

        self._roles[
            role.name.lower()
        ] = role

    def get(
        self,
        role_name: str,
    ) -> RoleProfile | None:

        return self._roles.get(
            role_name.lower()
        )

    def exists(
        self,
        role_name: str,
    ) -> bool:

        return (
            role_name.lower()
            in self._roles
        )

    def all_roles(
        self,
    ) -> list[str]:

        return sorted(

            role.name

            for role in self._roles.values()

        )

    def detect(
        self,
        skills: list[str],
    ) -> RoleProfile | None:
        """
        Returns the best matching role
        based on overlapping skills.
        """

        skill_set = {

            skill.lower()

            for skill in skills

        }

        best_role = None

        best_score = -1

        for role in self._roles.values():

            score = len(

                skill_set.intersection(

                    role.required_skills

                )

            )

            if score > best_score:

                best_score = score

                best_role = role

        return best_role




