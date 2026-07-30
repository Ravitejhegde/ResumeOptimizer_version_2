from __future__ import annotations

from dataclasses import dataclass



@dataclass(slots=True)
class ResponseLimit:
    """
    Represents AI response generation limits.

    Used before sending request to AI.

    Controls:

        - Maximum tokens.
        - Expected output size.
        - Single-call budget.

    Does NOT:

        - Validate final AI response.
        - Parse AI output.
        - Call AI.
    """


    max_tokens: int

    estimated_words: int

    estimated_sections: int = 0



class ResponseLimits:
    """
    Calculates safe AI response limits.

    Purpose:

        Avoid:
            - Very long responses.
            - Token waste.
            - Unexpected AI output.


    Architecture:

        Context
           |
           v
        ResponseLimits
           |
           v
        PromptBuilder
           |
           v
        OpenRouter


    Note:

        Final response length validation
        will be implemented separately later.
    """



    DEFAULT_WORD_TOKEN_RATIO = 1.3


    DEFAULT_SECTION_BUFFER = 200



    def calculate(
        self,
        expected_words: int,
        sections: int = 1,
    ) -> ResponseLimit:
        """
        Calculate token budget.

        Formula:

            tokens =
            words * ratio + section buffer


        Example:

            1000 words

            =>
            ~1500 tokens
        """


        token_estimate = int(

            expected_words
            *
            self.DEFAULT_WORD_TOKEN_RATIO

        )


        buffer = (

            sections
            *
            self.DEFAULT_SECTION_BUFFER

        )


        max_tokens = (
            token_estimate
            +
            buffer
        )


        return ResponseLimit(

            max_tokens=max_tokens,

            estimated_words=expected_words,

            estimated_sections=sections,

        )



    def from_resume(
        self,
        resume_word_count: int,
        section_count: int,
    ) -> ResponseLimit:
        """
        Calculate complete resume response budget.
        """


        return self.calculate(

            expected_words=resume_word_count,

            sections=section_count,

        )



    def create_instruction(
        self,
        limit: ResponseLimit,
    ) -> str:
        """
        Generate AI output restriction.
        """


        return (

            "Return only the required optimized resume data. "

            f"Expected maximum output size: "
            f"{limit.estimated_words} words. "

            "Do not add explanations, comments, "
            "or unnecessary content."

        )