from dataclasses import dataclass, field

from app.services.intelligence.detectors.technology_detector import (
    TechnologyDetector,
)


@dataclass
class Summary:

    text: str = ""

    technologies: list[str] = field(
        default_factory=list
    )

    sentences: int = 0

    words: int = 0


class SummaryDetector:
    """
    Extracts the Professional Summary section.
    """

    @classmethod
    def detect(
        cls,
        section_blocks,
    ) -> Summary:

        summary = Summary()

        lines = []

        for item in section_blocks:

            if item["section"] != "SUMMARY":
                continue

            text = item["block"].text.strip()

            if not text:
                continue

            lines.append(text)

            summary.technologies.extend(

                TechnologyDetector.detect(
                    text
                )

            )

        summary.text = "\n".join(lines)

        summary.technologies = sorted(
            set(summary.technologies)
        )

        summary.sentences = len(
            [
                sentence
                for sentence in summary.text.replace(
                    "\n",
                    ".",
                ).split(".")
                if sentence.strip()
            ]
        )

        summary.words = len(
            summary.text.split()
        )

        return summary