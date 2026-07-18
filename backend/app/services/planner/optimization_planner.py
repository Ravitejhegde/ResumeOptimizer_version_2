import re

from app.services.docx.document_block import DocumentBlock


class OptimizationPlanner:

    @staticmethod
    def plan(
        blocks: list[DocumentBlock],
    ) -> list[DocumentBlock]:

        selected = []

        for block in blocks:

            if not block.can_optimize:
                continue

            text = block.text.strip()

            if len(text) < 60:
                continue

            lower = text.lower()

            # Skip contact information
            if "@" in text:
                continue

            if "linkedin" in lower or "github" in lower:
                continue

            # Skip technology lists
            if "technologies:" in lower:
                continue

            if "programming languages:" in lower:
                continue

            if "tools & platforms:" in lower:
                continue

            if "frontend technologies:" in lower:
                continue

            if "backend technologies:" in lower:
                continue

            # Skip keyword-only lines
            if text.count("•") >= 2:
                continue

            selected.append(block)

        return selected