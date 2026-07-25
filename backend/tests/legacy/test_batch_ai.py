from docx import Document

from app.services.docx.parser import DocxParser
from app.services.knowledge.knowledge_builder import (
    KnowledgeBuilder,
)
from app.services.planner.optimization_planner import (
    OptimizationPlanner,
)
from app.services.ai.batch_ai_service import (
    BatchAIService,
)

# --------------------------------------------------
# Load Resume
# --------------------------------------------------

document = Document(
    "storage/temp/YOUR_FILE.docx"
)

# --------------------------------------------------
# Parse Resume
# --------------------------------------------------

blocks = DocxParser.parse(document)

# --------------------------------------------------
# Build Knowledge
# --------------------------------------------------

knowledge = KnowledgeBuilder.build(blocks)

# --------------------------------------------------
# Select Blocks
# --------------------------------------------------

selected_blocks = OptimizationPlanner.plan(blocks)

# --------------------------------------------------
# Job Description
# --------------------------------------------------

job_description = """
Looking for a Java Backend Developer.

Required Skills

Java
Spring Boot
REST APIs
MySQL
Docker
Git
"""

# --------------------------------------------------
# AI Service
# --------------------------------------------------

service = BatchAIService()

result = service.optimize_resume(
    selected_blocks,
    knowledge,
    job_description,
)

print("=" * 80)

print(result)