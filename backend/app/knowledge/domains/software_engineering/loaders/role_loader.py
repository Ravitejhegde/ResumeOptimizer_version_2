from __future__ import annotations

import json
from json import JSONDecodeError
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

        for file in sorted(self._path.glob("*.json")):

            if file.stat().st_size == 0:
                print(f"[Knowledge] Skipping empty role file: {file.name}")
                continue

            try:

                with file.open(
                    "r",
                    encoding="utf-8",
                ) as stream:

                    role = json.load(stream)

            except JSONDecodeError:

                print(f"[Knowledge] Invalid JSON: {file.name}")
                continue

            except Exception as ex:

                print(f"[Knowledge] Failed to load {file.name}: {ex}")
                continue

            if not isinstance(role, dict):
                continue

            role_id = role.get("id")

            if not role_id:
                print(f"[Knowledge] Missing role id: {file.name}")
                continue

            self._roles.append(role)

            self._lookup[role_id] = role

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

        return self._lookup.get(role_id)

    def exists(
        self,
        role_id: str,
    ) -> bool:

        return role_id in self._lookup