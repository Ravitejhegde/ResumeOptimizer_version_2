"""
app.ai.parser.ai_response_parser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Parses AI-generated text into structured content.
"""

from __future__ import annotations


class AIResponseParser:
    """
    Parses AI responses.

    MVP:
    Converts multiline AI output into
    clean bullet points.
    """

    def parse_bullets(
        self,
        text: str,
    ) -> list[str]:
        """
        Parse AI output into bullet points.
        """

        bullets: list[str] = []

        for line in text.splitlines():

            line = line.strip()

            if not line:
                continue

            # Remove common bullet prefixes
            while (
                line.startswith("-")
                or line.startswith("*")
                or line.startswith("•")
            ):
                line = line[1:].strip()

            # Ignore conversational responses
            if line.casefold().startswith(
                (
                    "here",
                    "hope",
                    "certainly",
                    "sure",
                    "note:",
                )
            ):
                continue

            bullets.append(line)

        return bullets