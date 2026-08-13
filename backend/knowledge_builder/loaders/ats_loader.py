"""
knowledge_builder.loaders.ats_loader
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Loads ATS rule definitions from the Knowledge Database.

Responsibilities
----------------
- Read ATS rule JSON files
- Convert dictionaries into ATSRule models
- Return strongly typed objects

This loader intentionally does NOT:
- Validate ATS rules
- Build indexes
- Score resumes
- Store data
"""

from __future__ import annotations

from knowledge_builder.config import (
    ATS_RULES_DIRECTORY,
)
from knowledge_builder.loaders.base_loader import BaseLoader
from knowledge_builder.models import ATSRule


class ATSLoader(BaseLoader):
    """
    Loads normalized ATS rules.
    """

    def load(self) -> list[ATSRule]:
        """
        Load every ATS rule from the configured directory.

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
            key=lambda rule: rule.id.casefold()
        )

        return rules

    @classmethod
    def from_default_location(
        cls,
    ) -> "ATSLoader":
        """
        Create a loader using the default Knowledge Database location.
        """
        return cls(ATS_RULES_DIRECTORY)