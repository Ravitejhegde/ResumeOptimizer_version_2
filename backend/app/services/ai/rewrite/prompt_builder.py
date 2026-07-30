from __future__ import annotations

from app.engine.models.ai.prompt_request import (
    ParagraphRewriteRequest,
)


class PromptBuilder:
    """
    Compatibility adapter.

    Converts old single paragraph
    requests into V3 format.
    """


    @staticmethod
    def build(
        request,
    ) -> str:

        paragraph = ParagraphRewriteRequest(

            id="single",

            paragraph_type="unknown",

            text=request.paragraph,

            max_characters=0,

            max_words=request.max_words,

        )

        return (
            "Use BatchPromptBuilder "
            "for production flow."
        )