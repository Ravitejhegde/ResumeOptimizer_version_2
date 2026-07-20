from app.services.intelligence.technology.matcher import (
    TechnologyMatcher,
)


class DuplicateCleaner:
    """
    Removes duplicate technologies, lines, and bullet points.
    """

    @classmethod
    def clean(
        cls,
        blocks,
    ):

        for block in blocks:

            lines = []

            seen = set()

            for line in block.text.split("\n"):

                normalized = line.strip().lower()

                if not normalized:
                    continue

                if normalized in seen:
                    continue

                seen.add(normalized)

                lines.append(line)

            block.text = "\n".join(lines)

        return blocks