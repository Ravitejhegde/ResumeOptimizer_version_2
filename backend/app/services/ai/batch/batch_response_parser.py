from __future__ import annotations

import json
import logging

from app.engine.models.ai.prompt_response import (
    BatchRewriteResult,
    ParagraphRewriteResult,
)


logger = logging.getLogger(__name__)


class BatchResponseParser:
    """
    Parses AI batch rewrite responses.

    Responsibilities:
        - Remove formatting noise.
        - Parse JSON.
        - Validate paragraph results.

    Does not:
        - Rewrite content.
        - Validate document layout.
    """


    @staticmethod
    def parse(
        response: str,
        provider: str,
    ) -> BatchRewriteResult:

        try:

            cleaned = (
                response
                .strip()
            )


            # ----------------------------------
            # Remove markdown fences
            # ----------------------------------

            if cleaned.startswith(
                "```"
            ):

                lines = (
                    cleaned
                    .splitlines()
                )

                if lines[0].startswith(
                    "```"
                ):
                    lines = lines[1:]


                if lines and lines[-1].startswith(
                    "```"
                ):
                    lines = lines[:-1]


                cleaned = (
                    "\n".join(lines)
                    .strip()
                )


            data = json.loads(
                cleaned
            )


            results: list[
                ParagraphRewriteResult
            ] = []


            seen_ids: set[str] = set()


            for item in data.get(
                "paragraphs",
                [],
            ):


                paragraph_id = (
                    item.get("id")
                )


                text = (
                    item.get("text")
                )


                if not paragraph_id:
                    continue


                if paragraph_id in seen_ids:

                    logger.warning(
                        "Duplicate AI paragraph id: %s",
                        paragraph_id,
                    )

                    continue


                if text is None:

                    continue


                seen_ids.add(
                    paragraph_id
                )


                results.append(

                    ParagraphRewriteResult(

                        id=paragraph_id,

                        text=text.strip(),

                    )

                )


            return BatchRewriteResult(

                paragraphs=results,

                success=True,

                provider=provider,

            )


        except json.JSONDecodeError:

            logger.exception(
                "AI returned invalid JSON"
            )


        except Exception:

            logger.exception(
                "Batch response parsing failed"
            )


        return BatchRewriteResult(

            paragraphs=[],

            success=False,

            provider=provider,

        )