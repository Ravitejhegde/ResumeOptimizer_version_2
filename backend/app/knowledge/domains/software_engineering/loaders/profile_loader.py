from __future__ import annotations

import json
from json import JSONDecodeError
from pathlib import Path


class ProfileLoader:
    """
    Loads role-specific knowledge profiles.

    Folder structure:

    profiles/
        full_stack_developer.json
        machine_learning_engineer.json
        ...

    Each file contains:

    {
        "profile": {
            "id": "...",
            "role_id": "...",
            "category_count": 5,
            "categories": [...]
        }
    }
    """

    def __init__(
        self,
        path: str | Path,
    ) -> None:

        self._path = Path(path)

        self._profiles: dict[str, dict] = {}

    # --------------------------------------------------

    def load(
        self,
    ) -> None:

        self._profiles.clear()

        if not self._path.exists():

            raise FileNotFoundError(
                f"Profiles directory not found: {self._path}"
            )

        for file in sorted(
            self._path.glob("*.json")
        ):

            if file.stat().st_size == 0:
                print(
                    f"[Knowledge] Skipping empty profile file: {file.name}"
                )
                continue

            try:

                with file.open(
                    "r",
                    encoding="utf-8",
                ) as stream:

                    data = json.load(stream)

            except JSONDecodeError:

                print(
                    f"[Knowledge] Invalid JSON: {file.name}"
                )
                continue

            except Exception as ex:

                print(
                    f"[Knowledge] Failed to load {file.name}: {ex}"
                )
                continue

            if not isinstance(data, dict):

                print(
                    f"[Knowledge] Invalid profile format: {file.name}"
                )
                continue

            profile = data.get("profile")

            if not isinstance(profile, dict):

                print(
                    f"[Knowledge] Missing 'profile' object: {file.name}"
                )
                continue

            profile_id = profile.get("id")

            if not profile_id:

                print(
                    f"[Knowledge] Missing profile id: {file.name}"
                )
                continue

            self._profiles[profile_id] = profile

    # --------------------------------------------------

    @property
    def profiles(
        self,
    ) -> dict[str, dict]:

        return self._profiles

    # --------------------------------------------------

    def exists(
        self,
        profile_id: str,
    ) -> bool:

        return profile_id in self._profiles

    # --------------------------------------------------

    def get(
        self,
        profile_id: str,
    ) -> dict | None:

        return self._profiles.get(
            profile_id,
        )

    # --------------------------------------------------

    def all(
        self,
    ) -> list[dict]:

        return list(
            self._profiles.values(),
        )