import re

from app.services.docx.document_block import DocumentBlock

from app.services.knowledge.resume_knowledge import (
    ResumeKnowledge,
)

from app.services.knowledge.technology_classifier import (
    TechnologyClassifier,
)

from app.services.knowledge.section_detector import (
    SectionDetector,
)

from app.services.knowledge.skill_occurrence import (
    SkillOccurrence,
)


class KnowledgeBuilder:

    @staticmethod
    def build(
        blocks: list[DocumentBlock],
    ) -> ResumeKnowledge:

        knowledge = ResumeKnowledge()

        current_section = "unknown"

        for block in blocks:

            # Detect section headings
            detected = SectionDetector.detect(block.text)

            if detected != "unknown":
                current_section = detected
                continue

            # Extract possible technologies
            words = re.findall(
                r"[A-Za-z0-9.+#-]+(?:\s+[A-Za-z0-9.+#-]+)?",
                block.text,
            )

            for word in words:

                category = TechnologyClassifier.classify(word)

                if category == "frontend":

                    knowledge.frontend.add(word)

                    knowledge.skills.append(

                        SkillOccurrence(

                            name=word,

                            category=category,

                            section=current_section,

                            paragraph_id=block.paragraph_index,

                        )

                )

                elif category == "backend":
                    knowledge.backend.add(word)

                elif category == "database":
                    knowledge.database.add(word)

                elif category == "programming_languages":
                    knowledge.programming_languages.add(word)

                elif category == "cloud":
                    knowledge.cloud.add(word)

                elif category == "devops":
                    knowledge.devops.add(word)

                elif category == "tools":
                    knowledge.tools.add(word)

        return knowledge