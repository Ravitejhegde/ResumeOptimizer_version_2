from docx import Document

from app.services.docx.parser import DocxParser
from app.services.planner.optimization_planner import (
    OptimizationPlanner,
)
from app.services.knowledge.knowledge_builder import (
    KnowledgeBuilder,
)
from app.services.batch.batch_prompt_builder import (
    BatchPromptBuilder,
)

# --------------------------------------------------
# Load Resume
# --------------------------------------------------

document = Document("storage/temp/YOUR_FILE.docx")

# --------------------------------------------------
# Parse Resume
# --------------------------------------------------

blocks = DocxParser.parse(document)

# --------------------------------------------------
# Build Resume Knowledge
# --------------------------------------------------

knowledge = KnowledgeBuilder.build(blocks)

# --------------------------------------------------
# Select Important Blocks
# --------------------------------------------------

selected_blocks = OptimizationPlanner.plan(blocks)

# --------------------------------------------------
# Job Description
# --------------------------------------------------

job_description = """
Looking for a Java Backend Developer.

Required Skills:
- Java
- Spring Boot
- REST APIs
- MySQL
- Docker
- Git
"""

# --------------------------------------------------
# Build AI Prompt
# --------------------------------------------------

prompt = BatchPromptBuilder.build(
    selected_blocks,
    knowledge,
    job_description,
)

# --------------------------------------------------
# Print Prompt
# --------------------------------------------------

print("=" * 80)
print(prompt)