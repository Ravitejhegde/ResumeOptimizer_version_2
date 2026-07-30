from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class AIPrompt:
    """
    Represents the final prompt payload sent to AI.

    This is the bridge between:

        Context Builders
              |
              v
        Prompt Builder
              |
              v
        AI Provider


    Responsibilities:

        - Store structured AI messages.
        - Store prompt metadata.
        - Track generation settings.


    Does NOT:

        - Build prompt content.
        - Call AI.
        - Parse AI response.
    """


    # --------------------------------------------------
    # Chat messages
    # --------------------------------------------------

    messages: list[dict[str, str]] = field(
        default_factory=list,
    )


    # --------------------------------------------------
    # Generation configuration
    # --------------------------------------------------

    model: str | None = None

    temperature: float = 0.2

    max_tokens: int | None = None


    # --------------------------------------------------
    # Purpose tracking
    # --------------------------------------------------

    task: str = (
        "resume_optimization"
    )


    version: str = (
        "v1"
    )


    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    metadata: dict[str, str] = field(
        default_factory=dict,
    )


    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def add_message(
        self,
        role: str,
        content: str,
    ) -> None:
        """
        Add AI conversation message.
        """

        self.messages.append(
            {
                "role": role,
                "content": content,
            }
        )



    def has_messages(
        self,
    ) -> bool:
        """
        Check prompt readiness.
        """

        return bool(
            self.messages
        )



    def system_message(
        self,
    ) -> str | None:
        """
        Return system instruction.
        """

        for message in self.messages:

            if message["role"] == "system":

                return message["content"]

        return None



    def user_message(
        self,
    ) -> str | None:
        """
        Return user payload.
        """

        for message in self.messages:

            if message["role"] == "user":

                return message["content"]

        return None