from __future__ import annotations

from dataclasses import dataclass, field

from app.engine.common.enums import SectionType


@dataclass(slots=True, frozen=True)
class SectionRule:
    """
    Defines optimization rules for a resume section.
    """

    section: SectionType

    editable: bool = True

    rename_allowed: bool = False

    reorder_allowed: bool = False

    add_content_allowed: bool = True

    remove_content_allowed: bool = False

    preserve_line_count: bool = True

    preserve_formatting: bool = True

    preserve_hyperlinks: bool = True


class SectionRules:
    """
    Central registry of resume section rules.

    Every optimizer must consult these rules before
    modifying a section.
    """

    def __init__(self) -> None:

        self._rules: dict[
            SectionType,
            SectionRule,
        ] = {}

    def register(
        self,
        rule: SectionRule,
    ) -> None:

        self._rules[
            rule.section
        ] = rule

    def get(
        self,
        section: SectionType,
    ) -> SectionRule | None:

        return self._rules.get(
            section
        )

    def exists(
        self,
        section: SectionType,
    ) -> bool:

        return (
            section
            in self._rules
        )

    def all_rules(
        self,
    ) -> list[SectionRule]:

        return list(
            self._rules.values()
        )




