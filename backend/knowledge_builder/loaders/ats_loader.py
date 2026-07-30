"""
knowledge_builder.loaders.ats_loader
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Loads ATS optimization rules from the knowledge source directory.

Responsibilities
----------------
- Read JSON files.
- Convert dictionaries into ATSRule models.
- Return strongly typed objects.

This loader intentionally does NOT:
- Validate ATS rules.
- Evaluate resumes.
- Score resumes.
- Store knowledge.
"""

from __future__ import annotations

from pathlib import Path

from knowledge_builder.loaders.base_loader import BaseLoader
from knowledge_builder.models import ATSRule


class ATSLoader(BaseLoader):
    """
    Loads ATS optimization rules.
    """

    def load(self) -> list[ATSRule]:
        """
        Load every ATS rule from the configured source directory.

        Returns
        -------
        list[ATSRule]
        """
        rules: list[ATSRule] = []

        for file_path in self.list_json_files():
            data = self.read_json(file_path)

            if isinstance(data, dict):
                rules.append(
                    ATSRule.from_dict(data)
                )

            elif isinstance(data, list):
                rules.extend(
                    ATSRule.from_dict(item)
                    for item in data
                )

            else:
                raise TypeError(
                    f"Unsupported JSON structure in {file_path}"
                )

        rules.sort(
            key=lambda rule: (
                rule.severity.value,
                rule.title.casefold(),
            )
        )

        return rules

    @classmethod
    def from_default_location(cls) -> "ATSLoader":
        """
        Create a loader using the default knowledge source directory.
        """
        source_directory = (
            Path(__file__).resolve().parent.parent
            / "sources"
            / "ats"
        )

        return cls(source_directory)