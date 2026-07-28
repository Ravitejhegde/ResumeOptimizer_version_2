from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class RoleProfile:
    """
    Represents a normalized job role.
    """

    id: str

    name: str

    required_skills: frozenset[str]

    optional_skills: frozenset[str]

    related_roles: frozenset[str]


class RoleMapper:
    """
    Maps skills to software engineering roles.

    Uses the Software Engineering Knowledge Domain.
    """

    def __init__(
        self,
        domain,
    ) -> None:

        self._domain = domain

    # --------------------------------------------------

    def get(
        self,
        role_id: str,
    ) -> dict | None:

        return self._domain.role(
            role_id,
        )

    # --------------------------------------------------

    def exists(
        self,
        role_id: str,
    ) -> bool:

        return self.get(
            role_id,
        ) is not None

    # --------------------------------------------------

    def all_roles(
        self,
    ) -> list[str]:

        return sorted(

            role["id"]

            for role in self._domain.roles.roles

        )

    # --------------------------------------------------

    def detect(
        self,
        skills: list[str],
    ) -> dict | None:
        """
        Detect the best matching role based on
        required skills overlap.
        """

        skill_set = {

            skill.lower()

            for skill in skills

        }

        best_role = None

        best_score = -1

        for role in self._domain.roles.roles:

            required = {

                skill.lower()

                for skill in role.get(
                    "required_skills",
                    [],
                )

            }

            score = len(
                skill_set.intersection(
                    required,
                )
            )

            if score > best_score:

                best_score = score

                best_role = role

        return best_role
