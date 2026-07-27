from __future__ import annotations

from dataclasses import dataclass, field

from app.engine.intelligence.technology_graph import (
    TechnologyGraph,
)
from app.engine.models.document import (
    Document,
)


@dataclass(slots=True, frozen=True)
class TechnologyEvidence:
    """
    Evidence collected for a technology.
    """

    technology: str

    occurrences: int

    sections: list[str] = field(
        default_factory=list
    )

    paragraphs: list[str] = field(
        default_factory=list
    )

    strong: bool = False


class EvidenceEngine:
    """
    Searches the resume for evidence that
    supports a technology.

    AI should never promote a technology
    without evidence.
    """

    def __init__(self) -> None:

        self._graph = TechnologyGraph()

    def analyze(
        self,
        document: Document,
        technologies: list[str],
    ) -> dict[str, TechnologyEvidence]:

        evidence: dict[
            str,
            TechnologyEvidence,
        ] = {}

        text_lookup = [

            (
                paragraph.id,
                paragraph.section or "",
                paragraph.text.lower(),
            )

            for paragraph in document.paragraphs

        ]

        for technology in technologies:

            node = self._graph.get(
                technology
            )

            if node is None:
                continue

            aliases = [

                node.name.lower(),

                *[
                    alias.lower()

                    for alias in node.aliases

                ],

            ]

            occurrences = 0

            sections: set[str] = set()

            paragraphs: list[str] = []

            for paragraph_id, section, text in text_lookup:

                matched = False

                for alias in aliases:

                    if alias in text:

                        occurrences += 1

                        matched = True

                if matched:

                    sections.add(section)

                    paragraphs.append(
                        paragraph_id
                    )

            evidence[node.name] = TechnologyEvidence(

                technology=node.name,

                occurrences=occurrences,

                sections=sorted(
                    sections
                ),

                paragraphs=paragraphs,

                strong=(
                    occurrences >= 2
                    or
                    "experience" in {
                        s.lower()
                        for s in sections
                    }
                    or
                    "projects" in {
                        s.lower()
                        for s in sections
                    }
                ),

            )

        return evidence




