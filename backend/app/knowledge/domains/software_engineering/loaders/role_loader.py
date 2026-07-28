from __future__ import annotations

import json
from pathlib import Path


class RoleLoader:
    """
    Loads all role definitions.

    Folder structure

    roles/
        backend_developer.json
        frontend_developer.json
        full_stack_developer.json
        ...
    """

    def __init__(
        self,
        path: str | Path,
    ) -> None:

        self._path = Path(path)

        self._roles: list[dict] = []

        self._lookup: dict[str, dict] = {}

    # --------------------------------------------------

    def load(
        self,
    ) -> None:

        self._roles.clear()

        self._lookup.clear()

        if not self._path.exists():

            raise FileNotFoundError(
                f"Roles directory not found: {self._path}"
            )

        for file in sorted(
            self._path.glob("*.json")
        ):

            with file.open(
                "r",
                encoding="utf-8",
            ) as stream:

                role = json.load(stream)

            self._roles.append(
                role,
            )

            self._lookup[
                role["id"]
            ] = role

    # --------------------------------------------------

    @property
    def roles(
        self,
    ) -> list[dict]:

        return self._roles

    # --------------------------------------------------

    def find(
        self,
        role_id: str,
    ) -> dict | None:

        return self._lookup.get(
            role_id,
        )

    def exists(
        self,
        role_id: str,
    ) -> bool:

        return role_id in self._lookup
