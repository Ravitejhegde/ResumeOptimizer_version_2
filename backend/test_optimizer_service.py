from docx import Document

from app.services.docx.parser import DocxParser
from app.services.optimizer.optimizer_service import OptimizerService


# Load Resume
document = Document("storage/temp/YOUR_FILE.docx")

# Parse Resume
blocks = DocxParser.parse(document)

# Job Description
job_description = """
Looking for a Java Backend Developer.

Skills:
Java
Spring Boot
REST API
Microservices
Docker
Git
SQL
"""

# Optimize
optimizer = OptimizerService()

optimized_blocks = optimizer.optimize(
    blocks,
    job_description,
)

print("=" * 70)

for block in optimized_blocks:

    print(f"[{block.block_type}]")

    print(block.text)

    print("-" * 70)