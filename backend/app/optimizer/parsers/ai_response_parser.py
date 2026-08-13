"""
app.optimizer.parsers.ai_response_parser

Parses AI JSON responses into ParagraphUpdate objects.
"""

from __future__ import annotations

import json
import re

from app.optimizer.models.paragraph_update import (
    ParagraphUpdate,
)


class AIResponseParser:
    """
    Converts raw AI responses into
    ParagraphUpdate objects.
    """

    def parse(
        self,
        response: str,
    ) -> list[ParagraphUpdate]:
        """
        Parse the AI response.
        """

        if not response.strip():
            return []

        payload = self._load_json(
            response,
        )

        updates: list[
            ParagraphUpdate
        ] = []

        for item in payload.get(
            "paragraph_updates",
            [],
        ):

            updates.append(
                ParagraphUpdate(
                    paragraph_id=item.get(
                        "paragraph_id",
                        "",
                    ),
                    section=item.get(
                        "section",
                        "",
                    ),
                    original_text=item.get(
                        "original_text",
                        "",
                    ),
                    optimized_text=item.get(
                        "optimized_text",
                        "",
                    ),
                    confidence=float(
                        item.get(
                            "confidence",
                            0.0,
                        )
                    ),
                    reason=item.get(
                        "reason",
                        "",
                    ),
                )
            )

        return updates

    # -------------------------------------------------
    # Helpers
    # -------------------------------------------------

    def _load_json(
        self,
        response: str,
    ) -> dict:
        """
        Extract JSON from common LLM responses.
        """

        response = response.strip()

        # -----------------------------------------
        # Try direct JSON
        # -----------------------------------------

        try:
            return json.loads(
                response,
            )

        except json.JSONDecodeError:
            pass

        # -----------------------------------------
        # Remove Markdown fences
        # -----------------------------------------

        cleaned = (
            response
            .replace(
                "```json",
                "",
            )
            .replace(
                "```",
                "",
            )
            .strip()
        )

        try:
            return json.loads(
                cleaned,
            )

        except json.JSONDecodeError:
            pass

        # -----------------------------------------
        # Extract first JSON object
        # -----------------------------------------

        match = re.search(
            r"\{.*\}",
            cleaned,
            flags=re.DOTALL,
        )

        if match:

            return json.loads(
                match.group(0),
            )

        raise ValueError(
            "AI did not return valid JSON."
        )