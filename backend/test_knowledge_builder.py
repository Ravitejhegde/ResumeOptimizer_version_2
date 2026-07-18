from docx import Document

from app.services.docx.parser import DocxParser
from app.services.knowledge.knowledge_builder import (
    KnowledgeBuilder,
)

# Load Resume
document = Document("storage/temp/YOUR_FILE.docx")

# Parse Resume
blocks = DocxParser.parse(document)

# Build Knowledge
knowledge = KnowledgeBuilder.build(blocks)

print("=" * 60)

print(knowledge)