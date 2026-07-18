from docx import Document

from app.services.docx.parser import (
    DocxParser,
)

from app.services.knowledge.knowledge_builder import (
    KnowledgeBuilder,
)

from app.services.jd.jd_parser import (
    JDParser,
)

from app.services.jd.skill_comparator import (
    SkillComparator,
)

from app.services.jd.technology_promoter import (
    TechnologyPromoter,
)


document = Document(
    "storage/temp/Ravitej_Hegde_Resume_Fullstack.docx"
)

blocks = DocxParser.parse(
    document
)

resume = KnowledgeBuilder.build(
    blocks
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

jd = JDParser.parse(
    job_description
)

comparison = SkillComparator.compare(
    resume,
    jd,
)

promotion = TechnologyPromoter.build(
    comparison
)

print("=" * 60)

print("PROMOTE")
print(promotion.promote)

print()

print("MISSING")
print(promotion.missing)

print()

print("EXTRA")
print(promotion.extra)