from app.services.jd.jd_parser import (
    JDParser,
)

from app.services.jd.skill_comparator import (
    SkillComparator,
)

from app.services.knowledge.knowledge_builder import (
    KnowledgeBuilder,
)

from app.services.docx.parser import (
    DocxParser,
)

from docx import Document


document = Document(
    "storage/temp/Ravitej_Hegde_Resume_Fullstack.docx"
)

blocks = DocxParser.parse(
    document
)

resume = KnowledgeBuilder.build(
    blocks
)

jd = """
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

jd_knowledge = JDParser.parse(
    jd
)

result = SkillComparator.compare(
    resume,
    jd_knowledge,
)

print("=" * 60)

print("MATCHED")
print(sorted(result.matched))

print()

print("MISSING")
print(sorted(result.missing))

print()

print("EXTRA")
print(sorted(result.extra))