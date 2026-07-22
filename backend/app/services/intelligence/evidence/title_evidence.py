from app.services.intelligence.evidence.evidence import (
    Evidence,
)


class TitleEvidence:
    """
    Builds evidence from the detected resume role.
    """

    @classmethod
    def build(
        cls,
        detected_role: str,
    ) -> list[Evidence]:

        if not detected_role:
            return []

        if detected_role.lower() == "unknown":
            return []

        return [

            Evidence(

                role=detected_role,

                source="title",

                confidence=100,

                technology=detected_role,

                section="Title",

                explanation="Detected from resume title",

            )

        ]