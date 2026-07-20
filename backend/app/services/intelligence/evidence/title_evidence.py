from app.services.intelligence.evidence.evidence import Evidence


class TitleEvidence:

    @classmethod
    def build(
        cls,
        detected_role: str,
    ) -> list[Evidence]:

        if not detected_role or detected_role == "Unknown":
            return []

        return [

            Evidence(

                role=detected_role,

                source="title",

                confidence=100,

                explanation="Detected from resume title",

            )

        ]