from __future__ import annotations

import json

from app.services.ai.batch.batch_models import (
    BatchRewriteResult,
    ParagraphRewriteResult,
)


class BatchResponseParser:
    """
    Parses the JSON returned by the AI after
    batch resume rewriting.
    """

    @staticmethod
    def parse(
        response: str,
        provider: str,
    ) -> BatchRewriteResult:

        try:

            response = response.strip()

            # Remove Markdown code fences if present.
            if response.startswith("```"):
                lines = response.splitlines()

                if lines and lines[0].startswith("```"):
                    lines = lines[1:]

                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]

                response = "\n".join(lines).strip()

            data = json.loads(response)

            paragraphs = []

            for item in data.get("paragraphs", []):

                paragraphs.append(
                    ParagraphRewriteResult(
                        id=item["id"],
                        text=item["text"].strip(),
                    )
                )

            return BatchRewriteResult(
                paragraphs=paragraphs,
                success=True,
                provider=provider,
            )

        except Exception as e:

            print("\n===== BATCH PARSER ERROR =====")
            print(e)
            print("==============================\n")

            return BatchRewriteResult(
                paragraphs=[],
                success=False,
                provider=provider,
            )