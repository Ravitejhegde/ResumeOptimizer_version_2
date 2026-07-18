class BlockClassifier:
    """
    Classifies a paragraph into a logical resume block.
    """

    @staticmethod
    def classify(
        *,
        text: str,
        style: str,
        current_section: str,
    ) -> tuple[str, bool]:

        upper = text.strip().upper()

        block_type = "description"
        can_optimize = True

        if "Heading" in style:
            return "heading", False

        if "Title" in style:
            return "title", False

        if upper == current_section:
            return "section", False

        if current_section == "PROJECTS":

            if "•" in text:
                return "technology", False

            if len(text) < 70:
                return "project", False

        if current_section == "INTERNSHIP EXPERIENCE":

            if "|" in text or "–" in text:
                return "company", False

        if current_section == "SKILLS":
            return "skills", False

        if current_section == "EDUCATION":
            return "education", False

        if text.strip().startswith(("•", "-", "·")):
            return "bullet", True

        return block_type, can_optimize