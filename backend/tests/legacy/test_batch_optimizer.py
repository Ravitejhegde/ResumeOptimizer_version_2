from docx import Document

from app.services.batch.batch_optimizer import (
    BatchOptimizer,
)

from app.services.docx.parser import (
    DocxParser,
)


document = Document(
    "storage/temp/Ravitej_Hegde_Resume_Fullstack.docx"
)

blocks = DocxParser.parse(
    document
)

job_description = """
Java Backend Developer

Required Skills

Java
Spring Boot
MySQL
Docker
Git
AWS
REST APIs
"""

optimizer = BatchOptimizer()

updated = optimizer.optimize(
    blocks,
    job_description,
)

print("=" * 60)

for block in updated[:10]:

    print(block.id)
    print(block.text)
    print("-" * 60)